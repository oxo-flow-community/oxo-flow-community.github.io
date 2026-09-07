---
title: "Variant calling for non-model organisms: trimming, alignment, per-sample gVCFs, joint genotyping, callable sites, postprocessing and QC dashboard"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-snparcher</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Variant calling for non-model organisms: trimming, alignment, per-sample gVCFs, joint genotyping, callable sites, postprocessing and QC dashboard</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">variant-calling</span><span class="ox-tag">population-genomics</span><span class="ox-tag">gatk</span><span class="ox-tag">bwa</span><span class="ox-tag">non-model-organisms</span><span class="ox-tag">snakemake</span><span class="ox-tag">deepvariant</span><span class="ox-tag">sra</span><span class="ox-tag">callable-sites</span></div>
<p class="ox-desc">Variant calling for non-model organisms: paired FASTQ reads (or SRA accessions, or external BAMs) are trimmed and filtered with fastp, aligned with BWA-MEM, optionally duplicate-marked with sambamba, and called to per-sample gVCFs with GATK HaplotypeCaller or DeepVariant (low-coverage defaults: -ploidy 2, --min-pruning 1). Optional upstream branches are gated by config keys: joint genotyping (GenomicsDBImport + GenotypeGVCFs, or GLnexus for DeepVariant), GATK hard variant filtration, callable-sites BED (mosdepth/clam coverage + genmap mappability), the postprocess module (clean SNP/indel call sets), the qc module (PLINK PCA/relatedness, ADMIXTURE, interactive dashboard), and a cohort QC metrics report. Two runtime-fan-out branches are ported with the engine&#x27;s output_pattern primitive (oxo-flow &gt;= 0.17): interval scatter (per-interval gVCF calling and per-shard joint genotyping) and the per-region bcftools caller; both default off. Long-contig (CSI) VCF indexing is auto-selected when any reference contig exceeds the 512 Mb TBI limit (long_contig_mode config: auto/true/false), mirroring upstream&#x27;s TBI_MAX_CONTIG_LENGTH decision; the postprocess module (basic/strict filtering, clean SNP/indel sets) follows the same CSI twin pattern.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-snparcher" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow reference_source=/path/to/genome.fa.gz</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">74</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 8 CPUs / 8 GB per rule (bwa_mem)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/harvardinformatics/snparcher">harvardinformatics/snparcher</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v2.2</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2292.1"><code>10.48546/workflowhub.workflow.2292.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastp</span><span class="tchip">bwa</span><span class="tchip">samtools</span><span class="tchip">gatk4</span><span class="tchip">picard</span><span class="tchip">sambamba</span><span class="tchip">sra-tools</span><span class="tchip">deepvariant</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow reference_source=/path/to/genome.fa.gz</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>snpArcher pipeline</strong>: variant calling for non-model organisms — trims reads, aligns, calls per-sample gVCFs, and optionally joint-genotypes, filters, and runs population QC.</p>
<p><strong>1. Reference preparation</strong> — <code>prepare_reference</code> bgzip-compresses the reference FASTA; <code>index_reference</code> builds the samtools and BWA indexes nearly every later step consumes.</p>
<p><strong>2. Read trimming and alignment</strong> — local FASTQ pairs are trimmed by <code>fastp</code>; SRA cohorts instead run <code>download_sra</code> -&gt; <code>fastp_srr</code>. Both feed <code>bwa_mem</code>, then <code>merge_library_bams</code> merges per-library BAMs. The final BAM is <code>merge_library_level_bams</code> + <code>index_bam_csi</code> (default) or, with duplicate marking, <code>markdup_library</code> -&gt; <code>merge_dedup_libraries</code> + <code>index_bam_csi_markdup</code>; external BAMs enter at <code>stage_external_bam</code> + <code>index_bam_csi_external</code>.</p>
<p><strong>3. Per-sample variant calling</strong> — <code>gatk_haplotypecaller</code> (with <code>gatk_haplotypecaller_markdup</code> and <code>gatk_haplotypecaller_external</code>) emits one gVCF per sample, as do the <code>deepvariant_call</code> variants. The bcftools route is <code>bcftools_regions</code> -&gt; <code>bcftools_call</code> -&gt; <code>bcftools_concat_regions</code>; GATK interval scatter runs <code>picard_intervals</code> -&gt; <code>filter_picard_intervals</code> -&gt; <code>create_gvcf_intervals</code> -&gt; <code>gatk_haplotypecaller_interval</code> -&gt; <code>concat_interval_gvcfs</code>. One route runs per cohort, chosen by configuration and input type.</p>
<p><strong>4. Joint genotyping</strong> — <code>create_db_mapfile</code> -&gt; <code>joint_genomics_db_import</code> -&gt; <code>joint_genotype_gvcfs</code> genotypes the cohort (interval mode: <code>create_db_intervals</code> -&gt; <code>gatk_genomics_db_import_interval</code> -&gt; <code>gatk_genotype_gvcfs_interval</code> -&gt; <code>concat_interval_vcfs</code>); DeepVariant gVCFs instead go through <code>glnexus_joint</code>, and external gVCFs are normalized by <code>normalize_external_gvcf_for_gatk</code>. All routes converge on the joint raw VCF, which <code>variant_filtration</code> hard-filters when enabled.</p>
<p><strong>5. QC, callable sites, and final modules</strong> — <code>collect_fastp_stats</code> and <code>bam_stats</code> (with <code>bam_stats_markdup</code> and <code>bam_stats_external</code>) feed <code>parse_bam_stats</code> -&gt; <code>combine_qc_metrics</code>; callable sites flow <code>mosdepth</code> -&gt; <code>clam_collect</code>/<code>callable_coverage_thresholds</code> -&gt; <code>clam_loci</code> -&gt; <code>coverage_bed</code> and <code>genmap_index</code> -&gt; <code>genmap_mappability</code> -&gt; <code>mappability_bed</code>, merged by <code>callable_sites_bed</code>. The postprocess chain (<code>postprocess_basic_filter</code> -&gt; <code>postprocess_strict_filter</code> -&gt; <code>postprocess_subset_indels</code>/<code>postprocess_subset_snps</code> -&gt; <code>postprocess_drop_indel_snps</code>) and the QC module (<code>qc_subsample_snps</code> -&gt; <code>qc_prepare_plink_inputs</code> -&gt; <code>qc_plink</code> -&gt; <code>qc_setup_admixture</code> -&gt; <code>qc_admixture</code>) converge on <code>qc_dashboard</code>.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-snparcher+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-snparcher reference_source=/path/to/genome.fa.gz
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-snparcher` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-snparcher@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-snparcher` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Set your reference genome as shown; preview with `oxo-flow dry-run main.oxoflow`.

