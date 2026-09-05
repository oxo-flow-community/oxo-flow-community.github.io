---
title: "Nanopore long-read: demultiplexing, QC and alignment"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-nanoseq</span></div>
<div class="ox-detail-cols">
<div>
<h1>Nanopore long-read: demultiplexing, QC and alignment</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>
<p>A nanopore long-read pipeline: samplesheet check, qcat barcode demultiplexing, NanoPlot + FastQC QC, minimap2 (or graphmap2) alignment, samtools view/sort/index, samtools stats/flagstat/idxstats, BigWig/BigBed tracks, NanoLyse contamination filtering, medaka/DeepVariant/PEPPER-Margin-DeepVariant short variant calling, Sniffles/cuteSV structural variant calling, bambu/StringTie2+featureCounts quantification with DESeq2/DEXSeq differential analysis, Nanopolish+xPore/m6anet RNA modification analysis, JAFFA RNA fusion detection (cDNA/directRNA; reference bundle auto-downloaded from figshare or supplied via config.jaffal_ref_dir as a directory or tar.gz), pre-aligned-BAM input, and a MultiQC report. The default path is the DNA protocol with all gated branches off by default (matching upstream). Every rule runs the upstream module&#x27;s exact pinned container image.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">54</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 12 CPUs / 84 GB per rule (minimap2 index)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/nanoseq">nf-core/nanoseq</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>3.1.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

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

