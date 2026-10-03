"""A test fixture with no API call: Life Sciences P1's hand-checked data, rewritten in the catalogue format, as if Claude had
produced it. Running `ingest.py --from-json` on it proves the back half (validate -> crop -> app data -> the app renders and marks)
on a paper whose right answers we already trust (the logic test, 85/85).

  python tools/ingest/fixture_from_ls_p1.py
  python tools/ingest/ingest.py "uploads/Life Sciences P1 May-June 2026 Eng.pdf" "uploads/Life Sciences P1 May-June 2026 MG Eng.pdf" --id ls-p1-fixture --from-json
"""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
KEEP = {"mcq": ["opts", "a"], "pickn": ["opts", "pool", "count"], "order": ["opts", "a"], "term": ["a", "reject"], "list": ["count", "pool"],
        "lettername": ["letters", "a"], "num": ["a", "tol", "unit"], "steps": ["steps"], "rubric": ["bullets", "each"], "draw": ["criteria", "memo"]}
# where 3.6's diagram sits on page 18 (fractions of the page, measured on the 1000x1415 page image): exercises the cropper
FIGURE = {"3.6": {"page": 18, "bbox": [0.228, 0.36, 0.822, 0.62], "caption": "Three plants in a cardboard box, light from the left: A untreated, B with a black cap, C with its tip removed."}}


def main():
    src = json.loads(subprocess.run(["node", "-e", "global.window={};require('./paper-ls-p1-2026.js');console.log(JSON.stringify(window.PAPER_LS_P1_2026))"],
                                    cwd=ROOT, capture_output=True, encoding="utf-8", check=True).stdout)   # (utf-8: Windows decodes with its code page, "…" became "â€¦")
    flags, secs = [], []
    for sec in src["sections"]:
        ms = []
        for m in sec["missions"]:
            items = []
            for q in m["items"]:
                t = q["t"]
                if t == "draw":   # the catalogue has no builders: a drawing is a self-check, flagged
                    flags.append({"n": q["n"], "kind": "no_fit", "detail": "a drawing: answered on paper, self-checked"})
                it = {"t": t, "n": q["n"], "marks": q["marks"], "q": q["q"], "clues": q.get("clues") or []}
                if q.get("note"): it["note"] = q["note"]
                for k in KEEP[t]:
                    if k in q: it[k] = q[k]
                if t == "num" and "tol" not in it: it["tol"] = 0.001   # the app's silent default, made explicit (the catalogue requires it)
                if t == "draw": it["criteria"] = [{"text": c[0], "marks": c[1]} for c in q.get("criteria", [])]
                if t == "steps": it["steps"] = [{k: st[k] for k in ("id", "label", "marks", "a", "tol", "memo")} for st in q["steps"]]   # (no ft: functions are not data)
                items.append(it)
            mm = {k: m[k] for k in ("id", "title", "kind", "lead", "marks", "extract", "table") if m.get(k) not in (None, "")}
            if m["id"] in FIGURE: mm["figure"] = FIGURE[m["id"]]
            mm["items"] = items
            ms.append(mm)
        secs.append({"title": sec["title"], "total": sec.get("total") or sum(x["marks"] for x in ms), "missions": ms})
    paper = {"catalog": "https://nexera.app/catalogs/exam/v1",
             "paper": {"subject": "Life Sciences", "title": "Life Sciences P1 (fixture)", "sitting": "May/June 2026", "total_marks": 150, "time": "2½ hours"},
             "sections": secs, "flags": flags}
    out = HERE / "out" / "ls-p1-fixture"; out.mkdir(parents=True, exist_ok=True)
    (out / "response.json").write_text(json.dumps({"meta": {"fixture": "from paper-ls-p1-2026.js"}, "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
    print("fixture:", sum(len(m["items"]) for s in secs for m in s["missions"]), "parts ->", out / "response.json")


if __name__ == "__main__":
    main()
