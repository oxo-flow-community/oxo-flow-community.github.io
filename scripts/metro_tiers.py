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
MIN_ASPECT = 1.05


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
        elif "-->" in line:
            m = re.match(r"^(\w+)\s*-->(?:\|([^|]*)\|)?\s*(\w+)", line)
            if m:
                edges.append((m.group(1), m.group(3), m.group(2)))
    return {
        "line_decls": lines_decl,
        "sections": sections,
        "order": order,
        "node_sections": node_sections,
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
    # One station per section for the overview: distinct stage-groups of
    # the same section (a cyclic-merged module like sarek's four-way
    # "align + variant + analysis + trim", or stages that only connect
    # inside the module, live: rnaseq's fastq_qc generic group) would emit
    # several stations carrying the same long title — fold each section
    # onto its first (main) group, which also keeps isolated groups off
    # the map as phantom stations.
    first_of_section: dict[str, tuple] = {}
    for rep in station_groups:
        first_of_section.setdefault(rep[0], rep)
    section_groups: dict[tuple, list] = defaultdict(list)
    for rep, gs in station_groups.items():
        section_groups[first_of_section[rep[0]]].extend(gs)
    station_groups = section_groups
    station_titles = {}
    for rep, gs in station_groups.items():
        names = sorted({sections[g[0]]["title"] for g in gs})
        station_titles[f"g_{rep[0]}_{rep[1]}"] = _join_compact(names)

    cedges: dict[tuple, Counter] = defaultdict(Counter)
    for gs, gt, lab in out_edges:
        rs, rt = rep_of.get(gs, gs), rep_of.get(gt, gt)
        if rs != rt:
            # Section-fold edge endpoints too: they must reference the same
            # stations the title map declares, or nf-metro renders the
            # undeclared endpoint as a bare `g_section_stage` station
            # (live: rnaseq showed "g_report_report" after the fold).
            rs, rt = first_of_section.get(rs[0], rs), first_of_section.get(rt[0], rt)
            if rs != rt:
                cedges[(f"g_{rs[0]}_{rs[1]}", f"g_{rt[0]}_{rt[1]}")][lab] += 1
    final = [(s, t, c.most_common(1)[0][0]) for (s, t), c in sorted(cedges.items())]
    return _emit(mmd["line_decls"], station_titles, final)


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
    under-allocates there. Rendering policy lives here, not in the engine.
    """
    proc = subprocess.run(
        [nf_metro, "render", str(mmd), "-o", str(svg), "--theme", "light",
         "--x-spacing", "130", "--y-spacing", "70"],
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
    return None


def render_ladder(
    name: str,
    workflow: pathlib.Path,
    binary: str,
    nf_metro: str,
    svg: pathlib.Path,
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

        tiers = [
            # Sections first: the module grouping is the nf-core transit
            # idiom and the off_track directive (engine-side) relieves the
            # routing pressure that previously forced the flat fallback
            # (live: 16-station genome-tracks renders sectioned at 1.2
            # aspect where flat is 0.74).
            ("rule-sections", text, True),
            ("rule-flat", flat_mmd(text), True),
            ("module-stage", module_stage_mmd(text), False),
            ("module", module_source, False),
        ]
        best = None  # (aspect, tier_svg_path, info) — the widest rendered tier
        for tier, source, is_rule_level in tiers:
            if source is None:
                continue
            if is_rule_level and stations > MAX_RULE_STATIONS:
                continue
            (tmp / f"{tier}.mmd").write_text(source)
            tier_svg = tmp / f"{tier}.svg"
            err = render_mmd(nf_metro, tmp / f"{tier}.mmd", tier_svg)
            if err is not None:
                last_err = err
                continue
            aspect = svg_aspect(tier_svg)
            tier_stations = (
                stations if is_rule_level else station_count(parse_mmd(source))
            )
            info = {
                "tier": tier,
                "stations": tier_stations,
                "is_rule_level": is_rule_level,
                "aspect": round(aspect, 2) if aspect else None,
            }
            if best is None or aspect is None or aspect > best[0]:
                best = (aspect if aspect is not None else 0.0, tier_svg, info)
            if aspect is None or aspect >= MIN_ASPECT:
                best_svg = tier_svg
                break
        if best is None:
            return last_err, None
        # The chosen tier's render becomes the committed artifact.
        shutil.copyfile(best[1], svg)
        return None, best[2]
