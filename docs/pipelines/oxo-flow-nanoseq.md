---
title: "Nanopore long-read: demultiplexing, QC and alignment"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-nanoseq</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Nanopore long-read: demultiplexing, QC and alignment</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">nanopore</span><span class="ox-tag">long-read</span><span class="ox-tag">demultiplexing</span><span class="ox-tag">alignment</span><span class="ox-tag">qcat</span><span class="ox-tag">minimap2</span><span class="ox-tag">multiqc</span><span class="ox-tag">nf-core</span></div>
<p class="ox-desc">A nanopore long-read pipeline: samplesheet check, qcat barcode demultiplexing, NanoPlot + FastQC QC, minimap2 (or graphmap2) alignment, samtools view/sort/index, samtools stats/flagstat/idxstats, BigWig/BigBed tracks, NanoLyse contamination filtering, medaka/DeepVariant/PEPPER-Margin-DeepVariant short variant calling, Sniffles/cuteSV structural variant calling, bambu/StringTie2+featureCounts quantification with DESeq2/DEXSeq differential analysis, Nanopolish+xPore/m6anet RNA modification analysis, JAFFA RNA fusion detection (cDNA/directRNA; reference bundle auto-downloaded from figshare or supplied via config.jaffal_ref_dir as a directory or tar.gz), pre-aligned-BAM input, and a MultiQC report. The default path is the DNA protocol with all gated branches off by default (matching upstream). Every rule runs the upstream module&#x27;s exact pinned container image.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-nanoseq" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">52</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v"><span title="up to 12 CPUs / 84 GB per rule (minimap2 index)">up to 12 CPUs / 84 GB per rule (minimap2 index)</span></span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/nanoseq">nf-core/nanoseq</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>3.1.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2286.1"><code>10.48546/workflowhub.workflow.2286.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">bambu</span><span class="tchip">bcftools</span><span class="tchip">bedtools</span><span class="tchip">curl</span><span class="tchip">cutesv</span><span class="tchip">deepvariant</span><span class="tchip">deseq2</span><span class="tchip">dexseq</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-nanoseq</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Nanopore sequencing pipeline</strong> (nf-core/nanoseq port): given a raw Nanopore FASTQ and a reference genome, it demultiplexes, quality-checks, aligns, and aggregates a MultiQC report, with optional variant calling, transcript quantification, and RNA-modification analysis.</p>
<p><strong>1. Input preparation</strong> — <code>samplesheet_check</code> validates the samplesheet, then <code>qcat</code> demultiplexes the raw FASTQ; each detected barcode becomes the per-sample identity downstream.</p>
<p><strong>2. Reference prep</strong> — <code>samtools_faidx</code> indexes the reference, <code>get_chrom_sizes</code> derives chromosome sizes from it, and <code>gtf2bed</code> converts a GTF annotation to BED12 when supplied.</p>
<p><strong>3. Read QC</strong> — <code>nanoplot</code> and <code>fastqc</code> run in parallel on demultiplexed reads, each skippable.</p>
<p><strong>4. Alignment</strong> — <code>minimap2_index</code> → <code>minimap2_align</code> maps reads; with aligner = graphmap2, <code>graphmap2_index</code> → <code>graphmap2_align</code> runs instead — the two routes are mutually exclusive.</p>
<p><strong>5. BAM processing</strong> — both routes converge into <code>samtools_view</code>, then <code>samtools_sort</code> → <code>samtools_index</code> (or the combined <code>samtools_sort_index</code> under variant calling); <code>samtools_stats</code>, <code>samtools_flagstat</code>, <code>samtools_idxstats</code> run on the sorted BAM.</p>
<p><strong>6. Coverage tracks</strong> — <code>bedtools_genomecov</code> converts the BAM to BEDGraph, <code>ucsc_bedgraphtobigwig</code> to BigWig; on cDNA/directRNA protocols <code>bedtools_bamtobed</code> → <code>ucsc_bed12tobigbed</code> adds BigBed tracks.</p>
<p><strong>7. Variant calling (DNA, off by default)</strong> — short callers are mutually exclusive: <code>medaka_variant</code> → <code>medaka_bgzip_vcf</code> → <code>medaka_tabix_vcf</code>, <code>deepvariant</code> → <code>deepvariant_tabix_vcf</code> + <code>deepvariant_tabix_gvcf</code>, or <code>pepper_margin_deepvariant</code>; structural ones: <code>sniffles</code> → <code>sniffles_sort_vcf</code> → <code>sniffles_tabix_vcf</code> or <code>cutesv</code> → <code>cutesv_sort_vcf</code> → <code>cutesv_tabix_vcf</code>.</p>
<p><strong>8. Quantification (cDNA/directRNA)</strong> — <code>bambu</code> counts transcripts in one step, or <code>stringtie2</code> → <code>stringtie_merge</code> → <code>subread_featurecounts</code>; the routes are mutually exclusive, and counts feed <code>deseq2</code>/<code>dexseq</code> (bambu) or <code>deseq2_featurecounts</code>/<code>dexseq_featurecounts</code> (featureCounts).</p>
<p><strong>9. RNA modifications (directRNA)</strong> — <code>nanopolish_index_eventalign</code> event-aligns reads; <code>xpore_dataprep</code> → <code>xpore_diffmod</code> and <code>m6anet_dataprep</code> → <code>m6anet_inference</code> fan out in parallel.</p>
<p><strong>10. Reporting</strong> — <code>dumpsoftwareversions</code> merges tool versions; <code>multiqc</code> aggregates the FastQC and samtools results into one report.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-nanoseq+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-nanoseq
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-nanoseq` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-nanoseq@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-nanoseq` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Default path is the DNA protocol with all gated branches off (matching upstream); `protocol=cDNA skip_bigwig=true` switches to the transcriptome path (see README).

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker/Singularity) — pinned images

