"""Grade 10 Geography P1 November 2025 (Eastern Cape Department of Education, provincial assessment): SECTION A whole (Questions 1
and 2, 120 marks) and the parts of SECTION B (Question 3) that do not read the maps (14 of its 30 marks), hand-transcribed into the
catalogue format, then run through `ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and
the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): stanmorephysics.com, one scanned PDF of the paper
(15 pages, the last the two maps) and the marking guidelines (8 pages), split by page into QP and MG files (no text layer).

  python tools/ingest/transcribe_g10_geo_p1_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g10-geo-p1-2025-11-ec/g10-geo-p1-2025-11-ec QP.pdf" "uploads/provincial/g10-geo-p1-2025-11-ec/g10-geo-p1-2025-11-ec MG.pdf" --id g10-geo-p1-2025-11-ec --from-json

SECTION B reads a 1 : 50 000 topographical map and a 1 : 10 000 orthophoto map of 3419AB CALEDON. The scan prints both at half a page
under watermarks: too small to measure centimetres on and too blurred to read. As every Geography P1, the parts that read the maps
(3.1.3-3.1.5, 3.2.2-3.2.4, 3.2.6, 3.3.2: 16 marks) wait for the maps; the rest plays (3.2.5 names area 2 as the hospital in 3.1.3's
own stem). The paper totals what is playable, 134.

The Geography rulings, as Grade 12: a choice between two printed options is multiple choice of the two; a written answer is
statements (the memo's points and clearly wrong ones, a card worth what the memo ticks); 'differ' is a sort; a station-model reading
the memo states with no working is an authored multiple choice. Figure boxes in PDF points (page 595 x 842), measured on the page
images (110 dpi, scale 1.5278)."""
from provincial import Paper

P = Paper("g10-geo-p1-2025-11-ec", 595.2, 841.8, {
    "1.2": [4, 119, 139, 542, 411], "1.3": [5, 86, 93, 571, 336], "1.4": [6, 84, 89, 537, 330], "1.5": [6, 99, 496, 463, 776],
    "2.1": [7, 117, 514, 411, 715], "2.2": [8, 136, 285, 512, 440], "2.3": [9, 56, 98, 474, 339], "2.4": [10, 84, 370, 529, 545],
    "2.5": [11, 170, 101, 513, 321], "3": [12, 151, 148, 446, 393]}, start=7)
answer, stmt, mcq, term, sort, work = P.answer, P.stmt, P.mcq, P.term, P.sort, P.work
two = lambda n, q, a_opt, b_opt, a, clues, **kw: mcq(n, q, [a_opt, b_opt], a, clues, marks=1, **kw)
ABC = lambda n, q, a, clues: mcq(n, q, ["A", "B", "C"], a, clues, marks=1)

# ---- SECTION A, QUESTION 1: THE ATMOSPHERE, the question paper pages 3-7 and the memo pages 2-4 ----
q11 = [  # printed Z above Y: Z is the first option
    two("1.1.1", "The process by which water vapour changes to liquid is known as …", "Evaporation", "Condensation", 1,
        ["Vapour to liquid.", "Droplets form on a cold glass."]),
    two("1.1.2", "The process by which water changes to water vapour is known as …", "Evaporation", "Condensation", 0,
        ["Liquid to vapour.", "The sun heats a puddle."]),
    two("1.1.3", "Forms overnight as the air near the ground cools and stabilises.", "Radiation fog", "Advection fog", 0,
        ["The ground loses heat at night.", "Advection fog moves in from the sea."]),
    two("1.1.4", "Gases that do not change in proportion (percentage) are …", "Constant gases", "Variable gases", 0,
        ["Nitrogen and oxygen stay the same.", "They do not vary."]),
    two("1.1.5", "A condition in the atmosphere where temperature increases with height is …", "Global warming", "Temperature inversion", 1,
        ["Normally temperature falls with height.", "Here it is turned upside down."]),
    two("1.1.6", "Incoming solar radiation is known as …", "Terrestrial radiation", "Insolation", 1,
        ["Incoming from the sun.", "In-sol-ation."]),
    two("1.1.7", "It includes temperature extremes, large latitudinal and seasonal ranges of temperature, small annual precipitation totals "
                 "and low relative humidity.", "Maritime climate", "Continental climate", 1,
        ["Far from the sea.", "The sea evens out temperature."]),
    two("1.1.8", "The temperature at which condensation begins.", "Dew point", "Temperature", 0,
        ["Dew forms at it.", "The air is saturated."])]
