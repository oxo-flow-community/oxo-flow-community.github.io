/* oxo-flow-community catalog renderer — no dependencies, vanilla JS.
   Reads window.OXO_PIPELINES (generated registry data) and renders stats,
   featured cards, and the searchable catalog grid. */
(() => {
  "use strict";

  const P = window.OXO_PIPELINES || [];
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

  const ORIGIN = {
    port: "⇄ Official port",
    original: "✦ Original",
    curated: "♺ Community listing",
  };

  function cardHTML(p) {
    const star = p.rating === "live-verified"
      ? '<span class="ox-badge ox-badge--live">✔ Live-tested</span>'
      : p.rating === "verified"
        ? '<span class="ox-badge ox-badge--star">★ Verified</span>'
        : '<span class="ox-badge">☆ Community</span>';
    const engBadge = p.engine === "nextflow"
      ? '<span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span>'
      : p.engine === "snakemake"
        ? '<span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span>'
        : "";
    const origin = ORIGIN[p.origin] || ORIGIN.curated;
    const cmd = p.quickstart || "oxo-flow run main.oxoflow";
    const compute = p.compute
      ? `<span class="ox-badge" title="Peak compute per rule">⚙ ${esc(p.compute)}</span>`
      : "";
    return `<article class="ox-card">
      <div class="row">
        <a class="name" href="/pipelines/${esc(p.name)}/">${esc(p.name)}</a>
        ${star}
      </div>
      <p class="title">${esc(p.title)}</p>
      <div class="meta">
        <span class="ox-badge ox-badge--origin">${origin}</span>
        ${engBadge}
        <span class="ox-badge">${esc(p.domain)}</span>
        <span class="ox-badge">${Number(p.rule_count) || 0} rules</span>
        ${compute}
      </div>
      <div class="tools">${(p.tools || []).map((t) => esc(t)).join('<span class="sep">·</span>')}</div>
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

  function renderCatalog() {
    const search = document.getElementById("ox-search");
    const chips = document.getElementById("ox-chips");
    const grid = document.getElementById("ox-all");
    const count = document.getElementById("ox-count");
    const empty = document.getElementById("ox-empty");
    if (!search || !grid) return;

    const state = { q: "", domains: new Set(), origins: new Set(), engines: new Set() };
    const domains = [...new Set(P.map((p) => p.domain))].sort();
    const origins = [...new Set(P.map((p) => p.origin || "curated"))].sort();
    const engines = [...new Set(P.map((p) => p.engine).filter(Boolean))].sort();

    function chip(label, key, values) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "ox-chip";
      b.textContent = label;
      b.setAttribute("aria-pressed", "false");
      b.addEventListener("click", () => {
        if (values.has(key)) { values.delete(key); b.setAttribute("aria-pressed", "false"); }
        else { values.add(key); b.setAttribute("aria-pressed", "true"); }
        apply();
      });
      return b;
    }

    const ORIGIN_LABEL = { port: "official ports", original: "originals", curated: "community" };
    domains.forEach((d) => chips.appendChild(chip(d, d, state.domains)));
    origins.forEach((o) => chips.appendChild(chip(ORIGIN_LABEL[o] || o, o, state.origins)));
    engines.forEach((e) => chips.appendChild(chip(e === "nextflow" ? "nf-core ports" : "snakemake ports", e, state.engines)));

    function matches(p) {
      const hay = [p.name, p.title, p.domain, ...(p.tags || []), ...(p.tools || [])]
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
      grid.innerHTML = shown.map(cardHTML).join("");
      empty.hidden = shown.length !== 0;
      count.textContent = shown.length === P.length
        ? `${P.length} workflows`
        : `${shown.length} of ${P.length} workflows`;
    }

    search.addEventListener("input", (e) => { state.q = e.target.value; apply(); });
    apply();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      renderStats(); renderFeatured(); renderCatalog();
    });
  } else {
    renderStats(); renderFeatured(); renderCatalog();
  }
})();
