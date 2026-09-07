---
title: "Bisulfite methylation analysis: alignment, methylation calls and QC"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-methylseq</span></div>
<div class="ox-detail-cols">
<div>
<h1>Bisulfite methylation analysis: alignment, methylation calls and QC</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>
<p>Run end-to-end bisulfite methylation analysis (WGBS, and RRBS-compatible) of paired-end reads (default) and single-end reads (upstream single_end samplesheet column, via the engine metadata binding): FastQC quality control, TrimGalore adapter trimming, alignment to the bisulfite-converted reference genome with any of the four upstream aligners — Bismark bowtie2 (default), Bismark hisat2, bwameth (bwa-meth) or BWA-MEM — PCR-deduplication, samtools sort/index, methylation calls (bismark_methylation_extractor, MethylDackel on bwameth, rastair for TAPS), per-sample and project-wide Bismark HTML reports, optional QualiMap BamQC, preseq complexity estimates and targeted-sequencing (bedtools intersect + Picard HS metrics), and a final MultiQC report. All optional branches are gated on the same config keys as the upstream params and off by default.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">61</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 12 CPUs / 72 GB per rule (genome preparation, index builds, trimgalore, aligners, deduplicate, extractor)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/methylseq">nf-core/methylseq</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>4.2.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2285.1"><code>10.48546/workflowhub.workflow.2285.1</code></a></span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs reference genome and reads — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.17.0

**Toolchain.** conda envs — pinned versions (conda-forge/bioconda)

**Requirements.**

