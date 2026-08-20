# chipseq completeness audit (2026-08-21)

Upstream: nf-core/chipseq @ 2.1.0 · Port: `oxo-flow-chipseq` (live-verified).

## Mode matrix (upstream — all parameter-driven, one entry point)

| axis | options | default |
|---|---|---|
| library layout | paired / single-end (per-sample samplesheet) | — |
| aligner | bwa / bowtie2 / chromap / star | bwa |
| peak mode | broad / `--narrow_peak` | broad |
| consensus peaks | `--skip_consensus_peaks` | ON |
| DESeq2 QC | `--skip_deseq2_qc` | ON |

NOT runnable at this tag: differential binding (removed in 2.0.0 — only
reproducibility QC remains), UMI mode (`with_umi=false` hardcoded,
UMITOOLS_EXTRACT is dead code), no-input mode (input mandatory).

## Gap tiers vs the port

**P0** (portable): the 3 non-default aligners — bowtie2, chromap, star
(each = index build + align step only; downstream shared). SE branch
(BAMTOOLS_FILTER se-JSON + SAMTOOLS_INDEX + BAM_STATS; bigWig `-fs`).

**P2** (config variants — the bulk of the surface): narrow/broad
(`--broad_cutoff`), `--macs_fdr/--macs_pvalue`, `--save_macs_pileup`,
`--min_reps_consensus`, all `--skip_*` gates (consensus_peaks,
deseq2_qc, peak_annotation, peak_qc, fastqc, trimming, preseq, picard_metrics,
spp, plot_profile, plot_fingerprint, igv, multiqc), `--keep_dups`,
`--keep_multi_map`, `--save_align_intermeds/--save_trimmed/--save_reference`,
`--fragment_size`, trim args, `--bwa_min_score`, `--seq_center`,
`--deseq2_vst`, iGenomes genome entries, manual reference overrides.

**P1**: none hard — all tools OSS. Soft gate: UCSC `bedGraphToBigWig`
(kent utilities: free academic/non-profit, UCSC license for commercial —
document it).

External deps: iGenomes S3 refs, blacklists ship in-repo, nf-core/configs
fetch (warning-only offline), test data HTTPS.

## Verdict

Likely the lightest audit of the batch — default bwa+broad path ported,
the gap surface is almost entirely P2 toggles + 3 P0 aligners sharing the
downstream chain.
