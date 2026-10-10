"""Phase 2 of the two-phase validation (A2UI's model: the AI's output is validated against the schema, then by the client).

check(paper)      -> issues: schema errors + semantic checks the schema cannot express (marks add up, indexes in range ...)
review(paper, issues) -> per part: "auto" (goes live after a glance), "check" (a person confirms it) or "blocked" (cannot go live)
to_app(paper, pid, figures) -> the app's paper data (the shape paper-ls-p1-2026.js has), ready to load as window.PAPERS_INGESTED

Usage: python tools/ingest/validate.py tools/ingest/out/<id>/paper.json   (prints the report)
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

# a memo marking NOTE, not a point: key words / phrases, criteria, an ACCEPT limit, "Mark the first TWO only", "Do NOT accept ...",
# "No marks for ...", "Facts are capped at 32 ...", "not necessarily a table ...", "X defined: 0/2", "deduct 1" (these belong
# in a rubric's `notes`, which is never scored)
NOTE_RE = re.compile(r"^(OR\s*[—-]\s*)?(Key (words?|phrases?)|Criteria|ACCEPT \(max|Mark the first|Do NOT accept|No marks for|Do not award|Facts are capped|(The answer )?(need not|not necessarily) be a table|Not necessarily a table)|:\s*0/\d|\bdeduct \d", re.I)


def schema_errors(paper):
    try:
        import jsonschema
    except ImportError:
        return [{"n": "-", "severity": "warn", "msg": "jsonschema not installed: schema check skipped (pip install jsonschema)"}]
    schema = json.loads((HERE / "catalog" / "paper.schema.json").read_text(encoding="utf-8"))
    v = jsonschema.Draft202012Validator(schema)
    return [{"n": "/".join(str(p) for p in e.absolute_path) or "-", "severity": "error", "msg": e.message[:300]}
            for e in sorted(v.iter_errors(paper), key=lambda e: list(e.absolute_path))]


# the LEAD rule for a list pool: the exam service's papers/domain/list_keys.py, character for character (and the app's
# leadHit); tools/ingest/check_lead_rule.py runs all three on the service's cases. An entry's key: its words before any "("
# up to and including the first word not a stop word; a line names it when the key's words stand together in it, each
# starting a word, a number exactly.
LEAD_STOP = frozenset("the a an same no not many all one two three four five until of in on at to for by with and or is are was were be its their there".split())


def lead_words(text):
    import unicodedata
    t = "".join(c for c in unicodedata.normalize("NFKD", str(text or "")) if not unicodedata.combining(c)).lower()
    return [w for w in re.split(r"[^a-z0-9]+", t.replace("'", "").replace("’", "")) if w]


def lead_key(entry):
    ws = lead_words(str(entry).split("(")[0])
    for i, w in enumerate(ws[:3]):
        if w not in LEAD_STOP:
            return tuple(ws[: i + 1])
    return tuple(ws[:3])


def lead_hit(line, entries):
    a = lead_words(line)
    hit = lambda x, k: x == k if k.isdigit() else x.startswith(k)
    return any(k and any(all(hit(a[i + j], k[j]) for j in range(len(k))) for i in range(len(a) - len(k) + 1))
               for k in (lead_key(e) for e in entries))


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
                if t == "mcq" and i.get("ab") and [o.strip().lower() for o in opts] != ["a only", "b only", "both a and b", "none"]:
                    add(n, "error", "a COLUMN II pair (ab) needs the options A only, B only, Both A and B, None, in that order")
                if t == "pickn" and (len(i.get("pool") or []) < i.get("count", 0) or any(not 0 <= x < len(opts) for x in i.get("pool") or [])):
                    add(n, "error", "pick-N pool does not fit its options or count")
                if t == "order" and sorted(i.get("a") or []) != list(range(len(opts))): add(n, "error", "order is not a permutation of the options")
                if t == "match":
                    left, right, a = i.get("left") or [], i.get("right") or [], i.get("a") or []
                    if len(a) != len(left) or any(not 0 <= x < len(right) for x in a): add(n, "error", "a match needs one right index per left item")
                    if len(left) * (i.get("each") or 1) != i.get("marks"): add(n, "error", "a match's marks are its pairs times each")
                    if not i.get("groups") and len(set(a)) != len(a): add(n, "error", "a one-to-one match uses a right item twice (classifying? set groups)")
                    if i.get("heads") is not None and len(i["heads"]) != 2: add(n, "error", "a match's heads are two titles")
                if t == "term" and not [a for a in i.get("a") or [] if a.strip()]: add(n, "error", "no accepted answer")
                if t == "list" and len(i.get("pool") or []) < i.get("count", 0): add(n, "error", "fewer memo answers than the count asked")
                if t == "list":   # a key of stop words only ("the same") would credit almost any line
                    weak = [e for g in i.get("pool") or [] for e in (g if isinstance(g, list) else [g]) if all(w in LEAD_STOP for w in lead_key(e))]
                    if weak: add(n, "error", f"list entries with no lead word: {weak}")
                if t == "steps" and sum(s.get("marks", 0) for s in i.get("steps") or []) != i.get("marks"): add(n, "warn", "step marks do not add up to the part")
                if t == "steps":   # a label is on screen during play: it names the quantity, never the working the memo marks
                    stps = i.get("steps") or []
                    keys = {float(s["a"]) for s in stps if isinstance(s.get("a"), (int, float))}
                    for s in stps:
                        lab = s.get("label", "")
                        nums = {float(x.replace(" ", "").replace(",", ".")) for x in re.findall(r"\d+(?:[ ,.]\d+)*", lab)}
                        if re.search(r"\d\s*[×÷−+=*/x]\s*[\d(]", lab) or nums & keys:
                            add(n, "error", f"step {s.get('id')}'s label prints the working or an answer: {lab!r}")
                if t == "rubric":
                    bl, must, worth = i.get("bullets") or [], i.get("must") or [], i.get("worth")
                    if worth is not None and len(worth) != len(bl): add(n, "error", f"worth has {len(worth)} marks for {len(bl)} points")
                    pw = (lambda k: worth[k]) if worth is not None and len(worth) == len(bl) else (lambda k: i.get("each") or 1)
                    if sum(pw(k) for k, b in enumerate(bl) if not b.startswith("OR")) < i.get("marks", 0): add(n, "warn", "fewer memo points than marks")
                    if any(not 0 <= k < len(bl) or bl[k].startswith("OR") for k in must): add(n, "error", "a compulsory point is not one of the memo points")
                    if must and len(must) * (i.get("each") or 1) >= i.get("marks", 0): add(n, "warn", "compulsory points leave no marks for the rest")
                if t == "lettername" and i.get("a", {}).get("letter") not in (i.get("letters") or []): add(n, "error", "answer letter is not one of the letters")
                if t == "lettername" and any(p.get("letter") not in (i.get("letters") or []) for p in i.get("or") or []): add(n, "error", "an alternative letter is not one of the letters")
                if t == "letternames":
                    pool = i.get("pool") or []
                    if len(pool) < i.get("count", 0): add(n, "error", "fewer memo parts than the count asked")
                    if any(p.get("letter") not in (i.get("letters") or []) for p in pool): add(n, "error", "a memo letter is not one of the letters")
                    if i.get("marks") != 2 * i.get("count", 0): add(n, "warn", "a letter + name is 2 marks per part: marks are not 2 x count")
                if t == "rubric":   # a memo NOTE in bullets is a point a learner earns ("Threshold frequency defined: 0/2" scored, 2026-10-10)
                    notey = [b for b in i.get("bullets") or [] if NOTE_RE.search(b)]
                    if notey: add(n, "warn", "a marking note in bullets, which a learner would earn: move it to notes: " + notey[0][:60])
                if t == "genotype":
                    al, pool = i.get("alleles") or [], i.get("pool") or []
                    if len(pool) < i.get("count", 0): add(n, "error", "fewer memo genotypes than the count asked")
                    per = 4 if i.get("per") == 4 else 2   # a dihybrid's genotype is four alleles (RRee)
                    if any(len(g) != per or any(x not in al for x in g) for g in pool): add(n, "error", f"a memo genotype is not {per} of the alleles")
                    if i.get("count") and (i.get("marks") or 0) % i["count"]: add(n, "warn", "marks do not split evenly over the genotypes")
                b = i.get("build") or {}
                if t == "draw" and b.get("kind") == "cross":   # everything the marker derives must exist: each parent, each offspring's phenotype
                    al, ph, par = b.get("alleles") or [], b.get("phenos") or [], b.get("parents") or []
                    gt = lambda g: "|".join(sorted(g))
                    key = {gt(o.get("geno") or []): o.get("pheno") for o in b.get("offspring") or []}
                    if len(par) != 2 or any(len(p.get("geno") or []) != 2 or any(x not in al for x in p["geno"]) or p.get("pheno") not in ph for p in par):
                        add(n, "error", "a cross needs two parents, each a phenotype from phenos and two of the alleles")
                    elif any(key.get(gt([x, y])) not in ph for x in par[0]["geno"] for y in par[1]["geno"]):
                        add(n, "error", "an offspring genotype of this cross has no phenotype in offspring (or one not in phenos)")
                    elif any(key.get(gt(p["geno"])) != p["pheno"] for p in par): add(n, "error", "a parent's phenotype disagrees with offspring's for its genotype")
                    if i.get("marks") and len(i.get("criteria") or []) <= i["marks"] - 1: add(n, "warn", "a cross's criteria: the memo's points (usually 8 for 6 marks)")
                tb = i.get("optTable")
                if t == "mcq" and tb and (len(tb.get("rows") or []) != len(opts) or any(len(r) != len(tb.get("head") or []) for r in tb.get("rows") or [])):
                    add(n, "error", "the options table needs one row per option and one cell per column")
        anyn = sec.get("answer_any")
        if anyn:   # "Answer any N": every question carries the same marks, and the section counts N of them
            qs = {}
            for m in sec.get("missions", []):
                qn = str(m.get("id", "?")).split(".")[0]
                qs[qn] = qs.get(qn, 0) + sum(int(i.get("marks") or 0) for i in m.get("items", []))
            if not 0 < anyn < len(qs): add(sec.get("title", "?"), "error", f"answer any {anyn} of {len(qs)} questions")
            if len(set(qs.values())) > 1: add(sec.get("title", "?"), "error", f"the questions to choose from carry different marks: {qs}")
            sec_sum = anyn * max(qs.values() or [0])
        if sec.get("total") is not None and sec_sum != sec["total"]:
            add(sec.get("title", "?"), "warn", f"section parts add up to {sec_sum}, the paper says {sec['total']}")
        total += sec_sum
    pt = paper.get("paper", {}).get("total_marks")
    if pt is not None and total != pt: add("paper", "warn", f"all parts add up to {total}, the paper says {pt}")
    # options WE write (a printed paper's own A-D keep their order) must not all put the answer in one place: Maths P2's six
    # were all A on 2026-10-08, so a learner who spotted it scored without reading
    at = [i.get("a") for sec in paper.get("sections", []) for m in sec.get("missions", []) for i in m.get("items", []) if i.get("t") == "mcq"]
    if len(at) >= 4 and len(set(at)) == 1:
        add("paper", "warn", f"every multiple-choice answer is option {at[0] + 1} of its list: vary where the answer sits")
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
        secs.append({"title": sec["title"], "total": sec["total"], "missions": ms, **({"answer_any": sec["answer_any"]} if sec.get("answer_any") else {})})
    return {"id": pid, "subject": meta["subject"], "title": meta["title"], "sitting": meta["sitting"], "total": meta["total_marks"],
            "time": meta["time"], "catalog": paper["catalog"], "sections": secs}


if __name__ == "__main__":
    p = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    iss = check(p)
    st = review(p, iss)
    for x in iss: print(f"{x['severity']:5} {x['n']:10} {x['msg']}")
    from collections import Counter
    print("parts:", len(st), dict(Counter(st.values())), "| issues:", dict(Counter(x["severity"] for x in iss)), "| flags:", len(p.get("flags", [])))
