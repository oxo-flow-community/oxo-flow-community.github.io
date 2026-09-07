---
title: "ATAC-seq: peak calling and QC"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-atacseq</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>ATAC-seq: peak calling and QC</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">atac-seq</span><span class="ox-tag">peaks</span><span class="ox-tag">epigenomics</span><span class="ox-tag">single-end</span><span class="ox-tag">paired-end</span><span class="ox-tag">qc</span></div>
<p class="ox-desc">ATAC-seq peak calling and QC: FastQC raw-read QC, Trim Galore adapter trimming, BWA-MEM alignment, Picard mark-duplicates, BAMTools filtering, MACS2 broad-peak calling, HOMER peak annotation, FRiP scoring, normalised bigWig tracks, deepTools QC plots and a combined MultiQC report. Default plan is the upstream single-end aligner=bwa main path (15 rules); when-gated branches port the paired-end path, Bowtie2/Chromap/STAR aligners, reference preparation, mitochondrial filtering, consensus peaks/DESeq2, preseq, Picard metrics, ataqv, IGV and R QC plots (27 further rules), and the merged-replicate analysis over _REP\d+ sample groups (43 total).</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-atacseq" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">43</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 12 CPUs / 72 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">epigenomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/atacseq">nf-core/atacseq</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>2.1.2</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2284.1"><code>10.48546/workflowhub.workflow.2284.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastqc</span><span class="tchip">trim-galore</span><span class="tchip">bwa</span><span class="tchip">bowtie2</span><span class="tchip">chromap</span><span class="tchip">star</span><span class="tchip">samtools</span><span class="tchip">picard</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>ATAC-seq peak calling and QC pipeline</strong> (BWA-MEM + MACS2): given a reference genome and FASTQ reads, it trims adapters, aligns, deduplicates, calls peaks, annotates them, and aggregates all QC into a MultiQC report — a port of nf-core/atacseq 2.1.2.</p>
<p><strong>1. Input QC and trimming</strong> — <code>fastqc</code> reports raw-read quality; <code>trimgalore</code> trims adapters and re-runs FastQC, feeding every alignment route.</p>
<p><strong>2. Alignment</strong> — single-end reads are aligned by <code>bwa_mem</code> against <code>ref::bwa_index</code>, or by one runtime-selected alternative (<code>alt::bowtie2_align</code>, <code>alt::chromap_align</code>, <code>alt::star_align</code>); paired-end reads take <code>pe::trimgalore_pe</code> → <code>pe::bwa_mem_pe</code>. All routes converge on <code>samtools_sort_stats</code>.</p>
<p><strong>3. Merge, deduplicate, filter</strong> — <code>picard_mergesamfiles</code> and <code>picard_markduplicates</code> consolidate libraries and mark duplicates (paired reads re-enter via <code>pe::bamtools_filter_pe</code> → <code>pe::pe_name_sort_remove_orphans</code>); <code>bamtools_filter</code> drops unmapped, secondary, and low-quality reads, and, when replicate samples are declared, <code>merge_replicates</code> merges the per-replicate filtered BAMs per sample.</p>
<p><strong>4. Peaks, annotation, FRiP</strong> — <code>macs2_callpeak</code> calls broad peaks; <code>homer_annotatepeaks</code> annotates them, while <code>frip_score</code> measures the fraction of reads in peaks.</p>
<p><strong>5. Tracks and enrichment plots</strong> — <code>bedtools_genomecov</code> writes a million-read-normalized bedGraph (<code>pe::bedtools_genomecov_pe</code> paired-end); <code>ucsc_bedgraphtobigwig</code> converts it to bigWig for <code>deeptools_plots</code>, and <code>plotfingerprint</code> (<code>pe::plotfingerprint_pe</code>) plots coverage fingerprints.</p>
<p><strong>6. Consensus peaks (gated)</strong> — <code>cons::macs2_consensus</code> merges peak sets into a consensus BED, annotated by <code>cons::homer_annotatepeaks_consensus</code> and quantified by <code>cons::subread_featurecounts</code>; <code>cons::deseq2_qc</code> runs DESeq2 QC.</p>
<p><strong>7. Extra QC and reports (gated)</strong> — optional branches add <code>qce::preseq_lcextrap</code>, <code>qce::picard_collectmultiplemetrics</code>, ATAQV (<code>qce::ataqv</code> on <code>qce::get_autosomes</code>, indexed by <code>qce::mkarv</code>), peak QC (<code>qce::plot_macs2_qc</code>, <code>qce::plot_homer_annotatepeaks</code>, <code>qce::multiqc_custom_peaks</code>) and <code>qce::igv</code>; <code>multiqc</code> (single-end) or <code>pe::multiqc_pe</code> (paired-end) aggregates the run.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-atacseq+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-atacseq
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-atacseq` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-atacseq@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-atacseq` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Needs reference genome and peak-calling inputs — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.12.0 (the merged-replicate mode — _REP\d+ sample groups plus config.merged_samples — additionally requires oxo-flow with input_groups support, Traitome/oxo-flow#231; on released engines the gate is inert and the default path is unchanged)

**Toolchain.** containers (Docker/Singularity) — pinned images for 40 of 43 rules, plus one pinned conda env (envs/picard-samtools.yaml) shared by the three picard rules (picard_mergesamfiles, picard_markduplicates, merge_replicates)

**Requirements.**

- reference data: genome FASTA with .fai, BWA index prefix (.amb/.ann/.bwt/.pac/.sa), chrom sizes file, GTF annotation, gene BED, TSS BED (optional blacklist BED); alt-aligner indexes for aligner=bowtie2/chromap/star
- input: single-end <sample>.fastq.gz reads (default) or <sample>_1/2.fastq.gz (paired=true), declared in [[sample_groups]]; replicate groups use the upstream _REP\d+ suffix and feed config.merged_samples (see README)
- compute: up to 12 CPUs / 72 GB per rule
- runtime: Docker or Singularity for the 40 container rules; conda/mamba for the three picard rules (picard_mergesamfiles, picard_markduplicates, merge_replicates)

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-atacseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-atacseq
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy aligner = value" data-copy="aligner = bwa">aligner</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>bwa</code></td>
<td class="ox-p-desc">params.aligner: &quot;bwa&quot; (default) | &quot;bowtie2&quot; | &quot;chromap&quot; | &quot;star&quot; (SE only)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy blacklist = value" data-copy="blacklist = ">blacklist</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">params.blacklist — include-regions BED (complement of ENCODE<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bowtie2_index = value" data-copy="bowtie2_index = ">bowtie2_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">params.bowtie2 — index prefix (.rev.1.bt2 etc. beside it) for aligner=&quot;bowtie2&quot;<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy broad_cutoff = value" data-copy="broad_cutoff = 0.1">broad_cutoff</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.1</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwa_index = value" data-copy="bwa_index = test/fixtures/genome/genome.fa">bwa_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genome/genome.fa</code></td>
<td class="ox-p-desc">params.bwa — index prefix (.amb/.ann/.bwt/.pac/.sa beside it)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy chrom_sizes = value" data-copy="chrom_sizes = test/fixtures/genome/genome.fa.sizes">chrom_sizes</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genome/genome.fa.sizes</code></td>
<td class="ox-p-desc">CUSTOM_GETCHROMSIZES output<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy chromap_index = value" data-copy="chromap_index = ">chromap_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">params.chromap — index file for aligner=&quot;chromap&quot;<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy deseq2_vst = value" data-copy="deseq2_vst = true">deseq2_vst</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">params.deseq2_vst<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fingerprint_bins = value" data-copy="fingerprint_bins = 500000">fingerprint_bins</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>500000</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fragment_size = value" data-copy="fragment_size = 200">fragment_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>200</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gene_bed = value" data-copy="gene_bed = test/fixtures/genome/gene.bed">gene_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genome/gene.bed</code></td>
<td class="ox-p-desc">params.gene_bed<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf = value" data-copy="gtf = test/fixtures/genome/genes.gtf">gtf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genome/genes.gtf</code></td>
<td class="ox-p-desc">params.gtf<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy keep_dups = value" data-copy="keep_dups = false">keep_dups</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy keep_mito = value" data-copy="keep_mito = false">keep_mito</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">params.keep_mito — keep mitochondrial reads when mito_name set<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy keep_multi_map = value" data-copy="keep_multi_map = false">keep_multi_map</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy macs_gsize = value" data-copy="macs_gsize = 2.7e9">macs_gsize</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>2.7e9</code></td>
<td class="ox-p-desc">blacklist + chrM when keep_mito=false); empty = no -L filter<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy merged_samples = value" data-copy="merged_samples = ">merged_samples</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">base names of replicate groups (e.g. &quot;S1,S2&quot; for samples S1_REP1/S1_REP2/S2_REP1/S2_REP2) — feeds merged-replicate files into the MultiQC / IGV aggregation rules; empty = no-op<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_reps_consensus = value" data-copy="min_reps_consensus = 1">min_reps_consensus</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">params.min_reps_consensus<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_trimmed_reads = value" data-copy="min_trimmed_reads = 10000">min_trimmed_reads</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10000</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mito_name = value" data-copy="mito_name = ">mito_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">params.mito_name, e.g. &quot;chrM&quot; — enables mitochondrial filtering (needs config.chrom_sizes)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy multiqc_custom_peaks = value" data-copy="multiqc_custom_peaks = false">multiqc_custom_peaks</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">port-only switch: emit MULTIQC_CUSTOM_PEAKS peak-count/FRiP TSVs<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy narrow_peak = value" data-copy="narrow_peak = false">narrow_peak</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">params.outdir<br><span class="ox-param-usedby">used by <code>41</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy paired = value" data-copy="paired = false">paired</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Gated branches (defaults keep the default plan identical to the upstream<br>default main path; toggle one key at a time to activate its branch only)<br><span class="ox-param-usedby">used by <code>24</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy picard_xmx_gb = value" data-copy="picard_xmx_gb = 8">picard_xmx_gb</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>8</code></td>
<td class="ox-p-desc">GB passed to picard -Xmx. Previously derived from the rule&#x27;s 36G<br>resource budget (Xmx≈30G), which thrash-killed the JVM on a 3.7 GB<br>machine (live run); the resource budget still drives scheduling.<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy prepare_reference = value" data-copy="prepare_reference = false">prepare_reference</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">port switch: build BWA index + chrom sizes from config.reference<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy raw_blacklist = value" data-copy="raw_blacklist = ">raw_blacklist</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">params.blacklist — raw ENCODE blacklist BED (complemented into include-regions)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy raw_dir = value" data-copy="raw_dir = test/fixtures/raw">raw_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/raw</code></td>
<td class="ox-p-desc">input fastqs (raw/&lt;sample&gt;.fastq.gz for single-end)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference = value" data-copy="reference = test/fixtures/genome/genome.fa">reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genome/genome.fa</code></td>
<td class="ox-p-desc">Reference inputs. Upstream obtains these from nf-core iGenomes (--genome);<br>this port expects pre-built files (see README &quot;References&quot;).<br><span class="ox-param-usedby">used by <code>13</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy save_trimmed = value" data-copy="save_trimmed = false">save_trimmed</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_ataqv = value" data-copy="skip_ataqv = true">skip_ataqv</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream default false; port ships this branch OFF (set false to enable)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_consensus_peaks = value" data-copy="skip_consensus_peaks = true">skip_consensus_peaks</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream default false; port ships this branch OFF (set false to enable)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_deseq2_qc = value" data-copy="skip_deseq2_qc = true">skip_deseq2_qc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream default false; port ships DESeq2 QC OFF (set false to enable)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastqc = value" data-copy="skip_fastqc = false">skip_fastqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_igv = value" data-copy="skip_igv = true">skip_igv</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream default false; port ships this branch OFF (set false to enable)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_merge_replicates = value" data-copy="skip_merge_replicates = false">skip_merge_replicates</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">params.skip_merge_replicates (upstream default false = merged-replicate analysis ON when replicate samples are declared)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_multiqc = value" data-copy="skip_multiqc = false">skip_multiqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_peak_annotation = value" data-copy="skip_peak_annotation = false">skip_peak_annotation</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">params.skip_peak_annotation (default false — HOMER annotation on by default, as upstream)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_peak_qc = value" data-copy="skip_peak_qc = true">skip_peak_qc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream default false; port ships the R QC plots OFF (set false to enable)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_picard_metrics = value" data-copy="skip_picard_metrics = true">skip_picard_metrics</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream default false; port ships this branch OFF (set false to enable)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_plot_fingerprint = value" data-copy="skip_plot_fingerprint = false">skip_plot_fingerprint</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_plot_profile = value" data-copy="skip_plot_profile = false">skip_plot_profile</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_preseq = value" data-copy="skip_preseq = true">skip_preseq</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">params.skip_preseq (upstream default true — preseq off by default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_qc = value" data-copy="skip_qc = false">skip_qc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_trimming = value" data-copy="skip_trimming = false">skip_trimming</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Upstream default params (kept as config so CLI overrides work)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_index = value" data-copy="star_index = ">star_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">params.star — STAR genome dir (built by STAR_GENOMEGENERATE upstream) for aligner=&quot;star&quot;<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy tss_bed = value" data-copy="tss_bed = test/fixtures/genome/tss.bed">tss_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genome/tss.bed</code></td>
<td class="ox-p-desc">params.tss_bed<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-atacseq-rules.svg?v=ceae994d1e" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-atacseq-rules.svg?v=ceae994d1e" alt="oxo-flow-atacseq rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-atacseq.svg?v=1d43bd0965" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-atacseq.svg?v=1d43bd0965" alt="oxo-flow-atacseq pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-atacseq — ATAC-seq peak calling and QC: FastQC raw-read QC, Trim Galore adapter trimming, BWA-MEM alignment, Picard mark-duplicates, BAMTools filtering, MACS2 broad-peak calling, HOMER peak annotation, FRiP scoring, normalised bigWig tracks, deepTools QC plots and a combined MultiQC report.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastqc
- trimgalore
- bwa_mem
- samtools_sort_stats
- picard_mergesamfiles
- picard_markduplicates
- bamtools_filter
- merge_replicates
- macs2_callpeak
- homer_annotatepeaks
- frip_score
- bedtools_genomecov
- ucsc_bedgraphtobigwig
- deeptools_plots
- plotfingerprint
- multiqc
- bowtie2_align
- chromap_align
- star_align
- macs2_consensus
- homer_annotatepeaks_consensus
- subread_featurecounts
- deseq2_qc
- genome_blacklist_regions
- fastqc_pe
- trimgalore_pe
- bwa_mem_pe
- bamtools_filter_pe
- pe_name_sort_remove_orphans
- bedtools_genomecov_pe
- plotfingerprint_pe
- multiqc_pe
- preseq_lcextrap
- picard_collectmultiplemetrics
- get_autosomes
- ataqv
- mkarv
- plot_macs2_qc
- plot_homer_annotatepeaks
- multiqc_custom_peaks
- igv
- bwa_index
- custom_getchromsizes

**Excluded**

- GFFREAD (GFF3→GTF conversion, upstream prepare_genome) — not ported; the port requires a pre-built GTF (`config.gtf`)
- GUNZIP of compressed reference/annotation files (upstream prepare_genome auto-decompresses `.gz` fasta/gtf/gff/bed/blacklist/tss) — not ported; reference files must be supplied uncompressed
- UNTAR of prebuilt alignment-index tarballs (upstream prepare_genome accepts bwa/bowtie2/chromap/star index tarballs) — not ported; the port requires unpacked index files
- KHMER_UNIQUEKMERS automatic `macs_gsize` estimation (upstream prepare_genome when `params.macs_gsize` is empty) — not ported; `config.macs_gsize` defaults to 2.7e9 (GRCh37/38 @ 50 bp) and must be set manually for other genomes

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- INPUT_CHECK (samplesheet_check) — pipeline plumbing; oxo-flow provides native [[sample_groups]] declaration + validate
- DUMP_SOFTWARE_VERSIONS — pipeline plumbing; oxo-flow has native version/audit mechanisms
- UMITOOLS_EXTRACT (umi branch) — dead code at 2.1.2: the workflow hardcodes with_umi=false so the branch can never fire
- nucleosome_analysis / genrich — not present at tag 2.1.2 (checked workflows/, conf/, subworkflows/)

## Fidelity

Ported with upstream defaults: `aligner=bwa`, single-end, `narrow_peak=false`
(broad peaks), no control. One row per upstream process; steps not ported are
listed with reasons. `when`-gated rules carry the gate in the Notes column.

| Upstream process | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` / `pe::fastqc_pe` | fastqc 0.11.9 | identical command (`--quiet --threads`); PE variant in the paired branch |
| TRIMGALORE | `trimgalore` / `pe::trimgalore_pe` | trim-galore 0.6.7 | identical command (`--fastqc --cores 8 --gzip`); PE variant uses `--paired` + `_val_1/2` outputs |
| FASTQ_FASTQC_UMITOOLS_TRIMGALORE (UMITOOLS_EXTRACT) | — | — | **not ported** — dead code at 2.1.2: the workflow hardcodes `with_umi=false`, the branch can never fire |
| BWA_MEM | `bwa_mem` / `pe::bwa_mem_pe` | bwa 0.7.17, samtools 1.17 | identical (`-M -R '@RG...'`, secondary-alignment filter `-F 0x0100`), mulled container; PE variant merges read groups |
| BOWTIE2_ALIGN | `alt::bowtie2_align` | bowtie2 2.5.1, samtools 1.17 | identical (end-to-end, `--very-sensitive`, `-k 4`, SAM→BAM filter); when `aligner = "bowtie2"` |
| CHROMAP_CHROMAP | `alt::chromap_align` | chromap 0.2.5, samtools 1.17 | identical (`-l 2000 --Tn5-shift --low-mem`); when `aligner = "chromap"` |
| STAR_ALIGN | `alt::star_align` | star 2.6.1d | identical (EndToEnd, `--alignIntronMax 1`, unsorted BAM); when `aligner = "star"` |
| BAM_SORT_STATS_SAMTOOLS (SAMTOOLS_SORT + SAMTOOLS_INDEX + SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS) | `samtools_sort_stats` / `pe::pe_name_sort_remove_orphans` | samtools 1.17 | identical commands, folded into one rule (same env); PE adds name sort → `bampe_rm_orphan.py --only_fr_pairs` → coordinate sort (upstream BAM_SORT_STATS_ORPHANS) |
| PICARD_MERGESAMFILES_LIBRARY | `picard_mergesamfiles` / `pe::bwa_mem_pe` | picard 3.0.0 | upstream symlink branch for single-library samples replicated; multi-library merge (actual MergeSamFiles) not expressible — no library source in oxo-flow |
| BAM_MARKDUPLICATES_PICARD (PICARD_MARKDUPLICATES + SAMTOOLS_INDEX + SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS) | `picard_markduplicates` | picard 3.0.0, samtools 1.17 | identical commands (`--ASSUME_SORTED --REMOVE_DUPLICATES false`, `XMX` heap sizing); combined conda env |
| BAMTOOLS_FILTER + SAMTOOLS_INDEX + BAM_STATS_SAMTOOLS (SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS) | `bamtools_filter` / `pe::bamtools_filter_pe` | bamtools 2.5.2, samtools 1.17 | identical (`-F 0x004 -F 0x0400 -q 1`, optional `-L blacklist`, `assets/bamtools_filter_{se,pe}.json`); PE adds `-f 0x001 -F 0x0008` |
| MACS2_CALLPEAK | `macs2_callpeak` | macs2 2.2.7.1 | identical (`--keep-dup all --nomodel --broad --broad-cutoff 0.1`, `gsize` from config, `--format BAM`) |
| HOMER_ANNOTATEPEAKS | `homer_annotatepeaks` / `cons::homer_annotatepeaks_consensus` | homer 4.11 | identical (`-gid -gtf`); consensus variant annotates the consensus BED, when `skip_consensus_peaks = false` |
| FRIP_SCORE | `frip_score` | bedtools 2.30.0, samtools 1.17 | identical (intersectBed `-f 0.20`, flagstat `mapped` fraction) |
| BEDTOOLS_GENOMECOV | `bedtools_genomecov` / `pe::bedtools_genomecov_pe` | bedtools 2.30.0 | identical (`-bg -scale 1e6/reads -fs fragment_size`, sort); PE uses `-pc` instead of `-fs` (upstream) |
| UCSC_BEDGRAPHTOBIGWIG | `ucsc_bedgraphtobigwig` | ucsc-bedgraphtobigwig 445 | identical |
| BIGWIG_PLOT_DEEPTOOLS (COMPUTEMATRIX scale-regions + reference-point, PLOTPROFILE, PLOTHEATMAP) | `deeptools_plots` | deeptools 3.5.1 | identical args (regionBodyLength 1000, ±3000, `--missingDataAsZero --skipZeros --smartLabels`) |
| MERGED_LIBRARY_DEEPTOOLS_PLOTFINGERPRINT | `plotfingerprint` / `pe::plotfingerprint_pe` | deeptools 3.5.1 | identical (`--extendReads fragment_size`); PE omits `--extendReads` (upstream) |
| MULTIQC | `multiqc` / `pe::multiqc_pe` | multiqc 1.13 | upstream mechanism replicated: `multiqc_config.yml` staged in cwd, `multiqc -f .`; config `path_filters` adapted to this port's `results/` layout; PE adds the PE fastqc/trimgalore patterns |
| BWA_INDEX | `ref::bwa_index` | bwa 0.7.17 | identical (`bwa index -p`); when `prepare_reference = true` (default false — port takes pre-built indexes) |
| CUSTOM_GETCHROMSIZES / CUSTOM_GENOME_FASTA_INDEX (prepare_genome) | `ref::custom_getchromsizes` | samtools 1.17 (envs/picard-samtools.yaml pin) | `samtools faidx` + `cut -f 1,2` into `config.chrom_sizes`; when `prepare_reference = true` |
| GENOME_BLACKLIST_REGIONS (mitochondrial filtering) | `mito::genome_blacklist_regions` | bedtools 2.30.0 | sortBed/complementBed over `config.raw_blacklist`, then optional chrM drop (`config.mito_name`, `keep_mito`); when `mito_name`/`raw_blacklist` set; consumed via `-L` by `bamtools_filter` |
| PRESEQ_LCEXTRAP | `qce::preseq_lcextrap` | preseq 3.1.2 | identical (`-verbose -bam -seed 1`; `-pe` when paired); when `skip_preseq = false` |
| PICARD_COLLECTMULTIPLEMETRICS | `qce::picard_collectmultiplemetrics` | picard 3.0.0 | identical (5 metrics + PDFs into `picard_metrics/{,pdf}/`); when `skip_picard_metrics = false` |
| GET_AUTOSOMES + ATAQV_ATAQV + ATAQV_MKARV | `qce::get_autosomes`, `qce::ataqv`, `qce::mkarv` | python 3.8.3, ataqv 1.3.1 | identical commands (`--ignore-read-groups`, mitochondrial-reference-name when `mito_name`; mkarv HTML index); when `skip_ataqv = false` |
| PLOT_MACS2_QC / PLOT_HOMER_ANNOTATEPEAKS | `qce::plot_macs2_qc` / `qce::plot_homer_annotatepeaks` | mulled R image | scripts copied verbatim from upstream `bin/`; when `skip_peak_qc = false` |
| MULTIQC_CUSTOM_PEAKS | `qce::multiqc_custom_peaks` | multiqc headers | identical count/FRiP TSVs (`assets/multiqc/` headers copied verbatim); when `multiqc_custom_peaks = true` (port-only switch; upstream always emits) |
| IGV | `qce::igv` | python 3.8.3 | `igv_files_to_session.py` copied verbatim, `--path_prefix '../../'`; when `skip_igv = false`; per-library tracks only (no merged-replicate sets, see below) |
| MACS2_CONSENSUS_PEAKS | `cons::macs2_consensus` | mulled (macs2 + bedtools + R) | `sort + mergeBed -c 2,3,4,5,6,7,8,9 -o collapse...` → `macs2_merged_expand.py --min_replicates` → BED/SAF/UpSet plot (bin scripts verbatim); when `skip_consensus_peaks = false`, needs ≥ 2 samples |
| SUBREAD_FEATURECOUNTS | `cons::subread_featurecounts` | subread 2.0.1 | identical (`-F SAF -O --fracOverlap 0.2 -s 0`, `-p` when paired); when `skip_consensus_peaks = false` |
| DESEQ2_QC | `cons::deseq2_qc` | mulled (R + DESeq2) | `deseq2_qc.r` verbatim (`--id_col 1 --count_col 7`, `--vst TRUE` when `deseq2_vst`); when `skip_consensus_peaks = false` and `skip_deseq2_qc = false` |
| PICARD_MERGESAMFILES / BAM_MARKDUPLICATES_PICARD / BAM_BEDGRAPH_BIGWIG_BEDTOOLS_UCSC / BAM_PEAKS_CALL_QC_ANNOTATE_MACS2_HOMER / BED_CONSENSUS_QUANTIFY_QC_BEDTOOLS_FEATURECOUNTS_DESEQ2 (aliased `MERGED_REPLICATE_*`) | `merge_replicates` + the same downstream rules | picard 3.0.0, samtools 1.17, macs2 2.2.7.1, homer 4.11, bedtools 2.30.0, deepTools 3.5.1 | **ported** via oxo-flow `input_groups`: `merge_replicates` folds per-replicate BAMs by base id (`_REP\d+$` suffix) and writes the merged BAM to the canonical `{sample}.mLb.clN.sorted.bam` path; the regular chain then runs on merged AND per-replicate inputs (same commands as upstream). when `skip_merge_replicates = false` (default); see "Merged-replicate analysis" below for semantics and deviations |
| INPUT_CHECK (samplesheet_check) | — | — | **not ported** — pipeline plumbing; oxo-flow provides native `[[sample_groups]]` declaration + `validate` |
| DUMP_SOFTWARE_VERSIONS | — | — | **not ported** — pipeline plumbing; oxo-flow has native version/audit mechanisms |
| PREPARE_GENOME: GFFREAD, GUNZIP, UNTAR, KHMER_UNIQUEKMERS | — | — | **not ported** — reference convenience layer; the port requires pre-built uncompressed GTF/BED/FASTA, unpacked index files and an explicit `macs_gsize` (upstream `prepare_genome.nf` auto-converts GFF3→GTF, decompresses `.gz`, unpacks index tarballs and estimates genome size via khmer) |

### Known divergences

- **Branches that upstream runs by default ship OFF here**: ataqv,
  Picard metrics, IGV, consensus peaks/DESeq2 and the R QC plots all run on
  the upstream default path; this port gates them behind
  `skip_ataqv`/`skip_picard_metrics`/`skip_igv`/`skip_consensus_peaks`/
  `skip_peak_qc` (default `true` = off) so the default plan stays the
  minimal main path. `skip_preseq = true` matches the upstream default
  (preseq is off there too). Enabling a branch is a single config flag.
- **Reference inputs**: upstream builds/derives the reference from
  `--genome` (iGenomes) at runtime; this port consumes pre-built files
  (`reference`, `bwa_index` prefix, `gtf`, `gene_bed`, `tss_bed`,
  `chrom_sizes`, optional `blacklist`). `prepare_reference = true` instead
  generates the BWA index and chrom sizes from the FASTA (the fixture
  already ships them, so the rules report up-to-date there).
- **ataqv and Picard metrics are SE-only**: both rules consume the
  single-end filtered `mLb.clN` BAM; the paired-end variants (over the
  `mLb.flT` orphan-removed BAM) are not ported — with `paired=true` the
  rules are skipped even when their `skip_*` gates are off.
- **Alternative aligners are single-end only** (`when` adds
  `!config.paired`): the paired branch is bwa-only, matching upstream's
  paired alignment options. Misconfigurations (e.g. `paired=true` with
  `aligner="star"`) surface as validation warnings via missing inputs.
- **PE requires `bwa_index` and produces `bwa/library/` outputs**: the
  paired branch's `bwa_mem_pe` emits the full read group
  (`-R '@RG\tID:{sample}\tSM:$SM\tPL:ILLUMINA\tLB:{sample}\tPU:1'`, where
  `SM` strips a `_T[0-9]*` suffix from the sample) rather than upstream's
  minimal `'@RG\tID:{sample}\tSM:{sample}'`; the default SE path keeps the
  original `@RG` handling.
- **Broad peaks are hardcoded**: the port's `macs2_callpeak` and all
  consumers use `--broad`; `narrow_peak = true` is honoured by
  `macs2_callpeak` but the downstream rules in this port read
  `*_peaks.broadPeak` only.
- **MultiQC config**: `path_filters`/`module_order` were trimmed to the
  ported steps; preseq/featureCounts/ataqv/DESeq2 sections appear when
  their branches are enabled (the PE MultiQC adds the PE fastqc/trimgalore
  logs). Report comment points at the upstream pipeline.
- **`macs_gsize`**: upstream derives it from the read length keyed genome
  block and auto-estimates via khmer when the value is empty; the port
  exposes it as `config.macs_gsize` (default `2.7e9`, the upstream
  GRCh37/38 @ 50 bp value — khmer auto-estimation is **not ported**, so
  non-human genomes must set this explicitly or the MACS2 commands run
  with the human genome size).
- **IGV session lists one merged `mLb_*` track set**: upstream separates
  per-replicate and merged-replicate bigWigs/peaks into two IGV track sets
  (`mLb_*` vs `mLb_clN_*`); this port's `igv` rule scans
  `merged_library/{bigwig,macs2/broad_peak}` once, so merged and
  per-replicate files land in the same set (the merged files are included
  when `config.merged_samples` names them).
- **featureCounts is unstranded**: `-s 0` is passed explicitly (the
  upstream default); a `[SCI-FEATURECOUNTS-STRAND]` preflight hint may
  appear for the gated rule — informational.
- **`size_factors/` stays in the workdir**: upstream DESeq2_QC publishes
  the `size_factors` directory; the port leaves it in the rule workdir
  (not declared as an output) — documented, not lost.
- **Legacy image pin**: `qce::multiqc_custom_peaks`
  (`modules/qc_extra.oxoflow`) still pins the retired
  `quay.io/nf-core/ubuntu:20.04` image (upstream's shell-only rule used a
  plain ubuntu container). It is kept as-is for byte-identical default
  behavior; the rule is gated off by default (`multiqc_custom_peaks =
  false`).
- **Dry-run prints benign `input ✗` lines on the default plan**:
  `{sample}.mLb.clN.sorted.bam` is declared as an output of both
  `bamtools_filter` (per-sample chain, runs) and `merge_replicates`
  (merged-replicate chain, off with the default empty `merged_samples`),
  so a dry-run with no files on disk reports that path unresolved for
  20 instances (per-sample consumers such as `macs2_callpeak`,
  `bedtools_genomecov`, `frip_score`, `plotfingerprint`, their transitive
  bigWig/peak consumers, and gated-off `pe::`/`qce::` copies).
  `oxo-flow dry-run` still exits 0; a real run resolves the files.
- **Consensus branch needs ≥ 2 samples**: upstream filters the peak
  channel to `size() > 1`; with one sample the consensus rules would
  produce degenerate output.

## Links

- Repository: [oxo-flow-atacseq](https://github.com/oxo-flow-community/oxo-flow-atacseq)
- Upstream: [nf-core/atacseq](https://github.com/nf-core/atacseq) @ `2.1.2`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