LAYERS = lambda n, q, a, clues: term(n, q, a, clues)
q12 = [
    LAYERS("1.2.1", "The coldest layer.", ["mesosphere"], ["Find the lowest temperature on the graph.", "About 80-90 km up."]),
    LAYERS("1.2.2", "The layer that comprises the densest air.", ["troposphere"], ["Air is densest near the ground.",
                                                                                    "The layer we live in."]),
    LAYERS("1.2.3", "A temperature inversion occurs in the stratosphere and which other layer?", ["thermosphere"],
           ["Where else does the graph lean right with height?", "The top layer."]),
    LAYERS("1.2.4", "The stratopause is the boundary that demarcates the stratosphere from which layer?", ["mesosphere"],
           ["The layer above the stratosphere.", "Read the graph upwards."]),
    LAYERS("1.2.5", "The layer of ozone is found in this layer.", ["stratosphere"], ["Ozone absorbs UV and warms its layer.",
                                                                                    "Above the troposphere."]),
    LAYERS("1.2.6", "The layer that prevents dust and rocks from space entering the lower layers of the atmosphere.", ["mesosphere"],
           ["Meteors burn up here.", "The coldest layer."]),
    LAYERS("1.2.7", "The layer that contains most of the air of the atmosphere.", ["troposphere"], ["The lowest layer.",
                                                                                                   "Weather happens here."])]
q13 = [
    stmt("1.3.1", "Explain the concept: the greenhouse effect.", 2,
         ["The process whereby heat is trapped close to the surface of the Earth by greenhouse gases.",
          "Greenhouse gases let sunlight in but trap the heat the Earth gives off."],
         ["The process of growing vegetables in a glass house.", "The cooling of the Earth by clouds.",
          "The destruction of the ozone layer by the sun.", "The movement of heat from the poles to the equator."],
         ["Gases trap heat.", "Like the glass of a greenhouse."], 2),
    stmt("1.3.2", "According to the pie graph, which sector contributes the most to greenhouse emissions globally?", 1,
         ["Electricity and heat production"], ["Transportation", "Industry", "Buildings", "Other energy"],
         ["Find the biggest slice.", "25%."], 1),
    stmt("1.3.3", "Name ONE greenhouse gas emitted by this sector (answer to 1.3.2).", 2,
         ["Carbon dioxide (CO₂)", "Methane (CH₄)", "Nitrous oxide (N₂O)"], ["Oxygen (O₂)", "Nitrogen (N₂)", "Helium (He)"],
         ["Burning coal releases it.", "Not the gases we breathe in."], 2, after=["1.3.2"]),
    stmt("1.3.4", "Explain how continuous emission of greenhouse gases into the atmosphere will have a negative impact on the environment.", 4,
         ["Global temperature rises and leads to the melting of ice caps.",
          "Plants and animals that cannot adapt to higher temperatures die and become extinct.", "More droughts and floods occur.",
          "Warmer oceans lead to marine life and coral reefs dying.", "Heat waves become more common."],
         ["The Earth becomes colder every year.", "Sea levels drop.", "More plants grow in every region."],
         ["The Earth gets warmer.", "Ice, oceans, plants and animals."], 2),
    stmt("1.3.5", "Suggest THREE strategies this sector can implement to reduce the emission of greenhouse gases.", 6,
         ["Introduce measures to save electricity.", "Switch to renewable sources of generating electricity.",
          "Introduce a carbon tax on the generation of electricity.", "Introduce an energy tax on combined heat and power."],
         ["Build more coal-fired power stations.", "Burn more wood for heat.", "Remove all limits on emissions."],
         ["Use less, or make it cleaner.", "Saving, renewables, taxes."], 2)]
