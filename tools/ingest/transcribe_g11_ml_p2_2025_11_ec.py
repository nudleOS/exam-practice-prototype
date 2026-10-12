"""Grade 11 Mathematical Literacy P2 November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 4, 100 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks, answers and the memo's
working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za,
2025 November Grade 11, the question paper zip (English PDF 'QPAPER (2)', 10 pages, text layer), its ADDENDUM (English, 4 pages:
ANNEXURE A, a map of Pilgrim's Rest, and B, a map of Mpumalanga, both landscape pages; C, the Pizza Den's table) and the memo
(English, 10 pages, text layer).

  python tools/ingest/transcribe_g11_ml_p2_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ml-p2-2025-11-ec/MATHS LIT GRADE 11 NOV 2025 QPAPER (2)_watermark.pdf" "uploads/provincial/g11-ml-p2-2025-11-ec/MATHS LIT P2 GRADE 11 NOV 2025 MEMO ENG_watermark.pdf" --id g11-ml-p2-2025-11-ec --from-json --answer-book "uploads/provincial/g11-ml-p2-2025-11-ec/MATHS LIT P2 GR11 NOV25 ADDENDUM ENGLISH FINAL (1)_watermark.pdf"

The Mathematical Literacy rulings, as in transcribe_ml_p2_2025_11.py: a calculation, a 'verify' and a 'show that' -> four whole
workings (provincial.work), the memo's first method and three real errors; a value read off -> num, term or an MCQ of answers; a
definition or a reason -> statements. A length the memo MEASURES on the printed annexure (2.1.3, and the bar scale in 2.1.4) cannot be
measured on a phone: the figure caption gives it, as Grade 12's ML P2 Nov 2025 2.2.4 does. Figure boxes are in PDF points of each
page (the annexures A and B are landscape pages), each 1% of the page inside its neighbours (ingest pads every crop by 1%); a source line the pad still reaches is blanked."""
from provincial import Paper

LAND = {"source": "answer_book", "size": [842.04, 595.32]}
P = Paper("g11-ml-p2-2025-11-ec", 595.44, 841.68, {
    "1.2": [4, 172.0, 293.0, 462.0, 560.0, {"blank": [[0, 0.6719, 1, 0.7]]}], "1.3": [5, 186.0, 99.0, 435.0, 224.0, {"blank": [[0, 0.2715, 1, 0.29]]}], "1.4": [5, 106.0, 405.0, 517.0, 564.0],
    "3.1": [7, 77.0, 172.0, 517.0, 343.0, {"blank": [[0, 0.4123, 1, 0.43]]}], "4.1": [9, 108.0, 164.0, 494.0, 378.0, {"blank": [[0.33, 0.4539, 1, 0.47]]}], "4.2": [10, 94.0, 147.0, 490.0, 307.0, {"blank": [[0.38, 0.3707, 1, 0.39]]}],
    "2.1": [2, 72.0, 147.0, 632.0, 494.5, LAND], "2.2": [3, 60.5, 116.0, 802.0, 501.0, LAND],
    "4.3": [4, 58.0, 156.0, 582.0, 488.5, {"source": "answer_book", "size": [595.32, 842.04], "blank": [[0.75, 0.5835, 1, 0.6]]}]}, start=5)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term

RECIPE = ("Andrea bakes wedding cakes. The most popular cake she bakes, is a carrot cake with cream cheese frosting.\n"
          "INGREDIENTS: 350 g self-raising flour; 325 g dark soft brown sugar; 1½ teaspoons fine sea salt; 2 teaspoons cinnamon; 200 ml olive "
          "oil; 1 teaspoon vanilla extract; 4 large eggs; 250 g grated peeled carrots; 75 g chopped pecan nuts; 4 tablespoons milk.\n"
          "FOR CREAMY FROSTING: 10 ounces cream cheese; 1¼ cups (140 g) powdered sugar; ¾ cup (80 ml) cold heavy cream; ½ cup salted butter.\n"
          "METHOD: 1. Preheat the oven to 356 ℉. 2. Grease and line the bottom and sides of two round cake pans with a double layer of "
          "greaseproof paper. 3. Mix the flour, salt, sugar, cinnamon, chopped pecan nuts and grated carrots in a large bowl. 4. Beat together "
          "the eggs, olive oil, vanilla extract and milk in a large jug and add to flour mixture. Mix well. 5. Divide the cake batter between "
          "the prepared cake pans. Bake for 35–45 minutes until a skewer comes out clean. 6. Cool the cake layers in the pans for 15 minutes, "
          "then carefully turn the cake layers out onto cooling racks.\n"
          "CREAM CHEESE FROSTING: 1. Once the cake layers are completely cooled off, mix the cream cheese and butter in a blender for 1 and a "
          "half minutes. 2. Add powdered sugar until frosting is creamy. Whip cold heavy cream into the mixture for 3 minutes until light and "
          "fluffy. 3. Cover the cake in frosting – this will take up to 15 minutes.\n"
          "BAKING CONVERSIONS: 1 cup = 250 ml; 1 tablespoon = 15 ml; 1 teaspoon = 5 ml")

