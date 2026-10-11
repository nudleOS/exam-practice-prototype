"""Physical Sciences P2 (Chemistry) Nov 2024, the whole paper (Questions 1 to 9), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: structural formulas are drawings.
Polished one subject at a time (Murci, 2026-10-10: "next subject: Physical Sciences").

  python tools/ingest/transcribe_ps_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P2 Nov 2024 Eng.pdf" "<...>/Physical Sciences P2 Nov 2024 MG Afr & Eng.pdf" --id ps-p2-2024-11 --from-json

How the memo's shapes map (Chemistry; as P2 Nov 2025, transcribe_ps_p2_2025_11.py):
  an IUPAC name or a formula -> term with strict (one letter is another compound: but-1-ene / but-2-ene, H2SO4 / H2SO3; spacing and
  punctuation free), the memo's part marks played all or nothing; "Write down the LETTER" -> mcq (one letter; letter pairs where the
  memo gives one mark for the pair, 2.3.2); a choice the paper names -> mcq; a STRUCTURAL formula, an equation in structural
  formulae or a redrawn graph -> draw, self-checked against the memo's criteria; a burette reading with no working (7.3.1, 7.3.2) ->
  num.
The rollout rulings (Murci, 2026-10-10): every calculation -> authored multiple choice, `work` (the memo's FIRST working line by line
  + three workings each built from a DIFFERENT real chemistry error, 0 or full marks; no wrong option inside a memo range or equal to
  a value the memo accepts; the right letter spread over A-D); every written answer -> statements (STATEMENTS at the bottom): a
  definition picks 1 card for its marks (the memo's wording right, its OR form a second right card, the wrong ones a key condition
  dropped or swapped, or another term's definition); an explanation, or a choice with its reason, picks the choice card and the
  memo's points, 1 mark each (the other choices and the reversed reasoning are the wrong cards; where the memo gives one mark for
  "A / B" forms of a point, only one form is a card, so two forms can never earn two marks). A balanced equation (8.2.1) or a
  half-reaction (9.2.2) -> multiple choice of four equations; a one-term written answer (5.2.1) -> multiple choice. No memo here
  weighs two sides, so no part plays as a sort. A part whose stem, options or cards show an earlier part's answer opens only after
  it (GATES).
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves (re-measured 2026-10-11 on gridded
renders: 1.9's voltmeter, 1.10's and 9.2's batteries were cut off, and the text above or below bled into 1.10, Q2, Q4, Q5, Q6,
Q9)."""
import json
import random
import re
from pathlib import Path

W, H = 595.44, 841.68
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.4": [4, 175, 122, 505, 352], "1.9": [6, 150, 108, 435, 262], "1.10": [6, 220, 437, 350, 554], "Q2": [7, 46, 137, 525, 404],
    "Q4": [9, 84, 181, 526, 438], "Q5": [11, 190, 328, 415, 488], "Q5.2": [12, 105, 252, 448, 434], "Q6": [13, 112, 228, 502, 496],
    "Q9": [17, 130, 143, 462, 228], "Q9.2": [17, 215, 369, 432, 510]}


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
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}
KEYPHRASES = "If any one of the underlined key phrases in the correct context is omitted, deduct 1 mark."


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


LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]
P = lambda a, b: "Compounds %s and %s" % (a, b)   # a pair of letters as an option ("C · A and C" would read as one letter)

# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
# (2026-10-11: the clues are questions; several pairs settled the answer between them, e.g. 1.5's "Equal amounts used from equal
# amounts: what is left?", 1.6's "Adding a reactant favours the forward reaction.", 1.8's "Which pair is a weak acid with a strong base?")
q1 = [
    mcq("1.1", "Which ONE of the following compounds has hydrogen bonds between its molecules?", ["CH₃CH₂CHO", "CH₃COOCH₃", "CH₃CH₂CH₂OH", "CH₃COCH₃"], 2,
        ["Hydrogen bonds form when an H atom is bonded to a very small, electronegative atom: which atoms are those?",
         "Look at the functional group in each formula: which one puts an H directly on such an atom?"]),
    mcq("1.2", "Which ONE of the following is a CORRECT GENERAL FORMULA for the carboxylic acids?", ["CₙH₂ₙ₊₁O₂", "CₙH₂ₙO₂ₙ", "CₙH₂ₙO₂", "CₙHₙO₂"], 2,
        ["Write the molecular formula of a carboxylic acid you know, such as ethanoic acid, CH₃COOH.",
         "Which general formula gives that molecular formula for its number of carbons?"]),
    mcq("1.3", "Study the reactions below. Reaction 1: CH₃CH₂CHOHCH₃ —(conc. H₂SO₄)→ Compound P (major product) + H₂O. Reaction 2: Compound P "
        "—(hydrogenation)→ Compound Q. Which ONE of the following combinations is the CORRECT IUPAC names of compounds P and Q?",
        ["P: but-1-ene · Q: butane", "P: but-2-ene · Q: butane", "P: but-1-ene · Q: butan-2-ol", "P: but-2-ene · Q: butan-2-ol"], 1,
        ["What type of reaction does concentrated H₂SO₄ cause with an alcohol, and which of the possible products is the major one?",
         "What does hydrogenation add, and to which kind of bond?"],   # (was "... the more substituted double bond." + "adds H₂ across
        # the double bond": the answer between them)
        optTable={"head": ["COMPOUND P", "COMPOUND Q"], "rows": [["But-1-ene", "Butane"], ["But-2-ene", "Butane"], ["But-1-ene", "Butan-2-ol"], ["But-2-ene", "Butan-2-ol"]]}),
    mcq("1.4", "The potential energy diagram below is for the following hypothetical chemical reaction: X + Y ⇌ Z. Which ONE of the following combinations "
        "of values for the heat of the reaction and the activation energies can be obtained for this reaction?",
        ["ΔH −400 · EA(forward) 300 · EA(reverse) 100", "ΔH −200 · EA(forward) 300 · EA(reverse) 100", "ΔH +400 · EA(forward) 100 · EA(reverse) 300",
         "ΔH −200 · EA(forward) 100 · EA(reverse) 300"], 3,
        ["Do the products end higher or lower than the reactants, and what sign does that give ΔH?",
         "How is ΔH related to the forward and the reverse activation energies?"],
        figure=fig("1.4", "A potential energy against course of reaction graph for X + Y ⇌ Z: the curve starts on a level, rises to a peak and falls to a "
                          "level below the starting one."),
        optTable={"head": ["ΔH(forward) (kJ·mol⁻¹)", "EA(forward) (kJ·mol⁻¹)", "EA(reverse) (kJ·mol⁻¹)"],
                  "rows": [["−400", "300", "100"], ["−200", "300", "100"], ["+400", "100", "300"], ["−200", "100", "300"]]}),
    mcq("1.5", "Initially, an equal number of moles of hydrogen gas, H₂(g), and iodine gas, I₂(g), are mixed in a closed container. The reaction reaches "
        "equilibrium at a constant temperature according to the balanced equation: H₂(g) + I₂(g) ⇌ 2HI(g). Which ONE of the following is ALWAYS TRUE at "
        "equilibrium?", ["[H₂] = [I₂]", "[HI] = [I₂]", "[HI] = 2[H₂]", "[H₂] = [I₂] = [HI]"], 0,
        ["In what mole ratio do H₂ and I₂ react?", "Which statement must hold whatever the value of Kc?"]),
    mcq("1.6", "Consider the following reaction at equilibrium: 2SO₂(g) + O₂(g) ⇌ 2SO₃(g), ΔH = −188 kJ·mol⁻¹. Which ONE of the changes to the reaction "
        "conditions below will increase the yield of SO₃(g)?",
        ["The addition of O₂(g)", "The addition of a catalyst", "An increase in temperature", "An increase in the volume of the container at a constant temperature"], 0,
        ["Which of these changes does not shift an equilibrium at all?", "For each of the others, which reaction does Le Chatelier's principle say is "
         "favoured?"]),
    mcq("1.7", "The table shows the ionisation constants, Ka, for two acids at 25 °C: butanoic acid, Ka = 1,5 x 10⁻⁵; ethanoic acid, Ka = 1,8 x 10⁻⁵. "
        "Consider the following statements for these two acids when they have equal concentration at 25 °C: (i) Both are weak acids. (ii) Butanoic acid is "
        "a stronger acid than ethanoic acid. (iii) The butanoic acid solution has a lower concentration of hydronium ion, H₃O⁺(aq), than the ethanoic acid "
        "solution. Which of the above statements are TRUE?", ["(i) and (ii) only", "(i) and (iii) only", "(ii) and (iii) only", "(i), (ii) and (iii)"], 1,
        ["What does the size of Ka tell you about how far an acid ionises?", "Compare the two Ka values: which acid makes more H₃O⁺ at the same "
         "concentration?"]),
    mcq("1.8", "Which ONE of the following pairs of acids and bases, all of the same concentration, react to give the highest pH at the equivalence point in a "
        "titration at 25 °C?", ["HCℓ and NH₃", "HCℓ and NaOH", "HNO₃ and KOH", "CH₃COOH and NaOH"], 3,
        ["Classify each acid and each base: strong or weak?", "For each pair, is the solution at the equivalence point acidic, neutral or basic?"]),
    mcq("1.9", "A standard galvanic cell is set up, as shown below. Which ONE of the following combinations of the metal used as cathode and the electron flow "
        "direction is CORRECT?", ["Cathode Cd · Cd to Ag", "Cathode Ag · Cd to Ag", "Cathode Cd · Ag to Cd", "Cathode Ag · Ag to Cd"], 1,
        ["Use Table 4: which ion, Cd²⁺ or Ag⁺, is the stronger oxidising agent?", "Does reduction or oxidation happen at the cathode, and from which "
         "electrode do electrons leave through the wire?"],
        figure=fig("1.9", "A Cd electrode in Cd²⁺(aq) on the left and an Ag electrode in Ag⁺(aq) on the right, joined by a salt bridge and, through a "
                          "voltmeter V, by a wire."),
        optTable={"head": ["METAL USED AS CATHODE", "ELECTRON FLOW DIRECTION"], "rows": [["Cd", "Cd to Ag"], ["Ag", "Cd to Ag"], ["Cd", "Ag to Cd"], ["Ag", "Ag to Cd"]]}),
    mcq("1.10", "An electrolytic cell is set up to electroplate an iron rod with nickel, as shown in the diagram below. Consider the following statements: (i) "
        "The iron rod is the negative electrode. (ii) The metal ions in the solution undergo reduction. (iii) The anode is pure nickel. Which of the above "
        "statements are TRUE?", ["(i) and (ii) only", "(i) and (iii) only", "(ii) and (iii) only", "(i), (ii) and (iii)"], 3,
        ["On which electrode does the nickel deposit, and what is that electrode's charge?", "As nickel ions are used up, where must new ones come "
         "from?"],   # (was "The object being plated is the cathode." + "... reduced onto the rod and replaced from the anode.": all three)
        figure=fig("1.10", "Two electrodes in a beaker of solution, connected to a battery above.")),
]

