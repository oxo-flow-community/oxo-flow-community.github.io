"""Unified author-side semantic-map renderer (hand-drawn metro style).

Reads a semantic `.mmd` (the machine-audited route drawing — every hop
is a real engine edge), and produces the site SVG with TOTAL layout
control and ONE font/style across every pipeline:

  - one grey main line, stations in flow order, labels above the stops;
  - orange assist routes hanging in a ladder (branches off the rail);
  - hidden junction `_aligned`-style nodes drawn as small dark dots;
  - JetBrains Mono stack @ 20px everywhere, ink #333333, white canvas,
    legend card bottom-left (fixed geometry, never overlaps).

The engine never infers layout — we ARE the author.
"""
import pathlib, re

MONO = "JetBrains Mono, Menlo, monospace"
INK = "#333333"
MAIN = "#79706E"
ASSIST = "#E8A33D"
FONT = 20
RAIL_Y = 86
STEP = 190
ROW = 76


def parse_hops(mmd: str) -> list[tuple[str, str, str]]:
    hops = []
    for line in mmd.splitlines():
        m = re.match(r'\s*([\w_+]+)(?:\[[^\]]*\])?\s*-->\|([^|]*)\|\s*([\w_+]+)(?:\[[^\]]*\])?', line)
        if m:
            hops.append((m.group(1), m.group(2), m.group(3)))
    return hops


