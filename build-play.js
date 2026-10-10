/* build-play.js: the paper's drawing questions as things to BUILD, auto-marked against the memo's own criteria (Murci approved the
   mockup 2026-10-03: "Yes please"). Four kinds:
   - "hist"  (3.1.3) a histogram, one examiner rule per step: Type (T), Caption (C), Axes labels (L), Scale (S), Plot (P, drag bars).
   - "stems" (3.6.4) three stems in the box: tap how each looks after the investigation (bends left / straight up / right / no growth).
   - "geno"  (LS P2 Nov 2025 2.3.3(b), 2.4.2) genotypes built from the paper's alleles: sockets filled from a tray, exact (DD is not dd).
   - "cross" (LS P2 Nov 2025 2.5.4) a monohybrid cross on a Punnett square, the memo's 8 points (ratio compulsory + any 5).
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

  window.BuildPlay = { mount(host, o) { return ({ hist: hist, geno: geno, cross: cross }[o.kind] || stems)(host, o); } };
})();
