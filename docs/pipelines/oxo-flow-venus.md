---
title: "Tumor multi-omics WGS/WES: somatic SNV/indel, CNV, SV, MSI and signature analysis with bulk/scRNA-seq cohort clinical reporting"
description: "Tumor multi-omics WGS/WES: somatic SNV/indel, CNV, SV, MSI and signature analysis with bulk/scRNA-seq cohort clinical reporting — the community-listed (☆) entry, cancer genomics, oxo-flow workflow, 78 rules, 19 tools."
---
---
title: "Tumor multi-omics WGS/WES: somatic SNV/indel, CNV, SV, MSI and signature analysis with bulk/scRNA-seq cohort clinical reporting"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-venus</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Tumor multi-omics WGS/WES: somatic SNV/indel, CNV, SV, MSI and signature analysis with bulk/scRNA-seq cohort clinical reporting</h1>
<div class="ox-page-badges"><span class="ox-badge ">☆ Community</span> <span class="ox-badge ox-badge--origin">Original</span> <span class="ox-badge ox-badge--native"><span class="dot" aria-hidden="true"></span>oxo-flow native</span><span class=ox-tag-sep></span><span class="ox-tag">tumor-multi-omics</span><span class="ox-tag">wgs</span><span class="ox-tag">wes</span><span class="ox-tag">somatic-calling</span><span class="ox-tag">mutect2</span><span class="ox-tag">copy-number-analysis</span><span class="ox-tag">structural-variants</span><span class="ox-tag">msi</span><span class="ox-tag">mutational-signatures</span><span class="ox-tag">bulk-rna-seq</span><span class="ox-tag">single-cell-rna-seq</span><span class="ox-tag">ecdna</span><span class="ox-tag">neoantigen</span><span class="ox-tag">clinical-report</span><span class="ox-tag">hla</span></div>
<p class="ox-desc">Tumor multi-omics pipeline covering the full path from raw FASTQ to a cohort clinical report with an auto-generated methods section. DNA chain: BWA-MEM2 alignment with MarkDuplicates and BQSR, Mutect2 somatic SNV/indel calling in paired and tumor-only modes with orientation-bias filtering, CNVkit copy-number profiles, ASCAT purity/ploidy fits, AmpliconSuite ecDNA classification, Manta SVs, MSIsensor MSI and in-house SBS96/COSMIC signature fits, annotated with vep-rs and tiered by CIViC-based clinical interpretation. RNA chain: two-pass STAR + featureCounts bulk RNA-seq with fusion screening, dnbc4tools single-cell counting, and SpecHLA -&gt; VEP -&gt; pVACseq/pVACfuse neoantigen prediction. Cohort reports (TMB, clinical evidence tables, MSI/frameshift and ICB pages) aggregate exactly the runs that executed, per the engine rule_runs checkpoint.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#preview-the-plan">▶ Preview the plan</a><a class="ox-btn" href="https://github.com/WangLabCSU/oxo-flow-venus" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow dry-run venus.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v">☆ Community</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">78</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">—</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--native"><span class="dot" aria-hidden="true"></span>oxo-flow native</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Original</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">cancer genomics</span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v0.5.0</code></span></div>
<div class="ox-kv"><span class="k">Added</span><span class="v">2026-05-19</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastp</span><span class="tchip">fastqc</span><span class="tchip">multiqc</span><span class="tchip">bwa-mem2</span><span class="tchip">picard</span><span class="tchip">gatk4</span><span class="tchip">mutect2</span><span class="tchip">vep-rs</span></div></div>
<p class="cmd">$ oxo-flow pull gh:WangLabCSU/oxo-flow-venus</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#preview-the-plan">Usage</a><a href="#scope">Scope</a></nav>


## Preview the plan

