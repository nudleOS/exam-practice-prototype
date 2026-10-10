"""Geography P1 Nov 2025: SECTION A whole (Questions 1 and 2, 120 marks) and the parts of SECTION B (Question 3) that do not read
the maps (8 marks), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the memo's points are the paper's and the
memo's own; clues and figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_geo_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Geography P1 Nov 2025 Eng.pdf" "<...>/Geography P1 Nov 2025 MG Eng.pdf" --id geo-p1-2025-11 --from-json

SECTION B reads a 1:50 000 topographical map (3318DD STELLENBOSCH) and a 1:10 000 orthophoto map (3318 DD 18) that are handed out
in the exam room: they are not in the question paper and DBE does not publish them. Its 22 marks that read the maps (3.1.1-3.1.6,
3.2.2-3.2.8, 3.3.2) wait for the maps; the paper totals what is playable, 128.

How the memo's shapes map (Geography):
  COLUMN A / COLUMN B with Y or Z -> mcq of the two options (1 mark); A-D -> mcq; a sketch or photo printed with ONE item -> that
  item's figure, a photo for several MCQs -> each item's figure (the MCQ stage shows an item's own figure); "Name / State" one term
  -> term; "Give TWO ..." -> list (synonym groups, the lead rule); "Explain / Describe / Suggest", "(n x 2)" -> rubric, each 2,
  one memo point a bullet with its part mark folded in (so a point is never counted twice); "MUST mention X and Y" -> must (the
  compulsory point); a paragraph "(4 x 2)" -> rubric each 2; "Classify EACH as ..." -> match into groups; "Draw" -> draw, self-checked.
Figure boxes are measured in PDF points (page 595.32 x 841.92) and checked on a contact sheet (ingest pads each crop by 1% of the page).

Learner rollout (Murci 2026-10-10): every written answer plays as STATEMENTS (`stmt`: pick the memo's points among clearly false
ones, `each` = the memo's marks per tick, 2 a point throughout) or, where the memo MUST have two sides covered, as a SORT (`sort_`:
1 mark a statement): 1.3.4 (the part-mark causes sorted into gale force winds C / heavy rainfall D), 1.5.3 (why warm / why dry)
and 2.3.7 (profile C / profile D). The memo points in the `rub()` calls stay as the source; the bottom block swaps them. The
paper has no typed calculation that does not read the maps (3.1.1 and 3.1.3 wait for the maps), so no whole-working MCQ.
Clues, captions and mission kinds were swept so that none states a memo answer (2026-10-10)."""
import json
import random
from pathlib import Path

W, H = 595.32, 841.92
FIGS = {  # tools: scratchpad geo/figs_geo_p1.py + the boxes eased off the source lines; [page, x0, y0, x1, y1] in points
    "1.1.7": [3, 186, 488, 340, 567], "1.1.8": [3, 186, 637, 340, 723], "1.2a": [4, 184, 180, 401, 414], "1.2b": [5, 134, 119, 451, 305.5],
    "1.3": [6, 50, 112, 535, 468], "1.4": [7, 50, 166, 531, 580], "1.5": [8, 75.3, 204.8, 534.0, 597.9], "2.1": [9, 102, 164, 483, 407],
    "2.2": [10, 50, 146.5, 535.5, 345.5], "2.3": [12, 118, 108.6, 475, 488.5], "2.4": [13, 50, 109.5, 535.5, 425.5], "2.5": [14, 106, 259.5, 531, 488.5],
    "3.3": [18, 50, 468.4, 535.5, 646]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None, must=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {})}


term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}

SLOPE = "A photograph of a valley, SOUTH marked on the left and NORTH on the right: slope A, upper left, is open grassland; slope B, " \
        "below and to the right of it, is covered in dense trees (an arrow labels them); the far slope on the right is grassy."
VALLEY = "A photograph of a mountain valley at night (a crescent moon top right): white arrows labelled A point down both mountain " \
         "slopes towards the valley floor, where a train runs along a curving track beside a plantation."
BASIN = "A drainage basin sketch: a main river A flows from the mountains to the sea, with tributaries. B lies between two streams " \
        "in the upper basin; E (circled) on the left; F (circled) on a stream on the right; G a steep slope at the top; D beside a " \
        "stream on the right; C beside the river, with tree symbols; H below a tight bend of the river, close to the sea; I beside a " \
        "stream on the far left. KEY: tree symbol, vegetation; solid line, permanent river; dashed line, periodic river."
CAPTURE = "Two block diagrams. A, BEFORE RIVER CAPTURE: river X flows down the front slope, river Y flows the other way on the " \
          "right, its headwaters near X's. B, AFTER RIVER CAPTURE: the same block with the rivers' courses changed; part of Y is " \
          "now drawn as a dashed line."

# ---- QUESTION 1: CLIMATE AND WEATHER, the question paper pages 3-8 and the memo pages 4-7 ----
q11 = [
    mcq("1.1.1", "The name of the air pressure cell that dominates the interior of South Africa in winter", ["heat low", "Kalahari high"], 1,
        ["Winter: the interior is cold and dry.", "In winter the plateau is cold: does the air above it rise or sink?"]),
    mcq("1.1.2", "Air movement associated with high-pressure cells", ["convergence", "divergence"], 1,
        ["In a high, air sinks.", "When sinking air reaches the ground, does it gather together or move apart?"]),
    mcq("1.1.3", "The general direction of movement of a coastal low-pressure system is …", ["easterly", "westerly"], 0,
        ["Coastal lows travel along the South African coast.", "Think about where coastal lows first form and where they end up."]),
    mcq("1.1.4", "The … is known as a blocking high when it is in the path of the mid-latitude cyclone.", ["South Indian high", "Kalahari high"], 0,
        ["A blocking high stands in the way of the cyclone.", "Mid-latitude cyclones move from west to east."]),
    mcq("1.1.5", "The elongation of isobars extending outwards from a high-pressure cell is referred to as …", ["diverging", "ridging"], 1,
        ["Think of a high pushing a tongue of isobars along the coast.",
         "Is the statement about how air moves, or about the shape the isobars make?"]),
    mcq("1.1.6", "A … is found between two air masses of different moisture contents.", ["moisture front", "inter-tropical convergence zone"], 0,
        ["It separates moist air from dry air.", "Over South Africa it forms in the interior, between air from the Indian Ocean and air from the west."]),
    mcq("1.1.7", "The conditions represented in the sketch below will lead to …", ["line thunderstorms", "berg winds"], 0,
        ["The high in the east brings moist air from the Indian Ocean; the air from the west is dry.",
         "A dashed line on a synoptic map marks a moisture front."],
        figure=fig("1.1.7", "A sketch of South Africa between two highs (H) over the oceans; curved arrows bring air in from both sides, "
                   "and a dashed line runs from the north-west across the interior.")),
    mcq("1.1.8", "Rainfall with 20 knots of wind is likely at …", ["Durban (Dbn)", "Cape Town (CT)"], 1,
        ["Read the station symbols: the dot beside a station means rain; the circle's shading shows cloud cover.",
         "Each full barb on the wind arrow is 10 knots."],
        figure=fig("1.1.8", "A sketch of South Africa with a low (L) over the interior. Durban (Dbn) and Cape Town (CT) each have a "
                   "station symbol with a dot beside it and a wind arrow."))]
