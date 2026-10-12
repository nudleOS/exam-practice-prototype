"""Grade 11 Geography P1 November 2024 (Eastern Cape Department of Education): SECTION A whole (Questions 1 and 2, 120 marks) and the
parts of SECTION B (Question 3) that do not read the maps (7 marks), hand-transcribed into the catalogue format, then run through
`ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and the memo's own; clues and figure
captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the question paper zip (English PDF, 16
pages, text layer) and the memo zip (English, 8 pages).

  python tools/ingest/transcribe_g11_geo_p1_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-geo-p1-2024-11-ec/GEOGRAPHY P1 QP GR11 NOV 2024 ENG D_watermark.pdf" "uploads/provincial/g11-geo-p1-2024-11-ec/GEOGRAPHY P1 MEMO GR11 NOV 2024 ENG_watermark.pdf" --id g11-geo-p1-2024-11-ec --from-json

SECTION B reads a topographical map and an orthophoto map of Hartbeespoort Dam handed out in the exam room: not in the question paper
and not in the download. As Grade 12's Geography P2 Nov 2024 (transcribe_geo_p2_2024_11.py), its 23 marks that read the maps wait for
the maps; 3.1.2 (an orthophoto's contour interval, always 5 m), 3.1.6 (the heights and the distance are in the stem), 3.3.1 and 3.3.4
play. The paper totals what is playable, 127.

The Geography rulings, as Grade 12: a choice between brackets or two columns is multiple choice of the two; a written answer is
statements (the memo's points and clearly wrong ones, a card worth what the memo ticks); a quote from an extract is a pick; the one
calculation (3.1.6) is four workings. Figure boxes are in PDF points (text blocks and image rects), 1% inside their neighbours."""
from provincial import Paper

P = Paper("g11-geo-p1-2024-11-ec", 595.22, 842.0, {
    "1.1": [3, 82.0, 177.0, 510.0, 580.0], "1.3": [6, 88.0, 88.0, 504.0, 345.0], "1.4": [7, 95.0, 108.0, 502.0, 313.0],
    "2.3": [11, 82.0, 107.0, 512.0, 330.0], "2.4": [12, 85.0, 90.0, 490.0, 336.0], "2.5": [13, 92.0, 100.0, 499.0, 336.0]}, start=0)
work, answer, stmt, mcq, term = P.work, P.answer, P.stmt, P.mcq, P.term
two = lambda n, q, a_opt, b_opt, a, clues, marks=1: mcq(n, q, [a_opt, b_opt], a, clues, marks=marks)

# ---- SECTION A, QUESTION 1: THE ATMOSPHERE, the question paper pages 3-8 and the memo pages 2-3 ----
q11 = [
    two("1.1.1", "The synoptic weather map above indicates a (summer/winter) season.", "summer", "winter", 0,
        ["Where is the South Atlantic High?", "Low pressure over the interior means summer."]),
    two("1.1.2", "The unit of measurement that indicates air pressure along the isobars is (hectopascal/millimetres).", "hectopascal",
        "millimetres", 0, ["Pressure, not rainfall.", "hPa."]),
    two("1.1.3", "The value of the calculated isobaric interval on the synoptic weather map is (2/4).", "2", "4", 1,
        ["Read two neighbouring isobars.", "The difference between them."]),
    two("1.1.4", "The area of constant pressure at C between the two high pressure systems is a (ridge/saddle).", "ridge", "saddle", 1,
        ["Between two highs and two lows.", "A pass between."]),
    two("1.1.5", "The pressure gradient at A is (gentle/steep).", "gentle", "steep", 0, ["Are the isobars far apart or close together?",
                                                                                        "Far apart means …"]),
    two("1.1.6", "The atmospheric pressure reading at letter D is approximately (1016/1024) millibars.", "1016", "1024", 1,
        ["D is in a high.", "Count up the isobars."]),
    two("1.1.7", "The pressure system between Durban and Port Elizabeth is a (coastal low/low-pressure).", "coastal low", "low-pressure", 0,
        ["Along the coast.", "Small lows that move along the coast."]),
    two("1.1.8", "Weather system B is a low-pressure system. Choose the indicator that does NOT fit.",
        "Characterised by unstable weather conditions", "Divergence occurs from the centre", 1,
        ["A low has converging air.", "Which one belongs to a high?"])]
