"""Grade 10 Geography P2 November 2024 (Eastern Cape Department of Education, provincial assessment): SECTION A whole (Questions 1
and 2, 120 marks) and the parts of SECTION B (Question 3) that do not read the maps (19 of its 30 marks), hand-transcribed into the
catalogue format, then run through `ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and
the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): stanmorephysics.com, one scanned PDF of the paper
(18 pages) and the marking guidelines (9 pages), split by page into QP and MG files (no text layer), read from page images (100 dpi).
A stand-in: no Grade 10 Geography P2 Nov 2025 paper is published.

  python tools/ingest/transcribe_g10_geo_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g10-geo-p2-2024-11-ec/g10-geo-p2-2024-11-ec QP.pdf" "uploads/provincial/g10-geo-p2-2024-11-ec/g10-geo-p2-2024-11-ec MG.pdf" --id g10-geo-p2-2024-11-ec --from-json

SECTION B reads a 1 : 50 000 topographical map and a 1 : 10 000 orthophoto map of Caledon handed out in the exam room: not in the
download. As every Geography paper, the parts that read the maps (3.1.3, 3.1.4, 3.2.1-3.2.4: 11 marks) wait for the maps; the rest
plays (3.1.5 gives its measurements in the stem; 3.2.5 asks what dams do for farmers). The paper totals what is playable, 139.

The Geography rulings, as Grade 12: a printed choice is multiple choice as printed; a written answer is statements (the memo's points
and clearly wrong ones, a card worth what the memo ticks); a calculation is four workings; a quote is a pick of the extract's
sentences; the grave symbol (3.3.5) is a multiple choice of symbols. Figure boxes in PDF points (page 595 x 842), measured on the page
images (100 dpi, scale 1.3889)."""
from provincial import Paper, sentences

P = Paper("g10-geo-p2-2024-11-ec", 595.32, 842.04, {
    "1.1": [3, 52, 222, 543, 497], "1.2a": [4, 79, 196, 511, 317], "1.2b": [5, 79, 138, 511, 274], "1.2c": [6, 79, 125, 511, 226],
    "1.3": [7, 84, 141, 513, 590], "1.4": [8, 52, 139, 546, 536], "1.5": [9, 166, 134, 430, 290], "2.4": [13, 102, 315, 524, 574],
    "2.5": [14, 146, 356, 446, 540], "3.3a": [18, 180, 99, 425, 248], "3.3b": [18, 92, 346, 513, 483]}, start=13)
answer, stmt, mcq, term, sort, work = P.answer, P.stmt, P.mcq, P.term, P.sort, P.work
yz = lambda n, q, y_opt, z_opt, a, clues: mcq(n, q, [y_opt, z_opt], a, clues, marks=1)
m1 = lambda n, q, opts, a, clues, **kw: mcq(n, q, opts, a, clues, marks=1, **kw)
pick = lambda n, q, opts, pool, clues, count: {"t": "pickn", "n": n, "marks": count, "q": q, "clues": clues, "opts": opts, "pool": pool,
                                               "count": count}
FACTOR = ["Physical", "Social", "Economic"]
fac = lambda n, q, a, clues: mcq(n, q, FACTOR, a, clues, marks=1)

# ---- SECTION A, QUESTION 1: POPULATION, the question paper pages 3-9 and the memo pages 2-5 ----
q11 = [  # Y first, Z second, as printed
    yz("1.1.1", "Over a quarter of South Africa's population lives in …", "Gauteng", "KwaZulu-Natal", 0,
       ["Read the longest bar.", "A quarter is 25%."]),
    yz("1.1.2", "South Africa's population is … distributed among provinces.", "evenly", "unevenly", 1,
       ["Compare 2,2% with 26,3%.", "Are the bars the same length?"]),
    yz("1.1.3", "… is the number of people that occupy a km² of land in the Western Cape.", "population density", "population distribution", 0,
       ["People per km².", "The table's last column."]),
    yz("1.1.4", "The province with the second lowest population in the country is …", "Western Cape", "Free State", 1,
       ["The lowest is the Northern Cape.", "Read the next bar up."]),
    yz("1.1.5", "Population size in KwaZulu-Natal is … than the population of the Western Cape.", "larger", "smaller", 0,
       ["12 423 907 against 7 113 776.", "Read the table."]),
    yz("1.1.6", "An economic factor that attracts people to Gauteng is …", "Reliable water", "Developed economy", 1,
       ["Economic: jobs and money.", "Water is physical."]),
    yz("1.1.7", "Northern Cape province has a … population density because of the vast land size and arid climate.", "low", "high", 0,
       ["3,64 people per km².", "Big and dry."])]
