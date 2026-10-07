"""Physical Sciences P2 (Chemistry) Nov 2025, the whole paper (Questions 1 to 9), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper draws its structural formulae
and sets charges as images, so its text layer has gaps.

  python tools/ingest/transcribe_ps_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P2 Nov 2025 Eng.pdf" "<...>/Physical Sciences P2 Nov 2025 MG Afr & Eng.pdf" --id ps-p2-2025-11 --from-json

How the memo's shapes map (Chemistry; the Physics paper's rules hold, see transcribe_ps_p1_2025_11.py):
  an IUPAC name, a formula, a cell notation -> term with strict (one letter is another compound: hexane / hexene, H2SO4 / H2SO3;
  spacing and punctuation free), the memo's part marks played all or nothing; "Write down the LETTER(S)" -> mcq (one letter) or
  pickn (two letters); a choice the paper names (EXOTHERMIC or ENDOTHERMIC, 10 s or 30 s, CO or O2) -> mcq; a STRUCTURAL formula or
  a redrawn curve -> draw, self-checked against the memo's criteria; "Write a balanced equation" -> rubric (reactants, products,
  balancing). A charge typed as "2-" is read through its digit only (norm drops signs): HPO4 2- needs the 2, H2PO4- cannot check its -.
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves and checked on a contact sheet."""
import json
from pathlib import Path

W, H = 595.44, 841.68
FIGS = {  # tools: scratchpad figs_p2.py; [page, x0, y0, x1, y1] in points
    "1.5": [4, 183.0, 384.4, 378.8, 519.0], "1.10": [6, 135.3, 342.8, 444.0, 504.0], "Q2": [7, 49.9, 133.8, 531.9, 533.7],
    "Q2.3": [8, 198.9, 194.6, 472.0, 241.6], "Q3": [9, 196.0, 163.7, 404.0, 315.0], "Q5": [11, 96.0, 232.0, 500.0, 482.9],
    "Q5.3": [12, 220.6, 301.0, 428.0, 488.3], "Q8": [15, 138.9, 145.6, 408.0, 294.8], "Q9": [16, 104.7, 146.6, 480.0, 323.0]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


rub = lambda n, q, marks, bullets, clues, each=None: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets,
                                                     **({"each": each} if each else {})}
term = lambda n, q, a, clues, marks=1, strict=False: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                      **({"strict": True} if strict else {})}
pick = lambda n, q, opts, pool, marks, clues: {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool,
                                               "count": len(pool)}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


LETTERS = ["A", "B", "C", "D", "E", "F", "G"]
CHANGE = ["Increases", "Decreases", "Remains the same"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which ONE of the following is the name of the functional group of propan-1-ol?", ["Carboxyl", "Carbonyl", "Hydroxyl", "Formyl"], 2,
        ["Propan-1-ol is an alcohol.", "Name the –OH group."]),
    mcq("1.2", "The organic compound C₂H₄ is converted to an alkane as shown by the reaction below.\nC₂H₄ → Alkane\nWhich ONE of the following is a "
        "suitable catalyst for this reaction?", ["Lead", "Platinum", "Hydrogen", "Iron"], 1,
        ["Turning an alkene into an alkane adds hydrogen: hydrogenation.", "Its catalyst is a transition metal such as Pt, Pd or Ni."]),
    mcq("1.3", "Which of the following statements ALWAYS apply to compounds that are structural isomers of one another?\n(i) They belong to the same "
        "homologous series.\n(ii) They have the same structural formula.\n(iii) They have the same molecular formula.",
        ["(iii) only", "(i) and (iii) only", "(i) and (ii) only", "(i), (ii) and (iii)"], 0,
        ["Structural isomers: the same molecular formula, a different structural formula.", "Functional isomers are structural isomers in DIFFERENT homologous series."]),
    mcq("1.4", "Magnesium ribbon of mass 2 g reacts with excess hydrochloric acid of concentration 0,1 mol·dm⁻³ at 20 °C:\nMg(s) + 2HCℓ(aq) → "
        "MgCℓ₂(aq) + H₂(g)\nWhich ONE of the following changes will NOT increase the initial rate of the reaction?",
        ["Using 2 g of powdered magnesium", "Increasing the temperature of HCℓ to 30 °C", "Using a longer piece of the magnesium ribbon",
         "Doubling the volume of the hydrochloric acid used"], 3,
        ["The rate depends on concentration, temperature, surface area and catalysts.", "Which change leaves the acid's concentration the same?"]),
    mcq("1.5", "The following reaction reaches equilibrium in a closed container:\nH₂(g) + S(s) ⇌ H₂S(g)   ΔH < 0\nThe reaction rate versus time "
        "graph for the reaction is given below. What change was made to the system at time t₁?",
        ["The pressure was increased at a constant temperature.", "The volume of the container was increased.", "The temperature was increased.",
         "More hydrogen was added to the system."], 0,
        ["Both rates jump up at the same moment and stay equal: the equilibrium does not shift.", "There is 1 mol of gas on each side: which change speeds both up equally?"],
        figure=fig("1.5", "Reaction rate against time: a solid line falls and a dashed line rises until they meet and run level; at t₁ both jump "
                   "straight up, together, to the same higher rate and stay level and equal.")),
    mcq("1.6", "A hypothetical endothermic reaction is given below.\nA(g) + B(g) ⇌ AB(g)\nThe activation energy for the reverse reaction is "
        "50 kJ·mol⁻¹. Which ONE of the following is possible for the reaction above?",
        ["The heat of the reaction is +70 kJ·mol⁻¹.", "The activation energy for the forward reaction is 50 kJ·mol⁻¹.",
         "The energy of the activated complex is 40 kJ·mol⁻¹.", "The activation energy for the forward reaction is 40 kJ·mol⁻¹."], 0,
        ["Endothermic: ΔH > 0.", "ΔH = Ea(forward) − Ea(reverse): the forward barrier is the bigger one."]),
    mcq("1.7", "The products for the reaction between a metal oxide and an acid are …",
        ["a salt and water.", "a salt and hydrogen gas.", "a salt and carbon dioxide.", "a salt, water and carbon dioxide."], 0,
        ["A metal oxide is a base.", "Acid + base → salt + ..."]),
    mcq("1.8", "The concentration of each of the four solutions below is 0,1 mol·dm⁻³.\nHNO₃(aq), NH₃(aq), NaOH(aq) and H₂CO₃(aq)\nWhich ONE of the "
        "following CORRECTLY places the solutions in order of INCREASING pH?",
        ["H₂CO₃ ; HNO₃ ; NH₃ ; NaOH", "HNO₃ ; H₂CO₃ ; NH₃ ; NaOH", "NaOH ; NH₃ ; H₂CO₃ ; HNO₃", "HNO₃ ; H₂CO₃ ; NaOH ; NH₃"], 1,
        ["The lowest pH comes first: the strong acid.", "Strong acid, weak acid, weak base, strong base."]),
    mcq("1.9", "A galvanic cell consists of the following half-cells:\nFe³⁺(aq)|Fe²⁺(aq)\nNi²⁺(aq)|Ni(s)\nWhich ONE of the following statements is "
        "CORRECT for this cell?",
        ["Ni²⁺ is reduced and Fe²⁺ is oxidised.", "Ni²⁺ is oxidised and Fe³⁺ is reduced.", "Pt is the electrode at the cathode.",
         "Ni is the electrode at the cathode."], 2,
        ["Table 4 of the data sheets: Fe³⁺ (+0,77 V) is a stronger oxidising agent than Ni²⁺ (−0,27 V).", "The Fe³⁺|Fe²⁺ half-cell has no solid metal: what electrode does it need?"]),
    mcq("1.10", "The set-up for electroplating an iron medal with silver is shown in the simplified diagram below. Which ONE of the following "
        "combinations for the ANODE and REACTION AT THE CATHODE is CORRECT?",
        ["Iron medal; Ag⁺(aq) + e⁻ → Ag(s)", "Silver rod; Fe²⁺(aq) + 2e⁻ → Fe(s)", "Iron medal; Ag(s) → Ag⁺(aq) + e⁻", "Silver rod; Ag⁺(aq) + e⁻ → Ag(s)"], 3,
        ["Silver ions are reduced on the object being plated.", "The silver rod dissolves to supply Ag⁺: oxidation, at the anode."],
        optTable={"head": ["ANODE", "REACTION AT THE CATHODE"],
                  "rows": [["Iron medal", "Ag⁺(aq) + e⁻ → Ag(s)"], ["Silver rod", "Fe²⁺(aq) + 2e⁻ → Fe(s)"], ["Iron medal", "Ag(s) → Ag⁺(aq) + e⁻"],
                           ["Silver rod", "Ag⁺(aq) + e⁻ → Ag(s)"]]},
        figure=fig("1.10", "A container of electrolyte with two electrodes wired to a power source above it: an iron medal on the left and a "
                   "silver rod on the right.")),
]

