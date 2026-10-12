"""Grade 11 Physical Sciences P2 (Chemistry) Nov 2017 (DBE common paper), the whole paper (Questions 1 to 10), hand-transcribed into the
catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper draws the 1.3 energy curve, the 6.1 and
6.2 graphs and the Q8 flow diagram and sets the 1.4 fractions as images, and the memo sets its Lewis diagrams, its 7.3 sketch, its
fractions and every working as images (its text layer turns fractions into columns of digits).

  python tools/ingest/transcribe_g11_ps_p2_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Physical Sciences P2 Nov 2017 Eng.pdf" "uploads/Grade 11 Physical Sciences P2 Nov 2017 MG Eng & Afr.pdf" --id g11-ps-p2-2017-11 --from-json

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; models: transcribe_ps_p2_2025_11.py, Chemistry, and the next year's
transcribe_g11_ps_p2_2018_11.py, whose structure this copies):
  multiple choice printed in the paper -> mcq as printed (1.3 prints its options as a table -> optTable, with its graph); a choice printed
  in the stem (3.4: water, ethanol or bromine) -> mcq of the printed choices. One term the memo names -> term (2.5.1, 2.5.2, 10.5); a
  substance's name or formula (2.4 H2O, 8.1.3 sodium sulphate, 8.1.4 HSO4-, 9.4 Cr2O7 2- / Cr6+) -> strict term. 2.3 (a count read off
  the Lewis structure) -> num. 9.1 (an oxidation number, no working) is an answer multiple choice.
  Every calculation ("Calculate", "Determine", "Use the answer to determine") -> authored multiple choice, `work`: the memo's FIRST
  working line by line and three workings each built from a DIFFERENT realistic chemistry error (a unit not converted, a formula upside
  down, a mole ratio or a molar mass wrong, the wrong constant, a value from the wrong row, a state swapped), every number recomputed;
  0 or full marks. A value the memo also accepts (its OPTIONS, its "any coordinates") is never a wrong option. 9.6 ("using the
  ion-electron method", the memo's half-reactions then the net ionic equation) plays as a working too. "Balance the equation" /
  "Write down a balanced equation" (6.1.1, 8.1.2) and the half-reaction (9.5) -> multiple choice of four equations, all or nothing.
  A definition -> statements (pick 1 card for its marks; an OR form a second right card); a conclusion or one memo statement worth 2
  (4.2, 4.3, 6.1.2, 10.4) picks 1 card for its 2 marks; an explanation the memo ticks point by point, or a choice with its reason
  (6.2.1, 7.2, 9.3, 10.2) -> statements, 1 mark a point; 8.1.5's two conjugate pairs pick 2 cards, 2 marks each. No memo here weighs
  two sides, so no part plays as a sort. Drawings (2.2.1 and 2.2.2 Lewis structures, 4.1 the graph on the ANSWER SHEET, 7.3 the
  potential energy sketch) -> draw with the memo's criteria, self-checked (flagged no_fit).
  A part whose stem, options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose lead changes part-way is two missions (6 and 6.2; 8 and 8.2).
Figure boxes are measured in PDF points (page 595.32 x 841.92, read from the PDF) tight to the ink (drawings and labels) and checked on a
contact sheet of the 1%-padded crops (scratchpad lower/g11-ps-p2-2017-11/figs.py)."""
import json
import random
import re
from pathlib import Path

PID = "g11-ps-p2-2017-11"
W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.3": [3, 128.0, 507.5, 446.0, 647.7], "Q5": [8, 233.3, 153.3, 350.9, 236.5], "Q6": [8, 166.8, 544.9, 400.9, 653.0],
    "Q6.2": [9, 168.4, 221.2, 387.1, 354.0], "Q8": [10, 137.4, 141.0, 448.0, 270.3]}


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
    mcq("1.1", "Which ONE of the bonds between the atoms below has the highest polarity?", ["H - C", "H - Cℓ", "H - O", "H - N"], 2,
        ["Where on the data sheet do you find the electronegativity of each element?",
         "How does the electronegativity difference between two bonded atoms affect the polarity of their bond?"]),
    mcq("1.2", "Solid iodine sublimes easily. The intermolecular forces present in iodine are …",
        ["London forces.", "hydrogen bonding.", "ion-dipole forces.", "dipole-dipole forces."], 0,
        ["Do the two atoms of an I₂ molecule differ in electronegativity, so that the molecule could be polar?",
         "Which intermolecular forces can act between molecules that have no permanent dipole?"]),
    mcq("1.3", "The graph below shows how the potential energy varies with distance between the nuclei of two nitrogen atoms when a double "
        "bond between the nitrogen atoms (N = N) is formed.\n\nChoose from the table the bond length and bond energy for N = N.",
        ["120; 0", "125; 518", "125; 418", "130; −100"], 2,
        ["Where on the curve is the potential energy of the two atoms at its lowest, and at what distance between the nuclei?",
         "Is bond energy the energy needed to break the bond, and what sign does it carry?"],
        optTable={"head": ["BOND LENGTH (pm)", "BOND ENERGY (kJ·mol⁻¹)"], "rows": [["120", "0"], ["125", "518"], ["125", "418"], ["130", "−100"]]},
        figure=fig("1.3", "A graph of potential energy (kJ·mol⁻¹), up, against distance between nuclei (pm), across, with 120 to 140 pm marked: "
                   "the curve falls steeply, dips to a minimum below zero and rises again to level off just below zero; dashed lines link "
                   "marked energy levels to marked distances.")),
    mcq("1.4", "According to Boyle's law, …",
        ["p ∝ 1/V if T is constant.", "V ∝ T if p is constant.", "V ∝ 1/T if p is constant.", "p ∝ V if n is constant."], 0,
        ["Which two quantities of a gas does Boyle's law relate, and which quantity must stay constant?",
         "What happens to the pressure of a gas when you squeeze it into half the volume?"]),
    mcq("1.5", "One mole of any gas occupies the same volume at the same temperature and pressure.\n\nThis statement is known as …",
        ["Charles's law.", "Gay Lussac's law.", "Avogadro's law.", "the ideal gas LAW."], 2,
        ["What do Charles's law and Gay Lussac's law each relate the temperature of a gas to?",
         "Which law compares equal amounts of DIFFERENT gases?"]),
    mcq("1.6", "One mole of a gas, SEALED in a container, has volume V at temperature T and pressure p. If the pressure is increased to 3p, "
        "the ratio between the volume and temperature (V : T) is …", ["1 : ⅓", "3 : 1", "⅓ : 3", "1 : 3"], 3,
        ["Can the volume of a gas sealed in a container change?",
         "At constant volume, what happens to the Kelvin temperature of a gas when its pressure is tripled?"]),
    mcq("1.7", "The chemical equation that represents an endothermic reaction:",
        ["NH₄NO₃(s) + H₂O(ℓ) → NH₄⁺(aq) + NO₃⁻(aq)   ΔH > 0", "2Mg(s) + O₂(g) → 2MgO(s)   ΔH < 0",
         "Zn(s) + 2HCℓ(aq) → ZnCℓ₂(aq) + H₂(g) + heat", "H₂(g) + Cℓ₂(g) → 2HCℓ(g)   ΔH = −131 kJ·mol⁻¹"], 0,
        ["Is energy absorbed or released in an endothermic reaction?",
         "What sign does ΔH have when the products have more energy than the reactants?"]),
    mcq("1.8", "The CORRECT formula for nitric acid:", ["H₂SO₄", "CH₃COOH", "NH₃", "HNO₃"], 3,
        ["Which element does the name 'nitric' point to?", "Which acid or base does each of the other formulas stand for?"]),
    mcq("1.9", "Consider the reaction below.\nZn(s) + CuSO₄(aq) → ZnSO₄(aq) + Cu(s)\n\nWhich substance is the oxidising agent?",
        ["Zn", "Cu²⁺", "Zn²⁺", "Cu"], 1,
        ["Is an oxidising agent itself oxidised or reduced in a reaction?", "Which particle gains electrons in this reaction?"]),
    mcq("1.10", "Which ONE of the reactions below will produce the salt sodium ethanoate (sodium acetate)?",
        ["HCℓ(s) + CH₃COOH(aq) →", "CH₃COOH(aq) + H₂O(ℓ) →", "CH₃COOH(aq) + NaOH(aq) →", "H₂CO₃(aq) + NaOH(aq) →"], 2,
        ["Which kind of reaction forms a salt from an acid?", "From which acid does an ethanoate salt get its name?"]),
]

