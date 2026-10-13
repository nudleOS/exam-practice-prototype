"""Grade 10 Mathematical Literacy P2 November 2024 (North West Department of Education, provincial assessment), the whole paper
(Questions 1 to 4, 75 marks, 1½ hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`.
Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours.
Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment, the question paper PDF (English, 7 pages, text
layer; the layout, bottle, tyre steps and boxes are images) and the marking guidelines PDF (English, 5 pages), read from their text
and page images (100 dpi).

  python tools/ingest/transcribe_g10_ml_p2_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ml-p2-2024-11-nw/19-NOVEMBER-2024-NW-S2-GR10-MATHEMATICAL-LITERACY-P2-ENG-QP.pdf" "uploads/provincial/g10-ml-p2-2024-11-nw/19-NOVEMBER-2024-NW-S2-GR10-MATHEMATICAL-LITERACY-P2-ENG-MG.pdf" --id g10-ml-p2-2024-11-nw --from-json

The Mathematical Literacy rulings, as in transcribe_g11_ml_p2_2024_11_ec.py: a calculation or a 'verify' -> four whole workings
(provincial.work), the memo's first method and three real errors; a word read off -> term or an MCQ of answers; a definition, an
explanation or directions -> statements; matching columns (1.1) and the tyre-changing steps (4.1.2) -> match.
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ml-p2-2024-11-nw", 595.32, 841.92, {
    "Q2.1": [4, 92, 182, 535, 352], "Q3": [5, 55, 199, 500, 480], "Q4.1": [6, 92, 262, 528, 492], "Q4.2": [7, 124, 169, 504, 340]},
    start=5)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term


def match(n, q, left, right, a, each, clues, **kw):
    """Matching columns: a, the index in right of each left row's answer; each row earns `each`."""
    return {"t": "match", "n": n, "marks": len(left) * each, "q": q, "clues": clues, "left": left, "right": right, "a": a,
            **({"each": each} if each > 1 else {}), **kw}


# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
q11 = [
    match("1.1", "Choose the unit/symbol from COLUMN B that matches the concept in COLUMN A.",
          ["Capacity", "Area", "Height", "Temperature"], ["℃", "millimetres", "millilitres", "m²", "kg"], [2, 3, 1, 0], 2,
          ["Capacity is how much a container holds.", "Area is measured in square units."])]
q12 = [
    answer("1.2.1", "Write 21:00 in a 12-hour format.", 2, ["09:00 pm", "09:00 am", "11:00 pm", "21:00 pm"],
           ["Subtract 12 from hours after 12:00.", "Is 21:00 in the morning or the evening?"]),
    work("1.2.2", "What time will the movie end?", 2, [
        "21:00 + 1 hour 45 minutes\n= 22:45",      # the memo
        "21:00 + 1 hour 45 minutes\n= 22:85",      # minutes added as a decimal
        "21:00 − 1 hour 45 minutes\n= 19:15",      # subtracted
        "21:00 + 1,45 hours\n= 22:27"],            # 1 h 45 min read as 1,45 hours
        ["Add the hour first, then the minutes.", "There are 60 minutes in an hour."])]
q13 = [
    work("1.3", "Connie weighs 94 kg and is concerned about her weight. She has joined a gym and wants to lose some weight. Convert her "
         "weight to grams.", 2, [
        "94 kg × 1 000\n= 94 000 g",     # the memo
        "94 kg ÷ 1 000\n= 0,094 g",      # divided
        "94 kg × 100\n= 9 400 g",        # × 100
        "94 kg × 10\n= 940 g"],          # × 10
        ["How many grams are in 1 kg?", "Grams are smaller, so the number gets bigger."])]

