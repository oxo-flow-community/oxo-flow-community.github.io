# WGS/WES germline and somatic variant calling

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

GATK best-practice variant calling for whole-genome and whole-exome sequencing (WGS/WES), germline by default: FastQC quality control, fastp trimming and splitting, BWA-MEM alignment, MarkDuplicates with CRAM conversion, base quality score recalibration (BQSR), single-sample HaplotypeCaller variant calling, CNN 1D scoring with tranche filtering, VEP annotation, per-sample VCF QC and a final MultiQC report.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 20 |
| **Tools** | fastqc · fastp · bwa · samtools · gatk · mosdepth · bcftools · vcftools · ensembl-vep · multiqc |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/sarek](https://github.com/nf-core/sarek) |
| **Pinned version** | `3.10.0` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker) — pinned images

**Requirements.**
- paired-end FASTQ reads at raw/{sample}_R1.fastq.gz / raw/{sample}_R2.fastq.gz
- GRCh38 genome FASTA plus .fai and .dict
- GRCh38 BWA index directory (bwa_index_dir)
- GATK bundle known-sites VCFs with .tbi: dbsnp_146.hg38.vcf.gz, Mills_and_1000G_gold_standard.indels.hg38.vcf.gz, Homo_sapiens_assembly38.known_indels.vcf.gz
- VEP cache (GRCh38, homo_sapiens, cache version 116) mounted at /.vep in the container
- compute: up to 24 CPUs / 36 GB per rule (BWA-MEM 24 threads/30G; VEP 6 threads/36G)
- input cap: ~50M read pairs per sample (fastp split, see fidelity deviations)
- disk: results/ for per-sample CRAMs/VCFs/reports, plus the reference bundle and VEP cache

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-sarek
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastqc
- fastp
- bwa_mem
- gatk_markduplicates
- mosdepth_md
- samtools_stats_md
- gatk_baserecalibrator
- gatk_applybqsr
- samtools_index_recal
- mosdepth_recal
- samtools_stats_recal
- gatk_haplotypecaller
- gatk_cnnscorevariants
- gatk_filtervarianttranches
- bcftools_stats
- vcftools_tstv_count
- vcftools_tstv_qual
- vcftools_filter_summary
- ensemblvep_vep
- multiqc

**Excluded**

- NGSCheckMate (BAM_NGSCHECKMATE + BCFTOOLS_MPILEUP) — sample-identity QC, not on the ported default path
- TrimGalore trimming (--trim_fastq_trimgalore alternative; fastp is the upstream default)
- bwa-mem2 aligner (upstream default aligner is bwa-mem)
- save_output_as_bam=true BAM branch of MarkDuplicates (CRAM-only port)
- Strelka2, Mutect2, Manta, DeepVariant, CNVkit, ASCAT, MSIsensor, SomaticSniper, VarDict, FreeBayes, etc. — optional --tools callers, not on the default path
- reference preparation (BWA_INDEX, GATK4_CREATESEQUENCEDICTIONARY, SAMTOOLS_FAIDX) — not ported; the port requires a pre-built reference bundle (upstream also accepts these as inputs via params.bwa/dict/fasta_fai)
- interval preparation (gawk BUILD_INTERVALS, CREATE_INTERVALS_BED, TABIX bgzip/tabix interval split) and the per-interval scatter/gather of BQSR/ApplyBQSR/HaplotypeCaller (GATK4_GATHERBQSRREPORTS, CRAM_MERGE_INDEX_SAMTOOLS, GATK4_MERGEVCFS) — not ported; the port runs single whole-genome GATK jobs without --intervals (gathers are exact, so results are equivalent, but the per-contig parallelism of the upstream default path is absent)
- joint_germline GVCF joint-genotyping subworkflow (default joint_germline=false)
- UMI workflows (SAREK_UMI_*) — not on the default path
- fastp split parts beyond 0001. — supported input size is capped at one split part (~50M read pairs / 200M lines per sample): only part 0001 is wired fastp -> BWA. Multi-part splits (any real WGS dataset above the threshold) are a known unsupported upstream behavior — upstream aligns every part and merges the BAMs before MarkDuplicates (BAM_MERGE_INDEX_SAMTOOLS)

