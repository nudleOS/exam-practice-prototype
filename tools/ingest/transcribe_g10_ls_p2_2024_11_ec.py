"""Grade 10 Life Sciences P2 November 2024 (Eastern Cape Department of Education, provincial assessment), the whole paper (Questions
1 to 3, 150 marks, 2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options,
marks and answers are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md):
stanmorephysics.com, one scanned PDF of the paper (16 pages) and the marking guidelines (8 pages), split by page into QP and MG files
(no text layer), read from page images (100 dpi). A stand-in: no Grade 10 Life Sciences Nov 2025 paper is published.

  python tools/ingest/transcribe_g10_ls_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ls-p2-2024-11-ec/g10-ls-p2-2024-11-ec QP.pdf" "uploads/provincial/g10-ls-p2-2024-11-ec/g10-ls-p2-2024-11-ec MG.pdf" --id g10-ls-p2-2024-11-ec --from-json

The Life Sciences rulings, as in transcribe_g10_ls_p2_2024_11_nw.py: printed multiple choice as printed; terms typed; Column I /
Column II as A only / B only / both / none; a written answer as statements to pick; the calculation (2.2.5) as four workings; the
tabulated and 'differentiate' differences (2.5, 3.4.2, 3.6.4) as sorts; the bird key (2.3) as matching each key letter to its
scientific name; the energy pyramid (2.1.5) and the bar graph (2.2.7) as pick the drawing (pictures_lower.py). The paper's question
numbers are used: the memo numbers the chimpanzee questions 2.3.2 and the kingdoms 2.4; the paper prints the blood vessels as a
second 3.5 with parts 3.6.1-3.6.4, played as 3.6. Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi,
scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ls-p2-2024-11-ec", 595.32, 841.92, {
    "1.1.4": [3, 170, 470, 425, 568], "1.1.5": [4, 150, 108, 490, 278], "1.1.7": [4, 230, 528, 348, 633], "1.1.8": [5, 137, 82, 555, 289],
    "1.4": [7, 71, 100, 548, 512], "1.5": [8, 89, 163, 509, 433], "2.1": [9, 104, 181, 480, 429], "2.3": [11, 39, 112, 541, 252],
    "3.1": [13, 84, 127, 482, 312], "3.2": [13, 121, 463, 476, 663], "3.4": [14, 84, 358, 548, 681], "3.6": [15, 84, 260, 504, 422]},
    start=11)
work, answer, num, draw, stmt, mcq, term, sort = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term, P.sort
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})

# ---- SECTION A, QUESTION 1, the question paper pages 3-8 and the memo page 3 ----
q11 = [
    mcq("1.1.1", "An animal that has skin with hairs and nourishes its young with milk.", ["Amphibian", "Bird", "Mammal", "Reptile"], 2,
        ["Milk comes from mammary glands.", "Hair, not feathers or scales."]),
    mcq("1.1.2", "The chamber, found in the heart, that has the thickest wall?", ["Left atrium", "Left ventricle", "Right ventricle",
                                                                                "Right atrium"], 1,
        ["It pumps blood to the whole body.", "Ventricles pump harder than atria."]),
    mcq("1.1.3", "Which ONE of the following is a biotic factor?", ["Decomposers", "Light", "Water", "Soil"], 0,
        ["Biotic means living.", "The others are not alive."]),
    mcq("1.1.4", "The diagram shows part of the nitrogen cycle. Which process in the cycle is performed by bacterium X?",
        ["Decomposition", "Nitrification", "Nitrogen fixation", "Denitrification"], 3,
        ["X turns nitrates in the soil into nitrogen gas.", "It removes nitrogen from the soil."],
        figure=P.fig("1.1.4", "An arrow from 'nitrates in soil' through bacterium X up to 'nitrogen in the atmosphere', and an arrow from the "
                              "atmosphere back down to the soil.")),
    mcq("1.1.5", "The diagram shows a section through rock layers containing fossils. Which ONE of the following statements is CORRECT?",
        ["Mollusc shells are the most recent fossils", "Dinosaur bones are younger fossils than the mollusc shells",
         "Teeth and bones of mammals are of the same age as the dinosaur bones", "Fish skeletons are the oldest fossils"], 1,
        ["The lowest layer is the oldest.", "Mollusc shells are at the bottom."],
        figure=P.fig("1.1.5", "A cliff of rock layers, top to bottom: R teeth and bones of mammals, S dinosaur bones, T fish skeletons, "
                              "U mollusc shells; across the valley another cliff with layers W, X, Y (with shells) and Z.")),
    mcq("1.1.6", "The longest phase of the cardiac cycle is …", ["atrial systole.", "ventricular systole.", "ventricular diastole.",
                                                                   "general diastole."], 3,
        ["The heart rests longest.", "All the chambers relax."]),
    mcq("1.1.7", "The diagram shows a section of a human vein. The function of the part labelled X is …",
        ["to make sure the blood flows to the lungs.", "to make sure the blood flows to the brain.",
         "to make sure the blood flows to the kidneys.", "to make sure the blood flows to the heart."], 3,
        ["X is a valve.", "Veins carry blood back."],
        figure=P.fig("1.1.7", "A section of a vein with pocket-shaped flaps X on its inner walls.")),
    mcq("1.1.8", "Which of the following pathways transfers the most energy to humans?", ["Pathway A", "Pathway B", "Pathway C",
                                                                                       "Pathway D"], 1,
        ["Energy is lost at every step.", "The shortest chain."],
        figure=P.fig("1.1.8", "From green plants: A insects to birds to humans; B straight to humans; C fish to humans; D cow to humans."))]
q12 = [
    term("1.2.1", "Organisms that do not have a true nucleus", ["prokaryotes", "prokaryote", "prokaryotic organisms"],
         ["Pro means before.", "Bacteria are an example."]),
    term("1.2.2", "Species found in one area and nowhere else in the world", ["endemic", "endemic species", "endemism"],
         ["Only found here.", "Like the fynbos plants of the Cape."]),
    term("1.2.3", "The study of fossils", ["palaeontology", "paleontology"], ["Palaeo means old.", "-ology is the study."]),
    term("1.2.4", "The process of the formation of large sheets of ice called glaciers", ["glaciation"], ["Ice ages.", "Glaciers form."]),
    term("1.2.5", "The large variety of living organisms found on earth", ["biodiversity", "biological diversity"],
         ["Bio means life.", "Diversity means variety."]),
    term("1.2.6", "The group name given to the first life forms, such as bacteria, which developed on Earth about 3,8 billion years ago",
         ["monera", "kingdom monera"], ["A kingdom.", "Bacteria belong to it."]),
    term("1.2.7", "A region with distinct climate together with all the organisms that live in it", ["biome", "biomes"],
         ["Grassland, savanna, desert …", "Bigger than an ecosystem."]),
    term("1.2.8", "The path taken by the energy as it passes from one organism to the other in an ecosystem", ["food chain", "food chains"],
         ["One path, not a web.", "Grass → cow → human."])]
q13 = [
    abq("1.3.1", "Driven by human impact", "Continental drift", "6th mass extinction", 1, ["Continents move by themselves.",
                                                                                         "People are causing extinctions now."]),
    abq("1.3.2", "Plants adapted to live in very dry conditions", "Hydrophytes", "Mesophytes", 3,
        ["Hydro means water.", "Dry-climate plants are xerophytes."]),
    abq("1.3.3", "The scientific way of naming organisms in which the name has two terms", "Classification", "Binomial nomenclature", 1,
        ["Bi means two.", "Classification is grouping."]),
    abq("1.3.4", "Physiographic factor/s", "Aspect", "Altitude", 2, ["Physiographic means the shape of the land.",
                                                                    "Which way a slope faces, and how high it is."])]
q14 = [
    term("1.4.1", "Name the type of timescale shown above.", ["geological", "geological timescale", "geological time scale", "geologic"],
         ["Eras and periods.", "It is measured in millions of years."]),
    term("1.4.2(a)", "In which period did dinosaurs first appear?", ["triassic"], ["Find 'first dinosaurs'.", "Read the period beside it."]),
    term("1.4.2(b)", "In which era did humans first appear?", ["cenozoic", "caenozoic", "cainozoic"],
         ["Find 'evolution of humans'.", "Read the era column."]),
    term("1.4.3", "In which period did an explosion (a large increase) in the number and diversity of life on Earth take place?",
         ["cambrian"], ["The Cambrian explosion.", "First chordates and fishes."]),
    term("1.4.4", "Identify the period during which by its end the worst mass extinction took place, wiping out approximately 90% of the "
                  "species.", ["permian"], ["Find 'major extinctions'.", "Before the Triassic."]),
    stmt("1.4.5", "Give TWO reasons why there are gaps in the fossil record.", 2,
         ["Not all organisms become fossilised.", "Some fossils have not yet been found."],
         ["All organisms become fossils when they die.", "Fossils are made only of soft tissue.", "Every fossil has already been found."],
         ["Fossils form only in special conditions.", "Not all have been dug up."], 1),
    stmt("1.4.6", "Name TWO other places that fossils are formed, other than in sedimentary rocks.", 2,
         ["Ice", "Tar", "Amber (resin)"], ["Lava", "Clouds", "Ocean waves"], ["Places that stop decay.", "Mammoths in ice."], 1)]
q15 = [
    stmt("1.5.1", "Write down the LETTER and NAME of the blood vessel that transports blood to the lungs.", 2,
         ["C – pulmonary artery"], ["B – aorta", "A – vena cava", "D – pulmonary artery", "B – pulmonary artery"],
         ["Arteries carry blood away from the heart.", "Which vessel leaves the right ventricle?"], 2),
    stmt("1.5.2", "Describe the type of blood that is found in blood vessel A.", 1,
         ["Deoxygenated blood: less oxygen, rich in carbon dioxide."],
         ["Oxygenated blood rich in oxygen.", "Blood with no red cells.", "Blood rich in digested food only.", "Blood with no carbon dioxide."],
         ["A brings blood from the body.", "The body has used the oxygen."], 1),
    term("1.5.3", "Which chamber of the heart contains the pacemaker in its wall?", ["right atrium"], ["The SA node.", "An upper chamber."]),
    term("1.5.4", "Give the NAME of the part that prevents oxygenated and deoxygenated blood from mixing.", ["septum"],
         ["The wall down the middle.", "It divides left from right."]),
    stmt("1.5.5", "Give ONE significance of one ventricle wall that is thicker than the other in a human heart.", 1,
         ["It enables the left ventricle to pump blood forcefully to the rest of the body."],
         ["It lets the right ventricle pump blood to the brain.", "It slows the heart down.", "It stores extra blood.",
          "It stops blood entering the heart."], ["Which ventricle pumps furthest?", "To the whole body."], 1),
    stmt("1.5.6", "Describe the function of valve E.", 2,
         ["It prevents blood flowing back into the right ventricle", "when the ventricle relaxes."],
         ["It pumps blood into the lungs.", "It lets blood flow back into the atrium.", "It mixes oxygenated and deoxygenated blood."],
         ["Valves stop backflow.", "When does backflow happen?"], 1),
    stmt("1.5.7", "Describe how the blood flow will be affected if part F is damaged and cannot open properly.", 1,
         ["Less blood enters the left ventricle: the heart must work harder."],
         ["More blood enters the left ventricle.", "Blood flows straight to the lungs.", "The blood flow is not affected.",
          "The blood turns deoxygenated."], ["F is a valve into the left ventricle.", "If it does not open …"], 1)]

# ---- SECTION B, QUESTION 2, the question paper pages 9-12 and the memo pages 4-6 ----
q21 = [
    stmt("2.1.1", "Define an ecosystem.", 2,
         ["A well-defined area in which plants, animals and the environment closely interact.",
          "An area where living organisms interact with each other and with their non-living environment."],
         ["A group of the same species living together.", "The study of fossils.", "A region with a distinct climate only.",
          "A single food chain."], ["An area.", "Living and non-living interact."], 2),
    term("2.1.2", "Identify the diagram above.", ["food web", "a food web"], ["Many food chains linked.", "Not one chain."]),
    term("2.1.3(a)", "Name ONE organism that represents a primary consumer.", ["bee", "hare", "rabbit", "grouse", "beetle"],
         ["It eats the plant.", "An arrow from the heather to it."]),
    term("2.1.3(b)", "Name ONE organism that represents a producer.", ["heather"], ["It makes its own food.", "The plant."]),
    term("2.1.3(c)", "Name ONE organism that represents a tertiary consumer.", ["adder", "eagle"],
         ["Three steps from the plant.", "It eats a secondary consumer."]),
    stmt("2.1.4(a)", "If all the shrews were removed from this ecosystem, explain what would happen to the population of the adder.", 2,
         ["The adder population would decrease.", "The adders would have no food to eat.",
          "They would need to find another source of food, or emigrate."],
         ["The adder population would increase.", "The adders would eat more heather.", "Nothing would change for the adders."],
         ["What does the adder eat?", "Only one food source."], 1),
    stmt("2.1.4(b)", "If all the shrews were removed from this ecosystem, explain what would happen to the population of the beetle.", 2,
         ["The beetle population would increase.", "They are no longer eaten by the shrews: only the grouse eats them."],
         ["The beetle population would decrease.", "The beetles would have no food.", "The beetles would eat the adders."],
         ["Shrews eat beetles.", "Fewer predators."], 1),
    draw("2.1.5", "Draw a food pyramid to show energy flow to the adder if the producer contains 5 500 kJ/m²/year of energy and only 14% of "
                  "this energy is passed on from one trophic level to the next.", 5,
         [["Heading", 1], ["The right organisms at each level with the right energy content", 4]],
         ["Heather → beetle → shrew → adder.", "Multiply by 0,14 at each step."],
         memo="The memo's pyramid of energy: heather 5 500, beetle 770, shrew 108 kJ/m²/year and the adder 15 kJ at the top."),
    stmt("2.1.6", "Use the food chains in the diagram to explain why the chances of survival of the stoat are higher than that of the adder.",
         2, ["The adder has one source of food, the shrew.", "The stoat eats shrews, hares and rabbits: if the shrews die out it has other food."],
         ["The adder eats more kinds of food than the stoat.", "The stoat is a producer.", "The eagle protects the stoat."],
         ["Count the arrows into each.", "More food sources, better survival."], 1)]
PLANTS = {"head": ["Plant", "Start mass (g)", "End mass (g)", "Increase (g)"],
          "rows": [["Aloe", "800", "842", "42"], ["Prickly Pear", "800", "853", "53"], ["Spekboom", "800", "896", "96"]]}
q22 = [
    term("2.2.1(a)", "Identify the independent variable.", ["type of plant", "types of plants", "type of plants", "different plants",
                                                            "the type of plant", "plant type"], ["What was changed.", "Three different …"]),
    term("2.2.1(b)", "Identify the dependent variable in this investigation.",
         ["absorption of co2", "rate of absorption of co2", "co2 absorption", "rate of co2 absorption", "absorption of carbon dioxide",
          "rate of absorption of carbon dioxide", "carbon dioxide absorption", "absorption of co₂", "rate of absorption of co₂"],
         ["What they wanted to measure.", "The aim of the investigation."]),
    stmt("2.2.2", "State the purpose of measuring the starting weight/mass of the plants.", 1,
         ["To have a baseline (control), to compare with the results after carbon dioxide has been absorbed."],
         ["To make the plants grow faster.", "To choose the heaviest plant.", "To water the plants correctly.", "To measure the CO₂ directly."],
         ["What is the end mass compared with?", "A starting point."], 1),
    stmt("2.2.3", "Give TWO ways that Lilitha and Mila used to ensure the validity of their investigation.", 2,
         ["They chose plants of the same height.", "They put the plants in equal-sized pots.", "All the plants had the same amount of soil.",
          "All the plants were in the same location.", "All the plants received the same amount of water."],
         ["They used three different types of plants.", "They measured the plants after one month.", "They bought the plants from a nursery."],
         ["What did they keep the same?", "Read the bullets."], 1),
    stmt("2.2.4", "Give ONE way in which the reliability of their investigation could be improved.", 1,
         ["Repeat the investigation.", "Use more plants of each type."],
         ["Use only one plant.", "Measure the plants only once.", "Give each plant a different amount of water."],
         ["Reliability: would you get the same results again?", "Repeat, or more samples."], 1),
    work("2.2.5", "Calculate the percentage increase in mass from the start to the end of the investigation of the spekboom plant. Show ALL "
                  "your working.", 3,
         ["{96}/{800} × 100\n= 12%", "{896}/{800} × 100\n= 112%", "{96}/{896} × 100\n= 10,71%", "{800}/{96} × 100\n= 833,33%"],
         ["The increase over the starting mass.", "Then × 100."]),
    stmt("2.2.6", "Explain how using the weight gain of the plants will give Lilitha and Mila an idea of how much CO₂ the plants are absorbing.",
         2, ["Plants use CO₂ to make organic compounds (carbohydrates),", "which they use to grow,", "and the more they grow, the more weight "
                                                                                                    "they gain."],
         ["Plants release CO₂ and become lighter.", "The soil absorbs the CO₂.", "Water makes the plants heavier, not CO₂."],
         ["Photosynthesis uses CO₂.", "Growth adds mass."], 1),
    draw("2.2.7", "Plot a bar graph of the weight/mass increase of the three plants.", 6, [
        ["Correct type of graph", 1], ["Correct caption (both variables)", 1], ["X and Y axes labels with the unit", 1],
        ["Scales, bars the same width and equal spaces between them", 1], ["All 3 bars plotted correctly", 2]],
        ["Type of plant on the x-axis.", "Use the increase column."],
        memo="The memo's rubric: type, caption, labels with the unit, scale and equal bars, the three increases (42, 53 and 96 g).")]
BIRDS = ["Ammodrammas bairdii", "Buceros rhinoceros", "Pandion hallaetus", "Haliaeetus lucocephalus", "Rynchops niger",
         "Recurvirostra avosetta"]
q23 = [
    {"t": "match", "n": "2.3", "marks": 6, "q": "Use the key to identify each bird. Match each letter A-F with its correct scientific name.",
     "clues": ["Start at 1: is the beak longer or shorter than the head?", "Follow the 'Go to' steps for each bird."],
     "left": ["A", "B", "C", "D", "E", "F"], "right": BIRDS, "a": [3, 4, 5, 1, 0, 2], "each": 1, "heads": ["LETTER", "SCIENTIFIC NAME"]}]
q24 = [
    term("2.4.1", "According to Linnaeus' system, to which class does the chimpanzee belong?", ["mammalia"],
         ["The third group in the list.", "Kingdom, phylum, class …"]),
    term("2.4.2", "Write correctly the scientific name of the chimpanzee.", ["pan troglodytes"], ["Genus, then species.",
                                                                                                "The last two names."], marks=2),
    term("2.4.3", "Identify the genus to which the chimpanzee belongs.", ["pan"], ["The second last name.", "Written with a capital."]),
    stmt("2.4.4", "State TWO reasons why organisms are given scientific names.", 2,
         ["To avoid confusion: to be accurate.", "Common names vary from region to region."],
         ["Scientific names are easier to pronounce.", "To make the names longer.", "Every language uses a different scientific name."],
         ["One organism, one name.", "Common names differ."], 1)]
q25 = [
    sort("2.5", "Differentiate between organisms grouped under kingdom Animalia and Plantae.", ["Animalia", "Plantae"],
         [("Depend on other organisms for food", 0), ("Cells do not have cell walls", 0), ("Manufacture their own food", 1),
          ("Cells have cell walls and chloroplasts", 1)],
         ["Food and cell walls.", "Plants photosynthesise."])]

# ---- QUESTION 3, the question paper pages 13-16 and the memo pages 6-8 ----
q31 = [
    term("3.1.1(1)", "Identify process 1, which leads to an increase in carbon in the atmosphere.", ["combustion", "burning"],
         ["Fossil fuels in transport and industry.", "Burning."]),
    term("3.1.1(3)", "Identify process 3, which leads to an increase in carbon in the atmosphere.", ["respiration", "cellular respiration"],
         ["Animals release CO₂.", "Breathing out."]),
    term("3.1.1(4)", "Identify process 4, which leads to an increase in carbon in the atmosphere.", ["decomposition", "decay"],
         ["Dead plants and animals.", "Decomposers break them down."]),
    stmt("3.1.2", "Identify process number 2 and explain its effect in the carbon cycle in ecosystems.", 3,
         ["Photosynthesis", "It reduces the concentration of carbon dioxide in the atmosphere,", "by trapping it to manufacture food."],
         ["Respiration", "It increases the carbon dioxide in the atmosphere.", "It releases carbon from fossil fuels."],
         ["Arrow 2 goes from the atmosphere to the plants.", "Plants take in CO₂."], 1)]
q32 = [
    term("3.2.1", "What do we call the study of the distribution of existing and extinct plant and animal species in specific areas on Earth?",
         ["biogeography"], ["Bio plus geography.", "Where living things are found."]),
    term("3.2.2", "Name the supercontinent that all these continents were originally part of.", ["pangaea", "pangea"],
         ["All the land in one.", "Pan means all."]),
    stmt("3.2.3", "Describe how the continental drift which led to the current distribution of camel species happened.", 4,
         ["The continents were originally one landmass called Pangaea.", "It broke into Laurasia and Gondwanaland (225-200 million years ago).",
          "Gondwanaland formed South America, Africa, Madagascar, Australia, India and Antarctica.",
          "Laurasia formed North America, Europe, the Middle East, Asia and China."],
         ["The continents have always been in the same place.", "Camels swam across the oceans.", "Laurasia formed South America and Africa."],
         ["One landmass, then two, then today's continents.", "Name them."], 1)]
q33 = [
    stmt("3.3.1", "Describe how a fossil is formed in sedimentary rocks.", 5,
         ["The organism dies and is covered rapidly by sediment (silt).", "The flesh decays and only the bone is left.",
          "As time passes, layers of sediment build up over the body.", "The layers are compressed by immense pressure.",
          "Minerals begin to replace the animal tissues,", "and the body petrifies."],
         ["The organism is burned by lava.", "The body floats on top of the sediment for ever."],
         ["Buried, then pressed, then replaced by minerals.", "In order."], 1),
    stmt("3.3.2", "Name TWO methods by which the age of fossils can be determined.", 2,
         ["Relative dating", "Radiometric dating"], ["Carbon counting by eye", "Weighing the fossil", "Measuring the fossil's length"],
         ["One compares layers.", "One uses radioactive decay."], 1)]
q34 = [
    stmt("3.4.1", "List THREE similarities ONLY shared between Ornitholestes (dinosaur) and Archaeopteryx.", 3,
         ["Long tail", "Clawed hands", "Spiky, sharp (serrated) teeth"], ["Furcula (wishbone)", "Large breastbone", "No teeth"],
         ["Shared by these two, not by the pigeon.", "Tail, hands, teeth."], 1),
    sort("3.4.2", "Tabulate TWO differences between a pigeon and the Archaeopteryx.", ["Pigeon", "Archaeopteryx"],
         [("Short 'parson's nose'", 0), ("No teeth", 0), ("A large breastbone", 0), ("Long bony tail", 1), ("Spiky teeth", 1)],
         ["Read the labels on each skeleton.", "Tail, teeth, breastbone."]),
    stmt("3.4.3", "Archaeopteryx seemed to be part bird and part dinosaur. Explain the significance of this.", 2,
         ["It is a transitional fossil.", "It shows intermediate characteristics.", "It is evidence for evolution."],
         ["It proves that birds came before dinosaurs.", "It shows that dinosaurs never existed.", "It is the oldest fossil on Earth."],
         ["Between two groups.", "What does it suggest about change over time?"], 1)]
q35 = [
    stmt("3.5", "Scientists discovered that five major extinction events occurred over time. The meteors which crashed into the Earth caused "
                "enormous permanent losses in biodiversity. Explain how the impact affected the planet to cause these major losses of life.", 4,
         ["Large amounts of dust moved up and blocked out the sun,", "leading to less photosynthesis,", "and therefore less oxygen and food.",
          "The temperature on Earth decreased.", "Many organisms went extinct, as they could not adapt."],
         ["The meteors added oxygen to the air.", "More sunlight reached the Earth.", "Plants grew faster after the impact."],
         ["Dust and the sun.", "Food chains start with plants."], 1)]
q36 = [
    term("3.6.1(a)", "Identify the type of blood vessel in Diagram B.", ["vein"], ["A wide lumen, a thinner wall.", "Not an artery."]),
    term("3.6.1(b)", "Identify the type of blood vessel in Diagram A.", ["artery"], ["A thick muscle layer.", "A narrow lumen."]),
    stmt("3.6.2", "Explain why the blood vessel in Diagram A has a thicker smooth muscle layer.", 2,
         ["To withstand the high pressure", "created by the pumping of the heart."],
         ["To store blood.", "Because blood flows slowly in it.", "To let oxygen diffuse through it."],
         ["Arteries leave the heart.", "Pressure."], 1),
    stmt("3.6.3", "Explain ONE structural adaptation of the blood vessel in Diagram C.", 2,
         ["Its wall is a single layer of cells,", "so oxygen and nutrients diffuse into the tissues (and CO₂ and wastes out)."],
         ["It has a thick muscle layer to pump blood.", "It has valves to stop backflow.", "It has a wide lumen to carry more blood."],
         ["C is a capillary.", "Thin walls, then what?"], 1),
    sort("3.6.4", "Tabulate TWO differences between the composition of blood in the pulmonary artery and in the pulmonary vein.",
         ["Pulmonary artery", "Pulmonary vein"],
         [("High level of carbon dioxide", 0), ("Low level of oxygen", 0), ("Deoxygenated blood", 0), ("Low level of carbon dioxide", 1),
          ("High level of oxygen", 1)],
         ["The pulmonary artery goes to the lungs.", "The pulmonary vein comes back from them."])]
CHOL = ("Your liver makes cholesterol for your body. You also can get cholesterol from the foods you eat. Meat, fish, eggs, butter, cheese, "
        "and milk all have cholesterol in them. Fruits, vegetables, and grains (like oatmeal) don't have any cholesterol.\nCholesterol is in "
        "every cell in your body. You need cholesterol to help your brain, skin, and other organs do their jobs. But eating too much fat and "
        "cholesterol is a bad idea.\nCholesterol floats around in your blood and can stick into the walls of the blood vessels. This can "
        "cause the blood vessels to get stiffer, narrower, or clogged. If clogging gets worse over many years, it can cause a heart attack or "
        "stroke in adults.")
q37 = [
    stmt("3.7.1", "From the extract above, give ONE food type without cholesterol.", 1, ["Fruit", "Vegetables", "Grains"],
         ["Meat", "Eggs", "Butter"], ["Read the first paragraph.", "Plant foods."], 1),
    stmt("3.7.2", "Explain what would happen if someone ate food with too much cholesterol over a long period of time.", 2,
         ["Cholesterol sticks to the walls of the blood vessels,", "the blood vessels get stiffer, narrower or clogged,",
          "resulting in a heart attack or stroke."],
         ["The blood vessels get wider.", "The liver stops making blood.", "Cholesterol is broken down in the stomach."],
         ["Read the last paragraph.", "Walls, narrowing, then what?"], 1)]
q38 = [
    stmt("3.8", "Describe the events that occur during the ventricular systole of the cardiac cycle.", 3,
         ["The left and right ventricles contract.", "The atria relax.", "The right ventricle pushes blood into the pulmonary artery.",
          "The left ventricle pushes blood into the aorta.", "The bicuspid and tricuspid valves close to prevent backflow."],
         ["The ventricles relax and fill with blood.", "The atria contract.", "The semilunar valves close."],
         ["Systole means contraction.", "Which chambers, which vessels, which valves?"], 1)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 16, "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 8,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 8,
     "lead": "Indicate whether each of the descriptions in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "The geological timescale", "marks": 9,
     "lead": "The table below is a timescale showing how life has changed over time.",
     "figure": P.fig("1.4", "Eras, periods and events from 650 million years ago: Late Proterozoic first soft-bodied animals; Cambrian first "
                            "chordates and fishes; Ordovician sudden diversification; Silurian first vascular land plants; Devonian first "
                            "amphibians; Carboniferous first reptiles; Permian major extinctions; Triassic first mammals and dinosaurs; "
                            "Jurassic first birds; Cretaceous first flowering plants and primates, extinction of dinosaurs; Paleogene and "
                            "Neogene mammals diversify; Quaternary (Cenozoic) evolution of humans."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "The heart", "marks": 9, "lead": "Study the diagram of the heart.",
     "figure": P.fig("1.5", "A section of the heart: A the large vessel entering at the top right of the picture with a downward arrow, B "
                            "the arch leaving the top, C a vessel branching from the top, D the upper chamber on the picture's left, E the "
                            "valves between that side's chambers, F a valve on the picture's right."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Ecosystems", "marks": 17, "lead": "Study the diagram of organisms in an ecosystem.",
     "figure": P.fig("2.1", "Heather eaten by the bee, hare, rabbit, grouse and beetle; the beetle eaten by the grouse and the shrew; the "
                            "shrew eaten by the stoat and the adder; the hare and rabbit eaten by the stoat and the eagle; the grouse "
                            "eaten by the eagle."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Investigation: CO₂ absorption", "marks": 17, "table": PLANTS,
     "lead": "Lilitha and Mila learnt that the spekboom plant is very good at absorbing carbon dioxide from the atmosphere. This helps prevent "
             "the extreme increase in the Earth's temperature called global warming. This carbon dioxide is used by plants to manufacture "
             "their own food by photosynthesis. They decided to investigate the rate at which different plants absorb CO₂.\n• They obtained "
             "THREE different types of plants from their local nursery (a spekboom, an aloe and a prickly pear).\n• They made sure that the "
             "plants are of the same height.\n• They planted the plants in equal-sized pots with the same amount of soil.\n• All three plants "
             "were placed in the same location and received equal amounts of water.\n• They measured the weight/mass of their plants in the "
             "pots at the start of the investigation.\n• They then left the plants to grow for one month and measured their weight/mass "
             "again.\nThe results are shown in the table below.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Identification key", "marks": 6,
     "lead": "Study the birds below and the key.\n1(a) Beak is longer than the head: go to 2. (b) Beak is shorter than the head: go to 3.\n"
             "2(a) Beak curves upwards: C. (b) Beak does not curve upwards: go to 4.\n3(a) Top part of the beak is hooked over the bottom "
             "part: go to 5. (b) Top part of the beak is not hooked over the bottom part: E.\n4(a) Top part of the beak is shorter than the "
             "bottom part: B. (b) Has a large projection above the beak: D.\n5(a) Head has a stripe: F. (b) Head does not have a stripe: A.",
     "figure": P.fig("2.3", "Six bird heads, named: Ammodrammas bairdii (a short pointed beak, a striped head), Buceros rhinoceros (a large "
                            "curved beak with a horn above it), Pandion hallaetus (a hooked beak, a dark stripe through the eye), "
                            "Haliaeetus lucocephalus (a hooked beak, a plain white head), Rynchops niger (a long beak, the lower part "
                            "longer), Recurvirostra avosetta (a long thin beak curving upwards)."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Classification", "marks": 6,
     "lead": "Read the extract below.\nCarolus Linnaeus established a hierarchical classification system of grouping similar organisms "
             "together. He grouped them from broad groups called Kingdoms down to the smallest group called species.\nUsing his system a "
             "chimpanzee is fully classified as follows: Animalia, Chordata, Mammalia, Primates, Hominidae, Pan, Troglodytes", "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Kingdoms", "marks": 4, "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "The carbon cycle", "marks": 6, "lead": "The diagram below shows part of a carbon cycle.",
     "figure": P.fig("3.1", "Fossil fuels (coal and oil) feed transport and industry and power, which give off carbon dioxide (1) to the "
                            "atmosphere; carbon dioxide goes to the plants (2); animals give carbon dioxide back (3); plants and animals "
                            "die and return carbon dioxide (4)."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Biogeography", "marks": 6,
     "lead": "The diagram below shows the distribution of members of the camel family on different continents. The arrows indicate the current "
             "distribution of the different species.",
     "figure": P.fig("3.2", "A world map: the dromedary in North Africa and Arabia, the Bactrian camel in central Asia, the llama in western "
                            "South America."), "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Fossils", "marks": 7, "lead": "The questions below are based on fossils.", "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Archaeopteryx", "marks": 10,
     "lead": "Archaeopteryx is an early prehistoric bird dating from 150 million years ago. A total of EIGHT fossils of archaeopteryx have been "
             "found in Germany. It lived during the Jurassic period when many dinosaurs lived. Archaeopteryx seemed to be part bird and part "
             "dinosaur. The diagram below shows the structure of three closely related organisms.",
     "figure": P.fig("3.4", "Three skeletons: Ornitholestes (sharp serrated teeth, short arms, a 3-clawed hand, pubis forward, a long tail); "
                            "Archaeopteryx (spiky teeth, long neck, furcula or wishbone, long arms with wing-like proportions, a long bony "
                            "tail, pubis bird- or reptile-like, reversed 1st toe); Pigeon (no teeth, long neck, furcula, a clawless hand, "
                            "pubis rotated backward, a large breastbone, a short 'parson's nose', reversed 1st toe)."), "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Mass extinctions", "marks": 4, "items": q35},
    {"id": "3.6", "title": "Question 3.6", "kind": "Blood vessels", "marks": 11,
     "lead": "Diagrams A, B and C below represent THREE types of blood vessels.",
     "figure": P.fig("3.6", "Three cross-sections: A a thick wall with a thick smooth muscle layer and a small lumen; B a thinner wall with a "
                            "thinner muscle layer and a wide lumen; C a single thin ring."), "items": q36},
    {"id": "3.7", "title": "Question 3.7", "kind": "Cholesterol", "marks": 3, "lead": "Read the extract below.\n" + CHOL, "items": q37},
    {"id": "3.8", "title": "Question 3.8", "kind": "The cardiac cycle", "marks": 3, "items": q38}]

P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P2", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
         [P.flag_workings(),
          {"n": "2.2.7", "kind": "memo_issue", "detail": "The memo's bar graph draws the increases as about 32, 43 and 71 g; the table gives 42, "
                                                         "53 and 96 g. The right drawing plots the table's values. For Murci to confirm."},
          {"n": "3.5", "kind": "low_confidence", "detail": "The paper prints 3.5 (4); the memo gives (5) for any of seven points. The paper's 4 "
                                                           "is used: it totals Question 3 to 50."},
          {"n": "1.5.6", "kind": "low_confidence", "detail": "The paper prints 1.5.6 (2); the memo ticks one point. The memo's point plays as "
                                                             "two cards (what the valve prevents, and when), 1 mark each."},
          {"n": "2.1.5", "kind": "no_fit", "detail": "The energy pyramid (2.1.5) and the bar graph (2.2.7) play as pick the drawing: the "
                                                     "memo's and three that lose marks."}],
         {"1": 50, "2": 50, "3": 50}, 150,
         {}, "Questions 1 to 3 (the whole paper)",
         sections=[("Section A", 50, None, ["1"]), ("Section B", 100, None, ["2", "3"])])