# ---- QUESTION 2, the question paper page 4 and the memo page 3 ----
ONE = "Rooms 01 to 06: 6 × 3 = 18 beds\nRoom 07: 4 beds\n"
q21 = [
    answer("2.1.1", "Write down the number of the room labelled A.", 2, ["Room 05", "Room 06", "Room 02", "Room 08"],
           ["The rooms on the top row go 07, A, 03, 01.", "They count up in odd numbers."]),
    answer("2.1.2", "Kitso is staying at B07. Explain what B07 means in this context.", 2,
           ["Block B, room 07", "Room B, block 07", "Bed 7 in room B", "Block 07, bed B"],
           ["The blocks are labelled with letters.", "The rooms are numbered."]),
    stmt("2.1.3", "Write a set of directions to walk from room 04 to room 07.", 3,
         ["From room 04, turn left into the passage.", "Walk to the end of the passage.", "Enter the room on the right-hand side (room 07)."],
         ["From room 04, turn right towards the entrance.", "Enter the bathroom on the left-hand side.",
          "Walk past the toilets and out of the block.", "Go up the stairs to the second floor."],
         ["Room 07 is at the far end, on the same side as room 03.", "Which way is that from room 04's door?"], 1),
    work("2.1.4", "The hostel matron states that the total number of learners in the hostel if ALL the rooms are fully occupied is 192. "
         "Verify, showing ALL calculations, whether her statement is CORRECT.", 4, [
        ONE + "One block: 18 + 4 = 22 learners\n12 blocks: 22 × 12 = 264\n264 ≠ 192: her statement is NOT CORRECT",           # the memo
        "Rooms 01 to 04: 4 × 3 = 12 beds\nRoom 07: 4 beds\nOne block: 12 + 4 = 16 learners\n12 blocks: 16 × 12 = 192\n"
        "192 = 192: her statement is CORRECT",                                                                                # the numbered rooms only
        "Rooms 01 to 07: 7 × 3 = 21 beds\nRoom 07: 4 beds\nOne block: 21 + 4 = 25 learners\n12 blocks: 25 × 12 = 300\n"
        "300 ≠ 192: her statement is NOT CORRECT",                                                                            # room 07 counted twice
        ONE + "One block: 18 + 4 = 22 learners\n12 blocks: 22 + 12 = 34\n34 ≠ 192: her statement is NOT CORRECT"],           # added, not multiplied
        ["How many rooms are in one block (A and the dotted room too)?", "Each room has 3 beds, but room 07 has 4."]),
    stmt("2.1.5", "Explain the meaning of the scale 1 : 150.", 2,
         ["1 unit on the layout represents 150 of the same units in real life.", "1 cm on the layout is 150 cm in reality."],
         ["The real building is 150 times smaller than the layout.", "The layout is 150 times bigger than the real building.",
          "There are 150 rooms in the hostel.", "1 m on the layout is 150 cm in reality."],
         ["A number scale has no units: both sides use the same unit.", "Is the layout bigger or smaller than the real building?"], 2),
    work("2.1.6", "The actual width of bedroom 07 is 3,6 m. Use the given scale to calculate the bedroom width on the layout in mm.", 4, [
        "3,6 m ÷ 150 = 0,024 m\nLayout width = 0,024 × 1 000\n= 24 mm",           # the memo
        "3,6 m × 150 = 540 m\nLayout width = 540 × 1 000\n= 540 000 mm",           # × the scale
        "3,6 m ÷ 150 = 0,024 m\nLayout width = 0,024 × 100\n= 2,4 mm",            # × 100 for mm
        "150 ÷ 3,6 m = 41,67 m\nLayout width = 41,67 × 1 000\n= 41 666,67 mm"],   # divided the wrong way round
        ["Is the layout length smaller or bigger than the real length?", "How many mm are in 1 m?"])]
q22 = [
    work("2.2", "The hostel caretaker found a library card at the hostel gate. What is the probability as a percentage, that it belongs to a "
         "learner in Block A? Round off your answer to the nearest percentage.", 4, [
        "P = {22}/{264} × 100\n= 8,33 %\n≈ 8 %",          # 2.1.4's numbers (the memo uses 24/192, flag)
        "P = {22}/{192} × 100\n= 11,46 %\n≈ 11 %",        # the matron's total
        "P = {22}/{264}\n= 0,083\n≈ 0 %",                 # not × 100
        "P = {264}/{22} × 100\n= 1 200 %\n≈ 1 200 %"],    # upside down
        ["How many learners live in Block A, and in the whole hostel?", "Probability = favourable ÷ total; × 100 for a percentage."],
        after=["2.1.4"])]

