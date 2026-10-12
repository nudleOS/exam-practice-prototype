"""Grade 11 Life Sciences P2 November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 3, 150 marks,
2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and answers are
the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2025 November Grade
11, the question paper zip (English PDF, 17 pages, text layer) and the memo zip (English, 11 pages).

  python tools/ingest/transcribe_g11_ls_p2_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ls-p2-2025-11-ec/LIFE SCIENCES P2 QP GR11 NOV 2025 ENG_watermark.pdf" "uploads/provincial/g11-ls-p2-2025-11-ec/LIFE SCIENCES P2 MEMO GR11 NOV 2025 ENG_watermark.pdf" --id g11-ls-p2-2025-11-ec --from-json

The Life Sciences rulings, as in transcribe_g11_ls_p1_2025_11_ec.py: a tabulated difference (2.2.3) plays as a sort; the one
calculation (3.1.3) as four workings; the graph to draw (3.3.4) as pick the drawing (pictures_lower.py: bars). Figure boxes are in PDF
points (text blocks and image rects), 1% inside their neighbours."""
from provincial import Paper

P = Paper("g11-ls-p2-2025-11-ec", 595.32, 842.04, {
    "1.1.6": [4, 115.0, 105.0, 486.0, 372.0], "1.1.9": [5, 133.0, 141.0, 502.0, 353.0], "1.4": [7, 90.0, 88.0, 505.0, 320.0],
    "1.5": [8, 91.0, 92.0, 499.0, 394.0], "2.1": [9, 80.0, 141.0, 517.0, 438.0], "2.2": [10, 130.0, 88.0, 464.0, 431.0],
    "2.3": [11, 85.0, 104.0, 507.0, 540.0], "2.4": [12, 79.0, 104.0, 514.0, 339.0], "2.5": [13, 82.0, 104.0, 510.0, 333.0],
    "3.2": [15, 91.0, 187.0, 477.0, 459.0]}, start=8)
work, answer, num, draw, stmt, mcq, term, sort = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term, P.sort
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})

# ---- SECTION A, QUESTION 1, the question paper pages 3-8 and the memo pages 4-5 ----
q11 = [
    mcq("1.1.1", "Organisms that cannot move since they are permanently attached to a surface are known as …", ["autotrophic.", "sessile.",
                                                                                                                "porifera.", "motile."], 1,
        ["They stay in one place.", "Motile means able to move."]),
    mcq("1.1.2", "Which of the following is the role of micro-organisms in the nitrogen cycle?", ["Photosynthesis", "Binary fission",
                                                                                                  "Nitrification", "Cause diseases"], 2,
        ["Which one is a step in the cycle?", "Bacteria turn ammonia into nitrates."]),
    mcq("1.1.3", "A feature of a developing country is …", ["an expanding older age population.", "a decreasing younger age population.",
                                                            "inadequate health facilities.", "a high literacy rate."], 2,
        ["Developing countries have many young people.", "Think of resources."]),
    mcq("1.1.4", "Flowers with large, feathery stigmas to catch pollen are …", ["wind pollinated.", "insect pollinated.", "bird pollinated.",
                                                                                "water pollinated."], 0,
        ["Feathery stigmas sieve the air.", "No pollinator needed."]),
    mcq("1.1.5", "A common characteristic for all micro-organisms is that they are …", ["Found only in soil.", "photosynthetic.", "microscopic.",
                                                                                        "harmful."], 2,
        ["Micro- means small.", "Many are useful."]),
    mcq("1.1.6", "The diagram below represents a process that negatively affects marine life. Which ONE of the following descriptions "
        "represents the process and events occuring in this habitat?",
        ["Eutrophication · nutrients increase · aquatic organisms survive", "Algal bloom · nutrients increase · aquatic organisms survive",
         "Eutrophication · nutrients decrease · aquatic organisms die", "Algal bloom · nutrients increase · aquatic organisms die"], 3,
        ["Water enriched with photosynthetic protozoa: an algal bloom.", "The bloom uses up the oxygen."],
        figure=P.fig("1.1.6", "A water body under the sun: the surface is thick with photosynthetic protozoa ('water enriched with "
                              "photosynthetic protozoan'), with aquatic organisms, a fish and plants below."),
        optTable={"head": ["PROCESS", "NUTRIENTS (NITROGEN, PHOSPHORUS)", "AQUATIC ORGANISMS"],
                  "rows": [["Eutrophication", "Increase", "Survive"], ["Algal bloom", "Increase", "Survive"], ["Eutrophication", "Decrease",
                                                                                                              "Die"],
                           ["Algal bloom", "Increase", "Die"]]}),
    mcq("1.1.7", "Which ONE of the following factors has yielded better crops that have contributed to the human exponential growth over the "
        "past century?", ["Ozone layer depletion", "Technological improvements", "Agricultural improvements", "Medicinal improvements"], 2,
        ["Better crops.", "Farming."]),
    mcq("1.1.8", "Viruses are considered living only when they …", ["are in soil.", "contain RNA.", "have a nucleus.",
                                                                   "reproduce inside a host cell."], 3,
        ["Outside a cell a virus does nothing.", "Reproduction is a sign of life."]),
    mcq("1.1.9", "The diagram below represents an interaction in a particular ecosystem. Both populations undergo logistic growth. What is "
        "likely to happen to the logistic growth form over the course of these species' survival?",
        ["The population size of B will always increase exponentially due to unlimited resources",
         "The population size of both A and B will always increase",
         "Population size of both A and B fluctuates over time with the species B population increasing first",
         "Population size of both A and B fluctuates over time with the population of A increasing first"], 2,
        ["A is the predator, B the prey.", "Prey numbers rise before predator numbers."],
        figure=P.fig("1.1.9", "A wolf, A, about to catch a rabbit, B."))]
