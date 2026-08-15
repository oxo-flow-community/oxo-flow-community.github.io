# Clinical WES tumor/normal variant calling: SNV + germline, MAF annotation, case report

<div class="ox-page-badges"><span class="ox-badge">☆ Community</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

Clinical WES tumor/normal pipeline: fastp QC -> bwa+fixmate+samtools sort -> GATK markdup -> five SNV callers (Mutect2, VarDict, VarScan2, MuSE, HaplotypeCaller) plus germline Strelka2+Manta and CaVEMan -> bcftools normalization -> vcf2maf with VEP annotation -> merged MAF -> region-based mutation flagging -> cancer case report (Rmd/knitr) and MultiQC. Ported verbatim from zyllifeworld/clindet default paired WES path.

| | |
|---:|---|
| **Rating** | ☆ Community |
| **Origin** | port |
| **Domain** | cancer genomics (WES) |
| **Rules** | 60 |
| **Tools** | fastp · bwa (>=0.7.18) · samtools · gatk4 4.6.2.0 (container) · bcftools >=1.22 · bgzip · tabix · varscan 2.4.6 · vardict-java 1.8.3 (container) · muse 2.1.2 (container) · strelka2 · manta · caveman 1.15.3 (container) · vcf2maf 1.6.22 · ensembl-vep 114.2 · libboost 1.85.0 · multiqc · R >= 4.4 (knitr, data.table, gpgr via post-deploy) |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [zyllifeworld/clindet](https://github.com/zyllifeworld/clindet) |
| **Pinned version** | `582a9131` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.11.0

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

# 2. get this workflow
git clone https://github.com/WangLabCSU/oxo-flow-clindet
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastp QC/trimming
- bwa mem + samtools fixmate + sort (markdup-ready)
- GATK MarkDuplicates + CollectHsMetrics + BQSR-recal path (BQSR off by default)
- Somatic SNV: Mutect2 (with GetPileupSummaries/CalculateContamination), VarDict (testsomatic/var2vcf_paired), VarScan2 (mpileup/somatic/processSomatic/filter), MuSE (call/sump), HaplotypeCaller
- Germline: Strelka2 + Manta (config + runWorkflow), CaVEMan (call/flag/germline flag)
- bcftools normalization + per-caller FILTER rules
- vcf2maf with VEP (cache 110)
- MAF merge (somatic + germline)
- Mutation flagging against BED tracks (flag_mutation_maf.R)
- Cancer case report (Rmd sections) + MultiQC

**Excluded**

- CNV branch (purple/amber/cobalt/ASCAT/FACETS/sequenza/freec/exomedepth) — Broad-only, unbuildable without commercial licenses and heavy reference data
- Extended SV branch (delly/gridss/svaba/BRASS/linx/igv-caller/jasmine) — reference-data heavy, out of default mini-test path
- RNA branch (arriba/TRUST4/isofox/RNA SNV) — separate sample type, not in default WES path
- Unpaired (single-sample) mode — upstream default is paired T/N
- BQSR recalibration stage — upstream mini-test default sets recal_BQSR=false (the recal_link rules symlink the dedup BAM)

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| fastp (T/N) | `fastp_tumor_sample` / `fastp_normal_sample` | fastp | identical flags (`-w 8 -Q -c -L`) |
| bam flagstat (T/N) | `bam_flagstat_tumor` / `bam_flagstat_normal` | samtools | identical command |
| map_reads (T/N) | `map_reads_tumor` / `map_reads_normal` | bwa >=0.7.18, samtools | `bwa mem -MR` + `fixmate` + `sort` |
| mark_duplicates (T/N) | `mark_duplicates_tumor` / `mark_duplicates_normal` | gatk4 4.6.2.0 (container) | `MarkDuplicates --CREATE_INDEX true`, `VALIDATION_STRINGENCY SILENT` |
| recal_link (T/N) | `recal_link_tumor` / `recal_link_normal` | ln -s | BQSR off (upstream mini-test default) |
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
| CM_call / CM_flag | `CM_call` / `CM_flag` | caveman 1.15.3 (container) | `-td 2 -nd 2 -seqType WGS -no-flagging`, flag with `-umv .` |
| CM_germ_flag | `CM_germ_flag` | bcftools | `-e 'DP<=30' -s LowDP --mode x` |
| vcf_norm (per caller) | `vcf_norm_{Mutect2,vardict,varscan2,muse,HaplotypeCaller,germline_strelkamanta,germline_caveman}` | bcftools >=1.22 | verbatim per-caller FILTER rules incl. vardict contig-header branch |
| loop_vcf2maf_paired | `vcf2maf_{Mutect2,vardict,varscan2,muse,HaplotypeCaller}` | vcf2maf 1.6.22, ensembl-vep 114.2 | verbatim tumor/normal IDs per `get_vcf_name` |
| loop_vcf2maf_germ_paired | `vcf2maf_germ_strelkamanta` / `vcf2maf_germ_caveman` | vcf2maf 1.6.22 | TUMOUR/NORMAL for CaVEMan |
| merge_loop (somatic) | `merge_paired_maf` | merge_maf.R (verbatim) | driven via scripts/smk.R shim |
| merge_loop_germline | `merge_paired_germ_maf` | merge_maf.R (verbatim) | |
| make_region_bed_list + flag_mutation_pairead_maf | `make_region_bed_list` + `flag_mutation_pairead_maf` | flag_mutation_maf.R (verbatim) | empty bed_list = header-only TSV |
| run_cancer_report | `run_cancer_report` | R >=4.4 (knitr, gpgr via post-deploy) | only MAF/panel/Rmd params; CNV/QC params unset (NULL) as in upstream default path |
| combined_multiqc | `prep_multiqc_data` + `combined_multiqc_prep_multiqc_data` + `combined_multiqc` | multiqc | conpair/purple inputs out of scope |

**Not ported** (upstream branches outside the default paired WES path, with
reasons): CNV branch (purple/amber/cobalt/ASCAT/FACETS/sequenza/freec/
exomedepth — Broad-only, unbuildable without commercial licenses and heavy
reference data), extended SV branch (delly/gridss/svaba/BRASS/linx/
igv-caller/jasmine — reference-data heavy), RNA branch (arriba/TRUST4/
isofox/RNA SNV — separate sample type), unpaired (single-sample) mode.

## Links

- Repository: [oxo-flow-clindet](https://github.com/WangLabCSU/oxo-flow-clindet)
- Upstream: [zyllifeworld/clindet](https://github.com/zyllifeworld/clindet) @ `582a9131`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
