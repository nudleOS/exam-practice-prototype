"""Geography P2 Nov 2025: SECTION A whole (Questions 1 and 2, 120 marks) and the parts of SECTION B (Question 3) that do not read
the maps (11 marks), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the memo's points are the paper's and the
memo's own; clues and figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_geo_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Geography P2 Nov 2025 Eng.pdf" "<...>/Geography P2 Nov 2025 MG Eng.pdf" --id geo-p2-2025-11 --from-json

SECTION B reads a 1:50 000 topographical map (2529CC eMALAHLENI (WITBANK)) and a 1:10 000 orthophoto map (2529 CC 15) that are
handed out in the exam room: they are not in the question paper and DBE does not publish them. Its 19 marks that read the maps
(3.1.1, 3.1.2, 3.1.4, 3.2.1-3.2.5, 3.2.7, 3.3.4) wait for the maps; the paper totals what is playable, 131.
The memo's shapes map as in transcribe_geo_p1_2025_11.py. A part that reads a TABLE plays on the page (the MCQ stage shows no
table), so 2.2.1-2.2.4 (the GDP table) are their own mission and 2.2.5-2.2.7 another (2.2.5's sketch is its own figure).
Figure boxes are measured in PDF points (page 595.32 x 841.92) and checked on a contact sheet."""
import json
from pathlib import Path

W, H = 595.32, 841.92
FIGS = {  # tools: scratchpad geo/figs_geo_p2.json; [page, x0, y0, x1, y1] in points
    "1.1.5": [3, 147, 393, 370, 476], "1.1.6": [3, 147, 517, 378, 592], "1.1.7": [3, 147, 635, 378, 706],
    "1.2.1": [4, 157, 184, 429, 330], "1.2.2": [4, 157, 465, 429, 605], "1.2.6": [5, 182, 431, 507, 570], "1.2.8": [6, 150, 166, 380, 270],
    "1.3": [7, 94, 129, 523, 301], "1.4": [8, 60, 241, 540, 590], "1.5": [9, 151, 414, 477, 575], "2.1": [11, 101, 231, 507, 479],
    "2.2.5": [12, 191, 567, 333, 644], "2.3": [13, 54, 113, 532, 697], "2.4": [14, 102, 562, 354, 706], "2.5": [15, 60, 270, 315, 421],
    "3.3": [20, 102, 116, 527, 343]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None, must=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {})}


term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}

GOLD = "A line graph, NUMBER OF PEOPLE EMPLOYED IN GOLD MINES FROM 1995 TO 2025: from about 385 000 in 1995 it falls steeply to about " \
       "200 000 by 2000, levels off, falls to about 160 000 by 2005, stays near 160 000 to 2010, then falls slowly to about 95 000 by " \
       "2020 and about 80 000 in 2025."

# ---- QUESTION 1: RURAL AND URBAN SETTLEMENTS, the question paper pages 3-9 and the memo pages 4-7 ----
q11 = [
    mcq("1.1.1", "Settlements are classified as rural, based on …", ["the number of functions", "the total population"], 0,
        ["Rural settlements are defined by what people DO there.", "Farming and other primary activities."]),
    mcq("1.1.2", "The actual physical position where a rural settlement is located", ["site", "situation"], 0,
        ["One describes the land the settlement is built on.", "The other describes its position relative to the surroundings."]),
    mcq("1.1.3", "A loose grouping of farmsteads is called a …", ["town", "hamlet"], 1,
        ["It is the smallest group of dwellings above a single farmstead.", "Not yet a village."]),
    mcq("1.1.4", "A … has mostly rural functions and some urban functions.", ["farmstead", "village"], 1,
        ["Bigger than a hamlet.", "It may have a shop, a school or a church."]),
    mcq("1.1.5", "The pattern of the settlement below is …", ["nucleated", "dispersed"], 1,
        ["Are the buildings grouped together or spread out?", "Look at the distances between them (scale 1:30 000)."],
        figure=fig("1.1.5", "A sketch at a scale of 1:30 000: four single buildings (settlements) far apart, each at the end of a road "
                   "branching off a main road.")),
    mcq("1.1.6", "The sketch below depicts a … settlement.", ["wet-point", "dry-point"], 0,
        ["The settlement is built beside the river, inside the 60 m contour.", "Was it built close to water, or above flooding?"],
        figure=fig("1.1.6", "A sketch: a river winds across the middle, contour lines of 60 and 80 m on both sides; small buildings stand "
                   "close to the river on the low ground.")),
    mcq("1.1.7", "The shape of the settlement below is …", ["linear", "round"], 0,
        ["Follow the buildings: what do they line up along?", "A settlement along a river or road is stretched out."],
        figure=fig("1.1.7", "A sketch: buildings lined up along both banks of a winding river."))]