# ---- QUESTION 2, the question paper page 6 and the memo page 3 ----
q2 = [
    rub("2.1", "Define the term covalent bond.", 2, ["A covalent bond is the sharing of electrons between two atoms to form a molecule. (2)"],
        ["How is a covalent bond different from an ionic bond?", "Between which particles does a covalent bond form, and what do they make together?"],
        each=2),
    draw("2.2.1", "Draw Lewis structures for: CH₃Cℓ", 2, [
        ["C shares one pair of electrons with each of the three H atoms and one pair with Cℓ, and Cℓ has three lone pairs", 2]],
        ["How many valence electrons do C, H and Cℓ each have?",
         "How many electron pairs must surround C, and Cℓ, for each to have a full outer energy level?"],
        memo="The memo's structure: C in the middle with an H above, an H below and an H to the left, each joined by one shared pair, and Cℓ to "
             "the right joined by one shared pair, with three lone pairs on Cℓ."),
    draw("2.2.2", "Draw Lewis structures for: CO₂", 2, [["C shares two pairs of electrons with each O atom, and each O atom has two lone pairs", 2]],
         ["How many valence electrons do carbon and oxygen each have?",
          "How many pairs must C share with each O atom so that every atom has eight electrons around it?"],
         memo="The memo's structure: O::C::O, two shared pairs between C and each O, and two lone pairs on each O."),
    num("2.3", "How many lone-pair electrons are on the central atom in the CO₂ molecule?", 0, 0, "",
        ["Which atom is the central atom in CO₂?", "How many of the central atom's valence electrons are used in its bonds with the two O atoms?"]),
    term("2.4", "Identify ONE of the substances in Reaction 2 that can form a dative covalent bond when reacting with an acid.", ["H2O", "Water"],
         ["What must an atom have to donate both electrons of a dative covalent bond?",
          "Which particle does an acid give to the substance it reacts with?"], strict=True),
    term("2.5.1", "Write down the shape of the H₂O molecule.", ["Angular", "Bent", "Angular shape", "Bent shape", "Angular molecule"],
         ["How many atoms are bonded to the oxygen atom, and how many lone pairs does it have?",
          "How do lone pairs on the central atom push the bonded atoms in the VSEPR model?"]),
    term("2.5.2", "Write down the shape of the CO₂ molecule.", ["Linear", "Linear shape", "Linear molecule"],
         ["How many atoms are bonded to the central carbon atom, and does it have any lone pairs?",
          "How far apart do two groups of electrons around a central atom push each other?"]),
    rub("2.6", "Although the molecules of CH₄ and CH₃Cℓ have the same shape, CH₄ is non-polar, while CH₃Cℓ is polar. Give a reason for the "
        "difference in molecular polarity.", 1, [
        "(The charge distribution in) CH₃Cℓ is asymmetrical and CH₄ is symmetrical. (1)",
        "OR — The chlorine has a higher electronegativity than the hydrogen. (1)"],
        ["When four identical bonds surround a carbon atom, do their dipoles cancel?",
         "Use the data sheet: how do the electronegativities of chlorine and hydrogen compare?"]),
]

# ---- QUESTION 3, the question paper pages 6-7 and the memo pages 3-4 ----
q3 = [
    rub("3.1", "Explain why ethanol is soluble in water. Refer to the relative strength of the intermolecular forces in ethanol and water.", 3, [
        "Both water and ethanol have hydrogen bonds (1)", "which are the same in relative strength. (1)",
        "Substances with comparable relative strength in intermolecular forces will dissolve. (1)"],
        ["Which type of intermolecular force acts between ethanol molecules, and which between water molecules?",
         "When can the molecules of two substances mix, replacing the forces within each substance?"]),
    rub("3.2", "Explain why the boiling point of iodine is higher than that of bromine. Refer to the intermolecular forces present in EACH "
        "substance in the explanation.", 3, [
        "The intermolecular forces between the molecules of iodine and bromine are both London forces (Van der Waals forces/Induced dipole "
        "forces). (1)",
        "Iodine molecules have a bigger molecular mass than the molecules of bromine/iodine molecules have a larger surface area than "
        "molecules of bromine/iodine molecules have more electrons than that of bromine and thus have a larger polarity (any option) (1)",
        "The bigger the molecules/larger the surface area of the molecules, the stronger the intermolecular forces. (1)"],
        ["Are Br₂ and I₂ polar or non-polar, and which forces act between their molecules?",
         "How does the size of a molecule affect the strength of its London forces?"]),
    rub("3.3", "Explain why phosphine will evaporate faster than ammonia by referring to the types of intermolecular forces present in EACH "
        "substance.", 4, [
        "The intermolecular forces between phosphine molecules are dipole-dipole forces/Van der Waals forces. (1)",
        "The intermolecular forces between ammonia molecules are hydrogen bonds. (1)", "The dipole-dipole forces are weaker than the hydrogen bonds. (1)",
        "Weaker forces will cause the molecules to evaporate faster/stronger forces will evaporate slower (1)"],
        ["To which atom is hydrogen bonded in NH₃ and in PH₃, and which of the two can form hydrogen bonds?",
         "How does the strength of the intermolecular forces affect how fast a liquid evaporates?"]),
    mcq("3.4", "Water, ethanol and bromine are all liquids at room temperature.\n\nWhich ONE will have the highest vapour pressure?",
        ["Water", "Ethanol", "Bromine"], 2,
        ["How are the vapour pressure and the boiling point of a liquid related?",
         "What do the boiling points in the table tell you about the strength of each liquid's intermolecular forces?"], marks=1),
    rub("3.5", "Give a reason for the answer to QUESTION 3.4 by referring to the relative strength of the intermolecular forces and boiling "
        "points.", 2, [
        "The boiling point of bromine is lower than the other two liquids therefore it has weaker intermolecular forces. (1)",
        "If the intermolecular forces are weaker, the vapour pressure will be higher. (1)",
        "OR — The boiling point of water and ethanol are higher than bromine, therefore it has stronger intermolecular forces. (1)",
        "If the intermolecular forces are stronger, the vapour pressure will be lower. (1)"],
        ["How does a liquid's boiling point compare with the strength of its intermolecular forces?",
         "How does the strength of the forces between molecules affect how easily they escape from the liquid?"],
        notes=["NEGATIVE MARKING FROM 3.4"],
        after=["3.4"]),   # its cards: bromine has the weaker forces and the higher vapour pressure (3.4's answer)
]

# ---- QUESTION 4, the question paper page 7 (ANSWER SHEET page 16) and the memo pages 5-7 ----
q4 = [
    # BUILT on the answer sheet's grid (2026-10-11, build "plot"): its axes printed and labelled (Pressure (kPa) up, Temperature (K)
    # across) on 11 big squares across and 7 up, 10 small squares in each, no numbers. The memo's four criteria (memo page 5, its graph
    # to scale on page 12): the scale on both axes (1: 50 K and 50 kPa a big square, the only choices that hold 450 K and 280,5 kPa and
    # use over half the grid); three or more points right (1: within half a small square of the learner's own scale); a line of best fit
    # (1: a straight line within two small squares of each of the learner's points); drawn to the origin (1: the straight line reaches
    # the y-axis within 7,5 kPa of 0, extrapolated as the stem asks)
    {**draw("4.1", "Draw a graph of pressure versus temperature on the attached ANSWER SHEET. Extrapolate the graph so that it intersects the "
            "y-axis.", 4, [
        ["Use of correct scale on both axes", 1], ["At least three (3) points plotted correctly", 1], ["Line of best fit drawn", 1],
        ["Graph drawn to the origin", 1]],
        ["Which quantity goes on the vertical axis of a graph of pressure versus temperature?",
         "What scale lets the largest temperature and the largest pressure in the table fit on the grid?"],
        memo="The memo's graph: Pressure (kPa), 0 to 300, up, against Temperature (K), 0 to 500, across: the five points of the table on a "
             "straight line, extended back through the origin."),
     "build": {"kind": "plot", "grid": {"nx": 11, "ny": 7, "sub": 10}, "extend": True,
               "x": {"name": "Temperature (K)", "unit": "K", "scales": [20, 25, 50, 100], "ok": [50]},
               "y": {"name": "Pressure (kPa)", "unit": "kPa", "scales": [20, 25, 50, 100], "ok": [50]},
               "points": [{"id": "t%d" % k, "name": "T = %d K" % t, "at": [t, p]}
                          for k, (t, p) in enumerate([(250, 155.8), (300, 187.0), (350, 218.1), (400, 249.3), (450, 280.5)])], "tol": [2.5, 2.5],
               "tests": [{"k": "scale"}, {"k": "points", "min": 3}, {"k": "fit", "min": 3, "tol": 10},
                         {"k": "extrap", "name": "Extended", "x": 0, "y": 0, "tol": 7.5}]}},
    rub("4.2", "What conclusion can be made from the final graph?", 2, [
        "Pressure of an enclosed gas is directly proportional to the temperature (1) if the volume stays constant. (1)",
        "OR — As the pressure of an enclosed gas increases, the temperature increases (1) proportionately. (1)"],
        ["What does a straight-line graph that passes through the origin tell you about two quantities?",
         "Which condition must you state for the relationship to hold?"], each=2,
        after=["4.1"]),   # its cards: pressure directly proportional to temperature (4.1's straight line through the origin)
    rub("4.3", "Explain why it will not be possible to obtain accurate values at very low temperatures.", 2, [
        "At very low temperature values, the gas will liquify, not acting like a gas anymore. (2)"],
        ["What happens to the motion of gas molecules, and to the forces between them, as the temperature drops?",
         "Is oxygen still a gas at, say, 50 K?"], each=2),
    rub("4.4", "Use the kinetic molecular theory to explain the effect of an increase in temperature on the pressure of a gas.", 4, [
        "If the temperature increases, the average kinetic energy of the particles increases. (1)", "The particles move faster. (1)",
        "The number of collisions between the particles increase (and force per unit area). (1)",
        "If the number of collisions increases, the pressure increases. (1)"],
        ["What does the temperature of a gas tell you about the motion of its particles?",
         "What causes the pressure a gas exerts on the walls of its container?"]),
    rub("4.5", "Under which conditions of temperature and pressure will a real gas act as an ideal gas?", 2, ["High temperature (1)", "Low pressure (1)"],
        ["Which assumptions about ideal gas particles stop being true when the particles are close together and slow?",
         "How do the temperature and the pressure each affect how close together and how fast the particles are?"]),
    work("4.6", "Calculate the gradient of the graph.", 3, [
        "Gradient = {450 − 250}/{280,5 − 155,8}\n= 1,60",                                 # the gradient turned upside down (run over rise)
        "Gradient = {280,5 − 155,8}/{450 − 250}\n= 0,62",                                 # the memo (any coordinates of the line give 0,62)
        "Gradient = {249,3 − 155,8}/{450 − 250}\n= 0,47",                                 # a pressure from the wrong row (400 K) with 450 K
        "Gradient = {155,8 − 280,5}/{450 − 250}\n= −0,62"], 1,                            # the two points taken in a different order above and below
        ["Which two points of the straight line can you read from the table?",
         "Which quantity is on the vertical axis of your graph, and which on the horizontal axis?"]),
    work("4.7", "Use the answer to QUESTION 4.6 to determine the volume of the container.", 5, [
        "n = {m}/{M} = {48}/{32}\nn = 1,5 mol\nGradient = {nR}/{V}\n0,62 = {1,5(8,31)}/{V}\nV = 20,10 m³",      # the gradient left in kPa·K⁻¹
        "n = {m}/{M} = {48}/{16}\nn = 3 mol\nGradient = {nR}/{V}\n620 = {3(8,31)}/{V}\nV = 0,04 m³",            # oxygen taken as O atoms (M = 16)
        "n = {m}/{M} = {48}/{32}\nn = 1,5 mol\nGradient = {V}/{nR}\n620 = {V}/{1,5(8,31)}\nV = 7 728,30 m³",    # the gradient's formula upside down
        "n = {m}/{M} = {48}/{32}\nn = 1,5 mol\nGradient = {nR}/{V}\n620 = {1,5(8,31)}/{V}\nV = 0,02 m³"], 3,    # the memo (its 20,1 dm³)
        ["How does pV = nRT give an expression for p/T, the gradient of the graph?",
         "In which unit must the pressure be when you use R = 8,31 J·K⁻¹·mol⁻¹?"],
        after=["4.6"]),   # the options show 4.6's gradient (0,62 kPa·K⁻¹ = 620 Pa·K⁻¹)
]