## Installation

**Engine.** oxo-flow >= 0.12.0 (interval-scatter and bcftools branches need output_pattern: >= 0.17)

**Toolchain.** conda envs — pinned versions (fastp 1.3.6, bwa 0.7.19, samtools 1.24, gatk4 4.6.2.0, sambamba 1.0.1, sra-tools 3.2.1, mosdepth 0.3.3, vcftools 0.1.16, bcftools 1.23, plink2; conda-forge + bioconda); deepvariant branch needs a docker backend

**Requirements.**

- reference genome FASTA (plain or gzip), passed as reference_source at run time — bgzip-compressed and indexed by the workflow itself (no pre-built indices)
- paired-end reads at raw/<sample>_1.fastq.gz and raw/<sample>_2.fastq.gz for fastq samples; SRA accession metadata for srr samples; bam_path metadata for bam samples
- compute: up to 8 CPUs / 8 GB per rule (bwa_mem 8 threads, fastp 4, gatk_haplotypecaller 7 GB Java heap)
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
oxo-flow pull gh:oxo-flow-community/oxo-flow-snparcher
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-snparcher
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bcftools_max_depth = value" data-copy="bcftools_max_depth = 250">bcftools_max_depth</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>250</code></td>
<td class="ox-p-desc">bcftools tool parameter (upstream --bcftools_max_depth) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bcftools_min_baseq = value" data-copy="bcftools_min_baseq = 20">bcftools_min_baseq</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>20</code></td>
<td class="ox-p-desc">bcftools tool parameter (upstream --bcftools_min_baseq) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bcftools_min_mapq = value" data-copy="bcftools_min_mapq = 20">bcftools_min_mapq</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>20</code></td>
<td class="ox-p-desc">bcftools tool parameter (upstream --bcftools_min_mapq) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy callable_sites_enabled = value" data-copy="callable_sites_enabled = false">callable_sites_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">callable tool parameter (upstream --callable_sites_enabled) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>18</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy callable_sites_fraction = value" data-copy="callable_sites_fraction = 1.0">callable_sites_fraction</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>1.0</code></td>
<td class="ox-p-desc">callable tool parameter (upstream --callable_sites_fraction) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy callable_sites_kmer = value" data-copy="callable_sites_kmer = 150">callable_sites_kmer</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>150</code></td>
<td class="ox-p-desc">callable tool parameter (upstream --callable_sites_kmer) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy callable_sites_max_coverage = value" data-copy="callable_sites_max_coverage = auto">callable_sites_max_coverage</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>auto</code></td>
<td class="ox-p-desc">callable tool parameter (upstream --callable_sites_max_coverage) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy callable_sites_merge_distance = value" data-copy="callable_sites_merge_distance = 100">callable_sites_merge_distance</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">callable tool parameter (upstream --callable_sites_merge_distance) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy callable_sites_min_coverage = value" data-copy="callable_sites_min_coverage = auto">callable_sites_min_coverage</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>auto</code></td>
<td class="ox-p-desc">callable tool parameter (upstream --callable_sites_min_coverage) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy callable_sites_min_score = value" data-copy="callable_sites_min_score = 1">callable_sites_min_score</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">callable tool parameter (upstream --callable_sites_min_score) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy deepvariant_model_type = value" data-copy="deepvariant_model_type = WGS">deepvariant_model_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>WGS</code></td>
<td class="ox-p-desc">deepvariant tool parameter (upstream --deepvariant_model_type) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy expected_coverage = value" data-copy="expected_coverage = low">expected_coverage</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>low</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_het_prior = value" data-copy="gatk_het_prior = 0.005">gatk_het_prior</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.005</code></td>
<td class="ox-p-desc">gatk tool parameter (upstream --gatk_het_prior) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy generate_filtered_vcf = value" data-copy="generate_filtered_vcf = false">generate_filtered_vcf</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy intervals_db_max_contigs_per_shard = value" data-copy="intervals_db_max_contigs_per_shard = 200">intervals_db_max_contigs_per_shard</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>200</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy intervals_db_max_intervals_per_shard = value" data-copy="intervals_db_max_intervals_per_shard = 200">intervals_db_max_intervals_per_shard</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>200</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy intervals_db_scatter_factor = value" data-copy="intervals_db_scatter_factor = 0.15">intervals_db_scatter_factor</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.15</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy intervals_enabled = value" data-copy="intervals_enabled = false">intervals_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>16</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy intervals_min_contig_length = value" data-copy="intervals_min_contig_length = 0">intervals_min_contig_length</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy intervals_min_nmer = value" data-copy="intervals_min_nmer = 500">intervals_min_nmer</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>500</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy intervals_scatter_count = value" data-copy="intervals_scatter_count = 50">intervals_scatter_count</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>50</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy joint_genotyping_enabled = value" data-copy="joint_genotyping_enabled = false">joint_genotyping_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mark_duplicates = value" data-copy="mark_duplicates = false">mark_duplicates</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>15</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy modules_postprocess_enabled = value" data-copy="modules_postprocess_enabled = false">modules_postprocess_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy modules_qc_enabled = value" data-copy="modules_qc_enabled = false">modules_qc_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ploidy = value" data-copy="ploidy = 2">ploidy</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy postprocess_contig_size = value" data-copy="postprocess_contig_size = 10000">postprocess_contig_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10000</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy postprocess_exclude_scaffolds = value" data-copy="postprocess_exclude_scaffolds = mtDNA,Y">postprocess_exclude_scaffolds</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>mtDNA,Y</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy postprocess_maf = value" data-copy="postprocess_maf = 0.01">postprocess_maf</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.01</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy postprocess_missingness = value" data-copy="postprocess_missingness = 0.75">postprocess_missingness</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.75</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qc_clusters = value" data-copy="qc_clusters = 3">qc_clusters</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>3</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qc_exclude_scaffolds = value" data-copy="qc_exclude_scaffolds = ">qc_exclude_scaffolds</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qc_google_api_key = value" data-copy="qc_google_api_key = ">qc_google_api_key</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qc_max_sample_missingness = value" data-copy="qc_max_sample_missingness = 0.49">qc_max_sample_missingness</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.49</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qc_min_depth = value" data-copy="qc_min_depth = 2">qc_min_depth</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qc_pca_dims = value" data-copy="qc_pca_dims = 10">qc_pca_dims</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference_name = value" data-copy="reference_name = my_organism">reference_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>my_organism</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>27</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference_source = value" data-copy="reference_source = test/fixtures/ref/genome.fa">reference_source</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/ref/genome.fa</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sample_metadata = value" data-copy="sample_metadata = ">sample_metadata</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy variant_tool = value" data-copy="variant_tool = gatk">variant_tool</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>gatk</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>25</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-snparcher.svg?v=d355d91b08" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-snparcher.svg?v=d355d91b08" alt="oxo-flow-snparcher pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-snparcher — Variant calling for non-model organisms: paired FASTQ reads (or SRA accessions, or external BAMs) are trimmed and filtered with fastp, aligned with BWA-MEM, optionally duplicate-marked with sambamba, and called to per-sample gVCFs with GATK HaplotypeCaller or DeepVariant (low-coverage defaults: -ploidy 2, --min-pruning 1).</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- prepare_reference
- index_reference
- fastp
- download_sra
- fastp_srr
- bwa_mem
- merge_library_bams
- merge_library_level_bams
- markdup_library
- merge_dedup_libraries
- stage_external_bam
- index_bam_csi
- index_bam_csi_markdup
- index_bam_csi_external
- normalize_external_gvcf_for_gatk
- gatk_haplotypecaller
- gatk_haplotypecaller_markdup
- gatk_haplotypecaller_external
- deepvariant_call
- deepvariant_call_markdup
- deepvariant_call_external
- create_db_mapfile
- joint_genomics_db_import
- joint_genotype_gvcfs
- glnexus_joint
- variant_filtration
- collect_fastp_stats
- bam_stats
- bam_stats_markdup
- bam_stats_external
- parse_bam_stats
- combine_qc_metrics
- mosdepth
- mosdepth_markdup
- mosdepth_external
- clam_collect
- callable_coverage_thresholds
- clam_loci
- coverage_bed
- genmap_index
- genmap_mappability
- mappability_bed
- callable_sites_bed
- postprocess_filter_individuals
- postprocess_basic_filter
- postprocess_basic_filter_long
- postprocess_update_bed
- postprocess_strict_filter
- postprocess_strict_filter_long
- postprocess_subset_indels
- postprocess_subset_indels_long
- postprocess_subset_snps
- postprocess_subset_snps_long
- postprocess_drop_indel_snps
- postprocess_drop_indel_snps_long
- qc_contig_map
- qc_vcftools_individuals
- qc_subsample_snps
- qc_prepare_plink_inputs
- qc_copy_qc_report
- qc_plink
- qc_setup_admixture
- qc_admixture
- generate_coords_file
- qc_dashboard
- picard_intervals
- filter_picard_intervals
- create_gvcf_intervals
- gatk_haplotypecaller_interval
- gatk_haplotypecaller_interval_markdup
- gatk_haplotypecaller_interval_external
- concat_interval_gvcfs
- create_db_intervals
- gatk_genomics_db_import_interval
- gatk_genotype_gvcfs_interval
- concat_interval_vcfs
- resolve_long_contig_mode
- gatk_haplotypecaller_interval_long
- gatk_haplotypecaller_interval_markdup_long
- gatk_haplotypecaller_interval_external_long
- concat_interval_gvcfs_long
- create_db_mapfile_long
- gatk_genomics_db_import_interval_long
- gatk_genotype_gvcfs_interval_long
- concat_interval_vcfs_long
- variant_filtration_long
- bcftools_regions
- bcftools_call
- bcftools_concat_regions

