"""Grade 10 Geography P1 November 2024 (North West Department of Education, provincial assessment): SECTION A whole (Questions 1 and
2, 120 marks) and the parts of SECTION B (Question 3) that do not read the maps (15 of its 30 marks), hand-transcribed into the
catalogue format, then run through `ingest.py --from-json`. Stems, options, marks, answers and the memo's points are the paper's and
the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment,
the question paper PDF (English, 17 pages, text layer; its sketches are images) and the marking guidelines PDF (English, 9 pages).

  python tools/ingest/transcribe_g10_geo_p1_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-geo-p1-2024-11-nw/06-NOVEMBER-24-NW-GR10-S2-Gography-QP-P1-ENG.pdf" "uploads/provincial/g10-geo-p1-2024-11-nw/06-November-24-NW-GR-10-S2-Geography-MG-P1-ENG.pdf" --id g10-geo-p1-2024-11-nw --from-json

SECTION B reads a 1 : 50 000 topographical map and a 1 : 10 000 orthophoto map of 2931CA Verulam handed out in the exam room: not in
the question paper and not in the download. As Grade 11's Geography P1 (transcribe_g11_geo_p1_2024_11_ec.py), its 15 marks that read
the maps (3.1.5-3.1.7, 3.2.2-3.2.4, 3.2.6-3.2.8) wait for the maps; the rest plays. The paper totals what is playable, 135.

The Geography rulings, as Grade 12: a choice between brackets or two columns is multiple choice of the choices; a written answer is
statements (the memo's points and clearly wrong ones, a card worth what the memo ticks); 'differentiate/distinguish' is a sort; a
quote from an extract is a pick. 2.1.5-2.1.8 print Z above Y; the memo's letters follow the Y-above-Z order of 2.1.1-2.1.4, so its
answers name limbs, asymmetrical, recumbent and isoclinal folds: those play as the named choices (flag below).
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper, sentences

P = Paper("g10-geo-p1-2024-11-nw", 595.32, 841.92, {
    "1.1": [3, 93, 210, 536, 380], "1.3": [5, 92, 128, 532, 373], "1.5": [7, 92, 113, 535, 423], "2.1": [8, 93, 180, 535, 341],
    "2.2": [9, 93, 140, 535, 428], "2.3": [11, 93, 113, 531, 293], "2.4": [12, 93, 377, 535, 590], "2.5": [13, 93, 236, 531, 444],
    "3.3": [16, 93, 534, 535, 675]}, start=5)
answer, stmt, mcq, term, sort = P.answer, P.stmt, P.mcq, P.term, P.sort
pick = lambda n, q, opts, pool, clues, count: {"t": "pickn", "n": n, "marks": count, "q": q, "clues": clues, "opts": opts, "pool": pool,
                                               "count": count}
two = lambda n, q, a_opt, b_opt, a, clues, marks=1: mcq(n, q, [a_opt, b_opt], a, clues, marks=marks)
WC = ["evaporation", "condensation", "precipitation"]
wc = lambda n, q, a, clues: mcq(n, q, WC, a, clues, marks=1)
BOUND = ["divergent", "convergent", "transform fault"]

# ---- SECTION A, QUESTION 1: THE ATMOSPHERE, the question paper pages 3-7 and the memo pages 2-4 ----
q11 = [
    wc("1.1.1", "… occurs when water changes from a liquid to a gas.", 0, ["Liquid to gas.", "The sun heats the sea."]),
    wc("1.1.2", "… happens when water changes from a gas to a liquid.", 1, ["Gas to liquid.", "Droplets form."]),
    wc("1.1.3", "… occurs when water falls from clouds.", 2, ["Water falling.", "Rain, hail, snow."]),
    wc("1.1.4", "Snow is an example of …", 2, ["Snow falls from clouds.", "A form of falling water."]),
    wc("1.1.5", "The heating of water surfaces will result in …", 0, ["Heat turns water into vapour.", "Liquid to gas."]),
    wc("1.1.6", "Mist is an example of …", 1, ["Tiny droplets in the air.", "Vapour that has turned to liquid."]),
    wc("1.1.7", "Clouds form when … occurs.", 1, ["Vapour cools into droplets.", "Gas to liquid."])]
q12 = [
    two("1.2.1", "(Insolation/Reflection) is the amount of incoming sunlight that is bounced off clouds and Earth's surface back into space.",
        "Insolation", "Reflection", 1, ["Bounced back.", "Like a mirror."]),
    two("1.2.2", "(Insolation/Absorption) is the amount of incoming sunlight that strikes a surface.", "Insolation", "Absorption", 0,
        ["Incoming solar radiation.", "In-sol-ation."]),
    two("1.2.3", "Transfer of heat in the form of waves is known as (reflection/radiation).", "reflection", "radiation", 1,
        ["Waves travel through space.", "The sun's heat reaches us this way."]),
    two("1.2.4", "(Conduction/Convection) is the transfer of heat between substances that are in direct contact with each other.",
        "Conduction", "Convection", 0, ["Touching.", "A hot pan heats your hand."]),
    two("1.2.5", "The transfer of heat by air circulation of warm and cold air is called (conduction/convection).", "conduction",
        "convection", 1, ["Air moves in currents.", "Warm air rises."]),
    two("1.2.6", "(Latitude/Albedo) is a measure of how much a surface reflects heat.", "Latitude", "Albedo", 1,
        ["Snow has a high one.", "Reflectivity."]),
    two("1.2.7", "(Ocean currents/River flow) are large-scale circulations of ocean water.", "Ocean currents", "River flow", 0,
        ["Large-scale and in the ocean.", "The Benguela is one."]),
    two("1.2.8", "The Sun's energy is called (solar radiation/terrestrial radiation).", "solar radiation", "terrestrial radiation", 0,
        ["Solar means sun.", "Terrestrial means earth."])]
q13 = [
    stmt("1.3.1", "Define the concept of atmosphere.", 2,
         ["The atmosphere is the layer of air that surrounds the Earth.", "The blanket of gases surrounding the Earth."],
         ["The atmosphere is the water on the Earth's surface.", "The atmosphere is the rock layer under the soil.",
          "The atmosphere is the Earth's core.", "The atmosphere is the space between the planets."],
         ["It is made of gases.", "It surrounds the Earth."], 2),
    two("1.3.2(a)", "In the troposphere, it gets (colder/hotter) with an increase in height.", "colder", "hotter", 0,
        ["Follow the line from 0 to 15 km.", "Mountain tops are cold."]),
    two("1.3.2(b)", "In other words, in the troposphere the temperature (increases/decreases) with altitude.", "increases", "decreases", 1,
        ["Colder with height means …", "Read the graph's lowest layer."]),
    stmt("1.3.3", "Describe the temperature pattern in the thermosphere.", 1,
         ["The temperature increases with height.", "It gets hotter as altitude increases."],
         ["The temperature decreases with height.", "The temperature stays the same with height.", "The temperature drops below −80 °C."],
         ["Follow the line above 80 km.", "Does it move left or right?"], 1),
    stmt("1.3.4", "Explain why temperature increases in the stratosphere.", 2,
         ["The reaction between sunlight and the ozone in the upper stratosphere generates heat.",
          "Ozone absorbs the sun's ultraviolet radiation, which heats the layer."],
         ["The stratosphere is closest to the Earth's surface.", "Clouds in the stratosphere trap heat.",
          "The stratosphere has no air, so it is hot.", "Rain releases heat in the stratosphere."],
         ["The ozone layer is in the stratosphere.", "What does ozone absorb?"], 2),
    term("1.3.5", "In which layer of the atmosphere will you find the ozone layer?", ["stratosphere"],
         ["Look at the arrow on the graph.", "Between the tropopause and the stratopause."]),
    stmt("1.3.6", "Name ONE human activity responsible for ozone depletion.", 1,
         ["CFCs used as propellants in aerosol sprays", "CFCs used as coolants in refrigerators", "CFCs used in air conditioning systems"],
         ["Planting trees", "Using solar energy", "Recycling paper"], ["CFCs destroy ozone.", "Sprays and fridges."], 1),
    stmt("1.3.7", "Explain the importance of the ozone layer for human life.", 2,
         ["The ozone layer absorbs most of the sun's harmful UV rays and acts as a natural sun shield.",
          "It protects people from skin cancer caused by ultraviolet rays."],
         ["The ozone layer produces rain for crops.", "The ozone layer supplies oxygen for breathing.",
          "The ozone layer keeps the Earth cold.", "The ozone layer blocks all sunlight."],
         ["What does ozone absorb?", "UV rays harm skin and eyes."], 2),
    stmt("1.3.8", "Suggest methods that can be implemented to reduce ozone depletion.", 4,
         ["Use products labelled 'ozone friendly'.", "Replace all CFCs.", "Run educational awareness programmes.",
          "Set emission limits for harmful gases.", "Reduce the use of fertilisers."],
         ["Use more aerosol sprays.", "Burn more fossil fuels.", "Remove all trees."], ["Stop what destroys ozone.", "CFCs are the main cause."], 2)]
GW = ("The drastic swing between extreme drought and unprecedented flooding is becoming common in South Africa. Water stress is expected to "
      "significantly affect poor, disenfranchised communities as well as ecosystems that have been underfunded and exploited. The intensity "
      "of extreme drought and rainfall has 'sharply' increased over the past years. These are not merely tough weather events, they are "
      "leading to extremes such as crop failure, infrastructure damage, and even humanitarian crises.")
q14 = [
    stmt("1.4.1", "Define the concept of global warming.", 2,
         ["An increase in the temperature near the Earth's surface.", "The rise in the average temperature of the Earth's atmosphere."],
         ["A decrease in the Earth's temperature.", "The warming of the Earth's core.", "A hot day in summer.", "The heating of water in a kettle."],
         ["It is about the whole Earth.", "Is the temperature rising or falling?"], 2),
    stmt("1.4.2", "Name ONE human factor that contributes to global warming.", 1,
         ["Burning coal for power generation", "Burning oil-based fuels for transport", "Deforestation", "Overgrazing"],
         ["Planting trees", "Using wind energy", "Walking to school"], ["Greenhouse gases.", "Burning and clearing."], 1),
    stmt("1.4.3", "According to the article, which weather conditions have become more common in South Africa because of global warming?", 2,
         ["Extreme drought", "Unprecedented (flash) flooding"], ["Snowstorms", "Tornadoes", "Hail every day"],
         ["Read the extract's first sentence.", "A swing between two extremes."], 1),
    stmt("1.4.4", "Describe TWO consequences of global warming mentioned in the extract.", 2,
         ["Water stress", "Crop failure", "Infrastructure damage", "Humanitarian crises"],
         ["More snow in summer", "Cheaper food", "Fewer floods"], ["Read the last sentence of the extract.", "Crops, buildings, people."], 1),
    stmt("1.4.5", "In a paragraph of approximately EIGHT lines, recommend sustainable solutions the government can implement to stop or slow "
         "down global warming and climate change.", 8,
         ["Reduce greenhouse gas emissions.", "Switch from fossil fuels to renewable sources of energy.",
          "Create public awareness to encourage people to conserve energy.", "Promote energy-efficient products to save energy.",
          "Encourage public transport and electric vehicles."],
         ["Build more coal-fired power stations.", "Cut down forests for farmland.", "Subsidise petrol cars."],
         ["Cut the gases that trap heat.", "Energy, transport, awareness."], 2)]
q15 = [
    term("1.5.1", "What are the black lines on the synoptic map called?", ["isobars", "isobar"],
         ["They join places of equal pressure.", "Iso means equal."]),
    two("1.5.2", "Is the pressure cell at A a high- or low-pressure cell?", "high-pressure cell", "low-pressure cell", 0,
        ["Read the isobar values towards A.", "Do they rise or fall towards the centre?"]),
    stmt("1.5.3", "State ONE factor evident on the synoptic weather map to substantiate your answer to QUESTION 1.5.2.", 2,
         ["The atmospheric pressure readings increase towards the centre of the pressure cell.",
          "The isobar values rise from 1008 to 1020 hPa towards A."],
         ["The pressure readings decrease towards the centre.", "There is a cold front at A.", "A tropical cyclone is at A.",
          "The isobars at A are labelled L."],
         ["Read the numbers on the isobars around A.", "Higher towards the middle means high pressure."], 2, after=["1.5.2"]),
    answer("1.5.4", "Describe the wind speed of station model D.", 1, ["5 knots", "15 knots", "22 knots", "10 knots"],
           ["Count the barbs on the wind arrow.", "A half barb is 5 knots."]),
    term("1.5.5", "Identify the front at F.", ["cold front"], ["Triangles on the line.", "It moves with the low."]),
    term("1.5.6", "What type of rainfall is associated with the system at F?", ["frontal", "frontal rainfall", "cyclonic", "cyclonic rainfall"],
         ["F is a front.", "Look at the sketches above the map."]),
    stmt("1.5.7", "Explain the formation of the type of rainfall mentioned in QUESTION 1.5.6.", 4,
         ["Warm air is forced to rise over the cold air.", "The warm air rises and cools.", "The water vapour condenses and clouds form."],
         ["Cold air rises over warm air and heats up.", "Mountains force the air to rise.", "The sun heats the ground and the air rises."],
         ["At a front, warm and cold air meet.", "Which one rises?"], 2, after=["1.5.6"]),
    sort("1.5.8", "Differentiate between convectional and orographic rainfall.", ["Convectional rainfall", "Orographic rainfall"],
         [("The Earth's surface is heated by the sun and the warm air rises by convection", 0),
          ("Water vapour condenses into towering cumulonimbus clouds with short heavy showers", 0),
          ("Mountains act as barriers that force moist air to rise", 1),
          ("The moist air moving upslope cools and condenses, producing rain on the windward side", 1)],
         ["Convection: heat from below.", "Orographic: mountains."])]

# ---- QUESTION 2: GEOMORPHOLOGY, the question paper pages 8-13 and the memo pages 5-7 ----
q21 = [
    two("2.1.1", "An upfold", "Syncline", "Anticline", 1, ["The fold arches up.", "An 'A' shape."]),
    two("2.1.2", "A downfold", "Syncline", "Anticline", 0, ["The fold dips down.", "Not the anticline."]),
    two("2.1.3", "A pointed or peaked fold", "Chevron fold", "Overturned fold", 0, ["Sharp points like a zigzag.", "Like a sergeant's stripes."]),
    two("2.1.4", "A fold with equal sides", "Symmetrical fold", "Asymmetrical fold", 0, ["Both sides the same.", "Mirror image."]),
    two("2.1.5", "The sloping beds on either side of an axial plane", "Limbs", "Crests", 0, ["Like arms on either side.", "The crest is the top."]),
    two("2.1.6", "A tilted or bent-over fold", "Symmetrical fold", "Asymmetrical fold", 1, ["The sides are not equal.", "Leaning to one side."]),
    two("2.1.7", "An overturned fold that has flopped over", "Isoclinal fold", "Recumbent fold", 1, ["It lies almost flat.", "Recumbent means lying down."]),
    two("2.1.8", "A very tight fold in which the limbs are parallel to one another", "Isoclinal fold", "Recumbent fold", 0,
        ["Iso means equal.", "The limbs run side by side."])]
q22 = [
    mcq("2.2.1", "The very thin, solid, brittle top layer of the Earth, indicated as number 1, is known as the …",
        ["inner core.", "outer core.", "mantle.", "crust."], 3, ["It is the outermost layer.", "We live on it."], marks=1),
    mcq("2.2.2", "The inner core is labelled by the number …", ["1", "2", "3", "4"], 3, ["It is at the centre.", "The innermost label."], marks=1),
    mcq("2.2.3", "The outer core is labelled by the number …", ["1", "2", "3", "4"], 2, ["Just outside the centre.", "Between the mantle and "
                                                                                                                  "the inner core."], marks=1),
    mcq("2.2.4", "The inner core of the Earth is made up of …", ["liquid iron and nickel.", "solid iron and nickel.",
        "liquid silicon and aluminium.", "solid silicon and aluminium."], 1, ["Huge pressure keeps it solid.", "Iron and nickel."], marks=1),
    mcq("2.2.5", "The layer of the Earth that is mined for minerals and oil.", ["Inner core", "Outer core", "Mantle", "Crust"], 3,
        ["Mines reach only a few kilometres down.", "The top layer."], marks=1),
    mcq("2.2.6", "The layer responsible for the Earth's magnetic field, labelled as 4, is the …", ["inner core.", "outer core.", "mantle.",
        "crust."], 0, ["Which layer is labelled 4?", "The centre of the Earth."], marks=1),
    mcq("2.2.7", "The mantle, layer 2, consists of …", ["magma.", "lava.", "water.", "solid rock."], 0,
        ["Molten rock below the surface.", "Lava is molten rock above the surface."], marks=1)]
q23 = [
    stmt("2.3.1", "Define the concept plate tectonics.", 2,
         ["The theory that the Earth's surface consists of several plates that are slowly moving.",
          "The theory that the crust is broken into plates that move on the mantle."],
         ["The theory that the continents have never moved.", "The study of volcanoes only.", "The theory that the Earth is flat.",
          "The study of weather fronts."],
         ["Plates are pieces of the crust.", "Do they move?"], 2),
    mcq("2.3.2(a)", "Plates push together at a (divergent/convergent/transform fault) boundary.", BOUND, 1,
        ["Converge means come together.", "Look at the arrows pointing at each other."], marks=1),
    mcq("2.3.2(b)", "At a (divergent/convergent/transform fault) boundary, plates slide past each other.", BOUND, 2,
        ["Sideways movement.", "Look at the right of the sketch."], marks=1),
    mcq("2.3.2(c)", "Plates move apart at a (divergent/convergent/transform fault) boundary.", BOUND, 0,
        ["Diverge means move apart.", "The mid-Atlantic ridge."], marks=1),
    term("2.3.3", "Name ONE landform formed when convergence occurs between two oceanic plates.", ["island arcs", "island arc", "volcanic islands",
                                                                                                    "volcanic island"],
         ["One plate sinks and volcanoes rise from the sea.", "Japan is one."]),
    term("2.3.4", "Name ONE landform formed when convergence occurs between two plates.", ["fold mountains", "fold mountain"],
         ["The crust crumples upward.", "The Himalayas."]),
    sort("2.3.5", "Distinguish between mid-oceanic ridges and oceanic trenches by referring to the different ways they form.",
         ["Mid-oceanic ridge", "Oceanic trench"],
         [("Forms where two oceanic plates move apart", 0), ("Magma rises and solidifies to create new crust", 0),
          ("Forms where a denser oceanic plate collides with a less dense plate", 1), ("The denser oceanic plate slides beneath the other", 1)],
         ["Ridges are at divergent boundaries.", "Trenches are at convergent boundaries."]),
    stmt("2.3.6", "Explain what causes tectonic plates to move.", 4,
         ["The plates float on the molten mantle.", "Convection currents in the mantle push the plates.",
          "The crust is broken into large pieces that constantly move in different directions.",
          "The plates are not fixed and slide around on the molten outer mantle."],
         ["The wind pushes the plates.", "Ocean tides move the plates.", "The moon pulls the plates apart."],
         ["What lies under the plates?", "Heat moves the molten mantle."], 2)]
EQ = ("Measuring 5.3; today's earthquake can be described as 'Moderate'. It can cause damage to buildings with poor construction, and "
      "everybody will feel its tremors. On a global scale, approximately 500-1500 of these earthquakes occur per year. Only earthquakes that "
      "reach above 7 cause great damage to buildings and are classified as Major (around 7) and Great (above 8).")
q24 = [
    term("2.4.1", "What instrument is used to measure the magnitude of an earthquake?", ["seismometer", "seismograph"],
         ["Seismic means earthquake.", "It records shaking."]),
    stmt("2.4.2", "What is the epicentre of an earthquake?", 2,
         ["The place on the surface directly above the focus.", "The point on the Earth's surface above where the earthquake starts."],
         ["The point deep underground where the earthquake starts.", "The place furthest from the earthquake.", "The top of a volcano.",
          "The boundary between two plates."],
         ["Epi means above.", "Above the focus."], 2),
    term("2.4.3", "Where was the epicentre of this earthquake?", ["orkney", "klerksdorp"], ["Read the first line of the extract.",
                                                                                             "Look at the map."]),
    pick("2.4.4", "Quote from the extract the sentence which described the earthquake as only moderate.", sentences(EQ), [0, 1],
         ["Read the third paragraph.", "Moderate damage."], 1),
    stmt("2.4.5", "Explain why mining activity can be the possible cause of this earthquake.", 2,
         ["Underground excavation can create stresses that cause earthquakes.",
          "Deep-level mining removes rock, which weakens the crust and triggers tremors."],
         ["Mining cools the Earth's core.", "Mining adds water to the plates.", "Mines are always built on plate boundaries.",
          "Mining increases rainfall."],
         ["Orkney has many gold mines.", "What does digging deep do to rock?"], 2),
    stmt("2.4.6", "In a paragraph of approximately EIGHT lines, explain the effects of earthquakes and suggest ways in which the impact of "
         "earthquakes can be reduced.", 8,
         ["Earthquakes lead to injuries and deaths.", "Earthquakes destroy infrastructure.", "Build earthquake-resistant buildings.",
          "Identify high-risk areas and active fault zones.", "Make sure emergency services are in place.", "Educate people about the dangers."],
         ["Build houses on fault lines.", "Ignore warning systems."], ["Effects first, then ways to reduce them.", "People, buildings, planning."], 2)]
q25 = [
    stmt("2.5.1", "Define the term volcano.", 2,
         ["An opening in the Earth's surface from which magma erupts as lava.", "A vent in the crust through which molten rock, ash and gas erupt."],
         ["A mountain made of folded rock.", "A deep trench in the ocean.", "A crack where plates slide past each other.",
          "A hill made of ice."],
         ["Molten rock comes out.", "An opening."], 2),
    term("2.5.2", "Identify the type of volcano illustrated in the sketch.", ["stratovolcano", "composite", "composite volcano", "strato volcano"],
         ["Look for layers of lava and ash.", "It has a main vent and a secondary cone."]),
    stmt("2.5.3", "Justify your answer in QUESTION 2.5.2.", 2,
         ["It has alternating layers of ash and lava.", "It is a very tall volcano with steep slopes."],
         ["It is wide and flat with gentle slopes.", "It has no crater.", "It is made only of ash.", "It erupts only under water."],
         ["Read the labels on the sketch.", "Layers and steep slopes."], 2, after=["2.5.2"]),
    sort("2.5.4", "Differentiate between the vent and the crater of a volcano.", ["Vent", "Crater"],
         [("The opening or mouth through which magma rises", 0), ("The pipe from the magma chamber to the surface", 0),
          ("The depression (hollow) at the top of the volcano", 1), ("The bowl-shaped hollow around the top of the vent", 1)],
         ["The vent is the pipe.", "The crater is the hollow at the top."]),
    stmt("2.5.5", "Explain the positive economic impact of volcanoes on a country.", 6,
         ["Volcanic ash acts as a fertiliser for the soil.", "Volcanic regions become tourist attractions.",
          "Hot underground water is used for heating and electricity generation.", "Volcanic rocks are mined for building materials and minerals."],
         ["Volcanoes destroy all farmland for ever.", "Volcanoes stop all tourism.", "Volcanoes make electricity more expensive."],
         ["Soil, tourism, energy.", "How can a country earn from a volcano?"], 2)]

# ---- SECTION B, QUESTION 3: GEOGRAPHICAL SKILLS AND TECHNIQUES (the parts that do not read the maps), pages 14-17 and the memo pages 8-9 ----
q31 = [
    mcq("3.1.1", "The map code 2931CA VERULAM indicates that the town lies on the …", ["29° E longitude and 31° N latitude",
        "29° S longitude and 31° E latitude", "29° E latitude and 31° N longitude", "29° S latitude and 31° E longitude"], 3,
        ["The first two digits are the latitude.", "South Africa is south of the equator and east of Greenwich."], marks=1),
    mcq("3.1.2", "The map scale of the topographical map (1 : 50 000) is … than the map scale of the orthophoto (1 : 10 000).",
        ["5 times larger", "5 times smaller", "20 times larger", "20 times smaller"], 1,
        ["50 000 ÷ 10 000.", "A bigger number on the right is a smaller scale."], marks=1),
    mcq("3.1.3", "The contour interval on the orthophoto is …", ["5 m.", "20 m.", "25 m.", "10 m."], 0,
        ["Orthophoto maps use a small interval.", "Topographical maps use 20 m."], marks=1),
    stmt("3.1.4", "What is the meaning of the topographical map scale 1 : 50 000?", 1,
         ["1 cm on the map represents 50 000 cm in reality.", "1 unit on the map represents 50 000 of the same units on the ground."],
         ["1 cm on the map represents 50 000 km in reality.", "The map is 50 000 times bigger than the area.", "50 000 maps cover the country."],
         ["The same unit on both sides.", "Map to ground."], 1)]
q32 = [
    stmt("3.2.1", "Give ONE similarity between an orthophoto and a topographical map.", 1,
         ["Both show the same area of land.", "Both have contour lines.", "Both have ratio and linear scales."],
         ["Both are photographs.", "Both use the same scale.", "Both show only roads."], ["What do both maps include?", "Area, contours, scales."], 1),
    stmt("3.2.5", "Name ONE advantage of using an orthophoto map rather than a topographical map.", 1,
         ["It is cheaper to produce.", "It is more accurate and readily updated.", "Its larger scale shows more detail."],
         ["It covers a much larger area.", "It has no contour lines.", "It shows no buildings."], ["An orthophoto is a photograph.", "Detail and cost."],
         1),
    term("3.2.9", "What type of road is the N17?", ["national road", "national route", "national"], ["N stands for …", "Not a regional road."])]
q33 = [
    stmt("3.3.1", "Define the concept Geographical Information System.", 2,
         ["A system for collecting, storing and displaying spatial data.", "A computer-based system that captures, stores, analyses and displays "
                                                                           "geographical data."],
         ["A system for drawing cartoons.", "A satellite that predicts the weather.", "A paper map of the world.", "A system for paying taxes."],
         ["Spatial data.", "Collect, store, display."], 2),
    stmt("3.3.2", "Explain why people are important in the GIS process.", 2,
         ["People collect, manage, analyse and visualise spatial data to support decisions.",
          "People operate the system and interpret its results."],
         ["People are not needed once the computer is on.", "People only provide electricity.", "People replace the software.",
          "People make the hardware heavier."],
         ["Who runs the system?", "Who uses the results?"], 2),
    term("3.3.3", "Name ONE hardware device that can capture information into the system.", ["scanner", "keyboard", "digitiser", "gps"],
         ["It puts data into a computer.", "A scanner is one."]),
    term("3.3.4", "What is collecting spatial data about an object or event and taking an image of it from a distance called?",
         ["remote sensing"], ["From a distance.", "Satellites do it."]),
    stmt("3.3.5", "Explain the importance of using GIS in today's fast-changing world.", 2,
         ["Computers are faster, cheaper and more efficient.", "More information is coming into the world.",
          "The world's problems exist in a geographical context.", "GIS can be used in daily life, e.g. choosing a nearby school."],
         ["GIS slows down decision-making.", "GIS works only without computers.", "GIS cannot handle new information."],
         ["Speed and information.", "Everyday decisions."], 2)]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "The water cycle", "marks": 7,
     "lead": "Refer to the sketch below showing the water cycle. Choose from EVAPORATION, CONDENSATION or PRECIPITATION to match the descriptions.",
     "figure": P.fig("1.1", "The water cycle: evaporation from the sea, condensation into clouds, precipitation over mountains, and collection "
                            "in rivers and lakes."), "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Heating of the atmosphere", "marks": 8,
     "lead": "Choose the correct word(s) from those given in brackets.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Layers of the atmosphere", "marks": 15,
     "lead": "Refer to the graph below, showing how temperature changes with height between the different layers of the atmosphere.",
     "figure": P.fig("1.3", "Temperature (°C) against altitude (km): falling through the troposphere to about −60 °C at the tropopause near "
                            "15 km, rising through the stratosphere (with the ozone layer) to about 0 °C at 50 km, falling through the "
                            "mesosphere to about −90 °C at 80 km, then rising through the thermosphere."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Global warming", "marks": 15,
     "lead": "Refer to the extract on global warming.\nDUE TO CLIMATE CHANGE THE COUNTRY'S RAINFALL PATTERNS HAVE BECOME MORE ERRATIC, LEADING "
             "TO FLASH FLOODS AND WATER SCARCITY IN SOME AREAS\n" + GW + " [Adapted from www.greenpeace.org]", "items": q14},
    {"id": "1.5", "title": "Question 1.5", "kind": "Rainfall and synoptic maps", "marks": 15,
     "lead": "Refer to the sketches below on types of rainfall and the synoptic weather map.",
     "figure": P.fig("1.5", "Sketches of relief, frontal and convectional rainfall above a synoptic weather map of 2010-01-30: a high-pressure "
                            "cell A in the south-west (isobars 1008 to 1020 hPa rising inwards), station model D in the west, a cold front "
                            "F leading to a low G, a coastal low E, and a tropical cyclone Cathy in the east."), "items": q15},
    {"id": "2.1", "title": "Question 2.1", "kind": "Folding", "marks": 8,
     "lead": "Refer to the sketches below, which show different types of folding. Complete the statement with the correct option.",
     "figure": P.fig("2.1", "Six kinds of folds: symmetrical, asymmetrical, isoclinal, recumbent, chevron and overturned."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "The structure of the Earth", "marks": 7,
     "lead": "Various options are provided as possible answers to the following questions.",
     "figure": P.fig("2.2", "A cut-away of the Earth with four layers labelled 1 (the thin outer layer) to 4 (the centre)."), "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Plate tectonics", "marks": 15,
     "lead": "Study the sketch below of landforms associated with plate boundaries.",
     "figure": P.fig("2.3", "Plate boundaries: a convergence zone with a trench where oceanic crust sinks, a divergence zone at the mid-Atlantic "
                            "ridge, a convergence zone where continental crust buckles into mountains, and a transform zone where plates slide "
                            "past each other."), "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Earthquakes", "marks": 15,
     "lead": "Refer to the extract and a map of South Africa below based on an earthquake.\nEarthquake of 5.3 magnitude! (Amended to 5,5 by "
             "experts at a depth of 10 km)\nCentred in Orkney, 120 km south-west of Johannesburg! An area with many gold mines. At around "
             "13h15 South African gold miners with head offices in Johannesburg and Sandton advised that they had felt the earthquake at their "
             "head offices but have so far received no reports of damage from their mines.\nEarthquakes and deep-level mining do not bode "
             "well, and I hope that no mine workers will be injured.\n" + EQ + " Earthquakes of magnitude 8 release an equal amount of energy "
             "to 6 million tons of TNT.",
     "figure": P.fig("2.4", "A map of South Africa with circles centred on Klerksdorp, south-west of Johannesburg."), "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Volcanoes", "marks": 15, "lead": "Study the sketch below showing a cross-section through a volcano.",
     "figure": P.fig("2.5", "A cross-section of a volcano: an eruption cloud, the crater, a secondary cone, a lava flow, layers of lava and ash, "
                            "the main vent and the magma chamber."), "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Map skills", "marks": 4,
     "lead": "GENERAL INFORMATION ON VERULAM. Coordinates: 29°35'S; 31°0'E. The town of Verulam is 170 years old and located to the north of "
             "Durban. It has a population of over 60 000 people. The Hazelmere Dam, just a few kilometres north of Verulam, is the main source "
             "of water for the area. A 1 : 50 000 topographical map 2931CA VERULAM and a 1 : 10 000 orthophoto map 2931CA VERULAM are used in "
             "the exam room.", "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Map interpretation", "marks": 3, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Geographical information systems", "marks": 8, "lead": "Refer to the sketch below of GIS.",
     "figure": P.fig("3.3", "GIS at the centre of a ring: hardware, methods, software, data and people."), "items": q33}]

P.finish(missions,
         {"subject": "Geography", "title": "Geography P1", "sitting": "November 2024", "total_marks": 135, "time": "3 hours"},
         [P.flag_answers(),
          {"n": "3.1", "kind": "missing_resource", "detail": "SECTION B reads the 1 : 50 000 topographical map and the 1 : 10 000 orthophoto of "
                                                             "2931CA Verulam handed out in the exam room; they are not in the download. 3.1.5-3.1.7, "
                                                             "3.2.2-3.2.4 and 3.2.6-3.2.8 (15 marks) wait for the maps; the paper totals 135."},
          {"n": "2.1.5", "kind": "memo_issue", "detail": "2.1.5-2.1.8 print Z above Y, but the memo's letters (Y, Z, Z, Y) follow the Y-above-Z "
                                                         "order of 2.1.1-2.1.4, giving 'crests', 'symmetrical', 'isoclinal' and 'recumbent' as "
                                                         "printed. Read by position, the memo means limbs, asymmetrical, recumbent and "
                                                         "isoclinal, the right folds; they play as the named choices."},
          {"n": "3.1.3", "kind": "memo_issue", "detail": "The memo gives C (25 m) for the orthophoto's contour interval; 1 : 10 000 orthophoto "
                                                         "maps use a 5 m interval (option A, printed '5 tm'), as Grade 11's 3.1.2 marks. The "
                                                         "right option is 5 m. For Murci to confirm."},
          {"n": "2.2.6", "kind": "low_confidence", "detail": "The memo accepts A/D for 'the layer responsible for the Earth's magnetic field, "
                                                             "labelled as 4'. Layer 4 is the inner core (A); D (crust) cannot be layer 4. The "
                                                             "right option is A. (The field is generated in the liquid outer core; the stem "
                                                             "names layer 4.)"}],
         {"1": 60, "2": 60, "3": 15}, 135, {"1.5.3": ["1.5.2"], "1.5.7": ["1.5.6"], "2.5.3": ["2.5.2"]},
         "Section A whole and the parts of Section B that do not read the maps")
