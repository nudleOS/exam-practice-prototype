"""Grade 11 Life Sciences P1 November 2024 (Eastern Cape Department of Education), Questions 1 to 3 (145 of the paper's 150 marks,
2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and answers are
the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za,
2024_November_Gr_11_Exams, the question paper zip (English PDF, 14 pages, text layer) and the memo zip, whose FINAL AMENDED English
memo (13 pages) is the one used: it supersedes the first memo and removes 3.3.6 ('Microscopic structure not in CAPS. Mark out of 145
and convert to 150'), so the paper plays 145.

  python tools/ingest/transcribe_g11_ls_p1_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ls-p1-2024-11-ec/LIFE SCIENCES P1 GR11 QP NOV2024 ENG D_watermark.pdf" "uploads/provincial/g11-ls-p1-2024-11-ec/FINAL AMENDED LIFE SCIENCES P1 GR11 MEMO NOV2024_English_watermark.pdf" --id g11-ls-p1-2024-11-ec --from-json

The Life Sciences rulings, as in transcribe_ls_p1_2024_11.py: printed multiple choice as printed; terms typed; Column I / Column II as
A only / B only / both / none; LETTER and NAME as lettername; a written answer as statements to pick (the memo's points and clearly
wrong ones, one mark a tick); the one typed calculation (2.3.3) as four workings; the graph to draw (2.1.1) as pick the drawing
(pictures_lower.py: bars). Figure boxes are in PDF points (text blocks and image rects), 1% inside their neighbours."""
from provincial import Paper

P = Paper("g11-ls-p1-2024-11-ec", 595.22, 842.0, {
    "1.1": [3, 77.0, 214.0, 518.0, 420.0], "1.1.9": [5, 119.7, 102.8, 511.0, 265.7], "1.4": [6, 80.0, 316.0, 518.0, 474.0],
    "1.5": [7, 81.0, 89.0, 513.0, 299.0], "2.1": [8, 97.0, 231.0, 491.0, 427.0], "2.3": [10, 80.0, 62.0, 511.0, 407.0],
    "2.5": [11, 83.3, 146.0, 508.0, 425.9], "3.1": [12, 77.4, 116.6, 518.2, 428.1], "3.3": [13, 78.0, 403.0, 518.0, 678.0],
    "3.4": [14, 80.0, 237.0, 511.0, 511.0]}, start=2)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
ln = lambda n, q, letters, letter, names, clues, **kw: {"t": "lettername", "n": n, "marks": 2, "q": q, "clues": clues, "letters": letters,
                                                       "a": {"letter": letter, "name": names}, **kw}

