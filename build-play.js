/* build-play.js: the paper's drawing questions as things to BUILD, auto-marked against the memo's own criteria (Murci approved the
   mockup 2026-10-03: "Yes please"). Four kinds:
   - "hist"  (3.1.3) a histogram, one examiner rule per step: Type (T), Caption (C), Axes labels (L), Scale (S), Plot (P, drag bars).
   - "stems" (3.6.4) three stems in the box: tap how each looks after the investigation (bends left / straight up / right / no growth).
   - "geno"  (LS P2 Nov 2025 2.3.3(b), 2.4.2) genotypes built from the paper's alleles: sockets filled from a tray, exact (DD is not dd).
   - "cross" (LS P2 Nov 2025 2.5.4) a monohybrid cross on a Punnett square, the memo's 8 points (ratio compulsory + any 5).
   - "sketch" (Maths P1 Nov 2025 4.5, Grade 10 P1 2017 6.1.3; 2026-10-11) a graph sketch: the memo's features placed on a grid, the curve
     drawn live through them.
   - "boxplot" (Maths P2 Nov 2024 2.4, Grade 10 P2 2017 1.4 and 2018 1.5; 2026-10-11) a box and whisker diagram: the five values placed on
     the paper's scaled line, the box and whiskers drawn from them.
   - "numline" (Grade 10 P1 2017 2.1.2; 2026-10-11) an inequality on a number line: its end(s), open or closed dots, and the shading.
   - "venn" (Grade 10 P1 2017 7.2.1, Grade 11 P1 2017 9.1, Maths P1 Nov 2024 11.1; 2026-10-11) a Venn diagram: the number (or the form in
     the unknown, x − 20) in each region of two or three circles. VT_V marks this file's Venn and tree builders.
   - "tree" (Grade 11 P1 2017 8.1.1 and 2018 8.2; 2026-10-11) a probability tree: on each drawn branch its outcome and its probability (a
     fraction or a decimal), and each end's outcome.
   - "plot" (Grade 10/11 Physical Sciences, Grade 11 Maths P2, ML P1 Nov 2024; 2026-10-11) a graph plotted from data: the axes' labels and
     the scale chosen where the memo marks them, each data point placed on the grid, then the line (a straight line of best fit, a smooth
     curve or the points joined), extended to the axis where asked; or a straight line drawn on a given graph (a tangent). PLOT_V marks it.
   - "forces" (Grade 11 and 12 Physical Sciences P1; 2026-10-11) a free-body (or vector) diagram: forces from the same tray of seven, each
     aimed from the dot by a tap (or dragged, or turned with the arrow keys), and an angle between two lines where asked. FORCE_V marks it.
   The host (Exam Practice) owns the ANSWER (its state, so Check, marking and "same answer" work as for every other type); this
   module owns only its DOM and its step. Nothing offers "draw it on paper" (Murci 2026-10-11: every drawing part is built on screen).

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
  // (the axis-label choices are listed SORTED: the config keeps the right one first, which a learner could read as the answer)
  // (2026-10-11, the plot builder's agent) a part may use only some steps (`use`: Maths P2 Nov 2025 2.1.3 marks the bars and "no gaps",
  // on the answer book's given axes and scale: Type and Plot; `step` the given scale, `axes` the given labels, `typeOpts` the type
  // choices' words, `pmin` how many right bars earn P's first mark); and a STACKED bar may be completed (`stack`, ML P1 Nov 2025 3.2.3:
  // each bar's printed parts drawn, the learner drags its new part up from their top and chooses its shading from the key). No "drew it
  // on paper" link any more (Murci 2026-10-11: "on paper" is never shown; every drawing part is built on screen)
  let hsN = 0;
  function hist(host, o) {
    const cfg = o.cfg, ALL = ["Type", "Caption", "Axes", "Scale", "Plot"], STEPS = Array.isArray(cfg.use) && cfg.use.length ? ALL.filter(s => cfg.use.indexOf(s) !== -1) : ALL;
    const ST = cfg.stack && Array.isArray(cfg.stack.base) ? cfg.stack : null, uid = "hs" + (++hsN);
    const lo = k => ST ? ST.base[k][ST.base[k].length - 1] : 0;   // where a bar's drag starts: 0, or the top of its printed parts
    const blank = () => Object.assign({ type: "", cap: "", xl: "", yl: "", step: 0, v: cfg.groups.map((_, k) => lo(k)) }, ST ? { sh: cfg.groups.map(() => -1) } : {});
    let v = Object.assign(blank(), clone(o.value));
    let i = 0, locked = false, chips = "", drag = false;   // drag: a bar is held (sync waits; a redraw would drop it)
    const set = patch => { v = Object.assign(v, patch); o.onChange(clone(v)); };
    const done = k => { const s = STEPS[k]; return s === "Type" ? !!v.type : s === "Caption" ? v.cap.trim().length > 5 : s === "Axes" ? !!(v.xl && v.yl) : s === "Scale" ? !!v.step
      : ST ? cfg.groups.every((_, j) => v.v[j] > lo(j) && v.sh[j] >= 0) : v.v.some(x => x > 0); };
    const stepOf = () => v.step || cfg.step || cfg.steps[1];
    const max = () => { const st = stepOf(); return Math.ceil(cfg.top / st) * st; };
    const num = n => String(Math.round(n * 1000) / 1000).replace(".", ",").replace(/^(\d+)/, d => d.replace(/\B(?=(\d{3})+(?!\d))/g, " "));
    // a stacked part's fill: the key's (hatched / white / black, as the paper prints them, in both themes)
    const fill = j => ST ? ` class="bp-s bp-f-${esc(ST.fill[j] || "white")}"${ST.fill[j] === "hatch" ? ` fill="url(#${uid}h)"` : ""}` : "";
    function chart() {
      const st = stepOf(), mx = max(), labs = []; for (let t = 0; t <= mx + 1e-9; t += st) labs.push(t);
      // (the left margin holds the longest number: "60 000 000" ran into the axis at 48)
      const X0 = Math.max(48, 12 + Math.max(...labs.map(t => num(t).length)) * 5.2), X1 = 292, Y0 = 180, Y1 = 14, w = (X1 - X0) / cfg.groups.length;
      const gap = ST ? Math.max(12, w - 64) : v.type === "bar" ? 12 : 0;
      const y = n => Y0 - (n / mx) * (Y0 - Y1); let g = "", b = "";
      if (cfg.minor > 0) for (let t = cfg.minor; t < mx - 1e-9; t += cfg.minor) if (Math.abs(t / st - Math.round(t / st)) > 1e-6) g += `<line x1="${X0}" x2="${X1}" y1="${y(t)}" y2="${y(t)}" class="bp-grid bp-minor"/>`;
      labs.forEach(t => { g += `<line x1="${X0}" x2="${X1}" y1="${y(t)}" y2="${y(t)}" class="bp-grid"/><text x="${X0 - 5}" y="${y(t) + 3}" class="bp-tick" text-anchor="end">${num(t)}</text>`; });
      v.v.forEach((n, k) => { const x = X0 + k * w + gap / 2, bw = w - gap;
        if (ST) { let y0 = 0; ST.base[k].forEach((top, j) => { b += `<rect x="${x}" y="${y(top)}" width="${bw}" height="${Math.max(0, y(y0) - y(top))}"${fill(j)}/>`; y0 = top; });
          if (n > lo(k)) b += `<rect x="${x}" y="${y(n)}" width="${bw}" height="${y(lo(k)) - y(n)}"${v.sh[k] >= 0 ? fill(v.sh[k]) : ' class="bp-s bp-sx"'}/>`; }
        else if (v.type !== "line") b += `<rect x="${x}" y="${y(n)}" width="${bw}" height="${Y0 - y(n)}" class="bp-barr"/>`;
        b += `<g class="bp-h" data-k="${k}" tabindex="${locked ? -1 : 0}" role="slider" aria-label="${esc(cfg.groups[k])}${ST ? ": the top of the new part" : " " + esc(cfg.unit || "years")}" aria-valuemin="${lo(k)}" aria-valuemax="${mx}" aria-valuenow="${n}" aria-valuetext="${num(n)}">`
          + (v.type === "line" && !ST ? `<circle cx="${x + bw / 2}" cy="${y(n)}" r="7" class="bp-knob"/>` : `<rect x="${x + bw / 2 - 15}" y="${y(n) - 7}" width="30" height="14" rx="7" class="bp-knob"/>`)
          + `<rect x="${x}" y="${Math.min(y(n) - 18, Y0 - 30)}" width="${bw}" height="40" fill="transparent"/></g>`
          + `<text x="${x + bw / 2}" y="${y(n) - 12}" class="bp-val" text-anchor="middle">${n > lo(k) ? num(n) : ""}</text>`
          + `<text x="${X0 + k * w + w / 2}" y="${Y0 + 21}" class="bp-tick" text-anchor="middle">${esc(cfg.groups[k])}</text>`; });
      if (v.type === "line" && !ST) b = `<polyline points="${v.v.map((n, k) => (X0 + k * w + w / 2) + "," + y(n)).join(" ")}" class="bp-line"/>` + b;
      // the axes' names: the learner's choice where the Axes step is used, else the paper's (`axes`)
      const AXS = STEPS.indexOf("Axes") !== -1 ? null : cfg.axes || ["", ""], xl = AXS ? AXS[0] : v.xl || "X-axis label?", yl = AXS ? AXS[1] : v.yl ? v.yl.replace(/ \(per .*\)$/, "") : "Y-axis label?";
      return `<svg class="bp-chart" viewBox="0 0 300 223" aria-label="Your graph">`
        + (ST ? `<defs><pattern id="${uid}h" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" class="bp-hb"/><line x1="0" y1="0" x2="0" y2="5" class="bp-hl"/></pattern></defs>` : "")
        + `<line x1="${X0}" y1="${Y0}" x2="${X1}" y2="${Y0}" class="bp-axis"/><line x1="${X0}" y1="${Y0}" x2="${X0}" y2="${Y1}" class="bp-axis"/>${g}${b}`
        + `<text x="170" y="220" class="bp-alab" text-anchor="middle">${esc(xl)}</text>`
        + `<text transform="translate(10,98) rotate(-90)" class="bp-alab" text-anchor="middle">${esc(yl)}</text></svg>`;
    }
    // a stacked bar's key (the paper's) and each bar's new part's shading
    const sw = j => `<i class="bp-sw bp-f-${esc(ST.fill[j] || "white")}" aria-hidden="true"></i>`;
    const shades = () => `<div class="bp-key" aria-hidden="true">${ST.series.map((s, j) => `<span>${sw(j)}${esc(s)}</span>`).join("")}</div>`
      + cfg.groups.map((g, k) => `<div class="bp-grp" role="group" aria-label="${esc(g)}: the shading of its new part"><p class="bp-q">${esc(g)}: shade the new part as</p>`
        + `<div class="bp-opts bp-shades">${ST.series.map((s, j) => `<button type="button" class="bp-opt bp-shade" data-sh="${k}:${j}" aria-pressed="${v.sh[k] === j}"${locked ? " disabled" : ""}>${sw(j)}<span>${esc(s)}</span></button>`).join("")}</div></div>`).join("");
    function body() {
      const s = STEPS[i];
      // (typeOpts: the paper's own words for the choice; typeHint "" shows none: "a histogram's bars touch" answered 2.1.3's "no gaps")
      if (s === "Type") return `<div class="bp-grp"><p class="bp-q">${esc(cfg.typeQ || "Which graph shows age GROUPS against a number?")}</p><div class="bp-opts">`
        + (Array.isArray(cfg.typeOpts) && cfg.typeOpts.length ? cfg.typeOpts : [["histogram", "Histogram"], ["bar", "Bar graph"], ["line", "Line graph"]]).map(([k, t]) =>
          `<button type="button" class="bp-opt" data-type="${esc(k)}" aria-pressed="${v.type === k}">${ICON[k] || ""}<span>${esc(t)}</span></button>`).join("") + `</div></div>`
        + (cfg.typeHint === "" ? "" : `<p class="bp-hint">${esc(cfg.typeHint || "A histogram's bars touch: its groups run on with no gaps.")}</p>`);
      if (s === "Caption") return `<div class="bp-grp"><label class="bp-q" for="bp-cap">The caption: name BOTH variables</label>`
        + `<textarea id="bp-cap" class="bp-in" rows="2" maxlength="160" placeholder="The number of … in different …" autocapitalize="off" spellcheck="false">${esc(v.cap)}</textarea></div>`
        + `<p class="bp-hint">What changes along the bottom, and what was counted.</p>`;
      if (s === "Axes") return `<div class="bp-grp"><label class="bp-q" for="bp-x">The X-axis (along the bottom)</label><select id="bp-x" class="bp-in"><option value="">Choose…</option>${[...cfg.x].sort().map(t => `<option${v.xl === t ? " selected" : ""}>${esc(t)}</option>`).join("")}</select></div>`
        + `<div class="bp-grp"><label class="bp-q" for="bp-y">The Y-axis (up the side)</label><select id="bp-y" class="bp-in"><option value="">Choose…</option>${[...cfg.y].sort().map(t => `<option${v.yl === t ? " selected" : ""}>${esc(t)}</option>`).join("")}</select></div>`;
      if (s === "Scale") return `<div class="bp-grp"><p class="bp-q">The Y-axis goes up in steps of</p><div class="bp-opts">${cfg.steps.map(s => `<button type="button" class="bp-opt" data-step="${s}" aria-pressed="${v.step === s}">${s}</button>`).join("")}</div></div>${chart()}`;
      return chart() + (ST ? shades() + `<p class="bp-hint">Drag each bar's new part up to its value (arrow keys work too), then choose its shading from the key.</p>`
        : `<p class="bp-hint">Drag each bar to its value (arrow keys work too). The table is in the shared information.</p>`);
    }
    function draw(keepFocus) {
      const a = keepFocus && document.activeElement && host.contains(document.activeElement) ? document.activeElement : null, f = a ? a.dataset.k : null, fs = a ? a.dataset.sh : null;
      const last = i >= STEPS.length - 1;
      host.innerHTML = `<div class="bp" data-locked="${locked}">` + (STEPS.length > 1 ? `<div class="bp-steps" style="grid-template-columns:repeat(${STEPS.length}, minmax(0, 1fr))">${STEPS.map((s, k) =>
        `<button type="button" class="bp-step" data-i="${k}" aria-current="${k === i ? "step" : "false"}" data-done="${done(k) && k !== i}"><span class="sr-only">Step ${k + 1}: </span>${s}${done(k) && k !== i ? '<span class="sr-only">, done</span>' : ""}</button>`).join("")}</div>` : "")
        + `<div class="bp-body">${body()}</div>${chips}`
        + (last ? "" : `<div class="bp-foot"><button type="button" class="nxb nxb-sec nxb-sm bp-next">Next step</button><span></span></div>`) + `</div>`;
      wire(); if (f != null) { const n = host.querySelector(`.bp-h[data-k="${f}"]`); if (n) n.focus({ preventScroll: true }); }
      if (fs != null) { const n = host.querySelector(`[data-sh="${fs}"]`); if (n) n.focus({ preventScroll: true }); }
    }
    function wire() {
      const q = s => host.querySelectorAll(s), off = () => locked;
      q(".bp-step").forEach(b => b.onclick = () => { i = +b.dataset.i; draw(); });
      q("[data-type]").forEach(b => b.onclick = () => { if (off()) return; set({ type: b.dataset.type }); draw(); });
      q("[data-step]").forEach(b => b.onclick = () => { if (off()) return; set({ step: +b.dataset.step }); draw(); });
      q("[data-sh]").forEach(b => b.onclick = () => { if (off()) return; const [k, j] = b.dataset.sh.split(":").map(Number), sh = v.sh.slice(); sh[k] = j; set({ sh: sh }); draw(true); });
      const cap = host.querySelector("#bp-cap"), ci = STEPS.indexOf("Caption");
      if (cap) { cap.disabled = locked; cap.oninput = e => { set({ cap: e.target.value }); const sb = host.querySelectorAll(".bp-step")[ci]; if (sb) sb.dataset.done = "false"; }; }
      const xs = host.querySelector("#bp-x"), ys = host.querySelector("#bp-y");
      if (xs) { xs.disabled = ys.disabled = locked; xs.onchange = e => set({ xl: e.target.value }); ys.onchange = e => set({ yl: e.target.value }); }
      const nx = host.querySelector(".bp-next"); if (nx) nx.onclick = () => { i++; draw(); const b = host.querySelector(".bp-body"); if (b) b.scrollIntoView({ block: "nearest" }); };
      const ch = host.querySelector(".bp-chart"); if (!ch || STEPS[i] !== "Plot" || locked) return;
      let k = -1; const mx = max();
      const at = e => { const r = ch.getBoundingClientRect(), yy = (e.clientY - r.top) * 223 / r.height; const sn = cfg.snap || 10; return Math.max(lo(k), Math.min(mx, Math.round((180 - yy) / 166 * mx / sn) * sn)); };
      const put = (kk, n) => { const a = v.v.slice(); a[kk] = n; set({ v: a }); };
      // (a drag repaints the svg's CHILDREN only: rebuilding the svg would drop the pointer capture, and a finger that slid past the
      // chart's edge would stop moving the bar)
      const paint = () => { const t = document.createElement("div"); t.innerHTML = chart(); ch.innerHTML = t.firstElementChild.innerHTML; };
      ch.onpointerdown = e => { const h = e.target.closest(".bp-h"); if (!h) return; k = +h.dataset.k; drag = true; document.documentElement.classList.add("bp-drag"); ch.setPointerCapture(e.pointerId); put(k, at(e)); paint(); e.preventDefault(); };
      ch.onpointermove = e => { if (k < 0) return; const n = at(e); if (n !== v.v[k]) { put(k, n); paint(); } };
      const end = () => { if (k < 0) return; const kk = k; k = -1; drag = false; document.documentElement.classList.remove("bp-drag"); o.onChange(clone(v)) /* one more update: the host reveals its Check now the bar is let go */; draw(); const n = host.querySelector(`.bp-h[data-k="${kk}"]`); if (n) n.focus({ preventScroll: true }); };
      ch.onpointerup = end; ch.onpointercancel = end;
      q(".bp-h").forEach(h => h.onkeydown = e => { const sn = cfg.snap || 10, d = { ArrowUp: sn, ArrowRight: sn, ArrowDown: -sn, ArrowLeft: -sn, PageUp: 5 * sn, PageDown: -5 * sn }[e.key];
        if (d == null) return; e.preventDefault(); const kk = +h.dataset.k; put(kk, Math.max(lo(kk), Math.min(mx, v.v[kk] + d))); draw(true); });
    }
    draw();
    // a stacked bar's chips name its bar: "KwaZulu-Natal: its end", "KwaZulu-Natal: completed"
    const stackLabels = () => Object.fromEntries(cfg.groups.flatMap((g, k) => [["E" + k, g + ": its end"], ["F" + k, g + ": completed"]]));
    return { sync(s) { const nv = Object.assign(blank(), clone(s.value));
        const changed = JSON.stringify(nv) !== JSON.stringify(v), was = locked + chips; v = nv; locked = !!s.locked;
        chips = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? chipRow(s.items, ST ? stackLabels() : cfg.labels || LABELS.hist) : "";
        if (changed && !Object.keys(s.value || {}).length) i = 0;   // a fresh try (Practise again / a retake) starts at step 1
        if ((changed || was !== locked + chips) && !drag) draw(true); },
      destroy() { document.documentElement.classList.remove("bp-drag"); host.innerHTML = ""; } };
  }

  // ── the stems
  function stems(host, o) {
    const cfg = o.cfg, SH = [["left", "bends left"], ["up", "grows straight up"], ["right", "bends right"], ["none", "no growth"]];
    let v = clone(o.value), locked = false, chips = "";
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
        + `<p class="bp-hint">Tap how each stem looks after five days.</p>${chips}</div>`;   // (no "drew it on paper": Murci 2026-10-11)
      host.querySelectorAll(".bp-sh").forEach(b => b.onclick = () => { if (locked) return; v[b.dataset.id] = b.dataset.s; o.onChange(clone(v)); draw();
        const n = host.querySelector(`.bp-sh[data-id="${b.dataset.id}"][data-s="${b.dataset.s}"]`); if (n) n.focus({ preventScroll: true }); });
    }
    draw();
    return { sync(s) { const nv = clone(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v), was = locked + chips; v = nv; locked = !!s.locked;
        chips = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? chipRow(s.items, cfg.labels || Object.fromEntries(cfg.stems.map(st => [st.id, "Stem " + st.id]))) : "";
        if (changed || was !== locked + chips) draw(); },
      destroy() { host.innerHTML = ""; } };
  }

  // ── genetics (LS P2 Nov 2025 2.3.3(b), 2.4.2, 2.5.4; mockup 2026-10-06): SOCKETS filled from a TRAY. Tap a socket, then a tray item;
  // or just tap tray items, each filling the next empty socket of its kind in reading order. A filled socket tapped empties and stays
  // chosen. The alleles are the paper's own tokens (Iᴮ, Xʰ ...), never typed, so case and superscripts are exact: DD is never dd.
  // The answer is a flat map, socket id -> token (ratio numbers as numbers): the marker reads it, nothing is derived on the phone.
  // an allele token's superscript, DRAWN: the data keeps the paper's Unicode modifier letters (exact to compare), but Sora has no
  // glyph for them and the fallback drew Iᴬ and Iᴮ 13 px wide, the A and B unreadable; shown as a real <sup>, spoken "superscript B"
  const SUP = "ᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁᵂᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ", PLAIN = "ABDEGHIJKLMNOPRTUWabcdefghijklmnoprstuvwxyz";
  const supRun = new RegExp("[" + SUP + "]+", "g"), plain = r => [...r].map(c => PLAIN[[...SUP].indexOf(c)]).join("");
  const tok = s => esc(s).replace(supRun, r => `<sup class="gx-sup">${plain(r)}</sup>`);
  const spoken = s => String(s == null ? "" : s).replace(supRun, r => " superscript " + plain(r));
  function sockets(host, o, spec) {
    // spec: ids [[id, kind, aria name]] in reading order; view(v, S, N) -> html; tray { kind: [tokens] }; trayName { kind }; labels
    let v = clone(o.value), act = "", locked = false, chips = "";
    const kindOf = id => (spec.ids.find(x => x[0] === id) || [])[1];
    // the next empty socket of a kind: FORWARD only (a learner working down the cross is never sent back up), and a kind listed in
    // spec.within stays in its own group (the parents' two phenotypes do not chain on to the offspring's, at the bottom)
    const nextEmpty = (kind, after) => { const L = spec.ids, i = L.findIndex(x => x[0] === after), hit = L.slice(i + 1).find(x => x[1] === kind && !v[x[0]]);
      return hit && (i < 0 || (spec.within || []).indexOf(kind) === -1 || hit[3] === L[i][3]) ? hit[0] : ""; };
    const S = (id, cls) => { const x = spec.ids.find(y => y[0] === id), val = v[id] || "";
      return `<button type="button" class="gx-s${cls ? " " + cls : ""}" data-sock="${id}" data-k="${x[1]}" data-f="${!!val}" aria-pressed="${act === id}"`
        + ` aria-label="${esc(x[2])}${val ? ": " + esc(spoken(val)) : ", empty"}"${locked ? " disabled" : ""}>${val ? tok(val) : spec.empty && spec.empty[x[1]] ? `<span class="gx-pl">${spec.empty[x[1]]}</span>` : ""}</button>`; };
    const N = id => locked ? `<span class="gx-n"><output class="gx-nv">${v[id] || "–"}</output></span>`   // (closed: the number alone, no dead steppers)
      : `<span class="gx-n" role="group" aria-label="How many"><button type="button" class="gx-nb" data-n="${id}" data-d="-1" aria-label="One fewer">−</button>`
      + `<output class="gx-nv" aria-live="polite">${v[id] || "–"}</output><button type="button" class="gx-nb" data-n="${id}" data-d="1" aria-label="One more">+</button></span>`;
    const set = () => o.onChange(clone(v));
    function draw(focus) {
      const kind = act ? kindOf(act) : spec.first;
      host.innerHTML = `<div class="bp gx" data-locked="${locked}">${spec.view(v, S, N, locked)}${chips}`
        + (locked ? "" : `<div class="gx-tray" role="group" aria-label="${esc(spec.trayName[kind])}"><p class="gx-th">${esc(spec.trayName[kind])}</p>`
          + `<div class="gx-ti">${spec.tray[kind].map(t => `<button type="button" class="gx-t" data-kind="${kind}" data-t="${esc(t)}" aria-label="${esc(spoken(t))}">${tok(t)}</button>`).join("")}</div></div>`) + `</div>`;
      host.querySelectorAll("[data-sock]").forEach(b => b.onclick = () => { if (locked) return; const id = b.dataset.sock;
        if (v[id]) { delete v[id]; set(); act = id; } else act = act === id ? "" : id; draw(id); });
      host.querySelectorAll("[data-t]").forEach(b => b.onclick = () => { if (locked) return; const kind = b.dataset.kind, id = act && kindOf(act) === kind ? act : nextEmpty(kind, "");
        if (!id) return; v[id] = b.dataset.t; set(); act = nextEmpty(kind, id); draw(); const n = host.querySelector(`[data-kind="${kind}"][data-t="${b.dataset.t}"]`); if (n) n.focus({ preventScroll: true }); });
      host.querySelectorAll("[data-n]").forEach(b => b.onclick = () => { if (locked) return; const id = b.dataset.n, n = Math.max(0, Math.min(4, (v[id] || 0) + +b.dataset.d));
        if (n) v[id] = n; else delete v[id]; set(); draw(); const f = host.querySelector(`[data-n="${id}"][data-d="${b.dataset.d}"]`); if (f) f.focus({ preventScroll: true }); });
      if (focus) { const n = host.querySelector(`[data-sock="${focus}"]`); if (n) n.focus({ preventScroll: true }); }
    }
    draw();
    return { sync(s) { const nv = clone(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v), was = locked + chips; v = nv; locked = !!s.locked; if (locked) act = "";
        chips = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? chipRow(s.items, o.cfg.labels || spec.labels) : "";
        if (changed && !Object.keys(nv).length) act = "";   // a fresh try starts with no socket chosen
        if (changed || was !== locked + chips) draw(); },
      destroy() { host.innerHTML = ""; } };
  }
  // a genotype question: `count` genotypes of two alleles each, from the paper's alleles (2.4.2: Iᴬ Iᴮ i, two genotypes)
  // per: alleles per genotype, 2 (Dd) or 4 (a dihybrid's RRee, LS P2 Nov 2024 1.5.3(a), 2026-10-09); socket ids g<k>a, b, c, d
  function geno(host, o) {
    const cfg = o.cfg, n = cfg.count || 1, per = cfg.per === 4 ? 4 : 2, ids = [], ORD = ["first", "second", "third", "fourth"];
    for (let k = 0; k < n; k++) for (let j = 0; j < per; j++) ids.push(["g" + k + "abcd"[j], "al", (n > 1 ? "Genotype " + (k + 1) : "Genotype") + ", " + ORD[j] + " allele"]);
    return sockets(host, o, { ids: ids, first: "al", tray: { al: cfg.alleles }, trayName: { al: "Alleles: tap one" },
      labels: Object.fromEntries(Array.from({ length: n }, (_, k) => ["g" + k, n > 1 ? "Genotype " + (k + 1) : "Genotype"])),
      view: (v, S) => Array.from({ length: n }, (_, k) => `<div class="gx-g"><span class="gx-k">${n > 1 ? "Genotype " + (k + 1) : "Genotype"}</span>${Array.from({ length: per }, (_, j) => S("g" + k + "abcd"[j])).join("")}</div>`).join("") });
  }
  // a monohybrid cross (2.5.4), laid out as the memo marks it: P1 phenotypes and genotypes, the gametes on a Punnett square's edges,
  // its cells the F1 genotypes, then the F1 phenotypes and their ratio. The four labels (P1, Meiosis, Fertilisation, F1) are placed by
  // the learner on the rail: the memo marks them, so printing them would give two marks away. The memo also accepts gamete and
  // fertilisation LINES instead of a square; the square is the one layout here (the same two marks).
  function cross(host, o) {
    const cfg = o.cfg, nf = Math.min(3, cfg.phenos.length), al = "al", ph = "ph", lab = "lab";
    // the generations as the paper names them (LS P2 Nov 2024 2.4.4 crosses parents 5 and 6: its memo marks "P2 and F2"), default P1 / F1
    const gen = Array.isArray(cfg.gens) && cfg.gens.length === 2 ? cfg.gens : ["P1", "F1"];
    const ids = [["L0", lab, "Label for the parents' row"], ["P0", ph, "First parent's phenotype", "P"], ["P1", ph, "Second parent's phenotype", "P"],
      ["G00", al, "First parent's genotype, first allele"], ["G01", al, "First parent's genotype, second allele"],
      ["G10", al, "Second parent's genotype, first allele"], ["G11", al, "Second parent's genotype, second allele"],
      ["L1", lab, "Label for the gametes"], ["T0", al, "Gamete, top edge, first"], ["T1", al, "Gamete, top edge, second"],
      ["S0", al, "Gamete, side edge, first"], ["S1", al, "Gamete, side edge, second"], ["L2", lab, "Label for the square's cells"]];
    ["00", "01", "10", "11"].forEach(rc => ids.push(["C" + rc + "a", al, "Offspring, row " + (+rc[0] + 1) + " column " + (+rc[1] + 1) + ", first allele"],
      ["C" + rc + "b", al, "Offspring, row " + (+rc[0] + 1) + " column " + (+rc[1] + 1) + ", second allele"]));
    ids.push(["L3", lab, "Label for the offspring's row"]);
    for (let k = 0; k < nf; k++) ids.push(["F" + k, ph, "Offspring phenotype " + (k + 1), "F"]);
    const cell = (S, rc) => `<td class="gx-cell">${S("C" + rc + "a")}${S("C" + rc + "b")}</td>`;
    return sockets(host, o, { ids: ids, first: al, within: [ph], empty: { ph: "phenotype", lab: "label" },   // (a blank dashed pill said nothing at 360 px)
      tray: { al: cfg.alleles, ph: [...cfg.phenos].sort(), lab: [gen[1], "Fertilisation", "Meiosis", gen[0]].sort() },   // (sorted: a paper's order could read as the answer)
      trayName: { al: "Alleles: tap one", ph: "Phenotypes: tap one", lab: "Labels: tap one" },
      labels: { P: gen[0] + " phenotypes", G: gen[0] + " genotypes", M: "Gametes", F: gen[1] + " genotypes", Ph: gen[1] + " phenotypes", R: "Ratio (compulsory)", L1: gen[0] + " and " + gen[1], L2: "Meiosis and fertilisation" },
      view: (v, S, N, locked) => `<div class="gx-x">`
        + `<div class="gx-r">${S("L0", "gx-lab")}<div class="gx-c"><span class="gx-k">Phenotype</span><div class="gx-pair">${S("P0", "gx-ph")}<b class="gx-by" aria-hidden="true">×</b>${S("P1", "gx-ph")}</div></div></div>`
        + `<div class="gx-r"><span></span><div class="gx-c"><span class="gx-k">Genotype</span><div class="gx-pair"><span class="gx-gt">${S("G00")}${S("G01")}</span><b class="gx-by" aria-hidden="true">×</b><span class="gx-gt">${S("G10")}${S("G11")}</span></div></div></div>`
        + `<div class="gx-r">${S("L1", "gx-lab")}<div class="gx-c"><span class="gx-k">Gametes</span><span class="gx-hint">on the square's edges</span></div></div>`
        + `<div class="gx-r">${S("L2", "gx-lab")}<table class="gx-pq"><tr><td class="gx-x0" aria-hidden="true">×</td><td>${S("T0")}</td><td>${S("T1")}</td></tr>`
        + `<tr><td>${S("S0")}</td>${cell(S, "00")}${cell(S, "01")}</tr><tr><td>${S("S1")}</td>${cell(S, "10")}${cell(S, "11")}</tr></table></div>`
        + `<div class="gx-r">${S("L3", "gx-lab")}<div class="gx-c"><span class="gx-k">Phenotypes and how many of each</span>`
        + Array.from({ length: nf }, (_, k) => !locked || v["F" + k] ? `<div class="gx-f">${S("F" + k, "gx-ph")}${v["F" + k] ? N("R" + k) : ""}</div>` : "").join("")
        + ((k => k.length > 1 ? `<p class="gx-ratio">Ratio ${k.map(x => v["R" + x] || "–").join(" : ")}</p>` : "")([0, 1, 2].slice(0, nf).filter(x => v["F" + x])))
        + `</div></div></div>` });
  }

  // ── the graph SKETCH (Murci 2026-10-11 picked mock A of three, "Build it on screen: place the key points; marked online"). "Sketch
  // the graph of f; show the intercepts and the asymptote" BUILT on a grid: a tray holds the features the memo marks (their names, never
  // their positions); tap one, then the grid (it snaps to the step; an asymptote is a line through the tapped value), or drag a placed
  // one; keyboard: Enter on a feature places it, the arrows move it, Delete removes it. The curve is drawn LIVE through what is placed,
  // the family fitted as far as the placed features fix it, nothing before that. The answer is the positions, plus the SHAPE word of
  // the curve the learner's own points make (or chose, where the memo's features leave it open, e.g. one intercept + an asymptote):
  // the marker reads only those, never the fit.
  //   cfg   { family, x: [min, max, step], y: [min, max, step], domain?: [x0, x1], features: [{ id, kind: "point" | "hline" | "vline",
  //           label, graph?, turn? }], shape?: { label, pick?: [words] }, b?, graphs?: [{ id, family, label, b?, domain?, shape? }] }
  //           (trig x in degrees, b the period factor the stem's equation prints; graphs: two graphs on one set of axes, each feature
  //           naming its graph)
  //   value { p: { featureId: [x, y] (a point) | number (a line's value) }, pick: { graphId: word }, s: { graphId: shape word(s) } }
  const SKD = Math.PI / 180, TRIG = { sin: 1, cos: 1, tan: 1 };
  const FAMN = { parabola: "parabola", hyperbola: "hyperbola", exponential: "exponential graph", log: "log graph", cubic: "cubic graph",
    line: "straight line", sin: "sine graph", cos: "cosine graph", tan: "tan graph" };
  const skNum = (n, deg) => { const r = Math.round(n * 100) / 100; return (r < 0 ? "−" : "") + String(Math.abs(r)).replace(".", ",") + (deg ? "°" : ""); };
  // least squares, rows [c1 .. cn, rhs]: { x, rank, res } (columns scaled first, so the rank test is relative; a free unknown is 0)
  function lsq(rows, n) {
    const sc = Array.from({ length: n }, (_, j) => Math.sqrt(rows.reduce((t, r) => t + r[j] * r[j], 0)) || 1);
    const M = Array.from({ length: n }, () => new Array(n + 1).fill(0));
    rows.forEach(r => { for (let i = 0; i < n; i++) { const ri = r[i] / sc[i]; for (let j = 0; j < n; j++) M[i][j] += ri * r[j] / sc[j]; M[i][n] += ri * r[n]; } });
    const piv = []; let row = 0;
    for (let c = 0; c < n && row < n; c++) {
      let best = row; for (let r = row + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[best][c])) best = r;
      if (Math.abs(M[best][c]) < 1e-9) continue;
      const t = M[row]; M[row] = M[best]; M[best] = t;
      for (let r = 0; r < n; r++) if (r !== row && M[r][c]) { const k = M[r][c] / M[row][c]; for (let j = c; j <= n; j++) M[r][j] -= k * M[row][j]; }
      piv.push(c); row++;
    }
    const x = new Array(n).fill(0); piv.forEach((c, r) => { x[c] = M[r][n] / M[r][c] / sc[c]; });
    return { x: x, rank: piv.length, res: rows.reduce((m, r) => Math.max(m, Math.abs(r.slice(0, n).reduce((t, a, j) => t + a * x[j], 0) - r[n])), 0) };
  }
  // one family through the placed features: { f, vas, has, word }, "nofit" (no curve of the family passes through them all), or null
  // (not fixed yet). pts [{ x, y, turn }]; hs / vs the placed asymptotes' values; pick the chosen shape word; R the grid (+ d0 d1 domain)
  function skFamily(fam, pts, hs, vs, pick, R) {
    const k = R.xr / R.yr, eps = 1e-6 * Math.max(1, R.yr);
    if (fam === "line" || fam === "parabola" || fam === "cubic") {
      const n = fam === "line" ? 2 : fam === "parabola" ? 3 : 4, rows = [];
      if (hs.length || vs.length) return "nofit";
      pts.forEach(p => { const r = []; for (let j = n - 1; j >= 0; j--) r.push(Math.pow(p.x, j)); rows.push(r.concat([p.y]));
        if (p.turn && n > 2) { const d = []; for (let j = n - 1; j >= 0; j--) d.push(j ? j * Math.pow(p.x, j - 1) * k : 0); rows.push(d.concat([0])); } });
      if (!rows.length) return null;
      let L = lsq(rows, n);
      // a parabola fixed but for how wide (a turning point alone) takes the chosen opening at a representative width
      if (L.rank === n - 1 && pick && fam === "parabola") { rows.push([1, 0, 0, (pick === "∩" ? -1 : 1) * 4 * R.yr / (R.xr * R.xr)]); L = lsq(rows, n); }
      if (L.rank < n) return null;
      const c = L.x, lead = c[0]; if (n > 2 && Math.abs(lead) < 1e-9) return "nofit";
      return { f: x => c.reduce((t, a) => t * x + a, 0), vas: [], has: [],
        word: fam === "line" ? (lead > 1e-12 ? "positive gradient" : lead < -1e-12 ? "negative gradient" : "horizontal") : fam === "parabola" ? (lead > 0 ? "∪" : "∩") : (lead > 0 ? "positive" : "negative") };
    }
    if (fam === "hyperbola") {   // y = a/(x − p) + q, as the linear xy = K + qx + py (K = a − pq)
      if (pts.some(p => p.turn)) return "nofit";
      const rows = pts.map(p => [1, p.x, p.y, p.x * p.y]).concat(vs.map(t => [0, 0, 1, t]), hs.map(t => [0, 1, 0, t]));
      if (!rows.length) return null;
      let L = lsq(rows, 3);
      if (L.rank === 2 && pick && vs.length && hs.length && !pts.length) { rows.push([1, 0, 0, (pick === "top left and bottom right" ? -1 : 1) * R.xr * R.yr / 32 - vs[0] * hs[0]]); L = lsq(rows, 3); }
      if (L.rank < 3) return null;
      const K = L.x[0], q = L.x[1], p = L.x[2], a = K + p * q; if (Math.abs(a) < 1e-9) return "nofit";
      return { f: x => a / (x - p) + q, vas: [p], has: [q], word: a > 0 ? "top right and bottom left" : "top left and bottom right" };
    }
    if (fam === "exponential") {   // y = a·bˣ + q: the asymptote first, then ln|y − q| is linear in x
      if (!hs.length) return null;
      const q = hs[0]; if (pts.some(p => p.turn || Math.abs(p.y - q) < eps)) return "nofit";
      if (!pts.length) return null;
      const s = Math.sign(pts[0].y - q); if (pts.some(p => Math.sign(p.y - q) !== s)) return "nofit";
      const rows = pts.map(p => [1, p.x, Math.log(Math.abs(p.y - q))]);
      let L = lsq(rows, 2);
      if (L.rank === 1 && pick) { rows.push([0, 1, (pick === "decreasing" ? -1 : 1) * s * Math.LN2]); L = lsq(rows, 2); }
      if (L.rank < 2) return null;
      const A = s * Math.exp(L.x[0]), B = L.x[1]; if (Math.abs(B) < 1e-9) return "nofit";
      return { f: x => A * Math.exp(B * x) + q, vas: [], has: [q], word: (s * B > 0 ? "increasing" : "decreasing") + ", " + (s > 0 ? "above" : "below") };
    }
    if (fam === "log") {   // y = k·ln(x − p) + q: the asymptote first
      if (!vs.length) return null;
      const p = vs[0]; if (pts.some(t => t.turn || t.x <= p + 1e-9)) return "nofit";
      if (!pts.length) return null;
      const rows = pts.map(t => [Math.log(t.x - p), 1, t.y]);
      let L = lsq(rows, 2);
      if (L.rank === 1 && pick) { rows.push([1, 0, (pick === "decreasing" ? -1 : 1) / Math.LN2]); L = lsq(rows, 2); }
      if (L.rank < 2) return null;
      const K = L.x[0], q = L.x[1]; if (Math.abs(K) < 1e-9) return "nofit";
      return { f: x => x > p ? K * Math.log(x - p) + q : NaN, vas: [p], has: [], word: K > 0 ? "increasing" : "decreasing" };
    }
    // y = a·s(b(x − p)) + q: the graph's own b (the stem prints the equation, "cos 2x + 1", so the period is no answer; without it, sin x − 1's
    // (0 ; −1), (90° ; 0), (270° ; −2) fit −sin 3x − 1 as well and the curve never fixed), else every b of a school paper; phase p on half
    // the x step; (a, q) by least squares
    if (TRIG[fam]) {
      const tan = fam === "tan", base = fam === "sin" ? Math.sin : fam === "cos" ? Math.cos : Math.tan;
      const dbase = fam === "sin" ? Math.cos : t => -Math.sin(t);
      if (hs.length || (!tan && vs.length) || (tan && pts.some(p => p.turn))) return "nofit";
      if (!pts.length) return null;
      const fits = []; let free = false;
      (R.b ? [R.b] : [0.5, 1, 1.5, 2, 3, 4]).forEach(b => { const per = (tan ? 180 : 360) / b, ps = R.xstep / 2;
        for (let ph = 0; ph < per - 1e-9; ph += ps) {
          const th = x => b * (x - ph) * SKD;
          if (tan && (vs.some(t => Math.abs(Math.cos(th(t))) > 1e-7) || pts.some(p => Math.abs(Math.cos(th(p.x))) < 1e-7))) continue;
          const rows = []; pts.forEach(p => { rows.push([base(th(p.x)), 1, p.y]); if (p.turn) rows.push([b * SKD * dbase(th(p.x)) * R.xr, 0, 0]); });
          const L = lsq(rows, 2); if (L.res > eps) continue;
          if (L.rank < 2) { free = true; continue; }
          if (Math.abs(L.x[0]) > 1e-9) fits.push({ a: L.x[0], q: L.x[1], b: b, ph: ph });
        } });
      if (free) return null;
      if (!fits.length) return "nofit";
      const fOf = c => x => c.a * base(c.b * (x - c.ph) * SKD) + c.q;
      const vasOf = c => { if (!tan) return []; const out = [], st = 180 / c.b; let x0 = c.ph + 90 / c.b; x0 -= Math.ceil((x0 - R.xmin) / st + 1) * st;
        for (let x = x0; x <= R.xmax + 1e-9; x += st) if (x >= R.xmin - 1e-9) out.push(Math.round(x * 1e6) / 1e6); return out; };
      // every fit must draw the same curve over the domain, or the features do not fix it yet
      const ref = fits[0], fr = fOf(ref), va = vasOf(ref).join();
      for (const c of fits.slice(1)) { if (vasOf(c).join() !== va) return null; const fc = fOf(c);
        for (let i = 0; i <= 96; i++) { const x = R.d0 + (R.d1 - R.d0) * i / 96;
          if (tan && (Math.abs(Math.cos(ref.b * (x - ref.ph) * SKD)) < 0.05 || Math.abs(Math.cos(c.b * (x - c.ph) * SKD)) < 0.05)) continue;
          if (Math.abs(fr(x) - fc(x)) > 1e-3 * R.yr) return null; } }
      return { f: fr, vas: vasOf(ref), has: [], word: tan ? (ref.a * ref.b > 0 ? "increasing" : "decreasing") : "drawn" };
    }
    return null;
  }
  // the family's fit, then the check every family shares: each placed point on the curve (a turning point flat there), each placed line
  // one of its asymptotes
  function skFit(fam, pts, hs, vs, pick, R) {
    const g = skFamily(fam, pts, hs, vs, pick, R); if (!g || g === "nofit") return g;
    const ey = 1e-6 * Math.max(1, R.yr), ex = 1e-6 * Math.max(1, R.xr), h = 1e-4 * R.xr;
    if (pts.some(p => !(Math.abs(g.f(p.x) - p.y) <= ey))) return "nofit";
    if (pts.some(p => p.turn && !(Math.abs(g.f(p.x + h) - g.f(p.x - h)) / (2 * h) * R.xr / R.yr <= 1e-4))) return "nofit";
    if (hs.some(t => !g.has.some(a => Math.abs(a - t) <= ey)) || vs.some(t => !g.vas.some(a => Math.abs(a - t) <= ex))) return "nofit";
    return g;
  }
  let skN = 0;
  function sketch(host, o) {
    const cfg = o.cfg, uid = "sk" + (++skN);
    const GR = cfg.graphs && cfg.graphs.length ? cfg.graphs : [{ id: "f", family: cfg.family, b: cfg.b, domain: cfg.domain, shape: cfg.shape, label: "" }];
    const FE = (cfg.features || []).map(f => Object.assign({}, f, { graph: f.graph || GR[0].id }));
    // two graphs on one set of axes: every feature names its graph (G11 P2 Nov 2017 6.2.3 had two "x-intercept"s and two "turning point"s,
    // f's and g's alike): a badge in the graph's curve colour on its chip, its placed tag or pill and its dot's colour, and " of f" in every
    // name read or announced. A label that already ends in its graph's name ("x-intercept of g") shows without it, beside the badge.
    const TWO = GR.length > 1, gk = f => Math.max(0, GR.findIndex(g => g.id === f.graph)), gName = f => GR[gk(f)].label || GR[gk(f)].id;
    const tail = f => " of " + gName(f), hasTail = f => f.label.length > tail(f).length && f.label.slice(-tail(f).length) === tail(f);
    const nameOf = f => TWO && !hasTail(f) ? f.label + tail(f) : f.label;                    // read and announced: "x-intercept of f"
    const shortOf = f => TWO && hasTail(f) ? f.label.slice(0, -tail(f).length) : f.label;    // on the chip, beside its badge
    const badge = f => TWO ? `<i class="sk-gb" data-g="${gk(f)}" aria-hidden="true">${esc(gName(f))}</i>` : "";
    // a text's width in this builder's font (a canvas measure; the family is read once a render, never during a drag)
    let FONT = "sans-serif", ctx2 = null;
    const tw = (s, size, weight) => { try { ctx2 = ctx2 || document.createElement("canvas").getContext("2d"); ctx2.font = weight + " " + size + "px " + FONT;
      return ctx2.measureText(s).width + 1; } catch (_) { return s.length * size * 0.6; } };
    const BW = TWO ? 18 : 0;   // a badge and its gap
    const deg = GR.some(g => TRIG[g.family]), R0 ={ xmin: cfg.x[0], xmax: cfg.x[1], xstep: cfg.x[2], ymin: cfg.y[0], ymax: cfg.y[1], ystep: cfg.y[2] };
    R0.xr = R0.xmax - R0.xmin; R0.yr = R0.ymax - R0.ymin;
    const normV = val => { const b = { p: {}, pick: {}, s: {} }, x = clone(val); ["p", "pick", "s"].forEach(k => { if (x[k] && typeof x[k] === "object") b[k] = x[k]; }); return b; };
    let v = normV(o.value), locked = false, items = null, drag = null, W = 0, ro = null, pinUp = 0;   // pinUp: when a pin was let go (its click is not a grid tap)
    const placed = id => v.p[id] != null;
    const firstOpen = after => { const i = FE.findIndex(f => f.id === after), L = FE.slice(i + 1).concat(FE.slice(0, i + 1)); return (L.find(f => !placed(f.id)) || {}).id || ""; };
    let act = firstOpen("");
    const fmtX = x => skNum(x, deg), fmtY = y => skNum(y, false);
    const valText = (f, val) => f.kind === "point" ? "(" + fmtX(val[0]) + " ; " + fmtY(val[1]) + ")" : f.kind === "hline" ? "y = " + fmtY(val) : "x = " + fmtX(val);
    const spoken = (f, val) => f.kind === "point" ? "x " + fmtX(val[0]) + ", y " + fmtY(val[1]) : valText(f, val);
    const snap = (u, lo, hi, st) => +(Math.max(lo, Math.min(hi, lo + Math.round((u - lo) / st) * st))).toFixed(9);
    const sx = u => snap(u, R0.xmin, R0.xmax, R0.xstep), sy = u => snap(u, R0.ymin, R0.ymax, R0.ystep);
    // the fit of every graph from what is placed (and the shape word each graph's marked shape reads)
    const fitAll = () => GR.map(g => { const fs = FE.filter(f => f.graph === g.id && placed(f.id)), d = g.domain || [R0.xmin, R0.xmax];
      return skFit(g.family, fs.filter(f => f.kind === "point").map(f => ({ x: v.p[f.id][0], y: v.p[f.id][1], turn: !!f.turn })),
        fs.filter(f => f.kind === "hline").map(f => v.p[f.id]), fs.filter(f => f.kind === "vline").map(f => v.p[f.id]), v.pick[g.id] || "", Object.assign({ d0: d[0], d1: d[1], b: g.b }, R0)); });
    const emit = () => { const F = fitAll(); v.s = {};
      GR.forEach((g, k) => { if (g.shape) v.s[g.id] = F[k] && F[k] !== "nofit" ? F[k].word : (v.pick[g.id] || ""); }); o.onChange(clone(v)); };
    // the grid, as large as the width allows (a phone's whole card), never taller than ~62% of what is in view, so the tray and the grid
    // are seen together: what scrolls it is the card on a tablet (608 px at 820 x 1180: a 588 px grid sat under its own tray), the page
    // under the header and the robot's dock on a phone; past 0.68 flatter, the width gives way instead
    let VH = 0;
    const inView = () => { for (let n = host.parentElement; n && n !== document.body; n = n.parentElement) { const o = getComputedStyle(n).overflowY;
        if ((o === "auto" || o === "scroll") && n.clientHeight > 200 && n.clientHeight < (window.innerHeight || 700) - 40) return n.clientHeight; }
      return (window.innerHeight || 700) - (document.body.classList.contains("nx-compact") ? 210 : 120); };
    function geo() {
      const cx = R0.xr / R0.xstep, cy = R0.yr / R0.ystep, a = Math.max(0.68, Math.min(1.05, cy / cx));
      const h = Math.min(Math.round(W * a), Math.max(220, Math.round(VH * 0.62))), w = Math.min(W, Math.max(240, Math.round(h / 0.68)));
      const ax = Math.max(R0.xmin, Math.min(R0.xmax, 0)), ay = Math.max(R0.ymin, Math.min(R0.ymax, 0));
      const L = ax === R0.xmin ? 38 : 12, B = ay === R0.ymin ? 24 : 12, T = 14, pw = w - L - 22, ph = h - T - B;   // (right: the arrow and "x")
      return { w: w, h: h, L: L, T: T, pw: pw, ph: ph, ax: ax, ay: ay, X: x => L + (x - R0.xmin) / R0.xr * pw, Y: y => T + (R0.ymax - y) / R0.yr * ph };
    }
    // ticks: every step a grid line (while 7 px apart), a label on every k-th step from 0, k the first that leaves room for the text; where
    // that k's labels would print rounded, the first roomy k whose labels are whole numbers (G11 P1 Nov 2018 5.4's y step of 1/3 read
    // "1,33 ; 2,67 ; 3,33" every 2nd step: now every 3rd, 1 ; 2 ; 3), else that k (a step of 0,5 or 22,5° keeps its exact labels)
    const labelEvery = (px, wide, st) => { const K = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 50, 100], i = K.findIndex(k => k * px >= wide), k0 = i < 0 ? K[K.length - 1] : K[i];
      const exact = u => Math.abs(u * 100 - Math.round(u * 100)) < 1e-6, whole = u => Math.abs(u - Math.round(u)) < 1e-6;
      return exact(k0 * st) ? k0 : (K.slice(Math.max(i, 0)).find(k => whole(k * st)) || k0); };
    function svgInner(F, G) {
      const X = G.X, Y = G.Y, x0 = X(G.ax), y0 = Y(G.ay), pxX = G.pw / (R0.xr / R0.xstep), pxY = G.ph / (R0.yr / R0.ystep);
      const wid = s => s.length * 6.3 + 10;
      const kx = labelEvery(pxX, Math.max(wid(fmtX(R0.xmin)), wid(fmtX(R0.xmax))), R0.xstep), ky = labelEvery(pxY, 17, R0.ystep);
      // every number on the axes (and the axes' names, each graph's name) as a box, for the placed points' tags to keep off
      G.ob = []; const box = (s, x, y, anchor, size) => { const w = tw(s, size || 11, 600) + 2; G.ob.push([anchor === "end" ? x - w : anchor === "middle" ? x - w / 2 : x, y - 10, w, 13]); };
      const on = (u, st, kk) => Math.abs(Math.round(u / (st * kk)) * st * kk - u) < 1e-6;
      // (a number a placed point sits on is left out: (0 ; 1)'s dot covered the y-axis' 1, which peeked out beside it)
      const pts = FE.filter(f => f.kind === "point" && placed(f.id)).map(f => v.p[f.id]);
      const underX = x => pts.some(p => Math.abs(p[1] - G.ay) < 1e-9 && Math.abs(p[0] - x) < 1e-9), underY = y => pts.some(p => Math.abs(p[0] - G.ax) < 1e-9 && Math.abs(p[1] - y) < 1e-9);
      let g = "", t = "";
      for (let i = 0; i <= Math.round(R0.xr / R0.xstep); i++) { const x = R0.xmin + i * R0.xstep, lab = on(x, R0.xstep, kx);
        if (pxX >= 7 || lab) g += `<line x1="${X(x).toFixed(1)}" x2="${X(x).toFixed(1)}" y1="${G.T}" y2="${G.T + G.ph}" class="sk-grid${lab ? " sk-grid2" : ""}"/>`;
        if (lab && Math.abs(x) > 1e-9 && !underX(x)) { t += `<text x="${X(x).toFixed(1)}" y="${(y0 + 15).toFixed(1)}" class="sk-tick" text-anchor="middle">${fmtX(x)}</text>`; box(fmtX(x), X(x), y0 + 15, "middle"); } }
      for (let i = 0; i <= Math.round(R0.yr / R0.ystep); i++) { const y = R0.ymin + i * R0.ystep, lab = on(y, R0.ystep, ky);
        if (pxY >= 7 || lab) g += `<line x1="${G.L}" x2="${G.L + G.pw}" y1="${Y(y).toFixed(1)}" y2="${Y(y).toFixed(1)}" class="sk-grid${lab ? " sk-grid2" : ""}"/>`;
        // (a label under the x-axis that would sit on the origin's 0, as −1 did at 360 px, is left out)
        if (lab && Math.abs(y) > 1e-9 && !underY(y) && Math.abs(Y(y) + 4 - (y0 + 15)) >= 13) { t += `<text x="${(x0 - 5).toFixed(1)}" y="${(Y(y) + 4).toFixed(1)}" class="sk-tick" text-anchor="end">${fmtY(y)}</text>`; box(fmtY(y), x0 - 5, Y(y) + 4, "end"); } }
      t += `<text x="${(x0 - 5).toFixed(1)}" y="${(y0 + 15).toFixed(1)}" class="sk-tick" text-anchor="end">0</text>`; box("0", x0 - 5, y0 + 15, "end");
      box("x", G.L + G.pw + 10, y0 + 4, "start", 12.5); box("y", x0 + 7, G.T + 9, "start", 12.5);
      const ax = `<line x1="${G.L}" x2="${G.L + G.pw}" y1="${y0}" y2="${y0}" class="sk-axis"/><path d="M${G.L + G.pw + 7} ${y0}l-8 -4v8z" class="sk-arrow"/>`
        + `<line x1="${x0}" x2="${x0}" y1="${G.T + G.ph}" y2="${G.T}" class="sk-axis"/><path d="M${x0} ${G.T - 7}l-4 8h8z" class="sk-arrow"/>`
        + `<text x="${G.L + G.pw + 10}" y="${y0 + 4}" class="sk-name">x</text><text x="${x0 + 7}" y="${G.T + 9}" class="sk-name">y</text>`;
      // the placed asymptotes (dashed), then each graph's curve, clipped to the grid
      let a = "", c = "";
      FE.forEach(f => { if (!placed(f.id) || f.kind === "point") return; const val = v.p[f.id];
        a += f.kind === "hline" ? `<line x1="${G.L}" x2="${G.L + G.pw}" y1="${Y(val).toFixed(1)}" y2="${Y(val).toFixed(1)}" class="sk-asym"/>`
          : `<line x1="${X(val).toFixed(1)}" x2="${X(val).toFixed(1)}" y1="${G.T}" y2="${G.T + G.ph}" class="sk-asym"/>`; });
      F.forEach((fit, k) => { if (!fit || fit === "nofit") return; const d = GR[k].domain || [R0.xmin, R0.xmax], lo = R0.ymin - R0.yr, hi = R0.ymax + R0.yr, N = 360;
        let p = "", pen = false, px = null, last = null;
        for (let i = 0; i <= N; i++) { const x = d[0] + (d[1] - d[0]) * i / N; let y = fit.f(x);
          if (px != null && fit.vas.some(va => (va - px) * (va - x) <= 0)) pen = false;
          px = x; if (!isFinite(y)) { pen = false; continue; }
          y = Math.max(lo, Math.min(hi, y)); p += (pen ? "L" : "M") + X(x).toFixed(1) + " " + Y(y).toFixed(1); pen = true;
          if (y >= R0.ymin && y <= R0.ymax) last = [x, y]; }
        c += `<path d="${p}" class="sk-curve${k ? " sk-c2" : ""}"/>`;
        if (GR.length > 1 && last) { c += `<text x="${(X(last[0]) - 4).toFixed(1)}" y="${(Y(last[1]) - 7).toFixed(1)}" class="sk-glab${k ? " sk-c2" : ""}" text-anchor="end">${esc(GR[k].label || GR[k].id)}</text>`;
          box(GR[k].label || GR[k].id, X(last[0]) - 4, Y(last[1]) - 7, "end", 12.5); } });
      return `<defs><clipPath id="${uid}c"><rect x="${G.L}" y="${G.T}" width="${G.pw}" height="${G.ph}"/></clipPath></defs>`
        + `<rect x="${G.L}" y="${G.T}" width="${G.pw}" height="${G.ph}" class="sk-bg"/>${g}${ax}${t}<g clip-path="url(#${uid}c)">${a}${c}</g>`;
    }
    const verdict = id => { const it = items && items.find(x => x.key === id); return it ? (it.verdict === "correct" ? "ok" : "bad") : ""; };
    // where each placed point's coordinates go: the first FREE spot round its dot (above-right, above-left, below-right, below-left, above,
    // below, slid a quarter either way, right, left; then a row further out, and further), free meaning inside the plot and on no tag placed
    // before it and no other dot; of the free spots, the one that covers least: an asymptote's pill (6), a number on an axis (2 + up to 4 for
    // how much of it), outside the grid (4), an axis line (1,5), a curve (1 each), a row further out (4 a row: a tag beside its dot over the
    // edge of a number beats one two rows off it). (G11 P2 Nov 2017 6.2.3's "(45° ; 0)" and "(135° ; 0)" ran into each other and Maths P2
    // Nov 2025 7.2's "(112,5° ; 0)" sat on the 45° and 90° ticks: four spots, all taken, were scored together and the least bad kept, even
    // on another tag)
    const TH = 15;   // a tag's height (CSS .sk-tag)
    function tagBoxes(G, F, list, pills) {
      const curves = F.filter(fit => fit && fit !== "nofit"), x0 = G.X(G.ax), y0 = G.Y(G.ay), done = [], H = TH;
      const hit = (a, b, m) => a[0] < b[0] + b[2] + m && b[0] < a[0] + a[2] + m && a[1] < b[1] + b[3] + m && b[1] < a[1] + a[3] + m;
      const over = (a, b) => Math.max(0, Math.min(a[0] + a[2], b[0] + b[2]) - Math.max(a[0], b[0])) * Math.max(0, Math.min(a[1] + a[3], b[1] + b[3]) - Math.max(a[1], b[1])) / (b[2] * b[3]);
      const dots = list.map(p => [p.px - 8, p.py - 8, 16, 16]);
      const cands = p => { const w = p.w, cand = [];
        for (let r = 0; r < 4; r++) { const up = p.py - 10 - H - r * (H + 3), dn = p.py + 10 + r * (H + 3);
          [p.px + 9, p.px - 9 - w].forEach(x => cand.push([x, up, r], [x, dn, r]));
          [p.px - w / 2, p.px - w / 4, p.px - 3 * w / 4].forEach(x => cand.push([x, up, r], [x, dn, r]));
          if (!r) cand.push([p.px + 13, p.py - H / 2, 0], [p.px - 13 - w, p.py - H / 2, 0]); }
        return cand; };
      // what a spot costs but for the tags placed before it (a row further out also keeps over its dot: off to one side as well,
      // "(112,5° ; 0)" read as the tag of the point beside it)
      const cost = (p, n, c, ci) => { const w = p.w, b = [c[0], c[1], w, H]; let s = c[2] * 4 + ci * 0.01 + (c[2] ? 0.5 * Math.abs(b[0] + w / 2 - p.px) / w : 0);
        if (b[0] < 1 || b[0] + w > G.w - 1 || b[1] < 1 || b[1] + H > G.h - 1 || dots.some((d, k) => k !== n && hit(b, d, 0))) s += 1000;
        if (b[0] < G.L || b[0] + w > G.L + G.pw || b[1] < G.T || b[1] + H > G.T + G.ph) s += 4;
        (G.ob || []).forEach(q => { const f = over(b, q); if (f > 0) s += 2 + 4 * f; }); pills.forEach(q => { if (hit(b, q, 1)) s += 6; });
        if (b[0] < x0 + 1 && b[0] + w > x0 - 1) s += 1.5; if (b[1] < y0 + 1 && b[1] + H > y0 - 1) s += 1.5;
        curves.forEach(fit => { for (let i = 0; i <= 8; i++) { const X = b[0] + w * i / 8, Y = G.Y(fit.f(R0.xmin + (X - G.L) / G.pw * R0.xr)); if (isFinite(Y) && Y >= b[1] - 2 && Y <= b[1] + H + 2) { s += 1; break; } } });
        return s; };
      // the most hemmed-in tag first (the fewest good spots beside its dot): at the grid's edge "(112,5° ; 0)" has one side, and took the
      // row above its neighbour's tag when "(22,5° ; 0)", in the open, had placed first on the spot it needed
      const ease = list.map((p, n) => cands(p).filter((c, ci) => !c[2] && cost(p, n, c, ci) < 2).length);
      const out = [];
      list.map((_, n) => n).sort((a, b) => ease[a] - ease[b] || a - b).forEach(n => { const p = list[n], w = p.w; let best = null, bs = Infinity;
        cands(p).forEach((c, ci) => { const s = cost(p, n, c, ci) + (done.some(q => hit([c[0], c[1], w, H], q, 2)) ? 1000 : 0); if (s < bs) { bs = s; best = c; } });
        const bx = [best[0], best[1], w, H]; done.push(bx);
        // (its side of the dot, so a drag carries the tag along on that side: a gap to its right or left, or the share of it left of the dot)
        const side = bx[0] >= p.px ? "r" : bx[0] + w <= p.px ? "l" : "c";
        out[n] = { x: bx[0], y: bx[1], side: side, gap: side === "r" ? bx[0] - p.px : side === "l" ? p.px - bx[0] - w : (p.px - bx[0]) / w, dy: bx[1] - p.py }; });
      return out;
    }
    const PH = 25;   // an asymptote pill's height (CSS: 12 px text, 4 px padding, 1,5 px border)
    const pillW = (f, tx) => tw(tx, 12, 800) + 19 + (TWO ? 20 : 0);
    function pinsHtml(G, F) {
      const vl = FE.filter(f => f.kind === "vline" && placed(f.id)).sort((p, q) => v.p[p.id] - v.p[q.id]).map(f => f.id);
      const ptsF = FE.filter(f => f.kind === "point" && placed(f.id)), pills = [], out = {};
      const aria = (f, val) => ` aria-label="${esc(nameOf(f))} at ${esc(spoken(f, val))}${locked ? "" : ". Arrow keys move it, Delete removes it"}"`;
      const common = f => `type="button" class="sk-pin sk-${f.kind}" data-pin="${f.id}"${TWO ? ` data-g="${gk(f)}"` : ""} data-act="${act === f.id}" data-v="${verdict(f.id)}"${locked ? ' tabindex="-1"' : ""}` + aria(f, v.p[f.id]);
      // the asymptotes' pills first (the tags keep off them)
      FE.filter(f => placed(f.id) && f.kind !== "point").forEach(f => { const val = v.p[f.id], tx = valText(f, val), w = pillW(f, tx);
        // an asymptote's pill sits just above its line (clear of the x-axis' numbers when it is y = 0), at the end its curve keeps away from
        if (f.kind === "hline") { const fit = F[GR.findIndex(g => g.id === f.graph)], far = x => { const y = fit && fit !== "nofit" ? fit.f(x) : NaN; return isFinite(y) ? Math.abs(y - val) : Infinity; };
          // (below the line when it is under the x-axis: above it, y = −1's pill covered the axis' numbers; and below at the grid's top)
          const left = !!(fit && fit !== "nofit") && far(R0.xmin + 0.04 * R0.xr) > far(R0.xmax - 0.04 * R0.xr), top = (val < 0 && G.Y(val) + 26 < G.T + G.ph) || G.Y(val) - G.T < 26;
          const x = left ? G.L + 4 : G.L + G.pw - 4; pills.push([left ? x : x - w, top ? G.Y(val) + 3 : G.Y(val) - 3 - PH, w, PH]);
          out[f.id] = `<button ${common(f)} data-side="${left ? "l" : "r"}" data-below="${top}" style="left:${x}px;top:${G.Y(val).toFixed(1)}px">${badge(f)}${tx}</button>`; return; }
        // (kept inside the grid: at x = −135°, the grid's left edge, half the pill was cut off)
        const low = vl.indexOf(f.id) % 2 === 1, cx = Math.max(G.L + w / 2, Math.min(G.L + G.pw - w / 2, G.X(val))), y = low ? G.T + G.ph - 4 : G.T + 4;
        pills.push([cx - w / 2, low ? y - PH : y, w, PH]);
        out[f.id] = `<button ${common(f)} data-low="${low}" style="left:${cx.toFixed(1)}px;top:${y}px">${badge(f)}${tx}</button>`; });
      const list = ptsF.map(f => ({ px: G.X(v.p[f.id][0]), py: G.Y(v.p[f.id][1]), w: tw(valText(f, v.p[f.id]), 11.5, 800) + (TWO ? 17 : 0) + 2 }));
      const boxes = tagBoxes(G, F, list, pills);
      // a tag a row or more off its dot hangs from it on a thin line (stacked over a neighbour's tag, it read as the neighbour's)
      const lead = boxes.map((b, k) => { const p = list[k]; if (b.dy > -30 && b.dy < 20) return "";
        const nx = Math.max(b.x, Math.min(b.x + p.w, p.px)), ny = Math.max(b.y, Math.min(b.y + TH, p.py)), d = Math.hypot(nx - p.px, ny - p.py) || 1;
        return `<line x1="${(p.px + (nx - p.px) * 9 / d).toFixed(1)}" y1="${(p.py + (ny - p.py) * 9 / d).toFixed(1)}" x2="${nx.toFixed(1)}" y2="${ny.toFixed(1)}"/>`; }).join("");
      ptsF.forEach((f, k) => { const p = list[k], b = boxes[k];
        out[f.id] = `<button ${common(f)} style="left:${p.px.toFixed(1)}px;top:${p.py.toFixed(1)}px"></button>`
          + `<span class="sk-tag" aria-hidden="true" data-side="${b.side}" data-gap="${b.gap.toFixed(3)}" data-dy="${b.dy.toFixed(1)}" style="left:${b.x.toFixed(1)}px;top:${b.y.toFixed(1)}px">${badge(f)}${valText(f, v.p[f.id])}</span>`; });
      return (lead ? `<svg class="sk-lead" width="${G.w}" height="${G.h}" aria-hidden="true" focusable="false">${lead}</svg>` : "")
        + FE.filter(f => placed(f.id)).map(f => out[f.id]).join("") + `<span class="sk-ghost" aria-hidden="true" hidden></span>`;
    }
    const nPlaced = () => FE.filter(f => placed(f.id)).length;
    const chip = f => { const on = placed(f.id), cv = `<span class="sk-cv" data-on="${on}">${on ? valText(f, v.p[f.id]) : "not placed"}</span>`;
      return `<button type="button" class="sk-chip" data-f="${f.id}" data-k="${f.kind}"${TWO ? ` data-g="${gk(f)}"` : ""} data-on="${on}" data-v="${verdict(f.id)}" aria-pressed="${act === f.id}"${locked ? " disabled" : ""}`
        + ` aria-label="${esc(nameOf(f))}${on ? ", at " + esc(spoken(f, v.p[f.id])) : ", not placed"}"><span class="sk-ic" aria-hidden="true"></span>`
        // (two lines whatever its state, in a grid: placing a feature never re-flows the tray, so the grid under it never jumps; with the
        // value beside the name the chips re-wrapped and the grid fell 52 px between two taps at 360 px). Two graphs: the graph's badge
        // starts the value line ("x-intercept" over "[f] (30° ; 0)"), where a 360 px chip has room
        + `<span class="sk-cb"><span class="sk-cl">${esc(shortOf(f))}</span>${TWO ? `<span class="sk-cr">${badge(f)}${cv}</span>` : cv}</span></button>`; };
    const shapeLabel = g => (g.shape && g.shape.label || "Shape") + (GR.length > 1 ? " of " + (g.label || g.id) : "");
    function resHtml() {
      if (!items) return "";
      return `<div class="bp-chips sk-res" role="status">${items.map(it => { const f = FE.find(x => x.id === it.key), g = GR.find(x => "shape" + (GR.length > 1 ? ":" + x.id : "") === it.key);
        const st = it.verdict === "correct" ? (it.awarded >= it.available ? "true" : "part") : "false";
        return `<span class="bp-chip" data-ok="${st}">${st === "true" ? "✓" : st === "part" ? "◐" : "✕"} ${esc(f ? nameOf(f) : g ? shapeLabel(g) : it.key)}${it.available ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
    }
    host.innerHTML = `<div class="bp sk" data-locked="false"><div class="sk-tray" role="group" aria-label="Features to place on the grid"></div><div class="sk-picks"></div>`
      + `<div class="sk-plot" role="group"><svg class="sk-svg" aria-hidden="true" focusable="false"></svg><div class="sk-pins"></div></div>`
      + `<div class="sk-foot"></div><div class="sk-out"></div><p class="sr-only" aria-live="polite"></p></div>`;
    const root = host.firstChild, tray = root.querySelector(".sk-tray"), picks = root.querySelector(".sk-picks"), plot = root.querySelector(".sk-plot"),
      svgEl = root.querySelector(".sk-svg"), pins = root.querySelector(".sk-pins"), foot = root.querySelector(".sk-foot"), out = root.querySelector(".sk-out"), live = root.querySelector("[aria-live]");
    const say = s => { live.textContent = s; };
    function paint() {   // the grid and the pins only (a drag repaints these; the dragged pin keeps its pointer capture by being moved, not rebuilt)
      const G = geo(), F = fitAll();
      svgEl.setAttribute("viewBox", "0 0 " + G.w + " " + G.h); svgEl.setAttribute("width", G.w); svgEl.setAttribute("height", G.h);
      plot.style.width = G.w + "px"; plot.style.height = G.h + "px"; svgEl.innerHTML = svgInner(F, G);
      return { G: G, F: F };
    }
    function render(focusSel) {
      if (focusSel === undefined) { const a = document.activeElement; focusSel = a && root.contains(a) ? (a.dataset.pin ? `[data-pin="${a.dataset.pin}"]` : a.dataset.f ? `[data-f="${a.dataset.f}"]`
        : a.dataset.op ? `[data-g="${a.dataset.g}"][data-op="${a.dataset.op}"]` : a.classList.contains("sk-rm") ? ".sk-rm" : null) : null; }
      W = Math.max(240, Math.min(560, Math.floor(host.getBoundingClientRect().width || 320))); VH = inView();
      try { FONT = getComputedStyle(root).fontFamily || FONT; } catch (_) { /* no style: the fallback measure */ }
      root.dataset.locked = String(locked);
      const { G, F } = paint();
      plot.setAttribute("aria-label", "Graph grid: x from " + fmtX(R0.xmin) + " to " + fmtX(R0.xmax) + ", y from " + fmtY(R0.ymin) + " to " + fmtY(R0.ymax));
      // a tray whose rows and the grid would not fit in view together becomes ONE row of chips that scrolls sideways, the chosen chip kept in
      // view (Maths P2 Nov 2025 7.2's eight chips: a 257 px tray over a 223 px grid at 360 x 702, never both in view while placing)
      const cols = Math.max(1, Math.floor(((tray.clientWidth || W) + 8) / 144)), rows = Math.ceil(FE.length / cols);
      const row = rows > 2 && 28 + rows * 60 + 12 + G.h > VH - 24, ti0 = tray.querySelector(".sk-ti"), sl = ti0 ? ti0.scrollLeft : 0;
      tray.dataset.row = String(row);
      tray.innerHTML = `<p class="sk-th"><span>${locked ? "Your features" : "Tap one, then tap the grid"}</span><span class="sk-n">${nPlaced()} of ${FE.length} placed</span></p><div class="sk-ti">${FE.map(chip).join("")}</div>`;
      if (row) keepInRow(sl);
      picks.innerHTML = GR.filter(g => g.shape && g.shape.pick).map(g => `<div class="sk-pick" role="group" aria-label="${esc(shapeLabel(g))}"><span class="sk-pl">${esc(shapeLabel(g))}</span>`
        + g.shape.pick.map(op => `<button type="button" class="sk-op" data-g="${g.id}" data-op="${esc(op)}" aria-pressed="${v.pick[g.id] === op}"${locked ? " disabled" : ""}>${esc(op)}</button>`).join("") + `</div>`).join("");
      pins.innerHTML = pinsHtml(G, F);
      const a = FE.find(f => f.id === act), bad = F.map((fit, k) => fit === "nofit" ? GR[k] : null).filter(Boolean);
      foot.innerHTML = locked ? "" : `<p class="sk-hint">${a ? (placed(a.id) ? "Tap the grid to move the " + esc(nameOf(a)) + ", or drag it." : "Tap the grid to place the " + esc(nameOf(a)) + ".")
        : nPlaced() ? "Drag a point or a line to move it." : ""}${a && placed(a.id) ? ` <button type="button" class="sk-rm">Remove</button>` : ""}</p>`
        + bad.map(g => `<p class="sk-note">These do not fit one ${FAMN[g.family] || "graph"}${GR.length > 1 ? " (" + esc(g.label || g.id) + ")" : ""}: move one.</p>`).join("");
      out.innerHTML = resHtml();
      wire();
      if (focusSel) { const n = root.querySelector(focusSel); if (n) n.focus({ preventScroll: true }); }
    }
    // the tray's row: back where it was scrolled (a render rebuilds it), then the chosen chip brought into view with a little of the next
    // one showing; a fade marks chips past either edge
    function keepInRow(sl) { const ti = tray.querySelector(".sk-ti"); if (!ti) return; ti.scrollLeft = sl;
      const edge = () => { ti.dataset.l = String(ti.scrollLeft > 2); ti.dataset.r = String(ti.scrollLeft + ti.clientWidth < ti.scrollWidth - 2); };
      ti.onscroll = edge;
      const c = ti.querySelector('[aria-pressed="true"]');
      if (c) { const l = c.offsetLeft, r = l + c.offsetWidth, m = 36; let to = ti.scrollLeft;
        if (l - m < to) to = Math.max(0, l - m); else if (r + m > to + ti.clientWidth) to = r + m - ti.clientWidth;
        if (Math.abs(to - ti.scrollLeft) > 1) ti.scrollTo({ left: to, behavior: o.reduced ? "auto" : "smooth" }); }
      edge(); }
    const centre = f =>f.kind === "point" ? [sx((R0.xmin + R0.xmax) / 2), sy((R0.ymin + R0.ymax) / 2)] : f.kind === "hline" ? sy((R0.ymin + R0.ymax) / 2) : sx((R0.xmin + R0.xmax) / 2);
    const fromEvent = (e, kind) => { const r = svgEl.getBoundingClientRect(), G = geo(), px = (e.clientX - r.left) * G.w / (r.width || G.w), py = (e.clientY - r.top) * G.h / (r.height || G.h);
      const x = sx(R0.xmin + (px - G.L) / G.pw * R0.xr), y = sy(R0.ymax - (py - G.T) / G.ph * R0.yr); return kind === "point" ? [x, y] : kind === "hline" ? y : x; };
    const put = (id, val, quiet) => { const f = FE.find(x => x.id === id), was = placed(id); v.p[id] = val; if (!quiet) say(nameOf(f) + (was ? " moved to " : " placed at ") + spoken(f, val)); };
    function wire() {
      tray.querySelectorAll("[data-f]").forEach(b => b.onclick = e => { if (locked) return; const id = b.dataset.f, f = FE.find(x => x.id === id);
        act = id;
        if (e.detail === 0) {   // the keyboard (or a screen reader): placed at the grid's centre if new, then its pin takes the focus for the arrows
          if (!placed(id)) { put(id, centre(f)); emit(); }
          render(`[data-pin="${id}"]`); return; }
        render(`[data-f="${id}"]`); });
      picks.querySelectorAll("[data-op]").forEach(b => b.onclick = () => { if (locked) return; v.pick[b.dataset.g] = b.dataset.op; emit(); render(`[data-g="${b.dataset.g}"][data-op="${b.dataset.op}"]`); });
      const rm = foot.querySelector(".sk-rm"); if (rm) rm.onclick = () => { if (locked || !act) return; const f = FE.find(x => x.id === act); delete v.p[act]; say(nameOf(f) + " removed"); emit(); render(`[data-f="${act}"]`); };
      // a tap on the grid places (or moves) the chosen feature; the grid lets the page scroll under a swipe (only the pins hold the finger)
      plot.onclick = e => { if (locked || drag || e.target.closest(".sk-pin") || Date.now() - pinUp < 450) return; if (!act) act = firstOpen(""); if (!act) return;
        const id = act, f = FE.find(x => x.id === id), was = placed(id); put(id, fromEvent(e, f.kind)); act = was ? "" : firstOpen(id); emit(); render(null); };
      const ghost = pins.querySelector(".sk-ghost");
      plot.onpointermove = e => { if (e.pointerType !== "mouse" || drag || locked || !act || e.target.closest(".sk-pin")) { if (ghost) ghost.hidden = true; return; }
        const f = FE.find(x => x.id === act), val = fromEvent(e, f.kind), G = geo();
        ghost.hidden = false; ghost.dataset.k = f.kind; ghost.textContent = valText(f, val);
        ghost.style.left = (f.kind === "hline" ? G.L : G.X(f.kind === "point" ? val[0] : val)) + "px"; ghost.style.top = (f.kind === "vline" ? G.T : G.Y(f.kind === "point" ? val[1] : val)) + "px";
        if (f.kind !== "point") { ghost.style.width = f.kind === "hline" ? G.pw + "px" : ""; ghost.style.height = f.kind === "vline" ? G.ph + "px" : ""; } };
      plot.onpointerleave = () => { if (ghost) ghost.hidden = true; };
      pins.querySelectorAll(".sk-pin").forEach(b => {
        const id = b.dataset.pin, f = FE.find(x => x.id === id);
        // (the grab keeps its offset: an asymptote's pill sits above its line, and the line would jump to the finger)
        b.onpointerdown = e => { if (locked) return; e.preventDefault(); e.stopPropagation(); b.setPointerCapture(e.pointerId); b.focus({ preventScroll: true });
          const r = svgEl.getBoundingClientRect(), G = geo(), s = r.width / G.w, cur = v.p[id];
          const fx = f.kind === "hline" ? e.clientX : r.left + G.X(f.kind === "point" ? cur[0] : cur) * s, fy = f.kind === "vline" ? e.clientY : r.top + G.Y(f.kind === "point" ? cur[1] : cur) * s;
          drag = { id: id, x: e.clientX, y: e.clientY, ox: fx - e.clientX, oy: fy - e.clientY, moved: false }; document.documentElement.classList.add("bp-drag");
          const ld = pins.querySelector(".sk-lead"); if (ld) ld.remove(); };   // (the tags' lines would point at where the pin was; the drop redraws them)
        b.onpointermove = e => { if (!drag || drag.id !== id) return; if (!drag.moved && Math.hypot(e.clientX - drag.x, e.clientY - drag.y) < 4) return; drag.moved = true;
          const val = fromEvent({ clientX: e.clientX + drag.ox, clientY: e.clientY + drag.oy }, f.kind); if (JSON.stringify(val) === JSON.stringify(v.p[id])) return; put(id, val, true);
          const { G } = paint(), tag = b.nextElementSibling;   // move this pin and its tag; the grid and the curve repaint under it
          // (the tag rides on its side of the dot; it finds its free spot again when the pin is let go)
          if (f.kind === "point") { const px = G.X(val[0]), py = G.Y(val[1]); b.style.left = px + "px"; b.style.top = py + "px"; tag.innerHTML = badge(f) + valText(f, val);
            const tw0 = tag.offsetWidth, gp = +tag.dataset.gap || 0, sd = tag.dataset.side;
            tag.style.left = (sd === "l" ? px - gp - tw0 : sd === "c" ? px - gp * tw0 : px + gp) + "px"; tag.style.top = (py + (+tag.dataset.dy || -9 - TH)) + "px"; }
          else { const tx = valText(f, val); b.innerHTML = badge(f) + tx; const hw = b.offsetWidth / 2;
            if (f.kind === "hline") b.style.top = G.Y(val) + "px"; else b.style.left = Math.max(G.L + hw, Math.min(G.L + G.pw - hw, G.X(val))) + "px"; } };
        const end = () => { if (!drag || drag.id !== id) return; const moved = drag.moved; drag = null; pinUp = Date.now(); document.documentElement.classList.remove("bp-drag");
          if (moved) say(nameOf(f) + " moved to " + spoken(f, v.p[id]));
          act = moved ? "" : id; if (moved) emit(); render(`[data-pin="${id}"]`); };
        b.onpointerup = end; b.onpointercancel = end;
        b.onclick = e => e.stopPropagation();
        b.onkeydown = e => { if (locked) return; const st = e.shiftKey ? 5 : 1, cur = v.p[id];
          const d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key];
          if (d) { e.preventDefault(); let val;
            if (f.kind === "point") val = [sx(cur[0] + d[0] * st * R0.xstep), sy(cur[1] + d[1] * st * R0.ystep)];
            else if (f.kind === "hline") { if (!d[1]) return; val = sy(cur + d[1] * st * R0.ystep); } else { if (!d[0]) return; val = sx(cur + d[0] * st * R0.xstep); }
            if (JSON.stringify(val) === JSON.stringify(cur)) return; act = id; put(id, val); emit(); render(`[data-pin="${id}"]`); return; }
          if (e.key === "Delete" || e.key === "Backspace") { e.preventDefault(); delete v.p[id]; act = id; say(nameOf(f) + " removed"); emit(); render(`[data-f="${id}"]`); return; }
          if (e.key === "Enter" || e.key === "Escape") { e.preventDefault(); const nx = e.key === "Enter" ? firstOpen(id) : id; act = e.key === "Enter" ? nx : act; render(nx ? `[data-f="${nx}"]` : `[data-f="${id}"]`); } };
      });
    }
    render(null);
    if (window.ResizeObserver) { ro = new ResizeObserver(() => { const w = Math.max(240, Math.min(560, Math.floor(host.getBoundingClientRect().width || 320))); if (Math.abs(w - W) >= 2 && !drag) render(); }); ro.observe(host); }
    return { sync(s) { const nv = normV(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v);
        const its = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? s.items : null, was = locked + "|" + JSON.stringify(items);
        v = nv; locked = !!s.locked; items = its;
        if (changed && !Object.keys(nv.p).length) act = firstOpen("");   // a fresh try starts at the first feature
        if (locked) act = "";
        if ((changed || was !== locked + "|" + JSON.stringify(items)) && !drag) render(); },
      destroy() { if (ro) ro.disconnect(); document.documentElement.classList.remove("bp-drag"); host.innerHTML = ""; } };
  }

  // ── the NUMBER LINE builders (2026-10-11): "Draw a box and whisker diagram" ("boxplot") and "Represent your answer on a number line"
  // ("numline") BUILT on the paper's own scaled line (the answer book's, where it prints one). A tray holds what the learner places (the
  // five values; an inequality's end or ends), never where they go: tap one, then tap the line (it snaps to the line's step), or drag
  // along the line (what is under the finger moves), or nudge the last one touched with − and +; keyboard: Enter on a chip places it
  // mid-line, the arrows move it (Shift: 5 steps), Delete removes it. The box and whiskers, or the shading and its open or closed dots,
  // draw themselves from what is placed. The answer is the placed values (and a number line's shading and dots): the marker reads only
  // those, against the memo's criteria.
  //   cfg   { x: [min, max, step], tick?, label?, unit? }   (the learner's view: the scale only)
  //   value boxplot { min, q1, med, q3, max } (numbers); numline { s: "left" | "right" | "between" | "outside", e0, e1 (numbers),
  //         c0, c1: "open" | "closed" } (e1 / c1 only with two ends)
  function lineBuild(host, o, spec) {
    const cfg = o.cfg, lo = cfg.x[0], hi = cfg.x[1], st = cfg.x[2] || 1;
    const snap = u => +(Math.max(lo, Math.min(hi, lo + Math.round((u - lo) / st) * st))).toFixed(9);
    const fmt = n => skNum(n, false), stepTx = fmt(st);
    let v = spec.norm(o.value), locked = false, items = null, drag = null, W = 0, ro = null, act = "", sel = "";
    const ids = () => spec.ids(v), byId = id => ids().find(x => x.id === id), placed = id => typeof v[id] === "number";
    // the next value still to place, after `after` (round the tray)
    const firstOpen = after => { const L = ids(), i = L.findIndex(x => x.id === after), R = L.slice(i + 1).concat(L.slice(0, i + 1)); return (R.find(x => !placed(x.id)) || {}).id || ""; };
    act = firstOpen("");
    const emit = () => o.onChange(clone(v));
    // the line as wide as the card allows (560 px at most); a number every `label` units, widened while the numbers would touch
    function geo() {
      const L = 26, pw = W - 2 * L, per = pw / (hi - lo), tick = cfg.tick || st, wide = Math.max(fmt(lo).length, fmt(hi).length) * 6.8 + 9;
      const lab0 = cfg.label || tick, lab = lab0 * ([1, 2, 4, 5, 10, 20, 50, 100].find(k => lab0 * k * per >= wide) || 100);
      return { L: L, pw: pw, per: per, tick: tick, lab: lab, X: u => L + (u - lo) * per, val: px => snap(lo + (px - L) / per) };
    }
    const vt = id => { const it = items && items.find(x => x.key === id); return it ? (it.verdict === "correct" || it.verdict === "partial" ? "ok" : "bad") : ""; };
    function axisSvg(G, y) {
      const on = (u, k) => Math.abs(Math.round(u / k) * k - u) < 1e-6, n = Math.round((hi - lo) / G.tick), minor = G.tick * G.per >= 3.5;
      let t = `<line x1="${G.L - 16}" x2="${G.L + G.pw + 16}" y1="${y}" y2="${y}" class="nl-axis"/>`
        + `<path d="M${G.L - 20} ${y}l8 -4.5v9z" class="nl-arrow"/><path d="M${G.L + G.pw + 20} ${y}l-8 -4.5v9z" class="nl-arrow"/>`;
      for (let i = 0; i <= n; i++) { const u = lo + i * G.tick, lab = on(u, G.lab), x = G.X(u).toFixed(1);
        if (lab || minor) t += `<line x1="${x}" x2="${x}" y1="${y - (lab ? 6 : 4)}" y2="${y + (lab ? 6 : 4)}" class="nl-tick${lab ? " nl-tick2" : ""}"/>`;
        if (lab) t += `<text x="${x}" y="${y + 21}" class="nl-num" text-anchor="middle">${fmt(u)}</text>`; }
      if (cfg.unit) t += `<text x="${(G.L + G.pw / 2).toFixed(1)}" y="${y + 39}" class="nl-unit" text-anchor="middle">${esc(cfg.unit)}</text>`;
      return t;
    }
    host.innerHTML = `<div class="bp nl nl-${spec.kind}" data-locked="false"><div class="nl-top"></div><div class="sk-tray nl-tray" role="group" aria-label="${esc(spec.trayName)}"></div>`
      + `<div class="nl-plot" role="group"><svg class="nl-svg" aria-hidden="true" focusable="false"></svg></div>`
      + `<div class="nl-nudge"></div><div class="nl-foot"></div><div class="sk-out"></div><p class="sr-only" aria-live="polite"></p></div>`;
    const root = host.firstChild, top = root.querySelector(".nl-top"), tray = root.querySelector(".nl-tray"), plot = root.querySelector(".nl-plot"), svgEl = root.querySelector(".nl-svg"),
      nudge = root.querySelector(".nl-nudge"), foot = root.querySelector(".nl-foot"), out = root.querySelector(".sk-out"), live = root.querySelector("[aria-live]");
    const say = s => { live.textContent = s; };
    function paint() {   // the drawing and the line only (a drag repaints this; the tray's chip value is updated in place)
      const G = geo(), Ay = spec.axisY, H = Ay + (cfg.unit ? 48 : 31);
      svgEl.setAttribute("viewBox", "0 0 " + W + " " + H); svgEl.setAttribute("width", W); svgEl.setAttribute("height", H); plot.style.width = W + "px";
      svgEl.innerHTML = `<rect x="0.75" y="0.75" width="${W - 1.5}" height="${H - 1.5}" rx="12" class="nl-bg"/>` + spec.diagram(v, G, Ay, sel, vt, ids()) + axisSvg(G, Ay);
      return G;
    }
    const chip = x => { const on = placed(x.id);
      return `<button type="button" class="sk-chip nl-chip" data-f="${x.id}" data-k="point" data-on="${on}" data-v="${vt(x.id)}" aria-pressed="${act === x.id}"${locked ? " disabled" : ""}`
        + ` aria-label="${esc(x.label)}${x.sub ? " (" + x.sub + ")" : ""}${on ? ", at " + fmt(v[x.id]) : ", not placed"}${locked ? "" : on ? ". Arrow keys move it, Delete removes it" : ""}"><span class="sk-ic" aria-hidden="true"></span>`
        // (two lines whatever its state, as the sketch's: placing a value never re-flows the tray, so the line under it never jumps)
        + `<span class="sk-cb"><span class="sk-cl">${esc(x.label)}</span><span class="sk-cv" data-on="${on}">${x.sub ? x.sub + (on ? " = " : " · ") : ""}${on ? fmt(v[x.id]) : "not placed"}</span></span></button>`; };
    function resHtml() {
      if (!items) return "";
      return `<div class="bp-chips sk-res" role="status">${items.map(it => { const s = it.verdict === "correct" ? "true" : it.verdict === "partial" ? "part" : "false";
        return `<span class="bp-chip" data-ok="${s}">${s === "true" ? "✓" : s === "part" ? "◐" : "✕"} ${esc(spec.resLabel(it.key, items))}${it.available ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
    }
    function render(focusSel) {
      if (focusSel === undefined) { const a = document.activeElement; focusSel = a && root.contains(a) ? (a.dataset.f ? `[data-f="${a.dataset.f}"]` : a.dataset.d ? `.nl-nb[data-d="${a.dataset.d}"]`
        : a.dataset.op ? `[data-op="${a.dataset.op}"]` : a.dataset.cc ? `[data-cc="${a.dataset.cc}"]` : a.classList.contains("nl-rm") ? ".nl-rm" : null) : null; }
      W = Math.max(240, Math.min(560, Math.floor(host.getBoundingClientRect().width || 320)));
      if (!locked && !byId(act)) act = firstOpen("");
      if (sel && !(byId(sel) && placed(sel))) sel = "";
      root.dataset.locked = String(locked);
      top.innerHTML = spec.top ? spec.top(v, locked) : "";
      const L = ids(), n = L.filter(x => placed(x.id)).length;
      tray.innerHTML = `<p class="sk-th"><span>${locked ? spec.trayDone : spec.trayHead}</span><span class="sk-n">${n} of ${L.length} placed</span></p>`
        + `<div class="sk-ti${spec.row ? " nl-rows" : ""}">${L.map(x => spec.row ? spec.row(x, chip(x), v, locked) : chip(x)).join("")}</div>`;
      paint();
      plot.setAttribute("aria-label", "Number line from " + fmt(lo) + " to " + fmt(hi) + (st !== 1 ? ", in steps of " + stepTx : ""));
      const s = byId(sel);
      nudge.innerHTML = locked || !s ? "" : `<div class="nl-nd" role="group" aria-label="Nudge the ${esc(s.lower)}"><span class="nl-ndl">${esc(s.label)} <b>${fmt(v[s.id])}</b></span>`
        + `<button type="button" class="nl-nb" data-d="-1" aria-label="Move the ${esc(s.lower)} one step left"${v[s.id] <= lo ? " disabled" : ""}>− ${stepTx}</button>`
        + `<button type="button" class="nl-nb" data-d="1" aria-label="Move the ${esc(s.lower)} one step right"${v[s.id] >= hi ? " disabled" : ""}>+ ${stepTx}</button>`
        + `<button type="button" class="sk-rm nl-rm">Remove</button></div>`;
      const a = byId(act);
      foot.innerHTML = locked ? "" : `<p class="sk-hint">${a ? (placed(a.id) ? "Tap the line to move the " : "Tap the line to place the ") + esc(a.lower) + "." : n ? "Drag a value along the line, or nudge it with − and +." : ""}</p>`
        + (spec.note ? spec.note(v) : "");
      out.innerHTML = resHtml();
      wire();
      if (focusSel) { const nd = root.querySelector(focusSel); if (nd) nd.focus({ preventScroll: true }); }
    }
    const move = (id, u) => { const w = snap(u), x = byId(id); if (w === v[id]) return; const was = placed(id); v[id] = w; sel = id; say(x.label + (was ? " moved to " : " placed at ") + fmt(w)); emit(); };
    const remove = id => { const x = byId(id); delete v[id]; if (sel === id) sel = ""; act = id; say(x.label + " removed"); emit(); };
    function wire() {
      tray.querySelectorAll("[data-f]").forEach(b => {
        const id = b.dataset.f;
        b.onclick = e => { if (locked) return; act = id; if (placed(id)) sel = id;
          if (e.detail === 0 && !placed(id)) { move(id, (lo + hi) / 2); act = firstOpen(id); }   // the keyboard: placed mid-line, then the arrows move it
          render(`[data-f="${id}"]`); };
        b.onkeydown = e => { if (locked || !placed(id)) return;
          const d = { ArrowLeft: -1, ArrowDown: -1, ArrowRight: 1, ArrowUp: 1, PageDown: -5, PageUp: 5 }[e.key];
          if (d) { e.preventDefault(); move(id, v[id] + d * st * (e.shiftKey ? 5 : 1)); render(`[data-f="${id}"]`); return; }
          if (e.key === "Delete" || e.key === "Backspace") { e.preventDefault(); remove(id); render(`[data-f="${id}"]`); } };
      });
      nudge.querySelectorAll(".nl-nb").forEach(b => b.onclick = () => { if (locked || !placed(sel)) return; move(sel, v[sel] + +b.dataset.d * st); render(`.nl-nb[data-d="${b.dataset.d}"]`); });
      const rm = nudge.querySelector(".nl-rm"); if (rm) rm.onclick = () => { if (locked || !sel) return; const id = sel; remove(id); render(`[data-f="${id}"]`); };
      if (spec.wire) spec.wire(root, { set: (fn, f) => { if (locked) return; fn(v); emit(); render(f); }, say: say });
    }
    // the line: a tap places (or moves) the chosen value; a sideways drag moves what is under the finger (else the chosen value); an
    // up-and-down swipe scrolls the page (touch-action: pan-y), never placing anything
    const pxOf = e => { const r = svgEl.getBoundingClientRect(); return (e.clientX - r.left) * W / (r.width || W); };
    const grab = px => { const G = geo(); let best = "", bd = 22; ids().forEach(x => { if (!placed(x.id)) return; const d = Math.abs(G.X(v[x.id]) - px) - (x.id === sel ? 3 : 0); if (d < bd) { bd = d; best = x.id; } }); return best; };
    plot.addEventListener("pointerdown", e => { if (locked || (e.pointerType === "mouse" && e.button !== 0)) return; drag = { x: e.clientX, y: e.clientY, pid: e.pointerId, near: grab(pxOf(e)), on: false }; });
    plot.addEventListener("pointermove", e => { const d = drag; if (!d || d.pid !== e.pointerId) return;
      if (!d.on) { const dx = Math.abs(e.clientX - d.x), dy = Math.abs(e.clientY - d.y); if (dy > 10 && dy > dx) { drag = null; return; } if (dx < 6) return;
        d.id = d.near || act; if (!d.id) { drag = null; return; } d.on = true; d.was = placed(d.id);
        try { plot.setPointerCapture(e.pointerId); } catch (_) { /* a synthetic pointer */ } document.documentElement.classList.add("bp-drag"); }
      e.preventDefault();
      const w = geo().val(pxOf(e)); if (w === v[d.id]) return; v[d.id] = w; sel = d.id; paint();
      const cv = tray.querySelector(`[data-f="${d.id}"] .sk-cv`), sub = (byId(d.id) || {}).sub; if (cv) { cv.textContent = (sub ? sub + " = " : "") + fmt(w); cv.dataset.on = "true"; } });
    const end = e => { const d = drag; if (!d || d.pid !== e.pointerId) return; drag = null; document.documentElement.classList.remove("bp-drag");
      if (d.on) { const x = byId(d.id); sel = d.id; if (act === d.id || !act) act = firstOpen(d.id); say(x.label + (d.was ? " moved to " : " placed at ") + fmt(v[d.id])); emit(); render(null); return; }
      if (e.type === "pointercancel" || locked) return;
      // a tap: with nothing chosen (all placed), a tap on a value chooses it; else the chosen value goes where the line was tapped
      if (!act) { if (d.near) { sel = act = d.near; render(null); } return; }
      const id = act; move(id, geo().val(pxOf(e))); sel = id; act = firstOpen(id); render(null); };
    plot.addEventListener("pointerup", end); plot.addEventListener("pointercancel", end);
    render(null);
    if (window.ResizeObserver) { ro = new ResizeObserver(() => { const w = Math.max(240, Math.min(560, Math.floor(host.getBoundingClientRect().width || 320))); if (Math.abs(w - W) >= 2 && !drag) render(); }); ro.observe(host); }
    return { sync(s) { if (drag && drag.on) return;   // (a drag owns the value until it is let go)
        const nv = spec.norm(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v);
        const its = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? s.items : null, was = locked + "|" + JSON.stringify(items);
        v = nv; locked = !!s.locked; items = its;
        if (changed && !Object.keys(nv).length) { act = firstOpen(""); sel = ""; }   // a fresh try starts at the first value
        if (locked) act = "";
        if (changed || was !== locked + "|" + JSON.stringify(items)) render(); },
      destroy() { if (ro) ro.disconnect(); document.documentElement.classList.remove("bp-drag"); host.innerHTML = ""; } };
  }
  // tags over a line: each placed value's text at its x, on the first of two rows where it touches no tag before it (the second row
  // higher); kept inside the plot
  function lineTags(list, W, y0, y1) {
    const rows = [[], []];
    return list.slice().sort((p, q) => p.x - q.x).map(p => { const w = p.text.length * 6.6 + 8, x = Math.max(w / 2 + 3, Math.min(W - w / 2 - 3, p.x));
      let r = rows.findIndex(R => R.every(b => x + w / 2 < b[0] || x - w / 2 > b[1])); if (r < 0) r = 1; rows[r].push([x - w / 2, x + w / 2]);
      return `<text x="${x.toFixed(1)}" y="${r ? y1 : y0}" class="nl-tag${p.cls ? " " + p.cls : ""}" text-anchor="middle">${esc(p.text)}</text>`; }).join("");
  }
  // a BOX AND WHISKER diagram: the five values on the paper's line; the whiskers, the box and the median line drawn from where they sit
  // (a quartile's chip names it in words and shows Q₁ / Q₃ on its value line: "Lower quartile (Q₁)" ran to three lines at 360 px)
  const BXV = [["min", "Minimum", "min"], ["q1", "Lower quartile", "Q₁", "Q₁"], ["med", "Median", "med"], ["q3", "Upper quartile", "Q₃", "Q₃"], ["max", "Maximum", "max"]];
  const BXL = { min: "Minimum", q1: "Lower quartile", med: "Median", q3: "Upper quartile", max: "Maximum" };
  function boxplot(host, o) {
    const L = BXV.map(([id, label, short, sub]) => ({ id: id, label: label, short: short, sub: sub, lower: label[0].toLowerCase() + label.slice(1) + (sub ? " (" + sub + ")" : "") }));
    return lineBuild(host, o, { kind: "boxplot", axisY: 98, trayName: "The five values to place on the line", trayHead: "Tap one, then tap the line", trayDone: "Your five values",
      norm: val => { const x = clone(val), b = {}; L.forEach(y => { if (typeof x[y.id] === "number" && isFinite(x[y.id])) b[y.id] = x[y.id]; }); return b; },
      ids: () => L,
      diagram: (v, G, Ay, sel, vt) => { const has = id => typeof v[id] === "number", X = id => G.X(v[id]), T = Ay - 58, B = Ay - 24, C = (T + B) / 2;
        const ln = (x1, y1, x2, y2, c) => `<line x1="${x1.toFixed(1)}" y1="${y1}" x2="${x2.toFixed(1)}" y2="${y2}" class="${c}"/>`;
        let d = "";
        L.forEach(y => { if (has(y.id)) d += ln(X(y.id), C, X(y.id), Ay, "nl-drop" + (sel === y.id ? " nl-on" : "")); });   // each value's dashed drop to the line
        if (has("min") && has("q1")) d += ln(X("min"), C, X("q1"), C, "nl-wh");
        if (has("q3") && has("max")) d += ln(X("q3"), C, X("max"), C, "nl-wh");
        if (has("q1") && has("q3")) { const a = Math.min(X("q1"), X("q3")), b = Math.max(X("q1"), X("q3")); d += `<rect x="${a.toFixed(1)}" y="${T}" width="${(b - a).toFixed(1)}" height="${B - T}" class="nl-box"/>`; }
        ["q1", "q3"].forEach(id => { if (has(id)) d += ln(X(id), T, X(id), B, "nl-edge"); });
        if (has("med")) d += ln(X("med"), T, X("med"), B, "nl-med");
        ["min", "max"].forEach(id => { if (has(id)) d += ln(X(id), C - 9, X(id), C + 9, "nl-cap"); });
        return d + lineTags(L.filter(y => has(y.id)).map(y => ({ x: X(y.id), text: y.short + " " + skNum(v[y.id], false), cls: [sel === y.id ? "nl-on" : "", vt(y.id) ? "nl-" + vt(y.id) : ""].join(" ").trim() })), G.L * 2 + G.pw, T - 7, T - 22); },
      // a structural rule, never the answer: from left to right the five run in order (a swapped Q₁ and Q₃ draws a box the wrong way round)
      note: v => { const p = L.map(y => v[y.id]).filter(n => typeof n === "number");
        return p.some((n, k) => k && n < p[k - 1]) ? `<p class="sk-note">These are out of order: from left to right a box and whisker diagram runs minimum, Q₁, median, Q₃, maximum.</p>` : ""; },
      resLabel: k => BXL[k] || k });
  }
  // an INEQUALITY on a number line: its end (or two ends) placed on the line, each an open or a closed (filled) dot, and the shading: to the left
  // or right of one end, between two ends, or outside them (x ≤ a or x ≥ b)
  // (short words beside each icon, the full sense in its name: "Between two ends" ran to two lines in a tablet's three columns; one row of four on a tablet, two by two on a phone)
  const NLS = [["left", "Left", "Shade to the left of the end"], ["right", "Right", "Shade to the right of the end"], ["between", "Between", "Shade between two ends"], ["outside", "Outside", "Shade outside two ends"]];
  const nlIc = d => `<svg viewBox="0 0 36 14" width="36" height="14" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">${d}</svg>`;
  const NLI = { left: nlIc('<path d="M5 7H26M26 2.5v9"/><path d="M2 7l6-4v8z" fill="currentColor" stroke="none"/>'), right: nlIc('<path d="M10 7H31M10 2.5v9"/><path d="M34 7l-6-4v8z" fill="currentColor" stroke="none"/>'),
    between: nlIc('<path d="M8 7H28M8 2.5v9M28 2.5v9"/>'), outside: nlIc('<path d="M5 7H12M12 2.5v9M24 7H31M24 2.5v9"/><path d="M2 7l5-3.5v7zM34 7l-5-3.5v7z" fill="currentColor" stroke="none"/>') };
  function numline(host, o) {
    const two = s => s === "between" || s === "outside";
    const E1 = [{ id: "e0", label: "End", lower: "end", short: "" }], E2 = [{ id: "e0", label: "End 1", lower: "first end", short: "1" }, { id: "e1", label: "End 2", lower: "second end", short: "2" }];
    return lineBuild(host, o, { kind: "numline", axisY: 76, trayName: "The ends to place on the line", trayHead: "Tap an end, then tap the line", trayDone: "Your number line",
      norm: val => { const x = clone(val), b = {}; if (NLS.some(s => s[0] === x.s)) b.s = x.s;
        (two(b.s) ? ["0", "1"] : ["0"]).forEach(k => { if (typeof x["e" + k] === "number" && isFinite(x["e" + k])) b["e" + k] = x["e" + k]; if (x["c" + k] === "open" || x["c" + k] === "closed") b["c" + k] = x["c" + k]; });
        return b; },
      ids: v => two(v.s) ? E2 : E1,
      top: (v, locked) => `<div class="sk-pick nl-shade" role="group" aria-label="Shading"><span class="sk-pl">Shading</span>`
        + NLS.map(([k, t, n]) => `<button type="button" class="sk-op nl-op" data-op="${k}" aria-label="${n}" aria-pressed="${v.s === k}"${locked ? " disabled" : ""}>${NLI[k]}<span>${t}</span></button>`).join("") + `</div>`,
      // each end's chip, then its dot: open (the end is not in the answer: < or >) or filled (it is: ≤ or ≥); neither is chosen for the learner
      row: (x, chipHtml, v, locked) => { const k = x.id.slice(1);
        return `<div class="nl-row">${chipHtml}<div class="nl-cc" role="group" aria-label="${esc(x.label)}: open or closed dot">`
          + [["open", "Open"], ["closed", "Closed"]].map(([c, t]) => `<button type="button" class="sk-op nl-c" data-cc="${k}:${c}" aria-pressed="${v["c" + k] === c}"${locked ? " disabled" : ""}><span class="nl-ci" data-c="${c}" aria-hidden="true"></span>${t}</button>`).join("") + `</div></div>`; },
      wire: (root, api) => {
        root.querySelectorAll("[data-op]").forEach(b => b.onclick = () => api.set(v => { v.s = b.dataset.op; if (!two(v.s)) { delete v.e1; delete v.c1; } api.say((NLS.find(x => x[0] === b.dataset.op) || [])[2]); }, `[data-op="${b.dataset.op}"]`));
        root.querySelectorAll("[data-cc]").forEach(b => b.onclick = () => { const [k, c] = b.dataset.cc.split(":"); api.set(v => { v["c" + k] = c; api.say((two(v.s) ? "End " + (+k + 1) : "End") + ": " + (c === "open" ? "open dot" : "closed dot")); }, `[data-cc="${b.dataset.cc}"]`); }); },
      diagram: (v, G, Ay, sel, vt, L) => { const Ty = Ay - 34, x0 = G.L - 12, x1 = G.L + G.pw + 12;
        const ends = L.filter(x => typeof v[x.id] === "number").map(x => ({ id: x.id, x: G.X(v[x.id]), c: v["c" + x.id.slice(1)], val: v[x.id] })), xs = ends.map(e => e.x).sort((a, b) => a - b);
        const seg = (a, b) => `<line x1="${a.toFixed(1)}" x2="${b.toFixed(1)}" y1="${Ty}" y2="${Ty}" class="nl-ray"/>`;
        const head = (x, dir) => `<path d="M${(x + dir * 4).toFixed(1)} ${Ty}l${-dir * 10} -6v12z" class="nl-rayhead"/>`;
        let d = "";
        ends.forEach(e => { d += `<line x1="${e.x.toFixed(1)}" x2="${e.x.toFixed(1)}" y1="${Ty + 8}" y2="${Ay}" class="nl-drop${sel === e.id ? " nl-on" : ""}"/>`; });
        if (v.s === "right" && xs.length) d += seg(xs[0], x1 - 6) + head(x1, 1);
        if (v.s === "left" && xs.length) d += seg(x0 + 6, xs[0]) + head(x0, -1);
        if (v.s === "between" && xs.length === 2) d += seg(xs[0], xs[1]);
        if (v.s === "outside" && xs.length === 2) d += seg(x0 + 6, xs[0]) + head(x0, -1) + seg(xs[1], x1 - 6) + head(x1, 1);
        ends.forEach(e => { d += `<circle cx="${e.x.toFixed(1)}" cy="${Ty}" r="7" class="nl-dot" data-c="${e.c || "unset"}"/>`; });
        return d + lineTags(ends.map(e => ({ x: e.x, text: skNum(e.val, false), cls: sel === e.id ? "nl-on" : "" })), G.L * 2 + G.pw, Ty - 13, Ty - 27); },
      // the marker's items name the memo's ends left to right, so a two-ended answer's chips say which end
      resLabel: (k, its) => { const tw = its.some(i => i.key === "end1");
        return { shade: "Shading", end0: tw ? "Left end" : "End", end1: "Right end", circle0: tw ? "Left dot" : "Open or closed dot", circle1: "Right dot" }[k] || k; } });
  }

  // ── the VENN diagram (2026-10-11, "venn"): "Draw a Venn diagram to represent the information" BUILT: two or three circles in the
  // universal set, labelled as the paper labels its sets (never with a count). Each region is a button on the diagram; the one chosen
  // is filled in the editor under it: its number typed (the phone's number keys) or stepped with − and +, and Enter goes on to the next
  // region with the keys still up, so the diagram stays in view while it fills. The outside region shows only where the memo fills
  // one. Where the memo's diagram carries an unknown (x − 20, 26 − x), every region also takes a FORM: the number alone, x, x + n,
  // x − n or n − x, the same five in every region, so none points at the regions that hold x. The answer is the regions' entries:
  // the marker reads only those, against the memo's.
  //   cfg   { sets: [{ id: "S", name?: "smartphone" }] (2 or 3; each id one letter, as the paper labels the circle), outside: bool,
  //           unknown?: "x" }
  //   value { n: { region: whole number }, f: { region: "x" | "x+n" | "x-n" | "n-x" } } (no f: the number alone); a region is the ids
  //           of the sets it lies in, in the sets' order ("S", "ST", "RVC"), or "out"
  let vtUid = 0;
  const vnRegions = (ids, outside) => (ids.length === 2 ? [ids[0], ids[0] + ids[1], ids[1]]
    : [ids[0], ids[1], ids[2], ids[0] + ids[1], ids[0] + ids[2], ids[1] + ids[2], ids.join("")]).concat(outside ? ["out"] : []);
  const vnName = (r, ids) => r === "out" ? (ids.length === 2 ? "Outside both circles" : "Outside all three circles") : r.length === 1 ? r + " only"
    : r.length === ids.length ? (ids.length === 2 ? r[0] + " and " + r[1] : r[0] + ", " + r[1] + " and " + r[2]) : r[0] + " and " + r[1] + " only";
  const VNF = ["n", "x", "x+n", "x-n", "n-x"];
  const vnText = (f, n, X) => { const m = typeof n === "number" ? String(n) : "n";
    return f === "x" ? X : f === "x+n" ? X + " + " + m : f === "x-n" ? X + " − " + m : f === "n-x" ? m + " − " + X : m; };
  // the diagram's geometry in px for a width W: the circles, each region's label point, each set's label (outside its circle)
  function vnGeo(ids, W, outside) {
    const three = ids.length === 3, r = Math.round(W * (three ? 0.215 : 0.235)), cx = W / 2;
    let C, H;
    if (!three) { const d = r * 0.95; H = Math.round(2 * r + 64); C = [[cx - d / 2, H / 2 + 4], [cx + d / 2, H / 2 + 4]]; }
    else { const d = r * 1.1, top = r + 34; H = Math.round(top + d * 0.866 + r + 30); C = [[cx - d / 2, top], [cx + d / 2, top], [cx, top + d * 0.866]]; }
    const G = [C.reduce((t, c) => t + c[0], 0) / C.length, C.reduce((t, c) => t + c[1], 0) / C.length];
    const away = (p, from, k) => { const dx = p[0] - from[0], dy = p[1] - from[1], L = Math.hypot(dx, dy) || 1; return [p[0] + dx / L * k, p[1] + dy / L * k]; };
    const at = {};
    if (!three) { at[ids[0]] = [C[0][0] - r * 0.52, C[0][1]]; at[ids[0] + ids[1]] = [cx, C[0][1]]; at[ids[1]] = [C[1][0] + r * 0.52, C[1][1]]; }
    else { ids.forEach((id, k) => { at[id] = away(C[k], G, r * 0.52); });
      // (0.55 r out from the two centres' midpoint: still 0.78 r from each, inside both; at 0.4 r the 44 x 40 buttons of the lower pairs
      // overlapped the middle one at 320 px)
      [[0, 1, 2], [0, 2, 1], [1, 2, 0]].forEach(([a, b, c]) => { at[ids[a] + ids[b]] = away([(C[a][0] + C[b][0]) / 2, (C[a][1] + C[b][1]) / 2], C[c], r * 0.55); });
      at[ids.join("")] = G; }
    if (outside) at.out = [W - 36, H - 24];
    const lab = C.map((c, k) => three && k === 2 ? [c[0] + r * 0.82, c[1] + r * 0.86] : [c[0] + (k ? 1 : -1) * r * 0.78, c[1] - r * 0.84]);
    return { r: r, C: C, H: H, at: at, lab: lab };
  }
  function venn(host, o) {
    const cfg = o.cfg, sets = (cfg.sets || []).slice(0, 3), ids = sets.map(s => s.id), X = cfg.unknown || "", R = vnRegions(ids, !!cfg.outside), uid = "vt" + (++vtUid);
    const nameOf = r => vnName(r, ids);
    const subOf = r => { if (r === "out") return ""; const nm = r.split("").map(c => (sets.find(s => s.id === c) || {}).name); if (nm.some(x => !x)) return "";
      return r.length === 1 ? nm[0] + " only" : nm.slice(0, -1).join(", ") + " and " + nm[nm.length - 1] + (r.length < ids.length ? " only" : ""); };
    const norm = val => { const x = clone(val), b = { n: {}, f: {} };
      R.forEach(r => { const n = (x.n || {})[r], f = (x.f || {})[r]; if (typeof n === "number" && isFinite(n) && n >= 0) b.n[r] = Math.round(n); if (X && VNF.indexOf(f) > 0) b.f[r] = f; });
      return b; };
    let v = norm(o.value), locked = false, items = null, W = 0, ro = null, sel = R[0];
    const F = r => v.f[r] || "n", has = r => F(r) === "x" || typeof v.n[r] === "number", text = r => has(r) ? vnText(F(r), v.n[r], X) : "";
    const spoken = t => t.replace(/ − /g, " minus ").replace(/ \+ /g, " plus ");
    const emit = () => o.onChange(clone(v));
    const vt = r => { const it = items && items.find(x => x.key === r); return it ? (it.verdict === "correct" || it.verdict === "partial" ? "ok" : "bad") : ""; };
    host.innerHTML = `<div class="bp vn" data-locked="false"><div class="vn-plot"><svg class="vn-svg" aria-hidden="true" focusable="false"></svg>`
      + `<div class="vn-regs" role="group" aria-label="The regions of the Venn diagram"></div></div><div class="vn-ed"></div><p class="sk-hint vn-hint"></p>`
      + `<div class="vt-out"></div><p class="sr-only" aria-live="polite"></p></div>`;
    const root = host.firstChild, plot = root.querySelector(".vn-plot"), svgEl = root.querySelector(".vn-svg"), regs = root.querySelector(".vn-regs"),
      ed = root.querySelector(".vn-ed"), hint = root.querySelector(".vn-hint"), out = root.querySelector(".vt-out"), live = root.querySelector("[aria-live]");
    const say = s => { live.textContent = s; };
    let g = null;
    // the circles, the set labels, and the chosen region shaded: clipped to the circles it lies in, the others masked out
    function svgHtml() {
      const c = (k, at) => `<circle cx="${g.C[k][0].toFixed(1)}" cy="${g.C[k][1].toFixed(1)}" r="${g.r}"${at || ""}/>`;
      let s = `<rect x="1" y="1" width="${W - 2}" height="${g.H - 2}" rx="14" class="vn-u"/>`;
      if (!locked && sel) { const inn = sel === "out" ? [] : sel.split("").map(id => ids.indexOf(id)), outK = ids.map((_, k) => k).filter(k => inn.indexOf(k) === -1);
        s += `<defs>${inn.map(k => `<clipPath id="${uid}-c${k}">${c(k)}</clipPath>`).join("")}<mask id="${uid}-m"><rect x="0" y="0" width="${W}" height="${g.H}" fill="#fff"/>${outK.map(k => c(k, ' fill="#000"')).join("")}</mask></defs>`
          + `<g mask="url(#${uid}-m)">${inn.reduce((h, k) => `<g clip-path="url(#${uid}-c${k})">${h}</g>`, `<rect x="2" y="2" width="${W - 4}" height="${g.H - 4}" rx="13" class="vn-hi"/>`)}</g>`; }
      g.C.forEach((_, k) => { s += c(k, ' class="vn-c"'); });
      ids.forEach((id, k) => { s += `<text x="${g.lab[k][0].toFixed(1)}" y="${g.lab[k][1].toFixed(1)}" class="vn-set" text-anchor="middle" dominant-baseline="middle">${esc(id)}</text>`; });
      return s;
    }
    const regLabel = r => nameOf(r) + (text(r) ? ": " + spoken(text(r)) : ", empty");
    const regHtml = r => { const p = g.at[r], t = text(r);
      return `<button type="button" class="vn-r" data-r="${r}" data-v="${vt(r)}" aria-pressed="${!locked && sel === r}" style="left:${p[0].toFixed(1)}px;top:${p[1].toFixed(1)}px"`
        + `${locked ? " disabled" : ""} aria-label="${esc(regLabel(r))}">${t ? `<span class="vn-t">${esc(t)}</span>` : `<span class="vn-q" aria-hidden="true">?</span>`}</button>`; };
    // the editor: the chosen region's name, with an unknown its form, then its number (typed or stepped). (The form sits ABOVE the field:
    // with the phone's keys up the page holds the field just over the coach strip, and a row under it went behind the strip at 360x702)
    function edHtml() {
      return `<div class="vn-eh"><label class="vn-nm" for="${uid}-in"><b></b><span class="vn-sub"></span></label><button type="button" class="vn-next"></button></div>`
        + `<div class="vn-ctl">` + (X ? `<div class="vn-fm" role="group" aria-label="What the region holds">${VNF.map(k => `<button type="button" class="vn-f" data-f="${k}" aria-pressed="false"></button>`).join("")}</div>` : "")
        + `<div class="vn-st" role="group" aria-label="The number"><button type="button" class="vn-nb" data-d="-1" aria-label="One fewer">−</button>`
        + `<input id="${uid}-in" class="vn-in" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="4" autocomplete="off" autocorrect="off" spellcheck="false">`
        + `<button type="button" class="vn-nb" data-d="1" aria-label="One more">+</button></div></div>`;
    }
    function paintEd() {   // in place: the field keeps its focus (and the phone its keys) as the learner moves from region to region
      if (locked) return; const r = sel, f = F(r), n = v.n[r], last = R.indexOf(r) === R.length - 1, inp = ed.querySelector(".vn-in"), sub = subOf(r);
      ed.querySelector(".vn-nm b").textContent = nameOf(r); const se = ed.querySelector(".vn-sub"); se.textContent = sub; se.hidden = !sub;
      ed.querySelector(".vn-next").textContent = last ? "First region" : "Next region";
      inp.disabled = f === "x"; inp.placeholder = f === "x" ? X : ""; inp.value = f === "x" || typeof n !== "number" ? "" : String(n); inp.enterKeyHint = last ? "done" : "next";
      ed.querySelectorAll(".vn-nb").forEach(b => { b.disabled = f === "x" || (b.dataset.d === "-1" && !(n > 0)); });
      ed.querySelectorAll(".vn-f").forEach(b => { b.textContent = vnText(b.dataset.f, n, X); b.setAttribute("aria-pressed", String(f === b.dataset.f)); });
    }
    function paintRegs() {
      svgEl.innerHTML = svgHtml();
      regs.querySelectorAll(".vn-r").forEach(b => { const r = b.dataset.r, t = text(r); b.setAttribute("aria-pressed", String(!locked && sel === r)); b.dataset.v = vt(r);
        b.setAttribute("aria-label", regLabel(r)); b.innerHTML = t ? `<span class="vn-t">${esc(t)}</span>` : `<span class="vn-q" aria-hidden="true">?</span>`; });
      const n = R.filter(has).length;
      hint.textContent = locked ? "" : (X ? "Tap a region, then type its number or step it with − and +. A region with " + X + " in it: choose its form (n is the number you type). "
        : "Tap a region, then type its number or step it with − and +. ") + n + " of " + R.length + " regions filled.";
      hint.hidden = locked;
    }
    function resHtml() {
      if (!items) return ""; const its = items.filter(it => R.indexOf(it.key) !== -1);
      return `<div class="bp-chips sk-res" role="status">${its.map(it => { const s = it.verdict === "correct" ? "true" : it.verdict === "partial" ? "part" : "false";
        return `<span class="bp-chip" data-ok="${s}">${s === "true" ? "✓" : s === "part" ? "◐" : "✕"} ${esc(nameOf(it.key))}${it.available ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
    }
    function choose(r, focus) { sel = r; paintRegs(); paintEd(); say(regLabel(r));
      if (focus) { const inp = ed.querySelector(".vn-in"), tgt = inp && !inp.disabled ? inp : ed.querySelector('.vn-f[aria-pressed="true"]'); if (tgt) tgt.focus({ preventScroll: true });
        ed.scrollIntoView({ block: "nearest", behavior: o.reduced ? "auto" : "smooth" }); } }
    const next = () => R[(R.indexOf(sel) + 1) % R.length];
    function render(focusSel) {
      if (focusSel === undefined) { const a = document.activeElement; focusSel = a && root.contains(a) ? (a.classList.contains("vn-in") ? ".vn-in" : a.dataset.r ? `.vn-r[data-r="${a.dataset.r}"]`
        : a.dataset.f ? `.vn-f[data-f="${a.dataset.f}"]` : a.dataset.d ? `.vn-nb[data-d="${a.dataset.d}"]` : a.classList.contains("vn-next") ? ".vn-next" : null) : null; }
      W = Math.max(260, Math.min(520, Math.floor(host.getBoundingClientRect().width || 320))); g = vnGeo(ids, W, !!cfg.outside);
      root.dataset.locked = String(locked); if (!R.includes(sel)) sel = R[0];
      plot.style.width = W + "px"; plot.style.height = g.H + "px";
      svgEl.setAttribute("viewBox", "0 0 " + W + " " + g.H); svgEl.setAttribute("width", W); svgEl.setAttribute("height", g.H);
      regs.innerHTML = R.map(regHtml).join(""); ed.innerHTML = locked ? "" : edHtml(); ed.hidden = locked;
      paintRegs(); paintEd(); out.innerHTML = resHtml(); wire();
      if (focusSel) { const nd = root.querySelector(focusSel); if (nd && !nd.disabled) nd.focus({ preventScroll: true }); }
    }
    function setN(n) { const r = sel; if (n == null) delete v.n[r]; else v.n[r] = Math.max(0, Math.min(9999, n)); paintRegs(); paintEd(); emit(); }
    function wire() {
      regs.querySelectorAll(".vn-r").forEach(b => { b.onclick = () => { if (!locked) choose(b.dataset.r, true); }; });
      if (locked) return;
      const inp = ed.querySelector(".vn-in");
      inp.oninput = () => { const d = inp.value.replace(/\D/g, "").slice(0, 4); if (d !== inp.value) inp.value = d; const r = sel;
        if (d === "") delete v.n[r]; else v.n[r] = +d;
        paintRegs(); ed.querySelectorAll(".vn-f").forEach(b => { b.textContent = vnText(b.dataset.f, v.n[r], X); });
        ed.querySelectorAll('.vn-nb[data-d="-1"]').forEach(b => { b.disabled = !(v.n[r] > 0); }); emit(); };
      inp.onkeydown = e => { if (e.key !== "Enter") return; e.preventDefault(); if (R.indexOf(sel) === R.length - 1) { inp.blur(); return; } choose(next(), true); };
      ed.querySelectorAll(".vn-nb").forEach(b => { b.onclick = () => { const n = v.n[sel], d = +b.dataset.d; setN(typeof n === "number" ? n + d : d > 0 ? 1 : 0); say(regLabel(sel)); }; });
      ed.querySelectorAll(".vn-f").forEach(b => { b.onclick = () => { if (b.dataset.f === "n") delete v.f[sel]; else v.f[sel] = b.dataset.f; paintRegs(); paintEd(); emit(); say(regLabel(sel)); }; });
      ed.querySelector(".vn-next").onclick = () => choose(next(), false);
    }
    // a tap on the diagram away from a region's button: the nearest region to it
    plot.addEventListener("click", e => { if (locked || e.target.closest(".vn-r")) return; const b = plot.getBoundingClientRect(), x = e.clientX - b.left, y = e.clientY - b.top;
      let best = "", bd = 64; R.forEach(r => { const d = Math.hypot(g.at[r][0] - x, g.at[r][1] - y); if (d < bd) { bd = d; best = r; } }); if (best) choose(best, true); });
    render(null);
    if (window.ResizeObserver) { ro = new ResizeObserver(() => { const w = Math.max(260, Math.min(520, Math.floor(host.getBoundingClientRect().width || 320))); if (Math.abs(w - W) >= 2) render(); }); ro.observe(host); }
    return { sync(s) {
        const nv = norm(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v), its = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? s.items : null;
        const lockCh = locked !== !!s.locked, itCh = JSON.stringify(items) !== JSON.stringify(its);
        v = nv; locked = !!s.locked; items = its;
        if (changed && !R.some(has)) sel = R[0];   // a fresh try starts at the first region
        if (changed || lockCh) render(); else if (itCh) { paintRegs(); out.innerHTML = resHtml(); } },   // (marks alone: the field under the learner's finger stays)
      destroy() { if (ro) ro.disconnect(); host.innerHTML = ""; } };
  }

  // ── the TREE diagram (2026-10-11, "tree"): "Draw a tree diagram ... show the probabilities on EACH branch and the outcomes" BUILT: the
  // branches are drawn (two stages, as many as the stem's events give each point), with the stages' names; on each branch the learner
  // chooses its outcome (the stem's outcomes, the same choices on every branch, so the drawing never says which is where) and types its
  // probability: a fraction (the top over the bottom, two fields on the phone's number keys) or a decimal (the top field alone, 0,6).
  // Where the memo marks them, each end's outcome is chosen too: "(B ; R)". Enter steps through the number fields in reading order.
  // The answer is what is chosen and typed: the marker reads only that, against the memo's tree.
  //   cfg   { outcomes: [{ id: "B", name: "blue" }], stages: [first, second], skel: [n0, n1, ...] (how many branches follow each first-stage
  //           branch; the first stage has skel.length), ends: bool }
  //   value { l: { path: outcome id }, p: { path: [top, bottom] (strings, bottom "" for a decimal) }, o: { path: "B;R" } }
  //           path "i" (the i-th first-stage branch) or "i.j" (the j-th branch after it)
  const trNum = s => { s = String(s == null ? "" : s).trim().replace(",", "."); return /^\d*\.?\d+$/.test(s) ? parseFloat(s) : NaN; };
  const trVal = p => { const t = Array.isArray(p) ? p : [], d = String(t[1] == null ? "" : t[1]).trim(); return d === "" ? trNum(t[0]) : trNum(t[0]) / trNum(d); };
  function tree(host, o) {
    const cfg = o.cfg, OUT = (cfg.outcomes || []).map(x => x.id), skel = cfg.skel || [], ends = !!cfg.ends, uid = "vt" + (++vtUid), st = cfg.stages || ["First stage", "Second stage"];
    const kids = i => Array.from({ length: skel[i] }, (_, j) => i + "." + j), P2 = skel.flatMap((_, i) => kids(i));
    const ALL = skel.flatMap((_, i) => [String(i)].concat(kids(i)));   // reading order: a branch, then the branches after it
    const combos = OUT.flatMap(a => OUT.map(b => a + ";" + b)), cText = c => "(" + c.split(";").join(" ; ") + ")";
    const norm = val => { const x = clone(val), b = { l: {}, p: {}, o: {} };
      ALL.forEach(k => { const l = (x.l || {})[k], p = (x.p || {})[k]; if (OUT.indexOf(l) !== -1) b.l[k] = l;
        if (Array.isArray(p) && String(p[0] || "") + String(p[1] || "") !== "") b.p[k] = [String(p[0] || ""), String(p[1] || "")]; });
      if (ends) P2.forEach(k => { const c = (x.o || {})[k]; if (combos.indexOf(c) !== -1) b.o[k] = c; });
      return b; };
    let v = norm(o.value), locked = false, items = null, W = 0, ro = null;
    const emit = () => o.onChange(clone(v));
    const vt = k => { const it = items && items.find(x => x.key === k); return it ? (it.verdict === "correct" ? "ok" : "bad") : ""; };
    const bn = k => "branch " + k.split(".").map(x => +x + 1).join(".");   // "branch 2.1": the first after the second
    host.innerHTML = `<div class="bp tr" data-locked="false"><p class="tr-key"></p><div class="tr-plot"><svg class="tr-svg" aria-hidden="true" focusable="false"></svg><div class="tr-in"></div></div>`
      + `<p class="sk-hint tr-hint"></p><div class="tr-note"></div><div class="vt-out"></div></div>`;
    const root = host.firstChild, key = root.querySelector(".tr-key"), plot = root.querySelector(".tr-plot"), svgEl = root.querySelector(".tr-svg"), box = root.querySelector(".tr-in"),
      hint = root.querySelector(".tr-hint"), note = root.querySelector(".tr-note"), out = root.querySelector(".vt-out");
    key.innerHTML = (cfg.outcomes || []).map(x => `<span><b>${esc(x.id)}</b>${x.name ? " " + esc(x.name) : ""}</span>`).join("");
    // the tree's geometry for a card W wide: two columns of branch cells (a fraction, then the outcome), the ends' outcomes after them,
    // the leaves 92 px apart (a fraction is two 40 px fields), each first-stage cell centred on the branches after it. Under 328 px (a
    // 320 px phone) the fields narrow to 42 px and the ends' outcomes to 64; the room left goes first to the gap before the outcomes (up
    // to 24 px: "Second marble" ran into "Outcome" at 820 px), then to the branches
    function geo() {
      const tight = W < 328, FW = tight ? 42 : 44, CW = 2 * FW + 4, OW = ends ? (tight ? 64 : 76) : 0, nL = P2.length, PIT = 92, head = 28;
      const free = W - 10 - 2 * CW - OW, g3 = ends ? Math.max(6, Math.min(24, free - 40)) : 0, rest = free - g3;
      const g1 = Math.max(14, Math.min(110, rest * 0.45)), g2 = Math.max(14, Math.min(130, rest - g1));
      const x1 = 10 + g1, x2 = x1 + CW + g2, x3 = x2 + CW + g3, ys = {}; let k = 0;
      skel.forEach((n, i) => { for (let j = 0; j < n; j++, k++) ys[i + "." + j] = head + k * PIT + PIT / 2; ys[i] = (ys[i + ".0"] + ys[i + "." + (n - 1)]) / 2; });
      const y0 = skel.length ? (ys["0"] + ys[String(skel.length - 1)]) / 2 : head;
      return { head: head, FW: FW, CW: CW, OW: OW, x1: x1, x2: x2, x3: x3, ys: ys, y0: y0, H: head + nL * PIT, Wt: ends ? x3 + OW : x2 + CW };
    }
    const frac = (k, stage) => { const p = v.p[k] || ["", ""], nm = bn(k) + " (" + st[stage] + ")";
      return `<div class="tr-fr" data-v="${vt("s:p:" + k)}"><input class="tr-pn" data-k="${k}" data-h="0" type="text" inputmode="decimal" maxlength="6" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="next" aria-label="${esc(nm)}: probability, the top of the fraction or a decimal" value="${esc(p[0])}"${locked ? " disabled" : ""}>`
        + `<i class="tr-bar" aria-hidden="true"></i><input class="tr-pd" data-k="${k}" data-h="1" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="4" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="next" aria-label="${esc(nm)}: probability, the bottom of the fraction" value="${esc(p[1])}"${locked ? " disabled" : ""}></div>`; };
    const sel = (cls, k, opts, val, label) => `<select class="${cls}" data-k="${k}" data-v="${vt((cls === "tr-l" ? "s:lab:" : "s:out:") + k)}" data-empty="${!val}" aria-label="${esc(label)}"${locked ? " disabled" : ""}>`
      + `<option value=""${val ? "" : " selected"}>?</option>${opts.map(([vv, t]) => `<option value="${esc(vv)}"${val === vv ? " selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
    function render(focusSel) {
      if (focusSel === undefined) { const a = document.activeElement; focusSel = a && root.contains(a) && a.dataset.k ? `.${a.className.split(" ")[0]}[data-k="${a.dataset.k}"]` : null; }
      W = Math.max(280, Math.min(640, Math.floor(host.getBoundingClientRect().width || 320)));
      const G = geo(); root.dataset.locked = String(locked);
      plot.style.width = G.Wt + "px"; plot.style.height = G.H + "px"; plot.style.setProperty("--tr-fw", G.FW + "px"); plot.style.setProperty("--tr-ow", G.OW + "px");
      svgEl.setAttribute("viewBox", "0 0 " + G.Wt + " " + G.H); svgEl.setAttribute("width", G.Wt); svgEl.setAttribute("height", G.H);
      const ln = (a, b, c, d) => `<line x1="${a.toFixed(1)}" y1="${b.toFixed(1)}" x2="${c.toFixed(1)}" y2="${d.toFixed(1)}" class="tr-ln"/>`;
      let s = `<circle cx="7" cy="${G.y0.toFixed(1)}" r="4" class="tr-root"/>`;
      skel.forEach((n, i) => { s += ln(7, G.y0, G.x1, G.ys[i]); kids(i).forEach(k => { s += ln(G.x1 + G.CW, G.ys[i], G.x2, G.ys[k]); }); });
      svgEl.innerHTML = s;
      const L = OUT.map(x => [x, x]), cell = (k, x, stage) => `<div class="tr-cell" style="left:${x.toFixed(1)}px;top:${(G.ys[k] - 42).toFixed(1)}px">${frac(k, stage)}`
        + sel("tr-l", k, L, v.l[k], bn(k) + " (" + st[stage] + "): its outcome") + `</div>`;
      box.innerHTML = `<span class="tr-h" style="left:${G.x1.toFixed(1)}px">${esc(st[0])}</span><span class="tr-h" style="left:${G.x2.toFixed(1)}px">${esc(st[1])}</span>`
        + (ends ? `<span class="tr-h" style="right:0">Outcome</span>` : "")   /* (flush right, as its column is: at 320 px "Second marble" ran into it) */
        + skel.map((_, i) => cell(String(i), G.x1, 0) + kids(i).map(k => cell(k, G.x2, 1)
          + (ends ? `<div class="tr-end" style="left:${G.x3.toFixed(1)}px;top:${(G.ys[k] - 22).toFixed(1)}px">${sel("tr-o", k, combos.map(c => [c, cText(c)]), v.o[k], "The outcome at the end of " + bn(k))}</div>` : "")).join("")).join("");
      paint(); out.innerHTML = resHtml(); wire();
      if (focusSel) { const nd = root.querySelector(focusSel); if (nd && !nd.disabled) nd.focus({ preventScroll: true }); }
    }
    // what is NOT re-drawn as the learner types: the verdicts, the count, and a general rule's note (never the answer): the branches
    // from one point add up to 1, and no probability is more than 1
    function paint() {
      // (a decimal in the top box: the bar and the empty bottom box fade, so 0,4 does not read as a fraction left unfinished)
      box.querySelectorAll(".tr-fr").forEach(f => { const top = f.querySelector(".tr-pn"), bot = f.querySelector(".tr-pd"); f.dataset.v = vt("s:p:" + top.dataset.k);
        f.dataset.dec = String(/[.,]/.test(top.value) && !bot.value); });
      box.querySelectorAll("select").forEach(e => { e.dataset.v = vt((e.classList.contains("tr-l") ? "s:lab:" : "s:out:") + e.dataset.k); e.dataset.empty = String(!e.value); });
      const done = ALL.filter(k => v.l[k] && v.p[k] && v.p[k][0] !== "").length + (ends ? P2.filter(k => v.o[k]).length : 0), all = ALL.length + (ends ? P2.length : 0);
      hint.textContent = locked ? "" : "On each branch choose its outcome and type its probability: a fraction (top over bottom) or a decimal in the top box alone"
        + (ends ? "; at each end choose the outcome. " : ". ") + done + " of " + all + " done.";
      hint.hidden = locked;
      const val = k => trVal(v.p[k]), groups = [[skel.map((_, i) => String(i)), "the " + st[0].toLowerCase() + "'s branches"]].concat(skel.map((_, i) => [kids(i), "the branches after " + bn(String(i))]));
      const over = ALL.some(k => val(k) > 1 + 1e-9), off = groups.filter(([ks]) => ks.every(k => isFinite(val(k))) && Math.abs(ks.reduce((t, k) => t + val(k), 0) - 1) > 1e-6);
      note.innerHTML = locked ? "" : (over ? `<p class="sk-note">A probability is never more than 1.</p>` : "")
        + (off.length ? `<p class="sk-note">The probabilities on the branches from one point add up to 1: ${esc(off[0][1])} do not.</p>` : "");
    }
    const CRN = { branches: "Branches", p: "Probabilities", p1: "First-stage probabilities", p2: "Second-stage probabilities", out: "Outcomes" };
    function resHtml() {
      if (!items) return ""; const its = items.filter(it => it.key.slice(0, 2) !== "s:");
      return `<div class="bp-chips sk-res" role="status">${its.map(it => { const s = it.verdict === "correct" ? "true" : it.verdict === "partial" ? "part" : "false";
        const nm = CRN[it.key] || (it.key.slice(0, 7) === "branch:" ? "Branch " + it.key.slice(7).split(">").join(" → ") : it.key);
        return `<span class="bp-chip" data-ok="${s}">${s === "true" ? "✓" : s === "part" ? "◐" : "✕"} ${esc(nm)}${it.available ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
    }
    function wire() {
      if (locked) return;
      const order = [...box.querySelectorAll(".tr-pn, .tr-pd")];
      order.forEach((inp, idx) => {
        inp.oninput = () => { const k = inp.dataset.k, h = +inp.dataset.h;
          let t = h ? inp.value.replace(/\D/g, "").slice(0, 4) : inp.value.replace(/[^0-9.,]/g, "").replace(/([.,].*)[.,]/g, "$1").slice(0, 6);
          if (t !== inp.value) inp.value = t; const p = (v.p[k] || ["", ""]).slice(); p[h] = t;
          if (p[0] === "" && p[1] === "") delete v.p[k]; else v.p[k] = p; paint(); emit(); };
        inp.onkeydown = e => { if (e.key !== "Enter") return; e.preventDefault(); const nx = order[idx + 1]; if (nx) nx.focus(); else inp.blur(); };
      });
      box.querySelectorAll("select").forEach(e => { e.onchange = () => { const k = e.dataset.k, m = e.classList.contains("tr-l") ? v.l : v.o; if (e.value) m[k] = e.value; else delete m[k]; paint(); emit(); }; });
    }
    render(null);
    if (window.ResizeObserver) { ro = new ResizeObserver(() => { const w = Math.max(280, Math.min(640, Math.floor(host.getBoundingClientRect().width || 320))); if (Math.abs(w - W) >= 2) render(); }); ro.observe(host); }
    return { sync(s) {
        const nv = norm(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v), its = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? s.items : null;
        const lockCh = locked !== !!s.locked, itCh = JSON.stringify(items) !== JSON.stringify(its);
        v = nv; locked = !!s.locked; items = its;
        if (changed || lockCh) render(); else if (itCh) { paint(); out.innerHTML = resHtml(); } },   // (marks alone: the field being typed in stays)
      destroy() { if (ro) ro.disconnect(); host.innerHTML = ""; } };
  }

  // ── a GRAPH PLOTTED FROM DATA (2026-10-11, "plot"): "Use the information in the table and draw an accurate graph" BUILT on a grid.
  // Where the memo marks them, the axes' labels (both chosen from one list of quantities with units, sorted) and the scale (a value per
  // big square of the paper's blank grid) are chosen first. Each row of the data table is a chip, named as the table names it ("t = 2 s",
  // "20 < x ≤ 30", "Starting point"), never where it goes: tap one, then tap the grid (it snaps to the scale's step), drag a placed
  // point, or nudge the chosen one with the arrow buttons; keyboard: Enter on a chip places it mid-grid, the arrows move it (Shift: 5
  // steps), Delete removes it. Then the line: a straight line (fitted to the learner's own points; its two ends drag; extended to the
  // y-axis where the stem asks), a smooth curve through the points (Akima: straight wherever three points in a row are, no overshoot),
  // or the points joined by straight lines (an ogive's or a frequency polygon's, a line graph). A graph the paper already prints is drawn
  // under it (`given`). Tangent mode: a straight line through two ends the learner places, drawn across the given graph. The answer is
  // what is chosen and placed: the marker reads only that, against the memo's criteria, never the drawing.
  //   cfg   { x, y: { name?, min, max, step, minor?, snap } (the paper's scale) | { name?, unit, scales: [value per big square] } (chosen),
  //           grid?: { nx, ny, sub } (with scales: big squares across and up, small squares in each), labels?: [quantities with units],
  //           points: [{ id, name }], extend?, tangent?, lines?: false, given?: [{ name, pts?, curve?, segs?, dots?, dash? }],
  //           names: [each memo criterion's NEUTRAL chip name] }
  //   value { xl, yl, sx, sy, p: { id: [x, y] }, k: "best" | "curve" | "join", a, b: [x, y] (the straight line's ends), lf (the line
  //           follows the fit to the points), ex (extended to the y-axis) }
  let plN = 0;
  const PLK = [["best", "Straight line"], ["curve", "Smooth curve"], ["join", "Join the points"]];
  const plIc = d => `<svg viewBox="0 0 28 18" width="28" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;
  const plDot = (x, y) => `<circle cx="${x}" cy="${y}" r="1.9" fill="currentColor" stroke="none"/>`;
  const PLI = { best: plIc('<path d="M3 15L25 3"/>' + plDot(8, 10.8) + plDot(14, 9) + plDot(19, 5.2)),
    curve: plIc('<path d="M3 15C11 14 15 4 25 3"/>' + plDot(9, 13.4) + plDot(17, 6.6)), join: plIc('<path d="M3 15L10 8L17 11L25 3"/>' + plDot(10, 8) + plDot(17, 11)) };
  // an Akima spline through points sorted by x, one per x: f(x), NaN outside them. Each point's slope is a weighted mean of its
  // neighbours' (the weights the slope changes further out), so where three points lie in a row the curve between them IS the line
  // (Grade 10 P1 2018 3.3: straight from 0 to 3 s, curved after) and it never overshoots a corner the way a cubic spline does
  function akima(P) {
    const n = P.length; if (n < 2) return null;
    const x = P.map(p => p[0]), y = P.map(p => p[1]), m = [];
    for (let i = 0; i < n - 1; i++) m.push((y[i + 1] - y[i]) / (x[i + 1] - x[i]));
    if (n === 2) return u => u < x[0] - 1e-9 || u > x[1] + 1e-9 ? NaN : y[0] + m[0] * (u - x[0]);
    const M = i => i >= 0 && i < n - 1 ? m[i] : i === -1 ? 2 * m[0] - m[1] : i === -2 ? 3 * m[0] - 2 * m[1] : i === n - 1 ? 2 * m[n - 2] - m[n - 3] : 3 * m[n - 2] - 2 * m[n - 3];
    const t = x.map((_, i) => { const w1 = Math.abs(M(i + 1) - M(i)), w2 = Math.abs(M(i - 1) - M(i - 2)); return w1 + w2 < 1e-12 ? (M(i - 1) + M(i)) / 2 : (w1 * M(i - 1) + w2 * M(i)) / (w1 + w2); });
    return u => { if (!(u >= x[0] - 1e-9 && u <= x[n - 1] + 1e-9)) return NaN; let i = 0; while (i < n - 2 && u > x[i + 1]) i++;
      const h = x[i + 1] - x[i], s = (u - x[i]) / h, s2 = s * s, s3 = s2 * s;
      return (2 * s3 - 3 * s2 + 1) * y[i] + (s3 - 2 * s2 + s) * h * t[i] + (-2 * s3 + 3 * s2) * y[i + 1] + (s3 - s2) * h * t[i + 1]; };
  }
  // a number as the paper prints it: a decimal comma, thousands spaced (4 000, 0,735)
  const pfmt = n => { const r = Math.round(n * 1000) / 1000, s = String(Math.abs(r)).split("."); s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, " "); return (r < 0 ? "−" : "") + s.join(","); };
  // points sorted by x, one per x (a second at the same x is left out of a line through them)
  const plSorted = ps => ps.slice().sort((p, q) => p[0] - q[0]).filter((p, k, A) => !k || Math.abs(p[0] - A[k - 1][0]) > 1e-9);
  function plot(host, o) {
    const cfg = o.cfg, uid = "pl" + (++plN), PT = Array.isArray(cfg.points) ? cfg.points : [], TAN = !!cfg.tangent, LINES = !TAN && cfg.lines !== false;
    const CH = !!(cfg.grid && cfg.x.scales && cfg.y.scales), SUB = CH ? cfg.grid.sub || 10 : 0, NAMES = cfg.names || [];
    const LAB = Array.isArray(cfg.labels) && cfg.labels.length ? cfg.labels.slice().sort() : null;
    const isPt = u => Array.isArray(u) && u.length === 2 && u.every(n => typeof n === "number" && isFinite(n));
    const normV = val => { const x = clone(val), r = { p: {} };
      if (x.p && typeof x.p === "object") PT.forEach(q => { if (isPt(x.p[q.id])) r.p[q.id] = x.p[q.id].slice(); });
      if (LAB) ["xl", "yl"].forEach(k => { if (LAB.indexOf(x[k]) !== -1) r[k] = x[k]; });
      if (CH) [["sx", cfg.x], ["sy", cfg.y]].forEach(([k, c]) => { if (c.scales.indexOf(x[k]) !== -1) r[k] = x[k]; });
      if (LINES && PLK.some(q => q[0] === x.k)) r.k = x.k;
      if (r.k === "best" && isPt(x.a) && isPt(x.b)) { r.a = x.a.slice(); r.b = x.b.slice(); }
      if (r.k === "best" && x.lf) r.lf = 1;
      if (r.k === "best" && x.ex) r.ex = 1;
      return r; };
    let v = normV(o.value), locked = false, items = null, drag = null, W = 0, VH = 0, ro = null, pinUp = 0, sel = "", AX = null, AY = null;
    const placed = id => isPt(v.p[id]), ptName = id => ((PT.find(q => q.id === id) || {}).name || "");
    const firstOpen = after => { const i = PT.findIndex(q => q.id === after), L = PT.slice(i + 1).concat(PT.slice(0, i + 1)); return (L.find(q => !placed(q.id)) || {}).id || ""; };
    let act = firstOpen("");
    // an axis as it stands: the paper's, or from the learner's scale (from 0, a bold line every big square, a tap snaps to a small
    // square), null until it is chosen
    const axis = (c, s, n) => c.scales ? (s ? { min: 0, max: +(s * n).toFixed(9), step: s, minor: s / SUB, snap: +(s / SUB).toFixed(9) } : null)
      : { min: c.min, max: c.max, step: c.step, minor: c.minor || 0, snap: c.snap || c.minor || c.step };
    const resolve = () => { AX = axis(cfg.x, v.sx, CH ? cfg.grid.nx : 0); AY = axis(cfg.y, v.sy, CH ? cfg.grid.ny : 0); };
    resolve();
    const ready = () => !!(AX && AY);
    const snapA = (u, A) => +(Math.max(A.min, Math.min(A.max, A.min + Math.round((u - A.min) / A.snap) * A.snap))).toFixed(9);
    const mine = () => PT.filter(q => placed(q.id)).map(q => v.p[q.id]);
    // the straight line fitted to the learner's own points (least squares), from the first point's x (or the y-axis, extended) to the last
    const refit = () => { const ps = mine(), n = ps.length; if (n < 2) { delete v.a; delete v.b; return; }
      const mx = ps.reduce((t, p) => t + p[0], 0) / n, my = ps.reduce((t, p) => t + p[1], 0) / n, sxx = ps.reduce((t, p) => t + (p[0] - mx) * (p[0] - mx), 0);
      if (sxx < 1e-12) { delete v.a; delete v.b; return; }
      const m = ps.reduce((t, p) => t + (p[0] - mx) * (p[1] - my), 0) / sxx, f = x => my + m * (x - mx), r = q => +q.toFixed(9);
      const xs = ps.map(p => p[0]), x0 = v.ex && AX ? AX.min : Math.min(...xs), x1 = Math.max(...xs);
      v.a = [r(x0), r(f(x0))]; v.b = [r(x1), r(f(x1))]; };
    // extended to the y-axis: a fitted line refits from it; a line the learner placed moves its left end along itself
    const extend = () => { if (!AX || !v.a || !v.b) return; v.ex = 1; if (v.lf) return;
      const L = v.a[0] <= v.b[0] ? "a" : "b", R = L === "a" ? "b" : "a", m = (v[R][1] - v[L][1]) / (v[R][0] - v[L][0]); if (!isFinite(m)) return;
      v[L] = [AX.min, +(v[R][1] + m * (AX.min - v[R][0])).toFixed(9)]; };
    const emit = () => { resolve(); if (v.k === "best" && v.lf) refit(); v = normV(v); o.onChange(clone(v)); };
    // a text's width in this builder's font (the y numbers set the left margin)
    let FONT = "sans-serif", ctx2 = null;
    const tw = (s, size, weight) => { try { ctx2 = ctx2 || document.createElement("canvas").getContext("2d"); ctx2.font = (weight || 600) + " " + size + "px " + FONT; return ctx2.measureText(s).width + 1; }
      catch (_) { return s.length * size * 0.6; } };
    const inView = () => { for (let n = host.parentElement; n && n !== document.body; n = n.parentElement) { const ov = getComputedStyle(n).overflowY;
        if ((ov === "auto" || ov === "scroll") && n.clientHeight > 200 && n.clientHeight < (window.innerHeight || 700) - 40) return n.clientHeight; }
      return (window.innerHeight || 700) - (document.body.classList.contains("nx-compact") ? 210 : 120); };
    const ticks = A => { const out = []; for (let i = 0; A.min + i * A.step <= A.max + 1e-9; i++) out.push(+(A.min + i * A.step).toFixed(9)); return out; };
    const cardW = () => Math.max(240, Math.min(560, Math.floor(host.clientWidth || host.getBoundingClientRect().width || 320)));   // (layout width: a client rect is post-transform)
    const onStep = (u, A) => Math.abs((u - A.min) / A.step - Math.round((u - A.min) / A.step)) < 1e-6;
    // the axis to draw: the real one, or (a scale still to choose) the blank grid's big squares
    const drawAx = (A, n) => A || { min: 0, max: n, step: 1, minor: SUB ? 1 / SUB : 0, blank: true };
    // the grid as large as the card allows (560 px at most) and no taller than ~60% of what is in view, so the tray, the grid and the
    // line's choice are seen close together; a blank grid's squares stay square
    function geo() {
      const DX = drawAx(AX, CH ? cfg.grid.nx : 1), DY = drawAx(AY, CH ? cfg.grid.ny : 1), nx = (DX.max - DX.min) / DX.step, ny = (DY.max - DY.min) / DY.step;
      const yw = DY.blank ? 8 : Math.max(...ticks(DY).map(u => tw(pfmt(u), 11, 600)));
      const L = Math.ceil(yw) + 12, R = 18, T = 30, B = 40, A = CH ? ny / nx : Math.max(0.62, Math.min(1.15, ny / nx));
      let pw = Math.max(180, W - L - R), ph = pw * A; const cap = Math.max(190, Math.round(VH * 0.6) - T - B);
      if (ph > cap) { ph = cap; pw = Math.min(pw, Math.max(170, ph / A)); }
      return { DX: DX, DY: DY, w: Math.round(L + pw + R), h: Math.round(T + ph + B), L: L, T: T, pw: pw, ph: ph,
        X: x => L + (x - DX.min) / (DX.max - DX.min) * pw, Y: y => T + (DY.max - y) / (DY.max - DY.min) * ph,
        ux: px => DX.min + (px - L) / pw * (DX.max - DX.min), uy: py => DY.max - (py - T) / ph * (DY.max - DY.min) };
    }
    const pathThrough = (G, ps, curve) => { if (!curve || ps.length < 3) return ps.map((p, k) => (k ? "L" : "M") + G.X(p[0]).toFixed(1) + " " + G.Y(p[1]).toFixed(1)).join("");
      const f = akima(ps), x0 = ps[0][0], x1 = ps[ps.length - 1][0], N = 160; let d = "";
      for (let i = 0; i <= N; i++) { const x = x0 + (x1 - x0) * i / N; d += (i ? "L" : "M") + G.X(x).toFixed(1) + " " + G.Y(f(x)).toFixed(1); } return d; };
    function svgInner(G) {
      const DX = G.DX, DY = G.DY, x0 = G.X(DX.min), y0 = G.Y(DY.min), xe = G.L + G.pw, ye = G.T;
      const vl = (u, c) => `<line x1="${G.X(u).toFixed(1)}" x2="${G.X(u).toFixed(1)}" y1="${ye}" y2="${y0.toFixed(1)}" class="${c}"/>`;
      const hl = (u, c) => `<line x1="${x0.toFixed(1)}" x2="${xe.toFixed(1)}" y1="${G.Y(u).toFixed(1)}" y2="${G.Y(u).toFixed(1)}" class="${c}"/>`;
      let g = "", t = "";
      // the small squares (while 3.5 px apart), then a bold line every step
      if (DX.minor > 0 && DX.minor / (DX.max - DX.min) * G.pw >= 3.5) for (let i = 1; DX.min + i * DX.minor < DX.max - 1e-9; i++) { const u = DX.min + i * DX.minor; if (!onStep(u, DX)) g += vl(u, "pl-grid"); }
      if (DY.minor > 0 && DY.minor / (DY.max - DY.min) * G.ph >= 3.5) for (let i = 1; DY.min + i * DY.minor < DY.max - 1e-9; i++) { const u = DY.min + i * DY.minor; if (!onStep(u, DY)) g += hl(u, "pl-grid"); }
      ticks(DX).forEach(u => { g += vl(u, "pl-grid2"); }); ticks(DY).forEach(u => { g += hl(u, "pl-grid2"); });
      // the numbers: every k-th step, k the first that leaves room; one 0 at the corner
      const zero = !DX.blank && !DY.blank && DX.min === 0 && DY.min === 0;
      if (!DX.blank) { const tx = ticks(DX), wx = Math.max(...tx.map(u => tw(pfmt(u), 11, 600))), px = G.pw / ((DX.max - DX.min) / DX.step), k = [1, 2, 3, 4, 5, 10, 20].find(k => k * px >= wx + 6) || 50;
        tx.forEach((u, i) => { if (i % k || (zero && u === 0)) return; t += `<text x="${G.X(u).toFixed(1)}" y="${(y0 + 15).toFixed(1)}" class="pl-tick" text-anchor="middle">${pfmt(u)}</text>`; }); }
      if (!DY.blank) { const ty = ticks(DY), py = G.ph / ((DY.max - DY.min) / DY.step), k = [1, 2, 3, 4, 5, 10, 20].find(k => k * py >= 15) || 50;
        ty.forEach((u, i) => { if (i % k || (zero && u === 0)) return; t += `<text x="${(x0 - 5).toFixed(1)}" y="${(G.Y(u) + 4).toFixed(1)}" class="pl-tick" text-anchor="end">${pfmt(u)}</text>`; }); }
      if (zero) t += `<text x="${(x0 - 5).toFixed(1)}" y="${(y0 + 15).toFixed(1)}" class="pl-tick" text-anchor="end">0</text>`;
      // the axes and their names: the paper's, or the learner's choice ("choose its label" until one is chosen)
      const ax = `<line x1="${x0.toFixed(1)}" x2="${(xe + 8).toFixed(1)}" y1="${y0.toFixed(1)}" y2="${y0.toFixed(1)}" class="pl-axis"/><path d="M${(xe + 15).toFixed(1)} ${y0.toFixed(1)}l-8 -4v8z" class="pl-arrow"/>`
        + `<line x1="${x0.toFixed(1)}" x2="${x0.toFixed(1)}" y1="${y0.toFixed(1)}" y2="${ye - 8}" class="pl-axis"/><path d="M${x0.toFixed(1)} ${ye - 15}l-4 8h8z" class="pl-arrow"/>`;
      const yN = LAB ? v.yl : cfg.y.name, xN = LAB ? v.xl : cfg.x.name;
      t += `<text x="${(x0 + 10).toFixed(1)}" y="${ye - 12}" class="pl-name${yN ? "" : " pl-name0"}">${esc(yN || (LAB ? "y-axis: choose its label" : ""))}</text>`
        + `<text x="${xe.toFixed(1)}" y="${G.h - 6}" class="pl-name${xN ? "" : " pl-name0"}" text-anchor="end">${esc(xN || (LAB ? "x-axis: choose its label" : ""))}</text>`;
      // the graph the paper prints already, then the learner's line (or the tangent mode's line across the grid)
      let gv = "", ln = "";
      (cfg.given || []).forEach((s, si) => { const cls = `pl-gv pl-g${si % 3}${s.dash ? " pl-" + s.dash : ""}`;
        (s.segs || []).forEach(q => { gv += `<line x1="${G.X(q[0]).toFixed(1)}" y1="${G.Y(q[1]).toFixed(1)}" x2="${G.X(q[2]).toFixed(1)}" y2="${G.Y(q[3]).toFixed(1)}" class="${cls}"/>`; });
        if (Array.isArray(s.pts) && s.pts.length > 1) gv += `<path d="${pathThrough(G, plSorted(s.pts), !!s.curve)}" class="${cls}"/>`;
        (s.dots || []).forEach(d => { gv += `<circle cx="${G.X(d[0]).toFixed(1)}" cy="${G.Y(d[1]).toFixed(1)}" r="3.4" class="pl-gdot pl-g${si % 3}${d[2] ? " pl-open" : ""}"/>`; }); });
      if (!DX.blank && !DY.blank && LINES && v.k) { const ps = plSorted(mine());
        if (v.k === "best" && v.a && v.b) ln = `<line x1="${G.X(v.a[0]).toFixed(1)}" y1="${G.Y(v.a[1]).toFixed(1)}" x2="${G.X(v.b[0]).toFixed(1)}" y2="${G.Y(v.b[1]).toFixed(1)}" class="pl-line"/>`;
        else if (v.k !== "best" && ps.length >= 2) ln = `<path d="${pathThrough(G, ps, v.k === "curve")}" class="pl-line"/>`; }
      if (TAN && !DX.blank && placed("a") && placed("b")) { const A = v.p.a, B = v.p.b;
        if (Math.abs(B[0] - A[0]) < 1e-9) { if (Math.abs(B[1] - A[1]) > 1e-9) ln = vl(A[0], "pl-line"); }
        else { const m = (B[1] - A[1]) / (B[0] - A[0]), f = x => A[1] + m * (x - A[0]);
          ln = `<line x1="${x0.toFixed(1)}" y1="${G.Y(f(DX.min)).toFixed(1)}" x2="${xe.toFixed(1)}" y2="${G.Y(f(DX.max)).toFixed(1)}" class="pl-line"/>`; } }
      return `<defs><clipPath id="${uid}c"><rect x="${G.L}" y="${G.T}" width="${G.pw}" height="${G.ph}"/></clipPath></defs>`
        + `<rect x="${G.L}" y="${G.T}" width="${G.pw}" height="${G.ph}" class="pl-bg"/>${g}<rect x="${G.L}" y="${G.T}" width="${G.pw}" height="${G.ph}" class="pl-frame"/>`
        + `${ax}${t}<g clip-path="url(#${uid}c)">${gv}${ln}</g>`;
    }
    const valText = u => "(" + pfmt(u[0]) + " ; " + pfmt(u[1]) + ")", spoken = u => "x " + pfmt(u[0]) + ", y " + pfmt(u[1]);
    const vt = id => { const it = items && items.find(x => x.key === "s:" + id); return it ? (it.verdict === "correct" ? "ok" : it.verdict === "incorrect" ? "bad" : "") : ""; };
    const ENDS = [["@a", "a", "Line end 1"], ["@b", "b", "Line end 2"]];
    const valOf = id => id[0] === "@" ? v[id.slice(1)] : v.p[id];
    const nameOf = id => id[0] === "@" ? (id === "@a" ? "Line end 1" : "Line end 2") : ptName(id);
    const has = id => isPt(valOf(id));
    function pinsHtml(G) {
      if (!ready()) return "";
      const cx = px => Math.max(0, Math.min(G.w, px)), cy = py => Math.max(0, Math.min(G.h, py));
      const pin = (id, cls, u, label) => `<button type="button" class="sk-pin sk-point ${cls}" data-pin="${esc(id)}" data-act="${sel === id}" data-v="${vt(id)}"${locked ? ' tabindex="-1"' : ""}`
        + ` style="left:${cx(G.X(u[0])).toFixed(1)}px;top:${cy(G.Y(u[1])).toFixed(1)}px" aria-label="${esc(label)} at ${esc(spoken(u))}${locked ? "" : ". Arrow keys move it" + (id[0] === "@" ? "" : ", Delete removes it")}"></button>`;
      let h = PT.filter(q => placed(q.id)).map(q => pin(q.id, "pl-pin", v.p[q.id], q.name)).join("");
      if (LINES && v.k === "best" && v.a && v.b && !locked) h += ENDS.map(([id, k, nm]) => pin(id, "pl-end", v[k], nm + " of the straight line")).join("");
      const su = sel && has(sel) ? valOf(sel) : null;
      if (su) { const tx = valText(su), w = tw(tx, 11.5, 800) + 2, px = cx(G.X(su[0])), py = cy(G.Y(su[1])); let x = px + 11, y = py - 25;
        if (x + w > G.w - 2) x = px - 11 - w; if (y < 2) y = py + 10;
        h += `<span class="sk-tag pl-tag" aria-hidden="true" style="left:${x.toFixed(1)}px;top:${y.toFixed(1)}px">${tx}</span>`; }
      return h;
    }
    const chip = q => { const on = placed(q.id);
      return `<button type="button" class="sk-chip pl-chip" data-f="${esc(q.id)}" data-k="point" data-on="${on}" data-v="${vt(q.id)}" aria-pressed="${act === q.id}"${locked ? " disabled" : ""}`
        + ` aria-label="${esc(q.name)}${on ? ", at " + esc(spoken(v.p[q.id])) : ", not placed"}"><span class="sk-ic" aria-hidden="true"></span>`
        + `<span class="sk-cb"><span class="sk-cl">${esc(q.name)}</span><span class="sk-cv" data-on="${on}">${on ? valText(v.p[q.id]) : "not placed"}</span></span></button>`; };
    function setupHtml() {
      let s = "";
      if (LAB) s += `<div class="pl-labs">` + [["x", "Across (x-axis)"], ["y", "Up (y-axis)"]].map(([k, t]) => `<label class="pl-lab"><span class="sk-pl">${t}</span>`
        + `<select class="pl-sel" data-ax="${k}" aria-label="${t}: its label"${locked ? " disabled" : ""}><option value="">Choose its label…</option>${LAB.map(q => `<option${v[k + "l"] === q ? " selected" : ""}>${esc(q)}</option>`).join("")}</select></label>`).join("") + `</div>`;
      // (the unit once, in the row's name: "0,15 m·s⁻²" on each of four buttons wrapped them to two rows at 360 px)
      if (CH) s += [["x", "Across"], ["y", "Up"]].map(([k, t]) => { const c = cfg[k], u = c.unit ? " (" + esc(c.unit) + ")" : "";
        return `<div class="sk-pick pl-scale" role="group" aria-label="${t}: the value of one big square${esc(c.unit ? ", in " + c.unit : "")}"><span class="sk-pl">${t}: one big square is${u}</span>`
          + c.scales.map(sv => `<button type="button" class="sk-op" data-sc="${k}:${sv}" aria-pressed="${v["s" + k] === sv}"${locked ? " disabled" : ""}>${pfmt(sv)}</button>`).join("") + `</div>`; }).join("");
      return s;
    }
    function linesHtml() {
      if (!LINES) return "";
      let s = `<div class="sk-pick pl-kinds" role="group" aria-label="The line"><span class="sk-pl">The line</span>`
        + PLK.map(([k, t]) => `<button type="button" class="sk-op pl-k" data-k="${k}" aria-pressed="${v.k === k}"${locked || !ready() ? " disabled" : ""}>${PLI[k]}<span>${t}</span></button>`).join("") + `</div>`;
      if (v.k === "best" && !locked && ready()) { const acts = [];
        if (!v.lf && mine().length >= 2) acts.push(`<button type="button" class="sk-rm pl-fit">Fit it to my points</button>`);
        if (cfg.extend && v.a && v.b && Math.min(v.a[0], v.b[0]) > AX.min + 1e-9) acts.push(`<button type="button" class="sk-rm pl-ext">Extend it to the y-axis</button>`);
        if (acts.length) s += `<p class="sk-hint pl-acts">${acts.join("")}</p>`; }
      return s;
    }
    // the chosen point (or line end): its place and one snap step either way on each axis (44 px targets), and Remove
    function nudgeHtml() {
      if (locked || !sel || !ready() || !has(sel)) return ""; const u = valOf(sel), nm = nameOf(sel), sx = pfmt(AX.snap), sy = pfmt(AY.snap);
      return `<div class="nl-nd pl-nd" role="group" aria-label="Move ${esc(nm)}"><span class="nl-ndl">${esc(nm)} <b>${valText(u)}</b></span><span class="pl-nbs">`
        + [["x:-1", "←", "left", sx], ["x:1", "→", "right", sx], ["y:-1", "↓", "down", sy], ["y:1", "↑", "up", sy]].map(([d, g, w, st]) =>
          `<button type="button" class="nl-nb pl-nb" data-nd="${d}" aria-label="Move it ${st} ${w}">${g}</button>`).join("")
        + `</span>${sel[0] === "@" ? "" : `<button type="button" class="sk-rm nl-rm pl-rm">Remove</button>`}</div>`;
    }
    function footHtml() {
      if (locked) return "";
      const s = !ready() ? "Choose the scale on both axes first, then place the points."
        : act ? (placed(act) ? "Tap the grid to move “" : "Tap the grid to place “") + ptName(act) + "”."
        : LINES && !v.k ? "Now choose the line." : LINES && v.k === "best" ? "Drag either end of the line to move it." : "Tap a point to nudge it, or drag it.";
      return `<p class="sk-hint">${esc(s)}</p>` + (LINES && v.k && mine().length < 2 ? `<p class="sk-note">Place at least two points to draw a line.</p>` : "");
    }
    function resHtml() {
      if (!items) return ""; const its = items.filter(it => /^c\d+$/.test(it.key));
      return `<div class="bp-chips sk-res" role="status">${its.map(it => { const s = it.available > 0 && it.awarded >= it.available ? "true" : it.awarded > 0 ? "part" : "false";
        return `<span class="bp-chip" data-ok="${s}">${s === "true" ? "✓" : s === "part" ? "◐" : "✕"} ${esc(NAMES[+it.key.slice(1)] || "Criterion " + (+it.key.slice(1) + 1))}${it.available ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
    }
    host.innerHTML = `<div class="bp sk pl" data-locked="false"><div class="pl-setup"></div><div class="sk-tray pl-tray" role="group" aria-label="${TAN ? "The ends of the straight line" : "The points to plot"}"></div>`
      + `<div class="sk-plot pl-plot" role="group"><svg class="pl-svg" aria-hidden="true" focusable="false"></svg><div class="sk-pins"></div></div>`
      + `<div class="pl-legend"></div><div class="pl-nudge"></div><div class="pl-lines"></div><div class="pl-foot"></div><div class="sk-out"></div><p class="sr-only" aria-live="polite"></p></div>`;
    const root = host.firstChild, $ = s => root.querySelector(s), setup = $(".pl-setup"), tray = $(".pl-tray"), plotEl = $(".pl-plot"), svgEl = $(".pl-svg"), pins = $(".sk-pins"),
      legend = $(".pl-legend"), nudge = $(".pl-nudge"), lines = $(".pl-lines"), foot = $(".pl-foot"), out = $(".sk-out"), live = $("[aria-live]");
    const say = s => { live.textContent = s; };
    function paint() { const G = geo(); svgEl.setAttribute("viewBox", "0 0 " + G.w + " " + G.h); svgEl.setAttribute("width", G.w); svgEl.setAttribute("height", G.h);
      plotEl.style.width = G.w + "px"; plotEl.style.height = G.h + "px"; svgEl.innerHTML = svgInner(G); return G; }
    function render(focusSel) {
      if (focusSel === undefined) { const a = document.activeElement, d = a && root.contains(a) ? a.dataset : null;
        focusSel = !d ? null : d.pin ? `[data-pin="${d.pin}"]` : d.f ? `[data-f="${d.f}"]` : d.sc ? `[data-sc="${d.sc}"]` : d.ax ? `select[data-ax="${d.ax}"]` : d.nd ? `[data-nd="${d.nd}"]`
          : a.classList.contains("pl-k") ? `.pl-k[data-k="${d.k}"]` : a.classList.contains("pl-fit") ? ".pl-fit" : a.classList.contains("pl-ext") ? ".pl-ext" : null; }
      W = cardW(); VH = inView();
      try { FONT = getComputedStyle(root).fontFamily || FONT; } catch (_) { /* no style: the fallback measure */ }
      resolve(); root.dataset.locked = String(locked);
      if (locked) { act = ""; sel = ""; }
      if (sel && !has(sel)) sel = "";
      setup.innerHTML = setupHtml();
      const G = paint();
      pins.innerHTML = pinsHtml(G);
      // a tray whose rows and the grid would not fit in view together becomes ONE row of chips that scrolls sideways (the sketch's rule:
      // ML P1 Nov 2024 4.1.2(b) has ten points)
      const cols = Math.max(1, Math.floor(((tray.clientWidth || W) + 8) / 144)), rows = Math.ceil(PT.length / cols);
      const row = rows > 2 && 28 + rows * 60 + 12 + G.h > VH - 24, ti0 = tray.querySelector(".sk-ti"), sl = ti0 ? ti0.scrollLeft : 0, n = PT.filter(q => placed(q.id)).length;
      tray.dataset.row = String(row);
      tray.innerHTML = `<p class="sk-th"><span>${locked ? (TAN ? "Your line's ends" : "Your points") : TAN ? "Tap an end, then tap the grid" : "Tap a point, then tap the grid"}</span><span class="sk-n">${n} of ${PT.length} placed</span></p>`
        + `<div class="sk-ti">${PT.map(chip).join("")}</div>`;
      if (row) keepInRow(sl);
      plotEl.setAttribute("aria-label", ready() ? "Graph grid: x from " + pfmt(AX.min) + " to " + pfmt(AX.max) + ", y from " + pfmt(AY.min) + " to " + pfmt(AY.max) : "Graph grid: choose the scale first");
      legend.innerHTML = (cfg.given || []).map((s, si) => `<span class="pl-lg"><svg viewBox="0 0 30 10" width="30" height="10" aria-hidden="true"><line x1="2" y1="5" x2="28" y2="5" class="pl-gv pl-g${si % 3}${s.dash ? " pl-" + s.dash : ""}"/></svg>${esc(s.name)}</span>`).join("");
      nudge.innerHTML = nudgeHtml(); lines.innerHTML = linesHtml(); foot.innerHTML = footHtml(); out.innerHTML = resHtml();
      wire();
      if (focusSel) { const nd = root.querySelector(focusSel); if (nd && !nd.disabled) nd.focus({ preventScroll: true }); }
    }
    function keepInRow(sl) { const ti = tray.querySelector(".sk-ti"); if (!ti) return; ti.scrollLeft = sl;
      const edge = () => { ti.dataset.l = String(ti.scrollLeft > 2); ti.dataset.r = String(ti.scrollLeft + ti.clientWidth < ti.scrollWidth - 2); };
      ti.onscroll = edge;
      const c = ti.querySelector('[aria-pressed="true"]');
      if (c) { const l = c.offsetLeft, r = l + c.offsetWidth, m = 36; let to = ti.scrollLeft;
        if (l - m < to) to = Math.max(0, l - m); else if (r + m > to + ti.clientWidth) to = r + m - ti.clientWidth;
        if (Math.abs(to - ti.scrollLeft) > 1) ti.scrollTo({ left: to, behavior: o.reduced ? "auto" : "smooth" }); }
      edge(); }
    const fromEvent = e => { const r = svgEl.getBoundingClientRect(), G = geo(), px = (e.clientX - r.left) * G.w / (r.width || G.w), py = (e.clientY - r.top) * G.h / (r.height || G.h);
      return [snapA(G.ux(px), AX), snapA(G.uy(py), AY)]; };
    const nearest = e => { const r = svgEl.getBoundingClientRect(), G = geo(), px = (e.clientX - r.left) * G.w / (r.width || G.w), py = (e.clientY - r.top) * G.h / (r.height || G.h);
      let best = "", bd = 26; PT.forEach(q => { if (!placed(q.id)) return; const d = Math.hypot(G.X(v.p[q.id][0]) - px, G.Y(v.p[q.id][1]) - py); if (d < bd) { bd = d; best = q.id; } }); return best; };
    // a point placed or moved (announced), or a line end moved (the line then stays where the learner put it: no more fitting)
    const setVal = (id, u, quiet) => { if (id[0] === "@") { v[id.slice(1)] = u; delete v.lf; return; }
      const was = placed(id); v.p[id] = u; if (!quiet) say(ptName(id) + (was ? " moved to " : " placed at ") + spoken(u)); };
    function wire() {
      setup.querySelectorAll("select[data-ax]").forEach(s => s.onchange = () => { if (locked) return; const k = s.dataset.ax + "l"; if (s.value) v[k] = s.value; else delete v[k];
        say((s.dataset.ax === "x" ? "The x-axis: " : "The y-axis: ") + (s.value || "no label")); emit(); render(`select[data-ax="${s.dataset.ax}"]`); });
      setup.querySelectorAll("[data-sc]").forEach(b => b.onclick = () => { if (locked) return; const [k, val] = b.dataset.sc.split(":"); v["s" + k] = +val;
        say((k === "x" ? "Across" : "Up") + ", one big square is " + pfmt(+val) + " " + (cfg[k].unit || "")); emit(); render(`[data-sc="${b.dataset.sc}"]`); });
      tray.querySelectorAll("[data-f]").forEach(b => b.onclick = e => { if (locked) return; const id = b.dataset.f; act = id; if (placed(id)) sel = id;
        if (!ready()) { say("Choose the scale on both axes first"); render(`[data-f="${id}"]`); return; }
        if (e.detail === 0) {   // the keyboard (or a screen reader): placed mid-grid if new, then its pin takes the focus for the arrows
          if (!placed(id)) { setVal(id, [snapA((AX.min + AX.max) / 2, AX), snapA((AY.min + AY.max) / 2, AY)]); emit(); }
          sel = id; render(`[data-pin="${id}"]`); return; }
        render(`[data-f="${id}"]`); });
      lines.querySelectorAll(".pl-k").forEach(b => b.onclick = () => { if (locked || !ready()) return; v.k = b.dataset.k;
        if (v.k === "best") v.lf = 1; else { delete v.a; delete v.b; delete v.lf; delete v.ex; if (sel[0] === "@") sel = ""; }
        say((PLK.find(q => q[0] === v.k) || [])[1] + " chosen"); emit(); render(`.pl-k[data-k="${v.k}"]`); });
      const fit = lines.querySelector(".pl-fit"); if (fit) fit.onclick = () => { if (locked) return; v.lf = 1; emit(); say("The line is fitted to your points"); render('.pl-k[data-k="best"]'); };
      const ext = lines.querySelector(".pl-ext"); if (ext) ext.onclick = () => { if (locked) return; extend(); emit(); say("The line is extended to the y-axis"); render('.pl-k[data-k="best"]'); };
      nudge.querySelectorAll("[data-nd]").forEach(b => b.onclick = () => { if (locked || !sel || !has(sel)) return; const [ax, d] = b.dataset.nd.split(":"), u = valOf(sel).slice();
        if (ax === "x") u[0] = snapA(u[0] + +d * AX.snap, AX); else u[1] = snapA(u[1] + +d * AY.snap, AY); setVal(sel, u); emit(); render(`[data-nd="${b.dataset.nd}"]`); });
      const rm = nudge.querySelector(".pl-rm"); if (rm) rm.onclick = () => { if (locked || !sel || sel[0] === "@") return; const id = sel; delete v.p[id]; sel = ""; act = id; say(ptName(id) + " removed"); emit(); render(`[data-f="${id}"]`); };
      // a tap on the grid places (or moves) the chosen point, or with none chosen picks the nearest one; a swipe scrolls the page
      plotEl.onclick = e => { if (locked || drag || e.target.closest(".sk-pin") || Date.now() - pinUp < 450) return;
        if (!ready()) { say("Choose the scale on both axes first"); return; }
        if (!act) { const id = nearest(e); if (id) { sel = id; render(null); } return; }
        const id = act, was = placed(id); setVal(id, fromEvent(e)); sel = id; act = was ? "" : firstOpen(id); emit(); render(null); };
      pins.querySelectorAll(".sk-pin").forEach(b => { const id = b.dataset.pin;
        b.onpointerdown = e => { if (locked) return; e.preventDefault(); e.stopPropagation(); try { b.setPointerCapture(e.pointerId); } catch (_) { /* a synthetic pointer */ }
          b.focus({ preventScroll: true }); const r = svgEl.getBoundingClientRect(), G = geo(), s = r.width / G.w, cur = valOf(id);
          drag = { id: id, x: e.clientX, y: e.clientY, ox: r.left + G.X(cur[0]) * s - e.clientX, oy: r.top + G.Y(cur[1]) * s - e.clientY, moved: false }; document.documentElement.classList.add("bp-drag"); };
        b.onpointermove = e => { if (!drag || drag.id !== id) return; if (!drag.moved && Math.hypot(e.clientX - drag.x, e.clientY - drag.y) < 4) return; drag.moved = true;
          const u = fromEvent({ clientX: e.clientX + drag.ox, clientY: e.clientY + drag.oy }), cur = valOf(id); if (u[0] === cur[0] && u[1] === cur[1]) return;
          setVal(id, u, true); if (v.k === "best" && v.lf && id[0] !== "@") refit();
          const G = paint(); b.style.left = G.X(u[0]) + "px"; b.style.top = G.Y(u[1]) + "px";   // (this pin moves; the grid and the line repaint under it)
          const tag = pins.querySelector(".pl-tag"); if (tag) { tag.textContent = valText(u); tag.style.left = (G.X(u[0]) + 11) + "px"; tag.style.top = (G.Y(u[1]) - 25) + "px"; } };
        const end = () => { if (!drag || drag.id !== id) return; const moved = drag.moved; drag = null; pinUp = Date.now(); document.documentElement.classList.remove("bp-drag");
          sel = id; if (moved) { say(nameOf(id) + " moved to " + spoken(valOf(id))); if (act === id) act = ""; emit(); } render(`[data-pin="${id}"]`); };
        b.onpointerup = end; b.onpointercancel = end; b.onclick = e => e.stopPropagation();
        b.onkeydown = e => { if (locked) return; const st = e.shiftKey ? 5 : 1, d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key], cur = valOf(id);
          if (d) { e.preventDefault(); const u = [snapA(cur[0] + d[0] * st * AX.snap, AX), snapA(cur[1] + d[1] * st * AY.snap, AY)]; if (u[0] === cur[0] && u[1] === cur[1]) return;
            sel = id; setVal(id, u); emit(); render(`[data-pin="${id}"]`); return; }
          if ((e.key === "Delete" || e.key === "Backspace") && id[0] !== "@") { e.preventDefault(); delete v.p[id]; sel = ""; act = id; say(ptName(id) + " removed"); emit(); render(`[data-f="${id}"]`); return; }
          if (e.key === "Enter" || e.key === "Escape") { e.preventDefault(); const nx = e.key === "Enter" && id[0] !== "@" ? firstOpen(id) : ""; if (nx) act = nx;
            render(nx ? `[data-f="${nx}"]` : id[0] === "@" ? '.pl-k[data-k="best"]' : `[data-f="${id}"]`); } };
      });
    }
    render(null);
    // (the first render is mid-transition: a scaled card measured 277 px for 328 and the play screen's compact class was not on yet, so
    // the grid grew 27 px on the first tap; it is measured again two frames and a moment later, and on any resize)
    const refresh = () => { if (!drag && root.isConnected && (Math.abs(cardW() - W) >= 2 || Math.abs(inView() - VH) >= 8)) render(); };
    requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(refresh, 150)));
    if (window.ResizeObserver) { ro = new ResizeObserver(refresh); ro.observe(host); }
    const mo = window.MutationObserver ? new MutationObserver(refresh) : null;   // (the compact class lands on the body after the mount)
    if (mo) mo.observe(document.body, { attributes: true, attributeFilter: ["class"] });
    return { sync(s) { const nv = normV(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v);
        const its = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? s.items : null, was = locked + "|" + JSON.stringify(items);
        v = nv; locked = !!s.locked; items = its; resolve();
        if (changed && !Object.keys(nv.p).length) { act = firstOpen(""); sel = ""; }   // a fresh try starts at the first point
        // (the host's render can change the room: the play screen turns compact after the builder mounts, and the card's 459 px scroller
        // gives way to the page: re-measured here, as the host syncs after each render)
        const room = Math.abs(cardW() - W) >= 2 || Math.abs(inView() - VH) >= 8;
        if ((changed || room || was !== locked + "|" + JSON.stringify(items)) && !drag) render(); },
      destroy() { if (ro) ro.disconnect(); if (mo) mo.disconnect(); document.documentElement.classList.remove("bp-drag"); host.innerHTML = ""; } };
  }

  // ── the FORCE DIAGRAM builder (2026-10-11, "forces"; Murci picked direction A of the mock-up, "tap and aim"): "Draw a labelled
  // free-body diagram" BUILT from a dot. The tray holds the SAME seven forces for every force question (never only the ones that act,
  // so it tells nothing): tap a force, then tap the diagram where it points; the arrow grows from the dot towards the tap, in 5° steps
  // on a uniform ring (no tick sits on the right answer). Tap a head to choose it, then tap the diagram to re-aim it, or drag its head;
  // Remove sits by the hint. Keyboard: Enter on a force draws it pointing right with its head focused, the arrow keys turn it (5°,
  // Shift 15°), Delete removes it. Where the question asks for an angle (a VECTOR DIAGRAM, "indicate at least ONE angle"): Mark an
  // angle, then two lines (an arrow, or a dashed guide: by a tap near it or its button); the arc shows the angle between them, worked
  // out from the learner's own arrows. Length is not marked (a free-body memo marks label and direction). The answer is the arrows
  // (label, direction) and the angle's two lines; the marker reads only those, against the memo's forces.
  //   cfg   { surface?: degrees (the surface the body rests on, as the paper's figure draws it: 0 level, 30 rising to the right, −15
  //           falling to the right), body?: "box" | "sphere" (a faint outline round the dot), angle?: true }
  //   value { f: [{ l: a force id (FZ), a: degrees anticlockwise from the right, r: length as a share of the ring (0,3 to 1) }],
  //           ang?: [line, line] (a line: "f<i>", the i-th arrow, or a guide: "V90" up, "V270" down, "H0" right, "H180" left) }
  const FZ = [{ id: "Fg", s: "F", sub: "g", name: "weight" }, { id: "FN", s: "F", sub: "N", name: "normal force" }, { id: "f", s: "f", sub: "", name: "friction" },
    { id: "FA", s: "F", sub: "A", name: "applied force" }, { id: "T", s: "T", sub: "", name: "tension" }, { id: "FE", s: "F", sub: "E", name: "electrostatic force" },
    { id: "Fnet", s: "F", sub: "net", name: "net force" }];
  const FZG = [["V90", "the vertical, up", 90], ["V270", "the vertical, down", 270], ["H0", "the horizontal, right", 0], ["H180", "the horizontal, left", 180]];
  const fzL = id => FZ.find(x => x.id === id), fzName = id => (fzL(id) || {}).name || "arrow";
  const fzSym = id => { const l = fzL(id); return l ? `<i>${l.s}</i>${l.sub ? `<sub>${l.sub}</sub>` : ""}` : "?"; };
  const fzSvgSym = id => { const l = fzL(id); return l ? `<tspan font-style="italic">${l.s}</tspan>${l.sub ? `<tspan class="fz-sub" dy="4">${l.sub}</tspan>` : ""}` : "?"; };
  const fzN = a => ((Math.round(a) % 360) + 360) % 360, fzDif = (p, q) => { const d = Math.abs(fzN(p) - fzN(q)); return Math.min(d, 360 - d); };
  const fzSnap = a => fzN(Math.round(a / 5) * 5), fzAng = (dx, dy) => fzN(Math.atan2(-dy, dx) * 180 / Math.PI), fzRad = a => a * Math.PI / 180, f1 = n => n.toFixed(1);
  // neutral words for a direction (the page's own terms: never "perpendicular to the slope", which would name an answer)
  const fzWords = a => { a = fzN(a);
    if (a === 0) return "pointing right"; if (a === 90) return "pointing straight up"; if (a === 180) return "pointing left"; if (a === 270) return "pointing straight down";
    if (a < 90) return "pointing up and right, " + a + "° above the horizontal"; if (a < 180) return "pointing up and left, " + (180 - a) + "° above the horizontal";
    if (a < 270) return "pointing down and left, " + (a - 180) + "° below the horizontal"; return "pointing down and right, " + (360 - a) + "° below the horizontal"; };
  let fzUid = 0;
  function forces(host, o) {
    const cfg = o.cfg, uid = "fz" + (++fzUid), ANG = !!cfg.angle, SURF = typeof cfg.surface === "number" ? cfg.surface : null, BODY = cfg.body || (SURF != null ? "box" : "");
    const normV = val => { const x = clone(val), f = (Array.isArray(x.f) ? x.f : []).filter(ar => ar && fzL(ar.l) && typeof ar.a === "number" && isFinite(ar.a))
        .map(ar => ({ l: ar.l, a: fzN(ar.a), r: Math.max(0.3, Math.min(1, typeof ar.r === "number" && isFinite(ar.r) ? Math.round(ar.r * 100) / 100 : 0.8)) }));
      const okRef = r => typeof r === "string" && (/^f\d+$/.test(r) ? +r.slice(1) < f.length : FZG.some(g => g[0] === r));
      const b = { f: f }; if (ANG && Array.isArray(x.ang) && x.ang.length === 2 && x.ang.every(okRef) && x.ang[0] !== x.ang[1]) b.ang = x.ang.slice(); return b; };
    let v = normV(o.value), locked = false, items = null, act = "", sel = -1, pick = null, drag = null, pinUp = 0, W = 0, VH = 0, G = null, ro = null;
    const emit = () => o.onChange(clone(v));
    // what is in view (the scroller the builder sits in, else the window less the header and the dock), as the sketch builder reckons it
    const inView = () => { for (let n = host.parentElement; n && n !== document.body; n = n.parentElement) { const ov = getComputedStyle(n).overflowY;
        if ((ov === "auto" || ov === "scroll") && n.clientHeight > 200 && n.clientHeight < (window.innerHeight || 700) - 40) return n.clientHeight; }
      return (window.innerHeight || 700) - (document.body.classList.contains("nx-compact") ? 210 : 120); };
    // the diagram: a phone's whole width, never so tall that the tray, the diagram, the hint and the host's Check arrow are not in view
    // together (the first arrow opens Check, and the host scrolls the page to bring it over the face strip: at 360 x 702 a 328 px
    // diagram pushed the tray under the header, so the next force could not be picked without scrolling back); from 560 px (a tablet's
    // card is 590) a square beside the tray (the tray, the hint and the marks to its right), as tall as the card's view allows
    function geo() {
      const wide = W >= 560; let w, h;
      if (wide) { w = h = Math.max(280, Math.min(420, Math.round(W * 0.56), VH - 120)); }
      else { w = W; h = Math.max(220, Math.min(W, 340, VH - 250)); }
      return { w: w, h: h, cx: Math.round(w / 2), cy: Math.round(h / 2), R: Math.round(Math.min(w, h) / 2 - 30), wide: wide };
    }
    const tip = ar => ({ x: G.cx + Math.cos(fzRad(ar.a)) * ar.r * G.R, y: G.cy - Math.sin(fzRad(ar.a)) * ar.r * G.R });
    const verdict = i => { const it = items && items.find(x => x.key === "f" + i); return !it ? "" : it.verdict === "correct" ? "ok" : it.verdict === "unmarked" ? "" : "bad"; };
    const lineRay = ref => { if (typeof ref !== "string") return null; if (ref[0] === "f") { const ar = v.f[+ref.slice(1)]; return ar ? ar.a : null; } const g = FZG.find(x => x[0] === ref); return g ? g[2] : null; };
    const lineName = ref => ref[0] === "f" ? "the " + fzName((v.f[+ref.slice(1)] || {}).l) : (FZG.find(x => x[0] === ref) || [0, "a line"])[1];
    const angInfo = () => { if (!v.ang) return null; const p = lineRay(v.ang[0]), q = lineRay(v.ang[1]); return p == null || q == null ? null : { p: p, q: q, val: fzDif(p, q) }; };
    // each label beyond its head; where it would sit on another label, another arrow, the dot or the edge, the least bad of a few spots
    // round the head (two arrows the same way, as the tow truck's f and T, get their labels side by side)
    function labelSpots(list) {
      const segs = list.map(p => [G.cx, G.cy, p.t.x, p.t.y]), out = [], placed = [];
      const dseg = (x, y, s) => { const vx = s[2] - s[0], vy = s[3] - s[1], L2 = vx * vx + vy * vy || 1, t = Math.max(0, Math.min(1, ((x - s[0]) * vx + (y - s[1]) * vy) / L2));
        return Math.hypot(x - s[0] - t * vx, y - s[1] - t * vy); };
      list.forEach((p, k) => { const dx = Math.cos(fzRad(p.a)), dy = -Math.sin(fzRad(p.a)), px = -dy, py = dx, l = fzL(p.l) || { sub: "" }, wl = 13 + l.sub.length * 7;
        let best = null, bs = Infinity;
        [[17, 0], [17, 21], [17, -21], [17, 40], [17, -40], [32, 0], [4, 26], [4, -26], [32, 24], [32, -24]].forEach(([al, off], ci) => {
          const x = p.t.x + dx * al + px * off, y = p.t.y + dy * al + py * off + 1; let s = ci * 0.1;
          if (x - wl / 2 < 3 || x + wl / 2 > G.w - 3 || y < 11 || y > G.h - 11) s += 100;
          if (placed.some(q => Math.abs(q.x - x) < (q.w + wl) / 2 + 3 && Math.abs(q.y - y) < 19)) s += 1000;
          segs.forEach((sg, j) => { if (j !== k && dseg(x, y, sg) < 12) s += 5; });
          if (Math.hypot(x - G.cx, y - G.cy) < 18) s += 50;
          if (s < bs) { bs = s; best = { x: x, y: y, w: wl }; } });
        placed.push(best); out[k] = best; });
      return out;
    }
    function arrowSvg(ar, i, lab, temp) {
      const a = fzRad(ar.a), dx = Math.cos(a), dy = -Math.sin(a), t = tip(ar), bx = t.x - dx * 12, by = t.y - dy * 12, px = -dy, py = dx;
      return `<g class="fz-g" data-sel="${!temp && sel === i}" data-v="${temp ? "" : verdict(i)}" data-temp="${!!temp}"><line x1="${G.cx}" y1="${G.cy}" x2="${f1(bx)}" y2="${f1(by)}" class="fz-ar"/>`
        + `<path d="M${f1(t.x)} ${f1(t.y)}L${f1(bx + px * 6.5)} ${f1(by + py * 6.5)}L${f1(bx - px * 6.5)} ${f1(by - py * 6.5)}Z" class="fz-hd"/>`
        + (!temp && sel === i ? `<circle cx="${f1(t.x)}" cy="${f1(t.y)}" r="15" class="fz-selr"/>` : "")
        + (lab ? `<text x="${f1(lab.x)}" y="${f1(lab.y)}" class="fz-lab" text-anchor="middle" dominant-baseline="central">${fzSvgSym(ar.l)}</text>` : "") + `</g>`;
    }
    function svgInner(temp) {
      const w = G.w, h = G.h, cx = G.cx, cy = G.cy, R = G.R;
      let s = `<defs><clipPath id="${uid}c"><rect x="1" y="1" width="${w - 2}" height="${h - 2}" rx="13"/></clipPath></defs><rect x="0.5" y="0.5" width="${w - 1}" height="${h - 1}" rx="14" class="fz-bg"/>`;
      // the body, faint: on the surface the paper's figure gives (so no hint), or a block or sphere on its own
      if (SURF != null) { const a = fzRad(SURF), ux = Math.cos(a), uy = -Math.sin(a), nx = -Math.sin(a), ny = -Math.cos(a), x0 = cx - nx * 23, y0 = cy - ny * 23;
        s += `<g clip-path="url(#${uid}c)"><line x1="${f1(x0 - ux * w)}" y1="${f1(y0 - uy * w)}" x2="${f1(x0 + ux * w)}" y2="${f1(y0 + uy * w)}" class="fz-surf"/></g>`; }
      if (BODY === "sphere") s += `<circle cx="${cx}" cy="${cy}" r="19" class="fz-ghost"/>`;
      else if (BODY) s += `<rect x="${cx - 21}" y="${cy - 21}" width="42" height="42" rx="3" class="fz-ghost"${SURF ? ` transform="rotate(${-SURF} ${cx} ${cy})"` : ""}/>`;
      // a uniform protractor ring (a tick every 15°, the same for every question) and the dashed vertical and horizontal guides
      s += `<circle cx="${cx}" cy="${cy}" r="${R}" class="fz-ring"/>`;
      for (let k = 0; k < 24; k++) { const a = fzRad(k * 15), big = k % 6 === 0, r0 = R - (big ? 10 : 5);
        s += `<line x1="${f1(cx + Math.cos(a) * r0)}" y1="${f1(cy - Math.sin(a) * r0)}" x2="${f1(cx + Math.cos(a) * R)}" y2="${f1(cy - Math.sin(a) * R)}" class="${big ? "fz-tick2" : "fz-tick"}"/>`; }
      s += `<line x1="${cx - R}" x2="${cx + R}" y1="${cy}" y2="${cy}" class="fz-guide"/><line x1="${cx}" x2="${cx}" y1="${cy - R}" y2="${cy + R}" class="fz-guide"/>`;
      if (pick && pick.first) { const a = lineRay(pick.first); if (a != null) s += `<line x1="${cx}" y1="${cy}" x2="${f1(cx + Math.cos(fzRad(a)) * R)}" y2="${f1(cy - Math.sin(fzRad(a)) * R)}" class="fz-pick"/>`; }
      const A = angInfo();
      if (A) { const r = 34; let a1 = A.p, a2 = A.q; if (fzN(a2 - a1) > 180) { const t = a1; a1 = a2; a2 = t; }
        const p1 = [cx + Math.cos(fzRad(a1)) * r, cy - Math.sin(fzRad(a1)) * r], p2 = [cx + Math.cos(fzRad(a2)) * r, cy - Math.sin(fzRad(a2)) * r], mid = fzRad(a1 + fzN(a2 - a1) / 2);
        s += `<path d="M${f1(p1[0])} ${f1(p1[1])}A${r} ${r} 0 0 0 ${f1(p2[0])} ${f1(p2[1])}" class="fz-arc"/>`
          + `<text x="${f1(cx + Math.cos(mid) * (r + 15))}" y="${f1(cy - Math.sin(mid) * (r + 15))}" class="fz-arct" text-anchor="middle" dominant-baseline="central">${Math.round(A.val)}°</text>`; }
      const list = v.f.map(ar => ({ a: ar.a, l: ar.l, t: tip(ar) })), labs = labelSpots(list);
      v.f.forEach((ar, i) => { s += arrowSvg(ar, i, labs[i], false); });
      if (temp) s += arrowSvg(temp, -1, null, true);
      return s + `<circle cx="${cx}" cy="${cy}" r="6.5" class="fz-dot"/>`;
    }
    host.innerHTML = `<div class="bp fz" data-locked="false"><div class="fz-lay"><div class="fz-tray"></div>`
      + `<div class="fz-main"><div class="fz-plot" role="group"><svg class="fz-svg" aria-hidden="true" focusable="false"></svg><div class="fz-pins"></div></div></div>`
      + `<div class="fz-side"><p class="sk-hint fz-hint"></p><div class="fz-out"></div></div></div><p class="sr-only" aria-live="polite"></p></div>`;
    const root = host.firstChild, lay = root.querySelector(".fz-lay"), tray = root.querySelector(".fz-tray"), plot = root.querySelector(".fz-plot"), svgEl = root.querySelector(".fz-svg"),
      pins = root.querySelector(".fz-pins"), hint = root.querySelector(".fz-hint"), out = root.querySelector(".fz-out"), live = root.querySelector("[aria-live]");
    const say = s => { live.textContent = ""; setTimeout(() => { live.textContent = s; }, 30); };
    function paint(temp) { svgEl.setAttribute("viewBox", "0 0 " + G.w + " " + G.h); svgEl.setAttribute("width", G.w); svgEl.setAttribute("height", G.h);
      plot.style.width = G.w + "px"; plot.style.height = G.h + "px"; svgEl.innerHTML = svgInner(temp); }
    const chip = l => { const n = v.f.filter(a => a.l === l.id).length;
      return `<button type="button" class="fz-chip" data-force="${l.id}" aria-pressed="${act === l.id}"${locked ? " disabled" : ""} aria-label="${esc(l.name)}${n ? ", " + n + " drawn" : ""}">`
        + `<span class="fz-sym" aria-hidden="true">${fzSym(l.id)}</span><span class="fz-cs" aria-hidden="true">${esc(l.name)}</span>${n ? `<span class="fz-count" aria-hidden="true">${n}</span>` : ""}</button>`; };
    function resHtml() {
      if (!items) return ""; const ch = [];
      v.f.forEach((ar, i) => { const it = items.find(x => x.key === "f" + i); if (!it) return;
        const t = it.verdict === "correct" ? ["true", "✓", it.available ? " " + it.awarded + "/" + it.available : ""] : it.verdict === "unmarked" ? ["info", "·", " not marked here"]
          : it.verdict === "extra" ? ["false", "✕", " extra force −1"] : ["false", "✕", " wrong way 0/" + (it.available || 1)];
        ch.push(`<span class="bp-chip fz-rc" data-ok="${t[0]}">${t[1]} <span class="fz-sym">${fzSym(ar.l)}</span>${t[2]}</span>`); });
      // a force left out is COUNTED, never named: a retry is not handed the answer
      const miss = items.find(x => x.key === "missing"); if (miss && miss.n) ch.push(`<span class="bp-chip" data-ok="info">${miss.n} ${miss.n > 1 ? "forces" : "force"} missing</span>`);
      const an = items.find(x => x.key === "angle");
      if (an) { const ok = an.verdict === "correct"; ch.push(`<span class="bp-chip" data-ok="${ok}">${ok ? "✓" : "✕"} Angle${an.available ? " " + an.awarded + "/" + an.available : ""}</span>`); }
      return `<div class="bp-chips sk-res fz-res" role="status">${ch.join("")}</div>`;
    }
    function hintHtml() {
      if (locked) return "";
      if (pick) return (pick.first ? "Now the second line: tap near it, or its button." : "The angle's first line: tap near an arrow or a dashed guide.")
        + ` <button type="button" class="sk-rm" data-cancel>Cancel</button>`;
      if (act) return "Tap the diagram in the direction the " + esc(fzName(act)) + " points.";
      // (short, so the hint keeps to two lines: "the electrostatic force" ran it to three, which moved the host's Check and scrolled the page)
      if (sel >= 0 && v.f[sel]) return "Tap to re-aim it, or drag its head. <button type=\"button\" class=\"sk-rm\" data-rm>Remove</button>";
      if (!v.f.length) return "Pick a force, then tap the diagram where it points. Every arrow starts at the dot.";
      return "Tap an arrow's head to change it." + (v.ang ? ` <button type="button" class="sk-rm" data-noang>Remove the angle</button>` : "");
    }
    function render(focusSel) {
      if (focusSel === undefined) { const a = document.activeElement; focusSel = a && root.contains(a) ? (a.dataset.i != null ? `[data-i="${a.dataset.i}"]` : a.dataset.force ? `[data-force="${a.dataset.force}"]`
        : a.dataset.gp ? `[data-gp="${a.dataset.gp}"]` : null) : null; }
      W = Math.max(260, Math.min(760, Math.floor(host.getBoundingClientRect().width || 320))); VH = inView(); G = geo();
      root.dataset.locked = String(locked); lay.dataset.wide = String(G.wide);
      paint();
      plot.setAttribute("aria-label", "Force diagram: every arrow starts at the dot. " + v.f.length + (v.f.length === 1 ? " arrow" : " arrows") + (angInfo() ? ", an angle of " + angInfo().val + "° marked" : ""));
      // a phone (the diagram under the tray, not beside it): ONE row of chips that scrolls sideways, the chosen one kept in view (the
      // sketch builder's row), so the tray and the diagram are in view together above the dock; beside the diagram, the chips wrap
      const row = !G.wide, ti0 = tray.querySelector(".fz-ti"), sl = ti0 ? ti0.scrollLeft : 0;
      tray.dataset.row = String(row);
      tray.innerHTML = `<p class="sk-th"><span>${locked ? "Your forces" : "Tap a force, then tap where it points"}</span><span class="sk-n">${v.f.length} ${v.f.length === 1 ? "arrow" : "arrows"}</span></p>`
        + `<div class="fz-ti" role="group" aria-label="Forces">${FZ.map(chip).join("")}`
        + (ANG ? `<button type="button" class="fz-chip fz-chip-ang" data-force="angle" aria-pressed="${!!pick}"${locked ? " disabled" : ""}><span class="fz-angic" aria-hidden="true">∠</span><span class="fz-cs">${v.ang ? "Mark the angle again" : "Mark an angle"}</span></button>` : "")
        + `</div>`;
      if (row) keepInRow(sl);
      // the heads (44 px finger targets) and, while an angle is being marked, a button at each end of the guides
      pins.innerHTML = v.f.map((ar, i) => { const t = tip(ar);
        return `<button type="button" class="fz-pin" data-i="${i}" data-pick="${!!(pick && pick.first === "f" + i)}" style="left:${f1(t.x)}px;top:${f1(t.y)}px"${locked ? ' tabindex="-1"' : ""}`
          + ` aria-label="${esc(fzName(ar.l))}, ${fzWords(ar.a)}${locked ? "" : pick ? ". Choose it as a line of the angle" : ". Arrow keys turn it, Delete removes it"}"></button>`; }).join("")
        + (pick && !locked ? FZG.map(g => `<button type="button" class="fz-pin fz-gp" data-gp="${g[0]}" data-pick="${pick.first === g[0]}" style="left:${f1(G.cx + Math.cos(fzRad(g[2])) * (G.R + 14))}px;top:${f1(G.cy - Math.sin(fzRad(g[2])) * (G.R + 14))}px" aria-label="${esc(g[1])}"></button>`).join("") : "");
      hint.innerHTML = hintHtml(); hint.hidden = locked;
      out.innerHTML = resHtml();
      wire();
      if (focusSel) { const nd = root.querySelector(focusSel); if (nd && !nd.disabled) nd.focus({ preventScroll: true }); }
    }
    function keepInRow(sl) { const ti = tray.querySelector(".fz-ti"); if (!ti) return; ti.scrollLeft = sl;
      const edge = () => { ti.dataset.l = String(ti.scrollLeft > 2); ti.dataset.r = String(ti.scrollLeft + ti.clientWidth < ti.scrollWidth - 2); };
      ti.onscroll = edge;
      const c = ti.querySelector('[aria-pressed="true"]');
      if (c) { const l = c.offsetLeft, r = l + c.offsetWidth, m = 36; let to = ti.scrollLeft;
        if (l - m < to) to = Math.max(0, l - m); else if (r + m > to + ti.clientWidth) to = r + m - ti.clientWidth;
        if (Math.abs(to - ti.scrollLeft) > 1) ti.scrollTo({ left: to, behavior: o.reduced ? "auto" : "smooth" }); }
      edge(); }
    // remove arrow i: the angle loses a line on it, the lines after it shift down
    function drop(i) { const nm = fzName(v.f[i].l); v.f.splice(i, 1);
      if (v.ang) { const fix = r => r[0] !== "f" ? r : +r.slice(1) === i ? null : +r.slice(1) > i ? "f" + (+r.slice(1) - 1) : r, a = v.ang.map(fix); if (a[0] && a[1]) v.ang = a; else delete v.ang; }
      sel = -1; emit(); say(nm + " removed"); }
    function pickLine(ref) {
      if (!pick) return; if (!pick.first) { pick.first = ref; say(lineName(ref) + " chosen. Now the second line."); render(); return; }
      if (ref === pick.first) return;
      v.ang = [pick.first, ref]; pick = null; emit(); const A = angInfo();
      say("Angle marked between " + lineName(v.ang[0]) + " and " + lineName(v.ang[1]) + ": " + (A ? A.val : 0) + " degrees"); render(`[data-force="angle"]`);
    }
    // the line nearest a tap's direction (an arrow before a guide), within 25°
    const nearestLine = ta => { const c = v.f.map((ar, i) => ({ ref: "f" + i, a: ar.a, pri: 0 })).concat(FZG.map(g => ({ ref: g[0], a: g[2], pri: 1 })));
      c.sort((p, q) => (fzDif(p.a, ta) - fzDif(q.a, ta)) || (p.pri - q.pri)); return c[0] && fzDif(c[0].a, ta) <= 25 ? c[0].ref : null; };
    const at = e => { const r = svgEl.getBoundingClientRect(), s = (r.width || G.w) / G.w, x = (e.clientX - r.left) / s, y = (e.clientY - r.top) / s, dx = x - G.cx, dy = y - G.cy;
      return { a: fzSnap(fzAng(dx, dy)), d: Math.hypot(dx, dy) }; };
    const lenOf = d => Math.round(Math.max(46, Math.min(G.R, d)) / G.R * 100) / 100;
    function wire() {
      // (data-force, not data-l: the row's scroller carries data-l / data-r, its fades, and a click on a chip bubbled to it as a "false" force)
      tray.querySelectorAll("[data-force]").forEach(b => b.onclick = e => { if (locked) return; const id = b.dataset.force;
        if (id === "angle") { pick = pick ? null : { first: null }; act = ""; sel = -1; if (pick) say("Marking an angle: choose its first line."); render(`[data-force="angle"]`); return; }
        pick = null; sel = -1;
        if (e.detail === 0) {   // the keyboard (or a screen reader): drawn pointing right, its head takes the focus for the arrow keys
          v.f.push({ l: id, a: 0, r: 0.8 }); act = ""; sel = v.f.length - 1; emit(); say(fzName(id) + " drawn, pointing right. The arrow keys turn it.");
          render(`[data-i="${v.f.length - 1}"]`); return; }
        act = act === id ? "" : id; render(`[data-force="${id}"]`); });
      const on = (s, fn) => { const n = hint.querySelector(s); if (n) n.onclick = fn; };
      on("[data-rm]", () => { if (sel < 0) return; drop(sel); render(".fz-chip"); });
      on("[data-cancel]", () => { pick = null; render(`[data-force="angle"]`); });
      on("[data-noang]", () => { delete v.ang; emit(); say("Angle removed"); render(`[data-force="angle"]`); });
      pins.querySelectorAll("[data-gp]").forEach(b => { b.onclick = e => { e.stopPropagation(); pickLine(b.dataset.gp); }; });
      pins.querySelectorAll("[data-i]").forEach(p => {
        const i = +p.dataset.i;
        p.onpointerdown = e => { if (locked || pick) return; e.preventDefault(); e.stopPropagation(); p.setPointerCapture(e.pointerId); drag = { i: i, x: e.clientX, y: e.clientY, moved: false };
          document.documentElement.classList.add("bp-drag"); };
        p.onpointermove = e => { if (!drag || drag.i !== i) return; if (!drag.moved && Math.hypot(e.clientX - drag.x, e.clientY - drag.y) < 5) return; drag.moved = true;
          const c = at(e); if (c.d < 12) return; v.f[i].a = c.a; v.f[i].r = lenOf(c.d); sel = i; paint(); const t = tip(v.f[i]); p.style.left = t.x + "px"; p.style.top = t.y + "px"; };
        const end = () => { if (!drag || drag.i !== i) return; const moved = drag.moved; drag = null; pinUp = Date.now(); document.documentElement.classList.remove("bp-drag");
          if (moved) { emit(); say(fzName(v.f[i].l) + " turned, " + fzWords(v.f[i].a)); }
          act = ""; sel = moved ? i : (sel === i ? -1 : i); render(`[data-i="${i}"]`); };
        p.onpointerup = end; p.onpointercancel = end;
        p.onclick = e => { e.stopPropagation(); if (locked) return; if (pick) { pickLine("f" + i); return; } if (e.detail === 0) { sel = sel === i ? -1 : i; act = ""; render(`[data-i="${i}"]`); } };
        p.onkeydown = e => { if (locked || pick) return; const k = e.key, st = e.shiftKey ? 15 : 5;
          if (["ArrowUp", "ArrowLeft", "ArrowDown", "ArrowRight"].indexOf(k) !== -1) { e.preventDefault(); v.f[i].a = fzN(v.f[i].a + (k === "ArrowUp" || k === "ArrowLeft" ? st : -st)); sel = i;
            emit(); say(fzWords(v.f[i].a)); render(`[data-i="${i}"]`); }
          else if (k === "Delete" || k === "Backspace") { e.preventDefault(); drop(i); render(".fz-chip"); }
          else if (k === "Escape") { e.preventDefault(); sel = -1; render(`[data-i="${i}"]`); } };
      });
    }
    // a tap on the diagram: aims the chosen force (or re-aims the chosen arrow), or picks an angle's line; the diagram lets the page
    // scroll under a swipe (only the heads hold the finger)
    plot.addEventListener("click", e => {
      if (locked || drag || e.target.closest(".fz-pin") || Date.now() - pinUp < 400) return;
      const c = at(e);
      if (pick) { if (c.d < 14) return; const r = nearestLine(c.a); if (r) pickLine(r); return; }
      if (c.d < 16) { hint.textContent = "Tap away from the dot, in the direction the force points."; return; }
      if (act) { v.f.push({ l: act, a: c.a, r: lenOf(c.d) }); sel = v.f.length - 1; say(fzName(act) + " drawn, " + fzWords(c.a)); act = ""; emit(); render(null); return; }
      if (sel >= 0 && v.f[sel]) { v.f[sel].a = c.a; v.f[sel].r = lenOf(c.d); say(fzName(v.f[sel].l) + " turned, " + fzWords(c.a)); emit(); render(null); return; }
      hint.textContent = "Pick a force first.";
    });
    // a mouse sees where its click would put the arrow (a finger has no hover)
    plot.addEventListener("pointermove", e => { if (e.pointerType !== "mouse" || locked || drag || pick || !(act || sel >= 0) || e.target.closest(".fz-pin")) return;
      const c = at(e); if (c.d < 16) { paint(); return; } paint({ l: act || v.f[sel].l, a: c.a, r: lenOf(c.d) }); });
    plot.addEventListener("pointerleave", () => { if (!drag && G) paint(); });
    render(null);
    if (window.ResizeObserver) { ro = new ResizeObserver(() => { const w = Math.max(260, Math.min(760, Math.floor(host.getBoundingClientRect().width || 320))); if (Math.abs(w - W) >= 2 && !drag) render(); }); ro.observe(host); }
    return { sync(s) { const nv = normV(s.value), changed = JSON.stringify(nv) !== JSON.stringify(v);
        const its = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? s.items : null, was = locked + "|" + JSON.stringify(items);
        if (its && !items) { act = ""; sel = -1; pick = null; }   // just marked: the marks show on the arrows, none of them chosen
        v = nv; locked = !!s.locked; items = its;
        if (sel >= v.f.length) sel = -1;
        if (locked) { act = ""; sel = -1; pick = null; }
        if ((changed || was !== locked + "|" + JSON.stringify(items)) && !drag) render(); },
      destroy() { if (ro) ro.disconnect(); document.documentElement.classList.remove("bp-drag"); host.innerHTML = ""; } };
  }

  // each kind names its marker's items (the memo's own words); a paper may override them with cfg.labels. (No paper ever carried
  // labels: chipRow read undefined[key] and threw on every render after a Check, so the T C L S P chips never showed; 2026-10-06)
  const LABELS = { hist: { T: "Type", C: "Caption", L: "Axes labels", S: "Scale", P: "Plotting" } };
  function chipRow(items, labels) {
    labels = labels || {};
    return `<div class="bp-chips" role="status">${items.map(it => { const ok = it.awarded >= it.available;
      return `<span class="bp-chip" data-ok="${ok}">${ok ? "✓" : it.awarded > 0 ? "◐" : "✕"} ${esc(labels[it.key] || it.key)}${it.available > 1 ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
  }

  // (fit: the sketch's curve fit, for a self-test; SKETCH_V / LINE_V: markers a test reads to prove this file's sketch / line builders
  // are the ones loaded)
  window.BuildPlay = { SKETCH_V: "sketch-2", LINE_V: "line-1", fit: skFit, mount(host, o) { return ({ hist: hist, geno: geno, cross: cross, sketch: sketch, boxplot: boxplot, numline: numline, venn: venn, tree: tree, plot: plot, forces: forces }[o.kind] || stems)(host, o); }, VT_V: "vt-6", trVal: trVal,
    FORCE_V: "forces-1", FZ: FZ.map(l => l.id),   // (FORCE_V proves this file's force-diagram builder is the one loaded; FZ: its tray, the same for every question)
    PLOT_V: "plot-1", akima: akima };   // (akima: the plot builder's curve, for a self-test; PLOT_V proves this file's plot builder is the one loaded)
})();
