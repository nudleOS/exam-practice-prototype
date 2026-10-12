"""Grade 11 Geography P2 November 2024 (Eastern Cape Department of Education): SECTION A whole (Questions 1 and 2, 120 marks) and the
parts of SECTION B (Question 3) that do not read the maps (14 marks), hand-transcribed into the catalogue format, then run through
`ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and the memo's own; clues and figure
captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the question paper zip (English PDF, 19
pages, text layer) and the memo zip (English, 12 pages).

  python tools/ingest/transcribe_g11_geo_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-geo-p2-2024-11-ec/GEOGRAPHY P2 GR11 QP NOV2024 ENG D_watermark.pdf" "uploads/provincial/g11-geo-p2-2024-11-ec/GEOGRAPHY P2 GR11 MEMO NOV2024_English_watermark.pdf" --id g11-geo-p2-2024-11-ec --from-json

SECTION B reads a 1:50 000 topographical map and a 1:10 000 orthophoto map of MBOMBELA 2530BD handed out in the exam room, not in the
download: as Grade 12's Geography P2 Nov 2024, its 16 marks that read the maps wait for them. 3.1.1 and 3.1.2 (answered from the
paper's own text), 3.2.3 (a general explanation) and 3.3 (its images are printed in the paper) play. The paper totals 134.

The Geography rulings, as in transcribe_g11_geo_p1_2024_11_ec.py. Figure boxes are in PDF points (text blocks and image rects), 1%
inside their neighbours."""
from provincial import Paper

P = Paper("g11-geo-p2-2024-11-ec", 595.22, 842.0, {
    "1.1": [3, 83.0, 169.0, 504.0, 414.0], "1.1.3": [3, 300.0, 537.0, 522.0, 712.0], "1.1.4": [4, 314.0, 60.0, 505.0, 299.0],
    "1.1.5": [4, 314.0, 309.0, 505.0, 490.0], "1.4": [8, 84.0, 91.0, 503.0, 419.0], "1.5": [9, 159.0, 92.0, 421.0, 276.0],
    "2.1": [10, 82.0, 159.0, 505.0, 562.0], "2.3": [12, 86.0, 104.0, 512.0, 427.0], "2.4": [13, 88.0, 92.0, 500.0, 304.0],
    "2.5": [14, 86.0, 90.0, 503.0, 284.0], "3.3": [19, 95.0, 130.0, 495.0, 312.0], "3.3.4": [19, 90.0, 446.0, 490.0, 577.0]}, start=0)
stmt, mcq, term, num = P.stmt, P.mcq, P.term, P.num
two = lambda n, q, a_opt, b_opt, a, clues, marks=1, **kw: mcq(n, q, [a_opt, b_opt], a, clues, marks=marks, **kw)
XZ = ["X", "Z"]

# ---- SECTION A, QUESTION 1: DEVELOPMENT, the question paper pages 3-9 and the memo pages 2-6 ----
q11 = [
    two("1.1.1", "Developing countries based on economic and social criteria:", "South of the Brandt Line", "North of the Brandt Line", 0,
        ["Read the map's LEDCs.", "Below the line."]),
    two("1.1.2", "Brazil, India and South Africa are considered:", "Newly industrialising countries", "Industrialised countries", 0,
        ["Still industrialising.", "Not yet MEDCs."]),
    mcq("1.1.3", "The employment structure in MEDCs:", XZ, 1, ["MEDCs have most people in services.", "Which pie is mostly tertiary?"],
        marks=1, figure=P.fig("1.1.3", "Two pie charts of employment by sector (primary, secondary, tertiary): X mostly primary, Z mostly "
                                       "tertiary.")),
    mcq("1.1.4", "The population pyramid typical of a LEDC:", XZ, 1, ["LEDCs have many children.", "A wide base."], marks=1,
        figure=P.fig("1.1.4", "Two population pyramids: X narrow at the base and wide in the middle ages; Z wide at the base, narrowing "
                              "upwards.")),
    mcq("1.1.5", "The proportion of people living in urban areas in a MEDC:", XZ, 1, ["MEDCs are highly urbanised.", "Mostly urban."],
        marks=1, figure=P.fig("1.1.5", "Two half-circle charts of urban and rural shares: X about half urban, Z mostly urban.")),
    two("1.1.6", "A factor that would contribute positively to a country's HDI:", "Higher literacy rates", "Decreased life expectancy", 0,
        ["HDI uses education, health and income.", "Positive."]),
    two("1.1.7", "A country that has a Gini coefficient score close to 1:", "Income equality", "Income inequality", 1,
        ["0 is perfect equality.", "Close to 1 means …"]),
    two("1.1.8", "An economic indicator that measures the overall economic performance of a country:", "Gross Domestic Product",
        "Level of unemployment", 0, ["The total value of goods and services.", "GDP."])]
