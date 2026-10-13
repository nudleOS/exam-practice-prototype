"""Grade 10 Mathematical Literacy P2 November 2025 (Eastern Cape Department of Education, O.R. Tambo Coastal District), Questions 1 to 4
(75 marks as printed), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks, answers and
the memo's working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): re-published
by Stanmore Secondary (stanmorephysics.com) as one scanned PDF, the question paper (pages 1-8) then the marking guidelines (pages 9-14),
no text layer: read from its page images (100 dpi). Split into '<id> QP.pdf' and '<id> MG.pdf'.

  python tools/ingest/transcribe_g10_ml_p2_2025_11_ecort.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ml-p2-2025-11-ecort/g10-ml-p2-2025-11-ecort QP.pdf" "uploads/provincial/g10-ml-p2-2025-11-ecort/g10-ml-p2-2025-11-ecort MG.pdf" --id g10-ml-p2-2025-11-ecort --from-json

The Mathematical Literacy rulings, as in transcribe_g10_ml_p2_2024_11_nw.py. Question 3 prints 3.1 to 3.8 but marks fifteen: the memo
answers seven parts (2 + 2 + 2 + 2 + 3 + 2 + 2) and gives nothing for 3.6 ('which rooms will get sunlight in the morning'), so 3.6 is
left out and the paper plays its printed 75. Where the paper's mark and the memo's differ (2.1(b) 3 / 2, 2.3 3 / 4, 4.1.1 3 / 2,
4.1.2 7 / 8; each question still 20), the paper's mark is used. 3.5's measured length (12,1 cm on the printed plan) is in the figure's
caption, as Grade 12's measured lengths. Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi)."""
from provincial import Paper

P = Paper("g10-ml-p2-2025-11-ecort", 595.32, 841.92, {
    "1.2": [4, 61, 122, 450, 308], "Q2": [4, 101, 560, 518, 702], "Q3": [6, 66, 162, 504, 421], "4.1": [7, 40, 140, 594, 441],
    "4.2": [8, 72, 112, 425, 464]}, start=8)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term

# ---- QUESTION 1, the question paper pages 3-4 and the memo page 12 ----
q11 = [
    answer("1.1.1", "How many muffins can be made from the recipe?", 2, ["24 muffins", "12 muffins", "2 muffins", "48 muffins"],
           ["The recipe makes 2 dozen.", "A dozen is 12."]),
    work("1.1.2", "How many batches can be made with 2 litres of milk?", 2, [
        "One batch uses 0,5 ℓ\n2 ℓ ÷ 0,5 ℓ = 4 batches",      # the memo
        "One batch uses 0,5 ℓ\n2 ℓ × 0,5 ℓ = 1 batch",        # multiplied
        "One batch uses 5 ℓ\n2 ℓ ÷ 5 ℓ = 0,4 batches",         # 0,5 read as 5
        "One batch uses 0,5 ℓ\n0,5 ℓ ÷ 2 ℓ = 0,25 batches"],  # upside down
        ["Each batch needs 0,5 litre of milk.", "How many 0,5 ℓ are in 2 ℓ?"]),
    answer("1.1.3", "Write the ratio of baking powder to melted butter in its simplest form.", 2, ["1 : 4", "4 : 1", "2 : 8", "1 : 8"],
           ["2 tbsp baking powder : 8 tbsp butter.", "Divide both by 2; keep the order."]),
    answer("1.1.4", "Which two international systems of measurement can be used in recipes?", 2,
           ["Metric and imperial", "Metric and decimal", "Imperial and Roman", "Celsius and Fahrenheit"],
           ["Grams and litres are one system.", "Cups and ounces are the other."]),
    work("1.1.5", "Write the total time in hours.", 2, [
        "15 min + 20 min = 35 min\n35 ÷ 60 = 0,58 h",      # the memo
        "15 min + 20 min = 35 min\n35 ÷ 100 = 0,35 h",     # 100 minutes in an hour
        "15 min + 20 min = 35 min\n35 × 60 = 2 100 h",     # multiplied
        "20 min − 15 min = 5 min\n5 ÷ 60 = 0,08 h"],       # subtracted
        ["Add the preparation and baking times.", "There are 60 minutes in an hour."]),
    work("1.1.6", "Convert the number of cups of sugar to millilitres.", 2, [
        "1 cup = 250 ml\n2 × 250 = 500 ml",     # the memo
        "1 cup = 250 ml\n2 + 250 = 252 ml",     # added
        "1 cup = 15 ml\n2 × 15 = 30 ml",        # the tablespoon for the cup
        "1 cup = 250 ml\n250 ÷ 2 = 125 ml"],    # divided
        ["The recipe uses 2 cups of sugar.", "1 cup = 250 ml."])]
