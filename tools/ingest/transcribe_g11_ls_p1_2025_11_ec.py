"""Grade 11 Life Sciences P1 November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 3, 150 marks,
2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and answers are
the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2025 November Grade
11, the question paper zip (English PDF, 16 pages, text layer) and the memo zip (English, 10 pages).

  python tools/ingest/transcribe_g11_ls_p1_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ls-p1-2025-11-ec/LIFE SCIENCES P1 GR11 QP NOV2025_English_watermark.pdf" "uploads/provincial/g11-ls-p1-2025-11-ec/LIFE SCIENCES P1 GR11 MEMO NOV2025_English_watermark.pdf" --id g11-ls-p1-2025-11-ec --from-json

The Life Sciences rulings, as in transcribe_g11_ls_p1_2024_11_ec.py; a tabulated difference (2.1.3) and a distinction (3.1.3) play as
a SORT into columns (Paper.sort, as Grade 12 LS P2 Nov 2024 3.4.3); the one calculation (2.2.3(b)) as four workings. Figure boxes are
in PDF points (text blocks and image rects), 1% inside their neighbours."""
from provincial import Paper

H = 841.92
P = Paper("g11-ls-p1-2025-11-ec", 595.32, H, {
    "1.1.5": [4, 160.0, 90.0, 476.0, 384.0, {"blank": [[0, 226 / H, 1, 252 / H]]}], "1.4": [7, 125.0, 88.0, 420.0, 388.0],
    "1.5": [8, 83.0, 117.0, 477.0, 475.0], "2.1": [9, 115.0, 140.0, 450.0, 285.0], "2.3": [11, 83.0, 103.0, 509.0, 295.0],
    "2.4": [12, 90.0, 300.0, 300.0, 510.0], "3.1": [13, 130.0, 118.0, 482.0, 412.0], "3.2": [14, 82.0, 89.0, 508.0, 270.0],
    "3.4": [15, 105.0, 108.0, 465.0, 470.0], "3.5": [16, 120.0, 105.0, 410.0, 414.0]}, start=6)
work, answer, num, draw, stmt, mcq, term, sort = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term, P.sort
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
ln = lambda n, q, letters, letter, names, clues, **kw: {"t": "lettername", "n": n, "marks": 2, "q": q, "clues": clues, "letters": letters,
                                                       "a": {"letter": letter, "name": names}, **kw}
LET6 = ["A", "B", "C", "D", "E", "F"]

