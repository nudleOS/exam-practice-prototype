"""Physical Sciences P2 (Chemistry) Nov 2024, the whole paper (Questions 1 to 9), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: structural formulas are drawings.
Polished one subject at a time (Murci, 2026-10-10: "next subject: Physical Sciences").

  python tools/ingest/transcribe_ps_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P2 Nov 2024 Eng.pdf" "<...>/Physical Sciences P2 Nov 2024 MG Afr & Eng.pdf" --id ps-p2-2024-11 --from-json

How the memo's shapes map (Chemistry, as P2 Nov 2025, with what the 2026-10-10 polish taught):
  an IUPAC name or a formula -> term with strict, the memo's part marks played all or nothing; "Write down the LETTER(S)" -> mcq /
  pickn; a choice the paper names -> mcq; a STRUCTURAL formula or an equation in structural formulae -> draw (self-checked); a
  balanced equation or a half-reaction -> rubric whose points carry each species as a phone types it (ASCII: 2Fe3, Pb2; the
  subscripts and charges of "Fe³⁺" normalise away) with the printed form in brackets, the labels ("Reactants") in brackets so they
  are not required words; a definition -> ONE point worth 2, its key-phrase note in `notes`; the memo's phrase-level "/" as OR
  wordings where a learner would write one alternative; "Calculate" -> steps on the memo's numbers; a memo range -> its centre and a
  tolerance covering it; "decide by calculation" (9.1) -> steps, the conclusion riding on the number.
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves (scratchpad figs24.py) and checked on a
contact sheet (sheet24.py)."""
import json
from pathlib import Path

W, H = 595.44, 841.68
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.4": [4, 175, 122, 505, 352], "1.9": [6, 150, 150, 450, 265], "1.10": [6, 215, 475, 352, 560], "Q2": [7, 40, 130, 532, 410],
    "Q4": [9, 84, 178, 526, 438], "Q5": [11, 175, 322, 435, 500], "Q5.2": [12, 98, 250, 492, 438], "Q6": [13, 98, 225, 530, 505],
    "Q9": [17, 118, 133, 500, 230], "Q9.2": [17, 208, 400, 452, 522]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points (key phrases, "per unit time" only in context): never scored, never shown
rub = lambda n, q, marks, bullets, clues, each=None, notes=None: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets,
                                                                 **({"each": each} if each else {}), **({"notes": notes} if notes else {})}
term = lambda n, q, a, clues, marks=1, strict=False: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                      **({"strict": True} if strict else {})}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
pick = lambda n, q, opts, pool, marks, clues: {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool,
                                               "count": len(pool)}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}
