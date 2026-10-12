"""Grade 11 Physical Sciences P2 (Chemistry) Nov 2018 (DBE common paper), the whole paper (Questions 1 to 10), hand-transcribed into the
catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper draws the 1.5 graphs, the 6.2 mass-time
graph and the Q7 energy diagram and sets the 1.8 ions as images, and the memo sets its Lewis diagrams, its fractions and every working as
images (its text layer turns fractions into columns of digits).

  python tools/ingest/transcribe_g11_ps_p2_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Physical Sciences P2 Nov 2018 Eng.pdf" "uploads/Grade 11 Physical Sciences P2 Nov 2018 MG Eng & Afr.pdf" --id g11-ps-p2-2018-11 --from-json

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; models: transcribe_ps_p2_2025_11.py, Chemistry, the same sitting's
transcribe_g11_ps_p1_2018_11.py and the Grade 10 Chemistry papers transcribe_g10_ps_p2_2018_11.py / transcribe_g10_ps_p2_2017_11.py):
  multiple choice printed in the paper -> mcq as printed (1.5's graph options: the figure and "Graph A".."Graph D"; 1.8 and 1.9 print their
  options as a table -> optTable); a choice printed in the stem with no explanation in the same part (2.5 POLAR or NON-POLAR, 2.8 YES or
  NO, 4.6 HIGH or LOW) and 3.2 (a FORMULA from the three substances of the table) -> mcq of the printed choices. One term the memo names
  -> term (2.3, 4.1, 8.2); a substance's name or formula (6.2.1 sulphuric acid, 9.3 H2S / S2-, 9.5 MnO4- / Mn+7, 10.2 O2) -> strict term
  (the service keeps a strict term's charge sign, 2026-10-11). 9.2 (an oxidation number, no working) is an answer multiple choice.
  Every calculation ("Calculate", "Determine", "Use calculations") -> authored multiple choice, `work`: the memo's FIRST working line by
  line and three workings each built from a DIFFERENT realistic chemistry error (a unit not converted, a formula upside down, a mole ratio
  or a molar mass wrong, the wrong constant, a value from the wrong row or sample), every number recomputed; 0 or full marks. A value the
  memo also accepts (its ranges, its OPTIONS) and a memo slip's value are never a wrong option. 9.7 ("Use the ion-electron method",
  the memo's half-reactions then the net ionic equation) plays as a working too. "Balance the equation" / "Write a balanced equation"
  (6.1.2, 8.3) and a half-reaction (9.6, 10.4) -> multiple choice of four equations, the memo's marks all or nothing.
  A definition, law or hypothesis -> statements (pick 1 card for its marks; an OR form a second right card); an explanation the memo
  ticks point by point, or a choice with its reasons (3.4) -> statements, 1 mark a point. No memo here weighs two sides, so no part plays
  as a sort. Drawings (2.2.1 and 2.2.2 Lewis structures, 4.3 the graph on the ANSWER SHEET, 7.4 the catalysed curve) -> draw with the
  memo's criteria, self-checked (flagged no_fit).
  A part whose stem, options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose lead changes part-way is two missions (2 and 2.6; 6 and 6.2; 8 and 8.4).
Figure boxes are measured in PDF points (page 595.32 x 841.92, read from the PDF) tight to the ink (drawings and labels) and checked on a
contact sheet of the 1%-padded crops (scratchpad lower/g11-ps-p2-2018-11/figs.py)."""
import json
import random
import re
from pathlib import Path

PID = "g11-ps-p2-2018-11"
W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.5": [4, 102.0, 143.5, 510.5, 355.0], "Q6.2": [9, 179.5, 571.0, 406.5, 700.5], "Q7": [10, 199.0, 190.3, 442.0, 338.5]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points ("[2 or 0]", criteria): never scored, never shown
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
EQ = "\n\nChoose the correct equation."   # a balanced equation or a half-reaction played as multiple choice of four
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


# ---- QUESTION 1: multiple choice, the question paper pages 3-5 and the memo page 2 ----
MC_LEAD = "Various options are provided as possible answers to the following questions."
q1 = [
    mcq("1.1", "The tendency of an atom to attract the bonding pair of electrons is known as …",
        ["electron affinity.", "electronegativity.", "polarity.", "activation energy."], 1,
        ["Is the term about a single atom in a bond, about a whole molecule, or about a reaction?",
         "How is attracting a SHARED pair of electrons in a bond different from gaining an extra electron?"]),
    mcq("1.2", "Bond length is the average distance between the …",
        ["orbitals of two bonded atoms.", "electrons in two bonded atoms.", "nuclei of two bonded atoms.", "molecules of the same substance."], 2,
        ["Electrons are spread out in clouds: which parts of two bonded atoms have a fixed position you can measure between?",
         "Is bond length about atoms inside one molecule, or about separate molecules?"]),
    mcq("1.3", "Hydrogen bonds and London forces (induced dipole forces) have a common characteristic in that they …",
        ["are both stronger than chemical bonds.", "both occur between non-polar molecules.", "both occur between polar molecules.",
         "are both intermolecular forces."], 3,
        ["Which of the two forces needs polar molecules, and which also acts between non-polar molecules?",
         "How does the strength of a hydrogen bond compare with that of a covalent bond?"]),
    mcq("1.4", "In order to double the volume of a fixed amount of moles of an enclosed gas, the temperature in … at constant pressure.",
        ["ºC can be doubled", "K can be doubled", "ºC can be halved", "K can be halved"], 1,
        ["Which gas law links the volume and the temperature of a gas at constant pressure?",
         "Is the volume of a gas at 20 ºC twice its volume at 10 ºC?"]),
    mcq("1.5", "The graph that CORRECTLY represents the relationship between the pressure (kPa) and the temperature (K) of an enclosed gas at "
        "constant volume is …", ["Graph A", "Graph B", "Graph C", "Graph D"], 2,
        ["What happens to the pressure of a gas when it is heated in a closed, rigid container?",
         "What would the pressure of the gas be at 0 K?"],
        figure=fig("1.5", "Four graphs, A to D, each of p (kPa) up against T (K) across. A: a straight line that falls from the p-axis to the "
                   "T-axis. B: a curve from the origin that gets steeper as T increases. C: a straight line from the origin. D: a curve that "
                   "falls steeply and then levels off.")),
    mcq("1.6", "The solution that will have the greatest concentration of H⁺ ions if complete ionisation takes place, is …",
        ["0,4 dm³ of a 1 mol·dm⁻³ H₂SO₄ solution.", "0,4 dm³ of a 1 mol·dm⁻³ HCℓ solution.", "1 dm³ of a 1 mol·dm⁻³ HCℓ solution.",
         "0,4 dm³ of a 1 mol·dm⁻³ CH₃COOH solution."], 0,
        ["Does the volume of a solution change its concentration?",
         "What is the difference between a monoprotic and a diprotic acid?"]),
    mcq("1.7", "Which ONE of the following is NOT a typical reaction of hydrochloric acid?",
        ["It neutralises a base with the release of hydrogen gas.", "It forms hydronium ions in water.", "It colours lithmus paper red.",
         "It forms CO₂ when reacting with a metal carbonate."], 0,
        ["What colour does blue litmus paper turn in an acid?", "What are the products when an acid neutralises a base?"]),
    mcq("1.8", "Which ONE of the following pairs represents the conjugate acid and conjugate base of HPO₄²⁻?",
        ["PO₄³⁻; H₂PO₄⁻", "H₂PO₄⁻; PO₄³⁻", "H₂PO₄⁻; H₃PO₄", "H₂PO₄²⁻; PO₄²⁻"], 1,
        ["How does an acid differ from its conjugate base?", "When an H⁺ ion is removed from a particle, what happens to its charge?"],
        optTable={"head": ["CONJUGATE ACID", "CONJUGATE BASE"],
                  "rows": [["PO₄³⁻", "H₂PO₄⁻"], ["H₂PO₄⁻", "PO₄³⁻"], ["H₂PO₄⁻", "H₃PO₄"], ["H₂PO₄²⁻", "PO₄²⁻"]]}),
    mcq("1.9", "Which ONE of the following indicates the CORRECT colour of bromothymol blue in an acid and a base?",
        ["Orange; Yellow", "Blue; Red", "Pink; Colourless", "Yellow; Blue"], 3,
        ["Is bromothymol blue named after its colour in an acid or in a base?", "Which indicator turns pink in a base?"],
        optTable={"head": ["BROMOTHYMOL BLUE IN AN ACID", "BROMOTHYMOL BLUE IN A BASE"],
                  "rows": [["Orange", "Yellow"], ["Blue", "Red"], ["Pink", "Colourless"], ["Yellow", "Blue"]]}),
    mcq("1.10", "In which ONE of the following reactions is HCℓ oxidised?",
        ["HCℓ(aq) + H₂O(ℓ) → H₃O⁺(aq) + Cℓ⁻(aq)", "CaCO₃(s) + 2HCℓ(aq) → CaCℓ₂(aq) + H₂O(ℓ) + CO₂(g)", "NH₃(aq) + HCℓ(aq) → NH₄Cℓ(aq)",
         "MnO₂(aq) + 4HCℓ(aq) → MnCℓ₂(aq) + H₂O(ℓ) + Cℓ₂(g)"], 3,
        ["What is the oxidation number of Cℓ in HCℓ, and in each product that contains chlorine?",
         "Is oxidation an increase or a decrease in oxidation number?"]),
]

