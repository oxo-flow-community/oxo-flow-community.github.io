---
title: "Paired-end RNA-seq alignment and four-caller alternative-splicing analysis"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-tcasia</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Paired-end RNA-seq alignment and four-caller alternative-splicing analysis</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · full-line</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">alternative-splicing</span><span class="ox-tag">rna-seq</span><span class="ox-tag">rmats</span><span class="ox-tag">majiq</span><span class="ox-tag">suppa2</span><span class="ox-tag">spladder</span><span class="ox-tag">star</span><span class="ox-tag">snakemake</span></div>
<p class="ox-desc">Paired-end RNA-seq from FASTQ to per-sample alternative-splicing calls: reads are trimmed with fastp, aligned with two-pass STAR and counted per gene with featureCounts; each sample&#x27;s splicing is then quantified independently with four callers — rMATS, MAJIQ (with Voila export), SUPPA2 (via Salmon transcript quantification) and SplAdder. The alignment and AS-calling stages are one chained DAG (run one stage with -t alignment / -t as_calling).</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-tcasia" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · full-line</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">17</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 10 threads per rule (STAR / rMATS)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">transcriptomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/OncoHarmony-Network/TCASIA_pipeline">OncoHarmony-Network/TCASIA_pipeline</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>main@06564ff1</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2301.1"><code>10.48546/workflowhub.workflow.2301.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastp</span><span class="tchip">star</span><span class="tchip">samtools</span><span class="tchip">subread</span><span class="tchip">salmon</span><span class="tchip">suppa</span><span class="tchip">rmats</span><span class="tchip">majiq</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>TCASIA alternative-splicing pipeline</strong>: given paired-end RNA-seq reads and a reference genome, it quality-filters and aligns them, then quantifies alternative splicing with four callers — rMATS, MAJIQ, SUPPA2 and SplAdder — each producing per-event PSI output.</p>
<p><strong>1. Input QC and alignment</strong> — <code>alignment::fastp_qc</code> trims and quality-filters the paired reads; <code>alignment::star_align</code> runs the two-pass STAR alignment with gene counts; <code>alignment::sort_bam</code> coordinate-sorts the BAM. From that sorted BAM, <code>alignment::index_bam</code> builds the BAI index and <code>alignment::featurecounts</code> counts reads per gene — and the same sorted BAM feeds every alternative-splicing caller downstream.</p>
<p><strong>2. SUPPA2 track (from raw reads, runs in parallel)</strong> — <code>as_calling::salmon_quant</code> quantifies transcripts directly from raw FASTQ; <code>as_calling::select_suppa_fields</code> extracts the isoform TPM column; <code>as_calling::format_suppa_fields</code> strips the transcript prefix; <code>as_calling::suppa_run</code> computes per-event PSI.</p>
<p><strong>3. rMATS</strong> — <code>as_calling::rmats_create_input</code> writes the single-BAM input list, then <code>as_calling::rmats_run</code> computes PSI values per sample.</p>
<p><strong>4. MAJIQ (gated on the run_majiq flag; the academic license is required)</strong> — <code>as_calling::majiq_create_ini</code> writes the build configuration, <code>as_calling::majiq_build</code> builds the splice graph, <code>as_calling::majiq_psi</code> quantifies PSI per local splicing variation; then both <code>as_calling::voila_modulize</code> (Voilà modules) and <code>as_calling::voila_tsv</code> (TSV table) consume the splice graph and PSI outputs.</p>
<p><strong>5. SplAdder</strong> — <code>as_calling::spladder_run</code> detects alternative-splicing events directly from the sorted BAM.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-tcasia+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>


<div class="ox-tryit">
<div class="ox-tryit-title">⬡ Try it — clone &amp; run</div>
<pre class="ox-tryit-cmd" data-copy="git clone https://github.com/oxo-flow-community/oxo-flow-tcasia.git &amp;&amp; cd oxo-flow-tcasia &amp;&amp; oxo-flow run main.oxoflow">git clone https://github.com/oxo-flow-community/oxo-flow-tcasia.git
cd oxo-flow-tcasia
oxo-flow run main.oxoflow</pre>
<p class="ox-tryit-note">The repository ships test fixtures (e.g. <code>test/fixtures/raw/sample_01_1.fastq.gz</code>, <code>test/fixtures/raw/sample_01_2.fastq.gz</code>, <code>test/fixtures/raw/sample_02_1.fastq.gz</code>, <code>test/fixtures/raw/sample_02_2.fastq.gz</code>) — point <code>input</code> at them or use the built-in sample group to <code>dry-run</code> first.</p>
</div>


## Run it

```bash
oxo-flow run main.oxoflow
```

Needs raw FASTQs and reference data — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.14.0

