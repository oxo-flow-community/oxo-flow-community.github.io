**BGCflow pipeline**: given assembled genomes, it annotates them with prokka, detects biosynthetic gene clusters with antiSMASH, and assembles comparison datasets, project summary tables, and a parquet data warehouse.

**1. Genome input and metadata** — `copy_custom_fasta` stages user FASTA files (`genbank_to_fna` covers the genbank route); `extract_meta_prokka` pulls organism metadata and `gtdb_prep` fetches GTDB taxonomy per genome. Optional branches run in parallel: `seqfu_stats` → `seqfu_combine`, `mash` → `mash_convert`, `fastani` → `fastani_convert`, `install_checkm` → `checkm`, and `gtdbtk`.

**2. Annotation** — `prokka` annotates (`prokka_gbk` takes genbank input), and `format_gbk` stamps BGCflow metadata comments onto the prokka genbank. Analyses off prokka: `install_amrfinder` → `amrfinderplus` → `amrfinder_gather`, `roary` → `roary_out`, `install_eggnog` → `eggnog`, `deeptfactor_setup` → `deeptfactor` → `deeptfactor_to_json` → `deeptfactor_summary`; `gecco`, `cblaster_genome_db`, and `prep_automlst_gbk` → `automlst_wrapper` → `automlst_wrapper_out` read the formatted genbank.

**3. antiSMASH mining** — `antismash_db_setup` prepares the reference databases; `antismash` (v7; `antismash_v6` for the v6 branch) then detects clusters and fans out to `copy_antismash`, `bgc_count`, `antismash_overview`, and the optional `arts` screen, plus the `bigscape` branch.

**4. Comparison preparation and summary** — `fix_gtdb_taxonomy` merges the per-genome taxonomy into a table feeding `downstream_bgc_prep`, staging BGC folders for optional `bigslice_prep` → `bigslice` (via `install_bigslice`); a separate BiG-FAM chain runs `fetch_bigslice_db` → `query_bigslice` → `summarize_bigslice_query` → `annotate_bigfam_hits`. `antismash_overview_gather`, `copy_log_changes`, and `bgc_count` converge in `antismash_summary`.

**5. Data warehouse** — `get_mibig_table` fetches the MIBiG reference set and `copy_mibig_table` copies it into the project tables; the antiSMASH summary, MIBiG table, and GTDB taxonomy converge into `csv_to_parquet`.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