# ---- QUESTION 2, the question paper pages 7-8 and the memo pages 2-3 ----
q2 = [
    mcq("2.1.1", "Write down the LETTER that represents an alcohol.", LETTERS, 3,
        ["An alcohol has an –OH group: read the formulas as well as the drawings.", "Check each molecular formula against the general formula of the "
         "alcohols."], marks=1),   # (was "Which formula has one O and is saturated?": it pointed at D)
    mcq("2.1.2", "Write down the LETTER that represents a compound with a formyl group.", LETTERS, 0,
        ["Which homologous series has the formyl group, –CHO, as its functional group?", "Read the drawings as well as the names and formulas."],
        marks=1),
    mcq("2.1.3", "Write down the LETTER that represents an unsaturated compound.", LETTERS, 4,
        ["Which kinds of bond between carbon atoms make a compound unsaturated?", "Draw out each condensed formula, giving every carbon four bonds."],
        marks=1),   # (was "CCC in a condensed formula hides a triple bond.": it pointed at E by its spelling)
    term("2.2.1", "Write down the IUPAC name of compound B.", ["3,3-dibromo-4,4-dimethylhexane"],
         ["Find the LONGEST chain: it may run up into a branch.", "Number for the lowest locants; list the substituents in alphabetical order."],
         marks=3, strict=True),   # (was "... bromo comes before methyl alphabetically": it named the memo's substituents mark)
    term("2.2.2", "Write down the IUPAC name of compound E.", ["4,4-dimethylpent-2-yne", "4,4-dimethyl-2-pentyne"],
         ["Draw E out in full, giving every carbon four bonds.", "Number the longest chain so that the functional group gets the lowest number; then "
          "place the branches."], marks=3, strict=True),   # (was "... the CC is a triple bond.": the stem mark, and 2.1.3's answer)
    rub("2.3.1", "Define the term functional isomer.", 2,
        ["Compounds with the same molecular formula, but different functional groups / homologous series. (2)"],
        ["Think of propanoic acid and methyl ethanoate: what do they have in common?", "Which part of the two molecules is different?"], each=2,
        notes=[KEYPHRASES]),   # (was "Same formula, different ... ?": the definition)
    # two letters for ONE mark (the memo: "A and C", the mark for the pair): multiple choice of six pairs, all or nothing (2026-10-11; a
    # pick of two letters gave half a mark for one right letter, which the memo does not). The wrong pairs have different molecular
    # formulae (A C₄H₈O, C C₄H₈O, D C₄H₁₀O, E C₇H₁₂, F C₅H₁₀O₂, G C₄H₈O₂, H C₆H₁₄): none is a pair of isomers.
    mcq("2.3.2", "Two different compounds in the above table are functional isomers. Write down the LETTERS that represent these functional isomers.",
        [P("A", "D"), P("F", "G"), P("C", "D"), P("A", "C"), P("E", "H"), P("D", "G")], 3,
        ["Work out the molecular formula of every compound, the drawn ones too.", "Which two formulas are the same, for compounds from different "
         "homologous series?"], marks=1),   # (was "Count the C, H and O of A and C.": it named the answer)
    term("2.4.1", "Compound F is formed when a carboxylic acid reacts with another organic compound, X, in the presence of a catalyst. Write down the NAME or "
         "FORMULA of the catalyst.", ["H2SO4", "sulphuric acid", "sulfuric acid", "concentrated sulphuric acid", "concentrated sulfuric acid", "conc. H2SO4",
                                      "concentrated H2SO4"],
         ["Is the catalyst an acid or a base, and is it dilute or concentrated?", "Which substance also takes up the water that the reaction forms?"],
         strict=True),   # (strict: a slip let H2SO3 pass)
    term("2.4.2", "Write down the type of reaction.", ["esterification", "condensation"],
         ["Which two kinds of organic compound react to form F?", "Is a small molecule, water, given off as they join?"]),
    # (was "A carboxylic acid and an alcohol make F." + "F is an ester.": the name between them)
    draw("2.4.3", "Write down the STRUCTURAL FORMULA of compound F.", 2,
         [["Functional group (ester, –COO–) correct", 1], ["Whole structural formula correct: CH₃COOCH₂CH₂CH₃ with every bond and H shown", 1]],
         ["F is CH₃COO(CH₂)₂CH₃.", "Show every atom and bond."]),
    term("2.4.4", "Write down the IUPAC name of compound X.", ["propan-1-ol", "1-propanol"],
         ["Which part of the ester, on which side of the –COO–, comes from the alcohol?", "Count the carbons in that part: on which carbon was the "
          "alcohol's –OH?"], marks=2, strict=True),   # (was "... three carbons, the O on the first.": the name)
]

# ---- QUESTION 3, the question paper page 8 and the memo pages 4-6 ----
q3 = [
    rub("3.1", "Define the term vapour pressure.", 2, ["The pressure exerted by a vapour at equilibrium with its liquid in a closed system. (2)"],
        ["Picture a liquid in a sealed container: what collects above it, and what does it push on?", "When does the amount above the liquid stop "
         "changing?"], each=2, notes=[KEYPHRASES]),
    mcq("3.2.1", "The vapour pressures of compounds A, B and C are given in random order: 79 kPa, 146 kPa, 58 kPa. Write down the vapour pressure of compound C.",
        ["79 kPa", "146 kPa", "58 kPa"], 1,
        ["All three compounds have the same molar mass: how do their structures differ?", "How does the shape of a molecule affect the forces between "
         "molecules, and so the vapour pressure?"], marks=1),
    # (was "The most branched compound has the weakest forces and the highest vapour pressure.": with the table's names, the answer)
    rub("3.2.2", "Fully explain your answer to QUESTION 3.2.1.", 3,
        ["Compound C is more branched / has a shorter chain / is more compact / spherical / has a smaller surface area (than A and B) (1)",
         "Compound C has weaker intermolecular forces / London forces / Van der Waals forces than A and B (1)",
         "Less energy is needed to overcome / break the intermolecular forces in compound C (than in A and B) (1)"],
        ["How do the structures compare: which compound is the most branched?", "Then: how strong are the forces between the molecules, and how much "
         "energy is needed to overcome them?"]),
    mcq("3.3.1", "Compounds D and E are compared. Which compound has the lower boiling point?", ["D", "E"], 1,
        ["Which compound has the stronger forces between its molecules?", "Stronger forces between molecules: a higher or a lower boiling point?"],
        marks=1),
    rub("3.3.2", "Fully explain the difference in the vapour pressures between compounds D and E.", 4,
        ["Compound D / propanoic acid has hydrogen bonding (dipole-dipole and London forces) between its molecules (1)",
         "Compound E / butanal has dipole-dipole forces (and London forces) between its molecules (1)",
         "The intermolecular forces in D / propanoic acid are stronger than those in E / butanal (1)",
         "More energy is needed to overcome / break the intermolecular forces in D / propanoic acid than in E / butanal (1)"],
        ["What is the strongest type of intermolecular force in each compound?", "Which forces are stronger, and which compound needs more energy to "
         "overcome them?"]),
]

