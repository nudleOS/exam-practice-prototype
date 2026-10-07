"""Mathematical Literacy P2 Nov 2025, the whole paper (Questions 1 to 5), hand-transcribed into the catalogue format (as if Claude
had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the memo's
working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the transcription is
the source, kept in git (out/ is not). The question paper and the answer book are SCANS (no text layer): read from their page
images; the memo has a text layer, checked against its page images.

  python tools/ingest/transcribe_ml_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Mathematical Literacy P2 Nov 2025 Eng.pdf" "<...>/Mathematical Literacy P2 Nov 2025 MG Afr & Eng.pdf" --id ml-p2-2025-11 --from-json --answer-book "<...>/Mathematical Literacy P2 Nov 2025 Answer Book Eng.pdf"

The paper reads four ANNEXURES printed in the SPECIAL ANSWER BOOK: A (a route map), B (two floor plans) and C (a map) are cropped
from the answer book (figure source "answer_book"); D (a bookcase and its pieces) is printed SIDEWAYS on its page, so a crop would
lie on its side: its DIAGRAM 2 is typed as a table (missions 5.1 and 5.2) and its DIAGRAM 1 described in 5.1's extract.

How the memo's shapes map (Mathematical Literacy):
  matching a list of concepts to TABLE 1's definitions (A-J), or statements to pictures P-U -> match (2 or 1 marks a pair);
  "Write only the letter" of ONE right method/formula/piece -> mcq; a choice the paper names with no explanation (clockwise or
  anticlockwise, left/right) -> mcq; a word, a name, a seat number, a probability, a time -> term (a time or date in every common
  written form, all or nothing where the memo splits MA and A); "Name / Write down TWO ..." -> list, and a one-line reason the
  memo marks as a fact (the ground floor, a broken line) -> list of one; "Calculate / Determine / Convert" -> steps, each step ONE
  number the memo's method produces (unit in the label's brackets), the memo's SF/MA/C marks riding on the number they lead to;
  "Verify the statement" -> steps for the numbers, the memo's conclusion (VALID / INVALID / CORRECT, the O mark) folded into the
  last step; an explanation (O marks) -> rubric; "Draw a scaled diagram" -> draw with the memo's criteria (self-checked).
  A memo RANGE -> its centre with a tolerance covering it; the memo's NPR rule (no penalty for rounding if the first decimal is
  correct) widens the tolerance of a non-money answer that must be rounded to cover its one-decimal rounding.
Figure boxes are measured in PDF points (both scans 595.2 x 841.68) from the page images, set so that ingest's 1% pad keeps the
drawings and leaves out the "[Adapted from ...]" lines and the text around them, and checked on a contact sheet."""
import json
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad agent_ml_p2/ink.py, rows.py; [source, page, x0, y0, x1, y1] in points ("qp" paper, "ab" answer book)
    "1.3": ["qp", 5, 106.8, 145.3, 521.3, 341.9], "2.1": ["qp", 6, 105.0, 130.7, 516.5, 449.3],
    "2.2": ["ab", 4, 60.5, 162.0, 532.0, 676.5], "2.3": ["ab", 6, 50.5, 134.0, 553.5, 602.0],
    "3.1": ["qp", 8, 105.0, 235.3, 515.9, 503.0], "3.2": ["qp", 10, 105.0, 192.7, 516.5, 480.0],
    "4.1": ["ab", 10, 48.5, 160.0, 527.0, 731.2]}


def fig(name, caption):
    src, p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"source": "answer_book"} if src == "ab" else {})}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None, must=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {})}


term = lambda n, q, a, clues, marks=2, strict=False: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                      **({"strict": True} if strict else {})}
num = lambda n, q, a, tol, unit, clues, marks=2: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
lst = lambda n, q, count, pool, clues, marks: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
match = lambda n, q, left, right, a, each, clues, **kw: {"t": "match", "n": n, "marks": len(left) * each, "q": q, "clues": clues, "left": left,
                                                         "right": right, "a": a, **({"each": each} if each > 1 else {}), **kw}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


def times(hh, mm):
    """A clock time in the forms learners write it: 09:45, 9:45, 09h45, 9h45, with or without am."""
    return [f"{h}{sep}{mm}{am}" for am in ("", " am") for h in (f"{hh:02d}", str(hh)) for sep in (":", "h")]


# ---- QUESTION 1, the question paper pages 3-5 and the memo pages 3-4 ----
TABLE1 = ["The three-dimensional space that is occupied by a gas, liquid or solid substance",
          "Visual representation of the exterior sides of a building", "Diagram of a real-life object drawn to scale",
          "The region covered by the shape or object", "The result of speed, in km/h, multiplied by the time, in hours",
          "Distance around the outside of a shape", "Scale where one unit on the map represents 50 000 units in reality",
          "Shows the design and dimensions of the inside of a building, viewed from the top",
          "The area of all the faces of an object added together", "The result of speed, in km/h, divided by the time, in hours"]
q11 = [match("1.1", "Use TABLE 1 above and match an explanation or a definition with EACH of the concepts below. Write only the letter (A–J) next "
             "to the question numbers (1.1.1 to 1.1.5), e.g. 1.1.6 K.",
             ["1.1.1 Elevation plan", "1.1.2 Number scale", "1.1.3 Volume", "1.1.4 Distance", "1.1.5 Perimeter"], TABLE1, [1, 6, 0, 4, 5], 2,
             ["An elevation shows a building from the outside; a floor plan shows it from the top.",
              "Two definitions differ by one word (multiplied / divided): distance = speed × time."],
             heads=["CONCEPT", "TABLE 1: DEFINITIONS"])]