# ---- QUESTION 2, the question paper pages 7-8 and the memo pages 2-5 ----
q2 = [
    mcq("2.1.1", "Write down the LETTER that represents an alcohol.", LETTERS, 3,
        ["An alcohol has an –OH group: read the formulas as well as the drawings.", "C₄H₁₀O fits CₙH₂ₙ₊₁OH."], marks=1),
    pick("2.1.2", "Write down the LETTERS that represent TWO compounds that are functional isomers of one another.", LETTERS, [0, 2], 1,
         ["Functional isomers: the same molecular formula, different functional groups.", "Count the C, H and O atoms of the compounds with a C=O."]),
    pick("2.1.3", "Write down the LETTERS that represent TWO compounds that belong to the same homologous series.", LETTERS, [4, 5], 1,
         ["A homologous series shares one general formula.", "Which two fit CₙH₂ₙ₊₂?"]),
    term("2.2.1", "Write down the IUPAC name of compound A.", ["3-methylbutan-2-one", "3-methylbutanone", "3-methyl-2-butanone", "methylbutanone"],
         ["The longest chain holding the C=O has four carbons: a butanone.", "Number from the end nearest the C=O, then place the methyl."], marks=3, strict=True),
    term("2.2.2", "Write down the IUPAC name of compound B.", ["2,6-dichloro-2,5-dimethylheptane"],
         ["Find the LONGEST chain: it runs up into the branch.", "Number for the lowest locants; name the substituents in alphabetical order (chloro before methyl)."],
         marks=3, strict=True),
    term("2.2.3", "Write down the IUPAC name of compound G.", ["3-ethyl-2-methylhex-2-ene", "3-ethyl-2-methyl-2-hexene"],
         ["The longest chain must contain the double bond.", "Number from the end nearest the double bond; ethyl before methyl."], marks=3, strict=True),
    draw("2.2.4", "Write down the STRUCTURAL FORMULAE of two STRAIGHT CHAIN positional isomers of compound D.", 4, [
        ["Butan-1-ol: the hydroxyl group on the 1st C-atom", 1], ["Butan-1-ol: whole structure correct, every atom and bond shown", 1],
        ["Butan-2-ol: the hydroxyl group on the 2nd C-atom", 1], ["Butan-2-ol: whole structure correct, every atom and bond shown", 1]],
        ["D, C₄H₁₀O, is an alcohol: draw a straight chain of four carbons.", "Positional isomers: move the –OH to another carbon."],
        memo="H–O–CH₂–CH₂–CH₂–CH₃ and CH₃–CH(OH)–CH₂–CH₃, every bond drawn. More than one functional group or a wrong functional group: 0/2 "
             "per molecule. Condensed structural formulae used: max 2/4. The bond between O and H not shown: accept.")]
q2c = [
    term("2.3.1", "Write down the name for this type of reaction.", ["Combustion", "Oxidation", "Combustion reaction", "Oxidation reaction"],
         ["A hydrocarbon reacts with oxygen.", "It forms CO₂ and H₂O and releases heat."]),
    steps("2.3.2", "Calculate the TOTAL volume of the GASES present in the container at the end of the reaction.", 5, [
        ("Volume of O₂ used (cm³)", 1, 40, 0.5, "V(O₂) used = 5V(C₃H₈) = (5)(8) ✓ (a) = 40 cm³"),
        ("Volume of CO₂ and H₂O formed together (cm³)", 1, 56, 0.5, "V(CO₂) = 3V(C₃H₈) = (3)(8) = 24 cm³; V(H₂O) = 4V(C₃H₈) = (4)(8) = 32 cm³ ✓ (b)"),
        ("Volume of O₂ left over (cm³)", 1, 10, 0.5, "V(O₂) unused = 50 − 40 ✓ (c) = 10 cm³ (the subtraction not shown: the mark for 10 cm³)"),
        ("Total volume of the gases at the end (cm³)", 2, 66, 0.5, "Total = 10 + 24 + 32 ✓ (d) = 66 cm³ ✓ (e) (or 0,066 dm³). Moles with 22,4 dm³·mol⁻¹ "
         "or any molar gas volume: accepted.")],
        ["Gas volumes react in the ratio of the coefficients: 1 : 5 : 3 : 4.", "Oxygen is in excess: add the O₂ left over to the products' volumes."])]

