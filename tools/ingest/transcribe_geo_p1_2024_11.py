"""Geography P1 Nov 2024: SECTION A whole (Questions 1 and 2, 120 marks) and the parts of SECTION B (Question 3) that do not read
the maps (9 marks), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the memo's points are the paper's and the
memo's own; clues and figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_geo_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Geography P1 Nov 2024 Eng.pdf" "<...>/Geography P1 Nov 2024 MG Eng.pdf" --id geo-p1-2024-11 --from-json

SECTION B reads a 1:50 000 topographical map (2829DB LADYSMITH) and a 1:10 000 orthophoto map (2829 DB 6 LADYSMITH) handed out in
the exam room: not in the question paper and not published. Its 21 marks that read the maps (3.1.1-3.1.6, 3.2.2-3.2.7, 3.3.3)
wait for the maps; the paper totals what is playable, 129.

The memo's shapes map as in Geography P1 Nov 2025 (transcribe_geo_p1_2025_11.py), with what Business Studies taught (2026-10-10):
the memo's "MUST refer to ..." and part-marking instructions are `notes` or `must`, never bullet text; only an alternative answer's
first point starts with "OR"; a point whose words are all short (no word over five letters) is written so the marker can read it:
a slash alternative gives a short word a keyword partner ("dry/dryness"), and an optional label goes in brackets ("(Wind A:)").
Figure boxes are measured in PDF points (page 595.32 x 841.92), found with scratchpad figs24.py and checked on rendered crops."""
import json
from pathlib import Path

W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.1": [3, 98, 207, 524, 354], "1.2a": [5, 78, 166, 542, 299], "1.2b": [5, 84, 470, 522, 644], "1.3": [6, 144, 110, 475, 316],
    "1.4": [7, 44, 114, 542, 627], "1.5": [8, 45, 299, 562, 627], "2.1.6": [9, 378, 341, 529, 398], "2.1.7": [9, 383, 415, 529, 504],
    "2.2.1": [10, 236, 179, 439, 328], "2.2.3": [10, 233, 537, 441, 658], "2.2.5": [11, 235, 228, 439, 379], "2.2.7": [11, 198, 583, 419, 717],
    "2.3": [12, 96, 275, 476, 490], "2.4": [13, 142, 110, 491, 280]}


INSET = {"2.1.6": 40, "2.1.7": 40, "2.3": 40, "1.3": 40}  # a label touches the crop's top-left corner, where the page's Hide button sits


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"inset": INSET[name]} if name in INSET else {})}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None, must=None, notes=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {}), **({"notes": notes} if notes else {})}


term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}

HIGHS = ("Two sketches of South Africa. A: a high (H) over the interior, a high just off the west coast, a high just off the east coast, "
         "and a low (L) on the south coast. B: a low (L) over the interior, a stretched-out high far off the south-west coast, and a high "
         "far off the south-east coast.")
VALLEYS = ("Two valley cross-sections. A: arrows run DOWN both slopes to the valley floor, labelled 'Cold air'. B: arrows run UP both "
           "slopes from the valley floor, labelled 'Warm air'.")
DOMES = ("Two sketches of a city skyline (Urban area) under a pollution dome. A: a tall, high dome with arrows pointing UP inside it. "
         "B: a low, flattened dome with arrows pointing DOWN onto the city.")
CONFLUENCE = ("Two sketches of a main stream flowing to the right, joined by a smaller stream from the lower left. Y: the circle sits on "
              "the smaller stream, before it reaches the main stream. Z: the circle sits on the point where the smaller stream meets the "
              "main stream.")
DIVIDES = ("Two sketches. KEY: a hatched line marks a high-lying area; lines with arrows are streams. Y: the high-lying area runs between "
           "two separate stream networks that flow away in different directions and never meet. Z: the high-lying area runs between two "
           "streams that join each other just beyond it.")

