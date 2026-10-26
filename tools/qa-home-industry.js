/* QA for the home (industry cards) and the industry page, run in the page: load it, then call window.NXQA.*.
   From the console or a test driver:
     const s = document.createElement("script"); s.src = "tools/qa-home-industry.js?" + Date.now(); document.head.append(s);
   Every check returns plain data (no asserts): the driver compares it against what the design says. */
(() => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const live = sel => [...document.querySelectorAll(sel)].filter(e => !e.closest("x-dc"));   // the raw <x-dc> template carries the same markup
  const one = sel => live(sel)[0] || null;
  const vis = e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none" && +cs.opacity > 0.05 && r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth; };
  const lab = e => (e.getAttribute("aria-label") || e.textContent || e.className || e.tagName).toString().trim().replace(/\s+/g, " ").slice(0, 36);
  const frames = (n = 2) => new Promise(r => { const f = () => (--n ? requestAnimationFrame(f) : r()); requestAnimationFrame(f); });
  const vtNames = () => live("*").filter(e => e.style.viewTransitionName).length;

  // the visible screen: sideways scroll, covered controls, small targets, broken images, clipped text
  function audit() {
    const ui = live("button, a[href], select, input, [tabindex]:not([tabindex='-1'])").filter(vis);
    const covered = [], small = [];
    for (const e of ui) { const r = e.getBoundingClientRect();
      const x = Math.min(innerWidth - 1, Math.max(0, r.left + r.width / 2)), y = Math.min(innerHeight - 1, Math.max(0, r.top + r.height / 2));
      const h = document.elementFromPoint(x, y); if (h && h !== e && !e.contains(h) && !h.contains(e)) covered.push(lab(e) + " <- " + lab(h));
      if (r.width < 44 || r.height < 44) small.push(lab(e) + " " + Math.round(r.width) + "x" + Math.round(r.height)); }
    const broken = [...document.images].filter(i => !i.closest("x-dc") && i.complete && i.naturalWidth === 0 && i.getAttribute("src")).map(i => i.getAttribute("src"));
    const clipped = live("h1,h2,h3,b,span,p,button,option").filter(e => vis(e) && e.children.length === 0 && e.scrollWidth > e.clientWidth + 1
      && ["hidden", "clip"].includes(getComputedStyle(e).overflowX) && getComputedStyle(e).textOverflow !== "ellipsis").map(lab).slice(0, 8);
    return { hScroll: document.documentElement.scrollWidth > innerWidth ? document.documentElement.scrollWidth : 0, covered: covered.slice(0, 10), small: small.slice(0, 14), broken, clipped };
  }

  // the deck: scroll position, the end/arrow, and the first cards' x (from the deck's start) / height / opacity
  function deck() { const d = one(".hm-deck"); if (!d) return null; const dl = d.getBoundingClientRect().left, nx = one(".hm-next");
    return { sl: Math.round(d.scrollLeft), max: d.scrollWidth - d.clientWidth, end: nx && nx.dataset.end, arrow: nx ? getComputedStyle(nx).opacity + "/" + getComputedStyle(nx).display : "none",
      cards: live(".hm-card").map(c => { const r = c.getBoundingClientRect(); return c.dataset.hmcard.slice(0, 4) + " " + Math.round(r.left - dl) + "/" + Math.round(r.height) + "/" + (+getComputedStyle(c).opacity).toFixed(2); }) }; }
  async function scrollDeck(x, smooth) { const d = one(".hm-deck"); d.scrollTo({ left: x, behavior: smooth ? "smooth" : "auto" });
    await sleep(smooth ? 900 : 120); await frames(3); return deck(); }

  // open an industry the way the device would: a touch screen taps to open then taps again; a mouse clicks once
  async function openInd(key) { const c = () => one(`[data-hmcard='${key}']`); c().scrollIntoView({ inline: "start", block: "nearest" }); await sleep(250);
    const hover = matchMedia("(hover: hover) and (pointer: fine)").matches; c().click(); let opened = null;
    if (!hover) { await sleep(350); opened = c() && c().getAttribute("aria-expanded"); c().click(); }
    await sleep(1300); await frames(2);
    const ind = one("section.ind");
    return { onPage: !!ind, opened, title: one("#ind-name") && one("#ind-name").textContent, focus: document.activeElement && (document.activeElement.id || document.activeElement.className || document.activeElement.tagName),
      imgs: live(".ind-pro-media img").map(i => i.naturalWidth).join(","), vtNames: vtNames(), vtBack: document.documentElement.classList.contains("vt-back") }; }
  async function back(key) { const h = one("[data-home]"); if (!h) return "no home button"; h.click(); await sleep(1200); await frames(2);
    const c = one(`[data-hmcard='${key}']`); if (!c) return { home: false };
    const r = c.getBoundingClientRect(); return { home: true, card: Math.round(r.left) + "-" + Math.round(r.right) + " of " + innerWidth, whole: r.left >= 0 && r.right <= innerWidth,
      focus: document.activeElement && (document.activeElement.dataset.hmcard || document.activeElement.className || document.activeElement.tagName), vtNames: vtNames() }; }

  // the industry page: pick a paper from a subject's dropdown; the map modal and Escape
  async function pick(secIndex, optIndex) { const s = live(".ind-sec select")[secIndex]; if (!s) return "no select";
    s.value = s.options[optIndex].value; s.dispatchEvent(new Event("change", { bubbles: true })); await sleep(600);
    const d = one(".ind-detail"); return { sel: s.value, detail: d && d.querySelector(".ind-dtitle").textContent, inSec: d ? d.closest(".ind-sec") === s.closest(".ind-sec") : false,
      focus: document.activeElement && document.activeElement.id, buttons: d ? [...d.querySelectorAll("button")].map(lab) : [] }; }
  async function modal() { const m = one("[data-indmap]"); m.click(); await sleep(700);
    const o = { open: !!one(".ind-modal"), focus: document.activeElement && document.activeElement.id, audit: audit() };
    document.activeElement.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true })); await sleep(500);
    o.afterEsc = { open: !!one(".ind-modal"), focus: document.activeElement && (document.activeElement.dataset.indmap ? "mapbox" : document.activeElement.className) }; return o; }

  window.NXQA = { audit, deck, scrollDeck, openInd, back, pick, modal, sleep, frames, vtNames, live, one };
})();
