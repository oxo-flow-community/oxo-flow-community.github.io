---
title: "Single-cell RNA-seq: alignment, quantification and QC"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-scrnaseq</span></div>
<div class="ox-detail-cols">
<div>
<h1>Single-cell RNA-seq: alignment, quantification and QC</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>
<p>Single-cell RNA-seq analysis from raw FASTQ reads to a final MultiQC report, on all six upstream aligner branches of nf-core/scrnaseq 4.2.0: cellranger (default, count or multi with per-modality GEX/VDJ/Ab/BEAM/CRISPR/CMO via the metadata table), simpleaf (upstream default; index + quant + optional QCatch), kallisto/bustools (standard/lamanno/nac), STARsolo (incl. legacy iGenomes index upgrade), and cellrangerarc multiome ATAC+GEX. Shared downstream path: FastQC, mtx→h5ad conversion per aligner, CellBender ambient-RNA background removal (skipped for cellrangerarc, like upstream), sample-wise h5ad concatenation, optional Seurat/SingleCellExperiment export, workflow summary + methods description, MultiQC.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">46</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 12 CPUs / 72 GB per rule (Cell Ranger)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">single-cell</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/scrnaseq">nf-core/scrnaseq</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>4.2.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2280.1"><code>10.48546/workflowhub.workflow.2280.1</code></a></span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs Cell Ranger reference data and reads — see Requirements; preview with `oxo-flow dry-run main.oxoflow`.

## Installation

