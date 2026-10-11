"""Physical Sciences P2 (Chemistry) Nov 2025, the whole paper (Questions 1 to 9), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper draws its structural formulae
and sets charges as images, so its text layer has gaps.

  python tools/ingest/transcribe_ps_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P2 Nov 2025 Eng.pdf" "<...>/Physical Sciences P2 Nov 2025 MG Afr & Eng.pdf" --id ps-p2-2025-11 --from-json

How the memo's shapes map (Chemistry; the Physics paper's rules hold, see transcribe_ps_p1_2025_11.py):
  an IUPAC name, a formula, a cell notation -> term with strict (one letter is another compound: hexane / hexene, H2SO4 / H2SO3;
  spacing and punctuation free), the memo's part marks played all or nothing; "Write down the LETTER(S)" -> mcq (one letter, or
  six letter pairs where the memo gives one mark for the pair); a choice the paper names (EXOTHERMIC or ENDOTHERMIC, 10 s or 30 s, CO or O2) -> mcq; a STRUCTURAL formula or
  a redrawn curve -> draw, self-checked against the memo's criteria. A charge typed as "2-" is read through its digit only (norm
  drops signs): HPO4 2- needs the 2, H2PO4- cannot check its -.
The rollout rulings (Murci, 2026-10-10): every calculation -> authored multiple choice, `work` (the memo's FIRST working line by
  line + three workings each built from a DIFFERENT real chemistry error, 0 or full marks; no wrong option inside a memo range or
  equal to a value the memo accepts; the right letter spread over A-D); every written answer -> statements (STATEMENTS at the
  bottom): a definition picks 1 card for its marks (the memo's wording right, its OR / ACCEPT form a second right card, the wrong
  ones a key condition dropped or swapped, or another term's definition); an explanation, or a choice with its reason, picks the
  choice card and the memo's points, 1 mark each (the other choices and the reversed reasoning are the wrong cards; where the memo
  gives one mark for "A / B / C" forms, only one form is a card, so two forms can never earn two marks). "Write a balanced
  equation" (7.1.5) -> multiple choice of four equations. No memo here weighs two sides, so no part plays as a sort. A part whose
  stem, options or cards show an earlier part's answer opens only after it (GATES).
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves and checked on a contact sheet."""
import json
import random
import re
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


# notes: the memo's marking notes that are NOT points (key phrases, "per unit time" only in context): never scored, never shown
rub = lambda n, q, marks, bullets, clues, each=None, notes=None: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets,
                                                                 **({"each": each} if each else {}), **({"notes": notes} if notes else {})}
term = lambda n, q, a, clues, marks=1, strict=False: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                      **({"strict": True} if strict else {})}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


