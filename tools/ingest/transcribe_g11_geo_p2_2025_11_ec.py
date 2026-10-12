"""Grade 11 Geography P2 November 2025 (Eastern Cape Department of Education): SECTION A whole (Questions 1 and 2, 120 marks) and
SECTION B (Question 3) except the one part that reads the map (28 of its 30 marks), hand-transcribed into the catalogue format, then run
through `ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and the memo's own; clues and
figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2025 November Grade 11, the question paper zip (English PDF, 18
pages, text layer) and the marking-guideline zip (English, 9 pages).

  python tools/ingest/transcribe_g11_geo_p2_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-geo-p2-2025-11-ec/GEOGRAPHY P2 GR11 QP NOV2025_English_watermark.pdf" "uploads/provincial/g11-geo-p2-2025-11-ec/GEOGRAPHY P2 GR11  NOV2025 ENGLISH MARKING GUIDELINE_watermark.pdf" --id g11-geo-p2-2025-11-ec --from-json

SECTION B reads the EMALAHLENI 2529CC maps (a one-page map PDF is in the download, not yet set up as a figure), but most of it prints
its own figures (the sheet-numbering sketch, cross sections X and Y, FIGURES J and K) or asks general knowledge: only 3.2.2 (evidence of
mining in block B1, 2 marks) waits for the map. The paper totals 148.

The Geography rulings, as in transcribe_g11_geo_p1_2024_11_ec.py. Figure boxes are in PDF points, 1% inside their neighbours."""
from provincial import Paper

P = Paper("g11-geo-p2-2025-11-ec", 595.32, 842.04, {
    "1.1.7": [3, 338.0, 402.0, 512.0, 696.0], "1.1.8": [4, 335.0, 62.0, 492.0, 342.0], "1.2.1": [4, 90.0, 492.0, 507.0, 604.0],
    "1.2.5": [5, 99.0, 462.0, 508.0, 620.0], "1.4": [7, 171.0, 96.0, 439.0, 305.0], "1.5": [8, 91.0, 90.0, 254.0, 304.0],
    "2.2": [9, 90.0, 434.0, 492.0, 632.0], "2.2.5": [10, 119.0, 75.0, 472.0, 376.0], "2.3": [11, 107.0, 95.0, 483.0, 409.0],
    "2.4": [12, 82.0, 92.0, 505.0, 294.0], "3.1": [15, 190.0, 140.0, 400.0, 310.0], "3.1.5": [16, 81.0, 110.0, 500.0, 296.0],
    "3.3": [17, 100.0, 328.0, 486.0, 562.0]}, start=2)
work, stmt, mcq, term, num = P.work, P.stmt, P.mcq, P.term, P.num
two = lambda n, q, a_opt, b_opt, a, clues, marks=1, **kw: mcq(n, q, [a_opt, b_opt], a, clues, marks=marks, **kw)
YZ = ["Y", "Z"]
CN = ("Conventional", "Non-conventional")

# ---- SECTION A, QUESTION 1: DEVELOPMENT, the question paper pages 3-8 and the memo pages 2-4 ----
q11 = [
    two("1.1.1", "The Gross Domestic Product is a(n) … indicator of development.", "social", "economic", 1, ["Money.", "Production."]),
    two("1.1.2", "The indicators for the … include life expectancy, GDP per capita and level of education.", "Human Development Index",
        "Gini co-efficient", 0, ["Health, wealth, education.", "HDI."]),
    two("1.1.3", "A country with a Gini co-efficient of 0,7 indicates … distribution of wealth.", "equal", "unequal", 1,
        ["0 is equal, 1 is unequal.", "0,7 is high."]),
    two("1.1.4", "Infant mortality rate and life expectancy are … indicators.", "demographic", "social", 0, ["Population data.", "Births and "
                                                                                                                 "deaths."]),
    two("1.1.5", "A country with a Human Development Index of 0,94 has a … quality of life.", "high", "low", 0, ["HDI runs 0 to 1.",
                                                                                                                "0,94 is near 1."]),
    two("1.1.6", "The Gross National Income per capita indicates … average income.", "the country's", "a person's", 1, ["Per capita.",
                                                                                                                       "Per person."]),
    mcq("1.1.7", "The urbanisation rate typical of a Less Economically Developed Country (LEDC).", YZ, 1,
        ["LEDCs are less urbanised but urbanising fast.", "Which graph starts low and climbs?"], marks=1,
        figure=P.fig("1.1.7", "Two line graphs of the percentage of people in urban areas, 1950 to 2025: Y from about 55% to about 80%; Z "
                              "from about 20% to about 55%.")),
    mcq("1.1.8", "The population pyramid typical of a More Economically Developed Country (MEDC).", YZ, 1,
        ["MEDCs have few births and many older people.", "Narrow base."], marks=1,
        figure=P.fig("1.1.8", "Two population pyramids by age and sex: Y wide at the base, narrowing quickly; Z narrower at the base, with "
                              "more people in the older age groups."))]
