---
hide:
  - toc
---

# Pipeline catalog

Every workflow in the catalog. Ratings are an [evidence ladder](../about/curation.md):
**✔ live-tested** end-to-end on real data, **★ verified** (fidelity-checked,
passes `validate` + `dry-run` in CI), **◆ dry-run verified** (maintained like
★ but no full end-to-end run yet), **☆ community** (meets listing
requirements, maintained by its authors). Filter by domain, origin, or source
engine; search by name, tool, tag, or description.

<div class="ox-filter">
  <input type="search" id="ox-search" placeholder="search: rna, star, variant, bam…" aria-label="Search workflows">
</div>
<div class="ox-filter" id="ox-chips" role="group" aria-label="Workflow filters"></div>
<p class="ox-mono" id="ox-count" role="status"></p>
<div id="ox-all" class="ox-cards"><noscript><p class="ox-empty">The interactive catalog needs JavaScript — the workflows and their run notes are linked from the navigation.</p></noscript></div>
<div id="ox-empty" class="ox-empty" hidden>
  no workflows match — clear a filter to widen the search
</div>