q12 = [
    term("1.2.1", "A diagram that shows the distribution of age and gender for a population", ["age-gender pyramid", "age gender pyramid",
                                                                                               "population pyramid", "age-sex pyramid"],
         ["Its shape names it.", "Males on one side, females on the other."]),
    term("1.2.2", "A plant structure that contains an embryo which results from a fertilised ovule", ["seed", "seeds"], ["It can germinate.",
                                                                                                                      "Inside a fruit."]),
    term("1.2.3", "A study of interactions between living organisms and their environment", ["ecology"], ["Eco- means home.", "-logy, study."]),
    term("1.2.4", "A process in which white blood cells engulf and digest harmful pathogens", ["phagocytosis"], ["Cell eating.", "Phago-…"]),
    term("1.2.5", "The movement of individuals of a population out of a habitat", ["emigration"], ["E- means out.", "Not immigration."]),
    term("1.2.6", "The collective name for a filament and an anther", ["stamen", "stamens"], ["The male part of a flower.", "Not the pistil."]),
    term("1.2.7", "A method of controlling alien invasive plant species by introducing their natural enemy into the environment",
         ["biological control", "biological"], ["A living organism does the work.", "Bio-…"]),
    term("1.2.8", "The average number of years a person is expected to live", ["life expectancy"], ["Life …", "Higher in developed countries."])]
q13 = [
    abq("1.3.1", "An organism that transmits pathogens from one host to another", "Vector", "Anopheles female mosquito", 2,
        ["A vector carries pathogens.", "The mosquito carries malaria."]),
    abq("1.3.2", "Division of resources by different species which reduces competition and enables coexistence", "Resource partitioning",
        "Competitive exclusion", 0, ["Sharing resources.", "Exclusion means one species wins."]),
    abq("1.3.3", "An avascular plant", "Bryophyte", "Gymnosperm", 0, ["Avascular: no xylem or phloem.", "Mosses."])]
LET6 = ["A", "B", "C", "D", "E", "F"]
q14 = [
    term("1.4.1", "Identify the micro-organism in diagram 1.", ["bacteria", "bacterium", "E. coli", "E.coli"], ["Rod-shaped with a tail.",
                                                                                                                "A prokaryote."]),
    term("1.4.2(a)", "Label part C", ["flagellum", "tail", "flagella"], ["It moves the cell.", "A long whip."]),
    term("1.4.2(b)", "Label part D", ["protein spikes", "spikes", "protein spike", "glycoprotein spikes"], ["On the virus's outside.",
                                                                                                          "They attach to host cells."]),
    mcq("1.4.3(a)", "Which diagram (1 or 2) represents a pathogenic micro-organism that causes HIV/Aids infection?", ["Diagram 1", "Diagram 2"],
        1, ["HIV is a virus.", "Which diagram is a virus?"], marks=1),
    mcq("1.4.3(b)", "Which diagram (1 or 2) represents a pathogenic micro-organism that develops resistance to antibiotics?",
        ["Diagram 1", "Diagram 2"], 0, ["Antibiotics act on bacteria.", "Which diagram is a bacterium?"], marks=1),
    {"t": "pickn", "n": "1.4.4", "marks": 2, "q": "Write only the TWO LETTERS of the organelles that contain genetic material in both diagrams.",
     "clues": ["One letter in each diagram.", "The coiled material inside each."], "opts": LET6, "pool": [0, 4], "count": 2},
    term("1.4.5(a)", "Give the name of the circular structure used in insulin production by organisms in diagram 1", ["plasmid", "plasmids"],
         ["A small ring of DNA.", "It carries the insulin gene."]),
    term("1.4.5(b)", "Give the name of the type of micro-organism as in diagram 2 that attacks organisms in diagram 1", ["bacteriophage",
                                                                                                                        "bacteriophages",
                                                                                                                        "phage"],
         ["A virus that infects bacteria.", "Bacterio-…"])]
