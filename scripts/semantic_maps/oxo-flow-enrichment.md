**oxo-flow-enrichment pipeline**: given region-set BED files and ranked gene lists, it runs region-set and gene-set enrichment (LOLA, GREAT, pycisTarget, RcisTarget, GSEApy ORA and preranked GSEA) against curated databases, delivering per-feature-set plots, per-group summaries, and reproducibility exports.

**1. Database preparation** — `prepare_databases_Azimuth_2023` converts the Azimuth_2023 JSON database to GMT, and `prepare_databases_Reactome` stages the Reactome pathway GMT; these two feed the GREAT, ORA, and preranked analyses below.

**2. Region enrichment** — `region_enrichment_analysis_LOLA` tests each region set for overlap enrichment against the LOLACore database, while `region_enrichment_analysis_GREAT_Azimuth_2023` and `region_enrichment_analysis_GREAT_Reactome` run rGREAT against both prepared databases. `region_gene_association_GREAT` maps each region set to its associated genes.

**3. Gene-level analyses** — the GREAT gene mapping feeds `gene_ORA_GSEApy_Azimuth_2023`, `gene_ORA_GSEApy_Reactome`, and the TFBS motif analysis `gene_motif_enrichment_analysis_RcisTarget`; separately, ranked gene lists feed `gene_preranked_GSEApy_Azimuth_2023` and `gene_preranked_GSEApy_Reactome` (RNA group). Region-side, `region_motif_enrichment_analysis_pycisTarget` runs TFBS motif enrichment and `process_results_pycisTarget` converts it to CSV tables; both motif branches are gated on provided databases.

**4. Per-feature-set plots** — each result CSV is plotted by `plot_enrichment_result_LOLA_LOLACore`, `plot_enrichment_result_GREAT_Azimuth_2023`, `plot_enrichment_result_GREAT_Reactome`, `plot_enrichment_result_pycisTarget_hg38_screen_v10clust`, `plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust`, `plot_enrichment_result_ORA_GSEApy_Azimuth_2023`, `plot_enrichment_result_ORA_GSEApy_Reactome`, `plot_enrichment_result_preranked_GSEApy_Azimuth_2023`, or `plot_enrichment_result_preranked_GSEApy_Reactome`.

**5. Group aggregation and visualization** — in parallel, results consolidate per group (ATAC vs RNA) via aggregate rules such as `aggregate_GREAT_Azimuth_2023_ATAC` and `aggregate_preranked_GSEApy_Reactome_RNA`, whose tables drive the matching summary plots (`visualize_GREAT_Azimuth_2023_ATAC`, `visualize_LOLA_LOLACore_ATAC`). Independent of the chain, `config_export` and `annot_export` copy the effective config and annotation into the results folder for reproducibility.

*Verified: every rule name above is a real rule of `main.oxoflow` (oxo-flow validate); the described order follows the actual rule dependencies.*
