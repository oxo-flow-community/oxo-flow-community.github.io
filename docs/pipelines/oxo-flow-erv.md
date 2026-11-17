---
title: "ERV / transposable-element quantification with four tools on one annotation"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-erv</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>ERV / transposable-element quantification with four tools on one annotation</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--dry">◆ Dry-run verified</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot" aria-hidden="true"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">erv</span><span class="ox-tag">transposable-elements</span><span class="ox-tag">rna-seq</span><span class="ox-tag">ervmap</span><span class="ox-tag">telescope</span><span class="ox-tag">squire</span><span class="ox-tag">tetranscripts</span><span class="ox-tag">star</span><span class="ox-tag">featurecounts</span><span class="ox-tag">snakemake</span></div>
<p class="ox-desc">RNA-seq from FASTQ to a comparable ERV expression table. fastp trims and STAR aligns; four published tools quantify endogenous retroviruses on one RepeatMasker-derived annotation (ERVmap at provirus level from the official 3,220-provirus BED, Telescope and TEtranscripts at locus level, SQuIRE at locus and subfamily level); featureCounts gives gene counts from the same BAMs; the aggregation layer writes a unified long table, per-sample QC and per-subfamily cross-tool evidence. Sample groups (cohorts) are a first-class directory level, and ERVmap is computed here instead of imported, with guards for the BED chromosome-name and contig-order pitfalls. ERVmap is quantified here instead of imported, using the official wrapper&#x27;s STAR parameters and bedtools coverage step. Paired- and single-end layouts are both supported.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-erv" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">◆ Dry-run verified</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">22</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">—</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot" aria-hidden="true"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">transcriptomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/SunPast/ERV-pipeline">SunPast/ERV-pipeline</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>main@02ae748</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-11-05</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastp</span><span class="tchip">star</span><span class="tchip">samtools</span><span class="tchip">subread</span><span class="tchip">bedtools</span><span class="tchip">ervmap</span><span class="tchip">telescope</span><span class="tchip">tetranscripts</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-erv</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#run-it">Usage</a><a href="#scope">Scope</a></nav>


## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-erv
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-erv` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-erv@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-erv` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


## Installation

**Engine.** oxo-flow >= 0.13.1

**Toolchain.** conda envs — pinned versions (fastp 0.23.4, STAR 2.7.7a, samtools 1.15/1.18, subread 2.0.1, bedtools 2.31.1, telescope 1.0.3, tetranscripts 2.2.3, squire 0.9.9.92, python 3.10; conda-forge + bioconda)

**Requirements.**

- GRCh38 genome FASTA, GENCODE GTF, UCSC hg38_rmsk.txt and the official ERVmap BED with a chr prefix (3,220 proviruses)
- reads at reads_dir/<sample>_1.fastq.gz (+ _2.fastq.gz for layout = "pe") for every sample in [[sample_groups]]
- compute: up to 10 threads per rule (STAR), 32 GB for STAR
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
oxo-flow pull gh:oxo-flow-community/oxo-flow-erv
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-erv
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastp_pe
- fastp_se
- star_align_pe
- star_align_se
- samtools_sort
- featurecounts_pe
- featurecounts_se
- genome_fai
- build_locus_gtf
- build_full_locus_map
- squire_clean_folder
- ervmap_bed_sorted
- ervmap_annotate
- ervmap_star_pe
- ervmap_star_se
- ervmap_count
- ervmap_normalize
- telescope_assign
- tetranscripts_count
- squire_count
- aggregate_sample
- merge_aggregate

**Excluded**

- merge_gene_counts
- compute_gene_factors
- import_external_gene_counts
- export_standard
- squire_map

## Links

- Repository: [oxo-flow-erv](https://github.com/oxo-flow-community/oxo-flow-erv)
- Upstream: [SunPast/ERV-pipeline](https://github.com/SunPast/ERV-pipeline) @ `main@02ae748`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-11-05 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
