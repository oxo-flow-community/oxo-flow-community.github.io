# snparcher completeness audit (2026-08-21)

Upstream: harvardinformatics/snparcher @ v2.2 · Port: `oxo-flow-snparcher`
(live-verified).

~58 distinct rules across 16 snakefiles; named targets (setup/
download_reads/map_samples/call_variants/qc_report/callable_sites/gvcfs)
+ 2 standalone modules (postprocess, qc) + template module.

## Mode matrix (upstream)

| axis | options |
|---|---|
| variant caller | gatk (default, ± intervals.enabled scatter) / sentieon / bcftools / deepvariant / parabricks |
| input_type (per sample) | srr (prefetch + ffq ENA fallback) / fastq / bam / gvcf |
| reference source | local path / URL / NCBI accession (datasets CLI) |
| long_contig_mode | auto (csi indexing, picard SortVcf, archive chains) |
| dedup | mark_duplicates per-sample override |
| callable sites | mosdepth+clam coverage / genmap mappability / merged BED |
| modules | postprocess (bcftools filter chain, split_by_type), qc (vcftools + plink2 + admixture + Rmd dashboard) |

## Gap tiers vs the port

**P0**: the 4 non-default callers (sentieon chain, bcftools regional
mpileup, deepvariant+glnexus, parabricks+joint chain); interval
scattering mode (checkpoint-driven gvcf/db intervals + staged concats);
gvcf/bam/srr input types; long-contig mode; callable-sites suite
(mosdepth/clam/genmap); both standalone modules (postprocess filter
chain + QC dashboard w/ plink/admixture).

**P1**: Sentieon (license env), Parabricks (commercial container +
GPU, hard error without image), Google Maps API key (optional QC
dashboard panel only).

**P2**: mark_duplicates toggles, ploidy/het_prior/coverage params,
concat batching, bcftools quality floors, deepvariant model_type,
genmap sub-modes, interval scatter factors, module enable switches.

Compatibility gates (upstream design, mirror or document): gvcf input
incompatible with bcftools/deepvariant/parabricks; long_contig_mode
incompatible with sentieon/parabricks; v1 config keys hard-fail;
removed modules (mk/trackhub) warned.

## Verdict

Widest config surface after sarek — 5 callers × 4 input types ×
callable-sites × 2 modules. Ported default (gatk intervals + fastq)
leaves the caller matrix and both modules as the main P0.

## Re-verification (2026-08-23, batch 2)

Engine: latest main (post-v0.14.1) · Box: tx-ubuntu · Mode: real CLI
run, not dry-run.

**21/21 rules succeeded, exit 0, one round, zero failures** at HEAD
(1b4d2f7, raw/-at-root fix merged). No new failure classes — the
default-path port (gatk intervals + fastq) runs clean against the
reference data with no intervention.