q12 = [
    two("1.2.1", "Movement of the earth in an orbit around the sun", "rotation", "revolution", 1, ["Around the sun.", "Rotation is on its "
                                                                                                       "axis."]),
    two("1.2.2", "Theoretical wind that would result from an exact balance between Coriolis force and pressure gradient force",
        "geostrophic flow", "geostrophic balance", 0, ["A wind.", "Flow."]),
    two("1.2.3", "It is experienced in midsummer 21 December when days are longer and nights are shorter", "spring equinox",
        "summer solstice", 1, ["Longest day.", "Equinox means equal day and night."]),
    two("1.2.4", "The direction in which the slope faces in relation to the sun", "aspect", "orbit", 0, ["Which way a slope faces.",
                                                                                                         "North-facing slopes are warmer."]),
    two("1.2.5", "The zone along 60° N/S where warm subtropical air and cold polar air meet", "front", "polar front", 1,
        ["At 60°.", "Polar …"]),
    two("1.2.6", "Manner in which there is a balance between incoming solar radiation and outgoing radiation of the earth",
        "terrestrial radiation", "energy balance", 1, ["A balance.", "In equals out."]),
    two("1.2.7", "Strong winds blowing from west to east in the upper atmosphere 10 km above the earth surface", "planetary winds",
        "jet streams", 1, ["High up.", "Fast streams."])]
q13 = [
    stmt("1.3.1", "What is a primary air circulation?", 2, ["Primary circulation is the circulatory pattern of air on a global scale."],
         ["Primary circulation is a local wind between land and sea.", "Primary circulation is air moving only in valleys.",
          "Primary circulation is the circulation of water in the oceans.", "Primary circulation is the movement of a single cloud."],
         ["Primary: the biggest scale.", "Global."], 2),
    term("1.3.2", "Identify the cell represented by the sketch above.", ["Hadley cell", "Hadley"], ["Between the equator and 30°.",
                                                                                                  "Named after a scientist."]),
    term("1.3.3", "Supply a suitable name for the surface winds blowing from 30° to 0° North and South of the equator.",
         ["tropical easterlies", "trade winds", "easterly trade winds", "south-east trade winds"], ["Towards the equator.",
                                                                                                    "They blow from the east."]),
    stmt("1.3.4", "Outline the resultant weather conditions associated with the winds named in QUESTION 1.3.3.", 2,
         ["Associated with warm, steady winds.", "Associated with heavy rainfall."],
         ["Associated with snow and freezing temperatures.", "Associated with calm, windless days.", "Associated with dense fog only."],
         ["Warm air converges at the ITCZ.", "Steady and wet."], 2),
    term("1.3.5", "Name the type of cloud that is found at A.", ["cumulonimbus", "cumulonimbus clouds", "cumulonimbus cloud"],
         ["Tall thunder clouds.", "Rising moist air."]),
    stmt("1.3.6", "Explain the formation of the cell identified in QUESTION 1.3.2.", 8,
         ["The Hadley cell forms out of the inter-tropical convergence zone (ITCZ) at the equator.",
          "High temperatures at the equator heat the air, so it rises.", "As the air rises it cools and condenses, causing thunderstorms.",
          "The air sinks back to the surface at 30° N/S.", "At 30° N/S some of the air flows back towards the equator."],
         ["Cold air sinks at the equator.", "The air rises at 30° N/S and sinks at the equator.", "The cell forms over the poles."],
         ["Heating, rising, cooling, sinking.", "Equator to 30°."], 2)]
