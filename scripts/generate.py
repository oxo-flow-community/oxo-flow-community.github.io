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
import re
import sys

from param_fallbacks import fallback_description

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



def _asset_img(rel_path: str, alt: str) -> str:
    """<img> with a content-fingerprint query: mkdocs copies assets as-is,
    browser caches them aggressively, and a re-render keeps the same
    filename — so a reader with a warm cache keeps seeing the OLD map
    even after a fix (live: clindet header looked 'unchanged'). The
    content hash busts that cache per regeneration AND stays
    drift-gate-stable: the CI check regenerates pages in a fresh clone,
    where a mtime query would differ and fail.
    """
    import hashlib
    # MkDocs emits pages at /pipelines/<name>/ (directory URLs); a
    # relative "../assets/…" src resolves to /pipelines/assets/… and 404s
    # on GitHub Pages — EVERY page's graph was unreachable that way
    # (confirmed by live 404s and a headless-Chrome capture). Use the
    # site-root absolute path instead.
    abs_path = "/" + rel_path[3:] if rel_path.startswith("../") else rel_path
    addr = pathlib.Path(ROOT) / "docs" / rel_path[3:]
    try:
        version = hashlib.sha1(addr.read_bytes()).hexdigest()[:10]
    except OSError:
        version = "0"
    href = abs_path + f"?v={version}"
    return (
        f'<a href="{href}" target="_blank" rel="noopener" '
        f'title="Open at native resolution">'
        f'<img src="{href}" alt="{alt}" loading="lazy"></a>'
    )


def _graph_note() -> str:
    """One paragraph every workflow graph carries, so the drawn shapes
    read correctly — off-track stations and independent chains are DAG
    reality, not broken rendering."""
    return (
        '<p class="ox-dag-note">Read: stations are rules (or module'
        ' groups); a line is a data dependency; stations without any line'
        ' are <em>off-track</em> inputs/terminal exports with no dataflow'
        ' edge; separate groups of lines are independent chains (e.g. a'
        ' quantifier reading raw reads while the alignment chain runs'
        ' aside — live: tcasia salmon_quant). The map shows the template'
        ' DAG; <code>oxo-flow graph --expanded</code> adds one node per'
        ' sample instance.</p>'
    )


def _esc(value) -> str:
    """HTML-escape a registry value for raw-HTML panel output."""
    return html.escape(str(value), quote=True)


def _desc_html(desc: str) -> str:
    """Description paragraph as raw HTML; inline `code` spans become <code>.

    Descriptions are prose with occasional backtick code spans (e.g.
    ``_REP\\d+``); everything else is escaped to plain text. Newlines
    survive as <br> — the workflow's own comment blocks fold multi-line
    prose (a reference_dir layout list, say) into the description and a
    single-run paragraph is unreadable (live: circrna reference_dir).
    """
    parts = _esc(desc).split("`")
    rendered = "".join(
        f"<code>{part}</code>" if i % 2 else part
        for i, part in enumerate(parts)
    )
    return rendered.replace("\n", "<br>")


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
        # Copyable commands derive the gh: owner from repo_url (gh_slug) —
        # fail at validate time, not as a 404 in the reader's shell.
        gh_slug(p)
        src = p.get("source") or {}
        if src.get("url") == p.get("repo_url") and p.get("origin") != "original":
            raise SystemExit(
                f"registry entry '{name}': origin=port but source points at its "
                "own repo — a port must name a real upstream (or origin=original)"
            )
        if p.get("rating") in ("dry-run-verified", "community") \
                and not p.get("quickstart", "").startswith("oxo-flow dry-run") \
                and not p.get("quickstart_note"):
            raise SystemExit(
                f"registry entry '{name}': rated {p['rating']} yet its quickstart "
                "is a full run with no quickstart_note — never-presented "
                "end-to-end entries must disclose that next to the command"
            )
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
            present = sorted(f.name for f in repo.iterdir() if f.suffix == ".oxoflow") if repo.is_dir() else []
            raise SystemExit(
                f"registry entry '{name}': quickstart references '{wf}' but the "
                f"staging repo has none (present: {present or 'none'})"
            )


