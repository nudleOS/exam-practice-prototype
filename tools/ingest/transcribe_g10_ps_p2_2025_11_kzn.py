"""Grade 10 Physical Sciences P2 (Chemistry) November 2025 (KwaZulu-Natal Department of Education), the whole paper (Questions 1 to 7,
100 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and the
memo's working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): re-published by
Stanmore Secondary (stanmorephysics.com) as one scanned PDF, the question paper (pages 1-12, with the data sheets) then the marking
memorandum (pages 13-18), no text layer: read from its page images (100 dpi). Split into '<id> QP.pdf' and '<id> MG.pdf'.

  python tools/ingest/transcribe_g10_ps_p2_2025_11_kzn.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ps-p2-2025-11-kzn/g10-ps-p2-2025-11-kzn QP.pdf" "uploads/provincial/g10-ps-p2-2025-11-kzn/g10-ps-p2-2025-11-kzn MG.pdf" --id g10-ps-p2-2025-11-kzn --from-json

The Grade 12 rulings, as in transcribe_g10_ps_p2_2024_11_nw.py: multiple choice printed in the paper as printed; a choice printed in the
stem an MCQ of the printed choices; every calculation an authored working (provincial.py); a definition or explanation statements; the
Lewis diagram (4.2.2) pick the drawing (pictures_lower.py: ion_row); the Aufbau diagram (4.2.3) an MCQ of four box diagrams written out.
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ps-p2-2025-11-kzn", 595.44, 841.68, {"3.1": [6, 61, 626, 486, 767], "3.2": [7, 115, 288, 461, 608]}, start=6)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term
CHANGE = ["INCREASE", "DECREASE", "REMAIN THE SAME"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-4 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which one of the following is an example of a pure substance?", ["Carbon dioxide", "Air", "Steel", "Aqueous sodium chloride"], 0,
        ["A pure substance is one element or one compound.", "Air, steel and salt water are mixtures."]),
    mcq("1.2", "Which one of the following has the highest first ionisation energy?", ["Li", "F", "Na", "Cl"], 1,
        ["Ionisation energy increases across a period.", "And decreases down a group."]),
    mcq("1.3", "Which of the following is true for the process of condensation?", ["The substance is heated and changes phase to gas.",
        "The substance is heated and changes phase to liquid.", "The substance is cooled and changes phase to gas.",
        "The substance is cooled and changes phase to liquid."], 3, ["Condensation is gas to liquid.", "Is heat added or removed?"]),
    mcq("1.4", "Which one of the following contains 6,02 × 10²³ ATOMS?", ["10 g of Ne", "28 g of N₂ gas", "4,48 dm³ of CH₄ gas at STP",
        "22,4 dm³ of NH₃ gas at STP"], 2, ["One mole of atoms.", "4,48 dm³ is 0,2 mol, and each CH₄ has 5 atoms."]),
    mcq("1.5", "Consider the balanced chemical equation CH₄(l) + H₂O(g) → CO(g) + 3H₂(g). The number of CH₄ molecules required to form "
        "22,4 dm³ of H₂ at STP is …", ["6,02 × 10²³", "½ × 6,02 × 10²³", "⅓ × 6,02 × 10²³", "¼ × 6,02 × 10²³"], 2,
        ["22,4 dm³ of H₂ at STP is 1 mol.", "CH₄ : H₂ = 1 : 3."])]

# ---- QUESTION 2, the question paper pages 5-6 and the memo page 2 ----
NM = "M(NH₄NO₃) = 14 × 2 + 1 × 4 + 16 × 3 = 80 g·mol⁻¹\n"
q21 = [
    mcq("2.1.1", "Would you classify the contents of the container, after the reaction, as a MIXTURE or a PURE SUBSTANCE?",
        ["MIXTURE", "PURE SUBSTANCE"], 0, ["The container holds XY and unreacted Y₂.", "Two substances together."], marks=1),
    mcq("2.1.2(a)", "At which temperature will both gases be in their liquid phase? Choose from: 20 °C, −70 °C, −190 °C.", ["20 °C", "−70 °C",
        "−190 °C"], 2, ["Both must be below their boiling points.", "Y₂ boils at −180 °C."], marks=1),
    mcq("2.1.2(b)", "Which of the two substances, Y₂ or XY, will more easily be converted to gas when the temperature is increased in STEP 2?",
        ["Y₂", "XY"], 0, ["Which has the lower boiling point?", "−180 °C or −50 °C?"], marks=1),
    answer("2.1.2(c)", "Does STEP 2 represent a PHYSICAL or CHEMICAL change? Explain the answer.", 2,
           ["PHYSICAL: no new substance is formed", "CHEMICAL: no new substance is formed", "CHEMICAL: a new substance is formed",
            "PHYSICAL: a new substance is formed"], ["Boiling changes only the phase.", "Is anything new made?"]),
    stmt("2.1.2(d)", "The substance that is more easily converted to gas is collected. It is observed that the collected gas is not 100% pure. "
                     "Give a reason for the observation.", 2,
         ["Some of the XY evaporates below its boiling point.", "Some XY particles have enough energy to escape as gas before −50 °C."],
         ["Y₂ reacts with XY in the container.", "The XY freezes and mixes with the Y₂.", "Heating creates new substances.",
          "The container leaks air in."],
         ["Evaporation happens below the boiling point.", "Can some XY become gas at −60 °C?"], 2)]
q22 = [
    answer("2.2.1", "Ammonia reacts with sulphuric acid (hydrogen sulphate) to form ammonium sulphate. Write a balanced chemical equation for the "
                    "above reaction.", 3,
           ["2NH₃ + H₂SO₄ → (NH₄)₂SO₄", "NH₃ + H₂SO₄ → NH₄SO₄", "2NH₃ + H₂SO₄ → 2NH₄SO₄", "NH₃ + H₂SO₄ → (NH₄)₂SO₄"],
           ["Ammonium sulphate is (NH₄)₂SO₄.", "How many NH₃ give two NH₄⁺?"]),
    mcq("2.2.2", "Is the above reaction an example of a SYNTHESIS or DECOMPOSITION reaction?", ["SYNTHESIS", "DECOMPOSITION"], 0,
        ["Two reactants make one product.", "Synthesis builds up."], marks=1),
    work("2.3.1", "Calculate the percentage nitrogen (N) in ammonium nitrate (NH₄NO₃).", 3, [
        "% N = {14 × 2}/{14 × 2 + 1 × 4 + 16 × 3} × 100\n= 35%",       # the memo
        "% N = {14}/{14 × 2 + 1 × 4 + 16 × 3} × 100\n= 17,5%",          # one N only
        "% N = {14 × 2}/{14 + 1 × 4 + 16 × 3} × 100\n= 42,42%",         # one N in the molar mass
        "% N = {14 × 2}/{14 × 2 + 1 × 4 + 16} × 100\n= 58,33%"],        # one O only
        ["How many N atoms are in NH₄NO₃?", "Divide by the molar mass, 80 g·mol⁻¹."]),
    work("2.3.2", "A farmer chooses to use ammonium nitrate as a fertiliser. He needs to supply 30 kg of NITROGEN to a field. Determine the mass of "
         "ammonium nitrate required.", 3, [
        "m(NH₄NO₃) = 30 ÷ 0,35\n= 85,71 kg",      # the memo
        "m(NH₄NO₃) = 30 × 0,35\n= 10,5 kg",       # multiplied
        "m(NH₄NO₃) = 30 ÷ 35\n= 0,86 kg",         # the percentage not converted
        "m(NH₄NO₃) = 30 ÷ 0,175\n= 171,43 kg"],   # one N's percentage
        ["Only 35% of the fertiliser is nitrogen.", "Which mass contains 30 kg of N?"], after=["2.3.1"]),
    work("2.4", "Use the balanced chemical equation 4NH₃ + 5O₂ → 4NO + 6H₂O to prove the law of conservation of mass.", 3, [
        "Mass of reactants = 4[14 + 1 × 3] + 5[16 × 2] = 228 g\nMass of products = 4[14 + 16] + 6[1 × 2 + 16] = 228 g\n"
        "Mass of reactants = mass of products: mass is conserved",                                                     # the memo
        "Mass of reactants = [14 + 1 × 3] + [16 × 2] = 49 g\nMass of products = [14 + 16] + [1 × 2 + 16] = 48 g\n"
        "Mass of reactants ≠ mass of products",                                                                       # the coefficients ignored
        "Mass of reactants = 4[14 + 1 × 3] + 5[16] = 148 g\nMass of products = 4[14 + 16] + 6[1 × 2 + 16] = 228 g\n"
        "Mass of reactants ≠ mass of products",                                                                       # O₂ as O
        "Mass of reactants = 4[14 + 1 × 3] + 5[16 × 2] = 228 g\nMass of products = 4[14 + 16] + 6[1 + 16] = 222 g\n"
        "Mass of reactants ≠ mass of products"],                                                                      # H₂O with one H
        ["Multiply each molar mass by its coefficient.", "Compare the totals."])]

# ---- QUESTION 3, the question paper pages 6-7 and the memo page 3 ----
q31 = [
    stmt("3.1.1", "Define the term diffusion in words.", 2,
         ["The movement of atoms or molecules from an area of higher concentration to an area of lower concentration.",
          "The spreading of particles from where they are more concentrated to where they are less concentrated."],
         ["The movement of particles from low to high concentration.", "The change from a gas to a liquid.",
          "The mixing of two liquids by stirring.", "The movement of water through a membrane only."],
         ["Which way do particles spread?", "High to low."], 2),
    stmt("3.1.2", "Provide a reason why the white ring formed closer to HCl than NH₃.", 1,
         ["Ammonia diffuses faster than hydrochloric acid.", "NH₃ molecules are lighter, so they move faster."],
         ["HCl diffuses faster than NH₃.", "HCl was released first.", "The tube is wider at the HCl end."],
         ["Which gas travelled further in the same time?", "Lighter molecules move faster."], 1),
    stmt("3.1.3", "The temperature of the gases in the glass tube is now increased. How would this affect the TIME taken for the white ring to "
                  "appear? Choose from INCREASE, DECREASE or REMAIN THE SAME. Explain the answer using the kinetic molecular theory.", 3,
         ["DECREASE", "At a higher temperature the particles move faster (have more kinetic energy).", "Therefore the gases diffuse faster."],
         ["INCREASE", "REMAIN THE SAME", "At a higher temperature the particles move slower."],
         ["What does heating do to the particles' kinetic energy?", "Faster particles meet sooner."], 1, after=["3.1.2"])]
q32 = [
    stmt("3.2.1", "Define the term boiling point in words.", 2,
         ["The temperature of a liquid at which its vapour pressure equals the external (atmospheric) pressure.",
          "The temperature at which a liquid's vapour pressure equals atmospheric pressure."],
         ["The temperature at which a solid becomes a liquid.", "The temperature at which a gas becomes a liquid.",
          "The highest temperature a liquid can reach.", "The temperature at which evaporation starts."],
         ["It is about vapour pressure.", "Compared with which pressure?"], 2),
    answer("3.2.2", "Write down the boiling point of hydrochloric acid.", 1, ["−85,1 °C", "−114,2 °C", "0 °C", "100 °C"],
           ["The boiling point is the higher flat part.", "Read the temperature axis there."]),
    mcq("3.2.3", "At which point, A or B, are the forces between HCl particles stronger?", ["A", "B"], 0,
        ["A is in the solid phase.", "Particles are closest in a solid."], marks=1),
    stmt("3.2.4", "Refer to the temperature, energy and movement of particles to explain the changes that take place between t₂ and t₃.", 3,
         ["The temperature of the HCl increases.", "The average kinetic energy of the particles increases.", "The particles move faster."],
         ["The temperature stays the same.", "The particles slow down.", "The potential energy decreases while the substance melts."],
         ["Between t₂ and t₃ the graph slopes up.", "Temperature measures average kinetic energy."], 1)]

# ---- QUESTION 4, the question paper page 8 and the memo pages 3-4 ----
SI = "Let % Si-29 = X; then % Si-30 = 7,8 − X\n"
q41 = [
    stmt("4.1.1", "Define the term isotope in words.", 2,
         ["Atoms of the same element with the same number of protons but a different number of neutrons.",
          "Atoms with the same atomic number but different mass numbers."],
         ["Atoms of different elements with the same mass number.", "Atoms of the same element with different numbers of protons.",
          "Atoms with different numbers of electrons.", "Ions of the same element."],
         ["What is the same, and what differs?", "Neutrons change the mass number."], 2),
    work("4.1.2", "Determine the percentage abundance of Si-29.", 5, [
        SI + "28,1 = 28 × {92,2}/{100} + 29 × {X}/{100} + 30 × {7,8 − X}/{100}\n28,1 = 28,156 − 0,01X\nX = 5,6%",          # the memo
        SI + "28,1 = 28 × {92,2}/{100} + 29 × {X}/{100} + 30 × {X}/{100}\n28,1 = 25,816 + 0,59X\nX = 3,87%",               # Si-30 also X
        "Let % Si-29 = X; then % Si-30 = X\n2X = 100 − 92,2 = 7,8\nThe rest shared equally\nX = {7,8}/{2} = 3,9%",             # shared equally
        SI + "28,1 = 28 × 92,2 + 29X + 30(7,8 − X)\n28,1 = 2 815,6 − X\nX = 2 787,5%"],                                         # not ÷ 100
        ["The three abundances add up to 100%.", "Relative atomic mass = Σ(mass × fraction)."]),
    answer("4.1.3", "Fill in the table for the most abundant isotope of silicon (Si-28): number of protons (a), number of neutrons (b), number of "
                    "valence electrons (c).", 3, ["(a) 14 ; (b) 14 ; (c) 4", "(a) 14 ; (b) 28 ; (c) 4", "(a) 28 ; (b) 14 ; (c) 14",
                                                  "(a) 14 ; (b) 14 ; (c) 2"],
           ["Silicon's atomic number is 14.", "Neutrons = 28 − 14; silicon is in group 14."])]
q42 = [
    term("4.2.1", "Identify the type of bond that forms when magnesium and chlorine combine.", ["ionic", "ionic bond", "ionic bonds", "ionic bonding"],
         ["A metal and a non-metal.", "Electrons are transferred."]),
    draw("4.2.2", "Draw the Lewis dot diagram for magnesium chloride.", 2, [["[Cl]⁻ Mg²⁺ [Cl]⁻, each Cl with eight electrons", 2]],
         ["Mg gives one electron to each of two Cl atoms.", "Show the brackets and charges."],
         memo="The memo's diagram: [Cl with eight electrons]⁻ Mg²⁺ [Cl with eight electrons]⁻, or Mg²⁺ 2[Cl]⁻."),
    answer("4.2.3", "Draw the Aufbau diagram for the magnesium ion (Mg²⁺).", 2,
           ["1s: ↑↓ ; 2s: ↑↓ ; 2p: ↑↓ ↑↓ ↑↓", "1s: ↑↓ ; 2s: ↑↓ ; 2p: ↑↓ ↑↓ ↑↓ ; 3s: ↑↓", "1s: ↑↓ ; 2s: ↑↓ ; 2p: ↑↓ ↑↓ ↑",
            "1s: ↑↑ ; 2s: ↑↑ ; 2p: ↑↑ ↑↑ ↑↑"],
           ["Mg has 12 electrons; Mg²⁺ has lost two.", "Each box holds two electrons of opposite spin."]),
    term("4.2.4", "Write down the name of the noble gas that has the same electronic configuration as the chloride ion.", ["argon"],
         ["Cl⁻ has 18 electrons.", "The next noble gas after chlorine."]),
    stmt("4.3", "How does the atomic radius of chlorine (Cl) compare to magnesium (Mg)? Choose from GREATER THAN, LESS THAN or EQUAL TO. Explain "
                "your answer by referring to the atomic structure.", 4,
         ["LESS THAN", "Chlorine and magnesium are in the same period (the same number of energy levels).",
          "The effective nuclear charge of chlorine is higher than magnesium's.",
          "The attraction between the nucleus and the outer electrons is stronger in chlorine."],
         ["GREATER THAN", "EQUAL TO", "Chlorine has more energy levels than magnesium."],
         ["Atomic radius decreases across a period.", "Why: more protons, same shells."], 1)]

# ---- QUESTION 5, the question paper page 9 and the memo pages 4-5 ----
NMG = "n(Mg₃N₂) = 0,1 mol\n"
q5 = [
    stmt("5.1", "Define the term concentration in words.", 2,
         ["The number of moles of solute per cubic decimetre of solution.", "The amount of solute (in mol) in 1 dm³ of solution."],
         ["The mass of solvent in a solution.", "The number of moles of solvent per litre.", "The volume of a solution.",
          "The mass of solute per mole."],
         ["c = n/V.", "Moles per volume."], 2),
    work("5.2", "Calculate the number of moles of Mg₃N₂ that reacted.", 3, [
        "n = {m}/{M}\n= {10}/{24 × 3 + 14 × 2}\n= 0,1 mol",      # the memo
        "n = {M}/{m}\n= {24 × 3 + 14 × 2}/{10}\n= 10 mol",       # upside down
        "n = {m}/{M}\n= {10}/{24 + 14}\n= 0,26 mol",             # one Mg and one N
        "n = m × M\n= 10 × (24 × 3 + 14 × 2)\n= 1 000 mol"],    # multiplied
        ["n = m/M.", "M(Mg₃N₂) = 3(24) + 2(14)."]),
    work("5.3.1", "Determine the concentration of HCl.", 4, [
        NMG + "Mg₃N₂ : HCl = 1 : 6, so n(HCl) = 0,6 mol\nc = {n}/{V}\n= {0,6}/{1,2} = 0,5 mol·dm⁻³",       # the memo
        NMG + "Mg₃N₂ : HCl = 1 : 1, so n(HCl) = 0,1 mol\nc = {n}/{V}\n= {0,1}/{1,2} = 0,08 mol·dm⁻³",      # the ratio ignored
        NMG + "Mg₃N₂ : HCl = 1 : 6, so n(HCl) = 0,6 mol\nc = nV\n= 0,6 × 1,2 = 0,72 mol·dm⁻³",             # multiplied
        NMG + "Mg₃N₂ : HCl = 6 : 1, so n(HCl) = 0,017 mol\nc = {n}/{V}\n= {0,017}/{1,2} = 0,01 mol·dm⁻³"],  # the ratio upside down
        ["Use the mole ratio from the balanced equation.", "c = n/V."], after=["5.2"]),
    work("5.3.2", "Determine the volume of NH₃ gas (in dm³) that formed at STP.", 4, [
        NMG + "Mg₃N₂ : NH₃ = 1 : 2, so n(NH₃) = 0,2 mol\nV = nVm\n= 0,2 × 22,4 = 4,48 dm³",      # the memo
        NMG + "Mg₃N₂ : NH₃ = 1 : 1, so n(NH₃) = 0,1 mol\nV = nVm\n= 0,1 × 22,4 = 2,24 dm³",      # the ratio ignored
        NMG + "Mg₃N₂ : NH₃ = 1 : 2, so n(NH₃) = 0,2 mol\nV = {n}/{Vm}\n= {0,2}/{22,4} = 0,009 dm³",   # divided
        NMG + "Mg₃N₂ : NH₃ = 2 : 1, so n(NH₃) = 0,05 mol\nV = nVm\n= 0,05 × 22,4 = 1,12 dm³"],   # the ratio upside down
        ["Mg₃N₂ : NH₃ from the equation.", "At STP, 1 mol of gas is 22,4 dm³."], after=["5.2"]),
    work("5.3.3", "Determine the number of chloride ions (Cl⁻) present in the MgCl₂ produced.", 5, [
        NMG + "Mg₃N₂ : MgCl₂ = 1 : 3, so n(MgCl₂) = 0,3 mol\nN(MgCl₂) = 0,3 × 6,02 × 10²³ = 1,806 × 10²³\nN(Cl⁻) = 2 × 1,806 × 10²³\n"
              "= 3,612 × 10²³ ions",                                                                                                   # the memo
        NMG + "Mg₃N₂ : MgCl₂ = 1 : 3, so n(MgCl₂) = 0,3 mol\nN(MgCl₂) = 0,3 × 6,02 × 10²³ = 1,806 × 10²³\nN(Cl⁻) = 1,806 × 10²³\n"
              "= 1,806 × 10²³ ions",                                                                                                   # one Cl⁻ per MgCl₂
        NMG + "Mg₃N₂ : MgCl₂ = 1 : 1, so n(MgCl₂) = 0,1 mol\nN(MgCl₂) = 0,1 × 6,02 × 10²³ = 6,02 × 10²²\nN(Cl⁻) = 2 × 6,02 × 10²²\n"
              "= 1,204 × 10²³ ions",                                                                                                   # the ratio ignored
        NMG + "Mg₃N₂ : MgCl₂ = 1 : 3, so n(MgCl₂) = 0,3 mol\nN(MgCl₂) = {0,3}/{6,02 × 10²³} = 4,98 × 10⁻²⁵\nN(Cl⁻) = 2 × 4,98 × 10⁻²⁵\n"
              "= 9,97 × 10⁻²⁵ ions"],                                                                                                  # ÷ Avogadro's number
        ["How many mol of MgCl₂ form?", "Each MgCl₂ has two Cl⁻ ions."], after=["5.2"])]

# ---- QUESTION 6, the question paper page 9 and the memo pages 5-6 ----
MOLES = "n(Mg) = {27,7}/{24} = 1,15 ; n(P) = {23,6}/{31} = 0,76 ; n(O) = {48,7}/{16} = 3,04\n"
q6 = [
    work("6.1", "Analysis of a compound made up of magnesium (Mg), phosphorus (P) and oxygen (O) only provided the following percentage "
         "composition by mass: magnesium 27,7%; phosphorus 23,6%; oxygen 48,7%. Determine the empirical formula of this compound.", 6, [
        MOLES + "Ratio ÷ 0,76: 1,51 : 1 : 4\n× 2: 3 : 2 : 8\nEmpirical formula: Mg₃P₂O₈",      # the memo
        MOLES + "Ratio ÷ 0,76: 1,51 : 1 : 4\nRounded: 2 : 1 : 4\nEmpirical formula: Mg₂PO₄",    # 1,51 rounded to 2
        "n(Mg) = {27,7}/{12} = 2,31 ; n(P) = {23,6}/{15} = 1,57 ; n(O) = {48,7}/{8} = 6,09\nRatio ÷ 1,57: 1,47 : 1 : 3,88\n× 2: 3 : 2 : 8\n"
        "Empirical formula: Mg₃P₂O₈ (with the atomic numbers)",                                  # atomic numbers for molar masses
        "Ratio of percentages: 27,7 : 23,6 : 48,7\n÷ 23,6: 1,17 : 1 : 2,06\nRounded: 1 : 1 : 2\nEmpirical formula: MgPO₂"],   # percentages not converted to moles
        ["Assume 100 g: the percentages become grams.", "Convert to moles, divide by the smallest, and make whole numbers."]),
    work("6.2", "Determine the mass of hydrated potassium sulphate (K₂SO₄·7H₂O) needed to prepare 100 ml of a 0,2 mol·dm⁻³ potassium sulphate "
         "solution.", 4, [
        "M(K₂SO₄·7H₂O) = 39 × 2 + 32 + 16 × 4 + 7 × 18 = 300 g·mol⁻¹\nc = {m}/{MV}\n0,2 = {m}/{300(0,1)}\nm = 6 g",        # the memo
        "M(K₂SO₄) = 39 × 2 + 32 + 16 × 4 = 174 g·mol⁻¹\nc = {m}/{MV}\n0,2 = {m}/{174(0,1)}\nm = 3,48 g",                  # the water left out
        "M(K₂SO₄·7H₂O) = 39 × 2 + 32 + 16 × 4 + 7 × 18 = 300 g·mol⁻¹\nc = {m}/{MV}\n0,2 = {m}/{300(100)}\nm = 6 000 g",   # ml not converted
        "M(K₂SO₄·7H₂O) = 39 + 32 + 16 × 4 + 7 × 18 = 261 g·mol⁻¹\nc = {m}/{MV}\n0,2 = {m}/{261(0,1)}\nm = 5,22 g"],       # one K
        ["Include the water of crystallisation in M.", "100 ml = 0,1 dm³."])]

# ---- QUESTION 7, the question paper page 10 and the memo page 6 ----
q7 = [
    work("7.1", "Determine the theoretical mass of copper (Cu) formed.", 3, [
        "% yield = {actual yield}/{theoretical yield} × 100\n85 = {15}/{theoretical yield} × 100\nm(Cu)theoretical = 17,65 g",   # the memo
        "% yield = {actual yield}/{theoretical yield} × 100\n85 = {theoretical yield}/{15} × 100\nm(Cu)theoretical = 12,75 g",   # upside down
        "% yield = {actual yield}/{theoretical yield} × 100\n85 = {5}/{theoretical yield} × 100\nm(Cu)theoretical = 5,88 g",     # Y's mass
        "% yield = {actual yield}/{theoretical yield} × 100\n15 = {85}/{theoretical yield} × 100\nm(Cu)theoretical = 566,67 g"],  # swapped
        ["15 g is the actual yield.", "Theoretical = actual ÷ 0,85."]),
    work("7.2", "Use relevant calculations to determine the NAME of metal Y.", 6, [
        "n(Cu) = {17,65}/{63,5} = 0,278 mol\nY : Cu = 2 : 3, so n(Y) = 0,185 mol\nM(Y) = {5}/{0,185} = 27,03 g·mol⁻¹\nY is aluminium",    # the memo
        "n(Cu) = {17,65}/{63,5} = 0,278 mol\nY : Cu = 3 : 2, so n(Y) = 0,417 mol\nM(Y) = {5}/{0,417} = 11,99 g·mol⁻¹\nY is carbon",       # the ratio upside down
        "n(Cu) = {15}/{63,5} = 0,236 mol\nY : Cu = 2 : 3, so n(Y) = 0,157 mol\nM(Y) = {5}/{0,157} = 31,8 g·mol⁻¹\nY is phosphorus",      # the actual yield
        "n(Cu) = {17,65}/{63,5} = 0,278 mol\nY : Cu = 1 : 1, so n(Y) = 0,278 mol\nM(Y) = {5}/{0,278} = 17,99 g·mol⁻¹\nY is fluorine"],   # the ratio ignored
        ["Use the theoretical mass of Cu.", "Y : Cu = 2 : 3; then M = m/n."], after=["7.1"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 10, "items": q1},
    {"id": "2.1", "title": "Question 2.1", "kind": "Classifying and separating matter", "marks": 7,
     "lead": "Two hypothetical gases, X₂ and Y₂, react in a closed container to form XY gas according to the equation X₂(g) + Y₂(g) → 2XY(g). "
             "After the reaction, the container is found to contain both XY gas and some unreacted Y₂ gas.\nTo separate XY from Y₂: STEP 1, the "
             "contents of the container are cooled to liquefy BOTH gases; STEP 2, the liquid is thereafter gradually heated to a maximum "
             "temperature of −60 °C. Boiling points: Y₂ −180 °C; XY −50 °C.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Reactions and calculations", "marks": 13,
     "lead": "Ammonium sulphate is one of the most common fertilisers used worldwide.", "items": q22},
    {"id": "3.1", "title": "Question 3.1", "kind": "Diffusion", "marks": 6,
     "lead": "A teacher performs a demonstration using ammonia (NH₃) and hydrochloric acid (HCl) GASES in a long glass tube. Ammonia and hydrochloric "
             "acid are simultaneously released from opposite ends of a long glass tube. A white ring of ammonium chloride (NH₄Cl) forms where the "
             "gases react. The position of the white ring formed is shown on the diagram below.",
     "figure": P.fig("3.1", "A long glass tube with NH₃ entering at the left end and HCl at the right; the white ring forms to the right of the "
                            "middle of the tube, closer to the HCl end."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Heating curve", "marks": 7,
     "lead": "The heating curve of hydrochloric acid (HCl) is represented by the graph below. The graph is not drawn to scale.",
     "figure": P.fig("3.2", "The heating curve of hydrochloric acid: temperature rises through A to −114,2 °C at t₁, stays level until t₂, rises "
                            "through B to −85,1 °C at t₃, stays level until t₄, then rises again."), "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Isotopes", "marks": 10,
     "lead": "Silicon occurs naturally as three stable isotopes: Si-28, Si-29 and Si-30. The percentage abundance of Si-28 is 92,2% and the relative "
             "atomic mass of silicon is 28,1.", "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Bonding and the periodic table", "marks": 10,
     "lead": "Magnesium combines with chlorine to form magnesium chloride.", "items": q42},
    {"id": "5", "title": "Question 5", "kind": "Stoichiometry", "marks": 18,
     "lead": "Magnesium nitride (Mg₃N₂) reacts with hydrochloric acid (HCl) according to the balanced equation:\nMg₃N₂(s) + 6HCl(aq) → 3MgCl₂(aq) + "
             "2NH₃(g)\nIn one such reaction a learner completely reacts 10 g magnesium nitride (Mg₃N₂) with 1,2 dm³ hydrochloric acid (HCl) at "
             "standard temperature and pressure (STP).", "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Empirical formula and solutions", "marks": 10, "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Percentage yield", "marks": 9,
     "lead": "A metal Y reacts with copper(II) oxide (CuO) according to the balanced equation 2Y + 3CuO → Y₂O₃ + 3Cu. A 5 g sample of Y reacts with "
             "excess copper(II) oxide to produce 15 g of copper (Cu). The percentage yield of copper in this reaction is 85%.", "items": q7}]

P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P2 (Chemistry)", "sitting": "November 2025", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "4.2.2", "kind": "no_fit", "detail": "The Lewis diagram of magnesium chloride (4.2.2) plays as pick the drawing; the Aufbau diagram "
                                                     "(4.2.3) as four box diagrams written out (1s: ↑↓ ; …)."},
          {"n": "5.3.2", "kind": "low_confidence", "detail": "The memo's last line writes V(H₂) = 4,48 dm³; the gas is NH₃ (the value is right)."}],
         {"1": 10, "2": 20, "3": 13, "4": 20, "5": 18, "6": 10, "7": 9}, 100,
         {"2.3.2": ["2.3.1"], "3.1.3": ["3.1.2"], "5.3.1": ["5.2"], "5.3.2": ["5.2"], "5.3.3": ["5.2"], "7.2": ["7.1"]},
         "Questions 1 to 7 (the whole paper)")
