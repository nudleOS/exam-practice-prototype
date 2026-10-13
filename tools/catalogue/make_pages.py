"""Writes papers-pages.js and the page images the paper viewer shows: the question paper and its memo as page IMAGES (2026-10-02).
Android Chrome will not show a PDF inside a page (it offers "Open" instead), and a browser's PDF viewer brings its toolbar; an
image of each page is just the paper, on every phone, loaded a page at a time. Also records which page each question (1.1,
1.4 ...) starts on, read from the PDF's own text, so the viewer opens at the question's page.

Papers: the design sample (ls-p1-2026) and every FINISHED paper (make_catalogue.py). Their PDFs are copied into uploads/ from
the papers folder (PAPERS_DIR) when missing. The question paper's pages are tracked (assets/papers/<id>/qp-NN.jpg, and the PDF
by name in .gitignore); the MEMO's stay out of git (uploads/ is ignored: memos are answers, Murci 2026-10-01).
An image already on disk is kept (delete it to re-render).

  python tools/catalogue/make_pages.py
"""
import json
import os
import re
import shutil

import fitz  # PyMuPDF

from make_catalogue import FINISHED, LOWER, ROOT

PAPERS_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Grade_12_Nov_Past_Papers_2024-2025")
DOCS = {"ls-p1-2026": {"qp": "uploads/Life Sciences P1 May-June 2026 Eng.pdf", "mg": "uploads/Life Sciences P1 May-June 2026 MG Eng.pdf"}}
DOCS.update({pid: {"qp": "uploads/" + qp, "mg": "uploads/" + mg} for pid, (qp, mg) in FINISHED.items()})
# Grades 10 and 11: a provincial paper's pages once it is transcribed (its PDFs are in uploads/provincial/<id>/, PROVENANCE-g10-g11.md)
DOCS.update({pid: {"qp": "uploads/" + qp, "mg": "uploads/" + mg} for pid, (qp, mg) in LOWER.items()
             if os.path.exists(os.path.join(ROOT, "tools", "ingest", "out", pid, "paper.json"))})
