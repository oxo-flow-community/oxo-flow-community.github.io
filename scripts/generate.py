#!/usr/bin/env python3
"""Regenerate the catalog from data/pipelines.json (registry v2).

The registry is self-contained — every entry carries its quickstart,
fidelity notes and requirements — and validate() fails loudly on broken
entries (missing fields, non-executable quickstarts, `--config`, references
to workflow files that do not exist in the staging tree when it is present).
The script emits:

  docs/javascripts/pipelines-data.js   data consumed by the catalog renderer
  docs/pipelines/<name>.md             one run-notes page per workflow

The generated files are committed, so CI only runs `mkdocs build`.
"""
from __future__ import annotations

import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "pipelines.json"
CONFIGS = ROOT / "data" / "configs.json"
OUT_JS = ROOT / "docs" / "javascripts" / "pipelines-data.js"
OUT_PAGES = ROOT / "docs" / "pipelines"
STAGING = pathlib.Path.home() / "Documents" / "GitHub" / "oxo-community" / "staging"

# Engine tarball used in every install snippet (data/pipelines.json engine
# floor is 0.12.0). "latest" tracks the newest release and needs no per-release
# edits; to pin an exact version instead, set ENGINE_VERSION to the tag
# (e.g. "v0.12.0") and use the release asset name oxo-flow-<tag>-<target>.tar.gz
# (https://github.com/Traitome/oxo-flow/releases/download/v0.12.0/
#  oxo-flow-v0.12.0-x86_64-unknown-linux-gnu.tar.gz).
ENGINE_VERSION = "latest"
ENGINE_TARGET = "x86_64-unknown-linux-gnu"
ENGINE_URL = (
    f"https://github.com/Traitome/oxo-flow/releases/"
    f"{'latest/download' if ENGINE_VERSION == 'latest' else f'download/{ENGINE_VERSION}'}/"
    f"oxo-flow-{ENGINE_VERSION}-{ENGINE_TARGET}.tar.gz"
)


def load() -> list[dict]:
    return json.loads(DATA.read_text())


def load_configs() -> dict:
    """Committed `oxo-flow info` output per pipeline (see regen-configs.py)."""
    if not CONFIGS.is_file():
        return {}
    return json.loads(CONFIGS.read_text())


def _esc(value) -> str:
    """HTML-escape a registry value for raw-HTML panel output."""
    return html.escape(str(value), quote=True)


def _desc_html(desc: str) -> str:
    """Description paragraph as raw HTML; inline `code` spans become <code>.

    Descriptions are prose with occasional backtick code spans (e.g.
    ``_REP\\d+``); everything else is escaped to plain text.
    """
    parts = _esc(desc).split("`")
    return "".join(
        f"<code>{part}</code>" if i % 2 else part
        for i, part in enumerate(parts)
    )


REQUIRED_FIELDS = ("name", "title", "description", "repo_url", "domain", "tags", "tools")


def validate(pipelines: list[dict]) -> None:
    """Fail loudly instead of emitting a broken/empty run-notes page."""
    names = []
    for p in pipelines:
        missing = [f for f in REQUIRED_FIELDS if not p.get(f)]
        inst = p.get("installation") or {}
        if not inst.get("engine") or not inst.get("toolchain"):
            missing.append("installation.engine/toolchain")
        if not p.get("quickstart"):
            missing.append("quickstart (fill in the quickstart field in data/pipelines.json)")
        if missing:
            raise SystemExit(f"registry entry '{p.get('name', '?')}' missing: {', '.join(missing)}")
        _validate_quickstart(p)
        names.append(p["name"])
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise SystemExit(f"duplicate registry names: {sorted(dupes)}")


def _validate_quickstart(p: dict) -> None:
    """A quickstart must be a literal, executable `oxo-flow run`/`dry-run`
    command referencing a workflow file that actually exists in the repo.

    Known-bad shapes rejected here: `workflow/<name>.toml` paths (no port uses
    them — every repo has main.oxoflow or a named .oxoflow at the root),
    `--config` (oxo-flow has no such flag; configuration lives in the
    workflow's `[config]` section or as positional args), `$OXO` prefixes and
    trailing `# comments` (fine in READMEs, not in the catalog).
    """
    name = p["name"]
    qs = p.get("quickstart", "").strip()
    if not qs.startswith("oxo-flow "):
        raise SystemExit(
            f"registry entry '{name}': quickstart must start with 'oxo-flow ' "
            f"(got: {qs!r})"
        )
    if "--config" in qs:
        raise SystemExit(
            f"registry entry '{name}': quickstart uses '--config', which "
            "oxo-flow does not have — set values in the workflow's [config] "
            "section or as positional args"
        )
    if "$OXO" in qs or "#" in qs:
        raise SystemExit(
            f"registry entry '{name}': quickstart must be a plain command — "
            "no '$OXO' prefix, no trailing '# comment'"
        )
    tokens = qs.split()
    if len(tokens) < 3 or tokens[1] not in ("run", "dry-run"):
        raise SystemExit(
            f"registry entry '{name}': quickstart must be 'oxo-flow run <file>' "
            f"or 'oxo-flow dry-run <file>' (got: {qs!r})"
        )
    wf = next((t for t in tokens[2:] if not t.startswith("-")), None)
    if not wf:
        raise SystemExit(f"registry entry '{name}': quickstart references no workflow file")
    # CI has no staging tree — the path check only runs when it is available.
    if STAGING.is_dir():
        repo = STAGING / name
        if not (repo / wf).is_file():
            present = sorted(f.name for f in repo.iterdir() if f.suffix == ".oxoflow")
            raise SystemExit(
                f"registry entry '{name}': quickstart references '{wf}' but the "
                f"staging repo has none (present: {present or 'none'})"
            )


