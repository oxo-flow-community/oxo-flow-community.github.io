---
title: "Unsupervised analysis of omics matrices: PCA, UMAP, clustering and validation"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-unsupervised</span></div>
<div class="ox-detail-cols">
<div>
<h1>Unsupervised analysis of omics matrices: PCA, UMAP, clustering and validation</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>
<p>Unsupervised analysis of omics matrices: PCA, UMAP and densMAP embeddings (2D/3D), distance matrices, hierarchical clustering heatmaps, Leiden clustering across partition types and resolutions, clustree analysis, external and internal cluster validation with TOPSIS ranking, static and interactive visualizations, per-feature dimred scatter plots (when-gated), and resolved-environment snapshots. A verified port of the default-parameter path of epigen/unsupervised_analysis v4.0.2 (Snakemake); all 61 rules and tool versions are pinned to the upstream release.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">61</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 2 CPUs / 32 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">other</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/epigen/unsupervised_analysis">epigen/unsupervised_analysis</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v4.0.2</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2297.1"><code>10.48546/workflowhub.workflow.2297.1</code></a></span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

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

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. The list below names the rules that read each key.</p>
<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>clustree_categorical_label_option</code><span class="ox-param-default">majority</span></div>
<p class="ox-param-desc">CLUSTREE</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>clustree_count_filter</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">CLUSTREE</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>clustree_layout</code><span class="ox-param-default">tree</span></div>
<p class="ox-param-desc">CLUSTREE</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>clustree_numerical_aggregation_option</code><span class="ox-param-default">mean</span></div>
<p class="ox-param-desc">CLUSTREE</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>clustree_prop_filter</code><span class="ox-param-default">0.1</span></div>
<p class="ox-param-desc">CLUSTREE</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>coord_fixed</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">VISUALIZATION</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>plot_dimred_clustering_densmap</code> <code>plot_dimred_clustering_pca</code> <code>plot_dimred_clustering_umap</code> <code>plot_dimred_features_pca</code> <code>plot_dimred_features_umap</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_pca</code> <code>plot_dimred_metadata_umap</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>data_dir</code><span class="ox-param-default">test/fixtures</span></div>
<p class="ox-param-desc">GENERAL</p>
<details class="ox-param-usedby"><summary>used by 40 rules</summary>
<div class="ox-param-rules"><code>aggregate_clustering_results</code> <code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code> <code>densmap_embed_2d</code> <code>densmap_embed_3d</code> <code>distance_matrix_features_correlation</code> <code>distance_matrix_features_cosine</code> <code>distance_matrix_observations_correlation</code> <code>distance_matrix_observations_cosine</code> <code>leiden_ModularityVertexPartition_NA</code> <code>leiden_RBConfigurationVertexPartition_0p5</code> <code>leiden_RBConfigurationVertexPartition_1</code> <code>leiden_RBConfigurationVertexPartition_1p5</code> <code>leiden_RBConfigurationVertexPartition_2</code> <code>leiden_RBConfigurationVertexPartition_4</code> <code>pca</code> <code>plot_dimred_interactive_densmap_2d</code> <code>plot_dimred_interactive_densmap_3d</code> <code>plot_dimred_interactive_pca_2d</code> <code>plot_dimred_interactive_pca_3d</code> <code>plot_dimred_interactive_umap_2d</code> <code>plot_dimred_interactive_umap_3d</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_pca</code> <code>plot_dimred_metadata_umap</code> <code>plot_heatmap_correlation</code> <code>plot_heatmap_cosine</code> <code>plot_pca_diagnostics</code> <code>prep_feature_plot</code> <code>umap_embed_2d</code> <code>umap_embed_3d</code> <code>umap_graph</code> <code>validation_external</code> <code>validation_internal_BIC</code> <code>validation_internal_C_index</code> <code>validation_internal_Calinski_Harabasz</code> <code>validation_internal_Davies_Bouldin</code> <code>validation_internal_Dunn</code> <code>validation_internal_Silhouette</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>features_to_plot</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">METADATA</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>prep_feature_plot</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>heatmap_hclust_method</code><span class="ox-param-default">complete</span></div>
<p class="ox-param-desc">HEATMAP (upstream heatmap: metrics [correlation, cosine] -&gt; 2 rules)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_heatmap_correlation</code> <code>plot_heatmap_cosine</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>heatmap_n_features</code><span class="ox-param-default">0.5</span></div>
<p class="ox-param-desc">HEATMAP (upstream heatmap: metrics [correlation, cosine] -&gt; 2 rules)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>distance_matrix_features_correlation</code> <code>distance_matrix_features_cosine</code> <code>distance_matrix_observations_correlation</code> <code>distance_matrix_observations_cosine</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>heatmap_n_observations</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">HEATMAP (upstream heatmap: metrics [correlation, cosine] -&gt; 2 rules)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>distance_matrix_features_correlation</code> <code>distance_matrix_features_cosine</code> <code>distance_matrix_observations_correlation</code> <code>distance_matrix_observations_cosine</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>leiden_metric</code><span class="ox-param-default">euclidean</span></div>
<p class="ox-param-desc">LEIDEN (upstream leiden: metric euclidean / n_neighbors 15 -&gt; 6 rules)</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>aggregate_clustering_results</code> <code>leiden_ModularityVertexPartition_NA</code> <code>leiden_RBConfigurationVertexPartition_0p5</code> <code>leiden_RBConfigurationVertexPartition_1</code> <code>leiden_RBConfigurationVertexPartition_1p5</code> <code>leiden_RBConfigurationVertexPartition_2</code> <code>leiden_RBConfigurationVertexPartition_4</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>leiden_n_iterations</code><span class="ox-param-default">2</span></div>
<p class="ox-param-desc">LEIDEN (upstream leiden: metric euclidean / n_neighbors 15 -&gt; 6 rules)</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>leiden_ModularityVertexPartition_NA</code> <code>leiden_RBConfigurationVertexPartition_0p5</code> <code>leiden_RBConfigurationVertexPartition_1</code> <code>leiden_RBConfigurationVertexPartition_1p5</code> <code>leiden_RBConfigurationVertexPartition_2</code> <code>leiden_RBConfigurationVertexPartition_4</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>leiden_n_neighbors</code><span class="ox-param-default">15</span></div>
<p class="ox-param-desc">LEIDEN (upstream leiden: metric euclidean / n_neighbors 15 -&gt; 6 rules)</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>aggregate_clustering_results</code> <code>leiden_ModularityVertexPartition_NA</code> <code>leiden_RBConfigurationVertexPartition_0p5</code> <code>leiden_RBConfigurationVertexPartition_1</code> <code>leiden_RBConfigurationVertexPartition_1p5</code> <code>leiden_RBConfigurationVertexPartition_2</code> <code>leiden_RBConfigurationVertexPartition_4</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>mem_mb</code><span class="ox-param-default">32000</span></div>
<p class="ox-param-desc">RESOURCES (upstream config: mem/threads)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>metadata_of_interest</code><span class="ox-param-default">target</span></div>
<p class="ox-param-desc">METADATA</p>
<details class="ox-param-usedby"><summary>used by 12 rules</summary>
<div class="ox-param-rules"><code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code> <code>plot_heatmap_correlation</code> <code>plot_heatmap_cosine</code> <code>plot_pca_diagnostics</code> <code>validation_internal_BIC</code> <code>validation_internal_C_index</code> <code>validation_internal_Calinski_Harabasz</code> <code>validation_internal_Davies_Bouldin</code> <code>validation_internal_Dunn</code> <code>validation_internal_Silhouette</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pca_n_components</code><span class="ox-param-default">0.9</span></div>
<p class="ox-param-desc">PCA (upstream pca: svd_solver, n_components)</p>
<details class="ox-param-usedby"><summary>used by 13 rules</summary>
<div class="ox-param-rules"><code>pca</code> <code>plot_dimred_clustering_pca</code> <code>plot_dimred_features_pca</code> <code>plot_dimred_interactive_pca_2d</code> <code>plot_dimred_interactive_pca_3d</code> <code>plot_dimred_metadata_pca</code> <code>plot_pca_diagnostics</code> <code>validation_internal_BIC</code> <code>validation_internal_C_index</code> <code>validation_internal_Calinski_Harabasz</code> <code>validation_internal_Davies_Bouldin</code> <code>validation_internal_Dunn</code> <code>validation_internal_Silhouette</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pca_svd_solver</code><span class="ox-param-default">auto</span></div>
<p class="ox-param-desc">PCA (upstream pca: svd_solver, n_components)</p>
<details class="ox-param-usedby"><summary>used by 13 rules</summary>
<div class="ox-param-rules"><code>pca</code> <code>plot_dimred_clustering_pca</code> <code>plot_dimred_features_pca</code> <code>plot_dimred_interactive_pca_2d</code> <code>plot_dimred_interactive_pca_3d</code> <code>plot_dimred_metadata_pca</code> <code>plot_pca_diagnostics</code> <code>validation_internal_BIC</code> <code>validation_internal_C_index</code> <code>validation_internal_Calinski_Harabasz</code> <code>validation_internal_Davies_Bouldin</code> <code>validation_internal_Dunn</code> <code>validation_internal_Silhouette</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>plot_dimred_features</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">FEATURE PLOTS: upstream runs plot_dimred_features only when<br>len(features_to_plot) &gt; 0; the oxo-flow <code>when</code> evaluator compares<br>scalars, not arrays, so this boolean switch carries the gate (set it to<br>true together with a non-empty features_to_plot)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>plot_dimred_features_pca</code> <code>plot_dimred_features_umap</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>project_name</code><span class="ox-param-default">digits</span></div>
<p class="ox-param-desc">GENERAL</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>annot_export</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>result_path</code><span class="ox-param-default">results</span></div>
<p class="ox-param-desc">GENERAL</p>
<details class="ox-param-usedby"><summary>used by 61 rules</summary>
<div class="ox-param-rules"><code>aggregate_all_clustering_results</code> <code>aggregate_clustering_results</code> <code>aggregate_rank_internal</code> <code>annot_export</code> <code>clustree_analysis_custom</code> <code>clustree_analysis_default</code> <code>clustree_analysis_metadata</code> <code>densmap_embed_2d</code> <code>densmap_embed_3d</code> <code>distance_matrix_features_correlation</code> <code>distance_matrix_features_cosine</code> <code>distance_matrix_observations_correlation</code> <code>distance_matrix_observations_cosine</code> <code>env_export_ComplexHeatmap</code> <code>env_export_clusterCrit</code> <code>env_export_clustree</code> <code>env_export_ggplot</code> <code>env_export_plotly</code> <code>env_export_pymcdm</code> <code>env_export_umap_leiden</code> <code>leiden_ModularityVertexPartition_NA</code> <code>leiden_RBConfigurationVertexPartition_0p5</code> <code>leiden_RBConfigurationVertexPartition_1</code> <code>leiden_RBConfigurationVertexPartition_1p5</code> <code>leiden_RBConfigurationVertexPartition_2</code> <code>leiden_RBConfigurationVertexPartition_4</code> <code>pca</code> <code>plot_dimred_clustering_densmap</code> <code>plot_dimred_clustering_pca</code> <code>plot_dimred_clustering_umap</code> <code>plot_dimred_features_pca</code> <code>plot_dimred_features_umap</code> <code>plot_dimred_interactive_densmap_2d</code> <code>plot_dimred_interactive_densmap_3d</code> <code>plot_dimred_interactive_pca_2d</code> <code>plot_dimred_interactive_pca_3d</code> <code>plot_dimred_interactive_umap_2d</code> <code>plot_dimred_interactive_umap_3d</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_pca</code> <code>plot_dimred_metadata_umap</code> <code>plot_heatmap_correlation</code> <code>plot_heatmap_cosine</code> <code>plot_indices_external</code> <code>plot_indices_internal</code> <code>plot_pca_diagnostics</code> <code>plot_umap_connectivity_densmap</code> <code>plot_umap_connectivity_umap</code> <code>plot_umap_diagnostics_densmap</code> <code>plot_umap_diagnostics_umap</code> <code>prep_feature_plot</code> <code>umap_embed_2d</code> <code>umap_embed_3d</code> <code>umap_graph</code> <code>validation_external</code> <code>validation_internal_BIC</code> <code>validation_internal_C_index</code> <code>validation_internal_Calinski_Harabasz</code> <code>validation_internal_Davies_Bouldin</code> <code>validation_internal_Dunn</code> <code>validation_internal_Silhouette</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>sample_proportion</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">CLUSTER VALIDATION</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>validation_internal_BIC</code> <code>validation_internal_C_index</code> <code>validation_internal_Calinski_Harabasz</code> <code>validation_internal_Davies_Bouldin</code> <code>validation_internal_Dunn</code> <code>validation_internal_Silhouette</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>scatterplot2d_alpha</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">VISUALIZATION</p>
<details class="ox-param-usedby"><summary>used by 15 rules</summary>
<div class="ox-param-rules"><code>plot_dimred_clustering_densmap</code> <code>plot_dimred_clustering_pca</code> <code>plot_dimred_clustering_umap</code> <code>plot_dimred_features_pca</code> <code>plot_dimred_features_umap</code> <code>plot_dimred_interactive_densmap_2d</code> <code>plot_dimred_interactive_densmap_3d</code> <code>plot_dimred_interactive_pca_2d</code> <code>plot_dimred_interactive_pca_3d</code> <code>plot_dimred_interactive_umap_2d</code> <code>plot_dimred_interactive_umap_3d</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_pca</code> <code>plot_dimred_metadata_umap</code> <code>plot_pca_diagnostics</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>scatterplot2d_size</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">VISUALIZATION</p>
<details class="ox-param-usedby"><summary>used by 15 rules</summary>
<div class="ox-param-rules"><code>plot_dimred_clustering_densmap</code> <code>plot_dimred_clustering_pca</code> <code>plot_dimred_clustering_umap</code> <code>plot_dimred_features_pca</code> <code>plot_dimred_features_umap</code> <code>plot_dimred_interactive_densmap_2d</code> <code>plot_dimred_interactive_densmap_3d</code> <code>plot_dimred_interactive_pca_2d</code> <code>plot_dimred_interactive_pca_3d</code> <code>plot_dimred_interactive_umap_2d</code> <code>plot_dimred_interactive_umap_3d</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_pca</code> <code>plot_dimred_metadata_umap</code> <code>plot_pca_diagnostics</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>threads</code><span class="ox-param-default">2</span></div>
<p class="ox-param-desc">RESOURCES (upstream config: mem/threads)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>umap_connectivity</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>umap_densmap</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>umap_diagnostics</code><span class="ox-param-default">1</span></div>
<p class="ox-param-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>umap_metric</code><span class="ox-param-default">euclidean</span></div>
<p class="ox-param-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)</p>
<details class="ox-param-usedby"><summary>used by 18 rules</summary>
<div class="ox-param-rules"><code>densmap_embed_2d</code> <code>densmap_embed_3d</code> <code>plot_dimred_clustering_densmap</code> <code>plot_dimred_clustering_umap</code> <code>plot_dimred_features_umap</code> <code>plot_dimred_interactive_densmap_2d</code> <code>plot_dimred_interactive_densmap_3d</code> <code>plot_dimred_interactive_umap_2d</code> <code>plot_dimred_interactive_umap_3d</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_umap</code> <code>plot_umap_connectivity_densmap</code> <code>plot_umap_connectivity_umap</code> <code>plot_umap_diagnostics_densmap</code> <code>plot_umap_diagnostics_umap</code> <code>umap_embed_2d</code> <code>umap_embed_3d</code> <code>umap_graph</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>umap_min_dist</code><span class="ox-param-default">0.1</span></div>
<p class="ox-param-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)</p>
<details class="ox-param-usedby"><summary>used by 17 rules</summary>
<div class="ox-param-rules"><code>densmap_embed_2d</code> <code>densmap_embed_3d</code> <code>plot_dimred_clustering_densmap</code> <code>plot_dimred_clustering_umap</code> <code>plot_dimred_features_umap</code> <code>plot_dimred_interactive_densmap_2d</code> <code>plot_dimred_interactive_densmap_3d</code> <code>plot_dimred_interactive_umap_2d</code> <code>plot_dimred_interactive_umap_3d</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_umap</code> <code>plot_umap_connectivity_densmap</code> <code>plot_umap_connectivity_umap</code> <code>plot_umap_diagnostics_densmap</code> <code>plot_umap_diagnostics_umap</code> <code>umap_embed_2d</code> <code>umap_embed_3d</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>umap_n_neighbors</code><span class="ox-param-default">15</span></div>
<p class="ox-param-desc">UMAP &amp; densMAP (upstream umap: single default metric/neighbors/min_dist)</p>
<details class="ox-param-usedby"><summary>used by 18 rules</summary>
<div class="ox-param-rules"><code>densmap_embed_2d</code> <code>densmap_embed_3d</code> <code>plot_dimred_clustering_densmap</code> <code>plot_dimred_clustering_umap</code> <code>plot_dimred_features_umap</code> <code>plot_dimred_interactive_densmap_2d</code> <code>plot_dimred_interactive_densmap_3d</code> <code>plot_dimred_interactive_umap_2d</code> <code>plot_dimred_interactive_umap_3d</code> <code>plot_dimred_metadata_densmap</code> <code>plot_dimred_metadata_umap</code> <code>plot_umap_connectivity_densmap</code> <code>plot_umap_connectivity_umap</code> <code>plot_umap_diagnostics_densmap</code> <code>plot_umap_diagnostics_umap</code> <code>umap_embed_2d</code> <code>umap_embed_3d</code> <code>umap_graph</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