# ---- QUESTION 4, the question paper pages 9-10 and the memo pages 7-9 ----
q4 = [
    rub("4.1", "Define the term cracking reaction.", 2,
        ["The chemical process / reaction in which longer chain hydrocarbon / alkane molecules are broken down to shorter (more useful) molecules. (2)"],
        ["Compare the size of U with the sizes of W and T.", "Are bonds between carbon atoms made or broken?"], each=2, notes=[KEYPHRASES]),
    # (was "It splits big molecules." + "Long-chain alkanes become ...": the definition)
    rub("4.2", "Is the product in reaction II a PRIMARY, SECONDARY or TERTIARY haloalkane? Give a reason for the answer.", 2,
        ["Primary (1)", "The halogen/bromine/Br (atom) is bonded to a C atom that is bonded to one other C atom OR the halogen/bromine/Br is bonded to "
         "the first/terminal C atom (1)"],
        ["The product of reaction II is CH₃CH₂CH₂CH₂Br.", "How many other C atoms is the carbon carrying the Br bonded to?"]),
    draw("4.3.1", "Write down the STRUCTURAL FORMULA of compound W.", 3,
         [["Correct stem: 4 C atoms in a chain", 1], ["Whole structural formula correct (butane, every H shown)", 2]],
         ["Cracking an alkane gives a shorter alkane and an alkene: T, C₄H₈, is the alkene.", "Reaction II gives CH₃CH₂CH₂CH₂Br: how many carbons "
          "does W have?"]),   # (was "Reaction II turns W into ... by substitution.": 4.4.2's answer)
    term("4.3.2", "Write down the MOLECULAR formula of compound U.", ["C8H18"],
         ["U breaks into W and T and nothing else.", "Add up the C atoms and the H atoms of W and T."], strict=True),
    # (was "Cracking U gives W (C₄H₁₀) and T (C₄H₈) ...": 4.3.1's answer)
    term("4.4.1", "For reaction II, write down the NAME or FORMULA of the inorganic reactant.", ["Br2", "bromine"],
         ["Which atom does the product of reaction II have that W does not?", "What is the formula of that element as a pure substance?"],
         strict=True),   # (was "... puts a Br on an alkane." + "It is a halogen.": the answer; strict: a slip let "bromide" pass)
    mcq("4.4.2", "For reaction II, write down the type of reaction (Choose from SUBSTITUTION, ADDITION or ELIMINATION.)", ["Substitution", "Addition", "Elimination"], 0,
        ["Is W saturated or unsaturated?", "Complete the equation W + Br₂ → CH₃CH₂CH₂CH₂Br + …: what is the other product?"], marks=1),
    # (was "An H is swapped for a Br.": the answer in words)
    lst("4.4.3", "For reaction II, write down ONE reaction condition.", 1, [["UV (light)", "ultraviolet", "sunlight", "light"], ["heat"]],
        ["Alkanes are unreactive: what must be supplied for them to react with bromine?", "In which forms can that energy be supplied?"]),
    # (was "Light, or ...": the answer)
    term("4.5", "Write down the TYPE of elimination in reaction III.", ["dehydrohalogenation", "dehydrobromination"],
         ["Which two atoms leave CH₃CH₂CH₂CH₂Br as the double bond forms?", "Types of elimination are named after what is removed, as dehydration "
          "removes water."]),
    draw("4.6.1", "Compounds R and T are positional isomers. The inorganic reagents Br₂, H₂SO₄(conc.), NaOH(conc.), HBr and H₂ are available for reactions IV "
         "and V. Write down the balanced equation for reaction IV, using STRUCTURAL FORMULAE and the correct inorganic reagent shown above.", 5,
         [["Functional group of the alkene on the first C atom", 1], ["Whole structural formula of the alkene (but-1-ene) correct", 1], ["HBr", 1],
          ["Functional group of the haloalkane correct", 1], ["Whole structural formula of the haloalkane correct (halogen on the second / first C atom)", 1]],
         ["R forms by elimination from CH₃CH₂CH₂CH₂Br: where can its double bond be?", "Which reagent in the list adds to a double bond to give a "
          "haloalkane?"],   # (was "... it is but-1-ene." + "... by addition of HBr.": two criteria)
         memo="Condensed, semi-structural or molecular formulae: max 1/5. An extra product or reactant: deduct 1 mark."),
    draw("4.6.2", "Write down the balanced equation for reaction V, using STRUCTURAL formulae and the correct reagent shown above.", 3,
         [["NaOH", 1], ["Whole structural formula of the alkene correct (functional group on the second / first C atom)", 1], ["NaBr + H₂O", 1]],
         ["Reaction V turns the haloalkane S into the alkene T: which type of reaction is that?", "Which reagent in the list does that, and which "
          "inorganic products form?"],   # (was "Concentrated NaOH removes HBr.": two criteria)
         memo="Condensed, semi-structural or molecular formulae: max 1/3. An extra product or reactant: deduct 1 mark."),
    term("4.6.3", "Write down the IUPAC name of compound T.", ["but-2-ene", "2-butene", "but-1-ene", "1-butene"],
         ["Where is the double bond in R?", "Positional isomers have the same chain, with the functional group on a different carbon."], marks=2,
         strict=True),   # (was "R has the double bond at the end of the chain.": with the first clue, the answer)
]

