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
  // (the axis-label choices are listed SORTED: the config keeps the right one first, which a learner could read as the answer)
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
      if (i === 2) return `<div class="bp-grp"><label class="bp-q" for="bp-x">The X-axis (along the bottom)</label><select id="bp-x" class="bp-in"><option value="">Choose…</option>${[...cfg.x].sort().map(t => `<option${v.xl === t ? " selected" : ""}>${esc(t)}</option>`).join("")}</select></div>`
        + `<div class="bp-grp"><label class="bp-q" for="bp-y">The Y-axis (up the side)</label><select id="bp-y" class="bp-in"><option value="">Choose…</option>${[...cfg.y].sort().map(t => `<option${v.yl === t ? " selected" : ""}>${esc(t)}</option>`).join("")}</select></div>`;
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
        chips = s.items && s.itemsFor === JSON.stringify(s.value || {}) ? chipRow(s.items, cfg.labels || LABELS.hist) : "";
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

  // each kind names its marker's items (the memo's own words); a paper may override them with cfg.labels. (No paper ever carried
  // labels: chipRow read undefined[key] and threw on every render after a Check, so the T C L S P chips never showed; 2026-10-06)
  const LABELS = { hist: { T: "Type", C: "Caption", L: "Axes labels", S: "Scale", P: "Plotting" } };
  function chipRow(items, labels) {
    labels = labels || {};
    return `<div class="bp-chips" role="status">${items.map(it => { const ok = it.awarded >= it.available;
      return `<span class="bp-chip" data-ok="${ok}">${ok ? "✓" : it.awarded > 0 ? "◐" : "✕"} ${esc(labels[it.key] || it.key)}${it.available > 1 ? " " + it.awarded + "/" + it.available : ""}</span>`; }).join("")}</div>`;
  }
  // drew it on paper: the memo's criteria to tick, shown and never banked (a self-ticked mark is not a mark)
  function selfCheck(criteria) {
    return `<div class="bp-self"><p class="bp-q">Drew it on paper? Tick what your drawing has.</p>${criteria.map((c, k) =>
      `<label class="bp-tick-row"><input type="checkbox"> ${esc(c[0])}</label>`).join("")}<p class="bp-hint">A self-check: it guides you, it is not marked.</p></div>`;
  }

  // (fit: the sketch's curve fit, for a self-test; SKETCH_V / LINE_V: markers a test reads to prove this file's sketch / line builders
  // are the ones loaded)
  window.BuildPlay = { SKETCH_V: "sketch-2", LINE_V: "line-1", fit: skFit, mount(host, o) { return ({ hist: hist, geno: geno, cross: cross, sketch: sketch, boxplot: boxplot, numline: numline }[o.kind] || stems)(host, o); } };
})();
