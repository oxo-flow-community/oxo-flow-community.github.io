# Single-cell RNA-seq: alignment, quantification and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Single-cell RNA-seq analysis from raw 10x Genomics FASTQ reads to a final MultiQC report: FastQC read QC, Cell Ranger reference preparation and per-sample cellranger count (alignment and quantification, optional BAM output), conversion of raw and filtered 10x matrices to h5ad, CellBender ambient-RNA background removal, sample-wise h5ad concatenation, and optional export to Seurat and SingleCellExperiment objects. Covers the Cell Ranger execution path of nf-core/scrnaseq; other aligners and assays (ATAC, multiome) are not included.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | single-cell |
| **Rules** | 23 |
| **Tools** | cellranger · fastqc · multiqc · scanpy · anndata · cellbender · anndataR · SeuratObject · SingleCellExperiment · rhdf5 · gzip · gawk · python |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/scrnaseq](https://github.com/nf-core/scrnaseq) |
| **Pinned version** | `4.2.0` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker/Singularity) — pinned images; conda alternatives in envs/ for non-Cell-Ranger rules (Cell Ranger rules are docker-only)

**Requirements.**
- reference genome FASTA, optionally gzipped (config.fasta, default refs/refdata.fa.gz)
- gene-annotation GTF, optionally gzipped (config.gtf, default refs/refdata.gtf.gz)
- raw 10x FASTQ pair per sample: raw/<sample>_R1.fastq.gz and raw/<sample>_R2.fastq.gz (one pair per sample)
- samplesheet.csv with columns sample,fastq_1,fastq_2,protocol,expected_cells (used by the combined-h5ad step)
- compute: up to 12 CPUs / 72 GB per rule (Cell Ranger mkref/count); 6 CPUs / 36 GB for h5ad conversion, CellBender and concat rules; concurrent per-sample rules scale with -j
- optional: pre-built Cell Ranger index (set build_cellranger_index=false and point transcriptome at it) to skip index building

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-scrnaseq
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `aligner` | `cellranger` | --aligner / --protocol (port implements the cellranger branch; see README fidelity table) | — |
| `build_cellranger_index` | `true` | cellranger reference: build from fasta/gtf, or point transcriptome at an existing index | `cellranger_mkgtf`, `cellranger_mkref` |
| `expected_cells` | `` | samplesheet `expected_cells` column -> `--expect-cells` when set | `cellranger_count` |
| `fasta` | `refs/refdata.fa.gz` | reference genome (upstream --fasta / --gtf; may be .gz) | `gunzip_fasta` |
| `fasta_gz` | `true` | — | `gunzip_fasta` |
| `fasta_prepared` | `refs/refdata.fa` | derived reference files (README "Reference genome" explains the chain) | `cellranger_mkref`, `gtf_gene_filter`, `gunzip_fasta` |
| `gtf` | `refs/refdata.gtf.gz` | — | `gunzip_gtf` |
| `gtf_filtered` | `refs/refdata_genes.gtf` | — | `gtf_gene_filter`, `gtf_source_fix` |
| `gtf_gz` | `true` | — | `gunzip_gtf` |
| `gtf_mkgtf` | `refs/refdata_genes.filtered.gtf` | — | `cellranger_mkgtf`, `cellranger_mkref` |
| `gtf_mkgtf_input` | `refs/refdata_genes.gtf` | set to the source-fixed file when gtf_source_fix=true | `cellranger_mkgtf` |
| `gtf_prepared` | `refs/refdata.gtf` | — | `gtf_gene_filter`, `gunzip_gtf` |
| `gtf_source_fix` | `false` | iGenomes GTF source-field rewrite (opt-in, upstream gtf_source_has_spaces) | `gtf_source_fix` |
| `gtf_source_fixed` | `refs/refdata_genes.source_fixed.gtf` | — | `gtf_source_fix` |
| `multiqc_config` | `assets/multiqc_config.yml` | — | `multiqc` |
| `multiqc_title` | `` | -> `--title` when set | `multiqc` |
| `out_dir` | `results` | — | — |
| `protocol` | `auto` | passed verbatim as `--chemistry` (10x auto-detection) | `cellranger_count` |
| `samplesheet` | `samplesheet.csv` | user samplesheet consumed by CONCAT_H5AD (same columns as upstream) | `concat_h5ad_cellbender_filter`, `concat_h5ad_filtered`, `concat_h5ad_raw` |
| `save_align_intermeds` | `true` | -> `--create-bam true` | `cellranger_count` |
| `skip_cellbender` | `false` | — | `anndata_barcodes`, `anndatar_convert_cellbender_filter`, `anndatar_convert_combined_cellbender_filter`, `anndatar_convert_combined_raw`, `anndatar_convert_raw`, `cellbender_removebackground`, `concat_h5ad_cellbender_filter`, `concat_h5ad_raw` |
| `skip_fastqc` | `false` | QC / reporting knobs | `fastqc` |
| `skip_multiqc` | `false` | — | `multiqc` |
| `transcriptome` | `refs/cellranger_reference` | — | `cellranger_count`, `cellranger_mkref` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-scrnaseq rule-level DAG](/assets/dag/oxo-flow-scrnaseq.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- PIPELINE_INITIALISATION (samplesheet input check)
- FASTQC
- GUNZIP_FASTA
- GUNZIP_GTF
- GTF_GENE_FILTER
- GTF_SOURCE_FIX (opt-in, off by default)
- CELLRANGER_MKGTF
- CELLRANGER_MKREF
- CELLRANGER_COUNT
- MTX_TO_H5AD
- CELLBENDER_REMOVEBACKGROUND
- ANNDATA_BARCODES
- CONCAT_H5AD
- ANNDATAR_CONVERT
- softwareVersionsToYAML + collectFile (collated versions)
- MULTIQC

**Excluded**

- simpleaf: aligner=simpleaf branch (upstream default aligner) — not on the ported cellranger path
- kallisto: aligner=kallisto branch (kallisto/bustools)
- star: aligner=star branch (STARsolo, incl. smartseq/dropseq protocols)
- smartseq: STARsolo/kallisto smartseq protocol — off the ported cellranger path
- dropseq: STARsolo/kallisto/simpleaf dropseq protocol — off the ported cellranger path
- scdna: not a scrnaseq 4.2.0 feature; excluded upstream feature list
- cellranger_atac: aligner=cellrangerarc branch (ATAC + barcode fastqs)
- cellrangermulti: aligner=cellrangermulti branch (multiome VDJ/Ab-seq, barcodes samplesheet)
- PIPELINE_COMPLETION: email/notification completion subworkflow (nf-core boilerplate)
- paramsSummaryMultiqc + methods_description_template.yml: workflow summary/methods MultiQC inputs (nf-core reporting boilerplate)

## Fidelity

Rows cover every upstream process/subworkflow involved in the default path; the
`aligner` branches not ported are listed at the bottom with reasons. Container image
strings and conda pins are copied verbatim from the upstream modules (all pinned, no
`latest`).

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `PIPELINE_INITIALISATION` (samplesheet check) | sample source + `config.samplesheet` | — | Samplesheet (`sample, fastq_1, fastq_2, protocol, expected_cells`) maps to `[[sample_groups]]`; `expected_cells` column → `config.expected_cells`; per-sample `protocol` column is informational (chemistry comes from `--protocol`). Schema checks are enforced by the port's fixtures + README contract. |
| `FASTQC` | `fastqc` | fastqc 0.12.1 | Identical command: `printf … \| while read; ln -s` staging loop, `fastqc --quiet --threads N --memory <12G/N clamped 100-10000>`. Published under `results/fastqc/` (upstream default publishDir). `--memory` computed in-shell from the process_low 12G/2 cpus. |
| `GUNZIP` (as `GUNZIP_FASTA`) | `gunzip_fasta` | gzip 1.13 | Identical command (`gzip -cd <fasta> > <out>`). Runs only when `config.fasta_gz` (upstream decides by `.endsWith('.gz')` at runtime — port uses an explicit flag, see Gotchas). |
| `GUNZIP` (as `GUNZIP_GTF`) | `gunzip_gtf` | gzip 1.13 | Same as above for the GTF. |
| `GTF_GENE_FILTER` | `gtf_gene_filter` | python 3.9 | Same bundled script `filter_gtf_for_genes_in_genome.py`, same flags (`--gtf --fasta -o`); output name `<fasta_stem>_genes.gtf` is `config.gtf_filtered`. |
| `GAWK` (as `GTF_SOURCE_FIX`) | `gtf_source_fix` | gawk 5.3.1 | Same awk program (`FS=OFS="\t"`, source-field spaces→underscores, output suffix `gtf`). Off by default, exactly like upstream (only fires for iGenomes entries flagged `gtf_source_has_spaces`). |
| `CELLRANGER_MKGTF` | `cellranger_mkgtf` | cellranger 10.0.0 | Same command incl. the three `--attribute=gene_biotype:` filters. Runs only when `build_cellranger_index=true` (mirrors upstream `if (!cellranger_index)`). |
| `CELLRANGER_MKREF` | `cellranger_mkref` | cellranger 10.0.0 | Same command (`--genome=… --fasta=… --genes=… --localcores --localmem --nthreads`). `--genome` is `config.transcriptome` (default `refs/cellranger_reference`) instead of a bare workdir name — same reference name, path relocated to the workflow tree. |
| `CELLRANGER_COUNT` | `cellranger_count` | cellranger 10.0.0 | Same command: reads staged under Cell Ranger naming (`<sample>_S1_L001_R1/R2_001.fastq.gz`), `cellranger count --id <sample> --fastqs fastq_all --transcriptome … --localcores … --localmem … --chemistry <protocol> --create-bam <bool>` + `--expect-cells` when set. The outs tree is then relocated to `results/cellranger/count/<sample>/outs/` (upstream publishDir `outdir/cellranger/count`). Multi-lane samples (several fastq pairs per sample) are not represented — one pair per sample. |
| `MTX_TO_H5AD` | `mtx_to_h5ad_raw`, `mtx_to_h5ad_filtered` | scanpy 1.10.2 / pandas / anndata | Same template script `mtx_to_h5ad_cellranger.py` (read_10x_h5, gene_symbols, gene_ids index, version-stripped gene ids, `var_names_make_unique`), one rule per input_type (upstream runs the process once per raw/filtered channel). Outputs `<sample>_{raw,filtered}_matrix.h5ad`. |
| `CELLBENDER_REMOVEBACKGROUND` | `cellbender_removebackground` | cellbender 0.3.2 | Same command `TMPDIR=. cellbender remove-background --cpu-threads … --estimator-multiple-cpu --input … --output <sample>.h5` (no `--cuda`: GPU profile is out of scope). Full output file set moved to `results/cellranger/<sample>/cellbender_removebackground/`. |
| `ANNDATA_BARCODES` | `anndata_barcodes` | anndata 0.11.4 / pandas | Same template script (barcode CSV → subset → write), same output name `<sample>_cellbender_filter_matrix.h5ad`. |
| `CONCAT_H5AD` | `concat_h5ad_filtered`, `concat_h5ad_cellbender_filter`, `concat_h5ad_raw` | scanpy 1.10.2 | Same template script (`ad.concat(label="sample", merge="unique", index_unique="_")` + samplesheet join on `sample`). Upstream runs one process per input_type; the port has one rule per input_type. `concat_h5ad_raw` only runs when `skip_cellbender=true`, mirroring upstream's channel replacement (raw is superseded by the CellBender-filtered h5ad). |
| `ANNDATAR_CONVERT` | `anndatar_convert_{filtered,cellbender_filter,raw}` + `anndatar_convert_combined_{…}` | anndataR 1.0.2, SeuratObject 5.5.0, SingleCellExperiment 1.32.0 | Same R template (read_h5ad → `as_Seurat()`/`as_SingleCellExperiment()` → saveRDS). Six rules: per sample and per combined h5ad, per input_type; type gating mirrors the concat rules. Upstream `dir.create(<sample>)` calls and versions.yml writing dropped (output dirs are pre-created by the engine; versions are recorded in `collect_versions`). |
| `softwareVersionsToYAML` + `collectFile` | `collect_versions` | — | Writes the same file `results/pipeline_info/nf_core_scrnaseq_software_mqc_versions.yml` consumed by MultiQC. Content is the port's pinned versions (upstream collates live tool versions from a channel topic, which has no oxo-flow equivalent); since containers are pinned, the recorded versions equal the executed ones. |
| `MULTIQC` | `multiqc` | multiqc 1.34 | Same command (`multiqc --force [--title] --config <assets/multiqc_config.yml> .`) with inputs staged flat like the module's `stageAs '?/*'`. Default `assets/multiqc_config.yml` copied verbatim from upstream. |

**Not ported (with reasons):**

| Upstream branch | Reason |
|---|---|
| `aligner = simpleaf` (upstream default aligner; alevin-fry) | Not on the ported cellranger default path; requires qcatch protocol handling and a simpleaf index/whitelist matrix. |
| `aligner = kallisto` (kallisto/bustools, incl. `smartseq`/`dropseq` protocols) | Not on the ported cellranger path. |
| `aligner = star` (STARsolo, incl. `smartseq`/`dropseq` protocols) | Not on the ported cellranger path. |
| `aligner = cellrangerarc` (ATAC, `fastq_barcode` samplesheet column) | Not on the ported cellranger path. |
| `aligner = cellrangermulti` (multiome: VDJ/Ab-seq/CRO, `cellranger_multi_barcodes`) | Not on the ported cellranger path. |
| `PIPELINE_COMPLETION` (email/notification) | nf-core boilerplate, out of scope. |
| `paramsSummaryMultiqc` / methods-description MultiQC inputs | nf-core reporting boilerplate; MultiQC still aggregates FastQC + Cell Ranger + versions. |
| `skip_cellranger_renaming` (multi-lane samples) | One fastq pair per sample is supported; the staging rename hard-codes lane `L001`. |

## Links

- Repository: [oxo-flow-scrnaseq](https://github.com/oxo-flow-community/oxo-flow-scrnaseq)
- Upstream: [nf-core/scrnaseq](https://github.com/nf-core/scrnaseq) @ `4.2.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
