"""The question-type catalogue, as JSON Schema: the ONE source of truth for ingestion.

Follows A2UI's catalog conventions (https://a2ui.org/concepts/catalogs/): a `catalogId`, and every component the client renders
declared as a JSON Schema of its props, so an AI can only emit what the app can render and mark, and both sides validate. What the
ingestion agent emits is our PAPER data (the app's own format, the one paper-ls-p1-2026.js uses), not A2UI surface messages: the
app already renders and marks these types; the catalogue is the contract between the AI and the app.

Run `python tools/ingest/catalog.py` to write:
  catalog/nexera-exam-catalog.v1.json  the catalogue (components + props)
  catalog/paper.schema.json            the ingestion output schema (a paper whose parts are catalogue components)

Structured-output limits respected (the API rejects otherwise): every object has additionalProperties false; no recursion; no
numeric or length constraints (validate.py checks those).
"""
import json
from pathlib import Path

CATALOG_ID = "https://nexera.app/catalogs/exam/v1"
HERE = Path(__file__).parent


def obj(props, required):
    return {"type": "object", "properties": props, "required": required, "additionalProperties": False}


STR, INT, NUM = {"type": "string"}, {"type": "integer"}, {"type": "number"}
STRS, INTS = {"type": "array", "items": STR}, {"type": "array", "items": INT}

# Fields every part carries. `q` is the stem exactly as printed; `clues` are two hints that lead without giving the answer.
COMMON = {
    "n": {"type": "string", "description": "The part's number exactly as printed, e.g. 2.4.1(a)"},
    "marks": INT,
    "q": {"type": "string", "description": "The question text exactly as printed, without the marks"},
    "clues": {"type": "array", "items": STR, "description": "Two hints that lead the learner without giving the answer"},
    "note": {"type": "string", "description": "Optional: what a figure's label shows, for the record (never shown)"},
}
COMMON_REQ = ["n", "marks", "q", "clues"]

FIGURE = obj({
    "page": {"type": "integer", "description": "1-based page of the QUESTION PAPER the figure is on"},
    "bbox": {"type": "array", "items": NUM, "description": "[x0, y0, x1, y1] as fractions of the page width and height (0-1), tight around the figure and its labels"},
    "caption": {"type": "string", "description": "What the figure shows, for a learner who cannot see it (alt text)"}}, ["page", "bbox", "caption"])


def component(t, description, props, required):
    """A catalogue component: its type tag `t` plus the common fields."""
    p = {"t": {"type": "string", "const": t}, **COMMON, **props}
    return {"description": description, "schema": obj(p, ["t", *COMMON_REQ, *required])}