# ---- SECTION A, QUESTION 1, the question paper pages 3-7 and the memo pages 4-5 ----
q11 = [
    mcq("1.1.1", "The above skull is that of a …", ["omnivore because of large canines and flat molars.", "carnivore because of reduced molar "
        "number.", "omnivore because of canines, incisors and molars are present.", "carnivore because of large canines and sharp molars."], 3,
        ["Look at the size of the canines.", "Are the back teeth flat or pointed?"]),
    mcq("1.1.2", "A function of the incisors of such an animal would be to:", ["Grind and crush food", "Catch and hold onto prey",
        "Bite and cut food", "Kill prey and tear-off flesh"], 2, ["Incisors are the front teeth.", "Canines catch and kill; incisors …"]),
    mcq("1.1.3", "Which ONE of the options listed below CORRECTLY summarises the waste product for each of the excretory organs?",
        ["Lungs CO₂ · Skin water · Liver urine · Kidney bile", "Lungs CO₂ · Skin water · Liver urea · Kidney urine",
         "Lungs water vapour · Skin bile · Liver water · Kidney salts", "Lungs urea · Skin water · Liver bile · Kidney CO₂"], 1,
        ["The liver makes urea from excess amino acids.", "The kidneys excrete urine."],
        optTable={"head": ["LUNGS", "SKIN", "LIVER", "KIDNEY"], "rows": [["CO₂", "Water", "Urine", "Bile"], ["CO₂", "Water", "Urea", "Urine"],
                                                                      ["Water vapour", "Bile", "Water", "Salts"], ["Urea", "Water", "Bile", "CO₂"]]}),
    mcq("1.1.4", "It is recommended that athletes train at a higher altitude for at least two weeks before a major event to increase the "
        "number of red blood cells in their body. The number of red blood cells increase to …",
        ["increase oxygen absorption because of the low oxygen levels in the atmosphere.",
         "allows the body time to remove excess carbon dioxide due to higher levels of carbon dioxide in the atmosphere.",
         "increase the amount of carbon dioxide exhaled due to high oxygen levels in the atmosphere.",
         "allows the body to absorb more oxygen due to high levels of oxygen in the atmosphere."], 0,
        ["Is the air thinner or thicker high up?", "Red blood cells carry oxygen."]),
    mcq("1.1.5", "The reason for boiling the leaf in alcohol during a starch test is to …", ["remove chlorophyll.", "show if starch is present.",
        "break cells walls making cells more permeable.", "kill the plant cells."], 0,
        ["The leaf turns white in alcohol.", "The green colour would hide the iodine's colour."]),
    mcq("1.1.6", "If the blood pH decreases, the kidneys will …", ["increase the absorption of urea into the blood.",
        "decrease the secretion of hydrogen ions into the tubules.", "increase the re-absorption of bicarbonate ions into the blood.",
        "decrease the absorption of sodium ions into the blood."], 2, ["A lower pH means the blood is more acidic.", "Bicarbonate is a base."]),
    mcq("1.1.7", "Study the list: (i) Water, (ii) CO₂, (iii) Hydrogen (H⁺) ions, (iv) Radiant energy. Which of the above listed reactants are "
        "required for photosynthesis?", ["(i); (ii) and (iv)", "(i); (iii) and (iv)", "(iv) only", "(i) and (iv)"], 0,
        ["6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂, with light.", "Hydrogen ions come from water, inside the leaf."]),
    mcq("1.1.8", "A plant's stomata close when temperatures exceed 30 ºC. What is the most likely factor to limit the photosynthetic rate after "
        "this happens?", ["Oxygen concentration", "Light intensity", "Temperature", "Carbon dioxide concentration"], 3,
        ["What enters the leaf through the stomata?", "Closed stomata keep a gas out."]),
    mcq("1.1.9", "In the diagram below, identify the process occurring at X and Y between bodily tissue cells and a capillary.",
        ["Gaseous exchange, active process", "Cellular respiration, passive process", "Gaseous exchange, passive process",
         "Cellular respiration, active process"], 2, ["O₂ and CO₂ move between the cells and the capillary.", "Diffusion uses no energy."],
        figure=P.fig("1.1.9", "Body cells around a capillary: arrow X carries O₂ from the capillary into the cells, arrow Y carries CO₂ from "
                              "the cells into the capillary."))]
q12 = [
    term("1.2.1", "Organelle in plant cells that contain chlorophyll", ["chloroplast", "chloroplasts"], ["It is green.", "Photosynthesis "
                                                                                                         "happens here."]),
    term("1.2.2", "Breathing muscle responsible for raising the rib cage during inhalation", ["intercostal muscle", "intercostal muscles",
                                                                                          "intercostals", "external intercostal muscles"],
         ["It lies between the ribs.", "Not the diaphragm."]),
    term("1.2.3", "Tubule responsible for transporting urine from the kidney to the bladder", ["ureter", "ureters"],
         ["One leaves each kidney.", "Not the urethra, which leaves the bladder."]),
    term("1.2.4", "Structures in the lung where gaseous exchange occur", ["alveoli", "alveolus", "air sacs"], ["Tiny sacs at the ends of the "
                                                                                                              "bronchioles.", "Many tiny ones."]),
    term("1.2.5", "The main photosynthetic tissue of the leaf", ["palisade mesophyll", "mesophyll", "chlorenchyma", "palisade parenchyma",
                                                              "palisade tissue"], ["It lies just under the upper epidermis.", "Its cells are packed "
                                                                                                                            "with chloroplasts."]),
    term("1.2.6", "The breakdown of a water molecule into hydrogen and oxygen atoms during photosynthesis", ["photolysis"],
         ["It needs light.", "Photo- means light; -lysis means splitting."]),
    term("1.2.7", "Protective double membrane enclosing the lungs", ["pleura", "pleural membrane", "pleural membranes"],
         ["It lines the thoracic cavity too.", "Its fluid reduces friction."]),
    term("1.2.8", "Gas required for aerobic respiration", ["oxygen", "O2", "O₂"], ["Aerobic means 'with air'.", "Which gas?"]),
    term("1.2.9", "Patches of cells in the pancreas that secrete insulin and glucagon", ["islets of Langerhans", "islets of langerhan",
                                                                                      "islets"], ["Named after a scientist.", "Islets …"])]
q13 = [
    abq("1.3.1", "Structure(s) which prevents food particles from entering the lungs", "Uvula", "Epiglottis", 1,
        ["Which one covers the opening of the trachea?", "The uvula closes the nasal passage."]),
    abq("1.3.2", "Region of the alimentary canal where most water is reabsorbed", "Proximal convoluted tubule", "Small intestine", 1,
        ["Is the PCT part of the alimentary canal?", "The alimentary canal runs from mouth to anus."]),
    abq("1.3.3", "Lined with ciliated epithelium", "Bronchi", "Trachea", 2, ["Cilia sweep mucus out of the air passages.", "Both airways."]),
    abq("1.3.4", "Hormone(s) responsible for osmoregulation", "Aldosterone", "Antidiuretic hormone", 2,
        ["Osmoregulation controls the water and salt balance.", "Aldosterone controls salts; ADH controls water."])]
