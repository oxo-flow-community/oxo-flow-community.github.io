---
title: "Unsupervised analysis of omics matrices: PCA, UMAP, clustering and validation"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-unsupervised</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Unsupervised analysis of omics matrices: PCA, UMAP, clustering and validation</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">unsupervised-learning</span><span class="ox-tag">pca</span><span class="ox-tag">umap</span><span class="ox-tag">densmap</span><span class="ox-tag">leiden</span><span class="ox-tag">clustering</span><span class="ox-tag">cluster-validation</span><span class="ox-tag">heatmap</span><span class="ox-tag">snakemake</span></div>
<p class="ox-desc">Unsupervised analysis of omics matrices: PCA, UMAP and densMAP embeddings (2D/3D), distance matrices, hierarchical clustering heatmaps, Leiden clustering across partition types and resolutions, clustree analysis, external and internal cluster validation with TOPSIS ranking, static and interactive visualizations, per-feature dimred scatter plots (when-gated), and resolved-environment snapshots. A verified port of the default-parameter path of epigen/unsupervised_analysis v4.0.2 (Snakemake); all 61 rules and tool versions are pinned to the upstream release.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-unsupervised" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">61</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 2 CPUs / 32 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">other</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/epigen/unsupervised_analysis">epigen/unsupervised_analysis</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v4.0.2</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2297.1"><code>10.48546/workflowhub.workflow.2297.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">igraph</span><span class="tchip">leidenalg</span><span class="tchip">scikit-learn</span><span class="tchip">python</span><span class="tchip">pandas</span><span class="tchip">scipy</span><span class="tchip">numpy</span><span class="tchip">pynndescent</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-unsupervised</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Unsupervised analysis pipeline</strong>: given a sample-by-features matrix and its annotations, it explores the data through PCA, UMAP/densMAP embeddings, Leiden clustering, clustree trees, hierarchical clustering heatmaps, and cluster validation — delivered as static and interactive plots.</p>
<p><strong>1. Dimensionality reduction</strong> — <code>pca</code> computes the PCA of the sample matrix and <code>umap_graph</code> builds the kNN graph; everything downstream builds on these roots.</p>
<p><strong>2. Embedding fan-out</strong> — <code>umap_graph</code> feeds four parallel embeddings: <code>umap_embed_2d</code>, <code>umap_embed_3d</code>, <code>densmap_embed_2d</code>, <code>densmap_embed_3d</code>.</p>
<p><strong>3. Leiden clustering fan-out</strong> — six configurations run in parallel (<code>leiden_RBConfigurationVertexPartition_0p5</code>, <code>leiden_RBConfigurationVertexPartition_1</code>, <code>leiden_RBConfigurationVertexPartition_1p5</code>, <code>leiden_RBConfigurationVertexPartition_2</code>, <code>leiden_RBConfigurationVertexPartition_4</code>, <code>leiden_ModularityVertexPartition_NA</code>), converge into <code>aggregate_clustering_results</code>, then merge into one table via <code>aggregate_all_clustering_results</code> — the source for every clustering-colored plot and validation.</p>
<p><strong>4. Clustered heatmaps</strong> — <code>distance_matrix_observations_correlation</code>, <code>distance_matrix_features_correlation</code>, <code>distance_matrix_observations_cosine</code>, <code>distance_matrix_features_cosine</code> converge pairwise into <code>plot_heatmap_correlation</code> and <code>plot_heatmap_cosine</code>; each heatmap needs both matrices.</p>
<p><strong>5. Validation and clustree</strong> — <code>validation_external</code> and six internal indices (<code>validation_internal_Silhouette</code>, <code>validation_internal_Calinski_Harabasz</code>, <code>validation_internal_Dunn</code>, <code>validation_internal_C_index</code>, <code>validation_internal_Davies_Bouldin</code>, <code>validation_internal_BIC</code>), each combining the aggregated clusterings with <code>pca</code>, converge into <code>aggregate_rank_internal</code> (TOPSIS ranking), rendered by <code>plot_indices_external</code> and <code>plot_indices_internal</code>; <code>clustree_analysis_default</code>, <code>clustree_analysis_custom</code>, and <code>clustree_analysis_metadata</code> render clustree trees.</p>
<p><strong>6. Scatter and diagnostic plots</strong> — clustering and metadata scatter plots per embedding (<code>plot_dimred_metadata_pca</code>, <code>plot_dimred_clustering_pca</code>, and the umap/densmap equivalents); feature plots and interactive HTML (<code>plot_dimred_features_pca</code>, <code>plot_dimred_interactive_pca_2d</code>) additionally merge <code>prep_feature_plot</code>; <code>plot_pca_diagnostics</code>, <code>plot_umap_diagnostics_umap</code>, <code>plot_umap_connectivity_umap</code> and their densmap counterparts wrap up the reporting.</p>
<p><em>Verified: every rule name above is a real rule of <code>main.oxoflow</code> (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-unsupervised+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-unsupervised
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-unsupervised` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-unsupervised@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-unsupervised` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Real sklearn `digits` data is committed under `test/fixtures/` — fully runnable out of the box.

## Installation

**Engine.** oxo-flow >= 0.12.0 (the report = caption annotations on 28 rules require >= 0.17.0 — the rule-captions report section; older engines ignore the key)

**Toolchain.** conda envs — pinned versions (7 environments under envs/, created by conda/mamba)

**Requirements.**

- per-sample omics matrix CSV and optional labels CSV ({config.data_dir}/{sample}_data.csv / _labels.csv), registered in config/annotation.csv; no reference genomes or index files needed (default fixtures: sklearn digits, 1797 samples x 64 features)
- compute: up to 2 CPUs / 32 GB RAM per rule (defaults threads=2, mem_mb=32000; 7 plotting rules use 8 GB)
- conda or mamba installed to build the 7 pinned environments on first run

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-unsupervised
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-unsupervised
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clustree_categorical_label_option = value" data-copy="clustree_categorical_label_option = majority">clustree_categorical_label_option</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>majority</code></td>
<td class="ox-p-desc">CLUSTREE<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clustree_count_filter = value" data-copy="clustree_count_filter = 0">clustree_count_filter</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">CLUSTREE<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clustree_layout = value" data-copy="clustree_layout = tree">clustree_layout</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>tree</code></td>
<td class="ox-p-desc">CLUSTREE<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clustree_numerical_aggregation_option = value" data-copy="clustree_numerical_aggregation_option = mean">clustree_numerical_aggregation_option</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>mean</code></td>
<td class="ox-p-desc">CLUSTREE<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clustree_prop_filter = value" data-copy="clustree_prop_filter = 0.1">clustree_prop_filter</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.1</code></td>
<td class="ox-p-desc">CLUSTREE<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy coord_fixed = value" data-copy="coord_fixed = 0">coord_fixed</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">VISUALIZATION<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy data_dir = value" data-copy="data_dir = test/fixtures">data_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures</code></td>
<td class="ox-p-desc">GENERAL<br><span class="ox-param-usedby">used by <code>40</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy features_to_plot = value" data-copy="features_to_plot = ">features_to_plot</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">METADATA<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy heatmap_hclust_method = value" data-copy="heatmap_hclust_method = complete">heatmap_hclust_method</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>complete</code></td>
<td class="ox-p-desc">HEATMAP (upstream heatmap: metrics [correlation, cosine] -&gt; 2 rules)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy heatmap_n_features = value" data-copy="heatmap_n_features = 0.5">heatmap_n_features</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.5</code></td>
<td class="ox-p-desc">HEATMAP (upstream heatmap: metrics [correlation, cosine] -&gt; 2 rules)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy heatmap_n_observations = value" data-copy="heatmap_n_observations = 1">heatmap_n_observations</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">HEATMAP (upstream heatmap: metrics [correlation, cosine] -&gt; 2 rules)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy leiden_metric = value" data-copy="leiden_metric = euclidean">leiden_metric</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>euclidean</code></td>
<td class="ox-p-desc">LEIDEN (upstream leiden: metric euclidean / n_neighbors 15 -&gt; 6 rules)<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy leiden_n_iterations = value" data-copy="leiden_n_iterations = 2">leiden_n_iterations</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">LEIDEN (upstream leiden: metric euclidean / n_neighbors 15 -&gt; 6 rules)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy leiden_n_neighbors = value" data-copy="leiden_n_neighbors = 15">leiden_n_neighbors</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">LEIDEN (upstream leiden: metric euclidean / n_neighbors 15 -&gt; 6 rules)<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mem_mb = value" data-copy="mem_mb = 32000">mem_mb</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>32000</code></td>
<td class="ox-p-desc">RESOURCES (upstream config: mem/threads)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy metadata_of_interest = value" data-copy="metadata_of_interest = target">metadata_of_interest</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>target</code></td>
<td class="ox-p-desc">METADATA<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pca_n_components = value" data-copy="pca_n_components = 0.9">pca_n_components</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.9</code></td>
<td class="ox-p-desc">PCA (upstream pca: svd_solver, n_components)<br><span class="ox-param-usedby">used by <code>13</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pca_svd_solver = value" data-copy="pca_svd_solver = auto">pca_svd_solver</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>auto</code></td>
<td class="ox-p-desc">PCA (upstream pca: svd_solver, n_components)<br><span class="ox-param-usedby">used by <code>13</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy plot_dimred_features = value" data-copy="plot_dimred_features = false">plot_dimred_features</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">FEATURE PLOTS: upstream runs plot_dimred_features only when<br>len(features_to_plot) &gt; 0; the oxo-flow <code>when</code> evaluator compares<br>scalars, not arrays, so this boolean switch carries the gate (set it to<br>true together with a non-empty features_to_plot)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy project_name = value" data-copy="project_name = digits">project_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>digits</code></td>
<td class="ox-p-desc">GENERAL<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy result_path = value" data-copy="result_path = results">result_path</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">GENERAL<br><span class="ox-param-usedby">used by <code>61</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sample_proportion = value" data-copy="sample_proportion = 1">sample_proportion</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">CLUSTER VALIDATION<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy scatterplot2d_alpha = value" data-copy="scatterplot2d_alpha = 1">scatterplot2d_alpha</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">VISUALIZATION<br><span class="ox-param-usedby">used by <code>15</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy scatterplot2d_size = value" data-copy="scatterplot2d_size = 1">scatterplot2d_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">VISUALIZATION<br><span class="ox-param-usedby">used by <code>15</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy threads = value" data-copy="threads = 2">threads</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">RESOURCES (upstream config: mem/threads)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy umap_connectivity = value" data-copy="umap_connectivity = 1">umap_connectivity</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy umap_densmap = value" data-copy="umap_densmap = 1">umap_densmap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy umap_diagnostics = value" data-copy="umap_diagnostics = 1">umap_diagnostics</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy umap_metric = value" data-copy="umap_metric = euclidean">umap_metric</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>euclidean</code></td>
<td class="ox-p-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)<br><span class="ox-param-usedby">used by <code>18</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy umap_min_dist = value" data-copy="umap_min_dist = 0.1">umap_min_dist</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.1</code></td>
<td class="ox-p-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)<br><span class="ox-param-usedby">used by <code>17</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy umap_n_neighbors = value" data-copy="umap_n_neighbors = 15">umap_n_neighbors</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)<br><span class="ox-param-usedby">used by <code>18</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-unsupervised-rules.svg?v=91b51a5f7f" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-unsupervised-rules.svg?v=91b51a5f7f" alt="oxo-flow-unsupervised rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card ox-dag-card--wide" markdown="1">

