#!/bin/bash
# wf-run.sh <workflow-file> [engine args...]
# Runs one workflow through the oxo-flow CLI under a two-lane file lock,
# appending a "run start"/"run end: exit=N" verdict pair to the repo log.
#
# Lanes: each repository hashes to lane 0 or 1 (cksum % 2); runners wait
# on flock, so a long queue forms a FIFO and at most 2 repos execute at
# once. Memory (not CPU) is the constraint on 4 GB boxes — do not raise
# the lane count casually.
#
# Env: OXO_BIN (default: oxo-flow on PATH), RUNS_ROOT (default:
# ~/community-runs) — logs land in $RUNS_ROOT/logs/<repo>.log.
set -u
WF_BASE="${1:-main.oxoflow}"; shift || true
REPO_NAME=$(basename "$PWD")
RUNS_ROOT="${RUNS_ROOT:-$HOME/community-runs}"
OXO="${OXO_BIN:-oxo-flow}"
LOGDIR="$RUNS_ROOT/logs"
mkdir -p "$LOGDIR"
LOG="$LOGDIR/$REPO_NAME.log"
echo "=== $(date -Is) run start: $WF_BASE $* ===" | tee -a "$LOG"
LANE=$(echo "$REPO_NAME" | cksum | awk '{print $1 % 2}')
if [ "$LANE" = "0" ]; then LOCK="$RUNS_ROOT/oxo-run.lock"; else LOCK="$RUNS_ROOT/oxo-run2.lock"; fi
flock --close "$LOCK" bash -c 'export PATH="$HOME/.cargo/bin:$HOME/miniforge3/bin:$PATH"; '"$OXO"' run "$0" "$@" 2>&1' "$WF_BASE" "$@" | tee -a "$LOG"
RC=${PIPESTATUS[0]:-1}
echo "=== $(date -Is) run end: exit=$RC ===" | tee -a "$LOG"
