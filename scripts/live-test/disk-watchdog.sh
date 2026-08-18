#!/bin/bash
# disk-watchdog.sh — keep the test server's disk usable (run every 10 min via cron).
#
# Policy: prune DANGLING docker images only. Never `image prune -a`:
# queued repositories re-pull their pinned images on demand, and an
# aggressive prune costs the queue minutes per repo (and can delete an
# image a lane needs mid-run). Conda envs are never reclaimed here —
# a deleted env costs a full re-solve (OOM risk on small boxes).
set -u
LOG="${LOG_FILE:-/tmp/disk-watchdog.log}"
log() { echo "$(date -Is) $*" >> "$LOG"; }

docker image prune -f > /dev/null 2>&1
ROOT_USE=$(df / | tail -1 | awk '{print $5}')
DATA_USE=$(df /data 2>/dev/null | tail -1 | awk '{print $5}')
log "pruned dangling; root=$ROOT_USE data=${DATA_USE:-n/a}"

# Only escalate when the root filesystem is truly full (never silently
# delete user data — reference bundles, results).
if [ "${ROOT_USE%\%}" -gt 95 ] 2>/dev/null; then
  log "WARN root >95% full — manual intervention needed"
fi
exit 0
