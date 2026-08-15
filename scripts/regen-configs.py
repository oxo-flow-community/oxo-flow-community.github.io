#!/usr/bin/env python3
"""Regenerate data/configs.json and the per-pipeline DAG SVGs from the
staged workflow files.

For every cataloged pipeline:

  - runs `oxo-flow info` on its workflow file (main.oxoflow first, else the
    first root *.oxoflow, then workflow/*.oxoflow or *.toml) and stores the
    derived `config` records — the data behind each run-notes page's
    Parameters table;
  - renders the rule-level DAG with `oxo-flow graph -f dot` + Graphviz into
    docs/assets/dag/<name>.svg — the image behind each page's Workflow graph
    section.

Both outputs are committed, so site CI stays hermetic (no engine binary, no
network); regenerate locally whenever a staged workflow changes, then run
generate.py and commit everything.

Requirements: an oxo-flow binary ($OXO_FLOW, `oxo-flow` on PATH, or
../bin/oxo-flow) and Graphviz `dot` on PATH.
Pipelines without a staged workflow file are skipped with a warning (their
pages simply omit the Parameters and Workflow graph sections).
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "pipelines.json"
OUT = ROOT / "data" / "configs.json"
DAG_DIR = ROOT / "docs" / "assets" / "dag"
STAGING = pathlib.Path.home() / "Documents" / "GitHub" / "oxo-community" / "staging"


def engine_binary() -> str:
    if env := os.environ.get("OXO_FLOW"):
        return env
    if found := shutil.which("oxo-flow"):
        return found
    sibling = ROOT.parent / "bin" / "oxo-flow"
    if sibling.is_file():
        return str(sibling)
    raise SystemExit(
        "oxo-flow binary not found (set $OXO_FLOW, add it to PATH, or build ../bin/oxo-flow)"
    )


def require_dot() -> str:
    if found := shutil.which("dot"):
        return found
    raise SystemExit(
        "graphviz `dot` not found on PATH (install Graphviz, e.g. "
        "`brew install graphviz` / `conda install graphviz`)"
    )


def workflow_file(name: str) -> pathlib.Path | None:
    """main.oxoflow first, then any other root *.oxoflow, then workflow/*."""
    repo = STAGING / name
    if not repo.is_dir():
        return None
    root_file = repo / "main.oxoflow"
    if root_file.is_file():
        return root_file
    root_candidates = [
        p for p in sorted(repo.glob("*.oxoflow")) if p.name != "main.oxoflow"
    ]
    if root_candidates:
        return root_candidates[0]
    candidates = sorted(repo.glob("workflow/*.oxoflow")) + sorted(
        repo.glob("workflow/*.toml")
    )
    return candidates[0] if candidates else None


def derive(name: str, workflow: pathlib.Path, binary: str) -> list[dict]:
    proc = subprocess.run(
        [binary, "info", str(workflow)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"info failed for {name}: {proc.stderr.strip()}")
    meta = json.loads(proc.stdout)
    return meta.get("config", [])


def render_dag(name: str, workflow: pathlib.Path, binary: str, dot: str) -> None:
    """`oxo-flow graph -f dot` → Graphviz SVG, committed per pipeline."""
    svg = DAG_DIR / f"{name}.svg"
    with tempfile.TemporaryDirectory() as tmp:
        dot_file = pathlib.Path(tmp) / f"{name}.dot"
        graph = subprocess.run(
            [binary, "graph", "-f", "dot", "-o", str(dot_file), str(workflow)],
            capture_output=True,
            text=True,
        )
        if graph.returncode != 0:
            raise SystemExit(f"graph failed for {name}: {graph.stderr.strip()}")
        render = subprocess.run(
            [dot, "-Grankdir=LR", "-Gbgcolor=transparent", "-Tsvg",
             "-o", str(svg), str(dot_file)],
            capture_output=True,
            text=True,
        )
        if render.returncode != 0:
            raise SystemExit(f"dot failed for {name}: {render.stderr.strip()}")


def main() -> int:
    pipelines = json.loads(DATA.read_text())
    binary = engine_binary()
    dot = require_dot()
    DAG_DIR.mkdir(parents=True, exist_ok=True)
    configs = {}
    rendered = 0
    for p in pipelines:
        name = p["name"]
        workflow = workflow_file(name)
        if workflow is None:
            print(
                f"warning: {name}: no staged workflow file, "
                "Parameters + Workflow graph omitted",
                file=sys.stderr,
            )
            continue
        configs[name] = {
            "workflow": str(workflow.relative_to(STAGING / name)),
            "config": derive(name, workflow, binary),
        }
        render_dag(name, workflow, binary, dot)
        rendered += 1
    OUT.write_text(json.dumps(configs, indent=2) + "\n")
    print(
        f"generated: {OUT.name} ({len(configs)}/{len(pipelines)} pipelines) "
        f"+ {rendered} DAG SVGs in {DAG_DIR.relative_to(ROOT)}/"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
