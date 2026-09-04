---
title: "RNA-seq: STAR alignment, DESeq2 differential expression and QC"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-rnaseq-star-deseq2</span></div>
<div class="ox-detail-cols">
<div>
<h1>RNA-seq: STAR alignment, DESeq2 differential expression and QC</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>
<p>End-to-end RNA-seq differential-expression analysis with STAR and DESeq2: Ensembl reference download, fastp trimming, STAR alignment with gene counts, RSeQC QC + MultiQC, count matrix with technical-replicate collapse, Ensembl biomaRt gene-symbol annotation, and DESeq2 (normalized counts, PCA plots, per-contrast results with ashr shrinkage and MA plots). Every tool is pinned to an exact conda version for reproducibility. Per-unit upstream semantics are ported via the engine metadata binding: the units sheet doubles as the metadata table, so per-unit fastp_adapters/fastp_extra overrides and per-unit SRA accessions (the get_sra auto-feed) resolve per unit with the global config as fallback. Non-default upstream branches are config-gated and off by default: SRA download (get_sra), single-end mode (fastp_se + star_align_se), raw-read alignment (trimming_activate = false), bwa index and samtools faidx.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">31</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 24 CPUs per rule (star_align)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">transcriptomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/snakemake-workflows/rna-seq-star-deseq2">snakemake-workflows/rna-seq-star-deseq2</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v3.1.1</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs reference genome, annotation and reads — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.12.0 (per-unit metadata features — per-unit fastp_adapters/fastp_extra lookup and the SRA auto-feed — require >= 0.17.0; on older engines the global config defaults apply)

**Toolchain.** conda envs — pinned

**Requirements.**