q12 = [
    mcq("1.2.1", "A … trade and transport town/city is shown in the photograph below.", ["gap", "junction", "break-of-bulk-point", "specialised"], 2,
        ["The photograph shows a harbour with cranes and ships.", "Goods change from one kind of transport to another here."],
        figure=fig("1.2.1", "An aerial photograph of a port city: a harbour with cranes, ships and railway lines beside a city centre of "
                   "tall buildings.")),
    mcq("1.2.2", "Plettenberg Bay in the photograph below is classified as a/an … urban settlement and its dominant economic function is …\n"
        "(i) gateway\n(ii) specialised\n(iii) tourism\n(iv) mining", ["(i) and (iii)", "(i) and (iv)", "(ii) and (iii)", "(ii) and (iv)"], 2,
        ["The photograph shows a crowded beach and a large hotel.", "A town built around one main function is ..."],
        figure=fig("1.2.2", "A photograph of a crowded beach with umbrellas and a large hotel behind it.")),
    mcq("1.2.3", "A … provides mostly low-order goods and services to the surrounding rural population.", ["city", "metropolis", "conurbation", "town"], 3,
        ["Low-order goods are bought often and cheaply (bread, milk).", "Which is the smallest urban settlement listed?"]),
    mcq("1.2.4", "… is the maximum distance that people will travel to buy goods or obtain services.",
        ["Sphere of influence", "Range", "Market", "Threshold population"], 1,
        ["Not the number of people needed, but a distance.", "How far will they go?"]),
    mcq("1.2.5", "… refers to the uncontrolled growth of urban areas.", ["Rate of urbanisation", "Urban growth", "Urban sprawl", "Level of urbanisation"], 2,
        ["The city spreads out over the countryside.", "Unplanned and uncontrolled."]),
    mcq("1.2.6", "The cartoon below depicts the negative impact of …", ["urban blight.", "urban renewal.", "counter-urbanisation.", "urban expansion."], 3,
        ["The buildings are 'eating' the trees.", "The city is growing into the natural land."],
        figure=fig("1.2.6", "A cartoon: tall buildings drawn as a monster with open jaws biting into a row of trees (KEY: building, tree).")),
    mcq("1.2.7", "… is a process whereby an increasing percentage of a country's population lives in urban rather than rural areas.",
        ["Urbanisation", "Population growth", "Urban growth", "Rural-urban migration"], 0,
        ["It is about the PERCENTAGE living in towns.", "The process, not the movement of people itself."]),
    mcq("1.2.8", "Refer to the table on the level and rate of urbanisation in South Africa. The level (%) of urbanisation in 2022 AND the rate (%) of "
        "urbanisation in 2024 is … and …\n(i) 68,34\n(ii) 69,34\n(iii) 0,51\n(iv) 0,47", ["(i) and (iii)", "(i) and (iv)", "(ii) and (iii)", "(ii) and (iv)"], 1,
        ["The level rises by about 0,5% a year: 2022 lies between 2021 and 2023.", "The rate falls by about 0,01 each year."],
        figure=fig("1.2.8", "A table, YEAR / LEVEL (%) / RATE (%): 2020 67,35 0,55; 2021 67,85 0,50; 2022 (blank) 0,49; 2023 68,82 0,48; "
                   "2024 69,30 (blank)."))]
q13 = [
    num("1.3.1", "According to the graph, state the rural population percentage of South Africa for 2024.", 31.18, 0.005, "%",
        ["Read the last bar.", "It is labelled with its value."]),
    term("1.3.2", "Give the general trend in the rural population (percentages) as depicted between 2017 and 2024 in the graph.",
         ["Downward", "Decreases", "Decreasing", "Decrease", "Declining", "Downward trend", "Decreasing trend"],
         ["Compare the first bar with the last.", "Is it going up or down?"]),
    rub("1.3.3", "Explain the social impact that the general trend (answer to QUESTION 1.3.2) will have on the rural community.", 4, [
        "Decrease in employment opportunities (accept examples) (2).", "Lack of facilities (accept examples) (2).", "Lack of services (accept examples) (2).",
        "Quality of life/standard of living will deteriorate (accept examples) (2).", "It will increase poverty (accept examples) (2).",
        "Infrastructure will deteriorate (accept examples) (2).", "Increase in crime/social ills (accept examples) (2).",
        "Population imbalance (accept examples) (2).", "Family ties are broken (accept examples) (2).", "Less social interaction (2).",
        "Loss of community identity (accept examples) (2)."],
        ["People are leaving the countryside.", "What happens to the people left behind and to their services?"], each=2),
    rub("1.3.4", "Refer to the extract on land restitution. What is land restitution?", 2, [
        "Returning the land to its rightful owners (2).", "Compensation for people for land forcefully taken away (2)."],
        ["It corrects past land dispossession.", "Land given back, or ..."], each=2),
    lst("1.3.5", "According to the extract, which option (model) of land restitution applied to the Moletele community?", 1,
        [["Opted to take their land back", "Take their land back", "Took their land back", "Restoration of land"]],
        ["Read the extract's first sentence.", "Land back, or money instead?"]),
    rub("1.3.6", "Suggest strategies that can be implemented after land restitution has taken place to reduce rural depopulation (as indicated in the graph).", 6, [
        "Facilitate skills training/education (accept examples) (2).", "Provide technical support (accept examples) (2).", "Provide financial training (2).",
        "Promote commercial farming (2).", "Create employment opportunities (accept examples) (2).", "Form business partnerships (accept examples) (2).",
        "Involve all stakeholders in decision making (accept examples) (2).", "Improve infrastructure (accept examples) (2).",
        "Improve services (accept examples) (2).", "Make financial subsidies available (2)."],
        ["Why do people leave? Give them reasons to stay.", "The Moletele farm shows some of them: jobs, skills, partnerships."], each=2)]