# ---- QUESTION 1: CLIMATE AND WEATHER, the question paper pages 3-8 and the memo pages 4-7 ----
q11 = [mcq(n, q, o, a, c, figure=fig("1.1", HIGHS)) for n, q, o, a, c in [
    ("1.1.1", "Sketch A shows typical ... conditions.", ["summer", "spring", "winter", "autumn"], 2,
     ["A high sits over the interior.", "The interior is high and cold in which season?"]),
    ("1.1.2", "The low-pressure system in sketch B forms due to ... over the land.",
     ["low evaporation", "intense heating", "cold dense air", "heavy rainfall"], 1,
     ["Sketch B: a low over the interior.", "Hot ground heats the air, which rises."]),
    ("1.1.3", "... is the concept used to describe the elongation of the isobars associated with the South Atlantic anticyclone in sketch B.",
     ["Backing", "Divergence", "Ridging", "Convergence"], 2,
     ["A high pushing a tongue of isobars outwards.", "The same word as the top of a mountain range."]),
    ("1.1.4", "The anticyclones in sketch A and B change their positions seasonally because of the ...",
     ["rotation of the Earth.", "frictional drag.", "shifting of the ITCZ.", "Coriolis force."], 2,
     ["The highs move north in winter and south in summer.", "The pressure belts follow the overhead sun."]),
    ("1.1.5", "The South Indian anticyclone in sketch B is likely to feed more moisture over the east coast in comparison with sketch A because "
     "it ...", ["is a blocking high.", "has a larger fetch (distance).", "diverges dry air.", "has a smaller fetch (distance)."], 1,
     ["In sketch B the high lies further out to sea.", "Air that crosses more ocean picks up more moisture."]),
    ("1.1.6", "The low-pressure system in sketch A will move in a ... direction.", ["northerly", "westerly", "easterly", "southerly"], 2,
     ["It is a coastal low on the south coast.", "Coastal lows travel round the coast from west to east."]),
    ("1.1.7", "Berg winds are most likely to develop in sketch A because of the presence of the ... and ...\n(i) Kalahari anticyclone\n"
     "(ii) coastal low\n(iii) South Indian anticyclone\n(iv) heat low", ["(i) and (ii)", "(ii) and (iii)", "(i) and (iv)", "(iii) and (iv)"], 0,
     ["Berg winds blow from the interior down to the coast.", "A high inland pushes air towards a low at the coast."]),
    ("1.1.8", "The inversion layer that forms over the escarpment in sketch B will favour the formation of ... and ...\n(i) frost\n(ii) rainfall\n"
     "(iii) fog\n(iv) hail", ["(i) and (ii)", "(i) and (iii)", "(ii) and (iv)", "(iii) and (iv)"], 2,
     ["Sketch B is summer, with a low over the interior.", "Think of summer thunderstorms on the plateau."])]]
q12 = [mcq(n, q, ["A", "B"], a, c, figure=fig(f, cap)) for n, q, a, c, f, cap in [
    ("1.2.1", "Represents an anabatic wind", 1, ["Anabatic winds blow UP the slopes.", "Which sketch has arrows going up?"], "1.2a", VALLEYS),
    ("1.2.2", "Cold air forces the warm air to rise which forms an inversion layer", 0,
     ["Cold air sinks into the valley at night.", "Which sketch has cold air flowing down?"], "1.2a", VALLEYS),
    ("1.2.3", "Occurs during the day due to insolation", 1, ["The sun heats the slopes in the day.", "Warm air rises up the slopes."], "1.2a", VALLEYS),
    ("1.2.4", "Frost forms on the valley floor when the temperature drops below 0 °C", 0,
     ["Frost needs the coldest air.", "Where does the cold air collect?"], "1.2a", VALLEYS),
    ("1.2.5", "Represents a pollution dome at night", 1, ["At night the air near the ground is cold and sinks.", "Which dome is pressed down?"],
     "1.2b", DOMES),
    ("1.2.6", "Pollutants are dispersed", 0, ["Rising air carries pollutants upwards and away.", "Which dome is tall?"], "1.2b", DOMES),
    ("1.2.7", "Denser concentration of pollutants over the urban area", 1, ["A low lid traps the pollution close to the city.",
                                                                           "Which dome is flattened?"], "1.2b", DOMES)]]