# ---- QUESTION 5, the question paper pages 11-12 and the memo pages 10-12 ----
q5a = [
    rub("5.1.1", "Define the term reaction rate.", 2,
        ["ANY ONE: the change in concentration of products/reactants per (unit) time; the change in amount/number of moles/volume/mass of products or "
         "reactants per (unit) time; the amount/number of moles/volume/mass of products formed/reactants used per (unit) time; the rate of change in "
         "concentration/amount/number of moles/volume/mass. (2 or 0)"],
        ["Think of how speed is defined in physics, then apply it to a reaction.", "What changes as a reaction goes on: the reactants and the "
         "products."], each=2,   # (was "A change in amount or concentration, divided by time.": the definition)
        notes=["Give the mark for 'per unit time' only in the context of reaction rate."]),
    # the memo's Option 1 (0,38 g; range 0,365 - 0,42 g): every wrong working ends outside the range
    work("5.1.2", "For the time interval t = 0 to t = 5 minutes, the average reaction rate for the formation of H₂(g) is 0,033 dm³·min⁻¹. Calculate the mass of "
         "Aℓ present in the container at t = 5 minutes. Take the molar gas volume as 24,5 dm³·mol⁻¹.", 6, [
        "Rate = {ΔV(H₂)}/{Δt}\n0,033 = {ΔV(H₂)}/{5}\nV(H₂) = 0,165 dm³\nn(H₂) = {V}/{Vm} = {0,165}/{24,5}\n= 6,74 × 10⁻³ mol\n"
        "n(Aℓ) = {3}/{2} n(H₂) = {3}/{2}(6,74 × 10⁻³)\n= 1,01 × 10⁻² mol\nn(Aℓ) = {m}/{M}: 1,01 × 10⁻² = {m}/{27}\nm(Aℓ) used = 0,27 g\n"
        "m(Aℓ) at 5 min = 0,5 − 0,27\n= 0,23 g",                                                  # the 2 : 3 mole ratio inverted
        "Rate = ΔV(H₂) × Δt\n0,033 = ΔV(H₂) × 5\nV(H₂) = 6,6 × 10⁻³ dm³\nn(H₂) = {V}/{Vm} = {6,6 × 10⁻³}/{24,5}\n= 2,69 × 10⁻⁴ mol\n"
        "n(Aℓ) = {2}/{3} n(H₂) = {2}/{3}(2,69 × 10⁻⁴)\n= 1,79 × 10⁻⁴ mol\nn(Aℓ) = {m}/{M}: 1,79 × 10⁻⁴ = {m}/{27}\nm(Aℓ) used = 4,83 × 10⁻³ g\n"
        "m(Aℓ) at 5 min = 0,5 − 4,83 × 10⁻³\n= 0,495 g",                                         # the rate formula wrong: rate = ΔV × Δt
        "Rate = {ΔV(H₂)}/{Δt}\n0,033 = {ΔV(H₂)}/{5}\nV(H₂) = 0,165 dm³\nn(H₂) = {V}/{Vm} = {0,165}/{24,5}\n= 6,74 × 10⁻³ mol\n"
        "n(Aℓ) = {2}/{3} n(H₂) = {2}/{3}(6,74 × 10⁻³)\n= 4,49 × 10⁻³ mol\nn(Aℓ) = {m}/{M}: 4,49 × 10⁻³ = {m}/{27}\nm(Aℓ) used = 0,12 g\n"
        "m(Aℓ) at 5 min = 0,5 − 0,12\n= 0,38 g",                                                  # the memo
        "Rate = {ΔV(H₂)}/{Δt}\n0,033 = {ΔV(H₂)}/{5}\nV(H₂) = 0,165 dm³\nn(H₂) = {V}/{Vm} = {0,165}/{24,5}\n= 6,74 × 10⁻³ mol\n"
        "n(Aℓ) = {2}/{3} n(H₂) = {2}/{3}(6,74 × 10⁻³)\n= 4,49 × 10⁻³ mol\nn(Aℓ) = {m}/{M}: 4,49 × 10⁻³ = {m}/{27}\nm(Aℓ) used = 0,12 g\n"
        "m(Aℓ) at 5 min = m(Aℓ) used\n= 0,12 g"], 2,                                              # the Aℓ used taken as the Aℓ left
        ["Find the volume of H₂ formed in the first 5 minutes, then its number of moles.", "Use the balanced equation for the mole ratio of Aℓ to H₂."]),
    # (was "2 mol Aℓ make 3 mol H₂; subtract the Aℓ used from the 0,5 g at the start.": it ruled out two of the three wrong workings)
    rub("5.1.3", "Assume that the concentration of the HCℓ(aq) stays constant for the duration of the reaction. Use the collision theory to explain the change in "
        "the reaction rate from t = 0 to t = 5 minutes.", 4,
        ["The surface area / contact area / mass / size of the aluminium decreases (1)", "Fewer particles are exposed (1)",
         "Fewer effective collisions per unit time OR a lower frequency of effective collisions (1)", "The reaction rate decreases / slows down (1)"],
        ["The acid's concentration stays the same: what happens to the aluminium as it reacts?", "How does the number of exposed particles affect the "
         "number of effective collisions per second?"]),   # (was "Less aluminium exposed means fewer effective collisions per second.")
    draw("5.1.4", "Experiment I is repeated using a 2 mol·dm⁻³ HCℓ solution (Experiment II). Redraw the above graph (NO numerical values need to be shown) and "
         "label the curve A. On the same set of axes, draw the curve that will be obtained for Experiment II. Label this as curve B.", 2,
         [["Curve B starts at the origin and ends at the same point (volume) as curve A", 1], ["The gradient of curve B is steeper for the whole duration", 1]],
         ["Which reactant is limiting: does the final volume of H₂ change?", "How does a more concentrated acid change the rate, and so the gradient?"],
         memo="Graph not labelled: max 1/2."),   # (was "... the final volume stays the same." + "... reacts faster.": both criteria)
    mcq("5.1.5", "Experiment I is repeated using 0,5 g pure powdered Aℓ (Experiment III). How will the volume of H₂(g) produced in Experiment III compare to that "
        "in Experiment I? Choose from GREATER THAN, LESS THAN or EQUAL TO.", ["Greater than", "Less than", "Equal to"], 2,
        ["Which reactant is limiting, and is its mass the same in Experiments I and III?", "Does powdering change how fast the H₂ forms, how much "
         "forms, or both?"], marks=1),   # (was "The same mass of aluminium makes the same amount of H₂.": the answer)
]
q5b = [
    # one term (the memo: "An increase in temperature"): multiple choice of the conditions a learner might name; a catalyst and more
    # particles are clearly not it (a catalyst leaves the curve as it is; more particles raise the whole curve, the peak in place)
    mcq("5.2.1", "What change was made to obtain curve Y?", ["The temperature was decreased.", "The temperature was increased.", "A catalyst was added.",
                                                              "More reactant particles were added."], 1,
        ["Which condition sets the average kinetic energy of the particles?", "Is the area under the two curves, the number of particles, the same?"],
        marks=1),   # (was "Curve Y has more particles at high kinetic energy.": 5.2.2's answer)
    rub("5.2.2", "Give a reason for the answer to QUESTION 5.2.1.", 1,
        ["Curve Y has its peak at a higher kinetic energy / the peak shifted to the right OR the (average) kinetic energy of the particles increases / more "
         "particles have higher kinetic energy. (1)"],
        ["Compare the positions and the heights of the two peaks.", "What does the position of a peak tell you about the kinetic energy of the "
         "particles?"]),   # (was "What does a peak further right mean ...?": the answer)
]

# ---- QUESTION 6, the question paper pages 13-14 and the memo pages 13-21 ----
q6a = [
    rub("6.1.1", "Define the term chemical equilibrium.", 2,
        ["(The dynamic equilibrium when) the rate of the forward reaction equals the rate of the reverse reaction. (2 or 0)",
         "OR — The stage in a chemical reaction when the concentrations of the reactants and products remain constant. (2)"],
        ["Does the reaction stop at equilibrium, or do both reactions keep going?", "What can you say about the amounts of the reactants and products "
         "once equilibrium is reached?"], each=2),
    mcq("6.1.2", "At t₁, oxygen, O₂(g), was added to the container. Write down the letter that represents O₂(g). Choose from X, Y or Z.", ["X", "Y", "Z"], 0,
        ["Adding a gas makes its concentration change suddenly, not gradually.", "After O₂ is added, the forward reaction is favoured: which "
         "lines should then rise, and which fall?"], marks=1),   # (was "Look just after t₁: which line changes suddenly?": the reading)
    mcq("6.1.3", "At t₂, the pressure is adjusted by changing the volume of the container. Was the pressure INCREASED or DECREASED?", ["Increased", "Decreased"], 1,
        ["How does changing the volume of the container change the concentrations of all the gases at once?", "Look at all three lines at the moment "
         "t₂: what happens to them together?"], marks=1),
    rub("6.1.4", "Give a reason for the answer to QUESTION 6.1.3.", 1, ["The concentrations of (all) the gases decreased / the reverse reaction was favoured. (1)"],
        ["What happened to all three lines at the moment t₂?", "After t₂, which reaction did the system favour: the one that makes more or fewer moles "
         "of gas?"]),   # (was "A bigger volume lowers every concentration.": the answer)
    term("6.1.5", "Write down the NAME or FORMULA of the gas that is represented by the letter Z.", ["CO", "carbon monoxide"],
         ["Which gases are the reactants, and which is the product?", "After t₂ and at t₃, which line changes in the same direction as the O₂ line?"]),
    # (was "X is O₂.": 6.1.2's answer)
    rub("6.1.6", "Give a reason for the answer to QUESTION 6.1.5.", 1,
        ["The concentration of Z (CO) decreased with a decrease in the concentration of X (O2) (or increased with an increase) / Z follows the same "
         "trend as X (O2) / Z and X are both reactants / Y (CO2) is the product OR the reverse reaction is favoured to increase the number of moles. (1)"],
        ["After t₂ and at t₃, does Z's line move with X's line or against it?", "Which gases are on the same side of the equation?"]),
    # (was "Reactants rise and fall together.": the answer)
    mcq("6.1.7", "What change in temperature is made at t₃? Choose between INCREASED or DECREASED.", ["Increased", "Decreased"], 1,
        ["Which reaction, forward or reverse, does the graph show is favoured after t₃?", "Is the forward reaction exothermic or endothermic, and which "
         "reaction does each temperature change favour?"], marks=1),
    # (was "After t₃ the product's concentration rises." + "ΔH < 0: which temperature change favours the forward (exothermic) reaction?")
    rub("6.1.8", "Use Le Chatelier's principle to explain the answer to QUESTION 6.1.7.", 3,
        ["The concentration of the product (Y / CO2) increases OR the concentration of the reactants (X / Z / CO / O2) decreases OR the forward reaction is favoured (1)",
         "The forward reaction is exothermic (1)", "A decrease in temperature favours the exothermic reaction (1)"],
        ["What does the graph show after t₃: which reaction was favoured?", "Which reaction is exothermic, and which reaction does a lower temperature "
         "favour?"]),
]
q6b = [
    # the memo's first working (reactants used, calculations using moles, x the change: 6,44 g; range 6,44 - 6,72 g, its other
    # workings 6,72 g and 6,53 g): every wrong working ends outside the range. (Moles not divided by the 2 dm³ is no wrong option:
    # the volume cancels here, 1 + 1 → 1 + 1.)
    work("6.2", "Carbon monoxide gas, CO(g), reacts with water vapour, H₂O(g), at T °C. The reaction reaches chemical equilibrium according to the balanced "
         "equation: CO(g) + H₂O(g) ⇌ CO₂(g) + H₂(g). Initially, 0,6 moles of CO(g), 0,6 moles of H₂O(g), 0,1 moles of carbon dioxide gas, CO₂(g), and 0,1 "
         "moles of hydrogen gas, H₂(g), were mixed and sealed in a 2 dm³ flask. If the equilibrium constant, Kc, for this reaction at T °C is 4, calculate "
         "the mass of CO(g) present in the flask at equilibrium.", 9, [
        "Ratio CO : H₂O : CO₂ : H₂ = 1 : 1 : 1 : 1\nAt equilibrium: n(CO) = n(H₂O) = 0,6 − x; n(CO₂) = n(H₂) = 0,1 + x\n"
        "c = {n}/{V}: each amount divided by 2 dm³\nKc = {[CO₂][H₂]}/{[CO][H₂O]}\n4 = {((0,1 + x)/2)²}/{((0,6 − x)/2)²}\nx = 0,37 mol\n"
        "n(CO) at equilibrium = 0,6 − 0,37\n= 0,23 mol\nn = {m}/{M}: 0,23 = {m}/{28}\nm(CO) = 6,44 g",              # the memo
        "Ratio CO : H₂O : CO₂ : H₂ = 1 : 1 : 1 : 1\nAt equilibrium: n(CO) = n(H₂O) = 0,6 − x; n(CO₂) = n(H₂) = 0,1 + x\n"
        "c = {n}/{V}: each amount divided by 2 dm³\nKc = {[CO][H₂O]}/{[CO₂][H₂]}\n4 = {((0,6 − x)/2)²}/{((0,1 + x)/2)²}\nx = 0,13 mol\n"
        "n(CO) at equilibrium = 0,6 − 0,13\n= 0,47 mol\nn = {m}/{M}: 0,47 = {m}/{28}\nm(CO) = 13,16 g",             # Kc inverted
        "Ratio CO : H₂O : CO₂ : H₂ = 1 : 1 : 1 : 1\nAt equilibrium: n(CO) = n(H₂O) = 0,6 − x; n(CO₂) = n(H₂) = x\n"
        "c = {n}/{V}: each amount divided by 2 dm³\nKc = {[CO₂][H₂]}/{[CO][H₂O]}\n4 = {(x/2)²}/{((0,6 − x)/2)²}\nx = 0,4 mol\n"
        "n(CO) at equilibrium = 0,6 − 0,4\n= 0,2 mol\nn = {m}/{M}: 0,2 = {m}/{28}\nm(CO) = 5,6 g",                  # the initial CO₂ and H₂ left out
        "Ratio CO : H₂O : CO₂ : H₂ = 1 : 1 : 1 : 1\nAt equilibrium: n(CO) = n(H₂O) = 0,6 − x; n(CO₂) = n(H₂) = 0,1 + x\n"
        "c = {n}/{V}: each amount divided by 2 dm³\nKc = {[CO₂][H₂]}/{[CO][H₂O]}\n4 = {((0,1 + x)/2)²}/{((0,6 − x)/2)²}\nx = 0,37 mol\n"
        "n(CO) at equilibrium = x\n= 0,37 mol\nn = {m}/{M}: 0,37 = {m}/{28}\nm(CO) = 10,36 g"], 0,                  # the CO that reacted, not what is left
        ["Set up a table of initial, change and equilibrium amounts for all four gases: in what ratio do they react?",
         "Kc uses equilibrium concentrations: divide each amount by the volume of the flask."]),
    # (was "√4 = 2 = (0,1 + x)/(0,6 − x): solve for x.": it ruled out two of the three wrong workings outright)
]