# ---- QUESTION 2, the question paper page 6 and the memo pages 3-4 ----
q2a = [
    rub("2.1", "Define the term chemical bond.", 2, [
        "Chemical bond is mutual attraction between two atoms resulting from the simultaneous attraction between their nuclei and (outer) "
        "electrons. (2)"],
        ["How is a chemical bond different from the forces between separate molecules?",
         "Which parts of an atom carry a positive charge, and which a negative charge?"], each=2),
    draw("2.2.1", "Draw Lewis structures for: HCN", 2, [
        ["H and C share one pair of electrons, C and N share three pairs, and N has one lone pair", 2]],
        ["How many valence electrons do H, C and N each have?", "How many electrons does each atom need around it to be stable?"],
        memo="The memo's structure: H:C:::N: (one shared pair between H and C, three shared pairs between C and N, and a lone pair on N)."),
    draw("2.2.2", "Draw Lewis structures for: H₂O", 2, [
        ["O shares one pair of electrons with each H atom and has two lone pairs", 2]],
        ["How many valence electrons does oxygen have, and how many does each hydrogen atom have?",
         "How many of oxygen's valence electrons are not used in bonding?"],
        memo="The memo's structure: O in the middle with two lone pairs, one shared pair to each of the two H atoms."),
    term("2.3", "What is the shape of the HCN molecule?", ["Linear", "Linear shape", "Linear molecule"],
         ["How many atoms are bonded to the central carbon atom, and does the carbon atom have any lone pairs?",
          "How does the VSEPR model decide a molecule's shape from the electron pairs around its central atom?"]),
    work("2.4", "Calculate the electronegativity difference for the CN bond.", 1, [
        "ΔEN = 2,5 − 2,1\n= 0,4",                                                       # the C–H bond's values (H 2,1): the wrong bond
        "ΔEN = 3 + 2,5\n= 5,5",                                                         # the two values added
        "ΔEN = 3 − 2,5\n= 0,5",                                                         # the memo
        "ΔEN = 3,5 − 2,5\n= 1"], 2,                                                     # oxygen's 3,5 read for nitrogen
        ["Where on the data sheet do you find the electronegativity of each element?",
         "Is a difference found by adding or by subtracting the two values?"]),
    mcq("2.5", "What is polarity of the HCN molecule? Write only POLAR or NON-POLAR.", ["Polar", "Non-polar"], 0,
        ["Are the electronegativity differences of the C–H and C–N bonds equal, so that their dipoles could cancel?",
         "Which end of the molecule, if any, carries a partial negative charge?"], marks=1),
]
q2b = [
    rub("2.6", "Explain why the bond energy of the CN bond is more than the bond energy of the CH bond.", 2, [
        "CN has a higher order bond/triple bond with more orbitals overlapping (1)", "than CH, which is a single bond. (1)"],
        ["How many electron pairs are shared between C and N, and between C and H, in HCN?",
         "How does the number of shared electron pairs (the bond order) affect how strongly two atoms are held together?"],
        after=["2.2.1"]),   # its cards: the CN bond is a triple bond (2.2.1's Lewis structure)
    rub("2.7", "Explain the difference between the bond length of the CH bond and the bond length of the CN bond.", 2, [
        "CN has a longer bond length than CH (1)", "because the H atom is smaller than the N atom. (1)"],
        ["What does the table tell you about the two bond lengths?",
         "How does the size of the atom joined to carbon affect the distance between the two nuclei?"]),
    mcq("2.8", "Will HCN be soluble in water? Write only YES or NO.", ["Yes", "No"], 0,
        ["Which kinds of substances dissolve in water?",
         "Can HCN molecules attract water molecules about as strongly as water molecules attract each other?"], marks=1),
    rub("2.9", "Explain the answer to QUESTION 2.8 by referring to the polarity and intermolecular forces of the compounds.", 3, [
        "HCN has polar molecules with dipole-dipole forces. (1)", "H₂O has polar molecules with hydrogen bonds (dipole-dipole forces). (1)",
        "If the forces are of the same order/comparable the substances will dissolve. (1)",
        "OR — Both molecules are polar (1)", "HCN has dipole-dipole forces and H₂O has (dipole-dipole forces) hydrogen bonds (1)",
        "Like dissolve like. (1)"],
        ["Which type of intermolecular force acts between HCN molecules, and which between water molecules?",
         "When can the forces between two different substances replace the forces within each substance?"],
        after=["2.5", "2.8"]),   # its cards: HCN is polar (2.5) and the substances dissolve (2.8)
]

# ---- QUESTION 3, the question paper page 7 and the memo pages 4-5 ----
q3 = [
    rub("3.1", "Refer to the intermolecular forces and explain the difference in boiling point between NH₃ and N₂.", 3, [
        "NH₃ has hydrogen bonds between the molecules (1)", "N₂ has London forces/induced dipole forces (1)",
        "NH₃ has stronger intermolecular forces than N₂ and therefore a higher boiling point than N₂ (1)",
        "OR — N₂ has weaker intermolecular forces than NH₃ and therefore a lower boiling point than NH₃ (1)"],
        ["To which atom is hydrogen bonded in NH₃, and what kind of intermolecular force does that allow?",
         "Is N₂ a polar or a non-polar molecule, and which forces act between non-polar molecules?"]),
    mcq("3.2", "Write down the FORMULA of the substance in the table that will have the lowest melting point.", ["H₂", "N₂", "NH₃"], 0,
        ["How are the melting point and the boiling point of a substance related to the strength of its intermolecular forces?",
         "How can you tell from the table which substance has the weakest intermolecular forces?"], marks=1),
    rub("3.3", "Explain why H₂ will evaporate faster than N₂. Refer to the type and relative strength of the intermolecular forces.", 3, [
        "H₂ and N₂ both have weak London forces/induced dipole forces (1)",
        "N₂ is a larger molecule/has a greater molecular mass/has a larger surface area than H₂ (1)",
        "and therefore N₂ has stronger intermolecular forces. (1)",
        "OR — H₂ is a smaller molecule/has a smaller molecular mass/has a smaller surface area than N₂ (1)",
        "and therefore H₂ has weaker intermolecular forces. (1)"],
        ["Are H₂ and N₂ polar or non-polar molecules, and which forces act between them?",
         "How does the size of a molecule affect the strength of its London forces?"],
        after=["3.2"]),   # its cards: N₂'s forces are stronger than H₂'s (with 3.1, H₂ has the weakest: 3.2's answer)
    rub("3.4", "Write down the FORMULA of the substance in the table that will have the highest vapour pressure. Explain your answer.", 3, [
        "H₂ (1)", "It has the weakest intermolecular forces/London forces (1)", "It has the lowest boiling point (1)",
        "OR — It has the weakest intermolecular forces/London forces (1)", "Boiling point is inversely proportional to vapour pressure (1)"],
        ["How does the strength of the intermolecular forces affect how easily molecules escape from a liquid?",
         "How are the vapour pressure and the boiling point of a substance related?"],
        after=["3.2", "3.3"]),   # its cards: H₂ has the weakest forces (3.2's answer, 3.3's conclusion)
]

# ---- QUESTION 4, the question paper page 8 (ANSWER SHEET page 17) and the memo pages 6-7 ----
q4 = [
    term("4.1", "Name the gas law that is represented by the results of the experiment.", ["Boyle's law", "Boyles law", "Boyle law", "Boyle's gas law"],
         ["What happens to the volume each time the pressure increases?", "What is the product of the pressure and the volume in each row of the table?"]),
    rub("4.2", "Write down a hypothesis for the investigation.", 2, [
        "If the pressure of an enclosed gas increases the volume will decrease at constant temperature. (2)",
        "OR — The pressure of an enclosed gas is inversely proportional to the volume it occupies if the temperature is kept constant. (2)"],
        ["Which quantity did the learners change, and which did they measure?",
         "A hypothesis is a prediction: how do you state the relationship you expect between the two variables?"], each=2,
        notes=["Criteria: the dependent (volume) and independent (pressure) variables stated correctly (1); the relationship between them stated (1)."],
        after=["4.1"]),   # its cards state the inverse relationship of pressure and volume (4.1's law)
    # BUILT on the answer sheet's grid (2026-10-11, build "plot"): its axes printed and labelled (Volume (dm³) up, Pressure (kPa) across)
    # on 8 big squares across and 8 up, 10 small squares in each, no numbers. The memo's criteria (memo page 6, its graph to scale on page
    # 16): the scale on both axes (1: 50 kPa and 25 dm³ a big square, the only choices that hold 260 kPa and 174 dm³ and use over half the
    # grid; every scale offered is even, so the memo's "table values as scale values: maximum 1/3" cannot arise here); five or more points
    # right (1: within half a small square of the learner's own scale); a curve drawn (1: a smooth curve through points that do not lie on
    # one line)
    {**draw("4.3", "Draw a graph of volume versus pressure on the ANSWER SHEET attached.", 3, [
        ["Correct scale on both axes (table values used as the scale values: maximum 1/3 for the line drawn)", 1],
        ["At least five (5) points plotted correctly", 1], ["Curve drawn", 1]],
        ["Which quantity goes on the vertical axis of a graph of volume versus pressure?",
         "What scale lets the largest pressure and the largest volume in the table fit on the grid?"],
        memo="The memo's graph: Volume (dm³), 0 to 200, up, against Pressure (kPa), 0 to 300, across, the seven points of the table joined by a "
             "smooth curve."),
     "build": {"kind": "plot", "grid": {"nx": 8, "ny": 8, "sub": 10},
               "x": {"name": "Pressure (kPa)", "unit": "kPa", "scales": [20, 25, 50, 100], "ok": [50]},
               "y": {"name": "Volume (dm³)", "unit": "dm³", "scales": [20, 25, 50, 100], "ok": [25]},
               "points": [{"id": "p%d" % k, "name": "p = %d kPa" % p, "at": [p, vol]}
                          for k, (p, vol) in enumerate([(70, 174), (95, 128), (130, 93.6), (165, 74), (205, 59), (240, 51), (260, 47)])], "tol": [2.5, 1.25],
               "tests": [{"k": "scale"}, {"k": "points", "min": 5}, {"k": "shape", "kinds": ["curve"], "straight": False}]}},
    work("4.4", "Calculate the volume of the gas at 300 kPa.", 3, [
        "p₁V₁ = p₂V₂\n70(174) = (300)V₂\nV₂ = 40,6 dm³",                                  # the memo (it accepts 40,32 - 40,8 dm³ from any row)
        "{p₁}/{V₁} = {p₂}/{V₂}\n{70}/{174} = {300}/{V₂}\nV₂ = 745,71 dm³",                # pressure and volume taken as directly proportional
        "p₁V₁ = p₂V₂\n260(174) = (300)V₂\nV₂ = 150,8 dm³",                                # a pressure and a volume from different rows
        "p₁V₁ = p₂V₂\n70 000(174) = (300)V₂\nV₂ = 40 600 dm³"], 0,                        # one pressure in Pa, the other left in kPa
        ["Which pair of values from the table can you use as the first state of the gas?",
         "Which quantity stays constant when the temperature does not change: the product or the quotient of p and V?"]),
    rub("4.5", "When the volume of the gas is measured at 300 kPa, it is 44 dm³. Explain why the measured volume differs from the volume "
        "calculated in QUESTION 4.4.", 2, [
        "At high pressure a gas starts to deviate from ideal gas behaviour (1)",
        "because the volume of the molecules of a gas and the intermolecular forces start to influence the measured value, causing it to be "
        "greater than the theoretical value calculated/Forces of repulsion between the gas particles prevents them from moving closer (1)"],
        ["Is 300 kPa a low or a high pressure for this gas?",
         "Which assumptions about ideal gas molecules stop being true when the molecules are pushed close together?"]),
    mcq("4.6", "Which temperature condition will cause a gas to deviate from ideal behaviour? Write only HIGH or LOW.", ["High", "Low"], 1,
        ["What happens to the speed of gas molecules as the temperature drops?",
         "Which assumption about an ideal gas concerns the forces between its molecules?"], marks=1),
    rub("4.7", "Explain the answer to QUESTION 4.6.", 2, [
        "Temperature is an indication of the average kinetic energy of the molecules of a gas. If the temperature of a gas decreases, the "
        "molecules move slower and closer together (1)", "up to a point where the gas will start to condense and not behave like an ideal gas. (1)",
        "OR — The intermolecular forces of attraction become significant (1)", "then the gas condenses. (1)"],
        ["What does the temperature of a gas tell you about the kinetic energy of its molecules?",
         "What happens to a gas when its molecules come close enough for the forces between them to hold them together?"],
        after=["4.6"]),   # its cards say "at a low temperature" (4.6's answer)
    work("4.8", "Calculate the number of moles of the gas in the container at the INITIAL pressure and volume.", 4, [
        "pV = nRT\n(70 000)(174 × 10⁻³) = n(8,31)(20)\nn = 73,29 mol",                    # the temperature left in ºC
        "pV = nRT\n(70)(174 × 10⁻³) = n(8,31)(293)\nn = 5,00 × 10⁻³ mol",                  # the pressure left in kPa
        "n = {V}/{Vm}\nn = {174}/{22,4}\nn = 7,77 mol",                                   # the molar gas volume at STP (the gas is not at STP)
        "pV = nRT\n(70 000)(174 × 10⁻³) = n(8,31)(293)\nn = 5 mol"], 3,                   # the memo
        ["Which equation links the pressure, volume, temperature and number of moles of a gas?",
         "What are the INITIAL pressure and volume in the table, and what is the temperature of the gas?"]),
]