q12 = [
    mcq("1.2.1", "Country X has a negative balance of trade because …", ["its exports are greater than its imports.",
                                                                         "its exports and imports are equal amounts.",
                                                                         "its imports are greater that its exports.",
                                                                         "it has no international trade activity."], 2,
        ["Negative: more money going out.", "Imports cost money."], marks=1),
    mcq("1.2.2", "The country that has the biggest trade surplus:", ["China", "Russia", "India", "United Kingdom"], 0,
        ["The world's biggest exporter.", "Factory of the world."], marks=1),
    mcq("1.2.3", "SADC stands for:", ["South African Development Community", "Southern African Development Countries",
                                      "Southern African Development Community", "South African Developing Countries"], 2,
        ["Southern Africa, not South Africa.", "A community."], marks=1),
    mcq("1.2.4", "A key economic benefit of SADC's free trade agreements:", ["A common currency", "Removing competition",
                                                                             "Barriers to entry for businesses",
                                                                             "Enhanced access to international markets"], 3,
        ["Free trade opens markets.", "Access."], marks=1),
    mcq("1.2.5", "Fair Trade is a type of trading relationship based on the principle of:", ["Reducing environmental regulations",
                                                                                             "Transparency and accountability in the supply "
                                                                                             "chain",
                                                                                             "Increasing profits by reducing production costs",
                                                                                             "Prioritising local markets over global markets"],
        1, ["Fair for producers.", "Openness."], marks=1),
    mcq("1.2.6", "Financial assistance from the government to help local businesses compete against foreign imports:", ["Quota", "Tariff",
                                                                                                                           "Subsidy",
                                                                                                                           "Embargo"], 2,
        ["Money given.", "Not a tax or a limit."], marks=1),
    mcq("1.2.7", "The main difference between a tariff and an import quota: (i) Tariffs are taxes on imports (ii) Import quotas limit quantity "
        "of imports (iii) Tariffs are taxes on exports (iv) Import quotas encourage more imports", ["(i) and (ii)", "(ii) and (iii)",
                                                                                                   "(iii) and (iv)", "(i) and (iv)"], 0,
        ["Tariffs tax imports.", "Quotas limit them."], marks=1)]
WYRE = ("EMPOWERING RURAL COMMUNITIES: INVESTING IN WOMEN\nRural communities and rural women in particular, bear the largest burden of "
        "poverty in South Africa. The main factors contributing to the poverty of rural women include low literacy and skills training and "
        "poor access to services, especially healthcare.\nInvesting in women is an imperative to development. Women often have different "
        "needs than men due to their societal standing, as well as continuing imbalance in the divisions of labour for managing or "
        "undertaking domestic tasks, such as taking care of or raising children.\nThe Kwanalu's Women and Youth in Rural Entrepreneurship "
        "(WYRE) initiative aims to strengthen KZN's rural and farming communities. Its goal is to build productive and sustainable family and "
        "community livelihoods.\nThrough WYRE's programme, women who are part of the community development programme receive the following "
        "support: agricultural training; financial and business management training; access to finance; networking (linking women across "
        "Africa).\nThe WYRE programme is not only enhancing the skills and leadership qualities of its participants, but is also playing a "
        "crucial role in the sustainable development of rural economies in KZN, fostering a new generation of entrepreneurial leaders in "
        "agriculture.")