# ---- QUESTION 5, the question paper page 8 and the memo page 7 ----
q5 = [
    work("5.1", "Calculate the temperature of the gas, in °C, in the balloon when it bursts.", 4, [
        "{p₁V₁}/{T₁} = {p₂V₂}/{T₂}\n{105 000(12,6)}/{298} = {27 640(36,3)}/{T₂}\nT₂ = 226 K\nT₂ = −47 °C",   # the memo
        "{p₁V₁}/{T₁} = {p₂V₂}/{T₂}\n{105 000(12,6)}/{25} = {27 640(36,3)}/{T₂}\nT₂ = 19 K\nT₂ = −254 °C",   # the temperature left in °C
        "{p₁V₁}/{T₁} = {p₂V₂}/{T₂}\n{105 000(12,6)}/{298} = {27 640(36,3)}/{T₂}\nT₂ = 226 K\nT₂ = 499 °C",  # 273 added, not subtracted
        "{p₁V₁}/{T₁} = {p₂V₂}/{T₂}\n{27 640(36,3)}/{298} = {105 000(12,6)}/{T₂}\nT₂ = 393 K\nT₂ = 120 °C"], 0,   # the two states swapped
        ["Which values describe the gas when it is released, and which when the balloon bursts?",
         "In which unit must the temperature be in a gas law calculation, and how do you change it back to °C?"]),
    work("5.2", "Calculate the initial amount of gas (in moles) in the balloon.", 4, [
        "pV = nRT\n(105 000)(12,6) = n(8,31)(25)\nn = 6 368,23 mol",                       # the temperature left in °C
        "pV = nRT\n(105)(12,6) = n(8,31)(298)\nn = 0,53 mol",                              # the pressure taken in kPa
        "pV = nRT\n(105 000)(12,6) = n(8,31)(298)\nn = 534,25 mol",                        # the memo
        "n = {V}/{Vm}\nn = {12 600}/{22,4}\nn = 562,5 mol"], 2,                            # the molar gas volume at STP (the gas is not at STP)
        ["Which equation links the pressure, volume, temperature and amount of a gas?",
         "In which units must p, V and T be when R = 8,31 J·K⁻¹·mol⁻¹?"]),
]

# ---- QUESTION 6, the question paper pages 8-9 and the memo page 8 ----
q6a = [
    # a balanced equation as multiple choice (the memo: 2H₂O₂ and 2H₂O, 1 mark each, played all or nothing): the memo's equation and three
    # wrong ones (left as printed, the oxygen over-balanced, a formula changed to balance it)
    mcq("6.1.1", "Balance the equation." + EQ, [
        "2H₂O₂(aq) → 2H₂O(ℓ) + O₂(g)", "H₂O₂(aq) → H₂O(ℓ) + O₂(g)", "2H₂O₂(aq) → 2H₂O(ℓ) + 2O₂(g)", "H₂O₂(aq) → H₂O(ℓ) + O(g)"], 0,
        ["How many oxygen atoms are on each side of the equation as printed?",
         "When you balance an equation, may you change a formula, or only the numbers in front of the formulas?"]),
    rub("6.1.2", "How would a catalyst affect the reaction?", 2, ["The catalyst lowers the activation energy of the reaction. (2)"],
        ["How does a catalyst change the path a reaction takes?",
         "Does a catalyst change how much oxygen forms in the end, or something about how the particles react?"], each=2),
    work("6.1.3", "Use the information on the graph to calculate the mass of hydrogen peroxide that decomposed.", 6, [
        "n = {V}/{Vm}\nn = {600}/{24,45}\nn = 24,54 mol of O₂\nH₂O₂ : O₂ = 2 : 1\nn = 49,08 mol of H₂O₂\nn = {m}/{M}\n"
        "49,08 = {m}/{34}\nm = 1 668,72 g",                                                  # 600 cm³ not converted to dm³
        "n = {V}/{Vm}\nn = {0,6}/{24,45}\nn = 0,0245 mol of O₂\nH₂O₂ : O₂ = 2 : 1\nn = 0,049 mol of H₂O₂\nn = {m}/{M}\n"
        "0,049 = {m}/{34}\nm = 1,67 g",                                                      # the memo's OPTION 1 (its OPTION 2 gives 1,67 g too)
        "n = {V}/{Vm}\nn = {0,6}/{24,45}\nn = 0,0245 mol of O₂\nH₂O₂ : O₂ = 1 : 1\nn = 0,0245 mol of H₂O₂\nn = {m}/{M}\n"
        "0,0245 = {m}/{34}\nm = 0,83 g",                                                     # the 2 : 1 ratio not applied
        "n = {V}/{Vm}\nn = {0,6}/{22,4}\nn = 0,0268 mol of O₂\nH₂O₂ : O₂ = 2 : 1\nn = 0,0536 mol of H₂O₂\nn = {m}/{M}\n"
        "0,0536 = {m}/{34}\nm = 1,82 g"], 1,                                                 # the molar gas volume at STP, not the stem's 24,45
        ["In which unit must the volume of O₂ read from the graph be when Vm = 24,45 dm³?",
         "Use your balanced equation: how many moles of H₂O₂ decompose for each mole of O₂ formed?"],
        after=["6.1.1"]),   # the options show the 2 : 1 ratio of the balanced equation (6.1.1's answer)
]
q6b = [
    rub("6.2.1", "Identify the limiting agent in this reaction. Give a reason for the answer.", 2, [
        "Magnesium (1)", "the mass of magnesium after 3 minutes/at the end of the reaction was zero (1)"],
        ["Which reactant runs out first, and so stops the reaction?", "What does the graph show about the magnesium when the reaction stops?"]),
    work("6.2.2", "Calculate the number of moles of unreacted hydrochloric acid in the test tube after 3 minutes.", 7, [
        "c = {n}/{V}\n0,36 = {n}/{0,5}\nn = 0,18 mol of HCℓ\nn = {m}/{M} = {1,2}/{24}\nn = 0,05 mol of Mg\nMg : HCℓ = 1 : 1\n"
        "n = 0,05 mol of HCℓ reacted\nn(HCℓ) left = 0,18 − 0,05 = 0,13 mol",                # the 1 : 2 ratio not applied
        "c = {n}/{V}\n0,36 = {n}/{500}\nn = 180 mol of HCℓ\nn = {m}/{M} = {1,2}/{24}\nn = 0,05 mol of Mg\nMg : HCℓ = 1 : 2\n"
        "n = 0,1 mol of HCℓ reacted\nn(HCℓ) left = 180 − 0,1 = 179,9 mol",                  # 500 cm³ not converted to dm³
        "c = {n}/{V}\n0,36 = {0,5}/{n}\nn = 1,39 mol of HCℓ\nn = {m}/{M} = {1,2}/{24}\nn = 0,05 mol of Mg\nMg : HCℓ = 1 : 2\n"
        "n = 0,1 mol of HCℓ reacted\nn(HCℓ) left = 1,39 − 0,1 = 1,29 mol",                  # n and V swapped in c = n/V
        "c = {n}/{V}\n0,36 = {n}/{0,5}\nn = 0,18 mol of HCℓ\nn = {m}/{M} = {1,2}/{24}\nn = 0,05 mol of Mg\nMg : HCℓ = 1 : 2\n"
        "n = 0,1 mol of HCℓ reacted\nn(HCℓ) left = 0,18 − 0,1 = 0,08 mol"], 3,              # the memo
        ["How many moles of HCℓ were added at the start, and in which unit must the 500 cm³ be?",
         "Use the balanced equation: how many moles of HCℓ react with one mole of Mg?"],
        after=["6.2.1"]),   # the options show all 1,2 g of magnesium reacting with HCℓ left over: 6.2.1's limiting agent
]

