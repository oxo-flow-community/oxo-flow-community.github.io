**Single-cell RNA-seq pipeline** (port of nf-core/scrnaseq): raw 10x-style FASTQs plus a reference genome and annotation go through one of several aligner routes into per-sample and combined matrices, cleaned of ambient RNA by CellBender.

**1. Reference preparation** — `gunzip_fasta` and `gunzip_gtf` decompress the (optionally gzipped) genome and annotation; their outputs converge in `gtf_gene_filter`, which keeps only annotations present in the genome FASTA, followed by the opt-in `gtf_source_fix` rewriting for Cell Ranger.

**2. Indexing and quantification (one exclusive route per run)** — Cell Ranger: `cellranger_mkgtf` → `cellranger_mkref` → `cellranger_count`, or, when the multi branch is on, `cellranger_mkvdjref` → `cellranger_multi`; cellranger-arc: `cellrangerarc_mkgtf` → `cellrangerarc_mkref` → `cellrangerarc_count`; simpleaf: `simpleaf_index` → `simpleaf_quant` → `qcatch`; kallisto|bustools: `kallistobustools_ref_standard` or `kallistobustools_ref_velocity` → `kallistobustools_count`; STARsolo: `star_genomegenerate` (or the legacy-index `star_genomeparams_upgrade`) → `star_align`.

**3. Matrix conversion** — whichever route ran, its raw and filtered outputs become per-sample h5ads: `mtx_to_h5ad_raw` and `mtx_to_h5ad_filtered` (Cell Ranger count, cellranger-arc), `mtx_to_h5ad_multi_raw` and `mtx_to_h5ad_multi_filtered`, `mtx_to_h5ad_simpleaf`, `mtx_to_h5ad_kallisto_raw` and `mtx_to_h5ad_kallisto_filtered`, `mtx_to_h5ad_star_raw` and `mtx_to_h5ad_star_filtered`.

**4. CellBender, merge, R objects** — `cellbender_removebackground` strips ambient RNA from raw matrices (never for cellrangerarc); `anndata_barcodes` subsets them to the surviving barcodes; `concat_h5ad_filtered`, `concat_h5ad_cellbender_filter` and `concat_h5ad_raw` merge each input type across samples; the anndataR rules convert per-sample and combined h5ads to Seurat and SingleCellExperiment RDS.

**5. Reporting** — `fastqc` reports (skipped for cellrangerarc), plus `collect_versions`, `workflow_summary` and `methods_description`, all feed `multiqc` for the final aggregate report.

*Verified: every rule name above is a real rule of `main.oxoflow` (oxo-flow validate); the described order follows the actual rule dependencies.*
