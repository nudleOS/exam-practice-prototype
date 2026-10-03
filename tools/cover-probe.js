// Cover probe (run in the page): is anything in the question COVERED by another layer where it shows on screen?
// For every visible leaf text and control inside the question, it samples three points across the middle of the element's on-screen
// box and asks the browser what is on top there (elementFromPoint). A hit that is not the element (or inside it) is a cover, unless
// the element is wholly behind the solid header or the bar (scrolled away, which is not an overlap). Returns the covers found.
// Usage: (await import('/tools/cover-probe.js?v=1')).probe()
export function probe() {
  const q = document.querySelector("main:not(#mq-stage) [data-question]"); if (!q) return [];
  const head = document.querySelector("[data-playhead]"), foot = document.querySelector("[data-footer]");
  const top = head ? head.getBoundingClientRect().bottom : 0;
  // the bar, or on a long phone question the SOLID part of its fade (--nx-fadeH, solid 20 px in): anything below it is scrolled away
  // behind the band, not overlapped (the fade lets taps through, so elementFromPoint cannot see it)
  const fh = parseFloat(document.body.style.getPropertyValue("--nx-fadeH")) || 0, ft = foot && foot.offsetHeight ? foot.getBoundingClientRect().top : innerHeight;
  const bot = document.body.classList.contains("nx-compact") && fh ? ft - fh + 20 : ft;
  const els = [...q.querySelectorAll("button, input, textarea, select, [role=slider], p, span, label, h2, text")]
    .filter(e => { const r = e.getBoundingClientRect(); if (!r.width || !r.height) return false;
      if (e.matches("span, p, label, h2, text") && [...e.children].some(c => c.matches("span, p, label, button, input, textarea"))) return false;   // leaves only
      const cs = getComputedStyle(e); return cs.visibility !== "hidden" && cs.opacity !== "0" && (e.textContent.trim() || e.matches("button, input, textarea, select, [role=slider]")); });
  const out = [];
  els.forEach(e => { const r = e.getBoundingClientRect(); if (r.bottom <= top + 2 || r.top >= bot - 2) return;   // fully scrolled under the solid header / bar
    const y = r.top + r.height / 2; if (y < top || y > bot) return;
    [0.2, 0.5, 0.8].some(f => { const x = r.left + r.width * f; if (x < 0 || x > innerWidth) return false; const h = document.elementFromPoint(x, y);
      // not covers: a hit on the element's own ancestor (wrapped inline text samples its parent's gaps), or a field's own in-box button
      if (e.closest(".sr-only") || !h || h === e || e.contains(h) || h.contains(e)) return false;
      if (e.matches("input, textarea") && h.closest("[data-submit]") && h.closest("[data-submit]").parentElement.contains(e)) return false;
      out.push({ el: (e.tagName + "." + (e.className.baseVal != null ? e.className.baseVal : e.className)).slice(0, 40) + " '" + e.textContent.trim().slice(0, 24) + "'", at: [Math.round(x), Math.round(y)],
        by: (h.tagName + "." + (h.className.baseVal != null ? h.className.baseVal : h.className)).slice(0, 40) + (h.closest(".nx-typestrip") ? " (strip)" : h.closest("[data-footer]") ? " (bar)" : "") });
      return true; }); });
  return out;
}