q14 = [
    term("1.4.1", "Identify the type of rainfall in the sketch.", ["orographic", "relief", "orographic rainfall", "relief rainfall"],
         ["Air is forced up a mountain.", "Oro means mountain."]),
    two("1.4.2", "On which side of the mountain is vegetation found (Windward or Leeward)?", "Windward", "Leeward", 0,
        ["The side facing the moist wind.", "Look for the trees in the sketch."]),
    stmt("1.4.3", "Give ONE reason why more vegetation will be growing on this side of the mountain (answer to 1.4.2).", 1,
         ["The windward side receives the most rain, as the moist air is forced to rise and condense."],
         ["The leeward side receives the most rain.", "The windward side is in a rain shadow.", "The wind blows the trees over the mountain.",
          "The windward side is warmer because it faces away from the sea."],
         ["Where does the rain fall?", "Rising air cools and condenses."], 1, after=["1.4.2"]),
    stmt("1.4.4", "Briefly explain how this type of rainfall is formed (answer to 1.4.1).", 4,
         ["Warm moist air from the ocean reaches a mountain, which forces the air upwards.",
          "The air cools as it rises and condensation starts, leading to rain.",
          "Clouds form and precipitation falls on the windward side of the mountain.",
          "The air then descends on the leeward side, warming and becoming dry."],
         ["Cold air sinks and warms, forming rain.", "The sun heats the ground and the air rises over flat land.",
          "Warm air rises over cold air at a front."],
         ["The mountain forces the air up.", "Rising air cools."], 2, after=["1.4.1"]),
    stmt("1.4.5", "Explain the negative physical impacts of this type of rainfall on the side of the mountain identified in QUESTION 1.4.2.", 8,
         ["Heavy rainfall can lead to soil erosion.", "Landslides damage the natural vegetation.",
          "Biodiversity can be destroyed because of landslides.", "Habitats are lost.",
          "Mudslides due to heavy rain can destroy the environment."],
         ["The windward side becomes a desert.", "Heavy rain stops all erosion."],
         ["Heavy rain on a slope.", "Soil, slides, habitats."], 2, after=["1.4.2"])]
q15 = [
    term("1.5.1", "Supply a name for the lines joining places of equal pressure on the map.", ["isobars", "isobar"],
         ["Iso means equal.", "Bar means pressure."]),
    term("1.5.2", "Give the name of the pressure cell dominating the interior of South Africa.",
         ["kalahari high", "kalahari anticyclone", "kalahari high pressure", "kalahari hp", "kalahari high pressure cell"],
         ["The H over the land.", "Named after a desert."], marks=2),
    term("1.5.3(a)", "What season is indicated on the synoptic weather chart?", ["winter"],
         ["A strong high over the land.", "Cold fronts reach Cape Town."], marks=2),
    stmt("1.5.3(b)", "Give TWO pieces of evidence to substantiate why you chose this season.", 4,
         ["High pressure dominates over the land (Kalahari High).", "There are no clouds over the interior of South Africa.",
          "A mid-latitude cyclone is present.", "A cold front is near Cape Town.", "It is raining at Cape Town (south-western Cape)."],
         ["A tropical cyclone is over Mozambique.", "A low dominates the interior.", "Thunderstorms cover the interior."],
         ["What is over the land, and what is at the coast?", "Fronts and the high."], 2, after=["1.5.3(a)"]),
    answer("1.5.4(a)", "Describe the cloud cover at Cape Town from the weather station model.", 1,
           ["8/8: overcast", "4/8: half covered", "0/8: clear", "2/8: mostly clear"], ["How much of the circle is shaded?",
                                                                                       "A full circle is overcast."]),
    answer("1.5.4(b)", "Give the wind direction at Cape Town.", 1, ["North-easterly", "South-westerly", "North-westerly", "South-easterly"],
           ["The wind blows from the side the shaft points to.", "Where does the shaft point?"]),
    answer("1.5.4(c)", "Give the wind speed at Cape Town.", 1, ["25 knots", "15 knots", "20 knots", "50 knots"],
           ["A full barb is 10 knots.", "A half barb is 5 knots."]),
    answer("1.5.4(d)", "Give the air temperature at Cape Town.", 1, ["17 °C", "15 °C", "7 °C", "1 °C"],
           ["The top-left number.", "Air temperature is above the dew point."]),
    answer("1.5.4(e)", "Give the dew point temperature at Cape Town.", 1, ["15 °C", "17 °C", "5 °C", "2 °C"],
           ["The bottom-left number.", "It is never above the air temperature."]),
    answer("1.5.4(f)", "Give the precipitation at Cape Town.", 1, ["Rain", "Snow", "Fog", "No precipitation"],
           ["A cold front is passing.", "Read the symbol beside the circle."])]