**Requirements.**

- genome FASTA reference (config.reference; defaults to test fixtures — override for real data)
- samplesheet CSV (config.input) plus raw nanopore FASTQ for demultiplexing (config.input_path; skip with skip_demultiplexing=true)
- optional GTF annotation (config.gtf + config.gtf_base) — only needed for the cDNA/directRNA junction-bed path
- compute: up to 12 CPUs / 84 GB RAM per rule (minimap2 index; most medium rules request 6 CPUs / 42 GB)
- container runtime (Docker or Singularity) — every rule pins its quay.io/biocontainers image

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-nanoseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-nanoseq
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy aligner = value" data-copy="aligner = minimap2">aligner</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>minimap2</code></td>
<td class="ox-p-desc">-- Alignment<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bam_suffix = value" data-copy="bam_suffix = .sorted.bam">bam_suffix</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>.sorted.bam</code></td>
<td class="ox-p-desc">-- Suffix appended to per-sample bam names wherever rules consume reads:<br>&quot;.sorted.bam&quot; (alignment branch) or &quot;.bam&quot; (skip_alignment branch,<br>user bams linked by bam_rename). Mirrors the upstream channel swap<br>between BAM_SORT_INDEX_SAMTOOLS.out.sortbam and BAM_RENAME.out.bam.<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy barcode_kit = value" data-copy="barcode_kit = RBK001">barcode_kit</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>RBK001</code></td>
<td class="ox-p-desc">-- Demultiplexing (upstream defaults)<br>RBK001 matches the shipped barcoded fixture (qcat Auto-detection needs<br>at least two distinct barcodes to guess the kit; the explicit kit makes<br>the test path deterministic).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy call_variants = value" data-copy="call_variants = false">call_variants</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>17</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy deepvariant_gpu = value" data-copy="deepvariant_gpu = false">deepvariant_gpu</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf = value" data-copy="gtf = ">gtf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">-- GTF annotation (upstream samplesheet gtf column; empty on the default path)<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_base = value" data-copy="gtf_base = ">gtf_base</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">-- GTF annotation (upstream samplesheet gtf column; empty on the default path)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy input = value" data-copy="input = test/fixtures/samplesheet.csv">input</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/samplesheet.csv</code></td>
<td class="ox-p-desc">-- Samplesheet and demultiplexing input (upstream: --input / --input_path)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy input_path = value" data-copy="input_path = test/fixtures/raw/sample.fastq.gz">input_path</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/raw/sample.fastq.gz</code></td>
<td class="ox-p-desc">-- Samplesheet and demultiplexing input (upstream: --input / --input_path)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy multiqc_config = value" data-copy="multiqc_config = ">multiqc_config</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">-- MultiQC options<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy multiqc_title = value" data-copy="multiqc_title = ">multiqc_title</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">-- MultiQC options<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nanolyse_fasta = value" data-copy="nanolyse_fasta = test/fixtures/refs/lambda.fasta.gz">nanolyse_fasta</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/lambda.fasta.gz</code></td>
<td class="ox-p-desc">-- Raw read cleaning (upstream default: off). Upstream downloads the<br>lambda genome when --nanolyse_fasta is unset (GET_NANOLYSE_FASTA);<br>the port ships it as a checked-in fixture.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nanopolish_fast5 = value" data-copy="nanopolish_fast5 = ">nanopolish_fast5</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">-- RNA modification analysis (upstream default: on, gated to protocol<br>directRNA; the fast5 dir comes from the upstream samplesheet<br>nanopolish_fast5 column — the port takes one dir for all samples)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">-- Output directory (upstream: --outdir, default ./results)<br><span class="ox-param-usedby">used by <code>52</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy phase_vcf = value" data-copy="phase_vcf = false">phase_vcf</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy protocol = value" data-copy="protocol = DNA">protocol</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>DNA</code></td>
<td class="ox-p-desc">-- Protocol (upstream: --protocol; mandatory upstream, one of DNA/cDNA/directRNA)<br><span class="ox-param-usedby">used by <code>32</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qcat_detect_middle = value" data-copy="qcat_detect_middle = false">qcat_detect_middle</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Demultiplexing (upstream defaults)<br>RBK001 matches the shipped barcoded fixture (qcat Auto-detection needs<br>at least two distinct barcodes to guess the kit; the explicit kit makes<br>the test path deterministic).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qcat_min_score = value" data-copy="qcat_min_score = 60">qcat_min_score</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>60</code></td>
<td class="ox-p-desc">-- Demultiplexing (upstream defaults)<br>RBK001 matches the shipped barcoded fixture (qcat Auto-detection needs<br>at least two distinct barcodes to guess the kit; the explicit kit makes<br>the test path deterministic).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy quantification_method = value" data-copy="quantification_method = bambu">quantification_method</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>bambu</code></td>
<td class="ox-p-desc">-- Quantification and differential analysis (upstream defaults: on, but<br>gated upstream to protocol cDNA/directRNA — never on the DNA path)<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference = value" data-copy="reference = test/fixtures/refs/genome.fa">reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/genome.fa</code></td>
<td class="ox-p-desc">-- Reference genome (collapses the samplesheet fasta column; the default<br>path uses a single reference for all samples, as in the upstream test data)<br><span class="ox-param-usedby">used by <code>14</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference_name = value" data-copy="reference_name = genome.fa">reference_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>genome.fa</code></td>
<td class="ox-p-desc">Basename of the reference; mirrors the upstream staged-file name so that<br>indexes keep the upstream naming (genome.fa.mmi / genome.fa.sizes / genome.fa.fai)<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_nanolyse = value" data-copy="run_nanolyse = false">run_nanolyse</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Raw read cleaning (upstream default: off). Upstream downloads the<br>lambda genome when --nanolyse_fasta is unset (GET_NANOLYSE_FASTA);<br>the port ships it as a checked-in fixture.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sample_bams = value" data-copy="sample_bams = ">sample_bams</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">-- Pre-aligned BAM input (upstream: the samplesheet input_file column<br>carrying .bam files, used only when --skip_alignment; the port takes a<br>comma-separated list of bam paths, one per barcode in samples_list<br>order, linked by the bam_rename rule)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_alignment = value" data-copy="skip_alignment = false">skip_alignment</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Alignment<br><span class="ox-param-usedby">used by <code>18</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_bigbed = value" data-copy="skip_bigbed = false">skip_bigbed</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Visualisation (upstream defaults: bigwig/bigbed ON; bigbed is<br>protocol-gated upstream to cDNA/directRNA and so never runs on the<br>default DNA path)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_bigwig = value" data-copy="skip_bigwig = false">skip_bigwig</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Visualisation (upstream defaults: bigwig/bigbed ON; bigbed is<br>protocol-gated upstream to cDNA/directRNA and so never runs on the<br>default DNA path)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_demultiplexing = value" data-copy="skip_demultiplexing = false">skip_demultiplexing</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Demultiplexing (upstream defaults)<br>RBK001 matches the shipped barcoded fixture (qcat Auto-detection needs<br>at least two distinct barcodes to guess the kit; the explicit kit makes<br>the test path deterministic).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_differential_analysis = value" data-copy="skip_differential_analysis = false">skip_differential_analysis</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Quantification and differential analysis (upstream defaults: on, but<br>gated upstream to protocol cDNA/directRNA — never on the DNA path)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastqc = value" data-copy="skip_fastqc = false">skip_fastqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- QC (upstream defaults: all QC on)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_m6anet = value" data-copy="skip_m6anet = false">skip_m6anet</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- RNA modification analysis (upstream default: on, gated to protocol<br>directRNA; the fast5 dir comes from the upstream samplesheet<br>nanopolish_fast5 column — the port takes one dir for all samples)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_modification_analysis = value" data-copy="skip_modification_analysis = false">skip_modification_analysis</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- RNA modification analysis (upstream default: on, gated to protocol<br>directRNA; the fast5 dir comes from the upstream samplesheet<br>nanopolish_fast5 column — the port takes one dir for all samples)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_multiqc = value" data-copy="skip_multiqc = false">skip_multiqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- QC (upstream defaults: all QC on)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_nanoplot = value" data-copy="skip_nanoplot = false">skip_nanoplot</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- QC (upstream defaults: all QC on)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_qc = value" data-copy="skip_qc = false">skip_qc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- QC (upstream defaults: all QC on)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_quantification = value" data-copy="skip_quantification = false">skip_quantification</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Quantification and differential analysis (upstream defaults: on, but<br>gated upstream to protocol cDNA/directRNA — never on the DNA path)<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_sv = value" data-copy="skip_sv = false">skip_sv</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_vc = value" data-copy="skip_vc = false">skip_vc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_xpore = value" data-copy="skip_xpore = false">skip_xpore</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- RNA modification analysis (upstream default: on, gated to protocol<br>directRNA; the fast5 dir comes from the upstream samplesheet<br>nanopolish_fast5 column — the port takes one dir for all samples)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy split_mnps = value" data-copy="split_mnps = false">split_mnps</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy stranded = value" data-copy="stranded = false">stranded</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">-- Alignment<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy structural_variant_caller = value" data-copy="structural_variant_caller = sniffles">structural_variant_caller</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>sniffles</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy variant_caller = value" data-copy="variant_caller = medaka">variant_caller</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>medaka</code></td>
<td class="ox-p-desc">-- Variant calling (upstream default: off; also gated upstream on<br>protocol == DNA). The three short-variant callers are mutually<br>exclusive on variant_caller; structural callers on<br>structural_variant_caller (upstream defaults: medaka / sniffles).<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-nanoseq-rules.svg?v=72a3eb250c" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-nanoseq-rules.svg?v=72a3eb250c" alt="oxo-flow-nanoseq rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card ox-dag-card--wide" markdown="1">