q14 = [
    rub("1.4.1", "What is an urban land-use zone?", 2, ["Land that has been zoned for a specific function (in an urban settlement) (2)."],
        ["A zone is an area of the town.", "It is set aside for one main use."], each=2),
    lst("1.4.2", "Name TWO urban land-use zones where commercial functions are mainly found.", 2,
        [["Central Business District", "CBD"], ["Transition zone", "Transition"], ["Residential zone", "Residential"], ["Rural-urban fringe"]],
        ["Commercial: shops and offices.", "Read the KEY of the urban profile."]),
    lst("1.4.3(a)", "Refer to the urban profile showing land-use zones and photographs that show examples of land use in these zones. Give evidence "
        "that the land use in B2 is a high-income residential area.", 2,
        [["Rural-urban fringe"], ["Plots", "Stands"], ["Houses are large", "Low density of buildings", "Density"],
         ["Away from the industries", "Far from the industries"], ["Architecture"], ["Cars", "Garages"], ["Wide roads", "Wide streets"],
         ["Gardens", "Trees", "Aesthetically appealing"], ["Away from the CBD", "Far from the CBD"], ["Security walls", "Walls"]],
        ["Look at the photograph of B2 and where B2 is on the profile.", "Size of houses and plots, gardens, distance from industry."]),
    mcq("1.4.3(b)", "Is the land use at A a heavy or a light industry?", ["Heavy", "Light"], 0,
        ["The photograph shows tall chimneys and smoke.", "Large plants that process raw materials."]),
    rub("1.4.4", "Explain TWO economic reasons why this land use (answer to QUESTION 1.4.3 (b)) is located on the outskirts of the urban area, as "
        "indicated in the urban profile.", 4, [
        "Availability of cheaper land (2).", "It is cheaper to build on flat land (2).", "Less expensive to combat pollution (2).",
        "Close to bulk transport (2).", "Close to the labour force (2).", "Lower fuel costs (2).", "Close to raw materials (2)."],
        ["Economic reasons are about costs.", "Land, transport, labour, pollution control."], each=2),
    rub("1.4.5", "Why is the land use at B2 not located close to the land use at A?", 4, [
        "The two land uses are incompatible (2).", "Preserves the aesthetics of the land use (accept examples) (2).",
        "Maintains the high value of land/property (2).", "To reduce the impact of pollution (accept examples) (2).", "Alleviates traffic congestion (2).",
        "Reduces health risks (accept examples) (2).",
        "Accept responses from A (heavy industries): the two land uses are incompatible; decreases aesthetic appeal; decreases the value of "
        "land/property; increases the impact of pollution; more traffic congestion; increases health risks (2 each)."],
        ["B2 is a high-income residential area; A is heavy industry.", "Think noise, smoke, traffic and property values."], each=2)]
q15 = [
    lst("1.5.1", "What evidence in the photograph suggests that urban blight/decay has taken place?", 1,
        [["Neglected buildings", "Dilapidated buildings"], ["Broken windows"], ["Graffiti on the walls", "Graffiti"],
         ["Litter in the streets", "Rubbish in the streets", "Litter", "Rubbish"]],
        ["Look at the building's walls and windows.", "And at the street."]),
    lst("1.5.2", "State TWO social causes of urban blight/decay.", 2,
        [["Unemployment"], ["Poverty"], ["Affordable housing", "Housing"], ["Abandoned buildings"], ["Illegal occupation", "Illegal occupants"],
         ["Landlords not interested in upgrading", "Landlords"], ["Service delivery"]],
        ["Social causes are about people's living conditions.", "Jobs, money, housing, services."]),
    rub("1.5.3", "Suggest possible reasons why the municipality of Cape Town has not attended to this issue of urban blight/decay in Wynberg.", 4, [
        "Lack of finances (2).", "Mismanagement of funds (accept examples) (2).", "People fail to pay municipality bills (2).",
        "The municipality has other urgent priorities (accept examples) (2).", "Lack of skills/capacity (accept examples) (2).",
        "Illegal occupation of buildings (2).", "The buildings are privately owned (2)."],
        ["Fixing an area costs money.", "Whose buildings are they, and who lives in them?"], each=2),
    rub("1.5.4", "In a paragraph of approximately EIGHT lines, explain the positive impact of urban renewal on the economy of Wynberg.", 8, [
        "Attracts more businesses/investors (accept examples) (2).", "Attracts more customers (accept examples) (2).", "Attracts more tourists (2).",
        "Influences the multiplier effect (accept examples) (2).", "Creates more job opportunities (accept examples) (2).", "Upskills workers (2).",
        "Increases the value of properties (2).", "Improves infrastructure (accept examples) (2)."],
        ["Renewal makes the area attractive again.", "Who comes back, and what does that do for jobs and money?"], each=2)]

