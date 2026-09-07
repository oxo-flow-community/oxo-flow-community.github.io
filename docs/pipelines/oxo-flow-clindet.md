---
title: "Cancer genome & transcriptome analysis (WES/WGS/RNA, single entry): somatic+germline+CNV+SV calling, MAF annotation, case report"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-clindet</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Cancer genome &amp; transcriptome analysis (WES/WGS/RNA, single entry): somatic+germline+CNV+SV calling, MAF annotation, case report</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">wes</span><span class="ox-tag">wgs</span><span class="ox-tag">rna</span><span class="ox-tag">somatic</span><span class="ox-tag">germline</span><span class="ox-tag">cnv</span><span class="ox-tag">sv</span><span class="ox-tag">unpaired</span><span class="ox-tag">tumor-only</span><span class="ox-tag">maf</span><span class="ox-tag">vep</span><span class="ox-tag">vcf2maf</span><span class="ox-tag">mutect2</span><span class="ox-tag">vardict</span><span class="ox-tag">varscan2</span><span class="ox-tag">muse</span><span class="ox-tag">strelka2</span><span class="ox-tag">caveman</span><span class="ox-tag">delly</span><span class="ox-tag">svaba</span><span class="ox-tag">manta</span><span class="ox-tag">control-freec</span><span class="ox-tag">sequenza</span><span class="ox-tag">exomedepth</span><span class="ox-tag">ascat</span><span class="ox-tag">arriba</span><span class="ox-tag">trust4</span><span class="ox-tag">isofox</span><span class="ox-tag">bqsr</span></div>
<p class="ox-desc">Port of zyllifeworld/clindet in its upstream single-Snakefile form: one entry file, config run_type (wes|wgs|rna) selects the rule tree, and paired vs tumor-only WES is derived PER PAIR from the sample sheet (a pair without a control runs the tumor-only tree — engine wildcard-scoped when predicates). 188 rules: somatic SNV (Mutect2, VarDict, VarScan2, MuSE, HaplotypeCaller) + germline (Strelka2+Manta, CaVEMan); tumor-only callers (Mutect2/HaplotypeCaller/varscan2/Strelka/vardict/lofreq/freebayes); CNV subset (Control-FREEC, Sequenza, ExomeDepth, ASCAT); WGS SV (delly chain incl. germ, svaba, Manta somaticSV); opt-in BQSR; vcf2maf/VEP MAF annotation, region flagging, cancer report, MultiQC; RNA fusion/expression (arriba/TRUST4/isofox). Live-verified per run type on tx-ubuntu.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/WangLabCSU/oxo-flow-clindet" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">188</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 30 threads / 10 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">cancer genomics (WES/WGS/RNA)</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/zyllifeworld/clindet">zyllifeworld/clindet</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>582a9131</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2299.1"><code>10.48546/workflowhub.workflow.2299.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastp</span><span class="tchip">bwa (&gt;=0.7.18)</span><span class="tchip">samtools</span><span class="tchip">gatk4 4.6.2.0 (container)</span><span class="tchip">bcftools &gt;=1.22</span><span class="tchip">bgzip</span><span class="tchip">tabix</span><span class="tchip">varscan 2.4.6</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>clindet pipeline</strong>: one entry point (<code>wes</code>/<code>wgs</code> = DNA, <code>rna</code> = RNA) calling somatic, germline and tumor-only variants, copy-number, SV, fusion and QC analysis, ending in merged VCF/MAF, case report and MultiQC.</p>
<p><strong>Shared inputs</strong> — pairs split into tumor/normal: <code>fastp_tumor_sample</code>/<code>fastp_normal_sample</code> trim, BWA mem aligns (<code>map_reads_tumor</code>, <code>map_reads_normal</code>), <code>mark_duplicates_tumor</code>/<code>mark_duplicates_normal</code> deduplicate, and <code>recal_link_tumor</code>/<code>recal_link_normal</code> (or <code>recalibrate_base_qualities_tumor</code> → <code>apply_base_quality_recalibration_tumor</code>, BQSR on) feed DNA rules.</p>
<p><strong>DNA module</strong></p>
<p>1. <strong>Sequencing quality</strong> — <code>bam_flagstat_tumor</code>/<code>bam_flagstat_normal</code>; <code>bed_to_interval_list</code> feeds <code>picard_collect_wes_tumor</code>/<code>picard_collect_wes_normal</code> (WGS: <code>picard_collect_wgs_tumor</code>, <code>picard_flength_wgs_tumor</code>); <code>prep_multiqc_data</code> and WGS/tumor-only variants lead to <code>combined_multiqc_prep_multiqc_data</code> → <code>combined_multiqc</code>.</p>
<p>2. <strong>Somatic and germline calling</strong> — <code>call_variants_HaplotypeCaller</code>, <code>vardict_paired_mode</code> → <code>vardict_filter_somatic</code>, <code>varscan2_mpileup</code> → <code>varscan2_call</code> → <code>varscan2_som_filter</code> → <code>varscan2_merge_somatic</code>, MuSE <code>muse_call</code> → <code>muse_sump</code>, Mutect2 (<code>mutect2</code>, <code>M2_ST</code>/<code>M2_SNC</code> → <code>M2_contam</code> → <code>M2_filter</code>), CaVEMan <code>CM_call</code> → <code>CM_flag</code>/<code>CM_germ_flag</code>; germline: <code>call_config_strelka</code> → <code>call_strelka_manta_germline</code>/<code>call_strelka_somatic_manta</code> → <code>merge_strelka_manta</code>/<code>merge_strelka_somatic_manta</code>; WGS reruns them on whole-genome data.</p>
<p>3. <strong>Tumor-only calling</strong> — control-less pairs run <code>unpaired_mutect2_call</code> → <code>M2_filter_unpaired</code>, <code>unpaired_call_config_strelka</code> → <code>unpaired_call_strelka_manta</code> → <code>unpaired_strelka_filter</code>, <code>unpaired_vardict_single_mode</code> → <code>unpaired_filter_vardict</code>, <code>lofreq_somatic_unpaired</code> → <code>unpair_lofreq_filter</code>, <code>varscan2_mpileup_unpaired</code> → <code>varscan2_merge_unpaired</code> (via <code>varscan2_call_unpaired_snp</code>/indel twin), plus <code>unpaired_call_variants_HaplotypeCaller</code>/<code>unpaired_freebayes</code>; <code>merge_unpaired_vcf</code> → <code>all_unpaired</code>.</p>
<p>4. <strong>Normalization and outputs</strong> — <code>vcf_norm_Mutect2</code>/<code>vcf_norm_vardict</code> and twins precede MAF conversion (<code>vcf2maf_Mutect2</code> and siblings); <code>merge_paired_vcf</code> → <code>all_vcf</code>; <code>merge_paired_maf</code> feeds <code>flag_mutation_pairead_maf</code> (<code>make_region_bed_list</code>) and <code>run_cancer_report</code>. CNV (<code>freec_config</code> → <code>freec_call_paired</code> → <code>plot_freec</code>; <code>sequenza_bam2seqz</code> → <code>sequenza_seqz_binning</code> → <code>sequenza_call</code>; <code>CNA_ASCAT</code> → <code>ASCAT_EXTRACT_PURITYPLOIDY</code>, <code>CNA_exomedepth</code>) fills <code>all_cnv</code>; WGS SVs (<code>SV_delly</code> → <code>SV_delly_filter_somatic</code> → <code>SV_delly_to_vcf</code> → <code>delly_filter</code> → <code>delly2bnd</code>, <code>SV_svaba</code> → <code>SV_sansa_anno_svaba</code>, Manta via <code>call_config_strelka_wgs</code>) fill <code>all_sv</code>.</p>
<p><strong>RNA module</strong></p>
<p>1. <strong>QC, alignment, quant</strong> — <code>fastp_trim</code>; <code>STAR_1_pass</code>, then <code>STAR_arriba_map</code>/<code>STAR_mut_map</code> re-align (plus <code>STAR_isofox_map</code> → <code>isofox_call</code>, <code>cal_exp_RSEM</code> → <code>RSEM_sort_genome</code>).
2. <strong>Fusion and immune receptors</strong> — <code>arriba_fusion</code> → <code>arriba_draw</code> (plus RSEM BAM) and <code>TRUST4_TBCR</code>.
3. <strong>Mutation and MAF</strong> — <code>link_bam</code> → <code>SplitNCigarReads</code> unlocks <code>mutect2_call</code> → <code>M2_filter_unpaired_rna</code>, <code>call_variants_HaplotypeCaller_rna</code>, <code>unpaired_freebayes_rna</code>, <code>unpaired_call_config_strelka_rna</code> → <code>unpaired_call_strelka_manta_rna</code> → <code>unpaired_strelka_filter_rna</code>, <code>lofreq_call_up</code> → <code>lofreq_norm_filter</code>, <code>unpaired_vardict_single_mode_rna</code> → <code>unpaired_filter_vardict_rna</code>, and the varscan2 RNA chain (<code>varscan2_mpileup_unpaired_rna</code> → SNP/indel calls → <code>varscan2_filter_snp</code> and the indel twin → <code>varscan2_merge_unpaired_rna</code>); each converts to MAF (<code>vcf2maf_rna_freebayes</code>, <code>vcf2maf_rna_Mutect2</code> and siblings).</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-clindet+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>