# ---- QUESTION 7, the question paper page 15 and the memo pages 22-25 ----
q7 = [
    rub("7.1", "Define the term weak base.", 2,
        ["Weak bases dissociate / ionise incompletely / partially in water (1)", "to form a low concentration of hydroxide/OH- ions (1)"],
        ["Compare a weak base with a strong base.", "How completely does it ionise in water, and which ions does it form?"]),
    # the memo: HCO₃⁻(aq) only (a name for a FORMULA question, "hydrogen carbonate", was accepted: dropped 2026-10-11)
    term("7.2", "Write down the formula of the conjugate acid of the carbonate ion, CO₃²⁻(aq).", ["HCO3-", "HCO3"],
         ["How does an acid differ from its conjugate base?", "What happens to the charge of a particle when it gains an H⁺?"], strict=True),
    # (was "Add H⁺ to CO₃²⁻.": the answer in one step)
    num("7.3.1", "Determine the value of p.", 26.55, 0.01, "cm³",
        ["p is run 1's final burette reading.", "How are the initial reading, the final reading and the volume used related?"]),
    num("7.3.2", "Determine the value of q.", 28.15, 0.01, "cm³",
        ["q is run 2's initial burette reading.", "How are the initial reading, the final reading and the volume used related?"]),
    rub("7.4", "METHYL ORANGE is used as the indicator. Explain why methyl orange is the most suitable indicator for this titration by referring to the pH at the "
        "equivalence point.", 2,
        ["The equivalence point is at a pH less than 7 OR the solution at the equivalence point is acidic (a strong acid with a weak base) (1)",
         "Methyl orange changes colour in this (acidic) pH range / at a pH less than 7 (1)"],
        ["HCℓ is a strong acid; K₂CO₃ is a weak base.", "Where is the equivalence point, and where does methyl orange change colour?"]),
    # the memo's Option 1 (0,0622 mol·dm⁻³; range 0,06 - 0,0625, its 20,05 or 20,15 used -1 also inside it): every wrong working ends
    # outside the range
    work("7.5", "Calculate the concentration of the K₂CO₃ solution.", 5, [
        "{caVa}/{cbVb} = {na}/{nb}\n{(0,1)(25)}/{cb(20,1)} = {1}/{2}\n[K₂CO₃] = 0,249 mol·dm⁻³",       # the 1 : 2 mole ratio inverted
        "{caVa}/{cbVb} = {na}/{nb}\n{(0,1)(20,1)}/{cb(25)} = {2}/{1}\n[K₂CO₃] = 0,0402 mol·dm⁻³",      # the acid's and the base's volumes swapped
        "{caVa}/{cbVb} = {na}/{nb}\n{(0,1)(25)}/{cb(26,55)} = {2}/{1}\n[K₂CO₃] = 0,0471 mol·dm⁻³",     # run 1's final reading, p, used as the volume
        "{caVa}/{cbVb} = {na}/{nb}\n{(0,1)(25)}/{cb(20,1)} = {2}/{1}\n[K₂CO₃] = 0,0622 mol·dm⁻³"], 3,  # the memo
        ["Which volume of the K₂CO₃ solution do you use, given two runs?", "Read the balanced equation: how many mol HCℓ react with 1 mol K₂CO₃?"]),
    # (was "Use the average volume of K₂CO₃ from the two runs." + "1 mol K₂CO₃ reacts with 2 mol HCℓ.": it ruled out two wrong workings)
    # the memo's Option 1 (x = 2, positive marking from 7.5): it shows 7.5's 0,0622 mol·dm⁻³, so it opens after 7.5 (GATES)
    work("7.6", "The above K₂CO₃ solution used in the titration was prepared by completely dissolving 6,525 g of the hydrated potassium carbonate, K₂CO₃·xH₂O, "
         "in 600 cm³ water. Calculate the value of x in the formula K₂CO₃·xH₂O.", 5, [
        "c = {m}/{MV}\n0,0622 = {6,525}/{M(0,6)}\nM = 174,84 g·mol⁻¹\n39 + 12 + 3(16) + x(18) = 174,84\nx = 4",              # K counted once
        "c = {m}/{MV}\n0,0622 = {6,525}/{M(0,6)}\nM = 174,84 g·mol⁻¹\n2(39) + 12 + 3(16) + x(18) = 174,84\nx = 2",           # the memo
        "c = {m}/{MV}\n0,0622 = {6,525}/{M(0,6)}\nM = 174,84 g·mol⁻¹\n2(39) + 12 + 3(8) + x(10) = 174,84\nx = 6",            # O's atomic number, 8, as its M
        "c = {m}/{MV}\n0,0622 = {6,525}/{M(0,6)}\nM = 174,84 g·mol⁻¹\nx(18) = 174,84\nx = 10"], 1,                         # the K₂CO₃ left out
        ["Which volume did the 6,525 g dissolve in, in dm³?", "Work out the molar mass of K₂CO₃ from the periodic table first: count every atom."]),
    # (was "M(K₂CO₃) = 138 g·mol⁻¹ and M(H₂O) = 18 g·mol⁻¹.": it ruled out two of the three wrong workings outright)
]