KEYPHRASES = "If any one of the underlined key phrases in the correct context is omitted, deduct 1 mark."


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]
CHANGE = ["Increases", "Decreases", "Remains the same"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which ONE of the following compounds has hydrogen bonds between its molecules?", ["CH₃CH₂CHO", "CH₃COOCH₃", "CH₃CH₂CH₂OH", "CH₃COCH₃"], 2,
        ["Hydrogen bonds need an H bonded to N, O or F.", "Which compound has an O–H group?"]),
    mcq("1.2", "Which ONE of the following is a CORRECT GENERAL FORMULA for the carboxylic acids?", ["CₙH₂ₙ₊₁O₂", "CₙH₂ₙO₂ₙ", "CₙH₂ₙO₂", "CₙHₙO₂"], 2,
        ["Ethanoic acid is CH₃COOH = C₂H₄O₂.", "Test each formula with n = 2."]),
    mcq("1.3", "Study the reactions below. Reaction 1: CH₃CH₂CHOHCH₃ —(conc. H₂SO₄)→ Compound P (major product) + H₂O. Reaction 2: Compound P "
        "—(hydrogenation)→ Compound Q. Which ONE of the following combinations is the CORRECT IUPAC names of compounds P and Q?",
        ["P: but-1-ene · Q: butane", "P: but-2-ene · Q: butane", "P: but-1-ene · Q: butan-2-ol", "P: but-2-ene · Q: butan-2-ol"], 1,
        ["Conc. H₂SO₄ removes water from the alcohol: the major product has the more substituted double bond.", "Hydrogenation adds H₂ across the double bond."],
        optTable={"head": ["COMPOUND P", "COMPOUND Q"], "rows": [["But-1-ene", "Butane"], ["But-2-ene", "Butane"], ["But-1-ene", "Butan-2-ol"], ["But-2-ene", "Butan-2-ol"]]}),
    mcq("1.4", "The potential energy diagram below is for the following hypothetical chemical reaction: X + Y ⇌ Z. Which ONE of the following combinations "
        "of values for the heat of the reaction and the activation energies can be obtained for this reaction?",
        ["ΔH −400 · EA(forward) 300 · EA(reverse) 100", "ΔH −200 · EA(forward) 300 · EA(reverse) 100", "ΔH +400 · EA(forward) 100 · EA(reverse) 300",
         "ΔH −200 · EA(forward) 100 · EA(reverse) 300"], 3,
        ["The products end lower than the reactants: is ΔH negative or positive?", "For any reaction ΔH = EA(forward) − EA(reverse)."],
        figure=fig("1.4", "A potential energy against course of reaction graph for X + Y ⇌ Z: the curve starts on a level, rises to a peak and falls to a "
                          "level below the starting one."),
        optTable={"head": ["ΔH(forward) (kJ·mol⁻¹)", "EA(forward) (kJ·mol⁻¹)", "EA(reverse) (kJ·mol⁻¹)"],
                  "rows": [["−400", "300", "100"], ["−200", "300", "100"], ["+400", "100", "300"], ["−200", "100", "300"]]}),
    mcq("1.5", "Initially, an equal number of moles of hydrogen gas, H₂(g), and iodine gas, I₂(g), are mixed in a closed container. The reaction reaches "
        "equilibrium at a constant temperature according to the balanced equation: H₂(g) + I₂(g) ⇌ 2HI(g). Which ONE of the following is ALWAYS TRUE at "
        "equilibrium?", ["[H₂] = [I₂]", "[HI] = [I₂]", "[HI] = 2[H₂]", "[H₂] = [I₂] = [HI]"], 0,
        ["H₂ and I₂ start equal and react 1 : 1.", "Equal amounts used from equal amounts: what is left?"]),
    mcq("1.6", "Consider the following reaction at equilibrium: 2SO₂(g) + O₂(g) ⇌ 2SO₃(g), ΔH = −188 kJ·mol⁻¹. Which ONE of the changes to the reaction "
        "conditions below will increase the yield of SO₃(g)?",
        ["The addition of O₂(g)", "The addition of a catalyst", "An increase in temperature", "An increase in the volume of the container at a constant temperature"], 0,
        ["A catalyst does not shift an equilibrium.", "Adding a reactant favours the forward reaction."]),
    mcq("1.7", "The table shows the ionisation constants, Ka, for two acids at 25 °C: butanoic acid, Ka = 1,5 x 10⁻⁵; ethanoic acid, Ka = 1,8 x 10⁻⁵. "
        "Consider the following statements for these two acids when they have equal concentration at 25 °C: (i) Both are weak acids. (ii) Butanoic acid is "
        "a stronger acid than ethanoic acid. (iii) The butanoic acid solution has a lower concentration of hydronium ion, H₃O⁺(aq), than the ethanoic acid "
        "solution. Which of the above statements are TRUE?", ["(i) and (ii) only", "(i) and (iii) only", "(ii) and (iii) only", "(i), (ii) and (iii)"], 1,
        ["A small Ka means a weak acid.", "The larger Ka ionises more and makes more H₃O⁺."]),
    mcq("1.8", "Which ONE of the following pairs of acids and bases, all of the same concentration, react to give the highest pH at the equivalence point in a "
        "titration at 25 °C?", ["HCℓ and NH₃", "HCℓ and NaOH", "HNO₃ and KOH", "CH₃COOH and NaOH"], 3,
        ["Strong acid + weak base: acidic; strong + strong: neutral.", "Which pair is a weak acid with a strong base?"]),
    mcq("1.9", "A standard galvanic cell is set up, as shown below. Which ONE of the following combinations of the metal used as cathode and the electron flow "
        "direction is CORRECT?", ["Cathode Cd · Cd to Ag", "Cathode Ag · Cd to Ag", "Cathode Cd · Ag to Cd", "Cathode Ag · Ag to Cd"], 1,
        ["Look up Cd and Ag in Table 4: the stronger oxidising agent's half-cell is the cathode.", "Electrons flow from the anode to the cathode."],
        figure=fig("1.9", "A Cd electrode in Cd²⁺(aq) on the left and an Ag electrode in Ag⁺(aq) on the right, joined by a salt bridge and, through a "
                          "voltmeter V, by a wire."),
        optTable={"head": ["METAL USED AS CATHODE", "ELECTRON FLOW DIRECTION"], "rows": [["Cd", "Cd to Ag"], ["Ag", "Cd to Ag"], ["Cd", "Ag to Cd"], ["Ag", "Ag to Cd"]]}),
    mcq("1.10", "An electrolytic cell is set up to electroplate an iron rod with nickel, as shown in the diagram below. Consider the following statements: (i) "
        "The iron rod is the negative electrode. (ii) The metal ions in the solution undergo reduction. (iii) The anode is pure nickel. Which of the above "
        "statements are TRUE?", ["(i) and (ii) only", "(i) and (iii) only", "(ii) and (iii) only", "(i), (ii) and (iii)"], 3,
        ["The object being plated is the cathode.", "Nickel ions are reduced onto the rod and replaced from the anode."],
        figure=fig("1.10", "Two electrodes in a beaker of solution, connected to a battery above.")),
]

# ---- QUESTION 2, the question paper pages 7-8 and the memo pages 2-3 ----
q2 = [
    mcq("2.1.1", "Write down the LETTER that represents an alcohol.", LETTERS, 3, ["An alcohol has an –OH group.", "Which formula has one O and is saturated?"], marks=1),
    mcq("2.1.2", "Write down the LETTER that represents a compound with a formyl group.", LETTERS, 0,
        ["A formyl group is –CHO.", "Look for a C=O at the end of a chain, with an H on that carbon."], marks=1),
    mcq("2.1.3", "Write down the LETTER that represents an unsaturated compound.", LETTERS, 4, ["Unsaturated: a double or triple bond between C atoms.", "CCC in a condensed formula hides a triple bond."], marks=1),
    term("2.2.1", "Write down the IUPAC name of compound B.", ["3,3-dibromo-4,4-dimethylhexane"],
         ["Find the longest chain through the central carbon.", "Number to give the lowest locants; bromo comes before methyl alphabetically."], marks=3, strict=True),
    term("2.2.2", "Write down the IUPAC name of compound E.", ["4,4-dimethylpent-2-yne", "4,4-dimethyl-2-pentyne"],
         ["CH₃C(CH₃)₂CCCH₃: the CC is a triple bond.", "Number from the end nearer the triple bond."], marks=3, strict=True),
    rub("2.3.1", "Define the term functional isomer.", 2,
        ["Compounds with the same molecular formula, but different functional groups / homologous series. (2)"],
        ["Think of what stays the same and what differs.", "Same formula, different ... ?"], each=2, notes=[KEYPHRASES]),
    pick("2.3.2", "Two different compounds in the above table are functional isomers. Write down the LETTERS that represent these functional isomers.",
         LETTERS, [0, 2], 1, ["An aldehyde and a ketone can share a molecular formula.", "Count the C, H and O of A and C."]),
    term("2.4.1", "Compound F is formed when a carboxylic acid reacts with another organic compound, X, in the presence of a catalyst. Write down the NAME or "
         "FORMULA of the catalyst.", ["H2SO4", "sulphuric acid", "sulfuric acid", "concentrated sulphuric acid", "concentrated sulfuric acid", "conc. H2SO4"],
         ["It is a strong acid.", "It also removes water from the reaction."]),
    term("2.4.2", "Write down the type of reaction.", ["esterification", "condensation"], ["A carboxylic acid and an alcohol make F.", "F is an ester."]),
    draw("2.4.3", "Write down the STRUCTURAL FORMULA of compound F.", 2,
         [["Functional group (ester, –COO–) correct", 1], ["Whole structural formula correct: CH₃COOCH₂CH₂CH₃ with every bond and H shown", 1]],
         ["F is CH₃COO(CH₂)₂CH₃.", "Show every atom and bond."]),
    term("2.4.4", "Write down the IUPAC name of compound X.", ["propan-1-ol", "1-propanol"],
         ["X is the alcohol part of the ester.", "The –(CH₂)₂CH₃ part has three carbons, the O on the first."], marks=2, strict=True),
]