# ---- QUESTION 3, the question paper page 9 and the memo page 6 ----
q3 = [
    rub("3.1", "Define the term homologous series.", 1, [
        "A series of organic compounds that can be described by the same general formula. (1 or 0)",
        "OR — A series of organic compounds in which one member differs from the next by a CH₂ group. (1 or 0)"],
        ["Its members share one general formula.", "Each member differs from the next by one CH₂."]),
    lst("3.2", "Identify the TWO homologous series to which these compounds belong.", 2, [["Ester", "Esters"], ["Carboxylic acid", "Carboxylic acids"]],
        ["C₄H₈O₂ has two oxygens: a –COO– group.", "One has –COOH; in the other the –COO– sits between two carbon chains."]),
    draw("3.3.1", "Write down the STRUCTURAL FORMULA of compound A.", 2, [
        ["Functional group correct: the carboxyl group, –COOH (C=O and C–O–H)", 1],
        ["Whole structure correct: butanoic acid, CH₃–CH₂–CH₂–COOH, every atom and bond shown", 1]],
        ["A has the lower vapour pressure: the stronger forces between its molecules.", "Which of the two series forms hydrogen bonds?"]),
    term("3.3.2", "Write down the IUPAC name for a possible compound B.", ["Methyl propanoate", "Propyl methanoate", "Ethyl ethanoate"],
         ["B is the ester: four carbons in all.", "Name the alcohol's part (…yl) first, then the acid's part (…oate)."], marks=2, strict=True),
    term("3.4.1", "Write down the strongest type of Van der Waals forces between the molecules in compound A.",
         ["Hydrogen bonds", "Hydrogen bonding", "Hydrogen bond", "H-bonds"],
         ["A's carboxyl group has an H bonded to an O.", "The strongest of the intermolecular forces."]),
    term("3.4.2", "Write down the strongest type of Van der Waals forces between the molecules in compound B.",
         ["Dipole-dipole forces", "Dipole-dipole", "Dipole-dipole interactions"],
         ["An ester is polar but has no H on an O.", "Polar molecules without hydrogen bonds attract by ..."]),
    rub("3.5", "Which compound, A or B, has a higher boiling point? Give a reason for the answer by referring to the strength of the intermolecular "
        "forces.", 2, [
        "A. (1)",
        "The hydrogen bond (in A) is stronger than the dipole-dipole force (in B) / the dipole-dipole force is weaker than the hydrogen bonds / "
        "compound A has stronger intermolecular forces (than B) / compound B has weaker intermolecular forces (than A). (1)"],
        ["Stronger forces between molecules need more energy to overcome.", "Compare hydrogen bonds with dipole-dipole forces."]),
    mcq("3.6", "The boiling point of compound A is measured again on another day when the atmospheric pressure is much lower. How will the boiling "
        "point of this compound now be affected? Choose from INCREASES, DECREASES or REMAINS THE SAME.", CHANGE, 1,
        ["A liquid boils when its vapour pressure equals the pressure outside.", "A lower outside pressure is reached at a lower temperature."], marks=1)]

# ---- QUESTION 4, the question paper page 10 and the memo pages 7-8 ----
q4a = [
    term("4.1.1", "Write down the IUPAC name of compound W.", ["2-bromobutane"],
         ["W + NaOH(aq) gives butan-2-ol: the –OH takes the place of one atom.", "Which haloalkane gives butan-2-ol?"], marks=2, strict=True),
    term("4.1.2", "Write down the NAME or FORMULA of R.", ["NaBr", "Sodium bromide"],
         ["Br leaves W; Na comes from the NaOH.", "The inorganic product is a salt."], strict=True),
    lst("4.1.3", "Write down TWO names for the type of reaction in reaction I.", 2, [["Addition"], ["Hydrohalogenation", "Hydrobromination"]],
        ["HBr adds across a double bond.", "Name it by what is added: hydrogen and a halogen."]),
    term("4.1.4", "Write down the NAME or FORMULA of S.", [
        "Sulphuric acid", "Sulfuric acid", "Concentrated sulphuric acid", "Concentrated sulfuric acid", "H2SO4", "Concentrated H2SO4", "Conc H2SO4",
        "Phosphoric acid", "Concentrated phosphoric acid", "H3PO4", "Concentrated H3PO4", "Conc H3PO4"],
         ["Reaction III removes water from an alcohol: dehydration.", "Its catalyst is a concentrated acid."], strict=True),
    draw("4.1.5", "Write down the STRUCTURAL formula of compound T.", 2, [
        ["Correct functional group: the C=C double bond, between the 2nd and 3rd carbons", 1],
        ["Whole structure correct: but-2-ene, CH₃–CH=CH–CH₃, every atom and bond shown", 1]],
        ["Dehydrating butan-2-ol: the major product.", "The double bond forms towards the carbon with fewer hydrogens."],
        memo="More than one functional group or a wrong functional group: 0/2. A correct condensed formula: max 1/2."),
    term("4.1.6", "Compound W can be converted to compound T in one step. State, besides heat, ONE other reaction condition for this conversion.", [
        "Concentrated strong base", "Concentrated NaOH", "Concentrated KOH", "Concentrated LiOH", "Concentrated sodium hydroxide",
        "Concentrated potassium hydroxide", "Concentrated lithium hydroxide", "Concentrated strong base in ethanol", "Concentrated NaOH in ethanol",
        "Concentrated KOH in ethanol"],
         ["W to T removes HBr: elimination.", "The base must be strong and NOT dilute."])]
q4b = [
    rub("4.2.1", "Define the term cracking.", 2, [
        "The chemical process/reaction in which longer chain hydrocarbon/alkane molecules are broken down to shorter (more useful) molecules. (2)",
        "Key phrases: longer chain hydrocarbon/alkane molecules; broken down; shorter molecules. A key phrase omitted (in the correct context): deduct 1."],
        ["It splits big molecules.", "Long-chain alkanes become ..."]),
    term("4.2.2", "State ONE change, besides a change in temperature, that will be observed when the mixture is bubbled in Br₂(aq).", [
        "Decolourisation", "The colour fades", "Becomes lighter in colour", "Colourless", "Decolourises", "The bromine water decolourises",
        "Turns colourless", "The bromine water becomes colourless", "Decolorisation", "The brown colour fades", "The orange colour fades"],
         ["Bromine water is orange-brown.", "Bromine is used up as it adds across a double bond."]),
    draw("4.2.3", "Write down the STRUCTURAL FORMULA of X.", 2, [
        ["Correct functional group: a C=C double bond", 1], ["Whole structure correct: propene, CH₂=CH–CH₃, every atom and bond shown", 1]],
        ["Balance the atoms: C₁₀H₂₂ − C₄H₁₀ leaves 2X.", "X is C₃H₆, with one double bond."]),
    rub("4.2.4", "Which compound, X or C₄H₁₀, reacts faster with Br₂(aq)? Explain the answer.", 3, [
        "X / C₃H₆ / propene. (1)", "X is unsaturated / has a double bond / is an alkene. (1)",
        "ANY ONE: X undergoes addition / alkenes are more reactive than alkanes / unsaturated compounds react faster than saturated compounds / "
        "an addition reaction is faster than substitution / an addition reaction does not need UV/light. (1)"],
        ["One product is an alkene, the other an alkane.", "In the dark, an alkane hardly reacts with bromine."])]