q13 = [
    stmt("1.3.1", "What is community development?", 2, ["Development for the people by the people, where community members and stakeholders "
                                                         "work together to identify needs and implement development."],
         ["Development planned only by foreign governments.", "The building of shopping malls in cities.", "Moving rural people to cities.",
          "A loan from the World Bank."], ["By the people.", "Working together."], 2),
    stmt("1.3.2", "Why are women important to community development?", 2,
         ["Women contribute to household incomes.", "Many families are headed by women.", "Women are primary caregivers who raise children.",
          "Women play an important role in managing natural resources."],
         ["Women take no part in farming.", "Women are not affected by poverty."], ["Households and families.", "Caregivers and earners."],
         1),
    stmt("1.3.3", "According to the extract, why do rural women bear the largest burden of poverty?", 2,
         ["Low literacy", "Poor skills training", "Poor access to services such as healthcare"], ["High wages", "Too many schools",
                                                                                                 "Easy access to finance"],
         ["Read the first paragraph.", "The main factors …"], 1),
    two("1.3.4(a)", "The WYRE initiative provides women with (physical / human) capital.", "physical", "human", 1,
        ["Training builds people's skills.", "Skills are human capital."]),
    stmt("1.3.4(b)", "How will agricultural training help alleviate poverty in rural communities?", 2,
         ["It increases agricultural productivity and crop yields.", "It contributes to food security.", "It creates employment opportunities.",
          "Farmers earn profits from selling produce."],
         ["It reduces the food available.", "It increases crime."], ["Better farming.", "Food and income."], 1),
    stmt("1.3.5", "Explain how the WYRE initiative hopes to empower women to become entrepreneurial leaders in agriculture throughout the "
         "continent.", 6,
         ["Agricultural training improves productivity and profitability in farming.", "Access to finance helps women buy inputs and expand.",
          "Business management training gives skills in planning, marketing and sales.", "Networking opens opportunities for partnerships "
                                                                                         "across Africa."],
         ["The initiative stops women from farming.", "It replaces training with charity handouts."],
         ["Training, finance, networking.", "Each card gives support and its benefit."], 2)]
q14 = [
    stmt("1.4.1", "State ONE factor evident in A that enables the sharing of knowledge.", 1,
         ["Internet connection", "Digital technology", "Communication networks", "Mobile devices"], ["Cargo ships", "Coal mines"],
         ["A shows computers and a world map.", "Technology."], 1),
    stmt("1.4.2", "How have modern transportation systems (B) promoted globalisation?", 2,
         ["Lower costs of transport.", "Quicker transport of goods.", "Increased access to markets."],
         ["Transport became slower and more expensive.", "Borders closed to trade.", "Fewer goods could be moved."],
         ["Faster and cheaper.", "Goods across borders."], 2),
    stmt("1.4.3", "Why can consumers benefit from increased globalisation of trade?", 2,
         ["Access to a wider range of products", "Lower prices", "Higher quality products"], ["Fewer products", "Higher prices",
                                                                                             "Lower quality goods"],
         ["Consumers buy.", "More choice."], 1),
    stmt("1.4.4", "Explain how liberalisation of trade (encouraged by globalisation) present challenges for local businesses.", 4,
         ["Foreign competitors have advantages, making it difficult for local businesses to compete.",
          "An influx of similar products reduces demand for local goods.", "Price pressure forces local businesses to lower their prices."],
         ["Local businesses face less competition.", "Imports increase the demand for local goods."], ["Open borders, more competitors.",
                                                                                                     "Prices and demand."], 2),
    stmt("1.4.5", "What potential environmental problems are associated with increased globalisation?", 6,
         ["Increased carbon emissions.", "Deforestation and habitat loss.", "Industrial pollution of air, water and soil.",
          "Higher levels of waste.", "Overfishing disrupts marine ecosystems."],
         ["Cleaner air everywhere.", "Less transport of goods.", "More forests planted."], ["More production and transport.",
                                                                                           "Pollution and loss."], 2)]