<img src="../assets/dag/oxo-flow-unsupervised.svg?v=1788704962" alt="oxo-flow-unsupervised pipeline overview" loading="lazy">

<p class="ox-dag-caption">figure · oxo-flow-unsupervised — Unsupervised analysis of omics matrices: PCA, UMAP and densMAP embeddings (2D/3D), distance matrices, hierarchical clustering heatmaps, Leiden clustering across partition types and resolutions, clustree analysis, external and internal cluster validation with TOPSIS ranking, static and interactive visualizations, per-feature dimred scatter plots (when-gated), and resolved-environment snapshots.</p>

</div>

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

- report/ generation — Snakemake `report(...)` wrapper metadata is partially ported: the per-rule .rst captions (workflow/report/dimred_2d_features.rst, dimred_2d_metadata.rst, dimred_2d_clusterings.rst, pca_diagnostics.rst, umap_diagnostics.rst, umap_connectivity.rst, heatmap.rst, clustree.rst, cluster_validation.rst, software.rst, configs.rst) are carried as report = "…" annotations on the 28 rules upstream wraps in report() (dimred/heatmap/clustree/indices plots, PCA/UMAP diagnostics and connectivity, 7 env_export snapshots, annot_export), rendered by the engine rule-captions report section (needs oxo-flow >= 0.17.0; older engines ignore the key). Still without an oxo-flow equivalent: the Snakemake artifact-catalog book itself (self-contained HTML with figures embedded, categories/subcategories/labels) and the workflow-level report: directive (workflow/report/workflow.rst); `oxo-flow report` generates an execution report from the checkpoint (rule status/timings). All underlying rule outputs are produced.

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