q13 = [
    term("1.3.1", "In which general direction do mid-latitude cyclones move?", ["West to east", "From west to east", "Eastwards", "Eastward", "East"],
         ["Read the arrow under the sketch.", "W on the left, E on the right."]),
    rub("1.3.2", "Give a reason for your answer to QUESTION 1.3.1.", 2, ["Driven by the westerlies (2).", "Occurs in the westerly wind belt (2)."],
        ["Which wind belt are mid-latitude cyclones found in?", "The wind belt that blows from the west."], each=2),
    rub("1.3.3", "How does front A give rise to the formation of cumulonimbus clouds?", 4, [
        "Cold front will undercut the warm air (ahead of it) (2).", "The steeper gradient will cause rapid uplift of the warm air (2).",
        "Cooling and condensation occurs (2)."],
        ["Front A is the steep one: a cold front.", "Cold air pushes under the warm air: what happens to the warm air?"], each=2),
    rub("1.3.4", "In a paragraph of approximately EIGHT lines, explain strategies that can be put in place to manage the negative environmental "
        "impact of the heavy rainfall associated with mid-latitude cyclones.", 8, [
        "Maintain natural vegetation (2).", "Encourage afforestation (2).", "Buffering of the area (2).", "Create effective drainage systems (2).",
        "Use of sandbags (2).", "Building of retaining walls (accept examples) (2).", "Use of catch nets (areas prone to rockfalls) (2).",
        "Use of canopies (areas prone to rockfalls) (2).", "Construction of gabions (2).", "Construct dams (wall)/weir (2).",
        "Construct artificial levees/barriers (2).", "Conserve wetlands/marshes/swamps (2).", "Implement contour ploughing (2).",
        "Terracing of slopes (2).", "Widening river channels (water management systems) (2).", "Canalising rivers (2).",
        "Educate people about environmental conservation (2).", "Awareness/early warning systems (2)."],
        ["Heavy rain brings flooding, soil erosion and mass movements.", "Four strategies: plants, structures and people."], each=2)]
q14 = [
    lst("1.4.1", "State ONE condition that could have led to the development of Tropical Cyclone Filipo.", 1,
        [["Low-pressure system", "Low pressure", "Convergence of air", "Convergence"], ["Coriolis force", "Coriolis"],
         ["Sea surface temperatures of 26,5 °C or more", "Warm sea surface temperatures", "Warm ocean", "Warm sea", "Warm water"],
         ["Calm conditions over the oceans", "Calm conditions"], ["Unstable conditions", "High rates of evaporation", "Evaporation", "High humidity"],
         ["Latent heat", "Production of latent heat"], ["Upper air divergence", "Divergence in the upper air"]],
        ["Tropical cyclones need a lot of energy from the sea.", "Think of the temperature of the water."]),
    lst("1.4.2", "Give evidence from the map and table of information that Tropical Cyclone Filipo had strengthened from 10 to 11 March.", 2,
        [["Exposed to more moisture over the ocean", "Over the ocean", "Moved over the ocean", "More moisture"],
         ["Wind speed increased from 63 km/h to 95 km/h/116 km/h", "Wind speed increased", "Increase in wind speed", "63 km/h to 95 km/h",
          "63 km/h to 116 km/h", "95 km/h", "116 km/h"]],
        ["Where was it on 10 and 11 March: over land or over the sea?", "Compare the wind speeds in the table."]),
    rub("1.4.3", "Give TWO reasons for the decrease in wind speed from 06:00 to 18:00 on 12 March.", 4, [
        "Moved over the land OR less moisture (2).", "More friction (2).", "Less latent heat (2).", "(Starting to) dissipate/weaken (2)."],
        ["Where was the cyclone on 12 March?", "Over land it loses its supply of moisture and meets more friction."], each=2),
    draw("1.4.4", "On 14 March, Tropical Cyclone Filipo reached the mature stage. In the ANSWER BOOK, draw a labelled cross-section of Tropical "
         "Cyclone Filipo in its mature stage. Marks will be awarded for the following:\n(a) Cross-section\n(b) Cloud type\n(c) Eye\n"
         "(d) Air movement in the eye", 4, [
        ["Cross-section: towering clouds on both sides of a clear centre", 1], ["Cloud type: cumulonimbus (Cb)", 1],
        ["Eye: labelled at the centre", 1], ["Air movement in the eye: arrows pointing down (sinking air)", 1]],
        ["A mature tropical cyclone is a ring of storms around a calm centre.", "In the eye the air sinks."]),
    rub("1.4.5", "Account for the lack of rainfall and clouds in the eye of the tropical cyclone.", 4, [
        "Air subsides (2).", "The air heats up (2). ACCEPT: the air is heated/warmed.", "Moisture gets evaporated/air is dry (2).",
        "No condensation takes place (2)."],
        ["What does the air do in the eye: rise or sink?", "Sinking air warms up: can clouds form?"], each=2)]