WORK = "\n\nChoose the correct working."
AUTHORED = []   # the calculations played as authored multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues, **kw):
    """A calculation as authored multiple choice (Murci, 2026-10-10; transcribe_ml_p2_2025_11.py's helper): opts are the memo's
    FIRST working and three workings built from real chemistry errors, one step a line, a fraction {numerator}/{denominator}; the
    part keeps its marks, all or nothing. kw: catalogue extras."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


LETTERS = ["A", "B", "C", "D", "E", "F", "G"]
P = lambda a, b: "Compounds %s and %s" % (a, b)   # a pair of letters as an option ("C · A and C" would read as one letter)
CHANGE = ["Increases", "Decreases", "Remains the same"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which ONE of the following is the name of the functional group of propan-1-ol?", ["Carboxyl", "Carbonyl", "Hydroxyl", "Formyl"], 2,
        ["Propan-1-ol is an alcohol.", "Name the –OH group."]),
    mcq("1.2", "The organic compound C₂H₄ is converted to an alkane as shown by the reaction below.\nC₂H₄ → Alkane\nWhich ONE of the following is a "
        "suitable catalyst for this reaction?", ["Lead", "Platinum", "Hydrogen", "Iron"], 1,
        ["Turning an alkene into an alkane adds hydrogen: hydrogenation.", "Hydrogen is a reactant here, not the catalyst; the catalyst is a "
         "transition metal."]),   # (was "such as Pt, Pd or Ni": it named the answer)
    mcq("1.3", "Which of the following statements ALWAYS apply to compounds that are structural isomers of one another?\n(i) They belong to the same "
        "homologous series.\n(ii) They have the same structural formula.\n(iii) They have the same molecular formula.",
        ["(iii) only", "(i) and (iii) only", "(i) and (ii) only", "(i), (ii) and (iii)"], 0,
        ["Recall the definition: what must structural isomers share, and what must differ?",
         "An aldehyde and a ketone can have the same molecular formula: are they in the same homologous series?"]),   # (the two
        # clues settled (i), (ii) and (iii) between them)
    mcq("1.4", "Magnesium ribbon of mass 2 g reacts with excess hydrochloric acid of concentration 0,1 mol·dm⁻³ at 20 °C:\nMg(s) + 2HCℓ(aq) → "
        "MgCℓ₂(aq) + H₂(g)\nWhich ONE of the following changes will NOT increase the initial rate of the reaction?",
        ["Using 2 g of powdered magnesium", "Increasing the temperature of HCℓ to 30 °C", "Using a longer piece of the magnesium ribbon",
         "Doubling the volume of the hydrochloric acid used"], 3,
        ["The rate depends on concentration, temperature, surface area and catalysts.", "Which change alters none of these factors?"]),
    # (was "Which change leaves the acid's concentration the same?": all four changes do)
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
        ["The lowest pH comes first.", "Classify each solution: a strong or a weak acid or base?"]),   # (the order was spelt out)
    mcq("1.9", "A galvanic cell consists of the following half-cells:\nFe³⁺(aq)|Fe²⁺(aq)\nNi²⁺(aq)|Ni(s)\nWhich ONE of the following statements is "
        "CORRECT for this cell?",
        ["Ni²⁺ is reduced and Fe²⁺ is oxidised.", "Ni²⁺ is oxidised and Fe³⁺ is reduced.", "Pt is the electrode at the cathode.",
         "Ni is the electrode at the cathode."], 2,
        ["Use Table 4 of the data sheets: which is the stronger oxidising agent, Fe³⁺ or Ni²⁺?",
         "Which half-cell has no solid metal of its own, and what electrode does it need?"]),
    mcq("1.10", "The set-up for electroplating an iron medal with silver is shown in the simplified diagram below. Which ONE of the following "
        "combinations for the ANODE and REACTION AT THE CATHODE is CORRECT?",
        ["Iron medal; Ag⁺(aq) + e⁻ → Ag(s)", "Silver rod; Fe²⁺(aq) + 2e⁻ → Fe(s)", "Iron medal; Ag(s) → Ag⁺(aq) + e⁻", "Silver rod; Ag⁺(aq) + e⁻ → Ag(s)"], 3,
        ["Which electrode must the silver be deposited on?", "Oxidation takes place at the anode, reduction at the cathode."],
        # (the two clues named the anode and the cathode reaction between them)
        optTable={"head": ["ANODE", "REACTION AT THE CATHODE"],
                  "rows": [["Iron medal", "Ag⁺(aq) + e⁻ → Ag(s)"], ["Silver rod", "Fe²⁺(aq) + 2e⁻ → Fe(s)"], ["Iron medal", "Ag(s) → Ag⁺(aq) + e⁻"],
                           ["Silver rod", "Ag⁺(aq) + e⁻ → Ag(s)"]]},
        figure=fig("1.10", "A container of electrolyte with two electrodes wired to a power source above it: an iron medal on the left and a "
                   "silver rod on the right.")),
]

# ---- QUESTION 2, the question paper pages 7-8 and the memo pages 2-5 ----
q2 = [
    mcq("2.1.1", "Write down the LETTER that represents an alcohol.", LETTERS, 3,
        ["An alcohol has an –OH group: read the formulas as well as the drawings.", "Check each molecular formula against CₙH₂ₙ₊₁OH too."],
        marks=1),   # (was "C₄H₁₀O fits CₙH₂ₙ₊₁OH.": it pointed at D)
    # two letters for ONE mark (the memo: "A and C", "E and F", the mark for the pair): multiple choice of six pairs, all or nothing
    # (2026-10-11; a pick of two letters gave half a mark for one right letter, which the memo does not). The wrong pairs are clearly
    # not the answer (different molecular formulae; different homologous series) and neither part offers the other's answer.
    mcq("2.1.2", "Write down the LETTERS that represent TWO compounds that are functional isomers of one another.",
        [P("A", "D"), P("C", "F"), P("A", "C"), P("B", "G"), P("C", "D"), P("A", "F")], 2,
        ["Functional isomers: the same molecular formula, different functional groups.", "Work out the molecular formula of every compound, "
         "then compare them."], marks=1),   # (was "Count the C, H and O atoms of the compounds with a C=O.": only A and C have one)
    mcq("2.1.3", "Write down the LETTERS that represent TWO compounds that belong to the same homologous series.",
        [P("B", "E"), P("D", "E"), P("F", "G"), P("B", "G"), P("E", "F"), P("C", "F")], 4,
        ["A homologous series shares one general formula.", "Find the general formula that each compound fits: which two share one?"],
        marks=1),   # (was "Which two fit CₙH₂ₙ₊₂?": only E and F do)
    term("2.2.1", "Write down the IUPAC name of compound A.", ["3-methylbutan-2-one", "3-methylbutanone", "3-methyl-2-butanone", "methylbutanone"],
         ["Count the carbons in the longest chain that holds the C=O.", "Number from the end nearest the C=O, then place the methyl."], marks=3,
         strict=True),   # (was "... four carbons: a butanone": it gave the memo's stem mark)
    term("2.2.2", "Write down the IUPAC name of compound B.", ["2,6-dichloro-2,5-dimethylheptane"],
         ["Find the LONGEST chain: it runs up into the branch.", "Number for the lowest locants; list the substituents in alphabetical order."],
         marks=3, strict=True),   # (was "... (chloro before methyl)": it named the memo's substituents mark, as 2.2.3's clue did)
    term("2.2.3", "Write down the IUPAC name of compound G.", ["3-ethyl-2-methylhex-2-ene", "3-ethyl-2-methyl-2-hexene"],
         ["The longest chain must contain the double bond.", "Number from the end nearest the double bond; list the substituents in alphabetical "
          "order."], marks=3, strict=True),   # (was "ethyl before methyl": it named the memo's substituents mark)
    draw("2.2.4", "Write down the STRUCTURAL FORMULAE of two STRAIGHT CHAIN positional isomers of compound D.", 4, [
        ["Butan-1-ol: the hydroxyl group on the 1st C-atom", 1], ["Butan-1-ol: whole structure correct, every atom and bond shown", 1],
        ["Butan-2-ol: the hydroxyl group on the 2nd C-atom", 1], ["Butan-2-ol: whole structure correct, every atom and bond shown", 1]],
        ["D, C₄H₁₀O, is an alcohol: draw a straight chain of four carbons.", "Positional isomers: move the –OH to another carbon."],
        memo="H–O–CH₂–CH₂–CH₂–CH₃ and CH₃–CH(OH)–CH₂–CH₃, every bond drawn. More than one functional group or a wrong functional group: 0/2 "
             "per molecule. Condensed structural formulae used: max 2/4. The bond between O and H not shown: accept.")]
q2c = [
    term("2.3.1", "Write down the name for this type of reaction.", ["Combustion", "Oxidation", "Combustion reaction", "Oxidation reaction"],
         ["A hydrocarbon reacts with oxygen.", "It forms CO₂ and H₂O and releases heat."]),
    # the memo's Option 1 (66 cm³; it also accepts 0,066 dm³ and the same total by moles with any molar gas volume)
    work("2.3.2", "Calculate the TOTAL volume of the GASES present in the container at the end of the reaction.", 5, [
        "V(O₂) used = V(C₃H₈)\n= 8 cm³\nV(CO₂) formed = V(C₃H₈)\n= 8 cm³\nV(H₂O) formed = V(C₃H₈)\n= 8 cm³\n"
        "V(O₂) unused = 50 − 8\n= 42 cm³\nTotal volume = 42 + 8 + 8\n= 58 cm³",                                  # the 1 : 5 : 3 : 4 ratio not applied
        "V(O₂) used = 5V(C₃H₈) = (5)(8)\n= 40 cm³\nV(CO₂) formed = 3V(C₃H₈) = (3)(8)\n= 24 cm³\nV(H₂O) formed = 4V(C₃H₈) = (4)(8)\n= 32 cm³\n"
        "V(C₃H₈) unused = 8 − 8\n= 0 cm³\nTotal volume = 24 + 32\n= 56 cm³",                                    # checks the propane: the excess O₂ left out
        "V(O₂) used = 5V(C₃H₈) = (5)(8)\n= 40 cm³\nV(CO₂) formed = 3V(C₃H₈) = (3)(8)\n= 24 cm³\nV(H₂O) formed = 4V(C₃H₈) = (4)(8)\n= 32 cm³\n"
        "V(O₂) unused = 50 − 40\n= 10 cm³\nTotal volume = 10 + 24 + 32\n= 66 cm³",                              # the memo
        "V(O₂) used = 5V(C₃H₈) = (5)(8)\n= 40 cm³\nV(CO₂) formed = 3V(C₃H₈) = (3)(8)\n= 24 cm³\nV(H₂O) formed = 4V(C₃H₈) = (4)(8)\n= 32 cm³\n"
        "V(O₂) unused = 50 − 40\n= 10 cm³\nTotal volume = 10 + 24\n= 34 cm³"], 2,                               # H₂O(g) taken as a liquid: left out
        ["Gas volumes react in the ratio of the coefficients: 1 : 5 : 3 : 4.", "Check which reactant is in excess: is any of it left at the end?"])]

# ---- QUESTION 3, the question paper page 9 and the memo page 6 ----
q3 = [
    rub("3.1", "Define the term homologous series.", 1, [
        "A series of organic compounds that can be described by the same general formula. (1 or 0)",
        "OR — A series of organic compounds in which one member differs from the next by a CH₂ group. (1 or 0)"],
        ["Think of the alkanes: CH₄, C₂H₆, C₃H₈ ... What do they have in common?", "What changes from one member to the next?"]),
    # (the clues were the memo's two answers)
    lst("3.2", "Identify the TWO homologous series to which these compounds belong.", 2, [["Ester", "Esters"], ["Carboxylic acid", "Carboxylic acids"]],
        ["C₄H₈O₂ has two oxygens: a –COO– group.", "Which two homologous series have the general formula CₙH₂ₙO₂?"]),
    # (was "One has –COOH; in the other the –COO– sits between two carbon chains": it described both answers)
    draw("3.3.1", "Write down the STRUCTURAL FORMULA of compound A.", 2, [
        ["Functional group correct: the carboxyl group, –COOH (C=O and C–O–H)", 1],
        ["Whole structure correct: butanoic acid, CH₃–CH₂–CH₂–COOH, every atom and bond shown", 1]],
        ["A has the lower vapour pressure: the stronger forces between its molecules.", "Which of your two homologous series has the stronger "
         "forces between its molecules?"]),   # (was "Which of the two series forms hydrogen bonds?": 3.4.1's answer)
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
        ["A liquid boils when its vapour pressure equals the pressure outside.", "How does the vapour pressure of a liquid change with its "
         "temperature?"], marks=1)]   # (was "A lower outside pressure is reached at a lower temperature.": the answer)

# ---- QUESTION 4, the question paper page 10 and the memo pages 7-8 ----
q4a = [
    term("4.1.1", "Write down the IUPAC name of compound W.", ["2-bromobutane"],
         ["W + NaOH(aq) gives butan-2-ol: the –OH takes the place of one atom.", "Which haloalkane gives butan-2-ol?"], marks=2, strict=True),
    term("4.1.2", "Write down the NAME or FORMULA of R.", ["NaBr", "Sodium bromide"],
         ["In reaction II the –OH of NaOH replaces the halogen atom of W.", "The inorganic product is a salt."], strict=True),
    # (was "Br leaves W; Na comes from the NaOH.": with the salt clue it spelt NaBr)
    lst("4.1.3", "Write down TWO names for the type of reaction in reaction I.", 2, [["Addition"], ["Hydrohalogenation", "Hydrobromination"]],
        ["Reaction I has two reactants and only one product.", "One name is the general type of reaction; the other names what is added."]),
    # (was "HBr adds across a double bond." + "... hydrogen and a halogen.": both names)
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
         ["W to T removes HBr: elimination.", "Compare with reaction II: what must be different about the base for elimination rather than "
          "substitution?"])]   # (was "The base must be strong and NOT dilute.": the answer)
q4b = [
    rub("4.2.1", "Define the term cracking.", 2, [
        "The chemical process/reaction in which longer chain hydrocarbon/alkane molecules are broken down to shorter (more useful) molecules. (2)"],
        ["Compare the size of C₁₀H₂₂ with the size of the products in the equation.", "Are bonds between carbon atoms made or broken?"], each=2,
        notes=["Key phrases: longer chain hydrocarbon/alkane molecules; broken down; shorter molecules. A key phrase omitted (in the correct context): deduct 1."]),
    term("4.2.2", "State ONE change, besides a change in temperature, that will be observed when the mixture is bubbled in Br₂(aq).", [
        "Decolourisation", "The colour fades", "Becomes lighter in colour", "Colourless", "Decolourises", "The bromine water decolourises",
        "Turns colourless", "The bromine water becomes colourless", "Decolorisation", "The brown colour fades", "The orange colour fades"],
         ["Bromine water is orange-brown.", "Bromine is used up as it adds across a double bond."]),
    draw("4.2.3", "Write down the STRUCTURAL FORMULA of X.", 2, [
        ["Correct functional group: a C=C double bond", 1], ["Whole structure correct: propene, CH₂=CH–CH₃, every atom and bond shown", 1]],
        ["Balance the atoms: C₁₀H₂₂ − C₄H₁₀ leaves 2X.", "Find X's molecular formula first: is it an alkane or an alkene?"]),
    rub("4.2.4", "Which compound, X or C₄H₁₀, reacts faster with Br₂(aq)? Explain the answer.", 3, [
        "X OR propene OR C3H6 (C₃H₆). (1)", "X is unsaturated / has a double bond / is an alkene. (1)",
        "ANY ONE: X undergoes addition / alkenes are more reactive than alkanes / unsaturated compounds react faster than saturated compounds / "
        "an addition reaction is faster than substitution / an addition reaction does not need UV/light. (1)"],
        ["Which of the two products is saturated, and which is unsaturated?", "Which type of reaction with bromine needs light, and which does "
         "not?"])]

# ---- QUESTION 5, the question paper pages 11-12 and the memo pages 9-12 ----
q5a = [
    rub("5.1", "Define the term reaction rate.", 2, [
        "ANY ONE: the change in concentration of products/reactants per (unit) time; the change in amount/number of moles/volume/mass of products or "
        "reactants per (unit) time; the amount/number of moles/volume/mass of products formed/reactants used per (unit) time; the rate of change in "
        "concentration/amount/number of moles/volume/mass. (2 or 0)"],
        ["Think of how speed is defined in physics, then apply it to a reaction.", "What changes as a reaction goes on: the reactants and the "
         "products."], each=2,
        notes=["Give the mark for 'per unit time' only in the context of reaction rate."]),
    mcq("5.2.1", "At which time, 10 s or 30 s, is the reaction rate higher?", ["10 s", "30 s"], 0,
        ["The rate is the steepness of the curve.", "Where is the graph steeper?"], marks=1),
    # the memo's Option 1 (0,072 mol·s⁻¹; range 0,06 - 0,072 from the graph reading, [O₂]initial 0,265 - 0,27): every wrong working
    # ends outside that range
    work("5.2.2", "The reaction takes place in a 3 dm³ container. Calculate the average rate (in mol·s⁻¹) at which CO₂(g) is formed in the first "
         "10 s.", 5, [
        "Rate = −{Δc(O₂)}/{Δt}\n= −{0,15 − 0,27}/{10 − 0}\n= 0,012 mol·dm⁻³·s⁻¹\nRate(O₂) = cV = (0,012)(3)\n= 0,036 mol·s⁻¹\n"
        "Rate(CO₂) = 2 × rate(O₂) = 2 × 0,036\n= 0,072 mol·s⁻¹",                                              # the memo
        "Rate = −{Δc(O₂)}/{Δt}\n= −{0,15 − 0,27}/{10 − 0}\n= 0,012 mol·dm⁻³·s⁻¹\nRate(O₂) = cV = (0,012)(3)\n= 0,036 mol·s⁻¹\n"
        "Rate(CO₂) = rate(O₂)\n= 0,036 mol·s⁻¹",                                                             # the 1 : 2 mole ratio not applied
        "Rate = {c(O₂)}/{Δt}\n= {0,15}/{10 − 0}\n= 0,015 mol·dm⁻³·s⁻¹\nRate(O₂) = cV = (0,015)(3)\n= 0,045 mol·s⁻¹\n"
        "Rate(CO₂) = 2 × rate(O₂) = 2 × 0,045\n= 0,09 mol·s⁻¹",                                               # the [O₂] at 10 s, not its change
        "Rate = −{Δc(O₂)}/{Δt}\n= −{0,15 − 0,27}/{10 − 0}\n= 0,012 mol·dm⁻³·s⁻¹\nRate(O₂) = {c}/{V} = {0,012}/{3}\n= 0,004 mol·s⁻¹\n"
        "Rate(CO₂) = 2 × rate(O₂) = 2 × 0,004\n= 0,008 mol·s⁻¹"], 0,                                          # divides by the 3 dm³
        ["The average rate uses the CHANGE in [O₂] over the first 10 s, read from the graph.",
         "Use the balanced equation: how many CO₂ form for each O₂ used?"]),   # (was "multiply by the 3 dm³; then O₂ : CO₂ = 1 : 2": with the
                                                                              # first clue it ruled out every wrong working)
    mcq("5.2.3", "Which reactant is in excess, CO or O₂?", ["CO", "O₂"], 1,
        ["Look at the end of the graph: does the O₂ run out?", "The reactant still left when the reaction stops is in excess."], marks=1),
    # (was "The [O₂] levels off above zero.": the reading that answers it)
    rub("5.2.4", "This reaction was repeated using a smaller sealed container. How will this affect the magnitude of the gradient of the graph at the "
        "beginning of the reaction? Choose from INCREASES, DECREASES or REMAINS THE SAME. Give a reason for the answer.", 2, [
        "Increases. (1)", "A higher reaction rate / the concentration of the reactants is higher. ACCEPT: the pressure increased. (1)"],
        ["The same amounts of gas are now in a smaller volume.", "How does the concentration affect the number of collisions per second?"])]
q5b = [
    mcq("5.3.1", "Was there a net release or net absorption of energy during the REVERSE reaction?", ["Net release", "Net absorption"], 1,
        ["Read the sign of ΔH in the equation.", "How is the reverse reaction's ΔH related to the forward reaction's?"], marks=1),
    # (was "ΔH < 0: the forward reaction is exothermic." + "The reverse reaction does the opposite.": the answer between them)
    rub("5.3.2", "Define the term activated complex.", 2, [
        "Unstable (high energy) transition state from reactants to products. ACCEPT: between reactants and products. (2)"],
        ["Picture the energy profile: where is the energy highest?", "Is the arrangement of atoms there long-lived or short-lived?"], each=2,
        notes=["Key phrases: unstable (high energy); transition state; from reactants to products. A key phrase omitted (in the correct context): deduct 1."]),
    rub("5.3.3", "A catalyst, vanadium pentoxide, is added to the reaction. Explain, in terms of the collision theory, why the rate of the reaction "
        "will increase.", 3, [
        "The catalyst provides an alternative path with a lower activation energy / lowers the activation energy. (1)",
        "More particles have sufficient (kinetic) energy / kinetic energy greater than (or equal to) the activation energy. (1)",
        "More effective collisions per unit time/second / a higher frequency of effective collisions. (1)"],
        ["What does a catalyst change about the energy barrier?", "Then: how many particles get over it, and how often do they collide effectively?"]),
    mcq("5.3.4", "More SO₂(g) is now added to the container at constant temperature. How will this change affect the heat of the reaction? Choose "
        "from INCREASES, DECREASES or REMAINS THE SAME.", CHANGE, 2,
        ["The heat of reaction, ΔH, is given per mole of reaction as written.", "What decides ΔH: the amounts present, or the bonds broken and "
         "formed?"], marks=1),   # (was "... changes how much reacts, not the energy per mole of reaction.": the answer)
    draw("5.3.5", "More SO₂(g) is now added to the container at constant temperature. Redraw the above graph in the ANSWER BOOK. On the same set of "
         "axes, draw the curve that will now be obtained. Label this as curve Y.", 2, [
        ["Both curves start at the origin and have the correct shape, with their peaks at the same Eₖ", 1],
        ["The peak of curve Y is higher than that of curve X, at the same Eₖ", 1]],
        ["Which feature of the curve is set by the temperature?", "What does adding more SO₂ do to the number of particles?"],
        memo="Both curves not labelled: 0/2. The curves cross at any point other than the origin: max 1/2. Curve Y drawn lower than curve X: max 1/2.")]

# ---- QUESTION 6, the question paper page 13 and the memo pages 13-16 ----
q6a = [
    rub("6.1.1", "State Le Chatelier's principle.", 2, [
        "When the equilibrium in a closed system is disturbed, the system will re-instate a new equilibrium by favouring the reaction that will "
        "cancel/oppose the disturbance. (2)"],
        ["It describes how a system at equilibrium responds when one of its conditions is changed.", "Does the system work with the change, or "
         "against it?"], each=2,   # (the earlier "a closed system at equilibrium ... disturbed" was the principle's own key phrases)
        notes=["Key phrases: equilibrium in a closed system disturbed; re-instate a new equilibrium; favouring the reaction that cancels/opposes the "
               "disturbance. A key phrase omitted (in the correct context): deduct 1."]),
    mcq("6.1.2", "A few drops of concentrated hydrochloric acid, HCℓ(conc.), are added to the equilibrium mixture. What effect does this addition "
        "have on the mass of Ca(OH)₂(s)? Choose from INCREASES, DECREASES or REMAINS THE SAME.", CHANGE, 1,
        ["Which ion in the equilibrium does an acid react with?", "If that ion is removed, which reaction is favoured, and what happens to the "
         "solid?"], marks=1),   # (was "H⁺ from the acid reacts with OH⁻.": a right card of 6.1.3)
    rub("6.1.3", "Explain the answer to QUESTION 6.1.2 by using Le Chatelier's principle.", 2, [
        "A decrease in the amount/concentration of OH⁻ ions favours the reaction that increases the amount/concentration of OH⁻ ions. OR The "
        "acid/HCℓ/H⁺ reacts with OH⁻ ions. (1)",
        "The forward reaction is favoured. OR The amount/concentration of the products increases. (1)"],
        ["What does the H⁺ from the acid do to the ions in the equilibrium?", "Then: which reaction restores them, and what does that do to the "
         "solid?"])]   # (was "The acid removes a product.": the memo's first point)
q6b = [
    mcq("6.2.1", "Is the decomposition of NH₄HS(s) an EXOTHERMIC or ENDOTHERMIC reaction?", ["Exothermic", "Endothermic"], 1,
        ["Read the table: how does Kc change as the temperature rises?", "What does a larger Kc say about the amount of products?"], marks=1),
    # (was "... heating favours the endothermic direction.": the answer)
    rub("6.2.2", "Explain the answer to QUESTION 6.2.1 by using Le Chatelier's principle.", 3, [
        "With an increase in the temperature the Kc value increases. (1)",
        "The concentration of the products increases / the concentration of the reactants decreases / the forward reaction is favoured. (1)",
        "(According to Le Chatelier's principle) an increase in temperature favours the endothermic reaction. (1)"],
        ["Start from the table: what does Kc do as the temperature rises?", "Which reaction does a rise in temperature favour?"]),
    # the memo's Option 1 (calculations using moles: 5,1 g; range 4,96 - 5,74 g, the memo's other options 5,61 g, 4,998 g, 5,128 g and
    # 5,74 g): every wrong working ends outside the range
    work("6.2.3", "Calculate the mass of NH₄HS(s) that will be present at equilibrium at 250 °C.", 8, [
        "n(NH₄HS) = {m}/{M} = {70}/{51}\n= 1,37 mol\nKc = [NH₃][H₂S]\n18 × 10⁻² = x²\nx = 0,42 mol\n"
        "n(NH₄HS) at equilibrium = 1,37 − 0,42\n= 0,95 mol\nm(NH₄HS) = nM = (0,95)(51)\n= 48,45 g",                  # x is a concentration: never × 3 dm³
        "n(NH₄HS) = {m}/{M} = {70}/{50}\n= 1,4 mol\nKc = [NH₃][H₂S]\n18 × 10⁻² = ({x}/{3})²\nx = 1,27 mol\n"
        "n(NH₄HS) at equilibrium = 1,4 − 1,27\n= 0,13 mol\nm(NH₄HS) = nM = (0,13)(50)\n= 6,5 g",                       # M(NH₄HS) as 50: an H missed
        "n(NH₄HS) = {m}/{M} = {70}/{51}\n= 1,37 mol\nKc = [NH₃][H₂S]\n18 × 10⁻² = ({x}/{3})²\nx = 1,27 mol\n"
        "n(NH₄HS) at equilibrium = x\n= 1,27 mol\nm(NH₄HS) = nM = (1,27)(51)\n= 64,77 g",                             # what decomposed, not what is left
        "n(NH₄HS) = {m}/{M} = {70}/{51}\n= 1,37 mol\nKc = [NH₃][H₂S]\n18 × 10⁻² = ({x}/{3})²\nx = 1,27 mol\n"
        "n(NH₄HS) at equilibrium = 1,37 − 1,27\n= 0,1 mol\nm(NH₄HS) = nM = (0,1)(51)\n= 5,1 g"], 3,                     # the memo
        ["Only the gases appear in Kc; the solid left at equilibrium is what did not decompose.",
         "Kc uses concentrations: how many moles are in the 3 dm³ container?"])]   # (was "Turn the concentration into moles (× 3 dm³), "
        # "subtract from the initial moles, then m = nM with M = 51": with the first clue it ruled out every wrong working)

# ---- QUESTION 7, the question paper page 14 and the memo pages 17-20 ----
q7a = [
    rub("7.1.1", "Which one is the stronger acid, H₂PO₄⁻ or HPO₄²⁻? Give a reason for the answer by referring to the data above.", 2, [
        "H₂PO₄⁻ OR H2PO4-. (1)", "The Ka of H₂PO₄⁻ is greater/higher than the Ka of HPO₄²⁻. ACCEPT: the Ka of H₂PO₄⁻ is greater. (1)"],
        ["A stronger acid ionises more.", "Compare the Ka values of the second and third steps."]),
    term("7.1.2", "Write down the FORMULA for the conjugate base of H₂PO₄⁻(aq).", ["HPO4 2−", "HPO4^2-", "HPO42-", "HPO4(2-)"],
         ["A conjugate base is the acid less one H⁺.", "Take away one H and add one negative charge."], strict=True),
    term("7.1.3", "Identify a substance behaving as an ampholyte in the reactions above.", [
        "H2PO4−", "HPO4 2−", "HPO4^2-", "Dihydrogen phosphate", "Dihydrogen phosphate ion", "Hydrogen phosphate", "Hydrogen phosphate ion"],
         ["An ampholyte is an acid in one reaction and a base in another.", "Find a species that is a product in one step and a reactant in the next."], strict=True),
    mcq("7.1.4", "Sodium hydrogen phosphate, Na₂HPO₄(s), is dissolved in water. Will the resulting solution be ACIDIC or BASIC?", ["Acidic", "Basic"], 1,
        ["HPO₄²⁻ gives up H⁺ very little (its Ka is tiny), but it can also take H⁺.", "If it takes H⁺ from water, which ion is left?"], marks=1),
    # a balanced equation as multiple choice (2026-10-10): the memo's first equation (reactants, products, balancing: 3 marks, played
    # all or nothing) and three wrong ones: HPO₄²⁻ acting as an acid (it would make the solution acidic), the wrong species (the second
    # ionisation step of the lead) and the memo's 2H₂O form with its coefficients left out (unbalanced). The memo's other accepted
    # forms (the 2H₂O equation balanced, the Na₂HPO₄ / NaOH / Na⁺ forms) are never wrong options.
    mcq("7.1.5", "Sodium hydrogen phosphate, Na₂HPO₄(s), is dissolved in water. Which balanced equation explains the answer to QUESTION 7.1.4?", [
        "HPO₄²⁻(aq) + H₂O(ℓ) ⇌ PO₄³⁻(aq) + H₃O⁺(aq)", "H₂PO₄⁻(aq) + H₂O(ℓ) ⇌ HPO₄²⁻(aq) + H₃O⁺(aq)",
        "HPO₄²⁻(aq) + H₂O(ℓ) ⇌ H₃PO₄(aq) + OH⁻(aq)", "HPO₄²⁻(aq) + H₂O(ℓ) ⇌ H₂PO₄⁻(aq) + OH⁻(aq)"], 3,
        ["HPO₄²⁻ acts as a base here: it takes H⁺ from water.", "Which ion is left over that makes the solution basic?"], marks=3)]
    # (the two clues together still leave two equations, the right one and the unbalanced one: the balancing is the learner's)
q7b = [
    # the memo's Option 1 (0,0417 mol·dm⁻³; range 0,04 - 0,042, its Option 2 via pOH gives 0,042): every wrong working ends outside it
    work("7.2.1", "Calculate the final concentration of the hydroxide ions in the flask.", 4, [
        "pH = −log[H₃O⁺]\n12,62 = log[H₃O⁺]\n[H₃O⁺] = 4,17 × 10¹²\n[H₃O⁺][OH⁻] = 1 × 10⁻¹⁴\n(4,17 × 10¹²)[OH⁻] = 1 × 10⁻¹⁴\n"
        "[OH⁻] = 2,4 × 10⁻²⁷ mol·dm⁻³",                                                        # the minus sign of −log dropped
        "pH = −log[H₃O⁺]\n12,62 = −log[H₃O⁺]\n[H₃O⁺] = 2,4 × 10⁻¹³\n[H₃O⁺][OH⁻] = 1 × 10⁻¹⁴\n(2,4 × 10⁻¹³)[OH⁻] = 1 × 10⁻¹⁴\n"
        "[OH⁻] = 0,0417 mol·dm⁻³",                                                              # the memo
        "pH = −log[H₃O⁺]\n12,62 = −log[H₃O⁺]\n[H₃O⁺] = 2,4 × 10⁻¹³\n[H₃O⁺][OH⁻] = 1 × 10⁻¹⁴\n(2,4 × 10⁻¹³)[OH⁻] = 1 × 10⁻¹⁴\n"
        "[OH⁻] = 24 mol·dm⁻³",                                                                  # divides the wrong way: 2,4 × 10⁻¹³ / 10⁻¹⁴
        "pH = −log[H₃O⁺]\n12,62 = −log[H₃O⁺]\n[H₃O⁺] = 1 × 10⁻¹³\n[H₃O⁺][OH⁻] = 1 × 10⁻¹⁴\n(1 × 10⁻¹³)[OH⁻] = 1 × 10⁻¹⁴\n"
        "[OH⁻] = 0,1 mol·dm⁻³"], 1,                                                             # the pH rounded to 13 too early
        ["Find [H₃O⁺] from the pH first.", "At 25 °C, Kw = [H₃O⁺][OH⁻] = 1 × 10⁻¹⁴."]),
    # (was "pH + pOH = 14 at 25 °C." + "[OH⁻] = 10^(−pOH).": the whole of the memo's Option 2 between them)
    # the memo's Option 1 (9,34 x 10⁻³ mol, carrying the unrounded 2,334 x 10⁻³; range 9,2 x 10⁻³ - 9,36 x 10⁻³): every wrong working
    # ends outside it. It shows 7.2.1's 0,0417 mol·dm⁻³, so it opens after 7.2.1 (GATES).
    work("7.2.2", "Calculate the number of moles of Ba(OH)₂ used to prepare the 100 cm³ solution.", 8, [
        "n(HCℓ) = cV = (0,2)(0,015)\n= 3 × 10⁻³ mol\nn(OH⁻) = n(HCℓ)\n= 3 × 10⁻³ mol\nn(OH⁻) final = cV = (0,0417)(0,025)\n= 1,04 × 10⁻³ mol\n"
        "n(OH⁻) initial = 3 × 10⁻³ + 1,04 × 10⁻³\n= 4,04 × 10⁻³ mol\nn(Ba(OH)₂) = {1}/{2} n(OH⁻) initial = {1}/{2}(4,04 × 10⁻³)\n"
        "= 2,02 × 10⁻³ mol in 25 cm³\nIn 100 cm³: n = (4)(2,02 × 10⁻³)\n= 8,08 × 10⁻³ mol",                  # the flask's 40 cm³ read as 25 cm³
        "n(HCℓ) = cV = (0,2)(0,015)\n= 3 × 10⁻³ mol\nn(OH⁻) = n(HCℓ)\n= 3 × 10⁻³ mol\nn(OH⁻) final = cV = (0,0417)(0,04)\n= 1,67 × 10⁻³ mol\n"
        "n(OH⁻) initial = 3 × 10⁻³ + 1,67 × 10⁻³\n= 4,67 × 10⁻³ mol\nn(Ba(OH)₂) = n(OH⁻) initial\n"
        "= 4,67 × 10⁻³ mol in 25 cm³\nIn 100 cm³: n = (4)(4,67 × 10⁻³)\n= 1,87 × 10⁻² mol",                  # the 1 : 2 ratio Ba(OH)₂ : OH⁻ not applied
        "n(HCℓ) = cV = (0,2)(0,015)\n= 3 × 10⁻³ mol\nn(OH⁻) = n(HCℓ)\n= 3 × 10⁻³ mol\nn(OH⁻) final = cV = (0,0417)(0,04)\n= 1,67 × 10⁻³ mol\n"
        "n(OH⁻) initial = 3 × 10⁻³ + 1,67 × 10⁻³\n= 4,67 × 10⁻³ mol\nn(Ba(OH)₂) = {1}/{2} n(OH⁻) initial = {1}/{2}(4,67 × 10⁻³)\n"
        "= 2,33 × 10⁻³ mol in 25 cm³\nIn 100 cm³: n = (4)(2,33 × 10⁻³)\n= 9,34 × 10⁻³ mol",                  # the memo
        "n(HCℓ) = cV = (0,2)(15)\n= 3 mol\nn(OH⁻) = n(HCℓ)\n= 3 mol\nn(OH⁻) final = cV = (0,0417)(40)\n= 1,67 mol\n"
        "n(OH⁻) initial = 3 + 1,67\n= 4,67 mol\nn(Ba(OH)₂) = {1}/{2} n(OH⁻) initial = {1}/{2}(4,67)\n"
        "= 2,33 mol in 25 cm³\nIn 100 cm³: n = (4)(2,33)\n= 9,34 mol"], 2,                                     # cm³ not converted to dm³
        ["What is the total volume of the solution in the flask once the HCℓ is added?", "OH⁻ at the start = the OH⁻ used by the HCℓ + the OH⁻ "
         "left over."], after=["7.2.1"])]
    # (was "The flask holds 25 + 15 = 40 cm³ ..." + "... Each Ba(OH)₂ gives 2 OH⁻, and the 100 cm³ holds 4 times the 25 cm³": with the
    # first clue it ruled out two of the three wrong workings outright)

# ---- QUESTION 8, the question paper page 15 and the memo pages 20-21 ----
q8 = [
    rub("8.1", "Define the term electrolyte.", 2, [
        "ANY ONE: a substance whose (aqueous) solution contains ions; a substance that dissolves in water to give a solution that conducts electricity "
        "(through the movement of ions); a substance that dissociates to form ions in water/in the molten state. (2 or 0)"],
        ["Think of what happens to table salt, NaCℓ, when it dissolves in water.", "Which particles carry the charge through a solution?"],
        each=2),   # (was "It is about ions." + "Dissolved or molten, it conducts because of ...": between them every wrong card was out)
    rub("8.2", "Which ion concentration, Aℓ³⁺(aq) or Zn²⁺(aq), will increase? Give a reason for the answer.", 2, [
        "Al3+ OR Aℓ³⁺ OR the aluminium ion. (1)", "Al/Aℓ/aluminium is oxidised OR Al/Aℓ/aluminium is a stronger reducing agent. (1)"],
        ["Table 4 of the data sheets: Aℓ³⁺/Aℓ −1,66 V; Zn²⁺/Zn −0,76 V.", "The half-cell with the more negative reduction potential is the "
         "anode: what happens to its metal?"]),   # (was "The metal that is oxidised forms more of its ions.": the reason card)
    term("8.3", "Write down the cell notation for this cell.", [
        "Al(s) | Al3+(aq) || Zn2+(aq) | Zn(s)", "Al | Al3+ || Zn2+ | Zn", "Al(s) | Al3+ || Zn2+ | Zn(s)", "Al | Al3+(aq) || Zn2+(aq) | Zn",
        "Al(s) | Al3+ (1 mol·dm-3) || Zn2+(aq) (1 mol·dm-3) | Zn(s)", "Al(s) | Al3+(aq) (1 mol·dm-3) || Zn2+(aq) (1 mol·dm-3) | Zn(s)"],
         ["The anode (oxidation) is written on the left, the cathode on the right, a double line for the salt bridge.", "Decide first which "
          "metal is oxidised: its half-cell is the anode."], marks=3, strict=True),
    # (was "Aℓ is the anode here.": with the first clue it spelt the whole notation)
    # the memo's Option 1 (42,75 g; no range): the wrong workings are the memo's own steps with one error each
    work("8.4", "Calculate the mass of Aℓ₂(SO₄)₃(s) needed to prepare 250 cm³ of this solution so that the cell operates initially under STANDARD "
         "CONDITIONS.", 4, [
        "n(Aℓ³⁺) = cV = (1)(0,25)\n= 0,25 mol\nn(Aℓ₂(SO₄)₃) = {1}/{2} n(Aℓ³⁺) = {1}/{2}(0,25)\n= 0,125 mol\nn = {m}/{M}: 0,125 = {m}/{342}\n"
        "m = 42,75 g",                                                                            # the memo
        "n(Aℓ³⁺) = cV = (1)(0,25)\n= 0,25 mol\nn(Aℓ₂(SO₄)₃) = n(Aℓ³⁺)\n= 0,25 mol\nn = {m}/{M}: 0,25 = {m}/{342}\n"
        "m = 85,5 g",                                                                             # the 1 : 2 ratio not applied
        "n(Aℓ³⁺) = cV = (1)(250)\n= 250 mol\nn(Aℓ₂(SO₄)₃) = {1}/{2} n(Aℓ³⁺) = {1}/{2}(250)\n= 125 mol\nn = {m}/{M}: 125 = {m}/{342}\n"
        "m = 42 750 g",                                                                           # 250 cm³ not converted to dm³
        "n(Aℓ³⁺) = cV = (1)(0,25)\n= 0,25 mol\nn(Aℓ₂(SO₄)₃) = {1}/{2} n(Aℓ³⁺) = {1}/{2}(0,25)\n= 0,125 mol\nn = {m}/{M}: 0,125 = {m}/{150}\n"
        "m = 18,75 g"], 0,                                                                        # M read as Aℓ₂SO₄ (150): the bracket's 3 dropped
        ["Standard conditions: [Aℓ³⁺] = 1 mol·dm⁻³.", "How many Aℓ³⁺ ions does one Aℓ₂(SO₄)₃ give when it dissolves?"])]
    # (was "Each Aℓ₂(SO₄)₃ gives 2 Aℓ³⁺; M(Aℓ₂(SO₄)₃) = 342 g·mol⁻¹.": it ruled out two of the three wrong workings outright)

# ---- QUESTION 9, the question paper page 16 and the memo page 22 ----
q9 = [
    mcq("9.1", "Is this an ELECTROLYTIC or a GALVANIC cell?", ["Electrolytic", "Galvanic"], 0,
        ["Is a battery driving the reaction?", "A cell that uses electrical energy to cause a reaction is ..."], marks=1),
    mcq("9.2.1", "How will the concentration of the zinc ions in the electrolyte be affected during the refining of the copper? Choose from "
        "INCREASES, DECREASES or REMAINS THE SAME.", CHANGE, 0,
        ["What happens to the zinc in the impure copper electrode?", "Use Table 4: is Zn²⁺ reduced at the cathode while Cu²⁺ is present?"],
        marks=1),   # (was "The impure copper's zinc is oxidised too." + "Zn²⁺ is a weaker oxidising agent than Cu²⁺: is it reduced ...": the
    # answer between them, and 9.2.2's OR reason word for word)
    rub("9.2.2", "Will the amount of Cu²⁺(aq) ions INCREASE or DECREASE? Explain the answer in terms of the relative strengths of the oxidising agents "
        "present.", 3, [
        "Decrease. (1)", "More Cu2+/Cu²⁺/copper ions are reduced than formed OR only Cu2+/Cu²⁺/copper ions are reduced. (1)",
        "Cu2+/Cu²⁺/copper(II) is a stronger oxidising agent than Zn2+/Zn²⁺/zinc(II) OR Zn2+/Zn²⁺ is a weaker oxidising agent than Cu2+/Cu²⁺. (1)"],
        ["At the anode both Cu and Zn are oxidised; at the cathode only one ion is reduced.", "Which ion, Cu²⁺ or Zn²⁺, is the stronger oxidising agent?"]),
    # the memo's working (9,6 g, a decrease; NO RANGE). It shows Zn leaving R as ions and the Cu²⁺ falling, 9.2.1's and 9.2.2's answers,
    # so it opens after both (GATES).
    work("9.2.3", "Calculate the change in mass of electrode R after T hours.", 6, [
        "n(Zn²⁺) = n(Cu) deposited\n= 0,15 mol\nm(Zn) = nM = (0,15)(65)\n= 9,75 g Zn from R\nn(Cu) from R = 0,15 − 0,05\n= 0,1 mol Cu\n"
        "m(Cu) = nM = (0,1)(63,5)\n= 6,35 g Cu from R\nChange in mass = 6,35 + 9,75\n= 16,1 g (a decrease)",        # the 1 : 1 ratio on the wrong amount
        "n(Zn²⁺) = n(Cu²⁺)\n= 0,05 mol\nm(Zn) = nM = (0,05)(65)\n= 3,25 g Zn from R\nn(Cu) from R = 0,15 − 0,05\n= 0,1 mol Cu\n"
        "m(Cu) = nM = (0,1)(63,5)\n= 6,35 g Cu from R\nChange in mass = 6,35 + 3,25\n= 9,6 g (a decrease)",          # the memo
        "n(Zn²⁺) = n(Cu²⁺)\n= 0,05 mol\nm(Zn) = nM = (0,05)(65)\n= 3,25 g Zn from R\nn(Cu) from R = 0,15 + 0,05\n= 0,2 mol Cu\n"
        "m(Cu) = nM = (0,2)(63,5)\n= 12,7 g Cu from R\nChange in mass = 12,7 + 3,25\n= 15,95 g (a decrease)",       # the moles added, not subtracted
        "n(Zn²⁺) = n(Cu²⁺)\n= 0,05 mol\nm(Zn) = nM = (0,05)(30)\n= 1,5 g Zn from R\nn(Cu) from R = 0,15 − 0,05\n= 0,1 mol Cu\n"
        "m(Cu) = nM = (0,1)(29)\n= 2,9 g Cu from R\nChange in mass = 2,9 + 1,5\n= 4,4 g (a decrease)"], 1,           # atomic numbers used as M
        ["R is the impure copper (the anode): both Zn and Cu leave it as ions.", "The Cu²⁺ fell by 0,05 mol while 0,15 mol Cu was deposited: what made "
         "up the difference?"], after=["9.2.1", "9.2.2"])]

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
    {"id": "2.3", "title": "Question 2.3", "kind": "Reacting gas volumes", "marks": 6,   # (was "Combustion": 2.3.1's answer)
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
     "figure": fig("Q5", "Graph of concentration of O₂(g) (mol·dm⁻³), 0 to 0,30, against time (s), 0 to 60, on a fine grid, with one "
                   "curve."), "items": q5a},
    # (no shape and no readings: "falls steeply ... then more and more slowly" was 5.2.1's answer in words, and the readings at
    # 10 s and 30 s showed which slope is steeper; the curve carries no printed values, reading it is the skill, 2026-10-11)
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
    {"id": "9", "title": "Question 9", "kind": "Refining copper", "marks": 11,   # (was "Electrolytic cells": 9.1's answer)
     "lead": "The diagram below represents a cell used for the refining of copper. The unrefined copper contains zinc as the only impurity.\n\nWhen the "
             "switch is closed, it is found after T hours that the amount of Cu²⁺(aq) ions in the electrolyte changed by 0,05 moles and 0,15 moles of "
             "Cu(s) were deposited on electrode Q.",
     "figure": fig("Q9", "A battery and a switch wired to two electrodes in one container of electrolyte: electrode Q on the left and electrode R "
                   "on the right."), "items": q9},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Business Studies P2 2025 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, another term's definition, the opposite choice, the reversed reasoning):
# never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns `each`;
# the cards are shuffled the same way every run. The rubric bullets above stay as the source. Where the memo gives ONE mark for
# "A / B" forms of a point (5.2.4's "higher rate / higher concentration", 6.1.3's two forms of its first point), one form is a card:
# two right cards for one mark would let two picks earn two marks.


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("ps-p2-2025-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    # 1 or 0, either OR form: the wrong ones are the structural isomers' definition, a CH₃ step, one carbon count, one boiling point
    "3.1": (1, ["A series of organic compounds that can be described by the same general formula.",
                "A series of organic compounds in which one member differs from the next by a CH₂ group."],
               ["A series of organic compounds that have the same molecular formula but different structural formulae.",
                "A series of organic compounds in which one member differs from the next by a CH₃ group.",
                "A series of organic compounds that all have the same number of carbon atoms.",
                "A series of organic compounds that all have the same boiling point."]),
    # 2 ticks: the choice and the reason (its OR forms say the same or "A has stronger intermolecular forces": one card, see above)
    "3.5": (1, ["Compound A has the higher boiling point.",
                "The hydrogen bonds between the molecules of A are stronger than the dipole-dipole forces between the molecules of B."],
               ["Compound B has the higher boiling point.",
                "The dipole-dipole forces between the molecules of B are stronger than the hydrogen bonds between the molecules of A.",
                "Compound A has the higher vapour pressure, so its molecules escape more easily.",
                "Only the molecules of compound B form hydrogen bonds with one another."]),
    # 2, key phrases (longer chain hydrocarbon molecules, broken down, shorter molecules): the wrong ones reverse it, or are
    # combustion, fractional distillation and hydrogenation
    "4.2.1": (2, ["The chemical process in which longer chain hydrocarbon molecules are broken down to shorter (more useful) molecules."],
                 ["The chemical process in which shorter chain hydrocarbon molecules are joined to form longer molecules.",
                  "The chemical process in which hydrocarbon molecules react with oxygen to form carbon dioxide and water.",
                  "The process in which longer chain hydrocarbon molecules are separated by their boiling points, without breaking any bonds.",
                  "The chemical process in which hydrogen is added to an unsaturated hydrocarbon to form a saturated one."]),
    # 3 ticks: the choice (X), unsaturated, and ONE of its "any one" reasons (addition, which needs no UV light: two memo forms in one
    # card); the other "any one" reasons are true, so they are neither right nor wrong cards
    "4.2.4": (1, ["X reacts faster with Br₂(aq).", "X is unsaturated: it has a double bond.",
                  "X undergoes an addition reaction, which does not need UV light."],
                 ["C₄H₁₀ reacts faster with Br₂(aq).", "X is saturated: it has only single bonds.",
                  "C₄H₁₀ is unsaturated, so it reacts with bromine by addition.", "A substitution reaction is faster than an addition reaction."]),
    # 2 or 0, any one of its forms (two as cards): the wrong ones per unit volume, no time at all, a completion time, activation energy
    "5.1": (2, ["The change in concentration of products or reactants per unit time.",
                "The amount of products formed or reactants used per unit time."],
               ["The change in concentration of products or reactants per unit volume.",
                "The total change in concentration of products or reactants during a reaction.",
                "The total time taken for all the reactants to be used up.",
                "The minimum energy that colliding particles need for a reaction to take place."]),
    # 2 ticks: the choice and ONE form of the reason (the memo's "higher reaction rate / concentration higher / ACCEPT pressure")
    "5.2.4": (1, ["The magnitude of the gradient increases.", "The concentration of the reactants is higher."],
                 ["The magnitude of the gradient decreases.", "The magnitude of the gradient remains the same.",
                  "The concentration of the reactants is lower.", "Fewer reactant particles collide per unit time."]),
    # 2, key phrases (unstable / high energy, transition state, from reactants to products; ACCEPT "between": a second right card):
    # the wrong ones are stable and low-energy, activation energy, a catalyst, the heat of reaction
    "5.3.2": (2, ["An unstable, high-energy transition state from reactants to products.",
                  "An unstable, high-energy transition state between reactants and products."],
                 ["A stable, low-energy state from reactants to products.", "The minimum energy needed for a reaction to take place.",
                  "A substance that increases the rate of a reaction without being used up.",
                  "The energy released when the products form from the reactants."]),
    # 3 ticks, the memo's collision-theory chain; the wrong ones are the usual catalyst misconceptions
    "5.3.3": (1, ["The catalyst provides an alternative path with a lower activation energy.",
                  "More particles have kinetic energy greater than or equal to the activation energy.",
                  "There are more effective collisions per unit time."],
                 ["The catalyst increases the average kinetic energy of the particles.", "The catalyst increases the activation energy of the reaction.",
                  "The catalyst increases the concentration of the reactants."]),
    # 2, key phrases (equilibrium in a closed system disturbed, a new equilibrium, favouring the reaction that opposes the disturbance):
    # the wrong ones reverse it, open the system, return to the old concentrations, or are the definition of dynamic equilibrium
    "6.1.1": (2, ["When the equilibrium in a closed system is disturbed, the system will re-instate a new equilibrium by favouring the reaction "
                  "that will oppose the disturbance."],
                 ["When the equilibrium in a closed system is disturbed, the system will re-instate a new equilibrium by favouring the reaction "
                  "that will increase the disturbance.",
                  "When the equilibrium in an open system is disturbed, the system will re-instate a new equilibrium by favouring the reaction "
                  "that will oppose the disturbance.",
                  "When the equilibrium in a closed system is disturbed, the concentrations always return to exactly their values before the "
                  "disturbance.",
                  "In a closed system at equilibrium, the rate of the forward reaction equals the rate of the reverse reaction."]),
    # 2 ticks: the first point (its two OR forms joined in one card) and the forward reaction
    "6.1.3": (1, ["The H⁺ ions from the acid react with the OH⁻ ions: the decrease in OH⁻ favours the reaction that increases the amount of "
                  "OH⁻ ions.", "The forward reaction is favoured."],
                 ["The reverse reaction is favoured.", "The added acid increases the concentration of the OH⁻ ions.",
                  "The H⁺ ions from the acid react with the Ca²⁺ ions, so the reverse reaction is favoured.",
                  "The decrease in OH⁻ favours the reaction that decreases the amount of OH⁻ ions."]),
    # 3 ticks: Kc up with temperature, more products (one of its OR forms), the endothermic reaction favoured
    "6.2.2": (1, ["With an increase in temperature, the Kc value increases.", "The concentration of the products increases.",
                  "An increase in temperature favours the endothermic reaction."],
                 ["With an increase in temperature, the Kc value decreases.", "The concentration of the products decreases.",
                  "An increase in temperature favours the exothermic reaction.", "The Kc value does not depend on the temperature."]),
    # 2 ticks: the choice and the Ka comparison
    "7.1.1": (1, ["H₂PO₄⁻ is the stronger acid.", "The Ka of H₂PO₄⁻ is greater than the Ka of HPO₄²⁻."],
                 ["HPO₄²⁻ is the stronger acid.", "The Ka of HPO₄²⁻ is greater than the Ka of H₂PO₄⁻.",
                  "The acid with the smaller Ka ionises to a greater extent.",
                  "HPO₄²⁻ has the greater negative charge, so it gives up H⁺ more easily."]),
    # 2 or 0, any one of its three forms (all three as cards): the wrong ones are electron conduction, no conduction, the anode, a product
    "8.1": (2, ["A substance whose aqueous solution contains ions.",
                "A substance that dissolves in water to give a solution that conducts electricity through the movement of ions.",
                "A substance that dissociates to form ions in water or in the molten state."],
               ["A substance that conducts electricity through the movement of free electrons, like a metal.",
                "A substance that dissolves in water to give a solution that does not conduct electricity.",
                "The electrode at which oxidation takes place.", "A substance that is formed at the cathode during electrolysis."]),
    # 2 ticks: the choice and ONE form of the reason ("Aℓ is oxidised"; its OR "a stronger reducing agent" is true: no card)
    "8.2": (1, ["The Aℓ³⁺(aq) concentration increases.", "Aℓ is oxidised."],
               ["The Zn²⁺(aq) concentration increases.", "Aℓ is reduced.", "Zn is a stronger reducing agent than Aℓ.",
                "Aℓ³⁺ is a stronger oxidising agent than Zn²⁺."]),
    # 3 ticks: the choice and the memo's two points (one form each)
    "9.2.2": (1, ["The amount of Cu²⁺(aq) ions decreases.", "More Cu²⁺ ions are reduced than are formed.",
                  "Cu²⁺ is a stronger oxidising agent than Zn²⁺."],
                 ["The amount of Cu²⁺(aq) ions increases.", "More Cu²⁺ ions are formed than are reduced.",
                  "Zn²⁺ is a stronger oxidising agent than Cu²⁺.", "Zn²⁺ ions are reduced at the cathode together with the Cu²⁺ ions."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, explanations and choices with reasons), so SORTS stays empty and sort_ is kept for parity.
SORTS = {}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("ps-p2-2025-11:sort:" + n).shuffle(order)
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
assert not [i["n"] for m in missions for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"

# GATES: a part whose stem, options or cards show an earlier part's answer opens only once that part is answered
GATES = {"3.5": ["3.4.1", "3.4.2"],     # its cards: hydrogen bonds in A, dipole-dipole forces in B
         "4.2.4": ["4.2.3"],            # its cards: X is unsaturated, with a double bond (4.2.3's functional group)
         "6.1.3": ["6.1.2"],            # its cards: the forward reaction is favoured (the solid dissolves)
         "6.2.2": ["6.2.1"],            # its cards: heating favours the endothermic reaction
         "7.1.5": ["7.1.4"],            # its stem and options: the equation that explains the answer, OH⁻ formed
         "7.2.2": ["7.2.1"],            # its options: [OH⁻] = 0,0417 mol·dm⁻³
         "9.2.2": ["9.2.1"],            # its cards: Cu²⁺ the stronger oxidising agent, so Zn²⁺ is not reduced
         "9.2.3": ["9.2.1", "9.2.2"]}   # its options: Zn leaves R as ions; less Cu dissolves than is deposited
ITEMS = [i for m in missions for i in m["items"]]
for _it in ITEMS:
    if _it["n"] in GATES:
        _it["after"] = GATES[_it["n"]]
nums = [i["n"] for i in ITEMS]
assert all(nums.index(e) < nums.index(n) for n, es in GATES.items() for e in es), "a gate on a later part"

# every part that played as typed steps before 2026-10-10, now authored multiple choice, the right letter spread over A-D
assert tuple(AUTHORED) == ("2.3.2", "5.2.2", "6.2.3", "7.2.1", "7.2.2", "8.4", "9.2.3"), AUTHORED
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "num", "rubric")], "a typed calculation or a written answer is left"
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == GATES
_at = ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED]
_spread = {k: _at.count(k) for k in "ABCD"}
assert max(_spread.values()) - min(_spread.values()) <= 1, _spread
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Chemistry", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic chemistry errors (a mole ratio not applied or on "
                                                       "the wrong amount, cm³ not converted to dm³, a wrong molar mass, a concentration used as "
                                                       "moles, a value misread or rounded too early, a sign slip), 0 or full marks: "
                                                       + ", ".join(AUTHORED) + " (%d parts, %d marks). A value the memo accepts is never a wrong "
                                                       "option: 2.3.2's 0,066 dm³; 5.2.2's range 0,06 - 0,072 mol·s⁻¹; 6.2.3's range 4,96 - "
                                                       "5,74 g (its options 5,1 g, 5,61 g, 4,998 g, 5,128 g, 5,74 g); 7.2.1's range 0,04 - 0,042 "
                                                       "mol·dm⁻³; 7.2.2's range 9,2 - 9,36 x 10⁻³ mol." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions (3.1, 4.2.1, 5.1, 5.3.2, "
                                                    "6.1.1, 8.1) pick one card for their marks (an OR / ACCEPT form is a second right card); the "
                                                    "explanations and the choices with reasons (3.5, 4.2.4, 5.2.4, 5.3.3, 6.1.3, 6.2.2, 7.1.1, 8.2, "
                                                    "9.2.2) pick the choice and the memo's points, 1 mark each. Where the memo gives one mark for "
                                                    "'A / B' forms of a point, one form is a card and the others are neither right nor wrong cards "
                                                    "(two forms picked would earn two marks); 4.2.4's 'any one' reason is one card." % len(PICKS)},
        {"n": "7.1.5", "kind": "no_fit", "detail": "'Write a balanced equation' plays as multiple choice of four equations, 3 marks all or nothing "
                                                   "(the memo: reactants, products, balancing): the memo's first equation and three wrong ones "
                                                   "(HPO₄²⁻ acting as an acid, the wrong species, the 2H₂O form unbalanced). The memo's other "
                                                   "accepted equations are never wrong options."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (structural formulae and charges are images); no API call."},
        {"n": "2.1.2", "kind": "no_fit", "detail": "Two letters for one mark (2.1.2, 2.1.3) play as multiple choice of six letter pairs, all or "
                                                   "nothing, as the memo gives the mark for the pair (a pick of two letters gave half a mark "
                                                   "for one right letter)."},
        {"n": "2.2.1", "kind": "no_fit", "detail": "IUPAC names (2.2.1-2.2.3, 3.3.2, 4.1.1), formulas (4.1.2, 4.1.4, 7.1.2, 7.1.3) and the cell "
                                                   "notation (8.3) play as strict terms: all or nothing, where the memo gives part marks (stem, "
                                                   "substituents, the whole name; a mark per half-cell and the salt bridge). Spacing and "
                                                   "punctuation are not judged, so a missing hyphen or a misplaced bar is not marked down."},
        {"n": "2.2.4", "kind": "no_fit", "detail": "Structural formulae (2.2.4, 3.3.1, 4.1.5, 4.2.3) and the Maxwell-Boltzmann curve (5.3.5) are "
                                                   "drawn on paper and self-checked against the memo's criteria."},
        {"n": "6.2.3", "kind": "memo_issue", "detail": "The memo's criterion (h) names 5,61 g as the correct final answer, but its Option 1 (the "
                                                       "right option here) ends at 5,1 g and its Option 2 at 5,61 g; the range differs by "
                                                       "language: English 4,96 - 5,74 g, Afrikaans 4,95 - 5,74 g. No wrong option is near it."},
        {"n": "7.2.2", "kind": "memo_issue", "detail": "The memo's '(g) in all options' line gives n(Ba(OH)₂) in 100 cm³ = (0,0936)(0,1) = 0,0936 "
                                                       "mol; that product is 0,00936 mol, in line with its stated answer 9,34 x 10⁻³ mol. Its "
                                                       "Option 1 writes (4)(2,33 x 10⁻³) = 9,34 x 10⁻³ mol, carrying the unrounded 2,334 x 10⁻³: "
                                                       "the right option keeps the memo's line."},
    ],
}
QTOTAL = {"1": 20, "2": 22, "3": 12, "4": 17, "5": 20, "6": 17, "7": 20, "8": 11, "9": 11}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks, right letters", _spread, "; statements:", len(PICKS), "parts")
print("total:", total)
out = Path(__file__).parent / "out" / "ps-p2-2025-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
