---
title: "TCGA bulk RNA-seq TCR/BCR immune repertoire profiling (MiXCR + TRUST4)"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-immune-repertoire</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>TCGA bulk RNA-seq TCR/BCR immune repertoire profiling (MiXCR + TRUST4)</h1>
<div class="ox-page-badges"><span class="ox-badge ">☆ Community</span> <span class="ox-badge ox-badge--origin">Original</span> <span class="ox-badge ox-badge--native"><span class="dot" aria-hidden="true"></span>oxo-flow native</span><span class=ox-tag-sep></span><span class="ox-tag">immune-repertoire</span><span class="ox-tag">TCR</span><span class="ox-tag">BCR</span><span class="ox-tag">CDR3</span><span class="ox-tag">MiXCR</span><span class="ox-tag">TRUST4</span><span class="ox-tag">TCGA</span><span class="ox-tag">RNA-seq</span><span class="ox-tag">AIRR</span><span class="ox-tag">clonotypes</span></div>
<p class="ox-desc">Extracts TCR/BCR clonotypes from bulk RNA-seq BAMs (TCGA GDC harmonized) with MiXCR and TRUST4, normalizes both tools&#x27; outputs into one 14-column unified clonotype schema, and reports per-sample repertoire metrics; designed for Slurm clusters (shard layout for production cohorts).</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#preview-the-plan">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-immune-repertoire" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow dry-run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">☆ Community</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">—</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v"><span title="4 CPUs / 48 GB per mixcr rule, 4 CPUs / 24 GB per trust4 rule; production runs 5 rules per node (20 CPUs, &lt;=48 GB each)">4 CPUs / 48 GB per mixcr rule, 4 CPUs / 24 GB per trust4 rule…</span></span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--native"><span class="dot" aria-hidden="true"></span>oxo-flow native</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Original</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">immunology</span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-11-16</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">MiXCR</span><span class="tchip">TRUST4</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-immune-repertoire</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#preview-the-plan">Usage</a></nav>


## Preview the plan

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-immune-repertoire -run
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-immune-repertoire` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-immune-repertoire@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-immune-repertoire` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Data-gated: MiXCR/TRUST4 need BAM inputs and the TRUST4 reference FASTAs (hg38_bcrtcr.fa, human_IMGT+C.fa, not committed). Dry-run works against the committed manifests; the shard variant demonstrates the production layout.

## Installation

**Engine.** oxo-flow >= 0.30

**Toolchain.** pixi (pixi.toml) — pinned MiXCR/TRUST4 and dependencies; TRUST4 reference FASTAs (hg38_bcrtcr.fa, human_IMGT+C.fa) are provisioned outside the repo (not committed)

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-immune-repertoire
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-immune-repertoire
```

## Links

- Repository: [oxo-flow-immune-repertoire](https://github.com/oxo-flow-community/oxo-flow-immune-repertoire)