q15 = [
    term("1.5.1", "According to the extract, in which season do line thunderstorms commonly occur?", ["Summer"],
         ["Read the first sentence of the extract.", "The rainy season on the plateau."]),
    rub("1.5.2", "Describe the temperature and moisture content of wind A and wind B that led to the formation of the line thunderstorm.", 4, [
        "(Wind A:) cold/colder (1).", "(Wind A:) dry/dryness (1).", "(Wind B:) warm/warmer (1).", "(Wind B:) moist/humid/wet (1)."],
        ["Wind A comes from the high in the south-west, over the cold Atlantic.", "Wind B comes from the north-east, from the warm Indian Ocean."],
        notes=["Wind A (south-westerly) is cold and dry; wind B (north-easterly) is warm and moist. Part marks: cold (1) or dry (1) for A, warm "
               "(1) or moist (1) for B; a maximum of two marks for part answers."]),
    rub("1.5.3", "Explain why the heaviest rainfall occurs closest to the moisture front, as evident in the source.", 4, [
        "Rapid uplift of air along the moisture front (2).", "Greater/more (vertical) condensation (2).", "(Dense line of) cumulonimbus clouds form (2).",
        "OR — Less uplift of air further from the moisture front (2).", "Less (vertical) condensation (2).", "Less clouds form (2)."],
        ["Air rises fastest where the cold and warm air meet.", "More rising air means more condensation and bigger clouds."], each=2,
        notes=["MUST refer to either close to OR further from the moisture front."]),
    rub("1.5.4", "Explain the negative physical (natural) impact of line thunderstorms.", 6, [
        "Natural habitats will be destroyed (2).", "Ecosystems will be destroyed (2).", "Biodiversity will be reduced (2).",
        "Top soil will be washed away/soil erosion (2).", "Mass movements can be triggered (accept examples) (2).",
        "Wildlife would be displaced/drowned (2).", "Trees/natural vegetation can be uprooted/destroyed (2).", "Water quality will be reduced (2).",
        "Increased leaching of soil (2).", "Sinkholes form (2).", "Silting up/deposition of material (2)."],
        ["Physical: the impact on nature, not on people.", "Damaging winds, hail and heavy rain: plants, animals, soil and water."], each=2)]

# ---- QUESTION 2: GEOMORPHOLOGY, the question paper pages 9-14 and the memo pages 8-10 ----
q21 = [
    mcq("2.1.1", "Area drained by a river and its tributaries", ["catchment area", "drainage basin"], 1,
        ["Both terms are close: one is the area that collects the rain, one the area the river system drains.", "The area DRAINED by a river."]),
    mcq("2.1.2", "Promotes a rapid rise in the water table", ["gentle gradient", "steep gradient"], 0,
        ["The water table rises when water soaks in.", "On which slope does water have time to soak in?"]),
    mcq("2.1.3", "The upper level of ground water", ["water table", "through flow"], 0,
        ["Ground water fills the soil and rock below a certain level.", "The top of the saturated zone."]),
    mcq("2.1.4", "Seepage of water into the ground", ["infiltration", "run-off"], 0,
        ["Run-off flows over the surface.", "Water soaking IN is ..."]),
    mcq("2.1.5", "Causes reduction of surface run-off", ["impermeable rocks", "dense vegetation"], 1,
        ["Water cannot soak into impermeable rock.", "What slows water down and lets it soak in?"]),
    mcq("2.1.6", "The confluence is located at Y/Z", ["Y", "Z"], 1,
        ["A confluence is where two streams meet.", "Which circle marks a meeting point?"], figure=fig("2.1.6", CONFLUENCE)),
    mcq("2.1.7", "High-lying area separating two tributaries in the same river system", ["Y", "Z"], 1,
        ["Same river system: the two streams belong together and meet.", "A watershed separates two different river systems."],
        figure=fig("2.1.7", DIVIDES))]
