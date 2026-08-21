# fetchngs completeness audit (2026-08-21)

Upstream: nf-core/fetchngs @ 1.12.0 · Port: `oxo-flow-fetchngs`
(live-verified).

## Mode matrix (upstream — single workflow, ID-prefix routing)

| axis | options |
|---|---|
| input IDs | SRA/SRP/SRS/SRX/SRR, ENA (ERA/ERP/ERS/ERX/ERR), DDBJ (PRJDB/SAMD/DRA/DRP/DRS/DRX/DRR), GEO (GSE/GSM), SAMN/SAMEA/PRJNA/PRJEB — regex-gated; per-prefix resolution via NCBI eutils (DDBJ/GEO/SRA) or ENA filereport |
| download backend | ftp (default, per-sample) / sratools (prefetch+fasterqdump+pigz) / aspera (ascp era-fasp) — per-sample routing with fallback chain, or forced via --download_method sratools |
| metadata-only | --skip_fastq_download |
| samplesheet shaping | --nf_core_pipeline rnaseq/atacseq/taxprofiler/viralrecon (+ --nf_core_rnaseq_strandedness) |
| metadata | --ena_metadata_fields (29-field default, 5 minimal), --sample_mapping_fields |
| controlled access | --dbgap_key (.ngc/.jwt) |

No --db sra|ena choice exists at this tag (routing is automatic).

## Gap tiers vs the port

**P0**: aspera backend (ascp + era-fasp key); sratools forced mode
(ncbi settings bootstrap + prefetch backoff wrapper + fasterq-dump);
dbGaP controlled-access path; GEO GSE/GSM expansion paths; DDBJ prefix
family; nf_core_pipeline samplesheet shaping (4 variants); metadata-only
mode.

**P1**: none — all services free (SRA/ENA/GEO/DDBJ); dbGaP is
controlled-access (user certificate) not a license.

**P2**: --ena_metadata_fields subsetting, --sample_mapping_fields,
retry/resilience mechanics (error_retry labels, backoff wrappers,
wget -t 5), publish modes.

Dead code at tag: untar module (never included), --force_sratools_download
(deprecated), viralrecon enum value (no-op), GDS resolver path
(unreachable from the input gate).

## Verdict

Compact surface — the ported ENA/fastq-ftp default path leaves the two
alternate backends + GEO/DDBJ ID expansion as the main P0, all
free-software.

## Live evidence update (2026-08-22, night campaign)

Full-line fill branch `full-line-fetchngs` (fb1d538, b6):
- Fixed 3 real bugs on the already-ported M7-M9 paths
- Added the full sratools chain (NCBI_SETTINGS / prefetch /
  fasterq-dump) + forced mode + dbGaP passthrough + aspera rule
- **tx-ubuntu live test PASS**: default FTP path 20/20 rules zero
  failure (ENA md5 checks green); sratools forced mode 9 succeeded +
  2 conditionally skipped; skip-mode + rnaseq samplesheet column
  assertions pass
- Draft-gated: aspera (port 33001 egress untestable on the box) and
  dbGaP (needs a real certificate)

Coverage status: pending merge + stamping; the three live-tested paths
move this repo toward `full-line` once merged (aspera/dbGaP remain
documented DRAFT constraints).

