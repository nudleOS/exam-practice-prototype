"""Grade 11 Geography P1 November 2025 (Eastern Cape Department of Education): SECTION A whole (Questions 1 and 2, 120 marks) and the
parts of SECTION B (Question 3) that do not read the maps (16 marks), hand-transcribed into the catalogue format, then run through
`ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and the memo's own; clues and figure
captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2025 November Grade 11, the question paper zip (English PDF, 16 pages,
text layer) and the memo zip (English, 9 pages).

  python tools/ingest/transcribe_g11_geo_p1_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-geo-p1-2025-11-ec/GEOGRAPHY P1 QP GR11 NOV 2025 ENG_watermark.pdf" "uploads/provincial/g11-geo-p1-2025-11-ec/GEOGAPHY P1 MEMO GR11 NOV 2025 ENG_watermark.pdf" --id g11-geo-p1-2025-11-ec --from-json

SECTION B reads a 1:50 000 topographical map (HOWICK) and a 1:10 000 orthophoto map. The download holds a one-page HOWICK map PDF
('GEOGRAPHY-HOWICK deb'), not yet set up as a figure; as Grade 12's Geography P2, the 14 map-reading marks wait for the maps. 3.1.1,
3.1.2 and 3.1.4 (answered from the paper's own instructions), 3.2.2, 3.2.4, 3.3.2-3.3.4 play. The paper totals 136.

The Geography rulings, as in transcribe_g11_geo_p1_2024_11_ec.py. Figure boxes are in PDF points, 1% inside their neighbours."""
from provincial import Paper

P = Paper("g11-geo-p1-2025-11-ec", 595.32, 842.04, {
    "1.2": [4, 77.0, 116.0, 530.0, 377.0], "1.3": [6, 122.0, 105.0, 466.0, 384.0], "1.4": [7, 112.0, 105.0, 477.0, 376.0],
    "2.2": [10, 98.0, 118.0, 505.0, 318.0], "2.3": [11, 82.0, 118.0, 513.0, 366.0], "2.4": [12, 94.0, 105.0, 502.0, 351.0],
    "2.5": [13, 90.0, 147.0, 546.0, 326.0]}, start=0)
stmt, mcq, term, num = P.stmt, P.mcq, P.term, P.num
two = lambda n, q, a_opt, b_opt, a, clues, marks=1, **kw: mcq(n, q, [a_opt, b_opt], a, clues, marks=marks, **kw)
ABCD = ["A", "B", "C", "D"]

# ---- SECTION A, QUESTION 1: THE ATMOSPHERE, the question paper pages 3-8 and the memo pages 2-4 ----
q11 = [
    two("1.1.1", "Incoming solar energy reaching a given area", "terrestrial radiation", "insolation", 1, ["From the sun.", "Incoming."]),
    two("1.1.2", "The manner in which heat is evened out between the polar areas and the equator", "albedo", "energy balance", 1,
        ["Evening out.", "Balance."]),
    two("1.1.3", "The earth turns around its imaginary axis once every 24 hours.", "rotation", "revolution", 0, ["On its axis.", "A day."]),
    two("1.1.4", "The time of the year when midday sun is directly overhead at one of the tropics", "equinox", "solstice", 1,
        ["At a tropic, not the equator.", "Longest or shortest day."]),
    two("1.1.5", "Circular pattern on a global scale", "primary circulation", "global air circulation", 0, ["The biggest scale.", "Primary."]),
    two("1.1.6", "Difference in air pressure causing air to move from high pressure to low pressure", "pressure gradient", "Coriolis force", 0,
        ["A difference in pressure.", "Coriolis deflects."]),
    two("1.1.7", "Zones of high pressure and low-pressure areas found at different latitudes", "pressure belts", "polar front", 0,
        ["Zones round the earth.", "Belts."]),
    two("1.1.8", "The cell of air circulation that occurs between 30º ‒ 60º North and South", "Ferrell cell", "polar cell", 0,
        ["Mid-latitudes.", "The polar cell is 60°–90°."])]