q12 = [
    answer("1.2.1", "Identify the type of clock represented by figure 1 and figure 2.", 2,
           ["Figure 1: analogue; figure 2: digital", "Figure 1: digital; figure 2: analogue", "Both analogue", "Both digital"],
           ["Figure 1 has hands.", "Figure 2 shows numbers."]),
    answer("1.2.2", "Write the time indicated by the clock in figure 1 in words.", 2,
           ["Ten minutes past ten", "Ten minutes to two", "Two minutes past ten", "Ten minutes to ten"],
           ["The short hand points to 10.", "The long hand points to 2: how many minutes is that?"]),
    answer("1.2.3", "What does a.m. in figure 2 mean?", 2, ["Morning (before noon)", "Afternoon", "Evening", "Midnight"],
           ["a.m. is ante meridiem.", "Before midday."]),
    answer("1.2.4", "Write the time in figure 1 in a 24-hour format.", 2, ["22:10", "14:50", "10:50", "20:10"],
           ["Read the hour and the minutes.", "In the evening, add 12 to the hour."])]

# ---- QUESTION 2, the question paper pages 4-5 and the memo pages 12-13 ----
C2 = "C = 2 × 3,142 × 0,68 = 4,27312 m\n"
q2 = [
    work("2.1(a)", "Calculate, in mm, the diameter of the tabletop.", 3, [
        "Diameter = 68 cm × 2 = 136 cm\n= 136 × 10\n= 1 360 mm",       # the memo
        "Diameter = 68 cm × 2 = 136 cm\n= 136 × 100\n= 13 600 mm",     # × 100 for mm
        "Diameter = 68 cm\n= 68 × 10\n= 680 mm",                       # the radius as the diameter
        "Diameter = 68 cm ÷ 2 = 34 cm\n= 34 × 10\n= 340 mm"],          # halved
        ["The radius is 68 cm.", "1 cm = 10 mm."]),
    stmt("2.1(b)", "What is the difference between diameter and radius?", 3,
         ["The diameter is the distance across the circle, through the centre, from one side of the circumference to the other.",
          "The radius is the distance from the centre to the circumference.", "The diameter is twice the radius."],
         ["The radius is twice the diameter.", "The diameter is the distance around the circle.", "The radius goes from one side to the other."],
         ["Which one passes through the centre from edge to edge?", "Which is half of the other?"], 1),
    work("2.2", "Calculate, rounded to the nearest hundred cm, the perimeter of the square piece of glass. You may use the formula: Perimeter = "
         "4 × length of side.", 3, [
        "P = 4 × 136 cm\n= 544 cm\n≈ 500 cm",      # the memo
        "P = 4 × 136 cm\n= 544 cm\n≈ 540 cm",      # rounded to the nearest ten
        "P = 4 × 68 cm\n= 272 cm\n≈ 300 cm",       # the radius as the side
        "P = 2 × 136 cm\n= 272 cm\n≈ 300 cm"],     # two sides only
        ["The glass is 136 cm by 136 cm.", "Round 544 to the nearest hundred."]),
    work("2.3", "Calculate, rounded to the nearest whole number, the area of the glass tabletop in cm². You may use the formula: Area = π × r², "
         "where π = 3,142.", 3, [
        "A = 3,142 × 68 × 68\n= 14 528,608 cm²\n≈ 14 529 cm²",       # the memo
        "A = 3,142 × 136 × 136\n= 58 114,432 cm²\n≈ 58 114 cm²",      # the diameter for the radius
        "A = 3,142 × 68 × 2\n= 427,312 cm²\n≈ 427 cm²",               # r × 2 for r²
        "A = 3,142 × 68 × 68\n= 14 528,608 cm²\n≈ 14 528 cm²"],       # rounded down
        ["r = 68 cm.", "Square the radius first."]),
    work("2.4", "Mrs Livo stated that the total cost of the aluminium strip will be less than R500. Verify, showing all calculations, whether her "
         "statement is valid. You may use the formula: Circumference of circle = 2 × 3,142 × radius.", 8, [
        C2 + "Strips = 4,27312 m ÷ 2 m = 2,14 ≈ 3 strips\nCost = 3 × R150 = R450\nLess than R500: her statement is VALID",       # the memo
        C2 + "Strips = 4,27312 m ÷ 2 m = 2,14 ≈ 2 strips\nCost = 2 × R150 = R300\nLess than R500: her statement is VALID",       # rounded down
        "C = 2 × 3,142 × 1,36 = 8,54624 m\nStrips = 8,54624 m ÷ 2 m = 4,27 ≈ 5 strips\nCost = 5 × R150 = R750\n"
        "More than R500: her statement is NOT VALID",                                                                           # the diameter for the radius
        "Perimeter = 4 × 1,36 = 5,44 m\nStrips = 5,44 m ÷ 2 m = 2,72 ≈ 3 strips\nCost = 3 × R150 = R450\nLess than R500: her statement is VALID"],   # the square's perimeter
        ["The strip goes round the circle: use the circumference in metres.", "A shop sells whole strips."])]