def emit_js(pipelines: list[dict]) -> None:
    # Compact (whitespace was ~6% of the file). Site-wide loading was the
    # real cost — catalog.js now lazy-injects this only on pages that host a
    # catalog mount (its MOUNTS check), so pipeline/audit pages never fetch it.
    body = json.dumps(pipelines, separators=(",", ":"))
    OUT_JS.write_text(
        "/* Generated by scripts/generate.py — do not edit by hand. */\n"
        f"window.OXO_PIPELINES = {body};\n"
    )


def compute_summary(value):
    """At-a-glance Compute cell: short summary, full string as tooltip —
    the verbose per-rule breakdown stays in Requirements. Long compute
    notes (live: ampliseq 5-line multi-tool spec) must never push the
    grid into the TOC column."""
    if not value:
        return "—"
    text = str(value).replace("\n", " ")
    short = text if len(text) <= 64 else text[:61].rstrip() + "…"
    return f'<span title="{_esc(text)}">{_esc(short)}</span>'


def rating_badge(rating: str, coverage: str = "") -> str:
    """Issue #3: evidence tiers — live-tested > dry-run verified > community.

    `coverage` (§15 completeness audit) is appended inside the badge for
    ports: full-line / default-path. Originals omit it (no upstream line).
    """
    if rating == "live-verified":
        label = "✔ Live-tested"
    elif rating == "verified":
        label = "★ Verified"
    elif rating == "dry-run-verified":
        label = "◆ Dry-run verified"
    else:
        label = "☆ Community"
    if coverage == "full-line":
        label += " · full-line"
    elif coverage == "default-path":
        label += " · default-path"
    cls = {
        "live-verified": "ox-badge--live",
        "verified": "ox-badge--star",
        "dry-run-verified": "ox-badge--dry",
    }.get(rating, "")
    return f'<span class="ox-badge {cls}">{label}</span>'


# Shared classification labels (single source — DRY across the hero, the
# glance panel and the catalog rendering in catalog.js).
ORIGIN_TEXT = {"port": "Official port", "original": "Original",
               "curated": "Community listing"}
ENGINE_BADGE = {
    "nextflow": '<span class="ox-badge ox-badge--nf"><span class="dot" aria-hidden="true"></span>nf-core port</span>',
    "snakemake": '<span class="ox-badge ox-badge--sn"><span class="dot" aria-hidden="true"></span>snakemake port</span>',
    "oxo-flow": '<span class="ox-badge ox-badge--native"><span class="dot" aria-hidden="true"></span>oxo-flow native</span>',
}


def badge_row(p: dict) -> str:
    """Hero badge strip: evidence rating, origin, engine, subject tags."""
    star = rating_badge(p.get("rating", "community"), p.get("coverage", ""))
    origin = ORIGIN_TEXT.get(p.get("origin"), ORIGIN_TEXT["curated"])
    eng = ENGINE_BADGE.get(p.get("engine"), "")
    tags = "".join(
        f'<span class="ox-tag">{_esc(t)}</span>' for t in (p.get("tags") or [])
    )
    return (f'<div class="ox-page-badges">{star} <span class="ox-badge ox-badge--origin">{origin}</span> '
            f'{eng}{("<span class=ox-tag-sep></span>" + tags) if tags else ""}</div>')


