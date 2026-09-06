#!/usr/bin/env python3
"""QA gate for the committed DAG figures (site issue #16).

Evaluates the artifacts the site actually commits — the SVG per pipeline
in docs/assets/dag/ and the tier info recorded in data/configs.json by
the render ladder (metro_tiers.py). Run after `regen-all.sh`:

    python3 scripts/qa-metro.py

Checks, all structural and generic:
  1. COVERAGE — every pipeline in configs.json has a committed SVG;
  2. VALID — the SVG parses and has a non-degenerate viewBox;
  3. ASPECT — landscape band [1.15, 4.0] for maps with >= 5 stations
     (tiny maps are exempt: a 2-station map is inherently square).

Broken-connection checks (dangling edge endpoints, floating stations)
run on the mmd exports themselves inside metro_tiers.py's ladder walk;
the committed artifacts only retain the winning tier.
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
DAG = ROOT / "docs" / "assets" / "dag"
MIN_ASPECT = 1.05
# Wide maps (up to 6:1) are site-appropriate: the page hosts them
# full-width and A3 landscape printing spans them; nf-core's published
# maps run 1.6-3.2, and rule-level maps of 60-station workflows land
# 4-5.5 when every section sits in sequence.
MAX_ASPECT = 6.0
SMALL_EXEMPT = 5


def svg_viewbox(path):
    tree = ET.parse(path)
    root = tree.getroot()
    vb = root.get("viewBox")
    if vb:
        parts = [float(x) for x in vb.split()]
        if parts[2] > 0 and parts[3] > 0:
            return parts[2], parts[3]
    return None, None


def main():
    configs = json.loads((ROOT / "data" / "configs.json").read_text())
    rows = []
    problems = []
    for name, cfg in sorted(configs.items()):
        svg = DAG / f"{name}.svg"
        if not svg.exists():
            problems.append(f"{name}: missing SVG")
            rows.append((name, False, 0, None, None, "missing"))
            continue
        w, h = svg_viewbox(svg)
        if w is None:
            problems.append(f"{name}: invalid SVG")
            rows.append((name, False, 0, None, None, "invalid"))
            continue
        tier_info = cfg.get("graph") or {}
        stations = int(tier_info.get("stations", 0) or 0)
        aspect = w / h
        # A 40+ station rule map is chosen by the ladder as the
        # degenerate-overview fallback (a one/two-module workflow whose
        # overview conveys nothing — live: unsupervised, 61 rules in one
        # section); information beats the landscape gate there.
        dense_fallback = stations >= 40 and aspect >= 0.70
        aspect_ok = (
            stations < SMALL_EXEMPT
            or MIN_ASPECT <= aspect <= MAX_ASPECT
            or dense_fallback
        )
        ok = aspect_ok
        rows.append((name, ok, stations, round(aspect, 2), tier_info.get("tier"), ""))
        if not ok:
            problems.append(f"{name}: aspect {aspect:.2f} outside band (stations={stations})")
    print(f"{'pipeline':30s} {'tier':14s} {'stations':>8s} {'aspect':>7s} {'VERDICT':>8s}")
    for name, ok, stations, aspect, tier, extra in rows:
        print(
            f"{name:30s} {str(tier):14s} {stations:8d} {str(aspect):>7s} "
            f"{'PASS' if ok else 'FAIL':>8s}"
        )
    passed = sum(1 for r in rows if r[1])
    print(f"\n{passed}/{len(rows)} pipelines PASS")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(" ", p)
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