# ---- SECTION A, QUESTION 1, the question paper pages 3-8 and the memo page 4 ----
q11 = [
    mcq("1.1.1", "The structure which prevents the food bolus from entering the trachea when swallowing:", ["Epiglottis", "Tongue", "Glottis",
                                                                                                            "Teeth"], 0,
        ["A flap of cartilage.", "It covers the windpipe's opening."]),
    mcq("1.1.2", "A function of the kidney:", ["CO₂ homeostasis", "Breakdown of bile pigments", "Blood pH homeostasis", "Deamination"], 2,
        ["The liver breaks down bile pigments and deaminates.", "The kidney secretes H⁺ ions."]),
    mcq("1.1.3", "The part of the alimentary canal in which the villus is found:", ["Oesophagus", "Large intestine", "Stomach", "Small intestine"],
        3, ["Villi absorb digested food.", "Where is most food absorbed?"]),
    mcq("1.1.4", "Factor(s) which facilitate oxygen absorption into the human body:",
        ["Air breathed in has less oxygen than air breathed out", "Alveoli having thick walls for oxygen storage and a large surface area",
         "There are few alveoli in each lung", "The concentration of oxygen in the blood is lower than in the alveoli"], 3,
        ["Diffusion needs a gradient.", "From high to low concentration."]),
    mcq("1.1.5", "A cross-section of a dicot leaf is shown below. Which type of cell is expected to be found at layer X?", ["A", "B", "C", "D"],
        2, ["X is just under the upper epidermis.", "Tall cells packed with chloroplasts."],
        figure=P.fig("1.1.5", "A dicot leaf in section, X pointing to the layer just under the upper epidermis. Below it, four cells: A a tall "
                              "empty cell, B a small round empty cell, C a tall cell packed with dots, D a small irregular cell with dots.")),
    mcq("1.1.6", "The table shows the composition of four air samples: P (O₂ 21%, CO₂ 0,04%, N₂ 78%), Q (16%, 4,04%, 78%), R (4%, 0,40%, 39%), "
        "S (20%, 4,00%, 39%). Which air sample represents inspired air and which air sample represents expired air?",
        ["Inspired S · expired R", "Inspired P · expired S", "Inspired P · expired Q", "Inspired Q · expired S"], 2,
        ["Air is about 78% nitrogen in and out.", "Breathed-out air has less oxygen and more carbon dioxide."],
        optTable={"head": ["INSPIRED AIR", "EXPIRED AIR"], "rows": [["S", "R"], ["P", "S"], ["P", "Q"], ["Q", "S"]]}),
    mcq("1.1.7", "Substances which are removed from the blood during tubular secretion.", ["Water, sodium ions and hormones",
                                                                                            "Glucose and sodium ions",
                                                                                            "Undigested food and creatine",
                                                                                            "Hormones, urea and creatine"], 3,
        ["Secretion adds waste to the filtrate.", "Glucose and water are reabsorbed, not secreted."]),
    mcq("1.1.8", "The correct path that urine takes through the excretory system", ["Kidney → urethra → bladder → ureter",
                                                                                    "Kidney → ureter → bladder → urethra",
                                                                                    "Bladder → kidney → ureter → urethra",
                                                                                    "Ureter → kidney → urethra → bladder"], 1,
        ["Urine is made in the kidney.", "The ureter comes before the bladder."]),
    mcq("1.1.9", "Osmoregulation is the way the body controls the amount of water and salts it contains. What is most likely to happen in the "
        "body on a cold day when a person drinks a lot of water?", ["Urea concentration low · renal tubule permeable · urine volume high",
                                                                    "Urea concentration high · renal tubule impermeable · urine volume low",
                                                                    "Urea concentration low · renal tubule impermeable · urine volume low",
                                                                    "Urea concentration high · renal tubule permeable · urine volume high"], 0,
        ["Lots of water dilutes the urine.", "Cold days mean little sweating, so more urine."],
        optTable={"head": ["UREA CONCENTRATION", "RENAL TUBULE PERMEABILITY", "URINE VOLUME"],
                  "rows": [["Low", "Permeable", "High"], ["High", "Impermeable", "Low"], ["Low", "Impermeable", "Low"],
                           ["High", "Permeable", "High"]]}),
    mcq("1.1.10", "The inside of the trachea (windpipe) is lined with a special tissue called ciliated columnar epithelium. This tissue has tiny "
        "hair-like structures called cilia. What is the main function of the cilia in the trachea (windpipe)?",
        ["Increase surface area for gaseous exchange", "Help gases move quickly because they are close to blood vessels",
         "Trap dirt and pathogenic (harmful) microbes (germs)", "Excrete metabolic waste products"], 2,
        ["No gaseous exchange happens in the trachea.", "They sweep mucus upwards."])]
q12 = [
    term("1.2.1", "Process of taking air into and expelling it from the lungs", ["breathing", "ventilation"], ["Inhaling and exhaling.",
                                                                                                             "Not respiration."]),
    term("1.2.2", "The hormone which assists in the regulation of sodium ions", ["aldosterone"], ["From the adrenal cortex.", "Salt balance."]),
    term("1.2.3", "Large flat and uneven teeth used for grinding and crushing food", ["molars", "molar", "premolars", "pre-molars", "premolar"],
         ["At the back of the mouth.", "Not incisors or canines."]),
    term("1.2.4", "Region which connects the nasal cavity with larynx and leads into the trachea and the oesophagus", ["pharynx"],
         ["The throat.", "Both air and food pass it."]),
    term("1.2.5", "Release of a useful substance (enzymes, saliva) from cells or glands", ["secretion"], ["Not excretion: the substance is "
                                                                                                          "useful.", "Glands …"]),
    term("1.2.6", "Semi-liquid mass of partially digested food which has gone through mechanical and chemical digestive processes of the stomach",
         ["chyme"], ["It leaves the stomach.", "Not bolus: that is in the mouth."]),
    term("1.2.7", "Folded portion of the nephron between the loop of Henle and the collecting tubule", ["distal convoluted tubule", "DCT",
                                                                                                        "second convoluted tubule"],
         ["Distal means far.", "Convoluted means coiled."]),
    term("1.2.8", "Process which requires no energy to move water from a region of high water potential to a region of low water potential",
         ["osmosis"], ["Water through a membrane.", "Passive."])]