q12 = [
    mcq("1.2.1", "Slope aspect refers to …", ["upslope movement of air in a valley.", "climate on a smaller scale.", "a zone of warmer air in the valley.",
                                               "slope direction in relation to the sun."], 3,
        ["Aspect is a property of the slope itself, not of the air in the valley.",
         "Compare slopes A and B in the photograph: why does one have trees and the other not?"], figure=fig("1.2a", SLOPE)),
    mcq("1.2.2", "The photograph represents a valley in the … Hemisphere.", ["Northern", "Eastern", "Southern", "Western"], 2,
        ["The trees grow on the slope that gets less sun.", "Which slope faces away from the sun in each hemisphere?"], figure=fig("1.2a", SLOPE)),
    mcq("1.2.3", "Slope B represents a … and … slope.\n(i) cooler\n(ii) warmer\n(iii) moist\n(iv) drier",
        ["(i) and (ii)", "(ii) and (iii)", "(i) and (iii)", "(ii) and (iv)"], 2,
        ["Slope B is the one covered in trees.",
         "In this hemisphere, which way does slope B face? Think about what less direct sun does to temperature and evaporation."],
        figure=fig("1.2a", SLOPE)),
    mcq("1.2.4", "The arrows at A indicate a/an … wind.", ["anabatic", "katabatic", "upslope", "onshore"], 1,
        ["The arrows point DOWN the slopes, at night.", "Cold dense air sinks into the valley."], figure=fig("1.2b", VALLEY)),
    mcq("1.2.5", "The main conditions for the formation of the wind at A are … and …\n(i) terrestrial radiation\n(ii) solar radiation\n"
        "(iii) low temperatures\n(iv) high temperatures", ["(i) and (iii)", "(i) and (iv)", "(ii) and (iii)", "(ii) and (iv)"], 0,
        ["It is night: the ground loses heat.", "The air on the slopes cools and becomes dense."], figure=fig("1.2b", VALLEY)),
    mcq("1.2.6", "… forms when the dew point temperature of air is below freezing point on the valley floor.", ["Mist", "Fog", "Frost", "Smog"], 2,
        ["Below freezing, water vapour turns straight to ice.", "It coats the ground in the cold valley floor."], figure=fig("1.2b", VALLEY)),
    mcq("1.2.7", "The negative physical (natural) impact of the answer to QUESTION 1.2.6 is that it …",
        ["reduces visibility.", "increases pollution.", "increases rainfall.", "destroys vegetation."], 3,
        ["Physical: an impact on nature, not on people's activities.",
         "Think about what happens to living things on the valley floor when the water inside them freezes."], figure=fig("1.2b", VALLEY))]
q13 = [
    term("1.3.1", "What is the name of the boundary between two air masses, as shown in sketch A?", ["Polar front", "The polar front"],
         ["It lies at about 60°S.", "Mid-latitude cyclones form along this boundary."]),
    term("1.3.2", "Give ONE reason why the boundary between the two air masses in sketch A would form a wave.", [
        "Atmospheric instability", "Frictional drag", "Jet streams", "Jet stream", "Orographic features", "Mountains", "Temperature differences",
        "Temperature difference", "Windspeed differences", "Wind speed differences"],
         ["The two air masses move in opposite directions.", "Think of what disturbs a straight boundary."]),
    term("1.3.3", "Name the stage of development of the mid-latitude cyclone associated with weather conditions in photographs C and D.",
         ["Mature stage", "Mature"], ["Strong winds and flooding: the cyclone at its strongest.",
                                      "Think about the stages a mid-latitude cyclone passes through, from its start to its end."]),
    rub("1.3.4", "Explain how the weather conditions illustrated in photographs C and D developed during the stage named in QUESTION 1.3.3.", 4, [
        "A steep pressure gradient results in gale force/strong winds (2). Part mark: steep pressure gradient (1).",
        "Strong updraughts/rapid upliftment results in (cumulonimbus clouds) heavy rainfall (2). Part mark: strong updraughts/rapid upliftment (1).",
        "Air behind the cold front undercuts the warm air ahead of it, giving rise to (cumulonimbus clouds) and heavy rainfall (2). Part mark: air "
        "behind the cold front undercuts the warm air (1)."],
        ["C shows gale force winds; D shows flooding from heavy rain.",
         "For each statement ask: does it explain what makes the wind so strong, or what makes so much rain fall?"],
        each=2, must=[0]),
    draw("1.3.5", "In the ANSWER BOOK, draw a fully labelled cross-section of a cold front (E–F) in sketch B. Clearly indicate the following:\n"
         "(a) Correct cross-section\n(b) General direction of movement of the mid-latitude cyclone\n(c) Cloud type\n(d) Sector", 4, [
        ["Correct cross-section drawing: cold air undercutting the warm air along a steep front", 1],
        ["Direction of movement of the system (west to east)", 1], ["One type of cloud: cumulonimbus (Cb) / cumulus (Cu)", 1],
        ["One sector labelled (the cold sector behind the front or the warm sector ahead of it)", 1]],
        ["E–F crosses the cold front only.", "A cold front is steep: cold, dense air pushes under the warm air."]),
    rub("1.3.6", "Refer to sketch B. Explain how the difference in temperature of the air masses behind the cold front and ahead of the warm front "
        "will result in the formation of a cold front occlusion.", 4, [
        "The air behind the cold front is colder than the air in front of the warm front (2). Part mark: the air behind the cold front is colder (1).",
        "The cold air behind the cold front undercuts the warmer air in front of the warm front (2). Part mark: the cold air behind the cold front "
        "undercuts (1).",
        "The warmer (less dense) air is uplifted over the colder (denser) air (2). Part mark: the warmer (less dense) air is uplifted (1)."],
        ["Compare the air behind the cold front with the air ahead of the warm front.",
         "Which of the two air masses is denser, and what does denser air do when it meets lighter air?"],
        each=2)]