# ---- QUESTION 3, the question paper page 8 and the memo pages 4-6 ----
q3 = [
    rub("3.1", "Define the term vapour pressure.", 2, ["The pressure exerted by a vapour at equilibrium with its liquid in a closed system. (2)"],
        ["It is a pressure.", "Where is the vapour, and what is it in equilibrium with?"], each=2, notes=[KEYPHRASES]),
    mcq("3.2.1", "The vapour pressures of compounds A, B and C are given in random order: 79 kPa, 146 kPa, 58 kPa. Write down the vapour pressure of compound C.",
        ["79 kPa", "146 kPa", "58 kPa"], 1, ["All three have the same molar mass.", "The most branched compound has the weakest forces and the highest vapour pressure."], marks=1),
    rub("3.2.2", "Fully explain your answer to QUESTION 3.2.1.", 3,
        ["Compound C is more branched / has a shorter chain / is more compact / spherical / has a smaller surface area (than A and B) (1)",
         "Compound C has weaker intermolecular forces / London forces / Van der Waals forces than A and B (1)",
         "Less energy is needed to overcome / break the intermolecular forces in compound C (than in A and B) (1)"],
        ["Compare the structures (branching, surface area).", "Then the intermolecular forces, then the energy needed to overcome them."]),
    mcq("3.3.1", "Compounds D and E are compared. Which compound has the lower boiling point?", ["D", "E"], 1,
        ["D is propanoic acid; E is butanal.", "The weaker intermolecular forces give the lower boiling point."], marks=1),
    rub("3.3.2", "Fully explain the difference in the vapour pressures between compounds D and E.", 4,
        ["Compound D / propanoic acid has hydrogen bonding (dipole-dipole and London forces) between its molecules (1)",
         "Compound E / butanal has dipole-dipole forces (and London forces) between its molecules (1)",
         "The intermolecular forces in D / propanoic acid are stronger than those in E / butanal (1)",
         "More energy is needed to overcome / break the intermolecular forces in D / propanoic acid than in E / butanal (1)"],
        ["Name the strongest intermolecular force in each compound.", "Compare their strength and the energy needed to overcome them."]),
]

# ---- QUESTION 4, the question paper pages 9-10 and the memo pages 7-9 ----
q4 = [
    rub("4.1", "Define the term cracking reaction.", 2,
        ["The chemical process / reaction in which longer chain hydrocarbon / alkane molecules are broken down to shorter (more useful) molecules. (2)"],
        ["It splits big molecules.", "Long-chain alkanes become ..."], each=2, notes=[KEYPHRASES]),
    rub("4.2", "Is the product in reaction II a PRIMARY, SECONDARY or TERTIARY haloalkane? Give a reason for the answer.", 2,
        ["Primary (1)", "The halogen/bromine/Br (atom) is bonded to a C atom that is bonded to only one other C atom OR the halogen/bromine/Br is bonded to the first/terminal C atom (1)"],
        ["The product is CH₃CH₂CH₂CH₂Br.", "How many other C atoms is the C bearing the Br bonded to?"]),
    draw("4.3.1", "Write down the STRUCTURAL FORMULA of compound W.", 3,
         [["Correct stem: 4 C atoms in a chain", 1], ["Whole structural formula correct (butane, every H shown)", 2]],
         ["Reaction II turns W into CH₃CH₂CH₂CH₂Br by substitution.", "W is the alkane with four carbons."]),
    term("4.3.2", "Write down the MOLECULAR formula of compound U.", ["C8H18"],
         ["Cracking U gives W (C₄H₁₀) and T (C₄H₈) as the only products.", "Add the atoms of W and T."], strict=True),
    term("4.4.1", "For reaction II, write down the NAME or FORMULA of the inorganic reactant.", ["Br2", "bromine"],
         ["Reaction II puts a Br on an alkane.", "It is a halogen."]),
    mcq("4.4.2", "For reaction II, write down the type of reaction (Choose from SUBSTITUTION, ADDITION or ELIMINATION.)", ["Substitution", "Addition", "Elimination"], 0,
        ["An alkane has no double bond to add to.", "An H is swapped for a Br."], marks=1),
    lst("4.4.3", "For reaction II, write down ONE reaction condition.", 1, [["UV (light)", "ultraviolet", "sunlight", "light"], ["heat"]],
        ["Alkanes react with bromine only with energy supplied.", "Light, or ..."]),
    term("4.5", "Write down the TYPE of elimination in reaction III.", ["dehydrohalogenation", "dehydrobromination"],
         ["Reaction III removes H and Br from CH₃CH₂CH₂CH₂Br.", "The name says what is removed: hydrogen and a halogen."]),
    draw("4.6.1", "Compounds R and T are positional isomers. The inorganic reagents Br₂, H₂SO₄(conc.), NaOH(conc.), HBr and H₂ are available for reactions IV "
         "and V. Write down the balanced equation for reaction IV, using STRUCTURAL FORMULAE and the correct inorganic reagent shown above.", 5,
         [["Functional group of the alkene on the first C atom", 1], ["Whole structural formula of the alkene (but-1-ene) correct", 1], ["HBr", 1],
          ["Functional group of the haloalkane correct", 1], ["Whole structural formula of the haloalkane correct (halogen on the second / first C atom)", 1]],
         ["R comes from 1-bromobutane by elimination: it is but-1-ene.", "S is made from R by addition of HBr."],
         memo="Condensed, semi-structural or molecular formulae: max 1/5. An extra product or reactant: deduct 1 mark."),
    draw("4.6.2", "Write down the balanced equation for reaction V, using STRUCTURAL formulae and the correct reagent shown above.", 3,
         [["NaOH", 1], ["Whole structural formula of the alkene correct (functional group on the second / first C atom)", 1], ["NaBr + H₂O", 1]],
         ["Reaction V makes T (C₄H₈) from S by elimination.", "Concentrated NaOH removes HBr."],
         memo="Condensed, semi-structural or molecular formulae: max 1/3. An extra product or reactant: deduct 1 mark."),
    term("4.6.3", "Write down the IUPAC name of compound T.", ["but-2-ene", "2-butene", "but-1-ene", "1-butene"],
         ["T is C₄H₈ and a positional isomer of R.", "R has the double bond at the end of the chain."], marks=2),
]