q13 = [
    abq("1.3.1", "Part(s) of the chloroplast in which chlorophyll is located", "Thylakoid", "Lamellae", 0,
        ["Chlorophyll sits in the stacked discs.", "Lamellae join the grana."]),
    abq("1.3.2", "Cell(s) which make up the surface of the villus", "Compound columnar", "Goblet", 1,
        ["The villus is lined with a single layer.", "Goblet cells make mucus."]),
    abq("1.3.3", "Structure(s) which assist in keeping the trachea open", "Circular muscle", "Epiglottis", 3,
        ["C-shaped cartilage rings keep it open.", "Neither is cartilage rings."]),
    abq("1.3.4", "A part of the blood circulatory system of the kidney", "Convoluted tubules", "Renal calyxes", 3,
        ["Tubules carry filtrate; calyces carry urine.", "Neither carries blood."])]
q14 = [
    ln("1.4.1(a)", "Identify the label and state the name of the cup-shaped structure which surrounds the renal papillae and funnels urine",
       LET6, "F", ["renal calyx", "calyx", "calyces", "renal calyces"], ["Cup-shaped.", "It collects from the papillae."]),
    ln("1.4.1(b)", "Identify the label and state the name of the part that has layers of fat (adipose tissue) to protect the kidney from "
       "mechanical injury", LET6, "B", ["renal capsule", "capsule"], ["The outer covering.", "Round the whole kidney."]),
    ln("1.4.1(c)", "Identify the label and state the name of the part that collects urine from the calyces and channels it into the ureter", LET6,
       "C", ["renal pelvis", "pelvis"], ["A funnel into the ureter.", "Renal p…"]),
    answer("1.4.2", "Explain why part D appears darker red or brown compared to part A.", 1,
           ["Part D contains more blood vessels.", "Part D contains more urine.", "Part D contains more fat.", "Part D is made of muscle."],
           ["What makes tissue red?", "Blood."])]
q15 = [
    stmt("1.5.1", "Define the term homeostasis.", 2,
         ["The body's ability to maintain a stable internal environment", "despite changes in the external environment."],
         ["The body's ability to change its internal environment to match the outside.", "Keeping the external environment constant.",
          "Fighting infections with antibodies."], ["Homeo- means the same.", "Inside stays steady."], 1),
    term("1.5.2(a)", "When the level of carbon dioxide in the human body becomes too high, which part of the body acts as the receptor?",
         ["chemoreceptors", "chemoreceptors in the carotid artery", "chemoreceptors of the carotid artery", "carotid artery",
          "receptors in the carotid artery"], ["It senses chemicals in the blood.", "In the neck."]),
    stmt("1.5.2(b)", "When the level of carbon dioxide in the human body becomes too high, which part of the body acts as the effector?", 2,
         ["Intercostal muscles", "Diaphragm", "Heart"], ["Medulla oblongata", "Carotid artery", "Kidney"],
         ["Effectors carry out the response.", "Breathing and heart rate speed up."], 1),
    stmt("1.5.3", "Give TWO reasons why it is important for carbon dioxide levels in the blood not to remain high.", 2,
         ["The blood becomes increasingly acidic.", "Less aerobic respiration can take place."],
         ["The blood becomes more alkaline.", "More oxygen is carried in the blood.", "Breathing slows down."],
         ["CO₂ forms an acid in water.", "Cells need oxygen to respire."], 1)]

# ---- SECTION B, QUESTION 2, the question paper pages 9-12 and the memo pages 5-7 ----
q21 = [
    term("2.1.1", "Identify the organelle shown above.", ["chloroplast"], ["Stacks of discs inside.", "Photosynthesis happens here."]),
    stmt("2.1.2", "State TWO visible reasons for the answer given to QUESTION 2.1.1.", 2,
         ["Thylakoids (grana) are present.", "Stroma is present.", "Starch granules are present."],
         ["Cristae are present.", "A nucleus is present.", "Contractile vacuoles are present."], ["What can you see inside?", "Stacks and fluid."],
         1),
    sort("2.1.3", "Beside their locations, tabulate TWO differences between the processes which occur at A and B.",
         ["Light phase (B)", "Dark phase (A)", "Neither phase"],
         [("Requires light", 0), ("Photolysis occurs", 0), ("Carbon dioxide is absorbed", 1), ("Glucose is produced", 1),
          ("Oxygen is absorbed", 2)], ["B is in the grana, A in the stroma.", "Light splits water; CO₂ is fixed in the dark."]),
    stmt("2.1.4", "List TWO biological importances of the process which occurs within the given organelle.", 2,
         ["It produces food for heterotrophs (the basis of food chains).", "It produces oxygen.", "It absorbs and stores carbon dioxide.",
          "It keeps the oxygen level in the environment constant."],
         ["It releases carbon dioxide into the air.", "It breaks down glucose for energy."], ["Food and gases.", "What do animals need from "
                                                                                                                "plants?"], 1),
    stmt("2.1.5", "Describe ONE visible structural feature within the organelle that makes it suitable for its primary function.", 2,
         ["Many grana (thylakoids) hold a lot of chlorophyll to maximise photosynthesis.", "A large surface area lets the most radiant energy in.",
          "Its fluid stroma allows the chemical reactions of the dark phase to take place."],
         ["It has cristae, which increase the surface area for respiration.", "It has a nucleus that controls photosynthesis."],
         ["Each card gives a feature and why it helps.", "Look at the stacks."], 2)]
