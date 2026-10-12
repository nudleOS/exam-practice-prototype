"""Grade 11 Life Sciences P2 November 2024 (Eastern Cape Department of Education), the whole paper (Questions 1 to 3, 150 marks,
2½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and answers are
the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za,
2024_November_Gr_11_Exams, the question paper zip (English PDF, 15 pages, text layer) and the memo zip (English, 10 pages).

  python tools/ingest/transcribe_g11_ls_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ls-p2-2024-11-ec/LIFE SCIENCES P2 GR11 QP NOV2024 ENG D_watermark.pdf" "uploads/provincial/g11-ls-p2-2024-11-ec/LIFE SCIENCES P2 GR11 MEMO NOV2024_English_watermark.pdf" --id g11-ls-p2-2024-11-ec --from-json

The Life Sciences rulings, as in transcribe_g11_ls_p1_2024_11_ec.py: printed multiple choice as printed; terms typed; Column I /
Column II; LETTER and NAME; written answers as statements (one mark a tick); the one calculation (3.1.4) as four workings; the two
drawings (2.1.4 a bacterium, 3.2.5 a pie chart) as pick the drawing (pictures_lower.py: bacterium, pie). Figure boxes are in PDF
points (text blocks and image rects), 1% inside their neighbours."""
from provincial import Paper

P = Paper("g11-ls-p2-2024-11-ec", 595.22, 842.0, {
    "1.1.3": [3, 143.0, 442.0, 496.0, 628.0], "1.1.9": [5, 175.0, 232.0, 500.0, 348.0], "1.4": [6, 150.0, 300.0, 470.0, 480.0],
    "1.5": [7, 86.0, 108.0, 510.0, 399.0], "2.1": [8, 83.0, 199.0, 492.0, 455.0], "2.2": [9, 94.0, 441.0, 483.0, 641.0],
    "2.3": [10, 85.0, 227.0, 506.0, 497.0], "2.4": [11, 86.0, 104.0, 450.0, 266.0], "2.4.3": [11, 126.0, 348.0, 505.0, 575.0],
    "3.1": [12, 83.0, 124.0, 513.0, 421.0], "3.5": [15, 85.0, 158.0, 508.0, 346.0]}, start=4)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term
AB = ["A only", "B only", "Both A and B", "None"]
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
ln = lambda n, q, letters, letter, names, clues, **kw: {"t": "lettername", "n": n, "marks": 2, "q": q, "clues": clues, "letters": letters,
                                                       "a": {"letter": letter, "name": names}, **kw}

# ---- SECTION A, QUESTION 1, the question paper pages 3-7 and the memo page 4 ----
q11 = [
    mcq("1.1.1", "A root system mainly found in monocots formed by many thin, moderately branching roots from the stem.",
        ["Vascular roots", "Aerial roots", "Adventitious roots", "Taproots"], 2, ["Monocots have no main root.", "Roots that grow from the stem."]),
    mcq("1.1.2", "A biological preparation made from damaged micro-organisms particles used to stimulate an immune response by the body's immune "
        "system.", ["Antibiotic", "Vaccine", "Antigen", "Virus"], 1, ["It is given before you get sick.", "It trains the immune system."]),
    mcq("1.1.3", "The diagram below shows a bread mould. The correct labels for the diagram above are:",
        ["X-spores, Y-sporangiophore, Z-sporangium", "X-sporangium, Y-spores, Z-sporangiophore", "Z-sporangiophore, Y-sporangium, X-spores",
         "Y-sporangium, X-sporangiophore, Z-spores"], 2, ["The spores are the tiny dots released.", "The sporangium is the round head on "
                                                                                                   "its stalk."],
        figure=P.fig("1.1.3", "A bread mould: threads across the bread with upright stalks, each with a round head; X points to tiny dots "
                              "leaving a head, Y to a round head, Z to a stalk.")),
    mcq("1.1.4", "A technique used to determine the elephant population from an aerial photograph:", ["Quadrat sampling", "Direct counting",
                                                                                                    "Mark-recapture", "Culling"], 1,
        ["Elephants are big and easy to see from the air.", "Every animal in the photograph is counted."]),
    mcq("1.1.5", "The table shows the water dam levels in the Nelson Mandela Bay municipality during certain months of 2024 (dam: capacity when "
        "full; current level; available water): Churchill 32 249 mℓ, 100%, 32 597 mℓ; Impofu 105 757 mℓ, 42.62%, 27 642 mℓ; Loerie 3 026 mℓ, "
        "98.65%, 2 410 mℓ; Kouga 125 910 mℓ, 100%, 121 755 mℓ; Groendal 11 638 mℓ, 100%, 11 149 mℓ. Which dam has the least available water?",
        ["Impofu", "Groendal", "Kouga", "Loerie"], 3, ["Read the available water column, not the percentage.", "Which is the smallest number?"]),
    mcq("1.1.6", "A narrow shaft drilled in the ground to extract water.", ["Aquifer", "Borehole", "Wetland", "Purification"], 1,
        ["It is drilled.", "An aquifer is the rock that holds the water."]),
    mcq("1.1.7", "Study the list: (i) Stops using medication after feeling better, (ii) Uses incorrect treatment, (iii) The pathogen undergoes "
        "mutations, (iv) Uses correct treatment on regular basis, (v) Gets infected with another disease. Which of the following combinations "
        "causes humans to develop resistance to a disease?", ["(i) and (v)", "(ii), (iv) and (v)", "(iii) and (iv)", "(i) and (iii)"], 3,
        ["Stopping treatment early leaves some pathogens alive.", "A changed pathogen is no longer killed by the drug."]),
    mcq("1.1.8", "The net increase in a population can be determined by …",
        ["adding deaths and immigrations and subtracting births and emigrations.", "adding births and immigrations and subtracting deaths "
                                                                                    "and emigrations.",
         "adding births and emigrations and subtracting deaths and immigrations.", "adding births and deaths and subtracting emigrations and "
                                                                                   "immigrations."], 1,
        ["What adds individuals to a population?", "Births and arrivals add; deaths and departures take away."]),
    mcq("1.1.9", "The following diagram shows a seed. Which labelled part develops into the stem and leaves?", ["1", "2", "3", "4"], 0,
        ["The embryo has a young shoot and a young root.", "The young shoot is the plumule."],
        figure=P.fig("1.1.9", "A seed cut open: 1 points to the small leafy part of the embryo, 2 to the embryo's stalk, 3 to the seed coat, "
                              "4 to the large stored-food part."))]