# ---- QUESTION 5, the question paper pages 11-12 and the memo pages 9-12 ----
q5a = [
    rub("5.1", "Define the term reaction rate.", 2, [
        "ANY ONE: the change in concentration of products/reactants per (unit) time; the change in amount/number of moles/volume/mass of products or "
        "reactants per (unit) time; the amount/number of moles/volume/mass of products formed/reactants used per (unit) time; the rate of change in "
        "concentration/amount/number of moles/volume/mass. (2 or 0)", "Give the mark for 'per unit time' only in the context of reaction rate."],
        ["How quickly something changes.", "A change in amount or concentration, divided by time."], each=2),
    mcq("5.2.1", "At which time, 10 s or 30 s, is the reaction rate higher?", ["10 s", "30 s"], 0,
        ["The rate is the steepness of the curve.", "Where is the graph steeper?"], marks=1),
    steps("5.2.2", "The reaction takes place in a 3 dm³ container. Calculate the average rate (in mol·s⁻¹) at which CO₂(g) is formed in the first 10 s.", 5, [
        ("Decrease in the concentration of O₂ in the first 10 s (mol·dm⁻³)", 1, 0.11, 0.011,
         "Δc(O₂) = [O₂]final − [O₂]initial = 0,15 − 0,27 ✓ (a) (accept 0,265 to 0,27 for [O₂]initial)"),
        ("Average rate at which O₂ is used (mol·dm⁻³·s⁻¹)", 1, 0.011, 0.0011, "Rate = −Δc(O₂)/Δt = −(0,15 − 0,27)/(10 − 0) ✓ (b) = 0,012 mol·dm⁻³·s⁻¹"),
        ("Average rate at which O₂ is used (mol·s⁻¹)", 1, 0.033, 0.0033, "Rate(O₂) = cV = (0,012)(3) ✓ (c) = 0,036 mol·s⁻¹"),
        ("Average rate at which CO₂ is formed (mol·s⁻¹)", 2, 0.066, 0.0066, "Rate(CO₂) = 2 × rate(O₂) ✓ (d) = 2 × 0,036 = 0,072 mol·s⁻¹ ✓ (e). Range: "
         "0,06 – 0,072. (OR Δn(O₂) = 0,12 × 3 = 0,36 mol; Δn(CO₂) = 2(0,36) = 0,72 mol; rate = 0,72/10.)")],
        ["Read [O₂] at 0 s and at 10 s from the graph.", "For mol·s⁻¹, multiply by the 3 dm³; then the mole ratio O₂ : CO₂ = 1 : 2."]),
    mcq("5.2.3", "Which reactant is in excess, CO or O₂?", ["CO", "O₂"], 1,
        ["Look at the end of the graph: does the O₂ run out?", "The [O₂] levels off above zero."], marks=1),
    rub("5.2.4", "This reaction was repeated using a smaller sealed container. How will this affect the magnitude of the gradient of the graph at the "
        "beginning of the reaction? Choose from INCREASES, DECREASES or REMAINS THE SAME. Give a reason for the answer.", 2, [
        "Increases. (1)", "A higher reaction rate / the concentration of the reactants is higher. ACCEPT: the pressure increased. (1)"],
        ["The same amounts of gas in a smaller volume.", "A higher concentration: more collisions per second."])]
q5b = [
    mcq("5.3.1", "Was there a net release or net absorption of energy during the REVERSE reaction?", ["Net release", "Net absorption"], 1,
        ["ΔH < 0: the forward reaction is exothermic.", "The reverse reaction does the opposite."], marks=1),
    rub("5.3.2", "Define the term activated complex.", 2, [
        "Unstable (high energy) transition state from reactants to products. ACCEPT: between reactants and products. (2)",
        "Key phrases: unstable (high energy); transition state; from reactants to products. A key phrase omitted (in the correct context): deduct 1."],
        ["It exists only at the top of the energy barrier.", "A short-lived state between reactants and products."]),
    rub("5.3.3", "A catalyst, vanadium pentoxide, is added to the reaction. Explain, in terms of the collision theory, why the rate of the reaction "
        "will increase.", 3, [
        "The catalyst provides an alternative path with a lower activation energy / lowers the activation energy. (1)",
        "More particles have sufficient (kinetic) energy / kinetic energy greater than (or equal to) the activation energy. (1)",
        "More effective collisions per unit time/second / a higher frequency of effective collisions. (1)"],
        ["What does a catalyst change about the energy barrier?", "Then: how many particles get over it, and how often do they collide effectively?"]),
    mcq("5.3.4", "More SO₂(g) is now added to the container at constant temperature. How will this change affect the heat of the reaction? Choose "
        "from INCREASES, DECREASES or REMAINS THE SAME.", CHANGE, 2,
        ["ΔH is fixed by the bonds broken and formed.", "Adding a reactant changes how much reacts, not the energy per mole of reaction."], marks=1),
    draw("5.3.5", "More SO₂(g) is now added to the container at constant temperature. Redraw the above graph in the ANSWER BOOK. On the same set of "
         "axes, draw the curve that will now be obtained. Label this as curve Y.", 2, [
        ["Both curves start at the origin and have the correct shape, with their peaks at the same Eₖ", 1],
        ["The peak of curve Y is higher than that of curve X, at the same Eₖ", 1]],
        ["The temperature is the same: the peak stays at the same kinetic energy.", "More particles: the whole curve is taller."],
        memo="Both curves not labelled: 0/2. The curves cross at any point other than the origin: max 1/2. Curve Y drawn lower than curve X: max 1/2.")]

# ---- QUESTION 6, the question paper page 13 and the memo pages 13-16 ----
q6a = [
    rub("6.1.1", "State Le Chatelier's principle.", 2, [
        "When the equilibrium in a closed system is disturbed, the system will re-instate a new equilibrium by favouring the reaction that will "
        "cancel/oppose the disturbance. (2)",
        "Key phrases: equilibrium in a closed system disturbed; re-instate a new equilibrium; favouring the reaction that cancels/opposes the "
        "disturbance. A key phrase omitted (in the correct context): deduct 1."],
        ["It is about a closed system at equilibrium being disturbed.", "The system responds to oppose the change."]),
    mcq("6.1.2", "A few drops of concentrated hydrochloric acid, HCℓ(conc.), are added to the equilibrium mixture. What effect does this addition "
        "have on the mass of Ca(OH)₂(s)? Choose from INCREASES, DECREASES or REMAINS THE SAME.", CHANGE, 1,
        ["H⁺ from the acid reacts with OH⁻.", "Less OH⁻: which way does the equilibrium shift?"], marks=1),
    rub("6.1.3", "Explain the answer to QUESTION 6.1.2 by using Le Chatelier's principle.", 2, [
        "A decrease in the amount/concentration of OH⁻ ions favours the reaction that increases the amount/concentration of OH⁻ ions. OR The "
        "acid/HCℓ/H⁺ reacts with OH⁻ ions. (1)",
        "The forward reaction is favoured. OR The amount/concentration of the products increases. (1)"],
        ["The acid removes a product.", "The system replaces it: which reaction is favoured, and what happens to the solid?"])]