def emit_js(pipelines: list[dict]) -> None:
    body = json.dumps(pipelines, indent=2)
    OUT_JS.write_text(
        "/* Generated by scripts/generate.py — do not edit by hand. */\n"
        f"window.OXO_PIPELINES = {body};\n"
    )


def rating_badge(rating: str, coverage: str = "") -> str:
    """Issue #3: evidence tiers — live-tested > dry-run verified > community.

    `coverage` (§15 completeness audit) is appended inside the badge for
    ports: full-line / default-path. Originals omit it (no upstream line).
    """
    if rating == "live-verified":
        label = "✔ Live-tested"
    elif rating == "verified":
        label = "★ Verified"
    else:
        label = "☆ Community"
    if coverage == "full-line":
        label += " · full-line"
    elif coverage == "default-path":
        label += " · default-path"
    cls = {
        "live-verified": "ox-badge--live",
        "verified": "ox-badge--star",
    }.get(rating, "")
    return f'<span class="ox-badge {cls}">{label}</span>'


def badges(p: dict) -> str:
    star = rating_badge(p.get("rating", "community"), p.get("coverage", ""))
    origin = {
        "port": "⇄ Official port",
        "original": "✦ Original",
        "curated": "♺ Community listing",
    }.get(p.get("origin"), "♺ Community listing")
    eng = ""
    if p.get("engine") == "nextflow":
        eng = '<span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span>'
    elif p.get("engine") == "snakemake":
        eng = '<span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span>'
    return f'<div class="ox-page-badges">{star} <span class="ox-badge ox-badge--origin">{origin}</span> {eng}</div>'


def glance_panel(p: dict) -> str:
    """P2 detail header — the right-hand 'At a glance' panel (was meta_table).

    Same rows, same data as the old table; rating keeps the coverage
    suffix here (cards drop it — see spec §Rating 后缀对账). Links and
    code are emitted as raw HTML because the panel is not markdown-parsed.
    """
    rating = p.get("rating", "community")
    rating_text = {
        "live-verified": "✔ Live-tested",
        "verified": "★ Verified",
        "community": "☆ Community",
    }.get(rating, "☆ Community")
    coverage = p.get("coverage", "")
    if coverage in ("full-line", "default-path"):
        rating_text += f" · {coverage}"
    origin = {
        "port": "⇄ Official port",
        "original": "✦ Original",
        "curated": "♺ Community listing",
    }.get(p.get("origin"), "♺ Community listing")
    eng = {
        "nextflow": '<span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span>',
        "snakemake": '<span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span>',
    }.get(p.get("engine"), "")
    rows = [
        ("Rating", rating_text, "live"),
        ("Rules", str(p.get("rule_count", "—")), ""),
        ("Compute", p.get("compute", "—"), ""),
        ("Engine", eng or "—", ""),
        ("Origin", origin, ""),
        ("Domain", p.get("domain", ""), ""),
    ]
    src = p.get("source")
    if src:
        rows += [
            ("Source", f'<a href="{_esc(src["url"])}">{_esc(src["repo"])}</a>', ""),
            ("Pinned version", f'<code>{_esc(src.get("tag") or src.get("sha", ""))}</code>', ""),
        ]
    rows += [
        ("Ported", p.get("created", "2026-08-15"), ""),
        ("License", p.get("license", "Apache-2.0"), ""),
    ]
    kv = "\n".join(
        f'<div class="ox-kv"><span class="k">{k}</span>'
        f'<span class="v{(" " + cls) if cls else ""}">{v}</span></div>'
        for k, v, cls in rows
    )
    return (
        '<div class="ox-glance">\n'
        '<div class="ox-glance-title">At a glance</div>\n'
        f"{kv}\n"
        f'<p class="cmd">$ {_esc(p["quickstart"])}</p>\n'
        "</div>"
    )


