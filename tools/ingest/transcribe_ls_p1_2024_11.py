"""Life Sciences P1 Nov 2024, Questions 1 and 2, hand-transcribed into the catalogue format (as if Claude had produced it), then run through
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
    # options printed as a TABLE: optTable carries it; opts read each row as a line (the medal card, the memo)
    mcq("1.1.6", "The diagram represents a part of the human eye. A spectator in a soccer stadium is seated 200 metres away from the field. "
        "Which ONE of the following describes the condition of structures X, Y and Z when he looks at the ball placed in the middle of the field?",
        ["Muscle in X relaxed · Structure Y slack · Part Z more convex", "Muscle in X contracted · Structure Y slack · Part Z less convex",
         "Muscle in X relaxed · Structure Y taut · Part Z less convex", "Muscle in X contracted · Structure Y taut · Part Z more convex"], 2,
        ["200 metres is far away: the eye is focusing on a distant object.", "For a distant object the lens has to bend the light less."],
        figure=fig(4, (211, 110, 384, 266), "Part of the human eye in section. X points to the ciliary body above the lens, Y to the "
                   "suspensory ligament below it, and Z to the lens."),
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
    # the memo accepts C – urethra OR D – penis (`or`); "C – penis" earns the letter mark only (Murci, 2026-10-05)
    {**ln("1.4.1(a)", "Give the LETTER and NAME of the structure that forms part of both the urinary and reproductive systems", "C", ["urethra"],
          ["Urine and semen leave the body the same way.", "Follow the tube that runs from the bladder to the outside."]),
     "or": [{"letter": "D", "name": ["penis"]}]},
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
    # two LETTER + NAME pairs in one part, any order
    {"t": "letternames", "n": "1.5.2", "marks": 4, "q": "Give the LETTERS and NAMES of the parts responsible for the regulation of body temperature.",
     "clues": ["The body loses heat through the skin in two ways.", "One part carries warm blood near the surface; the other makes sweat."],
     "letters": ["A", "B", "C", "D", "E", "F"], "count": 2,
     "pool": [{"letter": "B", "name": ["capillaries", "capillary", "blood vessel", "blood vessels"]}, {"letter": "C", "name": ["sweat gland", "sweat glands"]}]},
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
# ---- Question 2 (Section B), from the question paper pages 9-13 and the memo pages 5-6 ----
lst = lambda n, q, count, marks, pool, clues: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
rub = lambda n, q, marks, bullets, clues, **kw: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **kw}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
q21 = [
    term("2.1.1(a)", "Identify part A", ["fallopian tube", "fallopian tubes"],
         ["It carries the ovum from the ovary towards the uterus.", "Fertilisation normally happens in it."]),
    term("2.1.1(b)", "Identify part B", ["ovary", "ovaries"],
         ["It makes the ova.", "It also makes oestrogen and progesterone."]),
    # (a list: an answer scores when it holds an accepted answer's first word, so each group leads with its key word)
    lst("2.1.2(a)", "Give TWO characteristics of the endometrium that make it suitable for implantation", 2, 2,
        [["blood", "vascular", "rich blood supply"], ["glandular", "glands"], ["thick", "thickened"]],
        ["Think of what an embryo needs from the wall it sinks into.", "Look at how thick the lining is, and what it carries."]),
    lst("2.1.2(b)", "Give TWO visible reasons why there is an increased chance of fertilisation in this female", 2, 2,
        [["sperm", "sperm cells are present"], ["ovulation", "ovum has been released", "egg has been released"]],
        ["Look at what is swimming in the tube.", "Look at what has just left the ovary."]),
    rub("2.1.3", "Identify and describe the type of gametogenesis that leads to the formation of structure C.", 6,
        ["During oogenesis (compulsory)", "diploid cells in the ovary undergo mitosis", "to form numerous follicles", "at the onset of puberty",
         "under the influence of FSH", "one cell inside a follicle enlarges and undergoes meiosis",
         "of the four cells produced, only one survives to form a mature haploid ovum"],
        ["Structure C is a female gamete: name the process first.", "Go in order: mitosis to make follicles, then puberty, FSH and meiosis."]),
    rub("2.1.4", "In an ectopic pregnancy, the fertilised ovum can become implanted in part A. This normally results in the death of the embryo and may "
        "endanger the mother's life. Explain why an ectopic pregnancy may result in the death of an embryo.", 3,
        ["Part A (the fallopian tube) cannot provide the space", "and there is no endometrium / blood supply",
         "to provide nutrients / oxygen or remove waste products", "for the embryo to develop"],
        ["Compare the tube with the uterus wall.", "What does the endometrium give a growing embryo that the tube cannot?"]),
]
q22 = [
    num("2.2.1", "On which day of this menstrual cycle is the level of progesterone the highest?", 20, 0.001, "",
        ["Read down the progesterone column only.", "Find its biggest number, then read the day beside it."]),
    term("2.2.2", "Name the reproductive hormone that will begin to increase from day 24 of this female's menstrual cycle.", ["FSH", "follicle stimulating hormone"],
         ["A new cycle is about to begin.", "This hormone starts a new follicle growing."]),
    rub("2.2.3", "Use data from the table to explain your answer to QUESTION 2.2.2.", 2,
        ["The progesterone level is decreasing (from 5 to 0,8 ng/mℓ)", "therefore FSH secretion is no longer inhibited"],
        ["Look at progesterone from day 24 to day 28.", "High progesterone holds a hormone back. What happens when it falls?"]),
    {"t": "steps", "n": "2.2.4", "marks": 3, "q": "Calculate the percentage increase in the oestrogen level from day 8 to day 10. Show ALL your working.",
     "clues": ["Find how much the level went up first.", "Then divide that by the day 8 level and multiply by 100."],
     "steps": [{"id": "s1", "label": "Increase from day 8 to day 10 (pg/mℓ)", "marks": 1, "a": 210, "tol": 0.5, "memo": "280 − 70 = 210 ✓"},
               {"id": "s2", "label": "Percentage increase (%)", "marks": 2, "a": 300, "tol": 0.5, "memo": "210 ÷ 70 × 100 ✓ = 300% ✓"}]},
    term("2.2.5", "How would the progesterone level differ after day 20 if this female was pregnant?",
         ["remains high", "it remains high", "remain high", "stays high", "it stays high", "will increase", "it will increase", "increases", "it increases"],
         ["Pregnancy needs the uterus lining kept in place.", "Which hormone keeps the lining, and would it fall?"]),
    rub("2.2.6", "Explain what causes the change in the progesterone level stated in QUESTION 2.2.5.", 2,
        ["The corpus luteum does not disintegrate", "and continues to secrete progesterone", "OR — The placenta develops", "which secretes progesterone"],
        ["Which structure makes progesterone after ovulation?", "In a pregnancy, what keeps it going, and what takes over later?"]),
]
q23 = [
    term("2.3.1", "According to the passage, which type of cataract is associated with a disorder of the pancreas?",
         ["subcapsular cataracts", "subcapsular cataract", "subcapsular", "sub capsular cataracts", "sub capsular"],
         ["Which disorder of the pancreas is named in the passage?", "Find the type of cataract the passage links to it."]),
    rub("2.3.2", "Use information in the passage to explain why cataracts cause vision loss.", 5,
        ["Protein structures in the lens start to disintegrate and clump together", "The lens becomes opaque / milky",
         "less / no light passes through the lens", "onto the retina", "therefore less / no stimuli are converted to impulses"],
        ["Start with what the passage says happens to the proteins in the lens.", "Follow the light: through the lens, to the retina, to impulses."]),
]
q24 = [
    rub("2.4.1", "Explain how the structure of his eyeball affects his vision when he reads a book without glasses", 3,
        ["The eyeball is too short", "The image forms behind the retina", "causing blurred vision",
         "OR — The cornea is less convex", "Less refraction occurs / the image forms behind the retina", "causing blurred vision"],
        ["A book is close: the light has to be bent a lot.", "Where does the image fall if the eyeball is short?"]),
    rub("2.4.2", "Explain how wearing glasses with convex lenses will improve his vision when he reads a book", 2,
        ["The light rays will be refracted more", "causing the image to fall on the retina"],
        ["A convex lens bends light inwards.", "Where does the image fall now?"]),
]
q25 = [
    term("2.5.1", "Identify the type of neuron shown in the diagrams.", ["motor neuron", "motor neurone", "motor neurons"],
         ["Look at where the cell body is.", "Which neuron carries impulses to a muscle?"]),
    lst("2.5.2", "Give ONE visible reason for your answer to QUESTION 2.5.1.", 1, 1,
        [["dendrites", "many dendrites", "multipolar"], ["cell body", "cell body at one end"], ["long", "long axon", "axon is long"]],
        ["Look at the cell body and the branches around it.", "Compare the lengths of the axon and the dendrites."]),
    rub("2.5.3", "Describe the function of the type of neuron identified in QUESTION 2.5.1.", 3,
        ["It transmits impulses", "from the central nervous system / interneuron", "to the effector"],
        ["What does this neuron carry?", "From where, and to what?"]),
    {"t": "order", "n": "2.5.4", "marks": 2, "q": "Use the letters A, B and C to indicate the direction in which an impulse moves through the neuron.",
     "clues": ["An impulse enters a neuron through its dendrites.", "It leaves through the axon's branched ends."], "opts": ["A", "B", "C"], "a": [2, 0, 1]},
    term("2.5.5", "Name the disorder associated with degeneration of the myelin sheaths of neurons.", ["multiple sclerosis", "MS"],
         ["The myelin is attacked and scars form.", "Its name means \"many scars\"."]),
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
        ["As the axon diameter increases, the impulse speed increases"],
        ["Both lines go the same way.", "As one value goes up, what does the other do?"], each=2),
]
missions_b = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Female reproduction", "marks": 15,
     "lead": "The diagram below represents a part of the female reproductive system.", "items": q21,
     "figure": fig(9, (104, 160, 522, 441), "Part of the female reproductive system. A: the curved tube arching over the ovary, with sperm cells "
                   "swimming in it. B: the oval ovary below it. C: a small round cell just released beside the ovary. On the right, the endometrium "
                   "lines the uterus, and more sperm cells are swimming towards it.")},
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
     "figure": fig(13, (98, 168, 552, 403), "Two straight-line graphs of impulse speed (m/s) against axon diameter (µm). Myelinated neuron: "
                   "5 µm 20, 10 µm 40, 15 µm 60, 20 µm 80, 25 µm 100, 30 µm 120 m/s. Unmyelinated neuron: 200 µm 5, 400 µm 10, 600 µm 15, "
                   "800 µm 20, 1000 µm 25, 1200 µm 30 m/s.")},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}, {"title": "Section B", "total": 100, "missions": missions_b}],
    "flags": [
        {"n": "1.4.1(a)", "kind": "low_confidence", "detail": "The memo accepts C – urethra OR D – penis. Marked: either letter earns its mark, the name only when it names the part of the letter chosen ('C – penis' = 1). A Life Sciences teacher should confirm."},
        {"n": "2.1.3", "kind": "no_fit", "detail": "The memo makes 'oogenesis' a COMPULSORY mark (1) + any 5; the written-answer marker has no compulsory point, so it is not enforced."},
        {"n": "2.5.4", "kind": "low_confidence", "detail": "An order of LETTERS (C → A → B): the letter balls need a sequence design (shown to Murci first)."},
        {"n": "paper", "kind": "low_confidence", "detail": "Questions 1 and 2, hand-transcribed from the paper and memo PDFs; no API call. Question 3 is not in yet."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Questions 1 and 2"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]))