## Fidelity

Rows cover every upstream process/rule on the default main execution path.
"not ported" rows carry a reason.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command |
| FASTP | `fastp` | fastp 1.1.0 | upstream default trimming/fastp module; TrimGalore is the `--trim_fastq_trimgalore` alternative and is not ported |
| BWA_MEM | `bwa_mem` | bwa 0.7.19 | upstream default aligner is `bwa-mem`, not `bwa-mem2`; read-group flags from sarek.nf; prefix `{meta.id}.{reads[0] token}` = `test.0001` under split_fastq; the same image also carries samtools 1.22.1 (used for `samtools sort`) |
| GATK4_MARKDUPLICATES | `gatk_markduplicates` | gatk4 4.6.2.0 | CRAM-only port (`save_output_as_bam=false`); upstream's `if [[ ${prefix} == *.cram ]]` BAM branch not ported — conversion is unconditional |
| MOSDEPTH (post-MD) | `mosdepth_md` | mosdepth 0.3.14 | ext.prefix `{meta.id}.md`; WGS `--by 500` mode |
| SAMTOOLS_STATS (post-MD) | `samtools_stats_md` | samtools 1.24 | ext.prefix `{meta.id}.md.cram`; 1.24 is the version in the `htslib_samtools` stats/index images (the BWA image carries 1.22.1) |
| GATK4_BASERECALIBRATOR | `gatk_baserecalibrator` | gatk4 4.6.2.0 | known-sites = dbsnp + Mills gold standard + known indels (GRCh38); single whole-genome job, no per-interval scatter (see deviations) |
| GATK4_APPLYBQSR | `gatk_applybqsr` | gatk4 4.6.2.0 | output CRAM (not BAM) per default; single whole-genome job, no per-interval scatter (see deviations) |
| SAMTOOLS_INDEX (recal) | `samtools_index_recal` | samtools 1.24 | indexes the recalibrated CRAM |
| MOSDEPTH (recal) | `mosdepth_recal` | mosdepth 0.3.14 | ext.prefix `{meta.id}.recal` |
| SAMTOOLS_STATS (recal) | `samtools_stats_recal` | samtools 1.24 | ext.prefix `{meta.id}.recal.cram` |
| GATK4_HAPLOTYPECALLER | `gatk_haplotypecaller` | gatk4 4.6.2.0 | default `tools=haplotypecaller,vep` → `call_haplotypecaller=true`; single-sample mode (no `-ERC GVCF`), `--pcr-indel-model CONSERVATIVE`; single whole-genome job, no per-interval scatter (see deviations) |
| GATK4_CNNSCOREVARIANTS | `gatk_cnnscorevariants` | gatk4 4.6.2.0 | VCF_VARIANT_FILTERING_GATK part 1; CNN 1D scoring (module default `--tensor-type 1D`); upstream keeps the `{sample}.cnn.vcf.gz` intermediate unpublished — the port stores it under `results/variant_calling/cnnscorevariants/` for DAG handoff |
| GATK4_FILTERVARIANTTRANCHES | `gatk_filtervarianttranches` | gatk4 4.6.2.0 | VCF_VARIANT_FILTERING_GATK part 2; ext.args `--info-key CNN_1D`, ext.prefix `{meta.id}.haplotypecaller`, known sites (dbsnp + 2 GRCh38 indel sets) passed as `--resource`; produces `{sample}.haplotypecaller.filtered.vcf.gz` |
| BCFTOOLS_STATS | `bcftools_stats` | bcftools 1.23.1 | VCF_QC_BCFTOOLS_VCFTOOLS part 1; runs on the filtered VCF (prefix `{meta.id}.haplotypecaller.filtered`) |
| VCFTOOLS_TSTV_COUNT | `vcftools_tstv_count` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 2; runs on the filtered VCF |
| VCFTOOLS_TSTV_QUAL | `vcftools_tstv_qual` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 3; runs on the filtered VCF |
| VCFTOOLS_SUMMARY | `vcftools_filter_summary` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 4; runs on the filtered VCF |
| ENSEMBLVEP_VEP | `ensemblvep_vep` | ensembl-vep 116.0 | annotates the filtered VCF (`{sample}.haplotypecaller.filtered_VEP.ann.vcf.gz`); requires a VEP cache mounted at `/.vep` in the container (upstream bundles it via `--vep_cache`); `--cache_version 116`, GRCh38 |
| MULTIQC | `multiqc` | multiqc 1.35 | fan-in over all report producers; scans the results dir with the upstream `assets/multiqc_config.yml` |
| NGSCheckMate (BAM_NGSCHECKMATE + BCFTOOLS_MPILEUP) | — not ported | — | sample-identity QC on the CRAM; outside this port's scope (QC fan-in, needs a cohort reference) |
| PREPARE_GENOME (BWA_INDEX, GATK4_CREATESEQUENCEDICTIONARY, SAMTOOLS_FAIDX) | — not ported | — | reference preparation; the port requires a pre-built reference bundle (upstream also accepts pre-built index/dict/fai via `params.bwa`/`dict`/`fasta_fai`, so this is an upstream-compatible shortcut, not a behavior change) |
| BED_PREPARE_INTERVALS (BUILD_INTERVALS, CREATE_INTERVALS_BED, TABIX bgzip/tabix interval split) + per-interval scatter/gather (GATK4_GATHERBQSRREPORTS, CRAM_MERGE_INDEX_SAMTOOLS, GATK4_MERGEVCFS) | — not ported | — | interval preparation and the per-interval scatter/gather of BQSR/ApplyBQSR/HaplotypeCaller; the port runs single whole-genome GATK jobs without `--intervals` (gathers are exact, so results are equivalent, but the per-contig parallelism of the upstream default path is absent) |
| SAREK_UMI_* / Strelka2 / Mutect2 / Manta / DeepVariant / CNVkit / ASCAT / MSIsensor / ... | — not ported | — | UMI workflows, `--tools` alternatives and optional callers; out of scope (default `haplotypecaller,vep` only) |