# ---- QUESTION 1, the question paper pages 3-5 and the memo pages 3-4 ----
q11 = [
    work("1.1.1", "Calculate the time (in minutes) to cover the cake with the cream cheese frosting.", 2, [
        "Total time = 1,5 min + 3 min + 15 min\n= 19,5 minutes",      # the memo
        "Total time = 1 min + 3 min + 15 min\n= 19 minutes",          # 1 and a half read as 1
        "Total time = 35 min + 15 min + 15 min\n= 65 minutes",        # the baking and the cooling
        "Total time = 1,5 min + 3 min\n= 4,5 minutes"],               # the covering left out
        ["Add every timed step of the CREAM CHEESE FROSTING.", "Three steps: blend, whip, cover."]),
    work("1.1.2", "Determine the amount of cream cheese needed in the recipe in kilograms. NOTE: 1 kg = 35,274 ounces", 2, [
        "Cream cheese = {10}/{35,274}\n= 0,28 kg",     # the memo
        "Cream cheese = 10 × 35,274\n= 352,74 kg",     # multiplied
        "Cream cheese = {35,274}/{10}\n= 3,53 kg",     # upside down
        "Cream cheese = {10}/{1 000}\n= 0,01 kg"],     # ounces taken as grams
        ["The recipe uses 10 ounces.", "35,274 ounces make 1 kg: divide or multiply?"]),
    work("1.1.3", "Convert the salt needed in the recipe to millilitres.", 2, [
        "Salt = 1½ × 5 ml\n= 7,5 ml",       # the memo
        "Salt = 1½ × 15 ml\n= 22,5 ml",     # a tablespoon
        "Salt = 1½ × 250 ml\n= 375 ml",     # a cup
        "Salt = 1 × 5 ml\n= 5 ml"],         # the half left out
        ["The salt is 1½ teaspoons.", "Use BAKING CONVERSIONS."]),
    work("1.1.4", "Andrea's oven does not calibrate in degrees Fahrenheit. Determine the temperature, in ℃, at which Andrea should set her oven. "
         "You may use the following formula: ℃ = 5/9 × (℉ − 32°)", 2, [
        "℃ = {5}/{9} × (356 − 32)\n= 180 ℃",       # the memo
        "℃ = {5}/{9} × 356 − 32\n= 165,8 ℃",       # the bracket ignored
        "℃ = {9}/{5} × (356 − 32)\n= 583,2 ℃",     # the fraction upside down
        "℃ = {5}/{9} × (356 + 32)\n= 215,6 ℃"],    # 32 added
        ["The oven is set to 356 ℉ in METHOD step 1.", "Work the bracket first."])]
q12 = [
    stmt("1.2.1", "Define the term capacity.", 2, ["Capacity is the maximum amount of liquid a container can hold."],
         ["Capacity is the mass of a container.", "Capacity is the space a container takes up on a shelf.",
          "Capacity is the height of a container.", "Capacity is the amount of liquid poured out of a container."],
         ["Think of a jug filled to the top.", "How much can it hold?"], 2),
    answer("1.2.2", "Hence, determine the capacity of the measuring cup.", 2, ["500 ml", "450 ml", "50 ml", "1 000 ml"],
           ["Read the highest mark on the scale.", "The top mark is the most it measures."])]
q13 = [
    work("1.3.1", "Calculate the circumference of pan Y in squared inches (in.²). You may use the following formula: Circumference of a circle = "
         "π × diameter, where π = 3,142", 2, [
        "Circumference = 3,142 × 13\n= 40,846 in.",      # the memo, in inches
        "Circumference = 3,142 × 6,5\n= 20,423 in.",     # the radius
        "Circumference = 3,142 × 13²\n= 530,998 in.",    # squared, as for an area
        "Circumference = 3,142 × 16\n= 50,272 in."],     # pan Z
        ["Pan Y's diameter is 13 inches.", "π × diameter."]),
    work("1.3.2", "Write the diameter of pan Z to the diameter of pan X as a simplified ratio.", 2, [
        "Z : X\n= 16 : 8\n= 2 : 1",       # the memo
        "X : Z\n= 8 : 16\n= 1 : 2",       # swapped
        "Z : X\n= 16 : 8\n= 8 : 4",       # not fully simplified
        "Z : W\n= 16 : 5\n= 3,2 : 1"],    # pan W
        ["Z first, then X.", "Divide both by their highest common factor."])]
