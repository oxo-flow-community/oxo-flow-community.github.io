## Semantic map - how to read it

## Short names and groups (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| genome | copy_custom_fasta, genbank_to_fna, copy_custom_genbank, ncbi_genome_download |
| prokka | extract_meta_prokka, prokka, format_gbk, prokka_gbk |
| antismash | antismash_db_setup, antismash, antismash_v6, copy_antismash |
| summarize | bgc_count, antismash_overview, downstream_bgc_prep, antismash_overview_gather, copy_log_changes, antismash_summary |
| report | get_mibig_table, copy_mibig_table, csv_to_parquet |
| taxo | gtdb_prep, install_gtdbtk, gtdbtk, fix_gtdb_taxonomy |
| qc | seqfu_stats, seqfu_combine, mash, mash_convert, fastani, fastani_convert |
| checkm | install_checkm, checkm |
| amr | install_amrfinder, amrfinderplus, amrfinder_gather |
| roary | roary, roary_out |
| eggnog | install_eggnog, eggnog |
| bgc_alt | gecco, cblaster_genome_db, arts, bigscape |
| bigslice | install_bigslice, bigslice_prep, bigslice, fetch_bigslice_db, query_bigslice, summarize_bigslice_query, annotate_bigfam_hits |
| automlst | install_automlst_wrapper, prep_automlst_gbk, automlst_wrapper, automlst_wrapper_out |
| deeptfactor | deeptfactor_setup, deeptfactor, deeptfactor_to_json, deeptfactor_summary |
| versions | write_dependency_versions |

Every drawn edge is a real engine edge (subset check at generation).