- reference genome FASTA (a .gz FASTA is decompressed automatically before indexing) — the Bismark bowtie2 index is built automatically on first run; a prebuilt index archive (--bismark_index) is also supported
- paired-end raw reads: <dir>/<sample>_R1.fastq.gz and <dir>/<sample>_R2.fastq.gz (samples with >1 pair: <dir>/<sample>_<unit>_R{1,2}.fastq.gz per unit — concatenated by cat_fastq); single-end samples: <dir>/<sample>_R1.fastq.gz only, listed as SE in metadata/samples.tsv with config.single_end_mode = true
- compute: up to 12 CPUs / 72 GB RAM per rule (bismark_genomepreparation, trimgalore, bismark_align, bismark_deduplicate, bismark_methylationextractor, bwameth_index, bwameth_align, bwa_mem)
- conda or mamba to create the pinned per-rule environments
- disk: space in config.out_dir (default results/) for aligned BAMs, methylation calls and reports

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-methylseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-methylseq
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. The list below names the rules that read each key.</p>
<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>accel</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>aligner</code><span class="ox-param-default">bismark</span></div>
<p class="ox-param-desc">Aligner (upstream: --aligner, default &#x27;bismark&#x27;). One of:<br>&#x27;bismark&#x27;       - bowtie2, the default main path<br>&#x27;bismark_hisat&#x27; - hisat2 (needs a --known_splices GTF for splice sites)<br>&#x27;bwameth&#x27;       - bwa-meth (needs a --use_mem2 flag to use the mem2 index)<br>&#x27;bwamem&#x27;        - BWA-MEM (TAPS-optimized)</p>
<details class="ox-param-usedby"><summary>used by 52 rules</summary>
<div class="ox-param-rules"><code>bedtools_intersect</code> <code>bedtools_intersect_bwameth</code> <code>bedtools_intersect_bwameth_chg</code> <code>bedtools_intersect_bwameth_chh</code> <code>bismark_align</code> <code>bismark_align_se</code> <code>bismark_coverage2cytosine</code> <code>bismark_deduplicate</code> <code>bismark_deduplicate_se</code> <code>bismark_genomepreparation</code> <code>bismark_methylationextractor</code> <code>bismark_methylationextractor_se</code> <code>bismark_report</code> <code>bismark_report_se</code> <code>bismark_summary</code> <code>bismark_untar</code> <code>bwa_index</code> <code>bwa_mem</code> <code>bwameth_align</code> <code>bwameth_index</code> <code>methyldackel_extract</code> <code>methyldackel_extract_allcontexts</code> <code>methyldackel_extract_methylkit</code> <code>methyldackel_mbias</code> <code>multiqc</code> <code>multiqc_bwamem</code> <code>multiqc_bwameth</code> <code>picard_addorreplacereadgroups</code> <code>picard_collecthsmetrics</code> <code>picard_collecthsmetrics_alt</code> <code>picard_markduplicates</code> <code>picard_markduplicates_bwamem</code> <code>preseq_lcextrap</code> <code>preseq_lcextrap_alt</code> <code>qualimap_bamqc</code> <code>qualimap_bamqc_alt</code> <code>rastair_call_bwamem</code> <code>rastair_call_bwameth</code> <code>rastair_mbias_bwamem</code> <code>rastair_mbias_bwameth</code> <code>rastair_mbiasparser</code> <code>rastair_methylkit</code> <code>samtools_faidx</code> <code>samtools_flagstat</code> <code>samtools_idxstats</code> <code>samtools_index</code> <code>samtools_index_alignment</code> <code>samtools_index_deduplicated</code> <code>samtools_index_deduplicated_bwamem</code> <code>samtools_sort</code> <code>samtools_sort_alignment</code> <code>samtools_stats</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>all_contexts</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Methyldackel options (upstream params with the same defaults, active on<br>the bwameth branch when TAPS is off)</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>bedtools_intersect_bwameth_chg</code> <code>bedtools_intersect_bwameth_chh</code> <code>methyldackel_extract</code> <code>methyldackel_extract_allcontexts</code> <code>methyldackel_extract_methylkit</code> <code>methyldackel_mbias</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>bamqc_regions_file</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Targeted-sequencing inputs (upstream: --target_regions_file /<br>--bamqc_regions_file, default empty)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>qualimap_bamqc</code> <code>qualimap_bamqc_alt</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>bismark_index</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Prebuilt Bismark index archive (.tar.gz/.tar.bz2, as produced by<br>bismark_genome_preparation). Empty string (default) = build the index from<br>config.fasta (upstream default). When set, the archive is untarred into<br>refs/BismarkIndex and the build is skipped, like the upstream UNTAR module.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_genomepreparation</code> <code>bismark_untar</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cat_fastq</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">Concatenate multi-pair fastqs (upstream: CAT_FASTQ — always active for<br>samples with &gt;1 fastq pair; upstream has no param for it). Set to false<br>only when every sample has a single pair: multi-pair samples would then<br>lack the merged reads the downstream rules consume.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>cat_fastq_r1</code> <code>cat_fastq_r2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>clip_r1</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">Trimming options (upstream params with the same defaults)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>clip_r2</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">Trimming options (upstream params with the same defaults)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>collecthsmetrics</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Collect Picard HS metrics within the targeted-sequencing branch<br>(upstream: --collecthsmetrics, default false)</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>multiqc</code> <code>multiqc_bwameth</code> <code>picard_bedtointervallist</code> <code>picard_collecthsmetrics</code> <code>picard_collecthsmetrics_alt</code> <code>picard_createsequencedictionary</code> <code>samtools_faidx</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>comprehensive</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_methylationextractor</code> <code>bismark_methylationextractor_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cytosine_report</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Bismark options</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bismark_coverage2cytosine</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>em_seq</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>fasta</code><span class="ox-param-default">test/fixtures/refs/genome.fa</span></div>
<p class="ox-param-desc">Reference genome (upstream: --fasta). Uncompressed FASTA (a .gz FASTA is<br>decompressed automatically before indexing, like the upstream GUNZIP<br>module). The Bismark index is built from it automatically (upstream default<br>when --bismark_index is not supplied). Point this at your genome; the repo<br>default ships the tiny test fixture.</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>bismark_genomepreparation</code> <code>bwa_index</code> <code>bwameth_align</code> <code>bwameth_index</code> <code>samtools_faidx</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ignore_3prime_r1</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_methylationextractor</code> <code>bismark_methylationextractor_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ignore_3prime_r2</code><span class="ox-param-default">2</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bismark_methylationextractor</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ignore_flags</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Methyldackel options (upstream params with the same defaults, active on<br>the bwameth branch when TAPS is off)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>methyldackel_extract</code> <code>methyldackel_extract_allcontexts</code> <code>methyldackel_extract_methylkit</code> <code>methyldackel_mbias</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ignore_r1</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_methylationextractor</code> <code>bismark_methylationextractor_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ignore_r2</code><span class="ox-param-default">2</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bismark_methylationextractor</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>known_splices</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">bismark_hisat splice-site GTF (upstream: --known_splices, default empty).<br>When set and aligner = &#x27;bismark_hisat&#x27;, bismark is given the splice sites<br>extracted from this file (upstream uses process substitution for the same<br>data).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>length_trim</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">Trimming options (upstream params with the same defaults)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>local_alignment</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>maxins</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>merge_context</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Methyldackel options (upstream params with the same defaults, active on<br>the bwameth branch when TAPS is off)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>methyldackel_extract</code> <code>methyldackel_extract_allcontexts</code> <code>methyldackel_extract_methylkit</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>meth_cutoff</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_methylationextractor</code> <code>bismark_methylationextractor_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>methyl_kit</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Methyldackel options (upstream params with the same defaults, active on<br>the bwameth branch when TAPS is off)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>methyldackel_extract_methylkit</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>min_depth</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">Methyldackel options (upstream params with the same defaults, active on<br>the bwameth branch when TAPS is off)</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>methyldackel_extract</code> <code>methyldackel_extract_allcontexts</code> <code>methyldackel_extract_methylkit</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>minins</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>multiqc_title</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">MultiQC</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>multiqc</code> <code>multiqc_bwamem</code> <code>multiqc_bwameth</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>nextseq_trim</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">Trimming options (upstream params with the same defaults)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>no_overlap</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bismark_methylationextractor</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>nomeseq</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Bismark options</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>bismark_coverage2cytosine</code> <code>bismark_methylationextractor</code> <code>bismark_methylationextractor_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>non_directional</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>num_mismatches</code><span class="ox-param-default">0.6</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>out_dir</code><span class="ox-param-default">results</span></div>
<p class="ox-param-desc">Input reads directory: raw/&lt;sample&gt;_R1.fastq.gz + _R2.fastq.gz (paired-end).<br>The repo default ships the tiny test fixtures; point this at your data.</p>
<details class="ox-param-usedby"><summary>used by 55 rules</summary>
<div class="ox-param-rules"><code>bedtools_intersect</code> <code>bedtools_intersect_bwameth</code> <code>bedtools_intersect_bwameth_chg</code> <code>bedtools_intersect_bwameth_chh</code> <code>bismark_align</code> <code>bismark_align_se</code> <code>bismark_coverage2cytosine</code> <code>bismark_deduplicate</code> <code>bismark_deduplicate_se</code> <code>bismark_methylationextractor</code> <code>bismark_methylationextractor_se</code> <code>bismark_report</code> <code>bismark_report_se</code> <code>bismark_summary</code> <code>bwa_mem</code> <code>bwameth_align</code> <code>cat_fastq_r1</code> <code>cat_fastq_r2</code> <code>fastqc</code> <code>fastqc_se</code> <code>methyldackel_extract</code> <code>methyldackel_extract_allcontexts</code> <code>methyldackel_extract_methylkit</code> <code>methyldackel_mbias</code> <code>multiqc</code> <code>multiqc_bwamem</code> <code>multiqc_bwameth</code> <code>multiqc_versions</code> <code>picard_addorreplacereadgroups</code> <code>picard_bedtointervallist</code> <code>picard_collecthsmetrics</code> <code>picard_collecthsmetrics_alt</code> <code>picard_markduplicates</code> <code>picard_markduplicates_bwamem</code> <code>preseq_lcextrap</code> <code>preseq_lcextrap_alt</code> <code>qualimap_bamqc</code> <code>qualimap_bamqc_alt</code> <code>rastair_call_bwamem</code> <code>rastair_call_bwameth</code> <code>rastair_mbias_bwamem</code> <code>rastair_mbias_bwameth</code> <code>rastair_mbiasparser</code> <code>rastair_methylkit</code> <code>samtools_flagstat</code> <code>samtools_idxstats</code> <code>samtools_index</code> <code>samtools_index_alignment</code> <code>samtools_index_deduplicated</code> <code>samtools_index_deduplicated_bwamem</code> <code>samtools_sort</code> <code>samtools_sort_alignment</code> <code>samtools_stats</code> <code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>pbat</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code> <code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>raw_dir</code><span class="ox-param-default">test/fixtures/raw</span></div>
<p class="ox-param-desc">Input reads directory: raw/&lt;sample&gt;_R1.fastq.gz + _R2.fastq.gz (paired-end).<br>The repo default ships the tiny test fixtures; point this at your data.</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>cat_fastq_r1</code> <code>cat_fastq_r2</code> <code>fastqc</code> <code>fastqc_se</code> <code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>relax_mismatches</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rrbs</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>bismark_deduplicate</code> <code>bismark_deduplicate_se</code> <code>multiqc_bwameth</code> <code>picard_markduplicates</code> <code>samtools_index_deduplicated</code> <code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_preseq</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Optional QC branches (upstream params, all off by default)</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>multiqc</code> <code>multiqc_bwamem</code> <code>multiqc_bwameth</code> <code>preseq_lcextrap</code> <code>preseq_lcextrap_alt</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_qualimap</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Optional QC branches (upstream params, all off by default)</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>multiqc</code> <code>multiqc_bwamem</code> <code>multiqc_bwameth</code> <code>qualimap_bamqc</code> <code>qualimap_bamqc_alt</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_targeted_sequencing</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Optional QC branches (upstream params, all off by default)</p>
<details class="ox-param-usedby"><summary>used by 10 rules</summary>
<div class="ox-param-rules"><code>bedtools_intersect</code> <code>bedtools_intersect_bwameth</code> <code>bedtools_intersect_bwameth_chg</code> <code>bedtools_intersect_bwameth_chh</code> <code>multiqc</code> <code>multiqc_bwameth</code> <code>picard_bedtointervallist</code> <code>picard_collecthsmetrics</code> <code>picard_collecthsmetrics_alt</code> <code>picard_createsequencedictionary</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>single_cell</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code> <code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>single_end_mode</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Single-end reads (upstream: the samplesheet <code>single_end</code> column, absent<br>fastq_2 -&gt; single_end). Off by default (all samples paired-end, the<br>byte-identical default). Set to true AND uncomment [workflow]<br>metadata_file to route samples per-row: metadata/samples.tsv lists each<br>sample&#x27;s <code>endedness</code> (SE or PE); a sample without a row — or with no<br>metadata_file at all — stays paired-end. The SE branches are separate<br>gated rules mirroring the upstream per-sample routing (bismark chain:<br>fastqc_se -&gt; trimgalore_se -&gt; bismark_align_se -&gt; bismark_deduplicate_se<br>-&gt; bismark_methylationextractor_se -&gt; bismark_report_se; the bwameth/<br>bwamem aligners take the trimmed single read directly). Requires<br>oxo-flow &gt;= 0.17.0: on older engines <code>{meta.*}</code> is inert, so the SE rules<br>stay closed while this key is false.</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>bismark_align_se</code> <code>bismark_deduplicate_se</code> <code>bismark_methylationextractor_se</code> <code>bismark_report_se</code> <code>fastqc_se</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_deduplication</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Skip options (upstream: --skip_fastqc / --skip_trimming / --skip_deduplication /<br>--skip_multiqc). Same defaults as upstream.</p>
<details class="ox-param-usedby"><summary>used by 9 rules</summary>
<div class="ox-param-rules"><code>bismark_deduplicate</code> <code>bismark_deduplicate_se</code> <code>multiqc_bwamem</code> <code>multiqc_bwameth</code> <code>picard_addorreplacereadgroups</code> <code>picard_markduplicates</code> <code>picard_markduplicates_bwamem</code> <code>samtools_index_deduplicated</code> <code>samtools_index_deduplicated_bwamem</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_fastqc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Skip options (upstream: --skip_fastqc / --skip_trimming / --skip_deduplication /<br>--skip_multiqc). Same defaults as upstream.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>fastqc</code> <code>fastqc_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_multiqc</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Skip options (upstream: --skip_fastqc / --skip_trimming / --skip_deduplication /<br>--skip_multiqc). Same defaults as upstream.</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>multiqc</code> <code>multiqc_bwamem</code> <code>multiqc_bwameth</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_trimming</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Skip options (upstream: --skip_fastqc / --skip_trimming / --skip_deduplication /<br>--skip_multiqc). Same defaults as upstream.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_trimming_presets</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Trimming options (upstream params with the same defaults)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>slamseq</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bismark_genomepreparation</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>taps</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">TAPS protocol (upstream: --taps, default false). Runs rastair conversion<br>on the alignments. Only meaningful with the bwameth or bwamem aligners<br>(upstream builds no fasta index for TAPS on the bismark aligners, so<br>rastair silently produces nothing there — replicated).</p>
<details class="ox-param-usedby"><summary>used by 14 rules</summary>
<div class="ox-param-rules"><code>bedtools_intersect</code> <code>bedtools_intersect_bwameth</code> <code>bedtools_intersect_bwameth_chg</code> <code>bedtools_intersect_bwameth_chh</code> <code>methyldackel_extract</code> <code>methyldackel_extract_allcontexts</code> <code>methyldackel_extract_methylkit</code> <code>methyldackel_mbias</code> <code>picard_collecthsmetrics</code> <code>picard_collecthsmetrics_alt</code> <code>rastair_call_bwameth</code> <code>rastair_mbias_bwameth</code> <code>rastair_mbiasparser</code> <code>rastair_methylkit</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>target_regions_file</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Targeted-sequencing inputs (upstream: --target_regions_file /<br>--bamqc_regions_file, default empty)</p>
<details class="ox-param-usedby"><summary>used by 5 rules</summary>
<div class="ox-param-rules"><code>bedtools_intersect</code> <code>bedtools_intersect_bwameth</code> <code>bedtools_intersect_bwameth_chg</code> <code>bedtools_intersect_bwameth_chh</code> <code>picard_bedtointervallist</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>three_prime_clip_r1</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">Trimming options (upstream params with the same defaults)</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>three_prime_clip_r2</code><span class="ox-param-default">0</span></div>
<p class="ox-param-desc">Trimming options (upstream params with the same defaults)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>trimgalore</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>unmapped</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">The port&#x27;s DAG consumes the merged (--comprehensive) methylation-call<br>outputs, so the default differs from upstream (false): the per-strand<br>split files would leave the declared outputs unmoved.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>use_mem2</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">bwameth index variant (upstream: --use_mem2, default false).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bwameth_index</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>zymo</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Library presets (upstream params with the same defaults).</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>bismark_align</code> <code>bismark_align_se</code> <code>trimgalore</code> <code>trimgalore_se</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Rule-level detail (exact DAG)</summary>
<div class="ox-dag-card">
<img src="/assets/dag/oxo-flow-methylseq-rules.svg?v=9c3d0fe63c" alt="oxo-flow-methylseq rule-level detail" loading="lazy">
</div>
</details>
<details class="ox-flow-view">
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<img src="/assets/dag/oxo-flow-methylseq.svg?v=19ce1aaac8" alt="oxo-flow-methylseq pipeline overview" loading="lazy">

<p class="ox-dag-caption">figure · oxo-flow-methylseq — Run end-to-end bisulfite methylation analysis (WGBS, and RRBS-compatible) of paired-end reads (default) and single-end reads (upstream single_end samplesheet column, via the engine metadata binding): FastQC quality control, TrimGalore adapter trimming, alignment to the bisulfite-converted reference genome with any of the four upstream aligners — Bismark bowtie2 (default), Bismark hisat2, bwameth (bwa-meth) or BWA-MEM — PCR-deduplication, samtools sort/index, methylation calls (bismark_methylation_extractor, MethylDackel on bwameth, rastair for TAPS), per-sample and project-wide Bismark HTML reports, optional QualiMap BamQC, preseq complexity estimates and targeted-sequencing (bedtools intersect + Picard HS metrics), and a final MultiQC report.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- bismark_genomepreparation
- bismark_untar
- bwameth_index
- bwa_index
- samtools_faidx
- cat_fastq_r1
- cat_fastq_r2
- fastqc
- fastqc_se
- trimgalore
- trimgalore_se
- bismark_align
- bismark_align_se
- bwameth_align
- bwa_mem
- samtools_sort
- samtools_sort_alignment
- samtools_index
- samtools_index_alignment
- samtools_flagstat
- samtools_stats
- samtools_idxstats
- bismark_deduplicate
- bismark_deduplicate_se
- picard_markduplicates
- samtools_index_deduplicated
- picard_addorreplacereadgroups
- picard_markduplicates_bwamem
- samtools_index_deduplicated_bwamem
- bismark_methylationextractor
- bismark_methylationextractor_se
- methyldackel_extract
- methyldackel_extract_allcontexts
- methyldackel_extract_methylkit
- methyldackel_mbias
- rastair_mbias_bwameth
- rastair_mbias_bwamem
- rastair_mbiasparser
- rastair_call_bwameth
- rastair_call_bwamem
- rastair_methylkit
- bismark_coverage2cytosine
- bismark_report
- bismark_report_se
- bismark_summary
- qualimap_bamqc
- qualimap_bamqc_alt
- preseq_lcextrap
- preseq_lcextrap_alt
- picard_createsequencedictionary
- picard_bedtointervallist
- bedtools_intersect
- bedtools_intersect_bwameth
- bedtools_intersect_bwameth_chg
- bedtools_intersect_bwameth_chh
- picard_collecthsmetrics
- picard_collecthsmetrics_alt
- multiqc_versions
- multiqc
- multiqc_bwameth
- multiqc_bwamem

**Excluded**

- Parabricks fq2bammeth GPU alignment path (gpu profile; `PARABRICKS_FQ2BAMMETH` in fastq_align_dedup_bwameth + process_gpu accelerator) — not ported; the port runs bwameth on CPU only

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` / `fastqc_se` | fastqc 0.12.1 | identical command; `--memory` derived from task resources. The `_se` variant runs the single-end chain (reads named `{sample}.fastq.gz`, outputs `{sample}_fastqc.*`) when `single_end_mode` is on |
| TRIMGALORE | `trimgalore` / `trimgalore_se` | trim-galore 0.6.10, cutadapt 4.9, pigz 2.8 | identical command incl. library-preset clipping and `--cores` clamp. The `_se` variant is the upstream SE module: R1-side clipping only, `--cores cpus-3` clamped to [1, 8] |
| BISMARK_GENOMEPREPARATION | `bismark_genomepreparation` | bismark 0.25.1, gzip 1.13 | `--bowtie2` (or `--hisat2` for bismark_hisat, `--slam` for slamseq); runs when no prebuilt index is supplied (upstream default) |
| GUNZIP | (merged into the index-preparation shells) | gzip 1.13 | a gzipped reference FASTA is decompressed before index building, as in the upstream fasta_index_methylseq subworkflow |
| UNTAR | `bismark_untar` | tar 1.34 | active only when a prebuilt `--bismark_index` archive is supplied; strips a single top-level directory, like upstream |
| BISMARK_ALIGN | `bismark_align` / `bismark_align_se` | bismark 0.25.1 | identical flag order (pbat/non_directional/unmapped/score_min/local/minins/maxins/multicore); hisat2 splice sites via `known_splices` (see deviations). The `_se` variant drops `--minins`/`--maxins` (upstream `!meta.single_end` gate), keeps `--multicore` and the hisat2 rename |
| BISMARK_DEDUPLICATE | `bismark_deduplicate` / `bismark_deduplicate_se` | bismark 0.25.1 | identical command (`-s` for single-end, `-p` paired-end); skipped with `skip_deduplication`/`rrbs` like upstream |
| SAMTOOLS_SORT | `samtools_sort` | samtools 1.22.1, htslib 1.22.1 | upstream prefix `${sample}.deduplicated.sorted`; takes the SE deduplicated BAM when the sample is single-end |
| SAMTOOLS_INDEX | `samtools_index` | samtools 1.22.1 | identical command |
| BISMARK_METHYLATIONEXTRACTOR | `bismark_methylationextractor` / `bismark_methylationextractor_se` | bismark 0.25.1 | identical flag order on the **deduplicated** BAM; `--multicore`/`--buffer_size` derived from resources. The `_se` variant uses `-s` and drops `--no_overlap`/`--ignore_r2`/`--ignore_3prime_r2` (upstream `!meta.single_end` gate) |
| BISMARK_COVERAGE2CYTOSINE | `bismark_coverage2cytosine` | bismark 0.25.1 | off by default; runs with `cytosine_report`/`nomeseq`; takes the SE coverage file when the sample is single-end |
| BISMARK_REPORT | `bismark_report` / `bismark_report_se` | bismark 0.25.1 | bismark2report run with the four reports co-located, as in the upstream workdir; the `_se` variant feeds the `*_SE_report.txt` files |
| BISMARK_SUMMARY | `bismark_summary` | bismark 0.25.1 | bismark2summary with upstream BAM-name arguments; per-sample SE/PE detection via a `[ -f ]` probe on the SE alignment report (no per-sample binding; see deviations) |
| BWAMETH_INDEX | `bwameth_index` | bwameth 0.2.9 | `bwameth.py index`, or `index-mem2` with `use_mem2`; index dir `refs/BwamethIndex` |
| BWAMETH_ALIGN | `bwameth_align` | bwameth 0.2.9 | identical command (reference symlink re-created in the index dir, `samtools view -bhS`); one or two reads are passed positionally per sample (SE/PE from its metadata row — CPU-only exact command as upstream's non-GPU branch; the upstream GPU path (`params.aligner == "bwameth"` under the gpu profile → `PARABRICKS_FQ2BAMMETH`) is not ported, see Excluded |
| BWA_INDEX | `bwa_index` | bwa 0.7.19 | `bwa index -p`; upstream sizes memory dynamically (5.37x FASTA) — the port uses a fixed 4 threads/24G/24h budget (see deviations) |
| BWA_MEM | `bwa_mem` | bwa 0.7.19, samtools 1.22.1 | upstream `sort_bam = true`: `bwa mem \| samtools sort`; index prefix found by globbing `*.amb`; one or two reads passed positionally per sample (SE/PE) |
| SAMTOOLS_INDEX_ALIGNMENTS | `samtools_index_alignment` | samtools 1.22.1 | index of the sorted alignment BAM (bwameth/bwamem) |
| SAMTOOLS_FLAGSTAT | `samtools_flagstat` | samtools 1.22.1 | identical command |
| SAMTOOLS_STATS | `samtools_stats` | samtools 1.22.1 | identical command |
| SAMTOOLS_IDXSTATS | `samtools_idxstats` | samtools 1.22.1 | bwamem branch; `--threads cpus-1` as upstream |
| PICARD_MARKDUPLICATES | `picard_markduplicates` / `picard_markduplicates_bwamem` | picard 3.4.0 | identical args (ASSUME_SORTED/REMOVE_DUPLICATES/LENIENT/PROGRAM_RECORD_ID null/TMP_DIR); -Xmx = 0.8 x memory |
| PICARD_ADDORREPLACEREADGROUPS | `picard_addorreplacereadgroups` | picard 3.4.0 | identical args; upstream does not publish this BAM — the port declares it so the DAG can consume it |
| SAMTOOLS_INDEX_DEDUPLICATED | `samtools_index_deduplicated` / `samtools_index_deduplicated_bwamem` | samtools 1.22.1 | index of the deduplicated BAM |
| METHYLDACKEL_EXTRACT | `methyldackel_extract` (+ `_allcontexts`, `_methylkit`) | methyldackel 0.6.1 | same flags (CHG/CHH, mergeContext, ignoreFlags, minDepth, methylKit); the methylKit table and the all-contexts bedGraphs are separate gated rules (see deviations) |
| METHYLDACKEL_MBIAS | `methyldackel_mbias` | methyldackel 0.6.1 | identical command |
| RASTAIR_MBIAS | `rastair_mbias_bwameth` / `rastair_mbias_bwamem` | rastair 0.8.2 | active with `taps` on bwameth and always on bwamem, exactly like the upstream `if (params.taps \|\| aligner == 'bwamem')` |
| RASTAIR_MBIASPARSER | `rastair_mbiasparser` | rastair 0.8.2, r-base 4.4.0 | plot_mbias.R + parse_mbias.R |
| RASTAIR_CALL | `rastair_call_bwameth` / `rastair_call_bwamem` | rastair 0.8.2 | trim values flow from the mbiasparser CSV (see deviations) |
| RASTAIR_METHYLKIT | `rastair_methylkit` | rastair 0.8.2 | `rastair_call_to_methylkit.sh \| gzip` |
| QUALIMAP_BAMQC | `qualimap_bamqc` / `qualimap_bamqc_alt` | qualimap 2.3 | `-p non-strand-specific`, `--gff` with `bamqc_regions_file`, `_JAVA_OPTIONS` tmpdir; `--collect-overlap-pairs` only for paired-end samples (upstream `!meta.single_end` gate) |
| PRESEQ_LCEXTRAP | `preseq_lcextrap` / `preseq_lcextrap_alt` | preseq 3.2.0 | `-verbose -bam`, `-pe` only for paired-end samples (upstream `!meta.single_end` gate); the `*.command.log` is preseq's own stderr (see deviations) |
| PICARD_CREATESEQUENCEDICTIONARY | `picard_createsequencedictionary` | picard 3.4.0 | runs only when `collecthsmetrics` is requested, like upstream |
| PICARD_BEDTOINTERVALLIST | `picard_bedtointervallist` | picard 3.4.0 | output named `target_regions.intervallist` (fixed name; see deviations) |
| BEDTOOLS_INTERSECT | `bedtools_intersect` (+ `_bwameth`, `_chg`, `_chh`) | bedtools 2.31.1 | prefix = the bedGraph basename, suffix `targeted.bedGraph`, as upstream; the bismark variant takes the SE bedGraph when the sample is single-end |
| PICARD_COLLECTHSMETRICS | `picard_collecthsmetrics` / `picard_collecthsmetrics_alt` | picard 3.4.0 | same intervals for bait and target; excluded on the taps/bwamem branches, like the upstream rastair error |
| SAMTOOLS_FAIDX | `samtools_faidx` | samtools 1.22.1, htslib 1.22.1, gzip 1.13 | stages the reference at `refs/FastaRef/reference.fa`; upstream gate (bwameth/bwamem/collecthsmetrics) reproduced |
| MULTIQC | `multiqc` / `multiqc_bwameth` / `multiqc_bwamem` | multiqc 1.32 | one rule per aligner branch; same search space as upstream (fastqc zips, trimgalore logs, samtools stats/flagstat/idxstats, picard metrics + qualimap/preseq/HS extras), plus the single-end report names (`{sample}_fastqc.zip`, `{sample}.fastq.gz_trimming_report.txt`, `*_SE_report.txt`, ...) which are picked up exactly when present; the methyldackel/rastair outputs are not fed to MultiQC, exactly like upstream |
| softwareVersionsToYAML + collectFile | `multiqc_versions` | — | upstream extracts versions at runtime; port pins the module versions statically |
| CAT_FASTQ | `cat_fastq_r1` / `cat_fastq_r2` | coreutils 9.5 | ported via the engine's `input_groups` primitive (issue #227, oxo-flow >= 0.17.0): one instance per sample with >1 fastq pair, R1s and R2s concatenated into `results/fastq/<sample>_R{1,2}.fastq.gz`; single-pair samples pass through unchanged (downstream falls back to the raw pair). Upstream's single process is split into two rules (one per read); see deviations |

Additional notes: single-end samples are supported via the engine's
metadata binding (see Usage); `--save_*` / `publish_dir_mode` params are N/A
(oxo-flow publishes every declared output); per-process `withName:` resource
overrides are baked into `[rules.resources]` (upstream labels
process_single/low/medium/high + BISMARK_ALIGN 8d / DEDUPLICATE 2d /
METHYLATIONEXTRACTOR 1d time limits).

### Documented deviations

Each deviation is cosmetic or a mechanism swap — the effective commands and
outputs match upstream:

1. **bismark_hisat output names** — hisat2-mode alignments are renamed from
   the upstream `_bismark_hisat2_` infix (bismark 0.24.x names, live-verified)
   to the canonical `_bismark_bt2_` names so the shared downstream chain works
   unchanged (cosmetic).
2. **`--known-splicesite-infile`** — upstream passes
   `<(...)` (process substitution); the port materializes the same
   `hisat2_extract_splice_sites.py` output to a temp file (bash process
   substitution does not survive variable expansion).
3. **`--PROGRAM_RECORD_ID null`** — passed unquoted; the upstream quotes are
   Groovy escaping and the effective value is the bare word `null`.
4. **preseq `*.command.log`** — upstream copies the whole Nextflow task
   stderr (`.command.err`); oxo-flow has no such file, so the port's log is
   preseq's stderr (the informative part of the upstream log).
5. **Canonical staging names** — the Bismark index dir always contains the
   FASTA as `reference.fa`, the bwameth/bwamem/HS branches use
   `refs/FastaRef/reference.fa` + `refs/RefDict/reference.dict`, and
   `picard_bedtointervallist` writes `target_regions.intervallist` (upstream
   uses the BED file's basename). Names differ; content and ordering do not.
6. **Envs consolidated** — the upstream GUNZIP/UNTAR coreutils env is merged
   into the tool envs (gzip added to `bismark_genomeprep`/`samtools_faidx`,
   since the bioconda bismark 0.25.1 build does not depend on gzip), and the
   four upstream rastair envs are consolidated into one
   (`rastair=0.8.2=*_2` + `r-base=4.4.0`, the build that ships the R helper
   scripts) for every rastair rule.
7. **TAPS on the bismark aligners** — upstream builds no fasta index for
   `taps && aligner =~ /bismark/`, so BAM_TAPS_CONVERSION silently produces
   nothing there; the port replicates that (no bismark-family rastair rules)
   instead of the upstream's silent no-op.
8. **`bwa_index` resources** — upstream requests `5.37 x fasta.size()`
   memory dynamically; the port uses a fixed 4 threads / 24G / 24h budget
   (adequate for ~4GB genomes).
9. **`skip_deduplication`/`rrbs` on the bwameth/bwamem branches** — upstream
   passes the *alignment* BAM downstream when dedup is skipped; the port's
   methyldackel/rastair/qualimap/preseq/HS-metrics rules consume the
   deduplicated BAM, so those branches require deduplication. Upstream's
   dedup-independent callers behave identically when dedup runs (the default).
10. **MethylDackel `--methylKit`** — the tool emits only `*.methylKit` files
    when the flag is given, so the port runs `methyldackel_extract_methylkit`
    as a separate gated rule *in addition to* the bedGraph-producing run
    (the upstream module emits both outputs from one invocation; oxo-flow
    validates every declared output, so the split is required).
11. **MultiQC per aligner** — one `multiqc` rule per aligner branch with the
    branch's always-present files declared and the conditional extras
    (qualimap dirs, preseq logs, HS metrics, picard metrics) symlinked
    in-shell when they exist — the engine cannot declare conditional inputs.
12. **CAT_FASTQ as two rules + a shell fallback** — upstream runs one
    `CAT_FASTQ` process on `ch_samplesheet.multiple` and mixes its outputs
    with `ch_samplesheet.single`. The port splits the merge into
    `cat_fastq_r1` / `cat_fastq_r2` (the engine's `input_groups` allows one
    pattern per rule — see the docs' "Input Groups" section), each
    instantiating only for samples whose raw files carry a unit segment
    (`<sample>_<unit>_R{1,2}.fastq.gz`), and the downstream
    `fastqc`/`trimgalore` rules declare both the concatenated pair
    (`optional = "any"`) and the raw pair, using the concatenated one when
    it exists and the raw pair otherwise. Effective commands and outputs
    match upstream (a sample named with a single unit is copied through —
    `cat` of one file — which is the same content as the pass-through).
    Needs oxo-flow >= 0.17.0; on older engines the `cat_fastq` rules fail
    loudly instead of writing empty fastqs.
13. **Single-end via engine metadata** — upstream decides `single_end` per
    sample from the samplesheet (`fastq_2` absent); the port binds it with
    the engine's metadata feature (`[workflow] metadata_file` +
    `{meta.endedness}`, oxo-flow >= 0.17.0) instead of a samplesheet, gated
    on `config.single_end_mode` (off by default — the default run is
    unchanged). Paired-end rules carry a `{meta.endedness} != 'SE'` when-gate
    (a sample without a metadata row renders `'' != 'SE'` and stays
    paired-end) and six `*_se` variant rules reproduce the upstream SE
    modules verbatim (`-s` extractor/dedup, no `--minins`/`--maxins`, no
    `--collect-overlap-pairs`, no `-pe`, R1-side-only clipping, SE output
    names). The engine bakes the metadata literals into the `when`
    conditions and the per-sample shell selections at plan time.
14. **Per-sample SE detection in cohort rules** — `bismark_summary` and
    `multiqc` run once over the whole cohort (no per-sample binding), so
    they cannot read `{meta.endedness}` per sample. `bismark_summary`
    probes for each sample's SE alignment report with `[ -f ]` and picks the
    SE or PE BAM names accordingly, and the multiqc search loops list the SE
    report names, which are picked up exactly when present. Same effective
    behavior as the upstream per-sample `meta.single_end` branching.

## Links

- Repository: [oxo-flow-methylseq](https://github.com/oxo-flow-community/oxo-flow-methylseq)
- Upstream: [nf-core/methylseq](https://github.com/nf-core/methylseq) @ `4.2.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