q12 = [
    mcq("1.2.1", "The Sustainable Development Goals (SDGs) represent development from a … context.", ["local", "national", "regional",
                                                                                                    "global"], 3,
        ["Adopted by all UN member states.", "The whole world."], marks=1,
        figure=P.fig("1.2.1", "Five SUSTAINABLE DEVELOPMENT GOALS: 1 No poverty, 2 Zero hunger, 3 Good health, 4 Quality education, 5 Gender "
                              "equality.")),
    mcq("1.2.2", "The goal of reducing risk from disasters and economic shocks:", ["No poverty", "Zero hunger", "Good health",
                                                                                   "Quality education"], 0,
        ["Shocks push people into poverty.", "Goal 1."], marks=1),
    mcq("1.2.3", "Factors used to determine the Gender Inequality Index (GII): (i) Population life expectancy (ii) Health of girls and women "
        "(iii) Political representation of women (iv) Women's access to resources", ["(i) and (iii)", "(i) and (iv)", "(ii) and (iv)",
                                                                                     "(ii) and (iii)"], 3,
        ["About women.", "Health and empowerment."], marks=1),
    mcq("1.2.4", "A country with a high Gender Inequality Index (GII) is most likely to have …", ["limited job opportunities for women.",
                                                                                                 "fair access to education for boys and girls.",
                                                                                                 "equal pay between men and women.",
                                                                                                 "fair opportunities for everyone."], 0,
        ["High GII means high inequality.", "Unfair to women."], marks=1),
    mcq("1.2.5", "The country with the largest per capita carbon emissions:", ["Nigeria", "USA", "Canada", "China"], 2,
        ["Read the CO₂ bars.", "The longest bar."], marks=1,
        figure=P.fig("1.2.5", "A double bar graph for Rwanda, Kenya, Nigeria, USA, China and Canada: CO₂ emissions per capita (metric ton) to "
                              "the left and GDP per capita (thousands $) to the right.")),
    mcq("1.2.6", "The relationship between a country's GDP and its per-capita CO₂ emissions:",
        ["GDP and CO₂ emissions per capita are unrelated", "As GDP increases; per capita CO₂ emissions decrease",
         "As GDP increases; per capita CO₂ emissions increase", "Higher GDP guarantees lower emissions"], 2,
        ["Compare the two sides of the graph.", "Long bars on both sides."], marks=1),
    mcq("1.2.7", "… aims to balance economic growth, social inclusion and environmental protection:", ["Industrial development",
                                                                                                      "Sustainable development",
                                                                                                      "Modernisation", "Appropriate "
                                                                                                                       "development"], 1,
        ["Balance for the future.", "Sustainable."], marks=1)]
NC = ("FAILURE OF COMMUNITY-OWNED MACADAMIA NUT FARM\nThe Ncera Macadamia Nut Farm was launched in 2006 as a model of community-based rural "
      "development, aiming to empower local people. To support the project's development, it initially received over R135 million in "
      "investment. The money was sourced primarily from government departments and other public sector and development partners. In line "
      "with the principles of community-driven development, ownership of the farm was transferred to the Ncera community under the "
      "leadership of the Imidushane Council.\nDespite its ambitious goals, the nut farm struggled to gain momentum (success). It eventually "
      "collapsed in 2024 due to a combination of factors, including mismanagement of funds, government delays in infrastructure, limited "
      "skills among workers and a crash in macadamia nut prices.")
