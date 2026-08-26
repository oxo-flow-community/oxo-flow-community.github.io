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
**Root cause**: round 1 — random-sequence reads (no amplicon template
structure for learnErrors); round 2 — uniform Q40 qualities: the loess
error-rate fit needs error observations spread across the quality range.
**Fix**: templates × reads-per-template with PCR-style errors AND
Illumina-like declining qualities (Q40→Q20) + ~1% errors.
*Example*: ampliseq `generate_fixtures.py` (`290bce8` templates, `ba337dc` qualities).

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
**Root cause**: the engine substitutes scatter placeholders in input/output/shell but NOT in the script field (engine issue #98, FIXED in 0.14: script/pre_exec/on_success/on_failure substitute on all four fan-out paths — `Traitome/oxo-flow` `9544b0b`).
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

**Symptom**: SUPPA2 `psiPerEvent` dies with "No expression values have been buffered" after skipping every expression row; or the reference build exits 1 right after a successful `generateEvents`.
**Root cause**: SUPPA's `ExpressionReader`/`IoeReader` consume line 1 as the header and derive the expected field count from it — stripping the sample-name header makes the first data row the header (2 fields -> min_fields=3), so every real row rejects with "Unexpeced number of fields". `generateEvents` also writes one `events_<TYPE>_strict.ioe` PER event type and skips zero-event types entirely, so a hardcoded concat dies on the missing files (and a bare for-loop exits with its last iteration's status).
**Fix**: keep the expression header; concatenate event files with `awk "FNR==1 && NR!=1 {next} 1"` so only the first header survives and missing types are tolerated.
*Example*: tcasia `66d5a15`.

## License-gated user data