q12 = [
    rub("1.2.1", "State, in words, the arrival time of the flight using the 12-hour format.", 2, [
        "Quarter past two (1).", "In the afternoon (1).", "OR — Fifteen minutes after two (1).", "OR — In the afternoon (1)."],
        ["The flight lands at 14:15 on the 24-hour clock.", "In words: how many minutes past which hour, and which part of the day?"]),
    steps("1.2.2", "Only 33⅓% of the maximum number of passengers were on board this flight. Calculate the number of passengers on this flight.", 2,
          [("Number of passengers on this flight", 2, 63, 0.01, "Number of passengers = 33⅓% × 189 ✓MA = 63 ✓A (OR ⅓ × 189 ✓MA = 63 ✓A)")],
          ["33⅓% is the same as one third.", "Take that part of the maximum number of passengers, 189."]),
    mcq("1.2.3", "Write down which ONE of the methods below is the CORRECT method to calculate the speed in km/h of the aircraft. Write only the "
        "letter (A–C) next to the question number (1.2.3).", ["1 278 ÷ 14:15", "1 278 ÷ 2", "2 ÷ 1 278"], 1,
        ["Speed = distance ÷ time, with the time in hours.", "How long is the flight from 12:15 to 14:15?"]),
    term("1.2.4", "State which day of the week was 26 December 2024.", ["Thursday"],
         ["Start from Wednesday 8 January 2025 and count back.", "Seven days back is the same weekday: find 1 January, then 25 December."])]
q13 = [
    match("1.3.1", "Write down the letter (P–U) of the picture that matches EACH of the following statements:", [
        "(a) Cut out circles of the aerolite to be placed on both ends of the geyser.", "(b) Apply glue to the circular pieces of the aerolite.",
        "(c) The strips of aerolite are wrapped around the pipes.", "(d) Roll the aerolite around the lateral surface of the geyser.",
        "(e) Use duct tape to secure the aerolite around the lateral surface.", "(f) Attach the circular pieces of the aerolite to the geyser."],
        ["Picture P", "Picture Q", "Picture R", "Picture S", "Picture T", "Picture U"], [2, 3, 5, 0, 1, 4], 1,
        ["Read what each statement is DOING: cutting, gluing, wrapping, rolling, taping, attaching.",
         "Then find the picture showing that action: what is in the man's hands?"], heads=["STATEMENT", "PICTURE"]),
    mcq("1.3.2", "Choose ONE of the following formulae that can be used to calculate how much aerolite is needed for the total surface area of the "
        "geyser only. Write only the letter (A–D) next to the question number (1.3.2).",
        ["π × radius² × height + 2 × π × radius", "π × radius × height + length × width", "2 × π × radius × height + 2 × π × radius²",
         "½ base × height"], 2,
        ["A geyser is a cylinder: a curved side and two circular ends.", "Surface area adds the AREAS of all the faces: every term must be an area."]),
    steps("1.3.3", "The length of the geyser is 1,2 m. Convert this measurement to mm.", 2,
          [("Length of the geyser in millimetres (mm)", 2, 1200, 0.01, "Length of geyser = 1,2 m × 1 000 ✓MA = 1 200 mm ✓A")],
          ["1 m = 1 000 mm.", "To a smaller unit: multiply."])]

# ---- QUESTION 2, the question paper pages 6-7, ANNEXURES A and B (the answer book pages 4 and 6) and the memo pages 5-6 ----
q21 = [
    steps("2.1.1", "Determine the number of forward-facing passenger seats on this bus.", 2,
          [("Forward-facing passenger seats (seats)", 2, 77, 0.01, "Number of seats = 59 + 22 − 4 ✓MA = 77 seats ✓A. AO")],
          ["Each deck's seat total is printed above its plan.", "Compare each seat's drawing with the KEY's forward-facing seat: some face another way."]),
    term("2.1.2", "The seats are numbered according to the following numbering system:\n• A to F is for the lower deck.\n• G to V is for the upper "
         "deck.\n• The seats are numbered 1 to 4 from right to left if you are facing the back of the bus.\nWrite down the seat number which has "
         "the easiest access to the toilet.", ["F2"],
         ["The toilet is on the lower deck, next to row F.", "Face the back of the bus: the seats run 1 to 4 from your right."], strict=True),
    match("2.1.3", "Complete the following paragraph with the directions to move from seat C2 to seat J3 by using the words provided in the list "
          "below. Write only the word next to the question numbers (2.1.3(a) to 2.1.3(d)).\n\nMove forward towards the front set of stairs on "
          "your (a) … Use this set of stairs to get to the upper deck. Once on the upper deck, turn (b) … and you will find your seat on the "
          "(c) … in the (d) … row from the stairs.",
          ["(a) Move forward towards the front set of stairs on your …", "(b) Once on the upper deck, turn …",
           "(c) you will find your seat on the …", "(d) in the … row from the stairs."],
          ["aisle", "second", "left", "right", "first"], [3, 2, 0, 1], 1,
          ["Stand at C2 facing the front of the bus: which side are the front stairs on?",
           "Count the rows from where the stairs arrive on the upper deck."], heads=["PARAGRAPH", "WORDS"])]
q22 = [
    term("2.2.1", "Write down the name of the southern-most stop on this route.", ["Camps Bay", "Camps Bay (stop 14)", "Stop 14 Camps Bay"],
         ["The N arrow points up: south is down the map.", "Compare the numbered stops near the bottom edge; Bakoven is a label, not a stop."]),
    term("2.2.2", "Name the type of scale used on this map.", ["Bar scale", "Line scale", "Linear scale", "Graphic scale", "Graphical scale"],
         ["Look at the Scale in the bottom right corner.", "Is it written as a ratio (1 : 50 000), or drawn?"]),
    mcq("2.2.3", "State whether the bus will be driving in a clockwise or an anticlockwise direction from stop 11 to stop 18.",
        ["Clockwise", "Anticlockwise"], 0,
        ["Follow the numbers 11, 12, 13, 14 ... on the map.", "Picture a clock's hands over the map: do they turn the same way?"]),
    steps("2.2.4", "The distance of a round trip is 19,2 km. Use the given scale on the map to determine the map distance.", 5, [
        ("Length of the 500 m scale bar on the printed map (mm)", 1, 12.5, 0.55, "13 mm ✓A (accept 12 mm – 13 mm)"),
        ("Real distance of the round trip in metres (m)", 1, 19200, 0.01, "19,2 km = 19 200 m ✓C"),
        ("Map distance of the round trip (mm)", 3, 480, 19.25, "13 mm = 500 m ✓RT; map distance = 19 200 ÷ 500 × 13 ✓MCA = 499,2 mm ✓CA "
         "(OR 1,3 cm = 0,5 km: 19,2 km × 1,3 cm ÷ 0,5 km = 49,92 cm; OR the scale 1 : 38 461,53846: 19,2 km ÷ 38 461,53846 = 0,0004992 km "
         "= 499,2 mm). Accept 460,8 mm for 12 mm.")],
        ["The scale bar's printed length stands for 500 m (the caption gives it).", "Change 19,2 km to metres, then count how many 500 m lengths that is."])]
