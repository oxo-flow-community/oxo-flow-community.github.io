**SRA-powered RNA-seq pipeline**: given locally downloaded .sra archives and a metadata sheet, it converts archives to FASTQ, trims with fastp, aligns with STAR while counting per-gene reads, builds normalized bigWig signal tracks, and runs DESeq2 differential expression with ashr shrinkage.

**1. Archive handoff** — `get_sra` verifies the locally downloaded archives and symlinks each into sra/<SRR>/<SRR>.sra; `sra_dump` converts every sample's archives to FASTQ with fasterq-dump.

**2. Per-sample merge (PE vs SE route)** — from the dumped FASTQs, `merge_R1_data` and `merge_R2_data` concatenate all SRR runs of a sample into one R1/R2 pair, while `merge_data` concatenates the single-end reads instead; each sample takes one route according to its paired metadata.

**3. Trim, align, count** — paired reads pass through `data_clean_pair` (fastp) into `align_and_count` (STAR with GeneCounts quanting, yielding a sorted BAM and a per-gene ReadsPerGene table); single-end reads go through `data_clean_single` and `align_and_count_single`. Only one of these routes runs per sample.

**4. Index and signal tracks** — both alignment routes converge here: `build_bam_index` indexes each BAM with samtools, and `bamtobw` uses bamCoverage to emit BPM-normalized bigWig tracks from the BAM plus its index.

**5. Count matrix and differential expression** — `combine_count` merges all per-sample ReadsPerGene tables into one count matrix; `DGE_analysis` runs DESeq2 with ashr shrinkage to output the final R object, then cleans up the alignment directory and optionally emails results.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
