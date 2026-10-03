// Paper logic test (run in the page): every Life Sciences part's memo answer must score full marks and a wrong answer must not.
// Usage in DevTools or a JS tool on the Exam Practice page: (await import('/tools/logic-test.js?v=1')).run()
// Reports only failures, plus the counts. Reads the logic instance through the React fiber (the DC runtime keeps it there).
export function logic() {
  const host = document.querySelector(".sc-host");
  const fk = Object.keys(host).find(k => k.startsWith("__reactFiber$"));
  let f = host[fk]; while (f.return) f = f.return;
  const stack = [f];
  while (stack.length) { const n = stack.pop(); if (n.stateNode && n.stateNode.logic) return n.stateNode.logic; if (n.sibling) stack.push(n.sibling); if (n.child) stack.push(n.child); }
  return null;
}
// run() tests Life Sciences P1; run({ data, prefix }) any paper's data (an ingested paper: window.PAPERS_INGESTED[i], prefix its id + ":")
export function run(opts = {}) {
  const L = logic(), P = opts.data || window.PAPER_LS_P1_2026, pre = opts.prefix || "ls:", out = { full: 0, wrongOk: 0, fails: [] };
  const items = {}; P.sections.forEach(s => s.missions.forEach(m => m.items.forEach(q => { items[pre + q.n] = q; })));
  L.missions().forEach(m => m.parts.forEach(part => {
    const q = items[part.key]; if (!q || (q.t === "draw" && !q.build)) return;   // a built drawing is auto-marked: tested too
    const B = q.build, memo = B ? (B.kind === "hist" ? { type: "histogram", cap: "The number of women with MS in different age groups", xl: B.x[0], yl: B.y[0], step: 100, v: B.answers.slice() }
        : Object.fromEntries(B.stems.map(st => [st.id, st.ans]))) : q.t === "mcq" ? q.a : q.t === "pickn" ? q.pool.slice() : q.t === "order" ? q.a.slice() : q.t === "term" ? q.a[0]
      : q.t === "lettername" ? { letter: q.a.letter, name: q.a.name[0] } : q.t === "num" ? String(q.a)
      : q.t === "list" ? q.pool.slice(0, q.count).map(g => Array.isArray(g) ? g[0] : g)
      : q.t === "steps" ? Object.fromEntries(q.steps.map(st => [st.id, String(st.a)]))
      : q.bullets.filter(b => !/^OR\b/.test(b)).join(". ");
    const wrong = B ? (B.kind === "hist" ? { type: "bar", cap: "", v: [0, 0, 0, 0] } : Object.fromEntries(B.stems.map(st => [st.id, "right"]))) : q.t === "mcq" ? (q.a + 1) % q.opts.length : q.t === "pickn" ? [] : q.t === "order" ? q.a.slice().reverse()
      : q.t === "lettername" ? { letter: "Z", name: "banana" } : q.t === "num" ? "12345" : q.t === "list" ? ["banana", "kettle"]
      : q.t === "steps" ? Object.fromEntries(q.steps.map(st => [st.id, "12345"])) : q.t === "term" ? "banana" : "I do not know the answer";
    const r = L.mark(part, memo), w = L.mark(part, wrong);
    if (r.full) out.full++; else out.fails.push(q.n + " memo scored " + r.marks_awarded + "/" + r.marks);
    if (w.full) out.fails.push(q.n + " WRONG answer scored full"); else out.wrongOk++;
    // every accepted spelling of a term passes
    if (q.t === "term") q.a.forEach(t => { if (!L.mark(part, t).full) out.fails.push(q.n + " accepted '" + t + "' failed"); });
  }));
  return out;
}