q13 = [
    stmt("1.3.1", "According to the extract, what was the main aim of this community-based rural development project?", 1,
         ["To empower local people."], ["To make a profit for investors.", "To export nuts to China.", "To build a city.",
                                        "To train government officials."], ["Read the first sentence.", "Aiming to …"], 1),
    stmt("1.3.2", "Quote evidence from the extract that this project was a multi-stakeholder collaboration.", 2,
         ["The money was sourced primarily from government departments and other public sector and development partners."],
         ["The Ncera Macadamia Nut Farm was launched in 2006.", "It eventually collapsed in 2024.",
          "The nut farm struggled to gain momentum (success).", "It initially received over R135 million in investment."],
         ["Many partners.", "Who gave the money?"], 2),
    stmt("1.3.3", "What economic reasons contributed to the project's failure?", 2, ["Mismanagement of funds", "A crash in macadamia nut "
                                                                                     "prices"],
         ["Limited skills among workers", "Good rainfall", "Ownership by the community"], ["Money and prices.", "Economic."], 1),
    stmt("1.3.4", "Explain the negative impact on the local people after the failure of the project.", 4,
         ["Loss of jobs, leaving families without income.", "Increase in poverty levels.", "Lack of trust in community leaders.",
          "Rural-urban migration (brain drain)."],
         ["More jobs on the farm.", "Higher incomes for local families."], ["The farm closed.", "Jobs and trust."], 2),
    stmt("1.3.5", "Suggest strategies that could be put in place to ensure that other community-based rural development projects are more "
         "sustainable.", 6,
         ["Provide education and skills development.", "Deliver infrastructure on time.", "Set up a monitoring and evaluation system.",
          "Involve residents in planning and decision-making."],
         ["Exclude the community from decisions.", "Stop all training."], ["Skills, support, monitoring.", "Involve the people."], 2)]
SH = ("BALANCING CONSUMER GAINS AND LOCAL INDUSTRY COSTS\nMajor online retailers* Shein and Temu have rapidly expanded their presence in South "
      "Africa. Since entering the market in 2020 and 2023 respectively, they have captured over a third of online clothing sales, and in "
      "2024, generated an estimated R7,3 billion.\nTheir success was driven by South Africa's previous customs relief system, which let "
      "imports under R500 be charged only a 20% import duty (tariff) without VAT. This kept prices low and allowed them to sell goods much "
      "cheaper than local competitors.\nIt has now been proposed to the South African government that customs relief be removed so that "
      "every imported item will be charged both the 20% import duty (tariff) and the 15% VAT.\n* Online retailer: business that sells goods "
      "to consumers over the internet")
q14 = [
    term("1.4.1", "Identify the country from where Temu and Shein products are imported.", ["China"], ["Read the boxes in the image.",
                                                                                                      "Made in …"]),
    stmt("1.4.2", "According to the extract, what economic advantage do online retailers have over local South African companies?", 2,
         ["They benefited from the customs relief system, paying only import duty without VAT.", "They are able to sell goods cheaper."],
         ["They pay higher taxes than local companies.", "They employ more South Africans.", "They sell only luxury goods."],
         ["Read the second paragraph.", "No VAT."], 2),
    stmt("1.4.3", "What are the benefits for the local consumer buying from these international online retailers?", 4,
         ["Lower prices.", "Access to a wider range of products.", "Convenience of shopping online.", "Access to the latest fashion."],
         ["Higher prices.", "Less variety."], ["Cheap and convenient.", "Choice."], 2),
    stmt("1.4.4", "In a paragraph of approximately EIGHT lines, explain why South Africa has considered altering (changing) trade agreement "
         "terms.", 8,
         ["To protect local businesses that are undercut by cheaper goods.", "To encourage local production, which contributes to the economy.",
          "To save jobs in local industries.", "To increase government revenue through higher tariffs.", "To help reduce the growing trade "
                                                                                                          "deficit."],
         ["To make imports even cheaper.", "To close local factories.", "To remove all taxes on imports."],
         ["Protect local industry.", "Jobs and revenue."], 2)]
SO = ("Bilateral aid from the United States (U.S.), mainly through USAID, has long been one of Somalia's largest sources of external support. "
      "In the health sector, its primary goal was to save lives during emergencies, respond to disease outbreaks and provide emergency medical "
      "care.\nIn 2025, U.S. aid was reduced by $616 million (over 80 percent), mainly due to domestic financial pressures, concerns over aid "
      "effectiveness and geopolitical changes. Somalia now has to face the consequences of an 'aid trap' that has made its healthcare system "
      "highly vulnerable.")
