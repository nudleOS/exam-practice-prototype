"""Life Sciences P1 Nov 2025, hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks and answers are the paper's and the memo's own; the clues and
the figure captions (alt text) are ours. No API call: the transcription is the source, kept in git (out/ is not).
2025 papers first, 2024 stays playable (Murci, 2026-10-06).

  python tools/ingest/transcribe_ls_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Life Sciences P1 Nov 2025 Eng.pdf" "<...>/Life Sciences P1 Nov 2025 MG Eng.pdf" --id ls-p1-2025-11 --from-json
  then open Exam Practice.dc.html?ingested=ls-p1-2025-11&paper=ls-p1-2025-11&play=0

Figure boxes are measured in PDF points on the A4 page (595 x 842) and stored as fractions."""
import json
from pathlib import Path

W, H = 595.0, 842.0
box = lambda x0, y0, x1, y1: [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)]
fig = lambda page, b, caption: {"page": page, "bbox": box(*b), "caption": caption}
mcq = lambda n, q, opts, a, clues, **kw: {"t": "mcq", "n": n, "marks": 2, "q": q, "clues": clues, "opts": opts, "a": a, **kw}
mcq1 = lambda n, q, opts, a, clues: {"t": "mcq", "n": n, "marks": 1, "q": q, "clues": clues, "opts": opts, "a": a}
term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
lst = lambda n, q, count, marks, pool, clues: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
rub = lambda n, q, marks, bullets, clues, **kw: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **kw}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
AB = ["A only", "B only", "Both A and B", "None"]
# Column I / Column II (1.3): the description is the stem, COLUMN II's two items are `ab` (the Venn layout draws them as its two circles)
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})

FEMALE = fig(4, (202, 125, 442, 351), "The female reproductive system, front view. P labels the tube curving out to the upper right; S the "
             "hollow middle of the pear-shaped organ; Q, two lines to the thick wall lining it; R the narrow passage at the bottom.")