q14 = [
    term("1.4.1", "What structure in the respiratory system is label A representing?", ["trachea", "windpipe"],
         ["The tube the air enters through.", "It branches into the two balloons."]),
    stmt("1.4.2", "Describe the role played by D during inhalation.", 2, ["Part D (the diaphragm) contracts.",
                                                                          "This increases the volume of the thoracic cavity."],
         ["Part D relaxes and moves up into the thoracic cavity.", "This increases the pressure in the thoracic cavity.",
          "Part D pushes air out of the lungs."], ["D is the rubber sheet: the diaphragm.", "It is pulled down to breathe in."], 1),
    stmt("1.4.3", "Give TWO reasons why the model does not truly represent the human gaseous exchange system.", 2,
         ["The sides of the model cannot move, but the rib cage moves up and down.",
          "The model has a large space between the balloons and the jar; in the body the space around the lungs is very small.",
          "In the body the diaphragm is dome-shaped; in the model the rubber sheet is flat.",
          "The balloons are hollow sacs; the lungs are made up of many small sacs."],
         ["The model has two balloons, but the body has one lung.", "In the body the diaphragm is a rubber sheet.",
          "The model shows the trachea, but the body has none."], ["Compare the jar with the rib cage.", "Compare the rubber sheet with the "
                                                                                                              "diaphragm."], 1)]
LET7 = ["A", "B", "C", "D", "E", "F", "G"]
q15 = [
    term("1.5.1(a)", "Supply a suitable label for B", ["bronchus", "bronchi", "bronchiole"], ["It branches off the trachea.", "One goes to "
                                                                                                                           "each lung."]),
    term("1.5.1(b)", "Supply a suitable label for C", ["rib", "ribs"], ["Bone around the lungs.", "Intercostal muscles lie between them."]),
    stmt("1.5.2", "Explain TWO VISIBLE reasons why the above structure could be considered an effective gaseous exchange surface.", 4,
         ["Well protected: the ribs and intercostal muscles protect the lungs from mechanical injury.",
          "Large surface area: many alveoli increase the surface area for gaseous exchange.",
          "A double pleural membrane protects the lungs against friction.",
          "A ventilation mechanism (trachea, bronchi and breathing muscles) moves air in and out."],
         ["Thick walls slow down the diffusion of gases.", "The lungs contain their own muscle that pumps air in."],
         ["What does the diagram SHOW around and inside the lungs?", "Each card gives a feature and why it helps."], 2),
    ln("1.5.3(a)", "Give the LETTER and NAME of the structure that contains cartilaginous cords which vibrate for sound production", LET7, "G",
       ["larynx", "voice box"], ["The voice box.", "It sits at the top of the trachea."]),
    ln("1.5.3(b)", "Give the LETTER and NAME of the structure that contains C-shaped cartilaginous rings", LET7, "A", ["trachea", "windpipe"],
       ["The rings keep the airway open.", "The main tube to the lungs."], **{"or": [{"letter": "B", "name": ["bronchus", "bronchi"]}]})]

# ---- SECTION B, QUESTION 2, the question paper pages 8-11 and the memo pages 6-9 ----
q21 = [
    draw("2.1.1", "Draw a histogram to represent the above data in the table.", 6,
         [["Correct type of graph", 1], ["Caption includes both variables", 1], ["Correct scale for the y-axis and equal width of bars", 1],
          ["Correct labels on the x-axis and y-axis, with the unit on the y-axis", 1], ["All 3 bars plotted correctly", 2]],
         ["One bar for each colour of light.", "Label both axes and give the graph a caption."],
         memo="The memo's graph: bars Blue 40, Green 160 and Red 80 s, captioned, the time axis 0 – 180 s."),
    stmt("2.1.2", "Why did the scientists use oxygen bubble production to look at the growth of the plant?", 2,
         ["The rate of oxygen bubble production indicates the rate of photosynthesis.", "Photosynthesis is responsible for plant growth."],
         ["Oxygen bubbles show how much water the plant absorbs.", "Oxygen bubbles show the rate of respiration in the plant.",
          "Plants grow faster when they release less oxygen."], ["Which process releases oxygen?", "How does that process make a plant grow?"],
         1),
    term("2.1.3", "Write the ratio for number of bubbles under green light compared to red light.", ["2:1", "2 : 1", "1:1", "1 : 1"],
         ["Green 160 s, red 80 s.", "Simplify the ratio."], marks=2),
    term("2.1.4", "Which light source should be recommended to grow plants under?", ["blue", "blue light"],
         ["The fastest bubbles mean the most photosynthesis.", "Which colour took the shortest time?"])]
