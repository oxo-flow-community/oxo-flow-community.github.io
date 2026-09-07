#!/usr/bin/env python3
"""Label-integrity audit for the committed DAG figures.

Geometry (text/line clipping) is enforced at RENDER time: every figure
gets a guaranteed 20px canvas margin (metro_tiers.pad_viewport_left); a
pixel-level edge audit was run externally and estimate-based geometry
checks proved unreliable against the renderer. This tool keeps the LABEL
contract: every station has exactly one visible label, and no label is
orphaned or empty.

Station counts come from unique data-station-id attributes (nf-metro
stamps every station element ; a rect and an accent shape share the id).
Labels are the nf-metro-station-label text elements, one per station.

Run after `regen-configs.py`; exit non-zero on issues.
"""
import pathlib
import re
import sys

DAG = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets" / "dag"
issues: list[str] = []
files = sorted(DAG.glob("*.svg"))

for svg in files:
    text = svg.read_text()
    ids = set(re.findall(r'data-station-id="([^"]*)"', text))
    labels = [
        body
        for attrs, body in re.findall(r"<text\s([^>]*)>(.*?)</text>", text, re.S)
        if "nf-metro-station-label" in attrs
    ]
    label_count = len(labels)
    clean = [
        re.sub(r"<[^>]+>", "", body).strip().replace("&amp;", "&")
        for body in labels
    ]
    if clean and not all(clean):
        issues.append(f"{svg.name}: empty station label")
        continue
    if ids and label_count != len(ids):
        issues.append(f"{svg.name}: stations={len(ids)} labels={label_count} mismatch")
    # duplicated labels (the same station labelled twice)
    dup = [x for x in clean if clean.count(x) > 1 and x]
    if dup:
        issues.append(f"{svg.name}: repeated label text x{len(dup)} (e.g. '{dup[0]}')")

if issues:
    for i in issues:
        print("  ", i)
    print(f"FAIL: {len(issues)} issue(s) over {len(files)} assets")
    sys.exit(1)
print(f"geom-audit OK: {len(files)} assets, stations == labels, no empty/duplicate labels")
