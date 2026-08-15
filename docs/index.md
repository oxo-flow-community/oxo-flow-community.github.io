---
hide:
  - toc
---

<p class="ox-eyebrow">oxo-flow · community catalog</p>

# Curated workflows. Ready to run. {: .ox-hero-title }

A community catalog for the oxo-flow engine: verified ports of the pipelines
the field already trusts, original workflows built for oxo-flow, and community
submissions — classified, rated, and documented, so you can pick the right one
and run it with confidence.
{: .ox-sub }

<div class="ox-rule"></div>

<div class="ox-hero">
  <div class="ox-term" aria-label="Example oxo-flow session">
    <div class="ox-term-head">
      <span class="ox-term-dot"></span><span class="ox-term-dot"></span><span class="ox-term-dot"></span>
      <span class="ox-term-title">oxo-flow — dry-run</span>
    </div>
    <div class="ox-term-body">
      <div><span class="p">$</span> oxo-flow run workflow/rnaseq.toml --config config/illumina.toml</div>
      <div><span class="ok">✔</span> validated — 44 rules · 3 samples · 132 instances</div>
      <div><span class="ok">✔</span> dry-run — ready to run · containers pinned</div>
      <div><span class="faint"># classified, rated, and documented in the catalog</span></div>
    </div>
  </div>
</div>

<div class="ox-stats" id="ox-stats" aria-label="Catalog statistics"></div>

## Start here {: .ox-display }

<div id="ox-featured" class="ox-cards"></div>

<p class="ox-more"><a class="md-button md-button--primary" href="/pipelines/">Browse the full catalog</a></p>

## Where workflows come from

<div class="ox-pillars">
  <div class="ox-pillar">
    <span class="icon">⇄</span>
    <h3>Official ports</h3>
    <p>Migrations of widely adopted Nextflow and Snakemake pipelines — same
    tools, same versions, same commands — verified rule-by-rule against the
    source and rated <em>Verified</em>.</p>
  </div>
  <div class="ox-pillar">
    <span class="icon">✦</span>
    <h3>Original workflows</h3>
    <p>Pipelines designed for oxo-flow from the start, by the community team
    or anyone who opens a repository and asks for it to be listed.</p>
  </div>
  <div class="ox-pillar">
    <span class="icon">♺</span>
    <h3>Community listings</h3>
    <p>Workflows hosted anywhere on GitHub can join the catalog via pull
    request — the listing links to your repository, it does not move it.</p>
  </div>
</div>

See [Curation &amp; ratings](about/curation.md) for the classification scheme,
the rating criteria, and how to get a workflow listed.

## How to run a workflow

1. **Find it.** Search the catalog by domain, tool, or source. Every entry
   records its rating, origin, tools, and pinned versions.
2. **Read the notes.** Each workflow page documents installation, usage,
   scope, and — for ports — a per-rule fidelity table against the source.
3. **Copy the command and run.**

    ```bash
    oxo-flow run workflow/rnaseq.toml --config config/illumina.toml
    ```

New to the engine? Start with the
[oxo-flow documentation](https://github.com/Traitome/oxo-flow), then contribute
a workflow of your own with the [porting guide](about/porting.md).
