# Site Beautify v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the A+V2+W2+P2+D2 design system on the oxo-flow-community catalog site (split hero, evidence-first cards, At-a-glance detail panels, instrument dark mode, warning-free strict build).

**Architecture:** One CSS file (extra.css) carries all tokens and components; index.md restructures the home hero; catalog.js rebuilds cardHTML to the W2 structure; generate.py restructures the detail-page header and regenerates all 24 pages + pipelines-data.js from data/pipelines.json. No new dependencies, no framework changes.

**Tech Stack:** MkDocs Material (mkdocs build --strict in CI), vanilla JS, Python 3 stdlib only (scripts/generate.py), CSS custom properties.

**Spec:** `.superpowers/specs/2026-09-05-site-beautify-design.md` (the plan argues from the spec; read both)

**Repo:** /Users/wsx/Documents/GitHub/oxo-community/site, branch `feat/site-v2-beautify` (already created, spec committed as ee9cd46). Work in this repo, NOT the oxo-flow engine repo.

## Global Constraints

- Light tokens fixed (A · 精修现有): bg #f7faf8, ink #17211c, ink-2 #3f5047, muted #6b7d73, faint #97a69e, edge #dfe8e3, brand #0e7a5f, ok #0F9D6E, grad `linear-gradient(90deg, #0b93b8, #0e7a5f)`.
- Dark (slate) scheme is REPLACED by D2 · 仪器暗色: bg #0a0f0d, panel #101915, panel-2 #16211b, edge #1d2a24, ink #eef7f2, ink-2 #8ca096, muted/faint #5e6f65, brand/ok #34d399, cyan #22b8d4, brand-deep #6ee7b7, brand-soft #0f2a1e, term-bg #0e1613, cmd-bg #0c1310, on-brand #04120c, grad `linear-gradient(90deg, #22b8d4, #34d399)`.
- Evidence green stays green in BOTH schemes (light #0F9D6E, dark #34d399) — the only categorical marks remain the two engine dots (nf #0c8a5d light / sn #1a64b8).
- Cards show PLAIN rating text ("✔ Live-tested", no coverage suffix). Detail pages keep the suffix ("· full-line" / "· default-path").
- CI gate (pr.yml): `python3 scripts/generate.py` must be drift-free (`git diff --exit-code -- docs/ data/ scripts/ ':!docs/assets/dag'`) and `mkdocs build --strict` must pass with ZERO warnings.
- The committed `site/` mirror must be updated in the same commit as docs/ changes; 3 stale clindet SVGs in site/assets/dag are excluded (delete them, don't commit them).
- Copy rules: site copy is English; commit messages per repo convention (`<type>: <desc>`, no co-author trailer); one commit per task.
- index.md and mkdocs.yml edits have historically been reverted by the user's editor — after editing, `git diff` to confirm the change is present before committing.
- catalog.js has no test framework: verification = build + grep on built output + final browser pass (Task 6).
- Avoid nested double quotes inside compound bash commands (keep commands simple; prefer dedicated tools).

---

### Task 1: Design-system CSS — extra.css (tokens + all components)

**Files:**
- Modify: `docs/stylesheets/extra.css` (full file; edit anchors below are against the current committed version)

**Interfaces:**
- Consumes: spec §设计令牌 / §组件规格 (all values verbatim).
- Produces: CSS classes consumed by Tasks 2–4: `.ox-hero-split`, `.ox-eyebrow-light/.ox-eyebrow-dark`, `.ox-cta`, `.ox-card.live-card`, `.tchip`, `.ox-card .foot`, `.ox-crumb`, `.ox-detail-cols`, `.ox-glance`, `.ox-glance-title`, `.ox-kv`, plus tokens `--term-bg`, `--cmd-bg`, `--on-brand`.

- [ ] **Step 1: Add the three light-scheme tokens**

In `:root { ... }`, after the `--grad` line:

```css
  --grad: linear-gradient(90deg, #0b93b8, #0e7a5f);
  --term-bg: #ffffff;
  --cmd-bg: #ffffff;
  --on-brand: #ffffff;
}
```

- [ ] **Step 2: Replace the slate token block with D2 values**

Replace the whole `[data-md-color-scheme="slate"] { ... }` token block (currently `--bg: #0c1210;` … `--grad: linear-gradient(90deg, #35c2e0, #2bb58a);`) with:

```css
[data-md-color-scheme="slate"] {
  --bg: #0a0f0d;
  --panel: #101915;
  --panel-2: #16211b;
  --edge: #1d2a24;
  --edge-strong: #2a3a32;
  --ink: #eef7f2;
  --ink-2: #8ca096;
  --muted: #5e6f65;
  --faint: #5e6f65;
  --brand: #34d399;
  --brand-deep: #6ee7b7;
  --brand-soft: #0f2a1e;
  --cyan: #22b8d4;
  --nf: #34d399;
  --sn: #2e86d9;
  --star: #e5a44b;
  --code-bg: #0c1310;
  --term-bg: #0e1613;
  --cmd-bg: #0c1310;
  --on-brand: #04120c;
  --ok: #34d399;
  --shadow: 0 1px 2px rgb(0 0 0 / 0.35);
  --shadow-hover: 0 2px 6px rgb(0 0 0 / 0.45), 0 12px 30px rgb(0 0 0 / 0.4);
  --grad: linear-gradient(90deg, #22b8d4, #34d399);
}
```

- [ ] **Step 3: Update the slate primary block**

In `[data-md-color-scheme="slate"] { --md-primary-fg-color: … }`, change both `--md-primary-bg-color*` values from `#0c1210` to `#0a0f0d`.

- [ ] **Step 4: Nav restyle (brand + item colors)**

After the `.md-tabs__link--active, .md-tabs__link { ... }` block, insert:

```css
.md-header__topic:first-child {
  color: var(--brand);
  font-weight: 600;
}
```

Replace the existing rule

```css
.md-tabs__link--active,
.md-tabs__link {
  color: var(--ink);
}
```

with:

```css
.md-tabs__link--active { color: var(--ink); }
.md-tabs__link { color: var(--muted); }
```

(Active items keep ink in both schemes; inactive items go muted — light #6b7d73, dark #5e6f65 — matching the A and D2 mockups.)

- [ ] **Step 5: Hero V2 split (replaces the old `.ox-hero` rules)**

Replace the three rules `.ox-hero h1 { ... }`, `.ox-hero .ox-sub { ... }`, `.ox-hero .ox-rule { ... }` (currently `font-size: clamp(2.1rem…`, `max-width: 47rem`, `width: 88px`) with:

```css
/* ---- Hero (V2 split) ---- */
.ox-hero-split {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 1.6rem;
  align-items: center;
  margin: 1.2rem 0 2.4rem;
}

.ox-eyebrow-dark { display: none; }

.ox-hero-split h1 {
  font-size: clamp(2.1rem, 4.5vw, 3.2rem);
  line-height: 1.06;
  margin: 0 0 1rem;
  color: var(--ink);
}

.ox-hero-split .ox-sub {
  font-size: 1.06rem;
  color: var(--ink-2);
  max-width: 32rem;
  margin: 0 0 1.4rem;
  line-height: 1.65;
}

.ox-hero-split .ox-rule {
  height: 3px;
  width: 58px;
  border-radius: 2px;
  background: var(--grad);
  margin: 0 0 1.4rem;
}

.ox-cta {
  display: inline-block;
  background: var(--brand);
  color: var(--on-brand);
  font-weight: 600;
  font-size: 0.92rem;
  padding: 0.55rem 1.4rem;
  border-radius: 999px;
  text-decoration: none;
}

.ox-cta:hover {
  background: var(--brand-deep);
  color: var(--on-brand);
}

.ox-hero-split .ox-term {
  margin: 0 0 0.8rem;
  max-width: none;
}

.ox-hero-split .ox-stats {
  margin: 0;
}
```

- [ ] **Step 6: Card W2 (top evidence line + live-card variant)**

In the `.ox-card { ... }` rule, change `border-radius: 12px` to `10px` and add `border-top: 3px solid var(--edge);` after the `border:` line. Then immediately after the `.ox-card` rule block, insert:

```css
/* Evidence-first: live-tested cards carry the green top line (W2) */
.ox-card.live-card { border-top-color: var(--ok); }
```

- [ ] **Step 7: Card title color**

In `.ox-card .title { ... }`, change `color: var(--ink-2);` to `color: var(--ink);`.

- [ ] **Step 8: Tool chips**

After the `.ox-card .meta { ... }` block, insert:

```css
.tchip {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.68rem;
  color: var(--ink-2);
  background: var(--panel-2);
  border-radius: 5px;
  padding: 0.14rem 0.4rem;
  white-space: nowrap;
}
```

- [ ] **Step 9: Command strip becomes the card's white bottom anchor**

In `.ox-card .cmd { ... }`, change `background: var(--code-bg);` to `background: var(--cmd-bg);` and `border-radius: 8px;` to `border-radius: 6px;`.

- [ ] **Step 10: Card foot row (rating left, engine dot right)**

Before the `.ox-card .links { ... }` rule, insert:

```css
.ox-card .foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-top: auto;
  padding-top: 0.55rem;
  border-top: 1px solid var(--panel-2);
}
```

- [ ] **Step 11: Pillar + DAG-card radius 10px**

In `.ox-pillar` and `.ox-dag-card`, change `border-radius: 12px;` to `border-radius: 10px;` (two places).

- [ ] **Step 12: Detail header P2 (crumb + columns + At-a-glance panel)**

Insert this whole section before `/* ---- Focus + reduced motion ---- */`:

```css
/* ---- Detail-page header (P2) ---- */
.ox-crumb {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  color: var(--faint);
  margin: 0 0 0.8rem;
}

.ox-crumb a {
  color: var(--brand);
  text-decoration: none;
}

.ox-crumb a:hover { text-decoration: underline; }

.ox-detail-cols {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.2rem;
  align-items: start;
  margin: 0 0 1.4rem;
}

.ox-detail-cols h1 {
  font-size: 1.65rem;
  margin: 0 0 0.2rem;
}

.ox-detail-cols .ox-page-badges {
  margin: 0.5rem 0 0.9rem;
}

.ox-detail-cols p {
  line-height: 1.55;
}

.ox-glance {
  background: var(--panel);
  border: 1px solid var(--edge);
  border-radius: 10px;
  padding: 0.75rem 0.9rem;
  box-shadow: var(--shadow);
}

.ox-glance-title {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--faint);
  margin-bottom: 0.4rem;
}

.ox-kv {
  display: flex;
  justify-content: space-between;
  gap: 0.8rem;
  padding: 0.3rem 0;
  border-bottom: 1px solid var(--panel-2);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
}

.ox-kv:last-of-type { border-bottom: none; }

.ox-kv .k { color: var(--faint); }

.ox-kv .v {
  font-weight: 600;
  color: var(--ink);
  text-align: right;
}

.ox-kv .v.live { color: var(--ok); }

.ox-kv .v a { color: var(--brand); }

.ox-kv .v code { background: transparent; padding: 0; }

.ox-glance .cmd {
  display: block;
  margin-top: 0.6rem;
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  line-height: 1.4;
  color: var(--ink-2);
  background: var(--cmd-bg);
  border: 1px solid var(--edge);
  border-radius: 6px;
  padding: 0.45rem 0.6rem;
  overflow-x: auto;
  white-space: nowrap;
}
```

- [ ] **Step 13: Filter bar minimal polish**

In `.ox-chip { ... }`, add `user-select: none;` after `cursor: pointer;`. (Everything else — focus ring, pressed state — is already aligned with the card language.)

- [ ] **Step 14: Footer mono restyle**

After the `.md-tabs` / `.md-footer` rules, insert:

```css
.md-footer {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.68rem;
}

.md-footer a {
  color: var(--brand);
  text-decoration: none;
}

.md-footer a:hover { text-decoration: underline; }
```

- [ ] **Step 15: Dark-chip pressed text color**

In `[data-md-color-scheme="slate"] .ox-chip[aria-pressed="true"]`, change `color: #0c1210;` to `color: #04120c;`.

- [ ] **Step 16: Dark scheme (D2 instrument) component overrides**

Insert before `/* ---- Focus + reduced motion ---- */`:

```css
/* ---- Dark scheme (D2 · instrument) component overrides ---- */
[data-md-color-scheme="slate"] .ox-eyebrow-light { display: none; }
[data-md-color-scheme="slate"] .ox-eyebrow-dark { display: block; }

[data-md-color-scheme="slate"] .ox-term {
  box-shadow: 0 0 22px rgb(52 211 153 / 0.07);
}

[data-md-color-scheme="slate"] .ox-term-head {
  background: var(--term-bg);
}

[data-md-color-scheme="slate"] .ox-term-dot {
  background: #3ddc84;
  box-shadow: 0 0 5px #3ddc8488;
}

[data-md-color-scheme="slate"] .ox-term-body .p,
[data-md-color-scheme="slate"] .ox-term-body .ok {
  color: var(--brand);
  text-shadow: 0 0 7px rgb(52 211 153 / 0.33);
}

[data-md-color-scheme="slate"] .ox-badge {
  background: var(--cmd-bg);
  text-transform: lowercase;
}

[data-md-color-scheme="slate"] .ox-badge--live {
  color: var(--ok);
  border-color: #1f4d38;
  background: #0f2a1e;
}
```

- [ ] **Step 17: Mobile stacking**

In the existing `@media (max-width: 720px)` block, append:

```css
  .ox-hero-split { grid-template-columns: 1fr; }
  .ox-detail-cols { grid-template-columns: 1fr; }
```

- [ ] **Step 18: Build sanity check**

Run: `mkdocs build` (non-strict is fine here)
Expected: build succeeds. Up to 3 pre-existing warnings may appear (curation.md link, porting.md link, chipseq anchor) — they are fixed in Tasks 4–5 and must be gone by Task 6. No NEW warnings.

- [ ] **Step 19: Commit**

```bash
git add docs/stylesheets/extra.css
git commit -m "style: design system v2 — D2 instrument dark tokens, V2 hero, W2 cards, P2 glance panel"
```

---

### Task 2: Home hero V2 split — index.md

**Files:**
- Modify: `docs/index.md` (rewrite the hero region, lines 1–39; keep everything from `## Start here` down unchanged)

**Interfaces:**
- Consumes: `.ox-hero-split`, `.ox-eyebrow-light/.ox-eyebrow-dark`, `.ox-cta`, `.ox-term`, `.ox-stats` (Task 1).
- Produces: `id="ox-stats"` stays at the same element so catalog.js renderStats keeps working; `id="ox-featured"` unchanged.

- [ ] **Step 1: Rewrite the hero region**

Replace lines 1–33 (frontmatter through the closing `</div>` of `.ox-hero`) with:

```markdown
---
hide:
  - toc
---

<div class="ox-hero-split">
  <div markdown="1">

<p class="ox-eyebrow"><span class="ox-eyebrow-light">oxo-flow · community catalog</span><span class="ox-eyebrow-dark">$ catalog --list</span></p>

# Curated workflows.<br>Ready to run. {: .ox-hero-title }

A community catalog for the oxo-flow engine: verified ports of the pipelines
the field already trusts, original workflows built for oxo-flow, and community
submissions — classified, rated, and documented, so you can pick the right one
and run it with confidence.
{: .ox-sub }

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
```

The old `.ox-hero` wrapper div (lines 18–31) and the old standalone eyebrow/h1/sub/rule lines (6–16) are consumed by this replacement. `## Start here` and everything below is untouched.

- [ ] **Step 2: Build and verify structure**

Run: `mkdocs build` then `grep -c "ox-hero-split" site/index.html`
Expected: `1` (and `grep -c "ox-cta" site/index.html` → `1`; `grep -c "catalog --list" site/index.html` → `1`).

- [ ] **Step 3: Verify the edit survived (revert watch)**

Run: `git diff -- docs/index.md | head -40` — the new hero must be present in the diff before committing.

- [ ] **Step 4: Commit**

```bash
git add docs/index.md
git commit -m "feat: V2 split hero on the home page"
```

---

### Task 3: W2 evidence-first cards — catalog.js

**Files:**
- Modify: `docs/javascripts/catalog.js` (cardHTML restructure + dead-ORIGIN removal)

**Interfaces:**
- Consumes: `.tchip`, `.ox-card .foot`, `.ox-card.live-card` (Task 1); data fields `p.rating`, `p.engine`, `p.origin`, `p.domain`, `p.rule_count`, `p.compute`, `p.tools`, `p.quickstart`, `p.repo_url` (unchanged).
- Produces: no signature changes; renderStats/renderFeatured/renderCatalog untouched except cardHTML output.

- [ ] **Step 1: Restructure cardHTML**

Replace the whole `function cardHTML(p) { … }` body (from `const star = …` through the closing `</article>;\`` backtick) with:

```js
  function cardHTML(p) {
    const star = p.rating === "live-verified"
      ? '<span class="ox-badge ox-badge--live">✔ Live-tested</span>'
      : p.rating === "verified"
        ? '<span class="ox-badge ox-badge--star">★ Verified</span>'
        : '<span class="ox-badge">☆ Community</span>';
    const engBadge = p.engine === "nextflow"
      ? '<span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core</span>'
      : p.engine === "snakemake"
        ? '<span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake</span>'
        : "";
    const cmd = p.quickstart || "oxo-flow run main.oxoflow";
    // ox-badge--compute: long compute strings wrap instead of overflowing the card
    const compute = p.compute
      ? `<span class="ox-badge ox-badge--compute" title="Peak compute per rule">⚙ ${esc(p.compute)}</span>`
      : "";
    const tools = (p.tools || []).slice(0, 3)
      .map((t) => `<span class="tchip">${esc(t)}</span>`).join("");
    const cls = p.rating === "live-verified" ? "ox-card live-card" : "ox-card";
    return `<article class="${cls}">
      <div class="row">
        <a class="name" href="/pipelines/${esc(p.name)}/">${esc(p.name)}</a>
        <span class="ox-badge">${esc(p.domain)}</span>
      </div>
      <p class="title">${esc(p.title)}</p>
      <div class="meta">
        <span class="ox-badge">${Number(p.rule_count) || 0} rules</span>
        ${compute}
        ${tools}
      </div>
      <div class="foot">
        ${star}
        ${engBadge}
      </div>
      <p class="cmd">$ ${esc(cmd)}</p>
      <div class="links">
        <a href="/pipelines/${esc(p.name)}/">Run notes</a>
        <a href="${esc(p.repo_url)}" rel="noopener">GitHub ↗</a>
      </div>
    </article>`;
  }
```

Notes: the origin badge and the old `.tools` separator line are dropped from cards (origin lives on detail pages; tools become 3 tchips). Rating text is plain (no coverage suffix — detail pages keep it, Task 4).

- [ ] **Step 2: Add the compute-badge wrap rule to extra.css**

After the `.ox-badge--origin { border-style: dashed; }` rule, insert:

```css
/* Long compute strings ("up to 12 CPUs / 72 GB per rule (bwa_mem, …)") wrap
   inside the card instead of overflowing it */
.ox-badge--compute {
  white-space: normal;
  line-height: 1.35;
}
```

- [ ] **Step 3: Remove the now-dead ORIGIN map**

Delete the block:

```js
  const ORIGIN = {
    port: "⇄ Official port",
    original: "✦ Original",
    curated: "♺ Community listing",
  };
```

(renderCatalog's `ORIGIN_LABEL` is separate and stays.)

- [ ] **Step 4: Verify**

Run: `mkdocs build` then `grep -c "ox-card live-card" site/javascripts/catalog.js` (expect `1` — the class is composed in JS so grep the source), `grep -c "tchip" site/javascripts/catalog.js` (expect `2`), `grep -c "ORIGIN = {" site/javascripts/catalog.js` (expect `0`), `grep -c "ox-badge--compute" site/javascripts/catalog.js` (expect `1`) and `grep -c "ox-badge--compute" site/stylesheets/extra.css` (expect `1`). Also confirm the built `site/index.html` still carries the stats containers.

- [ ] **Step 5: Commit**

```bash
git add docs/javascripts/catalog.js docs/stylesheets/extra.css
git commit -m "feat: W2 evidence-first cards — green top line, tool chips, foot badges, wrapping compute badge"
```

---

### Task 4: P2 detail header — generate.py + chipseq anchor fix + regeneration

**Files:**
- Modify: `scripts/generate.py` (make_page header restructure; delete meta_table; add glance_panel + _esc)
- Modify: `data/pipelines.json` (one substring: chipseq fidelity anchor)
- Regenerate: `docs/pipelines/*.md` (24 files) + `docs/javascripts/pipelines-data.js`

**Interfaces:**
- Consumes: `.ox-crumb`, `.ox-detail-cols`, `.ox-glance`, `.ox-glance-title`, `.ox-kv`, `.ox-glance .cmd`, `.ox-page-badges` (Task 1); data fields as in current meta_table.
- Produces: every generated page opens with `crumb → cols(left: h1/badges/description | right: glance panel with kv rows + quickstart cmd)`; `meta_table()` no longer exists anywhere.

- [ ] **Step 1: Add the escape helper**

In generate.py, after `import json` add `import html`, and after `def load_configs() …` add:

```python
def _esc(value) -> str:
    """HTML-escape a registry value for raw-HTML panel output."""
    return html.escape(str(value), quote=True)
```

- [ ] **Step 2: Replace meta_table with glance_panel**

Replace the whole `def meta_table(p: dict) -> str: …` function with:

```python
def glance_panel(p: dict) -> str:
    """P2 detail header — the right-hand 'At a glance' panel (was meta_table).

    Same rows, same data as the old table; rating keeps the coverage
    suffix here (cards drop it — see spec §Rating 后缀对账). Links and
    code are emitted as raw HTML because the panel is not markdown-parsed.
    """
    rating = p.get("rating", "community")
    rating_text = {
        "live-verified": "✔ Live-tested",
        "verified": "★ Verified",
        "community": "☆ Community",
    }.get(rating, "☆ Community")
    coverage = p.get("coverage", "")
    if coverage in ("full-line", "default-path"):
        rating_text += f" · {coverage}"
    origin = {
        "port": "⇄ Official port",
        "original": "✦ Original",
        "curated": "♺ Community listing",
    }.get(p.get("origin"), "♺ Community listing")
    eng = {
        "nextflow": '<span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span>',
        "snakemake": '<span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span>',
    }.get(p.get("engine"), "")
    rows = [
        ("Rating", rating_text, "live"),
        ("Rules", str(p.get("rule_count", "—")), ""),
        ("Compute", p.get("compute", "—"), ""),
        ("Engine", eng or "—", ""),
        ("Origin", origin, ""),
        ("Domain", p.get("domain", ""), ""),
    ]
    src = p.get("source")
    if src:
        rows += [
            ("Source", f'<a href="{_esc(src["url"])}">{_esc(src["repo"])}</a>', ""),
            ("Pinned version", f'<code>{_esc(src.get("tag") or src.get("sha", ""))}</code>', ""),
        ]
    rows += [
        ("Ported", p.get("created", "2026-08-15"), ""),
        ("License", p.get("license", "Apache-2.0"), ""),
    ]
    kv = "\n".join(
        f'<div class="ox-kv"><span class="k">{k}</span>'
        f'<span class="v{(" " + cls) if cls else ""}">{v}</span></div>'
        for k, v, cls in rows
    )
    return (
        '<div class="ox-glance">\n'
        '<div class="ox-glance-title">At a glance</div>\n'
        f"{kv}\n"
        f'<p class="cmd">$ {_esc(p["quickstart"])}</p>\n'
        "</div>"
    )
```

- [ ] **Step 3: Restructure make_page's header**

In `def make_page(p: dict, configs: dict) -> str:`, replace the parts-list head — from `parts = [` through the `"```"` quickstart line — with:

```python
    parts = [
        f'<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>{_esc(p["name"])}</span></div>',
        # NOTE (Task 2 live-finding): md_in_html only processes markdown="1"
        # blocks at the markdown root level — a nested attributed div inside
        # an unattributed raw-HTML block is ignored. The OUTER grid div must
        # carry the attribute too, or the h1/badges/description stay raw text.
        '<div class="ox-detail-cols" markdown="1">',
        '<div markdown="1">',
        "",
        f"# {p['title']}",
        "",
        badges(p),
        "",
        p.get("description", ""),
        "",
        "</div>",
        "<div>",
        "",
        glance_panel(p),
        "",
        "</div>",
        "</div>",
        "",
        "## Run it" if "dry-run" not in p["quickstart"] else "## Preview the plan",
        "",
        "```bash",
        p["quickstart"],
        "```",
    ]
```

(The rest of make_page — quickstart_note, install_section, params, dag, scope, fidelity, links — is unchanged. `meta_table(p)` must no longer be referenced.)

- [ ] **Step 4: Fix the chipseq broken anchor in the registry**

In `data/pipelines.json`, replace the substring `[Multi-antibody runs](#multi-antibody-runs)` with `[Multi-antibody runs](#known-divergences)` (exactly one occurrence — the fidelity_md of oxo-flow-chipseq; the `### Known divergences` heading exists later in the same fidelity_md, so the anchor resolves).

- [ ] **Step 5: Regenerate**

Run: `python3 scripts/generate.py`
Expected: `generated: 24 pages + pipelines-data.js` (or current registry count), no errors.

- [ ] **Step 6: Verify the new header shape**

Run: `grep -c "ox-detail-cols" docs/pipelines/oxo-flow-rnaseq.md` (expect `1`), `grep -c "At a glance" docs/pipelines/oxo-flow-rnaseq.md` (expect `1`), `grep -c "ox-kv" docs/pipelines/oxo-flow-rnaseq.md` (expect `10`), `grep -c "meta_table" scripts/generate.py` (expect `0`).

- [ ] **Step 7: Build (still non-strict) and drift check**

Run: `mkdocs build` then `git diff --exit-code -- docs/ data/ scripts/ ':!docs/assets/dag'`
Expected: build succeeds (chipseq warning is now GONE — the anchor resolves; curation/porting warnings remain for Task 5). The drift check shows only the intended data/scripts/docs diffs.

- [ ] **Step 8: Commit**

```bash
git add scripts/generate.py data/pipelines.json docs/pipelines/ docs/javascripts/pipelines-data.js
git commit -m "feat: P2 at-a-glance detail header + fix chipseq multi-antibody anchor"
```

---

### Task 5: Remaining build warnings + footer links

**Files:**
- Modify: `docs/about/porting.md` (fence nesting fix)
- Modify: `docs/about/curation.md` (line 11 link)
- Modify: `mkdocs.yml` (copyright line)

**Interfaces:**
- Consumes: `.md-footer` mono styling (Task 1); the D2/light token system.
- Produces: `mkdocs build --strict` output with zero warnings (the strict gate is the deliverable).

- [ ] **Step 1: Fix the broken fence nesting in porting.md**

Root cause: the ```` ```markdown ```` fence (line 731) is closed early by the same-length ```` ```bash ```` fence at line 749 (CommonMark: an equal-length fence closes the block), so the template link at line 736 (and 796) parses as a real markdown link → strict warning.

Fix: widen the outer fence. Line 731: ```` ```markdown ```` → ```` ````markdown ```` ```` (4 backticks). Line 814: ```` ``` ```` → ```` ```` ```` ```` (4 backticks). The inner 3-backtick bash fences (749/754, 761/763, 776/782, 803/805) then nest correctly.

- [ ] **Step 2: Fix the curation.md directory-style link**

Line 11: `[catalog page](../pipelines/)` → `[catalog page](/pipelines/)`.

- [ ] **Step 3: Footer copyright with org/engine/issues links + evidence legend**

In mkdocs.yml, replace the `copyright: >-` block with:

```yaml
copyright: >-
  © 2026 <a href="https://github.com/oxo-flow-community">oxo-flow-community</a>
  · Apache-2.0 · engine
  <a href="https://github.com/Traitome/oxo-flow">oxo-flow</a> ·
  <a href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues">issues</a>
  · evidence: ✔ live-tested ⊃ ★ verified ⊃ ☆ community
  · ports are based on their upstream workflows — see each repository's NOTICE
```

- [ ] **Step 4: Strict build — zero warnings**

Run: `mkdocs build --strict`
Expected: exit 0, no warnings.

- [ ] **Step 5: Verify edits survived (revert watch)**

Run: `git diff --stat` — mkdocs.yml and both about/ files must appear.

- [ ] **Step 6: Commit**

```bash
git add docs/about/porting.md docs/about/curation.md mkdocs.yml
git commit -m "fix: strict-build warnings (fence nesting, catalog link) + linked mono footer"
```

---

### Task 6: Final gate — strict build, site/ mirror, PR, merge, deploy verification

**Files:**
- Regenerate: `site/` mirror (built artifact — commit with the docs changes)
- No source changes expected; fix any strict-build fallout here.

**Interfaces:**
- Consumes: everything from Tasks 1–5.
- Produces: merged PR on main; live site serving the v2 design.

- [ ] **Step 1: Clean rebuild into site/**

```bash
git checkout -- site/
git clean -fd site/assets/dag/
python3 scripts/generate.py
mkdocs build --strict
```

Expected: zero warnings; `git status` shows site/ changes plus possibly nothing else.

- [ ] **Step 2: Full CI-parity checks**

Run: `git diff --exit-code -- docs/ data/ scripts/ ':!docs/assets/dag'` (must be clean) and confirm `ls site/assets/dag | grep -c clindet` is `0` (the 3 stale SVGs must NOT exist in the built mirror).

- [ ] **Step 3: Sanity-grep the built site**

Run greps on site/: `grep -c "ox-hero-split" site/index.html` (1), `grep -c "ox-glance" site/pipelines/oxo-flow-rnaseq/index.html` (1), `grep -c "0a0f0d" site/stylesheets/extra.css` (1), `grep -c "known-divergences" site/pipelines/oxo-flow-chipseq/index.html` (≥1).

- [ ] **Step 4: Commit docs + site mirror**

```bash
git add docs/ data/ scripts/ mkdocs.yml site/
git commit -m "build: regenerate site mirror for design system v2"
```

- [ ] **Step 5: Push and open the PR**

```bash
git push -u origin feat/site-v2-beautify
gh pr create --base main --head feat/site-v2-beautify --title "Site beautify: design system v2 (split hero, evidence cards, instrument dark)" --body "A+V2+W2+P2+D2 design system per spec .superpowers/specs/2026-09-05-site-beautify-design.md. Strict build now warning-free."
```

- [ ] **Step 6: Wait for PR CI (pr.yml: generate drift check + strict build)**

Run: `gh pr checks feat/site-v2-beautify --watch`
Expected: all green.

- [ ] **Step 7: Squash-merge (repo workflow)**

Run: `gh pr merge feat/site-v2-beautify --squash --delete-branch`
Expected: merged to main; deploy.yml runs on main push.

- [ ] **Step 8: Verify live deployment**

Poll until `curl -s -o /dev/null -w "%{http_code}" https://oxo-flow-community.github.io/` returns 200, then spot-check: `curl -s https://oxo-flow-community.github.io/ | grep -c "ox-hero-split"` (1) and `curl -s https://oxo-flow-community.github.io/pipelines/oxo-flow-rnaseq/ | grep -c "At a glance"` (1). (CDN can lag a few minutes; deploy.yml itself polls all 26 URLs for 200.)

- [ ] **Step 9: Final report**

Summarize: what shipped, the design decision set (A+V2+W2+P2+D2), the 3 warnings fixed, and the live URLs to eyeball (home, /pipelines/, one port page, one original page) in both color schemes and mobile width — the last visual check is the user's.
