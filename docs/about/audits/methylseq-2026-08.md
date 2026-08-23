# methylseq completeness audit (2026-08-21)

Upstream: nf-core/methylseq @ 4.2.0 · Port: `oxo-flow-methylseq`
(live-verified).

## Mode matrix (upstream)

| axis | options | default |
|---|---|---|
| aligner | bismark / bismark_hisat / bwameth / bwamem (TAPS) | bismark |
| bwameth engine | CPU / GPU (Parabricks, `-profile gpu`) | CPU |
| methylation caller | Bismark extractor / MethylDackel (bwameth) / rastair TAPS (bwamem or `--taps`) | per-aligner |
| library presets | --taps / --pbat / --rrbs / --slamseq / --em_seq / --single_cell / --accel / --zymo | — |
| optional | --run_qualimap / --run_preseq / --run_targeted_sequencing (+ --collecthsmetrics) | off |

BAM-input mode NOT present at this tag (removed from 2.x). Paired/
single-end per-sample from samplesheet; CAT_FASTQ for multi-fastq.

## Gap tiers vs the port

**P0**: bismark_hisat (genomeprep + align --hisat2 + known_splices);
bwameth CPU chain (bwameth index/align, picard dedup, MethylDackel
extract + mbias + methyl_kit); bwamem TAPS chain (bwa-mem align,
addorreplace readgroups, rastair mbias/parser/call/methylkit);
targeted-sequencing mode (bedtools intersect + Picard hsmetrics chain);
qualimap + preseq optional tools; coverage2cytosine (--cytosine_report/
--nomeseq); library presets (pbat/rrbs/slamseq/em_seq/single_cell/accel/
zymo — each is a params-set, mostly P2 config actually).

**P1**: Parabricks GPU bwameth (commercial license + GPU + container-only).

**P2**: the library presets (TrimGalore/Bismark arg bundles — config
absorption), --skip_* gates, --use_mem2, bismark/methyldackel/rastair
tunables, save_* publish gates.

External deps: iGenomes S3, nf-core test data URLs, Seqera Wave for
arm64/wave profiles.

## Verdict

Compact surface: 4 aligners × 3 caller paths + presets. The ported
bismark default leaves bwameth + bwamem-TAPS chains as the main P0.

## Re-verification (2026-08-23, light group)

Engine: latest main (post-v0.14.1) · Box: tx-ubuntu (conda envs) ·
Mode: real CLI run, not dry-run · `-j 2 --keep-going`.

**19 succeeded, 3 skipped, 0 failed, exit 0**, one round, zero fixes.
Coverage chain: bismark genome prep → fastqc → trimgalore → bismark
align → dedup → sort/index → methylation extractor → bismark
report/summary → multiqc. All 3 skips are by design: coverage2cytosine
×2 gated off (upstream `--cytosine_report`/`--nomeseq` default-off,
kept verbatim by the port); genomepreparation = fresh checkpoint reuse
(BismarkIndex from Aug-17).