q14 = [
    answer("1.4.1", "Identify the clinic on the map.", 2, ["Oribi Animal Clinic", "Dignity4You", "Apex School of Driving",
                                                          "Sunshine Bay Beach Club"], ["Look for the word clinic.", "Near Jeffreys Bay."]),
    answer("1.4.2", "In which general direction will Andrea be travelling to Jeffreys Bay?", 2, ["South-east", "North-east", "North-west",
                                                                                               "South-west"],
           ["Humansdorp is top left, Jeffreys Bay to the right and a little lower.", "Use the compass: N up, E right."]),
    work("1.4.3", "Convert Andrea's travelling distance to metres.", 2, [
        "Distance = 21,1 km × 1 000\n= 21 100 m",     # the memo
        "Distance = 21,1 km × 100\n= 2 110 m",        # 100 m in a km
        "Distance = 21,1 km ÷ 1 000\n= 0,0211 m",     # divided
        "Distance = 26 km × 1 000\n= 26 000 m"],      # the minutes read as km
        ["The route box says 26 min and 21,1 km.", "1 km = 1 000 m."]),
    work("1.4.4", "Determine the time that Andrea will arrive in Jeffreys Bay if she leaves her house at 10:15.", 2, [
        "Arrival = 10:15 + 00:26\n= 10:41",    # the memo
        "Arrival = 10:15 + 00:21\n= 10:36",    # the 21,1 km read as minutes
        "Arrival = 10:15 − 00:26\n= 09:49",    # subtracted
        "Arrival = 10:15 + 01:26\n= 11:41"],   # an hour added
        ["The trip takes 26 minutes.", "Add it to 10:15."])]

# ---- QUESTION 2, the question paper page 6, the memo pages 5-6 and the ADDENDUM pages 2-3 (ANNEXURES A and B) ----
S = "Scale: 2,6 cm = "
T4 = "Time = {276 km}/{80 km/h}\n= 3,45 hours\n"
q21 = [
    answer("2.1.1", "Identify the tourist attraction found in block D5.", 2, ["Rober's Grave", "Store Museum", "Town Hall", "House museum"],
           ["Column D, row 5.", "Find the star in that block."]),
    answer("2.1.2", "Determine the probability of finding a railway on this part of the map.", 2, ["0", "1", "0,5", "1/35"],
           ["Is there a railway anywhere on the map?", "An impossible event has probability …"]),
    num("2.1.3", "Measure the distance between the Store Museum and the Town Hall in centimetres. (The figure's caption gives the printed "
        "lengths.)", 6.4, 0.2, "cm", ["Read the printed distance in the caption.", "From the Store Museum's star to the Town Hall's."], marks=2),
    work("2.1.4", "Hence, calculate the actual distance (in kilometres) between the Store Museum and the Town Hall, using the bar scale.", 5, [
        S + "600 m\n1 cm = {600}/{2,6} = 230,77 m\nDistance = 6,4 × 230,77\n= 1 476,92 m\n= 1,48 km",             # the memo
        S + "600 m\n1 cm = {2,6}/{600} = 0,0043 m\nDistance = 6,4 × 0,0043\n= 0,028 m\n= 0,000028 km",           # upside down
        S + "200 m\n1 cm = {200}/{2,6} = 76,92 m\nDistance = 6,4 × 76,92\n= 492,31 m\n= 0,49 km",                # the bar's 200 read as its end
        S + "600 m\n1 cm = {600}/{2,6} = 230,77 m\nDistance = 6,4 × 230,77\n= 1 476,92 m\n= 14,77 km"],          # ÷ 100, not ÷ 1 000
        ["How many metres does 1 cm stand for?", "Then multiply by 6,4 cm and change m to km."], after=["2.1.3"]),
    work("2.1.5", "Pilgrim's Rest has approximately 1 721 residents and occupies an area of 25,40 km². Determine the number of people per square "
         "kilometre (km²) residing in Pilgrim's Rest.", 2, [
        "People per km² = {1 721}/{25,40}\n= 67,76 ≈ 68 people",      # the memo
        "People per km² = 1 721 × 25,40\n= 43 713,4 ≈ 43 713 people",  # multiplied
        "People per km² = {25,40}/{1 721}\n= 0,015 ≈ 0 people",       # upside down
        "People per km² = {1 721}/{254}\n= 6,78 ≈ 7 people"],         # 25,40 read as 254
        ["People ÷ area.", "Round to whole people."])]