# ---- QUESTION 3, the question paper page 6 and the memo page 13 ----
q3 = [
    stmt("3.1", "Define the term floor plan.", 2,
         ["A floor plan shows the top view of a building, drawn to scale.", "A drawing of the layout of rooms as seen from above."],
         ["A picture of the front of a house.", "A list of the furniture in a house.", "A map of a town's streets.",
          "A drawing of the roof from the side."],
         ["Which view does it show?", "From above."], 2),
    answer("3.2", "Write down the number of windows shown on the plan.", 2, ["5", "4", "6", "3"],
           ["Windows are drawn as thin rectangles in the outer walls.", "Count every outer wall."]),
    stmt("3.3", "Name any two features that can be found in the bathroom.", 2, ["Sink (basin)", "Toilet"],
         ["Bed", "Stove", "Couch"], ["The bathroom is between the spare room and the kitchen.", "Look at its drawn fittings."], 1),
    stmt("3.4", "Write down the meaning of the scale given on the floor plan (1 : 50).", 2,
         ["1 unit on the plan is equal to 50 units on the ground (in reality).", "1 cm on the plan represents 50 cm in reality."],
         ["The house is 50 m long.", "1 cm on the plan represents 50 m in reality.", "The plan is 50 times bigger than the house.",
          "There are 50 rooms in the house."],
         ["A number scale has no units.", "Plan to reality."], 2),
    work("3.5", "Determine the actual length of the north-facing wall in metres.", 3, [
        "Measured length: 12,1 cm\n12,1 × 50 = 605 cm\n605 ÷ 100 = 6,05 m",       # the memo
        "Measured length: 12,1 cm\n12,1 ÷ 50 = 0,242 cm\n0,242 ÷ 100 = 0,002 m",   # divided by the scale
        "Measured length: 12,1 cm\n12,1 × 50 = 605 cm\n605 ÷ 1 000 = 0,605 m",     # ÷ 1 000 for metres
        "Measured length: 12,1 cm\n12,1 × 500 = 6 050 cm\n6 050 ÷ 100 = 60,5 m"],  # the scale read as 1 : 500
        ["The arrow above the plan measures 12,1 cm.", "Multiply by 50, then change cm to m."]),
    answer("3.7", "Determine the general direction of the kitchen from the main bedroom.", 2, ["South-east", "South-west", "North-east",
                                                                                                "North-west"],
           ["North points up on the plan.", "The kitchen is below and to the right of the main bedroom."]),
    answer("3.8", "What is the probability of finding windows on the western side?", 2, ["0 (impossible)", "1 (certain)", "0,5", "0,2"],
           ["West is the left-hand wall.", "Are there any windows on it?"])]

