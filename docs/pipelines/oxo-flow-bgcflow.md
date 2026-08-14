# Biosynthetic gene cluster analysis across genomes

oxo-flow port of the NBChub/bgcflow v1.1.2 default main path (antismash: true, everything else off): prokka annotation of user-provided FASTA genomes, antiSMASH 7 secondary-metabolite mining with automated database setup, BGC count/overview/summary aggregation, GTDB taxonomy lookup (API with offline-table fallback), MIBiG reference table download, BigSCAPE-compatible comparison preparation (region symlinks, taxonomy tsv, dataset registry, visualization mapping), and conversion of all result tables into a parquet data warehouse.

| | |
|---:|---|
| **Engine** | snakemake |
| **Source** | [NBChub/bgcflow](https://github.com/NBChub/bgcflow) |
| **Pinned version** | `v1.1.2` |
| **Ported** | 2026-08-15 |
| **Rules** | 18 |
| **Tools** | prokka@1.14.6 · antismash@7.1.0 · python@3.9.18 · pandas@2.0.3 · pyarrow@14.0.2 · biopython@1.81 · requests@2.31.0 · alive_progress@3.1.5 |
| **Domain** | genomics |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- copy_custom_fasta
- gtdb_prep
- extract_meta_prokka
- prokka
- format_gbk
- antismash_db_setup
- antismash
- copy_antismash
- bgc_count
- antismash_overview
- downstream_bgc_prep
- antismash_overview_gather
- copy_log_changes
- antismash_summary
- fix_gtdb_taxonomy
- get_mibig_table
- copy_mibig_table
- csv_to_parquet

**Excluded**

- prokka_gbk / copy_custom_genbank / copy_converted_gbk / genbank_to_fna|gff|faa / extract_meta_genbank — genbank input path, off by default (default config ships fna inputs)
- antismash v6 branch — off by default (default is v7)
- write_dependency_versions — bookkeeping, not on the default main path
- seqfu_stats/seqfu_combine — run_seqfu: true only
- mash/mash_convert — run_mash: true only
- fastani/fastani_convert — run_fastani: true only
- checkm/checkm_out — run_checkm: true only
- gtdbtk/gtdbtk_fna_fail/evaluate_gtdbtk_input/install_gtdbtk — run_gtdbtk: true only
- prokka_db_setup + install_* helpers — install rules for off-by-default pipelines
- bigscape/bigscape_no_mibig/bigscape_to_cytoscape/copy_bigscape* — run_bigscape: true only
- bigslice/bigslice_prep/query_bigslice/summarize_bigslice_query/fetch_bigslice_db — run_bigslice: true only
- automlst_wrapper* / prep_automlst_gbk — run_automlst: true only
- arts + 7 arts_* rules — run_arts: true only
- roary/roary_reassign_pangene_categories/roary_out — run_roary: true only
- eggnog/eggnog_roary/eggnog_roary_result_copy — run_eggnog: true only
- deeptfactor + 5 deeptfactor_* rules — run_deeptfactor: true only
- cblaster_genome_db/cblaster_bgc_db — run_cblaster: true only
- gecco/gecco_aggregate/antismash_sideload_gecco — run_gecco: true only
- amrfinderplus/amrfinder_gather — run_amrfinderplus: true only
- metabase_install/metabase_duckdb_plugin/build_warehouse — run_metabase: true only
- ncbi_genome_download/extract_ncbi_information / patric_genome_download/extract_patric_meta/download_patric_tables — non-custom genome sources, off by default
- report rules (copy_readme, copy_template_notebook, mkdocs_py_report, mkdocs_rpy_report, copy_template_rnotebook) — separate 'bgcflow build report' command, not in the main Snakefile

## Fidelity

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| copy_custom_fasta | `copy_custom_fasta` | bash/coreutils | identical command |
| gtdb_prep | `gtdb_prep` | python 3.9.18, requests 2.31.0 | identical command + wget/API fallback |
| extract_meta_prokka | `extract_meta_prokka` | python 3.9.18, pandas 2.0.3 | identical command |
| prokka | `prokka` | prokka 1.14.6 | identical command; `--cpus {threads}` (4) |
| format_gbk | `format_gbk` | python 3.9.18, biopython 1.81 | identical command |
| antismash_db_setup | `antismash_db_setup` | antiSMASH 7.1.0 | v7 branch, identical command |
| antismash | `antismash` | antiSMASH 7.1.0 | v7 branch, identical command incl. reuse-result retry |
| copy_antismash | `copy_antismash` | bash/coreutils | symlink loop, identical |
| bgc_count | `bgc_count` | python 3.9.18, biopython 1.81 | identical command |
| antismash_overview | `antismash_overview` | python 3.9.18 | identical command |
| downstream_bgc_prep | `downstream_bgc_prep` | python 3.9.18, pandas 2.0.3 | identical command |
| antismash_overview_gather | `antismash_overview_gather` | python 3.9.18, pandas 2.0.3 | identical command |
| copy_log_changes | `copy_log_changes` | bash/coreutils | identical command |
| antismash_summary | `antismash_summary` | python 3.9.18, pandas 2.0.3 | identical command |
| fix_gtdb_taxonomy | `fix_gtdb_taxonomy` | python 3.9.18, pandas 2.0.3 | identical command |
| get_mibig_table | `get_mibig_table` | python 3.9.18, pandas 2.0.3 | identical command |
| copy_mibig_table | `copy_mibig_table` | bash/coreutils | identical command |
| csv_to_parquet | `csv_to_parquet` | python 3.9.18, pandas 2.0.3, pyarrow 14.0.2 | identical command |
| prokka_gbk | not ported | prokka 1.14.6 | off by default — only for genbank input files |
| antismash (v6 branch) | not ported | antiSMASH 6.x | off by default — `antismash: v6` config branch |
| write_dependency_versions | not ported | python | metadata bookkeeping, not on the default main path |
| seqfu_stats / seqfu_combine | not ported | seqfu | `run_seqfu: true` only |
| mash / mash_convert | not ported | mash | `run_mash: true` only |
| fastani / fastani_convert | not ported | fastani | `run_fastani: true` only |
| checkm / checkm_out | not ported | checkm | `run_checkm: true` only |
| gtdbtk / gtdbtk_fna_fail / evaluate_gtdbtk_input | not ported | gtdbtk | `run_gtdbtk: true` only |
| prokka_db_setup / install_* rules | not ported | various | install helpers for off-by-default pipelines |
| bigscape / bigscape_no_mibig / bigscape_to_cytoscape / copy_bigscape* | not ported | bigscape | `run_bigscape: true` only |
| bigslice / bigslice_prep / query_bigslice / fetch_bigslice_db | not ported | bigslice | `run_bigslice: true` only |
| automlst_wrapper / automlst_wrapper_out / prep_automlst_gbk | not ported | automlst | `run_automlst: true` only |
| arts + 7 arts_* rules | not ported | arts | `run_arts: true` only |
| roary / roary_reassign_pangene_categories / roary_out | not ported | roary | `run_roary: true` only |
| eggnog / eggnog_roary / eggnog_roary_result_copy | not ported | eggnog-mapper | `run_eggnog: true` only |
| deeptfactor + 5 deeptfactor_* rules | not ported | deeptfactor | `run_deeptfactor: true` only |
| cblaster_genome_db / cblaster_bgc_db | not ported | cblaster | `run_cblaster: true` only |
| gecco / gecco_aggregate / antismash_sideload_gecco | not ported | gecco | `run_gecco: true` only |
| amrfinderplus / amrfinder_gather | not ported | amrfinderplus | `run_amrfinderplus: true` only |
| metabase_install / metabase_duckdb_plugin / build_warehouse | not ported | metabase/duckdb | `run_metabase: true` only |
| ncbi_genome_download / patric_genome_download + patric/ncbi meta rules | not ported | ncbi-genome-download | non-custom genome sources |
| copy_custom_genbank / copy_converted_gbk / genbank_to_fna/gff/faa / format_genbank_meta extras | not ported | python | genbank input path, off by default |
| report rules (copy_readme, copy_template_notebook, mkdocs_*_report) | not ported | jupyter/mkdocs | separate `bgcflow build report` command, not in the main Snakefile |

## Links

- Repository: [oxo-flow-bgcflow](https://github.com/oxo-flow-community/oxo-flow-bgcflow)
- Upstream: [NBChub/bgcflow](https://github.com/NBChub/bgcflow) @ `v1.1.2`
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