# ---- QUESTION 7, the question paper page 9 and the memo page 9 ----
q7 = [
    rub("7.1", "Define the term activation energy.", 2, ["The minimum energy needed for a reaction to take place. (2)"],
        ["Do all colliding particles react, or only some of them?", "What must colliding particles have, besides the right orientation, to react?"],
        each=2, notes=["[2 or 0]"]),
    rub("7.2", "Is the combustion reaction of butane exothermic or endothermic? Give a reason for the answer.", 2, [
        "An exothermic reaction (1)", "releases energy OR ΔH < 0 (1)"],
        ["What does the sign of ΔH in the equation tell you?",
         "How do the energies of the products and the reactants compare when ΔH has this sign?"]),
    draw("7.3", "Draw a sketch graph of potential energy versus course of reaction for the reaction above.\n\nClearly indicate the following on "
         "the graph:\n• Activation energy\n• Heat of reaction (ΔH)\n• Reactants and products", 3, [
        ["Activation energy Ea in the correct position and labelled", 1], ["Heat of reaction ΔH in the correct position and labelled", 1],
        ["Products have lower energy than reactants", 1]],
        ["From which level to which level is the activation energy measured?",
         "What does the sign of ΔH tell you about where the products sit compared with the reactants?"],
        memo="The memo's sketch: potential energy, up, against time (its label for the course of reaction), across: a level line for the "
             "reactants, a hump, then a level line for the products below the reactants; Ea marked from the reactants' level to the top of "
             "the hump, ΔH from the reactants' level down to the products' level.",
        after=["7.2"]),   # its criteria: products lower than reactants (7.2's exothermic and its reason)
    work("7.4", "Determine the empirical formula of butane gas if it consists of 82,76% carbon and 17,24% hydrogen.", 4, [
        "n(C) = {82,76}/{6} = 13,793 mol\nn(H) = {17,24}/{1} = 17,24 mol\n"
        "C : H = {13,793}/{13,793} : {17,24}/{13,793} = 1 : 1,25\nC : H = 4 : 5\nEmpirical formula: C₄H₅",          # the atomic number taken as M
        "n(C) = 82,76 mol\nn(H) = 17,24 mol\n"
        "C : H = {82,76}/{17,24} : {17,24}/{17,24} = 4,8 : 1\nC : H = 24 : 5\nEmpirical formula: C₂₄H₅",            # % not turned into moles
        "n(C) = {82,76}/{12} = 6,897 mol\nn(H) = {17,24}/{1} = 17,24 mol\n"
        "C : H = {6,897}/{6,897} : {17,24}/{6,897} = 1 : 2,5\nC : H = 2 : 5\nEmpirical formula: C₂H₅",               # the memo (it writes 6,896)
        "n(C) = {82,76}/{12} = 6,897 mol\nn(H) = {17,24}/{1} = 17,24 mol\n"
        "C : H = {6,897}/{6,897} : {17,24}/{6,897} = 1 : 2,5\nC : H = 1 : 3\nEmpirical formula: CH₃"], 2,            # 1 : 2,5 rounded up, not doubled
        ["How do you turn each percentage into a number of moles in a 100 g sample of butane?",
         "Which number do you divide every mole value by, and what do you do when the ratio is not a whole number?"]),
]

# ---- QUESTION 8, the question paper page 10 and the memo page 10 ----
q8a = [
    rub("8.1.1", "Define a Lowry-Brønsted base.", 2, ["A base is a proton acceptor. (2)"],
        ["Which particle is passed from one substance to another in a Lowry-Brønsted acid-base reaction?",
         "What does a Lowry-Brønsted acid do with that particle?"], each=2),
    # a balanced equation as multiple choice (the memo: reactants, products, balance, 1 mark each, played all or nothing): the memo's
    # equation and three wrong ones (unbalanced, the water left unbalanced, formulas changed to balance it)
    mcq("8.1.2", "Write down a balanced equation for Reaction 1." + EQ, [
        "H₂SO₄(aq) + NaOH(aq) → Na₂SO₄(aq) + H₂O(ℓ)", "H₂SO₄(aq) + 2NaOH(aq) → Na₂SO₄(aq) + 2H₂O(ℓ)",
        "H₂SO₄(aq) + 2NaOH(aq) → Na₂SO₄(aq) + H₂O(ℓ)", "H₂SO₄(aq) + Na(OH)₂(aq) → NaSO₄(aq) + 2H₂O(ℓ)"], 1, [
        "Which two products form when an acid neutralises a metal hydroxide?",
        "How many H⁺ ions can one H₂SO₄ give, and how many OH⁻ ions does one NaOH supply?"], marks=3),
    term("8.1.3", "Write down the NAME of the salt represented by X.", ["Sodium sulphate", "Sodium sulfate"],
         ["Which positive ion does the base supply, and which negative ion does the acid supply?",
          "How is a salt named from its positive and its negative ion?"], marks=2, strict=True),
    term("8.1.4", "Write down the FORMULA of ampholyte A.", ["HSO4-", "HSO4 -", "HSO4^-", "HSO4(-)"],
         ["What does H₂SO₄ give to H₂O in Reaction 2?", "What is left of H₂SO₄ after it loses one H⁺ ion, and what charge does it carry?"],
         marks=2, strict=True),
    rub("8.1.5", "Write down the formulae of the TWO conjugate acid-base pairs in Reaction 2.", 4, ["HSO₄⁻ and H₂SO₄ (2)", "H₂O and H₃O⁺ (2)"],
        ["How do the two members of a conjugate acid-base pair differ?",
         "Which particle in Reaction 2 does each acid become after it gives away an H⁺ ion?"], each=2,
        after=["8.1.4"]),   # its cards show HSO₄⁻ (8.1.4's ampholyte A)
]
q8b = [
    work("8.2.1", "Calculate the concentration of the NaOH solution.", 4, [
        "c = {m}/{MV}\nc = {6}/{(20)(0,5)}\nc = 0,6 mol·dm⁻³",                            # the atomic numbers added for M (11 + 8 + 1)
        "c = {m}/{MV}\nc = {6}/{(40)(5)}\nc = 0,03 mol·dm⁻³",                             # 500 cm³ taken as 5 dm³
        "c = {MV}/{m}\nc = {(40)(0,5)}/{6}\nc = 3,33 mol·dm⁻³",                           # the formula upside down
        "c = {m}/{MV}\nc = {6}/{(40)(0,5)}\nc = 0,3 mol·dm⁻³"], 3,                        # the memo's OPTION 1 (its OPTION 2 gives 0,3 too)
        ["In which unit must the 500 cm³ be for a concentration in mol·dm⁻³?", "What is the molar mass of NaOH?"]),
    work("8.2.2", "Calculate the percentage impurities in the NH₄Cℓ.", 6, [
        "n = {m}/{M} = {6}/{40}\nn = 0,15 mol of NaOH\nNaOH : NH₄Cℓ = 1 : 1\nn = {m}/{M}: 0,15 = {m}/{53,5}\nm = 8,025 g of NH₄Cℓ\n"
        "% pure = {8,025}/{10} × 100 = 80,25%\n% impurities = 100 − 80,25 = 19,75%",        # the memo (its OR, 1,975 g of 10 g, gives 19,75% too)
        "n = {m}/{M} = {6}/{40}\nn = 0,15 mol of NaOH\nNaOH : NH₄Cℓ = 1 : 1\nn = {m}/{M}: 0,15 = {m}/{50,5}\nm = 7,575 g of NH₄Cℓ\n"
        "% pure = {7,575}/{10} × 100 = 75,75%\n% impurities = 100 − 75,75 = 24,25%",        # M(NH₄Cℓ) with the four H counted once (50,5)
        "n = {m}/{M} = {6}/{40}\nn = 0,15 mol of NaOH\nNaOH : NH₄Cℓ = 1 : 1\nn = {m}/{M}: 0,15 = {m}/{53,5}\nm = 8,025 g of NH₄Cℓ\n"
        "% pure = {10}/{8,025} × 100 = 124,61%\n% impurities = 124,61 − 100 = 24,61%",       # the fraction upside down
        "n = {m}/{M} = {6}/{40}\nn = 0,15 mol of NaOH\nNaOH : NH₄Cℓ = 1 : 1\nn = {m}/{M}: 0,15 = {m}/{58,5}\nm = 8,775 g of NH₄Cℓ\n"
        "% pure = {8,775}/{10} × 100 = 87,75%\n% impurities = 100 − 87,75 = 12,25%"], 0,    # the molar mass of NaCℓ (58,5) used
        ["How many moles of NaOH react, and how many moles of NH₄Cℓ react with them?",
         "Which part of the 10 g of ammonium chloride is pure, and which part is impurity?"]),
]

