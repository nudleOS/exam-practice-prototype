"""Geography P2 Nov 2024: SECTION A whole (Questions 1 and 2, 120 marks) and the parts of SECTION B (Question 3) that do not read
the maps (8 marks), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the memo's points are the paper's and the
memo's own; clues and figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_geo_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Geography P2 Nov 2024 Eng.pdf" "<...>/Geography P2 Nov 2024 MG Eng.pdf" --id geo-p2-2024-11 --from-json

SECTION B reads a 1:50 000 topographical map (2926AA BLOEMFONTEIN-NOORD) and a 1:10 000 orthophoto map (2926AA 10) handed out in the
exam room: not in the question paper and not published. Its 22 marks that read the maps (3.1.3-3.1.7, 3.2.1-3.2.4, 3.3.3) wait for the
maps; the paper totals what is playable, 128.

The memo's shapes map as in Geography P1 Nov 2024 (transcribe_geo_p1_2024_11.py). New here: a memo that accepts EITHER option (1.1.8
"Y/Z") is a pick of one from a pool holding both; a quote from an extract is a pick of the extract's sentence (2.4.2, 2.5.2).
Figure boxes are measured in PDF points (page 595.32 x 841.92), found with scratchpad figs24.py and checked on rendered crops; `inset`
where a label touches the crop's top-left corner (the page's Hide button sits there)."""
import json
from pathlib import Path

W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.3": [5, 59, 124, 527, 395], "1.4": [6, 63, 110, 523, 305], "1.5": [7, 52, 140, 534, 298], "2.1": [8, 60, 345, 578, 471],
    "2.3": [10, 52, 120, 534, 347], "2.4": [11, 97, 387, 532, 694], "2.5": [13, 120, 352, 478, 591]}
INSET = {"1.5": 40, "2.1": 40, "2.3": 40, "2.4": 40, "2.5": 40}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"inset": INSET[name]} if name in INSET else {})}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None, must=None, notes=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {}), **({"notes": notes} if notes else {})}


def pick1(n, q, opts, pool, clues, marks=1):
    """Choose ONE: every index in `pool` is right (a memo that accepts more than one answer, or one quote among sentences)."""
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": 1}


def sentences(text):
    """An extract's sentences, as printed (each ends with a full stop)."""
    return [s.strip().rstrip(".") + "." for s in text.split(". ") if s.strip()]


term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}

FARMS = ("Four photographs. P: a combine harvester cutting a large wheat field. Q: a herd of cattle grazing in a large field. R: a "
         "centre-pivot irrigation system spraying a large field of crops. S: two people carrying buckets, watering a small vegetable "
         "plot by hand on a hillside.")
INFORMAL = ("UPGRADING OF INFORMAL SETTLEMENTS\n\nInformal settlements are generally located on any vacant land that is available. Informal "
            "settlements are characterised by a lack of basic services, pollution, overcrowding and poor waste management that impact "
            "negatively on the environment and poses a health risk. In spite of this, the number of informal settlements is growing.\n\nWhat are "
            "the solutions to informal settlements? Rather than disrupting important social and economic networks by uprooting and relocating "
            "residents, upgrading programmes would be associated with social benefits for the people in informal settlements. Such programmes "
            "can improve neighbourhood infrastructures, while low-income residents remain on site.\n\nUpgrading informal settlements creates "
            "income-generating opportunities that can directly benefit local companies and residents. This is particularly helpful for workers "
            "if jobs are created within the community. In many cases, young people within these settlements will be directly employed in "
            "upgrading projects.")
COAL = ("The high-quality coal reserves in South Africa have been decreasing over the years.\n\nShallow and high-quality resources in the "
        "Emalahleni (Witbank) coal field have been depleted. Mining companies are required to find other more cost-effective methods to "
        "extract the deeper, low quality coal seams of the basin.")
GAUTENG_1 = ("Gauteng (PWV) is the biggest contributor to South Africa's gross domestic product (GDP). Gauteng's (PWV) most important "
             "economic sectors are financial and business services, logistics and communications, manufacturing, property, telecommunications "
             "and trade.")
GAUTENG_2 = ("About 10 000 businesses involved in the province's manufacturing sector employ over half a million people. The economy of the "
             "province is moving away from traditional heavy industry markets and low value-added production* to sophisticated high value-added "
             "production**, particularly in information technology, telecommunications and other high-tech industries.")
GAUTENG = ("CHANGE IN GAUTENG'S (PWV) MANUFACTURING SECTOR\n\n" + GAUTENG_1 + "\n\n" + GAUTENG_2 + "\n\nGLOSSARY\n*Low value-added production: "
           "basic production that uses traditional technology and manual labour to operate machinery\n**High value-added production: production "
           "that uses advanced technology, is highly efficient, e.g. robotics to operate machinery")