OUT = {"qp": "assets/papers/{id}/qp-{n:02d}.jpg", "mg": "uploads/papers/{id}/mg-{n:02d}.jpg"}
WIDTH = 1000
LBL = re.compile(r"^\s*(\d{1,2}\.\d{1,2})(?:\.\d{1,2})?(?:\s|$)", re.M)
# a SCANNED question paper has no text to read the question numbers from: its pages are read by eye (2026-10-07)
FOUND_BY_EYE = {
    # Grade 10 / 11 common papers (scanned Mathematics), read off each page by the transcribing agent (2026-10-11)
    "g10-math-p1-2018-11": {"1.1": 3, "1.2": 3, "1.3": 3, "2.1": 3, "2.2": 3, "2.3": 3, "3": 4, "4": 4, "5": 5, "6": 6, "7": 6,
                            "8.1": 7, "8.2": 7, "8.3": 7},
    "g10-math-p1-2017-11": {"1.1": 3, "1.2": 3, "1.3": 3, "2.1": 3, "2.2": 3, "2.3": 3, "2.4": 3, "3.1": 4, "3.2": 4, "4.1": 4,
                            "4.2": 4, "5": 5, "6.1": 6, "6.2": 6, "7.1": 7, "7.2": 7},
    "g10-math-p2-2018-11": {"1": 3, "2": 4, "3.1": 5, "3.2": 5, "3.3": 5, "4.1": 6, "4.2": 6, "5.1": 6, "5.2": 7, "6": 7, "7": 8,
                            "8.1": 9, "8.2": 9},
    "g10-math-p2-2017-11": {"1": 3, "2": 3, "3": 4, "4.1": 5, "4.2": 5, "4.3": 5, "5": 5, "6": 6, "7": 7, "8.1": 8, "8.2": 8, "8.3": 9,
                            "9": 10},
    "g11-math-p1-2018-11": {"1.1": 3, "1.2": 3, "1.3": 3, "1.4": 3, "2.1": 3, "2.2": 3, "2.3": 3, "3.1": 4, "3.2": 4, "4": 4, "5": 5,
                            "6": 6, "7.1": 7, "7.2": 7, "7.3": 7, "8": 7, "9.1": 8, "9.2": 8},
    "g11-math-p1-2017-11": {"1.1": 3, "1.2": 3, "1.3": 3, "2.1": 3, "2.2": 3, "2.3": 3, "2.4": 3, "3.1": 4, "3.2": 4, "4": 4,
                            "5": 4, "6": 5, "7.1": 6, "7.2": 6, "7.3": 6, "7.4": 6, "8.1": 6, "8.2": 6, "9": 7},
    "g11-math-p2-2017-11": {"1.1": 3, "1.2": 3, "2": 4, "3": 5, "4": 6, "5.1": 7, "5.2": 7, "5.3": 7, "5.4": 7, "6": 8, "7": 8,
                            "8": 9, "9.1": 10, "9.2": 10, "10": 11, "11": 12, "12": 13},
    "g11-math-p2-2018-11": {"1": 3, "2.1": 4, "2.2": 5, "3": 6, "4": 7, "5.1": 8, "5.2": 8, "5.3": 8, "5.4": 8, "6": 9, "7.1": 10,
                            "7.2": 10, "8": 11, "9.1": 12, "9.2": 13, "9.3": 13, "10.1": 14, "10.2": 15, "11": 16},
    "ml-p1-2025-11": {"1.1": 3, "1.2": 4, "1.3": 5, "2.1": 6, "2.2": 7, "3.1": 8, "3.2": 9, "4.1": 10, "4.2": 11, "5.1": 12, "5.2": 13},
    "ml-p2-2025-11": {"1.1": 3, "1.2": 4, "1.3": 5, "2.1": 6, "2.2": 7, "2.3": 7, "3.1": 8, "3.1.5": 9, "3.2": 10, "4.1": 12, "4.2": 12,
                      "5.1": 14, "5.2": 14, "5.3": 15},
    "math-p1-2025-11": {"1.1": 3, "1.2": 3, "2.1": 3, "2.2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7.1": 8, "7.2": 8, "7.3": 8,
                        "8.1": 8, "8.2": 8, "9": 9, "10": 10, "11.1": 11, "11.2": 11, "11.3": 11},
    "math-p2-2025-11": {"1": 3, "2.1": 4, "2.2": 4, "3": 5, "4": 6, "5.1": 7, "5.2": 7, "6": 7, "7": 8, "8": 9, "9.1": 10,
                        "9.2": 11, "10": 12, "11.1": 13, "11.2": 14},
    # 2026-10-10, read off each page's left margin (the question numbers)
    "ml-p1-2024-11": {"1.1": 3, "1.2": 4, "1.3": 5, "2.1": 6, "2.2": 7, "2.3": 7, "3.1": 8, "3.2": 9, "3.2.4": 9, "4.1": 10, "4.2": 11,
                      "5.1": 12, "5.2": 12, "5.3": 13},
    "ml-p2-2024-11": {"1.1": 3, "1.2": 3, "1.3": 4, "2.1": 5, "2.1.6": 5, "2.2": 6, "2.2.3": 6, "3.1": 7, "3.2": 8, "3.3": 9, "3.3.2": 9,
                      "4.1": 10, "4.2": 11, "5.1": 12, "5.2": 12, "5.3": 13},
    "math-p1-2024-11": {"1.1": 3, "1.2": 3, "1.3": 3, "2.1": 3, "2.2": 3, "3": 4, "4": 4, "5": 5, "6": 6, "7.1": 7, "7.2": 7, "7.3": 7,
                        "8.1": 7, "8.2": 7, "8.3": 7, "9": 8, "10": 8, "11": 9, "12": 9},
    "math-p2-2024-11": {"1": 3, "2": 4, "3": 5, "4": 6, "5.1": 7, "5.2": 7, "6.1": 8, "6.2": 8, "6.3": 8, "7": 9, "8": 10, "9": 11,
                        "10.1": 12, "10.2": 12, "11": 13},
    # scanned provincial papers (stanmorephysics.com re-publications, split into QP and MG), read by eye (2026-10-13)
    "g10-ml-p2-2025-11-ecort": {"1.1": 3, "1.2": 4, "2": 4, "3": 6, "4.1": 7, "4.2": 8},
    "g10-ml-p1-2025-11-ecort": {"1.1": 3, "1.2": 3, "2.1": 4, "2.2": 5, "3": 6, "4.1": 7, "4.2": 8},
    "g10-ps-p2-2025-11-kzn": {"1": 3, "2": 5, "2.2": 6, "3": 6, "3.2": 7, "4": 8, "5": 9, "6": 9, "7": 10},
    "g10-ps-p1-2025-11-kzn": {"1": 3, "2": 5, "2.2": 6, "3": 6, "4": 7, "5": 8, "6": 9, "6.2": 10, "7": 11, "8": 12},
    "g10-math-p2-2025-11-kzn": {"1": 3, "2": 3, "3": 4, "4": 5, "5": 6, "5.2": 7, "6": 7, "7": 8, "7.2": 12, "7.3": 9, "8": 10, "9": 10},
    "g10-math-p1-2025-11-kzn": {"1": 3, "1.2": 3, "1.3": 3, "2": 4, "3": 4, "4": 5, "5": 6, "5.2": 7, "6": 7, "7": 7},
}
# memos with no text layer (scanned, bilingual): the page each question starts on, read by eye (2026-10-11)
MEMO_BY_EYE = {
    "g10-ml-p2-2025-11-ecort": {"1.1": 4, "1.2": 4, "2": 4, "3": 5, "4.1": 5, "4.2": 6},
    "g10-ml-p1-2025-11-ecort": {"1.1": 4, "1.2": 4, "2.1": 5, "2.2": 5, "3": 6, "4.1": 7, "4.2": 7},
    "g10-ps-p2-2025-11-kzn": {"1": 2, "2": 2, "3": 3, "4": 3, "4.2.3": 4, "5": 4, "5.3.2": 5, "6": 5, "6.2": 6, "7": 6},
    "g10-ps-p1-2025-11-kzn": {"1": 2, "2": 2, "2.2": 3, "3": 3, "4": 3, "5": 4, "6": 5, "7": 6, "8": 6},
    "g10-math-p2-2025-11-kzn": {"1": 2, "2": 2, "2.3": 3, "3": 3, "3.1.4": 4, "4": 4, "4.1.3": 5, "5": 5, "5.1.2": 6, "6": 7, "7": 8,
                                "7.3": 9, "8": 9, "8.3": 10, "9": 10},
    "g10-math-p1-2025-11-kzn": {"1": 2, "1.3": 2, "2": 3, "2.2": 3, "3": 4, "3.2.3": 5, "3.3": 5, "4": 5, "4.3": 6, "5": 6, "5.1.4": 7,
                                "5.2": 7, "6": 9, "7": 10},
    "g10-math-p2-2018-11": {"1": 2, "2": 3, "2.2.2": 4, "2.2.3": 4, "2.3": 5, "3.1": 5, "3.2": 5, "3.2.2": 6, "3.3": 6, "4.1": 7,
                            "4.2": 8, "5.1": 9, "5.2": 9, "6": 9, "7": 10, "8.1": 11, "8.1.2": 12, "8.2": 13},
    "g11-math-p1-2018-11": {"1.1": 2, "1.1.4": 3, "1.2": 4, "1.3": 5, "1.4": 5, "2.1": 6, "2.2": 6, "2.2.2": 7, "2.2.3": 7, "2.3": 7,
                            "3.1": 8, "3.2": 8, "4": 9, "4.2": 10, "4.3": 11, "4.4": 11, "5": 12, "5.5": 13, "5.6": 13, "5.7": 13,
                            "6": 14, "6.6": 15, "6.7": 16, "6.8": 16, "6.9": 16, "7.1": 17, "7.2": 17, "7.3": 17, "8": 18, "9.1": 19,
                            "9.2": 19},
    "g11-math-p2-2018-11": {"1": 2, "2.1": 3, "2.1.4": 4, "2.2": 4, "3": 5, "3.2": 6, "3.3": 6, "3.4": 6, "3.5": 7, "3.6": 7, "3.7": 8,
                            "4": 9, "4.3": 10, "4.4": 10, "5.1": 11, "5.1.5": 12, "5.2": 12, "5.3": 13, "5.4": 14, "6": 16, "7.1": 17,
                            "7.2": 18, "8": 20, "9.1": 21, "9.2": 22, "9.3": 23, "10.1": 24, "10.2": 25, "11": 26, "11.2": 27},
}


