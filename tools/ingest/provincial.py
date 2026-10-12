"""Shared helpers for the provincial Grade 10 and 11 transcriptions (2026-10-12): the part makers, the whole-working
multiple choice with its right option PLACED by a fixed sequence (not chosen by hand), and the checks every transcription
ran at its end (marks per mission and per question, the paper's total, the spread of the right letter, the "after" gates,
built sketches, Venn diagrams and trees), then response.json. Where each paper came from: PROVENANCE-g10-g11.md.

The rulings are the Grade 12 ones (2026-10-10, 2026-10-11), as in transcribe_g11_math_p1_2017_11.py:
  - a value the memo WORKS OUT in two or more lines -> `work`: the memo's FIRST method line by line and three workings
    each built from a DIFFERENT real error, every option the same layout; never a form the memo also accepts, never a memo
    slip's reading; 0 or full marks;
  - an answer the memo states with no working -> `answer`: the memo's and three common errors;
  - one number with no working -> `num`;
  - a sketch -> `draw` with build "sketch"; a drawing no builder makes -> pick the drawing (pictures.py).
`work` and `answer` take the RIGHT option FIRST; the sequence below moves it to its letter, so the letters are spread over
A-D across the paper without anyone choosing them."""
import json
import re
from pathlib import Path

ANSWER = "\n\nChoose the correct answer."
WORK = "\n\nChoose the correct working."
#: blocks of the four letters, each a permutation, walked in order: every 4 parts in a row use each letter once
BLOCKS = ["BDAC", "CADB", "DBCA", "ACBD", "CBDA", "DACB", "ADBC", "BCAD", "DCAB", "ABDC", "CDBA", "BACD"]


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


class Paper:
    def __init__(self, pid, w, h, figs, start=0):
        self.pid, self.W, self.H, self.FIGS = pid, w, h, figs
        self.seq = "".join(BLOCKS[(start + i) % len(BLOCKS)] for i in range(40))
        self.k = 0
        self.authored, self.answers = [], []

    # ---- figures and parts
    def fig(self, name, caption):
        p, x0, y0, x1, y1 = self.FIGS[name]
        return {"page": p, "bbox": [round(x0 / self.W, 4), round(y0 / self.H, 4), round(x1 / self.W, 4), round(y1 / self.H, 4)],
                "caption": caption}

    def _place(self, opts):
        at = "ABCD".index(self.seq[self.k])
        self.k += 1
        out = list(opts[1:])
        out.insert(at, opts[0])
        return out, at

    def work(self, n, q, marks, opts, clues, **kw):
        """opts: the memo's working FIRST, then three workings from real errors; one step a line, {a}/{b} a stacked fraction."""
        assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
        assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
        self.authored.append(n)
        o, a = self._place(opts)
        return {"t": "mcq", "n": n, "marks": marks, "q": q + WORK, "clues": clues, "opts": o, "a": a, **kw}

    def answer(self, n, q, marks, opts, clues, **kw):
        """opts: the memo's answer FIRST, then three common errors."""
        assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
        self.answers.append(n)
        o, a = self._place(opts)
        return {"t": "mcq", "n": n, "marks": marks, "q": q + ANSWER, "clues": clues, "opts": o, "a": a, **kw}

    @staticmethod
    def mcq(n, q, opts, a, clues, marks=2, **kw):
        """Multiple choice PRINTED in the paper (or a choice printed in the stem): its options and right letter as printed."""
        return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}

    @staticmethod
    def term(n, q, a, clues, marks=1, **kw):
        """One term the memo names: a, the accepted words."""
        return {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, **kw}

    def stmt(self, n, q, marks, right, wrong, clues, each, **kw):
        """A written answer as statements: the memo's points (right) and clearly false cards (wrong), shuffled with a fixed seed;
        the learner picks marks/each of them, any right one counts, each right pick earns `each`."""
        import random
        count = marks // each
        assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
        assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
        for salt in range(50):   # the first seed that puts no single right card first and not all right cards on top
            order = list(range(len(right) + len(wrong)))
            random.Random(self.pid + ":" + n + ("" if not salt else ":%d" % salt)).shuffle(order)
            pool = sorted(k for k, i in enumerate(order) if i < len(right))
            if (count > 1 or pool[0] != 0) and pool != list(range(len(pool))):
                break
        opts = [(right + wrong)[i] for i in order]
        return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count, **kw}

    @staticmethod
    def num(n, q, a, tol, unit, clues, marks=1, **kw):
        return {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit, **kw}

    @staticmethod
    def draw(n, q, marks, criteria, clues, memo="", **kw):
        return {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues, "criteria": [{"text": t, "marks": m} for t, m in criteria],
                **({"memo": memo} if memo else {}), **kw}

    # ---- the checks, then response.json
    def finish(self, missions, meta, flags, qtotal, total, after, scope):
        items = [i for m in missions for i in m["items"]]
        per_q = {}
        for m in missions:
            got = sum(i["marks"] for i in m["items"])
            assert got == m["marks"], (m["id"], got, m["marks"])
            q = m["id"].split(".")[0]
            per_q[q] = per_q.get(q, 0) + got
            print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
        assert per_q == qtotal, per_q
        assert sum(i["marks"] for i in items) == total, sum(i["marks"] for i in items)
        assert len({i["n"] for i in items}) == len(items), "a part number twice"
        for i in items:
            b = i.get("build") or {}
            if b.get("kind") == "sketch":
                sketch_ok(i)
            if b.get("kind") == "venn":
                venn_ok(i)
            if b.get("kind") == "tree":
                tree_ok(i)
            assert i["t"] != "mcq" or len(i["opts"]) == 4 or i["n"] not in self.authored + self.answers, i["n"]   # printed choices may be 3
            # a working line ending in "[...]" draws its bracket as a proof's REASON column (platform workings.ts workLines): a
            # concentration "[H₃O⁺]" or "[OH⁻]" at a line's end would be drawn as one
            for o in (i.get("opts") or []) if i["t"] == "mcq" else []:
                if "\n" in o:
                    for ln in o.split("\n"):
                        m = re.search(r"\[([^\[\]]+)\]\s*$", ln)
                        assert not (m and re.search(r"[⁺⁻]|^H|^OH", m.group(1))), (i["n"], "a concentration read as a reason", ln)
        at = ["ABCD"[i["a"]] for i in items if i["t"] == "mcq" and i["n"] in self.authored + self.answers]
        spread = {k: at.count(k) for k in "ABCD"}
        assert max(spread.values()) - min(spread.values()) <= 1, spread
        worked = {k: ["ABCD"[i["a"]] for i in items if i["n"] in self.authored].count(k) for k in "ABCD"}
        print("right letters:", spread, "workings:", worked, "| workings", len(self.authored), "answers", len(self.answers))
        got_after = {i["n"]: i["after"] for i in items if i.get("after")}
        assert got_after == after, got_after
        paper = {"catalog": "https://nexera.app/catalogs/exam/v1", "paper": meta,
                 "sections": [{"title": meta["subject"], "total": total, "missions": missions}], "flags": flags}
        out = Path(__file__).parent / "out" / self.pid   # written only once every check above has passed
        out.mkdir(parents=True, exist_ok=True)
        (out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and the memo (no API call)",
                                                                 "scope": scope}, "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
        print("total:", total, "->", out / "response.json")

    def flag_workings(self, extra=""):
        return {"n": self.authored[0], "kind": "no_fit",
                "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more lines plays as four "
                          "workings, the memo's FIRST method line by line and three built from real errors, one step a line, 0 or full "
                          "marks: " + ", ".join(self.authored) + "." + (" " + extra if extra else "")}

    def flag_answers(self, extra=""):
        return {"n": self.answers[0], "kind": "no_fit",
                "detail": "Authored multiple choice, answers: " + ", ".join(self.answers) + " ask for an answer the memo states with no "
                          "working that a word marker cannot read: four options, the memo's answer and three common errors, 0 or full "
                          "marks." + (" " + extra if extra else "")}