q14 = [
    stmt("1.4.1", "Define Föhn winds.", 2, ["Föhn winds are warm, dry winds that descend on the leeward side of a mountain."],
         ["Föhn winds are cold, wet winds on the windward side.", "Föhn winds are sea breezes at night.",
          "Föhn winds are winds that rise up a valley.", "Föhn winds are tornadoes over the ocean."], ["Leeward: the side away from the "
                                                                                                        "wind.", "Warm and dry."], 2),
    term("1.4.2", "Provide a suitable name for Föhn winds in South Africa.", ["berg winds", "berg wind", "bergwind"],
         ["They blow down from the plateau.", "Berg …"]),
    two("1.4.3", "Lapse rate is the rate at which the temperature of dry air decreases with an increase in height. Identify the letter on the "
        "sketch that represents dry adiabatic lapse rate and wet adiabatic lapse rate respectively.",
        "Dry adiabatic lapse rate B; wet adiabatic lapse rate A", "Dry adiabatic lapse rate A; wet adiabatic lapse rate B", 0,
        ["Dry air cools faster: 1 °C/100 m.", "Which letter has 0,5 °C/100 m?"], marks=2),
    stmt("1.4.4", "Briefly explain why the temperature of the descending air on the leeward side is higher (16,4°) than temperature on the "
         "windward side.", 2, ["The temperature increases by 1 °C/100 m as the air descends.", "Moisture evaporates as the air descends."],
         ["The air cools as it descends.", "The leeward side receives more rain.", "The air rises on the leeward side."],
         ["Descending air is compressed.", "Dry air warms faster."], 2),
    stmt("1.4.5", "In a paragraph of approximately EIGHT lines, explain the impact of Föhn winds on the environment on the leeward side of the "
         "mountain.", 8,
         ["Dry, gusty winds dry out vegetation and ignite fires.", "Melting snow results in avalanches.", "Melting snow results in flooding.",
          "Strong winds cause soil erosion.", "Fires may cause the germination of seeds."],
         ["Föhn winds bring heavy snowfall to the leeward side.", "Föhn winds increase the humidity of the air.",
          "Föhn winds cool the leeward side."], ["Warm, dry and gusty.", "Fire, snowmelt, erosion."], 2)]
DR = ("Dryland areas in Africa are under threat from deforestation, soil erosion, nutrient mining, recurrent drought and climate change, "
      "potentially resulting in land degradation, desertification, and aggravated poverty. Sustainable agricultural innovations are key to "
      "limiting adverse impacts on the environment and on the livelihoods of rural populations.")
q15 = [
    stmt("1.5.1", "Differentiate between drought and desertification.", 2,
         ["Drought is a period of abnormal scarcity of rainfall.", "Desertification is a process where once fertile soil becomes arid."],
         ["Drought is a period of heavy rainfall.", "Desertification is the planting of trees in deserts.", "Drought is a cold wind."],
         ["One is a lack of rain; one is land turning dry.", "Period and process."], 1),
    stmt("1.5.2", "State TWO causes of drought.", 4,
         ["Changing patterns of rainfall.", "Increased evaporation.", "Reduced cloud cover.", "High temperatures."],
         ["High relative humidity.", "More frequent rain."], ["Less rain, more heat.", "Weather causes."], 2),
    stmt("1.5.3", "Quote from the extract the consequences of drought.", 3, ["Land degradation", "Desertification", "Aggravated poverty"],
         ["Deforestation", "Soil erosion", "Nutrient mining"], ["Read the extract: '… potentially resulting in …'", "Results, not "
                                                                                                                    "threats."], 1),
    stmt("1.5.4", "Suggest THREE common management strategies to reduce the spread of drought and desertification.", 6,
         ["Impose water restrictions in urban areas.", "Reduce the size of cattle herds to within the land's carrying capacity.",
          "Educate the local community on best practices.", "Plant drought-resistant crops."],
         ["Increase cattle herds to use the land fully.", "Cut down trees to clear land for farming."],
         ["Save water, protect the land.", "Herds, crops, education."], 2)]

