---
title: "Ancient DNA (aDNA): QC, mapping, damage estimation and genotyping"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-eager</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Ancient DNA (aDNA): QC, mapping, damage estimation and genotyping</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">ancient-dna</span><span class="ox-tag">adna</span><span class="ox-tag">bam</span><span class="ox-tag">mapping</span><span class="ox-tag">deduplication</span><span class="ox-tag">damage</span><span class="ox-tag">genotyping</span><span class="ox-tag">metagenomic</span><span class="ox-tag">nf-core</span></div>
<p class="ox-desc">Ancient DNA (aDNA) analysis in one run: FastQC raw QC, optional fastp poly-G filtering (2-colour chemistry), AdapterRemoval adapter clipping and paired-end read merging, BWA aln mapping with ancient-DNA parameters, picard MarkDuplicates (or DeDup) deduplication, preseq library-complexity curves, DamageProfiler damage estimation, Qualimap BAM QC, optional pileupCaller genotyping with eigenstrat SNP coverage, optional metagenomic screening of the unmapped reads (bbduk entropy complexity filter, MALT or kraken2 classification with kraken_parse/kraken_merge tables, MaltExtract aDNA evaluation), and a final MultiQC report — every rule pinned to the nf-core/eager 2.5.3 tool versions in the upstream container (MALT 0.61 and HOPs 0.35 ship in the pinned nfcore/eager:2.5.3 image).</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-eager" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">57</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 4 CPUs / 8 GB per rule (bwa_aln)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/eager">nf-core/eager</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>2.5.3</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2288.1"><code>10.48546/workflowhub.workflow.2288.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastqc</span><span class="tchip">adapterremoval</span><span class="tchip">adapterremovalfixprefix</span><span class="tchip">bwa</span><span class="tchip">samtools</span><span class="tchip">picard</span><span class="tchip">dedup</span><span class="tchip">preseq</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-eager</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Ancient-DNA (aDNA) pipeline</strong>: given a reference and raw reads, it clips adapters, maps and deduplicates, estimates damage, runs QC, and optionally genotypes or screens metagenomically — all feeding one MultiQC report.</p>
<p><strong>1. Reference preparation</strong> — <code>make_fasta_index</code>, <code>make_seq_dict</code> and <code>make_bwa_index</code> index the reference (conditional <code>unzip_reference</code> decompresses gzipped input first); branch builders <code>circulargenerator</code>, <code>sexdeterrmine_prep</code> and <code>mask_reference_for_pmdtools</code> draw from the same processed reference.</p>
<p><strong>2. Read QC and cleanup</strong> — <code>fastqc</code> checks raw reads; <code>fastp</code> optionally filters poly-G; <code>adapter_removal</code> clips adapters and merges the ends, feeding <code>fastqc_after_clipping</code> and optional <code>post_ar_fastq_trimming</code>.</p>
<p><strong>3. Mapping and deduplication</strong> — <code>bwa_aln</code> maps the merged reads, <code>samtools_flagstat</code> reports stats, and either <code>markduplicates</code> or alternative <code>dedup</code> removes duplicates. When configured, <code>bwamem</code> (with optional <code>hostremoval_input_fastq</code>), <code>bowtie2</code> (with <code>make_bt2_index</code>) or <code>circularmapper</code> replaces <code>bwa_aln</code>.</p>
<p><strong>4. Ancient-DNA analytics</strong> — the mapped BAM feeds <code>preseq</code>; the deduplicated BAM feeds <code>damageprofiler</code> (with the indexed reference), <code>qualimap</code>, and optional <code>bedtools_coverage</code>, <code>bam_trim</code>, <code>picard_addorreplacereadgroups</code>, <code>mapdamage_calculation</code>, <code>mapdamage_rescaling</code>, <code>pmdtools</code>, <code>mtnucratio</code>, <code>sexdeterrmine</code>, <code>nuclear_contamination</code> → <code>print_nuclear_contamination</code>; <code>endor_spy</code> follows the flagstat stats.</p>
<p><strong>5. Optional genotyping</strong> — <code>genotyping_pileupcaller</code> → <code>eigenstrat_snp_coverage</code>; alternatively <code>genotyping_ug</code>, <code>genotyping_hc</code>, <code>genotyping_freebayes</code> or <code>genotyping_angsd</code>, with <code>vcf2genome</code> and <code>multivcfanalyzer</code> consuming the UnifiedGenotyper VCFs.</p>
<p><strong>6. Optional metagenomics</strong> — the four mapper filters (<code>samtools_filter_bwaaln</code>, <code>samtools_filter_bwamem</code>, <code>samtools_filter_bowtie2</code>, <code>samtools_filter_circularmapper</code>) feed <code>samtools_flagstat_after_filter</code>, and unmapped reads flow through <code>metagenomic_complexity_filter</code> into either <code>kraken</code> → <code>kraken_parse</code> → <code>kraken_merge</code> or <code>malt</code> → <code>maltextract</code>.</p>
<p><strong>7. Reporting</strong> — <code>multiqc</code> aggregates every route into one report.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-eager+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-eager
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-eager` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-eager@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-eager` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Needs reference genome and reads — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.12.0 (the gated multi-lane mode — run_lanemerge=true — additionally requires oxo-flow >= 0.16.0 with input_groups support, Traitome/oxo-flow#231; on older engines the gate is inert and the default single-pair path is unchanged)

**Toolchain.** containers (Docker/Singularity) — pinned image nfcore/eager:2.5.3 for all rules (bundles the pinned conda env from envs/eager.yaml)

**Requirements.**

- reference genome FASTA, plain and uncompressed (.gz references are not supported — upstream's unzip_reference step is not ported); the workflow builds the .fai / .dict / BWA indices itself
- paired-end FASTQ pairs named <sample>_R1.fastq.gz / <sample>_R2.fastq.gz in a directory (directory input mode; sample = text before the _R1/_R2 suffix); single-end is not supported
- optional — multi-lane input: name the pairs <sample>_L<lane>_R1.fastq.gz / _R2.fastq.gz (lane-tagged, as in upstream's TSV mode) and set run_lanemerge=true: the lanemerge rules concatenate the per-lane pairs of each sample into one merged pair (results/lanemerging/) that feeds AdapterRemoval and hostremoval_input_fastq; samples without lane-tagged files keep using the default-named pair. Requires oxo-flow >= 0.16.0 (input_groups, Traitome/oxo-flow#231)
- optional — pileupCaller genotyping (run_genotyping=true genotyping_tool='pileupcaller') requires pileupcaller_snpfile and pileupcaller_bedfile; the rule fails fast without them
- optional — metagenomic screening (run_metagenomic_screening=true, bam_unmapped_type='fastq') requires metagenomic_tool='kraken' with a kraken2_db (kraken2 database directory or .tar.gz bundle, unpacked by the kraken rule) or metagenomic_tool='malt' with a malt_db (MALT database directory); maltextract additionally requires maltextract_taxon_list and maltextract_ncbifiles. The chain is validate/dry-run-tested but not yet live-verified
- compute: up to 4 CPUs / 8 GB RAM per rule (bwa_aln: 4 threads / 8G; kraken: 4 threads / 8G — upstream's mc_huge label is 32 cpus / 256 GB, tune via CLI overrides; reference-index and MultiQC rules up to 8 GB; base default 1 CPU / 7 GB / 24 h)
- Docker or Singularity to run the pinned container nfcore/eager:2.5.3 (not needed for validate / lint / dry-run)
- disk: results/ holds reference indices, mapped BAMs and reports — size grows with the reference genome and number of samples

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-eager
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-eager
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy angsd_fasta_arg = value" data-copy="angsd_fasta_arg = ">angsd_fasta_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy angsd_glformat = value" data-copy="angsd_glformat = 4">angsd_glformat</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>4</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy angsd_glmodel = value" data-copy="angsd_glmodel = 1">angsd_glmodel</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy angsd_majorminor_arg = value" data-copy="angsd_majorminor_arg = ">angsd_majorminor_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy anno_file = value" data-copy="anno_file = ">anno_file</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy anno_file_is_unsorted_neg = value" data-copy="anno_file_is_unsorted_neg = -sorted">anno_file_is_unsorted_neg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>-sorted</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bam_input = value" data-copy="bam_input = false">bam_input</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bam_mapping_quality_threshold = value" data-copy="bam_mapping_quality_threshold = 0">bam_mapping_quality_threshold</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bam_unmapped_type = value" data-copy="bam_unmapped_type = discard">bam_unmapped_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>discard</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bamutils_clip_double_stranded_none_udg_left = value" data-copy="bamutils_clip_double_stranded_none_udg_left = 1">bamutils_clip_double_stranded_none_udg_left</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bamutils_clip_double_stranded_none_udg_right = value" data-copy="bamutils_clip_double_stranded_none_udg_right = 1">bamutils_clip_double_stranded_none_udg_right</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bamutils_softclip_arg = value" data-copy="bamutils_softclip_arg = ">bamutils_softclip_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bcftools_stats_source = value" data-copy="bcftools_stats_source = haplotypecaller">bcftools_stats_source</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>haplotypecaller</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bt2_preset = value" data-copy="bt2_preset = ">bt2_preset</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwaalnk = value" data-copy="bwaalnk = 2">bwaalnk</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">mapping<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwaalnl = value" data-copy="bwaalnl = 1024">bwaalnl</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1024</code></td>
<td class="ox-p-desc">mapping<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwaalnn = value" data-copy="bwaalnn = 0.01">bwaalnn</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.01</code></td>
<td class="ox-p-desc">mapping<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwaalno = value" data-copy="bwaalno = 2">bwaalno</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">mapping<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy circularextension = value" data-copy="circularextension = 100">circularextension</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy circularfilter_arg = value" data-copy="circularfilter_arg = ">circularfilter_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy circulartarget = value" data-copy="circulartarget = chrMT">circulartarget</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>chrMT</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clip_forward_adaptor = value" data-copy="clip_forward_adaptor = AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC">clip_forward_adaptor</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clip_min_read_quality = value" data-copy="clip_min_read_quality = 20">clip_min_read_quality</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>20</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clip_readlength = value" data-copy="clip_readlength = 30">clip_readlength</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>30</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clip_reverse_adaptor = value" data-copy="clip_reverse_adaptor = AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA">clip_reverse_adaptor</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy colour_chemistry = value" data-copy="colour_chemistry = 4">colour_chemistry</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>4</code></td>
<td class="ox-p-desc">input / library metadata (directory-input mode defaults)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy complexity_filter_poly_g = value" data-copy="complexity_filter_poly_g = false">complexity_filter_poly_g</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">complexity (poly-G) filter<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy complexity_filter_poly_g_min = value" data-copy="complexity_filter_poly_g_min = 10">complexity_filter_poly_g_min</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10</code></td>
<td class="ox-p-desc">complexity (poly-G) filter<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy damage_calculation_tool = value" data-copy="damage_calculation_tool = damageprofiler">damage_calculation_tool</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>damageprofiler</code></td>
<td class="ox-p-desc">damage estimation<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy damageprofiler_length = value" data-copy="damageprofiler_length = 100">damageprofiler_length</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">damage estimation<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy damageprofiler_threshold = value" data-copy="damageprofiler_threshold = 15">damageprofiler_threshold</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">damage estimation<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy damageprofiler_yaxis = value" data-copy="damageprofiler_yaxis = 0.30">damageprofiler_yaxis</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>0.30</code></td>
<td class="ox-p-desc">damage estimation<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dedup_all_merged = value" data-copy="dedup_all_merged = false">dedup_all_merged</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">deduplication<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dedupper = value" data-copy="dedupper = markduplicates">dedupper</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>markduplicates</code></td>
<td class="ox-p-desc">deduplication<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta = value" data-copy="fasta = test/fixtures/reference/genome.fa">fasta</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reference/genome.fa</code></td>
<td class="ox-p-desc">input / library metadata (directory-input mode defaults)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freebayes_C = value" data-copy="freebayes_C = 2">freebayes_C</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freebayes_g_arg = value" data-copy="freebayes_g_arg = ">freebayes_g_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freebayes_p = value" data-copy="freebayes_p = 1">freebayes_p</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_call_conf = value" data-copy="gatk_call_conf = 30">gatk_call_conf</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>30</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_downsample = value" data-copy="gatk_downsample = 250">gatk_downsample</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>250</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_hc_emitrefconf = value" data-copy="gatk_hc_emitrefconf = NONE">gatk_hc_emitrefconf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NONE</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_hc_out_mode = value" data-copy="gatk_hc_out_mode = EMIT_VARIANTS_ONLY">gatk_hc_out_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>EMIT_VARIANTS_ONLY</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_ploidy = value" data-copy="gatk_ploidy = 2">gatk_ploidy</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_ug_defaultbasequalities_arg = value" data-copy="gatk_ug_defaultbasequalities_arg = ">gatk_ug_defaultbasequalities_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_ug_genotype_model = value" data-copy="gatk_ug_genotype_model = SNP">gatk_ug_genotype_model</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>SNP</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gatk_ug_out_mode = value" data-copy="gatk_ug_out_mode = EMIT_VARIANTS_ONLY">gatk_ug_out_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>EMIT_VARIANTS_ONLY</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genotyping_source = value" data-copy="genotyping_source = raw">genotyping_source</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>raw</code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genotyping_tool = value" data-copy="genotyping_tool = ">genotyping_tool</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy hostremoval_input_fastq = value" data-copy="hostremoval_input_fastq = false">hostremoval_input_fastq</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy hostremoval_mode = value" data-copy="hostremoval_mode = mapped">hostremoval_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>mapped</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy input_bam = value" data-copy="input_bam = ">input_bam</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kraken2_db = value" data-copy="kraken2_db = ">kraken2_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy lane = value" data-copy="lane = 0">lane</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">input / library metadata (directory-input mode defaults)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy large_ref = value" data-copy="large_ref = false">large_ref</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">mapping<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_alignment_mode = value" data-copy="malt_alignment_mode = SemiGlobal">malt_alignment_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>SemiGlobal</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_db = value" data-copy="malt_db = ">malt_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_max_queries = value" data-copy="malt_max_queries = 100">malt_max_queries</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_memory_mode = value" data-copy="malt_memory_mode = load">malt_memory_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>load</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_min_support_mode = value" data-copy="malt_min_support_mode = percent">malt_min_support_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>percent</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_min_support_percent = value" data-copy="malt_min_support_percent = 0.01">malt_min_support_percent</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.01</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_mode = value" data-copy="malt_mode = BlastN">malt_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>BlastN</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_sam_output = value" data-copy="malt_sam_output = false">malt_sam_output</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy malt_top_percent = value" data-copy="malt_top_percent = 1">malt_top_percent</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_destackingoff = value" data-copy="maltextract_destackingoff = false">maltextract_destackingoff</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_downsamplingoff = value" data-copy="maltextract_downsamplingoff = false">maltextract_downsamplingoff</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_duplicateremovaloff = value" data-copy="maltextract_duplicateremovaloff = false">maltextract_duplicateremovaloff</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_filter = value" data-copy="maltextract_filter = def_anc">maltextract_filter</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>def_anc</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_matches = value" data-copy="maltextract_matches = false">maltextract_matches</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_megansummary = value" data-copy="maltextract_megansummary = false">maltextract_megansummary</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_ncbifiles = value" data-copy="maltextract_ncbifiles = ">maltextract_ncbifiles</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_percentidentity = value" data-copy="maltextract_percentidentity = 85.0">maltextract_percentidentity</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>85.0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_taxon_list = value" data-copy="maltextract_taxon_list = ">maltextract_taxon_list</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_topalignment = value" data-copy="maltextract_topalignment = false">maltextract_topalignment</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maltextract_toppercent = value" data-copy="maltextract_toppercent = 0.01">maltextract_toppercent</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.01</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mapdamage_downsample_arg = value" data-copy="mapdamage_downsample_arg = ">mapdamage_downsample_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mapdamage_singlestranded_arg = value" data-copy="mapdamage_singlestranded_arg = ">mapdamage_singlestranded_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mapdamage_yaxis = value" data-copy="mapdamage_yaxis = 0.25">mapdamage_yaxis</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.25</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mapper = value" data-copy="mapper = bwaaln">mapper</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>bwaaln</code></td>
<td class="ox-p-desc">mapping<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mergedonly = value" data-copy="mergedonly = false">mergedonly</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy metagenomic_complexity_entropy = value" data-copy="metagenomic_complexity_entropy = 0.3">metagenomic_complexity_entropy</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.3</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy metagenomic_complexity_filter = value" data-copy="metagenomic_complexity_filter = false">metagenomic_complexity_filter</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy metagenomic_min_support_reads = value" data-copy="metagenomic_min_support_reads = 1">metagenomic_min_support_reads</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy metagenomic_tool = value" data-copy="metagenomic_tool = ">metagenomic_tool</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_adap_overlap = value" data-copy="min_adap_overlap = 1">min_adap_overlap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_allele_freq_het = value" data-copy="min_allele_freq_het = 0.2">min_allele_freq_het</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.2</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_allele_freq_hom = value" data-copy="min_allele_freq_hom = 0.8">min_allele_freq_hom</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.8</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_base_coverage = value" data-copy="min_base_coverage = 0">min_base_coverage</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_genotype_quality = value" data-copy="min_genotype_quality = 0">min_genotype_quality</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mtnucratio_header = value" data-copy="mtnucratio_header = MT">mtnucratio_header</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>MT</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy multivcf_samples = value" data-copy="multivcf_samples = S1, S2">multivcf_samples</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>S1, S2</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nuclear_contamination_header = value" data-copy="nuclear_contamination_header = ">nuclear_contamination_header</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">input / library metadata (directory-input mode defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy percent_identity = value" data-copy="percent_identity = 85">percent_identity</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>85</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pileupcaller_bedfile = value" data-copy="pileupcaller_bedfile = ">pileupcaller_bedfile</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pileupcaller_method = value" data-copy="pileupcaller_method = randomHaploid">pileupcaller_method</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>randomHaploid</code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pileupcaller_min_base_quality = value" data-copy="pileupcaller_min_base_quality = 30">pileupcaller_min_base_quality</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>30</code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pileupcaller_min_map_quality = value" data-copy="pileupcaller_min_map_quality = 30">pileupcaller_min_map_quality</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>30</code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pileupcaller_snpfile = value" data-copy="pileupcaller_snpfile = ">pileupcaller_snpfile</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pileupcaller_transitions_mode = value" data-copy="pileupcaller_transitions_mode = AllSites">pileupcaller_transitions_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>AllSites</code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pmdtools_mask_bed = value" data-copy="pmdtools_mask_bed = ">pmdtools_mask_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pmdtools_max_reads = value" data-copy="pmdtools_max_reads = 1000000">pmdtools_max_reads</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000000</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pmdtools_platypus_arg = value" data-copy="pmdtools_platypus_arg = ">pmdtools_platypus_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pmdtools_range = value" data-copy="pmdtools_range = 10">pmdtools_range</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pmdtools_reference_mask = value" data-copy="pmdtools_reference_mask = false">pmdtools_reference_mask</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pmdtools_threshold = value" data-copy="pmdtools_threshold = 3">pmdtools_threshold</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>3</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pmdtools_treatment_arg = value" data-copy="pmdtools_treatment_arg = --UDGminus">pmdtools_treatment_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>--UDGminus</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy post_ar_trim_front = value" data-copy="post_ar_trim_front = 0">post_ar_trim_front</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy post_ar_trim_front2 = value" data-copy="post_ar_trim_front2 = 0">post_ar_trim_front2</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy post_ar_trim_tail = value" data-copy="post_ar_trim_tail = 0">post_ar_trim_tail</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy post_ar_trim_tail2 = value" data-copy="post_ar_trim_tail2 = 0">post_ar_trim_tail2</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy preseq_bootstrap = value" data-copy="preseq_bootstrap = 100">preseq_bootstrap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">preseq<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy preseq_cval = value" data-copy="preseq_cval = 0.95">preseq_cval</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.95</code></td>
<td class="ox-p-desc">preseq<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy preseq_maxextrap = value" data-copy="preseq_maxextrap = 10000000000">preseq_maxextrap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10000000000</code></td>
<td class="ox-p-desc">preseq<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy preseq_mode = value" data-copy="preseq_mode = c_curve">preseq_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>c_curve</code></td>
<td class="ox-p-desc">preseq<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy preseq_step_size = value" data-copy="preseq_step_size = 1000">preseq_step_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000</code></td>
<td class="ox-p-desc">preseq<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy preseq_terms = value" data-copy="preseq_terms = 100">preseq_terms</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">preseq<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy preserve5p = value" data-copy="preserve5p = false">preserve5p</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qualitymax = value" data-copy="qualitymax = 41">qualitymax</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>41</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference_gff_annotations = value" data-copy="reference_gff_annotations = ">reference_gff_annotations</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference_gff_exclude = value" data-copy="reference_gff_exclude = ">reference_gff_exclude</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rescale_length_3p_arg = value" data-copy="rescale_length_3p_arg = ">rescale_length_3p_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rescale_length_5p_arg = value" data-copy="rescale_length_5p_arg = ">rescale_length_5p_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rescale_seqlength = value" data-copy="rescale_seqlength = 12">rescale_seqlength</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>12</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_bam_filtering = value" data-copy="run_bam_filtering = false">run_bam_filtering</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_bcftools_stats = value" data-copy="run_bcftools_stats = false">run_bcftools_stats</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_bedtools_coverage = value" data-copy="run_bedtools_coverage = false">run_bedtools_coverage</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_endor_spy = value" data-copy="run_endor_spy = false">run_endor_spy</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_genotyping = value" data-copy="run_genotyping = false">run_genotyping</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">genotyping (pileupCaller branch)<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_maltextract = value" data-copy="run_maltextract = false">run_maltextract</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_mapdamage_rescaling = value" data-copy="run_mapdamage_rescaling = false">run_mapdamage_rescaling</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_metagenomic_screening = value" data-copy="run_metagenomic_screening = false">run_metagenomic_screening</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_mtnucratio = value" data-copy="run_mtnucratio = false">run_mtnucratio</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_multivcfanalyzer = value" data-copy="run_multivcfanalyzer = false">run_multivcfanalyzer</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_nuclear_contamination = value" data-copy="run_nuclear_contamination = false">run_nuclear_contamination</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_pmdtools = value" data-copy="run_pmdtools = false">run_pmdtools</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_post_ar_trimming = value" data-copy="run_post_ar_trimming = false">run_post_ar_trimming</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_sexdeterrmine = value" data-copy="run_sexdeterrmine = false">run_sexdeterrmine</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_trim_bam = value" data-copy="run_trim_bam = false">run_trim_bam</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_vcf2genome = value" data-copy="run_vcf2genome = false">run_vcf2genome</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy save_reference = value" data-copy="save_reference = false">save_reference</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">mapping<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy seqtype = value" data-copy="seqtype = PE">seqtype</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>PE</code></td>
<td class="ox-p-desc">input / library metadata (directory-input mode defaults)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sexdeterrmine_prep_s = value" data-copy="sexdeterrmine_prep_s = 1000000">sexdeterrmine_prep_s</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000000</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sexdeterrmine_s = value" data-copy="sexdeterrmine_s = 1000000">sexdeterrmine_s</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000000</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy single_end = value" data-copy="single_end = false">single_end</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">input / library metadata (directory-input mode defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy single_stranded = value" data-copy="single_stranded = false">single_stranded</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_adapterremoval = value" data-copy="skip_adapterremoval = false">skip_adapterremoval</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skipping (upstream defaults: run everything except optional branches)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_collapse = value" data-copy="skip_collapse = false">skip_collapse</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_damage_calculation = value" data-copy="skip_damage_calculation = false">skip_damage_calculation</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skipping (upstream defaults: run everything except optional branches)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_deduplication = value" data-copy="skip_deduplication = false">skip_deduplication</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skipping (upstream defaults: run everything except optional branches)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastqc = value" data-copy="skip_fastqc = false">skip_fastqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skipping (upstream defaults: run everything except optional branches)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_preseq = value" data-copy="skip_preseq = false">skip_preseq</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skipping (upstream defaults: run everything except optional branches)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_qualimap = value" data-copy="skip_qualimap = false">skip_qualimap</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skipping (upstream defaults: run everything except optional branches)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_trim = value" data-copy="skip_trim = false">skip_trim</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">read clipping / merging<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy snp_eff_results = value" data-copy="snp_eff_results = ">snp_eff_results</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy udg_type = value" data-copy="udg_type = none">udg_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>none</code></td>
<td class="ox-p-desc">input / library metadata (directory-input mode defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy unzip_reference = value" data-copy="unzip_reference = false">unzip_reference</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vcf2genome_minc = value" data-copy="vcf2genome_minc = 5">vcf2genome_minc</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vcf2genome_minfreq = value" data-copy="vcf2genome_minfreq = 0.5">vcf2genome_minfreq</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.5</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vcf2genome_minq = value" data-copy="vcf2genome_minq = 30">vcf2genome_minq</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>30</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy write_allele_frequencies_arg = value" data-copy="write_allele_frequencies_arg = F">write_allele_frequencies_arg</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>F</code></td>
<td class="ox-p-desc">see rules/branches.oxoflow for the ported rules + the structural<br>exclusions (lane/library merging, nf-core boilerplate).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-eager.svg?v=744e157379" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-eager.svg?v=744e157379" alt="oxo-flow-eager pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-eager — Ancient DNA (aDNA) analysis in one run: FastQC raw QC, optional fastp poly-G filtering (2-colour chemistry), AdapterRemoval adapter clipping and paired-end read merging, BWA aln mapping with ancient-DNA parameters, picard MarkDuplicates (or DeDup) deduplication, preseq library-complexity curves, DamageProfiler damage estimation, Qualimap BAM QC, optional pileupCaller genotyping with eigenstrat SNP coverage, optional metagenomic screening of the unmapped reads (bbduk entropy complexity filter, MALT or kraken2 classification with kraken_parse/kraken_merge tables, MaltExtract aDNA evaluation), and a final MultiQC report — every rule pinned to the nf-core/eager 2.5.3 tool versions in the upstream container (MALT 0.61 and HOPs 0.35 ship in the pinned nfcore/eager:2.5.3 image).</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- adapter_removal
- bam_trim
- bcftools_stats
- bedtools_coverage
- bowtie2
- bwa_aln
- bwamem
- circulargenerator
- circularmapper
- convert_bam
- damageprofiler
- dedup
- eigenstrat_snp_coverage
- endor_spy
- fastp
- fastqc
- fastqc_after_clipping
- fastqc_lanemerged
- genotyping_angsd
- genotyping_freebayes
- genotyping_hc
- genotyping_pileupcaller
- genotyping_ug
- hostremoval_input_fastq
- hostremoval_input_fastq_bwamem
- kraken
- kraken_merge
- kraken_parse
- lanemerge
- lanemerge_r2
- make_bt2_index
- make_bwa_index
- make_fasta_index
- make_seq_dict
- malt
- maltextract
- mapdamage_calculation
- mapdamage_rescaling
- markduplicates
- mask_reference_for_pmdtools
- metagenomic_complexity_filter
- mtnucratio
- multiqc
- multivcfanalyzer
- nuclear_contamination
- picard_addorreplacereadgroups
- pmdtools
- post_ar_fastq_trimming
- preseq
- print_nuclear_contamination
- qualimap
- samtools_filter_bowtie2
- samtools_filter_bwaaln
- samtools_filter_bwamem
- samtools_filter_circularmapper
- samtools_flagstat
- samtools_flagstat_after_filter
- sexdeterrmine
- sexdeterrmine_prep
- unzip_reference
- vcf2genome

**Excluded**

- library_merge / additional_library_merge: structural — upstream merges the per-LIBRARY BAMs of a sample (samtools merge of the per-library dedup / bam_trim BAMs, main.nf 1967 / 2320). The port's directory-input model has ONE library per sample (library = sample, lane = 0) and one BAM per sample at every stage, so there are no multi-library BAMs to merge; declaring each library as its own sample (or pre-merging) remains the workaround. lanemerge-style input_groups cannot express this either: it groups FILES of a pattern, and the port has no per-library file dimension
- seqtype_merge: structural — upstream merges the per-seqtype mapped BAMs of mixed PE/SE libraries into one BAM per library (samtools merge, main.nf 1597); the port is pure-PE (directory input, sample = text before _R1/_R2) with one mapped BAM per sample, so there are no mixed-PE/SE BAMs to merge. Convert SE samples to PE or run SE-only samples separately
- convertBam (ported as `convert_bam` but a documented dead end: with `bam_input=true` the rule extracts FASTQ while downstream still runs on the fixture FASTQs — upstream wires convertBam into the preprocessing channels; wiring it needs optional-input semantics, Traitome/oxo-flow#200; see the README fidelity row)
- indexinputbam — upstream indexes the input BAM for BAM pass-through mode (`bam != 'NA' && !run_convertinputbam`, main.nf 657); not ported (the port's BAM-input mode routes through `convert_bam`/bam2fq and nothing downstream consumes the input BAM directly)

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- output_documentation: nf-core boilerplate docs process (markdown_to_html.py of static run docs); upstream runs it unconditionally, so porting it would change the default plan for zero analytical value
- get_software_versions: nf-core boilerplate versions process (scrapes $workflow/$nextflow native variables into a versions.yml, which has no oxo-flow equivalent)

## Fidelity

Every upstream process of nf-core/eager 2.5.3 (63 total: 56 top-level
processes plus 7 conditional/indented ones — `makeBWAIndex`,
`makeBT2Index`, `unzip_reference`, `seqtype_merge`, `mtnucratio`,
`nuclear_contamination`, `decomp_kraken`) is listed below.
The 17 processes on the default-parameters main path (directory input,
paired-end, `mapper=bwaaln`, `dedupper=markduplicates`) are ported
byte-faithfully. The non-default branches are ported as `rules/branches.oxoflow`
(each gated on its upstream param, off by default) — including the full
metagenomic screening chain (bbduk complexity filter, kraken, kraken_parse,
kraken_merge, malt, maltextract; note the old "needs the upstream's bundled
MALT install (no conda package)" exclusion reason was wrong — the upstream
`environment.yml` pins `bioconda::malt=0.61` and `bioconda::hops=0.35`, so
MALT and MaltExtract ship inside the pinned `nfcore/eager:2.5.3` container).
The multi-lane raw-level merges (`lanemerge`, `lanemerge_hostremoval_fastq`)
are ported as a gated mode (`run_lanemerge`, off by default) built on the
`input_groups` engine primitive (Traitome/oxo-flow#231, oxo-flow >= 0.16.0) —
see the rows below. The remaining `not ported` rows are the BAM-level
library/seqtype channel merges (the port's model has one library per sample),
the unported BAM pass-through mode (`indexinputbam`), or nf-core boilerplate
(`output_documentation`, `get_software_versions`).

| Upstream process | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| unzip_reference | `unzip_reference` | pigz 2.6 | `gunzip -c` into the canonical reference path; `when = config.unzip_reference` (default false — pass a plain FASTA as before) |
| makeFastaIndex | `make_fasta_index` | samtools 1.12 | `samtools faidx` verbatim. Port copies the input to `results/reference_genome/fasta_index/reference.fa` (canonical name; upstream publishes `<fasta-base>.fai` only when `--save_reference`) |
| makeSeqDict | `make_seq_dict` | picard 2.26.0 | `picard -Xmx8192M CreateSequenceDictionary` verbatim; output named `reference.dict` (upstream `<fasta-base>.dict`) |
| makeBWAIndex | `make_bwa_index` | bwa 0.7.17 | `cp` into `BWAIndex/` + `bwa index` verbatim; canonical file name `reference.fa` |
| fastqc | `fastqc` | fastqc 0.11.9 | `fastqc -t N -q r1 r2` + rename `*_fastqc.zip` → `*_raw_fastqc.zip` verbatim (per-instance scoped rename; zips moved to `zips/` like the upstream publishDir saveAs) |
| fastp | `fastp` | fastp 0.20.1 | Off by default, same as upstream (`complexity_filter_poly_g=false`). PE branch flags verbatim. **Upstream feeds fastp only the 2-colour-chemistry branch** (`ch_input_for_fastp.twocol`, main.nf lines 723-746): with the default `colour_chemistry=4` fastp runs on zero samples even when the flag is on. The port mirrors this gate (`when = complexity_filter_poly_g && colour_chemistry == 2`); use `colour_chemistry=2` to actually filter poly-G |
| adapter_removal | `adapter_removal` | adapterremoval 2.3.2, adapterremovalfixprefix 0.0.5, pigz 2.6 | Default PE collapse branch verbatim: `--collapse --trimns --trimqualities`, cat of the 5 gz parts (`<base>.pe.collapsed.gz` etc. — the `.pe` basename AR writes, as upstream), `AdapterRemovalFixPrefix \| pigz -p <cpus-1>`. The `cat` operands are explicit per-sample names (shared results dir; upstream globs the workdir). When fastp is enabled the input switches to the fastp outputs (upstream channel mix); the AR basename stays the default-path one (`{r1.baseName}_L0` with the `_R1` suffix as upstream derives it) |
| fastqc_after_clipping | `fastqc_after_clipping` | fastqc 0.11.9 | Verbatim; zips to `zips/` |
| bwa | `bwa_aln` | bwa 0.7.17, samtools 1.12 | Verbatim PE branch: `bwa aln -n/-l/-k/-o` (Oliva 2021 defaults), `bwa samse` with the eager `@RG` string, `samtools sort -@ <cpus-1>`, `samtools index`. `.sai` written into the mapping dir (upstream workdir-local) |
| bwamem | `bwamem` | bwa 0.7.17, samtools 1.12 | `bwa mem -t N` + sort + index with the eager @RG string; `when = config.mapper == 'bwamem'` |
| bowtie2 | `bowtie2` | bowtie2 2.4.4, samtools 1.12 | `bowtie2 -x reference -1/-2` + sort + index; `when = config.mapper == 'bowtie2'` |
| makeBT2Index | `make_bt2_index` | bowtie2 2.4.4 | `bowtie2-build` into `results/reference_genome/bt2_index/`; `when = config.mapper == 'bowtie2'` |
| circulargenerator | `circulargenerator` | circularmapper 1.93.5, bwa | `circulargenerator -e -i -s` + `bwa index` on the elongated fasta; `when = config.mapper == 'circularmapper'` |
| circularmapper | `circularmapper` | bwa + circularmapper 1.93.5 | `bwa aln` on the elongated reference + `realignsamfile` + sort/index; `when = config.mapper == 'circularmapper'` |
| convertBam | `convert_bam` | samtools 1.12, pigz | `samtools bam2fq | pigz`; `when = config.bam_input` (default false — the fixture is FASTQ) |
| indexinputbam | — | samtools 1.12 | not ported — indexes the input BAM for upstream's BAM pass-through mode (`bam != 'NA' && !run_convertinputbam`, main.nf 657); the port's BAM-input mode routes through `convert_bam` (bam2fq) instead and nothing downstream consumes the input BAM directly, so no index is needed |
| hostremoval_input_fastq | `hostremoval_input_fastq` | extract_map_reads.py (bundled) | PE branch verbatim (`-m`, `-of`/`-or`, `-t`); `when = config.hostremoval_input_fastq` |
| samtools_flagstat | `samtools_flagstat` | samtools 1.12 | Verbatim: `samtools flagstat > {libraryid}_flagstat.stats` |
| samtools_filter | `samtools_filter_{bwaaln,bwamem,bowtie2,circularmapper}` | samtools 1.12, pigz 2.6 | Four per-mapper rules sharing ONE output set; each is gated `when = config.run_bam_filtering && config.mapper == '<mapper>'` (mutually exclusive, so the released engine needs no any-mode semantics) and takes its mapper's mapped BAM as `BAM="{input[0]}"` (`results/mapping/bwa/{sample}_PE.mapped.bam` / `results/mapping/bwa/{sample}.mapped.bam` / `results/mapping/bt2/{sample}.mapped.bam` / `results/mapping/circularmapper/{sample}.mapped.bam`). The shared body carries the minreadlength-0 branches selected by `bam_unmapped_type`: `discard` (`-F4 -q <thr>`, default) and `fastq` (upstream `-f4` / `-F4 -q` + `samtools fastq -tN \| pigz -p <cpus-1>` + `rm`, the metagenomic-chain producer), both verbatim. The discard branch additionally writes an EMPTY `{sample}.unmapped.fastq.gz` placeholder — the engine requires every declared output to exist, and it is never consumed (the metagenomic rules are gated on `bam_unmapped_type == 'fastq'`). The `keep`/`bam`/`both` branches fail fast with a clear error; bwaaln variant live-verified on tx-ubuntu 2026-08-27 (run_bam_filtering=true, 15 succeeded / 0 failed) |
| samtools_flagstat_after_filter | `samtools_flagstat_after_filter` | samtools 1.12 | `samtools flagstat` on the filtered BAM; `when = config.run_bam_filtering` |
| picard_addorreplacereadgroups | `picard_addorreplacereadgroups` | picard 2.26.0, samtools | verbatim RG replacement for MultiVCFAnalyzer; `when = run_genotyping && genotyping_tool == 'ug' && run_multivcfanalyzer` |
| markduplicates | `markduplicates` | picard 2.26.0, samtools 1.12 | Default dedupper. picard MarkDuplicates verbatim (`-Xmx4096M`, `REMOVE_DUPLICATES=TRUE AS=TRUE`, `VALIDATION_STRINGENCY=SILENT`) + `samtools index`. INPUT points at the mapped BAM directly instead of upstream's workdir-local `mv {bam} {libraryid}.bam` rename (the shared results dir must keep the mapped BAM for preseq/flagstat) |
| dedup | `dedup` | dedup 0.12.8, samtools 1.12 | Alternative dedupper (off by default, `dedupper='dedup'`). Verbatim: `dedup -Xmx4g -i ... -o . -u`, `mv *.log dedup.log`, in-place `samtools sort`, index. Upstream's `mv {bam} {libraryid}.bam` becomes a `cp` (shared-results-dir equivalent, same effect) |
| preseq | `preseq` | preseq 3.1.2 | Verbatim default branch: `preseq c_curve -s 1000 -o <base>.preseq -B <mapped bam>`. The `-H` (dedup mode) and `lc_extrap` branches are the alternate `preseq_mode`/`dedupper` combinations |
| bedtools | `bedtools_coverage` | bedtools 2.30.0, pigz | verbatim genome.txt + `bedtools coverage` breadth/depth; `when = config.run_bedtools_coverage` |
| damageprofiler | `damageprofiler` | damageprofiler 0.4.9 | Verbatim: `-Xmx4g -i <rmdup bam> -r <fasta> -l 100 -t 15 -o . -yaxis_damageplot 0.30`; output lands in `results/damageprofiler/<bam-basename>/` as upstream |
| mapdamage_calculation | `mapdamage_calculation` | mapdamage2 2.2.1 | verbatim `mapDamage -i -r --ymax --no-stats`; `when = !skip_damage_calculation && damage_calculation_tool == 'mapdamage'` |
| mapdamage_rescaling | `mapdamage_rescaling` | mapdamage2 2.2.1, samtools | verbatim `--rescale --rescale-out --seq-length` + index; `when = config.run_mapdamage_rescaling` |
| mask_reference_for_pmdtools | `mask_reference_for_pmdtools` | bedtools 2.30.0 | `bedtools maskfasta`; `when = pmdtools_reference_mask && run_pmdtools` |
| pmdtools | `pmdtools` | pmdtools 0.60, samtools | verbatim calmd|pmdtools filter + range chain incl. the 141 trap; `when = config.run_pmdtools` |
| bam_trim | `bam_trim` | bamutil 1.0.15, samtools | `bam trimBam -L -R` (double-stranded none-UDG clip values) + sort/index; `when = config.run_trim_bam` |
| post_ar_fastq_trimming | `post_ar_fastq_trimming` | fastp 0.20.1 | PE branch verbatim (`--trim_front1/2 --trim_tail1/2`); `when = config.run_post_ar_trimming` |
| lanemerge | `lanemerge` + `lanemerge_r2` | cat (pigz 2.6) | ported as a gated mode (`run_lanemerge=true`, off by default): the two rules group each sample's lane-tagged pairs (`{sample}_L{lane}_R{1,2}.fastq.gz`) via `input_groups` (group_by = sample, keep = lane; Traitome/oxo-flow#231, oxo-flow >= 0.16.0) and `cat` the pair into one merged fastq (`results/lanemerging/{sample}_R{1,2}_lanemerged.fq.gz`) consumed by fastp / adapter_removal / hostremoval_input_fastq. Deviations: upstream merges the per-library collapsed fastqs AFTER AdapterRemoval (main.nf 1125) and only merges R2 when `single_end=false`; the port merges the raw per-lane pairs pre-clipping (the raw-level `lanemerge_hostremoval_fastq` semantics) and always merges R2 (the port is pure-PE). Samples without lane-tagged files are untouched; with the gate off (or on a released engine without `input_groups`) the default single-pair path is byte-identical, and a fail-fast `{input}` guard prevents silently empty merges. Merged-content E2E passed locally 2026-08-27 (byte-identical to the single-pair inputs); full container run queued for tx-ubuntu |
| lanemerge_hostremoval_fastq | `hostremoval_input_fastq` (shell switch) | extract_map_reads.py (bundled) | ported as part of the gated mode: when `run_lanemerge=true` the rule feeds the merged pair from `results/lanemerging/` instead of the raw one — upstream's raw-level merge-into-hostremoval semantics (main.nf 1197). Without lane-tagged files the raw pair is used, exactly as before |
| library_merge | — | samtools 1.12 | not ported — structural: upstream merges the per-LIBRARY dedup BAMs of a sample (`samtools merge`, main.nf 1967); the port's directory-input model has ONE library per sample (library = sample, lane = 0) and one BAM per sample at every stage, so there are no multi-library BAMs to merge. `input_groups` cannot express it either — it groups FILES of a pattern, and the port has no per-library file dimension. Declare each library as its own sample (or pre-merge) before running |
| additional_library_merge | — | samtools 1.12 | not ported — structural: same constraint as `library_merge` (merges the per-library bam_trim BAMs, main.nf 2320); the port has one BAM per sample per stage |
| seqtype_merge | — | samtools 1.12 | not ported — structural: upstream merges the per-seqtype mapped BAMs of mixed PE/SE libraries into one BAM per library (`samtools merge`, main.nf 1597); the port is pure-PE (sample = text before `_R1`/`_R2`) with one mapped BAM per sample, so there are no mixed-PE/SE BAMs to merge. Convert SE samples to PE or run SE-only samples separately |
| qualimap | `qualimap` | qualimap 2.2.2d | Default path, ported: `qualimap bamqc -bam <rmdup bam> -nt 2 -outdir . -outformat "HTML" --java-mem-size=4G` verbatim; output lands in `results/qualimap/<bam-base>_bamqc/` as upstream |
| genotyping_pileupcaller | `genotyping_pileupcaller` | samtools 1.12, sequencetools 1.5.2 | Off by default, same as upstream (`run_genotyping=false`). Verbatim: `samtools mpileup -B --ignore-RG -q 30 -Q 30 [-l <bed>] -f <fasta> <bams> \| pileupCaller --randomHaploid --sampleNames <csv> [-f <snp>] -e pileupcaller.double` (single-instance fan-in; `-e` prefix `pileupcaller.double` = PE strandedness). `-l`/`-f` render only when `pileupcaller_bedfile`/`pileupcaller_snpfile` are set, exactly as upstream's dummy-file check (main.nf lines 2608-2609); without them the rule fails fast with upstream's error message — upstream exits 1 at workflow start (main.nf lines 74-78), the port's guard lives in the rule shell because oxo-flow has no params-validation stage |
| genotyping_ug | `genotyping_ug` | gatk3 3.5, bgzip | verbatim RealignerTargetCreator → IndelRealigner → UnifiedGenotyper → bgzip; `when = run_genotyping && genotyping_tool == 'ug'` |
| genotyping_hc | `genotyping_hc` | gatk4 4.2.0.0, bgzip | verbatim HaplotypeCaller flags + bgzip; `when = run_genotyping && genotyping_tool == 'hc'` |
| genotyping_freebayes | `genotyping_freebayes` | freebayes 1.3.5, bgzip | verbatim `freebayes -f -p -C [-g]` + bgzip; `when = run_genotyping && genotyping_tool == 'freebayes'` |
| genotyping_angsd | `genotyping_angsd` | angsd 0.935 | verbatim bam.filelist + `angsd -GL -doGlF`; `when = run_genotyping && genotyping_tool == 'angsd'` |
| bcftools_stats | `bcftools_stats` | bcftools 1.12 | `bcftools stats <vcf.gz> -F <fasta>`; `when = config.run_bcftools_stats` (source VCF via `bcftools_stats_source`) |
| eigenstrat_snp_coverage | `eigenstrat_snp_coverage` | eigenstratdatabasetools 1.0.2, python 3.9.4 | Off by default, same as upstream. Verbatim: `eigenstrat_snp_coverage -i pileupcaller.double >double_eigenstrat_coverage.txt` + `parse_snp_cov.py` (bundled upstream script, called via `python3 scripts/parse_snp_cov.py` — oxo-flow does not auto-add `bin/` to PATH) |
| metagenomic_complexity_filter | `metagenomic_complexity_filter` | bbduk 38.92 | verbatim `bbduk.sh -Xmx<g>g in=... threads=N entropymask=f entropy=<entropy> out=<in>_lowcomplexityremoved.fq.gz 2> <in>_bbduk.stats` — the output keeps upstream's `${input}_lowcomplexityremoved.fq.gz` naming; `when = metagenomic_complexity_filter && run_bam_filtering && bam_unmapped_type == 'fastq'` (upstream validates the same combination at workflow start, main.nf 115-122) |
| malt | `malt` | malt 0.61 | verbatim `malt-run -J-Xmx<g>g -t N -v -o . -d <db> [-a . -f SAM] -id -m -at -top <min-supp> -mq --memoryMode -i <all fastqs>` — one instance over ALL samples' unmapped reads (upstream `collect()`); reads the entropy-filtered fastqs when the complexity filter is on (upstream channel switch); `--database` is split into `malt_db` + `kraken2_db`; the percent/reads min-support exclusivity check (main.nf 129-134) is a shell guard; the per-input `.rma6` outputs are undeclared (no fixed template) — only `malt.log` is declared; NOT yet live-verified; `when = run_metagenomic_screening && run_bam_filtering && bam_unmapped_type == 'fastq' && metagenomic_tool == 'malt'` |
| maltextract | `maltextract` | hops 0.35 | verbatim `MaltExtract -Xmx<g>g -t <taxon_list> -i <rma6s> -o results/ -r <ncbifiles> -p N -f -a --minPI <flags>` + `postprocessing.AMPS.r -r results/ -m -t N -n <taxon_list> -j`; requires `maltextract_taxon_list` + `maltextract_ncbifiles` (fail-fast guard); consumes the rma6s via glob with a DAG edge through `malt.log`; NOT yet live-verified; `when = run_maltextract && metagenomic_tool == 'malt'` (upstream verbatim) |
| kraken | `kraken` | kraken2 2.1.2 | verbatim `kraken2 --db <db> --threads N --output <prefix>.kraken.out --report-minimizer-data --report <prefix>.kraken2_report <fastq>` + `cut -f1-3,6-8 > <prefix>.kreport`; reads the entropy-filtered fastq when the complexity filter is on (upstream channel switch); the output prefix is normalized to `{sample}.unmapped.fastq` in both branches (upstream prefixes by the input basename — see deviations); live-verified on tx-ubuntu 2026-08-27 (synthetic 2-taxon kraken2 DB built in-container via `kraken2-build --add-to-library` with `kraken:taxid|` headers; 14/14 injected alien reads classified as *Alienus syntheticus*, 18 succeeded / 0 failed); `when = run_metagenomic_screening && run_bam_filtering && bam_unmapped_type == 'fastq' && metagenomic_tool == 'kraken'` |
| kraken_parse | `kraken_parse` | python 3.9.4 | verbatim `kraken_parse.py -c <min_support_reads> -or <read csv> -ok <kmer csv> <kreport>` (upstream script bundled in `scripts/`, called via `python3 scripts/kraken_parse.py` — oxo-flow does not auto-add `bin/` to PATH); gated on the same `when` as kraken (upstream no-ops the process via an empty channel); live-verified on tx-ubuntu 2026-08-27 (same run as kraken) |
| kraken_merge | `kraken_merge` | python 3.9.4 | verbatim `merge_kraken_res.py -or kraken_read_count.csv -ok kraken_kmer_duplication.csv` (upstream script bundled in `scripts/`; it scans the working dir for the per-sample CSVs, which the fan-in gathers into one instance); gated on the same `when` as kraken; live-verified on tx-ubuntu 2026-08-27 (same run as kraken) |
| decomp_kraken | `kraken` (folded in) | kraken2 2.1.2 | folded into the kraken shell: a `.tar.gz` `kraken2_db` is unpacked in place (`tar xzf`, `mkdir -p <db>`, `mv *.k2d <db>/`) — no when-expression can test a filename suffix (deviation, documented below) |
| sexdeterrmine | `sexdeterrmine` | sexdeterrmine 1.1.2 | verbatim sexdeterrmine.py run; `when = config.run_sexdeterrmine` |
| sexdeterrmine_prep | `sexdeterrmine_prep` | sexdeterrmine 1.1.2 | verbatim sexdeterrmine_prep.py; `when = config.run_sexdeterrmine` |
| mtnucratio | `mtnucratio` | sequencetools 1.5.2 | verbatim `mtnucratio -Xmx`; `when = config.run_mtnucratio` |
| nuclear_contamination | `nuclear_contamination` | angsd 0.935 (contaminationX) | verbatim contaminationX invocation; `when = config.run_nuclear_contamination` |
| endorSpy | `endor_spy` | endorSpy | `endorS.py -o json -n <sample> <flagstat>`; `when = config.run_endor_spy` (upstream runs it unconditionally; the port gates it to keep the default path unchanged) |
| print_nuclear_contamination | `print_nuclear_contamination` | grep | report row extraction; `when = config.run_nuclear_contamination` |
| multivcfanalyzer | `multivcfanalyzer` | multivcfanalyzer 0.85.2, pigz | verbatim cohort run over all UG VCFs (expand_inputs over `multivcf_samples`); `when = run_genotyping && genotyping_tool == 'ug' && run_multivcfanalyzer` |
| vcf2genome | `vcf2genome` | vcf2genome 0.91, pigz | verbatim consensus call incl. refMod/uncertainty fastas; `when = config.run_vcf2genome` |
| multiqc | `multiqc` | multiqc 1.16 | `multiqc -f --config assets/multiqc_config.yaml .` (the upstream `--title/--filename` run-name flags are nf-core boilerplate and are dropped). Module files are staged into per-module subdirs mirroring the upstream multiqc process inputs; staging is guarded so skipped modules are simply absent. Report at `results/multiqc/multiqc_report.html` |
| output_documentation | — | — | not ported — nf-core boilerplate docs process (markdown_to_html.py of static run docs); upstream runs it unconditionally, so porting it would change the default plan for zero analytical value |
| get_software_versions | — | — | not ported — nf-core boilerplate versions process (scrapes `$workflow`/`$nextflow` native variables into a versions.yml; a versions.yml has no oxo-flow equivalent, and `scrape_software_versions.py` targets Nextflow env vars) |

Additional deviations from upstream (all on the default path):

- The `publishDir` mechanism has no oxo-flow equivalent: outputs are written
  directly at the `results/...` paths upstream publishes to (see
  `output = [...]` in `main.oxoflow`); `publish_dir_mode`/`saveAs` are
  folded into the shells where they rename files.
- Reference files use the canonical name `reference.fa` (and
  `reference.dict`) in `results/reference_genome/` instead of the input
  fasta basename; all reference-consuming rules point at those copies.
- Upstream labels are baked into per-rule `[rules.resources]`:
  `sc_tiny` 1 cpu/1G/4h, `sc_small` 1/4G, `sc_medium` 1/8G, `mc_small`
  2/4G, `mc_medium` 4/8G, plus the base-process default (1 cpu/7G/24h)
  used by the undefined `mc_tiny` label (eigenstrat_snp_coverage).
  JVM heaps are byte-identical (`-Xmx8192M`, `-Xmx4096M`, `-Xmx4g`,
  `--java-mem-size=4G`).
- Gated-mode deviations (`run_lanemerge=true`, off by default):
  - upstream runs `lanemerge` on the per-library collapsed fastqs AFTER
    AdapterRemoval (main.nf 1125, a small post-collapse cat of the `.pe`
    pair); the port merges the raw per-lane pairs BEFORE clipping (the
    `lanemerge_hostremoval_fastq` raw-level semantics, main.nf 1197) so
    that clipping, mapping, dedup, damage and QC all run on the merged
    pair exactly once. The lane-tagged naming (`{sample}_L{lane}_R{1,2}`)
    is upstream's TSV input-mode style; upstream detects multi-lane from
    the sample sheet, the port gates on `run_lanemerge` (auto-detection
    from filenames is impossible for a when-expression). Only R1 was
    upstream's documented lanemerge concern; the port merges R2 as well
    (pure-PE, both ends must exist).
  - `fastqc` runs on the merged pair in gated mode (twin rule
    `fastqc_lanemerged` with an exclusive when-gate); upstream runs
    FastQC on the per-lane input fastqs.
  - samples with lane-tagged files mixed with default-named files in one
    directory: lane-tagged samples flow through the merged path, the
    others through the default path (shell existence-check switch in
    fastp / adapter_removal / hostremoval_input_fastq).
  - local E2E 2026-08-27 (dev engine, no container): merged pairs
    byte-identical to the single-pair inputs (S1: 3635 reads, S2: 3602
    reads, R1/R2 counts equal). Full container run queued for tx-ubuntu
    (docker daemon unavailable on the authoring machine).
- Metagenomic-chain deviations (`rules/branches.oxoflow` B32-B37, all off by
  default):
  - upstream's run-level validation (main.nf 115-137) becomes rule gates +
    fail-fast shell guards (oxo-flow has no params-validation stage).
  - `kraken_parse`/`kraken_merge` carry the same `when` as `kraken`
    (upstream no-ops them via empty channels).
  - `decomp_kraken` (`.tar.gz` kraken2 DB unpack) is folded into the
    `kraken` shell — no when-expression can test a filename suffix.
  - the kraken output prefix is normalized to `{sample}.unmapped.fastq`
    in both filter branches (upstream prefixes by the input basename,
    which differs when the complexity filter is on).
  - MALT `.rma6` outputs are undeclared (per-input names, no fixed
    template; `.sai` precedent); only `malt.log` is declared and
    `maltextract` consumes the rma6s via glob with a DAG edge through
    `malt.log`.
  - upstream's single `--database` param is split into `malt_db` and
    `kraken2_db`.
  - each `samtools_filter_<mapper>` variant writes an empty `{sample}.unmapped.fastq.gz`
    placeholder in discard mode (engine output-existence contract; never
    consumed — the metagenomic rules are gated on `bam_unmapped_type == 'fastq'`).
  - the kraken metagenomic chain (kraken/kraken_parse/kraken_merge) is
    live-verified on tx-ubuntu 2026-08-27 with a synthetic 2-taxon
    kraken2 DB (build recipe: `kraken2-build --add-to-library` with
    `kraken:taxid|N|` sequence headers — a manual `seqid2taxid.map`
    alone builds an EMPTY table, and the map must be sorted);
    `bam_unmapped_type=fastq` + `run_bam_filtering` + 
    `run_metagenomic_screening` + `metagenomic_tool=kraken`, 18
    succeeded / 0 failed. The MALT half (malt/maltextract) remains NOT
    live-verified (needs a MALT index DB, not yet available on the test
    server).
- A `.gz`-compressed reference FASTA is not supported (upstream's
  `unzip_reference` pigz pre-step is not ported): pass a plain FASTA.
- Upstream's startup parameter validation (e.g. the pileupCaller
  bed/snp exit-1 check, main.nf lines 74-78) has no oxo-flow
  equivalent: the checks live as fail-fast guards at the top of the
  affected rule shells (`genotyping_pileupcaller`), so an invalid
  invocation fails when the rule runs rather than at workflow start.
- Upstream `errorStrategy retry` (signals 143/137/104/134/139/140, max 3)
  and the exit-1 retry on dedup/markduplicates/damageprofiler/qualimap are
  not ported (oxo-flow has no signal-based retry); `preseq`'s
  `errorStrategy 'ignore'` is likewise not ported.
- The conditional `preserve5p`/`mergedonly` AR branches (both off by
  default) are not ported; their config keys are kept with upstream
  defaults.
- `run_pmdtools`, `run_trim_bam`, `run_post_ar_trimming`,
  `run_mapdamage_rescaling`, `run_bedtools_coverage`, `run_vcf2genome`,
  `run_multivcfanalyzer`, `run_sexdeterrmine`, `run_mtnucratio`,
  `run_nuclear_contamination`, `run_endorSpy`, `run_convertinputbam`,
  `run_hostremoval` and the non-default mapper/dedupper/damage-tool/
  genotyping-tool choices are all ported as the gated branch rules above
  (the port's keys are `run_endor_spy`, `bam_input` and
  `hostremoval_input_fastq` where the upstream names `run_endorSpy`,
  `run_convertinputbam` and `hostremoval_input_fastq` differ);
  `run_bam_filtering` (incl. the metagenomic screening chain under
  `run_metagenomic_screening` with `metagenomic_tool` = `kraken`/`malt`) IS
  ported. Default values are kept in `[config]` where a config key exists.

## Links

- Repository: [oxo-flow-eager](https://github.com/oxo-flow-community/oxo-flow-eager)
- Upstream: [nf-core/eager](https://github.com/nf-core/eager) @ `2.5.3`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