q6b = [
    mcq("6.2.1", "Is the decomposition of NH₄HS(s) an EXOTHERMIC or ENDOTHERMIC reaction?", ["Exothermic", "Endothermic"], 1,
        ["Kc grows as the temperature rises.", "A larger Kc means more products; heating favours the endothermic direction."], marks=1),
    rub("6.2.2", "Explain the answer to QUESTION 6.2.1 by using Le Chatelier's principle.", 3, [
        "With an increase in the temperature the Kc value increases. (1)",
        "The concentration of the products increases / the concentration of the reactants decreases / the forward reaction is favoured. (1)",
        "(According to Le Chatelier's principle) an increase in temperature favours the endothermic reaction. (1)"],
        ["Start from the table: what does Kc do as the temperature rises?", "Which reaction does a rise in temperature favour?"]),
    steps("6.2.3", "Calculate the mass of NH₄HS(s) that will be present at equilibrium at 250 °C.", 8, [
        ("Initial amount of NH₄HS (mol)", 1, 1.37, 0.01, "n = m/M = 70/51 ✓ (a) = 1,37 mol"),
        ("Equilibrium concentration of NH₃, equal to that of H₂S (mol·dm⁻³)", 2, 0.424, 0.005,
         "Kc = [NH₃][H₂S] ✓ (d) (the solid is left out); 18 × 10⁻² = x² ✓ (e); x = 0,424 mol·dm⁻³"),
        ("Amount of NH₄HS that decomposed (mol)", 2, 1.27, 0.012,
         "NH₄HS : NH₃ : H₂S = 1 : 1 : 1 ✓ (b); n(NH₃) = cV = (0,424)(3) ✓ (c) = 1,27 mol, so 1,27 mol NH₄HS decomposed"),
        ("Amount of NH₄HS left at equilibrium (mol)", 1, 0.104, 0.007,
         "n(NH₄HS)eq = n(NH₄HS)in − n(NH₄HS)change = 1,37 − 1,27 ✓ (f) = 0,1 mol (0,098 – 0,11 by the memo's options)"),
        ("Mass of NH₄HS present at equilibrium (g)", 2, 5.345, 0.4,
         "m = nM = (0,11)(51) ✓ (g) = 5,61 g ✓ (h) (the memo's options also give 5,1 g, 4,998 g, 5,128 g and 5,74 g). Range: 4,96 – 5,74 g. "
         "A wrong Kc expression: max 6/8; no Kc expression but a correct substitution: max 7/8.")],
        ["Only the gases appear in Kc: Kc = [NH₃][H₂S], and the two are equal.", "Turn the concentration into moles (× 3 dm³), subtract from the "
         "initial moles, then m = nM with M = 51 g·mol⁻¹."])]

# ---- QUESTION 7, the question paper page 14 and the memo pages 17-20 ----
q7a = [
    rub("7.1.1", "Which one is the stronger acid, H₂PO₄⁻ or HPO₄²⁻? Give a reason for the answer by referring to the data above.", 2, [
        "H₂PO₄⁻. (1)", "The Ka of H₂PO₄⁻ is greater/higher than the Ka of HPO₄²⁻. ACCEPT: the Ka of H₂PO₄⁻ is greater. (1)"],
        ["A stronger acid ionises more.", "Compare the Ka values of the second and third steps."]),
    term("7.1.2", "Write down the FORMULA for the conjugate base of H₂PO₄⁻(aq).", ["HPO4 2−", "HPO4^2-", "HPO42-", "HPO4(2-)"],
         ["A conjugate base is the acid less one H⁺.", "Take away one H and add one negative charge."], strict=True),
    term("7.1.3", "Identify a substance behaving as an ampholyte in the reactions above.", [
        "H2PO4−", "HPO4 2−", "HPO4^2-", "Dihydrogen phosphate", "Dihydrogen phosphate ion", "Hydrogen phosphate", "Hydrogen phosphate ion"],
         ["An ampholyte is an acid in one reaction and a base in another.", "Find a species that is a product in one step and a reactant in the next."], strict=True),
    mcq("7.1.4", "Sodium hydrogen phosphate, Na₂HPO₄(s), is dissolved in water. Will the resulting solution be ACIDIC or BASIC?", ["Acidic", "Basic"], 1,
        ["HPO₄²⁻ gives up H⁺ very little (its Ka is tiny), but it can also take H⁺.", "If it takes H⁺ from water, which ion is left?"], marks=1),
    rub("7.1.5", "Sodium hydrogen phosphate, Na₂HPO₄(s), is dissolved in water. Write a balanced equation to explain the answer to QUESTION 7.1.4.", 3, [
        "Reactants: HPO₄²⁻(aq) + H₂O(ℓ), or Na₂HPO₄(aq) + H₂O(ℓ). (1)",
        "Products: H₂PO₄⁻(aq) + OH⁻(aq), or NaH₂PO₄(aq) + NaOH(aq), or H₂PO₄⁻(aq) + 2Na⁺(aq) + OH⁻(aq). (1)",
        "Balancing: HPO₄²⁻(aq) + H₂O(ℓ) ⇌ H₂PO₄⁻(aq) + OH⁻(aq). Ignore → and phases (marking rule 6.3.10). (1)",
        "OR — Reactants: HPO₄²⁻(aq) + 2H₂O(ℓ), or Na₂HPO₄(aq) + 2H₂O(ℓ). (1)",
        "Products: H₃PO₄(aq) + 2OH⁻(aq), or H₃PO₄(aq) + 2Na⁺(aq) + 2OH⁻(aq), or H₃PO₄(aq) + 2NaOH(aq). (1)",
        "Balancing: HPO₄²⁻(aq) + 2H₂O(ℓ) ⇌ H₃PO₄(aq) + 2OH⁻(aq). (1)"],
        ["HPO₄²⁻ acts as a base here: it takes H⁺ from water.", "Which ion is left over that makes the solution basic?"])]
