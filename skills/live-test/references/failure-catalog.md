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

**Symptom**: DESeq2 chain dies stepwise: `checkForExperimentalReplicates` (needs >=2 replicates per combination), then `estimateDispersionsFit` (locfit needs hundreds of genes), then all-zero size factors.
**Root cause**: fixtures with one replicate per condition, a handful of genes, or genes with zero counts everywhere.
**Fix**: >=2 replicates per condition combination, every gene expressed at differential levels in every sample (zero-free), and hundreds of genes for the dispersion fit.
*Example*: rnaseq-star-deseq2 `cc49939` (replicates), `db95056` (60 genes).

**Symptom**: STAR's stranded column counts nothing for '-' genes; the DESeq2 matrix has zero columns for the reverse-protocol units.
**Root cause**: for a reverse (TruSeq) protocol R1 is the ANTISENSE of the RNA — the generator emitted R1 as the sense transcript.
**Fix**: protocol-aware generator: emit R1 = reverse-complement of the transcript for `reverse` units.
*Example*: rnaseq-star-deseq2 `generate_fixtures.py` PROTOCOL map.

**Symptom**: an assembler writes no output at all (`scaffolds.fasta` never appears) yet the rule shell reports success; or the assembler dies with `Failed to determine offset!`.
**Root cause**: the fixture is below the tool's viable input (a few dozen reads), or its quality strings are uniform (offset autodetection needs varied low/high chars).
**Fix**: a few tens of kb of community at >=20x with error-free-ish reads for assembly; Illumina-like declining Q38->Q23 quality strings.
*Example*: mag `98513fa` (3x30kb community), `0dcdc57` (qualities).

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

**Symptom**: a long single-line tool command produces an empty output file after an edit (`--outStd BAM_SortedByCoordinate` became its own command).
**Root cause**: the command was split across lines so the redirect `> out.bam` attached to a fragment.
**Fix**: keep the whole invocation + redirect on ONE line; no line continuation inside redirect chains.
*Example*: rnaseq-star-deseq2 `1f2fb3c`.

