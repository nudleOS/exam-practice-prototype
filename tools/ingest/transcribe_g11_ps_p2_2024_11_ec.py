"""Grade 11 Physical Sciences P2 (Chemistry) November 2024 (Eastern Cape Department of Education), the whole paper (Questions 1 to 8,
150 marks, 3 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the question paper zip (English PDF, 24 pages, text layer) and the
memo PDF (English and Afrikaans, 11 pages), read from their text and page images.

  python tools/ingest/transcribe_g11_ps_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ps-p2-2024-11-ec/PHYSICAL Sc. P2 QP GR11 NOV 2024 ENG D_watermark.pdf" "uploads/provincial/g11-ps-p2-2024-11-ec/PHYSICAL SCIENCES P2 GR11 MEMO 2024 ENG_AFR_watermark.pdf" --id g11-ps-p2-2024-11-ec --from-json

The rulings as in transcribe_g11_ps_p1_2024_11_ec.py. 'Write down the formula / the shape / the bond' -> an MCQ of answers (the
compound list's own formulae); every drawing (Lewis structures, the gas graph, the energy profile) pick the drawing (pictures_lower.py).
Figure boxes in PDF points (page 595 x 842): the union of each diagram's drawings and labels (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-ps-p2-2024-11-ec", 595.2, 842.0, {"1.7": [5, 126.0, 97.5, 479.9, 257.7], "Q4": [10, 87.5, 131.5, 525.2, 438.1]}, start=2)
work, answer, num, draw, stmt, mcq = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq
YN = ["YES", "NO"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which ONE of the following bonds will have the highest bond energy?", ["H – H", "C – H", "C = C", "C ≡ C"], 3,
        ["How many shared pairs does each bond have?", "More shared pairs: shorter and stronger bond."]),
    mcq("1.2", "Consider the following compounds and their respective boiling points.\nHe: −268,9 °C ; HBr: −66 °C ; HF: 19,5 °C\n"
        "The correct arrangement for the decreasing strength of the intermolecular forces of the given compounds is …",
        ["HF, He, HBr.", "HBr, He, HF.", "HF, HBr, He.", "He, HBr, HF."], 2,
        ["A higher boiling point means stronger intermolecular forces.", "Put the compounds from the highest boiling point down."]),
    mcq("1.3", "Which ONE of the following is NOT a property of the ideal gas?",
        ["There are no forces of attraction between the molecules.", "The collisions between molecules are elastic.",
         "The volume occupied by the gas is equal to the total volume of the gas molecules.", "It has a low density."], 2,
        ["In an ideal gas, how much space do the molecules themselves take up?", "Which statement describes a real gas instead?"]),
    mcq("1.4", "The molar mass of hydrated oxalic acid (COOH)₂·xH₂O is 126 g·mol⁻¹.\nThe number of water molecules (x) present in the hydrated "
        "compound is …", ["1.", "2.", "3.", "4."], 1,
        ["What is the molar mass of (COOH)₂?", "The rest of 126 g·mol⁻¹ is water: how many 18 g·mol⁻¹ is that?"]),
    mcq("1.5", "10 moles of zinc (Zn) are allowed to react with 5 moles of hydrochloric acid (HCℓ) in a test tube according to the balanced "
        "equation:\nZn + 2 HCℓ → ZnCℓ₂ + H₂\nHow many moles of hydrochloric acid (HCℓ) and zinc chloride (ZnCℓ₂) is in the test tube after "
        "the completion of the reaction?",
        ["HCℓ 2,5 and ZnCℓ₂ 2,5", "HCℓ 0 and ZnCℓ₂ 2,5", "HCℓ 5 and ZnCℓ₂ 10", "HCℓ 0 and ZnCℓ₂ 10"], 1,
        ["Which reactant runs out first?", "How many moles of ZnCℓ₂ do 5 moles of HCℓ make?"]),
    mcq("1.6", "Which ONE of the following is the conjugate acid of HPO₄²⁻?", ["PO₄³⁻", "H₂PO₄⁻", "H₃PO₄", "H₂PO₄²⁻"], 1,
        ["A conjugate acid has one more proton than its base.", "What happens to the charge when an H⁺ is added?"]),
    mcq("1.7", "Consider the potential energy versus distance curve below.\n(I) At point A the repulsive forces are stronger than attractive "
        "forces\n(II) Point B represents bond length\n(III) At point C net attractive and repulsive forces is zero\nWhich of the above "
        "statement(s) regarding the above curve is CORRECT?", ["I and II only", "I and III only", "II and III only", "I, II and III"], 3,
        ["Where on the curve are the atoms closest together?", "Where is the potential energy lowest, and what does the distance there "
                                                               "mean?"],
        figure=P.fig("1.7", "A potential energy against distance curve: it falls steeply through A, crosses the distance axis near B, dips "
                            "to its lowest point C, and rises towards D, levelling off near zero.")),
    mcq("1.8", "Which ONE of the following indicates the CORRECT colour of phenolphthalein in HCℓ and NaOH?",
        ["HCℓ yellow; NaOH blue", "HCℓ colourless; NaOH pink", "HCℓ pink; NaOH colourless", "HCℓ blue; NaOH yellow"], 1,
        ["Phenolphthalein changes colour in a base.", "Which colour does it turn there?"]),
    mcq("1.9", "Which ONE of following solutions will have the lowest pH if all solutions have the SAME concentration?",
        ["H₂SO₄ (aq)", "HCℓ (aq)", "NaOH (aq)", "Ba(OH)₂ (aq)"], 0,
        ["The lowest pH means the most H₃O⁺.", "Which acid gives two H⁺ per molecule?"]),
    mcq("1.10", "Consider the following statements regarding a REDUCING AGENT:\n(I) The substance that causes reduction.\n(II) The substance "
        "that is reduced.\n(III) The substance that is oxidised.\nWhich of the above statement(s) regarding the reducing agent is CORRECT?",
        ["I only", "I and II only", "II and III only", "I and III only"], 3,
        ["A reducing agent gives electrons away.", "What happens to a substance that loses electrons?"])]

# ---- QUESTION 2, the question paper pages 7-8 and the memo pages 3-4 ----
COMP = "Consider the following compounds: I₂ ; HOCℓ ; NH₃ ; H₂S ; KBr\n"
q2 = [
    stmt("2.1", "Define covalent bond.", 2, ["The sharing of electrons between two atoms to form a molecule."],
         ["The transfer of electrons from a metal atom to a non-metal atom.", "The attraction between positive ions and a sea of delocalised "
                                                                             "electrons.",
          "The force of attraction between two molecules.", "The sharing of protons between two atoms."],
         ["Is a covalent bond a sharing or a transfer?", "What is shared?"], 2),
    answer("2.2.1", "Write down the formula of the compound from the given list that is non-polar.", 1, ["I₂", "HOCℓ", "NH₃", "H₂S"],
           ["A molecule of two identical atoms has no polar bond.", "Which formula has only one element?"]),
    answer("2.2.2", "Write down the formula of the compound from the given list that forms a bond as a result of transferring of electrons.", 1,
           ["KBr", "I₂", "NH₃", "H₂S"], ["Electrons transfer from a metal to a non-metal.", "Which compound has a metal in it?"]),
    answer("2.2.3", "Write down the formula of the compound from the given list that has one lone pair of electrons.", 1,
           ["NH₃", "H₂S", "HOCℓ", "I₂"], ["How many valence electrons does the central atom have?", "N has 5: 3 bond, how many are left?"]),
    answer("2.2.4", "Write down the formula of the compound from the given list that has a pure covalent bond.", 1, ["I₂", "KBr", "NH₃", "HOCℓ"],
           ["A pure covalent bond has an electronegativity difference of zero.", "Between which atoms is that?"]),
    draw("2.3.1", "Draw the Lewis structure of: HOCℓ", 2, [["H : O : Cℓ with the bonding pairs", 1], ["The lone pairs on O and Cℓ", 1]],
         ["Which atom is in the middle?", "How many lone pairs does each of O and Cℓ keep?"], memo="The memo's structure: H:Ö:Cℓ: (two lone "
                                                                                                  "pairs on O, three on Cℓ)."),
    draw("2.3.2", "Draw the Lewis structure of: H₂S", 2, [["H : S : H with the bonding pairs", 1], ["Two lone pairs on S", 1]],
         ["S is in group 16: how many valence electrons?", "Two bond with H: how many pairs are left?"], memo="The memo's structure: H:S:H with "
                                                                                                              "two lone pairs on S."),
    answer("2.4.1", "The ammonium ion (NH₄⁺) is formed from ammonia (NH₃).\nIdentify the bond responsible for the formation of NH₄⁺.", 1,
           ["Dative covalent (coordinate covalent) bond", "Ionic bond", "Hydrogen bond", "Pure covalent bond"],
           ["Where do both electrons of the new bond come from?", "A bond made from one atom's lone pair has its own name."]),
    draw("2.4.2", "Use the Lewis structure to show the formation of NH₄⁺ from NH₃.", 4,
         [["NH₃ with its lone pair", 1], ["H⁺ with no electrons", 1], ["[NH₄]⁺ in brackets with its charge", 2]],
         ["Which pair of electrons on N is not yet used?", "Does H⁺ bring any electrons?"],
         memo="The memo's drawing: H:N:H with H below and a lone pair on N, + H⁺ → [NH₄]⁺ in brackets."),
    answer("2.5.1", "Write down the molecular shape of: HOCℓ", 1, ["Bent", "Linear", "Trigonal planar", "Tetrahedral"],
           ["How many bonding pairs and lone pairs are on O?", "Two bonds and two lone pairs give which shape?"]),
    answer("2.5.2", "Write down the molecular shape of: NH₃", 1, ["Trigonal pyramidal", "Trigonal planar", "Tetrahedral", "Bent"],
           ["Three bonding pairs and one lone pair on N.", "Does the lone pair push the H atoms down into a pyramid?"]),
    mcq("2.6", "Will I₂ be soluble in CCℓ₄? Write down only YES or NO.", YN, 0,
        ["Is CCℓ₄ polar or non-polar?", "Like dissolves like."], marks=1),
    stmt("2.7", "Explain the answer to QUESTION 2.6 by referring to the molecular polarity and intermolecular forces involved in the compounds.", 3,
         ["I₂ is a non-polar molecule and only contains London forces.", "CCℓ₄ is a non-polar molecule and only contains London forces.",
          "Both are non-polar with only London forces: like dissolves like."],
         ["I₂ is a polar molecule with dipole-dipole forces.", "CCℓ₄ has hydrogen bonds between its molecules.",
          "Non-polar substances dissolve only in polar solvents.", "I₂ forms ionic bonds with CCℓ₄."],
         ["Is I₂ polar? Is CCℓ₄?", "Which intermolecular force does each have?"], 1, after=["2.6"])]
q28 = [
    stmt("2.8.1", "Define the term bond energy.", 2, ["Bond energy is the energy needed to break one mole of its molecules into separate atoms."],
         ["Bond energy is the energy released when one mole of molecules forms from ions.", "Bond energy is the energy stored in the nucleus of "
                                                                                           "an atom.",
          "Bond energy is the energy needed to break one molecule into its ions.", "Bond energy is the heat given off when a substance boils."],
         ["Is energy needed or released to break a bond?", "Into what are the molecules broken?"], 2),
    stmt("2.8.2", "Explain the trend observed in the bond energy in the table above.", 2,
         ["The bond length decreases from C–H to F–H.", "The shorter the bond length, the more energy is needed to break it."],
         ["The bond length increases from C–H to F–H.", "The longer the bond, the more energy is needed to break it.",
          "The atomic size increases from C to F.", "Bond energy depends only on the mass of the atoms."],
         ["How does the size of the atom change from C to F?", "How does bond length affect bond strength?"], 1)]

# ---- QUESTION 3, the question paper page 9 and the memo pages 4-5 ----
q3 = [
    stmt("3.1", "Define boiling point.", 2, ["The temperature at which the vapour pressure of a substance equals atmospheric pressure."],
         ["The temperature at which a solid changes into a liquid.", "The temperature at which a substance's vapour pressure is zero.",
          "The temperature at which water boils at sea level.", "The temperature at which all intermolecular forces disappear."],
         ["Boiling starts when the liquid's vapour pressure reaches what?", "Is it about melting or boiling?"], 2),
    stmt("3.2", "Is this a fair investigation? Write only YES or NO.\nGive a reason for the answer.", 2,
         ["YES", "Only one independent variable: all variables are controlled except the molecular mass."],
         ["NO", "The compounds have different boiling points, so it is not fair.", "Two variables are changed at the same time.",
          "The compounds are in different phases."],
         ["What changes from A to D?", "Do the compounds have the same type of intermolecular force?"], 1),
    answer("3.3", "Write down the phase of the above compounds at room temperature.", 1, ["Gas", "Liquid", "Solid", "Liquid and gas"],
           ["Room temperature is about 25 °C.", "Are all the boiling points below or above that?"]),
    stmt("3.4", "Explain the trend observed in boiling points of the compounds in the table above by referring to the molecular mass, "
         "intermolecular forces, and energy involved.", 3,
         ["The molecular mass increases from A to D.", "The strength of the London forces increases with an increase in the molecular size/mass.",
          "More energy is required to overcome the intermolecular forces from A to D."],
         ["The molecular mass decreases from A to D.", "Hydrogen bonds get stronger from A to D.",
          "Less energy is needed to overcome the intermolecular forces from A to D.", "The London forces get weaker as the molecular mass "
                                                                                       "increases."],
         ["How does the molecular mass change from CH₄ to SnH₄?", "How does that affect the London forces and the energy to boil?"], 1),
    stmt("3.5", "Which compound in the table above has the highest vapour pressure at a given temperature? Explain the answer by referring to "
         "the data in the table above.", 2, ["Compound A (CH₄)", "It has the lowest boiling point."],
         ["Compound D (SnH₄)", "It has the highest boiling point.", "Compound B (SiH₄)", "It has the strongest intermolecular forces."],
         ["Which compound evaporates most easily?", "How is that linked to the boiling point?"], 1),
    mcq("3.6.1", "The boiling point of HF (19,5 °C) and HCℓ (X) is compared.\nWill the value of X be HIGHER THAN, LOWER THAN or EQUAL TO 19,5 °C?",
        ["HIGHER THAN", "LOWER THAN", "EQUAL TO"], 1, ["Which intermolecular force does HF have that HCℓ does not?", "Stronger forces mean a "
                                                                                                                   "higher boiling point."],
        marks=1),
    stmt("3.6.2", "Fully explain the answer to QUESTION 3.6.1.", 4,
         ["HF has hydrogen bonds.", "HCℓ has dipole-dipole forces.", "Hydrogen bonds are stronger than dipole-dipole forces.",
          "More energy is needed to overcome the intermolecular forces in HF."],
         ["HCℓ has hydrogen bonds.", "HF has only London forces.", "Dipole-dipole forces are stronger than hydrogen bonds.",
          "Less energy is needed to overcome the intermolecular forces in HF."],
         ["Is H bonded to N, O or F in each compound?", "Which force is stronger?"], 1, after=["3.6.1"])]

# ---- QUESTION 4, the question paper page 10 and the memo pages 5-6 ----
q4 = [
    answer("4.1", "Name and state the law the experiment is based on.", 3, [
        "Boyle's law: the pressure of an enclosed gas is inversely proportional to the volume it occupies at constant temperature.",
        "Charles's law: the volume of an enclosed gas is directly proportional to its Kelvin temperature at constant pressure.",
        "Boyle's law: the pressure of an enclosed gas is directly proportional to the volume it occupies at constant temperature.",
        "Gay-Lussac's law: the pressure of an enclosed gas is directly proportional to its Kelvin temperature at constant volume."],
        ["Which two quantities does the experiment change?", "As the pressure goes up, what does the volume do?"]),
    stmt("4.2", "Write down a hypothesis for this investigation.", 2,
         ["The higher the pressure of a gas, the lower its volume.", "As the pressure on an enclosed gas increases, its volume decreases."],
         ["The higher the pressure of a gas, the higher its volume.", "The temperature of a gas depends on its volume.",
          "The pressure and the volume of a gas are not related.", "The volume of a gas increases as its temperature increases."],
         ["A hypothesis links the independent and the dependent variable.", "How does the volume change as the pressure rises?"], 2),
    num("4.3", "Read and write down the pressure from the graph when the volume is 12 cm³.", 40, 2, "kPa",
        ["Go across from 12 cm³ to the curve.", "Then down to the pressure axis (× 10³ Pa)."]),
    work("4.4", "Calculate the volume at 200 kPa.", 4, [
        "p₁V₁ = p₂V₂\n(40 × 10³)(12) = (200 × 10³)V₂\nV₂ = 2,4 cm³",          # the memo
        "p₁p₂ = V₁V₂\n(40 × 10³)(200 × 10³) = 12V₂\nV₂ = 6,67 × 10⁸ cm³",    # the quantities paired wrongly
        "{p₁}/{V₁} = {p₂}/{V₂}\n{40 × 10³}/{12} = {200 × 10³}/{V₂}\nV₂ = 60 cm³",  # p/V taken as constant
        "p₁V₁ = p₂V₂\n(40)(12) = (200 × 10³)V₂\nV₂ = 2,4 × 10⁻³ cm³"],        # kPa on one side, Pa on the other
        ["Boyle's law: which product stays the same?", "Use a point from the graph and the same pressure unit on both sides."],
        after=["4.3"]),
    draw("4.5", "Redraw the above graph and label it A. On the same set of axes draw the graph to show how a real gas will deviate at a high "
         "pressure. Label this graph as B.", 2, [["Curve B is higher than curve A at high pressure", 2]],
         ["At high pressure, do the real gas molecules' own volume and forces matter?", "Is the real gas volume bigger or smaller than the "
                                                                                       "ideal there?"],
         memo="The memo's graph: A the curve through the data; B dashed, leaving A near 100 kPa and staying above it at high pressure.")]

# ---- QUESTION 5, the question paper page 11 and the memo pages 6-7 ----
q5 = [
    stmt("5.1", "Define the term activation energy.", 2, ["The minimum energy needed for a reaction to take place."],
         ["The energy released when a reaction takes place.", "The energy of the products minus the energy of the reactants.",
          "The maximum energy the reactants can have.", "The energy needed to break all the bonds in the products."],
         ["Is it the least or the most energy?", "What is it needed for?"], 2),
    stmt("5.2", "Is the above reaction ENDOTHERMIC or EXOTHERMIC?\nGive a reason for the answer.", 2, ["EXOTHERMIC", "ΔH < 0 (ΔH is negative)."],
         ["ENDOTHERMIC", "ΔH > 0", "Energy is absorbed from the surroundings.", "The products have more potential energy than the reactants."],
         ["What is the sign of ΔH?", "Is energy released or absorbed?"], 1),
    work("5.3", "Calculate the heat of the products.", 2, [
        "ΔH = H(p) − H(r)\n−7,28 = H(p) − 26,6\nH(p) = 19,32 kJ·mol⁻¹",       # the memo
        "H(p) = H(r) + E(a)\nH(p) = 26,6 + 6,73\nH(p) = 33,33 kJ·mol⁻¹",       # the activated complex
        "ΔH = H(p) + H(r)\n−7,28 = H(p) + 26,6\nH(p) = −33,88 kJ·mol⁻¹",       # the energies added
        "ΔH = H(r) − H(p)\n−7,28 = 26,6 − H(p)\nH(p) = 33,88 kJ·mol⁻¹"],       # subtracted the wrong way
        ["Which formula links ΔH, H(products) and H(reactants)?", "ΔH is negative: are the products lower or higher?"]),
    draw("5.4", "Draw the potential energy versus course of reaction graph for the above reaction. On the graph indicate values for: Heat of "
         "reactants (H reactants) ; Heat of products (H products) ; Energy at the activated complex ; Heat of the reaction (ΔH)", 5,
         [["H reactants correct", 1], ["H products correct", 1], ["ΔH correct", 1], ["Energy at the activated complex", 1], ["Correct shape", 1]],
         ["The reactants are at 26,6 kJ·mol⁻¹: how high is the activated complex?", "Exothermic: are the products above or below?"],
         memo="The memo's graph: reactants at 26,6, the peak at 33,33 and products at 19,32 kJ·mol⁻¹, ΔH marked between the reactants and "
              "products.", after=["5.2", "5.3"]),
    draw("5.5", "On the same graph drawn in QUESTION 5.4, use a dotted line and draw the shape of the graph when a catalyst is added to the "
         "original reaction.", 2, [["The curve starts at the reactants' energy and ends at the products'", 1], ["The curve's peak is lower", 1]],
         ["Does a catalyst change the energies of the reactants or the products?", "What does a catalyst do to the activation energy?"],
         memo="The memo's dotted curve: the same start and end, with a lower peak.", after=["5.4"])]

# ---- QUESTION 6, the question paper page 12 and the memo pages 7-9 ----
CH = "C : H = {82,76}/{12} : {17,24}/{1}\n= 6,90 : 17,24\n"
q61 = [
    stmt("6.1.1", "Define empirical formula.", 2, ["The simplest whole number ratio of atoms in a compound."],
         ["The actual number of atoms of each element in a molecule.", "The mass of one mole of a compound.",
          "The ratio of the masses of the elements in a compound.", "The arrangement of the atoms in a molecule."],
         ["Is it the actual number or the simplest ratio?", "A ratio of what?"], 2),
    work("6.1.2", "Use the principle of conservation of mass and determine the value P.", 3, [
        "P(58) + 13(32) = 8(44) + 10(18)\n58P + 416 = 532\nP = 2",            # the memo
        "P(58) + 13(16) = 8(44) + 10(18)\n58P + 208 = 532\nP = 5,59",         # O₂ taken as 16 g·mol⁻¹
        "P(58) + 13(32) = 8(44) + 10(16)\n58P + 416 = 512\nP = 1,66",         # H₂O taken as 16 g·mol⁻¹
        "P + 13 = 8 + 10\nP = 18 − 13\nP = 5"],                               # molecules counted, not masses
        ["The mass of the reactants equals the mass of the products.", "What are the molar masses of O₂, CO₂ and H₂O?"]),
    work("6.1.3", "Determine the molecular formula of compound Q.", 5, [
        CH + "= 1 : 2,5 = 2 : 5\nEmpirical formula C₂H₅, formula mass 2(12) + 5 = 29\nRatio {58}/{29} = 2: molecular formula C₄H₁₀",   # the memo
        CH + "= 1 : 2,5 = 2 : 5\nEmpirical formula C₂H₅, formula mass 2(12) + 5 = 29\nRatio taken as 1: molecular formula C₂H₅",       # empirical as molecular
        "C : H = 82,76 : 17,24\n= 4,8 : 1\n= 5 : 1\nEmpirical formula C₅H, formula mass 5(12) + 1 = 61\nRatio {58}/{61} ≈ 1: molecular formula C₅H",  # % not ÷ M
        CH + "= 1 : 2,5 ≈ 1 : 3\nEmpirical formula CH₃, formula mass 12 + 3 = 15\nRatio {58}/{15} ≈ 4: molecular formula C₄H₁₂"],      # 2,5 rounded to 3
        ["Divide each percentage by its molar mass.", "How many empirical units fit into 58 g·mol⁻¹?"])]
NA = "n(Na₂CO₃) = {m}/{M} = {5}/{106} = 0,047 mol\n"
q62 = [
    stmt("6.2.1", "Define the term limiting reagent.", 2, ["A reactant that is completely used up in a chemical reaction."],
         ["A reactant that is left over after the reaction.", "A substance that speeds up a reaction without being used up.",
          "The product formed in the smallest amount.", "The reactant with the largest mass."],
         ["Which reactant stops the reaction?", "Is it used up or left over?"], 2),
    work("6.2.2", "Calculate the amount of hydrochloric acid that reacted with sodium carbonate.", 4, [
        NA + "n(HCℓ) = 2(0,047)\nn(HCℓ) = 0,094 mol",                                          # the memo
        NA + "n(HCℓ) = 1(0,047)\nn(HCℓ) = 0,047 mol",                                          # the 1 : 2 ratio ignored
        NA + "n(HCℓ) = 2(0,047) × 0,76\nn(HCℓ) = 0,071 mol",                                    # the 76% applied here
        "n(Na₂CO₃) = {m}/{M} = {5}/{83} = 0,060 mol\nn(HCℓ) = 2(0,060)\nn(HCℓ) = 0,120 mol"],    # M(Na₂CO₃) with one Na
        ["How many moles of Na₂CO₃ are in 5 g?", "What is the mole ratio of HCℓ to Na₂CO₃?"]),
    work("6.2.3", "Calculate the volume of carbon dioxide that was produced.\nTake the molar volume at room temperature as 24,45 dm³.", 4, [
        "n(CO₂) = n(Na₂CO₃) = 0,047 mol\nV = nV(m) = (0,047)(24,45)\nV = 1,149 dm³",      # the memo
        "n(CO₂) = n(HCℓ) = 0,094 mol\nV = nV(m) = (0,094)(24,45)\nV = 2,298 dm³",         # the HCℓ ratio
        "n(CO₂) = n(Na₂CO₃) = 0,047 mol\nV = nV(m) = (0,047)(22,4)\nV = 1,053 dm³",       # the STP molar volume
        "n(CO₂) = n(Na₂CO₃) = 0,047 mol\nV = {n}/{V(m)} = {0,047}/{24,45}\nV = 0,0019 dm³"],  # divided by V(m)
        ["What is the mole ratio of CO₂ to Na₂CO₃?", "V = n × V(m) at room temperature."], after=["6.2.2"]),
    work("6.2.4", "The hydrochloric acid that was used in the reaction was obtained by diluting 100 cm³ HCℓ to 250 cm³ hydrochloric acid (HCℓ) "
         "solution.\nCalculate the concentration of the concentrated hydrochloric acid (HCℓ).", 4, [
        "n(HCℓ) initial = 0,094 × {100}/{76} = 0,124 mol\nc(dilute) = {0,124}/{0,25} = 0,496 mol·dm⁻³\n(0,496)(250) = c(100)\nc = 1,24 mol·dm⁻³",  # the memo
        "n(HCℓ) = 0,094 mol\nc(dilute) = {0,094}/{0,25} = 0,376 mol·dm⁻³\n(0,376)(250) = c(100)\nc = 0,94 mol·dm⁻³",                            # the 76% ignored
        "n(HCℓ) initial = 0,094 × {100}/{76} = 0,124 mol\nc(dilute) = {0,124}/{0,25} = 0,496 mol·dm⁻³\n(0,496)(100) = c(250)\nc = 0,198 mol·dm⁻³",  # dilution inverted
        "n(HCℓ) initial = 0,094 × {76}/{100} = 0,071 mol\nc(dilute) = {0,071}/{0,25} = 0,286 mol·dm⁻³\n(0,286)(250) = c(100)\nc = 0,71 mol·dm⁻³"],  # 76% the wrong way
        ["Only 76% of the HCℓ reacted: how much was there at the start?", "The concentrated acid was diluted from 100 cm³ to 250 cm³."],
        after=["6.2.2"])]

# ---- QUESTION 7, the question paper page 13 and the memo pages 9-11 ----
OH = "[OH⁻] = 0,5 mol·dm⁻³\n"
q71 = [
    stmt("7.1.1", "Define an acid according to the Arrhenius theory.", 2,
         ["An acid is a substance that produces hydrogen ions (H⁺) / hydronium ions (H₃O⁺) when it dissolves in water."],
         ["An acid is a substance that produces hydroxide ions (OH⁻) when it dissolves in water.", "An acid is a substance that accepts "
                                                                                                   "electrons.",
          "An acid is a substance that turns phenolphthalein pink.", "An acid is a substance that accepts protons."],
         ["Arrhenius defines acids by the ions they make in water.", "Which ion?"], 2),
    answer("7.1.2", "Write down the FORMULAE of the TWO substances that can act as an ampholyte.", 2,
           ["H₂O and HCO₃⁻", "H₂CO₃ and H₃O⁺", "H₂O and H₃O⁺", "HCO₃⁻ and H₂CO₃"],
           ["An ampholyte can both give and take a proton.", "Which substances can still lose an H⁺ and also gain one?"]),
    answer("7.1.3", "Write down the FORMULAE of TWO acids from the reaction.", 2, ["H₂CO₃ and H₃O⁺", "H₂O and HCO₃⁻", "H₂CO₃ and HCO₃⁻",
                                                                                  "H₃O⁺ and H₂O"],
           ["An acid donates a proton.", "One acid is on each side of the equation."]),
    answer("7.1.4", "Write down the balanced equation between carbonic acid and sodium hydroxide (NaOH).", 3,
           ["H₂CO₃ + 2 NaOH → Na₂CO₃ + 2 H₂O", "H₂CO₃ + NaOH → Na₂CO₃ + H₂O", "H₂CO₃ + 2 NaOH → 2 NaCO₃ + 2 H₂O",
            "H₂CO₃ + 2 NaOH → Na₂CO₃ + 2 H₂O + CO₂"],
           ["An acid and a base give a salt and water.", "Count the Na, H and O atoms on each side."])]
q72 = [
    work("7.2.1", "Calculate the concentration of NaOH.", 3, [
        "c = {m}/{MV}\nc = {2}/{(40)(0,1)}\nc = 0,5 mol·dm⁻³",          # the memo
        "c = {m}/{MV}\nc = {2}/{(40)(100)}\nc = 5 × 10⁻⁴ mol·dm⁻³",     # cm³ not changed to dm³
        "c = {m}/{MV}\nc = {2}/{(23)(0,1)}\nc = 0,87 mol·dm⁻³",         # M of Na only
        "c = {mM}/{V}\nc = {(2)(40)}/{0,1}\nc = 800 mol·dm⁻³"],         # the formula upside down
        ["What is the molar mass of NaOH?", "100 cm³ is how many dm³?"]),
    work("7.2.2", "Calculate the pH of NaOH.", 4, [
        OH + "[H₃O⁺](0,5) = 1 × 10⁻¹⁴\n[H₃O⁺] = 2 × 10⁻¹⁴ mol·dm⁻³\npH = −log(2 × 10⁻¹⁴) = 13,70",       # the memo
        OH + "[H₃O⁺] taken as [OH⁻] = 0,5\npH = −log(0,5)\npH = 0,30",                                     # pH from [OH⁻]
        OH + "[H₃O⁺](0,5) = 1 × 10⁻¹⁴\n[H₃O⁺] = 5 × 10⁻¹⁵ mol·dm⁻³\npH = −log(5 × 10⁻¹⁵) = 14,30",        # multiplied, not divided
        "[OH⁻] = 2(0,5) = 1 mol·dm⁻³\n[H₃O⁺](1) = 1 × 10⁻¹⁴\n[H₃O⁺] = 1 × 10⁻¹⁴ mol·dm⁻³\npH = −log(1 × 10⁻¹⁴) = 14"],  # two OH⁻ per NaOH
        ["NaOH gives one OH⁻ per formula unit.", "K(w) = [H₃O⁺][OH⁻] = 1 × 10⁻¹⁴."], after=["7.2.1"])]
NOH = "n(NaOH) = cV = 0,8 × {55}/{1 000} = 0,044 mol\nn(HCℓ) excess = 0,044 mol (1 : 1)\n"
q73 = [
    work("7.3.1", "Calculate the initial number of moles of hydrochloric acid.", 3, [
        "n = {N}/{N(A)}\nn = {9,033 × 10²²}/{6,02 × 10²³}\nn = 0,15 mol",      # the memo
        "n = N × N(A)\nn = (9,033 × 10²²)(6,02 × 10²³)\nn = 5,44 × 10⁴⁶ mol",   # multiplied
        "n = {N(A)}/{N}\nn = {6,02 × 10²³}/{9,033 × 10²²}\nn = 6,66 mol",       # upside down
        "n = {N}/{N(A)}\nn = {9,033 × 10²²}/{6,02 × 10²²}\nn = 1,50 mol"],      # the power of N(A) slipped
        ["Which formula links a number of molecules to moles?", "N(A) = 6,02 × 10²³."]),
    work("7.3.2", "Calculate the percentage purity of magnesium carbonate.", 8, [
        NOH + "n(HCℓ) reacted = 0,15 − 0,044 = 0,106 mol\nn(MgCO₃) = {0,106}/{2} = 0,053 mol\nm = nM = 0,053 × 84 = 4,452 g\n"
              "% purity = {4,452}/{5} × 100 = 89,04%",                                                                 # the memo
        NOH + "n(HCℓ) reacted = 0,044 mol\nn(MgCO₃) = {0,044}/{2} = 0,022 mol\nm = nM = 0,022 × 84 = 1,848 g\n"
              "% purity = {1,848}/{5} × 100 = 36,96%",                                                                 # the excess taken as reacted
        NOH + "n(HCℓ) reacted = 0,15 − 0,044 = 0,106 mol\nn(MgCO₃) = 0,106 mol\nm = nM = 0,106 × 84 = 8,904 g\n"
              "% purity = {8,904}/{5} × 100 = 178,08%",                                                                # the 2 : 1 ratio ignored
        NOH + "n(HCℓ) reacted = 0,15 − 0,044 = 0,106 mol\nn(MgCO₃) = {0,106}/{2} = 0,053 mol\nm = nM = 0,053 × 52 = 2,756 g\n"
              "% purity = {2,756}/{5} × 100 = 55,12%"],                                                                # M(MgCO₃) with one O
        ["How much HCℓ was left over, from the NaOH that neutralised it?", "The rest reacted with MgCO₃ in a 2 : 1 ratio."],
        after=["7.3.1"])]

# ---- QUESTION 8, the question paper page 14 and the memo page 11 ----
HALF = "Sn²⁺ → Sn⁴⁺ + 2e⁻ (× 3)\nCr₂O₇²⁻ + 14 H⁺ + 6e⁻ → 2 Cr³⁺ + 7 H₂O\n"
q81 = [
    stmt("8.1.1", "Explain the term redox reaction.", 2,
         ["A redox reaction is a reaction that involves an electron transfer.", "It is a reaction that always involves changes in oxidation "
                                                                               "numbers."],
         ["A reaction in which a proton is transferred.", "A reaction between an acid and a base.", "A reaction in which no electrons move.",
          "A reaction in which only oxygen is gained."], ["What moves from one substance to another in a redox reaction?",
                                                          "What happens to the oxidation numbers?"], 2),
    answer("8.1.2", "Which ONE of Zn or Ni²⁺ is the oxidising agent?\nExplain the answer by referring to the oxidation numbers.", 3, [
        "Ni²⁺: its oxidation number decreases from +2 to 0 (it is reduced).", "Zn: its oxidation number increases from 0 to +2.",
        "Zn: its oxidation number decreases from +2 to 0.", "Ni²⁺: its oxidation number increases from 0 to +2."],
        ["An oxidising agent is itself reduced.", "Which species' oxidation number goes down?"]),
    answer("8.1.3", "Give a reason why the nitrate ion (NO₃⁻) is not written in the net ionic equation above.", 1, [
        "It is a spectator ion: its oxidation state does not change.", "It is reduced to nitrogen gas.", "It is the oxidising agent.",
        "It is insoluble in water."], ["Does the nitrate ion take part in the electron transfer?", "What do we call an ion that does not "
                                                                                                  "change?"])]
q82 = [
    work("8.2.1", "Determine the oxidation number of Cr in Cr₂O₇²⁻.", 2, [
        "2x + 7(−2) = −2\nx = +6",       # the memo
        "x + 7(−2) = −2\nx = +12",       # one Cr counted
        "2x + 7(−2) = 0\nx = +7",        # the ion's charge ignored
        "2x + 7(−2) = −2\nx = −6"],      # the sign lost
        ["The oxidation numbers add up to the ion's charge.", "Each O is −2: how many O atoms and Cr atoms are there?"]),
    answer("8.2.2", "Write down the reduction half-reaction.", 2, [
        "Cr₂O₇²⁻ + 14 H⁺ + 6e⁻ → 2 Cr³⁺ + 7 H₂O", "Sn²⁺ → Sn⁴⁺ + 2e⁻", "Cr₂O₇²⁻ + 14 H⁺ → 2 Cr³⁺ + 7 H₂O + 6e⁻",
        "Cr₂O₇²⁻ + 7 H⁺ + 3e⁻ → Cr³⁺ + 7 H₂O"],
        ["Reduction is a gain of electrons: on which side are they?", "Which species is reduced?"], after=["8.2.1"]),
    work("8.2.3", "Use the Table of Standard Reduction Potentials and write down the balanced net ionic equation.", 4, [
        HALF + "3 Sn²⁺ + Cr₂O₇²⁻ + 14 H⁺ → 3 Sn⁴⁺ + 2 Cr³⁺ + 7 H₂O",                                                # the memo
        "Sn²⁺ → Sn⁴⁺ + 2e⁻\nCr₂O₇²⁻ + 14 H⁺ + 6e⁻ → 2 Cr³⁺ + 7 H₂O\nSn²⁺ + Cr₂O₇²⁻ + 14 H⁺ → Sn⁴⁺ + 2 Cr³⁺ + 7 H₂O",   # electrons not balanced
        HALF + "3 Sn²⁺ + Cr₂O₇²⁻ + 14 H⁺ + 6e⁻ → 3 Sn⁴⁺ + 2 Cr³⁺ + 7 H₂O + 6e⁻",                                    # electrons left in
        "Sn⁴⁺ + 2e⁻ → Sn²⁺ (× 3)\nCr₂O₇²⁻ + 14 H⁺ + 6e⁻ → 2 Cr³⁺ + 7 H₂O\n3 Sn⁴⁺ + 2 Cr³⁺ + 7 H₂O → 3 Sn²⁺ + Cr₂O₇²⁻ + 14 H⁺"],  # reversed
        ["How many electrons does each half-reaction move?", "Multiply so they cancel, then add."], after=["8.2.2"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Chemical bonding", "marks": 21, "lead": COMP.strip(), "items": q2},
    {"id": "2.8", "title": "Question 2.8", "kind": "Bond energy", "marks": 4,
     "lead": "The following table shows the average bond energies of atoms that are bonded to the hydrogen atom.\nC – H: 413 kJ·mol⁻¹\n"
             "O – H: 463 kJ·mol⁻¹\nF – H: 565 kJ·mol⁻¹", "items": q28},
    {"id": "3", "title": "Question 3", "kind": "Intermolecular forces", "marks": 15,
     "lead": "Learners investigated the boiling points of the compounds listed in the table below.\nA: CH₄, −161,5 °C\nB: SiH₄, −111,8 °C\n"
             "C: GeH₄, −88,6 °C\nD: SnH₄, −52 °C", "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Ideal gases", "marks": 12,
     "lead": "Learners investigated the relationship between pressure and volume of a gas. The graph below shows the results obtained during "
             "the investigation.",
     "figure": P.fig("Q4", "A graph of volume (cm³, 0 to 20) against pressure (× 10³ Pa, 0 to 180): data points at about (30 ; 18), "
                           "(35 ; 15), (45 ; 10), (82 ; 6) and (165 ; 3) and a smooth curve falling through them."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Energy and change", "marks": 13,
     "lead": "Consider the decomposition reaction of dinitrogen pentoxide:\n2 N₂O₅(g) → 2 N₂O₄(g) + O₂(g)\nThe table below shows the "
             "different energies for the above reaction.\nHeat of the reactants (Hr): 26,6 kJ·mol⁻¹\nActivation energy (Ea): 6,73 kJ·mol⁻¹\n"
             "Heat of the reaction (ΔH): −7,28 kJ·mol⁻¹", "items": q5},
    {"id": "6.1", "title": "Question 6.1", "kind": "Quantitative aspects", "marks": 10,
     "lead": "Compound Q (CxHy) reacts with oxygen according to the balanced equation:\nP CxHy + 13 O₂ → 8 CO₂ + 10 H₂O\nThe molar mass of "
             "compound Q is 58 g·mol⁻¹.\nThe percentage composition of compound Q is: carbon 82,76% ; hydrogen 17,24%", "items": q61},
    {"id": "6.2", "title": "Question 6.2", "kind": "Quantitative aspects", "marks": 14,
     "lead": "5 g of sodium carbonate (Na₂CO₃) reacts with 250 cm³ of hydrochloric acid (HCℓ).\nNa₂CO₃(s) + 2 HCℓ(aq) → 2 NaCℓ(aq) + H₂O(ℓ) "
             "+ CO₂(g)\nThe percentage of hydrochloric acid (HCℓ) that reacted with sodium carbonate (Na₂CO₃) is 76%.", "items": q62},
    {"id": "7.1", "title": "Question 7.1", "kind": "Acids and bases", "marks": 9,
     "lead": "Carbonic acid ionises in water according to the following balanced equation:\nH₂CO₃(aq) + H₂O(ℓ) ⇌ HCO₃⁻(aq) + H₃O⁺(aq)",
     "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Acids and bases", "marks": 7,
     "lead": "2 g of NaOH is dissolved in water to make a 100 cm³ solution.", "items": q72},
    {"id": "7.3", "title": "Question 7.3", "kind": "Acids and bases", "marks": 11,
     "lead": "5 g of impure magnesium carbonate (MgCO₃), is added to 9,033 × 10²² molecules of hydrochloric acid (HCℓ).\nMgCO₃(s) + 2 HCℓ(aq) "
             "→ MgCℓ₂(aq) + CO₂(g) + H₂O(ℓ)\nThe reaction is allowed to proceed until all the pure magnesium carbonate completely reacts. The "
             "excess hydrochloric acid is neutralised by adding 55 cm³ of sodium hydroxide solution of concentration 0,8 mol·dm⁻³.\n"
             "HCℓ(aq) + NaOH(aq) → NaCℓ(aq) + H₂O(ℓ)", "items": q73},
    {"id": "8.1", "title": "Question 8.1", "kind": "Redox reactions", "marks": 6,
     "lead": "A solution of nickel (II) nitrate is placed in a zinc container. It was observed, after some time, that a chemical reaction has "
             "taken place. The net ionic equation is:\nZn(s) + Ni²⁺(aq) ⇌ Zn²⁺(aq) + Ni(s)", "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Redox reactions", "marks": 8,
     "lead": "The reaction between dichromate ions (Cr₂O₇²⁻) and tin (II) ions (Sn²⁺) in an acid medium is given below.\n"
             "Cr₂O₇²⁻ + Sn²⁺ + H⁺ → Cr³⁺ + Sn⁴⁺ + H₂O(ℓ)", "items": q82},
]
P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
         [P.flag_workings(),
          P.flag_answers("'Name and state' (4.1) and 'explain by the oxidation numbers' (8.1.2) play as named statements."),
          {"n": "4.3", "kind": "no_fit", "detail": "One read-off number stays typed: 4.3 (40 kPa read off the graph, within 2 kPa; the memo "
                                                   "also writes 40 × 10³ Pa)."},
          {"n": "2.3.1", "kind": "no_fit", "detail": "Every drawing plays as pick the drawing: the Lewis structures (2.3.1, 2.3.2, 2.4.2), the "
                                                     "real-gas graph (4.5) and the energy profile with and without a catalyst (5.4, 5.5): the "
                                                     "memo's and three mistakes it marks down."},
          {"n": "5.4", "kind": "memo_issue", "detail": "The memo's graph (page 7) labels ΔH = −25 kJ·mol⁻¹; the stem's ΔH is −7,28 kJ·mol⁻¹, "
                                                       "which its 26,6 and 19,32 give. The right drawing marks −7,28."}],
         {"1": 20, "2": 25, "3": 15, "4": 12, "5": 13, "6": 24, "7": 27, "8": 14}, 150,
         {"2.7": ["2.6"], "3.6.2": ["3.6.1"], "4.4": ["4.3"], "5.4": ["5.2", "5.3"], "5.5": ["5.4"], "6.2.3": ["6.2.2"], "6.2.4": ["6.2.2"],
          "7.2.2": ["7.2.1"], "7.3.2": ["7.3.1"], "8.2.2": ["8.2.1"], "8.2.3": ["8.2.2"]},
         "Questions 1 to 8 (the whole paper)")
