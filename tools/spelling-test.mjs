// The term marker's "is this a slip or a different answer" rule (meaningSlip), tested on the cases the coverage audit found.
// Run: node tools/spelling-test.mjs   (reads the rule straight from Exam Practice.dc.html, so it tests the shipped code)
import fs from "node:fs";
const src = fs.readFileSync(new URL("../Exam Practice.dc.html", import.meta.url), "utf8");
const code = src.slice(src.indexOf("const MEANING_PREFIX"), src.indexOf("const lev = "));
const meaningSlip = new Function(code + "; return meaningSlip;")();
const cases = [   // [typed, memo answer, is it a change of meaning?]
  ["complete dominance", "incomplete dominance", true], ["prophase ii", "prophase i", true], ["prophase i", "prophase ii", true],
  ["prophase", "prophase i", true], ["meiosis 2", "meiosis 1", true], ["nonpolar", "polar", true], ["hypotonic", "hypertonic", false],
  ["grafian follicle", "graafian follicle", false], ["peripherel nervous system", "peripheral nervous system", false],
  ["hypothalamas", "hypothalamus", false], ["cerebelum", "cerebellum", false]];
// (hypotonic / hypertonic: distance 3, beyond the slip allowance anyway; the rule itself only sees a prefix ADDED to the same word)
let bad = 0;
for (const [t, a, want] of cases) { const got = meaningSlip(t, a); if (got !== want) bad++; console.log((got === want ? "ok   " : "FAIL ") + JSON.stringify(t) + " vs " + JSON.stringify(a) + " -> " + got); }
console.log(bad ? bad + " FAILED" : "all " + cases.length + " pass"); process.exit(bad ? 1 : 0);
