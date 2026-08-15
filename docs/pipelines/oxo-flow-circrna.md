# circRNA detection: four callers with ensemble aggregation

<div class="ox-page-badges"><span class="ox-badge">☆ Community</span> <span class="ox-badge ox-badge--origin">✦ Original</span> </div>

Circular RNA detection with four independent callers (CIRIquant, CIRCexplorer2, find_circ, circRNA_finder) and ensemble aggregation of calls supported by at least two methods. Indexes and conda environments are built automatically on first run from a single reference_dir; samples are auto-discovered from raw/ with no CSV.

| | |
|---:|---|
| **Rating** | ☆ Community |
| **Origin** | original |
| **Domain** | transcriptomics (circRNA) |
| **Rules** | 9 |
| **Tools** | fastp · ciriquant · circexplorer2 · find_circ · circrna_finder · r-base · multiqc |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |

## Run it

```bash
oxo-flow run circrna.oxoflow -j 16
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned (envs/*.yaml, one per tool)

**Requirements.**
- reference_dir with genome.fa, genes.gtf, hg38_ref.txt, CIRIquant.yml
- paired FASTQ per sample in raw/ (<sample>_1.fastq.gz / <sample>_2.fastq.gz)
- compute: up to 8 threads / 32 GB per rule
- conda or mamba to create the pinned per-rule environments on first run

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/WangLabCSU/oxo-flow-circrna
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `bowtie2_index` | `/data/references/GRCh38/bowtie2/genome.fa` | — | `find_circ` |
| `bwa_index` | `/data/references/GRCh38/bwa/genome.fa` | — | — |
| `bwamem2_index` | `/data/references/GRCh38/bwamem2/genome.fa` | — | — |
| `circexplorer2_ref` | `{config.reference_dir}/hg38_ref.txt` | — | `circexplorer2` |
| `ciriquant_config` | `{config.reference_dir}/CIRIquant.yml` | — | `ciriquant` |
| `gatk_dict` | `/data/references/GRCh38/genome.dict` | — | — |
| `gene_annotation` | `{config.reference_dir}/genes.gtf` | — | `aggregate` |
| `hisat2_index` | `/data/references/GRCh38/hisat2/genome.fa` | — | — |
| `minimap2_index` | `/data/references/GRCh38/genome.fa.mmi` | — | — |
| `reference_dir` | `/data/references/GRCh38` | === The only path you need to set === All indexes and reference paths are auto-derived from this directory. Expected layout: {reference_dir}/genome.fa {reference_dir}/genes.gtf | — |
| `reference_fasta` | `{config.reference_dir}/genome.fa` | === Auto-derived from reference_dir — override any of these if your layout differs === | `circexplorer2`, `find_circ` |
| `samtools_faidx` | `/data/references/GRCh38/genome.fa.fai` | — | — |
| `star_index` | `/data/references/GRCh38/star` | — | `circrna_finder` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-circrna rule-level DAG](/assets/dag/oxo-flow-circrna.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Links

- Repository: [oxo-flow-circrna](https://github.com/WangLabCSU/oxo-flow-circrna)
