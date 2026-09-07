**Viral genome reconstruction pipeline** (nf-core/viralrecon port): given Illumina amplicon reads plus a viral FASTA, GFF, and primer scheme, it trims, aligns, calls and annotates intrahost variants, calls consensus and lineages, assembles de novo, and reports it all in MultiQC.

**1. Reference preparation** — `gunzip_fasta`, `gunzip_gff`, and `gunzip_primer_bed` uncompress gzipped references; `prepare_genome` indexes the FASTA while `build_bowtie2_index`, `build_snpeff_db`, `make_blast_db`, and `get_nextclade_dataset` build the alignment, snpEff, BLAST, and Nextclade databases. `collapse_primers` and `get_primer_fasta` prepare amplicon intervals and primer sequences; `untar_kraken2_db` or `kraken2_build` supplies the host database.

**2. Read QC and alignment** — `cat_fastq` concatenates per-sample reads, `fastp` trims them, and `fastqc_raw`/`fastqc_trim` check pre- and post-trim quality. `kraken2` strips host reads, `align_bowtie2` maps the trimmed reads, `bam_sort_index` sorts and indexes the BAM, and the amplicon branch's `ivar_trim` → `bam_sort_index_trimmed` removes primer sequences.

**3. Coverage and lineage deconvolution** — `picard_metrics` collects alignment metrics, `mosdepth_genome` → `plot_mosdepth_genome` and `mosdepth_amplicon` → `plot_mosdepth_amplicon` plot coverage, and `freyja_variants` feeds `freyja_demix` and `freyja_boot`; if the database must be downloaded, `freyja_update` feeds `freyja_demix_updated`/`freyja_boot_updated` instead.

**4. Variant calling, annotation, and consensus** — `call_variants_ivar` → `ivar_to_vcf` → `sort_vcf` is the amplicon default; the metagenomic `call_variants_bcftools` → `norm_vcf_bcftools` covers untrimmed runs. Both converge on `snpeff_ann` → `snpsift_extract`, and after `consensus_filter`/`consensus_filter_bcftools`, `consensus_call` (or `consensus_ivar`) emits the consensus feeding `quast_consensus`, `nextclade` → `nextclade_clade_mqc`, `pangolin`, and `plot_base_density`.

**5. Variant long table and assembly** — `variants_long_table` and its bcftools counterpart `variants_long_table_bcftools` merge called variants, snpEff fields, and Pangolin lineages. In parallel, `cutadapt` primer-trims the host-stripped reads that `assemble_spades` (or `assemble_unicycler`, `assemble_minia`) scaffolds; each assembler branch adds BLAST, QUAST, and ABACAS rules (`blast_assembly`, `quast_assembly_minia`) plus Bandage and plasmidID.

**6. Report aggregation** — `multiqc` collates quality, alignment, coverage, variant, and lineage metrics into one HTML report.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