# ---- QUESTION 2: GEOMORPHOLOGY, the question paper pages 9-13 and the memo pages 4-6 ----
q21 = [
    mcq("2.1.1", "Canyon landscapes develop in:", ["Tilted sedimentary rock", "Round igneous domes", "Massive igneous rock",
                                                    "Horizontally layered rock"], 3, ["Flat layers.", "Like the Grand Canyon."], marks=1),
    mcq("2.1.2", "A small, narrow, long area of erosion on a slope is called a …", ["gorge.", "gullies.", "badlands.", "plateau."], 1,
        ["Small and narrow.", "Water cuts it."], marks=1),
    mcq("2.1.3", "Planes separating layers of rocks:", ["Bedding plain", "Peneplains", "Pediplains", "Pediments"], 0,
        ["Between layers.", "Rock beds."], marks=1),
    mcq("2.1.4", "Erosion of a slope backwards causing no loss of height of landform is called …", ["downward erosion.", "vertical erosion.",
                                                                                                    "scarp retreat.", "down wasting."], 2,
        ["Backwards.", "The scarp moves back."], marks=1),
    mcq("2.1.5", "A … is a flat-topped hill with a greater height than width.", ["butte", "mesa", "conical hill", "plateau"], 0,
        ["Taller than wide.", "A mesa is wider than tall."], marks=1),
    mcq("2.1.6", "A long, narrow, elongated hill:", ["Ridge", "Plateau", "Mesa", "Sill"], 0, ["Long and narrow.", "Not flat-topped."],
        marks=1),
    mcq("2.1.7", "A ridge with an angle of the dip slope greater than 45° is referred to as a …", ["cuesta.", "homoclinal ridge.", "canyon.",
                                                                                                     "hogsback."], 3,
        ["Steep on both sides.", "Hogs…"], marks=1),
    mcq("2.1.8", "In Ridges and Karoo landscapes, flat land that is ideal for farming is found in … and … strata. (i) horizontal (ii) inclined "
        "(iii) massive igneous intrusion (iv) domes", ["(i) and (ii)", "(ii) and (iii)", "(iii) and (iv)", "(i) and (iv)"], 0,
        ["Sedimentary layers.", "Horizontal and tilted."], marks=1)]
q22 = [
    two("2.2.1", "The peeling of rock layers due to expansion and contraction", "mechanical weathering", "exfoliation", 1,
        ["Peeling like an onion.", "A particular kind."]),
    two("2.2.2", "Granite boulders left after surrounding rock has been weathered", "tors", "core stones", 1, ["Boulders left behind.",
                                                                                                                "Cores."]),
    two("2.2.3", "Landform resulting from erosion of overlying strata to expose a batholith", "granite dome", "poort", 0,
        ["A batholith exposed.", "Rounded granite."]),
    two("2.2.4", "A saucer shaped intrusion, which is found deeper in the Earth crust", "laccolith", "lopolith", 1, ["Saucer-shaped.",
                                                                                                                     "Laccoliths bulge up."]),
    two("2.2.5", "Vertical intrusion along the sedimentary rocks that forms serrated ridges", "dyke", "sill", 0, ["Vertical.",
                                                                                                                 "Sills are horizontal."]),
    two("2.2.6", "Rocks only joined at the bottom", "dome", "tors", 1, ["A pile of blocks on bedrock.", "Not a smooth dome."]),
    two("2.2.7", "Large dome shaped intrusion of magma deep within the earth surface", "bushveld igneous complex", "batholith", 1,
        ["Large and deep.", "The general name."])]