# ---- QUESTION 5, the question paper page 9 and the memo pages 7-8 ----
q5 = [
    work("5.1", "Calculate the volume of the balloon.", 4, [
        "n = {m}/{M}\nn = {160}/{40}\nn = 4 mol\npV = nRT\n(120 000)V = (4)(8,31)(15)\nV = 4,16 × 10⁻³ m³",     # the temperature left in ºC
        "n = {m}/{M}\nn = {160}/{40}\nn = 4 mol\npV = nRT\n(120 000)V = (4)(8,31)(288)\nV = 0,08 m³",           # the memo
        "n = {m}/{M}\nn = {160}/{80}\nn = 2 mol\npV = nRT\n(120 000)V = (2)(8,31)(288)\nV = 0,04 m³",           # argon taken as Ar₂ (M = 80)
        "n = {m}/{M}\nn = {160}/{40}\nn = 4 mol\npV = nRT\n(120)V = (4)(8,31)(288)\nV = 79,78 m³"], 1,          # the pressure left in kPa
        ["Which equation links the pressure, volume, temperature and amount of a gas?",
         "Is argon made of single atoms or of molecules of two atoms?"]),
    work("5.2", "The temperature of the gas is now increased BY 20 ºC and the initial pressure is doubled. Calculate the new volume of the "
         "balloon.", 4, [
        "{p₁V₁}/{T₁} = {p₂V₂}/{T₂}\n{120(0,08)}/{308} = {240V₂}/{288}\nV₂ = 0,037 m³",   # the two temperatures swapped
        "{p₁V₁}/{T₁} = {p₂V₂}/{T₂}\n{120(0,08)}/{15} = {240V₂}/{35}\nV₂ = 0,093 m³",     # the temperatures left in ºC
        "{p₁V₁}/{T₁} = {p₂V₂}/{T₂}\n{120(0,08)}/{288} = {240V₂}/{308}\nV₂ = 0,043 m³",   # the memo's OPTION 1 (its "(427,78 dm³)": flagged)
        "p₁V₁ = p₂V₂\n120(0,08) = 240V₂\nV₂ = 0,04 m³"], 2,                              # the temperature change ignored
        # (its OPTION 2, pV = nRT, gives 0,043 m³ too; the memo's 427,78 and 426,58 dm³ (slips for 42,78 and 42,66 dm³) are never options)
        ["Which values describe the gas before the change, and which after it?", "What is the new temperature of the gas in kelvin?"],
        after=["5.1"]),   # the options show 5.1's 0,08 m³
]

# ---- QUESTION 6, the question paper page 9 and the memo pages 8-10 ----
q6a = [
    rub("6.1.1", "Define the term one mole of a substance.", 2, [
        "One mole is the amount of a substance having the same number of particles as there are atoms in 12 g carbon-12. (2)"],
        ["What does Avogadro's number, 6,02 × 10²³, count?", "Is a mole a mass, a volume, or an amount of particles?"], each=2,
        notes=["[2 or 0]"]),
    # a balanced equation as multiple choice (the memo: 2HCℓ and 2NaCℓ, 1 mark each, played all or nothing): the memo's equation and three
    # left unbalanced (the sodium, the chlorine and hydrogen, the hydrogen and oxygen)
    mcq("6.1.2", "Balance the equation for the reaction." + EQ, [
        "Na₂CO₃ + 2HCℓ → NaCℓ + H₂O + CO₂", "Na₂CO₃ + HCℓ → 2NaCℓ + H₂O + CO₂", "Na₂CO₃ + 2HCℓ → 2NaCℓ + H₂O + CO₂",
        "Na₂CO₃ + 2HCℓ → 2NaCℓ + 2H₂O + CO₂"], 2,
        ["How many sodium atoms are on each side of the equation as printed?",
         "Which atoms appear in only one substance on each side, so that you can balance them first?"]),
    work("6.1.3", "Calculate the mass of sodium carbonate that reacted.", 7, [
        "n = {V}/{Vm}\nn = {306}/{24,45}\nn = 12,52 mol of CO₂\nNa₂CO₃ : CO₂ = 1 : 1\nn = 12,52 mol of Na₂CO₃\nn = {m}/{M}\n"
        "12,52 = {m}/{106}\nm = 1 327,12 g",                                                # 306 cm³ not converted to dm³
        "n = {V}/{Vm}\nn = {0,306}/{22,4}\nn = 0,0137 mol of CO₂\nNa₂CO₃ : CO₂ = 1 : 1\nn = 0,0137 mol of Na₂CO₃\nn = {m}/{M}\n"
        "0,0137 = {m}/{106}\nm = 1,45 g",                                                   # the molar gas volume at STP, not the stem's 24,45
        "n = {V}/{Vm}\nn = {0,306}/{24,45}\nn = 0,0125 mol of CO₂\nNa₂CO₃ : CO₂ = 1 : 1\nn = 0,0125 mol of Na₂CO₃\nn = {m}/{M}\n"
        "0,0125 = {m}/{83}\nm = 1,04 g",                                                    # M(Na₂CO₃) with one Na (83 g·mol⁻¹)
        "n = {V}/{Vm}\nn = {0,306}/{24,45}\nn = 0,0125 mol of CO₂\nNa₂CO₃ : CO₂ = 1 : 1\nn = 0,0125 mol of Na₂CO₃\nn = {m}/{M}\n"
        "0,0125 = {m}/{106}\nm = 1,33 g"], 3,                                               # the memo (range 1,325 - 1,33 g)
        ["How many moles of CO₂ formed, and in which unit must its volume be for Vm = 24,45 dm³?",
         "Use your balanced equation: how many moles of Na₂CO₃ react for each mole of CO₂ formed?"]),
    work("6.1.4", "Calculate the percentage of sodium carbonate in excess.", 2, [
        "% Na₂CO₃ unreacted = {1,5 − 1,33}/{1,5} × 100\n= 11,33%",                       # the memo's OPTION 1 (it writes "% CaCO₃": flagged)
        "% Na₂CO₃ unreacted = {1,33}/{1,5} × 100\n= 88,67%",                              # the percentage that reacted
        "% Na₂CO₃ unreacted = {1,5 − 1,33}/{1,33} × 100\n= 12,78%",                       # divided by the mass that reacted
        "% Na₂CO₃ unreacted = {1,5}/{1,5 − 1,33} × 100\n= 882,35%"], 0,                   # the fraction upside down
        # (the memo's range 11,33 - 11,67% and its OPTION 3's 11,97% are never options)
        ["Which part of the 1,5 g of sodium carbonate is in excess?", "What do you multiply a fraction by to turn it into a percentage?"],
        after=["6.1.3"]),   # the options show 6.1.3's 1,33 g
]
q6b = [
    term("6.2.1", "Name the substance that is the limiting reagent.", [
        "Sulphuric acid", "Sulfuric acid", "H2SO4", "Sulphuric acid (H2SO4)", "Sulfuric acid (H2SO4)", "The sulphuric acid", "Dilute sulphuric acid"],
         ["Which reactant is still left over when the reaction stops?", "Which reactant runs out first, and so decides when the reaction stops?"],
         strict=True),
    work("6.2.2", "Calculate the initial concentration of the sulphuric acid if 50 cm³ of the acid was used.", 5, [
        "n = {m}/{M} = {5}/{65}\n= 0,0769 mol of Zn\nZn : H₂SO₄ = 1 : 1\nn(H₂SO₄) = 0,0769 mol\nc = {n}/{V} = {0,0769}/{0,05}\n"
        "= 1,54 mol·dm⁻³",                                                                  # the initial 5 g of zinc, not the 3 g that reacted
        "n = {m}/{M} = {3}/{65}\n= 0,0462 mol of Zn\nZn : H₂SO₄ = 1 : 1\nn(H₂SO₄) = 0,0462 mol\nc = {n}/{V} = {0,0462}/{0,05}\n"
        "= 0,92 mol·dm⁻³",                                                                  # the memo's OPTION 1 (its OPTIONS 2 and 3 give 0,92 too)
        "n = {m}/{M} = {3}/{65}\n= 0,0462 mol of Zn\nZn : H₂SO₄ = 1 : 1\nn(H₂SO₄) = 0,0462 mol\nc = {n}/{V} = {0,0462}/{50}\n"
        "= 9,24 × 10⁻⁴ mol·dm⁻³",                                                           # 50 cm³ not converted to dm³
        "n = {m}/{M} = {3}/{65}\n= 0,0462 mol of Zn\nZn : H₂SO₄ = 1 : 1\nn(H₂SO₄) = 0,0462 mol\nc = nV = (0,0462)(0,05)\n"
        "= 2,31 × 10⁻³ mol·dm⁻³"], 1,                                                       # c = nV
        ["What mass of zinc reacted before the reaction stopped?", "Use the balanced equation: how many moles of H₂SO₄ react with one mole of Zn?"],
        after=["6.2.1"]),   # the options show zinc left over (3 g of the 5 g reacted): 6.2.1's limiting reagent
]