q15 = [
    term("1.5.1", "Identify the type of energy emitted by the sun in this greenhouse effect.", ["radiant", "radiant energy", "solar energy",
                                                                                               "light energy"], ["It travels as rays.",
                                                                                                                 "Radiant …"]),
    term("1.5.2", "State what happens to the type of energy identified in QUESTION 1.5.1 at point A.", ["reflected", "reflected into space",
                                                                                                      "bounces back into space",
                                                                                                      "it is reflected back into space"],
         ["The arrow turns back at A.", "Back into space."]),
    stmt("1.5.3", "Give TWO greenhouse gases that enhance the greenhouse effect in the atmosphere.", 2,
         ["Carbon dioxide (CO₂)", "Methane (CH₄)", "Nitrous oxide (N₂O)"], ["Oxygen (O₂)", "Nitrogen (N₂)", "Argon (Ar)"],
         ["They trap heat.", "Burning fuel and farming release them."], 1),
    term("1.5.4(a)", "Name the phenomenon that exists when the average global temperatures increase on Earth", ["global warming"],
         ["Global …", "The world heats up."]),
    term("1.5.4(b)", "Name the phenomenon that exists when humans cut-down trees for their own benefit", ["deforestation"],
         ["Forests are removed.", "De-…"]),
    term("1.5.4(c)", "Name the phenomenon that exists when there is a change in weather patterns over a long time", ["climate change"],
         ["Long-term weather.", "Climate …"]),
    term("1.5.4(d)", "Name the phenomenon that exists when the total amount of greenhouse gases emitted directly or indirectly by an individual "
         "per year", ["carbon footprint"], ["Carbon …", "A footprint you leave."]),
    term("1.5.5", "Name the human activity that enhances the greenhouse effect in the production of electricity.",
         ["burning of fossil fuels", "burning fossil fuels", "burning coal", "burning of coal", "fossil fuels"],
         ["Power stations in South Africa.", "Coal, oil, gas."])]

# ---- SECTION B, QUESTION 2, the question paper pages 9-13 and the memo pages 6-8 ----
q21 = [
    term("2.1.1", "Name the plant division represented by the plant in the diagram above.", ["angiosperms", "angiosperm", "flowering plants",
                                                                                            "angiospermae"], ["It has flowers.", "Angio-…"]),
    stmt("2.1.2", "State TWO unique characteristics of the plant division named in QUESTION 2.1.1.", 2,
         ["They produce flowers.", "Their seeds are enclosed in a fruit."],
         ["They reproduce by spores.", "They have no vascular tissue.", "Their seeds are naked on cones."],
         ["What do only angiosperms have?", "Flowers and fruit."], 1),
    term("2.1.3(a)", "Identify the labelled part which produces a male gamete", ["pollen", "pollen grain", "pollen grains"],
         ["It is carried by the bird.", "Male."]),
    term("2.1.3(b)", "Identify the labelled part which is located on top of the pistil", ["stigma"], ["It catches pollen.", "The tip."]),
    term("2.1.3(c)", "Identify the labelled part which attracts the hummingbird to this plant", ["nectar"], ["A sweet liquid.", "Food for the "
                                                                                                                             "bird."]),
    stmt("2.1.4", "Explain the significance for reproduction, of having both male and female reproductive parts being close to each other in "
         "this plant.", 3,
         ["It allows self-pollination to occur.", "Pollen lands on the stigma easily.", "So fertilisation can take place."],
         ["It prevents pollination.", "Pollen cannot reach the stigma.", "It stops fertilisation."],
         ["Male and female close together.", "Pollen to stigma, then fertilisation."], 1),
    term("2.1.5", "Name another pollinating agent that is attracted by a strong scent produced by other plants.", ["insects", "insect", "bees",
                                                                                                                   "bee", "moths", "moth"],
         ["Small animals that smell flowers.", "Not birds."]),
    stmt("2.1.6", "Discuss TWO important roles the process of pollination plays for plant survival in ecosystems.", 4,
         ["It transfers pollen from the male to the female parts, allowing plants to reproduce.",
          "Cross pollination creates genetic variation, producing offspring that can withstand changes in the environment."],
         ["It stops plants from producing seeds.", "It makes all offspring identical.", "It removes nectar from the plant."],
         ["Reproduction and variation.", "Each card gives a role and why it matters."], 2)]
