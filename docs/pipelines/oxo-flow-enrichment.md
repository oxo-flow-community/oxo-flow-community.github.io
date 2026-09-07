---
title: "Region set and gene set enrichment: LOLA, GREAT, pycisTarget and GSEA"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-enrichment</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Region set and gene set enrichment: LOLA, GREAT, pycisTarget and GSEA</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">region-enrichment</span><span class="ox-tag">gene-set-enrichment</span><span class="ox-tag">LOLA</span><span class="ox-tag">GREAT</span><span class="ox-tag">pycisTarget</span><span class="ox-tag">RcisTarget</span><span class="ox-tag">GSEApy</span><span class="ox-tag">GSEA</span><span class="ox-tag">ORA</span><span class="ox-tag">snakemake</span></div>
<p class="ox-desc">Run a complete region set and gene set enrichment analysis on your own data: region overlap enrichment (LOLA), genomic region enrichment of annotated terms (rGREAT), region TFBS motif enrichment (pycisTarget), gene TFBS motif enrichment (RcisTarget), and gene over-representation analysis (ORA) and preranked GSEA (GSEApy). Every tool applies its own multiple-test correction; the workflow produces per-set enrichment plots, per-group summary plots, and reproducibility exports (configs/ and envs/). Official port of epigen/enrichment_analysis v3.0.1 with tool versions and commands pinned to the source.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-enrichment" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">42</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 10 CPUs / 32 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/epigen/enrichment_analysis">epigen/enrichment_analysis</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v3.0.1</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2293.1"><code>10.48546/workflowhub.workflow.2293.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">gseapy</span><span class="tchip">pandas</span><span class="tchip">pycistarget</span><span class="tchip">bioconductor-rcistarget</span><span class="tchip">bioconductor-lola</span><span class="tchip">bioconductor-rgreat</span><span class="tchip">r-base</span><span class="tchip">r-ggplot2</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>oxo-flow-enrichment pipeline</strong>: given region-set BED files and ranked gene lists, it runs region-set and gene-set enrichment (LOLA, GREAT, pycisTarget, RcisTarget, GSEApy ORA and preranked GSEA) against curated databases, delivering per-feature-set plots, per-group summaries, and reproducibility exports.</p>
<p><strong>1. Database preparation</strong> — <code>prepare_databases_Azimuth_2023</code> converts the Azimuth_2023 JSON database to GMT, and <code>prepare_databases_Reactome</code> stages the Reactome pathway GMT; these two feed the GREAT, ORA, and preranked analyses below.</p>
<p><strong>2. Region enrichment</strong> — <code>region_enrichment_analysis_LOLA</code> tests each region set for overlap enrichment against the LOLACore database, while <code>region_enrichment_analysis_GREAT_Azimuth_2023</code> and <code>region_enrichment_analysis_GREAT_Reactome</code> run rGREAT against both prepared databases. <code>region_gene_association_GREAT</code> maps each region set to its associated genes.</p>
<p><strong>3. Gene-level analyses</strong> — the GREAT gene mapping feeds <code>gene_ORA_GSEApy_Azimuth_2023</code>, <code>gene_ORA_GSEApy_Reactome</code>, and the TFBS motif analysis <code>gene_motif_enrichment_analysis_RcisTarget</code>; separately, ranked gene lists feed <code>gene_preranked_GSEApy_Azimuth_2023</code> and <code>gene_preranked_GSEApy_Reactome</code> (RNA group). Region-side, <code>region_motif_enrichment_analysis_pycisTarget</code> runs TFBS motif enrichment and <code>process_results_pycisTarget</code> converts it to CSV tables; both motif branches are gated on provided databases.</p>
<p><strong>4. Per-feature-set plots</strong> — each result CSV is plotted by <code>plot_enrichment_result_LOLA_LOLACore</code>, <code>plot_enrichment_result_GREAT_Azimuth_2023</code>, <code>plot_enrichment_result_GREAT_Reactome</code>, <code>plot_enrichment_result_pycisTarget_hg38_screen_v10clust</code>, <code>plot_enrichment_result_RcisTarget_hg38_500bp_up_100bp_down_v10clust</code>, <code>plot_enrichment_result_ORA_GSEApy_Azimuth_2023</code>, <code>plot_enrichment_result_ORA_GSEApy_Reactome</code>, <code>plot_enrichment_result_preranked_GSEApy_Azimuth_2023</code>, or <code>plot_enrichment_result_preranked_GSEApy_Reactome</code>.</p>
<p><strong>5. Group aggregation and visualization</strong> — in parallel, results consolidate per group (ATAC vs RNA) via aggregate rules such as <code>aggregate_GREAT_Azimuth_2023_ATAC</code> and <code>aggregate_preranked_GSEApy_Reactome_RNA</code>, whose tables drive the matching summary plots (<code>visualize_GREAT_Azimuth_2023_ATAC</code>, <code>visualize_LOLA_LOLACore_ATAC</code>). Independent of the chain, <code>config_export</code> and <code>annot_export</code> copy the effective config and annotation into the results folder for reproducibility.</p>
<p><em>Verified: every rule name above is a real rule of <code>main.oxoflow</code> (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-enrichment+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>


<div class="ox-tryit">
<div class="ox-tryit-title">⬡ Try it — clone &amp; run</div>
<pre class="ox-tryit-cmd" data-copy="git clone https://github.com/oxo-flow-community/oxo-flow-enrichment.git &amp;&amp; cd oxo-flow-enrichment &amp;&amp; oxo-flow run main.oxoflow">git clone https://github.com/oxo-flow-community/oxo-flow-enrichment.git
cd oxo-flow-enrichment
oxo-flow run main.oxoflow</pre>
<p class="ox-tryit-note">The repository ships test fixtures (e.g. <code>test/data/CorcesATAC/Bcell_open_regions.bed</code>, <code>test/data/CorcesATAC/Ery_open_regions.bed</code>, <code>test/data/CorcesATAC/all_regions.bed</code>, <code>test/data/CorcesRNA/Bcell_ranked.csv</code>) — point <code>input</code> at them or use the built-in sample group to <code>dry-run</code> first.</p>
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

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adjp_cap = value" data-copy="adjp_cap = 4">adjp_cap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>4</code></td>
<td class="ox-p-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adjp_th_GREAT = value" data-copy="adjp_th_GREAT = 0.01">adjp_th_GREAT</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.01</code></td>
<td class="ox-p-desc">significance thresholds (upstream adjp_th)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adjp_th_LOLA = value" data-copy="adjp_th_LOLA = 0.01">adjp_th_LOLA</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.01</code></td>
<td class="ox-p-desc">significance thresholds (upstream adjp_th)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adjp_th_ORA_GSEApy = value" data-copy="adjp_th_ORA_GSEApy = 0.05">adjp_th_ORA_GSEApy</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.05</code></td>
<td class="ox-p-desc">significance thresholds (upstream adjp_th)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adjp_th_RcisTarget = value" data-copy="adjp_th_RcisTarget = 5">adjp_th_RcisTarget</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">significance thresholds (upstream adjp_th)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adjp_th_preranked_GSEApy = value" data-copy="adjp_th_preranked_GSEApy = 0.05">adjp_th_preranked_GSEApy</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.05</code></td>
<td class="ox-p-desc">significance thresholds (upstream adjp_th)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adjp_th_pycisTarget = value" data-copy="adjp_th_pycisTarget = 5">adjp_th_pycisTarget</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">significance thresholds (upstream adjp_th)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy all_region_sets = value" data-copy="all_region_sets = Bcell_open_regions, Ery_open_regions, all_regions">all_region_sets</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>Bcell_open_regions, Ery_open_regions, all_regions</code></td>
<td class="ox-p-desc">feature sets (derived from config/annotation.csv at port time)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy annotation = value" data-copy="annotation = config/annotation.csv">annotation</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>config/annotation.csv</code></td>
<td class="ox-p-desc">general<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy background_name = value" data-copy="background_name = all_regions">background_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>all_regions</code></td>
<td class="ox-p-desc">upstream annotation background_name (all region sets)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cluster_summary = value" data-copy="cluster_summary = 1">cluster_summary</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_GREAT_adj_pvalue = value" data-copy="cn_GREAT_adj_pvalue = p_adjust_hyper">cn_GREAT_adj_pvalue</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>p_adjust_hyper</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_GREAT_effect_size = value" data-copy="cn_GREAT_effect_size = fold_enrichment_hyper">cn_GREAT_effect_size</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>fold_enrichment_hyper</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_GREAT_overlap = value" data-copy="cn_GREAT_overlap = observed_region_hits">cn_GREAT_overlap</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>observed_region_hits</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_GREAT_p_value = value" data-copy="cn_GREAT_p_value = p_value_hyper">cn_GREAT_p_value</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>p_value_hyper</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_GREAT_term = value" data-copy="cn_GREAT_term = description">cn_GREAT_term</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>description</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_GREAT_top_n = value" data-copy="cn_GREAT_top_n = 25">cn_GREAT_top_n</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>25</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_LOLA_adj_pvalue = value" data-copy="cn_LOLA_adj_pvalue = qValue">cn_LOLA_adj_pvalue</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>qValue</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_LOLA_effect_size = value" data-copy="cn_LOLA_effect_size = oddsRatio">cn_LOLA_effect_size</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>oddsRatio</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_LOLA_overlap = value" data-copy="cn_LOLA_overlap = support">cn_LOLA_overlap</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>support</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_LOLA_p_value = value" data-copy="cn_LOLA_p_value = pValue">cn_LOLA_p_value</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>pValue</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_LOLA_term = value" data-copy="cn_LOLA_term = description">cn_LOLA_term</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>description</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_LOLA_top_n = value" data-copy="cn_LOLA_top_n = 25">cn_LOLA_top_n</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>25</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_ORA_GSEApy_adj_pvalue = value" data-copy="cn_ORA_GSEApy_adj_pvalue = Adjusted_P_value">cn_ORA_GSEApy_adj_pvalue</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Adjusted_P_value</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_ORA_GSEApy_effect_size = value" data-copy="cn_ORA_GSEApy_effect_size = Odds_Ratio">cn_ORA_GSEApy_effect_size</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Odds_Ratio</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_ORA_GSEApy_overlap = value" data-copy="cn_ORA_GSEApy_overlap = Overlap">cn_ORA_GSEApy_overlap</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Overlap</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_ORA_GSEApy_p_value = value" data-copy="cn_ORA_GSEApy_p_value = P_value">cn_ORA_GSEApy_p_value</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>P_value</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_ORA_GSEApy_term = value" data-copy="cn_ORA_GSEApy_term = Term">cn_ORA_GSEApy_term</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Term</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_ORA_GSEApy_top_n = value" data-copy="cn_ORA_GSEApy_top_n = 25">cn_ORA_GSEApy_top_n</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>25</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_RcisTarget_adj_pvalue = value" data-copy="cn_RcisTarget_adj_pvalue = NES">cn_RcisTarget_adj_pvalue</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NES</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_RcisTarget_effect_size = value" data-copy="cn_RcisTarget_effect_size = NES">cn_RcisTarget_effect_size</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NES</code></td>
<td class="ox-p-desc">NES combines significance and effect size<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_RcisTarget_overlap = value" data-copy="cn_RcisTarget_overlap = nEnrGenes">cn_RcisTarget_overlap</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>nEnrGenes</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_RcisTarget_p_value = value" data-copy="cn_RcisTarget_p_value = AUC">cn_RcisTarget_p_value</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>AUC</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_RcisTarget_term = value" data-copy="cn_RcisTarget_term = description">cn_RcisTarget_term</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>description</code></td>
<td class="ox-p-desc">motif name + highConfCat TFs<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_RcisTarget_top_n = value" data-copy="cn_RcisTarget_top_n = 25">cn_RcisTarget_top_n</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>25</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_preranked_GSEApy_adj_pvalue = value" data-copy="cn_preranked_GSEApy_adj_pvalue = FDR_q_val">cn_preranked_GSEApy_adj_pvalue</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>FDR_q_val</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_preranked_GSEApy_effect_size = value" data-copy="cn_preranked_GSEApy_effect_size = NES">cn_preranked_GSEApy_effect_size</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NES</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_preranked_GSEApy_overlap = value" data-copy="cn_preranked_GSEApy_overlap = Tag">cn_preranked_GSEApy_overlap</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Tag</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_preranked_GSEApy_p_value = value" data-copy="cn_preranked_GSEApy_p_value = NOM_p_val">cn_preranked_GSEApy_p_value</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NOM_p_val</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_preranked_GSEApy_term = value" data-copy="cn_preranked_GSEApy_term = Term">cn_preranked_GSEApy_term</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Term</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_preranked_GSEApy_top_n = value" data-copy="cn_preranked_GSEApy_top_n = 25">cn_preranked_GSEApy_top_n</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>25</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_pycisTarget_adj_pvalue = value" data-copy="cn_pycisTarget_adj_pvalue = NES">cn_pycisTarget_adj_pvalue</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NES</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_pycisTarget_effect_size = value" data-copy="cn_pycisTarget_effect_size = NES">cn_pycisTarget_effect_size</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NES</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_pycisTarget_overlap = value" data-copy="cn_pycisTarget_overlap = Motif_hits">cn_pycisTarget_overlap</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Motif_hits</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_pycisTarget_p_value = value" data-copy="cn_pycisTarget_p_value = AUC">cn_pycisTarget_p_value</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>AUC</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_pycisTarget_term = value" data-copy="cn_pycisTarget_term = description">cn_pycisTarget_term</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>description</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cn_pycisTarget_top_n = value" data-copy="cn_pycisTarget_top_n = 25">cn_pycisTarget_top_n</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>25</code></td>
<td class="ox-p-desc">tool-specific column names (upstream column_names)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy db_Azimuth_2023 = value" data-copy="db_Azimuth_2023 = test/resources/enrichment_analysis/Azimuth_2023.json">db_Azimuth_2023</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/resources/enrichment_analysis/Azimuth_2023.json</code></td>
<td class="ox-p-desc">databases (upstream local_databases / lola_databases)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy db_Reactome = value" data-copy="db_Reactome = test/resources/enrichment_analysis/ReactomePathways.gmt">db_Reactome</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/resources/enrichment_analysis/ReactomePathways.gmt</code></td>
<td class="ox-p-desc">databases (upstream local_databases / lola_databases)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genome = value" data-copy="genome = hg38">genome</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>hg38</code></td>
<td class="ox-p-desc">general<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy great_basal_downstream = value" data-copy="great_basal_downstream = 1000">great_basal_downstream</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000</code></td>
<td class="ox-p-desc">GREAT parameters (upstream great_parameters)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy great_basal_upstream = value" data-copy="great_basal_upstream = 5000">great_basal_upstream</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5000</code></td>
<td class="ox-p-desc">GREAT parameters (upstream great_parameters)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy great_extension = value" data-copy="great_extension = 1000000">great_extension</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000000</code></td>
<td class="ox-p-desc">GREAT parameters (upstream great_parameters)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy great_map_associated_regions = value" data-copy="great_map_associated_regions = 1">great_map_associated_regions</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">GREAT parameters (upstream great_parameters)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy great_min_gene_set_size = value" data-copy="great_min_gene_set_size = 0">great_min_gene_set_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">GREAT parameters (upstream great_parameters)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy great_mode = value" data-copy="great_mode = basalPlusExt">great_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>basalPlusExt</code></td>
<td class="ox-p-desc">GREAT parameters (upstream great_parameters)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy lola_db_LOLACore = value" data-copy="lola_db_LOLACore = test/resources/LOLACore/hg38">lola_db_LOLACore</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/resources/LOLACore/hg38</code></td>
<td class="ox-p-desc">databases (upstream local_databases / lola_databases)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nes_cap = value" data-copy="nes_cap = 5">nes_cap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy or_cap = value" data-copy="or_cap = 5">or_cap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy path_to_motif_annotations = value" data-copy="path_to_motif_annotations = ">path_to_motif_annotations</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">user-provided motif annotation tbl; &quot;&quot; disables motif enrichment<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy project_name = value" data-copy="project_name = Corces_CellTypes">project_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Corces_CellTypes</code></td>
<td class="ox-p-desc">general<br><span class="ox-param-usedby">used by <code>11</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_annotation_version = value" data-copy="pycistarget_annotation_version = v10nr_clust">pycistarget_annotation_version</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>v10nr_clust</code></td>
<td class="ox-p-desc">pycisTarget parameters (upstream pycistarget_parameters)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_annotations_to_use = value" data-copy="pycistarget_annotations_to_use = [&#x27;Direct_annot&#x27;, &#x27;Motif_similarity_annot&#x27;, &#x27;Orthology_annot&#x27;, &#x27;Motif_similarity_and_Orthology_annot&#x27;]">pycistarget_annotations_to_use</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>[&#x27;Direct_annot&#x27;, &#x27;Motif_similarity_annot&#x27;, &#x27;Orthology_annot&#x27;, &#x27;Motif_similarity_and_Orthology_annot&#x27;]</code></td>
<td class="ox-p-desc">upstream passes the python list literal; kept as a string so the rendered<br>command is byte-identical to upstream&#x27;s<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_auc_threshold = value" data-copy="pycistarget_auc_threshold = 0.005">pycistarget_auc_threshold</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.005</code></td>
<td class="ox-p-desc">pycisTarget parameters (upstream pycistarget_parameters)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_db_hg38_screen_v10clust = value" data-copy="pycistarget_db_hg38_screen_v10clust = ">pycistarget_db_hg38_screen_v10clust</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">user-provided pycisTarget rankings DB; &quot;&quot; disables motif enrichment<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_fraction_overlap_w_cistarget_database = value" data-copy="pycistarget_fraction_overlap_w_cistarget_database = 0.4">pycistarget_fraction_overlap_w_cistarget_database</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.4</code></td>
<td class="ox-p-desc">pycisTarget parameters (upstream pycistarget_parameters)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_motif_similarity_fdr = value" data-copy="pycistarget_motif_similarity_fdr = 0.001">pycistarget_motif_similarity_fdr</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.001</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_nes_threshold = value" data-copy="pycistarget_nes_threshold = 3">pycistarget_nes_threshold</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>3</code></td>
<td class="ox-p-desc">pycisTarget parameters (upstream pycistarget_parameters)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_orthologous_identity_threshold = value" data-copy="pycistarget_orthologous_identity_threshold = 0">pycistarget_orthologous_identity_threshold</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_rank_threshold = value" data-copy="pycistarget_rank_threshold = 0.05">pycistarget_rank_threshold</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.05</code></td>
<td class="ox-p-desc">pycisTarget parameters (upstream pycistarget_parameters)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pycistarget_term_col = value" data-copy="pycistarget_term_col = Direct_annot">pycistarget_term_col</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Direct_annot</code></td>
<td class="ox-p-desc">first entry of annotations_to_use<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_aucMaxRank_factor = value" data-copy="rcistarget_aucMaxRank_factor = 0.05">rcistarget_aucMaxRank_factor</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.05</code></td>
<td class="ox-p-desc">aucMaxRank = factor * ncol(motifRankings)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_db_hg38_500bp_up_100bp_down_v10clust = value" data-copy="rcistarget_db_hg38_500bp_up_100bp_down_v10clust = ">rcistarget_db_hg38_500bp_up_100bp_down_v10clust</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">gene-based TFBS motif enrichment (RcisTarget); &quot;&quot; disables both rules,<br>matching upstream&#x27;s &quot;to skip you have to leave one database entry with an<br>empty path&quot; convention<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_geneErnMaxRank = value" data-copy="rcistarget_geneErnMaxRank = 5000">rcistarget_geneErnMaxRank</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5000</code></td>
<td class="ox-p-desc">rcistarget tool parameter (upstream --rcistarget_geneErnMaxRank) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_geneErnMethod = value" data-copy="rcistarget_geneErnMethod = aprox">rcistarget_geneErnMethod</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>aprox</code></td>
<td class="ox-p-desc">alternatively exact but more intense: &quot;icistarget&quot;<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_motifAnnot_highConfCat = value" data-copy="rcistarget_motifAnnot_highConfCat = directAnnotation,inferredBy_Orthology">rcistarget_motifAnnot_highConfCat</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>directAnnotation,inferredBy_Orthology</code></td>
<td class="ox-p-desc">upstream python lists; comma-joined so the rendered command stays a single<br>token (values contain no commas)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_motifAnnot_lowConfCat = value" data-copy="rcistarget_motifAnnot_lowConfCat = inferredBy_MotifSimilarity,inferredBy_MotifSimilarity_n_Orthology">rcistarget_motifAnnot_lowConfCat</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>inferredBy_MotifSimilarity,inferredBy_MotifSimilarity_n_Orthology</code></td>
<td class="ox-p-desc">upstream python lists; comma-joined so the rendered command stays a single<br>token (values contain no commas)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_motif_annot = value" data-copy="rcistarget_motif_annot = ">rcistarget_motif_annot</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">user-provided motif-to-TF annotation tbl; &quot;&quot; disables<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rcistarget_nesThreshold = value" data-copy="rcistarget_nesThreshold = 3">rcistarget_nesThreshold</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>3</code></td>
<td class="ox-p-desc">upstream python lists; comma-joined so the rendered command stays a single<br>token (values contain no commas)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy region_beds = value" data-copy="region_beds = test/data/CorcesATAC">region_beds</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/data/CorcesATAC</code></td>
<td class="ox-p-desc">feature sets (derived from config/annotation.csv at port time)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy region_sets = value" data-copy="region_sets = Bcell_open_regions, Ery_open_regions">region_sets</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>Bcell_open_regions, Ery_open_regions</code></td>
<td class="ox-p-desc">feature sets (derived from config/annotation.csv at port time)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy result_path = value" data-copy="result_path = test/results/enrichment_analysis">result_path</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/results/enrichment_analysis</code></td>
<td class="ox-p-desc">general<br><span class="ox-param-usedby">used by <code>40</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rnk_dir = value" data-copy="rnk_dir = test/data/CorcesRNA">rnk_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/data/CorcesRNA</code></td>
<td class="ox-p-desc">{gene_set}.csv per entry of rnk_sets<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rnk_sets = value" data-copy="rnk_sets = Bcell_ranked, Ery_ranked">rnk_sets</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>Bcell_ranked, Ery_ranked</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy species = value" data-copy="species = homo_sapiens">species</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>homo_sapiens</code></td>
<td class="ox-p-desc">upstream derives species from genome (hg19/hg38 -&gt; homo_sapiens); ported as config key<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy top_terms_n = value" data-copy="top_terms_n = 5">top_terms_n</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">aggregate &amp; summarize (upstream top_terms_n / adjp_cap / or_cap / nes_cap / cluster_summary)<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-enrichment-rules.svg?v=0055e95439" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-enrichment-rules.svg?v=0055e95439" alt="oxo-flow-enrichment rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-enrichment.svg?v=6157d94671" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-enrichment.svg?v=6157d94671" alt="oxo-flow-enrichment pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-enrichment — Run a complete region set and gene set enrichment analysis on your own data: region overlap enrichment (LOLA), genomic region enrichment of annotated terms (rGREAT), region TFBS motif enrichment (pycisTarget), gene TFBS motif enrichment (RcisTarget), and gene over-representation analysis (ORA) and preranked GSEA (GSEApy).</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

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
