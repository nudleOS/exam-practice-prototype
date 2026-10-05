"""Life Sciences P1 Nov 2024, Question 1, hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks and answers are the paper's and the memo's own; the clues and
the figure captions (alt text) are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_ls_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Life Sciences P1 Nov 2024 Eng.pdf" "<...>/Life Sciences P1 Nov MG 2024 Eng.pdf" --id ls-p1-2024-11 --from-json
  then open Exam Practice.dc.html?ingested=ls-p1-2024-11&paper=ls-p1-2024-11&play=0

Figure boxes are measured in PDF points on the A4 page (595 x 842) and stored as fractions."""
import json
from pathlib import Path

W, H = 595.0, 842.0
box = lambda x0, y0, x1, y1: [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)]
fig = lambda page, b, caption: {"page": page, "bbox": box(*b), "caption": caption}
mcq = lambda n, q, opts, a, clues, **kw: {"t": "mcq", "n": n, "marks": 2, "q": q, "clues": clues, "opts": opts, "a": a, **kw}
term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
AB = ["A only", "B only", "Both A and B", "None"]
LET = ["A", "B", "C", "D", "E"]

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
        ["Extra carbon dioxide has to be detected before the body can respond.", "The receptors sit in a blood vessel, not in a muscle."]),
    mcq("1.1.4", "Which ONE of the following changes occurs under the influence of adrenalin?",
        ["An increased blood supply to the skeletal muscles", "Decreased blood pressure", "Decreased muscle tone of skeletal muscles",
         "An increased blood supply to the digestive system"], 0,
        ["Adrenalin gets the body ready for fight or flight.", "Which organs need more blood to run or fight, and which can wait?"]),
    mcq("1.1.5", "A girl is barefoot and steps onto a thorn, causing a reflex action. Which ONE of the following represents the CORRECT pathway of the reflex arc?",
        ["Pain receptor → motor neuron → sensory neuron → leg muscle", "Foot muscle → sensory neuron → motor neuron → pain receptor",
         "Foot muscle → motor neuron → sensory neuron → pain receptor", "Pain receptor → sensory neuron → motor neuron → leg muscle"], 3,
        ["A reflex starts where the stimulus is felt.", "The impulse travels in to the spinal cord before it travels out to the muscle."]),
    # TABLE-SHAPED OPTIONS (flagged): the paper prints the options as a table (MUSCLE IN X | STRUCTURE Y | PART Z); flattened here
    mcq("1.1.6", "The diagram represents a part of the human eye. A spectator in a soccer stadium is seated 200 metres away from the field. "
        "Which ONE of the following describes the condition of structures X, Y and Z when he looks at the ball placed in the middle of the field?",
        ["Muscle in X relaxed · Structure Y slack · Part Z more convex", "Muscle in X contracted · Structure Y slack · Part Z less convex",
         "Muscle in X relaxed · Structure Y taut · Part Z less convex", "Muscle in X contracted · Structure Y taut · Part Z more convex"], 2,
        ["200 metres is far away: the eye is focusing on a distant object.", "For a distant object the lens has to bend the light less."],
        figure=fig(4, (211, 110, 384, 266), "Part of the human eye in section. X points to the ciliary body above the lens, Y to the "
                   "suspensory ligament below it, and Z to the lens.")),
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
        figure=fig(5, (201, 119, 394, 276), "Part of the human ear: A points to the eardrum, B to the round window, and C to the "
                   "Eustachian tube.")),
    mcq("1.1.10", "The diagrams represent the transmission of impulses from a structure in the inner ear to the brain. "
        "The nerve impulses for balance are transmitted as follows:",
        ["J → F → H", "E → F → H", "E → F → G", "J → F → G"], 1,
        ["Balance is sensed in the semicircular canals, not in the cochlea.", "Which part of the brain coordinates balance?"],
        figure=fig(5, (163, 452, 519, 590), "Left: the inner ear, with nerve E from the semicircular canals and nerve J from the cochlea "
                   "joining as nerve F. Right: the brain, with G on the cerebrum and H on the cerebellum.")),
]
q12 = [
    term("1.2.1", "The structure that connects the foetus to the placenta", ["umbilical cord"],
         ["It holds the umbilical arteries and vein.", "It is cut after birth."]),
    term("1.2.2", "The part of the nervous system that consists of sympathetic and parasympathetic sections", ["autonomic nervous system", "autonomic"],
         ["It works without conscious control.", "It controls the heart rate and the movement of the gut."]),
    term("1.2.3", "Receptors in the ear that detect changes in speed and direction of movement of the head", ["cristae", "crista"],
         ["They sit in the ampullae of the semicircular canals.", "Compare the maculae, which detect the position of the head."]),
    term("1.2.4", "The ossicle that transfers vibrations to the oval window", ["stirrup", "stapes"],
         ["The three ossicles are the hammer, the anvil and one more.", "It is the smallest bone in the body."]),
    term("1.2.5", "The growth reaction of a plant in response to gravity", ["geotropism", "gravitropism"],
         ["A tropism is named after its stimulus.", "'Geo' means earth."]),
    term("1.2.6", "The part in the inner ear where the organ of Corti is located", ["cochlea"],
         ["It is the hearing part of the inner ear.", "It is coiled like a snail's shell."]),
    term("1.2.7", "A plant hormone that stimulates the germination of seeds", ["gibberellins", "gibberellin"],
         ["It breaks seed dormancy.", "It is not auxin or abscisic acid."]),
    term("1.2.8", "A structure in the head of a sperm cell that contains enzymes", ["acrosome"],
         ["It sits at the tip of the sperm's head.", "Its enzymes dissolve a way into the ovum."]),
]
q13 = [
    mcq("1.3.1", "Acts as a micro-filter for the developing foetus A: Placenta · B: Cervix", AB, 0,
        ["Which structure stands between the mother's blood and the foetus's blood?", "The cervix is a passage, not a filter."]),
    mcq("1.3.2", "The part of the brain that controls heart rate A: Corpus callosum · B: Medulla oblongata", AB, 1,
        ["The heart rate is not under conscious control.", "The corpus callosum joins the two halves of the cerebrum."]),
    mcq("1.3.3", "The area on the retina where there are no rods or cones A: Blind spot · B: Cornea", AB, 0,
        ["Is the cornea part of the retina?", "Where the optic nerve leaves the eye there is no room for receptors."]),
]
ln = lambda n, q, letter, names, clues: {"t": "lettername", "n": n, "marks": 2, "q": q, "clues": clues, "letters": LET, "a": {"letter": letter, "name": names}}
q14 = [
    # ALTERNATIVE PAIRS (flagged): the memo accepts C – urethra OR D – penis; the catalogue holds one letter
    ln("1.4.1(a)", "Give the LETTER and NAME of the structure that forms part of both the urinary and reproductive systems", "C", ["urethra"],
       ["Urine and semen leave the body the same way.", "Follow the tube that runs from the bladder to the outside."]),
    ln("1.4.1(b)", "Give the LETTER and NAME of the structure that stores sperm temporarily", "B", ["epididymis"],
       ["Sperm mature here before they move on.", "It is the coiled tube lying against the testis."]),
    ln("1.4.1(c)", "Give the LETTER and NAME of the structure that secretes testosterone", "E", ["testis", "testes"],
       ["Testosterone is made where sperm are made.", "It hangs in the scrotum."]),
    term("1.4.2(a)", "Identify part A", ["prostate gland", "prostate"],
         ["It is a gland just below the bladder.", "Its fluid is part of semen."]),
    term("1.4.2(b)", "Identify the type of gametogenesis that takes place in part E", ["spermatogenesis"],
         ["Gametogenesis is named after the gamete it makes.", "Which gamete does a male make?"]),
]
q15 = [
    {"t": "pickn", "n": "1.5.1", "marks": 2, "q": "Write the LETTERS of the parts that serve as endocrine glands only.",
     "clues": ["A gland that makes both hormones and digestive juices is not an endocrine gland ONLY.", "Look for glands that release hormones into the blood and nothing else."],
     "opts": ["A", "B", "C", "D", "E", "F"], "pool": [0, 5], "count": 2},
    # TWO LETTER + NAME PAIRS IN ONE PART (flagged no_fit): self-checked until the catalogue has a fitting type
    {"t": "draw", "n": "1.5.2", "marks": 4, "q": "Give the LETTERS and NAMES of the parts responsible for the regulation of body temperature.",
     "clues": ["The body loses heat through the skin in two ways.", "One part carries warm blood near the surface; the other makes sweat."],
     "criteria": [{"text": "B – capillaries / blood vessel", "marks": 2}, {"text": "C – sweat gland", "marks": 2}]},
    term("1.5.3(a)", "Name the hormone secreted by part A (the regulation of water content in the blood)", ["ADH", "antidiuretic hormone"],
         ["It is released when the blood has too little water.", "It makes the kidney tubules take more water back."]),
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
     "figure": fig(7, (129, 124, 471, 360), "Front view of the male reproductive system, with the bladder at the top. A: the gland just "
                   "below the bladder, around the tube that leaves it. B: the coiled part against the testis on the right of the picture. C: the tube running down "
                   "the middle of the penis. D: the penis. E: the testis on the left of the picture.")},
    {"id": "1.5", "title": "Question 1.5", "kind": "Homeostasis", "marks": 8,
     "lead": "The diagram below represents some structures involved in homeostasis in the human body.", "items": q15,
     "figure": fig(8, (114, 130, 508, 400), "The upper body with some organs, and an enlarged part of the skin. A: a small gland at the base "
                   "of the brain. B: the network of vessels under the skin's surface. C: the coiled structure in the skin with a duct to the "
                   "surface. D: the organ behind the stomach. E: the kidney on the right of the picture. F: the small structure on top of the kidney on the left of the picture.")},
]
paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}],
    "flags": [
        {"n": "1.1.6", "kind": "no_fit", "detail": "The options are a table (MUSCLE IN X | STRUCTURE Y | PART Z); flattened into lines until the MCQ card can show table options."},
        {"n": "1.4.1(a)", "kind": "memo_issue", "detail": "The memo accepts C – urethra OR D – penis; the catalogue holds one letter, so D – penis is marked wrong for now."},
        {"n": "1.5.2", "kind": "no_fit", "detail": "Two LETTER + NAME pairs in one part (4 marks); self-checked until the catalogue has a type for it."},
        {"n": "paper", "kind": "low_confidence", "detail": "Question 1 (Section A) only, hand-transcribed from the paper and memo PDFs; no API call. Section B is not in yet."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Question 1"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
print("parts:", sum(len(m["items"]) for m in missions), "marks:", sum(i["marks"] for m in missions for i in m["items"]))
