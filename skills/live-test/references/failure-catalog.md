# Failure catalog

Every entry: live symptom → root cause → fix pattern, with a real
example commit. Distilled from the 2026-08 campaign (24 workflows,
100+ individual failures). **Append new classes here as part of the
fix that discovered them** — this file is the institutional memory.

## Fixture incoherence

**Symptom**: alignment/quantification yields zero (STAR `0 alignments`,
salmon `was only able to assign 0 fragments`, DamageProfiler `No reads
processed. Can't create any output`).
**Root cause**: reads were not generated from the shipped genome, or
annotation/reads come from different sources.
**Fix**: one deterministic `generate_fixtures.py` emitting
genome+GTF+reads from one seed; reads drawn from feature regions.
*Example*: rnaseq-star-deseq2 `b381a15`.

**Symptom**: RSeQC/gffutils `End of last exon (N) does not match end
of feature (M)`.
**Root cause**: GTF reuses transcript ids across loci or exons escape
transcript bounds (hand-edited GTF).
**Fix**: regenerate the GTF structurally — unique ids, exon-bounded
transcripts, consistent `gene_id`.
*Example*: same commit as above.

**Symptom**: preseq `max count before zero is less than min required
count (4) duplicates removed`.
**Root cause**: fixtures have no duplicate structure — the duplicate
count curve is empty.
**Fix**: duplicate ~25-30 % of pairs at 2×/4×/8×/16× multiplicity.
*Example*: chipseq `f5e4c5c`.

**Symptom**: DamageProfiler writes only `DamageProfiler.log`, exit 0.
**Root cause**: read depth per reference position below the `-t`
threshold (e.g. 4-read fixtures).
**Fix**: concentrate reads on ~40 source positions at ≥50× depth.
*Example*: eager `709111c`.

**Symptom**: DADA2 `Error matrix is NULL`.
**Root cause**: random-sequence reads — no amplicon template
structure for learnErrors.
**Fix**: templates × reads-per-template with PCR-style errors.
*Example*: ampliseq `generate_fixtures.py`.

## Read-name contracts

**Symptom**: bwa mem `paired reads have different names: X/1_d3,
X/2_d3`.
**Root cause**: duplicate/suffix tags appended *after* the `/1` `/2`
mate suffix; bwa pairs by name after stripping only a trailing suffix.
**Fix**: insert tags before the final two characters.
*Example*: chipseq `eef4c39`.

**Symptom**: AdapterRemoval v2 `Error reading FASTQ record at line 1;
aborting` on valid files.
**Root cause**: read ids lack `/1` `/2` mate identifiers.
**Fix**: always emit the suffixes.
*Example*: eager `4f95070`.

## Stale state / isolation

**Symptom**: Cell Ranger exits instantly with no outputs; stale `_lock`
in the pipeline dir from a crashed attempt.
**Root cause**: oxo-flow runs every rule in the shared workdir (no
Nextflow-style per-task dir); tools that refuse to run in a dirty dir
need the shell to clean their state first.
**Fix**: `rm -rf` the tool's pipeline/output dirs at the top of the
shell (fresh-dir semantics preserved).
*Example*: scrnaseq `e073c09`.

**Symptom**: `mv: cannot stat X_1.unmapped.fastq.gz` after bowtie2
`--un-conc-gz X.unmapped_%.fastq.gz`.
**Root cause**: `%`-placeholder naming — the mate index lands where
the `%` sits, not where the mv expects.
**Fix**: put `%` immediately before the extension, or match the mv
and declared outputs to the actual names.
*Example*: mag `e4826cc`.

