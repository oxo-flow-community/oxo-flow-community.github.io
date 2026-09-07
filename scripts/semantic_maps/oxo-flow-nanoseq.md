**Nanopore sequencing pipeline** (nf-core/nanoseq port): given a raw Nanopore FASTQ and a reference genome, it demultiplexes, quality-checks, aligns, and aggregates a MultiQC report, with optional variant calling, transcript quantification, and RNA-modification analysis.

**1. Input preparation** — `samplesheet_check` validates the samplesheet, then `qcat` demultiplexes the raw FASTQ; each detected barcode becomes the per-sample identity downstream.

**2. Reference prep** — `samtools_faidx` indexes the reference, `get_chrom_sizes` derives chromosome sizes from it, and `gtf2bed` converts a GTF annotation to BED12 when supplied.

**3. Read QC** — `nanoplot` and `fastqc` run in parallel on demultiplexed reads, each skippable.

**4. Alignment** — `minimap2_index` → `minimap2_align` maps reads; with aligner = graphmap2, `graphmap2_index` → `graphmap2_align` runs instead — the two routes are mutually exclusive.

**5. BAM processing** — both routes converge into `samtools_view`, then `samtools_sort` → `samtools_index` (or the combined `samtools_sort_index` under variant calling); `samtools_stats`, `samtools_flagstat`, `samtools_idxstats` run on the sorted BAM.

**6. Coverage tracks** — `bedtools_genomecov` converts the BAM to BEDGraph, `ucsc_bedgraphtobigwig` to BigWig; on cDNA/directRNA protocols `bedtools_bamtobed` → `ucsc_bed12tobigbed` adds BigBed tracks.

**7. Variant calling (DNA, off by default)** — short callers are mutually exclusive: `medaka_variant` → `medaka_bgzip_vcf` → `medaka_tabix_vcf`, `deepvariant` → `deepvariant_tabix_vcf` + `deepvariant_tabix_gvcf`, or `pepper_margin_deepvariant`; structural ones: `sniffles` → `sniffles_sort_vcf` → `sniffles_tabix_vcf` or `cutesv` → `cutesv_sort_vcf` → `cutesv_tabix_vcf`.

**8. Quantification (cDNA/directRNA)** — `bambu` counts transcripts in one step, or `stringtie2` → `stringtie_merge` → `subread_featurecounts`; the routes are mutually exclusive, and counts feed `deseq2`/`dexseq` (bambu) or `deseq2_featurecounts`/`dexseq_featurecounts` (featureCounts).

**9. RNA modifications (directRNA)** — `nanopolish_index_eventalign` event-aligns reads; `xpore_dataprep` → `xpore_diffmod` and `m6anet_dataprep` → `m6anet_inference` fan out in parallel.

**10. Reporting** — `dumpsoftwareversions` merges tool versions; `multiqc` aggregates the FastQC and samtools results into one report.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