<a href="/assets/dag/oxo-flow-nanoseq.svg?v=09aa42dfd3" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-nanoseq.svg?v=09aa42dfd3" alt="oxo-flow-nanoseq pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-nanoseq — A nanopore long-read pipeline: samplesheet check, qcat barcode demultiplexing, NanoPlot + FastQC QC, minimap2 (or graphmap2) alignment, samtools view/sort/index, samtools stats/flagstat/idxstats, BigWig/BigBed tracks, NanoLyse contamination filtering, medaka/DeepVariant/PEPPER-Margin-DeepVariant short variant calling, Sniffles/cuteSV structural variant calling, bambu/StringTie2+featureCounts quantification with DESeq2/DEXSeq differential analysis, Nanopolish+xPore/m6anet RNA modification analysis, JAFFA RNA fusion detection (cDNA/directRNA; reference bundle auto-downloaded from figshare or supplied via config.jaffal_ref_dir as a directory or tar.gz), pre-aligned-BAM input, and a MultiQC report.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- samplesheet_check
- qcat
- nanoplot
- fastqc
- get_chrom_sizes
- samtools_faidx
- gtf2bed
- minimap2_index
- minimap2_align
- samtools_view
- samtools_sort
- samtools_index
- samtools_stats
- samtools_idxstats
- samtools_flagstat
- bedtools_genomecov
- ucsc_bedgraphtobigwig
- dumpsoftwareversions
- multiqc
- nanolyse
- graphmap2_index
- graphmap2_align
- samtools_sort_index
- bam_rename
- bedtools_bamtobed
- ucsc_bed12tobigbed
- medaka_variant
- medaka_bgzip_vcf
- medaka_tabix_vcf
- deepvariant
- deepvariant_tabix_vcf
- deepvariant_tabix_gvcf
- pepper_margin_deepvariant
- sniffles
- sniffles_sort_vcf
- sniffles_tabix_vcf
- cutesv
- cutesv_sort_vcf
- cutesv_tabix_vcf
- bambu
- stringtie2
- stringtie_merge
- subread_featurecounts
- deseq2
- deseq2_featurecounts
- dexseq
- dexseq_featurecounts
- nanopolish_index_eventalign
- xpore_dataprep
- xpore_diffmod
- m6anet_dataprep
- m6anet_inference
- get_jaffal_ref
- jaffal_ref