def hero_cta(p: dict, anchor: str) -> str:
    """Hero call-to-action: run command + repository button. The button
    mirrors what the anchor section actually does — a dry-run entry's
    section only previews, so the CTA must not promise "Run"."""
    cmd = _esc(p.get("quickstart") or "oxo-flow run main.oxoflow")
    repo = _esc(p.get("repo_url", ""))
    label = "▶ Preview the plan" if anchor == "preview-the-plan" else "▶ Run it"
    return (f'<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#{anchor}">{label}</a>'
            f'<a class="ox-btn" href="{repo}" rel="noopener">GitHub ↗</a>'
            f'<code class="ox-hero-cmd">$ {cmd}</code></div>')


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
        "dry-run-verified": "◆ Dry-run verified",
        "community": "☆ Community",
    }.get(rating, "☆ Community")
    coverage = p.get("coverage", "")
    if coverage in ("full-line", "default-path"):
        rating_text += f" · {coverage}"
    origin = ORIGIN_TEXT.get(p.get("origin"), ORIGIN_TEXT["curated"])
    eng = ENGINE_BADGE.get(p.get("engine"), "")
    rows = [
        # The "live" success-green is reserved for live-tested — rating rows
        # must not paint ★/◆/☆ with it (evidence-ladder honesty).
        ("Rating", rating_text, "live" if rating == "live-verified" else ""),
        ("Rules", str(p.get("rule_count", "—")), ""),
        ("Compute", compute_summary(p.get("compute")), ""),
        ("Engine", eng or "—", ""),
        ("Origin", origin, ""),
        ("Domain", p.get("domain", ""), ""),
    ]
    src = p.get("source")
    if src:
        if not (p.get("origin") == "original" and src.get("url") == p.get("repo_url")):
            # originals self-referencing their own repo don't need a Source
            # row that duplicates the repo link — the pin below still shows.
            rows += [
                ("Source", f'<a href="{_esc(src["url"])}">{_esc(src["repo"])}</a>', ""),
            ]
        pin = src.get("tag") or src.get("sha", "")
        if pin in ("main", "master", "develop") and src.get("sha"):
            # A bare branch name is not a pin — render it anchored to its sha.
            pin = f'{pin}@{src["sha"][:7]}'
        rows += [
            ("Pinned version", f'<code>{_esc(pin)}</code>', ""),
        ]
        if p.get("updated"):
            rows += [("Last verified", p["updated"], "")]
    rows += [
        ("Added" if p.get("origin") == "original" else "Ported", p.get("created", "2026-08-15"), ""),
        ("License", p.get("license", "Apache-2.0"), ""),
    ]
    wh = p.get("workflowhub")
    if wh:
        rows += [
            ("Cite", f'<a href="{_esc(wh["doi_url"])}"><code>{_esc(wh["doi"])}</code></a>', ""),
        ]
    kv = "\n".join(
        f'<div class="ox-kv"><span class="k">{k}</span>'
        f'<span class="v{(" " + cls) if cls else ""}">{v}</span></div>'
        for k, v, cls in rows
    )
    chips = "".join(
        f'<span class="tchip">{_esc(t)}</span>' for t in (p.get("tools") or [])[:8]
    )
    return (
        '<div class="ox-glance">\n'
        '<div class="ox-glance-title">At a glance</div>\n'
        f"{kv}\n"
        f'<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips">{chips}</div></div>\n'
        f'<p class="cmd">$ {_esc(pull_bar_body(gh_slug(p)))}</p>\n'
        "</div>"
    )


def gh_pull_url(repo_url: str) -> str:
    """Turn https://github.com/owner/repo into the gh:owner/repo form that
    `oxo-flow pull` accepts in repository mode (clone + auto-discover)."""
    if repo_url.startswith("https://github.com/"):
        return "gh:" + repo_url.removeprefix("https://github.com/").rstrip("/")
    return repo_url


def gh_slug(p: dict) -> str:
    """`owner/repo` derived from the authoritative repo_url — some entries
    are hosted outside the org (WangLabCSU/...); a hard-coded org prefix
    would render copy-fails-with-404 commands on those pages."""
    m = re.search(r"github\.com/([^/]+/[^/]+?)(?:\.git)?/?$", p["repo_url"])
    if not m:
        raise SystemExit(
            f"registry entry '{p['name']}': repo_url is not a github repo: {p['repo_url']}"
        )
    return m.group(1)


