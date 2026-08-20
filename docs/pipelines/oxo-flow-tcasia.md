# Paired-end RNA-seq alignment and four-caller alternative-splicing analysis

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

Paired-end RNA-seq from FASTQ to per-sample alternative-splicing calls: reads are trimmed with fastp, aligned with two-pass STAR and counted per gene with featureCounts; each sample's splicing is then quantified independently with four callers — rMATS, MAJIQ (with Voila export), SUPPA2 (via Salmon transcript quantification) and SplAdder. The alignment and AS-calling stages are one chained DAG (run one stage with -t alignment / -t as_calling).

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | transcriptomics |
| **Rules** | 17 |
| **Compute** | up to 10 threads per rule (STAR / rMATS) |
| **Tools** | fastp · star · samtools · subread · salmon · suppa · rmats · majiq · voila · spladder · perl |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [OncoHarmony-Network/TCASIA_pipeline](https://github.com/OncoHarmony-Network/TCASIA_pipeline) |
| **Pinned version** | `main@06564ff1` |

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs raw FASTQs and reference data — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned versions (fastp 0.23.4, STAR 2.7.7a, samtools 1.13/1.15, subread 2.0.1, salmon 1.10.3, suppa 2.3, rMATS 4.3.0, MAJIQ 2.5, SplAdder 3.1.1; conda-forge + bioconda)

**Requirements.**
- reference data (GRCh38 + GENCODE v34): STAR index (STAR 2.7.7a), annotation GTF + GFF3, Salmon transcript index, SUPPA2 events file, MAJIQ academic license
- paired-end reads at reads_dir/<sample>_1.fastq.gz / <sample>_2.fastq.gz for each sample in the [[sample_groups]] list
- compute: up to 10 threads per rule (STAR/rMATS), no memory limits set
- conda or mamba at runtime to create the pinned envs/*.yaml environments

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-tcasia
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-tcasia
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `align_out_dir` | `/path/to/output/alignment` | 01_alignment (upstream config.yml) | `alignment::fastp_qc`, `alignment::featurecounts`, `alignment::index_bam`, `alignment::sort_bam`, `alignment::star_align` |
| `aligned_dir` | `/path/to/output/alignment/aligned` | upstream: 01 output_dir/aligned == 02 bam_dir | `alignment::featurecounts`, `alignment::index_bam`, `alignment::sort_bam`, `alignment::star_align`, `as_calling::majiq_create_ini`, `as_calling::rmats_create_input`, `as_calling::spladder_run` |
| `as_out_dir` | `/path/to/output/as_calling` | 02_as_calling (upstream config.yml) | `as_calling::format_suppa_fields`, `as_calling::majiq_build`, `as_calling::majiq_create_ini`, `as_calling::majiq_psi`, `as_calling::rmats_create_input`, `as_calling::rmats_run`, `as_calling::salmon_quant`, `as_calling::select_suppa_fields`, `as_calling::spladder_run`, `as_calling::suppa_run`, `as_calling::voila_modulize`, `as_calling::voila_tsv` |
| `fastp_min_length` | `36` | fastp (upstream fastp.*) | `alignment::fastp_qc` |
| `fastp_n_base_limit` | `5` | — | `alignment::fastp_qc` |
| `fastp_qualified_quality_phred` | `20` | — | `alignment::fastp_qc` |
| `fastp_unqualified_percent_limit` | `40` | — | `alignment::fastp_qc` |
| `gff` | `/path/to/references/gencode.v34.annotation.gff3` | upstream: GFF | `as_calling::majiq_build` |
| `majiq_genome` | `hg38` | — | `as_calling::majiq_create_ini` |
| `majiq_license` | `/path/to/majiq_license_academic_official.lic` | — | `as_calling::majiq_build`, `as_calling::majiq_psi`, `as_calling::voila_modulize`, `as_calling::voila_tsv` |
| `majiq_minreads` | `10` | — | `as_calling::majiq_build` |
| `majiq_strandness` | `reverse` | fr-firststrand -> reverse \| fr-secondstrand -> forward \| fr-unstranded -> none | `as_calling::majiq_create_ini` |
| `read_len` | `150` | — | `as_calling::majiq_create_ini`, `as_calling::rmats_run` |
| `reads_dir` | `test/fixtures/raw` | point at your own fastq directory for real runs | `alignment::fastp_qc`, `as_calling::salmon_quant` |
| `ref` | `/path/to/references/gencode.v34.annotation.gtf` | featureCounts / rMATS / SplAdder annotation | `alignment::featurecounts`, `as_calling::rmats_run`, `as_calling::spladder_run` |
| `rmats_cstat` | `0.0001` | — | `as_calling::rmats_run` |
| `rmats_extra` | `` | — | `as_calling::rmats_run` |
| `salmon_index` | `/path/to/references/gencode.v34.transcripts.salmon.index` | — | `as_calling::salmon_quant` |
| `salmon_library_type` | `ISR` | Derived from `strandness` by upstream tcasia_config.py; kept explicit here: | `as_calling::salmon_quant` |
| `spladder_confidence` | `3` | — | `as_calling::spladder_run` |
| `spladder_event_types` | `exon_skip,intron_retention,alt_3prime,alt_5prime,mutex_exons` | — | `as_calling::spladder_run` |
| `spladder_merge_strategy` | `single` | — | `as_calling::spladder_run` |
| `star_index_dir` | `/path/to/references/STAR_index` | GRCh38 STAR index built with STAR 2.7.7a + GENCODE v34 | `alignment::star_align` |
| `star_limit_bam_sort_ram` | `39050942993` | — | `alignment::star_align` |
| `star_out_filter_mismatch_nmax` | `15` | STAR (upstream star.*) | `alignment::star_align` |
| `strandness` | `fr-firststrand` | shared | `as_calling::rmats_run` |
| `suppa2_events` | `/path/to/references/gencode.v34.events.ioe` | — | `as_calling::suppa_run` |
| `suppa2_min_tpm` | `1` | — | `as_calling::suppa_run` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-tcasia rule-level DAG](/assets/dag/oxo-flow-tcasia.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastp_qc
- star_align
- sort_bam
- index_bam
- featurecounts
- salmon_quant
- select_suppa_fields
- format_suppa_fields
- suppa_run
- rmats_create_input
- rmats_run
- majiq_create_ini
- majiq_build
- majiq_psi
- voila_modulize
- voila_tsv
- spladder_run

**Excluded**

- none

## Fidelity

Scope: the **default-parameters main execution path** (upstream `rule all` of both Snakefiles). Rows cover every upstream rule; no "not ported" rows — the full default path is ported.

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| fastp_qc | `alignment::fastp_qc` | fastp 0.23.4 | identical command; input layout from `[[sample_groups]]` + `reads_dir` instead of samples.tsv |
| star_align | `alignment::star_align` | STAR 2.7.7a | identical command; `params.prefix` inlined |
| sort_bam | `alignment::sort_bam` | samtools 1.15 | identical command |
| index_bam | `alignment::index_bam` | samtools 1.15 | identical command |
| featurecounts | `alignment::featurecounts` | subread 2.0.1 | identical command; upstream runs without a strandness flag (oxo-flow preflight warns — upstream behavior kept) |
| salmon_quant | `as_calling::salmon_quant` | salmon 1.10.3 | identical command; `-l` from explicit `salmon_library_type` (upstream derives it from `strandness` in tcasia_config.py) |
| select_suppa_fields | `as_calling::select_suppa_fields` | suppa 2.3 | identical command |
| format_suppa_fields | `as_calling::format_suppa_fields` | suppa 2.3 | identical perl one-liner |
| suppa_run | `as_calling::suppa_run` | suppa 2.3 | identical command; output prefix inlined |
| rmats_create_input | `as_calling::rmats_create_input` | rMATS 4.3.0 | identical command |
| rmats_run | `as_calling::rmats_run` | rMATS 4.3.0 | identical command; `--od` directory declared as the rule output |
| majiq_create_ini | `as_calling::majiq_create_ini` | MAJIQ 2.5 | identical printf; `bam_dir`/`bam_stem` params inlined |
| majiq_build | `as_calling::majiq_build` | MAJIQ 2.5 | identical command |
| majiq_psi | `as_calling::majiq_psi` | MAJIQ 2.5 | identical command |
| voila_modulize | `as_calling::voila_modulize` | MAJIQ 2.5 (Voila) | identical command; `modulized/` directory declared as the rule output |
| voila_tsv | `as_calling::voila_tsv` | MAJIQ 2.5 (Voila) | identical command |
| spladder_run | `as_calling::spladder_run` | SplAdder 3.1.1 | identical command; output directory declared as the rule output |
| rule all | — (DAG targets) | — | every output above is a default target of the single chained DAG |

**Port-level conventions** (config-shape deviations, commands unchanged):
- **Sample sheet**: upstream reads per-sample fastq paths from a TSV (`sample_id/fastq_1/fastq_2`); the port uses `[[sample_groups]]` plus the `reads_dir/{sample}_1.fastq.gz` / `{sample}_2.fastq.gz` layout.
- **One workflow file, one DAG**: the two upstream Snakefiles (+ the four `rules/snakefile_*` fragments) are `modules/alignment.oxoflow` + `modules/as_calling.oxoflow`, included from `main.oxoflow`; the two `config.yml` files merge into one `[config]`. Upstream `01 output_dir/aligned` and `02 bam_dir` are the single key `aligned_dir`, making the alignment → AS-calling chain structural. Run one stage only with `-t alignment` / `-t as_calling`.
- **Strandness-derived values are explicit config keys**: upstream computes `salmon_library_type` (`fr-firststrand→ISR`, `fr-secondstrand→ISF`, `fr-unstranded→IU`) and `majiq_strandness` (`fr-firststrand→reverse`, `fr-secondstrand→forward`, `fr-unstranded→none`) in `tcasia_config.py`; rMATS uses the `strandness` value directly (as upstream). Change `strandness` **and** the two derived keys together.
- **Helper scripts not ported**: `scripts/validate_config.py` and `scripts/read_length.sh` are user-facing helpers; oxo-flow validates config/inputs natively.
- **Threads only, no memory**: upstream declares threads per tool and no memory; the port mirrors that exactly.
- **MAJIQ is license-gated**: upstream runs the 5-rule MAJIQ chain unconditionally and fails hard without the academic license file. The port gates the chain on `run_majiq` (default `false`): a fresh clone completes with rMATS + SUPPA2 + SplAdder; set `run_majiq = true` after placing the license at `majiq_license` (commands unchanged when enabled).
- **MAJIQ env fixes**: upstream's own `pip majiq==2.5` installs from no index (PyPI/bioconda both lack majiq) — the port installs OncoHarmony-Network/majiq_academic@v2.5 (the TCASIA org's fork), with numpy=1.26 (the fork's Cython extensions break on numpy 2.x ABI) and setuptools=75.8.2 (voila's gunicorn imports pkg_resources, removed in setuptools 81+).

## Links

- Repository: [oxo-flow-tcasia](https://github.com/oxo-flow-community/oxo-flow-tcasia)
- Upstream: [OncoHarmony-Network/TCASIA_pipeline](https://github.com/OncoHarmony-Network/TCASIA_pipeline) @ `main@06564ff1`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