q7b = [
    steps("7.2.1", "Calculate the final concentration of the hydroxide ions in the flask.", 4, [
        ("Final concentration of OH⁻ ions in the flask (mol·dm⁻³)", 4, 0.041, 0.0011,
         "pH = −log[H₃O⁺] ✓ (a); 12,62 = −log[H₃O⁺] ✓ (b); [H₃O⁺] = 2,4 × 10⁻¹³; (2,4 × 10⁻¹³)[OH⁻] = 1 × 10⁻¹⁴ ✓ (c); [OH⁻] = 0,0417 mol·dm⁻³ ✓ (d). "
         "OR pH + pOH = 14: pOH = 1,38 = −log[OH⁻]; [OH⁻] = 0,042 mol·dm⁻³. Range: 0,04 – 0,042")],
        ["pH + pOH = 14 at 25 °C.", "[OH⁻] = 10^(−pOH)."]),
    steps("7.2.2", "Calculate the number of moles of Ba(OH)₂ used to prepare the 100 cm³ solution.", 8, [
        ("Moles of HCℓ added (mol)", 1, 3e-3, 0.05e-3, "n(HCℓ) = cV = (0,2)(0,015) ✓ (a) = 3 × 10⁻³ mol"),
        ("Moles of OH⁻ that reacted with the HCℓ (mol)", 1, 3e-3, 0.05e-3,
         "n(OH⁻) : n(HCℓ) = 1 : 1 ✓ (b): 3 × 10⁻³ mol (OR n(Ba(OH)₂) = ½ n(HCℓ) = 1,5 × 10⁻³ mol)"),
        ("Moles of OH⁻ left in the flask (mol)", 1, 1.64e-3, 0.045e-3, "n(OH⁻)final = cV = (0,0417)(0,04) ✓ (c) = 1,67 × 10⁻³ mol (the flask holds 40 cm³)"),
        ("Moles of OH⁻ in the 25 cm³ before the HCℓ was added (mol)", 2, 4.64e-3, 0.05e-3,
         "n(OH⁻)ini = n(OH⁻) reacted with HCℓ + n(OH⁻)final = 3 × 10⁻³ + 1,67 × 10⁻³ ✓✓ (d) = 4,67 × 10⁻³ mol"),
        ("Moles of Ba(OH)₂ in the 25 cm³ (mol)", 1, 2.32e-3, 0.025e-3, "n(Ba(OH)₂) : n(OH⁻) = 1 : 2 ✓ (e): ½(4,67 × 10⁻³) = 2,33 × 10⁻³ mol"),
        ("Moles of Ba(OH)₂ used to prepare the 100 cm³ (mol)", 2, 9.28e-3, 0.085e-3,
         "In 100 cm³ = (4)(2,33 × 10⁻³) ✓ (f) = 9,34 × 10⁻³ mol ✓ (g). Range: 9,2 × 10⁻³ – 9,36 × 10⁻³ (positive marking from 7.2.1)")],
        ["The flask holds 25 + 15 = 40 cm³, and OH⁻ is left over (pH 12,62).", "OH⁻ at the start = OH⁻ used by the HCℓ + OH⁻ left. Each Ba(OH)₂ "
         "gives 2 OH⁻, and the 100 cm³ holds 4 times the 25 cm³."])]

# ---- QUESTION 8, the question paper page 15 and the memo pages 20-21 ----
q8 = [
    rub("8.1", "Define the term electrolyte.", 2, [
        "ANY ONE: a substance whose (aqueous) solution contains ions; a substance that dissolves in water to give a solution that conducts electricity "
        "(through the movement of ions); a substance that dissociates to form ions in water/in the molten state. (2 or 0)"],
        ["It is about ions.", "Dissolved or molten, it conducts because of ..."], each=2),
    rub("8.2", "Which ion concentration, Aℓ³⁺(aq) or Zn²⁺(aq), will increase? Give a reason for the answer.", 2, [
        "Aℓ³⁺ / the aluminium ion. (1)", "Aℓ is oxidised OR Aℓ is a stronger reducing agent. (1)"],
        ["Table 4 of the data sheets: Aℓ (−1,66 V) against Zn (−0,76 V).", "The metal that is oxidised forms more of its ions."]),
    term("8.3", "Write down the cell notation for this cell.", [
        "Al(s) | Al3+(aq) || Zn2+(aq) | Zn(s)", "Al | Al3+ || Zn2+ | Zn", "Al(s) | Al3+ || Zn2+ | Zn(s)", "Al | Al3+(aq) || Zn2+(aq) | Zn",
        "Al(s) | Al3+ (1 mol·dm-3) || Zn2+(aq) (1 mol·dm-3) | Zn(s)", "Al(s) | Al3+(aq) (1 mol·dm-3) || Zn2+(aq) (1 mol·dm-3) | Zn(s)"],
         ["The anode (oxidation) is written on the left, the cathode on the right, a double line for the salt bridge.", "Aℓ is the anode here."],
         marks=3, strict=True),
    steps("8.4", "Calculate the mass of Aℓ₂(SO₄)₃(s) needed to prepare 250 cm³ of this solution so that the cell operates initially under STANDARD "
          "CONDITIONS.", 4, [
        ("Moles of Aℓ³⁺ needed (mol)", 1, 0.25, 0.005, "n(Aℓ³⁺) = cV = (1)(0,25) ✓ (a) = 0,25 mol (standard conditions: 1 mol·dm⁻³)"),
        ("Moles of Aℓ₂(SO₄)₃ needed (mol)", 1, 0.125, 0.003, "n(Aℓ₂(SO₄)₃) : n(Aℓ³⁺) = 1 : 2 ✓ (b): ½(0,25) = 0,125 mol"),
        ("Mass of Aℓ₂(SO₄)₃ needed (g)", 2, 42.75, 0.05, "n = m/M: 0,125 = m/342 ✓ (c); m = 42,75 g ✓ (d) (OR c = m/MV: 1 = m/(0,25)(342), m = 85,5 g; "
         "½(85,5) = 42,75 g)")],
        ["Standard conditions: [Aℓ³⁺] = 1 mol·dm⁻³.", "Each Aℓ₂(SO₄)₃ gives 2 Aℓ³⁺; M(Aℓ₂(SO₄)₃) = 342 g·mol⁻¹."])]