# ---- QUESTION 2: ECONOMIC GEOGRAPHY OF SOUTH AFRICA, the question paper pages 10-16 and the memo pages 8-11 ----
q21 = [
    mcq("2.1.1", "QUESTIONS 2.1.1 to 2.1.4 are based on sugar cane farming in KwaZulu-Natal. … is a positive social factor of sugar cane production "
        "in KwaZulu-Natal.", ["Earning foreign exchange", "Provision of employment", "Stimulation of industrial production", "Contribution to the GDP"], 1,
        ["Social: about people, not the economy as a whole.", "Which option affects households directly?"]),
    mcq("2.1.2", "… is/are a negative economic factor hindering sugar cane farming in KwaZulu-Natal.",
        ["Floods", "Lack of access to capital", "Shortage of large-scale farmers", "Crime"], 1,
        ["Economic: about money.", "Floods are physical; crime is social."]),
    mcq("2.1.3", "TWO advantages of sugar cane farming for the economy of South Africa is/are … and …\n(i) contributing to the gross domestic product (GDP)\n"
        "(ii) fluctuating prices\n(iii) development of infrastructure\n(iv) retrenchment of workers",
        ["(i) and (iv)", "(ii) and (iv)", "(i) and (iii)", "(iii) and (iv)"], 2,
        ["Advantages are positives.", "Fluctuating prices and retrenchments are problems."]),
    mcq("2.1.4", "Climatic factors that favour KwaZulu-Natal as the highest producer of sugar cane in South Africa is/are … and …\n(i) high temperatures\n"
        "(ii) low rainfall\n(iii) high rainfall\n(iv) low temperatures", ["(i) and (ii)", "(iii) and (iv)", "(i) and (iii)", "(ii) and (iv)"], 2,
        ["KwaZulu-Natal's coast is subtropical.", "Sugar cane needs heat and water."]),
    mcq("2.1.5", "QUESTIONS 2.1.5 to 2.1.8 are based on gold mining in South Africa. The province that produces the most gold in South Africa is …",
        ["Limpopo.", "Mpumalanga.", "KwaZulu-Natal.", "Gauteng."], 3,
        ["Johannesburg was built on the gold reefs.", "The Witwatersrand."]),
    mcq("2.1.6", "The number of people employed in South African gold mines decreased the most between …",
        ["1995 and 2000.", "2000 and 2005.", "2005 and 2010.", "2010 and 2015."], 0,
        ["Find the steepest part of the line.", "Compare the drop in each five-year step."], figure=fig("2.1", GOLD)),
    mcq("2.1.7", "A physical (natural) factor causing employment numbers to decrease in South African gold mines is/are …",
        ["threats of nationalisation.", "depletion of gold in mines.", "unskilled labourers.", "less foreign investment in mines."], 1,
        ["Physical: about nature, not people or money.", "What happens to a reef after a century of mining?"], figure=fig("2.1", GOLD)),
    mcq("2.1.8", "An economic factor that has caused employment numbers to decrease from 2015 onwards is/are …",
        ["HIV and Aids.", "fluctuating prices of gold.", "environmental degradation.", "strikes and protests."], 1,
        ["Economic: about money and markets.", "What happens to mines when the gold price falls?"], figure=fig("2.1", GOLD))]
q22a = [
    mcq("2.2.1", "… is a secondary economic activity.", ["Transport", "Manufacturing"], 1,
        ["Secondary activities process raw materials.", "Transport is a service."]),
    mcq("2.2.2", "Primary economic activities accounted for … of the gross domestic product (GDP).", ["8,4%", "11,3%"], 1,
        ["Primary: taken directly from nature.", "Add agriculture and mining."]),
    mcq("2.2.3", "… makes the largest contribution to the tertiary sector.", ["Finance and real estate", "Construction"], 0,
        ["Construction is secondary.", "Find the biggest service in the table."]),
    mcq("2.2.4", "The … sector was the greatest contributor to the gross domestic product (GDP) in 2024.", ["secondary", "tertiary"], 1,
        ["Add up the services.", "Finance, trade, transport and government are all services."])]
q22b = [
    mcq("2.2.5", "The sketch below illustrates …", ["balance of trade", "domestic trade"], 0,
        ["The scale weighs imports against exports.", "Trade between countries."],
        figure=fig("2.2.5", "A sketch of a pair of scales: one pan labelled Imports, the other Exports.")),
    mcq("2.2.6", "A factor that advantages international trade", ["trade tariffs", "well-developed infrastructure"], 1,
        ["Tariffs are taxes on imports.", "What makes moving goods easier?"]),
    mcq("2.2.7", "… is an economic benefit of international trade.", ["Access to foreign currencies", "Closing down of local industries"], 0,
        ["A benefit is a positive.", "Exports earn ..."])]
q23 = [
    rub("2.3.1", "Define the concept food insecurity.", 2, [
        "The condition of not having access to sufficient nutritious food (2). Accept: do not have (sufficient) nutritious food (1)."],
        ["It is the opposite of food security.", "Access to enough nutritious food."], each=2),
    num("2.3.2", "According to the extract, what percentage of households suffered from food insecurity in 2024?", 25.8, 0.05, "%",
        ["Read the first paragraph of FOOD SECURITY IN SOUTH AFRICA.", "Households facing moderate to severe food insecurity."]),
    rub("2.3.3", "What evidence in the photograph on large-scale farming suggests that it would have a positive impact on food production?", 2, [
        "Large tracts of land are cultivated (2).", "Use of machinery/a tractor/technology (accept examples) (2).",
        "Scientific methods are used (accept examples) (2).", "Use of pesticides (2)."],
        ["Look at the size of the field and what is working it.", "One piece of evidence, explained."], each=2),
    lst("2.3.4", "Refer to the graph. Identify TWO economic challenges that small-scale farmers would more likely experience than large-scale farmers.", 2,
        [["Farming equipment", "Equipment", "Technology"], ["Finance", "Money", "Capital"], ["Arable land", "Land"]],
        ["The graph compares three kinds of access.", "Small-scale farmers have the shorter bars."]),
    rub("2.3.5", "In a paragraph of approximately EIGHT lines, explain how these economic challenges identified in your answer to QUESTION 2.3.4 can have "
        "a negative impact on food production.", 8, [
        "Equipment/technology: lack of machinery will reduce efficiency/productivity (2). Part mark: lack of machinery (1).",
        "Equipment/technology: limited cultivation of land, hence less food is produced (2). Part mark: limited cultivation of land (1).",
        "Equipment/technology: manual labour is less efficient, leading to lower crop yields (2). Part mark: manual labour is less efficient (1).",
        "Equipment/technology: delays in planting/harvesting impact crop quality/market access (2). Part mark: delays in planting/harvesting (1).",
        "Equipment/technology: crop diversity is reduced, resulting in less nutritious options (2). Part mark: crop diversity is reduced (1).",
        "Equipment/technology: a lack of hybrid/genetically modified seeds exposes crops to the negative elements of weather (2). Part mark: lack of "
        "hybrid seeds/genetically modified seeds (1).",
        "Equipment/technology: limited use of pesticides will make crops vulnerable to insects/pests (2). Part mark: limited use of pesticides (1).",
        "Equipment/technology: a lack of vaccination/dipping tanks exposes livestock to diseases (2). Part mark: lack of vaccination/dipping tanks (1).",
        "Equipment/technology: ineffective farming methods reduce crop production (2). Part mark: ineffective farming methods (1).",
        "Equipment/technology: a lack of transport/storage will cause produce to spoil (2). Part mark: lack of transport/storage (1).",
        "Finance: financial institutions will not grant loans, so they will not be able to purchase seeds/equipment (2). Part mark: financial "
        "institutions will not grant loans to small-scale farming (1).",
        "Finance: farmers will not generate finance and therefore not provide sufficient food to sell (2). Part mark: small-scale farmers will not be "
        "able to provide enough food (1).",
        "Finance: they cannot afford labour costs, resulting in less food production (2). Part mark: they would not afford labour costs (1).",
        "Finance: limited access to finance reduces the sustainability of farms (accept examples) (2). Part mark: limited access to finance (1).",
        "Arable land: less arable land reduces food production (2). Part mark: less arable land (1).",
        "Arable land: crop diversity is hampered by limited arable land (2). Part mark: crop diversity is hampered (1).",
        "Arable land: limited opportunity for expansion due to a lack of arable land (2). Part mark: limited opportunity for expansion (1).",
        "Arable land: overgrazing of land due to a lack of arable land (2). Part mark: overgrazing of land (1)."],
        ["Take each challenge you named in 2.3.4 in turn.", "Link it to less food: lower yields, less land planted, crops lost."], each=2)]