q12 = [
    mcq("1.2.1", "The type of migration shown in the diagram is …", ["Urbanisation", "Urban-rural migration", "Urban growth",
        "Rural-urban migration"], 3, ["The arrow points from the farm to the city.", "From rural to urban."], marks=1,
        figure=P.fig("1.2a", "A farmer under RURAL, an arrow pointing right to a city skyline under URBAN.")),
    m1("1.2.2", "A physical push factor contributing to the migration of people is …", ["Famine", "Unemployment", "Drought", "Poverty"], 2,
       ["Physical means nature.", "Not social or economic."]),
    m1("1.2.3", "Consequences of this type of migration is … (i) rural depopulation (ii) urban depopulation (iii) increased urbanisation "
                "(iv) decreased urbanisation", ["(i) and (iii)", "(i) and (iv)", "(ii) and (iii)", "(ii) and (iv)"], 0,
       ["People leave the farms.", "And go to the cities."]),
    m1("1.2.4", "Political migration occurs because of …", ["famine.", "soil erosion.", "war or conflict.", "desertification."], 2,
       ["Political: the soldiers in the sketch.", "Not nature."],
       figure=P.fig("1.2b", "HOME COUNTRY with soldiers, POLITICAL MIGRANTS carrying bundles, an arrow to a NEIGHBOURING COUNTRY with a "
                            "family at a REFUGEES camp.")),
    m1("1.2.5", "The sketch shows … migration which is … (i) seasonal (ii) international (iii) forced (iv) voluntary",
       ["(i) and (iii)", "(ii) and (iii)", "(ii) and (iv)", "(i) and (iv)"], 1,
       ["They cross into a neighbouring country.", "They flee war."]),
    m1("1.2.6", "The primary purpose of a refugee camp is to provide … for refugees.", ["permanent housing",
       "temporary shelter and basic services", "job training and educational programmes", "legal citizenship"], 1,
       ["A camp is not a home for ever.", "Shelter and basics."]),
    m1("1.2.7", "When a South African legally emigrates to Australia, it is usually … and results in the loss of … in South Africa. "
                "(i) temporary (ii) permanent (iii) skilled professionals (iv) unskilled labourers",
       ["(ii) and (iv)", "(i) and (iii)", "(ii) and (iii)", "(i) and (iv)"], 2,
       ["Emigrating means leaving for good.", "The 'brain drain'."],
       figure=P.fig("1.2c", "A map of South Africa, an aeroplane flying to a map of Australia.")),
    m1("1.2.8", "A significant push factor for South Africans emigrating to Australia is …",
       ["A high quality of life in Australia", "Crime rates and safety concerns", "A high quality of life in South Africa",
        "The favourable exchange rate with the Australian dollar"], 1,
       ["A push factor is in the home country.", "Something bad at home."])]
q13 = [
    answer("1.3.1", "According to the population pyramid, which age group makes up the largest proportion of the total population?", 1,
           ["50-54", "0-4", "25-29", "85-89"], ["Find the widest bars.", "Read the age on the left."]),
    stmt("1.3.2", "Provide TWO pieces of evidence from the population pyramid that show a declining population.", 2,
         ["A narrowing base", "A top-heavy (inverted) shape", "A significant bulge in the upper-middle age groups"],
         ["A wide base", "A sharp triangle shape", "More children than adults"],
         ["Compare the bottom of the pyramid with the middle.", "Fewer babies."], 1),
    work("1.3.3", "Calculate the natural increase of the country's population (birth rate 0,72; death rate 6,9).", 2,
         ["Natural increase = birth rate − death rate\n= 0,72 − 6,9 = −6,18", "Natural increase = death rate − birth rate\n= 6,9 − 0,72 = 6,18",
          "Natural increase = birth rate + death rate\n= 0,72 + 6,9 = 7,62", "Natural increase = birth rate ÷ death rate\n= 0,72 ÷ 6,9 = 0,10"],
         ["Births minus deaths.", "More deaths than births gives a negative number."]),
    stmt("1.3.4", "Why is South Korea's life expectancy considered typical for an economically well-developed country?", 2,
         ["Access to essential medical services", "Advanced medical technology", "High standards of living", "High levels of education",
          "Nutrition and food security"],
         ["High birth rates", "Poor health care", "Low incomes"], ["Why do people live long?", "Health, wealth, education."], 1),
    stmt("1.3.5", "In a paragraph of approximately EIGHT lines, explain how South Korea's aging population will affect its future economy.", 8,
         ["The labour force shrinks because the working-age group (15-64) is declining.",
          "The dependency ratio rises sharply as the elderly increase relative to the working population.",
          "Demand for healthcare increases, which costs a lot of money.",
          "Growth slows because fewer people consume and spend money.", "Fewer people in the labour force means less tax revenue."],
         ["More young workers will join the labour force.", "Healthcare costs will fall.", "Tax revenue will increase."],
         ["Fewer workers, more elderly.", "Link the ageing to money."], 2)]
