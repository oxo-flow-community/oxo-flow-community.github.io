#!/usr/bin/env python3
"""Adaptive metro-map rendering ladder for `regen-configs.py`.

nf-metro 1.1.0 (the Seqera Rust rewrite) renders clean transit maps but
aborts on dense graphs with strict routing invariants (CurveInvariantError:
collinear overlays, hanging routes). Site issue #16 asked for
publication-quality maps on all pipelines; the ladder delivers one for
every workflow WITHOUT per-pipeline curation, by walking increasingly
coarse, structurally-safe representations:

  1. sectioned   — rule-level, rules grouped into module sections
                   (the engine's canonical `-f metro` export);
  2. flat        — rule-level without sections (section ports are what
                   trigger most collinear-overlay aborts);
  3. module-stage — one station per (module, stage): the overview
                   granularity nf-core publishes (tens of stations);
  4. module      — one station per module, from the engine's native
                   `--granularity module` export (SCC contraction and
                   dominant-stage coloring engine-side): the guaranteed
                   fallback that renders for every workflow.

Rules:
- tiers are tried in order; the first that renders wins;
- rule-level tiers (1-2) are skipped when the workflow has more than
  MAX_RULE_STATIONS rules — publication maps stay readable (nf-core's
  reference maps carry ~40-60 stations; ours are rule-level, so the gate
  sits at the publication upper bound);
- every tier is computed from the same engine export — no per-pipeline
  data, no hand-authored maps.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
from collections import Counter, defaultdict

# Rule-level maps above this many stations switch to the overview tiers —
# mirroring the nf-core publication scale (~40-60 stations per map). Our
# rule-level stations are one per RULE whereas the published reference
# maps are one per process/tool group, so a 43-station rule map is already
# denser than a published 43-station reference — the gate sits at 40 and
# dense pipelines land on the module-stage/module overview plans (visual
# QA: atacseq at 43 rule stations was unreadable at site card width).
MAX_RULE_STATIONS = 40

# A rendered tier narrower than this (portrait-ish) falls through to the
# next tier: site pages host horizontal figures, and nf-core's reference
# maps are 1.6-3.2:1 landscape. The widest rendered tier wins when none
# clears the gate. 1.15 proved too strict — a fine 16-station map at
# 1.144 (live: genome-tracks) was demoted to a 2-station overview empty
# of meaning. 1.05 only rejects genuinely portrait maps.
MIN_ASPECT = 0.75

# Tool-granularity maps above this many stations fall through to the
# overview tiers. Process stations ARE the nf-core reference scale
# (~40-60), so the bound sits at the reference ceiling.
MAX_PROCESS_STATIONS = 60


# ---------------------------------------------------------------------------
# mmd transforms
# ---------------------------------------------------------------------------

def parse_mmd(text: str) -> dict:
    """Rule-level metro mmd → {line_decls, sections, order, node_sections,
    edges[(src, dst, label)]}."""
    lines_decl = {}
    sections: dict[str, dict] = {}
    order: list[str] = []
    node_sections: dict[str, str] = {}
    node_labels: dict[str, str] = {}
    edges: list[tuple[str, str, str | None]] = []
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("%%metro line:"):
            body = line.split(":", 1)[1].strip()
            parts = [p.strip() for p in body.split("|")]
            lines_decl[parts[0]] = (
                parts[1] if len(parts) > 1 else parts[0],
                parts[2] if len(parts) > 2 else None,
            )
        elif line.startswith("subgraph "):
            m = re.match(r"subgraph\s+(\S+)\s*\[(.*)\]", line)
            name, title = m.group(1), m.group(2)
            sections[name] = {"title": title, "nodes": []}
            order.append(name)
            current = name
        elif line == "end":
            current = None
        elif re.match(r"^\w+\[\[?", line):
            node = re.split(r"[\[\s]", line, maxsplit=1)[0]
            if current is None:
                # Single-section export: stations are top-level, outside any
                # subgraph — group them under one synthetic section.
                if "__main__" not in sections:
                    sections["__main__"] = {"title": "Workflow", "nodes": []}
                    order.append("__main__")
                current = "__main__"
            sections[current]["nodes"].append(node)
            node_sections[node] = current
            lm = re.search(r'\["(.*)"\]', line)
            if lm:
                node_labels[node] = lm.group(1)
        elif "-->" in line:
            m = re.match(r"^(\w+)\s*-->(?:\|([^|]*)\|)?\s*(\w+)", line)
            if m:
                edges.append((m.group(1), m.group(3), m.group(2)))
    return {
        "line_decls": lines_decl,
        "sections": sections,
        "order": order,
        "node_sections": node_sections,
        "node_labels": node_labels,
        "edges": edges,
    }


def station_count(mmd: dict) -> int:
    return len(mmd["node_sections"])


def flat_mmd(text: str) -> str:
    """Same graph, no subgraph sections."""
    lines = [
        l for l in text.splitlines()
        if not re.match(r"^\s*(subgraph|end)\b", l.strip())
    ]
    return "\n".join(lines) + "\n"


def scc_of(edges: list[tuple], order: list[str]) -> dict:
    """Tarjan SCC over stations; {station: representative} with the rep
    being the earliest station in section order. Cyclic station groups
    (module interdependencies can genuinely cycle even when the rule DAG
    does not) collapse into one merged station."""
    adj = defaultdict(set)
    for e in edges:
        adj[e[0]].add(e[1])
    index, low, stack, on_stack, idx = {}, {}, [], set(), [0]
    comps = []

    def visit(v):
        index[v] = low[v] = idx[0]
        idx[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in adj.get(v, ()):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for v in list(adj):
        if v not in index:
            visit(v)
    rep_of = {}
    for comp in comps:
        rep = min(comp, key=lambda s: order.index(s) if s in order else 10**6)
        for s in comp:
            rep_of[s] = rep
    return rep_of


def _join_compact(names: list[str]) -> str:
    """Module-stage station title: joined with ' • ', wrapped to <= 40 chars.

    SCC-merged stations can carry many module titles (live: sarek merged
    four groups into "Alignment + Variant Calling + Analysis + Read
    Trimming", 55 chars — nf-metro leaves such labels clipped at the
    viewport edge). Join compactly and wrap at group boundaries, which
    nf-metro renders as a second label line.
    """
    # Segment at " + " first (an SCC-merged section title already joins
    # several module titles), then wrap at segment boundaries. 40 chars is
    # still too wide for a leading station's label (sarek clipped
    # "Alignment + Variant Calling ..." at the viewport edge); 32 keeps
    # each label line inside the canvas.
    segments: list[str] = []
    for name in names:
        segments.extend(part for part in name.split(" + ") if part)
    joined = " • ".join(segments)
    if len(joined) <= 32:
        return joined
    lines, line = [], ""
    for seg in segments:
        cand = f"{line} • {seg}" if line else seg
        if line and len(cand) > 32:
            lines.append(line)
            line = seg
        else:
            line = cand
    lines.append(line)
    return "\\n".join(lines)


def _emit(lines_decl: dict, station_titles: dict, out_edges: list) -> str:
    used = {lab for _, _, lab in out_edges if lab}
    out = ["graph LR"]
    for name, (label, color) in lines_decl.items():
        if name in used:
            color_part = f" | {color}" if color else ""
            out.append(f"    %%metro line: {name} | {label}{color_part}")
    for sid in station_titles:
        out.append(f'    {sid}["{station_titles[sid]}"]')
    for s, t, lab in out_edges:
        label_part = f"|{lab}|" if lab else ""
        out.append(f"    {s} -->{label_part} {t}")
    return "\n".join(out) + "\n"


def module_stage_mmd(text: str) -> str:
    """One station per (section, stage) group; inter-module edges only.

    Intra-module stage hops are dropped: they add routing pressure and
    nf-metro degenerates on them (live: "route hanging in open space"
    aborts), and the overview reads fine without them.
    """
    mmd = parse_mmd(text)
    sections, order, edges = mmd["sections"], mmd["order"], mmd["edges"]
    node_sections = mmd["node_sections"]

    node_stage: dict[str, str] = {}
    out_line = Counter()
    for s, _t, lab in edges:
        if lab:
            out_line[(node_sections[s], s)] = lab
    any_line: dict[str, str] = {}
    for s, _t, lab in edges:
        if lab:
            any_line[s] = lab
    groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for node, sec in node_sections.items():
        stage = out_line.get((sec, node)) or any_line.get(node) or "generic"
        node_stage[node] = stage
        groups[(sec, stage)].append(node)

    seen = set()
    out_edges = []
    for s, t, _lab in edges:
        gs, gt = (node_sections[s], node_stage[s]), (node_sections[t], node_stage[t])
        if gs == gt or gs[0] == gt[0]:
            continue
        key = (gs, gt, node_stage[s])
        if key in seen:
            continue
        seen.add(key)
        out_edges.append((gs, gt, node_stage[s]))

    # SCC over (section, stage)-group nodes (two-element edge pairs: the
    # group keys themselves — a three-element pair keyed the rep_of map by
    # edges, so every lookup missed and the contraction never applied).
    rep_of = scc_of([(g1, g2) for g1, g2, _l in out_edges], order)
    station_groups: dict[tuple, list] = defaultdict(list)
    for g in groups:
        station_groups[rep_of.get(g, g)].append(g)
    # Folding rule: distinct stage-groups of the SAME section that would
    # repeat one long title collapse onto the section's first group. An
    # SCC-MERGED section ("align + variant + analysis + trim", live:
    # sarek) is exempt — its stage groups carry DIFFERENT stage names once
    # titled per-stage, and folding them would lose three of the four
    # flow shapes that loop inside the cyclic module.
    merged_sections = {
        rep[0]
        for rep in station_groups
        if " + " in sections.get(rep[0], {}).get("title", "")
    }
    first_of_section: dict[str, tuple] = {}
    for rep in station_groups:
        first_of_section.setdefault(rep[0], rep)

    def fold_key(rep: tuple) -> tuple:
        if rep[0] in merged_sections:
            return rep
        return first_of_section[rep[0]]

    section_groups: dict[tuple, list] = defaultdict(list)
    for rep, gs in station_groups.items():
        section_groups[fold_key(rep)].extend(gs)
    station_groups = section_groups
    station_titles = {}
    stage_display_names = {k: v[0] for k, v in mmd["line_decls"].items()}
    for rep, gs in station_groups.items():
        names = sorted({sections[g[0]]["title"] for g in gs})
        merged_title = any(" + " in name for name in names)
        title = _join_compact(names)
        # A section that itself is an SCC-merged set of modules carries a
        # "Alignment + Variant Calling + …" title; with several stage
        # groups of the same section each station then repeats that long
        # merged title (live: sarek — four stations all reading
        # "Alignment + Variant Calling + Analysis + Read Trimming").
        # Name those after the stage that drives them instead — four
        # distinct stage stations read like the nf-core idiom.
        if merged_title:
            title = stage_display_names.get(rep[1], rep[1])
        station_titles[f"g_{rep[0]}_{rep[1]}"] = title

    cedges: dict[tuple, Counter] = defaultdict(Counter)
    for gs, gt, lab in out_edges:
        rs, rt = rep_of.get(gs, gs), rep_of.get(gt, gt)
        if rs != rt:
            # Section-fold edge endpoints too: they must reference the same
            # stations the title map declares, or nf-metro renders the
            # undeclared endpoint as a bare `g_section_stage` station
            # (live: rnaseq showed "g_report_report" after the fold).
            rs, rt = fold_key(rs), fold_key(rt)
            if rs != rt:
                cedges[(f"g_{rs[0]}_{rs[1]}", f"g_{rt[0]}_{rt[1]}")][lab] += 1
    final = [(s, t, c.most_common(1)[0][0]) for (s, t), c in sorted(cedges.items())]
    return _emit(mmd["line_decls"], station_titles, final)


def subflow_view_mmd(text: str, sections_wanted: list[str]) -> str | None:
    """Module-level map of a single-entry multi-omics workflow subset.

    One station PER MODULE SECTION (the sub-flow's own namespaces), edges
    are the deduplicated inter-module dataflow edges INSIDE the set, each
    labelled by the source module's dominant stage line. The result reads
    like the nf-core idiom and stays legible at ten-ish stations — the
    earlier rule-level version dragged 147 stations into a DNA view and
    made sense to nobody.

    Returns None when no section matches.
    """
    mmd = parse_mmd(text)
    wanted = []
    for sec in mmd["order"]:
        bare = sec[2:] if sec.startswith("s_") else sec
        if any(
            sec == w or bare == w or bare.startswith(w)
            for w in sections_wanted if w
        ):
            wanted.append(sec)
    if not wanted:
        return None
    wanted_set = set(wanted)
    # dominant stage per section = first out-edge label of its stations
    node_sec = {n: s for n, s in mmd["node_sections"].items() if s in wanted_set}
    label_of = {
        n: mmd["node_labels"].get(n, mmd["sections"][s]["title"])
        for n, s in node_sec.items()
    }
    stage_of: dict[tuple[str, str], str] = {}
    for s, _t, lab in mmd["edges"]:
        if s in node_sec and lab:
            stage_of.setdefault((node_sec[s], s), lab)
    any_stage: dict[str, str] = {
        s: l for s, _t, l in mmd["edges"] if s in node_sec and l
    }
    dom_stage: dict[str, str] = {}
    for sec in wanted:
        first = None
        for n in [n for n, s in node_sec.items() if s == sec]:
            cand = stage_of.get((sec, n)) or any_stage.get(n)
            if cand:
                first = cand
                break
        dom_stage[sec] = first or "generic"
    # dedupe cross-module edges within the set
    seen = set()
    out_edges = []
    for s, t, lab in mmd["edges"]:
        if s not in node_sec or t not in node_sec:
            continue
        a, b = node_sec[s], node_sec[t]
        if a == b:
            continue
        if (a, b) in seen:
            continue
        seen.add((a, b))
        out_edges.append((a, b, dom_stage.get(a, lab)))
    # station ids: sanitized section
    import re as _re
    def sid(sec: str) -> str:
        return _re.sub(r"[^A-Za-z0-9_]", "_", sec)
    lines_used = {lab for _s, _t, lab in out_edges if lab}
    out = ["graph LR"]
    for name, (label, color) in mmd["line_decls"].items():
        if name in lines_used:
            out.append(f"    %%metro line: {name} | {label} | {color}")
    for sec in wanted:
        out.append(
            f'    {sid(sec)}["{mmd["sections"][sec]["title"]}"]'
        )
    for a, b, lab in out_edges:
        lpart = f"|{lab}|" if lab else ""
        out.append(f"    {sid(a)} -->{lpart} {sid(b)}")
    return "\n".join(out) + "\n"



def svg_aspect(svg: pathlib.Path) -> float | None:
    """viewBox width/height of a rendered map (None when unparsable)."""
    head = svg.read_text()[:4096]
    m = re.search(r'viewBox="[\d.\- ]*?(\d+(?:\.\d+)?)[, ]+(\d+(?:\.\d+)?)"', head)
    if not m:
        return None
    w, h = float(m.group(1)), float(m.group(2))
    return w / h if h else None


def render_mmd(nf_metro: str, mmd: pathlib.Path, svg: pathlib.Path) -> str | None:
    """nf-metro render → svg; None on success, failure cause otherwise.

    Spacing policy: 130/70 clears long station labels from the viewport
    edge (live: sarek's module-stage row labels were clipped on the left)
    and keeps the legend clear of the trunk; the auto-adaptive default
    under-allocates there. Small maps (fewer than 15 stations) are better
    with the auto spacing — the fixed 130/70 stretched a 7-station map
    (mixscape) to a 0.98 portrait, which the aspect gate then rejected
    and the ladder over-demoted to a 1-station overview. Rendering policy
    lives here, not in the engine.
    """
    # Small maps keep the auto x-spacing but pin y=60: the auto track
    # pitch leaves the off-track station stack (live: mixscape, 4
    # off-track exports) overlapping labels. 60px separates them.
    stations = station_count(parse_mmd(mmd.read_text()))
    spacing = (
        ["--y-spacing", "60"]
        if stations < 15
        else ["--x-spacing", "130", "--y-spacing", "70"]
    )
    proc = subprocess.run(
        [nf_metro, "render", str(mmd), "-o", str(svg), "--theme", "light", *spacing],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        cause = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "unknown"
        return f"nf-metro failed: {cause}"
    if not svg.is_file() or svg.stat().st_size == 0:
        return "nf-metro produced no output"
    # Light theme must not bake a dark `nf-metro-bg` rect (site issue #16).
    if "nf-metro-bg" in svg.read_text():
        return "nf-metro rendered a dark background — not light-theme clean"
    pad_viewport_left(svg)
    return None


def pad_viewport_left(svg: pathlib.Path) -> None:
    """Widen a rendered SVG's viewBox so no station label clips at the edge.

    nf-metro center-anchors station labels at the station x; a wide label
    on the leftmost column extends past the viewBox and is silently
    clipped (live: sarek's two-line merged title lost its first line).
    Estimate each label's extent (14px font ≈ 7.2px/char) and grow the
    left edge of the viewBox to fit the widest overflow, plus a 12px pad.
    Every tier gets the same treatment so the fix is tier-agnostic.
    """
    text = svg.read_text()
    m = re.search(r'viewBox="([\d.\- ]+)"', text)
    if not m:
        return
    try:
        x0, y0, w, h = [float(v) for v in m.group(1).replace(",", " ").split()]
    except ValueError:
        return
    # Most-negative overflow: labels extend PAST the left edge (negative
    # x-extent); max() over 0.0 would silently clip the measurement.
    overflow = 0.0
    for mm in re.finditer(r'<text\s([^>]*)>(.*?)</text>', text, re.S):
        attrs, body = mm.group(1), mm.group(2)
        if "data-station-id" not in attrs or "text-anchor=\"middle\"" not in attrs:
            continue
        xm = re.search(r'x="([\d.]+)"', attrs)
        if not xm:
            continue
        x = float(xm.group(1))
        # Multi-line labels are a <text> with several <tspan>s: estimate
        # EVERY line (the widest line governs the overflow).
        lines = re.findall(r'<tspan[^>]*>([^<]+)</tspan>', body) or [body]
        for line in lines:
            # 14px nf-metro font: ~8.2px per glyph in practice (Inter bold,
            # letter spacing); under-estimating leaves a glyph clipped.
            est = len(line.replace(" ", "")) * 8.2 + line.count(" ") * 4.0
            candidate = x - est / 2
            if candidate < overflow:
                overflow = candidate
    if overflow < 0:
        new_x0 = x0 + overflow - 20
        new_text = re.sub(
            r'viewBox="[\d.\- ]+"',
            f'viewBox="{new_x0:.0f} {y0:.0f} {w - (new_x0 - x0):.0f} {h:.0f}"',
            text,
            count=1,
        )
        svg.write_text(new_text)


def render_ladder(
    name: str,
    workflow: pathlib.Path,
    binary: str,
    nf_metro: str,
    svg: pathlib.Path,
    detail_svg: pathlib.Path | None = None,
) -> tuple[str | None, dict | None]:
    """Export the engine's canonical metro mmd and walk the tier ladder.

    Returns (None, tier_info) on success or (failure_reason, None). The
    tier info is recorded in configs.json so pages can label the map
    (overview vs rule-level).
    """
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = pathlib.Path(tmpdir)
        mmd = tmp / "graph.mmd"
        graph = subprocess.run(
            [binary, "graph", "-f", "metro", "-o", str(mmd), str(workflow)],
            capture_output=True,
            text=True,
        )
        if graph.returncode != 0:
            cause = graph.stderr.strip().splitlines()[-1] if graph.stderr.strip() else "unknown"
            return f"graph failed: {cause}", None
        text = mmd.read_text()
        stations = station_count(parse_mmd(text))

        # The engine's native module tier (graph --granularity module,
        # engine >= 0.17.3) is the guaranteed fallback: one station per
        # contracted section, renders for every workflow. Graceful skip
        # on older engines keeps the ladder working mid-upgrade.
        mod_mmd = tmp / "module.mmd"
        mod_graph = subprocess.run(
            [
                binary,
                "graph",
                "-f",
                "metro",
                "--granularity",
                "module",
                "-o",
                str(mod_mmd),
                str(workflow),
            ],
            capture_output=True,
            text=True,
        )
        module_source = mod_mmd.read_text() if mod_graph.returncode == 0 else None

        # The engine's process tier (graph --granularity process): rules
        # chain-connected under one tool collapse into tool-named stations
        # (the nf-core transit-map idiom, ~40-60 stations). A workflow with
        # FEW modules (live: methylseq 61 rules/2 modules, nanoseq 52/3)
        # gets a two-station module-stage map otherwise, losing its whole
        # pipeline shape. Rendered at tool granularity it stays readable
        # (methylseq: 46 tool stations) and the page keeps its info density.
        proc_mmd = tmp / "process.mmd"
        proc_graph = subprocess.run(
            [
                binary,
                "graph",
                "-f",
                "metro",
                "--granularity",
                "process",
                "-o",
                str(proc_mmd),
                str(workflow),
            ],
            capture_output=True,
            text=True,
        )
        process_source = proc_mmd.read_text() if proc_graph.returncode == 0 else None

        # TWO-TIER output — every page reads the same way:
        #   overview  = module-stage (module·stage idiom) or module when
        #               module-stage does not render — one station per
        #               module on EVERY page, so "a point = a module" is
        #               site-wide constant ("展示水平统一");
        #   detail    = rule-level figure (<name>-rules.svg), the exact
        #               graph of every rule, behind a collapsed card.
        # The old "pick the finest tier that renders" logic made
        # neighboring pages show rules, tools or modules with no common
        # reading model — the system problem this replaces.
        tiers = [
            ("rule-sections", text, True, None),
            ("rule-flat", flat_mmd(text), True, None),
            ("module-stage", module_stage_mmd(text), False, None),
            ("module", module_source, False, None),
        ]
        best = None      # (aspect, tier_svg_path, info) — the OVERVIEW
        detail = None    # (aspect, tier_svg_path, info) — rule-level figure
        last_err = None
        for tier, source, is_rule_level, max_stations in tiers:
            if source is None:
                continue
            (tmp / f"{tier}.mmd").write_text(source)
            tier_svg = tmp / f"{tier}.svg"
            err = render_mmd(nf_metro, tmp / f"{tier}.mmd", tier_svg)
            if err is not None:
                last_err = err
                continue
            aspect = svg_aspect(tier_svg)
            tier_stations = station_count(parse_mmd(source))
            info = {
                "tier": tier,
                "stations": tier_stations,
                "is_rule_level": is_rule_level,
                "aspect": round(aspect, 2) if aspect else None,
            }
            if tier in ("rule-sections", "rule-flat"):
                if detail is None:
                    detail = (aspect if aspect is not None else 0.0, tier_svg, info)
                continue
            if best is None or aspect is None or aspect > best[0]:
                best = (aspect if aspect is not None else 0.0, tier_svg, info)
            # Tiny maps are exempt from the landscape gate (mirroring
            # qa-metro's SMALL_EXEMPT): a 3-station map at 0.99 aspect is
            # fine; over-demoting it loses meaning for no layout gain.
            if aspect is None or aspect >= MIN_ASPECT or tier_stations <= 5:
                best_svg = tier_svg
                break
        # Rule-level detail figure (informational, no readability gate —
        # it sits behind a collapsed card where size is irrelevant).
        if detail is not None and detail_svg is not None:
            shutil.copyfile(detail[1], detail_svg)
        # Degenerate overview (a one/two-module workflow whose overview
        # conveys nothing, live: unsupervised/methylseq) uses the rule
        # detail as the primary figure instead — information over
        # simplicity, exactly the trade the unified rule documents.
        if best is not None and best[2]["stations"] <= 2 and detail is not None:
            best = detail
        if best is None:
            return last_err, None
        # The chosen tier's render becomes the committed artifact.
        shutil.copyfile(best[1], svg)
        return None, best[2]