TRADE_1 = "Trading in the informal sector has always been a part of South Africa's economy, 30% of which occurs in Johannesburg."
TRADE_2 = ("The city of Johannesburg has informal trading by-laws that currently regulate trading in the informal sector. The municipality may "
           "declare any place to be an area in which informal trading is restricted or prevented. The restrictions include traders sleeping "
           "overnight as it exposes them to criminal activity. Anyone not complying with these regulations can be charged a fine of up to R500.")
TRADE_3 = ("Car window washers and other informal traders are part of a large group of poor South Africans who have been economically excluded "
           "and who are trying to find their own way to support their families. Human rights lawyers have said that certain regulations could be "
           "'punishing people just for being poor'.")
TRADE = "REGULATING TRADING IN THE INFORMAL SECTOR\n\n" + TRADE_1 + "\n\n" + TRADE_2 + "\n\n" + TRADE_3

# ---- QUESTION 1: RURAL AND URBAN SETTLEMENTS, the question paper pages 3-7 and the memo pages 4-7 ----
q11 = [
    mcq("1.1.1", "Exact piece of land that a settlement is built on", ["situation", "site"], 1,
        ["One word describes the land itself, the other its position compared with what is around it.", "The ground a settlement stands on."]),
    mcq("1.1.2", "The situation of a commercial livestock farm is influenced by ...", ["topography", "markets"], 1,
        ["Situation is about a place's position relative to other places.", "Where does a commercial farmer sell the animals?"]),
    mcq("1.1.3", "Settlements located close to a water source in arid areas", ["wet-point", "dry-point"], 0,
        ["In a dry area people settle where there IS water.", "Dry-point settlements avoid flooding."]),
    mcq("1.1.4", "The shape of this settlement is influenced by a river", ["circular", "linear"], 1,
        ["A river runs in a line.", "Houses built along it form a line too."]),
    mcq("1.1.5", "The largest rural settlement type", ["village", "hamlet"], 0,
        ["Isolated farmstead, hamlet, village.", "A hamlet is a handful of houses."]),
    mcq("1.1.6", "Greater profits are associated with this settlement pattern", ["dispersed", "nucleated"], 0,
        ["Commercial farms are large and far apart.", "Spread-out farms have room to produce more."]),
    mcq("1.1.7", "Land returned to the original owners", ["land restitution", "land tenure"], 0,
        ["Land tenure is about how land is held.", "Restoring land taken away is ..."]),
    pick1("1.1.8", "An economic challenge of land reform", ["poverty", "legal disputes"], [0, 1],
          ["Land reform has social, economic and legal challenges.", "Choose one."])]
q12 = [
    mcq("1.2.1", "The smallest urban settlement in an urban hierarchy is a ...", ["city.", "metropolis.", "town.", "megalopolis."], 2,
        ["Order them from small to large.", "Town, city, metropolis, conurbation, megalopolis."]),
    mcq("1.2.2", "A ... has the smallest number of settlements.", ["conurbation", "city", "town", "megalopolis"], 3,
        ["The higher the order, the fewer there are.", "The very largest urban settlement is the rarest."]),
    mcq("1.2.3", "A ... is the largest settlement type found in South Africa.", ["megalopolis", "conurbation", "metropolis", "city"], 1,
        ["South Africa has no megalopolis.", "Gauteng's cities have grown together into one."]),
    mcq("1.2.4", "A ... is an urban settlement type made up of a major city and towns.", ["metropolis", "conurbation", "city", "megalopolis"], 0,
        ["One big city with smaller towns round it.", "A conurbation is several cities joined."]),
    mcq("1.2.5", "The ... of a city covers a larger area than a town.", ["range", "sphere of influence", "threshold population", "service area"], 1,
        ["The area from which a settlement draws its customers.", "A city's influence reaches further."]),
    mcq("1.2.6", "A university has a ... range and a ... sphere of influence than a school.",
        ["smaller; larger", "smaller; smaller", "larger; larger", "larger; smaller"], 2,
        ["How far will students travel to a university?", "A university serves a whole region."]),
    mcq("1.2.7", "The range associated with the purchase of a motor vehicle is greater than the purchase of bread because it is:\n"
        "(i) More expensive\n(ii) Purchased on a daily basis\n(iii) Not purchased frequently\n(iv) Less expensive",
        ["(i) and (iii)", "(ii) and (iv)", "(i) and (ii)", "(iii) and (iv)"], 0,
        ["People travel far for things that cost a lot.", "And for things they buy only now and then."])]