q11 = [
    mcq("1.1.1", "The hormone that prepares the body for an emergency is …", ["aldosterone.", "progesterone.", "adrenalin.", "prolactin."], 2,
        ["Think of the 'fight or flight' response.", "It comes from the adrenal glands and speeds up the heart."]),
    mcq("1.1.2", "Which ONE of the following are functions of the placenta?",
        ["Excretion and nutrition", "Gaseous exchange and protection against mechanical injury", "Nutrition and temperature regulation",
         "Temperature regulation and excretion"], 0,
        ["The placenta is an exchange organ between mother and foetus.", "The amniotic fluid, not the placenta, cushions and keeps the temperature."]),
    mcq("1.1.3", "The table below shows the reaction time of four learners to a stimulus. Which ONE of the following learners demonstrates the "
        "fastest response to the stimulus?", ["Temisha", "Luke", "Anika", "Jordy"], 3,
        ["The fastest response takes the least time.", "Find the smallest reaction time in the table."],
        optTable={"head": ["NAME OF LEARNER", "REACTION TIME (SECONDS)"], "rows": [["Temisha", "0,7"], ["Luke", "0,6"], ["Anika", "0,8"], ["Jordy", "0,4"]]}),
    mcq("1.1.4", "A high level of thyroxin in the blood will stimulate the …",
        ["pituitary gland to secrete less TSH.", "thyroid gland to secrete more TSH.", "pituitary gland to secrete more TSH.",
         "thyroid gland to secrete more thyroxin."], 0,
        ["This is a negative feedback: the response reverses the change.", "Which gland makes TSH, and should it make more or less now?"]),
    # options printed as a TABLE: optTable carries it; opts read each row as a line (the medal card, the memo)
    mcq("1.1.5", "Which ONE of the following combinations is CORRECT for a normal pregnancy?",
        ["Fertilisation in P · implantation in S", "Fertilisation in S · implantation in Q", "Fertilisation in P · implantation in Q",
         "Fertilisation in R · implantation in P"], 2,
        ["The ovum meets the sperm soon after it leaves the ovary.", "The embryo sinks into the thick lining of the uterus."],
        figure=FEMALE, optTable={"head": ["SITE OF FERTILISATION", "SITE OF IMPLANTATION"], "rows": [["P", "S"], ["S", "Q"], ["P", "Q"], ["R", "P"]]}),
    mcq("1.1.6", "In which part does the zygote develop into a morula?", ["S", "Q", "R", "P"], 3,
        ["The zygote divides while it is still travelling.", "Where is it before it reaches the uterus?"], figure=FEMALE),
    mcq("1.1.7", "The following is a list of male reproductive parts: (i) Prostate gland (ii) Seminal vesicle (iii) Urethra (iv) Cowper's gland. "
        "Which ONE of the following combinations is responsible for the formation of semen?",
        ["(i) and (ii) only", "(i), (ii) and (iv) only", "(ii) and (iii) only", "(i) and (iv) only"], 1,
        ["Semen is sperm plus fluids from glands.", "Which of the four is a passage, not a gland?"]),
    mcq("1.1.8", "The diagram below represents a human sperm. This sperm is NOT structurally suitable for fertilisation because of the …",
        ["absence of a nucleus to provide genetic material.", "absence of an acrosome to improve motility.",
         "presence of a long tail for the movement of the sperm.", "absence of mitochondria to provide energy."], 3,
        ["Check each option against what is drawn, and whether its reason is right.", "Look closely at the middle piece: what normally fills it?"],
        figure=fig(5, (192, 116, 450, 221), "A human sperm: a long thin tail on the left, a smooth middle piece with nothing drawn inside it, and a "
                   "round head on the right with a dark nucleus.")),
    mcq("1.1.9", "The following is a list of growth responses in plants: (i) Plants grow straight upwards (ii) No upward growth (iii) Increased "
        "number of lateral branches (iv) Stems bend towards unilateral light. Which ONE of the following combinations describes the growth "
        "responses that occur when apical buds of plants are removed?",
        ["(i), (ii) and (iii) only", "(ii) and (iii) only", "(i) and (iv) only", "(i), (ii), (iii) and (iv)"], 1,
        ["The apical bud makes auxins that keep the side buds dormant.", "Without it, does the plant still grow up, or out?"]),
    mcq("1.1.10", "Which ONE of the following is CORRECT for a person who exercises on a hot day without taking in any liquids?",
        ["Increased ADH secretion and increased permeability of renal tubules", "Increased ADH secretion and the production of dilute urine",
         "Decreased ADH secretion and increased permeability of renal tubules", "Decreased ADH secretion and the production of concentrated urine"], 0,
        ["The body is losing water through sweat.", "ADH makes the tubules take back more water."]),
]
q12 = [
    term("1.2.1", "The ovarian hormone that is secreted by the corpus luteum", ["progesterone"],
         ["It keeps the uterus lining ready for pregnancy.", "Its name means 'for gestation'."]),
    term("1.2.2", "The eye defect that is characterised by a cloudy lens", ["cataracts", "cataract"],
         ["It is common in older people.", "The lens turns milky."]),
    term("1.2.3", "The production of ova by meiosis", ["oogenesis"], ["Gametogenesis, named after the female gamete.", "'Oo' means egg."]),
    term("1.2.4", "The part of the retina that contains no rods and cones", ["blind spot"],
         ["The optic nerve leaves the eye here.", "An image falling here is not seen."]),
    term("1.2.5", "The release of an ovum from the ovary", ["ovulation"], ["It happens around day 14 of the cycle.", "The follicle bursts."]),
    term("1.2.6", "The extra-embryonic membrane that plays a role in the formation of the placenta", ["chorion"],
         ["It is the outermost membrane around the embryo.", "Its villi grow into the uterus wall."]),
    term("1.2.7", "A plant hormone responsible for seed dormancy", ["abscisic acid", "ABA"],
         ["It is the plant's 'stress' and 'wait' hormone.", "It also makes leaves fall."]),
    term("1.2.8", "The maintenance of a constant internal environment within narrow limits", ["homeostasis"],
         ["'Homeo' means the same.", "It keeps temperature, glucose and water steady."]),
]
q13 = [
    abq("1.3.1", "The hormone responsible for the development of secondary sexual characteristics during puberty", "Oestrogen", "Testosterone", 2,
        ["Think of both sexes at puberty.", "Which hormone does each sex rely on?"]),
    abq("1.3.2", "Plays a role in the pupillary mechanism", "Ciliary muscles", "Radial muscles", 1,
        ["The pupillary mechanism changes the size of the pupil.", "Which muscles are in the iris, and which change the lens?"]),
    abq("1.3.3", "A plant defence mechanism", "Thorns", "Chemicals", 2,
        ["Plants defend themselves physically and chemically.", "Is each one a way to stop an animal eating the plant?"]),
]
LETS3 = ["A", "B", "C"]
q14 = [
    mcq1("1.4.1(a)", "Give the LETTER of the diagram that represents a response due to abscisic acid", LETS3, 2,
         ["Abscisic acid is linked to leaves falling.", "Which diagram shows a leaf dropping off?"]),
    {"t": "pickn", "n": "1.4.1(b)", "marks": 2, "q": "Give the LETTERS of the diagrams that represent a response due to auxins",
     "clues": ["Auxins cause bending growth: towards light, and of roots downwards.", "Two diagrams show a part bending."], "opts": LETS3, "pool": [0, 1], "count": 2},
    mcq1("1.4.1(c)", "Give the LETTER of the diagram that represents a response due to gibberellins", LETS3, 0,
         ["Gibberellins break seed dormancy.", "Which diagram shows seeds starting to grow?"]),
    term("1.4.2(a)", "Identify the growth response shown by the roots in diagram A", ["geotropism", "gravitropism", "positive geotropism", "positive gravitropism"],
         ["The roots respond to a force that pulls downwards.", "'Geo' means earth."]),
    term("1.4.2(b)", "Identify the growth response shown in diagram B", ["phototropism", "positive phototropism"],
         ["The stem grows towards the gap where light comes in.", "'Photo' means light."]),
    mcq1("1.4.3(a)", "Using X and Y in diagram B, state which side of the stem has the highest concentration of auxins", ["X", "Y"], 0,
         ["Light moves auxins away from the lit side.", "Which side is in the shade?"]),
    mcq1("1.4.3(b)", "Using X and Y in diagram B, state which side of the stem has the highest rate of cell division", ["X", "Y"], 0,
         ["More auxin means more growth on that side.", "The stem bends away from the side that grows more."]),
]
LETS6 = ["A", "B", "C", "D", "E", "F"]
q15 = [
    term("1.5.1", "Name the type of neuron represented by the diagram.", ["sensory neuron", "sensory neurone", "sensory", "afferent neuron"],
         ["Look at where the cell body sits: off to the side on a stalk.", "Which neuron carries impulses from a receptor?"]),
    term("1.5.2(a)", "Identify part B", ["axon"], ["It is the long fibre the impulse runs along.", "It carries the impulse away from the cell body."]),
    term("1.5.2(b)", "Identify part D", ["cell body", "cyton", "soma"], ["It holds the nucleus.", "It is the round part on the stalk."]),
    term("1.5.2(c)", "Identify part E", ["dendrite", "dendrites"], ["Branches that pick up the impulse.", "The impulse starts at this end."]),
    mcq1("1.5.3(a)", "Give the LETTER of the part that contains the genetic material of the neuron", LETS6, 2,
         ["Genetic material is in the nucleus.", "Find the dark dot."]),
    mcq1("1.5.3(b)", "Give the LETTER of the part that insulates the neuron", LETS6, 5,
         ["The insulation wraps the fibre in segments.", "It speeds the impulse up."]),
    mcq1("1.5.3(c)", "Give the LETTER of the part that makes synaptic contact with an interneuron", LETS6, 0,
         ["A synapse is where the impulse leaves this neuron.", "Follow the arrow to the end the impulse reaches."]),
    term("1.5.4", "Name the disorder that is associated with the degeneration of part F.", ["multiple sclerosis", "MS"],
         ["Part F is attacked and scars form.", "Its name means 'many scars'."]),
]
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 8,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "A, B, both or none", "marks": 6,
     "lead": "Indicate whether each of the descriptions in COLUMN I apply to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.", "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Plant hormones", "marks": 8,
     "lead": "The diagrams below represent different plant responses caused by hormones.", "items": q14,
     "figure": fig(7, (160, 112, 487, 447), "Three diagrams. Diagram A: three stages of a seed in the soil, its root growing downwards and its "
                   "shoot upwards. Diagram B: a potted plant inside a closed box with a gap in its right-hand wall; the stem curves up and to the "
                   "right towards the gap, with X above the curve of the stem and Y below it. Diagram C: three stages of a plant, its leaves "
                   "dropping off one by one; in the last, a leaf lies on the ground.")},
    {"id": "1.5", "title": "Question 1.5", "kind": "The neuron", "marks": 8, "lead": "The diagram below shows the structure of a neuron.", "items": q15,
     "figure": fig(8, (154, 113, 459, 295), "A neuron, with an arrow under it: 'Direction of impulse', from right to left. E points to the branches "
                   "at the right-hand end; a round body sits above the fibre on a short stalk, C pointing to the dark dot inside it and D a bracket "
                   "beside it; F points to one of the sausage-shaped segments wrapping the fibre on the right; B to the long fibre on the left; "
                   "A to the knobbed ends at the left-hand end.")},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2025", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "Question 1 (Section A) hand-transcribed from the paper and memo PDFs; no API call. Section B is not in yet."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p1-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Question 1"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]))