GLOBAL = ("The global population reached 8 billion people in 2022. This growing number is putting pressure on global resources and "
          "negatively impacting the environment. It's projected that by 2050, the global population will be 9,7 billion. At this time, "
          "Africa's population will reach close to 2.5 billion. This will mean that more than 25 percent of the world's population will "
          "be African.")
q14 = [
    stmt("1.4.1", "Define the term population growth.", 2,
         ["The increase in the total number of people within a given area over time.",
          "The change in the number of people living in an area."],
         ["The movement of people from rural to urban areas.", "The number of deaths per 1 000 people.",
          "The number of people per km².", "The number of babies born in a year."],
         ["Growth: getting bigger.", "The number of people."], 2),
    m1("1.4.2(a)", "According to the cartoon, what global population number does the baby represent?", ["8 billion", "9,7 billion",
       "2,5 billion", "25 percent"], 0, ["Read the banner.", "#8 BILLION."]),
    pick("1.4.2(b)", "Quote from the extract to prove that population has negative impacts on the environment.", sentences(GLOBAL), [1],
         ["Find 'environment'.", "Global resources."], 1),
    m1("1.4.3", "Identify the projected (expected) global population for 2050 from the extract.", ["9,7 billion", "8 billion",
       "2,5 billion", "25 billion"], 0, ["By 2050 …", "Read the second paragraph."]),
    stmt("1.4.4", "Describe other negative environmental impacts associated with population increase in Africa, beside those mentioned in "
                  "question 1.4.2(b) above.", 4,
         ["Deforestation", "Loss of biodiversity", "Soil degradation and erosion", "Increased pollution", "Increased desertification"],
         ["More rainfall everywhere", "More wetlands", "Cleaner rivers"], ["More people need more land.", "Forests, soil, wildlife."], 2),
    stmt("1.4.5", "Suggest THREE strategies to manage population growth in Africa.", 6,
         ["Improve education.", "Empower girls and women (gender equality).", "Increase access to contraception and family planning.",
          "Run awareness campaigns and sex education in schools.", "Pass laws against early and child marriage."],
         ["Ban education for girls.", "Encourage early marriage.", "Give incentives for large families."],
         ["Education and family planning.", "Women's rights."], 2)]
XENO = ("Due to its middle-income status, stable democratic institutions and comparatively industrialised economy, South Africa hosts the "
        "largest number of immigrants on the African continent. According to official estimates, the country is home to about 2.9 million "
        "immigrants. However, this number is thought to be an underestimate because of the presence of large numbers of unauthorised "
        "migrants, particularly from neighboring countries.\nBut across South Africa, low-income foreign nationals encounter xenophobia which "
        "leaves them in a state of constant fear and uncertainty. People migrate to South Africa for a variety of reasons but are primarily "
        "driven by the perceived (apparent) opportunities the country offers compared to the rest of the continent. Political disorder, "
        "economic instability and a history of human rights abuses and armed conflict are cited as reasons foreigners leave their home "
        "country. This helps explain why they endure (tolerate) the mistreatment and victimization once they arrive in South Africa.")