q13 = [
    rub("1.3.1", "Define the term rural-urban migration.", 2, ["Movement/moving/move/moves of people from rural areas to urban areas (2)."],
        ["Migration is the movement of people.", "From where to where?"], each=2,
        notes=["Concept. Part mark: movement of people from rural areas (1)."]),
    mcq("1.3.2", "According to the graph, the percentage level of poverty decreased by a smaller amount in (rural/urban) areas.", ["Rural", "Urban"], 0,
        ["Compare the two lines from 1994 to 2024.", "Which line falls less steeply?"]),
    rub("1.3.3", "How has unemployment contributed to this trend in poverty levels (answer to QUESTION 1.3.2)?", 2, [
        "People earn no/low salaries/income/wages (2).", "They are not able to afford basic services (accept examples) (2)."],
        ["No job means no income.", "What can people without an income not pay for?"], each=2),
    rub("1.3.4", "How does the movement of young adults to urban areas have a negative social impact on the rural community?", 4, [
        "Birth rate declines (2).", "Ageing population (2).", "Disruption to family units (accept examples) (2).", "Increase in poverty (2).",
        "Increase in unemployment (2).", "Decrease in (access to) services (accept examples) (2).",
        "Standard of living decreases (accept examples) (2).", "Older/younger community members vulnerable to social ills (accept examples) (2).",
        "Gender structure changes (2).", "Quality of life decreases (accept examples) (2).", "Brain drain as skilled people leave rural area (2).",
        "Loss of community identity (2)."],
        ["Who is left behind when the young adults go?", "Think of families, the old, the very young and the skills that leave."], each=2),
    rub("1.3.5", "Suggest strategies that can be introduced in rural areas to reduce the movement of young adults to urban areas.", 6, [
        "Create opportunities for investments (accept examples) (2).", "Increase employment opportunities (accept examples) (2).",
        "Skills development programmes (accept examples) (2).", "Promote entrepreneurship (2).", "Develop community projects (2).",
        "Make services more accessible (accept examples) (2).", "Improve the quality of services (accept examples) (2).",
        "Improve infrastructure (accept examples) (2).", "Increase recreational/cultural activities (accept examples) (2).",
        "Promote tourism (accept examples) (2).", "Subsidising education (2).", "Land reform programmes (accept examples) (2).",
        "Young farmers receive financial assistance (accept examples) (2).", "Provide market-related salaries/bonuses (accept examples) (2)."],
        ["Why do young adults leave?", "Give them reasons to stay: jobs, skills, services."], each=2)]
q14 = [
    rub("1.4.1", "Define the concept urban profile.", 2, ["Side view/cross-section of an urban area/city/town (2)."],
        ["A profile is how something looks from the side.", "The side view of a whole town."], each=2,
        notes=["Concept. Part mark: side view (1)."]),
    rub("1.4.2", "Comment on the height of buildings in the CBD in comparison to those in the rural-urban fringe.", 1, [
        "Height of buildings decreases (towards the rural-urban fringe) (1).", "Height of buildings increases towards the CBD (1).",
        "Buildings are taller/higher in the CBD OR lower/shorter in the rural-urban fringe (1)."],
        ["Look at the CBD on the left and the fringe on the right.", "Tall or low?"]),
    rub("1.4.3", "How has the demand for land influenced the density of buildings in the CBD?", 2, [
        "(Resulted in a) high/higher building density (2). ACCEPT: buildings close together."],
        ["Land in the CBD is scarce and expensive.", "So buildings are packed close together."], each=2),
    rub("1.4.4", "Why are both the transition zone and rural-urban fringe referred to as zones of change?", 4, [
        "(Characterised by) mixed land use (2).", "Invasion and succession (accept examples) (2).", "(Urban) renewal (occurs) (2).",
        "Urban expansion OR urban sprawl (occurs) (accept examples) (2)."],
        ["Land uses in these zones keep changing.", "Old uses are pushed out by new ones; the town grows outwards."], each=2),
    rub("1.4.5", "Suggest economic reasons why the rural-urban fringe would be an attractive location for commercial activities.", 6, [
        "Land is cheaper (2).", "Available land (2).", "Accessible market (2).", "Reduced transport costs (accept examples) (2).",
        "Accessible transport infrastructure (accept examples) (2).", "Less costs incurred due to less crime (accept examples) (2).",
        "Access to raw materials (2)."],
        ["Economic reasons: what saves a business money?", "Land, transport, customers."], each=2)]