# ---- QUESTION 8, the question paper page 16 and the memo page 26 ----
q8 = [
    rub("8.1.1", "Use oxidation numbers for EACH of the reactants and explain why this reaction is a redox reaction.", 2,
        ["The oxidation number of H changes from +1 to 0 / decreases (1)", "The oxidation number of Mg changes from 0 to +2 / increases (1)"],
        ["What are the oxidation numbers of Mg and of H, before and after the reaction?", "Which one goes up (oxidised), and which goes down (reduced)?"]),
    term("8.1.2", "Write down the FORMULA of the oxidising agent in this reaction.", ["H+", "HCl", "HCℓ", "H3O+"],
         ["The oxidising agent is itself reduced.", "Which reactant's oxidation number decreases?"]),
    rub("8.1.3", "It is observed that dilute hydrochloric acid does not react with copper, Cu(s), at 25 °C. Explain this observation by referring to the relative "
        "strengths of the reducing agents.", 2,
        ["Cu/copper is a weaker reducing agent than hydrogen/H2 (and will not reduce H+ to H2). (2)",
         "OR — Cu/copper is too weak a reducing agent to reduce H+ (to H2). (2)"],
        ["Find Cu and H₂ in Table 4.", "Compare them as reducing agents."], each=2),
    rub("8.1.4", "Will dilute nitric acid, HNO₃(aq), react with copper, Cu(s), at 25 °C? Choose from YES or NO. Explain the answer in terms of the relative "
        "strengths of the oxidising agents.", 3,
        ["Yes (1)", "NO3-/NO₃⁻/nitrate ion/nitric acid is a stronger oxidising agent (1)", "than Cu2+/Cu²⁺/copper(II) ion (so Cu is oxidised to Cu²⁺) (1)"],
        ["Find NO₃⁻ and Cu²⁺ in Table 4.", "Compare them as oxidising agents."]),
    # a balanced equation as multiple choice (2026-10-11): the memo's equation (reactants, products, balancing: 3 marks, played all or
    # nothing) and three wrong ones: the cell run backwards (the cathode's reaction at the anode), the electrons not balanced (one
    # Fe³⁺ for each Pb), and the wrong iron couple (Fe²⁺/Fe, not Fe³⁺/Fe²⁺ on Pt). The memo ignores ⇌ and phases: none of these differs
    # from the right one only in those.
    mcq("8.2.1", "A galvanic cell is represented by the following cell notation: Pb(s) | Pb²⁺(aq) || Fe³⁺(aq), Fe²⁺(aq) | Pt(s). Write down the balanced net "
        "ionic equation for this cell.", [
        "Pb²⁺(aq) + 2Fe²⁺(aq) → Pb(s) + 2Fe³⁺(aq)", "Pb(s) + Fe³⁺(aq) → Pb²⁺(aq) + Fe²⁺(aq)", "Pb(s) + 2Fe³⁺(aq) → Pb²⁺(aq) + 2Fe²⁺(aq)",
        "Pb(s) + Fe²⁺(aq) → Pb²⁺(aq) + Fe(s)"], 2,
        ["In cell notation, which half-cell is written on the left, and what happens there?", "How many electrons does each half-reaction transfer? "
         "Make them equal."], marks=3),
    # (was "... each Fe³⁺ takes one.": with the first clue it ruled out every wrong equation)
    mcq("8.2.2", "A stronger reducing agent is now used with the same oxidising agent under the same conditions. How will this affect the initial emf of the cell? "
        "Choose from INCREASES, DECREASES or NO EFFECT.", ["Increases", "Decreases", "No effect"], 0,
        ["How does the E° of a stronger reducing agent's half-cell compare with the E° of a weaker one?", "With the same cathode, what happens to "
         "E°cathode − E°anode?"], marks=1),
]