q24 = [
    term("2.4.1", "In which province is the Dube Trade Port (IDZ) located?", ["KwaZulu-Natal", "KZN"],
         ["It is near Durban.", "King Shaka International Airport is there too."]),
    rub("2.4.2", "Quote evidence from the extract that indicates that the Dube Trade Port (IDZ) has a variety of manufacturing industries.", 2, [
        "'The automotive industry would join the electronic, high-value manufacturing, food processing and fibre optics sectors' (2)."],
        ["Quote: copy the words exactly.", "Find the sentence that lists several sectors."], each=2),
    rub("2.4.3", "According to the extract, why is the Dube Trade Port classified as an industrial development zone (IDZ)?", 2, [
        "Direct links to the airport/harbour (2).", "(Foreign) investment (2).", "Creates jobs (2)."],
        ["An IDZ is built to attract industry.", "What does the extract say it attracts?"], each=2),
    rub("2.4.4", "How did the proximity (distance) to the airport and harbour favour the location of the automotive plants in the Dube Trade Port (IDZ)?", 4, [
        "Lower transport costs (2).", "The airport/harbour is easily accessible (accept examples) (2).", "Access to international markets (2).",
        "Reduces costs for exports/imports (accept examples) (2)."],
        ["Car parts come in and cars go out.", "Think cost and markets."], each=2),
    rub("2.4.5", "Explain how the variety of manufacturing industries in the Dube Trade Port (IDZ) would have a positive impact on the economy of the province.", 6, [
        "Upskilling of local communities will provide a variety of employment opportunities (2). Part mark: upskilling of local communities (1).",
        "Upskilling would result in higher income and greater buying power (2).",
        "The multiplier effect will lead to more employment opportunities (2). Part mark: the multiplier effect (1).",
        "Different types of industries in one area will attract investors (2). Part mark: different types of industries in one area (1).",
        "Improved infrastructure will attract more businesses (2). Part mark: improved infrastructure (1).",
        "More link industries, increasing employment opportunities (2). Part mark: more link industries (1).",
        "Export of these products would increase port tariffs (2). Part mark: export of these products (1).",
        "Foreign investment contributes to the GGP (Gross Geographic Product) (2). Part mark: foreign investments (1)."],
        ["Many industries in one place create jobs and attract more.", "Think multiplier effect, skills, investment, exports."], each=2)]
q25 = [
    rub("2.5.1", "What is the informal sector?", 2, [
        "Businesses that are not registered and do not pay income tax (2). Part marks: businesses that are not registered (1); they do not pay "
        "income tax (1)."],
        ["Informal: not formally registered.", "And what do they not pay?"], each=2),
    lst("2.5.2", "Why is the informal trader in the photograph found on the main road?", 1,
        [["Accessible to potential customers", "Potential customers", "Customers pass by", "Accessible to customers"]],
        ["Who walks and drives along a main road?", "Traders go where the buyers are."]),
    lst("2.5.3", "State TWO challenges that this informal trader is likely to experience with the type of goods being sold.", 2,
        [["Storage", "No storage"], ["Rot", "Rotting", "Perishable"], ["Stolen", "Theft"],
         ["Insects", "Pests"], ["Harsh weather conditions", "Weather"], ["Competition"]],
        ["The trader sells fruit and vegetables.", "Fresh goods, outdoors, next to a road."]),
    rub("2.5.4", "Refer to the table. Account for the large number of informal traders during the month of December.", 2, [
        "The holiday season increases shoppers (2).", "More tourists, hence more potential customers (2).",
        "The buying power of locals increases due to extra income/bonuses (2).", "People have additional income (during the festive season) (accept examples) (2)."],
        ["December is the festive season.", "More buyers, more money to spend."], each=2),
    rub("2.5.5", "How will the municipality of Richards Bay benefit by issuing permits to informal traders?", 4, [
        "They would be able to regulate the sector (accept examples) (2).",
        "This information can be used to set up ideal locations for informal traders (accept examples) (2).", "It would increase their revenue base (2).",
        "Monitor the quality of goods being sold (accept examples) (2).", "Monitor health and safety conditions (accept examples) (2)."],
        ["A permit is a record and a fee.", "Control and money."], each=2),
    rub("2.5.6", "What can the municipality of Richards Bay provide to the informal traders with the money collected from the issuing of permits?", 4, [
        "Designate areas for trade (2).", "Provide infrastructure (accept examples) (2).", "Provide storage facilities (accept examples) (2).",
        "Effective policing (accept examples) (2).", "Facilitate partnerships with the formal/private sector (accept examples) (2).",
        "Upskilling entrepreneurial programmes (accept examples) (2).", "Access to funding (accept examples) (2).",
        "Provision of basic services (accept examples) (2)."],
        ["Think of what the trader in the photograph lacks.", "Shelter, storage, safety, skills."], each=2)]

