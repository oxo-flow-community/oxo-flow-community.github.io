---
title: "Biosynthetic gene cluster (BGC) genome mining: annotation, antiSMASH and data warehouse"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-bgcflow</span></div>
<div class="ox-detail-cols">
<div>
<h1>Biosynthetic gene cluster (BGC) genome mining: annotation, antiSMASH and data warehouse</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>
<p>End-to-end biosynthetic gene cluster (BGC) analysis of user-provided bacterial genomes: prokka annotation, antiSMASH 7 secondary-metabolite mining with automated database setup, per-genome BGC counts and overview tables, GTDB taxonomy lookup, MIBiG reference table download, BigSCAPE-compatible comparison preparation (symlinks, taxonomy, dataset registry, visualization mapping), and conversion of all result tables into a parquet data warehouse — ready for downstream comparison and exploration.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">60</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 4 CPUs per rule (antiSMASH)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genome-mining</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/NBChub/bgcflow">NBChub/bgcflow</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v1.1.2</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2296.1"><code>10.48546/workflowhub.workflow.2296.1</code></a></span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs input genomes and the antiSMASH database — see Requirements.

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
#    NOTE: bioconda currently ships 0.10.2, older than the >= 0.12.0
#    minimum of every catalog entry — prefer the release binary.

# 2. get this workflow (clones the repo, auto-discovers the workflow,
#    sanity-parses it with the engine)
oxo-flow pull gh:oxo-flow-community/oxo-flow-bgcflow
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-bgcflow
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. The list below names the rules that read each key.</p>
<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>antismash_db_path</code><span class="ox-param-default">resources/antismash_db</span></div>
<p class="ox-param-desc">upstream resources_path.antismash_db</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>antismash</code> <code>antismash_db_setup</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>antismash_major</code><span class="ox-param-default">7</span></div>
<p class="ox-param-desc">antiSMASH (upstream rule_parameters.antismash + envs/antismash.yaml)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>antismash_v6</code> <code>write_dependency_versions</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>antismash_taxon</code><span class="ox-param-default">bacteria</span></div>
<p class="ox-param-desc">upstream env var BGCFLOW_ANTISMASH_MODE</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>antismash</code> <code>antismash_v6</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>antismash_version</code><span class="ox-param-default">7.1.0</span></div>
<p class="ox-param-desc">matches envs/antismash.yaml bioconda::antismash=7.1.0</p>
<details class="ox-param-usedby"><summary>used by 17 rules</summary>
<div class="ox-param-rules"><code>annotate_bigfam_hits</code> <code>antismash</code> <code>antismash_overview</code> <code>antismash_overview_gather</code> <code>antismash_summary</code> <code>antismash_v6</code> <code>arts</code> <code>bgc_count</code> <code>bigscape</code> <code>bigslice</code> <code>bigslice_prep</code> <code>copy_antismash</code> <code>copy_log_changes</code> <code>csv_to_parquet</code> <code>downstream_bgc_prep</code> <code>query_bigslice</code> <code>summarize_bigslice_query</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>bgc_dataset</code><span class="ox-param-default">data/interim/bgcs/datasets.tsv</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>downstream_bgc_prep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>bgcflow_version</code><span class="ox-param-default">1.1.2</span></div>
<p class="ox-param-desc">BGCflow housekeeping</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>format_gbk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gecco_version</code><span class="ox-param-default">0.9.10</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gecco</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtdb_api_base</code><span class="ox-param-default">https://gtdb-api.ecogenomic.org</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gtdb_prep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtdb_offline</code><span class="ox-param-default">False</span></div>
<p class="ox-param-desc">upstream: use_gtdb_api False -&gt; offline mode</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gtdb_prep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtdb_release</code><span class="ox-param-default">220.0</span></div>
<p class="ox-param-desc">GTDB taxonomy (upstream rule_parameters.install_gtdbtk + use_gtdb_api)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>gtdb_prep</code> <code>install_gtdbtk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtdb_release_major</code><span class="ox-param-default">220</span></div>
<p class="ox-param-desc">GTDB release major version (upstream: release.split(&#x27;.&#x27;)[0])</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>gtdb_prep</code> <code>install_gtdbtk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtdb_release_version</code><span class="ox-param-default">r220</span></div>
<p class="ox-param-desc">GTDB release id (e.g. r214, r220)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>install_gtdbtk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtdb_tax_paths</code><span class="ox-param-default">[]</span></div>
<p class="ox-param-desc">upstream GTDB_PATHS: space-separated user gtdb-tax tsv(s)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gtdb_prep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>input_type</code><span class="ox-param-default">fna</span></div>
<p class="ox-param-desc">upstream get_input_location(): fna | gbk</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>copy_custom_fasta</code> <code>copy_custom_genbank</code> <code>format_gbk</code> <code>genbank_to_fna</code> <code>prokka</code> <code>prokka_gbk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>mibig_version</code><span class="ox-param-default">3.1</span></div>
<p class="ox-param-desc">MIBiG JSON release used by get_mibig_table</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>get_mibig_table</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ncbi_genera</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>ncbi_genome_download</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>project</code><span class="ox-param-default">genomes</span></div>
<p class="ox-param-desc">Project / input genomes (upstream: config.yaml <code>projects</code> + data/raw/fasta)</p>
<details class="ox-param-usedby"><summary>used by 29 rules</summary>
<div class="ox-param-rules"><code>amrfinder_gather</code> <code>annotate_bigfam_hits</code> <code>antismash_overview_gather</code> <code>antismash_summary</code> <code>automlst_wrapper</code> <code>automlst_wrapper_out</code> <code>bigscape</code> <code>bigslice</code> <code>bigslice_prep</code> <code>cblaster_genome_db</code> <code>checkm</code> <code>copy_log_changes</code> <code>copy_mibig_table</code> <code>csv_to_parquet</code> <code>deeptfactor_summary</code> <code>downstream_bgc_prep</code> <code>fastani</code> <code>fastani_convert</code> <code>fix_gtdb_taxonomy</code> <code>gtdbtk</code> <code>mash</code> <code>mash_convert</code> <code>prep_automlst_gbk</code> <code>query_bigslice</code> <code>roary</code> <code>roary_out</code> <code>seqfu_combine</code> <code>summarize_bigslice_query</code> <code>write_dependency_versions</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>project_source</code><span class="ox-param-default">custom</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>ncbi_genome_download</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>raw_dir</code><span class="ox-param-default">test/fixtures/raw</span></div>
<p class="ox-param-desc">directory containing fasta/&lt;genome_id&gt;.fna</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>copy_custom_fasta</code> <code>copy_custom_genbank</code> <code>genbank_to_fna</code> <code>prokka_gbk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_amrfinderplus</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>amrfinder_gather</code> <code>amrfinderplus</code> <code>install_amrfinder</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_arts</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>arts</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_automlst</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream pipelines.automlst-wrapper</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>automlst_wrapper</code> <code>automlst_wrapper_out</code> <code>install_automlst_wrapper</code> <code>prep_automlst_gbk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_bigscape</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bigscape</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_bigslice</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream pipelines.bigslice</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>bigslice</code> <code>bigslice_prep</code> <code>install_bigslice</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_cblaster</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>cblaster_genome_db</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_checkm</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>checkm</code> <code>install_checkm</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_deeptfactor</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream pipelines.deeptfactor</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>deeptfactor</code> <code>deeptfactor_setup</code> <code>deeptfactor_summary</code> <code>deeptfactor_to_json</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_eggnog</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>eggnog</code> <code>install_eggnog</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_fastani</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>fastani</code> <code>fastani_convert</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_gecco</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gecco</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_gtdbtk</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>gtdbtk</code> <code>install_gtdbtk</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_mash</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>mash</code> <code>mash_convert</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_query_bigslice</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream pipelines.query-bigslice (needs the 18GB BiG-FAM bundle)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>annotate_bigfam_hits</code> <code>fetch_bigslice_db</code> <code>query_bigslice</code> <code>summarize_bigslice_query</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_roary</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>roary</code> <code>roary_out</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_seqfu</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">see rules/branches.oxoflow; samples_list is the engine-injected sample ids</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>seqfu_combine</code> <code>seqfu_stats</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>write_dependency_versions</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>write_dependency_versions</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<img src="/assets/dag/oxo-flow-bgcflow.svg?v=a6da5ef0bf" alt="oxo-flow-bgcflow pipeline overview" loading="lazy">

<p class="ox-dag-caption">figure · oxo-flow-bgcflow — End-to-end biosynthetic gene cluster (BGC) analysis of user-provided bacterial genomes: prokka annotation, antiSMASH 7 secondary-metabolite mining with automated database setup, per-genome BGC counts and overview tables, GTDB taxonomy lookup, MIBiG reference table download, BigSCAPE-compatible comparison preparation (symlinks, taxonomy, dataset registry, visualization mapping), and conversion of all result tables into a parquet data warehouse — ready for downstream comparison and exploration.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

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
- fix_gtdb_taxonomy
- downstream_bgc_prep
- antismash_overview_gather
- copy_log_changes
- antismash_summary
- get_mibig_table
- copy_mibig_table
- csv_to_parquet
- seqfu_stats
- seqfu_combine
- mash
- mash_convert
- fastani
- fastani_convert
- install_checkm
- checkm
- install_gtdbtk
- gtdbtk
- install_amrfinder
- amrfinderplus
- amrfinder_gather
- roary
- roary_out
- install_eggnog
- eggnog
- gecco
- cblaster_genome_db
- arts
- bigscape
- antismash_v6
- prokka_gbk
- copy_custom_genbank
- genbank_to_fna
- ncbi_genome_download
- write_dependency_versions
- install_bigslice
- bigslice_prep
- bigslice
- fetch_bigslice_db
- query_bigslice
- summarize_bigslice_query
- annotate_bigfam_hits
- install_automlst_wrapper
- prep_automlst_gbk
- automlst_wrapper
- automlst_wrapper_out
- deeptfactor_setup
- deeptfactor
- deeptfactor_to_json
- deeptfactor_summary

**Excluded**

- metabase_install / metabase_duckdb_plugin / build_warehouse — metabase.smk + build-database.smk are not in the main Snakefile; upstream runs them via its own entrypoint `workflow/Metabase` / `workflow/Database` (`snakemake --snakefile workflow/<Name>`), which has no oxo-flow port — note there is **no** wrapper CLI: `workflow/bgcflow/bgcflow/cli.py` is a console-script stub and the README's `bgcflow build report` is unimplemented; the warehouse branch additionally needs a live Metabase server + credentials
- patric_genome_download / download_patric_tables / extract_patric_meta — download endpoint ftp.patricbrc.org is dead: PATRIC was decommissioned in 2023 (merged into BV-BRC); verified 550 / connection refused 2026-08-06
- report rules (copy_readme, copy_template_notebook, mkdocs_py_report, mkdocs_rpy_report, copy_template_rnotebook) — upstream `report.smk` has no entrypoint include at all (the advertised `bgcflow build report` CLI is unimplemented upstream); no pipeline gate to mirror
- Upstream subworkflow entrypoints with no oxo-flow coverage: PPanGGOLiN (`workflow/ppanggolin`, 26 rules incl. ppanggolin_roary), LsABGC (`workflow/lsabgc`, 5), Alleleome (`workflow/Alleleome`, 3), BGC comparison (`workflow/BGC`, 19: clinker / interproscan / mmseqs2 / getphylo / downstream_bgc_prep_selection), Database extras (6: antismash_json_extract / build_dna_sequences_table / build_regions_table / build_cdss_table / get_dbt_template / build_database) + antismash_db_duckdb — none reachable from the main Snakefile entrypoint, none ported
- Main-path upstream rules without ported counterparts: create_diamond_db (rules/diamond.smk), mlst (rules/mlst.smk), refseq_masher (rules/refseq_masher.smk), get_project_metadata (rules/bgc_analytics.smk) — the port's 42 branches.oxoflow rules cover the documented gate-set, not these
- Upstream rules acknowledged group-wise in the README fidelity table without ported counterparts: checkm_out, gtdbtk_fna_fail + evaluate_gtdbtk_input, prokka_db_setup, bigscape_no_mibig + bigscape_to_cytoscape + copy_bigscape (install_bigscape group), arts_extract + 7 arts_* combine/final rules (install pydude... group), roary_reassign_pangene_categories + eggnog_roary + eggnog_roary_result_copy + deeptfactor_roary + diamond_roary, cblaster_bgc_db, antismash_sideload_gecco + gecco_aggregate — see the README fidelity table for the full list

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
| prokka_gbk | `prokka_gbk` | prokka 1.14.6 | `when = config.input_type == 'gbk'`; default copy_custom_fasta/prokka/format_gbk now gate on `'fna'` (upstream resolves the same producer overlap with input-function branching) |
| antismash (v6 branch) | `antismash_v6` | antiSMASH 6.x | `when = config.antismash_major == '6'`, envs/antismash6.yaml (upstream antismash_v6.yaml verbatim) |
| write_dependency_versions | `write_dependency_versions` | python 3.9.18, pyyaml 6.0.1 | `when = config.write_dependency_versions`; upstream get_dependencies.py ported as scripts/write_dependency_versions.py (metadata/dependency_versions.json, upstream output path) |
| seqfu_stats / seqfu_combine | `seqfu_stats` / `seqfu_combine` | seqfu 1.20.3 | `when = config.run_seqfu`; combine gathers via expand_inputs |
| mash / mash_convert | `mash` / `mash_convert` | mash 2.3 | `when = config.run_mash`; convert_triangular_matrix.py verbatim |
| fastani / fastani_convert | `fastani` / `fastani_convert` | fastani 1.33 | `when = config.run_fastani` |
| install_checkm / checkm / checkm_out | `install_checkm` / `checkm` | checkm-genome 1.2.2 | `when = config.run_checkm`; the 2015 CheckM DB download is the upstream install rule; checkm_out (report-table extraction via get_checkm_data.py) not ported |
| install_gtdbtk / gtdbtk / gtdbtk_fna_fail / evaluate_gtdbtk_input | `install_gtdbtk` / `gtdbtk` | gtdbtk 2.4.0 | `when = config.run_gtdbtk`; the release package download is multi-GB (upstream install rule); the gtdbtk_fna_fail rule + evaluate_gtdbtk_input branching (fna-fail reroute) not ported |
| prokka_db_setup / install_* rules | `install_checkm` / `install_gtdbtk` / `install_eggnog` | various | install rules for the off-by-default pipelines, same downloads as upstream |
| bigscape / bigscape_no_mibig / copy_bigscape_zip / bigscape_to_cytoscape / copy_bigscape | `bigscape` | bigscape (conda) | `when = config.run_bigscape`; needs the pfam + MIBiG databases in resources/ (upstream install_bigscape step); bigscape_no_mibig / copy_bigscape_zip / bigscape_to_cytoscape / copy_bigscape (report-view variants) not ported — documented in the rule header |
| bigslice / bigslice_prep | `bigslice` / `bigslice_prep` | bigslice (NBChub fork) | `when = config.run_bigslice`; models downloaded by install_bigslice (upstream env post-deploy equivalent); env pip-installs the NBChub fork @c0085de (original medema-group/bigslice discontinued) |
| fetch_bigslice_db / query_bigslice / summarize_bigslice_query / annotate_bigfam_hits | `fetch_bigslice_db` / `query_bigslice` / `summarize_bigslice_query` / `annotate_bigfam_hits` | bigslice + python | `when = config.run_query_bigslice`; fetch_bigslice_db downloads the BiG-FAM full-run-result bundle (~18GB, bioinformatics.nl — verified alive 2026-08) |
| automlst_wrapper / automlst_wrapper_out / prep_automlst_gbk / install_automlst_wrapper | `automlst_wrapper` / `automlst_wrapper_out` / `prep_automlst_gbk` / `install_automlst_wrapper` | automlst-simplified-wrapper 0.1.2 (python 2.7 env) | `when = config.run_automlst`; install downloads the release zip (not a git clone); scripts verbatim |
| arts + 6 arts_* rules | `arts` | arts env (upstream pins) | `when = config.run_arts`; needs the ARTS reference bundle in resources/arts; arts_extract + the 5 arts_*_combine/final report rules not ported (arts_extract_all.py is shipped but no rule consumes it) |
| roary / roary_out / roary_reassign_pangene_categories / eggnog_roary / eggnog_roary_result_copy / deeptfactor_roary / diamond_roary | `roary` / `roary_out` | roary 3.13.0 | `when = config.run_roary`; verbatim flags (-i 80 -g 80000 -e -n -r -v); the reassign / eggnog_roary / deeptfactor_roary / diamond_roary report rules not ported |
| install_eggnog / eggnog | `install_eggnog` / `eggnog` | eggnog-mapper 2.1.6 | `when = config.run_eggnog`; DB download + create_dbs.py as upstream |
| deeptfactor / deeptfactor_setup / deeptfactor_to_json / deeptfactor_summary | `deeptfactor` / `deeptfactor_setup` / `deeptfactor_to_json` / `deeptfactor_summary` | deeptfactor (bitbucket, ~23MB) | `when = config.run_deeptfactor`; setup git-clones the unpinned bitbucket repo (model bundle included — verified public 2026-08); env is upstream's python 3.6 + pytorch 1.10.2 pin |
| cblaster_genome_db / cblaster_bgc_db | `cblaster_genome_db` | cblaster 1.3.18 | `when = config.run_cblaster`; verbatim makedb over prokka GBKs; cblaster_bgc_db (MIBiG-BGC database build) not ported |
| gecco / antismash_sideload_gecco / gecco_aggregate | `gecco` | gecco 0.9.10 | `when = config.run_gecco`; verbatim gecco run --antismash-sideload; antismash_sideload_gecco + gecco_aggregate (report tables) not ported |
| amrfinderplus / amrfinder_gather | `amrfinderplus` / `amrfinder_gather` | ncbi-amrfinderplus | `when = config.run_amrfinderplus`; verbatim flags; gather_amrfinder.py verbatim |
| create_diamond_db | not ported | diamond | rules/diamond.smk (main Snakefile include): concatenates prokka `.faa` + `diamond makedb`; no ported rule |
| mlst | not ported | mlst | rules/mlst.smk (main Snakefile include): `mlst --csv` per genome; the port ships `automlst_wrapper` instead (different tool, gated) |
| refseq_masher | not ported | refseq-masher | rules/refseq_masher.smk (main Snakefile include): `refseq_masher matches --top-n-results 10` |
| get_project_metadata | not ported | peppy | rules/bgc_analytics.smk; the port only mentions it in a comment (`branches.oxoflow`) |
| metabase_install / metabase_duckdb_plugin / build_warehouse | not ported | metabase/duckdb | metabase.smk + build-database.smk are not in the main Snakefile; upstream reaches them via its own entrypoint `workflow/Metabase` / `workflow/Database` (`snakemake --snakefile workflow/<Name>`) — no oxo-flow port of those entrypoints. There is no wrapper CLI: `workflow/bgcflow/bgcflow/cli.py` is a console-script stub and the advertised `bgcflow build report` is unimplemented; the warehouse branch additionally needs a live Metabase server + credentials |
| ncbi_genome_download / extract_ncbi_information (+ patric meta rules) | `ncbi_genome_download` | ncbi-genome-download | `when = config.project_source == 'ncbi'`; deviation: bulk genus download via `--genera` (upstream fetches per-accession with `-A`); extract_ncbi_information / download_patric_tables / extract_patric_meta meta rules not ported |
| patric_genome_download + patric meta rules | not ported | patric | per-sample source=patric; download endpoint ftp.patricbrc.org is dead (PATRIC decommissioned 2023, merged into BV-BRC; verified 550/connection-refused 2026-08) |
| copy_custom_genbank / genbank_to_fna + genbank_to_faa / extract_meta_genbank / genbank_to_gff / copy_converted_gbk / summarize_converted_gbk | `copy_custom_genbank` / `genbank_to_fna` | python | gbk-input path (`input_type = 'gbk'`); genbank_to_fna reads the raw gbk directly (upstream uses input-function branching to avoid the producer overlap); the faa/gff/meta/summary extras not ported |
| report rules (copy_readme, copy_template_notebook, mkdocs_*_report) | not ported | jupyter/mkdocs | separate `bgcflow build report` command, not in the main Snakefile |

Known deviations: the upstream `mlst`, `refseq_masher`, and `diamond` modules
are unreachable in upstream's own default DAG (no pipeline gate or consumer
wires them in) and are therefore not ported; `diamond` survives only inside
the eggnog DB build (`create_dbs.py -m diamond`).

## Links

- Repository: [oxo-flow-bgcflow](https://github.com/oxo-flow-community/oxo-flow-bgcflow)
- Upstream: [NBChub/bgcflow](https://github.com/NBChub/bgcflow) @ `v1.1.2`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