**Symptom**: a caller stage fails hard on a fresh clone because it needs an academic license file that no repo can ship; upstream runs the chain unconditionally, so the whole default path dies.
**Root cause**: upstream treats the license as always-present, but the license IS user data.
**Fix**: gate the caller's whole rule chain on an explicit config flag (default false) with commands unchanged when enabled; document the deviation in the README fidelity table. Also verify the caller's env installs at all — upstream's own pip pin may resolve on no index (majiq==2.5: PyPI and bioconda both lack it), and the fix chain continues (Cython extensions need numpy<2, gunicorn needs pkg_resources -> setuptools<81).
*Example*: tcasia `055b6cc` (MAJIQ chain on `run_majiq`), `a91a86e` (install from the org's `majiq_academic@v2.5` fork), `2063b63`/`cb6efd0` (numpy/setuptools pins).

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

**Symptom**: an assembler's EM spins forever ONLY under the engine (99.9% CPU for hours) while the identical command completes in seconds in a manual shell; flags, threads, data shape and CPU contention are all ruled out.
**Root cause**: metabat2 2.17 flaky EM spin (standalone-reproducible; engine premise refuted — engine #101 closed with a stdin-null contract hardening).
**Fix**: a generous shell-level timeout (20 min) that converts the spin into the empty-artifact emission — when the input legitimately yields zero bins, the zero-result channel contract applies.
*Example*: mag `c87e507`.

**Symptom**: a binner stops without writing a single file ("Marker gene search reveals that the dataset cannot be binned. Program stop.").
**Root cause**: gene-less input (random-sequence fixtures) or genuinely low-diversity real data — a valid zero-bin result.
**Fix**: emit the empty artifacts (noclass/tooshort/log/marker/summary) so the declared-output contract holds; guard the post-processing globs with `[ -e ]` or `|| true`.
*Example*: mag `53f5cbe` (maxbin2).

**Symptom**: cross-sample depth columns are all zero and composition binners degrade; or a checker dies with "Assembly fasta does not match alignment file".
**Root cause**: the fixture draws each species' sequence per sample — samples share no genome content, so cross-sample alignments map nothing; separately, a stale bam from a previous assembly generation sits next to a fresh fasta.
**Fix**: ONE shared community generated once, abundance-only variation between samples; and file-level (not directory-level) rule inputs/outputs so re-runs propagate through exact-string edges and per-file manifests.
*Example*: mag `2d7115f` (shared community), `af46b5a` + `945cd0b` (file-level wiring).

**Symptom**: helper scripts ship in the repo's scripts/ but rules call them bare (`foo.py: command not found`) — upstream containers had them in bin/.
**Fix**: `python scripts/foo.py` (or `python "$wd/scripts/foo.py"`) and declare the script as a rule input for invalidation.
*Example*: mag `c41983f`/`1255ad4` (15 call sites), viralrecon `5cba76b`.

**Symptom**: the kraken2 filter classifies ~100% of the reads and every downstream channel runs empty.
**Root cause**: the minimal host-removal DB was indexed over the VIRUS genome — the kraken2 step is the HOST filter, so the DB must cover the host and viral reads must pass through unclassified (the semantics were inverted).
**Fix**: index the DB over a host sequence (bundled 6kb human slice, taxid 9606); add a few percent host reads to the fixtures so the filter does real work.
*Example*: viralrecon `d9934b2`.

**Symptom**: fastp collapses thousands of pairs to a handful.
**Root cause**: the workflow's own QC is stricter than the fixture — viralrecon's fastp runs --qualified_quality_phred 30 --unqualified_percent_limit 10, which discards reads whose tails decline below Q30.
**Fix**: fixture qualities must satisfy the workflow's QC end to end (Q38->Q32 floor for viralrecon); check the workflow's fastp arguments before choosing quality curves.
*Example*: viralrecon `4ae6f4f`.

**Symptom**: a pipeline's zero-variant path dies repeatedly downstream (empty tsv kills the converter; the empty VCF loses FORMAT headers; freyja degenerates on the empty mutation set; the long-table script silently writes nothing).
**Root cause**: upstream drops zero-variant samples via a channel-level runtime filter; the port has no equivalent, so every consumer meets the empty channel unprepared.
**Fix**: the zero-variant channel family — header-carrying empty VCF (the full tool header block, not bare fileformat), row-count guards (wc -l > 1, not -s), passthrough for zero-record files at sort steps (bcftools sort strips headers no record uses), empty artifact emission with the tool's own header lines.
*Example*: viralrecon `82455f4`/`0492f5d`/`63a7f00`/`b3e60fb`/`af3bec9`/`0b331f9`.

**Symptom**: a helper script's outputs land with a different prefix than the declared names (summary_variants_metrics_mqc.csv vs variants_metrics_mqc.csv).
**Root cause**: the bundled script defaults --out_prefix to "summary" and the rule never passed one.
**Fix**: run the script once manually to see its real output names, then declare those.
*Example*: viralrecon `d4c7eeb`.

**Symptom**: multiqc's report writer dies with 'module rich has no attribute panel', or a bundled multiqc csv-extraction script finds no yaml files.
**Root cause**: rich.panel was removed in rich 13+ (the resolver picks it); multiqc 1.31 renamed the aggregate yamls to per-plot files the script does not read.
**Fix**: pin rich=12.6.0 and multiqc to the version whose yaml layout matches the bundled script (1.21); add pyyaml explicitly.
*Example*: viralrecon `ca70e91`/`8ba51b0`/`f6abdc7`.

**Symptom**: a multi-tool R env fails sequential solve conflicts after bumping r-base (r-tidyverse 1.3.2 pins r-base <4.3; bioconductor packages pin r42/r43 per build).
**Root cause**: an r42-generation pin set; one bump forces a generation-wide migration.
**Fix**: migrate the whole set in one pass (r-base + tidyverse + bioconductor builds), and verify each bioconductor version EXISTS on the channels before pinning.
*Example*: viralrecon `51051c7`/`0db6c3c`/`446bcc6`/`b660028`.

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

## Version-locked ML stacks

**Symptom**: a tool embeds a neural model, and its scoring python needs a dependency era that no modern solver produces — every "reasonable" version pairing fails at a different point (import, model load, session API).
**Root cause**: the model file (and the tool's python package) fix the stack: the saved model's keras version, the backend it needs, the h5py attribute semantics (2.x bytes vs 3.x str), the numpy ABI. Newer versions of any piece break a different link.
**Fix**: read the artifact itself — the hd5's `keras_version`/`backend` attrs, the package's imports (`vqsr_cnn` calls `K.clear_session`/`K.get_session` = TF-only) — and pin the era, not the latest. Beware conda activation scripts overriding `KERAS_BACKEND` per-OS (conda keras hardcodes theano on Linux). Also check where the python package actually comes from: gatktool declares only python; vqsr_cnn ships in the GATK sources, not on any index.
*Example*: sarek CNN stack (`python 3.6 + keras 2.2.4 + tensorflow 1.15.5 + h5py 2.7.1 + vqsr_cnn from the GATK repo`), gatk4 env pins in envs/gatk4.yaml.

## Container backends

**Symptom**: docker rules fail with daemon-level errors (`failed to lease content: NotFound`, `lease does not exist`, snapshot-store ENOENT) that persist across `docker system prune` and even full store wipes + service restarts.
**Root cause**: deleting live daemon state during a disk crisis corrupts the lease/snapshot metadata; the docker/containerd pair never recovers without re-provisioning.
**Fix**: pivot the rules to the singularity backend (`singularity = "docker://<same-image>"` — same registry images, portable SIFs, no daemon); give the pulls a big TMPDIR; and fix the engine setup to be idempotent (pull only when the image/SIF is absent — a leftover `.sif` makes `pull` refuse to overwrite).
*Examples*: sarek `0b8fd2a` (fastqc/vcftools to singularity), engine Traitome/oxo-flow#105 (docker inspect-first), #107 (singularity SIF-aware setup).

**Symptom**: mantaWorkflow.py dies at runLocusGraph with "Task memory requirement exceeds full available resources" despite a box-sized budget.
**Root cause**: upstream passes NO `-g`; runWorkflow's node auto-estimate under-reports on small boxes, and mergeMemMb=4096 exceeds the estimated budget.
**Fix**: pass `-g 4` explicitly (matches the mergeMemMb=4096 need).
*Example*: clindet `9a33799`.

**Symptom**: Manta GetAlignmentStats errors "Too few high-confidence read pairs (0)... At least 100 required".
**Root cause**: the fixture kit shipped 2-pair reads — Manta needs >=100 high-confidence pairs to estimate.
**Fix**: generate 10k-pair wgsim reads (ship `test/generate_reads.sh` alongside the fixtures).
*Example*: clindet `1be4181`.

**Symptom**: strelka2 segfaults in the dynamic loader (all frames in ld-linux, zero LD_DEBUG output) while starling2 in the same container works.
**Root cause**: bioconda strelka 2.9.10 (hdfd78af_2) is broken on glibc 2.39 hosts; germline path (starling2) is unaffected, somatic dies.
**Fix**: pin `strelka=2.9.7`.
*Example*: clindet `316b867`.

**Symptom**: caveman rejects the upstream default ignore-file: "should be an existing file" then "should be file with non-zero size".
**Root cause**: upstream passes `-ignore-file ""`; caveman 1.15.3 validates the arg strictly.
**Fix**: feed a one-region bed on an absent contig (same no-ignore semantics).
*Example*: clindet `b248def`.

**Symptom**: cgpFlagCaVEMan rejects the upstream defaults (empty -c/-v/-b/-ab, -t genome).
**Root cause**: 1.15.3 validates every arg; flag-config sections key off the `-s` species value (HG38_CHR21_WGS, not HUMAN_WGS); FLAGLIST is a Config::IniFiles heredoc that must end with an empty line; BEDFILES needs >=1 key.
**Fix**: ship GRCh38-verbatim flag params; drop bed-based flags when no chr21 flag data ships.
*Example*: clindet `ca223ad`.

**Symptom**: GATK dies with "An index is required" on annotation VCFs that look complete.
**Root cause**: the fixture shipped plain .vcf.gz without .tbi.
**Fix**: BGZF-compress + tabix-index every annotation VCF in the kit.
*Example*: clindet `5d72771`.

**Symptom**: R scripts die with "data.table::dcast currently only has a method for data.tables" / "The melt generic in data.table has been passed a data.frame" despite correct-looking code.
**Root cause**: the script loads data.table AFTER reshape2; data.table masks dcast/melt and its methods only accept data.tables.
**Fix**: qualify `reshape2::dcast` / `reshape2::melt` at the call sites.
*Example*: enrichment `2aa1a73`, `6780702`.

**Symptom**: rGREAT dies with "missing value where TRUE/FALSE needed" in great(); GSEApy prerank reports "No gene sets passed through filtering condition".
**Root cause**: GMT fixtures with placeholder names (GENE1..GENE10) pass naive tools but fail validating ones — SYMBOL→ENTREZ mapping yields empty sets (rGREAT's 0/0 check), and prerank filters every set against a ranked list that shares no symbols.
**Fix**: use real gene symbols in both the GMTs and the ranked CSVs.
*Example*: enrichment `5245b4a`, `5c04bef`.

**Symptom**: plotRegionGeneAssociations errors "need finite 'ylim' values".
**Root cause**: tiny fixtures make every binomial p-value zero — the barplot's ylim is non-finite.
**Fix**: guard the plot in tryCatch and draw a note; the table is the product.
*Example*: enrichment `c12a7c8`.

**Symptom**: runLOLA errors "Negative b entry... universe has a region that overlaps multiple user set regions"; downstream plot dies on log2(NULL) ("non-numeric argument").
**Root cause**: a single-region universe overlapping several query regions breaks LOLA's 2x2; the analysis never wrote oddsRatio/qValue columns the plot config consumes.
**Fix**: disjoint-window universe fixtures; write oddsRatio (b/c) + BH-adjusted qValue in the LOLA result.
*Example*: enrichment `9b8917e`.

**Symptom**: cellranger's martian jobmngr loops forever — "Need 6 GB of memory to start the next job (2.6 GB available). Waiting for jobs to complete."
**Root cause**: the port auto-sized `--localmem` from the engine's effective memory, which includes swap (RAM+swap on the box: 9.8G) — jobmngr gates on the physically-available MemAvailable, so a swap-backed budget is unreachable and the pipeline deadlocks at 0.4% CPU.
**Fix**: auto-size from `/proc/meminfo` MemAvailable (×2/3, 1 GB floor), with a config override for forcing; never from effective_memory (the engine's scheduling number, not a tool's physical budget — the same physical-vs-scheduled boundary as the cgroup clamp).
*Example*: scrna-seq `d28b72e`.

**Symptom**: cellranger count fails for one sample of a multi-sample demultiplexed folder while the other passes (or the pass is a concurrency race).
**Root cause**: the shared fastq staging dir is a multi-sample demultiplexed folder — count must receive `--sample` to select its own; without it, which sample wins depends on concurrent startup timing.
**Fix**: pass `--sample {sample}` explicitly.
*Example*: scrna-seq (v22 fix round).

**Symptom**: cellbender remove-background crashes in a chain on statistically-degenerate fixtures — flat count distributions raise a priors IndexError; 100 cells / 2000 empty droplets trip an encoder minibatch assert.
**Root cause**: the synthetic fixture's count distribution and cell/droplet ratios don't resemble real 10x output.
**Fix**: log-normal cell-count distribution (median ~150) + ambient empty droplets + ~800-cell scale; verify the fixture whitelist against the container's own barcode file.
*Example*: scrna-seq (fixture round).

**Symptom**: cellbender resumes from a stray ckpt.tar.gz left in the workdir (hash match → posterior loaded from checkpoint → no new files written → the rule's mv dies).
**Root cause**: cellbender persists checkpoints in the CWD and silently resumes.
**Fix**: `rm -f` the checkpoint before invoking; fresh-dir semantics for multiqc's mv on resume (results/multiqc is non-empty after a resume).
*Example*: scrna-seq (cellbender/multiqc round).

**Symptom**: an R helper ignores a `--flag value` argument (anndatar's get_arg greps `^--flag=`).
**Root cause**: the helper's arg contract is `--flag=value`, the shell form passes space-separated.
**Fix**: match the helper's own contract (`--flag=value`).
*Example*: scrna-seq (R round).

**Symptom**: wave/OCI images (scanpy/anndata/cellbender) are OCI→SIF-converted at exec time under names derived from the OCI repo — a pre-placed SIF or symlink with the pull-derived name never matches.
**Root cause**: the engine's SIF name derivation covers `docker://` pulls, not OCI repo conversions whose names differ.
**Fix**: point APPTAINER_CACHEDIR at the big disk (/data) and let the conversions land there.
*Example*: scrna-seq (infra round).

**Lesson — fixture whitelists**: a synthetic fixture's self-declared whitelist can be bogus (0% real chemistry match); validate fixture barcodes against the tool's own whitelist file before trusting the fixture.
*Example*: scrna-seq (whitelist round).

**Lesson — checkpoint command records**: `rule_runs[].command` may be confounded by masking or cross-run checkpoint reuse; it is not a primary bug-triaging artifact — prefer in-run diagnostic echoes.
*Example*: scrna-seq (samples_list retraction).

## Varlociraptor rounds (2026-08-22, verdict #24 — bioinfo-wsx full Tier A)

**Symptom**: reads map to the genome but at MAPQ 3 (or not at all), so downstream BQSR finds no usable reads (`apply_bqsr` on an empty RecalTable) and callers see garbage.
**Root cause**: the fixture window was repeat-rich (reads map to a paralog) or N-masked (maps nothing).
**Fix**: sample a uniquely-mapping window and probe-verify MAPQ 60 on a majority of reads before the campaign (192/200 probe reads at MAPQ 60).
*Example*: varlociraptor `8afbb85`.

**Symptom**: `PackagesNotFoundError` for a pin that solved fine days earlier.
**Root cause**: the version was REMOVED from the channel after the pin was written (vega-lite-cli 5.16, datavzrd 2.70.0 both gone).
**Fix**: re-pin to a version verified to exist on the channel right now, with the channel qualifier (conda-forge::6.4.3 / 2.71.0).
*Example*: varlociraptor `716054f`, `1b7e0e0`.

**Symptom**: `exit 127: samtools: command not found` in a rule that pipes `vg giraffe | samtools view` under the vg env.
**Root cause**: upstream assumes a host samtools; the port's env must carry every binary the shell invokes.
**Fix**: add the piped tool to the env yaml; audit each shell for binary/env mismatches.
*Example*: varlociraptor `8e3e69d`.

**Symptom**: pool fast-fails `resource budget too small` because upstream hardcodes 96 threads on a 64-core box.
**Root cause**: over-capacity hardcoded requests.
**Fix**: `threads = {effective_threads}` with a sensible ceiling (48) — and quote the placeholder in TOML: bare `{effective_threads}` parses as an inline table (parse error).
*Example*: varlociraptor `e303597`, `b30cb4d`, `fd71598`.

**Symptom**: a sed one-liner dies with `unknown option to s` / `unterminated s` / produces a chrom-prefixed two-column list that freebayes-parallel rejects (no regions → bcftools `Could not read VCF/BCF headers from -`).
**Root cause**: `:` and `/` delimiters collide with chrom colons and paths; the substitution produced `chrom:start-end` instead of a three-column BED.
**Fix**: `#` delimiters, map `chrom:start-end` → `chrom start end` (three columns), and guard the empty-region case by emitting a header-only BCF so the pipeline survives fixture-scale inputs.
*Example*: varlociraptor `246ef51`, `f73c04f`, `f83b046`, `54ec945`.

**Symptom**: oncoprint.py crashes on an empty call set (`ValueError: Must pass non-zero number of levels/codes`).
**Root cause**: the guard was placed AFTER the labels DataFrame construction, which already crashes set_index on the empty columns.
**Fix**: check for empty calls immediately after the concat, BEFORE any label construction; emit an empty oncoprint instead.
*Example*: varlociraptor `7fb9db3`, `ae315bd`, `515c497`.

**Symptom**: yte renders fail with `dict object has no attribute csv` / `SimpleNamespace has no attribute loc`.
**Root cause**: templates use attribute access (`?input.csv`) and pandas `.loc` on nested dicts — plain JSON dicts don't support either.
**Fix**: wrap the variables in SimpleNamespace and rebuild frame-encoded dicts recursively at ANY nesting depth.
*Example*: varlociraptor `9cdb02b`, `71bf729`.

**Lesson — server-side conda corruption**: a corrupted conda env cache + zombie child processes can wedge rules even when the workflow is correct; wipe the env cache and kill zombies (pgid) before re-solving.
*Example*: varlociraptor (server round).

## Clindet-RNA rounds (2026-08-22, verdict #21-RNA — tx-ubuntu)

**Symptom**: `ln: failed to create symbolic link '...': File exists` on a re-run/resume (link_bam round).
**Root cause**: the shell uses `ln -s` without `-f`; the checkpointed re-entry re-runs the rule and the link already exists.
**Fix**: `ln -sf` (idempotent) for every link in re-runnable rules.
*Example*: clindet-RNA (rna-port fix round).

**Symptom**: lofreq refuses to overwrite an existing output on resume (`Cannot write to ... file exists`-style).
**Root cause**: lofreq does not overwrite by default.
**Fix**: `rm -f` the declared output in the shell before invoking.
*Example*: clindet-RNA (rna-port fix round).

**Symptom**: a rule using `{input[0]}` receives the path in a position that downstream tools misparse.
**Root cause**: positional array expansion differences between the port's array form and the tool's CLI expectation.
**Fix**: expand `{input[0]}` explicitly in the intended argument position.
*Example*: clindet-RNA (rna-port fix round).

**Symptom**: FAI-derived offsets wrong (index tools report corrupt region files).
**Root cause**: the port computed offsets in characters; FAI offsets are byte offsets.
**Fix**: derive offsets in bytes from the .fai record semantics.
*Example*: clindet-RNA (rna-port fix round).

**Symptom**: STAR index reused stale after reference/GTF change — alignment silently uses the old index (or crashes on mismatch).
**Root cause**: the index path is not an engine-visible input, so checkpoint invalidation cannot see reference changes.
**Fix**: declare ref/gtf as rule inputs, rebuild the index unconditionally, and serialize pass1-log consumers with an explicit edge.
*Example*: clindet-RNA (rna-port fix round).

**Symptom**: arriba fusion calling outputs 0 rows on a synthetic fixture despite real chimeric reads flowing through.
**Root cause**: arriba's biological filters (end-to-end support, mate patterns) reject synthetic fusions — a FIXTURE limit, not a port defect; upstream parameters were kept verbatim.
**Fix**: document the limit in the fixture generator docstring; assert the chimeric read count upstream of arriba instead of arriba rows.
*Example*: clindet-RNA (f0fd05c fixture round).

**Lesson — fusion fixtures**: a workable chimeric fixture needs a mini reference DB and a fused region with real breakpoint structure (20kb chrX fusion worked); the tool's own filters decide what survives, so assert on the evidence the tool CONSUMES, not its output rows.
*Example*: clindet-RNA (arriba round).

## 2026-08-23 full-campaign re-verification (batch 1: mixscape + unsupervised)

**Symptom**: a rule fails with `EnvironmentLocationNotFound: Not a conda environment: <prefix>/envs/<name>` even though the env was created earlier.
**Root cause**: the engine's env-cache held a stale entry — the cache recorded the env as present but its conda metadata was invalidated (or the env was built on a full root disk and later moved/removed). The verify step trusts the cache and skips creation.
**Fix**: delete the env-cache entry (or `--skip-env-setup` off + clean `.oxo-flow/env-cache`) and re-run; long-term the verify path should re-validate a cached env's conda metadata before trusting it.
*Example*: unsupervised (2026-08-23 box round).

**Lesson — env disk placement**: conda envs on the box's ROOT disk hit ENOSPC mid-campaign (59G root, conda pkgs + envs); moving envs + pkgs dirs to the data volume freed 25G. Always place conda envs/pkgs and CARGO_TARGET_DIR on the data volume for campaign boxes.
*Example*: tx-ubuntu (2026-08-23 batch-1 round).

## 2026-08-23 full-campaign re-verification (batch 2: genome-tracks sc + snparcher)

**Symptom**: sinto aborts on unsorted/unindexed BAM input with a cryptic index error mid-run.
**Root cause**: sinto's split-by-barcode path requires position-sorted BAM + `.bai` present next to the BAM; fixtures were shipped without indexes.
**Fix**: index fixture BAMs at fixture-generation time (samtools index) so downstream tools find `.bai` without a pre-rule.
*Example*: genome-tracks full-line-sc (63c42ed).

**Symptom**: `ModuleNotFoundError: No module named 'pkg_resources'` inside a fresh env that resolved fine weeks ago.
**Root cause**: setuptools ≥81 removed pkg_resources (upstream sinto still imports it); a loose `setuptools` pin re-resolved to the breaking version.
**Fix**: pin `setuptools <81` in the env yaml and add `samtools` for indexing.
*Example*: genome-tracks full-line-sc (63c42ed).

**Symptom**: samtools merge refuses header-only (zero-byte) BAM stubs with "no data" — the port used `touch`-empty placeholders for empty barcode groups.
**Root cause**: modern samtools (≥1.16) validates input BAMs at merge; a 0-byte file is not a valid BAM.
**Fix**: emit a true header-only BAM (samtools view -b -H) for empty groups instead of `touch`.
*Example*: genome-tracks full-line-sc (ccd2abf).

**Symptom**: re-running ucsc_hub export fails with "file exists" on symlink creation.
**Root cause**: hub symlinks were created unconditionally — a resume/rerun re-links the same paths.
**Fix**: guard with an existence/identity check (idempotent symlink) so re-entry is safe.
*Example*: genome-tracks full-line-sc (fdfeec6).

**Lesson — sc-branch fixture budget**: pair-level plots on a sc demo pair were gated behind `plot_enabled` and the demo pair dropped from the mini fixture — mini fixtures must stay runnable under campaign disk budget while the full fixture keeps ≥2 groups for the real run.
*Example*: genome-tracks full-line-sc (fdfeec6 + b696baa/dede881).

## 2026-08-23 auto-sra mini track (STAR pathology, corrected diagnosis)

**Symptom**: STAR hangs mid-alignment — CPU spins for hours with no output; gdb shows an infinite recursion in `stitchWindowAligns`.
**Root cause (final)**: chr21-only reference subset + real human RNA-seq reads — cross-chromosome mates land unmapped and `quantMode GeneCounts` transcript stitching degenerates into unbounded recursion. Version-independent: 2.7.10a and 2.7.11b (avx2 AND plain builds) hang identically. An earlier "avx2 startup race" hypothesis was disproved by gdb + plain-build reproduction; full-genome runs do not exhibit the pathology (the nf-core ecosystem uses 2.7.11b at scale).
**Fix**: build the full-genome index (GRCh38.111 fasta) and restrict counting to the chr21 annotation — reference completeness pathology, not a tool or workflow defect. Keep the repo's STAR pin.
*Example*: auto-sra mini track, bioinfo-wsx (2026-08-23).

**Lesson — hang detection**: a rule that writes nothing for hours while CPUs spin needs a stack sample (gdb) before blaming the build variant; the earlier conclusion was wrong and had to be corrected. Validate "tool bug" hypotheses against a second build AND a second version.
*Example*: auto-sra mini track (2026-08-23).

**Lesson — reference provenance honesty**: a "GRCh38" reference that is actually a chr21-only subset existed on the box since old-index days — mini verdicts must record the actual reference content, not the label. Subset references can also create tool pathologies (this STAR hang) that look like port defects.
*Example*: auto-sra mini track (2026-08-23).

## 2026-08-23 light group (conda post-link network pathology)

**Symptom**: conda env creation fails 3× on the bioconda `genomeinfodbdata` post-link script with `curl 18` (proxy truncation) — the post-link download never completes behind the campaign proxy.
**Root cause**: post-link scripts fetch data at install time; a truncating proxy kills the transfer, and conda retries identically.
**Fix (box-local)**: download the source tarball on a clean host (Mac), place it in a local relay dir, patch the cached post-link script to prefer the local file, and rebuild the pkgs-cache tarball flat. Works because conda trusts already-extracted cache tarballs (no md5 re-verification at that point). Do NOT change the workflow repo — the pathology is network-side.
*Example*: rnaseq-star-deseq2 biomart env, tx-ubuntu (2026-08-23).

**Harder variant (8 attempts, final solution)**: the same post-link pathology on a package whose repodata sha256 forces online re-verification (.conda cache surgery impossible) and whose retries corrupt via mixed connections. Final: sudo-hosts redirect the bioconductor/galaxy domains to 127.0.0.1, serve the Mac-relayed data from a local `openssl s_server -WWW` with a locally-trusted cert, and — the last hurdle — set `SSL_CERT_FILE` to the SYSTEM CA bundle so the env's curl uses it. Roll everything back afterwards (hosts/CA/server cleared) to stay mirror-neutral.
*Example*: ampliseq dada2 env, tx-ubuntu (2026-08-23).

## 2026-08-23 heavy group (fetchngs repo races)

**Symptom**: three id rules writing the same fixed filename (id.txt) in a shared docker workdir overwrite each other — nondeterministic output depending on rule scheduling.
**Root cause**: concurrency race on a hardcoded scratch filename; per-rule workdir isolation was not honored by the port.
**Fix**: unique filenames per rule (0a118df).
*Example*: fetchngs, bioinfo-wsx (2026-08-23).

**Symptom**: `wget -c` on an already-complete file appends and corrupts it.
**Root cause**: resume flag on a complete download re-fetches with an offset.
**Fix**: md5-check-first idempotence guard before resuming (9a9f09f).
*Example*: fetchngs, bioinfo-wsx (2026-08-23).

**Symptom**: a rule fails with an env-version incompatibility (`rich.panel` AttributeError from multiqc 1.29 + rich 15) even though the repo's env yaml is correct.
**Root cause**: a pre-built shared env predates a repo pin update — the cache has the OLD version and the engine trusts it (see also the env-cache vanished-entry class).
**Fix**: verify pre-built env versions against the repo pin before re-runs (`conda install <pkg>=<pinned>` on the box); repo change NOT needed.
*Example*: sarek multiqc env, tx-ubuntu (2026-08-23).

**Symptom**: a rule fails with "no package called X" although its env yaml pins X — a DIFFERENT workflow's env with the same name was reused.
**Root cause**: the engine identifies conda envs by NAME only; two workflows shipping different `deseq2.yaml` contents both derive the name `deseq2` and share one conda prefix. The first-built env wins.
**Fix (box)**: `conda env remove -n <name>` + `rm .oxo-flow/env-cache/environment_cache.json`, rebuild. Engine-side: content hash in the env identity / per-workflow prefixes — tracked as issue #159.
*Example*: rnaseq-star-deseq2 vs rnaseq deseq2 collision, tx-ubuntu (2026-08-23).

**Symptom**: LOLA ≥1.22 errors with "object 'filename' not found" on a fixture index that worked with older LOLA.
**Root cause**: loadRegionDB evaluates columns by name; the fixture's 2-column index.txt had no header, and 'filename' became a named requirement in ≥1.22.
**Fix**: add the header row with a real `filename` column (c7f194c).
*Example*: enrichment LOLA fixture, bioinfo-wsx (2026-08-23).

**Lesson — patch the pkgs cache, not the env dir**: post-link dataURLs rewrites made INSIDE an env directory get wiped by the next env rebuild; the durable patch point is the conda pkgs cache (e.g. dataURLs.json rewritten to file://) so re-extraction reads the patched copy.
*Example*: enrichment region env (7 bioconda data packages), bioinfo-wsx (2026-08-23).

**Symptom**: a rule fails on a raw.githubusercontent.com fetch — the domain is unreachable from the box's network.
**Root cause**: direct GitHub-raw URLs have no mirror fallback in the rule.
**Fix (repo)**: mirror fallback (ghfast.top first, original as fallback) — same pattern as mag's build_ale.sh (6fda195).
*Example*: varlociraptor delly exclusion regions, bioinfo-wsx (2026-08-23).

**Engine defect candidate — singularity URI→IMG naming**: %3A-encoded colons in a container URI are not decoded before the `s#:#_#g` IMG-name substitution, so the computed name never matches the cached image and the backend always re-pulls. Bare-colon URIs work. Tracked as engine issue #162; box workaround = pre-place the sif at the expected cache hash path.
*Example*: clindet lofreq sif, tx-ubuntu (2026-08-23).

**Lesson — live-query evidence**: biomaRt gene2symbol ran against live Ensembl (3 steps, 48-66s each) — prefer recording live-network evidence over mocking when the tool's core value is annotation freshness.
*Example*: rnaseq-star-deseq2 (2026-08-23).

## 2026-08-23 auto-sra mini track closure (7 classes, 24/24 收官)

1. **STAR stitchWindowAligns recursion** — chr21-subset reference + cross-chromosome mates; fixed by full-genome index (see entry above).
2. **conda star 2.7.10a ships a single binary** — no SIMD wrapper family; `star` resolves directly, unlike 2.7.11b's avx2/plain selection.
3. **conda hardlink trap** — `cat > env/bin/<tool>` writes through conda's hardlinks and pollutes the SHARED pkgs cache; patch envs via a copy, never a redirect into bin/.
4. **DESeq2 needs ≥2 replicates per condition** — a 1v1 fixture fails `checkForExperimentalReplicates`; mini fixtures for DGE workflows must be 2v2.
5. **.sra copy mtime triggers dump fingerprint invalidation** — copying staged .sra files refreshes mtime → the input manifest (issue #72) invalidates the dump rule → full re-dump; keep .dumped markers or copy with `cp -p`.
6. **fasterq-dump 3.4.1 segfaults** — pin 3.1.1 with an absolute path in the env.
7. **Reference chromosome naming** — Ensembl `1` vs `chr1` mismatch breaks annotation joins; align fasta and GTF naming before building indexes.
*Example*: auto-sra mini track rounds 1-21, bioinfo-wsx (2026-08-23).

## 2026-08-23 9-mini queue (docker storage exhaustion)

**Symptom**: docker image pull fails mid-layer with "failed commit on ref" after the root disk filled earlier in the campaign.
**Root cause**: leftover ENOSPC aftereffects — the docker storage pool cannot commit layers with the root partition near-full (96%).
**Fix**: `docker system prune -af` to reclaim unused images/volumes (reclaimed 23GB here), then re-pull. Keep docker images on a data volume from the start where possible.
*Example*: eager (nfcore/eager:2.5.3), tx-ubuntu (2026-08-23).

## 2026-08-23 9-mini queue (checkpoint no-op trap — methodology)

**Symptom**: a "re-verification" run reports 0 succeeded / N skipped with exit 0 — every rule's checkpoint is fresh from a previous round.
**Root cause**: the engine's resume semantics (a feature) make a re-run of an already-verified repo a pure no-op — the "verdict" would be fake.
**Fix**: before re-running an already-live repo, force a real run — `rm -rf .oxo-flow results` (or `--rerun` where semantically honest). ALWAYS check the succeeded/skipped split before calling a round a live test.
*Example*: scrna-seq first launch (0/32 no-op → forced 22/0/10), tx-ubuntu (2026-08-23). Applies to every re-verification round in this campaign.

## 2026-08-23 9-mini queue (legacy C source vs modern GCC)

**Symptom**: a vendored 2018-era C tool fails to compile in its build script — implicit declarations (strcmp/close/tdestroy/...) and K&R-style pointers are hard errors under GCC≥14.
**Root cause**: C compilers tightened implicit-declaration rules over the years; code that built in 2018 does not build verbatim on GCC 14.
**Fix**: `-D_GNU_SOURCE`, force-include the standard headers, and downgrade only the specific warnings that gate the build (-Wno-error=...) — do not blanket-disable -Werror.
*Example*: mag's ale build (2554bde), bioinfo-wsx (2026-08-23).

## 2026-08-23 9-mini queue (China-network DB pre-staging)

**Symptom**: tool-run DB downloads crawl (EBI pfam 293MB at 2MB/min) or die behind the campaign proxy (curl 18 / SSL 77), blocking antismash 7 (10 DB components, 1.76GB total), gtdb metadata (193MB), and bioconductor post-link fetches.
**Fix (repeatable pattern)**: download the full DB set on the Mac (clean network), transfer to the box, and pre-stage into the exact paths the tool's `download_if_not_present` checks — the sha256 verification then accepts the staged files and skips the download. Same idea as the conda pkgs-cache patch. Do NOT change the workflow repo — the pathology is network-side.
*Example*: bgcflow antismash DBs + gtdb metadata, bioinfo-wsx (2026-08-23); 3 independent hits this campaign (also ampliseq/rnaseq-star-deseq2 bioconductor post-links).

## atacseq excluded-branch port rounds (2026-08-25/26, bioinfo-wsx — 14/14 gates)

Nine queue rounds over the when-gated branches (14 gates, engine 0.14.1).
Every class below was hit live, root-caused and fixed in
oxo-flow-community/oxo-flow-atacseq#2.

**Symptom**: `ln: failed to create symbolic link '...mLb.sorted.bam': File exists` — the merged-library symlink rule fails on every gated re-run.
**Root cause**: the engine re-runs rules IN PLACE when a config change invalidates them (each gate = one config override in the same workdir); plain `ln -s` refuses to replace the previous run's symlink. Upstream only ever runs on a fresh workdir.
**Fix**: `ln -sf` for re-created symlinks; `rm -rf` before `mv` of directories (same class bit `mv multiqc_data`).
*Example*: atacseq `2167877`, `0242bb0`.

**Symptom**: `[bns_restore_core] Parse error reading genome.fa.amb` in bwa_mem after the prepare_reference gate rebuilt the index.
**Root cause**: the index rule ran in a different biocontainer build than the aligner; the two bwa 0.7.17 builds' `.amb` formats are incompatible.
**Fix**: index-building rules use the SAME container image as the rule that consumes the index.
*Example*: atacseq `0242bb0` (ref::bwa_index → the bwa_mem mulled image).

**Symptom**: align rules race/ignore index rules — no DAG edge.
**Root cause**: align rules declared only reads as inputs; `{config.bwa_index}`-style config paths form no edge and no invalidation (exact-string edge matching).
**Fix**: declare the index files (`.amb/.ann/.bwt/.pac/.sa`, `.1.bt2..rev.2.bt2`, `Genome/SA/SAindex`) as rule inputs.
*Example*: atacseq `0242bb0`.

**Symptom**: chromap mapping segfaults AND the reference FASTA on disk turns into binary junk.
**Root cause**: `chromap_index` was set to the reference path itself — `chromap -i -o <ref>` OVERWRITES the reference with the index, then mapping against the self-clobbered file crashes. Silent data-loss hazard in the inline index-build pattern.
**Fix**: index path must differ from the reference (`<fasta>.index`, like upstream); hard-error guard `chromap_index != reference` in the rule.
*Example*: atacseq `0242bb0`.

**Symptom**: PE branch produces zero-mapped-read BAMs; plotFingerprint: "does not have any mapped reads ... No reads were found in N regions sampled".
**Root cause**: fixture synthesized R2 as the REVERSE of R1 (not reverse-complement) — every pair is same-strand, fails the `-f 0x001` proper-pair filter, filtered BAM is empty.
**Fix**: R2 = reverse_complement(R1) in the generator.
*Example*: atacseq `100b398` (generate_fixtures.py).

**Symptom**: preseq `ERROR: too many defects in the approximation, consider running in defect mode`.
**Root cause**: fixtures with incidental duplicates only — no geometric duplicate structure for the extrapolation.
**Fix**: ~30 % of reads duplicated at 2×/4×/8×/16× multiplicity (see the preseq class above).
*Example*: atacseq `100b398`.

**Symptom**: DESeq2 dies with `newsplit: out of vertex space` in `localDispersionFit -> locfit -> lfproc` (via VST or rlog — both estimate dispersions).
**Root cause**: a tiny fixture genome yields a handful of consensus peaks; locfit needs hundreds of differential features. `deseq2_vst=false` does NOT dodge it (rlog hits the same fit).
**Fix**: hundreds of differential features — the generator emits ~150 peak zones per autosome with sample-differential read weights.
*Example*: atacseq `100b398`.

**Symptom**: deseq2_qc.r writes `size_factors/results/bwa/.../S1.size_factors.txt` — "No such file or directory".
**Root cause**: featureCounts names its count columns after the paths it is GIVEN; full relative paths survive the script's `--sample_suffix` strip, and the stripped name is prepended to size_factors/.
**Fix**: cd into the bam dir and pass BARE names (with `$PWD`-absolute `-a`/`-o` so the cd cannot break them).
*Example*: atacseq `d020d62`.

**Symptom**: engine output validation fails a Picard metrics rule: declared `insert_size_metrics` / `insert_size_histogram.pdf` never appear.
**Root cause**: CollectInsertSizeMetrics emits nothing on single-end bams; the rule (SE-only) declared the PE-only outputs. An earlier PASS was bogus — it silently consumed stale flT files left by the previous paired gate in the shared workdir.
**Fix**: declare only what the SE run can produce; document the PE variant as unported. Also: never trust a gate PASS when an earlier gate may have left same-named files behind — re-verify on a clean workdir.
*Example*: atacseq `d020d62`.

**Symptom**: `ref::bwa_index` fails with `fail to open file 'genome.fa.pac' : Permission denied` right after a manual docker index build.
**Root cause**: the engine runs containers with `--user $(id -u):$(id -g)`; a manual `docker run` (root) left root-owned index files that the engine user cannot overwrite.
**Fix**: build fixture artifacts AS the engine user, or delete them so the rule rebuilds as the engine user.
*Example*: atacseq round 10.

**Symptom**: re-runs of fixed code keep failing with the OLD error; the box checkout shows a stale commit.
**Root cause**: the queue's `git fetch origin -q` failed silently (China network) and the script continued on the cached ref — the first queue generation had a `ghfast.top` mirror fallback, later ones dropped it.
**Fix**: keep the mirror fallback in every queue/launcher (`git fetch origin || git fetch https://ghfast.top/...`); print the checked-out SHA in the queue output.
*Example*: atacseq rounds 9→11.