**Engine.** oxo-flow >= 0.12.0

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

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. The list below names the rules that read each key.</p>
<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>aligner</code><span class="ox-param-default">cellranger</span></div>
<p class="ox-param-desc">--aligner / --protocol. The port implements ALL upstream aligner branches:<br>cellranger (default, matches upstream&#x27;s most-tested path), simpleaf (upstream<br>default aligner), kallisto (kallisto/bustools), star (STARsolo) and<br>cellrangerarc (multiome ATAC+GEX). Protocol values are mapped per aligner<br>inside the alignment rules (upstream protocols.json); &#x27;auto&#x27; is only valid<br>for cellranger/cellrangerarc, exactly like upstream.</p>
<details class="ox-param-usedby"><summary>used by 41 rules</summary>
<div class="ox-param-rules"><code>anndata_barcodes</code> <code>anndatar_convert_cellbender_filter</code> <code>anndatar_convert_combined_cellbender_filter</code> <code>anndatar_convert_combined_filtered</code> <code>anndatar_convert_combined_raw</code> <code>anndatar_convert_filtered</code> <code>anndatar_convert_raw</code> <code>cellbender_removebackground</code> <code>cellranger_count</code> <code>cellranger_mkgtf</code> <code>cellranger_mkref</code> <code>cellranger_mkvdjref</code> <code>cellranger_multi</code> <code>cellrangerarc_count</code> <code>cellrangerarc_mkgtf</code> <code>cellrangerarc_mkref</code> <code>collect_versions</code> <code>concat_h5ad_cellbender_filter</code> <code>concat_h5ad_filtered</code> <code>concat_h5ad_raw</code> <code>fastqc</code> <code>kallistobustools_count</code> <code>kallistobustools_ref_standard</code> <code>kallistobustools_ref_velocity</code> <code>mtx_to_h5ad_filtered</code> <code>mtx_to_h5ad_kallisto_filtered</code> <code>mtx_to_h5ad_kallisto_raw</code> <code>mtx_to_h5ad_multi_filtered</code> <code>mtx_to_h5ad_multi_raw</code> <code>mtx_to_h5ad_raw</code> <code>mtx_to_h5ad_simpleaf</code> <code>mtx_to_h5ad_star_filtered</code> <code>mtx_to_h5ad_star_raw</code> <code>multiqc</code> <code>qcatch</code> <code>simpleaf_index</code> <code>simpleaf_quant</code> <code>star_align</code> <code>star_genomegenerate</code> <code>star_genomeparams_upgrade</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>build_cellranger_index</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">cellranger reference: build from fasta/gtf, or point transcriptome at an existing index</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>cellranger_mkgtf</code> <code>cellranger_mkref</code> <code>cellrangerarc_mkgtf</code> <code>cellrangerarc_mkref</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellranger_localmem</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">GB passed to cellranger&#x27;s --localmem (mkref/count). 0 = auto: 2/3 of<br>the actually-free physical memory (/proc/meminfo MemAvailable, 1 GB<br>floor) — never the engine&#x27;s effective memory, which counts swap:<br>cellranger&#x27;s jobmngr waits forever when --localmem exceeds the free<br>RAM (live: &#x27;Need 6 GB ... (2.6 GB available)&#x27; looped for hours on a<br>3.7GB box). Set a positive number to force a value.</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>cellranger_count</code> <code>cellranger_mkref</code> <code>cellranger_mkvdjref</code> <code>cellranger_multi</code> <code>cellrangerarc_count</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellranger_multi</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">cellranger multi (upstream aligner = cellrangermulti): the multiome<br>VDJ / Ab-seq / CRO branch. OFF by default. Enabling it supersedes<br>cellranger_count (upstream&#x27;s aligner branches are exclusive). Per-sample<br>per-modality FASTQs come from the [workflow] metadata_file table<br>(refs/cellranger_multi_metadata.tsv): one pair per modality per sample in<br>columns &lt;modality&gt;_fastq_1/&lt;modality&gt;_fastq_2 for vdj/ab/beam/crispr/cmo;<br>an empty cell = modality absent for that sample — the engine renders<br>{meta.&lt;col&gt;} as &#x27;&#x27;, the port&#x27;s equivalent of upstream&#x27;s EMPTY-file<br>injection (the exclusion is closed without an engine follow-up).</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>cellranger_count</code> <code>cellranger_mkvdjref</code> <code>cellranger_multi</code> <code>mtx_to_h5ad_filtered</code> <code>mtx_to_h5ad_multi_filtered</code> <code>mtx_to_h5ad_multi_raw</code> <code>mtx_to_h5ad_raw</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellranger_multi_barcodes</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">upstream --cellranger_multi_barcodes: barcode table (sample,multiplexed_sample_id,description[,cmo_ids])</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>cellranger_multi</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellranger_multi_fb_reference</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">upstream --fb_reference: feature-barcoding reference (antibody/CRISPR)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>cellranger_multi</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellranger_multi_gex_reference</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">upstream --cellranger_index; empty = the built {config.transcriptome}</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>cellranger_multi</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellranger_multi_vdj_reference</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">upstream --cellranger_vdj_index; empty = built by cellranger_mkvdjref</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>cellranger_mkvdjref</code> <code>cellranger_multi</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellrangerarc_config</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">optional mkref config json (upstream --cellrangerarc_config); auto-generated when empty</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>cellrangerarc_mkref</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cellrangerarc_reference</code><span class="ox-param-default">refs/cellrangerarc_reference</span></div>
<p class="ox-param-desc">cellrangerarc reference (multiome ATAC+GEX)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>cellrangerarc_count</code> <code>cellrangerarc_mkref</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>email</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">completion notifications (nf-core PIPELINE_COMPLETION port): summary email<br>on success (<code>email</code>), failure address (<code>email_on_fail</code>) and a webhook<br>(<code>hook_url</code>). Empty = no notification, exactly like upstream&#x27;s empty email<br>params. Consumed by the workflow-level on_complete / on_error hooks above<br>(engine &gt;= 0.17.0); older engines ignore the hook keys and the run is<br>untouched.</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>email_on_fail</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">failure-only recipient (upstream --email_on_fail; used when email is empty)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>expected_cells</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">samplesheet <code>expected_cells</code> column -&gt; --expect-cells/--soloCellFilter when set</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>cellranger_count</code> <code>cellranger_multi</code> <code>cellrangerarc_count</code> <code>star_align</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>fasta</code><span class="ox-param-default">refs/refdata.fa.gz</span></div>
<p class="ox-param-desc">reference genome (upstream --fasta / --gtf; may be .gz)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>gunzip_fasta</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>fasta_gz</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">upstream --fasta gzipped flag (gunzipped by the prep rule)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gunzip_fasta</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>fasta_prepared</code><span class="ox-param-default">refs/refdata.fa</span></div>
<p class="ox-param-desc">derived reference files (README &quot;Reference genome&quot; explains the chain)</p>
<details class="ox-param-usedby"><summary>used by 9 rules</summary>
<div class="ox-param-rules"><code>cellranger_mkref</code> <code>cellranger_mkvdjref</code> <code>cellrangerarc_mkref</code> <code>gtf_gene_filter</code> <code>gunzip_fasta</code> <code>kallistobustools_ref_standard</code> <code>kallistobustools_ref_velocity</code> <code>simpleaf_index</code> <code>star_genomegenerate</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf</code><span class="ox-param-default">refs/refdata.gtf.gz</span></div>
<p class="ox-param-desc">annotation GTF (upstream --gtf; may be .gz)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>gunzip_gtf</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_filtered</code><span class="ox-param-default">refs/refdata_genes.gtf</span></div>
<p class="ox-param-desc">gene-level GTF for cellranger/count filtering (upstream filtered_gtf; the &quot;biotype = protein_coding&quot; filter)</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>cellrangerarc_mkgtf</code> <code>gtf_gene_filter</code> <code>gtf_source_fix</code> <code>kallistobustools_ref_standard</code> <code>kallistobustools_ref_velocity</code> <code>simpleaf_index</code> <code>star_align</code> <code>star_genomegenerate</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_gz</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">upstream --gtf gzipped flag (gunzipped by the prep rule)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gunzip_gtf</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_mkgtf</code><span class="ox-param-default">refs/refdata_genes.filtered.gtf</span></div>
<p class="ox-param-desc">cellranger mkgtf output (the filtered annotation)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>cellranger_mkgtf</code> <code>cellranger_mkref</code> <code>cellranger_mkvdjref</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_mkgtf_input</code><span class="ox-param-default">refs/refdata_genes.gtf</span></div>
<p class="ox-param-desc">set to the source-fixed file when gtf_source_fix=true</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>cellranger_mkgtf</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_prepared</code><span class="ox-param-default">refs/refdata.gtf</span></div>
<p class="ox-param-desc">gunzipped GTF (prep-rule output)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>gtf_gene_filter</code> <code>gunzip_gtf</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_source_fix</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">iGenomes GTF source-field rewrite (opt-in, upstream gtf_source_has_spaces)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gtf_source_fix</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_source_fixed</code><span class="ox-param-default">refs/refdata_genes.source_fixed.gtf</span></div>
<p class="ox-param-desc">source-field-rewritten GTF (gtf_source_fix output)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>gtf_source_fix</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>hook_url</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">webhook URL for the on_complete / on_error notifications</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>kallisto_index</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">kallisto/bustools</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>kallistobustools_count</code> <code>kallistobustools_ref_standard</code> <code>kallistobustools_ref_velocity</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>kb_t1c</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">optional cdna_t2c.txt override</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>kallistobustools_count</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>kb_t2c</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">optional intron_t2c.txt override</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>kallistobustools_count</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>kb_workflow</code><span class="ox-param-default">standard</span></div>
<p class="ox-param-desc">standard | lamanno | nac (any non-standard builds the intron index too)</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>kallistobustools_count</code> <code>kallistobustools_ref_standard</code> <code>kallistobustools_ref_velocity</code> <code>mtx_to_h5ad_kallisto_filtered</code> <code>mtx_to_h5ad_kallisto_raw</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>multiqc_config</code><span class="ox-param-default">assets/multiqc_config.yml</span></div>
<p class="ox-param-desc">MultiQC config path (upstream --multiqc_config)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>multiqc</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>multiqc_title</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">-&gt; <code>--title</code> when set</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>multiqc</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>out_dir</code><span class="ox-param-default">results</span></div>
<p class="ox-param-desc">results directory (upstream --outdir)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>protocol</code><span class="ox-param-default">auto</span></div>
<p class="ox-param-desc">cellranger/arc: &#x27;auto&#x27; or 10XV1-4; simpleaf/kallisto/star: 10XV1-4/dropseq(/smartseq)</p>
<details class="ox-param-usedby"><summary>used by 13 rules</summary>
<div class="ox-param-rules"><code>anndatar_convert_combined_filtered</code> <code>anndatar_convert_filtered</code> <code>cellranger_count</code> <code>cellranger_multi</code> <code>concat_h5ad_filtered</code> <code>kallistobustools_count</code> <code>mtx_to_h5ad_kallisto_filtered</code> <code>mtx_to_h5ad_star_filtered</code> <code>mtx_to_h5ad_star_raw</code> <code>qcatch</code> <code>simpleaf_quant</code> <code>star_align</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>qcatch_n_partitions</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">qcatch --n_partitions when set (for protocols without a chemistry mapping)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>qcatch</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>remove_doublets</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream --remove_doublets: doublet removal for simpleaf</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>qcatch</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>samplesheet</code><span class="ox-param-default">test/fixtures/samplesheet.csv</span></div>
<p class="ox-param-desc">consumed by CONCAT_H5AD (same columns as upstream)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>concat_h5ad_cellbender_filter</code> <code>concat_h5ad_filtered</code> <code>concat_h5ad_raw</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>save_align_intermeds</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">-&gt; <code>--create-bam true</code> (cellranger) / publish the BAM (star)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>cellranger_count</code> <code>cellranger_multi</code> <code>star_align</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>seq_center</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">--outSAMattrRGline CN field when set</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>star_align</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>simpleaf_index</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">simpleaf (upstream default aligner)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>simpleaf_index</code> <code>simpleaf_quant</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>simpleaf_umi_resolution</code><span class="ox-param-default">cr-like</span></div>
<p class="ox-param-desc">upstream --simpleaf_umi_resolution (cr-like | paired | naive)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>simpleaf_quant</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_cellbender</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream --skip_cellbender: skip ambient-RNA background removal</p>
<details class="ox-param-usedby"><summary>used by 10 rules</summary>
<div class="ox-param-rules"><code>anndata_barcodes</code> <code>anndatar_convert_cellbender_filter</code> <code>anndatar_convert_combined_cellbender_filter</code> <code>anndatar_convert_combined_raw</code> <code>anndatar_convert_raw</code> <code>cellbender_removebackground</code> <code>collect_versions</code> <code>concat_h5ad_cellbender_filter</code> <code>concat_h5ad_raw</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_cellrangermulti_vdjref</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream same name: skip the VDJ reference build</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>cellranger_mkvdjref</code> <code>cellranger_multi</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_fastqc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">QC / reporting knobs</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>fastqc</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_multiqc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream --skip_multiqc</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>multiqc</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_qcatch</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream --skip_qcatch: skip the qcatch QC step</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>qcatch</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>star_feature</code><span class="ox-param-default">Gene</span></div>
<p class="ox-param-desc">--soloFeatures (Gene | Gene Velocyto | ...)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>mtx_to_h5ad_star_filtered</code> <code>mtx_to_h5ad_star_raw</code> <code>star_align</code> <code>workflow_summary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>star_ignore_sjdbgtf</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">skip --sjdbGTFfile</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>star_align</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>star_index</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">STARsolo</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>star_align</code> <code>star_genomegenerate</code> <code>star_genomeparams_upgrade</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>star_index_legacy</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upgrade a legacy 2.6.x iGenomes index (genomeParameters rewrite)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>star_genomeparams_upgrade</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>transcript_fasta</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">transcript FASTA for simpleaf index building (mutually exclusive with fasta/gtf)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>simpleaf_index</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>transcriptome</code><span class="ox-param-default">refs/cellranger_reference</span></div>
<p class="ox-param-desc">cellranger reference dir (upstream --transcriptome): built by cellranger_mkref, or an existing index</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>cellranger_count</code> <code>cellranger_mkref</code> <code>cellranger_multi</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>txp2gene</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">t2g map (required with transcript_fasta; also used as the kallisto t2g)</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>kallistobustools_count</code> <code>mtx_to_h5ad_kallisto_filtered</code> <code>mtx_to_h5ad_kallisto_raw</code> <code>simpleaf_index</code> <code>simpleaf_quant</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>whitelist</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">barcode whitelist for simpleaf/star. Empty = mapped per protocol from<br>assets/whitelist/10x_V{1..4}_barcode_whitelist.txt.gz (upstream<br>protocols.json behavior); set a path to override.</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>simpleaf_quant</code> <code>star_align</code> <code>workflow_summary</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

<img src="../assets/dag/oxo-flow-scrnaseq.svg?v=6f91dd3a86" alt="oxo-flow-scrnaseq pipeline overview" loading="lazy">

<p class="ox-dag-caption">figure · oxo-flow-scrnaseq — Single-cell RNA-seq analysis from raw FASTQ reads to a final MultiQC report, on all six upstream aligner branches of nf-core/scrnaseq 4.2.0: cellranger (default, count or multi with per-modality GEX/VDJ/Ab/BEAM/CRISPR/CMO via the metadata table), simpleaf (upstream default; index + quant + optional QCatch), kallisto/bustools (standard/lamanno/nac), STARsolo (incl.</p>

</div>

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
