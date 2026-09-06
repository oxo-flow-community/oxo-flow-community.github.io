#!/bin/zsh
# One-shot regeneration of every pipeline artifact the site carries:
#   data/configs.json   — parameters, used_by, tier info (regen-configs.py)
#   docs/assets/dag/*.svg — nf-metro transit maps (render ladder)
#   docs/pipelines/*.md — per-pipeline pages (generate.py)
#
# Requirements:
#   - an oxo-flow binary >= 0.17.3 (module granularity): $OXO_FLOW, PATH, or ../bin/oxo-flow
#   - nf-metro 1.1.0: the repo-local .regen-venv (preferred) or PATH
#
# Usage:
#   OXO_FLOW=/path/to/oxo-flow ./scripts/regen-all.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== engine =="
BIN="${OXO_FLOW:-$(command -v oxo-flow || echo ../bin/oxo-flow)}"
"$BIN" --version | head -1

echo "== nf-metro =="
if [ ! -x .regen-venv/bin/nf-metro ]; then
  echo "creating .regen-venv with nf-metro 1.1.0 ..."
  python3 -m venv .regen-venv
  .regen-venv/bin/pip install --quiet --index-url https://pypi.org/simple "nf-metro==1.1.0"
fi
.regen-venv/bin/nf-metro --version | head -1

echo "== regen-configs (parameters + DAG SVGs) =="
OXO_FLOW="$BIN" python3 scripts/regen-configs.py

echo "== generate (pipeline pages) =="
python3 scripts/generate.py

echo "== done — review git diff, then commit both scripts and generated files =="