# ---- QUESTION 3 (SECTION B): only the parts that do not read the maps, the question paper pages 17-20 and the memo pages 12-13 ----
q3a = [
    rub("3.1.3", "Why is the measurement of the breadth on the topographical map smaller than that on the orthophoto map?", 1, [
        "The scale of the topographical map is (5x) smaller (1).", "OR — The scale of the orthophoto map is (5x) larger (1)."],
        ["The topographical map is 1:50 000, the orthophoto map 1:10 000.", "Which shows the same ground smaller?"]),
    rub("3.1.5", "Why is it important to calculate the current magnetic declination?", 1, ["To determine the correct position of true north (1)."],
        ["Magnetic north moves a little every year.", "A compass bearing must be corrected to ..."]),
    term("3.2.6", "Refer to the opencast mining taking place at H in block D1 on the topographical map and the general information. What mineral is mined "
         "at the opencast mine?", ["Coal"], ["eMalahleni means 'place of coal'.", "Read the general information."]),
    rub("3.2.8", "Refer to the industries at I in block C3 on the topographical map. What are the economic advantages of these industries for the local "
        "population?", 2, [
        "Provide employment opportunities (2).", "Increases buying power/the multiplier effect (2).", "Upskilling of people in the local community (2).",
        "Access to goods (2).", "Access to improved infrastructure (2)."],
        ["Industries need workers.", "Jobs bring income, and income is spent locally."], each=2)]
q3b = [
    rub("3.3.1", "What is data layering?", 2, ["Layers of information that are placed on top of one another (2)."],
        ["GIS builds a map from several kinds of data.", "Each kind on its own 'sheet', stacked."], each=2),
    term("3.3.2", "Name the data layer at B (in the sketch above) as it is represented on the topographical map.", ["Drainage", "Drainage layer"],
         ["Layer B shows non-perennial water.", "Rivers, dams and pans make up the ... layer."]),
    draw("3.3.3", "Redraw layer C in the sketch above in your ANSWER BOOK. Apply the data layers of A and B to the sketch.", 3, [
        ["The row of trees (the dots of layer A) drawn on layer C", 1], ["The woodland (the shaded patches of layer A) drawn on layer C", 1],
        ["The non-perennial water (layer B) drawn on layer C", 1]],
        ["Layer C is the sum: A + B = C.", "Copy each feature to the same place on C."])]

MOLETELE = ("MOLETELE CITRUS FRUIT FARM SHOWCASING THE SUCCESS OF A LAND RESTITUTION PROGRAMME IN LIMPOPO\n\nThe Moletele community opted to take their "
            "land back and this has resulted in a successful land restitution programme. The newest agricultural technology and rows of well-maintained "
            "citrus trees at Moletele Farm in Hoedspruit are clear indicators of this success.\n\nThe lime-producing farm in Hoedspruit is a joint venture "
            "project of the Moletele communal property association (holding a 51% stake) and the established commercial fruit producer Komati Fruit Group."
            "\n\nA total of 30 permanent and 60 temporary jobs have already been created. The programme transfers skills to the workforce and community. "
            "Proceeds are given to thousands of families in the Moletele community.\n\nA bursary scheme makes it possible for profits to be used in the "
            "education of children in the community. The restitution programme includes profit sharing. This makes it possible to invest back into the business.")
WYNBERG = ("URBAN BLIGHT/DECAY IN WYNBERG, CAPE TOWN\n\nOver the past decade, business owners have felt helpless as they watched on as the buildings and "
           "services in the area have gradually deteriorated. They have tried to get the municipality of Cape Town to take action, but their cries seem to "
           "have gone unheard as the issue of urban blight/decay remains unresolved.\n\nLeif Petersen, co-director for Sustainable Livelihoods Foundation, "
           "whose offices are along the road (shown in the photograph), said that Ebor Road has been in a state of decay for more than a decade. The living "
           "conditions in the buildings are terrible – there are illegal water and electricity connections and people sleeping in squalor (filth).\n\n"
           "'A small, committed group of business owners, including ourselves, have invested time, effort and money in our attempts to implement urban renewal.'")
