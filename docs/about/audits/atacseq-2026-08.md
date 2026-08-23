# atacseq completeness audit (2026-08-21)

Upstream: nf-core/atacseq @ 2.1.2 · Port: `oxo-flow-atacseq` (live-verified).

## Mode matrix (upstream — param-driven, single workflow)

| axis | options | default |
|---|---|---|
| aligner | bwa / bowtie2 / chromap / star | bwa |
| layout | paired / single-end (samplesheet per-sample) | — |
| controls | `--with_control` + control columns | off |
| replicate merging | merged-replicate arm (full second chain: markdup/bigwig/peaks/consensus) | ON |
| consensus peaks | `--skip_consensus_peaks` | ON |
| peak mode | broad (default) / `--narrow_peak` | broad |
| QC toggles | 13 skip flags (picard/preseq/plot_profile/plot_fingerprint/ataqv/igv/peak_qc/peak_annotation/deseq2_qc/multiqc/fastqc/trimming) | mixed |

Peak caller: MACS2 only (no Genrich at this tag); annotation HOMER;
QC ataqv/deepTools/Preseq/Picard.

## Gap tiers vs the port

**P0**: 3 non-default aligners (bowtie2, chromap, star — each index +
align arm only, downstream shared; star pins 2.6.1d index format);
controls mode (MACS2 control pairing + samplesheet columns); merged-
replicate arm (full second chain).

**P1**: none — all tools OSS (ataqv MIT, chromap MIT, MACS2 BSD;
STAR/bowtie2 GPLv3 compliance note only).

**P2**: the whole QC-toggle matrix, narrow/broad + cutoff, macs_fdr/
pvalue, min_reps_consensus, save_macs_pileup, keep_dups/keep_multi_map/
keep_mito, fragment_size, seq_center, min_trimmed_reads, deseq2_vst,
save_* publish gates, blacklist handling, iGenomes genomes.

Tag-level gotchas (do not port): --skip_qc only gates FastQC (schema
overclaims); macs_fdr/pvalue ignored on the replicate arm; --read_length
enum-restricted; samples silently dropped below min_trimmed_reads.

External deps: iGenomes S3, raw.githubusercontent test data, Biocontainers.

## Verdict

Light surface — shared backbone with 4 swappable aligners and one
controls branch as the only structural P0s; everything else is toggles.

## Re-verification (2026-08-23, batch 3)

Engine: latest main (post-v0.14.1) · Box: tx-ubuntu · Mode: real CLI
run, not dry-run.

**29/29 rules succeeded, exit 0, one round, zero failures** at the
latest commit. No fixes needed and no new failure classes — the
default path (bwa aligner arm) runs clean against the reference data
with no intervention.