<a href="/assets/dag/oxo-flow-unsupervised.svg?v=f47d2ccd2e" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-unsupervised.svg?v=f47d2ccd2e" alt="oxo-flow-unsupervised pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-unsupervised — Unsupervised analysis of omics matrices: PCA, UMAP and densMAP embeddings (2D/3D), distance matrices, hierarchical clustering heatmaps, Leiden clustering across partition types and resolutions, clustree analysis, external and internal cluster validation with TOPSIS ranking, static and interactive visualizations, per-feature dimred scatter plots (when-gated), and resolved-environment snapshots.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- pca
- umap_graph
- umap_embed_2d
- umap_embed_3d
- densmap_embed_2d
- densmap_embed_3d
- distance_matrix_observations_correlation
- distance_matrix_observations_cosine
- distance_matrix_features_correlation
- distance_matrix_features_cosine
- prep_feature_plot
- plot_dimred_features_pca
- plot_dimred_features_umap
- leiden_RBConfigurationVertexPartition_0p5
- leiden_RBConfigurationVertexPartition_1
- leiden_RBConfigurationVertexPartition_1p5
- leiden_RBConfigurationVertexPartition_2
- leiden_RBConfigurationVertexPartition_4
- leiden_ModularityVertexPartition_NA
- aggregate_clustering_results
- aggregate_all_clustering_results
- plot_dimred_metadata_pca
- plot_dimred_metadata_umap
- plot_dimred_metadata_densmap
- plot_dimred_clustering_pca
- plot_dimred_clustering_umap
- plot_dimred_clustering_densmap
- plot_pca_diagnostics
- plot_umap_diagnostics_umap
- plot_umap_diagnostics_densmap
- plot_umap_connectivity_umap
- plot_umap_connectivity_densmap
- plot_dimred_interactive_pca_2d
- plot_dimred_interactive_pca_3d
- plot_dimred_interactive_umap_2d
- plot_dimred_interactive_umap_3d
- plot_dimred_interactive_densmap_2d
- plot_dimred_interactive_densmap_3d
- plot_heatmap_correlation
- plot_heatmap_cosine
- clustree_analysis_default
- clustree_analysis_custom
- clustree_analysis_metadata
- validation_external
- validation_internal_Silhouette
- validation_internal_Calinski_Harabasz
- validation_internal_Dunn
- validation_internal_C_index
- validation_internal_Davies_Bouldin
- validation_internal_BIC
- aggregate_rank_internal
- plot_indices_external
- plot_indices_internal
- annot_export
- env_export_umap_leiden
- env_export_clusterCrit
- env_export_clustree
- env_export_ComplexHeatmap
- env_export_ggplot
- env_export_plotly
- env_export_pymcdm