AID = ("FOREIGN AID: IMPACT ON DEVELOPMENT\nOver the decades, billions of dollars have been channelled from wealthier nations to poorer ones in "
       "the hope of promoting economic growth, alleviating poverty and enhancing the people's quality of life.\nHowever, a complex and often "
       "disappointing reality emerges: despite these efforts, many developing countries continue to struggle with high levels of poverty. "
       "Despite receiving $36 billion annually in aid, Sub-Saharan Africa remains the poorest region globally.\nOne of the factors "
       "contributing to the limited success of foreign aid is when it comes with conditions. Unfortunately, when all the conditions are "
       "considered, the aid may not necessarily benefit the recipient's population.\nForeign aid undoubtedly plays a crucial role in "
       "addressing immediate humanitarian needs and supporting development initiatives in struggling economies. However, the notion that aid "
       "alone can lift countries out of poverty, is overly simplistic and often unrealistic.")
q15 = [
    stmt("1.5.1", "According to the extract, what is the purpose of foreign aid?", 1,
         ["Promote economic growth", "Alleviate poverty", "Enhance people's quality of life"], ["Increase debt", "Fund wars"],
         ["Read the first paragraph.", "In the hope of …"], 1),
    stmt("1.5.2", "What factors, as indicated in the cartoon, hinder the success of foreign aid in Africa?", 2,
         ["Theft", "Waste", "Dictators", "Corruption", "Crime", "Graft"], ["Rainfall", "Education"], ["Read the pipes' leaks.", "Where does "
                                                                                                                              "the aid "
                                                                                                                              "leak?"], 1),
    stmt("1.5.3", "Why does conditional aid not necessarily benefit the recipient country's population?", 4,
         ["The donor may have a hidden agenda that is not beneficial.", "Aid may not suit the needs of the recipient country.",
          "The focus is on immediate results to satisfy the donor.", "Long-term development goals can be neglected."],
         ["Conditions always match local needs.", "Conditional aid has no strings attached."], ["Conditions come from the donor.",
                                                                                                "Whose needs?"], 2),
    stmt("1.5.4", "In a paragraph of approximately EIGHT lines, explain how technical aid can be beneficial in eradicating poverty.", 8,
         ["Training and education equip people with skills that enhance employability.", "Development projects create jobs (a multiplier "
                                                                                          "effect).",
          "Technical aid builds local skills to solve problems and manage resources.", "Empowered communities become self-reliant.",
          "Increased agricultural production contributes to food security."],
         ["Technical aid makes communities dependent forever.", "Technical aid removes local skills.", "It is only short-term food parcels."],
         ["Skills, not just money.", "Self-reliance."], 2)]

# ---- QUESTION 2: RESOURCES AND SUSTAINABILITY, the question paper pages 10-15 and the memo pages 7-10 ----
q21 = [
    term("2.1.1", "The South African province with the largest concentration of coal mines.", ["Mpumalanga"], ["Read the map's key.",
                                                                                                              "East of Gauteng."]),
    term("2.1.2", "The process of grinding coal into a fine powder.", ["pulverisation", "pulverization", "pulverising"], ["Read the sketch.",
                                                                                                                       "Fine powder."]),
    term("2.1.3", "The heat needed for producing the steam comes from the burning of which fuel?", ["coal"], ["A fossil fuel.", "Thermal power."]),
    term("2.1.4", "The solid waste produced by the power station that accumulates at the bottom of the furnace.", ["ash"],
         ["Left after burning.", "At the bottom."]),
    term("2.1.5", "The machine which turns mechanical energy into electrical energy.", ["generator"], ["Turned by the turbine.",
                                                                                                      "Generates."]),
    term("2.1.6", "What is handled and dispersed of by the smokestack?", ["flue gases", "flue gasses", "gases", "gasses"],
         ["Out of the chimney.", "Flue …"]),
    term("2.1.7", "Heat removed from the steam is dissipated through which component of the power plant?", ["cooling tower", "cooling towers"],
         ["Hot moist air rises out of it.", "Cooling …"]),
    term("2.1.8", "To adjust the voltage for long-distance travel, to what is generated electricity sent?", ["transformer", "transformers"],
         ["Before the power lines.", "It changes voltage."])]