# ---- QUESTION 9, the question paper page 16 and the memo page 22 ----
q9 = [
    mcq("9.1", "Is this an ELECTROLYTIC or a GALVANIC cell?", ["Electrolytic", "Galvanic"], 0,
        ["Is a battery driving the reaction?", "A cell that uses electrical energy to cause a reaction is ..."], marks=1),
    mcq("9.2.1", "How will the concentration of the zinc ions in the electrolyte be affected during the refining of the copper? Choose from "
        "INCREASES, DECREASES or REMAINS THE SAME.", CHANGE, 0,
        ["The impure copper's zinc is oxidised too.", "Zn²⁺ is a weaker oxidising agent than Cu²⁺: is it reduced at the cathode?"], marks=1),
    rub("9.2.2", "Will the amount of Cu²⁺(aq) ions INCREASE or DECREASE? Explain the answer in terms of the relative strengths of the oxidising agents "
        "present.", 3, [
        "Decrease. (1)", "More copper(II) ions/Cu²⁺ are reduced than formed / only copper(II) ions/Cu²⁺ are reduced. (1)",
        "The copper(II) ion/Cu²⁺ is a stronger oxidising agent than the zinc(II) ion/Zn²⁺ OR Zn²⁺ is a weaker oxidising agent than Cu²⁺. (1)"],
        ["At the anode both Cu and Zn are oxidised; at the cathode only one ion is reduced.", "Which ion, Cu²⁺ or Zn²⁺, is the stronger oxidising agent?"]),
    steps("9.2.3", "Calculate the change in mass of electrode R after T hours.", 6, [
        ("Moles of Zn²⁺ formed (mol)", 1, 0.05, 0.001, "n(Cu²⁺) : n(Zn²⁺) = 1 : 1 ✓ (a): n(Zn²⁺) = n(Cu²⁺) = 0,05 mol"),
        ("Mass of Zn that left electrode R (g)", 2, 3.25, 0.02, "n = m/M ✓ (b); m(Zn) = nM = (0,05)(65) ✓ (c) = 3,25 g"),
        ("Moles of Cu that left electrode R (mol)", 1, 0.1, 0.001, "0,15 − 0,05 ✓ (d) = 0,1 mol Cu"),
        ("Mass of Cu that left electrode R (g)", 1, 6.35, 0.02, "m(Cu) = nM = (0,1)(63,5) ✓ (e) = 6,35 g"),
        ("Magnitude of the change in mass of electrode R (g)", 1, 9.6, 0.02, "Change in mass = 6,35 + 3,25 = 9,6 g ✓ (f) (a decrease). No range.")],
        ["R is the impure copper (the anode): both Zn and Cu leave it as ions.", "The Cu²⁺ fell by 0,05 mol while 0,15 mol Cu was deposited: what made "
         "up the difference?"])]

C_TABLE = {"head": ["", "FORMULA OR NAME"], "rows": [["C", "CH₃CH(CH₃)CH₂CHO"], ["D", "C₄H₁₀O"], ["E", "C₃H₈"], ["F", "Pentane"]]}
VP_TABLE = {"head": ["COMPOUND", "VAPOUR PRESSURE"], "rows": [["A", "0,071 kPa"], ["B", "9,7 kPa"]]}
R_TABLE = {"head": ["", "REACTION"], "rows": [["I", "HBr(g) + T → W"], ["II", "W + NaOH(aq) → CH₃CH(OH)CH₂CH₃ + R"],
                                             ["III", "CH₃CH(OH)CH₂CH₃ → T + H₂O(ℓ), with S written over the arrow"]]}