COMPONENTS = {
    "mcq": component("mcq", "Pick ONE of 2-6 options.", {"opts": STRS, "a": {"type": "integer", "description": "0-based index of the right option"},
                                                       "optTable": obj({"head": STRS, "rows": {"type": "array", "items": STRS}}, ["head", "rows"]) | {
                                                           "description": "Only when the paper prints the options as a TABLE: its column heads, and one row of cells per option in the order of opts (opts then reads each row as a line)"},
                                                       "figure": {**FIGURE, "description": "Only when the paper prints a figure for THIS one question (not the whole block)"}}, ["opts", "a"]),
    "pickn": component("pickn", "Pick N of several options.", {"opts": STRS, "pool": {**INTS, "description": "0-based indexes of every right option"}, "count": INT}, ["opts", "pool", "count"]),
    "order": component("order", "Put the options in sequence.", {"opts": STRS, "a": {**INTS, "description": "option indexes in the right order"}}, ["opts", "a"]),
    "term": component("term", "One term or short phrase (one line).", {
        "a": {**STRS, "description": "Every answer the memo accepts, first the memo's own wording"},
        "reject": {**STRS, "description": "Real terms one or two letters away that are WRONG (e.g. 'complete dominance' for 'incomplete dominance')"}}, ["a"]),
    "list": component("list", "N numbered one-line answers ('Name TWO ...').", {
        "count": INT, "pool": {"type": "array", "items": STRS, "description": "Each memo answer as a group of accepted synonyms"}}, ["count", "pool"]),
    "lettername": component("lettername", "Give the LETTER of a labelled part, then its NAME.", {
        "letters": STRS, "a": obj({"letter": STR, "name": STRS}, ["letter", "name"]),
        "or": {"type": "array", "items": obj({"letter": STR, "name": STRS}, ["letter", "name"]),
               "description": "Other letter + name pairs the memo accepts INSTEAD ('C - urethra OR D - penis': a = C, or = [D])"}}, ["letters", "a"]),
    "letternames": component("letternames", "Give the LETTERS and NAMES of COUNT labelled parts, in any order (one letter + name per part).", {
        "letters": STRS, "count": INT,
        "pool": {"type": "array", "items": obj({"letter": STR, "name": STRS}, ["letter", "name"]), "description": "Every part the memo accepts, each with its accepted names"}},
        ["letters", "count", "pool"]),
    "num": component("num", "One number (keypad), within a tolerance.", {"a": NUM, "tol": NUM, "unit": STR}, ["a", "tol"]),
    "steps": component("steps", "A calculation in numbered steps, each one NUMBER (method marks per step).", {
        "steps": {"type": "array", "items": obj({"id": STR, "label": STR, "marks": INT, "a": NUM, "tol": NUM,
                                                  "memo": {"type": "string", "description": "the memo's working for this step"}},
                                                 ["id", "label", "marks", "a", "tol", "memo"])}}, ["steps"]),
    "rubric": component("rubric", "A written answer marked against the memo's points (Explain / Describe / State ...).", {
        "bullets": {**STRS, "description": "The memo's marking points, one per mark (or per 'each'). An alternative answer starts 'OR — '"},
        "each": {"type": "integer", "description": "Marks per point when one point is worth more than 1"}}, ["bullets"]),
    "draw": component("draw", "No catalogue type fits (a drawing, a graph to plot, a structured essay ...): the learner answers on paper and self-checks against the memo's criteria. Flag it no_fit.", {
        "criteria": {"type": "array", "items": obj({"text": STR, "marks": INT}, ["text", "marks"])},
        "memo": STR}, ["criteria"]),
}

TABLE = obj({"title": STR, "head": STRS, "rows": {"type": "array", "items": STRS},
             "after": {"type": "string", "description": "Text printed after the table, if any"}}, ["head", "rows"])
MISSION = obj({
    "id": {"type": "string", "description": "The question number this block of parts shares, e.g. 2.4"},
    "title": STR, "kind": {"type": "string", "description": "A 2-5 word topic name"},
    "lead": {"type": "string", "description": "The lead sentence(s) printed before the parts"},
    "marks": INT,
    "extract": {"type": "string", "description": "Shared text the parts depend on (case study, procedure), exactly as printed"},
    "table": TABLE, "figure": FIGURE,
    "items": {"type": "array", "items": {"anyOf": [c["schema"] for c in COMPONENTS.values()]}}}, ["id", "title", "marks", "items"])
FLAG = obj({
    "n": {"type": "string", "description": "The part (or mission) number the flag is about"},
    "kind": {"type": "string", "enum": ["low_confidence", "no_fit", "memo_issue", "missing_resource", "figure_unclear"]},
    "detail": STR}, ["n", "kind", "detail"])
PAPER = obj({
    "catalog": {"type": "string", "const": CATALOG_ID},
    "paper": obj({"subject": STR, "title": STR, "sitting": STR, "total_marks": INT, "time": STR}, ["subject", "title", "sitting", "total_marks", "time"]),
    "sections": {"type": "array", "items": obj({"title": STR, "total": INT, "missions": {"type": "array", "items": MISSION}}, ["title", "total", "missions"])},
    "flags": {"type": "array", "items": FLAG}}, ["catalog", "paper", "sections", "flags"])


def catalog():
    return {"catalogId": CATALOG_ID, "title": "Nexera exam-practice question types",
            "components": {k: {"description": c["description"], "props": c["schema"]} for k, c in COMPONENTS.items()}}


if __name__ == "__main__":
    out = HERE / "catalog"; out.mkdir(exist_ok=True)
    (out / "nexera-exam-catalog.v1.json").write_text(json.dumps(catalog(), indent=1), encoding="utf-8")
    (out / "paper.schema.json").write_text(json.dumps(PAPER, indent=1), encoding="utf-8")
    print("wrote", len(COMPONENTS), "components ->", out)