q12 = [
    term("1.2.1", "Organisms of the same species that live together in the same environment and can interbreed", ["population"],
         ["Not a community: one species.", "They can breed together."]),
    term("1.2.2", "A plant body that is not differentiated into stems and leaves and which lacks true roots", ["thallus"],
         ["Found in algae and liverworts.", "A flat plant body."]),
    term("1.2.3", "Plant and animal species that remain stable in their environment", ["climax species", "climax community"],
         ["The last stage of succession.", "Climax …"]),
    term("1.2.4", "Organic component of soil, formed by the decomposition of leaves and other plant material by micro-organisms", ["humus"],
         ["Dark, rich soil matter.", "Decomposed plant material."]),
    term("1.2.5", "A stem which grows horizontally", ["rhizome", "rhizomes"], ["Usually underground.", "Ginger is one."]),
    term("1.2.6", "Factors that will exert an influence on a population regardless of its size", ["density-independent factors",
                                                                                                    "density-independent factor",
                                                                                                    "density independent factors"],
         ["Floods and fire affect a population of any size.", "Density-…"]),
    term("1.2.7", "A process of initial colonisation of land in a previously disturbed area", ["primary succession"],
         ["Pioneer species arrive first.", "On bare land: primary or secondary?"]),
    term("1.2.8", "Growing of a single species of plant crops in large areas for many consecutive years", ["monoculture"],
         ["Mono- means one.", "One crop."]),
    term("1.2.9", "Electricity generated by the power of water", ["hydroelectricity", "hydro-electricity", "hydroelectric power",
                                                                  "hydro-electric power"], ["Hydro- means water.", "Dams generate it."])]
q13 = [
    abq("1.3.1", "Develop a notochord", "Arthropoda", "Chordata", 1, ["The name gives it away.", "Insects have no notochord."]),
    abq("1.3.2", "Hemocoel", "Open blood system", "Closed blood system", 0, ["A hemocoel is a body cavity filled with blood.",
                                                                            "Blood that is not kept in vessels."]),
    abq("1.3.3", "Autotrophic", "Green algae", "Amoeba", 0, ["Autotrophs make their own food.", "Which has chlorophyll?"])]
