**SRA data fetch pipeline**: give it a list of SRA/ENA/DDBJ accessions (e.g. `SRR9984183`) and it validates them, fetches run metadata, downloads FASTQ through several backends, and emits a standard samplesheet ready for nf-core pipelines — plus a MultiQC config.

**1. Input validation** — the `ids` sample group defines the accessions to fetch; `check_ids` validates them against the SRA/ENA/DDBJ/GEO accession patterns and deduplicates; everything downstream is gated on this list, and `sra_ids_to_runinfo` pulls the ENA run metadata (runinfo) for each validated id.

**2. Download manifest** — `sra_runinfo_to_ftp` turns the metadata into one download manifest per sample; this is the common entry point of every download route.

**3. FASTQ download (parallel tool backends)** — from the manifest the pipeline fans out several download routes: `sra_fastq_ftp` over FTP; `sra_prefetch` prefetches and `sra_fastq_sratools` converts to FASTQ; `sra_fastq_aspera` over Aspera; plus a fallback chain (`sra_prefetch_fallback` → `sra_fastq_sratools_fallback`, and `sra_fastq_ftp_aspera_fallback`) and a dbGaP-specific chain (`sra_prefetch_dbgap` → `sra_fastq_sratools_dbgap`). Which route actually runs depends on the data source and runtime conditions — the results converge into the same samplesheet generation step.

**4. Samplesheet assembly and aggregation** — `sra_to_samplesheet` consolidates metadata and all FASTQ routes into the downstream samplesheet; `combine_samplesheets` and `combine_mappings` then merge per-sample sheets and mappings (the `nf_core_pipeline` config can tailor row format for a specific downstream nf-core pipeline).

**5. Reporting** — after the mappings are combined, `multiqc_mappings_config` generates the MultiQC configuration used by the downstream aggregate report.

*Verified: every rule name above is a real rule of `main.oxoflow` (oxo-flow validate); the described order follows the actual rule dependencies.*