q15 = [
    m1("1.5.1", "According to the graph, how many foreign-born citizens were living in South Africa in 2022?",
       ["2,42 million", "2,18 million", "2,9 million", "0,84 million"], 0, ["Read the 2022 bar.", "The tallest bar."]),
    stmt("1.5.2", "Refer to the extract and identify TWO pull factors that attract migrants to South Africa.", 2,
         ["Middle-income status", "Stable democratic institutions", "An industrialised economy", "Economic opportunities"],
         ["Political disorder", "Armed conflict", "Human rights abuses"], ["What draws people to South Africa?", "Read the first sentence."],
         1),
    stmt("1.5.3", "Why do official estimates and the actual number of migrants living in South Africa show a difference?", 2,
         ["There is a large number of unauthorised migrants.", "Migrants may not be documented or registered."],
         ["All migrants are counted at the border.", "Migrants leave every year.", "Official estimates count tourists as well."],
         ["Read the end of the first paragraph.", "Who is not counted?"], 2),
    stmt("1.5.4", "Explain why many low-income foreign nationals that live in a constant state of fear and uncertainty in South Africa do not "
                  "return to their home countries.", 4,
         ["Returning home could expose them to even greater danger or hardship.",
          "Political persecution and armed conflict at home make it too dangerous to return.",
          "Economic instability at home means their options there are limited.",
          "Their lives would be in danger from human rights abuses if they returned."],
         ["Their home countries are richer than South Africa.", "They are welcomed back with jobs.", "South Africa forbids them to leave."],
         ["The push factors at home.", "Why is home not an option?"], 2),
    stmt("1.5.5", "State reasons why some South Africans 'mistreat and victimise' foreign nationals.", 6,
         ["Perceived competition for jobs.", "Competition for limited resources.", "Foreigners are an easy target to blame for problems.",
          "Foreigners are associated with crime.", "Pressure on strained government services."],
         ["Foreigners bring more jobs for locals.", "South Africans have too many resources.", "Foreigners pay all the taxes."],
         ["Jobs and resources.", "Blame."], 2)]

# ---- QUESTION 2: WATER RESOURCES, the question paper pages 10-14 and the memo pages 5-8 ----
q21 = [
    fac("2.1.1", "South Africa's low average annual rainfall.", 0, ["Rain is nature.", "Not people or money."]),
    fac("2.1.2", "Increased demand for water because more people are living in urban areas.", 1, ["People and where they live.",
                                                                                                  "Not nature."]),
    fac("2.1.3", "Alien vegetation that reduces stream flow.", 0, ["Plants.", "Nature."]),
    fac("2.1.4", "Low household income leading to the inability for many South Africans to pay for water.", 2, ["Income is money.",
                                                                                                                 "Paying."]),
    fac("2.1.5", "Climate change causing rising temperatures and more droughts.", 0, ["Temperature and drought.", "Nature."]),
    fac("2.1.6", "Corruption and theft of money destined for water purification plants.", 2, ["Money stolen.", "Funds."]),
    fac("2.1.7", "Increased number of people using groundwater causing the water table to drop.", 1, ["People using water.", "Society."]),
    fac("2.1.8", "Uneven distribution of rainfall in South Africa.", 0, ["Rainfall.", "Nature."])]
q22 = [
    m1("2.2.1", "… is the removal of salt from sea water to make it safe and usable for human consumption.", ["purification",
       "desalination", "distillation", "deionization"], 1, ["De-salt.", "Sea water."]),
    m1("2.2.2", "The process whereby water in dams/lakes/rivers/sea changes into gas is …", ["condensation", "precipitation", "evaporation",
       "transpiration"], 2, ["Liquid to gas.", "From open water."]),
    m1("2.2.3", "Clearing or removal of trees from the surface causes …", ["more infiltration", "less floods", "more run-off", "less erosion"],
       2, ["Roots hold soil and slow water.", "Without trees, water runs off."]),
    m1("2.2.4", "The process of transferring water from one river basin to another through tunnels and canals is …",
       ["spot mart transfer", "piping", "inter-basin transfer", "water exchange"], 2, ["Between basins.", "Inter means between."]),
    m1("2.2.5", "The scarcity and poor quality of water in South Africa is affected by … and … (i) silted dams due to soil erosion which "
                "reduces dam capacity (ii) enough rainfall that fills up rivers and dams (iii) industry and mining activities which pollute "
                "water resulting in poor quality (iv) vendors selling contaminated water and increasing the cost of water",
       ["(ii) and (iv)", "(i) and (iii)", "(iv) and (iii)", "(i) and (ii)"], 1, ["Enough rain is not a problem.", "Silt and pollution."]),
    m1("2.2.6", "Floods occur because of …", ["more infiltration during rainy days",
       "deforestation that increases soil erosion, reducing infiltration and increasing runoff that overfills the rivers",
       "well managed solid waste in informal settlements", "proper management of drains by municipalities to make sure that there are no "
                                                             "blockages"], 1,
       ["Which one makes more water run off?", "Good management prevents floods."]),
    m1("2.2.7", "People in areas without clean and safe water are likely to …", ["suffer illnesses and diseases", "ignore water crisis",
       "use grey water over and over again", "regard this poor access as just part of their lives"], 0, ["Dirty water.", "Cholera."])]
