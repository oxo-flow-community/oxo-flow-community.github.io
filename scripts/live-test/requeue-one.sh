#!/bin/bash
# requeue-one.sh <repo-dir-name> [workflow-file] [config overrides...]
# Kill every existing wf-run entry for the repo, then launch exactly one.
#
# RESUME mode: when the workflow file's content is unchanged since the
# previous launch, keep .oxo-flow (checkpoint) so the retry resumes;
# a changed workflow wipes state. NOTE: this hashes the main workflow
# file only — if an INCLUDED module changed but the main file did not,
# force a clean restart by deleting .oxo-flow and results first.
set -u
REPO="$1"; shift
WF="${1:-main.oxoflow}"; shift || true
REPOS_ROOT="${REPOS_ROOT:-$HOME/community-runs/repos}"
RUNS_ROOT="${RUNS_ROOT:-$HOME/community-runs}"
cd "$REPOS_ROOT/$REPO" || exit 1

for p in $(pgrep -f "^bash .*wf-run.sh"); do
  cwd=$(readlink "/proc/$p/cwd" 2>/dev/null)
  case "$cwd" in *"/$REPO") kill "$p" 2>/dev/null;; esac
done
for p in $(pgrep -f "flock.*oxo-run.*lock"); do
  cwd=$(readlink "/proc/$p/cwd" 2>/dev/null)
  case "$cwd" in *"/$REPO") kill "$p" 2>/dev/null;; esac
done
sleep 1
NOW=$(sha256sum "$WF" 2>/dev/null | cut -d' ' -f1)
PREV=""
[ -f .oxo-flow/workflow_hash ] && PREV=$(cat .oxo-flow/workflow_hash)
if [ -n "$NOW" ] && [ "$PREV" = "$NOW" ]; then
  RESUME=1
else
  RESUME=0
  rm -rf .oxo-flow results
fi
mkdir -p .oxo-flow
echo "$NOW" > .oxo-flow/workflow_hash
setsid nohup bash "$(dirname "$0")/wf-run.sh" "$WF" -j 2 "$@" > /dev/null 2>&1 < /dev/null &
echo "requeued one: $REPO ($WF) resume=$RESUME"
