"""The lead rule's two halves agree: the prototype's leadHit / leadKey (Exam Practice.dc.html, between `// <lead-rule>` and
`// </lead-rule>`, extracted and run with node) and validate.py's copy run the exam service's own cases
(nexera-exam-service/tests/fixtures/list_lead_cases.json). It also runs the OLD rule (the first word as a substring) on the
same cases, to show what changed.

  python tools/ingest/check_lead_rule.py [path/to/list_lead_cases.json]
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import validate  # noqa: E402

CASES = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[3] / "nexera-exam-service" / "tests" / "fixtures" / "list_lead_cases.json"
cases = json.loads(CASES.read_text(encoding="utf-8"))
html = (HERE.parent.parent / "Exam Practice.dc.html").read_text(encoding="utf-8")
block = "//" + html.split("// <lead-rule>", 1)[1].split("// </lead-rule>", 1)[0]   # (the marker line's own comment)
js = block + """
const norm = s => String(s).normalize("NFKD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
const old = (line, entries) => { const n = norm(line); return !!n && entries.some(e => { const t = norm(e); return n === t || n.indexOf(t.split(" ")[0]) !== -1; }); };
const c = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
console.log(JSON.stringify({ matches: c.matches.map(([e, l]) => [leadHit(l, e), old(l, e)]), keys: c.keys.map(([e]) => leadKey(e)) }));
"""
got = json.loads(subprocess.run(["node", "-e", js, str(CASES)], capture_output=True, text=True, encoding="utf-8", check=True).stdout)
bad, old_bad = [], []
for (entries, line, want), (js_hit, old_hit) in zip(cases["matches"], got["matches"], strict=True):
    py_hit = validate.lead_hit(line, entries)
    if js_hit != want or py_hit != want:
        bad.append(f"{line!r}: want {want}, prototype {js_hit}, validate.py {py_hit}")
    if old_hit != want:
        old_bad.append(f"{line!r}: the old rule said {old_hit}")
for (entry, want), js_key in zip(cases["keys"], got["keys"], strict=True):
    if js_key != want or list(validate.lead_key(entry)) != want:
        bad.append(f"key of {entry!r}: want {want}, prototype {js_key}, validate.py {list(validate.lead_key(entry))}")
print(f"{len(cases['matches'])} lines, {len(cases['keys'])} keys: " + ("both halves agree with the service" if not bad else f"{len(bad)} DISAGREE"))
for b in bad:
    print("  ", b)
print(f"the old substring rule got {len(old_bad)} wrong:")
for b in old_bad:
    print("  ", b)
sys.exit(1 if bad else 0)