JHB = ("Through the process of decentralising the water supply, the South African government has made it the responsibility of local "
       "authorities (municipalities) to get water to the consumer.\nThe City of Johannesburg is currently facing a water crisis. As a result "
       "there is 'watershedding'. This is a planned process of reducing water supply to different areas of the city in order to manage "
       "demand and prevent the complete depletion of water resources.\nThe inability of the municipality to supply sufficient water to the "
       "residents of Johannesburg has resulted from decades of neglecting water infrastructure. In 2023, the city was loosing 48,2% of its "
       "water to leakage and theft. In addition, mismanagement of municipal funds has played a significant role in the current water crisis "
       "that the city faces.\nMillions of people have been affected by the collapse of the Johannesburg water system. The crisis is also "
       "impacting industry, as many of the region's mines and factories cannot operate without water.")
q23 = [
    term("2.3.1", "Who is responsible for providing water to the consumers in Johannesburg?",
         ["local authorities", "municipality", "the municipality", "local municipality", "city of johannesburg municipality", "local authority",
          "municipalities"], ["Read the first paragraph.", "Decentralised to …"]),
    stmt("2.3.2", "What are the TWO aims of 'watershedding'?", 2,
         ["To manage the demand for water.", "To prevent the complete depletion of water resources."],
         ["To sell more water.", "To fill the dams faster.", "To stop rain."], ["Read the second paragraph.", "In order to …"], 1),
    stmt("2.3.3", "According to the extract, in what ways has the municipality contributed to the water crisis that Johannesburg faces?", 2,
         ["Neglecting water infrastructure", "Leakage and theft", "Mismanagement of municipal funds"],
         ["Too much rainfall", "Building too many dams", "Mines using no water"], ["Read the third paragraph.", "Neglect and money."], 1),
    stmt("2.3.4", "How can water conservation campaigns be used to address the water crisis in Johannesburg?", 4,
         ["Encourage residents to report leaks.", "Encourage residents to use less water.", "Promote the installation of rainwater harvesting "
                                                                                            "systems.",
          "Promote water-efficient appliances."],
         ["Encourage people to water gardens at midday.", "Tell residents to ignore leaks.", "Promote longer showers."],
         ["Saving and reporting.", "What can each household do?"], 2),
    stmt("2.3.5", "Explain how the water crisis ('watershedding') is negatively impacting the economy of Johannesburg.", 6,
         ["Disrupted businesses reduce output and lose money.", "Manufacturing slowdowns can lead to job losses.",
          "Mines face delays that affect production.", "Investor and tourist confidence drops, reducing foreign investment.",
          "Water-saving technology and alternative water sources are expensive."],
         ["Factories produce more without water.", "More tourists visit the city.", "Property values rise."],
         ["Businesses, jobs, investors.", "Explain how, not just what."], 2)]
FBW = ("The Free Basic Water (FBW) project in South Africa is a government policy that provides a minimum amount of safe drinking water "
       "(6000 liters per month per household) to poor households at no cost.\nThe FBW policy has improved water service delivery, with 86% of "
       "households in South Africa receiving safe water. This is a significant improvement from the apartheid era, when only 66% of urban "
       "households and 39% of rural households received safe water.\nThe FBW policy has been difficult to implement in rural areas, and some "
       "municipalities have struggled with implementation.")
q24 = [
    m1("2.4.1", "How much free water is allocated per month to qualifying households?", ["6 000 litres", "600 litres", "86 litres",
       "60 000 litres"], 0, ["Read the first paragraph.", "Per month per household."]),
    stmt("2.4.2", "Who is the key target group of the project?", 2, ["Poor households"],
         ["Rich households", "Factories", "Farmers with dams", "Tourists"], ["At no cost to whom?", "Read the first paragraph."], 2),
    stmt("2.4.3", "From the extract, identify TWO successes that the project has achieved.", 2,
         ["Improved water service delivery", "More urban households receive safe water", "More rural households receive safe water"],
         ["Fewer households receive water", "It is easy to implement in rural areas", "Water is now sold to poor households"],
         ["Read the second paragraph.", "86%."], 1),
    stmt("2.4.4", "Why has the policy been difficult to implement in rural areas?", 4,
         ["Limited or outdated water supply infrastructure in rural areas.", "Isolated rural settlements make it logistically challenging.",
          "It is expensive: there is a lack of funding.", "Weak local governance, management and corruption."],
         ["Rural areas have too many pipelines.", "Rural people need no water.", "Rural municipalities have too much money."],
         ["Distance, pipes, money, management.", "Why is the countryside harder?"], 2),
    stmt("2.4.5", "Explain the role the THREE non-traditional water sources (illustrated in the sketch) can play in increasing the supply of water.",
         6, ["Desalination removes salt from seawater to give fresh water for drinking, irrigation and industry.",
             "Recycled wastewater is treated to remove contaminants so it can be reused.",
             "Rainwater harvesting collects and stores rainwater from rooftops for later use."],
         ["Desalination adds salt to river water.", "Recycled wastewater is poured into the sea.", "Rainwater harvesting drains rain away."],
         ["Sea, used water, rain.", "Explain each one."], 2)]