**Excluded**

- none

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- note: committee scope mentions Dorado demultiplex + pycoQC QC; nanoseq 3.1.0 actually uses qcat + NanoPlot/FastQC — port follows the real source

## Fidelity

Port scope: the **default-parameters main execution path** (`protocol = DNA`, demultiplexing on, minimap2 aligner, all QC/bigwig/reporting on) plus **every gated branch** of the upstream workflow, ported as `when`-gated rules and all off by default (matching upstream). Commands mirror the upstream modules byte-for-byte under each branch's parameters; upstream Groovy `params.*` conditionals are reproduced as bash conditionals over the same config keys.

### Default path (DNA, minimap2, demultiplexing on)

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| SAMPLESHEET_CHECK | `samplesheet_check` | python 3.8.3 | identical command (`check_samplesheet.py`, `not_changed` path arg) |
| QCAT | `qcat` | qcat 1.1.0 | identical command (`-f`, `-b`, `--kit`, `--min-score`, zcat preamble, gzip); runs once on `input_path`. Declared outputs are the ported barcode set `barcode01/02` (upstream emits `fastq/*.fastq.gz` dynamically) |
| NANOPLOT | `nanoplot` | NanoPlot 1.41.0 | identical command (`-t N --fastq`); upstream publishes all samples' fixed-named `NanoPlot-report.html` into one dir (silently clobbering) — the port isolates each sample in `nanoplot/<barcode>/` |
| FASTQC | `fastqc` | fastqc 0.11.9 | identical command incl. the symlink-rename preamble; per-sample `<barcode>_fastqc.{html,zip}` |
| GET_CHROM_SIZES | `get_chrom_sizes` | samtools 1.13 | identical (`samtools faidx` + `cut -f 1,2`); upstream conda pin says samtools=1.10, container is 1.13 — port pins the container tag |
| SAMTOOLS_FAIDX | `samtools_faidx` | samtools 1.16.1 | identical (`samtools faidx`); runs on a local copy of the reference like the upstream workdir staging |
| GTF2BED | `gtf2bed` | perl 5.26.2 | identical (`gtf2bed <gtf> > <name>.bed`); **off on the default path** — upstream only runs it when the samplesheet carries a gtf column (`when = config.gtf != ""`) |
| MINIMAP2_INDEX | `minimap2_index` | minimap2 2.17 | identical flags for default params (`-ax map-ont -t 12 -d <fasta>.mmi`); protocol/stranded/junction conditionals preserved |
| MINIMAP2_ALIGN | `minimap2_align` | minimap2 2.17 | identical flags + `> <sample>.sam`; `--MD` conditional preserved (off by default) |
| SAMTOOLS_VIEW_BAM | `samtools_view` | samtools 1.15.1 | identical (`view -b -h -O BAM -@ N -o`) |
| SAMTOOLS_SORT | `samtools_sort` | samtools 1.16.1 | identical minus `-m 512M` capped per-thread sort buffer (added to prevent OOM on large BAMs) |
| SAMTOOLS_INDEX | `samtools_index` | samtools 1.16.1 | identical (`index -@ N-1`) |
| SAMTOOLS_STATS | `samtools_stats` | samtools 1.16.1 | identical (`stats --threads N --reference <fasta>`) |
| SAMTOOLS_IDXSTATS | `samtools_idxstats` | samtools 1.16.1 | identical (`idxstats --threads N-1`) |
| SAMTOOLS_FLAGSTAT | `samtools_flagstat` | samtools 1.16.1 | identical (`flagstat --threads N`) |
| BEDTOOLS_GENOMECOV | `bedtools_genomecov` | bedtools 2.29.2 | identical (`genomecov -split -ibam -bg \| bedtools sort`; upstream hardcodes `-split`) |
| UCSC_BEDGRAPHTOBIGWIG | `ucsc_bedgraphtobigwig` | ucsc-bedgraphtobigwig 377 | identical (`bedGraphToBigWig <bedgraph> <sizes>`) |
| CUSTOM_DUMPSOFTWAREVERSIONS | `dumpsoftwareversions` | python (multiqc 1.13 image) | upstream merges per-process `versions.yml` collected at run time; the port pins the same versions statically in `assets/versions.yml` (values = container tags) and runs the upstream merge script verbatim |
| MULTIQC | `multiqc` | multiqc 1.11 | identical (`multiqc -f .` on a dir with config + report inputs); `--title`/`--config` conditionals preserved; output at `results/multiqc/minimap2/` matching the upstream publishDir path |