def sketch_ok(i):
    """A built sketch: its features' and shapes' marks are the memo criteria's, criterion by criterion."""
    b = i["build"]
    got = {}
    for x in b["features"] + [g["shape"] for g in b.get("graphs", []) if g.get("shape")] + ([b["shape"]] if b.get("shape") else []):
        got[x["crit"]] = got.get(x["crit"], 0) + x["marks"]
    assert got == {k: c["marks"] for k, c in enumerate(i["criteria"])}, (i["n"], got)
    assert not b.get("graphs") or all(f.get("graph") in {g["id"] for g in b["graphs"]} for f in b["features"]), i["n"]


def venn_ok(i):
    b = i["build"]
    ids = [s["id"] for s in b["sets"]]
    want = ([ids[0], ids[0] + ids[1], ids[1]] if len(ids) == 2 else
            [ids[0], ids[1], ids[2], ids[0] + ids[1], ids[0] + ids[2], ids[1] + ids[2], "".join(ids)]) + (["out"] if b["outside"] else [])
    assert sorted(g["in"] for g in b["regions"]) == sorted(want), (i["n"], "regions")
    assert sorted({g["crit"] for g in b["regions"] if "crit" in g}) == list(range(len(i["criteria"]))), (i["n"], "every criterion a region")
    x = b.get("unknown", "x")
    for g in b["regions"]:
        s = re.sub(r"\s+", "", str(g["at"])).replace("−", "-")
        assert re.fullmatch(r"\d+|%s|%s[+-]\d+|\d+[+-]%s" % (x, x, x), s), (i["n"], g)


def tree_ok(i):
    b = i["build"]
    ids = [x["id"] for x in b["outcomes"]]
    val = lambda p: (lambda t: float(t[0]) / float(t[1]) if len(t) == 2 else float(t[0]))(p.replace(",", ".").split("/"))
    for kids in [b["tree"]] + [t["next"] for t in b["tree"]]:
        assert all(t["id"] in ids for t in kids) and len({t["id"] for t in kids}) == len(kids), (i["n"], "outcomes")
        assert abs(sum(val(t["p"]) for t in kids) - 1) < 1e-9, (i["n"], "a point's branches add up to 1")
    named = set(b["crit"].values()) | {t["crit"] for t in b["tree"] + [u for t in b["tree"] for u in t["next"]] if "crit" in t}
    assert sorted(named) == list(range(len(i["criteria"]))), (i["n"], "every criterion earned by a component")
