// overlap-sweep.js: a check for things drawn on top of each other on a phone (2026-10-03, after Murci's P30 lite walk).
// Usage, in the browser console at the device size (e.g. 360x702):
//   await import('/tools/overlap-sweep.js'); __sweep({ label: 'map' })
// Returns { covers: text with a DRAWN layer over it, controls: controls overlapping controls, hiddenControls: controls under a
// drawn layer, sideScroll }. Expected, not defects: an in-box arrow over its own input; the page behind an open modal sheet
// (pm-dim); content scrolling under the sticky header or the bottom bar; the MCQ glass resting on the bar's edge.

// everything while it runs, because bubbles and strips are pointer-events:none and would otherwise be invisible to the probe.
window.__sweep = function (opts) {
  opts = opts || {};
  const st = document.createElement("style"); st.textContent = "*, *::before, *::after { pointer-events: auto !important; }"; document.head.appendChild(st);
  const W = innerWidth, H = innerHeight, covers = [];
  const name = e => { if (!e || !e.tagName) return "?"; const c = typeof e.className === "string" ? e.className.trim().split(/\s+/)[0] : (e.className && e.className.baseVal || "");
    const d = e.dataset ? Object.keys(e.dataset).filter(k => k !== "dcTpl")[0] : ""; return e.tagName.toLowerCase() + (c ? "." + c : "") + (d ? "[" + d + "]" : ""); };
  const visible = e => { for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const cs = getComputedStyle(x); if (cs.visibility === "hidden" || cs.display === "none" || +cs.opacity < 0.08) return false;
      const r = x.getBoundingClientRect(); if (cs.overflow === "hidden" && (r.width <= 2 || r.height <= 2)) return false;
      if (/rect\(0px,? 0px,? 0px,? 0px\)/.test(cs.clip)) return false; } return true; };
  const alpha = c => { const m = /rgba?\(([^)]+)\)/.exec(c || ""); if (!m) return c && c !== "transparent" ? 1 : 0; const p = m[1].split(/[ ,/]+/).filter(Boolean); return p.length > 3 ? parseFloat(p[3]) : 1; };
  const paints = (e, x, y) => { if (!visible(e)) return false;
    if (/^CANVAS$/i.test(e.tagName)) { let ctx = null; try { ctx = e.getContext("2d"); } catch (_) {} if (!ctx) return true;   // a 3D canvas: cannot read it, count it
      const r = e.getBoundingClientRect(), px = Math.floor((x - r.left) * e.width / r.width), py = Math.floor((y - r.top) * e.height / r.height);
      try { return ctx.getImageData(px, py, 1, 1).data[3] > 12; } catch (_) { return true; } }                                // a 2D one: is the pixel there clear?
    if (/^(IMG|SVG|VIDEO|MODEL-FLOOR|PATH|CIRCLE|RECT)$/i.test(e.tagName)) return true;
    const cs = getComputedStyle(e); if (alpha(cs.backgroundColor) > 0.05 || cs.backgroundImage !== "none" || cs.boxShadow !== "none") return true;
    if (parseFloat(cs.borderTopWidth) > 0 && alpha(cs.borderTopColor) > 0.05) return true;
    return [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const txt = n.textContent.replace(/\s+/g, " ").trim(); if (txt.length < 2) continue;
    const el = n.parentElement; if (!el || !visible(el) || el.closest("script, style, .nx-kbsim")) continue;
    const box = el.closest("button, a, label, [role='button'], li");
    const rg = document.createRange(); rg.selectNodeContents(n);
    [...rg.getClientRects()].forEach(r => {
      if (r.width < 4 || r.height < 4 || r.bottom < 0 || r.top > H) return;
      const y = r.top + r.height / 2;
      [0.08, 0.3, 0.5, 0.7, 0.92].forEach(f => { const x = r.left + r.width * f; if (x < 0 || x >= W) return;
        for (const e of document.elementsFromPoint(x, y)) {
          if (e === el || el.contains(e) || e.contains(el)) break;          // reached the text (or its own box): nothing drawn over it
          if (box && box.contains(e)) break;                                 // an icon inside the same control is not a cover
          if (paints(e, x, y)) { covers.push({ text: txt.slice(0, 40), by: name(e), at: [Math.round(x), Math.round(y)] }); break; }
        } }); });
  }
  // controls on top of controls (Skip on the answer box, 2026-10-03): any two visible, on-screen controls whose boxes overlap by
  // more than 4 px each way, neither inside the other
  const ctl = [...document.querySelectorAll("button, input, textarea, select, a[href], [role='button']")].filter(e => { const r = e.getBoundingClientRect();
    return visible(e) && r.width > 6 && r.height > 6 && r.bottom > 0 && r.top < H && r.right > 0 && r.left < W; });
  const clash = [];
  for (let i = 0; i < ctl.length; i++) for (let j = i + 1; j < ctl.length; j++) { const a = ctl[i], b = ctl[j]; if (a.contains(b) || b.contains(a)) continue;
    const p = a.getBoundingClientRect(), q = b.getBoundingClientRect(), ox = Math.min(p.right, q.right) - Math.max(p.left, q.left), oy = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
    if (ox > 4 && oy > 4) clash.push(name(a) + " '" + (a.innerText || a.placeholder || a.getAttribute("aria-label") || "").trim().slice(0, 18) + "' x " + name(b) + " '" + (b.innerText || b.placeholder || b.getAttribute("aria-label") || "").trim().slice(0, 18) + "'"); }
  // a control with something drawn over its centre (a check arrow under the strip, 2026-10-03)
  const hidden = [];
  ctl.forEach(c => { const r = c.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2; if (x < 0 || x >= W || y < 0 || y >= H) return;
    for (const e of document.elementsFromPoint(x, y)) { if (e === c || c.contains(e) || e.contains(c)) break;
      if (paints(e, x, y)) { hidden.push(name(c) + " '" + (c.innerText || c.placeholder || c.getAttribute("aria-label") || "").trim().slice(0, 18) + "' under " + name(e)); break; } } });
  st.remove();
  const s = new Set(), out = covers.filter(c => { const k = c.text + "|" + c.by; if (s.has(k)) return false; s.add(k); return true; });
  return { screen: opts.label || location.search, covers: out, controls: clash, hiddenControls: hidden, sideScroll: document.documentElement.scrollWidth > W + 1 ? document.documentElement.scrollWidth : false };
};