q15 = [
    rub("1.5.1", "Define the term informal settlement.", 2, [
        "Building of structures on land that people occupy with no legal claim (2). ACCEPT: people occupy/live on land illegally/without "
        "permission OR shacks built on vacant land OR temporary/unplanned settlements OR no basic services."],
        ["Informal: not planned or approved.", "Who owns the land the shacks stand on?"], each=2, notes=["Concept."]),
    lst("1.5.2", "State ONE factor in the extract that has a negative impact on the health of residents in informal settlements.", 1,
        [["Lack of basic services", "No basic services", "Basic services"], ["Pollution", "Polluted"], ["Overcrowding", "Overcrowded"],
         ["Poor waste management", "Waste management", "Waste"]],
        ["Read the extract's first paragraph.", "It lists four problems."]),
    rub("1.5.3", "Explain TWO economic reasons for the increase in informal settlements.", 4, [
        "Municipal budgets cannot keep up with the increasing demand (2).", "High levels of unemployment/lower wages (2).",
        "High levels of poverty (2).", "Unaffordable formal housing/rent (2).", "Difficulty in obtaining financial assistance (accept examples) (2).",
        "High interest rates (2).", "Cheaper to rent/build (accept examples) (2).", "Closer proximity to work (2)."],
        ["Economic: about money.", "Why can people not afford a formal house?"], each=2),
    rub("1.5.4", "In a paragraph of approximately EIGHT lines, explain how the upgrading (improvement) of informal settlements would have a "
        "positive social impact for people living in these settlements.", 8, [
        "Improved services (accept examples) improve quality of life (2).", "More facilities (accept examples) built for greater convenience (2).",
        "Improved transport infrastructure will link surrounding areas to allow for accessibility (accept examples) (2).",
        "Upgraded infrastructure (accept examples) improves quality of life (2).",
        "Better access to recreational facilities (accept examples) to improve quality of life (2).",
        "Community networks (accept examples) are preserved lowering levels of crime (2).",
        "Aesthetics/healthier environment (accept examples) improves life expectancy (2).",
        "Building social capital will create a sense of community belonging (2).", "Teach locals new skills (accept examples) that could ensure employment (2).",
        "Appointment of local people creates job opportunities (2)."],
        ["Social: people's lives, health and community.", "Four improvements, each with what it does for people."], each=2,
        notes=["Part marks: each improvement named without its effect earns 1; a maximum of four marks for part answers."])]

# ---- QUESTION 2: ECONOMIC GEOGRAPHY OF SOUTH AFRICA, the question paper pages 8-14 and the memo pages 8-12 ----
q21 = [
    mcq("2.1.1", "The main difference between small-scale and large-scale farming is the ...",
        ["size of farm holdings.", "use of research technology.", "types of farmers.", "impact on the market."], 0,
        ["The names say it: small or large.", "What is small or large about the farm?"]),
    mcq("2.1.2", "Photograph ... below illustrates small-scale farming.", ["P", "Q", "R", "S"], 3,
        ["Small-scale farming uses little machinery.", "Which photograph shows people working by hand?"], figure=fig("2.1", FARMS)),
    mcq("2.1.3", "A characteristic of small-scale farming evident in the photograph is ...",
        ["the use of hybrid seeds.", "that it is only export-orientated.", "the high capital investment.", "the use of manual labour."], 3,
        ["What can you SEE in the small-scale photograph?", "People carrying water in buckets."], figure=fig("2.1", FARMS)),
    mcq("2.1.4", "... is an economic advantage for a farmer practising large-scale farming.",
        ["The use of machinery", "Larger profits", "A large labour force", "The practising of monoculture"], 1,
        ["Economic: about money.", "Which option is about earnings?"]),
    mcq("2.1.5", "Cattle farming is an activity in the ... economic sector.", ["primary", "secondary", "tertiary", "quaternary"], 0,
        ["Primary activities use natural resources directly.", "Farming, mining, fishing ..."]),
    mcq("2.1.6", "Distribution of dairy products is an activity in the ... economic sector.", ["primary", "secondary", "tertiary", "quaternary"], 2,
        ["Distribution moves products to customers.", "A service."]),
    mcq("2.1.7", "A factor favouring cattle farming in South Africa is ...",
        ["heavy rainfall.", "high temperatures.", "available grazing land.", "climatic variation."], 2,
        ["Cattle need food.", "Large areas of natural grass."]),
    mcq("2.1.8", "Challenges faced by small-scale cattle farmers in South Africa are:\n(i) High rate of unemployment\n(ii) Animal diseases\n"
        "(iii) Semi-arid land\n(iv) Export market", ["(i) and (ii)", "(ii) and (iii)", "(i) and (iv)", "(iii) and (iv)"], 1,
        ["Challenges for the cattle themselves.", "Sick animals, and dry land with little grass."])]
