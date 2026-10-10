"""Life Sciences P1 Nov 2024, the whole paper (Questions 1 to 3), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks and answers are the paper's and the memo's own; the clues and
the figure captions (alt text) are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_ls_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Life Sciences P1 Nov 2024 Eng.pdf" "<...>/Life Sciences P1 Nov MG 2024 Eng.pdf" --id ls-p1-2024-11 --from-json
  then open Exam Practice.dc.html?ingested=ls-p1-2024-11&paper=ls-p1-2024-11&play=0

Written answers (2026-10-10): the memo's points stay below as rubric bullets (the source); the bottom block plays every one as
statements to pick (STATEMENTS), and the one typed calculation (2.2.4) is a choose-the-working multiple choice (`work`).

Figure boxes are measured in PDF points on the A4 page (595 x 842) and stored as fractions."""
import json
import random
import re
from pathlib import Path

W, H = 595.0, 842.0
box = lambda x0, y0, x1, y1: [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)]
fig = lambda page, b, caption: {"page": page, "bbox": box(*b), "caption": caption}
mcq = lambda n, q, opts, a, clues, **kw: {"t": "mcq", "n": n, "marks": 2, "q": q, "clues": clues, "opts": opts, "a": a, **kw}
term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
AB = ["A only", "B only", "Both A and B", "None"]
# Column I / Column II (1.3): the description is the stem, COLUMN II's two items are `ab` (the Venn layout draws them as its two circles)
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
LET = ["A", "B", "C", "D", "E"]

