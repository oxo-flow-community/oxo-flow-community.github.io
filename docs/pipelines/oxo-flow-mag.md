# Metagenome assembly, binning and taxonomic classification

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Turn paired-end metagenomic reads into quality-checked, taxonomically classified draft genomes: FastQC and fastp QC with phiX removal, SPAdes and MEGAHIT assembly, QUAST and Prodigal assessment, bowtie2 mapping, binning with six binners (MetaBAT2, MaxBin2, CONCOCT, COMEBin, MetaBinner, SemiBin2), BUSCO bin QC, GTDB-Tk classification with a combined summary, PROKKA annotation, ALE evaluation and a final MultiQC report. The default short-read path of nf-core/mag, faithfully ported with the same tool versions and commands.

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | metagenomics |
| **Rules** | 134 |
| **Compute** | up to 12 CPUs / 140 GB per rule (defaults 1 thread / 6 GB) |
| **Tools** | fastqc · fastp · bowtie2 · samtools · spades · megahit · quast · prodigal · bioawk · seqkit · metabat2 · maxbin2 · concoct · comebin · metabinner · semibin · busco · qsv · ale · gtdbtk · prokka · multiqc · python · pandas · biopython |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/mag](https://github.com/nf-core/mag) |
| **Pinned version** | `5.5.0` |

## Run it

```bash
oxo-flow run main.oxoflow
```

Download the GTDB-Tk database (~100 GB), set `config.gtdb_db`, then run — the default config otherwise points at committed test fixtures.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned

**Requirements.**
- input: paired-end reads as {sample}_R1.fastq.gz / {sample}_R2.fastq.gz in config.input_dir (default test/fixtures/raw); single-end not ported
- reference: GTDB-Tk database — download gtdbtk_data.tar.gz (~100 GB) or unpacked directory and set config.gtdb_db (oxo-flow cannot download it mid-run)
- reference: phiX genome FASTA bundled in the repo (assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz) — no download needed
- compute: up to 12 CPUs / 140 GB per rule (defaults 1 thread / 6 GB; per-rule maxima below)
- per-rule maxima: SPAdes 10 CPUs/72 GB/24 h; GTDB-Tk classifywf 2 CPUs/140 GB/12 h
- software: conda or mamba with the pinned envs/*.yaml environments (one per tool, no container layer)
- optional: disk — hundreds of GB for real datasets (GTDB-Tk database plus per-sample assemblies and bins)

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-mag
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-mag
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `ale_per_base_output` | `false` | ALE (upstream --ale_per_base_output default false -> --metagenome --nout) | — |
| `bin_concoct_chunksize` | `10000` | Binning options (upstream params with the same defaults) | `concoct_cutup_megahit`, `concoct_cutup_spades` |
| `bin_concoct_donotconcatlast` | `false` | — | — |
| `bin_concoct_overlap` | `0` | — | `concoct_cutup_megahit`, `concoct_cutup_spades` |
| `bin_max_size` | `` | — | — |
| `bin_metabinner_scale` | `large` | — | `metabinner_run_megahit`, `metabinner_run_spades` |
| `bin_min_size` | `0` | Bin size filtering (upstream --bin_min_size / --bin_max_size; defaults 0/null make the seqkit-based filter a no-op) | — |
| `cohort_samples` | `S1 S2` | Space-separated list of sample ids used by the binning-preparation bowtie2 alignment rules (binning_map_mode='group': every assembly is aligned against every sample's reads). Keep in sync with the sample group below. | `bowtie2_align_megahit`, `bowtie2_align_spades`, `semibin_megahit`, `semibin_spades` |
| `fastp_cut_mean_quality` | `15` | — | `fastp` |
| `fastp_qualified_quality` | `15` | — | `fastp` |
| `fastp_trim_polyg` | `false` | — | `fastp` |
| `gtdb_db` | `` | GTDB-Tk database: local path to the release .tar.gz or an unpacked directory (upstream --gtdb_db, ~100GB). oxo-flow cannot download it mid-run (the prep rule only unpacks), so the default is empty and run_gtdbtk=true fails fast until a local path is set. | `gtdbtk_db_preparation` |
| `gtdbtk_max_contamination` | `10.0` | — | `gtdbtk_megahit_comebin`, `gtdbtk_megahit_concoct`, `gtdbtk_megahit_maxbin2`, `gtdbtk_megahit_metabat2`, `gtdbtk_megahit_metabinner`, `gtdbtk_megahit_semibin2`, `gtdbtk_spades_comebin`, `gtdbtk_spades_concoct`, `gtdbtk_spades_maxbin2`, `gtdbtk_spades_metabat2`, `gtdbtk_spades_metabinner`, `gtdbtk_spades_semibin2` |
| `gtdbtk_min_af` | `0.65` | — | `gtdbtk_megahit_comebin`, `gtdbtk_megahit_concoct`, `gtdbtk_megahit_maxbin2`, `gtdbtk_megahit_metabat2`, `gtdbtk_megahit_metabinner`, `gtdbtk_megahit_semibin2`, `gtdbtk_spades_comebin`, `gtdbtk_spades_concoct`, `gtdbtk_spades_maxbin2`, `gtdbtk_spades_metabat2`, `gtdbtk_spades_metabinner`, `gtdbtk_spades_semibin2` |
| `gtdbtk_min_completeness` | `50.0` | GTDB-Tk (upstream params with the same defaults) | `gtdbtk_megahit_comebin`, `gtdbtk_megahit_concoct`, `gtdbtk_megahit_maxbin2`, `gtdbtk_megahit_metabat2`, `gtdbtk_megahit_metabinner`, `gtdbtk_megahit_semibin2`, `gtdbtk_spades_comebin`, `gtdbtk_spades_concoct`, `gtdbtk_spades_maxbin2`, `gtdbtk_spades_metabat2`, `gtdbtk_spades_metabinner`, `gtdbtk_spades_semibin2` |
| `gtdbtk_min_perc_aa` | `10` | — | `gtdbtk_megahit_comebin`, `gtdbtk_megahit_concoct`, `gtdbtk_megahit_maxbin2`, `gtdbtk_megahit_metabat2`, `gtdbtk_megahit_metabinner`, `gtdbtk_megahit_semibin2`, `gtdbtk_spades_comebin`, `gtdbtk_spades_concoct`, `gtdbtk_spades_maxbin2`, `gtdbtk_spades_metabat2`, `gtdbtk_spades_metabinner`, `gtdbtk_spades_semibin2` |
| `gtdbtk_place_species` | `false` | — | — |
| `gtdbtk_pplacer_cpus` | `1` | — | `gtdbtk_megahit_comebin`, `gtdbtk_megahit_concoct`, `gtdbtk_megahit_maxbin2`, `gtdbtk_megahit_metabat2`, `gtdbtk_megahit_metabinner`, `gtdbtk_megahit_semibin2`, `gtdbtk_spades_comebin`, `gtdbtk_spades_concoct`, `gtdbtk_spades_maxbin2`, `gtdbtk_spades_metabat2`, `gtdbtk_spades_metabinner`, `gtdbtk_spades_semibin2` |
| `gtdbtk_use_full_tree` | `false` | — | — |
| `input_dir` | `test/fixtures/raw` | Input directory containing {sample}_R1.fastq.gz / {sample}_R2.fastq.gz paired-end read files (upstream --input samplesheet; single-end and multi-library lanes are not ported). The repo default ships tiny test fixtures; point this at your data. | `fastp`, `fastqc_raw` |
| `max_unbinned_contigs` | `100` | — | `split_fasta_maxbin2_megahit`, `split_fasta_maxbin2_spades`, `split_fasta_metabat2_megahit`, `split_fasta_metabat2_spades`, `split_fasta_metabinner_megahit`, `split_fasta_metabinner_spades` |
| `metabat_rng_seed` | `1` | — | `metabat2_megahit`, `metabat2_spades` |
| `min_contig_size` | `1500` | — | `metabat2_megahit`, `metabat2_spades`, `metabinner_bins_megahit`, `metabinner_bins_spades`, `metabinner_kmer_megahit`, `metabinner_kmer_spades`, `metabinner_run_megahit`, `metabinner_run_spades`, `metabinner_tooshort_megahit`, `metabinner_tooshort_spades`, `semibin_megahit`, `semibin_spades`, `split_fasta_maxbin2_megahit`, `split_fasta_maxbin2_spades`, `split_fasta_metabat2_megahit`, `split_fasta_metabat2_spades`, `split_fasta_metabinner_megahit`, `split_fasta_metabinner_spades` |
| `min_length_unbinned_contigs` | `1000000` | — | `split_fasta_maxbin2_megahit`, `split_fasta_maxbin2_spades`, `split_fasta_metabat2_megahit`, `split_fasta_metabat2_spades`, `split_fasta_metabinner_megahit`, `split_fasta_metabinner_spades` |
| `out_dir` | `results` | — | `ale_megahit`, `ale_spades`, `bin_summary`, `bowtie2_align_megahit`, `bowtie2_align_spades`, `busco_megahit_comebin`, `busco_megahit_concoct`, `busco_megahit_maxbin2`, `busco_megahit_metabat2`, `busco_megahit_metabinner`, `busco_megahit_semibin2`, `busco_spades_comebin`, `busco_spades_concoct`, `busco_spades_maxbin2`, `busco_spades_metabat2`, `busco_spades_metabinner`, `busco_spades_semibin2`, `comebin_megahit`, `comebin_spades`, `concat_busco`, `concat_quast`, `concoct_extract_megahit`, `concoct_extract_spades`, `concoct_merge_megahit`, `concoct_merge_spades`, `depths_megahit`, `depths_spades`, `fastp`, `fastqc_raw`, `fastqc_trimmed`, `gtdbtk_megahit_comebin`, `gtdbtk_megahit_concoct`, `gtdbtk_megahit_maxbin2`, `gtdbtk_megahit_metabat2`, `gtdbtk_megahit_metabinner`, `gtdbtk_megahit_semibin2`, `gtdbtk_spades_comebin`, `gtdbtk_spades_concoct`, `gtdbtk_spades_maxbin2`, `gtdbtk_spades_metabat2`, `gtdbtk_spades_metabinner`, `gtdbtk_spades_semibin2`, `gtdbtk_summary`, `mag_depths_megahit_comebin`, `mag_depths_megahit_concoct`, `mag_depths_megahit_maxbin2`, `mag_depths_megahit_metabat2`, `mag_depths_megahit_metabinner`, `mag_depths_megahit_semibin2`, `mag_depths_spades_comebin`, `mag_depths_spades_concoct`, `mag_depths_spades_maxbin2`, `mag_depths_spades_metabat2`, `mag_depths_spades_metabinner`, `mag_depths_spades_semibin2`, `mag_depths_summary`, `maxbin2_megahit`, `maxbin2_spades`, `megahit`, `metabat2_megahit`, `metabat2_spades`, `metabinner_bins_megahit`, `metabinner_bins_spades`, `multiqc`, `phix_align`, `prodigal_megahit`, `prodigal_spades`, `prokka_megahit_comebin`, `prokka_megahit_concoct`, `prokka_megahit_maxbin2`, `prokka_megahit_metabat2`, `prokka_megahit_metabinner`, `prokka_megahit_semibin2`, `prokka_spades_comebin`, `prokka_spades_concoct`, `prokka_spades_maxbin2`, `prokka_spades_metabat2`, `prokka_spades_metabinner`, `prokka_spades_semibin2`, `quast_bins_megahit_comebin`, `quast_bins_megahit_concoct`, `quast_bins_megahit_maxbin2`, `quast_bins_megahit_metabat2`, `quast_bins_megahit_metabinner`, `quast_bins_megahit_semibin2`, `quast_bins_spades_comebin`, `quast_bins_spades_concoct`, `quast_bins_spades_maxbin2`, `quast_bins_spades_metabat2`, `quast_bins_spades_metabinner`, `quast_bins_spades_semibin2`, `quast_megahit`, `quast_spades`, `semibin_megahit`, `semibin_spades`, `seqkit_megahit_comebin`, `seqkit_megahit_concoct`, `seqkit_megahit_maxbin2`, `seqkit_megahit_metabat2`, `seqkit_megahit_metabinner`, `seqkit_megahit_semibin`, `seqkit_spades_comebin`, `seqkit_spades_concoct`, `seqkit_spades_maxbin2`, `seqkit_spades_metabat2`, `seqkit_spades_metabinner`, `seqkit_spades_semibin`, `spades`, `split_fasta_maxbin2_megahit`, `split_fasta_maxbin2_spades`, `split_fasta_metabat2_megahit`, `split_fasta_metabat2_spades`, `split_fasta_metabinner_megahit`, `split_fasta_metabinner_spades` |
| `phix_reference` | `assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz` | phiX reference (upstream --phix_reference default = projectDir/assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz) | `phix_build` |
| `prokka_fast_mode` | `false` | — | — |
| `prokka_with_compliance` | `false` | PROKKA (upstream params with the same defaults) | — |
| `reads_minlength` | `15` | fastp clipping (upstream params with the same defaults) | `fastp` |
| `run_gtdbtk` | `true` | GTDB-Tk gate: the ~100GB reference database is user-provided (see the README requirements); run_gtdbtk=false runs the full pipeline minus the GTDB-Tk classification (the documented live-test contract). | `gtdbtk_db_preparation`, `gtdbtk_megahit_comebin`, `gtdbtk_megahit_concoct`, `gtdbtk_megahit_maxbin2`, `gtdbtk_megahit_metabat2`, `gtdbtk_megahit_metabinner`, `gtdbtk_megahit_semibin2`, `gtdbtk_spades_comebin`, `gtdbtk_spades_concoct`, `gtdbtk_spades_maxbin2`, `gtdbtk_spades_metabat2`, `gtdbtk_spades_metabinner`, `gtdbtk_spades_semibin2`, `gtdbtk_summary` |
| `semibin_environment` | `global` | — | `semibin_megahit`, `semibin_spades` |
| `semibin_rng_seed` | `1` | — | `semibin_megahit`, `semibin_spades` |
| `shortread_percentidentity` | `` | — | — |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-mag rule-level DAG](../assets/dag/oxo-flow-mag.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- ale_megahit
- ale_spades
- bin_summary
- bowtie2_align_megahit
- bowtie2_align_spades
- bowtie2_build_megahit
- bowtie2_build_spades
- busco_megahit_comebin
- busco_megahit_concoct
- busco_megahit_maxbin2
- busco_megahit_metabat2
- busco_megahit_metabinner
- busco_megahit_semibin2
- busco_spades_comebin
- busco_spades_concoct
- busco_spades_maxbin2
- busco_spades_metabat2
- busco_spades_metabinner
- busco_spades_semibin2
- comebin_megahit
- comebin_spades
- concat_busco
- concat_quast
- concoct_cutup_megahit
- concoct_cutup_spades
- concoct_extract_megahit
- concoct_extract_spades
- concoct_megahit
- concoct_merge_megahit
- concoct_merge_spades
- concoct_spades
- concoct_table_megahit
- concoct_table_spades
- convert_depths_megahit
- convert_depths_spades
- depths_megahit
- depths_spades
- fastp
- fastqc_raw
- fastqc_trimmed
- gtdbtk_db_preparation
- gtdbtk_megahit_comebin
- gtdbtk_megahit_concoct
- gtdbtk_megahit_maxbin2
- gtdbtk_megahit_metabat2
- gtdbtk_megahit_metabinner
- gtdbtk_megahit_semibin2
- gtdbtk_spades_comebin
- gtdbtk_spades_concoct
- gtdbtk_spades_maxbin2
- gtdbtk_spades_metabat2
- gtdbtk_spades_metabinner
- gtdbtk_spades_semibin2
- gtdbtk_summary
- gunzip_megahit
- gunzip_spades
- mag_depths_megahit_comebin
- mag_depths_megahit_concoct
- mag_depths_megahit_maxbin2
- mag_depths_megahit_metabat2
- mag_depths_megahit_metabinner
- mag_depths_megahit_semibin2
- mag_depths_spades_comebin
- mag_depths_spades_concoct
- mag_depths_spades_maxbin2
- mag_depths_spades_metabat2
- mag_depths_spades_metabinner
- mag_depths_spades_semibin2
- mag_depths_summary
- maxbin2_megahit
- maxbin2_spades
- megahit
- metabat2_megahit
- metabat2_spades
- metabinner_bins_megahit
- metabinner_bins_spades
- metabinner_kmer_megahit
- metabinner_kmer_spades
- metabinner_run_megahit
- metabinner_run_spades
- metabinner_tooshort_megahit
- metabinner_tooshort_spades
- multiqc
- phix_align
- phix_build
- prodigal_megahit
- prodigal_spades
- prokka_megahit_comebin
- prokka_megahit_concoct
- prokka_megahit_maxbin2
- prokka_megahit_metabat2
- prokka_megahit_metabinner
- prokka_megahit_semibin2
- prokka_spades_comebin
- prokka_spades_concoct
- prokka_spades_maxbin2
- prokka_spades_metabat2
- prokka_spades_metabinner
- prokka_spades_semibin2
- quast_bins_megahit_comebin
- quast_bins_megahit_concoct
- quast_bins_megahit_maxbin2
- quast_bins_megahit_metabat2
- quast_bins_megahit_metabinner
- quast_bins_megahit_semibin2
- quast_bins_spades_comebin
- quast_bins_spades_concoct
- quast_bins_spades_maxbin2
- quast_bins_spades_metabat2
- quast_bins_spades_metabinner
- quast_bins_spades_semibin2
- quast_megahit
- quast_spades
- semibin_megahit
- semibin_spades
- seqkit_megahit_comebin
- seqkit_megahit_concoct
- seqkit_megahit_maxbin2
- seqkit_megahit_metabat2
- seqkit_megahit_metabinner
- seqkit_megahit_semibin
- seqkit_spades_comebin
- seqkit_spades_concoct
- seqkit_spades_maxbin2
- seqkit_spades_metabat2
- seqkit_spades_metabinner
- seqkit_spades_semibin
- spades
- split_fasta_maxbin2_megahit
- split_fasta_maxbin2_spades
- split_fasta_metabat2_megahit
- split_fasta_metabat2_spades
- split_fasta_metabinner_megahit
- split_fasta_metabinner_spades

**Excluded**

- longreads — long-read assemblies (Flye/MetaMDBG) and long-read binning, off by default
- refinement — DAS Tool binning refinement, off by default
- kaiju — taxonomic profiling with kaiju, off by default
- diamond — taxonomic profiling with diamond, off by default
- run_checkm / run_checkm2 / run_gunc — additional bin QC tools, off by default (the GTDB-Tk filter therefore uses BUSCO metrics only, which is the default configuration)
- bin_domain_classification (tiara) — off by default; all bins keep domain='unclassified' exactly like the upstream default
- hostremoval — off by default
- assembly_input / bbnorm / adapters trimming variants (adapterremoval, trimmomatic) — non-default preprocessing branches
- ancient_dna / catpack / virus_identification — dedicated subworkflows, off by default
- pydamage, checkm2 and gunc report pages — off by default
- BUSCO `*-busco.batch_summary.failed.txt` artifact — only produced by upstream when a BUSCO run fails
- nf-core boilerplate files (pipeline_summary/methods_description, versions.yml) — not part of the analysis

## Fidelity

| Upstream | Port | Notes |
|----------|------|-------|
| Process-per-(assembler, binner) with `meta` tuples | One rule per (assembler, binner, ...) combination, names hard-coded | oxo-flow has no assembler/binner wildcard; `04_binning` has 48 rules, `05_binqc` 41, `06_taxonomy` 28 |
| Nextflow task workdir per process | Shared workflow dir + per-rule `.tmp/` scratch dirs | Tools that write generic-named files (spades, megahit, busco, quast, prokka, gtdbtk) run inside a scratch subdir and move outputs out |
| bash task scripts | `sh -c` executor | Process substitution (`2> >(tee ...)` in fastp) replaced with a plain redirect; brace expansion (`short_summary.*.{txt,json}`) split into two `mv` commands |
| Two BUSCO/GTDB-Tk/QUAST_BINS/MAG_DEPTHS runs per group (bins + chunks) | One rule per group that runs the tool twice in separate scratch subdirs | The two upstream runs share output names (`S1-auto-busco.*`); they are kept apart by the publish dirs `...-unclassified-unrefined-{sample}/` and `...-unclassified-unrefined_unbinned-{sample}/` |
| GTDB-Tk QC filter (Groovy) | `scripts/filter_bins_by_qc.py` | Same semantics: negative readings dropped, bins without metrics dropped, pass iff any reading clears both thresholds; BUSCO `Duplicated` is the contamination column |
| `gtdbtk_single_job` option | Not ported | Off by default upstream |
| `gtdbtk_use_full_tree` / `gtdbtk_place_species` | Config keys not exposed | Off by default upstream |
| Empty bin groups crash upstream (BUSCO on no input) | Empty groups produce empty/touched outputs and skip downstream classification | The pipeline never fails on empty groups |
| Versions.yml / pipeline boilerplate (summary, methods_description) | Not ported | Not analysis output |
| `*-busco.batch_summary.failed.txt` | Not produced | Only exists upstream when a BUSCO run failed |
| `results/GenomeBinning/QC/BUSCO/` flat short_summaries | Published into the same per-group dir as upstream | Same publish pattern `*{.txt,.json,.log}` |
| Conda environments | `envs/*.yaml` with the same pins | `tar` added to `gunzip`/`gtdbtk_db_preparation` because there is no container layer; `split_fasta` and `mag_depths` pin `conda-forge::pandas=1.1.5` exactly like upstream (the other pins use the `bioconda::` channel prefix instead of `conda-forge::` — same package, same version) |
| QUAST_BINS / BUSCO / GTDB-Tk file names | `{assembler}-{binner}-unclassified-unrefined-{sample}[-unbinned]-...` in summary names, QC dirs and input globs | Matches upstream meta naming (`domain=unclassified`, `refinement=unrefined`/`unrefined_unbinned`); the port previously omitted `{sample}` from QUAST summary names and used `-unclassified-unrefined-` in bin input globs, where the files are actually named `{assembler}-{binner}-{sample}*` — the globs matched nothing (fixed) |
| METABAT2 `-m` clamp | `<1500` is clamped to `1500` in the rule shell | Upstream clamps in `conf/modules.config` (`ext.args`); port replicates it with a shell guard |
| METABAT2 / METABINNER_BINS discarded bins | tooShort/lowDepth moved to `GenomeBinning/{binner}/discarded/`; METABINNER unbinned also copied to `GenomeBinning/MetaBinner/unbinned/` | Matches the upstream `publishDir` patterns; the lowDepth move is guarded because `create_metabinner_bins.py` never emits that file |
| CONCOCT stats | clustering/merged CSV and coverage TSV copied to `GenomeBinning/CONCOCT/stats/` | Matches the upstream `*.{txt,csv,tsv}` publish pattern |
| COMEBin | no `-s large` argument | Upstream `COMEBIN_RUNCOMEBIN` passes no `ext.args` (the `-s` scale flag belongs to MetaBinner, which does pass it) |
| SemiBin2 `--environment` | passed only for single-sample cohorts | Matches upstream `meta.sample_count == 1` in `ext.args2` |
| METABINNER coverage profile | contig length filter uses `{config.min_contig_size}` (was hardcoded 1500) | Upstream passes `val_min_contig_size` to the awk filter |
| SPAdes (METASPADES) resources | 10 cpu / 72 GB / 24 h (was 12 cpu / 16 h) | Matches upstream `base.config` (`cpus = 10 * attempt`, `time = 24.h * attempt`); the `--memory 72` flag matches `memory = 72.GB` |
| MultiQC | report published to `multiqc/` (lowercase) with `--force` | Matches upstream publishDir and the nf-core multiqc module script |
| Convert-depths / split_fasta scratch | per-sample scratch dirs and guarded sample-scoped globs | oxo-flow executes rules in one shared working directory (upstream gives every task its own); the generic `mv *.abund` / `mv *.pooled.fa.gz *.remaining.fa.gz` would otherwise race or fail when a sample produces no such files |

### Not ported (off by default upstream)

Long-read assembly and binning, DAS Tool refinement, kaiju and diamond taxonomic profiling, CheckM/CheckM2/GUNC QC, tiara domain classification, host removal, ancient DNA, CAT/BAT, pydamage, hybrid assembly, and the benchmarking modes.

## Links

- Repository: [oxo-flow-mag](https://github.com/oxo-flow-community/oxo-flow-mag)
- Upstream: [nf-core/mag](https://github.com/nf-core/mag) @ `5.5.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
