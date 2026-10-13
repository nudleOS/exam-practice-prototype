"""Grade 10 Life Sciences P1 November 2024 (North West Department of Education, provincial assessment), the whole paper
(Questions 1 to 3, 150 marks, 2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`.
Stems, options, marks and answers are the paper's and the memo's own; clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment, the question paper PDF (English, 16 pages, text layer;
its diagrams are images) and the marking guidelines PDF (English, 11 pages), read from their text and page images (100 dpi).

  python tools/ingest/transcribe_g10_ls_p1_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ls-p1-2024-11-nw/22-November-2024-S2-Gr10-Life-Sciences-QP-P1-ENG.pdf" "uploads/provincial/g10-ls-p1-2024-11-nw/22-November-2024-S2-Gr10-Life-Sciences-MG-P1-ENG.pdf" --id g10-ls-p1-2024-11-nw --from-json

The Life Sciences rulings, as in transcribe_g11_ls_p1_2024_11_ec.py: printed multiple choice as printed; terms typed; Column I /
Column II as A only / B only / both / none; a LETTER an MCQ of the diagram's letters; a written answer as statements to pick (the
memo's points and clearly wrong ones); the one calculation (1.4.5) as four workings; the tabulated differences (3.4.4) as a sort;
the drawings (2.6.3, the root hair; 3.3.3, the bar graph) as pick the drawing (pictures_lower.py: root_hair, bars2). The survey
table (3.3) is typed. 3.5.3 prints "the tissue mentioned in QUESTION 3.6.2"; it means 3.5.2, and says so here.
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ls-p1-2024-11-nw", 595.32, 842.04, {
    "1.4": [6, 150, 110, 480, 410], "1.5": [7, 65, 110, 495, 333], "2.1": [8, 133, 258, 494, 418], "2.2": [9, 189, 110, 436, 297],
    "2.4": [10, 135, 456, 529, 611], "2.5": [11, 105, 291, 520, 510], "2.6": [12, 92, 110, 519, 307], "3.1": [13, 141, 133, 493, 314],
    "3.2": [13, 131, 533, 504, 681], "3.4": [15, 135, 118, 518, 308], "3.5": [16, 130, 110, 544, 285]}, start=3)
work, answer, num, draw, stmt, mcq, term, sort = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term, P.sort
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
let = lambda n, q, letters, a, clues: mcq(n, q, letters, letters.index(a), clues, marks=1)
CELL, MIT = list("ABCDEFG"), list("ABCDE")

# ---- SECTION A, QUESTION 1, the question paper pages 3-7 and the memo pages 4-5 ----
q11 = [
    mcq("1.1.1", "Which of the following cells make up a xylem tissue?", ["Xylem vessels and tracheids", "Sieve tubes and companion cells",
        "Tracheids and sieve tubes", "Companion cells and xylem vessels"], 0, ["Xylem carries water.", "Sieve tubes belong to the phloem."]),
    mcq("1.1.2", "Which of the following is the site of protein synthesis?", ["Golgi body", "Cell wall", "Ribosomes", "Plasma membrane"], 2,
        ["Amino acids are joined here.", "They are the smallest organelles, on the ER or free."]),
    mcq("1.1.3", "The similarity between sclerenchyma and collenchyma tissue is that they are both …",
        ["packaging tissue.", "contain flexible fibres.", "provide support to the plant.", "manufacture food."], 2,
        ["Both have thickened cell walls.", "What do thick walls do for a plant?"]),
    mcq("1.1.4", "A motor neuron carries a nerve impulse to …", ["a receptor.", "an effector.", "the brain.", "the cell body."], 1,
        ["Motor neurons make muscles move.", "Muscles and glands are effectors."]),
    mcq("1.1.5", "Which bone does not belong to the upper limb?", ["Carpals", "Metacarpals", "Ulna", "Fibula"], 3,
        ["The upper limb is the arm and hand.", "Which bone is in the lower leg?"]),
    mcq("1.1.6", "Kwashiorkor is a deficiency disease of …", ["proteins.", "vitamin A.", "vitamin B.", "fats/lipids."], 0,
        ["Children with kwashiorkor have swollen bellies.", "Which nutrient builds the body?"]),
    mcq("1.1.7", "Which organelle contains the genetic information of an organism?", ["Chloroplast", "Mitochondrion", "Nucleus",
        "Centrosome"], 2, ["The chromosomes are found here.", "It controls the cell's activities."]),
    mcq("1.1.8", "Cells in a leaf that do not contain chloroplasts.", ["Guard cells", "Sclerenchyma cells", "Palisade cells",
        "Parenchyma cells"], 1, ["Which cells are dead when mature?", "Their thick walls give support."]),
    mcq("1.1.9", "The tissue that allows sunlight to pass through into a leaf.", ["Palisade mesophyll", "Epidermis", "Collenchyma",
        "Epithelium"], 1, ["It is the outer layer of the leaf.", "Its cells are transparent."]),
    mcq("1.1.10", "An organelle that generates spindle fibres in an animal cell during mitosis.", ["Cytoplasm", "Chromosome", "Centromere",
        "Centriole"], 3, ["It is found only in animal cells.", "Two of them move to the poles."])]
q12 = [
    term("1.2.1", "The tissue which lines all blood vessels", ["endothelium", "endothelial tissue"],
         ["It is a thin layer of flat cells.", "Its name starts with 'endo-'."]),
    term("1.2.2", "The tissue which continually forms new cells in plants", ["meristematic tissue", "meristematic", "meristem", "cambium"],
         ["It is found at root and shoot tips.", "Its cells divide by mitosis all the time."]),
    term("1.2.3", "The element needed to form haemoglobin", ["iron", "fe"], ["A lack of it causes anaemia.", "It is a metal."]),
    term("1.2.4", "The structure that joins two chromatids of a chromosome together during cell division", ["centromere"],
         ["It holds the two chromatids at one point.", "Not the centriole."]),
    term("1.2.5", "The tissue that transports food from leaves to all parts of the plant", ["phloem"],
         ["It has sieve tubes and companion cells.", "Not the xylem."])]
q13 = [
    abq("1.3.1", "A differentially permeable membrane", "Cell membrane", "Cell wall", 0,
        ["Which one lets some substances through and not others?", "The cell wall is fully permeable."]),
    abq("1.3.2", "Gives colour to the flower", "Leucoplast", "Chromoplast", 1, ["'Chromo' means colour.", "Leucoplasts are colourless."]),
    abq("1.3.3", "Upward movement of water in a plant due to transpiration", "Force of cohesion", "Transpiration pull", 2,
        ["Water molecules stick together.", "Transpiration pulls the column of water up."])]
q14 = [
    term("1.4.1", "Name the above instrument.", ["microscope", "light microscope", "compound microscope", "compound light microscope"],
         ["It magnifies small objects.", "It has lenses and a stage."]),
    term("1.4.2(a)", "Identify part A", ["eyepiece", "eyepiece lens", "ocular lens", "ocular"], ["You look through it.", "It is at the top."]),
    term("1.4.2(b)", "Identify part B", ["coarse adjustment knob", "coarse adjustment", "coarse focus knob", "coarse focusing knob"],
         ["It is the large knob on the arm.", "It moves the lenses or stage a long way."]),
    term("1.4.2(c)", "Identify part D", ["stage"], ["The slide is placed on it.", "It has a hole for light."]),
    stmt("1.4.3", "Give the function of the part labelled C.", 1,
         ["The objective lens magnifies the object.", "It enlarges the image of the specimen."],
         ["It holds the slide in place.", "It lets light pass up to the specimen.", "It moves the stage up and down."],
         ["C is a lens just above the stage.", "What do lenses do?"], 1),
    stmt("1.4.4", "What is meant by magnification of a microscope?", 1,
         ["Enlarging the apparent size of an object, not its physical size.", "How many times bigger the image appears than the object."],
         ["How clearly two points close together can be seen apart.", "Making the object physically bigger.",
          "The brightness of the image."],
         ["Does the object itself change?", "It is about how big the image looks."], 1),
    work("1.4.5", "Calculate the actual size of a cell in micrometres using the information and formula below:\nWidth of a cell = 50 mm\n"
         "True length of scale line = 0,9 µm\nMeasured scale line = 8\nActual size = (measured size × true length of scale line) ÷ "
         "measured length of scale line", 3, [
        "Actual size = {measured size × true length}/{measured length of scale line}\n= {50 × 0,9}/{8}\n= 5,63 µm",     # the memo's working
        "Actual size = {measured size × measured length}/{true length}\n= {50 × 8}/{0,9}\n= 444,44 µm",                # the scale lengths swapped
        "Actual size = {measured length × true length}/{measured size}\n= {8 × 0,9}/{50}\n= 0,14 µm",                  # 8 and 50 swapped
        "Actual size = {measured size + true length}/{measured length of scale line}\n= {50 + 0,9}/{8}\n= 6,36 µm"],    # added, not multiplied
        ["Put the measured size and the two scale-line lengths into the formula.", "Multiply first, then divide by 8."])]
q15 = [
    let("1.5.1(a)", "Write down the LETTER only of the vacuole.", CELL, "D", ["It is a large sac of cell sap.", "It has no inner structure."]),
    let("1.5.1(b)", "Write down the LETTER only of the endoplasmic reticulum.", CELL, "B",
        ["It is a folded system of membranes.", "It lies next to the nucleus."]),
    let("1.5.1(c)", "Write down the LETTER only of the nucleus.", CELL, "A", ["It holds the chromosomes.", "Look for the bracket."]),
    let("1.5.2(a)", "Write down the LETTER of the organelle that supports and protects the living contents of the cell and gives rigidity to "
        "the cell.", CELL, "G", ["It is the outermost layer.", "Only plant cells have it."]),
    let("1.5.2(b)", "Write down the LETTER of the part that is the site of all metabolic processes.", CELL, "F",
        ["It is the jelly-like fluid filling the cell.", "The organelles float in it."]),
    let("1.5.2(c)", "Write down the LETTER of the organelle that provides the energy to the cell through cellular respiration.", CELL, "E",
        ["It is the powerhouse of the cell.", "Look for an organelle with folded inner membranes."]),
    stmt("1.5.3", "Provide ONE observable reason why this cell cannot be from the root of a plant.", 1,
         ["It contains chloroplasts.", "It has organelles that make food by photosynthesis."],
         ["It has a cell wall.", "It has a large vacuole.", "It has a nucleus.", "It has mitochondria."],
         ["Root cells grow underground, in the dark.", "Which organelle needs light?"], 1),
    stmt("1.5.4", "Explain ONE observation that you would make if this cell was placed in a concentrated sugar solution.", 3,
         ["The cell membrane will pull away from the cell wall: the cell plasmolyses.", "Water leaves the cell by osmosis.",
          "Water moves into the concentrated sugar solution, down the concentration gradient."],
         ["The cell will swell and burst.", "Sugar moves into the cell by osmosis.", "Water moves into the cell from the sugar solution."],
         ["Where is the water concentration higher: inside the cell or in the sugar solution?", "What happens to the vacuole and the "
                                                                                              "membrane as water leaves?"], 1)]

# ---- SECTION B, QUESTION 2, the question paper pages 8-12 and the memo pages 6-8 ----
q21 = [
    stmt("2.1.1", "Define an organic compound.", 2,
         ["A compound that contains carbon combined with hydrogen and oxygen.",
          "A compound containing carbon bonded to other elements such as hydrogen, oxygen and nitrogen."],
         ["A compound that contains no carbon.", "A compound made only of minerals such as calcium and iron.", "A compound found only in "
                                                                                                               "plants.",
          "Any compound that contains water."],
         ["Which element do all organic compounds contain?", "Water and minerals are inorganic."], 2),
    term("2.1.2(a)", "Name the organic compound A", ["carbohydrates", "carbohydrate"], ["A is not part of the cell membrane.",
                                                                                       "It is stored as glycogen and starch."]),
    term("2.1.2(b)", "Name the organic compound B", ["lipids", "lipid", "fats", "fat"], ["B and C make up the cell membrane.",
                                                                                        "B is made of fatty acids and glycerol."]),
    term("2.1.2(c)", "Name the organic compound C", ["proteins", "protein"], ["C is made of amino acids.", "Enzymes are made of it."]),
    term("2.1.3(a)", "Name the monomers of carbohydrates", ["monosaccharides", "monosaccharide", "simple sugars", "saccharides"],
         ["Glucose is one.", "'Mono' means one."]),
    term("2.1.3(b)", "Name the monomers of lipids", ["fatty acids and glycerol", "glycerol and fatty acids", "fatty acid and glycerol"],
         ["There are two kinds.", "Three of one join to one of the other."]),
    mcq("2.1.4", "Which organic compound (A, B or C) is stored as glycogen in the liver of humans?", ["A", "B", "C"], 0,
        ["Glycogen is a polysaccharide.", "Which compound is a carbohydrate?"], marks=1)]
q22 = [
    term("2.2.1", "Identify the phase of mitosis represented in the above diagram.", ["prophase", "late prophase"],
         ["The nuclear membrane is breaking down.", "The chromosomes are not yet in a line."]),
    let("2.2.2(a)", "Write down the LETTER only of the part that represents the nucleolus.", MIT, "A",
        ["It is a dark spot inside the nucleus.", "It disappears in prophase."]),
    let("2.2.2(b)", "Write down the LETTER only of the part that represents the nucleoplasm.", MIT, "E",
        ["It is the fluid inside the nucleus.", "Look inside the dashed membrane."]),
    term("2.2.3(a)", "Identify part D", ["chromatid", "chromatids"], ["Each chromosome has two of them.", "They are joined at the centromere."]),
    term("2.2.3(b)", "Identify part C", ["cytoplasm", "cytosol"], ["It is outside the nucleus.", "It fills the cell."]),
    stmt("2.2.4", "Explain the importance of interphase that occurs before mitosis.", 2,
         ["DNA replication occurs.", "The genetic material is doubled.", "So that each cell after mitosis has identical genetic material."],
         ["The chromosomes line up at the equator.", "The nuclear membrane disappears.", "The cytoplasm divides into two."],
         ["What must happen to the DNA before a cell divides?", "Each new cell needs a full set."], 1),
    num("2.2.5", "How many chromosomes would you expect in each of the daughter cells after mitosis?", 4, 0, "",
        ["Count the chromosomes in the diagram.", "Mitosis keeps the chromosome number the same."])]
q23 = [
    term("2.3.1", "According to the extract, name ONE method used in hospitals to treat cancer.", ["chemotherapy", "radiotherapy"],
         ["Hospitals use two methods in the extract.", "Traditional healers use a plant."]),
    term("2.3.2", "Identify the genus name of the plant used by traditional healers.", ["sutherlandia"],
         ["A scientific name has two words.", "The genus is the first word."]),
    stmt("2.3.3", "Explain how 'destroying the DNA' can help fight cancer.", 2,
         ["There will be no DNA replication.", "So there is no mitosis: the cancer cells cannot divide."],
         ["The DNA makes the cells divide faster.", "Destroying the DNA makes the cancer cells bigger.",
          "The DNA is turned into proteins that kill the cells."],
         ["Cancer cells divide out of control.", "What must a cell copy before it can divide?"], 1),
    stmt("2.3.4", "State TWO ways in which the scientists can improve the reliability of the results obtained in the test with vervet monkeys.",
         2, ["Repeat the investigation.", "Increase the number of monkeys (use more than 10)."],
         ["Use only one monkey.", "Use a different extract for each monkey.", "Do the test once only.", "Stop recording the results."],
         ["Reliability comes from repeating.", "Is 10 monkeys a big sample?"], 1)]
q24 = [
    term("2.4.1", "Provide the caption for the above diagram.", ["sensory neuron", "a sensory neuron", "unipolar neuron", "sensory"],
         ["The cell body is on a side branch.", "This neuron carries impulses from a receptor."]),
    term("2.4.2(a)", "From the diagram, identify a structure that provides nutrients and energy to the impulse", ["cell body", "cyton"],
         ["It contains the nucleus.", "It is the round part."]),
    term("2.4.2(b)", "From the diagram, identify a structure that receives and transmits impulses to the cell body",
         ["dendrites", "dendrite", "motor end plate"], ["They are the branched ends.", "They carry impulses towards the cell body."]),
    stmt("2.4.3", "Describe the functional difference between the motor neuron and the sensory neuron.", 2,
         ["A sensory neuron conducts impulses from the receptors to the central nervous system.",
          "A motor neuron conducts impulses from the central nervous system to the effectors (muscles and glands)."],
         ["A sensory neuron conducts impulses from the central nervous system to the muscles.",
          "A motor neuron conducts impulses from the sense organs to the brain.", "Both neurons carry impulses only within the brain."],
         ["Which neuron starts at a sense organ?", "Which one ends at a muscle?"], 1)]
q25 = [
    stmt("2.5.1", "State TWO planning steps that were taken for this investigation.", 2,
         ["Decide on the time to do the investigation.", "Decide on the place to do the investigation.",
          "Decide on the recording tool to use.", "Decide on the type of shirts to use."],
         ["Record the results in a table.", "Repeat the investigation five times.", "Draw a conclusion."],
         ["Planning happens before the investigation starts.", "Doing and recording are not planning."], 1),
    stmt("2.5.2", "State TWO factors that were kept constant during this investigation.", 2,
         ["The type of shirt.", "The type of detergent.", "The washing time (3 minutes)."],
         ["The temperature of the water.", "The amount of fat stain removed.", "The colour of the stain after washing."],
         ["What was the same for shirts X and Y?", "The temperature was changed on purpose."], 1),
    stmt("2.5.3", "Why was the white shirt X included in this investigation?", 2,
         ["It serves as a control, to compare the results.", "It shows what happens at 37 °C, for comparison with boiling water."],
         ["To make the investigation take longer.", "To test a different detergent.", "Because shirt Y was dirtier.",
          "To measure the boiling point of water."],
         ["Shirt X was washed at a normal temperature.", "What is a control for?"], 2),
    stmt("2.5.4", "State a conclusion for this investigation.", 2,
         ["The high temperature of boiling water affects (reduces) the activity of the fat-digesting enzymes.",
          "The boiling water denatured the fat-digesting enzymes, so the fat stain was not removed."],
         ["High temperature increases the activity of the fat-digesting enzymes.", "Temperature has no effect on fat-digesting enzymes.",
          "The detergent works better in boiling water.", "Shirt X was not cleaned at 37 °C."],
         ["Which shirt still has the fat stain?", "What happens to enzymes at high temperatures?"], 2)]
q26 = [
    term("2.6.1(B)", "Identify tissue B", ["parenchyma"], ["Thin-walled, round cells with spaces between them.", "It is a packing tissue."]),
    term("2.6.1(C)", "Identify tissue C", ["collenchyma"], ["The walls are thickened at the corners.", "It supports young stems."]),
    stmt("2.6.2", "Explain TWO structural adaptations of tissue A for its functions.", 4,
         ["The epidermal cells are transparent, to let sunlight into the leaf for photosynthesis.",
          "The cells are closely packed, to protect the cells underneath.", "A cuticle covers the cells, to reduce water loss.",
          "Guard cells with stomata allow gaseous exchange."],
         ["The cells contain many chloroplasts, to absorb water.", "The cells have thick lignified walls, to transport water.",
          "The cells are loosely packed, to let water evaporate faster."],
         ["Tissue A is the epidermis with a stoma.", "Each adaptation: the structure, then what it does."], 2),
    draw("2.6.3", "Tissue A also lines the root where it plays a role in increasing the surface area for absorption of water. Draw a labelled "
         "diagram of a root hair.", 3, [["Caption", 1], ["Correct drawing", 1], ["Correct labels (any one)", 1]],
         ["A root hair is one epidermal cell with a long outgrowth.", "Label it and give it a caption."],
         memo="The memo's diagram: an epidermal cell with a long outgrowth, labelled cell wall, cell membrane, nucleus, vacuole and cytosol, "
              "captioned 'Structure of the root hair'."),
    stmt("2.6.4", "Explain TWO ways in which the root hair is adapted for its function.", 4,
         ["It is a long, tube-like outgrowth of the epidermis, to increase the surface area for absorbing water and nutrients.",
          "It contains mitochondria, which release energy for active transport.",
          "It has a large vacuole with a lower water potential in the cell sap than the soil water.",
          "It has a thin cell wall without a cuticle, to maximise water movement into the root."],
         ["It has a thick cuticle, to stop water entering.", "It contains chloroplasts, to make food.",
          "It is short and round, to reduce the surface area."],
         ["What does a root hair absorb?", "Each adaptation: the structure, then how it helps."], 2),
    stmt("2.6.5", "Explain why a high temperature in the soil will increase the absorption of water by the root hair.", 2,
         ["Water molecules have more kinetic energy at a higher temperature.", "So they move into the root hair more readily."],
         ["The root hair cell dies in hot soil and lets water in.", "High temperature closes the stomata.",
          "Hot water is thicker and flows faster."],
         ["How does temperature change how fast molecules move?", "Faster molecules diffuse faster."], 1)]

# ---- SECTION B, QUESTION 3, the question paper pages 13-16 and the memo pages 9-11 ----
SURVEY = {"head": ["AGE GROUP (years)", "MEN: FREQUENCY OF OSTEOPOROSIS (%)", "WOMEN: FREQUENCY OF OSTEOPOROSIS (%)"],
          "rows": [["20-35", "0", "2"], ["36-50", "2", "5"], ["51-65", "8", "25"], ["65-80", "26", "35"]]}
q31 = [
    term("3.1.1", "To which of the two main parts of the skeleton do these structures belong?", ["axial skeleton", "axial", "the axial skeleton"],
         ["The skeleton has an axial and an appendicular part.", "The skull is along the body's axis."]),
    term("3.1.2", "Identify the opening marked X.", ["foramen magnum"], ["The spinal cord passes through it.", "It is the largest opening."]),
    term("3.1.3", "With which vertebra does this part of the skeleton articulate?", ["atlas", "atlas vertebra", "first cervical vertebra"],
         ["It is the first vertebra of the neck.", "It holds up the skull, as Atlas held the world."]),
    answer("3.1.4", "Write down the dental formula of a human.", 1, ["2:1:2:3", "2:1:2:2", "2:1:3:3", "3:1:4:3"],
           ["Count incisors, canines, premolars, molars in half a jaw.", "Adults have 32 teeth."]),
    num("3.1.5", "How many teeth does an adult human have in the upper jaw?", 16, 0, "",
        ["An adult has 32 teeth.", "Half of them are in the upper jaw."]),
    stmt("3.1.6", "What is determined by an animal's dental formula?", 2,
         ["The number of teeth.", "The type of teeth.", "The arrangement of the teeth."],
         ["The colour of the teeth.", "The age of the animal.", "The size of the skull."],
         ["A dental formula counts the teeth of each type.", "In what order are they?"], 1)]
q32 = [
    term("3.2.1(A)", "Identify the type of joint A according to the movement it permits", ["pivot", "pivot joint"],
         ["One bone turns around another.", "The head says 'no'."]),
    term("3.2.1(B)", "Identify the type of joint B according to the movement it permits", ["hinge", "hinge joint"],
         ["It bends in one direction only.", "Like a door."]),
    term("3.2.1(C)", "Identify the type of joint C according to the movement it permits", ["gliding", "gliding joint", "sliding",
                                                                                            "sliding joint"],
         ["The small bones of the wrist slide over each other.", "Not a ball and socket."]),
    stmt("3.2.2", "State THREE functions of the skeleton other than giving protection.", 3,
         ["Support.", "Movement.", "Hearing.", "Storage of minerals."],
         ["Digestion of food.", "Pumping blood.", "Producing hormones such as insulin."],
         ["What would the body be like without bones?", "The ear has tiny bones."], 1)]
q33 = [
    term("3.3.1(a)", "Identify the dependent variable", ["frequency of osteoporosis", "the frequency of osteoporosis",
                                                         "percentage of osteoporosis"],
         ["It is what was measured.", "It depends on the age group."]),
    answer("3.3.1(b)", "Identify the age group with the lowest frequency of osteoporosis", 1,
           ["20-35 years", "65-80 years", "36-50 years", "51-65 years"], ["Look for the smallest percentages.", "Young bones are strong."]),
    mcq("3.3.2", "Which gender shows the higher frequency of osteoporosis?", ["Men", "Women"], 1,
        ["Compare the two columns.", "Which has the larger numbers?"], marks=1),
    draw("3.3.3", "Draw a bar graph to show the results of the survey.", 6, [
        ["Caption", 1], ["Correct type of graph (bar graph)", 1], ["Labels on both axes", 1], ["Correct scale on both axes", 1],
        ["Plotting: all sets plotted correctly", 2]],
        ["Two bars for each age group: men and women.", "Add a key, a caption and labels with units."],
        memo="The memo's rubric: caption, a bar graph, both axes labelled, the right scale, and all the sets plotted correctly.")]
q34 = [
    answer("3.4.1(a)", "Give the numbers which will indicate open stomata", 2, ["1 and 4", "2 and 3", "1 and 2", "3 and 4"],
           ["Open stomata let water vapour out.", "Where is the transpiration rate rising?"]),
    answer("3.4.1(b)", "Give the numbers which will indicate closed stomata", 2, ["2 and 3", "1 and 4", "1 and 3", "2 and 4"],
           ["Closed stomata stop transpiration.", "Which points are at night?"]),
    stmt("3.4.2", "Mention any ONE environmental condition in the guard cells responsible for the changes at 2.", 1,
         ["Temperature.", "Light intensity."], ["The colour of the leaf.", "The number of roots.", "The size of the flower."],
         ["Point 2 is at 18:00.", "What changes when the sun sets?"], 1),
    stmt("3.4.3", "Explain TWO structural adaptations of leaves to limit transpiration.", 4,
         ["The leaves are small, to reduce the surface area for evaporation.",
          "The stomata occur in the lower epidermis, away from direct sunlight.",
          "Sunken stomata reduce the diffusion gradient between the leaf and the outside air.", "Hairs on the leaf trap water vapour.",
          "A thick cuticle lowers transpiration."],
         ["The leaves are large and flat, to catch more wind.", "There are many stomata on the upper surface.",
          "The cuticle is thin, to let water out."],
         ["Water vapour leaves through the stomata.", "Each adaptation: the structure, then how it limits water loss."], 2),
    sort("3.4.4", "Tabulate TWO structural differences between a dicotyledonous root and a dicotyledonous stem.",
         ["Dicotyledonous root", "Dicotyledonous stem"],
         [("Xylem and phloem occur in a central stele", 0),
          ("Xylem and phloem occur in vascular bundles", 1),
          ("Xylem alternates with phloem (a cross of xylem with phloem between its arms)", 0),
          ("The vascular bundles are arranged in a circle", 1),
          ("Root hairs are present", 0)],
         ["Where are the xylem and phloem in a root, and in a stem?", "Which organ has root hairs?"])]
q35 = [
    stmt("3.5.1", "Explain ONE visible structural adaptation that assists the plant to prevent water loss.", 3,
         ["Tissue A is covered by a cuticle.", "The cuticle is a waxy layer.", "The cuticle is waterproof, so it keeps water in."],
         ["The leaf has many stomata on top.", "The root hair is long.", "The cells are loosely packed."],
         ["Look at the top layer of the leaf.", "What covers it?"], 1),
    term("3.5.2", "Name the tissue that transports water from the root to reach the leaf.", ["xylem"],
         ["It is part of the vascular bundle (tissue B).", "Not the phloem."]),
    stmt("3.5.3", "Explain TWO ways how the tissue mentioned in QUESTION 3.5.2 is structurally adapted to perform its function efficiently.", 4,
         ["The cross walls are perforated, to form continuous tubes for the movement of water.",
          "Xylem vessels have no cell contents (they are dead and hollow), so water flows freely.",
          "The walls are strengthened with lignin, so they do not collapse under the pull of transpiration.",
          "The walls have pits, to allow sideways movement of water.",
          "They are long and cylindrical, to allow continuous movement of water."],
         ["They contain many chloroplasts, to make food.", "They have sieve plates and companion cells.",
          "Their walls are thin and flexible, so they bend in the wind."],
         ["What must a tube that carries water look like?", "Each adaptation: the structure, then how it helps."], 2),
    term("3.5.4", "Name the process for which tissue A is responsible.", ["photosynthesis"],
         ["Tissue A is the palisade layer.", "Its cells are full of chloroplasts."]),
    term("3.5.5", "Name the process which causes water to move from one parenchyma cell to another, as it passes through the cortex of the root.",
         ["osmosis", "root pressure", "transpiration pull", "transpiration"], ["Water moves from cell to cell.", "Down a water potential "
                                                                                                                 "gradient."])]
q36 = [
    stmt("3.6", "Explain any TWO precautions you would take when measuring the rate of transpiration using a potometer.", 4,
         ["Cut the stem of the plant under water, to prevent air from entering the xylem.",
          "Apply petroleum jelly (Vaseline), to make the potometer airtight.",
          "Cut the stem at an angle, to expose more of the xylem for water absorption."],
         ["Keep the plant in the dark.", "Leave an air bubble in the stem.", "Cut the stem in the air, above the water.",
          "Use a plant with no leaves."],
         ["Air in the xylem stops water moving up.", "The apparatus must not leak."], 2)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 20, "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 5,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 6,
     "lead": "Indicate whether each of the descriptions in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "The microscope", "marks": 9, "lead": "The diagram below shows a scientific instrument.",
     "figure": P.fig("1.4", "A microscope: A points to the eyepiece at the top of the tube, B to the large knob on the arm, C to a lens just "
                            "above the stage, and D to the flat stage."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "The cell", "marks": 10, "lead": "Study the diagram of a cell shown below.",
     "figure": P.fig("1.5", "A plant cell with letters A to G: A the nucleus (bracketed), B a folded membrane system beside it, C and E oval "
                            "organelles with inner folds or stripes, D a round sac, F the cytoplasm and G the outer boundary."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Organic compounds", "marks": 8,
     "lead": "In the diagram below the letters A, B and C represent THREE groups of organic compounds.\n• Number 1 represents characteristics "
             "common to A and B only.\n• Number 2 represents characteristics common to B and C only.\n• B and C make up a cell membrane.\n"
             "• C is made up of amino acids.",
     "figure": P.fig("2.1", "Three overlapping circles in a row, A, B and C: 1 where A and B overlap, 2 where B and C overlap."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Mitosis", "marks": 8, "lead": "The diagram below shows a phase of mitosis.",
     "figure": P.fig("2.2", "A cell in mitosis: spindle fibres from the two poles, a dashed nuclear membrane, four chromosomes inside it, "
                            "labels A to E."), "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Cancer", "marks": 6,
     "lead": "Read the extract below about the treatment of cancer.\nChemotherapy either destroys the cancer cells directly or by destroying "
             "their DNA. Radiotherapy involves the use of radiation to destroy cancer cells. In an alternative method, traditional healers "
             "use the plant Sutherlandia frutescens. Recently scientists carried out tests using an extract from Sutherlandia frutescens on "
             "10 vervet monkeys to treat cancer and found that it had no side effects.", "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Nerve tissue", "marks": 5, "lead": "The diagram below represents an animal tissue.",
     "figure": P.fig("2.4", "A neuron with branched ends on both sides of a long fibre and a round cell body on a short side branch, no labels."),
     "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Investigation: enzymes", "marks": 8,
     "lead": "An investigation was carried out to determine the effect of high temperature on a washing powder containing fat-digesting "
             "enzymes. The procedure was as follows:\n• Two of the same school white shirts were used.\n• White shirts X and Y had the "
             "same fat stain.\n• White shirt X was washed with detergent containing fat-digesting enzymes for 3 minutes at 37 °C.\n• White "
             "shirt Y was washed with detergent containing fat-digesting enzymes for 3 minutes in boiling water.\n• The investigation was "
             "repeated five times.\nThe results of the investigation are shown below.",
     "figure": P.fig("2.5", "White shirt X, clean; white shirt Y, with a large fat stain still on its front."), "items": q25},
    {"id": "2.6", "title": "Question 2.6", "kind": "Plant tissues", "marks": 15, "lead": "The diagram below shows different types of plant tissues.",
     "figure": P.fig("2.6", "Three plant tissues: A, epidermal cells around a stoma with two guard cells; B, thin-walled round cells; C, cells "
                            "with walls thickened at the corners."), "items": q26},
    {"id": "3.1", "title": "Question 3.1", "kind": "The skull", "marks": 7,
     "lead": "The diagram below represents the side and ventral views of a human skull.",
     "figure": P.fig("3.1", "A human skull from the side and from below; X points to the large opening at the base."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Joints", "marks": 6, "lead": "The diagram below shows different joints.",
     "figure": P.fig("3.2", "Three joints: A, the atlas turning on the axis; B, the elbow; C, the bones of the wrist and hand."), "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Investigation: osteoporosis", "marks": 9, "table": SURVEY,
     "lead": "Osteoporosis is a disorder whereby bones develop small pores and can easily break. An investigation was conducted to determine "
             "the frequency of osteoporosis amongst different age groups of men and women. The investigators carried out a survey amongst "
             "500 men and 500 women of different age groups in a certain country. The results of the survey are shown in the table below.",
     "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Transpiration", "marks": 14,
     "lead": "The graph below illustrates the rate of transpiration in a plant under conditions of light and darkness.",
     "figure": P.fig("3.4", "Rate of transpiration over two days and nights from 06:00: it rises through point 1 to a peak in the day, falls to "
                            "point 2 at 18:00, stays low through the night to point 3 at 06:00, then rises through point 4."), "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Plant structure", "marks": 10, "lead": "The diagram below shows different parts of a plant.",
     "figure": P.fig("3.5", "A section of a leaf with tissue A, the palisade layer, under the upper epidermis and tissue B, a vascular bundle; "
                            "a section of a root with a root hair; the word 'stem' between them."), "items": q35},
    {"id": "3.6", "title": "Question 3.6", "kind": "The potometer", "marks": 4, "items": q36}]

P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "1.4.5", "kind": "memo_issue", "detail": "The memo's working reads 50 mm × 0,9 µm ÷ 8 = 5,6 and then = 0,0056, mixing units. The "
                                                         "formula as printed gives 50 × 0,9 ÷ 8 = 5,63 µm, the right option; 0,0056 is in "
                                                         "no option."},
          {"n": "1.5.3", "kind": "low_confidence", "detail": "The memo says the cell cannot be from a root because it contains chloroplasts, "
                                                             "and 1.5.2(c) names E as the mitochondrion; in the drawing E and C are both "
                                                             "striped ovals. The answers follow the memo."},
          {"n": "2.6.3", "kind": "no_fit", "detail": "The root hair (2.6.3) and the bar graph (3.3.3) play as pick the drawing: the memo's and "
                                                     "three drawings that lose a rubric mark."}],
         {"1": 50, "2": 50, "3": 50}, 150,
         {}, "Questions 1 to 3 (the whole paper)",
         sections=[("Section A", 50, None, ["1"]), ("Section B", 100, None, ["2", "3"])])
