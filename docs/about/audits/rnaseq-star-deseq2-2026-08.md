# rna-seq-star-deseq2 completeness audit (2026-08-21)

Upstream: snakemake-workflows/rna-seq-star-deseq2 @ v3.1.1 · Port:
`oxo-flow-rnaseq-star-deseq2` (live-verified).

Single-DAG snakemake pipeline (24 rules): Ensembl ref download + faidx/
bwa/STAR indices → fastp → STAR align (GeneCounts) → 9 RSeQC rules →
count_matrix (technical-rep collapse) → deseq2_init → deseq2 × contrasts
(ashr) → gene_2_symbol (biomaRt) → pca → multiqc.

## Mode axes (config-driven, orthogonal)

| axis | options |
|---|---|
| read source | local PE / local SE / SRA accession (per unit; SRA PE-only) |
| trimming | on (fastp_se/pe) / off |
| strandedness | none/yes/reverse per unit |
| contrasts | arbitrary count; dict form or R expression `list(c(...))` |
| model | default interaction model / explicit formula |
| batch effects | list → additive model terms + PCA |
| PCA | activate + labels |

Per-sample PE/SE mixing rejected by assert.

## Gap tiers vs the port

**P0**: SRA source mode (get_sra via fasterq-dump); single-end mode
(fastp_se + SE chains); biomaRt symbol mapping (4-mirror fallback chain
— network dependency); arbitrary R-expression contrasts (port pins
declared contrasts? verify scope).

**P1**: none — MIT, all tools OSS, no paid DBs (Ensembl/BioMart free).

**P2**: trimming toggle, PCA activate/labels, contrast/batch/model
config, strandedness column, fastp per-unit adapters, star index/align
passthrough args, ref species/release/build.

Upstream gotchas (do not port): mergeReads.activate is a dead toggle;
pca.labels as bare string is a latent bug (char-wise extend);
get_bioc_species_name assumes `_` in species; test submodule stale.

Gates: Ensembl FTP (pinned release), SRA/ENA for get_sra, biomaRt
mirrors, snakemake wrappers fetched at runtime, bwa_index mem 369GB
(resource gate — index build on the server class).

## Verdict

Compact; the ported default (local PE + trimming + simple contrasts)
leaves SRA/SE sources + biomaRt mapping + expression contrasts as the
main P0. Port scope (24 rules after normalization) matches the upstream
rule count closely — the gap is in the branch axes, not the rule list.

## Re-verification (2026-08-23, light group)

Engine: latest main (post-v0.14.1) · Box: tx-ubuntu · Mode: real CLI
run, not dry-run · `-j 2 --keep-going`.

**56 succeeded, 48 skipped, 0 failed, exit 0**, one round, zero repo
fixes. Coverage chain (all real execution): local reference override
path (the repo's `genome_fasta`/`annotation_gtf` config keys, skipping
the Ensembl download) → fastp → STAR align + GeneCounts → RSeQC →
count matrix → DESeq2 init/contrast → **biomaRt gene2symbol live
Ensembl queries, all three steps passed (65.7s / 48.1s / 57.3s)** →
multiqc. All 48 skips are checkpoint reuse from the earlier round plus
condition gates — no unexpected skips.