q23 = [
    stmt("2.3.1", "Define a cuesta.", 2, ["A cuesta is a ridge with a dip slope and a scarp slope."],
         ["A cuesta is a flat-topped hill.", "A cuesta is a deep river valley.", "A cuesta is a volcanic cone.", "A cuesta is a dyke."],
         ["Two different slopes.", "A ridge."], 2),
    stmt("2.3.2", "Describe the difference between a dip slope and a scarp slope.", 2, ["The dip slope is gentle.", "The scarp slope is steep."],
         ["The dip slope is vertical.", "The scarp slope is gentle.", "Both slopes are flat."], ["Gentle and steep.", "Which is which?"], 1),
    term("2.3.3", "Provide the suitable name for the cuesta at A.", ["cuesta dome", "dome"], ["Its layers arch upwards.", "Circular."]),
    stmt("2.3.4", "How will the cuesta at B form?", 4,
         ["Magma cools down, shrinks and sags.", "This causes the rock strata to become tilted.", "Erosion and weathering result in a circular "
                                                                                                  "cuesta landscape.",
          "The dip slope faces inward towards the centre."],
         ["Magma pushes the strata upwards into an arch.", "The dip slope faces outwards."], ["B is a basin.", "Sagging."], 2),
    stmt("2.3.5", "Suggest how humans can utilise cuestas.", 6,
         ["Farming takes place in the cuesta valleys and plains.", "Cuestas are used for outdoor activities such as hang gliding.",
          "Dip slopes can be used for forestry.", "Cuesta basins are a good source of water for irrigation."],
         ["Cuestas are too steep for any human use.", "Scarp slopes are best for building cities."], ["Farming, recreation, forestry.",
                                                                                                     "Uses."], 2)]
EFGH = ["E", "F", "G", "H"]
q24 = [
    mcq("2.4.1(a)", "From the sketch above, which slope element has a convex shape?", EFGH, 0, ["Convex bulges outwards.", "At the top."],
        marks=1),
    mcq("2.4.1(b)", "From the sketch above, which slope element has a concave shape?", EFGH, 3, ["Concave curves inwards.", "At the foot."],
        marks=1),
    two("2.4.2", "A distinct change in the angle of the slope between the talus and the pediment is a (knickpoint/scarp retreat).",
        "knickpoint", "scarp retreat", 0, ["A sharp change.", "A point."]),
    term("2.4.3", "Name the geomorphological process dominant at slope element E.", ["soil creep", "creep"], ["Slow movement of soil.",
                                                                                                           "On the crest."], marks=2),
    stmt("2.4.4", "Describe the characteristics of slope elements F and G.", 4,
         ["F (the cliff) is the steepest slope element, with vertical bare rock.", "G (the talus) is made of weathered material from the cliff, "
                                                                                   "with a constant slope."],
         ["F is the flattest slope element.", "G is covered in thick soil and trees.", "F is concave and gentle."],
         ["F is the free face; G is the debris slope.", "Steep rock; loose material."], 2),
    stmt("2.4.5", "Evaluate the impact of slope element H on human activities.", 6,
         ["The pediment's weathered material is ideal for farming.", "The gentle slope favours the establishment of settlements.",
          "The gentle gradient suits recreational grounds.", "The gentle gradient eases the construction of infrastructure."],
         ["The pediment is too steep for farming.", "Nothing can be built on a pediment."], ["H is the pediment.", "Gentle and fertile."], 2)]