<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>aligner</code><span class="ox-param-default">minimap2</span></div>
<p class="ox-param-desc">-- Alignment</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>graphmap2_align</code> <code>graphmap2_index</code> <code>minimap2_align</code> <code>minimap2_index</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>bam_suffix</code><span class="ox-param-default">.sorted.bam</span></div>
<p class="ox-param-desc">-- Suffix appended to per-sample bam names wherever rules consume reads: &quot;.sorted.bam&quot; (alignment branch) or &quot;.bam&quot; (skip_alignment branch, user bams linked by bam_rename). Mirrors the upstream channel swap between BAM_SORT_INDEX_SAMTOOLS.out.sortbam and BAM_RENAME.out.bam.</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>bambu</code> <code>nanopolish_index_eventalign</code> <code>stringtie2</code> <code>subread_featurecounts</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>barcode_kit</code><span class="ox-param-default">RBK001</span></div>
<p class="ox-param-desc">-- Demultiplexing (upstream defaults) RBK001 matches the shipped barcoded fixture (qcat Auto-detection needs at least two distinct barcodes to guess the kit; the explicit kit makes the test path deterministic).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>qcat</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>call_variants</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">-- Variant calling (upstream default: off; also gated upstream on protocol == DNA). The three short-variant callers are mutually exclusive on variant_caller; structural callers on structural_variant_caller (upstream defaults: medaka / sniffles).</p>
<details class="ox-param-usedby"><summary>used by 17 rules</summary>
<div class="ox-param-rules"><code>cutesv</code> <code>cutesv_sort_vcf</code> <code>cutesv_tabix_vcf</code> <code>deepvariant</code> <code>deepvariant_tabix_gvcf</code> <code>deepvariant_tabix_vcf</code> <code>medaka_bgzip_vcf</code> <code>medaka_tabix_vcf</code> <code>medaka_variant</code> <code>minimap2_align</code> <code>pepper_margin_deepvariant</code> <code>samtools_index</code> <code>samtools_sort</code> <code>samtools_sort_index</code> <code>sniffles</code> <code>sniffles_sort_vcf</code> <code>sniffles_tabix_vcf</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>deepvariant_gpu</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>pepper_margin_deepvariant</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">-- GTF annotation (upstream samplesheet gtf column; empty on the default path)</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>bambu</code> <code>graphmap2_align</code> <code>graphmap2_index</code> <code>gtf2bed</code> <code>stringtie2</code> <code>stringtie_merge</code> <code>xpore_dataprep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>gtf_base</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>gtf2bed</code> <code>minimap2_align</code> <code>minimap2_index</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>input</code><span class="ox-param-default">test/fixtures/samplesheet.csv</span></div>
<p class="ox-param-desc">-- Samplesheet and demultiplexing input (upstream: --input / --input_path)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>samplesheet_check</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>input_path</code><span class="ox-param-default">test/fixtures/raw/sample.fastq.gz</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>qcat</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>jaffal_ref_dir</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>get_jaffal_ref</code> <code>jaffal_ref</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>multiqc_config</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>multiqc</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>multiqc_title</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">-- MultiQC options</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>multiqc</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>nanolyse_fasta</code><span class="ox-param-default">test/fixtures/refs/lambda.fasta.gz</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>nanolyse</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>nanopolish_fast5</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>m6anet_dataprep</code> <code>m6anet_inference</code> <code>nanopolish_index_eventalign</code> <code>xpore_dataprep</code> <code>xpore_diffmod</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>out_dir</code><span class="ox-param-default">results</span></div>
<p class="ox-param-desc">-- Output directory (upstream: --outdir, default ./results)</p>
<details class="ox-param-usedby"><summary>used by 54 rules</summary>
<div class="ox-param-rules"><code>bam_rename</code> <code>bambu</code> <code>bedtools_bamtobed</code> <code>bedtools_genomecov</code> <code>cutesv</code> <code>cutesv_sort_vcf</code> <code>cutesv_tabix_vcf</code> <code>deepvariant</code> <code>deepvariant_tabix_gvcf</code> <code>deepvariant_tabix_vcf</code> <code>deseq2</code> <code>deseq2_featurecounts</code> <code>dexseq</code> <code>dexseq_featurecounts</code> <code>dumpsoftwareversions</code> <code>fastqc</code> <code>get_chrom_sizes</code> <code>get_jaffal_ref</code> <code>graphmap2_align</code> <code>graphmap2_index</code> <code>gtf2bed</code> <code>jaffal_ref</code> <code>m6anet_dataprep</code> <code>m6anet_inference</code> <code>medaka_bgzip_vcf</code> <code>medaka_tabix_vcf</code> <code>medaka_variant</code> <code>minimap2_align</code> <code>minimap2_index</code> <code>multiqc</code> <code>nanolyse</code> <code>nanoplot</code> <code>nanopolish_index_eventalign</code> <code>pepper_margin_deepvariant</code> <code>qcat</code> <code>samplesheet_check</code> <code>samtools_faidx</code> <code>samtools_flagstat</code> <code>samtools_idxstats</code> <code>samtools_index</code> <code>samtools_sort</code> <code>samtools_sort_index</code> <code>samtools_stats</code> <code>samtools_view</code> <code>sniffles</code> <code>sniffles_sort_vcf</code> <code>sniffles_tabix_vcf</code> <code>stringtie2</code> <code>stringtie_merge</code> <code>subread_featurecounts</code> <code>ucsc_bed12tobigbed</code> <code>ucsc_bedgraphtobigwig</code> <code>xpore_dataprep</code> <code>xpore_diffmod</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>phase_vcf</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>medaka_variant</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>protocol</code><span class="ox-param-default">DNA</span></div>
<p class="ox-param-desc">-- Protocol (upstream: --protocol; mandatory upstream, one of DNA/cDNA/directRNA)</p>
<details class="ox-param-usedby"><summary>used by 34 rules</summary>
<div class="ox-param-rules"><code>bambu</code> <code>bedtools_bamtobed</code> <code>cutesv</code> <code>cutesv_sort_vcf</code> <code>cutesv_tabix_vcf</code> <code>deepvariant</code> <code>deepvariant_tabix_gvcf</code> <code>deepvariant_tabix_vcf</code> <code>deseq2</code> <code>deseq2_featurecounts</code> <code>dexseq</code> <code>dexseq_featurecounts</code> <code>get_jaffal_ref</code> <code>graphmap2_align</code> <code>graphmap2_index</code> <code>jaffal_ref</code> <code>m6anet_dataprep</code> <code>m6anet_inference</code> <code>medaka_bgzip_vcf</code> <code>medaka_tabix_vcf</code> <code>medaka_variant</code> <code>minimap2_align</code> <code>minimap2_index</code> <code>nanopolish_index_eventalign</code> <code>pepper_margin_deepvariant</code> <code>sniffles</code> <code>sniffles_sort_vcf</code> <code>sniffles_tabix_vcf</code> <code>stringtie2</code> <code>stringtie_merge</code> <code>subread_featurecounts</code> <code>ucsc_bed12tobigbed</code> <code>xpore_dataprep</code> <code>xpore_diffmod</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>qcat_detect_middle</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>qcat</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>qcat_min_score</code><span class="ox-param-default">60</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>qcat</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>quantification_method</code><span class="ox-param-default">bambu</span></div>
<p class="ox-param-desc">-- Quantification and differential analysis (upstream defaults: on, but gated upstream to protocol cDNA/directRNA — never on the DNA path)</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>bambu</code> <code>deseq2</code> <code>deseq2_featurecounts</code> <code>dexseq</code> <code>dexseq_featurecounts</code> <code>stringtie2</code> <code>stringtie_merge</code> <code>subread_featurecounts</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>reference</code><span class="ox-param-default">test/fixtures/refs/genome.fa</span></div>
<p class="ox-param-desc">-- Reference genome (collapses the samplesheet fasta column; the default path uses a single reference for all samples, as in the upstream test data)</p>
<details class="ox-param-usedby"><summary>used by 14 rules</summary>
<div class="ox-param-rules"><code>bambu</code> <code>cutesv</code> <code>deepvariant</code> <code>get_chrom_sizes</code> <code>graphmap2_align</code> <code>graphmap2_index</code> <code>medaka_variant</code> <code>minimap2_index</code> <code>nanopolish_index_eventalign</code> <code>pepper_margin_deepvariant</code> <code>samtools_faidx</code> <code>samtools_stats</code> <code>stringtie2</code> <code>xpore_dataprep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>reference_name</code><span class="ox-param-default">genome.fa</span></div>
<p class="ox-param-desc">Basename of the reference; mirrors the upstream staged-file name so that indexes keep the upstream naming (genome.fa.mmi / genome.fa.sizes / genome.fa.fai)</p>
<details class="ox-param-usedby"><summary>used by 10 rules</summary>
<div class="ox-param-rules"><code>deepvariant</code> <code>get_chrom_sizes</code> <code>graphmap2_align</code> <code>graphmap2_index</code> <code>minimap2_align</code> <code>minimap2_index</code> <code>pepper_margin_deepvariant</code> <code>samtools_faidx</code> <code>ucsc_bed12tobigbed</code> <code>ucsc_bedgraphtobigwig</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_nanolyse</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">-- Raw read cleaning (upstream default: off). Upstream downloads the lambda genome when --nanolyse_fasta is unset (GET_NANOLYSE_FASTA); the port ships it as a checked-in fixture.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>nanolyse</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>sample_bams</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">-- Pre-aligned BAM input (upstream: the samplesheet input_file column carrying .bam files, used only when --skip_alignment; the port takes a comma-separated list of bam paths, one per barcode in samples_list order, linked by the bam_rename rule)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bam_rename</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_alignment</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 18 rules</summary>
<div class="ox-param-rules"><code>bam_rename</code> <code>bedtools_bamtobed</code> <code>bedtools_genomecov</code> <code>get_chrom_sizes</code> <code>graphmap2_align</code> <code>graphmap2_index</code> <code>minimap2_align</code> <code>minimap2_index</code> <code>samtools_faidx</code> <code>samtools_flagstat</code> <code>samtools_idxstats</code> <code>samtools_index</code> <code>samtools_sort</code> <code>samtools_sort_index</code> <code>samtools_stats</code> <code>samtools_view</code> <code>ucsc_bed12tobigbed</code> <code>ucsc_bedgraphtobigwig</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_bigbed</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bedtools_bamtobed</code> <code>ucsc_bed12tobigbed</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_bigwig</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">-- Visualisation (upstream defaults: bigwig/bigbed ON; bigbed is protocol-gated upstream to cDNA/directRNA and so never runs on the default DNA path)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bedtools_genomecov</code> <code>ucsc_bedgraphtobigwig</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_demultiplexing</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>qcat</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_differential_analysis</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>deseq2</code> <code>deseq2_featurecounts</code> <code>dexseq</code> <code>dexseq_featurecounts</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_fastqc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>fastqc</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_fusion_analysis</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">-- RNA fusion analysis (upstream default: on, gated to protocol cDNA/directRNA; skip_fusion_analysis / jaffal_ref_dir). The reference bundle is auto-downloaded from figshare when jaffal_ref_dir is unset (upstream GET_JAFFAL_REF + UNTAR); a user-supplied path is untarred (.tar.gz/.tgz/.tar) or symlinked (directory) instead, A12-style.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>get_jaffal_ref</code> <code>jaffal_ref</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_m6anet</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>m6anet_dataprep</code> <code>m6anet_inference</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_modification_analysis</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">-- RNA modification analysis (upstream default: on, gated to protocol directRNA; the fast5 dir comes from the upstream samplesheet nanopolish_fast5 column — the port takes one dir for all samples)</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>m6anet_dataprep</code> <code>m6anet_inference</code> <code>nanopolish_index_eventalign</code> <code>xpore_dataprep</code> <code>xpore_diffmod</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_multiqc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>multiqc</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_nanoplot</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>nanoplot</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_qc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">-- QC (upstream defaults: all QC on)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>fastqc</code> <code>nanoplot</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_quantification</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>bambu</code> <code>deseq2</code> <code>deseq2_featurecounts</code> <code>dexseq</code> <code>dexseq_featurecounts</code> <code>stringtie2</code> <code>stringtie_merge</code> <code>subread_featurecounts</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_sv</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>cutesv</code> <code>cutesv_sort_vcf</code> <code>cutesv_tabix_vcf</code> <code>sniffles</code> <code>sniffles_sort_vcf</code> <code>sniffles_tabix_vcf</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_vc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>deepvariant</code> <code>deepvariant_tabix_gvcf</code> <code>deepvariant_tabix_vcf</code> <code>medaka_bgzip_vcf</code> <code>medaka_tabix_vcf</code> <code>medaka_variant</code> <code>pepper_margin_deepvariant</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_xpore</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>xpore_dataprep</code> <code>xpore_diffmod</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>split_mnps</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>medaka_variant</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>stranded</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>minimap2_align</code> <code>minimap2_index</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>structural_variant_caller</code><span class="ox-param-default">sniffles</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>cutesv</code> <code>cutesv_sort_vcf</code> <code>cutesv_tabix_vcf</code> <code>sniffles</code> <code>sniffles_sort_vcf</code> <code>sniffles_tabix_vcf</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>variant_caller</code><span class="ox-param-default">medaka</span></div>
<p class="ox-param-desc">—</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>deepvariant</code> <code>deepvariant_tabix_gvcf</code> <code>deepvariant_tabix_vcf</code> <code>medaka_bgzip_vcf</code> <code>medaka_tabix_vcf</code> <code>medaka_variant</code> <code>pepper_margin_deepvariant</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-nanoseq rule-level DAG](../assets/dag/oxo-flow-nanoseq.svg)

<p class="ox-dag-caption">figure · oxo-flow-nanoseq — rule-level transit map (nf-metro)</p>

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` and rendered with [nf-metro](https://github.com/seqeralabs/nf-metro) — rules are grouped into colored transit lines by analysis stage. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

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