q23 = [
    mcq("2.3.1", "State whether the bathroom door opens to the (left/right) as you enter the bathroom.", ["Left", "Right"], 1,
        ["Stand in the dining room facing the bathroom door.", "Which side of the doorway is the door hinged on?"]),
    steps("2.3.2", "Convert the longer dimension of the living room to centimetres.", 5, [
        ("The feet of the longer dimension in centimetres (cm)", 3, 365.76, 0.005, "Longer dimension = 12'8\" ✓RT; length in cm: 12' × 30,48 ✓MCA "
         "= 365,76 cm ✓C"),
        ("The inches of the longer dimension in centimetres (cm)", 1, 20.32, 0.005, "8\" × 2,54 = 20,32 cm ✓C"),
        ("Longer dimension of the living room (cm)", 1, 386.08, 0.005, "Total = 365,76 + 20,32 = 386,08 cm ✓CA (OR (12 × 30,48 cm) + (8 × 2,54 cm) = 386,08 cm)")],
        ["Read the living room's two dimensions: which is the longer?", "Change the feet and the inches separately (the NOTE), then add."]),
    lst("2.3.3", "Write down TWO differences between Flat 1 and Flat 2.", 2, [["Living room", "Bedroom"], ["Balcony"]],
        ["Compare the room in the north-east corner of each flat.", "Look along the east wall of Flat 2."], 4),
    lst("2.3.4", "Give ONE possible reason why Flat 1 does not have a balcony.", 1, [["Ground floor"]],
        ["Which floor is Flat 1 on?", "A balcony stands out from an upper floor."], 2),
    rub("2.3.5", "Explain why there are no windows in the north- and south-facing walls of both plans.", 2, [
        "There must be more flats adjacent to it (2)."],
        ["The flats form part of a block of flats.", "What would a north or a south window look into?"], each=2)]

# ---- QUESTION 3, the question paper pages 8-11 and the memo pages 7-9 ----
q31 = [
    term("3.1.1", "Mrs Xulu took 3 hours and 27 minutes without any break to cut out the circles. She finished at 13:12. Determine the time at "
         "which Mrs Xulu started cutting out the circles.", times(9, 45) + ["Quarter to ten in the morning", "Quarter to ten"],
         ["Count back 3 hours from 13:12 first.", "Then take away the 27 minutes: borrow an hour if you need to."]),
    steps("3.1.2", "In Part A, there are seven rows of circles. The first row consists of one circle at the top and thereafter, each successive row "
          "has an additional circle added to complete the rest of the rows. Calculate the total number of circles in Part A.", 3,
          [("Total number of circles in Part A", 3, 28, 0.01, "Number = 1 + 2 + 3 + 4 + 5 + 6 + 7 ✓RT ✓MA = 28 ✓CA (OR 7(1 + 7) ÷ 2 = 7 × 4 = 28). AO")],
          ["Row 1 has 1 circle, row 2 has 2 circles ...", "Add the circles of all seven rows."]),
    steps("3.1.3", "Calculate, in cm², the area of Part A. You may use the following formula:\nArea of triangle = ½ base × height", 4, [
        ("Height of Part A in centimetres (cm)", 1, 24, 0.01, "Height in cm = 240 mm = 24 cm ✓C"),
        ("Area of Part A (cm²)", 3, 336, 0.01, "Area = ½(28 cm ✓RT × 24 cm) ✓SF = 336 cm² ✓CA (OR ½ × 280 mm × 240 mm = 33 600 mm² = 336 cm²)")],
        ["The base is given in cm (28 cm), the height in mm: convert first.", "Area = ½ × base × height."]),
    steps("3.1.4", "The area of Part B is 30 240 mm². The area of Part C is 1,6 times the area of Part B. Calculate, in mm², the total area of the "
          "cardboard template.", 5, [
        ("Area of Part C (mm²)", 2, 48384, 0.01, "Area of C = 30 240 mm² × 1,6 ✓MA = 48 384 mm² ✓CA"),
        ("Area of Part A in square millimetres (mm²)", 1, 33600, 0.01, "336 cm² = 33 600 mm² ✓C (CA from 3.1.3)"),
        ("Total area of the cardboard template (mm²)", 2, 112224, 0.01, "Total area = 48 384 mm² + 30 240 mm² + 33 600 mm² ✓MCA = 112 224 mm² ✓CA "
         "(OR in cm²: 302,4 + 483,84 + 336 = 1 122,24 cm² = 112 224 mm²)")],
        ["Part C = 1,6 × Part B.", "Part A from 3.1.3 is in cm², and 1 cm² = 100 mm²."])]
q315 = [
    steps("3.1.5", "Determine, as a percentage, the probability of randomly choosing a green circle or a red circle from the container.", 4, [
        ("Total number of circles in the container", 1, 74, 0.01, "9 + 7 + 28 + 8 + 22 = 74 ✓A"),
        ("Probability of a green or a red circle (%)", 3, 21.62, 0.025, "P = 16/74 ✓MA × 100% ✓MA ≈ 21,62% ✓CA (OR P(red) = 9/74 × 100% = 12,16%, "
         "P(green) = 7/74 × 100% = 9,46%; 12,16% + 9,46% = 21,62%)")],
        ["Add all the circles first: that is the bottom of the fraction.", "Green or red: add the green and the red circles for the top."])]