LET4 = ["A", "B", "C", "D"]
q14 = [
    term("1.4.1", "Identify the kingdom represented by the phylogenetic diagram above.", ["Plantae", "plant kingdom", "plants"],
         ["Seeds and vascular tissue.", "Which kingdom has these?"]),
    ln("1.4.2(a)", "Write down the LETTER and NAME of the division that has a dominant gametophyte generation", LET4, "A",
       ["bryophytes", "bryophyta", "mosses"], ["It has no vascular tissue.", "Mosses."]),
    ln("1.4.2(b)", "Write down the LETTER and NAME of the division that has fronds as leaves", LET4, "B", ["pteridophytes", "pteridophyta",
                                                                                                         "ferns"],
       ["It has vascular tissue but no seeds.", "Ferns."]),
    term("1.4.3", "State the evolutionary adaptation at X in division D that allowed it to be successful.", ["fruits", "flowers", "fruit",
                                                                                                             "flower"],
         ["Division D is the angiosperms.", "Gymnosperms lack these."]),
    term("1.4.4", "Name the vascular tissue that transports manufactured foods.", ["phloem"], ["Not xylem: that carries water.", "Food "
                                                                                                                              "moves in …"]),
    term("1.4.5", "Which kingdom has sessile organisms that differ to the one above in their mode of nutrition?", ["fungi", "fungus"],
         ["They do not move, like plants.", "They cannot photosynthesise."])]
YEARS = [str(y) for y in range(1845, 1900, 5)]
q15 = [
    term("1.5.1(a)", "Name the prey species", ["hare", "hares"], ["The prey is eaten.", "Which animal does a lynx eat?"]),
    term("1.5.1(b)", "Name the predator species", ["lynx"], ["The predator hunts.", "A wild cat."]),
    num("1.5.2", "What is the carrying capacity of the hare population in the above predator-prey graph? (The axis is in thousands: type "
        "the whole number.)", 92000, 1000, "",
        ["Read the dashed line.", "It is just above 90."]),
    {"t": "pickn", "n": "1.5.3", "marks": 2, "q": "In which years is the population size of the hare twice as much as the lynx population?",
     "clues": ["Compare the two lines year by year.", "Look for hare = 2 × lynx."], "opts": YEARS, "pool": [3, 9], "count": 2},
    term("1.5.4(a)", "Identify the phase marked B", ["exponential", "exponential phase", "geometric", "geometric phase",
                                                     "exponential growth phase"], ["The population rises fast.", "Rapid growth."]),
    term("1.5.4(b)", "Identify the phase marked D", ["death", "death phase", "extinction", "extinction phase"], ["The population falls fast.",
                                                                                                              "The opposite of growth."]),
    stmt("1.5.5", "State TWO other density-dependent factors that may have a negative effect on a population.", 2, ["Disease", "Competition"],
         ["Floods", "Fire", "Drought"], ["Density-dependent factors grow stronger in a crowded population.", "Weather is density-independent."],
         1)]

# ---- SECTION B, QUESTION 2, the question paper pages 8-11 and the memo pages 5-7 ----
q21 = [
    term("2.1.1(a)", "Name the biotechnological process above", ["genetic engineering", "genetic modification", "genetic manipulation"],
         ["A gene is moved from one organism to another.", "Genetic …"]),
    term("2.1.1(b)", "Name micro-organism X used in this process", ["bacteria", "bacterium"], ["It has a plasmid.", "A prokaryote."]),
    stmt("2.1.2", "Explain how micro-organism X named in QUESTION 2.1.1 (b) reproduces to make it suitable for the above process.", 2,
         ["Bacteria reproduce asexually.", "They produce identical copies of themselves."],
         ["Bacteria reproduce sexually by forming gametes.", "Each bacterium produces offspring that differ from it.",
          "Bacteria reproduce slowly, once a year."], ["Every copy must carry the insulin gene.", "Asexual or sexual?"], 1),
    stmt("2.1.3", "Describe the steps involved in producing insulin.", 4,
         ["A plasmid (circular DNA) is removed from the bacterial cell.", "The plasmid is cut using enzymes.",
          "The insulin gene is removed from a human cell.", "The gene is inserted into the plasmid.", "This forms recombinant DNA."],
         ["The insulin gene is removed from the bacterium and put into a human cell.", "The plasmid is put into the human cell's nucleus.",
          "Insulin is taken out of the plasmid with no gene added."], ["Follow the arrows in the diagram.", "Cut, insert, recombine."], 1),
    draw("2.1.4", "Draw a neatly labelled diagram of micro-organism X to show its structure.", 5,
         [["Correct diagram", 1], ["Caption", 1], ["Any three correct labels", 3]],
         ["A bacterium has no nucleus.", "Label its parts and give the drawing a caption."],
         memo="The memo's drawing: a bacterium labelled flagellum, plasmid, nucleoid, cell membrane, cell wall, cytoplasm and ribosome.")]
