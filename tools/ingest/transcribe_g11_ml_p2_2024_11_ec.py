"""Grade 11 Mathematical Literacy P2 November 2024 (Eastern Cape Department of Education), the whole paper (Questions 1 to 4, 100 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks, answers and the memo's
working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za,
2024_November_Gr_11_Exams, the question paper zip (English PDF, 9 pages and blank pages, text layer), its ADDENDUM (English, 3 pages:
ANNEXURE A, a map of Knysna, and ANNEXURE B, a road map of Scranton) and the memo (English, 11 pages, text layer).

  python tools/ingest/transcribe_g11_ml_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ml-p2-2024-11-ec/MATHS LIT P2 GRADE 11 NOV 2024  ENGLISH D_watermark.pdf" "uploads/provincial/g11-ml-p2-2024-11-ec/MATHS LIT P2 GRADE 11 NOV 2024 MARKING GUIDELINE_ENG_watermark.pdf" --id g11-ml-p2-2024-11-ec --from-json --answer-book "uploads/provincial/g11-ml-p2-2024-11-ec/MATHS LIT P2 ADD GR11 NOV 2024 ENG D_watermark.pdf"

The Mathematical Literacy rulings, as in transcribe_ml_p2_2024_11.py: a calculation, a 'verify' and a 'show that' -> four whole
workings (provincial.work), the memo's first method and three real errors; a word read off -> term or an MCQ of answers; a definition
-> statements; a list of named items -> statements, one mark each. The annexures are cropped from the addendum (figure source
"answer_book", page = the addendum's page). Figure boxes are in PDF points (scratch figbox.py)."""
from provincial import Paper

BOOK = {"source": "answer_book"}
P = Paper("g11-ml-p2-2024-11-ec", 595.2, 842.0, {
    "1.1": [3, 203.0, 146.0, 377.0, 319.0], "1.2": [3, 93.0, 482.0, 488.0, 700.0], "1.3": [4, 214.0, 110.0, 400.0, 256.0],
    "1.4": [4, 104.0, 409.0, 490.0, 671.0], "3.1": [6, 124.0, 118.0, 462.0, 386.0], "3.2": [7, 115.0, 104.0, 480.0, 303.5],
    "4.2": [8, 83.0, 477.0, 517.0, 626.0],
    "2.1": [2, 42.8, 145.9, 552.7, 494.6, BOOK], "2.2": [2, 42.8, 145.9, 552.7, 494.6, BOOK], "4.1": [3, 40.0, 144.9, 546.0, 747.6, BOOK]},
    start=3)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term

# ---- QUESTION 1, the question paper pages 3-4 and the memo pages 3-4 ----
q11 = [
    answer("1.1.1", "Identify the type of clock displayed above.", 2, ["Analogue clock", "Digital clock", "Stopwatch", "Sundial"],
           ["Does it show the time with hands or with digits?", "A clock with hands has a name."]),
    answer("1.1.2", "Write down the time Zanele left home in words.", 2, ["Ten past ten in the morning", "Ten to two in the afternoon",
                                                                         "Ten past two in the afternoon", "Ten past ten in the evening"],
           ["The short hand shows the hour, the long hand the minutes.", "They drive one morning."]),
    work("1.1.3", "Zanele arrived at Reneiloe's place at 10:27. Determine how long it took her to get to Midrand.", 2, [
        "Time taken = 10:27 − 10:10\n= 17 minutes",              # the memo
        "Time taken = 10:27 − 10:02\n= 25 minutes",              # the minute hand at 2 read as 2 minutes
        "Time taken = 10:27 − 01:50\n= 8 hours 37 minutes",      # the hands swapped
        "Time taken = 10:27 + 10:10\n= 20 hours 37 minutes"],    # added
        ["Read the clock first: what time did she leave?", "Time taken = arrival − departure."])]
