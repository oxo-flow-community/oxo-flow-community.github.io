#!/usr/bin/env python3
"""Regenerate data/configs.json from the staged workflow files.

For every cataloged pipeline, runs `oxo-flow info` on its workflow file
(main.oxoflow first, else the first workflow/*.oxoflow or *.toml) and stores
the derived `config` records — the data behind each run-notes page's
Parameters table. The output is committed, so site CI stays hermetic (no
engine binary, no network); regenerate locally whenever a staged workflow
changes, then run generate.py and commit both.

Engine binary lookup: $OXO_FLOW, then `oxo-flow` on PATH, then ../bin/oxo-flow.
Pipelines without a staged workflow file are skipped with a warning (their
pages simply omit the Parameters section).
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "pipelines.json"
OUT = ROOT / "data" / "configs.json"
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


def main() -> int:
    pipelines = json.loads(DATA.read_text())
    binary = engine_binary()
    configs = {}
    for p in pipelines:
        name = p["name"]
        workflow = workflow_file(name)
        if workflow is None:
            print(
                f"warning: {name}: no staged workflow file, Parameters omitted",
                file=sys.stderr,
            )
            continue
        configs[name] = {
            "workflow": str(workflow.relative_to(STAGING / name)),
            "config": derive(name, workflow, binary),
        }
    OUT.write_text(json.dumps(configs, indent=2) + "\n")
    print(f"generated: {OUT.name} ({len(configs)}/{len(pipelines)} pipelines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
