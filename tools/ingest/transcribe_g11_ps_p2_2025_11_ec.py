"""Grade 11 Physical Sciences P2 (Chemistry) November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 9,
150 marks, 3 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): ecexams.co.za, 2025_November_Gr_11_Exams, the question paper zip (English PDF, 22 pages, text layer) and the
memo PDF (English and Afrikaans, 16 pages), read from their text and page images.

  python tools/ingest/transcribe_g11_ps_p2_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ps-p2-2025-11-ec/PHYSICAL SC P2 QP GR11 NOVEMBER 2025 (2)_watermark.pdf" "uploads/provincial/g11-ps-p2-2025-11-ec/PHYSICAL SCIENCES P2 GRADE 11 MEMO NOVEMBER 2025 ENG & AFR_watermark.pdf" --id g11-ps-p2-2025-11-ec --from-json

The rulings as in transcribe_g11_ps_p2_2024_11_ec.py.
Figure boxes in PDF points (page 595 x 842): the union of each diagram's drawings and labels (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-ps-p2-2025-11-ec", 595.3, 841.9, {
    "1.4": [4, 144.5, 148.6, 448.0, 234.5], "2.5": [8, 98.5, 106.0, 518.1, 371.2], "3.1": [9, 161.9, 156.5, 283.0, 272.9],
    "Q4": [11, 84.3, 151.8, 511.1, 401.9], "Q5": [12, 84.3, 201.7, 511.1, 453.2], "Q7": [14, 98.5, 229.0, 518.1, 439.0],
    "Q9": [16, 133.0, 140.0, 433.1, 312.9]}, start=5)
work, answer, num, draw, stmt, mcq = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq
CHANGE = ["INCREASE", "DECREASE", "REMAIN THE SAME"]
CMP = ["HIGHER THAN", "LOWER THAN", "EQUAL TO"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which ONE of the following molecules contains a dative covalent bond?", ["H₂O", "NH₃", "BF₃", "NH₄⁺"], 3,
        ["A dative bond forms when one atom gives both electrons of the pair.", "Which ion forms from a molecule's lone pair and an H⁺?"]),
    mcq("1.2", "Consider the chemical bonds C – C ; C = C ; C ≡ C.\nWhich ONE of the following combinations regarding the bond length and bond "
        "energy is CORRECT?", ["Shortest bond length C – C; highest bond energy C – C", "Shortest bond length C = C; highest bond energy C = C",
                               "Shortest bond length C ≡ C; highest bond energy C ≡ C", "Shortest bond length C – C; highest bond energy C ≡ C"], 2,
        ["More shared pairs pull the atoms closer.", "A shorter bond is a stronger bond."]),
    mcq("1.3", "Which ONE of the following substances have ION DIPOLE FORCES between its molecules?", ["H₂O (ℓ)", "CO₂ (g)", "NaCℓ (aq)", "NaCℓ (s)"],
        2, ["Ion-dipole forces need ions and polar molecules together.", "Where are Na⁺ and Cℓ⁻ surrounded by water molecules?"]),
    mcq("1.4", "The diagram below shows a gas syringe containing a certain gas. When the plunger is at position A the volume occupied by the gas "
        "is X and exerts a pressure P. When the plunger moves to position B the volume occupied by the gas is ⅓X.\nWhat is the DIFFERENCE in "
        "pressure exerted by the gas between points A and B?", ["3P", "⅔P", "⅓P", "2P"], 3,
        ["Boyle's law: the volume falls to ⅓, so the pressure becomes what?", "The difference is the new pressure minus P."],
        figure=P.fig("1.4", "A gas syringe: the plunger at A gives a volume X; at B, further in, a volume ⅓X.")),
    mcq("1.5", "Consider the following statement regarding the activated complex during a chemical reaction:\n(I) The activation energy must be "
        "overcome to reach the activated complex.\n(II) It is the unstable transition state from reactants to products.\n(III) It is the energy "
        "released or absorbed during a chemical reaction.\nWhich of the above statement(s) is/are CORRECT about the activated complex?",
        ["II and III only", "II only", "I and II only", "I only"], 2,
        ["Which statement describes the heat of reaction instead?", "What is at the top of the energy profile?"]),
    mcq("1.6", "Consider the balanced equation:\nNa₂CO₃(aq) + 2 HCℓ(aq) → 2 NaCℓ(aq) + H₂O(ℓ) + CO₂(g)\n1 mol of Na₂CO₃ reacts with 1 mol of HCℓ to "
        "yield 0,2 mol of CO₂.\nWhich ONE of the following combinations is CORRECT regarding the reaction?",
        ["Limiting reagent Na₂CO₃; yield of CO₂ 40%", "Limiting reagent Na₂CO₃; yield of CO₂ 20%", "Limiting reagent HCℓ; yield of CO₂ 40%",
         "Limiting reagent HCℓ; yield of CO₂ 20%"], 2,
        ["1 mol of Na₂CO₃ needs 2 mol of HCℓ: which runs out?", "How much CO₂ can 1 mol of HCℓ make, and what is 0,2 of that?"]),
    mcq("1.7", "Consider the incomplete equation below:\nH₂Y + 2 NaOH → Na₂Y + 2 H₂O\nThe formula of Y is …", ["Cℓ⁻", "SO₄²⁻", "NO₃⁻", "PO₄³⁻"], 1,
        ["H₂Y gives two H⁺: what is Y's charge?", "Which ion has a 2− charge?"]),
    mcq("1.8", "Consider the following equation:\n(COOH)₂(aq) + H₂O(ℓ) ⇌ (COO)₂²⁻(aq) + H₃O⁺(aq)\nThe bases in the above reaction are …",
        ["(COOH)₂ and H₂O", "(COO)₂²⁻ and H₃O⁺", "H₂O and (COO)₂²⁻", "(COOH)₂ and (COO)₂²⁻"], 2,
        ["A base accepts a proton.", "One base is on each side of the equation."]),
    mcq("1.9", "Consider the reaction below:\n5 Zn + 2 MnO₄⁻ + 16 H⁺ → 5 Zn²⁺ + 2 Mn²⁺ + 8 H₂O\nThe reducing agent in the above reaction is …",
        ["Zn", "MnO₄⁻", "H⁺", "Mn²⁺"], 0, ["A reducing agent is oxidised.", "Whose oxidation number goes up?"]),
    mcq("1.10", "How many electrons are needed to reduce 2 mol of H₂O to 2 mol of OH⁻ and 1 mol of H₂?", ["2", "3", "4", "5"], 0,
        ["Write the half-reaction: 2 H₂O + ?e⁻ → H₂ + 2 OH⁻.", "Balance the charge on each side."])]

# ---- QUESTION 2, the question paper pages 7-8 and the memo pages 3-4 ----
q2 = [
    stmt("2.1", "Define the term chemical bond.", 2,
         ["A mutual attraction between two atoms resulting from the simultaneous attraction between their nuclei and the outer electrons."],
         ["The repulsion between the nuclei of two atoms.", "The force between two separate molecules.", "The transfer of protons between two "
                                                                                                         "atoms.",
          "The attraction between an atom's nucleus and its own inner electrons."], ["Is a bond an attraction or a repulsion?",
                                                                                       "What attracts what?"], 2),
    draw("2.2.1", "Draw the Lewis structure for: HOCℓ", 2, [["H : O : Cℓ with the bonding pairs", 1], ["The lone pairs on O and Cℓ", 1]],
         ["Which atom is in the middle?", "How many lone pairs do O and Cℓ each keep?"],
         memo="The memo's structure: H:Ö:Cℓ: (two lone pairs on O, three on Cℓ)."),
    draw("2.2.2", "Draw the Lewis structure for: HCN", 2, [["H : C and C ⋮ N (a triple bond)", 1], ["One lone pair on N", 1]],
         ["How many bonds does C make?", "How many electrons does N have left after three shared pairs?"],
         memo="The memo's structure: H:C:::N: (one lone pair on N)."),
    answer("2.3.1", "Write down the name of the molecular shape for: H₂S", 1, ["Bent (angular)", "Linear", "Trigonal planar", "Tetrahedral"],
           ["How many bonding pairs and lone pairs on S?", "Two bonds and two lone pairs give which shape?"]),
    answer("2.3.2", "Write down the name of the molecular shape for: NF₃", 1, ["Trigonal pyramidal", "Trigonal planar", "Tetrahedral", "Bent"],
           ["Three bonding pairs and one lone pair on N.", "Does the lone pair push the three bonds into a pyramid?"]),
    stmt("2.4", "Is NF₃ a POLAR or NON-POLAR molecule?\nFully explain the answer.", 4,
         ["POLAR", "F is more electronegative than N (ΔEN = 4,0 − 3,0 = 1).", "The N–F bond is polar.", "NF₃'s molecular geometry is asymmetrical."],
         ["NON-POLAR", "N and F have the same electronegativity.", "NF₃ is symmetrical, so its dipoles cancel.", "NF₃ has no lone pairs."],
         ["Compare the electronegativities of N and F.", "Do the bond dipoles cancel in a trigonal pyramid?"], 1)]
q25 = [
    answer("2.5.1", "Use the letters A, B, C or D as it appears on the graph above to identify: Bond energy", 1, ["B", "A", "C", "D"],
           ["Bond energy is the depth of the energy well.", "Which letter marks the drop from zero to the lowest point?"]),
    answer("2.5.2", "Use the letters A, B, C or D as it appears on the graph above to identify: Point when repulsive forces are stronger than the "
           "attractive forces", 1, ["D", "A", "B", "C"], ["Where are the two nuclei pushed closest together?", "Where is the potential energy "
                                                                                                              "highest?"]),
    stmt("2.5.3", "Explain the formation of H₂ from the graph.\nRefer to the electrostatic force between the protons and electrons and energy "
         "involved.", 2,
         ["As the two H atoms approach, each atom's electron is attracted to the other atom's nucleus (proton).",
          "The attractive forces are greater than the repulsive forces, so the potential energy decreases to a minimum (the most stable state)."],
         ["The two protons attract each other.", "The potential energy increases as the atoms approach.",
          "The repulsive forces are greater than the attractive forces at the bond length.", "Energy is absorbed when the bond forms."],
         ["What does each nucleus attract as the atoms come closer?", "What happens to the potential energy until the bond forms?"], 1)]

# ---- QUESTION 3, the question paper pages 9-10 and the memo pages 5-6 ----
q31 = [
    answer("3.1.1", "Write down the name of the predominant intermolecular force that is represented by letter (b) in the diagram above.", 1,
           ["Hydrogen bond", "London forces", "Dipole-dipole forces", "Covalent bond"],
           ["b is between two NH₃ molecules.", "H is bonded to N, a small and very electronegative atom."]),
    stmt("3.1.2", "Write down TWO requirements for the formation of the force named in QUESTION 3.1.1.", 2,
         ["A hydrogen atom covalently bonded to a highly electronegative atom.", "A lone pair of electrons on a nearby highly electronegative "
                                                                                  "atom."],
         ["A hydrogen atom ionically bonded to a metal.", "Two non-polar molecules close together.", "A molecule with no lone pairs.",
          "A large molecular mass."], ["To which kind of atom must H be bonded?", "What must the other molecule offer?"], 1, after=["3.1.1"]),
    answer("3.1.3", "Write down the name of bond labelled (a).", 1, ["(Polar) covalent bond", "Hydrogen bond", "Ionic bond", "Metallic bond"],
           ["a is inside one NH₃ molecule.", "N and H share a pair of electrons."]),
    mcq("3.1.4", "Which ONE (a or b) requires the highest amount of energy to break/overcome its forces?", ["a", "b"], 0,
        ["Which is stronger: a bond inside a molecule or a force between molecules?", "Boiling NH₃ does not break its N–H bonds."], marks=1)]
q32 = [
    stmt("3.2.1", "Define the term boiling point.", 2, ["The temperature at which the vapour pressure of a substance equals the atmospheric "
                                                        "pressure."],
         ["The temperature at which a solid changes into a liquid.", "The temperature at which a substance's vapour pressure is zero.",
          "The temperature at which water boils at sea level.", "The temperature at which all intermolecular forces disappear."],
         ["Boiling starts when the vapour pressure reaches what?", "Is it about melting or boiling?"], 2),
    answer("3.2.2", "Write down the phase of the hydrogen halides at room temperature.", 1, ["Gas", "Liquid", "Solid", "Liquid and gas"],
           ["Room temperature is about 25 °C.", "Are all the boiling points below or above that?"]),
    stmt("3.2.3", "Explain the trend observed in the boiling points of the hydrogen halides by referring to the molecular size and energy "
         "involved.", 3,
         ["From H₂S to H₂Te the molecular size increases.", "As the molecular size increases, so do the London forces.",
          "More energy is needed to overcome the intermolecular forces from H₂S to H₂Te."],
         ["From H₂S to H₂Te the molecular size decreases.", "Hydrogen bonds get stronger from H₂S to H₂Te.",
          "Less energy is needed to overcome the intermolecular forces from H₂S to H₂Te.", "London forces get weaker as the molecules get "
                                                                                             "bigger."],
         ["How does the size change down the group?", "How does that affect the London forces and the energy to boil?"], 1),
    stmt("3.2.4", "Which hydrogen halide (H₂S, H₂Se or H₂Te) will have the lowest vapour pressure at a certain temperature?\nGive a reason for the "
         "answer.", 2, ["H₂Te", "It has the highest boiling point."],
         ["H₂S", "It has the lowest boiling point.", "H₂Se", "It has the weakest intermolecular forces."],
         ["Which compound evaporates least easily?", "How is that linked to the boiling point?"], 1),
    mcq("3.2.5", "How will the boiling point of HF compare to that of H₂S?\nChoose from HIGHER THAN, LOWER THAN or EQUAL TO.", CMP, 0,
        ["Which intermolecular force does HF have?", "Stronger forces mean a higher boiling point."], marks=1),
    stmt("3.2.6", "Explain the answer in QUESTION 3.2.5 by referring to type of intermolecular forces and energy involved.", 4,
         ["HF has hydrogen bonds.", "H₂S has dipole-dipole forces.", "Hydrogen bonds are stronger than dipole-dipole forces.",
          "More energy is needed to overcome the intermolecular forces in HF."],
         ["H₂S has hydrogen bonds.", "HF has only London forces.", "Dipole-dipole forces are stronger than hydrogen bonds.",
          "Less energy is needed to overcome the intermolecular forces in HF."],
         ["Is H bonded to N, O or F in each compound?", "Which force is stronger?"], 1, after=["3.2.5"])]

# ---- QUESTION 4, the question paper page 11 and the memo pages 7-8 ----
q4 = [
    answer("4.1", "Name the gas law that is investigated.", 1, ["Boyle's law", "Charles's law", "Gay-Lussac's law", "The general gas law"],
           ["Which two quantities are varied?", "Which law links pressure and volume at constant temperature?"]),
    stmt("4.2.1", "From the investigation write down: An investigative question for this investigation", 2,
         ["How does the pressure of a gas affect its volume?", "What is the relationship between the pressure and the volume of a gas?"],
         ["How does the temperature of a gas affect its volume?", "What is the pressure of the gas?", "Does a gas have mass?",
          "How does the volume of a liquid change with pressure?"],
         ["An investigative question names the independent and dependent variables.", "Which two quantities are they here?"], 2),
    stmt("4.2.2", "From the investigation write down: TWO controlled variables for this investigation", 2,
         ["Temperature", "Amount (mass) of gas"], ["Pressure", "Volume", "The inverse of the volume (1/V)"],
         ["Which quantities are kept the same?", "Pressure and volume are the ones that change."], 1),
    stmt("4.3", "Explain the relationship observed between pressure and volume by referring to the kinetic molecular theory.", 3,
         ["The same number of gas particles now occupy a smaller volume.", "The particles collide with each other and the walls of the "
                                                                            "container more frequently.",
          "More frequent collisions mean a greater pressure."],
         ["The particles move faster when the volume decreases.", "The particles get bigger when the pressure increases.",
          "Fewer collisions mean a greater pressure.", "The number of particles increases when the volume decreases."],
         ["What happens to the space for the particles as the volume decreases?", "How does that change the collisions with the walls?"], 1),
    work("4.4", "Determine the volume that the gas occupied at 96 kPa.", 2, [
        "At 96 kPa, {1}/{V} = 0,66 × 10⁻¹ cm⁻³\nV = {1}/{0,66 × 10⁻¹} = 15,15 cm³",      # the memo
        "At 96 kPa, {1}/{V} = 0,66 × 10⁻¹ cm⁻³\nV = 0,66 × 10⁻¹ = 0,066 cm³",            # the reading not turned over
        "At 96 kPa, {1}/{V} = 0,66 cm⁻³\nV = {1}/{0,66} = 1,52 cm³",                      # the × 10⁻¹ left off
        "At 96 kPa, {1}/{V} = 0,66 × 10⁻¹ cm⁻³\nV = 0,66 cm³"],                           # read as the volume
        ["Read 1/V at 96 kPa: mind the axis scale (× 10⁻¹ cm⁻³).", "Then turn it over to get V."]),
    work("4.5", "Calculate the volume occupied by the gas at 252 kPa.", 4, [
        "p₁V₁ = p₂V₂\n(96)(15,15) = (252)V₂\nV₂ = 5,77 cm³",                 # the memo
        "p₁V₂ = p₂V₁\n(96)V₂ = (252)(15,15)\nV₂ = 39,77 cm³",                # the pressures swapped
        "p₁V₁ = p₂V₂\n(96)(0,066) = (252)V₂\nV₂ = 0,025 cm³",                # 1/V used for V
        "{p₁}/{V₁} = {p₂}/{V₂}\n{96}/{15,15} = {252}/{V₂}\nV₂ = 39,77 cm³"],  # p/V taken as constant
        ["Boyle's law: which product stays the same?", "Use the volume from 4.4."], after=["4.4"]),
    stmt("4.6", "It is observed that the gas does not obey the gas law named in QUESTION 4.1 at very high pressure. Explain this observation.", 3,
         ["At very high pressure the particles are very close together.", "The volume of the gas particles themselves becomes significant.",
          "The volume measured is higher than the gas law predicts."],
         ["At very high pressure the particles move faster.", "The gas particles disappear at high pressure.",
          "The volume measured is lower than the gas law predicts.", "At very high pressure the temperature drops to zero."],
         ["Does the ideal gas model count the particles' own volume?", "When does that volume start to matter?"], 1)]

# ---- QUESTION 5, the question paper page 12 and the memo pages 8-9 ----
q5 = [
    stmt("5.1", "Define the term heat of reaction.", 2, ["The energy absorbed or released per mole in a chemical reaction."],
         ["The minimum energy needed for a reaction to start.", "The energy of the activated complex.", "The heat of the products only.",
          "The temperature change of a reaction."], ["Is it about energy per mole?", "Absorbed or released in what?"], 2),
    stmt("5.2", "Is the above reaction ENDOTHERMIC or EXOTHERMIC?\nGive a reason for the answer.", 2,
         ["EXOTHERMIC", "The heat (enthalpy) of the products is less than that of the reactants (ΔH < 0)."],
         ["ENDOTHERMIC", "The products have more energy than the reactants.", "ΔH > 0", "Energy is absorbed from the surroundings."],
         ["Compare the energy of the products with that of the reactants.", "Is energy released or absorbed?"], 1),
    work("5.3", "Calculate the heat of reaction.", 2, [
        "ΔH = H(products) − H(reactants)\nΔH = 0 − 164,1\nΔH = −164,1 kJ·mol⁻¹",                         # the memo
        "ΔH = H(reactants) − H(products)\nΔH = 164,1 − 0\nΔH = +164,1 kJ·mol⁻¹",                         # subtracted the wrong way
        "ΔH = E(a) = 405,30 − 164,1\nΔH = 241,20\nΔH = 241,20 kJ·mol⁻¹",                                 # the activation energy
        "ΔH = −(energy released) + H(reactants)\nΔH = −405,30 + 164,1\nΔH = −241,20 kJ·mol⁻¹"],          # the released energy used
        ["Which formula gives ΔH from the graph?", "The products are at 0 kJ·mol⁻¹."]),
    work("5.4", "The energy that is released from the formation of N₂ and O₂ molecules are 405,30 kJ·mol⁻¹.\nCalculate the activation energy for "
         "this reaction.", 3, [
        "E(a) = 405,30 − 164,1\nE(a) = 241,20 kJ·mol⁻¹",     # the memo
        "E(a) = 405,30 + 164,1\nE(a) = 569,40 kJ·mol⁻¹",     # added
        "E(a) = 405,30\nE(a) = 405,30 kJ·mol⁻¹",             # the released energy taken as E(a)
        "E(a) = 164,1 − 0\nE(a) = 164,1 kJ·mol⁻¹"],          # ΔH taken as E(a)
        ["The peak is 405,30 kJ·mol⁻¹ above the products at 0.", "E(a) is the climb from the reactants at 164,1 to the peak."]),
    draw("5.5", "Redraw the energy profile graph in your ANSWER BOOK. Draw on the same set of axes the effect that a catalyst would have on the "
         "energy profile graph. Indicate the graph of the catalyst with a dotted line.", 2,
         [["The catalyst's peak is lower", 1], ["The graphs start at the same reactants' level and end at the same products' level", 1]],
         ["Does a catalyst change the reactants' or the products' energy?", "What does it do to the activation energy?"],
         memo="The memo's graph: the original curve from 164,1 to 0 and a dotted curve with the same ends and a lower peak.")]

# ---- QUESTION 6, the question paper page 13 and the memo pages 10-11 ----
EMP = "n(C) : n(H) : n(O) = {54,54}/{12} : {9,1}/{1} : {36,36}/{16}\n= 4,545 : 9,1 : 2,2725\n"
MOH = "n = cV = (0,326)(0,1) = 0,0326 mol\nM = {m}/{n} = {1,826}/{0,0326} = 56 g·mol⁻¹\nM + 16 + 1 = 56, so M = 39\n"
q6 = [
    stmt("6.1", "Define the term molar mass.", 2, ["The mass of one mole of a substance."],
         ["The mass of one molecule.", "The number of particles in one mole.", "The mass of a substance per dm³ of solution.",
          "The total mass of all the atoms in a sample."], ["Molar mass is measured in g·mol⁻¹.", "The mass of how much substance?"], 2),
    work("6.2", "Determine by calculation, the molecular formula of the organic compound (CxHyOz)", 7, [
        EMP + "= 2 : 4 : 1 (÷ 2,2725)\nEmpirical formula C₂H₄O, M = 2(12) + 4(1) + 16 = 44\n{88}/{44} = 2: molecular formula C₄H₈O₂",   # the memo
        "C : H : O = 54,54 : 9,1 : 36,36 (the masses)\n= 5,99 : 1 : 3,99 (÷ 9,1)\n= 6 : 1 : 4\nEmpirical formula C₆HO₄, M = 6(12) + 1 + 4(16) = "
        "137\n{88}/{137} ≈ 1: molecular formula C₆HO₄",                                                                              # masses not ÷ M
        EMP + "= 2 : 4 : 1 (÷ 2,2725)\nEmpirical formula C₂H₄O, M = 2(12) + 4(1) + 16 = 44\nRatio taken as 1: molecular formula C₂H₄O",   # empirical as molecular
        "n(C) : n(H) : n(O) = {54,54}/{12} : {9,1}/{1} : {36,36}/{32}\n= 4,545 : 9,1 : 1,136\n= 4 : 8 : 1 (÷ 1,136)\nEmpirical formula "
        "C₄H₈O, M = 4(12) + 8(1) + 16 = 72\n{88}/{72} ≈ 1: molecular formula C₄H₈O"],                                                  # O ÷ 32
        ["Divide each mass by its element's molar mass.", "How many empirical units fit into 88 g·mol⁻¹?"])]
q63 = [
    stmt("6.3.1", "Define the term concentration.", 2, ["The amount of solute per litre (dm³) of solution."],
         ["The mass of solvent in a solution.", "The volume of a solution.", "The number of moles of solvent.", "The mass of solute in one "
                                                                                                                  "molecule."],
         ["Concentration is measured in mol·dm⁻³.", "The amount of what, in how much?"], 2),
    work("6.3.2", "Determine by calculation, the name of the metal hydroxide.", 5, [
        MOH + "MOH = potassium hydroxide (KOH)",                                                                 # the memo
        MOH + "MOH = sodium hydroxide (NaOH)",                                                                   # the wrong element for 39
        "n = cV = (0,326)(0,1) = 0,0326 mol\nM = {m}/{n} = {1,826}/{0,0326} = 56 g·mol⁻¹\nM = 56 taken as the metal\nMOH = iron hydroxide (FeOH)",  # 56 as the metal
        "n = cV = (0,326)(100) = 32,6 mol\nM = {m}/{n} = {1,826}/{32,6} = 0,056 g·mol⁻¹\nM + 16 + 1 = 0,056\nNo metal fits"],  # 100 cm³ not in dm³
        ["How many moles are in 100 cm³ of a 0,326 mol·dm⁻³ solution?", "M(MOH) − M(OH) gives the metal's molar mass."])]

# ---- QUESTION 7, the question paper page 14 and the memo pages 12-13 ----
q7 = [
    stmt("7.1", "Define the term limiting reagent.", 2, ["The substance that is completely used up during a chemical reaction."],
         ["A reactant that is left over after the reaction.", "A substance that speeds up a reaction without being used up.",
          "The product formed in the smallest amount.", "The reactant with the largest mass."],
         ["Which reactant stops the reaction?", "Is it used up or left over?"], 2),
    work("7.2", "Calculate the mass of calcium carbonate contained in the 1,5 g sample of eggshells.", 5, [
        "n(CO₂) = {V}/{V(m)} = {0,325}/{22,4} = 0,0145 mol\nn(CaCO₃) = n(CO₂) = 0,0145 mol (1 : 1)\nm = nM = (0,0145)(100)\nm = 1,45 g",   # the memo
        "n(CO₂) = {V}/{V(m)} = {325}/{22,4} = 14,51 mol\nn(CaCO₃) = n(CO₂) = 14,51 mol (1 : 1)\nm = nM = (14,51)(100)\nm = 1 451 g",      # cm³ not dm³
        "n(CO₂) = {V}/{V(m)} = {0,325}/{22,4} = 0,0145 mol\nn(CaCO₃) = 2(0,0145) = 0,029 mol\nm = nM = (0,029)(100)\nm = 2,90 g",         # a 1 : 2 ratio
        "n(CO₂) = {V}/{V(m)} = {0,325}/{24,45} = 0,0133 mol\nn(CaCO₃) = n(CO₂) = 0,0133 mol (1 : 1)\nm = nM = (0,0133)(100)\nm = 1,33 g"],  # the room-temperature V(m)
        ["The CO₂ was collected at STP: what is V(m)?", "325 cm³ in dm³; then the mole ratio CaCO₃ : CO₂."]),
    work("7.3", "Calculate the percentage purity of calcium carbonate in 1,5 g of eggshells.", 2, [
        "% purity = {1,45}/{1,5} × 100\n= 96,67%",      # the memo
        "% purity = {1,5}/{1,45} × 100\n= 103,45%",     # upside down
        "% purity = {1,45}/{1,5}\n= 0,97%",             # × 100 left out
        "% purity = {1,5 − 1,45}/{1,5} × 100\n= 3,33%"],  # the impurities
        ["Pure mass ÷ sample mass × 100.", "Which mass is the pure CaCO₃?"], after=["7.2"]),
    work("7.4", "Calculate the number of molecules of HCℓ that reacted with calcium carbonate.", 4, [
        "n(HCℓ) = 2(0,0145) = 0,029 mol\nN = nN(A) = 0,029 × 6,02 × 10²³\nN = 1,75 × 10²² molecules",      # the memo
        "n(HCℓ) = 0,0145 mol (1 : 1)\nN = nN(A) = 0,0145 × 6,02 × 10²³\nN = 8,73 × 10²¹ molecules",          # the 1 : 2 ratio ignored
        "n(HCℓ) = 2(0,0145) = 0,029 mol\nN = {n}/{N(A)} = {0,029}/{6,02 × 10²³}\nN = 4,82 × 10⁻²⁶ molecules",  # divided by N(A)
        "n(HCℓ) = {0,0145}/{2} = 0,00725 mol\nN = nN(A) = 0,00725 × 6,02 × 10²³\nN = 4,36 × 10²¹ molecules"],  # the ratio upside down
        ["What is the mole ratio of HCℓ to CaCO₃?", "N = n × N(A)."], after=["7.2"]),
    stmt("7.5", "How does the carbon dioxide gas produced after 8 min compare to the carbon dioxide gas produced at 5 min?\nWrite down only "
         "HIGHER THAN, SMALLER THAN or EQUAL TO. Give a reason for the answer.", 2,
         ["EQUAL TO", "All the calcium carbonate had reacted by 5 min, so no more CO₂ was produced."],
         ["HIGHER THAN", "SMALLER THAN", "The reaction speeds up after 5 min.", "The HCℓ ran out at 5 min."],
         ["What does the flat part of the graph after 5 min mean?", "Which reactant ran out?"], 1)]

# ---- QUESTION 8, the question paper page 15 and the memo pages 14-15 ----
N835 = "n(HNO₃) initial = cV = (0,25)(0,5) = 0,125 mol\nn(HNO₃) excess = cV = (1,58 × 10⁻³)(1) = 1,58 × 10⁻³ mol\n"
q8 = [
    stmt("8.1", "Define an acid in terms of Arrhenius theory.", 2,
         ["An acid is a substance that produces hydrogen ions (H⁺) / hydronium ions (H₃O⁺) when it dissolves in water."],
         ["An acid is a substance that produces hydroxide ions (OH⁻) when it dissolves in water.", "An acid is a substance that accepts electrons.",
          "An acid is a substance that turns phenolphthalein pink.", "An acid is a substance that accepts protons."],
         ["Arrhenius defines acids by the ions they make in water.", "Which ion?"], 2),
    answer("8.2.1", "From the reaction above, write down the: Formulae of the TWO substances that can act as ampholytes", 2,
           ["HSO₄⁻ and H₂O", "H₃O⁺ and SO₄²⁻", "HSO₄⁻ and SO₄²⁻", "H₂O and H₃O⁺"],
           ["An ampholyte can both donate and accept a proton.", "Which two can still lose an H⁺ and also gain one?"]),
    answer("8.2.2", "From the reaction above, write down the: Conjugate base of HSO₄⁻", 1, ["SO₄²⁻", "H₂SO₄", "H₃O⁺", "HSO₄²⁻"],
           ["A conjugate base has one proton fewer.", "What is HSO₄⁻ without its H⁺?"])]
q83 = [
    stmt("8.3.1", "Describe the term acid base indicator.", 2,
         ["A weak acid or a weak base whose colour changes as the H⁺ or OH⁻ concentration of the solution changes."],
         ["A strong acid that neutralises a base.", "A substance that speeds up a neutralisation reaction.",
          "A solution of known concentration used in a titration.", "A salt formed in a neutralisation reaction."],
         ["What does an indicator show?", "Is it a strong or a weak acid or base?"], 2),
    answer("8.3.2", "Write down the colour when bromothymol blue is added to HNO₃ solution.", 1, ["Yellow", "Blue", "Green", "Pink"],
           ["Bromothymol blue changes colour between acids and bases.", "HNO₃ is an acid."]),
    stmt("8.3.3", "Is the reaction above EXOTHERMIC or ENDOTHERMIC?\nGive a reason for the answer.", 2,
         ["EXOTHERMIC", "It gives off heat: the temperature rises."],
         ["ENDOTHERMIC", "It absorbs heat from the surroundings.", "The temperature drops.", "ΔH > 0"],
         ["What happened to the temperature of the mixture?", "Is heat given off or taken in?"], 1),
    work("8.3.4", "Calculate the concentration of H₃O⁺ in the final solution.", 3, [
        "pH = −log[H₃O⁺] = 2,8\n[H₃O⁺] = 10^(−2,8)\n[H₃O⁺] = 1,58 × 10⁻³ mol·dm⁻³",                              # the memo
        "pH = −log[H₃O⁺] = 2,8\n[H₃O⁺] = 10^(2,8)\n[H₃O⁺] = 630,96 mol·dm⁻³",                                    # the sign lost
        "pH = −log[H₃O⁺] = 2,8\n[H₃O⁺] = −log(2,8)\n[H₃O⁺] = −0,45 mol·dm⁻³",                                    # log taken again
        "pOH = 2,8 (pH taken as pOH)\n[OH⁻] = 10^(−2,8) = 1,58 × 10⁻³\n[H₃O⁺] = {1 × 10⁻¹⁴}/{1,58 × 10⁻³} = 6,31 × 10⁻¹² mol·dm⁻³"],  # pH as pOH
        ["pH = −log[H₃O⁺]: how do you undo a log?", "[H₃O⁺] = 10^(−pH)."]),
    work("8.3.5", "Calculate the initial concentration of NaOH solution.", 7, [
        N835 + "n(HNO₃) reacted = 0,125 − 1,58 × 10⁻³ = 0,123 mol\nn(NaOH) = n(HNO₃) reacted = 0,123 mol (1 : 1)\n"
               "c(NaOH) = {n}/{V} = {0,123}/{0,5} = 0,246 mol·dm⁻³",                                                       # the memo
        "n(HNO₃) initial = cV = (0,25)(0,5) = 0,125 mol\nn(HNO₃) excess = cV = (1,58 × 10⁻³)(0,5) = 7,9 × 10⁻⁴ mol\n"
        "n(HNO₃) reacted = 0,125 − 7,9 × 10⁻⁴ = 0,124 mol\nn(NaOH) = n(HNO₃) reacted = 0,124 mol (1 : 1)\n"
        "c(NaOH) = {n}/{V} = {0,124}/{0,5} = 0,248 mol·dm⁻³",                                                              # the excess in 0,5 dm³
        N835 + "n(HNO₃) reacted = 0,125 + 1,58 × 10⁻³ = 0,127 mol\nn(NaOH) = n(HNO₃) reacted = 0,127 mol (1 : 1)\n"
               "c(NaOH) = {n}/{V} = {0,127}/{0,5} = 0,253 mol·dm⁻³",                                                       # the excess added
        N835 + "n(HNO₃) reacted = 0,125 − 1,58 × 10⁻³ = 0,123 mol\nn(NaOH) = n(HNO₃) reacted = 0,123 mol (1 : 1)\n"
               "c(NaOH) = {n}/{V} = {0,123}/{1} = 0,123 mol·dm⁻³"],                                                        # the total volume for NaOH's
        ["How much HNO₃ was there, and how much was left over in the 1 dm³ mixture?", "The NaOH used up the rest, 1 : 1, in 500 cm³."],
        after=["8.3.4"])]

# ---- QUESTION 9, the question paper pages 16-17 and the memo page 16 ----
HALF9 = "Cr₂O₇²⁻ + 14 H⁺ + 6e⁻ → 2 Cr³⁺ + 7 H₂O\n"
q9 = [
    stmt("9.1", "Explain the term oxidation in terms of oxidation number.", 2, ["Oxidation is an increase in oxidation number."],
         ["Oxidation is a decrease in oxidation number.", "Oxidation is a gain of electrons.", "Oxidation is the gain of hydrogen.",
          "Oxidation is when the oxidation number stays the same."],
         ["An oxidised substance loses electrons.", "What does losing electrons do to the oxidation number?"], 2),
    answer("9.2.1", "Write down the chemical symbol of a substance that is oxidised.", 2, ["Aℓ", "Cu²⁺", "Cu", "Aℓ³⁺"],
           ["Which species loses electrons?", "Whose oxidation number goes from 0 to +3?"]),
    answer("9.2.2", "Write down the chemical symbol of a substance that is the oxidising agent.", 2, ["Cu²⁺", "Aℓ", "Cu", "SO₄²⁻"],
           ["An oxidising agent is itself reduced.", "Which species gains electrons?"]),
    stmt("9.3", "Will the oxidation number of the sulphate ion INCREASE, DECREASE or REMAIN THE SAME during this reaction?\nGive a reason for the "
         "answer.", 2, ["REMAIN THE SAME", "It is a spectator ion."],
         ["INCREASE", "DECREASE", "The sulphate ion is oxidised.", "The sulphate ion is reduced to sulphur."],
         ["Does the sulphate ion appear in the net ionic equation?", "What do we call an ion that does not change?"], 1)]
q94 = [
    work("9.4.1", "Determine the oxidation number of chromium (Cr) in Cr₂O₇²⁻.", 2, [
        "2x + 7(−2) = −2\nx = +6",       # the memo
        "x + 7(−2) = −2\nx = +12",       # one Cr counted
        "2x + 7(−2) = 0\nx = +7",        # the ion's charge ignored
        "2x + 7(−2) = −2\nx = −6"],      # the sign lost
        ["The oxidation numbers add up to the ion's charge.", "Each O is −2."]),
    answer("9.4.2", "Will the concentration of the potassium dichromate INCREASE, DECREASE or REMAINS THE SAME as the reaction proceeds?\nExplain "
           "the answer by referring to the relevant half-reaction.", 4, [
        "DECREASES: Cr₂O₇²⁻ + 14 H⁺ + 6e⁻ → 2 Cr³⁺ + 7 H₂O, so the dichromate is reduced to Cr³⁺ and used up.",
        "INCREASES: Fe²⁺ → Fe³⁺ + e⁻ makes more dichromate.",
        "DECREASES: 2 Cr³⁺ + 7 H₂O → Cr₂O₇²⁻ + 14 H⁺ + 6e⁻, so the dichromate is oxidised.",
        "REMAINS THE SAME: potassium dichromate is a spectator."],
        ["Is the dichromate oxidised or reduced?", "Does it get used up?"], after=["9.4.1"]),
    work("9.4.3", "Write down the balanced net ionic equation for this reaction.", 3, [
        HALF9 + "6(Fe²⁺ → Fe³⁺ + e⁻)\nCr₂O₇²⁻ + 6 Fe²⁺ + 14 H⁺ → 2 Cr³⁺ + 6 Fe³⁺ + 7 H₂O",                                    # the memo
        HALF9 + "Fe²⁺ → Fe³⁺ + e⁻\nCr₂O₇²⁻ + Fe²⁺ + 14 H⁺ → 2 Cr³⁺ + Fe³⁺ + 7 H₂O",                                          # electrons not balanced
        HALF9 + "6(Fe²⁺ → Fe³⁺ + e⁻)\nCr₂O₇²⁻ + 6 Fe²⁺ + 14 H⁺ + 6e⁻ → 2 Cr³⁺ + 6 Fe³⁺ + 7 H₂O + 6e⁻",                       # electrons left in
        HALF9 + "6(Fe³⁺ + e⁻ → Fe²⁺)\n2 Cr³⁺ + 6 Fe³⁺ + 7 H₂O → Cr₂O₇²⁻ + 6 Fe²⁺ + 14 H⁺"],                                   # reversed
        ["How many electrons does each half-reaction move?", "Multiply so they cancel, then add."], after=["9.4.2"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Chemical bonding", "marks": 12,
     "lead": "Consider the following substances (A–D):\nA: HOCℓ\nB: NF₃\nC: H₂S\nD: HCN", "items": q2},
    {"id": "2.5", "title": "Question 2.5", "kind": "Bond formation", "marks": 4,
     "lead": "Two hydrogen atoms form a bond according to the energy profile graph shown below.",
     "figure": P.fig("2.5", "Potential energy against distance for two H atoms: far apart at A (energy zero); the curve falls to its lowest point, "
                            "B marking the depth below zero; C marks the distance at the bottom; at D, close together, the energy is high."),
     "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Intermolecular forces", "marks": 5,
     "lead": "The diagram below is used to demonstrate the differences between intermolecular forces and intramolecular forces (chemical bonds) "
             "between two NH₃ molecules.",
     "figure": P.fig("3.1", "Two NH₃ molecules, one above the other: a labels an N–H bond inside the top molecule; b labels the dashed "
                            "attraction between an H of the top molecule and the lone pair on the N of the lower one."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Intermolecular forces", "marks": 13,
     "lead": "Consider the boiling points of the hydrogen halides on group 16 as shown on the table below.\nA: H₂S, −60 °C\nB: H₂Se, −41 °C\n"
             "C: H₂Te, −2 °C", "items": q32},
    {"id": "4", "title": "Question 4", "kind": "Ideal gases", "marks": 17,
     "lead": "A group of learners investigated the relationship between the pressure and volume of a certain gas. The graph of the pressure "
             "versus inverse of volume was obtained from the data in the investigation.",
     "figure": P.fig("Q4", "Pressure (kPa, 0 to 140) against 1/volume (× 10⁻¹ cm⁻³, 0 to 1,15): a straight line from the origin through "
                           "data points near the top."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Energy and change", "marks": 11,
     "lead": "Consider the balanced equation that shows the decomposition of nitrogen oxide (N₂O) into nitrogen (N₂) and oxygen (O₂) molecules.\n"
             "2 N₂O(g) → 2 N₂(g) + O₂(g)\nThe energy profile graph is drawn for the decomposition of N₂O.",
     "figure": P.fig("Q5", "Potential energy (kJ·mol⁻¹) against reaction progress: the reactants at 164,1, a peak, and the products at 0."),
     "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Quantitative aspects", "marks": 9,
     "lead": "A certain organic compound (CxHyOz) is composed of 54,54 g of carbon; 9,1 g of hydrogen and 36,36 g of oxygen and has a molecular "
             "mass of 88 g·mol⁻¹.", "items": q6},
    {"id": "6.3", "title": "Question 6.3", "kind": "Quantitative aspects", "marks": 7,
     "lead": "A bottle in a laboratory contains an unknown metal hydroxide (MOH). A lab technician dissolves 1,826 g of the metal hydroxide to "
             "make a 100 cm³ solution. Upon analysis it was found that the concentration of the metal hydroxide is 0,326 mol·dm⁻³.",
     "items": q63},
    {"id": "7", "title": "Question 7", "kind": "Quantitative aspects", "marks": 15,
     "lead": "Learners crushed eggshells to determine the percentage of calcium carbonate that are found in a 1,5 g sample. The crushed eggshells "
             "are allowed to react with EXCESS hydrochloric acid.\nCaCO₃(s) + 2 HCℓ(aq) → CaCℓ₂(aq) + CO₂(g) + H₂O(ℓ)\nThe calcium carbonate "
             "reacted completely in 5 minutes. The graph below shows the carbon dioxide gas that was collected at STP.",
     "figure": P.fig("Q7", "Volume of CO₂ collected (cm³) against time (minutes): the curve rises steeply and levels off at 325 cm³ by 5 "
                           "minutes."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Acids and bases", "marks": 5,
     "lead": "Consider the reaction below:\nHSO₄⁻(aq) + H₂O(ℓ) → H₃O⁺(aq) + SO₄²⁻(aq)", "items": q8},
    {"id": "8.3", "title": "Question 8.3", "kind": "Acids and bases", "marks": 15,
     "lead": "500 cm³ of NaOH are added to 500 cm³ of HNO₃ with a concentration of 0,25 mol·dm⁻³. The temperature of the reaction mixture rises "
             "during the reaction. The pH of the final solution is 2,8.\nNaOH(aq) + HNO₃(aq) → NaNO₃(aq) + H₂O(ℓ)", "items": q83},
    {"id": "9", "title": "Question 9", "kind": "Redox reactions", "marks": 8,
     "lead": "A clean piece of aluminium metal strip is placed in a copper sulphate (CuSO₄) solution. The reaction was observed again after 2 hours.\n"
             "After 2 hours it was observed that the blue solution turned colourless and the shiny metallic aluminium turned brown.\n"
             "2 Aℓ(s) + 3 Cu²⁺(aq) → 3 Cu(s) + 2 Aℓ³⁺(aq)",
     "figure": P.fig("Q9", "Two test tubes: at the start, a coiled aluminium strip in blue CuSO₄ solution; after 2 hours, a brown-coated "
                           "strip in a colourless solution."), "items": q9},
    {"id": "9.4", "title": "Question 9.4", "kind": "Redox reactions", "marks": 9,
     "lead": "Acidified potassium dichromate (K₂Cr₂O₇) is an orange solution due to the presence of the dichromate ions (Cr₂O₇²⁻).\n(For 9.4.2 and "
             "9.4.3: when iron sulphate solution (FeSO₄) is added to acidified potassium dichromate (K₂Cr₂O₇) solution, the solution changes "
             "colour from orange to green after a few seconds. During this reaction Fe²⁺ ions were oxidised to Fe³⁺ and Cr₂O₇²⁻ is reduced to "
             "Cr³⁺.)", "items": q94},
]
P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P2", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
         [P.flag_workings(),
          P.flag_answers("9.4.2 ('explain by the half-reaction') plays as named statements."),
          {"n": "2.2.1", "kind": "no_fit", "detail": "Every drawing plays as pick the drawing: the Lewis structures (2.2.1, 2.2.2) and the energy "
                                                     "profile with the catalyst (5.5), the memo's and three mistakes it marks down."},
          {"n": "9.1", "kind": "memo_issue", "detail": "The memo (page 16) defines oxidation NUMBER ('a number that shows the number of electrons "
                                                       "an atom has gained, lost or shared'); the question asks for oxidation in terms of "
                                                       "oxidation number: an increase in oxidation number. The right card is that; the memo's "
                                                       "sentence is on no card."},
          {"n": "6.2", "kind": "memo_issue", "detail": "The memo's line (page 10) divides 5,545 for carbon; 54,54/12 = 4,545, which its ratio 2 : 4 "
                                                       ": 1 uses. The right option writes 4,545."}],
         {"1": 20, "2": 16, "3": 18, "4": 17, "5": 11, "6": 16, "7": 15, "8": 20, "9": 17}, 150,
         {"3.1.2": ["3.1.1"], "3.2.6": ["3.2.5"], "4.5": ["4.4"], "7.3": ["7.2"], "7.4": ["7.2"], "8.3.5": ["8.3.4"], "9.4.2": ["9.4.1"],
          "9.4.3": ["9.4.2"]},
         "Questions 1 to 9 (the whole paper)")