q12 = [
    stmt("1.2.1", "Define the term perimeter.", 2, ["Perimeter is the distance around an object or shape."],
         ["Perimeter is the space inside a shape.", "Perimeter is the length of the longest side of a shape.",
          "Perimeter is the amount a container holds.", "Perimeter is the distance from the centre of a circle to its edge."],
         ["Think of walking along the walls of the room.", "Is it a length or a space?"], 2),
    work("1.2.2", "Hence, calculate the perimeter of the room in centimetres.", 2, [
        "Perimeter = 230 + 200 + 95 + 88 + 135 + 112\n= 860 cm",   # the memo
        "Perimeter = 230 + 200 + 95 + 88 + 135\n= 748 cm",         # a side missed
        "Perimeter = 230 + 200\n= 430 cm",                         # the length and the width only
        "Perimeter = 230 × 200\n= 46 000 cm"],                     # multiplied, as for an area
        ["The room has six walls.", "Add every side's length."])]
q13 = [
    work("1.3.1", "Convert 43 cm to metres (m).", 2, [
        "43 cm ÷ 100\n= 0,43 m",       # the memo
        "43 cm × 100\n= 4 300 m",      # multiplied
        "43 cm ÷ 1 000\n= 0,043 m",    # 1 000 cm taken as 1 m
        "43 cm ÷ 10\n= 4,3 m"],        # 10 cm taken as 1 m
        ["How many centimetres make one metre?", "A metre is bigger, so the number gets smaller."]),
    work("1.3.2", "Hence, calculate the area of the tile in m². You may use the following formula: Area of a square = side × side", 2, [
        "Area = 0,43 × 0,43\n= 0,1849\n≈ 0,18 m²",      # the memo
        "Area = 0,43 × 4\n= 1,72\n≈ 1,72 m²",            # the perimeter
        "Area = 0,43 + 0,43\n= 0,86\n≈ 0,86 m²",         # added
        "Area = 43 × 43\n= 1 849\n≈ 1 849 m²"],          # the centimetres not converted
        ["Use the side in metres from 1.3.1.", "Side × side."], after=["1.3.1"])]
q14 = [
    num("1.4.1", "Identify the number of casters (wheels) needed to assemble the office chair.", 5, 0, "",
        ["Find item 1 in the list.", "Read the number after the ×."], marks=2),
    term("1.4.2", "Name the tool that will be used to tighten the bolts and washers.", ["Allen key"],
         ["Look at the bottom right of the list.", "It is an L-shaped tool."], marks=2),
    stmt("1.4.3", "List the different types of bolts and washers needed for the backrest.", 2, ["M8 × 15 mm", "M5 × 18 mm"],
         ["M8 × 22 mm", "M5 × 15 mm", "M8 × 18 mm"], ["Find BOLTS AND WASHERS in the list.", "Which ones say FOR BACKREST?"], 1)]

# ---- QUESTION 2, the question paper page 5, the memo pages 5-6 and the ADDENDUM page 2 (ANNEXURE A) ----
P23 = "\nCost = R24,45 × "
q21 = [
    term("2.1.1", "Identify the national road on the map.", ["N2"], ["National roads start with N.", "Look at the road signs on the map."],
         marks=2),
    answer("2.1.2", "In which general direction will you go if you travel from Belvidere Village to Leisure Island?", 2,
           ["South-east", "North-east", "South-west", "North-west"], ["The N arrow points up the page.", "Leisure Island is to the right "
                                                                                                       "of and below Belvidere Village."]),
    work("2.1.3", "The actual distance between Paradise and Hornlee is 7 km. Use the scale to calculate the map distance (to the nearest cm) "
         "between the two towns.", 4, [
        "7 km = 700 000 cm\nMap distance = {700 000}/{56 000}\n= 12,5 cm\n≈ 13 cm",      # the memo
        "7 km = 70 000 cm\nMap distance = {70 000}/{56 000}\n= 1,25 cm\n≈ 1 cm",         # 10 000 cm taken as 1 km
        "7 km = 700 000 cm\nMap distance = {700 000}/{56 000}\n= 12,5 cm\n≈ 12 cm",      # 12,5 rounded down
        "7 km = 700 000 cm\nMap distance = {56 000}/{700 000}\n= 0,08 cm\n≈ 0,1 cm"],    # upside down
        ["1 : 56 000 means 1 cm on the map is 56 000 cm on the ground.", "Change 7 km to cm, then divide by 56 000."])]
