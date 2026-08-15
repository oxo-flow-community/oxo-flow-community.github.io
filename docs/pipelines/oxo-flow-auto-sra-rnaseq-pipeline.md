# SRA-powered RNA-seq: .sra archives to differential expression

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

Automated RNA-seq analysis from locally downloaded SRA archives to differential expression results: verify and symlink .sra files, fasterq-dump conversion to FASTQ, read merging across multiple SRR runs per sample, fastp trimming, STAR alignment with gene counts, BAM indexing, BPM-normalized bigWig signal tracks, a merged count matrix, and DESeq2 differential analysis with ashr shrinkage. Every tool is pinned to an exact conda version for reproducibility.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | transcriptomics |
| **Rules** | 10 |
| **Tools** | sra-tools · fastp · star · samtools · deeptools · pandas · bioconductor-deseq2 · r-ashr · r-data.table |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [xuzhougeng/auto_sra_rnaseq_pipeline](https://github.com/xuzhougeng/auto_sra_rnaseq_pipeline) |
| **Pinned version** | `main` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned

**Requirements.**
- Reference data: STAR index dir and GTF (config index / GTF, e.g. GRCh38)
- Pre-downloaded .sra files at <sra_data_path>/<SRR>/<SRR>.sra, one metadata TSV row per sample (GSM) with columns: Dataset GSE GSM gene method celline group group_name type platform SRR paired
- Sample list in [[sample_groups]] and config db_id must match the metadata file (see repo README Usage)
- Compute: up to 20 threads / 10 GB per rule (align_and_count); 8 (data_clean_pair); 10 (bamtobw); 4 (build_bam_index)
- Disk: FASTQ, BAM and bigWig intermediates — several tens of GB for a typical cohort

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-auto-sra-rnaseq-pipeline
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- get_sra
- data_conversion_pair
- merge_R1_data
- merge_R2_data
- data_clean_pair
- align_and_count
- build_bam_index
- bamtobw
- combine_count
- DGE_analysis

**Excluded**

- data_conversion_single — single-end branch; upstream routes per sample by the metadata 'paired' column, oxo-flow cannot branch per sample (upstream example dataset D21122 is all-PAIRED)
- merge_data — single-end branch, not ported
- data_clean_single — single-end branch, not ported
- Snakefile_ENCODE — alternate entry point (ENCODE metadata format, DESeq2_diff_encode.R)
- run.py — batch runner over multiple metadata files (validation, bark/feishu notifications, --restart-times 3)
- bark/feishu notification flags — consumed only by run.py
- snakemake onerror email — oxo-flow has per-rule on_failure hooks, no workflow-level error hook
- slurm/config.yaml — cluster profile (use oxo-flow [cluster] instead)
- scripts/update_json.py — file_dict.json tracker used by external orchestration
- pigz_threads config key — merge rules use plain cat (pigz pipe commented out upstream)

## Fidelity

Scope: the **default-parameters main execution path** (upstream `rule all`).
Rows cover every upstream rule; "not ported" rows carry a reason.

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| get_sra | `get_sra` | python 3.11 + pandas 3.0.5 | run: block ported to `scripts/get_sra.py` (identical symlink logic); single-instance script rule (oxo-flow fans out over `{sample}`/`{pair_id}` only, upstream `{sra}` values come from the metadata TSV). Splits multi-SRR values on `srr_separator` like the upstream merge input functions and run.py `check_sra_files` (upstream get_sra itself does not split — latent bug for multi-SRR rows). No declared outputs (per-SRR paths are dynamic) |
| data_conversion_pair | `data_conversion_pair` | sra-tools 3.1.1 | `fasterq-dump sra/<SRR> -O sra` identical per SRR; upstream per-SRR jobs capped at 2 concurrent dumps (run.py `--resources limit_dump=2`) → script with an internal worker pool of 2. Script deps (python/pandas) join the download env — oxo-flow runs one environment per rule (upstream split input function + command across base/download envs) |
| data_conversion_single | not ported | — | single-end branch; upstream routes per sample by the metadata `paired` column, oxo-flow cannot branch per sample (upstream example dataset D21122 is all-PAIRED) |
| merge_R1_data | `merge_R1_data` | coreutils `cat` (via python script) | input function `get_merged_input_data_R1` ported to `scripts/merge_reads.py --read 1`; identical `cat ... > 00_raw_data/{sample}_R1.fq`. `limit_merge` cap preserved: 1 unit per rule + `[resource_groups] limit_merge = { max = 2 }` (upstream run.py `--resources limit_merge=2`) |
| merge_R2_data | `merge_R2_data` | coreutils `cat` (via python script) | same, `--read 2` |
| merge_data | not ported | — | single-end branch |
| data_clean_pair | `data_clean_pair` | fastp 1.3.6 | command byte-identical (`-w`, `-i/-I`, `-o/-O`, `-j log/{sample}.json`, `-h log/{sample}.html`, `&> log/{sample}_fastp.log`). Upstream does not pin fastp; resolved from bioconda on 2026-08-15. Threads 8 (upstream `fastp_threads` baked into `[rules.resources]`) |
| data_clean_single | not ported | — | single-end branch |
| align_and_count | `align_and_count` | star 2.7.1a | command byte-identical (flags, `--outFileNamePrefix`, `--limitBAMsortRAM $((10000 * 1000000))`, `--quantMode GeneCounts`, `--outTmpKeep None`, `mv ..._Log.final.out` to log). Threads 20 (upstream `star_threads` baked in). Attempt-based memory escalation lambda (`10000` → `60000*(attempt-1)`) not expressible — first-attempt value pinned (`resources.memory = "10G"`) |
| build_bam_index | `build_bam_index` | samtools 1.24 | `samtools index -@ 4 {input}` identical; upstream unpinned, resolved from bioconda 2026-08-15 |
| bamtobw | `bamtobw` | deeptools 3.5.6 | command byte-identical (`-p 10 --binSize 50 --effectiveGenomeSize 2913022398 --normalizeUsing BPM -b ... -o 04_bigwig/{sample}.bw`); upstream unpinned, resolved from bioconda 2026-08-15 |
| combine_count | `combine_count` | python 3.11 + pandas 3.0.5 | run: block ported verbatim to `scripts/combine_count.py` (same merge order and column renaming); per-sample counts gathered via `expand_inputs`. Adds a fail-fast check that `[config] db_id` matches the metadata file name. Upstream runs in the snakemake base env (`snakemake==8.16 pandas`); snakemake itself not needed — oxo-flow is the orchestrator |
| DGE_analysis | `DGE_analysis` | R 4.3.2, DESeq2 1.42.0, ashr 2.2.63, data.table 1.18.4 | `scripts/DESeq2_diff.R` ported verbatim (design `~group`, contrast `treat`/`control`, `lfcShrink(type="ashr")`, saves exprSet + metadata + diffResults). Env pins from the upstream Dockerfile (r432 env); r-data.table resolved from conda-forge 2026-08-15; python added for the on_success mail hook |
| onsuccess | `on_success` (DGE_analysis) | shell + smtplib | workflow-level `onsuccess` → final rule's hook: `rm -rf 02_read_align` + conditional email via `scripts/send_mail.py` (port of `send_mail()`; upstream `client.quit()` NameError on SMTP failure fixed; notification failures exit 0 so they never fail a finished workflow). `mail` defaults to false, as upstream |
| onerror | not ported | — | oxo-flow has per-rule `on_failure` hooks, no workflow-level error hook |
| Snakefile_ENCODE | not ported | — | alternate entry point (ENCODE metadata columns, `DESeq2_diff_encode.R`) |
| run.py | not ported | — | batch runner over multiple metadata files (validation, bark/feishu, `--restart-times 3`); its `limit_dump`/`limit_merge` caps are ported as described above; for re-runs use `oxo-flow run --resume-failed` |
| slurm/config.yaml | not ported | — | cluster profile; oxo-flow's `[cluster]` section covers this |
| scripts/update_json.py | not ported | — | `file_dict.json` tracker used by external orchestration |
| pigz_threads config key | dropped | — | merge rules use plain `cat`; the pigz pipe is commented out upstream |

**Port-level conventions** (config-shape deviations, commands unchanged):
upstream derives the sample list (GSM column), the per-sample SRR lists and
DB_ID from the metadata TSV at load time; the port declares the samples in
`[[sample_groups]]`, reads SRR lists in the ported scripts, and takes DB_ID
from `[config] db_id` — all three must match the metadata file (see the
repo README Usage). Upstream `fastp_threads`/`star_threads` config keys are
baked into `[rules.resources] threads` (oxo-flow resource numbers are
literals). Upstream example metadata `doc/D21122.txt` (16 GSM samples,
all PAIRED) ships as the default fixture at
test/fixtures/metadata/D21122.txt.

## Links

- Repository: [oxo-flow-auto-sra-rnaseq-pipeline](https://github.com/oxo-flow-community/oxo-flow-auto-sra-rnaseq-pipeline)
- Upstream: [xuzhougeng/auto_sra_rnaseq_pipeline](https://github.com/xuzhougeng/auto_sra_rnaseq_pipeline) @ `main`
- License: Apache-2.0 (this workflow) · none (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