# ---- QUESTION 3, the question paper pages 5-6 and the memo page 4 ----
R4 = "r = 8 cm ÷ 2 = 4 cm\n"
V = "1 206,53 cm³ = 1 206,53 ml\n"
q3 = [
    work("3.1", "Determine the amount of milk needed in ml, if 1 cup = 200 ml.", 2, [
        "1⅔ × 200 ml\n= 333,33 ml",      # the memo
        "⅔ × 200 ml\n= 133,33 ml",       # the whole cup left out
        "1⅔ + 200 ml\n= 201,67 ml",      # added, not multiplied
        "1,23 × 200 ml\n= 246 ml"],      # 1⅔ read as 1,23
        ["How many cups of milk does the recipe use?", "Multiply the cups by 200 ml."]),
    work("3.2", "Determine the number of bananas needed to make 1 500 ml of smoothie.", 3, [
        "{1 500 ml}/{550 ml} × 1 banana\n= 2,73 bananas\n≈ 3 bananas",      # the memo
        "{1 500 ml}/{550 ml} × 1 banana\n= 2,73 bananas\n≈ 2 bananas",      # rounded down
        "{550 ml}/{1 500 ml} × 1 banana\n= 0,37 bananas\n≈ 1 banana",       # upside down
        "{1 500 ml}/{200 ml} × 1 banana\n= 7,5 bananas\n≈ 8 bananas"],      # the cup size for the recipe's yield
        ["One banana makes 550 ml of smoothie.", "Can you buy part of a banana?"]),
    answer("3.3", "Convert 240 mm to cm.", 2, ["24 cm", "2,4 cm", "2 400 cm", "240 cm"],
           ["How many mm are in 1 cm?", "Centimetres are bigger, so the number gets smaller."]),
    work("3.4", "Hence determine the volume of this bottle in cm³. You may use the formula: V = πr²h, where π = 3,142.", 4, [
        R4 + "V = 3,142 × (4 cm)² × 24 cm\n= 1 206,53 cm³",          # the memo
        "r = 8 cm\nV = 3,142 × (8 cm)² × 24 cm\n= 4 826,11 cm³",      # the diameter for the radius
        R4 + "V = 3,142 × (4 cm)² × 240 cm\n= 12 065,28 cm³",        # the height in mm
        R4 + "V = 3,142 × 4 cm × 24 cm\n= 301,63 cm³"],              # r not squared
        ["The radius is half the diameter.", "Use the height in cm from 3.3."], after=["3.3"]),
    work("3.5", "Connie claims that one bottle is big enough to hold TWICE the mixture. Verify, showing ALL calculations, whether her claim is "
         "VALID.", 5, [
        V + "Number of mixtures = 1 206,53 ml ÷ 550 ml\n= 2,19\nAt least 2: her claim is VALID",           # the memo
        "1 206,53 cm³ = 1,21 ml\nNumber of mixtures = 1,21 ml ÷ 550 ml\n= 0,002\nLess than 2: her claim is NOT VALID",  # cm³ ÷ 1 000
        V + "Number of mixtures = 1 206,53 ml ÷ 1 100 ml\n= 1,10\nLess than 2: her claim is NOT VALID",    # doubled twice
        V + "Number of mixtures = 550 ml ÷ 1 206,53 ml\n= 0,46\nLess than 2: her claim is NOT VALID"],     # upside down
        ["1 cm³ holds 1 ml.", "How many 550 ml mixtures fit in the bottle?"], after=["3.4"]),
    work("3.6", "The material used to make this bottle costs R0,20/cm². Determine the cost of making 1 water bottle. You may use the formula: "
         "SA = π × r(r + 2 × h), where π = 3,142.", 5, [
        "SA = 3,142 × 4 cm × (4 cm + 2 × 24 cm)\n= 653,54 cm²\nCost = R0,20 × 653,54\n= R130,71",       # the memo
        "SA = 3,142 × 4 cm × (4 cm + 2) × 24 cm\n= 1 809,79 cm²\nCost = R0,20 × 1 809,79\n= R361,96",   # the brackets misplaced
        "SA = 3,142 × 8 cm × (8 cm + 2 × 24 cm)\n= 1 407,62 cm²\nCost = R0,20 × 1 407,62\n= R281,52",   # the diameter for the radius
        "SA = 3,142 × 4 cm × (4 cm + 2 × 24 cm)\n= 653,54 cm²\nCost = 653,54 ÷ R0,20\n= R3 267,68"],     # divided by the price
        ["Put r = 4 cm and h = 24 cm into the formula.", "The material costs R0,20 for every cm²."], after=["3.4"])]