FLOOD = ("The multiple cold fronts that affected the region on the southwest tip of Africa (July 2024) brought record high rainfall in some "
         "parts of the province.\nThe series of cold fronts led to extremely cold conditions, gusty winds, heavy snowfall and torrential rain. "
         "At least 4,500 people were forced out of their homes and approximately 15,000 structures were damaged.\nAlthough many people were "
         "affected, the majority of the people left homeless were from the impoverished (poor) informal settlements where metal and wooden "
         "shacks are especially vulnerable to strong wind and flooding.")
q25 = [
    stmt("2.5.1", "What is a flood?", 2,
         ["A natural or man-made event in which water overflows onto normally dry land.", "The overflow of water onto land that is normally dry."],
         ["A long period with no rain.", "A strong wind over the sea.", "The melting of a glacier only.", "Water evaporating from a dam."],
         ["Water where it is usually dry.", "Overflow."], 2),
    stmt("2.5.2", "From the extract, identify ONE negative impact of the floods.", 1,
         ["4 500 people were forced out of their homes.", "15 000 structures were damaged.", "People were left homeless."],
         ["Record high rainfall filled the dams.", "Snow fell on the mountains.", "Cold fronts reached the Cape."],
         ["Read the second paragraph.", "People and buildings."], 1),
    stmt("2.5.3", "Why are informal settlements more at risk to adverse (bad) weather conditions?", 4,
         ["They have inadequate drainage and storm-water management.", "They are often built on floodplains, riverbanks or low-lying areas.",
          "Their structures are vulnerable: weak building materials.", "People there cannot afford protective measures."],
         ["They are built of strong bricks.", "They are on high ground.", "They have the best drainage in the city."],
         ["Where are they built, and with what?", "Drainage."], 2),
    stmt("2.5.4", "In a paragraph of approximately EIGHT lines, suggest strategies to minimise (reduce) the impacts of floods in informal "
                  "settlements.", 8,
         ["Establish and maintain storm-water drainage.", "Keep drainage channels free of waste and blockages.",
          "Provide stronger building materials.", "Set up early flood warning systems.", "Run community flood preparedness campaigns.",
          "Relocate people from flood-prone areas."],
         ["Build more shacks on the riverbanks.", "Block the drains with rubbish."],
         ["Drains, buildings, warnings.", "What can a community do before the rain?"], 2)]

# ---- SECTION B, QUESTION 3 (the parts that do not read the maps), the question paper pages 15-18 and the memo pages 8-9 ----
q31 = [
    m1("3.1.1", "Caledon is situated in … province", ["KwaZulu-Natal", "Eastern Cape", "Northern Cape", "Western Cape"], 3,
       ["Look at the map of South Africa.", "In the south-west."]),
    m1("3.1.2", "The number 19 on the map's reference (map index 3419) represents …", ["Seconds", "Minutes",
       "Degrees East of the prime meridian", "Degrees South of the equator"], 2, ["Caledon is at 19° 25' E.", "The first two digits are "
                                                                                                           "the latitude."]),
    work("3.1.5", "On the orthophoto map (1 : 10 000) the breadth of the hospital is 1,3 cm and its length is 3 cm. Calculate the area of the "
                  "hospital in m².", 3,
         ["Breadth: 1,3 × 100 = 130 m; length: 3 × 100 = 300 m\nArea = 130 m × 300 m = 39 000 m²",
          "Breadth: 1,3 × 500 = 650 m; length: 3 × 500 = 1 500 m\nArea = 650 m × 1 500 m = 975 000 m²",
          "Breadth: 1,3 × 100 = 130 m; length: 3 × 100 = 300 m\nArea = 2 × (130 m + 300 m) = 860 m²",
          "Breadth: 1,3 × 10 = 13 m; length: 3 × 10 = 30 m\nArea = 13 m × 30 m = 390 m²"],
         ["1 cm on a 1 : 10 000 map is 100 m.", "Area = length × breadth."]),
    stmt("3.1.6", "Why does the hospital on the orthophoto map appear bigger than the hospital on the topographical map?", 2,
         ["The scale of the orthophoto map is (five times) larger.", "The scale of the topographical map is (five times) smaller."],
         ["The orthophoto was taken from higher up.", "The hospital was enlarged after the topographical map was made.",
          "The orthophoto map has a smaller scale."], ["1 : 10 000 against 1 : 50 000.", "A larger scale shows more detail."], 2)]