q15 = [
    stmt("1.5.1", "What is bilateral aid?", 2, ["Aid from one government (country) to another."],
         ["Aid from many countries through the UN.", "Aid from a charity to a person.", "A loan from a bank.", "Trade between two companies."],
         ["Bi- means two.", "Country to country."], 2),
    stmt("1.5.2", "Why is this health aid an example of humanitarian aid?", 1, ["It saves lives during emergencies.", "It alleviates "
                                                                                                                     "suffering."],
         ["It builds factories.", "It earns interest.", "It funds armies."], ["Emergencies.", "Saving lives."], 1),
    stmt("1.5.3", "How does the cartoon illustrate changes regarding development aid from the USA?", 2,
         ["The USA is cutting off (literally cutting) the money (aid)."], ["The USA is doubling its aid.", "Somalia is giving aid to the USA.",
                                                                           "The aid is unchanged.", "The aid is being turned into loans."],
         ["Look at the scissors.", "Cutting."], 2),
    stmt("1.5.4", "What factors have contributed to Somalia becoming caught in an 'aid trap'?", 4,
         ["It became dependent on aid over the years.", "It relied on continuous support.", "Weak government institutions.",
          "Overreliance on a few key donors."],
         ["It never received aid.", "It has a strong, self-reliant economy."], ["Dependence.", "Weak systems."], 2),
    stmt("1.5.5", "Explain the negative social impact that the reduction of aid from the USA will have on the people of Somalia.", 6,
         ["Decrease in quality of life.", "Increased poverty.", "Reduced access to basic services such as healthcare.", "Higher death rate.",
          "Increased food insecurity."],
         ["Better healthcare for all.", "Fewer deaths."], ["Health and survival.", "Poverty."], 2)]

# ---- QUESTION 2: RESOURCES AND SUSTAINABILITY, the question paper pages 9-13 and the memo pages 5-7 ----
q21 = [two("2.1.%d" % (k + 1), "Classify the energy source as conventional or non-conventional: " + src, *CN, a,
           ["Conventional: widely used for a long time.", "Renewables are non-conventional."])
       for k, (src, a) in enumerate([("Wind", 1), ("Geothermal", 1), ("Nuclear", 0), ("Thermal", 0), ("Solar", 1), ("Biofuel", 1),
                                     ("Hydro", 0)])]
q22 = [
    two("2.2.1", "The generation of nuclear energy in South Africa (2022‒2024) shows a … trend.", "decreasing", "increasing", 0,
        ["Read the bars for 2022 to 2024.", "12,15 then 10,09 then 8,13."]),
    two("2.2.2", "Nuclear energy contributes … % to South Africa's total energy supply.", "4,2", "82,5", 0, ["Read the donut chart.",
                                                                                                           "82,5 is coal."]),
    two("2.2.3", "Nuclear energy is produced by the fission of … atoms.", "carbon", "uranium", 1, ["Nuclear fuel.", "Radioactive."]),
    two("2.2.4", "An advantage of nuclear energy is that it is a … -carbon energy source.", "low", "high", 0, ["No burning.", "Few "
                                                                                                                 "emissions."]),
    two("2.2.5", "South Africa's only nuclear power plant is located in the ... province.", "Northern Cape", "Western Cape", 1,
        ["Koeberg.", "Read the map."],
        figure=P.fig("2.2.5", "SOUTH AFRICA'S NUCLEAR POWER STATION: a map of South Africa's provinces with Koeberg marked on the coast north "
                              "of Cape Town.")),
    two("2.2.6", "Nuclear power is a … energy source.", "renewable", "non-renewable", 1, ["Uranium runs out.", "Mined."]),
    two("2.2.7", "The nuclear power plant produces electricity that is fed into the national grid operated by …", "Eskom", "Koeberg", 0,
        ["Koeberg is the plant.", "The national utility."]),
    two("2.2.8", "A disadvantage of using nuclear energy is the …", "high operational costs", "radioactive waste", 1, ["Waste stays dangerous.",
                                                                                                                   "Radioactive."])]
SE = ("Although soil erosion is a natural process worsened by climate change, human activities such as overgrazing, deforestation and poor "
      "farming practices accelerate erosion. Agricultural intensification often removes natural vegetation, exposing soil to erosion.\nAs soil "
      "forms very slowly, it is considered a non-renewable resource and its loss reduces productivity and threatens food security. South "
      "Africa's average soil loss rate is 12,6 tons per hectare annually, while the natural formation rate is approximately 4,9 tons per "
      "hectare per year. This imbalance highlights the urgent need for better land management efforts.")