EN = ["Thermal energy", "Solar energy", "Nuclear energy", "Hydro energy"]
q22 = [
    mcq("2.2.1", "Produces radioactive waste.", EN, 2, ["Radioactive.", "Uranium."], marks=1),
    mcq("2.2.2", "South Africa's primary source of electricity.", EN, 0, ["Coal-fired.", "Most of SA's power."], marks=1),
    mcq("2.2.3", "The leading renewable energy source in South Africa.", EN, 1, ["Renewable.", "Plenty of sun."], marks=1),
    mcq("2.2.4", "The Gariep Dam is the largest … facility in South Africa.", EN, 3, ["A dam.", "Water power."], marks=1),
    mcq("2.2.5", "Obtained by splitting uranium atoms.", EN, 2, ["Splitting atoms.", "Fission."], marks=1),
    mcq("2.2.6", "Requires photovoltaic (PV) installations.", EN, 1, ["PV panels.", "Sunlight."], marks=1),
    mcq("2.2.7", "The non-conventional energy source in South Africa.", EN, 1, ["Non-conventional: not coal.", "Read the memo's pick: the "
                                                                                                                 "sun."], marks=1)]
q23 = [
    stmt("2.3.1", "What is soil erosion?", 2, ["Soil erosion is the loss of soil from the ground's surface by wind and water."],
         ["Soil erosion is the formation of new soil.", "Soil erosion is planting trees.", "Soil erosion is adding fertiliser.",
          "Soil erosion is the flooding of a dam."], ["Soil is lost.", "Wind and water."], 2),
    term("2.3.2", "From the sketch above, provide evidence of soil erosion.", ["donga", "dongas", "gully", "gullies"],
         ["Look at the circled photo.", "A deep channel."]),
    stmt("2.3.3", "Why does overgrazing by livestock (X) contribute to soil erosion?", 4,
         ["Vegetation is removed, reducing the ground cover that protects the soil.", "Bare soil is more easily displaced by wind and water.",
          "Raindrops hit the soil directly, dislodging soil particles.", "Soil compaction reduces infiltration and increases runoff."],
         ["Overgrazing plants more grass.", "Livestock bind the soil with roots."], ["Animals eat the cover.", "Bare and compacted."], 2),
    stmt("2.3.4", "What are the negative economic effects of soil erosion?", 4,
         ["Soil conservation and restoration measures are expensive.", "Reduced agricultural productivity and lower crop yields.",
          "Increased food prices.", "Loss of arable land."],
         ["Higher crop yields.", "Cheaper food."], ["Farming suffers.", "Costs and losses."], 2),
    stmt("2.3.5", "How does the management strategy implemented at Z prevent soil erosion?", 4,
         ["Vegetation protects the soil from heavy rain.", "Roots bind and stabilise the soil.", "Trees act as a windbreak.",
          "More vegetation means less runoff and more infiltration."],
         ["Removing trees exposes the soil.", "Afforestation increases runoff."], ["Z is afforestation.", "Trees protect soil."], 2)]
q24 = [
    num("2.4.1", "According to the graph, what percentage of South Africa's electricity is nuclear generated?", 4.9, 0, "%",
        ["Read the pie chart.", "Nuclear's slice."]),
    stmt("2.4.2", "How does South Africa's uranium production support the proposal for two new nuclear reactors?", 2,
         ["South Africa can support its own nuclear infrastructure with local uranium.", "A domestic source ensures a stable supply for future "
                                                                                          "projects.",
          "It is cost-effective, as uranium is produced locally and not imported."],
         ["South Africa must import all its uranium.", "Uranium production makes reactors unnecessary.", "Uranium is used only for coal."],
         ["The 11th-largest producer.", "Local supply."], 2),
    stmt("2.4.3", "Why is nuclear power production an option for the country to achieve net-zero emissions?", 4,
         ["Lower greenhouse gas emissions.", "No fossil fuels are burnt, so no carbon dioxide is released.", "Significantly less air pollution.",
          "A small amount of uranium produces a large amount of energy."],
         ["Nuclear power burns coal.", "Nuclear power releases large amounts of carbon dioxide."], ["Low-carbon.", "No burning."], 2),
    stmt("2.4.4", "In a paragraph of approximately EIGHT lines, explain why South Africa favours coal as its main source of energy despite the "
         "advantages associated with nuclear energy.", 8,
         ["Abundant coal reserves make coal readily available and cost-effective.", "Infrastructure for coal mining and power generation is "
                                                                                    "already established.",
          "Coal extraction is relatively cheap in South Africa.", "The coal industry supports a large number of jobs.",
          "Most power plants are designed to run on coal."],
         ["South Africa has no coal reserves.", "Coal is imported at high cost.", "Coal power creates no jobs."],
         ["Plenty of coal, existing plants, jobs.", "History and cost."], 2)]