# ---- QUESTION 4, the question paper pages 7-8 and the memo pages 13-14 ----
DIMS = "Length: {2,01}/{0,335} = 6 boxes\nWidth: {0,69}/{0,23} = 3 boxes\n"
q41 = [
    work("4.1.1", "Calculate the volume of a small box. You may use the formula: Volume = l × b × h.", 3, [
        "V = 33,5 × 23 × 13\n= 10 016,5 cm³",       # the memo
        "V = 33,5 + 23 + 13\n= 69,5 cm³",           # added
        "V = 33,5 × 23\n= 770,5 cm³",               # the height left out
        "V = 2,01 × 0,69 × 0,52\n= 0,72 cm³"],      # the big box's sizes
        ["Use the small box's three sizes.", "Multiply them."]),
    work("4.1.2", "The courier company claims that one big box will hold 72 small boxes if the small boxes are packed lengthwise in the big boxes. "
         "Verify the claim.", 7, [
        "Small box: 0,335 m × 0,23 m × 0,13 m\n" + DIMS + "Height: {0,52}/{0,13} = 4 boxes\n6 × 3 × 4 = 72: the claim is VALID",       # the memo
        "Small box: 33,5 cm × 23 cm × 13 cm\nLength: {2,01}/{33,5} = 0,06 boxes\nWidth: {0,69}/{23} = 0,03 boxes\nHeight: {0,52}/{13} = 0,04 boxes\n"
        "0 boxes fit: the claim is NOT VALID",                                                                                        # units not converted
        "Small box: 0,335 m × 0,23 m × 0,13 m\n" + DIMS + "Height: {0,52}/{0,13} = 4 boxes\n6 + 3 + 4 = 13: the claim is NOT VALID",   # added
        "Small box: 0,335 m × 0,23 m × 0,13 m\nLength: {2,01}/{0,23} = 8 boxes\nWidth: {0,69}/{0,335} = 2 boxes\nHeight: {0,52}/{0,13} = 4 boxes\n"
        "8 × 2 × 4 = 64: the claim is NOT VALID"],                                                                                    # packed widthwise
        ["Change the small box's sizes to metres.", "How many fit along each edge? Multiply."], after=["4.1.1"])]