q22 = [
    stmt("2.2.1", "Discuss how the hole in the diaphragm, caused by diaphragmatic hernia, will affect inhalation.", 3,
         ["Space in the thoracic cavity would be limited.", "The abdominal organs push into the thoracic cavity.",
          "The lungs cannot fully expand, which limits inhalation.", "The thoracic cavity is no longer a closed system.",
          "When the diaphragm contracts, the pressure in the thoracic cavity does not decrease."],
         ["Inhalation becomes deeper because the thoracic cavity is larger.", "Air enters the lungs more easily through the hole.",
          "The diaphragm relaxes more strongly during inhalation."], ["What fills the space the lungs need?", "Can the pressure still drop?"], 1),
    stmt("2.2.2", "Describe why the symptom of a rapid heart rate would occur.", 5,
         ["Breathing is difficult because the diaphragm is damaged.", "The carbon dioxide level in the blood increases.",
          "This is detected by (chemo)receptors in the aorta and carotid arteries.", "They stimulate the medulla oblongata.",
          "The medulla sends impulses to the heart muscle.", "The heart muscle contracts faster."],
         ["The oxygen level in the blood increases, which slows the heart.", "Receptors in the stomach detect the low carbon dioxide level."],
         ["Less breathing out leaves which gas in the blood?", "Receptors, the brain, then the heart."], 1)]
q23 = [
    answer("2.3.1", "State the aim for this investigation.", 2,
           ["To determine if living organisms require oxygen for aerobic respiration", "To determine if glass beads use oxygen",
            "To determine how sodium hydroxide affects insects", "To determine if living organisms release oxygen during respiration"],
           ["What did the researchers want to find out?", "The first sentence of 2.3 says it."]),
    term("2.3.2(a)", "Identify the dependent variable", ["oxygen uptake", "oxygen consumption", "oxygen", "aerobic respiration",
                                                         "movement of the dye", "volume of oxygen taken in"],
         ["What was measured?", "The dye's movement shows it."]),
    term("2.3.2(b)", "Identify the independent variable", ["presence or absence of living organisms", "presence of a living organism",
                                                           "living organism", "the insect", "presence or absence of the insect"],
         ["What differs between flask A and flask B?", "One has an insect, one glass beads."]),
    work("2.3.3", "Calculate the percentage increase of oxygen consumption from 30 minutes to 60 minutes in FLASK A.", 3, [
        "% increase = {28 − 13}/{13} × 100\n= 115,38%",    # the memo
        "% increase = {28 − 13}/{28} × 100\n= 53,57%",     # divided by the new value
        "% increase = {28}/{13} × 100\n= 215,38%",         # the old value not subtracted
        "% increase = {28 − 13}/{13}\n= 1,15%"],           # not × 100
        ["Flask A: +13 at 30 min, +28 at 60 min.", "Increase ÷ the 30-minute value × 100."]),
    stmt("2.3.4", "Explain ONE way how validity was ensured in this investigation.", 2,
         ["Both flasks had the same amount of sodium hydroxide solution, so carbon dioxide was absorbed equally in both.",
          "The insect and the glass beads had the same mass, so both flasks started at the same pressure.",
          "The syringes contained the same amount of air, so both flasks received the same amount of oxygen."],
         ["Flask B had no sodium hydroxide, so it acted as the control.", "The insect was given more air than the glass beads.",
          "Each flask was kept at a different temperature."], ["What was kept the SAME in both flasks?", "Why does that matter?"], 2)]
