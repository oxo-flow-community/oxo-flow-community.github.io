# Fetching public sequencing data: FastQ download, metadata and samplesheets

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Fetch metadata and raw FastQ files from public sequence databases (SRA/ENA/DDBJ/GEO). Given a list of database identifiers — run accessions (SRR/ERR/DRR), experiments, studies, biosamples or GEO series — the pipeline retrieves the ENA run metadata, downloads the FastQ files over FTP, validates every download against its ENA md5 sum, and auto-creates a samplesheet plus sample id-mappings and a MultiQC mappings config, ready for downstream nf-core pipelines such as rnaseq, atacseq or taxprofiler.

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 8 |
| **Compute** | up to 2 CPUs / 12 GB per rule (download) |
| **Tools** | python · wget · coreutils |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/fetchngs](https://github.com/nf-core/fetchngs) |
| **Pinned version** | `1.12.0` |

## Run it

```bash
oxo-flow run main.oxoflow
```

Downloads public data by SRA/ENA accessions (network required) — configure your IDs first.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker) — pinned images (quay.io/biocontainers, identical to upstream)

**Requirements.**
- ids file: one SRA/ENA/DDBJ/GEO accession per line (config.input, default test/fixtures/ids.txt), kept in sync with the [[sample_groups]] sample source
- reference data: none — the workflow downloads data from public archives; no genome FASTA, annotation or indices required
- network: outbound access to ENA over FTP (wget -t 5 -c -T 60, 2 retries)
- compute: up to 2 CPUs / 12 GB per rule (FastQ download 2 threads/12G; metadata fetch 1 thread/6G; 4 h time limits on three rules)
- disk: results/fastq/ grows with downloaded FastQ files plus md5/ checksums (depends on input size); metadata/ and samplesheet/ stay small

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-fetchngs
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-fetchngs
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `download_method` | `ftp` | — | `sra_fastq_ftp` |
| `ena_metadata_fields` | `` | Comma-separated ENA metadata fields; empty = upstream default field list. | `sra_ids_to_runinfo` |
| `input` | `test/fixtures/ids.txt` | File containing SRA/ENA/GEO/DDBJ identifiers, one per line (upstream --input). Keep in sync with the [[sample_groups]] list below: check_ids validates this file, the sample source drives the per-id expansion. Add extra ids on the CLI with `oxo-flow run main.oxoflow --sample <ID>`. | `check_ids` |
| `nf_core_pipeline` | `` | nf-core pipeline to tailor the samplesheet for (rnaseq/atacseq/taxprofiler); empty = none. | `sra_to_samplesheet` |
| `nf_core_rnaseq_strandedness` | `auto` | — | `sra_to_samplesheet` |
| `out_dir` | `results` | — | `check_ids`, `combine_mappings`, `combine_samplesheets`, `multiqc_mappings_config`, `sra_fastq_ftp`, `sra_ids_to_runinfo`, `sra_runinfo_to_ftp`, `sra_to_samplesheet` |
| `sample_mapping_fields` | `experiment_accession,run_accession,sample_accession,experiment_alias,run_alias,sample_alias,experiment_title,sample_title,sample_description` | — | `multiqc_mappings_config`, `sra_to_samplesheet` |
| `skip_fastq_download` | `false` | — | `combine_mappings`, `combine_samplesheets`, `sra_fastq_ftp`, `sra_to_samplesheet` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-fetchngs rule-level DAG](/assets/dag/oxo-flow-fetchngs.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- check_ids
- sra_ids_to_runinfo
- sra_runinfo_to_ftp
- sra_fastq_ftp
- sra_to_samplesheet
- combine_samplesheets
- combine_mappings
- multiqc_mappings_config

**Excluded**

- sratools download path (prefetch/fasterq-dump incl. sralite variant) — data-dependent per-run fallback for runs without FTP links, not on the default ftp path
- aspera download path (ASPERA_CLI / fasp links) — download_method=aspera only
- dbGaP (--dbgap_key) — sratools-path only
- softwareVersionsToYAML + versions.yml, PIPELINE_COMPLETION — nf-core boilerplate

## Fidelity

Default-parameters main execution path (`--download_method ftp`,
`--skip_fastq_download false`). Rows cover every upstream process/subworkflow
that the default path touches.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| PIPELINE_INITIALISATION (`isSraId` + id channel) | `check_ids` | python 3.9.5 | Validation regex, mixture/empty errors and deduplication ported 1:1 into `scripts/check_ids.py`; outputs `results/pipeline_info/input_ids.txt`. The ids channel itself is expanded from the workflow sample source (`[[sample_groups]]`, add ids via `--sample`); keep `[config] input` in sync. |
| SRA_IDS_TO_RUNINFO | `sra_ids_to_runinfo` | python 3.9.5 (`quay.io/biocontainers/python:3.9--1`) | Upstream `echo $id > id.txt; sra_ids_to_runinfo.py id.txt <id>.runinfo.tsv` verbatim; `--ena_metadata_fields` flag emitted only when set (same conditional). One instance per input id (upstream: one process per id). The intermediate `.runinfo.tsv` lands in `results/metadata/` (upstream leaves it unpublished in the workdir; oxo-flow requires declared outputs for the DAG contract). |
| SRA_RUNINFO_TO_FTP | `sra_runinfo_to_ftp` | python 3.9.5 | `sra_runinfo_to_ftp.py` verbatim; output `<id>.runinfo_ftp.tsv` → `results/metadata/` (published upstream). |
| SRA_FASTQ_FTP | `sra_fastq_ftp` | wget 1.20.1 (`quay.io/biocontainers/wget:1.20.1`), md5sum (coreutils, in the same image) | wget flags `-t 5 -nv -c -T 60`, `-O <exp>_<run>[_1|_2].fastq.gz` naming and `echo md5 … | md5sum -c` verification byte-identical; fastq → `results/fastq/`, md5 → `results/fastq/md5/` (upstream publishDir patterns). Per-run row parsing replaces the Groovy channel `branch`; **no outputs declared** because the produced file set (single- vs paired-end, per-run names) is data-dependent — md5 verification in the command is the correctness gate (same as upstream). Runs without FTP links are skipped with a warning (upstream routes them to the sra-tools fallback, not ported). |
| SRA_TO_SAMPLESHEET | `sra_to_samplesheet` | python 3.9.5 | Groovy `exec` block ported 1:1 into `scripts/sra_to_samplesheet.py` (removed keys, `sample` = experiment accession, `fastq_1/2` = `<outdir>/fastq/<file>`, ENA columns appended, `--sample_mapping_fields` validation with upstream error text). `localrule`, 100 MB memory, `executor 'local'` mapped to `localrule = true`. Runs only when `skip_fastq_download` is false (upstream: channel empty when skipped). |
| `collectFile('samplesheet.csv')` | `combine_samplesheets` | system (bash + coreutils) | Gather via `expand_inputs` over `config.samples_list`; header kept once, sorted by basename (upstream `keepHeader: true, sort: { it.baseName }`); `results/samplesheet/samplesheet.csv`. |
| `collectFile('id_mappings.csv')` | `combine_mappings` | system (bash + coreutils) | Same gather semantics; `results/samplesheet/id_mappings.csv`. |
| MULTIQC_MAPPINGS_CONFIG | `multiqc_mappings_config` | python 3.9.5 | `multiqc_mappings_config.py` verbatim; output `results/samplesheet/multiqc_config.yml` (upstream publishDir). Gated on `sample_mapping_fields` being set — on by default, same as upstream. |
| softwareVersionsToYAML + `versions.yml` | not ported | — | nf-core boilerplate (software-version collection for the MultiQC report); no engine equivalent, no downstream consumer in the port. |
| PIPELINE_COMPLETION (emails, summary, hooks) | not ported | — | nf-core boilerplate; oxo-flow has no workflow-level hooks. |
| CUSTOM_SRATOOLSNCBISETTINGS, SRATOOLS_PREFETCH, SRATOOLS_FASTERQDUMP (sra-tools 3.0.8 / 2.11.0 + pigz 2.6, incl. the `.sralite` variant) | not ported | — | Data-dependent fallback branch: only runs with **no** FTP links go here, decided per-run from fetched metadata at runtime. oxo-flow cannot branch per-row on data; the default path is FTP. Runs without FTP links are skipped with a warning (see `sra_fastq_ftp`). |
| ASPERA_CLI (Aspera CLI 4.14.0, `fasp` links) | not ported | — | Only with `--download_method aspera`, not the default. |
| dbGaP (`--dbgap_key`) | not ported | — | Only relevant to the sra-tools path (controlled-access data). |
| `params.nf_core_pipeline` (rnaseq/atacseq/taxprofiler columns) | `sra_to_samplesheet` | — | Off by default (empty), same as upstream; the column logic is ported and activates when `nf_core_pipeline` is set. |
| publishDir / `--publish_dir_mode` | n/a | — | oxo-flow has no publishDir; outputs are declared directly at their `results/…` paths. |

Known limitations: the ids used for per-id expansion must be declared in the
sample source (`[[sample_groups]]`, or `--sample` on the CLI) and should match
`[config] input` validated by `check_ids`; sra-tools / Aspera download methods
are not ported (see table).

## Links

- Repository: [oxo-flow-fetchngs](https://github.com/oxo-flow-community/oxo-flow-fetchngs)
- Upstream: [nf-core/fetchngs](https://github.com/nf-core/fetchngs) @ `1.12.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
