"""Grade 10 Physical Sciences P2 (Chemistry) November 2024 (North West Department of Education, provincial assessment), the whole
paper (Questions 1 to 8, 100 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`.
Stems, options, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions
are ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment, the question paper PDF (English, 12
pages with the data sheets; its diagrams are images) and the marking guidelines PDF (English and Afrikaans, 6 pages), read from
their text and page images (100 dpi). The paper prints Question 7 before Question 6 (page 9); they play in number order.

  python tools/ingest/transcribe_g10_ps_p2_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ps-p2-2024-11-nw/13-November-2024-NW-S2-GR10-Physical-Sciences-QP-P2-ENG.pdf" "uploads/provincial/g10-ps-p2-2024-11-nw/13-November-2024-NW-S2-GR10-Physical-Sciences-MG-P2-ENGAFR.pdf" --id g10-ps-p2-2024-11-nw --from-json

The Grade 12 rulings, as in transcribe_g11_ps_p2_2024_11_ec.py: multiple choice printed in the paper as printed; a choice printed
in the stem (a letter from the table, INCREASE / DECREASE / ..., YES / NO) an MCQ of the printed choices; every calculation an
authored working (provincial.py); a definition, law or explanation statements ("choose and explain" with the choice as a card);
a one-word name a term; the Lewis diagram 4.2.4 pick the drawing (pictures_lower.py).
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ps-p2-2024-11-nw", 595.32, 841.92, {
    "Q3": [6, 198, 148, 362, 275], "Q3.4": [6, 105, 400, 500, 540], "Q5": [8, 138, 147, 459, 387]}, start=10)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term
CHANGE = ["INCREASE", "DECREASE", "REMAIN THE SAME"]
SUBS = ["A: Cobalt", "B: Gold", "C: Phosphorus", "D: Silicon", "E: Air", "F: Ammonium nitrate"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-4 and the memo page 2 ----
q1 = [
    mcq("1.1", "The process when a solid substance changes directly to the gaseous phase is called …",
        ["evaporation.", "condensation.", "sublimation.", "boiling."], 2,
        ["Which phase is skipped?", "Think of dry ice or iodine crystals."]),
    mcq("1.2", "Which ONE of the following substances is a pure substance?", ["Steel", "Sulphur", "Juice", "Salt water"], 1,
        ["A pure substance is one element or one compound.", "Which of the four is a mixture of nothing?"]),
    mcq("1.3", "Which ONE of the following represents the electronic structure of phosphorus (P)?",
        ["1s²2s²2p⁶3s²", "1s²2s²2p⁶3s²3p³", "1s²2s²2p⁶3s²3p⁵", "1s²2s²2p⁶3s²3p⁶"], 1,
        ["How many electrons does phosphorus have?", "Its atomic number is 15: add up the superscripts."]),
    mcq("1.4", "In which ONE of the following compounds do covalent bonds occur between elementary particles?",
        ["Sodium chloride", "Mercury", "Ammonia", "Carbon"], 2,
        ["A covalent bond forms between non-metal atoms.", "Which option is a compound of non-metals?"]),
    mcq("1.5", "What is the percentage of hydrogen in a molecule of hydrogen peroxide with molar mass of 34 g·mol⁻¹, if one mole of "
        "hydrogen reacts with one mole of oxygen?", ["72,72 %", "94,12 %", "11,11 %", "5,88 %"], 3,
        ["What is the formula of hydrogen peroxide?", "% H = mass of hydrogen ÷ molar mass × 100."]),
    mcq("1.6", "If 30 g of reactant A reacts completely with 25 g of reactant B, which ONE of the following statements is CORRECT?",
        ["The total mass of the products will be equal to 55 g.",
         "The total mass of products for any unreacted reactants will be less than 55 g.",
         "The total mass of products for any unreacted reactants will be greater than 55 g.",
         "The total mass of products for any unreacted reactants will be 55 g."], 0,
        ["What does the law of conservation of mass say?", "Both reactants react completely."]),
    mcq("1.7", "Two identical flasks are filled with different gases at the same temperature and pressure. One flask contains ozone (O₃) "
        "and the other an unknown gas X. The mass of the ozone gas in the flask is 0,48 g and the mass of gas X in the flask is 0,34 g. "
        "Gas X is:", ["O₂", "SO₂", "H₂S", "NH₃"], 2,
        ["Equal volumes of gases at the same temperature and pressure contain equal numbers of moles.", "How many moles of O₃ is 0,48 g, "
                                                                                                      "and what molar mass gives 0,34 g?"])]

# ---- QUESTION 2, the question paper page 5 and the memo page 2 ----
q21 = [
    mcq("2.1.1", "Identify the ELEMENT that has a dull surface and cannot conduct electricity.", SUBS, 2,
        ["Which elements in the table are non-metals?", "Non-metals are dull and do not conduct."], marks=1),
    stmt("2.1.2", "Identify ONE substance that is ductile.", 1, ["Cobalt", "Gold"],
         ["Phosphorus", "Silicon", "Air", "Ammonium nitrate"],
         ["Ductile means it can be drawn into a wire.", "Which substances are metals?"], 1),
    mcq("2.1.3", "Which element has magnetic properties?", SUBS, 0,
        ["Iron, cobalt and nickel are magnetic.", "Which of those is in the table?"], marks=1),
    mcq("2.1.4", "Identify the element that is a metalloid.", SUBS, 3,
        ["A metalloid has properties of metals and non-metals.", "It is used in computer chips."], marks=1),
    answer("2.1.5", "Write down the chemical formula for substance F (ammonium nitrate).", 2, ["NH₄NO₃", "NH₃NO₃", "NH₄NO₂", "(NH₄)₂NO₃"],
           ["What are the formulae of the ammonium ion and the nitrate ion?", "NH₄⁺ and NO₃⁻ have charges of the same size."])]
q22 = [
    stmt("2.2.1", "What benefit does the base of the pan, made from aluminium, have?", 1,
         ["Aluminium is a metal that is a good thermal conductor.", "Aluminium allows heat to pass through it easily."],
         ["Aluminium is a thermal insulator.", "Aluminium stops heat from reaching the food.", "Aluminium does not get hot."],
         ["What property of metals matters when cooking on a stove?", "Does the base need to let heat through or keep it out?"], 1),
    stmt("2.2.2", "Why would the handle of the pan be made of plastic?", 1,
         ["Plastic is a thermal insulator.", "Plastic does not allow heat to pass through it easily."],
         ["Plastic is a good conductor of heat.", "Plastic conducts electricity.", "Plastic melts at a lower temperature than aluminium."],
         ["The handle is held by the cook.", "Should the handle let heat through?"], 1)]

# ---- QUESTION 3, the question paper page 6 and the memo pages 2-3 ----
q3 = [
    stmt("3.1", "Define the term temperature.", 2,
         ["A measure of the average kinetic energy of the particles.", "A measure of how much kinetic energy the particles have on average."],
         ["The total energy of all the particles in a substance.", "The amount of heat a substance contains.",
          "A measure of the potential energy between particles.", "The energy needed to melt a substance."],
         ["Temperature is linked to how fast the particles move.", "Is it the total or the average?"], 2),
    term("3.2", "Name the apparatus labelled X.", ["thermometer", "a thermometer"],
         ["What measures the temperature of the water?", "It stands in the beaker of ice."]),
    stmt("3.3", "Why is it important to continuously stir the melting ice with a glass rod?", 1,
         ["To distribute the heat evenly in the beaker.", "To keep the temperature uniform throughout."],
         ["To make the ice melt at a lower temperature.", "To stop the thermometer from breaking.", "To add energy to the water."],
         ["Is the water near the flame hotter than at the top?", "What would the thermometer read without stirring?"], 1)]
q34 = [
    term("3.4.1", "Name the process taking place between t₁ and t₂.", ["melting", "melt", "fusion"],
         ["The temperature stays at 0 °C.", "Ice is changing to water."]),
    answer("3.4.2", "Will the water particles move SLOWER or FASTER between t₂ and t₃ when compared to the movement of the particles between "
                    "0 and t₁? Give a reason for your answer.", 2,
           ["FASTER: the water is now a liquid, and its particles have more kinetic energy",
            "SLOWER: the water is now a liquid, and its particles are closer together",
            "SLOWER: the particles have less kinetic energy", "FASTER: the particles have more potential energy"],
           ["Between 0 and t₁ the water is ice; between t₂ and t₃ it is liquid.", "Which energy decides how fast particles move?"]),
    mcq("3.4.3", "Will the potential energy between t₃ and t₄ INCREASE, DECREASE or REMAIN THE SAME?", CHANGE, 0,
        ["What is happening to the water between t₃ and t₄?", "During boiling, the particles move further apart."], marks=1),
    mcq("3.4.4", "Can the particles be compressed between t₄ and t₅? Answer YES or NO only.", ["YES", "NO"], 0,
        ["What phase is the water in after t₄?", "Can a gas be compressed?"], marks=1),
    mcq("3.4.5", "The forces between particles of ethanol are weaker than those in water. Will the boiling point for ethanol be GREATER THAN "
        "or LESS THAN 100 °C under the same standard conditions?", ["GREATER THAN", "LESS THAN"], 1,
        ["Weaker forces between particles need less energy to overcome.", "Less energy means a lower temperature."], marks=1)]

# ---- QUESTION 4, the question paper page 7 and the memo page 3 ----
AR = "Aᵣ = {(99,76 × 16) + (0,04 × 17) + (0,2 × 18)}/{100}\n"
q41 = [
    stmt("4.1.1", "Define isotopes.", 2,
         ["Atoms of the same element with the same atomic number but a different mass number, because of a different number of neutrons.",
          "Atoms of the same element with the same number of protons but different numbers of neutrons."],
         ["Atoms of different elements with the same mass number.", "Atoms of the same element with different numbers of protons.",
          "Atoms of the same element with different numbers of electrons.", "Molecules of the same element with different numbers of atoms."],
         ["What is the same, and what differs, in isotopes?", "Which particle in the nucleus changes the mass number only?"], 2),
    work("4.1.2", "What percentage abundance does O-18 occupy?", 2, [
        "% O-18 = 100 − (99,76 + 0,04)\n= 0,2 %",          # the memo
        "% O-18 = 100 − (99,76 − 0,04)\n= 0,28 %",         # the brackets' sign
        "% O-18 = 99,76 + 0,04\n= 99,8 %",                 # the other two added only
        "% O-18 = {100}/{3}\n= 33,33 %"],                  # shared equally
        ["What do all the abundances add up to?", "Subtract the other two from that total."]),
    work("4.1.3", "Calculate the relative atomic mass of oxygen.", 4, [
        AR + "= 16,0044 ≈ 16,00",                                                         # the memo
        "Aᵣ = {16 + 17 + 18}/{3}\n= 17",                                                  # the abundances ignored
        "Aᵣ = {(99,76 × 16) + (0,04 × 17) + (0,2 × 18)}/{3}\n= 533,48",                   # ÷ the number of isotopes
        "Aᵣ = (99,76 × 16) + (0,04 × 17) + (0,2 × 18)\n= 1 600,44"],                      # not ÷ 100
        ["Each isotope's mass counts as much as its abundance.", "The abundances are percentages: divide by 100."], after=["4.1.2"])]
q42 = [
    term("4.2.1", "Name the type of bonding between the aluminium atoms that makes it a good conductor of electricity.",
         ["metallic bonding", "metallic bond", "metallic bonds", "metallic"],
         ["Aluminium is a metal.", "Its valence electrons are delocalised."]),
    stmt("4.2.2", "State AND explain another property of aluminium that can be attributed to the type of bond identified.", 2,
         ["Aluminium is ductile: it can be stretched into a wire.", "Aluminium is malleable: it can be hammered into shape without breaking."],
         ["Aluminium is brittle: it shatters when it is hit.", "Aluminium has a low melting point because its bonds are weak.",
          "Aluminium is a poor conductor of heat.", "Aluminium dissolves easily in water."],
         ["Which properties come from layers of positive ions in a sea of electrons?", "Can the layers slide without the metal breaking?"], 2),
    term("4.2.3", "Aluminium reacts with nitrogen according to the following reaction equation: Aℓ + N₂ → AℓN. Name the product that forms.",
         ["aluminium nitride", "aluminum nitride"], ["A metal and a non-metal: the metal is named first.", "Nitrogen as an ion ends in -ide."],
         marks=2),
    draw("4.2.4", "Use Lewis diagrams to show how the product is formed.", 4, [
        ["Aℓ with three valence electrons", 1], ["N with five valence electrons", 1], ["Aℓ³⁺", 1], ["[N with eight electrons]³⁻", 1]],
        ["How many valence electrons do Aℓ and N have?", "How many electrons does Aℓ give to N?"],
        memo="The memo's diagram: Aℓ with three single dots + N with one pair and three single dots → Aℓ³⁺ and [N with four pairs]³⁻.")]

# ---- QUESTION 5, the question paper page 8 and the memo page 4 ----
q5 = [
    stmt("5.1", "Define ionisation energy.", 2,
         ["The minimum energy per mole needed to remove an electron from an atom in the gaseous phase.",
          "The energy needed per mole to remove an electron from a gaseous atom."],
         ["The energy released when an atom gains an electron.", "The energy needed to break a covalent bond.",
          "The energy needed to remove a proton from an atom.", "The energy needed to melt one mole of a solid."],
         ["Is energy needed or released?", "What is removed, and from what phase?"], 2),
    answer("5.2", "Describe the general trend in the first ionisation energies from sodium to argon.", 1,
           ["They increase from sodium to argon", "They decrease from sodium to argon", "They stay the same from sodium to argon",
            "They increase from sodium to magnesium, then decrease to argon"],
           ["Compare Na at the start with Ar at the end.", "Ignore the small dips at Aℓ and S."]),
    stmt("5.3", "Explain the difference in the first ionisation energies of magnesium and chlorine.", 4,
         ["Chlorine has a greater first ionisation energy than magnesium.",
          "Chlorine and magnesium have the same number of energy levels, but chlorine has more protons.",
          "The chlorine nucleus attracts the valence electrons more strongly than the magnesium nucleus.",
          "More energy is needed to remove a valence electron from chlorine than from magnesium."],
         ["Magnesium has a greater first ionisation energy than chlorine.", "Chlorine has more energy levels than magnesium.",
          "The magnesium nucleus attracts its valence electrons more strongly than the chlorine nucleus."],
         ["Which has the higher value on the graph?", "Both are in period 3: what differs in their nuclei?"], 1),
    stmt("5.4", "How will the SECOND ionisation energy of sodium compare to its FIRST ionisation energy? Choose from GREATER THAN, EQUAL TO "
                "or LESS THAN. Explain your answer.", 4,
         ["GREATER THAN", "The sodium ion has a completely filled outermost energy level, a more stable state.",
          "The second electron to be removed is closer to the nucleus and is attracted more strongly.",
          "So more energy is needed to overcome that attraction."],
         ["LESS THAN", "EQUAL TO", "The second electron is further from the nucleus.", "The sodium ion has more protons than the sodium atom."],
         ["After losing one electron, what does Na⁺'s outer energy level look like?", "Is the next electron closer to the nucleus?"], 1)]

# ---- QUESTION 6, the question paper page 9 and the memo page 5 ----
REACT = "Reactants: 2[207 + 2(14) + 6(16)] = 2(331) = 662 g\n"
PROD = "Products: 2(207 + 16) + 4[14 + 2(16)] + 2(16) = 446 + 184 + 32 = 662 g\n"
q61 = [
    answer("6.1.1", "Iron metal is melted. Explain your answer.", 2,
           ["PHYSICAL: a phase change takes place, and the chemical composition of the metal stays the same",
            "CHEMICAL: a phase change takes place, and the chemical composition of the metal stays the same",
            "CHEMICAL: a new substance forms when the iron melts", "PHYSICAL: the iron reacts with oxygen when it is heated"],
           ["Is melted iron still iron?", "Does a phase change make a new substance?"]),
    mcq("6.1.2", "Grey hair is dyed to a red colour.", ["PHYSICAL", "CHEMICAL"], 0,
        ["Classify the change as the memo does.", "Is the hair itself turned into a new substance?"], marks=1),
    mcq("6.1.3", "A car rusts.", ["PHYSICAL", "CHEMICAL"], 1,
        ["Rust is iron oxide.", "Is a new substance formed?"], marks=1)]
q62 = [
    term("6.2.1", "What type of reaction is shown above?", ["decomposition", "thermal decomposition", "decomposition reaction"],
         ["One reactant breaks into several products.", "Heat drives it."]),
    work("6.2.2", "By use of a calculation prove that the law of conservation of mass is TRUE for this reaction.", 5, [
        REACT + PROD + "Mass of reactants = mass of products",                                                              # the memo
        "Reactants: 2[207 + 14 + 3(16)] = 2(269) = 538 g\n" + PROD + "Mass of reactants ≠ mass of products",              # (NO₃)₂ read as NO₃
        "Reactants: 207 + 2(14) + 6(16) = 331 g\nProducts: (207 + 16) + [14 + 2(16)] + 2(16) = 223 + 46 + 32 = 301 g\n"
        "Mass of reactants ≠ mass of products",                                                                             # the coefficients ignored
        REACT + "Products: 2(207 + 16) + 4[14 + 2(16)] + 16 = 446 + 184 + 16 = 646 g\nMass of reactants ≠ mass of products"],  # O₂ as 16
        ["Multiply each molar mass by its coefficient in the balanced equation.", "Compare the total mass on each side."]),
    work("6.2.3", "When 6,62 g of lead nitrate [Pb(NO₃)₂] is heated, 4,46 g of solid is produced. What is the mass of gas that will be "
         "produced?", 2, [
        "m(gas) = 6,62 − 4,46\n= 2,16 g",        # the memo
        "m(gas) = 6,62 + 4,46\n= 11,08 g",       # added, not subtracted
        "m(gas) = {4,46}/{6,62}\n= 0,67 g",      # a ratio, not a difference
        "m(gas) = 4,46 − 6,62\n= −2,16 g"],      # subtracted the wrong way round
        ["What does the law of conservation of mass say about the total mass?", "The solid and the gas together come from the lead "
                                                                                 "nitrate."])]
q63 = [
    answer("6.3", "Balance the following reaction equation: NH₃(g) + O₂(g) → NO(g) + H₂O(ℓ)", 2,
           ["4NH₃ + 5O₂ → 4NO + 6H₂O", "2NH₃ + 2O₂ → 2NO + 3H₂O", "4NH₃ + 3O₂ → 4NO + 6H₂O", "NH₃ + O₂ → NO + H₂O"],
           ["Balance N and H first, then O.", "Count the oxygen atoms on the right: 4NO + 6H₂O."])]

# ---- QUESTION 7, the question paper page 9 and the memo page 5 ----
NC = "n = {m}/{M} = {5,85}/{58,5} = 0,1 mol\n"
q7 = [
    work("7.1", "Calculate the concentration of a solution prepared by dissolving 5,85 g of sodium chloride in enough water to make a "
         "500 cm³ solution.", 4, [
        NC + "c = {n}/{V}\n= {0,1}/{0,5}\n= 0,2 mol·dm⁻³",                                       # the memo
        NC + "c = {n}/{V}\n= {0,1}/{500}\n= 0,0002 mol·dm⁻³",                                   # cm³ not converted
        "n = {M}/{m} = {58,5}/{5,85} = 10 mol\nc = {n}/{V}\n= {10}/{0,5}\n= 20 mol·dm⁻³",       # n upside down
        NC + "c = nV\n= (0,1)(0,5)\n= 0,05 mol·dm⁻³"],                                          # multiplied, not divided
        ["How many moles is 5,85 g of NaCℓ?", "Concentration is in mol·dm⁻³: what is 500 cm³ in dm³?"]),
    stmt("7.2", "Explain the concept of water of crystallisation and give the formula of a common hydrated salt.", 3,
         ["Water of crystallisation is water that is chemically bonded within the crystal structure of a salt.",
          "The water molecules are part of the crystal lattice of a hydrated salt.", "CuSO₄·5H₂O is a common hydrated salt.",
          "Na₂CO₃·10H₂O is a common hydrated salt."],
         ["Water of crystallisation is water that evaporates from a solution.", "Water of crystallisation is the water a salt dissolves in.",
          "NaCℓ is a common hydrated salt.", "H₂O₂ is a common hydrated salt."],
         ["Where are the water molecules in a hydrated crystal?", "A hydrated salt's formula shows · xH₂O."], 1),
    work("7.3", "A learner heats 5 g of a hydrated salt until all the water of crystallisation has evaporated, leaving 3 g of the anhydrous "
         "salt. Determine the percentage of water of crystallisation in the hydrated salt.", 2, [
        "m(H₂O) = 5 − 3 = 2 g\n% H₂O = {2}/{5} × 100 = 40 %",          # the memo
        "m(H₂O) = 5 − 3 = 2 g\n% H₂O = {2}/{3} × 100 = 66,67 %",       # ÷ the anhydrous salt
        "m(H₂O) = 5 − 3 = 2 g\n% H₂O = {3}/{5} × 100 = 60 %",          # the salt's percentage
        "m(H₂O) = 5 − 3 = 2 g\n% H₂O = {5}/{2} × 100 = 250 %"],        # upside down
        ["How much water was lost?", "Out of which mass is the percentage taken?"])]

# ---- QUESTION 8, the question paper page 10 and the memo page 6 ----
NO = "M(NO) = 14 + 16 = 30 g·mol⁻¹\n"
FU = "N = nN_A = 2(6,02 × 10²³) = 1,204 × 10²⁴ formula units\n"
q8 = [
    stmt("8.1", "Define mole.", 2,
         ["The amount of substance with as many particles as there are atoms in 12 g of carbon-12.",
          "The number of particles of a substance that is the same as there are atoms in 12 g of carbon-12."],
         ["The mass of one atom of carbon-12.", "The number of atoms in 1 g of hydrogen gas.", "The volume of 1 g of any gas at STP.",
          "The mass of a substance in grams."],
         ["The mole is a counting unit.", "Which standard is the mole compared with?"], 2),
    term("8.2", "Give the scientific name of nitric acid.", ["hydrogen nitrate"],
         ["Name it as a compound of hydrogen and the nitrate ion.", "HNO₃."]),
    work("8.3.1", "Calculate the molecular mass of ammonium nitrate.", 2, [
        "M(NH₄NO₃) = 14 + 4(1) + 14 + 3(16)\n= 80 g·mol⁻¹",        # the memo
        "M(NH₄NO₃) = 14 + 4(1) + 3(16)\n= 66 g·mol⁻¹",             # one nitrogen only
        "M(NH₄NO₃) = 14 + 4(1) + 14 + 16\n= 48 g·mol⁻¹",           # one oxygen only
        "M(NH₄NO₃) = 14(4) + 1 + 14 + 16(3)\n= 119 g·mol⁻¹"],      # the 4 on nitrogen
        ["Count the atoms of each element in NH₄NO₃.", "N = 14, H = 1, O = 16."]),
    work("8.3.2", "Calculate the number of moles of ammonium nitrate if 15 g of it was formed.", 3, [
        "n = {m}/{M}\n= {15}/{80}\n= 0,19 mol",        # the memo
        "n = {M}/{m}\n= {80}/{15}\n= 5,33 mol",        # upside down
        "n = mM\n= (15)(80)\n= 1 200 mol",             # multiplied
        "n = {m}/{M}\n= {15}/{66}\n= 0,23 mol"],       # the molar mass with one nitrogen
        ["Which equation links moles, mass and molar mass?", "Use M from 8.3.1."], after=["8.3.1"]),
    work("8.3.3", "Calculate the volume of 12 g of nitrogen oxide at STP.", 5, [
        NO + "n = {m}/{M} = {12}/{30} = 0,4 mol\nV = nV_m\n= (0,4)(22,4)\n= 8,96 dm³",                             # the memo (NO)
        "M(NO₂) = 14 + 2(16) = 46 g·mol⁻¹\nn = {m}/{M} = {12}/{46} = 0,26 mol\nV = nV_m\n= (0,26)(22,4)\n= 5,84 dm³",  # NO₂
        NO + "n = {m}/{M} = {12}/{30} = 0,4 mol\nV = {n}/{V_m}\n= {0,4}/{22,4}\n= 0,02 dm³",                         # ÷ the molar volume
        NO + "n = {M}/{m} = {30}/{12} = 2,5 mol\nV = nV_m\n= (2,5)(22,4)\n= 56 dm³"],                              # n upside down
        ["Which nitrogen oxide is in the equations (NO)?", "At STP, one mole of gas has a volume of 22,4 dm³."]),
    work("8.3.4", "Calculate the number of nitrogen atoms present in 2 moles of ammonium nitrate.", 4, [
        FU + "Each NH₄NO₃ has 2 N atoms\nN atoms = 2(1,204 × 10²⁴)\n= 2,41 × 10²⁴ nitrogen atoms",                      # the memo
        FU + "Each NH₄NO₃ has 1 N atom\nN atoms = 1(1,204 × 10²⁴)\n= 1,20 × 10²⁴ nitrogen atoms",                       # one N per formula unit
        FU + "Each NH₄NO₃ has 9 atoms\nN atoms = 9(1,204 × 10²⁴)\n= 1,08 × 10²⁵ nitrogen atoms",                        # all the atoms
        "N = {n}/{N_A} = {2}/{6,02 × 10²³} = 3,32 × 10⁻²⁴ formula units\nEach NH₄NO₃ has 2 N atoms\n"
        "N atoms = 2(3,32 × 10⁻²⁴)\n= 6,64 × 10⁻²⁴ nitrogen atoms"],                                                     # ÷ Avogadro's number
        ["How many formula units are in 2 mol?", "How many nitrogen atoms are in one NH₄NO₃?"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 14, "items": q1},
    {"id": "2.1", "title": "Question 2.1", "kind": "Classifying matter", "marks": 6,
     "lead": "Use the following substances to answer the questions: A Cobalt, B Gold, C Phosphorus, D Silicon, E Air, F Ammonium nitrate.",
     "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Properties of materials", "marks": 2,
     "lead": "The base of a frying pan is made from aluminium while the handle is made of hard plastic.", "items": q22},
    {"id": "3", "title": "Question 3", "kind": "States of matter", "marks": 4,
     "lead": "Grade 10 learners conducted an experiment to determine the heating curve of water by using ice cubes. The experiment was "
             "set up as shown below.",
     "figure": P.fig("Q3", "A beaker of ice cubes on a tripod over a burner, with a glass rod and an instrument X held in a clamp on a "
                           "retort stand, dipping into the ice."), "items": q3},
    {"id": "3.4", "title": "Question 3.4", "kind": "Heating curve", "marks": 6, "lead": "The graph below shows the results of the experiment.",
     "figure": P.fig("Q3.4", "A heating curve of temperature (°C) against time (minutes): rising from −20 °C to 0 °C at t₁, level at "
                             "0 °C until t₂, rising to 100 °C at t₃, level at 100 °C until t₄, then rising again to t₅."), "items": q34},
    {"id": "4.1", "title": "Question 4.1", "kind": "Isotopes", "marks": 8,
     "lead": "Naturally occurring oxygen consists of three isotopes: O-16, 99,76 %; O-17, 0,04 %; O-18, X %.", "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Chemical bonding", "marks": 9,
     "lead": "Aluminium is a metal and a good conductor of electricity.", "items": q42},
    {"id": "5", "title": "Question 5", "kind": "Periodic trends", "marks": 11,
     "lead": "The graph below shows the first ionisation energies of the elements of period 3 in the periodic table.",
     "figure": P.fig("Q5", "First ionisation energy (kJ·mol⁻¹) of the period 3 elements: Na about 500, Mg about 740, Aℓ about 580, Si "
                           "about 790, P about 1 010, S about 1 000, Cℓ about 1 250, Ar about 1 520."), "items": q5},
    {"id": "6.1", "title": "Question 6.1", "kind": "Physical and chemical change", "marks": 4,
     "lead": "Classify the following as a PHYSICAL or CHEMICAL change.", "items": q61},
    {"id": "6.2", "title": "Question 6.2", "kind": "Conservation of mass", "marks": 8,
     "lead": "The balanced equation for the reaction is: 2Pb(NO₃)₂(s) → 2PbO(s) + 4NO₂(g) + O₂(g)", "items": q62},
    {"id": "6.3", "title": "Question 6.3", "kind": "Balancing equations", "marks": 2, "items": q63},
    {"id": "7", "title": "Question 7", "kind": "Concentration and hydrated salts", "marks": 9, "items": q7},
    {"id": "8", "title": "Question 8", "kind": "The mole", "marks": 17,
     "lead": "There are several steps in the production of fertilisers. In the third step, nitrogen dioxide is absorbed by water to "
             "produce nitric acid. Nitric acid and ammonia can react together in an acid-base process to form the salt, ammonium nitrate, "
             "which is soluble in water.\n3NO₂(g) + H₂O(ℓ) → 2HNO₃(aq) + NO(g)\nNH₃(ℓ) + HNO₃(ℓ) → NH₄NO₃(s)", "items": q8}]

P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P2 (Chemistry)", "sitting": "November 2024", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "4.2.4", "kind": "no_fit", "detail": "The Lewis diagrams play as pick the drawing: the memo's (Aℓ³⁺ and [N]³⁻ with eight "
                                                     "electrons) and three mistakes."},
          {"n": "5.3", "kind": "memo_issue", "detail": "The memo's last point reads 'More energy is needed in magnesium than in chlorine'; "
                                                       "its own first point (chlorine's first ionisation energy is greater) and the graph "
                                                       "say the opposite. The card says more energy is needed for chlorine."},
          {"n": "6.2.2", "kind": "memo_issue", "detail": "The memo's first line writes 2[207 + 2(14) + 3(16)]; Pb(NO₃)₂ has six oxygens and "
                                                         "its own next line uses 2(207 + 124) = 662. The right option writes 6(16)."},
          {"n": "6.1.2", "kind": "low_confidence", "detail": "The memo classifies dyeing grey hair red as PHYSICAL; permanent hair dyes "
                                                             "react chemically with the hair. The right option follows the memo."}],
         {"1": 14, "2": 8, "3": 10, "4": 17, "5": 11, "6": 14, "7": 9, "8": 17}, 100,
         {"4.1.3": ["4.1.2"], "8.3.2": ["8.3.1"]},
         "Questions 1 to 8 (the whole paper)")