q23 = [
    term("2.3.1", "From the map, identify the province that is most severely affected by erosion.", ["Northern Cape"],
         ["The largest number of hectares.", "160 885."]),
    stmt("2.3.2", "Quote evidence from the passage, that shows soil loss exceeds soil formation in South Africa.", 2,
         ["South Africa's average soil loss rate is 12,6 tons per hectare annually, while the natural formation rate is approximately 4,9 "
          "tons per hectare per year."],
         ["Soil erosion is a natural process worsened by climate change.", "This imbalance highlights the urgent need for better land "
                                                                          "management efforts.",
          "Agricultural intensification often removes natural vegetation.", "Soil is considered a non-renewable resource."],
         ["Two numbers compared.", "Loss against formation."], 2),
    stmt("2.3.3", "What is the negative economic impact of reduced soil quality for farmers?", 4,
         ["Decreased crop yield.", "Reduced income and profit.", "Increased operating costs.", "Reduced farm value."],
         ["Higher crop yields.", "Lower costs."], ["Less produce.", "Less income."], 2),
    stmt("2.3.4", "In a paragraph of about EIGHT lines, suggest sustainable strategies that farmers could use to reduce soil erosion.", 8,
         ["Plant cover crops and trees.", "Contour ploughing across a slope.", "Introduce crop rotation.", "Build terraces on slopes.",
          "Avoid overgrazing."],
         ["Plough straight down steep slopes.", "Remove all vegetation.", "Burn the veld regularly."], ["Protect and hold the soil.",
                                                                                                       "Cover, contours, rotation."], 2)]
WF = ("COOKHOUSE WIND FARM\nInvestment in and development of wind power in South Africa have increased due to South Africa's rising electricity "
      "demand. The Cookhouse Wind Farm in the Eastern Cape is an ideal site for wind energy because of its low population density, plateau "
      "landscape and strong average wind speeds, factors that allow wind turbines to be installed with minimal disruption to farming and "
      "nearby settlements. Occupying only a small portion of leased land, the farm generates approximately 341,000 MWh of energy annually. "
      "Beyond energy production, the Cookhouse Wind Farm makes a meaningful contribution to the community and local economy.")
q24 = [
    two("2.4.1", "Wind energy is classified as (renewable / non-renewable).", "renewable", "non-renewable", 0, ["Wind never runs out.",
                                                                                                             "Renewable."]),
    term("2.4.2", "What trend does the graph indicate about wind energy in South Africa from 2014 to 2024?", ["increase", "increasing",
                                                                                                             "it increases", "increased"],
         ["Read the bars.", "Up or down?"]),
    stmt("2.4.3", "According to the extract, to what can the trend be attributed?", 1, ["South Africa's rising electricity demand."],
         ["Falling electricity demand.", "The closing of the wind farm.", "Low wind speeds.", "Coal shortages in Europe."],
         ["Read the first sentence.", "Due to …"], 1, after=["2.4.2"]),
    stmt("2.4.4", "From the extract, state TWO physical (natural) factors that promoted the development of the wind farm in Cookhouse.", 2,
         ["Plateau landscape", "Strong average wind speeds"], ["Low population density", "Leased land", "Rising electricity demand"],
         ["Physical: nature.", "Land and wind."], 1),
    stmt("2.4.5", "What are the environmental advantages of using wind energy?", 4,
         ["It does not deplete any natural resource.", "No carbon (greenhouse gas) emissions.", "No waste products.", "No water use."],
         ["It burns coal.", "It creates radioactive waste."], ["Clean energy.", "Nothing burnt."], 2),
    stmt("2.4.6", "Explain how the Cookhouse Wind Farm benefits the local community socially, beyond energy production.", 6,
         ["On-site training leads to upskilling.", "Employment at the wind farm decreases poverty.", "Social programmes improve quality of life.",
          "Less unemployment reduces crime."],
         ["It forces people to leave the area.", "It closes local schools."], ["Jobs and skills.", "Community programmes."], 2)]
CC = ("SOUTH AFRICA'S CLIMATE CHANGE ACT: A GREENER FUTURE\nAdopted on 18 July 2024, South Africa's Climate Change Act marks a major turning "
      "point in the country's move towards a greener economy. The Act sets an ambitious target: achieving net-zero greenhouse gas (GHG) "
      "emissions by 2050. It introduces a multi-tiered governance model that clearly defines responsibilities across different levels of "
      "government. Additionally, the Act sets sector-specific GHG reduction targets, encouraging businesses to adopt cleaner practices. This "
      "shift is expected to attract both local and international investment ─ particularly in renewable energy sectors such as solar and wind "
      "─ while also strengthening energy security and reducing dependence on coal. At the individual level, the Act promotes "
      "energy-conscious living.")
