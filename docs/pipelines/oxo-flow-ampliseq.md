# Amplicon sequencing (16S/ITS): DADA2 denoising, taxonomy assignment and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Amplicon sequencing analysis (16S/ITS) that takes raw paired-end reads through FastQC quality control, cutadapt primer trimming, DADA2 denoising (quality profiles, filterAndTrim, learnErrors, denoise, chimera removal, read tracking), taxonomy assignment against the SBDI-GTDB reference, a QIIME2 taxa barplot over sample metadata, an overall summary table and a MultiQC report.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | amplicon |
| **Rules** | 26 |
| **Tools** | fastqc · cutadapt · python · pandas · r-base · dada2 · bioconductor-digest · curl · biocontainers · qiime2 · multiqc |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/ampliseq](https://github.com/nf-core/ampliseq) |
| **Pinned version** | `2.18.0` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker/Singularity) — pinned images

**Requirements.**
- raw paired-end FASTQ reads per sample (raw/<sample>_R1.fastq.gz / _R2.fastq.gz) plus a sample groups file (default test/fixtures/groups.tsv)
- sample metadata TSV for the QIIME2 taxa barplot (config metadata_file, default test/fixtures/metadata.tsv); the SBDI-GTDB taxonomy reference database is downloaded automatically
- compute: up to 10 CPUs / 20 GB per rule (dada2_denoising with 48h limit, dada2_taxonomy with 24h limit); most rules need 1-6 CPUs / 1-6 GB
- host: Docker or Singularity to run the pinned container images, curl for the taxonomy-database download rule, and network access to figshare
- optional: disk for intermediates/ and results/ plus the auto-downloaded SBDI-GTDB reference database

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-ampliseq
```

## Parameters

| Parameter | Default | Used by |
|---:|---|---|
| `FW_primer` | `` | `cutadapt` |
| `RV_primer` | `` | `cutadapt` |
| `cutadapt_max_error_rate` | `0.1` | `cutadapt` |
| `cutadapt_min_overlap` | `3` | `cutadapt` |
| `dada_addspecies_allowmultiple` | `false` | `dada2_taxonomy` |
| `dada_assign_chunksize` | `10000` | `dada2_taxonomy` |
| `dada_assign_taxlevels` | `Domain,Kingdom,Phylum,Class,Order,Family,Genus,Species` | `dada2_taxonomy` |
| `dada_min_boot` | `50` | `dada2_taxonomy` |
| `dada_ref_taxonomy` | `sbdi-gtdb=R11-RS232-1` | — |
| `dada_ref_taxonomy_citation` | `Lundin D, Andersson A. SBDI Sativa curated 16S GTDB database. FigShare. doi: 10.17044/scilifelab.14869077.v12` | — |
| `dada_ref_taxonomy_dbversion` | `SBDI-GTDB-R11-RS232-1 (https://figshare.scilifelab.se/articles/dataset/SBDI_Sativa_curated_16S_GTDB_database/14869077/10)` | — |
| `dada_ref_taxonomy_title` | `SBDI-GTDB - Sativa curated 16S GTDB database - Release R11-RS232-1` | — |
| `dada_ref_taxonomy_urls` | `https://ndownloader.figshare.com/files/64711203,https://ndownloader.figshare.com/files/64711218` | `download_taxonomy_db` |
| `dada_taxonomy_rc` | `false` | `dada2_taxonomy` |
| `max_ee` | `2` | `dada2_filtntrim` |
| `max_len` | `Inf` | `dada2_filtntrim` |
| `mergepairs_strategy` | `merge` | `dada2_denoising` |
| `metadata_file` | `test/fixtures/metadata.tsv` | `qiime2_barplot` |
| `min_len` | `50` | `dada2_filtntrim` |
| `quality_type` | `Auto` | `dada2_denoising`, `dada2_err`, `dada2_filtntrim` |
| `run_id` | `1` | `dada2_denoising`, `dada2_err`, `dada2_merge`, `dada2_rmchimera`, `dada2_stats` |
| `sample_inference` | `independent` | `dada2_denoising` |
| `seed` | `100` | `dada2_denoising`, `dada2_err`, `dada2_taxonomy` |
| `skip_barplot` | `false` | `qiime2_barplot` |
| `skip_dada_taxonomy` | `false` | `dada2_taxonomy`, `download_taxonomy_db`, `format_taxonomy`, `qiime2_barplot`, `qiime2_intax` |
| `skip_fastqc` | `false` | `fastqc` |
| `skip_multiqc` | `false` | `multiqc` |
| `skip_qiime` | `false` | `qiime2_barplot`, `qiime2_inasv`, `qiime2_inseq`, `qiime2_intax` |
| `skip_taxonomy` | `false` | `dada2_taxonomy`, `download_taxonomy_db`, `format_taxonomy`, `qiime2_barplot`, `qiime2_intax` |
| `trunc_qmin` | `25` | `trunclen_fw`, `trunclen_rv` |
| `trunc_rmin` | `0.75` | `trunclen_fw`, `trunclen_rv` |
| `truncq` | `2` | `dada2_filtntrim` |

Derived from the workflow's `[config]` section — no schema file to maintain.

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- rename_raw_data_files
- fastqc
- cutadapt
- cutadapt_summary
- cutadapt_summary_merge
- dada2_quality_fw
- dada2_quality_rv
- trunclen_fw
- trunclen_rv
- dada2_filtntrim
- dada2_quality_fw_preprocessed
- dada2_quality_rv_preprocessed
- dada2_err
- dada2_denoising
- dada2_rmchimera
- dada2_stats
- dada2_merge
- merge_stats
- download_taxonomy_db
- format_taxonomy
- dada2_taxonomy
- qiime2_inasv
- qiime2_inseq
- qiime2_intax
- qiime2_barplot
- multiqc

**Excluded**

- dada2_its: ITS (fungal) analysis branch — not in the default main path (params.its false by default)
- qiime2: QIIME2 downstream analyses beyond the default taxa barplot (diversity, ANCOM, classifier training/prediction, feature table exports) — off by default (params.qiime2 false)
- nanopore: nanopore sequencing branch (params.nanopore false by default)
- syncom: synthetic community controls branch (params.syncom false by default)
- multi-run merge: DADA2_MERGE mergeSequenceTables branch for multiple --run_ids — single-run default path only
- picrust / other optional reports gated by additional params off by default

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| RENAME_RAW_DATA_FILES | `rename_raw_data_files` | nf-core/ubuntu 20.04 | identical command (soft links) |
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command; upstream publishes only `*.html` — the port also declares the `*.zip` files because MultiQC consumes them |
| CUTADAPT_BASIC | `cutadapt` | cutadapt 5.2 | identical `ext.args` (`-O 3 -e 0.1 -g/-G --discard-untrimmed`) |
| CUTADAPT_SUMMARY | `cutadapt_summary` | python 3.8.3 | verbatim `bin/cutadapt_summary.py`, `paired_end` mode |
| CUTADAPT_SUMMARY_MERGE | `cutadapt_summary_merge` | — | copy action |
| DADA2_QUALITY1 / DADA2_QUALITY2 | `dada2_quality_fw`, `dada2_quality_rv`, `dada2_quality_fw_preprocessed`, `dada2_quality_rv_preprocessed` | r-base 4.0.3 / dada2 1.26.0 | upstream runs the same process twice per stage with different prefixes; the port splits each into one rule per prefix |
| TRUNCLEN | `trunclen_fw`, `trunclen_rv` | pandas 1.1.5 | verbatim `bin/trunclen.py` |
| DADA2_FILTNTRIM | `dada2_filtntrim` | dada2 1.26.0 | identical `filterAndTrim` args; args file renamed `{sample}.filterAndTrim.args.txt` (all oxo-flow rules share one workdir, upstream name would collide); `ID` column uses the file basename so read-tracking sample names match upstream |
| DADA2_ERR | `dada2_err` | dada2 1.26.0 | identical `learnErrors` args + `checkConvergence`/`plotErrors` outputs |
| DADA2_DENOISING | `dada2_denoising` | dada2 1.26.0 | identical `dada` (incl. `getDadaOpt` defaults) + `mergePairs` + `makeSequenceTable`; `params.sample_inference` wired to `pool =` (upstream only records it in the args file); retries=3 (upstream `error_retry`), 48h limit (`process_long`) |
| DADA2_RMCHIMERA | `dada2_rmchimera` | dada2 1.26.0 | identical `removeBimeraDenovo` args |
| DADA2_STATS | `dada2_stats` | dada2 1.26.0 | identical read-tracking table |
| DADA2_MERGE | `dada2_merge` | dada2 1.26.0 / digest 0.6.27 | single-run default path only; multi-run `mergeSequenceTables` branch not ported |
| MERGE_STATS_STD | `merge_stats` | r-base 4.0.3 | identical merge by `sample` |
| DB download (launcher) | `download_taxonomy_db` | curl | upstream downloads the reference DB in the Nextflow launcher (`file(url)`); the port makes it an explicit system-backend rule |
| FORMAT_TAXONOMY | `format_taxonomy` | biocontainers 1.2.0 | verbatim `bin/taxref_reformat_sbdi-gtdb.sh`; runs in a scratch dir (the script globs `*`) |
| DADA2_TAXONOMY + DADA2_ADDSPECIES + collectFile | `dada2_taxonomy` | dada2 1.26.0 | **merged**: upstream splits `ASV_seqs.fasta` into 10000-sequence chunks (`splitFasta by: 10000`) and runs assignTaxonomy + addSpecies per chunk, then concatenates chunk tables with header + sorted rows (`collectFile keepHeader, skip 1, sort`). The port replicates chunking with `awk` + per-chunk `Rscript` calls + `head`/`tail -n +2 | sort` concatenation — same chunk files, same args, same outputs. addSpecies resource hint (1 cpu/50G) becomes rule-level 10 cpus/20G, 24h limit |
| QIIME2_INASV | `qiime2_inasv` | qiime2 2026.4 | identical: biom convert + `tools import` `BIOMV210Format` |
| QIIME2_INSEQ | `qiime2_inseq` | qiime2 2026.4 | identical `FeatureData[Sequence]` import |
| QIIME2_INTAX | `qiime2_intax` | qiime2 2026.4 | verbatim `bin/parse_dada2_taxonomy.r` (porting change: output path is argv[2]) + `HeaderlessTSVTaxonomyFormat` import |
| QIIME2_BARPLOT | `qiime2_barplot` | qiime2 2026.4 | identical `taxa barplot` + `tools export` |
| MULTIQC | `multiqc` | multiqc 1.34 | identical command in a scratch dir (`multiqc` scans cwd `.`); verbatim `assets/multiqc_config.yml` |
| — (not ported) | — | — | ITS branch (`params.its`, default false), nanopore branch (`params.nanopore`, default false), syncom controls (`params.syncom`, default false), QIIME2 analyses beyond the barplot (diversity, ANCOM, classifier — `params.qiime2` default false), multi-run merge, `versions.yml` per-module tool version files, PICRUSt and other optional reports |

Other notes:

- `params.FW_primer`/`RV_primer` default to `null` upstream, which renders
  a literal `null` adapter into the cutadapt command; the port defaults
  them to empty strings (`-g ""`/`-G ""` = no 5'/3' adapter trimming), the
  behavior the upstream docs describe.
- All skip flags map 1:1 to `params.skip_*` (default false = full path).
  `skip_fastqc` requires `skip_multiqc` too — the MultiQC rule consumes the
  FastQC zips. `skip_taxonomy`/`skip_dada_taxonomy` additionally gate the
  QIIME2 taxonomy import and barplot, mirroring upstream's empty-taxonomy
  channel handling.
- `metadata_file` is a config key (default `test/fixtures/metadata.tsv`);
  upstream takes it from the samplesheet.

## Links

- Repository: [oxo-flow-ampliseq](https://github.com/oxo-flow-community/oxo-flow-ampliseq)
- Upstream: [nf-core/ampliseq](https://github.com/nf-core/ampliseq) @ `2.18.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