# ---- QUESTION 9, the question paper pages 10-11 and the memo page 11 ----
CR = "Cr₂O₇²⁻"
q9 = [
    # the memo: Cr⁶⁺ (+6), no working: an answer multiple choice. The wrong ones: the ion's charge left out (+7), both Cr atoms together
    # (+12), chromium in the product (+3)
    mcq("9.1", "Determine the oxidation number of CHROMIUM in " + CR + "(aq).", ["+7", "+12", "+3", "+6"], 3,
        ["What is the oxidation number of each oxygen atom, and what is the charge on the whole ion?",
         "How many chromium atoms share the oxidation numbers that balance the oxygen?"]),
    rub("9.2", "Define reduction in terms of electron transfer.", 2, ["Gain of electrons (2)"],
        ["How is reduction the opposite of oxidation?",
         "What happens to the oxidation number of a substance that is reduced, and what does that tell you about its electrons?"], each=2),
    rub("9.3", "Write down the FORMULA of the substance that undergoes oxidation. Explain the answer in terms of oxidation numbers.", 2, [
        "Fe²⁺ (1)", "the oxidation number increases from +2 to +3 (1)"],
        ["How do you find the oxidation number of a simple ion such as Fe²⁺?",
         "How does the oxidation number of an element change when it is oxidised?"]),
    term("9.4", "Write down the FORMULA of the oxidising agent.", [
        "Cr2O7 2-", "Cr2O72-", "Cr2O7^2-", "Cr2O7(2-)", "Cr2O7 -2", "Cr6+", "Cr 6+", "Cr+6", "Cr^6+", "Cr(+6)"],
         ["Is an oxidising agent itself oxidised or reduced in the reaction?",
          "Which element's oxidation number decreases in the reaction?"], marks=2, strict=True),
    # a half-reaction as multiple choice (the paper's 2 marks, all or nothing): the memo's and three wrong ones: the oxidation (reversed),
    # the electrons on the wrong side, Cr unbalanced
    mcq("9.5", "Write down the reduction half-reaction." + EQ, [
        "2Cr³⁺ + 7H₂O → Cr₂O₇²⁻ + 14H⁺ + 6e⁻", "Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O", "Cr₂O₇²⁻ + 14H⁺ → 2Cr³⁺ + 7H₂O + 6e⁻",
        "Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → Cr³⁺ + 7H₂O"], 1,
        ["Where in Table 4 is the half-reaction for the substance that is reduced, and in which direction must you read it?",
         "How do you check that a half-reaction is balanced for atoms and for charge?"],
        after=["9.4"]),   # its options show Cr₂O₇²⁻ gaining electrons (9.4's oxidising agent)
    work("9.6", "Write down the net balanced ionic equation for the reaction, using the ion-electron method.", 3, [
        "Fe²⁺ → Fe³⁺ + e⁻\nCr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O\nCr₂O₇²⁻ + 14H⁺ + Fe²⁺ → 2Cr³⁺ + 7H₂O + Fe³⁺",        # the electrons not equalised
        "6Fe²⁺ → 6Fe³⁺ + 6e⁻\nCr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O\nCr₂O₇²⁻ + 14H⁺ + 6Fe²⁺ → 2Cr³⁺ + 7H₂O + 6Fe³⁺",  # the memo
        "3Fe²⁺ → 3Fe³⁺ + 3e⁻\nCr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O\nCr₂O₇²⁻ + 14H⁺ + 3Fe²⁺ → 2Cr³⁺ + 7H₂O + 3Fe³⁺",  # x 3 (one Cr's change)
        "6Fe²⁺ → 6Fe³⁺ + 6e⁻\nCr₂O₇²⁻ + 14H⁺ + 6e⁻ → Cr³⁺ + 7H₂O\nCr₂O₇²⁻ + 14H⁺ + 6Fe²⁺ → Cr³⁺ + 7H₂O + 6Fe³⁺"], 1,  # Cr not balanced
        ["How many electrons does one Fe²⁺ ion lose, and how many does one Cr₂O₇²⁻ ion gain?",
         "What must be true of the electrons lost and the electrons gained before you add the two half-reactions?"],
        after=["9.3", "9.4", "9.5"]),   # its options show Fe²⁺ oxidised (9.3), Cr₂O₇²⁻ reduced (9.4) and 9.5's half-reaction
]

# ---- QUESTION 10, the question paper page 11 and the memo page 11 ----
IRON = "Consider the iron extraction reaction. "
GOLD = "Consider the gold extraction reaction. "
q10 = [
    rub("10.1", "State TWO advantages of open-cast mining when compared to deep-shaft (underground) mining.", 2, [
        "Miners do not have to risk their lives going deep or being trapped underground. (1)", "No risk of sink holes (1)"],
        ["Where do the miners work in open-cast mining, compared with deep-shaft mining?",
         "What can happen to the ground above old underground tunnels?"], notes=["OR Any other relevant answer"]),
    rub("10.2", IRON + "Is iron oxidised or reduced during the reaction? Give a reason for the answer.", 2, [
        "Reduction (1)", "oxidation number of iron decreases from 6+ to 0. (1)"],
        ["How do you work out the oxidation number of iron from the formula Fe₂O₃?",
         "What is the oxidation number of an uncombined element, such as Fe(ℓ)?"]),
    rub("10.3", IRON + "State TWO disadvantages of using carbon in this reaction.", 2, [
        "Carbon is a non-renewable resource (1)", "Carbon dioxide as product can increase global warming (1)"],
        ["Where does the carbon used in the furnace come from, and can it be replaced?", "What does the CO₂ formed do in the atmosphere?"],
        notes=["OR Any other relevant answer"]),
    rub("10.4", GOLD + "Give ONE reason why gold is present as an element in the ore.", 2, ["The gold does not oxidize easily like iron. (2)"],
        ["Why are gold coins and jewellery still shiny after hundreds of years?",
         "What would happen to the gold in the rock if it reacted easily with oxygen and water?"], each=2),
    term("10.5", GOLD + "What role does oxygen gas (O₂) play in the reaction?", [
        "Oxidising agent", "Oxidizing agent", "An oxidising agent", "An oxidizing agent", "It acts as an oxidising agent",
        "It acts as oxidising agent", "Oxidant"],
         ["What happens to the oxidation number of oxygen from O₂ to NaOH?",
          "What does a substance that is reduced do to the substance it reacts with?"], marks=2),
]

BP_TABLE = {"head": ["NAME OF SUBSTANCE", "FORMULA", "BOILING POINT (°C)"],
            "rows": [["Water", "H₂O", "100"], ["Ethanol", "CH₃CH₂OH", "78"], ["Bromine", "Br₂", "58,8"], ["Iodine", "I₂", "184,3"],
                     ["Ammonia", "NH₃", "−33,3"], ["Phosphine", "PH₃", "−87,7"]]}
