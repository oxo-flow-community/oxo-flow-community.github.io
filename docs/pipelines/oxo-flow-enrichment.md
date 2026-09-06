---
title: "Region set and gene set enrichment: LOLA, GREAT, pycisTarget and GSEA"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-enrichment</span></div>
<div class="ox-detail-cols">
<div>
<h1>Region set and gene set enrichment: LOLA, GREAT, pycisTarget and GSEA</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>
<p>Run a complete region set and gene set enrichment analysis on your own data: region overlap enrichment (LOLA), genomic region enrichment of annotated terms (rGREAT), region TFBS motif enrichment (pycisTarget), gene TFBS motif enrichment (RcisTarget), and gene over-representation analysis (ORA) and preranked GSEA (GSEApy). Every tool applies its own multiple-test correction; the workflow produces per-set enrichment plots, per-group summary plots, and reproducibility exports (configs/ and envs/). Official port of epigen/enrichment_analysis v3.0.1 with tool versions and commands pinned to the source.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">48</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 10 CPUs / 32 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/epigen/enrichment_analysis">epigen/enrichment_analysis</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v3.0.1</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2293.1"><code>10.48546/workflowhub.workflow.2293.1</code></a></span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs ATAC peak / BAM inputs — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned (conda/mamba at runtime; five environments declared in main.oxoflow, exact pins from upstream)

**Requirements.**

- annotation.csv declaring each feature set (region set or ranked gene set), its path, background, and group
- region BED files, one per region set, plus a background BED (hg38)
- ranked gene list CSVs, one per gene set (gene, score columns)
- gene-set databases for GSEApy ORA: Azimuth_2023.json and ReactomePathways.gmt
- LOLA region database for the genome of interest (e.g. LOLACore hg38)
- pycisTarget cisTarget rankings (.feather) and motif annotation table
- RcisTarget gene-motif rankings (.feather) and motif-to-TF annotation table (optional; both empty by default)
- compute: up to 10 CPUs and 32 GB RAM per rule (defaults: 1 thread / 32 GB per rule; pycisTarget uses 10 threads as upstream)
- disk: modest — enrichment tables, per-set plots, and pycisTarget HDF5 outputs (a few GB)

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli
#    NOTE: bioconda currently ships 0.10.2, older than the >= 0.12.0
#    minimum of every catalog entry — prefer the release binary.