KC_TABLE = {"head": ["TEMPERATURE (°C)", "Kc"], "rows": [["200", "7,5 x 10⁻²"], ["250", "18 x 10⁻²"], ["300", "40 x 10⁻²"]]}
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Organic molecules", "marks": 16,
     "lead": "The letters A to G in the table below represent organic compounds.", "table": C_TABLE,
     "figure": fig("Q2", "A table of seven organic compounds. A: a structural formula, CH₃–CO–CH(CH₃)–CH₃ (a C=O on the second carbon and a CH₃ "
                   "branch down from the third). B: a structural formula, a horizontal chain of six carbons: a CH₃; then a carbon with a Cℓ below "
                   "and a CH₃ above; two CH₂; a carbon with a –CHCℓ–CH₃ branch above; a CH₃. C: CH₃CH(CH₃)CH₂CHO. D: C₄H₁₀O. E: C₃H₈. F: Pentane. "
                   "G: a structural formula, CH₃–CH₂–C=C–CH₃ with a CH₃ above the fourth carbon and a –CH₂–CH₂–CH₃ chain below the third."),
     "items": q2},
    {"id": "2.3", "title": "Question 2.3", "kind": "Combustion", "marks": 6,
     "lead": "Compound E, C₃H₈(g), reacts with oxygen, O₂(g), according to the balanced equation:\nC₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(g)\n"
             "Initially 8 cm³ of compound E and 50 cm³ of oxygen were injected into a container of adjustable volume and allowed to react.",
     "figure": fig("Q2.3", "A cylinder with a movable piston, like a syringe; an arrow points to the reaction mixture inside."), "items": q2c},
    {"id": "3", "title": "Question 3", "kind": "Physical properties of organic compounds", "marks": 12,
     "lead": "Two bottles contain compounds A and B with the same molecular formula, C₄H₈O₂. These compounds are straight chain organic molecules that "
             "belong to two different homologous series. The boiling points are used to distinguish between the two compounds.\n\nThe following "
             "are the vapour pressures of these compounds at a given temperature:", "table": VP_TABLE,
     "figure": fig("Q3", "Two stoppered bottles, labelled A and B, each marked C₄H₈O₂."), "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Organic reactions", "marks": 9,
     "lead": "Study the three organic reactions I, II and III below. Compounds T and W are organic compounds. R and S are inorganic substances. "
             "Consider only the major products.", "table": R_TABLE, "items": q4a},
    {"id": "4.2", "title": "Question 4.2", "kind": "Cracking", "marks": 8,
     "lead": "A compound with the formula C₁₀H₂₂ undergoes a cracking reaction according to the equation:\nC₁₀H₂₂(ℓ) → 2X(g) + C₄H₁₀(g)\n"
             "The mixture of the two products is bubbled in bromine water, Br₂(aq), in a darkened room.", "items": q4b},
    {"id": "5", "title": "Question 5", "kind": "Reaction rate", "marks": 11,
     "lead": "Carbon monoxide, CO(g), reacts with oxygen, O₂(g), to form carbon dioxide, CO₂(g), in a sealed container according to the balanced "
             "equation:\n2CO(g) + O₂(g) → 2CO₂(g)\nThe graph below shows the concentration of O₂(g) versus time.",
     "figure": fig("Q5", "Graph of concentration of O₂(g) (mol·dm⁻³), 0 to 0,30, against time (s), 0 to 60, on a fine grid. The curve starts at "
                   "0,27 at 0 s, falls steeply to 0,15 at 10 s, then more and more slowly, to about 0,05 at 30 s, and levels off just above 0,02 "
                   "from about 52 s."), "items": q5a},
    {"id": "5.3", "title": "Question 5.3", "kind": "Energy and the collision theory", "marks": 9,
     "lead": "The reaction between sulphur dioxide, SO₂(g), and oxygen, O₂(g), takes place in a sealed container according to the balanced equation "
             "below.\n2SO₂(g) + O₂(g) ⇌ 2SO₃(g)   ΔH = −196 kJ·mol⁻¹\n\nCurve X is the Maxwell Boltzmann distribution curve for the reaction above.",
     "figure": fig("Q5.3", "Number of particles (up) against kinetic energy (across): curve X rises from the origin to a peak, then falls with a long "
                   "tail to the right."), "items": q5b},
    {"id": "6.1", "title": "Question 6.1", "kind": "Chemical equilibrium", "marks": 5,
     "lead": "Equilibrium is established at 25 °C in a saturated calcium hydroxide solution according to the reaction:\nCa(OH)₂(s) ⇌ Ca²⁺(aq) + 2OH⁻(aq)",
     "items": q6a},
    {"id": "6.2", "title": "Question 6.2", "kind": "The equilibrium constant", "marks": 12,
     "lead": "Initially 70 g of NH₄HS(s) is placed in a 3 dm³ container at 250 °C. The container is sealed and the reaction is allowed to reach "
             "equilibrium according to the balanced equation:\nNH₄HS(s) ⇌ NH₃(g) + H₂S(g)\nThe Kc values for the decomposition of NH₄HS(s) at "
             "different temperatures are given in the table below.", "table": KC_TABLE, "items": q6b},
    {"id": "7.1", "title": "Question 7.1", "kind": "Acids and bases", "marks": 8,
     "lead": "Phosphoric acid, H₃PO₄(aq), is an example of an acid that can ionise in three steps, as shown below.\n"
             "H₃PO₄(aq) + H₂O(ℓ) ⇌ H₃O⁺(aq) + H₂PO₄⁻(aq)   Ka\u00a0=\u00a06,9\u00a0x\u00a010⁻³\nH₂PO₄⁻(aq) + H₂O(ℓ) ⇌ H₃O⁺(aq) + HPO₄²⁻(aq)   Ka\u00a0=\u00a06,2\u00a0x\u00a010⁻⁸\n"
             "HPO₄²⁻(aq) + H₂O(ℓ) ⇌ H₃O⁺(aq) + PO₄³⁻(aq)   Ka\u00a0=\u00a04,8\u00a0x\u00a010⁻¹³", "items": q7a},
    {"id": "7.2", "title": "Question 7.2", "kind": "Neutralisation and pH", "marks": 12,
     "lead": "Barium hydroxide, Ba(OH)₂, dissolves in water according to the balanced equation:\nBa(OH)₂(s) → Ba²⁺(aq) + 2OH⁻(aq)\nA 100 cm³ "
             "solution is prepared by dissolving an unknown amount of Ba(OH)₂ at 25 °C.\n25 cm³ of this Ba(OH)₂ solution is reacted with 15 cm³ of a "
             "0,2 mol·dm⁻³ HCℓ solution in a flask, according to the balanced equation:\nBa(OH)₂(aq) + 2HCℓ(aq) → BaCℓ₂(aq) + 2H₂O(ℓ)\nThe final pH "
             "of the solution is 12,62 at 25 °C.", "items": q7b},
    {"id": "8", "title": "Question 8", "kind": "Galvanic cells", "marks": 11,
     "lead": "The diagram below represents a cell that operates initially under standard conditions.\n\nThe electrolyte in the aluminium half-cell is "
             "prepared by dissolving some aluminium sulphate, Aℓ₂(SO₄)₃(s), in water.",
     "figure": fig("Q8", "Two beakers joined by a salt bridge and, above them, through a voltmeter V: on the left an aluminium electrode (Aℓ) in "
                   "Aℓ³⁺(aq), on the right a zinc electrode (Zn) in Zn²⁺(aq)."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Electrolytic cells", "marks": 11,
     "lead": "The diagram below represents a cell used for the refining of copper. The unrefined copper contains zinc as the only impurity.\n\nWhen the "
             "switch is closed, it is found after T hours that the amount of Cu²⁺(aq) ions in the electrolyte changed by 0,05 moles and 0,15 moles of "
             "Cu(s) were deposited on electrode Q.",
     "figure": fig("Q9", "A battery and a switch wired to two electrodes in one container of electrolyte: electrode Q on the left and electrode R "
                   "on the right."), "items": q9},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Chemistry", "total": 150, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (structural formulae and charges are images); no API call."},
        {"n": "2.1.2", "kind": "no_fit", "detail": "Two letters for one mark (2.1.2, 2.1.3) play as a pick of two, half a mark each; the memo gives "
                                                   "the mark for the pair."},
        {"n": "2.2.1", "kind": "no_fit", "detail": "IUPAC names (2.2.1-2.2.3, 3.3.2, 4.1.1), formulas (4.1.2, 4.1.4, 7.1.2, 7.1.3) and the cell "
                                                   "notation (8.3) play as strict terms: all or nothing, where the memo gives part marks (stem, "
                                                   "substituents, the whole name; a mark per half-cell and the salt bridge). Spacing and "
                                                   "punctuation are not judged, so a missing hyphen or a misplaced bar is not marked down."},
        {"n": "2.2.4", "kind": "no_fit", "detail": "Structural formulae (2.2.4, 3.3.1, 4.1.5, 4.2.3) and the Maxwell-Boltzmann curve (5.3.5) are "
                                                   "drawn on paper and self-checked against the memo's criteria."},
        {"n": "2.3.2", "kind": "no_fit", "detail": "Calculations play as steps: each step is the number the memo's method produces, its formula and "
                                                   "substitution marks riding on that number (the phone sees numbers, not working)."},
        {"n": "7.1.5", "kind": "no_fit", "detail": "A balanced equation is typed as text and marked against the memo's reactants, products and "
                                                   "balancing points by the written-answer marker."},
        {"n": "5.2.2", "kind": "memo_issue", "detail": "A range from the graph reading (0,06 - 0,072 mol·s⁻¹): played as 0,066 ± 0,0066, the earlier "
                                                       "steps' tolerances matching it."},
        {"n": "6.2.3", "kind": "memo_issue", "detail": "The range differs by language: English 4,96 - 5,74 g, Afrikaans 4,95 - 5,74 g. Played as "
                                                       "5,345 ± 0,4 (the memo's bounds inside)."},
        {"n": "7.2.2", "kind": "memo_issue", "detail": "The memo's '(g) in all options' line gives n(Ba(OH)₂) in 100 cm³ = (0,0936)(0,1) = 0,0936 "
                                                       "mol; that product is 0,00936 mol, in line with its stated answer 9,34 x 10⁻³ mol."},
    ],
}
out = Path(__file__).parent / "out" / "ps-p2-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    print(m["id"], "parts:", len(m["items"]), "marks:", sum(i["marks"] for i in m["items"]), "/", m["marks"])
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
