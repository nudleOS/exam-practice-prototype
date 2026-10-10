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
Figure boxes are measured in PDF points (page 595.32 x 841.92), found with scratchpad figs24.py and checked on rendered crops.

Learner rollout (Murci 2026-10-10): every written answer plays as STATEMENTS (`stmt`: pick the memo's points among clearly false
ones, `each` = the memo's marks per tick) or, where the memo weighs two sides (1.5.3: close to / further from the moisture front),
as a SORT (`sort_`: 1 mark a statement). The memo points in the `rub()` calls stay as the source; the bottom block swaps them.
The paper has no typed calculation that does not read the maps (3.1.4 and 3.1.5 wait for the maps), so no whole-working MCQ.
Clues and figure captions were swept so that none states a memo answer (2026-10-10)."""
import json
import random
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
     ["A high sits over the interior.", "Think about what the land surface does to the air above it in each season."]),
    ("1.1.2", "The low-pressure system in sketch B forms due to ... over the land.",
     ["low evaporation", "intense heating", "cold dense air", "heavy rainfall"], 1,
     ["Sketch B: a low over the interior.", "What does the summer sun do to the land of the interior?"]),
    ("1.1.3", "... is the concept used to describe the elongation of the isobars associated with the South Atlantic anticyclone in sketch B.",
     ["Backing", "Divergence", "Ridging", "Convergence"], 2,
     ["A high pushing a tongue of isobars outwards.", "The term describes the shape the isobars take, not how the air moves."]),
    ("1.1.4", "The anticyclones in sketch A and B change their positions seasonally because of the ...",
     ["rotation of the Earth.", "frictional drag.", "shifting of the ITCZ.", "Coriolis force."], 2,
     ["The highs move north in winter and south in summer.", "The pressure belts follow the overhead sun."]),
    ("1.1.5", "The South Indian anticyclone in sketch B is likely to feed more moisture over the east coast in comparison with sketch A because "
     "it ...", ["is a blocking high.", "has a larger fetch (distance).", "diverges dry air.", "has a smaller fetch (distance)."], 1,
     ["Compare where the South Indian high sits in sketch A and in sketch B.", "What does air pick up as it crosses the ocean?"]),
    ("1.1.6", "The low-pressure system in sketch A will move in a ... direction.", ["northerly", "westerly", "easterly", "southerly"], 2,
     ["It is a coastal low on the south coast.", "Coastal lows are pushed along by the pressure systems that follow them around the country."]),
    ("1.1.7", "Berg winds are most likely to develop in sketch A because of the presence of the ... and ...\n(i) Kalahari anticyclone\n"
     "(ii) coastal low\n(iii) South Indian anticyclone\n(iv) heat low", ["(i) and (ii)", "(ii) and (iii)", "(i) and (iv)", "(iii) and (iv)"], 0,
     ["Berg winds blow from the interior down to the coast.", "Air always flows from high pressure towards low pressure."]),
    ("1.1.8", "The inversion layer that forms over the escarpment in sketch B will favour the formation of ... and ...\n(i) frost\n(ii) rainfall\n"
     "(iii) fog\n(iv) hail", ["(i) and (ii)", "(i) and (iii)", "(ii) and (iv)", "(iii) and (iv)"], 2,
     ["Sketch B is summer, with a low over the interior.", "Which kinds of weather does the interior usually get in summer?"])]]
q12 = [mcq(n, q, ["A", "B"], a, c, figure=fig(f, cap)) for n, q, a, c, f, cap in [
    ("1.2.1", "Represents an anabatic wind", 1, ["Anabatic and katabatic winds differ in the direction the air moves along the slope.",
                                                  "Think about whether the slopes are being heated or cooled."], "1.2a", VALLEYS),
    ("1.2.2", "Cold air forces the warm air to rise which forms an inversion layer", 0,
     ["An inversion layer forms when cold air lies below warmer air.", "Think about which wind brings air down into the valley."], "1.2a", VALLEYS),
    ("1.2.3", "Occurs during the day due to insolation", 1, ["Insolation is incoming solar radiation.", "What does heated air do along a slope?"],
     "1.2a", VALLEYS),
    ("1.2.4", "Frost forms on the valley floor when the temperature drops below 0 °C", 0,
     ["Frost forms on clear, calm nights.", "Think about which wind drains air onto the valley floor at night."], "1.2a", VALLEYS),
    ("1.2.5", "Represents a pollution dome at night", 1, ["Think about how the air near the ground behaves on a cold night.",
                                                         "Compare the height of the two domes."], "1.2b", DOMES),
    ("1.2.6", "Pollutants are dispersed", 0, ["Dispersed means spread out over a larger area.", "Look at the direction of the arrows in each sketch."],
     "1.2b", DOMES),
    ("1.2.7", "Denser concentration of pollutants over the urban area", 1, ["Denser means the same pollution packed into less space.",
                                                                           "Compare how much room each dome gives the pollution."], "1.2b", DOMES)]]
q13 = [
    term("1.3.1", "In which general direction do mid-latitude cyclones move?", ["West to east", "From west to east", "Eastwards", "Eastward", "East"],
         ["Mid-latitude cyclones are carried along by the prevailing winds of the mid-latitudes.",
          "Use the compass letters on the sketch to describe the direction."]),
    rub("1.3.2", "Give a reason for your answer to QUESTION 1.3.1.", 2, ["Driven by the westerlies (2).", "Occurs in the westerly wind belt (2)."],
        ["Which planetary wind belt lies over the mid-latitudes (30° to 60°)?", "Wind belts are named after the direction they blow from."], each=2),
    rub("1.3.3", "How does front A give rise to the formation of cumulonimbus clouds?", 4, [
        "Cold front will undercut the warm air (ahead of it) (2).", "The steeper gradient will cause rapid uplift of the warm air (2).",
        "Cooling and condensation occurs (2)."],
        ["Front A is the steep front: which air mass is advancing behind it?",
         "Think about what denser air does to lighter air, and what happens to air as it rises."], each=2),
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
        ["Tropical cyclones need a lot of energy from the sea.", "Think about the sea, the air above it and the Earth's rotation."]),
    lst("1.4.2", "Give evidence from the map and table of information that Tropical Cyclone Filipo had strengthened from 10 to 11 March.", 2,
        [["Exposed to more moisture over the ocean", "Over the ocean", "Moved over the ocean", "More moisture"],
         ["Wind speed increased from 63 km/h to 95 km/h/116 km/h", "Wind speed increased", "Increase in wind speed", "63 km/h to 95 km/h",
          "63 km/h to 116 km/h", "95 km/h", "116 km/h"]],
        ["Find 10 and 11 March on the map.", "Find the same dates in the table."]),
    rub("1.4.3", "Give TWO reasons for the decrease in wind speed from 06:00 to 18:00 on 12 March.", 4, [
        "Moved over the land OR less moisture (2).", "More friction (2).", "Less latent heat (2).", "(Starting to) dissipate/weaken (2)."],
        ["Where was the cyclone between 06:00 and 18:00 on 12 March?",
         "What does a tropical cyclone need from the ocean, and what does a land surface do to moving air?"], each=2),
    draw("1.4.4", "On 14 March, Tropical Cyclone Filipo reached the mature stage. In the ANSWER BOOK, draw a labelled cross-section of Tropical "
         "Cyclone Filipo in its mature stage. Marks will be awarded for the following:\n(a) Cross-section\n(b) Cloud type\n(c) Eye\n"
         "(d) Air movement in the eye", 4, [
        ["Cross-section: towering clouds on both sides of a clear centre", 1], ["Cloud type: cumulonimbus (Cb)", 1],
        ["Eye: labelled at the centre", 1], ["Air movement in the eye: arrows pointing down (sinking air)", 1]],
        ["A mature tropical cyclone is a ring of storms around a calm centre.", "Think about the air movement that keeps the eye clear of cloud."]),
    rub("1.4.5", "Account for the lack of rainfall and clouds in the eye of the tropical cyclone.", 4, [
        "Air subsides (2).", "The air heats up (2). ACCEPT: the air is heated/warmed.", "Moisture gets evaporated/air is dry (2).",
        "No condensation takes place (2)."],
        ["Think about the direction the air moves in the eye.", "What must happen to air for clouds to form, and does that happen here?"], each=2)]
q15 = [
    term("1.5.1", "According to the extract, in which season do line thunderstorms commonly occur?", ["Summer"],
         ["The extract names the time of year.", "Think about which season brings thunderstorms to South Africa's interior."]),
    rub("1.5.2", "Describe the temperature and moisture content of wind A and wind B that led to the formation of the line thunderstorm.", 4, [
        "(Wind A:) cold/colder (1).", "(Wind A:) dry/dryness (1).", "(Wind B:) warm/warmer (1).", "(Wind B:) moist/humid/wet (1)."],
        ["Find where each wind starts: which high-pressure cell and which ocean?",
         "Think about the ocean current along each coast and what it does to the air above it."],
        notes=["Wind A (south-westerly) is cold and dry; wind B (north-easterly) is warm and moist. Part marks: cold (1) or dry (1) for A, warm "
               "(1) or moist (1) for B; a maximum of two marks for part answers."]),
    rub("1.5.3", "Explain why the heaviest rainfall occurs closest to the moisture front, as evident in the source.", 4, [
        "Rapid uplift of air along the moisture front (2).", "Greater/more (vertical) condensation (2).", "(Dense line of) cumulonimbus clouds form (2).",
        "OR — Less uplift of air further from the moisture front (2).", "Less (vertical) condensation (2).", "Less clouds form (2)."],
        ["Where do the two air masses meet, and what does the air do there?",
         "Link the amount of rising air to the amount of condensation and cloud."], each=2,
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
        ["Both terms describe land around a river, but they are not used in exactly the same way.",
         "Which term would you use for the whole network: a river together with all its tributaries?"]),
    mcq("2.1.2", "Promotes a rapid rise in the water table", ["gentle gradient", "steep gradient"], 0,
        ["The water table rises when water infiltrates the ground.", "Think about how fast water runs off each kind of slope."]),
    mcq("2.1.3", "The upper level of ground water", ["water table", "through flow"], 0,
        ["Ground water fills the soil and rock below a certain level.", "The top of the saturated zone."]),
    mcq("2.1.4", "Seepage of water into the ground", ["infiltration", "run-off"], 0,
        ["Think about where the water goes: over the surface or into the soil.", "Seepage is a slow movement of water through tiny spaces."]),
    mcq("2.1.5", "Causes reduction of surface run-off", ["impermeable rocks", "dense vegetation"], 1,
        ["Run-off is the water that flows over the surface instead of soaking in.", "Think about what each option does to rain that falls on it."]),
    mcq("2.1.6", "The confluence is located at Y/Z", ["Y", "Z"], 1,
        ["Look closely at where each circle sits on the streams.", "Think about where a tributary ends."], figure=fig("2.1.6", CONFLUENCE)),
    # (the paper's KEY sits in COLUMN A, outside the crop of the Y/Z sketches: it goes in the stem)
    mcq("2.1.7", "High-lying area separating two tributaries in the same river system\n(KEY: the hatched line is a high-lying area; the lines "
        "with arrows are streams.)", ["Y", "Z"], 1,
        ["Read the KEY, then follow each stream to see where it ends up.", "Think about the difference between a watershed and an interfluve."],
        figure=fig("2.1.7", DIVIDES))]
q22 = [
    mcq("2.2.1", "... is responsible for the shape of the river valley below.", ["Deposition", "Lateral erosion", "Weathering", "Vertical erosion"], 3,
        ["The valley is a narrow V.", "Which way does a river in its upper course mostly erode?"],
        figure=fig("2.2.1", "A block sketch of a narrow, steep-sided V-shaped valley with a small stream at the bottom.")),
    mcq("2.2.2", "A ... forms at the base of a waterfall.", ["braided stream", "delta", "gorge", "plunge pool"], 3,
        ["Think about what the falling water does at the foot of the drop.", "Rock fragments are swirled around by the water there."]),
    mcq("2.2.3", "The fluvial landform/feature depicted in the sketch is a ...", ["waterfall.", "valley.", "rapid.", "cliff."], 2,
        ["Look at the size of each drop in the river bed.", "How is this feature different from a waterfall?"],
        figure=fig("2.2.3", "A sketch of a river bed: arrows show the water flowing over a bed of rock labelled Soft Rocks and Outcrops of rock.")),
    mcq("2.2.4", "The flat, low-lying area along the banks of a river in the lower course is a/an ...",
        ["meander.", "delta.", "flood plain.", "alluvial fan."], 2,
        ["Fine sediment is laid down here each time the river overflows its banks.", "It lies on both sides of a meandering river."]),
    mcq("2.2.5", "The slope at X on the inner bank of a meander is also referred to as a/an ... slope.", ["steep", "undercut", "concave", "slip-off"], 3,
        ["The inner bank is where the river deposits.", "On the inner bank the water is slow, so the bank is gentle, not cut away."],
        figure=fig("2.2.5", "A sketch of a winding river; an arrow labelled X points to the inside of one bend.")),
    mcq("2.2.6", "A/An ... forms when the meander loop is cut off from the main stream.", ["delta", "rapid", "ox-bow lake", "flood plain"], 2,
        ["Think about what happens to a meander loop as the outer banks erode closer together.",
         "What is left behind when the river cuts through the narrow neck?"]),
    mcq("2.2.7", "The benefit of natural levees is ... on the flood plain.",
        ["increased deposition", "reduced flooding", "reduced fertility", "increased flooding"], 1,
        ["Levees are raised banks along the river.", "Think about what happens when the river rises during heavy rain."],
        figure=fig("2.2.7", "A cross-section of a river channel on a flood plain with raised ridges labelled Natural levees along both banks.")),
    mcq("2.2.8", "Deltas form at the river mouth when the following conditions occur:\n(i) Shallow sea bed\n(ii) Steep sea bed\n"
        "(iii) Strong currents\n(iv) Small tidal range", ["(i) and (ii)", "(ii) and (iii)", "(iii) and (iv)", "(i) and (iv)"], 3,
        ["A delta is sediment that the sea does not wash away.", "Think about the depth of the water and the strength of the tides at the river mouth."])]
q23 = [
    term("2.3.1", "Identify drainage pattern A.", ["Radial", "Centrifugal", "Radial drainage pattern"],
         ["Look at the way the streams leave the centre.", "The pattern is named after the shape the streams make together."]),
    term("2.3.2", "Determine the stream order of X in drainage pattern A.", ["2nd", "Second", "2", "Second order", "2nd order"],
         ["A stream with no tributaries is a first-order stream.", "Follow X upstream: how many streams meet above it, and what order are they?"],
         marks=2),
    rub("2.3.3", "Give a reason for the direction in which streams flow in drainage pattern A.", 2, [
        "Radiates outwards/away from a high-lying central point/centre (accept examples of landforms) (2)."],
        ["Look at where all the streams begin.", "What must the land be like there for water to flow away from it in every direction?"], each=2),
    rub("2.3.4", "How does the joining of the tributaries to the mainstream differ in drainage patterns A and B?", 2, [
        "The tributaries join the main river at acute angles at A and at right angles at B (2)."],
        ["Look at the angle where each tributary meets its main stream.", "Use the correct names for the angles you see."], each=2),
    rub("2.3.5", "State TWO conditions associated with the underlying rock that contributed to the formation of trellis drainage pattern B.", 4, [
        "Alternate layers of hard/resistant and soft rock (varying resistance) (2).", "Folded rocks (2)."],
        ["Think about the rock structure under the long, parallel valleys of B.",
         "Think about how resistant each rock layer is, and what earth forces have done to the layers."], each=2),
    rub("2.3.6", "Why are human activities limited in areas where drainage patterns A and B are found?", 4, [
        "Land is steep/uneven (2).", "Prone to soil erosion/thin soils (2).", "Infertile soils (2).", "Risk of mass movements (2).",
        "High cost of developing land (2)."],
        ["Picture the landscape each pattern forms on.", "What makes it hard to farm or build there?"], each=2)]
q24 = [
    rub("2.4.1", "Define the term river rejuvenation.", 2, [
        "When the river experiences an increase in energy (erodes vertically) (2). ACCEPT: the river gains (more) energy and erodes "
        "vertically/downwards."],
        ["Rejuvenate means to make young again.", "Think about what a young river in its upper course is like."], each=2,
        notes=["Concept: an increase in the river's energy, so it erodes vertically."]),
    term("2.4.2", "Identify the feature at A.", ["Knickpoint", "Knick point", "Waterfall"],
         ["Look at what happens to the river's course at A.", "This feature moves upstream over time as the river erodes it."]),
    rub("2.4.3", "How does feature A indicate that river rejuvenation has taken place?", 2, [
        "Change/drop in gradient (2).", "(Evidence of) vertical erosion (2).", "Water flowing/flows faster (2).",
        "(Evidence of) old and new river profiles (2)."],
        ["Look at the river's long profile at A.", "What does rejuvenation do to the river's energy and to the shape of its course?"], each=2),
    rub("2.4.4", "Describe the change that river rejuvenation has made to the landscape at B.", 2, [
        "It formed a valley in a valley (2).", "The river channel got deeper/steeper/wider (2)."],
        ["Compare the shape at B with the wider, older valley around it.", "Think about which way a rejuvenated river erodes."], each=2),
    rub("2.4.5", "How do river terraces form?", 4, [
        "Vertical erosion occurs on the flood plain (2).", "A new (river) valley is formed/forms/created (2).",
        "(This creates) a step-like feature/landform (known as a terrace) (2).", "The old flood plain/floodplain is now the river terrace (2)."],
        ["Start with a river on its flood plain that suddenly gains energy.", "What is left on either side once the river is far below its old level?"],
        each=2),
    rub("2.4.6", "Why are some river terraces not suitable for farming?", 4, [
        "Far/distant from water sources (2).", "Difficult/expensive to build infrastructure (accept examples) (2).",
        "River terraces can be very narrow (2).", "Limit use of machinery (2).", "(Decrease in) soil fertility/infertile/thin soils (2).",
        "Uneven slopes/rugged landscape (2).", "Unstable soil OR mass movement (accept examples) (2)."],
        ["Look at where the terraces lie in the sketch.", "Think about what a farmer needs: water, space, good soil and gentle land."], each=2)]
q25 = [
    rub("2.5.1", "What is river management?", 2, [
        "Monitoring and controlling (management) of water resources in a drainage basin/catchment area (2)."],
        ["Management means looking after something.", "Think about what must be done so that a basin's water stays enough and clean for everyone."],
        each=2, notes=["Concept: the monitoring and controlling of water resources in a drainage basin."]),
    term("2.5.2", "Name ONE human activity in the extract that has a negative impact on South Africa's catchment areas.",
         ["Agriculture", "Agricultural activities", "Agricultural run-off", "Farming"],
         ["The extract names an activity that sends chemicals into rivers.", "Think about how the fertile ground around river catchments is used."]),
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
        ["Think about what a government controls that ordinary people cannot.",
         "Sustainable means the strategy keeps working for future generations."], each=2)]

# ---- QUESTION 3 (SECTION B): only the parts that do not read the maps, the question paper pages 15-17 and the memo pages 11-12 ----
LADYSMITH = ("GENERAL INFORMATION ON LADYSMITH\n\nCoordinates: 28°33'S; 29°46'E\n\nLadysmith is a city in the Uthukela District of KwaZulu-Natal. "
             "It is situated along the Klip River. The climate is warm and temperate with the highest rainfall recorded in summer. The average "
             "annual temperature is 17,3 °C. The average annual precipitation is approximately 1 057 mm. This climate provides ideal conditions "
             "for agricultural raw materials.")
q3a = [
    term("3.2.1(a)", "The temperature at F, in the centre of the town, is 2 °C higher than at G, outside the centre. Name the concept that "
         "describes this difference.", ["Urban heat island", "Urban heat island effect", "Heat island"],
         ["Towns are warmer than the countryside around them.", "On an isotherm map the warm town stands out from the cooler land all around it."]),
    rub("3.2.1(b)", "Give ONE reason why the high density of buildings at F generally contributes to the higher temperatures.", 2, [
        "Heat will get trapped (2).", "Reduced wind speed (2).", "Reduced air flow (2).", "Artificial surfaces (2).", "Multiple reflections (2)."],
        ["Think about what tall buildings close together do to moving air.", "Think about what the buildings and roads are made of."], each=2)]
q3b = [
    mcq("3.3.1", "The vertical aerial photograph used to make the 1:10 000 orthophoto map has a (high/low) resolution.", ["High", "Low"], 0,
        ["Resolution is how much detail an image shows.", "Compare the scale of the orthophoto map with that of the topographical map."]),
    mcq("3.3.2", "The reference (key) of the topographical map represents (spatial/attribute) data.", ["Spatial", "Attribute"], 1,
        ["One kind of data gives a position; the other describes characteristics.", "Think about what the reference (key) tells you about a symbol."]),
    rub("3.3.4", "Define the term buffering.", 2, ["The demarcation of an area around/along a geographical feature/location (2)."],
        ["Think of a buffer as something that protects.", "Picture a GIS map with a zone marked out next to a river or a road."], each=2,
        notes=["Concept: a zone demarcated around a feature."]),
    rub("3.3.5", "How would buffering beside the Klip River protect the quality of the water in the river?", 2, [
        "Restrict development on the banks of the river (2).", "Decrease pollution from the built-up area (2).",
        "Reduces eroded soil from entering the river (2).", "Decreased eutrophication (2).", "Reduces salinity (2).",
        "The natural course/capacity of the river will be maintained (2).", "Biodiversity of the river will be preserved (2)."],
        ["What happens on the land right next to a river that can harm its water?", "What would no longer reach the water?"], each=2)]

sec_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Anticyclones", "marks": 8,
     "lead": "Refer to sketches A and B below. Various options are provided as possible answers to the following questions based on the "
             "influence of anticyclones in South Africa.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Valley climates and pollution domes", "marks": 7,
     "lead": "Match the descriptions below with sketches A and B. Sketches A and B on valley climates are for QUESTIONS 1.2.1 to 1.2.4; sketches "
             "A and B on pollution domes are for QUESTIONS 1.2.5 to 1.2.7.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Mid-latitude cyclones", "marks": 15, "lead": "Refer to the cross-section below of a mid-latitude cyclone.",
     "figure": fig("1.3", "A cross-section of a mid-latitude cyclone with a long arrow along the ground from W to E labelled DIRECTION OF MOVEMENT. "
                   "On the left, front A is a steep curved line with arrows rising beside it into a tall cloud with rain falling from it; 12 °C "
                   "at the ground near it. On the right, front B is a gently sloping straight line with arrows rising beside it into smaller "
                   "clouds with a little rain; 8 °C at the ground beneath it."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Tropical cyclones", "marks": 15, "lead": "Refer to the infographic below based on Tropical Cyclone Filipo.",
     "figure": fig("1.4", "An infographic, TROPICAL CYCLONE FILIPO. Text: the tropical storm made landfall in Mozambique on 12 March after "
                   "strengthening off the coast of south-east Africa, bringing strong winds and heavy rain to Mozambique. On 13 March it moved back "
                   "over the ocean and developed into a tropical cyclone on 14 March. A map shows its path: over the ocean east of Mozambique "
                   "on 10 March and at 12:00 on 11 March, at the coast at 18:00 on 11 March, over land on 12 March, near Maputo at 06:00 on "
                   "13 March, back over the Indian Ocean at 18:00 on 13 March and further out to sea on 14 March. A table gives the wind: 10 Mar 12:00 UTC 63 km/h; 11 Mar 12:00 UTC 95 km/h; 11 Mar 18:00 UTC 116 km/h; 12 Mar 06:00 "
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
    {"id": "2.1", "title": "Question 2.1", "kind": "River systems", "marks": 7,   # (not "Drainage basins": that is 2.1.1's answer)
     "lead": "Match the statements in COLUMN A with the options in COLUMN B.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Fluvial processes and landforms", "marks": 8,
     "lead": "Various options are provided as possible answers to the following questions on fluvial processes and landforms/features.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Drainage patterns", "marks": 15, "lead": "Refer to drainage patterns A and B below.",
     "figure": fig("2.3", "Two drainage patterns. A: arrowed streams start at an irregular shape in the middle and run out towards the edges "
                   "of the box; on the lower left two of these streams join, and X marks the stream just below that junction. B: long parallel "
                   "streams run up and down the page, with short tributaries joining them from the sides."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "River rejuvenation", "marks": 15, "lead": "Refer to the sketch below on river rejuvenation.",
     "figure": fig("2.4", "A block sketch of a river valley. Flat strips on both sides of the valley are labelled River terraces. A dark river "
                   "runs along the bottom of a narrow channel in the middle; A points to a spot on the river, and B points to the hatched slopes "
                   "on either side of the river."), "items": q24},
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


# ---- Written answers as STATEMENTS (Murci 2026-10-10; helpers as in transcribe_bs_p2_2025_11.py) ----
# A written part plays as picking statements: the memo's own points (right, tidied to one reading of its "/" alternatives) and
# CLEARLY wrong ones (the opposite, or a confusion with another concept; never a true point the memo leaves out, which its
# "any other relevant answer" would make right). The learner picks marks/each of them, any right one counts (the memo's "any N"),
# each right pick earns `each` (the memo's ticks: 2 a point here, 1 in 1.5.2). The cards are shuffled the same way every run.
def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("geo-p1-2024-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    "1.3.2": (2, ["Mid-latitude cyclones are driven by the westerlies.", "Mid-latitude cyclones occur in the westerly wind belt."],
                 ["Mid-latitude cyclones are driven by the tropical easterlies.", "Mid-latitude cyclones occur in the polar easterly wind belt.",
                  "Mid-latitude cyclones are driven by land breezes blowing off the coast."]),
    "1.3.3": (2, ["The cold front undercuts the warm air ahead of it.", "The steeper gradient causes rapid uplift of the warm air.",
                  "Cooling and condensation occur."],
                 ["The warm air undercuts the cold air ahead of it.", "The gentle gradient causes slow uplift of the warm air.",
                  "The rising air warms up and evaporation occurs."]),
    "1.3.4": (2, ["Maintain natural vegetation.", "Build retaining walls.", "Create effective drainage systems.", "Construct artificial levees.",
                  "Conserve wetlands."],
                 ["Clear the natural vegetation from steep slopes.", "Build houses on the flood plains close to rivers.",
                  "Plough up and down the slopes."]),
    "1.4.3": (2, ["It moved over the land, where there is less moisture.", "There was more friction.", "There was less latent heat.",
                  "It was starting to dissipate."],
                 ["It moved back over the warm ocean.", "There was less friction.", "More latent heat was released."]),
    "1.4.5": (2, ["The air subsides.", "The air heats up.", "Moisture gets evaporated, so the air is dry.", "No condensation takes place."],
                 ["The air rises rapidly.", "The air cools as it rises.", "Condensation forms cumulonimbus clouds."]),
    "1.5.2": (1, ["Wind A is cold.", "Wind A is dry.", "Wind B is warm.", "Wind B is moist."],
                 ["Wind A is warm.", "Wind A is moist.", "Wind B is cold.", "Wind B is dry."]),
    "1.5.4": (2, ["Natural habitats will be destroyed.", "Biodiversity will be reduced.", "Top soil will be washed away.",
                  "Wildlife would be displaced.", "Natural vegetation can be uprooted."],
                 ["Biodiversity will increase.", "Soil erosion will be reduced.", "Water quality will improve."]),
    "2.3.3": (2, ["The streams flow outwards from a high-lying central point.", "The streams flow outwards from a central dome or volcano."],
                 ["The streams flow inwards towards a low-lying central basin.", "The streams flow parallel to each other down a uniform slope.",
                  "The streams follow lines of weakness such as joints and faults."]),
    "2.3.4": (2, ["The tributaries join the main river at acute angles at A and at right angles at B."],
                 ["The tributaries join the main river at right angles at A and at acute angles at B.",
                  "The tributaries join the main river at the same angle in A and in B.",
                  "The tributaries never join a main river in B.",
                  "The tributaries join the main river at obtuse angles, pointing upstream, at A and at B."]),
    "2.3.5": (2, ["Alternate layers of hard and soft rock.", "Folded rocks."],
                 ["Rock layers that are all equally resistant.", "Flat, horizontal rock layers that were never folded.",
                  "A single dome of uniform rock."]),
    "2.3.6": (2, ["The land is steep and uneven.", "The area is prone to soil erosion.", "The soils are infertile.", "There is a risk of mass movements."],
                 ["The land is flat and easy to build on.", "The soils are deep and very fertile.", "There is no water, because no streams flow there."]),
    "2.4.1": (2, ["When the river experiences an increase in energy and erodes vertically."],
                 ["When the river loses energy and deposits its load.", "When a river captures the headwaters of a neighbouring river.",
                  "When the river reaches its base level and stops eroding.",
                  "When the river widens its valley by lateral erosion in its lower course."]),
    "2.4.3": (2, ["There is a change in gradient.", "There is evidence of vertical erosion.", "The water flows faster."],
                 ["The gradient stays the same along the whole river.", "There is evidence of deposition only.", "The water flows slower."]),
    "2.4.4": (2, ["It formed a valley in a valley.", "The river channel got deeper."],
                 ["It formed a wide, flat flood plain.", "The river channel got shallower.", "It formed an ox-bow lake."]),
    "2.4.5": (2, ["Vertical erosion occurs on the flood plain.", "A new river valley is formed.",
                  "This creates a step-like feature (known as a terrace).", "The old flood plain is now the river terrace."],
                 ["Deposition builds the river bed up above the old flood plain.", "Terraces form when sea level rises and the river loses energy.",
                  "Farmers cut the terraces into the valley slopes."]),
    "2.4.6": (2, ["They are far from water sources.", "It is difficult and expensive to build infrastructure.", "River terraces can be very narrow.",
                  "They limit the use of machinery."],
                 ["River terraces lie below the level of the river.", "River terraces are too flat for crops to grow.",
                  "The soils on river terraces are too fertile for crops."]),
    "2.5.1": (2, ["Monitoring and controlling of water resources in a drainage basin."],
                 ["The area drained by a river and its tributaries.", "The total length of streams per square kilometre of a drainage basin.",
                  "The movement of water from the surface into the soil.", "Building as many dams as possible to store all of a river's water."]),
    "2.5.3": (2, ["It causes eutrophication.", "It creates an imbalance in the nutrient levels in the river.", "It reduces biodiversity.",
                  "It causes water pollution."],
                 ["Fertilisers increase the oxygen levels in the river.", "It increases the number of plant and animal species in the river.",
                  "Agricultural run-off purifies the river water."]),
    "2.5.4": (2, ["Run educational programmes.", "Implement legislation and conservation zones.", "Create buffer zones.", "Remove alien vegetation.",
                  "Conserve wetlands."],
                 ["Allow factories to dump waste into rivers.", "Drain wetlands to make room for farms.", "Plant alien trees along river banks."]),
    "3.2.1(b)": (2, ["Heat will get trapped.", "Wind speed is reduced.", "There are many artificial surfaces."],
                    ["Buildings reflect all incoming heat straight back into space.", "Buildings absorb less heat than natural surfaces.",
                     "Heat escapes easily from between the buildings."]),
    "3.3.4": (2, ["The demarcation of an area around a geographical feature."],
                 ["Combining two or more map layers into one map.", "Making a map simpler by leaving out less important detail.",
                  "Collecting information about the Earth from a distance.", "Converting a paper map into digital data."]),
    "3.3.5": (2, ["Restrict development on the banks of the river.", "Decrease pollution from the built-up area.",
                  "Reduce the eroded soil that enters the river."],
                 ["Increase pollution from the built-up area.", "Allow more eroded soil to enter the river.",
                  "Encourage building right up to the river banks."]),
}
# A written part whose memo weighs two sides plays as a SORT instead (variety, Murci 2026-10-10): each statement dragged to its side,
# or to "Not true" (the clearly wrong one), 1 mark a statement; a grouped match, played as a classification. 1.5.3's memo explains
# from either side of the moisture front ("close to ... OR further from ...").
SORTS = {
    "1.5.3": (["Closest to the moisture front", "Further from the moisture front", "Not true"], [
        ("Rapid uplift of air takes place.", 0),
        ("A dense line of cumulonimbus clouds forms.", 0),
        ("Less vertical condensation takes place.", 1),
        ("Rain clouds form by evaporation, not by condensation.", 2)]),
}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("geo-p1-2024-11:sort:" + n).shuffle(order)
    rows = [rows[i] for i in order]
    assert marks == len(rows) and len(set(b for _, b in rows)) == len(bins), n
    return {"t": "match", "n": n, "marks": marks, "q": q + " Sort each statement.", "clues": clues, "left": [r for r, _ in rows],
            "right": bins, "a": [b for _, b in rows], "heads": ["STATEMENTS", "SORT INTO"], "groups": True}


for _m in sec_a + sec_b:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric" and _it["n"] in SORTS:
            _bins, _rows = SORTS[_it["n"]]
            _m["items"][_k] = sort_(_it["n"], _it["q"], _it["marks"], _bins, _rows, _it["clues"])
        elif _it["t"] == "rubric" and _it["n"] in STATEMENTS:
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            assert _it.get("each", 1) == _each, (_it["n"], "each differs from the memo's ticks")
            _m["items"][_k] = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
assert not [i["n"] for m in sec_a + sec_b for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"
assert set(STATEMENTS) | set(SORTS) <= {i["n"] for m in sec_a + sec_b for i in m["items"]}, "a statement key names no part"

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
        {"n": "1.5.2", "kind": "no_fit", "detail": "Each wind's temperature and moisture are separate one-mark statements (the memo's part marks: "
                                                   "cold (1) or dry (1)), each beside its opposite (Wind A is warm, ...): pick the four true ones."},
        {"n": "1.5.3", "kind": "no_fit", "detail": "The memo explains from either side of the moisture front (close to OR further from): played as a "
                                                   "sort of its points into the two sides, with one false statement, 1 mark a statement."},
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