# 2. get this workflow (clones the repo, auto-discovers the workflow,
#    sanity-parses it with the engine)
oxo-flow pull gh:oxo-flow-community/oxo-flow-enrichment
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-enrichment
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. The list below names the rules that read each key.</p>
<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>adjp_cap</code><span class="ox-param-default">4</span></div>
<p class="ox-param-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)</p>
<details class="ox-param-usedby"><summary>used by 9 rules</summary>
<div class="ox-param-rules"><code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code> <code>visualize_LOLA_LOLACore_ATAC</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>adjp_th_GREAT</code><span class="ox-param-default">0.01</span></div>
<p class="ox-param-desc">significance thresholds (upstream adjp_th)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>adjp_th_LOLA</code><span class="ox-param-default">0.01</span></div>
<p class="ox-param-desc">significance thresholds (upstream adjp_th)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>visualize_LOLA_LOLACore_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>adjp_th_ORA_GSEApy</code><span class="ox-param-default">0.05</span></div>
<p class="ox-param-desc">significance thresholds (upstream adjp_th)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>adjp_th_RcisTarget</code><span class="ox-param-default">5</span></div>
<p class="ox-param-desc">significance thresholds (upstream adjp_th)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>adjp_th_preranked_GSEApy</code><span class="ox-param-default">0.05</span></div>
<p class="ox-param-desc">significance thresholds (upstream adjp_th)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>adjp_th_pycisTarget</code><span class="ox-param-default">5</span></div>
<p class="ox-param-desc">significance thresholds (upstream adjp_th)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>all_region_sets</code><span class="ox-param-default">Bcell_open_regions, Ery_open_regions, all_regions</span></div>
<p class="ox-param-desc">feature sets (derived from config/annotation.csv at port time)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>annotation</code><span class="ox-param-default">config/annotation.csv</span></div>
<p class="ox-param-desc">general</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>background_name</code><span class="ox-param-default">all_regions</span></div>
<p class="ox-param-desc">upstream annotation background_name (all region sets)</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>gene_ORA_GSEApy_Azimuth_2023</code> <code>gene_ORA_GSEApy_Reactome</code> <code>gene_motif_enrichment_analysis_RcisTarget</code> <code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_enrichment_analysis_LOLA</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cluster_summary</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)</p>
<details class="ox-param-usedby"><summary>used by 9 rules</summary>
<div class="ox-param-rules"><code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code> <code>visualize_LOLA_LOLACore_ATAC</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_GREAT_adj_pvalue</code><span class="ox-param-default">p_adjust_hyper</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_GREAT_Azimuth_2023</code> <code>plot_enrichment_result_GREAT_Reactome</code> <code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_GREAT_effect_size</code><span class="ox-param-default">fold_enrichment_hyper</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_GREAT_Azimuth_2023</code> <code>plot_enrichment_result_GREAT_Reactome</code> <code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_GREAT_overlap</code><span class="ox-param-default">observed_region_hits</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_GREAT_Azimuth_2023</code> <code>plot_enrichment_result_GREAT_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_GREAT_p_value</code><span class="ox-param-default">p_value_hyper</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_GREAT_Azimuth_2023</code> <code>plot_enrichment_result_GREAT_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_GREAT_term</code><span class="ox-param-default">description</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_GREAT_Azimuth_2023</code> <code>plot_enrichment_result_GREAT_Reactome</code> <code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_GREAT_top_n</code><span class="ox-param-default">25</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_GREAT_Azimuth_2023</code> <code>plot_enrichment_result_GREAT_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_LOLA_adj_pvalue</code><span class="ox-param-default">qValue</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_LOLA_LOLACore</code> <code>visualize_LOLA_LOLACore_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_LOLA_effect_size</code><span class="ox-param-default">oddsRatio</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_LOLA_LOLACore</code> <code>visualize_LOLA_LOLACore_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_LOLA_overlap</code><span class="ox-param-default">support</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_LOLA_LOLACore</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_LOLA_p_value</code><span class="ox-param-default">pValue</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_LOLA_LOLACore</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_LOLA_term</code><span class="ox-param-default">description</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_LOLA_LOLACore</code> <code>visualize_LOLA_LOLACore_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_LOLA_top_n</code><span class="ox-param-default">25</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_LOLA_LOLACore</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_ORA_GSEApy_adj_pvalue</code><span class="ox-param-default">Adjusted_P_value</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_ORA_GSEApy_Reactome</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_ORA_GSEApy_effect_size</code><span class="ox-param-default">Odds_Ratio</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_ORA_GSEApy_Reactome</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_ORA_GSEApy_overlap</code><span class="ox-param-default">Overlap</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_ORA_GSEApy_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_ORA_GSEApy_p_value</code><span class="ox-param-default">P_value</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_ORA_GSEApy_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_ORA_GSEApy_term</code><span class="ox-param-default">Term</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_ORA_GSEApy_Reactome</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_ORA_GSEApy_top_n</code><span class="ox-param-default">25</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_ORA_GSEApy_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_RcisTarget_adj_pvalue</code><span class="ox-param-default">NES</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_RcisTarget_effect_size</code><span class="ox-param-default">NES</span></div>
<p class="ox-param-desc">NES combines significance and effect size</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_RcisTarget_overlap</code><span class="ox-param-default">nEnrGenes</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_RcisTarget_p_value</code><span class="ox-param-default">AUC</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_RcisTarget_term</code><span class="ox-param-default">description</span></div>
<p class="ox-param-desc">motif name + highConfCat TFs</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_RcisTarget_top_n</code><span class="ox-param-default">25</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_preranked_GSEApy_adj_pvalue</code><span class="ox-param-default">FDR_q_val</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_preranked_GSEApy_Reactome</code> <code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_preranked_GSEApy_effect_size</code><span class="ox-param-default">NES</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_preranked_GSEApy_Reactome</code> <code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_preranked_GSEApy_overlap</code><span class="ox-param-default">Tag</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_preranked_GSEApy_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_preranked_GSEApy_p_value</code><span class="ox-param-default">NOM_p_val</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_preranked_GSEApy_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_preranked_GSEApy_term</code><span class="ox-param-default">Term</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_preranked_GSEApy_Reactome</code> <code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_preranked_GSEApy_top_n</code><span class="ox-param-default">25</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_preranked_GSEApy_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_pycisTarget_adj_pvalue</code><span class="ox-param-default">NES</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_pycisTarget_effect_size</code><span class="ox-param-default">NES</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_pycisTarget_overlap</code><span class="ox-param-default">Motif_hits</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_pycisTarget_p_value</code><span class="ox-param-default">AUC</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_pycisTarget_term</code><span class="ox-param-default">description</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cn_pycisTarget_top_n</code><span class="ox-param-default">25</span></div>
<p class="ox-param-desc">tool-specific column names (upstream column_names)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>db_Azimuth_2023</code><span class="ox-param-default">test/resources/enrichment_analysis/Azimuth_2023.json</span></div>
<p class="ox-param-desc">databases (upstream local_databases / lola_databases)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>prepare_databases_Azimuth_2023</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>db_Reactome</code><span class="ox-param-default">test/resources/enrichment_analysis/ReactomePathways.gmt</span></div>
<p class="ox-param-desc">databases (upstream local_databases / lola_databases)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>prepare_databases_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>genome</code><span class="ox-param-default">hg38</span></div>
<p class="ox-param-desc">general</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_enrichment_analysis_LOLA</code> <code>region_gene_association_GREAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>great_basal_downstream</code><span class="ox-param-default">1000</span></div>
<p class="ox-param-desc">GREAT parameters (upstream great_parameters)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_gene_association_GREAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>great_basal_upstream</code><span class="ox-param-default">5000</span></div>
<p class="ox-param-desc">GREAT parameters (upstream great_parameters)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_gene_association_GREAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>great_extension</code><span class="ox-param-default">1000000</span></div>
<p class="ox-param-desc">GREAT parameters (upstream great_parameters)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_gene_association_GREAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>great_map_associated_regions</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">GREAT parameters (upstream great_parameters)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>great_min_gene_set_size</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">GREAT parameters (upstream great_parameters)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_gene_association_GREAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>great_mode</code><span class="ox-param-default">basalPlusExt</span></div>
<p class="ox-param-desc">GREAT parameters (upstream great_parameters)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_gene_association_GREAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>lola_db_LOLACore</code><span class="ox-param-default">test/resources/LOLACore/hg38</span></div>
<p class="ox-param-desc">databases (upstream local_databases / lola_databases)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_LOLA</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>nes_cap</code><span class="ox-param-default">5</span></div>
<p class="ox-param-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>or_cap</code><span class="ox-param-default">5</span></div>
<p class="ox-param-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code> <code>visualize_LOLA_LOLACore_ATAC</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>path_to_motif_annotations</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">user-provided motif annotation tbl; &quot;&quot; disables motif enrichment</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>aggregate_pycisTarget_hg38_screen_v10clust_ATAC</code> <code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code> <code>process_results_pycisTarget</code> <code>region_motif_enrichment_analysis_pycisTarget</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>project_name</code><span class="ox-param-default">Corces_CellTypes</span></div>
<p class="ox-param-desc">general</p>
<details class="ox-param-usedby"><summary>used by 11 rules</summary>
<div class="ox-param-rules"><code>annot_export</code> <code>config_export</code> <code>gene_ORA_GSEApy_Azimuth_2023</code> <code>gene_ORA_GSEApy_Reactome</code> <code>gene_preranked_GSEApy_Azimuth_2023</code> <code>gene_preranked_GSEApy_Reactome</code> <code>prepare_databases_Azimuth_2023</code> <code>prepare_databases_Reactome</code> <code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_gene_association_GREAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_annotation_version</code><span class="ox-param-default">v10nr_clust</span></div>
<p class="ox-param-desc">pycisTarget parameters (upstream pycistarget_parameters)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_annotations_to_use</code><span class="ox-param-default">[&#x27;Direct_annot&#x27;, &#x27;Motif_similarity_annot&#x27;, &#x27;Orthology_annot&#x27;, &#x27;Motif_similarity_and_Orthology_annot&#x27;]</span></div>
<p class="ox-param-desc">upstream passes the python list literal; kept as a string so the rendered<br>command is byte-identical to upstream&#x27;s</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_auc_threshold</code><span class="ox-param-default">0.005</span></div>
<p class="ox-param-desc">pycisTarget parameters (upstream pycistarget_parameters)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_db_hg38_screen_v10clust</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">user-provided pycisTarget rankings DB; &quot;&quot; disables motif enrichment</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>aggregate_pycisTarget_hg38_screen_v10clust_ATAC</code> <code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code> <code>process_results_pycisTarget</code> <code>region_motif_enrichment_analysis_pycisTarget</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_fraction_overlap_w_cistarget_database</code><span class="ox-param-default">0.4</span></div>
<p class="ox-param-desc">pycisTarget parameters (upstream pycistarget_parameters)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_motif_similarity_fdr</code><span class="ox-param-default">0.001</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_nes_threshold</code><span class="ox-param-default">3</span></div>
<p class="ox-param-desc">pycisTarget parameters (upstream pycistarget_parameters)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_orthologous_identity_threshold</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_rank_threshold</code><span class="ox-param-default">0.05</span></div>
<p class="ox-param-desc">pycisTarget parameters (upstream pycistarget_parameters)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pycistarget_term_col</code><span class="ox-param-default">Direct_annot</span></div>
<p class="ox-param-desc">first entry of annotations_to_use</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>process_results_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_aucMaxRank_factor</code><span class="ox-param-default">0.05</span></div>
<p class="ox-param-desc">aucMaxRank = factor * ncol(motifRankings)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gene_motif_enrichment_analysis_RcisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_db_hg38_500bp_up_100bp_down_v10clust</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">gene-based TFBS motif enrichment (RcisTarget); &quot;&quot; disables both rules,<br>matching upstream&#x27;s &quot;to skip you have to leave one database entry with an<br>empty path&quot; convention</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>aggregate_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>gene_motif_enrichment_analysis_RcisTarget</code> <code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_geneErnMaxRank</code><span class="ox-param-default">5000</span></div>
<p class="ox-param-desc">rcistarget tool parameter (upstream --rcistarget_geneErnMaxRank) <span class="ox-param-inferred">inferred</span></p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gene_motif_enrichment_analysis_RcisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_geneErnMethod</code><span class="ox-param-default">aprox</span></div>
<p class="ox-param-desc">alternatively exact but more intense: &quot;icistarget&quot;</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gene_motif_enrichment_analysis_RcisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_motifAnnot_highConfCat</code><span class="ox-param-default">directAnnotation,inferredBy_Orthology</span></div>
<p class="ox-param-desc">upstream python lists; comma-joined so the rendered command stays a single<br>token (values contain no commas)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gene_motif_enrichment_analysis_RcisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_motifAnnot_lowConfCat</code><span class="ox-param-default">inferredBy_MotifSimilarity,inferredBy_MotifSimilarity_n_Orthology</span></div>
<p class="ox-param-desc">upstream python lists; comma-joined so the rendered command stays a single<br>token (values contain no commas)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gene_motif_enrichment_analysis_RcisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_motif_annot</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">user-provided motif-to-TF annotation tbl; &quot;&quot; disables</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>aggregate_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>gene_motif_enrichment_analysis_RcisTarget</code> <code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rcistarget_nesThreshold</code><span class="ox-param-default">3</span></div>
<p class="ox-param-desc">upstream python lists; comma-joined so the rendered command stays a single<br>token (values contain no commas)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gene_motif_enrichment_analysis_RcisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>region_beds</code><span class="ox-param-default">test/data/CorcesATAC</span></div>
<p class="ox-param-desc">feature sets (derived from config/annotation.csv at port time)</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_enrichment_analysis_LOLA</code> <code>region_gene_association_GREAT</code> <code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>region_sets</code><span class="ox-param-default">Bcell_open_regions, Ery_open_regions</span></div>
<p class="ox-param-desc">feature sets (derived from config/annotation.csv at port time)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>result_path</code><span class="ox-param-default">test/results/enrichment_analysis</span></div>
<p class="ox-param-desc">general</p>
<details class="ox-param-usedby"><summary>used by 40 rules</summary>
<div class="ox-param-rules"><code>aggregate_GREAT_Azimuth_2023_ATAC</code> <code>aggregate_GREAT_Reactome_ATAC</code> <code>aggregate_LOLA_LOLACore_ATAC</code> <code>aggregate_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>aggregate_ORA_GSEApy_Reactome_ATAC</code> <code>aggregate_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>aggregate_preranked_GSEApy_Azimuth_2023_RNA</code> <code>aggregate_preranked_GSEApy_Reactome_RNA</code> <code>aggregate_pycisTarget_hg38_screen_v10clust_ATAC</code> <code>annot_export</code> <code>config_export</code> <code>gene_ORA_GSEApy_Azimuth_2023</code> <code>gene_ORA_GSEApy_Reactome</code> <code>gene_motif_enrichment_analysis_RcisTarget</code> <code>gene_preranked_GSEApy_Azimuth_2023</code> <code>gene_preranked_GSEApy_Reactome</code> <code>plot_enrichment_result_GREAT_Azimuth_2023</code> <code>plot_enrichment_result_GREAT_Reactome</code> <code>plot_enrichment_result_LOLA_LOLACore</code> <code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_ORA_GSEApy_Reactome</code> <code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code> <code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code> <code>plot_enrichment_result_preranked_GSEApy_Reactome</code> <code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code> <code>process_results_pycisTarget</code> <code>region_enrichment_analysis_GREAT_Azimuth_2023</code> <code>region_enrichment_analysis_GREAT_Reactome</code> <code>region_enrichment_analysis_LOLA</code> <code>region_gene_association_GREAT</code> <code>region_motif_enrichment_analysis_pycisTarget</code> <code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code> <code>visualize_LOLA_LOLACore_ATAC</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rnk_dir</code><span class="ox-param-default">test/data/CorcesRNA</span></div>
<p class="ox-param-desc">{gene_set}.csv per entry of rnk_sets</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>gene_preranked_GSEApy_Azimuth_2023</code> <code>gene_preranked_GSEApy_Reactome</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>rnk_sets</code><span class="ox-param-default">Bcell_ranked, Ery_ranked</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>species</code><span class="ox-param-default">homo_sapiens</span></div>
<p class="ox-param-desc">upstream derives species from genome (hg19/hg38 -&gt; homo_sapiens); ported as config key</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>region_motif_enrichment_analysis_pycisTarget</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>top_terms_n</code><span class="ox-param-default">5</span></div>
<p class="ox-param-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)</p>
<details class="ox-param-usedby"><summary>used by 9 rules</summary>
<div class="ox-param-rules"><code>visualize_GREAT_Azimuth_2023_ATAC</code> <code>visualize_GREAT_Reactome_ATAC</code> <code>visualize_LOLA_LOLACore_ATAC</code> <code>visualize_ORA_GSEApy_Azimuth_2023_ATAC</code> <code>visualize_ORA_GSEApy_Reactome_ATAC</code> <code>visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC</code> <code>visualize_preranked_GSEApy_Azimuth_2023_RNA</code> <code>visualize_preranked_GSEApy_Reactome_RNA</code> <code>visualize_pycisTarget_hg38_screen_v10clust_ATAC</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-enrichment pipeline overview](../assets/dag/oxo-flow-enrichment.svg)