**Toolchain.** conda envs — pinned versions (fastp 0.23.4, STAR 2.7.7a, samtools 1.13/1.15, subread 2.0.1, salmon 1.10.3, suppa 2.3, rMATS 4.3.0, MAJIQ 2.5, SplAdder 3.1.1; conda-forge + bioconda)

**Requirements.**

- reference data (GRCh38 + GENCODE v34): STAR index (STAR 2.7.7a), annotation GTF + GFF3, Salmon transcript index, SUPPA2 events file, MAJIQ academic license
- paired-end reads at reads_dir/<sample>_1.fastq.gz / <sample>_2.fastq.gz for each sample in the [[sample_groups]] list
- compute: up to 10 threads per rule (STAR/rMATS), no memory limits set
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
oxo-flow pull gh:oxo-flow-community/oxo-flow-tcasia
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-tcasia
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy align_out_dir = value" data-copy="align_out_dir = results/alignment">align_out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results/alignment</code></td>
<td class="ox-p-desc">01_alignment (upstream config.yml)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy aligned_dir = value" data-copy="aligned_dir = results/alignment/aligned">aligned_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results/alignment/aligned</code></td>
<td class="ox-p-desc">upstream: 01 output_dir/aligned == 02 bam_dir<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy as_out_dir = value" data-copy="as_out_dir = results/as_calling">as_out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results/as_calling</code></td>
<td class="ox-p-desc">02_as_calling (upstream config.yml)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fastp_min_length = value" data-copy="fastp_min_length = 36">fastp_min_length</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>36</code></td>
<td class="ox-p-desc">fastp (upstream fastp.*)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fastp_n_base_limit = value" data-copy="fastp_n_base_limit = 5">fastp_n_base_limit</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">fastp (upstream fastp.*)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fastp_qualified_quality_phred = value" data-copy="fastp_qualified_quality_phred = 20">fastp_qualified_quality_phred</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>20</code></td>
<td class="ox-p-desc">fastp (upstream fastp.*)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fastp_unqualified_percent_limit = value" data-copy="fastp_unqualified_percent_limit = 40">fastp_unqualified_percent_limit</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>40</code></td>
<td class="ox-p-desc">fastp (upstream fastp.*)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gff = value" data-copy="gff = test/fixtures/reference/genes.gff3">gff</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reference/genes.gff3</code></td>
<td class="ox-p-desc">upstream: GFF (tiny synthetic)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy majiq_genome = value" data-copy="majiq_genome = hg38">majiq_genome</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>hg38</code></td>
<td class="ox-p-desc">majiq tool parameter (upstream --majiq_genome) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy majiq_license = value" data-copy="majiq_license = test/fixtures/reference/majiq_license.lic">majiq_license</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reference/majiq_license.lic</code></td>
<td class="ox-p-desc">MAJIQ requires the upstream academic license file — place it at<br>test/fixtures/reference/majiq_license.lic (obtain from MAJIQ) and set<br>run_majiq = true. Upstream fails hard without the license; the port<br>gates the whole MAJIQ chain on this flag instead (documented in the<br>README fidelity table).<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy majiq_minreads = value" data-copy="majiq_minreads = 10">majiq_minreads</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10</code></td>
<td class="ox-p-desc">majiq tool parameter (upstream --majiq_minreads) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy majiq_strandness = value" data-copy="majiq_strandness = reverse">majiq_strandness</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>reverse</code></td>
<td class="ox-p-desc">fr-firststrand -&gt; reverse | fr-secondstrand -&gt; forward | fr-unstranded -&gt; none<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy read_len = value" data-copy="read_len = 150">read_len</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>150</code></td>
<td class="ox-p-desc">salmon_index is auto-built below from the shipped transcripts.fa<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reads_dir = value" data-copy="reads_dir = test/fixtures/raw">reads_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/raw</code></td>
<td class="ox-p-desc">point at your own fastq directory for real runs<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ref = value" data-copy="ref = test/fixtures/reference/genes.gtf">ref</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reference/genes.gtf</code></td>
<td class="ox-p-desc">featureCounts / rMATS / SplAdder annotation (tiny synthetic; GRCh38 GTF for real runs)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rmats_cstat = value" data-copy="rmats_cstat = 0.0001">rmats_cstat</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.0001</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rmats_extra = value" data-copy="rmats_extra = ">rmats_extra</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_majiq = value" data-copy="run_majiq = false">run_majiq</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">MAJIQ requires the upstream academic license file — place it at<br>test/fixtures/reference/majiq_license.lic (obtain from MAJIQ) and set<br>run_majiq = true. Upstream fails hard without the license; the port<br>gates the whole MAJIQ chain on this flag instead (documented in the<br>README fidelity table).<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy salmon_index = value" data-copy="salmon_index = test/fixtures/reference/salmon_index">salmon_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reference/salmon_index</code></td>
<td class="ox-p-desc">salmon_index is auto-built below from the shipped transcripts.fa<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy salmon_library_type = value" data-copy="salmon_library_type = ISR">salmon_library_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>ISR</code></td>
<td class="ox-p-desc">Derived from <code>strandness</code> by upstream tcasia_config.py; kept explicit here:<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy spladder_confidence = value" data-copy="spladder_confidence = 3">spladder_confidence</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>3</code></td>
<td class="ox-p-desc">spladder tool parameter (upstream --spladder_confidence) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy spladder_event_types = value" data-copy="spladder_event_types = exon_skip,intron_retention,alt_3prime,alt_5prime,mutex_exons">spladder_event_types</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>exon_skip,intron_retention,alt_3prime,alt_5prime,mutex_exons</code></td>
<td class="ox-p-desc">spladder tool parameter (upstream --spladder_event_types) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy spladder_merge_strategy = value" data-copy="spladder_merge_strategy = single">spladder_merge_strategy</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>single</code></td>
<td class="ox-p-desc">spladder tool parameter (upstream --spladder_merge_strategy) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_index_dir = value" data-copy="star_index_dir = test/fixtures/reference/STAR_index">star_index_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reference/STAR_index</code></td>
<td class="ox-p-desc">star_index_dir is auto-built below from test/fixtures/reference (tiny<br>synthetic genome) — point it at a real GRCh38 STAR index for real runs.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_limit_bam_sort_ram = value" data-copy="star_limit_bam_sort_ram = 0">star_limit_bam_sort_ram</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">0 = auto: the machine-effective memory (clamped declared value)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_out_filter_mismatch_nmax = value" data-copy="star_out_filter_mismatch_nmax = 15">star_out_filter_mismatch_nmax</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">STAR (upstream star.*)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy strandness = value" data-copy="strandness = fr-firststrand">strandness</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>fr-firststrand</code></td>
<td class="ox-p-desc">shared<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy suppa2_events = value" data-copy="suppa2_events = test/fixtures/reference/events.ioe">suppa2_events</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reference/events.ioe</code></td>
<td class="ox-p-desc">suppa2_events is auto-built below from the shipped GTF (SUPPA2 generateEvents)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy suppa2_min_tpm = value" data-copy="suppa2_min_tpm = 1">suppa2_min_tpm</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card ox-dag-card--wide" markdown="1">