q42 = [
    answer("4.2.1", "Determine the quantity of wooden parts.", 2, ["7", "5", "4", "8"],
           ["Parts 1, 2, 3 and 4 are wooden.", "Add their quantities: 1 + 2 + 2 + 2."]),
    answer("4.2.2", "Determine the total number of bolts and screws.", 2, ["16", "8", "15", "24"],
           ["8 bolts (part 5) and 8 screws (part 7).", "Add them."]),
    answer("4.2.3", "Identify the part number that can be used to tighten the bolts.", 2, ["Part 6", "Part 5", "Part 7", "Part 4"],
           ["It is the L-shaped tool.", "One piece."]),
    answer("4.2.4", "Must the screws be turned in a clockwise or anticlockwise direction?", 2, ["Clockwise", "Anticlockwise", "Either way",
                                                                                               "Neither: they are hammered in"],
           ["Screws are tightened.", "Righty-tighty."]),
    answer("4.2.5", "Name the piece of furniture Bukho assembled.", 2, ["A (side) table", "A chair", "A bookshelf", "A bed"],
           ["Look at the finished picture.", "A top on four legs."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Recipes and conversions", "marks": 12,
     "lead": "Luntu's mother is turning 80 years old. She plans to bake some vanilla muffins using the recipe below. It takes 15 minutes for "
             "preparation and 20 minutes for baking 12 vanilla muffins.\nVANILLA MUFFINS. Ingredients for a batch (makes 2 dozen muffins): 600 g "
             "all-purpose flour; 2 cups of sugar; 2 tbsp baking powder; ¾ tsp salt; 0,5 litre milk; 2 large eggs; 1 tbsp vanilla extract; 8 tbsp "
             "butter (melted).\nKEY: tablespoon = tbsp; teaspoon = tsp; one litre = 1 000 ml; 1 tbsp = 15 ml; 1 tsp = 5 ml; 1 cup = 250 ml.",
     "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Time", "marks": 8, "lead": "Using the clocks below, answer the questions that follow.",
     "figure": P.fig("1.2", "Figure 1: a wall clock with hands, the hour hand just past 10 and the minute hand on 2. Figure 2: a digital alarm "
                            "clock showing 12:59. Note: 12:59 a.m."), "items": q12},
    {"id": "2", "title": "Question 2", "kind": "Measurement: circles", "marks": 20,
     "lead": "Mrs Livo had a coffee table that was damaged by one of her children. She decided to replace it with a circular glass tabletop which "
             "was cut from a piece of glass with dimensions of 136 cm by 136 cm.\nNOTE: a flexible aluminium strip is attached to the circular "
             "edge of the tabletop to form an edging. The aluminium edging is sold in strips of 2 m @ R150 per strip.",
     "figure": P.fig("Q2", "A square of glass 136 cm by 136 cm with a dashed circle inside touching all four sides, its radius 68 cm; beside it, "
                           "a round glass coffee table on crossed wooden legs."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Floor plans", "marks": 15,
     "lead": "The diagram below shows a floor plan of a house. It is not drawn according to scale. The scale is 1 : 50.",
     "figure": P.fig("Q3", "A floor plan, north pointing up, scale 1 : 50: the main bedroom top left, the spare room top right, the lounge "
                           "bottom left, a bathroom (sink and toilet) and the kitchen bottom right. Windows: one in each room's top wall (main "
                           "bedroom, spare room), two in the right wall (bathroom, kitchen) and one in the lounge's bottom wall; none in the "
                           "left wall. The arrow above the plan, along the north-facing wall, measures 12,1 cm on the printed paper."),
     "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Packaging", "marks": 10,
     "lead": "A shoe company packs their brand of shoes in a small box, and then the small boxes are packed in a bigger box for transportation.\n"
             "Small box: length 33,5 cm, width 23 cm, height 13 cm.\nBig box: length 2,01 m, width 0,69 m, height 0,52 m.",
     "figure": P.fig("4.1", "A grey small shoe box (33,5 cm × 23 cm × 13 cm) and a brown big cardboard box."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Assembly instructions", "marks": 10,
     "lead": "Bukho bought a piece of furniture that needs to be assembled. It is made up of a wooden top and wooden frame and metal screws and "
             "bolts. The diagram below shows the part numbers and the assembly instructions using the part numbers.",
     "figure": P.fig("4.2", "Parts: 1, a top (1 pc); 2, a square frame (2 pcs); 3, a rod (2 pcs); 4, a rod (2 pcs); 5, bolts (8 pcs); 6, an "
                            "L-shaped key (1 pc); 7, screws (8 pcs). Step 1: the frames and rods joined with bolts using the key; step 2: the "
                            "frame turned 180° and the top fixed with 8 screws turned clockwise; then the finished side table."), "items": q42}]

P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P2", "sitting": "November 2025", "total_marks": 75,
          "time": "1 hour 30 minutes"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "3.7", "kind": "memo_issue", "detail": "The memo gives South-West for the direction of the kitchen from the main bedroom; with north "
                                                       "pointing up, the kitchen (bottom right) is SOUTH-EAST of the main bedroom (top left). The "
                                                       "right option is South-east. For Murci to confirm."},
          {"n": "3.8", "kind": "memo_issue", "detail": "Question 3 prints 3.1 to 3.8 but totals 15; the memo answers seven parts and gives nothing for "
                                                       "3.6 ('which room(s) will get sunlight in the morning'), so 3.6 is left out and the paper "
                                                       "plays its printed 75."},
          {"n": "1.2.4", "kind": "low_confidence", "detail": "The memo gives 22:10 for figure 1's analogue clock; the clock shows no a.m. or p.m., "
                                                             "so 10:10 is not offered as an option and neither reading is marked wrong."},
          {"n": "2.1(b)", "kind": "low_confidence", "detail": "The paper's marks are used where they differ from the memo's (2.1(b) 3 / 2, 2.3 3 / 4, "
                                                              "4.1.1 3 / 2, 4.1.2 7 / 8); each question still totals 20."}],
         {"1": 20, "2": 20, "3": 15, "4": 20}, 75, {"4.1.2": ["4.1.1"]}, "Questions 1 to 4 (3.6 has no memo answer)")