<p class="ox-dag-caption">figure · oxo-flow-enrichment — Run a complete region set and gene set enrichment analysis on your own data: region overlap enrichment (LOLA), genomic region enrichment of annotated terms (rGREAT), region TFBS motif enrichment (pycisTarget), gene TFBS motif enrichment (RcisTarget), and gene over-representation analysis (ORA) and preranked GSEA (GSEApy).</p>

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or module overview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- aggregate_GREAT_Azimuth_2023_ATAC
- aggregate_GREAT_Reactome_ATAC
- aggregate_LOLA_LOLACore_ATAC
- aggregate_ORA_GSEApy_Azimuth_2023_ATAC
- aggregate_ORA_GSEApy_Reactome_ATAC
- aggregate_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC
- aggregate_preranked_GSEApy_Azimuth_2023_RNA
- aggregate_preranked_GSEApy_Reactome_RNA
- aggregate_pycisTarget_hg38_screen_v10clust_ATAC
- annot_export
- config_export
- gene_ORA_GSEApy_Azimuth_2023
- gene_ORA_GSEApy_Azimuth_2023_txt
- gene_ORA_GSEApy_Reactome
- gene_ORA_GSEApy_Reactome_txt
- gene_motif_enrichment_analysis_RcisTarget
- gene_motif_enrichment_analysis_RcisTarget_txt
- gene_preranked_GSEApy_Azimuth_2023
- gene_preranked_GSEApy_Reactome
- plot_enrichment_result_GREAT_Azimuth_2023
- plot_enrichment_result_GREAT_Reactome
- plot_enrichment_result_LOLA_LOLACore
- plot_enrichment_result_ORA_GSEApy_Azimuth_2023
- plot_enrichment_result_ORA_GSEApy_Azimuth_2023_txt
- plot_enrichment_result_ORA_GSEApy_Reactome
- plot_enrichment_result_ORA_GSEApy_Reactome_txt
- plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust
- plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust_txt
- plot_enrichment_result_preranked_GSEApy_Azimuth_2023
- plot_enrichment_result_preranked_GSEApy_Reactome
- plot_enrichment_result_pycisTarget_hg38_screen_v10clust
- prepare_databases_Azimuth_2023
- prepare_databases_Reactome
- process_results_pycisTarget
- region_enrichment_analysis_GREAT_Azimuth_2023
- region_enrichment_analysis_GREAT_Reactome
- region_enrichment_analysis_LOLA
- region_gene_association_GREAT
- region_motif_enrichment_analysis_pycisTarget
- visualize_GREAT_Azimuth_2023_ATAC
- visualize_GREAT_Reactome_ATAC
- visualize_LOLA_LOLACore_ATAC
- visualize_ORA_GSEApy_Azimuth_2023_ATAC
- visualize_ORA_GSEApy_Reactome_ATAC
- visualize_RcisTarget_hg38_500bp_up_100bp_down_v10clust_ATAC
- visualize_preranked_GSEApy_Azimuth_2023_RNA
- visualize_preranked_GSEApy_Reactome_RNA
- visualize_pycisTarget_hg38_screen_v10clust_ATAC