<a href="/assets/dag/oxo-flow-tcasia.svg?v=5828140598" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-tcasia.svg?v=5828140598" alt="oxo-flow-tcasia pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-tcasia — Paired-end RNA-seq from FASTQ to per-sample alternative-splicing calls: reads are trimmed with fastp, aligned with two-pass STAR and counted per gene with featureCounts; each sample&#x27;s splicing is then quantified independently with four callers — rMATS, MAJIQ (with Voila export), SUPPA2 (via Salmon transcript quantification) and SplAdder.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastp_qc
- star_align
- sort_bam
- index_bam
- featurecounts
- salmon_quant
- select_suppa_fields
- format_suppa_fields
- suppa_run
- rmats_create_input
- rmats_run
- majiq_create_ini
- majiq_build
- majiq_psi
- voila_modulize
- voila_tsv
- spladder_run

**Excluded**

- none

## Fidelity

Scope: the **default-parameters main execution path** (upstream `rule all` of both Snakefiles). Rows cover every upstream rule; no "not ported" rows — the full default path is ported.

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| fastp_qc | `alignment::fastp_qc` | fastp 0.23.4 | identical command; input layout from `[[sample_groups]]` + `reads_dir` instead of samples.tsv |
| star_align | `alignment::star_align` | STAR 2.7.7a | identical command; `params.prefix` inlined; `--limitBAMsortRAM` differs — upstream hardcodes 39050942993 (~36 G), the port defaults `star_limit_bam_sort_ram = 0` → machine-effective memory |
| sort_bam | `alignment::sort_bam` | samtools 1.15 | same sort; `-@ {effective_threads}` + `-m 512M` cap added (upstream `-@ 8` with sort's default 768 MB/thread buffer over-allocated the live box) |
| index_bam | `alignment::index_bam` | samtools 1.15 | identical command |
| featurecounts | `alignment::featurecounts` | subread 2.0.1 | identical command; upstream runs without a strandness flag (oxo-flow preflight warns — upstream behavior kept) |
| salmon_quant | `as_calling::salmon_quant` | salmon 1.10.3 | identical command; `-l` from explicit `salmon_library_type` (upstream derives it from `strandness` in tcasia_config.py) |
| select_suppa_fields | `as_calling::select_suppa_fields` | suppa 2.3 | identical command |
| format_suppa_fields | `as_calling::format_suppa_fields` | suppa 2.3 | equivalent perl one-liner (anchored rewrite of the upstream regex; same output) |
| suppa_run | `as_calling::suppa_run` | suppa 2.3 | identical command; output prefix inlined |
| rmats_create_input | `as_calling::rmats_create_input` | rMATS 4.3.0 | identical command |
| rmats_run | `as_calling::rmats_run` | rMATS 4.3.0 | identical command; `--od` directory declared as the rule output |
| majiq_create_ini | `as_calling::majiq_create_ini` | MAJIQ 2.5 | identical printf; `bam_dir`/`bam_stem` params inlined |
| majiq_build | `as_calling::majiq_build` | MAJIQ 2.5 | identical command |
| majiq_psi | `as_calling::majiq_psi` | MAJIQ 2.5 | identical command |
| voila_modulize | `as_calling::voila_modulize` | MAJIQ 2.5 (Voila) | identical command; `modulized/` directory declared as the rule output |
| voila_tsv | `as_calling::voila_tsv` | MAJIQ 2.5 (Voila) | identical command |
| spladder_run | `as_calling::spladder_run` | SplAdder 3.1.1 | identical command; output directory declared as the rule output |
| rule all | — (DAG targets) | — | every output above is a default target of the single chained DAG |

**Port-level conventions** (config-shape deviations, commands unchanged):
- **Sample sheet**: upstream reads per-sample fastq paths from a TSV (`sample_id/fastq_1/fastq_2`); the port uses `[[sample_groups]]` plus the `reads_dir/{sample}_1.fastq.gz` / `{sample}_2.fastq.gz` layout.
- **One workflow file, one DAG**: the two upstream Snakefiles (+ the four `rules/snakefile_*` fragments) are `modules/alignment.oxoflow` + `modules/as_calling.oxoflow`, included from `main.oxoflow`; the two `config.yml` files merge into one `[config]`. Upstream `01 output_dir/aligned` and `02 bam_dir` are the single key `aligned_dir`, making the alignment → AS-calling chain structural. Run one stage only with `-t alignment` / `-t as_calling`.
- **Strandness-derived values are explicit config keys**: upstream computes `salmon_library_type` (`fr-firststrand→ISR`, `fr-secondstrand→ISF`, `fr-unstranded→IU`) and `majiq_strandness` (`fr-firststrand→reverse`, `fr-secondstrand→forward`, `fr-unstranded→none`) in `tcasia_config.py`; rMATS uses the `strandness` value directly (as upstream). Change `strandness` **and** the two derived keys together.
- **Helper scripts not ported**: `scripts/validate_config.py` and `scripts/read_length.sh` are user-facing helpers; oxo-flow validates config/inputs natively.
- **Threads only, no memory**: upstream declares threads per tool and no memory; the port mirrors that exactly.
- **STAR BAM-sort RAM is machine-sized by default**: upstream hardcodes `--limitBAMsortRAM 39050942993` (~36 GB); the port adds `star_limit_bam_sort_ram` (default `0` = auto) and sizes the limit from `{effective_memory_mb}`, so STAR adapts to small boxes; set it to a byte count to pin an exact value.
- **samtools sort buffer cap**: `sort_bam` runs `samtools sort -@ {effective_threads} -m 512M` instead of upstream's plain `-@ 8` — sort's default 768 MB/thread buffer over-allocated the live box.
- **SUPPA2 field formatting regex**: `format_suppa_fields` applies the same transformation as the upstream one-liner with an anchored regex (`s/^\|.*?\|\t//` instead of upstream's capture-and-delete); output is identical for the quant.sf-derived input shape.
- **MAJIQ is license-gated**: upstream runs the 5-rule MAJIQ chain unconditionally and fails hard without the academic license file. The port gates the chain on `run_majiq` (default `false`): a fresh clone completes with rMATS + SUPPA2 + SplAdder; set `run_majiq = true` after placing the license at `majiq_license` (commands unchanged when enabled).
- **MAJIQ env fixes**: upstream's own `pip majiq==2.5` installs from no index (PyPI/bioconda both lack majiq) — the port installs OncoHarmony-Network/majiq_academic@v2.5 (the TCASIA org's fork), with numpy=1.26 (the fork's Cython extensions break on numpy 2.x ABI) and setuptools=75.8.2 (voila's gunicorn imports pkg_resources, removed in setuptools 81+).

## Links

- Repository: [oxo-flow-tcasia](https://github.com/oxo-flow-community/oxo-flow-tcasia)
- Upstream: [OncoHarmony-Network/TCASIA_pipeline](https://github.com/OncoHarmony-Network/TCASIA_pipeline) @ `main@06564ff1`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
