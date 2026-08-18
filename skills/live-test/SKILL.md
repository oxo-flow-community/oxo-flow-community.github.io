---
name: live-test
description: >-
  Live-test oxo-flow workflows end-to-end on a real server: group repositories
  by difficulty, verify/design minimal fixtures, run via the CLI harness,
  diagnose failures from the checkpoint, fix semantics-preservingly, and
  archive findings. Use for any campaign that must prove workflows actually
  run (not just dry-run) — port verification, release hardening, community
  catalog stamping.
---

# oxo-flow live-testing

Execute the community live-testing practice
([docs/about/live-testing.md](../../../docs/about/live-testing.md)) on a
batch of workflow repositories. The doc is the methodology — this skill
is the operational loop.

## Phase 0 — Scope

1. Inventory the repositories; clone each to a fixed layout
   (`repos-oxo-flow-<name>` next to this repo's worktree).
2. Classify: conda-only vs docker, single-sample vs cohort,
   reference-gated vs self-contained. Order easy → hard.
3. Server requirements: 4 vCPU / 4 GB RAM minimum, docker + conda,
   ≥ 20 GB free disk. At most **2 repositories concurrently** — the
   constraint is memory, not CPU.

## Phase 1 — Fixtures

For each repository: `validate` + `dry-run` first. Then decide which
of the three fixture states it is in:

- **coherent** — reads map to the shipped reference (spot-check: grep
  read windows against the genome in the generator's own terms);
- **incoherent** — reads/reference/annotation from different sources
  (the #1 failure class) → write/extend
  `test/fixtures/generate_fixtures.py` (deterministic seed, one script
  emitting genome+GTF+reads, tool-shaped signal per the doc);
- **gated** — needs user-scale data → close the documented gate
  (`run_gtdbtk=false` style) and record the contract in README +
  `quickstart_note`.

## Phase 2 — Run

1. Ship the harness: `scripts/live-test/` (wf-run, requeue-one,
   lane-supervisor, disk-watchdog, queue-report) — read
   `references/harness-scripts.md` for their contracts.
2. Install cron entries for supervisor (every 5 min) and disk watchdog
   (every 10 min). **After any server reboot, re-check the crontab.**
3. Requeue repos in difficulty order: `requeue-one.sh <repo> <wf> [-j 2] [overrides…]`.
   Pass gated-contract overrides explicitly every time.
4. Watch for `run end: exit=N` verdicts. exit=0 is the only pass.

## Phase 3 — Diagnose (per failure)

1. Read the checkpoint — never the log tail:
   `failed_rules` names the real failure; `rule_runs[<rule>].stderr_tail`
   carries the evidence (the visible ✗ line is often a decoy — see the
   doc's diagnosis traps).
2. Classify against `references/failure-catalog.md` before new
   debugging; the catalog entry gives the fix pattern.
3. Fix in the repository (never the server): semantics-preserving,
   one commit per fix, `Live: …` evidence in the body.
4. Push → sync the server tree (verify the commit actually landed —
   mirrors lag, partial syncs silently ship stale files) → requeue.
5. Environment-level failures (conda solve OOM, mirror lag): prefer
   background env pre-creation with retries, wrapped in the engine's
   env-create flock (`~/.oxo-flow/env-create.lock`) so it never
   collides with in-workflow setup.

## Phase 4 — Verify & archive

1. A repository passes only when a clean run exits 0 end-to-end;
   capture the report JSON as evidence.
2. Hand the merge-ready list (branch, tip, commit subjects) to a
   second reviewer; live-verified stamps attach to the exact tree that
   passed.
3. **Archive**: add every newly discovered failure class to
   `references/failure-catalog.md` in the same change as its fix; note
   any engine-level gaps as issues on `Traitome/oxo-flow`.

## Rules

- Never commit test-environment mirror/proxy configuration to a
  workflow repository (mirror neutrality — repo pins, environment
  mirrors).
- Never change pipeline semantics to make a test pass; gate it and
  document the gate instead.
- Park, don't deadlock: three same-signature failures or 30-minute
  stalls mean the repository waits for an off-lane fix.
- Keep the server honest: monitor memory/disk/load; the disk watchdog
  prunes dangling images only — never images pinned by queued rules.

See also: `references/harness-scripts.md`, `references/failure-catalog.md`,
and the methodology doc the skill instantiates.