q22 = [
    term("2.2.1(a)", "Identify the type of stem at X", ["rhizome"], ["It grows horizontally.", "Underground."]),
    term("2.2.1(b)", "Identify the type of leaf at Y", ["fronds", "frond"], ["Fern leaves.", "F-…"]),
    term("2.2.2", "Name the cluster of sporangia that are usually found on the underside of the leaf at Y.", ["sori", "sorus"],
         ["Brown dots under the frond.", "S-…"]),
    sort("2.2.3", "Tabulate ONE difference between the plant sizes of pteridophytes in comparison to bryophytes.",
         ["Pteridophytes", "Bryophytes"], [("Bigger (larger) plants", 0), ("Smaller plants", 1), ("Grow only a few centimetres tall", 1)],
         ["Ferns have vascular tissue to grow tall.", "Mosses stay small."]),
    stmt("2.2.4", "Name TWO vascular tissues that are found in the roots of this fern plant.", 2, ["Xylem", "Phloem"],
         ["Epidermis", "Cambium of a tree trunk", "Mesophyll"], ["One carries water, one food.", "Vascular tissues."], 1)]
ORG = ["Ancestor", "Lancelets", "Tunicates", "Jawless fishes", "Cartilaginous fishes", "Bony fishes", "Amphibians", "Reptiles"]
q23 = [
    term("2.3.1(a)", "Identify the phylum represented by the diagram above", ["Chordata", "chordates"], ["All have a notochord.", "Chord-…"]),
    {"t": "pickn", "n": "2.3.1(b)", "marks": 2, "q": "Identify TWO organisms in the diagram above that lack a backbone",
     "clues": ["The vertebrae appear after them in the tree.", "Below the 'Vertebrae' branch."], "opts": ORG, "pool": [0, 1, 2], "count": 2},
    stmt("2.3.2", "Some organisms that belong to the animal group identified in QUESTION 2.3.1(b) are also found on land. Explain the role played "
         "by those organisms in agriculture.", 3,
         ["Decomposition of dead organisms leads to the formation of humus,", "which improves the soil texture and fertility.",
          "Burrowing into the soil leads to better aeration,", "which increases the oxygen supply to the root cells,",
          "promoting better root growth."],
         ["They eat the crops' roots, increasing harvests.", "They compact the soil, keeping water out.", "They pollinate underground roots."],
         ["Invertebrates in the soil: worms and insects.", "Decomposing and burrowing."], 1),
    term("2.3.3(a)", "Name the characteristic shared by mammals, birds and reptiles", ["amnion", "presence of an amnion", "amniotic egg"],
         ["Read the branch below reptiles.", "A membrane round the embryo."]),
    term("2.3.3(b)", "Name the group of organisms with the most advanced evolutionary features", ["mammals", "mammalia"], ["At the top of the "
                                                                                                                       "tree.", "Hair."])]
q24 = [
    term("2.4.1(a)", "Identify the type of blood circulatory system 1", ["open", "open blood system", "open circulatory system",
                                                                         "open system"], ["Blood flows in sinuses.", "Not in vessels."]),
    term("2.4.1(b)", "Identify the type of blood vessel P", ["capillaries", "capillary"], ["The smallest vessels.", "Where exchange happens."]),
    stmt("2.4.2", "Name TWO useful substances that are transported in blood vessel P of organism B that assist in its survival.", 2,
         ["Nutrients", "Oxygen"], ["Carbon dioxide", "Urea", "Lactic acid"], ["Useful, not waste.", "Food and a gas."], 1),
    stmt("2.4.3", "Describe the type of body symmetry associated with organism A.", 2,
         ["Organism A has bilateral symmetry.", "It can be cut through the centre once", "to produce two equal halves."],
         ["Organism A has radial symmetry.", "It can be cut in many planes.", "It has no symmetry at all."],
         ["A grasshopper.", "Left and right sides."], 1),
    term("2.4.4(a)", "Name the fluid filled body cavity that acts as a hydrostatic skeleton in organism B", ["coelom"],
         ["Earthworms have one.", "In the mesoderm."]),
    term("2.4.4(b)", "Name the fluid filled body cavity that plays a role in nutrient distribution and waste removal in organism A",
         ["haemocoel", "hemocoel", "haemocoele"], ["Blood fills it.", "Haemo- means blood."]),
    stmt("2.4.5", "Give TWO benefits of having segmented body plans displayed by organism A and B.", 2,
         ["Body parts can be specialised to perform different functions.", "Sections of the body can move independently.",
          "It allows for growth."], ["It makes the body heavier.", "It stops the body from moving.", "All segments must do the same job."],
         ["Each segment can do its own job.", "Movement."], 1)]