FOOD = ("FOOD SECURITY IN SOUTH AFRICA\n\nSouth Africa has a complex food security situation, with millions of people experiencing food insecurity. In 2024, "
        "25,8% of households faced moderate to severe food insecurity.\n\nBoth large-scale and small-scale farming are important contributors to food "
        "security in South Africa. However, large-scale farmers are often seen as the main drivers of national food security. They can contribute to food "
        "security in the region through increased production of agricultural products.\n\nSmall-scale farmers are important drivers of household food "
        "security. The government has implemented programmes to support small-scale farmers, including financial assistance, training and market access."
        "\n\nDespite these efforts, food insecurity remains a challenge for many South Africans.")
DUBE = ("DUBE TRADE PORT (IDZ) ATTRACTS INVESTMENTS FROM THE AUTOMOTIVE INDUSTRY\n\nThe Dube Trade Port (IDZ) has seen positive economic investments in "
        "August 2024 as major automotive (car) companies pledged investment and have set up business in this industrial development zone (IDZ).\n\nThe "
        "automotive industry would join the electronic, high-value manufacturing, food processing and fibre optics sectors at the Dube Trade Port (IDZ)."
        "\n\nAuto Investment Holdings Group and Mahindra (South Africa) revealed a new assembly plant. Construction of the new assembly plant is expected to "
        "be completed in 2025. The company would expand its staff to complement the growing production volumes, as they currently have 90 staff on the "
        "assembly line.\n\nOgihara South Africa is a new joint venture between Toyota Tsusho Africa, Ogihara (Thailand) Corporation and Toyota South "
        "Africa Motors. They have pledged a R1,2 billion investment among themselves. These companies are building a facility at the Dube Trade Port (IDZ) "
        "to manufacture parts for their current and future vehicles.\n\nThe Dube Trade Port (IDZ) is located in the same vicinity as the King Shaka "
        "International Airport, 30 minutes from Africa's busiest cargo port, Durban Harbour, and 34 minutes (41 km) from the Durban-Pinetown industrial region.")
INFORMAL = ("GIVE THE INFORMAL SECTOR A BREAK\n\nInformal traders are part of the informal sector. Everyone in town has become familiar with the sight of "
            "informal traders on the main road in Richards Bay. Most of these informal traders are women without any other income other than selling their "
            "goods next to the road.\n\nHowever, during the December holidays, which is normally peak season for informal traders, the municipality fined "
            "all of these traders R300 each for selling goods without permits. As it is the only income for some of the informal traders, their income will "
            "now take a huge knock. Selling fruit/vegetables/cooked food only twice a week will not cover monthly bills, and some of them are faced with hard "
            "times ahead.")
EMALAHLENI = ("GENERAL INFORMATION ON eMALAHLENI (WITBANK)\n\nCoordinates: 25°50′S; 29°10′E\n\neMalahleni (previously known as Witbank) is a city situated "
              "on the Highveld of Mpumalanga, South Africa.\n\neMalahleni is in a coal mining area. Opencast mining is mainly used to extract coal. This type "
              "of mining involves digging near the surface to extract coal seams. There are a number of power stations, as well as a steel mill nearby which "
              "all require coal.\n\nThe farmland surrounding eMalahleni is being bought by investors, coal mining companies and real estate developers to "
              "accommodate the rapid growth of the city, which is good for local businesses and residents. The region experiences highly polluted air due to "
              "the coal mining and power stations.")
GDP = {"head": ["ECONOMIC ACTIVITY", "PERCENTAGE (%) CONTRIBUTION TO THE GDP"],
       "rows": [["Transport", "11"], ["Agriculture", "2,9"], ["Mining", "8,4"], ["General government services", "10,6"], ["Electricity and gas", "2,8"],
                ["Construction", "3"], ["Trade, catering and accommodation", "14,7"], ["Manufacturing", "15"], ["Finance and real estate", "31,7"]]}
TRADERS = {"head": ["MONTH (2024)", "NUMBER OF INFORMAL TRADERS (RICHARDS BAY CBD)"],
           "rows": [["January", "35"], ["February", "22"], ["March", "38"], ["April", "24"], ["May", "22"], ["June", "42"], ["July", "35"],
                    ["August", "29"], ["September", "46"], ["October", "49"], ["November", "58"], ["December", "60"]]}
