"""Grade 10 Life Sciences P2 November 2024 (North West Department of Education, provincial assessment), the whole paper
(Questions 1 to 3, 150 marks, 2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`.
Stems, options, marks and answers are the paper's and the memo's own; clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment, the question paper PDF (English, 15 pages, text layer;
its diagrams are images) and the marking guidelines PDF (English, 10 pages), read from their text and page images (100 dpi).

  python tools/ingest/transcribe_g10_ls_p2_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ls-p2-2024-11-nw/11-NOVEMBER-24-S2-NW-GR10-LIFE-SCIENCES-QP-P2-ENG.pdf" "uploads/provincial/g10-ls-p2-2024-11-nw/11-NOVEMBER-24-S2-NW-GR-10-LIFE-SCIENCES-MG-ENG-P2.pdf" --id g10-ls-p2-2024-11-nw --from-json

The Life Sciences rulings, as in transcribe_g10_ls_p1_2024_11_nw.py: printed multiple choice as printed; terms typed; Column I /
Column II as A only / B only / both / none; LETTER and NAME as lettername; a written answer as statements; a value worked from a table
or an extract as four workings; the tabulated differences (1.4.1) as a sort; the drawings (1.5.4, the food pyramid; 3.1.4, the bar
graph) as pick the drawing (pictures_lower.py: food_pyramid, bars2). The carbon-14 and potato tables are typed.
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ls-p2-2024-11-nw", 595.32, 841.92, {
    "1.1.7": [4, 69, 212, 520, 520], "1.5": [6, 76, 173, 533, 397], "2.1": [7, 83, 170, 524, 497], "3.2": [12, 79, 117, 526, 412],
    "3.3": [13, 76, 130, 531, 389], "3.4": [14, 76, 116, 522, 421], "3.5": [15, 72, 113, 531, 299]}, start=4)
work, answer, num, draw, stmt, mcq, term, sort = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term, P.sort
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
ln = lambda n, q, letters, letter, names, clues, **kw: {"t": "lettername", "n": n, "marks": 2, "q": q, "clues": clues, "letters": letters,
                                                       "a": {"letter": letter, "name": names}, **kw}
HEART = list("ABCDEF")

# ---- SECTION A, QUESTION 1, the question paper pages 3-6 and the memo pages 3-4 ----
q11 = [
    mcq("1.1.1", "Which of the following is a biotic component?", ["Soil", "Water", "Atmosphere", "Animals"], 3,
        ["Biotic means living.", "Which of the four is alive?"]),
    mcq("1.1.2", "The animal organ that pumps the blood to the rest of the body is known as …", ["vein.", "heart.", "vena cava.", "artery."],
        1, ["It is an organ, not a blood vessel.", "It beats."]),
    mcq("1.1.3", "The death of all individuals of a species in the world is known as …", ["extinction.", "speciation.", "mortality.",
        "survival."], 0, ["The species is gone for ever.", "The dinosaurs suffered it."]),
    mcq("1.1.4", "The correct sequence of the energy flow in terms of trophic levels is:",
        ["Primary consumers, producers, secondary consumers, tertiary consumers",
         "Producers, primary consumers, secondary consumers, tertiary consumers",
         "Tertiary consumers, producers, secondary consumers, primary consumers",
         "Secondary consumers, primary consumers, producers, tertiary consumers"], 1,
        ["Energy enters through plants.", "Which level eats the plants?"]),
    mcq("1.1.5", "A long geological period of a drastic decrease in temperature of the earth's surface and the atmosphere.",
        ["Ice age", "Global warming", "Drought", "Climate change"], 0, ["It is a cold period.", "Ice sheets spread."]),
    mcq("1.1.6", "Variety of life forms that exist on earth", ["Ecosystem", "Population", "Biodiversity", "Biome"], 2,
        ["'Bio' means life; 'diversity' means variety.", "Not one species or one area."])]
q117 = [
    mcq("1.1.7", "The diagram above represents the …", ["line graph.", "geological time scale.", "pedigree diagram.",
        "Ordovician extinction graph."], 1, ["The bottom bar shows the eras.", "It spans 600 million years."]),
    mcq("1.1.8", "In which era did the Cretaceous mass extinction occur?", ["Paleozoic era", "Mesozoic era", "Cenozoic era",
        "Permian extinction"], 1, ["Find the Cretaceous extinction on the graph.", "Which era's bar is it above?"])]
q12 = [
    term("1.2.1", "A blood vessel that supplies the heart tissues with oxygen and glucose", ["coronary artery", "coronary arteries"],
         ["It runs over the surface of the heart.", "A blocked one causes a heart attack."]),
    term("1.2.2", "About 250 million years ago all continents were joined into one large continent known as …", ["pangaea", "pangea"],
         ["Its name means 'all lands'.", "It later split into Laurasia and Gondwana."]),
    term("1.2.3", "The height of the land above sea level", ["altitude"], ["It is measured in metres above sea level.",
                                                                          "Mountains have a high one."]),
    term("1.2.4", "Part of the earth where living organisms occur; the global sum of ecosystems", ["biosphere"],
         ["'Bio' means life.", "It includes land, water and air where life exists."]),
    term("1.2.5", "The position of an area in relation to the sun", ["aspect"], ["A north-facing slope in South Africa gets more sun.",
                                                                            "It is a topographic factor."]),
    term("1.2.6", "A group of food chains arranged to show how the feeding of organisms is connected", ["food web"],
         ["Many chains linked together.", "Not a food chain."]),
    term("1.2.7", "The process of finding out the ages of rocks and fossils using radioactive elements",
         ["radiometric dating", "radioactive dating", "radiometric"], ["It uses half-lives.", "Carbon-14 dating is one kind."])]
q13 = [
    abq("1.3.1", "The kingdom to which the lion belongs", "Animalia", "Plantae", 0, ["A lion is an animal.", "It cannot make its own food."]),
    abq("1.3.2", "Pumps the deoxygenated blood from the body to the lungs", "Right ventricle", "Left ventricle", 0,
        ["Deoxygenated blood is on the right side of the heart.", "The left ventricle pumps to the body."]),
    abq("1.3.3", "Type of fossil dating wherein sediment is laid down on top of each other and the oldest rock will be below the upper "
        "layers", "Relative dating", "Radiometric dating", 0, ["It gives an order, not an age in years.", "Lower layers are older."]),
    abq("1.3.4", "Abiotic factors", "Light", "Temperature", 2, ["Abiotic means non-living.", "Are light and temperature alive?"])]
q14 = [
    sort("1.4.1", "Tabulate THREE differences between eukaryotes and prokaryotes.", ["Prokaryotes", "Eukaryotes"],
         [("Cells with no true nucleus", 0), ("Cells with a true nucleus", 1),
          ("The DNA is not enclosed by a nuclear membrane; it lies free in the cytoplasm", 0),
          ("The DNA is enclosed by a nuclear membrane", 1), ("No true (membrane-bound) organelles in the cytoplasm", 0),
          ("True organelles occur in the cytoplasm", 1), ("Monera (bacteria) are examples", 0)],
         ["'Pro' means before; 'karyon' means nucleus.", "Which group has a nuclear membrane?"])]
q15 = [
    term("1.5.1", "Name the type of diagram shown.", ["food web"], ["Many food chains are linked together.", "Arrows show who eats whom."]),
    stmt("1.5.2", "Define an ecosystem.", 2,
         ["A particular area (a pond, a forest) with all the living organisms that interact with each other and with their non-living "
          "environment.", "A community of organisms interacting with each other and with their abiotic environment."],
         ["All the organisms of one species living in an area.", "The non-living parts of an area only.",
          "The place where an organism lives.", "A group of food chains linked together."],
         ["Does it include both living and non-living parts?", "Do the parts interact?"], 2),
    stmt("1.5.3", "Explain the changes that may result in the ecosystem if the carrots, grasses and grains are removed from the area.", 2,
         ["The rabbits, mice, grasshoppers and birds will lack food.", "They will die out.",
          "As a result the foxes and owls will also lack food and die out."],
         ["The foxes and owls will have more food.", "The number of rabbits will increase.",
          "Nothing will change, because the animals eat other animals."],
         ["The carrots, grasses and grains are the producers.", "What do the animals that eat them depend on?"], 1),
    draw("1.5.4", "Draw a food pyramid to show three different trophic levels of organisms in the diagram above.", 4, [
        ["Correct diagram (a pyramid)", 1], ["Foxes and owls at the top", 1], ["Grasshoppers and birds in the middle", 1],
        ["Carrots, grasses and grains at the base", 1]],
        ["The producers form the base.", "The top carnivores are at the top."],
        memo="The memo's pyramid: foxes and owls at the top, grasshopper and bird in the middle, carrot, grasses and grain at the base."),
    stmt("1.5.5", "Make a simple schematic diagram to show any THREE possible food chains from the diagram.", 3,
         ["Carrots → rabbits → foxes", "Grasses → rabbits → foxes", "Grasses → grasshoppers → birds", "Grains → mice → owls",
          "Grains → grasshoppers → owls"],
         ["Foxes → rabbits → carrots", "Owls → mice → grains", "Rabbits → carrots → foxes"],
         ["A food chain starts with a producer.", "The arrows point to the eater."], 1)]

# ---- SECTION B, QUESTION 2, the question paper pages 7-10 and the memo pages 5-6 ----
C14 = {"head": ["NUMBER OF HALF-LIVES ELAPSED", "YEARS FROM THE PRESENT", "PERCENTAGE OF ORIGINAL CARBON-14 REMAINING"],
       "rows": [["0", "0", "100"], ["1", "5 730", "50"], ["2", "11 460", "25"], ["3", "17 190", "B"], ["4", "22 920", "6,25"],
                ["5", "A", "3,125"], ["6", "34 380", "1,56"]]}
q21 = [
    term("2.1.1(A)", "Identify the part labelled A", ["aorta"], ["It is the largest artery.", "It leaves the left ventricle."]),
    term("2.1.1(B)", "Identify the part labelled B", ["bicuspid valve", "mitral valve", "bicuspid"],
         ["It is between the left atrium and the left ventricle.", "It has two flaps."]),
    term("2.1.1(C)", "Identify the part labelled C", ["left ventricle"], ["It has the thickest wall.", "It pumps blood to the whole body."]),
    ln("2.1.2(a)", "Give the LETTER and NAME of the part that receives blood from the superior vena cava", HEART, "F",
       ["right atrium", "right auricle"], ["The venae cavae bring blood back from the body.", "Which upper chamber is on the right?"]),
    ln("2.1.2(b)", "Give the LETTER and NAME of the part that prevents backflow of blood from the right ventricle into the right atrium", HEART,
       "E", ["tricuspid valve", "tricuspid"], ["It is the valve between the right atrium and the right ventricle.", "It has three flaps."]),
    stmt("2.1.3", "Explain why the wall of part C is thicker than that of part D.", 2,
         ["Part C pumps blood over a long distance, to all parts of the body.", "Part D pumps blood over a short distance, to the lungs only."],
         ["Part C receives blood from the lungs only.", "Part D pumps blood to the whole body.", "Part C has thinner walls than part D."],
         ["Where does each ventricle pump blood to?", "Which needs more force?"], 1),
    stmt("2.1.4", "Explain the meaning of a double, closed circulatory system.", 2,
         ["Blood passes through the heart twice in one complete circuit: first to the lungs, then to the rest of the body.",
          "The blood always stays inside blood vessels."],
         ["Blood passes through the heart once in each circuit.", "Blood flows freely in the body cavities.", "The heart has two chambers only."],
         ["'Double': how many times does blood pass the heart?", "'Closed': where is the blood?"], 1),
    stmt("2.1.5", "Describe the heart events of the cardiac cycle during the general diastole.", 5,
         ["The heart relaxes: the ventricles and atria relax.", "Deoxygenated blood enters the right atrium from the inferior and superior "
                                                              "vena cava.",
          "Oxygenated blood enters the left atrium from the pulmonary vein.", "The tricuspid and bicuspid valves are open.",
          "So blood also moves into the ventricles."],
         ["The ventricles contract and push blood into the arteries.", "The semilunar valves open.",
          "The tricuspid and bicuspid valves close."],
         ["Diastole is the relaxing phase.", "Where does blood flow while the heart rests?"], 1)]
q22 = [
    answer("2.2.1", "Give the name of the scientist and the type of system he used to name organisms using the genus and the species.", 2,
           ["Carl Linnaeus; the binomial system", "Charles Darwin; the binomial system", "Carl Linnaeus; the five-kingdom system",
            "Robert Whittaker; the binomial system"],
           ["He was a Swedish scientist of the 1700s.", "'Bi' means two names."]),
    term("2.2.2(a)", "To which Kingdom does the pine tree belong?", ["plantae"], ["It is the first group in the list.", "Pines are plants."]),
    term("2.2.2(b)", "To which Order does the pine tree belong?", ["corniferales", "coniferales"],
         ["Order comes after class in the list.", "Orders often end in -ales."]),
    term("2.2.2(c)", "To which Family does the pine tree belong?", ["pinaceae"], ["Family comes after order.", "Families end in -aceae."]),
    answer("2.2.3", "Write the scientific name of the pine tree.", 2, ["Pinus ponderosa", "pinus Ponderosa", "Ponderosa pinus",
                                                                      "Pinaceae ponderosa"],
           ["The genus first, with a capital letter.", "Then the species, with a small letter."]),
    stmt("2.2.4", "The five-kingdom system is the most common classification system that was proposed by Robert Whittaker in 1969. Give the "
                  "5 kingdoms that were proposed by Robert Whittaker.", 5,
         ["Monera", "Protista", "Fungi", "Plantae", "Animalia"], ["Viruses", "Minerals", "Rocks"],
         ["Bacteria are in one kingdom.", "Mushrooms are not plants."], 1)]
q23 = [
    stmt("2.3.1", "What does endemic species mean?", 1,
         ["Species that occur in one region and nowhere else in the world.", "Plant and animal species found only in one area."],
         ["Species that have died out.", "Species brought in from another country.", "Species found all over the world."],
         ["The extract explains it in brackets.", "Where else can they be found?"], 1),
    term("2.3.2", "Which biome is discussed by the extract above?", ["fynbos", "fynbos biome", "cape floral kingdom"],
         ["It is in the Western Cape.", "Its plants are mostly small bushes."]),
    stmt("2.3.3", "What did the conservation group do in order to save this biome?", 2,
         ["Projects that encourage responsible travel to natural areas, to conserve the environment.",
          "Projects that encourage responsible travel and improve the well-being of local communities."],
         ["They burned the vegetation to stop fires.", "They built more houses in the biome.", "They planted alien trees.",
          "They moved the plants to another country."],
         ["Read the last sentence of the extract.", "What kind of travel is encouraged?"], 2),
    work("2.3.4", "Calculate the total number of species that are endemic to this biome. Show your working.", 3, [
        "{70}/{100} × 9 000\n= 6 300 species",     # the memo
        "{30}/{100} × 9 000\n= 2 700 species",     # the species found elsewhere
        "70 × 9 000\n= 630 000 species",           # 70, not 70%
        "{9 000}/{70}\n= 128,57 species"],         # divided by 70
        ["What percentage of the 9 000 species is found nowhere else?", "Find 70% of 9 000."]),
    stmt("2.3.5", "Describe the type of climate and vegetation found in this biome.", 3,
         ["The vegetation is mostly small bushes.", "The plants grow in nutrient-poor soil.", "The summers are long and dry.",
          "Frequent fires occur."],
         ["It has tall rainforest trees.", "It rains every day throughout the year.", "The soil is very rich in nutrients."],
         ["Read the extract's description of the plants.", "What conditions must they survive?"], 1)]
q24 = [
    term("2.4.1", "Name ONE type of method used to determine the age of fossils other than carbon-14 dating.", ["relative dating",
                                                                                                                "relative"],
         ["It uses the order of rock layers.", "It gives no age in years."]),
    work("2.4.2(a)", "Find the value of A.", 2, [
        "A = 5 × 5 730\n= 28 650 years",           # the memo
        "A = 5 + 5 730\n= 5 735 years",            # added, not multiplied
        "A = 22 920 + 5\n= 22 925 years",          # 5 half-lives added as 5 years
        "A = 5 × 22 920\n= 114 600 years"],        # 5 × the previous row
        ["One half-life is 5 730 years.", "How many half-lives have passed at A?"]),
    work("2.4.2(b)", "Find the value of B.", 2, [
        "B = 25 ÷ 2\n= 12,5 %",                    # half of the previous row (the memo prints 2,5, flag)
        "B = 25 − 2\n= 23 %",                      # 2 subtracted
        "B = 25 × 2\n= 50 %",                      # doubled
        "B = 6,25 ÷ 2\n= 3,125 %"],                # halved from the wrong row
        ["Each half-life halves the carbon-14 left.", "What is half of 25%?"]),
    stmt("2.4.3", "Explain why it would not be possible to date a fossil which existed 80 million years ago using the decay of carbon-14.", 2,
         ["Carbon-14 has a short half-life (5 730 years).",
          "After about 50 000 years practically no carbon-14 is left, so an 80-million-year-old fossil has none to measure."],
         ["Carbon-14 has a half-life of 80 million years.", "Old fossils have more carbon-14 than young ones.",
          "Carbon-14 is only found in rocks, not in fossils."],
         ["How long is carbon-14's half-life?", "How much would be left after 80 million years?"], 1),
    stmt("2.4.4", "Describe how carbon-14 decay/radiometric dating is performed.", 5,
         ["Instruments measure the radioactive elements, e.g. uranium or carbon, in fossils or rocks.",
          "The more the radioactive element in a fossil has decayed, the older the fossil.",
          "For fossils older than 50 000 years, the age of the rocks in which they are embedded is determined.",
          "Carbon-14 dating measures the age of fossils younger than 50 000 years.",
          "The amount of the radioactive element left is used with its half-life to calculate the age."],
         ["The deeper the layer, the younger the fossil.", "The fossil is weighed to find its age.",
          "Carbon-14 dating works for fossils of any age."],
         ["Radioactive elements decay at a fixed rate.", "Which method suits young fossils, and which old ones?"], 1)]

# ---- SECTION B, QUESTION 3, the question paper pages 11-15 and the memo pages 7-10 ----
POTATO = {"head": ["TEMPERATURE (°C)", "AVERAGE YIELD PER PLANT, LOW LIGHT (kg)", "AVERAGE YIELD PER PLANT, HIGH LIGHT (kg)"],
          "rows": [["5", "0,5", "0,5"], ["10", "1,5", "2,5"], ["15", "3", "5"], ["20", "3,6", "8,5"], ["25", "3,5", "7,8"],
                   ["30", "2,5", "6,2"]]}
q31 = [
    stmt("3.1.1", "State TWO steps the investigator may have taken into consideration during the planning stage of the investigation.", 2,
         ["Ask permission from the owner of the farm.", "Decide on the duration of the investigation.",
          "Decide how to vary the temperature in the greenhouses.", "Decide on the measuring apparatus."],
         ["Record the yield of potatoes.", "Draw a graph of the results.", "Write a conclusion."],
         ["Planning happens before the investigation starts.", "Recording and concluding come later."], 1),
    term("3.1.2(a)", "Identify the independent variable", ["temperature", "light", "temperature and light", "light intensity",
                                                            "light level"],
         ["It is what the investigator changed.", "It is in the first column (or the light levels)."]),
    term("3.1.2(b)", "Identify the dependent variable", ["yield of potatoes", "average yield of potatoes", "yield of potatos", "potato yield",
                                                         "the yield of potatoes"],
         ["It is what was measured.", "It is in kg per plant."]),
    stmt("3.1.3", "State TWO ways in which the scientists could have improved the reliability of the investigation.", 2,
         ["Set up more plants in each greenhouse.", "Repeat the investigation."],
         ["Use only one plant.", "Change the temperature and light at random.", "Do the investigation only once."],
         ["Reliability comes from a bigger sample.", "And from repeating."], 1),
    draw("3.1.4", "Plot bar graphs on the same system of axes showing the results of the average yield of the potatoes from 20 °C to 30 °C for "
         "both light levels.", 6, [
        ["Correct type of graph (bar graph)", 1], ["Caption", 1], ["Labels on both axes with units", 1], ["Correct scale on both axes", 1],
        ["Plotting: all six bars plotted correctly", 2]],
        ["Two bars at each temperature: low and high light.", "Only 20, 25 and 30 °C."],
        memo="The memo's rubric: a bar graph, a caption, both axes labelled with units, the right scale and all six bars plotted.")]
q32 = [
    term("3.2.1", "Identify the type of cycle represented by the flow chart above.", ["carbon cycle"],
         ["Carbon dioxide in the atmosphere is at the top.", "Fossil fuels are at the bottom."]),
    term("3.2.2(a)", "Identify the process labelled C", ["decomposition", "decay"],
         ["It returns carbon from dead organic material to the air.", "Bacteria and fungi do it."]),
    term("3.2.2(b)", "Identify the process labelled A", ["cellular respiration", "respiration"],
         ["Both plants and animals do it.", "It releases carbon dioxide."]),
    term("3.2.2(c)", "Identify the process labelled B", ["photosynthesis"], ["Only plants do it.", "It takes carbon dioxide from the air."]),
    stmt("3.2.3", "Explain how process A produces carbon dioxide.", 2,
         ["Organic compounds in plants and animals are broken down in the presence of oxygen.", "Energy, water and carbon dioxide are released."],
         ["Carbon dioxide is absorbed from the air.", "Light energy is changed into chemical energy.",
          "Glucose is made from carbon dioxide and water."],
         ["Process A is respiration.", "What happens to glucose in respiration?"], 1),
    stmt("3.2.4", "Briefly describe the type of cycle identified in QUESTION 3.2.1.", 4,
         ["Carbon occurs as carbon dioxide in the atmosphere; some is dissolved in water.",
          "Green plants use carbon dioxide during photosynthesis to produce organic compounds.",
          "The carbon in the plants' organic compounds passes to animals when they eat plants.",
          "Some dead plant and animal remains do not decompose but form fossil fuels (coal and oil)."],
         ["Carbon is made by animals from nitrogen in the air.", "Plants release carbon dioxide only during photosynthesis.",
          "Fossil fuels form from rocks, not from living things."],
         ["Follow the arrows from carbon dioxide in the atmosphere.", "How does carbon get into plants, then animals?"], 1)]
q33 = [
    term("3.3.1", "Name the phenomenon that led to the world having separated continents.", ["continental drift"],
         ["The continents moved apart slowly.", "Wegener proposed it."]),
    term("3.3.2", "On which continent is the ostrich found?", ["africa"], ["Look at the map.", "It is on the right."]),
    term("3.3.3", "What is the unique characteristic that is common to the rhea and the ostrich?", ["flightless", "they are flightless",
                                                                                                    "cannot fly", "both are flightless"],
         ["They are large birds.", "Can they fly?"]),
    term("3.3.4", "What do we call the study of the distribution of existing and extinct organisms in different geographical areas?",
         ["biogeography"], ["'Bio' and 'geography' together.", "It explains where organisms are found."]),
    stmt("3.3.5", "Mention the two major supercontinents that South America and Africa belonged to.", 2,
         ["Gondwana (Gondwanaland)", "Pangaea"], ["Laurasia", "Eurasia", "Antarctica"],
         ["About 250 million years ago all land was one supercontinent.", "It split into a northern and a southern part."], 1),
    stmt("3.3.6", "Birds like the rhea and ostrich are different species, yet they share many similar characteristics. Explain how such similar "
                  "birds ended up on continents separated by a vast ocean.", 4,
         ["Both developed from a common ancestor.", "The ancestor lived on one continent, Gondwanaland.",
          "Then South America and Africa broke apart.", "Because of continental drift."],
         ["The birds flew across the ocean.", "Humans carried the birds between the continents.", "The two birds have no shared ancestor."],
         ["Were the continents always apart?", "What happened to the ancestor's population when they split?"], 1)]
q34 = [
    stmt("3.4.1", "Define mass extinction.", 2,
         ["Extinction when many species disappear over the same (short) period of time.",
          "The dying out of a large number of species at about the same time."],
         ["The death of one individual organism.", "When a species moves to a new area.", "When the population of a species grows quickly.",
          "The slow extinction of one species over millions of years."],
         ["'Mass' means many.", "Over how long a time?"], 2),
    answer("3.4.2", "When did the dinosaurs become extinct?", 1, ["65 MYA", "251 MYA", "200 MYA", "165 MYA"],
           ["Look for 'Dinosaur extinction' on the diagram.", "Read the date below it."]),
    term("3.4.3", "To which era did the Triassic, Jurassic and Cretaceous periods belong?", ["mesozoic", "mesozoic era"],
         ["Read the era above the three periods.", "It is the era of the dinosaurs."]),
    stmt("3.4.4", "Explain how dinosaurs might have become extinct.", 3,
         ["A giant meteor (asteroid) hit the earth.", "It filled the atmosphere with deadly gas, vaporised rock and dust.",
          "Volcanic eruptions may also have played a part."],
         ["Humans hunted the dinosaurs.", "An ice age started today.", "The dinosaurs ate all the plants and starved."],
         ["The diagram shows a falling object.", "What would a huge impact do to the air?"], 1),
    term("3.4.5(a)", "To which era do human beings belong?", ["cenozoic", "cenozoic era"], ["Humans live today.", "Read the last era."]),
    term("3.4.5(b)", "To which era did the ammonites (sea animals) belong, as shown on the diagram?", ["paleozoic", "palaeozoic",
                                                                                                        "paleozoic era"],
         ["Find the ammonite on the diagram.", "Read the era below it."]),
    term("3.4.6", "Which extinction took place toward the end of the Paleozoic era?", ["permian extinction", "permian"],
         ["Look at the line between the Paleozoic and the Mesozoic.", "It happened 251 MYA."])]
q35 = [
    mcq("3.5.1(a)", "Which diagram represents an artery?", ["A", "B"], 0, ["Arteries have thick muscular walls.", "Which lumen is smaller?"],
        marks=1),
    mcq("3.5.1(b)", "Which diagram represents a vein?", ["A", "B"], 1, ["Veins have thin walls.", "Which lumen is larger?"], marks=1),
    stmt("3.5.2", "Explain your answer to QUESTION 3.5.1 (a).", 2,
         ["It has a thick muscular wall, to withstand the pressure from the heart's pumping.", "Its lumen is smaller, which creates a higher "
                                                                                              "pressure."],
         ["It has a large lumen.", "It has valves.", "Its wall is thin."],
         ["Compare the walls of A and B.", "Compare the lumens."], 1, after=["3.5.1(a)"]),
    mcq("3.5.3", "Which blood vessel (A or B) has valves?", ["A", "B"], 1, ["Valves stop backflow at low pressure.", "Which vessel carries "
                                                                                                                    "blood at low pressure?"],
        marks=1),
    term("3.5.4(a)", "Provide the label for the part numbered 3", ["lumen"], ["It is the space in the middle.", "Blood flows through it."]),
    term("3.5.4(b)", "Provide the label for the part numbered 2", ["muscle layer", "muscle", "smooth muscle", "muscular layer"],
         ["It is the thick shaded layer.", "It contracts."]),
    term("3.5.4(c)", "Provide the label for the part numbered 1", ["connective tissue", "connective tissue layer", "outer layer"],
         ["It is the outermost layer.", "It holds the vessel in place."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 12, "items": q11},
    {"id": "1.1.7", "title": "Questions 1.1.7 and 1.1.8", "kind": "Multiple choice", "marks": 4,
     "lead": "Questions 1.1.7 and 1.1.8 are based on the diagram below.",
     "figure": P.fig("1.1.7", "A graph of the number of families (0 to 800) against millions of years ago (600 to 0), with the Paleozoic, "
                              "Mesozoic and Cenozoic eras along the bottom; the Ordovician and Permian extinctions in the Paleozoic and the "
                              "Cretaceous extinction near the end of the Mesozoic are marked as dips."), "items": q117},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 7,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 8,
     "lead": "Indicate whether each of the descriptions in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Classification", "marks": 7,
     "lead": "Organisms can be classified as eukaryotes and prokaryotes.", "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Food webs", "marks": 12,
     "lead": "The diagram below shows feeding relationships in an ecosystem.",
     "figure": P.fig("1.5", "A food web: carrots, grasses and grains at the bottom; arrows to rabbits, mice, grasshoppers and birds; and from "
                            "them to foxes and owls at the top."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "The heart", "marks": 16, "lead": "The diagram below shows the structure of a heart.",
     "figure": P.fig("2.1", "A section of the heart with labels A to F: A the large artery arching from the top, B the valve between the left "
                            "atrium and left ventricle, C the thick-walled left ventricle, D the right ventricle, E the valve between the "
                            "right atrium and right ventricle, F the right atrium."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Classification", "marks": 12,
     "lead": "A plant commonly known as a pine tree is classified as follows: Plantae, Pteridophyta, Gymnospermae, Corniferales, Pinaceae, "
             "Pinus, ponderosa.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Biomes", "marks": 10,
     "lead": "Read the extract below.\nThe Cape floral kingdom is the smallest of the world's floral kingdoms. It is home to more endemic "
             "(species that occur in one region and nowhere else in the world) and indigenous plants than any other region in South Africa. "
             "Approximately 70% of the 9 000 plant species in this area are found nowhere else in the world. The vegetation of this biome, "
             "which is mostly small bushes, grows in nutrient-poor soil. They also survive the long dry summer conditions, as well as "
             "frequent fires. The flora of the Cape is threatened, amongst others, by habitat destruction by humans. Already numerous "
             "species are extinct from this biome. Hence, its conservation is a national conservation priority. In a bid to save this "
             "biome, there are several projects aiming at encouraging responsible travel to natural areas in order to conserve the "
             "environment, as well as improving the well-being of local communities.", "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Dating fossils", "marks": 12, "table": C14,
     "lead": "Study the table below that shows the decay of carbon-14 over time (DECAY OF CARBON-14).", "items": q24},
    {"id": "3.1", "title": "Question 3.1", "kind": "Investigation: potato yield", "marks": 12, "table": POTATO,
     "lead": "The table below shows the results of a study that investigated the effect of temperature and light on the yield of potatoes in "
             "two greenhouses on a farm.", "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Nutrient cycles", "marks": 10,
     "lead": "The diagram below shows the flow chart of a particular cycle.",
     "figure": P.fig("3.2", "A flow chart: carbon dioxide in the atmosphere at the top; arrow B down to plants and arrows A up from plants "
                            "and from animals; plants pass food to animals; both die to dead organic material, which returns to the "
                            "atmosphere by C or forms fossil fuel, which returns by combustion."), "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Continental drift", "marks": 10,
     "lead": "The diagram below shows how South America and Africa were once joined in the past.",
     "figure": P.fig("3.3", "South America and Africa fitted together, a rhea drawn in South America and an ostrich in Africa."),
     "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Mass extinctions", "marks": 10,
     "lead": "The diagram below shows geological events in millions of years ago (MYA).",
     "figure": P.fig("3.4", "A time line: the Paleozoic era with an ammonite, the Permian extinction at 251 mya, the Mesozoic era (Triassic, "
                            "Jurassic from 200 mya, Cretaceous from 165 mya) with dinosaurs, the dinosaur extinction with a meteor at 65 mya, "
                            "and the Cenozoic era with humans to today."), "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Blood vessels", "marks": 8,
     "lead": "The diagram below shows a transverse section through two different blood vessels.",
     "figure": P.fig("3.5", "Two blood vessels in cross-section: A with a thick shaded middle layer and a small lumen, B with a thin middle "
                            "layer and a large lumen; 1 points to the outer layer, 2 to the middle layer, 3 to the lumen."), "items": q35}]

P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P2", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.4.2(b)", "kind": "memo_issue", "detail": "The memo gives B = 2,5; three half-lives leave 100 → 50 → 25 → 12,5 %, which the "
                                                            "table's next value (6,25 = half of 12,5) confirms. The right option is 12,5 %; "
                                                            "2,5 is in no option."},
          {"n": "3.3.5", "kind": "memo_issue", "detail": "The memo gives 'Laurasia and Gondwanaland'. South America and Africa were part of "
                                                         "Pangaea and then Gondwana; Laurasia was the northern supercontinent. The right cards "
                                                         "here are Gondwana and Pangaea; Laurasia is a wrong card. A science-over-memo call: "
                                                         "for Murci to confirm."},
          {"n": "1.5.4", "kind": "no_fit", "detail": "The food pyramid (1.5.4) and the bar graph (3.1.4) play as pick the drawing: the memo's "
                                                     "and three drawings that lose a rubric mark."}],
         {"1": 50, "2": 50, "3": 50}, 150, {"3.5.2": ["3.5.1(a)"]}, "Questions 1 to 3 (the whole paper)",
         sections=[("Section A", 50, None, ["1"]), ("Section B", 100, None, ["2", "3"])])