q25 = [
    stmt("2.5.1", "What is mass movement?", 2, ["Mass movement is the movement of loose material down a slope under the influence of gravity."],
         ["Mass movement is the movement of people to cities.", "Mass movement is wind blowing sand uphill.",
          "Mass movement is the flow of a river.", "Mass movement is a type of weather."], ["Down a slope.", "Gravity."], 2),
    term("2.5.2", "Identify the type of mass movement depicted on the photograph above.", ["rock fall", "rock falls", "rockfall",
                                                                                          "rockfalls"],
         ["Rocks have fallen onto the road.", "Read the extract."]),
    stmt("2.5.3", "Besides rainfall mentioned in the above extract, explain other possible causes of mass movement.", 4,
         ["Deforestation leaves fewer roots to bind the soil.", "Road construction and blasting at the foot of slopes upset their balance.",
          "Building on steep slopes makes rocks unstable.", "Steeper gradients cause faster movement of material."],
         ["Planting vegetation makes slopes unstable.", "Gentle slopes cause the fastest movement."], ["Human and natural causes.",
                                                                                                       "Roots, roads, building."], 2),
    stmt("2.5.4", "In a paragraph of approximately EIGHT lines, suggest strategies to minimise or prevent effects of mass movement.", 8,
         ["Drill bolts into the sides of the hill slope.", "Build gabions or stone walls at the base of a slope.",
          "Use wire mesh to hold rocks in place.", "Plant natural vegetation on slopes.", "Use early warning systems to detect land movement."],
         ["Remove all vegetation from slopes.", "Build houses at the foot of unstable slopes.", "Blast the slopes regularly."],
         ["Hold rocks in place; warn people.", "Bolts, walls, mesh, plants."], 2)]

