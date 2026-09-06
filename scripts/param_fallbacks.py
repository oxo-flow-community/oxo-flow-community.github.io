#!/usr/bin/env python3
"""Generic description fallbacks for config keys the workflow does not
comment on its own.

`oxo-flow info` surfaces the workflow's own `#` comments as parameter
descriptions; keys without one render as "—". The community workflows
mirror nf-core parameter names (their comments say so explicitly:
"upstream --skip_fastqc"), so high-confidence name patterns get a
generic fallback here instead of nothing. The page marks inferred
descriptions — workflow authors should replace them with a real comment
(the source of truth) when they touch the file.

Deliberately conservative: only patterns whose semantics are unambiguous
across the ported workflows qualify. Everything else keeps "—".
"""

from __future__ import annotations

import re


# Tool prefixes whose keys mirror the upstream tool parameter names
# (`--<key>`), verified against the ported workflows' own comments
# ("upstream --fastp_qualified_quality" style).
TOOL_PREFIXES = (
    "adapterremoval_", "angsd_", "arriba_", "ascat_", "bcftools_", "bbnorm_",
    "bbsplit_", "bin_concoct_", "bowtie2_", "bwa_", "callable_sites_",
    "cat_", "cellranger_", "checkm2_", "checkm_", "cnvkit_", "cutadapt_",
    "dada_", "deepvariant_", "delly_", "exomedepth_", "fastp_", "fastqc_",
    "featurecounts_", "freebayes_", "freec_", "freyja_", "gatk_",
    "genomad_", "gtdbtk_", "gunc_", "hisat2_", "ivar_", "kallisto_",
    "kraken2_", "lola_", "majiq_", "maltextract_", "mapdamage_", "maxbin2_",
    "megahit_", "metabat_", "methyl_", "mosdepth_", "mutect2_", "nanopolish_",
    "nextclade_", "pangolin_", "picard_", "pileupcaller_", "pmdtools_",
    "preseq_", "prokka_", "qcat_", "qiime_", "qualimap_", "quast_",
    "rcistarget_", "rsem_", "salmon_", "samtools_", "semibin_", "sequenza_",
    "simpleaf_", "snpeff_", "sortmerna_", "spades_", "spladder_", "star_",
    "strelka_", "svaba_", "tiddit_", "trimgalore_", "umitools_", "vep_",
)


def fallback_description(key: str) -> str | None:
    if re.fullmatch(r"skip_[a-z0-9_]+", key):
        rest = key[5:].replace("_", " ")
        return f"Skip {rest} (upstream --{key})"
    if re.fullmatch(r"run_[a-z0-9_]+", key):
        rest = key[4:].replace("_", " ")
        return f"Enable {rest} (upstream --{key})"
    if re.fullmatch(r"[a-z0-9_]+_db|db_[a-z0-9_]+", key):
        name = key[:-3] if key.endswith("_db") else key[3:]
        return f"Path to the {name.replace('_', ' ')} database (user-provided)"
    if re.fullmatch(r"[a-z0-9_]+_(index|indices)", key):
        name = re.sub(r"_(index|indices)$", "", key).replace("_", " ")
        return f"Path to the prebuilt {name} index (built when empty)"
    if re.fullmatch(r"[a-z0-9_]+_(fasta|fa)", key):
        name = re.sub(r"_(fasta|fa)$", "", key).replace("_", " ")
        return f"Path to the {name} reference FASTA"
    if key in ("out_dir", "output_dir", "result_path", "results_dir"):
        return "Output directory (upstream --outdir)"
    if key == "email":
        return "Notification recipient for pipeline completion (upstream --email; empty = none)"
    if key == "email_on_fail":
        return "Failure-only notification recipient (upstream --email_on_fail; used when email is empty)"
    if key == "hook_url":
        return "Webhook URL for the completion/failure notifications (empty = none)"
    if key == "multiqc_config":
        return "MultiQC config path (upstream --multiqc_config)"
    if key == "genome":
        return "Reference genome build name (upstream --genome, iGenomes key)"
    if key == "metadata_file":
        return "Per-sample metadata table consumed by the metadata binding (issue #227)"
    if re.fullmatch(r"[a-z0-9_]+_version", key):
        name = re.sub(r"_version$", "", key).replace("_", " ")
        return f"Version pin for {name}"
    if key.startswith(TOOL_PREFIXES):
        return f"{key.split('_', 1)[0]} tool parameter (upstream --{key})"
    return None