def shell_wrap(cmd: str, width: int = 78) -> str:
    """Break a long one-line command into backslash-continuation lines at
    argument boundaries — bash consumes ` \\`+newline, so the fenced command
    stays copy-pasteable and reads complete without horizontal scrolling."""
    if len(cmd) <= width:
        return cmd
    lines: list[str] = []
    cur = ""
    for tok in cmd.split(" "):
        if cur and len(cur) + 1 + len(tok) > width:
            lines.append(cur)
            cur = tok
        else:
            cur = cur + " " + tok if cur else tok
    lines.append(cur)
    return " \\\n  ".join(lines)


# The narrow mono bars (glance panel pull, catalog card pull) fit roughly 52
# rendered chars — past that the tail scrolls out of sight and reads as a
# truncated command, so emit an idiomatic continuation pair instead.
CMD_BAR_LIMIT = 52


def pull_bar_body(slug: str) -> str:
    """Text after the `$ ` in the .cmd pull bars (catalog.js mirrors the
    threshold and form for the card variant)."""
    cmd = f"oxo-flow pull gh:{slug}"
    if len("$ " + cmd) > CMD_BAR_LIMIT:
        return f"oxo-flow pull \\\n  gh:{slug}"
    return cmd


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
        "#    or, via conda (bioconda's oxo-flow-cli tracks releases with a lag):",
        "#    conda install -c bioconda oxo-flow-cli",
        "#    Check `oxo-flow --version` against the Engine minimum above — if",
        "#    bioconda trails it, use the release binary instead.",
        "",
        "# 2. get this workflow (clones the repo, auto-discovers the workflow,",
        "#    sanity-parses it with the engine)",
        shell_wrap(f"oxo-flow pull {gh_pull_url(p['repo_url'])}"),
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
    """`## Parameters` — one searchable table per workflow.

    Table layout (nf-core style): key | type | default | description. The
    description keeps the "used by N rules" hint inline; every row has a
    copy button for `key = value` (one generic click handler in catalog.js
    reading data-copy, so no per-page JS). The used-by rule list stays
    behind an inline expandable on the row when a key fans out widely.
    """
    if not config:
        return []
    rows = []
    for record in config:
        key = record.get("key", "?")
        used_by = record.get("used_by", []) or []
        description = record.get("description")
        inferred = False
        if not description:
            # Generic fallback for well-known key patterns the workflow
            # does not comment on its own (see param_fallbacks.py) —
            # marked as inferred so authors know a real comment wins.
            description = fallback_description(key)
            inferred = description is not None
        description_html = _desc_html(description or "—")
        if inferred:
            description_html += (
                ' <span class="ox-param-inferred">inferred</span>'
            )
        typ = _esc(record.get("value_type") or "string")
        default = _esc(fmt_default_plain(record.get("default")))
        n_used = len(used_by)
        used_hint = (
            f'<span class="ox-param-usedby">used by <code>{n_used}</code>'
            f" rules</span>"
            if n_used
            else (
                '<span class="ox-param-unused">not referenced by any rule'
                " (ported for upstream compatibility — overriding has no "
                "effect here)</span>"
            )
        )
        rows.append(
            f"<tr>\n"
            f'<td class="ox-p-k"><button class="ox-p-copy" type="button" '
            f'title="Copy {_esc(key)} = value" '
            f'aria-label="Copy {_esc(key)} = {_esc(default)} to clipboard" '
            f'data-copy="{_esc(key)} = '
            f'{default}">{_esc(key)}</button></td>\n'
            f'<td class="ox-p-t"><code>{typ}</code></td>\n'
            f'<td class="ox-p-d"><code>{default}</code></td>\n'
            f'<td class="ox-p-desc">{description_html}<br>{used_hint}</td>\n'
            "</tr>"
        )
    return [
        "",
        "## Parameters",
        "",
        '<p class="ox-param-usage">Parameters are consumed by rules through '
        "<code>{config.key}</code> placeholders in inputs, outputs, and "
        "shells. Set a value in the workflow's <code>[config]</code> "
        "section (edit the file), or override at run time with "
        "<code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat "
        "<code>-e</code> for multiple keys. Copy a row to paste the key "
        "directly. Click any parameter name to copy <code>key = value</code>; "
        "clicking <code>default</code> copies just the value.</p>",
        '<table class="ox-params">',
        "<thead><tr><th>Parameter</th><th>Type</th><th>Default</th>"
        "<th>Description</th></tr></thead>",
        "<tbody>",
        "\n".join(rows),
        "</tbody>",
        "</table>",
        "",
        "Descriptions are the workflow's own `#` comments from its `[config]` "
        "section (and the `[config]` sections of its included modules), "
        "surfaced by `oxo-flow info` — no schema file to maintain.",
    ]