# ---- QUESTION 2: GEOMORPHOLOGY, the question paper pages 7-11 and the memo pages 4-6 ----
q21 = [
    term("2.1.1", "The layer is a very dense solid metallic ball.", ["inner core"], ["At the centre.", "Solid, not liquid."]),
    term("2.1.2", "The layer that is formed of solid rock.", ["crust"], ["The outer layer.", "We live on it."]),
    term("2.1.3", "The layer that is molten in nature.", ["mantle"], ["Between the crust and the core.", "Magma comes from it."]),
    term("2.1.4", "The layer that is solid and dense and consists of iron and nickel.", ["inner core"],
         ["The very centre.", "Pressure keeps it solid."]),
    term("2.1.5", "The layer that is generally referred to as being soft and pliable (bendable).", ["mantle", "asthenosphere"],
         ["Plates float on it.", "Below the crust."]),
    term("2.1.6", "The layer that is largely made up of granite and basalt.", ["crust"], ["Rocks we can see.", "The outer layer."]),
    term("2.1.7", "The layer where humans practise farming.", ["crust"], ["The surface.", "Soil lies on it."])]
q22 = [
    ABC("2.2.1", "Extensional forces cause the Earth's crust to be pulled apart.", 0, ["The hanging wall drops.", "Tension."]),
    ABC("2.2.2", "A tear fault / transform fault.", 2, ["The blocks slide sideways.", "Look at the arrows."]),
    ABC("2.2.3", "Associated with shear stress and not compressional or tensional forces.", 2, ["Sideways sliding.", "Shear."]),
    ABC("2.2.4", "Caused by compressional forces.", 1, ["Pushed together.", "The hanging wall rises."]),
    ABC("2.2.5", "A reverse fault.", 1, ["The hanging wall moves up.", "Compression."]),
    ABC("2.2.6", "Horizontal movement along a fault plane.", 2, ["No up or down.", "Side by side."]),
    ABC("2.2.7", "A normal fault.", 0, ["The hanging wall moves down.", "Tension."]),
    ABC("2.2.8", "The hanging wall block moves upward relative to the footwall block.", 1, ["Read the arrow on the hanging wall.",
                                                                                            "A reverse fault."])]