q22 = [
    work("2.2.1", "Calculate the approximate time, in minutes, that Busisiwe will take to travel from Knysna Heights to Pezula Estate. You may "
         "use the following formula: Speed = Distance ÷ Time", 4, [
        "Time = {11,2 km}/{100 km/h}\n= 0,112 hours\n= 0,112 × 60\n= 6,72 minutes",         # the memo
        "Time = {100 km/h}/{11,2 km}\n= 8,93 hours\n= 8,93 × 60\n= 535,8 minutes",           # upside down
        "Time = 11,2 km × 100 km/h\n= 1 120 hours\n= 1 120 × 60\n= 67 200 minutes",          # multiplied
        "Time = {11,2 km}/{100 km/h}\n= 0,112 hours\n= 0,112 × 100\n= 11,2 minutes"],        # 100 minutes in an hour
        ["Time = distance ÷ speed.", "How many minutes are in an hour?"]),
    work("2.2.2", "Busisiwe and her friends travelled an approximate distance, in and around Pezula Estate, of 156 km with her car. Determine "
         "the total distance Busisiwe travelled during the weekend including her trip to Pezula Estate and back.", 3, [
        "Total = (11,2 km × 2) + 156 km\n= 178,4 km",     # the memo
        "Total = 11,2 km + 156 km\n= 167,2 km",           # the trip back forgotten
        "Total = (11,2 km + 156 km) × 2\n= 334,4 km",     # the weekend driving doubled too
        "Total = 156 km − (11,2 km × 2)\n= 133,6 km"],    # subtracted
        ["She drives there AND back.", "Then add the weekend's 156 km."]),
    work("2.2.3", "Busisiwe claims that she will spend less than R250,00 on petrol for her return trip including the weekend driving to and "
         "from Pezula Estate. Verify, with the necessary calculations, whether her statement is valid or not. NOTE: Cost of petrol = R24,45 "
         "per litre", 5, [
        "Petrol = {178,4}/{100} × 5,7\n= 10,1688 litres" + P23 + "10,1688\n= R248,63\nLess than R250: her statement is valid",          # the memo
        "Petrol = {178,4}/{5,7} × 100\n= 3 129,82 litres" + P23 + "3 129,82\n= R76 524,21\nMore than R250: her statement is not valid",  # inverted
        "Petrol = {178,4}/{100} × 5,7\n= 10,1688 litres" + P23 + "10,1688 × 2\n= R497,25\nMore than R250: her statement is not valid",  # doubled again
        "Petrol = {178,4}/{100} + 5,7\n= 7,484 litres" + P23 + "7,484\n= R182,98\nLess than R250: her statement is valid"],            # added 5,7
        ["5,7 litres for every 100 km: how many litres for 178,4 km?", "Then multiply the litres by the price."], after=["2.2.2"])]