def _intrinsic_width(svg_path) -> float:
    """viewBox width of a committed DAG svg (for wide-card layout)."""
    try:
        m = re.search(r'viewBox="[\d.\- ]+"', svg_path.read_text(encoding="utf-8"))
        if not m:
            return 0.0
        return float(m.group(0).split('"')[1].split()[2])
    except OSError:
        return 0.0


def dag_section(p: dict, configs: dict) -> list[str]:
    """`## Workflow graph` — the ladder-chosen metro map SVG that
    regen-configs.py renders via metro_tiers.py (rule-level to overview
    tiers, nf-metro transit-map style). Plus collapsible flow views
    (per-subflow mini maps of a multi-omics single-entry workflow)."""
    name = p["name"]
    svg = OUT_PAGES.parent / "assets" / "dag" / f"{name}.svg"
    if not svg.is_file():
        raise SystemExit(
            f"missing {svg.relative_to(ROOT)} for '{name}' — run scripts/regen-configs.py"
        )
    # The map's stations name the workflow's own module namespaces; the
    # caption's first sentence of the registry description reads the
    # pipeline as a flow (fastp QC → alignment → callers → report), so
    # both a newcomer and a designer who knows the pipeline can make
    # sense of the figure without decoding file stems.
    summary = re.split(r"(?<=[.!?])\s+", p.get("description", "").strip())[0]
    caption = f"figure · {name} — {summary}"
    # PRIMARY ORDER: per-subflow module maps (the readable入口 for a
    # multi-omics entry — DNA/RNA at ten stations each), then the full
    # overview as a collapsed reference, then extra_workflows cards.
    cards = []
    for vid, vinfo in sorted((configs.get(name, {}).get("flow_views") or {}).items()):
        svg_path = f"../assets/dag/{name}-{_esc(vid)}.svg"
        cards += [
            f'<details class="ox-flow-view" open>',
            f'<summary>{_esc(vinfo.get("label", vid))}</summary>',
            '<div class="ox-dag-card">',
            _asset_img(svg_path, f"{name} {_esc(vid)} flow view"),
            "<p class=\"ox-dag-note\">Stations are the sub-flow's modules; "
            "a stage name above the module set tells what the module does. "
            'Unconnected stations are conditional or auxiliary modules '
            'without a dataflow edge on the template DAG (clindet: QC, Isofox).</p>',
            "</div>",
            "</details>",
        ]
    # Rule-level detail (where it renders and where the primary figure is
    # NOT itself rule-level): the exact graph of every rule, collapsed by
    # default. When the ladder promoted the rule-level figure to be the
    # primary (a degenerate multi-module workflow, live: nanoseq) the same
    # picture would appear twice — the detail card is omitted then.
    info = configs.get(name, {}).get("graph") or {}
    primary_is_rule = bool(info.get("is_rule_level"))
    rules_svg = OUT_PAGES.parent / "assets" / "dag" / f"{name}-rules.svg"
    if rules_svg.is_file() and not primary_is_rule:
        rules_wide = " ox-dag-card--wide" if _intrinsic_width(rules_svg) > 1400 else ""
        cards += [
            '<details class="ox-flow-view">',
            '<summary>Exact rule DAG (multi-route truth — operational view)</summary>',
            f'<div class="ox-dag-card{rules_wide}">',
            _asset_img(f"../assets/dag/{name}-rules.svg", f"{name} rule-level detail"),
            "</div>",
            "</details>",
        ]
    # The overview card is the reading anchor: default-open when it is the
    # page's only primary figure (single-workflow pages and degenerate
    # rule-level primaries), collapsed behind the open flow views on
    # multi-omics entries.
    has_views = bool(configs.get(name, {}).get("flow_views"))
    open_mark = " open" if primary_is_rule or not has_views else ""
    wide = " ox-dag-card--wide" if _intrinsic_width(svg) > 1400 else ""
    cards += [
        f'<details class="ox-flow-view"{open_mark}>',
        '<summary>Overview — all modules</summary>',
        f'<div class="ox-dag-card{wide}" markdown="1">',
        "",
        _asset_img(f"../assets/dag/{name}.svg", f"{name} pipeline overview"),
        "",
        f'<p class="ox-dag-caption">{_esc(caption)}</p>',
        "",
        "</div>",
        "</details>",
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
            _asset_img(f"../assets/dag/{ew['dag']}.svg", f"{name} — {ew['label']}"),
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
        _graph_note(),
        "",
        "The graph is derived at catalog-build time from "
        "`oxo-flow graph -f metro` through the adaptive render ladder "
        "(`scripts/metro_tiers.py`): each workflow gets the finest metro "
        "tier that nf-metro renders while staying readable at site width — "
        "rule-level stations for smaller workflows, module-stage or module"
        "overview stations for dense ones. Colored transit lines group "
        "stations by analysis stage. Wildcard `{sample}` instances expand "
        "at run time when sample data is discovered (the runtime view is "
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
    # Section-presence flags for the section tabs — must mirror exactly the
    # gates used below for the Parameters table, the Workflow graph and the
    # semantic card, so no tab ever links to an unrendered heading.
    cfg = configs.get(p["name"], {})
    has_semantic = (
        pathlib.Path(ROOT) / "scripts" / "semantic_maps" / f"{p['name']}.md"
    ).is_file()
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
        "<div class=\"ox-detail-main\">",
        f"<h1>{_esc(p['title'])}</h1>",
        badge_row(p),
        f"<p class=\"ox-desc\">{_desc_html(p.get('description', ''))}</p>",
        hero_cta(p, "preview-the-plan" if "dry-run" in p["quickstart"] else "run-it"),
        "</div>",
        "<div>",
        glance_panel(p),
        "</div>",
        "</div>",
        "",
        section_tabs(p, bool(src), bool(fidelity), has_semantic,
                     bool(cfg.get("config")), p["name"] in configs),
        "",
        *semantic_card(p),
        "",
        "## Run it" if "dry-run" not in p["quickstart"] else "## Preview the plan",
        "",
        run_cmd(p),
        "",
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
        parts += dag_section(p, configs)
    if src:
        self_sourced = p.get("origin") == "original" and src.get("url") == p.get("repo_url")
        intro = (
            "Native oxo-flow design — no upstream port: steps implemented by "
            "this workflow are listed as in scope; alternate paths of the "
            "domain's conventional pipelines appear under excluded."
            if self_sourced
            else "The default-parameters main path of the source pipeline was ported "
            "rule-for-rule; alternate paths are documented as excluded."
        )
        parts += [
            "",
            "## Scope",
            "",
            intro,
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
    cov = (p.get("coverage") or "").strip()
    if cov and cov not in ("full-line", "default-path"):
        # Long-form coverage (why a ★ was pulled down from ✔ after a re-port,
        # what evidence stands) was written into the registry but rendered
        # nowhere — surface it as a collapsed evidence card. Raw <details> +
        # md_in_html is this repo's collapsible idiom (no admonition ext).
        parts += [
            "",
            '<details class="ox-evidence" markdown="1"><summary>Verification evidence</summary>',
            "",
            cov,
            "",
            "</details>",
        ]
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
            + (f" · last catalog sync {p['updated']}." if p.get("updated")
               else " — this entry may lag behind upstream releases.")
            + " See the repository's NOTICE for full attribution.",
        ]
    return "\n".join(parts) + "\n"


def sem_to_html(md: str) -> str:
    """Tiny renderer for the semantic-overview text (markdown subset:
    paragraphs, **bold**, `code`, *emphasis*) — the card sits inside a raw
    HTML <details> block where mkdocs' inline markdown would not run."""
    import html as _html
    parts = []
    for para in md.split("\n\n"):
        p = para.strip()
        if not p:
            continue
        p = _html.escape(p, quote=False)
        p = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"`([^`]+)`", r"<code>\1</code>", p)
        m = re.fullmatch(r"\*(.+)\*", p)
        if m:
            p = f"<em>{m.group(1)}</em>"
        parts.append(f"<p>{p}</p>")
    return "\n".join(parts)