q12 = [
    mcq("1.2.1", "… are large movements of water that occur in all the oceans of the world.", ["Ocean currents", "Tides", "Streams", "Waves"],
        0, ["Large and continuous.", "They flow like rivers in the sea."], marks=1),
    mcq("1.2.2", "The ocean on the West Coast of South Africa is called the …", ["Atlantic Ocean.", "Indian Ocean.", "Pacific Ocean.",
                                                                               "Benguela Ocean."], 0,
        ["West coast.", "Benguela is a current."], marks=1),
    mcq("1.2.3", "The exchange of heat between the ocean and the atmosphere mainly occurs through …", ["ocean salanity.",
                                                                                                     "wind and evaporation.",
                                                                                                     "sea floor spreading.",
                                                                                                     "tidal action."], 1,
        ["At the surface.", "Air and water vapour."], marks=1),
    mcq("1.2.4", "The … is the ocean current that flows along B.", ["Canary Current", "Mozambique Current", "Benguela Current",
                                                                   "Kuroshio Current"], 1, ["B is on the east coast.", "Warm, from the "
                                                                                                                      "north."], marks=1),
    mcq("1.2.5", "The ocean currents play a combined role in redistributing heat energy by …", ["increasing temperature.",
                                                                                               "decreasing temperature.",
                                                                                               "moderating temperatures.",
                                                                                               "increasing rainfall."], 2,
        ["Warm and cold together.", "Evening out."], marks=1),
    mcq("1.2.6", "The cold Benguela Current transfers … air from the poles to the … zone.", ["warm; coastal", "cold; temperate",
                                                                                             "warm; desert", "cold; coastal"], 1,
        ["Cold current, cold air.", "From the poles towards …"], marks=1),
    mcq("1.2.7", "Warm ocean currents move from the … to the …", ["poles; equator.", "west; poles.", "equator; poles.", "east; equator."], 2,
        ["Warm water comes from where it is hot.", "Towards cooler areas."], marks=1)]
q13 = [
    two("1.3.1", "Does the wet adiabatic lapse rate occur at A or B?", "A", "B", 0, ["Wet: where the air rises and clouds form.",
                                                                                    "The windward side."]),
    stmt("1.3.2", "Classify any TWO natural disasters that Föhn winds and other similar kinds of winds can cause.", 2,
         ["Drought", "Fires", "Avalanches", "Floods"], ["Earthquakes", "Tsunamis", "Volcanic eruptions"], ["Warm, dry, strong winds.",
                                                                                                          "Fire and snowmelt."], 1),
    stmt("1.3.3", "Why is the Föhn wind an example of a regional wind?", 2, ["Föhn winds are warm, dry winds blowing from the interior to the "
                                                                            "coast."],
         ["Föhn winds blow around the whole globe.", "Föhn winds are sea breezes.", "Föhn winds blow only inside valleys at night.",
          "Föhn winds are ocean currents."], ["A region: interior to coast.", "Not global."], 2),
    stmt("1.3.4", "Explain why no rain occurs on the leeward side of the mountain.", 2,
         ["Descending air causes available moisture to evaporate as it heats up.", "There is adiabatic warming.", "There is no condensation."],
         ["Rising air cools and condenses.", "The air gains moisture as it descends."], ["Descending air warms.", "No condensation."], 2),
    stmt("1.3.5", "Suggest measures to reduce fires caused by Föhn winds.", 8,
         ["Maintain fire breaks.", "Establish fire belts.", "Run awareness campaigns on fire safety.", "Keep an eye on weather warnings.",
          "Install early warning systems."],
         ["Burn the veld on windy days.", "Remove all fire breaks.", "Ignore weather warnings."], ["Prevent and warn.", "Breaks and "
                                                                                                                       "awareness."], 2)]
q14 = [
    num("1.4.1", "Determine the pressure reading at B.", 1012, 0, "hPa", ["B is on an isobar.", "Read its value."]),
    term("1.4.2", "Provide the term given to area D on the map.", ["saddle"], ["Between two highs and two lows.", "A col."]),
    stmt("1.4.3", "Give evidence from the synoptic weather map to prove that feature C is a low-pressure cell.", 2,
         ["There is an 'L' label at the centre.", "Atmospheric pressure increases outwards from the central point."],
         ["Pressure decreases outwards from the centre.", "There is an 'H' at the centre.", "The isobars are open lines."],
         ["L means low.", "Pressure rises outwards."], 1),
    stmt("1.4.4", "The synoptic weather map represents winter. Provide evidence from the map.", 4,
         ["A cold front brushes the land.", "The Kalahari High is over the interior.", "The South Indian and South Atlantic Highs have migrated "
                                                                                       "northwards, close to the land.",
          "A coastal low is ahead of the cold front."],
         ["A tropical cyclone over Mozambique.", "A heat low over the interior."], ["Winter: highs move north.", "Cold fronts reach the "
                                                                                                                 "land."], 2),
    stmt("1.4.5", "Determine the weather conditions experienced at A by focusing on cloud cover, wind direction and dew point temperature.", 3,
         ["Cloud cover: ¾", "Wind direction: north-west", "Dew point temperature: 13 °C"],
         ["Cloud cover: clear", "Wind direction: south-east", "Dew point temperature: 18 °C"], ["Read the station model at A.",
                                                                                                 "The lower number is the dew point."], 1),
    stmt("1.4.6", "Comment on the pressure gradient at E and the resultant wind speed.", 4,
         ["The closer the isobars, the steeper the pressure gradient.", "The closer the isobars, the stronger the wind."],
         ["Close isobars mean a gentle gradient.", "Close isobars mean calm winds.", "Pressure gradient does not affect wind speed."],
         ["Look at the spacing of the isobars at E.", "Steep gradient, strong wind."], 2)]
