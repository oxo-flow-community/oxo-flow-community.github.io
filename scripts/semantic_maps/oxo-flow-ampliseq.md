## Short names and groups used on this map (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| rename | rename_raw_data_files |
| fastqc | fastqc |
| cutadapt + summary | cutadapt, cutadapt_summary, cutadapt_summary_merge |
| DADA2 QC | dada2_quality_fw, dada2_quality_rv |
| DADA2 trim len | trunclen_fw, trunclen_rv |
| DADA2 filter (+QC out) | dada2_filtntrim, dada2_quality_fw_preprocessed, dada2_quality_rv_preprocessed |
| DADA2 err | dada2_err |
| DADA2 denoise | dada2_denoising |
| DADA2 chimeras | dada2_rmchimera |
| DADA2 stats | dada2_stats, merge_stats |
| DADA2 merge | dada2_merge |
| ITSx | itsx_cutasv, itsxrust_cutasv |
| ITSx filter | filter_len_itsx |
| taxonomy DB | download_taxonomy_db, format_taxonomy |
| taxonomy assign | dada2_taxonomy, dada2_taxonomy_its |
| QIIME2 core pipeline | qiime2_inasv, qiime2_inseq, qiime2_inasv_its, qiime2_inseq_its, qiime2_intax, qiime2_diversity_tree |
| QIIME2 analyses | qiime2_diversity_core, qiime2_classify, qiime2_alphararefaction, qiime2_metadata_categories, qiime2_preptax |
| QIIME2 plots & export | qiime2_barplot, qiime2_export_absolute, qiime2_export_relasv, qiime2_export_reltax |
| QIIME2 comparisons | qiime2_ancom, qiime2_ancombc, qiime2_ancombc2 |
| QIIME2 diversity | qiime2_diversity_alpha, qiime2_diversity_beta, qiime2_diversity_betaord, qiime2_diversity_adonis |
| MultiQC | multiqc |
| PICRUSt | picrust |

Group edges are drawn when at least one member-to-member real edge exists;
each line of the drawing descends from the engine DAG (subset-checked at
generation). Per-rule detail lives in the rule-level card below.
