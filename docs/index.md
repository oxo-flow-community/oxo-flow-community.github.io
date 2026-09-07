---
hide:
  - toc
title: Curated workflows. Ready to run.
---

<div class="ox-hero-split">
<div>
<p class="ox-eyebrow"><span class="ox-eyebrow-light">oxo-flow · community catalog</span><span class="ox-eyebrow-dark">$ catalog --list</span></p>
<h1 class="ox-hero-title">Curated workflows.<br>Ready to run.</h1>
<p class="ox-sub">A community catalog for the oxo-flow engine: verified ports of the pipelines the field already trusts, original workflows built for oxo-flow, and community submissions — classified, rated, and documented, so you can pick the right one and run it with confidence.</p>
<div class="ox-rule"></div>
<a class="ox-cta" href="/pipelines/">Browse the catalog →</a>
</div>
<div>
<div class="ox-term" aria-label="Example oxo-flow session">
<div class="ox-term-head">
<span class="ox-term-dot"></span><span class="ox-term-dot"></span><span class="ox-term-dot"></span>
<span class="ox-term-title">oxo-flow — run</span>
</div>
<div class="ox-term-body">
<div><span class="p">$</span> oxo-flow run main.oxoflow</div>
<div><span class="ok">✔</span> validated — 44 rules · 3 samples · 132 instances</div>
<div><span class="ok">✔</span> run — 132 instances submitted · environments pinned</div>
<div><span class="faint"># classified, rated, and documented in the catalog</span></div>
</div>
</div>
<div class="ox-stats" id="ox-stats" aria-label="Catalog statistics"></div>
</div>
</div>

## How to use this catalog {: .ox-display }

<div class="ox-domains">
<a class="ox-domain-pill" href="/about/curation/"><span class="ox-domain-ico">🎓</span><span class="ox-domain-name">Learn the ratings</span><span class="ox-domain-count">what ✔ ★ ☆ mean</span></a>
<a class="ox-domain-pill" href="/about/selection/"><span class="ox-domain-ico">🧭</span><span class="ox-domain-name">Pick a workflow</span><span class="ox-domain-count">domain &amp; tool guide</span></a>
<a class="ox-domain-pill" href="/about/porting/"><span class="ox-domain-ico">🔁</span><span class="ox-domain-name">Port one yourself</span><span class="ox-domain-count">step-by-step guide</span></a>
</div>

## Browse by domain {: .ox-display }

<div id="ox-domains" class="ox-domains"></div>

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
3. **Copy the command and run.** Each workflow page shows the exact command;
   run it straight from the repository, or from a local clone:

    ```bash
    # straight from the repository — no clone or bundle needed
    oxo-flow run oxo-flow-community/oxo-flow-rnaseq

    # or clone a local copy first (pull keeps the gh: prefix)
    oxo-flow pull gh:oxo-flow-community/oxo-flow-rnaseq
    oxo-flow run oxo-flow-rnaseq/main.oxoflow
    ```

   For `run`, `owner/repository` shorthand works for any public GitHub
   workflow — the `gh:` prefix is optional and `@ref` pins a tag
   (`oxo-flow run gh:owner/repository@v1.0.0`).

New to the engine? Start with the
[oxo-flow documentation](https://github.com/Traitome/oxo-flow), then contribute
a workflow of your own with the [porting guide](about/porting.md).