q23 = [
    stmt("2.3.1", "Define the concept continental drift.", 2,
         ["The theory that explains how continents shift positions on the Earth's surface.",
          "The theory that the continents were once joined and have slowly moved apart."],
         ["The theory that the continents have never moved.", "The movement of icebergs across the ocean.",
          "The erosion of coastlines by waves.", "The flow of rivers into the sea."],
         ["The continents move.", "Over millions of years."], 2),
    stmt("2.3.2", "Name TWO continents that formed part of Gondwanaland.", 2,
         ["South America", "Africa", "Antarctica", "Australasia"], ["North America", "Eurasia", "Europe"],
         ["Gondwanaland was the southern part.", "Look at the BEFORE map."], 1),
    stmt("2.3.3", "What is the main reason for the drifting of continents?", 1,
         ["Convection currents in the fluid (molten) mantle", "The fluidity of the magma in the mantle"],
         ["The wind blowing over the oceans", "The Earth's orbit around the sun", "Rain eroding the coastlines"],
         ["What lies under the plates?", "Heat moves the molten mantle."], 1),
    stmt("2.3.4", "Explain what happens at divergent plate boundaries.", 2,
         ["Two tectonic plates move away from each other.", "Molten rock from the mantle solidifies to create new oceanic crust."],
         ["Two plates push into each other.", "Two plates slide past each other.", "One plate sinks under another.",
          "The plates stop moving."],
         ["Diverge means move apart.", "New crust forms."], 2),
    stmt("2.3.5", "Give evidence that suggests South America and Africa were previously connected.", 4,
         ["The east coast of South America and the west coast of Africa fit like a puzzle.",
          "Rock formations match up across the coastlines of South America and South Africa.",
          "Identical deposits have been found in South America and Africa.",
          "The same fossils found in Africa and South America suggest the two continents were once joined."],
         ["Both continents have the same capital cities.", "Both continents speak the same language.",
          "Both continents are in the northern hemisphere."],
         ["Shape, rocks, fossils.", "Look at the coastlines."], 2),
    sort("2.3.6", "How does the theory of continental drift differ from the theory of plate tectonics?",
         ["Continental drift", "Plate tectonics"],
         [("The world was once made up of a single continent", 0), ("The continents moved apart from one supercontinent", 0),
          ("The Earth's surface is broken into a number of shifting plates", 1), ("The plates move on the mantle", 1)],
         ["Drift is about continents; tectonics about plates.", "One continent or many plates?"])]
HAITI = ("On 14th August 2021 a magnitude 7.2 earthquake struck Haiti in the Caribbean. The plate boundaries around Haiti are complex. The "
         "North American Plate lies to the north and the Caribbean Plate to the south. The earthquake took place at a conservative plate "
         "boundary, where the Caribbean plate moved eastwards. The focus was only 10 km deep, and the epicentre was 125 km from the capital "
         "Port-au-Prince. Years of exploitation from outside countries, dating back to the enslavement of the island's people after "
         "Christopher Columbus arrived in 1492, and political unrest within Haiti have resulted in the country's current standing as the "
         "poorest in Latin America. The unrest and poverty have translated to the development of the region, which is rife with substandard "
         "structures and building materials. Many structures use concrete, which is inexpensive and can be used to create heavy walls and "
         "roofs that resist hurricane winds. But much of the region's concrete is unreinforced, and it readily crumbles under the shaking of "
         "earthquakes.")
q24 = [
    stmt("2.4.1", "What is an earthquake?", 2,
         ["A vibration in the Earth's crust, sent as shockwaves from the point where faulting and movement occur.",
          "A sudden shaking of the ground caused by movement along a fault."],
         ["A storm with strong winds over the sea.", "An opening where lava erupts.", "A slow sinking of the land.",
          "A flood after heavy rain."],
         ["The ground shakes.", "Movement along a fault."], 2),
    stmt("2.4.2", "Where in Haiti did the earthquake occur?", 1,
         ["At a conservative plate boundary, where the Caribbean plate moves eastwards."],
         ["At a divergent plate boundary in the middle of the Atlantic.", "In the capital Port-au-Prince, on a volcano.",
          "Far from any plate boundary.", "At a convergent boundary where two continents collide."],
         ["Read the case study.", "Which kind of boundary?"], 1),
    stmt("2.4.3", "According to the article, the focus was only 10 km deep. Define the concept focus.", 2,
         ["The point below the Earth's surface where the earthquake occurs.", "The place underground where the rocks first break."],
         ["The point on the surface directly above the earthquake.", "The place with the most damage.", "The top of a volcano.",
          "The instrument that records earthquakes."],
         ["Below the surface.", "Not the epicentre."], 2),
    stmt("2.4.4", "Explain the negative impact of this earthquake on the people living close to the epicentre of the earthquake.", 4,
         ["High fatalities in densely populated areas.", "People lose their homes.",
          "Infrastructure is destroyed, which makes communication difficult.",
          "Secondary hazards such as fires and mudslides cause more deaths and injuries.", "Widespread displacement and poverty."],
         ["People's homes become stronger.", "The earthquake creates new jobs in tourism.", "Roads are improved by the shaking."],
         ["People, homes and infrastructure.", "What follows the shaking?"], 2),
    stmt("2.4.5", "What strategies can Haiti implement to reduce the impact of earthquakes?", 6,
         ["Set up earthquake warning systems.", "Build safer buildings.", "Establish evacuation routes.",
          "Establish first aid stations with volunteer doctors and nurses.", "Educate the public on emergency preparedness."],
         ["Build with unreinforced concrete.", "Ignore warning systems.", "Build more houses on the fault line."],
         ["Warn, build, prepare.", "Unreinforced concrete crumbles."], 2)]