Deviations (all documented, nothing silently dropped):

- **fastp split parts — supported input cap**: upstream `--split_by_lines`
  produces `0001.`-prefixed outputs; only the first split part (`0001.`) is
  wired to BWA-MEM (the nf-core bwa/mem prefix logic `tokenize('.')[0]` gives
  `{sample}.0001.bam`). The supported input size is therefore capped at one
  split part — ~50M read pairs / 200M lines per sample (the upstream default
  `split_fastq=50,000,000` threshold). Datasets above the threshold are a
  **known unsupported upstream behavior**: upstream aligns every part and
  merges the part BAMs before MarkDuplicates (`BAM_MERGE_INDEX_SAMTOOLS`),
  which this port does not reproduce — **do not run WGS data above ~50M read
  pairs per sample** with this port until the multi-part path is wired.
- **no per-interval scatter/gather**: BQSR, ApplyBQSR and HaplotypeCaller run
  as single whole-genome jobs (no `--intervals`, no
  GATK4_GATHERBQSRREPORTS / CRAM_MERGE_INDEX_SAMTOOLS / GATK4_MERGEVCFS).
  Gathers are exact, so the results are mathematically equivalent to
  upstream's, but wall-time and per-contig parallelism differ substantially.
- **CNN-scored intermediate location**: upstream disables the
  CNNSCOREVARIANTS publishDir (the `{sample}.cnn.vcf.gz` stays in the task
  workdir); oxo-flow hands files between rules through `results/`, so the
  port keeps it under `results/variant_calling/cnnscorevariants/`.
- **markduplicates CRAM branch**: unconditional `samtools view -Ch` +
  `samtools index` replaces upstream's bash conditional; BAM output mode
  (`save_output_as_bam=true`) is not ported.
- **Docker staging**: only the rule workdir is mounted, so reference files are
  copied into the workdir under fixed local names (`reference.fasta`,
  `reference.fasta.fai`, `reference.dict`) — same effect as Nextflow's
  staging of the reference into the task directory.
- **`known_indels`** is a TOML array (2 GRCh38 files); both it and
  `known_indels_tbi` must be updated together when changing references.

## Links

- Repository: [oxo-flow-sarek](https://github.com/oxo-flow-community/oxo-flow-sarek)
- Upstream: [nf-core/sarek](https://github.com/nf-core/sarek) @ `3.10.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