q14 = [
    term("1.4.1", "According to the fact file, in which stage of development was Tropical Cyclone Dikeledi on 8 January 2025?",
         ["Immature stage", "Immature"], ["996 hPa and 75 km/h: it is not yet at full strength.",
                                          "Compare these conditions with those recorded on 13 January."]),
    lst("1.4.2", "Give TWO reasons in the fact file to support your answer to QUESTION 1.4.1.", 2,
        [["996 hPa", "996"], ["75 km/h", "75"], ["Given a name", "Named"]],
        ["Read the conditions recorded on 8 January.", "Compare them with 13 January."]),
    rub("1.4.3", "Refer to location map B. Explain why Tropical Cyclone Dikeledi developed between 5° and 20° south of the equator.", 4, [
        "Coriolis force is present within these latitudes, resulting in deflection (2). Part mark: Coriolis force is present (1).",
        "High temperatures/warm oceans promote a high evaporation rate (2). Part mark: high temperatures/warm oceans (1).",
        "Latent heat is released during condensation (2). Part mark: latent heat (1).",
        "A high evaporation rate will lead to intense low pressure (2). Part mark: high evaporation rate (1)."],
        ["Why do tropical cyclones not form right on the equator?", "What does a tropical cyclone need from the ocean below it?"], each=2),
    rub("1.4.4", "Refer to satellite images C and D. Describe the weather conditions associated with the forward left-hand quadrant (dangerous "
        "semicircle) in satellite image D.", 4, [
        "Hurricane force/strength/very strong destructive winds (2).", "Torrential rainfall/heavy rainfall/thunderstorms (2).", "Hailstorms (2).",
        "Lightning (2)."],
        ["This is the most dangerous part of the cyclone.", "Why is this part called the dangerous semicircle?"], each=2),
    rub("1.4.5", "Explain why Tropical Cyclone Dikeledi intensified from 8 January to 13 January 2025.", 4, [
        "It moved from land/Madagascar to the warmer waters (Mozambique Channel), resulting in increased evaporation/latent heat (2). Part mark: it "
        "moved from land/Madagascar to the warmer waters (1).",
        "Less frictional drag over the ocean increases the wind speed (2). Part mark: less frictional drag over the ocean (1).",
        "The (central) pressure dropped (996 hPa to 976 hPa) due to the warmer ocean (2). Part mark: the (central) pressure dropped (1)."],
        ["Compare its position on 8 and 13 January: over land or over the sea?", "Compare the pressure and wind speed on the two dates."], each=2)]
q15 = [
    term("1.5.1", "Name ONE South African city indicated on the synoptic weather map that is experiencing berg wind conditions.",
         ["East London", "Durban"], ["Berg winds blow from the interior to the coast.", "Look for coastal stations with high temperatures."]),
    rub("1.5.2", "Give evidence from the synoptic weather map to support your answer to QUESTION 1.5.1.", 2, [
        "A large temperature range (2).", "High air temperatures/an air temperature of 34 °C/27 °C (2).", "Low humidity/dry air/clear sky (2).",
        "(Accept: the presence of the Kalahari high and a coastal low) (2)."],
        ["Read the station model: the top number is the temperature, the bottom the dew point.",
         "Compare the two numbers at your city with those at Cape Town: what does the gap tell you about the air?"], each=2),
    rub("1.5.3", "Explain the processes that lead to berg winds being warm and dry.", 4, [
        "TEMPERATURE: the air descends (from the interior) down the escarpment (2).",
        "TEMPERATURE: the air is heated adiabatically (1 °C/100 m) (2).",
        "MOISTURE: moisture is evaporated as the air descends (from the interior to the coast) (2)."],
        ["Think about which way the air moves between the plateau and the coast, and what that does to its temperature.",
         "Then think about what happens to the moisture in air that is warming up."], each=2, must=[2]),
    rub("1.5.4", "The warm and dry conditions can influence veld fires. In a paragraph of approximately EIGHT lines, suggest sustainable strategies "
        "that can be put in place to reduce the negative impact of veld fires.", 8, [
        "Create firebreaks/a buffer zone (accept examples) (2).", "Build water storage facilities (accept examples) (2).",
        "Educate the community about strategies they could implement (accept examples) (2).", "Make emergency services accessible (accept examples) (2).",
        "Access to fire-fighting equipment (2).", "Implement early warning systems (accept examples) (2).",
        "Create emergency assembly points (accept examples) (2).", "Create awareness (accept examples) (2).", "Create lookout towers (2).",
        "Install sprinklers (2).", "Evacuation routes and plans (accept examples) (2).", "Remove alien vegetation/plants (which are flammable) (2)."],
        ["Think before (prevention), during (fighting) and after (recovery).",
         "Pick strategies that make a fire less likely, or less harmful when it comes."], each=2)]