q25 = [
    stmt("2.5.1", "According to the extract, what is the main target of South Africa's Climate Change Act?", 1,
         ["Achieving net-zero greenhouse gas emissions by 2050."], ["Building more coal power stations.", "Doubling coal exports.",
                                                                    "Ending all renewable energy.", "Raising electricity prices."],
         ["An ambitious target.", "Net-zero."], 1),
    stmt("2.5.2", "From the extract, identify who will be key to reaching this target.", 2, ["Government", "Businesses", "Individuals"],
         ["Foreign armies", "Coal mines only", "Tourists"], ["Read the extract: levels of government, …", "Three groups."], 1),
    stmt("2.5.3", "In what way does South Africa's Climate Change Act hope to strengthen energy security in South Africa?", 2,
         ["By promoting renewable energy.", "By diversifying energy sources.", "By reducing dependence on coal."],
         ["By building more coal plants.", "By importing all electricity.", "By banning solar power."], ["Renewables.", "Less coal."], 2),
    stmt("2.5.4", "How will a reduced dependence on coal positively impact the environment?", 4,
         ["Fewer greenhouse gas emissions.", "Improved air quality.", "Less acid rain.", "Reduced land degradation from mining."],
         ["More air pollution.", "More acid rain."], ["Burning coal pollutes.", "Air, rain, land."], 2),
    stmt("2.5.5", "Explain the economic challenges that South Africa faces in fully transitioning (changing) to a greener economy.", 6,
         ["The transition is expensive and needs large investments.", "It increases national debt.", "Jobs related to coal will be lost.",
          "Coal mining towns will suffer economic decline."],
         ["The transition costs nothing.", "Coal jobs will increase."], ["Costs and jobs.", "Coal-dependent economy."], 2)]

# ---- SECTION B, QUESTION 3, the question paper pages 14-18 and the memo pages 8-9 (3.2.2 reads the map and waits) ----
EM = ("GENERAL INFORMATION ON EMALAHLENI\nEmalahleni, formerly known as Witbank, is a city in Mpumalanga whose name is derived from the Nguni "
      "language, means 'place of coal'. It is one of South Africa's major coal-mining hubs. The city is home to several large Eskom "
      "coal-fired power stations that contribute significantly to the country's electricity supply. Emalahleni also benefits from a "
      "well-developed transport infrastructure, with railway lines connecting it to Pretoria and the Maputo Port in Mozambique. Additionally, "
      "the convergence of the N4 and N12 highways supports the efficient transport of coal and other goods.")
q31 = [
    mcq("3.1.1", "In the map reference 2529 CC, what does the 25 represent?", ["Degrees south of the equator", "Minutes south of the equator",
                                                                               "Degrees east of the Greenwich Meridian",
                                                                               "Degrees north of the equator"], 0,
        ["Latitude comes first.", "South Africa is south of the equator."], marks=1),
    mcq("3.1.2", "Which sheet will be directly to the east of the 2529 CC map?", ["2529 BC", "2529 BB", "2529 CD", "2529 DC"], 2,
        ["Read the sketch: C is divided into A, B, C, D.", "East of CC within block C."], marks=1),
    work("3.1.3", "Calculate the area (m²) of the reservoir at R on the 1 : 10 000 orthophoto map. Use the following information: Length = 0,9 "
         "cm; Breadth = 0,9 cm. Formula: Area = Length (L) × Breadth (B)", 2, [
        "0,9 cm × 100 = 90 m\nArea = 90 m × 90 m\n= 8 100 m²",            # the memo
        "0,9 cm × 500 = 450 m\nArea = 450 m × 450 m\n= 202 500 m²",       # the topographical map's scale
        "0,9 cm × 10 = 9 m\nArea = 9 m × 9 m\n= 81 m²",                   # 1 cm taken as 10 m
        "0,9 cm = 0,9 m\nArea = 0,9 m × 0,9 m\n= 0,81 m²"],               # not converted
        ["1 cm on a 1 : 10 000 map = 100 m.", "Change both sides to metres first."]),
    stmt("3.1.4", "Why does the reservoir appear bigger on the orthophoto map compared to the same reservoir on the topographical map?", 2,
         ["The orthophoto map has a larger scale.", "The orthophoto map's scale is five times larger."],
         ["The orthophoto map has a smaller scale.", "The reservoir is a different one.", "Orthophotos are always printed on bigger paper."],
         ["1 : 10 000 against 1 : 50 000.", "Scale."], 2)]
