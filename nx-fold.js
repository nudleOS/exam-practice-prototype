/* Long question text, condensed (Murci, 2026-10-11: "some questions have a lot of text and take too much space ... learners can still
   view more of the question if they want to"; he picked B + A):
   B. a lead-in over LEAD_MAX words moves into the shared-information sheet, which names its length ("· 63 words"); a sheet over
      CTX_LONG words starts closed on every screen size, so the question is what the learner sees first.
   A. a stem over STEM_MAX words folds: its SETUP is cut to two lines behind "Read more", its ASK (the last sentence or two: "Calculate
      the ...") always shows. Folding the first three lines instead would hide the instruction, which the papers print last. A stem
      whose ask can't be told apart folds whole, to three lines.
   Measured on the 34 papers (2026-10-11): 108 of 581 leads run over 40 words, 37 extracts over 60, 66 of 2143 stems over 45.
   The play screen (Exam Practice.dc.html) and the MCQ panel (mcq-play.js) both read this, so the two fold the same text the same way. */
(function () {
  const LEAD_MAX = 40, CTX_LONG = 60, STEM_MAX = 45;
  const ASK_MAX = 40, SETUP_MIN = 15;
  const words = t => String(t || "").trim().split(/\s+/).filter(Boolean).length;
  // a sentence ends at . ? ! or : before a capital, a digit, a bullet or an opening bracket/quote, or at a line break ("0.5" and
  // "e.g. the" never cut: no space after the point, or a small letter after it)
  const END = /[.?!:]\s+(?=[A-Z0-9(“"‘'•])|\n+/g;
  // the ASK: a sentence that asks (a question mark, an MCQ's trailing "…") or instructs ("Calculate", "Which", "Draw", ...)
  const ASKS = /\?|(?:…|\.\.\.)\s*\)?\s*$|\b(?:calculate|determine|write|which|what|how|why|explain|describe|show|prove|draw|sketch|name|give|state|identify|complete|verify|predict|find|list|tabulate|suggest|define|discuss|evaluate|justify|plot|indicate|express|simplify|solve|estimate|compare|distinguish|mention|convert|derive|construct|deduce|interpret|classify|match|arrange|select|choose)\b/i;
  // ... but not a NOTE after it: the answer's form, a given formula, the picker's own line. A note stays with the ask, never IS it
  // (bench, 2026-10-11: "Area = length × width" and "Write only the letter ..." each hid the real question behind Read more)
  const NOTE = /^(?:choose the correct|write only|write the answer as|show (?:all|your)|give (?:your|the) answer|round|leave your answer|label (?:this|it|the)|take |you may use|use the (?:formula|following)|ignore|assume|note)\b|^[•\-–]|^\([a-z]{1,4}\)\s/i;
  // a given formula ("Area = length × width") is a note; an ask that holds a "=" ("at t = 5 minutes", "prove that TÔP = 2 TK̂P") is not
  const FORMULA = /=/, VERB = /\b(?:calculate|determine|prove|show that|find|solve|which|what|how)\b|\?/i;
  const isNote = s => NOTE.test(s) || (FORMULA.test(s) && !VERB.test(s));
  function split(stem) {
    const t = String(stem || "").trim();
    if (words(t) <= STEM_MAX) return null;
    const cuts = [0];
    let m;
    END.lastIndex = 0;
    while ((m = END.exec(t))) cuts.push(m.index + m[0].length);
    for (let i = cuts.length - 1; i > 0; i--) {   // from the last sentence back: the last one that asks, with every note after it
      const one = t.slice(cuts[i], i + 1 < cuts.length ? cuts[i + 1] : t.length).trim();
      if (!ASKS.test(one) || isNote(one)) continue;
      const setup = t.slice(0, cuts[i]).trim();
      if (words(one) <= ASK_MAX && words(setup) >= SETUP_MIN) return { setup: setup, ask: t.slice(cuts[i]).trim() };
      break;
    }
    return { setup: t, ask: "" };   // no ask to keep apart: the whole stem folds
  }
  window.NXFold = { LEAD_MAX: LEAD_MAX, CTX_LONG: CTX_LONG, STEM_MAX: STEM_MAX, words: words, split: split,
    leadLong: lead => words(lead) > LEAD_MAX, ctxLong: text => words(text) > CTX_LONG };
})();