# ---- QUESTION 2: GEOMORPHOLOGY, the question paper pages 9-14 and the memo pages 8-10 ----
q21 = [
    mcq("2.1.1", "The main river A and its tributaries are referred to as a …", ["catchment area", "river system"], 1,
        ["Is it the land, or the rivers themselves?", "The main river with all its tributaries."], figure=fig("2.1", BASIN)),
    mcq("2.1.2", "The ... in area B separates one stream from another.", ["watershed", "interfluve"], 1,
        ["Look at the streams on either side of B.", "Do the streams beside B end up in the same main river, or in different rivers?"],
        figure=fig("2.1", BASIN)),
    mcq("2.1.3", "The area at C will have a ... infiltration rate.", ["low", "high"], 1,
        ["C is covered in vegetation.", "Think about what plant roots and leaf litter do to rain that falls on them."], figure=fig("2.1", BASIN)),
    mcq("2.1.4", "The river at D is a ... river.", ["permanent", "periodic"], 0,
        ["Check the KEY.", "Solid line or dashed line?"], figure=fig("2.1", BASIN)),
    mcq("2.1.5", "The confluence on the sketch is located at …", ["E", "F"], 0,
        ["A confluence is where two rivers meet.", "Which circle marks a meeting of streams?"], figure=fig("2.1", BASIN)),
    mcq("2.1.6", "... will increase in area G due to the steep slope.", ["Infiltration", "Run-off"], 1,
        ["On a steep slope water has little time to soak in.", "Where does rain go if it cannot soak in?"], figure=fig("2.1", BASIN)),
    mcq("2.1.7", "The stage of the river at H is the … course.", ["lower", "middle"], 0,
        ["H is near the sea.", "Wide bends and gentle gradients."], figure=fig("2.1", BASIN)),
    mcq("2.1.8", "The water table at I will resemble … (KEY: dashed line, rainy season water table; dotted line, dry season water table)",
        ["Both the rainy-season and the dry-season water tables lie above the river bed.",
         "The rainy-season water table lies above the river bed; the dry-season water table lies well below it."], 1,
        ["Check the KEY for the river at I.", "A periodic river flows only when the water table reaches its bed."], figure=fig("2.1", BASIN))]
q22 = [
    mcq("2.2.1", "A river that has its water diverted into another river is referred to as a …",
        ["captured stream.", "stream piracy.", "captor stream.", "headward stream."], 0,
        ["It loses its water.", "The 'victim' of river capture."], figure=fig("2.2", CAPTURE)),
    mcq("2.2.2", "Rivers flowing over areas with a … are more likely to be the captor stream.",
        ["gentle gradient and soft rock", "steep gradient and low rainfall", "steep gradient and soft rock", "heavy rainfall and resistant rock"], 2,
        ["The captor erodes headward faster.", "What makes erosion fast?"], figure=fig("2.2", CAPTURE)),
    mcq("2.2.3", "Evidence that river capture has taken place in sketch B:",
        ["River Y has more water flowing in it.", "River Y has captured the headwaters of river X.", "River X has captured the headwaters of river Y.",
         "River X has a smaller drainage basin."], 2,
        ["Compare sketches A and B.", "Which river now has the other's headstreams?"], figure=fig("2.2", CAPTURE)),
    mcq("2.2.4", "The cause of river capture, as shown in sketch B, is …",
        ["headward erosion by river Y.", "lateral erosion by river X.", "headward erosion by river X.", "vertical erosion by river Y."], 2,
        ["The captor cut back into its source area.", "Erosion towards the source is called ..."], figure=fig("2.2", CAPTURE)),
    mcq("2.2.5", "The part of the river that has less water after river capture is known as the … stream.",
        ["captor", "non-perennial", "perennial", "misfit"], 3,
        ["Look at the dashed part of river Y in sketch B.", "Compare the size of the stream with the size of the valley it flows in."],
        figure=fig("2.2", CAPTURE)),
    mcq("2.2.6", "River X has more erosive power after river capture because of …",
        ["a greater volume of water and turbulent stream flow.", "a greater volume of water and laminar flow.",
         "headward erosion and turbulent stream flow.", "rejuvenation and laminar flow."], 0,
        ["It gained the captured stream's water.", "Of the two kinds of flow named in the options, which one erodes more?"],
        figure=fig("2.2", CAPTURE)),
    mcq("2.2.7", "The physical (natural) impact of river capture on the captor stream is that the … and …\n(i) drainage basin decreases\n"
        "(ii) river rejuvenation takes place\n(iii) deposition increases\n(iv) water flows faster",
        ["(i) and (iv)", "(i) and (iii)", "(ii) and (iv)", "(ii) and (iii)"], 2,
        ["The captor gains water, and its basin grows.", "More water means more energy to erode."], figure=fig("2.2", CAPTURE))]
q23 = [
    rub("2.3.1", "What is a longitudinal profile?", 2, ["A side view of a river from source to mouth (2). Part mark: a side view of the river (1)."],
        ["Look at sketches A and B: from where to where does each line run, and from which angle are you looking?",
         "Compare it with a cross-profile, like C and D."], each=2),
    mcq("2.3.2", "Which ONE of the sketches above shows a graded longitudinal profile?", ["A", "B"], 1,
        ["A graded river has reached a smooth balance.", "Follow each line from source to mouth: does anything interrupt it?"]),
    lst("2.3.3", "Give evidence in the sketch to support your answer to QUESTION 2.3.2.", 2,
        [["No temporary base levels", "No knickpoints"], ["No obstructions", "No waterfalls", "No dams"], ["Smooth concave shape", "Concave shape"]],
        ["Compare B with A.", "What is missing from B's line, and what shape is it?"]),
    {"t": "match", "n": "2.3.4", "marks": 2, "q": "Classify EACH of the temporary base levels in sketch A as either natural or human-made.",
     "clues": ["Sketch A labels a waterfall and a dam.", "Which one did people build?"],
     "left": ["Waterfall", "Dam"], "right": ["Natural", "Human-made"], "a": [0, 1], "groups": True, "heads": ["TEMPORARY BASE LEVEL", "TYPE"]},
    rub("2.3.5", "Why is the sea indicated as the permanent base level?", 2, ["It is the lowest (ultimate) level to which a river can erode (2)."],
        ["Think about what stops a river from cutting its bed any deeper.", "Where does every river end?"], each=2),
    rub("2.3.6", "Refer to cross-profiles C and D. Differentiate between the shapes of the cross-profiles at C and D.", 2, [
        "Profile C is a closed V-shape (narrow, deep and steep-sided) whereas profile D is an open U-shape (very wide and gently sloping) (2)."],
        ["C is near the source, D near the mouth.", "Look at the sides and the width of each cross-profile."], each=2),
    rub("2.3.7", "Explain the main processes that give rise to the difference in the shape of cross-profiles C and D.", 4, [
        "Profile C: vertical/downward erosion is dominant in the upper course (2).",
        "Profile D: deposition is dominant in the lower course (2).", "Profile D: lateral erosion occurs (2)."],
        ["Compare the river's energy and gradient near the source and near the mouth.",
         "What does the river mostly do with that energy in each place?"], each=2, must=[0])]
