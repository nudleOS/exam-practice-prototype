"""Writes papers-catalogue.js: a MOCK of the exam service's paper list (GET /v1/papers) for rollout 1's Grade 12 November
papers (six subjects, P1 + P2, 2025 + 2024). Every fact comes from the paper itself:
  time  = the cover's "TIME:" line (text papers read by script; the 8 scanned maths covers read by eye 2026-10-02: 3 hours)
  marks = the cover's total (a ready paper played in part: the marks it plays, the cover's kept as printed_marks);
          questions / missions = the question paper's mark map (pairs/<QP>.json, checked against the memo's
          by compare_pairs.py on 2026-10-02; the memo maps hold answers and stay out of git)

A paper in FINISHED is transcribed and validated (tools/ingest/out/<id>/paper.js): it is "ready", the page loads it with the
app, and its question paper is its source_pdf (so the question pages show the view-paper button; tools/catalogue/make_pages.py
renders its page images). Every other paper is "preparing".

Grades 10 and 11 (Murci 2026-10-12: the provincial November 2024 and 2025 papers replace the DBE 2017/2018 common papers, the
same six subjects as Grade 12): LOWER, each paper's source in tools/ingest/PROVENANCE-g10-g11.md. A lower-grade paper is listed
only once it is transcribed (tools/ingest/out/<id>): its grade from its id (g10-, g11-), its subject, number, sitting, marks
and time from its own paper.json, its provenance label from the province that set it.

  python tools/catalogue/make_catalogue.py      (then python tools/catalogue/make_pages.py)
"""
import hashlib
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
    "ls-p2-2024-11": ("Life Sciences P2 Nov 2024 Eng.pdf", "Life Sciences P2 Nov 2024 MG Eng.pdf"),
    "bs-p1-2025-11": ("Business Studies P1 Nov 2025 Eng.pdf", "Business Studies P1 Nov 2025 MG Eng.pdf"),
    "bs-p2-2025-11": ("Business Studies P2 Nov 2025 Eng.pdf", "Business Studies P2 Nov 2025 MG Eng.pdf"),
    "bs-p1-2024-11": ("Business Studies P1 Nov 2024 Eng.pdf", "Business Studies P1 Nov 2024 MG Eng.pdf"),
    "bs-p2-2024-11": ("Business Studies P2 Nov 2024  Eng.pdf", "Business Studies P2 Nov 2024 MG Eng.pdf"),
    "ps-p1-2025-11": ("Physical Sciences P1 Nov 2025 Eng.pdf", "Physical Sciences P1 Nov 2025 MG Afr & Eng.pdf"),
    "ps-p2-2025-11": ("Physical Sciences P2 Nov 2025 Eng.pdf", "Physical Sciences P2 Nov 2025 MG Afr & Eng.pdf"),
    "ps-p1-2024-11": ("Physical Sciences P1 Nov 2024 Eng.pdf", "Physical Sciences P1 Nov 2024 MG Afr & Eng.pdf"),
    "ps-p2-2024-11": ("Physical Sciences P2 Nov 2024 Eng.pdf", "Physical Sciences P2 Nov 2024 MG Afr & Eng.pdf"),
    "geo-p1-2025-11": ("Geography P1 Nov 2025 Eng.pdf", "Geography P1 Nov 2025 MG Eng.pdf"),
    "geo-p2-2025-11": ("Geography P2 Nov 2025 Eng.pdf", "Geography P2 Nov 2025 MG Eng.pdf"),
    "geo-p1-2024-11": ("Geography P1 Nov 2024 Eng.pdf", "Geography P1 Nov 2024 MG Eng.pdf"),
    "geo-p2-2024-11": ("Geography P2 Nov 2024 Eng.pdf", "Geography P2 Nov 2024 MG Eng.pdf"),
    "ml-p1-2025-11": ("Mathematical Literacy P1 Nov 2025 Eng.pdf", "Mathematical Literacy P1 Nov 2025 MG Afr & Eng.pdf"),
    "ml-p2-2025-11": ("Mathematical Literacy P2 Nov 2025 Eng.pdf", "Mathematical Literacy P2 Nov 2025 MG Afr & Eng.pdf"),
    "ml-p1-2024-11": ("Mathematical Literacy P1 Nov 2024 Eng.pdf", "Mathematical Literacy P1 Nov 2024 MG Afr & Eng.pdf"),
    "ml-p2-2024-11": ("Mathematical Literacy P2 Nov 2024 Eng.pdf", "Mathematical Literacy P2 Nov 2024 MG Afr & Eng.pdf"),
    "math-p1-2025-11": ("Mathematics P1 Nov 2025 Eng.pdf", "Mathematics P1 Nov 2025 MG Afr & Eng.pdf"),
    "math-p2-2025-11": ("Mathematics P2 Nov 2025 Eng.pdf", "Mathematics P2 Nov 2025 MG Afr & Eng.pdf"),
    "math-p1-2024-11": ("Mathematics P1 Nov 2024 Eng.pdf", "Mathematics P1 Nov 2024 MG Afr & Eng.pdf"),
    "math-p2-2024-11": ("Mathematics P2 Nov 2024 Eng.pdf", "Mathematics P2 Nov 2024 MG Afr & Eng.pdf"),
}