```bash
oxo-flow dry-run venus.oxoflow
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-venus` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:WangLabCSU/oxo-flow-venus@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:WangLabCSU/oxo-flow-venus` fetches the repo, then `oxo-flow dry-run venus.oxoflow`.


Data-gated tumor multi-omics pipeline (WGS/WES + bulk/scRNA inputs, cohort sheets). Dry-run validates the DAG without compute; committed `tests/` parse and cross-check the shipped workflow fragments and pixi environments.

## Installation

**Engine.** oxo-flow >= 0.24 (README Requirements; the [engine] disk-pressure guard additionally needs engine commit a456c796+ — oxo-flow PR #845)

**Toolchain.** pixi — pinned per-rule environments in envs/*/pixi.toml (pixi.lock present for all modules except arcas); resolved into .oxo-flow/pixi/ at run time

**Requirements.**

- Linux x86-64
- Reference data (exact keys in venus.oxoflow [config]): GRCh38 FASTA with UCSC-style chr-prefixed contigs (chr1..chrX, chrM) + BWA-MEM2 index, STAR index + GENCODE GTF, GATK resource bundle (dbsnp/mills/gnomad/PoN), vep-rs binary + JSON cache, single-cell reference for dnbc4tools, CNVkit normal reference for tumor-only CNV
- pixi on PATH (workflow environments resolve per rule into .oxo-flow/pixi/)
- cohort inputs: raw/{sample}_R1.fastq.gz / _R2.fastq.gz in the run workdir; cohort declared in config/pairs.tsv (paired and tumor-only pairs may mix, gated per pair) and config/groups.tsv (assay column drives the wgs/rnaseq/scrna per-sample gating)

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (bioconda's oxo-flow-cli tracks releases with a lag):
#    conda install -c bioconda oxo-flow-cli
#    Check `oxo-flow --version` against the Engine minimum above — if
#    bioconda trails it, use the release binary instead.

# 2. get this workflow (clones the repo, auto-discovers the workflow,
#    sanity-parses it with the engine)
oxo-flow pull gh:WangLabCSU/oxo-flow-venus
#    (alternative: plain git clone)
#    git clone https://github.com/WangLabCSU/oxo-flow-venus
```

## Scope

Native oxo-flow design — no upstream port: steps implemented by this workflow are listed as in scope; alternate paths of the domain's conventional pipelines appear under excluded.

**In scope**

- ampliconsuite
- ascat_cohort
- ascat_cohort_tumoronly
- ascat_paired
- bqsr
- bqsr_passthrough
- bwa_mem2
- clinical_biomarkers_paired
- clinical_biomarkers_tumoronly
- clinical_cnv_genes
- clinical_cohort
- clinical_kb_prep
- clinical_oncokb
- clinical_oncokb_skip
- clinical_report
- clinical_snv_annotate
- clinical_sv_fusions_paired
- clinical_sv_fusions_tumoronly
- cnvkit_paired
- cnvkit_tumoronly
- cohort_tables
- ecdna_cohort
- fastp
- fastqc
- featurecounts
- filter_mutect
- gather_chr_vcfs
- gene_symbol_map
- hla_dna_rna_qc
- hla_loh
- hla_type_dna
- hla_type_rna
- icb_linkage_page
- learn_orientation
- manta_paired
- manta_tumoronly
- mark_duplicates
- merge_counts
- merge_mutect_stats
- methods_from_rule_runs
- msi_cohort
- msi_cohort_tumoronly
- msi_frameshift_page
- msi_paired
- msisensor_scan
- multiqc
- mutect2_paired
- mutect2_tumoronly
- neoantigen_cohort
- neoantigen_cohort_paired
- neoantigen_report
- neoantigen_report_scrna
- pvacfuse_run_paired
- pvacfuse_run_tumoronly
- pvacseq_run
- rna_fusion_cohort
- rna_fusion_screen
- rna_qc_summary
- sbs96_fit
- scrna_corroboration
- scrna_count
- scrna_fastqc
- scrna_integrate
- scrna_metrics_cohort
- scrna_qc_cluster
- select_pass
- star_align
- sv_deliver_paired
- sv_deliver_tumoronly
- tcr_from_rna
- tmb_per_pair
- vcf2maf
- vep_annotate
- vep_reannotate_plugins
- wgs_alignqc_summary
- wgs_bamstats
- wgs_flagstat
- wgs_mosdepth

**Excluded**

- none

## Links

- Repository: [oxo-flow-venus](https://github.com/WangLabCSU/oxo-flow-venus)
- Upstream: [WangLabCSU/oxo-flow-venus](https://github.com/WangLabCSU/oxo-flow-venus) @ `v0.5.0`
- License: Apache-2.0 (this workflow) · Apache-2.0 (upstream)

Created on 2026-05-19 — this entry may lag behind upstream releases. See the repository's NOTICE for full attribution.
