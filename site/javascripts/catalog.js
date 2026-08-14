/* oxo-flow-community catalog renderer — no dependencies, vanilla JS.
   Reads window.OXO_PIPELINES (generated data) and renders stats, featured
   cards, and the searchable catalog grid. */
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

  const engineName = (p) => (p.engine === "nextflow" ? "nf-core" : "snakemake");
  const shortName = (p) => p.name.replace(/^oxo-flow-/, "");

  function cardHTML(p) {
    const eng = engineName(p);
    const engClass = p.engine === "nextflow" ? "nf" : "sn";
    const cmd = p.quickstart ||
      `oxo-flow run workflow/${shortName(p)}.toml --config config/default.toml`;
    return `<article class="ox-card">
      <a class="name" href="pipelines/${esc(p.name)}/">${esc(p.name)}</a>
      <p class="title">${esc(p.title)}</p>
      <div class="meta">
        <span class="ox-badge ox-badge--${engClass}"><span class="dot"></span>${eng}</span>
        <span class="ox-badge">${esc(p.domain)}</span>
        <span class="ox-badge">${Number(p.rule_count) || 0} rules</span>
      </div>
      <div class="tools">${(p.tools || []).map((t) => "● " + esc(t)).join("  ")}</div>
      <p class="cmd">$ ${esc(cmd)}</p>
      <div class="links">
        <a href="pipelines/${esc(p.name)}/">Run notes</a>
        <a href="${esc(p.repo_url)}" rel="noopener">GitHub ↗</a>
      </div>
    </article>`;
  }

  function renderStats() {
    const el = document.getElementById("ox-stats");
    if (!el || !P.length) return;
    const rules = P.reduce((a, p) => a + (Number(p.rule_count) || 0), 0);
    const tools = new Set(P.flatMap((p) => p.tools || [])).size;
    const domains = new Set(P.map((p) => p.domain)).size;
    el.innerHTML = `
      <div class="ox-stat"><div class="v">${P.length}</div><div class="k">workflows</div></div>
      <div class="ox-stat"><div class="v">${rules}</div><div class="k">rules ported</div></div>
      <div class="ox-stat"><div class="v">${tools}</div><div class="k">tools pinned</div></div>
      <div class="ox-stat"><div class="v">${domains}</div><div class="k">domains</div></div>`;
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

    const state = { q: "", domains: new Set(), engines: new Set() };
    const domains = [...new Set(P.map((p) => p.domain))].sort();
    const engines = [...new Set(P.map((p) => p.engine))].sort();

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

    domains.forEach((d) => chips.appendChild(chip(d, d, state.domains)));
    engines.forEach((e) => chips.appendChild(chip(engineLabel(e), e, state.engines)));
    function engineLabel(e) { return e === "nextflow" ? "nf-core" : "snakemake"; }

    function matches(p) {
      const hay = [p.name, p.title, p.domain, ...(p.tags || []), ...(p.tools || [])]
        .join(" ").toLowerCase();
      const q = state.q.trim().toLowerCase();
      if (q && !hay.includes(q)) return false;
      if (state.domains.size && !state.domains.has(p.domain)) return false;
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