q22 = [
    mcq("2.2.1", "... is responsible for the shape of the river valley below.", ["Deposition", "Lateral erosion", "Weathering", "Vertical erosion"], 3,
        ["The valley is a narrow V.", "The river cuts downwards."],
        figure=fig("2.2.1", "A block sketch of a narrow, steep-sided V-shaped valley with a small stream at the bottom.")),
    mcq("2.2.2", "A ... forms at the base of a waterfall.", ["braided stream", "delta", "gorge", "plunge pool"], 3,
        ["Falling water hits the bottom hard.", "It digs a deep pool."]),
    mcq("2.2.3", "The fluvial landform/feature depicted in the sketch is a ...", ["waterfall.", "valley.", "rapid.", "cliff."], 2,
        ["Several small steps, not one big drop.", "Water tumbles over outcrops of hard rock."],
        figure=fig("2.2.3", "A sketch of a river bed with a series of small steps: soft rocks wear away between outcrops of harder rock, and arrows "
                   "show the water tumbling down over the steps.")),
    mcq("2.2.4", "The flat, low-lying area along the banks of a river in the lower course is a/an ...",
        ["meander.", "delta.", "flood plain.", "alluvial fan."], 2,
        ["It is covered in water when the river floods.", "Flat land beside the river in its lower course."]),
    mcq("2.2.5", "The slope at X on the inner bank of a meander is also referred to as a/an ... slope.", ["steep", "undercut", "concave", "slip-off"], 3,
        ["The inner bank is where the river deposits.", "A gentle slope that slips off into the water."],
        figure=fig("2.2.5", "A sketch of a winding river; an arrow labelled X points to the inside of one bend.")),
    mcq("2.2.6", "A/An ... forms when the meander loop is cut off from the main stream.", ["delta", "rapid", "ox-bow lake", "flood plain"], 2,
        ["The cut-off loop holds still water.", "A curved lake beside the river."]),
    mcq("2.2.7", "The benefit of natural levees is ... on the flood plain.",
        ["increased deposition", "reduced flooding", "reduced fertility", "increased flooding"], 1,
        ["Levees are raised banks along the river.", "What do higher banks hold back?"],
        figure=fig("2.2.7", "A cross-section of a river channel on a flood plain with raised ridges labelled Natural levees along both banks.")),
    mcq("2.2.8", "Deltas form at the river mouth when the following conditions occur:\n(i) Shallow sea bed\n(ii) Steep sea bed\n"
        "(iii) Strong currents\n(iv) Small tidal range", ["(i) and (ii)", "(ii) and (iii)", "(iii) and (iv)", "(i) and (iv)"], 3,
        ["A delta is sediment that the sea does not wash away.", "Shallow water and weak tides let it build up."])]
q23 = [
    term("2.3.1", "Identify drainage pattern A.", ["Radial", "Centrifugal", "Radial drainage pattern"],
         ["The streams spread out in all directions.", "Like the spokes of a wheel."]),
    term("2.3.2", "Determine the stream order of X in drainage pattern A.", ["2nd", "Second", "2", "Second order", "2nd order"],
         ["Two first-order streams join to form ...", "X is below the point where two streams join."], marks=2),
    rub("2.3.3", "Give a reason for the direction in which streams flow in drainage pattern A.", 2, [
        "Radiates outwards/away from a high-lying central point/centre (accept examples of landforms) (2)."],
        ["Where do all the streams start?", "Water flows down from a high point in the middle."], each=2),
    rub("2.3.4", "How does the joining of the tributaries to the mainstream differ in drainage patterns A and B?", 2, [
        "The tributaries join the main river at acute angles at A and at right angles at B (2)."],
        ["Look at the angle where each tributary meets its main stream.", "Sharp angles or square corners?"], each=2),
    rub("2.3.5", "State TWO conditions associated with the underlying rock that contributed to the formation of trellis drainage pattern B.", 4, [
        "Alternate layers of hard/resistant and soft rock (varying resistance) (2).", "Folded rocks (2)."],
        ["Trellis patterns form where rock layers differ.", "Hard and soft layers, bent by earth forces."], each=2),
    rub("2.3.6", "Why are human activities limited in areas where drainage patterns A and B are found?", 4, [
        "Land is steep/uneven (2).", "Prone to soil erosion/thin soils (2).", "Infertile soils (2).", "Risk of mass movements (2).",
        "High cost of developing land (2)."],
        ["A: a dome or mountain. B: folded ridges and valleys.", "What makes it hard to farm or build there?"], each=2)]
q24 = [
    rub("2.4.1", "Define the term river rejuvenation.", 2, [
        "When the river experiences an increase in energy (erodes vertically) (2). ACCEPT: the river gains (more) energy and erodes "
        "vertically/downwards."],
        ["Rejuvenate means to make young again.", "The river gains energy and cuts down."], each=2,
        notes=["Concept: an increase in the river's energy, so it erodes vertically."]),
    term("2.4.2", "Identify the feature at A.", ["Knickpoint", "Knick point", "Waterfall"],
         ["A marks a sudden break in the river's long profile.", "Where the old and new profiles meet."]),
    rub("2.4.3", "How does feature A indicate that river rejuvenation has taken place?", 2, [
        "Change/drop in gradient (2).", "(Evidence of) vertical erosion (2).", "Water flowing/flows faster (2).",
        "(Evidence of) old and new river profiles (2)."],
        ["A is a break in the slope of the river.", "Why would a rejuvenated river have a sudden drop?"], each=2),
    rub("2.4.4", "Describe the change that river rejuvenation has made to the landscape at B.", 2, [
        "It formed a valley in a valley (2).", "The river channel got deeper/steeper/wider (2)."],
        ["B is the new valley cut into the old valley floor.", "What did the downward erosion do to the channel?"], each=2),
    rub("2.4.5", "How do river terraces form?", 4, [
        "Vertical erosion occurs on the flood plain (2).", "A new (river) valley is formed/forms/created (2).",
        "(This creates) a step-like feature/landform (known as a terrace) (2).", "The old flood plain/floodplain is now the river terrace (2)."],
        ["The river cuts down into its old flood plain.", "The old flood plain is left high up as a step."], each=2),
    rub("2.4.6", "Why are some river terraces not suitable for farming?", 4, [
        "Far/distant from water sources (2).", "Difficult/expensive to build infrastructure (accept examples) (2).",
        "River terraces can be very narrow (2).", "Limit use of machinery (2).", "(Decrease in) soil fertility/infertile/thin soils (2).",
        "Uneven slopes/rugged landscape (2).", "Unstable soil OR mass movement (accept examples) (2)."],
        ["Terraces sit high above the river.", "Think water, space, soil and slopes."], each=2)]
