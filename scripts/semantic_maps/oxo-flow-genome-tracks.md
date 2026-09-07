**Genome browser track generation pipeline**: given aligned BAMs, it merges sample groups, computes bigWig coverage, and renders genomic track plots plus a UCSC genome browser hub — with an optional single-cell split path and an opt-in IGV report.

**1. Inputs and documentation exports** — `annot_export`, `gene_list_export`, and `config_export` copy the sample annotation, gene list, and workflow config into the results configs dir; `annotate_genes` extracts gene coordinates, isoform counts, and y-max from the gene list and the genome BED.

**2. Bulk coverage chain** — `merge_bams` merges the BAMs of each annotation group with samtools and indexes the merged BAM; `coverage` generates one bigWig per group with bamCoverage.

**3. Single-cell chain (runtime-conditional)** — when sc_enabled is set, `split_sc_bam` splits each single-cell BAM into per-group BAMs by cell barcode (sinto filterbarcodes), `merge_sc_bams` merges those splits, and `coverage_sc` yields the bigWig per sc group. Both routes write bigWigs into the same directory, which the plots and hub read by group name.

**4. Plotting and hub** — `plot_tracks` renders gene/region track plots via gtracks and `ucsc_hub` assembles the hub files; both run after `coverage`, and `annotate_genes` feeds the plot directly.

**5. Opt-in reporting** — with igv_report_enabled set, `make_bed` projects the annotated genes to BED4, then `igv_report` builds the self-contained HTML report over the merged BAMs; `env_export_pygenometracks`, `env_export_sinto`, and `env_export_igv_reports` export pinned conda environments when enabled.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
