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

**Engine.** oxo-flow >= 0.11.0

**Toolchain.** conda envs — pinned (envs/*.yaml, one per tool)

**Requirements.**
- reference_dir with genome.fa, genes.gtf, hg38_ref.txt, CIRIquant.yml
- paired FASTQ per sample in raw/ (<sample>_1.fastq.gz / <sample>_2.fastq.gz)
- compute: up to 8 threads / 32 GB per rule
- conda or mamba to create the pinned per-rule environments on first run

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/download/v0.11.0/oxo-flow-v0.11.0-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/WangLabCSU/oxo-flow-circrna
```

## Links

- Repository: [oxo-flow-circrna](https://github.com/WangLabCSU/oxo-flow-circrna)
