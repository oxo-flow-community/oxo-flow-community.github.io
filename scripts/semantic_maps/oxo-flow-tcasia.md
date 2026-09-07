**TCASIA alternative-splicing pipeline**: given paired-end RNA-seq reads and a reference genome, it quality-filters and aligns them, then quantifies alternative splicing with four callers — rMATS, MAJIQ, SUPPA2 and SplAdder — each producing per-event PSI output.

**1. Input QC and alignment** — `alignment::fastp_qc` trims and quality-filters the paired reads; `alignment::star_align` runs the two-pass STAR alignment with gene counts; `alignment::sort_bam` coordinate-sorts the BAM. From that sorted BAM, `alignment::index_bam` builds the BAI index and `alignment::featurecounts` counts reads per gene — and the same sorted BAM feeds every alternative-splicing caller downstream.

**2. SUPPA2 track (from raw reads, runs in parallel)** — `as_calling::salmon_quant` quantifies transcripts directly from raw FASTQ; `as_calling::select_suppa_fields` extracts the isoform TPM column; `as_calling::format_suppa_fields` strips the transcript prefix; `as_calling::suppa_run` computes per-event PSI.

**3. rMATS** — `as_calling::rmats_create_input` writes the single-BAM input list, then `as_calling::rmats_run` computes PSI values per sample.

**4. MAJIQ (gated on the run_majiq flag; the academic license is required)** — `as_calling::majiq_create_ini` writes the build configuration, `as_calling::majiq_build` builds the splice graph, `as_calling::majiq_psi` quantifies PSI per local splicing variation; then both `as_calling::voila_modulize` (Voilà modules) and `as_calling::voila_tsv` (TSV table) consume the splice graph and PSI outputs.

**5. SplAdder** — `as_calling::spladder_run` detects alternative-splicing events directly from the sorted BAM.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