**Excluded**

- env_export — conda env export requires the conda CLI inside the runtime environment and dumps the runtime env state, not the declared pins; exact pins are already declared in envs/*.yaml
- report rendering — upstream renders an HTML report via snakemake's report() wrapping outputs with .rst captions, categories and labels; the captions half is ported as `report` annotations on all 23 wrapped rules (needs engine 0.17.0+, rendered by the rule-captions report section), while the artifact-catalog book form (self-contained HTML, figures embedded, categories/labels) has no oxo-flow equivalent and remains unported

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- note: the anticipated names liftover/enrichr/gost/single_region_mode do not exist in v3.0.1 (Enrichr appears only as a commented-out reference in gene_ORA_GSEApy.py and a database-source comment in config.yaml)

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| prepare_databases | `prepare_databases_Azimuth_2023`, `prepare_databases_Reactome` | gseapy 1.1.3 | identical command; database fan-out baked as static blocks (2 default-path databases) |
| region_enrichment_analysis_LOLA | `region_enrichment_analysis_LOLA` | bioconductor-lola 1.32.0 | identical command; database fan-out baked as static block (1 default-path database) |
| region_enrichment_analysis_GREAT | `region_enrichment_analysis_GREAT_Azimuth_2023`, `region_enrichment_analysis_GREAT_Reactome` | bioconductor-rgreat 2.4.0 | identical command; upstream `great_parameters` nested dict flattened into `great_*` config keys |
| region_gene_association_GREAT | `region_gene_association_GREAT` | bioconductor-rgreat 2.4.0 | identical command; uses the first database (Azimuth_2023) as upstream |
| region_motif_enrichment_analysis_pycisTarget | `region_motif_enrichment_analysis_pycisTarget` | pycistarget 1.1 | command text verbatim (incl. upstream error-tolerance wrapper); threads=10 as upstream |
| process_results_pycisTarget | `process_results_pycisTarget` | pycistarget 1.1 | identical command |
| gene_motif_enrichment_analysis_RcisTarget | `gene_motif_enrichment_analysis_RcisTarget` (+ `_txt`) + plot/aggregate/visualize `*_RcisTarget_*` blocks | bioconductor-rcistarget 1.20.0 | identical command/logic; when-gated on the user-provided rankings feather + motif annotation (both `""` by default); fans over region sets (via GREAT `genes.txt`) and `.txt` gene sets (`config.txt_gene_sets`; zero instances when the default-empty list is unset, so the default plan is unchanged); upstream also folds the `.txt`-set results into the group aggregate/visualize — the port's static per-group blocks cannot enumerate user-defined gene sets, so txt-set results stop at per-set plots |
| gene_ORA_GSEApy | `gene_ORA_GSEApy_Azimuth_2023`, `gene_ORA_GSEApy_Reactome` | gseapy 1.1.3 | identical command; upstream genes_dict fan-out has zero default-path members, region-set fan-out kept |
| gene_preranked_GSEApy | `gene_preranked_GSEApy_Azimuth_2023`, `gene_preranked_GSEApy_Reactome` | gseapy 1.1.3 | identical command |
| plot_enrichment_result | `plot_enrichment_result_*` (9 blocks) | r-ggplot2 3.5.0, r-svglite 2.1.0 | identical command; upstream wildcard fan-out (tool × db × feature_set) baked as per-(tool,db) scatter blocks |
| aggregate | `aggregate_*` (9 blocks) | pandas 1.1.4 / 1.5.3 | identical logic; upstream wildcards group/tool/db passed as CLI args |
| visualize | `visualize_*` (9 blocks) | r-ggplot2 3.5.0, r-pheatmap 1.0.12 | identical command/logic; `cluster_summary` config key kept as upstream numeric flag |
| config_export | `config_export` | — | upstream dumps the in-memory config dict; the port copies `config/config.yaml` (effective-config mirror) |
| annot_export | `annot_export` | — | identical command |
| env_export | not ported | — | `conda env export` needs the conda CLI inside the runtime env; exact pins are already declared in `envs/*.yaml` |
| report rendering | not ported | — | oxo-flow has no report module; `config_export` / `annot_export` are ported as plain rules (`env_export` is excluded separately — see the row above) |

Script ports: upstream scripts run inside snakemake's `snakemake@input/...`
namespace; the port passes the same values as positional CLI arguments
(`scripts/*`), keeping every analysis step and output byte-identical.
`utils.R` is copied verbatim. Fidelity conventions: `{config.a.b}` nested
access does not exist in oxo-flow — all upstream nested config dicts
(`great_parameters`, `pycistarget_parameters`, `rcistarget_parameters`,
`column_names`, `adjp_th`, caps) are flattened into prefixed top-level
keys; the pycisTarget `annotations_to_use` list is carried as a python-list
literal string, and the RcisTarget `motifAnnot_highConfCat` /
`motifAnnot_lowConfCat` lists are comma-joined strings (values contain no
commas; split back to vectors inside the R script), so the rendered
commands are byte-identical to upstream.


## Links

- Repository: [oxo-flow-enrichment](https://github.com/oxo-flow-community/oxo-flow-enrichment)
- Upstream: [epigen/enrichment_analysis](https://github.com/epigen/enrichment_analysis) @ `v3.0.1`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