# ---- QUESTION 9, the question paper page 17 and the memo pages 27-28 ----
q9a = [
    # decide by calculation (the memo's Option 1, −0,93 V, non-spontaneous): the conclusion is a line of each working, so a right
    # number with the wrong conclusion is a wrong option. (The paper prints "2Ag⁺(s)"; the stem writes (aq), the ion in solution.)
    work("9.1", "A strip of silver is added to a 1 mol·dm⁻³ solution of Pb(NO₃)₂ at 25 °C. Consider the reaction below: 2Ag(s) + Pb²⁺(aq) → 2Ag⁺(aq) + Pb(s). "
         "By means of a calculation, determine whether this reaction is SPONTANEOUS or NON-SPONTANEOUS.", 5, [
        "E°cell = E°reduction − E°oxidation\n= 0,80 − (−0,13)\n= 0,93 V\n∴ spontaneous",           # Ag⁺ taken as reduced: the half-cells swapped
        "E°cell = E°reduction − E°oxidation\n= −0,13 − (0,80)\n= −0,93 V\n∴ non-spontaneous",      # the memo
        "E°cell = E°reduction − E°oxidation\n= −0,13 − 2(0,80)\n= −1,73 V\n∴ non-spontaneous",     # E° multiplied by the coefficient 2
        "E°cell = E°reduction − E°oxidation\n= −0,13 − (0,80)\n= −0,93 V\n∴ spontaneous"], 1,     # a negative E°cell read as spontaneous
        ["In the reaction as written, which species gains electrons and which loses them?", "What sign does E°cell have for a spontaneous reaction?"]),
    # (was "Pb²⁺ is reduced (cathode); Ag is oxidised (anode)." + "A negative E°cell means the reaction is not spontaneous.": they ruled out
    # two of the three wrong workings)
]
q9b = [
    rub("9.2.1", "Define an electrolyte.", 2,
        ["ANY ONE: a substance of which the (aqueous) solution contains ions (2)",
         "OR — a substance that dissolves in water to give a solution that conducts electricity (2)",
         "OR — a substance that forms ions in water / when melted (2)", "OR — a solution / substance that conducts electricity through the movement of ions (2)"],
        ["Think of what happens to table salt, NaCℓ, when it dissolves in water.", "Which particles carry the charge through a solution?"], each=2),
    # (was "It is about ions." + "What does its solution contain, or do?": between them every wrong card was out)
    # a half-reaction as multiple choice (2026-10-11), 2 marks all or nothing: the memo's 2Cℓ⁻ → Cℓ₂ + 2e⁻ and three wrong ones: the
    # reduction, the oxidation of water (not the predominant one in CONCENTRATED NaCℓ) and the electrons not balanced. The memo's
    # other marks (Cℓ₂ + 2e⁻ ← 2Cℓ⁻ 2/2; 2Cℓ⁻ ⇌ Cℓ₂ + 2e⁻ 1/2) are never wrong options.
    mcq("9.2.2", "Write down the PREDOMINANT oxidation half-reaction that takes place in this cell.", [
        "Cℓ₂ + 2e⁻ → 2Cℓ⁻", "2Cℓ⁻ → Cℓ₂ + 2e⁻", "2H₂O → O₂ + 4H⁺ + 4e⁻", "2Cℓ⁻ → Cℓ₂ + e⁻"], 1,
        ["Is oxidation a loss or a gain of electrons?", "In concentrated NaCℓ(aq), which negative ions are present in large numbers to give up "
         "electrons?"], marks=2),   # (was "In concentrated NaCℓ, chloride ions are oxidised.": the answer)
    lst("9.2.3", "Write down the NAMES or FORMULAE of the products formed at electrode Q.", 2,
        [["hydrogen (gas)", "H2"], ["hydroxide (ions)", "OH-", "sodium hydroxide", "NaOH"]],
        ["Is electrode Q the anode or the cathode? Look at the battery.", "Which species near Q is reduced, Na⁺ or H₂O? Use Table 4."]),
    # (was "Water is reduced there: what does it form?": 9.2.4's answer)
    rub("9.2.4", "Explain the answer to QUESTION 9.2.3 by referring to the relative strengths of the oxidising agents involved.", 2,
        ["Water/H2O is a stronger oxidising agent than Na+/sodium ions (1)", "so water / H2O is reduced (1)"],
        ["Which is the stronger oxidising agent in Table 4, H₂O or Na⁺?", "What happens to the stronger oxidising agent at the cathode?"]),
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
     # (the readings only: was "steep at first and levelling off", 5.1.3's answer in words)
     "figure": fig("Q5", "Volume of H₂ (dm³) against time (minutes): a curve from the origin, with a dot on it at t = 5 minutes and a dashed line from "
                         "the dot down to the time axis."), "items": q5a},
    {"id": "5.2", "title": "Question 5", "kind": "Reaction rates", "marks": 2,
     "lead": "Curve X is the Maxwell-Boltzmann distribution curve for a reaction under a set of reaction conditions. A change was made to one of the reaction "
             "conditions to obtain curve Y.",
     # (was "... curve Y has a lower, wider peak further to the right.": 5.2.2's answer, the memo's words)
     "figure": fig("Q5.2", "Number of particles against kinetic energy: two curves from the origin, curve X (dashed) and curve Y (solid), each with one "
                           "peak; they cross once."), "items": q5b},
    {"id": "6", "title": "Question 6", "kind": "Chemical equilibrium", "marks": 11,
     "lead": "The reaction of carbon monoxide gas, CO(g), with oxygen gas, O₂(g), is investigated. The reaction reaches equilibrium in a closed container at "
             "constant temperature T °C, according to the balanced equation: 2CO(g) + O₂(g) ⇌ 2CO₂(g), ΔH < 0. Changes to the conditions of equilibrium "
             "are made at different times. The graph shows the results obtained. X, Y and Z represent the gases in the above reaction.",
     # (was "At t₁ X jumps up ...; at t₂ all three drop; at t₃ X and Z fall a little and Y rises": the answers to 6.1.2, 6.1.4 and 6.1.8)
     "figure": fig("Q6", "Concentration (mol·dm⁻³) against time (minutes): three lines, X (solid, top), Y (dashed, middle) and Z (dotted, bottom), level "
                         "at first; dotted vertical lines mark t₁, t₂ and t₃, where the lines change."),
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

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Business Studies P2 2025 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, another term's definition, the opposite choice, the reversed reasoning):
# never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns `each`;
# the cards are shuffled the same way every run. The rubric bullets above stay as the source. Where the memo gives ONE mark for
# "A / B" forms of a point (4.2's "bonded to one other C atom / the first C atom", 6.1.8's three forms of its first point, 9.2.4's
# "Na⁺ is a weaker oxidising agent" OR), one form is a card: two right cards for one mark would let two picks earn two marks.


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("ps-p2-2024-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    # 2, key phrases (same molecular formula, different functional groups): the wrong ones are positional and chain isomers, a
    # homologous series, and a self-contradiction
    "2.3.1": (2, ["Compounds with the same molecular formula, but different functional groups."],
                 ["Compounds with the same molecular formula, but with the same functional group on a different carbon atom.",
                  "Compounds with the same molecular formula and the same functional group, but a different chain (branching).",
                  "Compounds with the same functional group, but different molecular formulae.",
                  "Compounds with the same structural formula, but different molecular formulae."]),
    # 2, key phrases (pressure exerted by a vapour, at equilibrium with its liquid, closed system): the wrong ones open the system,
    # are the boiling point, a liquid's pressure, the atmosphere's
    "3.1": (2, ["The pressure exerted by a vapour at equilibrium with its liquid in a closed system."],
               ["The pressure exerted by a vapour at equilibrium with its liquid in an open container.",
                "The temperature at which the vapour pressure of a liquid equals the atmospheric pressure.",
                "The pressure exerted by a liquid on the bottom of its container.",
                "The pressure of the atmosphere on the surface of a liquid."]),
    # 3 ticks: structure (its "more branched / smaller surface area" forms are one point: one card), forces, energy
    "3.2.2": (1, ["Compound C is more branched than compounds A and B: it has a smaller surface area.",
                  "Compound C has weaker intermolecular forces than compounds A and B.",
                  "Less energy is needed to overcome the intermolecular forces in compound C than in compounds A and B."],
                 ["Compound C is less branched than compounds A and B: it has a larger surface area.",
                  "Compound C has stronger intermolecular forces than compounds A and B.",
                  "More energy is needed to overcome the intermolecular forces in compound C than in compounds A and B.",
                  "Compound C has a greater molar mass than compounds A and B."]),
    # 4 ticks: the force in D, the force in E, the comparison, the energy (its OR forms, "E's forces are weaker" and "less energy for
    # E", are true and are no wrong cards; the wrong comparison cards are the reverse)
    "3.3.2": (1, ["Compound D (propanoic acid) has hydrogen bonding between its molecules.",
                  "Compound E (butanal) has dipole-dipole forces between its molecules.",
                  "The intermolecular forces in compound D are stronger than those in compound E.",
                  "More energy is needed to overcome the intermolecular forces in compound D than in compound E."],
                 ["Compound E (butanal) has hydrogen bonding between its molecules.",
                  "The intermolecular forces in compound E are stronger than those in compound D.",
                  "Less energy is needed to overcome the intermolecular forces in compound D than in compound E.",
                  "Compound D has only London forces between its molecules."]),
    # 2, key phrases (longer chain hydrocarbon molecules, broken down, shorter molecules): as P2 Nov 2025's 4.2.1
    "4.1": (2, ["The chemical process in which longer chain hydrocarbon molecules are broken down to shorter (more useful) molecules."],
               ["The chemical process in which shorter chain hydrocarbon molecules are joined to form longer molecules.",
                "The chemical process in which hydrocarbon molecules react with oxygen to form carbon dioxide and water.",
                "The process in which longer chain hydrocarbon molecules are separated by their boiling points, without breaking any bonds.",
                "The chemical process in which hydrogen is added to an unsaturated hydrocarbon to form a saturated one."]),
    # 2 ticks: the choice and ONE form of the reason
    "4.2": (1, ["It is a primary haloalkane.", "The bromine atom is bonded to a C atom that is bonded to one other C atom."],
               ["It is a secondary haloalkane.", "It is a tertiary haloalkane.",
                "The bromine atom is bonded to a C atom that is bonded to two other C atoms.",
                "The bromine atom is bonded to a C atom that is bonded to three other C atoms."]),
    # 2 or 0, any one of its forms (two as cards): as P2 Nov 2025's 5.1 (the same memo)
    "5.1.1": (2, ["The change in concentration of products or reactants per unit time.",
                  "The amount of products formed or reactants used per unit time."],
                 ["The change in concentration of products or reactants per unit volume.",
                  "The total change in concentration of products or reactants during a reaction.",
                  "The total time taken for all the reactants to be used up.",
                  "The minimum energy that colliding particles need for a reaction to take place."]),
    # 4 ticks, the memo's collision-theory chain; the wrong ones its reverse
    "5.1.3": (1, ["The surface area of the aluminium decreases.", "Fewer aluminium particles are exposed to the acid.",
                  "There are fewer effective collisions per unit time.", "The reaction rate decreases."],
                 ["The surface area of the aluminium increases.", "More aluminium particles are exposed to the acid.",
                  "There are more effective collisions per unit time.", "The reaction rate increases."]),
    # 1, either OR form (two as cards): the wrong ones misread the peaks or confuse temperature with a catalyst
    "5.2.2": (1, ["Curve Y has its peak at a higher kinetic energy.", "More particles have a higher kinetic energy."],
                 ["Curve Y has its peak at a lower kinetic energy.", "Curve Y has a higher peak than curve X.",
                  "Fewer particles have a high kinetic energy.", "The activation energy of the reaction is lower for curve Y."]),
    # 2 or 0, either OR form: the wrong ones are equal concentrations, the reactions stopping, unequal rates, Le Chatelier's principle
    "6.1.1": (2, ["The dynamic equilibrium when the rate of the forward reaction equals the rate of the reverse reaction.",
                  "The stage in a chemical reaction when the concentrations of the reactants and products remain constant."],
                 ["The stage in a chemical reaction when the concentrations of the reactants and products are equal.",
                  "The stage in a chemical reaction when the forward and the reverse reactions stop.",
                  "The stage when the rate of the forward reaction is greater than the rate of the reverse reaction.",
                  "The state in which a closed system opposes a disturbance by favouring the reaction that cancels it."]),
    # 1, either form of the memo's reason (two as cards)
    "6.1.4": (1, ["The concentrations of all the gases decreased.", "The reverse reaction was favoured."],
                 ["The concentrations of all the gases increased.", "The forward reaction was favoured.",
                  "Only the concentration of the product decreased.", "The temperature of the container was decreased."]),
    # 1, two of the memo's forms as cards; they name Z (CO) and X (O₂), so it opens after 6.1.2 and 6.1.5 (GATES). "The forward
    # reaction is favoured to increase the number of moles" reverses the memo's last form (the forward reaction lowers it)
    # (its "Z follows the same trend as X" form is no card: at t₁ X jumps up while Z falls, so a learner reading the graph would doubt
    # a true card; its first form holds at every change)
    "6.1.6": (1, ["The concentration of Z decreased when the concentration of X (O₂) decreased.",
                  "Z (CO) and X (O₂) are both reactants; Y (CO₂) is the product."],
                 ["The concentration of Z increased when the concentration of X (O₂) decreased at t₃.", "Z is the product of the reaction.",
                  "The concentration of Z increased when O₂ was added at t₁.", "The forward reaction is favoured to increase the number of moles."]),
    # 3 ticks: the product's concentration (one of its OR forms; no letter, so the card does not say which line is CO₂), exothermic,
    # a lower temperature favours the exothermic reaction
    "6.1.8": (1, ["The concentration of the product, CO₂, increases.", "The forward reaction is exothermic.",
                  "A decrease in temperature favours the exothermic reaction."],
                 ["The concentration of the product, CO₂, decreases.", "The forward reaction is endothermic.",
                  "A decrease in temperature favours the endothermic reaction.", "A decrease in temperature increases the rate of the forward reaction."]),
    # 2 ticks in one sentence (ionises incompletely in water; a low concentration of OH⁻): one card for 2. The wrong ones are a strong
    # base, a weak acid, a dilute base, a proton donor
    "7.1": (2, ["A weak base ionises incompletely in water to form a low concentration of hydroxide (OH⁻) ions."],
               ["A weak base ionises completely in water to form a high concentration of hydroxide (OH⁻) ions.",
                "A weak base ionises incompletely in water to form a low concentration of hydronium (H₃O⁺) ions.",
                "A weak base is a solution that contains only a small amount of base dissolved in a lot of water.",
                "A weak base is a substance that donates protons (H⁺ ions) to water."]),
    # 2 ticks: the equivalence point below pH 7 (its "acidic / strong acid with a weak base" forms in one card), methyl orange's range
    "7.4": (1, ["The equivalence point is at a pH less than 7: a strong acid reacts with a weak base.",
                "Methyl orange changes colour at a pH less than 7."],
               ["The equivalence point is at a pH greater than 7.", "The equivalence point is at a pH of exactly 7.",
                "Methyl orange changes colour at a pH greater than 7.", "Methyl orange is used because K₂CO₃ is a strong base."]),
    # 2 ticks: H from +1 to 0, Mg from 0 to +2
    "8.1.1": (1, ["The oxidation number of H changes from +1 to 0.", "The oxidation number of Mg changes from 0 to +2."],
                 ["The oxidation number of H changes from 0 to +1.", "The oxidation number of Mg changes from +2 to 0.",
                  "The oxidation number of Cℓ changes from −1 to 0.", "The oxidation number of Mg changes from 0 to +1."]),
    # 2 ticks in one sentence (a weaker reducing agent; than H₂): one card for 2, its OR form a second right card
    "8.1.3": (2, ["Cu is a weaker reducing agent than H₂, so it will not reduce H⁺ to H₂.", "Cu is too weak a reducing agent to reduce H⁺ to H₂."],
                 ["Cu is a stronger reducing agent than H₂, so H⁺ cannot oxidise it.", "H₂ is a weaker reducing agent than Cu, so Cu cannot be oxidised.",
                  "Cu²⁺ is a weaker oxidising agent than H⁺, so the copper does not react.",
                  "Dilute hydrochloric acid is too weak an acid to react with any metal."]),
    # 3 ticks: "Yes", and the comparison's two ticks (a stronger oxidising agent; than Cu²⁺) as its two directions, one card each, so
    # the comparison earns 2 as in the memo; the wrong ones are "No" and the comparison reversed both ways
    "8.1.4": (1, ["Yes, dilute nitric acid reacts with copper.", "NO₃⁻ is a stronger oxidising agent than Cu²⁺.",
                  "Cu²⁺ is a weaker oxidising agent than NO₃⁻."],
                 ["No, dilute nitric acid does not react with copper.", "Cu²⁺ is a stronger oxidising agent than NO₃⁻.",
                  "NO₃⁻ is a weaker oxidising agent than Cu²⁺.", "Copper is oxidised by the H⁺ ions of the nitric acid."]),
    # 2 or 0, any one of its four forms (two as cards): as P2 Nov 2025's 8.1
    "9.2.1": (2, ["A substance of which the aqueous solution contains ions.",
                  "A substance that dissolves in water to give a solution that conducts electricity."],
                 ["A substance that conducts electricity through the movement of free electrons, like a metal.",
                  "A substance that dissolves in water to give a solution that does not conduct electricity.",
                  "The electrode at which oxidation takes place.", "A substance that is formed at the cathode during electrolysis."]),
    # 2 ticks: water the stronger oxidising agent (one form), water reduced; they show what forms at Q, so it opens after 9.2.3
    "9.2.4": (1, ["Water is a stronger oxidising agent than Na⁺.", "Water is reduced."],
                 ["Na⁺ is a stronger oxidising agent than water.", "Na⁺ ions are reduced to sodium metal.",
                  "Water is oxidised at electrode Q.", "Cℓ⁻ ions are reduced at electrode Q."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, explanations and choices with reasons), so SORTS stays empty and sort_ is kept for parity.
SORTS = {}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("ps-p2-2024-11:sort:" + n).shuffle(order)
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
GATES = {"2.3.2": ["2.3.1"],             # its clue: same formula, different homologous series (2.3.1's definition)
         "3.2.2": ["3.2.1"],             # its cards: C has the weakest forces (the highest vapour pressure)
         "3.3.2": ["3.3.1"],             # its cards: D's forces are stronger (E boils lower)
         "5.2.2": ["5.2.1"],             # its cards: the peak at a higher kinetic energy (a higher temperature)
         "6.1.4": ["6.1.3"],             # its cards: all the concentrations decreased (the pressure decreased)
         "6.1.6": ["6.1.2", "6.1.5"],    # its cards: X is O₂, Z is CO
         "6.1.8": ["6.1.7"],             # its cards: a decrease in temperature
         "7.6": ["7.5"],                 # its options: [K₂CO₃] = 0,0622 mol·dm⁻³
         "9.2.4": ["9.2.3"]}             # its cards: water is reduced at Q
ITEMS = [i for m in missions for i in m["items"]]
for _it in ITEMS:
    if _it["n"] in GATES:
        _it["after"] = GATES[_it["n"]]
nums = [i["n"] for i in ITEMS]
assert all(nums.index(e) < nums.index(n) for n, es in GATES.items() for e in es), "a gate on a later part"

# every part that played as typed steps before 2026-10-11, now authored multiple choice, the right letter spread over A-D
assert tuple(AUTHORED) == ("5.1.2", "6.2", "7.5", "7.6", "9.1"), AUTHORED
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["7.3.1", "7.3.2"]   # burette readings, no working in the memo: one value each
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == GATES
_at = ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED]
_spread = {k: _at.count(k) for k in "ABCD"}
assert max(_spread.values()) - min(_spread.values()) <= 1, _spread
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Chemistry", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic chemistry errors (a mole ratio inverted, a wrong "
                                                       "formula, the amount used taken as the amount left, Kc inverted, the initial products left "
                                                       "out, the volumes swapped or misread, a molar mass wrong, E° multiplied by a coefficient, a "
                                                       "sign rule reversed), 0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, %d marks). A "
                                                       "value the memo accepts is never a wrong option: 5.1.2's range 0,365 - 0,42 g; 6.2's range "
                                                       "6,44 - 6,72 g; 7.5's range 0,06 - 0,0625 mol·dm⁻³ (its 20,05 / 20,15 forms included)."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions (2.3.1, 3.1, 4.1, 5.1.1, "
                                                    "6.1.1, 7.1, 9.2.1) and 8.1.3's two-tick sentence pick one card for their marks (an OR form "
                                                    "is a second right card); the explanations and the choices with reasons (3.2.2, 3.3.2, 4.2, "
                                                    "5.1.3, 5.2.2, 6.1.4, 6.1.6, 6.1.8, 7.4, 8.1.1, 8.1.4, 9.2.4) pick the choice and the memo's "
                                                    "points, 1 mark each. Where the memo gives one mark for 'A / B' forms of a point, one form is "
                                                    "a card. 8.1.4's comparison earns 2 ticks in the memo (a stronger oxidising agent; than "
                                                    "Cu²⁺): its two directions are its two cards." % len(PICKS)},
        {"n": "8.2.1", "kind": "no_fit", "detail": "A balanced equation (8.2.1, 3 marks) and a half-reaction (9.2.2, 2 marks) play as multiple "
                                                   "choice of four equations, all or nothing: the memo's equation and three wrong ones (8.2.1: "
                                                   "the cell reversed, the electrons not balanced, the wrong iron couple; 9.2.2: the reduction, "
                                                   "water oxidised, the electrons not balanced). The memo's other accepted or part-marked forms "
                                                   "(9.2.2: Cℓ₂ + 2e⁻ ← 2Cℓ⁻ 2/2, 2Cℓ⁻ ⇌ Cℓ₂ + 2e⁻ 1/2) are never wrong options."},
        {"n": "2.3.2", "kind": "no_fit", "detail": "Two letters for one mark (2.3.2) plays as multiple choice of six letter pairs, all or nothing, "
                                                   "as the memo gives the mark for the pair (a pick of two letters gave half a mark for one right "
                                                   "letter). 5.2.1's one-term answer (an increase in temperature) plays as multiple choice."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from the paper and memo PDFs and their page images "
                                                           "(structural formulae are drawings); no API call."},
        {"n": "2.2.1", "kind": "no_fit", "detail": "IUPAC names (2.2.1, 2.2.2, 2.4.4, 4.6.3) and formulas (2.4.1, 4.3.2, 4.4.1, 7.2) play as strict "
                                                   "terms: all or nothing, where the memo gives part marks (stem, substituents, the whole name; "
                                                   "'propanol' 1/2 in 2.4.4, 'butene' 1/2 in 4.6.3)."},
        {"n": "2.4.3", "kind": "no_fit", "detail": "Structural formulae (2.4.3, 4.3.1) and equations in structural formulae (4.6.1, 4.6.2), and the redrawn graph "
                                                   "(5.1.4), are done on paper and self-checked against the memo's criteria."},
        {"n": "7", "kind": "no_fit", "detail": "The titration table is transposed (a run per column): the paper's five columns cut off on a 360 px phone. The "
                                               "values are the paper's."},
        {"n": "7.5", "kind": "memo_issue", "detail": "The memo's criterion (e) names 0,0625 mol·dm⁻³ as the final answer, but both its options end at "
                                                     "0,0622 mol·dm⁻³ (2,5 x 10⁻³ / 2 / 20,1 x 10⁻³); the range 0,06 - 0,0625 covers both. The "
                                                     "right option keeps the working's 0,0622. (7.6's Option 3 writes (1,250 x 10⁻²)(600)/20 for "
                                                     "1,25 x 10⁻³ in 20 cm³: not played.)"},
        {"n": "9.1", "kind": "memo_issue", "detail": "The question paper prints the reaction as 2Ag(s) + Pb²⁺(aq) → 2Ag⁺(s) + Pb(s); the stem writes "
                                                     "2Ag⁺(aq), the silver ion in solution (the memo's own equation has no phases)."},
    ],
}
QTOTAL = {"1": 20, "2": 18, "3": 11, "4": 22, "5": 17, "6": 20, "7": 17, "8": 12, "9": 13}   # the paper's [n] per question
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
out = Path(__file__).parent / "out" / "ps-p2-2024-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
