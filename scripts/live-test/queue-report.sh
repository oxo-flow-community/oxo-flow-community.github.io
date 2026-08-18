#!/bin/bash
# queue-report.sh — one-screen snapshot of the live-test queue.
#
# Columns per repository: latest verdict (or RUNNING), the last rule
# activity line, and the parked flag. Run manually or from cron; the
# output is also the shape the AI-side monitor polls.
RUNS_ROOT="${RUNS_ROOT:-$HOME/community-runs}"
PARK="${PARK_FILE:-/tmp/parked.txt}"
touch "$PARK" 2>/dev/null

echo "== queue report $(date -Is) =="
for repo in $(ls "$RUNS_ROOT/repos/" 2>/dev/null | sort); do
  LOG="$RUNS_ROOT/logs/$repo.log"
  [ -f "$LOG" ] || { echo "$repo: no log yet"; continue; }
  LAST=$(grep "run end: exit=" "$LOG" | tail -1 | grep -o "exit=[0-9]*")
  RUNNING=$(pgrep -f "^bash .*wf-run.sh" | while read p; do readlink /proc/$p/cwd 2>/dev/null; done | grep -c "/$repo$")
  PARKED=$(grep -qx "$repo" "$PARK" 2>/dev/null && echo " PARKED" || true)
  if [ "$RUNNING" -gt 0 ]; then
    ACT=$(grep -E "Running: " "$LOG" | tail -1 | cut -c1-60)
    echo "$repo: RUNNING [$ACT]$PARKED"
  else
    echo "$repo: $LAST$PARKED"
  fi
done
echo "== mem: $(free -m | awk 'NR==2{print $3"/"$2"MB, "$7" avail"}') | disk /data: $(df -h /data 2>/dev/null | tail -1 | awk '{print $4" free"}') =="
exit 0
