/* build-play.js: the paper's drawing questions as things to BUILD, auto-marked against the memo's own criteria (Murci approved the
   mockup 2026-10-03: "Yes please"). Two kinds:
   - "hist"  (3.1.3) a histogram, one examiner rule per step: Type (T), Caption (C), Axes labels (L), Scale (S), Plot (P, drag bars).
   - "stems" (3.6.4) three stems in the box: tap how each looks after the investigation (bends left / straight up / right / no growth).
   The host (Exam Practice) owns the ANSWER (its state, so Check, marking and "same answer" work as for every other type); this
   module owns only its DOM and its step. A learner who drew it on paper gets the criteria as a self-check (shown, never banked).

   window.BuildPlay.mount(host, { kind, cfg, value, onChange(value), reduced }) -> { sync({ value, locked, items, itemsFor }), destroy() }
     value      the answer so far ({} at the start)
     items      the marker's items for the last check ({ key, awarded, available }), shown as chips while the answer is unchanged
     itemsFor   JSON of the answer those items marked (an edit hides them: they no longer describe what is on screen)
*/
(function () {
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const clone = o => JSON.parse(JSON.stringify(o || {}));
  const svg = d => `<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const ICON = { histogram: svg('<path d="M3 21h18M5 21V11h4v10M9 21V6h4v15M13 21V9h4v12"/>'), bar: svg('<path d="M3 21h18M5 21v-9h3v9M10.5 21V6h3v15M16 21v-6h3v6"/>'),
    line: svg('<path d="M3 21h18M4 16l5-6 4 3 7-8"/>'), left: svg('<path d="M14 21v-7a5 5 0 0 0-5-5H5M8 6L5 9l3 3"/>'), up: svg('<path d="M12 21V4M8 8l4-4 4 4"/>'),
    right: svg('<path d="M10 21v-7a5 5 0 0 1 5-5h4M16 6l3 3-3 3"/>'), none: svg('<circle cx="12" cy="12" r="8"/><path d="M6.5 17.5l11-11"/>') };

  // ── the histogram builder
  function hist(host, o) {
    const cfg = o.cfg, STEPS = ["Type", "Caption", "Axes", "Scale", "Plot"];
    let v = Object.assign({ type: "", cap: "", xl: "", yl: "", step: 0, v: cfg.groups.map(() => 0) }, clone(o.value));
    let i = 0, locked = false, chips = "", paper = false, drag = false;   // drag: a bar is held (sync waits; a redraw would drop it)
    const set = patch => { v = Object.assign(v, patch); o.onChange(clone(v)); };
    const done = k => k === 0 ? !!v.type : k === 1 ? v.cap.trim().length > 5 : k === 2 ? !!(v.xl && v.yl) : k === 3 ? !!v.step : v.v.some(x => x > 0);
    const max = () => { const st = v.step || cfg.steps[1]; return Math.ceil(cfg.top / st) * st; };
    function chart() {
      const st = v.step || cfg.steps[1], mx = max(), X0 = 48, X1 = 292, Y0 = 180, Y1 = 14, w = (X1 - X0) / cfg.groups.length, gap = v.type === "bar" ? 12 : 0;
      const y = n => Y0 - (n / mx) * (Y0 - Y1); let g = "", b = "";
      for (let t = 0; t <= mx; t += st) g += `<line x1="${X0}" x2="${X1}" y1="${y(t)}" y2="${y(t)}" class="bp-grid"/><text x="${X0 - 5}" y="${y(t) + 3}" class="bp-tick" text-anchor="end">${t}</text>`;
      v.v.forEach((n, k) => { const x = X0 + k * w + gap / 2, bw = w - gap;
        if (v.type !== "line") b += `<rect x="${x}" y="${y(n)}" width="${bw}" height="${Y0 - y(n)}" class="bp-barr"/>`;
        b += `<g class="bp-h" data-k="${k}" tabindex="${locked ? -1 : 0}" role="slider" aria-label="${esc(cfg.groups[k])} ${esc(cfg.unit || "years")}" aria-valuemin="0" aria-valuemax="${mx}" aria-valuenow="${n}" aria-valuetext="${n}">`
          + (v.type === "line" ? `<circle cx="${x + bw / 2}" cy="${y(n)}" r="7" class="bp-knob"/>` : `<rect x="${x + bw / 2 - 15}" y="${y(n) - 7}" width="30" height="14" rx="7" class="bp-knob"/>`)
          + `<rect x="${x}" y="${Math.min(y(n) - 18, Y0 - 30)}" width="${bw}" height="40" fill="transparent"/></g>`
          + `<text x="${x + bw / 2}" y="${y(n) - 12}" class="bp-val" text-anchor="middle">${n || ""}</text>`
          + `<text x="${X0 + k * w + w / 2}" y="${Y0 + 21}" class="bp-tick" text-anchor="middle">${esc(cfg.groups[k])}</text>`; });
      if (v.type === "line") b = `<polyline points="${v.v.map((n, k) => (X0 + k * w + w / 2) + "," + y(n)).join(" ")}" class="bp-line"/>` + b;
      return `<svg class="bp-chart" viewBox="0 0 300 223" aria-label="Your graph">`
        + `<line x1="${X0}" y1="${Y0}" x2="${X1}" y2="${Y0}" class="bp-axis"/><line x1="${X0}" y1="${Y0}" x2="${X0}" y2="${Y1}" class="bp-axis"/>${g}${b}`
        + `<text x="170" y="220" class="bp-alab" text-anchor="middle">${esc(v.xl || "X-axis label?")}</text>`
        + `<text transform="translate(10,98) rotate(-90)" class="bp-alab" text-anchor="middle">${esc(v.yl ? v.yl.replace(/ \(per .*\)$/, "") : "Y-axis label?")}</text></svg>`;
    }
    function body() {
      if (i === 0) return `<div class="bp-grp"><p class="bp-q">${esc(cfg.typeQ || "Which graph shows age GROUPS against a number?")}</p><div class="bp-opts">`
        + [["histogram", "Histogram"], ["bar", "Bar graph"], ["line", "Line graph"]].map(([k, t]) =>
          `<button type="button" class="bp-opt" data-type="${k}" aria-pressed="${v.type === k}">${ICON[k]}<span>${t}</span></button>`).join("") + `</div></div>`
        + `<p class="bp-hint">${esc(cfg.typeHint || "A histogram's bars touch: its groups run on with no gaps.")}</p>`;
      if (i === 1) return `<div class="bp-grp"><label class="bp-q" for="bp-cap">The caption: name BOTH variables</label>`
        + `<textarea id="bp-cap" class="bp-in" rows="2" maxlength="160" placeholder="The number of … in different …" autocapitalize="off" spellcheck="false">${esc(v.cap)}</textarea></div>`
        + `<p class="bp-hint">What changes along the bottom, and what was counted.</p>`;
      if (i === 2) return `<div class="bp-grp"><label class="bp-q" for="bp-x">The X-axis (along the bottom)</label><select id="bp-x" class="bp-in"><option value="">Choose…</option>${cfg.x.map(t => `<option${v.xl === t ? " selected" : ""}>${esc(t)}</option>`).join("")}</select></div>`
        + `<div class="bp-grp"><label class="bp-q" for="bp-y">The Y-axis (up the side)</label><select id="bp-y" class="bp-in"><option value="">Choose…</option>${cfg.y.map(t => `<option${v.yl === t ? " selected" : ""}>${esc(t)}</option>`).join("")}</select></div>`;
      if (i === 3) return `<div class="bp-grp"><p class="bp-q">The Y-axis goes up in steps of</p><div class="bp-opts">${cfg.steps.map(s => `<button type="button" class="bp-opt" data-step="${s}" aria-pressed="${v.step === s}">${s}</button>`).join("")}</div></div>${chart()}`;
      return chart() + `<p class="bp-hint">Drag each bar to its value (arrow keys work too). The table is in the shared information.</p>`;
    }
    function draw(keepFocus) {
      const f = keepFocus && document.activeElement && host.contains(document.activeElement) ? document.activeElement.dataset.k : null;
      host.innerHTML = `<div class="bp" data-locked="${locked}"><div class="bp-steps">${STEPS.map((s, k) =>
        `<button type="button" class="bp-step" data-i="${k}" aria-current="${k === i ? "step" : "false"}" data-done="${done(k) && k !== i}"><span class="sr-only">Step ${k + 1}: </span>${s}${done(k) && k !== i ? '<span class="sr-only">, done</span>' : ""}</button>`).join("")}</div>`
        + `<div class="bp-body">${body()}</div>${chips}`
        + `<div class="bp-foot">${i < 4 ? `<button type="button" class="nxb nxb-sec nxb-sm bp-next">Next step</button>` : `<span></span>`}<button type="button" class="bp-paper">I drew it on paper</button></div>`
        + (paper ? selfCheck(cfg.criteria) : "") + `</div>`;
      wire(); if (f != null) { const n = host.querySelector(`.bp-h[data-k="${f}"]`); if (n) n.focus({ preventScroll: true }); }
    }
    function wire() {
      const q = s => host.querySelectorAll(s), off = () => locked;
      q(".bp-step").forEach(b => b.onclick = () => { i = +b.dataset.i; draw(); });
      q("[data-type]").forEach(b => b.onclick = () => { if (off()) return; set({ type: b.dataset.type }); draw(); });
      q("[data-step]").forEach(b => b.onclick = () => { if (off()) return; set({ step: +b.dataset.step }); draw(); });
      const cap = host.querySelector("#bp-cap"); if (cap) { cap.disabled = locked; cap.oninput = e => { set({ cap: e.target.value }); host.querySelectorAll(".bp-step")[1].dataset.done = "false"; }; }
      const xs = host.querySelector("#bp-x"), ys = host.querySelector("#bp-y");
      if (xs) { xs.disabled = ys.disabled = locked; xs.onchange = e => set({ xl: e.target.value }); ys.onchange = e => set({ yl: e.target.value }); }
      const nx = host.querySelector(".bp-next"); if (nx) nx.onclick = () => { i++; draw(); const b = host.querySelector(".bp-body"); if (b) b.scrollIntoView({ block: "nearest" }); };
      host.querySelector(".bp-paper").onclick = () => { paper = !paper; draw(); };
      const ch = host.querySelector(".bp-chart"); if (!ch || i !== 4 || locked) return;
      let k = -1; const mx = max();
      const at = e => { const r = ch.getBoundingClientRect(), yy = (e.clientY - r.top) * 223 / r.height; const sn = cfg.snap || 10; return Math.max(0, Math.min(mx, Math.round((180 - yy) / 166 * mx / sn) * sn)); };
      const put = (kk, n) => { const a = v.v.slice(); a[kk] = n; set({ v: a }); };
      // (a drag repaints the svg's CHILDREN only: rebuilding the svg would drop the pointer capture, and a finger that slid past the
      // chart's edge would stop moving the bar)
      const paint = () => { const t = document.createElement("div"); t.innerHTML = chart(); ch.innerHTML = t.firstElementChild.innerHTML; };
      ch.onpointerdown = e => { const h = e.target.closest(".bp-h"); if (!h) return; k = +h.dataset.k; drag = true; document.documentElement.classList.add("bp-drag"); ch.setPointerCapture(e.pointerId); put(k, at(e)); paint(); e.preventDefault(); };
      ch.onpointermove = e => { if (k < 0) return; const n = at(e); if (n !== v.v[k]) { put(k, n); paint(); } };
      const end = () => { if (k < 0) return; const kk = k; k = -1; drag = false; document.documentElement.classList.remove("bp-drag"); o.onChange(clone(v)) /* one more update: the host reveals its Check now the bar is let go */; draw(); const n = host.querySelector(`.bp-h[data-k="${kk}"]`); if (n) n.focus({ preventScroll: true }); };
      ch.onpointerup = end; ch.onpointercancel = end;
      q(".bp-h").forEach(h => h.onkeydown = e => { const sn = cfg.snap || 10, d = { ArrowUp: sn, ArrowRight: sn, ArrowDown: -sn, ArrowLeft: -sn, PageUp: 5 * sn, PageDown: -5 * sn }[e.key];
        if (d == null) return; e.preventDefault(); const kk = +h.dataset.k; put(kk, Math.max(0, Math.min(mx, v.v[kk] + d))); draw(true); });
    }
    draw();
    return { sync(s) { const nv = Object.assign({ type: "", cap: "", xl: "", yl: "", step: 0, v: cfg.groups.map(() => 0) }, clone(s.value));
        const changed = JSON.stringify(nv) !== JSON.stringify(v), was = locked + chips; v = nv; locked = !!s.locked;
        chips = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? chipRow(s.items, cfg.labels) : "";
        if (changed && !Object.keys(s.value || {}).length) i = 0;   // a fresh try (Practise again / a retake) starts at step 1
        if ((changed || was !== locked + chips) && !drag) draw(true); },
      destroy() { document.documentElement.classList.remove("bp-drag"); host.innerHTML = ""; } };
  }

  // ── the stems
  function stems(host, o) {
    const cfg = o.cfg, SH = [["left", "bends left"], ["up", "grows straight up"], ["right", "bends right"], ["none", "no growth"]];
    let v = clone(o.value), locked = false, chips = "", paper = false;
    const X = [74, 167, 260];   // each stem's x in the box (of 300); its buttons sit centred under it (--x)
    const stem = (st, k) => { const x = X[k], s = v[st.id] || "", top = s === "up" ? 58 : 100;
      const d = s === "left" ? `M${x} 160V112Q${x} 82 ${x - 22} 72` : s === "right" ? `M${x} 160V112Q${x} 82 ${x + 22} 72` : `M${x} 160V${top}`;
      const e = s === "left" ? [x - 22, 72] : s === "right" ? [x + 22, 72] : [x, top];
      const tip = st.tip === "tip" ? `<ellipse cx="${e[0]}" cy="${e[1]}" rx="3.5" ry="6" fill="#111"/>` : st.tip === "cap" ? `<path d="M${e[0] - 7} ${e[1] + 9}L${e[0] - 4} ${e[1] - 6}H${e[0] + 4}L${e[0] + 7} ${e[1] + 9}Z" fill="#111"/>` : "";
      return `<path d="${d}" stroke="#111" stroke-width="7" fill="none" stroke-linecap="${st.tip === "none" ? "butt" : "round"}"/>${tip}`
        + `<text x="${x}" y="173" font-size="11" fill="#222" text-anchor="middle">${st.id}</text>`; };
    function draw() {
      host.innerHTML = `<div class="bp" data-locked="${locked}">`
        + `<svg class="bp-box" viewBox="0 0 300 190" role="img" aria-label="${esc(cfg.alt)}"><text x="8" y="70" font-size="11" fill="#222">Light</text>`
        + `<path d="M8 78h26M28 72l7 6-7 6" stroke="#222" stroke-width="2" fill="none"/><path d="M44 30V62M44 96V160H290V30H44" stroke="#222" stroke-width="2" fill="none"/>`
        + `<rect x="54" y="160" width="226" height="18" rx="4" fill="#eee" stroke="#222"/>${cfg.stems.map(stem).join("")}</svg>`
        + `<div class="bp-cols">${cfg.stems.map((st, k) => `<div class="bp-sg" role="group" aria-label="Stem ${st.id}" style="--x:${(X[k] / 300).toFixed(4)}">${SH.map(([s, nm]) =>
          `<button type="button" class="bp-sh bp-sh-${s}" data-id="${st.id}" data-s="${s}" aria-pressed="${v[st.id] === s}" aria-label="Stem ${st.id}: ${nm}"${locked ? " disabled" : ""}>${ICON[s]}</button>`).join("")}</div>`).join("")}</div>`
        + `<p class="bp-hint">Tap how each stem looks after five days.</p>${chips}`
        + `<div class="bp-foot"><span></span><button type="button" class="bp-paper">I drew it on paper</button></div>${paper ? selfCheck(cfg.criteria) : ""}</div>`;
      host.querySelectorAll(".bp-sh").forEach(b => b.onclick = () => { if (locked) return; v[b.dataset.id] = b.dataset.s; o.onChange(clone(v)); draw();
        const n = host.querySelector(`.bp-sh[data-id="${b.dataset.id}"][data-s="${b.dataset.s}"]`); if (n) n.focus({ preventScroll: true }); });
      host.querySelector(".bp-paper").onclick = () => { paper = !paper; draw(); };
    }
    draw();
    return { sync(s) { const nv = clone(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v), was = locked + chips; v = nv; locked = !!s.locked;
        chips = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? chipRow(s.items, cfg.labels) : "";
        if (changed || was !== locked + chips) draw(); },
      destroy() { host.innerHTML = ""; } };
  }

  function chipRow(items, labels) {
    return `<div class="bp-chips" role="status">${items.map(it => { const ok = it.awarded >= it.available;
      return `<span class="bp-chip" data-ok="${ok}">${ok ? "✓" : it.awarded > 0 ? "◐" : "✕"} ${esc(labels[it.key] || it.key)}${it.available > 1 ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
  }
  // drew it on paper: the memo's criteria to tick, shown and never banked (a self-ticked mark is not a mark)
  function selfCheck(criteria) {
    return `<div class="bp-self"><p class="bp-q">Drew it on paper? Tick what your drawing has.</p>${criteria.map((c, k) =>
      `<label class="bp-tick-row"><input type="checkbox"> ${esc(c[0])}</label>`).join("")}<p class="bp-hint">A self-check: it guides you, it is not marked.</p></div>`;
  }

  window.BuildPlay = { mount(host, o) { return (o.kind === "hist" ? hist : stems)(host, o); } };
})();