PT_TABLE = {"head": ["PRESSURE (kPa)", "TEMPERATURE (K)"],
            "rows": [["155,8", "250"], ["187,0", "300"], ["218,1", "350"], ["249,3", "400"], ["280,5", "450"]]}
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20, "lead": MC_LEAD, "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Bonding in methane reactions", "marks": 11,
     "lead": "Consider the following two reactions of methane (CH₄):\nReaction 1: CH₄(g) + HCℓ(g) → CH₃Cℓ(g) + H₂(g)\n"
             "Reaction 2: CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(g)", "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Intermolecular forces", "marks": 13,
     "lead": "Consider the list of six substances with their formulae and boiling points in the table below.", "table": BP_TABLE, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Pressure and temperature", "marks": 22,
     "lead": "In an experiment to investigate the relationship between pressure and temperature of an enclosed gas, 48 g of oxygen gas was "
             "sealed in a container. The results obtained are recorded in the table below.", "table": PT_TABLE, "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Weather balloon", "marks": 8,
     "lead": "Weather balloons are sent into space to gather data. The balloons usually burst at a pressure of 27 640 Pa and a volume of "
             "36,3 m³. The data collector then falls back to Earth.\n\nThe gas in a certain weather balloon has an initial volume of 12,6 m³ "
             "and pressure of 105 000 Pa at a temperature of 25 °C when it is released into space.",
     "figure": fig("Q5", "A round balloon on a string with a small box hanging below it, labelled balloon and data collector."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Decomposition of hydrogen peroxide", "marks": 10,
     "lead": "The decomposition of hydrogen peroxide in the presence of a catalyst at standard pressure and room temperature is given by the "
             "unbalanced chemical equation below.\nH₂O₂(aq) → H₂O(ℓ) + O₂(g)\n\nThe oxygen gas is collected and the volume is recorded over "
             "a period of time. The reaction is completed at time t.\n\nThe results are plotted on a graph of volume O₂ versus time, as shown "
             "below.\n\nTake the molar gas volume (Vm) as 24,45 dm³ at room temperature and standard pressure.",
     "figure": fig("Q6", "A graph of volume O₂ (cm³), up, against time (s), across: the curve rises from the origin, steeply at first, and "
                   "levels off; a dashed line from 600 on the volume axis meets the curve above t on the time axis, where a dashed line rises "
                   "from t."), "items": q6a},
    {"id": "6.2", "title": "Question 6.2", "kind": "Magnesium and hydrochloric acid", "marks": 9,
     "lead": "In an experiment, a learner adds 500 cm³ hydrochloric acid (HCℓ), with a concentration of 0,36 mol·dm⁻³, to 1,2 g of magnesium "
             "in a test tube. She records the change in the mass of magnesium as the reaction proceeds at regular intervals. The balanced "
             "chemical equation for the reaction is:\nMg(s) + 2HCℓ(aq) → MgCℓ₂(aq) + H₂(g)\n\nThe change in the mass of magnesium during the "
             "reaction is shown on the graph below.",
     "figure": fig("Q6.2", "A graph of the mass of magnesium (g), up, against time (min.), across, with 1, 2 and 3 marked on the time axis and "
                   "1,2 on the mass axis: the curve starts at 1,2 and falls, steeply at first and then more slowly."), "items": q6b},
    {"id": "7", "title": "Question 7", "kind": "Combustion of butane", "marks": 11,
     "lead": "The equation for the combustion of butane gas is given below.\nbutane(g) + 13O₂(g) → 8CO₂(g) + 10H₂O(g)   ΔH < 0", "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Reactions of sulphuric acid", "marks": 13,
     "lead": "Two reactions of sulphuric acid are shown in the diagram below.",
     "figure": fig("Q8", "A flow diagram: from H₂SO₄ an arrow labelled Reaction 1 and NaOH points to Salt X + Product Y, and an arrow labelled "
                   "Reaction 2 and H₂O points down to Ampholyte A + H₃O⁺."), "items": q8a},
    {"id": "8.2", "title": "Question 8.2", "kind": "Impure ammonium chloride", "marks": 10,
     "lead": "A solution of sodium hydroxide (NaOH) is prepared by dissolving 6 g solid NaOH in 500 cm³ water.\n\nThis solution reacts "
             "completely with 10 g impure ammonium chloride (NH₄Cℓ) according to the equation below.\n"
             "NaOH(aq) + NH₄Cℓ(s) → NaCℓ(aq) + H₂O(ℓ) + NH₃(aq)", "items": q8b},
    {"id": "9", "title": "Question 9", "kind": "Redox reactions", "marks": 13,
     "lead": "The reaction between dichromate ions (" + CR + ") and iron(II) ions (Fe²⁺) in an acidic medium is given below.\n"
             + CR + "(aq) + Fe²⁺(aq) + H⁺(aq) → Cr³⁺(aq) + Fe³⁺(aq) + H₂O(ℓ)", "items": q9},
    {"id": "10", "title": "Question 10", "kind": "Mining gold and iron", "marks": 10,
     "lead": "Gold and iron are two of many minerals mined in South Africa. Iron is mined in open-cast mines, while gold is usually found in "
             "deep-shaft (underground) mines. During the process of refining, the following chemical reactions take place to extract the "
             "metal from the ore:\n\nGold is dissolved in a solution containing cyanide ions (CN⁻) to extract it from the ore. The balanced "
             "chemical equation for the reaction is:\n4Au(s) + 8NaCN(aq) + 2H₂O(ℓ) + O₂(g) → 4NaAu(CN)₂(aq) + NaOH(aq)\n\nIron(VI) oxide "
             "and carbon are heated in a furnace to extract iron from the ore. The balanced chemical equation for the reaction is:\n"
             "2Fe₂O₃(s) + 3C(s) → 4Fe(ℓ) + 3CO₂(g)", "items": q10},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Grade 12 Physical Sciences P2 2025 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, another term's definition, the opposite choice, the reversed reasoning):
# never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns `each`;
# the cards are shuffled the same way every run. The rubric bullets above stay as the source. Where the memo's OR reading restates a
# point of its first reading, only the first reading is cards (one point twice can never earn two marks).
# Card order: the seeded shuffle (PID:n). Where it puts a single right card first, or every right card on top, the pilots added wrong
# cards until it moved (2.6 and 10.1: one more wrong card each), and a single right card that lands first at EVERY count from 5 to 8
# takes a second wording (2.1). 9.3's two right cards (the formula and its reason) land on top at every count from 5 to 8, and a second
# wording of either would let one point earn two marks, so 9.3 draws the shuffle again with a numbered seed (PID:n:1), as
# transcribe_g10_ps_p2_2017_11.py does; REDRAWN records it.
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
    # a single right card first, or every right card on top, would be an answer by position
    assert pool != list(range(len(pool))), (n, "the right cards on top: an answer by position", pool)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count}