# ---- Typed calculations as authored multiple choice (Murci, 2026-10-10; as tools/ingest/transcribe_ml_p2_2025_11.py) ----
WORK = "\n\nChoose the correct working."
AUTHORED = []   # the typed calculations played as authored multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues):
    """A typed calculation as authored multiple choice: opts are the memo's FIRST working and three workings built from common
    errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return {"t": "mcq", "n": n, "marks": marks, "q": q + WORK, "clues": clues, "opts": opts, "a": a}

q11 = [
    mcq("1.1.1", "The hormone responsible for the regulation of salt content in the human body is …",
        ["testosterone.", "aldosterone.", "prolactin.", "glucagon."], 1,
        ["It comes from the adrenal glands, not the sex organs or the pancreas.", "It makes the kidney tubules take sodium back into the blood."]),
    mcq("1.1.2", "Which ONE of the following is a stage in human embryonic development?",
        ["Choroid", "Amnion", "Morula", "Chorion"], 2,
        ["One option is part of the eye, and two are membranes around the embryo.", "Which one is a ball of cells formed by the dividing zygote?"]),
    mcq("1.1.3", "When the carbon dioxide level in the blood increases above normal, the …",
        ["rate and depth of breathing decrease.", "receptor cells in the diaphragm are stimulated.", "heart beats slower.",
         "receptor cells in the carotid artery in the neck are stimulated."], 3,
        ["Extra carbon dioxide has to be detected before the body can respond.", "The receptors sample the blood on its way to the brain."]),
    mcq("1.1.4", "Which ONE of the following changes occurs under the influence of adrenalin?",
        ["An increased blood supply to the skeletal muscles", "Decreased blood pressure", "Decreased muscle tone of skeletal muscles",
         "An increased blood supply to the digestive system"], 0,
        ["Adrenalin gets the body ready for fight or flight.", "Which organs need more blood to run or fight, and which can wait?"]),
    mcq("1.1.5", "A girl is barefoot and steps onto a thorn, causing a reflex action. Which ONE of the following represents the CORRECT pathway of the reflex arc?",
        ["Pain receptor → motor neuron → sensory neuron → leg muscle", "Foot muscle → sensory neuron → motor neuron → pain receptor",
         "Foot muscle → motor neuron → sensory neuron → pain receptor", "Pain receptor → sensory neuron → motor neuron → leg muscle"], 3,
        ["A reflex starts where the stimulus is felt.", "The impulse travels in to the spinal cord before it travels out to the muscle."]),
    # options printed as a TABLE: optTable carries it; opts read each row as a line (the medal card, the memo)
    mcq("1.1.6", "The diagram represents a part of the human eye. A spectator in a soccer stadium is seated 200 metres away from the field. "
        "Which ONE of the following describes the condition of structures X, Y and Z when he looks at the ball placed in the middle of the field?",
        ["Muscle in X relaxed · Structure Y slack · Part Z more convex", "Muscle in X contracted · Structure Y slack · Part Z less convex",
         "Muscle in X relaxed · Structure Y taut · Part Z less convex", "Muscle in X contracted · Structure Y taut · Part Z more convex"], 2,
        ["200 metres is far away: the eye is focusing on a distant object.", "For a distant object the lens has to bend the light less."],
        # (the captions name no structure the paper leaves to the learner: only letters, shapes and positions)
        figure=fig(4, (211, 110, 384, 266), "Part of the human eye in section. X points to the thickened part of the wall at the top "
                   "end of the oval transparent body in the middle, Y to the strands joining the bottom of that body to the wall, and Z to "
                   "the oval transparent body itself."),
        optTable={"head": ["MUSCLE IN X", "STRUCTURE Y", "PART Z"],
                  "rows": [["Relaxed", "Slack", "More convex"], ["Contracted", "Slack", "Less convex"],
                           ["Relaxed", "Taut", "Less convex"], ["Contracted", "Taut", "More convex"]]}),
    mcq("1.1.7", "Which ONE of the following is involved in thermoregulation?",
        ["Corpus callosum", "Hypothalamus", "Cerebellum", "Spinal cord"], 1,
        ["Body temperature is kept steady by a control centre in the brain.", "The same centre also controls the water balance of the blood."]),
    mcq("1.1.8", "The following is a list of factors regarding a developing foetus: (i) Temperature regulation (ii) Protection (iii) Free movement "
        "(iv) Nutrition. For which combination of factors is the amniotic fluid responsible?",
        ["(i), (ii) and (iii) only", "(i) and (iv) only", "(ii) and (iii) only", "(i), (ii), (iii) and (iv)"], 0,
        ["The amniotic fluid surrounds the foetus; it does not carry food to it.", "Which factor does the placenta take care of instead?"]),
    mcq("1.1.9", "The diagram shows a part of the human ear. Which ONE of the following occurs when there are excess waves in the inner ear?",
        ["Pressure is released at A", "Pressure is released at C", "Pressure is absorbed at B", "Pressure is absorbed at A and C"], 2,
        ["The excess waves are in the fluid of the inner ear.", "A membrane on the cochlea bulges outward to take up the pressure."],
        figure=fig(5, (201, 119, 394, 276), "Part of the human ear: A points to the thin membrane at the inner end of the canal on "
                   "the left, B to a small membrane on the inner-ear side, just below the last of the chain of small bones, and C to a tube "
                   "running downwards from the cavity.")),
    mcq("1.1.10", "The diagrams represent the transmission of impulses from a structure in the inner ear to the brain. "
        "The nerve impulses for balance are transmitted as follows:",
        ["J → F → H", "E → F → H", "E → F → G", "J → F → G"], 1,
        ["Balance is sensed in the semicircular canals, not in the cochlea.", "Which part of the brain coordinates balance?"],
        figure=fig(5, (163, 452, 519, 590), "Left: the inner ear, with nerve E from the three looped canals and nerve J from the coiled, "
                   "snail-shaped tube, the two joining as nerve F. Right: the brain, with G on the large folded upper part and H on the small "
                   "rounded part at the back, below it.")),
]
q12 = [
    term("1.2.1", "The structure that connects the foetus to the placenta", ["umbilical cord"],
         ["It holds two arteries and a vein.", "It is cut after birth."]),
    term("1.2.2", "The part of the nervous system that consists of sympathetic and parasympathetic sections", ["autonomic nervous system", "autonomic"],
         ["It works without conscious control.", "It controls the heart rate and the movement of the gut."]),
    term("1.2.3", "Receptors in the ear that detect changes in speed and direction of movement of the head", ["cristae", "crista"],
         ["They sit in the ampullae of the semicircular canals.", "Compare the maculae, which detect the position of the head."]),
    term("1.2.4", "The ossicle that transfers vibrations to the oval window", ["stirrup", "stapes"],
         ["The three ossicles are the hammer, the anvil and one more.", "It is the smallest bone in the body."]),
    term("1.2.5", "The growth reaction of a plant in response to gravity", ["geotropism", "gravitropism"],
         ["A tropism is named after its stimulus.", "Roots grow down and shoots grow up because of it."]),
    term("1.2.6", "The part in the inner ear where the organ of Corti is located", ["cochlea"],
         ["It is the hearing part of the inner ear.", "It is coiled like a snail's shell."]),
    term("1.2.7", "A plant hormone that stimulates the germination of seeds", ["gibberellins", "gibberellin"],
         ["It breaks seed dormancy.", "It is not auxin or abscisic acid."]),
    term("1.2.8", "A structure in the head of a sperm cell that contains enzymes", ["acrosome"],
         ["It sits at the tip of the sperm's head.", "Its enzymes dissolve a way into the ovum."]),
]
q13 = [
    abq("1.3.1", "Acts as a micro-filter for the developing foetus", "Placenta", "Cervix", 0,
        ["Which structure stands between the mother's blood and the foetus's blood?", "The cervix is a passage, not a filter."]),
    abq("1.3.2", "The part of the brain that controls heart rate", "Corpus callosum", "Medulla oblongata", 1,
        ["The heart rate is not under conscious control.", "The corpus callosum joins the two halves of the cerebrum."]),
    abq("1.3.3", "The area on the retina where there are no rods or cones", "Blind spot", "Cornea", 0,
        ["Is the cornea part of the retina?", "Where the optic nerve leaves the eye there is no room for receptors."]),
]
ln = lambda n, q, letter, names, clues: {"t": "lettername", "n": n, "marks": 2, "q": q, "clues": clues, "letters": LET, "a": {"letter": letter, "name": names}}
q14 = [
    # the memo accepts C – urethra OR D – penis (`or`); "C – penis" earns the letter mark only (Murci, 2026-10-05)
    {**ln("1.4.1(a)", "Give the LETTER and NAME of the structure that forms part of both the urinary and reproductive systems", "C", ["urethra"],
          ["Urine and semen leave the body the same way.", "It carries urine at some times and semen at others."]),
     "or": [{"letter": "D", "name": ["penis"]}]},
    ln("1.4.1(b)", "Give the LETTER and NAME of the structure that stores sperm temporarily", "B", ["epididymis"],
       ["Sperm mature here before they move on.", "From here, sperm move on into the sperm duct."]),
    ln("1.4.1(c)", "Give the LETTER and NAME of the structure that secretes testosterone", "E", ["testis", "testes"],
       ["Testosterone is made where sperm are made.", "It hangs in the scrotum."]),
    term("1.4.2(a)", "Identify part A", ["prostate gland", "prostate"],
         ["It is a gland just below the bladder.", "Its fluid is part of semen."]),
    term("1.4.2(b)", "Identify the type of gametogenesis that takes place in part E", ["spermatogenesis"],
         ["It happens inside the tiny tubules of part E.", "It begins at puberty and goes on throughout life."]),
]
q15 = [
    {"t": "pickn", "n": "1.5.1", "marks": 2, "q": "Write the LETTERS of the parts that serve as endocrine glands only.",
     "clues": ["A gland that makes both hormones and digestive juices is not an endocrine gland ONLY.", "Look for glands that release hormones into the blood and nothing else."],
     "opts": ["A", "B", "C", "D", "E", "F"], "pool": [0, 5], "count": 2},
    # two LETTER + NAME pairs in one part, any order
    {"t": "letternames", "n": "1.5.2", "marks": 4, "q": "Give the LETTERS and NAMES of the parts responsible for the regulation of body temperature.",
     "clues": ["The body loses heat through the skin in two ways.", "One part can widen to bring more heat to the skin's surface; the other cools the skin by evaporation."],
     "letters": ["A", "B", "C", "D", "E", "F"], "count": 2,
     "pool": [{"letter": "B", "name": ["capillaries", "capillary", "blood vessel", "blood vessels"]}, {"letter": "C", "name": ["sweat gland", "sweat glands"]}]},
    term("1.5.3(a)", "Name the hormone secreted by part A (the regulation of water content in the blood)", ["ADH", "antidiuretic hormone", "anti-diuretic hormone"],
         ["It is released when the blood has too little water.", "It makes the body keep more water, so less urine is made."]),
    term("1.5.3(b)", "Name target organ E (the regulation of water content in the blood)", ["kidney", "kidneys"],
         ["The hormone acts on the organ that makes urine.", "It filters the blood."]),
]
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 8,
     "lead": "Give the correct biological term for EACH of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "A, B, both or none", "marks": 6,
     "lead": "Indicate whether each of the descriptions in COLUMN I apply to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.", "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Male reproductive system", "marks": 8,
     "lead": "The diagram below represents the front view of the human male reproductive system.", "items": q14,
     "figure": fig(7, (129, 124, 471, 360), "Front view of the male reproductive system, with the bladder labelled at the top. A: the rounded "
                   "structure just below the bladder, around the tube that leaves it. B: the curved part against the oval body in the sac on the right "
                   "of the picture. C: the tube running down the middle of the long organ that hangs at the bottom. D: that long organ. E: the oval "
                   "body in the sac on the left of the picture.")},
    {"id": "1.5", "title": "Question 1.5", "kind": "Homeostasis", "marks": 8,
     "lead": "The diagram below represents some structures involved in homeostasis in the human body.", "items": q15,
     "figure": fig(8, (114, 130, 508, 400), "The upper body with some organs, and an enlarged part of the skin (labelled 'Part of the skin'). "
                   "A: a small structure at the base of the brain. B: the looping lines that run up to just under the skin's surface. C: the coiled "
                   "structure deep in the skin with a duct to the surface. D: the long structure below the stomach, along its curve. E: the bean-shaped "
                   "organ on the right of the picture. F: the small cap on top of the bean-shaped organ on the left of the picture.")},
]
# ---- Question 2 (Section B), from the question paper pages 9-13 and the memo pages 5-6 ----
lst = lambda n, q, count, marks, pool, clues: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
rub = lambda n, q, marks, bullets, clues, **kw: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **kw}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
q21 = [
    term("2.1.1(a)", "Identify part A", ["fallopian tube", "fallopian tubes"],
         ["It carries the ovum towards the uterus.", "Fertilisation normally happens in it."]),
    term("2.1.1(b)", "Identify part B", ["ovary", "ovaries"],
         ["It makes the ova.", "It also makes oestrogen and progesterone."]),
    # (a list: an answer scores when it holds an accepted answer's first word, so each group leads with its key word)
    lst("2.1.2(a)", "Give TWO characteristics of the endometrium that make it suitable for implantation", 2, 2,
        [["blood (a rich blood supply)", "vascular"], ["glandular", "glands"], ["thick", "thickened"]],
        ["Think of what an embryo needs from the wall it sinks into.", "Look closely at the lining in the figure, and think about what it must supply."]),
    lst("2.1.2(b)", "Give TWO visible reasons why there is an increased chance of fertilisation in this female", 2, 2,
        [["sperm", "sperm cells are present"], ["ovulation", "ovum has been released", "egg has been released"]],
        ["Look at what is swimming inside part A.", "Look at what has just left part B."]),
    rub("2.1.3", "Identify and describe the type of gametogenesis that leads to the formation of structure C.", 6,
        ["During oogenesis", "diploid cells in the ovary undergo mitosis", "to form numerous follicles", "At the onset of puberty",
         "under the influence of FSH", "one cell inside a follicle (enlarges and) undergoes meiosis",
         "Of the four cells that are produced, only one survives to form a (mature), haploid ovum"],
        ["Name the process first, then describe it from the start.", "Think about which cell divisions happen before birth and which begin later in life."], must=[0]),
    rub("2.1.4", "In an ectopic pregnancy, the fertilised ovum can become implanted in part A. This normally results in the death of the embryo and may "
        "endanger the mother's life. Explain why an ectopic pregnancy may result in the death of an embryo.", 3,
        ["Part A/the fallopian tube is unable to provide the space", "and there is no endometrium/blood supply",
         "to provide nutrients/oxygen OR remove waste products", "in order for the embryo to develop"],
        ["Compare part A with the wall of the uterus.", "What does a growing embryo need from the wall it implants in?"]),
]
q22 = [
    num("2.2.1", "On which day of this menstrual cycle is the level of progesterone the highest?", 20, 0.001, "",
        ["Read down the progesterone column only.", "Find its biggest number, then read the day beside it."]),
    term("2.2.2", "Name the reproductive hormone that will begin to increase from day 24 of this female's menstrual cycle.", ["FSH", "follicle stimulating hormone"],
         ["A new cycle is about to begin.", "This hormone starts a new follicle growing."]),
    rub("2.2.3", "Use data from the table to explain your answer to QUESTION 2.2.2.", 2,
        ["The progesterone level is decreasing/goes from 5 to 0,8 ng/mℓ", "therefore FSH secretion/the pituitary gland is no longer inhibited"],
        ["Look at progesterone from day 24 to day 28.", "Recall how progesterone affects the pituitary gland."]),
    # (typed steps until 2026-10-10: the memo's working [(280 − 70) / 70] × 100 = 300%, ticks on the fraction, the × 100 and the 300)
    work("2.2.4", "Calculate the percentage increase in the oestrogen level from day 8 to day 10. Show ALL your working.", 3, [
        "Percentage increase = {280 − 70}/{280} × 100\n= {210}/{280} × 100\n= 75%",        # divides by the day 10 level, not the day 8 one
        "Percentage increase = {300 − 70}/{70} × 100\n= {230}/{70} × 100\n≈ 328,57%",      # reads day 12's 300 for day 10's 280
        "Percentage increase = {280}/{70} × 100\n= 4 × 100\n= 400%",                       # the new level as a percentage of the old: no subtraction
        "Percentage increase = {280 − 70}/{70} × 100\n= {210}/{70} × 100\n= 300%"], 3,     # the memo
        ["Read the day 8 and day 10 oestrogen levels carefully.", "A percentage increase compares the change with the starting value."]),
    # ("it decreases" is two letters from "it increases" and the same word count, so the slip rule took it: `reject` refuses the opposites)
    {**term("2.2.5", "How would the progesterone level differ after day 20 if this female was pregnant?",
            ["remains high", "it remains high", "remain high", "stays high", "it stays high", "will increase", "it will increase", "increases", "it increases",
             "would remain high", "it would remain high", "will remain high", "it will remain high", "would stay high", "it would stay high",
             "will stay high", "it will stay high", "would increase", "it would increase", "the progesterone level remains high",
             "the progesterone level would remain high", "progesterone remains high", "higher", "it would be higher", "it will be higher"],
            ["Pregnancy needs the uterus lining kept in place.", "Which hormone keeps the lining, and would it fall?"]),
     "reject": ["decreases", "it decreases", "will decrease", "it will decrease", "would decrease", "it would decrease", "decrease"]},
    rub("2.2.6", "Explain what causes the change in the progesterone level stated in QUESTION 2.2.5.", 2,
        ["The corpus luteum does not disintegrate", "and continues to secrete progesterone", "OR — The placenta develops", "which secretes progesterone"],
        ["Which structure makes progesterone after ovulation?", "In a pregnancy, what keeps it going, and what takes over later?"]),
]
q23 = [
    term("2.3.1", "According to the passage, which type of cataract is associated with a disorder of the pancreas?",
         ["subcapsular cataracts", "subcapsular cataract", "subcapsular", "sub capsular cataracts", "sub capsular"],
         ["Which disorder of the pancreas is named in the passage?", "Find the type of cataract the passage links to it."]),
    rub("2.3.2", "Use information in the passage to explain why cataracts cause vision loss.", 5,
        ["Protein structures in the lens start to disintegrate and clump together", "The lens becomes opaque/milky",
         "less/no light passes through the lens", "onto the retina", "therefore less/no stimuli will be converted to impulses"],
        ["Start with what the passage says happens to the proteins in the lens.", "Then think about what light must do for the brain to see."]),
]
q24 = [
    rub("2.4.1", "Explain how the structure of his eyeball affects his vision when he reads a book without glasses", 3,
        ["The eyeball is too short", "The image forms behind the retina", "causing blurred vision",
         "OR — The cornea is less convex", "Less refraction occurs/the image forms behind the retina", "causing blurred vision"],
        ["A book is close: the light has to be bent a lot.", "Think about the shape of a long-sighted eye, and where the image lands in it."]),
    rub("2.4.2", "Explain how wearing glasses with convex lenses will improve his vision when he reads a book", 2,
        ["The light rays will be refracted more", "causing the image to fall on the retina"],
        ["Think about what a convex lens does to light before it reaches the eye.", "Recall where the image fell without glasses in QUESTION 2.4.1."]),
]
q25 = [
    # (the memo: "Motor✓neuron", the tick on Motor: the word alone earns the mark, and the one-word spelling too)
    term("2.5.1", "Identify the type of neuron shown in the diagrams.", ["motor neuron", "motor neurone", "motor neurons", "motorneuron", "motorneurone", "motor"],
         ["Look at where the cell body is.", "Which neuron carries impulses to a muscle?"]),
    # (keys that carry the meaning: "dendrites" alone took "It has dendrites", "body" took "the cell body is in the middle". "long axon" keys
    # on "long", the lead rule's first content word, so "long dendrites" still scores: a limit of the rule)
    lst("2.5.2", "Give ONE visible reason for your answer to QUESTION 2.5.1.", 1, 1,
        [["many dendrites (the neuron has many dendrites)", "multipolar", "numerous (numerous dendrites)"], ["one end (the cell body is located at one end)"],
         ["long axon (the axon is long and the dendrites are short)"]],
        ["Look at the cell body and the branches around it.", "Compare the lengths of the axon and the dendrites."]),
    rub("2.5.3", "Describe the function of the type of neuron identified in QUESTION 2.5.1.", 3,
        ["It transmits impulses", "from the central nervous system/interneuron", "to the effector"],
        ["What does this neuron carry?", "From where, and to what?"]),
    {"t": "order", "n": "2.5.4", "marks": 2, "q": "Use the letters A, B and C to indicate the direction in which an impulse moves through the neuron.",
     "clues": ["An impulse enters a neuron through its dendrites.", "It leaves through the axon's branched ends."], "opts": ["A", "B", "C"], "a": [2, 0, 1]},
    term("2.5.5", "Name the disorder associated with degeneration of the myelin sheaths of neurons.", ["multiple sclerosis", "MS"],
         ["The myelin is attacked and scars form.", "It usually first appears in young adults."]),
]
q26 = [
    num("2.6.1(a)", "Give the axon diameter (in µm) at which an impulse moves at 20 m/s in a myelinated neuron", 5, 0.5, "µm",
        ["Use the myelinated graph only.", "Find 20 m/s on the speed axis and read down."]),
    num("2.6.1(b)", "Give the axon diameter (in µm) at which an impulse moves at 20 m/s in an unmyelinated neuron", 800, 10, "µm",
        ["Use the unmyelinated graph only.", "Find 20 m/s on the speed axis and read down."]),
    rub("2.6.2(a)", "Use the graphs to describe the difference in impulse speed for myelinated and unmyelinated neurons", 2,
        ["The impulse speed is faster in a myelinated neuron than in an unmyelinated neuron",
         "OR — The impulse speed is slower in an unmyelinated neuron than in a myelinated neuron"],
        ["Compare the speeds the two graphs reach.", "Say which is faster, and than which."], each=2),
    rub("2.6.2(b)", "Use the graphs to describe the relationship between axon diameter and impulse speed", 2,
        ["As the axon diameter increases, the impulse speed is faster"],
        ["Both lines go the same way.", "As one value goes up, what does the other do?"], each=2),
]
missions_b = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Female reproduction", "marks": 15,
     "lead": "The diagram below represents a part of the female reproductive system.", "items": q21,
     "figure": fig(9, (104, 160, 522, 441), "Part of the female reproductive system. A: the curved tube arching over B, with small tailed cells "
                   "inside it. B: the large oval structure below the tube. C: a small round cell beside B, with an arrow pointing from B to it. On "
                   "the right, the lining labelled Endometrium, with more small tailed cells beside it.")},
    {"id": "2.2", "title": "Question 2.2", "kind": "Menstrual cycle hormones", "marks": 10,
     "lead": "The table below shows the levels of two hormones during the menstrual cycle of a healthy human female.", "items": q22,
     "table": {"head": ["Day of menstrual cycle", "Oestrogen level (pg/mℓ)", "Progesterone level (ng/mℓ)"],
               "rows": [["4", "55", "0,23"], ["8", "70", "0,03"], ["10", "280", "0,03"], ["12", "300", "0,03"], ["14", "140", "3,0"],
                        ["16", "110", "12,5"], ["20", "80", "15,0"], ["24", "70", "5,0"], ["28", "65", "0,8"]]}},
    {"id": "2.3", "title": "Question 2.3", "kind": "Cataracts", "marks": 6, "lead": "Read the passage below.", "items": q23,
     "extract": "CATARACTS – THE MOST COMMON CAUSE OF BLINDNESS\n\nCataracts are primarily formed when protein structures in the lens of the eye "
                "start to disintegrate and clump together. Cataracts is the most common cause of blindness and the main cause of vision loss in "
                "people over 40 years of age.\n\nTwo types of cataracts that occur are nuclear cataracts and subcapsular cataracts. In nuclear "
                "cataracts, the cataracts form in the central region of the lens and gradually spread outwards. In subcapsular cataracts, the "
                "cataracts develop at the back of the lens and it is most common in people with diabetes."},
    {"id": "2.4", "title": "Question 2.4", "kind": "Long-sightedness", "marks": 5, "lead": "A man is long-sighted. Explain how:", "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Neurons", "marks": 8,
     "lead": "The diagrams below represent a neuron with a myelin sheath (myelinated) and a neuron without a myelin sheath (unmyelinated). "
             "(The diagrams are NOT drawn to scale.)", "items": q25,
     "figure": fig(12, (131, 142, 486, 374), "Two neurons, not drawn to scale. Left: a neuron with a myelin sheath in segments along its long "
                   "middle fibre. Right: the same kind of neuron without a myelin sheath. A labels its long middle fibre, B the branched ends at "
                   "the top, and C the branches around the cell body at the bottom.")},
    {"id": "2.6", "title": "Question 2.6", "kind": "Impulse speed", "marks": 6,
     "lead": "In the human body, the axons of myelinated neurons have much smaller diameters than the axons of unmyelinated neurons. The graphs "
             "below show the speed of nerve impulses in myelinated neurons and in unmyelinated neurons with different axon diameters.", "items": q26,
     # (the caption gives the axes and the lines' shape, not the plotted values: 2.6.1 asks for two of them)
     "figure": fig(13, (98, 168, 552, 403), "Two line graphs of impulse speed (m/s) against axon diameter (µm), six plotted points each, joined "
                   "by a straight line. Myelinated neuron: diameter 5 to 30 µm, speed axis 0 to 140 m/s, the line rising steadily to 120 m/s at "
                   "30 µm. Unmyelinated neuron: diameter 200 to 1 200 µm, speed axis 0 to 35 m/s, the line rising steadily to 30 m/s at 1 200 µm.")},
]

# ---- Question 3 (Section B), from the question paper pages 14-18 and the memo pages 7-9 ----
# (a list scores an answer that holds the FIRST WORD of an accepted answer, so every accepted answer here leads with a word only that
# point uses: "body (the cell body ...)", never "the" / "same" / "no"; the words after it are what the memo shows)
mcq1 = lambda n, q, opts, a, clues: {"t": "mcq", "n": n, "marks": 1, "q": q, "clues": clues, "opts": opts, "a": a}
q31 = [
    lst("3.1.1(a)", "Give ONE reason from the passage why vultures are considered as oviparous", 1, 1,
        [["lay (they lay eggs)", "laid", "egg"]],
        ["What does an oviparous animal do with its young before they hatch?", "Find what the female vulture does in the passage."]),
    lst("3.1.1(b)", "Give ONE reason from the passage why vultures have a high survival rate even though few eggs are laid", 1, 1,
        [["protected (the eggs are protected / incubated by the parents)", "protect", "incubat"],
         ["fed (the chicks are fed by the parents)", "feed", "parental"]],
        ["Few eggs, yet most survive: who looks after them?", "Look at what the parents do before and after the eggs hatch."]),
    lst("3.1.2", "Fertilisation in vultures takes place internally. State TWO advantages of internal fertilisation.", 2, 2,
        [["chance (fertilisation is more likely: the gametes are in close contact)", "likely", "contact"],
         ["protected (the gametes are protected from predators / drying out)", "predat", "desiccat", "dry", "environment"],
         ["water (water is not needed)"],
         ["fewer (fewer gametes are needed)"]],
        ["Think about where the gametes meet, and what can harm them outside the body.", "Compare it with fish releasing gametes into water."]),
    # (each group keys on the word that carries the meaning: "eyes", "feather" and "move" took the precocial opposites, "eyes are open")
    lst("3.1.3", "State TWO characteristics of chicks that display altricial development.", 2, 2,
        [["closed (eyes are closed when they hatch)", "blind", "shut", "not open"],
         ["featherless (bodies do not have down feathers)", "not have", "naked", "no feathers", "no down", "dont (don't have feathers)"],
         ["unable (unable to move directly after hatching)", "immobile", "helpless", "cannot", "cant (can't move)", "not move", "not able"],
         ["dependent (on parents for food/protection)", "depend", "rely", "relies"]],
        ["Altricial chicks hatch early in their development.", "Think about what they can and cannot do on day one."]),
    rub("3.1.4", "Explain why birds with altricial development would have short incubation periods.", 2,
        ["The chicks are not fully developed when hatched since", "the eggs have less yolk/there is a high degree of parental care"],
        ["How developed is an altricial chick when it hatches?", "What does an embryo need from its egg to stay inside it longer?"]),
]
q32 = [
    term("3.2.1(a)", "Identify part X", ["pupil", "the pupil"], ["It is the opening that lets light into the eye.", "It looks black in the middle of the eye."]),
    term("3.2.1(b)", "Identify part Y", ["iris", "the iris"], ["It is the coloured ring around X.", "Its muscles change the size of X."]),
    rub("3.2.2", "Explain why the pupillary mechanism is considered to be a reflex action.", 3,
        ["It is a rapid", "involuntary response", "to light"],
        ["Recall the definition of a reflex action.", "Think about what the pupil responds to, and whether you decide it."]),
    lst("3.2.3", "Name the TWO effector muscles that are involved in the pupillary mechanism.", 2, 2,
        [["radial muscles", "radial"], ["circular muscles", "circular"]],
        ["Both are in part Y.", "One set runs like the spokes of a wheel, the other in rings."]),
    rub("3.2.4", "Explain the significance of the change in the diameter of part X from diagram A to diagram B.", 4,
        ["The pupil dilated/enlarged so that", "more light will enter the eye", "to improve vision", "in dim light"],
        ["Did X get bigger or smaller from A to B?", "What does that let in, and when would the eye need it?"]),
]
q33 = [
    rub("3.3.1", "State the purpose of the control group in this investigation.", 2,
        ["To ensure that the change in blood glucose levels was due to insulin only"],
        ["A control lets you compare.", "Compare the two groups: in what one way do they differ?"], each=2),
    rub("3.3.2", "Describe TWO ways in which insulin decreases blood glucose levels.", 4,
        ["It stimulates the absorption of glucose from the blood into the cells", "It stimulates the liver/muscles to convert glucose to glycogen",
         "It causes increased cellular respiration which utilises glucose"],
        ["Think of where the glucose goes when it leaves the blood.", "Insulin lowers glucose; its partner hormone, glucagon, does the opposite."], each=2),
    mcq1("3.3.3", "Which group (X or Y) consists of healthy individuals?", ["X", "Y"], 1,
         ["Compare each group's glucose at 0 minutes with the normal range in the note.", "Which group's insulin rose after the glucose?"]),
    rub("3.3.4", "Use data in the table to explain your answer to QUESTION 3.3.3.", 3,
        ["At 0 minutes the blood glucose level for group Y was within the normal range / for group X it was high",
         "At 90 minutes the blood glucose level for group Y returned to normal / for group X it remained high",
         "After the ingestion of glucose the insulin level for group Y increased / for group X it decreased"],
        ["Check each statement against the table and the normal ranges in the note.", "Read the numbers for the right group and time before you pick."]),
]
q34 = [
    term("3.4.1(a)", "Identify the type of interaction represented by the diagram", ["negative feedback mechanism", "negative feedback", "negative feedback loop"],
         ["A change is detected and then reversed.", "Is the response the opposite of the change, or more of it?"]),
    term("3.4.1(b)", "Identify gland Y", ["thyroid", "thyroid gland"], ["It makes thyroxin.", "It sits in the neck."]),
    term("3.4.1(c)", "Identify the disorder that is characterised by the enlargement of gland Y", ["goitre", "goiter"],
         ["A swelling in the neck.", "It is often caused by too little iodine."]),
    lst("3.4.2", "State ONE function of thyroxin.", 1, 1,
        [["metabolic (it regulates the metabolic rate)", "metabol"], ["heart (the growth and functioning of the heart / nervous system)", "nervous", "growth"],
         ["bone (bone development / muscle control)", "muscle"]],
        ["It sets how fast the body uses energy.", "Think about why people with too little of it feel tired and gain weight."]),
    rub("3.4.3", "Describe the role of the pituitary gland in correcting the level of thyroxin at X.", 4,
        ["The thyroxin level is low", "The pituitary gland is stimulated", "More TSH is secreted", "which stimulates gland Y/the thyroid gland",
         "to secrete more thyroxin"],
        ["Follow the line from X through the pituitary gland and back to gland Y.", "What does the pituitary release, and what does that make gland Y do?"]),
    rub("3.4.4", "Explain why a continuous undersecretion of thyroxin may lead to an increase in body mass.", 2,
        ["A lower metabolic rate", "causes decreased usage of nutrients", "and excess nutrients/fat will be stored in the body"],
        ["Too little thyroxin slows something down.", "Think about what the body does with food it does not use."]),
]
q35 = [
    term("3.5.1(a)", "For this investigation give the independent variable", ["auxins", "auxin", "presence of auxins", "the presence of auxins", "presence or absence of auxins"],
         ["What did the investigators change between the groups?", "Groups B and C differ in one thing only."]),
    lst("3.5.1(b)", "For this investigation give TWO variables that were controlled", 2, 2,
        [["species (the same species of plant)"], ["duration (72 hours in the dark)", "hours", "72", "time"], ["light (all kept in darkness)", "dark"]],
        ["What was kept the same for all twelve plants?", "Read the procedure again, looking for what all three groups shared."]),
    rub("3.5.2(a)", "Give the expected results of the plants in group A", 1, ["The plant / stem grows (straight) upwards"],
        ["Group A keeps its own tip, and there is no light from one side.", "Which way does it grow?"]),
    rub("3.5.2(b)", "Give the expected results of the plants in group C", 1, ["No upward growth will occur", "OR — Lateral branches will develop"],
        ["Group C has no tip and no auxins.", "What do auxins from the tip normally make the stem do?"]),
    rub("3.5.3", "How was the reliability of this investigation ensured?", 2, ["Four plants in each group"],
        ["Reliability comes from repeating.", "Look at how the twelve plants were shared out."], each=2),
    rub("3.5.4", "After 72 hours, the stems of the plants in group B bent towards the right-hand side. Explain these results.", 4,
        ["The auxins diffuse into the left side of the stem", "The higher concentration of auxins on the left side",
         "results in more cell elongation/growth of cells on the left side", "There is less growth on the right-hand side and the stem will bend to the right-hand side"],
        ["Look at where the agar sits on group B's stem.", "Recall what auxins do to the cells they reach."]),
]
missions_q3 = [
    {"id": "3.1", "title": "Question 3.1", "kind": "Vulture breeding", "marks": 8, "lead": "The passage below describes the breeding habits of vultures.", "items": q31,
     "extract": "Vultures are birds of prey that feed on the flesh of dead animals.\n\nA female vulture lays only one to two fertilised eggs, which are then "
                "protected by both parents during incubation. Incubation is the period from the time an egg is laid up to the time it hatches. Vultures "
                "have a short incubation period of 32 to 45 days. This short incubation period is typical of birds displaying altricial development. "
                "After hatching, the parents feed the young chicks as often as 20 times a day."},
    {"id": "3.2", "title": "Question 3.2", "kind": "Pupillary mechanism", "marks": 11, "lead": "The diagrams below represent the pupillary mechanism in the human eye.",
     "items": q32,
     "figure": fig(15, (109, 110, 502, 274), "Two front views of an eye, diagram A and diagram B, with an arrow from A to B. X labels the dark round opening "
                   "in the centre; Y labels the grey ring around it. In diagram B the dark opening X is larger and the grey ring Y narrower than in diagram A.")},
    {"id": "3.3", "title": "Question 3.3", "kind": "Insulin and glucose", "marks": 10,
     "lead": "An investigation was conducted to determine the effect of insulin on blood glucose levels.", "items": q33,
     "extract": "The procedure was as follows:\n• Two groups of ten people each were selected.\n• One of the groups consisted of healthy individuals and the "
                "second group, which served as a control, consisted of people with diabetes.\n• Each group was given 75 g of glucose to ingest.\n"
                "• Their blood was tested again after 60 and 90 minutes to determine the levels of glucose and insulin.\n\nNOTE:\n• The normal level of "
                "glucose in the blood is between 3,9 mmol/ℓ and 5,6 mmol/ℓ.\n• The normal level of insulin in the blood, 60 minutes after glucose "
                "ingestion, is between 18 mU/ℓ and 276 mU/ℓ.\n\nThe results are recorded in the table below.",
     # (the paper's table runs the two groups side by side, six columns of times; one row per group and time reads the same on a phone)
     "table": {"title": "Average levels in the blood", "head": ["Group", "Time after glucose ingestion (minutes)", "Glucose (mmol/ℓ)", "Insulin (mU/ℓ)"],
               "rows": [["X", "0", "6,8", "4"], ["X", "60", "8,9", "2"], ["X", "90", "8,7", "2"], ["Y", "0", "4,5", "8"], ["Y", "60", "6,2", "142"], ["Y", "90", "4,5", "108"]]}},
    {"id": "3.4", "title": "Question 3.4", "kind": "Thyroxin control", "marks": 10, "lead": "The flow diagram below shows the homeostatic control of thyroxin in the human body.",
     "items": q34,
     "figure": fig(17, (121, 131, 512, 321), "A flow diagram between GLAND Y on the left and the PITUITARY GLAND on the right. Two arrows run from gland Y into the pituitary: a dashed one on top, labelled 'Level of thyroxin (X)', and a solid one below, labelled 'Level of thyroxin (Z)'. Inside the pituitary the two lines cross: the dashed X line turns down into the arrow along the bottom, labelled 'More TSH', which runs back to gland Y; the solid Z line turns up into the arrow over the top, labelled 'Less TSH', which runs back to gland Y.")},
    {"id": "3.5", "title": "Question 3.5", "kind": "Auxins and tropism", "marks": 11,
     "lead": "An investigation was conducted to determine the effect of auxins on plant tropism.", "items": q35,
     "extract": "The investigation was conducted as follows:\n• Twelve plants of the same species were divided into three groups (group A, B and C), of four "
                "plants each.\n• All the plants were kept in darkness for 72 hours during the investigation.\n• The growing tips of group A received no "
                "treatment.\n• The growing tips of group B were cut off and replaced by a piece of agar that contained auxins (agar is a jelly-like substance "
                "through which other substances can diffuse).\n• The growing tips of group C were cut off and replaced by a piece of agar without auxins.\n\n"
                "The diagram below shows how the growing tips of the three groups were treated.",
     "figure": fig(18, (167, 309, 419, 482), "Three plant stems side by side. Group A: the stem with its rounded growing tip. Group B: the tip cut off, and a "
                   "striped block of agar containing auxins on the cut end, sitting over the left side of the stem. Group C: the tip cut off, and a plain "
                   "block of agar without auxins on the cut end.")},
]
missions_b += missions_q3

# ---- Written answers as STATEMENTS (Murci 2026-10-10; as tools/ingest/transcribe_bs_p2_2025_11.py) ----
# A written part plays as picking statements: the memo's own points (right, tidied to one reading of its "/" alternatives) and
# CLEARLY wrong ones (never a true point the memo leaves out: its "any other relevant answer" would make that right). The learner
# picks marks/each of them, any right one counts (the memo's "any N"), each right pick earns `each` (Life Sciences: 1 a tick; a
# point the memo ticks twice, 2); the cards are shuffled the same way every run. The rubric bullets above stay as the source.
#   2.1.3: the memo's compulsory mark (naming oogenesis) is one of the six right cards and the 6 marks need all six, so a learner who
#   leaves it out scores at most 5, as the memo's "Compulsory (1) + Any (5)" gives; "mitosis" and "to form numerous follicles" share a
#   card (two ticks, one card: the six cards cover all seven ticks).
#   2.2.6 and 2.4.1: the memo's two OR answers are both on the cards (each a memo point).
def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("ls-p1-2024-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    "2.1.3": (1, ["Structure C is formed by oogenesis.", "Diploid cells in the ovary undergo mitosis to form numerous follicles.",
                  "The next stage starts at the onset of puberty.", "This stage takes place under the influence of FSH.",
                  "One cell inside a follicle enlarges and undergoes meiosis.",
                  "Of the four cells that are produced, only one survives to form a mature, haploid ovum."],
                 ["Structure C is formed by spermatogenesis.", "All four cells produced by meiosis develop into mature ova."]),
    "2.1.4": (1, ["Part A is unable to provide the space the embryo needs.", "Part A has no endometrium with a blood supply.",
                  "So the embryo cannot get nutrients and oxygen, or have its waste products removed.", "Without these, the embryo cannot develop."],
                 ["Part A has more space than the uterus, so the embryo grows too fast.", "Part A has a thick endometrium that crushes the embryo.",
                  "The embryo receives too much oxygen in part A."]),
    "2.2.3": (1, ["The progesterone level is decreasing, from 5 to 0,8 ng/mℓ.", "Therefore FSH secretion by the pituitary gland is no longer inhibited."],
                 ["The progesterone level is increasing after day 24.", "Therefore FSH secretion is inhibited even more.",
                  "The oestrogen level rises sharply from day 24 to day 28.", "High progesterone stimulates the pituitary gland to secrete FSH."]),
    "2.2.6": (1, ["The corpus luteum does not disintegrate.", "The corpus luteum continues to secrete progesterone.", "The placenta develops.",
                  "The placenta secretes progesterone."],
                 ["The corpus luteum disintegrates, so progesterone secretion stops.", "The pituitary gland secretes progesterone during pregnancy.",
                  "The endometrium breaks down and releases progesterone."]),
    "2.3.2": (1, ["Protein structures in the lens start to disintegrate and clump together.", "The lens becomes opaque (milky).",
                  "Less light passes through the lens.", "Less light falls onto the retina.", "Therefore fewer stimuli are converted to impulses."],
                 ["Protein structures in the lens multiply and make the lens more transparent.", "More light passes through the lens onto the retina.",
                  "The cataracts form on the retina, so the rods and cones die."]),
    "2.4.1": (1, ["The eyeball is too short.", "The image forms behind the retina.", "This causes blurred vision.", "The cornea is less convex.",
                  "Less refraction occurs."],
                 ["The eyeball is too long.", "The image forms in front of the retina.", "The lens is too convex, so the light is refracted too much."]),
    "2.4.2": (1, ["The light rays will be refracted more.", "This causes the image to fall on the retina."],
                 ["The light rays will be refracted less.", "This causes the image to fall in front of the retina.",
                  "The convex lenses make the eyeball longer.", "This causes the image to fall on the blind spot."]),
    "2.5.3": (1, ["It transmits impulses.", "The impulses come from the central nervous system (an interneuron).", "It carries the impulses to the effector."],
                 ["It carries impulses from the receptors to the central nervous system.", "It carries impulses only within the brain and spinal cord.",
                  "It secretes hormones that travel in the blood to the effector."]),
    "2.6.2(a)": (2, ["The impulse speed is faster in a myelinated neuron than in an unmyelinated neuron.",
                     "The impulse speed is slower in an unmyelinated neuron than in a myelinated neuron."],
                    ["The impulse speed is faster in an unmyelinated neuron than in a myelinated neuron.",
                     "The impulse speed is slower in a myelinated neuron than in an unmyelinated neuron.",
                     "The impulse speed is the same in myelinated and unmyelinated neurons."]),
    "2.6.2(b)": (2, ["As the axon diameter increases, the impulse speed is faster."],
                    ["As the axon diameter increases, the impulse speed is slower.", "As the axon diameter decreases, the impulse speed is faster.",
                     "The impulse speed stays the same at every axon diameter.",
                     "The impulse speed is faster only up to an axon diameter of 15 µm, then it stays the same."]),
    "3.1.4": (1, ["The chicks are not fully developed when they hatch.", "The eggs have less yolk, and there is a high degree of parental care."],
                 ["The chicks are fully developed and can feed themselves when they hatch.",
                  "The eggs have a large yolk that feeds the chicks for weeks after hatching.", "The parents leave the eggs, so the chicks must hatch quickly."]),
    "3.2.2": (1, ["It is a rapid response.", "It is an involuntary response.", "It is a response to light."],
                 ["It is a slow response.", "It is a voluntary response controlled by the cerebrum.", "It is a response to sound."]),
    "3.2.4": (1, ["The pupil dilated (enlarged).", "More light will enter the eye.", "This improves vision.", "This happens in dim light."],
                 ["The pupil constricted.", "Less light will enter the eye.", "This happens in bright light."]),
    "3.3.1": (2, ["To ensure that the change in blood glucose levels was due to insulin only."],
                 ["To make the results reliable by repeating the investigation.", "To show that people with diabetes produce more insulin than healthy people.",
                  "To increase the amount of glucose each person ingested.", "To make sure that the healthy group did not ingest any glucose."]),
    "3.3.2": (2, ["It stimulates the absorption of glucose from the blood into the cells.", "It stimulates the liver and muscles to convert glucose to glycogen.",
                  "It causes increased cellular respiration, which utilises glucose."],
                 ["It stimulates the liver to convert glycogen to glucose.", "It stops the cells from absorbing glucose from the blood.",
                  "It makes the kidneys excrete all the glucose in the urine."]),
    "3.3.4": (1, ["At 0 minutes, the blood glucose level for group Y was within the normal range.",
                  "At 90 minutes, the blood glucose level for group Y had returned to normal.",
                  "After the ingestion of glucose, the insulin level for group Y increased."],
                 ["At 0 minutes, the blood glucose level for group Y was above the normal range.",
                  "At 90 minutes, the blood glucose level for group X had returned to normal.",
                  "After the ingestion of glucose, the insulin level for group Y decreased."]),
    "3.4.3": (1, ["The thyroxin level at X is low.", "The pituitary gland is stimulated.", "More TSH is secreted.", "TSH stimulates gland Y.",
                  "Gland Y secretes more thyroxin."],
                 ["The thyroxin level at X is high.", "Less TSH is secreted.", "The pituitary gland secretes thyroxin directly into the blood."]),
    "3.4.4": (1, ["The metabolic rate is lower.", "The usage of nutrients decreases.", "Excess nutrients (fat) are stored in the body."],
                 ["The metabolic rate is higher, so more fat is burnt.", "Thyroxin itself is changed into fat and stored.",
                  "The extra mass comes from larger muscles."]),
    "3.5.2(a)": (1, ["The stem grows straight upwards."],
                    ["The stem bends towards the right.", "The stem bends towards the left.", "The stem stops growing.", "The stem bends downwards."]),
    "3.5.2(b)": (1, ["No upward growth will occur.", "Lateral branches will develop."],
                    ["The stem grows straight upwards.", "The stem bends towards the right.", "The stem bends towards the left."]),
    "3.5.3": (2, ["Four plants were used in each group."],
                 ["Only one plant was used in each group.", "Twelve groups of one plant each were used.",
                  "Each group was kept in a different amount of light.", "The plants in each group were of different species."]),
    "3.5.4": (1, ["The auxins diffuse into the left side of the stem.", "There is a higher concentration of auxins on the left side.",
                  "This results in more cell elongation on the left side.",
                  "There is less growth on the right-hand side, and the stem bends to the right-hand side."],
                 ["The auxins diffuse into the right side of the stem.", "The auxins inhibit cell elongation on the left side.",
                  "Light from the right-hand side makes the stem bend to the right."]),
}
# a part whose cards show an EARLIER part's answer opens only once that part is answered (the catalogue's `after`)
AFTER = {"2.1.3": ["2.1.1(b)"],    # "the ovary" (2.1.1(b) identifies part B)
         "2.2.3": ["2.2.2"],       # FSH
         "2.2.6": ["2.2.5"],       # the progesterone level stays high
         "2.5.3": ["2.5.1"],       # central nervous system to effector: a motor neuron
         "3.1.4": ["3.1.3"],       # parental care: the chicks depend on their parents
         "3.2.4": ["3.2.1(a)"],    # the pupil
         "3.3.4": ["3.3.3"],       # group Y
         "3.4.4": ["3.4.2"]}       # the metabolic rate (a function of thyroxin)
ALL = missions + missions_b
for _m in ALL:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric":
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            assert _each == _it.get("each", 1), (_it["n"], "each differs from the memo's")
            _m["items"][_k] = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
        if _it["n"] in AFTER:
            _m["items"][_k]["after"] = AFTER[_it["n"]]
ITEMS = [i for m in ALL for i in m["items"]]
_nums = [i["n"] for i in ITEMS]
assert not [i["n"] for i in ITEMS if i["t"] in ("rubric", "steps")], "a written part or typed steps left"
assert set(STATEMENTS) <= set(_nums) and all(_nums.index(a) < _nums.index(n) for n, aa in AFTER.items() for a in aa), "a statement or after out of place"
assert tuple(AUTHORED) == ("2.2.4",), AUTHORED

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}, {"title": "Section B", "total": 100, "missions": missions_b}],
    "flags": [
        {"n": "1.4.1(a)", "kind": "low_confidence", "detail": "The memo accepts C – urethra OR D – penis. Marked: either letter earns its mark, the name only when it names the part of the letter chosen ('C – penis' = 1). A Life Sciences teacher should confirm."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 3), hand-transcribed from the paper and memo PDFs; no API call."},
        {"n": "2.1.3", "kind": "no_fit", "detail": "Written answers play as picking statements (Murci, 2026-10-10): the memo's points and clearly wrong ones, "
                                                   "1 mark a tick (2 where the memo ticks one point twice: 2.6.2, 3.3.1, 3.3.2, 3.5.3). 2.1.3's "
                                                   "compulsory mark (oogenesis) is one of six right cards and full marks need all six, so leaving it "
                                                   "out caps the part at 5, as the memo's 'Compulsory (1) + Any (5)'. " + ", ".join(sorted(STATEMENTS)) + "."},
        {"n": "2.2.4", "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): the typed calculation plays as the memo's working "
                                                   "[(280 − 70) / 70] × 100 = 300% plus three built from common errors (the day 10 level as the base, "
                                                   "day 12's 300 misread for day 10, the new level over the old with no subtraction), 0 or 3 marks."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Questions 1 to 3 (the whole paper)"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]))