**Symptom**: rules reading `{config.path}` inputs in the shell but
declaring no `input` re-use stale copies after the source changes.
**Root cause**: the checkpoint's input manifests only track declared
inputs — config-driven reads are invisible to invalidation.
**Fix**: declare the config source as an `input` (empty for the
download branch; the shell's if/else handles both).
*Example*: rnaseq-star-deseq2 `d09f6cc`.

**Symptom**: stale binary index files outliving a fixture swap (bulk
tar syncs overwrite tracked files but cannot delete untracked stale
ones).
**Root cause**: partial syncs — a README placeholder is not an index.
**Fix**: delete + rebuild artifacts from the current fixtures; verify
the served tree matches the pushed commit.

## Tool quirks

**Symptom**: fastqc zip lands next to the input despite `cd` + `mv`
failing with `cannot stat`.
**Root cause**: the container image's fastqc writes beside the INPUT
by default (patched builds).
**Fix**: explicit `-o .`.
*Example*: eager `af82465` (raw) + the after-clipping instance.

**Symptom**: CIRCexplorer2 annotate `not enough values to unpack
(expected 4, got 3)`.
**Root cause**: its ref file needs `gene_id iso_id chrom strand`, not
`chrom start end`.
**Fix**: emit the 4-column ref from the GTF in the generator.
*Example*: circrna `1a6cd83`.

**Symptom**: kraken2 `malformed taxonomy file taxo.k2d`.
**Root cause**: the shipped DB tarball was a stub.
**Fix**: build a real minimal DB offline (hand-written
`nodes.dmp`/`names.dmp`/`seqid2taxid.map` over the fixture genome) and
commit it with a build script.
*Example*: viralrecon `3edee4d`.

**Symptom**: ~9800 treatment reads shrink to 19 after a
`samtools view -L blacklist.bed | bamtools filter` pipeline; macs3
reports 2 treatment fragments, calls zero peaks, and the whole
downstream chain fails on empty inputs (`mergeBed` "Requested column
2, but database file - only has fields 1 - 0").
**Root cause**: `samtools view -L` is a *target-file selector* — it
KEEPS only blacklist-overlapping reads, the inverse of the intended
blacklist removal.
**Fix**: exclude with the `-L … -U out.bam` pair (stdout gets the
blacklist reads, `-U` writes the pass reads); feed the file to the
next tool with `-in`. Give per-instance temp names (`{pair_id}`)
because fan-out instances share the workdir.
*Example*: chipseq `6bd7141`.

## Resource over-allocation

**Symptom**: `samtools sort: couldn't allocate memory for bam_mem`.
**Root cause**: default 768 MB/thread × the upstream thread label
(e.g. 24) ≫ machine RAM.
**Fix**: `--threads {effective_threads} -m 512M` (and
`-t {effective_threads}` on the upstream tool).
*Examples*: sarek `3a1a897`, nanoseq `47d9aa5`.

**Symptom**: container tools see absurd cgroup limits (`--memory 72G`
on a 4 GB box), Cell Ranger's job manager reports machine-check
numbers the kernel cannot back.
**Root cause**: the engine passed declared memory straight to the
container.
**Fix (engine)**: container `--memory` is clamped to the machine
total (same policy as the pool clamp). *Engine*: `Traitome/oxo-flow`
`7738e6e`.

**Symptom**: Cell Ranger mkref waits forever on `Need 16 GB`.
**Root cause**: jobmngr's per-job memory scales with `--localmem` —
the gate is real but tunable.
**Fix**: `--localmem $(({effective_memory_mb} / 1024))`; the "16 GB"
gate drops to a machine-sized "Need 3 GB".

## Environment provisioning

**Symptom**: `PackagesNotFoundError` for a pinned package even on the
main channel.
**Root cause**: the package was removed from bioconda (upstream pins
it too — dead dependency for everyone).
**Fix**: install from the official source tag via pip
(`git+https://…@vX.Y.Z`) + build toolchain in the yaml.
*Example*: tcasia `c4c8179` (spladder).

**Symptom**: env setup re-resolves and fails on flaky mirrors even
though the env is fully installed.
**Root cause**: cold env cache → setup's `conda env update --prune`
fallback runs unconditionally.
**Fix (engine)**: verify existing envs in place before setup.
*Engine*: `Traitome/oxo-flow` `48b725b`.

**Symptom**: `setup failed: Killed` during a rule's env creation.
**Root cause**: conda solver memory peak colliding with running lanes
(4 GB boxes).
**Fix**: pre-create envs in the background with retries at nice 19,
wrapped in `flock ~/.oxo-flow/env-create.lock` (the engine's own
cross-process mutex) so it can never collide with in-workflow setup.

**Symptom**: post-link script failures / SSL 77 during env creation.
**Root cause**: post-link downloads happen before the new env's CA
bundle is linked (engine now exports the base CA for setup).
**Fix**: engine-side CA export; workflow-side: nothing.

## Infrastructure / queue

**Symptom**: everything fails with `No space left on device` /
`cannot create ./.oxo-flow`.
**Root cause**: docker store + reference downloads filled the disk.
**Fix**: prune unused images (re-pulls are cheap on a paid mirror),
relocate the containerd store to a data disk, watchdog cron that
prunes dangling only (never images pinned by queued rules).

**Symptom**: three unrelated runs die within seconds of each other
with no ✗ lines.
**Root cause**: fail-fast cascade — one repo's real failure aborts
its siblings; the ✗ of the *visible* repo is a decoy.
**Fix**: read every checkpoint's `failed_rules` before concluding.

**Symptom**: the queue silently degrades — no parking, no pruning.
**Root cause**: cron entries (supervisor/watchdog) vanish on reboot.
**Fix**: re-check crontab after every reboot; treat it as part of
server bring-up.

**Symptom**: pkill/pgrep commands kill the SSH session itself
(exit 255).
**Root cause**: `-f` patterns match the invoking shell's own command
line.
**Fix**: bracket-trick patterns (`mix-rep[r]o`) or PID-file-based
kills.

**Symptom**: a repository's rerun uses an old workflow despite a
pushed fix.
**Root cause**: server trees drift — mirrors serve stale branch refs,
partial scp syncs, bulk tar syncs that cannot delete untracked files.
**Fix**: verify the tree against the commit before requeueing
(checksum a sentinel file); sync full trees via archive+scp when git
transport is blocked.
