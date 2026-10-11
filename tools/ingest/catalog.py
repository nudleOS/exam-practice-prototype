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
    "after": {**STRS, "description": "Optional: earlier parts (numbers) whose ANSWERS this part shows (e.g. it classifies the sentences an earlier part asks the learner to quote): it opens only once they are answered"},
}
COMMON_REQ = ["n", "marks", "q", "clues"]

FIGURE = obj({
    "page": {"type": "integer", "description": "1-based page of the QUESTION PAPER the figure is on"},
    "bbox": {"type": "array", "items": NUM, "description": "[x0, y0, x1, y1] as fractions of the page width and height (0-1), tight around the figure and its labels"},
    "caption": {"type": "string", "description": "What the figure shows, for a learner who cannot see it (alt text)"},
    "source": {"type": "string", "enum": ["answer_book"], "description": "Only when the figure is printed in the ANSWER BOOK (an answer sheet's "
                                                                           "graph or annexure), not the question paper: page is then the answer book's"},
    "inset": {"type": "integer", "description": "Pixels of white margin round the crop, when a label touches its corner (the page's Hide "
                                                "button sits on the figure's top-left corner)"},
    "rotate": {"type": "integer", "enum": [90, 180, 270], "description": "Clockwise degrees that turn a figure printed SIDEWAYS upright "
                                                                        "(a landscape annexure on its side): 90 when its text reads bottom to top"}},
    ["page", "bbox", "caption"])


def component(t, description, props, required):
    """A catalogue component: its type tag `t` plus the common fields."""
    p = {"t": {"type": "string", "const": t}, **COMMON, **props}
    return {"description": description, "schema": obj(p, ["t", *COMMON_REQ, *required])}


NUMS = {"type": "array", "items": NUM}
FAMILIES = ["parabola", "hyperbola", "exponential", "log", "cubic", "line", "sin", "cos", "tan"]
# a graph sketch (2026-10-11): the memo's features placed on a grid, the curve drawn through them (build-play.js "sketch")
SK_SHAPE = obj({
    "label": {"type": "string", "description": "A NEUTRAL name for the shape, shown on its result chip ('Shape'): never the answer ('decreasing')"},
    "answer": {"anyOf": [STR, STRS], "description": "The shape word the memo marks, as the builder names a curve: exponential 'increasing' / "
               "'decreasing' (+ ', above' / ', below' its asymptote: 'increasing, above'), log 'increasing' / 'decreasing', line 'positive "
               "gradient' / 'negative gradient', parabola '∪' / '∩', cubic 'positive' / 'negative' (leading coefficient), hyperbola 'top right "
               "and bottom left' / 'top left and bottom right', tan 'increasing' / 'decreasing'; 'drawn' for any curve through the features "
               "(a sine or cosine's 'Shape'). A shorter answer is met by a longer word ('decreasing' by 'decreasing, above'); a list: any of them"},
    "marks": INT,
    "crit": {"type": "integer", "description": "0-based index of the memo criterion this shape belongs to (see the feature's crit)"},
    "pick": {**STRS, "description": "Only when the memo's features leave the shape open (one intercept + the asymptote fix no exponential): "
             "the words the learner chooses from (['increasing', 'decreasing']); the curve then follows the choice"}},
    ["label", "answer", "marks"])
SK_FEATURE = obj({
    "id": STR,
    "kind": {"type": "string", "enum": ["point", "hline", "vline"], "description": "a point, or an asymptote: a horizontal / vertical line"},
    "label": {"type": "string", "description": "The memo's NAME for it, never its position ('y-intercept', 'turning point', 'asymptote', "
              "'one other point', 'x-intercept of g'); features with the same graph, kind and label are matched as a set, in any order"},
    "at": {"anyOf": [NUMS, NUM], "description": "Where the memo puts it: [x, y] for a point, the value for a line (y = −9: -9)"},
    "alt": {"type": "array", "items": {"anyOf": [NUMS, NUM]}, "description": "Other places the memo accepts ('ANY other point', "
            "'(45° ; −3) or (135° ; 3)'), on the grid"},
    "tol": {"type": "number", "description": "How far from at (or an alt) still earns it, in the axis' units (0: the exact grid point)"},
    "marks": {"type": "integer", "description": "Its marks (0 when it only completes a criterion another feature carries)"},
    "crit": {"type": "integer", "description": "0-based index of the memo criterion it belongs to: features (and a shape) sharing a crit earn "
             "only together ('Intercepts (2 ; 0) and (0 ; −8)', 1 mark: one carries the mark, the other 0)"},
    "graph": {"type": "string", "description": "With graphs: the id of the graph it belongs to"},
    "turn": {"type": "boolean", "description": "A turning point (the curve is flat there): the fit uses it"}},
    ["id", "kind", "label", "at", "tol", "marks"])