q25 = [
    stmt("2.5.1", "What is a volcano?", 2,
         ["An opening in the Earth's crust through which lava, ash and gases erupt.", "A vent in the crust from which molten rock erupts."],
         ["A mountain made of folded rock.", "A crack where plates slide past each other.", "A deep trench in the ocean.",
          "A hill made of ice."],
         ["Molten rock comes out.", "An opening."], 2),
    term("2.5.2", "What type of volcanic structure is illustrated above?", ["composite", "composite volcano", "stratovolcano", "strato volcano",
                                                                             "composite cone"],
         ["Layers of solid rock from earlier eruptions.", "Steep sides."], marks=2),
    term("2.5.3(A)", "Identify label A.", ["crater", "vent"], ["At the top.", "The opening."]),
    term("2.5.3(B)", "Identify label B.", ["volcanic pipe", "pipe", "main pipe", "conduit"], ["It joins the chamber to the top.",
                                                                                              "Magma rises through it."]),
    term("2.5.3(C)", "Identify label C.", ["magma chamber"], ["Under the crust.", "Where magma collects."]),
    stmt("2.5.4", "In a paragraph of approximately EIGHT lines, explain TWO negative and TWO positive impacts that volcanoes have on people.", 8,
         ["Positive: volcanic ash makes fertile soil.", "Positive: ground water is used for geothermal electricity.",
          "Positive: hot springs and geysers become tourist attractions.",
          "Negative: volcanic ash causes respiratory problems.", "Negative: people are displaced and evacuated.",
          "Negative: volcanic ash disrupts air travel."],
         ["Positive: volcanoes stop all earthquakes.", "Negative: volcanic ash makes soil less fertile for ever."],
         ["Two good, two bad.", "Soil, energy, tourism; health, homes, travel."], 2)]

# ---- SECTION B, QUESTION 3 (the parts that do not read the maps), the question paper pages 12-14 and the memo pages 7-8 ----
q31 = [
    mcq("3.1.1", "The topographic map number 3419 refers to the …", ["longitude and latitude.", "latitude and longitude.",
        "contour line and isobar.", "longitude and contour lines."], 1, ["34 is the latitude.", "19 is the longitude."], marks=1),
    mcq("3.1.2", "The scale of the orthophoto map is … times larger than the scale of the topographic map.", ["5", "10", "20", "40"], 0,
        ["1 : 10 000 and 1 : 50 000.", "50 000 ÷ 10 000."], marks=1),
    work("3.1.6", "Calculate the magnetic declination of Caledon for 2025. The topographic map gives the mean magnetic declination as "
                  "23°46' west of true north (July 2001). Difference in years: 24 years. Mean annual change: 4' westwards.", 3,
         ["Total change: 24 × 4' = 96' = 1°36'\nDeclination 2025: 23°46' + 1°36' = 25°22' W of true north",
          "Total change: 24 × 4' = 96' = 1°36'\nDeclination 2025: 23°46' − 1°36' = 22°10' W of true north",
          "Total change: 24 × 4' = 96' = 0°96'\nDeclination 2025: 23°46' + 0°96' = 24°82' W of true north",
          "Total change: 25 × 4' = 100' = 1°40'\nDeclination 2025: 23°46' + 1°40' = 25°26' W of true north"],
         ["Westward change is added.", "60' make 1°."])]
