#!/usr/bin/env python3
"""Regenerate data/configs.json and the per-pipeline DAG SVGs from the
staged workflow files.

For every cataloged pipeline:

  - runs `oxo-flow info` on its workflow file (main.oxoflow first, else the
    first root *.oxoflow, then workflow/*.oxoflow or *.toml) and stores the
    derived `config` records — the data behind each run-notes page's
    Parameters blocks;
  - renders the rule-level DAG with `oxo-flow graph -f metro` + nf-metro into
    docs/assets/dag/<name>.svg — the transit-map image behind each page's
    Workflow graph section.

Both outputs are committed, so site CI stays hermetic (no engine binary, no
network); regenerate locally whenever a staged workflow changes, then run
generate.py and commit everything.

Requirements: an oxo-flow binary ($OXO_FLOW, `oxo-flow` on PATH, or
../bin/oxo-flow) and nf-metro. The repo-local `.regen-venv/` (nf-metro
0.7.2, created once with `python3 -m venv .regen-venv && .regen-venv/bin/
pip install "nf-metro==0.7.2"`) is preferred: nf-metro >= 1.0 aborts on
dense graphs with CurveInvariantError (collinear overlays) where 0.7.2
renders them. The engine must be >= 0.16.0 for the metro export, and must
recognize every key the staged workflows use (workflows occasionally run
ahead of the released engine — such pipelines are skipped with a warning
so a partial regeneration never blocks the others).
Pipelines without a staged workflow file are skipped with a warning (their
pages simply omit the Parameters and Workflow graph sections).
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "pipelines.json"
OUT = ROOT / "data" / "configs.json"
DAG_DIR = ROOT / "docs" / "assets" / "dag"
STAGING = pathlib.Path.home() / "Documents" / "GitHub" / "oxo-community" / "staging"

# First engine version carrying both the config descriptions in `info`
# (v0.13.1, Traitome/oxo-flow#86) and the metro graph export (v0.16.0).
MIN_ENGINE = (0, 16, 0)


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


def engine_version(binary: str) -> tuple[int, int, int] | None:
    """`oxo-flow --version` → (major, minor, patch), or None when unparsable."""
    proc = subprocess.run([binary, "--version"], capture_output=True, text=True)
    m = re.search(r"oxo-flow (\d+)\.(\d+)\.(\d+)", proc.stdout)
    return tuple(map(int, m.groups())) if m else None


def require_engine(binary: str) -> None:
    """Fail loudly on engines too old to derive descriptions — a silent
    downgrade of the committed Parameters data is worse than an error."""
    version = engine_version(binary)
    if version is None or version < MIN_ENGINE:
        raise SystemExit(
            f"oxo-flow {'.'.join(map(str, version)) if version else 'unknown'} "
            f"is too old — regenerating requires >= {'.'.join(map(str, MIN_ENGINE))} "
            "(older binaries silently drop config descriptions)"
        )


def require_nf_metro() -> str:
    """Repo-local venv (pinned 0.7.2) first, then PATH — with a version guard:
    nf-metro >= 1.0 aborts on dense graphs (CurveInvariantError) that 0.7.2
    renders, so a 1.x on PATH without the venv is a hard error."""
    venv = ROOT / ".regen-venv" / "bin" / "nf-metro"
    if venv.is_file():
        return str(venv)
    found = shutil.which("nf-metro")
    if not found:
        raise SystemExit(
            "nf-metro not found — run once:\n"
            "  python3 -m venv .regen-venv\n"
            "  .regen-venv/bin/pip install \"nf-metro==0.7.2\""
        )
    proc = subprocess.run([found, "--version"], capture_output=True, text=True)
    m = re.search(r"version\s+(\d+)\.(\d+)", proc.stdout)
    if m and (int(m.group(1)), int(m.group(2))) >= (1, 0):
        raise SystemExit(
            f"nf-metro {m.group(1)}.{m.group(2)} aborts on dense graphs "
            "(CurveInvariantError) — install the pinned venv instead:\n"
            "  python3 -m venv .regen-venv\n"
            "  .regen-venv/bin/pip install \"nf-metro==0.7.2\""
        )
    return found


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


def derive(name: str, workflow: pathlib.Path, binary: str) -> tuple[list[dict] | None, str | None]:
    """`oxo-flow info` → config records; (None, reason) when the engine cannot
    parse the workflow (e.g. staged ahead of the released engine)."""
    proc = subprocess.run(
        [binary, "info", str(workflow)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        cause = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "unknown"
        return None, f"info failed: {cause}"
    meta = json.loads(proc.stdout)
    return meta.get("config", []), None


def render_dag(name: str, workflow: pathlib.Path, binary: str, nf_metro: str) -> str | None:
    """`oxo-flow graph -f metro` → nf-metro transit-map SVG, committed per pipeline.

    Returns None on success, or the failure reason — callers skip the
    pipeline with a warning so one broken workflow never blocks the rest.
    """
    svg = DAG_DIR / f"{name}.svg"
    with tempfile.TemporaryDirectory() as tmp:
        mmd = pathlib.Path(tmp) / f"{name}.mmd"
        graph = subprocess.run(
            [binary, "graph", "-f", "metro", "-o", str(mmd), str(workflow)],
            capture_output=True,
            text=True,
        )
        if graph.returncode != 0:
            cause = graph.stderr.strip().splitlines()[-1] if graph.stderr.strip() else "unknown"
            return f"graph failed: {cause}"
        render = subprocess.run(
            [nf_metro, "render", str(mmd), "-o", str(svg), "--theme", "light"],
            capture_output=True,
            text=True,
        )
        if render.returncode != 0:
            cause = render.stderr.strip().splitlines()[-1] if render.stderr.strip() else "unknown"
            return f"nf-metro failed: {cause}"
        # Light theme must not bake a dark `nf-metro-bg` rect (site issue #16).
        if "nf-metro-bg" in svg.read_text():
            return "nf-metro rendered a dark background — not light-theme clean"
    return None


def main() -> int:
    pipelines = json.loads(DATA.read_text())
    binary = engine_binary()
    require_engine(binary)
    nf_metro = require_nf_metro()
    DAG_DIR.mkdir(parents=True, exist_ok=True)
    # Start from the committed entries: pipelines skipped this run (engine
    # cannot parse their workflow yet) keep their last-known config data.
    configs = json.loads(OUT.read_text()) if OUT.is_file() else {}
    rendered = 0
    failures: list[str] = []
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
        # Info first — a workflow the engine cannot parse also cannot be
        # graphed; skip it with a warning and keep its committed artifacts.
        config, info_err = derive(name, workflow, binary)
        if info_err is not None:
            failures.append(f"{name}: {info_err}")
            print(f"warning: {failures[-1]} — Parameters + Workflow graph kept as-is",
                  file=sys.stderr)
            continue
        configs[name] = {
            "workflow": str(workflow.relative_to(STAGING / name)),
            "config": config,
        }
        dag_err = render_dag(name, workflow, binary, nf_metro)
        if dag_err is not None:
            failures.append(f"{name}: {dag_err} — DAG kept as-is")
            print(f"warning: {failures[-1]}", file=sys.stderr)
        else:
            rendered += 1
        for ew in p.get("extra_workflows") or []:
            wf_path = STAGING / name / ew["workflow"]
            if not wf_path.is_file():
                failures.append(f"{name}: extra workflow '{ew['workflow']}' missing in staging")
                print(f"warning: {failures[-1]}", file=sys.stderr)
                continue
            ew_err = render_dag(ew["dag"], wf_path, binary, nf_metro)
            if ew_err is not None:
                failures.append(f"{name}/{ew['dag']}: {ew_err} — DAG kept as-is")
                print(f"warning: {failures[-1]}", file=sys.stderr)
            else:
                rendered += 1
    OUT.write_text(json.dumps(configs, indent=2) + "\n")
    print(
        f"generated: {OUT.name} ({len(configs)}/{len(pipelines)} pipelines) "
        f"+ {rendered} DAG SVGs in {DAG_DIR.relative_to(ROOT)}/"
    )
    if failures:
        print(f"skipped {len(failures)} item(s) — kept their committed artifacts:",
              file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