SK_GRAPH = obj({"id": STR, "family": {"type": "string", "enum": FAMILIES}, "label": {"type": "string", "description": "its name on the paper (g, h)"},
                "b": {"type": "number", "description": "trig only: the period factor the stem's equation prints (cos 2x: 2)"},
                "domain": {**NUMS, "description": "[x0, x1] where it is drawn, when the paper limits it ('for 0° ≤ x ≤ 270°')"}, "shape": SK_SHAPE},
               ["id", "family", "label"])
SKETCH = obj({
    "kind": {"type": "string", "const": "sketch"},
    "family": {"type": "string", "enum": FAMILIES, "description": "the graph's family (with graphs: the first graph's)"},
    "b": {"type": "number", "description": "trig only: the period factor the stem's equation prints (cos 2x + 1: 2; tan x: 1)"},
    "x": {**NUMS, "description": "[min, max, step] of the grid's x-axis (degrees for a trig graph); the learner's taps snap to the step"},
    "y": {**NUMS, "description": "[min, max, step] of the y-axis"},
    "domain": {**NUMS, "description": "[x0, x1] where the curve is drawn, when the paper limits it"},
    "features": {"type": "array", "items": SK_FEATURE, "description": "every feature the memo's criteria mark, in the memo's order"},
    "shape": SK_SHAPE,
    "graphs": {"type": "array", "items": SK_GRAPH, "description": "Only for TWO graphs on one set of axes ('Sketch f and g'): each with its "
               "family and shape; every feature names its graph"}},
    ["kind", "family", "x", "y", "features"])
# a box and whisker diagram and an inequality on a number line (2026-10-11): placed on the paper's own scaled line (build-play.js
# "boxplot" and "numline"); the learner sees the scale only
NL_SCALE = {
    "x": {**NUMS, "description": "[min, max, step] of the line: the paper's scale (the ANSWER BOOK's scaled line where it prints one, else "
          "a line that holds the answer with room either side). Every placement snaps to the step, so every memo value must be a multiple "
          "of it: 44 and 84 on a line ticked every 5 need step 1"},
    "tick": {"type": "number", "description": "A short tick every so many units, as the paper's line has them (default: the step)"},
    "label": {"type": "number", "description": "A number every so many units, as the paper's line prints them (default: the tick); the "
             "builder widens it on a narrow phone while the numbers would touch"},
    "unit": {"type": "string", "description": "The line's quantity and unit, only when the paper's line names it ('Time (in minutes)')"},
    "tol": {"type": "number", "description": "How far from the memo's value still earns it, in the line's units (0: exactly the memo's value)"}}
BX_IDS = ["min", "q1", "med", "q3", "max"]
BOXPLOT = obj({
    "kind": {"type": "string", "const": "boxplot"}, **NL_SCALE,
    "at": obj({k: NUM for k in BX_IDS}, BX_IDS) | {"description": "The memo's five-number summary: min, q1 (the lower quartile), med (the "
                                                                "median), q3 (the upper quartile), max"},
    "crit": obj({k: INT for k in BX_IDS}, BX_IDS) | {"description": "Each value's memo criterion: the 0-based index into criteria. A criterion "
                                                                  "earns its marks only when ALL its values are right: the memo's '✓ min. & "
                                                                  "max. ✓ median ✓ Q1 and Q3' is min 0, max 0, med 1, q1 2, q3 2; '✓ box "
                                                                  "✓ whiskers ending at 5 & 120' is q1 0, med 0, q3 0, min 1, max 1. "
                                                                  "List them in the memo's order: the result chips follow it, and the "
                                                                  "first value of a criterion shows its marks"}},
    ["kind", "x", "tol", "at", "crit"])