q22 = [
    stmt("2.2.1", "List ONE benefit of greenhouse systems on the local community.", 1,
         ["Greenhouses create jobs and support the local economy.", "Local vegetables are grown, so food need not be imported.",
          "Crops grow all year, even when it is cold."],
         ["Greenhouses make winters warmer outside.", "Greenhouses stop people from farming."], ["Read the extract.", "Jobs and food."], 1),
    stmt("2.2.2", "Explain how Russian greenhouses are energy efficient.", 2,
         ["Greenhouses use geothermal and solar energy.", "This reduces the need for electricity from the power grid and saves costs."],
         ["Greenhouses burn coal for heat.", "Greenhouses use more electricity in winter.", "Greenhouses need no energy at all."],
         ["Read the extract's last lines.", "Sun and earth."], 1),
    stmt("2.2.3(a)", "The best temperature for growing plants in a greenhouse is 28 °C; outside it is −25 °C. Give TWO ways to keep the "
         "temperature warm inside the greenhouse when it is very cold outside.", 2,
         ["Use heaters powered by geothermal energy.", "Use insulating material (double walls or plastic layers) to keep the heat in."],
         ["Open the windows at night.", "Remove the roof in winter.", "Water the plants with ice water."], ["Add heat.", "Keep heat in."], 1),
    work("2.2.3(b)", "Calculate the percentage difference in temperature between outside (−25 °C) and inside (28 °C) the greenhouse.", 3, [
        "% difference = {28 − (−25)}/{25} × 100\n= {53}/{25} × 100\n= 212%",       # the memo's second form
        "% difference = {28 − 25}/{25} × 100\n= {3}/{25} × 100\n= 12%",            # the minus sign dropped
        "% difference = {28 − (−25)}/{28} × 100\n= {53}/{28} × 100\n= 189,29%",    # divided by the inside temperature
        "% difference = {28 + 25}/{100} × 100\n= {53}/{100} × 100\n= 53%"],        # divided by 100
        ["From −25 °C up to 28 °C is 53 degrees.", "Divide by the size of the outside temperature, then × 100."]),
    stmt("2.2.4(a)", "Greenhouses use UV-A and UV-B light bulbs when there is not enough sunlight. Briefly discuss the relationship between light "
         "intensity and the photosynthetic rate of plants.", 3,
         ["As light intensity increases, the rate of photosynthesis increases.", "This happens up to a point.",
          "Beyond this point, more light does not change the rate."],
         ["As light intensity increases, the rate of photosynthesis decreases.", "The rate keeps increasing without any limit.",
          "Light intensity has no effect on photosynthesis."], ["More light, more photosynthesis …", "… until something else limits it."],
         1),
    stmt("2.2.4(b)", "Explain ONE limiting factor of light intensity in plants.", 2,
         ["Chlorophyll is saturated or insufficient.", "There are not enough enzymes to assist with photosynthesis."],
         ["There is too much water in the soil.", "The roots cannot absorb the light.", "Oxygen stops the light phase."],
         ["What inside the leaf captures light?", "It can only use so much."], 2)]