DD = ("DROUGHT AND DESERTIFICATION\nDrought and desertification in the Harry Gwala District Municipality, KwaZulu-Natal, impact communities "
      "through reduced water availability, diminished crop production and loss of agricultural land. This is leading to food insecurity and "
      "potential migration to urban areas. These events also cause increased run-away fires, high erosion and loss of species and habitat.")
q15 = [
    stmt("1.5.1", "What is desertification?", 2, ["The process where once fertile soil becomes arid."],
         ["A period of heavy rain.", "The planting of trees in deserts.", "The flooding of farmland.", "The building of dams."],
         ["Land turning to desert.", "Fertile becomes dry."], 2),
    stmt("1.5.2", "Quote, from the extract, environmental impacts caused by the events of drought and desertification.", 3,
         ["Loss of agricultural land", "Increased run-away fires", "High erosion", "Loss of species and habitat"],
         ["Migration to urban areas", "Food insecurity"], ["Environmental, not social.", "Land, fire, erosion, habitat."], 1),
    stmt("1.5.3", "Outline the natural causes of desertification.", 4,
         ["Climate change and shifts in weather patterns worsen desertification.", "Prolonged periods without rain reduce vegetation and soil "
                                                                                    "moisture.",
          "Uncontrolled fires destroy vegetation, increasing soil erosion."],
         ["Heavy, regular rainfall.", "Reforestation."], ["Natural, not human.", "Climate and fire."], 2),
    stmt("1.5.4", "Recommend THREE management strategies to reduce desertification.", 6,
         ["Practise land management.", "Reforest the area.", "Enhance soil fertility.", "Reduce the size of cattle herds to the land's carrying "
                                                                                         "capacity."],
         ["Increase cattle herds.", "Clear more vegetation for farming."], ["Protect the land.", "Trees, soil, herds."], 2)]

# ---- QUESTION 2: GEOMORPHOLOGY, the question paper pages 9-13 and the memo pages 5-7 ----
q21 = [
    two("2.1.1", "Cuestas is found in topography associated with …", "horizontal layers", "inclined layers", 1, ["Cuestas tilt.", "Inclined."]),
    two("2.1.2", "The landform where the layers dip at 25º to 45º", "homoclinal ridge", "hogsback", 0, ["Between a cuesta and a hogsback.",
                                                                                                       "Hogsbacks dip over 45°."]),
    two("2.1.3", "Breaking down of rocks due to extreme temperatures", "mechanical weathering", "chemical weathering", 0,
        ["Expansion and contraction.", "Physical."]),
    two("2.1.4", "Top soil becomes saturated and slides on the frozen ground beneath it", "solifluction", "soil creep", 0,
        ["Saturated, over frozen ground.", "Soil flow."]),
    two("2.1.5", "The scarp slope faces towards the centre of the dome and the dip slope faces towards the outwards", "cuesta basin",
        "cuesta dome", 1, ["The dip slopes face outwards.", "A dome."]),
    two("2.1.6", "Mushroom shaped intrusion of magma", "laccolith", "lopolith", 0, ["Mushroom.", "Lopoliths are saucers."]),
    two("2.1.7", "Vertical intrusion along sedimentary rocks", "dykes", "sills", 0, ["Vertical.", "Sills are horizontal."]),
    two("2.1.8", "The factor that distinguishes cuestas from homoclinal ridges is the …", "angle of the dip slope", "type of resistant rock", 0,
        ["Both have resistant rock.", "The angle."])]