NUMLINE = obj({
    "kind": {"type": "string", "const": "numline"}, **NL_SCALE,
    "shade": {"type": "string", "enum": ["left", "right", "between", "outside"], "description": "The memo's shading: 'left' or 'right' of ONE "
              "end (x < a, x ≥ a), 'between' two ends (a < x ≤ b), 'outside' two ends (x ≤ a or x > b)"},
    "ends": {"type": "array", "items": obj({"at": NUM, "closed": {"type": "boolean", "description": "true: a filled dot, the end is in the "
                                                                                                   "answer (≤, ≥); false: an open dot (<, >)"}},
                                           ["at", "closed"]),
             "description": "The memo's end: one for left / right, two for between / outside (any order)"},
    "crit": obj({"end": INT, "circle": INT, "shade": INT, "end0": INT, "end1": INT, "circle0": INT, "circle1": INT}, []) | {
        "description": "Each component's memo criterion: the 0-based index into criteria. 'end' is every end's place, 'circle' every end's "
                       "open or filled dot, 'shade' the shading; end0 / end1 / circle0 / circle1 one end (0 the LEFT one) where the memo "
                       "marks the ends apart. A criterion earns its marks only when ALL its components are right ('An open dot at −6 with "
                       "an arrow to the right', 1 mark: end 0, circle 0, shade 0); a component no criterion names is not marked"}},
    ["kind", "x", "tol", "shade", "ends", "crit"])
# a Venn diagram and a probability tree (2026-10-11, build-play.js "venn" and "tree"); the learner sees the frame only: the sets as the
# paper labels them; a tree's outcomes, stage names and how many branches leave each point
VN_SET = obj({"id": {"type": "string", "description": "The set's label as the paper prints it on its circle: ONE capital letter ('S', 'R')"},
              "name": {"type": "string", "description": "What the set is, in a word or two as the stem names it ('smartphone', 'rugby'): read "
                       "out with each region's name"}}, ["id"])
VENN = obj({
    "kind": {"type": "string", "const": "venn"},
    "sets": {"type": "array", "items": VN_SET, "description": "The 2 or 3 sets, in the order the paper names them (the first circle top "
             "left, the second top right, the third below)"},
    "outside": {"type": "boolean", "description": "true when the memo's diagram fills the region outside every circle (the learners in "
                "none of the sets); false when it leaves it empty ('all the learners take at least one')"},
    "unknown": {"type": "string", "description": "Only when the memo's diagram carries an unknown in a region ('x − 20', '26 − x', 'x'): its "
                "letter. Every region then takes a form (the number alone, x, x + n, x − n, n − x), so none points at the regions with x"},
    "regions": {"type": "array", "items": obj({
        "in": {"type": "string", "description": "The region: the ids of the sets it lies in, in the sets' order ('S' = S only, 'ST' = S "
               "and T, 'RV' = R and V only, 'RVC' = all three), or 'out' (outside every circle)"},
        "at": {"anyOf": [INT, STR], "description": "What the memo's diagram puts there: a whole number, or an expression in the unknown "
               "as the memo writes it: 'x', 'x − 20', 'x + 5', '26 − x'"},
        "crit": {"type": "integer", "description": "The memo criterion (0-based index into criteria) that marks this region; leave it "
                 "out for a region the memo does not mark (a value the stem gives: 'x in all three')"}}, ["in", "at"]),
        "description": "EVERY region of the diagram (3 or 7, plus 'out' when outside is true), in the memo's order of ticks: the "
                       "result chips follow it. A criterion earns its marks when ALL its regions are right ('✓ 3 ; 4 ; 5')"},
    "any": {**INTS, "description": "The criteria (indexes) the memo gives for ANY ONE of their regions ('✓ 14 or 12 or 15': one mark for "
            "any one of the three right)"}},
    ["kind", "sets", "outside", "regions"])
TR_BRANCH = {"id": {"type": "string", "description": "The branch's outcome: one of outcomes' ids"},
             "p": {"type": "string", "description": "Its probability as the memo writes it: '3/5' or '0,6' (any equal form earns it: 2/4 = "
                   "1/2 = 0,5)"},
             "crit": {"type": "integer", "description": "Only where a memo criterion marks THIS branch's probability alone ('✓ 18 (number "
                      "of yellow balls)': the Y branch, 18/32): its index"}}