q25 = [
    rub("2.5.1", "What is river management?", 2, [
        "Monitoring and controlling (management) of water resources in a drainage basin/catchment area (2)."],
        ["Management means looking after something.", "Watching over and controlling a river's water."], each=2,
        notes=["Concept: the monitoring and controlling of water resources in a drainage basin."]),
    term("2.5.2", "Name ONE human activity in the extract that has a negative impact on South Africa's catchment areas.",
         ["Agriculture", "Agricultural activities", "Agricultural run-off", "Farming"],
         ["Read the extract's second paragraph.", "Run-off from which activity carries chemicals?"]),
    rub("2.5.3", "How does the human activity (answer to QUESTION 2.5.2) negatively impact the health (water quality) of a catchment area?", 4, [
        "Causes eutrophication/reduction in oxygen levels (2).", "Imbalance in the nutrient levels in the river (2).", "Reduction in biodiversity (2).",
        "Reduction in fauna and flora (2).", "Water pollution (accept examples) (2).", "Increase in water borne diseases (2).",
        "Ecosystems/natural habitats are disrupted (2).", "Water table will be lowered (2).", "Increase in soil erosion (2)."],
        ["Fertilisers and chemicals wash into the river.", "What happens to the water, the plants and the animals?"], each=2),
    rub("2.5.4", "In a paragraph of approximately EIGHT lines, suggest sustainable strategies the government can put in place to preserve river "
        "catchment areas.", 8, [
        "Educational programmes (2).", "Awareness programmes (accept examples) (2).", "Implement legislation/laws/conservation zones (accept examples) (2).",
        "Impose fines (2).", "Improve waste water/grey water treatment (2).", "Create buffer zones (accept examples) (2).", "Encourage afforestation (2).",
        "Remove alien vegetation (2).", "Proper sewerage/water purification systems (2).", "Maximise wastewater/grey water usage (2).",
        "Frequent testing of water (2).", "Conserve wetlands (2).", "Recycle agricultural/domestic/industrial waste (2).",
        "Maintain/construct water infrastructure (2).", "Sustainable farming (accept examples) (2).", "Encourage rain water harvesting (2)."],
        ["The government makes laws, educates and builds infrastructure.", "Four strategies, each in a full sentence."], each=2)]

# ---- QUESTION 3 (SECTION B): only the parts that do not read the maps, the question paper pages 15-17 and the memo pages 11-12 ----
LADYSMITH = ("GENERAL INFORMATION ON LADYSMITH\n\nCoordinates: 28°33'S; 29°46'E\n\nLadysmith is a city in the Uthukela District of KwaZulu-Natal. "
             "It is situated along the Klip River. The climate is warm and temperate with the highest rainfall recorded in summer. The average "
             "annual temperature is 17,3 °C. The average annual precipitation is approximately 1 057 mm. This climate provides ideal conditions "
             "for agricultural raw materials.")
q3a = [
    term("3.2.1(a)", "The temperature at F, in the centre of the town, is 2 °C higher than at G, outside the centre. Name the concept that "
         "describes this difference.", ["Urban heat island", "Urban heat island effect", "Heat island"],
         ["Towns are warmer than the countryside around them.", "An 'island' of heat over the town."]),
    rub("3.2.1(b)", "Give ONE reason why the high density of buildings at F generally contributes to the higher temperatures.", 2, [
        "Heat will get trapped (2).", "Reduced wind speed (2).", "Reduced air flow (2).", "Artificial surfaces (2).", "Multiple reflections (2)."],
        ["Buildings close together block the wind.", "Concrete and tar absorb heat and bounce it between walls."], each=2)]