**Symptom**: a rule's script field still shows a literal `{variable}`.
**Root cause**: the engine substitutes scatter placeholders in input/output/shell but NOT in the script field (engine issue #98).
**Fix**: expand the scatter into explicit per-instance rules.
*Example*: rnaseq-star-deseq2 `79c1cd0` (three explicit pca rules).

**Symptom**: RSeQC `read_distribution` dies on negative intron spans from a gffutils-built BED12.
**Root cause**: gffutils emits '-' strand blocks in transcript (descending) order; RSeQC computes introns as (block_i.end, block_{i+1}.start).
**Fix**: sort block sizes/starts into ascending genomic order before writing the BED12.
*Example*: rnaseq-star-deseq2 `gtf2bed.py`.

**Symptom**: an R script dies with `replacement has N rows, data has 0` or an unrelated positional-arg error after a config change.
**Root cause**: empty config values (`""`) vanished in word-splitting, shifting every later positional argument.
**Fix**: quote every `{config.x}` argument (`"{config.x}"`) so empties stay in place.
*Example*: mixscape `ad59243`.

**Symptom**: CalcPerturbSig dies with `Cannot find more nearest neighbours than there are points`.
**Root cause**: n_neighbors exceeds the per-class cell count in the fixture (or the RNG draw collapses a class to a single point).
**Fix**: every class >= 2x n_neighbors cells; control the RNG draw order so the good draw lands first.
*Example*: mixscape `8b10d8a`, `778a250`.

**Symptom**: an R script's tolerance path never fires under the engine, yet the identical command succeeds manually.
**Root cause**: the engine's script field executed a stale copy (the script is re-written per run and the copy raced).
**Fix**: run R via the shell field (`Rscript scripts/foo.R ...`) so the environment and file are resolved fresh.
*Example*: mixscape `18fc091`.

**Symptom**: visualize dies with `'X' is not an assay` on the default config.
**Root cause**: the config default assumes an assay the minimal input does not carry (10x Antibody_Capture).
**Fix**: default the assay to `""` (the disable sentinel per the script's arg contract).
*Example*: mixscape `0c0a56d`.

**Symptom**: an LDA (or any conditional subset) rule dies when the subset is empty, e.g. `replacement has N rows, data has 0`.
**Root cause**: zero perturbed cells after filtering is a legal result; the code assumed the subset is non-empty.
**Fix**: guard on the cell COUNT (not factor levels); on zero, write the empty filtered artifacts + a placeholder plot and exit 0 — the zero-result channel contract.
*Example*: mixscape `lda.R`.

**Symptom**: CIRIquant hangs forever (orphaned wait_for_partner processes) on a dataset with no backsplice junctions.
**Root cause**: its precheck finds nothing and it still waits for partners that never appear.
**Fix**: pre-run CIRI2 (fast junction call) and skip the quant step when the row count is zero; tolerate the resulting empty beds downstream.
*Example*: circrna `9b14b4e`.

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

**Symptom**: a tool gets killed/OOMs or fails mysteriously although its rule's memory request was clamped.
**Root cause**: the TOOL flag hardcodes the upstream machine's budget (`megahit -m 42949672960` = 40 GB) instead of using the engine placeholder.
**Fix**: `-m $(( {effective_memory_mb} * 1048576 ))` (or the tool's unit); reservations clamp automatically, tool flags do not.
*Example*: mag `98513fa`.

**Symptom**: a prep rule dies with `tar: Cannot connect to https` on the DEFAULT config.
**Root cause**: the config default is the upstream download URL but the rule only unpacks local paths — tar cannot fetch URLs.
**Fix**: default the path to `""` and fail fast with a clear message when the gate is on and the path is empty; document the local-file contract.
*Example*: mag `3cdd911`.

## Environment provisioning

**Symptom**: `PackagesNotFoundError` for a pinned package even on the
main channel.
**Root cause**: the package was removed from bioconda (upstream pins
it too — dead dependency for everyone).
**Fix**: install from the official source tag via pip
(`git+https://…@vX.Y.Z`) + build toolchain in the yaml.
*Example*: tcasia `c4c8179` (spladder).

**Symptom**: `PackagesNotFoundError` for a conda-forge-native package (pigz, pandas, python, igraph, ...) pinned with a `bioconda::` qualifier.
**Root cause**: the qualifier restricts resolution to the bioconda channel ALONE, which does not carry that package (or that version); the error looks like a dead pin but the pin is fine on conda-forge.
**Fix**: drop the qualifier and let channel priority (conda-forge first) resolve; sweep every yaml in envs/ in one pass.
*Example*: mag `d936682` (12 envs; earlier coreutils instance `07dfa9e`).

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

**Symptom**: `igv_files_to_session.py` (or any consumer of a
tab-separated helper file) dies with `not enough values to unpack
(expected 2, got 1)`.
**Root cause**: the file was written by `echo "a\\tb"` inside a TOML
shell block — TOML's `\\t` reaches the shell as backslash-t, and
plain `echo` prints it literally, so the file has one field.
**Fix**: `printf "%s\\t%s\\n" a b > file` — `printf` interprets the
escapes and writes a real tab. Always `cat -A` the file to see
`^I` vs `\t` before debugging consumers.
*Example*: chipseq `c3c66ce`.

**Symptom**: docker pull fails with `error from registry: denied`
even on a working mirror.
**Root cause**: the upstream image repo was retired from Docker Hub
(nf-core deleted the `nf-core/ubuntu` org image); mirrors cannot
serve what no longer exists.
**Fix**: switch to the neutral `docker.io/library/...` base for
shell-only rules; for tool images, re-pin a live biocontainers tag.
*Example*: chipseq `5e8b86d`.

**Symptom**: AdapterRemoval (or any strict parser) dies at
`Error reading FASTQ record at line 1; invalid FASTQ record;
sequence/quality length does not match` on every record.
**Root cause**: the generator drew fragments *shorter than the read
length*, so `frag[:READ_LEN]` returned the whole fragment (75-87bp)
while the quality string stayed fixed at READ_LEN — every record
mismatches.
**Fix**: fragments ≥ READ_LEN so both mates are exactly READ_LEN;
for a collapse pipeline keep inserts at READ_LEN+20…READ_LEN+60 so
the mates still overlap. Validate seq==qual length for every record
after regenerating.
*Example*: eager `967bcae`.

**Symptom**: a tool prints a success banner and exits 0, but its
declared outputs are missing (`Shell exited 0 but declared outputs
are missing`).
**Root cause**: the tool silently skips writing when its outdir is
the current directory (qualimap 2.2.2-dev: `-outdir .` →
"Output folder already exists" → nothing written).
**Fix**: point the outdir at the declared output's own directory
(the engine pre-creates it), never `.`; reproduce manually with
`-outdir freshdir` to see where the tool really writes.
*Example*: eager `2334495`.
**Symptom**: a fix that passed before fails again on requeue — the failure is the OLD one, verbatim.
**Root cause**: `git reset --hard` on the server clobbered uncommitted server-side regens (fixture files) with the repo's stale committed copies.
**Fix**: commit regenerated fixtures in the SAME change as the generator fix, before resetting the server tree; never rely on server-local regens surviving a reset.
*Example*: mixscape `778a250` (regens committed) vs the resurrected nn2 failure.
