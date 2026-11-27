#!/usr/bin/env python3
"""Idempotently give committed DAG SVGs an accessible name.

The transit-map SVGs open bare in a new tab (wide card) with no accessible
name and screen readers announce nothing. Inserts
`<title>…workflow DAG…</title>` + role="img" right after the opening <svg>
tag (and a <desc> naming the pipeline). Runs over docs/assets/dag/*.svg —
safe to re-run (files already carrying a <title> are skipped). regen-configs
calls ensure_svg_title() at each placement site so regenerations keep it."""
import pathlib
import re
import sys

DAG = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets" / "dag"

def ensure_svg_title(text: str, name: str, desc: str | None = None) -> str:
    m = re.search(r"<svg\b[^>]*>", text, re.S)
    if not m:
        raise SystemExit(f"no opening <svg> tag — refusing to guess: {name}")
    open_tag = m.group(0)
    body = ""
    if "<title" not in text:
        if "role=" not in open_tag:
            open_tag = open_tag[:-1] + ' role="img">'
        title = f"<title>{name} workflow DAG</title>"
        d = f"<desc>{desc}</desc>" if desc else ""
        body = title + d
    elif "role=" not in open_tag:
        open_tag = open_tag[:-1] + ' role="img">'
    else:
        return text  # already named and labeled
    return text[: m.start()] + open_tag + body + text[m.end():]

def main() -> None:
    import json
    names = [p["name"] for p in json.loads(
        (DAG.parent.parent.parent / "data" / "pipelines.json").read_text())]
    changed = 0
    total = 0
    for f in sorted(DAG.glob("*.svg")):
        total += 1
        stem = f.stem
        # Longest registry name that is the stem itself or its dash-prefixed
        # base (handles compound names like oxo-flow-rnaseq-star-deseq2
        # versus view/rules variants oxo-flow-<name>-<view>.svg).
        cands = [n for n in names if stem == n or stem.startswith(n + "-")]
        if not cands:
            raise SystemExit(f"{f.name}: matches no registry name — refusing to guess")
        base = max(cands, key=len)
        old = f.read_text()
        new = ensure_svg_title(old, base)
        if new != old:
            f.write_text(new)
            changed += 1
    print(f"title-injected: {changed}, already-ok: {total - changed}")

if __name__ == "__main__":
    main()
