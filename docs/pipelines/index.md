---
hide:
  - toc
---

# Pipeline catalog

Every workflow in the catalog. Ratings are an [evidence ladder](../about/curation.md):
**✔ live-tested** end-to-end on real data, **★ verified** (fidelity-checked,
passes `validate` + `dry-run` in CI), **☆ community** (meets listing
requirements, maintained by its authors). Filter by domain, origin, or source
engine; search by name, tool, or tag.

<div class="ox-filter">
  <input type="search" id="ox-search" placeholder="search: rna, star, variant, bam…" aria-label="Search workflows">
</div>
<div class="ox-filter" id="ox-chips" role="group" aria-label="Workflow filters"></div>
<p class="ox-mono" id="ox-count" aria-live="polite"></p>
<div id="ox-all" class="ox-cards"></div>
<div id="ox-empty" class="ox-empty" hidden>
  no workflows match — clear a filter to widen the search
</div>