# ---- QUESTION 3, the question paper pages 6-7 and the memo pages 7-9 ----
q31 = [
    stmt("3.1.1", "Define the term volume in the context above.", 2, ["Volume is the amount of space inside the fish tank."],
         ["Volume is the distance around the fish tank.", "Volume is the area of the bottom of the fish tank.",
          "Volume is the weight of the water in the fish tank.", "Volume is the height of the water in the fish tank."],
         ["Volume is measured in cubic units.", "Of what?"], 2),
    work("3.1.2", "Calculate the height of the fish tank if the volume is 38,8 ft³. You may use the following formula: Volume of fish tank = "
         "π × radius² × height, where π = 3,142", 3, [
        "38,8 = 3,142 × 2,1² × height\n38,8 = 13,85622 × height\nHeight = {38,8}/{13,85622}\n= 2,8 ft",      # the memo
        "38,8 = 3,142 × 2,1 × height\n38,8 = 6,5982 × height\nHeight = {38,8}/{6,5982}\n= 5,9 ft",          # the radius not squared
        "38,8 = 3,142 × 4,2² × height\n38,8 = 55,42488 × height\nHeight = {38,8}/{55,42488}\n= 0,7 ft",     # the diameter used
        "38,8 = 3,142 × 2,1² × height\n38,8 = 13,85622 × height\nHeight = 38,8 × 13,85622\n= 537,6 ft"],    # multiplied
        ["Put the radius 2,1 ft and the volume into the formula.", "Undo the × by dividing."]),
    work("3.1.3", "The required temperature for the fish tank is 72 ℉. Hein claims that he needs to set the temperature to 22,2 ℃ to be "
         "equivalent to the required temperature. Verify, with the necessary calculations, whether Hein's claim is valid or not. You may use "
         "the following formula: ℃ = (℉ − 32°) × 5/9", 3, [
        "℃ = (72 − 32) × {5}/{9}\n= 22,2 ℃\nHein's claim is valid",          # the memo
        "℃ = 72 − 32 × {5}/{9}\n= 54,2 ℃\nHein's claim is not valid",        # the brackets ignored
        "℃ = (72 − 32) × {9}/{5}\n= 72 ℃\nHein's claim is not valid",        # the fraction upside down
        "℃ = (72 + 32) × {5}/{9}\n= 57,8 ℃\nHein's claim is not valid"],     # 32 added
        ["Work the bracket first.", "Then multiply by 5/9."]),
    work("3.1.4", "The fish tank is 75% full of water. After adding stones to the bottom of the fish tank, the fish tank is 87% full of water. "
         "Calculate the volume of the stones in cubic feet (ft³). Round your final answer to ONE decimal place.", 5, [
        "Stones = 87% − 75%\n= 12%\nVolume = {12}/{100} × 38,8\n= 4,656 ft³\n≈ 4,7 ft³",          # the memo
        "Stones = 87% + 75%\n= 162%\nVolume = {162}/{100} × 38,8\n= 62,856 ft³\n≈ 62,9 ft³",      # added
        "Stones = 87% − 75%\n= 12%\nVolume = 12 × 38,8\n= 465,6 ft³\n≈ 465,6 ft³",                # the % not divided by 100
        "Stones = 100% − 87%\n= 13%\nVolume = {13}/{100} × 38,8\n= 5,044 ft³\n≈ 5,0 ft³"],        # the empty part
        ["The stones push the water up from 75% to 87%.", "That rise is the stones' share of 38,8 ft³."]),
    work("3.1.5", "Hein has 7 fish in his fish tank: 3 yellow, 1 blue, 2 red, and 1 silver. Determine the probability (as a percentage) of "
         "selecting a silver fish from the fish tank.", 3, [
        "P = {1}/{7} × 100\n= 14,2857…\n≈ 14,29%",     # the memo
        "P = {1}/{6} × 100\n= 16,6667…\n≈ 16,67%",     # the silver fish left out of the total
        "P = {3}/{7} × 100\n= 42,8571…\n≈ 42,86%",     # the yellow fish
        "P = {1}/{4} × 100\n= 25\n≈ 25%"],              # four colours as the total
        ["How many silver fish are there?", "Out of how many fish?"])]