# ---- QUESTION 7, the question paper page 10 and the memo pages 11-12 ----
q7 = [
    rub("7.1", "Define the term activation energy.", 2, ["The minimum energy needed for a reaction to take place. (2)"],
        ["Do all colliding particles react, or only some of them?", "On the diagram, between which two levels is Ea marked?"], each=2,
        notes=["[2 or 0]"]),
    rub("7.2", "Give a reason why this reaction is exothermic.", 1, [
        "More energy is released than absorbed (1)", "OR — energy of products is less than energy of reactants (1)", "OR — ΔH < 0 / ΔH is negative (1)"],
        ["Is more energy taken in to break bonds, or given out when new bonds form?",
         "How does the diagram show whether the reaction takes in or gives out energy overall?"]),
    work("7.3", "Calculate the heat of reaction.", 3, [
        "ΔH = H(products) − H(reactants)\n= 400 − 183,3\n= +216,7 kJ·mol⁻¹",           # subtracted the wrong way round
        "ΔH = H(products) − H(reactants)\n= 2 670 − 400\n= 2 270 kJ·mol⁻¹",             # the peak taken as the products (the activation energy)
        "ΔH = H(products) − H(reactants)\n= 183,3 − 400\n= −216,7 kJ·mol⁻¹",           # the memo
        "ΔH = H(products) − H(reactants)\n= 183,3 − 2 670\n= −2 486,7 kJ·mol⁻¹"], 2,   # the peak taken as the reactants
        ["Which level on the diagram shows the energy of the reactants, and which the energy of the products?",
         "Which energy is subtracted from which when you work out ΔH?"],
        after=["7.2"]),   # the right option shows ΔH < 0 (a reason 7.2 asks for)
    draw("7.4", "Redraw the graph and indicate with a dotted line the effect of a catalyst on the activation energy.", 2, [
        ["A lower curve, drawn as a dotted line", 1], ["The lower activation energy indicated", 1]],
        ["How does a catalyst change the path a reaction takes?", "Does a catalyst change the energies of the reactants and the products?"],
        memo="The memo's sketch: a dotted curve from the 400 level up to a lower peak than 2 670 and down to 183,3, with the smaller Ea marked."),
    rub("7.5", "State Avogadro's law in words.", 2, ["One mole of any gas occupies the same volume at the same temperature and pressure. (2)"],
        ["Does the law compare different gases, or one gas under different conditions?",
         "What is the molar gas volume at STP, and what does it tell you about one mole of different gases?"], each=2, notes=["[2 or 0]"]),
    work("7.6", "If 6 dm³ of NH₃ and 9 dm³ of O₂ are used, calculate the TOTAL VOLUME of the gases at the end of the reaction.", 4, [
        "Initial (dm³): NH₃ 6; O₂ 9; NO 0; H₂O 0\nChange (dm³, ratio 4 : 5 : 4 : 6): NH₃ 6; O₂ 7,5; NO 6; H₂O 9\n"
        "Final (dm³): NH₃ 0; O₂ 1,5; NO 6; H₂O 9\nTotal volume = 1,5 + 6\n= 7,5 dm³",                       # the H₂O(g) left out, as if liquid
        "Initial (dm³): NH₃ 6; O₂ 9; NO 0; H₂O 0\nChange (dm³, ratio 4 : 5 : 4 : 6): NH₃ 6; O₂ 7,5; NO 6; H₂O 9\n"
        "Final (dm³): NH₃ 0; O₂ 1,5; NO 6; H₂O 9\nTotal volume = 6 + 9\n= 15 dm³",                          # the excess O₂ left out
        "Initial (dm³): NH₃ 6; O₂ 9; NO 0; H₂O 0\nChange (dm³, ratio 4 : 5 : 4 : 6): NH₃ 6; O₂ 4,8; NO 6; H₂O 9\n"
        "Final (dm³): NH₃ 0; O₂ 4,2; NO 6; H₂O 9\nTotal volume = 4,2 + 6 + 9\n= 19,2 dm³",                  # the 4 : 5 ratio turned round (O₂ = 4/5 x 6)
        "Initial (dm³): NH₃ 6; O₂ 9; NO 0; H₂O 0\nChange (dm³, ratio 4 : 5 : 4 : 6): NH₃ 6; O₂ 7,5; NO 6; H₂O 9\n"
        "Final (dm³): NH₃ 0; O₂ 1,5; NO 6; H₂O 9\nTotal volume = 1,5 + 6 + 9\n= 16,5 dm³"], 3,             # the memo's OPTION 1 (its table, row by row)
        ["Which reactant runs out first?", "How are the reacting volumes of gases related to the coefficients in the balanced equation?"]),
    work("7.7", "The reaction above is the first step in the manufacturing of an acid. This acid contains 1,59% hydrogen, 22,2% nitrogen and "
         "76,2% oxygen. Determine the empirical formula of the acid.", 5, [
        "n(H) = {1,59}/{1} = 1,59 mol\nn(N) = {22,2}/{7} = 3,1714 mol\nn(O) = {76,2}/{8} = 9,525 mol\n"
        "H : N : O = {1,59}/{1,59} : {3,1714}/{1,59} : {9,525}/{1,59} = 1 : 1,99 : 5,99 ≈ 1 : 2 : 6\nEmpirical formula: HN₂O₆",        # atomic numbers as M
        "n(H) = {1,59}/{1} = 1,59 mol\nn(N) = {22,2}/{14} = 1,5857 mol\nn(O) = {76,2}/{16} = 4,7625 mol\n"
        "H : N : O = {1,59}/{1,5857} : {1,5857}/{1,5857} : {4,7625}/{1,5857} = 1 : 1 : 3\nEmpirical formula: HNO₃",                    # the memo
        # (it writes n(O) = 4,625 mol: 76,2 / 16 = 4,7625, flagged; its 4,625 earns the marks too and is in no option)
        "n(H) = 1,59 mol\nn(N) = 22,2 mol\nn(O) = 76,2 mol\n"
        "H : N : O = {1,59}/{1,59} : {22,2}/{1,59} : {76,2}/{1,59} = 1 : 13,96 : 47,92 ≈ 1 : 14 : 48\nEmpirical formula: HN₁₄O₄₈",     # % not turned into moles
        "n(H) = {1,59}/{1} = 1,59 mol\nn(N) = {22,2}/{14} = 1,5857 mol\nn(O) = {76,2}/{32} = 2,3813 mol\n"
        "H : N : O = {1,59}/{1,5857} : {1,5857}/{1,5857} : {2,3813}/{1,5857} = 1 : 1 : 1,5 = 2 : 2 : 3\nEmpirical formula: H₂N₂O₃"], 1,  # O as O₂ (32)
        ["How do you turn each percentage into a number of moles in a 100 g sample of the acid?",
         "Which number do you divide every mole value by to find the simplest ratio?"]),
]