Deviation (identity model, see also `main.oxoflow` header): upstream
demultiplexes the raw fastq into **barcode-named** files and then joins them
onto samplesheet rows by barcode, so downstream artifacts are named
`<group>_R<replicate>.bam` etc. oxo-flow has no channel join, so the port
keys all per-sample rules by the barcode itself — outputs are named
`barcode01.sam`, `barcode01.bam`, `barcode01.bigWig`, ... while keeping every
command and intermediate filename upstream-identical. The samplesheet
fixture maps barcodes `01`/`02` exactly like the upstream test data.

### Gated branches (all off by default, matching upstream defaults)

| Upstream process/rule | oxo-flow rule | Tool (version) | Gate / notes |
|---|---|---|---|
| NANOLYSE | `nanolyse` | NanoLyse 1.2.0 | `run_nanolyse`; reference = checked-in `test/fixtures/refs/lambda.fasta.gz` (upstream downloads it via GET_NANOLYSE_FASTA) |
| GRAPHMAP2_INDEX | `graphmap2_index` | graphmap 0.6.3 | `aligner == "graphmap2"`; `-x rnaseq`/`--gtf` conditionals preserved (non-DNA protocols) |
| GRAPHMAP2_ALIGN | `graphmap2_align` | graphmap 0.6.3 | same gate; `--extcigar` |
| SAMTOOLS_SORT_INDEX | `samtools_sort_index` | samtools 1.16.1 | `call_variants` — combined sort+index instead of the separate rules in the VC branch |
| MEDAKA_VARIANT | `medaka_variant` | medaka 1.4.4 | `call_variants && protocol == DNA && !skip_vc && variant_caller == "medaka"`; `-d -f -i -o -t` + `split_mnps`/`phase_vcf` flags |
| TABIX_BGZIP / TABIX_TABIX (as MEDAKA_BGZIP_VCF / MEDAKA_TABIX_VCF) | `medaka_bgzip_vcf` / `medaka_tabix_vcf` | tabix 1.11 | same gate |
| DEEPVARIANT | `deepvariant` | google/deepvariant 1.4.0 | `variant_caller == "deepvariant"`; docker-only upstream; `--model_type WGS --num_shards=N` |
| DEEPVARIANT_TABIX_VCF / DEEPVARIANT_TABIX_GVCF | `deepvariant_tabix_vcf` / `deepvariant_tabix_gvcf` | tabix 1.11 | same gate |
| PEPPER_MARGIN_DEEPVARIANT | `pepper_margin_deepvariant` | kishwars/pepper_deepvariant r0.8 | `variant_caller == "pepper_margin_deepvariant"`; `-g` honored via `deepvariant_gpu` (CPU image pinned, see Deviations) |
| SNIFFLES | `sniffles` | sniffles 1.0.12 | `call_variants && protocol == DNA && !skip_sv && structural_variant_caller == "sniffles"`; `-m -v -t` |
| BCFTOOLS_SORT / TABIX_TABIX (as SNIFFLES_SORT_VCF / SNIFFLES_TABIX_VCF) | `sniffles_sort_vcf` / `sniffles_tabix_vcf` | bcftools 1.16 / tabix 1.11 | same gate |
| CUTESV | `cutesv` | cutesv 1.0.12 | `structural_variant_caller == "cutesv"`; `cuteSV bam fasta vcf . --threads --sample --genotype` |
| BCFTOOLS_SORT / TABIX_TABIX (as CUTESV_SORT_VCF / CUTESV_TABIX_VCF) | `cutesv_sort_vcf` / `cutesv_tabix_vcf` | bcftools 1.16 / tabix 1.11 | same gate |
| BEDTOOLS_BAMBED | `bedtools_bamtobed` | bedtools 2.29.2 | `!skip_bigbed && protocol cDNA/directRNA` (upstream module `when` — never on the DNA path) |
| UCSC_BED12TOBIGBED | `ucsc_bed12tobigbed` | ucsc-bedtobigbed 377 | same gate |
| BAMBU | `bambu` | bioconductor-bambu 3.0.8 | `protocol != DNA && !skip_quantification && quantification_method == "bambu"`; gathers all sample BAMs via expand_inputs; upstream `bin/run_bambu.r` verbatim |
| STRINGTIE2 | `stringtie2` | stringtie 2.1.4 | `quantification_method == "stringtie2"`; `-L -G <gtf> -o <s>.stringtie.gtf` |
| STRINGTIE_MERGE | `stringtie_merge` | stringtie 2.2.1 | same gate; gathers per-sample assemblies, `-G` reference GTF conditional preserved |
| SUBREAD_FEATURECOUNTS | `subread_featurecounts` | subread 2.0.1 | same gate; gene counts + transcript counts, `-L -O --primary --fraction` |
| DESEQ2 | `deseq2` (bambu counts) / `deseq2_featurecounts` (featureCounts counts) | mulled-v2-8849acf3… (bioconductor-deseq2) | `!skip_differential_analysis`; mutually exclusive on `quantification_method`; upstream `bin/run_deseq2.r` verbatim; results under `results/bambu/deseq2/` (upstream publishDir quirk kept) |
| DEXSEQ | `dexseq` (bambu counts) / `dexseq_featurecounts` (featureCounts counts) | docker.io/yuukiiwa/nanoseq:dexseq | same gates; upstream `bin/run_dexseq.r` verbatim |
| NANOPOLISH_INDEX_EVENTALIGN | `nanopolish_index_eventalign` | nanopolish 0.13.2 | `protocol == directRNA && !skip_modification_analysis && nanopolish_fast5 != ""`; `nanopolish index -d <fast5>` + `eventalign --scale-events --signal-index` |
| XPORE_DATAPREP | `xpore_dataprep` | xpore 2.1 | `!skip_xpore` (same branch gate); `--genome --gtf_or_gff --transcript_fasta` |
| XPORE_DIFFMOD | `xpore_diffmod` | xpore 2.1 | same gate; upstream `bin/create_yml.py` verbatim |
| M6ANET_DATAPREP | `m6anet_dataprep` | docker.io/yuukiiwa/m6anet:1.0 | `!skip_m6anet` (same branch gate) |
| M6ANET_INFERENCE | `m6anet_inference` | docker.io/yuukiiwa/m6anet:1.0 | same gate; `--batch_size 512 --num_iterations 5 --device cpu` |
| BAM_RENAME | `bam_rename` | sed 4.7.0 (shell-only container) | `skip_alignment && sample_bams != ""`; comma-separated `sample_bams` split via expand_inputs and linked to the barcode names, `[ ! -f ] && ln -s` like upstream |