JET = ("THE COST OF NON-CONVENTIONAL ENERGY IN SOUTH AFRICA\nSouth Africa is at a critical moment in its energy transition (shift): trying to "
       "decarbonise its economy and make sure that everyone has access to reliable and affordable energy. South Africa is a major carbon "
       "emitter and there is an urgent need for the country to reduce its greenhouse gas emissions.\nWhile the country has already made "
       "progress in integrating renewable energy into its power grid, its path to a sustainable energy future is complicated by financial "
       "problems and limited energy storage technology. Renewable energy sources, such as wind and solar are intermittent (erratic) and their "
       "output fluctuates. As a result, it is important to set up grid-scale storage which is very expensive.\nThe International Partners "
       "Group has agreed to give South Africa $8,5 billion. The money aims to accelerate (quicken) the decarbonisation of South Africa's "
       "economy to help it achieve the goal of reaching net-zero carbon emissions by 2050. However, only 2,7% of the offers are grants, with "
       "the other 97% in the form of loans.")
q25 = [
    stmt("2.5.1", "What is non-conventional energy?", 2, ["Energy sources that are not widely used, considered alternatives to traditional "
                                                          "fossil fuels."],
         ["Energy from burning coal.", "Energy that is used everywhere.", "Energy from oil only.", "Energy that cannot be renewed."],
         ["Not conventional.", "Alternatives."], 2),
    num("2.5.2", "According to the graph, what percentage of global carbon dioxide (CO₂) from fossil fuels, does South Africa contribute?", 1.7,
        0, "%", ["Read the last bar.", "South Africa."]),
    stmt("2.5.3(a)", "Give evidence from the extract that shows that South Africa's energy shift is influenced by a social factor.", 1,
         ["Make sure that everyone has access to reliable and affordable energy."],
         ["South Africa is a major carbon emitter.", "Only 2,7% of the offers are grants.", "Wind and solar are intermittent.",
          "Grid-scale storage is very expensive."], ["Social: people.", "Everyone."], 1),
    stmt("2.5.3(b)", "Give evidence from the extract that shows that South Africa's energy shift is influenced by an environmental factor.", 1,
         ["Trying to decarbonise its economy.", "South Africa is a major carbon emitter.", "An urgent need to reduce greenhouse gas emissions."],
         ["Only 2,7% of the offers are grants.", "Make sure everyone has affordable energy."], ["Environmental: emissions.", "Carbon."], 1),
    stmt("2.5.4", "What makes wind and solar energy sources unreliable?", 4,
         ["They are intermittent, depending on weather conditions.", "They vary from place to place and over time.",
          "Storage technologies are complex.", "It is difficult to balance supply and demand in real time."],
         ["They never stop producing power.", "They burn coal at night."], ["Weather.", "Storage."], 2),
    stmt("2.5.5", "Explain the negative effects on the South African economy as it implements increased non-conventional energy sources.", 6,
         ["Loan repayments are very expensive.", "Initial costs for renewable infrastructure are high.", "Grid upgrades are costly.",
          "The shift away from coal can lead to job losses."],
         ["The shift is completely free.", "More coal jobs are created."], ["Mostly loans.", "Costs and jobs."], 2)]