**Excluded**

- report/ generation — Snakemake `report(...)` wrapper metadata is partially ported: the per-rule .rst captions (workflow/report/dimred_2d_features.rst, dimred_2d_metadata.rst, dimred_2d_clusterings.rst, pca_diagnostics.rst, umap_diagnostics.rst, umap_connectivity.rst, heatmap.rst, clustree.rst, cluster_validation.rst, software.rst, configs.rst) are carried as report = "…" annotations on the 28 ported rules (upstream wraps 16 report() sites, expanding to 22 instances with env_export×7 — dimred/heatmap/clustree/indices plots, PCA/UMAP diagnostics and connectivity, 7 env_export snapshots, annot_export), rendered by the engine rule-captions report section (needs oxo-flow >= 0.17.0; older engines ignore the key). Still without an oxo-flow equivalent: the Snakemake artifact-catalog book itself (self-contained HTML with figures embedded, categories/subcategories/labels) and the workflow-level report: directive (workflow/report/workflow.rst); `oxo-flow report` generates an execution report from the checkpoint (rule status/timings). All underlying rule outputs are produced.

## Fidelity

Upstream rules and how each is ported (61 ported rules; every analysis step
of the default-parameter path is executed, none are stubbed):

| Upstream rule | Port | Notes |
|---|---|---|
| `pca` | `pca` | same script; snakemake object replaced by CLI args |
| `umap_graph` | `umap_graph` | knn-graph for the default metric/neighbors |
| `umap_embed` | `umap_embed_2d`, `umap_embed_3d` | parameter-list fan-out (n_components 2/3) becomes explicit rules |
| `densmap_embed` | `densmap_embed_2d`, `densmap_embed_3d` | same fan-out |
| `distance_matrix` | `distance_matrix_{observations,features}_{correlation,cosine}` (4) | wildcard fan-out ({type} x {metric}) becomes explicit rules |
| `prep_feature_plot` | `prep_feature_plot` | runs always (upstream always computes it) |
| `leiden_cluster` | `leiden_RBConfigurationVertexPartition_{0.5,1,1.5,2,4}`, `leiden_ModularityVertexPartition_NA` (6) | partition_types x resolutions fan-out becomes explicit rules; graph always taken from the precomputed UMAP knn-graph |
| `aggregate_clustering_results` | `aggregate_clustering_results` | upstream `run:` block ported to `scripts/aggregate_clustering.py` (input[0] metadata unused upstream, mirrored) |
| `aggregate_all_clustering_results` | `aggregate_all_clustering_results` | `run:` block ported to `scripts/aggregate_all_clustering.py` |
| `plot_dimred_features` | `plot_dimred_features_{pca,umap}` (2) | method fan-out (upstream appends "features" content only for PCA and UMAP); gated on `config.plot_dimred_features` — see porting note 7 |
| `plot_dimred_metadata` | `plot_dimred_metadata_{pca,umap,densmap}` (3) | method fan-out; 2D only (upstream default n_components 2) |
| `plot_dimred_clustering` | `plot_dimred_clustering_{pca,umap,densmap}` (3) | same |
| `plot_pca_diagnostics` | `plot_pca_diagnostics` | variance/pairs/loadings/lollipop PNGs, mem 8000M |
| `plot_umap_diagnostics` | `plot_umap_diagnostics_{umap,densmap}` (2) | mem 32000M (upstream) |
| `plot_umap_connectivity` | `plot_umap_connectivity_{umap,densmap}` (2) | mem 16000M (upstream) |
| `plot_dimred_interactive` | `plot_dimred_interactive_{pca,umap,densmap}_{2d,3d}` (6) | n_components fan-out; mem 8000M |
| `plot_heatmap` | `plot_heatmap_{correlation,cosine}` (2) | metric fan-out; hclust method from default list |
| `clustree_analysis` | `clustree_analysis_default`, `clustree_analysis_custom` (2) | content fan-out |
| `clustree_analysis_metadata` | `clustree_analysis_metadata` | directory output of per-metadata PNGs |
| `validation_external` | `validation_external` | all 6 indices (AMI, ARI, FMI, Homogeneity, Completeness, V) in one rule, 6 outputs |
| `validation_internal` | `validation_internal_{Silhouette,Calinski_Harabasz,Dunn,C_index,Davies_Bouldin,BIC}` (6) | index fan-out; mem 2x (upstream) |
| `aggregate_rank_internal` | `aggregate_rank_internal` | TOPSIS ranking of the 6 internal indices |
| `plot_indices` | `plot_indices_external`, `plot_indices_internal` (2) | type fan-out; external = 6 heatmaps, internal = 1 ranked heatmap |
| `annot_export` | `annot_export` | `cp {input} {output}` |
| `env_export` (7) | `env_export_{umap_leiden,clusterCrit,clustree,ComplexHeatmap,ggplot,plotly,pymcdm}` (7) | resolved-env snapshot: oxo-flow runs each rule inside its pinned env via `conda run`, so `conda env export -p "$CONDA_PREFIX"` exports the ANALYSIS env (mamba fallback; mem 1000M like upstream) |
| `config_export` | **not ported** | excluded — see the Excluded list above |
| `report/` generation | **not ported** | excluded — see the Excluded list above |