T3 = "Length = 24 cm = 240 mm\nTSA = "
q32 = [
    work("3.2.1", "Calculate the total surface area (in mm²) of one of the bricks needed for the wall display cabinet. You may use the "
         "following formula: Total Surface Area = [2 (l × w) + 2 (l × h) + 2 (w × h)]", 4, [
        T3 + "2(240 × 112) + 2(240 × 70) + 2(112 × 70)\n= 53 760 + 33 600 + 15 680\n= 103 040 mm²",                                  # the memo
        "Length = 24 mm\nTSA = 2(24 × 112) + 2(24 × 70) + 2(112 × 70)\n= 5 376 + 3 360 + 15 680\n= 24 416 mm²",                    # not converted
        T3 + "(240 × 112) + (240 × 70) + (112 × 70)\n= 26 880 + 16 800 + 7 840\n= 51 520 mm²",                                        # the 2s left out
        "Length = 24 cm = 2 400 mm\nTSA = 2(2 400 × 112) + 2(2 400 × 70) + 2(112 × 70)\n= 537 600 + 336 000 + 15 680\n= 889 280 mm²"],  # × 100
        ["The length is in cm: change it to mm first.", "Each face appears twice."]),
    work("3.2.2", "Determine the number of complete pallets transported by truck if one pallet contains 500 bricks.", 2, [
        "Pallets = {2 500}/{500}\n= 5 pallets",       # the memo
        "Pallets = 2 500 × 500\n= 1 250 000 pallets",  # multiplied
        "Pallets = {500}/{2 500}\n= 0,2 pallets",      # upside down
        "Pallets = 2 500 − 500\n= 2 000 pallets"],     # subtracted
        ["He needs 2 500 bricks.", "How many groups of 500?"]),
    work("3.2.3", "The weight of the pallets transported is 9 187,5 kg. Convert the weight of one pallet to ton. NOTE: 1 000 kg = 1 ton", 3, [
        "One pallet = {9 187,5}/{5}\n= 1 837,5 kg\n= {1 837,5}/{1 000}\n= 1,8375 ton",        # the memo
        "One pallet = {9 187,5}/{5}\n= 1 837,5 kg\n= 1 837,5 × 1 000\n= 1 837 500 ton",      # multiplied by 1 000
        "One pallet = {9 187,5}/{500}\n= 18,375 kg\n= {18,375}/{1 000}\n= 0,018375 ton",     # divided by the bricks on a pallet
        "One pallet = 9 187,5 × 5\n= 45 937,5 kg\n= {45 937,5}/{1 000}\n= 45,9375 ton"],     # multiplied by 5
        ["9 187,5 kg is all the pallets together.", "Divide by the number of pallets, then by 1 000."], after=["3.2.2"]),
    work("3.2.4", "Hein claims that the volume of all the bricks is 4,7 m³. Verify, with the necessary calculations, whether Hein's claim is "
         "valid or not. You may use the following formula: Volume of one brick = Length × Width × Height", 5, [
        "Volume = 240 mm × 112 mm × 70 mm\n= 1 881 600 mm³\nAll bricks = 1 881 600 × 2 500\n= 4 704 000 000 mm³\n"
        "= {4 704 000 000}/{1 000 000 000} = 4,7 m³\nHein's claim is valid",                                                # the memo
        "Volume = 240 mm × 112 mm × 70 mm\n= 1 881 600 mm³\nAll bricks = 1 881 600 × 2 500\n= 4 704 000 000 mm³\n"
        "= {4 704 000 000}/{1 000 000} = 4 704 m³\nHein's claim is not valid",                                              # mm³ to m³ by 10⁶
        "Volume = 240 mm × 112 mm × 70 mm\n= 1 881 600 mm³\nAll bricks = 1 881 600 × 500\n= 940 800 000 mm³\n"
        "= {940 800 000}/{1 000 000 000} = 0,9 m³\nHein's claim is not valid",                                              # one pallet
        "Volume = 24 mm × 112 mm × 70 mm\n= 188 160 mm³\nAll bricks = 188 160 × 2 500\n= 470 400 000 mm³\n"
        "= {470 400 000}/{1 000 000 000} = 0,5 m³\nHein's claim is not valid"],                                             # 24 cm as 24 mm
        ["Find one brick's volume in mm³, then all 2 500.", "1 m³ = 1 000 000 000 mm³."]),
    work("3.2.5", "One of the bricks that Hein is going to use costs R2,60 and the cost of delivery is R650. Calculate the cost Hein will have "
         "to pay for the bricks that will be needed, including delivery. Round your final answer to the nearest hundred rand.", 4, [
        "Bricks = R2,60 × 2 500\n= R6 500\nTotal = R6 500 + R650 = R7 150\n≈ R7 200",    # the memo
        "Bricks = R2,60 × 2 500\n= R6 500\nTotal = R6 500 + R650 = R7 150\n≈ R7 100",    # rounded down
        "Bricks = R2,60 × 500\n= R1 300\nTotal = R1 300 + R650 = R1 950\n≈ R2 000",      # one pallet's bricks
        "Bricks = R2,60 × 2 500\n= R6 500\nTotal = R6 500 − R650 = R5 850\n≈ R5 900"],   # delivery subtracted
        ["All 2 500 bricks, plus delivery once.", "R7 150 lies halfway between two hundreds: which way?"])]