q22 = [
    mcq("2.2.1", "The main purpose of an industrial development zone (IDZ) is to promote ...", ["exports", "imports"], 0,
        ["IDZs are built near harbours and airports.", "To sell more goods overseas."]),
    mcq("2.2.2", "SDIs are generally located in ... areas.", ["underdeveloped", "developed"], 0,
        ["Spatial development initiatives aim to develop places.", "Which places need developing?"]),
    mcq("2.2.3", "A positive economic impact of spatial development initiatives (SDIs) is ...",
        ["improved quality of life", "upgraded infrastructure"], 1,
        ["Economic, not social.", "Roads, ports and railways."]),
    mcq("2.2.4", "A social challenge experienced in the Saldanha Bay IDZ is ...", ["unskilled workforce", "poor harbour facilities"], 0,
        ["Social: about people.", "Saldanha Bay has a deep-water harbour."]),
    mcq("2.2.5", "The main industry associated with the West Coast SDI is a/an ...", ["automotive plant", "steel plant"], 1,
        ["Saldanha Bay exports iron ore.", "What is made from iron ore?"]),
    mcq("2.2.6", "The South-western Cape core industrial region is restricted by ...", ["few mineral resources", "small local markets"], 0,
        ["Cape Town has a large market.", "What does the region lack for heavy industry?"]),
    mcq("2.2.7", "A physical factor that promotes industries in the South-western Cape core industrial region is ...",
        ["overseas markets", "coastal location"], 1,
        ["Physical: a natural feature.", "Markets are a human factor."])]
q23 = [
    term("2.3.1", "According to the graph, what amount of coal, in billions, was exported in 2023?", ["R250 billion", "250 billion", "R250", "250"],
         ["Read the dashed line (rands in billions) at 2023.", "Use the right-hand axis."]),
    rub("2.3.2", "What has been the general trend in profits from the export of coal in recent years?", 1, [
        "An upward/increasing/positive/rising trend (1)."],
        ["Follow the dashed line to 2023.", "Up or down?"], notes=["Accept figures that indicate an increase in exports."]),
    term("2.3.3", "According to the graph, between which years was the smallest number of employees recorded in the coal mining industry?",
         ["Between 2021 and 2022", "2021 and 2022", "2021-2022", "2021 to 2022"],
         ["Follow the light line (number of employees).", "Where is its lowest point?"]),
    rub("2.3.4", "Give ONE possible reason for the small number of employees (answer to QUESTION 2.3.3).", 2, [
        "Depletion of coal (2).", "Economic recession (accept examples) (2).", "Impact of illness/pandemics (accept examples) (2).",
        "Possible strikes/uprisings (accept examples) (2).", "Increase in mechanisation (2).", "Threats of nationalisation (accept examples) (2).",
        "Use of environmentally friendly energy sources/reduced demand of coal (accept examples) (2).", "Load-shedding (2).", "Mine accidents (2)."],
        ["What happened around 2021 that slowed work everywhere?", "Machines, demand and the coal itself."], each=2),
    rub("2.3.5", "According to the extract, the high-quality coal reserves in South Africa have been decreasing over the years. Explain the "
        "negative impact of decreasing high-quality coal reserves for the future supply of power in South Africa.", 4, [
        "There would be more frequent load-shedding/load reduction (2).", "There would be a greater demand than supply (2).",
        "The cost of electricity would increase (accept examples) (2).", "Invest in alternate sources of renewable energy (2).",
        "Lower/lesser/poorer quality coal will have to be used (2).", "Leads to shut downs/maintenance of power stations (2).",
        "Expensive to invest in alternative energy sources (accept examples) (2)."],
        ["Most of South Africa's electricity comes from coal.", "Less good coal: what happens to power supply and prices?"], each=2),
    rub("2.3.6", "Explain why the coal mining industry is important to the economy of South Africa.", 6, [
        "It creates employment opportunities thus reducing dependency on government/increasing the buying power of people (2).",
        "Multiplier effect stimulates other industries growing the economy (2).", "Coal mining contributes to the GDP that stimulates the economy (2).",
        "Coal is our main source of power that all sectors of our economy are dependent on (2).", "Export of coal will earn foreign exchange (2).",
        "Taxes from coal mining industry contribute to the GDP/GNP (2).", "The use of coal as a raw material to manufacture other products (2).",
        "Promotes the development/upgrading of infrastructure (accept examples) that benefits other sectors of the economy (2)."],
        ["Jobs, power, exports, taxes.", "Each point: what coal does, then how it helps the economy."], each=2,
        notes=["Part marks: each fact named without its effect earns 1; a maximum of three marks for part answers."])]