q24 = [
    mcq("2.4.1", "Meanders are more likely to form in the (upper/lower) stage/course of a river.", ["Upper", "Lower"], 1,
        ["Meanders need a gentle gradient.", "Where does the river slow down?"]),
    rub("2.4.2", "Account for the gentle gradient of the inner bank at C in photograph A.", 2, ["Due to deposition (2).", "Slow movement/velocity of water (2)."],
        ["C is the inside of the bend.", "Compare how fast the water moves on the inside and on the outside of the bend."], each=2),
    rub("2.4.3", "Refer to photograph B and cross-section E–F. How does the process of river rejuvenation lead to the formation of incised meanders?", 4, [
        "River rejuvenation results in vertical (downward) erosion (2).", "It results in a deeper stream channel/valley (due to vertical erosion) (2)."],
        ["Rejuvenation gives the river new energy.", "Look at cross-section E–F: in which direction has that energy been used?"], each=2),
    rub("2.4.4", "Refer to photograph A. In a paragraph of approximately EIGHT lines, explain how an oxbow lake is formed.", 8, [
        "Continuous (lateral) erosion takes place on the outer bank/undercut slope (2).", "Deposition on the inner bank/slip-off slope (2).",
        "The meander neck narrows (2).", "The river floods and cuts through the meander neck (2).",
        "The meander loop is separated from the main stream (by deposition, resulting in an oxbow lake) (2)."],
        ["Start with erosion and deposition on the two banks.",
         "Then think about what happens to the narrow strip of land between two bends during a flood."], each=2)]
q25 = [
    # the first entry of a group is the memo point a learner is shown (the lead rule keys on its first words: "service", "means")
    lst("2.5.1", "According to the extract, why are dense settlements along rivers associated with pollution?", 1,
        [["Service provision is poor", "Service provision", "Services"],
         ["Means to pay for waste removal are lacking", "Means to pay for waste removal", "Cannot pay for waste removal", "Unable to pay"],
         ["Waste disposed of in the river", "Dump waste in the river", "Piled-up waste"]],
        ["Read the extract's first paragraph.", "What service do they not get?"]),
    lst("2.5.2", "Give TWO reasons from the photograph to support your answer to QUESTION 2.5.1.", 2,
        [["Solid waste", "Rubbish", "Litter"], ["No infrastructure to remove waste", "No refuse bins", "No waste removal"],
         ["No potable water", "No clean water"]],
        ["Look at the river bed and the banks.", "What is missing that a serviced area would have?"]),
    rub("2.5.3", "Explain how the rise in the water level of the river will negatively affect the houses (in the photograph) due to their location.", 2, [
        "The houses are close to the river and could easily flood (2). Part mark: the houses are close to the river (1).",
        "The river banks could collapse, destroying houses (accept examples) (2). Part mark: the river banks could collapse (1)."],
        ["Where are the houses built?", "What happens to the banks and the houses when the river rises?"], each=2),
    rub("2.5.4", "Explain the negative impact of poor river management on the health of rivers.", 4, [
        "Reduced water quality (accept examples) (2).", "Damages habitat for aquatic life (2).", "Destroys aquatic life (accept examples) (2).",
        "Destroys food chains/food webs (2).", "Causes eutrophication (accept examples) (2).", "Disrupts ecosystems (2).", "Loss of biodiversity (2).",
        "Increased sedimentation (accept examples) (2)."],
        ["A river is an ecosystem.", "Picture the river downstream of the settlement in the photograph."], each=2),
    rub("2.5.5", "Suggest strategies that the municipality can put in place to ensure the sustainability of the river in the photograph.", 6, [
        "Relocate the people (2).", "Create a buffer zone (2).", "Create awareness campaigns (accept examples) (2).",
        "Educate people on river management (accept examples) (2).", "Encourage people not to build houses on the river bank (2).",
        "Implement legislation (2).", "Impose fines (2).", "Plant more vegetation (accept examples) (2).",
        "Provide more refuse removal facilities (accept examples) (2).", "Continuous monitoring/testing (2).",
        "Encourage community involvement (accept examples) (2).", "Provide incentives to people (accept examples) (2).",
        "Encourage the recycling of waste (2).", "Build proper sanitation/drainage systems/water treatment plants (2).", "Maintain infrastructure (2)."],
        ["The municipality provides services and makes by-laws.", "Think about what the municipality can provide, enforce and teach."], each=2)]

# ---- QUESTION 3 (SECTION B): only the parts that do not read the maps, the question paper pages 15-18 and the memo pages 11-12 ----
q3a = [
    mcq("3.2.1", "Stellenbosch has a … climate.", ["tropical", "arid", "Mediterranean", "subtropical"], 2,
        ["Read the general information on Stellenbosch.", "Warm, dry summers and cool, rainy winters."]),
    mcq("3.3.1", "The number 310, labelled M on the main road in block A3 on the topographical map, is referred to as … data.",
        ["spatial", "vector", "attribute", "numerical"], 2,
        ["The number describes the road; it is not its position.", "Information ABOUT a feature is ... data."]),
    rub("3.3.3", "Refer to area 9 in block A3 on the orthophoto map. Using data manipulation, explain how you would manipulate the scale at area 9 "
        "to make the image clearer.", 2, ["Make the scale larger (2)."],
        ["To see more detail, you zoom in.", "Zooming in changes the scale: larger or smaller?"], each=2),
    mcq("3.3.4", "… refers to the clarity of an image.", ["Data integration", "Buffering", "Data sharing", "Resolution"], 3,
        ["How sharp is the picture?", "More pixels, more detail."])]