def draw(name: str, mmd: str) -> str:
    hops = parse_hops(mmd)
    main = [(a, b) for a, l, b in hops if l == 'main']
    assist = [(a, b) for a, l, b in hops if l != 'main']
    # order chain by main hops (sources first)
    in_main = {b for a, b in main}
    starts = [a for a, b in main if a not in in_main or a not in [x for x, y in main if y == x]]
    chain: list[str] = []
    frontier = [s for s in starts if s not in chain]
    while frontier:
        cur = frontier.pop(0)
        if cur in chain:
            continue
        chain.append(cur)
        for a, b in main:
            if a == cur and b not in chain and b not in frontier:
                frontier.append(b)
    for a, b in main:
        if a not in chain:
            chain.append(a)
        if b not in chain:
            chain.append(b)
    # branch stations: assist targets; attach point = their assist source if on chain,
    # else the last chain station before it.
    branches = []
    for a, b in assist:
        if b.startswith('_') or b in chain:
            # into-main merges are already expressed by the rail itself
            continue
        branches.append((b, a))
    juncts = [n for a, l, b in hops for n in (a, b) if n.startswith('_')]

    # ---- layout ----
    widths = {s: max(60, int(0.72 * FONT * max(3, len(s)))) for s in chain}
    positions: dict[str, int] = {}
    x = 70
    for s in chain:
        positions[s] = x
        x += max(STEP, widths[s] + 66)
    total_w = x + 60
    # assist labels extend right of their nodes — extend canvas past them
    ext = 0
    for (b, _parent) in branches:
        if b in positions:
            ext = max(ext, positions[b] + int(0.72 * FONT * len(b)) + 40)
    total_w = max(total_w, ext)
    rows: dict[str, int] = {}
    for k, (a, b) in enumerate(assist):
        if not b.startswith('_'):
            rows[b] = k
    n_assist = max(10, len(rows) + 2)
    total_h = RAIL_Y + max(n_assist, len(branches) + 1) * ROW + 120

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="-20 -20 {total_w + 40} {total_h + 40}">']
    svg.append('<defs><marker id="arr" markerWidth="13" markerHeight="13" refX="10" refY="6.5" orient="auto">'
               '<path d="M0 0 L13 6.5 L0 13 z" fill="#79706E"/></marker>'
               '<marker id="arru" markerWidth="13" markerHeight="13" refX="10" refY="6.5" orient="auto">'
               '<path d="M0 0 L13 6.5 L0 13 z" fill="#E8A33D"/></marker></defs>')
    svg.append(f'<rect x="-30" y="-30" width="{total_w + 80}" height="{total_h + 80}" fill="#ffffff"/>')
    svg.append(f'<text x="{total_w - 210}" y="-8" font-size="15" fill="#999999" font-family="{MONO}" text-anchor="end">condensed semantic view · edges subset-checked</text>')

    def px(n):
        return positions.get(n, 70)
    def py(n):
        return RAIL_Y + 130 + rows.get(n, 0) * ROW

    for k, (b, parent) in enumerate(branches):
        if b not in positions:
            positions[b] = (px(parent) if parent != 'float' else 60) + 70 + (k % 3) * 86
    # main rail path
    pts = [(px(s), RAIL_Y) for s in chain]
    d = 'M ' + ' L '.join(f'{x} {y}' for x, y in pts)
    svg.append(f'<path d="{d}" fill="none" stroke="{MAIN}" stroke-width="7" marker-mid="url(#arr)"/>')
    # junction dots on rail (hidden collectors, e.g. _aligned): right after the
    # last main stop that feeds them
    for j in juncts:
        feeds = [a for a, l, b in hops if a != j and b == j]
        if not feeds:
            continue
        jx = px(feeds[-1]) + 60 if feeds[-1] in positions else total_w - 110
        svg.append(f'<circle cx="{jx}" cy="{RAIL_Y}" r="7" fill="#79706E"/>')
    # branch ladder (branches whose target is off the chain) + MERGE hops:
    # an assist hop whose target IS on the chain is drawn as a ladder bump
    # that rejoins the rail (down, right, back up) — the real converge.
    def draw_branch(ax, ay, bx, by):
        r = min(28, max(10, by - ay - 20))
        d2 = f'M {ax} {ay} L {ax} {by - r} Q {bx} {by - r} {bx} {by}'
        svg.append(f'<path d="{d2}" fill="none" stroke="{ASSIST}" stroke-width="5" marker-end="url(#arru)"/>')
    for (b, parent) in branches:
        if parent == 'float':
            continue
        draw_branch(px(parent), RAIL_Y, px(b) if b in positions else total_w - 110, py(b))
    for (a, b) in [(x, y) for x, l, y in hops if l != 'main' and y in chain and x in chain]:
        # both on the rail: short under-rail merge (down, right, back up)
        ax, bx, by = px(a), px(b), RAIL_Y
        drop = RAIL_Y + 40
        r = 22
        d2 = (f'M {ax} {by} L {ax} {drop} Q {ax} {drop + r} {bx} {drop + r} '
              f'L {bx} {by + 40} L {bx} {by}')
        svg.append(f'<path d="{d2}" fill="none" stroke="{ASSIST}" stroke-width="5" marker-end="url(#arru)"/>')
    for (a, b) in [(x, y) for x, l, y in hops if l != 'main' and y in chain and x not in chain]:
        # merge hop: from source branch station up into the rail at b
        ax = px(a) if a in positions else total_w - 110
        bx = px(b)
        ay = py(a) if a in rows else RAIL_Y + len(rows) * ROW + 90
        by = RAIL_Y
        r = min(26, max(10, ay - by - 20))
        d2 = f'M {ax} {ay} Q {ax} {by + r} {bx} {by + r} L {bx} {by}'
        svg.append(f'<path d="{d2}" fill="none" stroke="{ASSIST}" stroke-width="5" marker-end="url(#arru)"/>')
    # stations
    for s in chain:
        if s.startswith('_'):
            continue
        x0 = px(s)
        svg.append(f'<circle cx="{x0}" cy="{RAIL_Y}" r="8" fill="#ffffff" stroke="{MAIN}" stroke-width="3"/>')
        svg.append(f'<text x="{x0}" y="{RAIL_Y - 26}" font-size="{FONT}" fill="{INK}" font-family="{MONO}">{s}</text>')
    for (b, parent) in branches:
        x0, y0 = px(b), py(b)
        svg.append(f'<circle cx="{x0}" cy="{y0}" r="8" fill="#ffffff" stroke="{ASSIST}" stroke-width="3"/>')
        svg.append(f'<text x="{x0 + 18}" y="{y0 + 7}" font-size="{FONT}" fill="{INK}" font-family="{MONO}">{b}</text>')
    # shared legend card
    lx, ly = 40, total_h - 118
    svg.append(f'<rect x="{lx}" y="{ly}" width="332" height="112" rx="10" fill="#f8f8f8" stroke="#dddddd"/>')
    svg.append(f'<path d="M {lx + 14} {ly + 30} L {lx + 82} {ly + 30}" stroke="{MAIN}" stroke-width="7"/>')
    svg.append(f'<text x="{lx + 96}" y="{ly + 37}" font-size="{FONT}" fill="{INK}" font-family="{MONO}">Main pipeline</text>')
    svg.append(f'<path d="M {lx + 14} {ly + 74} L {lx + 82} {ly + 74}" stroke="{ASSIST}" stroke-width="5"/>')
    svg.append(f'<text x="{lx + 96}" y="{ly + 81}" font-size="{FONT}" fill="{INK}" font-family="{MONO}">Assist routes</text>')
    svg.append('</svg>')
    return '\n'.join(svg)