q24 = [
    term("2.4.1", "Refer to the statistics and state the percentage that the Gauteng (PWV) core industrial region contributes to the GDP of "
         "South Africa.", ["38%", "38", "38 percent"], ["Read the statistics list.", "The line about the GDP."]),
    pick1("2.4.2", "Quote evidence from the extract that shows why 31% of South Africa's labour force is found in the Gauteng (PWV) core "
          "industrial region.", sentences(GAUTENG_1) + sentences(GAUTENG_2), [2],
          ["Which sentence is about jobs?", "Businesses and the people they employ."], marks=2),
    rub("2.4.3", "Refer to the sketch and explain the role of the major roads in supporting industrial development in the Gauteng (PWV) core "
        "industrial region.", 4, [
        "Allows for effective transportation of goods/raw materials/labour (accept examples) (2).", "Creates accessibility to major markets (2).",
        "The dense network of roads creates greater accessibility (2).",
        "The shortest possible distance to the towns/cities is available, making it cost effective (2).",
        "Effective road network will attract investors (2).", "Decreases traffic congestion/rapid delivery of products (2)."],
        ["The roads link the industrial areas to each other and to other towns.", "What moves along them, and why does that help industry?"],
        each=2),
    rub("2.4.4", "Explain TWO challenges faced by the Gauteng (PWV) core industrial region.", 4, [
        "Load-shedding/load reduction reduces production (2).", "Traffic congestion slows movement of goods/people (2).",
        "Shortage of water resources/water shedding (2).", "Gauteng has limited land available for further expansion (2).",
        "High petrol prices increase transport costs (2).", "Deterioration of rail transport (2).", "Increased dependency on road transport (2).",
        "Labour strikes/unrest decrease production (2).", "Increased operating costs (wage negotiations) (2).",
        "Distance from harbours increases transport costs (2).", "Reduced access to raw materials (2).", "High crime rate (2).",
        "Increase in pollution (2).", "Lack of skills (2).", "Lack of maintenance of transport infrastructure (accept examples) (2).",
        "Competition from counterfeit (fake) cheap products against originals (2).", "Political issues affect business confidence (accept examples) (2)."],
        ["Gauteng is inland, crowded and depends on electricity.", "Each challenge, then what it does to industry."], each=2),
    rub("2.4.5", "Suggest ONE advantage and ONE disadvantage of industries moving towards high value-added production in the Gauteng (PWV) "
        "core industrial region.", 4, [
        "Advantage: higher profits (2).", "Advantage: efficient production process (2).", "Advantage: upskilling of people (accept examples) (2).",
        "Advantage: increased investment (2).", "Advantage: increased foreign income (2).", "Advantage: access to a larger market (2).",
        "Advantage: diversifies production (2).", "Advantage: provides opportunities in specialised sectors (2).",
        "Disadvantage: less job opportunities for unskilled workers (2).", "Disadvantage: skilled labour will be sourced from other countries/regions (2).",
        "Disadvantage: buyers will have to pay more for goods (2).", "Disadvantage: businesses in low value production will be negatively affected (2).",
        "Disadvantage: high cost for skills development (accept examples) (2).", "Disadvantage: production losses due to load-shedding (2).",
        "Disadvantage: requires a large capital outlay (2).", "Disadvantage: existing infrastructure struggles to meet demands (2).",
        "Disadvantage: high maintenance cost (2)."],
        ["High value-added production uses advanced technology such as robots (see the glossary).", "Good for profits; bad for whom?"], each=2,
        notes=["MUST give one advantage and one disadvantage."])]
q25 = [
    term("2.5.1", "According to the extract, what is the percentage of informal trading that takes place in Johannesburg?", ["30%", "30", "30 percent"],
         ["Read the extract's first sentence.", "A percentage of South Africa's informal trading."]),
    pick1("2.5.2", "Quote evidence from the extract why trading has been restricted in Johannesburg at night.",
          sentences(TRADE_1) + sentences(TRADE_2) + sentences(TRADE_3), [3],
          ["Which sentence mentions overnight?", "Why is sleeping at a stall dangerous?"]),
    term("2.5.3", "According to the graph, which is the busiest time period for trading in the informal sector?",
         ["16:00 to 18:00", "16:00-18:00", "16:00 - 18:00", "16h00 to 18h00", "16:00 18:00", "4 pm to 6 pm"],
         ["Find the highest point of the line.", "Read the time below it."]),
    rub("2.5.4", "Suggest TWO reasons for the rapid growth of the informal sector in the city of Johannesburg.", 4, [
        "High unemployment rate/retrenchments (2).", "Low paying jobs (2).", "The high number of illegal immigrants (2).",
        "Increase in the urban population (accept examples) (2).", "Lack of skills/education (2).",
        "Economic recession/slump in the economy (accept examples) (2).", "Increase in poverty (2).", "Lower start-up costs (accept examples) (2).",
        "Fewer regulations (accept examples) (2).", "Lack of access to finance/loans (2).", "Formal businesses sub-contract from the informal sector (2)."],
        ["Why do people start trading on the street?", "No formal job, and it is easy to start."], each=2),
    rub("2.5.5", "In a paragraph of approximately EIGHT lines, explain measures that the municipality can put in place to assist traders in the "
        "informal sector to operate under more favourable conditions.", 8, [
        "Regulate the informal sector (accept examples) (2).", "Allocate space near markets (2).", "Provide them with stalls (accept examples) (2).",
        "Access to storage facilities (accept examples) (2).", "Access to basic services (accept examples) (2).",
        "Access to financial assistance (accept examples) (2).", "Provide skills training/learnership opportunities (2).",
        "Create partnerships with the formal sector/private businesses (2).", "Effective policing/increase security (2).",
        "Public awareness/by-laws to improve the perception of the informal sector (accept examples) (2)."],
        ["What do traders need to work safely and well?", "Space, stalls, storage, services, money and safety."], each=2)]