q24 = [
    stmt("2.4.1", "Describe the process of the Kreb's cycle.", 3,
         ["Pyruvic acid is broken down.", "Hydrogen atoms are released.", "Carbon dioxide is released.", "It takes place in the presence of "
                                                                                                         "oxygen.",
          "A small amount of energy (ATP) is released."],
         ["Glucose is split into two pyruvic acid molecules in the cytoplasm.", "Oxygen is released as a waste product.",
          "It takes place without oxygen."], ["It follows glycolysis, in the mitochondrion.", "What goes in, and what comes out?"], 1),
    stmt("2.4.2", "How does anaerobic respiration differ in plant cells compared animal cells?", 4,
         ["In animal cells pyruvic acid is broken down into lactic acid.", "This is lactic acid fermentation.",
          "In plant cells pyruvic acid is broken down into ethanol and carbon dioxide.", "This is alcoholic fermentation."],
         ["In animal cells pyruvic acid is broken down into ethanol and carbon dioxide.", "In plant cells pyruvic acid is broken down into "
                                                                                        "lactic acid.",
          "Both use oxygen to break down pyruvic acid."], ["Muscles make one product, yeast another.", "Name each product and the process."],
         1),
    stmt("2.4.3", "Discuss TWO economic benefits of the use of anaerobic respiration in yeast.", 4,
         ["Alcoholic fermentation forms alcohol, which can be sold for income.",
          "It makes bread dough rise, giving a greater volume of product at a greater profit."],
         ["Yeast's anaerobic respiration produces oxygen for fish farms.", "Yeast fermentation removes alcohol from wine.",
          "Yeast's anaerobic respiration makes cheese go hard."], ["Think of brewing and baking.", "Each card gives a use and its benefit."], 2),
    term("2.4.4", "List ONE symptom of prolonged anaerobic respiration in muscles.", ["muscle cramps", "cramps", "cramp", "muscle cramp",
                                                                                      "spasms", "fatigue", "muscle fatigue"],
         ["Lactic acid builds up.", "What do tired muscles do?"])]
q25 = [
    stmt("2.5.1", "Name TWO other environmental conditions that can be controlled in a greenhouse.", 2,
         ["Light intensity", "Temperature", "Water", "Humidity"], ["Altitude", "Latitude", "The time of day"],
         ["What else does a plant need, apart from carbon dioxide?", "What can a greenhouse change?"], 1),
    stmt("2.5.2", "What causes the drop in CO₂ concentration from 06:00 to 12:00.", 2,
         ["Photosynthesis (its light-independent phase) takes place.", "This phase uses carbon dioxide to produce glucose."],
         ["Respiration releases carbon dioxide.", "Carbon dioxide is pumped out of the greenhouse.",
          "The plants stop photosynthesising in the morning."], ["The sun is up.", "Which process uses carbon dioxide?"], 1),
    stmt("2.5.3", "Why should a farmer not exceed the recommended dosage of CO₂.", 2,
         ["Excess carbon dioxide would be a wasted expense.", "Plants cannot absorb carbon dioxide beyond a set maximum.",
          "Excess carbon dioxide could become toxic to plant growth.", "It may lead to the death of the plant."],
         ["Extra carbon dioxide always makes plants grow faster.", "Carbon dioxide is free, so there is no cost.",
          "Plants release more oxygen the more carbon dioxide they get, without limit."], ["Is there a limit to what plants can use?",
                                                                                          "What does it cost?"], 1),
    stmt("2.5.4", "After 16:00 no further carbon dioxide was pumped into the greenhouse. Explain what would have caused CO₂ levels to increase "
         "from 22:00 until 06:00.", 4,
         ["Cellular respiration occurs.", "Glucose is broken down in the presence of oxygen.", "Carbon dioxide is released.",
          "No photosynthesis occurs because there is no light.", "No carbon dioxide is being absorbed."],
         ["Photosynthesis releases carbon dioxide at night.", "Carbon dioxide is still being pumped in.",
          "The plants absorb more carbon dioxide in the dark."], ["It is night.", "Which process goes on day and night?"], 1)]

