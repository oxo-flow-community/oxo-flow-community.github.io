#!/bin/bash
# lane-supervisor.sh — keep the 2-lane queue flowing (run every 5 min via cron).
#
# Rules:
# 1. A repo whose run produced NO new rule-activity line for 30 min
#    (stalled on network/I-O) gets evicted and PARKED.
# 2. A repo with >=3 consecutive failures carrying the same error
#    signature gets PARKED (needs an off-lane fix, not retries).
# 3. Parked repos are never requeued by the supervisor; they stay out
#    until a fix lands (then requeue-one clears the parking).
# 4. Everything is logged to $RUNS_ROOT/supervisor.log.
#
# IMPORTANT: cron entries do not survive server reboots — re-check
# `crontab -l` as part of bring-up.
PARK="${PARK_FILE:-/tmp/parked.txt}"
RUNS_ROOT="${RUNS_ROOT:-$HOME/community-runs}"
touch "$PARK"

log() { echo "$(date -Is) $*" >> "$RUNS_ROOT/supervisor.log"; }

for repo in $(ls "$RUNS_ROOT/repos/" | sort -u); do
  [ -f "$RUNS_ROOT/repos/$repo" ] && continue
  grep -qx "$repo" "$PARK" && continue

  LOG="$RUNS_ROOT/logs/$repo.log"
  [ -f "$LOG" ] || continue
  RUNNING=$(pgrep -f "^bash .*wf-run.sh" | while read p; do readlink /proc/$p/cwd 2>/dev/null; done | grep -c "/$repo$")

  # --- failure signature: last 3 run-end lines of this log ---
  LAST3=$(grep "run end: exit=" "$LOG" | tail -3 | grep -o "exit=[0-9]*" | tr '\n' ' ')
  FAILS=$(echo "$LAST3" | grep -o "exit=1" | wc -l)
  if [ "$FAILS" -ge 3 ]; then
    SIG=$(grep -B6 "run end: exit=1" "$LOG" | grep -oE "(Error in [^:]+|syntax error[^:]*|NoSpaceLeft|PackagesNotFound|invalid option[^:]*|Could not create[^:]*|Error matrix is NULL|Cannot find assay [A-Za-z]+)" | tail -3 | sort -u | tr '\n' '|')
    PREV=$(grep "^$repo " "$RUNS_ROOT/parked-sig.txt" 2>/dev/null | cut -d' ' -f2-)
    if [ "$RUNNING" -gt 0 ] && [ -n "$SIG" ] && [ "$SIG" = "$PREV" ]; then
      log "PARK $repo — 3 consecutive failures, same signature: $SIG"
      echo "$repo" >> "$PARK"
      for p in $(pgrep -f "^bash .*wf-run.sh"); do
        cwd=$(readlink "/proc/$p/cwd" 2>/dev/null)
        case "$cwd" in *"/$repo") kill "$p" 2>/dev/null;; esac
      done
    fi
    echo "$repo $SIG" >> "$RUNS_ROOT/parked-sig.txt"
    continue
  fi

  # --- stall: no rule activity in 30 min while the run is live ---
  if [ "$RUNNING" -gt 0 ]; then
    LAST_ACT=$(grep -E "Running: |✓ rule|✗ rule" "$LOG" | tail -1 | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z?" | head -1 | sed "s/Z$//")
    if [ -n "$LAST_ACT" ]; then
      AGE=$(( $(date +%s) - $(date -d "$LAST_ACT" +%s 2>/dev/null || echo 0) ))
      if [ "$AGE" -gt 1800 ] && [ "$AGE" -lt 86400 ]; then
        log "PARK $repo — stalled $AGE s (last activity $LAST_ACT)"
        echo "$repo" >> "$PARK"
        for p in $(pgrep -f "^bash .*wf-run.sh"); do
          cwd=$(readlink "/proc/$p/cwd" 2>/dev/null)
          case "$cwd" in *"/$repo") kill "$p" 2>/dev/null;; esac
        done
      fi
    fi
  fi
done
exit 0