# ---- QUESTION 3 (SECTION B): only the parts that do not read the maps, the question paper pages 15-18 and the memo pages 13-15 ----
BLOEMFONTEIN = ("GENERAL INFORMATION ON BLOEMFONTEIN\n\nCoordinates: 29°05'S; 26°09'E\n\nBloemfontein is the capital city of the Free State. "
                "It is located in central South Africa on the southern edge of the Highveld. The area is generally flat with isolated hills. "
                "Although agriculture is the main primary activity, businesses mainly drive Bloemfontein's economy.\n\nDue to the many businesses, "
                "it has attracted more people into the area. This has led to many new developments.")
q3a = [
    mcq("3.1.1", "The (1:50 000 topographical map/1:10 000 orthophoto map) has a smaller scale.", ["Topographical map", "Orthophoto map"], 0,
        ["Compare 1/50 000 with 1/10 000.", "The smaller fraction is the smaller scale."]),
    mcq("3.1.2", "A small-scale map shows:\n(i) A small area\n(ii) Greater detail\n(iii) A large area\n(iv) Less detail",
        ["(i) and (ii)", "(ii) and (iv)", "(i) and (iii)", "(iii) and (iv)"], 3,
        ["A small-scale map fits a big area on one page.", "So each feature is drawn with less detail."])]
q3b = [
    mcq("3.3.1", "The process of converting data from raster to vector format is called data ...",
        ["analysis.", "integration.", "layering.", "manipulation."], 3,
        ["Changing data from one form to another.", "Working the data into a new form."]),
    rub("3.3.2", "Explain how the data was converted from the vertical aerial photograph (used to make the orthophoto map) to the topographical map.", 2, [
        "Data was converted from images/raster data to symbols/vector data (accept examples) (2).", "Changed/reduced the scale (2)."],
        ["A photograph is made of pixels; a map is made of symbols.", "Raster to ..."], each=2),
    rub("3.3.4", "Define the concept data integration.", 2, ["Combining of sources of information/data layers (2)."],
        ["Integrate means to bring together.", "Bringing different data together."], each=2, notes=["Concept."]),
    term("3.3.5", "Name the method of data integration used on the topographical map.", ["Data layering", "Layering", "Layers"],
         ["A topographical map puts roads, rivers, contours and buildings on top of each other.", "Each kind of feature is one ..."])]