q22 = [
    term("2.2.1", "Identify the type of immunity the PrEP drugs offer to people.", ["artificial", "acquired", "artificial immunity",
                                                                                    "acquired immunity", "artificially acquired immunity"],
         ["It comes from a drug.", "Not natural."]),
    term("2.2.2(a)", "Identify the dependent variable", ["prevention of HIV infection", "preventing HIV infection", "incidence of developing "
                                                                                                                  "HIV infection",
                                                         "incidence of HIV infection"], ["What was measured?", "Read the graph's y-axis."]),
    term("2.2.2(b)", "Identify the independent variable", ["PrEP drugs", "PrEP drug", "type of PrEP drug", "the PrEP drug"],
         ["What did the scientists change?", "Read the graph's x-axis."]),
    answer("2.2.3", "Give ONE reason why this investigation could be considered reliable.", 1,
           ["A large sample of 5 338 women was used.", "Only women took part.", "Three different drugs were tested.", "The drugs were taken "
                                                                                                                   "for a year."],
           ["Reliability: would the results repeat?", "How many people took part?"]),
    stmt("2.2.4", "State TWO factors that were considered in the selection of women participants in this investigation.", 2,
         ["The women were HIV negative.", "The women were of a similar age group (16–25 years)."],
         ["The women all lived in the same house.", "The women were HIV positive.", "The women had all used PrEP before."],
         ["PrEP is for people without HIV.", "Read their ages."], 1),
    stmt("2.2.5", "Explain which PrEP drug would be highly recommended for sexually active people.", 3,
         ["Lenacapavir is the most effective PrEP drug.", "There was no incidence of developing HIV infection with it.",
          "So it prevents the spread of HIV infection."],
         ["Descovy is the most effective PrEP drug.", "Truvada had the lowest incidence of HIV infection.", "Lenacapavir must be taken every "
                                                                                                         "day."],
         ["Which bar is lowest?", "Zero incidence means …"], 1),
    term("2.2.6", "State ONE other HIV/Aids preventative measure sexually active people must practice during sexual intercourse.",
         ["condom", "condoms", "use a condom", "use condoms", "protection"], ["A barrier method.", "Used every time."])]
LET5 = ["A", "B", "C", "D", "E"]
q23 = [
    term("2.3.1(a)", "Identify the pollinating agent in the above process", ["bee", "bees", "insect", "insects"], ["It flies between the "
                                                                                                                 "flowers.", "Look at the "
                                                                                                                             "top."]),
    term("2.3.1(b)", "Identify the type of pollination represented", ["cross pollination", "cross-pollination", "cross"],
         ["Pollen moves from flower 1 to flower 2.", "Two different flowers."]),
    ln("2.3.2(a)", "Write down the LETTER and NAME of the structure that attracts the pollinating agent", LET5, "C", ["corolla", "petal",
                                                                                                                    "petals"],
       ["Colourful parts.", "Bees see them."]),
    ln("2.3.2(b)", "Write down the LETTER and NAME of the structure that has a protective function", LET5, "B", ["calyx", "sepal", "sepals"],
       ["Green parts below the petals.", "They protect the bud."]),
    stmt("2.3.3", "Describe the events that occur when pollen lands on part D.", 4,
         ["The pollen grain germinates, forming a pollen tube down the style.", "It fertilises an ovule inside the ovary.",
          "The fertilised ovule forms a seed.", "The ovary wall forms the fruit."],
         ["The pollen grain fertilises the stigma.", "The ovary forms the seed.", "The ovule forms the fruit."],
         ["D is the stigma.", "Tube, fertilisation, seed, fruit."], 1),
    term("2.3.4", "Give ONE characteristic in the offspring produced by these plants, that would enable them to survive in harsh changing "
         "environments.", ["genetic variation", "variation", "genetic diversity"], ["Cross pollination mixes genes.", "Different offspring."]),
    stmt("2.3.5", "Research shows a decline in the population size of the pollinating agent above. Explain how this could affect the cost of "
         "seed-based foods.", 2,
         ["The cost of seed-based foods will increase.", "Fewer seeds are produced because there is less insect pollination."],
         ["The cost of seed-based foods will decrease.", "More seeds are produced by self-pollination.", "Bees eat the seeds."],
         ["Fewer bees, fewer pollinated flowers.", "Less supply, higher price."], 1)]
q24 = [
    num("2.4.1", "How many tissue layers does an octopus have?", 3, 0, "", ["Triploblastic.", "Tri- means three."]),
    term("2.4.2", "Give ONE possible function of the eight limbs on the octopus body.", ["movement", "locomotion", "catching prey",
                                                                                         "to catch prey", "feeding", "swimming", "to move"],
         ["What does an octopus do with its arms?", "Moving or eating."])]
