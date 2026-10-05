/* mcq-play: the MCQ experience as a component (glass cards, the break and the robot under it, the thought hint,
   the answer card), so the concept page and the Exam Missions prototype run the same code.

   McqPlay.mount(opts) -> { go(n, practice), destroy() }
   opts:
     paper       the paper data (sections -> missions -> items)          required
     order       the question numbers to play, in order ["1.1.1", ...]   required
     why         { n: { why, not } } explanations for the answer card   optional
     start       the first question (default order[0]); practice: true = no XP, no marks
     host        where the page part goes (default document.body); hud: false hides its top bar (the host has one)
     screen      true = the question scrolls in its own fixed screen under the host's header (topOffset() px; topEl: the header
                 element, watched so the screen follows it when it changes size)
     xpFor({ item, tries })       the host's XP for a right answer (default 100 / 60 / 20)
     onAttempt({ n, pick, correct, tries, practice, final })   every try
     onScore({ n, marks, tier, gone, tries })                  once per question, the first time it is finished
     onNext({ from, to, sameGroup })   the learner moves on (default: the next in order); onMap()  the Map button
     judge(item, pick, tryNo) -> { correct, xp, marks, clue, closed, answer, replay }   a host that marks (Exam Practice):
                 the component never holds the answer key; it learns the answer only once the host reveals it (closed)
     onMarksLanded(marks)   the earned marks reached the host's counter (update its number now)
     targets     { xpBox, marksBox } host elements the "+XP" / "+marks" fly to; back / retry: false to switch off
     glassRain   true = a wrong card's glass rains over the whole screen (about 30% of it aimed at the robot's head): the
                 robot does not run to the card, it is hit wherever it stands, plays its hit, then runs to the other half
                 of the screen, as if to get away (the learner-colours standalone; default off: the robot runs under the card)
     slideIn     true = moving on, the question slides out to the left and the next slides in from the right, against the
                 robot sweeping the glass off to the right (default: it rises and its cards are dealt from below)
     pointAtHint true = while it thinks a hint, the robot's raised hand points at the bubble: its standing pose raises the
                 hand on the screen's left, so with the bubble on its right it is mirrored (a quick turn), and back as it moves
     look        "panel" = the question on a panel (the boss's design, 2026-09-29): a chip with the number and topic, the marks
                 as a pill at its right, a "Question N" label, the question, cards with an icon (the radio is the look's to show or hide); no try dots
     leadFor(item) -> the group's lead-in line ("" = none) · iconFor(i, item) -> the card's icon (SVG markup), panel look only
     robotFixed  true = the robot keeps its corner (the boss's design): the glass rains and hits it where it stands, it never
                 runs to a card; on Next it steps down off its rock (.pal.floor), sweeps the glass as before, and steps back up · idleSay: its line at rest ("You got this!")
     fit         true = every option card fits the screen without scrolling: after each render and resize it steps the page to
                 fit-1 .. fit-5 while the last card ends below the visible area (the look's CSS defines the levels; each card is sized to its text)
     heroIn      "stage" = the answer card grows to fill the question's panel (the stage), not the middle of the screen
     celebrate   "corner" = the robot dances / claps / is defeated where it stands (its corner), not inside the answer card
     after       "panel" = once answered, Back and Next sit on the panel; a tap anywhere only closes the big card (it never
                 moves on), and every wrong card, the broken ones too, comes back to its place, dimmed (the glass stays down)
   Marks only for a first-try right answer; a practice run gives no XP and no marks. Built 2026-09-29 from the concept. */