def run_cmd(p: dict) -> str:
    """Run-it section: the engine executes a catalog repo directly —
    `oxo-flow run gh:owner/repo[@ref]` checks the repo out under
    .oxo-flow/repos/<name> and keeps outputs in the current directory.

    Positional args and flags come verbatim from the validated quickstart's
    tail (everything after `oxo-flow run|dry-run <file>`). Entries whose
    quickstart is a dry-run get the validated literal instead — we never
    promote a never-tested workflow to a full-run example command."""
    name = p["name"]
    slug = gh_slug(p)
    tokens = p.get("quickstart", "oxo-flow run main.oxoflow").split()
    wf = next((t for t in tokens[2:] if t.endswith(".oxoflow")), "main.oxoflow")
    if tokens[1] == "dry-run":
        cmd = " ".join(tokens)
    else:
        argtail = " ".join(t for t in tokens[2:] if not t.endswith(".oxoflow"))
        cmd = f"oxo-flow run gh:{slug}" + (f" {argtail}" if argtail else "")
    return "\n".join([
        "```bash",
        shell_wrap(cmd),
        "```",
        "",
        f"Runs straight from the catalog — `oxo-flow` checks the repo out under "
        f"`.oxo-flow/repos/{name}` and keeps outputs/checkpoints in the current "
        "directory, no manual clone. Pin a revision with "
        f"`gh:{slug}@<branch-or-tag>`.",
        "",
        "Preview the plan first: `oxo-flow pull gh:" + slug +
        "` fetches the repo, then `oxo-flow dry-run " + wf + "`.",
    ])