q32 = [
    steps("3.2.1", "Determine, in mm, the radius of the small circle if it is 4/7 of the radius of the large circle.", 2,
          [("Radius of the small circle (mm)", 2, 8, 0.01, "Radius of small circle = 4/7 × 14 mm ✓MA = 8 mm ✓A. AO")],
          ["Find one seventh of 14 mm first.", "Then take four of those sevenths."]),
    steps("3.2.2", "Calculate, rounded to the nearest mm, the circumference of the large circle. You may use the following formula:\n"
          "Circumference of circle = 3,142 × 2 × radius", 3, [
        ("Circumference of the large circle (mm)", 2, 87.976, 0.005, "Circumference = 3,142 × 2 × 14 mm ✓SF = 87,976 mm ✓CA"),
        ("Circumference rounded to the nearest mm (mm)", 1, 88, 0.01, "≈ 88 mm ✓R")],
        ["Use 3,142 as the formula says, and the radius of the LARGE circle.", "Nearest mm: look at the first decimal."]),
    steps("3.2.3", "Amanda decides to make 48 pairs of earrings using flower-patterned synthetic leather for the large circles. Both sides of the "
          "large circle are covered using synthetic leather, while the small circle is painted black.\n\nThe radius of one large circle is 1,4 cm."
          "\n\nThe synthetic leather is sold in rolls with a width of 1,37 m. Amanda buys 30 cm of the synthetic leather.\n\nShe states that after "
          "cutting the leather for ALL the large circles, the remaining synthetic leather will have an area of less than 3 000 cm².\n\nVerify her "
          "statement, showing ALL calculations. You may use the following formulae:\nArea of rectangle = length × width\n"
          "Area of circle = 3,142 × radius²", 9, [
        ("Area of the synthetic leather bought (cm²)", 3, 4110, 0.01, "Area of material = 30 cm × 137 cm ✓C ✓SF = 4 110 cm² ✓CA"),
        ("Area of leather for ALL the large circles, both sides (cm²)", 4, 1182.40, 0.01, "Total area of all circles = 3,142 × (1,4 cm)² ✓SF × 48 ✓MA "
         "× 2 × 2 ✓MA = 1 182,40 cm² ✓CA (OR one circle 3,142 × (1,4 cm)² = 6,15832 cm²; 48 × 2 = 96 circles, × 2 sides = 192; "
         "6,15832 cm² × 192 = 1 182,39744 cm²)"),
        ("Area of the remaining leather (cm²)", 2, 2927.60, 0.01, "Area of off-cuts = 4 110 cm² − 1 182,40 cm² = 2 927,60 cm² ✓CA. "
         "Her statement is CORRECT ✓O (2 927,60 cm² is less than 3 000 cm²)")],
        ["Work in cm: the roll is 1,37 m wide and she buys 30 cm of it.", "48 PAIRS of earrings, and BOTH sides of each large circle are covered."])]

# ---- QUESTION 4, the question paper pages 12-13, ANNEXURE C (the answer book page 10) and the memo pages 10-11 ----
q41 = [
    term("4.1.1", "Name the closest town directly west of Colesberg.", ["De Aar"],
         ["Find Colesberg, then move straight left (west) on the map.", "Which town do you reach first?"]),
    num("4.1.2(a)", "National roads are indicated with a number enclosed in a pentagon, e.g. a pentagon with 1. Write down how many different "
        "national roads are shown on this map.", 8, 0.01, "roads",
        ["Look for the numbers in pentagon shields.", "The same road can appear more than once: count each number once."]),
    lst("4.1.2(b)", "Name the towns found on the N12.", 2, [["Kimberley", "Kimberly"], ["Britstown"]],
        ["Find the 12 shields: there are two on the map.", "Follow the road through each shield to the nearest town."], 3),
    lst("4.1.3", "Hanover is a town in the Northern Cape, while Middelburg is a town in the Eastern Cape. Describe how the provincial borders are "
        "indicated on this map.", 1, [["Broken line", "Dotted line", "Dashed line"]],
        ["Hanover and Middelburg lie on either side of a border: what runs between them?", "Look at the kind of line, not its colour."], 2)]
ARRIVE = [f"{d}{j}{t}" if dfirst else f"{t}{j}{d}" for dfirst, joins in ((True, (" at ", " ")), (False, (" on ", " ")))
          for j in joins for d in ("16 June 2023", "16 June") for t in times(9, 25)]