# ---- QUESTION 4, the question paper pages 6-7 and the memo page 5 ----
L3 = "Along the length: 65 ÷ 20 = 3,25 ≈ 3\nAlong the width: 65 ÷ 20 = 3,25 ≈ 3\n"
q41 = [
    term("4.1.1", "Name the tool needed to lift the car.", ["jack", "a jack", "car jack"],
         ["Look at pictures 3 to 5, under the car.", "It is placed under the car to raise it."], marks=2),
    match("4.1.2", "Write the step-by-step instructions from STEP 2 to STEP 5: match each step to its instruction.",
          ["Step 2", "Step 3", "Step 4", "Step 5"],
          ["Unscrew the nuts using the spanner", "Lift the car up with the jack", "Remove the flat tyre", "Put on the spare wheel",
           "Lower the car down", "Tighten the nuts"], [0, 1, 2, 3], 1,
          ["Look at what the hands do in each picture.", "The car goes up before the wheel comes off."]),
    answer("4.1.3", "Which step indicates that the car must be lowered down?", 2, ["Step 6", "Step 3", "Step 7", "Step 5"],
           ["Look for the arrow pointing down.", "The car comes down after the spare wheel is on."]),
    stmt("4.1.4", "It is recommended that the process of changing a tyre must be performed on a flat surface. Give a reason for this "
                  "recommendation.", 2,
         ["The car may roll if the surface is not flat.", "On a slope the jack can slip and the car can fall."],
         ["A flat surface makes the tyre go flat faster.", "The spare wheel only fits on a flat road.",
          "It is easier to see the nuts on a flat surface.", "A flat surface keeps the tyre cool."],
         ["What could happen to a raised car on a slope?", "Think of safety."], 2)]
