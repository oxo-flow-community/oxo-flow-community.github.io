# Harness scripts

`scripts/live-test/` — the queue-and-triage machinery for running a
batch of workflows on a shared server. All paths derive from env vars:
`RUNS_ROOT` (default `~/community-runs`, holds `logs/` and the lock
files), `REPOS_ROOT` (default `$RUNS_ROOT/repos`), and `OXO_PATH_PREPEND`
(the dirs `wf-run.sh` prepends to PATH for the CLI and conda; default
`~/.cargo/bin:~/.miniforge3/bin` — override for other server layouts).
No mirror or proxy configuration lives here.

| Script | Role | Invocation |
|---|---|---|
| `wf-run.sh` | one workflow through the CLI under a 2-lane `flock`; appends `run start` / `run end: exit=N` verdicts to `$RUNS_ROOT/logs/<repo>.log` | launched by requeue-one; or `bash wf-run.sh main.oxoflow -j 2 [overrides…]` from the repo dir |
| `requeue-one.sh` | kill the repo's runners, relaunch one; resume-aware via `.oxo-flow/workflow_hash` | `bash requeue-one.sh <repo> [wf] [overrides…]` |
| `lane-supervisor.sh` | parks stalled (30 min silent) or 3×same-signature-failing repos | cron every 5 min |
| `disk-watchdog.sh` | prunes dangling docker images only; reports fullness | cron every 10 min |
| `queue-report.sh` | one-screen queue snapshot | manual / cron |
| `diagnose-checkpoint.py` | authoritative failure report from `checkpoint.json` | `python3 diagnose-checkpoint.py [repo]` |

## Contracts

- **Verdicts**: `grep "run end: exit=" $RUNS_ROOT/logs/<repo>.log | tail -1`.
  exit 0 is the only pass; the engine additionally writes
  `.oxo-flow/reports/report-*.json` on success — that is the review
  artifact.
- **Lanes**: `cksum(repo) % 2` picks the lock file; runners block on
  `flock`, so the queue is a FIFO and at most 2 repositories execute
  at once. Do not raise the lane count on small-memory boxes — the
  binding constraint is RAM, not CPU.
- **Resume**: `requeue-one.sh` keeps `.oxo-flow` when the *main*
  workflow file is unchanged; the engine's input manifests then
  invalidate exactly the affected rules. If an included module changed
  but the main file did not, `rm -rf .oxo-flow results` first — the
  hash covers the main file only.
- **Parking**: parked repos (in `$PARK_FILE`, default `/tmp/parked.txt`)
  are skipped by the supervisor; a fix followed by `requeue-one.sh`
  clears the entry.
- **Reboot amnesia**: crontabs do not survive reboots. Bring-up
  checklist: re-add the supervisor (5 min) and watchdog (10 min)
  entries, verify the disk layout (containerd store location), and
  confirm `~/.oxo-flow/env-create.lock` exists.
- **Env pre-creation**: for heavy environments, pre-create in the
  background with retries at `nice 19`, wrapped in
  `flock ~/.oxo-flow/env-create.lock` — the engine's own cross-process
  env mutex — so a manual create can never collide with an
  in-workflow setup of the same environment.

## Server sync discipline

Git transport from the test server is often broken (firewalls,
mirrors lagging on branch refs). The reliable patterns, in order:

1. server-side `git fetch <direct-url>` when reachable, with a tree
   guard (checksum the fixed file before building/requeueing);
2. `git archive <sha>` locally → `scp` → extract over the server tree
   (bulk tree syncs cannot delete untracked stale files — delete
   rebuilt artifacts explicitly, e.g. STAR indexes);
3. never trust "pushed" == "server has it": verify the sentinel before
   requeueing.

## Server sizing notes (from the 2026-08 campaign)

- 4 vCPU / 3.7 GB RAM + 6 GB swap runs every catalog workflow except
  user-data-gated steps; 2 lanes is the right concurrency.
- Docker images on a 20 GB data disk via a containerd-store symlink;
  ~19 GB free after pruning suffices for the biggest pulls (Cell
  Ranger ~5 GB).
- Paid registry mirrors make image re-pulls cheap — prune aggressively
  rather than hoarding pinned images.