q23 = [
    term("2.3.1(a)", "Identify process A", ["glycolysis"], ["The first stage.", "In the cytoplasm."]),
    term("2.3.1(b)", "Identify reactant X", ["oxygen", "O2", "O₂"], ["Needed in the last stage.", "Aerobic."]),
    term("2.3.1(c)", "Identify product Y", ["carbon dioxide", "CO2", "CO₂"], ["A waste gas.", "Breathed out."]),
    answer("2.3.2", "Is process A an anabolic or catabolic process? Give ONE reason for the answer.", 2,
           ["Catabolic: glucose is broken down into pyruvic acid", "Anabolic: glucose is built up from pyruvic acid",
            "Catabolic: pyruvic acid is built up into glucose", "Anabolic: glucose is broken down into pyruvic acid"],
           ["Catabolic means breaking down.", "What happens to glucose?"]),
    answer("2.3.3", "Between A and B, which process produces more ATP? Give a reason for the answer.", 2,
           ["Process B: oxygen is the final electron acceptor, and about 36 ATP are made", "Process A: it makes 36 ATP while B makes 2",
            "Process A: it takes place without oxygen", "Process B: it takes place in the cytoplasm"],
           ["Glycolysis makes only 2 ATP.", "The electron transport chain needs oxygen."]),
    stmt("2.3.4", "Describe the events of the Krebs cycle.", 4,
         ["It can only take place if oxygen is present.", "It occurs inside the mitochondrion.", "It releases carbon dioxide and high-energy "
                                                                                                "hydrogen.",
          "It transports hydrogen atoms to the third stage."],
         ["It takes place in the cytoplasm.", "It takes place without oxygen.", "It produces lactic acid."],
         ["The second stage.", "Where, what goes in, what comes out?"], 1),
    stmt("2.3.5", "An athlete complained about muscle cramps after running a marathon for four and a half hours. Using your understanding of "
         "cellular respiration, explain why this has occurred.", 3,
         ["Not enough oxygen reached his muscles for aerobic respiration.", "Pyruvic acid was converted into lactic acid.",
          "Lactic acid caused his muscles to cramp."],
         ["Too much oxygen reached his muscles.", "Glucose was converted into alcohol in his muscles.", "Lactic acid was turned into glucose, "
                                                                                                       "causing cramps."],
         ["Long, hard exercise.", "Anaerobic respiration in muscle."], 1)]
CO2 = {"head": ["TIME IN DAYS"] + [str(d) for d in range(16)],
       "rows": [["CO₂ CONCENTRATION (ARBITRARY UNITS)", "5", "5", "5", "5", "5", "5", "5,3", "5,4", "5,5", "6,4", "6,5", "6,5", "6,6", "6,8",
                 "7,1", "7,4"]]}
q24 = [
    term("2.4.1", "Identify the dependent variable of the investigation.", ["carbon dioxide concentration", "CO2 concentration",
                                                                            "CO₂ concentration", "carbon dioxide level", "CO2 level",
                                                                            "concentration of carbon dioxide"],
         ["What did the data logger record?", "Read the table's heading."]),
    stmt("2.4.2", "State a suitable control for the investigation.", 2,
         ["Duplicate the experiment with all variables kept the same.", "Leave out the pondweed and the pond snail."],
         ["Use a bigger snail.", "Remove the data logger.", "Add more pondweed."], ["A control lacks what is being tested.", "Same set-up, "
                                                                                                                        "without the "
                                                                                                                        "organisms."], 1),
    stmt("2.4.3", "Account for the carbon dioxide concentration between day 0 and day 5.", 2,
         ["Carbon dioxide is released by cellular respiration.", "It is used by the pondweed in photosynthesis, so the level stays the same."],
         ["No respiration took place in the first five days.", "The snail absorbed the carbon dioxide.", "The data logger removed carbon "
                                                                                                        "dioxide."],
         ["The level stays at 5.", "One process adds CO₂, the other takes it."], 1),
    stmt("2.4.4", "Suggest a reason why carbon dioxide concentration increased after day 5.", 2,
         ["Photosynthesis could no longer take place.", "No light was available."],
         ["The snail stopped respiring.", "The pondweed photosynthesised faster in the dark.", "The data logger added carbon dioxide."],
         ["The tube was covered on day 5.", "What needs light?"], 1),
    stmt("2.4.5", "The snail died on day 10. Explain why this happened.", 2,
         ["The water lacked sufficient oxygen.", "The snail needs oxygen for cellular respiration."],
         ["The snail had too much oxygen.", "The pondweed ate the snail.", "The water became too cold."],
         ["No photosynthesis means no new oxygen.", "What does the snail need to respire?"], 1),
    stmt("2.4.6", "State a suitable conclusion for the investigation.", 2,
         ["Photosynthesis and cellular respiration are complementary processes regulating carbon dioxide in the environment.",
          "Photosynthesis removes carbon dioxide and produces oxygen.",
          "When there is no light, photosynthesis stops and carbon dioxide increases due to respiration."],
         ["Respiration removes carbon dioxide from the water.", "Light has no effect on the carbon dioxide level."],
         ["What did the experiment show about the two processes?", "Light versus dark."], 2)]