STATEMENTS = {
    # 2: the wrong ones are the ionic bond, an intermolecular force, protons shared, the metallic bond, the bond energy. The memo's one
    # statement landed first at every card count (5 to 8: the seeded shuffle), so it is a card in two wordings (the memo's, and "two
    # atoms share electrons"), a pick of ONE, and the wrong ionic bond is in two wordings too, so a pair of cards that say the same thing
    # never marks the right one
    "2.1": (2, ["A covalent bond is the sharing of electrons between two atoms to form a molecule.",
                "A covalent bond forms when two atoms share electrons, making a molecule."],
               ["A covalent bond is the transfer of electrons from one atom to another to form ions.",
                "A covalent bond forms when one atom gives electrons to another atom, making ions.",
                "A covalent bond is the attraction between separate molecules of a substance.",
                "A covalent bond is the sharing of protons between two atoms.",
                "A covalent bond is the attraction between positive metal ions and a sea of delocalised electrons.",
                "A covalent bond is the energy needed to break one mole of bonds."]),
    # 1, either of the memo's OR forms: the wrong ones reverse the symmetry or the electronegativities, deny the stem's same shape,
    # or put the polar bonds in the wrong molecule (5 wrong cards: with four the two right cards came first)
    "2.6": (1, ["The charge distribution in CH₃Cℓ is asymmetrical, and in CH₄ it is symmetrical.",
                "Chlorine has a higher electronegativity than hydrogen."],
               ["The charge distribution in CH₄ is asymmetrical, and in CH₃Cℓ it is symmetrical.",
                "Hydrogen has a higher electronegativity than chlorine.", "CH₃Cℓ has a different shape from CH₄.",
                "CH₄ has polar bonds, but CH₃Cℓ has only non-polar bonds.", "Carbon has a higher electronegativity than chlorine."]),
    # 3 ticks: the memo's three points
    "3.1": (1, ["Both water and ethanol have hydrogen bonds.", "The hydrogen bonds in water and in ethanol are the same in relative strength.",
                "Substances with comparable relative strength in intermolecular forces will dissolve."],
               ["Ethanol molecules have only London forces between them.", "Water molecules have only London forces between them.",
                "Substances with very different strengths of intermolecular forces dissolve in each other.",
                "Ethanol dissolves in water because ethanol is an ionic compound."]),
    # 3 ticks: one form of each "/" (London forces; molecular mass; bigger molecules)
    "3.2": (1, ["The intermolecular forces in iodine and in bromine are both London forces.",
                "Iodine molecules have a bigger molecular mass than bromine molecules.",
                "The bigger the molecules, the stronger the intermolecular forces."],
               ["Iodine has hydrogen bonds between its molecules.", "Bromine molecules have a bigger molecular mass than iodine molecules.",
                "The bigger the molecules, the weaker the intermolecular forces.",
                "Iodine boils at a higher temperature because the bond between its two atoms is stronger than the bond in bromine."]),
    # 4 ticks: one form of each "/" (dipole-dipole forces; weaker forces evaporate faster)
    "3.3": (1, ["The intermolecular forces between phosphine molecules are dipole-dipole forces.",
                "The intermolecular forces between ammonia molecules are hydrogen bonds.", "The dipole-dipole forces are weaker than the hydrogen bonds.",
                "Weaker forces will cause the molecules to evaporate faster."],
               ["The intermolecular forces between phosphine molecules are hydrogen bonds.",
                "The intermolecular forces between ammonia molecules are London forces only.",
                "The dipole-dipole forces are stronger than the hydrogen bonds.", "Stronger forces will cause the molecules to evaporate faster."]),
    # 2 ticks: the memo's first reading (its OR reading, water and ethanol have the higher boiling points and stronger forces, turns the
    # same points round: no cards)
    "3.5": (1, ["The boiling point of bromine is lower than that of the other two liquids, so bromine has weaker intermolecular forces.",
                "If the intermolecular forces are weaker, the vapour pressure will be higher."],
               ["The boiling point of bromine is higher than that of the other two liquids.",
                "If the intermolecular forces are weaker, the vapour pressure will be lower.",
                "Bromine has hydrogen bonds, the strongest intermolecular forces of the three.",
                "The vapour pressure of a liquid does not depend on its intermolecular forces."]),
    # 2 in one statement (a tick each for the relationship and the condition), either of the memo's forms: the wrong ones make it inverse,
    # swap in the volume, reverse the trend, deny any relationship
    "4.2": (2, ["The pressure of an enclosed gas is directly proportional to the temperature, if the volume stays constant.",
                "As the pressure of an enclosed gas increases, the temperature increases proportionately."],
               ["The pressure of an enclosed gas is inversely proportional to the temperature, if the volume stays constant.",
                "The pressure of an enclosed gas is directly proportional to its volume, if the temperature stays constant.",
                "As the temperature of an enclosed gas increases, its pressure decreases.",
                "The pressure of an enclosed gas does not depend on its temperature."]),
    # 2 in one statement: the wrong ones speed the molecules up, remove the forces or the molecules' volume, blow up the pressure
    "4.3": (2, ["At very low temperatures the gas will liquefy and no longer act like a gas."],
               ["At very low temperatures the gas molecules move faster.", "At very low temperatures the intermolecular forces disappear.",
                "At very low temperatures the pressure of the gas becomes very large.",
                "At very low temperatures the gas molecules take up no space at all."]),
    # 4 ticks: the memo's four points
    "4.4": (1, ["If the temperature increases, the average kinetic energy of the particles increases.", "The particles move faster.",
                "The number of collisions between the particles (and the force per unit area) increases.",
                "If the number of collisions increases, the pressure increases."],
               ["If the temperature increases, the average kinetic energy of the particles decreases.", "The particles move slower.",
                "The particles become larger when they are heated.", "If the number of collisions increases, the pressure decreases."]),
    # 2 ticks: the two conditions; the wrong ones are their opposites and two conditions that bring the molecules close together
    "4.5": (1, ["High temperature", "Low pressure"],
               ["Low temperature", "High pressure", "A temperature just above the boiling point of the gas",
                "A small volume, with the molecules close together"]),
    # 2 in one statement: the wrong ones raise the activation energy, change the yield or ΔH, use the catalyst up, lower the products
    "6.1.2": (2, ["The catalyst lowers the activation energy of the reaction."],
                 ["The catalyst raises the activation energy of the reaction.", "The catalyst increases the final volume of oxygen formed.",
                  "The catalyst changes the heat of reaction (ΔH).", "The catalyst is used up during the reaction.",
                  "The catalyst lowers the energy of the products."]),
    # 2 ticks: the choice (magnesium) and one form of its "/" reason (after 3 minutes)
    "6.2.1": (1, ["Magnesium is the limiting agent.", "The mass of magnesium after 3 minutes is zero."],
                 ["Hydrochloric acid is the limiting agent.", "Magnesium chloride is the limiting agent.",
                  "The mass of magnesium stays the same during the reaction.", "Some magnesium is left over when the reaction stops."]),
    # 2 or 0: the wrong ones are the maximum, ΔH, the products' energy, the average kinetic energy
    "7.1": (2, ["The minimum energy needed for a reaction to take place."],
               ["The maximum energy released during a reaction.", "The energy difference between the products and the reactants.",
                "The energy of the products of a reaction.", "The average kinetic energy of the particles of the reactants."]),
    # 2 ticks: the choice and its reason (the memo's two OR forms in one card, so the two forms can never earn two marks)
    "7.2": (1, ["The reaction is exothermic.", "It releases energy (ΔH < 0)."],
               ["The reaction is endothermic.", "It absorbs energy (ΔH > 0).", "The products have more energy than the reactants.",
                "It needs no activation energy to start."]),
    # 2: the wrong ones are a proton donor, an electron acceptor, releasing H⁺, an acid's colour change
    "8.1.1": (2, ["A base is a proton acceptor."],
                 ["A base is a proton donor.", "A base is an electron acceptor.", "A base is a substance that releases H⁺ ions in water.",
                  "A base is a substance that turns blue litmus paper red."]),
    # 2 pairs, 2 marks each: the wrong pairs join two acids, two bases, the two reactants, the two products
    "8.1.5": (2, ["HSO₄⁻ and H₂SO₄", "H₂O and H₃O⁺"],
                 ["H₂SO₄ and H₃O⁺", "H₂O and HSO₄⁻", "H₂SO₄ and H₂O", "HSO₄⁻ and H₃O⁺"]),
    # 2 (the paper's; the memo prints (1)): the wrong ones are oxidation, protons, oxygen, oxidation numbers, sharing
    "9.2": (2, ["Reduction is a gain of electrons."],
               ["Reduction is a loss of electrons.", "Reduction is a gain of protons.", "Reduction is a gain of oxygen.",
                "Reduction is an increase in oxidation number.", "Reduction is the sharing of electrons between two atoms."]),
    # 2 ticks: the formula and the change of oxidation number
    "9.3": (1, ["Fe²⁺ undergoes oxidation.", "The oxidation number of Fe increases from +2 to +3."],
               ["Cr₂O₇²⁻ undergoes oxidation.", "H⁺ undergoes oxidation.", "The oxidation number of Fe decreases from +3 to +2.",
                "The oxidation number of H increases from +1 to +2."]),
    # 2, the memo's two (it accepts any relevant answer: no other true advantage is a card); the wrong ones are clearly false (5 wrong
    # cards: with four the two right cards came first)
    "10.1": (1, ["Miners do not have to risk their lives going deep underground or being trapped underground.", "There is no risk of sinkholes."],
                ["Open-cast mining leaves the land surface undisturbed.",
                 "Open-cast mining can reach ore much deeper underground than deep-shaft mining.", "Open-cast mining produces no dust or noise.",
                 "Open-cast mining needs no machinery.", "Open-cast mining has no effect on nearby rivers and groundwater."]),
    # 2 ticks: the choice and the change, with iron's oxidation number in Fe₂O₃ (+3; the memo's 6+ follows the paper's misprinted
    # "Iron(VI) oxide" and is in no card, so it is never a wrong card)
    "10.2": (1, ["Iron is reduced.", "The oxidation number of iron decreases from +3 (in Fe₂O₃) to 0 (in Fe)."],
                ["Iron is oxidised.", "The oxidation number of iron increases from 0 to +3.", "Iron gains oxygen in the reaction.",
                 "The oxidation number of carbon decreases from 0 to −4."]),
    # 2, the memo's two (it accepts any relevant answer: no other true disadvantage is a card); the wrong ones are clearly false
    "10.3": (1, ["Carbon is a non-renewable resource.", "The carbon dioxide produced can increase global warming."],
                ["Carbon is a renewable resource that is never used up.", "The reaction produces oxygen gas, which pollutes the air.",
                 "The carbon dioxide produced reduces global warming.", "Carbon cannot react with iron oxide at any temperature."]),
    # 2 in one statement: the wrong ones make gold reactive, a good reducing agent, or a non-metal
    "10.4": (2, ["Gold does not oxidise easily, unlike iron."],
                ["Gold oxidises more easily than iron.", "Gold reacts readily with oxygen and water in the rock.", "Gold atoms lose electrons very easily.",
                 "Gold is a non-metal, so it cannot form compounds.", "Gold is a strong reducing agent."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (10.1 asks for
# advantages only, 10.3 for disadvantages only), so SORTS stays empty and sort_ is kept for parity.
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
assert REDRAWN == {"9.3": 1}, REDRAWN   # only 9.3 draws its shuffle again (see the card-order note above STATEMENTS)

assert tuple(AUTHORED) == ("4.6", "4.7", "5.1", "5.2", "6.1.3", "6.2.2", "7.4", "8.2.1", "8.2.2", "9.6"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
nums = [i["n"] for i in ITEMS]
assert len(set(nums)) == len(nums), "a part number twice"
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["2.3"], "one count read off the Lewis structure"
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["2.4", "2.5.1", "2.5.2", "8.1.3", "8.1.4", "9.4", "10.5"]
assert [i["n"] for i in ITEMS if i.get("strict")] == ["2.4", "8.1.3", "8.1.4", "9.4"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.2.1", "2.2.2", "4.1", "7.3"]
for i in ITEMS:   # a built plot (build-play.js "plot"): one test per memo criterion, its marks the part's; every value inside the grid at every
    b = i.get("build") or {}   # scale the memo accepts (a tap snaps to a small square: always within half a small square of the value)
    if b.get("kind") == "plot":
        assert len(b["tests"]) == len(i["criteria"]) and sum(c["marks"] for c in i["criteria"]) == i["marks"], i["n"]
        assert all(set(t.get("ids", [])) <= {p["id"] for p in b["points"]} for t in b["tests"]), i["n"]
        for k, ax, n in ((0, b["x"], b["grid"]["nx"]), (1, b["y"], b["grid"]["ny"])):
            assert set(ax["ok"]) <= set(ax["scales"]) and all(0 <= p["at"][k] <= min(ax["ok"]) * n for p in b["points"]), (i["n"], k)
            assert all(p["at"][k] * 2 > max(ax["ok"]) * n for p in b["points"][-1:]), (i["n"], k, "an accepted scale uses under half the grid")
assert all(nums.index(e) < nums.index(i["n"]) for i in ITEMS for e in i.get("after", [])), "a gate on a later part"
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]
assert PICKS == ["2.1", "2.6", "3.1", "3.2", "3.3", "3.5", "4.2", "4.3", "4.4", "4.5", "6.1.2", "6.2.1", "7.1", "7.2", "8.1.1", "8.1.5",
                 "9.2", "9.3", "10.1", "10.2", "10.3", "10.4"], PICKS
EQUATIONS = ["6.1.1", "8.1.2", "9.5"]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2017", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Chemistry", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic chemistry errors (a unit not converted, a formula "
                                                       "upside down, a mole ratio or a molar mass wrong, the wrong constant, a value from the wrong "
                                                       "row, the two states swapped), 0 or full marks: " + ", ".join(AUTHORED) +
                                                       " (%d parts, %d marks). 9.6 ('using the ion-electron method') plays as the memo's "
                                                       "half-reactions and net ionic equation. A value the memo also accepts is never a wrong "
                                                       "option: 4.6's 'any combination of coordinates from the graph' (every point of the line "
                                                       "gives 0,62), 4.7's 20,1 dm³, 6.1.3's OPTION 2 (1,67 g), 8.2.1's OPTION 2 (0,3 mol·dm⁻³), "
                                                       "8.2.2's OR (19,75%%). 7.4: the memo writes 82,76 / 12 = 6,896 (truncated); the right "
                                                       "option shows 6,897 (the ratio 1 : 2,5 and C₂H₅ stand either way). The right letters of the "
                                                       "ten workings sit at A2 B3 C2 D3 (as even as ten allow)." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "9.2", "kind": "memo_issue", "detail": "The memo (page 11) marks 9.2 '(1)' with one tick ('Gain of electrons'); the question paper "
                                                     "(page 10) prints (2) and the memo's own Question 9 total [13] needs 2 (its parts as printed "
                                                     "add to 11). Played at the paper's 2 marks: one card, 2 or 0."},
        {"n": "9.5", "kind": "memo_issue", "detail": "The memo (page 11) marks 9.5 '(1)' with no tick; the question paper (page 11) prints (2) "
                                                     "and the memo's Question 9 total [13] needs 2. Played at the paper's 2 marks, the equation "
                                                     "all or nothing."},
        {"n": "10.2", "kind": "memo_issue", "detail": "The memo (page 11) answers 'oxidation number of iron decreases from 6+ to 0', following "
                                                      "the question paper's 'Iron(VI) oxide' (page 11); in Fe₂O₃ iron is +3 (iron(III) oxide). "
                                                      "The right card shows +3 to 0; the memo's 6+ earns the mark too (Murci's ruling "
                                                      "2026-10-10) and is in no card, so it is never a wrong card."},
        {"n": "10", "kind": "memo_issue", "detail": "The question paper (page 11) names Fe₂O₃ 'Iron(VI) oxide' (iron(III) oxide is meant) and "
                                                    "prints the gold equation as 4Au + 8NaCN + 2H₂O + O₂ → 4NaAu(CN)₂ + NaOH, called balanced "
                                                    "(4NaOH balances it). Both kept as printed; 10.2's right card gives iron's +3 from the "
                                                    "formula, and no part depends on the NaOH coefficient."},
        {"n": "7", "kind": "memo_issue", "detail": "The question paper (page 9) prints butane(g) + 13O₂(g) → 8CO₂(g) + 10H₂O(g): with butane "
                                                   "C₄H₁₀ it balances only as 2C₄H₁₀ (the formula is hidden because 7.4 asks for it). Kept as "
                                                   "printed; 7.4 works from the percentages only."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions (2.1, 7.1, 8.1.1, 9.2) and "
                                                    "the memo's single 2-mark statements (4.2 the conclusion, 4.3, 6.1.2, 10.4) pick one card "
                                                    "for their 2 marks (4.2's OR form a second right card); 2.6 picks one card for 1 mark (its "
                                                    "two OR forms both right); the explanations (3.1, 3.2, 3.3, 3.5, 4.4), the two conditions "
                                                    "of 4.5, the two advantages (10.1) and disadvantages (10.3), and the choices with their "
                                                    "reasons (6.2.1, 7.2, 9.3, 10.2) pick the memo's points, 1 mark each; 8.1.5 picks the two "
                                                    "conjugate pairs, 2 marks each. Where the memo's OR reading restates its first (3.5), only "
                                                    "the first reading is cards; 7.2's two OR forms of the reason (releases energy, ΔH < 0) are "
                                                    "one card, so they can never earn two marks. 10.1 and 10.3 accept any relevant answer: only "
                                                    "the memo's two are right cards, and no other true point is a card. Card order: 2.1's one "
                                                    "memo statement landed first at every card count of the seeded shuffle, so it is a card in "
                                                    "two wordings (a pick of ONE: no extra mark) beside the wrong ionic bond in two wordings; "
                                                    "9.3's two right cards landed on top at every count and a second wording would let one point "
                                                    "earn two marks, so its shuffle is drawn again with a numbered seed (PID:9.3:1)." % len(PICKS)},
        {"n": EQUATIONS[0], "kind": "no_fit", "detail": "'Balance the equation' (6.1.1), 'Write down a balanced equation' (8.1.2, the memo's "
                                                        "reactants, products and balance marks) and the half-reaction (9.5) play as multiple "
                                                        "choice of four equations, all or nothing: the memo's equation and three wrong ones "
                                                        "(unbalanced; a formula changed to balance it; the reverse reaction; electrons on the "
                                                        "wrong side; Cr unbalanced). 9.1 (an oxidation number, no working) plays as an answer "
                                                        "multiple choice; 3.4 (one of the three printed liquids) as multiple choice of the three; "
                                                        "2.3 (a count read off the Lewis structure) as a number."},
        {"n": "2.2.1", "kind": "no_fit", "detail": "Drawings (2.2.1 and 2.2.2 the Lewis structures, 7.3 the "
                                                   "potential energy sketch) are done on paper and self-checked against the memo's criteria."},
        {"n": "4.1", "kind": "no_fit", "detail": "The graph of pressure versus temperature is BUILT on the answer sheet's grid (2026-10-11, build "
                                                 "'plot'): 11 big squares across and 7 up, its axes printed and labelled, no numbers: the learner "
                                                 "chooses each axis' scale (20 / 25 / 50 / 100 a big square: only 50 K and 50 kPa hold the table and "
                                                 "use over half the grid), places the five points, draws a straight line of best fit and extends it "
                                                 "to the y-axis ('drawn to the origin': within 7,5 kPa of 0 there)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 10), hand-transcribed from the paper and memo PDFs and "
                                                           "their page images (the 1.3 curve and table, the 1.4 fractions, the 6.1, 6.2 and Q8 "
                                                           "figures, the memo's Lewis structures, sketch and workings are images); no API call. "
                                                           "The paper writes the dichromate charge as Cr₂O₇⁻² (here Cr₂O₇²⁻, as the memo and the "
                                                           "data sheet write it), proportionality as 'α' (here ∝), and prints 1.6 without its (2) "
                                                           "(the memo and the [20] give 2)."},
    ],
}
QTOTAL = {"1": 20, "2": 11, "3": 13, "4": 22, "5": 8, "6": 19, "7": 11, "8": 23, "9": 13, "10": 10}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's ten printed letters are the paper's (A3 B1 C4 D2) and 3.4's printed choice is C, so the authored
# four-option questions lean towards A, B and D: the 10 workings sit at A2 B3 C2 D3, the four answer / equation MCQs at A1 B2 D1, the 24
# four-option questions at A6 B6 C6 D6 and the whole paper at A6 B6 C7 D6
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 3, spread
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(wspread.values()) - min(wspread.values()) <= 1 and min(wspread.values()) >= 2, wspread   # ten workings: as even as possible
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, the paper:", spread, "authored:", wspread, "four-option:", fspread)
print("statement right-card positions:", {i["n"]: (i["pool"], len(i["opts"])) for i in ITEMS if i["t"] == "pickn"})
total = sum(i["marks"] for i in ITEMS)
assert total == 150 == paper["paper"]["total_marks"], total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; statements:", len(PICKS), "parts")
print("total:", total)
# GATES (the last check): a part whose stem, options, cards or criteria show an earlier part's answer opens only after it
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "3.5": ["3.4"], "4.2": ["4.1"], "4.7": ["4.6"], "6.1.3": ["6.1.1"], "6.2.2": ["6.2.1"], "7.3": ["7.2"], "8.1.5": ["8.1.4"], "9.5": ["9.4"],
    "9.6": ["9.3", "9.4", "9.5"]}, {i["n"]: i.get("after") for i in ITEMS if i.get("after")}
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