# ---- QUESTION 4, the question paper pages 8-9, the memo pages 10-11 and the ADDENDUM page 3 (ANNEXURE B) ----
H = "Time = {121,4}/{85} = 1,4282 hours\n0,4282 × 60 = 25,69 minutes\nTravel time = 1 h 25 min 42 s\n"
q41 = [
    stmt("4.1.1", "List TWO types of scales used on maps.", 2, ["Bar (graphic or linear) scale", "Number (ratio) scale"],
         ["Temperature scale", "Richter scale", "Weighing scale"], ["One is drawn, one is written as a ratio.", "Look at the bottom of "
                                                                                                                  "the map."], 1),
    work("4.1.2", "Using the given scale, calculate the actual distance in miles between Clarks Summit and Archbald, if the distance on the "
         "map between these two places is 10,5 cm. (On the printed map, the scale bar from 0 to 12 mi measures 6,7 cm.)", 5, [
        "6,7 cm = 12 miles\n1 cm = {12}/{6,7} = 1,791 miles\nDistance = 10,5 × 1,791\n= 18,81 miles",       # the memo
        "6,7 cm = 12 miles\n1 cm = {6,7}/{12} = 0,558 miles\nDistance = 10,5 × 0,558\n= 5,86 miles",        # upside down
        "6,7 cm = 6 miles\n1 cm = {6}/{6,7} = 0,896 miles\nDistance = 10,5 × 0,896\n= 9,40 miles",          # the bar's 6 read as its end
        "6,7 cm = 12 miles\n1 cm = 12 × 6,7 = 80,4 miles\nDistance = 10,5 × 80,4\n= 844,2 miles"],         # multiplied
        ["How many miles does 1 cm stand for?", "Then multiply by 10,5 cm."]),
    work("4.1.3", "A tourist must attend a conference in Blakely at 15:00. The travelling distance from his house to Blakely is 121,4 miles. "
         "He claims that if he leaves his house at 13:30 and stops at the petrol station for 25 minutes, he will be on time for his "
         "conference. The tourist travels at an average speed of 85 miles/hour. Verify, with the necessary calculations, whether his claim "
         "is valid or not. You may use the following formula: Time = Distance ÷ Speed", 6, [
        H + "Arrival = 13:30:00 + 01:25:42 + 00:25:00\n= 15:20:42\nAfter 15:00: his claim is not valid",           # the memo
        H + "Arrival = 13:30:00 + 01:25:42\n= 14:55:42\nBefore 15:00: his claim is valid",                          # the stop forgotten
        "Time = {121,4}/{85} = 1,4282 hours\n1,4282 hours = 1 h 43 min\nTravel time = 1 h 43 min\n"
        "Arrival = 13:30 + 01:43 + 00:25\n= 15:38\nAfter 15:00: his claim is not valid",                           # 0,4282 h read as 43 min
        "Time = {85}/{121,4} = 0,7002 hours\n0,7002 × 60 = 42,01 minutes\nTravel time = 0 h 42 min 1 s\n"
        "Arrival = 13:30:00 + 00:42:01 + 00:25:00\n= 14:37:01\nBefore 15:00: his claim is valid"],                 # upside down
        ["Time = distance ÷ speed, in hours: change the decimal part to minutes.", "Add the driving time AND the stop to 13:30."]),
    answer("4.1.4", "Determine the probability of randomly selecting a road on the map that is a state road.", 2,
           ["P = 2/8 (= 1/4)", "P = 3/8", "P = 2/3", "P = 1/8"],
           ["List every road number on the map: 81, 476, 48, 380, 11, 6, 436, 690.", "Which of them wear the State Road sign?"])]