q22 = [
    mcq("2.2.1", "Weathered material from the cliff and crest accumulates here.", ABCD, 2, ["Below the cliff.", "The talus."], marks=1),
    mcq("2.2.2", "Also known as the free face.", ABCD, 1, ["The cliff.", "Steep and bare."], marks=1),
    mcq("2.2.3", "Covered with sediments from the talus slope.", ABCD, 3, ["The gentle foot.", "The pediment."], marks=1),
    mcq("2.2.4", "It has a convex slope.", ABCD, 1, ["Read the memo's labelling of the sketch.", "Near the top."], marks=1),
    mcq("2.2.5", "The cliff retreats backward due to erosion.", ABCD, 1, ["The cliff.", "Scarp retreat."], marks=1),
    mcq("2.2.6", "The dominant geomorphological processes taking place here are weathering and soil creep.", ABCD, 1,
        ["Read the memo's labelling of the sketch.", "Near the top."], marks=1),
    mcq("2.2.7", "Vegetation grows better on this slope.", ABCD, 3, ["Gentle, with deep soil.", "At the foot."], marks=1)]
q23 = [
    two("2.3.1", "The process that is responsible for the widening of the valleys is (scarp retreat / tectonic forces).", "scarp retreat",
        "tectonic forces", 0, ["The cliffs move back.", "Erosion, not plates."]),
    stmt("2.3.2", "Comment on the general climate of this area.", 2, ["These landforms develop in an arid climate with little or no rainfall."],
         ["A wet tropical climate with daily rain.", "A cold polar climate with ice.", "A humid coastal climate.", "A snowy alpine climate."],
         ["Mesas and buttes.", "Dry."], 2),
    stmt("2.3.3", "Identify the landforms labelled C and D.", 2, ["C – mesa", "D – butte"], ["C – butte", "D – mesa", "C – canyon"],
         ["C is wider than tall.", "D is taller than wide."], 1),
    stmt("2.3.4", "Distinguish between landforms C and D.", 4, ["C: the resistant top layer is wider than its height.",
                                                                "D: the resistant top layer is smaller than its height."],
         ["C: the top layer is pointed.", "D: the top layer is wider than its height.", "C and D are the same size."],
         ["Width against height.", "Mesa and butte."], 2),
    stmt("2.3.5", "Briefly discuss the impact of the utilisation of this landscape by humans.", 6,
         ["Impressive scenery makes the canyons good tourist attractions.", "Adventure activities such as abseiling and hiking.",
          "Holiday resorts create employment for local people.", "The area around the canyon is dry and infertile.",
          "Wide canyons create a transport barrier."],
         ["The area is ideal for rice farming.", "Canyons make road building easy."], ["Tourism and barriers.", "Positive or negative."], 2)]
q24 = [
    stmt("2.4.1", "What are tors?", 2, ["Tors are exposed granite blocks made up of core stones."],
         ["Tors are deep valleys.", "Tors are sand dunes.", "Tors are volcanic craters.", "Tors are river terraces."],
         ["Granite blocks.", "Core stones."], 2),
    term("2.4.2", "Mention ONE igneous intrusion from which tors develop.", ["batholith", "laccolith", "batholiths"], ["A large intrusion.",
                                                                                                                      "Granite."]),
    stmt("2.4.3", "Describe the characteristics of the rocks mentioned in QUESTION 2.4.2.", 4,
         ["Hard and resistant.", "Prone to exfoliation (peeling of rock layers).", "There are no fossils."],
         ["Soft and easily eroded.", "Full of fossils."], ["Granite.", "Hard, no fossils."], 2),
    stmt("2.4.4", "In a paragraph of approximately EIGHT lines, explain how tors develop.", 8,
         ["Water seeps into the vertical and horizontal joints of igneous rock and chemical weathering takes place.",
          "The mass of igneous rock is broken down into rectangular blocks.", "The joints widen, and the rocks become smaller and more rounded.",
          "When the overlying material is eroded, the exposed rocks are tors."],
         ["Tors form when lava cools on the surface.", "Rivers deposit boulders in piles."], ["Joints, weathering, erosion.", "Exposure."],
         2)]
