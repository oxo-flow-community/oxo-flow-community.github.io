# unsupervised_analysis completeness audit (2026-08-21)

Upstream: epigen/unsupervised_analysis @ v4.0.2 · Port:
`oxo-flow-unsupervised` (live-verified).

Single-Snakefile, 24 rules, 15 config toggles, zero external services.
Input: data CSV + metadata CSV per sample (orientation flag).

## Mode matrix (upstream — config-driven DAG branches)

| mode | enable key | chain |
|---|---|---|
| PCA | always | pca → diagnostics (4 PNGs) + metadata plots + interactive 2D/3D |
| UMAP | always | umap_graph (metrics×n_neighbors) → umap_embed → plots |
| densMAP | `umap.densmap` | graph → densmap_embed → same plot set |
| heatmap | heatmap.metrics/hclust_methods non-empty | distance_matrix → plot_heatmap |
| Leiden | `leiden.metrics` ⊆ umap.metrics | leiden_cluster (×partition×resolution) → aggregate results |
| clustree | Leiden + | clustree default/custom + metadata/features dirs |
| external validation | Leiden | 6 indices → plot_indices |
| internal validation + TOPSIS | Leiden + `sample_proportion > 0` | pca + clusterings → 6 indices → TOPSIS rank → heatmap |
| exports | always | 7 env yamls + config + annotation |

Overlays: connectivity/diagnostics plots, feature plots
(features_to_plot [ALL]), clustering overlay on dimred.

## Gap tiers vs the port

**P0**: densMAP branch; Leiden cluster mode + the whole downstream
clustree/validation/TOPSIS cascade (all gated on it); heatmap branch;
interactive plotly outputs; feature-plot overlays.

**P1**: none — MIT, all-OSS, fully local computation (zero
requests/urlopen/API hits in the code).

**P2**: n_components/svd_solver, umap hyperparams, coord_fixed, point
aesthetics, clustree layout/aggregation, metadata_of_interest,
sample_proportion, orientation flag.

Environment gates (upstream, mirror as appropriate): global container
image ghcr.io/epigen/unsupervised_analysis (or --sdm conda);
env_export requires a conda binary on PATH even under conda mode;
clusterCrit Silhouette NA bug (rows removed pre-TOPSIS — known caveat).

## Verdict

Mid-size config surface: the ported PCA+UMAP default leaves densMAP,
heatmap, and the entire Leiden-clustering cascade (B/C/D modes) as the
P0 block — all free software.
