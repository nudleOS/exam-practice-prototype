"""Grade 10 Physical Sciences P2 (Chemistry) Nov 2017 (DBE common paper), the whole paper (Questions 1 to 9), hand-transcribed into the
catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper draws the 1.2 heating curve, the 1.6 flow
chart, the 2.5 models, the 2.6 diagram, the Q3 graph (an image), the Q7 circuit and the Q9 cycle, and the memo sets its Lewis diagrams
and every working as images (its text layer turns fractions into columns of digits).

  python tools/ingest/transcribe_g10_ps_p2_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Physical Sciences P2 Nov 2017 Eng.pdf" "uploads/Grade 10 Physical Sciences P2 Nov 2017 MG Eng & Afr.pdf" --id g10-ps-p2-2017-11 --from-json

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; models: transcribe_ps_p2_2025_11.py, Chemistry, and the Grade 10
transcribe_g10_ps_p2_2018_11.py):
  multiple choice printed in the paper -> mcq as printed (1.6's options printed as a table -> optTable); a choice printed in the stem or
  list with no explanation in the same part (2.1.2-2.1.4 a substance from the list, 2.6.1 physical or chemical, 2.7.x and 7.9.1
  INCREASE / DECREASE / REMAIN THE SAME, 5.3, 6.1 REDOX or GAS FORMING, 8.1 a chemical from the list) -> mcq of the printed choices;
  2.1.1, whose memo accepts two ("CO2 OR H2O"), is a pick of one with both right. One term the memo names -> term; a chemical name or
  formula (2.5.1 potassium iodide, 2.5.2 CH4, 8.4 barium carbonate) -> strict term. The sp-notations of 3.3.1 (superscripts cannot be
  typed) play as answer multiple choice. The seven table cells of 4.2 (a number each, no working) -> num.
  Every calculation -> authored multiple choice, `work`: the memo's FIRST working line by line and three workings each built from a
  DIFFERENT realistic chemistry error (a mole ratio wrong, a formula upside down, a wrong molar mass, cm3 not converted, a mass added
  not subtracted, the wrong sample, a gas that is a liquid counted), every number recomputed; 0 or full marks. A value the memo also
  accepts, and a memo slip's value, is never a wrong option. "Write down / Use a balanced chemical equation" (7.3, 8.2, 8.3) ->
  multiple choice of four equations, the memo's marks all or nothing; an ion the learner would type is never a typed term (the term
  check drops charge signs).
  A definition or law -> statements (pick 1 card for its marks; an OR form a second right card); an explanation, a reason or a choice
  with its reason -> statements, the memo's marks per point. No memo here weighs two sides, so no part plays as a sort.
  Drawings (2.2 the Lewis diagram of CO2, 2.4 the formation of NaCl) -> draw with the memo's criteria, self-checked (flagged no_fit).
  A part whose stem, options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose lead or diagram changes part-way is several missions (2, 2.5, 2.6, 2.7; 4 and 4.2; 6, 6.2, 6.3).
Figure boxes are measured in PDF points (page 595.32 x 841.92, read from the PDF) tight to the ink (drawings, images and labels) and
checked on a contact sheet of the 1%-padded crops (scratchpad lower/g10-ps-p2-2017-11/figs.py); 1.6's top sits 1.7 pt below the "Yes"
ink so the padded crop stays clear of the stem line above it."""
import json
import random
import re
from pathlib import Path

PID = "g10-ps-p2-2017-11"
W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.2": [3, 176.5, 355.5, 402.0, 494.0], "1.6": [4, 118.0, 425.5, 479.5, 606.0], "Q2.5": [6, 99.8, 433.5, 538.6, 579.1],
    "Q2.6": [7, 110.6, 161.7, 512.6, 281.2], "Q3": [8, 63.0, 143.0, 507.4, 395.0], "Q7": [11, 218.0, 189.5, 371.4, 338.5],
    "Q9": [13, 160.1, 138.0, 405.3, 366.3]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def pick1(n, q, opts, pool, clues, marks=1):
    """Choose ONE: every index in `pool` is right (a printed choice whose memo accepts two answers)."""
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": 1}


# notes: the memo's marking notes that are NOT points: never scored, never shown
# kw: catalogue extras the played part keeps (after=[...] when its cards show an earlier part's answer)
rub = lambda n, q, marks, bullets, clues, each=None, notes=None, **kw: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues,
                                                                       "bullets": bullets, **({"each": each} if each else {}),
                                                                       **({"notes": notes} if notes else {}), **kw}