# ---- QUESTION 5, the question paper pages 11-12 and the memo pages 10-12 ----
q5a = [
    rub("5.1.1", "Define the term reaction rate.", 2,
        ["ANY ONE: the change in concentration of products/reactants per (unit) time; the change in amount/number of moles/volume/mass of products or "
         "reactants per (unit) time; the amount/number of moles/volume/mass of products formed/reactants used per (unit) time; the rate of change in "
         "concentration/amount/number of moles/volume/mass. (2 or 0)"],
        ["How quickly something changes.", "A change in amount or concentration, divided by time."], each=2,
        notes=["Give the mark for 'per unit time' only in the context of reaction rate."]),
    steps("5.1.2", "For the time interval t = 0 to t = 5 minutes, the average reaction rate for the formation of H₂(g) is 0,033 dm³·min⁻¹. Calculate the mass of "
          "Aℓ present in the container at t = 5 minutes. Take the molar gas volume as 24,5 dm³·mol⁻¹.", 6,
          [("Volume of H₂ formed in the first 5 minutes (dm³)", 1, 0.165, 0.001, "Rate = ΔV/Δt: 0,033 = ΔV/5 ✓; V(H₂) = 0,165 dm³"),
           ("Moles of H₂ formed (mol)", 1, 6.73e-3, 0.05e-3, "n = V/Vm = 0,165/24,5 ✓ = 6,74 x 10⁻³ mol"),
           ("Moles of Aℓ used (mol)", 1, 4.49e-3, 0.05e-3, "n(Aℓ) = ⅔ n(H₂) ✓ = 4,49 x 10⁻³ mol"),
           ("Mass of Aℓ left at t = 5 minutes (g)", 3, 0.3925, 0.0275, "n = m/M: 4,49 x 10⁻³ = m/27 ✓, m = 0,12 g; Δm = 0,5 − 0,12 ✓ = 0,38 g ✓ "
            "(range 0,365 – 0,42 g)")],
          ["Work out the volume of H₂ made in 5 minutes, then its moles.", "2 mol Aℓ make 3 mol H₂; subtract the Aℓ used from the 0,5 g at the start."]),
    rub("5.1.3", "Assume that the concentration of the HCℓ(aq) stays constant for the duration of the reaction. Use the collision theory to explain the change in "
        "the reaction rate from t = 0 to t = 5 minutes.", 4,
        ["The surface area / contact area / mass / size of the aluminium decreases (1)", "Fewer particles are exposed (1)",
         "Fewer effective collisions per unit time OR a lower frequency of effective collisions (1)", "The reaction rate decreases / slows down (1)"],
        ["The acid's concentration stays the same, so what is changing?", "Less aluminium exposed means fewer effective collisions per second."]),
    draw("5.1.4", "Experiment I is repeated using a 2 mol·dm⁻³ HCℓ solution (Experiment II). Redraw the above graph (NO numerical values need to be shown) and "
         "label the curve A. On the same set of axes, draw the curve that will be obtained for Experiment II. Label this as curve B.", 2,
         [["Curve B starts at the origin and ends at the same point (volume) as curve A", 1], ["The gradient of curve B is steeper for the whole duration", 1]],
         ["The aluminium is the limiting reactant: the final volume stays the same.", "A more concentrated acid reacts faster."],
         memo="Graph not labelled: max 1/2."),
    mcq("5.1.5", "Experiment I is repeated using 0,5 g pure powdered Aℓ (Experiment III). How will the volume of H₂(g) produced in Experiment III compare to that "
        "in Experiment I? Choose from GREATER THAN, LESS THAN or EQUAL TO.", ["Greater than", "Less than", "Equal to"], 2,
        ["Powder changes how fast, not how much.", "The same mass of aluminium makes the same amount of H₂."], marks=1),
]
q5b = [
    rub("5.2.1", "What change was made to obtain curve Y?", 1, ["An increase in temperature / the temperature was increased (1)"],
        ["Curve Y has more particles at high kinetic energy.", "Which condition changes the spread of particle energies?"]),
    rub("5.2.2", "Give a reason for the answer to QUESTION 5.2.1.", 1,
        ["Curve Y has its peak at a higher kinetic energy / the peak shifted to the right OR the (average) kinetic energy of the particles increases / more "
         "particles have higher kinetic energy. (1)"],
        ["Compare where the two peaks are.", "What does a peak further right mean for the particles' energy?"]),
]