q3b = [
    mcq("3.3.5", "Which photograph, A or B, has fewer pixels?", ["A", "B"], 0,
        ["Fewer pixels: each pixel is bigger.", "Which image looks blocky?"]),
    rub("3.3.6", "Give a reason for your answer to QUESTION 3.3.5.", 2, [
        "The clarity of the photograph is poor (2).", "There is low resolution (2).", "It shows less detail (2).",
        "The image is blurry/unclear/distorted (2).", "Large pixels (2)."],
        ["Compare the detail you can see in A and B.", "What does fewer pixels do to how much detail you can see?"], each=2)]

STELLENBOSCH = ("GENERAL INFORMATION ON STELLENBOSCH\n\nCoordinates: 33°45′S; 18°45′E\n\nStellenbosch is located in a hilly, sheltered valley within "
                "the Cape Winelands, with an average elevation of 136 metres above sea level, surrounded by hills and mountains, like Papegaaiberg, "
                "Stellenboschberg, and the Jonkershoek, Drakenstein and Simonsberg mountain ranges. It is situated approximately 50 kilometres east "
                "of Cape Town.\n\nStellenbosch has a Mediterranean climate with warm, dry summers and cool, rainy winters.\n\nThe Eerste River "
                "originates in the Jonkershoek Mountains, 60 kilometres east of Cape Town, and flows through the Jonkershoek Valley before reaching "
                "Stellenbosch.")
RIVERS = ("IMPACT OF SETTLEMENTS ON RIVER MANAGEMENT\n\nDense settlements that locate along rivers have a negative impact on rivers. The main "
          "reason is that these settlements generally receive poor service provision. These poor communities also do not have the means to pay for "
          "the provision of services, such as waste removal.\n\nWhen large amounts of waste pile up in the settlement, the community is more likely "
          "to dispose of the waste in the river. This leads to further pollution, eventually leading to serious health risks for the community.")