q32 = [
    stmt("3.2.1", "What type of climate does Caledon experience? Give a reason for your answer.", 2,
         ["Mediterranean climate", "Caledon has warm, dry summers and cool, wet winters.", "Caledon is in the Western Cape.",
          "Caledon lies at latitude 34° S on the western side of South Africa."],
         ["Tropical climate", "Desert climate", "Caledon has summer rainfall."],
         ["Read the general information.", "Dry summers, wet winters."], 1),
    two("3.2.5", "The main economic activity at 2 (the hospital) in block E2 on the orthophoto map is (secondary / tertiary).",
        "secondary", "tertiary", 1, ["A hospital provides a service.", "Services are tertiary."])]
q33 = [
    stmt("3.3.1", "What is a geographical information system?", 2,
         ["A computer system which captures, stores, analyses, manipulates and displays geographical data.",
          "A computer-based system for working with spatial data."],
         ["A paper map of the world.", "A satellite that forecasts the weather.", "A system for drawing cartoons.",
          "A list of place names."],
         ["Computer and spatial data.", "Capture, store, analyse, display."], 2),
    two("3.3.3", "Is the orthophoto an example of raster data or vector data?", "raster data", "vector data", 0,
        ["A photograph is made of pixels.", "Vector data is points, lines and polygons."]),
    stmt("3.3.4", "What is remote sensing?", 1,
         ["Capturing data from a distance, using satellites or drones, without physical contact with the ground."],
         ["Measuring the ground by walking over it.", "Drawing a map by hand.", "Asking people about an area.",
          "Feeling the ground for earthquakes."],
         ["From a distance.", "Satellites."], 1),
    stmt("3.3.5", "State TWO advantages of remote sensing.", 2,
         ["You do not physically have to be in the area of study.", "It obtains information on areas that are inaccessible.",
          "It does not disturb natural inhabitants.", "It can cover a large area from above the ground."],
         ["It needs someone to visit every place.", "It covers only a tiny area.", "It disturbs the animals it studies."],
         ["From above, from far away.", "Hard-to-reach places."], 1)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Column A and Column B", "marks": 8,
     "lead": "Choose the word or term from COLUMN B that completes the statement in COLUMN A.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Structure of the atmosphere", "marks": 7,
     "lead": "The sketch below shows the structure of the atmosphere. Match each description with the name of the atmospheric layer.",
     "figure": P.fig("1.2", "Temperature (°C) and pressure (mb) against altitude (km): the troposphere up to about 12 km (Mount Everest "
                            "8.85 km), the stratosphere to 50 km, the mesosphere to about 85 km and the thermosphere above."), "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "The greenhouse effect", "marks": 15,
     "lead": "Study the infographic on the greenhouse effect.",
     "figure": P.fig("1.3", "A pie graph of global greenhouse gas emissions by economic sector: electricity and heat production 25%, "
                            "agriculture, forestry and other land use 24%, industry 21%, transportation 14%, other energy 10%, buildings 6%; "
                            "beside it, the natural and the human-enhanced greenhouse effect."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Rainfall", "marks": 15, "lead": "Study the sketch on a type of rainfall.",
     "figure": P.fig("1.4", "Prevailing winds carry moist air from a warm ocean up a mountain (20 °C at sea level, −4 °C at 3 000 m); "
                            "trees grow on the moist side and the far side is arid."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Synoptic weather map", "marks": 15, "lead": "Refer to the synoptic map.",
     "figure": P.fig("1.5", "A synoptic map of South Africa: a high over the interior, highs over the oceans, a cold front near Cape Town, "
                            "and the weather station model at Cape Town (shaded circle, 17 and 15, wind barbs)."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Structure of the Earth", "marks": 7,
     "lead": "Study the diagram on the structure of the Earth. Give ONE term that best describes each description. The same term may be used "
             "for more than one answer.",
     "figure": P.fig("2.1", "A cut-away of the Earth labelled crust, mantle, outer core and inner core."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Faults", "marks": 8,
     "lead": "Refer to the sketches showing different types of faults. Match each description with sketch A, B or C.",
     "figure": P.fig("2.2", "Three fault blocks: A with the hanging wall dropped below the footwall, B with the hanging wall pushed above "
                            "the footwall, and C with the blocks sliding sideways past each other."), "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Continental drift", "marks": 15, "lead": "Study the diagram on continental drift.",
     "figure": P.fig("2.3", "BEFORE: the continents joined, with South America, Africa, India, Antarctica and Australia in the south and "
                            "North America and Eurasia in the north. PRESENT DAY: the continents apart across the Atlantic."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Earthquakes", "marks": 15,
     "lead": "Study the infographic on the Haiti earthquake.\nCASE STUDY: HAITI EARTHQUAKE, 2021\n" + HAITI,
     "figure": P.fig("2.4", "A map of Haiti marking the 14 August 2021 magnitude 7.2 earthquake west of Port-au-Prince, and a photograph "
                            "of a collapsed building."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Volcanoes", "marks": 15, "lead": "Refer to the sketch of a volcano.",
     "figure": P.fig("2.5", "A cross-section of a volcano: A at the top by the vent, B the pipe through layers of solid rock from earlier "
                            "eruptions, C below the crust; flowing lava on the slope."), "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Map skills", "marks": 5,
     "lead": "GENERAL INFORMATION ON CALEDON. Co-ordinates: 34°13' S; 19°25' E. Caledon has a Mediterranean climate of warm, dry summers "
             "and cool, wet winters. Temperatures are modified by its close proximity to the South Atlantic Ocean, just over the Klein River "
             "Mountains to the south. A 1 : 50 000 topographical map 3419AB CALEDON and a 1 : 10 000 orthophoto map 3419 AB 24 CALEDON are "
             "used in the exam room.",
     "figure": P.fig("3", "A map of South Africa's provinces with Caledon marked in the south-western Cape."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Map interpretation", "marks": 3, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Geographical information systems", "marks": 6, "items": q33}]

P.finish(missions,
         {"subject": "Geography", "title": "Geography P1", "sitting": "November 2025", "total_marks": 134, "time": "3 hours"},
         [P.flag_answers(),
          {"n": "3.1", "kind": "missing_resource", "detail": "SECTION B reads the 1 : 50 000 topographical map and the 1 : 10 000 orthophoto of "
                                                             "3419AB Caledon. The scan prints them at half a page under watermarks: too small to "
                                                             "measure and too blurred to read. 3.1.3-3.1.5, 3.2.2-3.2.4, 3.2.6 and 3.3.2 (16 "
                                                             "marks) wait for the maps; the paper totals 134."},
          {"n": "3.1.6", "kind": "low_confidence", "detail": "The 2001 declination is printed on the map, unreadable in the scan; the stem gives "
                                                             "the memo's 23°46' W (2001 + 24 years = 2025, as the paper's steps). The memo's "
                                                             "working (24 × 4' = 1°36'; 23°46' + 1°36' = 25°22' W) is the right option."},
          {"n": "2.3.3", "kind": "memo_issue", "detail": "The memo gives 'faulting and folding / fluidity of magma' as the main reason continents "
                                                         "drift. Faulting and folding are results of plate movement, not its cause, so they are "
                                                         "not offered; the cards are the memo's fluidity of magma and the convection currents "
                                                         "its own 2.3.4 names. For Murci to confirm."},
          {"n": "2.3.2", "kind": "low_confidence", "detail": "The memo accepts South America, Africa, Antarctica and Australasia and adds "
                                                             "'NOT INDIA AND AUSTRALIA'. India and Australia were part of Gondwanaland; to keep "
                                                             "to the memo, the cards offer the memo's four (Australasia, not Australia) and no "
                                                             "India."}],
         {"1": 60, "2": 60, "3": 14}, 134,
         {"1.3.3": ["1.3.2"], "1.4.3": ["1.4.2"], "1.4.4": ["1.4.1"], "1.4.5": ["1.4.2"], "1.5.3(b)": ["1.5.3(a)"]},
         "Section A whole and the parts of Section B that do not read the maps")