q243 = [
    term("2.4.3(a)", "Identify tissue layer Y.", ["mesoderm"], ["Between the endoderm and ectoderm.", "The middle layer."]),
    mcq("2.4.3(b)", "Which DIAGRAM (1 or 2) is found in an octopus?", ["Diagram 1", "Diagram 2"], 1, ["An octopus is triploblastic.",
                                                                                                      "Which has three layers?"], marks=1),
    stmt("2.4.4", "More evolved animal phyla developed fluid X in tissue layer Y. Name fluid X and explain TWO advantages of fluid X in more "
         "evolved phyla.", 5,
         ["Fluid X fills the coelom.", "It allows space for more complex organs to develop.", "It acts as a hydrostatic skeleton for the "
                                                                                                "movement of muscles.",
          "It separates the endoderm and ectoderm with a cavity.", "So the layers can move independently of each other."],
         ["It stores digested food permanently.", "It makes the animal diploblastic.", "It replaces the digestive cavity."],
         ["X is the body cavity in the mesoderm.", "What does a fluid-filled cavity allow?"], 1),
    term("2.4.5", "Name the animal phylum that has the symmetry in DIAGRAM 1.", ["Cnidaria", "cnidarians", "Coelenterata"],
         ["Two tissue layers, radial symmetry.", "Jellyfish."])]
q25 = [
    stmt("2.5", "Describe TWO ways invertebrates can be useful in agriculture.", 4,
         ["They act as pollinators: honeybees and butterflies pollinate flowers.", "They decompose dead organic material, e.g. termites, "
                                                                                    "beetles and worms.",
          "They enrich the soil: earthworm faeces are rich in nutrients for plants.", "They aerate the soil: their tunnels let water in "
                                                                                      "and roots grow deeper."],
         ["They eat crops, increasing harvests.", "They compete with crops for sunlight."],
         ["Bees, earthworms, termites.", "Each card gives a use and an example."], 2)]

# ---- QUESTION 3, the question paper pages 12-15 and the memo pages 8-10 ----
W314 = " × {51,2}/{100}"
q31 = [
    term("3.1.1", "What is the name of the graph shown above, used to illustrate the distribution of a population in a country?",
         ["age-gender pyramid", "age gender pyramid", "population pyramid", "age-sex pyramid"], ["Ages and sexes.", "Its shape gives "
                                                                                                                  "its name."]),
    mcq("3.1.2(a)", "In which year did China lack basic resources for its growing population?", ["1980", "2020"], 0,
        ["A wide base means many children.", "Which pyramid narrows fast?"], marks=1),
    mcq("3.1.2(b)", "In which year did China improve life expectancy of its population?", ["1980", "2020"], 1,
        ["More people in the older age groups.", "Which pyramid is wider at the top?"], marks=1),
    stmt("3.1.3", "Explain your answer to QUESTION 3.1.2 (b) by referring to the graph.", 2,
         ["There is a higher survival rate of adults in 2020 than in 1980.", "This indicates better health care services."],
         ["The 2020 pyramid has a wider base.", "Fewer people reach old age in 2020.", "There are more children in 2020 than in 1980."],
         ["Compare the top of each pyramid.", "Why do people live longer?"], 1, after=["3.1.2(b)"]),
    work("3.1.4", "Determine the total number of males in the 2020 Chinese population if the percentage of males is 51,2%. Show ALL workings.",
         2, [
        "Males = 1 424 929 781" + W314 + "\n= 729 564 048 males",            # the memo
        "Males = 1 424 929 781 × {48,8}/{100}\n= 695 365 733 males",          # the females' share
        "Males = 982 372 466" + W314 + "\n= 502 974 703 males",              # the 1980 population
        "Males = 1 424 929 781 ÷ 51,2\n= 27 830 660 males"],                 # divided
        ["The 2020 population is 1 424 929 781.", "51,2% of it."]),
    stmt("3.1.5(a)", "Explain how these policies affected the pre-reproductive age and the working-age population percentages from the year "
         "1980 to the year 2020.", 4,
         ["The percentage of the pre-reproductive ages decreased from 1980 to 2020, due to fewer births.",
          "The percentage of the working-age group increased from 1980 to 2020, due to improved economic activity."],
         ["The percentage of the pre-reproductive ages increased, due to more births.", "The working-age group decreased because more "
                                                                                         "people emigrated.",
          "The old-age group became the largest group."], ["One child per couple: what happens to the base?", "Each card gives a change "
                                                                                                               "and its cause."], 2),
    stmt("3.1.5(b)", "Give TWO other strategies governments can implement to reduce population growth in a country.", 2,
         ["Educate people about family planning (contraceptives).", "Give incentives or tax rebates to people with fewer family members.",
          "Remove or limit the child support grant."],
         ["Increase the child support grant for every child.", "Ban contraceptives.", "Reward families with many children."],
         ["Fewer births.", "Education and money."], 1)]