# Grades 10 and 11: the provincial papers (downloaded 2026-10-12 into uploads/provincial/<id>/, PROVENANCE-g10-g11.md: every
# file's URL and sha256). id -> (question paper, memo) under uploads/; a paper printed with its memo in one PDF is split into
# "<id> QP.pdf" and "<id> MG.pdf" beside it (tools/ingest/split_combined.py).
PROVINCE = {"ec": "Eastern Cape DoE", "nw": "North West DoE", "kzn": "KwaZulu-Natal DoE", "ecort": "Eastern Cape DoE (OR Tambo)"}
LOWER = {
    "g11-math-p1-2024-11-ec": ("provincial/g11-math-p1-2024-11-ec/MATHS P1 QP GR11 NOV2024 ENG D_watermark.pdf",
                               "provincial/g11-math-p1-2024-11-ec/MATHS P1 MEMO GR11 NOV2024_ENG_AFR_watermark.pdf"),
    "g11-math-p2-2024-11-ec": ("provincial/g11-math-p2-2024-11-ec/MATHS P2 QP GR11 2024 ENG D_watermark.pdf",
                               "provincial/g11-math-p2-2024-11-ec/MATHS P2 GRADE 11 NOV 2024 ENG_AFR MARKING GUIDELINE_watermark.pdf"),
    "g11-math-p1-2025-11-ec": ("provincial/g11-math-p1-2025-11-ec/MATHS P1 QP GR11 NOV 2025 ENG_watermark.pdf",
                               "provincial/g11-math-p1-2025-11-ec/MATHS P1 MEMO GR11 NOV 2025 E+A_watermark.pdf"),
    "g11-math-p2-2025-11-ec": ("provincial/g11-math-p2-2025-11-ec/MATHS P2 QP GR 11 2025 ENG_watermark.pdf",
                              "provincial/g11-math-p2-2025-11-ec/MATHS P2 MEMO GR 11  NOVEMBER 2025 (ENG & AFR)_watermark.pdf"),
    "g11-ps-p1-2024-11-ec": ("provincial/g11-ps-p1-2024-11-ec/PHYS SCIENCES  P1 QP GR11 NOV 2024 ENG D_watermark.pdf",
                            "provincial/g11-ps-p1-2024-11-ec/PHYS SCIENCES P1 GR11 MEMO NOV 2024 ENG + AFR_watermark.pdf"),
    "g11-ps-p2-2024-11-ec": ("provincial/g11-ps-p2-2024-11-ec/PHYSICAL Sc. P2 QP GR11 NOV 2024 ENG D_watermark.pdf",
                            "provincial/g11-ps-p2-2024-11-ec/PHYSICAL SCIENCES P2 GR11 MEMO 2024 ENG_AFR_watermark.pdf"),
    "g11-ps-p1-2025-11-ec": ("provincial/g11-ps-p1-2025-11-ec/PHYSICAL SC P1 QP GR11 NOV 2025 ENG_watermark.pdf",
                            "provincial/g11-ps-p1-2025-11-ec/PHYSICAL SC P1 MEMO NOV 2025 E+A_watermark.pdf"),
    "g11-ps-p2-2025-11-ec": ("provincial/g11-ps-p2-2025-11-ec/PHYSICAL SC P2 QP GR11 NOVEMBER 2025 (2)_watermark.pdf",
                            "provincial/g11-ps-p2-2025-11-ec/PHYSICAL SCIENCES P2 GRADE 11 MEMO NOVEMBER 2025 ENG & AFR_watermark.pdf"),
    "g11-ml-p1-2024-11-ec": ("provincial/g11-ml-p1-2024-11-ec/MATHS LIT P1 GR11 QP NOV 2024 ENG DD_watermark.pdf",
                            "provincial/g11-ml-p1-2024-11-ec/MATHS LIT P1 MEMO GR 11 NOV2024_English_watermark.pdf"),
    "g11-ml-p2-2024-11-ec": ("provincial/g11-ml-p2-2024-11-ec/MATHS LIT P2 GRADE 11 NOV 2024  ENGLISH D_watermark.pdf",
                            "provincial/g11-ml-p2-2024-11-ec/MATHS LIT P2 GRADE 11 NOV 2024 MARKING GUIDELINE_ENG_watermark.pdf"),
    "g11-ml-p1-2025-11-ec": ("provincial/g11-ml-p1-2025-11-ec/MATHS LITERACY P1 GR11 QP NOV2025_English_watermark.pdf",
                            "provincial/g11-ml-p1-2025-11-ec/MATHS LITERACY P1 GR11 MEMO NOV2025_English_watermark.pdf"),
    "g11-ml-p2-2025-11-ec": ("provincial/g11-ml-p2-2025-11-ec/MATHS LIT GRADE 11 NOV 2025 QPAPER (2)_watermark.pdf",
                            "provincial/g11-ml-p2-2025-11-ec/MATHS LIT P2 GRADE 11 NOV 2025 MEMO ENG_watermark.pdf"),
    "g11-ls-p1-2024-11-ec": ("provincial/g11-ls-p1-2024-11-ec/LIFE SCIENCES P1 GR11 QP NOV2024 ENG D_watermark.pdf",
                            "provincial/g11-ls-p1-2024-11-ec/FINAL AMENDED LIFE SCIENCES P1 GR11 MEMO NOV2024_English_watermark.pdf"),
    "g11-ls-p2-2024-11-ec": ("provincial/g11-ls-p2-2024-11-ec/LIFE SCIENCES P2 GR11 QP NOV2024 ENG D_watermark.pdf",
                            "provincial/g11-ls-p2-2024-11-ec/LIFE SCIENCES P2 GR11 MEMO NOV2024_English_watermark.pdf"),
    "g11-ls-p1-2025-11-ec": ("provincial/g11-ls-p1-2025-11-ec/LIFE SCIENCES P1 GR11 QP NOV2025_English_watermark.pdf",
                            "provincial/g11-ls-p1-2025-11-ec/LIFE SCIENCES P1 GR11 MEMO NOV2025_English_watermark.pdf"),
    "g11-ls-p2-2025-11-ec": ("provincial/g11-ls-p2-2025-11-ec/LIFE SCIENCES P2 QP GR11 NOV 2025 ENG_watermark.pdf",
                            "provincial/g11-ls-p2-2025-11-ec/LIFE SCIENCES P2 MEMO GR11 NOV 2025 ENG_watermark.pdf"),
    "g11-bs-p1-2024-11-ec": ("provincial/g11-bs-p1-2024-11-ec/BUSINESS STUDIES P1 GR 11 NOV Final ENG D_watermark.pdf",
                            "provincial/g11-bs-p1-2024-11-ec/BUSINESS STUDIES P1 GR11 MEMO NOV2024 -English_watermark.pdf"),
    "g11-bs-p2-2024-11-ec": ("provincial/g11-bs-p2-2024-11-ec/BUSINESS STUDIES gr 11 P2 QP ENG D_watermark.pdf",
                            "provincial/g11-bs-p2-2024-11-ec/BUSINESS STUDIES GR 11 P2 MG_ENG_watermark.pdf"),
    "g11-bs-p1-2025-11-ec": ("provincial/g11-bs-p1-2025-11-ec/BSTD P1 GRADE 11 Nov 2025 ENG_watermark.pdf",
                            "provincial/g11-bs-p1-2025-11-ec/BUSINESS STUDIES GRADE 11 NOV 2025 MARKING GUIDELINE_watermark.pdf"),
    "g11-bs-p2-2025-11-ec": ("provincial/g11-bs-p2-2025-11-ec/BUSINESS STUDIES P2 GR11 QP NOV2025_English_watermark.pdf",
                            "provincial/g11-bs-p2-2025-11-ec/BUSINESS STUDIES P2 GR11 MEMO NOV2025_English_watermark.pdf"),
}