q22 = [
    term("2.2.1", "Name ONE neighbouring country bordering Mpumalanga.", ["Mozambique", "Swaziland", "Eswatini"],
         ["Look at the edge of the map.", "Countries, not provinces."], marks=2),
    num("2.2.2", "Identify the number of national roads found on this map.", 6, 0, "", ["The key shows the national-road sign.",
                                                                                       "Count the N-numbers: N1, N11, …"], marks=2),
    work("2.2.3", "The actual distance between Lydenburg and Standerton is 276 km and it measures 8,3 cm on the map. Hence, determine the scale "
         "of this map.", 3, [
        "276 km = 27 600 000 cm\nScale = 8,3 : 27 600 000\n= 1 : 3 325 301,2",        # the memo
        "276 km = 276 000 cm\nScale = 8,3 : 276 000\n= 1 : 33 253",                    # km to cm by 1 000
        "276 km = 27 600 000 cm\nScale = 27 600 000 : 8,3\n= 3 325 301,2 : 1",         # the ratio upside down
        "276 km = 27 600 000 cm\nScale = 8,3 : 27 600 000\n= 1 : 229 080 000"],        # multiplied by 8,3
        ["Change 276 km to cm.", "Divide both sides by 8,3 to get 1 : …"]),
    work("2.2.4", "Siphokazi claims that if she travels at an average speed of 80 km/h and leaves her home at 12:45, she will arrive in "
         "Standerton at 16:05, without any stops. Verify, with the necessary calculations, whether her claim is VALID. You may use the "
         "following formula: Speed = Distance ÷ Time", 7, [
        T4 + "0,45 × 60 = 27 minutes\nTravel time = 3 h 27 min\nArrival = 12:45 + 03:27\n= 16:12\n16:12, not 16:05: her claim is NOT VALID",  # the memo
        T4 + "3,45 hours = 3 h 45 min\nTravel time = 3 h 45 min\nArrival = 12:45 + 03:45\n= 16:30\n16:30, not 16:05: her claim is NOT VALID",  # read as 3 h 45
        "Time = {80 km/h}/{276 km}\n= 0,29 hours\n0,29 × 60 = 17,39 minutes\nTravel time = 0 h 17 min\nArrival = 12:45 + 00:17\n= 13:02\n"
        "13:02, not 16:05: her claim is NOT VALID",                                                                                    # upside down
        "Time = {8,3 km}/{80 km/h}\n= 0,104 hours\n0,104 × 60 = 6,23 minutes\nTravel time = 0 h 6 min\nArrival = 12:45 + 00:06\n= 12:51\n"
        "12:51, not 16:05: her claim is NOT VALID"],                                                                                   # the map's 8,3 cm
        ["Time = distance ÷ speed: 276 km at 80 km/h.", "Change the decimal part of the hours to minutes before adding."])]