# ---- QUESTION 8, the question paper page 11 and the memo pages 13-14 ----
q8a = [
    rub("8.1", "Explain why a hydroxide ion is regarded as a Lowry-Brønsted base.", 2, ["A hydroxide ion can act as proton acceptor. (2)"],
        ["Which particle is passed from one substance to another in a Lowry-Brønsted acid-base reaction?",
         "What does a hydroxide ion become when it reacts with an acid?"], each=2),
    term("8.2", "Identify the type of bond responsible for the formation of the ammonium ion in the above equation.", [
        "Dative covalent bond", "Dative covalent", "Dative bond", "Dative covalent bonding", "Dative", "Coordinate covalent bond",
        "Co-ordinate covalent bond", "Coordinate bond"],
         ["Which atom in NH₃ has a lone pair of electrons, and to which particle does it bond?",
          "Where do BOTH electrons of the new N–H bond come from?"]),
    # a balanced equation as multiple choice (the memo: reactants, products, 1 mark each, played all or nothing): the memo's first
    # equation and three wrong ones: water acting as the acid (the given reaction), water giving the proton, unbalanced. The memo's OR,
    # HCℓ(aq) + NH₃(g) → NH₄⁺(aq) + Cℓ⁻(aq), is never a wrong option.
    mcq("8.3", "Write a balanced equation to show how the ampholyte in the above equation will act as a base when it reacts with hydrochloric acid "
        "(HCℓ)." + EQ, [
        "HCℓ(aq) + H₂O(ℓ) → H₃O⁺(aq) + Cℓ⁻(aq)", "NH₃(g) + H₂O(ℓ) → NH₄⁺(aq) + OH⁻(aq)", "HCℓ(aq) + H₂O(ℓ) → H₂Cℓ⁺(aq) + OH⁻(aq)",
        "HCℓ(aq) + 2H₂O(ℓ) → H₃O⁺(aq) + Cℓ⁻(aq)"], 0,
        ["Which substance in the equation above can act as an acid in one reaction and as a base in another?",
         "When a base reacts with HCℓ, which particle does it take from the HCℓ?"]),
]
q8b = [
    rub("8.4", "Define the term concentration.", 2, [
        "Concentration is the amount of solute per litre of solution. (2)", "OR — Concentration is the number of moles of a substance per dm³ of solution. (2)"],
        ["Is concentration a property of the solute alone, or of the solute and the solution together?",
         "How does adding more water to a solution change its concentration?"], each=2),
    work("8.5", "Calculate the concentration of the acid AFTER it was spilled in the pond.", 4, [
        "c = {n}/{V}\n0,75 = {5}/{n}\nn = 6,67 mol\nc = {n}/{V} = {6,67}/{1 000}\n= 6,67 × 10⁻³ mol·dm⁻³",     # the first formula upside down
        "c = {n}/{V}\n0,75 = {n}/{5}\nn = 3,75 mol\nc = {n}/{V} = {3,75}/{5}\n= 0,75 mol·dm⁻³",                 # the acid's own 5 dm³, not the pond
        "c = {n}/{V}\n0,75 = {n}/{5}\nn = 3,75 mol\nc = {n}/{V} = {3,75}/{1 000}\n= 3,75 × 10⁻³ mol·dm⁻³",      # the memo's OPTION 1
        "c = {n}/{V}\n0,75 = {n}/{5}\nn = 3,75 mol\nc = {n}/{V} = {3,75}/{1}\n= 3,75 mol·dm⁻³"], 2,             # 1 000 dm³ "converted" to 1 dm³
        # (its OPTIONS 2 and 3, c₁V₁ = c₂V₂ and the ratio, give 3,75 x 10⁻³ mol·dm⁻³ too)
        ["How many moles of HNO₃ are in the 5 dm³ that spilled?", "Does the number of moles of acid change when it mixes with the pond water?"]),
    work("8.6", "Use calculations to determine if 120 g of calcium hydroxide will be sufficient to react completely with ALL the acid in the pond.", 6, [
        "c = {n}/{V}: 0,75 = {n}/{5}\nn(HNO₃) = 3,75 mol\nHNO₃ : Ca(OH)₂ = 2 : 1\nn(Ca(OH)₂) = 1,875 mol\nn = {m}/{M}: 1,875 = {m}/{74}\n"
        "m = 138,75 g\nNo, it is insufficient.",                                                                # the memo's OPTION 1
        "c = {n}/{V}: 0,75 = {n}/{5}\nn(HNO₃) = 3,75 mol\nHNO₃ : Ca(OH)₂ = 1 : 1\nn(Ca(OH)₂) = 3,75 mol\nn = {m}/{M}: 3,75 = {m}/{74}\n"
        "m = 277,5 g\nNo, it is insufficient.",                                                                 # the 2 : 1 ratio not applied
        "c = {n}/{V}: 0,75 = {n}/{5}\nn(HNO₃) = 3,75 mol\nHNO₃ : Ca(OH)₂ = 2 : 1\nn(Ca(OH)₂) = 1,875 mol\nn = {m}/{M}: 1,875 = {m}/{57}\n"
        "m = 106,88 g\nYes, it is sufficient.",                                                                 # M of CaOH (57), the bracket's 2 dropped
        "c = {n}/{V}: 3,75 × 10⁻³ = {n}/{5}\nn(HNO₃) = 0,01875 mol\nHNO₃ : Ca(OH)₂ = 2 : 1\nn(Ca(OH)₂) = 0,009375 mol\n"
        "n = {m}/{M}: 0,009375 = {m}/{74}\nm = 0,69 g\nYes, it is sufficient."], 0,                             # 8.5's concentration with the 5 dm³
        # (its OPTIONS 2 and 3 reach the same 1,875 mol and the same conclusion)
        ["How many moles of HNO₃ are in the pond, before and after the acid mixes with the water?",
         "Use the balanced equation: how many moles of Ca(OH)₂ react with each mole of HNO₃?"],
        after=["8.5"]),   # the options show 8.5's 3,75 mol and its 3,75 x 10⁻³ mol·dm⁻³
]

# ---- QUESTION 9, the question paper page 12 and the memo page 15 ----
q9 = [
    rub("9.1", "Define reduction in terms of oxidation numbers.", 2, ["Reduction is a decrease in oxidation number. (2)"],
        ["What does an oxidation number tell you about an atom in a compound or an ion?", "Is reduction the gain or the loss of electrons?"], each=2),
    # the memo: +7 / Mn⁷⁺ (no working): an answer multiple choice. The wrong ones: the ion's charge left out (+8), the ion's charge itself,
    # the sign wrong
    mcq("9.2", "Determine the oxidation number of manganese in the permanganate ion.", ["+8", "−1", "+7", "−7"], 2,
        ["What is the oxidation number of each oxygen atom, and what is the charge on the whole ion?",
         "How must the oxidation numbers of all the atoms in an ion add up?"], marks=1),
    term("9.3", "Write down the FORMULA of the substance that undergoes oxidation.", ["H2S", "S2-", "S 2-", "S^2-", "S(2-)"],
         ["Which element's oxidation number increases in the reaction?", "Does a substance that is oxidised lose electrons or gain them?"],
         strict=True),
    rub("9.4", "Explain the answer to QUESTION 9.3 in terms of oxidation numbers.", 2, [
        "The oxidation number of S increases (1)", "from -2 to 0. (1)"],
        ["What is the oxidation number of S in H₂S, and of S in S(s)?", "How do you work out the oxidation number of an element in a compound?"],
        after=["9.3"]),   # its cards: the oxidation number of S increases (H₂S is oxidised: 9.3's answer)
    term("9.5", "Write down the FORMULA for the oxidising agent.", ["MnO4-", "MnO4 -", "MnO4^-", "MnO4(-)", "Mn+7", "Mn7+", "Mn 7+", "Mn(+7)"],
         ["Is an oxidising agent itself oxidised or reduced in the reaction?",
          "What happens to the oxidation number of an element in the substance that is reduced?"], strict=True),
    # a half-reaction as multiple choice (the memo's 2 marks, all or nothing): the memo's and three wrong ones: the reduction as Table 4
    # prints it, the electrons on the wrong side, H and the charge unbalanced
    mcq("9.6", "Write down the oxidation half-reaction." + EQ, [
        "S + 2H⁺ + 2e⁻ → H₂S(g)", "H₂S(g) → S + 2H⁺ + 2e⁻", "H₂S(g) + 2e⁻ → S + 2H⁺", "H₂S(g) → S + H⁺ + e⁻"], 1,
        ["Where in Table 4 is the half-reaction for sulphur and H₂S, and in which direction must you read it for an oxidation?",
         "How do you check that a half-reaction is balanced for atoms and for charge?"],
        after=["9.3", "9.4"]),   # its options show H₂S turning into S (9.3's answer; 9.4's S from −2 to 0)
    work("9.7", "Use the ion-electron method and write down the balanced net ionic equation.", 3, [
        "H₂S → S + 2H⁺ + 2e⁻\nMnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O\nMnO₄⁻ + H₂S + 6H⁺ → Mn²⁺ + S + 4H₂O",                 # the electrons not equalised
        "H₂S → S + 2H⁺ + 2e⁻\nMnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O\n2MnO₄⁻ + 5H₂S + 6H⁺ → 2Mn²⁺ + 5S + 8H₂O",           # the memo (its "→ 2Mn²⁺": flagged)
        "H₂S → S + 2H⁺ + 2e⁻\nMnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O\n5MnO₄⁻ + 2H₂S + 36H⁺ → 5Mn²⁺ + 2S + 20H₂O",        # the multipliers swapped (x 2, x 5)
        "H₂S → S + 2H⁺ + 2e⁻\nMnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O\n2MnO₄⁻ + 5H₂S + 16H⁺ → 2Mn²⁺ + 5S + 8H₂O"], 1,     # the 10H⁺ formed not subtracted
        ["What must be true of the electrons lost and the electrons gained before you add the two half-reactions?",
         "Which half-reaction in Table 4 shows MnO₄⁻ being reduced to Mn²⁺?"],
        after=["9.3", "9.4", "9.5", "9.6"]),   # its options show H₂S oxidised (9.3, 9.4), MnO₄⁻ reduced (9.5) and 9.6's half-reaction
]

# ---- QUESTION 10, the question paper page 12 and the memo page 15 ----
q10 = [
    rub("10.1", "Name TWO disadvantages of deep-shaft mining in comparison with open-cast mining.", 2, [
        "Dangerous for workers because they can be trapped underground. (1)", "Sinkholes (1)"],
        ["Where do the miners work in deep-shaft mining, compared with open-cast mining?",
         "Think of the people and of the land: how can each be harmed by deep-shaft mining?"],
        notes=["(Any relevant answer)"]),
    term("10.2", "Write down the FORMULA of the substance that is reduced in the reaction used to extract gold.", ["O2"],
         ["Does a substance that is reduced gain or lose electrons?", "Which reactants are elements, with an oxidation number of zero?"],
         strict=True),
    rub("10.3", "Use oxidation numbers to explain how you arrived at the answer to QUESTION 10.2.", 1, [
        "Oxidation number of O decreases from 0 (in O₂) to -2 (in NaOH). (1)"],
        ["What is the oxidation number of an element that is not combined with another element?",
         "Does the oxidation number go up or down when a substance is reduced?"],
        after=["10.2"]),   # its cards: O₂ is reduced (10.2's answer)
    # a half-reaction as multiple choice (the memo's 2 marks, all or nothing): the memo's and three wrong ones: the oxidation, iron(II),
    # the electrons on the wrong side
    mcq("10.4", "Write the reduction half-reaction for the iron extraction reaction." + EQ, [
        "Fe → Fe³⁺ + 3e⁻", "Fe²⁺ + 2e⁻ → Fe", "Fe³⁺ → Fe + 3e⁻", "Fe³⁺ + 3e⁻ → Fe"], 3,
        ["Which particle of iron is in Fe₂O₃, and what is its charge?", "How many electrons are transferred for each iron atom?"]),
    work("10.5", "Calculate the percentage of iron present in Fe₂O₃.", 2, [
        "%Fe = {56}/{160} × 100%\n= 35%",                                                # one Fe atom only
        "%Fe = {160}/{2(56)} × 100%\n= 142,86%",                                         # the fraction upside down
        "%Fe = {2(56)}/{160} × 100%\n= 70%",                                             # the memo
        "%Fe = {3(16)}/{160} × 100%\n= 30%"], 2,                                         # the oxygen's percentage
        ["What is the molar mass of Fe₂O₃?", "How many iron atoms are there in one formula unit of Fe₂O₃?"]),
    work("10.6", "Only 65% of the ore contains iron. If 2 500 kg of ore is used, calculate the mass of iron that can be extracted from the ore.", 2, [
        "m(Fe) = (0,35)(2 500)\n= 875 kg",                                               # the 35% that is not iron
        "m(Fe) = {2 500}/{0,65}\n= 3 846,15 kg",                                         # divided by the fraction
        "m(Fe) = (65)(2 500)\n= 162 500 kg",                                             # 65% not turned into 0,65
        "m(Fe) = (0,65)(2 500)\n= 1 625 kg"], 3,                                         # the memo (it accepts 1,625 x 10⁶ g)
        # (1 137,5 kg, 65% of the ore taken as Fe₂O₃ and then 10.5's 70%, is never an option)
        ["How do you find a percentage of a quantity?", "Which percentage of the ore does the question say contains iron?"]),
]