**Excluded**

- parabricks — every rule runs with --nv GPU passthrough (workflow/rules/parabricks.smk); the oxo-flow docker backend has no --nv support, plus NVIDIA EULA/license cannot be enforced
- sentieon — proprietary SENTIEON_LICENSE server gating (config/config.yaml sentieon section); cannot be distributed or verified

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- denovo — no such step in upstream v2.2
- structural_variants — no such step in upstream v2.2

## Fidelity

> **Port-side renames of upstream rules** (for upstream claim tracing): `concat_interval_gvcfs_stage` → `concat_interval_gvcfs` / `concat_interval_gvcfs_long`; `concat_interval_vcfs_stage` → `concat_interval_vcfs` / `concat_interval_vcfs_long`; `drop_indel_SNPs` → `postprocess_drop_indel_snps` / `postprocess_drop_indel_snps_long`. The commercial families (see Excluded) cover: `parabricks_haplotypecaller`, `parse_sentieon_stats`, `sentieon_combine_gvcf`, `sentieon_haplotyper` (plus the `sentieon_dedup`/`sentieon_*` gate rules).


74 rules ported from upstream v2.2 (up from 60), covering every branch that
can be expressed in oxo-flow's DAG. Commands are ported verbatim
(same flags, same output paths); upstream's snakemake `{{...}}` shell escaping
is unwrapped to literal braces, and snakemake `{params.*}`/`{resources.*}`
references are resolved to their upstream values or to `{config.*}` keys.
The two runtime-fan-out branches (interval scatter, bcftools caller) are
ported with the engine's `output_pattern` primitive (issue #227 item 5,
merged in oxo-flow 0.17): a producer rule whose outputs are enumerated by a
filesystem scan after it completes, instantiating one downstream consumer per
discovered value. These branches require an engine with `output_pattern`
support; older engines ignore the key and the when-gates keep the default
plan unchanged.

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `prepare_reference` (local branch) | `prepare_reference` | samtools 1.24 (bgzip) | identical command; url/accession branches not ported (config `reference_source` is a local path) |
| `index_reference` | `index_reference` | samtools 1.24, bwa 0.7.19 | identical command (faidx + dict + bwa index) |
| `fastp` | `fastp` / `fastp_srr` | fastp 1.3.6 | identical flags; `{sample}/{sample}/u1` fan-out for single-row sheets with empty `library_id`; SRA-downloaded reads via `fastp_srr` |
| `download_sra` | `download_sra` | sra-tools 3.2.1, ffq, curl, pigz | identical prefetch→fasterq-dump→pigz flow with ffq/ENA fallback; fasterq-dump `--tmpdir` dropped (oxo-flow has no per-rule tmpdir) |
| `bwa_mem` | `bwa_mem` | bwa 0.7.19, samtools 1.24 | identical command incl. read group `ID:{sample}.u1 SM:{sample} LB:{sample} PL:ILLUMINA`; raw BAM is temp like upstream |
| `merge_library_bams` | `merge_library_bams` | samtools 1.24 | per-library merge, single input unit in the default path |
| `merge_library_level_bams` | `merge_library_level_bams` | samtools 1.24 | no-markdup path (`results/bams/merged/{sample}.bam`) |
| `markdup_library` / `merge_dedup_libraries` | `markdup_library` / `merge_dedup_libraries` | sambamba 1.0.1, samtools 1.24 | identical commands; gated on `mark_duplicates` (default `false`; upstream default `true` — see deviations below; per-sample override via the `metadata_file` `mark_duplicates` column) |
| `index_bam_csi` | `index_bam_csi` / `index_bam_csi_markdup` / `index_bam_csi_external` | samtools 1.24 | identical (`samtools index -c`), one per BAM-producing branch |
| `stage_external_bam` | `stage_external_bam` | — | external BAM inputs symlinked into `results/bams/input/` then run through the standard callers |
| `normalize_external_gvcf_for_gatk` / `archive_gatk_gvcf` (gvcf input type) | `normalize_external_gvcf_for_gatk` | bcftools 1.23 | external gVCF inputs recompressed + tabix-indexed to `results/gvcfs/{sample}.g.vcf.gz` (upstream long-contig mode's archive command) and fed straight into joint genotyping; gVCF samples skip calling. Upstream short mode feeds the raw external path to the mapfile; the port normalizes so the uniform `results/gvcfs/{sample}.g.vcf.gz` pattern holds. Upstream refuses gvcf inputs with non-GATK callers; the port accepts them in the GLnexus path (normalized gVCFs are valid GLnexus input) — see deviations |
| `gatk_haplotypecaller` (standard mode) | `gatk_haplotypecaller` / `_markdup` / `_external` | gatk4 4.6.2.0 | identical flags incl. `-ploidy 2 --emit-ref-confidence GVCF --min-pruning 1 --min-dangling-branch-length 1` (low-coverage defaults); `-Xmx7000m` = upstream default profile `mem_mb_reduced`; threads 1 as upstream |
| `picard_intervals` (interval mode) | `picard_intervals` | picard 3.5.0 | identical `ScatterIntervalsByNs` call (`MAX_TO_MERGE=500`, `OUTPUT_TYPE=ACGT` = upstream `ScatterIntervalsByNs` block) |
| `create_gvcf_intervals` (interval mode) | `create_gvcf_intervals` | gatk4 4.6.2.0 | upstream `intervals.smk:59` checkpoint: one `SplitIntervals --scatter-count N --subdivision-mode BALANCING_WITHOUT_INTERVAL_SUBDIVISION` per sample, then the per-interval file list is enumerated by the engine's `output_pattern` scan (see deviations) |
| `gatk_haplotypecaller` (interval mode) | `gatk_haplotypecaller_interval` / `_markdup` / `_external` (short mode) + `_long` twins | gatk4 4.6.2.0 | deferred consumers, instantiated once per discovered interval; same flags as standard mode plus `-L {interval}` from the scattered list; long-contig mode writes plain `.vcf` (no `.gz`, no index) since GATK silently omits the index for `-O *.vcf.gz` on long contigs |
| `concat_interval_gvcfs` | `concat_interval_gvcfs` | bcftools 1.23 | `bcftools concat -D -a` over the per-interval gVCFs + `bcftools sort` + `index -t`, one per sample |
| `create_db_intervals` (interval mode) | `create_db_intervals` | gatk4 4.6.2.0, python | upstream `intervals.smk:89` checkpoint: `DB_SCATTER = db_scatter_factor × samples × num_gvcf_intervals` (computed from `{config.samples_list}`), `SplitIntervals --subdivision-mode INTERVAL_SUBDIVISION`, then `scripts/interval_list_tools.py split-db` re-shards to the per-shard interval/contig caps |
| `gatk_genomics_db_import` (interval mode) | `gatk_genomics_db_import_interval` | gatk4 4.6.2.0 | deferred consumer, one import per db shard (`-L {db_interval}`, mapfile + `--merge-input-intervals` like the cohort rule) |
| `gatk_genotype_gvcfs` (interval mode) | `gatk_genotype_gvcfs_interval` | gatk4 4.6.2.0 | deferred consumer, `gendb://` per-shard GenotypeGVCFs → `results/vcfs/intervals/L{db_interval}.vcf.gz` |
| `concat_interval_vcfs` | `concat_interval_vcfs` / `concat_interval_vcfs_long` | bcftools 1.23 | `bcftools concat -D -a` + sort + index over the per-shard VCFs → `results/vcfs/raw.vcf.gz` (+ `.tbi` short mode, `.csi` long mode) |
| `bcftools_regions` (bcftools caller) | `bcftools_regions` | bcftools 1.23 | upstream `bcftools.smk:13` checkpoint: enumerates reference contigs from the runtime `.fai` into per-contig marker files + `regions.tsv`; the file list is runtime-discovered via `output_pattern` |
| `bcftools_call` (bcftools caller) | `bcftools_call` | bcftools 1.23 | deferred consumer, one mpileup+call per region (`-q/-Q/-d` from config, `-r "$CONTIG"`, `--ploidy`, `-v`); the cohort BAM list is resolved per sample with upstream's markdup → merged → external priority (see deviations) |
| `bcftools_concatenate_vcfs` (bcftools caller) | `bcftools_concat_regions` | bcftools 1.23 | `bcftools concat -D -a` + sort + index over the per-region VCFs → `results/vcfs/raw.vcf.gz` |
| `deepvariant_call` | `deepvariant_call` / `_markdup` / `_external` | google/deepvariant:1.10.0 (docker) | identical `/opt/deepvariant/bin/run_deepvariant` invocation; gated on `variant_tool = "deepvariant"` |
| `create_db_mapfile` | `create_db_mapfile` | python (script) | identical logic, ported as `scripts/write_joint_gvcf_mapfile.py` |
| `joint_genomics_db_import` | `joint_genomics_db_import` | gatk4 | identical GenomicsDBImport flow incl. `TILEDB_DISABLE_FILE_LOCKING` and `--merge-input-intervals` from `scripts/interval_list_tools.py` (merge threshold 50 = upstream `GENOMICSDB_MERGE_CONTIG_THRESHOLD`) |
| `joint_genotype_gvcfs` | `joint_genotype_gvcfs` | gatk4 | identical (tar-extract → `gendb://` GenotypeGVCFs → `results/vcfs/raw.vcf.gz`); temp raw VCF like upstream |
| `glnexus_joint` | `glnexus_joint` | glnexus, bcftools 1.23 | identical DeepVariant-config GLnexus join; `mem_gbytes` = `mem_mb_reduced/1024` rounded to 8, computed from the default profile (see deviations) |
| `variant_filtration` | `variant_filtration` | gatk4, bcftools | identical RPRS/FS_SOR/MQ/QUAL hard filters, `--invalidate-previous-filters true`, then `bcftools index -f -t` |
| long-contig (CSI) indexing — `_resolve_long_contig_mode` (common.smk) + `compress_interval_raw_vcf` (interval mode) + postprocess module `regions_to_index` | `resolve_long_contig_mode` + `*_long` twins (`gatk_haplotypecaller_interval_long`/`_markdup_long`/`_external_long`, `concat_interval_gvcfs_long`, `create_db_mapfile_long`, `gatk_genomics_db_import_interval_long`, `gatk_genotype_gvcfs_interval_long`, `concat_interval_vcfs_long`, `variant_filtration_long`, `postprocess_basic_filter_long`, `postprocess_strict_filter_long`, `postprocess_subset_indels_long`, `postprocess_subset_snps_long`, `postprocess_drop_indel_snps_long`) | bcftools 1.24, gatk4 4.6.2.0 | config `long_contig_mode` ("auto"/true/false) mirrors upstream `TBI_MAX_CONTIG_LENGTH = 2**29 - 1` auto-detection from the `.fai`; long mode emits `.csi` (`bcftools index -c`) and keeps GATK consumers on plain `.vcf` + `.idx`; the postprocess module follows the same twin pattern (`.csi` produced and consumed end-to-end); short mode is byte-identical to a run without the key (see deviations 3, 10, 13, 14) |
| `collect_fastp_stats` | `collect_fastp_stats` | python (script) | identical logic, ported as `scripts/collect_fastp_stats.py` |
| `bam_stats` | `bam_stats` / `_markdup` / `_external` | samtools 1.24 | identical (coverage + flagstat -O tsv); outputs temp like upstream |
| `parse_bam_stats` | `parse_bam_stats` | python (script) | identical logic, ported as `scripts/parse_bam_stats.py` |
| `combine_qc_metrics` | `combine_qc_metrics` | python (script) | identical report format; gather via `expand_inputs` |
| `mosdepth` | `mosdepth` / `_markdup` / `_external` | mosdepth 0.3.3 | identical (`--d4 -t {threads}`), per BAM branch |
| `clam_collect` | `clam_collect` | clam | identical (`clam collect -o depths.zarr`) |
| `callable_coverage_thresholds` | `callable_coverage_thresholds` | python (script) | identical logic, ported verbatim as `scripts/callable_coverage_thresholds.py` |
| `clam_loci` | `clam_loci` | clam | identical incl. per-sample mode and `-m/-M` from the thresholds TSV |
| `coverage_bed` | `coverage_bed` | python, bedtools | identical logic, ported verbatim as `scripts/callable_zarr_to_bed.py` |
| `genmap_index` | `genmap_index` | genmap | identical index-mode switching on decompressed FASTA size (skew ≥ 5 GB, sampled ≥ 2 GB) |
| `genmap_mappability` | `genmap_mappability` | genmap | identical (`-K 150 -E 2 -bg -T`) |
| `mappability_bed` | `mappability_bed` | awk, bedtools | identical score filter + `-d 100` merge |
| `callable_sites_bed` | `callable_sites_bed` | bedtools | identical sort/merge of coverage + mappability BEDs |
| postprocess module (`filter_individuals`, `basic_filter`, `update_bed`, `strict_filter`, `subset_snps`, `subset_indels`, `drop_indel_SNPs`) | `postprocess_filter_individuals` … `postprocess_drop_indel_snps` | bcftools 1.23, awk, bedtools, tabix | identical commands; `scripts/write_include_samples.py` for the sample list; AF upper bound computed as `1 - maf` (upstream `1-{params.maf}`) |
| qc module (`contig_map`, `vcftools_individuals`, `subsample_snps`, `prepare_plink_inputs`, `copy_qc_report`, `plink`, `setup_admixture`, `admixture`, `generate_coords_file`, `qc_dashboard`) | `qc_contig_map` … `qc_dashboard` | vcftools 0.1.16, bcftools 1.23, plink2/plink, admixture, R | identical commands; logic ported to `scripts/contig_map.py`, `vcftools_individuals.py`, `prepare_plink_inputs.py`, `contigs4admixture.py`, `generate_coords.py`, `qc_dashboard_render.R`. `generate_coords_file` reads the optional `sample_metadata` CSV (lat/long) into `results/qc/coords.txt`, consumed by the dashboard's terrain-map panel when `qc_google_api_key` is set; without metadata it writes the empty placeholder (upstream's own else branch) so the panel just prints its placeholder text |
| `setup` / `download_reads` / `map_samples` / `call_variants` / `qc_report` / `callable_sites` / `gvcfs` (Snakefile aggregation targets) | n/a | — | Snakemake target rules, no commands of their own |