Not ported (remainder):

| Upstream step | Reason |
|---|---|
| JAFFAL / GET_JAFFAL_REF / UNTAR (RNA fusion, `protocol` cDNA/directRNA) | not portable: the JAFFA reference bundle (`https://ndownloader.figshare.com/files/28168755`) redirects to a signed S3 URL that returns **HTTP 403** (verified 2026-08), is multi-GB, and embeds the `JAFFA_stages.groovy` script the module executes via `bpipe run` — the process cannot run without the bundle |
| GET_TEST_DATA / GET_NANOLYSE_FASTA (upstream download processes) | GET_TEST_DATA is nf-core `-profile test` infrastructure (clones `nf-core/test-datasets`); GET_NANOLYSE_FASTA fetches the lambda genome whenever `run_nanolyse=true` without `--nanolyse_fasta` (any profile). Both are replaced by checked-in fixtures — the nanolyse reference ships as `test/fixtures/refs/lambda.fasta.gz` |
| `-profile test*` configs, cluster/container profiles, Tower reporting, completion email | nf-core infrastructure, out of port scope |

Deviations (see README): (1) NanoLyse cannot reassign the reads channel — filtered reads land in `results/nanolyse/`, the downstream chain keeps the demultiplexed reads; (2) graphmap2 outputs publish under `results/minimap2/` so the shared downstream chain needs no duplicate rules; (3) `bam_suffix` lets the quantification/modification rules target either naming scheme (alignment vs `skip_alignment`); (4) DESEQ2/DEXSEQ come as two rules per tool with the same output path, mutually exclusive on `quantification_method`; (5) `nanopolish_fast5` takes one directory, guarded by a `!= ""` gate; (6) pepper pins the CPU image (swap + `deepvariant_gpu = true` for GPU); (7) `-m 512M` caps the samtools sort buffer; (8) `assets/versions.yml` pins the default-path tool versions statically; (9) MultiQC cannot aggregate featureCounts `.summary` files (excluded from the report); (10) the samplesheet `is_transcripts` column is not ported (barcode-identity model; non-DNA default applies).

Live verification (tx-ubuntu, oxo-flow 0.15.0): default path, call_variants (medaka), structural_variant_caller (sniffles/cutesv) and the nanolyse branch PASS; cDNA/directRNA quantification tool-execution verified (mini-fixture reads lie off the annotated region — documented).

## Links

- Repository: [oxo-flow-nanoseq](https://github.com/oxo-flow-community/oxo-flow-nanoseq)
- Upstream: [nf-core/nanoseq](https://github.com/nf-core/nanoseq) @ `3.1.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