q32 = [
    stmt("3.2.5", "Explain how farm dams have positive economic impacts on the farmers.", 4,
         ["A reliable and consistent water supply for irrigation.", "Improved crop yields.", "A reliable source of water for livestock.",
          "Extended growing seasons."],
         ["Dams cause droughts on the farm.", "Dams make crops wilt.", "Dams stop the farmer from irrigating."],
         ["Water stored for dry months.", "Crops and animals."], 2)]
q33 = [
    term("3.3.1(A)", "State the GIS component labelled A.", ["hardware"], ["The computer.", "Physical equipment."]),
    term("3.3.1(B)", "State the GIS component labelled B.", ["methods", "method", "procedures"], ["How the work is done.",
                                                                                                "Not people, data or software."]),
    mcq("3.3.2", "Which data (X or Y) is attribute data?", ["X", "Y"], 1, ["Attribute data describes a feature.", "Name and area."], marks=1,
        figure=P.fig("3.3b", "DATA X: co-ordinates, latitude 34 S, longitude 29 E; DATA Y: name Caledon Cemetery, total area 5 941 m²; "
                             "beside them stacked data layers and an aerial photograph of the walled cemetery.")),
    stmt("3.3.3", "Give a reason for your answer in QUESTION 3.3.2 above.", 2,
         ["Y describes the cemetery's characteristics (its name and total area), not its position."],
         ["Y gives the cemetery's latitude and longitude.", "X describes the cemetery's name.", "Y is a photograph.",
          "Attribute data is always a coordinate."], ["What does each box tell you?", "Spatial data is where; attribute data is what."], 2,
         after=["3.3.2"]),
    stmt("3.3.4", "Why is the photograph an example of raster data?", 2,
         ["It consists of a grid of pixels (cells)."],
         ["It is made of points, lines and polygons.", "It is a table of names.", "It has coordinates written on it.",
          "It was drawn by hand."], ["Zoom in on a photo.", "Squares."], 2),
    m1("3.3.5", "Choose the symbol for a grave as it would be shown on a topographical map.", ["† (a cross)", "▲ (a triangle)",
       "● (a dot)", "⌂ (a house)"], 0, ["Topographical maps mark graves with a cross.", "A church has a cross too."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Provincial population", "marks": 7,
     "lead": "Refer to the graph and table in Fig 1.1, which show population statistics in the provinces of South Africa. Choose Y or Z.",
     "figure": P.fig("1.1", "Provincial population as a percentage of South Africa's total: Northern Cape 2,2; Free State 4,9; North West 6,9; "
                            "Mpumalanga 7,9; Limpopo 9,9; Eastern Cape 11,1; Western Cape 11,8; KZN 19,1; Gauteng 26,3. Table: Western Cape "
                            "7 113 776 people, 129 462 km², 54,9 per km²; Gauteng 15 099 422, 18 178 km², 831; KwaZulu-Natal 12 423 907, "
                            "94 361 km², 132; Northern Cape 1 355 946, 372 889 km², 3,64."), "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Migration", "marks": 8,
     "lead": "Various options are provided as possible answers to the following questions. Refer to the sketches.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "South Korea's demographics", "marks": 15,
     "lead": "Refer to the source, Fig 1.3, based on South Korea's demographics.",
     "figure": P.fig("1.3", "Population pyramid for South Korea (2023), male and female in millions: narrow at 0-4, widest at 45-59 (about "
                            "2,2 million each), narrowing above. Birth rate 0,72; death rate 6,9; life expectancy over 83 years; 20% of the "
                            "population is 65 and older."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Population growth", "marks": 15,
     "lead": "Refer to the infographic, Fig 1.4, on population growth.\n" + GLOBAL,
     "figure": P.fig("1.4", "A cartoon of a stork labelled 'global resources' straining to carry a crying baby with a '#8 BILLION' banner; a "
                            "map of the eight countries expected to account for over half of the population growth to 2050: Egypt, Pakistan, "
                            "India, Nigeria, Ethiopia, the DRC, Tanzania and the Philippines."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Migration and xenophobia", "marks": 15,
     "lead": "Refer to the graph and extract, Fig 1.5, on migration and xenophobia.\nFOREIGNERS FACE CHALLENGES IN AFRICA'S TOP IMMIGRATION "
             "DESTINATION\n" + XENO,
     "figure": P.fig("1.5", "Number (millions) of foreign-born citizens in South Africa: 0,84 in 1996, 1,03 in 2001, 2,18 in 2011, 2,42 in "
                            "2022."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Water availability", "marks": 8,
     "lead": "Classify the factors influencing water availability in South Africa as physical, social or economic.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Multiple choice", "marks": 7,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Watershedding", "marks": 15,
     "lead": "Read the case study, Fig 2.3, on the role of municipalities in water provision in South Africa.\nWATERSHEDDING IN THE CITY OF "
             "JOHANNESBURG\n" + JHB, "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Free basic water", "marks": 15,
     "lead": "Refer to the extract and sketch, Fig 2.4, on South Africa's ability to provide free basic water and non-traditional water "
             "sources.\nSOUTH AFRICA'S FREE BASIC WATER POLICY\n" + FBW,
     "figure": P.fig("2.4", "Non-traditional water sources: rainwater harvesting tanks beside houses under rain clouds, recycled wastewater "
                            "from buildings, and a desalination plant by the sea feeding a tap."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Floods", "marks": 15,
     "lead": "Refer to the extract and photograph, Fig 2.5, on floods in the Western Cape.\nFLOODS AFFECT THE WESTERN CAPE\n" + FLOOD,
     "figure": P.fig("2.5", "Flooding in an informal settlement: metal shacks standing in brown floodwater with rubbish floating in it."),
     "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Map skills and calculations", "marks": 7,
     "lead": "GENERAL INFORMATION ON CALEDON. Co-ordinates: 34° 13' S; 19° 25' E. A 1 : 50 000 topographical map and a 1 : 10 000 orthophoto "
             "map of Caledon are used in the exam room.", "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Map interpretation", "marks": 4, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Geographical information systems", "marks": 8,
     "lead": "Refer to the sketch of GIS components, and to the sketch and photograph of the cemetery in block E3 of the topographical map. "
             "DATA X: co-ordinates, latitude 34 S, longitude 29 E. DATA Y: name, Caledon Cemetery; total area 5 941 m².",
     "figure": P.fig("3.3a", "GIS at the centre of a ring: A a computer, software, B a set of tools and charts, people, and data layers."),
     "items": q33}]

P.finish(missions,
         {"subject": "Geography", "title": "Geography P2", "sitting": "November 2024", "total_marks": 139, "time": "3 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "3.1", "kind": "missing_resource", "detail": "SECTION B reads the 1 : 50 000 topographical map and the 1 : 10 000 orthophoto of "
                                                             "Caledon handed out in the exam room; they are not in the download. 3.1.3, 3.1.4 and "
                                                             "3.2.1-3.2.4 (11 marks) wait for the maps; the paper totals 139."},
          {"n": "2.2.3", "kind": "memo_issue", "detail": "The memo gives D (less erosion) for what clearing trees causes. Removing trees causes "
                                                         "more run-off and more erosion; the right option is C (more run-off). For Murci to "
                                                         "confirm."},
          {"n": "3.1.2", "kind": "memo_issue", "detail": "The memo gives B (minutes) for the 19 in map index 3419. The 34 and 19 are whole "
                                                         "degrees: 19 is degrees east of the prime meridian (Caledon 19° 25' E), option C. For "
                                                         "Murci to confirm."},
          {"n": "3.3.2", "kind": "memo_issue", "detail": "The paper asks which data is ATTRIBUTE data; the memo answers 'spatial' and gives "
                                                         "the co-ordinates as its reason (it answered which is spatial: X). Attribute data is "
                                                         "Y (name and area); 3.3.3's reason follows. For Murci to confirm."},
          {"n": "1.3.4", "kind": "low_confidence", "detail": "The paper prints 1.3.4 (2x1) (2); the memo gives (2x2) (4). The paper's 2 is used "
                                                             "(it totals 1.3 to 15)."}],
         {"1": 60, "2": 60, "3": 19}, 139,
         {"3.3.3": ["3.3.2"]}, "Section A whole and the parts of Section B that do not read the maps")