TREE = obj({
    "kind": {"type": "string", "const": "tree"},
    "outcomes": {"type": "array", "items": obj({"id": {"type": "string", "description": "As the memo labels the branch: 'B', 'R'"},
                                                "name": {"type": "string", "description": "As the stem names it: 'blue'"}}, ["id"]),
                 "description": "The outcomes the stem defines, the choices on every branch"},
    "stages": {**STRS, "description": "The two stages' names, as the stem describes them: ['First marble', 'Second marble']"},
    "tree": {"type": "array", "items": obj({**TR_BRANCH, "next": {"type": "array", "items": obj(TR_BRANCH, ["id", "p"]),
                                                                  "description": "The branches after it, the second stage"}},
                                           ["id", "p", "next"]),
             "description": "The memo's tree, two stages: the first stage's branches, each with the branches after it. The learner sees "
                            "only how many branches leave each point; their order on the screen is free (paired by outcome)"},
    "crit": obj({"branches": INT, "p": INT, "p1": INT, "p2": INT, "out": INT}, []) | {
        "description": "Each memo criterion's index (into criteria): 'branches' every branch's outcome; 'p' every probability (or p1 / p2 "
                       "a stage's); 'out' every end's outcome, (B ; R), asked only when this is given. A criterion earns its marks when "
                       "ALL its components are right; a criterion no component names cannot be earned (flag it)"}},
    ["kind", "outcomes", "stages", "tree", "crit"])