# ---- SECTION B, QUESTION 3: the parts that do not read the maps, the question paper pages 16-19 and the memo pages 11-12 ----
q31 = [
    mcq("3.1.1", "Mbombela lies about 330 km east of Johannesburg. Johannesburg is in a(n) … direction from Mbombela.",
        ["north-easterly", "south-westerly", "westerly", "easterly"], 2, ["Mbombela is east of Johannesburg.", "So Johannesburg is …"],
        marks=1),
    mcq("3.1.2", "The scale of the 1 : 10 000 orthophoto map is … times … than the scale of the 1 : 50 000 topographical map. (i) five "
        "(ii) ten (iii) smaller (iv) larger", ["(i) and (iii)", "(i) and (iv)", "(ii) and (iii)", "(iii) and (iv)"], 1,
        ["50 000 ÷ 10 000.", "A smaller denominator is a larger scale."], marks=1),
    stmt("3.2.3", "Explain the negative impact that soil erosion, caused by an excavation (feature H), can have on the river (J).", 4,
         ["Eroded soil leads to sedimentation of the river.", "Erosion weakens riverbanks, increasing the risk of collapse.",
          "Pollutants in the soil degrade water quality.", "Increased sediment increases the risk of flooding."],
         ["Erosion makes the river deeper and cleaner.", "Sediment improves aquatic habitats."], ["Soil washes into the river.",
                                                                                                 "Sediment and pollution."], 2)]
q33 = [
    mcq("3.3.1", "Which image (A or B) is vector data?", ["A", "B"], 0, ["Vector: points, lines and polygons.", "The drawn map."], marks=1),
    term("3.3.2", "Identify a natural line feature on A.", ["river", "non-perennial river", "stream"], ["Natural, not a road.",
                                                                                                       "Water flows in it."]),
    stmt("3.3.3", "Why is B classified as a vertical aerial photograph?", 1,
         ["The image is taken from directly above the ground.", "It is taken at a right angle to the ground."],
         ["It is taken from the side.", "It is drawn by hand.", "It is taken at ground level."], ["Vertical.", "From above."], 1)]