def semantic_card(p: dict) -> list[str]:
    """LLM-authored plain-language semantic overview (scripts/semantic_maps/
    <name>.md) — the page's Introduction body, right under the hero: every
    step is named with its real rule, nothing invented; rendered as
    markdown, updated by editing the .md file (no figure re-generation)."""
    sem_doc = pathlib.Path(ROOT) / "scripts" / "semantic_maps" / f"{p['name']}.md"
    if not sem_doc.is_file():
        return []
    sem_text = sem_doc.read_text(encoding="utf-8").strip()
    return [
        '<details class="ox-flow-view" open id="semantic-overview">',
        '<summary>Semantic overview — plain-language walkthrough '
        '<span class="ox-badge ox-badge--sem">text</span></summary>',
        '<div class="ox-sem-text">',
        sem_to_html(sem_text),
        f'<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/'
        f'oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+{_esc(p["name"])}+semantic+text+'
        f'correction&body=Which step or rule name looks wrong (paste the step/rule names)">'
        f'Report a correction to this overview</a></p>',
        "</div>",
        "</details>",
    ]


def section_tabs(p: dict, has_scope: bool, has_fidelity: bool,
                 has_semantic: bool, has_params: bool, has_graph: bool) -> str:
    """genomeqc-style pipeline sub-navigation: sticky anchor tabs for the
    page's own sections (Introduction → Usage → Parameters → …).

    A tab is emitted only when its section actually rendered — entries
    without a committed `oxo-flow info` record (no Parameters table, no DAG)
    or without a semantic map (live: erv, immune-repertoire) would else
    carry tabs that jump nowhere. The flags mirror the exact gates in
    make_page/params_section/dag_section/semantic_card."""
    anchors = []
    if has_semantic:
        anchors.append(("#semantic-overview", "Introduction"))
    anchors.append(
        ("#preview-the-plan" if "dry-run" in p["quickstart"] else "#run-it", "Usage")
    )
    if has_params:
        anchors.append(("#parameters", "Parameters"))
    if has_graph:
        anchors.append(("#workflow-graph", "Workflow graph"))
    if has_scope:
        anchors.append(("#scope", "Scope"))
    if has_fidelity:
        anchors.append(("#fidelity", "Fidelity"))
    items = "".join(f'<a href="{h}">{t}</a>' for h, t in anchors)
    return f'<nav class="ox-tabs" aria-label="Page sections">{items}</nav>'