# ---- QUESTION 6, the question paper pages 13-14 and the memo pages 13-21 ----
q6a = [
    rub("6.1.1", "Define the term chemical equilibrium.", 2,
        ["(The dynamic equilibrium when) the rate of the forward reaction equals the rate of the reverse reaction. (2 or 0)",
         "OR — The stage in a chemical reaction when the concentrations of the reactants and products remain constant. (2)"],
        ["Two reactions run at once.", "What is equal at equilibrium?"], each=2),
    mcq("6.1.2", "At t₁, oxygen, O₂(g), was added to the container. Write down the letter that represents O₂(g). Choose from X, Y or Z.", ["X", "Y", "Z"], 0,
        ["Adding a gas makes its concentration jump at once.", "Which line jumps up at t₁?"], marks=1),
    mcq("6.1.3", "At t₂, the pressure is adjusted by changing the volume of the container. Was the pressure INCREASED or DECREASED?", ["Increased", "Decreased"], 1,
        ["All the concentrations change at once at t₂.", "Did they all jump up or drop down?"], marks=1),
    rub("6.1.4", "Give a reason for the answer to QUESTION 6.1.3.", 1, ["The concentrations of (all) the gases decreased / the reverse reaction was favoured. (1)"],
        ["Look at all three lines at t₂.", "A bigger volume lowers every concentration."]),
    term("6.1.5", "Write down the NAME or FORMULA of the gas that is represented by the letter Z.", ["CO", "carbon monoxide"],
         ["X is O₂.", "Which gas changes the same way as O₂ when the system shifts?"]),
    rub("6.1.6", "Give a reason for the answer to QUESTION 6.1.5.", 1,
        ["The concentration of Z (CO) follows the same trend as X (O2) / Z and X are both reactants / Y (CO2) is the product OR the reverse reaction is "
         "favoured to increase the number of moles. (1)"],
        ["Compare Z's line with X's.", "Reactants rise and fall together."]),
    mcq("6.1.7", "What change in temperature is made at t₃? Choose between INCREASED or DECREASED.", ["Increased", "Decreased"], 1,
        ["After t₃ the product's concentration rises.", "ΔH < 0: which temperature change favours the forward (exothermic) reaction?"], marks=1),
    rub("6.1.8", "Use Le Chatelier's principle to explain the answer to QUESTION 6.1.7.", 3,
        ["The concentration of the product (Y / CO2) increases OR the concentration of the reactants (X / Z / CO / O2) decreases OR the forward reaction is favoured (1)",
         "The forward reaction is exothermic (1)", "A decrease in temperature favours the exothermic reaction (1)"],
        ["Say what the graph shows after t₃.", "Then which reaction is exothermic and what a lower temperature favours."]),
]
q6b = [
    steps("6.2", "Carbon monoxide gas, CO(g), reacts with water vapour, H₂O(g), at T °C. The reaction reaches chemical equilibrium according to the balanced "
          "equation: CO(g) + H₂O(g) ⇌ CO₂(g) + H₂(g). Initially, 0,6 moles of CO(g), 0,6 moles of H₂O(g), 0,1 moles of carbon dioxide gas, CO₂(g), and 0,1 "
          "moles of hydrogen gas, H₂(g), were mixed and sealed in a 2 dm³ flask. If the equilibrium constant, Kc, for this reaction at T °C is 4, calculate "
          "the mass of CO(g) present in the flask at equilibrium.", 9,
          [("Moles of CO that react before equilibrium (mol)", 6, 0.367, 0.01,
            "Ratio 1 : 1 : 1 : 1 ✓; n(eq) = 0,6 − x and 0,1 + x ✓; divide by 2 dm³ ✓; Kc = [CO₂][H₂]/[CO][H₂O] ✓; 4 ✓ = (0,1 + x)²/(0,6 − x)² (over 2²) ✓; "
            "x = 0,37 mol"),
           ("Moles of CO at equilibrium (mol)", 1, 0.235, 0.01, "n(CO)eq = 0,6 − 0,37 ✓ = 0,23 mol (0,24 mol by concentrations)"),
           ("Mass of CO at equilibrium (g)", 2, 6.58, 0.14, "n = m/M: 0,23 = m/28 ✓; m = 6,44 g ✓ (range 6,44 – 6,72 g)")],
          ["Make a table: initial, change, equilibrium, for all four gases (they react 1 : 1 : 1 : 1).", "√4 = 2 = (0,1 + x)/(0,6 − x): solve for x."]),
]

