# clindet completeness audit (2026-08-21, pilot)

Upstream: [zyllifeworld/clindet](https://github.com/zyllifeworld/clindet) @
`582a9131` · Port: `oxo-flow-clindet` (60 rules, WES default paired path).

This is the pilot for the §15 full-line completeness audit. Coverage tiers:
P0 portable gap (must port) · P1 objective blocker (evidence required) ·
P2 config variant (absorb as `[config]`).

## Upstream run modes vs port

| mode | upstream entry | port status |
|---|---|---|
| `wes` | wrapper/wes.smk (incl. the full WGS SV chain) | **partial** — default caller set ported; gaps below |
| `wgs` | wrapper/wgs.smk | **absent** |
| `rna` | wrapper/rna.smk | **absent** |
| `build_b37` | workflow/setup/rules/human_b37.smk (18 rules) | absent (setup tier) |
| `build_hg38` | workflow/setup/rules/human_hg38.smk (15 rules) | absent (setup tier) |
| `pull_zenodo` | env_setup.smk (container pulls) | absent (setup tier) |

Legacy template Snakefiles (`template/snake_*.smk`) are entry styles, not
branches — no porting work. Dead code on disk (bicseq2, octopus, lancet2,
ecDNA, virusbreakend, orange, ...) is not part of the executable DAG —
excluded from the audit, noted in the upstream inventory.

## RNA branch — P0 (first fill campaign)

| upstream rule | tool | env pin (upstream) | notes |
|---|---|---|---|
| `fastp_trim` | fastp | clindet.yaml | |
| `STAR_1_pass` | STAR | rsem.yaml (star>=2.7.11b) | |
| `STAR_arriba_map` | STAR | rsem.yaml | arriba-specific params |
| `STAR_mut_map` | STAR | rsem.yaml | SplitNCigarReads chain for SNV callers |
| `cal_exp_RSEM`, `RSEM_sort_genome` | RSEM+bowtie2 | rsem.yaml | |
| `kallisto` | kallisto | rsem.yaml | |
| `salmon` | salmon | rsem.yaml | |
| `mutect2_call`, `M2_filter_unpaired` | GATK4 | singularity pins | |
| `unpaired_freebayes`, `norm_filter_freebayes` | freebayes | | |
| `call_variants_HaplotypeCaller`, `norm_filter_HaplotypeCaller` | GATK4 | | |
| `unpaired_call_config_strelka`, `unpaired_call_strelka_manta`, `unpaired_strelka_filter` | strelka+manta | strelka.yaml | |
| `lofreq_call_up`, `lofreq_norm_filter` | lofreq | | |
| `unpaired_vardict_single_mode`, `unpaired_filter_vardict` | vardict-java | | |
| `varscan2_mpileup_unpaired`, `varscan2_call_unpaired_snp`, `varscan2_call_unpaired_indel`, `varscan2_filter_snp`, `varscan2_filter_indel`, `varscan2_merge_unpaired` | varscan2 | clindet.yaml (varscan=2.4.6) | |
| `loop_vcf2maf_rna`, `merge_rna_maf` | vcf2maf | clindet_vep.yaml | |
| `arriba_fusion`, `arriba_draw` | arriba 2.4.0 | singularity pin | gated genome b37/hg38/hg38_chr21 |
| `TRUST4_TBCR` | trust4 | rsem.yaml (trust4>=1.1.5) | upstream auto-clones repo at runtime → port must pre-pin (conda pin exists) |
| `STAR_isofox_map`, `isofox_call` | isofox 1.7.2 | hmftools.yaml | gated genome b37/hg38 |

Mode notes: `redup=False` hardcoded (link_bam branch); GATK backend is the
default (sentieon backend = P1, see below); RNA stages toggleable
(`salmon`/`kallisto`/`RSEM`/`TRUST4`/`arriba`/`isofox`/`call_mut`) →
port as rules + caller-list config (P2 pattern).

## WGS branch

- **P2 config absorption**: WES↔WGS switch is mostly per-rule bed/seqtype
  differences (`seqtype = WXS|WGS`, `vardict_wgs_bed`, `sequenza_gc_bins`).
  Absorb as `[config] run_type` + conditional params where the shared rule
  shells already exist.
- **P0**: WGS-only free tools — `paired_sage` + sage filter/annotation
  chain (pave), `deepvariant_somatic_call` (deepsomatic 1.10.0, free),
  `CNA_ASCAT_sc`, Battenberg v2/combine/ABSOLUTE_GISTIC (cgpbattenberg,
  free), sequenza extras.
- **P1**: `call_variants_sentieon` / `filter_sentieon` (commercial
  license, no OSS fallback in WGS mode).
- **P0 (SV chain, shared with WES mode)**: `SV_delly`+filter chain,
  `SV_gridss`+filter, `SV_svaba`+anno, `SV_brass`+bamstat (gated ascat_wgs
  + b37/hg38), `paired_linx`/`report_linx`, `SV_igcaller` (needs .sif),
  jasmine merge chain, delly2bnd/sansa. All tools free; reference-data
  heavy (P2 data notes).

## WES branch extras (already-ported path)

- **P0**: `conpair_*` chain (free, gated on conpair refs); `SM_check`;
  free CNV callers — `freec_*` (control-freec 11.6b, free),
  `CNA_exomedepth`, `facets_*` (facets-suite v2.0.8, free),
  `sequenza_*` (free). The port's blanket "CNV unbuildable without
  commercial licenses" claim is **wrong for these** — only ASCAT is
  license-gated.
- **P1**: `CNA_ASCAT`, `ASCAT_EXTRACT_PURITYPLOIDY`, `ASCAT_GISTIC`
  (academic license/registration; evidence: ASCAT distribution terms).
- **P2**: unpaired (tumor-only) mode — engine supports control-less
  pairs; caller selection lists → `[config]` lists; Mutect2 PoN flavors
  → config keys; `moalmanac_annotation` (free MIT, Docker Hub container →
  container portability convention); `run_cancer_report` (Rmd report —
  ported already as the report module? verify during fill).

## Setup modes (build_b37 / build_hg38 / pull_zenodo)

Separate tier — reference/container provisioning, not analysis. Recommend:
port as a dedicated `setup` include module (download rules + index
builders, free sources: GCS buckets, Zenodo, Sanger/Ensembl/NCBI FTP),
after the analysis branches. Not counted in `coverage` for the analysis
line but listed in the fidelity table.

## Verdict

- `coverage` today: `default-path` (WES default caller set only).
- P0 total: RNA branch (~35 rules) + SV chain (~20) + free CNV (~15) +
  WGS extras (~8). P1: sentieon (WGS), ASCAT (WES/WGS). P2: unpaired,
  caller selection, seqtype, PoN, setup tier.
- Fill order: RNA → SV chain → free CNV → WGS absorption → P2 config work
  → setup module → P1 documentation.
