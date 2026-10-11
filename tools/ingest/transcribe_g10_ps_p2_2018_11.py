"""Grade 10 Physical Sciences P2 (Chemistry) Nov 2018 (DBE common paper), the whole paper as the memo marks it (Questions 1 to 10,
without 1.4 and 8.4, which the memo voids), hand-transcribed into the catalogue format (as if Claude had produced it), then run
through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the memo's working are the paper's and
the memo's own (its English); clues and figure captions are ours. No API call: the transcription is the source, kept in git (out/ is
not). Read from the page IMAGES too: the paper sets the 1.4 equations, the AZX notation and the Q2 / Q6 particle diagrams as images.

  python tools/ingest/transcribe_g10_ps_p2_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Physical Sciences P2 Nov 2018 Eng.pdf" "uploads/Grade 10 Physical Sciences P2 Nov 2018 MG Eng & Afr.pdf" --id g10-ps-p2-2018-11 --from-json

The memo's cover: "NOTE: Ignore 1.4 and Question 8.4 molecular formula not in CAPS. MARKS: 141" (its final total; the question
paper's cover prints 150). 1.4 has no correct option as printed (C writes Mg⁺(g) + energy → Mg²⁺ + 2e⁻) and 8.4 is outside the
Grade 10 curriculum, so both are left out and the paper totals the memo's 141 (flagged).

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; models: transcribe_ps_p2_2025_11.py, Chemistry, and the Grade 10
pilot transcribe_g10_ps_p1_2018_11.py):
  multiple choice printed in the paper -> mcq as printed; a choice printed in the stem with no explanation in the same part (2.3
  ELEMENT or COMPOUND, 3.4 INCREASES / DECREASES / REMAINS THE SAME, 9.2.1 CARBONATE or SULPHATE) and a "Write down the LETTER" (2.2,
  3.2.2, 3.2.3, 4.2.2, 5.2, 6.1) -> mcq of the printed choices; 10.3 (ENERGY GAINED or ENERGY LOST for each of A and B, 1 mark each)
  -> a classify (match with groups), the memo's mark per process. One term the memo names -> term; an IUPAC-style formula (4.3.1 Rb2O)
  -> strict term. Two symbols play as answer multiple choice, not typed: 4.2.1's AZX notation (superscript over subscript cannot be
  typed) and 4.2.3's S²⁻ (the term check drops signs, so S2+ would earn the memo's charge mark). One read-off value with no working ->
  num (3.2.1, 6.4.3).
  Every calculation -> authored multiple choice, `work`: the memo's FIRST working line by line and three workings each built from a
  DIFFERENT realistic chemistry error (a mole ratio wrong, a formula upside down, a wrong molar mass, cm³ not converted, the wrong
  volume or sample, percentages misapplied), every number recomputed; 0 or full marks. A value the memo also accepts (its ranges) is
  never a wrong option. "Write down a BALANCED CHEMICAL EQUATION" (5.5.2, 7.2, 9.2.2) -> multiple choice of four equations, the
  memo's marks all or nothing; no memo-accepted form is a wrong option.
  A definition or law -> statements (pick 1 card for its marks; an OR form a second right card); an explanation or a choice with its
  reasons -> statements, the memo's marks per point. No memo here weighs two sides, so no part plays as a sort.
  Drawings (4.5 the Aufbau diagram, 6.4.4 the Lewis diagram) -> draw with the memo's criteria, self-checked (flagged no_fit).
  A part whose options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose lead or diagram changes part-way is several missions (7 and 7.3; 9, 9.2 and 9.3).
Figure boxes are measured in PDF points (page 595.32 x 841.92, read from the PDF) from the drawings, images and labels themselves and
checked on a contact sheet of the 1%-padded crops (scratchpad lower/g10-ps-p2-2018-11/figs.py)."""
import json
import random
import re
from pathlib import Path

PID = "g10-ps-p2-2018-11"
W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "Q2": [6, 47.8, 137.2, 522.4, 431.8], "Q3": [7, 69.8, 127.2, 518.2, 473.0], "Q6": [10, 110.6, 162.5, 459.4, 315.7],
    "Q9a": [13, 188.5, 154.0, 418.3, 314.0], "Q9b": [13, 232.0, 420.7, 392.0, 521.8], "Q10": [14, 87.8, 171.0, 497.6, 266.0]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


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
EQ = "\n\nChoose the correct equation."   # a "Write down a BALANCED CHEMICAL EQUATION" played as multiple choice of four
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


def classify(n, q, marks, left, right, a, clues, heads, **kw):
    """Each item into one of a few groups (a match with groups): one mark per item, as the memo marks it."""
    assert marks == len(left) == len(a) and all(0 <= k < len(right) for k in a), n
    return {"t": "match", "n": n, "marks": marks, "q": q, "clues": clues, "left": left, "right": right, "a": a, "heads": heads,
            "groups": True, **kw}