sec_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Rural settlements", "marks": 8,
     "lead": "Match the statements in COLUMN A with the options in COLUMN B.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Urban hierarchies", "marks": 7,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Rural-urban migration", "marks": 15,
     "lead": "Refer to the sketch and graph below showing the levels of poverty caused by rural-urban migration.",
     "figure": fig("1.3", "A sketch of a city with an arrow labelled Young Adults curving towards it, above a line graph of the percentage level "
                   "of poverty (30 to 100) from 1994 to 2024. Dashed line (level of poverty of young adults that remain in rural areas): about 82% "
                   "in 1994, level until about 2004, then falling slowly to about 72% by 2024. Solid line (level of poverty of young adults that "
                   "migrate to urban areas): about 80% in 1994, level until about 2004, then falling steeply to about 52% around 2014 and about "
                   "32% by 2024."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Urban profiles", "marks": 15, "lead": "Refer to the sketch below showing an urban profile.",
     "figure": fig("1.4", "An urban profile across 25 km from the CBD to the rural-urban fringe: tall high-rise buildings in the CBD; old houses "
                   "mixed with small businesses in the Transition Zone; rows of two-storey houses in the Residential zone; a factory with smoking "
                   "chimneys in the Industrial zone; open farmland with a cow and a few low buildings in the Rural-urban fringe."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Informal settlements", "marks": 15,
     "lead": "Refer to the photographs and extract below on informal settlements.", "extract": INFORMAL,
     "figure": fig("1.5", "Two photographs. Before: a dense, untidy informal settlement of makeshift shacks of corrugated iron and scrap, with "
                   "washing lines strung between them. After: neat rows of identical prefabricated units along a straight, cleared street with "
                   "electricity poles; a person is sweeping."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Agriculture", "marks": 8,
     "lead": "Various options are provided as possible answers to the following questions. The photographs on small- and large-scale farming "
             "are for QUESTIONS 2.1.2 and 2.1.3.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Industrial development", "marks": 7,
     "lead": "Match the statements in COLUMN A with the options in COLUMN B.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Coal mining", "marks": 15, "lead": "Refer to the graph and extract below on coal mining in South Africa.",
     "extract": COAL,
     "figure": fig("2.3", "A line graph, SOUTH AFRICA'S COAL EXPORTS AND EMPLOYMENT, 2016 to 2023. Light line, number of employees (left axis, "
                   "60 000 to 100 000): about 87 000 in 2016, 86 000 in 2017, 93 000 in 2018, 91 000 in 2019, 88 000 in 2020 and 85 000 in 2021, "
                   "falling to its lowest, about 76 000, between 2021 and 2022, then about 84 000 in 2023. Dashed line, exports in billions of "
                   "rands (right axis, 50 to 250): about 50 in 2016, 55 in 2017, 75 in 2018, 80 in 2019, 65 in 2020, 60 in 2021, 90 in 2022 and "
                   "250 in 2023."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Core industrial regions", "marks": 15,
     "lead": "Refer to the infographic below on the Gauteng (PWV) core industrial region.", "extract": GAUTENG,
     "figure": fig("2.4", "Two panels. Statistics for the Gauteng (PWV) core industrial region: 20% of South Africa's population; 31% of SA's "
                   "labour force in all economic sectors; 22% contributed to the mining sector; 38% contribution to the GDP of South Africa; 45% of "
                   "South Africa's manufacturing capacity. A sketch of the major roads that link the main industrial areas: Pretoria, "
                   "Witwatersrand and Vereeniging are joined by roads running north to south, and from them major roads run out to Mabopane, "
                   "Polokwane, KwaNdebele, Brits, Rustenburg, Middelburg, Emalahleni (Witbank), Bronkhorstspruit, Potchefstroom, Klerksdorp, "
                   "Delmas and Secunda/Evander."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "The informal sector", "marks": 15,
     "lead": "Refer to the extract and graph below on the informal sector.", "extract": TRADE,
     "figure": fig("2.5", "A line graph, Busiest time for trading in the informal sector in Johannesburg: % of informal trade by time of day. "
                   "08:00-10:00 about 6%; 10:00-12:00 about 20%; 12:00-14:00 about 6%; 14:00-16:00 about 10%; 16:00-18:00 about 37%; 18:00-20:00 "
                   "about 18%; 20:00-22:00 about 2%."), "items": q25},
]
sec_b = [
    {"id": "3.1", "title": "Question 3.1", "kind": "Map scale", "marks": 2,
     "lead": "The parts of Question 3.1 that do not read the maps. The topographical map is 1:50 000 and the orthophoto map 1:10 000.",
     "extract": BLOEMFONTEIN, "items": q3a},
    {"id": "3.3", "title": "Question 3.3", "kind": "Geographical information systems (GIS)", "marks": 6,
     "lead": "The parts of Question 3.3 that do not read the topographical or orthophoto map.", "items": q3b},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Geography", "title": "Geography P2", "sitting": "November 2024", "total_marks": 128, "time": "3 hours"},
    "sections": [{"title": "Section A: Rural and urban settlements and the economic geography of South Africa", "total": 120, "missions": sec_a},
                 {"title": "Section B: Geographical skills and techniques", "total": 8, "missions": sec_b}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "Section A whole and the map-free parts of Section B, hand-transcribed from the paper and "
                                                           "memo PDFs and their page images; no API call."},
        {"n": "3", "kind": "no_fit", "detail": "Section B reads the 1:50 000 topographical map 2926AA BLOEMFONTEIN-NOORD and the 1:10 000 orthophoto "
                                               "map 2926AA 10, handed out in the exam room: not in the question paper and not published. Its 22 "
                                               "marks that read them (3.1.3-3.1.7, 3.2.1-3.2.4, 3.3.3) wait for the maps; the paper totals the 128 "
                                               "marks that can be played (the printed paper: 150)."},
        {"n": "1.1.8", "kind": "memo_issue", "detail": "The memo accepts both options (Y/Z): played as a pick of one with both right."},
        {"n": "2.4.5", "kind": "no_fit", "detail": "The memo MUST have one advantage and one disadvantage; the keyword marker cannot require one of "
                                                   "each (two advantages also score): the rule is the part's note, for model marking."},
        {"n": "2.4.2", "kind": "no_fit", "detail": "Quote items (2.4.2, 2.5.2) are played by picking the extract's sentence: the memo awards marks "
                                                   "for a quote from the extract, so picking the right sentence is the same skill."},
        {"n": "paper", "kind": "memo_issue", "detail": "The memo's pages 1-3 are the notes to markers and a marked sample from another paper (its "
                                                       "answers, e.g. 1.2.1 'Melting snow', match nothing here): ignored."},
    ],
}
out = Path(__file__).parent / "out" / "geo-p2-2024-11"
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