BOND_TABLE = {"head": ["BOND", "BOND LENGTH (nm)", "BOND ENERGY (kJ·mol⁻¹)"], "rows": [["CH", "0,109", "413"], ["CN", "0,116", "890"]]}
BP_TABLE = {"head": ["SUBSTANCE", "BOILING POINT (ºC)"], "rows": [["H₂", "−252,9"], ["N₂", "−195,8"], ["NH₃", "−33,3"]]}
PV_TABLE = {"head": ["PRESSURE (kPa)", "VOLUME (dm³)"],
            "rows": [["70", "174"], ["95", "128"], ["130", "93,6"], ["165", "74"], ["205", "59"], ["240", "51"], ["260", "47"]]}
HCN = "Hydrogen cyanide (HCN) is a very poisonous compound used in the manufacturing of plastics, mining of gold and as a poison."
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20, "lead": MC_LEAD, "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Hydrogen cyanide", "marks": 9, "lead": HCN, "items": q2a},
    {"id": "2.6", "title": "Question 2.6", "kind": "Bond energy and bond length", "marks": 8,
     "lead": HCN + "\n\nThe table below indicates the values of the bond length and bond energy of the different bonds in HCN.",
     "table": BOND_TABLE, "items": q2b},
    {"id": "3", "title": "Question 3", "kind": "Intermolecular forces", "marks": 10,
     "lead": "The reaction below is used in the Haber process to manufacture ammonia.\nN₂(g) + 3H₂(g) → 2NH₃(g)\n\nThe boiling points of the "
             "substances in the reaction are as follows:", "table": BP_TABLE, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Pressure and volume", "marks": 18,
     "lead": "A certain amount of gas is sealed in a container of which the volume can change. The relationship between the pressure and volume "
             "of the gas at 20 ºC is investigated. The results of the experiment are given in the table below.", "table": PV_TABLE, "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Gas in a balloon", "marks": 8,
     "lead": "A balloon is filled with 160 g of argon gas (Ar). The pressure of the gas is 120 kPa at a temperature of 15 ºC.", "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Reacting masses and volumes", "marks": 13,
     "lead": "In an experiment, a learner added 1,5 g of sodium carbonate (Na₂CO₃) to hydrochloric acid (HCℓ). A volume of 306 cm³ of carbon "
             "dioxide gas was formed and collected under standard pressure at room temperature. Take the molar gas volume at room temperature "
             "(Vm) as 24,45 dm³.\n\nThe unbalanced equation for the reaction is:\nNa₂CO₃(s) + HCℓ(aq) → NaCℓ(aq) + H₂O(ℓ) + CO₂(g)", "items": q6a},
    {"id": "6.2", "title": "Question 6.2", "kind": "Mass of zinc over time", "marks": 6,
     "lead": "Zinc reacts with sulphuric acid according to the reaction below.\nZn(s) + H₂SO₄(aq) → ZnSO₄(aq) + H₂(g)\n\nThe mass of zinc is "
             "recorded during the experiment and is shown on the graph below. The reaction stops after 2 minutes.",
     "figure": fig("Q6.2", "A graph of the mass of Zn (g), up, against time (min), across, with 1, 2 and 3 marked on the time axis: the curve "
                   "starts at 5 on the mass axis, falls steeply at first and then levels off along a dashed line at 2."), "items": q6b},
    {"id": "7", "title": "Question 7", "kind": "Ammonia and oxygen", "marks": 19,
     "lead": "The following reaction between ammonia and oxygen takes place in a closed system at constant pressure and temperature:\n"
             "4NH₃(g) + 5O₂(g) → 4NO(g) + 6H₂O(g)",
     "figure": fig("Q7", "A potential energy diagram: Ep (kJ.mol⁻¹) up against course of reaction across. The curve runs level at 400, rises to a "
                   "peak at 2 670 and comes down to run level at 183,3; a double arrow labelled Ea joins the 400 and 2 670 levels, and a double "
                   "arrow labelled ΔH joins the 400 and 183,3 levels."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Acids and bases", "marks": 5,
     "lead": "Ammonia can readily dissolve in water according to the equation below:\nNH₃(g) + H₂O(ℓ) → NH₄⁺(aq) + OH⁻(aq)", "items": q8a},
    {"id": "8.4", "title": "Question 8.4", "kind": "Neutralising an acid spill", "marks": 12,
     "lead": "5 dm³ of nitric acid (HNO₃), with a concentration of 0,75 mol·dm⁻³, is spilled accidentally in a small pond of water. The acid and "
             "water has a total volume of 1 000 dm³. To neutralise the acid, calcium hydroxide is added to the water.\n"
             "2HNO₃(aq) + Ca(OH)₂(aq) → Ca(NO₃)₂(aq) + 2H₂O(ℓ)", "items": q8b},
    {"id": "9", "title": "Question 9", "kind": "Redox reactions", "marks": 12,
     "lead": "The reaction between permanganate ions (MnO₄⁻) and hydrogen sulphide (H₂S) is given below.\n"
             "MnO₄⁻(aq) + H⁺(aq) + H₂S(g) → Mn²⁺(aq) + S(s) + H₂O(ℓ)", "items": q9},
    {"id": "10", "title": "Question 10", "kind": "Extracting gold and iron", "marks": 10,
     "lead": "Gold and iron extraction are important mining processes in South Africa. Refining takes place according to the following reactions:"
             "\n\nGold is dissolved using cyanide ions (CN⁻) to extract it from the ore:\n4Au(s) + 8NaCN(aq) + 2H₂O(ℓ) + O₂(g) → 4NaAu(CN)₂(aq) + "
             "4NaOH(aq)\n\nIron(III)oxide is burned in a furnace in the presence of CO:\nFe₂O₃(s) + 3CO(s) → 2Fe(ℓ) + 3CO₂(g)", "items": q10},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Grade 12 Physical Sciences P2 2025 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, another term's definition, the opposite choice, the reversed reasoning):
# never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns `each`;
# the cards are shuffled the same way every run. The rubric bullets above stay as the source. Where the memo's OR reading restates a
# point of its first reading, only the first reading is cards (one point twice can never earn two marks). No wrong card is another
# part's right answer word for word (2.1 leaves out bond length, 1.2's answer, and electronegativity, 1.1's).


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random(PID + ":" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    pool = sorted(k for k, i in enumerate(order) if i < len(right))
    # a single right card first, or every right card on top, would be an answer by position
    assert pool != list(range(len(pool))), (n, "the right cards on top: an answer by position", pool)
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count}


STATEMENTS = {
    # 2: the wrong ones are a repulsion, an intermolecular force, the bond energy, electrons only, a proton transfer
    "2.1": (2, ["A mutual attraction between two atoms resulting from the simultaneous attraction between their nuclei and (outer) electrons."],
               ["A mutual repulsion between two atoms resulting from the repulsion between their nuclei.",
                "An attraction between separate molecules of a substance.", "The energy needed to break one mole of bonds.",
                "A mutual attraction between two atoms resulting from the attraction between their electrons only.",
                "The transfer of a proton from one atom to another."]),
    # 2 ticks: the CN triple bond (the memo's "/" form, a higher order bond, the same reading) and the CH single bond
    "2.6": (1, ["The CN bond is a triple bond, with more orbitals overlapping.", "The CH bond is a single bond."],
               ["The CN bond is a single bond.", "The CH bond is a triple bond.", "The CN bond is longer, and longer bonds need more energy to break.",
                "Carbon is more electronegative than nitrogen.", "The CH bond has more orbitals overlapping than the CN bond."]),
    # 2 ticks: the comparison and its reason
    "2.7": (1, ["The CN bond is longer than the CH bond.", "The H atom is smaller than the N atom."],
               ["The CH bond is longer than the CN bond.", "The H atom is larger than the N atom.",
                "The CN bond is longer because nitrogen is less electronegative than hydrogen.",
                "Both bonds have the same length, because both contain a carbon atom."]),
    # 3 ticks: the memo's first reading (its OR reading, both polar / the forces / like dissolves like, restates it: no cards)
    "2.9": (1, ["HCN has polar molecules with dipole-dipole forces.", "H₂O has polar molecules with hydrogen bonds.",
                "The forces are of the same order (comparable), so the substances dissolve."],
               ["HCN has non-polar molecules with London forces only.", "H₂O has non-polar molecules with London forces only.",
                "The forces are very different in strength, so the substances dissolve.", "Polar and non-polar substances always dissolve in each other."]),
    # 3 ticks: the memo's three points (its OR form of the third, N₂'s weaker forces, says the same: no card)
    "3.1": (1, ["NH₃ has hydrogen bonds between its molecules.", "N₂ has London forces (induced dipole forces) between its molecules.",
                "NH₃ has stronger intermolecular forces than N₂ and therefore a higher boiling point than N₂."],
               ["NH₃ has London forces only between its molecules.", "N₂ has hydrogen bonds between its molecules.",
                "N₂ has stronger intermolecular forces than NH₃ and therefore a higher boiling point than NH₃.",
                "NH₃ has a higher boiling point because its N–H bonds are stronger than the bond in N₂."]),
    # 3 ticks: the memo's first reading, one form of its "/" (molecular mass); its OR reading turns the same points round: no cards
    "3.3": (1, ["H₂ and N₂ both have weak London forces (induced dipole forces).", "N₂ has a greater molecular mass than H₂.",
                "Therefore N₂ has stronger intermolecular forces than H₂."],
               ["H₂ has hydrogen bonds between its molecules.", "N₂ has dipole-dipole forces between its molecules.",
                "H₂ has a greater molecular mass than N₂.", "Therefore H₂ has stronger intermolecular forces than N₂."]),
    # 3 ticks: the choice (H₂) and the memo's first reading of the reasons (its OR, "boiling point is inversely proportional to vapour
    # pressure", replaces the second reason: neither a right nor a wrong card, so one point twice can never earn two marks)
    "3.4": (1, ["H₂ has the highest vapour pressure.", "H₂ has the weakest intermolecular forces (London forces).", "H₂ has the lowest boiling point."],
               ["NH₃ has the highest vapour pressure.", "N₂ has the highest vapour pressure.", "H₂ has the strongest intermolecular forces.",
                "H₂ has the highest boiling point."]),
    # 2, either of the memo's examples: the wrong ones reverse the trend, make it direct, ask a question, change the variables
    "4.2": (2, ["If the pressure of an enclosed gas increases, the volume will decrease, at constant temperature.",
                "The pressure of an enclosed gas is inversely proportional to the volume it occupies, if the temperature is kept constant."],
               ["If the pressure of an enclosed gas increases, the volume will increase, at constant temperature.",
                "The pressure of an enclosed gas is directly proportional to the volume it occupies, if the temperature is kept constant.",
                "What is the relationship between the pressure and the volume of an enclosed gas?",
                "If the temperature of an enclosed gas increases, its volume will decrease, at constant pressure."]),
    # 2 ticks: the high pressure and ONE reading of its "/" reason (the molecules' own volume and forces); the repulsion form: no card
    "4.5": (1, ["At high pressure a gas starts to deviate from ideal gas behaviour.",
                "The volume of the gas molecules and the intermolecular forces start to influence the measured value, making it greater than the "
                "calculated value."],
               ["At high pressure a gas behaves more like an ideal gas.", "At high pressure the gas molecules have no volume of their own.",
                "At high pressure the gas molecules move further apart.",
                "The measured volume is smaller than the calculated value because the molecules attract each other strongly."]),
    # 2 ticks: the memo's first reading (its OR, the forces become significant then the gas condenses, restates it: no cards)
    "4.7": (1, ["At a low temperature the molecules move slower and closer together.", "The gas starts to condense and no longer behaves like an ideal gas."],
               ["At a low temperature the molecules move faster and further apart.", "At a low temperature the molecules have more kinetic energy.",
                "At a low temperature the intermolecular forces disappear.", "At a low temperature the gas molecules take up no space at all."]),
    # 2 or 0: the wrong ones are 1 g of carbon-12, one particle's mass, 12 g of water, one particle's volume, a fixed mass of 1 g
    "6.1.1": (2, ["One mole is the amount of a substance having the same number of particles as there are atoms in 12 g carbon-12."],
                 ["One mole is the amount of a substance having the same number of particles as there are atoms in 1 g carbon-12.",
                  "One mole is the mass of one particle of a substance.",
                  "One mole is the amount of a substance having the same number of particles as there are molecules in 12 g of water.",
                  "One mole is the volume occupied by one particle of a gas.", "One mole is the amount of a substance that has a mass of exactly 1 g."]),
    # 2 or 0: the wrong ones are the maximum, ΔH, the products' energy, the average kinetic energy
    "7.1": (2, ["The minimum energy needed for a reaction to take place."],
               ["The maximum energy released during a reaction.", "The energy difference between the products and the reactants.",
                "The energy of the products of a reaction.", "The average kinetic energy of the particles of the reactants."]),
    # 1, any of the memo's OR forms: the wrong ones are the endothermic forms and an activated complex below the reactants
    "7.2": (1, ["More energy is released than absorbed.", "The energy of the products is less than the energy of the reactants.", "ΔH < 0 (ΔH is negative)."],
               ["More energy is absorbed than released.", "The energy of the products is greater than the energy of the reactants.",
                "ΔH > 0 (ΔH is positive).", "The activated complex has less energy than the reactants."]),
    # 2 or 0: the wrong ones drop the conditions, use mass, are Charles's law, fix 22,4 dm³ at any conditions, use equal masses
    "7.5": (2, ["One mole of any gas occupies the same volume at the same temperature and pressure."],
               ["One mole of any gas occupies the same volume at any temperature and pressure.",
                "One mole of any gas has the same mass at the same temperature and pressure.",
                "The volume of a fixed amount of gas is directly proportional to its Kelvin temperature at constant pressure.",
                "One mole of any substance occupies 22,4 dm³ at any temperature and pressure.",
                "Equal masses of all gases occupy the same volume at the same temperature and pressure."]),
    # 2 in one statement: the wrong ones are a proton donor (in two wordings), an electron acceptor, releasing H⁺, a positive charge.
    # The memo's one statement landed first at every card count (5 to 8: the seeded shuffle), so it is a card in two wordings (the
    # memo's, and "can accept a proton"), a pick of ONE, and the wrong proton donor is in two wordings too, so a pair of cards that say
    # the same thing never marks the right one
    "8.1": (2, ["A hydroxide ion can act as a proton acceptor.", "A hydroxide ion can accept a proton (an H⁺ ion)."],
               ["A hydroxide ion can act as a proton donor.", "A hydroxide ion can donate a proton (an H⁺ ion).",
                "A hydroxide ion can act as an electron acceptor.", "A hydroxide ion releases H⁺ ions in water.", "A hydroxide ion has a positive charge."]),
    # 2, either of the memo's forms: the wrong ones are the solution's mass, the molar mass, the inverse, a volume left out
    "8.4": (2, ["Concentration is the amount of solute per litre of solution.", "Concentration is the number of moles of a substance per dm³ of solution."],
               ["Concentration is the total mass of a solution.", "Concentration is the mass of one mole of a substance.",
                "Concentration is the volume of solution per mole of solute.", "Concentration is the number of moles of solute in any volume of solution."]),
    # 2: the wrong ones are oxidation, a loss of electrons, a gain of oxygen, a loss of hydrogen, a change in the nucleus, a rising
    # charge, a falling mass (7 wrong cards: with four to six the right card came first)
    "9.1": (2, ["Reduction is a decrease in oxidation number."],
               ["Reduction is an increase in oxidation number.", "Reduction is a loss of electrons.", "Reduction is a gain of oxygen.",
                "Reduction is a decrease in the number of protons in an atom.", "Reduction is a loss of hydrogen.",
                "Reduction is an increase in the charge of an ion.", "Reduction is a decrease in the mass of an atom."]),
    # 2 ticks: the increase and its values
    "9.4": (1, ["The oxidation number of S increases.", "It increases from −2 (in H₂S) to 0 (in S)."],
               ["The oxidation number of S decreases.", "It decreases from 0 (in S) to −2 (in H₂S).", "The oxidation number of Mn increases.",
                "The oxidation number of H increases from +1 to +2."]),
    # 2, the memo's two (it accepts any relevant answer: no other true disadvantage is a card); the wrong ones are open-cast's features
    # or not disadvantages at all
    "10.1": (1, ["It is dangerous for workers, because they can be trapped underground.", "It can cause sinkholes."],
                ["It leaves larger open pits on the surface than open-cast mining.",
                 "It removes the topsoil and vegetation over a larger area than open-cast mining.",
                 "It is cheaper and quicker to start than open-cast mining.", "It produces no waste rock or mine dumps."]),
    # 1: the wrong ones reverse the change, give the wrong value, or name gold or sodium
    "10.3": (1, ["The oxidation number of O decreases from 0 (in O₂) to −2 (in NaOH)."],
                ["The oxidation number of O increases from −2 to 0.", "The oxidation number of O decreases from 0 to −1.",
                 "The oxidation number of Au decreases from 0 to −1.", "The oxidation number of Na decreases from +1 to 0."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (10.1 asks for
# disadvantages only), so SORTS stays empty and sort_ is kept for parity.
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
        if _it.get("after"):   # its gate rides along onto the played part
            _m["items"][_k]["after"] = _it["after"]
assert not [i["n"] for m in missions for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"

assert tuple(AUTHORED) == ("2.4", "4.4", "4.8", "5.1", "5.2", "6.1.3", "6.1.4", "6.2.2", "7.3", "7.6", "7.7", "8.5", "8.6", "9.7", "10.5",
                           "10.6"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
nums = [i["n"] for i in ITEMS]
assert len(set(nums)) == len(nums), "a part number twice"
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == [], "no part is a one-value read-off"
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["2.3", "4.1", "6.2.1", "8.2", "9.3", "9.5", "10.2"]
assert [i["n"] for i in ITEMS if i.get("strict")] == ["6.2.1", "9.3", "9.5", "10.2"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.2.1", "2.2.2", "4.3", "7.4"]
for i in ITEMS:   # a built plot (build-play.js "plot"): one test per memo criterion, its marks the part's; every value inside the grid at every
    b = i.get("build") or {}   # scale the memo accepts (a tap snaps to a small square: always within half a small square of the value)
    if b.get("kind") == "plot":
        assert len(b["tests"]) == len(i["criteria"]) and sum(c["marks"] for c in i["criteria"]) == i["marks"], i["n"]
        assert all(set(t.get("ids", [])) <= {p["id"] for p in b["points"]} for t in b["tests"]), i["n"]
        for k, ax, n in ((0, b["x"], b["grid"]["nx"]), (1, b["y"], b["grid"]["ny"])):
            top = max(p["at"][k] for p in b["points"])
            assert set(ax["ok"]) <= set(ax["scales"]) and top <= min(ax["ok"]) * n and top * 2 > max(ax["ok"]) * n, (i["n"], k)
            assert all(top > s * n or top * 2 <= s * n for s in ax["scales"] if s not in ax["ok"]), (i["n"], k, "a scale left out holds the data on over half the grid")
assert all(nums.index(e) < nums.index(i["n"]) for i in ITEMS for e in i.get("after", [])), "a gate on a later part"
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]
assert PICKS == ["2.1", "2.6", "2.7", "2.9", "3.1", "3.3", "3.4", "4.2", "4.5", "4.7", "6.1.1", "7.1", "7.2", "7.5", "8.1", "8.4", "9.1", "9.4",
                 "10.1", "10.3"], PICKS
EQUATIONS = ["6.1.2", "8.3", "9.6", "10.4"]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2018", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Chemistry", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic chemistry errors (a unit not converted, a formula "
                                                       "upside down, a mole ratio or a molar mass wrong, the wrong constant, a value from the wrong "
                                                       "row or sample), 0 or full marks: " + ", ".join(AUTHORED) +
                                                       " (%d parts, %d marks). 2.4's one-line memo working (3 − 2,5 = 0,5) plays as its substitution "
                                                       "and its answer; 7.6's first working is the memo's OPTION 1 table, typed row by row; 9.7 "
                                                       "('Use the ion-electron method') plays as the memo's half-reactions and net ionic equation. "
                                                       "A value the memo also accepts is never a wrong option: 4.4's range 40,32 - 40,8 dm³ (any row "
                                                       "of the table), 5.2's 0,043 m³ by pV = nRT (its OPTION 2), 6.1.3's range 1,325 - 1,33 g, "
                                                       "6.1.4's range 11,33 - 11,67%% and its OPTION 3's 11,97%%, 10.6's 1,625 x 10⁶ g; a memo slip's "
                                                       "value neither (5.2's 427,78 / 426,58 dm³). 10.6 follows the memo's reading (65%% of the ore "
                                                       "is iron: 1 625 kg); 1 137,5 kg (65%% of the ore read as Fe₂O₃, then 10.5's 70%%) is never "
                                                       "an option." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "5.2", "kind": "memo_issue", "detail": "The memo (page 8) converts its 0,043 m³ to '(427,78 dm³)' (OPTION 1) and '(426,58 dm³)' "
                                                     "(OPTION 2): 0,042778 m³ = 42,78 dm³ and 0,042658 m³ = 42,66 dm³ (a power of ten slipped). "
                                                     "The right option shows the memo's 0,043 m³; the slipped dm³ values earn the marks too "
                                                     "(Murci's ruling 2026-10-10) and are never a wrong option."},
        {"n": "6.1.4", "kind": "memo_issue", "detail": "The memo (page 9) heads 6.1.4 'POSITIVE MARKING FROM QUESTION 6.3' (the paper has no 6.3: "
                                                       "6.1.3 is meant) and writes '% CaCO₃ unreacted' / '% CaCO₃ reacted' for the sodium "
                                                       "carbonate (Na₂CO₃) of the question. The right option writes Na₂CO₃; the numbers are the "
                                                       "memo's (11,33%%)."},
        {"n": "9.7", "kind": "memo_issue", "detail": "The memo (page 15) writes the reduction half-reaction as MnO₄⁻ + 8H⁺ + 5e⁻ → 2Mn²⁺ + 4H₂O "
                                                     "(Mn and charge unbalanced: one Mn²⁺); its net ionic equation 2MnO₄⁻ + 5H₂S + 6H⁺ → 2Mn²⁺ + "
                                                     "5S + 8H₂O is balanced. The right option writes the half-reaction with Mn²⁺; no option shows "
                                                     "the memo's 2Mn²⁺ half-reaction."},
        {"n": "7.7", "kind": "memo_issue", "detail": "The memo (page 12) writes n(O) = 76,2 / 16 = 4,625 mol; 76,2 / 16 = 4,7625 mol. Its ratio "
                                                     "1 : 1 : 3 and HNO₃ stand (4,7625 / 1,5857 = 3,00; its 4,625 gives 2,92). The right option "
                                                     "shows 4,7625 mol; the memo's 4,625 earns the marks too (Murci's ruling 2026-10-10) and is "
                                                     "in no option."},
        {"n": "3.1", "kind": "memo_issue", "detail": "The memo's OR line (page 4) reads '(Accept: less energy requires to overcome weaker forces of "
                                                     "H2)' where N₂ is meant (the question compares NH₃ and N₂). It is an ACCEPT note, not a card."},
        {"n": "1.10", "kind": "memo_issue", "detail": "The question paper (page 5) prints option D as MnO₂(aq) + 4HCℓ(aq) → MnCℓ₂(aq) + H₂O(ℓ) + "
                                                      "Cℓ₂(g), unbalanced (2H₂O balances it). Kept as printed: the memo's D stands, HCℓ is "
                                                      "oxidised to Cℓ₂ either way."},
        {"n": "10", "kind": "memo_issue", "detail": "The question paper (page 12) prints the iron reaction as Fe₂O₃(s) + 3CO(s) → 2Fe(ℓ) + 3CO₂(g): "
                                                    "carbon monoxide is a gas, CO(g). Kept as printed; no part depends on the phase."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions, the law and the hypothesis "
                                                    "(2.1, 4.2, 6.1.1, 7.1, 7.5, 8.1, 8.4, 9.1) pick one card for their 2 marks (an OR form the "
                                                    "memo accepts is a second right card); 7.2 and 10.3 pick one card for 1 mark (7.2's three OR "
                                                    "forms all right); the explanations (2.6, 2.7, 2.9, 3.1, 3.3, 4.5, 4.7, 9.4) and 10.1 pick the "
                                                    "memo's points, 1 mark each; 3.4 picks the choice (H₂) and its two reasons. Where the memo's OR "
                                                    "reading restates its first (2.9, 3.1, 3.3, 3.4, 4.5, 4.7), only the first reading is cards, "
                                                    "so one point twice can never earn two marks. 10.1's memo accepts any relevant answer: only its "
                                                    "two are right cards, and no other true disadvantage is a card. 8.1's one memo statement (a "
                                                    "proton acceptor) landed first at every card count of the seeded shuffle, so it is a card in two "
                                                    "wordings (a pick of ONE: no extra mark) beside the wrong proton donor in two wordings." % len(PICKS)},
        {"n": EQUATIONS[0], "kind": "no_fit", "detail": "'Balance the equation' (6.1.2), 'Write a balanced equation' (8.3) and the half-reactions "
                                                        "(9.6, 10.4) play as multiple choice of four equations, the memo's marks all or nothing: "
                                                        "the memo's equation and three wrong ones (unbalanced; electrons on the wrong side or "
                                                        "missing; the reverse reaction; water acting as the acid). 8.3's memo OR, HCℓ(aq) + NH₃(g) "
                                                        "→ NH₄⁺(aq) + Cℓ⁻(aq), is never a wrong option. 9.2 (an oxidation number, no working) plays "
                                                        "as an answer multiple choice; 3.2 (a FORMULA from the table's three substances) as "
                                                        "multiple choice of the three."},
        {"n": "2.2.1", "kind": "no_fit", "detail": "Drawings (2.2.1 and 2.2.2 the Lewis structures, 7.4 the "
                                                   "catalysed curve) are done on paper and self-checked against the memo's criteria."},
        {"n": "4.3", "kind": "no_fit", "detail": "The graph of volume versus pressure is BUILT on the answer sheet's grid (2026-10-11, build 'plot'): "
                                                 "8 big squares across and 8 up, its axes printed and labelled, no numbers: the learner chooses "
                                                 "each axis' scale (20 / 25 / 50 / 100 a big square: only 50 kPa and 25 dm³ hold the table and use "
                                                 "over half the grid), places the seven points and chooses the line (a smooth curve earns 'Curve "
                                                 "drawn'). The memo's 'table values as scale values: maximum 1/3' cannot arise: every scale offered "
                                                 "is even. The memo's graph plots 95 kPa at about 140 dm³; the paper's table gives 128 dm³, kept."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 10), hand-transcribed from the paper and memo PDFs and "
                                                           "their page images (the 1.5 graphs, the 1.8 ions, the 6.2 and Q7 graphs, the memo's Lewis "
                                                           "structures and workings are images); no API call."},
    ],
}
QTOTAL = {"1": 20, "2": 17, "3": 10, "4": 18, "5": 8, "6": 19, "7": 19, "8": 17, "9": 12, "10": 10}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's ten printed letters are the paper's (A2 B3 C2 D3) and the printed choices (2.5 A, 2.8 A, 3.2 A, 4.6 B)
# are fixed by their answers, so the authored four-option questions lean towards C and D: the 16 workings sit at A3 B4 C5 D4, the five
# answer / equation MCQs at A1 B1 C2 D1, the 31 four-option questions at A6 B8 C9 D8 and the whole paper at A9 B9 C9 D8
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 3, spread
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert min(wspread.values()) >= 3 and max(wspread.values()) <= 7, wspread
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, the paper:", spread, "authored:", wspread, "four-option:", fspread)
print("statement right-card positions:", {i["n"]: i["pool"] for i in ITEMS if i["t"] == "pickn"})
total = sum(i["marks"] for i in ITEMS)
assert total == 150 == paper["paper"]["total_marks"], total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; statements:", len(PICKS), "parts")
print("total:", total)
# GATES (the last check): a part whose stem, options, cards or criteria show an earlier part's answer opens only after it
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "2.6": ["2.2.1"], "2.9": ["2.5", "2.8"], "3.3": ["3.2"], "3.4": ["3.2", "3.3"], "4.2": ["4.1"], "4.7": ["4.6"], "5.2": ["5.1"],
    "6.1.4": ["6.1.3"], "6.2.2": ["6.2.1"], "7.3": ["7.2"], "8.6": ["8.5"], "9.4": ["9.3"], "9.6": ["9.3", "9.4"], "9.7": ["9.3", "9.4", "9.5", "9.6"],
    "10.3": ["10.2"]}, {i["n"]: i.get("after") for i in ITEMS if i.get("after")}
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
