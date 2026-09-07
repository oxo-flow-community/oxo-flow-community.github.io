---
title: "WGS/WES germline and somatic variant calling"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-sarek</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>WGS/WES germline and somatic variant calling</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">wgs</span><span class="ox-tag">wes</span><span class="ox-tag">germline</span><span class="ox-tag">somatic</span><span class="ox-tag">variant-calling</span><span class="ox-tag">gatk</span><span class="ox-tag">bwa</span><span class="ox-tag">bwa-mem2</span><span class="ox-tag">vep</span><span class="ox-tag">umi</span><span class="ox-tag">nf-core</span></div>
<p class="ox-desc">GATK best-practice variant calling for whole-genome and whole-exome sequencing (WGS/WES), germline by default: FastQC quality control, fastp trimming and splitting, BWA-MEM (or BWA-MEM2) alignment, MarkDuplicates with CRAM or BAM output, base quality score recalibration (BQSR), single-sample HaplotypeCaller variant calling with CNN 1D scoring and tranche filtering, VEP annotation, per-sample VCF QC and a final MultiQC report. Optional ported branches (all gated off by default): reference preparation (BWA/BWAmem2 index, .dict, .fai), UMI-aware consensus calling (fgbio chain + fastp), fastp split-parts fan-out (split_parts=true: runtime-discovered per-part BWA-MEM/BWA-MEM2 alignment + BAM merge + index, no input cap), FreeBayes, Strelka2 germline, Manta germline, bcftools mpileup, TIDDIT SV (germline only; somatic mode + SVDB merge excluded), goleft indexcov, DeepVariant, NGSCheckMate sample-identity QC, the joint-germline path (GVCF mode + GenomicsDBImport + GenotypeGVCFs + VQSR), per-caller VCF QC + VEP annotation (upstream fan-out over every enabled caller), and the per-chromosome scatter/gather branch (scatter_gatk=true) that ports upstream interval preparation + GATK4_GATHERBQSRREPORTS / CRAM/BAM_MERGE_INDEX_SAMTOOLS / GATK4_MERGEVCFS with one job per chromosome.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-sarek" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">109</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 24 CPUs / 36 GB per rule (BWA-MEM)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/sarek">nf-core/sarek</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>3.10.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2279.1"><code>10.48546/workflowhub.workflow.2279.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastqc</span><span class="tchip">fastp</span><span class="tchip">bwa</span><span class="tchip">bwa-mem2</span><span class="tchip">samtools</span><span class="tchip">gatk</span><span class="tchip">mosdepth</span><span class="tchip">fgbio</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>oxo-flow-sarek pipeline</strong>: WGS/WES germline variant calling from raw FASTQ to annotated VCFs and a MultiQC report — a community port of nf-core/sarek 3.10.0.</p>
<p><strong>1. Reference preparation</strong> — <code>bwa_index</code> or <code>bwamem2_index</code> builds the aligner index, <code>gatk_createsequencedictionary</code> the sequence dictionary, and <code>samtools_faidx</code> the FASTA index; all config-gated on the prepare_reference flag.</p>
<p><strong>2. Read QC and trimming</strong> — <code>fastqc</code> screens raw reads; <code>fastp</code> trims and splits them (multipart alternative <code>fastp_split</code>). With UMI consensus preprocessing, a fgbio chain runs first: <code>fgbio_fastqtobam</code> → <code>samtools_bam2fq_umi</code> → <code>bwa_mem_umi</code> → <code>fgbio_groupreadsbyumi</code> → <code>fgbio_callmolecularconsensusreads</code> → <code>samtools_bam2fq_consensus</code> → <code>fastp_umi</code>.</p>
<p><strong>3. Alignment (exclusive runtime routes)</strong> — <code>fastp</code>, <code>fastp_split</code>, and <code>fastp_umi</code> feed the BWA-MEM and BWA-MEM2 aligners: <code>bwa_mem</code>/<code>bwa_mem2</code> single-part, or <code>bwa_mem_split</code>/<code>bwa_mem2_split</code> per split part, gathered by <code>bam_merge_index_samtools</code>. The aligned BAM is deduplicated by <code>gatk_markduplicates</code> (CRAM mode) or <code>gatk_markduplicates_bam</code> (BAM mode); the deduplicated file also feeds <code>mosdepth_md</code> and <code>samtools_stats_md</code>.</p>
<p><strong>4. Base quality recalibration</strong> — <code>gatk_baserecalibrator</code> builds the recalibration table and <code>gatk_applybqsr</code> applies it; <code>samtools_index_recal</code> indexes the recalibrated alignment (required upstream of <code>mosdepth_recal</code>), while <code>samtools_stats_recal</code> summarizes it.</p>
<p><strong>5. Variant calling — parallel, config-gated</strong> — all callers share the recalibrated alignment: default <code>gatk_haplotypecaller</code> → <code>gatk_cnnscorevariants</code> → <code>gatk_filtervarianttranches</code>; optional <code>freebayes</code> (→ <code>bcftools_sort_freebayes</code> → <code>tabix_freebayes</code>/<code>vcffilter_freebayes</code> → <code>tabix_freebayes_filt</code>), <code>strelka_germline</code>, <code>manta_germline</code>, <code>bcftools_mpileup_call</code>, <code>tiddit_sv</code> → <code>tabix_tiddit</code>, <code>deepvariant</code>; cohort checks via <code>samtools_reindex_bam</code> → <code>goleft_indexcov</code> and <code>bcftools_mpileup_ngscheckmate</code> → <code>ngscheckmate_ncm</code>. Joint germline instead chains <code>gatk_haplotypecaller_gvcf</code> → <code>gatk_genomicsdbimport</code> → <code>gatk_genotypegvcfs</code> → <code>bcftools_sort_joint</code> → <code>gatk_mergevcfs_joint</code> → <code>gatk_variantrecalibrator_snp</code>/<code>gatk_variantrecalibrator_indel</code> → <code>gatk_applyvqsr_snp</code> → <code>gatk_applyvqsr_indel</code>.</p>
<p><strong>6. QC, annotation, and aggregate reporting</strong> — each produced VCF fans out to per-caller <code>bcftools_stats</code>, <code>vcftools_tstv_count</code>, <code>vcftools_tstv_qual</code>, and <code>vcftools_filter_summary</code> QC plus an <code>ensemblvep_vep</code> annotation (e.g. <code>ensemblvep_vep_freebayes</code>, <code>ensemblvep_vep_joint</code>); with the scatter_gatk option enabled, <code>create_intervals_bed</code> → <code>tabix_interval</code> feed per-chromosome <code>gatk_applybqsr_scatter</code> and <code>gatk_haplotypecaller_scatter</code>, gathered back by <code>merge_index_samtools</code> and <code>gatk_mergevcfs_scatter</code>. Finally <code>multiqc</code> aggregates all reports.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-sarek+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-sarek
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-sarek` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-sarek@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-sarek` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Point the `[config]` fasta / bwa_index / dbsnp / known_indels paths at your GRCh38 bundle and place reads as `raw/<sample>_R1.fastq.gz` / `_R2.fastq.gz`; `oxo-flow dry-run main.oxoflow` previews the plan.