q42 = [
    num("4.2.1", "Write down the number of months the bird spent in area A.", 17, 0.01, "months",
        ["From 13 January 2022 to 13 January 2023 is 12 months.", "Then count on to 13 June 2023."]),
    term("4.2.2", "Determine the bird's date and time of arrival at area E.", ARRIVE,
         ["19:00 to midnight is 5 hours: how much flying time is left?", "After midnight it is the next day."], marks=3),
    term("4.2.3", "Write down the probability that the bird flew directly over Queenstown.", ["0", "0%", "Impossible", "Zero"],
         ["Find Queenstown and the flight line on the map.", "Does the line pass over it?"]),
    steps("4.2.4", "The flight from area B to area E is 770 km. Calculate (in km/h) the average speed of the bird as it flew from area B to area E. "
          "You may use this formula: Distance = speed × time", 4, [
        ("Flying time in hours (h)", 1, 14.4167, 0.02, "14 hours 25 min = 14,4166… hours ✓C"),
        ("Average speed of the bird (km/h)", 3, 53.41, 0.065, "770 km = speed × 14 hours 25 min ✓SF; speed = 770 km ÷ 14 hours 25 min ✓S "
         "= 770 km ÷ 14,4166… hours ≈ 53,41 km/h ✓CA")],
        ["Change the 25 minutes to hours: divide by 60.", "Speed = distance ÷ time."]),
    steps("4.2.5", "The direct distance between area B and area E is 311,72 miles. The person tracking the bird's GPS stated that the bird flew an "
          "extra distance of 268,13 km when compared to the direct distance.\n1 mile = 1,60934 km\nVerify, with calculations, whether this "
          "statement is VALID.", 5, [
        ("Direct distance in kilometres (km)", 2, 501.6635, 0.04, "311,72 miles × 1,60934 km ✓MA = 501,6634… km ✓A"),
        ("Extra distance the bird flew (km)", 3, 268.3365, 0.04, "Extra distance = 770 km − 501,6634… km ✓MCA = 268,336… km ✓CA. INVALID ✓O "
         "(OR total distance = 501,6634… km + 268,13 km ✓MCA = 769,7934… km ✓CA, not 770 km: INVALID ✓O)")],
        ["Change the miles to km first: multiply by 1,60934.", "The bird flew 770 km: how much more is that than the direct distance?"]),
    steps("4.2.6", "The biggest flamingo is 59 inches tall, which is approximately 5 feet. Some interesting facts about a country where flamingos "
          "are common:\n• Approximately 10% of this country's women are shorter than 5 feet.\n• Women make up 50% of this country's population.\n"
          "• This country has a total population of 333 million people.\n• 78% of this country's population are adults.\nCalculate, rounded to "
          "the nearest million, the number of adult women shorter than 5 feet in this country.", 5, [
        ("Number of adults (million)", 1, 259.74, 0.005, "Number of adults = 78% × 333 million ✓MA = 259,74 million"),
        ("Number of adult women (million)", 1, 129.87, 0.005, "Number of adult women = 50% × 259,74 million ✓MA = 129,87 million"),
        ("Adult women shorter than 5 feet (million)", 2, 12.987, 0.015, "10% × 129,87 million ✓MA = 12,987 million ✓CA"),
        ("Rounded to the nearest million (million)", 1, 13, 0.01, "≈ 13 million ✓R (OR women first: 50% × 333 000 000 = 166 500 000; adults "
         "78% × 166 500 000 = 129 870 000; 10% × 129 870 000 = 12 987 000 ≈ 13 000 000)")],
        ["Take the percentages one after another: 78% of everyone, then 50% of those, then 10%.", "Work in millions, and round only at the end."])]

# ---- QUESTION 5, the question paper pages 14-15, ANNEXURE D (the answer book page 14, typed) and the memo pages 12-15 ----
LETTERS = ["A", "B", "C", "D", "E", "F", "G"]
PICK = "Choose the letter (A–G) in DIAGRAM 2 that matches the item in DIAGRAM 1 given below. Write down only the letter next to the question number.\n"
q51 = [
    term("5.1.1(a)", PICK + "(a) Shelf", ["F", "G", "F or G"],
         ["The shelves are fitted in between the side pieces.", "So a shelf is slightly shorter than the top and bottom pieces (60 cm)."]),
    mcq("5.1.1(b)", PICK + "(b) Back of bookcase", LETTERS, 2,
        ["The back is not made of wood.", "Which piece in DIAGRAM 2 is hardboard?"]),
    term("5.1.2", "Write down the probability of randomly placing a book on a shelf with a height greater than 30 cm.",
         ["1/3", "0,333", "33,3%", "0,33", "33,33%", "One third", "1 out of 3", "1 in 3"],
         ["Count the spaces between the shelves and read their heights.", "Probability = the spaces higher than 30 cm ÷ all the spaces."]),
    rub("5.1.3(a)", "The back of the bookcase is made out of hardboard. Explain why the dimensions of the hardboard is 60 cm by 90 cm.", 2, [
        "The length of the bookcase is 60 cm and the height of the bookcase is 90 cm (2).", "OR — It covers the entire back of the bookcase (2)."],
        ["Compare 60 cm and 90 cm with DIAGRAM 1.", "Which part of the bookcase does the hardboard close?"], each=2),
    draw("5.1.3(b)", "The back of the bookcase is made out of hardboard. Draw a scaled diagram of the hardboard according to scale 1 : 20.", 6, [
        ["Uses the scale: width = 60 cm ÷ 20 (MA)", 1], ["Width = 3 cm (A)", 1], ["Height = 90 cm ÷ 20 = 4,5 cm (CA)", 1],
        ["The width drawn 3 cm long (CA)", 1], ["The height drawn 4,5 cm long (CA)", 1], ["The shape: a rectangle (CA)", 1]],
        ["Divide each real measurement by 20.", "Draw a rectangle with those two sides and label them."],
        memo="Dimensions: width = 60 cm ÷ 20 = 3 cm; height = 90 cm ÷ 20 = 4,5 cm; a rectangle 3 cm wide and 4,5 cm high, its sides labelled.")]
q52 = [
    steps("5.2", "Determine the area of the remaining part of the wood after cutting the required material. You may use the following formula:\n"
          "Area of rectangle = length × breadth", 6, [
        ("Area of the complete piece of wood (cm²)", 2, 18060, 0.01, "Area of complete piece of wood = 42 cm × 430 cm ✓SF = 18 060 cm² ✓A"),
        ("Area of the wooden pieces for ONE bookcase (cm²)", 2, 8240, 0.01, "= (90 + 60 + 56) cm × (20 + 20) cm ✓MA = 8 240 cm² ✓CA (OR E & D: "
         "60 cm × 20 cm × 2 = 2 400 cm²; F & G: 56 cm × 20 cm × 2 = 2 240 cm²; A & B: 90 cm × 20 cm × 2 = 3 600 cm²; total 8 240 cm²)"),
        ("Area of the remaining wood (cm²)", 2, 1580, 0.01, "Area of unused wood = 18 060 − 2(8 240) ✓MCA = 1 580 cm² ✓CA (OR one bookcase's "
         "pieces laid end to end: 2(90) + 2(60) + 2(56) = 412 cm; 430 − 412 = 18 cm left; 18 cm × 40 cm + 2 × 430 = 1 580 cm²)")],
        ["One bookcase needs the six pieces in DIAGRAM 2, each 20 cm wide.", "Two bookcases: take twice their area from the whole piece."])]