- paired-end FASTQ reads per config/units.tsv (raw/<unit-key>_R1.fastq.gz / _R2.fastq.gz) and sample conditions in config/samples.tsv
- reference genome + annotation downloaded automatically from Ensembl release 115 (GRCh38) — network access required (also for biomaRt gene-symbol annotation)
- compute: up to 24 CPUs per rule (star_align); 8 (fastp_pe); 4 (fastp_se, star_index); no per-rule memory limits configured in the workflow
- disk: several tens of GB — ~30 GB GRCh38 STAR index, plus BAMs and trimmed reads

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-rnaseq-star-deseq2
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-rnaseq-star-deseq2
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `annotation_gtf` | `` | — | `get_annotation` |
| `annotation_url` | `ftp://ftp.ensembl.org/pub/release-115/gtf/homo_sapiens/Homo_sapiens.GRCh38.115.gtf.gz` | — | `get_annotation` |
| `biomart_species` | `hsapiens` | biomaRt species dataset suffix (upstream get_bioc_species_name()). | `gene_2_symbol_counts`, `gene_2_symbol_diffexp`, `gene_2_symbol_normcounts` |
| `bwa_index_activate` | `false` | Activate the BWA index / samtools faidx rules. Upstream declares both but its default path never requests them (snakemake lazy evaluation); oxo-flow runs every rule in the file, so both are gated off unless activated. | `bwa_index` |
| `contrast_exprs` | `` | String-form DESeq2 contrasts (upstream diffexp.contrasts string entries, e.g. 'list(c("treatment_1_treated_vs_untreated", ...))'). Semicolon-joined list parallel to `contrasts`; an empty entry = list-form for that contrast. Entries are R expressions evaluated by DESeq2: use single quotes for R strings (the value is double-quoted on the shell command line) and no semicolons inside an entry. | `deseq2` |
| `contrast_levels` | `treated` | — | `deseq2` |
| `contrast_variables` | `treatment_1` | — | `deseq2` |
| `contrasts` | `treatment_1` | Contrasts (upstream: diffexp.contrasts). One comma-joined entry per contrast: contrast id, its variable_of_interest, its level_of_interest. The base level comes from diffexp_base_levels. | `deseq2` |
| `diffexp_base_levels` | `untreated,untreated` | — | `deseq2`, `deseq2_init` |
| `diffexp_batch_effects` | `jointly_handled` | — | `deseq2_init` |
| `diffexp_model` | `` | — | — |
| `diffexp_variables` | `treatment_1,treatment_2` | Differential expression (upstream: diffexp.*). Comma-joined lists mirror the upstream nested tables; positions pair up (treatment_1 -> untreated, treatment_2 -> untreated). | `deseq2`, `deseq2_init` |
| `fastp_adapters` | `--detect_adapter_for_pe` | fastp adapter args and extra args (upstream: per-unit columns fastp_adapters / fastp_extra in config/units.tsv, looked up per unit via the metadata binding — {meta.fastp_adapters} / {meta.fastp_extra} render per unit and these global keys are the per-unit defaults when a unit's column is empty; equal the upstream defaults). fastp_adapters_se matches the upstream single-end default (""). | `fastp_pe` |
| `fastp_adapters_se` | `` | — | `fastp_se` |
| `fastp_extra` | `--trim_poly_x --poly_x_min_len 7 --trim_poly_g --poly_g_min_len 7` | — | `fastp_pe`, `fastp_se` |
| `genome_faidx_activate` | `false` | — | `genome_faidx` |
| `genome_fasta` | `` | Local reference overrides: set to a local FASTA/GTF to skip the Ensembl download entirely (offline machines, tiny test runs). Empty = download (the upstream-faithful default). A tiny synthetic kit ships at test/fixtures/reference/ with matching reads in raw-synthetic/. | `get_genome` |
| `genome_url` | `https://ftp.ensembl.org/pub/release-115/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz` | — | `get_genome` |
| `genome_url_toplevel` | `https://ftp.ensembl.org/pub/release-115/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.toplevel.fa.gz` | — | `get_genome` |
| `pca_activate` | `true` | PCA (upstream: pca.activate / pca.labels). pca_variables is the derived upstream list (variables_of_interest + batch_effects + labels), kept explicit here — keep it in sync with the diffexp keys below. | `pca_jointly_handled`, `pca_treatment_1`, `pca_treatment_2` |
| `pca_labels` | `` | — | — |
| `pca_variables` | `treatment_1,treatment_2,jointly_handled` | — | — |
| `raw_dir` | `test/fixtures/raw` | Directory holding <unit-key>_R1.fastq.gz / _R2.fastq.gz per config/units.tsv. The repo default ships the tiny test fixtures; point this at your data (e.g. "raw"). | `fastp_pe`, `fastp_se`, `star_align_raw`, `star_align_se_raw` |
| `ref_build` | `GRCh38` | — | — |
| `ref_release` | `115` | — | — |
| `ref_species` | `homo_sapiens` | Reference (upstream: ref.species / ref.release / ref.build). The download URLs below are the Ensembl URLs the wrappers resolve for these values. | — |
| `single_end` | `false` | Single-end mode (upstream decides per sample from the units.tsv fq2/sra columns; the port applies it globally — engine rules have fixed input arities). Single-end units provide only <unit-key>_R1.fastq.gz. Default false = the paired-end path. | `fastp_pe`, `fastp_se`, `star_align`, `star_align_raw`, `star_align_se`, `star_align_se_raw` |
| `sra_accessions` | `` | SRA auto-feed master switch (upstream get_sra branch: units whose fq1/fq2 are empty carry an sra accession in config/units.tsv). Any non-empty value enables the per-unit download; each unit's accession comes from its units sheet sra column (the {meta.sra} lookup), and reads land at <raw_dir>/<unit-key>_R{1,2}.fastq.gz (the raw_dir convention) so the trimming/alignment rules consume them automatically (upstream get_units_fastqs). Default empty = no SRA download. Requires oxo-flow >= 0.17.0 — on older engines keep this empty (the per-unit sra column is not read, and the gate then stays closed). | `get_sra` |
| `star_align_extra` | `` | — | `star_align`, `star_align_raw`, `star_align_se`, `star_align_se_raw` |
| `star_index_extra` | `` | STAR extra params (upstream: params.star.index / params.star.align). | `star_index` |
| `trimming_activate` | `true` | Trimming (upstream: trimming.activate). With trimming off, the port's star_align_raw / star_align_se_raw variants feed the raw reads to STAR, mirroring the upstream rewiring (get_fq with trimming.activate = False). | `fastp_pe`, `fastp_se`, `star_align`, `star_align_raw`, `star_align_se`, `star_align_se_raw` |
| `units_file` | `config/units.tsv` | — | `count_matrix` |

{: .ox-params }

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-rnaseq-star-deseq2 rule-level DAG](../assets/dag/oxo-flow-rnaseq-star-deseq2.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- bwa_index
- count_matrix
- deseq2
- deseq2_init
- fastp_pe
- fastp_se
- gene_2_symbol_counts
- gene_2_symbol_diffexp
- gene_2_symbol_normcounts
- genome_faidx
- get_annotation
- get_genome
- get_sra
- multiqc
- pca_jointly_handled
- pca_treatment_1
- pca_treatment_2
- rseqc_gtf2bed
- rseqc_infer
- rseqc_innerdis
- rseqc_junction_annotation
- rseqc_junction_saturation
- rseqc_readdis
- rseqc_readdup
- rseqc_readgc
- rseqc_stat
- star_align
- star_align_raw
- star_align_se
- star_align_se_raw
- star_index

**Excluded**

- Snakemake report artifacts (workflow/report/*.rst) — jinja captions rendered by the sphinx-based snakemake --report machinery (report: directive + report() output annotations); no oxo-flow equivalent

## Fidelity

Scope: the **default-parameters main execution path** (upstream `rule all`).
Rows cover every upstream rule; "not ported" rows carry a reason. Upstream
rules use snakemake wrappers v7.2.0 (`bio/fastp`, `bio/star/*`,
`bio/multiqc`, `bio/reference/ensembl-*`, `bio/samtools/faidx`,
`bio/bwa/index`, `bio/sra-tools/fasterq-dump`) whose conda pins were carried
over verbatim. Rules that upstream declares but never runs in the default
path (get_sra, fastp_se, bwa_index, genome_faidx) and the alternate
trimming/SE wiring are ported as config-gated rules (see the `when`/flag
notes per row); they appear as `skip` in the default dry-run plan.

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| get_genome | `get_genome` | curl (system) + Ensembl FTP/HTTPS | ensembl-sequence wrapper: primary_assembly URL with toplevel fallback; probe/fallback restructured into shell, HTTPS branch only (upstream also probes FTP) |
| get_annotation | `get_annotation` | curl (system) + Ensembl FTP/HTTPS | ensembl-annotation wrapper, identical URL + `gzip -d` logic |
| star_index | `star_index` | STAR 2.7.11b | star/index wrapper verbatim; tmpdir moved to `.oxo-flow/tmp/star_index` |
| fastp_pe | `fastp_pe` | fastp 1.0.1 | fastp wrapper verbatim (extra + adapters + reads + trimmed + json + html ordering); upstream per-unit `fastp_adapters`/`fastp_extra` lookup() columns → per-unit `{meta.fastp_adapters}`/`{meta.fastp_extra}` from the units sheet (`config/units.tsv`), with the global `[config] fastp_adapters`/`fastp_extra` as per-unit defaults (empty column → global value, both equal upstream defaults) |
| star_align | `star_align` (+ `star_align_raw`, `star_align_se`, `star_align_se_raw`) | STAR 2.7.11b | star/align wrapper verbatim: `--outSAMtype BAM SortedByCoordinate --quantMode GeneCounts --sjdbGTFfile "<gtf>"` in the upstream extra-string order, `--readFilesCommand gunzip -c`, `--outStd BAM_SortedByCoordinate` to the BAM, `cat` of ReadsPerGene/SJ/Logs out of the tmp prefix. Upstream's one rule takes trimmed or raw, one or two reads per sample (get_fq + units.tsv); engine rules have fixed input patterns, so the port makes the 2×2 matrix explicit: PE-trimmed (default), PE-raw (`trimming_activate = false`), SE-trimmed, SE-raw — each gated so exactly one variant is active |
| get_sra | `get_sra` | sra-tools 3.2.1 | fasterq-dump wrapper verbatim (`-x`, tmpdir via `mktemp -d`, log `logs/get-sra/{sample}.log`); per-unit auto-feed ported via the units sheet `sra` column: `{meta.sra}` routes each unit to its own accession, gated on `config.sra_accessions != ''` as the master switch (default empty → skip; upstream triggers per unit from the same column). Deviation: upstream writes uncompressed `sra/{accession}_1.fastq` and get_units_fastqs binds them as inputs; the port gzips into `<raw_dir>/<unit-key>_R{1,2}.fastq.gz` (the raw_dir naming convention) so the trimming/alignment rules consume the reads without per-unit input binding. On engines < 0.17.0 keep the default empty `sra_accessions` — the per-unit auto-feed requires the `{meta.*}` binding (oxo-flow >= 0.17.0) |
| fastp_se | `fastp_se` | fastp 1.0.1 | fastp wrapper verbatim (single-end arg set: `--in1 --out1 --failed_out --json --html`); gated on `single_end && trimming_activate` (default off). Deviation: upstream writes the shared `{sample}-{unit}.json` for both SE and PE; the port names the SE report `{sample}_single.json` because two rules must not share an output file here |
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
| pca | `pca_treatment_1` / `pca_treatment_2` / `pca_jointly_handled` | DESeq2 1.46.0 | plot-pca.R verbatim (`rlog(blind=FALSE)`, `plotPCA(intgroup=variable)`); one explicit rule per `pca_variables` entry (the engine's scatter does not substitute `{variable}` inside the script field), gated by `pca_activate` |
| deseq2 | `deseq2` | DESeq2 1.46.0, r-ashr 2.2_63 | deseq2.R logic identical (list-form contrast = vof + level + base_level, ashr `lfcShrink`, `order(padj)`, MA plot); string-form contrasts ported via `contrast_exprs` (semicolon-joined R expressions parallel to `contrasts`, e.g. `list(c('a_vs_b', ...))`, evaluated `eval(parse(text = ...))` verbatim like upstream; entries must use single-quoted R strings and no semicolons); one instance per `contrasts` entry |
| bwa_index | `bwa_index` | bwa 0.7.19 | bwa/index wrapper verbatim: `-b <size/10 MB, clamped to [10, 51200]>M -p resources/genome.fasta` (the wrapper's block-size formula, replicated with `wc -c` + shell arithmetic), outputs `resources/genome.fasta.{amb,ann,bwt,pac,sa}`; gated on `bwa_index_activate` (default off — upstream `rule all` never requests it; snakemake lazy evaluation vs oxo-flow runs every rule) |
| genome_faidx | `genome_faidx` | samtools 1.22 | `samtools faidx` wrapper verbatim → `resources/genome.fasta.fai`; gated on `genome_faidx_activate` (same reasoning as bwa_index) |
| report/ (`report/*.rst`) | not ported | — | Snakemake report artifacts: the `.rst` captions are jinja templates rendered by the sphinx-based `snakemake --report` machinery (`report:` directive + `report()` output annotations); no oxo-flow equivalent |
| trimming.activate = False rewiring | `star_align_raw` / `star_align_se_raw` | STAR 2.7.11b | upstream then feeds raw reads to star_align; ported as explicit variants gated on `!trimming_activate` |
| edger / kallisto / trimgalore | n/a | — | not present in upstream v3.1.1 (fastp is the trimmer, DESeq2 the DE tool) |

**Port-level conventions** (config-shape deviations, commands unchanged):
upstream wildcards are `(sample, unit)`; the port fans out over one composite
`{sample}` = `<sample>-<unit>` (e.g. `A-lane1`), so output paths are
byte-identical to upstream (`results/trimmed/A-lane1/A-lane1_R1.fastq.gz`,
`results/star/A-lane1/...`). Nested upstream config (`diffexp.*`, `ref.*`,
`trimming.activate`, `pca.*`) is flattened into flat `[config]` keys with the
same defaults (see `main.oxoflow` header). The upstream `config/samples.tsv`
demo sheet ships with the port, extended with replicate units F/G/H so every
treatment combination has ≥2 samples (a DESeq2 run requirement): 8 samples
(A–H), 9 units (A-lane1, A-lane2, B–H lane1). Raw reads live at
`<raw_dir>/<unit-key>_R1.fastq.gz` / `_R2.fastq.gz` (`[config] raw_dir`
defaults to `test/fixtures/raw/`, which contains tiny real reads so the
dry-run resolves every input; point it at your data, e.g. `raw_dir = "raw"`).
Upstream demo-data FASTQ paths (`A.1.fq.gz` etc.) were renamed to this
convention — data-path substitution only. `config/units.tsv` keeps the
upstream columns (`sample_name`, `unit_name`, `fq1`, `fq2`, `sra`,
`strandedness`, `fastp_adapters`, `fastp_extra`) and adds a leading
`unit_key` column holding the composite `{sample}` wildcard values
(`A-lane1`, …) — the sheet doubles as the workflow's metadata table
(`[workflow] metadata_file`): `{meta.sra}`, `{meta.fastp_adapters}` and
`{meta.fastp_extra}` resolve per unit, and an empty per-unit cell falls back
to the global config defaults (upstream `lookup()` semantics).


## Links

- Repository: [oxo-flow-rnaseq-star-deseq2](https://github.com/oxo-flow-community/oxo-flow-rnaseq-star-deseq2)
- Upstream: [snakemake-workflows/rna-seq-star-deseq2](https://github.com/snakemake-workflows/rna-seq-star-deseq2) @ `v3.1.1`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