q334 = [
    stmt("3.3.4", "What is spatial resolution?", 2, ["How clear and easy the detail is to see on a picture."],
         ["The scale written on a map.", "The colour of a photograph.", "The number of maps in an atlas.", "The direction of north."],
         ["Compare the three photos.", "Detail."], 2),
    mcq("3.3.5", "The image with a (high / medium / low) spatial resolution has the highest number of pixels.", ["high", "medium", "low"], 0,
        ["More pixels, more detail.", "Which looks sharpest?"], marks=1),
    stmt("3.3.6", "How has the size of the pixels influenced the image with a low spatial resolution?", 2,
         ["The larger the pixels, the less the detail, clarity and accuracy."],
         ["Larger pixels make the image sharper.", "Pixel size has no effect.", "Smaller pixels blur the image.", "Larger pixels add colour."],
         ["Big pixels average an area.", "Less detail."], 2)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "The North-South divide", "marks": 8,
     "lead": "Refer to the map showing the 'North-South' divide. Complete the statements in COLUMN A with the options in COLUMN B.",
     "figure": P.fig("1.1", "A world map divided by the Brandt Line into MEDCs in the north and LEDCs in the south."), "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Multiple choice", "marks": 7,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Rural community development", "marks": 15,
     "lead": "Refer to the extract below on rural community development.\n" + WYRE, "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Globalisation", "marks": 15, "lead": "Refer to the sketch below on globalisation.",
     "figure": P.fig("1.4", "GLOBALISATION: A, computers and devices before a world map; B, ships and planes over a world map; POSITIVES: "
                            "sharing knowledge and innovation, consumers benefit; NEGATIVES: local businesses, impact on environment."),
     "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Development aid", "marks": 15,
     "lead": "Refer to the cartoon and extract on development aid.\n" + AID,
     "figure": P.fig("1.5", "A cartoon: a large pipe labelled AFRICA AID leaks through holes labelled theft, waste, dictators, corruption, "
                            "crime and graft."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Thermal power", "marks": 8,
     "lead": "The sketches below show a simplified version of thermal power production. Match each description with the information from the "
             "sketches.",
     "figure": P.fig("2.1", "A map of South Africa's coal mines by province; coal on a conveyance to pulverisation; a power station: coal into "
                            "a boiler, steam to a turbine and generator, a transformer and power lines, a smokestack with flue gasses, a "
                            "cooling tower with hot moist air, and ash below."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Energy sources", "marks": 7,
     "lead": "The images show different ways that electrical energy is obtained in South Africa: thermal energy, solar energy, nuclear energy "
             "and hydro energy. Match each description with the appropriate energy source.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Soil erosion", "marks": 15, "lead": "Refer to the sketch and photos on soil erosion.",
     "figure": P.fig("2.3", "Photos before and after afforestation of a slope (Z), and a sketch of a farm with livestock at X grazing near a "
                            "river, a circled photo of a deep channel in the soil."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Energy in South Africa", "marks": 15,
     "lead": "Refer to the infographic on conventional energy sources in South Africa.\nNuclear energy has been significant in South Africa's "
             "energy landscape for decades with the country's first and only nuclear power plant constructed in 1976 in Duynefontein, near Cape "
             "Town. Koeberg NPP, owned and operated by Eskom, has two reactors with a combined capacity of 1 869 MW.\nSouth Africa's focus on "
             "nuclear energy (as a low-carbon source of energy) is ever-increasing as the global drive towards mitigating climate change and "
             "South Africa's goal of achieving net-zero emissions becomes more pressing.\nHowever, despite the potential of nuclear production "
             "to help with the country's energy supply and meet climate goals, nuclear energy provides only 4,9% of the electricity "
             "supplied to the grid today. In South Africa, there is a historical dependency on coal due to its abundance and the economic "
             "importance of the mining industry.",
     "figure": P.fig("2.4", "A pie chart of South Africa's electricity generation by source (coal, nuclear, other) and a table, OVERVIEW OF SOUTH "
                            "AFRICA'S NUCLEAR POWER (2023): generation 8,2 TWh, 2 reactors operable, 0 under construction, 2 proposed, 277 tons "
                            "of uranium a year; the world's eleventh-largest producer of uranium."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Energy management", "marks": 15,
     "lead": "Refer to the graph and extract on energy management in South Africa.\n" + JET,
     "figure": P.fig("2.5", "A bar graph, TOP CO₂ EMITTING COUNTRIES FROM FOSSIL FUELS, percentages for China, USA, India, Russia, Japan, Germany, "
                            "Indonesia, Iran, Korea, Canada, Saudi Arabia and South Africa."), "items": q25},
    {"id": "3.1", "title": "Question 3", "kind": "Geographical skills (without the maps)", "marks": 6,
     "lead": "GENERAL INFORMATION ON MBOMBELA\nMbombela, formerly Nelspruit, is a city in northeastern South Africa. It is the capital of the "
             "Mpumalanga province. Located on the Crocodile River, the city lies about 330 km east of Johannesburg. (A 1 : 50 000 topographical "
             "map and a 1 : 10 000 orthophoto map of Mbombela are not available: only the parts that do not read them play.)", "items": q31},
    {"id": "3.3", "title": "Question 3.3", "kind": "GIS", "marks": 3,
     "lead": "Refer to A, extracted from block D4 on the topographical map, and B, which shows a portion of the orthophoto map.",
     "figure": P.fig("3.3", "A: a black-and-white map extract with roads, buildings and a river. B: an aerial photograph of the same kind of "
                            "area."), "items": q33},
    {"id": "3.3.4", "title": "Question 3.3.4", "kind": "Spatial resolution", "marks": 5,
     "lead": "Refer to the photographs below to answer QUESTIONS 3.3.4 to 3.3.6.",
     "figure": P.fig("3.3.4", "The same aerial photograph at HIGH, MEDIUM and LOW SPATIAL RESOLUTION, from sharp to blurred."), "items": q334},
]
P.finish(missions,
         {"subject": "Geography", "title": "Geography P2", "sitting": "November 2024", "total_marks": 134, "time": "3 hours"},
         [{"n": "3.1", "kind": "missing_resource", "detail": "SECTION B reads a 1 : 50 000 topographical map and a 1 : 10 000 orthophoto map of "
                                                             "MBOMBELA 2530BD handed out in the exam room, not in the download: its 16 "
                                                             "map-reading marks (3.1.3-3.1.5, 3.2.1, 3.2.2, 3.2.4-3.2.7) wait for the maps; "
                                                             "the paper plays 134."},
          {"n": "3.2.3", "kind": "no_fit", "detail": "3.2.3 names feature H as the memo's answer to 3.2.1 (an excavation), which reads the map."}],
         {"1": 60, "2": 60, "3": 14}, 134, {}, "Section A whole and the Section B parts that do not read the maps")