# ---- QUESTION 3, the question paper pages 13-16 and the memo pages 8-10 ----
q31 = [
    term("3.1.1(a)", "Provide a suitable label for tube A", ["oesophagus", "esophagus", "gullet"], ["From the mouth to the stomach.",
                                                                                                    "Food tube."]),
    term("3.1.1(b)", "Provide a suitable label for vein C", ["hepatic portal vein", "portal vein"], ["It carries blood from the intestine to "
                                                                                                    "the liver.", "Hepatic …"]),
    stmt("3.1.2", "Explain THREE ways structure E is adapted for its function.", 6,
         ["It is long, increasing the surface area for absorption.", "It has circular folds, increasing the surface area for absorption.",
          "It is lined with millions of villi, increasing the surface area for absorption.",
          "It is richly supplied with blood vessels, transporting nutrients from the gut to the body.",
          "It has smooth muscle tissue to move food through the gut.", "It has a mucus layer in which nutrients dissolve before they are "
                                                                       "absorbed."],
         ["It has thick walls to slow down absorption.", "It has a poor blood supply to keep nutrients in the gut."],
         ["E is the small intestine.", "Each card gives a feature and why it helps."], 2),
    sort("3.1.3", "Distinguish between the physical and chemical digestion which occur simultaneously in structure B.",
         ["Physical digestion", "Chemical digestion"],
         [("Churning movements of the stomach", 0), ("Smooth muscle contracts, mixing the bolus with gastric juices", 0),
          ("Gastric enzymes react with the surface of the food", 1), ("Insoluble large molecules are broken into soluble ones", 1)],
         ["B is the stomach.", "Physical changes size; chemical changes the molecules."]),
    stmt("3.1.4", "Explain why fat absorption is still possible, despite structure F being surgically removed.", 2,
         ["Bile is produced by the liver.", "Bile still enters the duodenum, so fat emulsification takes place."],
         ["Structure F produces bile.", "Fat is absorbed in the stomach.", "Fats need no bile at all."],
         ["F is the gall bladder: it only stores bile.", "Who makes bile?"], 1)]
q32 = [
    answer("3.2.1", "Based on the diagram above, name the phase of human nutrition shown. Also, name the enzyme responsible for breaking down "
           "proteins during this phase.", 2, ["Digestion; proteases", "Absorption; amylase", "Ingestion; lipase", "Digestion; amylase"],
           ["Protein becomes amino acids.", "Enzymes that break down proteins."]),
    term("3.2.2", "Where in the human body will the enzyme mentioned in QUESTION 3.2.1 be produced?", ["stomach"],
         ["Pepsin is one.", "An acid organ."]),
    term("3.2.3", "During which phase of human nutrition will proteins be formed in the human body?", ["assimilation"],
         ["After absorption.", "Cells use the amino acids."]),
    stmt("3.2.4", "Identify and discuss the final phase of human nutrition. Mention the structure(s) involved and their biological importance.",
         3, ["The final phase is egestion.", "In the colon most water and mineral salts are absorbed from the undigested material.",
             "Undigested material is stored in the rectum until it leaves through the anus."],
         ["The final phase is assimilation.", "Undigested food is stored in the stomach.", "Egestion takes place in the small intestine."],
         ["The last step removes what was not digested.", "Colon, rectum, anus."], 1)]
q33 = [
    stmt("3.3.1", "Bread is masticated in the human mouth. Explain the importance of mastication in human nutrition.", 2,
         ["Mastication breaks large food pieces into smaller pieces, making it easier to swallow.",
          "It increases the surface area so that digestive enzymes work more effectively."],
         ["Mastication digests proteins into amino acids.", "It absorbs glucose into the blood.", "It decreases the surface area of the food."],
         ["Mastication is chewing.", "Smaller pieces, more surface."], 1),
    stmt("3.3.2", "Explain why bread tastes sweeter after a short period of time in the mouth.", 2,
         ["Bread contains starch.", "Salivary amylase breaks starch down into maltose, which tastes sweet."],
         ["Saliva adds sugar to the bread.", "Pepsin breaks the bread into amino acids.", "The tongue turns proteins into glucose."],
         ["Saliva has an enzyme.", "Starch becomes a sugar."], 1)]