q3b = [
    mcq("3.3.1", "The vertical aerial photograph used to make the 1:10 000 orthophoto map has a (high/low) resolution.", ["High", "Low"], 0,
        ["Resolution is how much detail an image shows.", "An orthophoto shows individual buildings and roads."]),
    mcq("3.3.2", "The reference (key) of the topographical map represents (spatial/attribute) data.", ["Spatial", "Attribute"], 1,
        ["Spatial data says WHERE a feature is.", "The key tells you WHAT each symbol is."]),
    rub("3.3.4", "Define the term buffering.", 2, ["The demarcation of an area around/along a geographical feature/location (2)."],
        ["A buffer is a protective zone.", "A zone drawn around something."], each=2, notes=["Concept: a zone demarcated around a feature."]),
    rub("3.3.5", "How would buffering beside the Klip River protect the quality of the water in the river?", 2, [
        "Restrict development on the banks of the river (2).", "Decrease pollution from the built-up area (2).",
        "Reduces eroded soil from entering the river (2).", "Decreased eutrophication (2).", "Reduces salinity (2).",
        "The natural course/capacity of the river will be maintained (2).", "Biodiversity of the river will be preserved (2)."],
        ["A buffer keeps buildings and activities away from the river.", "What would no longer reach the water?"], each=2)]