q53 = [
    steps("5.3", "Simon states that it will take more than three months to accumulate one ton of unused wood. Verify his statement, showing ALL "
          "calculations. You may use the following formula:\nDensity = mass ÷ volume", 6, [
        ("Volume of unused wood per month (cm³)", 1, 400000, 0.5, "Volume of wood per month = 0,4 m³ × 100³ = 400 000 cm³ ✓C"),
        ("Mass of unused wood per month (kg)", 2, 300, 0.01, "Mass per month = 0,75 g/cm³ × 400 000 cm³ ✓MA = 300 000 g ÷ 1 000 = 300 kg ✓CA"),
        ("Months to accumulate one ton of unused wood (months)", 3, 3.33, 0.035, "1 ton = 1 000 kg ✓C; number of months = 1 000 kg ÷ 300 kg "
         "= 3,33 ✓CA. VALID ✓O (OR 0,3 ton a month × 3 = 0,9 ton < 1 ton; OR 1,2 m³ in 3 months = 900 kg < 1 000 kg: his statement is correct)")],
        ["1 m³ = 100 × 100 × 100 cm³.", "Mass = density × volume, and 1 ton = 1 000 kg."])]

FLIGHT = {"head": ["South African Airways", "Wednesday 8 January 2025"],
          "rows": [["Distance", "1 278 km"], ["Aircraft", "Boeing 737-800"], ["Codeshare", "NZ 3120"], ["Flight number", "SA332"],
                   ["Maximum number of passengers", "189"], ["Departure", "12:15 Cape Town"], ["Arrival", "14:15 Johannesburg"]]}
COLOURS = {"title": "TABLE 2: NUMBER OF CIRCLES PER COLOUR", "head": ["COLOUR OF CIRCLE", "NUMBER OF CIRCLES"],
           "rows": [["Red", "9"], ["Green", "7"], ["Gold", "28"], ["Dark denim", "8"], ["Mixed colour", "22"]]}
PIECES = {"title": "ANNEXURE D, DIAGRAM 2: HARDBOARD AND SIX PIECES OF WOOD TO ASSEMBLE A SINGLE BOOKCASE",
          "head": ["LETTER", "MATERIAL", "DIMENSIONS"],
          "rows": [["E", "Wood", "60 cm × 20 cm"], ["D", "Wood", "60 cm × 20 cm"], ["F", "Wood", "56 cm × 20 cm"], ["G", "Wood", "56 cm × 20 cm"],
                   ["A", "Wood", "90 cm × 20 cm"], ["B", "Wood", "90 cm × 20 cm"], ["C", "Hardboard", "(no dimensions shown)"]]}
BOOKCASE = ("ANNEXURE D, DIAGRAM 1: TOP, BOTTOM, SIDES AND SHELVES OF BOOKCASE AND HARDBOARD FOR THE BACK\n\nA drawing of the bookcase with its "
            "parts labelled TOP, SIDE, SHELVES and BOTTOM: 60 cm wide, 90 cm high and 20 cm deep. Two shelves divide the inside into three "
            "spaces, 27 cm, 27 cm and 32 cm high from the top down.\n\nNOTE:\n• The back of this bookcase is made of a thin hardboard.\n• The top "
            "and bottom pieces of wood extend right across the bookcase.\n• The shelves are fitted in between the side pieces, so they are "
            "slightly shorter than the top and bottom pieces.")