## Installation

**Engine.** oxo-flow >= 0.17.0

**Toolchain.** conda environments (envs/*.yaml) with optional Singularity docker:// image pins

**Requirements.**

- paired-end FASTQ reads at raw/{sample}_R1.fastq.gz / raw/{sample}_R2.fastq.gz
- GRCh38 genome FASTA plus .fai and .dict
- GRCh38 BWA index directory (bwa_index_dir); bwa_mem2_index_dir when aligner = "bwa-mem2"
- GATK bundle known-sites VCFs with .tbi: dbsnp_146.hg38.vcf.gz, Mills_and_1000G_gold_standard.indels.hg38.vcf.gz, Homo_sapiens_assembly38.known_indels.vcf.gz; known_snps + known_snps_tbi for joint VQSR
- VEP cache (GRCh38, homo_sapiens, cache version 112) mounted at /.vep in the container
- NGSCheckMate SNP bed (ngscheckmate_bed) when tools_ngscheckmate = true
- compute: up to 24 CPUs / 36 GB per rule (BWA-MEM 24 threads/30G; VEP 6 threads/36G)
- input cap: ~50M read pairs per sample when split_parts = false (fastp single-part mode); no cap with split_parts = true (runtime-discovered fan-out, requires mapped_bam = "sorted")
- scatter_gatk = true: config.chromosomes must match the fasta .fai contigs
- disk: results/ for per-sample CRAMs/VCFs/reports, plus the reference bundle and VEP cache

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-sarek
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-sarek
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy aligner = value" data-copy="aligner = bwa-mem">aligner</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>bwa-mem</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy alignment_ext = value" data-copy="alignment_ext = cram">alignment_ext</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>cram</code></td>
<td class="ox-p-desc">Alignment-file mode: &#x27;cram&#x27; (default) or &#x27;bam&#x27; (when save_output_as_bam=true).<br>recal_index_ext must match the mode (&#x27;cram.crai&#x27; vs &#x27;bam.bai&#x27;).<br><span class="ox-param-usedby">used by <code>22</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy annotate_vep = value" data-copy="annotate_vep = true">annotate_vep</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwa_index_dir = value" data-copy="bwa_index_dir = /data/references/GRCh38/Sequence/BWAIndex/">bwa_index_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Sequence/BWAIndex/</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwa_mem2_index_dir = value" data-copy="bwa_mem2_index_dir = /data/references/GRCh38/Sequence/BWAmem2Index/">bwa_mem2_index_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Sequence/BWAmem2Index/</code></td>
<td class="ox-p-desc">Optional branches (all default-off; upstream equivalents in parentheses)<br>Reference preparation — upstream PREPARE_GENOME builds the BWA/BWAmem2<br>indexes + .dict + .fai when the reference lacks them; the port gates this on<br>prepare_reference and writes into results/reference/. Point bwa_index_dir /<br>bwa_mem2_index_dir / fasta_fai / dict at the built files to use them.<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_deepvariant = value" data-copy="call_deepvariant = false">call_deepvariant</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_freebayes = value" data-copy="call_freebayes = false">call_freebayes</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Optional callers (upstream --tools list, one boolean per tool)<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_haplotypecaller = value" data-copy="call_haplotypecaller = true">call_haplotypecaller</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>22</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_indexcov = value" data-copy="call_indexcov = false">call_indexcov</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream runs indexcov on WGS only (germline)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_manta = value" data-copy="call_manta = false">call_manta</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Optional callers (upstream --tools list, one boolean per tool)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_mpileup = value" data-copy="call_mpileup = false">call_mpileup</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Optional callers (upstream --tools list, one boolean per tool)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_strelka = value" data-copy="call_strelka = false">call_strelka</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Optional callers (upstream --tools list, one boolean per tool)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_tiddit = value" data-copy="call_tiddit = false">call_tiddit</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Optional callers (upstream --tools list, one boolean per tool)<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy chromosomes = value" data-copy="chromosomes = chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY, chrM">chromosomes</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY, chrM</code></td>
<td class="ox-p-desc">Optional per-chromosome scatter/gather branch (default off). When<br>scatter_gatk = true, BQSR / ApplyBQSR / HaplotypeCaller (and the joint<br>GenotypeGVCFs) run one job per chromosome and the per-chromosome outputs<br>are gathered (GatherBQSRReports / samtools merge+index / MergeVcfs) —<br>results identical to the single whole-genome job (gathers are exact), with<br>per-chromosome parallelism. Upstream scatters over dynamic duration-binned<br>interval files; the engine&#x27;s scatter takes a static value list, so the port<br>uses one interval per chromosome. Keep <code>chromosomes</code> in sync with the<br>contigs of your fasta .fai (each entry must exist in the .fai).<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dbsnp = value" data-copy="dbsnp = /data/references/GRCh38/Annotation/GATKBundle/dbsnp_146.hg38.vcf.gz">dbsnp</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Annotation/GATKBundle/dbsnp_146.hg38.vcf.gz</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>11</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dbsnp_tbi = value" data-copy="dbsnp_tbi = /data/references/GRCh38/Annotation/GATKBundle/dbsnp_146.hg38.vcf.gz.tbi">dbsnp_tbi</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Annotation/GATKBundle/dbsnp_146.hg38.vcf.gz.tbi</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>11</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dict = value" data-copy="dict = /data/references/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.dict">dict</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.dict</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>19</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta = value" data-copy="fasta = /data/references/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.fasta">fasta</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.fasta</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>41</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta_fai = value" data-copy="fasta_fai = /data/references/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.fasta.fai">fasta_fai</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.fasta.fai</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>26</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freebayes_filter = value" data-copy="freebayes_filter = 30">freebayes_filter</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>30</code></td>
<td class="ox-p-desc">upstream params.freebayes_filter<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_pcr_indel_model = value" data-copy="gatk_pcr_indel_model = CONSERVATIVE">gatk_pcr_indel_model</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>CONSERVATIVE</code></td>
<td class="ox-p-desc">gatk tool parameter (upstream --gatk_pcr_indel_model) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genome = value" data-copy="genome = GRCh38">genome</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>GRCh38</code></td>
<td class="ox-p-desc">Reference genome build name (upstream --genome, iGenomes key) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy group_by_umi_strategy = value" data-copy="group_by_umi_strategy = Adjacency">group_by_umi_strategy</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Adjacency</code></td>
<td class="ox-p-desc">upstream params.group_by_umi_strategy<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy joint_germline = value" data-copy="joint_germline = false">joint_germline</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>29</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy joint_interval_name = value" data-copy="joint_interval_name = whole_genome">joint_interval_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>whole_genome</code></td>
<td class="ox-p-desc">Joint germline: the port runs without interval scatter; a single whole-genome<br>interval is built from the fasta .fai (upstream: per-contig BED_PREPARE_INTERVALS)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy known_indels = value" data-copy="known_indels = /data/references/GRCh38/Annotation/GATKBundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz, /data/references/GRCh38/Annotation/GATKBundle/Homo_sapiens_assembly38.known_indels.vcf.gz">known_indels</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Annotation/GATKBundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz, /data/references/GRCh38/Annotation/GATKBundle/Homo_sapiens_assembly38.known_indels.vcf.gz</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy known_indels_tbi = value" data-copy="known_indels_tbi = /data/references/GRCh38/Annotation/GATKBundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz.tbi, /data/references/GRCh38/Annotation/GATKBundle/Homo_sapiens_assembly38.known_indels.vcf.gz.tbi">known_indels_tbi</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Annotation/GATKBundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz.tbi, /data/references/GRCh38/Annotation/GATKBundle/Homo_sapiens_assembly38.known_indels.vcf.gz.tbi</code></td>
<td class="ox-p-desc">Reference data (user-provided; GRCh38 GATK bundle layout from upstream<br>conf/igenomes.config, substituted at port time)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy known_snps = value" data-copy="known_snps = /data/references/GRCh38/Annotation/GATKBundle/1000G_omni2.5.hg38.vcf.gz">known_snps</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Annotation/GATKBundle/1000G_omni2.5.hg38.vcf.gz</code></td>
<td class="ox-p-desc">VQSR resources for joint germline (upstream conf/igenomes.config known_snps)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy known_snps_tbi = value" data-copy="known_snps_tbi = /data/references/GRCh38/Annotation/GATKBundle/1000G_omni2.5.hg38.vcf.gz.tbi">known_snps_tbi</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Annotation/GATKBundle/1000G_omni2.5.hg38.vcf.gz.tbi</code></td>
<td class="ox-p-desc">VQSR resources for joint germline (upstream conf/igenomes.config known_snps)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy lane = value" data-copy="lane = L1">lane</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>L1</code></td>
<td class="ox-p-desc">Sample metadata — mirrors tests/csv/3.0/fastq_single.csv (single-lane model:<br>nf-core/sarek meta.id = &quot;{sample}-{lane}&quot;, read-group ID = &quot;{sample}.{lane}&quot;)<br><span class="ox-param-usedby">used by <code>15</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy length_required = value" data-copy="length_required = 15">length_required</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mapped_bam = value" data-copy="mapped_bam = 0001">mapped_bam</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>0001</code></td>
<td class="ox-p-desc">mapped bam stem fed to markduplicates: {sample}.{mapped_bam}.bam (&quot;sorted&quot; with split_parts = true)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ngscheckmate_bed = value" data-copy="ngscheckmate_bed = /data/references/GRCh38/Annotation/NGSCheckMate/SNP_GRCh38_hg38_wChr.bed">ngscheckmate_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/data/references/GRCh38/Annotation/NGSCheckMate/SNP_GRCh38_hg38_wChr.bed</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">Output directory (upstream --outdir) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>109</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy patient = value" data-copy="patient = test">patient</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test</code></td>
<td class="ox-p-desc">Sample metadata — mirrors tests/csv/3.0/fastq_single.csv (single-lane model:<br>nf-core/sarek meta.id = &quot;{sample}-{lane}&quot;, read-group ID = &quot;{sample}.{lane}&quot;)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy prepare_reference = value" data-copy="prepare_reference = false">prepare_reference</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Optional branches (all default-off; upstream equivalents in parentheses)<br>Reference preparation — upstream PREPARE_GENOME builds the BWA/BWAmem2<br>indexes + .dict + .fai when the reference lacks them; the port gates this on<br>prepare_reference and writes into results/reference/. Point bwa_index_dir /<br>bwa_mem2_index_dir / fasta_fai / dict at the built files to use them.<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy recal_index_ext = value" data-copy="recal_index_ext = cram.crai">recal_index_ext</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>cram.crai</code></td>
<td class="ox-p-desc">Alignment-file mode: &#x27;cram&#x27; (default) or &#x27;bam&#x27; (when save_output_as_bam=true).<br>recal_index_ext must match the mode (&#x27;cram.crai&#x27; vs &#x27;bam.bai&#x27;).<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy save_output_as_bam = value" data-copy="save_output_as_bam = false">save_output_as_bam</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">CRAM output mode (upstream default)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy scatter_gatk = value" data-copy="scatter_gatk = false">scatter_gatk</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Optional per-chromosome scatter/gather branch (default off). When<br>scatter_gatk = true, BQSR / ApplyBQSR / HaplotypeCaller (and the joint<br>GenotypeGVCFs) run one job per chromosome and the per-chromosome outputs<br>are gathered (GatherBQSRReports / samtools merge+index / MergeVcfs) —<br>results identical to the single whole-genome job (gathers are exact), with<br>per-chromosome parallelism. Upstream scatters over dynamic duration-binned<br>interval files; the engine&#x27;s scatter takes a static value list, so the port<br>uses one interval per chromosome. Keep <code>chromosomes</code> in sync with the<br>contigs of your fasta .fai (each entry must exist in the .fai).<br><span class="ox-param-usedby">used by <code>22</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy seq_platform = value" data-copy="seq_platform = ILLUMINA">seq_platform</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>ILLUMINA</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sex = value" data-copy="sex = XX">sex</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>XX</code></td>
<td class="ox-p-desc">Sample metadata — mirrors tests/csv/3.0/fastq_single.csv (single-lane model:<br>nf-core/sarek meta.id = &quot;{sample}-{lane}&quot;, read-group ID = &quot;{sample}.{lane}&quot;)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_bcftools = value" data-copy="skip_bcftools = false">skip_bcftools</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastqc = value" data-copy="skip_fastqc = false">skip_fastqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_mosdepth = value" data-copy="skip_mosdepth = false">skip_mosdepth</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_multiqc = value" data-copy="skip_multiqc = false">skip_multiqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_samtools = value" data-copy="skip_samtools = false">skip_samtools</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_vcftools = value" data-copy="skip_vcftools = false">skip_vcftools</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">tools / skip_tools equivalents (upstream comma-list params expressed as booleans)<br><span class="ox-param-usedby">used by <code>24</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy split_fastq = value" data-copy="split_fastq = 50000000">split_fastq</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>50000000</code></td>
<td class="ox-p-desc">fastp --split_by_lines = split_fastq * 4<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy split_parts = value" data-copy="split_parts = false">split_parts</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Runtime-discovered split parts: when true, fastp&#x27;s --split_by_lines parts<br>are discovered by filesystem scan (engine output_pattern primitive) and the<br>BWA_MEM + BAM_MERGE_INDEX_SAMTOOLS stages fan out per part — no 0001-only<br>cap. Requires mapped_bam = &quot;sorted&quot; (the merge output name). Not supported<br>with umi_read_structure. Off by default (upstream single-part behavior).<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy status = value" data-copy="status = 0">status</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">Sample metadata — mirrors tests/csv/3.0/fastq_single.csv (single-lane model:<br>nf-core/sarek meta.id = &quot;{sample}-{lane}&quot;, read-group ID = &quot;{sample}.{lane}&quot;)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy tools_ngscheckmate = value" data-copy="tools_ngscheckmate = false">tools_ngscheckmate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy trim_fastq = value" data-copy="trim_fastq = false">trim_fastq</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy umi_read_structure = value" data-copy="umi_read_structure = ">umi_read_structure</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">UMI consensus preprocessing (upstream params.umi_read_structure, e.g.<br>&#x27;3M2S+T&#x27; or &#x27;5M2S+T&#x27;; empty string disables the whole UMI chain)<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_cache_ready = value" data-copy="vep_cache_ready = false">vep_cache_ready</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">The VEP cache version must match the VEP binary in envs/vep.yaml<br>(upstream&#x27;s image pins 116; this env ships ensembl-vep 112, whose<br>cache format is version-locked — a 116 cache is unreadable).<br>The cache itself is user data (upstream bundles it in the container<br>at /.vep; ~30GB for whole-genome GRCh38, or a gtf2vep subset) —<br>the VEP rule gates on vep_cache_ready. Upstream fails hard without<br>the cache; set the flag after placing it at vep_dir_cache (see<br>README fidelity table).<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_cache_version = value" data-copy="vep_cache_version = 112">vep_cache_version</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>112</code></td>
<td class="ox-p-desc">The VEP cache version must match the VEP binary in envs/vep.yaml<br>(upstream&#x27;s image pins 116; this env ships ensembl-vep 112, whose<br>cache format is version-locked — a 116 cache is unreadable).<br>The cache itself is user data (upstream bundles it in the container<br>at /.vep; ~30GB for whole-genome GRCh38, or a gtf2vep subset) —<br>the VEP rule gates on vep_cache_ready. Upstream fails hard without<br>the cache; set the flag after placing it at vep_dir_cache (see<br>README fidelity table).<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_dir_cache = value" data-copy="vep_dir_cache = /.vep">vep_dir_cache</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/.vep</code></td>
<td class="ox-p-desc">The VEP cache version must match the VEP binary in envs/vep.yaml<br>(upstream&#x27;s image pins 116; this env ships ensembl-vep 112, whose<br>cache format is version-locked — a 116 cache is unreadable).<br>The cache itself is user data (upstream bundles it in the container<br>at /.vep; ~30GB for whole-genome GRCh38, or a gtf2vep subset) —<br>the VEP rule gates on vep_cache_ready. Upstream fails hard without<br>the cache; set the flag after placing it at vep_dir_cache (see<br>README fidelity table).<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_genome = value" data-copy="vep_genome = GRCh38">vep_genome</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>GRCh38</code></td>
<td class="ox-p-desc">vep tool parameter (upstream --vep_genome) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_species = value" data-copy="vep_species = homo_sapiens">vep_species</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>homo_sapiens</code></td>
<td class="ox-p-desc">vep tool parameter (upstream --vep_species) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy wes = value" data-copy="wes = false">wes</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-sarek-rules.svg?v=b6f09ad42b" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-sarek-rules.svg?v=b6f09ad42b" alt="oxo-flow-sarek rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-sarek.svg?v=c76342b9fa" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-sarek.svg?v=c76342b9fa" alt="oxo-flow-sarek pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-sarek — GATK best-practice variant calling for whole-genome and whole-exome sequencing (WGS/WES), germline by default: FastQC quality control, fastp trimming and splitting, BWA-MEM (or BWA-MEM2) alignment, MarkDuplicates with CRAM or BAM output, base quality score recalibration (BQSR), single-sample HaplotypeCaller variant calling with CNN 1D scoring and tranche filtering, VEP annotation, per-sample VCF QC and a final MultiQC report.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- bam_merge_index_samtools
- bcftools_mpileup_call
- bcftools_mpileup_ngscheckmate
- bcftools_sort_freebayes
- bcftools_sort_joint
- bcftools_sort_joint_scatter
- bcftools_stats
- bcftools_stats_deepvariant
- bcftools_stats_freebayes
- bcftools_stats_joint
- bcftools_stats_manta
- bcftools_stats_mpileup
- bcftools_stats_strelka
- bcftools_stats_tiddit
- bwa_index
- bwa_mem
- bwa_mem2
- bwa_mem2_split
- bwa_mem_split
- bwa_mem_umi
- bwamem2_index
- create_intervals_bed
- deepvariant
- ensemblvep_vep
- ensemblvep_vep_deepvariant
- ensemblvep_vep_freebayes
- ensemblvep_vep_joint
- ensemblvep_vep_manta
- ensemblvep_vep_mpileup
- ensemblvep_vep_strelka
- ensemblvep_vep_tiddit
- fastp
- fastp_split
- fastp_umi
- fastqc
- fgbio_callmolecularconsensusreads
- fgbio_fastqtobam
- fgbio_groupreadsbyumi
- freebayes
- gatk_applybqsr
- gatk_applybqsr_scatter
- gatk_applyvqsr_indel
- gatk_applyvqsr_snp
- gatk_baserecalibrator
- gatk_baserecalibrator_scatter
- gatk_calculatecontamination_paired
- gatk_cnnscorevariants
- gatk_createsequencedictionary
- gatk_filtermutectcalls_paired
- gatk_filtermutectcalls_tumor_only
- gatk_filtervarianttranches
- gatk_gatherbqsrreports
- gatk_genomicsdbimport
- gatk_genomicsdbimport_scatter
- gatk_genotypegvcfs
- gatk_genotypegvcfs_scatter
- gatk_getpileupsummaries_paired
- gatk_haplotypecaller
- gatk_haplotypecaller_gvcf
- gatk_haplotypecaller_gvcf_scatter
- gatk_haplotypecaller_scatter
- gatk_markduplicates
- gatk_markduplicates_bam
- gatk_mergevcfs_joint
- gatk_mergevcfs_joint_scatter
- gatk_mergevcfs_scatter
- gatk_mutect2_paired
- gatk_mutect2_tumor_only
- gatk_variantrecalibrator_indel
- gatk_variantrecalibrator_snp
- goleft_indexcov
- manta_germline
- manta_somatic
- merge_index_samtools
- mosdepth_md
- mosdepth_recal
- multiqc
- ngscheckmate_ncm
- samtools_bam2fq_consensus
- samtools_bam2fq_umi
- samtools_faidx
- samtools_index_recal
- samtools_reindex_bam
- samtools_stats_md
- samtools_stats_recal
- strelka_germline
- strelka_somatic
- tabix_freebayes
- tabix_freebayes_filt
- tabix_interval
- tabix_tiddit
- tiddit_sv
- vcffilter_freebayes
- vcftools_filter_summary
- vcftools_filter_summary_deepvariant
- vcftools_filter_summary_freebayes
- vcftools_filter_summary_joint
- vcftools_filter_summary_manta
- vcftools_filter_summary_mpileup
- vcftools_filter_summary_strelka
- vcftools_filter_summary_tiddit
- vcftools_tstv_count
- vcftools_tstv_count_deepvariant
- vcftools_tstv_count_freebayes
- vcftools_tstv_count_joint
- vcftools_tstv_count_manta
- vcftools_tstv_count_mpileup
- vcftools_tstv_count_strelka
- vcftools_tstv_count_tiddit
- vcftools_tstv_qual
- vcftools_tstv_qual_deepvariant
- vcftools_tstv_qual_freebayes
- vcftools_tstv_qual_joint
- vcftools_tstv_qual_manta
- vcftools_tstv_qual_mpileup
- vcftools_tstv_qual_strelka
- vcftools_tstv_qual_tiddit

**Excluded**

- Sentieon / Parabricks / DRAGMAP — commercial accelerators (licensed binaries), out of scope
- MUSE (upstream subworkflow bam_variant_calling_somatic_muse: MUSE_CALL + MUSE_SUMP) — somatic SNV caller not ported; needs its own env + tumor/normal fixtures
- MSIsensorpro (modules/nf-core/msisensorpro: scan + msisomatic) — MSI caller not ported; needs own env + model data + fixtures
- CNVkit / ASCAT / Control-FREEC / MSIsensor2 / LoFreq / Varlociraptor — the remaining somatic callers that exist in upstream 3.10.0; Mutect2 / Strelka2-somatic / Manta-somatic are ported (call_mutect2 / call_strelka_somatic / call_manta_somatic, pair-fanned via config/somatic_pairs.tsv); the rest need their own envs/fixtures. (SomaticSniper and VarDict are NOT upstream 3.10.0 features — absent from the nextflow_schema.json tools enum and from all wired subworkflows — so they are not listed)
- TIDDIT somatic mode + SVDB merge (subworkflow bam_variant_calling_somatic_tiddit; modules/nf-core/svdb/merge) and FreeBayes / mpileup in somatic & tumor-only mode — not ported; port call_tiddit is germline single-sample (--skip_assembly), call_freebayes/call_mpileup are germline, and the tumor-only path is Mutect2 only
- Annotation beyond VEP: snpEff / SnpSift (modules/nf-core/snpeff + snpsift, upstream prepare_snpsift_databases / vcf_annotate_all) and the upstream merge / bcftools annotate (bcfann) options — not ported; the port annotates every caller VCF with VEP only
- Non-default I/O and prep paths not ported: gatk4spark Spark BQSR/ApplyBQSR/MarkDuplicates (modules/nf-core/gatk4spark; subworkflows bam_applybqsr_spark / bam_baserecalibrator_spark / bam_markduplicates_spark), bbsplit/bbmap genomic-contaminant split (fastq_preprocess_gatk), SPRING compressed FASTQ input (samplesheet_to_channel spring_1/spring_2; nf-core/spring), and untar-based reference download in prepare_genome (UNTAR_BBSPLIT_INDEX / UNTAR_CHR_DIR / UNTAR_MSISENSOR2_MODELS) — the port runs non-Spark GATK4, accepts raw FASTQ.gz, and requires user-provided reference files

## Fidelity

Rows cover every upstream process/rule on the default main execution path plus
every ported optional branch (gated by config flags — all default-off).
"not ported" rows carry a reason + evidence.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command |
| FASTP | `fastp` | fastp 1.1.0 | upstream default trimming/splitting module (TrimGalore does not exist in 3.10.0 — `grep -ri trimgalore` over the upstream tree is empty; the `--trim_fastq_trimgalore` param was dropped in 3.10.0) |
| BWA_MEM | `bwa_mem` | bwa 0.7.17 (envs/bwa-samtools.yaml; the 0.7.19 image is used by the prepare_reference rules) | upstream default aligner is `bwa-mem`, not `bwa-mem2`; read-group flags from sarek.nf; prefix `{meta.id}.{reads[0] token}` = `test.0001` under split_fastq; the same image also carries samtools 1.22.1 (used for `samtools sort`) |
| BWA_MEM2 | `bwa_mem2` | bwa-mem2 2.2.1 | `aligner = "bwa-mem2"` (upstream `params.aligner`); same `-K 100000000 -Y -R` args as BWA_MEM; shares bwa_mem's output path — the two rules are mutually exclusive via `when`, all downstream rules are unchanged; index from `bwa_mem2_index_dir` |
| GATK4_MARKDUPLICATES | `gatk_markduplicates` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | default CRAM branch (`save_output_as_bam=false`) |
| GATK4_MARKDUPLICATES (BAM branch) | `gatk_markduplicates_bam` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | `save_output_as_bam = true`; `--CREATE_INDEX true`, no CRAM conversion; `.md.bai` renamed to `.md.bam.bai` (upstream BAM_MERGE_INDEX_SAMTOOLS); downstream rules read `{config.alignment_ext}` / `{config.recal_index_ext}` (set `"bam"` / `"bam.bai"` together) |
| MOSDEPTH (post-MD) | `mosdepth_md` | mosdepth 0.3.14 (env pin >=0.3.9,<0.4) | ext.prefix `{meta.id}.md`; WGS `--by 500` mode |
| SAMTOOLS_STATS (post-MD) | `samtools_stats_md` | samtools 1.24 | ext.prefix `{meta.id}.md.{alignment_ext}`; 1.24 is the version in the `htslib_samtools` stats/index images (the BWA image carries 1.22.1) |
| GATK4_BASERECALIBRATOR | `gatk_baserecalibrator` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | known-sites = dbsnp + Mills gold standard + known indels (GRCh38); single whole-genome job by default; per-chromosome jobs under `scatter_gatk = true` (see the scatter/gather row) |
| GATK4_APPLYBQSR | `gatk_applybqsr` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | output CRAM per default (BAM in the `save_output_as_bam` branch); single whole-genome job by default; per-chromosome jobs under `scatter_gatk = true` (see the scatter/gather row) |
| SAMTOOLS_INDEX (recal) | `samtools_index_recal` | samtools 1.24 | indexes the recalibrated alignment (`.crai` or `.bam.bai`) |
| MOSDEPTH (recal) | `mosdepth_recal` | mosdepth 0.3.14 (env pin >=0.3.9,<0.4) | ext.prefix `{meta.id}.recal` |
| SAMTOOLS_STATS (recal) | `samtools_stats_recal` | samtools 1.24 | ext.prefix `{meta.id}.recal.{alignment_ext}` |
| GATK4_HAPLOTYPECALLER | `gatk_haplotypecaller` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | default `tools=haplotypecaller,vep` → `call_haplotypecaller=true`; single-sample mode (no `-ERC GVCF`), `--pcr-indel-model CONSERVATIVE`; gated off when `joint_germline = true` (upstream picks the GVCF branch); single whole-genome job by default; per-chromosome jobs under `scatter_gatk = true` (see the scatter/gather row) |
| GATK4_CNNSCOREVARIANTS | `gatk_cnnscorevariants` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | VCF_VARIANT_FILTERING_GATK part 1; CNN 1D scoring (module default `--tensor-type 1D`); upstream keeps the `{sample}.cnn.vcf.gz` intermediate unpublished — the port stores it under `results/variant_calling/cnnscorevariants/` for DAG handoff; skipped in joint mode (upstream: no filtering of the joint VCF) |
| GATK4_FILTERVARIANTTRANCHES | `gatk_filtervarianttranches` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | VCF_VARIANT_FILTERING_GATK part 2; ext.args `--info-key CNN_1D`, ext.prefix `{meta.id}.haplotypecaller`, known sites (dbsnp + 2 GRCh38 indel sets) passed as `--resource`; produces `{sample}.haplotypecaller.filtered.vcf.gz` |
| BCFTOOLS_STATS | `bcftools_stats` | bcftools 1.23.1 | VCF_QC_BCFTOOLS_VCFTOOLS part 1; runs on the filtered VCF (prefix `{meta.id}.haplotypecaller.filtered`) |
| VCFTOOLS_TSTV_COUNT | `vcftools_tstv_count` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 2; runs on the filtered VCF |
| VCFTOOLS_TSTV_QUAL | `vcftools_tstv_qual` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 3; runs on the filtered VCF |
| VCFTOOLS_SUMMARY | `vcftools_filter_summary` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 4; runs on the filtered VCF |
| ENSEMBLVEP_VEP | `ensemblvep_vep` | ensembl-vep 112.0 | annotates the filtered VCF (`{sample}.haplotypecaller.filtered_VEP.ann.vcf.gz`); **gated on `vep_cache_ready`** — upstream fails hard without the cache (bundled at `/.vep` via `--vep_cache`); set the flag after placing a cache at `vep_dir_cache`; `--cache_version 112` (matches the env binary — VEP caches are version-locked), GRCh38 |
| PREPARE_GENOME (BWA_INDEX) | `bwa_index` | bwa 0.7.19 | `prepare_reference = true`; builds `results/reference/bwa/index.{amb,ann,bwt,pac,sa}` — fixed `index` prefix (upstream: fasta basename; irrelevant downstream, the BWA rules find the index by extension). Deviation: upstream does not publish the index unless `save_reference`; the port publishes it because oxo-flow outputs must be tracked |
| PREPARE_GENOME (BWAMEM2_INDEX) | `bwamem2_index` | bwa-mem2 2.2.1 | same gating/prefix note; `results/reference/bwamem2/index.{0123,amb,ann,bwt.2bit.64,pac}` |
| PREPARE_GENOME (GATK4_CREATESEQUENCEDICTIONARY) | `gatk_createsequencedictionary` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes) | `--URI` is the fasta basename as upstream; GATK writes `<fasta-basename>.dict`, the port renames it to `reference.dict` for a fixed output path |
| PREPARE_GENOME (SAMTOOLS_FAIDX) | `samtools_faidx` | samtools 1.24 | indexes a workdir copy of the fasta (the `{config.fasta}` path is treated as read-only); output `results/reference/fai/reference.fasta.fai` |
| SAREK_UMI (FGBIO_FASTQTOBAM → SAMTOOLS_BAM2FQ → BWA_MEM → FGBIO_GROUPREADSBYUMI → FGBIO_CALLMOLECULARCONSENSUSREADS → BAM_CONVERT_SAMTOOLS → FASTP) | `fgbio_fastqtobam`, `samtools_bam2fq_umi`, `bwa_mem_umi`, `fgbio_groupreadsbyumi`, `fgbio_callmolecularconsensusreads`, `samtools_bam2fq_consensus`, `fastp_umi` | fgbio 3.1.2, bwa 0.7.17 (envs/bwa-samtools.yaml), samtools 1.24, fastp 1.1.0 | `umi_read_structure` set (e.g. `"3M2S+T"`); `fastp_umi` shares the fastp output paths so BWA-MEM downstream is untouched; GroupReadsByUmi histogram/metrics go to `reports/umi/`; see deviations for the BAM_CONVERT_SAMTOOLS collapse |
| BAM_VARIANT_CALLING_FREEBAYES (FREEBAYES_GERMLINE, BCFTOOLS_SORT, TABIX_VC, VCFLIB_VCF_FILTER, TABIX_FILT) | `freebayes`, `bcftools_sort_freebayes`, `tabix_freebayes`, `vcffilter_freebayes`, `tabix_freebayes_filt` | freebayes 1.3.10, bcftools 1.23.1, vcflib 1.0.14 | `call_freebayes = true`; `--min-alternate-fraction 0.1 --min-mapping-quality 1`; QUAL filter threshold from `freebayes_filter` (30, upstream `params.freebayes_filter`); all four VCFs/TBI published to `variant_calling/freebayes/{sample}/` as upstream |
| STRELKA_GERMLINE | `strelka_germline` | strelka 2.9.10 | `call_strelka = true`; ext.prefix `{meta.id}.strelka`; email-check disabled via the upstream `sed`; all six outputs (SNP/INDEL/variants × vcf+tbi) published as upstream |
| MANTA_GERMLINE | `manta_germline` | manta 1.6.0 | `call_manta = true`; ext.prefix `{meta.id}.manta`; only the `diploid_sv` pair is published — candidateSmallIndels/candidateSV stay in the workdir exactly as upstream |
| BCFTOOLS_MPILEUP (germline) | `bcftools_mpileup_call` | bcftools 1.23.1 | `call_mpileup = true`; args `--output-type v --multiallelic-caller`, filter `count(GT=="RR")==0`; the module's own bcftools_stats file stays unpublished (as upstream) |
| TIDDIT_SV + TABIX_BGZIP_TIDDIT_SV | `tiddit_sv`, `tabix_tiddit` | tiddit 3.9.5 | `call_tiddit = true`; `--skip_assembly` (upstream passes an empty bwa index channel for germline); `.ploidies.tab` published as upstream |
| BAM_VARIANT_CALLING_INDEXCOV (SAMTOOLS_REINDEX_BAM + GOLEFT_INDEXCOV) | `samtools_reindex_bam`, `goleft_indexcov` | samtools 1.24, goleft 0.2.4 | WGS only (`!wes && call_indexcov`); per-sample header-only reindex with `-F 3844 -q 30` + `--write-index` over `/dev/null##idx##`; cohort run `--fai --directory indexcov` (no `--extranormalize` — inputs are BAMs, matching upstream's reindex path); bed.gz+tbi published to `variant_calling/indexcov/` |
| RUNDEEPVARIANT | `deepvariant` | deepvariant 1.10.0 | `call_deepvariant = true`; `--model_type=WGS --sample_name {sample}`; vcf + g.vcf pairs published to `variant_calling/deepvariant/{sample}/` |
| BAM_NGSCHECKMATE (BCFTOOLS_MPILEUP + NGSCHECKMATE_NCM) | `bcftools_mpileup_ngscheckmate`, `ngscheckmate_ncm` | bcftools 1.23.1, ngscheckmate 1.0.1 | `tools_ngscheckmate = true`; per-sample mpileup `--no-version --ploidy 1 -c` with `-T` SNP bed, reheader to `{sample}-{lane}`; cohort `NCM_REF=./reference.fasta ncm.py -d . -bed <bed> -O . -N ngscheckmate -V`; outputs published to `reports/ngscheckmate/` (live-verify: ncm.py's exact output filenames, see Test) |
| Joint germline (GATK4_HAPLOTYPECALLER GVCF, GATK4_GENOMICSDBIMPORT, GATK4_GENOTYPEGVCFS, BCFTOOLS_SORT, GATK4_MERGEVCFS, GATK4_VARIANTRECALIBRATOR SNP+INDEL, GATK4_APPLYVQSR SNP+INDEL) | `gatk_haplotypecaller_gvcf`, `gatk_genomicsdbimport`, `gatk_genotypegvcfs`, `bcftools_sort_joint`, `gatk_mergevcfs_joint`, `gatk_variantrecalibrator_snp`, `gatk_variantrecalibrator_indel`, `gatk_applyvqsr_snp`, `gatk_applyvqsr_indel` | gatk4 4.5.0.0 (envs/gatk4.yaml; upstream module pin at this tag is 4.6.2.0 for some processes), bcftools 1.23.1 | `joint_germline = true`; VQSR resource labels from `conf/igenomes.config` GRCh38 (1000G omni2.5 SNP → `known_snps`, dbsnp; gatk+mills indels); upstream prefixes `joint_variant_calling_SNP/INDEL` (VQSR intermediates unpublished upstream — the port keeps them under `results/` for DAG handoff); final `joint_germline_recalibrated.vcf.gz`; one whole-genome interval from the fasta `.fai` by default, per-chromosome under `scatter_gatk = true` (see the scatter/gather row) |
| Joint VCF QC + VEP | `bcftools_stats_joint`, `vcftools_tstv_count_joint`, `vcftools_tstv_qual_joint`, `vcftools_filter_summary_joint`, `ensemblvep_vep_joint` | bcftools 1.23.1, vcftools 0.1.17, ensembl-vep 112.0 | upstream runs VCF_QC + VEP on the joint VCF (`vcf_all`); the per-sample QC/VEP rules are gated off in joint mode and these cohort rules take over (prefix `joint_germline_recalibrated`) |
| MULTIQC | `multiqc` | multiqc 1.35 | fan-in over all report producers (depends_on covers the gated branches — skipped rules auto-satisfy); scans the results dir with the upstream `assets/multiqc_config.yml` |
| PREPARE_INTERVALS (BUILD_INTERVALS, CREATE_INTERVALS_BED, TABIX_BGZIPTABIX) + per-interval scatter/gather of BQSR / ApplyBQSR / HaplotypeCaller / joint GenotypeGVCFs (GATK4_GATHERBQSRREPORTS, CRAM/BAM_MERGE_INDEX_SAMTOOLS, GATK4_MERGEVCFS) | `create_intervals_bed`, `tabix_interval`, `gatk_baserecalibrator_scatter`, `gatk_gatherbqsrreports`, `gatk_applybqsr_scatter`, `merge_index_samtools`, `gatk_haplotypecaller_scatter`, `gatk_mergevcfs_scatter`, `gatk_haplotypecaller_gvcf_scatter`, `gatk_genomicsdbimport_scatter`, `gatk_genotypegvcfs_scatter`, `bcftools_sort_joint_scatter`, `gatk_mergevcfs_joint_scatter` | gawk 5.3.0, samtools 1.24, gatk4 4.5.0.0 | `scatter_gatk = true` (default off). Deviation: the engine's scatter fan-out takes a **static** value list, so intervals are one per chromosome (`config.chromosomes` — keep it in sync with the fasta `.fai`) instead of upstream's duration-binned windows (`nucleotides_per_second`); every downstream gather is exact and writes the same paths as the single-job branch, so results are identical — the branch adds per-contig parallelism, it does not change outputs. Live-verified on tx-ubuntu 2026-08-27 (`scatter_gatk=true`, 13 rules + gathers, 0 failed; surfaced + fixed the CRAM 3.0 merge issue — see Test) |
| fastp split parts (multi-part BWA_MEM + BAM_MERGE_INDEX_SAMTOOLS) | `fastp_split`, `bwa_mem_split`, `bwa_mem2_split`, `bam_merge_index_samtools` | fastp 1.1.0, bwa 0.7.17 / bwa-mem2 2.2.1, samtools 1.24 | `split_parts = true` (default off) — fastp's `--split_by_lines` parts are enumerated at runtime via the engine's `output_pattern` primitive (data-dependent part count, exactly like upstream's channel scan) and the per-part BWA_MEM/BWA_MEM2 + BAM_MERGE_INDEX_SAMTOOLS fan-out is reproduced: every part is aligned (`{sample}.NNNN.bam`, upstream prefix `{meta.id}.{token}`) and merged + indexed into `{sample}.sorted.bam` (upstream MERGE_BAM prefix `{meta.id}.sorted`) before MarkDuplicates — no input cap. Requires `mapped_bam = "sorted"`; not supported with `umi_read_structure`. See the deviation note below for the merge gating design. Requires the engine's output_pattern primitive (Traitome/oxo-flow#235) — available on the oxo-flow 0.17 line (metadata engine floor is 0.17.0) |
| Mutect2 (paired + tumor-only, FilterMutectCalls, optional GetPileupSummaries → CalculateContamination) | `call_mutect2` (+ `contamination_estimation`) | off | pair-fanned via `config/somatic_pairs.tsv` (`pair_id, experiment=tumor, control=normal`; empty control = tumor-only). Deviation: Mutect2's optional `--germline-resource` / `--panel-of-normals` inputs are not wired — the port has no config keys for them and contamination is estimated from the pair's pileups instead; to use a PoN, filter the Mutect2 VCF downstream (upstream passes them only when resource files are provided) |
| Strelka2 somatic | `call_strelka_somatic` | off | paired only (upstream `configureStrelkaSomaticWorkflow.py` requires a normal BAM — tumor-only pairs skip it) |
| Manta somatic SV | `call_manta_somatic` | off | paired only (tumor-only SV runs the per-sample germline `manta_germline`); publishes somaticSV.vcf.gz |
| CNVkit, ASCAT, Control-FREEC, MSIsensor2, MSIsensorpro, MUSE, LoFreq, Varlociraptor | — not ported | — | the somatic callers that exist in upstream 3.10.0 (tools enum + `bam_variant_calling_somatic_all`); tumor/normal pairs required; further callers follow the same `[[pairs]]` pattern once their env fixtures exist. **SomaticSniper and VarDict are not upstream 3.10.0 features** (absent from the tools enum and every wired subworkflow) and are therefore not listed |
| Annotation options beyond VEP (snpEff, SnpSift, merge, bcftools annotate `bcfann`) | — not ported | — | upstream `prepare_snpsift_databases` + `vcf_annotate_all`; the port annotates every caller VCF with VEP only |
| TIDDIT somatic + SVDB merge; FreeBayes/mpileup somatic and tumor-only modes | — not ported | — | upstream `bam_variant_calling_somatic_tiddit` (TIDDIT_NORMAL/TIDDIT_TUMOR + `SVDB_MERGE`), `somatic_all`/`tumor_only_all` FreeBayes+mpileup legs; the port's `call_tiddit`/`call_freebayes`/`call_mpileup` are germline single-sample, and the tumor-only path is Mutect2 only |
| gatk4spark / bbsplit / SPRING / untar | — not ported | — | upstream Spark BQSR/ApplyBQSR/MarkDuplicates (`modules/nf-core/gatk4spark` + `*_spark` subworkflows), `bbsplit` contaminant split (`fastq_preprocess_gatk`), SPRING compressed FASTQ input (`samplesheet_to_channel` spring_1/spring_2 + `nf-core/spring`), and untar-based reference download in `prepare_genome` (UNTAR_BBSPLIT_INDEX / UNTAR_CHR_DIR / UNTAR_MSISENSOR2_MODELS); the port runs non-Spark GATK4, accepts raw FASTQ.gz, and requires user-provided reference files (the `assets/multiqc_config.yml` snpeff/bbmap entries are inert MultiQC glob leftovers, not ported rules) |
| Sentieon / Parabricks / DRAGMAP | — not ported | — | commercial accelerators (licensed binaries); out of scope |
| VCF_QC + ENSEMBLVEP_VEP fan-out over the optional callers | `bcftools_stats_{freebayes,strelka,mpileup,deepvariant,manta,tiddit}`, `vcftools_tstv_count_{...}`, `vcftools_tstv_qual_{...}`, `vcftools_filter_summary_{...}`, `ensemblvep_vep_{...}` | bcftools 1.23.1, vcftools 0.1.17, ensembl-vep 112.0 | upstream runs VCF_QC + VEP on every caller VCF (`vcf_all`); the port now mirrors that: when `call_freebayes`/`call_strelka`/`call_mpileup`/`call_deepvariant`/`call_manta`/`call_tiddit` enables a caller, its VCF is QC'd (`reports/bcftools/<caller>/`, `reports/vcftools/<caller>/`) and annotated (`annotation/<caller>/`) with the same prefix conventions as the haplotypecaller rules; tiddit's uncompressed `.vcf` uses `--vcf` instead of `--gzvcf` (as upstream). All 30 rules are gated on their caller's flag (+ `skip_bcftools`/`skip_vcftools`/`annotate_vep`/`vep_cache_ready`) and feed the multiqc `depends_on`. Needs live verification (see Test) |

Deviations (all documented, nothing silently dropped):

- **Two environment tracks.** Each rule declares exactly one environment: a pinned container (`singularity = ...`) or a conda env (`envs/*.yaml`); the fidelity table's Tool (version) column reports the runtime track's version. Conda-track pins that deliberately differ from the upstream module/image pins are documented in the cells (bwa 0.7.17 vs upstream 0.7.19; gatk4 4.5.0.0 vs the 4.6.2.0 pins upstream uses for some processes; mosdepth `>=0.3.9,<0.4` after bioconda pruned the exact 0.3.9 pin).

- **fastp split parts — runtime-discovered fan-out (`split_parts = true`)**: the
  engine has no fan-in/collection over runtime-discovered values (output_pattern
  v1), so the per-sample merge is a plan-time rule whose shell waits for the
  deterministic part count — fastp's parts are 1:1 with the part BAMs and
  `fastp_split`'s final `mv` lands all parts at once — then runs
  BAM_MERGE_INDEX_SAMTOOLS exactly once. A failed per-part alignment fails the
  run (fail-fast cancels the waiting merge), so the wait cannot hang on a
  healthy pipeline. `split_parts` is off by default and the default path is
  unchanged: single part `0001.` -> `{sample}.0001.bam` (the upstream
  `tokenize('.')[0]` behavior), so small/medium inputs never see the new
  machinery. UMI consensus mode (`umi_read_structure`) is not supported with
  `split_parts` — the two gates are mutually exclusive.
- **scatter/gather is opt-in and uses per-chromosome intervals**: the
  upstream per-interval fan-out (duration-binned windows) becomes
  `scatter_gatk = true` in the port — one interval per chromosome (the
  engine's scatter needs a static value list, so `config.chromosomes`
  replaces upstream's `nucleotides_per_second` binning; both split a
  whole-genome interval set, but per-chromosome granularity is coarser).
  Off by default: BQSR, ApplyBQSR, HaplotypeCaller (and joint
  GenotypeGVCFs) run as single whole-genome jobs (one interval from the
  fasta `.fai` for the joint path). Every gather (GatherBQSRReports,
  samtools merge+index, MergeVcfs) writes the same output paths in both
  branches, so the branches are exchangeable without touching downstream
  rules.
- **BAM_CONVERT_SAMTOOLS collapse (UMI path)**: at this upstream commit the
  four `samtools view` calls in `bam_convert_samtools` have no distinguishing
  `-f/-F` flags anywhere in `conf/` (grep-verified), so the view → merge →
  collate → cat machinery emits four identical BAMs and **doubles the reads**
  in the merged output. The port reproduces the functional intent with a
  single `samtools collate -O | samtools fastq` instead.
- **CNN-scored intermediate location**: upstream disables the
  CNNSCOREVARIANTS publishDir (the `{sample}.cnn.vcf.gz` stays in the task
  workdir); oxo-flow hands files between rules through `results/`, so the
  port keeps it under `results/variant_calling/cnnscorevariants/` (same for
  the joint VQSR intermediates, unpublished upstream).
- **reference-prep outputs are published**: upstream leaves built
  BWA/BWAmem2 indexes, `.dict` and `.fai` in the task workdir unless
  `save_reference`; oxo-flow requires tracked outputs, so the port publishes
  them under `results/reference/` — point `bwa_index_dir` /
  `bwa_mem2_index_dir` / `fasta_fai` / `dict` at those paths to use them.
- **single-lane model**: `meta.id` = `{sample}` from BWA-MEM onward
  (upstream: `{sample}-{lane}`); preprocessing stage files keep the upstream
  `{sample}-{lane}` prefix. Read-group IDs are `{sample}.{lane}` as upstream.
- **BWA-MEM alignment args**: upstream `aligner.config` appends `-B 3` for
  tumor samples (`meta.status == 1`, longer insert-size penalty for
  tumor/normal pairs); the port's `bwa_mem` rules always run
  `-K 100000000 -Y` without `-B 3`, for all samples.
- **Docker staging**: only the rule workdir is mounted, so reference files are
  copied into the workdir under fixed local names (`reference.fasta`,
  `reference.fasta.fai`, `reference.dict`) — same effect as Nextflow's
  staging of the reference into the task directory.
- **`known_indels`** is a TOML array (2 GRCh38 files); both it and
  `known_indels_tbi` must be updated together when changing references.

## Links

- Repository: [oxo-flow-sarek](https://github.com/oxo-flow-community/oxo-flow-sarek)
- Upstream: [nf-core/sarek](https://github.com/nf-core/sarek) @ `3.10.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