q25 = [
    term("2.5.1", "State what happens to antibody levels after Covid-19 vaccine is initially administered on day 0 to 40.", ["increase",
                                                                                                                          "increases",
                                                                                                                          "they increase",
                                                                                                                          "it increases"],
         ["Follow each line from day 0 to day 40.", "Up or down?"]),
    num("2.5.2(a)", "Give the antibody level two months after the second Covid-19 vaccine dose was administered (arbitrary units)", 90, 5, "",
        ["Two months is day 60.", "Read the second-dose line."]),
    term("2.5.2(b)", "Give the type of immunity the Covid-19 vaccine offers to patients", ["artificial", "acquired", "artificial immunity",
                                                                                          "acquired immunity"], ["It comes from a vaccine.",
                                                                                                                 "Not natural."]),
    term("2.5.2(c)", "Give the cells in the immune system that produce antibodies", ["white blood cells", "lymphocytes", "white blood cell",
                                                                                     "lymphocyte", "B-lymphocytes", "B lymphocytes"],
         ["Not red blood cells.", "Lympho-…"]),
    stmt("2.5.3", "Give ONE reason why 6 245 participants were used instead of 60 participants in this study.", 2,
         ["To increase", "the reliability of the results."], ["To decrease", "the cost of the vaccine.", "the validity of the dose."],
         ["More people, more trust in the results.", "Reliability."], 1),
    term("2.5.4", "Give the main active component of a vaccine.", ["weakened pathogen", "dead pathogen", "weakened or dead pathogen",
                                                                   "antigen", "antigens", "weakened virus", "dead virus", "suspension of the "
                                                                                                                         "pathogen"],
         ["A harmless form of the germ.", "It carries the antigen."]),
    stmt("2.5.5", "Based on the information on the graphs over the 120-day period, explain why it is necessary for people to take the third dose "
         "of the Covid-19 vaccine dose.", 3,
         ["Antibody levels are higher for the third dose,", "indicating a stronger immune response,", "which prevents Covid-19 infection."],
         ["Antibody levels are lowest for the third dose.", "The third dose weakens the immune response.", "The third dose causes Covid-19."],
         ["Compare the three lines.", "Higher antibodies mean …"], 1)]

# ---- QUESTION 3, the question paper pages 14-17 and the memo pages 9-11 ----
JP = {"head": ["PERIOD (Years)", "POPULATION DECREASE"],
      "rows": [["2016-2017", "363 000"], ["2017-2018", "405 000"], ["2018-2019", "497 000"], ["2019-2020", "505 000"],
               ["2020-2021", "610 000"], ["2021-2022", "780 000"], ["2022-2023", "837 000"], ["2023-2024", "890 000"]]}