sec_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Synoptic weather maps", "marks": 8,
     "lead": "The questions are based on synoptic weather map interpretation. Complete the statements in COLUMN A with the options in COLUMN B.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Slope aspect and valley climates", "marks": 7,
     "lead": "Various options are provided as possible answers to the following questions. Refer to the photograph on slope aspect for QUESTIONS "
             "1.2.1 to 1.2.3, and the photograph on valley winds for QUESTIONS 1.2.4 to 1.2.7.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Mid-latitude cyclones", "marks": 15, "lead": "Refer to the sketches below on the mid-latitude cyclone.",
     "figure": fig("1.3", "Four panels. A: lines of latitude at 30°S, 60°S and 90°S; WARM AIR moves east above a thick line labelled BOUNDARY "
                   "BETWEEN TWO AIR MASSES at 60°S, COLD AIR moves west below it. B: a mid-latitude cyclone with a cold front (triangles, E–F "
                   "across it) and a warm front (semicircles), isobars 1008 and 1004, warm air in the sector between them, cold air behind, "
                   "station models (8 and −2; 11 and 1). C: a photograph of palm trees bent by strong wind and rain. D: a photograph of a car "
                   "driving through a flooded street."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Tropical cyclones", "marks": 15, "lead": "Refer to the infographic below on Tropical Cyclone Dikeledi.",
     "figure": fig("1.4", "An infographic. A, FACT FILE: Tropical Cyclone Dikeledi was first observed off the north-east coast of Madagascar. "
                   "8 January 2025: pressure in the centre 996 hPa, maximum wind speed 75 km/h. 13 January 2025: pressure in the centre 976 hPa, "
                   "maximum wind speed 150 km/h. B, LOCATION MAP: southern Africa and Madagascar with the equator (0°), 5°S and 20°S; Dikeledi "
                   "marked between 5°S and 20°S north of Madagascar. C, SATELLITE IMAGE (8 January): a cloud spiral near Madagascar. "
                   "D, SATELLITE IMAGE (13 January): a large cyclone with a clear eye, Madagascar to its east; the forward left-hand "
                   "quadrant marked with a dashed line."), "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Berg winds", "marks": 15, "lead": "Refer to the synoptic weather map below showing South African berg winds.",
     "figure": fig("1.5", "A synoptic weather map of southern Africa: a high (H, 1016 hPa) over the interior, lows (L) on the west and off the "
                   "south-east coast, a cold front approaching Cape Town (isobars 996 to 1012 hPa). Station models: Windhoek 12/8; Maputo 21/12; "
                   "Durban 27/10; East London 34/10; Cape Town 12/12. Text: Extremely hot and uncomfortable conditions are expected across the "
                   "Eastern Cape. Temperatures are expected to rise above 30 °C."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Drainage basins", "marks": 8,
     "lead": "Refer to the sketch below based on drainage basins. Complete the statements in COLUMN A with the options in COLUMN B.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "River capture", "marks": 7,
     "lead": "Refer to the sketches below on river capture. Various options are provided as possible answers to the following questions.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "River profiles", "marks": 15, "lead": "Refer to the sketches below showing two longitudinal river profiles.",
     "figure": fig("2.3", "Two river profiles, each labelled SOURCE on the left and MOUTH at the sea on the right. A: a profile with a "
                   "waterfall over resistant rock and a dam, both arrowed from the label temporary base level; the sea level is labelled "
                   "the permanent base level. B: a profile with cross-profile C drawn near the source and cross-profile D near the mouth; "
                   "the sea level is labelled the permanent base level."),
     "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Meanders", "marks": 15, "lead": "Refer to photographs A and B below showing meanders.",
     "figure": fig("2.4", "Two photographs with cross-sections. A: an aerial photograph of a winding river through farmland, a line C–D across one "
                   "bend; its cross-section slopes gently down from C and rises steeply at D. B: a river looping deeply between steep, wooded "
                   "valley sides, a line E–F across it; its cross-section has steep sides on both banks."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Catchment and river management", "marks": 15,
     "lead": "Refer to the extract and photograph below on catchment and river management.", "extract": RIVERS,
     "figure": fig("2.5", "A photograph of a narrow, shallow river channel full of rocks and rubbish, with rows of corrugated-iron shacks built "
                   "right up to both banks."), "items": q25},
]
sec_b = [
    {"id": "3", "title": "Question 3", "kind": "Geographical skills and techniques", "marks": 5,
     "lead": "The parts of Question 3 that do not read the topographical or orthophoto map.", "extract": STELLENBOSCH, "items": q3a},
    {"id": "3.3.5", "title": "Question 3.3.5", "kind": "Comparing images", "marks": 3,
     "lead": "Refer to the images of the Danie Craven Stadium below, extracted from block D1/D2 on the orthophoto map.",
     "figure": fig("3.3", "Two images, A and B, of the same sports stadium side by side."), "items": q3b},
]


# ---- Written answers as STATEMENTS (Murci 2026-10-10; helpers as in transcribe_bs_p2_2025_11.py) ----
# A written part plays as picking statements: the memo's own points (right, tidied to one reading of its "/" alternatives) and
# CLEARLY wrong ones (the opposite, or a confusion with another concept; never a true point the memo leaves out, which its
# "any other relevant answer" would make right). The learner picks marks/each of them, any right one counts (the memo's "any N"),
# each right pick earns `each` (the memo's ticks: 2 a point throughout this paper). The cards are shuffled the same way every run.
def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("geo-p1-2025-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    "1.3.6": (2, ["The air behind the cold front is colder than the air in front of the warm front.",
                  "The cold air behind the cold front undercuts the warmer air in front of the warm front.",
                  "The warmer (less dense) air is uplifted over the colder (denser) air."],
                 ["The air behind the cold front is warmer than the air in front of the warm front.",
                  "The warmer air undercuts the colder air and lifts it off the ground.",
                  "The warm front moves faster than the cold front and pulls away from it."]),
    "1.4.3": (2, ["Coriolis force is present within these latitudes, resulting in deflection.",
                  "High temperatures (warm oceans) promote a high evaporation rate.", "Latent heat is released during condensation.",
                  "A high evaporation rate leads to intense low pressure."],
                 ["There is no Coriolis force between 5° and 20° south, so the air rises straight up.",
                  "The cold ocean water at these latitudes cools the air so that it sinks.",
                  "Little evaporation takes place over these oceans, so no latent heat is released."]),
    "1.4.4": (2, ["There are hurricane-force, very strong destructive winds.", "There is torrential rainfall.", "Hailstorms occur.",
                  "Lightning occurs."],
                 ["The weather is calm, with clear skies.", "There are only light winds and a little drizzle.",
                  "Temperatures drop below freezing and snow falls."]),
    "1.4.5": (2, ["It moved from land (Madagascar) to the warmer waters of the Mozambique Channel, resulting in increased evaporation.",
                  "Less frictional drag over the ocean increases the wind speed.",
                  "The central pressure dropped (996 hPa to 976 hPa) due to the warmer ocean."],
                 ["It moved over land, where more friction increased its wind speed.",
                  "The central pressure rose from 976 hPa to 996 hPa.", "It moved over colder water, which gave it more energy."]),
    # 1.5.2 "Large temperature range" read on the station model: the gap between the air temperature and the dew point (34 and 10)
    "1.5.2": (2, ["There is a large range between the air temperature and the dew point temperature.",
                  "The air temperature is high (34 °C at East London, 27 °C at Durban).", "The humidity is low: the air is dry."],
                 ["The air temperature and the dew point temperature are the same, so the air is saturated.",
                  "The station model shows heavy rain falling.", "The wind blows onshore, from the ocean towards the land."]),
    "1.5.4": (2, ["Create firebreaks.", "Build water storage facilities.", "Implement early warning systems.",
                  "Remove flammable alien vegetation.", "Install sprinklers."],
                 ["Plant more flammable alien vegetation near homes.", "Let dry grass build up around houses and farms.",
                  "Block the access roads so that fire engines cannot reach the area."]),
    "2.3.1": (2, ["A side view of a river from source to mouth."],
                 ["A view across a river valley from one side to the other.", "A view of a river and its tributaries from above.",
                  "The area of land drained by a river and its tributaries.", "The point where a river flows into the sea."]),
    "2.3.5": (2, ["It is the lowest (ultimate) level to which a river can erode."],
                 ["It is the highest level, at the source, where the river starts.", "It is a level set for a while by a dam or a waterfall.",
                  "It is the level of the water table in the dry season.", "It is where the river flows fastest and erodes most."]),
    "2.3.6": (2, ["Profile C is a closed V-shape (narrow, deep and steep-sided), whereas profile D is an open U-shape (very wide and gently sloping)."],
                 ["Profile C is an open U-shape (very wide and gently sloping), whereas profile D is a closed V-shape (narrow, deep and steep-sided).",
                  "Profiles C and D are both closed V-shapes (narrow, deep and steep-sided).",
                  "Profiles C and D are both open U-shapes (very wide and gently sloping).",
                  "Profile C is wider than profile D, but both have gently sloping sides."]),
    "2.4.2": (2, ["It is due to deposition.", "The water moves slowly (low velocity)."],
                 ["It is due to erosion by fast-flowing water.", "The water flows fastest on the inner bank.",
                  "The river undercuts the inner bank."]),
    "2.4.3": (2, ["River rejuvenation results in vertical (downward) erosion.", "It results in a deeper stream channel (valley)."],
                 ["River rejuvenation results in more deposition, which fills the channel.", "It results in a wider, shallower channel.",
                  "The meander loop is cut off and becomes an oxbow lake.", "The river loses energy and stops eroding."]),
    "2.4.4": (2, ["Continuous (lateral) erosion takes place on the outer bank (undercut slope).",
                  "Deposition takes place on the inner bank (slip-off slope).", "The meander neck narrows.",
                  "The river floods and cuts through the meander neck.",
                  "The meander loop is separated from the main stream (by deposition), resulting in an oxbow lake."],
                 ["Deposition takes place on the outer bank, where the water flows fastest.", "The meander neck widens over time.",
                  "The lake forms where the river flows into the sea."]),
    "2.5.3": (2, ["The houses are close to the river and could easily flood.", "The river banks could collapse, destroying the houses."],
                 ["The houses are built far from the river, so the rising water cannot reach them.",
                  "Rising water makes the river banks stronger.", "A rise in the water level lowers the risk of flooding."]),
    "2.5.4": (2, ["The water quality is reduced.", "Habitats for aquatic life are damaged.", "Eutrophication occurs.", "Biodiversity is lost."],
                 ["The water quality improves.", "Biodiversity in the river increases.", "Less sediment enters the river."]),
    "2.5.5": (2, ["Relocate the people.", "Create a buffer zone.", "Provide more refuse removal facilities.", "Impose fines.",
                  "Build proper sanitation systems."],
                 ["Allow more houses to be built on the river banks.", "Stop refuse removal to save money.",
                  "Dump the settlement's waste into the river further downstream."]),
    "3.3.3": (2, ["Make the scale larger."],
                 ["Make the scale smaller.", "Reduce the number of pixels in the image.", "Print the image on a smaller sheet of paper.",
                  "Add more map layers on top of the image."]),
    "3.3.6": (2, ["The clarity of the photograph is poor.", "The photograph has a low resolution.", "The photograph's pixels are large."],
                 ["The photograph has a high resolution.", "The photograph shows more detail.", "The photograph's pixels are smaller."]),
}
# A written part whose memo MUST cover two sides plays as a SORT (variety, Murci 2026-10-10): each statement dragged to its side, or
# to "Not true" (the clearly wrong one), 1 mark a statement; a grouped match, played as a classification.
#   1.3.4 [MUST MENTION GALE FORCE/STRONG WINDS AND HEAVY RAINFALL]: the memo's part-mark causes, sorted to the weather they explain;
#   1.5.3 [MUST INCLUDE TEMPERATURE AND MOISTURE]: its TEMPERATURE and MOISTURE points; 2.3.7 [MUST REFER TO BOTH PROFILE C AND D].
SORTS = {
    "1.3.4": (["Gale force winds (C)", "Heavy rainfall (D)", "Not true"], [
        ("There is a steep pressure gradient.", 0),
        ("There are strong updraughts (rapid upliftment of air).", 1),
        ("The air behind the cold front undercuts the warm air ahead of it.", 1),
        ("There is a gentle pressure gradient.", 2)]),
    "1.5.3": (["Why it is warm", "Why it is dry", "Not true"], [
        ("The air descends from the interior down the escarpment.", 0),
        ("The air is heated adiabatically (1 °C per 100 m).", 0),
        ("Moisture is evaporated as the air descends to the coast.", 1),
        ("The air rises over the escarpment and its moisture condenses.", 2)]),
    "2.3.7": (["Profile C", "Profile D", "Not true"], [
        ("Vertical (downward) erosion is dominant.", 0),
        ("Deposition is dominant.", 1),
        ("Lateral erosion occurs.", 1),
        ("The river deposits most of its load near its source.", 2)]),
}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("geo-p1-2025-11:sort:" + n).shuffle(order)
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
    "paper": {"subject": "Geography", "title": "Geography P1", "sitting": "November 2025", "total_marks": 128, "time": "3 hours"},
    "sections": [{"title": "Section A: Climate and weather and geomorphology", "total": 120, "missions": sec_a},
                 {"title": "Section B: Geographical skills and techniques", "total": 8, "missions": sec_b}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "Section A whole and the map-free parts of Section B, hand-transcribed from the paper and "
                                                           "memo PDFs and their page images; no API call."},
        {"n": "3", "kind": "no_fit", "detail": "Section B reads the 1:50 000 topographical map 3318DD STELLENBOSCH and the 1:10 000 orthophoto map "
                                               "3318 DD 18, handed out in the exam room: not in the question paper and not published. Its 22 "
                                               "marks that read them (3.1.1-3.1.6, 3.2.2-3.2.8, 3.3.2) wait for the maps; the paper totals the "
                                               "128 marks that can be played (the printed paper: 150)."},
        {"n": "2.1.8", "kind": "no_fit", "detail": "The two options are drawings (cross-sections of a river channel with the two water tables): "
                                                   "played as words that describe each drawing."},
        {"n": "1.3.6", "kind": "no_fit", "detail": "Written answers play as statements (pick the memo's points among clearly false ones, 2 marks "
                                                   "a right pick, the memo's ticks); the memo's part marks (1 for a point without its explanation) "
                                                   "are not awarded in that format."},
        {"n": "1.3.4", "kind": "no_fit", "detail": "The memo's 'must mention' rules (1.3.4 winds AND rainfall, 1.5.3 temperature AND moisture, "
                                                   "2.3.7 profile C AND D) play as sorts: its points dragged to the side they explain, with one "
                                                   "false statement, 1 mark a statement (1.3.4 sorts the memo's part-mark causes)."},
        {"n": "2.1.4", "kind": "memo_issue", "detail": "COLUMN B (Y) prints 'permanant'; transcribed 'permanent' (the paper's typo)."},
        {"n": "1.3.5", "kind": "no_fit", "detail": "The cold-front cross-section is drawn on paper and self-checked against the memo's criteria."},
        {"n": "paper", "kind": "memo_issue", "detail": "The memo's page 3 is a marked sample from another paper (its answers, e.g. 1.1.1 'South "
                                                       "Atlantic High' and 1.2.1 'Melting snow', match nothing here): ignored."},
    ],
}
out = Path(__file__).parent / "out" / "geo-p1-2025-11"
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