# ---- QUESTION 3, the question paper pages 7-8 and the memo pages 7-8 ----
WH = "Width = 0,08 m × 1 000 = 80 mm\nHeight = 14,5 cm × 10 = 145 mm\n"
q31 = [
    work("3.1.1", "Determine the volume of the cylindrical-shaped container in cubic centimetres (cm³).", 3, [
        "Radius = 50 mm ÷ 10 = 5 cm\nVolume = 3,142 × 5² × 12\n= 942,6 cm³",        # the memo
        "Radius = 50 mm ÷ 10 = 5 cm\nVolume = 3,142 × 5 × 12\n= 188,52 cm³",        # the radius not squared
        "Radius = 50 mm\nVolume = 3,142 × 50² × 12\n= 94 260 cm³",                  # mm not changed to cm
        "Radius = 50 mm ÷ 10 = 5 cm\nVolume = 3,142 × 10² × 12\n= 3 770,4 cm³"],    # the diameter used
        ["The 50 mm runs from the centre to the edge: the radius.", "Change it to cm first."]),
    work("3.1.2", "Determine the total surface of the rectangular-shaped container that needs to be covered in petroleum-based plastic. Give your "
         "answer rounded to the nearest thousand square millimetres (mm²).", 6, [
        WH + "TSA = 2(150 × 80) + 2(150 × 145) + 2(145 × 80)\n= 24 000 + 43 500 + 23 200\n= 90 700 mm²\n≈ 91 000 mm²",           # the memo
        "Width = 0,08 m × 100 = 8 mm\nHeight = 14,5 cm × 10 = 145 mm\nTSA = 2(150 × 8) + 2(150 × 145) + 2(145 × 8)\n"
        "= 2 400 + 43 500 + 2 320\n= 48 220 mm²\n≈ 48 000 mm²",                                                                    # m to mm by 100
        WH + "TSA = (150 × 80) + (150 × 145) + (145 × 80)\n= 12 000 + 21 750 + 11 600\n= 45 350 mm²\n≈ 45 000 mm²",              # the 2s left out
        WH + "TSA = 2(150 × 80) + 2(150 × 145) + 2(145 × 80)\n= 24 000 + 43 500 + 23 200\n= 90 700 mm²\n≈ 90 000 mm²"],          # rounded down
        ["Change the width (m) and the height (cm) to mm.", "90 700 lies nearer to which thousand?"]),
    work("3.1.3", "The petroleum-based plastic that Wilmien will use to cover the containers is sold at R27,55/m². Calculate the cost to cover 50 "
         "of the rectangular-shaped containers with this plastic. NOTE: The petroleum-based plastic can only be bought in whole square metres "
         "(m²).", 4, [
        "Plastic = {91 000}/{1 000 000} = 0,091 m²\n0,091 × 50 = 4,55 m² ≈ 5 m²\nCost = 5 × R27,55\n= R137,75",          # the memo
        "Plastic = {91 000}/{1 000 000} = 0,091 m²\n0,091 × 50 = 4,55 m²\nCost = 4,55 × R27,55\n= R125,35",              # not whole m²
        "Plastic = {91 000}/{1 000} = 91 m²\n91 × 50 = 4 550 m²\nCost = 4 550 × R27,55\n= R125 352,50",                  # mm² to m² by 1 000
        "Plastic = {91 000}/{1 000 000} = 0,091 m² ≈ 1 m²\n1 × 50 = 50 m²\nCost = 50 × R27,55\n= R1 377,50"],          # rounded up per container
        ["1 m² = 1 000 000 mm².", "Buy whole square metres for all 50 together."], after=["3.1.2"]),
    work("3.1.4", "Wilmien realised that she cannot fill the containers to maximum capacity. Instead, she fills the containers with coffee beans "
         "to a height that is 7% less than the container height. Show that the height of the coffee beans in the cylindrical container is "
         "11,2 cm.", 3, [
        "7% of 12 cm = {7}/{100} × 12 = 0,84 cm\nHeight = 12 cm − 0,84 cm\n= 11,16 cm ≈ 11,2 cm",              # the memo
        "7% of 12 cm = {7}/{100} × 12 = 0,84 cm\nHeight = 12 cm + 0,84 cm\n= 12,84 cm ≈ 12,8 cm",              # added
        "7% of 12 cm = {12}/{7} = 1,71 cm\nHeight = 12 cm − 1,71 cm\n= 10,29 cm ≈ 10,3 cm",                    # divided by 7
        "7% of 14,5 cm = {7}/{100} × 14,5 = 1,015 cm\nHeight = 14,5 cm − 1,015 cm\n= 13,485 cm ≈ 13,5 cm"],     # the other container
        ["The cylinder is 12 cm high.", "Take 7% of 12 cm away."]),
    work("3.1.5", "A sales representative advised Wilmien that the volume of the most economical container should not exceed 1 200 cm³. Wilmien "
         "thus claim that the rectangular-shaped container would be the most economical. Verify, with the necessary calculations, whether "
         "Wilmien's claim is VALID.", 5, [
        "Cylinder: 942,6 cm³\nRectangle: 15 cm × 8 cm × 14,5 cm\n= 1 740 cm³\nMore than 1 200 cm³: her claim is NOT VALID",    # the memo
        "Cylinder: 942,6 cm³\nRectangle: 150 × 0,08 × 14,5\n= 174 cm³\nLess than 1 200 cm³: her claim is VALID",              # units mixed
        "Cylinder: 942,6 cm³\nRectangle: 15 cm × 8 cm\n= 120 cm³\nLess than 1 200 cm³: her claim is VALID",                   # the base only
        "Cylinder: 942,6 cm³\nRectangle: 15 cm × 80 cm × 14,5 cm\n= 17 400 cm³\nMore than 1 200 cm³: her claim is NOT VALID"],  # 0,08 m as 80 cm
        ["Change all three sides to cm.", "Compare the rectangular container's volume with 1 200 cm³."], after=["3.1.1"]),
    stmt("3.1.6", "Provide ONE reason why Wilmien would want to wrap the containers in petroleum-based plastic.", 2,
         ["To keep the coffee beans fresh.", "To protect the containers against breakage."],
         ["To make the containers heavier.", "To let air in to the coffee beans.", "To make the coffee beans cheaper to import."],
         ["Plastic keeps air and water out.", "What could damage a container?"], 2)]

