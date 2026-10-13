"""Grade 10 Geography P2 November 2024 (North West Department of Education, provincial assessment): SECTION A whole (Questions 1 and
2, 120 marks) and the parts of SECTION B (Question 3) that do not read the maps (10 of its 30 marks), hand-transcribed into the
catalogue format, then run through `ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and
the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment,
the question paper PDF (English, 15 pages, text layer; its pyramid, photographs and cartoon are images) and the marking guidelines PDF
(English, 11 pages).

  python tools/ingest/transcribe_g10_geo_p2_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-geo-p2-2024-11-nw/11-November-24-NW-GR10-S2-GEOGRAPHY-QP-P2-ENG.pdf" "uploads/provincial/g10-geo-p2-2024-11-nw/11-November-24-NW-GR10-S2-GEOGRAPHY-MG-P2-ENG.pdf" --id g10-geo-p2-2024-11-nw --from-json

SECTION B reads a 1 : 50 000 topographic map 3126DD QUEENSTOWN and a 1 : 10 000 orthophoto map 3126DD1 NOOITGEDACHT handed out in the
exam room: not in the download. As transcribe_g10_geo_p1_2024_11_nw.py, its 20 marks that read the maps (3.1.2, 3.1.4, 3.1.5, 3.2.1,
3.2.2, 3.2.3(a)(b), 3.2.4-3.2.6, 3.3.3) wait for the maps; the rest plays. The paper totals what is playable, 130.

The Geography rulings, as transcribe_g10_geo_p1_2024_11_nw.py; the one calculation (1.3.4) is four workings. Figure boxes in PDF points
(page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-geo-p2-2024-11-nw", 595.32, 841.92, {
    "1.3": [5, 92, 113, 502, 424], "1.4": [6, 102, 136, 504, 386], "2.3": [10, 97, 160, 506, 405], "2.4": [11, 92, 228, 502, 559]}, start=7)
work, answer, stmt, mcq, term = P.work, P.answer, P.stmt, P.mcq, P.term
two = lambda n, q, a_opt, b_opt, a, clues, marks=1: mcq(n, q, [a_opt, b_opt], a, clues, marks=marks)

# ---- SECTION A, QUESTION 1: POPULATION, the question paper pages 3-7 and the memo pages 2-5 ----
COLB = ["Demographics", "Baby boom", "Population distribution", "Exiles", "Refugee", "'Brain drain'", "Population density", "Ecumene", "Genocide"]
q11 = [
    {"t": "match", "n": "1.1", "marks": 8, "q": "Choose the term/concept in COLUMN B that matches the statement in COLUMN A.",
     "clues": ["Density is people per square kilometre; distribution is where they live.", "Exiles cannot return home."],
     "left": ["1.1.1 The number of people per square kilometre", "1.1.2 Where people live, or how they are spread around the world",
              "1.1.3 When the country loses professional people due to emigration",
              "1.1.4 The deliberate killing of people from a certain ethnic group or nation",
              "1.1.5 A political migrant who is forced to migrate to another country", "1.1.6 Period during which a large number of babies is born",
              "1.1.7 Political migrants who cannot return home", "1.1.8 The study of population statistics"],
     "right": COLB, "a": [6, 2, 5, 8, 4, 1, 3, 0], "heads": ["COLUMN A", "COLUMN B (A–I)"]}]
q12 = [
    two("1.2.1", "(Birth rate/Fertility rate) is the average number of children born to each woman in her child-bearing years.", "Birth rate",
        "Fertility rate", 1, ["Per woman, not per 1 000 people.", "Fertile years."]),
    two("1.2.2", "Women who are more educated tend to bear (fewer/more) children.", "fewer", "more", 0,
        ["Education often means careers first.", "Family planning."]),
    two("1.2.3", "(Polygamy/Polyandry) is the practice of having more than one wife at the same time.", "Polygamy", "Polyandry", 0,
        ["Polyandry is more than one husband.", "Wives."]),
    two("1.2.4", "Lack of access to medical care (increases/decreases) the death rate.", "increases", "decreases", 0,
        ["Without care, more people die.", "Death rate up or down?"]),
    two("1.2.5", "The literacy rate is (higher/lower) in More Economically Developed Countries than in Less Economically Developed Countries.",
        "higher", "lower", 0, ["MEDCs have more schools.", "More people can read."]),
    two("1.2.6", "(Contraception/Vasectomy) is a permanent method of prevention.", "Contraception", "Vasectomy", 1,
        ["Permanent: an operation.", "Contraception can be stopped."]),
    two("1.2.7", "(Infant mortality rate/Death rate) refers to the number of children who die before they reach the age of five.",
        "Infant mortality rate", "Death rate", 0, ["Young children only.", "Infant."])]
q13 = [
    stmt("1.3.1", "What is a population pyramid?", 2,
         ["A graph showing the population structure of a country by age groups and gender.",
          "A visual way of showing a population's age and sex structure."],
         ["A map showing where people live.", "A pyramid-shaped building for many people.", "A graph of rainfall over a year.",
          "A list of a country's cities."],
         ["It shows age and gender.", "Bars on either side of a centre line."], 2),
    two("1.3.2", "The type of population pyramid shown above is (progressive/regressive).", "progressive", "regressive", 1,
        ["Is the base wide or narrow?", "A narrow base means few births."]),
    two("1.3.3", "The shape of this population pyramid indicates (low/high) infant mortality rate and death rate.", "low", "high", 0,
        ["Many people reach old age.", "The top is wide."]),
    work("1.3.4", "Calculate the total percentage of females aged between 0 and 14 years.", 2, [
        "1,6% + 1,9% + 2,1%\n= 5,6%",                                  # the memo
        "1,7% + 2,0% + 2,2%\n= 5,9%",                                  # the males' bars
        "1,7% + 2,0% + 2,2% + 1,6% + 1,9% + 2,1%\n= 11,5%",            # both sexes
        "1,6% + 1,9%\n= 3,5%"],                                        # 10-14 left out
        ["Which three age groups make up 0 to 14?", "Read the female (right) side."]),
    answer("1.3.5", "Which age group represents the largest portion of the population in 2023?", 2,
           ["50–54 years", "70–74 years", "45–49 years", "0–4 years"], ["Add the male and female bars of each group.", "Look for the widest bar."]),
    two("1.3.6(a)", "Which gender lives the longest in Japan?", "Males", "Females", 1, ["Compare the oldest bars.", "Which side is wider at the top?"]),
    stmt("1.3.6(b)", "Explain why this is the case.", 2,
         ["Women generally eat healthier and pay more attention to their health.",
          "Men are more likely to work in hazardous occupations, increasing their mortality.", "Women tend to choose better lifestyles."],
         ["Women do not get sick.", "Men live in a different country.", "Women are counted twice in the census."],
         ["Health, lifestyle, work.", "Why do more women reach old age?"], 2, after=["1.3.6(a)"]),
    stmt("1.3.7", "Demographers use population pyramids to calculate their countries' dependency ratio. Why is it important for the country to "
                  "know its dependency ratio?", 4,
         ["For planning and making decisions.", "To provide insights into family formation and housing needs.",
          "To know the relationship between the potential labour force and the rest of the population.",
          "To plan pensions, schools and health care for dependants."],
         ["To count the number of tourists.", "To decide the country's flag.", "To measure rainfall."],
         ["Dependants are the young and the old.", "Who supports them?"], 2)]
q14 = [
    stmt("1.4.1", "What evidence in the source indicates that India is overpopulated?", 2,
         ["Overcrowding at the railway station in the photograph", "'The second most populous country of the world'",
          "A population of 1 210 193 422"],
         ["Empty trains", "Quiet shopping malls", "Few people at the airport"], ["Look at the photograph and the numbers.", "Crowds."], 1),
    answer("1.4.2", "According to the extract, what was the total population of India in 2011?", 1,
           ["1 210 193 422", "1 000 000 000", "121 019 342", "2 025 000 000"], ["Read the second paragraph.", "The census figure."]),
    stmt("1.4.3", "Describe TWO possible social issues that are leading to overpopulation in India.", 4,
         ["Getting married at a young age.", "Marriage is a sacred obligation and a universal practice.",
          "Lagging behind in the use of contraceptives and birth control.", "A high illiteracy rate.", "Poor, impoverished families."],
         ["Too many people use contraceptives.", "Most people marry very late.", "Everyone is highly educated."],
         ["Social issues are about people's customs and choices.", "Marriage, education, contraception."], 2),
    stmt("1.4.4", "In a paragraph of approximately EIGHT lines, explain the negative effects of overpopulation in a country and suggest steps that "
         "need to be taken in order to bring population under control.", 8,
         ["Resources are overexploited.", "Unemployment rates increase.", "Municipal services break down.", "Practise birth control and make "
                                                                                                             "contraceptives available.",
          "Educate people about the problems of overpopulation.", "Encourage family planning and delayed marriage."],
         ["Overpopulation creates more farmland.", "Ban all schools."], ["Effects first, then steps to control it.", "Resources, services, planning."],
         2)]
q15 = [
    stmt("1.5.1", "Define the concept xenophobia.", 2,
         ["The fear, hatred or lack of acceptance of people from a different country.", "Dislike or fear of foreigners."],
         ["Love of travelling abroad.", "The study of population.", "Fear of heights.", "A disease spread by migrants."],
         ["Xeno means stranger.", "Phobia means fear."], 2),
    term("1.5.2", "What is the name of the commercial district that is located close to Alexandra?", ["sandton"],
         ["Read the second paragraph.", "Towering skyscrapers."]),
    term("1.5.3", "According to the extract, what is the meaning of the word Dudula?", ["push back", "drive back", "to push back",
                                                                                         "to drive back"],
         ["It is a Zulu word.", "Read the fourth paragraph."]),
    stmt("1.5.4", "Give the main aim of the two groups that are mentioned in the extract.", 1,
         ["To drive out undocumented African migrants from their communities."],
         ["To welcome more foreign traders.", "To build houses for migrants.", "To start new businesses in Sandton.", "To support xenophobic violence "
                                                                                                                      "abroad."],
         ["Read the last paragraph.", "Dudula means push back."], 1),
    stmt("1.5.5", "Why do people choose to move from their place of origin to go and stay in cities?", 4,
         ["More job opportunities.", "Higher wages.", "Better living conditions.", "Improved access to basic services.", "Better security."],
         ["Fewer jobs in cities.", "Lower wages in cities.", "No services in cities."], ["Pull factors of the city.", "Jobs, wages, services."], 2),
    stmt("1.5.6", "Explain THREE reasons for the outbreak of violence against foreign nationals in South Africa.", 6,
         ["South Africans blame foreigners for 'taking' their jobs, as they work for lower wages.",
          "South Africans blame foreigners for the high crime rate.", "South Africans believe foreigners increase competition for housing.",
          "Foreigners put more pressure on resources.", "A lack of trust of people from outside South Africa."],
         ["Foreigners bring more jobs for everyone.", "Foreigners lower the cost of housing.", "Foreigners reduce competition for resources."],
         ["Poverty drives the tension.", "Jobs, crime, housing, resources."], 2)]

# ---- QUESTION 2: WATER AND WATER RESOURCES, the question paper pages 8-12 and the memo pages 6-9 ----
q21 = [
    mcq("2.1.1", "The primary source of water in South Africa is …", ["rainfall.", "groundwater.", "desalination.", "recycling."], 0,
        ["Rivers and dams fill from it.", "It falls from the sky."], marks=1),
    mcq("2.1.2", "A physical factor that affects rainfall patterns in South Africa.", ["Topography", "Climate change", "Soil type", "Vegetation"], 0,
        ["Mountains force air to rise.", "Relief and height."], marks=1),
    mcq("2.1.3", "The … is the largest river in South Africa.", ["Orange River", "Vaal River", "Limpopo River", "Tugela River"], 0,
        ["It flows into the Atlantic.", "The Vaal is its tributary."], marks=1),
    mcq("2.1.4", "The sector which uses the most water in South Africa is the … sector.", ["agriculture", "industrial", "forestry", "mining"], 0,
        ["Irrigation.", "Farms."], marks=1),
    mcq("2.1.5", "A major challenge facing South Africa's water infrastructure.", ["Aging infrastructure", "Inadequate funding",
        "Lack of maintenance", "All of the above"], 3, ["Are all three true?", "Pipes, money and repairs."], marks=1),
    mcq("2.1.6", "The main purpose of water storage facilities in South Africa is to …", ["support irrigation.", "generate hydroelectric power.",
        "supply water during scarcity.", "provide drinking water."], 2, ["Dams store water for dry times.", "South Africa is water-scarce."],
        marks=1),
    mcq("2.1.7", "The province that receives the most rainfall in South Africa.", ["Western Cape", "Eastern Cape", "KwaZulu-Natal", "Mpumalanga"], 2,
        ["The east coast is wettest.", "Warm Agulhas current."], marks=1)]
WLIST = "Desalination; Water treatment; Water harvesting; Ocean currents; Grey water; Marine pollution; Water transfer; Water scarcity; Water conservation"
q22 = [
    term("2.2.1", "The practice of using water efficiently and reducing waste to minimise the amount of water used.", ["water conservation"],
         ["Saving water.", "Conserve."]),
    term("2.2.2", "Used water which is still clean.", ["grey water", "greywater"], ["From baths and washing.", "Not black water."]),
    term("2.2.3", "Moving water from one drainage basin to another.", ["water transfer", "inter-basin transfer"], ["The Lesotho Highlands scheme.",
                                                                                                                   "Moving water."]),
    term("2.2.4", "The lack of sufficient water to meet demand.", ["water scarcity"], ["Too little water.", "Scarce."]),
    term("2.2.5", "Removing contaminants and pollutants from water to make it safe for use.", ["water treatment"], ["At a treatment works.",
                                                                                                                    "Cleaning water."]),
    term("2.2.6", "A process of removing salt from seawater.", ["desalination"], ["De-salt.", "Coastal plants do it."]),
    term("2.2.7", "Collecting and storing rainwater for non-potable uses, such as irrigation or toilet flushing.", ["water harvesting",
                                                                                                                    "rainwater harvesting"],
         ["Tanks under the gutters.", "Harvesting rain."]),
    term("2.2.8", "Introduction of harmful materials into the water sources.", ["marine pollution", "water pollution"], ["Harmful materials.",
                                                                                                                         "Pollution."])]
q23 = [
    term("2.3.1", "Name the dam that is invaded by hyacinth weed.", ["hartbeespoort dam", "hartbeespoort", "harties"],
         ["Read the first line of the article.", "North-west of Johannesburg."]),
    stmt("2.3.2", "Give TWO main causes of pollution in this dam as mentioned in the article.", 2,
         ["Sewage", "Industrial chemicals", "Heavy metals", "Litter"], ["Fresh rainwater", "Fish", "Boats' sails"],
         ["Read the second paragraph.", "What flows in from the cities?"], 1),
    stmt("2.3.3", "How do pollutants promote growth of hyacinth weed?", 2,
         ["Nutrients in the pollutants act as perfect fertilisers for the weed.", "The pollutants add nitrates and phosphates that feed the weed."],
         ["Pollutants kill the weed.", "Pollutants cool the water.", "Pollutants make the water salty.", "Pollutants block sunlight."],
         ["Read the third paragraph.", "Fertiliser."], 2),
    stmt("2.3.4", "According to the article, how does the invasion of hyacinth weed impact negatively on the nearby communities?", 4,
         ["Businesses came to a standstill.", "People are about to lose their jobs in the tourism industry.", "Tourism in the town is affected."],
         ["More tourists visit the dam.", "Boat companies hire more workers.", "Fishing improves."],
         ["Read about Dion Mostert.", "Jobs and tourism."], 2),
    stmt("2.3.5", "Suggest ways in which water managers can reduce the negative impact of alien species on water availability in their area.", 6,
         ["Decrease the use of pesticides and fertilisers near rivers.", "Manage the dumping of industrial waste.",
          "Implement wastewater treatment.", "Run awareness campaigns.", "Test the water regularly."],
         ["Add more fertiliser to the dam.", "Allow sewage into the rivers.", "Plant more water hyacinth."],
         ["Cut what feeds the weed.", "Waste, treatment, awareness."], 2)]
q24 = [
    two("2.4.1", "Is water a renewable or non-renewable resource?", "renewable", "non-renewable", 0, ["The water cycle.", "It is replaced."]),
    stmt("2.4.2", "Name TWO ways in which water is used by people at their homes.", 2,
         ["Drinking", "Cooking", "Bathing", "Washing clothes and dishes", "Watering the garden"], ["Mining gold", "Generating electricity",
                                                                                                    "Irrigating large farms"],
         ["Think of a day at home.", "Kitchen, bathroom, garden."], 1),
    stmt("2.4.3", "Why is it difficult for the government to provide free basic water?", 2,
         ["In rural areas communities are small, spread out and far from dams.", "Informal settlements grow faster than services can be provided.",
          "Water provision takes time and costs money.", "Poor maintenance of the existing infrastructure."],
         ["There is too much water in South Africa.", "Nobody needs water at home.", "Water pipes cost nothing."],
         ["Distance, cost, growth.", "Infrastructure."], 2),
    stmt("2.4.4", "Describe THREE water-saving techniques that are depicted in the cartoon.", 6,
         ["Close taps when not using the water.", "Fix dripping taps and leaks.", "Take short showers instead of baths.",
          "Use a watering can instead of a hosepipe.", "Switch the water off while brushing your teeth."],
         ["Leave the tap running while brushing.", "Water the garden at noon with a hosepipe.", "Take long baths every day."],
         ["Look at each bubble in the cartoon.", "Taps, shower, watering can, toothbrush."], 2),
    stmt("2.4.5", "Suggest TWO government initiatives that can be used to secure South Africa's scarce water supply in the future.", 4,
         ["Build dams to store more water.", "Desalinate seawater in coastal settlements.", "Purify and recycle more waste water.",
          "Use groundwater from boreholes.", "Introduce water restrictions."],
         ["Remove all dams.", "Lower water prices to increase use.", "Stop treating waste water."],
         ["Store, desalinate, recycle.", "More supply, less waste."], 2)]
KH = ("Hundreds of people have abandoned their homes after heavy rains in Cape Town. Dozens of residents of RR section of Khayelitsha have taken "
      "refuge in local churches. Community leader Sihla Tongo said the shacks of about 400 people are now underwater after two days of "
      "incessant rain. Tongo and about 12 others slept at a church in Zion on Tuesday night. He said many people are staying in less affected "
      "shacks nearby, 'cramped in groups of eight and ten, depending on the size of the shacks'. 'Our shacks have become dams,' said Tongo. "
      "'We had to huddle together on a mattress in one place to avoid leaks. We covered ourselves with three wet blankets that we took out of "
      "flooded shacks … I have been wearing the same clothes since Monday.'")
q25 = [
    stmt("2.5.1", "Define the term flood.", 2,
         ["When a large amount of water covers land that is not usually under water.", "An overflow of water onto normally dry land."],
         ["A long period without rain.", "A river in its normal channel.", "Water stored in a dam.", "A light shower of rain."],
         ["Water where it is not usually.", "Overflow."], 2),
    term("2.5.2", "What caused flooding in Khayelitsha?", ["heavy rains", "heavy rain", "incessant rain", "non-stop rain"],
         ["Read the headline.", "Two days of …"]),
    stmt("2.5.3", "How did the floods affect residents of Khayelitsha?", 2,
         ["They lost their homes and had to shelter in churches.", "Their shacks were flooded."],
         ["They gained new homes.", "They had more clean water to drink.", "Nothing changed for them."],
         ["Read the first paragraph.", "Where did they sleep?"], 2),
    stmt("2.5.4", "Give ONE reason why informal settlements are more affected by floods than formal settlements.", 2,
         ["They are often located below flood lines.", "They use poor building materials that cannot withstand floods.",
          "They lack proper drainage and storm-water systems.", "Their streets are dense and unplanned."],
         ["They are built on high, dry ground.", "They have the best drainage systems.", "Their houses are made of concrete."],
         ["Location and materials.", "Drainage."], 2),
    stmt("2.5.5", "In a paragraph of approximately EIGHT lines, discuss how the City of Cape Town could have prevented the worst effects of flooding "
         "in the urban area.", 8,
         ["Build well-designed storm-water drains to remove run-off.", "Prevent construction close to rivers.",
          "Design disaster plans to handle floods.", "Provide formal houses in safer areas.", "Introduce a better flood warning system."],
         ["Build more shacks on the floodplain.", "Remove all drains.", "Ignore weather warnings."],
         ["Drains, planning, housing, warnings.", "Keep people out of harm's way."], 2)]

# ---- SECTION B, QUESTION 3 (the parts that do not read the maps), the question paper pages 13-15 and the memo pages 10-11 ----
q3 = [
    mcq("3.1.1", "Queenstown is located in the … province.", ["North West", "Western Cape", "Eastern Cape", "Limpopo"], 2,
        ["Read the general information.", "On the Komani River."], marks=1),
    mcq("3.1.3", "The scale of the topographical map (1 : 50 000) is … times smaller than that of the orthophoto map (1 : 10 000).",
        ["0,5", "5", "10 000", "50 000"], 1, ["50 000 ÷ 10 000.", "How many times?"], marks=1),
    stmt("3.2.3(c)", "Describe TWO possible factors that could force people to move from Nooitgedacht (a rural settlement) to Queenstown.", 2,
         ["Few job opportunities", "Lack of basic services", "Poor infrastructure", "Lower wages"],
         ["Many jobs on the farms", "Better schools than in town", "Too many shopping malls"],
         ["Push factors from rural areas.", "Jobs and services."], 1),
    stmt("3.3.1(a)", "Define the concept Geographical Information System.", 2,
         ["A computer-based tool used for capturing, storing, analysing and displaying geographically referenced data.",
          "A system that collects, stores and displays spatial data."],
         ["A paper map of a town.", "A satellite that predicts rainfall.", "A system for paying taxes.", "A telephone directory."],
         ["Spatial data on computers.", "Capture, store, analyse, display."], 2),
    stmt("3.3.1(b)", "Define the concept remote sensing.", 2,
         ["Gathering information about the Earth's surface with sensors that are not in contact with it.",
          "Collecting data about an object from a distance, e.g. by satellite."],
         ["Touching an object to measure it.", "Drawing a map by hand on site.", "Asking people questions in a survey.",
          "Measuring rainfall in a rain gauge."],
         ["Remote means from far away.", "Satellites and aircraft."], 2),
    stmt("3.3.2", "List TWO components of a Geographical Information System.", 2,
         ["Hardware", "Software", "People", "Methods", "Data"], ["Weather", "Rivers", "Mountains"], ["GIS needs equipment and people.",
                                                                                                    "Hardware, software …"], 1)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Population concepts", "marks": 8, "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Population dynamics", "marks": 7,
     "lead": "Choose the correct word(s) between brackets to make the statements true.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Population pyramids", "marks": 15,
     "lead": "Refer to the population pyramid of Japan below for the year 2023.",
     "figure": P.fig("1.3", "Japan's population pyramid, 2023: males on the left and females on the right in five-year age groups. The base is "
                            "narrow (females 0-4: 1,6%, 5-9: 1,9%, 10-14: 2,1%); the widest bars are at 45-54 and 70-74; females outnumber "
                            "males in the oldest groups."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Overpopulation", "marks": 15,
     "lead": "Refer to the photograph and extract below on overpopulation.\nOVERPOPULATION IN INDIA\nWhether you are in a metro station, airport, "
             "railway station, road, highway, bus stop, hospital, shopping mall, market, temple, or even in a social/religious gathering, we "
             "see all these places are overcrowded at any time of the day.\nAccording to the Indian census, carried out in 2011, the population "
             "of India was exactly 1 210 193 422, which means India has crossed the 1-billion mark. This is the second most populous country of "
             "the world after China and various studies have projected that India will be the world's number-1 populous country, surpassing "
             "China, by 2025.",
     "figure": P.fig("1.4", "A crowded railway platform in India, packed with people carrying bags beside a train."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Population movement", "marks": 15,
     "lead": "Refer to the extract on population movement below.\nDudula: How South African anger has focused on foreigners (BBC News, 13 March "
             "2022)\nPolice in South Africa are on alert in case of renewed clashes between residents of Johannesburg's Alexandra township and "
             "foreign street vendors. Alexandra is one of the poorest areas of the country but from its shacks, residents can easily see the "
             "towering skyscrapers of Sandton, one of the richest commercial districts on the whole continent, just a few kilometres away. As a "
             "result, people from across South Africa and neighbouring countries flock to the township to use it as a base to earn a living.\n"
             "Two controversial groups, the Alexandra Dudula Movement and Operation Dudula, which are campaigning against undocumented foreign "
             "nationals, have emerged recently. There are concerns that their campaigns could lead to yet another outbreak of xenophobic "
             "violence in the country.\nPoverty is the main driver of the tension as South African residents believe, whether rightly or "
             "wrongly, that foreigners are the cause of many of their difficulties. Dudula is a word in the Zulu language which loosely means to "
             "'push back' or 'drive back'.\nThough the two groups are separate, they both hope to drive out undocumented African migrants from "
             "their communities. They believe by doing this they can ensure that jobs and business opportunities go to South Africans.",
     "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Water resources", "marks": 7,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Water concepts", "marks": 8,
     "lead": "Choose ONE term/concept from the list below that matches the descriptions that follow.\n" + WLIST, "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Water pollution", "marks": 15,
     "lead": "Refer to the article on water pollution below.\nSOUTH AFRICAN SCIENTISTS USE BUGS IN WAR AGAINST WATER HYACINTH (1 March 2023)\nThe "
             "Hartbeespoort Dam north-west of Johannesburg used to be brimming with people enjoying scenic landscapes and recreational "
             "watersports. Now the visitors are greeted by the sight of boats stuck in a sea of invasive green water hyacinth weed.\nThe spike "
             "in Harties, as Hartbeespoort is known, can be attributed to pollution, with sewage, industrial chemicals, heavy metals and litter "
             "flowing on rivers from Johannesburg and Pretoria.\nNutrients in the pollutants act as perfect fertilisers for the weed, a big "
             "concern for nearby communities due to its devastating impact on livelihoods.\nDion Mostert, 53, is on the verge of laying off 25 "
             "workers at his recreational boat company after his business came to a standstill because of the carpet of water hyacinths. 'The "
             "boats aren't going anywhere. It's affecting tourism in our town… tourist jobs,' Mostert said.\n*Hyacinth: a perennial aquatic "
             "plant, free floating in shallow water.",
     "figure": P.fig("2.3", "An aerial photograph of Hartbeespoort Dam, its water covered by a carpet of water hyacinth with boats stuck in it."),
     "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Water saving", "marks": 15, "lead": "Refer to the cartoon below on water-saving techniques.",
     "figure": P.fig("2.4", "A cartoon water drop titled SAVE WATER, surrounded by bubbles: washing vegetables in a bowl, a shower, a tap crossed "
                            "out, a watering can on plants, fixing a tap with a spanner, and a toothbrush with a glass of water."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Floods", "marks": 15,
     "lead": "Refer to the newspaper article below on floods.\nKHAYELITSHA RESIDENTS SHELTER IN CHURCHES AFTER NON-STOP RAIN (15-06-22)\n" + KH,
     "items": q25},
    {"id": "3", "title": "Question 3", "kind": "Geographical skills and GIS", "marks": 10,
     "lead": "GENERAL INFORMATION ON QUEENSTOWN. Coordinates: 31°54'S; 26°53'E. Queenstown (officially known as Komani) is a town in the Eastern "
             "Cape, roughly halfway between Cathcart and Sterkstroom on the N6 National Route. The town was established in 1853 and is the "
             "commercial, administrative and educational centre of the surrounding farming district. It lies on the banks of the Komani River, "
             "part of the Great Kei river system. A 1 : 50 000 topographic map 3126DD QUEENSTOWN and a 1 : 10 000 orthophoto map 3126DD1 "
             "NOOITGEDACHT are used in the exam room.", "items": q3}]

P.finish(missions,
         {"subject": "Geography", "title": "Geography P2", "sitting": "November 2024", "total_marks": 130, "time": "3 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "3.1.1", "kind": "missing_resource", "detail": "SECTION B reads the 1 : 50 000 topographic map 3126DD Queenstown and the 1 : 10 000 "
                                                               "orthophoto 3126DD1 Nooitgedacht handed out in the exam room; they are not in the "
                                                               "download. 3.1.2, 3.1.4, 3.1.5, 3.2.1, 3.2.2, 3.2.3(a)(b), 3.2.4-3.2.6 and 3.3.3 "
                                                               "(20 marks) wait for the maps; the paper totals 130."},
          {"n": "2.1.2", "kind": "memo_issue", "detail": "The memo gives B (climate change) as 'a physical factor that affects rainfall patterns'. "
                                                         "Topography (A) is the physical factor (relief forces air to rise: orographic rain); "
                                                         "climate change is a long-term change, largely human-driven. The right option is A. "
                                                         "For Murci to confirm."},
          {"n": "2.2.8", "kind": "low_confidence", "detail": "The memo gives 'water pollution', which is not in the printed list; the list's term "
                                                             "is 'marine pollution'. Both are accepted."}],
         {"1": 60, "2": 60, "3": 10}, 130, {"1.3.6(b)": ["1.3.6(a)"]},
         "Section A whole and the parts of Section B that do not read the maps")