# ---- QUESTION 3, the question paper pages 12-14 and the memo pages 10-13 (3.3.6 removed by the amended memo) ----
LET6 = ["A", "B", "C", "D", "E", "F"]
q31 = [
    ln("3.1.1(a)", "Give the LETTER and NAME of the part of the nephron where tubular excretion occurs", LET6, "C",
       ["distal convoluted tubule", "DCT", "second convoluted tubule"], ["Substances are secreted from the blood into the tubule.",
                                                                          "After the loop of Henle."],
       **{"or": [{"letter": "B", "name": ["collecting duct", "collecting tubule"]}]}),
    ln("3.1.1(b)", "Give the LETTER and NAME of the part of the nephron where sodium (salt) is actively pumped out", LET6, "D",
       ["ascending limb of Henle", "ascending limb of the loop of Henle", "loop of Henle"], ["The loop pumps salt into the medulla.",
                                                                                            "Which side of the loop?"]),
    stmt("3.1.2", "Explain THREE structural adaptations of structure A for efficient filtration.", 6,
         ["The capillaries have microscopic pores, allowing only smaller components of blood through.",
          "A dense capillary network (and the cup-shaped Bowman's capsule) increases the surface area for filtration.",
          "The afferent arteriole is wider than the efferent arteriole, placing the blood in the glomerulus under pressure.",
          "Podocytes lining the Bowman's capsule form filtration slits.",
          "The glomerulus is in close contact with the Bowman's capsule, reducing the distance the filtrate moves.",
          "The thin, semi-permeable endothelium lets substances move through easily."],
         ["The efferent arteriole is wider than the afferent arteriole, lowering the pressure.",
          "The glomerulus has thick walls to stop substances passing."],
         ["A is the renal corpuscle: the glomerulus in the Bowman's capsule.", "Each card gives a feature and why it helps."], 2),
    stmt("3.1.3(a)", "Describe how the reabsorption of glucose takes place from part F.", 2,
         ["Active reabsorption.", "Energy (ATP) from the cuboidal epithelial cells is used."],
         ["Passive reabsorption by osmosis.", "Glucose moves down the concentration gradient without energy.", "Glucose is secreted into "
                                                                                                            "the tubule."],
         ["F is the proximal convoluted tubule.", "Does it need energy?"], 1),
    stmt("3.1.3(b)", "Describe how the reabsorption of water takes place from part F.", 2,
         ["Passive reabsorption by osmosis.", "Water moves from a region of high water potential to a region of low water potential."],
         ["Active reabsorption using ATP.", "Water moves from a region of low water potential to a region of high water potential.",
          "Water is pumped by carrier proteins."], ["Water follows the solutes.", "Which way does water move by osmosis?"], 1),
    stmt("3.1.4", "Describe the role of ADH on structure B and C when the body is dehydrated.", 3,
         ["More ADH is produced.", "The distal convoluted tubules and collecting ducts become more permeable to water.",
          "More water leaves the renal tubules.", "More water is reabsorbed into the blood."],
         ["Less ADH is produced.", "The tubules become less permeable to water.", "More dilute urine is produced."],
         ["The body needs to keep water.", "ADH opens the walls to water."], 1)]
q32 = [
    term("3.2.1", "Identify the excretory product in the table above that is produced in the liver from deamination of amino acids.", ["urea"],
         ["Deamination removes the amino group.", "It is far higher in the urine than in the plasma."]),
    stmt("3.2.2", "Explain ONE reason why no proteins are found in the filtrate.", 2,
         ["Proteins are too large.", "They cannot move through the pores of the glomerulus."],
         ["Proteins are reabsorbed in the loop of Henle.", "Proteins are digested in the Bowman's capsule.", "Proteins are too small to be "
                                                                                                           "filtered."],
         ["Think of the filter's holes.", "What size are protein molecules?"], 1),
    stmt("3.2.3", "The table indicates that high levels sodium ions were excreted. Explain what causes the high sodium levels in the urine when "
         "levels are too high in the blood.", 2,
         ["Less aldosterone is secreted.", "The renal tubules become less permeable to sodium ions.", "Fewer sodium ions are reabsorbed from "
                                                                                                    "the filtrate."],
         ["More aldosterone is secreted.", "More sodium ions are reabsorbed into the blood.", "ADH pumps sodium into the urine."],
         ["Which hormone controls salt?", "Too much salt: more or less of it?"], 1),
    stmt("3.2.4", "Explain the condition that the patient most likely has, given the glucose levels in the table.", 3,
         ["The patient most likely has diabetes mellitus.", "There is a high glucose level in the urine.", "Insulin is not being produced or "
                                                                                                           "is not effective."],
         ["The patient has kidney stones.", "Too much insulin is being produced.", "There is no glucose in the urine."],
         ["Healthy urine has no glucose.", "Which hormone lowers blood glucose?"], 1)]
q33 = [
    term("3.3.1(a)", "Provide a suitable label for part A", ["liver"], ["The largest organ in the abdomen.", "Upper right."]),
    term("3.3.1(b)", "Provide a suitable label for part D", ["rectum"], ["The last part of the large intestine.", "It stores faeces."]),
    term("3.3.1(c)", "Provide a suitable label for part F", ["gall bladder", "gallbladder"], ["A small sac under the liver.", "It stores "
                                                                                                                         "bile."]),
    stmt("3.3.2", "List TWO functions of the HCl produced in structure B.", 2,
         ["It provides a low pH (acidic conditions) for enzymes to function.", "It kills bacteria."],
         ["It emulsifies fats.", "It neutralises the chyme.", "It absorbs glucose."], ["B is the stomach.", "What does acid do?"], 1),
    stmt("3.3.3", "Explain TWO adaptations of part E for its effective functioning.", 4,
         ["It is long, increasing the time and surface area for absorption.", "Its walls are folded, increasing the surface area for "
                                                                              "absorption.",
          "Its inner wall has villi, increasing the surface area for absorption.", "Each villus has microvilli, further increasing the surface "
                                                                                   "area.",
          "A good blood supply maintains the gradient for nutrient absorption."],
         ["Its walls are thick to slow down absorption.", "It has a poor blood supply to keep nutrients in the gut."],
         ["E is the small intestine.", "Each card gives a feature and why it helps."], 2),
    term("3.3.4", "Identify the structure that secretes bile.", ["liver", "A"], ["Not the gall bladder: it only stores bile.", "Part A."]),
    stmt("3.3.5", "Describe ONE role bile serves as it enters the small intestine.", 2,
         ["Emulsification of fats.", "Neutralisation of acidic chyme."],
         ["Digestion of proteins into amino acids.", "Killing bacteria with acid.", "Absorption of glucose."],
         ["Bile has no enzymes.", "It breaks fat into droplets."], 2)]