# ---- QUESTION 7, the question paper page 15 and the memo pages 22-25 ----
q7 = [
    rub("7.1", "Define the term weak base.", 2,
        ["Weak bases dissociate / ionise incompletely / partially in water (1)", "to form a low concentration of hydroxide/OH- ions (1)"],
        ["Compare with a strong base.", "How completely does it ionise, and what does it form?"]),
    term("7.2", "Write down the formula of the conjugate acid of the carbonate ion, CO₃²⁻(aq).", ["HCO3-", "HCO3", "hydrogen carbonate", "hydrogencarbonate", "bicarbonate"],
         ["A conjugate acid has one more H⁺.", "Add H⁺ to CO₃²⁻."], strict=True),
    num("7.3.1", "Determine the value of p.", 26.55, 0.01, "cm³", ["p is run 1's final burette reading.", "Final = initial + volume used."]),
    num("7.3.2", "Determine the value of q.", 28.15, 0.01, "cm³", ["q is run 2's initial burette reading.", "Initial = final − volume used."]),
    rub("7.4", "METHYL ORANGE is used as the indicator. Explain why methyl orange is the most suitable indicator for this titration by referring to the pH at the "
        "equivalence point.", 2,
        ["The equivalence point is at a pH less than 7 OR the solution at the equivalence point is acidic (a strong acid with a weak base) (1)",
         "Methyl orange changes colour in this (acidic) pH range / at a pH less than 7 (1)"],
        ["HCℓ is strong; K₂CO₃ is a weak base.", "Where is the equivalence point, and where does methyl orange change colour?"]),
    steps("7.5", "Calculate the concentration of the K₂CO₃ solution.", 5,
          [("Moles of HCℓ used (mol)", 2, 2.5e-3, 0.01e-3, "n = cV ✓ = (0,1)(25 x 10⁻³) ✓ = 2,5 x 10⁻³ mol"),
           ("Moles of K₂CO₃ that reacted (mol)", 1, 1.25e-3, 0.01e-3, "n(K₂CO₃) = ½ n(HCℓ) ✓ = 1,25 x 10⁻³ mol"),
           ("Concentration of the K₂CO₃ solution (mol·dm⁻³)", 2, 0.06125, 0.00125, "c = n/V with the average volume 20,1 cm³ ✓: 1,25 x 10⁻³/(20,1 x 10⁻³) "
            "= 0,0622 mol·dm⁻³ ✓ (range 0,06 – 0,0625; 20,05 or 20,15 used: −1)")],
          ["Use the average volume of K₂CO₃ from the two runs.", "1 mol K₂CO₃ reacts with 2 mol HCℓ."]),
    steps("7.6", "The above K₂CO₃ solution used in the titration was prepared by completely dissolving 6,525 g of the hydrated potassium carbonate, K₂CO₃·xH₂O, "
          "in 600 cm³ water. Calculate the value of x in the formula K₂CO₃·xH₂O.", 5,
          [("Moles of K₂CO₃·xH₂O in the 600 cm³ (mol)", 2, 0.0374, 0.0005, "n = cV ✓ = (0,0622)(0,6) ✓ = 0,0373 mol"),
           ("Molar mass of K₂CO₃·xH₂O (g·mol⁻¹)", 1, 174.9, 1.0, "M = m/n = 6,525/0,0373 ✓ = 174,84 g·mol⁻¹"),
           ("x", 2, 2, 0.05, "2(39) + 12 + 3(16) + x(18) = 174,84 ✓ (138 and 18); x = 2 ✓ (positive marking from 7.5)")],
          ["Use the concentration from 7.5 and the 600 cm³.", "M(K₂CO₃) = 138 g·mol⁻¹ and M(H₂O) = 18 g·mol⁻¹."]),
]

# ---- QUESTION 8, the question paper page 16 and the memo page 26 ----
q8 = [
    rub("8.1.1", "Use oxidation numbers for EACH of the reactants and explain why this reaction is a redox reaction.", 2,
        ["The oxidation number of H changes from +1 to 0 / decreases (it is reduced) (1)", "The oxidation number of Mg changes from 0 to +2 / increases (it is oxidised) (1)"],
        ["Give the oxidation numbers of Mg and of H, before and after.", "One goes up (oxidised), one goes down (reduced)."]),
    term("8.1.2", "Write down the FORMULA of the oxidising agent in this reaction.", ["H+", "HCl", "HCℓ", "H3O+"],
         ["The oxidising agent is reduced.", "Which reactant's oxidation number decreases?"]),
    rub("8.1.3", "It is observed that dilute hydrochloric acid does not react with copper, Cu(s), at 25 °C. Explain this observation by referring to the relative "
        "strengths of the reducing agents.", 2,
        ["Cu/copper is a weaker reducing agent than hydrogen/H2 (and will not reduce H+ to H2). (2)"],
        ["Find Cu and H₂ in Table 4.", "Compare them as reducing agents."], each=2),
    rub("8.1.4", "Will dilute nitric acid, HNO₃(aq), react with copper, Cu(s), at 25 °C? Choose from YES or NO. Explain the answer in terms of the relative "
        "strengths of the oxidising agents.", 3,
        ["Yes (1)", "NO3-/NO₃⁻/nitrate ion/nitric acid is a stronger oxidising agent (1)", "than Cu2+/Cu²⁺/copper(II) ion (so Cu is oxidised to Cu²⁺) (1)"],
        ["Find NO₃⁻ and Cu²⁺ in Table 4.", "Compare them as oxidising agents."]),
    # an equation as a phone types it: each species also in ASCII (the subscripts and charges of "2Fe³⁺" normalise away)
    rub("8.2.1", "A galvanic cell is represented by the following cell notation: Pb(s) | Pb²⁺(aq) || Fe³⁺(aq), Fe²⁺(aq) | Pt(s). Write down the balanced net ionic "
        "equation for this cell.", 3,
        ["(Reactants) Pb + 2Fe3+ (Pb + 2Fe³⁺) (1)", "(Products) Pb2+ + 2Fe2+ (Pb²⁺ + 2Fe²⁺) (1)", "(Balanced) Pb + 2Fe3+ → Pb2+ + 2Fe2+ (1)"],
        ["The anode (left of ||) is oxidised; the cathode's oxidising agent is reduced.", "Balance the electrons: one Pb gives two electrons, each Fe³⁺ takes one."],
        notes=["Ignore ⇌ and phases. Marking rule 6.3.10."]),
    mcq("8.2.2", "A stronger reducing agent is now used with the same oxidising agent under the same conditions. How will this affect the initial emf of the cell? "
        "Choose from INCREASES, DECREASES or NO EFFECT.", ["Increases", "Decreases", "No effect"], 0,
        ["A stronger reducing agent has a more negative E°.", "E°cell = E°cathode − E°anode."], marks=1),
]

