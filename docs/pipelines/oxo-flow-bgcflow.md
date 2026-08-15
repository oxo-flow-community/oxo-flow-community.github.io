# Biosynthetic gene cluster (BGC) genome mining: annotation, antiSMASH and data warehouse

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

End-to-end biosynthetic gene cluster (BGC) analysis of user-provided bacterial genomes: prokka annotation, antiSMASH 7 secondary-metabolite mining with automated database setup, per-genome BGC counts and overview tables, GTDB taxonomy lookup, MIBiG reference table download, BigSCAPE-compatible comparison preparation (symlinks, taxonomy, dataset registry, visualization mapping), and conversion of all result tables into a parquet data warehouse — ready for downstream comparison and exploration.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | genome-mining |
| **Rules** | 18 |
| **Tools** | prokka · antismash · python · pandas · pyarrow · biopython · requests · alive_progress |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [NBChub/bgcflow](https://github.com/NBChub/bgcflow) |
| **Pinned version** | `v1.1.2` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned versions (declared in main.oxoflow: envs/antismash.yaml, envs/prokka.yaml, envs/bgc_analytics.yaml; a few antiSMASH helper packages use unpinned ranges)

**Requirements.**
- genome FASTA per genome at {config.raw_dir}/fasta/<genome_id>.fna (raw_dir defaults to test/fixtures/raw; .fna/.fasta/.fa accepted)
- sample table config/samples.csv — columns genome_id,source,organism,genus,species,strain
- network access on first run: antiSMASH databases (~several GB, into resources/antismash_db), GTDB bac120_metadata_r220.tsv fallback table, MIBiG JSON 3.1
- optional: GTDB offline taxonomy TSVs via config.gtdb_tax_paths
- compute: up to 4 CPUs per rule (prokka, antiSMASH); no explicit memory limits — antiSMASH dominates
- disk: several GB for downloaded resources (antiSMASH DB, MIBiG) plus the data/ output tree

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-bgcflow
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `antismash_db_path` | `resources/antismash_db` | upstream resources_path.antismash_db | `antismash`, `antismash_db_setup` |
| `antismash_major` | `7` | antiSMASH (upstream rule_parameters.antismash + envs/antismash.yaml) | — |
| `antismash_taxon` | `bacteria` | upstream env var BGCFLOW_ANTISMASH_MODE | `antismash` |
| `antismash_version` | `7.1.0` | derived from envs/antismash.yaml pip pin git@7-1-0-1 | `antismash`, `antismash_overview`, `antismash_overview_gather`, `antismash_summary`, `bgc_count`, `copy_antismash`, `copy_log_changes`, `csv_to_parquet`, `downstream_bgc_prep` |
| `bgc_dataset` | `data/interim/bgcs/datasets.tsv` | — | `downstream_bgc_prep` |
| `bgcflow_version` | `1.1.2` | BGCflow housekeeping | `format_gbk` |
| `gtdb_api_base` | `https://gtdb-api.ecogenomic.org` | — | `gtdb_prep` |
| `gtdb_offline` | `False` | upstream: use_gtdb_api False -> offline mode | `gtdb_prep` |
| `gtdb_release` | `220.0` | GTDB taxonomy (upstream rule_parameters.install_gtdbtk + use_gtdb_api) | `gtdb_prep` |
| `gtdb_release_major` | `220` | GTDB release major version (upstream: release.split('.')[0]) | `gtdb_prep` |
| `gtdb_release_version` | `r220` | GTDB release id (e.g. r214, r220) | — |
| `gtdb_tax_paths` | `[]` | upstream GTDB_PATHS: space-separated user gtdb-tax tsv(s) | `gtdb_prep` |
| `input_type` | `fna` | upstream get_input_location(): fna \| gbk | — |
| `mibig_version` | `3.1` | MIBiG JSON release used by get_mibig_table | `get_mibig_table` |
| `project` | `genomes` | Project / input genomes (upstream: config.yaml `projects` + data/raw/fasta) | `antismash_overview_gather`, `antismash_summary`, `copy_log_changes`, `copy_mibig_table`, `csv_to_parquet`, `downstream_bgc_prep`, `fix_gtdb_taxonomy` |
| `raw_dir` | `test/fixtures/raw` | directory containing fasta/<genome_id>.fna | `copy_custom_fasta` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-bgcflow rule-level DAG](/assets/dag/oxo-flow-bgcflow.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

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
- antismash v6 branch — off by default (config default is antismash v7)
- write_dependency_versions — dependency bookkeeping, not on the default main path
- seqfu_stats/seqfu_combine — run_seqfu: true only
- mash/mash_convert — run_mash: true only
- fastani/fastani_convert — run_fastani: true only
- checkm/checkm_out — run_checkm: true only
- gtdbtk/gtdbtk_fna_fail/evaluate_gtdbtk_input/install_gtdbtk — run_gtdbtk: true only
- prokka_db_setup, install_* helpers — install rules for off-by-default pipelines
- bigscape/bigscape_no_mibig/bigscape_to_cytoscape/copy_bigscape/copy_bigscape_zip — run_bigscape: true only
- bigslice/bigslice_prep/query_bigslice/summarize_bigslice_query/fetch_bigslice_db — run_bigslice: true only
- automlst_wrapper/automlst_wrapper_out/prep_automlst_gbk/install_automlst_wrapper — run_automlst: true only
- arts + arts_extract/arts_knownhits_combine/arts_allhits_combine/arts_bgctable_combine/arts_coretable_combine/arts_final — run_arts: true only
- roary/roary_reassign_pangene_categories/roary_out — run_roary: true only
- eggnog/eggnog_roary/eggnog_roary_result_copy — run_eggnog: true only
- deeptfactor + deeptfactor_setup/to_json/summary/roary — run_deeptfactor: true only
- cblaster_genome_db/cblaster_bgc_db — run_cblaster: true only
- gecco/gecco_aggregate/antismash_sideload_gecco — run_gecco: true only
- amrfinderplus/amrfinder_gather — run_amrfinderplus: true only
- metabase_install/metabase_duckdb_plugin/build_warehouse — run_metabase: true only
- ncbi_genome_download/extract_ncbi_information / patric_genome_download/extract_patric_meta/download_patric_tables — non-custom genome sources, off by default
- report rules (copy_readme, copy_template_notebook, mkdocs_py_report, mkdocs_rpy_report, copy_template_rnotebook) — separate 'bgcflow build report' command, not part of the main Snakefile default path

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
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