# ---- QUESTION 4, the question paper pages 9-10, the memo pages 9-10 and the ADDENDUM page 4 (ANNEXURE C) ----
TM = "Time = 10:15 − 08:30 = 1 h 45 min\n45 ÷ 60 = 0,75 h, so 1,75 hours\nDistance = 1,4 × 1,75\n= 2,45 miles\n"
R21 = "Radius = 42 ÷ 2 = 21 cm\nArea = 3,142 × 21² = 1 385,622 cm²\n"
q41 = [
    work("4.1.1", "Determine the probability, as a percentage, that Wilmien will be selling her coffee beans to a store with an uneven number.",
         3, [
        "P = {7}/{11} × 100\n= 63,64%",     # the memo
        "P = {7}/{13} × 100\n= 53,85%",     # 13 stores counted
        "P = {4}/{11} × 100\n= 36,36%",     # the even numbers
        "P = {6}/{11} × 100\n= 54,55%"],    # one odd store missed
        ["List the numbered stores: 8 and 10 are not there.", "Uneven: 1, 3, 5 …"]),
    work("4.1.2", "Wilmien arrived at the mall to do her deliveries at 08:30 and she concluded her delivery at 10:15. Wilmien claimed that she "
         "walked at an average speed of 1,4 miles per hour and thus covered a travelling distance inside the mall of more than 4 km. Verify, "
         "with the necessary calculations, whether Wilmien's claim is VALID. NOTE: 1 mile = 1,60934 km. You may use the following formula: "
         "Distance = Speed × Time", 7, [
        TM + "= 2,45 × 1,60934 = 3,94 km\nLess than 4 km: her claim is NOT VALID",                                                  # the memo
        "Time = 10:15 − 08:30 = 1 h 45 min\n1 h 45 min = 1,45 hours\nDistance = 1,4 × 1,45\n= 2,03 miles\n= 2,03 × 1,60934 = 3,27 km\n"
        "Less than 4 km: her claim is NOT VALID",                                                                                  # 1 h 45 as 1,45 h
        TM + "= {2,45}/{1,60934} = 1,52 km\nLess than 4 km: her claim is NOT VALID",                                               # divided
        "Time = 10:15 − 08:30 = 2 h 15 min\n15 ÷ 60 = 0,25 h, so 2,25 hours\nDistance = 1,4 × 2,25\n= 3,15 miles\n= 3,15 × 1,60934 = "
        "5,07 km\nMore than 4 km: her claim is VALID"],                                                                            # the minutes not borrowed
        ["How long was she in the mall, in hours?", "Miles × 1,60934 gives km."])]
q42 = [
    work("4.2.1", "Determine the area of the pizza box, rounded to the nearest ten square centimetres (cm²). You may use the following formula: "
         "Area of a square = side × side", 3, [
        "Area = 45 cm × 45 cm\n= 2 025 cm²\n≈ 2 030 cm²",     # the memo
        "Area = 45 cm × 45 cm\n= 2 025 cm²\n≈ 2 020 cm²",     # rounded down
        "Area = 42 cm × 42 cm\n= 1 764 cm²\n≈ 1 760 cm²",     # the pizza's diameter
        "Area = 45 cm × 4\n= 180 cm²\n≈ 180 cm²"],            # the perimeter
        ["The box is 45 cm × 45 cm.", "2 025 is halfway between two tens: round up."]),
    work("4.2.2", "Determine the value of D.", 3, [
        "2D = 45 cm − 42 cm = 3 cm\nD = {3 cm}/{2}\n= 1,5 cm",       # the memo
        "2D = 45 cm − 42 cm = 3 cm\nD = 3 cm × 2\n= 6 cm",           # multiplied
        "2D = 45 cm + 42 cm = 87 cm\nD = {87 cm}/{2}\n= 43,5 cm",    # added
        "2D = 45 cm − 21 cm = 24 cm\nD = {24 cm}/{2}\n= 12 cm"],     # the radius
        ["The box's side = pizza + a gap D on each side.", "Two gaps share 45 − 42."]),
    work("4.2.3", "Calculate the area of one slice of the pizza if it is cut in eight equal slices as illustrated in the picture above. You may "
         "use the following formula: Area of a circle = π × radius², where π = 3,142", 4, [
        R21 + "One slice = {1 385,622}/{8}\n= 173,20 cm²",                                                    # the memo
        "Radius = 42 cm\nArea = 3,142 × 42² = 5 542,488 cm²\nOne slice = {5 542,488}/{8}\n= 692,81 cm²",       # the diameter as the radius
        R21 + "One slice = {1 385,622}/{6}\n= 230,94 cm²",                                                    # six slices
        "Radius = 42 ÷ 2 = 21 cm\nArea = 3,142 × 21 × 2 = 131,964 cm²\nOne slice = {131,964}/{8}\n= 16,50 cm²"],   # × 2, not squared
        ["Radius = diameter ÷ 2.", "Find the whole pizza's area, then share it by 8."])]