q25 = [
    stmt("2.5.1", "What is mass movement?", 2, ["Mass movement is the movement of weathered material down the slope."],
         ["Mass movement is the movement of people.", "Mass movement is wind blowing sand uphill.", "Mass movement is the flow of a river.",
          "Mass movement is a type of weather."], ["Down a slope.", "Gravity."], 2),
    term("2.5.2", "According to the extract, mention the factor that has triggered mass movement.", ["heavy rainfall", "heavy rain", "rainfall",
                                                                                                    "rain"],
         ["Read the first sentence.", "Heavy …"]),
    stmt("2.5.3", "Give evidence from the photograph, that landslides have taken place.", 2,
         ["The road has been damaged (collapsed).", "Soil has moved down the slope."], ["The road is newly built.", "The trees are green.",
                                                                                       "The sky is clear."], ["Look at the road.",
                                                                                                              "Soil out of place."], 1),
    stmt("2.5.4", "Explain the negative impact that these landslides have on people.", 4,
         ["Houses and properties may be damaged.", "Road closures force long detours.", "Damaged pipes may cause water shortages.",
          "People may be injured or lose their lives."],
         ["Landslides improve roads.", "Landslides create new farmland for people."], ["Homes, roads, services.", "Safety."], 2),
    stmt("2.5.5", "Suggest THREE strategies that can be put in place to minimise the impact of landslides.", 6,
         ["Restrict activities along slopes.", "Plant natural vegetation on slopes.", "Build retaining walls.",
          "Install systems that monitor rainfall and ground movement."],
         ["Remove vegetation from slopes.", "Build more houses on steep slopes."], ["Hold slopes; warn people.", "Plants, walls, warnings."],
         2)]

