---
title: "Cancer genome & transcriptome analysis (WES/WGS/RNA, single entry): somatic+germline+CNV+SV calling, MAF annotation, case report"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-clindet</span></div>
<div class="ox-detail-cols">
<div>
<h1>Cancer genome &amp; transcriptome analysis (WES/WGS/RNA, single entry): somatic+germline+CNV+SV calling, MAF annotation, case report</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>
<p>Port of zyllifeworld/clindet in its upstream single-Snakefile form: one entry file, config run_type (wes|wgs|rna) selects the rule tree, and paired vs tumor-only WES is derived PER PAIR from the sample sheet (a pair without a control runs the tumor-only tree — engine wildcard-scoped when predicates). 183 rules: somatic SNV (Mutect2, VarDict, VarScan2, MuSE, HaplotypeCaller) + germline (Strelka2+Manta, CaVEMan); tumor-only callers (Mutect2/HaplotypeCaller/varscan2/Strelka/vardict/lofreq/freebayes); CNV subset (Control-FREEC, Sequenza, ExomeDepth, ASCAT); WGS SV (delly chain incl. germ, svaba, Manta somaticSV); opt-in BQSR; vcf2maf/VEP MAF annotation, region flagging, cancer report, MultiQC; RNA fusion/expression (arriba/TRUST4/isofox). Live-verified per run type on tx-ubuntu.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">188</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 30 threads / 10 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">cancer genomics (WES/WGS/RNA)</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/zyllifeworld/clindet">zyllifeworld/clindet</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>582a9131</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2299.1"><code>10.48546/workflowhub.workflow.2299.1</code></a></span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
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

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. The list below names the rules that read each key.</p>
<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>annotate_beds_file</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">BED tracks used by mutation_flag — name/path TSV mirroring upstream<br>softwares_params[genome].annotate_beds dict (empty = header-only, no flags)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>make_region_bed_list</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>arriba_blacklist</code><span class="ox-param-default">test/fixtures/refs/annotations/arriba_blacklist.tsv</span></div>
<p class="ox-param-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>arriba_fusion</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>arriba_cytobands</code><span class="ox-param-default">test/fixtures/refs/annotations/arriba_cytobands_mini.tsv</span></div>
<p class="ox-param-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>arriba_draw</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>arriba_known_fusions</code><span class="ox-param-default">test/fixtures/refs/annotations/arriba_known_fusions_mini.tsv.gz</span></div>
<p class="ox-param-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>arriba_fusion</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>arriba_protein_domains</code><span class="ox-param-default">test/fixtures/refs/annotations/arriba_protein_domains_mini.gff3</span></div>
<p class="ox-param-desc">Arriba databases (upstream softwares_params[genome].arriba.database).<br>Mini-test: blacklist + mini known_fusions/protein_domains/cytobands are<br>local files matching the 922 bp fixture reference (the whole-genome DBs<br>in the uhrigs/arriba:2.4.0 image fail to parse against it, observed live).<br>Real hg38 runs keep the container paths; the mini DBs mirror the formats 1:1.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>arriba_draw</code> <code>arriba_fusion</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ascat_alleles_prefix</code><span class="ox-param-default">test/fixtures/cnv/ascat_alleles/</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CNA_ASCAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ascat_chroms</code><span class="ox-param-default">21</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CNA_ASCAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ascat_gc_file</code><span class="ox-param-default">test/fixtures/cnv/ascat_gc.txt</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CNA_ASCAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ascat_loci_prefix</code><span class="ox-param-default">test/fixtures/cnv/ascat_loci/</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CNA_ASCAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ascat_rt_file</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CNA_ASCAT</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cnv_enabled</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 10 rules</summary>
<div class="ox-param-rules"><code>ASCAT_EXTRACT_PURITYPLOIDY</code> <code>CNA_ASCAT</code> <code>CNA_exomedepth</code> <code>all_cnv</code> <code>freec_call_paired</code> <code>freec_config</code> <code>plot_freec</code> <code>sequenza_bam2seqz</code> <code>sequenza_call</code> <code>sequenza_seqz_binning</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>dbsnp</code><span class="ox-param-default">test/fixtures/refs/annotations/dbsnp_146.hg38_chr21.vcf.gz</span></div>
<p class="ox-param-desc">cgpFlagCaVEMan configs (bed-based flags dropped: no chr21 flag data)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>dbsnp_gz</code><span class="ox-param-default">test/fixtures/refs/annotations/dbsnp_146.hg38_chr21.vcf.gz</span></div>
<p class="ox-param-desc">MuSE sump needs a gzipped dbSNP</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>muse_sump</code> <code>muse_sump_wgs</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>dbsnp_indel</code><span class="ox-param-default">test/fixtures/refs/annotations/Mills_and_1000G_gold_standard.indels.hg38_chr21.vcf.gz</span></div>
<p class="ox-param-desc">cgpFlagCaVEMan configs (bed-based flags dropped: no chr21 flag data)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>SV_svaba</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>exomedepth_bed</code><span class="ox-param-default">test/fixtures/cnv/exomedepth_regions.bed</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CNA_exomedepth</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>exomedepth_use_target_bed</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CNA_exomedepth</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>flag_config_dir</code><span class="ox-param-default">test/fixtures/flag</span></div>
<p class="ox-param-desc">cgpFlagCaVEMan configs (bed-based flags dropped: no chr21 flag data)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>CM_flag</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>freec_chr_files</code><span class="ox-param-default">test/fixtures/cnv/freec_chr_fasta</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>freec_config</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>freec_chr_len_file</code><span class="ox-param-default">test/fixtures/cnv/freec_chrlen.txt</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>freec_config</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>freec_ini_template</code><span class="ox-param-default">scripts/config_exome.mini.ini</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>freec_config</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>freec_sambamba</code><span class="ox-param-default">sambamba</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>freec_config</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>genome_version</code><span class="ox-param-default">hg38_chr21</span></div>
<p class="ox-param-desc">Upstream Snakefile dispatch key (VALID_RUN_TYPES): wes | wgs | rna</p>
<details class="ox-param-usedby"><summary>used by 188 rules</summary>
<div class="ox-param-rules"><code>ASCAT_EXTRACT_PURITYPLOIDY</code> <code>CM_call</code> <code>CM_cnv</code> <code>CM_flag</code> <code>CM_germ_flag</code> <code>CNA_ASCAT</code> <code>CNA_exomedepth</code> <code>M2_SNC</code> <code>M2_SNC_wgs</code> <code>M2_ST</code> <code>M2_ST_wgs</code> <code>M2_contam</code> <code>M2_contam_wgs</code> <code>M2_filter</code> <code>M2_filter_unpaired</code> <code>M2_filter_unpaired_rna</code> <code>M2_filter_wgs</code> <code>RSEM_sort_genome</code> <code>STAR_1_pass</code> <code>STAR_arriba_map</code> <code>STAR_isofox_map</code> <code>STAR_mut_map</code> <code>SV_delly</code> <code>SV_delly_filter_somatic</code> <code>SV_delly_germ</code> <code>SV_delly_sample_tsv</code> <code>SV_delly_to_vcf</code> <code>SV_sansa_anno_svaba</code> <code>SV_sansa_annodelly</code> <code>SV_svaba</code> <code>SV_svanno_svaba</code> <code>SplitNCigarReads</code> <code>TRUST4_TBCR</code> <code>all</code> <code>all_cnv</code> <code>all_sv</code> <code>all_unpaired</code> <code>all_unpaired_maf</code> <code>all_vcf</code> <code>apply_base_quality_recalibration_normal</code> <code>apply_base_quality_recalibration_tumor</code> <code>apply_base_quality_recalibration_tumor_unpaired</code> <code>arriba_draw</code> <code>arriba_fusion</code> <code>bam_flagstat_normal</code> <code>bam_flagstat_tumor</code> <code>bed_to_interval_list</code> <code>cal_exp_RSEM</code> <code>call_config_strelka</code> <code>call_config_strelka_wgs</code> <code>call_strelka_manta_germline</code> <code>call_strelka_manta_wgs</code> <code>call_strelka_somatic_manta</code> <code>call_strelka_somatic_manta_wgs</code> <code>call_variants_HaplotypeCaller</code> <code>call_variants_HaplotypeCaller_rna</code> <code>call_variants_HaplotypeCaller_wgs</code> <code>combined_multiqc</code> <code>combined_multiqc_prep_multiqc_data</code> <code>delly2bnd</code> <code>delly_filter</code> <code>fastp_normal_sample</code> <code>fastp_trim</code> <code>fastp_tumor_sample</code> <code>fastp_tumor_sample_unpaired</code> <code>flag_mutation_pairead_maf</code> <code>freec_call_paired</code> <code>freec_config</code> <code>isofox_call</code> <code>kallisto</code> <code>link_bam</code> <code>lofreq_call_up</code> <code>lofreq_norm_filter</code> <code>lofreq_somatic_unpaired</code> <code>make_region_bed_list</code> <code>map_reads_normal</code> <code>map_reads_tumor</code> <code>map_reads_tumor_unpaired</code> <code>mark_duplicates_normal</code> <code>mark_duplicates_tumor</code> <code>mark_duplicates_tumor_unpaired</code> <code>merge_paired_germ_maf</code> <code>merge_paired_maf</code> <code>merge_paired_vcf</code> <code>merge_rna_maf</code> <code>merge_strelka_manta</code> <code>merge_strelka_manta_wgs</code> <code>merge_strelka_somatic_manta</code> <code>merge_strelka_somatic_manta_wgs</code> <code>merge_unpaired_maf</code> <code>merge_unpaired_vcf</code> <code>muse_call</code> <code>muse_call_wgs</code> <code>muse_sump</code> <code>muse_sump_wgs</code> <code>mutect2</code> <code>mutect2_call</code> <code>mutect2_wgs</code> <code>norm_filter_HaplotypeCaller</code> <code>norm_filter_freebayes</code> <code>picard_collect_wes_normal</code> <code>picard_collect_wes_tumor</code> <code>picard_collect_wgs_normal</code> <code>picard_collect_wgs_tumor</code> <code>picard_flength_wgs_normal</code> <code>picard_flength_wgs_tumor</code> <code>plot_freec</code> <code>prep_multiqc_data</code> <code>prep_multiqc_data_tumor_only</code> <code>prep_multiqc_data_wgs</code> <code>recal_link_normal</code> <code>recal_link_tumor</code> <code>recal_link_tumor_unpaired</code> <code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code> <code>run_cancer_report</code> <code>salmon</code> <code>sequenza_bam2seqz</code> <code>sequenza_call</code> <code>sequenza_seqz_binning</code> <code>unpair_lofreq_filter</code> <code>unpaired_call_config_strelka</code> <code>unpaired_call_config_strelka_rna</code> <code>unpaired_call_strelka_manta</code> <code>unpaired_call_strelka_manta_rna</code> <code>unpaired_call_variants_HaplotypeCaller</code> <code>unpaired_filter_vardict</code> <code>unpaired_filter_vardict_rna</code> <code>unpaired_freebayes</code> <code>unpaired_freebayes_rna</code> <code>unpaired_mutect2_call</code> <code>unpaired_strelka_filter</code> <code>unpaired_strelka_filter_rna</code> <code>unpaired_vardict_single_mode</code> <code>unpaired_vardict_single_mode_rna</code> <code>vardict_filter_somatic</code> <code>vardict_filter_somatic_wgs</code> <code>vardict_paired_mode</code> <code>vardict_paired_mode_wgs</code> <code>vardict_wgs_bed_wgs</code> <code>varscan2_call</code> <code>varscan2_call_unpaired_indel</code> <code>varscan2_call_unpaired_indel_rna</code> <code>varscan2_call_unpaired_snp</code> <code>varscan2_call_unpaired_snp_rna</code> <code>varscan2_call_wgs</code> <code>varscan2_filter_indel</code> <code>varscan2_filter_snp</code> <code>varscan2_merge_somatic</code> <code>varscan2_merge_somatic_wgs</code> <code>varscan2_merge_unpaired</code> <code>varscan2_merge_unpaired_rna</code> <code>varscan2_mpileup</code> <code>varscan2_mpileup_unpaired</code> <code>varscan2_mpileup_unpaired_rna</code> <code>varscan2_mpileup_wgs</code> <code>varscan2_processSomatic</code> <code>varscan2_processSomatic_wgs</code> <code>varscan2_som_filter</code> <code>varscan2_som_filter_wgs</code> <code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code> <code>vcf_norm_HaplotypeCaller</code> <code>vcf_norm_Mutect2</code> <code>vcf_norm_germline_caveman</code> <code>vcf_norm_germline_strelkamanta</code> <code>vcf_norm_muse</code> <code>vcf_norm_vardict</code> <code>vcf_norm_varscan2</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>germ_caller_list</code><span class="ox-param-default">strelkamanta, caveman</span></div>
<p class="ox-param-desc">Caller lists (upstream run_params)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>hmftools_ensembl_data_dir</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">HMF tools (isofox; excluded for hg38_chr21 upstream — needs the multi-GB<br>hmf_pipeline_resources tree, not shipped in the mini-test)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>isofox_call</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>isofox_mem_mb</code><span class="ox-param-default">30000</span></div>
<p class="ox-param-desc">HMF tools (isofox; excluded for hg38_chr21 upstream — needs the multi-GB<br>hmf_pipeline_resources tree, not shipped in the mini-test)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>isofox_call</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>java_temp_dir</code><span class="ox-param-default">/tmp</span></div>
<p class="ox-param-desc">Java temp dir (upstream: config[&#x27;params&#x27;][&#x27;java&#x27;][&#x27;temp_directory&#x27;])</p>
<details class="ox-param-usedby"><summary>used by 36 rules</summary>
<div class="ox-param-rules"><code>M2_SNC</code> <code>M2_SNC_wgs</code> <code>M2_ST</code> <code>M2_ST_wgs</code> <code>M2_contam</code> <code>M2_contam_wgs</code> <code>M2_filter</code> <code>M2_filter_unpaired</code> <code>M2_filter_unpaired_rna</code> <code>M2_filter_wgs</code> <code>SV_svanno_svaba</code> <code>SplitNCigarReads</code> <code>apply_base_quality_recalibration_normal</code> <code>apply_base_quality_recalibration_tumor</code> <code>apply_base_quality_recalibration_tumor_unpaired</code> <code>bed_to_interval_list</code> <code>call_variants_HaplotypeCaller</code> <code>call_variants_HaplotypeCaller_rna</code> <code>call_variants_HaplotypeCaller_wgs</code> <code>mark_duplicates_normal</code> <code>mark_duplicates_tumor</code> <code>mark_duplicates_tumor_unpaired</code> <code>mutect2</code> <code>mutect2_call</code> <code>mutect2_wgs</code> <code>picard_collect_wes_normal</code> <code>picard_collect_wes_tumor</code> <code>picard_collect_wgs_normal</code> <code>picard_collect_wgs_tumor</code> <code>picard_flength_wgs_normal</code> <code>picard_flength_wgs_tumor</code> <code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code> <code>unpaired_call_variants_HaplotypeCaller</code> <code>unpaired_mutect2_call</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>kallisto_index</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Quant indexes are empty in the upstream hg38_chr21 test config — the<br>RSEM/kallisto/salmon rules only run when explicitly targeted</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>kallisto</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>known_sites1</code><span class="ox-param-default">test/fixtures/refs/annotations/known_sites1.mini.vcf.gz</span></div>
<p class="ox-param-desc">BQSR (upstream config[&#x27;project&#x27;][&#x27;recal_BQSR&#x27;] + resources[&#x27;varanno&#x27;][genome]):<br>recal_bqsr = false is the upstream mini-test default (recal_link symlinks the<br>dedup BAM); set true to run BaseRecalibrator + ApplyBQSR instead.</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>known_sites2</code><span class="ox-param-default">test/fixtures/refs/annotations/known_sites2.mini.vcf.gz</span></div>
<p class="ox-param-desc">BQSR (upstream config[&#x27;project&#x27;][&#x27;recal_BQSR&#x27;] + resources[&#x27;varanno&#x27;][genome]):<br>recal_bqsr = false is the upstream mini-test default (recal_link symlinks the<br>dedup BAM); set true to run BaseRecalibrator + ApplyBQSR instead.</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>mutect2_germline_vcf</code><span class="ox-param-default">test/fixtures/refs/annotations/gnomAD.r2.1.1.GRCh38.PASS.AC.AF.only_chr21.vcf.gz</span></div>
<p class="ox-param-desc">Mutect2 GetPileupSummaries sites + germline resource</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>mutect2</code> <code>mutect2_call</code> <code>mutect2_wgs</code> <code>unpaired_mutect2_call</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>mutect2_vcf</code><span class="ox-param-default">test/fixtures/refs/annotations/gnomAD.r2.1.1.GRCh38.PASS.AC.AF.only_chr21.vcf.gz</span></div>
<p class="ox-param-desc">Mutect2 GetPileupSummaries sites + germline resource</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>M2_SNC</code> <code>M2_SNC_wgs</code> <code>M2_ST</code> <code>M2_ST_wgs</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>ncbi_build</code><span class="ox-param-default">GRCh38</span></div>
<p class="ox-param-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])</p>
<details class="ox-param-usedby"><summary>used by 20 rules</summary>
<div class="ox-param-rules"><code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>normal_fastq_r1</code><span class="ox-param-default">test/fixtures/reads/mini-NC_R1.fq.gz</span></div>
<p class="ox-param-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>fastp_normal_sample</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>normal_fastq_r2</code><span class="ox-param-default">test/fixtures/reads/mini-NC_R2.fq.gz</span></div>
<p class="ox-param-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>fastp_normal_sample</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>output_dir</code><span class="ox-param-default">mini_test</span></div>
<p class="ox-param-desc">Upstream Snakefile dispatch key (VALID_RUN_TYPES): wes | wgs | rna</p>
<details class="ox-param-usedby"><summary>used by 188 rules</summary>
<div class="ox-param-rules"><code>ASCAT_EXTRACT_PURITYPLOIDY</code> <code>CM_call</code> <code>CM_cnv</code> <code>CM_flag</code> <code>CM_germ_flag</code> <code>CNA_ASCAT</code> <code>CNA_exomedepth</code> <code>M2_SNC</code> <code>M2_SNC_wgs</code> <code>M2_ST</code> <code>M2_ST_wgs</code> <code>M2_contam</code> <code>M2_contam_wgs</code> <code>M2_filter</code> <code>M2_filter_unpaired</code> <code>M2_filter_unpaired_rna</code> <code>M2_filter_wgs</code> <code>RSEM_sort_genome</code> <code>STAR_1_pass</code> <code>STAR_arriba_map</code> <code>STAR_isofox_map</code> <code>STAR_mut_map</code> <code>SV_delly</code> <code>SV_delly_filter_somatic</code> <code>SV_delly_germ</code> <code>SV_delly_sample_tsv</code> <code>SV_delly_to_vcf</code> <code>SV_sansa_anno_svaba</code> <code>SV_sansa_annodelly</code> <code>SV_svaba</code> <code>SV_svanno_svaba</code> <code>SplitNCigarReads</code> <code>TRUST4_TBCR</code> <code>all</code> <code>all_cnv</code> <code>all_sv</code> <code>all_unpaired</code> <code>all_unpaired_maf</code> <code>all_vcf</code> <code>apply_base_quality_recalibration_normal</code> <code>apply_base_quality_recalibration_tumor</code> <code>apply_base_quality_recalibration_tumor_unpaired</code> <code>arriba_draw</code> <code>arriba_fusion</code> <code>bam_flagstat_normal</code> <code>bam_flagstat_tumor</code> <code>bed_to_interval_list</code> <code>cal_exp_RSEM</code> <code>call_config_strelka</code> <code>call_config_strelka_wgs</code> <code>call_strelka_manta_germline</code> <code>call_strelka_manta_wgs</code> <code>call_strelka_somatic_manta</code> <code>call_strelka_somatic_manta_wgs</code> <code>call_variants_HaplotypeCaller</code> <code>call_variants_HaplotypeCaller_rna</code> <code>call_variants_HaplotypeCaller_wgs</code> <code>combined_multiqc</code> <code>combined_multiqc_prep_multiqc_data</code> <code>delly2bnd</code> <code>delly_filter</code> <code>fastp_normal_sample</code> <code>fastp_trim</code> <code>fastp_tumor_sample</code> <code>fastp_tumor_sample_unpaired</code> <code>flag_mutation_pairead_maf</code> <code>freec_call_paired</code> <code>freec_config</code> <code>isofox_call</code> <code>kallisto</code> <code>link_bam</code> <code>lofreq_call_up</code> <code>lofreq_norm_filter</code> <code>lofreq_somatic_unpaired</code> <code>make_region_bed_list</code> <code>map_reads_normal</code> <code>map_reads_tumor</code> <code>map_reads_tumor_unpaired</code> <code>mark_duplicates_normal</code> <code>mark_duplicates_tumor</code> <code>mark_duplicates_tumor_unpaired</code> <code>merge_paired_germ_maf</code> <code>merge_paired_maf</code> <code>merge_paired_vcf</code> <code>merge_rna_maf</code> <code>merge_strelka_manta</code> <code>merge_strelka_manta_wgs</code> <code>merge_strelka_somatic_manta</code> <code>merge_strelka_somatic_manta_wgs</code> <code>merge_unpaired_maf</code> <code>merge_unpaired_vcf</code> <code>muse_call</code> <code>muse_call_wgs</code> <code>muse_sump</code> <code>muse_sump_wgs</code> <code>mutect2</code> <code>mutect2_call</code> <code>mutect2_wgs</code> <code>norm_filter_HaplotypeCaller</code> <code>norm_filter_freebayes</code> <code>picard_collect_wes_normal</code> <code>picard_collect_wes_tumor</code> <code>picard_collect_wgs_normal</code> <code>picard_collect_wgs_tumor</code> <code>picard_flength_wgs_normal</code> <code>picard_flength_wgs_tumor</code> <code>plot_freec</code> <code>prep_multiqc_data</code> <code>prep_multiqc_data_tumor_only</code> <code>prep_multiqc_data_wgs</code> <code>recal_link_normal</code> <code>recal_link_tumor</code> <code>recal_link_tumor_unpaired</code> <code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code> <code>run_cancer_report</code> <code>salmon</code> <code>sequenza_bam2seqz</code> <code>sequenza_call</code> <code>sequenza_seqz_binning</code> <code>unpair_lofreq_filter</code> <code>unpaired_call_config_strelka</code> <code>unpaired_call_config_strelka_rna</code> <code>unpaired_call_strelka_manta</code> <code>unpaired_call_strelka_manta_rna</code> <code>unpaired_call_variants_HaplotypeCaller</code> <code>unpaired_filter_vardict</code> <code>unpaired_filter_vardict_rna</code> <code>unpaired_freebayes</code> <code>unpaired_freebayes_rna</code> <code>unpaired_mutect2_call</code> <code>unpaired_strelka_filter</code> <code>unpaired_strelka_filter_rna</code> <code>unpaired_vardict_single_mode</code> <code>unpaired_vardict_single_mode_rna</code> <code>vardict_filter_somatic</code> <code>vardict_filter_somatic_wgs</code> <code>vardict_paired_mode</code> <code>vardict_paired_mode_wgs</code> <code>vardict_wgs_bed_wgs</code> <code>varscan2_call</code> <code>varscan2_call_unpaired_indel</code> <code>varscan2_call_unpaired_indel_rna</code> <code>varscan2_call_unpaired_snp</code> <code>varscan2_call_unpaired_snp_rna</code> <code>varscan2_call_wgs</code> <code>varscan2_filter_indel</code> <code>varscan2_filter_snp</code> <code>varscan2_merge_somatic</code> <code>varscan2_merge_somatic_wgs</code> <code>varscan2_merge_unpaired</code> <code>varscan2_merge_unpaired_rna</code> <code>varscan2_mpileup</code> <code>varscan2_mpileup_unpaired</code> <code>varscan2_mpileup_unpaired_rna</code> <code>varscan2_mpileup_wgs</code> <code>varscan2_processSomatic</code> <code>varscan2_processSomatic_wgs</code> <code>varscan2_som_filter</code> <code>varscan2_som_filter_wgs</code> <code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code> <code>vcf_norm_HaplotypeCaller</code> <code>vcf_norm_Mutect2</code> <code>vcf_norm_germline_caveman</code> <code>vcf_norm_germline_strelkamanta</code> <code>vcf_norm_muse</code> <code>vcf_norm_vardict</code> <code>vcf_norm_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>recal_bqsr</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">BQSR (upstream config[&#x27;project&#x27;][&#x27;recal_BQSR&#x27;] + resources[&#x27;varanno&#x27;][genome]):<br>recal_bqsr = false is the upstream mini-test default (recal_link symlinks the<br>dedup BAM); set true to run BaseRecalibrator + ApplyBQSR instead.</p>
<details class="ox-param-usedby"><summary>used by 9 rules</summary>
<div class="ox-param-rules"><code>apply_base_quality_recalibration_normal</code> <code>apply_base_quality_recalibration_tumor</code> <code>apply_base_quality_recalibration_tumor_unpaired</code> <code>recal_link_normal</code> <code>recal_link_tumor</code> <code>recal_link_tumor_unpaired</code> <code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>reference</code><span class="ox-param-default">test/fixtures/refs/sequence/Homo_sapiens_assembly38_chr21.fasta</span></div>
<p class="ox-param-desc">Resources (upstream: config[&#x27;resources&#x27;][genome_version])</p>
<details class="ox-param-usedby"><summary>used by 103 rules</summary>
<div class="ox-param-rules"><code>CM_call</code> <code>CM_flag</code> <code>CNA_exomedepth</code> <code>M2_SNC</code> <code>M2_SNC_wgs</code> <code>M2_ST</code> <code>M2_ST_wgs</code> <code>M2_filter</code> <code>M2_filter_unpaired</code> <code>M2_filter_unpaired_rna</code> <code>M2_filter_wgs</code> <code>STAR_1_pass</code> <code>SV_delly</code> <code>SV_delly_germ</code> <code>SV_svaba</code> <code>SplitNCigarReads</code> <code>apply_base_quality_recalibration_normal</code> <code>apply_base_quality_recalibration_tumor</code> <code>apply_base_quality_recalibration_tumor_unpaired</code> <code>arriba_fusion</code> <code>call_config_strelka</code> <code>call_config_strelka_wgs</code> <code>call_strelka_manta_germline</code> <code>call_strelka_manta_wgs</code> <code>call_strelka_somatic_manta</code> <code>call_strelka_somatic_manta_wgs</code> <code>call_variants_HaplotypeCaller</code> <code>call_variants_HaplotypeCaller_rna</code> <code>call_variants_HaplotypeCaller_wgs</code> <code>delly2bnd</code> <code>freec_config</code> <code>isofox_call</code> <code>lofreq_call_up</code> <code>lofreq_norm_filter</code> <code>lofreq_somatic_unpaired</code> <code>map_reads_normal</code> <code>map_reads_tumor</code> <code>map_reads_tumor_unpaired</code> <code>muse_call</code> <code>muse_call_wgs</code> <code>mutect2</code> <code>mutect2_call</code> <code>mutect2_wgs</code> <code>norm_filter_HaplotypeCaller</code> <code>norm_filter_freebayes</code> <code>picard_collect_wes_normal</code> <code>picard_collect_wes_tumor</code> <code>picard_collect_wgs_normal</code> <code>picard_collect_wgs_tumor</code> <code>picard_flength_wgs_normal</code> <code>picard_flength_wgs_tumor</code> <code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code> <code>sequenza_bam2seqz</code> <code>unpair_lofreq_filter</code> <code>unpaired_call_config_strelka</code> <code>unpaired_call_config_strelka_rna</code> <code>unpaired_call_strelka_manta</code> <code>unpaired_call_strelka_manta_rna</code> <code>unpaired_call_variants_HaplotypeCaller</code> <code>unpaired_freebayes</code> <code>unpaired_freebayes_rna</code> <code>unpaired_mutect2_call</code> <code>unpaired_vardict_single_mode</code> <code>unpaired_vardict_single_mode_rna</code> <code>vardict_paired_mode</code> <code>vardict_paired_mode_wgs</code> <code>vardict_wgs_bed_wgs</code> <code>varscan2_call</code> <code>varscan2_call_unpaired_indel_rna</code> <code>varscan2_call_unpaired_snp_rna</code> <code>varscan2_mpileup</code> <code>varscan2_mpileup_unpaired</code> <code>varscan2_mpileup_unpaired_rna</code> <code>varscan2_mpileup_wgs</code> <code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code> <code>vcf_norm_HaplotypeCaller</code> <code>vcf_norm_Mutect2</code> <code>vcf_norm_germline_caveman</code> <code>vcf_norm_germline_strelkamanta</code> <code>vcf_norm_muse</code> <code>vcf_norm_vardict</code> <code>vcf_norm_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>reference_dict</code><span class="ox-param-default">test/fixtures/refs/sequence/Homo_sapiens_assembly38_chr21.dict</span></div>
<p class="ox-param-desc">Resources (upstream: config[&#x27;resources&#x27;][genome_version])</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>bed_to_interval_list</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>rna_caller_list</code><span class="ox-param-default">freebayes, HaplotypeCaller, lofreq, Mutect2, vardict, varscan2</span></div>
<p class="ox-param-desc">RNA SNV callers for the vcf2maf merge tail (upstream<br>run_params.rna_caller_list in mini_test_data/rna/fusion/data/test_rna.yaml;<br>matches the six unrolled vcf2maf_rna_* rules in rules/rna/60_vcf2maf_merge.oxoflow)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rna_fastq_r1</code><span class="ox-param-default">test/fixtures/reads/mini-T_RNA_R1.fq.gz</span></div>
<p class="ox-param-desc">RNA (upstream wrapper/rna.smk; run_type = &quot;rna&quot;). Default stages:<br>[arriba, call_mut]; quant/isofox rules run when explicitly targeted.</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>STAR_1_pass</code> <code>STAR_arriba_map</code> <code>STAR_isofox_map</code> <code>STAR_mut_map</code> <code>cal_exp_RSEM</code> <code>fastp_trim</code> <code>kallisto</code> <code>salmon</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rna_fastq_r2</code><span class="ox-param-default">test/fixtures/reads/mini-T_RNA_R2.fq.gz</span></div>
<p class="ox-param-desc">RNA (upstream wrapper/rna.smk; run_type = &quot;rna&quot;). Default stages:<br>[arriba, call_mut]; quant/isofox rules run when explicitly targeted.</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>STAR_1_pass</code> <code>STAR_arriba_map</code> <code>STAR_isofox_map</code> <code>STAR_mut_map</code> <code>cal_exp_RSEM</code> <code>fastp_trim</code> <code>kallisto</code> <code>salmon</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rna_gtf</code><span class="ox-param-default">test/fixtures/refs/annotations/mini_chr21.gtf</span></div>
<p class="ox-param-desc">RNA (upstream wrapper/rna.smk; run_type = &quot;rna&quot;). Default stages:<br>[arriba, call_mut]; quant/isofox rules run when explicitly targeted.</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>STAR_1_pass</code> <code>STAR_arriba_map</code> <code>STAR_isofox_map</code> <code>STAR_mut_map</code> <code>arriba_draw</code> <code>arriba_fusion</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>rsem_index</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Quant indexes are empty in the upstream hg38_chr21 test config — the<br>RSEM/kallisto/salmon rules only run when explicitly targeted</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>cal_exp_RSEM</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_report</code><span class="ox-param-default">true</span></div>
<p class="ox-param-desc">Report stages (upstream <code>stages</code>): case_report + multiqc are ON in the port<br>default; set run_report = false to match the upstream mini-test default.</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>combined_multiqc</code> <code>combined_multiqc_prep_multiqc_data</code> <code>prep_multiqc_data</code> <code>prep_multiqc_data_tumor_only</code> <code>prep_multiqc_data_wgs</code> <code>run_cancer_report</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>run_type</code><span class="ox-param-default">wes</span></div>
<p class="ox-param-desc">Upstream Snakefile dispatch key (VALID_RUN_TYPES): wes | wgs | rna</p>
<details class="ox-param-usedby"><summary>used by 188 rules</summary>
<div class="ox-param-rules"><code>ASCAT_EXTRACT_PURITYPLOIDY</code> <code>CM_call</code> <code>CM_cnv</code> <code>CM_flag</code> <code>CM_germ_flag</code> <code>CNA_ASCAT</code> <code>CNA_exomedepth</code> <code>M2_SNC</code> <code>M2_SNC_wgs</code> <code>M2_ST</code> <code>M2_ST_wgs</code> <code>M2_contam</code> <code>M2_contam_wgs</code> <code>M2_filter</code> <code>M2_filter_unpaired</code> <code>M2_filter_unpaired_rna</code> <code>M2_filter_wgs</code> <code>RSEM_sort_genome</code> <code>STAR_1_pass</code> <code>STAR_arriba_map</code> <code>STAR_isofox_map</code> <code>STAR_mut_map</code> <code>SV_delly</code> <code>SV_delly_filter_somatic</code> <code>SV_delly_germ</code> <code>SV_delly_sample_tsv</code> <code>SV_delly_to_vcf</code> <code>SV_sansa_anno_svaba</code> <code>SV_sansa_annodelly</code> <code>SV_svaba</code> <code>SV_svanno_svaba</code> <code>SplitNCigarReads</code> <code>TRUST4_TBCR</code> <code>all</code> <code>all_cnv</code> <code>all_sv</code> <code>all_unpaired</code> <code>all_unpaired_maf</code> <code>all_vcf</code> <code>apply_base_quality_recalibration_normal</code> <code>apply_base_quality_recalibration_tumor</code> <code>apply_base_quality_recalibration_tumor_unpaired</code> <code>arriba_draw</code> <code>arriba_fusion</code> <code>bam_flagstat_normal</code> <code>bam_flagstat_tumor</code> <code>bed_to_interval_list</code> <code>cal_exp_RSEM</code> <code>call_config_strelka</code> <code>call_config_strelka_wgs</code> <code>call_strelka_manta_germline</code> <code>call_strelka_manta_wgs</code> <code>call_strelka_somatic_manta</code> <code>call_strelka_somatic_manta_wgs</code> <code>call_variants_HaplotypeCaller</code> <code>call_variants_HaplotypeCaller_rna</code> <code>call_variants_HaplotypeCaller_wgs</code> <code>combined_multiqc</code> <code>combined_multiqc_prep_multiqc_data</code> <code>delly2bnd</code> <code>delly_filter</code> <code>fastp_normal_sample</code> <code>fastp_trim</code> <code>fastp_tumor_sample</code> <code>fastp_tumor_sample_unpaired</code> <code>flag_mutation_pairead_maf</code> <code>freec_call_paired</code> <code>freec_config</code> <code>isofox_call</code> <code>kallisto</code> <code>link_bam</code> <code>lofreq_call_up</code> <code>lofreq_norm_filter</code> <code>lofreq_somatic_unpaired</code> <code>make_region_bed_list</code> <code>map_reads_normal</code> <code>map_reads_tumor</code> <code>map_reads_tumor_unpaired</code> <code>mark_duplicates_normal</code> <code>mark_duplicates_tumor</code> <code>mark_duplicates_tumor_unpaired</code> <code>merge_paired_germ_maf</code> <code>merge_paired_maf</code> <code>merge_paired_vcf</code> <code>merge_rna_maf</code> <code>merge_strelka_manta</code> <code>merge_strelka_manta_wgs</code> <code>merge_strelka_somatic_manta</code> <code>merge_strelka_somatic_manta_wgs</code> <code>merge_unpaired_maf</code> <code>merge_unpaired_vcf</code> <code>muse_call</code> <code>muse_call_wgs</code> <code>muse_sump</code> <code>muse_sump_wgs</code> <code>mutect2</code> <code>mutect2_call</code> <code>mutect2_wgs</code> <code>norm_filter_HaplotypeCaller</code> <code>norm_filter_freebayes</code> <code>picard_collect_wes_normal</code> <code>picard_collect_wes_tumor</code> <code>picard_collect_wgs_normal</code> <code>picard_collect_wgs_tumor</code> <code>picard_flength_wgs_normal</code> <code>picard_flength_wgs_tumor</code> <code>plot_freec</code> <code>prep_multiqc_data</code> <code>prep_multiqc_data_tumor_only</code> <code>prep_multiqc_data_wgs</code> <code>recal_link_normal</code> <code>recal_link_tumor</code> <code>recal_link_tumor_unpaired</code> <code>recalibrate_base_qualities_normal</code> <code>recalibrate_base_qualities_tumor</code> <code>recalibrate_base_qualities_tumor_unpaired</code> <code>run_cancer_report</code> <code>salmon</code> <code>sequenza_bam2seqz</code> <code>sequenza_call</code> <code>sequenza_seqz_binning</code> <code>unpair_lofreq_filter</code> <code>unpaired_call_config_strelka</code> <code>unpaired_call_config_strelka_rna</code> <code>unpaired_call_strelka_manta</code> <code>unpaired_call_strelka_manta_rna</code> <code>unpaired_call_variants_HaplotypeCaller</code> <code>unpaired_filter_vardict</code> <code>unpaired_filter_vardict_rna</code> <code>unpaired_freebayes</code> <code>unpaired_freebayes_rna</code> <code>unpaired_mutect2_call</code> <code>unpaired_strelka_filter</code> <code>unpaired_strelka_filter_rna</code> <code>unpaired_vardict_single_mode</code> <code>unpaired_vardict_single_mode_rna</code> <code>vardict_filter_somatic</code> <code>vardict_filter_somatic_wgs</code> <code>vardict_paired_mode</code> <code>vardict_paired_mode_wgs</code> <code>vardict_wgs_bed_wgs</code> <code>varscan2_call</code> <code>varscan2_call_unpaired_indel</code> <code>varscan2_call_unpaired_indel_rna</code> <code>varscan2_call_unpaired_snp</code> <code>varscan2_call_unpaired_snp_rna</code> <code>varscan2_call_wgs</code> <code>varscan2_filter_indel</code> <code>varscan2_filter_snp</code> <code>varscan2_merge_somatic</code> <code>varscan2_merge_somatic_wgs</code> <code>varscan2_merge_unpaired</code> <code>varscan2_merge_unpaired_rna</code> <code>varscan2_mpileup</code> <code>varscan2_mpileup_unpaired</code> <code>varscan2_mpileup_unpaired_rna</code> <code>varscan2_mpileup_wgs</code> <code>varscan2_processSomatic</code> <code>varscan2_processSomatic_wgs</code> <code>varscan2_som_filter</code> <code>varscan2_som_filter_wgs</code> <code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code> <code>vcf_norm_HaplotypeCaller</code> <code>vcf_norm_Mutect2</code> <code>vcf_norm_germline_caveman</code> <code>vcf_norm_germline_strelkamanta</code> <code>vcf_norm_muse</code> <code>vcf_norm_vardict</code> <code>vcf_norm_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>sage_ref_genome_version</code><span class="ox-param-default">38</span></div>
<p class="ox-param-desc">HMF tools (isofox; excluded for hg38_chr21 upstream — needs the multi-GB<br>hmf_pipeline_resources tree, not shipped in the mini-test)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>isofox_call</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>salmon_index</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Quant indexes are empty in the upstream hg38_chr21 test config — the<br>RSEM/kallisto/salmon rules only run when explicitly targeted</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>salmon</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>sansa_call</code><span class="ox-param-default">sansa</span></div>
<p class="ox-param-desc">SV annotation branch (issue #7; upstream WGS SV rules gate on the sansa<br>software config being present — absent upstream by default, so these are<br>off by default and the port mirrors that with empty keys = zero instances).<br>sansa_db/sansa_g: the sansa annotate -a database and -g gene-model inputs<br>(upstream softwares.sansa[&lt;genome_version&gt;].{db,g}); sansa_call: the<br>binary/invocation (upstream config[softwares][sansa][call]).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>SV_sansa_anno_svaba</code> <code>SV_sansa_annodelly</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>sansa_db</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">SV annotation branch (issue #7; upstream WGS SV rules gate on the sansa<br>software config being present — absent upstream by default, so these are<br>off by default and the port mirrors that with empty keys = zero instances).<br>sansa_db/sansa_g: the sansa annotate -a database and -g gene-model inputs<br>(upstream softwares.sansa[&lt;genome_version&gt;].{db,g}); sansa_call: the<br>binary/invocation (upstream config[softwares][sansa][call]).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>SV_sansa_anno_svaba</code> <code>SV_sansa_annodelly</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>sansa_g</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">SV annotation branch (issue #7; upstream WGS SV rules gate on the sansa<br>software config being present — absent upstream by default, so these are<br>off by default and the port mirrors that with empty keys = zero instances).<br>sansa_db/sansa_g: the sansa annotate -a database and -g gene-model inputs<br>(upstream softwares.sansa[&lt;genome_version&gt;].{db,g}); sansa_call: the<br>binary/invocation (upstream config[softwares][sansa][call]).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>SV_sansa_anno_svaba</code> <code>SV_sansa_annodelly</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>sequenza_gc_wiggle</code><span class="ox-param-default">test/fixtures/cnv/sequenza_gc.wig</span></div>
<p class="ox-param-desc">CNV branch (upstream somatic_cnv_list; mini-test default = [notrun]<br>sentinel -&gt; off). Set true to run the ported subset<br>(freec/sequenza/exomedepth/ASCAT — purple/amber/cobalt/facets need the<br>upstream&#x27;s custom containers, see rules/80_cnv.oxoflow).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>sequenza_bam2seqz</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>somatic_caller_list</code><span class="ox-param-default">HaplotypeCaller, vardict, varscan2, muse, Mutect2</span></div>
<p class="ox-param-desc">Caller lists (upstream run_params)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>star_index</code><span class="ox-param-default">test/fixtures/refs/star_index</span></div>
<p class="ox-param-desc">STAR index built inline by STAR_1_pass when missing (upstream ships a<br>pre-built index; the synthetic fixture reference needs its own)</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>STAR_1_pass</code> <code>STAR_arriba_map</code> <code>STAR_isofox_map</code> <code>STAR_mut_map</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>svanno_gtf</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">svanno: gatk SVAnnotate needs a protein-coding GTF (upstream<br>resources[genome_version].GTF). Empty default = rule never runs.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>SV_svanno_svaba</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>target_bed</code><span class="ox-param-default">test/fixtures/bed/exome_target_hg38_chr21.bed</span></div>
<p class="ox-param-desc">Resources (upstream: config[&#x27;resources&#x27;][genome_version])</p>
<details class="ox-param-usedby"><summary>used by 33 rules</summary>
<div class="ox-param-rules"><code>M2_SNC</code> <code>M2_SNC_wgs</code> <code>M2_ST</code> <code>M2_ST_wgs</code> <code>M2_filter</code> <code>bed_to_interval_list</code> <code>call_config_strelka</code> <code>call_strelka_manta_germline</code> <code>call_strelka_somatic_manta</code> <code>call_variants_HaplotypeCaller</code> <code>call_variants_HaplotypeCaller_rna</code> <code>freec_config</code> <code>lofreq_somatic_unpaired</code> <code>muse_call</code> <code>mutect2</code> <code>mutect2_call</code> <code>unpaired_call_config_strelka</code> <code>unpaired_call_config_strelka_rna</code> <code>unpaired_call_strelka_manta</code> <code>unpaired_call_strelka_manta_rna</code> <code>unpaired_call_variants_HaplotypeCaller</code> <code>unpaired_freebayes</code> <code>unpaired_freebayes_rna</code> <code>unpaired_mutect2_call</code> <code>unpaired_vardict_single_mode</code> <code>unpaired_vardict_single_mode_rna</code> <code>vardict_paired_mode</code> <code>varscan2_call</code> <code>varscan2_call_unpaired_indel_rna</code> <code>varscan2_call_unpaired_snp_rna</code> <code>varscan2_mpileup</code> <code>varscan2_mpileup_unpaired</code> <code>varscan2_mpileup_unpaired_rna</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>trust4_dir</code><span class="ox-param-default">resources/softwares/TRUST4</span></div>
<p class="ox-param-desc">TRUST4 (upstream softwares_params[genome].trust4; git-cloned at rule<br>runtime into trust4_dir when trust4_f is missing — not in default stages)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>TRUST4_TBCR</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>trust4_f</code><span class="ox-param-default">resources/softwares/TRUST4/hg38_bcrtcr.fa</span></div>
<p class="ox-param-desc">TRUST4 (upstream softwares_params[genome].trust4; git-cloned at rule<br>runtime into trust4_dir when trust4_f is missing — not in default stages)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>TRUST4_TBCR</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>trust4_ref</code><span class="ox-param-default">resources/softwares/TRUST4/human_IMGT+C.fa</span></div>
<p class="ox-param-desc">TRUST4 (upstream softwares_params[genome].trust4; git-cloned at rule<br>runtime into trust4_dir when trust4_f is missing — not in default stages)</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>TRUST4_TBCR</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>tumor_fastq_r1</code><span class="ox-param-default">test/fixtures/reads/mini-T_R1.fq.gz</span></div>
<p class="ox-param-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>fastp_tumor_sample</code> <code>fastp_tumor_sample_unpaired</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>tumor_fastq_r2</code><span class="ox-param-default">test/fixtures/reads/mini-T_R2.fq.gz</span></div>
<p class="ox-param-desc">Reads (upstream samplesheet columns Tumor_R1_file_path / Normal_R1_file_path<br>...). The sample-sheet pairs (pairs_file above) drive {pair_id}/{experiment}/<br>{control} fan-out; these config paths are the fixture FASTQ locations.</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>fastp_tumor_sample</code> <code>fastp_tumor_sample_unpaired</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>unpaired_caller_list</code><span class="ox-param-default">Mutect2, HaplotypeCaller, varscan2, strelka, vardict, lofreq, freebayes</span></div>
<p class="ox-param-desc">Tumor-only callers (upstream run_params.tumor_only_caller; upstream default<br>is [sage] — needs the custom hmftools container, so the port defaults to<br>the seven portable callers, see rules/70_unpaired.oxoflow)</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>vep_cache_ready</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">VEP needs a local cache at {vep_data}/{vep_species} (~10GB download; the<br>fixture kit does not ship it). The vcf2maf rules and the downstream MAF<br>merge/flag/cancer-report tail gate on this flag — set true once the cache<br>is in place (upstream fails hard without it).</p>
<details class="ox-param-usedby"><summary>used by 28 rules</summary>
<div class="ox-param-rules"><code>all</code> <code>all_unpaired_maf</code> <code>flag_mutation_pairead_maf</code> <code>merge_paired_germ_maf</code> <code>merge_paired_maf</code> <code>merge_rna_maf</code> <code>merge_unpaired_maf</code> <code>run_cancer_report</code> <code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>vep_cache_version</code><span class="ox-param-default">110</span></div>
<p class="ox-param-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])</p>
<details class="ox-param-usedby"><summary>used by 20 rules</summary>
<div class="ox-param-rules"><code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>vep_data</code><span class="ox-param-default">resources/ref_genome/hg38/vep</span></div>
<p class="ox-param-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])</p>
<details class="ox-param-usedby"><summary>used by 20 rules</summary>
<div class="ox-param-rules"><code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>vep_species</code><span class="ox-param-default">homo_sapiens</span></div>
<p class="ox-param-desc">vcf2maf / VEP (upstream: config[&#x27;softwares_params&#x27;][genome_version][&#x27;vcf2maf&#x27;])</p>
<details class="ox-param-usedby"><summary>used by 20 rules</summary>
<div class="ox-param-rules"><code>vcf2maf_HaplotypeCaller</code> <code>vcf2maf_Mutect2</code> <code>vcf2maf_germ_caveman</code> <code>vcf2maf_germ_strelkamanta</code> <code>vcf2maf_muse</code> <code>vcf2maf_rna_HaplotypeCaller</code> <code>vcf2maf_rna_Mutect2</code> <code>vcf2maf_rna_freebayes</code> <code>vcf2maf_rna_lofreq</code> <code>vcf2maf_rna_vardict</code> <code>vcf2maf_rna_varscan2</code> <code>vcf2maf_unpaired_HaplotypeCaller</code> <code>vcf2maf_unpaired_Mutect2</code> <code>vcf2maf_unpaired_freebayes</code> <code>vcf2maf_unpaired_lofreq</code> <code>vcf2maf_unpaired_strelka</code> <code>vcf2maf_unpaired_vardict</code> <code>vcf2maf_unpaired_varscan2</code> <code>vcf2maf_vardict</code> <code>vcf2maf_varscan2</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>wes_pon</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Upstream hg38_chr21 has no panel of normals (WES_PON: null) — leave empty</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>mutect2</code> <code>mutect2_call</code> <code>unpaired_mutect2_call</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>wgs_pon</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">Upstream hg38_chr21 has no panel of normals (WES_PON: null) — leave empty</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>mutect2_wgs</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-clindet pipeline overview](../assets/dag/oxo-flow-clindet.svg)

<p class="ox-dag-caption">figure · oxo-flow-clindet — Port of zyllifeworld/clindet in its upstream single-Snakefile form: one entry file, config run_type (wes|wgs|rna) selects the rule tree, and paired vs tumor-only WES is derived PER PAIR from the sample sheet (a pair without a control runs the tumor-only tree — engine wildcard-scoped when predicates).</p>

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or module overview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

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
- CNV: SM_check / CNA_ABSOLUTE_GISTIC / CNA_Battenberg — marked 'for future development' upstream (workflow/WES/rules/rtm/paired/CNV.smk comment); ABSOLUTE/GISTIC2 are Broad tools without conda packages, Battenberg needs the cgpbattenberg sif + 1000G impute reference data
- SV: gridss/BRASS/linx/igcaller/jasmine — upstream custom sifs (gridss 2.13.2, brass634, linx, jasminesv) or hardcoded local software paths (/public/ClinicalExam/...) plus Sanger/HMF reference trees; delly/svaba/Manta ARE ported
- unpaired-mode callers beyond the seven portable ones (sage/deepvariant/pindel/octopus/UnifiedGeniTyper — custom containers) + WGS Battenberg/ecDNA/VirusScan (custom containers + resource trees)
- conpair contamination check — custom conpair_latest.sif container
- ASCATsc (feeds the BRASS input chain; HMF ASCATsc.R) + multi-lane entry variant (mapping_muliti.smk) — non-default-path variants

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- sansa-annotation (SV_sansa_*) + svaba svanno — gated on an upstream sansa config absent from the mini test (svanno additionally needs the GTF, empty in the mini test)
- telomerecat — marked 'departed' upstream (workflow/WGS/rules/mapping.smk)

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
| SV_svaba | `SV_svaba` | svaba (container) | verbatim run; sansa/svanno annotation gates absent from the mini config — not ported |
| Manta SV | `call_config_strelka` (WGS) | manta | `somaticSV.vcf.gz` from the WGS Manta run (upstream SV list entry 'Manta') |

**Not ported** (upstream branches, verified at 582a9131): CNV purple/amber/cobalt/FACETS (custom hmftools.sif / facets-suite image + multi-GB hmf_pipeline_resources and snp-pileup PoN trees, pull_zenodo-built; unpaired CNV freec/purple likewise — the ported CNV gate is paired-only); CNV SM_check / CNA_ABSOLUTE_GISTIC / CNA_Battenberg (marked "for future development" upstream; ABSOLUTE/GISTIC2 have no conda packages, Battenberg needs the cgpbattenberg sif + 1000G impute data); SV gridss/BRASS/linx/igcaller/jasmine (custom sifs or hardcoded /public/ClinicalExam paths + Sanger/HMF reference trees — delly/svaba/Manta ARE ported); sansa-annotation + svaba svanno (sansa config absent from the mini test; svanno also needs the GTF, empty in the mini test); telomerecat ("departed" upstream); unpaired-mode callers beyond the seven portable ones (sage/deepvariant/pindel/octopus/UnifiedGeniTyper) + WGS Battenberg/ecDNA/VirusScan (custom containers + resource trees); conpair (custom conpair_latest.sif); ASCATsc (feeds the BRASS chain) + multi-lane entry variant (mapping_muliti.smk).

## Links

- Repository: [oxo-flow-clindet](https://github.com/WangLabCSU/oxo-flow-clindet)
- Upstream: [zyllifeworld/clindet](https://github.com/zyllifeworld/clindet) @ `582a9131`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