COMPONENTS = {
    "mcq": component("mcq", "Pick ONE of 2-6 options.", {"opts": STRS, "a": {"type": "integer", "description": "0-based index of the right option"},
                                                       "optTable": obj({"head": STRS, "rows": {"type": "array", "items": STRS}}, ["head", "rows"]) | {
                                                           "description": "Only when the paper prints the options as a TABLE: its column heads, and one row of cells per option in the order of opts (opts then reads each row as a line)"},
                                                       "figure": {**FIGURE, "description": "Only when the paper prints a figure for THIS one question (not the whole block)"},
                                                       "ab": obj({"a": STR, "b": STR}, ["a", "b"]) | {
                                                           "description": "Only for COLUMN I / COLUMN II (A only, B only, both A and B, none): COLUMN II's two items; opts are then exactly "
                                                                          "['A only', 'B only', 'Both A and B', 'None'] and q is COLUMN I's description"}}, ["opts", "a"]),
    "pickn": component("pickn", "Pick N of several options.", {"opts": STRS, "pool": {**INTS, "description": "0-based indexes of every right option"}, "count": INT}, ["opts", "pool", "count"]),
    "order": component("order", "Put the options in sequence.", {"opts": STRS, "a": {**INTS, "description": "option indexes in the right order"}}, ["opts", "a"]),
    "match": component("match", "Match each COLUMN A item to ONE COLUMN B description (more descriptions than items, e.g. A-J for five terms), "
                       "or classify each item into one of a few groups (micro / market / macro environment).", {
        "left": {**STRS, "description": "COLUMN A's items (or the items to classify), in the paper's order"},
        "right": {**STRS, "description": "COLUMN B's descriptions (or the groups), in the paper's order (A, B, C ...)"},
        "a": {**INTS, "description": "for each left item, the 0-based index of its right item"},
        "each": {**INT, "description": "marks per pair when one pair is worth more than 1 (1.3: 5 x 2)"},
        "heads": {**STRS, "description": "Only when the paper titles the two sides otherwise than COLUMN A / COLUMN B: the two titles"},
        "groups": {"type": "boolean", "description": "true when the right items are GROUPS that several left items may share (classifying); "
                                                     "absent: a one-to-one match, each right item used at most once"}}, ["left", "right", "a"]),
    "term": component("term", "One term or short phrase (one line).", {
        "a": {**STRS, "description": "Every answer the memo accepts, first the memo's own wording"},
        "reject": {**STRS, "description": "Real terms one or two letters away that are WRONG (e.g. 'complete dominance' for 'incomplete dominance')"},
        "strict": {"type": "boolean", "description": "true when ANY letter changes the meaning, so no spelling slip is forgiven: IUPAC names "
                                                    "(hexane / hexene), formulas (H2SO4 / H2SO3), cell notation. Letters and digits must match in "
                                                    "order; spacing and punctuation are free. List every accepted form in a"}}, ["a"]),
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
    "genotype": component("genotype", "COUNT genotypes built from the paper's alleles (never typed: case and superscripts are exact, DD is never dd).", {
        "alleles": {**STRS, "description": "Every allele of the system as printed, dominant first (['D', 'd'], ['Iᴬ', 'Iᴮ', 'i'], ['Xᴴ', 'Xʰ', 'Y'])"},
        "count": INT,
        "pool": {"type": "array", "items": STRS, "description": "Every genotype the memo accepts, each as its alleles (['Iᴮ', 'i']; a dihybrid's four, ['R', 'R', 'e', 'e'])"},
        "per": {"type": "integer", "description": "Alleles per genotype: 2 (default) or 4 (a dihybrid, RRee)"}},
        ["alleles", "count", "pool"]),
    "num": component("num", "One number (keypad), within a tolerance.", {"a": NUM, "tol": NUM, "unit": STR}, ["a", "tol"]),
    "steps": component("steps", "A calculation in numbered steps, each one NUMBER (method marks per step).", {
        "steps": {"type": "array", "items": obj({"id": STR, "label": STR, "marks": INT, "a": NUM, "tol": NUM,
                                                  "memo": {"type": "string", "description": "the memo's working for this step"},
                                                  "also": {"type": "array", "items": NUM, "description": "Other values that earn the step, each within "
                                                           "tol: only when the memo's own value is a slip the paper contradicts and the right one "
                                                           "must not lose the mark (ML P1 Nov 2024 5.1.5: lakh crore converted with one crore)"}},
                                                 ["id", "label", "marks", "a", "tol", "memo"])}}, ["steps"]),
    "rubric": component("rubric", "A written answer marked against the memo's points (Explain / Describe / State ...).", {
        "bullets": {**STRS, "description": "The memo's marking points, one per mark (or per 'each'). An alternative answer starts 'OR — '"},
        "each": {"type": "integer", "description": "Marks per point when one point is worth more than 1"},
        "worth": {**INTS, "description": "Each point's own marks, one per bullet, when points differ (the memo's 'Force (2) + Motivation (1)': "
                  "the name and its quote as two points worth [2, 1]); overrides each"},
        "notes": {**STRS, "description": "The memo's marking NOTES that are not points (key-word rules, 'X defined: 0/2', ACCEPT limits, criteria): never scored and never shown to the learner; a note in bullets would be a point a learner earns"},
        "table": {**STRS, "description": "Tabulate: the table's column headings (the things compared, in the paper's order); the answer is played as that table, one row per difference the question asks for"},
        "must": {**INTS, "description": "0-based indexes of COMPULSORY points (the memo's 'Compulsory mark * (1) + Any (5)'): each earns its own "
                 "mark, and the other points together earn at most marks minus the compulsory ones"}}, ["bullets"]),
    "insight": component("insight", "An essay's insight (Business Studies LASO: Layout, Analysis, Synthesis, Originality, 2 each), never answered: "
                         "worked out from the essay's own sections (written answers as statements, 2026-10-10).", {
        "of": {**STRS, "description": "the essay's section parts (their numbers), introduction to conclusion"},
        "intro": {**STR, "description": "the introduction part's number"}, "conclusion": {**STR, "description": "the conclusion part's number"},
        "examples": {"type": "array", "items": {"type": "array", "prefixItems": [STR, INT], "minItems": 2, "maxItems": 2},
                     "description": "[part number, option index] of each EXAMPLE statement (recent, real): Originality, 1 each, 2 at most"}},
        ["of", "intro", "conclusion"]),
    "draw": component("draw", "No catalogue type fits (a drawing, a graph to plot, a structured essay ...): the learner answers on paper and self-checks against the memo's criteria. Flag it no_fit.", {
        "criteria": {"type": "array", "items": obj({"text": STR, "marks": INT}, ["text", "marks"])},
        "build": {"anyOf": [
            obj({"kind": {"type": "string", "const": "hist"}, "want": {"type": "string", "enum": ["histogram", "bar", "line"]},
                 "groups": STRS, "answers": {"type": "array", "items": NUM}, "tol": NUM, "top": NUM, "steps": {"type": "array", "items": NUM},
                 "okSteps": {"type": "array", "items": NUM}, "snap": NUM, "x": STRS, "y": STRS, "capWords": {"type": "array", "items": STRS},
                 "typeQ": STR, "typeHint": STR, "unit": STR},
                ["kind", "want", "groups", "answers", "tol", "top", "steps", "okSteps", "x", "y", "capWords"]) | {
                "description": "Only when the paper asks to DRAW a bar graph / histogram / line graph the memo marks by T C L S P: the graph is BUILT on the phone step by step. want: the right type; groups: the X categories in order; answers: each group's value; x / y: the axis label choices, the right one FIRST; capWords: groups of words, the caption needs one word from each; okSteps: Y-axis steps the memo accepts"},
            obj({"kind": {"type": "string", "const": "cross"}, "alleles": STRS, "phenos": STRS,
                 "parents": {"type": "array", "items": obj({"pheno": STR, "geno": STRS}, ["pheno", "geno"])},
                 "offspring": {"type": "array", "items": obj({"geno": STRS, "pheno": STR}, ["geno", "pheno"])},
                 "gens": {**STRS, "description": "The generations' labels as the memo marks them: default ['P1', 'F1']; ['P2', 'F2'] for a cross of a second generation"}},
                ["kind", "alleles", "phenos", "parents", "offspring"]) | {
                "description": "Only for a MONOHYBRID genetic cross the memo marks P1 phenotypes, P1 genotypes, gametes, F1 genotypes, F1 phenotypes, ratio (compulsory), P1/F1, meiosis/fertilisation: BUILT on a Punnett square. alleles: the system's alleles; phenos: every phenotype the stem names; parents: the two P1 parents; offspring: EVERY possible genotype with its phenotype. The criteria keep the memo's 8 points"},
            SKETCH | {"description": "Only for 'Sketch / Draw the graph of f' the memo marks by its features (intercepts, turning points, "
                                     "asymptotes, a point, the shape): BUILT on a grid, the learner placing each feature, the curve drawn "
                                     "through them. Every criterion becomes features (or the shape) whose marks add up to the part's; a "
                                     "criterion no feature can earn ('smooth curve') is flagged. The criteria keep the memo's own text"},
            BOXPLOT | {"description": "Only for 'Draw a box and whisker diagram' the memo marks by its values (min & max / the whiskers, the "
                                      "median, Q1 and Q3 / the box): BUILT on the paper's scaled line, the learner placing the five values, "
                                      "the box and whiskers drawn from them. Each memo criterion names the values it needs (crit); its "
                                      "marks come from criteria, in the memo's order. The criteria keep the memo's own text"},
            NUMLINE | {"description": "Only for 'Represent the answer (an inequality or interval) on a number line': BUILT on a number line, "
                                      "the learner choosing the shading, placing each end and choosing its dot (open or filled). Each memo "
                                      "criterion names the components it needs (crit); its marks come from criteria. Keep the part's 'after' "
                                      "when the inequality is an earlier part's answer"},
            VENN | {"description": "Only for 'Draw / Represent the information in a Venn diagram' (two or three sets): BUILT, the learner "
                                   "filling each region (a number, or a form in the unknown where the memo's diagram has one: x − 20). "
                                   "Each region names its memo criterion (crit); its marks come from criteria. The criteria keep the "
                                   "memo's own text"},
            TREE | {"description": "Only for 'Draw a tree diagram' (two stages) the memo marks by its branches, probabilities and outcomes: "
                                   "BUILT, the branches drawn, the learner choosing each branch's outcome, typing its probability and, "
                                   "where crit has 'out', choosing each end's outcome. The criteria keep the memo's own text"}]},
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
    "sections": {"type": "array", "items": obj({"title": STR, "total": INT, "missions": {"type": "array", "items": MISSION},
                                                "answer_any": {**INT, "description": "Only for a section that says 'Answer any N questions': N. Its questions "
                                                               "are the missions' first numbers (2.x, 3.x, 4.x); the total is N questions' marks"}},
                                               ["title", "total", "missions"])},
    "flags": {"type": "array", "items": FLAG}}, ["catalog", "paper", "sections", "flags"])


def catalog():
    return {"catalogId": CATALOG_ID, "title": "Nexera exam-practice question types",
            "components": {k: {"description": c["description"], "props": c["schema"]} for k, c in COMPONENTS.items()}}


if __name__ == "__main__":
    out = HERE / "catalog"; out.mkdir(exist_ok=True)
    (out / "nexera-exam-catalog.v1.json").write_text(json.dumps(catalog(), indent=1), encoding="utf-8")
    (out / "paper.schema.json").write_text(json.dumps(PAPER, indent=1), encoding="utf-8")
    print("wrote", len(COMPONENTS), "components ->", out)
