---
hide:
  - toc
---

<p class="ox-eyebrow">oxo-flow-community · workflow catalog</p>

# Faithful ports. One engine. {: .ox-hero-title }

The community catalog of oxo-flow workflows: the most-used nf-core and Snakemake
pipelines, ported rule-for-rule — same tools, same versions, same commands,
re-expressed as one TOML file. Search the catalog, read the run notes, copy the
command. {: .ox-sub }

<div class="ox-hero">
  <div class="ox-term" aria-label="Example oxo-flow session">
    <div class="ox-term-head">
      <span class="ox-term-dot"></span><span class="ox-term-dot"></span><span class="ox-term-dot"></span>
      <span class="ox-term-title">oxo-flow — dry-run</span>
    </div>
    <div class="ox-term-body">
      <div><span class="p">$</span> oxo-flow run workflow/rnaseq.toml --config config/illumina.toml</div>
      <div><span class="ok">✔</span> validated — 14 rules · 3 samples · 42 instances</div>
      <div><span class="ok">✔</span> dry-run — 42/42 ready · 8 containers pinned</div>
      <div><span class="faint"># ported from nf-core/rnaseq 3.26.0 — same tools, same versions</span></div>
    </div>
  </div>
  <div class="ox-dag-wrap">
    <svg viewBox="0 0 800 250" role="img"
         aria-label="A workflow DAG: three samples fan out through trim and align into quantification and multiqc">
      <defs>
        <linearGradient id="oxg" x1="0" y1="250" x2="800" y2="0" gradientUnits="userSpaceOnUse">
          <stop offset="0" stop-color="#29D0FF"/>
          <stop offset="1" stop-color="#2EE6A8"/>
        </linearGradient>
      </defs>
      <g class="ox-dag">
        <line class="edge" x1="94" y1="45" x2="232" y2="113"/>
        <line class="edge" x1="94" y1="125" x2="232" y2="125"/>
        <line class="edge" x1="94" y1="205" x2="232" y2="137"/>
        <line class="edge" x1="268" y1="125" x2="422" y2="125"/>
        <line class="edge" x1="458" y1="125" x2="606" y2="79"/>
        <line class="edge" x1="458" y1="125" x2="606" y2="171"/>
        <line class="edge" x1="634" y1="75" x2="727" y2="114"/>
        <line class="edge" x1="634" y1="175" x2="727" y2="136"/>
        <circle class="node" cx="80" cy="45" r="14" style="animation-delay:0s"/>
        <circle class="node" cx="80" cy="125" r="14" style="animation-delay:.3s"/>
        <circle class="node" cx="80" cy="205" r="14" style="animation-delay:.6s"/>
        <circle class="node" cx="250" cy="125" r="18" style="animation-delay:.15s"/>
        <circle class="node" cx="440" cy="125" r="18" style="animation-delay:.45s"/>
        <circle class="node" cx="620" cy="75" r="14" style="animation-delay:.9s"/>
        <circle class="node" cx="620" cy="175" r="14" style="animation-delay:1.05s"/>
        <circle class="node" cx="745" cy="125" r="18" style="animation-delay:.75s"/>
        <text class="label" x="80" y="240">samples ×3</text>
        <text class="label" x="250" y="158">trim</text>
        <text class="label" x="440" y="158">align</text>
        <text class="label" x="620" y="208">quant ×2</text>
        <text class="label" x="745" y="158">multiqc</text>
      </g>
    </svg>
  </div>
</div>

<div class="ox-stats" id="ox-stats" aria-label="Catalog statistics"></div>

## Start here {: .ox-display }

<div id="ox-featured" class="ox-cards"></div>

<p class="ox-more"><a class="md-button md-button--primary" href="pipelines/">Browse the full catalog</a></p>

## How it works

1. **Find your workflow.** Search the catalog by domain, tool, or source engine.
   Every entry records its upstream pipeline, pinned version, and tool list.
2. **Read the run notes.** Each workflow page documents what was ported, what was
   excluded, and a per-rule fidelity table against the source.
3. **Copy the command and run.**

    ```bash
    oxo-flow run workflow/rnaseq.toml --config config/illumina.toml
    ```

New to oxo-flow? Start with the
[engine documentation](https://github.com/Traitome/oxo-flow) — then come back and
port your favorite workflow with the [porting guide](about/porting.md).
