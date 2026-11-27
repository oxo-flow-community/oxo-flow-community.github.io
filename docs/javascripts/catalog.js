/* oxo-flow-community catalog renderer — no dependencies, vanilla JS.
   Reads window.OXO_PIPELINES (generated registry data) and renders stats,
   featured cards, and the searchable catalog grid. Since the script is
   loaded on every page it also carries the ONE copy-to-clipboard handler
   for every [data-copy] element (parameter rows, hero commands, …). */
(() => {
  "use strict";
  // Own src, captured while the parser still knows about us — used to load
  // the registry data lazily (only pages with catalog mounts pay for it).
  const SELF = (document.currentScript && document.currentScript.src) || "javascripts/catalog.js";

  // ---- copy-to-clipboard (single source; elements opt in via data-copy) ----
  let liveRegion;
  const announce = (msg) => {
    if (!liveRegion) {
      liveRegion = document.createElement("span");
      liveRegion.setAttribute("role", "status");
      liveRegion.setAttribute("aria-live", "polite");
      Object.assign(liveRegion.style, {
        position: "absolute", width: "1px", height: "1px",
        overflow: "hidden", clip: "rect(0 0 0 0)", whiteSpace: "nowrap",
      });
      document.body.appendChild(liveRegion);
    }
    liveRegion.textContent = msg;
  };
  document.addEventListener("click", (ev) => {
    const btn = ev.target.closest("[data-copy]");
    if (!btn) return;
    const text = btn.getAttribute("data-copy");
    // aria-label outranks the CSS ::after glyph (" ⧉"/" ✓") in the
    // accessible name — without it the button is spoken as its content.
    if (!btn.getAttribute("aria-label")) {
      btn.setAttribute("aria-label", "Copy " + text);
    }
    const flash = (ok) => {
      btn.classList.add("copied");
      setTimeout(() => btn.classList.remove("copied"), 1200);
      announce(ok ? "Copied: " + text : "Copy failed — select the text manually");
    };
    (navigator.clipboard?.writeText(text) || Promise.reject())
      .then(() => flash(true))
      .catch(() => flash(false));
  });

  let P = [];
  const FEATURED = [
    "oxo-flow-rnaseq",
    "oxo-flow-sarek",
    "oxo-flow-rnaseq-star-deseq2",
    "oxo-flow-viralrecon",
    "oxo-flow-mag",
    "oxo-flow-chipseq",
  ];

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));

  function cardHTML(p) {
    const star = p.rating === "live-verified"
      ? '<span class="ox-badge ox-badge--live">✔ Live-tested</span>'
      : p.rating === "verified"
        ? '<span class="ox-badge ox-badge--star">★ Verified</span>'
        : p.rating === "dry-run-verified"
          ? '<span class="ox-badge ox-badge--dry">◆ Dry-run verified</span>'
          : '<span class="ox-badge">☆ Community</span>';
    const engBadge = p.engine === "nextflow"
      ? '<span class="ox-badge ox-badge--nf"><span class="dot" aria-hidden="true"></span>nf-core</span>'
      : p.engine === "snakemake"
        ? '<span class="ox-badge ox-badge--sn"><span class="dot" aria-hidden="true"></span>snakemake</span>'
        : p.engine === "oxo-flow"
          ? '<span class="ox-badge ox-badge--native"><span class="dot" aria-hidden="true"></span>oxo-flow native</span>'
          : "";
    // Cards show the fetch-to-runs path: pull the repo, run from it.
    // The owner comes from repo_url — community entries live outside the
    // org (WangLabCSU/...); a hard-coded org prefix would 404 on those.
    const m = /github\.com\/([^/]+\/[^/]+?)\/?$/.exec(p.repo_url || "");
    const ghSlug = m ? m[1] : "oxo-flow-community/" + p.name;
    // Mirrors generate.py pull_bar_body EXACTLY (same 52-char threshold):
    // six slugs sit in the 53–54 band and must not render one-line on cards
    // while the page shows the continuation pair.
    const cmd = ("$ oxo-flow pull gh:" + ghSlug).length > 52
      ? "oxo-flow pull \\\n  gh:" + ghSlug
      : "oxo-flow pull gh:" + ghSlug;
    // Compute badge on its own line — long strings never squeeze the tool chips
    const compute = p.compute
      ? `<div class="compute">⚙ <span title="Peak compute per rule">${esc(p.compute)}</span></div>`
      : "";
    const tools = (p.tools || []);
    const toolChips = tools.slice(0, 2)
      .map((t) => `<span class="tchip">${esc(t)}</span>`).join("");
    const more = tools.length > 2
      ? `<span class="tchip tchip--more">+${tools.length - 2}</span>` : "";
    const cls = p.rating === "live-verified" ? "ox-card live-card" : "ox-card";
    return `<article class="${cls}">
      <div class="row">
        <a class="name" href="/pipelines/${esc(p.name)}/">${esc(p.name)}</a>
        <span class="ox-badge">${esc(p.domain)}</span>
      </div>
      <p class="title">${esc(p.title)}</p>
      ${compute}
      <div class="meta">
        <span class="ox-badge">${p.rule_count != null ? `${Number(p.rule_count) || 0} rules` : "rules —"}</span>
        ${toolChips}
        ${more}
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

  function renderStats() {
    const el = document.getElementById("ox-stats");
    if (!el || !P.length) return;
    const rules = P.reduce((a, p) => a + (Number(p.rule_count) || 0), 0);
    const tools = new Set(P.flatMap((p) => p.tools || [])).size;
    // Tier counts are cumulative (evidence ladder), so a bare "verified"
    // count alongside live-tested would violate monotonicity: every
    // live-tested workflow already satisfies verified. Show coverage of
    // the top rung instead; per-workflow badges carry the ladder detail.
    const live = P.filter((p) => p.rating === "live-verified").length;
    el.innerHTML = `
      <div class="ox-stat"><div class="v">${P.length}</div><div class="k">workflows</div></div>
      <div class="ox-stat"><div class="v">${live}/${P.length}</div><div class="k">live-tested</div></div>
      <div class="ox-stat"><div class="v">${rules}</div><div class="k">rules</div></div>
      <div class="ox-stat"><div class="v">${tools}</div><div class="k">tools pinned</div></div>
      <p class="ox-stats-note">Ratings are an evidence ladder — ✔ live-tested already includes ★ verified. <a href="/about/curation/">What the ratings mean</a></p>`;
  }

  function renderFeatured() {
    const el = document.getElementById("ox-featured");
    if (!el) return;
    const items = FEATURED.map((n) => P.find((p) => p.name === n))
      .filter(Boolean);
    if (!items.length) { el.hidden = true; return; }
    items.forEach((p) => el.insertAdjacentHTML("beforeend", cardHTML(p)));
  }

  // Modern landing "browse by domain" pills -> faceted catalog entry.
  function renderDomains() {
    const el = document.getElementById("ox-domains");
    if (!el) return;
    const by = new Map();
    P.forEach((p) => {
      if (!by.has(p.domain)) by.set(p.domain, []);
      by.get(p.domain).push(p);
    });
    // Keys are the registry's actual domain values (data/pipelines.json) —
    // the old set (rna-seq/proteomics/...) never matched and 8 of 11 domains
    // fell back to ▦. Keep in sync when the domain vocabulary is normalized.
    const ICONS = {
      genomics: "🧬", metagenomics: "🔬", "single-cell": "🦠",
      transcriptomics: "🧫", "transcriptomics (circRNA)": "🌀",
      amplicon: "🧪", epigenomics: "🧿", immunology: "🩸",
      "cancer genomics (WES/WGS/RNA)": "🎯", "genome-mining": "⛏️",
      other: "🧩",
    };
    el.innerHTML = [...by.entries()]
      .sort((a, b) => b[1].length - a[1].length)
      .map(([dom, items]) =>
        `<a class="ox-domain-pill" href="/pipelines/?domain=${encodeURIComponent(dom)}">` +
        `<span class="ox-domain-ico" aria-hidden="true">${ICONS[dom] || "▦"}</span><span class="ox-domain-name">${esc(dom)}</span>` +
        `<span class="ox-domain-count">${items.length}</span></a>`)
      .join("");
  }

  function renderCatalog() {
    const search = document.getElementById("ox-search");
    const chips = document.getElementById("ox-chips");
    const grid = document.getElementById("ox-all");
    const count = document.getElementById("ox-count");
    const empty = document.getElementById("ox-empty");
    if (!search || !grid) return;

    const state = { q: "", domains: new Set(), origins: new Set(), engines: new Set() };
    // Pre-select a domain facet from the landing pages: /pipelines?domain=x
    const pre = new URLSearchParams(location.search).get("domain");
    if (pre) state.domains.add(pre);
    const domains = [...new Set(P.map((p) => p.domain))].sort();
    const origins = [...new Set(P.map((p) => p.origin || "curated"))].sort();
    const engines = [...new Set(P.map((p) => p.engine).filter(Boolean))].sort();

    function chip(label, key, values, count) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "ox-chip";
      // Accessible name via aria-label ("genomics (12)") — the previous
      // aria-labelledby chained the shared #ox-count live region into every
      // chip's name ("24 of 24 workflows genomics 12"), and every count
      // update re-announced all chips. #ox-count keeps role=status for its
      // own announcements only.
      const l = document.createElement("span");
      l.textContent = label;
      b.appendChild(l);
      if (count !== undefined) {
        const c = document.createElement("span");
        c.className = "ox-chip-count";
        c.textContent = count;
        b.appendChild(c);
        b.setAttribute("aria-label", label + " (" + count + ")");
      }
      b.setAttribute("aria-pressed", values.has(key) ? "true" : "false");
      b.addEventListener("click", () => {
        if (values.has(key)) { values.delete(key); b.setAttribute("aria-pressed", "false"); }
        else { values.add(key); b.setAttribute("aria-pressed", "true"); }
        apply();
      });
      return b;
    }

    const ORIGIN_LABEL = { port: "official ports", original: "originals", curated: "community" };
    domains.forEach((d) => chips.appendChild(chip(d, d, state.domains,
      P.filter((p) => p.domain === d).length)));
    origins.forEach((o) => chips.appendChild(chip(ORIGIN_LABEL[o] || o, o, state.origins,
      P.filter((p) => (p.origin || "curated") === o).length)));
    engines.forEach((e) => chips.appendChild(chip(e === "nextflow" ? "nf-core ports"
      : e === "snakemake" ? "snakemake ports" : "oxo-flow native", e, state.engines,
      P.filter((p) => p.engine === e).length)));

    function matches(p) {
      const hay = [p.name, p.title, p.domain, p.description,
                   ...(p.tags || []), ...(p.tools || [])]
        .join(" ").toLowerCase();
      const q = state.q.trim().toLowerCase();
      if (q && !hay.includes(q)) return false;
      if (state.domains.size && !state.domains.has(p.domain)) return false;
      if (state.origins.size && !state.origins.has(p.origin || "curated")) return false;
      if (state.engines.size && !state.engines.has(p.engine)) return false;
      return true;
    }

    function apply() {
      const shown = P.filter(matches);
      const filtering = state.q.trim() || state.domains.size || state.origins.size || state.engines.size;
      if (!filtering) {
        // Faceted browse: one stacked group per domain — #ox-all stops being
        // a grid itself so each group owns its card grid (never half-width).
        grid.classList.remove("ox-cards");
        const groups = new Map();
        shown.forEach((p) => {
          if (!groups.has(p.domain)) groups.set(p.domain, []);
          groups.get(p.domain).push(p);
        });
        grid.innerHTML = [...groups.entries()]
          .sort((a, b) => a[0].localeCompare(b[0]))
          .map(([dom, items]) =>
            `<div class="ox-cards-group">` +
            `<h3 class="ox-group">${esc(dom)}` +
            `<span class="ox-group-count">${items.length}</span></h3>` +
            `<div class="ox-cards">${items.map(cardHTML).join("")}</div></div>`)
          .join("");
      } else {
        grid.classList.add("ox-cards");
        grid.innerHTML = shown.map(cardHTML).join("");
      }
      empty.hidden = shown.length !== 0;
      count.textContent = shown.length === P.length
        ? `${P.length} workflows`
        : `${shown.length} of ${P.length} workflows`;
    }

    search.addEventListener("input", (e) => { state.q = e.target.value; apply(); });
    apply();
  }

  // The registry data file is ~0.5 MB — audit/pipeline pages must not fetch
  // or parse it. Only pages hosting a catalog mount load it, lazily.
  const MOUNTS = ["ox-stats", "ox-domains", "ox-featured", "ox-count"];
  const wantsCatalog = MOUNTS.some((id) => document.getElementById(id));
  const boot = () => {
    P = window.OXO_PIPELINES || [];
    renderStats(); renderFeatured(); renderDomains(); renderCatalog();
  };
  const whenReady = (fn) => document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", fn)
    : fn();
  if (wantsCatalog) {
    whenReady(() => {
      if (window.OXO_PIPELINES) { boot(); return; }
      const s = document.createElement("script");
      s.src = SELF.replace("catalog.js", "pipelines-data.js");
      s.onload = boot;
      document.head.appendChild(s);
    });
  }
})();