def main() -> int:
    pipelines = load()
    validate(pipelines)
    configs = load_configs()
    emit_js(pipelines)
    OUT_PAGES.mkdir(parents=True, exist_ok=True)
    for p in pipelines:
        (OUT_PAGES / f"{p['name']}.md").write_text(page_meta(p) + "\n" + make_page(p, configs))
    print(f"generated: {len(pipelines)} pages + pipelines-data.js")
    return 0


def page_meta(p: dict) -> str:
    """Per-page front matter: a real description so Material emits a unique
    meta description + og:description per pipeline page (the site-wide
    fallback made every page read identically in search/IM previews).
    Built from registry facts only — rating label, engine, counts."""
    rating = p.get("rating", "community")
    label = {
        "live-verified": "live-tested (✔)",
        "verified": "verified (★)",
        "dry-run-verified": "dry-run verified (◆)",
    }.get(rating, "community-listed (☆)")
    bits = [f"{p['title']} — the {label} entry"]
    if p.get("domain"):
        bits.append(p["domain"].strip())
    if p.get("engine"):
        bits.append(f"{str(p['engine']).strip()} workflow")
    if p.get("rule_count"):
        bits.append(f"{str(p['rule_count']).strip()} rules")
    if p.get("tools"):
        bits.append(f"{len(p['tools'])} tools")
    desc = ", ".join(bits) + "."
    # title: beats Material's filename→titlecase ("oxo-flow-rnaseq" would
    # otherwise surface as "Oxo flow rnaseq" in <title>/og:title).
    return ("---\ntitle: " + _yaml_scalar(p["title"]) + "\n"
            + yaml_safe_dump({"description": desc}) + "---")


def yaml_safe_dump(d: dict) -> str:
    return "".join(f"{k}: {_yaml_scalar(v)}\n" for k, v in d.items())


def _yaml_scalar(v) -> str:
    s = str(v)
    # Empty must be quoted too: bare `key: ` would parse back as None. And
    # YAML type-homing words (yes/no/null/~/numbers/True, tabs) would reload
    # as bool/None/int or blow the parse — quote anything not plain-safe.
    if (s == "" or s.strip() != s or "\t" in s
            or s.lower() in ("yes", "no", "true", "false", "null", "~", "on", "off")
            or re.fullmatch(r"[-+]?[0-9.]+", s)
            or re.search(r'[:#"\']', s)):
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return s


if __name__ == "__main__":
    sys.exit(main())