(function () {
  const LAYERS_HTML = '<div class="backdrop" aria-hidden="true"></div>\n<div class="scrim" id="mq-scrim" aria-hidden="true"></div>\n<div class="hero-layer" id="mq-heroLayer"></div>\n<button class="next" id="mq-next"><span>Next question</span><span class="arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></button>\n<div class="pal" id="mq-pal" aria-hidden="true"><div class="pal-body" id="mq-palBody"></div><div class="pal-say" id="mq-clue"><i class="puff p1"></i><i class="puff p2"></i><span class="say-txt" id="mq-clueTxt"></span></div></div>\n<canvas id="mq-fx"></canvas>\n<div class="shards" id="mq-shards" aria-hidden="true"></div>\n\n<div class="dock"><div class="dock-in">\n  <div class="say" id="mq-say"></div>\n</div></div>\n<div class="toast" id="mq-toast" role="status"></div>\n<div class="mapsheet" id="mq-mapSheet" hidden><div class="ms-in" role="dialog" aria-modal="true" aria-labelledby="mq-msTitle">\n  <div class="ms-head"><span id="mq-msTitle">Map</span><button class="ms-x" id="mq-msX" aria-label="Close map">&times;</button></div><div id="mq-msList"></div></div></div>\n<p class="sr" id="mq-live" aria-live="polite"></p>';
  const PAGE_HTML = '<div class="top">\n  <button class="mapbtn" id="mq-mapBtn" aria-haspopup="dialog" aria-label="Map"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4 3 6.5v13.5l6-2.5 6 2.5 6-2.5V4l-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg><span class="lbl">Map</span></button>\n  <div class="streak" id="mq-streak"></div>\n  <button class="mute" id="mq-motion" hidden aria-pressed="false" aria-label="Tilt the glass with your phone" title="Tilt"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="3" width="8" height="18" rx="2" transform="rotate(-14 12 12)"/><path d="M3.5 9.5a9 9 0 0 0 0 5M20.5 9.5a9 9 0 0 1 0 5"/></svg></button>\n  <div class="xp marks" id="mq-marksBox" aria-label="Marks"><span><span id="mq-mk">0</span><span class="of">/<span id="mq-mkOf"></span></span></span><span class="lbl">marks</span></div>\n  <div class="xp" id="mq-xpBox"><span aria-hidden="true">⚡</span><span id="mq-xp">0</span><span style="color:var(--tint)">XP</span></div>\n</div>\n<main class="stage" id="mq-stage"></main>';
  const CSS_URL = (document.currentScript && document.currentScript.src || "").replace(/mcq-play\.js/, "mcq-play.css");   // keeps a ?v= query, so a versioned script loads its matching CSS
  let mounted = null;
  function mount(opts) {
    if (mounted) mounted.destroy();
    if (CSS_URL && !document.querySelector('link[data-mcqp]')) { const l = document.createElement("link"); l.rel = "stylesheet"; l.href = CSS_URL; l.dataset.mcqp = ""; document.head.appendChild(l); }
    const LAYERS = document.createElement("div"); LAYERS.className = "mcqp mcqp-layers"; LAYERS.innerHTML = LAYERS_HTML; document.body.appendChild(LAYERS);
    const PAGE = document.createElement("div"); PAGE.className = "mcqp mcqp-page" + (opts.screen ? " mcqp-screen" : ""); PAGE.innerHTML = PAGE_HTML;
    (opts.host || document.body).appendChild(PAGE);
    if (opts.screen && opts.topOffset) PAGE.style.top = opts.topOffset() + "px";
    if (opts.hud === false) PAGE.querySelector(".top").hidden = true;
    if (opts.screen) document.body.classList.add("mcqp-on");
    const SC = opts.screen ? PAGE : window;
    const RQ = sel => LAYERS.querySelector(sel) || PAGE.querySelector(sel);
    const RQA = sel => [...LAYERS.querySelectorAll(sel), ...PAGE.querySelectorAll(sel)];
    const OFF = []; const listen = (t, type, fn, o) => { t.addEventListener(type, fn, o); OFF.push(() => t.removeEventListener(type, fn, o)); };
    // Screen mode: the screen starts where the host's header ends, re-placed whenever that header changes size (topEl) or the
    // window does. Measured once at mount it went stale: the host header's SVGs were 300 x 150 until its stylesheet landed,
    // the header read 1402 px tall at mount, and the whole question sat below the page.
    const placeScreen = () => { if (opts.screen && opts.topOffset) PAGE.style.top = opts.topOffset() + "px"; if (opts.fit) fitCards(); };   // the screen's height changes with it
    // fit (opt-in): every option card on screen without scrolling. After each render and resize, if the last card ends below the
    // visible area, step the layout tighter (fit-1 .. fit-5 on the page; the look's CSS says what each level does) until it fits.
    // A question too long even at fit-5 scrolls, as before. Measured, not guessed: question lengths differ.
    const FIT_MAX = 5;
    // one card sized to its own text: its back when it is flipped (the side that shows). fitCards runs it on every card; dismiss
    // runs it on the closing card BEFORE it glides home, so it lands at its real height (measured: it glided to its face's
    // 48 px while its back needed 56, spilled for ~170 ms, then the refit after the glide grew it: "overflows, then settles").
    function fitTile(x) { const f = x.querySelector(x.classList.contains("flipped") ? ".back" : ".face"); if (!f) return;
      const cs = getComputedStyle(f), kids = [...f.children].filter(c => getComputedStyle(c).display !== "none" && getComputedStyle(c).position !== "absolute");
      const need = Math.ceil(Math.max(0, ...kids.map(c => c.scrollHeight)) + parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom));
      if (need > x.offsetHeight) x.style.minHeight = need + "px"; }
    function fitCards() { const tiles = [...PAGE.querySelectorAll("#mq-tiles .tile")]; if (!tiles.length) return;
      // the level goes on the page AND the layers: the last one also makes the robot smaller (on the same rock), lowering the floor
      const set = k => { for (let j = 1; j <= FIT_MAX; j++) { PAGE.classList.toggle("fit-" + j, j === k); LAYERS.classList.toggle("fit-" + j, j === k); } };
      // a card's face is absolute (it flips), so the card does not grow with its text: size each card to its own text, per level.
      // The text block's height, not the face's scrollHeight: the face centres its content, so it overflows at both ends and
      // scrollHeight counts only the bottom half (measured: 1.1.9's cards stayed clipped with it).
      const size = () => { tiles.forEach(x => x.style.removeProperty("min-height")); tiles.forEach(fitTile); };
      // layout position, not getBoundingClientRect: the cards deal in with a transform, which a mid-animation measure would count
      const top = el => { let y = 0; for (let e = el; e && e !== PAGE && e !== document.body; e = e.offsetParent) y += e.offsetTop; return y; };
      // the whole panel, not just the cards: its padding and the Back / Next row must be on screen too (measured: the cards fitted and
      // the screen still scrolled 4 px); clear of the bottom fade (22 px in nx-play)
      // the panel's CONTENT bottom (its last row + its bottom padding), in layout terms: the host may cap the panel's height (it then
      // scrolls inside), and the capped box hid its own overflow (measured: fit-0 "fitted" at 412x915 while the panel ran 6 px
      // over). Not scrollHeight: it counts the cards' deal-in transforms.
      const stage = $("stage"), padB = () => parseFloat(getComputedStyle(stage).paddingBottom) || 0,
        // the last row IN the panel: a row the host lifts out of it (position absolute / fixed, e.g. a phone's Next row under the
        // panel) is not the panel's content
        contentBottom = () => { const rows = [...stage.children].filter(c => !/^(absolute|fixed)$/.test(getComputedStyle(c).position)), last = rows[rows.length - 1];
          return last ? top(last) + last.offsetHeight + padB() : top(stage) + stage.offsetHeight; },
        bottomOf = () => Math.max(tiles.reduce((m, x) => Math.max(m, top(x) + x.offsetHeight), 0), stage ? Math.max(top(stage) + stage.offsetHeight, contentBottom()) : 0);
      // the room: the screen less the fade, or the panel's own height cap when the host sets one (it may keep room under the
      // panel, e.g. for a phone's Next row), whichever is lower
      // The cap is read from the host's --cap-off (the space it keeps off the panel's height: its max-height is 100% - --cap-off),
      // not from max-height itself: a computed max-height comes back as the calc() text (NaN), and the cap was silently ignored.
      const H = () => (opts.screen ? PAGE.clientHeight : innerHeight);
      const capB = () => { const off = stage ? parseFloat(getComputedStyle(stage).getPropertyValue("--cap-off")) : NaN; return isFinite(off) ? top(stage) + H() - off : Infinity; };
      const overBy = () => bottomOf() - Math.min(H() - 24, capB());
      // the least level that fits; if none does, the one that comes closest (the rest scrolls). opts.fitMax() caps the level
      // (Exam Practice: a phone stops at fit-3, one readable column, and a longer question scrolls INSIDE its panel)
      const top_ = Math.min(FIT_MAX, opts.fitMax ? opts.fitMax() : FIT_MAX);
      let best = -1, bestBy = Infinity; for (let k = 0; k <= top_; k++) { set(k); size(); const by = overBy(); if (by <= 0) { best = k; break; } if (by < bestBy) { bestBy = by; best = k; } }
      set(best); size(); growTiles(); alignHead(); centreStage(); panelScroll(); }
    // a table's column heads sit over the cards' cells: measured off the first card (its letter and padding change with the fit
    // level and the screen), in layout terms (offsets, not client rects: the cards deal in and lift with transforms)
    function alignHead() { const hd = PAGE.querySelector("#mq-tblhead"), c = PAGE.querySelector("#mq-tiles .tile .cells"), g = PAGE.querySelector("#mq-tiles"); if (!hd || !c || !g) return;
      const left = el => { let x = 0; for (let e = el; e && e !== PAGE && e !== document.body; e = e.offsetParent) x += e.offsetLeft; return x; };
      const l = left(c) - left(g); hd.style.marginLeft = l + "px"; hd.style.width = c.offsetWidth + "px"; }
    // A card's faces are absolute (the flip), so its height is only its min-height: a 3-line option spilled 3 px over both edges
    // (1.1.9 at 360 px, fit-4: text 51 px in a 46 px card; found 2026-10-03). A card whose text needs more grows to fit it.
    function growTiles() { RQA(".tile").forEach(t => { t.style.removeProperty("min-height"); const f = t.querySelector(".face"), x = t.querySelector(".txt"); if (!f || !x) return;
      const cs = getComputedStyle(f), need = Math.ceil(x.scrollHeight + parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom));
      if (need > t.offsetHeight + 1) t.style.setProperty("min-height", need + "px", "important"); }); }   // (important: a phone rule pins min-height:46px !important)
    // opts.centreY (0-1): where the panel and its Back / Next row sit in the room left under them (Exam Practice: 0.4, the optical
    // centre; Murci, 2026-09-30: "it looks a bit up and too close to the navbar"). Wider than a phone only (a phone's robot has the
    // lower half). The room is the fit's own: the screen less the row's room (--cap-off) and the 24 px floor gap.
    function centreStage() { const st = $("stage"); if (!st || opts.centreY == null) return; st.style.removeProperty("margin-top"); if (innerWidth <= 600) return;
      const top = el => { let y = 0; for (let e = el; e && e !== PAGE && e !== document.body; e = e.offsetParent) y += e.offsetTop; return y; };
      const H = opts.screen ? PAGE.clientHeight : innerHeight, off = parseFloat(getComputedStyle(st).getPropertyValue("--cap-off")) || 0, base = parseFloat(getComputedStyle(st).marginTop) || 0;
      const spare = H - (off - base) - (top(st) + st.offsetHeight), extra = Math.max(0, Math.min(160, Math.round(spare * opts.centreY)));
      if (extra) st.style.marginTop = (base + extra) + "px"; }
    // The panel (the host caps its height) scrolls inside when its question is longer than the room: "scrolls" shows the fade
    // at its bottom edge, "atend" drops it once the end is in view (so the fade never covers the last card).
    function panelScroll() { const st = $("stage"); if (!st) return; st.scrollTop = 0;
      const more = st.scrollHeight > st.clientHeight + 1; st.classList.toggle("scrolls", more); st.classList.remove("atend");
      // a Back / Next row the host lifts out of the panel (position absolute: a phone) follows the panel's real bottom edge, --after-gap
      // under it (measured: pinned to the area's bottom, it sat 136 px under a short question's panel at 412x915)
      // (a FIXED row stays where the host puts it: a phone's Next at the screen's bottom-right)
      const af = $("after"); if (af) { if (getComputedStyle(af).position === "absolute") {
        const gap = parseFloat(getComputedStyle(af).getPropertyValue("--after-gap")) || 12; af.style.top = (st.offsetTop + st.offsetHeight + gap) + "px"; af.style.bottom = "auto"; }
        else { af.style.removeProperty("top"); af.style.removeProperty("bottom"); } }
      dockAfter();
      if (!st._scrollHooked) { st._scrollHooked = true;
        listen(st, "scroll", () => st.classList.toggle("atend", st.scrollTop + st.clientHeight >= st.scrollHeight - 2), { passive: true }); } }
    // A host may DOCK the Back / Next row under the panel (nx-play wider than a phone sets --after-dock:1 on the row): still fixed, so it
    // never scrolls with the panel, placed 12 px under the panel's real bottom edge and flush with its right edge (Murci, 2026-09-30: at
    // the screen's corner it was ~700 px from the answer on a desktop). The place goes in custom properties the host's CSS reads.
    function dockAfter() { const af = $("after"), st = $("stage"); if (!af || !st) return; const cs = getComputedStyle(af);
      const on = cs.getPropertyValue("--after-dock").trim() === "1" && cs.position === "fixed"; af.classList.toggle("docked", on); if (!on) return;
      // --after-inset (the host's, optional): how far in from the panel's box the row lines up (a phone with no panel card: the text's edge)
      const r = st.getBoundingClientRect(), inset = parseFloat(cs.getPropertyValue("--after-inset")) || 0;
      af.style.setProperty("--dock-top", Math.round(r.bottom + 12) + "px"); af.style.setProperty("--dock-right", Math.max(12, Math.round(innerWidth - r.right + inset)) + "px"); af.style.setProperty("--dock-left", Math.round(r.left + inset) + "px"); }
    // measured 2026-09-30: docked while the page still rose in (its animation moved the panel), Skip landed at y 2973, off screen, and
    // nothing measured again. So it docks again whenever an animation or transition in the page ends (one pass per frame).
    let dockRaf = 0; const dockSoon = () => { if (!dockRaf) dockRaf = requestAnimationFrame(() => { dockRaf = 0; dockAfter(); }); };
    listen(PAGE, "animationend", dockSoon); listen(PAGE, "transitionend", dockSoon); listen(window, "resize", dockSoon);
    if (opts.fit) listen(window, "resize", () => fitCards());
    if (opts.fit && document.fonts) document.fonts.ready.then(() => fitCards());   // the web font changes the text's height
    if (opts.screen && opts.topOffset) { listen(window, "resize", placeScreen);
      if (opts.topEl && window.ResizeObserver) { const ro = new ResizeObserver(placeScreen); ro.observe(opts.topEl); OFF.push(() => ro.disconnect()); } }
    // ---- the engine (from the concept page) ----
    const P = opts.paper, ITEMS = {};
    const GROUP = {};                                                   // each question's group on the paper ("Question 1.1", its extract)
    P.sections.forEach(s => s.missions.forEach(m => m.items.forEach(it => { ITEMS[it.n] = it; GROUP[it.n] = m; })));
    const XP_BY_TRY = [100, 60, 20, 0], L = "ABCDEFGH";
    let S = null, xp = 0, streak = 0;
    // CONCEPT-ONLY explanations: the paper's memo for an MCQ is just the letter, so these are written here from CAPS Gr 12
    // Life Sciences content, NOT added to the paper file ("nothing invented"). A Life Sciences teacher must check them before use.
    const WHY = opts.why || {};                                          // the host's explanations (per question number)
    const ORDER = opts.order.slice();                                  // the questions, in paper order
    const TIER_BY_TRY = ["gold", "silver", "bronze"];                          // the XP tiers: 100 / 60 / 20
    const book = Object.assign({}, opts.seed || {});                           // marks per question, first sitting only (opts.seed: the host's record of questions finished under an earlier mount, so a revisit shows its end state)
    Object.keys(book).forEach(n => { if (ITEMS[n] && book[n].a != null) ITEMS[n].a = book[n].a; });   // a seeded question knows its answer (the host marks: it is known only once found)
    const NEXT = document.getElementById("mq-next");                      // one Next button, moved to wherever the cards are
    const $ = id => document.getElementById("mq-" + id), live = t => { $("live").textContent = t; };
    const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
    $("mkOf").textContent = P.total; $("marksBox").setAttribute("aria-label", `0 of ${P.total} marks`);
    const rnd = (a, b) => a + Math.random() * (b - a);

    const buzz = ms => { if (navigator.vibrate) navigator.vibrate(ms); };   // Android only: iOS ignores vibrate from the web
    // One vibration pattern per moment (ms on/off): a tick for a pick, a burst for a shatter, rising for gold, heavy for defeat.
    const HAPTIC = { pick: 6, lock: 14, crack: 10, shatter: [14, 24, 40], shine: 8, gold: [20, 50, 30, 50, 70], silver: [20, 60, 35], bronze: 30, defeat: [70, 90, 140] };

    // Tilt (phones): the glass tilts with the phone and its glint follows the light, like the mouse tilt on desktop.
    // Android: on by default (no permission needed). iOS: needs a tap to allow motion (DeviceOrientationEvent.requestPermission).
    // The neutral angle follows how the phone is held (a slow re-centre), so the glass doesn't stay tipped when you lean back.
    const TILT = { on: false, base: null, x: 0, y: 0, tx: 0, ty: 0, raf: 0 };
    const TILT_OK = !reduced && matchMedia("(pointer: coarse)").matches && "DeviceOrientationEvent" in window;
    const TILT_ASK = TILT_OK && typeof DeviceOrientationEvent.requestPermission === "function";      // iOS
    function onOrient(e) { if (e.beta == null || e.gamma == null) return;
      if (!TILT.base) TILT.base = { b: e.beta, g: e.gamma };
      TILT.base.b += (e.beta - TILT.base.b) * 0.01; TILT.base.g += (e.gamma - TILT.base.g) * 0.01;   // re-centre slowly
      TILT.tx = Math.max(-1, Math.min(1, (e.gamma - TILT.base.g) / 18)); TILT.ty = Math.max(-1, Math.min(1, (e.beta - TILT.base.b) / 18));
      if (!TILT.raf) TILT.raf = requestAnimationFrame(tiltFrame); }
    function tiltFrame() { TILT.raf = 0; TILT.x += (TILT.tx - TILT.x) * 0.18; TILT.y += (TILT.ty - TILT.y) * 0.18;
      RQA("#mq-tiles .tile:not(.dead):not(.sel):not(.flipped) .face").forEach(f => {
        f.style.setProperty("--ty", (TILT.x * 5).toFixed(2) + "deg"); f.style.setProperty("--tx", (-TILT.y * 4).toFixed(2) + "deg");
        f.style.setProperty("--mx", (50 + TILT.x * 40).toFixed(1) + "%"); f.style.setProperty("--my", (-10 + TILT.y * 30).toFixed(1) + "%"); });
      if (Math.abs(TILT.tx - TILT.x) + Math.abs(TILT.ty - TILT.y) > 0.002) TILT.raf = requestAnimationFrame(tiltFrame); }
    function setTilt(on) { TILT.on = on; TILT.base = null; $("motion").setAttribute("aria-pressed", String(on));
      if (on) listen(window, "deviceorientation", onOrient); else { window.removeEventListener("deviceorientation", onOrient); TILT.tx = TILT.ty = 0; tiltFrame(); }
      try { localStorage.setItem("mcq.tilt", on ? "1" : "0"); } catch (e) {} }
    if (TILT_OK) { $("motion").hidden = false; let saved = null; try { saved = localStorage.getItem("mcq.tilt"); } catch (e) {}
      if (saved !== "0" && !TILT_ASK) setTilt(true);                                                 // Android: on unless switched off
      $("motion").onclick = () => { if (TILT.on) return setTilt(false);
        if (!TILT_ASK) return setTilt(true);
        DeviceOrientationEvent.requestPermission().then(r => { if (r === "granted") setTilt(true); }).catch(() => {}); }; }


    function load(n, practice = false) {
      const it = ITEMS[n];
      S = { it, sel: null, gone: new Set(), tries: 0, done: false, hit: {}, practice: practice && !!book[n] };   // practice: a retry of a finished question
      setHint(null); NEXT.classList.remove("show"); palHome(null); $("heroLayer").innerHTML = ""; heroBox(); $("scrim").classList.remove("on");   // the robot comes home before the card is cleared
      render(!book[n] || S.practice);                                     // a finished question comes back as it ended; a retry deals fresh
    }

    function render(deal) {
      const { it } = S, st = $("stage"), grp = GROUP[it.n] || {}, desc = grp.extract || it.note || "";
      // An "A: … · B: …" pair (Column II on the paper) sits under the stem as its two lines; the stem is otherwise as printed.
      const ab = it.q.match(/^(.*?)\s*A:\s*(.+?)\s*·\s*B:\s*(.+)$/), stem = ab ? ab[1] : it.q;
      const k = ORDER.indexOf(it.n);
      // panel look (Murci, 2026-09-30: "as in the original question papers"): the paper's order, "Question 1" and the marks as plain
      // text, then the group's own lead-in line (opts.leadFor, "1.2 Give the correct ..."), then the sub-question with its number
      const panel = opts.look === "panel", lead = panel && opts.leadFor ? String(opts.leadFor(it) || "") : "";
      const esc = t => t.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
      st.innerHTML = (panel
        // one line (Murci, 2026-09-30): the paper's question ("Question 1") beside its part's chip (1.1.1), the marks on the right
        ? `<div class="qhead"><span class="qid"><span class="qlabel">Question ${String(it.n).split(".")[0]}</span>${S.practice ? `<span class="qpractice">Practice round · no marks or XP</span>` : ""}</span><span class="tries" role="img"></span><span class="qmarks" aria-label="${it.marks} marks">${it.marks}<span class="mw"> ${it.marks === 1 ? "mark" : "marks"}</span></span></div>` + (lead ? `<p class="qlead"><b>${esc(String(grp.id || ""))}</b> ${esc(lead)}</p>` : "")
        : `<div class="qhead">${k > 0 ? `<button class="qback" id="mq-qback" aria-label="Previous question: ${ORDER[k - 1]}">‹</button>` : ""}<span class="qtitle">${grp.title || ""}</span><span class="tries"></span></div>`) +
        (desc ? `<p class="qdesc">${desc}</p>` : "") +
        `<h1><span class="num">${it.n}</span><span>${stem}</span></h1>` +
        (ab ? `<div class="ab"><div><b>A</b>${ab[2]}</div><div><b>B</b>${ab[3]}</div></div>` : "") +
      // the paper's own figure (opts gives it as it.img {src, w, h, alt}): under the stem, as printed; a tap enlarges it (2026-10-03, Murci:
      // "the real paper had images on MCQ but our MCQs dont have any of those images")
      (it.img ? `<figure class="qimg" role="button" tabindex="0" aria-label="Figure for ${it.n}. Tap to enlarge"><img src="${it.img.src}" width="${it.img.w}" height="${it.img.h}" alt="${esc(it.img.alt || "")}"></figure>` :
      it.fig ? `<div class="qfig"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="m3 16 5-5 4 4 3-3 6 6"/></svg><span>The diagram is on ${it.fig} of the paper</span></div>` : "");   // a question never loses its figure (the paper images are not in yet)
      const qim = st.querySelector(".qimg");
      if (qim) { const im = qim.querySelector("img"); if (opts.fit) im.addEventListener("load", () => fitCards(), { once: true });
        const zoom = () => { qim.classList.toggle("big"); qim.setAttribute("aria-label", "Figure for " + it.n + (qim.classList.contains("big") ? ". Tap to make smaller" : ". Tap to enlarge")); };
        qim.onclick = zoom; qim.onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); zoom(); } }; }
      const g = document.createElement("div"); g.className = "tiles"; g.id = "mq-tiles"; g.setAttribute("role", "radiogroup"); g.setAttribute("aria-label", "Options");
      // options printed as a TABLE (it.table {head, rows}; LS P1 Nov 2024 1.1.6, Murci 2026-10-05: "as printed"): one card per row, a
      // cell per column, the column heads above the cards; a screen reader hears each card as "C: muscle in X relaxed, ...". The
      // flattened option text (it.opts) stays the answer's words everywhere else (the medal card, the memo).
      const tbl = it.table && it.table.rows && it.table.rows.length === it.opts.length ? it.table : null;
      if (tbl) { g.classList.add("tbl"); g.style.setProperty("--cols", tbl.head.length);
        st.insertAdjacentHTML("beforeend", `<div class="tblhead" id="mq-tblhead" aria-hidden="true" style="--cols:${tbl.head.length}">${tbl.head.map(h => `<span>${esc(h)}</span>`).join("")}</div>`); }
      it.opts.forEach((o, i) => {
        const t = document.createElement("div"); t.className = "tile" + (deal && !reduced ? " dealt" : ""); t.dataset.i = i;
        t.style.setProperty("--d", (i * 90) + "ms"); t.style.setProperty("--gd", (1.2 + i * 0.85).toFixed(2) + "s"); t.style.setProperty("--rz", ((i % 2 ? 1 : -1) * (4 + i)) + "deg");
        t.innerHTML = `<button class="side face" role="radio" aria-checked="false"><span class="gleam" aria-hidden="true"></span><span class="letter">${L[i]}</span><span class="txt">${tbl ? `<span class="cells">${tbl.rows[i].map(c => `<span>${esc(c)}</span>`).join("")}</span>` : o}</span>${panel ? `<span class="ico" aria-hidden="true">${opts.iconFor ? opts.iconFor(i, it) || "" : ""}</span><span class="radio" aria-hidden="true"></span>` : ""}</button>
          <div class="side back" aria-hidden="true"><span class="gleam" aria-hidden="true"></span><div class="buddy" aria-hidden="true"></div><div class="copy"><div class="ok"></div><div class="ans"></div><div class="why"></div><div class="not"></div><div class="more">Tap to see why</div></div></div>`;
        const face = t.querySelector(".face");
        // (a head's single letters are the figure's labels and stay capitals: "muscle in X", not "muscle in x")
        if (tbl) face.setAttribute("aria-label", L[i] + ": " + tbl.head.map((h, j) => h.toLowerCase().replace(/\b[a-z]\b/g, c => c.toUpperCase()) + " " + String(tbl.rows[i][j]).toLowerCase()).join(", "));
        face.addEventListener("pointermove", e => { const r = face.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
          face.style.setProperty("--mx", x + "px"); face.style.setProperty("--my", y + "px");
          if (e.pointerType === "touch" || reduced || S.done || t.classList.contains("sel")) return;
          const u = x / r.width - 0.5, v = y / r.height - 0.5;
          face.style.setProperty("--ty", (u * 10).toFixed(2) + "deg"); face.style.setProperty("--tx", (-v * 8).toFixed(2) + "deg"); });
        face.addEventListener("pointerleave", () => ["--mx", "--my", "--tx", "--ty"].forEach(k => face.style.removeProperty(k)));
        face.addEventListener("pointerenter", () => { if (!S.done) palLook(t); }); face.addEventListener("focus", () => { if (!S.done) palLook(t); });
        face.addEventListener("pointerleave", () => { if (!S.done) palLook(null); });
        face.addEventListener("pointerdown", () => ["--tx", "--ty"].forEach(k => face.style.removeProperty(k)));   // flat before it answers
        face.addEventListener("pointerdown", e => { S.hit[i] = { cx: e.clientX, cy: e.clientY }; });   // screen coordinates: the pane grows under the finger
        face.onclick = () => press(i);
        t.addEventListener("animationend", ev => { if (ev.animationName === "mq-deal") t.classList.remove("dealt"); });
        t.addEventListener("click", () => { if (!S.done || S.busy) return; if (t.classList.contains("hero")) tapOut(); else if (t.classList.contains("flipped")) lift(t); });
        g.appendChild(t);
      });
      st.appendChild(g); st.insertAdjacentHTML("beforeend", `${panel ? "" : `<div class="qmarks">${it.marks} marks</div>`}<div class="again"><button class="retry nxb nxb-sec nxb-sm" id="mq-retry" hidden aria-label="Practise this question again: no marks or XP">Practise again</button></div><div class="after" id="mq-after"></div>`);   // the marks under the last card; Practise again under the cards (off the bar, 2026-10-03); the bar holds Back and Next
      // opts.onBack / opts.canBack: the host owns the order (it mounts one mission's MCQs, but a Back can lead to a part of another
      // type): the host says whether there is a way back and takes it (measured 2026-09-30: back:false left no Back at all)
      const hostBack = typeof opts.onBack === "function", canBack = hostBack ? !!(opts.canBack ? opts.canBack() : true) : k > 0 && opts.back !== false;
      if (opts.after === "panel" && canBack) { $("after").insertAdjacentHTML("afterbegin", `<button class="prevq" id="mq-prevq" aria-label="${hostBack ? "Previous question" : "Previous question: " + ORDER[k - 1]}"><span aria-hidden="true">‹</span>&nbsp;Back</button>`); $("prevq").onclick = () => { if (!S.busy) hostBack ? opts.onBack() : go(ORDER[k - 1]); }; }
      if ($("qback") && opts.back === false) $("qback").remove();
      if ($("qback")) $("qback").onclick = () => { if (!S.busy) go(ORDER[k - 1]); };
      // opts.onRetry(n): the host reopens the question as practice (its own record: no marks or XP) before the fresh deal
      $("retry").onclick = () => { if (S.busy) return; if (opts.onRetry) opts.onRetry(it.n); go(it.n, true); };
      $("after").appendChild(NEXT); paintTiles(); paintTop(); say();   // Next lives just under the cards
      // opts.skip (Murci, 2026-09-30: "showing Next before the learner answers, so they can skip"): the button is there from the start
      // as "Skip"; an answer turns it into "Next" (placeNext). The host decides what a skip does (Exam Practice: it comes back round).
      if (opts.skip && (typeof opts.skip !== "function" || opts.skip())) { NEXT.querySelector("span").textContent = "Skip"; NEXT.classList.add("show", "skip"); NEXT.setAttribute("aria-label", "Skip this question for now"); }
      if (book[it.n] && book[it.n].gone && !S.practice) restore(book[it.n]);
      palSize(); if (opts.idleSay && !S.done && !book[it.n]) sayIdle(opts.idleSay);   // at rest it encourages; a hint replaces it after a miss
      if (opts.fit) fitCards();
    }

    function press(i) {
      if (S.done || S.busy || S.gone.has(i)) return;                   // busy: one answer's consequence plays out before the next is taken
      if (PAL.cleaning) { S.sel = i; paintTiles(); PAL.queued = i; return; }   // the robot is still sweeping the last glass: the card shows picked, and is answered when it is back on its rock
      S.sel = i; palLook(RQ(`.tile[data-i="${i}"]`));                                                  // one tap answers (Murci): no second tap, no Lock in
      paintTiles();                                               // the card takes the picked colour, then answers
      submit();
    }
    function paintTiles() { RQA(".tile").forEach(t => { const i = +t.dataset.i, on = S.sel === i && !S.done;
      t.classList.toggle("sel", on); t.querySelector(".face").setAttribute("aria-checked", String(S.sel === i)); }); }
    function say() { $("say").textContent = S.done ? "" : S.sel == null ? "" : `Tap ${L[S.sel]} to answer`; }
    function paintTop() { $("xp").textContent = xp;
      $("streak").textContent = streak >= 2 ? `${streak} in a row` : ""; $("streak").dataset.n = streak;
      const tr = RQ(".tries");
      // a dot per try: red for each wrong one, green for the right one, the tries still to come in the tint; each also carries the
      // medal it plays for (gold, silver, bronze) and "now" on the one this try is for, so a skin can draw them as medals
      const wrong = S.gone.size, right = S.done && S.tries > wrong, TIER = ["gold", "silver", "bronze"];
      if (tr) { tr.innerHTML = [0, 1, 2].map(i => `<i class="${TIER[i]} ${i < wrong ? "no" : right && i === wrong ? "yes" : i >= S.tries ? "live" : ""}${!S.done && i === wrong ? " now" : ""}"></i>`).join("");
        tr.setAttribute("aria-label", right ? `${TIER[wrong][0].toUpperCase() + TIER[wrong].slice(1)}, on try ${wrong + 1} of 3` : S.done ? "No tries left" : `Try ${wrong + 1} of 3: ${TIER[Math.min(wrong, 2)]} if right`); } }
    listen(document, "keydown", e => { if (!S) return; if (S.done) { if (e.key === "Escape") dismiss(); else if (e.key === "Enter" && document.activeElement !== $("retry")) next(); return; }
      const i = "abcd".indexOf(e.key.toLowerCase()); if (i >= 0 && i < S.it.opts.length && !e.metaKey && !e.ctrlKey) { press(i); return; }
      const a = document.activeElement;
      if (e.key === "Enter" && S.sel != null && a === document.body) { e.preventDefault(); submit(); } });

    function submit() {
      const i = S.sel; if (i == null || S.done) return;
      const it = S.it, t = RQ(`.tile[data-i="${i}"]`), J = opts.judge ? opts.judge(it, i, S.tries + 1) : null, ok = J ? !!J.correct : i === S.it.a; S.tries++; buzz(HAPTIC.lock);
      if (J) { if (ok) it.a = i; else if (J.closed && J.answer != null) it.a = J.answer; }   // the host marks: the answer is known only once it is revealed
      if (opts.onAttempt) opts.onAttempt({ n: it.n, item: it, pick: i, correct: ok, tries: S.tries, practice: !!S.practice, final: J ? !!(ok || J.closed) : ok || S.tries >= 3 || S.gone.size + 1 >= it.opts.length - 1 });
      const SQ = S, up = raise(t); setHint(null); $("pal").classList.remove("small");   // it grows back to act                                      // it rises over the others first, then the verdict
      setTimeout(() => { if (S !== SQ) return; if (ok) t.dataset.tier = TIER_BY_TRY[S.tries - 1]; t.classList.add(ok ? "yes" : "no"); verdictLight(t, S.hit[i], ok); }, up);   // the verdict: green light, or red in the cracks (data-tier: the medal this try earns, so a skin can light it in that colour)
      if (ok) {
        S.done = true; const pr = S.practice || !!(J && J.replay), gain = pr ? 0 : J ? (J.xp || 0) : opts.xpFor ? opts.xpFor({ item: S.it, tries: S.tries }) : XP_BY_TRY[S.tries - 1], tier = TIER_BY_TRY[S.tries - 1], mk = pr ? 0 : J ? (J.marks || 0) : S.tries === 1 ? S.it.marks : 0;
        if (!pr) streak = S.tries === 1 ? streak + 1 : 0; setHint(null);   // practice: the medal shows how it went, nothing is added
        const name = tier[0].toUpperCase() + tier.slice(1), mkText = mk ? "+" + mk + (mk === 1 ? " mark" : " marks") : "0 marks";
        // the host's streak multiplier as its own chip ("x3 streak"): "+300 XP" alone never said why (measured 2026-09-30)
        t.querySelector(".ok").innerHTML = okHTML(name, pr ? ["Practice · no marks or XP"] : ["+" + gain + " XP"].concat(J && J.mult > 1 ? ["×" + J.mult + " streak"] : [], [mkText]), true, ["First try", "Second try", "Third try"][S.tries - 1]);
        fillBack(t, it); const rec = { gone: [...S.gone], tries: S.tries, ok: t.querySelector(".ok").innerHTML };
        live(pr ? `Correct, ${L[i]}. ${name}, practice: no XP or marks. ${whyOf(it)}` : `Correct, ${L[i]}. ${name}: plus ${gain} XP, ${mk ? "plus " + mk + " marks" : "no marks, marks are for a first try"}. ${whyOf(it)}`);
        const S0 = S; S.busy = true;                                   // S0: a question switched during the green light must not get this card
        if (mk) { if (!reduced) setTimeout(() => { if (S === S0) flyMarks(mk); }, up); else if (opts.onMarksLanded) opts.onMarksLanded(mk); }   // the marks go to the counter as the card turns green
        wait(up + (reduced ? 0 : VERDICT_MS)).then(() => { if (S !== S0) throw 0; return present(t, tier); }).then(() => {
          buzz(HAPTIC[tier]); burst(t, tier); if (!pr) { fly(t, "+" + gain, "xpBox");
          setTimeout(() => { xp += gain; $("xp").textContent = xp; bump("xpBox"); }, reduced ? 0 : 700); }   // counts up as the +XP lands
          setTimeout(() => score(it, mk, tier, rec), mk && !reduced ? 860 : 0); toast(pr ? name + " · practice" : name + " · +" + gain + " XP" + (mk ? " · +" + mk + " marks" : ""), "ok"); showNext(); }).catch(e => { if (e !== 0) console.error(e); });   // a stale card (question switched, thrown as 0) just stops; anything else is a real error and is reported
      } else {
        if (!S.practice) streak = 0; S.sel = null; S.gone.add(i); const rec = { gone: [...S.gone], tries: S.tries, ok: okHTML("The answer", ["0 XP", "0 marks"], false, "") };
        const clues = S.it.clues || [], clue = J ? (J.clue || "") : clues[Math.min(S.tries - 1, clues.length - 1)] || "", last = J ? !!J.closed : S.tries >= 3 || S.gone.size >= S.it.opts.length - 1;
        let rb = null;
        if (PAL.el && !PAL.sweeping && !reduced) { const rain = !!opts.glassRain || !!opts.robotFixed; if (rain) palStop(); const tx = rain ? PAL.x : palUnder(t), n = S.tries; rb = { ...palHead(tx), rain, minHold: rain ? 0 : Math.max(0, palRunMs(tx) + 140 - up), onHit: () => { const back = palHit(n, last, opts.robotFixed ? PAL.x : rain ? palAway() : 0);   /* robotFixed: back to where it stands, i.e. it stays */
          // robotFixed: it does not run anywhere, so it thinks the clue as it flinches (measured: 2.8 s from the tap, 0.76 s of it
          // waiting for a recovery that goes nowhere); a robot that runs off says it once it is back on its feet
          const say = () => { if (S === SQ && !S.done && S.tries === n) sayHint(clue); };
          if (back) { if (opts.robotFixed) setTimeout(say, 280); else back.then(say); } } }; if (!rain) palRunTo(tx).then(() => { if (!PAL.hurt && !PAL.down && !PAL.anim) palIdle(); }); }   // it arrives and stands, looking up at your card (glassRain: it stays where it is; the glass finds it anyway)
        S.busy = true;                                                  // until its glass has fallen (the robot is committed to this card)
        wait(up).then(() => shatter(t, S.hit[i], rb)).then(() => { if (!last) S.busy = false;
          if (last) { S.done = true; const r = RQ(`.tile[data-i="${S.it.a}"]`); if (PAL.down) r.classList.add("nobuddy");
            r.querySelector(".ok").innerHTML = S.practice ? okHTML("The answer", ["practice"], false, "") : okHTML("The answer", ["0 XP", "0 marks"], false, ""); score(it, 0, "none", rec); fillBack(r, it); setHint(null);
            live(`The answer is ${L[it.a]}. ${whyOf(it)}`); wait(PAL.down ? (opts.robotFixed ? 450 : 1700) : 0).then(() => present(r, null)).then(showNext); }   // the answer rises as it hits the ground (robotFixed: as it goes down, not after; measured 2026-09-30: 6.9 s from the last tap to the answer)
          const first = [...RQA(".tile")].find(x => !S.gone.has(+x.dataset.i));
          if (first && !last) first.querySelector(".face").focus({ preventScroll: true });
          if (!last && !rb) sayHint(clue);                                // no robot to say it: the clue comes as the glass lands
          paintTiles(); say(); });
        if (last) toast("Answer: " + L[S.it.a], "no");
        else { toast("Not that one · " + (3 - S.tries) + " left", "no"); setHint(null); }   // the robot says the new clue once it is up
        live(`${L[i]} is wrong and removed. ${last ? "The answer is " + L[S.it.a] + "." : (3 - S.tries) + (3 - S.tries === 1 ? " try" : " tries") + " left."}`);
      }
      paintTop(); say();
    }

    // The back: the medal line (set by the caller), the answer, why it is right, and why the others are not.
    const whyOf = it => (WHY[it.n] || {}).why || (it.clues || [])[0] || "";
    // A finished question, revisited: its end state (as after the big card was put back), to look at; the marks stand.
    function restore(b) { const it = S.it, tile = i => RQ(`.tile[data-i="${i}"]`), r = tile(it.a);
      S.done = true; S.tries = b.tries || 0; S.tier = b.tier; (b.gone || []).forEach(i => { S.gone.add(i); leaveGap(tile(i), false); });   // revisit: already closed up
      fillBack(r, it); r.querySelector(".ok").innerHTML = b.ok || ""; if (b.tier !== "none") r.classList.add(b.tier); r.classList.add("flipped");
      killWrong(); paintTiles(); paintTop(); say(); showNext(); palSize(); }
    // The medal line in parts (the tier's name, what it paid, how it was earned), so a skin can lay it out; read as one line it is
    // what it always was ("Gold · +100 XP · +2 marks": the separators are text). Only fixed strings and numbers go in.
    function okHTML(name, bits, medal, sub) {
      return (medal ? '<span class="medal" aria-hidden="true"></span>' : "") + '<span class="ok-name">' + name + "</span>" +
        bits.map(b => '<span class="ok-sep"> · </span><span class="ok-bit">' + b + "</span>").join("") + (sub ? '<span class="ok-sub">' + sub + "</span>" : ""); }
    // the answer as its letter + its text (the paper's text by textContent, never HTML); reads "D · seed germination." as before
    function fillBack(t, it) { const w = WHY[it.n] || {};
      const ans = t.querySelector(".ans"); ans.textContent = ""; const l = document.createElement("span"), x = document.createElement("span");
      l.className = "ans-l"; l.textContent = L[it.a]; x.className = "ans-t"; x.textContent = it.opts[it.a];
      const sep = document.createElement("span"); sep.className = "ans-sep"; sep.textContent = " · "; ans.append(l, sep, x); t.querySelector(".why").textContent = whyOf(it);
      t.querySelector(".not").innerHTML = w.not ? "Why not the others · " + w.not : ""; t.querySelector(".back").removeAttribute("aria-hidden"); }
    // Where the learner goes next, and how: inside the same question group (1.1.1 -> 1.1.5) a tap anywhere continues; the
    // Next button only between groups, named for the group it opens ("Question 1.3").
    const nextN = () => ORDER[(ORDER.indexOf(S.it.n) + 1) % ORDER.length];
    const sameGroup = () => (GROUP[nextN()] || {}).id === (GROUP[S.it.n] || {}).id;
    function placeNext() { const hero = $("heroLayer").querySelector(".tile.hero"), onPanel = opts.after === "panel", cont = hero && (onPanel || sameGroup());
      NEXT.querySelector("span").textContent = onPanel ? "Next" : sameGroup() ? "Continue" : (GROUP[nextN()] || {}).title || "Next question";   // on the panel: Back / Next
      NEXT.classList.remove("skip"); NEXT.removeAttribute("aria-label");   // answered: no longer a skip
      let c = $("cont"); if (cont && !c) { c = document.createElement("button"); c.className = "cont"; c.id = "mq-cont"; c.onclick = e => { e.stopPropagation(); onPanel ? dismiss() : next(); }; }
      if (c) c.textContent = onPanel ? "Tap anywhere to close" : "Tap anywhere to continue";
      if (cont) { $("heroLayer").appendChild(c); if (onPanel) ($("after") || $("stage")).appendChild(NEXT); else NEXT.remove(); } else { if (c) c.remove(); (hero ? $("heroLayer") : $("after") || $("stage")).appendChild(NEXT); }
      if ($("retry")) $("retry").hidden = opts.retry === false || !(S.done && !hero) || S.tier === "gold"; }   // gold needs no second go
    // A tap outside the open card, or on it: inside a group it continues; between groups it puts the card back.
    // The map: every group (as on the paper) and its sub-questions, each with its result; a tap opens that question.
    function openMap() { if (S.busy) return; const groups = [];
      ORDER.forEach(n => { const g = GROUP[n] || {}; let row = groups.find(x => x.g === g); if (!row) groups.push(row = { g, items: [] }); row.items.push(n); });
      $("msList").innerHTML = groups.map(({ g, items }) => `<div class="ms-grp">${g.title || ""}${g.kind ? " · " + g.kind : ""}</div>` + items.map(n => { const b = book[n], it = ITEMS[n];
        return `<button class="ms-q ${b ? b.tier : ""}${n === S.it.n ? " cur" : ""}" data-q="${n}"><span class="n">${n}</span><span class="t">${it.q.replace(/<[^>]+>/g, "")}</span><span class="d" aria-label="${b ? (b.tier === "none" ? "not answered" : b.tier) : n === S.it.n ? "current" : "not started"}"></span></button>`; }).join("")).join("");
      $("msList").querySelectorAll(".ms-q").forEach(b => b.onclick = () => { closeMap(); if (b.dataset.q !== S.it.n) go(b.dataset.q); });
      $("mapSheet").hidden = false; $("msX").focus(); }
    function closeMap() { $("mapSheet").hidden = true; $("mapBtn").focus({ preventScroll: true }); }
    $("mapBtn").onclick = () => opts.onMap ? opts.onMap() : openMap(); $("msX").onclick = closeMap;
    $("mapSheet").addEventListener("click", e => { if (e.target === e.currentTarget) closeMap(); });
    listen(document, "keydown", e => { if (e.key === "Escape" && !$("mapSheet").hidden) { e.stopImmediatePropagation(); closeMap(); } }, true);
    function tapOut() { if (opts.after !== "panel" && S.done && !S.busy && $("cont") && $("cont").isConnected) next(); else dismiss(); }   // on the panel a tap only closes
    function autoClose() { if (!opts.autoClose || opts.after !== "panel") return; const S0 = S; clearTimeout(S.acT);
      const tryClose = n => { if (S !== S0 || !S.heroT || !S.heroT.classList.contains("hero")) return; if (S.busy && n < 20) { S.acT = setTimeout(() => tryClose(n + 1), 200); return; } dismiss(); };
      S.acT = setTimeout(() => tryClose(0), opts.autoClose); }
    function showNext() { autoClose(); placeNext(); NEXT.classList.add("show"); ($("cont") && $("cont").isConnected ? $("cont") : NEXT).focus({ preventScroll: true }); nextInView(); }
    // Under the grid, Next can land behind the dock's solid fade (a tall question on a short screen): bring it up into view.
    function nextInView() { if (NEXT.parentElement !== $("stage")) return; const d = RQ(".dock").getBoundingClientRect(), clear = d.top + d.height * 0.4, r = NEXT.getBoundingClientRect();
      if (r.bottom > clear) SC.scrollBy({ top: r.bottom - clear + 12, behavior: reduced ? "auto" : "smooth" }); }

    // The hero: the card leaves its slot (an empty slot keeps the grid still), grows to the centre over a scrim, then
    // (right answer) shines in its medal colour and flips twice, landing on its back; (revealed answer) turns once, calmly.
    // The companion on the big card. One 3D view only (phones cap WebGL contexts); none on the small cards.
    const BUDDY = { src: "assets/companion-robot.glb", still: "assets/companion-stand.webp" };
    const BUDDY_3D = !reduced && !(navigator.connection && navigator.connection.saveData);
    const MOVE = { gold: { clip: "dance", from: 4.5 }, silver: { clip: "clap" }, bronze: { clip: "clap" }, none: { clip: "defeat", end: 5.5, fit: 0.85 } };   // lying down it spans ~2.1 units: framed wider
    // Warm the cache while the learner reads the question, so the robot is there when the card lands.
    // opts.noPal: no robot on this page at all (Exam Practice on a phone, Murci 2026-10-03: "we can just use that circled image
    // one"): nothing is fetched or drawn, its lines are the host's to say (it marks every tap: judge), and the glass sinks away
    const NOPAL = !!opts.noPal;
    if (BUDDY_3D && !NOPAL) (window.requestIdleCallback || setTimeout)(() => fetch(BUDDY.src).catch(() => {}));
    function buddyStill(box) { box.replaceChildren(Object.assign(document.createElement("img"), { src: BUDDY.still, alt: "" })); }
    // ONE robot element (PAL.el) for the whole page: it lives in its corner and moves into the big card and back.
    // model-floor keeps its renderer through a move and re-frames on a `fit` change, so it never reloads or doubles.
    const PAL = { el: null, x: 0, anim: null, timer: 0, down: false, hurt: false, sweeping: false, cleaning: false, queued: null, cleanT: 0 };
    function palMake() { const body = $("palBody"); if (NOPAL) { PAGE.classList.add("nopal"); LAYERS.classList.add("nopal"); return; } if (!BUDDY_3D) { buddyStill(body); return; }
      const mf = document.createElement("model-floor");
      [["src", BUDDY.src], ["autorotate", "off"], ["face", "user"], ["floor", "none"], ["fit", "0.8"], ["inplace", ""]].forEach(([k, v]) => mf.setAttribute(k, v));   // inplace: it stays centred in its box and turns about itself
      mf.addEventListener("failed", () => { PAL.el = null; buddyStill(body); }); body.appendChild(mf); PAL.el = mf; palGreet(); }
    // Play a clip: clear the play options, set this one's, then ask for "" then the clip (so the same clip restarts).
    function palClip(clip, o = {}) { const m = PAL.el; if (!m) return;
      ["loop", "hold", "from", "paused", "speed", "fade"].forEach(k => m.removeAttribute(k));
      if (o.once) m.setAttribute("loop", "once"); if (o.hold != null) m.setAttribute("hold", o.hold); if (o.from) m.setAttribute("from", o.from); if (o.paused) m.setAttribute("paused", "");
      if (o.speed) m.setAttribute("speed", o.speed); if (o.fade) m.setAttribute("fade", o.fade);
      m.setAttribute("fit", String(o.fit || 0.8)); m.setAttribute("clip", ""); m.setAttribute("clip", clip); }
    const GREET_POSE = 1.95;   // measured on greet_04 (2.79 s): the arm raised out to the side, open hand up (Murci: it stands like this)
    // (opts.noWave: it goes straight to the pose, no wave: Exam Practice's question pages, Murci 2026-09-30)
    const palGreet = () => { if (!palFree()) return; if (opts.noWave) return palIdle(); palClip("greet", { once: true, hold: GREET_POSE }); };   // waves, then holds with the hand raised
    const palIdle = () => palClip("greet", { once: true, from: GREET_POSE - 0.05, hold: GREET_POSE, fade: 0.25 });   // standing: the same raised-hand frame
    // Free = standing in its spot: not running, hurt, down, sweeping or inside a card.
    const palFree = () => !PAL.anim && !PAL.down && !PAL.sweeping && !PAL.hurt && !$("pal").classList.contains("away");
    // Movement. The run clip is authored in place; measured, its planted foot moves 3.51 units/s, and the box shows 2·H·fit
    // units (H 2.4, fit 0.8) over its height, so px/s = 3.51 · rate · boxHeight / 3.84. Moving the box at exactly that pace
    // is what keeps the feet from sliding. `translate` (not transform) carries the position, so the jump arcs compose with it.
    // robotFixed cleanup (Murci, 2026-09-30: the sweep ran ~6 s into the next question): a brisk sweep and return, and a tap during it waits
    // (2026-10-01: a host that waits for the sweep before its next question, Exam Practice's cleanUp, wants it easy, not a dash:
    // Murci, "it should not run too fast")
    const CLEAN_SWEEP = 1.6, CLEAN_RUN = 1.4;
    const RUN_RATE = 1.0, SWEEP_RATE = 1.2;   // px/s = rate x box height: cut as the robot grew, so its pace on screen holds   // an unhurried jog (Murci: slower); the sweep a little quicker
    const palSpeed = rate => 3.513 * rate * ($("pal").offsetHeight / 3.84);
    // Small while the learner chooses (CSS gives it a size on a phone only): the question is open and the robot is home and free.
    function palSize() { const pal = $("pal"), on = !!S && !S.done && !S.busy && !PAL.anim && !PAL.hurt && !PAL.down && !PAL.sweeping && PAL.x === 0 && !pal.classList.contains("away");
      pal.classList.toggle("small", on); }
    function palBase() { const r = $("pal").getBoundingClientRect(); return { left: r.left - PAL.x, top: r.top, w: r.width, h: r.height }; }
    function palStop() { const pal = $("pal"); if (PAL.anim) { PAL.x = parseFloat(getComputedStyle(pal).translate) || 0; PAL.anim.cancel(); PAL.anim = null; pal.style.translate = `${PAL.x}px 0`; } }
    function palRunTo(tx, rate = RUN_RATE) { const pal = $("pal"), m = PAL.el; clearTimeout(PAL.timer); palStop(); palPoint(false);
      const from = PAL.x, d = tx - from; PAL.x = tx; pal.style.translate = `${tx}px 0`;
      if (Math.abs(d) < 6 || reduced || !m) { if (m) m.setAttribute("yaw", "0"); return Promise.resolve(); }
      m.setAttribute("yaw", d > 0 ? "1.35" : "-1.35"); palClip("run", { speed: rate, fade: 0.18 });        // three-quarters: its face stays in view
      PAL.anim = pal.animate([{ translate: `${from}px 0` }, { translate: `${tx}px 0` }], { duration: Math.abs(d) / palSpeed(rate) * 1000, easing: "cubic-bezier(.3,.05,.45,1)" });
      const a = PAL.anim; return a.finished.then(() => { if (PAL.anim === a) { PAL.anim = null; m.setAttribute("yaw", "0"); } }, () => {}); }
    const palRunMs = (tx, rate = RUN_RATE) => Math.abs(tx - PAL.x) / palSpeed(rate) * 1000;
    // Under a card: its centre below the card's centre, kept on screen.
    function palUnder(tile) { const B = palBase(), c = tile.getBoundingClientRect(); return Math.max(4 - B.left, Math.min(innerWidth - B.left - B.w - 4, c.left + c.width / 2 - B.left - B.w / 2)); }
    // Its head and shoulders, as the glass meets them: a curve from the top of the head down to the shoulders (screen px).
    // The figure fills 2.4 / 3.84 = 62.5% of the box height, centred, so its head top is 18.75% down the box.
    function palHead(tx) { const B = palBase(); return { cx: B.left + tx + B.w / 2, headY: B.top + B.h * 0.1875, halfW: B.h * 0.15, drop: B.h * 0.12 }; }
    function jolt() { if (reduced) return; const kf = [{ transform: "none" }, { transform: "translate(-6px,4px)" }, { transform: "translate(5px,-3px)" }, { transform: "translate(-3px,2px)" }, { transform: "translate(1px,-1px)" }, { transform: "none" }];
      [$("stage"), $("shards"), $("palBody")].forEach(e => e.animate(kf, { duration: 360, easing: "ease-out" })); }
    // Hit by the glass. Measured on defeat_03: 0.55 s the head snaps back, 0.8-1.3 s it jolts, 1.6-2.0 s it slumps, 2.5-3.1 s it
    // goes down, 4.0 s+ it lies on the floor. So a first miss flinches, a second staggers, the last knocks it down.
    const HURT = [{ hold: 1.1, back: 760 }, { hold: 2.2, back: 1900 }];
    // glassRain: after the hit it runs to the other half of the screen from where it was hit (home when it was on the
    // right). It cannot get away: the next wrong card's glass rains there too.
    function palAway() { const B = palBase(), me = B.left + PAL.x + B.w / 2; return me < innerWidth / 2 ? Math.max(0, innerWidth - B.left - B.w - 4) : 0; }
    // The thought bubble opens toward the room: to its left when the robot stands on the right half (glassRain only).
    function palSide() { if (!opts.glassRain) return; const B = palBase(); $("pal").classList.toggle("sayleft", B.left + PAL.x + B.w / 2 > innerWidth / 2); }
    function palHit(n, last, to = 0) { const m = PAL.el; if (!m) return; palPoint(false); $("clue").classList.remove("show");
      if (last) { PAL.down = true; PAL.hurt = false; palClip("defeat", { once: true, from: 0.4, fade: 0.12 }); jolt(); buzz(HAPTIC.defeat); return; }
      const H = HURT[Math.min(n, 2) - 1]; PAL.hurt = true; palClip("defeat", { once: true, from: 0.4, hold: H.hold, fade: 0.12 });
      return new Promise(home => { PAL.timer = setTimeout(() => { PAL.hurt = false; palRunTo(to).then(() => { if (!PAL.anim && !PAL.down) palIdle(); palSize(); palSide(); home(); }); }, H.back); }); }
    // Next: it gets up if it is down (the fall played backwards), runs to the left of the pile, then sprints right pushing every
    // piece off the floor, and comes back round from the left to its spot. The next question is already up meanwhile.
    function palCleanUp() { const m = PAL.el, pieces = [...$("shards").children];
      if (!m || PAL.sweeping) return; clearTimeout(PAL.timer); PAL.hurt = false; $("pal").classList.remove("small");
      if (m.parentElement !== $("palBody")) palHome(null);                                     // it was inside the answer card: home first
      if (!pieces.length && !PAL.down) { palRunTo(0).then(() => { if (palFree()) palGreet(); palSize(); }); return; }
      // robotFixed: its home is on its rock, so it steps DOWN to the floor to sweep (the "floor" class eases it there), sweeps as
      // before, runs home and steps back UP (Murci, 2026-09-30: "swept by our robot like it was before, then back on the rock")
      const fixed = !!opts.robotFixed, pal = $("pal");
      if (fixed && !pieces.length) { if (PAL.down) { PAL.down = false; palClip("defeat", { once: true, from: 4.2, speed: -2.4, hold: 0.45, fade: 0.2 }); wait(1650).then(() => { if (palFree()) palIdle(); palSize(); }); } return; }
      PAL.sweeping = true; PAL.cleaning = true; clearTimeout(PAL.cleanT);
      PAL.cleanT = setTimeout(() => { if (!PAL.cleaning) return; PAL.cleaning = false; const q = PAL.queued; PAL.queued = null; if (q != null && S && !S.done && S.sel === q) press(q); }, 6000);   // a safety net: a stuck cleanup never blocks the cards
      const sweepAt = fixed ? CLEAN_SWEEP : SWEEP_RATE, runAt = fixed ? CLEAN_RUN : RUN_RATE;
      const getUp = () => PAL.down ? (palClip("defeat", { once: true, from: 4.2, speed: -2.4, hold: 0.45, fade: 0.2 }), wait(1650)) : Promise.resolve();
      const up = getUp().then(() => fixed ? (pal.classList.add("floor"), wait(reduced ? 0 : FLOOR_MS)) : null);   // up first (if it was down), then off the rock
      PAL.down = false;
      up.then(() => { const B = palBase(), xs = pieces.map(el => { const b = el.getBoundingClientRect(); return b.left + b.width / 2; });
        const leftOfPile = Math.min(...xs) - B.left - B.w * 0.9;
        return (leftOfPile < PAL.x - 8 ? palRunTo(Math.max(4 - B.left, leftOfPile), runAt) : Promise.resolve()).then(() => sweepRight(pieces, sweepAt)); })
      .then(() => { PAL.sweeping = false; return palRunTo(0, runAt); }).then(() => fixed ? (pal.classList.remove("floor"), wait(reduced ? 0 : FLOOR_MS)) : null)   // home: back up on its rock
      .then(() => { PAL.cleaning = false; clearTimeout(PAL.cleanT); if (palFree()) palGreet(); palSize(); cleaned();
        const q = PAL.queued; PAL.queued = null; if (q != null && S && !S.done && S.sel === q) press(q); });   // a card tapped while it cleaned: answered now
    }
    // the host's cleanUp() waits on this: the robot is back home (on its rock) with the floor clear
    function cleaned() { const f = PAL.onClean; PAL.onClean = null; clearTimeout(PAL.onCleanT); if (f) f(); }
    const FLOOR_MS = 460;   // robotFixed: the step down from its rock to the floor, and back up (nx-play.css eases .pal.floor over this)
    // the broken pieces sink off the floor and fade (a short, staggered drop): kept for a host that wants the glass gone without a sweep
    function dropAway(pieces) { pieces.forEach((el, k) => { const a = el.getAnimations(); a.forEach(x => x.commitStyles && x.commitStyles()); a.forEach(x => x.cancel());
      el.animate([{ opacity: 1 }, { opacity: 0, translate: "0 26px" }], { duration: 420, delay: (k % 8) * 30, easing: "ease-in", fill: "forwards" }).finished.then(() => el.remove(), () => el.remove()); }); }
    function sweepRight(pieces, rate = SWEEP_RATE) { const pal = $("pal"), B = palBase(), exit = innerWidth - B.left + 40, v = palSpeed(rate), start = PAL.x;
      const front0 = B.left + start + B.w * 0.62;                                                   // its leading foot
      pieces.forEach(el => { const b = el.getBoundingClientRect(), cx = b.left + b.width / 2, when = Math.max(0, (cx - front0) / v * 1000);
        if (cx > innerWidth + 4 || cx < -4) { el.remove(); return; }                                // thrown off-screen in the break: nothing to sweep, don't keep it
        setTimeout(() => { const dist = innerWidth + 60 - cx;                                          // pushed ahead of it, a little hop, off the edge
          el.animate([{ translate: "0 0" }, { translate: `${(dist * 0.15).toFixed(0)}px -7px`, offset: 0.14 }, { translate: `${dist.toFixed(0)}px 0` }],
            { duration: dist / (v * 1.12) * 1000, easing: "cubic-bezier(.2,.6,.4,1)", fill: "forwards" }).finished.then(() => el.remove(), () => el.remove()); }, when); });
      return palRunTo(exit, rate).then(() => {                                                      // off the right edge; back round from the left
        pal.classList.add("away"); PAL.x = -B.left - B.w - 30; pal.style.translate = `${PAL.x}px 0`; void pal.offsetWidth; pal.classList.remove("away"); });
    }
    // It turns to look at a card: yaw (radians) from where the card is relative to the robot.
    function palLook(el) { const m = PAL.el; if (!m || !palFree()) return; if (!el) { m.setAttribute("yaw", "0"); return; }
      const r = el.getBoundingClientRect(), p = $("pal").getBoundingClientRect();
      m.setAttribute("yaw", Math.max(-0.6, Math.min(0.9, ((r.left + r.width / 2) - (p.left + p.width / 2)) / innerWidth * 1.6)).toFixed(2)); }
    // Into the card: an arc from its corner to the card's centre, shrinking and fading as it dives in.
    // Between the floor and a card the robot does not travel: it dissolves (brightens, blurs, fades, sinking a touch toward
    // its feet) and materialises at the other end, the same frames reversed.
    const BLINK_MS = 300, BLINK_OUT = [{ opacity: 1, filter: "blur(0px) brightness(1)", transform: "none" }, { opacity: 0, filter: "blur(7px) brightness(1.8)", transform: "scale(0.94)" }],
      BLINK_IN = [...BLINK_OUT].reverse();
    function palJump(t) { const pal = $("pal"); $("clue").classList.remove("show"); palPoint(false); palStop(); PAL.sweeping = false; clearTimeout(PAL.timer); PAL.hurt = false;
      if (reduced || pal.classList.contains("away")) { pal.classList.add("away"); return Promise.resolve(); }
      return pal.animate(BLINK_OUT, { duration: BLINK_MS, easing: "cubic-bezier(.5,0,.75,0)" }).finished     // it dissolves where it stands
        .then(() => pal.classList.add("away"), () => pal.classList.add("away")); }
    // Home: back in its corner (it materialises there when it was in a card), and it greets.
    function palHome(fromEl) { const pal = $("pal"), body = $("palBody"), wasAway = pal.classList.contains("away");
      if (fromEl) { const box = fromEl.querySelector(".buddy"); if (box && box.querySelector("img")) box.replaceChildren(); }
      const inCard = !!(PAL.el && PAL.el.parentElement !== body);
      if (!inCard && !wasAway) return;                                                              // it never left: it's on the floor (standing, down or sweeping)
      if (inCard) { body.appendChild(PAL.el); PAL.el.setAttribute("floor", "none"); }            // out of the card: no floor under it
      PAL.x = 0; pal.style.translate = "0px 0"; pal.classList.remove("away"); palLook(null); palGreet();
      if (!wasAway || !fromEl || reduced) return;
      pal.animate(BLINK_IN, { duration: BLINK_MS + 60, easing: "cubic-bezier(.2,.8,.2,1)" }); }             // gone from the card, it materialises in its spot
    // Mount the robot on the back. frozen: holds the clip's first pose (it spins with the card); otherwise it is already
    // moving, or already down (lifting a small card again shows the end state, it does not replay the whole scene).
    // Into the card's back: the same robot element moves in. frozen: it holds the clip's first pose while the card spins
    // (unless the card has already landed). Otherwise it is already moving, or already down (the end state).
    function buddyIn(t, frozen) { const box = t.querySelector(".buddy"); if (!box) return;
      if (!PAL.el) { buddyStill(box); return; }
      const m = MOVE[S.tier], hold = frozen && !S.landed; box.appendChild(PAL.el); PAL.el.setAttribute("floor", "ring"); PAL.el.setAttribute("yaw", "0");   // it faces the learner when it dances or claps
      if (!reduced) box.animate(BLINK_IN, { duration: BLINK_MS + 60, delay: 80, fill: "backwards", easing: "cubic-bezier(.2,.8,.2,1)" });   // it materialises in the card, after the ~70 ms its 3D view takes to set up there (measured)
      palClip(m.clip, { once: !!m.end, from: m.end ? (hold ? 0 : m.end) : m.from, paused: hold, fit: m.fit || 0.72 }); }
    function buddyGo(t) { S.landed = true; if (PAL.el && t.contains(PAL.el)) PAL.el.removeAttribute("paused"); }
    // The wrong cards still standing go dark, one by one, once the right card is home.
    // after "panel": the broken ones come back too, dimmed (their glass stays on the floor until the robot sweeps it)
    function restoreGone() { if (opts.after !== "panel" || !S.gone.size) return;   // the glass stays on the floor: the robot sweeps it on Next
      S.gone.forEach(i => { const x = RQ(`.tile[data-i="${i}"]`); if (!x) return; ["visibility", "pointer-events", "display", "opacity", "transition"].forEach(k => x.style.removeProperty(k));
        x.removeAttribute("aria-hidden"); x.classList.remove("no", "raised", "sel");
        // the break left: its face hidden inline, its crack / crush / impact layers, and finished animations holding their end state
        x.getAnimations({ subtree: true }).forEach(a => a.cancel()); x.querySelectorAll(".vline, .vfill, .cracks, .crush, .impact").forEach(e => e.remove());
        const f = x.querySelector(".face"); if (f) f.style.removeProperty("visibility"); }); }
    function killWrong() { restoreGone(); [...RQA("#mq-tiles .tile")].filter(x => +x.dataset.i !== S.it.a && (opts.after === "panel" || !S.gone.has(+x.dataset.i)) && !x.classList.contains("dead"))
      .forEach((x, k) => { x.style.setProperty("--dd", (k * 0.12).toFixed(2) + "s"); x.classList.add("dead"); }); }

    const RAISE_MS = 380;
    // Raise the selected card: larger, on top, leaning 12% of the way toward the grid's middle. Returns when it is up (ms).
    // Measured on screenshot 2 (D, bottom-right, on a 355×96 card): its glass reached 73 px toward the middle, 41 px up over
    // B's lower strip, 13 px down, and pulled in 8 px on its outer side. Mirrored for the other corners; on one column it
    // grows a little each side instead.
    const PANE = { in: 73, out: -8, vin: 41, vout: 13 };
    function raise(t) { if (reduced) return 0; const g = $("tiles").getBoundingClientRect(), r = t.getBoundingClientRect();
      const leftSide = r.left + r.width / 2 < g.left + g.width / 2, topRow = r.top + r.height / 2 < g.top + g.height / 2, oneCol = r.width > g.width * 0.7;
      const h = oneCol ? [10, 10] : leftSide ? [PANE.out, PANE.in] : [PANE.in, PANE.out];          // [grow left, grow right]
      // [grow up, grow down]. One column: the first card grows up only into the gap above the cards (it covered the question's
      // last line, measured 2026-10-02); the rest of its 32 px goes down, over the card below.
      const above = $("tiles").previousElementSibling, roomU = above ? Math.max(0, r.top - above.getBoundingClientRect().bottom - 2) : 16, oU = Math.min(16, roomU);
      const v = oneCol ? [oU, 32 - oU] : topRow ? [PANE.vout, PANE.vin] : [PANE.vin, PANE.vout];
      // Inset values are negative to grow. Two columns: clamped to the grid's edges. One column (a phone): it may reach
      // 10 px into the page's side margin, and grows 16 px up and down, over its neighbours (8 px gaps).
      // One column: it stays inside the stage, which scrolls and so CLIPS (Murci, 2026-10-02: on a phone the raised card was cut
      // at the screen's edge; the stage starts 4 px left of the card, the 10 px grow went 6 px past it). A side without room gives
      // its share to the other, so the card still grows by the same amount, only shifted.
      const sr = $("stage").getBoundingClientRect(), roomL = Math.max(0, r.left - sr.left - 2), roomR = Math.max(0, sr.right - r.right - 2);
      const oL = Math.min(h[0], roomL), oR = Math.min(h[1] + h[0] - oL, roomR);
      const L = oneCol ? oL : Math.min(h[0], r.left - g.left), R = oneCol ? oR : Math.min(h[1], g.right - r.right);
      [["--rl", -L], ["--rr", -R], ["--rt", -v[0]], ["--rb", -v[1]]].forEach(([k, px]) => t.style.setProperty(k, px + "px"));
      t.classList.add("raised"); return RAISE_MS; }
    const VERDICT_MS = 440;                 // the green light shows this long before the right card moves
    // The right answer: a green hairline runs round the rim from the fingertip, both ways, meeting opposite, while green
    // light fills the glass from that point. (Perimeter position from the straight edges; the corners are small.)
    function verdictLight(t, hit, ok) { const face = t.querySelector(".face"), w = face.offsetWidth, h = face.offsetHeight, NS = "http://www.w3.org/2000/svg";
      const fr = face.getBoundingClientRect(), p = hit && hit.cx != null ? { x: hit.cx - fr.left, y: hit.cy - fr.top } : hit && hit.x > 0 ? hit : { x: w / 2, y: h / 2 }, R = Math.min(parseFloat(getComputedStyle(face).borderTopLeftRadius) || 17, h / 2, w / 2) - 1, P = 2 * (w + h - 4 * R);   // the rim follows the glass's own corner
      const d = [p.y, w - p.x, h - p.y, p.x], edge = d.indexOf(Math.min(...d));                                   // nearest edge: top, right, bottom, left
      const along = [Math.max(0, p.x - R), (w - 2 * R) + Math.max(0, p.y - R), (w - 2 * R) + (h - 2 * R) + Math.max(0, w - R - p.x), 2 * (w - 2 * R) + (h - 2 * R) + Math.max(0, h - R - p.y)][edge];
      const f = along / P * 1000;
      const svg = document.createElementNS(NS, "svg"); svg.setAttribute("class", ok ? "vline" : "vline no");   // no viewBox: drawn in the card's own pixels at every size
      // The rect is 100% of an SVG inset 1 px in the card (CSS), so as the card grows the line follows it with the card's own
      // corners (a viewBox stretched with the card stretched the corners too: 17 px became a 23 x 36 px oval, a second curve).
      const rc = document.createElementNS(NS, "rect"); [["x", 0], ["y", 0], ["width", "100%"], ["height", "100%"], ["rx", R], ["pathLength", 1000]].forEach(([k, v]) => rc.setAttribute(k, v)); svg.appendChild(rc);
      const fill = document.createElement("div"); fill.className = "vfill"; fill.style.setProperty("--vx", p.x + "px"); fill.style.setProperty("--vy", p.y + "px");
      if (ok) face.append(fill, svg); else face.append(svg);                                           // red: the rim only; the cracks glow red inside
      if (ok) { const lt = face.querySelector(".letter"); if (lt && !lt.querySelector(".vtick")) lt.insertAdjacentHTML("beforeend", '<svg class="vtick" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.6 12.6 L10 17 L18.6 7.6" pathLength="1"/></svg>'); }   // a tick in the letter badge: hidden here (mcq-play.css), a skin can show it
      if (reduced) { rc.style.strokeDasharray = "1000 0"; fill.style.opacity = "1"; return; }
      const kf = Array.from({ length: 11 }, (_, k) => { const u = k / 10, e = 1 - Math.pow(1 - u, 3), sHalf = 500 * e;   // both ends run outward, easing to meet
        return { offset: u, strokeDasharray: `${(2 * sHalf).toFixed(1)} ${(1000 - 2 * sHalf).toFixed(1)}`, strokeDashoffset: `${(-(f - sHalf)).toFixed(1)}` }; });
      rc.animate(kf, { duration: 380, fill: "forwards" });
      if (ok) fill.animate([{ opacity: 0, transform: "scale(0.6)", transformOrigin: `${p.x}px ${p.y}px` }, { opacity: 1, transform: "scale(1)", transformOrigin: `${p.x}px ${p.y}px` }], { duration: 420, easing: "cubic-bezier(.2,.7,.3,1)", fill: "forwards" }); }
    const SPIN = 540;                       // "flips two times revealing the back": it passes the back, the front, lands on the back
    const FLIP_MS = 2400, SHINE_MS = 900, GROW_MS = 800, BACK_MS = 700;

    // FLIP a card between two places: it is drawn where it was (r0) and eases to where it now is. `rot` keeps a flipped card flipped.
    function glide(t, r0, ms, rot) { const r1 = t.getBoundingClientRect();
      const dx = r0.left + r0.width / 2 - (r1.left + r1.width / 2), dy = r0.top + r0.height / 2 - (r1.top + r1.height / 2);
      return t.animate([{ transform: `translate(${dx}px, ${dy}px) scale(${r0.width / r1.width}, ${r0.height / r1.height})${rot}` }, { transform: rot || "none" }],
        { duration: ms, easing: "cubic-bezier(.22,.8,.25,1)" }).finished; }
    // Lift a card out of its slot (the slot keeps the grid still) to the centre, over the scrim.
    // The hero layer is fixed and the chips scroll with the page: keep the card's top under wherever the chips are now
    // (a smooth scroll still running when a card opens moved them 67 px after it was measured once).
    function heroTop() { const t = opts.topOffset ? opts.topOffset() : RQ(".top").getBoundingClientRect().bottom; $("heroLayer").style.setProperty("--ht", Math.max(16, Math.round(t + 12)) + "px"); }
    // heroIn "stage": the layer takes the panel's box (clipped to what is on screen), so the card fills the panel, not the screen
    function heroBox() { if (opts.heroIn !== "stage") return; const L = $("heroLayer"), on = !!L.querySelector(".tile.hero");
      L.classList.toggle("inpanel", on); if (!on) { ["top", "left", "width", "height"].forEach(k => L.style.removeProperty(k)); L.classList.remove("tight"); $("stage").style.removeProperty("min-height"); dockAfter(); return; }
      const place = () => { const st = $("stage").getBoundingClientRect(), sc = opts.screen ? PAGE.getBoundingClientRect() : { top: 0, bottom: innerHeight };
        const top = Math.max(st.top, sc.top), bottom = Math.min(st.bottom, sc.bottom);
        Object.assign(L.style, { top: top + "px", left: st.left + "px", width: st.width + "px", height: Math.max(0, bottom - top) + "px" }); return sc; };
      const sc = place(); heroFit(L, sc) && place(); dockAfter(); }
    // The big card must fit the panel it fills (Murci, 2026-09-30: "the correct card after flipping has a huge part of it hidden
    // below the panel"; measured at 1348x648: the panel 332 px, the card's back 338 + the "Tap anywhere" row). Its need is its
    // back's natural height plus the layer's padding and the tap row. The panel grows to it while the card is up (down to 16 px
    // off the screen's bottom); past that the card tightens (.tight: a smaller medal, less air); past that the layer scrolls,
    // with no scrollbar drawn. Returns true when the panel changed size (the layer is placed again).
    function heroFit(L, sc) { const st = $("stage"), t = L.querySelector(".tile.hero"), b = t && t.querySelector(".back"); if (!b) return false;
      const need = () => { b.style.setProperty("min-height", "0", "important"); const cs = getComputedStyle(L), c = $("cont");
        const h = b.offsetHeight + parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom) + (opts.after === "panel" ? (c && c.isConnected ? c.offsetHeight : 38) + (parseFloat(cs.rowGap) || 10) : 0);
        b.style.removeProperty("min-height"); return Math.ceil(h); };
      const before = st.style.minHeight; L.classList.remove("tight");
      const room = Math.floor(sc.bottom - 16 - st.getBoundingClientRect().top);
      let n = need(); if (n > room) { L.classList.add("tight"); n = need(); }
      const want = Math.min(n, room), has = st.getBoundingClientRect().height;
      if (want > has + 1) st.style.minHeight = want + "px"; else if (!before) return false;
      return st.style.minHeight !== before; }
    listen(SC, "scroll", () => { if ($("heroLayer").querySelector(".tile.hero")) { heroTop(); heroBox(); } }, { passive: true });
    listen(window, "resize", () => heroBox());
    function grow(t) {
      heroTop();                                                        // phone: the card starts under the chips (they wrap to two rows on a narrow phone)
      const r0 = (t.classList.contains("raised") ? t.querySelector(".face") : t).getBoundingClientRect(); t.classList.remove("raised"); /* the grow starts from the grown pane */ if (!S.slot) { S.slot = document.createElement("div"); S.slot.className = "slot"; }
      S.slot.style.height = r0.height + "px"; S.heroT = t;
      t.classList.remove("dealt"); t.style.animation = "none";                                 // a tap during the deal-in must not carry the deal animation into the hero
      t.replaceWith(S.slot); $("heroLayer").appendChild(t); t.classList.add("hero"); $("scrim").classList.add("on"); heroBox();
      ["--tx", "--ty"].forEach(k => t.querySelector(".face").style.removeProperty(k));
      return reduced ? Promise.resolve() : glide(t, r0, GROW_MS, t.classList.contains("flipped") ? " rotateY(180deg)" : "");
    }
    // Back to its slot, still flipped (tap outside, tap the card, or Esc). Tapping the small card lifts it again.
    function dismiss() { const t = S.heroT; if (!t || S.busy || !t.classList.contains("hero")) return;
      const r0 = t.getBoundingClientRect(); palHome(t); S.slot.replaceWith(t); t.classList.remove("hero"); $("scrim").classList.remove("on"); heroBox();
      if (opts.fit) { t.style.removeProperty("min-height"); fitTile(t); }
      if (reduced) { killWrong(); return; } S.busy = true; $("stage").style.zIndex = "36";   // the card glides home above the fading scrim, never under its blur
      placeNext(); glide(t, r0, BACK_MS, " rotateY(180deg)").then(() => { S.busy = false; $("stage").style.zIndex = ""; killWrong(); if (opts.fit) fitCards(); nextInView(); }); }   // refit: the flipped card is sized by its back   // Next goes back under the grid with it
    // heroIn "stage": the turn inside the panel (Murci, 2026-09-30: "it should look cool when it spins inside the parent card").
    // Measured before: the panel-wide card swelled up to 115 px past the panel mid-turn (perspective on a 900 px card plus
    // the lift toward the viewer), was clipped, and flashed the panel's scrollbars. Here it pulls back into the panel as it
    // turns (78% at mid-turn, under a deeper perspective: its near edge stays inside), winds up a touch, whips round and
    // lands with a small overshoot (one eased curve, so no kinks), while a glare sweeps its faces. Transform and opacity only.
    function spinInPanel(t, big) {
      const L = $("heroLayer"), turn = big ? SPIN : 180, dip = big ? 0.22 : 0.1, ms = big ? 2100 : 1000;
      L.classList.add("spinning"); t.style.willChange = "transform";
      const kf = Array.from({ length: 9 }, (_, k) => { const q = k / 8;
        return { offset: q, transform: `rotateY(${(turn * q).toFixed(1)}deg) scale(${(1 - dip * Math.sin(q * Math.PI)).toFixed(4)})` }; });
      const glares = [...t.querySelectorAll(".side")].map(sd => { const g = document.createElement("i"); g.className = "glare"; g.setAttribute("aria-hidden", "true");
        const b = document.createElement("b"); g.appendChild(b); sd.appendChild(g);
        b.animate([{ transform: "translateX(-100%)", opacity: 0 }, { opacity: 1, offset: 0.3 }, { opacity: 1, offset: 0.75 }, { transform: "translateX(100%)", opacity: 0 }],
          { duration: ms, easing: "cubic-bezier(.45,0,.25,1)" }); return g; });
      return t.animate(kf, { duration: ms, easing: big ? "cubic-bezier(.6,-0.18,.3,1.18)" : "cubic-bezier(.5,-0.1,.3,1.1)" }).finished
        .finally(() => { L.classList.remove("spinning"); t.style.removeProperty("will-change"); glares.forEach(g => g.remove()); });
    }
    function lift(t) { if (S.busy) return; S.busy = true; if (opts.celebrate === "corner") { grow(t).then(() => { placeNext(); S.busy = false; }); return; }
      grow(t).then(() => { placeNext(); return palJump(t); }).then(() => { buddyIn(t, false); S.busy = false; }); }

    function present(t, tier) {
      if (tier) t.classList.add(tier); S.busy = true; S.tier = tier || "none";
      const corner = opts.celebrate === "corner"; if (corner) t.classList.add("nobuddy");   // corner: the card has no robot slot; it celebrates on its rock
      if (reduced) { grow(t); t.classList.remove("sel"); t.classList.add("flipped"); if (!corner) { palJump(t); buddyIn(t, false); } S.busy = false; return Promise.resolve(); }
      const g = grow(t); palLook(t);
      return g.then(() => {
        if (!PAL.down && !corner) palJump(t).then(() => buddyIn(t, true));                       // it vanishes and appears in the card, then rides the spin frozen (not when it's down)
        if (!tier) return wait(opts.robotFixed ? 300 : 650);
        t.querySelectorAll(".vline, .vfill").forEach(x => x.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 300, fill: "forwards" }).finished.then(() => x.remove()));
        t.classList.remove("yes"); t.classList.add("shine"); buzz(HAPTIC.shine);   // green hands over to the medal colour                                          // the shine, before it turns
        return t.animate([{ transform: "none" }, { transform: "scale(1.03)" }, { transform: "none" }], { duration: SHINE_MS, easing: "ease-in-out" }).finished;
      }).then(() => {
        t.classList.remove("sel", "shine"); t.classList.add("flipped");                          // the class holds the end state (180 = 540 mod 360)
        if (opts.heroIn === "stage") return spinInPanel(t, !!tier);
        // One eased turn: the rotation is linear in the eased progress (no kinks); the lift is a sine arc, sampled at 9 points.
        const turn = tier ? SPIN : 180, rise = (tier ? 90 : 40) * (innerWidth <= 600 ? 0.4 : 1), swell = tier ? 0.05 : 0.02;   // a phone has no room above the card: a smaller lift
        const kf = Array.from({ length: 9 }, (_, k) => { const q = k / 8, a = Math.sin(q * Math.PI);
          return { offset: q, transform: `translateZ(${(a * rise).toFixed(1)}px) scale(${(1 + a * swell).toFixed(4)}) rotateY(${(turn * q).toFixed(1)}deg)` }; });
        return t.animate(kf, { duration: tier ? FLIP_MS : 1100, easing: "cubic-bezier(.45,0,.25,1)" }).finished;
      }).then(() => { buddyGo(t); if (corner && !PAL.down && PAL.el) { const m = MOVE[S.tier]; palClip(m.clip, { once: !!m.end, from: m.end || m.from }); }   // corner: it celebrates where it stands, as the card lands
        if (!tier && !PAL.down) buzz(HAPTIC.defeat); S.busy = false; });                  // it lands: the robot dances, claps, or is defeated
    }
    function bump(id) { const b = $(id); b.classList.remove("bump"); void b.offsetWidth; b.classList.add("bump"); }
    // Marks: out of the paper's total (P.total, 150 for LS P1). A question counts once (its first sitting); a later sitting changes nothing.
    function score(it, mk, tier, rec = {}) { if (it.n in book) return; book[it.n] = { got: mk, of: it.marks, tier, ...rec }; paintTop(); if (opts.onScore) opts.onScore({ n: it.n, item: it, marks: mk, tier, ...rec });   // `it` captured at answer time: a question switch mid-animation can't misfile it
      if (!S.marksFlown) { $("mk").textContent = Object.values(book).reduce((a, b) => a + b.got, 0); bump("marksBox"); }   // flown marks already updated it as they landed
      $("marksBox").setAttribute("aria-label", `${Object.values(book).reduce((a, b) => a + b.got, 0)} of ${$("mkOf").textContent} marks`); }
    // Marks earned (a first-try right answer): the "2 marks" under the cards beeps (two gold pulses) and turns gold; a copy
    // of it lifts off where it is and travels in an arc to the marks counter, which counts up and rings as it lands.
    // A host's own counter (opts.targets.marksBox) gets the ring; the host updates its number itself.
    function flyMarks(mk) {
      const src = RQ(".qmarks"), host = (opts.targets || {}).marksBox, to = host || $("marksBox");
      if (!src || !to) { if (opts.onMarksLanded) opts.onMarksLanded(mk); return Promise.resolve(); }
      src.classList.add("earned");
      return wait(420).then(() => {   // lifts off before the answer card grows over the label
        const a = src.getBoundingClientRect(), b = to.getBoundingClientRect(), c = document.createElement("div");
        c.className = "mfly"; c.textContent = "+" + mk + (mk === 1 ? " mark" : " marks"); LAYERS.appendChild(c);
        const cw = c.offsetWidth, ch = c.offsetHeight, x0 = a.right - cw, y0 = a.top + a.height / 2 - ch / 2;
        c.style.left = x0 + "px"; c.style.top = y0 + "px";
        const dx = b.left + b.width / 2 - (x0 + cw / 2), dy = b.top + b.height / 2 - (y0 + ch / 2);
        return c.animate([{ transform: "translate(0px, 0px) scale(1)" }, { transform: `translate(${(dx * 0.45).toFixed(0)}px, ${(dy * 0.45 - 70).toFixed(0)}px) scale(1.18)`, offset: 0.45 },
          { transform: `translate(${dx.toFixed(0)}px, ${dy.toFixed(0)}px) scale(0.5)`, opacity: 0.85 }], { duration: 860, easing: "cubic-bezier(.35,.1,.3,1)", fill: "forwards" }).finished
          .then(() => { c.remove();
            to.animate([{ boxShadow: "0 0 0 0 rgba(245,196,81,0.8)", scale: "1" }, { boxShadow: "0 0 0 10px rgba(245,196,81,0)", scale: "1.12", offset: 0.35 }, { boxShadow: "0 0 0 16px rgba(245,196,81,0)", scale: "1" }], { duration: 620, easing: "ease-out" });
            if (!host) { S.marksFlown = true; countUp($("mk"), Object.values(book).reduce((x, y) => x + y.got, 0) + mk); } if (opts.onMarksLanded) opts.onMarksLanded(mk); }); }); }
    function countUp(el, to) { let v = parseInt(el.textContent, 10) || 0; if (to <= v) { el.textContent = to; return; } const step = () => { v++; el.textContent = v; if (v < to) setTimeout(step, 110); }; step(); }

    // The card breaks like glass: a spider-web of cracks from where it was tapped, then shards along those cracks fly, spin and fall;
    // the card is taken out and the others close the gap. Shards carry their own piece of the text (a clipped copy).
    // The break, modelled on real glass.
    // 1 · Cracks: radial cracks that wander (a random walk pulled back to its heading) and sometimes fork, joined by two
    //     rings into a spider-web, from a crushed white spot with micro-cracks. Drawn with depth (dark under bright),
    //     thicker near the impact, spreading outward at ~1.4 px/ms rather than appearing at once.
    // 2 · Pieces are cut exactly along those cracks (11 rays × 3 rings = 33), each carrying its bit of the card and a bright
    //     cut edge. The hairline gaps open first, then the inner pieces leave, the outer ones a beat later.
    // 3 · The fall is simulated: gravity, spin (small pieces spin fast, big ones slowly), a bounce (small pieces more),
    //     friction, then lying flat on the pile at the bottom of the screen. A few pieces clink.
    function shatter(tile, hit, rb) {                                                        // rb: the robot under it (head curve, minHold, onHit), or null
      const face = tile.querySelector(".face"), r = face.getBoundingClientRect(), w = face.offsetWidth, h = face.offsetHeight, k = r.width / w, NS = "http://www.w3.org/2000/svg";
      const hp = hit && hit.cx != null ? { x: hit.cx - r.left, y: hit.cy - r.top } : hit;
      const p = hp && hp.x > 0 ? { x: Math.min(w - 10, Math.max(10, hp.x)), y: Math.min(h - 10, Math.max(10, hp.y)) } : { x: w * 0.5, y: h * 0.45 };
      if (reduced) { tile.style.transition = "opacity 200ms"; tile.style.opacity = "0"; return wait(220).then(() => leaveGap(tile)); }
      const inside = q => q.x >= 0 && q.x <= w && q.y >= 0 && q.y <= h;
      // Radial cracks: a random walk from the impact, each step pulled back toward the ray's own heading so rays never cross.
      const N = 11, rays = [];
      for (let k = 0; k < N; k++) {
        const base = (k / N) * Math.PI * 2 + rnd(-0.17, 0.17); let a = base, q = { ...p }; const pts = [{ ...p }], dist = [0];
        while (true) { a += rnd(-0.16, 0.16); a += (base - a) * 0.35; const step = rnd(9, 15), nq = { x: q.x + Math.cos(a) * step, y: q.y + Math.sin(a) * step };
          if (!inside(nq)) { const e = edge(q, a, w, h); pts.push(e); dist.push(dist[dist.length - 1] + Math.hypot(e.x - q.x, e.y - q.y)); break; }
          pts.push(nq); dist.push(dist[dist.length - 1] + step); q = nq; }
        rays.push({ base, pts, dist, len: dist[dist.length - 1] });
      }
      const at = (ry, t) => { t = Math.max(0, Math.min(ry.len, t)); let i = 1; while (i < ry.dist.length - 1 && ry.dist[i] < t) i++;
        const a = ry.pts[i - 1], b = ry.pts[i], u = (t - ry.dist[i - 1]) / ((ry.dist[i] - ry.dist[i - 1]) || 1); return { x: a.x + (b.x - a.x) * u, y: a.y + (b.y - a.y) * u }; };
      const slice = (ry, t0, t1) => { const out = [at(ry, t0)]; ry.pts.forEach((q, i) => { if (ry.dist[i] > t0 && ry.dist[i] < t1) out.push(q); }); out.push(at(ry, t1)); return out; };
      // Two rings where the rays are joined: distance along each ray (jittered), so the web is irregular.
      const RING = [0.2, 0.47]; rays.forEach(ry => { ry.ring = RING.map(f => ry.len * f * rnd(0.84, 1.16)); ry.q = ry.ring.map(t => at(ry, t)); });
      // Draw: each crack twice (dark split, bright light), tapering outward, spreading from the impact.
      const svg = document.createElementNS(NS, "svg"); svg.setAttribute("class", "cracks"); svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
      const lo = document.createElementNS(NS, "g"), rd = document.createElementNS(NS, "g"), hi = document.createElementNS(NS, "g");
      rd.setAttribute("class", "redglow"); hi.setAttribute("class", "glow"); svg.append(lo, rd, hi);
      const SPEED = 1.4;
      const draw = (pts, width, startDist, alpha = 1, lag = 0) => { const len = pts.reduce((m, q, k) => k ? m + Math.hypot(q.x - pts[k - 1].x, q.y - pts[k - 1].y) : 0, 0); if (len < 1) return;
        const d = "M" + pts.map(q => q.x.toFixed(1) + " " + q.y.toFixed(1)).join(" L");
        [[lo, "lo", width + 1.2, 0.7], [rd, "rd", width + 0.3, 0], [hi, "hi", Math.max(0.45, width * 0.42), 0]].forEach(([g, cls, sw, off]) => { const e = document.createElementNS(NS, "path"); e.setAttribute("class", cls); e.setAttribute("d", d);
          e.setAttribute("stroke-width", sw.toFixed(2)); if (off) e.setAttribute("transform", `translate(${off} ${off})`); if (alpha < 1) e.setAttribute("opacity", alpha.toFixed(2));
          e.style.strokeDasharray = len; e.style.strokeDashoffset = len; g.appendChild(e);
          e.animate([{ strokeDashoffset: len }, { strokeDashoffset: 0 }], { duration: len / SPEED, delay: startDist / SPEED + lag, easing: "cubic-bezier(.3,.6,.4,1)", fill: "forwards" }); }); };
      // It grows the way glass does: four main cracks shoot out first, the other seven follow (~0.2 s), the rings link them
      // as the rays pass, then forks, a third partial ring and short hairlines fill the web in. Only the 11 rays and 2 rings
      // cut pieces (33, as measured for frame rate); the rest is drawn on the glass.
      const FIRST = new Set([0, 3, 6, 8]); rays.forEach((ry, k) => ry.d0 = FIRST.has(k) ? 0 : 170 + rnd(0, 90));
      rays.forEach(ry => { draw(slice(ry, 0, ry.ring[0]), 1.7, 0, 1, ry.d0); draw(slice(ry, ry.ring[0], ry.ring[1]), 1.2, ry.ring[0], 1, ry.d0); draw(slice(ry, ry.ring[1], ry.len), 0.8, ry.ring[1], 1, ry.d0);
        [[0.8, 0.5, 0.75], [0.4, 0.3, 0.55]].forEach(([pr, lo, hi]) => { if (Math.random() > pr) return;                        // forks: most rays one, some two
          const t0 = ry.len * rnd(lo, hi), o = at(ry, t0); let a = ry.base + rnd(0.3, 0.5) * (Math.random() < 0.5 ? -1 : 1), q = o; const pts = [o];
          for (let n = 0, L = rnd(18, 55); n * 9 < L; n++) { a += rnd(-0.22, 0.22); const nq = { x: q.x + Math.cos(a) * 9, y: q.y + Math.sin(a) * 9 }; if (!inside(nq)) break; pts.push(nq); q = nq; }
          draw(pts, 0.65, t0, rnd(0.7, 1), ry.d0 + 60); }); });
      RING.forEach((_, j) => rays.forEach((ry, k) => { const nx = rays[(k + 1) % N]; draw([ry.q[j], nx.q[j]], 0.9, Math.max(ry.ring[j], nx.ring[j]), rnd(0.55, 1), Math.max(ry.d0, nx.d0) + 40); }));
      rays.forEach((ry, k) => { if (Math.random() < 0.4) return; const nx = rays[(k + 1) % N], ta = ry.len * 0.74, tb = nx.len * 0.74;   // a third, broken ring
        draw([at(ry, ta), at(nx, tb)], 0.6, Math.max(ta, tb), rnd(0.45, 0.85), Math.max(ry.d0, nx.d0) + 120); });
      rays.forEach((ry, k) => { const nx = rays[(k + 1) % N], m = { x: (ry.q[0].x + nx.q[0].x) / 2, y: (ry.q[0].y + nx.q[0].y) / 2 }, a = Math.atan2(m.y - p.y, m.x - p.x) + rnd(-0.3, 0.3), l = rnd(8, 22);   // hairlines off the inner ring
        draw([m, { x: m.x + Math.cos(a) * l, y: m.y + Math.sin(a) * l }], 0.5, Math.max(ry.ring[0], nx.ring[0]), rnd(0.5, 0.9), Math.max(ry.d0, nx.d0) + 160); });
      for (let n = 0; n < 8; n++) { const a = rnd(0, Math.PI * 2), l = rnd(4, 11); draw([p, { x: p.x + Math.cos(a) * l, y: p.y + Math.sin(a) * l }], 0.6, 0); }   // micro-cracks
      face.appendChild(svg); buzz(HAPTIC.crack);
      const crush = document.createElement("div"); crush.className = "crush"; crush.style.left = p.x + "px"; crush.style.top = p.y + "px"; face.appendChild(crush);
      crush.animate([{ opacity: 0, transform: "scale(0.4)" }, { opacity: 1, transform: "scale(1)" }], { duration: 90, fill: "forwards" });
      const fl = document.createElement("div"); fl.className = "impact"; fl.style.left = p.x + "px"; fl.style.top = p.y + "px"; face.appendChild(fl);
      fl.animate([{ opacity: 0, transform: "scale(0.3)" }, { opacity: 1, transform: "scale(1)", offset: 0.25 }, { opacity: 0, transform: "scale(1.4)" }], { duration: 300, easing: "ease-out", fill: "forwards" });
      tile.animate([{ translate: "0 0", rotate: "0deg" }, { translate: "-4px 0", rotate: "-0.5deg" }, { translate: "3px 0", rotate: "0.4deg" }, { translate: "0 0", rotate: "0deg" }], { duration: 200 });   // translate/rotate, not transform: it shudders ON the raised card instead of undoing its lift
      const crackMs = Math.max(...rays.map(ry => ry.d0 + ry.len / SPEED)) + 160;   // until the last wave has drawn
      // The pieces are built while the learner looks at the cracked glass (invisible), so the instant of breaking only
      // shows and moves them. Measured before: building 33 full-card clones at that instant dropped the fall to 19 fps.
      // Built 6 pieces a frame (measured: all 33 at once froze one frame for 326 ms, visible in the robot's hop).
      let built = null, raf = 0;
      const chunk = () => { built = built || build(); for (let n = 0; n < 6 && built.next < built.cells.length; n++) built.make(built.cells[built.next++]);
        if (built.next < built.cells.length) raf = requestAnimationFrame(chunk); };
      const hold = setTimeout(chunk, crackMs + 60);
      function build() {
        // Pieces: cell j of sector k is bounded by ray k, ring j+1, ray k+1 (back) and ring j, along the drawn cracks.
        const corners = [{ x: 0, y: 0 }, { x: w, y: 0 }, { x: w, y: h }, { x: 0, y: h }].map(c => ({ ...c, a: norm(Math.atan2(c.y - p.y, c.x - p.x)) }));
        const cells = [];
        for (let k = 0; k < N; k++) { const A = rays[k], B = rays[(k + 1) % N], ea = A.pts[A.pts.length - 1], eb = B.pts[B.pts.length - 1];
          const a0 = norm(Math.atan2(ea.y - p.y, ea.x - p.x)), a1 = norm(Math.atan2(eb.y - p.y, eb.x - p.x));
          const between = corners.filter(c => a1 > a0 ? c.a > a0 && c.a < a1 : c.a > a0 || c.a < a1).sort((u, v) => ((u.a - a0 + 2 * Math.PI) % (2 * Math.PI)) - ((v.a - a0 + 2 * Math.PI) % (2 * Math.PI)));
          cells.push({ poly: [...slice(A, 0, A.ring[0]), ...slice(B, 0, B.ring[0]).reverse()], ring: 0 });
          cells.push({ poly: [...slice(A, A.ring[0], A.ring[1]), ...slice(B, B.ring[0], B.ring[1]).reverse()], ring: 1 });
          cells.push({ poly: [...slice(A, A.ring[1], A.len), ...between, ...slice(B, B.ring[1], B.len).reverse()], ring: 2 }); }
        const layer = $("shards"), G = 0.0026, maxD = Math.hypot(w, h) / 2, landings = [], pieces = [], hits = [];
        // the floor the glass lands on: the screen's bottom, or the top of the host's bottom bar when the host marks its row --floor-on: 1
        const AF = $("after"), GROUND = AF && getComputedStyle(AF).getPropertyValue("--floor-on").trim() === "1" ? Math.round(AF.getBoundingClientRect().top) : innerHeight;
        const make = ({ poly, ring }) => {
          // A window the size of the piece, clipped to its shape, holding a full-size copy of the card offset into place.
          const bx = Math.max(0, Math.floor(Math.min(...poly.map(q => q.x))) - 2), by = Math.max(0, Math.floor(Math.min(...poly.map(q => q.y))) - 2);
          const bw = Math.min(w, Math.ceil(Math.max(...poly.map(q => q.x))) + 2) - bx, bh = Math.min(h, Math.ceil(Math.max(...poly.map(q => q.y))) + 2) - by;
          const el = document.createElement("div"); el.className = "shard"; el.dataset.i = tile.dataset.i;   // data-i: a skin can colour a piece like its card
          Object.assign(el.style, { width: bw + "px", height: bh + "px", opacity: "0.01",   /* 1%, not 0: painted in advance (0 is skipped, then all 33 paint in one frame) */
            clipPath: "polygon(" + poly.map(q => (q.x - bx).toFixed(1) + "px " + (q.y - by).toFixed(1) + "px").join(",") + ")" });
          const inner = face.cloneNode(true); inner.removeAttribute("role"); inner.className = "shard-in"; inner.querySelectorAll(".cracks, .crush, .impact, .gleam, .buddy").forEach(g => g.remove());
          Object.assign(inner.style, { left: -bx + "px", top: -by + "px", width: w + "px", height: h + "px", display: "flex", gap: "12px", padding: "16px 16px 16px 14px", visibility: "visible", transform: "none" });
          const edgeSvg = document.createElementNS(NS, "svg"); edgeSvg.setAttribute("class", "edge"); edgeSvg.setAttribute("width", bw); edgeSvg.setAttribute("height", bh);
          const pg = document.createElementNS(NS, "polygon"); pg.setAttribute("points", poly.map(q => (q.x - bx).toFixed(1) + "," + (q.y - by).toFixed(1)).join(" ")); edgeSvg.appendChild(pg);
          el.append(inner, edgeSvg); layer.appendChild(el);
          // How it leaves: from its centre, size (area) and distance from the impact.
          let area = 0; poly.forEach((q, i) => { const n = poly[(i + 1) % poly.length]; area += q.x * n.y - n.x * q.y; }); area = Math.abs(area) / 2;
          const c = poly.reduce((m, q) => ({ x: m.x + q.x / poly.length, y: m.y + q.y / poly.length }), { x: 0, y: 0 }), size = Math.sqrt(area), small = size < 22;
          el.style.transformOrigin = `${(c.x - bx).toFixed(1)}px ${(c.y - by).toFixed(1)}px`;
          el.style.left = (r.left + c.x * k - (c.x - bx)).toFixed(1) + "px"; el.style.top = (r.top + c.y * k - (c.y - by)).toFixed(1) + "px";   // its centre where it sits on the raised card
          const dx = c.x - p.x, dy = c.y - p.y, dd = Math.hypot(dx, dy) || 1, near = 1 - Math.min(1, dd / maxD);
          const speed = (0.05 + near * 0.3) * rnd(0.7, 1.2), delay = (ring * 45 + (1 - near) * 70 + rnd(0, 40));   // inner pieces leave first and fastest
          let x = dx / dd * 2, y = dy / dd * 2, vx = dx / dd * speed + rnd(-0.04, 0.04), vy = dy / dd * speed * 0.5 - rnd(0.05, 0.22);        // the gap opens (2 px), then it flies
          const spin = small ? 1.8 : 0.8; let rx = 0, rz = 0, wx = rnd(0.25, 0.9) * spin * (Math.random() < 0.5 ? -1 : 1), wz = rnd(-0.4, 0.4) * spin;
          let aimX = null;
          if (rb && rb.rain) {   // glassRain: tossed up, then over the whole screen; about 30% aimed at the robot's head (it is hit every time)
            const sx = r.left + c.x * k, fl = GROUND - 6 - (r.top + c.y * k);
            aimX = Math.random() < 0.3 ? rb.cx + rnd(-0.6, 0.6) * rb.halfW : rnd(10, innerWidth - 10);
            vy = -rnd(0.12, 0.34); vx = (aimX - sx) / ((-vy + Math.sqrt(vy * vy + 2 * G * fl)) / G);   // x covered by the time it falls to the floor
          }
          const bin = Math.round((aimX != null ? aimX : r.left + c.x * k + dx / dd * 60) / 34), level = PILE[bin] = Math.min(28, (PILE[bin] || 0) + Math.min(3.2, size * 0.05 + rnd(0.6, 1.4)));
          const floor = GROUND - 6 - level - (r.top + c.y * k), e = small ? 0.34 : 0.16;
          // 2D on purpose: a true rotateX on a clip-path piece is re-rasterised every frame (measured: 17-26 fps vs 57 without the
          // clip). Squashing along its own axis by cos(rx) reads as the same tumble, and lying flat is cos(80°): a flat sliver.
          // Order matters: spin (rotate) first, THEN squash along the screen's vertical, so a resting piece is a flat horizontal
          // sliver however it spun (squashing first then spinning stood pieces up as needles).
          // It starts at the raised card's size (k) and comes back to its true size as it falls away to the floor (~0.5 s).
          const T = () => `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) scale(${(1 + (k - 1) * Math.max(0, 1 - t / 520)).toFixed(3)}) scaleY(${Math.cos(rx * Math.PI / 180).toFixed(3)}) rotate(${rz.toFixed(1)}deg)`;
          const frames = [{ offset: 0, transform: `scale(${k.toFixed(3)})` }]; let t = 0, landed = false, flat = null, rest = 0;
          const sx0 = r.left + c.x * k, sy0 = r.top + c.y * k;   // its start on screen: taken out here, because the step loop's own `k` hid the card's scale (half the steps tested the head at the wrong x)
          while (t < 3000) {                                                                        // 16 ms steps; a keyframe every 32 ms
            for (let k = 0; k < 2; k++) { const y0 = y; t += 16; x += vx * 16; y += vy * 16; vy += G * 16; rx += wx * 16; rz += wz * 16;
              if (rb && rb.rain && ((sx0 + x < 6 && vx < 0) || (sx0 + x > innerWidth - 6 && vx > 0))) vx = -vx * 0.3;   // glassRain: the screen's sides are walls (measured: pieces slid out to -204 / 866 px)
              if (rb && vy > 0) { const u = (sx0 + x - rb.cx) / rb.halfW;                       // its head and shoulders: a curve the glass meets
                if (Math.abs(u) < 1) { const ys = rb.headY + rb.drop * u * u - sy0;
                  if (y >= ys && y0 < ys) { y = ys; vy = -vy * 0.28; vx += (u >= 0 ? 1 : -1) * rnd(0.1, 0.22); wx *= 1.3; hits.push(t + delay); } } }
              if (y >= floor) { y = floor; if (!landed) { landed = true; landings.push({ t: t + delay, x: sx0 + x }); flat = 80 + 180 * Math.round((rx - 80) / 180); }   // the nearest lying-flat angle (80°: flat, but with body; 86° read as a line)
                if (vy > 0.06) { vy = -vy * e; vx *= 0.55; wx *= 0.4; wz *= 0.5; } else { vy = 0; vx *= 0.8; wx *= 0.6; wz *= 0.6; }
                rx += ((flat ?? rx) - rx) * 0.3; }
              if (landed && Math.abs(vy) < 0.001 && Math.abs(vx) < 0.004) rest++; }
            frames.push({ offset: t, transform: T() }); if (rest > 6) break; }
          frames.forEach(f => { f.offset = f.offset / t; });
          pieces.push({ el, frames, t, delay });
        };
        return { pieces, landings, hits, cells, make, next: 0 };
      }
      return wait(Math.max(crackMs + 420, (rb && rb.minHold) || 0)).then(() => {                 // it waits for the robot to arrive under it                                                     // the web finishes spreading; a beat to see it; it gives
        clearTimeout(hold); cancelAnimationFrame(raf); const B = built || build(); while (B.next < B.cells.length) B.make(B.cells[B.next++]);   // finish any not yet built
        face.style.visibility = "hidden"; buzz(HAPTIC.shatter);
        B.pieces.forEach(pc => { pc.el.style.opacity = "1"; pc.el.animate(pc.frames, { duration: pc.t, delay: pc.delay, easing: "linear", fill: "both" }); });
        if (rb && rb.onHit) setTimeout(rb.onHit, B.hits.length ? Math.min(...B.hits) : B.landings.length ? Math.min(...B.landings.map(L => L.t)) : 400);   // the first piece that meets it
        // A few pieces clink where and when they land (not all 33: that would be a rattle, not glass).
        leaveGap(tile); return wait(950);                                                          // the question moves on; the pieces finish on their own
      });
    }
    // The broken card's slot. Two columns: it stays, empty, so the others stay where the learner last saw them. One column
    // (a phone): the cards below slide up into it (FLIP on "translate", which composes with their own transforms).
    function leaveGap(tile, slide = true) {
      tile.style.visibility = "hidden"; tile.style.pointerEvents = "none"; tile.setAttribute("aria-hidden", "true");
      const g = tile.parentElement; if (!g || getComputedStyle(g).gridTemplateColumns.split(" ").length !== 1) return;
      const rest = [...g.children].filter(x => x !== tile && x.style.display !== "none"), before = rest.map(x => x.getBoundingClientRect().top);
      tile.style.display = "none";
      if (!slide || reduced) return;
      rest.forEach((x, k) => { const dy = before[k] - x.getBoundingClientRect().top;
        if (Math.abs(dy) > 0.5) x.animate([{ translate: `0 ${dy.toFixed(1)}px` }, { translate: "0 0" }], { duration: 440, delay: k * 35, easing: "cubic-bezier(.2,.8,.2,1)" }); });
    }
    let PILE = {};                                                                               // floor height per 34 px strip of the screen's bottom edge
    const norm = a => (a + 2 * Math.PI) % (2 * Math.PI), wait = ms => new Promise(r => setTimeout(r, ms));
    function edge(p, a, w, h) { const cx = Math.cos(a), cy = Math.sin(a); let t = Infinity;
      if (cx > 1e-6) t = Math.min(t, (w - p.x) / cx); if (cx < -1e-6) t = Math.min(t, -p.x / cx); if (cy > 1e-6) t = Math.min(t, (h - p.y) / cy); if (cy < -1e-6) t = Math.min(t, -p.y / cy);
      return { x: p.x + cx * t, y: p.y + cy * t }; }

    // Between questions: the table clears (the big card lifts away, the cards sweep off one by one, the question fades up),
    // the progress bar runs on to the next segment, and the next question rises in and deals its cards.
    let leaving = false;
    function next() { if (opts.onNext) return opts.onNext({ from: S.it.n, to: nextN(), sameGroup: sameGroup() }); go(ORDER[(ORDER.indexOf(S.it.n) + 1) % ORDER.length]); }
    function go(n, practice = false) { if (leaving) return; if (reduced || PAGE.classList.contains("sweeping")) return arrive(n, practice); leaving = true;   // faded for the sweep: nothing to clear
      NEXT.classList.remove("show"); if ($("cont")) $("cont").remove(); setHint(null); $("scrim").classList.remove("on");
      const outs = [], hero = $("heroLayer").firstElementChild, flip = x => x.classList.contains("flipped") ? "rotateY(180deg) " : "";
      // Fading a card flattens its 3D (opacity groups it), so backface hiding stops working and the far side would show
      // through mirrored: hide the side facing away first.
      [hero, ...RQA("#mq-tiles .tile")].forEach(x => { if (!x) return; const away = x.querySelector(x.classList.contains("flipped") ? ".face" : ".back"); if (away) away.style.visibility = "hidden"; });
      if (hero) outs.push(hero.animate([{ transform: flip(hero), opacity: 1 }, { transform: flip(hero) + "translateY(-36px) scale(0.9)", opacity: 0 }], { duration: 360, easing: "cubic-bezier(.5,0,.8,.4)", fill: "forwards" }).finished);
      [...RQA("#mq-tiles .tile")].forEach((x, k) => outs.push(x.animate([{ transform: flip(x), opacity: 1 },
        { transform: flip(x) + (opts.slideIn ? "translateX(-110px) rotate(-2deg)" : "translateX(-34px) translateY(-6px) rotate(-2deg)"), opacity: 0 }], { duration: 320, delay: 60 + k * 55, easing: "cubic-bezier(.5,0,.8,.4)", fill: "forwards" }).finished));
      RQA("#mq-stage .qhead, #mq-stage .qdesc, #mq-stage h1, #mq-stage .ab, #mq-stage .qmarks").forEach(x =>
        outs.push(x.animate([{ transform: "none", opacity: 1 }, { transform: opts.slideIn ? "translateX(-80px)" : "translateY(-10px)", opacity: 0 }], { duration: 300, easing: "ease-in", fill: "forwards" }).finished));
      if ($("shards").firstChild && !PAL.el) outs.push($("shards").animate([{ transform: "none", opacity: 1 }, { transform: "translateX(-34px)", opacity: 0 }], { duration: 360, delay: 120, easing: "cubic-bezier(.5,0,.8,.4)", fill: "forwards" }).finished);
      palCleanUp();                                                                                // the robot gets up and sweeps the glass away
      Promise.all(outs).then(() => arrive(n, practice)).catch(() => arrive(n, practice)); }
    function arrive(n, practice = false) { leaving = false; PAGE.classList.remove("sweeping"); if (!PAL.sweeping) { $("shards").replaceChildren(); $("shards").getAnimations().forEach(a => a.cancel()); } PILE = {}; SC.scrollTo({ top: 0 }); const st = $("stage");
      if (opts.slideIn && !reduced) { load(n, practice); slideIn(); return; }
      st.classList.add("enter"); load(n, practice);
      setTimeout(() => st.classList.remove("enter"), 900); }
    // slideIn: the new question comes in from the right, part by part (header, question, then the cards one by one), as
    // the robot sweeps the glass off to the right: two movements crossing. It replaces the rise and the deal from below.
    function slideIn() { RQA("#mq-tiles .tile.dealt").forEach(t => t.classList.remove("dealt"));
      const D = Math.round(Math.min(innerWidth * 0.5, 420)), parts = [...RQA("#mq-stage .qhead, #mq-stage .qdesc, #mq-stage h1, #mq-stage .ab, #mq-stage .qfig"), ...RQA("#mq-tiles .tile"), ...RQA("#mq-stage .qmarks")];
      parts.forEach((x, k) => x.animate([{ transform: `translateX(${D}px)`, opacity: 0 }, { transform: "none", opacity: 1 }], { duration: 560, delay: k * 45, easing: "cubic-bezier(.2,.8,.2,1)", fill: "backwards" })); }
    NEXT.onclick = next;
    $("scrim").onclick = () => tapOut();
    $("heroLayer").addEventListener("click", e => { if (e.target === e.currentTarget) tapOut(); });   // phone: the layer takes taps (it scrolls); its empty area = the scrim
    // The hint: after a miss the robot thinks the clue on its own, in a bubble out of its head, once it is back on its feet in its
    // spot (it was just hit by the glass). It stays while the learner chooses, and goes when they answer.
    function setHint(text) { $("clue").classList.remove("show"); palPoint(false); if (text) $("clueTxt").textContent = text; }
    // pointAtHint: the standing pose (greet_04 held) raises the hand on the screen's left, so it points at a bubble on its
    // left (.sayleft); a bubble on its right gets the robot mirrored (.pointr), for as long as the bubble is up.
    function palPoint(on) { if (opts.pointAtHint) $("pal").classList.toggle("pointr", !!on); }
    // A wrapped box keeps its max width; the cloud should hug the words, so measure the lines and set the width to the longest.
    function fitCloud(el) { el.style.animation = "none"; el.style.width = "";
      const rg = document.createRange(); rg.selectNodeContents(el); const rs = [...rg.getClientRects()];
      // the rects are on-screen (after transforms): the robot is scaled down while it is small, so they are divided back by that scale
      // (measured 2026-10-01 at 375x812: "You got this!" measured 63 px of its 85 and broke onto two lines)
      if (rs.length) { const cs = getComputedStyle(el), pad = cs.boxSizing === "border-box" ? parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight) : 0;
        const k = el.offsetWidth ? el.getBoundingClientRect().width / el.offsetWidth || 1 : 1;
        el.style.width = Math.ceil((Math.max(...rs.map(r => r.right)) - Math.min(...rs.map(r => r.left))) / k + pad + 1) + "px"; }
      void el.offsetWidth; el.style.animation = "";
      // measured in the fallback font while the web font loads, the width is wrong once it lands (seen 2026-10-01: 82 px, three
      // lines, on a first load): measure again when the fonts are in, if it still says the same words
      if (document.fonts && document.fonts.status !== "loaded") { const said = el.textContent; document.fonts.ready.then(() => { if (el.isConnected && el.textContent === said) fitCloud(el); }); } }
    // The robot talks: its words for each clue, first person, to the learner (not a line lifted from a mark scheme). The
    // paper data keeps the plain clues (other pages use them); a clue without its words here is said as written.
    const SAY = {
      "Gibberellins act at the very start of a plant's life.": "Hmm… gibberellins get busy at the very start of a plant's life. When's that?",
      "Think of what a seed does when it breaks dormancy.": "Picture a seed waking up after a long rest. What's it doing?",
      "The pupil got bigger. When does a pupil dilate?": "Look, the pupil got bigger in Y! When do your pupils open wide?",
      "Radial muscles pull the pupil open; circular muscles close it.": "My trick: radial muscles pull the pupil open, circular ones shut it.",
      "Growth hormone is not picky about tissue.": "Growth hormone isn't picky. Would it stop at just one of these?",
      "Bones AND muscles grow.": "Think about growing up: longer bones, and bigger muscles too.",
    };
    function sayIdle(text) { const c = $("clue"); $("clueTxt").textContent = text; c.classList.remove("show"); void c.offsetWidth; c.classList.add("show", "idle"); fitCloud($("clueTxt")); }   // not read out: it is company, not information
    function sayHint(text) { if (!text) return; text = SAY[text] || text; const c = $("clue"); $("clueTxt").textContent = text; c.classList.remove("show", "idle"); void c.offsetWidth; c.classList.add("show"); fitCloud($("clueTxt")); palPoint(!$("pal").classList.contains("sayleft"));
      live("Hint: " + text); }                                                                       // it stands and thinks it (no wave)
    // (heroIn "stage": the card in the panel says it too, and the toast sat on the panel's top border: never over the open card)
    function toast(t, k) { if (k === "ok" && (opts.heroIn === "stage" || innerWidth <= 600 || innerHeight <= 520) && $("heroLayer").querySelector(".tile.hero")) return;   // phone (upright or on its side): no room above the big card, and it already says this
      const e = $("toast"); e.textContent = t; e.className = "toast show " + k; clearTimeout(e._t); e._t = setTimeout(() => e.className = "toast " + k, 1500); }

    const fx = $("fx"), cx = fx.getContext("2d"); let parts = [];
    function size() { fx.width = innerWidth * devicePixelRatio; fx.height = innerHeight * devicePixelRatio; cx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0); } size(); listen(window, "resize", size);
    const BURST = { gold: ["#fbe39a", "#e3b341", "#ffffff", "#dca834"], silver: ["#ffffff", "#cfd4db", "#9aa1ab", "#e8ebef"], bronze: ["#f3bf98", "#bb7a4c", "#ffffff", "#d99b6c"] };
    // A card that fills the panel (heroIn "stage"): the sparks start on its edge and fly OUT, so they never cross its words
    // (measured: from the centre they ran over the medal line and the answer)
    function burst(t, tier) { if (reduced) return; const pal = BURST[tier] || BURST.gold; const r = t.getBoundingClientRect(), ox = r.left + r.width / 2, oy = r.top + r.height / 2, start = !parts.length;
      const rim = opts.heroIn === "stage" && t.classList.contains("hero");
      for (let k = 0; k < 46; k++) { const a = Math.random() * Math.PI * 2, v = 2 + Math.random() * 5;
        if (rim) { const s = Math.random() * 2 * (r.width + r.height), top = s < r.width, right = !top && s < r.width + r.height, bottom = !top && !right && s < 2 * r.width + r.height;
          const x = top ? r.left + s : right ? r.right : bottom ? r.right - (s - r.width - r.height) : r.left, y = top ? r.top : right ? r.top + (s - r.width) : bottom ? r.bottom : r.bottom - (s - 2 * r.width - r.height);
          const nx = right ? 1 : x === r.left && !top && !bottom ? -1 : 0, ny = top ? -1 : bottom ? 1 : 0;
          parts.push({ x, y, vx: nx * v + (Math.random() - 0.5) * 2, vy: ny * v - (ny ? 0 : 1.5) + (Math.random() - 0.5) * 2, life: 1, c: pal[k % 4] }); continue; }
        parts.push({ x: ox, y: oy, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 2, life: 1, c: pal[k % 4] }); }
      if (start) requestAnimationFrame(loop); }
    function loop() { cx.clearRect(0, 0, innerWidth, innerHeight); parts.forEach(p => { p.x += p.vx; p.y += p.vy; p.vy += 0.18; p.life -= 0.018; cx.globalAlpha = Math.max(0, p.life); cx.fillStyle = p.c; cx.fillRect(p.x, p.y, p.sz || 4, p.sz || 4); });
      parts = parts.filter(p => p.life > 0); cx.globalAlpha = 1; if (parts.length) requestAnimationFrame(loop); }
    function fly(t, text, box) { if (text === "+0") return; const r = t.getBoundingClientRect(), to = ((opts.targets || {})[box] || $(box)).getBoundingClientRect(), e = document.createElement("div"); e.className = "fly"; e.textContent = text;
      e.style.left = (r.left + r.width / 2) + "px"; e.style.top = (r.top) + "px"; LAYERS.appendChild(e);
      requestAnimationFrame(() => { e.style.transform = `translate(${to.left - r.left - r.width / 2}px, ${to.top - r.top}px) scale(0.7)`; e.style.opacity = "0.2"; });
      setTimeout(() => e.remove(), 950); }

    palMake();
    load(opts.start || ORDER[0], !!opts.practice);

    // ---- the host's handle ----
    const api = { go: (n, practice) => go(n, practice), get state() { return S; },
      // the glass on the floor, and the sweep as a promise, for a host that moves on only once the robot is home (Exam Practice:
      // Next, then the sweep, then the next question). The question fades meanwhile (.sweeping). A safety net resolves it anyway.
      glass: () => $("shards").children.length,
      cleanUp: () => new Promise(res => { const ps = [...$("shards").children]; if (NOPAL && ps.length && !reduced) { dropAway(ps); setTimeout(res, 640); return; }   // no robot: the pieces sink (420 ms + the last one's 210 ms delay)
        if (!PAL.el || reduced || !$("shards").children.length) { $("shards").replaceChildren(); res(); return; }
        PAGE.classList.add("sweeping"); PAL.onClean = res;   // (the question stays faded until the next one arrives: arrive() lifts it) clearTimeout(PAL.onCleanT); PAL.onCleanT = setTimeout(cleaned, 9000);
        if (PAL.sweeping) return; palCleanUp(); }),
      // for tests and debugging: the engine's own functions and state
      t: { S: () => S, press, go, dismiss, next, submit, $, RQ, RQA, PAL, NEXT, book: () => book, xp: () => xp, sayHint, openMap, closeMap, nextN, sameGroup, leaving: () => leaving, restore },
      destroy() { OFF.forEach(f => f()); try { if (PAL.el) PAL.el.remove(); } catch (x) {} LAYERS.remove(); PAGE.remove(); document.body.classList.remove("mcqp-on"); if (mounted === api) mounted = null; } };
    mounted = api; return api;
  }
  window.McqPlay = { mount };
})();