### Remaining exclusions

| Item | Why excluded | Evidence |
|---|---|---|
| parabricks (all `parabricks_*` rules) | requires `--nv` GPU passthrough (upstream `parabricks.smk` runs `--nv` images with `nvidia-docker`); the oxo-flow docker backend has no `--nv` support and no GPU device declaration; additionally NVIDIA EULA/license enforcement cannot be guaranteed in CI | `variant_calling/parabricks.smk` (every rule is `--nv`) |
| sentieon (all `sentieon_*` rules) | proprietary tool gated on a `SENTIEON_LICENSE` server and a pre-installed license; cannot be distributed or verified in a community port | `config/config.yaml` `sentieon` section; `workflow/rules/sentieon.smk` |
| `denovo` and `structural_variants` pipeline sections | do not exist as rules in upstream v2.2 | grep of `workflow/` at e0e7a94 finds neither rule set |
| multi-library / multi-unit rows (library_id, input_unit) | `{library}` fan-out via the `library` [[values]] table (`values_from = "config.library_ids"`, default `u1` = the single-library port byte-identical); `--arg library_ids=u1,u2` fans fastp_srr/bwa_mem/markdup per library and the merge chain gathers into the per-sample BAM | multi-library FASTQ cohorts on the fastq branch name per-library sources through the SRR branch or external BAM staging (v1: the fastq branch's raw path is per-sample) |

### Documented deviations from upstream

1. **Default config differs from upstream**: upstream defaults `mark_duplicates: true`, `joint_genotyping: true`, `generate_filtered_vcf: true`, `callable_sites.enabled: true`; the port defaults all of these to `false` so its default plan is byte-identical to the previous 12-rule port. Flip the keys to get upstream's full pipeline.
2. **postprocess/qc modules consume `results/vcfs/raw.vcf.gz`**, not upstream's `FINAL_VCF` (which is the hard-filtered VCF when `generate_filtered_vcf: true` and GATK is used). The modules were run on the raw joint VCF. The difference only matters when combining GATK + `generate_filtered_vcf` + a module, and reproduces upstream behavior for the DeepVariant path.
3. **Postprocess module long-contig CSI mode**: upstream conditionally uses CSI indexes when contigs exceed 512 Mb (`regions_to_index`); the port's postprocess rules follow the calling side's `*_long` twin pattern — `postprocess_basic_filter_long`/`postprocess_strict_filter_long`/`postprocess_subset_indels_long`/`postprocess_subset_snps_long`/`postprocess_drop_indel_snps_long` emit `.csi` (`bcftools index -c`; `tabix -C` for the SNP-positions file) and consume the `.csi`-indexed upstream VCFs of the chain when `long_contig_mode` selects long mode. Short mode is unchanged (`.tbi` everywhere, byte-identical plans).
4. **`glnexus_joint` memory**: upstream computes `mem_gbytes` from the default profile's `mem_mb_reduced`; the port inlines the resulting value 8 (with the same `if < 1 then 1` clamp).
5. **QC-metrics and callable-sites branches with non-fastq input types**: `combine_qc_metrics` and the callable-sites `expand_inputs` reference `results/fastp/{sample}/{sample}/u1.json` / `results/callable_sites/depths/{sample}.*` for every sample, which only exist for fastq/srr (fastp stats) or BAM-bearing samples (depths). For bam/gvcf cohorts the expands fail at plan time. Use fastq/srr groups when combining QC metrics or computing callable sites.
6. **`fasterq-dump --tmpdir` dropped** (no per-rule tmpdir in oxo-flow); SRA downloads use the current directory.
7. **gvcf inputs are accepted on any caller**: upstream hard-fails gvcf inputs with non-GATK callers (bcftools/deepvariant/parabricks); the port normalizes them regardless, so the DeepVariant GLnexus path also accepts them. Normalized gVCFs are valid GLnexus input, so this is a relaxation, not a behavior change.
8. **`coords.txt` is always produced in qc mode**: upstream only creates it when the metadata CSV actually has lat/long rows; the port writes the same file empty otherwise (upstream's own placeholder branch), so the dashboard's map panel shows its placeholder text instead of being absent.
9. **Interval scatter runs one `SplitIntervals` per sample** (gVCF mode): upstream's `create_gvcf_intervals` checkpoint runs once for the whole cohort and downstream per-interval rules address the shared `results/intervals/{sample}/...` per-sample subdirectory; the engine's `output_pattern` gives each producer instance its own scan domain, so the port runs the split per sample (identical inputs → identical interval lists) and the per-interval HaplotypeCallers read `results/intervals/gvcf/{sample}/{interval}-scattered.interval_list`. Functionally equivalent, N × the split work (N = samples); the per-sample scans are independent, so a scatter of 50 × 20 samples costs 20 short GATK calls instead of 1.
10. **No standalone `compress_interval_raw_vcf` step**: upstream re-compresses the per-shard raw VCFs before concatenation; the port's `concat_interval_vcfs` consumes the per-shard VCFs directly (`bcftools concat -D -a` is format-agnostic) and `bcftools sort` normalizes coordinate order. The long-contig (CSI) side of that step IS ported (`concat_interval_vcfs_long` emits `raw.vcf.gz` + `.csi`; `archive_gatk_gvcf` is folded into `concat_interval_gvcfs_long`, which writes the GATK-consumable plain `.vcf` + `.idx` that upstream stages in `results/gvcfs/work/` and never emits a separate durable gz+csi archive — nothing consumes one in the port's interval chain).
11. **`bcftools_call` resolves the per-sample final BAM in the shell** (upstream's `get_final_bam` markdup → merged → external priority) from `{config.samples_list}`, instead of a static input per branch; the declared `results/bams/{merged,markdup,input}/*.bam` glob inputs still order the calls behind every BAM-producing branch via DAG edges. A sample with no final BAM (e.g. gvcf-only cohorts) contributes nothing and the call proceeds with the remaining samples; an empty BAM list exits 0 with a log note (upstream's shell has the same degenerate-cohort behavior).
12. **The interval and bcftools branches need an engine with `output_pattern`** (oxo-flow ≥ 0.17). On older engines the key is ignored and the fresh wildcards (`{interval}`, `{db_interval}`, `{region}`) stay unbound, so `validate`/`lint`/`dry-run` still pass (when-gates keep both branches off by default) but those branches must not be enabled there.
13. **Long-contig mode gates on a side-effect flag file**: `resolve_long_contig_mode` writes a fixed-path flag (`results/reference/.long_contig.flag`) and every `*_long` rule is gated on it (`depends_on = ["resolve_long_contig_mode"]`); the short rules carry the negated gate. Engine gotcha: a `when` containing `wildcard.` is evaluated at PLAN time for DAG morphing, when the flag does not exist yet — a plan-level long rule would be dropped from the plan entirely. Plan-level long rules therefore avoid `wildcard.` in `when`: `concat_interval_gvcfs_long` gates on `{meta.input_type} != 'gvcf'` (baked per instance at expansion time, no `wildcard.` reference), so its `file_exists(...)` gate is evaluated at execution time. Rules instantiated at run time via `output_pattern` (per-interval HC long, db import long, genotype long) are unaffected. The `when` evaluator does not expand `{config.x}` inside `file_exists()`, hence the fixed flag path. Changing the reference or `long_contig_mode` between runs requires a fresh run directory (standard checkpoint semantics).
14. **GATK cannot read `.csi`-indexed VCFs** (verified with GATK 4.6.2.0: VariantFiltration and GenomicsDBImport reject `.csi`, accepting `.tbi`/`.idx`; GATK also silently writes no index for `-O x.vcf.gz` on long contigs). Upstream's long-mode `variant_filtration` feeds `raw.vcf.gz` + `.csi` to GATK and fails; the port's `variant_filtration_long` converts to plain `.vcf` in-shell (`bcftools view -O v`), filters, and re-indexes with `bcftools index -f -c`. GenomicsDBImport reads the plain work gVCFs via GATK `.idx` (created by `gatk IndexFeatureFile` in `concat_interval_gvcfs_long`); GATK reads plain `.vcf` without any index for streaming tools, but db import strictly requires `.idx`. Memory: the port mirrors upstream's default GATK heap (`-Xmx7000m` = upstream profile `mem_mb_reduced: attempt * 7000`). A fully homozygous-reference interval over a contig at the CSI limit can exhaust this heap at gVCF finalization (GATK materializes the whole hom-ref block's depth array for `getMedianDP`; a 600 Mb hom-ref block peaks around 7.2 GB and dies with `OutOfMemoryError` at the default heap — verified live, upstream-inherited since upstream assigns whole contigs to intervals too, `BALANCING_WITHOUT_INTERVAL_SUBDIVISION`). Raise `-Xmx` in the two interval HaplotypeCaller rules (short and long) for such references. The postprocess module is bcftools-only, so its long mode needs no GATK workaround: the `*_long` twins produce and consume `.csi` directly. Two long-chain fixes on top of PR #17: `concat_interval_gvcfs_long` and `concat_interval_vcfs_long` stage bgzip-compressed, indexed copies of the plain per-interval gVCFs / per-shard VCFs in `results/{gvcfs,vcfs}/work/` before concatenating — `bcftools concat` cannot read the plain `.g.vcf`/`.vcf` files the long HaplotypeCaller and GenotypeGVCFs emit (GATK `.idx` convention). One long-chain fix on top of PR #17: `concat_interval_gvcfs_long` stages bgzip-compressed, indexed copies of the plain per-interval gVCFs in `results/gvcfs/work/` before concatenating — `bcftools concat` cannot read the plain `.g.vcf` files the long HaplotypeCaller emits.

Version pinning: upstream envs declare only `>=` ranges with no lockfile;
exact pins (fastp 1.3.6, samtools 1.24, bwa 0.7.19, gatk4 4.6.2.0, bcftools
1.23, sra-tools 3.2.1, mosdepth 0.3.3, vcftools 0.1.16, plink2) were resolved
from bioconda/conda-forge at port time (2026-08-15). Upstream default-profile
thread overrides (fastp 6, bwa_mem 16) are runtime knobs; the port keeps the
rules' own declarations (4 and 8).

## Links

- Repository: [oxo-flow-snparcher](https://github.com/oxo-flow-community/oxo-flow-snparcher)
- Upstream: [harvardinformatics/snparcher](https://github.com/harvardinformatics/snparcher) @ `v2.2`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