q34 = [
    term("3.4.1", "Identify the type of movement represented by A.", ["diffusion"], ["Gases move from high to low concentration.",
                                                                                     "Passive."]),
    stmt("3.4.2", "Identify and describe TWO visible features of the alveolus that make it an effective gaseous exchange surface.", 4,
         ["A mucus layer inside the alveolus lets O₂ and CO₂ dissolve as diffusion occurs.",
          "The alveolus wall is one squamous cell thick, so gases diffuse easily.", "The capillary wall is one cell thick, so gases diffuse "
                                                                                     "easily.",
          "It is richly supplied with blood vessels, for efficient gaseous exchange."],
         ["The alveolus has thick walls that store oxygen.", "The alveolus has few blood vessels."],
         ["Thin, moist, and close to blood.", "Each card gives a feature and why it helps."], 2),
    stmt("3.4.3", "List TWO ways in which oxygen is transported in the body.", 2, ["As oxyhaemoglobin", "Dissolved in the blood plasma"],
         ["As carbaminohaemoglobin in the lymph", "Stored in the alveoli", "Bound to glucose"], ["Red blood cells and plasma.",
                                                                                                "Haemoglobin carries most."], 1),
    stmt("3.4.4", "Describe how a bullet wound to the chest could affect effective ventilation of the lungs.", 5,
         ["Blood would move into the lung (the alveoli).", "This limits efficient gaseous exchange.",
          "Pressure would no longer be regulated and the lung would collapse.", "This impedes inhalation and exhalation, which need pressure "
                                                                                 "changes.",
          "Lung tissue, alveoli or bronchioles would be damaged.", "This limits the gas pathways through the lung."],
         ["The lungs would inflate more easily.", "More oxygen would reach the blood."], ["A hole lets air and blood in.", "Breathing needs "
                                                                                                                         "pressure changes."],
         1)]