# ---- QUESTION 9, the question paper page 17 and the memo pages 27-28 ----
q9a = [
    # decide by calculation: the conclusion (non-spontaneous) rides on the negative E°cell
    steps("9.1", "A strip of silver is added to a 1 mol·dm⁻³ solution of Pb(NO₃)₂ at 25 °C. Consider the reaction below: 2Ag(s) + Pb²⁺(aq) → 2Ag⁺(aq) + Pb(s). "
          "By means of a calculation, determine whether this reaction is SPONTANEOUS or NON-SPONTANEOUS.", 5,
          [("E°cell for this reaction (V)", 5, -0.93, 0.005, "E°cell = E°reduction − E°oxidation ✓ = −0,13 ✓ − (0,80) ✓ = −0,93 V ✓; negative, so "
            "NON-SPONTANEOUS ✓")],
          ["Pb²⁺ is reduced (cathode); Ag is oxidised (anode).", "A negative E°cell means the reaction is not spontaneous."]),
]
q9b = [
    rub("9.2.1", "Define an electrolyte.", 2,
        ["ANY ONE: a substance of which the (aqueous) solution contains ions (2)",
         "OR — a substance that dissolves in water to give a solution that conducts electricity (2)",
         "OR — a substance that forms ions in water / when melted (2)", "OR — a solution / substance that conducts electricity through the movement of ions (2)"],
        ["It is about ions.", "What does its solution contain, or do?"], each=2),
    rub("9.2.2", "Write down the PREDOMINANT oxidation half-reaction that takes place in this cell.", 2,
        ["2Cl- → Cl2 + 2e- (2Cℓ⁻ → Cℓ₂ + 2e⁻) (2)"],
        ["Oxidation happens at the anode.", "In concentrated NaCℓ, chloride ions are oxidised."], each=2,
        notes=["Cℓ₂ + 2e⁻ ← 2Cℓ⁻: 2/2; 2Cℓ⁻ ⇌ Cℓ₂ + 2e⁻: 1/2; Cℓ₂ + 2e⁻ ⇌ 2Cℓ⁻ or 2Cℓ⁻ ← Cℓ₂ + 2e⁻: 0/2. The charge on Cℓ⁻ omitted: max 1/2."]),
    lst("9.2.3", "Write down the NAMES or FORMULAE of the products formed at electrode Q.", 2,
        [["hydrogen (gas)", "H2"], ["hydroxide (ions)", "OH-", "sodium hydroxide", "NaOH"]],
        ["Electrode Q is the cathode: reduction.", "Water is reduced there: what does it form?"]),
    rub("9.2.4", "Explain the answer to QUESTION 9.2.3 by referring to the relative strengths of the oxidising agents involved.", 2,
        ["Water/H2O is a stronger oxidising agent than Na+/sodium ions (1)", "so water / H2O is reduced (1)"],
        ["Compare H₂O and Na⁺ as oxidising agents.", "The stronger oxidising agent is reduced."]),
]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Organic compounds", "marks": 18,
     "lead": "The letters A to H in the table below represent organic compounds. C: butanone; D: C₄H₁₀O; E: CH₃C(CH₃)₂CCCH₃; F: CH₃COO(CH₂)₂CH₃; G: C₄H₈O₂; "
             "H: CH₃C(CH₃)₂CH₂CH₃. A and B are structural formulae (see the figure).",
     "figure": fig("Q2", "A table of eight compounds. A, a structural formula: four carbons in a chain; the first carries three H, the second and third two H "
                         "each, and the fourth is double-bonded to an O and bonded to one H. B, a structural formula: a central carbon bonded to a CH₃ on the left, "
                         "a CH₂–CH₃ going up, a CH₃ going down and, on the right, a carbon carrying two Br that continues to CH₂ and then CH₃. C butanone, D "
                         "C₄H₁₀O, E CH₃C(CH₃)₂CCCH₃, F CH₃COO(CH₂)₂CH₃, G C₄H₈O₂, H CH₃C(CH₃)₂CH₂CH₃."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Vapour pressure", "marks": 11,
     "lead": "The vapour pressures of different organic compounds are determined at 20 °C. The vapour pressures of compounds A, B and C are NOT shown in the table.",
     "table": {"head": ["COMPOUND", "IUPAC NAME", "MOLAR MASS (g·mol⁻¹)", "VAPOUR PRESSURE (kPa) AT 20 °C"],
               "rows": [["A", "Pentane", "72", "–"], ["B", "2-methylbutane", "72", "–"], ["C", "2,2-dimethylpropane", "72", "–"],
                        ["D", "Propanoic acid", "74", "0,32"], ["E", "Butanal", "72", "12,2"]]}, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Organic reactions", "marks": 22,
     "lead": "Study the flow diagram below. Reaction I is a CRACKING REACTION forming two organic compounds, W and T, as the ONLY products.",
     "figure": fig("Q4", "A flow diagram. Organic compound U → (reaction I) → organic compound W + organic compound T (C₄H₈). W → (reaction II) → "
                         "CH₃CH₂CH₂CH₂Br. CH₃CH₂CH₂CH₂Br → (reaction III, elimination) → organic compound R. R → (reaction IV) → organic compound S. "
                         "S → (reaction V) → T."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Reaction rates", "marks": 15,
     "lead": "The reaction between pure aluminium, Aℓ(s), and EXCESS hydrochloric acid, HCℓ(aq), is used to investigate the factors that affect the rate of a "
             "reaction. The balanced equation for the reaction is: 2Aℓ(s) + 6HCℓ(aq) → 2AℓCℓ₃(aq) + 3H₂(g). EXPERIMENT I: In this experiment, 1 mol·dm⁻³ HCℓ "
             "solution reacts with a 0,5 g Aℓ strip from an aluminium roll at room temperature. The graph of volume H₂(g) versus time for this experiment, "
             "not drawn to scale, is shown below.",
     "figure": fig("Q5", "Volume of H₂ (dm³) against time (minutes): a curve rising from the origin, steep at first and levelling off; a dashed line marks "
                         "t = 5 minutes on the curve."), "items": q5a},
    {"id": "5.2", "title": "Question 5", "kind": "Reaction rates", "marks": 2,
     "lead": "Curve X is the Maxwell-Boltzmann distribution curve for a reaction under a set of reaction conditions. A change was made to one of the reaction "
             "conditions to obtain curve Y.",
     "figure": fig("Q5.2", "Number of particles against kinetic energy: dashed curve X has a tall, narrow peak at low kinetic energy; solid curve Y has a "
                           "lower, wider peak further to the right."), "items": q5b},
    {"id": "6", "title": "Question 6", "kind": "Chemical equilibrium", "marks": 11,
     "lead": "The reaction of carbon monoxide gas, CO(g), with oxygen gas, O₂(g), is investigated. The reaction reaches equilibrium in a closed container at "
             "constant temperature T °C, according to the balanced equation: 2CO(g) + O₂(g) ⇌ 2CO₂(g), ΔH < 0. Changes to the conditions of equilibrium "
             "are made at different times. The graph shows the results obtained. X, Y and Z represent the gases in the above reaction.",
     "figure": fig("Q6", "Concentration (mol·dm⁻³) against time (minutes), three lines X (top, solid), Y (middle, dashed) and Z (bottom, dotted), flat at "
                         "first. At t₁ X jumps up and falls back a little, Y rises and Z falls; at t₂ all three drop; at t₃ X and Z fall a little and Y rises."),
     "items": q6a},
    {"id": "6.2", "title": "Question 6", "kind": "Chemical equilibrium", "marks": 9, "lead": "", "items": q6b},
    {"id": "7", "title": "Question 7", "kind": "Acids and bases", "marks": 17,
     "lead": "Hydrated potassium carbonate, K₂CO₃·xH₂O, is a WEAK BASE. A solution is prepared by dissolving some of this solid in water. For QUESTIONS 7.3 to "
             "7.5: a hydrochloric acid solution, HCℓ(aq), of concentration 0,1 mol·dm⁻³ is titrated with the prepared potassium carbonate solution, "
             "K₂CO₃(aq), of unknown concentration. The balanced equation for the reaction is: K₂CO₃(aq) + 2HCℓ(aq) → 2KCℓ(aq) + CO₂(g) + H₂O(ℓ). The "
             "results of the titration are given below (K₂CO₃(aq) in the burette).",
     # transposed for phones (2026-10-10): the paper's five columns cut off at 360 px; the same values, a run per column
     "table": {"head": ["", "RUN 1", "RUN 2"],
               "rows": [["Volume of HCℓ(aq) used (cm³)", "25", "25"], ["Initial burette reading (cm³)", "6,5", "q"],
                        ["Final burette reading (cm³)", "p", "48,3"], ["Volume of K₂CO₃(aq) used (cm³)", "20,05", "20,15"]]}, "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Redox reactions", "marks": 12,
     "lead": "Dilute hydrochloric acid, HCℓ(aq), reacts with magnesium, Mg(s), at 25 °C according to the following balanced equation: "
             "Mg(s) + 2HCℓ(aq) → MgCℓ₂(aq) + H₂(g).", "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Electrochemistry", "marks": 5, "lead": "",
     "figure": fig("Q9", "A beaker of Pb(NO₃)₂(aq) with a silver strip lying at the bottom."), "items": q9a},
    {"id": "9.2", "title": "Question 9", "kind": "Electrochemistry", "marks": 8,
     "lead": "The simplified diagram below represents an electrolytic cell. The electrodes are made of carbon.",
     "figure": fig("Q9.2", "A beaker of concentrated NaCℓ(aq) with two carbon electrodes connected to a battery above; the right-hand electrode is labelled "
                           "Q and is connected to the battery's negative terminal."), "items": q9b},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Chemistry", "total": 150, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from the paper and memo PDFs and their page images "
                                                           "(structural formulae are drawings); no API call."},
        {"n": "2.4.3", "kind": "no_fit", "detail": "Structural formulae (2.4.3, 4.3.1) and equations in structural formulae (4.6.1, 4.6.2), and the redrawn graph "
                                                   "(5.1.4), are done on paper and self-checked against the memo's criteria."},
        {"n": "8.2.1", "kind": "no_fit", "detail": "A balanced equation (8.2.1) and a half-reaction (9.2.2) are written answers: the keyword stand-in checks that "
                                                   "the memo's species are named (in ASCII too: 2Fe3, Pb2, 2Cl, Cl2), not the balancing, the arrow or the side "
                                                   "each is on; a reversed equation scores. An equation control, or model marking, would mark them properly."},
        {"n": "9.1", "kind": "no_fit", "detail": "Decide by calculation: one step on E°cell (−0,93 V); the conclusion 'non-spontaneous' rides on its sign."},
        {"n": "7", "kind": "no_fit", "detail": "The titration table is transposed (a run per column): the paper's five columns cut off on a 360 px phone. The "
                                               "values are the paper's."},
        {"n": "5.1.2", "kind": "memo_issue", "detail": "Memo ranges played as their centre with a tolerance covering them: 5.1.2 (0,365 – 0,42 g), 6.2 "
                                                       "(6,44 – 6,72 g), 7.5 (0,06 – 0,0625 mol·dm⁻³)."},
    ],
}
out = Path(__file__).parent / "out" / "ps-p2-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    print(m["id"], "parts:", len(m["items"]), "marks:", sum(i["marks"] for i in m["items"]), "/", m["marks"])
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