q32 = [
    term("3.2.1", "Name the type of plastic waste that has contributed the most to climate change.", ["landfill sites", "landfill",
                                                                                                     "landfills", "landfill site"],
         ["The biggest amount.", "Read the table."]),
    stmt("3.2.2", "Explain how communities can use the type of plastic waste in QUESTION 3.2.1 to their advantage.", 2,
         ["Waste from a landfill site can be burned to release methane.", "The methane is used to generate electricity."],
         ["Landfill plastic can be fed to livestock.", "Food crops can be grown on the plastic.", "Plastic in landfills quickly turns into "
                                                                                                  "fertiliser."],
         ["Landfills give off a gas.", "What can the gas power?"], 1),
    stmt("3.2.3", "Describe how incineration (burning of plastic) can have a negative effect on people's health.", 3,
         ["Burning plastic releases carbon dioxide and harmful gases into the atmosphere.", "The pollutants and toxins may be inhaled or get "
                                                                                            "into food and water.",
          "This leads to respiratory diseases, cancer or birth defects."],
         ["Burning plastic releases oxygen that people breathe.", "Incineration removes all toxins from the air.",
          "Burnt plastic improves the soil for food crops."], ["What goes into the air?", "Where does it end up?"], 1),
    stmt("3.2.4", "Suggest TWO possible reasons for the low percentage in recycled plastic waste.", 2,
         ["Lack of education about recycling.", "Few recycling bins.", "Lack of incentives for people who recycle.",
          "Plastic is cheap and easy to buy."],
         ["There are too many recycling bins.", "Plastic is too expensive to buy."], ["Why don't people recycle?", "Knowledge, bins, money."],
         1),
    draw("3.2.5", "Draw a pie chart to represent the amount of plastic, measured in percentage, of the different types of plastic waste in 2019.",
         7, [["Pie chart drawn", 1], ["Title showing both variables", 1], ["Correct calculations", 2], ["Key or labels", 1],
             ["Correct proportion of the segments", 2]],
         ["Each sector's angle = percentage ÷ 100 × 360°.", "Give it a title and a key."],
         memo="The memo's pie chart: landfill sites 49,3% (177,48°), incinerated 19% (68,4°), released 22,4% (80,64°), recycled 9,3% (33,48°).")]
EV = ["It invades previously disturbed land areas.", "It has poisonous berries.", "It absorbs a lot of carbon dioxide from the atmosphere.",
      "It has a rapid growth rate."]
q33 = [
    stmt("3.3.1", "What is meant by alien invasive?", 2,
         ["Plants brought into an area where they are not naturally found.", "They spread very fast and outcompete indigenous plants."],
         ["Plants that are indigenous to South Africa.", "Plants that grow slowly and die out.", "Plants that are poisonous to humans only."],
         ["Alien: from somewhere else.", "Invasive: it spreads."], 1),
    answer("3.3.2", "Why was the Brazilian peppertree introduced in South Africa?", 1, ["For ornamental and street tree purposes",
                                                                                       "To feed wildlife", "To control erosion along rivers",
                                                                                       "To absorb carbon dioxide"],
           ["Read the first paragraph.", "'Initially introduced for …'"]),
    answer("3.3.3(a)", "Give evidence from the extract that states the Brazilian peppertree is a pioneer species", 1,
           [EV[0], EV[1], EV[2], EV[3]], ["Pioneer species are the first to settle bare land.", "Where does it grow?"]),
    answer("3.3.3(b)", "Give evidence from the extract that states the Brazilian peppertree is toxic to animal life", 1,
           [EV[1], EV[0], EV[2], EV[3]], ["Toxic means poisonous.", "What do the birds eat?"]),
    answer("3.3.3(c)", "Give evidence from the extract that states the Brazilian peppertree can reduce global warming", 1,
           [EV[2], EV[0], EV[1], EV[3]], ["Which gas causes global warming?", "What does the tree take in?"]),
    stmt("3.3.4", "Explain how the rapid growth rate of the Brazilian peppertree can affect plant biodiversity.", 3,
         ["It forms a dense canopy layer over indigenous plants.", "This blocks light from reaching indigenous plants.",
          "This limits the growth of indigenous plants.", "Animals that rely on indigenous plants for food cannot reach them.",
          "Their seeds cannot be dispersed."],
         ["Its canopy lets more light reach indigenous plants.", "Indigenous plants grow faster under it.", "Birds eat more indigenous plants."],
         ["A tall, fast tree shades others.", "What do plants need from the sky?"], 1),
    stmt("3.3.5", "Describe how biological control could work in helping to reduce the population of the Brazilian peppertree.", 2,
         ["Introduce a natural enemy of the Brazilian peppertree.", "The enemy eats the Brazilian peppertree.", "This reduces its growth and "
                                                                                                                 "spread."],
         ["Spray herbicide on the trees.", "Cut the trees down by hand.", "Plant more peppertrees to compete."],
         ["Biological: a living organism does the work.", "Not chemicals or machines."], 1)]