CHANGE = ["Increases", "Decreases", "Remains the same"]
LIQ = ["A", "B", "C", "D"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-5 and the memo page 2 (1.4 left out: the memo voids it) ----
q1 = [
    mcq("1.1", "Which ONE of the following substances is NOT a pure substance?", ["Iron", "Sugar", "Steel", "Graphite"], 2,
        ["What is the difference between a pure substance and a mixture?", "Which of the four are elements, and which is a compound?"]),
    mcq("1.2", "The CORRECT chemical formula for potassium nitrate is …", ["K₃N", "PNO₃", "KNO₃", "K₂NO₃"], 2,
        ["Which element has the symbol K, and which has the symbol P?", "What are the charges on a potassium ion and on a nitrate ion?"]),
    mcq("1.3", "Different isotopes of the same element have different …",
        ["atomic numbers.", "numbers of neutrons.", "numbers of protons.", "numbers of electrons."], 1,
        ["What do all the atoms of one element have in common?", "Which particles make up the mass number of an atom?"]),
    mcq("1.5", "Which PAIR of elements is most likely to have a similar arrangement of outer electrons and similar chemical behaviour?",
        ["Boron and aluminium", "Helium and fluorine", "Carbon and nitrogen", "Chlorine and oxygen"], 0,
        ["Which feature of an element's atoms decides how the element reacts?",
         "Find each pair in the periodic table: are the two elements in the same group or in the same period?"]),
    mcq("1.6", "Which ONE of the following statements is INCORRECT about the properties of a physical change?",
        ["When a physical change occurs, the compounds may rearrange themselves, but the bonds in between the atoms will not break.",
         "Physical change in matter is reversible.", "Energy is absorbed when matter changes from a solid to a liquid.",
         "Molecules are not conserved during a physical change."], 3,
        ["Are new substances formed during a physical change?", "When ice melts, are any water molecules broken up or made?"]),
    mcq("1.7", "In the compound, H₂O, the ratio of the MASS of hydrogen to oxygen is always …", ["1 : 2.", "2 : 1.", "1 : 8.", "1 : 16."], 2,
        ["What are the relative atomic masses of hydrogen and oxygen?", "How many hydrogen atoms are there for each oxygen atom in H₂O?"]),
    mcq("1.8", "One mole of H₂SO₄ contains …", ["7 atoms.", "1 molecule.", "6,02×10²³ molecules.", "42,14×10²³ molecules."], 2,
        ["What does one mole of any substance always contain the same number of?",
         "Is the number of molecules in a mole of H₂SO₄ the same as the number of atoms in it?"]),
    mcq("1.9", "Which ONE of the following solutions will NOT form a precipitate if added to a solution of silver nitrate?",
        ["NaCl(aq)", "MgBr₂(aq)", "KI(aq)", "Mg(NO₃)₂(aq)"], 3,
        ["Which ion besides the metal ion does each solution contain?", "Which silver salts are insoluble in water?"]),
    mcq("1.10", "The sphere in which minerals are found is known as …", ["atmosphere.", "biosphere.", "lithosphere.", "stratosphere."], 2,
        ["Where on Earth are minerals mined from?", "Which sphere holds the living things, and which the layer of air around the Earth?"]),
]

# ---- QUESTION 2, the question paper page 6 and the memo page 2 ----
LET = "Write down a LETTER that represents "
PROP = "Write down the physical property upon which the separation techniques are based to separate "
q2 = [
    rub("2.1", "Define the term element.", 2, ["A pure substance consisting of one type of atom. (2)"],
        ["Think of copper, oxygen and carbon: what do they have in common?",
         "Can an element be broken down into simpler substances by a chemical reaction?"], each=2),
    mcq("2.2.1", LET + "a pure substance.", ["P", "Q", "R"], 0,
        ["Is a pure substance made of one kind of particle, or of several kinds?", "Use the key to name the particles in each box."], marks=1),
    mcq("2.2.2", LET + "a homogeneous mixture.", ["P", "Q", "R"], 1,
        ["What is the difference between a homogeneous and a heterogeneous mixture?", "Which boxes contain more than one substance?"], marks=1),
    mcq("2.2.3", LET + "a heterogeneous mixture.", ["P", "Q", "R"], 2,
        ["In a heterogeneous mixture, can you see the different parts?", "Use the key: which substances make up each box?"], marks=1),
    mcq("2.3", "Indicate whether the pure substance identified in QUESTION 2.2.1 is an element or a compound.", ["Element", "Compound"], 0,
        ["Use the key: what are the particles in the box you chose in 2.2.1?",
         "Does a compound contain one kind of atom, or two or more kinds bonded together?"], marks=1),
    term("2.4", "Which physical method would you use to separate substance Q into its components?", ["Evaporation"],
         ["Use the key: which substances make up Q?", "Which of these substances can be turned into a gas by heating, leaving the other behind?"]),
    term("2.5.1", PROP + "substance Q into its individual components.", [
        "Boiling point", "Boiling points", "Difference in boiling points", "Difference in boiling point"],
         ["What property of each substance in Q does the method you named in 2.4 depend on?",
          "Which substance in Q leaves the mixture first when it is heated, and why?"]),
    term("2.5.2", PROP + "substance R into its individual components.", ["Magnetism", "Magnetic properties", "Magnetic property", "Magnetic"],
         ["Use the key: which substances make up R?", "Which property of one of these substances lets you pull it out of the mixture?"]),
]

# ---- QUESTION 3, the question paper page 7 and the memo page 3 ----
q3 = [
    rub("3.1", "Define the term boiling point.", 2, ["The temperature of the liquid at which the vapour pressure equals the external (atmospheric) "
                                                     "pressure. (2)"],
        ["Is the boiling point a temperature, a pressure or an energy?",
         "What happens to the vapour pressure of a liquid as it is heated, until bubbles of vapour form?"], each=2),
    num("3.2.1", "Write down the boiling point of liquid B.", 80, 0, "°C",
        ["At what vapour pressure does a liquid boil when the atmospheric pressure is 101,3 kPa?",
         "Where does curve B cross that pressure, and which temperature is below that point?"]),
    mcq("3.2.2", "Write down the liquid which remains a liquid at 115 °C.", LIQ, 3,
        ["A liquid stays a liquid below its boiling point: how do you read each liquid's boiling point from the graph?",
         "Find 115 °C on the temperature axis: which curves have not yet reached 101,3 kPa there?"], marks=1),
    mcq("3.2.3", "Write down the liquid that is most likely to be water.", LIQ, 2,
        ["What is the boiling point of water at standard atmospheric pressure?", "Which curve crosses 101,3 kPa at that temperature?"], marks=1),
    term("3.3", "State the PHASE CHANGE that takes place at the stage when the vapour pressure is equal to atmospheric pressure.", [
        "Liquid changes to gas", "Liquid to gas", "Liquid changes to vapour", "Liquid to vapour", "Boiling", "Vaporisation", "Vaporization"],
         ["What name is given to the temperature at which the vapour pressure equals the atmospheric pressure?",
          "What happens to the particles of the liquid at that temperature?"]),
    mcq("3.4", "What happens to the temperature of a liquid during a phase change? Write down only INCREASES, DECREASES or REMAINS THE SAME.",
        CHANGE, 2, ["What does the temperature of a substance measure about its particles?",
                    "Where does the energy supplied during a phase change go?"], marks=1),
    rub("3.5", "Explain the answer to QUESTION 3.4.", 2, [
        "Energy is used to overcome the intermolecular forces. (1)", "No energy available to increase the kinetic energy of the particles. (1)"],
        ["What is the energy supplied during a phase change used for?", "Which quantity of the particles does the temperature measure?"],
        after=["3.4"]),   # its cards: no energy goes to the kinetic energy (the temperature stays the same)
    rub("3.6", "Which liquid (A, B, C or D) has the weakest intermolecular forces? Give a reason for the answer.", 3, [
        "A. (1)", "Lowest boiling point. (2)", "OR — Highest vapour pressure at a specific temperature. (2)"],
        ["How are the boiling point and the strength of the intermolecular forces related?",
         "How do you read the boiling point of each liquid from the graph?"]),
    rub("3.7", "What is the relationship between vapour pressure of the liquid and temperature?", 2, [
        "Vapour pressure increases with an increase in temperature. (2)", "OR — Vapour pressure is proportional to temperature. (2)"],
        ["Which quantity is on each axis of the graph?",
         "Pick one curve: how does its vapour pressure at 25 °C compare with its vapour pressure at 75 °C?"], each=2),
]

# ---- QUESTION 4, the question paper page 8 and the memo pages 4-5 ----
P43 = "Element P reacts with oxygen to form the compound with the chemical formula P₂O. "
q4 = [
    rub("4.1", "Define the term atomic number.", 2, ["The number of protons in an atom of an element. (2)"],
        ["Look up sodium in the periodic table: what is its atomic number, and how many electrons does a sodium atom have?",
         "Is the atomic number the same as the mass number?"], each=2),
    # the memo: ³⁰₁₄Si (2); ²⁸₁₄Si earns 1 (the element right), A and Z swapped no mark for them: an answer multiple choice of four
    # (the notation cannot be typed), ²⁸₁₄Si never an option. Wrong: A and Z swapped, the neutrons as A, the neutrons as Z (sulphur)
    mcq("4.2.1", "Write down the chemical symbol of element Q using the notation AZX (A written at the top and Z at the bottom, before the "
        "symbol X).", ["³⁰₁₆S", "³⁰₁₄Si", "¹⁴₃₀Si", "¹⁶₁₄Si"], 1,
        ["How do you find the mass number from the numbers of protons and neutrons?",
         "In the notation, which number is written at the top and which at the bottom?"]),
    mcq("4.2.2", "Write down the element (P, Q or R) that is an alkali metal.", ["P", "Q", "R"], 0,
        ["In which group of the periodic table are the alkali metals?", "Use the number of protons to find each element in the periodic table."],
        marks=1),
    # the memo: S²⁻ (the element 1, the charge 1; a wrong element 0/2). Multiple choice, not a term: a term reads "S2-" through its digit
    # only, so "S2+" would earn the charge mark. Wrong: the charge's sign, no charge, the element from the 18 electrons (argon)
    mcq("4.2.3", "Write down the chemical symbol of R.", ["S²⁺", "Ar", "S", "S²⁻"], 3,
        ["How do you identify an element from the table?",
         "Compare the numbers of protons and electrons of R: is it an atom or an ion, and what is its charge?"]),
    term("4.3.1", P43 + "Predict the chemical formula that element Rb in the periodic table will form when it reacts with oxygen.", ["Rb2O"],
         ["In which group of the periodic table is Rb, and in which is P?", "What does the formula P₂O tell you about the valency of P?"],
         marks=2, strict=True),
    rub("4.3.2", P43 + "Explain the answer to QUESTION 4.3.1.", 2, [
        "Rb is in the same group as P / Na OR Rb is in group 1. (1)", "∴ has the same valency as P / Na. (1)"],
        ["How many electrons do P and Rb have in their outer energy levels?", "How is the valency of an element related to its outer electrons?"],
        after=["4.2.2", "4.3.1"]),   # its cards: Rb, a group 1 element, is in P's group (4.2.2) with P's valency (4.3.1's Rb₂O)
    rub("4.4", "What is the trend in ionisation energy as you move from element P to element R? Write down only INCREASES, DECREASES or "
        "REMAINS THE SAME. Explain the answer.", 4, [
        "Increases. (1)", "From P to R, the atomic radius gets smaller OR the outer electrons get closer to the nucleus. (1)",
        "The attraction between the nucleus and the outer electron gets stronger. (1)", "∴ More energy is needed to remove the electrons. (1)"],
        ["What happens to the number of protons in the nucleus as you move from P to R across the period?",
         "How does the size of an atom affect how strongly its nucleus holds the outer electrons?"]),
    draw("4.5", "How many electrons does an ION of element P have? Draw the Aufbau diagram of this ion.", 3, [
        ["10 electrons", 1], ["2p: three boxes, each with a pair of arrows (↑↓)", 1], ["1s and 2s: one box each, each with a pair of arrows (↑↓)", 1]],
        ["Does an atom of P lose or gain electrons when it forms an ion, and how many?", "In which order are the 1s, 2s and 2p orbitals filled?"],
        memo="10 (electrons): 1s ↑↓, 2s ↑↓, 2p ↑↓ ↑↓ ↑↓, drawn as boxes, the energy increasing upwards."),
    term("4.6", "When orbitals of identical energy are available, electrons are placed in individual orbitals before they are paired. Give the "
         "name of this rule.", ["Hund's rule", "Hunds rule", "Hund rule"],
         ["Which rules for placing electrons in orbitals do you know (the Aufbau principle is one)?",
          "Which of these rules is about orbitals of the SAME energy, such as the three 2p orbitals?"]),
    # the memo (28,11 u; no range): the wrong workings are a plain average, the percentages paired with the wrong isotopes, ÷ 3
    work("4.7", "Element Y occurs as these isotopes in the following proportions:\nY – 28(92,23%); Y – 29(4,68%); Y – 30(3,09%)\n"
         "Calculate the relative atomic mass of element Y.", 3, [
        "Aᵣ = {28 + 29 + 30}/{3}\n= 29,00",                                                        # a plain average of the mass numbers
        "Aᵣ = {28 × 92,23 + 29 × 4,68 + 30 × 3,09}/{100}\n= 28,11",                               # the memo
        "Aᵣ = {28 × 3,09 + 29 × 4,68 + 30 × 92,23}/{100}\n= 29,89",                               # the percentages on the wrong isotopes
        "Aᵣ = {28 × 92,23 + 29 × 4,68 + 30 × 3,09}/{3}\n= 936,95"], 1,                            # divided by the 3 isotopes, not 100
        ["What does each percentage tell you about how common each isotope is?", "How do you find a weighted average of the three mass numbers?"]),
]

# ---- QUESTION 5, the question paper page 9 and the memo pages 5-6 ----
PZ = "For process Z, write down "
P56 = "A 20 g sample of CaCO₃(s) in process Y decomposes to form 11,2 g of CaO. In a second sample, 30 g decomposes to form x g of CO₂. "
q5 = [
    rub("5.1", "Define the term physical change.", 2, [
        "A change in which no new substances are formed. (2)", "OR — A change in which energy changes are small in relation to chemical changes. (2)",
        "OR — A change in which mass, number of atoms and molecules are being conserved. (2)"],
        ["Think of ice melting: what stays the same, and what changes?", "How does a physical change differ from a chemical change?"], each=2),
    mcq("5.2.1", "Write down the LETTER of the process that represents a physical change.", ["X", "Y", "Z"], 0,
        ["Which processes form new substances, and which does not?", "Compare the formulas on the two sides of each arrow."], marks=1),
    mcq("5.2.2", "Write down the LETTER of the process that represents a decomposition reaction.", ["X", "Y", "Z"], 1,
        ["How many reactants and how many products does a decomposition reaction have?", "Count the reactants and the products in each process."],
        marks=1),
    term("5.3", "Give the name of the physical change stated in QUESTION 5.2.1.", ["Sublimation"],
         ["Which process in the list changes only the phase of a substance, and from which phase to which?", "Which phase does that change skip?"]),
    rub("5.4", "State TWO properties of a reaction that indicate that a chemical change has taken place.", 2, [
        "ANY TWO: colour change; formation of gas; formation of a precipitate; change in temperature. (1 each)"],
        ["What new things can you see, feel or measure when a chemical reaction takes place?",
         "What do you see when an antacid tablet is dropped into water?"]),
    term("5.5.1", PZ + "what the symbol Δ represents.", ["Heat", "Heating", "Heat energy"],
         ["Where is the symbol Δ written in the processes?", "What does a symbol written under or over a reaction arrow describe?"]),
    # a balanced equation as multiple choice (the memo: reactants, products, phases, balancing: 4 marks, all or nothing): the memo's
    # equation and three wrong ones, unbalanced, oxygen as single atoms, iron(II) oxide formed
    mcq("5.5.2", PZ + "a BALANCED CHEMICAL EQUATION (Show the phases of ALL reactants and products.)" + EQ, [
        "4Fe(s) + 3O₂(g) → 2Fe₂O₃(s)", "Fe(s) + O₂(g) → Fe₂O₃(s)", "2Fe(s) + 3O(g) → Fe₂O₃(s)", "2Fe(s) + O₂(g) → 2FeO(s)"], 0,
        ["What is the formula of iron(III) oxide: what are the charges on an Fe³⁺ ion and on an oxide ion?",
         "Is oxygen gas made of single atoms or of molecules?"], marks=4),
    rub("5.6.1", P56 + "State the law of constant composition.", 2, [
        "No matter how a chemical compound is prepared, it always contains the same elements in the same proportion by mass. (2)"],
        ["Does pure water from a river and pure water made in a laboratory contain the same elements?",
         "Is the law about the masses of the reactants and products, or about the composition of one compound?"], each=2),
    # the memo's Option 1 (13,2 g; all three options end at 13,2 g, no range): every wrong working ends elsewhere
    work("5.6.2", P56 + "Use the law in QUESTION 5.6.1 to calculate mass x of the CO₂ formed.", 4, [
        "m(CO₂) in the 1st sample = 20 + 11,2\n= 31,2 g\nProportion of CO₂ in the 1st sample = {31,2}/{20}\n"
        "m(CO₂) in the 2nd sample = {31,2}/{20} × 30\n= 46,8 g",                                    # the masses added, not subtracted
        "m(CO₂) in the 1st sample = 20 − 11,2\n= 8,8 g\nProportion of CO₂ in the 1st sample = {20}/{8,8}\n"
        "m(CO₂) in the 2nd sample = {20}/{8,8} × 30\n= 68,18 g",                                   # the proportion upside down
        "m(CO₂) in the 1st sample = 20 − 11,2\n= 8,8 g\nProportion of CO₂ in the 1st sample = {8,8}/{30}\n"
        "m(CO₂) in the 2nd sample = {8,8}/{30} × 20\n= 5,87 g",                                    # the two samples' masses swapped
        "m(CO₂) in the 1st sample = 20 − 11,2\n= 8,8 g\nProportion of CO₂ in the 1st sample = {8,8}/{20}\n"
        "m(CO₂) in the 2nd sample = {8,8}/{20} × 30\n= 13,2 g"], 3,                                # the memo
        ["How much CO₂ formed from the first 20 g sample?",
         "What fraction of the CaCO₃'s mass is CO₂, and does that fraction change for a 30 g sample?"]),
]

# ---- QUESTION 6, the question paper page 10 and the memo page 6 ----
P64 = "Magnesium and chlorine react to form compound magnesium chloride. "
q6 = [
    mcq("6.1.1", "Choose the substance (A or B) that describes a metallic structure.", ["A", "B"], 0,
        ["What particles make up a metal?", "Look at the signs and labels in each box: what particles do they show?"], marks=1),
    mcq("6.1.2", "Choose the substance (A or B) that describes the structure of magnesium chloride.", ["A", "B"], 1,
        ["Is magnesium chloride made of a metal and a non-metal?", "What kind of particles do a metal and a non-metal form when they react?"],
        marks=1),
    rub("6.2", "Explain how the type of bond in substance A forms.", 2, [
        "It is formed when a pool of delocalised electrons (1) surround the positive metal ion core (1)."],
        ["What particles do the circles marked + in substance A stand for?", "What holds these particles together in a metal?"],
        after=["6.1.1"]),   # its cards: metal ions in a pool of electrons (A is the metallic structure)
    term("6.3", "Name the type of bond that exists in substance B.", ["Ionic bond", "Ionic", "Ionic bonding", "Ionic bonds"],
         ["What particles do the + and − circles in substance B stand for?", "Is the bond formed by sharing electrons or by transferring them?"]),
    rub("6.4.1", P64 + "Define the term compound.", 2, ["A pure substance consisting of two or more different elements. (2)"],
        ["Think of water, H₂O: how is it different from hydrogen gas?", "Can a compound be separated into its elements by a physical method?"],
        each=2),
    term("6.4.2", P64 + "Write down the NAME of the group to which magnesium belongs.", [
        "Alkali earth metals", "Alkali earth", "Alkaline earth metals", "Alkaline earth"],   # the memo's "Alkali earth (metals)"; the usual name
         ["In which group of the periodic table is magnesium?", "What do beryllium, calcium and magnesium have in common in the periodic table?"]),
    num("6.4.3", P64 + "Write down the valency of a chlorine atom.", 1, 0, "",
        ["How many valence electrons does a chlorine atom have?", "What does the valency of an atom tell you about the bonds it forms?"]),
    draw("6.4.4", P64 + "Use the Lewis dot diagram to show the formation of magnesium chloride.", 3, [
        ["Lewis diagram of magnesium: Mg with its two valence electrons", 1],
        ["Lewis diagrams of two chlorine atoms, each Cl with its seven valence electrons", 1],
        ["The products: Mg²⁺ and two Cl⁻ ions in square brackets, each Cl⁻ with eight electrons (MgCl₂)", 1]],
        ["How many valence electrons do magnesium and chlorine atoms have?", "How many chlorine atoms does one magnesium atom need to give its electrons to?"],
        memo="Mg with two dots + 2 Cl, each with seven crosses → Mg²⁺ + 2[Cl with eight electrons]⁻ → MgCl₂.",
        after=["6.1.2", "6.3", "6.4.3"]),   # its criteria: MgCl₂ made of ions (6.1.2, 6.3), each Cl gains one electron (6.4.3)
]

# ---- QUESTION 7, the question paper page 11 and the memo page 7 ----
q7a = [
    rub("7.1", "Explain the meaning of the term hydrated.", 1, ["Hydrated: surrounded by water molecules. (1)"],
        ["What does the '·xH₂O' part of the formula Na₂CO₃·xH₂O show?", "Are the water particles part of the crystal or a separate liquid?"]),
    # a balanced equation as multiple choice (the memo: products, balancing: 2 marks, all or nothing): unbalanced, the carbonate's
    # charge wrong, the carbonate ion broken up
    mcq("7.2", "Write down a BALANCED CHEMICAL EQUATION to show how sodium carbonate dissociates in water." + EQ, [
        "Na₂CO₃(s) → Na⁺(aq) + CO₃²⁻(aq)", "Na₂CO₃(s) → 2Na⁺(aq) + CO₃⁻(aq)", "Na₂CO₃(s) → 2Na⁺(aq) + C⁴⁺(aq) + 3O²⁻(aq)",
        "Na₂CO₃(s) → 2Na⁺(aq) + CO₃²⁻(aq)"], 3,
        ["Which ions does sodium carbonate contain, and what are their charges?", "Is the carbonate ion broken up when sodium carbonate dissolves?"]),
]
q7b = [
    rub("7.3.1", "Define the term a mole of a substance.", 2, [
        "The amount of a substance having the same number of particles as there are atoms in 12 g carbon-12. (2)"],
        ["What is Avogadro's number, and what does it count?", "Which reference substance is used to define the mole?"], each=2),
    term("7.3.2", "What type of chemical reaction is represented by the chemical equation above?", [
        "Acid-base", "Acid-base reaction", "Gas forming", "Gas-forming reaction", "Neutralisation", "Neutralisation reaction", "Neutralization"],
         ["What kind of substance is HCl?", "What gas is given off, and what kind of substance is sodium carbonate in this reaction?"]),
    # the memo (0,005 mol; no range): cm³ not converted, the 10 cm³ of the carbonate solution, c = nV
    work("7.3.3", "Calculate the number of moles of hydrochloric acid in 5 cm³ of hydrochloric acid if its concentration is 1 mol·dm⁻³.", 3, [
        "c = {n}/{V}\n1 = {n}/{0,005}\nn = 0,005 mol",                                              # the memo
        "c = {n}/{V}\n1 = {n}/{5}\nn = 5 mol",                                                      # 5 cm³ not converted to dm³
        "c = {n}/{V}\n1 = {n}/{0,01}\nn = 0,01 mol",                                                # the 10 cm³ of carbonate solution
        "c = nV\n1 = n(0,005)\nn = 200 mol"], 0,                                                     # the formula as c = nV
        ["Which formula links concentration, number of moles and volume?", "In which unit must the volume be?"]),
    # the memo (0,29 g; positive marking from 7.3.3): the 1 : 2 ratio, n = M/m, the molar mass of HCl
    work("7.4", "Calculate the mass of sodium chloride formed in the reaction in QUESTION 7.3.", 5, [
        "n(NaCl) : n(HCl) = 1 : 2\nn(NaCl) = {1}/{2} × 0,005\n= 0,0025 mol\nn(NaCl) = {m}/{M}\n0,0025 = {m}/{58,5}\nm = 0,15 g",   # 1 : 2
        "n(NaCl) : n(HCl) = 1 : 1\nn(NaCl) = {1}/{1} × 0,005\n= 0,005 mol\nn(NaCl) = {M}/{m}\n0,005 = {58,5}/{m}\nm = 11 700 g",   # upside down
        "n(NaCl) : n(HCl) = 1 : 1\nn(NaCl) = {1}/{1} × 0,005\n= 0,005 mol\nn(NaCl) = {m}/{M}\n0,005 = {m}/{58,5}\nm = 0,29 g",     # the memo
        "n(NaCl) : n(HCl) = 1 : 1\nn(NaCl) = {1}/{1} × 0,005\n= 0,005 mol\nn(NaCl) = {m}/{M}\n0,005 = {m}/{36,5}\nm = 0,18 g"], 2, # M(HCl)
        ["Use the balanced equation: how many moles of NaCl form for each mole of HCl?",
         "Which formula links the number of moles, the mass and the molar mass?"],
        after=["7.3.3"]),   # the options show 7.3.3's 0,005 mol
]

# ---- QUESTION 8, the question paper page 12 and the memo pages 7-8 (8.4 left out: the memo voids it) ----
P83 = "For the investigation, predict with reasons the substance that will yield "
q8 = [
    rub("8.1", "Define the term electrolyte.", 2, ["A solution that conducts electricity (through the movement of ions). (2)"],
        ["Think of table salt, NaCl: what happens to it when it dissolves in water?", "Which particles carry the charge through a solution?"],
        each=2, notes=["If learners refer to movement of electrons, a mark is forfeited."]),
    rub("8.2.1", "For the investigation, write down the investigative question.", 2, [
        "What is the relationship between a type of substance and its (electrical) conductivity? (2)",
        "OR — How does a type of substance affect the (electrical) conductivity of a substance? (2)"],
        ["Which variable did the learners change, and which did they measure?", "How would you ask about the relationship between those two variables?"],
        each=2, notes=["Criteria: dependent and independent variable correctly stated (1); a question about the relationship between them (1)."]),
    term("8.2.2", "For the investigation, write down the dependent variable.", ["Conductivity", "Electrical conductivity", "The conductivity"],
         ["Which quantity did the learners measure in each experiment?", "Is it the cause or the effect?"]),
    term("8.2.3", "For the investigation, write down the independent variable.", [
        "Type of a substance", "Type of substance", "The type of substance", "Substance type"],
         ["Which quantity did the learners choose to change from one experiment to the next?", "Is it the cause or the effect?"]),
    term("8.2.4", "For the investigation, write down the controlled variable.", [
        "Mass", "Temperature", "Mass of substance", "Mass of the substance", "The temperature"],
         ["Why must some quantities be kept the same in a fair test?", "Read the table: which columns show the same value in every experiment?"]),
    rub("8.3.1", P83 + "the highest conductivity.", 2, [
        "A solution of CaCl₂. (1)", "It is the strongest electrolyte OR it has the highest concentration of (chloride) ions. (1)"],
        ["Which solutions contain ions, and which contain only molecules?", "What carries the charge through a solution?"]),
    rub("8.3.2", P83 + "zero conductivity.", 2, ["A solution of sugar. (1)", "It contains no free ions. (1)"],
        ["Which kind of particles must a solution contain to conduct electricity?", "Which of the three substances is a covalent molecular compound?"]),
]

# ---- QUESTION 9, the question paper page 13 and the memo page 9 ----
Q9_LEAD = ("Two test tubes, A and B, both contain a sodium salt solution. After a small amount of barium chloride is added, the solution in "
           "both test tubes forms a white precipitate.")
q9a = [
    term("9.1", "Write down the type of reaction that takes place in the test tubes.", ["Precipitation reaction", "Precipitation"],
         ["What forms in both test tubes when the barium chloride is added?", "What name is given to a reaction named after the solid it forms?"]),
]
q9b = [
    mcq("9.2.1", "Identify which IONS (CARBONATE or SULPHATE) are present in test tube B.", ["Carbonate", "Sulphate"], 1,
        ["What are the two possible white precipitates that barium chloride forms here?", "Which of them reacts with an acid, and what would you see?"],
        marks=1),
    # a balanced equation as multiple choice (the memo: reactants, products, balancing: 3 marks, all or nothing): unbalanced, the
    # sulphate precipitate, the sodium salt instead of the precipitate
    mcq("9.2.2", "Write down a BALANCED CHEMICAL EQUATION that represents the reaction between nitric acid and the precipitate formed in test "
        "tube A." + EQ, ["BaCO₃ + HNO₃ → Ba(NO₃)₂ + CO₂ + H₂O", "BaCO₃ + 2HNO₃ → Ba(NO₃)₂ + CO₂ + H₂O", "BaSO₄ + 2HNO₃ → Ba(NO₃)₂ + H₂SO₄",
                    "Na₂CO₃ + 2HNO₃ → 2NaNO₃ + CO₂ + H₂O"], 1,
        ["What is the precipitate in test tube A?", "Which three products form when an acid reacts with a carbonate?"], marks=3,
        after=["9.2.1"]),   # its options: the carbonate precipitate in A (so B holds the sulphate)
]
q9c = [
    # the memo (9,26 g, range 9,25 - 9,87 g): every wrong working ends outside it
    work("9.3.1", "Calculate the mass of barium carbonate that should form in this reaction.", 5, [
        "n(Na₂CO₃) = {m}/{M} = {5}/{83}\n= 0,060 mol\nn(BaCO₃) : n(Na₂CO₃) = 1 : 1\nm(BaCO₃) = nM = (0,060)(197)\n= 11,82 g",     # one Na in M
        "n(Na₂CO₃) = {m}/{M} = {5}/{106}\n= 0,047 mol\nn(BaCO₃) : n(Na₂CO₃) = 1 : 2\nm(BaCO₃) = nM = (0,0235)(197)\n= 4,63 g",  # 1 : 2
        "n(Na₂CO₃) = {M}/{m} = {106}/{5}\n= 21,2 mol\nn(BaCO₃) : n(Na₂CO₃) = 1 : 1\nm(BaCO₃) = nM = (21,2)(197)\n= 4 176,4 g",   # upside down
        "n(Na₂CO₃) = {m}/{M} = {5}/{106}\n= 0,047 mol\nn(BaCO₃) : n(Na₂CO₃) = 1 : 1\nm(BaCO₃) = nM = (0,047)(197)\n= 9,26 g"], 3,  # the memo
        ["Which formula gives the number of moles from a mass?", "Use the balanced equation: how many moles of BaCO₃ form from one mole of Na₂CO₃?"]),
    # the memo (89,63%, range 84,26 - 89,64%; positive marking from 9.3.1): every wrong working ends outside it
    work("9.3.2", "It was found that only 8,3 g precipitate formed. Calculate the percentage yield.", 2, [
        "% yield = {actual yield}/{theoretical yield} × 100\n= {8,3}/{9,26} × 100\n= 89,63%",                        # the memo
        "% yield = {theoretical yield}/{actual yield} × 100\n= {9,26}/{8,3} × 100\n= 111,57%",                       # upside down
        "% yield = {theoretical yield − actual yield}/{theoretical yield} × 100\n= {9,26 − 8,3}/{9,26} × 100\n= 10,37%",   # the loss
        "% yield = {actual yield}/{theoretical yield} × 100\n= {8,3}/{5} × 100\n= 166%"], 0,                         # the 5 g as the yield
        ["Which mass is the theoretical yield, and which the actual yield?", "Which formula gives the percentage yield?"],
        after=["9.3.1"]),   # the options show 9.3.1's 9,26 g
]

# ---- QUESTION 10, the question paper page 14 and the memo page 10 ----
q10 = [
    rub("10.1", "Differentiate between the hydrosphere and biosphere.", 2, [
        "Hydrosphere: includes all water of the earth found as liquid water. (1)", "Biosphere: includes all the living organisms. (1)"],
        ["In the diagram, which boxes belong to the hydrosphere and which to the biosphere?", "What does each sphere contain that the other does not?"]),
    term("10.2.1", "Write down the name of process A.", ["Transpiration"],
         ["Through which parts of a plant does water vapour escape into the air?", "Is process A the same as evaporation from a lake, or special to plants?"]),
    term("10.2.2", "Write down the name of process B.", ["Condensation"],
         ["What happens to water vapour when it cools high up in the air?", "Does process B change a gas into a liquid, or a liquid into a gas?"]),
    term("10.2.3", "Write down the name of process C.", ["Precipitation"],
         ["How does water get from the clouds back to the ground and the plants?",
          "What happens to the water droplets in a cloud when they become too heavy?"]),
    classify("10.3", "Describe the energy changes during processes A and B. Write down only ENERGY GAINED or ENERGY LOST.", 2,
             ["Process A", "Process B"], ["Energy gained", "Energy lost"], [0, 1],
             ["In processes A and B, which phase changes into which?", "Is energy needed to pull particles apart, or released when they come together?"],
             ["PROCESS", "ENERGY CHANGE"]),
    rub("10.4", "Describe the interaction between the hydrosphere and plants.", 4, [
        "Roots of plants absorb water from the ground. (1)", "Plants release the water to the atmosphere by transpiration. (1)",
        "The water condenses to form clouds. (1)", "Then water falls back to the ground by precipitation. (1)"],
        ["Through which part of a plant does water enter, and through which does it leave?",
         "What happens to the water at each arrow of the diagram, from PLANTS round to PLANTS again?"],
        after=["10.2.1", "10.2.2", "10.2.3"]),   # its cards name transpiration, condensation and precipitation
]

PQR_TABLE = {"head": ["ELEMENT/ION", "NUMBER OF PROTONS", "NUMBER OF NEUTRONS", "NUMBER OF ELECTRONS"],
             "rows": [["P", "11", "12", "11"], ["Q", "14", "16", "14"], ["R", "16", "16", "18"]]}
EXP_TABLE = {"head": ["EXPERIMENT", "MASS OF SUBSTANCE (g)", "TYPE OF SUBSTANCE", "TEMPERATURE (°C)"],
             "rows": [["1", "2", "Solution of CaCl₂", "25"], ["2", "2", "Solution of KCl", "25"], ["3", "2", "Solution of sugar", "25"]]}
Q7_LEAD = ("A group of learners prepare a 0,25 mol·dm⁻³ solution of sodium carbonate by dissolving a 14,2 g sample of hydrated sodium "
           "carbonate (Na₂CO₃·xH₂O) in 200 cm³ of water.")
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 18,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Classification of matter", "marks": 9,
     "lead": "The diagram below shows three different substances, P, Q and R.\n\nUse the diagram and the key provided to answer the questions "
             "that follow.",
     "figure": fig("Q2", "A table of three boxes of particles drawn as circles, P, Q and R, above a key. P: five pairs of small white circles, the "
                   "two circles of each pair joined. Q: three circles with vertical lines, each joined to a large dotted circle, and three black "
                   "circles, each joined to two small white circles. R: separate large circles, some with a grid and some with diagonal lines. "
                   "Key: hydrogen, a small white circle; oxygen, a black circle; sodium, a circle with vertical lines; chlorine, a large dotted "
                   "circle; sulphur, a circle with a grid; iron, a circle with diagonal lines."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Vapour pressure", "marks": 14,
     "lead": "The vapour pressure versus temperature graph below was obtained for four unknown liquids (A, B, C and D). Atmospheric pressure is "
             "measured as 101,3 kPa.",
     "figure": fig("Q3", "Vapour pressure versus temperature: vapour pressure (kPa), 0 to 200, up against temperature (°C), 0 to 125, across, on "
                   "a fine grid; four curves labelled A, B, C and D, and a dashed horizontal line marked 101,3 kPa."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Atomic structure", "marks": 22, "lead": "Study the table below and answer the questions that follow.",
     "table": PQR_TABLE, "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Physical and chemical change", "marks": 18,
     "lead": "Study the physical and chemical processes below and answer the questions that follow.\nX: H₂O(s) → H₂O(g)\n"
             "Y: CaCO₃(s) → CaO(s) + CO₂(g), with Δ written under the arrow\nZ: Iron + Oxygen → Iron(III) oxide", "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Chemical bonding", "marks": 12,
     "lead": "Study the diagram below showing structures of two different substances (A and B) and answer the questions that follow.",
     "figure": fig("Q6", "Two boxes. Substance A: three rows of five circles, each marked +, with an e⁻ beside each circle. Substance B: large "
                   "circles marked − packed together, with small circles marked + in the gaps between them."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Sodium carbonate solution", "marks": 3, "lead": Q7_LEAD, "items": q7a},
    {"id": "7.3", "title": "Question 7.3", "kind": "Moles and reacting masses", "marks": 11,
     "lead": Q7_LEAD + "\n\nLearners then take 10 cm³ of the prepared solution and allow it to react completely with 5 cm³ of dilute hydrochloric "
             "acid, according the following balanced chemical equation:\nNa₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂", "items": q7b},
    {"id": "8", "title": "Question 8", "kind": "Investigating solutions", "marks": 11,
     "lead": "Learners investigate how the type of substance affects electrical conductivity of the substance. They conduct three experiments "
             "using three different substances under the same conditions, as shown in the table below.", "table": EXP_TABLE, "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Testing a sodium salt", "marks": 1, "lead": Q9_LEAD,
     "figure": fig("Q9a", "Barium chloride solution dropped from two droppers into test tubes A and B, each holding a solution."), "items": q9a},
    {"id": "9.2", "title": "Question 9.2", "kind": "Testing for anions", "marks": 4,
     "lead": Q9_LEAD + "\n\nA concentrated nitric acid solution is then added into each test tube to establish which one contains carbonate ions "
             "and which one contains sulphate ions.\n\nBubbles are formed in test tube A. There is no reaction in test tube B.",
     "figure": fig("Q9b", "Test tubes A and B after the nitric acid is added: bubbles in the liquid of test tube A, none in test tube B."),
     "items": q9b},
    {"id": "9.3", "title": "Question 9.3", "kind": "Reacting masses and yield", "marks": 7,
     "lead": "A solution of sodium carbonate was prepared by dissolving 5 g of the powder in 100 cm³ of water. The solution reacted with a barium "
             "chloride solution, according to the following balanced chemical equation:\nNa₂CO₃(aq) + BaCl₂(aq) → BaCO₃(s) + 2NaCl(aq)",
     "items": q9c},
    {"id": "10", "title": "Question 10", "kind": "Hydrosphere and biosphere", "marks": 11,
     "lead": "The diagram below shows how the hydrosphere is linked to the biosphere. Study the diagram and answer the questions that follow.",
     "figure": fig("Q10", "Three boxes in a cycle: PLANTS, an arrow labelled A to Water vapour, an arrow labelled B to CLOUDS, and a wide arrow "
                   "labelled C from CLOUDS back to PLANTS."), "items": q10},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Grade 12 Physical Sciences P2 2025 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, another term's definition, the opposite choice, the reversed reasoning):
# never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns `each`;
# the cards are shuffled the same way every run. The rubric bullets above stay as the source. Where the memo gives ONE mark for
# "A / B" forms of a point, one form is a card: two right cards for one mark would let two picks earn two marks. No wrong card is
# another part's right answer word for word (2.1's element / 6.4.1's compound; 5.1 leaves out its third OR form, molecules conserved,
# which is 1.6's answer).


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random(PID + ":" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    pool = sorted(k for k, i in enumerate(order) if i < len(right))
    assert pool != list(range(len(pool))), (n, "the right card first, or every right card on top: an answer by position", pool)
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count}


STATEMENTS = {
    # 2: the wrong ones are a mixture, a molecule, isotopes denied, a diatomic rule, a physical breakdown
    "2.1": (2, ["A pure substance consisting of one type of atom."],
               ["A mixture of two or more substances that are not chemically bonded.", "The smallest particle of a substance that can exist on its own.",
                "A pure substance whose atoms all have the same number of neutrons.", "A pure substance that always consists of molecules made of two atoms.",
                "A substance that can be broken down into simpler substances by physical methods."]),
    # 2: the wrong ones are a zero or half vapour pressure, the melting point, the vapour pressure itself
    "3.1": (2, ["The temperature of the liquid at which the vapour pressure equals the external (atmospheric) pressure."],
               ["The temperature of the liquid at which the vapour pressure is zero.", "The temperature at which a solid changes into a liquid.",
                "The temperature of the liquid at which the vapour pressure is half the external (atmospheric) pressure.",
                "The pressure of the vapour above a liquid in a closed container.", "The temperature at which a liquid changes into a solid.",
                "The temperature at which the particles of a liquid stop moving.", "The amount of energy needed to change a liquid into a gas."]),
    # (7 wrong cards: with four to six the right card came first)
    # 2 ticks: the memo's two points
    "3.5": (1, ["Energy is used to overcome the intermolecular forces.", "No energy is available to increase the kinetic energy of the particles."],
               ["Energy is used to increase the kinetic energy of the particles.", "Energy is used to break the bonds between the atoms inside the molecules.",
                "The intermolecular forces become stronger during the phase change.", "No energy is absorbed during a phase change."]),
    # 3 ticks, the memo's 1 + 2 (the choice; the reason, either OR form): played as 1 + 1 + 1, the choice and BOTH OR forms of the reason
    # as cards (the pick has one mark a card; together the two forms earn the reason's 2)
    "3.6": (1, ["Liquid A has the weakest intermolecular forces.", "Liquid A has the lowest boiling point.",
                "Liquid A has the highest vapour pressure at a specific temperature."],
               ["Liquid D has the weakest intermolecular forces.", "Liquid A has the highest boiling point.",
                "Liquid A has the lowest vapour pressure at a specific temperature.", "Weaker intermolecular forces need more energy to overcome."]),
    # 2: the first form only. The memo's OR "vapour pressure is proportional to temperature" (Afrikaans: directly proportional) is not
    # what the graph shows (curves, not straight lines through the origin): neither a right nor a wrong card (flagged)
    "3.7": (2, ["Vapour pressure increases with an increase in temperature."],
               ["Vapour pressure decreases with an increase in temperature.", "Vapour pressure does not depend on the temperature.",
                "Vapour pressure first increases and then decreases as the temperature increases.",
                "Vapour pressure stays constant until the boiling point is reached."]),
    # 2: the wrong ones are the neutrons, the mass number, the valence electrons, a mass
    "4.1": (2, ["The number of protons in an atom of an element."],
               ["The number of neutrons in an atom of an element.", "The number of protons and neutrons in the nucleus of an atom.",
                "The number of electrons in the outer energy level of an atom.", "The mass of one atom of an element in grams."]),
    # 2 ticks: the group (its OR "group 1" one card with it) and the valency
    "4.3.2": (1, ["Rb is in the same group as P (group 1).", "Rb therefore has the same valency as P."],
                 ["Rb is in the same period as P.", "Rb is in group 2, so it has a valency of 2.",
                  "Rb has more electrons than P, so it forms more bonds with oxygen.", "Rb takes the valency of oxygen, which is 2."]),
    # 4 ticks: the choice and the memo's chain (its OR "the outer electrons get closer to the nucleus" one card with the radius)
    "4.4": (1, ["The ionisation energy increases.", "From P to R, the atomic radius gets smaller.",
                "The attraction between the nucleus and the outer electrons gets stronger.", "More energy is needed to remove the electrons."],
               ["The ionisation energy decreases.", "From P to R, the atomic radius gets larger.",
                "The attraction between the nucleus and the outer electrons gets weaker.", "Less energy is needed to remove the electrons."]),
    # 2, either of its first two OR forms (the third, "molecules are conserved", is 1.6's answer: no card)
    "5.1": (2, ["A change in which no new substances are formed.", "A change in which energy changes are small in relation to chemical changes."],
               ["A change in which new substances with new properties are formed.", "A change in which energy changes are large in relation to chemical changes.",
                "A change in which atoms of one element change into atoms of another element.",
                "A change in which the total mass of the substances decreases."]),
    # 2, any two of the memo's four: the wrong ones are physical changes
    "5.4": (1, ["Colour change.", "Formation of gas.", "Formation of a precipitate.", "Change in temperature."],
               ["Change in shape.", "Change of phase, such as melting.", "Dissolving of a solid in water.", "Cutting a substance into smaller pieces."]),
    # 2: the wrong ones are a varying proportion, conservation of mass, a mixture, equal masses
    "5.6.1": (2, ["No matter how a chemical compound is prepared, it always contains the same elements in the same proportion by mass."],
                 ["A chemical compound always contains the same elements, but their proportion by mass depends on how it is prepared.",
                  "In a chemical reaction, the total mass of the reactants equals the total mass of the products.",
                  "No matter how a mixture is prepared, it always contains the same substances in the same proportion by mass.",
                  "No matter how a chemical compound is prepared, it always contains equal masses of each of its elements."]),
    # 2 ticks: the pool of delocalised electrons and the positive metal ion cores it surrounds
    "6.2": (1, ["It is formed by a pool of delocalised electrons.", "The delocalised electrons surround the positive metal ion cores."],
               ["Electrons are transferred from one atom to another to form positive and negative ions.", "Two atoms share a pair of electrons between them.",
                "Each electron stays in a fixed position, bound to one atom.", "Positive metal ion cores surround a pool of negative ions."]),
    # 2: the wrong ones are a mixture of elements, a mixture of compounds, isotopes, dissolving into ions
    "6.4.1": (2, ["A pure substance consisting of two or more different elements."],
                 ["A mixture of two or more different elements that are not chemically bonded.",
                  "A substance consisting of two or more different compounds mixed together.",
                  "A substance consisting of two or more isotopes of the same element.", "Any substance that dissolves in water to form ions.",
                  "A substance whose elements can be separated from each other by filtration."]),   # (a 5th wrong card: with four the
                  # right card came first)
    # 1: the wrong ones are an acid, no water, hydrogen gas, a gas
    "7.1": (1, ["Hydrated means surrounded by water molecules."],
               ["Hydrated means dissolved in an acid.", "Hydrated means containing no water molecules.",
                "Hydrated means surrounded by hydrogen gas molecules.", "Hydrated means changed into a gas."]),
    # 2: the wrong ones are 1 g of carbon-12, one particle's mass, 12 g of water, one particle's volume
    "7.3.1": (2, ["The amount of a substance having the same number of particles as there are atoms in 12 g carbon-12."],
                 ["The amount of a substance having the same number of particles as there are atoms in 1 g carbon-12.",
                  "The mass of one particle of a substance.",
                  "The amount of a substance having the same number of particles as there are molecules in 12 g of water.",
                  "The volume occupied by one particle of a gas.", "The number of atoms in one molecule of a substance.",
                  "The amount of a substance that has a mass of exactly 1 g.", "The number of electrons in one atom of carbon-12."]),
    # (7 wrong cards: with four to six the right card came first)
    # 2: the wrong ones are a metal's electron conduction, no conduction, no ions, the anode
    "8.1": (2, ["A solution that conducts electricity through the movement of ions."],
               ["A metal that conducts electricity through the movement of free electrons.", "A solution that does not conduct electricity.",
                "A substance that dissolves in water without forming ions.", "The electrode at which oxidation takes place."]),
    # 2, either of the memo's questions: the wrong ones name a controlled variable, reverse cause and effect, or miss the dependent one
    "8.2.1": (2, ["What is the relationship between a type of substance and its (electrical) conductivity?",
                  "How does a type of substance affect the (electrical) conductivity of a substance?"],
                 ["What is the relationship between the temperature of a solution and its conductivity?",
                  "How does the conductivity of a solution affect the type of substance?",
                  "How does the mass of a substance affect its temperature?",
                  "What is the relationship between the mass of a substance and its conductivity?"]),
    # 2 ticks: the choice and ONE form of the reason (its OR "the strongest electrolyte" says the same: no card)
    "8.3.1": (1, ["The solution of CaCl₂.", "It has the highest concentration of chloride ions."],
                 ["The solution of KCl.", "The solution of sugar.", "It has the lowest concentration of ions.",
                  "It contains free electrons that carry the charge."]),
    # 2 ticks: the choice and the reason
    "8.3.2": (1, ["The solution of sugar.", "It contains no free ions."],
                 ["The solution of KCl.", "The solution of CaCl₂.", "It contains the most free ions.", "Its molecules break up into ions in water."]),
    # 2 ticks: one card for each sphere; the wrong ones swap them, or are the atmosphere and a plants-only biosphere
    "10.1": (1, ["The hydrosphere includes all the water of the earth, found as liquid water.", "The biosphere includes all the living organisms."],
                ["The hydrosphere includes all the living organisms.", "The biosphere includes all the water of the earth.",
                 "The hydrosphere is the layer of gases that surrounds the earth.", "The biosphere includes only the plants, and not the animals."]),
    # 4 ticks: the memo's four steps of the cycle
    "10.4": (1, ["The roots of plants absorb water from the ground.", "Plants release the water to the atmosphere by transpiration.",
                 "The water condenses to form clouds.", "The water then falls back to the ground by precipitation."],
                ["The leaves of plants absorb water vapour from the clouds.", "Plants release the water to the atmosphere by condensation.",
                 "The water vapour evaporates to form clouds.", "The water falls back to the ground by transpiration."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, laws, explanations and choices with reasons), so SORTS stays empty and sort_ is kept for parity.
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

assert tuple(AUTHORED) == ("4.7", "5.6.2", "7.3.3", "7.4", "9.3.1", "9.3.2"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
nums = [i["n"] for i in ITEMS]
assert len(set(nums)) == len(nums), "a part number twice"
assert "1.4" not in nums and "8.4" not in nums, "the memo voids 1.4 and 8.4"
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["3.2.1", "6.4.3"], "only the read-offs stay typed numbers"
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["2.4", "2.5.1", "2.5.2", "3.3", "4.3.1", "4.6", "5.3", "5.5.1", "6.3", "6.4.2", "7.3.2",
                                                        "8.2.2", "8.2.3", "8.2.4", "9.1", "10.2.1", "10.2.2", "10.2.3"]
assert [i["n"] for i in ITEMS if i.get("strict")] == ["4.3.1"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["4.5", "6.4.4"]
assert [i["n"] for i in ITEMS if i["t"] == "match"] == ["10.3"]
assert all(nums.index(e) < nums.index(i["n"]) for i in ITEMS for e in i.get("after", [])), "a gate on a later part"
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]
EQUATIONS = ["5.5.2", "7.2", "9.2.2"]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2018", "total_marks": 141, "time": "2 hours"},
    "sections": [{"title": "Chemistry", "total": 141, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "memo_issue", "detail": "The question paper's cover prints MARKS 150; the memo's cover notes 'Ignore 1.4 and Question "
                                                       "8.4 molecular formula not in CAPS. MARKS: 141' and its last page 'FINAL TOTAL: 141' "
                                                       "(Question 1 [18], Question 8 [11]). 1.4 and 8.4 are left out and the paper totals 141."},
        {"n": "1.4", "kind": "memo_issue", "detail": "'Which ONE of the following ionisation equations represents the second ionisation of "
                                                     "magnesium?' (question paper page 3): no option is correct as printed (C, the nearest, "
                                                     "writes Mg⁺(g) + energy → Mg²⁺ + 2e⁻; the second ionisation releases one electron). The "
                                                     "memo (page 2): 'Ignore this question'. Left out (2 marks)."},
        {"n": "8.4", "kind": "memo_issue", "detail": "'Determine the molecular formula if the molar mass is 180 g·mol⁻¹' (question paper page 12, "
                                                     "7 marks): the memo (page 8) works it to C₆H₁₂O₆ but marks it '[ignore this question]', the "
                                                     "molecular formula not being in the Grade 10 CAPS. Left out."},
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic chemistry errors (a mole ratio wrong, a formula "
                                                       "upside down, a wrong molar mass, cm³ not converted, the wrong volume or sample, the "
                                                       "percentages on the wrong isotopes, a plain average), 0 or full marks: " + ", ".join(AUTHORED)
                                                       + " (%d parts, %d marks). A value the memo accepts is never a wrong option: 9.3.1's range "
                                                       "9,25 - 9,87 g, 9.3.2's range 84,26 - 89,64%%." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions and laws (2.1, 3.1, 3.7, 4.1, "
                                                    "5.1, 5.6.1, 6.4.1, 7.1, 7.3.1, 8.1) and the investigative question (8.2.1) pick one card for "
                                                    "their marks (an OR form is a second right card); the explanations and the choices with "
                                                    "reasons (3.5, 4.3.2, 4.4, 6.2, 8.3.1, 8.3.2, 10.1, 10.4) pick the choice and the memo's "
                                                    "points, 1 mark each; 5.4 picks two of the memo's four. Where the memo gives one mark for "
                                                    "'A / B' forms of a point, one form is a card." % len(PICKS)},
        {"n": "3.6", "kind": "no_fit", "detail": "The memo marks 3.6 as 1 + 2 (A; 'Lowest boiling point' OR 'Highest vapour pressure at a specific "
                                                 "temperature' for 2). A pick has one mark a card, so it plays as 1 + 1 + 1: the choice and BOTH "
                                                 "OR forms of the reason are right cards, the two forms together earning the reason's 2."},
        {"n": "3.7", "kind": "memo_issue", "detail": "The memo's OR answer 'Vapour pressure is proportional to temperature' (Afrikaans: 'direk "
                                                     "eweredig', directly proportional) is not what the graph shows: the curves are not straight "
                                                     "lines through the origin. Only its first form is a card; the proportional form is neither a "
                                                     "right nor a wrong card."},
        {"n": "5.5.1", "kind": "memo_issue", "detail": "The paper asks 'For process Z, write down: 5.5.1 What the symbol Δ represents', but Δ is "
                                                       "printed under the arrow of process Y (CaCO₃ decomposing), not Z. Kept as printed; the "
                                                       "memo's answer is Heat."},
        {"n": "5.6.2", "kind": "memo_issue", "detail": "The memo's Option 3 writes x = 16,83 g CaO and 30 − 16,83 = 13,2 g; 30 × 11,2 / 20 = 16,8 g "
                                                       "and 30 − 16,8 = 13,2 g. The right option is its Option 1 (13,2 g)."},
        {"n": EQUATIONS[0], "kind": "no_fit", "detail": "'Write down a BALANCED CHEMICAL EQUATION' (5.5.2, 7.2, 9.2.2) plays as multiple choice of four "
                                                        "equations, the memo's marks all or nothing (reactants, products, phases, balancing): the "
                                                        "memo's equation and three wrong ones (unbalanced; a wrong reactant or product; a wrong ion "
                                                        "or formula). No form the memo accepts is a wrong option."},
        {"n": "4.2.1", "kind": "no_fit", "detail": "4.2.1 (the AZX notation, superscript over subscript, cannot be typed) and 4.2.3 (S²⁻: a term "
                                                   "reads a charge through its digit only, so S2+ would earn the memo's 'correct charge' mark) "
                                                   "play as answer multiple choice of four symbols, all or nothing. 4.2.1's options leave out "
                                                   "²⁸₁₄Si, which the memo credits 1 of 2. 4.3.1 (Rb2O) is a strict term."},
        {"n": "10.3", "kind": "no_fit", "detail": "ENERGY GAINED or ENERGY LOST for each of processes A and B (1 mark each) plays as a classify: "
                                                  "each process into one of the two groups."},
        {"n": "4.5", "kind": "no_fit", "detail": "Drawings (4.5 the number of electrons and the Aufbau diagram of P's ion, 6.4.4 the Lewis dot "
                                                 "diagram) are done on paper and self-checked against the memo's criteria."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper as the memo marks it (Questions 1 to 10 without 1.4 and 8.4), hand-"
                                                           "transcribed from the paper and memo PDFs and their page images (the 1.4 equations, "
                                                           "the AZX notation and the particle diagrams are images); no API call."},
    ],
}
QTOTAL = {"1": 18, "2": 9, "3": 14, "4": 22, "5": 18, "6": 12, "7": 14, "8": 11, "9": 12, "10": 11}   # the memo's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's nine printed letters are the paper's (A1 B1 C5 D2) and the printed letter / choice picks are fixed by
# their answers (2.2.x, 2.3, 3.2.x, 3.4, 4.2.2, 5.2.x, 6.1.x, 9.2.1), so the authored four-option questions (the six workings and the
# five answer / equation MCQs) lean away from C: the workings sit as even as six allow, the four-option questions within 3, the
# paper within 2
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 2, spread
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(wspread.values()) - min(wspread.values()) <= 1, wspread   # six workings: as even as possible
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, the paper:", spread, "authored workings:", wspread, "four-option:", fspread)
print("statement right-card positions:", {i["n"]: i["pool"] for i in ITEMS if i["t"] == "pickn"})
total = sum(i["marks"] for i in ITEMS)
assert total == 141 == paper["paper"]["total_marks"], total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; statements:", len(PICKS), "parts")
print("total:", total)
# GATES (the last check): a part whose stem, options, cards or criteria show an earlier part's answer opens only after it
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "3.5": ["3.4"], "4.3.2": ["4.2.2", "4.3.1"], "6.2": ["6.1.1"], "6.4.4": ["6.1.2", "6.3", "6.4.3"], "7.4": ["7.3.3"], "9.2.2": ["9.2.1"],
    "9.3.2": ["9.3.1"], "10.4": ["10.2.1", "10.2.2", "10.2.3"]}, "a gate dropped or changed"
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 as the memo marks them (1.4 and 8.4 voided)"}, "paper": paper},
                                              indent=1, ensure_ascii=False), encoding="utf-8")
