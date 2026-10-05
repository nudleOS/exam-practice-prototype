"""Phase 2 of the two-phase validation (A2UI's model: the AI's output is validated against the schema, then by the client).

check(paper)      -> issues: schema errors + semantic checks the schema cannot express (marks add up, indexes in range ...)
review(paper, issues) -> per part: "auto" (goes live after a glance), "check" (a person confirms it) or "blocked" (cannot go live)
to_app(paper, pid, figures) -> the app's paper data (the shape paper-ls-p1-2026.js has), ready to load as window.PAPERS_INGESTED

Usage: python tools/ingest/validate.py tools/ingest/out/<id>/paper.json   (prints the report)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def schema_errors(paper):
    try:
        import jsonschema
    except ImportError:
        return [{"n": "-", "severity": "warn", "msg": "jsonschema not installed: schema check skipped (pip install jsonschema)"}]
    schema = json.loads((HERE / "catalog" / "paper.schema.json").read_text(encoding="utf-8"))
    v = jsonschema.Draft202012Validator(schema)
    return [{"n": "/".join(str(p) for p in e.absolute_path) or "-", "severity": "error", "msg": e.message[:300]}
            for e in sorted(v.iter_errors(paper), key=lambda e: list(e.absolute_path))]


def semantic_issues(paper):
    out = []
    add = lambda n, sev, msg: out.append({"n": n, "severity": sev, "msg": msg})
    seen, total = set(), 0
    for sec in paper.get("sections", []):
        sec_sum = 0
        for m in sec.get("missions", []):
            items = m.get("items", [])
            msum = sum(int(i.get("marks") or 0) for i in items)
            if m.get("marks") is not None and msum != m["marks"]:
                add(m.get("id", "?"), "warn", f"parts add up to {msum}, the question says {m['marks']}")
            sec_sum += msum
            for where, fig in [(m.get("id", "?"), m.get("figure"))] + [(i.get("n", "?"), i.get("figure")) for i in items]:
                b = (fig or {}).get("bbox")
                if fig and (len(b or []) != 4 or not all(0 <= x <= 1 for x in b) or b[0] >= b[2] or b[1] >= b[3]):
                    add(where, "error", f"figure bbox is not 4 fractions x0<x1, y0<y1: {b}")
            for i in items:
                n, t = i.get("n", "?"), i.get("t")
                if n in seen: add(n, "error", "duplicate part number")
                seen.add(n)
                if not i.get("q", "").strip(): add(n, "error", "empty question text")
                if len(i.get("clues") or []) < 2: add(n, "warn", "fewer than 2 hints")
                opts = i.get("opts") or []
                if t == "mcq" and not (0 <= i.get("a", -1) < len(opts)): add(n, "error", f"answer index {i.get('a')} outside {len(opts)} options")
                if t == "pickn" and (len(i.get("pool") or []) < i.get("count", 0) or any(not 0 <= x < len(opts) for x in i.get("pool") or [])):
                    add(n, "error", "pick-N pool does not fit its options or count")
                if t == "order" and sorted(i.get("a") or []) != list(range(len(opts))): add(n, "error", "order is not a permutation of the options")
                if t == "term" and not [a for a in i.get("a") or [] if a.strip()]: add(n, "error", "no accepted answer")
                if t == "list" and len(i.get("pool") or []) < i.get("count", 0): add(n, "error", "fewer memo answers than the count asked")
                if t == "steps" and sum(s.get("marks", 0) for s in i.get("steps") or []) != i.get("marks"): add(n, "warn", "step marks do not add up to the part")
                if t == "rubric":
                    pts = [b for b in i.get("bullets") or [] if not b.startswith("OR")]
                    if len(pts) * (i.get("each") or 1) < i.get("marks", 0): add(n, "warn", "fewer memo points than marks")
                if t == "lettername" and i.get("a", {}).get("letter") not in (i.get("letters") or []): add(n, "error", "answer letter is not one of the letters")
        if sec.get("total") is not None and sec_sum != sec["total"]:
            add(sec.get("title", "?"), "warn", f"section parts add up to {sec_sum}, the paper says {sec['total']}")
        total += sec_sum
    pt = paper.get("paper", {}).get("total_marks")
    if pt is not None and total != pt: add("paper", "warn", f"all parts add up to {total}, the paper says {pt}")
    return out


def check(paper):
    return schema_errors(paper) + semantic_issues(paper)


def review(paper, issues):
    """Every part's review state: what a person must look at before the paper goes live."""
    flags = paper.get("flags", [])
    states = {}
    for sec in paper.get("sections", []):
        for m in sec.get("missions", []):
            for item in m.get("items", []):
                n = item.get("n", "?")
                mine = [x for x in issues if x["n"] in (n, m.get("id"))]
                fl = [f for f in flags if f.get("n") in (n, m.get("id"))]
                states[n] = route(item, mine, fl)
    return states


def route(item, issues, flags):
    # TODO(human): decide each part's review state: "auto", "check" or "blocked".
    return "check"


def to_app(paper, pid, figures):
    """The app's paper data. `figures`: {mission id or "part:" + number: {"src", "w", "h"}} for the crops ingest.py made."""
    meta = paper["paper"]
    secs = []
    for sec in paper["sections"]:
        ms = []
        for m in sec["missions"]:
            items = []
            for i in m["items"]:
                i = dict(i)
                if i["t"] == "draw": i["criteria"] = [[c["text"], c["marks"]] for c in i.get("criteria", [])]
                fig = i.pop("figure", None)   # one question's own figure: the app shows it under the stem (an MCQ card's `img`)
                if fig and "part:" + i["n"] in figures: i["img"] = {**figures["part:" + i["n"]], "alt": fig["caption"]}
                items.append(i)
            mm = {k: m[k] for k in ("id", "title", "kind", "lead", "marks", "extract", "table") if m.get(k) not in (None, "")}
            if m["id"] in figures:
                mm["figure"] = {**figures[m["id"]], "caption": m["figure"]["caption"]}
            mm["items"] = items
            ms.append(mm)
        secs.append({"title": sec["title"], "total": sec["total"], "missions": ms})
    return {"id": pid, "subject": meta["subject"], "title": meta["title"], "sitting": meta["sitting"], "total": meta["total_marks"],
            "time": meta["time"], "catalog": paper["catalog"], "sections": secs}


if __name__ == "__main__":
    p = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    iss = check(p)
    st = review(p, iss)
    for x in iss: print(f"{x['severity']:5} {x['n']:10} {x['msg']}")
    from collections import Counter
    print("parts:", len(st), dict(Counter(st.values())), "| issues:", dict(Counter(x["severity"] for x in iss)), "| flags:", len(p.get("flags", [])))