q31 = [
    stmt("3.1.1", "Define the term population.", 3,
         ["Organisms of the same species", "occupying the same habitat", "at the same time (able to interbreed)."],
         ["Organisms of different species", "living in different habitats.", "All the living things in an ecosystem."],
         ["One species.", "One place, one time."], 1),
    answer("3.1.2", "Describe the general trend that can be observed in the population size of Japan over this period.", 2,
           ["As the years increase, the population size decreases", "As the years increase, the population size increases",
            "The population size stays the same", "The population size rises, then falls"],
           ["The table gives decreases.", "Each year more people are lost."]),
    work("3.1.3", "Calculate the percentage increase in the number of people by which Japan's population decreased from 2019‒2020 and 2020‒2021. "
         "Show ALL working.", 3, [
        "% increase = {610 000 − 505 000}/{505 000} × 100\n= 20,79%",     # the memo
        "% increase = {610 000 − 505 000}/{610 000} × 100\n= 17,21%",     # divided by the new value
        "% increase = {610 000}/{505 000} × 100\n= 120,79%",              # the old value not subtracted
        "% increase = {610 000 − 505 000}/{505 000}\n= 0,21%"],           # not × 100
        ["2019-2020: 505 000; 2020-2021: 610 000.", "Increase ÷ the earlier value × 100."]),
    stmt("3.1.4", "Explain TWO ways in which a negative population growth could negatively harm a country.", 4,
         ["The economy (GDP) decreases, with fewer taxes, due to a smaller labour force.",
          "Skills and innovation are reduced, due to fewer young people.",
          "Health facilities are under pressure from an aging population that needs medical care.",
          "Social programmes are strained, with fewer workers to pay for them."],
         ["More workers lead to a growing economy.", "Fewer old people need health care."], ["Fewer workers, more old people.",
                                                                                            "Each card gives an effect and its cause."], 2),
    term("3.1.5", "Name ONE factor that might increase the population size of Japan.", ["immigration", "high birth rate", "births",
                                                                                       "increased birth rate", "higher birth rate"],
         ["People arriving or being born.", "Births or arrivals."])]
q32 = [
    stmt("3.2.1", "Give TWO cloud seeding agents that are NOT dispersed by this aircraft.", 2, ["Dry ice", "Sodium chloride"],
         ["Silver iodide", "Potassium iodide", "Water vapour"], ["The aircraft disperses iodide agents.", "Which named agents are left?"], 1),
    term("3.2.2", "Name ONE human-made reservoir that will store water from the rainfall caused by cloud seeding.", ["dam", "dams"],
         ["Built across a river.", "Human-made."]),
    stmt("3.2.3", "Explain ONE benefit on agriculture that cloud seeding has in regions affected by drought.", 2,
         ["Water availability will increase,", "giving a constant supply of water for irrigation."],
         ["Less water will be available.", "Crops will need no water.", "Soil erosion stops completely."], ["More rain.", "Farms need water."],
         1),
    stmt("3.2.4", "Suggest THREE other strategies of increasing water availability in drought affected regions.", 3,
         ["Desalinate seawater.", "Fix and maintain waterworks and pipes.", "Locate aquifers and drill boreholes.",
          "Remove alien plants from dam catchment areas.", "Recycle grey water."],
         ["Plant more alien trees near rivers.", "Leave leaking pipes."], ["New sources, and save what there is.", "Sea, ground, recycling."],
         1)]
q33 = [
    term("3.3.1(a)", "Identify the independent variable", ["concentration of microplastics", "microplastic concentration", "concentration "
                                                                                                                           "of microplastic",
                                                           "microplastics"], ["What did the scientists change?", "Groups A to D."]),
    term("3.3.1(b)", "Identify the dependent variable", ["rate of photosynthesis", "photosynthetic rate", "the rate of photosynthesis"],
         ["What was measured?", "Read the results table."]),
    stmt("3.3.2", "State THREE ways in which the variable identified in QUESTION 3.3.1(b) was measured.", 3,
         ["Dissolved oxygen production", "Carbon dioxide uptake", "Chlorophyll fluorescence"],
         ["Number of beakers", "Mass of microplastics", "Water temperature"], ["Read the investigation.", "Oxygen, CO₂ and a glow."], 1),
    stmt("3.3.3(a)", "Explain the purpose of including group A in this investigation.", 2,
         ["It served as a control,", "to compare whether microplastics had any effect on the rate of photosynthesis."],
         ["It had the most microplastics.", "To increase the rate of photosynthesis.", "To measure the temperature."],
         ["Group A has 0 ppm.", "Something to compare with."], 1),
    stmt("3.3.3(b)", "Explain the purpose of placing the beakers under the same light and temperature condition during this investigation.", 2,
         ["To keep other factors affecting photosynthesis constant,", "to ensure the validity of the investigation."],
         ["To change the rate of photosynthesis.", "To make the algae grow faster.", "To use less light."],
         ["Only one variable should change.", "Fair test."], 1),
    draw("3.3.4", "Draw a bar graph to represent the rate of photosynthesis in the groups with microplastics.", 6,
         [["Type of graph: a bar graph", 1], ["Caption with both variables", 1], ["Axes labelled, with units", 1],
          ["Equal bars and a correct scale", 1], ["All three groups plotted correctly", 2]],
         ["Groups B, C and D have microplastics.", "Caption, labels, equal bars."],
         memo="The memo's graph: bars B 85%, C 67% and D 53%, captioned, the y-axis 0 – 90%."),
    stmt("3.3.5", "Use the information in the table to explain how microplastics could negatively affect food security.", 2,
         ["Food security will decrease,", "due to a decrease in the rate of photosynthesis."],
         ["Food security will increase.", "Microplastics speed up photosynthesis.", "Algae are not part of food chains."],
         ["Algae are producers.", "Less photosynthesis, less food."], 1)]