q315 = [
    num("3.1.5", "What is the contour interval of the orthophoto map?", 5, 0, "m", ["Orthophotos use a small interval.", "Metres."]),
    work("3.1.6", "Determine the vertical interval (VI) between P and Q.", 2, [
        "VI = 1 590 m − 1 565 m\n= 25 m",      # the memo
        "VI = 1 590 m + 1 565 m\n= 3 155 m",   # added
        "VI = 1 585 m − 1 565 m\n= 20 m",      # P misread
        "VI = 1 590 m ÷ 1 565 m\n= 1,02 m"],   # divided
        ["Read P's and Q's heights on the cross sections.", "VI = the difference in height."]),
    mcq("3.1.7", "The vertical exaggeration of cross section X is … than that of cross section Y which makes the slope appear … (i) greater "
        "(ii) smaller (iii) steeper (iv) gentler", ["(i) and (iv)", "(ii) and (iv)", "(i) and (iii)", "(ii) and (iii)"], 2,
        ["X's vertical axis is stretched more.", "Stretched looks steeper."], marks=1)]
q32 = [
    two("3.2.1", "(Coal / Platinum) is the main mineral mined in Emalahleni.", "Coal", "Platinum", 0, ["'Place of coal'.", "Read the "
                                                                                                          "general information."]),
    stmt("3.2.3", "In what way could mining activity negatively affect the residents of Coronation Village and KwaGuqa?", 2,
         ["Exposure to noise pollution", "Health risks from dust", "Contamination of water", "Blasting can damage homes"],
         ["Cleaner air", "Higher property values"], ["Mines near homes.", "Noise, dust, water."], 1),
    stmt("3.2.4", "Explain the positive impact that well-developed rail and road infrastructure has had on the mining industry in Emalahleni.",
         4, ["It allows effective transport of goods and raw materials.", "It gives access to major markets.", "Transport costs are reduced.",
             "It allows the bulk movement of commodities."],
         ["It makes coal harder to move.", "It raises transport costs."], ["Rail to Maputo, the N4 and N12.", "Moving coal."], 2),
    mcq("3.2.5", "Refer to the area demarcated by S on the topographical map. A human factor that could have contributed to the soil erosion:",
        ["Heavy rain", "Flooding", "Deforestation", "Strong wind"], 2, ["Human, not natural.", "Removing trees."], marks=1),
    stmt("3.2.6", "How can the soil erosion along the river banks negatively impact the quality of the river water?", 2,
         ["Increased sedimentation (cloudiness)", "Sediments can carry pollutants", "Eutrophication from increased nutrients"],
         ["Cleaner water", "More fish"], ["Soil washes in.", "Sediment and pollutants."], 1)]