term = lambda n, q, a, clues, marks=1, strict=False: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                      **({"strict": True} if strict else {})}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="", **kw: {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                           "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {}), **kw}

WORK = "\n\nChoose the correct working."
EQ = "\n\nChoose the correct equation."   # a "Write down / Use a balanced chemical equation" played as multiple choice of four
AUTHORED = []   # the calculations played as authored multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues, **kw):
    """A calculation as authored multiple choice (Murci, 2026-10-10): opts are the memo's FIRST working and three workings built
    from realistic chemistry errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing.
    kw: catalogue extras, e.g. after=[...] when the options show an earlier part's answer."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


CHANGE = ["Increase", "Decrease", "Remain the same"]
LIST2 = ["C₉₀", "NaCℓ", "CO₂", "Fe", "H₂O"]   # the substances Question 2 lists, in the paper's order

# ---- QUESTION 1: multiple choice, the question paper pages 3-5 and the memo page 2 ----
q1 = [
    mcq("1.1", "Air can be classified as a/an …", ["element.", "compound.", "homogenous mixture.", "heterogeneous mixture."], 2,
        ["Is air made of one substance, or of several substances mixed together?", "Can you see the different parts of air, or is it the same "
         "throughout?"]),
    mcq("1.2", "The graph below shows the heating curve of a substance. In which part(s) of the graph does the substance gain kinetic energy?",
        ["BC only", "CD only", "AB and CD", "AB, BC and CD"], 0,
        ["Which quantity on the graph tells you how the average kinetic energy of the particles changes?",
         "Where does the energy go while a substance is changing phase?"],
        figure=fig("1.2", "A heating curve: temperature (°C) up against time (s) across, with 100 marked on the temperature axis; the line runs "
                   "through the points A, B, C and D in turn.")),   # (no slopes: which sections rise and which run level is the question)
    mcq("1.3", "In which ratio will group (I) elements react with group (VI) elements?", ["2 : 1", "1 : 6", "6 : 1", "1 : 3"], 0,
        ["How many electrons does a group (I) atom give away when it forms an ion?",
         "How many electrons does a group (VI) atom need to fill its outer energy level?"]),
    mcq("1.4", "What is the total number of nucleons in the ion of calcium when calcium loses two electrons to form Ca²⁺?", ["40", "18", "22", "20"], 0,
        ["Which particles of an atom are nucleons?", "Does losing electrons change the nucleus of an atom?"]),
    # the memo: C (the general trend down group 1; potassium is in fact less dense than sodium: flagged)
    mcq("1.5", "Which ONE of the following groups of elements shows the CORRECT trend of the density of metals?",
        ["Rb < K < Na < Li", "K < Na < Li < Rb", "Li < Na < K < Rb", "Na < Li < Rb < K"], 2,
        ["In which order are Li, Na, K and Rb found in group 1, from top to bottom?",
         "As you go down group 1, does the mass of an atom grow faster or slower than its size?"]),
    mcq("1.6", "A learner used the flow chart below to classify some examples of substances P, Q and R. What could substances P, Q and R possibly "
        "be?", ["Marble; Oil; Oxygen", "Oil; Marble; Oxygen", "Oxygen; Oil; Marble", "Oxygen; Marble; Oil"], 0,
        ["Which phase of matter has a definite shape, and which has a definite volume but no definite shape?",
         "Follow the flow chart: which substance answers 'No' to both questions?"],
        optTable={"head": ["P", "Q", "R"], "rows": [["Marble", "Oil", "Oxygen"], ["Oil", "Marble", "Oxygen"], ["Oxygen", "Oil", "Marble"],
                                                    ["Oxygen", "Marble", "Oil"]]},
        figure=fig("1.6", "A flow chart: Substance (P, Q, R) leads to 'Definite shape'; Yes leads to P, No leads down to 'Definite volume'; Yes "
                   "leads to Q, No leads down to R.")),
    mcq("1.7", "In a 20 g sample of molecules, which sample below has the greatest number of moles?", ["NH₃", "N₂", "CO₂", "H₂"], 3,
        ["Which formula links the number of moles to the mass and the molar mass?", "For the same mass, does a larger molar mass give more moles "
         "or fewer?"]),
    mcq("1.8", "Carbon dioxide can change directly from the solid phase to the gas phase. This process is known as …",
        ["sublimation.", "evaporation.", "decomposition.", "melting."], 0,
        ["Between which phases does a substance change when it evaporates, and when it melts?",
         "Is a new substance formed when carbon dioxide changes phase?"]),
    mcq("1.9", "The chemical name for Fe₂(SO₄)₃ is …", ["iron sulphite.", "iron(III) sulphate.", "iron(II) sulphate.", "iron sulphide."], 1,
        ["What do the endings -ate, -ite and -ide tell you about the negative ion?",
         "How do you work out the charge on each iron ion from the formula Fe₂(SO₄)₃?"]),
    mcq("1.10", "All the soil on Earth is known as the …", ["atmosphere.", "biosphere.", "lithosphere.", "hydrosphere."], 2,
        ["Which sphere holds the living things, which the water, and which the air?", "Is soil part of the air, the water, or the Earth's crust?"]),
]

# ---- QUESTION 2, the question paper pages 6-7 and the memo page 3 ----
SUB = "Write down a substance from the list above that is the following: "
q2a = [
    # the memo: "CO2 OR H2O" (either earns the mark): a pick of one with both right
    pick1("2.1.1", SUB + "a molecular structure.", LIST2, [2, 4],
          ["Which of the substances are made of separate small groups of non-metal atoms?", "Which substances contain a metal, and so cannot be "
           "molecular?"]),
    mcq("2.1.2", SUB + "a metallic structure.", LIST2, 3,
        ["What kind of element forms a metallic structure?", "Which of the five substances are made of one element only, and is each a metal or a "
         "non-metal?"], marks=1),
    # the memo: C₉₀ (a fullerene is a molecule, not a covalent network: flagged; kept as the memo marks it)
    mcq("2.1.3", SUB + "a covalent network structure.", LIST2, 0,
        ["Which element forms giant structures such as diamond and graphite?", "Which substance in the list is made of atoms of one non-metal only?"],
        marks=1),
    mcq("2.1.4", SUB + "an ionic network structure.", LIST2, 1,
        ["What kinds of particles make up an ionic network?", "Which substance is made of a metal and a non-metal bonded together?"], marks=1),
    draw("2.2", "Draw the Lewis dot diagram for the CO₂ molecule.", 2, [
        ["Two shared electron pairs (a double bond) between the C atom and each O atom", 1],
        ["Two lone pairs on each O atom, and no lone pair on the C atom", 1]],
        ["How many valence electrons do carbon and oxygen atoms have?",
         "How many electrons must each oxygen atom share with carbon to fill its outer energy level?"],
        memo="O::C::O, each O with two lone pairs (the memo draws the O electrons as dots and the C electrons as crosses).",
        after=["2.1.1"]),   # its stem calls CO₂ a molecule (2.1.1's answer)
    term("2.3", "Identify the type of chemical bond in H₂O.", ["Covalent bond", "Covalent", "Covalent bonding", "Covalent bonds"],
         ["Are hydrogen and oxygen metals or non-metals?", "Do the atoms in water share electrons, or transfer them?"]),
    draw("2.4", "Draw the Lewis dot diagrams to show the formation of NaCℓ.", 3, [
        ["Na× → Na⁺ + e⁻: the sodium atom loses its one valence electron", 1],
        ["Cℓ with seven electrons + e⁻ → [Cℓ with eight electrons]⁻", 1],
        ["Na× + Cℓ (seven electrons) → Na⁺[Cℓ (eight electrons)]⁻", 1]],
        ["How many valence electrons do sodium and chlorine atoms have?", "Which atom gives away an electron, and which takes it?"],
        memo="Na× → Na⁺ + e⁻; Cℓ (seven dots) + e⁻ → [Cℓ (seven dots and one cross)]⁻; Na× + Cℓ → Na⁺[Cℓ]⁻.",
        after=["2.1.4"]),   # its criteria: NaCℓ formed of Na⁺ and Cℓ⁻ ions (2.1.4's ionic network)
]
q2b = [
    term("2.5.1", "Write down the chemical name of compound A.", ["Potassium iodide"],
         ["What do the K⁺ and I⁻ labels in model A stand for?", "How is a compound of a metal and a non-metal named: which part gets the ending -ide?"],
         strict=True),
    term("2.5.2", "Write down the chemical formula of compound B.", ["CH4"],
         ["Which atoms make up model B, and how many of each?", "How do you show the number of atoms of an element in a chemical formula?"],
         strict=True),
    term("2.5.3", "Write down the common name of compound C.", ["Ammonia"],
         ["Which atoms make up model C, and how many of each?",
          "Some compounds have common names instead of chemical names, like water for H₂O: which one have you learnt for this compound?"]),
]
q2c = [
    mcq("2.6.1", "Is this separation process physical or chemical?", ["Physical", "Chemical"], 0,
        ["Are new substances formed when liquid air is separated?", "Does boiling change the molecules of a gas, or only its phase?"], marks=1),
    term("2.6.2", "Which physical property is used to separate the gases after they have been liquefied?", [
        "Boiling point", "Boiling points", "Difference in boiling points", "Difference in boiling point"],
         ["What is written beside each arrow leaving the liquid air?", "What does each gas do at its own temperature as the liquid air warms up?"]),
    rub("2.6.3", "Which gas has the weakest intermolecular forces? Explain the answer.", 2, [
        "Nitrogen. (1)", "It has the lowest boiling point. (1)"],
        ["Does a liquid with weak intermolecular forces need much or little energy to boil?",
         "Compare the three temperatures in the diagram: which is the coldest?"],
        after=["2.6.2"]),   # its cards: the boiling point (2.6.2's answer)
]
P27 = " (when liquid nitrogen changes into gaseous nitrogen)"
q2d = [
    mcq("2.7.1", "Spaces between the particles" + P27, CHANGE, 0,
        ["How do the particles of a gas move compared with the particles of a liquid?", "Can a gas be squashed into a smaller space more easily than "
         "a liquid?"], marks=1),
    mcq("2.7.2", "Strength of the forces between the particles" + P27, CHANGE, 1,
        ["What must happen to the forces between the particles for them to escape from the liquid?",
         "Are gas particles held together as strongly as liquid particles?"], marks=1),
    mcq("2.7.3", "Energy of the particles" + P27, CHANGE, 0,
        ["Is energy taken in or given out when a liquid boils?", "Where does that energy go?"], marks=1),
]

# ---- QUESTION 3, the question paper page 8 and the memo page 4 ----
P33 = "There is a drop in ionisation energy from beryllium to boron. "
P35 = "Study the ionisation energy of the group (I) elements in the graph above. "
q3 = [
    rub("3.1", "Define the term ionisation energy.", 2, ["Energy needed per mole to remove an electron from an atom in a gaseous phase. (2)"],
        ["What happens to an atom when it is ionised?", "Is energy taken in or given out when an electron is pulled away from the nucleus?"],
        each=2),
    rub("3.2", "State the general trend in ionisation energy from left to right across a period on the periodic table.", 2, [
        "Ionisation energy increases from left to right, across a period. (2)"],
        ["Use the graph: how does the ionisation energy change from Li to Ne, if you ignore the small drops?",
         "What happens to the number of protons in the nucleus as you move across a period?"], each=2),
    # the memo: Be: 1s² 2s² (2), B: 1s² 2s² 2p¹ (2). Superscripts cannot be typed: an answer multiple choice of four pairs, all or nothing.
    # Wrong: the electrons counted from the mass numbers (9 and 11), the 2s and 2p filled one electron each, three electrons in the 2s
    mcq("3.3.1", P33 + "Write down the sp-notation for beryllium AND boron.", [
        "Be: 1s² 2s² 2p⁵; B: 1s² 2s² 2p⁶ 3s¹", "Be: 1s² 2s²; B: 1s² 2s² 2p¹", "Be: 1s² 2s¹ 2p¹; B: 1s² 2s¹ 2p²", "Be: 1s² 2s²; B: 1s² 2s³"], 1,
        ["How many electrons do beryllium and boron atoms have?",
         "In which order are the 1s, 2s and 2p orbitals filled, and how many electrons fit in one s orbital?"], marks=4),
    rub("3.3.2", P33 + "Explain this drop in ionisation energy.", 3, [
        "B has a 2p energy level; 2p has a higher energy than 2s. (1)", "Therefore less energy is needed to remove the valence electrons from B "
        "as from Be. (2)", "OR — 2s electrons are paired and 2p electron is unpaired. (1) Therefore less energy needed to remove 2p electron. (2)"],
        ["In which orbital is the outermost electron of Be, and in which is that of B?",
         "Is an electron in a higher-energy orbital easier or harder to remove?"],
        after=["3.3.1"]),   # its cards: B's outer electron in a 2p level (3.3.1's sp-notation of B)
    rub("3.4", "Is the following statement TRUE or FALSE? If false, rewrite the statement correctly.\nThe ionisation energy of noble gases is high "
        "because of the half-filled s- and p-orbitals.", 2, [
        "False. (1)", "The energy is high because of filled s and p-orbitals. (1)"],
        ["How many electrons are in the outer s- and p-orbitals of a noble gas such as neon?",
         "Is a half-filled or a completely filled set of orbitals the more stable arrangement?"]),
    term("3.5.1", P35 + "Give the general name of the group (I) elements.", ["Alkali metals", "Alkali metal"],
         ["What do lithium, sodium and potassium have in common in the periodic table?",
          "What kind of solution do these elements form when they react with water?"]),
    rub("3.5.2", P35 + "State the trend in the reactivity of elements in group (I).", 2, ["Reactivity increases from top to bottom. (2)"],
        ["Which group (I) element reacts more violently with water: lithium or potassium?",
         "As you go down group (I), do the atoms get bigger or smaller?"], each=2),
    rub("3.5.3", P35 + "Explain the reason for the trend in QUESTION 3.5.2 by using the graph of ionisation energy.", 2, [
        "Ionisation energy decreases, thus less energy to remove an electron. Therefore reactivity increases. (2)"],
        ["Use the graph: how does the ionisation energy change from Li to Na to K?",
         "When an alkali metal reacts, does it lose or gain an electron?"], each=2,
        after=["3.5.2"]),   # its card: the reactivity increases down the group (3.5.2's answer)
]

# ---- QUESTION 4, the question paper page 9 and the memo page 5 ----
q4a = [
    rub("4.1.1", "Define the term isotope.", 2, [
        "Atoms of the same element having the same number of protons, but different number of neutrons. (2)",
        "OR — Same atomic number, but different mass numbers. (2)"],
        ["Think of chlorine-35 and chlorine-37: what is the same about their atoms, and what differs?",
         "Which particles make up the mass number of an atom?"], each=2),
    # the memo's working (108; it writes 50 x 108,9 in the fraction where the paper and its own line above give 109,1: flagged; its 108
    # follows from 109,1, and the slip's 107,9 is never an option). Wrong: the percentages left out, not divided by 100, the percentages
    # as fractions and still divided by 100
    work("4.1.2", "Calculate the relative atomic mass of element X.", 5, [
        "50% = 106,9 amu\n50% = 109,1 amu\nAᵣ = {106,9 + 109,1}/{100}\n= 2,16",                                   # the percentages left out
        "50% = 106,9 amu\n50% = 109,1 amu\nAᵣ = {(50 × 106,9) + (50 × 109,1)}/{100}\n= 108",                       # the memo
        "50% = 106,9 amu\n50% = 109,1 amu\nAᵣ = (50 × 106,9) + (50 × 109,1)\n= 10 800",                            # not divided by 100
        "50% = 106,9 amu\n50% = 109,1 amu\nAᵣ = {(0,5 × 106,9) + (0,5 × 109,1)}/{100}\n= 1,08"], 1,               # fractions AND ÷ 100
        ["What percentage of the atoms is the second isotope, if the first makes up 50%?",
         "How do you find a weighted average of the two isotope masses?"]),
    term("4.1.3", "Identify element X in QUESTION 4.1.2.", ["Ag", "Silver"],
         ["Which element has a relative atomic mass closest to your answer to 4.1.2?",
          "Where in the periodic table is the approximate relative atomic mass of each element printed?"], marks=2),
]
CELL = "Complete the table: write down the answer for "
q4b = [
    num("4.2.1", CELL + "4.2.1, the NUMBER OF PROTONS of Aℓ.", 13, 0, "",
        ["What does the atomic number of an element count?", "Is the number of protons the same in every atom of aluminium?"]),
    num("4.2.2", CELL + "4.2.2, the NUMBER OF NEUTRONS of Aℓ.", 14, 0, "",
        ["Which particles together make up the mass number?", "How do you find the number of neutrons from the mass number and the number of "
         "protons?"]),
    num("4.2.3", CELL + "4.2.3, the NUMBER OF ELECTRONS of Aℓ.", 13, 0, "",
        ["Is the aluminium in the table a neutral atom or an ion?", "In a neutral atom, how does the number of electrons compare with the number "
         "of protons?"]),
    num("4.2.4", CELL + "4.2.4, the MASS NUMBER of K⁺.", 39, 0, "",
        ["Where in the periodic table do you find the approximate relative atomic mass of potassium?",
         "Does losing an electron change the mass number of an atom?"]),
    num("4.2.5", CELL + "4.2.5, the NUMBER OF PROTONS of K⁺.", 19, 0, "",
        ["What does the atomic number of potassium tell you?", "Does an atom lose protons or electrons when it forms a positive ion?"]),
    num("4.2.6", CELL + "4.2.6, the NUMBER OF NEUTRONS of K⁺.", 20, 0, "",
        ["How do you find the number of neutrons from the mass number and the atomic number?", "Does forming an ion change the nucleus?"]),
    num("4.2.7", CELL + "4.2.7, the NUMBER OF ELECTRONS of K⁺.", 18, 0, "",
        ["What does the + sign on K⁺ tell you about its electrons?", "How many electrons does a neutral potassium atom have?"]),
]

# ---- QUESTION 5, the question paper page 9 and the memo pages 5-6 ----
q5 = [
    term("5.1", "What does the (aq) represent in the equation above?", ["An aqueous solution", "Aqueous solution", "Aqueous", "Dissolved in water"],
         ["What do the symbols (s), (ℓ) and (g) tell you about a substance?", "What is the hydrogen peroxide dissolved in?"]),
    rub("5.2", "Identify the type of reaction above. Choose between PRECIPITATION and REDOX. Give a reason for the answer.", 2, [
        "Redox. (1)", "Electron transfer took place. (1)"],
        ["Is a solid formed from two solutions in this reaction?",
         "What happens to the electrons when hydrogen peroxide breaks up into oxygen and water?"]),
    mcq("5.3", "Is the reaction an example of a physical or a chemical change?", ["Physical change", "Chemical change"], 1,
        ["Are new substances formed in this reaction?", "Are the products the same substance as the reactant?"], marks=1),
    rub("5.4", "Define the term one mole of a substance.", 2, [
        "The amount of substance having the same number of particles as there are atoms in 12 g C-12. (2)"],
        ["What is Avogadro's number, and what does it count?", "Which reference substance is used to define the mole?"], each=2),
    # the memo (44,8 dm³; no range): the 1 : 1 ratio, the formula upside down, the H₂O(ℓ) counted as gas
    work("5.5", "If 4 moles of hydrogen peroxide decomposes, calculate the volume of gas formed at STP.", 4, [
        "n(H₂O₂) : n(O₂) = 1 : 1\nn(O₂) = 4 mol\nn = {V}/{Vm}\n4 = {V}/{22,4}\nV = 89,6 dm³",                        # the 2 : 1 ratio not applied
        "n(H₂O₂) : n(O₂) = 2 : 1\nn(O₂) = 2 mol\nn = {Vm}/{V}\n2 = {22,4}/{V}\nV = 11,2 dm³",                        # the formula upside down
        "n(H₂O₂) : n(gas) = 2 : 3\nn(gas) = 6 mol\nn = {V}/{Vm}\n6 = {V}/{22,4}\nV = 134,4 dm³",                     # the water counted as gas
        "n(H₂O₂) : n(O₂) = 2 : 1\nn(O₂) = 2 mol\nn = {V}/{Vm}\n2 = {V}/{22,4}\nV = 44,8 dm³"], 3,                    # the memo
        ["Use the balanced equation: how many moles of O₂ form from 2 moles of H₂O₂?",
         "Which of the products is a gas at room temperature, and which is not?"]),
    # the memo (6,02 x 10²³ atoms; no range): the two O atoms a molecule left out, M(H₂O₂) as 18, the formula upside down
    work("5.6", "Calculate the number of oxygen atoms in H₂O₂ if 17 g of H₂O₂ decomposes.", 4, [
        "n(H₂O₂) = {m}/{M} = {17}/{34}\n= 0,5 mol\nn = {N}/{NA}\n(0,5)(2) = {N}/{6,02 × 10²³}\nN = 6,02 × 10²³ atoms",  # the memo
        "n(H₂O₂) = {m}/{M} = {17}/{34}\n= 0,5 mol\nn = {N}/{NA}\n0,5 = {N}/{6,02 × 10²³}\nN = 3,01 × 10²³ atoms",       # one O a molecule
        "n(H₂O₂) = {m}/{M} = {17}/{18}\n= 0,94 mol\nn = {N}/{NA}\n(0,94)(2) = {N}/{6,02 × 10²³}\nN = 1,13 × 10²⁴ atoms",  # M of H₂O, 18
        "n(H₂O₂) = {M}/{m} = {34}/{17}\n= 2 mol\nn = {N}/{NA}\n(2)(2) = {N}/{6,02 × 10²³}\nN = 2,41 × 10²⁴ atoms"], 0,  # upside down
        ["Which formula gives the number of moles from a mass?", "How many oxygen atoms are there in one H₂O₂ molecule?"]),
]

# ---- QUESTION 6, the question paper page 10 and the memo pages 6-8 ----
q6a = [
    mcq("6.1", "Identify the type of reaction above. Choose between REDOX and GAS FORMING.", ["Redox", "Gas forming"], 1,
        ["What do you see when sodium carbonate reacts with hydrochloric acid?",
         "Does any element change its charge (oxidation number) in this reaction?"], marks=1),
]
q6b = [
    # the memo (106 g·mol⁻¹): one Na, one O, the atomic numbers
    work("6.2.1", "Calculate the molar mass of sodium carbonate.", 2, [
        "M(Na₂CO₃) = 23 + 12 + 3(16)\n= 83 g·mol⁻¹",                                     # one Na
        "M(Na₂CO₃) = 2(23) + 12 + 16\n= 74 g·mol⁻¹",                                     # one O
        "M(Na₂CO₃) = 2(23) + 12 + 3(16)\n= 106 g·mol⁻¹",                                 # the memo
        "M(Na₂CO₃) = 2(11) + 6 + 3(8)\n= 52 g·mol⁻¹"], 2,                                # the atomic numbers used as masses
        ["Which relative atomic masses do you need from the periodic table?", "How many atoms of each element are in one Na₂CO₃?"]),
    # the memo (0,1 mol): upside down, M as 83, n = mM
    work("6.2.2", "Calculate the initial number of moles of sodium carbonate.", 2, [
        "n(Na₂CO₃) = {M}/{m}\n= {106}/{10,6}\n= 10 mol",                                 # upside down
        "n(Na₂CO₃) = {m}/{M}\n= {10,6}/{83}\n= 0,13 mol",                                # one Na in M
        "n(Na₂CO₃) = mM\n= (10,6)(106)\n= 1 123,6 mol",                                  # multiplied
        "n(Na₂CO₃) = {m}/{M}\n= {10,6}/{106}\n= 0,1 mol"], 3,                            # the memo
        ["Which formula links the number of moles, the mass and the molar mass?", "Which molar mass did you work out in 6.2.1?"],
        after=["6.2.1"]),   # the options show 6.2.1's 106
    # the memo (4,4 g): the 1 : 2 ratio, M of CO (28), upside down
    work("6.2.3", "Calculate the mass of CO₂ produced during this reaction.", 4, [
        "n(Na₂CO₃) : n(CO₂) = 1 : 2\nn(CO₂) = 0,2 mol\nn(CO₂) = {m}/{M}\n0,2 = {m}/{44}\nm = 8,8 g",               # 1 : 2
        "n(Na₂CO₃) : n(CO₂) = 1 : 1\nn(CO₂) = 0,1 mol\nn(CO₂) = {m}/{M}\n0,1 = {m}/{44}\nm = 4,4 g",               # the memo
        "n(Na₂CO₃) : n(CO₂) = 1 : 1\nn(CO₂) = 0,1 mol\nn(CO₂) = {m}/{M}\n0,1 = {m}/{28}\nm = 2,8 g",               # M of CO
        "n(Na₂CO₃) : n(CO₂) = 1 : 1\nn(CO₂) = 0,1 mol\nn(CO₂) = {M}/{m}\n0,1 = {44}/{m}\nm = 440 g"], 1,           # upside down
        ["Use the balanced equation: how many moles of CO₂ form for each mole of Na₂CO₃?", "What is the molar mass of CO₂?"],
        after=["6.2.2"]),   # the options show 6.2.2's 0,1 mol
    # the memo writes m = 25,16 g, but its own 0,434 x 58,5 = 25,39 g (flagged): the right option ends 25,39 g and 25,16 g is never an
    # option. Wrong: the 1 : 1 ratio, the formula upside down, M(NaCℓ) with Cℓ₂ (71)
    work("6.2.4", "Calculate the mass of sodium chloride produced if 4,87 dm³ of carbon dioxide was produced at STP.", 6, [
        "n(CO₂) = {V}/{Vm}\n= {4,87}/{22,4}\n= 0,217 mol\nn(CO₂) : n(NaCℓ) = 1 : 2\nn(NaCℓ) = 0,434 mol\nn(NaCℓ) = {m}/{M}\n"
        "0,434 = {m}/{58,5}\nm = 25,39 g",                                                                    # the memo (its slip corrected)
        "n(CO₂) = {V}/{Vm}\n= {4,87}/{22,4}\n= 0,217 mol\nn(CO₂) : n(NaCℓ) = 1 : 1\nn(NaCℓ) = 0,217 mol\nn(NaCℓ) = {m}/{M}\n"
        "0,217 = {m}/{58,5}\nm = 12,69 g",                                                                    # 1 : 1
        "n(CO₂) = {Vm}/{V}\n= {22,4}/{4,87}\n= 4,60 mol\nn(CO₂) : n(NaCℓ) = 1 : 2\nn(NaCℓ) = 9,20 mol\nn(NaCℓ) = {m}/{M}\n"
        "9,20 = {m}/{58,5}\nm = 538,2 g",                                                                     # upside down
        "n(CO₂) = {V}/{Vm}\n= {4,87}/{22,4}\n= 0,217 mol\nn(CO₂) : n(NaCℓ) = 1 : 2\nn(NaCℓ) = 0,434 mol\nn(NaCℓ) = {m}/{M}\n"
        "0,434 = {m}/{94}\nm = 40,80 g"], 0,                                                                  # M with Cℓ₂: 23 + 71
        ["Which formula gives the number of moles of a gas from its volume at STP?",
         "Use the balanced equation: how many moles of NaCℓ form for each mole of CO₂?"]),
]
q6c = [
    # the memo's Option 1 (x = 10; its Option 2 writes M(Na₂CO₃) = 160 but divides as by 106: flagged). Wrong: the masses added, the
    # hydrated 14,2 g used as the Na₂CO₃, one Na in M (83)
    work("6.3", "Calculate the number of moles of water of crystallisation in the sodium carbonate sample, if 5,3 g of solid remained after strong "
         "heating.", 5, [
        "m(H₂O) = 14,2 + 5,3\n= 19,5 g\nn(Na₂CO₃) = {m}/{M} = {5,3}/{106}\n= 0,05 mol\nn(H₂O) = {m}/{M} = {19,5}/{18}\n= 1,08 mol\n"
        "n(Na₂CO₃) : n(H₂O) = 0,05 : 1,08\n= 1 : 21,6\nx = 22",                                               # the masses added
        "m(H₂O) = 14,2 − 5,3\n= 8,9 g\nn(Na₂CO₃) = {m}/{M} = {14,2}/{106}\n= 0,13 mol\nn(H₂O) = {m}/{M} = {8,9}/{18}\n= 0,5 mol\n"
        "n(Na₂CO₃) : n(H₂O) = 0,13 : 0,5\n= 1 : 3,8\nx = 4",                                                  # the hydrated sample's mass
        "m(H₂O) = 14,2 − 5,3\n= 8,9 g\nn(Na₂CO₃) = {m}/{M} = {5,3}/{106}\n= 0,05 mol\nn(H₂O) = {m}/{M} = {8,9}/{18}\n= 0,5 mol\n"
        "n(Na₂CO₃) : n(H₂O) = 0,05 : 0,5\n= 1 : 10\nx = 10",                                                  # the memo
        "m(H₂O) = 14,2 − 5,3\n= 8,9 g\nn(Na₂CO₃) = {m}/{M} = {5,3}/{83}\n= 0,064 mol\nn(H₂O) = {m}/{M} = {8,9}/{18}\n= 0,5 mol\n"
        "n(Na₂CO₃) : n(H₂O) = 0,064 : 0,5\n= 1 : 7,8\nx = 8"], 2,                                             # one Na in M
        ["Which mass is the water that was driven off?", "How do you find x from the numbers of moles of Na₂CO₃ and H₂O?"],
        after=["6.2.1"]),   # the options show 6.2.1's 106 g·mol⁻¹
]

# ---- QUESTION 7, the question paper pages 11-12 and the memo pages 8-9 ----
P79 = "A learner accidentally dropped hydrochloric acid into the solution. "
q7 = [
    rub("7.1", "Give a reason why the ammeter reading was initially zero.", 1, ["Distilled water does not contain free ions. (1)"],
        ["What particles must a liquid contain to conduct electricity?", "What has been removed from water when it is distilled?"]),
    term("7.2", "Give ONE word/term for a solution that conducts electricity.", ["Electrolyte", "An electrolyte"],
         ["What particles in a solution carry the electric charge?", "Think of a car battery: what is the liquid that carries the current inside it "
          "called?"], marks=2),
    # a balanced equation as multiple choice (the memo: Ag⁺(aq) 1, NO₃⁻(aq) 1: 2 marks, all or nothing): the charges doubled, the signs
    # swapped, the nitrate ion broken up
    mcq("7.3", "Write down a balanced chemical equation to show how AgNO₃ dissociates in water." + EQ, [
        "AgNO₃(s) → Ag²⁺(aq) + NO₃²⁻(aq)", "AgNO₃(s) → Ag⁻(aq) + NO₃⁺(aq)", "AgNO₃(s) → Ag⁺(aq) + N⁵⁺(aq) + 3O²⁻(aq)",
        "AgNO₃(s) → Ag⁺(aq) + NO₃⁻(aq)"], 3,
        ["Which ions does silver nitrate contain, and what are their charges?", "Is the nitrate ion broken up when silver nitrate dissolves?"]),
    rub("7.4.1", "Write down the following for the investigation above: a hypothesis.", 2, [
        "The conductivity of AgNO₃ solution will increase with an increase in the concentration of the AgNO₃ solution at a constant temperature. (2)"],
        ["Which variable did the learners change, and which did they measure?",
         "A hypothesis is a prediction: what do you expect to happen to one variable when the other increases?"], each=2),
    term("7.4.2", "Write down the following for the investigation above: dependent variable.", [
        "Conductivity", "Electrical conductivity", "The conductivity", "Conductivity of the solution"],
         ["Which quantity did the ammeter readings stand for?", "Is it the cause or the effect in this investigation?"]),
    term("7.4.3", "Write down the following for the investigation above: independent variable.", [
        "Concentration", "Concentration of the AgNO3 solution", "Concentration of AgNO3", "Concentration of the solution", "The concentration"],
         ["What did the learners change by adding more spoons of AgNO₃?", "Is it the cause or the effect in this investigation?"]),
    term("7.4.4", "Write down the following for the investigation above: controlled variable.", ["Temperature", "The temperature"],
         ["Which condition does the first sentence of the investigation say was kept constant?",
          "Why must a condition be kept the same in a fair test?"]),
    rub("7.5", "Define the term anhydrous.", 1, ["Without water. (1)"],
        ["Which word for a crystal means the opposite of anhydrous?", "What is the difference between Na₂CO₃·xH₂O and Na₂CO₃?"]),
    # the memo divides by M = 106 (sodium carbonate's molar mass) and ends at 0,5 mol·dm⁻³; M(AgNO₃) = 108 + 14 + 3(16) = 170, so
    # c = 0,31 mol·dm⁻³ (flagged): the right option uses 170 and 0,5 is never an option. Wrong: one spoon, 200 cm³ not converted, one O in M
    work("7.6", "If the mass of AgNO₃ is 5,3 g per spoon, calculate the concentration of the solution after TWO spoons have been added.", 4, [
        "m(AgNO₃) = (5,3)(1)\n= 5,3 g\nc = {m}/{MV}\n= {5,3}/{(170)(0,2)}\n= 0,16 mol·dm⁻³",                      # one spoon only
        "m(AgNO₃) = (5,3)(2)\n= 10,6 g\nc = {m}/{MV}\n= {10,6}/{(170)(200)}\n= 3,12 × 10⁻⁴ mol·dm⁻³",              # cm³ not converted
        "m(AgNO₃) = (5,3)(2)\n= 10,6 g\nc = {m}/{MV}\n= {10,6}/{(138)(0,2)}\n= 0,38 mol·dm⁻³",                    # one O in M: 108 + 14 + 16
        "m(AgNO₃) = (5,3)(2)\n= 10,6 g\nc = {m}/{MV}\n= {10,6}/{(170)(0,2)}\n= 0,31 mol·dm⁻³"], 3,                # the memo (M corrected)
        ["How much AgNO₃ is in the solution after TWO spoons?",
         "Which formula links concentration, mass, molar mass and volume, and in which unit must the volume be?"]),
    rub("7.7", "Can tap water be used for this experiment? Give a reason for the answer.", 2, [
        "No. (1)", "Tap water contains ions and it will affect the conductivity of the AgNO₃ solution. (1)"],
        ["What does tap water contain that distilled water does not?", "How would those particles change the ammeter readings?"],
        after=["7.1"]),   # its card: tap water contains ions (the other side of 7.1's distilled water without free ions)
    rub("7.8", "From the results, deduce the relationship between the ion concentration in the solution and its conductivity.", 2, [
        "An increase in concentration of ions in a solution increases conductivity of a solution. (2)"],
        ["What happens to the ammeter reading as more spoons are added?", "What does each spoon of AgNO₃ add to the solution?"], each=2,
        after=["7.4.1"]),   # its card: the conductivity rises with the concentration (7.4.1's hypothesis)
    mcq("7.9.1", P79 + "How will this affect the ammeter reading? Write down only INCREASE, DECREASE or REMAIN THE SAME.", CHANGE, 1,
        ["Which ions does hydrochloric acid add to the solution?", "Which silver salt is insoluble in water?"], marks=1),
    rub("7.9.2", P79 + "Explain the answer to QUESTION 7.9.1.", 2, [
        "Silver chloride precipitate forms / a reaction takes place. (1)", "Thus decreasing the concentration of the ions. (1)"],
        ["What forms when silver ions meet chloride ions?", "Are the ions in a solid still free to move?"],
        after=["7.9.1"]),   # its cards: the concentration of the ions decreases (7.9.1's answer)
]

# ---- QUESTION 8, the question paper page 12 and the memo page 9 ----
P83 = "Both carbonates and sulphates form a white precipitate with the chemical in QUESTION 8.1. "
q8 = [
    mcq("8.1", "Which chemical would you choose to test for the presence of carbonates (CO₃⁻²)?", ["AgNO₃", "BaCl₂", "Dilute HNO₃"], 1,
        ["Which of the three chemicals is an acid, and what would an acid do to a carbonate?",
         "Which of the other two is used to test for chloride ions?"], marks=1),
    # a balanced equation as multiple choice (the memo: reactants 1, BaCO₃(s) 1, 2Cℓ⁻(aq) 1, balancing 1: 4 marks, all or nothing; its
    # CO₃⁻² written CO₃²⁻): unbalanced, chloride ions as chlorine gas, the barium carbonate formula wrong
    mcq("8.2", "Use a balanced chemical equation to show the test for carbonates in QUESTION 8.1." + EQ, [
        "CO₃²⁻(aq) + BaCl₂(aq) → BaCO₃(s) + Cl⁻(aq)", "CO₃²⁻(aq) + BaCl₂(aq) → BaCO₃(s) + 2Cl⁻(aq)",
        "CO₃²⁻(aq) + BaCl₂(aq) → BaCO₃(s) + Cl₂(g)", "2CO₃²⁻(aq) + BaCl₂(aq) → Ba(CO₃)₂(s) + 2Cl⁻(aq)"], 1,
        ["What precipitate forms when barium ions meet carbonate ions?",
         "How many chloride ions are left in the solution for each barium ion that reacts?"], marks=4,
        after=["8.1"]),   # its options: barium chloride is the chemical (8.1's answer)
    # a balanced equation as multiple choice (the memo: reactants, products, balancing: 4 marks, all or nothing). The memo prints
    # BaCO₃ + HNO₃ → Ba(NO₃)₂ + CO₂ + H₂O, without the 2 before HNO₃, and still gives its 'Bal' mark (flagged): the right option is the
    # balanced equation and the memo's unbalanced form is never an option. Wrong: the sulphate, hydrogen for water, BaNO₃
    mcq("8.3", P83 + "Use a balanced chemical equation to explain how you would confirm that the precipitate is a carbonate." + EQ, [
        "BaSO₄(s) + 2HNO₃(aq) → Ba(NO₃)₂(aq) + H₂SO₄(aq)", "BaCO₃(s) + 2HNO₃(aq) → Ba(NO₃)₂(aq) + CO₂(g) + H₂(g)",
        "BaCO₃(s) + HNO₃(aq) → BaNO₃(aq) + CO₂(g) + H₂O(ℓ)", "BaCO₃(s) + 2HNO₃(aq) → Ba(NO₃)₂(aq) + CO₂(g) + H₂O(ℓ)"], 3,
        ["What happens when an acid is added to a carbonate?",
         "What is the formula of barium nitrate: what are the charges on a barium ion and on a nitrate ion?"], marks=4,
        after=["8.1", "8.2"]),   # its options: barium compounds (8.1) and the BaCO₃ precipitate (8.2's product)
    term("8.4", "Give the chemical name of the precipitate formed when the carbonate and the chemical in QUESTION 8.1 reacts.", ["Barium carbonate"],
         ["Which ions combine to form the precipitate in 8.2?", "How is a salt named: the metal first, then which part?"], marks=2, strict=True),
]

# ---- QUESTION 9, the question paper page 13 and the memo pages 9-10 ----
q9 = [
    term("9.1.1", "The water cycle consists of many processes. Identify the following process: A", ["Condensation"],
         ["What happens to water vapour when it cools high up in the air?", "Does arrow A change a gas into a liquid, or a liquid into a gas?"]),
    term("9.1.2", "The water cycle consists of many processes. Identify the following process: B", ["Precipitation"],
         ["How does water get from the clouds back to the oceans and rivers?",
          "What happens to the water droplets in a cloud when they become too heavy?"]),
    term("9.1.3", "The water cycle consists of many processes. Identify the following process: E", ["Transpiration"],
         ["Through which parts of a plant does water vapour escape into the air?",
          "Is process E the same as evaporation from a lake, or special to plants?"]),
    rub("9.2", "Is energy ABSORBED or RELEASED during condensation? Give a reason for the answer.", 2, [
        "Released. (1)", "Energy is released to the surrounding / cooling takes place / particles move closer together. (1)"],
        ["Which phase changes into which during condensation?", "Is energy needed to pull particles apart, or given out when they come together?"],
        after=["9.1.1"]),   # its stem names condensation, 9.1.1's answer for arrow A
    rub("9.3", "Give ONE reason why water vapour is referred to as an important greenhouse gas.", 2, [
        "Water absorbs the infrared energy from the sun and re-emits it therefore regulating the climate. (2)"],
        ["What does a greenhouse gas do with the heat radiation that passes through the air?",
         "How would the earth's temperature change if there were no water vapour in the air?"], each=2),
    rub("9.4", "The amount of rainfall in large parts of South Africa has decreased considerably recently. Various reasons have been given to explain "
        "the drought. State ONE possible strategy that a community can adopt to ensure that they have a regular supply of water.", 2, [
        "Drilling of boreholes / Building of dams. (2)"],
        ["Where is water found besides in rivers: above the ground or below it?",
         "How could a community keep water from the wet season for the dry season?"], each=2),
]

PT_TABLE = {"head": ["ELEMENT", "ATOMIC NUMBER", "MASS NUMBER", "NUMBER OF PROTONS", "NUMBER OF NEUTRONS", "NUMBER OF ELECTRONS"],
            "rows": [["Aℓ", "13", "27", "4.2.1", "4.2.2", "4.2.3"], ["K⁺", "19", "4.2.4", "4.2.5", "4.2.6", "4.2.7"]]}
SPOON_TABLE = {"head": ["SPOONS OF AgNO₃ IN DISTILLED WATER", "AMMETER READING (mA)"],
               "rows": [["0", "0"], ["1", "0,18"], ["2", "0,92"], ["3", "1,47"], ["4", "1,84"]]}
Q6_LEAD = ("Study the balanced chemical equation of the reaction between sodium carbonate (Na₂CO₃) and hydrochloric acid (HCℓ) and answer the "
           "questions that follow.\nNa₂CO₃ + 2HCℓ → 2NaCℓ + CO₂ + H₂O")
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Structures and bonding", "marks": 10,
     "lead": "Consider the following substances:\nC₉₀;   NaCℓ;   CO₂;   Fe;   H₂O", "items": q2a},
    {"id": "2.5", "title": "Question 2.5", "kind": "Models of compounds", "marks": 3,
     "lead": "Study the models of compounds A, B and C below and answer the questions that follow.",
     "figure": fig("Q2.5", "Three models. A: three rows of four large touching circles, each marked K⁺ or I⁻ in turn. B: a circle marked C in the "
                   "centre with circles marked H bonded around it, one bond drawn dotted. C: a circle marked N in the centre with circles marked H "
                   "bonded around it."), "items": q2b},   # (no counts: the formula of B is the question)
    {"id": "2.6", "title": "Question 2.6", "kind": "Separating the gases in air", "marks": 4,
     "lead": "Many of the gases in air are very useful. An important industrial process, fractional distillation of liquid air, separates these "
             "gases from one another.\n\nConsider the diagram below and answer the questions that follow.",
     "figure": fig("Q2.6", "AIR, an arrow marked 'Compressed' to LIQUID AIR, and three arrows from LIQUID AIR: to NITROGEN, marked 'Boils at "
                   "-196 °C'; to ARGON, marked 'Boils at -186 °C'; to OXYGEN, marked 'Boils at -183 °C'."), "items": q2c},
    {"id": "2.7", "title": "Question 2.7", "kind": "Changes of phase", "marks": 3,
     "lead": "State how EACH of the following changes when liquid nitrogen changes into gaseous nitrogen. Write down only INCREASE, DECREASE or "
             "REMAIN THE SAME.", "items": q2d},
    {"id": "3", "title": "Question 3", "kind": "Ionisation energy", "marks": 18,
     "lead": "Consider the graph of the first ionisation energy and answer the questions that follow.",
     "figure": fig("Q3", "A line graph: ionisation energy (kJ·mol⁻¹), 0 to 2500, up against atomic number, 1 to 20, across; one point for each "
                   "element, labelled with its symbol from H to Ca, the points joined by straight lines."), "items": q3},
    # (no trend: the rise across a period and the fall down a group are 3.2's and 3.5.3's answers)
    {"id": "4", "title": "Question 4", "kind": "Isotopes and relative atomic mass", "marks": 9,
     "lead": "A certain element, X, has two isotopes in nature. One isotope has an atomic mass of 106,9 amu. The percentage appearance of this "
             "isotope is 50%. The atomic mass of the other isotope is 109,1.", "items": q4a},
    {"id": "4.2", "title": "Question 4.2", "kind": "Atomic structure", "marks": 7,
     "lead": "Complete the table below. Write only the answer next to the question number (4.2.1–4.2.7).", "table": PT_TABLE, "items": q4b},
    {"id": "5", "title": "Question 5", "kind": "Hydrogen peroxide", "marks": 14,
     "lead": "Hydrogen peroxide decomposes at room temperature according to the following balanced chemical equation:\n2H₂O₂(aq) → O₂(g) + 2H₂O(ℓ)",
     "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Sodium carbonate and hydrochloric acid", "marks": 1, "lead": Q6_LEAD, "items": q6a},
    {"id": "6.2", "title": "Question 6.2", "kind": "Reacting masses", "marks": 14,
     "lead": Q6_LEAD + "\n\nIn a reaction, 10,6 g of sodium carbonate reacts completely with excess hydrochloric acid.", "items": q6b},
    {"id": "6.3", "title": "Question 6.3", "kind": "Water of crystallisation", "marks": 5,
     "lead": "14,2 g of a sample of hydrated sodium carbonate, Na₂CO₃•xH₂O, was strongly heated until no further change in mass was recorded. On "
             "heating, all the water of crystallisation evaporated as follows:\nNa₂CO₃•xH₂O → Na₂CO₃ + xH₂O", "items": q6c},
    {"id": "7", "title": "Question 7", "kind": "Investigating a silver nitrate solution", "marks": 22,
     "lead": "Learners investigated the relationship between the concentration of a silver nitrate (AgNO₃) solution and its conductivity at a "
             "constant temperature.\n\nThey set up the apparatus, as shown below, and recorded the current. The initial reading of the ammeter was "
             "taken before anhydrous AgNO₃ was added to distilled water.\n\nThe anhydrous AgNO₃ was added to 200 cm³ distilled water spoon by "
             "spoon. The ammeter reading was recorded after each spoon was added. The results are shown in the table below.",
     "figure": fig("Q7", "A circuit: a cell, a switch and an ammeter A in series with two electrodes that dip into a beaker."),
     "table": SPOON_TABLE, "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Testing river water", "marks": 11,
     "lead": "Your teacher asked you to use your knowledge of precipitation reactions to test the quality of water in the local river.\n\nYou are "
             "provided with the following chemicals:\nAgNO₃,   BaCl₂,   dilute HNO₃", "items": q8},
    {"id": "9", "title": "Question 9", "kind": "The water cycle", "marks": 9, "lead": "Study the water cycle below and answer the questions that follow.",
     "figure": fig("Q9", "Four boxes joined by arrows: arrow A from Water vapour to Clouds; arrow B from Clouds to Oceans/Rivers; arrow C from "
                   "Oceans/Rivers to Water vapour; arrow D from Clouds to Plants; arrow E from Plants to Water vapour; and an unlabelled arrow "
                   "from Plants up to Oceans/Rivers."), "items": q9},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Grade 10 Physical Sciences P2 2018 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, another term's definition, the opposite choice, the reversed reasoning):
# never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns `each`;
# the cards are shuffled the same way every run. The rubric bullets above stay as the source. Where the memo gives ONE mark for
# "A / B" forms of a point, one form is a card: two right cards for one mark would let two picks earn two marks.
# Card order: the seeded shuffle (PID:n). Where it puts a single right card first, or every right card on top, the pilots added wrong
# cards until it moved; here no count of cards from 5 to 8 moves it for 3.1, 7.5 and 7.9.2 (and only 7 or 8 cards would for 7.1, 7.4.1
# and 7.8), so those six draw the shuffle again with a numbered seed (PID:n:1), not filler cards. REDRAWN records them.
REDRAWN = {}


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    for salt in range(10):
        order = list(range(len(right) + len(wrong)))
        random.Random(PID + ":" + n + (":%d" % salt if salt else "")).shuffle(order)
        pool = sorted(k for k, i in enumerate(order) if i < len(right))
        if pool != list(range(len(pool))):
            break
    if salt:
        REDRAWN[n] = salt
    assert pool != list(range(len(pool))), (n, "the right card first, or every right card on top: an answer by position", pool)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count}


STATEMENTS = {
    # 2 ticks: the choice and the reason
    "2.6.3": (1, ["Nitrogen has the weakest intermolecular forces.", "Nitrogen has the lowest boiling point."],
                 ["Oxygen has the weakest intermolecular forces.", "Argon has the weakest intermolecular forces.",
                  "Nitrogen has the highest boiling point.", "The gas with the weakest intermolecular forces needs the most energy to boil."]),
    # 2: the wrong ones are electron affinity, the solid phase, a proton added, electronegativity, bond breaking
    "3.1": (2, ["The energy needed per mole to remove an electron from an atom in the gaseous phase."],
               ["The energy released per mole when an atom in the gaseous phase gains an electron.",
                "The energy needed per mole to remove an electron from an atom in the solid phase.",
                "The energy needed per mole to add a proton to the nucleus of an atom.",
                "The tendency of an atom in a molecule to attract the bonding electrons.",
                "The energy needed per mole to break the bonds between the atoms of a molecule."]),
    # 2: the wrong ones are the opposite, no change, a dip then a rise, a group trend reversed
    "3.2": (2, ["Ionisation energy increases from left to right across a period."],
               ["Ionisation energy decreases from left to right across a period.", "Ionisation energy stays the same from left to right across a period.",
                "Ionisation energy first decreases and then increases from left to right across a period.",
                "Ionisation energy increases from top to bottom down a group."]),
    # 3, the memo's 1 + 2 (2p higher in energy than 2s; less energy to remove B's electron), played as 1 + 1 + 1: the reason and BOTH
    # forms of the 2-mark conclusion (its Option 1's and its Option 2's) as right cards, the two forms together earning the conclusion's 2.
    # Its Option 2 reason (the 2s electrons paired, the 2p electron unpaired) is neither a right nor a wrong card
    "3.3.2": (1, ["B has a 2p energy level, and 2p has a higher energy than 2s.",
                  "Therefore less energy is needed to remove the valence electron from B than from Be.",
                  "Therefore less energy is needed to remove the 2p electron."],
                 ["Be has a 2p energy level, and 2p has a lower energy than 2s.",
                  "Therefore more energy is needed to remove the valence electron from B than from Be.",
                  "B has more protons than Be, so its outer electron is held more weakly.",
                  "The 2s electrons of B are removed before its 2p electron."]),
    # 2 ticks: false, and the corrected statement
    "3.4": (1, ["The statement is false.", "The ionisation energy of noble gases is high because of the filled s- and p-orbitals."],
               ["The statement is true.", "The ionisation energy of noble gases is high because of the empty s- and p-orbitals.",
                "The ionisation energy of noble gases is low because of the filled s- and p-orbitals.",
                "The ionisation energy of noble gases is high because they have the largest atoms in each period."]),
    # 2: the wrong ones are the opposite, no change, a rise then a fall, only one element reacting
    "3.5.2": (2, ["Reactivity increases from top to bottom in group (I)."],
                 ["Reactivity decreases from top to bottom in group (I).", "Reactivity stays the same from top to bottom in group (I).",
                  "Reactivity first increases and then decreases from top to bottom in group (I).",
                  "Only the first element in group (I) reacts with water."]),
    # 2: the memo's one point (its ticks stand together at the end); the wrong ones reverse a link of its chain
    "3.5.3": (2, ["Ionisation energy decreases down the group, thus less energy is needed to remove an electron. Therefore reactivity increases."],
                 ["Ionisation energy increases down the group, thus more energy is needed to remove an electron. Therefore reactivity increases.",
                  "Ionisation energy decreases down the group, thus more energy is needed to remove an electron. Therefore reactivity decreases.",
                  "Ionisation energy increases down the group, thus less energy is needed to remove an electron. Therefore reactivity increases.",
                  "Ionisation energy stays the same down the group, so reactivity depends only on the number of neutrons."]),
    # 2, either OR form: the wrong ones swap protons and neutrons, are different elements, ions, isobars, allotropes
    "4.1.1": (2, ["Atoms of the same element having the same number of protons, but a different number of neutrons.",
                  "Atoms with the same atomic number, but different mass numbers."],
                 ["Atoms of the same element having the same number of neutrons, but a different number of protons.",
                  "Atoms of different elements having the same mass number.",
                  "Atoms of the same element having a different number of electrons.",
                  "Atoms with the same mass number, but different atomic numbers.",
                  "Molecules made of the same element, but with a different number of atoms."]),
    # 2 ticks: the choice and the reason
    "5.2": (1, ["The reaction is a redox reaction.", "Electron transfer takes place."],
               ["The reaction is a precipitation reaction.", "A solid precipitate forms when two solutions are mixed.",
                "No electrons are transferred in the reaction.", "Two ionic compounds exchange their ions."]),
    # 2: the wrong ones are 1 g of carbon-12, one particle's mass, 12 g of water, one particle's volume, 1 g
    "5.4": (2, ["The amount of substance having the same number of particles as there are atoms in 12 g carbon-12."],
               ["The amount of substance having the same number of particles as there are atoms in 1 g carbon-12.",
                "The mass of one particle of a substance.",
                "The amount of substance having the same number of particles as there are molecules in 12 g of water.",
                "The volume occupied by one particle of a gas.", "The amount of substance that has a mass of exactly 1 g."]),
    # 1: the wrong ones are many ions, electron conduction, undissolved salt, an overload
    "7.1": (1, ["Distilled water does not contain free ions."],
               ["Distilled water contains many free ions.", "Distilled water conducts electricity through free electrons.",
                "The AgNO₃ had not dissolved yet, so it blocked the current.", "The current was too large for the ammeter to measure."]),
    # 2: the wrong ones are a question, wrong variables, the independent and controlled variables swapped
    "7.4.1": (2, ["The conductivity of the AgNO₃ solution will increase with an increase in the concentration of the AgNO₃ solution at a constant "
                  "temperature."],
                 ["What is the relationship between the concentration of a AgNO₃ solution and its conductivity?",
                  "The temperature of the AgNO₃ solution will increase with an increase in its concentration.",
                  "The mass of AgNO₃ in a spoon will increase with an increase in the volume of distilled water.",
                  "The conductivity of the AgNO₃ solution will increase with an increase in its temperature, at a constant concentration."]),
    # 1: the wrong ones are dissolved, hydrated, water of crystallisation, no ions, no oxygen
    "7.5": (1, ["Anhydrous means without water."],
               ["Anhydrous means dissolved in water.", "Anhydrous means surrounded by water molecules.",
                "Anhydrous means containing water of crystallisation.", "Anhydrous means without any ions.", "Anhydrous means without oxygen."]),
    # 2 ticks: the choice and the reason
    "7.7": (1, ["No, tap water cannot be used.", "Tap water contains ions and it will affect the conductivity of the AgNO₃ solution."],
               ["Yes, tap water can be used.", "Tap water contains no ions, so it does not affect the conductivity.",
                "Tap water reacts with the electrodes to form a precipitate.", "Tap water is a compound, while distilled water is a mixture."]),
    # 2: the wrong ones are the opposite, no dependence, a rise then a fall, temperature alone
    "7.8": (2, ["An increase in the concentration of ions in a solution increases the conductivity of the solution."],
               ["An increase in the concentration of ions in a solution decreases the conductivity of the solution.",
                "The conductivity of a solution does not depend on the concentration of ions in it.",
                "An increase in the concentration of ions in a solution first increases and then decreases the conductivity.",
                "The conductivity of a solution depends only on its temperature."]),
    # 2 ticks: the precipitate (its "a reaction takes place" form says less: no card) and the decrease in ions
    "7.9.2": (1, ["A silver chloride precipitate forms.", "The concentration of the ions in the solution decreases."],
                 ["A silver nitrate precipitate forms.", "Hydrogen gas forms and carries the current away.",
                  "The silver ions and the nitrate ions join to form AgNO₃ molecules again.", "The concentration of the AgNO₃ solution doubles."]),
    # 2 ticks: the choice and ONE form of the reason (its "released to the surrounding" repeats the choice; "cooling takes place" says the
    # same as the particles moving closer: no cards)
    "9.2": (1, ["Energy is released during condensation.", "The particles move closer together."],
               ["Energy is absorbed during condensation.", "The particles move further apart.",
                "Energy is needed to overcome the intermolecular forces.", "The particles gain kinetic energy."]),
    # 2: the wrong ones are reflection, ozone, the main gas of the air, removing carbon dioxide
    "9.3": (2, ["Water vapour absorbs the infrared energy from the sun and re-emits it, therefore regulating the climate."],
               ["Water vapour reflects all the sunlight back into space, so it cools the earth.",
                "Water vapour absorbs ultraviolet light and turns it into ozone.",
                "Water vapour makes up most of the gases in the atmosphere.",
                "Water vapour reacts with carbon dioxide to remove it from the atmosphere."]),
    # 2, either of the memo's two strategies: the wrong ones waste water or harm its sources
    "9.4": (2, ["Drilling of boreholes.", "Building of dams."],
               ["Watering gardens every day.", "Washing cars with running hoses.", "Cutting down the trees along the rivers.",
                "Leaving taps running so that the pipes do not dry out."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, explanations and choices with reasons), so SORTS stays empty and sort_ is kept for parity.
SORTS = {}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random(PID + ":sort:" + n).shuffle(order)
    rows = [rows[i] for i in order]
    assert marks == len(rows) and len(set(b for _, b in rows)) == len(bins), n
    return {"t": "match", "n": n, "marks": marks, "q": q + " Sort each statement.", "clues": clues, "left": [r for r, _ in rows],
            "right": bins, "a": [b for _, b in rows], "heads": ["STATEMENTS", "SORT INTO"], "groups": True}


for _m in missions:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric" and _it["n"] in SORTS:
            _bins, _rows = SORTS[_it["n"]]
            _m["items"][_k] = sort_(_it["n"], _it["q"], _it["marks"], _bins, _rows, _it["clues"])
        elif _it["t"] == "rubric" and _it["n"] in STATEMENTS:
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            _m["items"][_k] = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
        if _it.get("after"):   # its gate rides along
            _m["items"][_k]["after"] = _it["after"]
assert not [i["n"] for m in missions for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"
assert REDRAWN == {"3.1": 1, "7.1": 1, "7.4.1": 1, "7.5": 1, "7.8": 1, "7.9.2": 1}, REDRAWN

assert tuple(AUTHORED) == ("4.1.2", "5.5", "5.6", "6.2.1", "6.2.2", "6.2.3", "6.2.4", "6.3", "7.6"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
nums = [i["n"] for i in ITEMS]
assert len(set(nums)) == len(nums), "a part number twice"
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["4.2.%d" % k for k in range(1, 8)], "only the table cells stay typed numbers"
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["2.3", "2.5.1", "2.5.2", "2.5.3", "2.6.2", "3.5.1", "4.1.3", "5.1", "7.2", "7.4.2",
                                                        "7.4.3", "7.4.4", "8.4", "9.1.1", "9.1.2", "9.1.3"]
assert [i["n"] for i in ITEMS if i.get("strict")] == ["2.5.1", "2.5.2", "8.4"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.2", "2.4"]
assert not [i["n"] for i in ITEMS if i["t"] == "match"], "no classify and no sort in this paper"
assert [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] not in STATEMENTS] == ["2.1.1"]
assert all(nums.index(e) < nums.index(i["n"]) for i in ITEMS for e in i.get("after", [])), "a gate on a later part"
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]
EQUATIONS = ["7.3", "8.2", "8.3"]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2017", "total_marks": 150, "time": "2 hours"},
    "sections": [{"title": "Chemistry", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic chemistry errors (a mole ratio not applied, a "
                                                       "formula upside down, a wrong molar mass, cm³ not converted, masses added not subtracted, "
                                                       "the wrong sample, the liquid water counted as gas, a factor dropped), 0 or full marks: "
                                                       + ", ".join(AUTHORED) + " (%d parts, %d marks). No memo range here; a memo slip's value "
                                                       "(4.1.2's 107,9, 6.2.4's 25,16 g, 7.6's 0,5 mol·dm⁻³) is never a wrong option."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions and trends (3.1, 3.2, 3.5.2, "
                                                    "3.5.3, 4.1.1, 5.4, 7.4.1, 7.5, 7.8, 9.3, 9.4) pick one card for their marks (an OR form is a "
                                                    "second right card); the reasons and the choices with reasons (2.6.3, 3.3.2, 3.4, 5.2, 7.1, "
                                                    "7.7, 7.9.2, 9.2) pick the choice and the memo's points, 1 mark each. Where the memo gives "
                                                    "one mark for 'A / B' forms of a point, one form is a card." % len(PICKS)},
        {"n": "3.3.2", "kind": "no_fit", "detail": "The memo marks 3.3.2 as 1 + 2 ('2p has a higher energy than 2s'; 'therefore less energy is "
                                                   "needed to remove the valence electron from B' for 2), with an OR answer of the same shape. A "
                                                   "pick has one mark a card, so it plays as 1 + 1 + 1: the reason and BOTH forms of the "
                                                   "conclusion (Option 1's and Option 2's) are right cards, the two forms together earning the "
                                                   "conclusion's 2. Option 2's reason (the 2s electrons paired, the 2p electron unpaired) is "
                                                   "neither a right nor a wrong card."},
        {"n": "2.1.1", "kind": "no_fit", "detail": "'Write down a substance from the list' (2.1.1-2.1.4) plays as a choice of the five listed "
                                                   "substances; 2.1.1, whose memo accepts 'CO₂ OR H₂O', is a pick of one with both right."},
        {"n": "3.3.1", "kind": "no_fit", "detail": "The sp-notations of Be and B (superscripts cannot be typed) play as answer multiple choice of four "
                                                   "pairs, the memo's 4 marks (2 a notation) all or nothing."},
        {"n": EQUATIONS[0], "kind": "no_fit", "detail": "'Write down / Use a balanced chemical equation' (7.3, 8.2, 8.3) plays as multiple choice of "
                                                        "four equations, the memo's marks all or nothing (reactants, products, balancing): its "
                                                        "ions would be typed with charges the term check drops. The wrong ones are charges "
                                                        "doubled or swapped, an ion broken up, unbalanced, a wrong product or formula, the "
                                                        "sulphate."},
        {"n": "2.2", "kind": "no_fit", "detail": "Drawings (2.2 the Lewis dot diagram of CO₂, 2.4 the formation of NaCℓ) are done on paper and "
                                                 "self-checked against the memo's criteria. The memo ticks 2.2 as a whole (2); its two criteria "
                                                 "(the shared pairs; the lone pairs) are our split of its drawing."},
        {"n": "4.2.1", "kind": "no_fit", "detail": "The seven cells of the 4.2 table (1 mark each, no working) play as seven typed numbers."},
        {"n": "1.5", "kind": "memo_issue", "detail": "The memo's C (Li < Na < K < Rb) is the general trend down group 1, but potassium is less dense "
                                                     "than sodium (about 0,86 against 0,97 g·cm⁻³; Li 0,53, Rb 1,53), so no option is exactly "
                                                     "right. C is kept as the memo marks it."},
        {"n": "2.1.3", "kind": "memo_issue", "detail": "The memo answers C₉₀ for 'a covalent network structure' (memo page 3). C₉₀ is a fullerene, a "
                                                       "molecular form of carbon, not a giant covalent network like diamond or graphite, and the "
                                                       "memo does not accept it for 2.1.1 'a molecular structure'. Kept as the memo marks it."},
        {"n": "4.1.2", "kind": "memo_issue", "detail": "The memo's working (page 5) writes (50 × 106,9) + (50 × 108,9) over 100, where the paper and "
                                                       "the memo's own line above give the other isotope as 109,1 amu; its answer 108 follows from "
                                                       "109,1 (with 108,9 it would be 107,9). The right option uses 109,1; 107,9 is never an option."},
        {"n": "6.2.4", "kind": "memo_issue", "detail": "The memo (page 7) ends m = 25,16 g, but its own 0,434 × 58,5 = 25,39 g (25,44 g unrounded). "
                                                       "The right option ends 25,39 g; the memo's 25,16 g is never a wrong option (a learner's "
                                                       "25,16 g would earn the memo's mark too)."},
        {"n": "6.3", "kind": "memo_issue", "detail": "The memo's Option 2 (page 8) writes M(Na₂CO₃) = 160 g·mol⁻¹ yet gets 5,3/160 = 0,05 (it is "
                                                     "5,3/106); the right option is its Option 1. The paper asks for 'the number of moles of water of "
                                                     "crystallisation in the sample' and the memo works to x = 10 (moles of water per mole of "
                                                     "Na₂CO₃), passing n(H₂O) = 0,5 mol on the way: the options end at x = 10 as the memo marks it."},
        {"n": "7.6", "kind": "memo_issue", "detail": "The memo (page 9) divides by M = 106 g·mol⁻¹ (sodium carbonate's) and ends at 0,5 mol·dm⁻³; "
                                                     "M(AgNO₃) = 108 + 14 + 3(16) = 170 g·mol⁻¹, so c = 10,6 / (170 × 0,2) = 0,31 mol·dm⁻³. The right "
                                                     "option uses 170; 0,5 mol·dm⁻³ is never a wrong option (a learner's 0,5 would earn the memo's "
                                                     "marks too)."},
        {"n": "8.3", "kind": "memo_issue", "detail": "The memo (page 9) prints BaCO₃ + HNO₃ → Ba(NO₃)₂ + CO₂ + H₂O, without the 2 before HNO₃, and "
                                                     "still gives its 'Bal' mark. The right option is the balanced equation (2HNO₃); the memo's "
                                                     "unbalanced form is never an option."},
        {"n": "7.9.1", "kind": "memo_issue", "detail": "The memo's DECREASE counts the AgCℓ precipitate removing ions; the H⁺ the acid brings stays in "
                                                       "solution in place of the Ag⁺ removed (and H⁺ conducts better), so the real reading need not "
                                                       "fall. Kept as the memo marks it (DECREASE, and 7.9.2's points)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (the figures, the Q3 graph and every memo working are images); no API call. "
                                                           "The memo prints 2.6.3 twice (page 3), the same answer both times."},
    ],
}
QTOTAL = {"1": 20, "2": 20, "3": 18, "4": 16, "5": 14, "6": 20, "7": 22, "8": 11, "9": 9}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's ten printed letters are the paper's (A5 B1 C3 D1) and the printed choice picks are fixed by their answers
# (2.1.x, 2.6.1, 2.7.x, 5.3, 6.1, 7.9.1, 8.1), so the authored four-option questions (the nine workings, the 3.3.1 notation and the three
# equations) lean away from A: the workings sit as even as nine allow, the four-option questions within 3
at = ["ABCDE"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCDE"}
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(wspread.values()) - min(wspread.values()) <= 1, wspread   # nine workings: as even as possible
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, the paper:", spread, "authored workings:", wspread, "four-option:", fspread)
print("statement right-card positions:", {i["n"]: i["pool"] for i in ITEMS if i["t"] == "pickn"})
total = sum(i["marks"] for i in ITEMS)
assert total == 150 == paper["paper"]["total_marks"], total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; statements:", len(PICKS), "parts")
print("total:", total)
# GATES (the last check): a part whose stem, options, cards or criteria show an earlier part's answer opens only after it
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "2.2": ["2.1.1"], "2.4": ["2.1.4"], "2.6.3": ["2.6.2"], "3.3.2": ["3.3.1"], "3.5.3": ["3.5.2"], "6.2.2": ["6.2.1"], "6.2.3": ["6.2.2"],
    "6.3": ["6.2.1"], "7.7": ["7.1"], "7.8": ["7.4.1"], "7.9.2": ["7.9.1"], "8.2": ["8.1"], "8.3": ["8.1", "8.2"], "9.2": ["9.1.1"]}, \
    "a gate dropped or changed"
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper},
                                              indent=1, ensure_ascii=False), encoding="utf-8")
