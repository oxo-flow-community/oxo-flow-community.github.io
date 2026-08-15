# RNA-seq: STAR alignment, DESeq2 differential expression and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

End-to-end RNA-seq differential-expression analysis with STAR and DESeq2: Ensembl reference download, fastp trimming, STAR alignment with gene counts, RSeQC QC + MultiQC, count matrix with technical-replicate collapse, Ensembl biomaRt gene-symbol annotation, and DESeq2 (normalized counts, PCA plots, per-contrast results with ashr shrinkage and MA plots). Every tool is pinned to an exact conda version for reproducibility.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | transcriptomics |
| **Rules** | 22 |
| **Tools** | star · fastp · rseqc · gffutils · pandas · multiqc · bioconductor-deseq2 · r-stringr · r-ashr · bioconductor-biomart · r-tidyverse · r-dbplyr · curl |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [snakemake-workflows/rna-seq-star-deseq2](https://github.com/snakemake-workflows/rna-seq-star-deseq2) |
| **Pinned version** | `v3.1.1` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned

**Requirements.**
- paired-end FASTQ reads per config/units.tsv (raw/<unit-key>_R1.fastq.gz / _R2.fastq.gz) and sample conditions in config/samples.tsv
- reference genome + annotation downloaded automatically from Ensembl release 115 (GRCh38) — network access required (also for biomaRt gene-symbol annotation)
- compute: up to 24 CPUs per rule (star_align); 8 (fastp_pe); 4 (star_index); no per-rule memory limits configured in the workflow
- disk: several tens of GB — ~30 GB GRCh38 STAR index, plus BAMs and trimmed reads

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-rnaseq-star-deseq2
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `annotation_url` | `ftp://ftp.ensembl.org/pub/release-115/gtf/homo_sapiens/Homo_sapiens.GRCh38.115.gtf.gz` | — | `get_annotation` |
| `biomart_species` | `hsapiens` | biomaRt species dataset suffix (upstream get_bioc_species_name()). | `gene_2_symbol_counts`, `gene_2_symbol_diffexp`, `gene_2_symbol_normcounts` |
| `contrast_levels` | `treated` | — | `deseq2` |
| `contrast_variables` | `treatment_1` | — | `deseq2` |
| `contrasts` | `treatment_1` | Contrasts (upstream: diffexp.contrasts). One comma-joined entry per contrast: contrast id, its variable_of_interest, its level_of_interest. The base level comes from diffexp_base_levels. | — |
| `diffexp_base_levels` | `untreated,untreated` | — | `deseq2`, `deseq2_init` |
| `diffexp_batch_effects` | `jointly_handled` | — | `deseq2_init` |
| `diffexp_model` | `` | — | `deseq2_init` |
| `diffexp_variables` | `treatment_1,treatment_2` | Differential expression (upstream: diffexp.*). Comma-joined lists mirror the upstream nested tables; positions pair up (treatment_1 -> untreated, treatment_2 -> untreated). | `deseq2`, `deseq2_init` |
| `fastp_adapters` | `--detect_adapter_for_pe` | fastp adapter args and extra args (upstream: per-unit columns fastp_adapters / fastp_extra; the port uses the upstream defaults). | `fastp_pe` |
| `fastp_extra` | `--trim_poly_x --poly_x_min_len 7 --trim_poly_g --poly_g_min_len 7` | — | `fastp_pe` |
| `genome_url` | `https://ftp.ensembl.org/pub/release-115/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz` | — | `get_genome` |
| `genome_url_toplevel` | `https://ftp.ensembl.org/pub/release-115/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.toplevel.fa.gz` | — | `get_genome` |
| `pca_activate` | `true` | PCA (upstream: pca.activate / pca.labels). pca_variables is the derived upstream list (variables_of_interest + batch_effects + labels), kept explicit here — keep it in sync with the diffexp keys below. | `pca` |
| `pca_labels` | `` | — | — |
| `pca_variables` | `treatment_1,treatment_2,jointly_handled` | — | — |
| `raw_dir` | `test/fixtures/raw` | Directory holding <unit-key>_R1.fastq.gz / _R2.fastq.gz per config/units.tsv. The repo default ships the tiny test fixtures; point this at your data (e.g. "raw"). | `fastp_pe` |
| `ref_build` | `GRCh38` | — | — |
| `ref_release` | `115` | — | — |
| `ref_species` | `homo_sapiens` | Reference (upstream: ref.species / ref.release / ref.build). The download URLs below are the Ensembl URLs the wrappers resolve for these values. | — |
| `star_align_extra` | `` | — | `star_align` |
| `star_index_extra` | `` | STAR extra params (upstream: params.star.index / params.star.align). | `star_index` |
| `trimming_activate` | `true` | Trimming (upstream: trimming.activate). The fastp rule runs only when activated; deactivating breaks star_align in this port (upstream rewires star_align to the raw reads — not ported). | `fastp_pe` |
| `units_file` | `config/units.tsv` | — | `count_matrix` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-rnaseq-star-deseq2 rule-level DAG](/assets/dag/oxo-flow-rnaseq-star-deseq2.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- get_genome
- get_annotation
- star_index
- fastp_pe
- star_align
- rseqc_gtf2bed
- rseqc_junction_annotation
- rseqc_junction_saturation
- rseqc_stat
- rseqc_infer
- rseqc_innerdis
- rseqc_readdis
- rseqc_readdup
- rseqc_readgc
- multiqc
- count_matrix
- gene_2_symbol
- deseq2_init
- pca
- deseq2

**Excluded**

- get_sra — SRA-accession branch (fasterq-dump), not in the default path
- fastp_se — single-end branch, not in the default path
- bwa_index — no consumer in the upstream default path
- genome_faidx — no consumer in the upstream default path
- edger — not present in upstream v3.1.1
- kallisto — not present in upstream v3.1.1
- trimgalore — not present in upstream v3.1.1 (fastp is the trimmer)
- trimming.activate=false rewiring (star_align from raw reads) — default path only
- complex string-form DESeq2 contrasts — list-form (default) only
- Snakemake report artifacts (report/*.rst) — no oxo-flow equivalent
- per-unit fastp_adapters/fastp_extra lookup — pipeline-level config instead

## Fidelity

Scope: the **default-parameters main execution path** (upstream `rule all`).
Rows cover every upstream rule; "not ported" rows carry a reason. Upstream
rules use snakemake wrappers v7.2.0 (`bio/fastp`, `bio/star/*`,
`bio/multiqc`, `bio/reference/ensembl-*`, `bio/samtools/faidx`,
`bio/bwa/index`) whose conda pins were carried over verbatim.

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| get_genome | `get_genome` | curl (system) + Ensembl FTP/HTTPS | ensembl-sequence wrapper: primary_assembly URL with toplevel fallback; probe/fallback restructured into shell, HTTPS branch only (upstream also probes FTP) |
| get_annotation | `get_annotation` | curl (system) + Ensembl FTP/HTTPS | ensembl-annotation wrapper, identical URL + `gzip -d` logic |
| star_index | `star_index` | STAR 2.7.11b | star/index wrapper verbatim; tmpdir moved to `.oxo-flow/tmp/star_index` |
| fastp_pe | `fastp_pe` | fastp 1.0.1 | fastp wrapper verbatim (extra + adapters + reads + trimmed + json + html ordering); upstream per-unit `fastp_adapters`/`fastp_extra` columns → global `[config] fastp_adapters`/`fastp_extra` (defaults equal upstream defaults) |
| star_align | `star_align` | STAR 2.7.11b | star/align wrapper verbatim: `--outSAMtype BAM SortedByCoordinate --quantMode GeneCounts --sjdbGTFfile "<gtf>"` in the upstream extra-string order, `--readFilesCommand gunzip -c`, `--outStd BAM_SortedByCoordinate` to the BAM, `cat` of ReadsPerGene/SJ/Logs out of the tmp prefix |
| get_sra | not ported | sra-tools | SRA-accession branch (fasterq-dump); not in the default path |
| fastp_se | not ported | fastp | single-end branch; not in the default path (paired-end fixtures) |
| rseqc_gtf2bed | `rseqc_gtf2bed` | gffutils 0.13 | gtf2bed.py ported to CLI args; `annotation.db` is `temp_output` (= upstream `temp()`) |
| rseqc_junction_annotation | `rseqc_junction_annotation` | RSeQC 5.0.4 | `junction_annotation.py -q 255 -i <bam> -r <bed> -o <prefix>` verbatim |
| rseqc_junction_saturation | `rseqc_junction_saturation` | RSeQC 5.0.4 | `junction_saturation.py -q 255 ...` verbatim |
| rseqc_stat | `rseqc_stat` | RSeQC 5.0.4 | `bam_stat.py -i <bam> > <out> 2> <log>` verbatim |
| rseqc_infer | `rseqc_infer` | RSeQC 5.0.4 | `infer_experiment.py -r <bed> -i <bam> > <out> 2> <log>` verbatim |
| rseqc_innerdis | `rseqc_innerdis` | RSeQC 5.0.4 | `inner_distance.py -r <bed> -i <bam> -o <prefix>` verbatim |
| rseqc_readdis | `rseqc_readdis` | RSeQC 5.0.4 | `read_distribution.py -r <bed> -i <bam>` verbatim |
| rseqc_readdup | `rseqc_readdup` | RSeQC 5.0.4 | `read_duplication.py -i <bam> -o <prefix>` verbatim |
| rseqc_readgc | `rseqc_readgc` | RSeQC 5.0.4 | `read_GC.py -i <bam> -o <prefix>` verbatim |
| multiqc | `multiqc` | MultiQC 1.29 | multiqc wrapper verbatim: parent dirs of all inputs (incl. the junction-annotation log dir), `--no-data-dir --outdir results/qc --filename multiqc_report`. (In upstream's `rule all` — ported, not excluded.) |
| count_matrix | `count_matrix` | pandas 2.3.2 | count-matrix.py logic identical (strandedness column pick 1/2/3, sample naming, `groupby(...).sum()` collapse of technical replicates); unit→(sample, strandedness) mapping read from `config/units.tsv` instead of snakemake params |
| gene_2_symbol | `gene_2_symbol_counts` / `gene_2_symbol_normcounts` / `gene_2_symbol_diffexp` | biomaRt 2.62.0, r-tidyverse 2.0.0 | upstream is one wildcard-generic rule over `{prefix}`; the port makes the three call sites explicit (oxo-flow has no arbitrary `{prefix}` wildcard). `{contrast}` variant scatters per contrast |
| deseq2_init | `deseq2_init` | DESeq2 1.46.0 | deseq2-init.R logic identical (relevel base levels, batch-effect factors, default interaction model, `rowSums>1` filter, normalized counts); config values passed as CLI args |
| pca | `pca` | DESeq2 1.46.0 | plot-pca.R verbatim (`rlog(blind=FALSE)`, `plotPCA(intgroup=variable)`); one instance per `pca_variables` entry; gated by `pca_activate` |
| deseq2 | `deseq2` | DESeq2 1.46.0, r-ashr 2.2_63 | deseq2.R logic identical (list-form contrast = vof + level + base_level, ashr `lfcShrink`, `order(padj)`, MA plot); complex string-form contrasts not ported (not in default config); one instance per `contrasts` entry |
| bwa_index | not ported | bwa | no consumer in the default path (upstream `rule all` never requests it) |
| genome_faidx | not ported | samtools | no consumer in the default path |
| report/ (`report/*.rst`) | not ported | — | Snakemake report artifacts; no oxo-flow equivalent |
| trimming.activate = False rewiring | not ported | — | upstream then feeds raw reads to star_align; the port keeps the default trimmed-read chain |

**Port-level conventions** (config-shape deviations, commands unchanged):
upstream wildcards are `(sample, unit)`; the port fans out over one composite
`{sample}` = `<sample>-<unit>` (e.g. `A-lane1`), so output paths are
byte-identical to upstream (`results/trimmed/A-lane1/A-lane1_R1.fastq.gz`,
`results/star/A-lane1/...`). Nested upstream config (`diffexp.*`, `ref.*`,
`trimming.activate`, `pca.*`) is flattened into flat `[config]` keys with the
same defaults (see `main.oxoflow` header). The upstream `config/samples.tsv`
demo sheet (samples A–E) and `config/units.tsv` (6 units) ship with the port;
raw reads live at `<raw_dir>/<unit-key>_R1.fastq.gz` / `_R2.fastq.gz`
(`[config] raw_dir` defaults to `test/fixtures/raw/`, which contains tiny real
reads so the dry-run resolves every input; point it at your data, e.g.
`raw_dir = "raw"`). Upstream demo-data FASTQ paths (`A.1.fq.gz` etc.) were
renamed to this convention — data-path substitution only.

## Links

- Repository: [oxo-flow-rnaseq-star-deseq2](https://github.com/oxo-flow-community/oxo-flow-rnaseq-star-deseq2)
- Upstream: [snakemake-workflows/rna-seq-star-deseq2](https://github.com/snakemake-workflows/rna-seq-star-deseq2) @ `v3.1.1`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