q33 = [
    two("3.3.1(a)", "Classify the following data about the stadium as either attribute or spatial data: 25°53'02\"S; 29°12'48\"E", "Spatial",
        "Attribute", 0, ["Co-ordinates give location.", "Where."]),
    two("3.3.1(b)", "Classify the following data about the stadium as either attribute or spatial data: Puma Stadium", "Spatial", "Attribute",
        1, ["A name describes the feature.", "What."]),
    mcq("3.3.2", "FIGURE J shows data collected by a satellite using the process of …", ["remote sensing.", "data manipulation.",
                                                                                         "observation.", "data integration."], 0,
        ["From a distance.", "Remote."], marks=1),
    mcq("3.3.3", "FIGURE J is a(n) … aerial photograph showing the stadium at a(n) … angle. (i) oblique (ii) vertical (iii) 90° (iv) 30°",
        ["(i) and (iii)", "(i) and (iv)", "(ii) and (iv)", "(ii) and (iii)"], 3, ["Taken from directly above.", "A right angle."], marks=1),
    two("3.3.4", "FIGURE J represents (vector / raster) data.", "vector", "raster", 1, ["A photograph.", "Pixels."]),
    stmt("3.3.5", "Give a reason for the answer to QUESTION 3.3.4.", 2, ["It is made up of pixels.", "The data is cell-based."],
         ["It is made of points, lines and polygons.", "It is drawn by hand.", "It has no colour."], ["Zoom in on a photo.", "Cells."], 2,
         after=["3.3.4"]),
    term("3.3.6", "What type of feature is used to represent the two-dimensional shape of the stadium in FIGURE K?", ["area", "polygon",
                                                                                                                     "area feature"],
         ["Two-dimensional.", "Not a point or a line."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Indicators of development", "marks": 8,
     "lead": "Complete the statements in COLUMN A with the options in COLUMN B.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Multiple choice", "marks": 7,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Community-based development", "marks": 15,
     "lead": "Refer to the extract below on community-based development.\n" + NC, "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Trade", "marks": 15, "lead": "Refer to the image and extract on South African trading "
                                                                                 "relationships.\n" + SH,
     "figure": P.fig("1.4", "A phone and laptop showing the TEMU and SHEIN apps and ONLINE SHOPPING, BUY NOW, beside parcels marked MADE IN "
                            "CHINA."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Development aid", "marks": 15,
     "lead": "Refer to the cartoon and extract on development aid in Somalia.\n" + SO,
     "figure": P.fig("1.5", "A cartoon: Uncle Sam (USA) cutting with scissors the strings of a bag of USAID money."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Energy sources", "marks": 7,
     "lead": "Classify each energy source in South Africa as either conventional or non-conventional.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Nuclear energy", "marks": 8,
     "lead": "Refer to the infographic on nuclear energy in South Africa. Complete the statements in COLUMN A with the options in COLUMN B.",
     "figure": P.fig("2.2", "A bar graph, NUCLEAR ENERGY GENERATION IN SA (BILLION KILOWATT/HOUR): 13,3 (2020), 11,62 (2021), 12,15 (2022), "
                            "10,09 (2023), 8,13 (2024); and a donut chart, SOUTH AFRICA'S ENERGY SOURCES (%): coal 82,5, wind 5,1, nuclear "
                            "4,2, other 4,8, solar 3,4."), "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Soil erosion", "marks": 15,
     "lead": "Refer to the map and extract below based on soil erosion in South Africa.\n" + SE,
     "figure": P.fig("2.3", "A map, SOIL EROSION (IN HECTARES) PER PROVINCE: Northern Cape 160 885, Eastern Cape 151 759, Kwa-Zulu Natal "
                            "87 522, Free State 64 674, Limpopo 58 669, Western Cape 25 403, Mpumalanga 17 420, North West 10 782, Gauteng "
                            "110."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Wind energy", "marks": 15,
     "lead": "Refer to the graph and extract on wind energy in South Africa.\n" + WF,
     "figure": P.fig("2.4", "A bar graph, TOTAL WIND ENERGY (MW) IN SOUTH AFRICA (2014–2024), every second year, the bars rising from about "
                            "300 to about 3 400 MW."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Energy management", "marks": 15,
     "lead": "Refer to the extract on energy management in South Africa.\n" + CC, "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Map skills", "marks": 6, "lead": EM,
     "figure": P.fig("3.1", "A sketch of map sheet numbering: the 1° square at 25° S and 29° E divided into A, B, C and D, with C divided again "
                            "into A, B, C and D and its C shaded; a north arrow."), "items": q31},
    {"id": "3.1.5", "title": "Question 3.1.5 – 3.1.7", "kind": "Cross sections", "marks": 4,
     "lead": "Refer to P and Q on the orthophoto map and the cross sections (X and Y) below.",
     "figure": P.fig("3.1.5", "CROSS SECTION X and CROSS SECTION Y from P to Q: height (m) against distance, P at 1 590 m and Q at 1 565 m; X's "
                              "vertical axis is stretched more than Y's."), "items": q315},
    {"id": "3.2", "title": "Question 3.2", "kind": "Map interpretation", "marks": 10, "lead": EM, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "GIS", "marks": 8,
     "lead": "FIGURE J is an aerial photograph of the Puma Stadium. FIGURE K shows the Puma Stadium as indicated on the topographical map.",
     "figure": P.fig("3.3", "FIGURE J: an aerial photograph of a stadium from above, a 50 m scale bar. FIGURE K: the stadium on the 1 : 50 000 "
                            "topographical map, labelled Stadium."), "items": q33},
]
P.finish(missions,
         {"subject": "Geography", "title": "Geography P2", "sitting": "November 2025", "total_marks": 148, "time": "3 hours"},
         [P.flag_workings(),
          {"n": "3.2", "kind": "missing_resource", "detail": "3.2.2 (evidence of mining activity in block B1, 2 marks) reads the EMALAHLENI "
                                                             "2529CC topographical map; a one-page map PDF is in the download but not yet a "
                                                             "figure, so the part waits; the paper plays 148."}],
         {"1": 60, "2": 60, "3": 28}, 148, {"2.4.3": ["2.4.2"], "3.3.5": ["3.3.4"]}, "Section A whole and Section B except 3.2.2")