q35 = [
    {"t": "pickn", "n": "3.5.1", "marks": 2, "q": "List TWO letters from the nephron diagram that are located in the renal cortex.",
     "clues": ["The cortex holds the capsule and the coiled tubules.", "The loop dips into the medulla."], "opts": LET6, "pool": [0, 1, 2],
     "count": 2},
    stmt("3.5.2", "Identify and discuss TWO significant processes which occur between the renal tubule and network F.", 4,
         ["Tubular reabsorption: useful solutes and water move from the renal tubule back into network F.",
          "Tubular secretion: waste products and toxins move from F into the renal tubule."],
         ["Ultrafiltration: blood is filtered from F into the collecting duct.", "Tubular secretion: glucose moves from the tubule into F.",
          "Deamination: amino acids are broken down in F."], ["F is the capillary network round the tubule.", "Into the blood, and out of "
                                                                                                             "it."], 2),
    ln("3.5.3(a)", "Bartter syndrome is a rare genetic disorder which causes ineffective reabsorption of sodium ions, despite aldosterone's "
       "secretion. Sodium pumps are also unable to actively pump sodium out. Identify and write down the name of the part Bartter syndrome "
       "will most likely affect.", LET6, "D", ["ascending limb of Henle", "ascending limb of the loop of Henle", "loop of Henle"],
       ["Where is sodium pumped out?", "The loop's rising side."]),
    stmt("3.5.3(b)", "Discuss how Bartter syndrome will negatively affect osmoregulation.", 5,
         ["The renal medulla will no longer be hypertonic in sodium.", "No osmotic (water potential) gradient is created.",
          "There is no gradient between the filtrate and the medulla's tissue fluid.", "Less water is drawn into the renal medulla.",
          "Less water is reabsorbed back into the blood."],
         ["The medulla becomes more hypertonic.", "More water is reabsorbed into the blood.", "Aldosterone stops being secreted."],
         ["Salt in the medulla pulls water out of the tubules.", "No salt, no pull."], 1)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 8,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 8,
     "lead": "Indicate whether each description in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "The kidney", "marks": 7, "lead": "A macroscopic diagram of the kidney is shown below.",
     "figure": P.fig("1.4", "A kidney cut lengthways: A points into a pale cone-shaped region inside, D to the dark outer band, B to the "
                            "outer covering, F to a cup at the tip of a cone, C to the funnel in the middle and E to the tube leaving it."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Homeostasis", "marks": 7,
     "lead": "Negative feedback mechanisms are essential processes which ensure homeostasis. A simple negative feedback loop with its components "
             "is shown below.",
     "figure": P.fig("1.5", "A loop: Stimulus / Imbalance → Receptor → Control Center → Effector → Restore Homeostasis, and back."),
     "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Photosynthesis", "marks": 12, "lead": "Study the organelle below that is found in a cell.",
     "figure": P.fig("2.1", "An oval organelle in section with stacks of discs inside: A points to the fluid between the stacks, B to a stack."),
     "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Greenhouses", "marks": 13,
     "lead": "GREENHOUSES HELP GROW FOOD EVEN WHEN THE WEATHER IS UNFAVOURABLE\nIn Russia, winters are very cold and the time for growing food "
             "is short. Greenhouses give a safe and warm space for growing vegetables all year round, even when it is −25 °C outside. In places "
             "like Siberia, people can now grow local vegetables instead of buying them from other countries. Russian greenhouses use clean "
             "energy from the sun (solar) and the earth (geothermal). Greenhouses also help people get jobs and support local businesses.",
     "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Cellular respiration", "marks": 14,
     "lead": "Cellular respiration is a 3-phase process in which ATP is formed. A schematic representation of this process is given below.",
     "figure": P.fig("2.3", "Process A makes ATP and passes electrons via NADH; a mitochondrion runs the Krebs cycle and process B, which "
                            "takes in X and gives out Y, each making ATP."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Investigation", "marks": 11, "table": CO2,
     "lead": "A scientist investigated how photosynthesis and respiration affect carbon dioxide levels in water. The experiment used pondweed "
             "(a plant) and a pond snail (an animal). Experimental design:\n• The apparatus was left in a well-lit room for 5 days.\n• After 5 "
             "days, the scientist completely covered the boiling tube with black paper.\n• A data logger was used to record carbon dioxide "
             "(CO₂) levels every day for 15 days.\n• The results are shown in the table below.",
     "figure": P.fig("2.4", "A boiling tube of water with a pondweed and a pond snail, closed with a rubber plug through which a data logger "
                            "probe reaches the water."), "items": q24},
    {"id": "3.1", "title": "Question 3.1", "kind": "Digestion", "marks": 14, "lead": "Below is a diagram of some parts of the digestive system.",
     "figure": P.fig("3.1", "Part of the digestive system: tube A leading down to B, the stomach; C a vein from the intestines to the liver; "
                            "D the wide intestine on the right; E the coiled intestine in the middle; F a small sac under the liver."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Human nutrition", "marks": 7,
     "lead": "The diagram below shows one of the five phases of human nutrition.",
     "figure": P.fig("3.2", "A long folded chain labelled Protein becomes a short chain labelled Peptide, which becomes single beads labelled "
                            "Amino Acids."), "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Mastication", "marks": 4, "lead": "Bread is masticated in the human mouth.", "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Gaseous exchange", "marks": 12,
     "lead": "The diagram below shows an alveolus, a small, hollow, air-filled sac located in the lungs.",
     "figure": P.fig("3.4", "An alveolus wrapped in a capillary: arrows marked A carry gases across the alveolus wall and the capillary wall."),
     "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "The nephron", "marks": 13, "lead": "The diagram below shows a nephron.",
     "figure": P.fig("3.5", "A nephron: A the cup at its start, B and C the coiled tubules near the top, D the rising side of the loop, E the "
                            "wide duct on the right, and F the network of capillaries round the tubule."), "items": q35},
]
P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2025", "total_marks": 150, "time": "2½ hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.1.3", "kind": "no_fit", "detail": "Tabulated differences (2.1.3) and the physical/chemical distinction (3.1.3) play as a sort "
                                                     "into columns, one mark a row; the memo's table mark is the sort's own layout (Grade 12 "
                                                     "precedent: LS P2 Nov 2024 3.4.3)."},
          {"n": "3.5.1", "kind": "no_fit", "detail": "Two letters of the cortex: the six letters as cards, any two of A, B and C, one mark each."},
          {"n": "2.4.5", "kind": "no_fit", "detail": "The memo's compulsory point (too little oxygen) is one of the two right cards and both are "
                                                     "needed; its third point (the water became too acidic) is left out."},
          {"n": "paper", "kind": "low_confidence", "detail": "The question paper prints TOTAL SECTION B: 50 on its last page; Questions 2 and 3 "
                                                             "are 50 each and the memo's total is 100."}],
         {"1": 50, "2": 50, "3": 50}, 150,
         {}, "Questions 1 to 3 (the whole paper)")