def minutes(text):
    """'2 hours' -> 120, '1½ hours' -> 90, '3 hours' -> 180 (the cover's TIME line, as transcribed)."""
    m = re.match(r"^\s*(\d+)(½)?\s*hours?", text or "")
    assert m, "time not in hours: %r" % text
    return int(m.group(1)) * 60 + (30 if m.group(2) else 0)


def lower_entry(pid):
    """A transcribed Grade 10 / 11 paper's catalogue entry, every fact from its own paper.json; None until it is transcribed."""
    path = os.path.join(ROOT, "tools", "ingest", "out", pid, "paper.json")
    if not os.path.exists(path):
        return None
    d = json.load(open(path, encoding="utf-8"))
    meta, grade = d["paper"], int(pid[1:3])
    year = int(re.search(r"\d{4}", meta["sitting"]).group(0))
    missions = [m for s in d["sections"] for m in s["missions"]]
    js = os.path.join(ROOT, "tools", "ingest", "out", pid, "paper.js")
    assert os.path.exists(js), pid + ": not ingested yet"
    return {"id": pid, "title": meta["title"], "subject": meta["subject"], "paper_no": int(re.search(r"P(\d)", meta["title"]).group(1)),
            "qualification": "high_school", "curriculum": "CAPS", "grade": grade, "level": "G%d" % grade, "level_detail": "Grade %d" % grade,
            "sitting": meta["sitting"], "year": year, "month": 11, "total_marks": meta["total_marks"], "duration_minutes": minutes(meta["time"]),
            "questions": len({re.split(r"[.(]", m["id"])[0] for m in missions}), "missions": len(missions), "status": "ready",
            "rev": hashlib.sha1(open(js, "rb").read()).hexdigest()[:10], "source_pdf": "uploads/" + LOWER[pid][0],
            "provenance_label": "%s · November %d" % (PROVINCE[pid.rsplit("-", 1)[1]], year)}


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
                    # its content's fingerprint: the page loads paper.js?v=<rev>, so the browser keeps it until a re-ingest changes it
                    entry["rev"] = hashlib.sha1(open(os.path.join(ROOT, "tools", "ingest", "out", pid, "paper.js"), "rb").read()).hexdigest()[:10]
                    entry["source_pdf"] = "uploads/" + FINISHED[pid][0]
                    # a paper played in part (Geography: its maps are not published, so Section B's map questions wait) shows the marks
                    # it plays; the cover's stays as printed_marks
                    played = json.load(open(os.path.join(ROOT, "tools", "ingest", "out", pid, "paper.json"), encoding="utf-8"))["paper"].get("total_marks")
                    if played and played != entry["total_marks"]:
                        entry["printed_marks"], entry["total_marks"] = entry["total_marks"], played
                papers.append(entry)
    papers += [e for e in (lower_entry(pid) for pid in LOWER) if e]
    unknown = set(FINISHED) - {p["id"] for p in papers}
    assert not unknown, "FINISHED names papers outside the catalogue: %s" % sorted(unknown)
    src = ("// GENERATED by tools/catalogue/make_catalogue.py on the verified rollout-1 papers. Do not edit by hand.\n"
           "// MOCK of GET /v1/papers: Grade 12 November 2024 + 2025, P1 + P2, the six rollout subjects; Grade 10 and 11\n"
           "// provincial papers (the same six subjects, November 2024 + 2025) once transcribed.\n"
           "window.NX_CATALOGUE = " + json.dumps({"version": 1, "papers": papers}, ensure_ascii=False, indent=1) + ";\n")
    open(OUT, "w", encoding="utf-8", newline="\n").write(src)
    print("papers:", len(papers), "| ready:", sorted(p["id"] for p in papers if p["status"] == "ready"), "| no mark map yet:", missing or "none")