COLS = "Complete the statements in COLUMN A with the options in COLUMN B."
sec_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Rural settlements", "marks": 7, "lead": COLS, "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Urban settlements", "marks": 8,
     "lead": "Various options are provided as possible answers to the following questions based on concepts and classification of urban settlements.",
     "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Rural depopulation and land restitution", "marks": 15,
     "lead": "Refer to the graph below showing the percentage of rural population in South Africa from 2017 to 2024 and the extract on land restitution.",
     "extract": MOLETELE,
     "figure": fig("1.3", "A bar graph, PERCENTAGE OF RURAL POPULATION IN SOUTH AFRICA: 2017 34,66; 2018 34,16; 2019 33,65; 2020 33,14; 2021 32,65; "
                   "2022 32,15; 2023 31,67; 2024 31,18."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Urban land-use zones", "marks": 15,
     "lead": "Refer to the urban profile depicting urban land-use zones and the photographs showing urban land-use below.",
     "figure": fig("1.4", "An urban profile from left to right: A, industrial zone (factories with chimneys); B1, residential; C, transition zone; "
                   "D, CBD (the tallest buildings); C; B2, residential with trees; E, rural-urban fringe. KEY: A industrial zone, B residential zone, "
                   "C transition zone, D CBD, E rural-urban fringe. Below, a photograph from A: a large factory with tall chimneys and smoke; and one "
                   "from B2: large houses on big plots with gardens and trees."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Urban blight and renewal", "marks": 15,
     "lead": "Refer to the extract and photograph below on urban blight/decay.", "extract": WYNBERG,
     "figure": fig("1.5", "A photograph of an old building along a street: dirty walls covered in graffiti, broken windows, rubbish and belongings "
                   "piled against the wall."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Primary economic activities", "marks": 8,
     "lead": "Various options are provided as possible answers to the following questions on primary economic activities.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Economic sectors", "marks": 4,
     "lead": COLS + " Use the table of the contributions (%) made to the gross domestic product (GDP) during 2024.", "table": GDP, "items": q22a},
    {"id": "2.2.5", "title": "Question 2.2.5", "kind": "International trade", "marks": 3, "lead": COLS, "items": q22b},
    {"id": "2.3", "title": "Question 2.3", "kind": "Food security", "marks": 15,
     "lead": "Refer to the infographic below on food security and small/large-scale farming.", "extract": FOOD,
     "figure": fig("2.3", "An infographic. Photographs: large-scale farming (a tractor spraying long rows of crops in a wide field) and small-scale "
                   "farming (people working a small plot with hand hoes). The FOOD SECURITY text. A bar graph, MAJOR CHALLENGES EXPERIENCED BY SMALL- "
                   "AND LARGE-SCALE FARMERS IN SOUTH AFRICA (percentage): access to farming equipment/technology, small-scale 19,2 and large-scale "
                   "80,8; access to finance, 6,9 and 93,1; access to arable land, 25 and 75."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Industrial development zones", "marks": 15,
     "lead": "Refer to the extract and map below on the Dube Trade Port Industrial Development Zone (IDZ).", "extract": DUBE,
     "figure": fig("2.4", "A map of the coast near Durban: the Durban-Pinetown Industrial Region; Dube Transport to the north; Durban Harbour 30 km "
                   "south of it; Toyota SA 22 km south of the harbour; the ocean to the east."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "The informal sector", "marks": 15,
     "lead": "Refer to the infographic below on the informal sector (Richards Bay – informal trader on main road).", "extract": INFORMAL, "table": TRADERS,
     "figure": fig("2.5", "A photograph of an informal trader's table on the main road in Richards Bay, piled with fruit (bananas) and vegetables "
                   "(tomatoes)."), "items": q25},
]
sec_b = [
    {"id": "3", "title": "Question 3", "kind": "Geographical skills and techniques", "marks": 5,
     "lead": "The parts of Question 3 that do not read the topographical or orthophoto map. The topographical map is 1:50 000 and the orthophoto "
             "map 1:10 000.", "extract": EMALAHLENI, "items": q3a},
    {"id": "3.3", "title": "Question 3.3", "kind": "Geographical information systems (GIS)", "marks": 6,
     "lead": "GEOGRAPHICAL INFORMATION SYSTEMS (GIS): refer to the sketch below.",
     "figure": fig("3.3", "A data-layering sketch of three stacked sheets: A, the vegetation layer, with shaded patches (woodland) and a line of dots "
                   "(a row of trees); B, a layer named '… layer', with a shaded patch labelled non-perennial water; C, the data layering sheet, blank. "
                   "A + B = C."), "items": q3b},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Geography", "title": "Geography P2", "sitting": "November 2025", "total_marks": 131, "time": "3 hours"},
    "sections": [{"title": "Section A: Rural and urban settlement and economic geography of South Africa", "total": 120, "missions": sec_a},
                 {"title": "Section B: Geographical skills and techniques", "total": 11, "missions": sec_b}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "Section A whole and the map-free parts of Section B, hand-transcribed from the paper and "
                                                           "memo PDFs and their page images; no API call."},
        {"n": "3", "kind": "no_fit", "detail": "Section B reads the 1:50 000 topographical map 2529CC eMALAHLENI (WITBANK) and the 1:10 000 orthophoto "
                                               "map 2529 CC 15, handed out in the exam room: not in the question paper and not published. Its 19 "
                                               "marks that read them (3.1.1, 3.1.2, 3.1.4, 3.2.1-3.2.5, 3.2.7, 3.3.4) wait for the maps; the paper "
                                               "totals the 131 marks that can be played (the printed paper: 150)."},
        {"n": "1.3.3", "kind": "no_fit", "detail": "Part marks (one mark for a point stated without its explanation) are folded into each memo point "
                                                   "for the written-answer marker (2.3.5, 2.4.5, 2.5.1); 2.3.5's 'minimum of two challenges' is not "
                                                   "enforced."},
        {"n": "3.3.3", "kind": "no_fit", "detail": "The redrawn layer C is drawn on paper and self-checked against the memo's criteria."},
        {"n": "paper", "kind": "memo_issue", "detail": "The memo's page 3 is a marked sample from another paper (its answers, e.g. 1.1.1 'South "
                                                       "Atlantic High' and 1.2.1 'Melting snow', match nothing here): ignored."},
        {"n": "3.1.4", "kind": "memo_issue", "detail": "Not played (it reads the map), but its memo writes 18°19′ + 55′ = '18°74′' before converting "
                                                       "to 19°14′ west of true north."},
    ],
}
out = Path(__file__).parent / "out" / "geo-p2-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Section A whole; Section B's parts that do not read the maps"}, "paper": paper},
                                              indent=1, ensure_ascii=False), encoding="utf-8")
for s in paper["sections"]:
    for m in s["missions"]:
        got = sum(i["marks"] for i in m["items"])
        assert got == m["marks"], (m["id"], got, m["marks"])
        print(m["id"], "parts:", len(m["items"]), "marks:", got)
print("total:", sum(i["marks"] for s in paper["sections"] for m in s["missions"] for i in m["items"]))
