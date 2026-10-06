"""Life Sciences P1 Nov 2025, the whole paper (Questions 1 to 3), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
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

# ---- Section B: Questions 2 and 3, from the question paper pages 9-16 and the memo pages 5-9 ----
# (a list scores an answer that holds the FIRST WORD of an accepted answer: each accepted answer leads with a word only that point uses)
ln = lambda n, q, letters, letter, names, clues: {"t": "lettername", "n": n, "marks": 2, "q": q, "clues": clues, "letters": letters, "a": {"letter": letter, "name": names}}
q21 = [
    rub("2.1.1", "Explain why we may conclude that ducks display precocial development.", 3,
        ["The egg has a high percentage of yolk", "therefore it contains more energy / nutrients", "the hatchling will be well developed",
         "making it more independent"],
        ["Find the duck's yolk percentage in the table: high or low?", "What does a lot of yolk let the chick become before it hatches?"], must=[0]),
    lst("2.1.2", "Name the THREE bird types that would have a higher degree of parental care.", 3, 3, [["eagle"], ["vulture"], ["pigeon"]],
        ["More parental care goes with less developed chicks.", "Look for the three lowest yolk percentages."]),
    rub("2.1.3", "Give a reason for your answer to QUESTION 2.1.2.", 2,
        ["The eggs have a lower percentage of yolk", "therefore the hatchlings will not be fully developed"],
        ["Compare their yolk percentages with the others'.", "Less yolk: how developed is the chick when it hatches?"]),
]
q22 = [
    ln("2.2.1(a)", "Give the LETTER and the NAME of the gland that secretes testosterone", ["A", "B", "C"], "C", ["testis", "testes", "testicle"],
       ["Testosterone is made where sperm are made.", "It is the large organ inside the scrotum."]),
    ln("2.2.1(b)", "Give the LETTER and the NAME of the part that stores sperm until maturation", ["A", "B", "C"], "A", ["epididymis"],
       ["Sperm wait here before they leave the testis.", "It sits like a cap on top of the testis."]),
    rub("2.2.2", "Explain the role of the scrotum in sperm production.", 2,
        ["It maintains the temperature of the testes lower than body temperature", "to ensure the production of good quality / quantity of sperm",
         "OR — It protects the testes from mechanical injury", "to ensure the production of good quality / quantity of sperm"],
        ["Why do the testes hang outside the body?", "Sperm are made best a little below body temperature."]),
    rub("2.2.3", "Name and describe the process of sperm production.", 5,
        ["Spermatogenesis", "under the influence of testosterone", "diploid cells", "in the seminiferous tubules / testes", "undergo meiosis",
         "to form haploid sperm cells"],
        ["Name the process first: gametogenesis named after the male gamete.", "Then: which hormone, which cells, where, which division, what forms."], must=[0]),
]
q23 = [
    rub("2.3.1(a)", "Referring to ovarian hormones, explain the decrease in thickness of the endometrium from day 0 to day 7", 3,
        ["The corpus luteum degenerates", "therefore the progesterone levels decrease", "the endometrium is no longer maintained / menstruation occurs"],
        ["Which ovarian hormone keeps the lining in place?", "What happens to its source at the end of a cycle?"]),
    rub("2.3.1(b)", "Referring to ovarian hormones, explain the increase in thickness of the endometrium from day 7 to day 14", 2,
        ["The Graafian follicle secretes", "oestrogen, which increases the endometrium thickness"],
        ["A new follicle is growing in this part of the cycle.", "Which hormone does it make, and what does it do to the lining?"]),
    rub("2.3.2", "Describe changes in the endometrium that cause it to become thicker.", 2, ["It becomes more vascular", "and more glandular"],
        ["Think of what grows into the lining.", "Blood vessels, and what else?"]),
    rub("2.3.3", "State the significance of the change in endometrium thickness described in QUESTION 2.3.2.", 1,
        ["It allows for implantation of the embryo / the development of the placenta / increased blood supply to nourish the embryo"],
        ["Why does the uterus prepare a thick lining?", "What might arrive and sink into it?"]),
    {"t": "draw", "n": "2.3.4", "marks": 6, "q": "Draw a bar graph to show the results in the table.",
     "clues": ["Each day is its own bar: a bar graph's bars stand apart.", "The days go along the bottom, the thickness up the side."],
     "criteria": [{"text": "Type of graph: a bar graph is drawn", "marks": 1}, {"text": "Caption includes both variables", "marks": 1},
                  {"text": "Correct labels for the X-axis and Y-axis, and the unit for the Y-axis", "marks": 1},
                  {"text": "Equal space and width of bars on the X-axis, and a correct scale for the Y-axis", "marks": 1},
                  {"text": "Plotting: 1–4 co-ordinates correct (1), all 5 correct (2)", "marks": 2}],
     # built step by step, one memo criterion a step (T C L S P), as June's histogram (Exam Practice's graph builder)
     "build": {"kind": "hist", "want": "bar", "groups": ["0", "7", "14", "21", "28"], "answers": [14, 3, 5, 13, 16], "tol": 0.5, "top": 20,
               "steps": [1, 2, 5, 10], "okSteps": [1, 2, 5], "snap": 1, "unit": "days",
               "x": ["Day of the menstrual cycle", "Thickness of the endometrium (mm)", "Endometrium"],
               "y": ["Thickness of the endometrium (mm)", "Day of the menstrual cycle", "Menstrual cycle"],
               "capWords": [["day", "cycle"], ["thick", "endometri"]],
               "typeQ": "Which graph shows separate days against a measurement?",
               "typeHint": "A histogram's bars touch for groups that run on; a bar graph's stand apart."}},
]
q24 = [
    term("2.4.1", "Name the part of the brain that controls thermoregulation.", ["hypothalamus"],
         ["It is the brain's thermostat.", "It sits just above the pituitary gland."]),
    mcq1("2.4.2", "Give the LETTER of the diagram which represents the arteriole on a cold day.", ["X", "Y", "Z"], 0,
         ["On a cold day the body keeps heat in.", "Less blood near the skin: a narrower arteriole."]),
    rub("2.4.3", "Explain the significance of the change in the diameter of the arteriole from normal conditions to the condition in diagram Z.", 4,
        ["The arteriole dilates / vasodilation takes place", "more blood flows to the surface of the skin", "and more heat is lost / more radiation occurs",
         "to decrease / regulate the body temperature"],
        ["Did the arteriole get wider or narrower from Y to Z?", "More blood near the skin: what happens to the body's heat?"]),
]
q25 = [
    lst("2.5.1", "State the dependent variable of this investigation.", 1, 1, [["height (of the boys)"]],
        ["What was measured every month?", "It is what the growth hormone was expected to change."]),
    lst("2.5.2", "List THREE variables that were kept constant and which contributed to the validity of the investigation.", 3, 3,
        [["gender (only boys took part)", "boys", "male"], ["ISS (all the boys had ISS)", "idiopathic", "stature"],
         ["two-year-old (all the boys were the same age)", "2-year", "aged"], ["duration (of the investigation)", "until 18", "18 years", "period"]],
        ["What did all the participants have in common?", "Think of who they were, what condition they had, how old, and for how long."]),
    rub("2.5.3", "Explain the purpose of Group B in this investigation.", 2,
        ["To prove that it is the added growth hormone that caused the change in height and not any other factor"],
        ["Group B is the control.", "A control lets you say what caused the difference."], each=2),
    {"t": "steps", "n": "2.5.4", "marks": 3,
     "q": "Calculate the daily amount of added human growth hormone that was given to a boy with a mass of 25 kg. Show ALL your working, INCLUDING the correct unit.",
     "clues": ["The dosage is per kg of body weight.", "Multiply the dosage by the boy's mass."],
     "steps": [{"id": "s1", "label": "Daily amount: 25 × 0,028 (mg)", "marks": 3, "a": 0.7, "tol": 0.005, "memo": "25 × 0,028 ✓ = 0,7 ✓ mg ✓"}]},
    rub("2.5.5", "Give a conclusion for this investigation.", 2, ["Added growth hormone causes an increase in height of children with ISS"],
        ["A conclusion answers the aim.", "What did the growth hormone do to the boys' height?"], each=2),
]
q31 = [
    term("3.1.1(a)", "Identify fluid A", ["aqueous humour", "aqueous humor", "aqueous"], ["It fills the space behind the cornea.", "It is watery."]),
    term("3.1.1(b)", "Identify part B", ["pupil"], ["It is the opening in front of the lens.", "Light passes through it."]),
    term("3.1.1(c)", "Identify part C", ["iris"], ["It surrounds the opening.", "Its muscles change the opening's size."]),
    rub("3.1.2", "Describe the appearance of the cornea of an eye with astigmatism.", 1, ["It is not evenly curved / rounded"],
        ["Compare the two corneas.", "Is the curve the same all round?"]),
    rub("3.1.3", "Explain how astigmatism affects vision.", 3,
        ["The light is refracted unevenly / in different directions", "and does not focus on the retina", "forming a blurred image"],
        ["The cornea bends light.", "If its curve is uneven, where does the light go?"]),
    lst("3.1.4", "Give ONE treatment for astigmatism.", 1, 1, [["laser"], ["surgery", "operation"], ["glasses", "spectacles", "lenses", "contact"]],
        ["It can be corrected, not cured by medicine.", "Think of what an optometrist offers."]),
]
LETS5 = ["A", "B", "C", "D", "E"]
q32 = [
    term("3.2.1", "Name the branch of the nervous system represented by the parts shown.", ["central nervous system", "CNS"],
         ["The brain and the spinal cord together.", "It is the central branch."]),
    ln("3.2.2(a)", "Give the LETTER and NAME of the part responsible for balance and coordination", LETS5, "B", ["cerebellum"],
       ["It is at the back, below the large folded part.", "Its name means 'little brain'."]),
    ln("3.2.2(b)", "Give the LETTER and NAME of the part responsible for control of breathing", LETS5, "C", ["medulla oblongata", "medulla"],
       ["It joins the brain to the spinal cord.", "It controls what you do without thinking: heart rate, breathing."]),
    ln("3.2.2(c)", "Give the LETTER and NAME of the part responsible for control of skeletal muscles", LETS5, "A", ["cerebrum"],
       ["Voluntary movement is controlled here.", "It is the largest part of the brain."]),
    rub("3.2.3", "Describe the pathway of an impulse from part D through the spinal cord to part E, to bring about a reflex action.", 6,
        ["The impulse is transmitted by the sensory neuron", "via the dorsal root of the spinal nerve", "to the interneuron", "and to the motor neuron",
         "by synaptic contact", "It is then transmitted via the ventral root of the spinal nerve", "to the effector, which brings about the reflex action"],
        ["Follow the arrows: in at D, out at E.", "Sensory, then inter, then motor neuron: through which roots?"]),
]
q34 = [
    term("3.4.1(a)", "Identify part A", ["pinna", "auricle"], ["It is the outer flap.", "It collects sound."]),
    term("3.4.1(b)", "Identify part B", ["ossicles", "ossicle", "hammer, anvil and stirrup", "malleus, incus and stapes"],
         ["Three small bones.", "They pass vibrations across the middle ear."]),
    {"t": "pickn", "n": "3.4.2", "marks": 2, "q": "Give the LETTERS of TWO parts that are normally filled with fluid.",
     "clues": ["The inner ear is filled with fluid.", "One part is for balance, one for hearing."], "opts": LETS5, "pool": [2, 3], "count": 2},
    rub("3.4.3", "Describe how balance is restored when there is a change in the speed and direction of head movement.", 5,
        ["The cristae are stimulated", "and convert the stimulus to an impulse", "which is sent via the auditory nerve", "to the cerebellum for interpretation",
         "Impulses are then sent to the skeletal muscles to restore balance"],
        ["Speed and direction changes are sensed in the semicircular canals.", "Receptor, nerve, brain, then muscles."]),
    rub("3.4.4(a)", "Explain how damage to the hair cells in the organ of Corti can lead to hearing loss", 2,
        ["Fewer / no stimuli will be converted into impulses", "Fewer / no impulses will be sent to the cerebrum to be interpreted"],
        ["The hair cells are the hearing receptors.", "No receptor, no impulse: where would it have gone?"]),
    rub("3.4.4(b)", "Explain how earplugs can prevent damage to the hair cells in the organ of Corti", 3,
        ["The earplugs limit the sound waves in the auditory canal / reaching the tympanic membrane", "Fewer vibrations are formed in the middle ear",
         "Fewer pressure waves are formed in the cochlea to prevent damage"],
        ["Follow the sound in: canal, eardrum, bones, cochlea.", "Less sound in means less of what at each step?"]),
]
q35 = [
    term("3.5.1", "Name the organ that secretes insulin.", ["pancreas"], ["It also makes digestive juices.", "Its islets of Langerhans make the hormone."]),
    term("3.5.2", "State the number of meals that were eaten during the 23-hour period.", ["three", "3", "3 meals", "three meals", "nine", "9"],
         ["The healthy person's insulin rises after each meal.", "Count person A's peaks."]),
    # a TABLE the memo marks (1) for the table + (2 x 2) for two differences, each with both sides
    rub("3.5.3", "Tabulate TWO differences between long-acting insulin treatment and rapid-acting insulin treatment over the 23-hour period.", 5,
        ["Table with the two treatments as column headings", "Long-acting: one injection over 23 hours", "Rapid-acting: three injections over 23 hours",
         "Long-acting: the injection is given at 23:00", "Rapid-acting: an injection is given before every meal",
         "Long-acting: a lower concentration of insulin (10 units)", "Rapid-acting: a higher concentration of insulin (30 units)",
         "Long-acting: the concentration remains constant for long periods (20 hours)", "Rapid-acting: the concentration fluctuates",
         "Long-acting: takes 1 hour to reach its peak", "Rapid-acting: takes 2 hours to reach its peak"],
        ["Compare person C's line with person B's.", "Count the injections, see when they are given, and how high and steady each line is."]),
    term("3.5.4", "Name the type of insulin treatment that is similar to insulin secretion in a healthy person.",
         ["rapid-acting insulin", "rapid-acting", "rapid acting insulin", "rapid acting", "rapid-acting insulin treatment"],
         ["Which treated line rises and falls like person A's?", "It is given before each meal."]),
    rub("3.5.5", "Explain why person B may experience a lack of energy after receiving a rapid-acting insulin injection if NO meal is taken.", 2,
        ["The insulin will reduce the glucose level even further / glucose is converted to glycogen / cells take up more glucose",
         "There is less glucose available for cellular respiration"],
        ["Insulin lowers blood glucose.", "With no meal, what is left for respiration?"]),
]
missions_b = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Bird eggs", "marks": 8, "lead": "In bird eggs, the yolk is the main source of energy for the developing embryo.",
     "items": q21, "extract": "The table below provides information about the eggs of some bird types.",
     "table": {"head": ["Type of bird", "Average % of yolk in the egg"],
               "rows": [["Goose", "35,1"], ["Eagle", "12,0"], ["Duck", "35,4"], ["Vulture", "14,0"], ["Chicken", "31,9"], ["Pigeon", "17,9"]]}},
    {"id": "2.2", "title": "Question 2.2", "kind": "Male reproductive system", "marks": 11, "lead": "The diagram below shows a part of the male reproductive system.",
     "items": q22,
     "figure": fig(9, (216, 488, 412, 612), "A part of the male reproductive system inside the scrotum (labelled). C points to the large grey round "
                   "organ; A to the cap sitting on top of it; B to the tube leading up and away to the right.")},
    {"id": "2.3", "title": "Question 2.3", "kind": "The menstrual cycle", "marks": 14,
     "lead": "The thickness of the endometrium varies throughout the menstrual cycle of a female.", "items": q23,
     "extract": "The table below shows the results recorded for a woman who had her endometrial thickness monitored for a particular menstrual cycle.",
     "table": {"head": ["Day of the menstrual cycle", "Thickness of the endometrium (mm)"],
               "rows": [["0", "14"], ["7", "3"], ["14", "5"], ["21", "13"], ["28", "16"]]}},
    {"id": "2.4", "title": "Question 2.4", "kind": "Thermoregulation", "marks": 6,
     "lead": "The diagrams below represent the differences in the diameter of an arteriole (small artery) close to the surface of the skin. These "
             "differences are due to changes that occur during thermoregulation under different environmental conditions. Diagram Y shows the arteriole "
             "under normal conditions.", "items": q24,
     "figure": fig(11, (134, 160, 502, 323), "Three cross-sections of the arteriole, each a grey wall round a white opening. X: the narrowest "
                   "opening and the thickest wall. Y (normal conditions): in between. Z: the widest opening and the thinnest wall.")},
    {"id": "2.5", "title": "Question 2.5", "kind": "Growth hormone", "marks": 11,
     "lead": "Idiopathic Short Stature (ISS) describes a condition where children have normal birth height, but grow slowly and do not reach the "
             "expected height for their age group. This condition is NOT due to malnutrition or different lifestyles.", "items": q25,
     "extract": "Scientists investigated the effect of added growth hormone on the height of children with ISS.\n\nThe procedure was as follows:\n"
                "• Consent was obtained from the parents of a group of two-year-old boys with ISS.\n• The boys were divided into two groups.\n"
                "• The participants in Group A received human growth hormone at a daily dosage of 0,028 mg per kg of body weight.\n"
                "• The participants in Group B did not receive the hormone treatment.\n"
                "• The height of the participants was measured and recorded monthly until each participant reached the age of 18 years.\n\n"
                "At 18 years of age, the average height in Group A was 8 cm more than that in Group B."},
    {"id": "3.1", "title": "Question 3.1", "kind": "Astigmatism", "marks": 8,
     "lead": "The diagrams below represent the structure of a normal eye and that of an eye with astigmatism.", "items": q31,
     "figure": fig(13, (150, 152, 475, 356), "Two eyes in section, a normal eye on the left and an eye with astigmatism on the right. On the normal "
                   "eye, A points to the fluid-filled space at the front, behind the cornea; B to a bracket at the opening in front of the lens; C to "
                   "the part around that opening. The cornea of the eye with astigmatism has an irregular, uneven curve.")},
    {"id": "3.2", "title": "Question 3.2", "kind": "The nervous system", "marks": 13, "lead": "The diagrams below show parts of the human nervous system.",
     "items": q32,
     "figure": fig(14, (105, 114, 524, 437), "Left: the brain in section. A labels the large folded upper part; B the smaller folded part at the "
                   "back, below it; C the stalk joining the brain to the spinal cord (labelled). Right: a cross-section of the spinal cord with a "
                   "spinal nerve on each side; D is an arrow going in at the top right, E an arrow leaving at the bottom right.")},
    {"id": "3.3", "title": "Question 3.3", "kind": "Accommodation", "marks": 5, "lead": "",
     "items": [rub("3.3", "Describe how the human eye ACCOMMODATES for distant vision.", 5,
                   ["The ciliary muscles relax", "The suspensory ligaments become taut / tension on the lens increases", "The lens becomes less convex",
                    "causing light to be refracted less", "to form a clear image on the retina"],
                   ["Start with the muscles round the lens.", "For a distant object the lens must bend light less."])]},
    {"id": "3.4", "title": "Question 3.4", "kind": "The ear", "marks": 14, "lead": "The diagram below shows the structure of the human ear.", "items": q34,
     "figure": fig(15, (107, 111, 529, 389), "The human ear. A labels the outer flap on the left; the auditory canal (labelled) runs inward from it; "
                   "B, three lines to the small bones behind the eardrum; C, a bracket beside the three loops at the top right; D, the spiral at the "
                   "bottom right; E, the tube running down from the middle ear."),
     "extract": "When a person is exposed to loud noise over a long period, it may lead to noise-induced hearing loss (NIHL), which is caused by "
                "damage to the hair cells in the organ of Corti. These cells are not repaired when damaged. Placing earplugs in the auditory canal "
                "can prevent damage to the hair cells."},
    {"id": "3.5", "title": "Question 3.5", "kind": "Insulin treatment", "marks": 10,
     "lead": "The graph below shows the insulin levels of three people over a 23-hour period, who were treated as follows:", "items": q35,
     "extract": "Person A: A healthy person who received no treatment\nPerson B: A person with diabetes mellitus who received a rapid-acting insulin "
                "injection before each meal\nPerson C: A person with diabetes mellitus who received a daily injection, containing long-acting insulin, "
                "at 23:00\n\nAll three people received the same meals at the same time of the day.",
     "figure": fig(16, (104, 261, 524, 495), "Line graph 'Blood insulin concentration over a period of 23 hours': insulin concentration (international "
                   "units, 0 to 60) against time of day, 4:00 to 3:00. Person A (solid line): about 4 until 6:00, peaks of 55 at 8:00, 40 at 14:00 and "
                   "40 at 20:00, falling to about 10 between them and to 4 by 3:00. Person B (dashed line): about 1 most of the time, with peaks of 30 at "
                   "8:00, 15:00 and 22:00. Person C (dotted line): steady at 10 all day, dipping to about 4 at 23:00 and back to 10 after 0:00.")},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2025", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}, {"title": "Section B", "total": 100, "missions": missions_b}],
    "flags": [
        {"n": "3.5.3", "kind": "no_fit", "detail": "Tabulate TWO differences: the memo gives 1 mark for the table and 2 x 2 for the differences (both sides each). Played as a written answer; a two-column table input is the right layout (2025 survey, item 11)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 3), hand-transcribed from the paper and memo PDFs; no API call."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p1-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Questions 1 to 3 (the whole paper)"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]))