q43 = [
    work("4.3.1", "Calculate the radius of the plastic PVC tablecloth that is used to cover the tables.", 3, [
        "Diameter = 160 cm + 35 cm + 35 cm = 230 cm\nRadius = {230}/{2}\n= 115 cm",     # the memo
        "Diameter = 160 cm + 35 cm = 195 cm\nRadius = {195}/{2}\n= 97,5 cm",            # one overhang
        "Diameter = 160 cm + 35 cm + 35 cm = 230 cm\nRadius = 230 × 2\n= 460 cm",       # doubled
        "Diameter = 160 cm\nRadius = {160}/{2}\n= 80 cm"],                              # the overhang ignored
        ["The cloth hangs 35 cm over on BOTH sides.", "Radius = diameter ÷ 2."]),
    work("4.3.2", "Calculate the height of the support pole (in cm) if the total height of the table is 78 cm.", 3, [
        "Pole = 78 cm − (2,8 cm + 0,7 cm)\n= 78 cm − 3,5 cm\n= 74,5 cm",       # the memo
        "Pole = 78 cm + (2,8 cm + 0,7 cm)\n= 78 cm + 3,5 cm\n= 81,5 cm",       # added
        "Pole = 78 cm − (2,8 cm + 35 cm)\n= 78 cm − 37,8 cm\n= 40,2 cm",       # the overhang
        "Pole = 78 cm − (2,8 cm × 0,7 cm)\n= 78 cm − 1,96 cm\n= 76,04 cm"],    # multiplied
        ["Total = base + pole + table top.", "Take the base and the top's thickness away."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Recipes and conversions", "marks": 8, "lead": RECIPE, "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Capacity", "marks": 4, "lead": "Andrea uses the measuring cup below to measure her "
                                                                                 "ingredients.",
     "figure": P.fig("1.2", "A glass measuring jug marked from 50 ml to 500 ml."), "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Circles and ratio", "marks": 4,
     "lead": "Andrea bakes her cakes in round pans, each with a diameter as shown in the diagram below.",
     "figure": P.fig("1.3", "Four round cake pans. Diameter: W = 5 inches, X = 8 inches, Y = 13 inches, Z = 16 inches."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Maps", "marks": 8,
     "lead": "The map below shows the distance between Andrea's house in Humansdorp and Jeffreys Bay where she needs to deliver a cake for a "
             "wedding.",
     "figure": P.fig("1.4", "A road map from Humansdorp (top left) to Jeffreys Bay (right, on the coast): the route box reads 26 min, 21,1 km; "
                            "Apex School of Driving, Dignity4You, Oribi Animal Clinic, Sunshine Bay Beach Club, Lombardini Game Farm, Ashton "
                            "Bay and Paradise Beach; a compass N, E, S, W."), "items": q14},
    {"id": "2.1", "title": "Question 2.1", "kind": "Maps and scale", "marks": 13,
     "lead": "Pilgrim's Rest is a small museum town in the Ehlanzeni district in Mpumalanga, South Africa. It has approximately 1 721 residents "
             "and occupies an area of 25,40 km². The map of Pilgrim's Rest and surrounding areas is shown in ANNEXURE A.",
     "figure": P.fig("2.1", "ANNEXURE A: a map of Pilgrim's Rest in a grid, columns A–G and rows 1–5, with its tourist attractions starred "
                            "(Potters, Silversmith, Pilgrim's place, Store Museum, House museum, Scott House, Info Centre, News museum, Town "
                            "Hall, The Residence, Gold Mine Digging Site, Rober's Grave) and a bar scale 0 – 100 – 200 – 600 metres. On the "
                            "printed annexure, as the memo measures it, the Store Museum is 6,4 cm from the Town Hall and the bar from 0 to 600 m "
                            "is 2,6 cm long."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Maps and travel", "marks": 14,
     "lead": "Siphokazi, who resides in Lydenburg, found the map of Mpumalanga and surrounding areas shown in ANNEXURE B.",
     "figure": P.fig("2.2", "ANNEXURE B: a map of Mpumalanga and its neighbours (Limpopo, Gauteng, Free State, KwaZulu-Natal, Swaziland, "
                            "Mozambique), with towns such as Lydenburg, Standerton, Witbank and Nelspruit, and the national roads N1, N11, N4, "
                            "N12, N17 and N2 in the key's sign."), "items": q22},
    {"id": "3.1", "title": "Question 3.1", "kind": "Volume and surface area", "marks": 23,
     "lead": "Wilmien decided to sell imported coffee beans in resealable containers to generate funds in aid of a wheelchair for her "
             "physically disabled brother. The diagram below shows two types of containers that Wilmien can choose from. The containers will "
             "be covered in petroleum-based plastic.\nThe following formulae may be used:\nVolume of a cylinder: π × radius² × height, where "
             "π = 3,142\nVolume of a rectangular prism = length × width × height\nTotal surface area of a rectangular prism: 2 (l × w) + "
             "2 (l × h) + 2 (w × h)",
     "figure": P.fig("3.1", "A rectangular-shaped container: length 150 mm, width 0,08 m, height 14,5 cm. A cylindrical-shaped container: "
                            "radius 50 mm, height 12 cm."), "items": q31},
    {"id": "4.1", "title": "Question 4.1", "kind": "Layout plans and speed", "marks": 10,
     "lead": "The layout plan of the shopping mall where Wilmien will be selling her imported coffee beans is shown below. Wilmien will only be "
             "selling to the stores that are numbered.",
     "figure": P.fig("4.1", "A mall layout plan: stores numbered 1, 2, 3, 4, 5, 6, 7, 9, 11, 12 and 13, with The Pizza Den, Kohl's, Sports "
                            "Authority, Mc Flurries, Bellis Fair Cinema, a Pet Shop and Food & More; a key for the restrooms, ATMs and mall "
                            "entrances."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Area", "marks": 10,
     "lead": "The Pizza Den is a new establishment inside the shopping mall that makes delicious pizzas. A picture of the sliced pizza and its "
             "packaging box is shown in the diagram below.\nThe pizza has a diameter of 42 cm.",
     "figure": P.fig("4.2", "A pizza cut into eight slices, and its box seen from above: dimensions of box are 45 cm × 45 cm, the round pizza "
                            "inside with a gap D on the left and the right."), "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Measurement", "marks": 6,
     "lead": "The table used inside The Pizza Den where customers can enjoy their food is shown in ANNEXURE C. The tables are covered with PVC "
             "tablecloths with an overhang of 35 cm around the table.",
     "figure": P.fig("4.3", "ANNEXURE C: the table, diameter = 160 cm, thickness = 0,7 cm, a support pole, base height = 2,8 cm; and the "
                            "tablecloth with an overhang of 35 cm."), "items": q43},
]
P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P2", "sitting": "November 2025", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.1.3", "kind": "no_fit", "detail": "The memo MEASURES the printed annexure: 6,4 cm from the Store Museum to the Town Hall "
                                                     "(accept 6,2 – 6,6) and 2,6 cm for the 0 – 600 m bar (accept 2,5 – 2,7). A phone shows the "
                                                     "map at another size, so the caption gives the memo's lengths: 2.1.3 becomes a read-off "
                                                     "(± 0,2 cm) and 2.1.4 starts from 2,6 cm. (This PDF prints both at about 93%: 5,9 cm and "
                                                     "2,4 cm, the same ratio.)"},
          {"n": "1.3.1", "kind": "memo_issue", "detail": "The stem asks for the circumference 'in squared inches (in.²)' and the memo writes "
                                                         "40,846 m; a circumference is a length, 3,142 × 13 inches = 40,846 inches. The stem is "
                                                         "kept as printed; the options give inches."},
          {"n": "4.1.2", "kind": "memo_issue", "detail": "The memo writes '0,45 ÷ 60 = 0,75 h' for 45 minutes; the right option writes 45 ÷ 60 "
                                                         "= 0,75 h."},
          {"n": "3.1.6", "kind": "no_fit", "detail": "A reason the memo accepts in any relevant words: two of its reasons as statements among "
                                                     "three false ones; pick one."}],
         {"1": 24, "2": 27, "3": 23, "4": 26}, 100,
         {"2.1.4": ["2.1.3"], "3.1.3": ["3.1.2"], "3.1.5": ["3.1.1"]},
         "Questions 1 to 4 (the whole paper)")
