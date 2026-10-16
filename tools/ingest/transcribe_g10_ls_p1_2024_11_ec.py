"""Grade 10 Life Sciences P1 November 2024 (Eastern Cape Department of Education, provincial assessment), the whole paper (Questions
1 to 3, 150 marks, 2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options,
marks and answers are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md):
stanmorephysics.com, one scanned PDF of the paper (19 pages) and the marking guidelines (11 pages), split by page into QP and MG
files (no text layer), read from page images (100 dpi). A stand-in: no Grade 10 Life Sciences Nov 2025 paper is published.

  python tools/ingest/transcribe_g10_ls_p1_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ls-p1-2024-11-ec/g10-ls-p1-2024-11-ec QP.pdf" "uploads/provincial/g10-ls-p1-2024-11-ec/g10-ls-p1-2024-11-ec MG.pdf" --id g10-ls-p1-2024-11-ec --from-json

The Life Sciences rulings, as in transcribe_g10_ls_p1_2024_11_nw.py: printed multiple choice as printed; terms typed; Column I /
Column II as A only / B only / both / none; a NUMBER from a diagram an MCQ of the numbers; a written answer as statements to pick
(the memo's points and clearly wrong ones); the two calculations (2.2.3, 3.6.2) as four workings; the tabulated differences (3.2) as
a sort; the line graph (3.6.3) as pick the drawing (pictures_lower.py). The meal table (2.2), the enzyme table (1.1.7) and the
ribosome table (3.6) are typed. Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ls-p1-2024-11-ec", 595.32, 842.04, {
    "1.1.2": [3, 130, 280, 540, 520], "1.1.5": [4, 216, 208, 459, 415], "1.1.8": [5, 245, 343, 405, 510], "1.1.10": [6, 162, 112, 538, 325],
    "1.4": [8, 101, 115, 540, 301], "1.5": [9, 109, 114, 528, 394], "2.1": [10, 124, 180, 439, 342], "2.3": [12, 110, 137, 495, 502],
    "2.5": [14, 130, 111, 523, 441], "2.6": [15, 101, 169, 540, 539], "3.1": [16, 112, 143, 479, 323], "3.3": [17, 85, 106, 552, 314],
    "3.4": [18, 166, 112, 441, 307]}, start=9)
work, answer, num, draw, stmt, mcq, term, sort = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term, P.sort
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
pickn = lambda n, q, opts, a, clues: mcq(n, q, opts, a, clues, marks=1)

# ---- SECTION A, QUESTION 1, the question paper pages 3-9 and the memo pages 4-5 ----
q11 = [
    mcq("1.1.1", "Which ONE of the following is a nucleic acid?", ["Protein", "Lipid", "DNA", "Phosphorus"], 2,
        ["Nucleic acids carry genetic information.", "Deoxyribonucleic acid."]),
    mcq("1.1.2", "The diagram shows events during cell division. The correct sequence of events is …",
        ["1-2-3-4-5", "2-4-3-2-1", "3-1-2-4-5", "3-4-1-2-5"], 3, ["Interphase comes first: the chromatin is not yet coiled.",
                                                                  "Then prophase, metaphase, anaphase, telophase."],
        figure=P.fig("1.1.2", "Five cells: 1 chromosomes lined up across the middle on spindle fibres; 2 chromosomes pulled to the two "
                              "poles of a cell starting to pinch in; 3 a nucleus with thread-like chromatin; 4 a nucleus with coiled "
                              "chromosomes; 5 two cells, each with its own chromosomes.")),
    mcq("1.1.3", "Mitosis is responsible for …", ["forming daughter cells with an unequal chromosome number", "forming a sperm cell",
        "causing variation in sex cells", "repairing skin cells worn out through friction"], 3,
        ["Mitosis makes identical cells.", "Growth and repair."]),
    mcq("1.1.4", "The phase during which the centromere splits is …", ["telophase.", "prophase.", "anaphase.", "metaphase."], 2,
        ["The chromatids then move apart.", "It follows metaphase."]),
    mcq("1.1.5", "The diagram represents a type of connective tissue. The type of tissue represented is …",
        ["hyaline cartilage.", "loose areolar connective.", "dense fibrous tissue.", "blood tissue."], 1,
        ["Fibres run loosely in all directions.", "Cells are scattered between them."],
        figure=P.fig("1.1.5", "Loosely arranged fibres, some wavy and some straight, running in all directions, with scattered cells.")),
    mcq("1.1.6", "Which ONE of the following tissues prevents friction between the bones?", ["Blood", "Cartilage", "Epithelium", "Muscle"], 1,
        ["It covers the ends of the bones at a joint.", "Smooth and firm."]),
    mcq("1.1.7", "A biological washing powder contains enzymes that break down the stains caused by organic substances. The optimum pH of "
                 "enzymes J, K, L and M: J 5; K 10; L 8; M 7-9. Which ONE of the following enzymes would be most effective in a washing "
                 "powder that works in an acidic medium?", ["J", "K", "L", "M"], 0,
        ["Acidic means a pH below 7.", "Which optimum pH is below 7?"]),
    mcq("1.1.8", "The diagram shows a cell during a phase in mitosis. Which ONE of the statements describes the chromosome condition in the "
                 "nucleus of the cell?", ["8 chromosomes, each with 4 chromatids", "8 chromosomes, each with 2 chromatids",
                                          "16 chromosomes each with 1 chromatid", "16 chromosomes each with 8 chromatids"], 1,
        ["Count the X shapes.", "Each X is one chromosome of two chromatids."],
        figure=P.fig("1.1.8", "A cell with eight X-shaped chromosomes of different sizes scattered inside the nucleus.")),
    mcq("1.1.9", "Types of muscle tissue in the human body: (i) cardiac muscle, (ii) smooth muscle, (iii) skeletal muscle. Which combination "
                 "represents muscle tissue made up of muscle fibres?", ["(i), (ii) and (iii)", "(i) and (iii) only", "(ii) and (iii) only",
                                                                         "(i) and (ii) only"], 1,
        ["Smooth muscle is made of spindle-shaped cells.", "The striped muscles form fibres."]),
    mcq("1.1.10", "The graph shows the enzyme activity at different temperatures. Which ONE of the following is an explanation for the shape "
                  "of the graph between 35 °C and 55 °C?",
        ["The mass of food broken down increases, because as the temperature increases the enzyme activity increases.",
         "The mass of food broken down decreases, because as the temperature increases the enzyme activity decreases as enzymes denature.",
         "The temperature increases, because the mass of food broken down increases as the enzyme activity decreases as enzymes denature.",
         "The mass of food broken down increases, because as the temperature decreases the enzyme activity increases."], 1,
        ["Read the line after 35 °C.", "High temperature denatures enzymes."],
        figure=P.fig("1.1.10", "Mass of food broken down (mg/hour) against temperature (°C): rising from about 2 at 5 °C to 20 at 35 °C, "
                               "about 17 at 45 °C, then falling steeply to about 1 at 55 °C."))]
q12 = [
    term("1.2.1", "A disease caused by uncontrolled mitotic division of cells", ["cancer"], ["Cells divide out of control.",
                                                                                          "A tumour forms."]),
    term("1.2.2", "Movement of water molecules from a region of high water potential to a region of low water potential through a "
                  "semi-permeable membrane", ["osmosis"], ["Water only.", "Through a membrane."]),
    term("1.2.3", "The type of blood cell that transports oxygen in the body", ["red blood cell", "red blood cells", "erythrocyte",
                                                                               "erythrocytes"], ["It contains haemoglobin.", "Not white."]),
    term("1.2.4", "The division of the cytoplasm during mitosis", ["cytokinesis"], ["Not the nucleus dividing.", "Cyto means cell."]),
    term("1.2.5", "Organic substances required in small quantities", ["vitamins", "vitamin"], ["A, B, C, D, E, K.", "Organic, not minerals."]),
    term("1.2.6", "Nutrients that are needed in small quantities by the body", ["micronutrients", "micro-nutrients", "micro nutrients"],
         ["Micro means small.", "The opposite of macronutrients."]),
    term("1.2.7", "The openings in a leaf that are responsible for gaseous exchange", ["stomata", "stoma"], ["Guard cells surround them.",
                                                                                                         "Mostly on the lower surface."]),
    term("1.2.8", "Parenchyma tissue with chloroplasts in the cells", ["chlorenchyma"], ["Chloro means green.",
                                                                                         "It photosynthesises."]),
    term("1.2.9", "A collective name for xylem and phloem tissue", ["vascular tissue", "vascular tissues", "vascular bundle", "vascular bundles"],
         ["They transport substances.", "Vessels."])]
q13 = [
    abq("1.3.1", "The seven vertebrae in the neck region", "Lumbar", "Cervical", 1, ["The neck vertebrae.", "Lumbar is the lower back."]),
    abq("1.3.2", "Responsible for blood clotting", "Platelets", "Red blood cells", 0, ["Cell fragments.", "Red cells carry oxygen."]),
    abq("1.3.3", "Transmits impulses from the receptor to the central nervous system", "Motor neuron", "Sensory neuron", 1,
        ["From the receptor inwards.", "Motor neurons go to effectors."])]
ORG = ["1", "2", "3"]
q14 = [
    pickn("1.4.1(a)", "Give the NUMBER (1, 2 or 3) of the diagram that represents the root.", ORG, 1,
          ["The xylem is in the centre.", "A star shape in the middle."]),
    pickn("1.4.1(b)", "Give the NUMBER (1, 2 or 3) of the diagram that represents the stem.", ORG, 0,
          ["Vascular bundles in a ring.", "Round with bundles near the edge."]),
    pickn("1.4.1(c)", "Give the NUMBER (1, 2 or 3) of the diagram that represents the leaf.", ORG, 2,
          ["Palisade and spongy cells.", "Not round."]),
    term("1.4.2(a)", "Identify tissue A.", ["xylem", "xylem tissue"], ["In a vascular bundle.", "It carries water."]),
    term("1.4.2(b)", "Identify tissue B.", ["xylem", "xylem tissue"], ["At the centre of the root.", "It carries water up."]),
    term("1.4.2(c)", "Identify tissue C.", ["spongy mesophyll", "spongy tissue", "spongy parenchyma", "spongy mesophyll tissue"],
         ["Loosely packed cells in the leaf.", "Below the palisade layer."]),
    stmt("1.4.3", "Describe the OBSERVABLE difference between organ 1 and organ 2.", 2,
         ["Organ 1 has its vascular bundles arranged in a ring; organ 2 has its xylem at the centre.",
          "Organ 1 has no endodermis; organ 2 has an endodermis."],
         ["Organ 1 has its xylem at the centre; organ 2 has its vascular bundles in a ring.",
          "Organ 1 has palisade cells; organ 2 has none.", "Organ 2 has no vascular tissue at all."],
         ["Where is the vascular tissue in each?", "Ring or centre."], 2)]
q15 = [
    term("1.5.1(a)", "Identify part A.", ["basement membrane", "basement layer", "basal membrane"], ["The cells sit on it.",
                                                                                                   "A thin layer beneath."]),
    term("1.5.1(b)", "Identify epithelial tissue 2.", ["columnar epithelium", "columnar", "columnar epithelial tissue"],
         ["Tall, column-shaped cells.", "Taller than they are wide."]),
    term("1.5.1(c)", "Identify epithelial tissue 4.", ["squamous epithelium", "squamous", "squamous epithelial tissue"],
         ["Flat, thin cells.", "Like scales."]),
    pickn("1.5.2", "Give the NUMBER of the tissue that is found lining the respiratory tract.", ["1", "2", "3", "4"], 2,
          ["It has cilia.", "And mucus-secreting cells."]),
    term("1.5.3", "Identify cell B that secretes mucus.", ["goblet cell", "goblet", "goblet cells"], ["Shaped like a cup.",
                                                                                                     "Full of mucus droplets."]),
    stmt("1.5.4", "Explain the consequence if cilia in the epithelium lining respiratory passages become damaged.", 2,
         ["Dust particles, micro-organisms and mucus will not be removed from the trachea.",
          "This causes lung infections, or makes the person cough."],
         ["The person will breathe faster and absorb more oxygen.", "Mucus production stops completely.",
          "The lungs will clean themselves better."],
         ["What do cilia sweep away?", "What happens if it stays?"], 1)]

# ---- SECTION B, QUESTION 2, the question paper pages 10-15 and the memo pages 5-7 ----
q21 = [
    stmt("2.1.1", "Give ONE observable reason why the cell in the diagram represents a plant cell.", 1,
         ["It has chloroplasts.", "It has a cell wall."], ["It has a nucleus.", "It has mitochondria.", "It has a cell membrane."],
         ["What do only plant cells have?", "Look for the oval green organelle and the outer wall."], 1),
    stmt("2.1.2(a)", "State ONE function of organelle A (the Golgi body).", 1,
         ["It transports, packages and secretes proteins and enzymes."],
         ["It releases energy by cellular respiration.", "It makes food by photosynthesis.", "It controls the cell's activities.",
          "It stores cell sap."], ["A is a stack of flattened sacs.", "It packages."], 1),
    stmt("2.1.2(b)", "State ONE function of organelle E (the mitochondrion).", 1,
         ["It releases energy by cellular respiration."],
         ["It makes food by photosynthesis.", "It transports proteins.", "It controls all the cell's activities.",
          "It gives the cell its shape."], ["E has folded inner membranes.", "The powerhouse."], 1),
    stmt("2.1.3", "Give the LETTER and NAME of the organelle that contains genetic material.", 2,
         ["D – nucleus", "E – mitochondrion", "F – chloroplast"], ["A – nucleus", "B – chloroplast", "C – mitochondrion"],
         ["The chromosomes are in D.", "Mitochondria and chloroplasts have their own DNA."], 2),
    stmt("2.1.4", "Why do animal cells contain more mitochondria than plant cells?", 2,
         ["Animal cells need more energy.", "The energy is needed for movement."],
         ["Plant cells make their energy in chloroplasts and need none.", "Animal cells are bigger than plant cells.",
          "Animal cells have no cell wall to protect them."], ["Animals move.", "Mitochondria release energy."], 1),
    stmt("2.1.5", "Name TWO organelles enclosed by a double membrane.", 2,
         ["Chloroplast", "Mitochondrion", "Nucleus"], ["Ribosome", "Golgi body", "Vacuole"],
         ["The organelles with their own DNA.", "Two membranes around them."], 1)]
MEAL = {"head": ["Food eaten", "Carbohydrate (g)", "Protein (g)", "Fat (g)", "Vitamin C (g)", "Iron (mg)"],
        "rows": [["Sausage", "5", "9", "24", "0", "1"], ["Fried potato chips", "70", "8", "20", "20", "2"], ["Beans", "20", "10", "1", "4", "3"],
                 ["Fruit pie", "60", "2", "25", "1", "1"], ["Ice cream", "20", "0", "12", "0", "0"]]}
FOODS = ["Sausage", "Fried potato chips", "Beans", "Fruit pie", "Ice cream"]
q22 = [
    pickn("2.2.1(a)", "Identify the food with the most proteins.", FOODS, 2, ["Read the protein column.", "The largest number."]),
    pickn("2.2.1(b)", "Identify the food suitable for a person with anaemia.", FOODS, 2, ["Anaemia is a lack of iron.",
                                                                                          "Read the iron column."]),
    pickn("2.2.2", "Which food has the LEAST overall nutritional value?", FOODS, 4, ["Look for the zeros.", "No protein, vitamin C or iron."]),
    work("2.2.3", "The total energy value of this meal is 5 000 kJ. In one day, this learner requires a total of 15 000 kJ of energy. "
                  "Calculate the percentage of daily energy need that this meal provides. Show ALL working.", 3,
         ["{5 000}/{15 000} × 100\n= 33,33%", "{15 000}/{5 000} × 100\n= 300%", "{5 000 + 15 000}/{15 000} × 100\n= 133,33%",
          "{15 000 − 5 000}/{15 000} × 100\n= 66,67%"],
         ["The part over the whole.", "Then multiply by 100."])]
q23 = [
    term("2.3.1", "Identify compound P.", ["protein", "proteins"], ["It contains nitrogen.", "Made of amino acids."]),
    stmt("2.3.2", "Give a reason for your answer in QUESTION 2.3.1.", 1,
         ["It contains nitrogen (carbon, hydrogen, oxygen and nitrogen)."],
         ["It contains only carbon, hydrogen and oxygen.", "It contains the most oxygen.", "It contains phosphorus.", "It has no carbon."],
         ["Which element is only in P?", "Q and R have no nitrogen."], 1, after=["2.3.1"]),
    stmt("2.3.3", "Give TWO reasons why compound P is biologically important.", 2,
         ["It is a source of amino acids.", "It provides structure and support: it forms cell membranes.",
          "It speeds up chemical reactions as enzymes.", "It provides protection as antibodies.", "It is involved in coordination as hormones."],
         ["It stores genetic information as DNA.", "It is the main source of quick energy.", "It forms the cell walls of plants."],
         ["Enzymes, antibodies, hormones.", "What is built from amino acids?"], 1),
    answer("2.3.4", "What is the ratio of hydrogen to oxygen in compound R?", 1, ["2:1", "1:2", "1:1", "4:1"],
           ["Compare the hydrogen and oxygen sectors.", "Hydrogen is half the circle."]),
    stmt("2.3.5", "Explain why high temperature decreases enzyme activity.", 3,
         ["Enzymes are denatured: they lose their shape at high temperature.", "The active site is damaged.",
          "So the enzyme can no longer act on the substrate."],
         ["High temperature makes enzymes work faster for ever.", "Enzymes melt into fat.", "The substrate turns into an enzyme."],
         ["Enzymes are proteins.", "Shape and the active site."], 1)]
q24 = [
    term("2.4.1(a)", "Identify the independent variable.", ["hydrogen peroxide concentration", "concentration of hydrogen peroxide",
                                                            "the concentration of hydrogen peroxide"],
         ["What the learner changed.", "Seven different …"]),
    term("2.4.1(b)", "Identify the dependent variable.", ["enzyme activity", "the enzyme activity", "height of the bubble foam",
                                                          "the height of the bubble foam", "height of bubble foam"],
         ["What was measured.", "It depends on the concentration."]),
    stmt("2.4.2", "State TWO planning steps that were considered by the learners before doing the investigation.", 2,
         ["Decide on and collect the apparatus needed.", "Decide on the concentrations of hydrogen peroxide to use.",
          "Decide how the results will be recorded."],
         ["Measure the height of the foam.", "Put the potato in the test tubes.", "Write the conclusion."],
         ["Before starting.", "Apparatus, concentrations, recording."], 1),
    stmt("2.4.3", "Give TWO factors that were kept constant in all the test tubes during the investigation.", 2,
         ["The same amount of dishwashing liquid (3 drops).", "The same amount of food dye (1 drop).",
          "The same time of observation (30 seconds)."],
         ["The concentration of hydrogen peroxide.", "The amount of potato in every tube.", "The height of the bubble foam."],
         ["Read the procedure.", "Not the seventh tube's potato."], 1),
    term("2.4.4", "Which substance represents the substrate?", ["hydrogen peroxide", "h2o2"], ["Catalase breaks it down.",
                                                                                             "It releases oxygen."]),
    stmt("2.4.5", "Explain the purpose of the seventh test tube in this investigation.", 3,
         ["It is a control, to compare with.", "It shows that the oxygen bubbles are due to catalase in the potato,",
          "which acts on the hydrogen peroxide.",
          "With no potato there is no catalase to act on the hydrogen peroxide, so no oxygen bubbles are released."],
         ["It contains the most hydrogen peroxide.", "It speeds up the reaction in the other tubes.", "It measures the temperature."],
         ["The seventh tube had no potato.", "A control."], 1)]
q25 = [
    term("2.5.1(a)", "Identify part A.", ["chromatid", "chromatids"], ["Half of a chromosome.", "Two are joined."]),
    term("2.5.1(b)", "Identify part C.", ["spindle fibre", "spindle fibres", "spindle fiber", "spindle"], ["Dashed lines pole to pole.",
                                                                                                         "They pull."]),
    stmt("2.5.2(a)", "State ONE function of part B.", 1,
         ["It forms the spindle fibres."],
         ["It holds the two chromatids together.", "It releases energy.", "It makes proteins.", "It stores genetic information."],
         ["B is at a pole.", "The fibres start there."], 1),
    stmt("2.5.2(b)", "State ONE function of part D.", 1,
         ["It holds the two chromatids together.", "It attaches the chromosome to a spindle fibre."],
         ["It forms the spindle fibres.", "It releases energy.", "It divides the cytoplasm."],
         ["D is where the chromatids join.", "The centromere."], 1),
    num("2.5.3(a)", "How many chromosomes were present in the cell before the start of the cell division?", 3, 0, "",
        ["Count the chromosomes on the equator.", "Mitosis keeps the number."]),
    num("2.5.3(b)", "How many chromosomes will be present in each daughter cell at the end of this division?", 3, 0, "",
        ["Mitosis keeps the number.", "The same as the parent cell."]),
    stmt("2.5.4", "Explain what would happen if part C failed to contract.", 3,
         ["The centromere will not split.", "The sister chromatids will not be pulled to opposite poles.",
          "The daughter cells will not have the required (an equal) chromosome number."],
         ["The cell will divide faster.", "The chromosomes will double again.", "The nuclear membrane will disappear for ever."],
         ["C pulls the chromatids apart.", "What if nothing pulls?"], 1)]
q26 = [
    stmt("2.6.1", "Provide a suitable caption for the graph.", 1,
         ["The distance moved by the air bubble at different temperatures over 20 minutes."],
         ["The rate of photosynthesis at different light intensities.", "Temperature against time.", "The number of leaves on the twig.",
          "The distance moved by the twig in the wind."], ["Both variables.", "Distance, temperature, time."], 1),
    term("2.6.2", "Name the apparatus that can be used to measure the rate of transpiration in plants.", ["potometer"],
         ["The air bubble moves along its capillary tube.", "Poto means drink."]),
    stmt("2.6.3", "Give a reason why the leafy twig had to be cut under water.", 1,
         ["To prevent air bubbles from blocking (getting into) the xylem."],
         ["To keep the leaves cool.", "To make the twig absorb salt.", "To kill bacteria on the stem.", "To make the twig heavier."],
         ["Air in the xylem stops the water.", "Cut under water, no air gets in."], 1),
    stmt("2.6.4", "Explain why the distance moved by the air bubble was the highest at 25 °C.", 2,
         ["A higher temperature gives the water molecules more (kinetic) energy,", "so water evaporates faster and transpiration increases."],
         ["At 25 °C the stomata close.", "Cold air holds more water vapour.", "The bubble moves backwards when it is warm."],
         ["Heat and molecules.", "Faster evaporation."], 1),
    stmt("2.6.5", "Explain how using a needle-shaped leaf twig would affect the rate of transpiration.", 2,
         ["The surface area will decrease,", "which decreases the rate of transpiration."],
         ["The surface area will increase.", "The rate of transpiration will increase.", "Needle leaves have more stomata, so the rate doubles."],
         ["Needles are thin.", "Less surface, less water lost."], 1),
    stmt("2.6.6", "Name ONE other environmental factor that increases the rate of transpiration.", 1,
         ["High light intensity", "High wind velocity", "Low humidity"], ["High humidity", "Darkness", "Still air"],
         ["Not temperature: that is in the graph.", "Light, wind, humidity."], 1)]

# ---- QUESTION 3, the question paper pages 16-19 and the memo pages 8-11 ----
q31 = [
    term("3.1.1(a)", "Identify part B (vertebrae).", ["lumbar", "lumbar vertebrae", "lumbar vertebra"], ["The lower back.",
                                                                                                        "Above the sacrum."]),
    term("3.1.1(b)", "Identify part C.", ["ilium"], ["The large wing of the pelvis.", "Not 'hipbone'."]),
    term("3.1.1(c)", "Identify part D.", ["sacrum", "coccyx"], ["Fused vertebrae at the back of the pelvis.", "Below the lumbar vertebrae."]),
    term("3.1.2", "Name the bone that encloses the brain.", ["cranium"], ["The skull's dome.", "Not the jaw."]),
    stmt("3.1.3", "Give TWO letters of the parts that are classified as part of the axial skeleton.", 2,
         ["A", "B", "D"], ["C", "E", "F"], ["The axial skeleton: skull, vertebral column, ribs, sternum.", "Not the limbs or the pelvis."], 1),
    stmt("3.1.4", "Give FOUR functions of the human skeleton.", 4,
         ["Movement", "Protection of the internal organs", "Support, strength and shape", "Storage of minerals",
          "Formation of red blood cells", "Hearing (the bones in the ear)"],
         ["Digestion of food", "Pumping blood"], ["What would you be without bones?", "Bone marrow, minerals, the ear."], 1),
    term("3.1.5", "Name the opening at the base of the skull.", ["foramen magnum"], ["The largest opening.", "The spinal cord passes."]),
    stmt("3.1.6", "State the function of the part mentioned in QUESTION 3.1.5.", 1,
         ["It allows the spinal cord to enter the skull."],
         ["It lets air into the lungs.", "It holds the teeth.", "It lets light into the eye.", "It joins the skull to the pelvis."],
         ["What passes through it?", "The spinal cord meets the brain."], 1, after=["3.1.5"])]
q32 = [
    sort("3.2", "Tabulate TWO differences between tendons and ligaments.", ["Tendons", "Ligaments"],
         [("Attach muscle to bone", 0), ("Made of inelastic, white fibrous connective tissue", 0), ("Not able to stretch", 0),
          ("Attach bone to bone", 1), ("Made of elastic, yellow connective tissue that can stretch", 1)],
         ["Tendons: muscle to bone.", "Ligaments: bone to bone, and elastic."])]
q33 = [
    stmt("3.3.1", "State what is meant by a permanent tissue.", 1,
         ["A tissue that is specialised (differentiated) to perform a specific function."],
         ["A tissue whose cells keep dividing.", "A tissue that never dies.", "A tissue found only in roots.", "A tissue made of one cell."],
         ["The opposite of meristematic.", "Specialised."], 1),
    term("3.3.2(a)", "Identify the tissue represented as A.", ["xylem", "xylem tissue"], ["Long tubes with pits.", "It carries water."]),
    term("3.3.2(b)", "Identify the tissue represented as B.", ["sclerenchyma"], ["Thick-walled cells.", "Dead cells for support."]),
    stmt("3.3.3", "State ONE function of tissue C.", 1,
         ["Provides support.", "Allows gaseous exchange.", "Packaging tissue: fills in around other tissues.", "Storage."],
         ["Transports water to the leaves.", "Makes the plant woody and dead.", "Conducts nerve impulses."],
         ["C is parenchyma.", "Thin-walled round cells."], 1),
    stmt("3.3.4", "Explain TWO ways in which tissue A is structurally suited for its function.", 4,
         ["No end walls, forming continuous tubes for water movement.", "Dead cells, hollow to allow the transport of water.",
          "Pits, for sideways water movement.", "Lignified walls, to provide support and stop the walls collapsing."],
         ["Living cells with large nuclei, to make food.", "Sieve plates, to carry sugars.", "Chloroplasts, for photosynthesis."],
         ["A is xylem.", "A structure and what it does."], 2)]
q34 = [
    term("3.4.1(a)", "Identify part A.", ["epidermal cell", "epidermis", "cell wall", "epidermal cell wall"],
         ["The outer layer of the root.", "The root hair grows from it."]),
    term("3.4.1(b)", "Identify part B.", ["cell sap", "vacuole", "sap"], ["Inside the root hair.", "A large sac."]),
    stmt("3.4.2", "Give TWO ways in which the root hair is structurally suited for the absorption of water.", 2,
         ["Large surface area.", "Permeable cell wall.", "Cell sap with a high solute concentration (a lower water potential than the soil "
                                                         "water).",
          "Thin cell wall.", "Many mitochondria."],
         ["A thick waxy cuticle.", "Many chloroplasts."], ["Long and thin.", "Water moves in by osmosis."], 1),
    stmt("3.4.3", "Describe TWO ways water can move through layer C to reach the endodermis.", 2,
         ["Water moves through the intercellular air spaces.", "Water moves through the cell wall, cell membrane and cytoplasm."],
         ["Water moves through the phloem only.", "Water is pumped by the heart.", "Water moves through the stomata."],
         ["Between the cells, or through them.", "Describe, do not just name."], 1),
    stmt("3.4.4", "Explain the effect of soil water with a high salt concentration on part B.", 3,
         ["The soil water has a lower water potential than the cell sap.", "Water moves out of the vacuole by osmosis into the soil.",
          "The root hair vacuole (B) will shrink."],
         ["Water moves into the root hair.", "The vacuole will burst.", "Salt moves into the vacuole by osmosis."],
         ["Where is the water potential lower?", "Water leaves."], 1)]
q35 = [
    stmt("3.5", "Describe the THREE forces involved in the upward movement of water.", 6,
         ["Root pressure: water entering the roots pushes water up into the stem.",
          "Capillarity: water moves up the narrow xylem by adhesion and cohesion.",
          "Transpiration pull: the loss of water vapour from the leaves pulls water up the xylem."],
         ["Gravity pulls water up the stem.", "The phloem pumps water up with sugar.", "The plant's heart pumps water."],
         ["One from below, one in the tubes, one from above.", "Name each force and describe it."], 2)]
RIBO = {"head": ["Age of a leaf (days)", "Number of ribosomes (per 10 cm²)"],
        "rows": [["5", "17"], ["15", "32"], ["20", "40"], ["30", "45"], ["35", "45"]]}
q36 = [
    stmt("3.6.1", "State the relationship between the age of the leaf and the number of ribosomes.", 2,
         ["As the age of the leaf increases (from 5 to 30 days), the number of ribosomes increases,",
          "then it stays the same from 30 to 35 days."],
         ["As the age increases, the number of ribosomes decreases.", "The number of ribosomes is the same at all ages.",
          "Younger leaves have the most ribosomes."], ["Read the table down.", "Two parts: rising, then level."], 1),
    work("3.6.2", "Calculate the percentage increase of ribosomes from day 5 to day 35. Show ALL working.", 2,
         ["Increase: 45 − 17 = 28\n{28}/{17} × 100 = 164,71%", "Increase: 45 − 17 = 28\n{28}/{45} × 100 = 62,22%",
          "Increase: 45 + 17 = 62\n{62}/{17} × 100 = 364,71%", "Increase: 45 − 17 = 28\n{45}/{17} × 100 = 264,71%"],
         ["Increase ÷ the starting value.", "Then × 100."]),
    draw("3.6.3", "Draw a line graph to represent the data in the table.", 6, [
        ["Caption (both variables stated)", 1], ["Type of graph (line graph)", 1], ["X- and Y-axis labels with units", 1],
        ["Correct scale for the X- and Y-axis", 1], ["All 5 coordinates plotted correctly", 2]],
        ["Age on the x-axis, ribosomes on the y-axis.", "Join the five points."],
        memo="The memo's graph: the five points (5 ; 17), (15 ; 32), (20 ; 40), (30 ; 45), (35 ; 45) joined, captioned 'Number of "
             "ribosomes in a leaf of different age', both axes labelled.")]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 20, "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 9,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 6,
     "lead": "Indicate whether each of the descriptions in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Plant organs", "marks": 8,
     "lead": "The diagram below represents internal structures of different plant organs.",
     "figure": P.fig("1.4", "Three cross-sections: 1 round with vascular bundles in a ring (A points to one); 2 round with a star-shaped "
                            "xylem at the centre (B); 3 a leaf section with palisade and spongy cells (C points to the spongy layer)."),
     "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Epithelial tissues", "marks": 7,
     "lead": "The diagrams below represent different epithelial tissues.",
     "figure": P.fig("1.5", "Four epithelia: 1 a row of cube-shaped cells on a layer A; 2 tall column-shaped cells; 3 tall cells with cilia "
                            "and a cup-shaped cell B full of droplets; 4 thin flat cells."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "The plant cell", "marks": 9, "lead": "The diagram below shows a plant cell.",
     "figure": P.fig("2.1", "A plant cell labelled A (a stack of flattened sacs with small vesicles), B and C at the cell's edge, D the "
                            "nucleus with its chromatin, E an organelle with folded inner membranes, F an oval organelle with stacked "
                            "membranes."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Nutrition", "marks": 6, "table": MEAL,
     "lead": "The table below shows the details of a meal eaten by a Grade 10 learner.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Organic compounds", "marks": 8,
     "lead": "The following pie graphs show the composition of three organic compounds that are found in living organisms.",
     "figure": P.fig("2.3", "Three pie graphs: P with carbon, hydrogen, oxygen and nitrogen; Q with carbon, oxygen and hydrogen (about half); "
                            "R with carbon a quarter, oxygen a quarter and hydrogen a half."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Investigation: catalase", "marks": 10,
     "lead": "The rate of enzyme activity increases as the substrate concentration increases up to a point where all enzyme active sites are "
             "occupied by substrates to form an enzyme-substrate complex. Catalase is an enzyme in potatoes that is able to break down "
             "hydrogen peroxide to release oxygen gas, which forms bubbles. A learner conducted an investigation to determine the effect of "
             "increasing hydrogen peroxide concentration on the enzyme activity. The procedure was as follows:\n• Seven test tubes, each "
             "containing different concentrations of hydrogen peroxide, were used.\n• Three drops of dishwashing liquid were added into each "
             "test tube so that bubbles form a foam.\n• One drop of food dye was added so bubbles could be seen more clearly.\n• Potato "
             "segments of the same size and weight were put in six test tubes.\n• A potato segment was not put in the seventh test tube.\n"
             "• The reaction was observed for 30 seconds.\n• To measure enzyme activity, the height of the bubble foam was measured after the "
             "30 seconds.", "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Mitosis", "marks": 9, "lead": "The diagram below represents a phase during mitosis.",
     "figure": P.fig("2.5", "A cell with three chromosomes lined up across the middle on dashed spindle fibres from two poles: A one "
                            "chromatid, B the structure at a pole, C a spindle fibre, D the point where two chromatids join."), "items": q25},
    {"id": "2.6", "title": "Question 2.6", "kind": "Transpiration", "marks": 8,
     "lead": "A learner investigated the effect of temperature on the rate of transpiration in a leafy twig. She measured and recorded the "
             "distance travelled by the air bubble inside the capillary tube. The graph below represents the results recorded by the learner.",
     "figure": P.fig("2.6", "Distance moved by the air bubble (mm) against time (min), 0 to 20 minutes: at 25 °C rising to 20 mm, at −4 °C "
                            "to about 6 mm, at −10 °C to about 2 mm."), "items": q26},
    {"id": "3.1", "title": "Question 3.1", "kind": "The skull and pelvis", "marks": 12,
     "lead": "The diagram below represents the skull and pelvis.",
     "figure": P.fig("3.1", "A skull from the side, A pointing to the dome; the pelvis with B the vertebrae above it, C its large wing, D the "
                            "fused bones at the back, E the thigh bone and F the hip joint circled."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Tendons and ligaments", "marks": 5, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Plant tissues", "marks": 8,
     "lead": "The diagrams below represent types of permanent tissues in plants.",
     "figure": P.fig("3.3", "Three tissues: A long tubes, one spiral-thickened and one with pits; B thick-walled angular cells packed "
                            "together; C thin-walled round cells with spaces between them."), "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "The root hair", "marks": 9,
     "lead": "The diagram below represents the outer tissues of a root showing the root hair.",
     "figure": P.fig("3.4", "Root cells with a root hair growing out between soil particles: A the outer cell's wall, B inside the root "
                            "hair, C the layers of cells inside."), "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Water movement", "marks": 6, "items": q35},
    {"id": "3.6", "title": "Question 3.6", "kind": "Investigation: ribosomes", "marks": 10, "table": RIBO,
     "lead": "The table below shows the results obtained in an investigation to determine the relationship between the age of the leaf and "
             "the number of ribosomes present in the leaf cells.", "items": q36}]

P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P1", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.3.1", "kind": "low_confidence", "detail": "The paper prints 2.3.1 (2) but 2.3 totals (8) and the memo gives 2.3.1 one mark "
                                                             "(1 + 1 + 2 + 1 + 3 = 8). The memo's 1 is used."},
          {"n": "2.1.3", "kind": "no_fit", "detail": "The memo accepts any ONE of D – nucleus, E – mitochondrion or F – chloroplast; the cards "
                                                     "offer all three right, and wrong letter-name pairs."},
          {"n": "3.6.3", "kind": "no_fit", "detail": "The line graph plays as pick the drawing: the memo's graph and three that lose a rubric "
                                                     "mark."}],
         {"1": 50, "2": 50, "3": 50}, 150,
         {"2.3.2": ["2.3.1"], "3.1.6": ["3.1.5"]}, "Questions 1 to 3 (the whole paper)",
         sections=[("Section A", 50, None, ["1"]), ("Section B", 100, None, ["2", "3"])])
