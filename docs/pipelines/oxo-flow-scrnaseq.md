---
title: "Single-cell RNA-seq: alignment, quantification and QC"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-scrnaseq</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Single-cell RNA-seq: alignment, quantification and QC</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">single-cell</span><span class="ox-tag">scrna-seq</span><span class="ox-tag">cellranger</span><span class="ox-tag">cellranger-arc</span><span class="ox-tag">simpleaf</span><span class="ox-tag">alevin-fry</span><span class="ox-tag">kallisto</span><span class="ox-tag">starsolo</span><span class="ox-tag">10x-genomics</span><span class="ox-tag">nf-core</span></div>
<p class="ox-desc">Single-cell RNA-seq analysis from raw FASTQ reads to a final MultiQC report, on all six upstream aligner branches of nf-core/scrnaseq 4.2.0: cellranger (default, count or multi with per-modality GEX/VDJ/Ab/BEAM/CRISPR/CMO via the metadata table), simpleaf (upstream default; index + quant + optional QCatch), kallisto/bustools (standard/lamanno/nac), STARsolo (incl. legacy iGenomes index upgrade), and cellrangerarc multiome ATAC+GEX. Shared downstream path: FastQC, mtx→h5ad conversion per aligner, CellBender ambient-RNA background removal (skipped for cellrangerarc, like upstream), sample-wise h5ad concatenation, optional Seurat/SingleCellExperiment export, workflow summary + methods description, MultiQC.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-scrnaseq" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">46</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 12 CPUs / 72 GB per rule (Cell Ranger)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">single-cell</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/scrnaseq">nf-core/scrnaseq</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>4.2.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2280.1"><code>10.48546/workflowhub.workflow.2280.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">cellranger</span><span class="tchip">cellranger-arc</span><span class="tchip">simpleaf</span><span class="tchip">alevin-fry</span><span class="tchip">piscem</span><span class="tchip">salmon</span><span class="tchip">qcatch</span><span class="tchip">kallisto-bustools</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Single-cell RNA-seq pipeline</strong> (port of nf-core/scrnaseq): raw 10x-style FASTQs plus a reference genome and annotation go through one of several aligner routes into per-sample and combined matrices, cleaned of ambient RNA by CellBender.</p>
<p><strong>1. Reference preparation</strong> — <code>gunzip_fasta</code> and <code>gunzip_gtf</code> decompress the (optionally gzipped) genome and annotation; their outputs converge in <code>gtf_gene_filter</code>, which keeps only annotations present in the genome FASTA, followed by the opt-in <code>gtf_source_fix</code> rewriting for Cell Ranger.</p>
<p><strong>2. Indexing and quantification (one exclusive route per run)</strong> — Cell Ranger: <code>cellranger_mkgtf</code> → <code>cellranger_mkref</code> → <code>cellranger_count</code>, or, when the multi branch is on, <code>cellranger_mkvdjref</code> → <code>cellranger_multi</code>; cellranger-arc: <code>cellrangerarc_mkgtf</code> → <code>cellrangerarc_mkref</code> → <code>cellrangerarc_count</code>; simpleaf: <code>simpleaf_index</code> → <code>simpleaf_quant</code> → <code>qcatch</code>; kallisto|bustools: <code>kallistobustools_ref_standard</code> or <code>kallistobustools_ref_velocity</code> → <code>kallistobustools_count</code>; STARsolo: <code>star_genomegenerate</code> (or the legacy-index <code>star_genomeparams_upgrade</code>) → <code>star_align</code>.</p>
<p><strong>3. Matrix conversion</strong> — whichever route ran, its raw and filtered outputs become per-sample h5ads: <code>mtx_to_h5ad_raw</code> and <code>mtx_to_h5ad_filtered</code> (Cell Ranger count, cellranger-arc), <code>mtx_to_h5ad_multi_raw</code> and <code>mtx_to_h5ad_multi_filtered</code>, <code>mtx_to_h5ad_simpleaf</code>, <code>mtx_to_h5ad_kallisto_raw</code> and <code>mtx_to_h5ad_kallisto_filtered</code>, <code>mtx_to_h5ad_star_raw</code> and <code>mtx_to_h5ad_star_filtered</code>.</p>
<p><strong>4. CellBender, merge, R objects</strong> — <code>cellbender_removebackground</code> strips ambient RNA from raw matrices (never for cellrangerarc); <code>anndata_barcodes</code> subsets them to the surviving barcodes; <code>concat_h5ad_filtered</code>, <code>concat_h5ad_cellbender_filter</code> and <code>concat_h5ad_raw</code> merge each input type across samples; the anndataR rules convert per-sample and combined h5ads to Seurat and SingleCellExperiment RDS.</p>
<p><strong>5. Reporting</strong> — <code>fastqc</code> reports (skipped for cellrangerarc), plus <code>collect_versions</code>, <code>workflow_summary</code> and <code>methods_description</code>, all feed <code>multiqc</code> for the final aggregate report.</p>
<p><em>Verified: every rule name above is a real rule of <code>main.oxoflow</code> (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-scrnaseq+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>


<div class="ox-tryit">
<div class="ox-tryit-title">⬡ Try it — clone &amp; run</div>
<pre class="ox-tryit-cmd" data-copy="git clone https://github.com/oxo-flow-community/oxo-flow-scrnaseq.git &amp;&amp; cd oxo-flow-scrnaseq &amp;&amp; oxo-flow run main.oxoflow">git clone https://github.com/oxo-flow-community/oxo-flow-scrnaseq.git
cd oxo-flow-scrnaseq
oxo-flow run main.oxoflow</pre>
<p class="ox-tryit-note">The repository ships test fixtures (e.g. <code>test/fixtures/generate_fixtures.py</code>, <code>test/fixtures/raw/S1_R1.fastq.gz</code>, <code>test/fixtures/raw/S1_R2.fastq.gz</code>, <code>test/fixtures/raw/S2_R1.fastq.gz</code>) — point <code>input</code> at them or use the built-in sample group to <code>dry-run</code> first.</p>
</div>


## Run it

```bash
oxo-flow run main.oxoflow
```

Needs Cell Ranger reference data and reads — see Requirements; preview with `oxo-flow dry-run main.oxoflow`.

## Installation

**Engine.** oxo-flow >= 0.13.1 ({effective_threads}/{effective_memory_mb} sizing, shipped in 0.13.1); cellranger_multi=true additionally requires >= 0.17.0 (per-sample {meta.*} metadata placeholders)

**Toolchain.** containers (Docker/Singularity) — pinned images; conda alternatives in envs/ for non-Cell-Ranger rules (Cell Ranger rules are docker-only)

**Requirements.**

- reference genome FASTA, optionally gzipped (config.fasta, default refs/refdata.fa.gz)
- gene-annotation GTF, optionally gzipped (config.gtf, default refs/refdata.gtf.gz)
- raw FASTQ pair per sample: raw/<sample>_R1.fastq.gz and raw/<sample>_R2.fastq.gz (one pair per sample); for aligner=cellrangerarc five pre-named files per sample: raw/<sample>_{gex,atac}_S1_L001_R{1,2,3}_001.fastq.gz
- for cellranger_multi=true only: per-modality FASTQ pairs (vdj/ab/beam/crispr/cmo) listed in refs/cellranger_multi_metadata.tsv (GEX always comes from raw/<sample>_R{1,2}.fastq.gz); empty cell = modality absent; plus optional cellranger_multi_gex_reference / cellranger_multi_vdj_reference / cellranger_multi_fb_reference / cellranger_multi_barcodes (upstream --cellranger_index / --cellranger_vdj_index / --fb_reference / --cellranger_multi_barcodes)
- barcode whitelist per protocol for simpleaf/star (config.whitelist; the four upstream whitelists ship under assets/whitelist/)
- samplesheet.csv with columns sample,fastq_1,fastq_2,protocol,expected_cells (used by the combined-h5ad step)
- compute: up to 12 CPUs / 72 GB per rule (index builds and alignments); 6 CPUs / 36 GB for h5ad conversion, CellBender and concat rules; concurrent per-sample rules scale with -j
- optional pre-built indexes to skip building: cellranger (build_cellranger_index=false + transcriptome), simpleaf_index, kallisto_index (+ txp2gene), star_index, cellrangerarc_reference

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-scrnaseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-scrnaseq
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy aligner = value" data-copy="aligner = cellranger">aligner</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>cellranger</code></td>
<td class="ox-p-desc">--aligner / --protocol. The port implements ALL upstream aligner branches:<br>cellranger (default, matches upstream&#x27;s most-tested path), simpleaf (upstream<br>default aligner), kallisto (kallisto/bustools), star (STARsolo) and<br>cellrangerarc (multiome ATAC+GEX). Protocol values are mapped per aligner<br>inside the alignment rules (upstream protocols.json); &#x27;auto&#x27; is only valid<br>for cellranger/cellrangerarc, exactly like upstream.<br><span class="ox-param-usedby">used by <code>41</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy build_cellranger_index = value" data-copy="build_cellranger_index = true">build_cellranger_index</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">cellranger reference: build from fasta/gtf, or point transcriptome at an existing index<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellranger_localmem = value" data-copy="cellranger_localmem = 0">cellranger_localmem</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">GB passed to cellranger&#x27;s --localmem (mkref/count). 0 = auto: 2/3 of<br>the actually-free physical memory (/proc/meminfo MemAvailable, 1 GB<br>floor) — never the engine&#x27;s effective memory, which counts swap:<br>cellranger&#x27;s jobmngr waits forever when --localmem exceeds the free<br>RAM (live: &#x27;Need 6 GB ... (2.6 GB available)&#x27; looped for hours on a<br>3.7GB box). Set a positive number to force a value.<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellranger_multi = value" data-copy="cellranger_multi = false">cellranger_multi</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">cellranger multi (upstream aligner = cellrangermulti): the multiome<br>VDJ / Ab-seq / CRO branch. OFF by default. Enabling it supersedes<br>cellranger_count (upstream&#x27;s aligner branches are exclusive). Per-sample<br>per-modality FASTQs come from the [workflow] metadata_file table<br>(refs/cellranger_multi_metadata.tsv): one pair per modality per sample in<br>columns &lt;modality&gt;_fastq_1/&lt;modality&gt;_fastq_2 for vdj/ab/beam/crispr/cmo;<br>an empty cell = modality absent for that sample — the engine renders<br>{meta.&lt;col&gt;} as &#x27;&#x27;, the port&#x27;s equivalent of upstream&#x27;s EMPTY-file<br>injection (the exclusion is closed without an engine follow-up).<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellranger_multi_barcodes = value" data-copy="cellranger_multi_barcodes = ">cellranger_multi_barcodes</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream --cellranger_multi_barcodes: barcode table (sample,multiplexed_sample_id,description[,cmo_ids])<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellranger_multi_fb_reference = value" data-copy="cellranger_multi_fb_reference = ">cellranger_multi_fb_reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream --fb_reference: feature-barcoding reference (antibody/CRISPR)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellranger_multi_gex_reference = value" data-copy="cellranger_multi_gex_reference = ">cellranger_multi_gex_reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream --cellranger_index; empty = the built {config.transcriptome}<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellranger_multi_vdj_reference = value" data-copy="cellranger_multi_vdj_reference = ">cellranger_multi_vdj_reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream --cellranger_vdj_index; empty = built by cellranger_mkvdjref<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellrangerarc_config = value" data-copy="cellrangerarc_config = ">cellrangerarc_config</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">optional mkref config json (upstream --cellrangerarc_config); auto-generated when empty<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cellrangerarc_reference = value" data-copy="cellrangerarc_reference = refs/cellrangerarc_reference">cellrangerarc_reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/cellrangerarc_reference</code></td>
<td class="ox-p-desc">cellrangerarc reference (multiome ATAC+GEX)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy email = value" data-copy="email = ">email</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">completion notifications (nf-core PIPELINE_COMPLETION port): summary email<br>on success (<code>email</code>), failure address (<code>email_on_fail</code>) and a webhook<br>(<code>hook_url</code>). Empty = no notification, exactly like upstream&#x27;s empty email<br>params. Consumed by the workflow-level on_complete / on_error hooks above<br>(engine &gt;= 0.17.0); older engines ignore the hook keys and the run is<br>untouched.<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy email_on_fail = value" data-copy="email_on_fail = ">email_on_fail</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">failure-only recipient (upstream --email_on_fail; used when email is empty)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy expected_cells = value" data-copy="expected_cells = ">expected_cells</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">samplesheet <code>expected_cells</code> column -&gt; --expect-cells/--soloCellFilter when set<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta = value" data-copy="fasta = refs/refdata.fa.gz">fasta</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata.fa.gz</code></td>
<td class="ox-p-desc">reference genome (upstream --fasta / --gtf; may be .gz)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta_gz = value" data-copy="fasta_gz = true">fasta_gz</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream --fasta gzipped flag (gunzipped by the prep rule)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta_prepared = value" data-copy="fasta_prepared = refs/refdata.fa">fasta_prepared</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata.fa</code></td>
<td class="ox-p-desc">derived reference files (README &quot;Reference genome&quot; explains the chain)<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf = value" data-copy="gtf = refs/refdata.gtf.gz">gtf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata.gtf.gz</code></td>
<td class="ox-p-desc">annotation GTF (upstream --gtf; may be .gz)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_filtered = value" data-copy="gtf_filtered = refs/refdata_genes.gtf">gtf_filtered</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata_genes.gtf</code></td>
<td class="ox-p-desc">gene-level GTF for cellranger/count filtering (upstream filtered_gtf; the &quot;biotype = protein_coding&quot; filter)<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_gz = value" data-copy="gtf_gz = true">gtf_gz</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream --gtf gzipped flag (gunzipped by the prep rule)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_mkgtf = value" data-copy="gtf_mkgtf = refs/refdata_genes.filtered.gtf">gtf_mkgtf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata_genes.filtered.gtf</code></td>
<td class="ox-p-desc">cellranger mkgtf output (the filtered annotation)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_mkgtf_input = value" data-copy="gtf_mkgtf_input = refs/refdata_genes.gtf">gtf_mkgtf_input</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata_genes.gtf</code></td>
<td class="ox-p-desc">set to the source-fixed file when gtf_source_fix=true<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_prepared = value" data-copy="gtf_prepared = refs/refdata.gtf">gtf_prepared</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata.gtf</code></td>
<td class="ox-p-desc">gunzipped GTF (prep-rule output)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_source_fix = value" data-copy="gtf_source_fix = false">gtf_source_fix</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">iGenomes GTF source-field rewrite (opt-in, upstream gtf_source_has_spaces)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtf_source_fixed = value" data-copy="gtf_source_fixed = refs/refdata_genes.source_fixed.gtf">gtf_source_fixed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/refdata_genes.source_fixed.gtf</code></td>
<td class="ox-p-desc">source-field-rewritten GTF (gtf_source_fix output)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy hook_url = value" data-copy="hook_url = ">hook_url</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">webhook URL for the on_complete / on_error notifications<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kallisto_index = value" data-copy="kallisto_index = ">kallisto_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">kallisto/bustools<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kb_t1c = value" data-copy="kb_t1c = ">kb_t1c</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">optional cdna_t2c.txt override<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kb_t2c = value" data-copy="kb_t2c = ">kb_t2c</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">optional intron_t2c.txt override<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kb_workflow = value" data-copy="kb_workflow = standard">kb_workflow</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>standard</code></td>
<td class="ox-p-desc">standard | lamanno | nac (any non-standard builds the intron index too)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy multiqc_config = value" data-copy="multiqc_config = assets/multiqc_config.yml">multiqc_config</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>assets/multiqc_config.yml</code></td>
<td class="ox-p-desc">MultiQC config path (upstream --multiqc_config)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy multiqc_title = value" data-copy="multiqc_title = ">multiqc_title</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">-&gt; <code>--title</code> when set<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">results directory (upstream --outdir)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy protocol = value" data-copy="protocol = auto">protocol</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>auto</code></td>
<td class="ox-p-desc">cellranger/arc: &#x27;auto&#x27; or 10XV1-4; simpleaf/kallisto/star: 10XV1-4/dropseq(/smartseq)<br><span class="ox-param-usedby">used by <code>13</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qcatch_n_partitions = value" data-copy="qcatch_n_partitions = ">qcatch_n_partitions</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">qcatch --n_partitions when set (for protocols without a chemistry mapping)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy remove_doublets = value" data-copy="remove_doublets = false">remove_doublets</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream --remove_doublets: doublet removal for simpleaf<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy samplesheet = value" data-copy="samplesheet = test/fixtures/samplesheet.csv">samplesheet</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/samplesheet.csv</code></td>
<td class="ox-p-desc">consumed by CONCAT_H5AD (same columns as upstream)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy save_align_intermeds = value" data-copy="save_align_intermeds = true">save_align_intermeds</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">-&gt; <code>--create-bam true</code> (cellranger) / publish the BAM (star)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy seq_center = value" data-copy="seq_center = ">seq_center</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">--outSAMattrRGline CN field when set<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy simpleaf_index = value" data-copy="simpleaf_index = ">simpleaf_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">simpleaf (upstream default aligner)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy simpleaf_umi_resolution = value" data-copy="simpleaf_umi_resolution = cr-like">simpleaf_umi_resolution</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>cr-like</code></td>
<td class="ox-p-desc">upstream --simpleaf_umi_resolution (cr-like | paired | naive)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_cellbender = value" data-copy="skip_cellbender = false">skip_cellbender</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream --skip_cellbender: skip ambient-RNA background removal<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_cellrangermulti_vdjref = value" data-copy="skip_cellrangermulti_vdjref = false">skip_cellrangermulti_vdjref</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream same name: skip the VDJ reference build<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastqc = value" data-copy="skip_fastqc = false">skip_fastqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">QC / reporting knobs<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_multiqc = value" data-copy="skip_multiqc = false">skip_multiqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream --skip_multiqc<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_qcatch = value" data-copy="skip_qcatch = false">skip_qcatch</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream --skip_qcatch: skip the qcatch QC step<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_feature = value" data-copy="star_feature = Gene">star_feature</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Gene</code></td>
<td class="ox-p-desc">--soloFeatures (Gene | Gene Velocyto | ...)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_ignore_sjdbgtf = value" data-copy="star_ignore_sjdbgtf = false">star_ignore_sjdbgtf</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skip --sjdbGTFfile<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_index = value" data-copy="star_index = ">star_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">STARsolo<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_index_legacy = value" data-copy="star_index_legacy = false">star_index_legacy</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upgrade a legacy 2.6.x iGenomes index (genomeParameters rewrite)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy transcript_fasta = value" data-copy="transcript_fasta = ">transcript_fasta</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">transcript FASTA for simpleaf index building (mutually exclusive with fasta/gtf)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy transcriptome = value" data-copy="transcriptome = refs/cellranger_reference">transcriptome</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>refs/cellranger_reference</code></td>
<td class="ox-p-desc">cellranger reference dir (upstream --transcriptome): built by cellranger_mkref, or an existing index<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy txp2gene = value" data-copy="txp2gene = ">txp2gene</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">t2g map (required with transcript_fasta; also used as the kallisto t2g)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy whitelist = value" data-copy="whitelist = ">whitelist</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">barcode whitelist for simpleaf/star. Empty = mapped per protocol from<br>assets/whitelist/10x_V{1..4}_barcode_whitelist.txt.gz (upstream<br>protocols.json behavior); set a path to override.<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-scrnaseq-rules.svg?v=e8d438a5ab" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-scrnaseq-rules.svg?v=e8d438a5ab" alt="oxo-flow-scrnaseq rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-scrnaseq.svg?v=c9c8344cf5" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-scrnaseq.svg?v=c9c8344cf5" alt="oxo-flow-scrnaseq pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-scrnaseq — Single-cell RNA-seq analysis from raw FASTQ reads to a final MultiQC report, on all six upstream aligner branches of nf-core/scrnaseq 4.2.0: cellranger (default, count or multi with per-modality GEX/VDJ/Ab/BEAM/CRISPR/CMO via the metadata table), simpleaf (upstream default; index + quant + optional QCatch), kallisto/bustools (standard/lamanno/nac), STARsolo (incl.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- anndata_barcodes
- anndatar_convert_cellbender_filter
- anndatar_convert_combined_cellbender_filter
- anndatar_convert_combined_filtered
- anndatar_convert_combined_raw
- anndatar_convert_filtered
- anndatar_convert_raw
- cellbender_removebackground
- cellranger_count
- cellranger_mkgtf
- cellranger_mkref
- cellranger_mkvdjref
- cellranger_multi
- cellrangerarc_count
- cellrangerarc_mkgtf
- cellrangerarc_mkref
- collect_versions
- concat_h5ad_cellbender_filter
- concat_h5ad_filtered
- concat_h5ad_raw
- fastqc
- gtf_gene_filter
- gtf_source_fix
- gunzip_fasta
- gunzip_gtf
- kallistobustools_count
- kallistobustools_ref_standard
- kallistobustools_ref_velocity
- methods_description
- mtx_to_h5ad_filtered
- mtx_to_h5ad_kallisto_filtered
- mtx_to_h5ad_kallisto_raw
- mtx_to_h5ad_multi_filtered
- mtx_to_h5ad_multi_raw
- mtx_to_h5ad_raw
- mtx_to_h5ad_simpleaf
- mtx_to_h5ad_star_filtered
- mtx_to_h5ad_star_raw
- multiqc
- qcatch
- simpleaf_index
- simpleaf_quant
- star_align
- star_genomegenerate
- star_genomeparams_upgrade
- workflow_summary

**Excluded**

- none

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- nf-core/gffread + gffread_transcriptome module is present in the upstream tree but unreachable: no include anywhere in workflows/ or subworkflows/ at 4.2.0 (only the modules.json dependency listing)

## Fidelity

Rows cover every upstream process/subworkflow of nf-core/scrnaseq 4.2.0, on all
six aligner branches. Container image strings and conda pins are copied
verbatim from the upstream modules (all pinned, no `latest`). Deviations from
upstream mechanics are called out per row; one multi-lane data limitation
remains and is listed at the bottom with evidence. `PIPELINE_COMPLETION` is
ported via workflow-level hooks (row below).

**Live verification** (2026-08-26/27, tx-ubuntu, engine 0.15.0 + apptainer):
five configurations passed end-to-end — `aligner = cellranger`, `simpleaf`,
`kallisto`, `star` (10X) and `star` with `protocol = dropseq`. The
`cellrangerarc` branch is ported and validate/lint-clean but was not live-run
in this wave. The `cellranger_multi` branch is ported and validate/lint/
dry-run-clean with the expanded per-sample config.csv verified shell-level
(see the [Cell Ranger multi mode](#cell-ranger-multi-mode) section); it needs
the `quay.io/nf-core/cellranger:10.0.0` container (present for `count`), so a
live run only needs the metadata table filled — queued for the next container
wave.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `PIPELINE_INITIALISATION` (samplesheet check) | sample source + `config.samplesheet` | — | Samplesheet (`sample, fastq_1, fastq_2, protocol, expected_cells`) maps to `[[sample_groups]]`; `expected_cells` column → `config.expected_cells`; per-sample `protocol` column is informational (chemistry comes from `--protocol`). Schema checks are enforced by the port's fixtures + README contract. |
| `FASTQC` | `fastqc` | fastqc 0.12.1 | Identical command: `printf … \| while read; ln -s` staging loop, `fastqc --quiet --threads N --memory <12G/N clamped 100-10000>`. Published under `results/fastqc/` (upstream default publishDir). `--memory` computed in-shell from the process_low 12G/2 cpus. |
| `GUNZIP` (as `GUNZIP_FASTA`) | `gunzip_fasta` | gzip 1.13 | Identical command (`gzip -cd <fasta> > <out>`). Runs only when `config.fasta_gz` (upstream decides by `.endsWith('.gz')` at runtime — port uses an explicit flag, see Gotchas). |
| `GUNZIP` (as `GUNZIP_GTF`) | `gunzip_gtf` | gzip 1.13 | Same as above for the GTF. |
| `GTF_GENE_FILTER` | `gtf_gene_filter` | python 3.9 | Same bundled script `filter_gtf_for_genes_in_genome.py`, same flags (`--gtf --fasta -o`); output name `<fasta_stem>_genes.gtf` is `config.gtf_filtered`. |
| `GAWK` (as `GTF_SOURCE_FIX`) | `gtf_source_fix` | gawk 5.3.1 | Same awk program (`FS=OFS="\t"`, source-field spaces→underscores, output suffix `gtf`). Off by default, exactly like upstream (only fires for iGenomes entries flagged `gtf_source_has_spaces`). |
| `CELLRANGER_MKGTF` | `cellranger_mkgtf` | cellranger 10.0.0 | Same command incl. the three `--attribute=gene_biotype:` filters. Runs only when `build_cellranger_index=true` (mirrors upstream `if (!cellranger_index)`). |
| `CELLRANGER_MKREF` | `cellranger_mkref` | cellranger 10.0.0 | Same command (`--genome=… --fasta=… --genes=… --localcores --localmem --nthreads`). `--genome` is `config.transcriptome` (default `refs/cellranger_reference`) instead of a bare workdir name — same reference name, path relocated to the workflow tree. |
| `CELLRANGER_COUNT` | `cellranger_count` | cellranger 10.0.0 | Same command: reads staged under Cell Ranger naming (`<sample>_S1_L001_R1/R2_001.fastq.gz`), `cellranger count --id <sample> --fastqs fastq_all --transcriptome … --localcores … --localmem … --chemistry <protocol> --create-bam <bool>` + `--expect-cells` when set. The outs tree is then relocated to `results/<aligner>/count/<sample>/outs/` (upstream publishDir `outdir/cellranger/count`). Skipped when `cellranger_multi = true` (the upstream aligner branches are exclusive). Multi-lane samples (several fastq pairs per sample) are not represented — one pair per sample. |
| `CELLRANGER_MKVDJREF` | `cellranger_mkvdjref` | cellranger 10.0.0 | Same command (`cellranger mkvdjref --genome=… --fasta=… --genes=… --localcores … --localmem …`). Runs only when `cellranger_multi = true` and no `cellranger_multi_vdj_reference` is set and `skip_cellrangermulti_vdjref = false` — mirrors the upstream `if (!cellranger_vdj_index && !params.skip_cellrangermulti_vdjref)` gate. Output at `refs/cellranger_vdj_reference/`. |
| `CELLRANGER_MULTI` | `cellranger_multi` | cellranger 10.0.0 | Same module (`cellranger multi --id <sample> --csv=<config.csv> --localcores … --localmem …`, `TENX_DISABLE_TELEMETRY` set): per-modality reads staged under `fastq_all/<modality>/` with Cell Ranger naming, config.csv assembled with `[gene-expression]` (reference/chemistry/create-bam), `[vdj]`, `[feature]` and `[libraries]` rows per present modality, `[samples]` when CMO FASTQs are present. outs tree relocated to `results/<aligner>/multi/<sample>/outs/` (upstream `outdir/cellranger/multi`; the port keeps `count/` and `multi/` disjoint instead of upstream's single `count/` dir). Upstream's per-sample, per-modality `groupTuple` + EMPTY-file injection is replaced by the metadata table — see the [Cell Ranger multi mode](#cell-ranger-multi-mode) section. |
| `SIMPLEAF_INDEX` | `simpleaf_index` | simpleaf 0.19.5, piscem 0.12.2, alevin-fry 0.11.2, salmon 1.10.3 | Same command (`simpleaf set-paths` + `simpleaf index --threads … [--ref-seq <transcript_fasta> | --fasta … --gtf …] -o simpleaf_index`; `ulimit -n 2048` and `ALEVIN_FRY_HOME` exported). Transcript-fasta mode requires `txp2gene`, mirroring upstream's assert. Output under `refs/simpleaf_index/`. |
| `SIMPLEAF_QUANT` | `simpleaf_quant` | simpleaf 0.19.5, alevin-fry 0.11.2, piscem 0.12.2, salmon 1.10.3 | Same command (`simpleaf quant [--t2g-map …] --chemistry <protocol-mapped> --index … --reads1/2 … --resolution cr-like --output simpleaf_quant --threads … --anndata-out --unfiltered-pl <whitelist>`; cell filtering hardcoded to `unfiltered-pl` upstream → input_type is always raw). Protocol→chemistry mapping and per-protocol whitelist mirror `assets/protocols.json`. Output `results/<aligner>/<sample>/simpleaf_quant/af_quant/`. |
| `QCATCH` | `qcatch` | qcatch 0.2.12 | Same command (`qcatch --input <af_quant dir> --output qcatch [--chemistry 10X_3p_v2/v3/v4] --save_filtered_h5ad --export_summary_table [--n_partitions] [--remove_doublets --visualize_doublets]`), same output renames (`QCatch_report.html` → `<sample>_qcatch_report.html`, `filtered_quants.h5ad` → `<sample>_filtered_quants.h5ad`, `summary_table.csv` → `<sample>_metrics_summary.csv`). Chemistry mapping for 10XV2-4 only, exactly like upstream. |
| `KALLISTOBUSTOOLS_REF` | `kallistobustools_ref_standard`, `kallistobustools_ref_velocity` | kb-python 0.28.2 | Same commands: standard `kb ref -i … -g … -f1 cdna.fa --workflow standard`; non-standard workflows (`lamanno`/`nac`) add `-f2 intron.fa -c1 cdna_t2c.txt -c2 intron_t2c.txt --workflow <mode>`. Mutual exclusion is a `when` on `kb_workflow` (upstream picks the command by the same variable). Outputs under `refs/kallisto/`. |
| `KALLISTOBUSTOOLS_COUNT` | `kallistobustools_count` | kb-python 0.28.2 | Same command (`kb count -t … -i … -g … [-c1 …] [-c2 …] -x <technology> --workflow <kb_workflow> --filter -o <sample>.count -m <memory.toGiga()-1>G reads`); technology mapping for 10XV1-4/DROPSEQ/SMARTSEQ mirrors upstream. Ext.args `--workflow … --filter` applied. Output `results/<aligner>/<sample>.count/`. |
| `STAR_GENOMEGENERATE` | `star_genomegenerate` | star 2.7.11b, samtools 1.21, gawk 5.1.0 | Same command: `samtools faidx` + gawk SAindexNbases heuristic from the `.fai` (14 cap), `--runMode genomeGenerate --genomeDir … --genomeFastaFiles … --sjdbGTFfile … --runThreadN … --genomeSAindexNbases … --limitGenomeGenerateRAM <memory-100000000>`. Output under `refs/star_index/`. |
| `STAR_GENOMEPARAMS_UPGRADE` | `star_genomeparams_upgrade` | gawk 5.3.1 | Same script: symlink the legacy index files, awk-rewrite `genomeParameters.txt` (versionGenome 20201 → 2.7.4a, append genomeType/Full + genomeTransformType/None + genomeTransformVCF/-), move to `refs/star_index_upgraded/`. Fires only when `star_index` is set and `star_index_legacy=true` (upstream `isStarIndexLegacy`). |
| `STAR_ALIGN` | `star_align` | star 2.7.10b | Same command: reads passed REVERSE first, `--readFilesCommand zcat --runDirPerm All_RWX --outWigType bedGraph --twopassMode Basic --outSAMtype BAM SortedByCoordinate --limitBAMsortRAM <memory bytes>`, `--soloCBwhitelist` with the same `.gz`→uncompress handling (protocols without an upstream whitelist — dropseq/smartseq — get the literal `--soloCBwhitelist None`, STAR's required spelling for no whitelist; live-found: omitting the flag aborts with "--soloCBwhitelist is not defined"), `--soloType`/`--soloUMIlen` per protocol (10XV1/2→10, 10XV3/4→12, dropseq/smartseq→none), `--soloCellFilter CellRanger2.2 <expected_cells> 0.99 10` when set, `--soloFeatures <star_feature>` (+Velocyto publish rename). Solo.out tsv/mtx files gzipped in-place before publish, exactly like upstream. Index selection: upgraded legacy > user `star_index` > built. |
| `CELLRANGERARC_MKGTF` | `cellrangerarc_mkgtf` | cellranger-arc 2.0.2 | Same command as upstream (`cellranger-arc mkgtf` with the three biotype filters). Runs only when `build_cellranger_index=true`. |
| `CELLRANGERARC_MKREF` | `cellrangerarc_mkref` | cellranger-arc 2.0.2 | Same flow: auto-generated mkref config json (`organism: "refdata"`, `genome: ["<prefix>_reference"]`, `input_fasta`, `input_gtf`) or user `cellrangerarc_config`, then `cellranger-arc mkref --config=config --nthreads …`. Output at `refs/cellrangerarc_reference/` (the config's `genome` name; `cellrangerarc_reference` can point at an existing reference to skip building). |
| `CELLRANGERARC_COUNT` | `cellrangerarc_count` | cellranger-arc 2.0.2 | Same flow: fastqs staged under `fastqs/`, 2-row `lib.csv` (Gene Expression / Chromatin Accessibility), `cellranger-arc count --id=<sample> --libraries=… --reference=… --localcores … --localmem … [--expect-cells]`, outs tree relocated to `results/<aligner>/count/<sample>/outs/`. Deviation: the upstream samplesheet's `sample_type`/`fastq_barcode` columns are replaced by a fixed file-naming contract — see the sample-data requirements. |
| `MTX_TO_H5AD` | `mtx_to_h5ad_{raw,filtered,multi_raw,multi_filtered,simpleaf,kallisto_raw,kallisto_filtered,star_raw,star_filtered}` | scanpy 1.10.2 / pandas / anndata | Same template scripts per aligner (`mtx_to_h5ad_cellranger.py` — read_10x_h5, also used for cellrangerarc and the multi branch exactly like upstream's `(input_aligner in ['cellranger','cellrangerarc','cellrangermulti']) ? 'cellranger' : input_aligner`; `mtx_to_h5ad_simpleaf.py`; `mtx_to_h5ad_kallisto.py` with standard/lamanno/nac branches; `mtx_to_h5ad_star.py` incl. the Velocyto layer code, dead upstream, kept verbatim), one rule per aligner×input_type; the multi branch reads the per-sample count h5s from `per_sample_outs/<sample>/count/` (upstream `CELLRANGER_MULTI` emits the same files under `count/`). Raw/filtered gating mirrors the upstream channels: simpleaf emits only raw (upstream hardcodes `unfiltered-pl`); star/kallisto filtered conversions skip for protocols without a whitelist (dropseq/smartseq) — the upstream filtered dirs don't exist there. |
| `CELLBENDER_REMOVEBACKGROUND` | `cellbender_removebackground` | cellbender 0.3.2 | Same command `TMPDIR=. cellbender remove-background --cpu-threads … --estimator-multiple-cpu --input … --output <sample>.h5` (no `--cuda`: GPU profile is out of scope). Full output file set moved to `results/<aligner>/<sample>/cellbender_removebackground/`. Skipped for `cellrangerarc`, exactly like upstream. |
| `ANNDATA_BARCODES` | `anndata_barcodes` | anndata 0.11.4 / pandas | Same template script (barcode CSV → subset → write), same output name `<sample>_cellbender_filter_matrix.h5ad`. Skipped for `cellrangerarc` with the upstream subworkflow. |
| `CONCAT_H5AD` | `concat_h5ad_filtered`, `concat_h5ad_cellbender_filter`, `concat_h5ad_raw` | scanpy 1.10.2 | Same template script (`ad.concat(label="sample", merge="unique", index_unique="_")` + samplesheet join on `sample`). Upstream runs one process per input_type; the port has one rule per input_type. Gating mirrors the upstream channels: `filtered` skips for simpleaf (no filtered h5ads), star+dropseq and kallisto+dropseq (no filtered dirs), and smartseq (no whitelist); `raw` runs only when `skip_cellbender=true` or aligner=cellrangerarc (raw superseded by the CellBender-filtered h5ad otherwise). |
| `ANNDATAR_CONVERT` | `anndatar_convert_{filtered,cellbender_filter,raw}` + `anndatar_convert_combined_{…}` | anndataR 1.0.2, SeuratObject 5.5.0, SingleCellExperiment 1.32.0 | Same R template (read_h5ad → `as_Seurat()`/`as_SingleCellExperiment()` → saveRDS). Six rules: per sample and per combined h5ad, per input_type; type gating mirrors the concat rules. Upstream `dir.create(<sample>)` calls and versions.yml writing dropped (output dirs are pre-created by the engine; versions are recorded in `collect_versions`). |
| `softwareVersionsToYAML` + `collectFile` | `collect_versions` | — | Writes the same file `results/pipeline_info/nf_core_scrnaseq_software_mqc_versions.yml` consumed by MultiQC. Content is the port's pinned versions (upstream collates live tool versions from a channel topic, which has no oxo-flow equivalent); since containers are pinned, the recorded versions equal the executed ones. Only the active aligner's block is emitted, like the upstream channel topic. |
| `paramsSummaryMultiqc` + methods description | `workflow_summary`, `methods_description` | — | New default-ON rules producing the summary/methods MultiQC YAMLs from the copied-verbatim `assets/methods_description_template.yml` (the `${…}` placeholders are filled at render time; upstream fills them from the Nextflow workflow object, which has no oxo-flow equivalent). They run in the default config, so a single-sample default dry-run plan (`oxo-flow dry-run main.oxoflow --samples first:1`, as exercised by test/run.sh) shows 21 rules executing (19 baseline + these 2); with the two bundled samples the plan shows 29 running instances — documented new default behavior. |
| `MULTIQC` | `multiqc` | multiqc 1.34 | Same command (`multiqc --force [--title] --config <assets/multiqc_config.yml> .`) with inputs staged flat like the module's `stageAs '?/*'`; the input union covers the active aligner's web summaries/logs (FastQC + cellranger count web_summary + cellranger multi `multi/` web_summary + simpleaf quants.h5ad + STAR Log.final.out). Default `assets/multiqc_config.yml` copied verbatim from upstream. |
| `PIPELINE_COMPLETION` (email/webhook) | workflow-level hooks (no rule) | sendmail / mail / curl | Same semantics, implemented as `[workflow] on_complete` / `on_error` hooks (engine ≥ 0.17.0; older engines ignore the hook keys, so released-engine runs are untouched). Success email goes to `config.email`; failure email to `config.email` when set, else `config.email_on_fail` (upstream completionEmail address selection); webhook POST (`succeeded=`/`failed=` counters) to `config.hook_url` on both paths. Email via `sendmail -t` when available, else `mail -s`; all three keys default empty — the default run never touches mail or network tools. Best-effort like upstream: a failing notification warns, never changes the run status. |

**Not ported (with reasons):**

| Upstream branch | Reason |
|---|---|
| `skip_cellranger_renaming` (multi-lane samples) | One fastq pair per sample is supported; the staging rename hard-codes lane `L001`. |

**Other deliberate deviations** (documented per row above): FastQC is skipped
for `cellrangerarc` (five reads per sample cannot fit one static input
pattern; upstream runs it on all of them); the arc samplesheet columns are a
file-naming contract; `workflow_summary`/`methods_description` are new
default-ON rules; simpleaf/star/kallisto accept one explicit `whitelist` path
instead of upstream's automatic per-protocol mapping; the cellranger multi
branch takes its per-modality fastq paths from the metadata table instead of
upstream's `--cellranger_multi_sample_*` CLI flags (see below).

## Cell Ranger multi mode

`aligner = cellranger` runs `cellranger count` by default; setting
`cellranger_multi = true` switches the cellranger branch to the upstream
`aligner = cellrangermulti` mode — `cellranger multi` per sample, with the
same GEX reads plus any of VDJ, antibody, BEAM, CRISPR or CMO FASTQ pairs.
`count` and `multi` are mutually exclusive (the `when` gates mirror the
upstream aligner branch), and both converge on the same downstream h5ad
chain, so `cellbender`/`concat`/`anndatar` need no changes.

**Per-modality inputs via the metadata table.** Upstream feeds per-sample,
per-modality fastq groups into the module with channel branching
(`groupTuple` + EMPTY-file injection when a modality is absent) — a
variable-cardinality input set that a fixed rule signature cannot express.
The port's metadata binding (`[workflow] metadata_file`, engine ≥ 0.17.0)
replaces it: each sample's optional modality pairs live in one
`<modality>_fastq_1` / `<modality>_fastq_2` column pair of
`refs/cellranger_multi_metadata.tsv`, and an empty cell renders as `''` — the
port's equivalent of the upstream EMPTY-file injection. The `cellranger_multi`
rule reads those cells through `{meta.<modality>_fastq_1/2}` placeholders
(expanded per sample at plan time) and builds the config.csv with only the
present modalities, so the variable-cardinality config is expressible in the
shell with no engine follow-up.

**Reference selection** mirrors the upstream channels:

- GEX: `cellranger_multi_gex_reference` if set (upstream `--cellranger_index`),
  else the built `{config.transcriptome}`.
- VDJ: `cellranger_multi_vdj_reference` if set (upstream `--cellranger_vdj_index`),
  else the `cellranger_mkvdjref`-built `refs/cellranger_vdj_reference/`
  (skipped when `skip_cellrangermulti_vdjref = true`, same gate as upstream).
- Feature barcoding: `cellranger_multi_fb_reference` (upstream `--fb_reference`),
  **required when** antibody or CRISPR FASTQs are present — the rule fails
  fast with upstream's message otherwise.
- CMO: `cellranger_multi_barcodes` (upstream `--cellranger_multi_barcodes`),
  **required when** CMO FASTQs are present.

All configured paths are existence-checked before `cellranger multi` starts;
VDJ and GEX references are directory checks, the fb reference and barcodes
are file checks.

**Chemistry mapping** reuses the port's protocol→chemistry table
(`auto`→`auto`, 10XV1-4→SC3Pv1-4), with upstream's exact guard that only
cellranger accepts `protocol = 'auto'`; unrecognized protocols pass through
verbatim with a warning (upstream logs the same).

**Outputs** land at `results/<aligner>/multi/<sample>/outs/` — the upstream
module's `outs/` tree including `web_summary.html` and
`per_sample_outs/<sample>/count/sample_{filtered,raw}_feature_bc_matrix.h5`,
which feed the shared `mtx_to_h5ad_multi_{raw,filtered}` rules.

**Verification status:** the branch is validate/lint-clean, and the expanded
per-sample shells were exercised end-to-end against a `cellranger` stub that
consumes the generated config.csv and emits the declared outs tree — S1 with
VDJ + antibody produced `[gene-expression]`/`[vdj]`/`[feature]` sections and
three `[libraries]` rows; S2 without them produced the GEX-only config. A
live run needs the same `quay.io/nf-core/cellranger:10.0.0` container the
`count` branch already uses, so it only waits on a container-backed host with
the metadata table filled — queued for the next container wave.

**Live-root-caused fixes** (engine 0.15.0, tx-ubuntu): tool-facing
threads/cores use `{effective_threads}` (rules declare 12/6 CPUs; a 4-core box
would oversubscribe); every container spec is quay.io-qualified (bare
`biocontainers/...` resolves to Docker Hub, not the pinned quay.io registry);
directory-moving rules `rm -rf` the engine-precreated output parent before
`mv` (the parent exists, so `mv` would nest the tree inside itself); the STAR
index nbases heuristic truncates with `int()` and a 14 cap (the 52kb fixture
genome rounded up to 7 where STAR requires 6 — "may cause seg-fault"); the
fixture GTF gives every gene two exons with an intron (single-exon
transcripts crash simpleaf's grangers intron pass: polars "invalid series
dtype: expected List, got null"); the fixture genome is padded to ~52kb (STAR
double-frees on the original 1.9 kb genome).

## Links

- Repository: [oxo-flow-scrnaseq](https://github.com/oxo-flow-community/oxo-flow-scrnaseq)
- Upstream: [nf-core/scrnaseq](https://github.com/nf-core/scrnaseq) @ `4.2.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
