**Unsupervised analysis pipeline**: given a sample-by-features matrix and its annotations, it explores the data through PCA, UMAP/densMAP embeddings, Leiden clustering, clustree trees, hierarchical clustering heatmaps, and cluster validation — delivered as static and interactive plots.

**1. Dimensionality reduction** — `pca` computes the PCA of the sample matrix and `umap_graph` builds the kNN graph; everything downstream builds on these roots.

**2. Embedding fan-out** — `umap_graph` feeds four parallel embeddings: `umap_embed_2d`, `umap_embed_3d`, `densmap_embed_2d`, `densmap_embed_3d`.

**3. Leiden clustering fan-out** — six configurations run in parallel (`leiden_RBConfigurationVertexPartition_0p5`, `leiden_RBConfigurationVertexPartition_1`, `leiden_RBConfigurationVertexPartition_1p5`, `leiden_RBConfigurationVertexPartition_2`, `leiden_RBConfigurationVertexPartition_4`, `leiden_ModularityVertexPartition_NA`), converge into `aggregate_clustering_results`, then merge into one table via `aggregate_all_clustering_results` — the source for every clustering-colored plot and validation.

**4. Clustered heatmaps** — `distance_matrix_observations_correlation`, `distance_matrix_features_correlation`, `distance_matrix_observations_cosine`, `distance_matrix_features_cosine` converge pairwise into `plot_heatmap_correlation` and `plot_heatmap_cosine`; each heatmap needs both matrices.

**5. Validation and clustree** — `validation_external` and six internal indices (`validation_internal_Silhouette`, `validation_internal_Calinski_Harabasz`, `validation_internal_Dunn`, `validation_internal_C_index`, `validation_internal_Davies_Bouldin`, `validation_internal_BIC`), each combining the aggregated clusterings with `pca`, converge into `aggregate_rank_internal` (TOPSIS ranking), rendered by `plot_indices_external` and `plot_indices_internal`; `clustree_analysis_default`, `clustree_analysis_custom`, and `clustree_analysis_metadata` render clustree trees.

**6. Scatter and diagnostic plots** — clustering and metadata scatter plots per embedding (`plot_dimred_metadata_pca`, `plot_dimred_clustering_pca`, and the umap/densmap equivalents); feature plots and interactive HTML (`plot_dimred_features_pca`, `plot_dimred_interactive_pca_2d`) additionally merge `prep_feature_plot`; `plot_pca_diagnostics`, `plot_umap_diagnostics_umap`, `plot_umap_connectivity_umap` and their densmap counterparts wrap up the reporting.

*Verified: every rule name above is a real rule of `main.oxoflow` (oxo-flow validate); the described order follows the actual rule dependencies.*