# ---- SECTION B, QUESTION 3: the parts that do not read the maps, the question paper pages 15-16 and the memo pages 8-9 ----
q3 = [
    mcq("3.1.1", "The orthophoto map is an example of a … photograph.", ["high angle oblique", "low angle oblique", "horizontal aerial",
                                                                        "vertical aerial"], 3,
        ["Taken from directly above.", "Vertical."], marks=1),
    mcq("3.1.2", "The scale of the 1 : 10 000 orthophoto map is … times … than the scale of the 1 : 50 000 topographical map. (i) five "
        "(ii) ten (iii) smaller (iv) larger", ["(i) and (iii)", "(i) and (iv)", "(ii) and (iii)", "(iii) and (iv)"], 1,
        ["50 000 ÷ 10 000.", "A smaller denominator is a larger scale."], marks=1),
    mcq("3.1.4", "The orthophoto map is an extract from 2930AC 25 HOWICK. … is the photo number for the orthophoto map.", ["29", "30", "25",
                                                                                                                           "AC"], 2,
        ["The orthophoto's name ends with its number.", "After AC."], marks=1),
    stmt("3.2.2", "Howick experiences warm summers and cool dry winters. Give the climatological reason for the numerous dams (perennial water) "
         "on the topographic map.", 2, ["Rainfall is seasonal."], ["Rain falls evenly all year.", "It never rains in Howick.",
                                                                    "Snow falls all year.", "The area is a desert."],
         ["Dry winters.", "Store water from the summer rain."], 2),
    stmt("3.2.4(a)", "The landform at point 8 on the orthophoto map is a ridge. Define the term ridge.", 2,
         ["A ridge is a long, relatively narrow, high-lying area."], ["A ridge is a deep, wide valley.", "A ridge is a flat plain.",
                                                                     "A ridge is a round hill.", "A ridge is a river bend."],
         ["Long and narrow.", "High."], 2),
    stmt("3.2.4(b)", "Outline the significance of a ridge.", 2, ["It acts as a habitat for various species.", "It influences the flow of "
                                                                                                             "water.",
                                                               "It attracts tourists."], ["It stops all rainfall.", "It is always a mine."],
         ["Habitat, water, tourism.", "Why does a ridge matter?"], 2),
    two("3.3.2", "Is the topographic or orthophoto map a primary source?", "Topographic map", "Orthophoto map", 1,
        ["A photograph taken directly.", "First-hand."]),
    stmt("3.3.3", "Give a reason for the answer in QUESTION 3.3.2.", 2,
         ["The orthophoto map has first-hand information.", "Photographs are taken directly from the source.", "There is less manipulation."],
         ["It is drawn by hand from other maps.", "It shows symbols instead of photographs."], ["First-hand.", "Directly from the source."],
         2, after=["3.3.2"]),
    stmt("3.3.4", "Explain the difference between spatial resolution and spectral resolution.", 4,
         ["Spatial resolution: the level of detail visible in an image, how sharp it appears.",
          "Spectral resolution: how many colours (wavelengths) a sensor captures and differentiates."],
         ["Spatial resolution: the number of colours captured.", "Spectral resolution: the scale of a map.", "Both mean the size of the map."],
         ["Detail versus colour.", "Space and spectrum."], 2)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Column A and Column B", "marks": 8,
     "lead": "Complete the statements in COLUMN A with the options in COLUMN B.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Ocean currents", "marks": 7, "lead": "Refer to the sketch below.",
     "figure": P.fig("1.2", "An outline of South Africa with an ocean current A along the west coast flowing north and a current B along the "
                            "east coast flowing south."), "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Föhn winds", "marks": 15, "lead": "Refer to the sketch below.",
     "figure": P.fig("1.3", "Air rising up a mountain at A, a rain cloud above the windward side, and air descending the other side at B, the "
                            "sun above."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Synoptic weather map", "marks": 15, "lead": "Refer to the synoptic weather map of Southern "
                                                                                                "Africa.",
     "figure": P.fig("1.4", "A synoptic weather map of Southern Africa: highs (H) and lows (L), a station model at A (18 and 13 beside a part-"
                            "filled circle with a wind arrow), a low B, a low C, D between two highs and two lows, and closely spaced isobars "
                            "at E near a cold front."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Drought and desertification", "marks": 15,
     "lead": "Read the extract below on the effects of drought and desertification in Harry Gwala District Municipality.\n" + DD,
     "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Column A and Column B", "marks": 8,
     "lead": "Complete the statements in COLUMN A with the options in COLUMN B.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Slope elements", "marks": 7,
     "lead": "Refer to the sketch below showing slope elements. Write only the letter (A–D).",
     "figure": P.fig("2.2", "A block of land: A on the flat top near the edge, B at the cliff, C on the debris below it and D on the gentle "
                            "slope at the foot."), "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Horizontally layered rocks", "marks": 15,
     "lead": "Refer to the sketch below showing topography associated with horizontally layered rocks.",
     "figure": P.fig("2.3", "A layered landscape cut by valleys, with a flat-topped hill C, wider than it is tall, and a smaller flat-topped "
                            "hill D, taller than it is wide."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Tors", "marks": 15, "lead": "Refer to the sketch below showing tors.",
     "figure": P.fig("2.4", "A photograph of stacked granite blocks on a grassy hilltop."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Mass movement", "marks": 15,
     "lead": "Refer to the photograph and extract below showing mass movement.\nHEAVY RAINS TRIGGER LANDSLIDES IN PORT ST. JOHNS, EC\nFRIDAY 24 "
             "MARCH 2023 – 10:30 am\nHeavy rainfall in Port St. Johns has recently triggered landslides and widespread flooding, causing "
             "significant damage to homes, roads and infrastructure. Mayor Nomvuzo Mlobile Cingos says she 'is expecting disaster management "
             "teams to arrive in the next few hours'. Gift of the Givers has also volunteered to help those affected by floods.",
     "figure": P.fig("2.5", "Two photographs: a road with its edge collapsed down a slope, and soil slid down a hillside below a house."),
     "items": q25},
    {"id": "3.1", "title": "Question 3", "kind": "Geographical skills (without the maps)", "marks": 16,
     "lead": "GENERAL INFORMATION ON HOWICK\nHowick is a town located in the Umngeni Local Municipality of KwaZulu-Natal Province, South Africa. "
             "The town is 1 050 m above sea level, and about 88 kilometres from the port city of Durban. It experiences warm summers and cool "
             "dry winters. A 1 : 50 000 topographical map (EXTRACT from 2930 AC and AD HOWICK) and a 1 : 10 000 orthophoto map (EXTRACT from "
             "2930AC 25 HOWICK ortho-rectified image) go with the paper: only the parts that do not read them play.", "items": q3},
]
P.finish(missions,
         {"subject": "Geography", "title": "Geography P1", "sitting": "November 2025", "total_marks": 136, "time": "3 hours"},
         [{"n": "3.1", "kind": "missing_resource", "detail": "SECTION B reads the HOWICK topographical and orthophoto maps: the download holds a "
                                                             "one-page HOWICK map PDF not yet set up as a figure, so the 14 map-reading marks "
                                                             "(3.1.3, 3.1.5, 3.1.6, 3.2.1, 3.2.3, 3.3.1) wait; the paper plays 136."},
          {"n": "2.2.4", "kind": "low_confidence", "detail": "The memo keys 2.2.4 (convex slope) and 2.2.6 (weathering and soil creep) as B, the "
                                                             "letter it also gives the free face (2.2.2); on the sketch the crest is near A. "
                                                             "Played as the memo keys them; low confidence."}],
         {"1": 60, "2": 60, "3": 16}, 136, {"3.3.3": ["3.3.2"]}, "Section A whole and the Section B parts that do not read the maps")