sec_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Anticyclones", "marks": 8,
     "lead": "Refer to sketches A and B below. Various options are provided as possible answers to the following questions based on the "
             "influence of anticyclones in South Africa.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Valley climates and pollution domes", "marks": 7,
     "lead": "Match the descriptions below with sketches A and B. Sketches A and B on valley climates are for QUESTIONS 1.2.1 to 1.2.4; sketches "
             "A and B on pollution domes are for QUESTIONS 1.2.5 to 1.2.7.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Mid-latitude cyclones", "marks": 15, "lead": "Refer to the cross-section below of a mid-latitude cyclone.",
     "figure": fig("1.3", "A cross-section of a mid-latitude cyclone with a long arrow along the ground from W to E labelled DIRECTION OF MOVEMENT. "
                   "On the left, front A curves up steeply: warm air is pushed up sharply along it into a tall cumulonimbus cloud with heavy rain; "
                   "12 °C at the ground near it. On the right, front B rises at a gentle slope with low, layered clouds and light rain; 8 °C at the "
                   "ground beneath it."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Tropical cyclones", "marks": 15, "lead": "Refer to the infographic below based on Tropical Cyclone Filipo.",
     "figure": fig("1.4", "An infographic, TROPICAL CYCLONE FILIPO. Text: the tropical storm made landfall in Mozambique on 12 March after "
                   "strengthening off the coast of south-east Africa, bringing strong winds and heavy rain to Mozambique. On 13 March it moved back "
                   "over the ocean and developed into a tropical cyclone on 14 March. A map shows its path: from the ocean east of Mozambique on "
                   "10 March, onto the Mozambique coast on 11 and 12 March, south past Maputo on 13 March and back out over the Indian Ocean on "
                   "14 March. A table gives the wind: 10 Mar 12:00 UTC 63 km/h; 11 Mar 12:00 UTC 95 km/h; 11 Mar 18:00 UTC 116 km/h; 12 Mar 06:00 "
                   "UTC 95 km/h; 12 Mar 18:00 UTC 74 km/h; 13 Mar 06:00 UTC 84 km/h; 13 Mar 18:00 UTC 106 km/h; 14 Mar 06:00 UTC 127 km/h. A small "
                   "synoptic sketch labelled MATURE STAGE shows closed isobars (980, 984 hPa) round the centre."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Line thunderstorms", "marks": 15, "lead": "Refer to the source below based on line thunderstorms.",
     "figure": fig("1.5", "LINE THUNDERSTORMS OVER SOUTH AFRICA. Text: during summer, thunderstorms can form a line that can extend for hundreds "
                   "of kilometres; they can persist for many hours and produce damaging winds and hail, which impacts negatively on the natural "
                   "environment. A map of South Africa: a high (H) in the Atlantic Ocean to the south-west sends arrow A north-eastwards into the "
                   "west of the country; a high (H) in the Indian Ocean to the south-east sends arrow B round and into the interior from the "
                   "north-east. A moisture front (a shaded band) runs north to south across the western interior, with cumulonimbus clouds just "
                   "east of it. A diagram beside it describes the rainfall from the moisture front: heavy rain closest to it, then moderate rain, "
                   "then light rain furthest away."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Drainage basins", "marks": 7,
     "lead": "Match the statements in COLUMN A with the options in COLUMN B on drainage basins.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Fluvial processes and landforms", "marks": 8,
     "lead": "Various options are provided as possible answers to the following questions on fluvial processes and landforms/features.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Drainage patterns", "marks": 15, "lead": "Refer to drainage patterns A and B below.",
     "figure": fig("2.3", "Two drainage patterns. A: streams flow outwards in all directions from a central high area; on the lower left two "
                   "streams leaving the centre join, and X marks the stream just below that junction. B: long parallel streams run up and down "
                   "the page, with short tributaries joining them from the sides."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "River rejuvenation", "marks": 15, "lead": "Refer to the sketch below on river rejuvenation.",
     "figure": fig("2.4", "A block sketch of a river valley: a wide old valley floor forms flat steps labelled River terraces on both sides; a "
                   "narrow new channel is cut into the floor of the old valley. A marks a sudden break (step) in the river's course; B marks the "
                   "steep sides of the new channel cut into the old valley floor."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Catchment and river management", "marks": 15,
     "lead": "Refer to the extract below on catchment and river management.",
     "extract": "MANAGEMENT OF CATCHMENT AREAS AND RIVER NETWORKS (SYSTEMS)\n\nRiver catchments are under severe pressure in some parts of South "
                "Africa. The plentiful water they provide has meant that the fertile ground surrounding them is an ideal place for agricultural "
                "activities. They are areas of natural beauty and often support both plant and animal species.\n\nUnfortunately, humans have not "
                "always recognised the importance of river catchments. When toxins and heavy metals leach into the catchment areas, they can "
                "endanger the lives of the flora and fauna. Agricultural run-off can carry chemicals into river catchments, creating an imbalance "
                "in nutrient levels and impacts on different species in different ways.\n\nFortunately, we are now beginning to pay attention to "
                "the conservation of these vital natural resources.", "items": q25},
]
sec_b = [
    {"id": "3.2.1", "title": "Question 3.2.1", "kind": "Urban climate", "marks": 3,
     "lead": "F is in the centre of Ladysmith and G is outside the centre (blocks C2 and D4 on the topographical map).", "extract": LADYSMITH,
     "items": q3a},
    {"id": "3.3", "title": "Question 3.3", "kind": "Geographical information systems (GIS)", "marks": 6,
     "lead": "The parts of Question 3.3 that do not read the topographical or orthophoto map.", "items": q3b},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Geography", "title": "Geography P1", "sitting": "November 2024", "total_marks": 129, "time": "3 hours"},
    "sections": [{"title": "Section A: Climate and weather and geomorphology", "total": 120, "missions": sec_a},
                 {"title": "Section B: Geographical skills and techniques", "total": 9, "missions": sec_b}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "Section A whole and the map-free parts of Section B, hand-transcribed from the paper and "
                                                           "memo PDFs and their page images; no API call."},
        {"n": "3", "kind": "no_fit", "detail": "Section B reads the 1:50 000 topographical map 2829DB LADYSMITH and the 1:10 000 orthophoto map "
                                               "2829 DB 6 LADYSMITH, handed out in the exam room: not in the question paper and not published. Its "
                                               "21 marks that read them (3.1.1-3.1.6, 3.2.2-3.2.7, 3.3.3) wait for the maps; the paper totals the "
                                               "129 marks that can be played (the printed paper: 150)."},
        {"n": "3.3.1", "kind": "low_confidence", "detail": "The printed question reads the orthophoto map's photograph; played as the fact that a "
                                                           "1:10 000 orthophoto is made from a high-resolution photograph."},
        {"n": "2.1.6", "kind": "no_fit", "detail": "The options of 2.1.6 and 2.1.7 are small sketches (Y and Z): played as Y/Z with the sketches as "
                                                   "the item's figure."},
        {"n": "1.4.4", "kind": "no_fit", "detail": "The tropical cyclone cross-section is drawn on paper and self-checked against the memo's criteria."},
        {"n": "1.5.2", "kind": "no_fit", "detail": "Each wind's temperature and moisture are separate one-mark points (the memo's part marks: cold "
                                                   "(1) or dry (1)); the marker cannot tell which wind a word was written for."},
        {"n": "paper", "kind": "memo_issue", "detail": "The memo's pages 1-3 are the notes to markers and a marked sample from another paper (its "
                                                       "answers, e.g. 1.3.1 'Katabatic', match nothing here): ignored."},
    ],
}
out = Path(__file__).parent / "out" / "geo-p1-2024-11"
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
