# Live testing — the community practice

This page codifies the practice developed while live-testing all 24
catalog workflows end-to-end on a real server with the oxo-flow CLI
(2026-08 campaign, 16 live-verified and counting). It is a **reference
paradigm**, not a policy: follow the checklist with or without an AI
assistant — the AI layer (the [`live-test` skill](https://github.com/oxo-flow-community/oxo-flow-community.github.io/blob/main/skills/live-test/SKILL.md))
just executes the same steps faster.

**Why live-test at all** — `dry-run` proves the graph parses and the
plan is schedulable; it does not prove tools run, environments resolve,
or outputs validate. Every workflow in the catalog must therefore pass
a full `oxo-flow run` against minimal real data before it earns the
*live-verified* rating. The practice below is the cheapest reliable way
to get there.

## The four principles

1. **Minimal data, maximal coverage** — at least 2 samples/pairs, tiny
   enough to finish in minutes, structured enough that every tool in
   the pipeline has real signal to compute (see [fixture design](#fixture-design)).
2. **One generator, three products** — genome, annotation and reads are
   emitted by a single deterministic script. Mixed-origin fixtures are
   the single most common live-test failure class.
3. **Never change semantics** — fixes tune resource labels, naming,
   isolation and environment pins; they never alter what the pipeline
   computes. Anything that needs user-scale data becomes a documented
   [gated contract](#gated-contracts), not a silent change.
4. **Evidence over guessing** — the checkpoint file is the source of
   truth for failures ([diagnosis](#diagnosis)); every fix commit cites
   the live error it addresses.

## Before you start

- **Group by difficulty.** Sort workflows: pure-conda before docker,
   single-sample before cohort, no-reference before reference-gated.
   Work the list easy → hard; never deadlock on one repository — park
   it and move on.
- **Right-size the machine.** 4 vCPU / 4 GB RAM runs every catalog
   workflow *except* the user-data-gated steps; that is deliberate — a
   small box exposes resource bugs a big one hides. Anything smaller
   than 2 GB starts failing for the wrong reasons.
- **Two lanes, strict.** Run at most 2 repositories concurrently.
   Beyond that, memory contention (conda solver + R + JVM peaks) kills
   unrelated runs and wastes the whole queue. The harness scripts
   enforce this with file locks.
- **Mirror neutrality.** A workflow repository must work against both
   international sources and CN mirrors — pins go in the repo, mirror
   choice goes in the environment. Test-environment proxy or mirror
   configuration must **never** be committed to a workflow repository.

## Fixture design

The pattern that works (one `test/fixtures/generate_fixtures.py` per
workflow, fixed seed, committed alongside the generated files):

- **Reads are derived from the shipped genome** — drawn from feature
  regions so alignment, quantification and annotation steps all see
  signal; ~0.5 % substitution error; Phred-30+ qualities.
- **The annotation is self-consistent** — unique transcript ids, exons
  inside transcript bounds, `gene_id` matching the gene feature. Tools
  like gffutils/RSeQC hard-fail on reused ids across loci
  (`End of last exon (2000) does not match end of feature (500)`).
- **Tool-shaped signal, added on demand** — preseq needs a duplicate
  count curve (≥4 multiplicity levels); DamageProfiler needs per-position
  depth above its `-t` threshold; DADA2 needs amplicon template
  structure; circRNA callers need back-splice junctions; DESeq2 needs a
  two-condition signal. Add each only when a tool demands it, and note
  why in the generator docstring.
- **Read-name contracts** — `/1` `/2` mate suffixes (AdapterRemoval v2
  rejects files without them); duplicate tags *before* the suffix
  (`@read_dup1/1`, never `@read/1_dup1` — bwa mem pairs by name after
  stripping the trailing `/1` or `/2`).
- **Paired-end arithmetic** — inserts sized so mergers (AdapterRemoval)
  can overlap; spliced reads assemble exon segments along the
  transcription direction.
- **Regeneration is idempotent** — the generator overwrites its
  outputs; one-shot post-processors (e.g. adding duplicates) must start
  from the pristine fixtures (`git checkout` the base first), or they
  stack tags on tags.

## Resource adaptation

The engine gives every rule two pairs of placeholders — `{threads}` /
`{memory}` (the declaration, pool semantics) and `{effective_threads}`
/ `{effective_memory_mb}` (the machine-clamped reality). Rules that
embed resource-sized flags use the effective pair:

- `bwa -t {effective_threads}`, `samtools sort --threads {effective_threads} -m 512M`
  (samtools' default 768 MB/thread over-allocates and dies with
  `couldn't allocate memory for bam_mem` on small boxes);
- `-Xmx{effective_memory_mb}m` for JVM tools instead of HPC-scale
  hardcodes;
- container `--memory` is clamped to the machine by the engine itself
  (a `72G` label runs as `--memory 4G` on a 4 GB box — cgroup-aware
  tools like Cell Ranger see an honest limit);
- **the machine ceiling counts swap** — RAM + swap is the backable
  budget the kernel will actually use under pressure; pass
  `--max-memory` to pin it to RAM only when latency matters more than
  headroom.

These are the semantics-preserving fixes: the workflow still declares
its upstream labels, only the *tool-facing* numbers adapt.

## Gated contracts

Some pipelines legitimately require data no repository can ship.
Instead of failing or faking, the port documents a **gated contract**:

- the gate is an explicit config switch (e.g. `run_gtdbtk = false`,
  `annotate_vep = false`, `skip_ref_downloads = true`);
- the README states exactly which rules the gate covers and what the
  user must provide to lift it (GTDB-Tk's ~100 GB database, a VEP
  cache, a GRCh38 bundle…);
- the live test runs with the gate closed, and the catalog entry's
  `quickstart_note` says so honestly.

Gated steps are verified separately (command construction, environment
resolution) and rated below live-verified — see the
[curation ladder](curation.md).

## Execution & monitoring

The `scripts/live-test/` harness (documented in the [skill
reference](https://github.com/oxo-flow-community/oxo-flow-community.github.io/blob/main/skills/live-test/references/harness-scripts.md)) runs
the queue:

- **2 lanes** via `flock` on two lock files — blocked runners form a
  FIFO; only two repositories execute at any moment.
- **Resume-aware requeues** — a runner keeps `.oxo-flow` when the
  workflow files are unchanged (the engine's input manifests then
  invalidate exactly the affected rules); a changed workflow wipes and
  restarts.
- **A supervisor** parks repositories that stall (>30 min without rule
  activity) or fail three times with the same signature — parked repos
  stay out until a fix lands.
- **Verdicts** are the `run end: exit=N` lines; exit 0 is the only
  pass. On success the engine also writes
  `.oxo-flow/reports/report-*.json` — the reference snapshot for
  reviewers.

Run the supervisor and a disk watchdog from cron on the test server —
after reboots, crontabs vanish and the queue degrades silently.

## Diagnosis

When a run fails, read the **checkpoint**, not the log tail:

```bash
python3 - <<'EOF'
import json
d = json.load(open(".oxo-flow/checkpoint.json"))
print("failed:", d["failed_rules"])
for k, v in d["rule_runs"].items():
    if v.get("exit_code") not in (0, "0") and v.get("exit_code") is not None:
        print(k, "|", v.get("exit_code"), "|", str(v.get("stderr_tail", ""))[-400:])
EOF
```

Two traps the campaign hit repeatedly:

- **The visible ✗ is not the failure.** The engine aborts fast and the
  last scheduled rule's WARN lines sit right before the generic
  `workflow execution failed` — the *real* failing rule is in
  `failed_rules`, its stderr in `rule_runs`.
- **`Shell exited 0 but declared outputs are missing`** means the tool
  wrote somewhere else (cwd quirks, `%`-placeholder naming, stale
  state) — locate the actual artifacts before touching the shell.

Recurring failure classes, each with its live symptom, root cause and
fix pattern, live in the [failure catalog](https://github.com/oxo-flow-community/oxo-flow-community.github.io/blob/main/skills/live-test/references/failure-catalog.md)
— consult it before debugging from scratch.

## Fix discipline

1. One commit per fix, body citing the live evidence
   (`Live: 'sort: invalid option -- F' from the pinned image's samtools…`).
2. Push, sync the test server, requeue — and verify the *fixed* tree
   actually ran (server trees drift: stale checkouts, partial syncs,
   mirrors lagging on branch refs).
3. Update the docs the fix affects in the same change.
4. A second reviewer diffs and merges; live-verified evidence is
   stamped only against the exact tree that passed.
5. Record every new failure class in the [failure catalog](https://github.com/oxo-flow-community/oxo-flow-community.github.io/blob/main/skills/live-test/references/failure-catalog.md)
   — that file *is* the accumulating institutional memory this page
   promises. Update it as part of the fix that discovered the class.

## With or without AI

- **Without AI**: follow the checklists above literally; the harness
  scripts run the queue for you; the failure catalog short-circuits
  most debugging.
- **With AI (Claude Code)**: install the
  [`live-test` skill](https://github.com/oxo-flow-community/oxo-flow-community.github.io/blob/main/skills/live-test/SKILL.md) (`/live-test`),
  point it at a server and a batch of repositories; it executes the
  same loop — group, fixture-check, run, diagnose via checkpoint, fix,
  archive the finding — with the campaign scripts and catalog as its
  reference.

Either way, the acceptance bar is the same: **every catalog workflow
runs end-to-end via the CLI on real minimal data, or it is honestly
documented as gated.**
