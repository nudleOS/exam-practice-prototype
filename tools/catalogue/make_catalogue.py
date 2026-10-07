"""Writes papers-catalogue.js: a MOCK of the exam service's paper list (GET /v1/papers) for rollout 1's Grade 12 November
papers (six subjects, P1 + P2, 2025 + 2024). Every fact comes from the paper itself:
  time  = the cover's "TIME:" line (text papers read by script; the 8 scanned maths covers read by eye 2026-10-02: 3 hours)
  marks = the cover's total (a ready paper played in part: the marks it plays, the cover's kept as printed_marks);
          questions / missions = the question paper's mark map (pairs/<QP>.json, checked against the memo's
          by compare_pairs.py on 2026-10-02; the memo maps hold answers and stay out of git)

A paper in FINISHED is transcribed and validated (tools/ingest/out/<id>/paper.js): it is "ready", the page loads it with the
app, and its question paper is its source_pdf (so the question pages show the view-paper button; tools/catalogue/make_pages.py
renders its page images). Every other paper is "preparing".

  python tools/catalogue/make_catalogue.py      (then python tools/catalogue/make_pages.py)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAIRS = os.path.join(HERE, "pairs")
OUT = os.path.join(ROOT, "papers-catalogue.js")
SUBJECTS = ["Business Studies", "Geography", "Life Sciences", "Mathematical Literacy", "Mathematics", "Physical Sciences"]
MINUTES = {"Business Studies": 120, "Geography": 180, "Life Sciences": 150, "Mathematical Literacy": 180, "Mathematics": 180, "Physical Sciences": 180}
SLUG = {"Business Studies": "bs", "Geography": "geo", "Life Sciences": "ls", "Mathematical Literacy": "ml", "Mathematics": "math", "Physical Sciences": "ps"}

# id -> its question paper and memo, as named in the papers folder (make_pages.py copies them into uploads/). Add a paper here
# when tools/ingest has produced it and validate.py passes.
FINISHED = {
    "ls-p1-2025-11": ("Life Sciences P1 Nov 2025 Eng.pdf", "Life Sciences P1 Nov 2025 MG Eng.pdf"),
    "ls-p2-2025-11": ("Life Sciences P2 Nov 2025 Eng.pdf", "Life Sciences P2 Nov 2025 MG Eng.pdf"),
    "ls-p1-2024-11": ("Life Sciences P1 Nov 2024 Eng.pdf", "Life Sciences P1 Nov MG 2024 Eng.pdf"),
    "bs-p1-2025-11": ("Business Studies P1 Nov 2025 Eng.pdf", "Business Studies P1 Nov 2025 MG Eng.pdf"),
    "bs-p2-2025-11": ("Business Studies P2 Nov 2025 Eng.pdf", "Business Studies P2 Nov 2025 MG Eng.pdf"),
    "ps-p1-2025-11": ("Physical Sciences P1 Nov 2025 Eng.pdf", "Physical Sciences P1 Nov 2025 MG Afr & Eng.pdf"),
    "ps-p2-2025-11": ("Physical Sciences P2 Nov 2025 Eng.pdf", "Physical Sciences P2 Nov 2025 MG Afr & Eng.pdf"),
}


def qp_json(subject, n, year):
    for f in os.listdir(PAIRS):
        if f.endswith(".json") and " MG " not in f and re.sub(r"\s+", " ", f).startswith("%s P%d Nov %d" % (subject, n, year)):
            return json.load(open(os.path.join(PAIRS, f), encoding="utf-8"))
    return None


if __name__ == "__main__":
    papers, missing = [], []
    for subj in SUBJECTS:
        for year in (2025, 2024):
            for n in (1, 2):
                d = qp_json(subj, n, year)
                if d is None:
                    missing.append("%s P%d %d" % (subj, n, year))
                pid = "%s-p%d-%d-11" % (SLUG[subj], n, year)
                entry = {
                    "id": pid, "title": "%s P%d" % (subj, n), "subject": subj, "paper_no": n,
                    "qualification": "high_school", "curriculum": "CAPS", "grade": 12, "level": "G12", "level_detail": "Grade 12",
                    "sitting": "November %d" % year, "year": year, "month": 11,
                    "total_marks": (d or {}).get("paper_total") or 150, "duration_minutes": MINUTES[subj],
                    "questions": len((d or {}).get("questions") or []) or None,
                    # the prototype's unit: a numbered group (1.1, 1.2, 2.1 ...), what a learner plays as one mission
                    "missions": len({".".join(re.split(r"[.(]", i["label"])[:2]) for q in (d or {}).get("questions") or [] for i in q.get("items", [])}) or None,
                    "status": "preparing", "provenance_label": "DBE question paper · November %d" % year}
                if pid in FINISHED:
                    assert os.path.exists(os.path.join(ROOT, "tools", "ingest", "out", pid, "paper.js")), pid + ": not ingested yet"
                    entry["status"] = "ready"
                    entry["source_pdf"] = "uploads/" + FINISHED[pid][0]
                    # a paper played in part (Geography: its maps are not published, so Section B's map questions wait) shows the marks
                    # it plays; the cover's stays as printed_marks
                    played = json.load(open(os.path.join(ROOT, "tools", "ingest", "out", pid, "paper.json"), encoding="utf-8"))["paper"].get("total_marks")
                    if played and played != entry["total_marks"]:
                        entry["printed_marks"], entry["total_marks"] = entry["total_marks"], played
                papers.append(entry)
    unknown = set(FINISHED) - {p["id"] for p in papers}
    assert not unknown, "FINISHED names papers outside the catalogue: %s" % sorted(unknown)
    src = ("// GENERATED by tools/catalogue/make_catalogue.py on the verified rollout-1 papers. Do not edit by hand.\n"
           "// MOCK of GET /v1/papers: Grade 12 November 2024 + 2025, P1 + P2, the six rollout subjects.\n"
           "window.NX_CATALOGUE = " + json.dumps({"version": 1, "papers": papers}, ensure_ascii=False, indent=1) + ";\n")
    open(OUT, "w", encoding="utf-8", newline="\n").write(src)
    print("papers:", len(papers), "| ready:", sorted(p["id"] for p in papers if p["status"] == "ready"), "| no mark map yet:", missing or "none")