q42 = [
    work("4.2.1", "Show that the area of the white cloth needed to cover the circle is 70,89 cm². You may use the following formula: Area of a "
         "circle = π × radius², where π = 3,142", 3, [
        "Radius = {9,5}/{2} = 4,75 cm\nArea = 3,142 × 4,75²\n= 70,89 cm²",        # the memo
        "Radius = 9,5 cm\nArea = 3,142 × 9,5²\n= 283,57 cm²",                     # the diameter as the radius
        "Radius = {9,5}/{2} = 4,75 cm\nArea = 3,142 × 4,75 × 2\n= 29,85 cm²",     # × 2, not squared
        "Radius = {9,5}/{2} = 4,75 cm\nArea = (3,142 × 4,75)²\n= 222,74 cm²"],    # π squared too
        ["9,5 cm is across the circle: the diameter.", "Square only the radius."]),
    work("4.2.2", "Determine the width of the rectangular wooden frame in centimetres, if the area of the rectangular wooden frame, without "
         "the circle, is 2 682 cm². You may use the following formula: Area of a rectangle = Length × Width. NOTE: 1 inch = 2,54 cm", 5, [
        "Length = 22 inches × 2,54 = 55,88 cm\n2 682 = 55,88 × width\nWidth = {2 682}/{55,88}\n= 48 cm",           # the memo
        "Length = {22}/{2,54} = 8,66 cm\n2 682 = 8,66 × width\nWidth = {2 682}/{8,66}\n= 309,65 cm",               # divided by 2,54
        "Length = 22 inches\n2 682 = 22 × width\nWidth = {2 682}/{22}\n= 121,91 cm",                               # not converted
        "Length = 22 inches × 2,54 = 55,88 cm\n2 682 = 55,88 × width\nWidth = 2 682 × 55,88\n= 149 870,16 cm"],    # multiplied
        ["Change 22 inches to cm first.", "Width = area ÷ length."]),
    work("4.2.3", "Lwandile claims that the width of ONE of the rectangular bars is 8 cm. Verify, with the necessary calculations, whether his "
         "claim is valid or not.", 3, [
        "Bars on the flag = 6\nOne bar = {48}/{6} = 8 cm\nLwandile's claim is valid",              # the memo
        "Bars on the flag = 3\nOne bar = {48}/{3} = 16 cm\nLwandile's claim is not valid",         # the three colours
        "Bars on the flag = 5\nOne bar = {48}/{5} = 9,6 cm\nLwandile's claim is not valid",        # a bar missed
        "Bars on the flag = 6\nOne bar = {55,88}/{6} = 9,31 cm\nLwandile's claim is not valid"],   # the length shared
        ["Count the stripes on the flag.", "Share the width from 4.2.2 among them."], after=["4.2.2"])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Time", "marks": 6,
     "lead": "Zanele and Reneiloe are driving to Pretoria one morning. Zanele departs from Randburg and picks up Reneiloe who stays in "
             "Midrand. The car is driven at an average speed of 100 km/h from Randburg to Midrand and then to Pretoria. The clock below shows "
             "the time at which Zanele left Randburg.",
     "figure": P.fig("1.1", "A round analogue wall clock: the short hand at 10, the long hand at 2."), "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Perimeter", "marks": 4, "lead": "Sisanda drew the diagram below, showing the room she "
                                                                                     "uses to study.",
     "figure": P.fig("1.2", "An L-shaped room: sides 230 cm, 200 cm, 95 cm, 88 cm, 135 cm (with the door) and 112 cm."), "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Area", "marks": 4,
     "lead": "Timothy wants to lay ceramic tiles in his rectangular bedroom. Study the details of the size of the tiles that Timothy will use.",
     "figure": P.fig("1.3", "A square ceramic tile, 43 cm by 43 cm."), "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Assembly", "marks": 6,
     "lead": "Study the list of items below that are needed to assemble an office chair.",
     "figure": P.fig("1.4", "The office chair's parts: 1 casters ×5, 2 base ×1, 3 gas lift ×1, 4 armrest ×2, 5 seat cushion ×1, 6 backrest "
                            "×1, a headrest ×1; bolts and washers: M8 × 22 mm for the armrest, M8 × 15 mm and M5 × 18 mm for the backrest; "
                            "an Allen key."), "items": q14},
    {"id": "2.1", "title": "Question 2.1", "kind": "Maps", "marks": 8,
     "lead": "Knysna is a town in the Western Cape province of South Africa. The map of Knysna and surrounding areas in the Western Cape is "
             "shown in ANNEXURE A.",
     "figure": P.fig("2.1", "ANNEXURE A: a map of Knysna and surrounding areas, with the N2, Paradise, Central, Belvidere Village, Knysna "
                            "Heights, Thesens Island, Leisure Island, Hornlee, Fisher's Haven, Pezula Estate and the Indian Ocean; a north "
                            "arrow and the scale 1 : 56 000."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Distance and fuel", "marks": 12,
     "lead": "Busisiwe lives in Knysna Heights and plans a trip to Pezula Estate where she will spend the weekend with her friends. The "
             "distance between Knysna Heights and Pezula Estate is 11,2 km travelled via the N2.\nBusisiwe travels at an average speed of "
             "100 km/h and she drives a Polo Vivo 1.4 with a fuel consumption of 5,7 litres per 100 km.",
     "figure": P.fig("2.2", "ANNEXURE A: the map of Knysna, Knysna Heights in the west and Pezula Estate in the south-east."), "items": q22},
    {"id": "3.1", "title": "Question 3.1", "kind": "Volume", "marks": 16,
     "lead": "Hein bought a fish tank at Premium Aquatics. The fish tank, with dimensions, is shown in the picture below.",
     "figure": P.fig("3.1", "A round glass fish tank with fish, plants and stones. Dimensions of the fish tank: radius = 2,1 foot."),
     "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Surface area and volume", "marks": 18,
     "lead": "Hein wants to build a cabinet to display his fish tank and to prevent it from falling and breaking. His bricklayer informed him "
             "that he would need about 2 500 bricks for the cabinet he has in mind. Below is an image of the brick they will use.",
     "figure": P.fig("3.2", "A brick: length = 24 cm, width = 112 mm, height = 70 mm; weight of brick = 3,675 kg."), "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Maps and time", "marks": 15,
     "lead": "Scranton is a hamlet in the town of Pennsylvania in New York, United States. Study the road map of Scranton in ANNEXURE B of the "
             "addendum.",
     "figure": P.fig("4.1", "ANNEXURE B: a road map of Scranton, with Clarks Summit, Chinchilla, Blakely, Dickson City, Archbald, Jessup, "
                            "Dunmore, Scranton, Taylor, Old Forge, Moosic, Avoca and Dupont; interstates 81, 476, 48 and 380, highways 11 "
                            "and 6, state roads 436 and 690; a scale bar 0 – 3 – 6 – 12 mi; the key State Road, Highway, Interstate."),
     "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Area", "marks": 11,
     "lead": "Lwandile bought an Ugandan flag mounted on a rectangular wooden frame as shown in the diagrams below. (Diagram NOT drawn to "
             "scale).",
     "figure": P.fig("4.2", "Left: the Ugandan flag, six horizontal stripes with a white circle in the middle. Right: the rectangular wooden "
                            "frame, length 22 inches, an unknown width, and a circle 9,5 cm across."), "items": q42},
]
P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P2", "sitting": "November 2024", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "4.1.2", "kind": "no_fit", "detail": "The memo's 1A measures the bar scale on the printed map (6,7 cm for 12 miles); a screen "
                                                     "cannot be measured, so the stem gives the measurement and the four workings start from it."},
          {"n": "1.4.3", "kind": "no_fit", "detail": "A list of the two backrest bolts: two statements to pick, one mark each, as the memo's "
                                                     "1A + 1A."},
          {"n": "4.1.1", "kind": "no_fit", "detail": "Two types of map scale: two statements to pick, one mark each, as the memo's 1A + 1A."},
          {"n": "4.1", "kind": "figure_unclear", "detail": "ANNEXURE B's heading says QUESTION 4.2; the paper's instructions and Question 4.1 use it "
                                                   "for 4.1 (4.2 reads the flag on the question paper)."}],
         {"1": 20, "2": 20, "3": 34, "4": 26}, 100,
         {"1.3.2": ["1.3.1"], "2.2.3": ["2.2.2"], "3.2.3": ["3.2.2"], "4.2.3": ["4.2.2"]},
         "Questions 1 to 4 (the whole paper)")