<div class="ox-tryit">
<div class="ox-tryit-title">⬡ Try it — clone &amp; run</div>
<pre class="ox-tryit-cmd" data-copy="git clone https://github.com/oxo-flow-community/oxo-flow-clindet.git &amp;&amp; cd oxo-flow-clindet &amp;&amp; oxo-flow run main.oxoflow">git clone https://github.com/oxo-flow-community/oxo-flow-clindet.git
cd oxo-flow-clindet
oxo-flow run main.oxoflow</pre>
<p class="ox-tryit-note">The repository ships test fixtures (e.g. <code>test/extend_fixture_ref.py</code>, <code>test/fixtures/bed/exome_target_hg38_chr21.bed</code>, <code>test/fixtures/bed/exome_target_hg38_chr21.bed.gz</code>, <code>test/fixtures/cnv/ascat_alleles/21.txt</code>) — point <code>input</code> at them or use the built-in sample group to <code>dry-run</code> first.</p>
</div>


## Run it

```bash
oxo-flow run main.oxoflow
```

Needs clinical sequencing inputs — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.16.0

**Toolchain.** conda envs (envs/*.yaml) + pinned Singularity/Docker containers for GATK, VarDict, MuSE, CaVEMan; VEP cache installed via the clindet_vep env post-deploy

**Requirements.**

- Reference data: genome FASTA + .fai + .dict, target BED, dbSNP / Mills indels / gnomAD VCFs (paths in [config])
- BWA index of the reference FASTA and tabix indexes for the annotation VCFs
- VEP cache (GRCh38, version 110) at the configured vep_data path
- Compute: up to 30 threads / 10 GB per rule

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
oxo-flow pull gh:WangLabCSU/oxo-flow-clindet
#    (alternative: plain git clone)
#    git clone https://github.com/WangLabCSU/oxo-flow-clindet
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy annotate_beds_file = value" data-copy="annotate_beds_file = ">annotate_beds_file</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">BED tracks used by mutation_flag — name/path TSV mirroring upstream<br>softwares_params[genome].annotate_beds dict (empty = header-only, no flags)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy arriba_blacklist = value" data-copy="arriba_blacklist = test/fixtures/refs/annotations/arriba_blacklist.tsv">arriba_blacklist</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/arriba_blacklist.tsv</code></td>
<td class="ox-p-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy arriba_cytobands = value" data-copy="arriba_cytobands = test/fixtures/refs/annotations/arriba_cytobands_mini.tsv">arriba_cytobands</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/arriba_cytobands_mini.tsv</code></td>
<td class="ox-p-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy arriba_known_fusions = value" data-copy="arriba_known_fusions = test/fixtures/refs/annotations/arriba_known_fusions_mini.tsv.gz">arriba_known_fusions</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/arriba_known_fusions_mini.tsv.gz</code></td>
<td class="ox-p-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy arriba_protein_domains = value" data-copy="arriba_protein_domains = test/fixtures/refs/annotations/arriba_protein_domains_mini.gff3">arriba_protein_domains</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/arriba_protein_domains_mini.gff3</code></td>
<td class="ox-p-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ascat_alleles_prefix = value" data-copy="ascat_alleles_prefix = test/fixtures/cnv/ascat_alleles/">ascat_alleles_prefix</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/cnv/ascat_alleles/</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ascat_chroms = value" data-copy="ascat_chroms = 21">ascat_chroms</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>21</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ascat_gc_file = value" data-copy="ascat_gc_file = test/fixtures/cnv/ascat_gc.txt">ascat_gc_file</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/cnv/ascat_gc.txt</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ascat_loci_prefix = value" data-copy="ascat_loci_prefix = test/fixtures/cnv/ascat_loci/">ascat_loci_prefix</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/cnv/ascat_loci/</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ascat_rt_file = value" data-copy="ascat_rt_file = ">ascat_rt_file</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cnv_enabled = value" data-copy="cnv_enabled = false">cnv_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dbsnp = value" data-copy="dbsnp = test/fixtures/refs/annotations/dbsnp_146.hg38_chr21.vcf.gz">dbsnp</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/dbsnp_146.hg38_chr21.vcf.gz</code></td>
<td class="ox-p-desc">cgpFlagCaVEMan configs (bed-based flags dropped: no chr21 flag data)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dbsnp_gz = value" data-copy="dbsnp_gz = test/fixtures/refs/annotations/dbsnp_146.hg38_chr21.vcf.gz">dbsnp_gz</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/dbsnp_146.hg38_chr21.vcf.gz</code></td>
<td class="ox-p-desc">MuSE sump needs a gzipped dbSNP<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dbsnp_indel = value" data-copy="dbsnp_indel = test/fixtures/refs/annotations/Mills_and_1000G_gold_standard.indels.hg38_chr21.vcf.gz">dbsnp_indel</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/Mills_and_1000G_gold_standard.indels.hg38_chr21.vcf.gz</code></td>
<td class="ox-p-desc">cgpFlagCaVEMan configs (bed-based flags dropped: no chr21 flag data)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy exomedepth_bed = value" data-copy="exomedepth_bed = test/fixtures/cnv/exomedepth_regions.bed">exomedepth_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/cnv/exomedepth_regions.bed</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy exomedepth_use_target_bed = value" data-copy="exomedepth_use_target_bed = true">exomedepth_use_target_bed</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy flag_config_dir = value" data-copy="flag_config_dir = test/fixtures/flag">flag_config_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/flag</code></td>
<td class="ox-p-desc">cgpFlagCaVEMan configs (bed-based flags dropped: no chr21 flag data)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freec_chr_files = value" data-copy="freec_chr_files = test/fixtures/cnv/freec_chr_fasta">freec_chr_files</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/cnv/freec_chr_fasta</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freec_chr_len_file = value" data-copy="freec_chr_len_file = test/fixtures/cnv/freec_chrlen.txt">freec_chr_len_file</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/cnv/freec_chrlen.txt</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freec_ini_template = value" data-copy="freec_ini_template = scripts/config_exome.mini.ini">freec_ini_template</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>scripts/config_exome.mini.ini</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freec_sambamba = value" data-copy="freec_sambamba = sambamba">freec_sambamba</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>sambamba</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genome_version = value" data-copy="genome_version = hg38_chr21">genome_version</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>hg38_chr21</code></td>
<td class="ox-p-desc">Upstream Snakefile dispatch key (VALID_RUN_TYPES): wes | wgs | rna<br><span class="ox-param-usedby">used by <code>188</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy germ_caller_list = value" data-copy="germ_caller_list = strelkamanta, caveman">germ_caller_list</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>strelkamanta, caveman</code></td>
<td class="ox-p-desc">Caller lists (upstream run_params)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy hmftools_ensembl_data_dir = value" data-copy="hmftools_ensembl_data_dir = ">hmftools_ensembl_data_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">HMF tools (isofox; excluded for hg38_chr21 upstream — needs the multi-GB<br>hmf_pipeline_resources tree, not shipped in the mini-test)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy isofox_mem_mb = value" data-copy="isofox_mem_mb = 30000">isofox_mem_mb</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>30000</code></td>
<td class="ox-p-desc">HMF tools (isofox; excluded for hg38_chr21 upstream — needs the multi-GB<br>hmf_pipeline_resources tree, not shipped in the mini-test)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy java_temp_dir = value" data-copy="java_temp_dir = /tmp">java_temp_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>/tmp</code></td>
<td class="ox-p-desc">Java temp dir (upstream: config[&#x27;params&#x27;][&#x27;java&#x27;][&#x27;temp_directory&#x27;])<br><span class="ox-param-usedby">used by <code>36</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kallisto_index = value" data-copy="kallisto_index = ">kallisto_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Quant indexes are empty in the upstream hg38_chr21 test config — the<br>RSEM/kallisto/salmon rules only run when explicitly targeted<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy known_sites1 = value" data-copy="known_sites1 = test/fixtures/refs/annotations/known_sites1.mini.vcf.gz">known_sites1</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/known_sites1.mini.vcf.gz</code></td>
<td class="ox-p-desc">BQSR (upstream config[&#x27;project&#x27;][&#x27;recal_BQSR&#x27;] + resources[&#x27;varanno&#x27;][genome]):<br>recal_bqsr = false is the upstream mini-test default (recal_link symlinks the<br>dedup BAM); set true to run BaseRecalibrator + ApplyBQSR instead.<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy known_sites2 = value" data-copy="known_sites2 = test/fixtures/refs/annotations/known_sites2.mini.vcf.gz">known_sites2</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/known_sites2.mini.vcf.gz</code></td>
<td class="ox-p-desc">BQSR (upstream config[&#x27;project&#x27;][&#x27;recal_BQSR&#x27;] + resources[&#x27;varanno&#x27;][genome]):<br>recal_bqsr = false is the upstream mini-test default (recal_link symlinks the<br>dedup BAM); set true to run BaseRecalibrator + ApplyBQSR instead.<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mutect2_germline_vcf = value" data-copy="mutect2_germline_vcf = test/fixtures/refs/annotations/gnomAD.r2.1.1.GRCh38.PASS.AC.AF.only_chr21.vcf.gz">mutect2_germline_vcf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/gnomAD.r2.1.1.GRCh38.PASS.AC.AF.only_chr21.vcf.gz</code></td>
<td class="ox-p-desc">Mutect2 GetPileupSummaries sites + germline resource<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mutect2_vcf = value" data-copy="mutect2_vcf = test/fixtures/refs/annotations/gnomAD.r2.1.1.GRCh38.PASS.AC.AF.only_chr21.vcf.gz">mutect2_vcf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/gnomAD.r2.1.1.GRCh38.PASS.AC.AF.only_chr21.vcf.gz</code></td>
<td class="ox-p-desc">Mutect2 GetPileupSummaries sites + germline resource<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ncbi_build = value" data-copy="ncbi_build = GRCh38">ncbi_build</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>GRCh38</code></td>
<td class="ox-p-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])<br><span class="ox-param-usedby">used by <code>20</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy normal_fastq_r1 = value" data-copy="normal_fastq_r1 = test/fixtures/reads/mini-NC_R1.fq.gz">normal_fastq_r1</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reads/mini-NC_R1.fq.gz</code></td>
<td class="ox-p-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy normal_fastq_r2 = value" data-copy="normal_fastq_r2 = test/fixtures/reads/mini-NC_R2.fq.gz">normal_fastq_r2</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reads/mini-NC_R2.fq.gz</code></td>
<td class="ox-p-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy output_dir = value" data-copy="output_dir = mini_test">output_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>mini_test</code></td>
<td class="ox-p-desc">Upstream Snakefile dispatch key (VALID_RUN_TYPES): wes | wgs | rna<br><span class="ox-param-usedby">used by <code>188</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy recal_bqsr = value" data-copy="recal_bqsr = false">recal_bqsr</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">BQSR (upstream config[&#x27;project&#x27;][&#x27;recal_BQSR&#x27;] + resources[&#x27;varanno&#x27;][genome]):<br>recal_bqsr = false is the upstream mini-test default (recal_link symlinks the<br>dedup BAM); set true to run BaseRecalibrator + ApplyBQSR instead.<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference = value" data-copy="reference = test/fixtures/refs/sequence/Homo_sapiens_assembly38_chr21.fasta">reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/sequence/Homo_sapiens_assembly38_chr21.fasta</code></td>
<td class="ox-p-desc">Resources (upstream: config[&#x27;resources&#x27;][genome_version])<br><span class="ox-param-usedby">used by <code>103</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reference_dict = value" data-copy="reference_dict = test/fixtures/refs/sequence/Homo_sapiens_assembly38_chr21.dict">reference_dict</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/sequence/Homo_sapiens_assembly38_chr21.dict</code></td>
<td class="ox-p-desc">Resources (upstream: config[&#x27;resources&#x27;][genome_version])<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rna_caller_list = value" data-copy="rna_caller_list = freebayes, HaplotypeCaller, lofreq, Mutect2, vardict, varscan2">rna_caller_list</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>freebayes, HaplotypeCaller, lofreq, Mutect2, vardict, varscan2</code></td>
<td class="ox-p-desc">RNA SNV callers for the vcf2maf merge tail (upstream<br>run_params.rna_caller_list in mini_test_data/rna/fusion/data/test_rna.yaml;<br>matches the six unrolled vcf2maf_rna_* rules in rules/rna/60_vcf2maf_merge.oxoflow)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rna_fastq_r1 = value" data-copy="rna_fastq_r1 = test/fixtures/reads/mini-T_RNA_R1.fq.gz">rna_fastq_r1</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reads/mini-T_RNA_R1.fq.gz</code></td>
<td class="ox-p-desc">RNA (upstream wrapper/rna.smk; run_type = &quot;rna&quot;). Default stages:<br>[arriba, call_mut]; quant/isofox rules run when explicitly targeted.<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rna_fastq_r2 = value" data-copy="rna_fastq_r2 = test/fixtures/reads/mini-T_RNA_R2.fq.gz">rna_fastq_r2</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reads/mini-T_RNA_R2.fq.gz</code></td>
<td class="ox-p-desc">RNA (upstream wrapper/rna.smk; run_type = &quot;rna&quot;). Default stages:<br>[arriba, call_mut]; quant/isofox rules run when explicitly targeted.<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rna_gtf = value" data-copy="rna_gtf = test/fixtures/refs/annotations/mini_chr21.gtf">rna_gtf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/annotations/mini_chr21.gtf</code></td>
<td class="ox-p-desc">RNA (upstream wrapper/rna.smk; run_type = &quot;rna&quot;). Default stages:<br>[arriba, call_mut]; quant/isofox rules run when explicitly targeted.<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy rsem_index = value" data-copy="rsem_index = ">rsem_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Quant indexes are empty in the upstream hg38_chr21 test config — the<br>RSEM/kallisto/salmon rules only run when explicitly targeted<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_report = value" data-copy="run_report = true">run_report</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">Report stages (upstream <code>stages</code>): case_report + multiqc are ON in the port<br>default; set run_report = false to match the upstream mini-test default.<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_type = value" data-copy="run_type = wes">run_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>wes</code></td>
<td class="ox-p-desc">Upstream Snakefile dispatch key (VALID_RUN_TYPES): wes | wgs | rna<br><span class="ox-param-usedby">used by <code>188</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sage_ref_genome_version = value" data-copy="sage_ref_genome_version = 38">sage_ref_genome_version</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>38</code></td>
<td class="ox-p-desc">HMF tools (isofox; excluded for hg38_chr21 upstream — needs the multi-GB<br>hmf_pipeline_resources tree, not shipped in the mini-test)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy salmon_index = value" data-copy="salmon_index = ">salmon_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Quant indexes are empty in the upstream hg38_chr21 test config — the<br>RSEM/kallisto/salmon rules only run when explicitly targeted<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sansa_call = value" data-copy="sansa_call = sansa">sansa_call</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>sansa</code></td>
<td class="ox-p-desc">SV annotation branch (issue #7; upstream WGS SV rules gate on the sansa<br>software config being present — absent upstream by default, so these are<br>off by default and the port mirrors that with empty keys = zero instances).<br>sansa_db/sansa_g: the sansa annotate -a database and -g gene-model inputs<br>(upstream softwares.sansa[&lt;genome_version&gt;].{db,g}); sansa_call: the<br>binary/invocation (upstream config[softwares][sansa][call]).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sansa_db = value" data-copy="sansa_db = ">sansa_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">SV annotation branch (issue #7; upstream WGS SV rules gate on the sansa<br>software config being present — absent upstream by default, so these are<br>off by default and the port mirrors that with empty keys = zero instances).<br>sansa_db/sansa_g: the sansa annotate -a database and -g gene-model inputs<br>(upstream softwares.sansa[&lt;genome_version&gt;].{db,g}); sansa_call: the<br>binary/invocation (upstream config[softwares][sansa][call]).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sansa_g = value" data-copy="sansa_g = ">sansa_g</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">SV annotation branch (issue #7; upstream WGS SV rules gate on the sansa<br>software config being present — absent upstream by default, so these are<br>off by default and the port mirrors that with empty keys = zero instances).<br>sansa_db/sansa_g: the sansa annotate -a database and -g gene-model inputs<br>(upstream softwares.sansa[&lt;genome_version&gt;].{db,g}); sansa_call: the<br>binary/invocation (upstream config[softwares][sansa][call]).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sequenza_gc_wiggle = value" data-copy="sequenza_gc_wiggle = test/fixtures/cnv/sequenza_gc.wig">sequenza_gc_wiggle</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/cnv/sequenza_gc.wig</code></td>
<td class="ox-p-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy somatic_caller_list = value" data-copy="somatic_caller_list = HaplotypeCaller, vardict, varscan2, muse, Mutect2">somatic_caller_list</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>HaplotypeCaller, vardict, varscan2, muse, Mutect2</code></td>
<td class="ox-p-desc">Caller lists (upstream run_params)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy star_index = value" data-copy="star_index = test/fixtures/refs/star_index">star_index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/star_index</code></td>
<td class="ox-p-desc">STAR index built inline by STAR_1_pass when missing (upstream ships a<br>pre-built index; the synthetic fixture reference needs its own)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy svanno_gtf = value" data-copy="svanno_gtf = ">svanno_gtf</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">svanno: gatk SVAnnotate needs a protein-coding GTF (upstream<br>resources[genome_version].GTF). Empty default = rule never runs.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy target_bed = value" data-copy="target_bed = test/fixtures/bed/exome_target_hg38_chr21.bed">target_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/bed/exome_target_hg38_chr21.bed</code></td>
<td class="ox-p-desc">Resources (upstream: config[&#x27;resources&#x27;][genome_version])<br><span class="ox-param-usedby">used by <code>33</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy trust4_dir = value" data-copy="trust4_dir = resources/softwares/TRUST4">trust4_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>resources/softwares/TRUST4</code></td>
<td class="ox-p-desc">TRUST4 (upstream softwares_params[genome].trust4; git-cloned at rule<br>runtime into trust4_dir when trust4_f is missing — not in default stages)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy trust4_f = value" data-copy="trust4_f = resources/softwares/TRUST4/hg38_bcrtcr.fa">trust4_f</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>resources/softwares/TRUST4/hg38_bcrtcr.fa</code></td>
<td class="ox-p-desc">TRUST4 (upstream softwares_params[genome].trust4; git-cloned at rule<br>runtime into trust4_dir when trust4_f is missing — not in default stages)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy trust4_ref = value" data-copy="trust4_ref = resources/softwares/TRUST4/human_IMGT+C.fa">trust4_ref</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>resources/softwares/TRUST4/human_IMGT+C.fa</code></td>
<td class="ox-p-desc">TRUST4 (upstream softwares_params[genome].trust4; git-cloned at rule<br>runtime into trust4_dir when trust4_f is missing — not in default stages)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy tumor_fastq_r1 = value" data-copy="tumor_fastq_r1 = test/fixtures/reads/mini-T_R1.fq.gz">tumor_fastq_r1</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reads/mini-T_R1.fq.gz</code></td>
<td class="ox-p-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy tumor_fastq_r2 = value" data-copy="tumor_fastq_r2 = test/fixtures/reads/mini-T_R2.fq.gz">tumor_fastq_r2</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/reads/mini-T_R2.fq.gz</code></td>
<td class="ox-p-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy unpaired_caller_list = value" data-copy="unpaired_caller_list = Mutect2, HaplotypeCaller, varscan2, strelka, vardict, lofreq, freebayes">unpaired_caller_list</button></td>
<td class="ox-p-t"><code>array</code></td>
<td class="ox-p-d"><code>Mutect2, HaplotypeCaller, varscan2, strelka, vardict, lofreq, freebayes</code></td>
<td class="ox-p-desc">Tumor-only callers (upstream run_params.tumor_only_caller; upstream default<br>is [sage] — needs the custom hmftools container, so the port defaults to<br>the seven portable callers, see rules/70_unpaired.oxoflow)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_cache_ready = value" data-copy="vep_cache_ready = false">vep_cache_ready</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">VEP needs a local cache at {vep_data}/{vep_species} (~10GB download; the<br>fixture kit does not ship it). The vcf2maf rules and the downstream MAF<br>merge/flag/cancer-report tail gate on this flag — set true once the cache<br>is in place (upstream fails hard without it).<br><span class="ox-param-usedby">used by <code>28</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_cache_version = value" data-copy="vep_cache_version = 110">vep_cache_version</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>110</code></td>
<td class="ox-p-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])<br><span class="ox-param-usedby">used by <code>20</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_data = value" data-copy="vep_data = resources/ref_genome/hg38/vep">vep_data</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>resources/ref_genome/hg38/vep</code></td>
<td class="ox-p-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])<br><span class="ox-param-usedby">used by <code>20</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy vep_species = value" data-copy="vep_species = homo_sapiens">vep_species</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>homo_sapiens</code></td>
<td class="ox-p-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])<br><span class="ox-param-usedby">used by <code>20</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy wes_pon = value" data-copy="wes_pon = ">wes_pon</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Upstream hg38_chr21 has no panel of normals (WES_PON: null) — leave empty<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy wgs_pon = value" data-copy="wgs_pon = ">wgs_pon</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Upstream hg38_chr21 has no panel of normals (WES_PON: null) — leave empty<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>DNA — WES/WGS paired, germline, CNV, tumor-only unpaired</summary>
<div class="ox-dag-card">
<a href="/assets/dag/oxo-flow-clindet-dna.svg?v=2e336201bb" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-clindet-dna.svg?v=2e336201bb" alt="oxo-flow-clindet dna flow view" loading="lazy"></a>
<p class="ox-dag-note">Stations are the sub-flow's modules; a stage name above the module set tells what the module does. Unconnected stations are conditional or auxiliary modules without a dataflow edge on the template DAG (clindet: QC, Isofox).</p>
</div>
</details>
<details class="ox-flow-view" open>
<summary>RNA — fusion calling, unpaired SNV callers, isofox/quantifiers (run with -t)</summary>
<div class="ox-dag-card">
<a href="/assets/dag/oxo-flow-clindet-rna.svg?v=670647840a" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-clindet-rna.svg?v=670647840a" alt="oxo-flow-clindet rna flow view" loading="lazy"></a>
<p class="ox-dag-note">Stations are the sub-flow's modules; a stage name above the module set tells what the module does. Unconnected stations are conditional or auxiliary modules without a dataflow edge on the template DAG (clindet: QC, Isofox).</p>
</div>
</details>
<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-clindet-rules.svg?v=5e14806db2" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-clindet-rules.svg?v=5e14806db2" alt="oxo-flow-clindet rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view">
<summary>Overview — all modules</summary>
<div class="ox-dag-card ox-dag-card--wide" markdown="1">

<a href="/assets/dag/oxo-flow-clindet.svg?v=74a2c40ac5" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-clindet.svg?v=74a2c40ac5" alt="oxo-flow-clindet pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-clindet — Port of zyllifeworld/clindet in its upstream single-Snakefile form: one entry file, config run_type (wes|wgs|rna) selects the rule tree, and paired vs tumor-only WES is derived PER PAIR from the sample sheet (a pair without a control runs the tumor-only tree — engine wildcard-scoped when predicates).</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- wes (run_type=wes, default): paired WES tree for pairs with a control + tumor-only WES tree for pairs without (fastp, bwa+GATK mapping/markdup, opt-in BQSR, 5 somatic SNV callers, Strelka2/Manta/CaVEMan germline, vcf2maf/VEP MAF, region flagging, cancer report, MultiQC)
- wgs (run_type=wgs): WGS metrics, the paired callers with WGS config, delly SV chain (call/filter/to_vcf/germ/delly2bnd), svaba, Manta somaticSV
- rna (run_type=rna): arriba/TRUST4/isofox fusion + expression default stages (quant rules targetable)
- CNV (paired, cnv_enabled gate): freec_config/call/plot (Control-FREEC), sequenza bam2seqz/binning/call, ExomeDepth, ASCAT + purity/ploidy extraction
- Non-human reference parity: GRCh37/38 + non-human config keys

**Excluded**

- CNV: purple/amber/cobalt/FACETS — HMF/Sanger custom containers (hmftools.sif, facets-suite image) + multi-GB hmf_pipeline_resources / snp-pileup PoN trees built via the upstream pull_zenodo run type; unpaired CNV (freec/purple) also not ported — the ported CNV gate is paired-only; the conda-portable subset freec/sequenza/exomedepth/ASCAT IS ported and live-verified
- CNV: SM_check / CNA_ABSOLUTE_GISTIC / CNA_Battenberg — marked 'for future development' upstream (workflow/WES/rules/rtm/paired/CNV.smk comment); ABSOLUTE/GISTIC2 are Broad tools without conda packages (same family: WGS ASCAT_GISTIC), Battenberg needs the cgpbattenberg sif + 1000G impute reference data
- SV: gridss/BRASS/linx/igcaller/jasmine — upstream custom sifs (gridss 2.13.2, brass634, linx, jasminesv) or hardcoded local software paths (/public/ClinicalExam/...) plus Sanger/HMF reference trees (the merge chain continues into SV_merge_final — bcftools filter SUPP>=2); delly/svaba/Manta ARE ported
- unpaired-mode callers beyond the seven portable ones (note: some of these tools do have paired variants upstream — pindel cgppindel PI_ggz, deepvariant WES/WGS SNV/DeepVariant.smk, sage — the exclusion covers their custom containers either way) (sage/deepvariant/pindel/octopus/UnifiedGeniTyper — custom containers) + WGS Battenberg/ecDNA/VirusScan (custom containers + resource trees)
- conpair contamination check — custom conpair_latest.sif container
- ASCATsc (feeds the BRASS input chain; HMF ASCATsc.R) + multi-lane entry variant (mapping_muliti.smk) — non-default-path variants
- Mutect2 PoN build chain (upstream WGS SNV/Mutect2_pon.smk: pon_GB / pon_facetsCH / M2_CSPN / call_variants_pon) — not ported; the port consumes a configured `-pon` only and does not build PoN databases (facets inputs are excluded anyway)
- CNV/SV/QC callers not ported: BIC-seq2 (WES bicseq2.smk + WGS bicseq.smk), esvee (WGS SV/esvee.smk), lumpy (WGS SV/lumpy.smk), sentieon WGS paired caller (WGS SNV/sentieon.smk; the RNA-side sentieon chain is already noted in the port), lancet2 (WES SNV/Lancet2.smk — off-default like the others), moalmanac + split_maf_snp_indel (common case_report.smk — downstream of the excluded facets/ASCAT CNV), orange + bamMetrics WGS report (report/orange.smk — downstream of purple/linx), ngs_bit QC (common qc.smk: 145), summary_softwares version grid (common summary_softwares.smk; the port substitutes conda env versions in MultiQC)
- Reference-data/setup rule family (upstream setup/* download_* x19, build_b37_ref / build_hg38_ref / build_bwa_index / build_star_index / rsem_star_index etc.) — the README records the concept (reference-data utilities without a mini fixture, not ported); these rule names are not individually listed upstream-side documents — see the README setup note

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- sansa-annotation (SV_sansa_*) + svaba svanno — gated on an upstream sansa config absent from the mini test (svanno additionally needs the GTF, empty in the mini test)
- telomerecat — marked 'departed' upstream (workflow/WGS/rules/mapping.smk)
- WES rules/filtering.smk select_calls / hard_filter_calls / recalibrate_calls / merge_calls — upstream dead chain (the `results/genotyped/all.vcf.gz` input has no producer in the tree), so nothing to port

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| fastp (T/N) | `fastp_tumor_sample` / `fastp_normal_sample` | fastp | identical flags (`-w 8 -Q -c -L`) |
| bam flagstat (T/N) | `bam_flagstat_tumor` / `bam_flagstat_normal` | samtools | identical command |
| map_reads (T/N) | `map_reads_tumor` / `map_reads_normal` | bwa >=0.7.18, samtools | `bwa mem -MR` + `fixmate` + `sort` |
| mark_duplicates (T/N) | `mark_duplicates_tumor` / `mark_duplicates_normal` | gatk4 4.6.2.0 (container) | `MarkDuplicates --CREATE_INDEX true`, `VALIDATION_STRINGENCY SILENT` |
| recal_link (T/N) | `recal_link_tumor` / `recal_link_normal` | ln -s | `when = "!config.recal_bqsr"` (upstream mini-test default `recal_BQSR: False`) |
| recalibrate_base_qualities (T/N) | `recalibrate_base_qualities_tumor` / `recalibrate_base_qualities_normal` | gatk4 (container) | `BaseRecalibrator --use-original-qualities`, known-sites = upstream varanno KNOWN_SITES1/2; `when = "config.recal_bqsr"` |
| apply_base_quality_recalibration (T/N) | `apply_base_quality_recalibration_tumor` / `apply_base_quality_recalibration_normal` | gatk4 (container) | `ApplyBQSR -use-original-qualities` + `samtools index`; `when = "config.recal_bqsr"` |
| bed_to_interval_list | `bed_to_interval_list` | gatk4 (container) | `BedToIntervalList --SORT true` |
| picard_collect_wes (T/N) | `picard_collect_wes_tumor` / `picard_collect_wes_normal` | gatk4 (container) | `CollectHsMetrics` |
| call_variants_HaplotypeCaller | `call_variants_HaplotypeCaller` | gatk4 (container) | identical `-A` annotation flags |
| vardict_paired_mode | `vardict_paired_mode` | vardict-java 1.8.3 (container) | `vardict-java` + `testsomatic.R` + `var2vcf_paired.pl` |
| vardict_filter_somatic | `vardict_filter_somatic` | bcftools >=1.22 | StrongSomatic/LikelySomatic + `SSF <= 0.05` |
| varscan2 mpileup/call/processSomatic/filter | `varscan2_mpileup` … `merge_somatic` | varscan 2.4.6, samtools, bcftools | `--strand-filter 1`, `--output-vcf 1`, concat chain |
| muse_call / muse_sump | `muse_call` / `muse_sump` | muse 2.1.2 (container) | `sump -E -n {threads} -D {dbsnp_gz}` |
| mutect2 chain | `M2_ST`/`M2_SNC`/`M2_contam`/`mutect2`/`M2_filter` | gatk4 (container) | `-pon` only when `wes_pon` set (upstream hg38_chr21 has none) |
| call_config_strelka | `call_config_strelka` | manta | `configManta.py --exome --callRegions` |
| call_strelka_manta_germline | `call_strelka_manta_germline` | strelka2, manta | `configureStrelkaGermlineWorkflow` + `runWorkflow.py` |
| merge_strelka_manta | `merge_strelka_manta` | bcftools | upstream `{params.indel}` bug fixed (single concat+sort) |
| strelka somatic (via manta) | `call_strelka_somatic_manta` + `merge_strelka_somatic_manta` | strelka2, manta, bcftools | same pipeline on somatic config |
| CM_cnv | `CM_cnv` | touch | empty tumour/normal CNV beds (upstream default) |
| CM_call / CM_flag | `CM_call` / `CM_flag` | caveman 1.15.3 (container) | `-td 2 -nd 2 -seqType WGS -no-flagging`, flag with `-umv .`; `-ignore-file` fed a one-region bed on a contig absent from the reference (upstream passes `""`, which caveman 1.15.3 rejects — same "no ignore regions" semantics); flagger gets real `-c`/`-v` configs from `test/fixtures/flag` (GRCh38 params verbatim, bed-based flags dropped — no chr21 flag data) plus empty `-b`/`-ab` dirs and `-t genomic` (upstream's `""`/`""`/`"genome"` are rejected by cgpFlagCaVEMan 1.15.3) |
| CM_germ_flag | `CM_germ_flag` | bcftools | `-e 'DP<=30' -s LowDP --mode x` |
| vcf_norm (per caller) | `vcf_norm_{Mutect2,vardict,varscan2,muse,HaplotypeCaller,germline_strelkamanta,germline_caveman}` | bcftools >=1.22 | verbatim per-caller FILTER rules incl. vardict contig-header branch |
| loop_vcf2maf_paired | `vcf2maf_{Mutect2,vardict,varscan2,muse,HaplotypeCaller}` | vcf2maf 1.6.22, ensembl-vep 114.2 | verbatim tumor/normal IDs per `get_vcf_name`; gated on `vep_cache_ready` |
| loop_vcf2maf_germ_paired | `vcf2maf_germ_strelkamanta` / `vcf2maf_germ_caveman` | vcf2maf 1.6.22 | TUMOUR/NORMAL for CaVEMan; gated on `vep_cache_ready` |
| merge_loop (somatic) | `merge_paired_maf` | merge_maf.R (verbatim) | driven via scripts/smk.R shim |
| merge_paired_vcf | `merge_paired_vcf` | merge_caller_vcfs.py (verbatim) + pysam | driven via scripts/smk.py shim; upstream mini-test default stage `call_mut_vcf` |
| merge_loop_germline | `merge_paired_germ_maf` | merge_maf.R (verbatim) | |
| make_region_bed_list + flag_mutation_pairead_maf | `make_region_bed_list` + `flag_mutation_pairead_maf` | flag_mutation_maf.R (verbatim) | empty bed_list = header-only TSV |
| run_cancer_report | `run_cancer_report` | R >=4.4 (knitr, gpgr via post-deploy) | only MAF/panel/Rmd params; CNV/QC params unset (NULL) as in upstream default path |
| combined_multiqc | `prep_multiqc_data` + `combined_multiqc_prep_multiqc_data` + `combined_multiqc` | multiqc | conpair/purple inputs out of scope |
| freec_config / freec_call_paired / plot_freec | `freec_config` / `freec_call_paired` / `plot_freec` | Control-FREEC >=11.6, sambamba | verbatim `config_freec.py` + `config_exome.ini`; upstream runs freec in the facets-suite container, port uses bioconda control-freec; `when = "config.cnv_enabled"` |
| sequenza bam2seqz/binning/call | `sequenza_bam2seqz` / `sequenza_seqz_binning` / `sequenza_call` | sequenza-utils, r-sequenza | upstream's referenced `scripts/sequenza.R` does not exist in the tree — port ships the standard extract→fit→results chain (`scripts/sequenza_call.R`) |
| CNA_exomedepth | `CNA_exomedepth` | ExomeDepth (Bioc) | verbatim `ExomeDepth.R`; upstream counts over hardcoded exons.hg19 (dead `target.file` read) — port keeps that and adds a documented `use_target_bed` switch for the mini fixture |
| CNA_ASCAT / ASCAT_EXTRACT_PURITYPLOIDY | `CNA_ASCAT` / `ASCAT_EXTRACT_PURITYPLOIDY` | ASCAT >=3.2, alleleCounter | verbatim `ASCAT.R` (+chroms/GC/rt from config — upstream hardcodes c(1:22)); `ascat_pp.R` verbatim |
| WGS mapping/recal/QC | shared `00_common` rules | bwa/gatk4/picard | upstream WGS map_reads/markdup/BQSR/recal_link are identical to WES |
| WGS callers (no exome restrictions) | `rules/91_wgs_callers.oxoflow` | gatk4/muse/varscan/vardict/strelka2/manta | no `--intervals`/`--callRegions`/`--exome`; Manta emits somaticSV; germline Strelka takes BOTH bams (WES: normal only); vardict regions from `vardict_wgs_bed` |
| WGS picard_collect_wgs / picard_flength_wgs | `picard_collect_wgs_{tumor,normal}` / `picard_flength_wgs_{tumor,normal}` | picard | CollectWgsMetrics + CollectInsertSizeMetrics (telomerecat is "departed" upstream — not ported) |
| SV_delly chain | `SV_delly` → `SV_delly_sample_tsv` → `SV_delly_filter_somatic` → `SV_delly_to_vcf` → `delly_filter` → `delly2bnd` | delly 1.7.2 (container), bcftools | verbatim; `delly2bnd.py` verbatim (upstream env lacks cyvcf2 — added to envs/clindet.yaml, upstream bug) |
| SV_svaba | `SV_svaba` | svaba (container) | verbatim run |
| sansa-annotation (svaba + delly) | `SV_sansa_anno_svaba` / `SV_sansa_annodelly` | site-provided sansa binary (`sansa_call`) | gated on `sansa_db`/`sansa_g` being set (upstream gates on the sansa software config being present — absent upstream by default, so off by default here too; zero instances without the keys) |
| svanno (gatk SVAnnotate) | `SV_svanno_svaba` | gatk4 (container) | gated on `svanno_gtf` (protein-coding GTF); zero instances without the key |
| Manta SV | `call_config_strelka` (WGS) | manta | `somaticSV.vcf.gz` from the WGS Manta run (upstream SV list entry 'Manta') |

**Not ported** (upstream branches with reasons):
- CNV purple/amber/cobalt: HMF tools run in the upstream's custom
  hmftools.sif with the multi-GB hmf_pipeline_resources tree (built
  locally upstream, `pull_zenodo` run type) — not a portable image;
  dryclean has no rule file upstream (list-only).
- CNV FACETS/facets-suite: custom facets-suite-dev.img + snp-pileup PoN
  chain, requires compiling cnv_facets C++.
- CNV CNA_ABSOLUTE_GISTIC / ASCAT_GISTIC: ABSOLUTE + GISTIC2 are Broad
  tools without conda packages; SM_check / CNA_Battenberg are marked
  "for future development" upstream (Battenberg needs cgpbattenberg371.sif
  + 1000G impute reference data).
- SV gridss/BRASS/linx/igv-caller/jasmine: custom containers (gridss2/
  brass634/jasminesv sifs) + Sanger VAGrENT/BRASS and HMF resource trees.
- WGS unpaired callers (sage/deepvariant/pindel/octopus/UnifiedGeniTyper)
  and WGS Battenberg/ecDNA/VirusScan: custom containers + resource trees
  as above.
- conpair contamination check: custom conpair_latest.sif container.
- unpaired CNV (upstream `rtm/unpaired/CNV.smk`: freec + purple): the
  ported CNV branch is paired-only (upstream mini-test default
  `somatic_cnv_list: [notrun]`).
- non-human genomes: supported at config level (WBcel235/mm10 parity table
  above) — the upstream rule set itself is species-agnostic.

## Links

- Repository: [oxo-flow-clindet](https://github.com/WangLabCSU/oxo-flow-clindet)
- Upstream: [zyllifeworld/clindet](https://github.com/zyllifeworld/clindet) @ `582a9131`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