def gh_pull_url(repo_url: str) -> str:
    """Turn https://github.com/owner/repo into the gh:owner/repo form that
    `oxo-flow pull` accepts in repository mode (clone + auto-discover)."""
    if repo_url.startswith("https://github.com/"):
        return "gh:" + repo_url.removeprefix("https://github.com/").rstrip("/")
    return repo_url


def install_section(p: dict) -> str:
    inst = p.get("installation") or {}
    lines = [
        "## Installation",
        "",
        f"**Engine.** {inst.get('engine', 'oxo-flow >= 0.12.0')}",
        "",
        f"**Toolchain.** {inst.get('toolchain', 'containers or conda envs — pinned')}",
    ]
    if inst.get("requirements"):
        # The blank line is required — without it the `- item` lines merge
        # into the "Requirements." paragraph and render as literal text.
        lines += ["", "**Requirements.**", ""] + [f"- {r}" for r in inst["requirements"]]
    lines += [
        "",
        "```bash",
        "# 1. install oxo-flow (release binary, recommended)",
        f"curl -fL -o oxo-flow.tar.gz {ENGINE_URL}",
        "tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/",
        "#    or, via conda (may lag behind releases):",
        "#    conda install -c bioconda oxo-flow-cli",
        "#    NOTE: bioconda currently ships 0.10.2, older than the >= 0.12.0",
        "#    minimum of every catalog entry — prefer the release binary.",
        "",
        "# 2. get this workflow (clones the repo, auto-discovers the workflow,",
        "#    sanity-parses it with the engine)",
        f"oxo-flow pull {gh_pull_url(p['repo_url'])}",
        "#    (alternative: plain git clone)",
        f"#    git clone {p['repo_url']}",
        "```",
    ]
    return "\n".join(lines)


def fmt_default_plain(value) -> str:
    """Render a `[config]` default as plain text (no backticks — the params
    block is raw HTML and carries its own badge styling)."""
    if isinstance(value, bool):
        value = "true" if value else "false"
    elif isinstance(value, list):
        value = ", ".join(fmt_default_plain(item) for item in value)
    elif value is None:
        value = "—"
    return str(value).replace("\n", " ")


def params_section(p: dict, config: list[dict] | None) -> list[str]:
    """`## Parameters` — one collapsible block per config key (was a table).

    Long "used by" fan-outs (rnaseq has a key used by 135 rules) made the
    4-column table unreadable; blocks show key + default + description and
    collapse the rule list behind a native <details> — no JS. The whole
    section is ONE raw-HTML block (no blank lines inside; a blank line
    terminates a raw HTML block), so blocks are joined by single newlines.
    """
    if not config:
        return []
    blocks = []
    for record in config:
        key = record.get("key", "?")
        used_by = record.get("used_by", []) or []
        description = _desc_html(record.get("description") or "—")
        if used_by:
            rules = " ".join(
                f"<code>{html.escape(rule, quote=True)}</code>" for rule in used_by
            )
            usedby_html = (
                f'<details class="ox-param-usedby">'
                f"<summary>used by {len(used_by)} rules</summary>\n"
                f'<div class="ox-param-rules">{rules}</div>\n'
                "</details>"
            )
        else:
            usedby_html = (
                '<details class="ox-param-usedby">'
                "<summary>not referenced by any rule</summary>\n"
                '<div class="ox-param-rules">—</div>\n'
                "</details>"
            )
        blocks.append(
            f'<div class="ox-param">\n'
            f'<div class="ox-param-head"><code>{_esc(key)}</code>'
            f'<span class="ox-param-default">{_esc(fmt_default_plain(record.get("default")))}</span></div>\n'
            f'<p class="ox-param-desc">{description}</p>\n'
            f"{usedby_html}\n"
            "</div>"
        )
    return [
        "",
        "## Parameters",
        "",
        '<div class="ox-params">',
        "\n".join(blocks),
        "</div>",
        "",
        "Descriptions are the workflow's own `#` comments from its `[config]` "
        "section, surfaced by `oxo-flow info` — no schema file to maintain.",
    ]