# ---- SECTION B, QUESTION 3: the parts that do not read the maps, the question paper pages 15-16 and the memo pages 7-8 ----
CI = ["20 m.", "5 m.", "5 km.", "20 km."]
G = "VI = 1 465 m − 1 170,7 m = 294,3 m\n"
q3 = [
    mcq("3.1.2", "The contour interval on the orthophoto map is …", CI, 1, ["Orthophoto maps have a closer interval than topographic maps.",
                                                                           "Metres, not kilometres."], marks=1),
    work("3.1.6", "The horizontal equivalent between the benchmark 1170,7 m and spot height 1465 m in block B3 on the topographical map is "
         "500 m. Calculate the average gradient using the information above.", 3, [
        G + "Gradient = {294,3}/{500}\n= 1 : 1,7",                                           # the memo
        "VI = 1 465 m + 1 170,7 m = 2 635,7 m\nGradient = {2 635,7}/{500}\n= 1 : 0,19",       # added
        G + "Gradient = {500}/{294,3}\n= 1 : 0,59",                                          # upside down
        G + "Gradient = 294,3 × 500\n= 1 : 147 150"],                                        # multiplied
        ["Vertical interval = the difference in height.", "Gradient = VI ÷ HE, written as 1 : …"]),
    stmt("3.3.1", "Define a data layer.", 2, ["A data layer is a layer of information based on a specific theme."],
         ["A data layer is a layer of rock on a map.", "A data layer is the scale of a map.", "A data layer is the north arrow.",
          "A data layer is the paper a map is printed on."], ["GIS stacks themes.", "One theme."], 2),
    two("3.3.4", "The detail in which a map describes the location and shape of the feature is (spatial data/spatial resolution).",
        "spatial data", "spatial resolution", 0, ["Read the memo's GIS terms.", "Data about space."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Synoptic weather map", "marks": 8,
     "lead": "Refer to the synoptic weather map of Southern Africa. Choose the correct word/number from those given in brackets.",
     "figure": P.fig("1.1", "A synoptic weather map of Southern Africa with isobars, highs (H) and lows (L), labelled A to E: A a high over the "
                            "South Atlantic, B a low to the south, C between two highs, D a high over the Indian Ocean, E a circled area "
                            "in the north-west."), "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Column A and Column B", "marks": 7,
     "lead": "Complete the statements in COLUMN A with the options in COLUMN B.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Global air circulation", "marks": 15, "lead": "Study the sketch below.",
     "figure": P.fig("1.3", "A circulation cell from 30° N to 30° S: moist air flows in at the surface to the ITCZ, rises into cloud A, "
                            "flows out as cool, dry air aloft, loses heat by radiation and sinks as warm, dry air at 30°."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Föhn winds", "marks": 15, "lead": "Refer to the sketch below illustrating Föhn winds.",
     "figure": P.fig("1.4", "Air crossing a mountain: on the windward side it rises from 10 °C, 75% to 5 °C, 100%, cooling at the rates marked "
                            "A (0,5 °C/100 m, in the cloud) and B (1 °C/100 m, below it); on the leeward side it descends to 16,4 °C, 31%."),
     "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Drought and desertification", "marks": 15,
     "lead": "Read the extract on drought and desertification.\nDESERTIFICATION, DROUGHT AND CLIMATE CHANGE\n" + DR, "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Multiple choice", "marks": 8,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Column A and Column B", "marks": 7,
     "lead": "Choose the word/term from COLUMN B that completes the statement in COLUMN A.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Cuestas", "marks": 15, "lead": "Refer to the sketch showing cuestas.",
     "figure": P.fig("2.3", "Two block diagrams of cuestas, each with a dip slope, an escarpment and a resistant layer: A, ridges arching "
                            "upwards; B, ridges in a basin."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Slope elements", "marks": 15, "lead": "Refer to the sketch on slope elements.",
     "figure": P.fig("2.4", "A slope from top to bottom: E the rounded crest, F the vertical cliff, G the straight debris slope and H the "
                            "gentle slope at the foot."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Mass movement", "marks": 15,
     "lead": "Refer to the photograph below on mass movement.\nSTEADY RAINS CAUSING HAVOC ON THE ROADS\nThe Department of Transport has urged "
             "drivers to be cautious when approaching mountain passes, after rock falls have partially obstructed roads in two parts of the "
             "province.\nA rock fall has partially obstructed the R67 from Makhanda to Fort Beaufort, 40 km from Makhanda according to "
             "Department of Transport spokesperson, Unathi Binqose. Binqose urged road users to be extra cautious when approaching mountain "
             "passes as there are threats of mudslides. Steady rains in most parts of the province were causing havoc on the roads and "
             "mudslides had been reported on the R102 old Cape Town Road near Mondplaas in Humansdorp area as well as the R67 between "
             "Makhanda and Fort Beaufort.",
     "figure": P.fig("2.5", "A photograph: rocks and soil fallen from a steep cutting across a road, a road marker in front."), "items": q25},
    {"id": "3.1", "title": "Question 3", "kind": "Geographical skills (without the maps)", "marks": 7,
     "lead": "GENERAL INFORMATION ON HARTBEESPOORT DAM\nHartbeespoort Dam (also known as Harties) is an arch type of dam situated in the North "
             "West Province of South Africa. It lies in a valley to the south of the Magaliesberg mountain range and north of the "
             "Witwatersberg Mountain Range. (The topographical and orthophoto maps are not available: only the parts that do not read them "
             "play.)", "items": q3},
]
P.finish(missions,
         {"subject": "Geography", "title": "Geography P1", "sitting": "November 2024", "total_marks": 127, "time": "3 hours"},
         [P.flag_workings(),
          {"n": "3.1", "kind": "missing_resource", "detail": "SECTION B reads a topographical map and an orthophoto map of Hartbeespoort Dam "
                                                             "handed out in the exam room, not in the download: its 23 map-reading marks "
                                                             "(3.1.1, 3.1.3-3.1.5, 3.2.1-3.2.5, 3.3.2, 3.3.3) wait for the maps; the paper "
                                                             "plays 127."},
          {"n": "2.1.5", "kind": "memo_issue", "detail": "The memo writes 'B butte'; option B is mesa and A is butte. A flat-topped hill higher "
                                                         "than it is wide is a butte: the right option is A."},
          {"n": "2.2.6", "kind": "memo_issue", "detail": "The memo keys 'Rocks only joined at the bottom' as Y (dome); a pile of rock blocks "
                                                         "joined only at the base is a tor, Z. The right option is Z; low confidence."},
          {"n": "3.1.6", "kind": "memo_issue", "detail": "The memo writes 1 : 1,69; 500 ÷ 294,3 = 1,699, which rounds to 1 : 1,7, the right "
                                                         "option."}],
         {"1": 60, "2": 60, "3": 7}, 127, {}, "Section A whole and the Section B parts that do not read the maps")