q34 = [
    ln("3.4.1(a)", "Give the NAME of the monomer(s) and the LETTER where it is absorbed in the villus for lipids", ["A", "B", "C"], "C",
       ["glycerol and fatty acids", "fatty acids and glycerol", "fatty acids", "glycerol"], ["Lipids go into the lacteal.",
                                                                                           "Lipids are made of glycerol and …"]),
    ln("3.4.1(b)", "Give the NAME of the monomer(s) and the LETTER where it is absorbed in the villus for carbohydrate", ["A", "B", "C"], "A",
       ["glucose", "monosaccharides", "monosaccharide"], ["Sugars go into the blood capillaries.", "The simplest sugar."]),
    stmt("3.4.2", "Due to Crohn's disease the villus in the small intestine becomes reduced in size and eventually flattened. Briefly discuss how "
         "Crohn's disease will affect the nutrition and lifestyle of an individual.", 4,
         ["There is a smaller surface area for the absorption of nutrient monomers.", "Fewer nutrients reach the blood.",
          "The body cannot sustain its nutritional needs.", "The person may get tired more often, with less energy.",
          "This leads to health complications."],
         ["The flattened villi absorb more nutrients.", "The person will have more energy.", "Digestion in the stomach stops completely."],
         ["Flat villi: more or less surface?", "What happens to energy?"], 1)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 18,
     "lead": "Various options are provided as possible answers to the following questions. Study the diagram below of an animal's skull and "
             "answer QUESTIONS 1.1.1 to 1.1.2.",
     "figure": P.fig("1.1", "An animal's skull from the side, the jaws open: long pointed canines, small front incisors and pointed back teeth."),
     "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 9,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 8,
     "lead": "Indicate whether each description in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Breathing", "marks": 5,
     "lead": "The model of the lungs below is used to demonstrate the mechanism of breathing.",
     "figure": P.fig("1.4", "Two bell-jar models: a glass jar with a Y-tube into two balloons, a rubber sheet across the bottom. A points to "
                            "the stem of the Y-tube, B to a branch, C to a balloon, D to the rubber sheet, pulled down in the second model."),
     "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Gaseous exchange", "marks": 10,
     "lead": "The diagram below represents part of the human gaseous exchange system.",
     "figure": P.fig("1.5", "The lungs in the chest, in section: G points to the top of the airway in the neck, A to the airway below it, B "
                            "to a branch into a lung, C to the bones round the chest, D and E to the muscle below the lungs and F to the "
                            "lung's tissue."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Photosynthesis investigation", "marks": 11,
     "table": {"head": ["COLOUR OF LIGHT", "TIME (IN SECONDS) TO RELEASE 20 OXYGEN BUBBLES"], "rows": [["Blue", "40"], ["Green", "160"],
                                                                                                    ["Red", "80"]]},
     "lead": "Scientists conducted a study to determine under which colour of light Elodea (waterweed) grows best. The experiment was "
             "conducted as follows:\n• The apparatus was set up as in the diagram below\n• Three experiments were set-up, each, under a different "
             "colour of light (blue, green or red)\n• The distance from the light source in each, remained 30 cm\nThe average time taken to "
             "produce 20 oxygen bubbles was recorded in the table below.",
     "figure": P.fig("2.1", "A lamp shining on Elodea in a beaker of water under an upturned test tube, oxygen bubbles rising into it."),
     "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Breathing and the heart", "marks": 8,
     "lead": "A serious motor vehicle accident resulted in a child having a perforated diaphragm (diaphragmatic hernia). His abdominal organs "
             "were pushed into his thoracic cavity. Symptoms included difficulty in breathing and a rapid heart rate.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Respiration investigation", "marks": 9,
     "table": {"head": ["MOVEMENT OF DYE (CM)", "0 min", "15 min", "30 min", "45 min", "60 min"],
               "rows": [["FLASK A", "0", "+7", "+13", "+20", "+28"], ["FLASK B", "0", "−7", "−13", "−20", "−28"]]},
     "lead": "Researchers wanted to determine if living organisms require oxygen for aerobic respiration. Oxygen uptake can be measured using a "
             "respirator as shown in the set-up below.\n• The apparatus consists of two flasks, one containing the living organism and the "
             "other glass beads.\n• Both tubes contain the same volume of sodium hydroxide.\n• Once the apparatus has been set up, the movement "
             "of the coloured liquid in the manometer (U-shaped tube containing a dyed fluid) will indicate how much oxygen is used.\n• The "
             "decrease in oxygen in one tube increases pressure causing the coloured liquid to move up that tube.\nThe distance moved by the "
             "liquid in the manometer over time was measured to indicate the volume of oxygen taken in by the insect per minute.",
     "figure": P.fig("2.3", "Two flasks joined by a U-shaped manometer of dyed fluid: FLASK A holds an insect on metal gauze, FLASK B glass "
                            "beads of the same mass; each has sodium hydroxide solution, a filter paper wick, a rubber stopper and a syringe "
                            "of air; a closed tap on flask A."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Respiration", "marks": 12,
     "lead": "Respiration occurs in both aerobic and anaerobic conditions. These processes differ in plant and animal cells. In plant cells "
             "anaerobic respiration has been shown to hold several key economic uses and benefits.", "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Greenhouses", "marks": 10,
     "lead": "Greenhouses are enclosed structures used to grow plants under controlled conditions. Carbon dioxide levels are kept high during "
             "the day light hours so optimal photosynthesis can take place. The graph below displays the CO₂ concentration in a greenhouse "
             "over a 24-hour period. From 12:00 until 16:00 carbon dioxide was pumped into the greenhouse.",
     "figure": P.fig("2.5", "A line graph, CARBON DIOXIDE CONCENTRATION (PPM) IN A GREENHOUSE SYSTEM OVER A 24 HOUR DAY: 500 ppm at 00:00 "
                            "rising to 700 at 06:00, falling to 500 at 12:00, rising to about 640 at 16:00, falling to about 390 at 22:00 and "
                            "rising to 500 at 24:00."), "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "The nephron", "marks": 17, "lead": "A line diagram of the nephron is shown below.",
     "figure": P.fig("3.1", "A nephron beside its blood vessels: A points to the cup at the start with its knot of capillaries, F to the "
                            "coiled tubule after it, E to the bottom of the loop, D to the loop's rising side, C to the second coiled tubule "
                            "and B to the duct it joins."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Kidney function", "marks": 8,
     "table": {"head": ["", "PLASMA", "FILTRATE", "URINE"],
               "rows": [["Glucose", ">120", ">90", "50"], ["Proteins", "740–750", "0", "0"], ["Urea", "30", "30", ">1 200"],
                        ["Sodium", "287", "262", "276"], ["Water", "900", "900", "687"], ["Amino acids", "0,5", "0,5", "0,0"]]},
     "lead": "The chart below shows the composition of various solutes found in blood plasma, glomerular filtrate, and urine of a patient that "
             "came to the hospital after collapsing into a coma.", "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Digestion", "marks": 12, "lead": "The diagram below represents the human digestive system.",
     "figure": P.fig("3.3", "The digestive system in the body: A points to the large organ at the upper right, F to the small sac below it, "
                            "B to the stomach, C to the organ behind the stomach, E to the coiled tube in the middle and D to the end of the "
                            "large intestine."), "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Absorption", "marks": 8,
     "lead": "The end products of digestion are monomers that are easily absorbed. Review the given line diagram of the villus.",
     "figure": P.fig("3.4", "A villus: C points to the vessel down its centre, A to the network of blood vessels around it and B to the "
                            "vessels at its base."), "items": q34},
]
P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2024", "total_marks": 145, "time": "2½ hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "3.3", "kind": "no_fit", "detail": "3.3.6 (draw a line diagram of a cross-section through part E, 5 marks) is left out: the "
                                                   "FINAL AMENDED memo removes it ('Microscopic structure not in CAPS. Mark out of 145 and "
                                                   "convert to 150'). The paper plays 145."},
          {"n": "1.3.4", "kind": "memo_issue", "detail": "The memo accepts BOTH A and B OR B ONLY; one right option plays: Both A and B, the "
                                                         "memo's first answer."},
          {"n": "2.1.3", "kind": "memo_issue", "detail": "The question asks the ratio of the NUMBER of bubbles (20 : 20 = 1 : 1); the memo's "
                                                         "first answer is the ratio of the times (160 : 80 = 2 : 1) and it accepts 1 : 1. "
                                                         "Both are typed answers."},
          {"n": "2.1.1", "kind": "no_fit", "detail": "The graph to draw (2.1.1) plays as pick the drawing; the memo marks it as a bar graph."}],
         {"1": 50, "2": 50, "3": 45}, 145, {}, "Questions 1 to 3 (3.3.6 removed by the amended memo)")