def dag_section(p: dict) -> list[str]:
    """`## Workflow graph` — the static rule-level DAG SVG that
    regen-configs.py renders from `oxo-flow graph -f metro` + nf-metro
    (transit-map style)."""
    name = p["name"]
    svg = OUT_PAGES.parent / "assets" / "dag" / f"{name}.svg"
    if not svg.is_file():
        raise SystemExit(
            f"missing {svg.relative_to(ROOT)} for '{name}' — run scripts/regen-configs.py"
        )
    cards = [
        '<div class="ox-dag-card" markdown="1">',
        "",
        f"![{name} rule-level DAG](../assets/dag/{name}.svg)",
        "",
        f'<p class="ox-dag-caption">figure · {name} — rule-level transit map (nf-metro)</p>',
        "",
        "</div>",
    ]
    for ew in p.get("extra_workflows") or []:
        svg_extra = OUT_PAGES.parent / "assets" / "dag" / f"{ew['dag']}.svg"
        if not svg_extra.is_file():
            raise SystemExit(
                f"missing {svg_extra.relative_to(ROOT)} for '{name}' — "
                "run scripts/regen-configs.py"
            )
        cards += [
            '<div class="ox-dag-card" markdown="1">',
            "",
            f"![{name} — {ew['label']}](../assets/dag/{ew['dag']}.svg)",
            "",
            f'<p class="ox-dag-caption">figure · {name} — {ew["label"]} (nf-metro)</p>',
            "",
            "</div>",
        ]
    return [
        "",
        "## Workflow graph",
        "",
        *cards,
        "",
        "The graph is derived at catalog-build time from "
        "`oxo-flow graph -f metro` and rendered with [nf-metro]"
        "(https://github.com/seqeralabs/nf-metro) — rules are grouped into "
        "colored transit lines by analysis stage. It shows the workflow at "
        "rule level: wildcard `{sample}` instances expand at run time when "
        "sample data is discovered (the runtime view is "
        "`oxo-flow graph --expanded`).",
    ]


def make_page(p: dict, configs: dict) -> str:
    src = p.get("source") or {}
    scope = "\n".join(f"- {s}" for s in p.get("scope", []))
    excluded = "\n".join(f"- {s}" for s in p.get("excluded", [])) or "- none"
    # not_applicable: upstream-absent features / boilerplate / dead code /
    # deliberate non-goals (Traitome/oxo-flow#267 bucket D) — shown under a
    # separate heading so excluded reads as "genuinely blocked/missing".
    not_applicable = "\n".join(f"- {s}" for s in p.get("not_applicable", []))
    fidelity = p.get("fidelity_md")
    parts = [
        "---",
        f"title: {json.dumps(p['title'])}",
        "---",
        "",
        f'<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>{_esc(p["name"])}</span></div>',
        # The header is ONE raw-HTML block: a raw HTML block ends at the
        # first blank line, so there must be no blank lines inside the
        # grid/columns (live-finding 2026-09-05 — markdown="1" nesting
        # shreds nested raw HTML into code blocks).
        '<div class="ox-detail-cols">',
        "<div>",
        f"<h1>{_esc(p['title'])}</h1>",
        badges(p),
        f"<p>{_desc_html(p.get('description', ''))}</p>",
        "</div>",
        "<div>",
        glance_panel(p),
        "</div>",
        "</div>",
        "",
        "## Run it" if "dry-run" not in p["quickstart"] else "## Preview the plan",
        "",
        "```bash",
        p["quickstart"],
        "```",
    ]
    if p.get("quickstart_note"):
        parts += ["", p["quickstart_note"]]
    parts += [
        "",
        install_section(p),
        *params_section(p, configs.get(p["name"], {}).get("config")),
    ]
    # Same signal as the Parameters table: a staged workflow existed at
    # regen time, so the DAG SVG must exist too (dag_section fails loudly).
    if p["name"] in configs:
        parts += dag_section(p)
    if src:
        parts += [
            "",
            "## Scope",
            "",
            "The default-parameters main path of the source pipeline was ported "
            "rule-for-rule; alternate paths are documented as excluded.",
            "",
            "**In scope**",
            "",
            scope,
            "",
            "**Excluded**",
            "",
            excluded,
        ]
    if not_applicable:
        parts += [
            "",
            "**Not applicable** (upstream-absent features, boilerplate, dead code, "
            "deliberate non-goals — see the excluded-key taxonomy in "
            "[Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))",
            "",
            not_applicable,
        ]
    if fidelity:
        parts += ["", "## Fidelity", "", fidelity]
    parts += [
        "",
        "## Links",
        "",
        f"- Repository: [{p['name']}]({p['repo_url']})",
    ]
    if src:
        parts += [
            f"- Upstream: [{src['repo']}]({src['url']})"
            + (f" @ `{src['tag']}`" if src.get("tag") else ""),
            f"- License: {p.get('license', 'Apache-2.0')} (this workflow)"
            + (f" · {p.get('upstream_license') or src.get('license')} (upstream)" if src else ""),
            "",
            "Created on " + p.get("created", "2026-08-15")
            + " — this port may lag behind upstream releases. See the "
            "repository's NOTICE for full attribution.",
        ]
    return "\n".join(parts) + "\n"


def main() -> int:
    pipelines = load()
    validate(pipelines)
    configs = load_configs()
    emit_js(pipelines)
    OUT_PAGES.mkdir(parents=True, exist_ok=True)
    for p in pipelines:
        (OUT_PAGES / f"{p['name']}.md").write_text(make_page(p, configs))
    print(f"generated: {len(pipelines)} pages + pipelines-data.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