q42 = [
    stmt("4.2.1", "Give a reason why there are arrows on these boxes.", 2,
         ["They show how to handle the box.", "They show which side of the box must face upwards."],
         ["They show the direction to push the box.", "They show that the box is empty.", "They show where to cut the box open.",
          "They show the box's weight."],
         ["The boxes hold glass bowls.", "Which way should a box of glass be kept?"], 2),
    work("4.2.2", "Connie claims that she can pack more than 18 small boxes in a big one. Verify, showing ALL calculations, whether her claim "
         "is VALID.", 7, [
        L3 + "Along the height: 55 ÷ 20 = 2,75 ≈ 2\nTotal = 3 × 3 × 2 = 18\nNot more than 18: her claim is NOT VALID",          # the memo
        "Along the length: 65 ÷ 20 = 3,25 ≈ 4\nAlong the width: 65 ÷ 20 = 3,25 ≈ 4\nAlong the height: 55 ÷ 20 = 2,75 ≈ 3\n"
        "Total = 4 × 4 × 3 = 48\nMore than 18: her claim is VALID",                                                             # rounded up
        "Big box: 65 × 65 × 55 = 232 375 cm³\nSmall box: 20 × 20 × 20 = 8 000 cm³\nNumber: 232 375 ÷ 8 000 = 29,05 ≈ 29\n"
        "Total = 29\nMore than 18: her claim is VALID",                                                                         # volumes divided
        L3 + "Along the height: 55 ÷ 20 = 2,75 ≈ 3\nTotal = 3 × 3 × 3 = 27\nMore than 18: her claim is VALID"],                  # the height rounded up
        ["How many small boxes fit along each edge of the big box?", "Can part of a box fit? Round down."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Units of measurement", "marks": 8,
     "lead": "TABLE 1 below shows a list of concepts and units/symbols thereof (TABLE 1: CONCEPTS AND UNITS/SYMBOLS).", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Time", "marks": 4,
     "lead": "Dan wants to watch a movie. The movie starts at 21:00 and is 1 hour 45 minutes long.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Conversions", "marks": 2, "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Layout plans and scale", "marks": 17,
     "lead": "Morare Secondary is a boarding school. The school hostel has 12 identical blocks labelled A to L. Each room has 3 beds except "
             "room 07 which has 4 beds. Below is a layout of Block A of Morare Secondary School hostel.",
     "figure": P.fig("Q2.1", "A layout of Block A, scale 1 : 150: along the top, Room 07, a room labelled A, Room 03 and Room 01; a passage "
                             "in the middle with the toilets at its far left end and the entrance arrow on the right; along the bottom, the "
                             "bathroom, an unlabelled room (…), Room 04 and Room 02. Windows are on the outside walls."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Probability", "marks": 4, "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Volume and surface area", "marks": 21,
     "lead": "Connie found a healthy smoothie recipe on the internet. She must blend a medium-sized banana, an apple, a handful of blueberries "
             "and 1⅔ cups of milk. The mixture yields 550 ml of smoothie. Below is a bottle she uses to drink her smoothie.\n"
             "1 cup = 200 ml ; 1 000 ml = 1 000 cm³",
     "figure": P.fig("Q3", "A picture of the insulated water bottle with its lid, and a diagram of the bottle without the lid as a cylinder: "
                           "height H = 240 mm, diameter = 8 cm."), "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Assembly instructions", "marks": 10,
     "lead": "The diagram below shows steps on how to change a car's flat tyre.",
     "figure": P.fig("Q4.1", "Seven numbered pictures: 1, a man takes the spare wheel out of the boot; 2, a spanner on a wheel nut; 3, a jack "
                             "under the raised car; 4, the flat wheel being pulled off; 5, the spare wheel being put on; 6, the car with a "
                             "downward arrow; 7, a man kneeling, tightening the nuts."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Packaging", "marks": 9,
     "lead": "Connie makes glass bowls and sells them to local stores. She packs ONE bowl in a small box with the dimensions 20 cm × 20 cm × "
             "20 cm. During distribution to local stores, she packs the small boxes in a bigger one (65 cm × 65 cm × 55 cm). The diagram "
             "below shows the dimensions of each box.",
     "figure": P.fig("Q4.2", "A big box 65 cm × 65 cm × 55 cm high and a small box 20 cm × 20 cm × 20 cm, each with a large arrow printed on "
                             "its side pointing up."), "items": q42}]

P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P2", "sitting": "November 2024", "total_marks": 75,
          "time": "1 hour 30 minutes"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.2", "kind": "memo_issue", "detail": "The memo's 2.2 is 24/192 × 100 = 12,5 % ≈ 13 %: 192 is the matron's claim that 2.1.4 "
                                                       "proves wrong, and Block A holds 22 learners (6 × 3 + 4). With the memo's own 2.1.4 "
                                                       "numbers the probability is 22/264 = 8,33 % ≈ 8 %, the right option here."},
          {"n": "1.1", "kind": "no_fit", "detail": "Matching columns (1.1) and the tyre-changing steps (4.1.2, written instructions in the paper) "
                                                   "play as matches; the directions (2.1.3) as statements."}],
         {"1": 14, "2": 21, "3": 21, "4": 19}, 75, {"2.2": ["2.1.4"], "3.4": ["3.3"], "3.5": ["3.4"], "3.6": ["3.4"]},
         "Questions 1 to 4 (the whole paper)")