### Porting notes and deviations

1. **Annotation mapping**: the upstream annotation CSV's `data`/`metadata`
   columns become `{config.data_dir}/{sample}_data.csv` and
   `{config.data_dir}/{sample}_labels.csv`; `samples_by_features` is a global
   config key (upstream reads it per sample).
2. **Parameter-list fan-out**: upstream wildcards over parameter lists
   (UMAP/densMAP n_components, distance-matrix metric/type, Leiden
   partition_type/resolution, heatmap metric, clustree content, internal
   index) have no oxo-flow engine equivalent, so each default combination is
   an explicit rule whose name and paths embed the combination. Changing a
   listed parameter (e.g. adding a UMAP metric) requires adding rules.
3. **Snakemake runtime object**: all scripts read their inputs/outputs/params
   as CLI arguments instead of the `snakemake` global; the analysis code is
   unchanged. R scripts share `scripts/args.R` for `--flag value` parsing.
4. **Aggregation rules**: upstream `run:` blocks were ported to Python
   scripts with identical logic.
5. **Memory/threads**: upstream `mem: 32000` / `threads: 2` defaults become
   `[defaults]`; per-rule overrides match upstream (pca diagnostics and
   interactive plots 8000M, internal validation 2x).
6. **Environment**: each rule pins the same conda environment as upstream
   (7 environments, copied verbatim from `workflow/envs/`).
7. **Boolean gate instead of list gate**: upstream runs `plot_dimred_features`
   only when `len(features_to_plot) > 0`; the oxo-flow `when` evaluator
   compares scalar config values (booleans, numbers, strings), not arrays, so
   the port carries the gate on `config.plot_dimred_features` (default
   `false`, matching the upstream default of an empty `features_to_plot`).
   Enable it together with a non-empty `features_to_plot` — the plotting
   script then uses the requested features, or falls back to the first 10
   columns when the requested features are absent.


## Links

- Repository: [oxo-flow-unsupervised](https://github.com/oxo-flow-community/oxo-flow-unsupervised)
- Upstream: [epigen/unsupervised_analysis](https://github.com/epigen/unsupervised_analysis) @ `v4.0.2`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