MAP_C = ("ANNEXURE C, a road map of the central interior of South Africa, north up (an arrow N at the top right). The flamingo's tracked flight "
         "is a line with arrows through five marked areas: A just north of Bloemfontein; B just west of Bloemfontein; south, east of Colesberg, "
         "to C beside Middelburg; south-east to D; east, north of Makhanda, then south past Port Alfred and west to E on the coast. Towns: "
         "Kimberley, Douglas, Bloemfontein, Botshabelo, Orania, Britstown, De Aar, Colesberg, Aliwal North, Hanover, Middelburg, Nieu-Bethesda, "
         "Graaff-Reinet, Queenstown (east of the flight line), Makhanda, Port Alfred. Britstown, De Aar and Colesberg lie in a west-to-east row. "
         "National road numbers in pentagons: 12 (north of Kimberley, and west of Orania towards Britstown), 8 (west and east of Bloemfontein), "
         "1, 6, 5, 10, 9 and 2. Provincial borders are broken (dotted) lines: south from Kimberley past Orania, east past Colesberg to Aliwal "
         "North, and between Hanover and Middelburg, on past Nieu-Bethesda and Graaff-Reinet.")
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Concepts and definitions", "marks": 10,
     "lead": "TABLE 1 below contains a list of statements and definitions of concepts used in Mathematical Literacy.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Flight times and speed", "marks": 8,
     "lead": "Shown below is the information regarding a South African Airways flight from Cape Town to Johannesburg.", "table": FLIGHT,
     "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Surface area and conversion", "marks": 10,
     "lead": "One way to save money during winter is to wrap the geyser and waterpipes with a geyser blanket. A geyser blanket is made of aerolite "
             "which can easily be cut.\n\nThe pictures below show the steps to wrap the geyser in aerolite.\n\nNOTE: Aerolite is insulating "
             "material that allows heat to stay in an object.",
     "figure": fig("1.3", "Six line drawings of a man wrapping a geyser, joined by arrows: P, Q, R along the top row from left to right, then down "
                   "to S, T, U along the bottom row from right to left. P: the man behind a geyser lying on its side, spreading a sheet over its "
                   "curved side. Q: he pulls a strip of tape around the sheet on the geyser. R: he kneels on a flat sheet and traces a circle "
                   "on it (a curved arrow beside him). S: he holds a small brush or tube over a round piece standing on its edge. T: he presses a "
                   "round piece against the end of the geyser. U: hands wrapping strips around a pipe."), "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Seating plan", "marks": 8,
     "lead": "The seating plan for a tourist bus that travels around Cape Town is shown below.",
     "figure": fig("2.1", "The seating plan of a double-decker bus seen from above, the front on the right. UPPER DECK, 59 SEATS: a back row of "
                   "five seats across the rear (left end, ROW V), then pairs of seats on both sides of an aisle forward to ROW G at the front; "
                   "stairs arrive in the middle and at the front right. LOWER DECK, 22 SEATS AND DRIVER SEAT: an open area at the rear (left), "
                   "then the toilet and the rear stairs, ROW F just in front of them, pairs of seats on both sides of the aisle (two narrow "
                   "hatched panels between them) forward to ROW A, then the front stairs and the driver seat at the front right. KEY: driver "
                   "seat, toilet, forward-facing seat (its back on the left), stairs."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Route map and scale", "marks": 11,
     "lead": "ANNEXURE A in the ANSWER BOOK shows a route map of a round trip and the 18 stops made by a tour bus.",
     "figure": fig("2.2", "ANNEXURE A, ROUTE MAP OF A ROUND TRIP AND THE 18 STOPS MADE BY THE TOUR BUS: a street map of Cape Town, north up (an "
                   "arrow N, top left). The route is a line through 18 numbered stops: 1 and 2 at the V&A Waterfront (top right), 3 at De "
                   "Waterkant, 4 to 12 in the city centre, then down to 13 at the Table Mountain Cableway (lower middle), 14 at Camps Bay (lower "
                   "left, above the label Bakoven), and up the Atlantic coast through 15, 16 (Sea Point), 17 and 18 (Green Point, top). The key: "
                   "1. Two Oceans Aquarium; 2. The Clock Tower; 3. CTICC; 4. Cape Town Tourism; 5. St George's Cathedral; 6. South African Museum; "
                   "7. Mount Nelson Hotel; 8. SA Jewish Museum; 9. District Six Museum; 10. Castle of Good Hope; 11. Gold Museum; 12. Jewel "
                   "Africa; 13. Table Mountain Cableway; 14. Camps Bay; 15. President Hotel; 16. Sea Point; 17. Winchester Mansions; 18. Green "
                   "Point Light House. Scale (bottom right): a bar labelled 500 m, printed 13 mm long on the A4 answer book (on a screen it "
                   "shows at another size)."), "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Floor plans", "marks": 15,
     "lead": "John lives in a flat in Cape Town. ANNEXURE B in the ANSWER BOOK shows the floor plans of two flats in John's block of flats. Flat 1 "
             "is on the ground floor and Flat 2 is on the first floor, which forms part of a block of flats.",
     "figure": fig("2.3", "ANNEXURE B, PLAN OF A GROUND-FLOOR FLAT AND A FIRST-FLOOR FLAT, north up (arrow N on the left). FLOOR PLAN OF FLAT 1: "
                   "two BEDROOMS 13'0\" x 10'0\" on the west side, with WINDOWS in the west wall; BATH 6'6\" x 5'0\" and KITCHEN 6'6\" x 7'8\" "
                   "along the north wall in the middle; DINING ROOM 13'4\" x 13'1\" in the middle; LIVING ROOM 12'8\" x 12'7\" in the north-east "
                   "corner, a window in its east wall; the STAIRS in the south-east corner. The bathroom door, in the bathroom's south wall, is "
                   "hinged on the east (right-hand) side of the doorway and swings into the bathroom. FLOOR PLAN OF FLAT 2: the same, except "
                   "that the north-east room is a BEDROOM 12'8\" x 12'7\" with a BALCONY along its east wall. No windows in the north or south "
                   "walls. NOTE: 22'6\" = 22 feet and 6 inches; 1 foot = 30,48 cm; 1 inch = 2,54 cm."), "items": q23},
    {"id": "3.1", "title": "Question 3.1", "kind": "Area and number patterns", "marks": 14,
     "lead": "Mrs Xulu used different recycled materials to make a tree decoration to hang on the wall, as shown in the picture below. She cut out "
             "different coloured circles to form the tree pattern.\n\nShe made a tree-shaped template using cardboard to form the backing for the "
             "coloured circles to be pasted on.\n\nThe template was made up of three sections: Part A, Part B and Part C.\n\nNOTE: Dimension of "
             "the base of the triangle in Part A = 28 cm",
     "figure": fig("3.1", "Left, PICTURE OF TREE DECORATION: a Christmas tree made of many small coloured circles, a star on top. Right, "
                   "MEASUREMENTS OF CARDBOARD TEMPLATE: a tree shape with a star on top, in three sections split by dashed lines: Part A, a "
                   "triangle at the top, 240 mm high (an arrow along its right side); Part B, a band below it; Part C, a wider band at the "
                   "bottom."), "items": q31},
    {"id": "3.1.5", "title": "Question 3.1.5", "kind": "Probability", "marks": 4,
     "lead": "Mrs Xulu placed all the coloured circles in a container as she cut them out.\n\nTABLE 2 below shows the number of circles and the "
             "specific colours that Mrs Xulu cut out.", "table": COLOURS, "items": q315},
    {"id": "3.2", "title": "Question 3.2", "kind": "Circles and area", "marks": 14,
     "lead": "Amanda Xulu, Mrs Xulu's daughter, makes circular-shaped earrings. She sells these earrings at the local flea market.\n\nThe radius of "
             "the large circle in the picture below is 14 mm.\n\nShown below is a picture of a pair of earrings and a diagram showing the circles "
             "of one earring.\n\nNOTE: Synthetic – not real",
     "figure": fig("3.2", "Left, PICTURE OF A PAIR OF EARRINGS: two earrings, each a small plain black circle hanging above a larger circle "
                   "covered in a leaf and flower pattern. Right, DIAGRAM OF THE CIRCLES OF ONE EARRING: a SMALL CIRCLE, and below it a LARGE "
                   "CIRCLE with its radius drawn and labelled 14 mm."), "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Reading a map", "marks": 9,
     "lead": "A flamingo (bird) was fitted with a Global Positioning System (GPS) tracking device.\n\nANNEXURE C in the ANSWER BOOK shows the map "
             "with the tracked flight of the flamingo, starting at point A and ending at point E.", "figure": fig("4.1", MAP_C), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Time, speed and conversions", "marks": 21,
     "lead": "On 13 January 2022, the flamingo was in area A on the map.\nOn 13 June 2023, it started moving southwards from area A, the starting "
             "point of tracking the bird, and followed the following path:\n• On 14 June, the flamingo spent the night at a small pan at area B.\n"
             "• On 15 June at 19:00, it flew non-stop for 14 hours and 25 minutes to arrive at area E, the end point.",
     "figure": fig("4.1", MAP_C), "items": q42},
    {"id": "5.1", "title": "Question 5.1", "kind": "Assembly diagrams and scale", "marks": 14,
     "lead": "Simon is a carpenter. He builds wooden bookcases using wooden pieces for shelves and the frame, and hardboard for the back.\n\nThe "
             "diagrams on ANNEXURE D in the ANSWER BOOK can be described as follows:\n• DIAGRAM 1: Shows wooden pieces for the top, bottom, sides "
             "and shelves of a bookcase, with hardboard for the back of the bookcase\n• DIAGRAM 2: Shows the hardboard (i.e. the back of the "
             "bookcase) and SIX pieces of wood, with dimensions, that will have to be cut out to assemble a single bookcase",
     "extract": BOOKCASE, "table": PIECES, "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Area of the offcuts", "marks": 6,
     "lead": "The wooden pieces for two identical bookcases are cut from ONE complete rectangular piece of wood which is 2 cm thick, 42 cm wide and "
             "430 cm long.", "table": PIECES, "items": q52},
    {"id": "5.3", "title": "Question 5.3", "kind": "Density and mass", "marks": 6,
     "lead": "The density of the wood is 0,75 g/cm³.\n\nA volume of approximately 0,4 m³ unused wood is accumulated each month.", "items": q53},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P2", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematical Literacy", "total": 150, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 5), hand-transcribed from the page images of the question "
                                                           "paper and the answer book (both scans, no text layer) and from the memo; no API call."},
        {"n": "1.3.1", "kind": "no_fit", "detail": "Statements matched to pictures P-U play as a match: the app letters its right column A-F, so each "
                                                   "item carries the picture's own letter ('Picture P'); the memo marks letters P-U."},
        {"n": "2.2.4", "kind": "no_fit", "detail": "The memo's first mark is for MEASURING the printed scale bar (13 mm; accept 12-13 mm). A phone "
                                                   "shows the map at another size, so the figure caption gives the printed length (measured on the "
                                                   "PDF: 36,7 pt = 12,9 mm) and the mark becomes a read-off. The map distance range 460,8-499,2 mm "
                                                   "plays as its centre 480 ± 19,25 (the memo's 499,2 mm is in the working)."},
        {"n": "2.1.2", "kind": "no_fit", "detail": "Terms the memo marks in parts play all or nothing: 2.1.2 (row 1 + seat 1), 3.1.1 (MA + A), "
                                                   "4.2.2 (MA + date + time) and 5.1.2 (numerator + denominator). A time or date is typed (09:45, "
                                                   "9h45, 9:45 am ...; 4.2.2 '16 June 2023 at 09:25' in its common written orders), never on a keypad."},
        {"n": "1.2.2", "kind": "no_fit", "detail": "Calculations play as steps: each step is the number the memo's method produces, its SF/MA/C marks "
                                                   "riding on that number. 'Verify the statement' parts (3.2.3, 4.2.5, 5.3) fold the memo's "
                                                   "conclusion (CORRECT / INVALID / VALID, the O mark) into the last step's number. The memo's NPR "
                                                   "rule (first decimal correct) widens the tolerance where an answer must be rounded (3.1.5, 4.2.4, "
                                                   "4.2.5, 4.2.6, 5.3); 4.2.4's speed also takes 53,47 km/h (CA from 14,4 h)."},
        {"n": "4.1.2(b)", "kind": "no_fit", "detail": "The two towns on the N12 play as a list of two, 1,5 marks each; the memo gives 2 for the first "
                                                      "correct town and 1 for the second."},
        {"n": "5.1.3(b)", "kind": "no_fit", "detail": "The scaled diagram of the hardboard is drawn on paper and self-checked against the memo's criteria."},
        {"n": "5.1", "kind": "no_fit", "detail": "ANNEXURE D is printed sideways on the answer book's page 14, so a crop would lie on its side: its "
                                                 "DIAGRAM 2 (the six pieces of wood and the hardboard) is typed as a table, shown on 5.1 and again on "
                                                 "5.2 (which needs its dimensions), and DIAGRAM 1 (the bookcase) is described in 5.1's extract."},
        {"n": "2.3.2", "kind": "memo_issue", "detail": "The memo's second method writes (12 × 30,48 cm) = 365,6 cm; it is 365,76 cm, as its first "
                                                       "method and its total 386,08 cm have."},
        {"n": "3.1.5", "kind": "memo_issue", "detail": "The memo's third method writes 7/74 = 0,945945…; it is 0,0945945… (its sum 0,216216… is right)."},
        {"n": "3.2.3", "kind": "memo_issue", "detail": "The memo's second method writes 4 110 − 1 182,439744; the area of the circles is "
                                                       "1 182,39744 cm² (its answer 2 927,60 cm² is right)."},
    ],
}
out = Path(__file__).parent / "out" / "ml-p2-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper, answer book and memo PDFs and their page "
                                                                       "images (no API call)",
                                                        "scope": "Questions 1 to 5 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