q34 = [
    stmt("3.4", "Coastal provinces in South Africa have experienced adverse weather patterns, causing severe damage to communities. Explain the "
         "impact of global warming on the weather patterns.", 5,
         ["Higher temperatures occur.", "Heat waves occur.", "The distribution of rainfall changes.", "Some areas get more rainfall and floods.",
          "Other areas get less rainfall and drought.", "Storms are more severe and frequent."],
         ["Global warming lowers temperatures everywhere.", "Rainfall becomes the same everywhere."],
         ["Warmer air and seas.", "Floods in one place, drought in another."], 1)]
q35 = [
    term("3.5.1(a)", "Name the type of competition that occurs in DIAGRAM 1", ["intraspecific", "intraspecific competition"],
         ["The same kind of animal.", "Intra- means within."]),
    term("3.5.1(b)", "Name the type of competition that occurs in DIAGRAM 2", ["interspecific", "interspecific competition"],
         ["Different kinds of animals.", "Inter- means between."]),
    stmt("3.5.2", "Name and describe TWO symbiotic relationships that can benefit one organism in an ecosystem.", 4,
         ["Parasitism: one organism benefits while the host is harmed.", "Commensalism: one organism benefits while the other is neither "
                                                                         "harmed nor benefits."],
         ["Mutualism: one organism benefits while the other is killed.", "Predation: both organisms benefit equally.",
          "Parasitism: both organisms benefit."], ["Only ONE of the two benefits.", "Each card gives a name and its meaning."], 2)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 18,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 9,
     "lead": "Give the correct biological term for each of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column I and Column II", "marks": 6,
     "lead": "Indicate whether each description in COLUMN I applies to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.",
     "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Plant diversity", "marks": 8,
     "lead": "The phylogenetic diagram below shows possible evolutionary relationships in living organisms with four divisions.",
     "figure": P.fig("1.4", "A phylogenetic tree from a common ancestor to four divisions A, B, C and D: vascular tissue appears after A's "
                            "branch, seeds after B's, and X marks D's branch."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Population ecology", "marks": 9,
     "lead": "The graph below shows the interaction of between the lynx and hare population over time.",
     "figure": P.fig("1.5", "A line graph, PREDATOR-PREY GRAPH OF LYNX AND HARE POPULATION NUMBERS FROM 1845 TO 1895: population size "
                            "(thousands) against year, a dotted lynx line and a solid hare line rising and falling in turn, a dashed "
                            "carrying-capacity line near the top, a rising part of the hare line marked B and a falling part marked D."),
     "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Biotechnology", "marks": 13,
     "lead": "The diagram below shows a process in biotechnology on how insulin is produced for humans with diabetes mellitus.",
     "figure": P.fig("2.1", "Micro-organism X with its DNA and a plasmid, and a human cell with DNA: the plasmid is cut, a gene is cut from "
                            "the human DNA, and the two join as recombinant DNA."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Investigation", "marks": 10,
     "lead": "HIV/Aids has been a global health pandemic for many years, with more than 35 million lives lost globally through this disease. "
             "Although no cure for this virus has been developed, scientists have developed prevention therapy to stop and reduce the spread "
             "of HIV in humans.\nOne such prevention therapy for HIV/Aids is Pre-Exposure Prophylaxis (PrEP). PrEP works by stimulating the "
             "immune system into blocking an enzyme HIV needs to reproduce in the body. These drugs are usually taken daily at the same time "
             "interval by HIV negative people.\nScientists carried out an investigation to determine the effectiveness of PrEP drugs on "
             "preventing HIV infection in women. The procedure was as follows:\n• 5 338 women aged 16‒25 years old participated in the "
             "investigation and were divided into three groups (A, B and C).\n• Group A which consisted of 2 134 women, were given the "
             "Lenacapavir drug twice a year (once every 6 months).\n• Group B had 2 136 women participants who took the Descovy drug daily for "
             "a year.\n• Group C had 1 068 women participants who took the Truvada drug daily for a year.",
     "figure": P.fig("2.2", "A bar graph, INCIDENCE OF DEVELOPING HIV INFECTION TO DIFFERENT PrEP DRUGS (per 100): Lenacapavir about 0, "
                            "Descovy about 2, Truvada about 1,7."), "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Pollination", "marks": 13, "lead": "The diagram below shows pollination in flowering plants.",
     "figure": P.fig("2.3", "A bee carrying pollen from flower 1 to flower 2: A points to flower 1's anthers, B to the green parts under "
                            "flower 1, C to flower 2's coloured parts, D to the top of flower 2's centre, E below it, and the ovary at the "
                            "bottom."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Animal body plans", "marks": 2,
     "lead": "The diagram below shows an octopus, a triploblastic marine organism with eight limbs.",
     "figure": P.fig("2.4", "An octopus with its eight limbs labelled."), "items": q24},
    {"id": "2.4.3", "title": "Question 2.4.3", "kind": "Animal body plans", "marks": 8,
     "lead": "Diagram 1 and 2 below shows a possible body plan for an octopus.",
     "figure": P.fig("2.4.3", "DIAGRAM 1: two round layers, the ectoderm and endoderm, a non-living layer between, round the digestive "
                              "cavity. DIAGRAM 2: three layers, the ectoderm, a middle layer Y and the endoderm round the digestive cavity, "
                              "with a fluid-filled space X in layer Y."), "items": q243},
    {"id": "2.5", "title": "Question 2.5", "kind": "Invertebrates", "marks": 4, "lead": "Invertebrates in agriculture.", "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Human population", "marks": 13,
     "lead": "The graphs below show the population pyramids of China in the years 1980 and 2020.\nThe Chinese government introduced the One "
             "Child Policy in 1980 and other economic reform policies in the following years. These policies were designed to slow down the "
             "rapid population growth and increase the number of people of working-age. Under the One Child Policy married couples were "
             "allowed to have one child.",
     "figure": P.fig("3.1", "Two population pyramids. China 1980, population 982 372 466: wide at the base, narrowing quickly upwards. China "
                            "2020, population 1 424 929 781: narrower at the base, widest in the working ages, wider at the top."),
     "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Pollution", "marks": 15,
     "table": {"head": ["Type of plastic waste", "Amount of plastic (millions of tons)", "Amount of plastic (Percentage %)"],
               "rows": [["Landfill sites", "174", "49,3"], ["Incinerated (burned)", "67", "19"], ["Released into the environment", "79", "22,4"],
                        ["Recycled", "33", "9,3"]]},
     "lead": "Plastic pollution is linked to climate change, especially plastics that are only used once which are often disposed-off and in "
             "some cases burned in landfill sites in informal dwellings. The burning of plastic contributes negatively to people's health. "
             "Many attempts have been made by some municipalities and other organisations to recycle plastic with little success achieved.\n"
             "The table below shows the amount of plastic wasted in millions of tons (Mt) in 2019 by different types of plastic waste.",
     "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Invasive species", "marks": 11,
     "lead": "THE BRAZILIAN PEPPERTREE THREATENS BIODIVERSITY\nThe Brazilian peppertree (Schinus terebinthifolius) is an invasive alien plant "
             "in parts of South Africa that is indigenous to Brazil in South America. This plant which was initially introduced for "
             "ornamental and street tree purposes usually invades previously disturbed land areas and river margins.\nThe Brazilian "
             "peppertree has a rapid growth rate that enables it to outcompete indigenous vegetation by forming a dense canopy layer over "
             "other plants. This plant has poisonous berries that are harmful to wildlife such as birds and other animals that eat them, thus "
             "causing them to die. The growth of this invasive plant can reach up to 10 metres in height and it absorbs a lot of carbon "
             "dioxide from the atmosphere.", "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Global warming", "marks": 5, "lead": "Adverse weather patterns.", "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Competition and symbiosis", "marks": 6,
     "lead": "Competition and symbiosis exist in ecosystems to allow organisms to compete and interact with each other and share limited "
             "environmental resources. Competition often causes some organisms to die out if they are outcompeted while others survive.\nThe "
             "diagrams below show organisms competing.",
     "figure": P.fig("3.5", "DIAGRAM 1: two antelope of the same kind locking horns. DIAGRAM 2: zebras and impala grazing together."),
     "items": q35},
]
P.finish(missions,
         {"subject": "Life Sciences", "title": "Life Sciences P2", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.4.4", "kind": "no_fit", "detail": "The memo's compulsory mark (naming the coelom) + any TWO advantages × 2: five cards cover "
                                                     "the coelom and the memo's advantages, all five to pick for full marks."},
          {"n": "1.5.3", "kind": "no_fit", "detail": "Two years read off the graph: the years on the axis as cards, pick the memo's 1860 and "
                                                     "1890, one mark each."},
          {"n": "2.1.4", "kind": "no_fit", "detail": "The two drawings (2.1.4 the bacterium, 3.2.5 the pie chart) play as pick the drawing."},
          {"n": "3.2.5", "kind": "memo_issue", "detail": "The memo writes the sector angles with a % sign (177.48% …); they are degrees."}],
         {"1": 50, "2": 50, "3": 50}, 150, {"3.1.3": ["3.1.2(b)"]}, "Questions 1 to 3 (the whole paper)")