def ensure_pdf(rel):
    """The PDF at uploads/<name>, copied from the papers folder when it is not there yet."""
    path = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(path):
        name = os.path.basename(path)
        found = [os.path.join(d, name) for d, _, files in os.walk(PAPERS_DIR) if name in files]
        if len(found) != 1:
            raise SystemExit("%s: expected it once in %s, found %d" % (name, PAPERS_DIR, len(found)))
        shutil.copyfile(found[0], path)
    return path


manifest = {}
for pid, docs in DOCS.items():
    manifest[pid] = {}
    for kind, rel in docs.items():
        doc = fitz.open(ensure_pdf(rel))
        find, made = {}, 0
        for i, page in enumerate(doc):
            for m in LBL.finditer(page.get_text()):
                q = m.group(1)
                if q not in find and int(q.split(".")[0]) <= 12:
                    find[q] = i + 1
            path = os.path.join(ROOT, OUT[kind].format(id=pid, n=i + 1).replace("/", os.sep))
            if not os.path.exists(path):
                z = WIDTH / page.rect.width
                os.makedirs(os.path.dirname(path), exist_ok=True)
                page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False).save(path, jpg_quality=70)
                made += 1
        if not find and kind == "qp":
            find = dict(FOUND_BY_EYE.get(pid, {}))
        if not find and kind == "mg":
            find = dict(MEMO_BY_EYE.get(pid, {}))
        manifest[pid][kind] = {"pages": doc.page_count, "src": OUT[kind].format(id=pid, n=0)[:-6], "pdf": rel,
                               "w": WIDTH, "h": round(WIDTH * doc[0].rect.height / doc[0].rect.width), "find": find}
        print("%s %s: %d pages (%d rendered now), %d questions located" % (pid, kind, doc.page_count, made, len(find)))
js = ("// GENERATED by tools/catalogue/make_pages.py. Which page images a paper and its memo have, and where each question starts.\n"
      "window.NX_PAGES = " + json.dumps(manifest, indent=1) + ";\n")
open(os.path.join(ROOT, "papers-pages.js"), "w", encoding="utf-8", newline="\n").write(js)
print("ok")