q34 = [
    stmt("3.4.1", "Name and describe the symbiotic relationship that exists between the sea anemone and the clownfish.", 2,
         ["Mutualism", "Both organisms benefit from the relationship."],
         ["Parasitism", "One organism is harmed.", "Neither organism benefits."], ["Shelter for one, cleaning for the other.", "Both gain."],
         1),
    stmt("3.4.2", "Name TWO other symbiotic relationships that occur in species within ecosystems.", 2, ["Commensalism", "Parasitism"],
         ["Mutualism", "Predation", "Competition"], ["Other than the one in 3.4.1.", "Symbiotic ones only."], 1),
    term("3.4.3(a)", "From the extract, give evidence of a poisonous secretion of the sea anemone.", ["powerful venom", "venom",
                                                                                                   "release and inject a powerful venom"],
         ["Read the first paragraph.", "What do the tentacles inject?"]),
    term("3.4.3(b)", "From the extract, give evidence of a defence strategy of the clownfish from the sea anemone tentacles.",
         ["mucus layer", "special mucus layer", "mucus layer on their skin", "a special mucus layer on their skin"],
         ["Read the second paragraph.", "What do clownfish secrete?"]),
    term("3.4.3(c)", "From the extract, give evidence of a blind gut in the sea anemone.", ["central single digestive opening",
                                                                                           "single digestive opening", "one opening"],
         ["A blind gut has one opening.", "Read the first paragraph."]),
    stmt("3.4.4", "Explain how intraspecific competition in clownfish prevents their population size from exceeding the carrying capacity in "
         "the ecosystem.", 5,
         ["An increase in the clownfish population", "makes clownfish compete amongst themselves", "for limited resources (sea anemones, "
                                                                                                     "shelter).",
          "Less breeding occurs among the weaker competitors.", "Clownfish die due to predation (environmental resistance).",
          "The population growth rate decreases (logistic growth)."],
         ["More sea anemones appear when clownfish compete.", "Competition increases the breeding of weak clownfish."],
         ["Intraspecific: within one species.", "Limited anemones."], 1)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 18,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 8,
     "lead": "Give the correct biological term for EACH of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 6,
     "lead": "Indicate whether each description in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Micro-organisms", "marks": 9,
     "lead": "The diagrams below represent two pathogenic micro-organisms to humans.",
     "figure": P.fig("1.4", "Diagram 1: a rod-shaped cell with hair-like projections; A points to the coiled material inside, B to the outer "
                            "wall, C to a long tail. Diagram 2: a many-sided particle; D points to a projection on its surface, E to the "
                            "coiled material inside, F to its outer coat."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "The greenhouse effect", "marks": 9,
     "lead": "The diagram below illustrates the greenhouse effect.",
     "figure": P.fig("1.5", "The Sun's rays reach the Earth through a curved layer of the atmosphere; some rays turn back at point A, others "
                            "are trapped and bounce between the Earth and the layer."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Plant reproduction", "marks": 14,
     "lead": "The diagram below shows a hummingbird pollinating a plant.",
     "figure": P.fig("2.1", "A hummingbird feeding at a lily-like flower, the parts labelled Nectar, Pollen and Stigma."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Plant diversity", "marks": 8, "lead": "The diagram below shows a pteridophyte (fern) plant.",
     "figure": P.fig("2.2", "A fern: X points to the horizontal stem at the base, Y to a large divided leaf, and the roots below."),
     "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Animal diversity", "marks": 8,
     "lead": "The phylogenetic tree below shows different organisms that belong to the most evolved phylum in the animal kingdom.",
     "figure": P.fig("2.3", "A phylogenetic tree from the Ancestor: Lancelets, then Tunicates, then the Vertebrae branch to Jawless fishes, Jaws to "
                            "Cartilaginous fishes, Lungs to Bony fishes, Limbs to Amphibians, Amnion to Reptiles, Feathers to Birds, and "
                            "Mammary glands, hair to Mammals."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Body plans", "marks": 10,
     "lead": "The diagrams below represent two circulatory systems that exist in different animals.",
     "figure": P.fig("2.4", "Circulatory system 1, in organism A (a grasshopper): a heart with fluid in sinuses around organs. Circulatory system "
                            "2, in organism B (an earthworm): a heart joined to vessels, P the fine vessels between them."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Immunity", "marks": 10,
     "lead": "The graphs below show the antibody response after Covid-19 vaccine doses in 6 245 participants in the United States of America "
             "(USA).",
     "figure": P.fig("2.5", "A line graph, ANTIBODY RESPONSE AFTER COVID-19 VACCINE DOSES: antibody level (arbitrary units) against days since "
                            "vaccination (0 to 120), one line for each of the first, second and third doses; each rises to a peak at day 40 "
                            "and then falls, the third dose highest and the first lowest."), "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Human population", "marks": 13, "table": JP,
     "lead": "An aging population together with low-fertility rates has seen the population of Japan decline rapidly in recent years. Japan had "
             "a population size of 126,9 million people in 2016.\nThe table below shows the annual population decrease rate from 2016 to 2024 "
             "in Japan. The population decrease rate is calculated by subtracting the number of deaths from the number of births.",
     "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Water availability", "marks": 8,
     "lead": "Cloud seeding is a weather modification technique that introduces seeding agents (substances) such as silver/potassium iodide, "
             "dry ice as well as sodium chloride into the clouds. These seeding agents are usually transported by aircrafts into small clouds "
             "to allow them to condense and enlarge. This eventually increases rainfall in drought-affected regions.\nThe diagram below shows a "
             "schematic representation of how cloud seeding is performed.",
     "figure": P.fig("3.2", "An aircraft flies through clouds: 'iodide cloud seeding agents dispersed by aircraft into clouds'; rain falls on "
                            "a farmhouse."), "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Investigation", "marks": 17,
     "table": {"head": ["GROUP", "A", "B", "C", "D"], "rows": [["Concentration of microplastics (ppm)", "0", "10", "50", "100"],
                                                              ["Rate of photosynthesis (%)", "100%", "85%", "67%", "53%"]]},
     "lead": "Scientists carried out an investigation to determine how different concentrations of microplastics affect the rate of "
             "photosynthesis in aquatic organisms such as algae. They:\n• Identified and cultured a freshwater algae (Chlorella vulgaris) in a "
             "lab.\n• Prepared multiple beakers with growth medium and equal amounts of freshwater algae in each beaker. The beakers were "
             "divided into FOUR groups A to D.\n• Added a microplastic (polyethylene microspheres) in the beakers with increasing "
             "concentrations of microplastic.\nScientists further:\n• Placed the samples/beakers under the same light and temperature "
             "conditions.\n• Measured the rate of photosynthesis in the algae over a few days by using dissolved oxygen production, carbon "
             "dioxide uptake and chlorophyll fluorescence (red glow of excess energy given off by chlorophyll which is not used in "
             "photosynthesis).\nThe results of this investigation are tabulated below.", "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Symbiosis", "marks": 12,
     "lead": "THE CLOWNFISH AND THE SEA ANEMONE SYMBIOTIC RELATIONSHIP\nThe sea anemone has stinging tentacles made of nematocysts cells that it "
             "uses to catch prey. These tentacles release and inject a powerful venom into prey, which paralyses and kills the animal when in "
             "contact. This enables the sea anemone to use these tentacles to move food into its central single digestive opening.\nThe "
             "clownfish has found shelter in the sea anemone that allows it to escape predators by living and breeding within the sea anemone "
             "tentacles. The clownfish secrete a special mucus layer on their skin that protect them from the stinging tentacles of the sea "
             "anemone. The clownfish feeds on the leftovers from the sea anemone meals, helping to clean the tentacles. A limited number of sea "
             "anemones often leads to the death of many clownfish.", "items": q34},
]
P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P2", "sitting": "November 2025", "total_marks": 150, "time": "2½ hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.2.3", "kind": "no_fit", "detail": "A tabulated difference plays as a sort into the two divisions' columns, one mark a row; "
                                                     "the memo's compulsory table mark is the sort's own layout."},
          {"n": "2.3.1(b)", "kind": "no_fit", "detail": "Two organisms read off the tree: its organisms as cards, any two of the memo's "
                                                        "Lancelets, Tunicates and Ancestor."},
          {"n": "3.3.4", "kind": "no_fit", "detail": "The bar graph to draw plays as pick the drawing."}],
         {"1": 50, "2": 50, "3": 50}, 150, {}, "Questions 1 to 3 (the whole paper)")
