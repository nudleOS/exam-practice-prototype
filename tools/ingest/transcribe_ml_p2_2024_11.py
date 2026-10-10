"""Mathematical Literacy P2 Nov 2024: every part playable from the question paper (115 of the paper's 150 marks), hand-transcribed into
the catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options,
marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API
call: the transcription is the source, kept in git (out/ is not). The question paper is a SCAN (no text layer): read from its page
images; the memo has a text layer, checked against its page images.

  python tools/ingest/transcribe_ml_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Mathematical Literacy P2 Nov 2024 Eng.pdf" "<...>/Mathematical Literacy P2 Nov 2024 MG Afr & Eng.pdf" --id ml-p2-2024-11 --from-json

The paper reads three ANNEXURES printed in an ADDENDUM that is not on disk: A (an aerial view of the camp) for 2.1.2-2.1.5, B (the
trail-run map and its elevation map) for 2.2 and C (a map of Australia and the trip plan) for 5.1. Those 35 marks wait for the
addendum; the paper totals the 115 marks that can be played. 5.3 says "refer to ANNEXURE C" but every part reads only TABLE 3.

The memo's shapes map as in Mathematical Literacy P2 Nov 2025 (transcribe_ml_p2_2025_11.py):
  matching concepts to TABLE 1's definitions (A-G) -> match (2 marks a pair); "Choose ... (A, B or C)" -> mcq; a name, a product, a
  duration, a probability read off a table, a simplified ratio -> term (every spelling the memo accepts; all or nothing where the memo
  splits the marks); a count read off a figure -> num; "Calculate / Determine / Convert" -> steps, each step ONE number the memo's
  method produces (unit in the label's brackets), the memo's SF/MA/RT/C marks riding on the number they lead to; "Verify" -> steps,
  the memo's conclusion (the O mark) folded into the last step; an explanation or a reason (A/O marks) -> rubric, each memo
  alternative one 2-mark point.
  A memo RANGE or two accepted methods -> a tolerance spanning them; the memo's NPR rule (no penalty for rounding if the first
  decimal is correct) widens the tolerance of an answer that must be rounded to cover its one-decimal rounding.
Figure boxes are measured in PDF points (the scan is 595.2 x 841.68) with ink profiles of the page (scratchpad ml2_24_tools/ink.py),
set so that ingest's 1% pad keeps each drawing and its frame and leaves out the "[Adapted from ...]" / "[Source: ...]" lines, the
text around it and the question's outer box; `inset` where a printed heading touches the crop's top-left corner (the page's Hide
button sits there). Checked on the rendered crops."""
import json
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # [page, x0, y0, x1, y1] in points (the question paper)
    "1.2": [3, 113.5, 458.6, 530.8, 580.0], "1.3": [4, 111.5, 125.2, 521.0, 510.5], "2.1.6": [5, 160.0, 503.0, 501.0, 653.5],
    "3.1": [7, 111.5, 228.6, 516.5, 402.8], "3.2": [8, 107.9, 264.2, 520.7, 412.0], "3.3": [9, 107.5, 127.0, 500.0, 306.0],
    "4.1": [10, 111.5, 162.5, 513.0, 418.5], "4.2": [11, 108.9, 113.6, 507.3, 474.0], "5.2": [12, 92.0, 528.0, 530.5, 681.5]}
INSET = {"1.2": 40, "1.3": 40, "2.1.6": 40, "3.1": 40, "3.2": 40, "3.3": 40, "4.1": 40, "4.2": 40}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"inset": INSET[name]} if name in INSET else {})}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking instructions that are NOT points: never scored, never shown. worth: each point's own marks where they differ.
def rub(n, q, marks, bullets, clues, each=None, must=None, notes=None, worth=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {}), **({"notes": notes} if notes else {}), **({"worth": worth} if worth else {})}


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


# ---- QUESTION 1, the question paper pages 3-4 and the memo pages 2-3 ----
TABLE1 = ["A measuring system using metres, litres and kilograms", "The amount of space occupied by an object",
          "A system measuring in inches, gallons and pounds", "The amount of space available to hold something",
          "The side of a building you see when you are facing south", "The side of a building you see when you are facing north",
          "The amount of space that is enclosed by the perimeter of an object"]
q11 = [match("1.1", "Use TABLE 1 above and match an explanation or a definition with EACH of the concepts below. Write only the letter (A–G) next "
             "to the question numbers (1.1.1 to 1.1.4), e.g. 1.1.5 H.",
             ["1.1.1 Capacity", "1.1.2 North elevation", "1.1.3 Imperial system", "1.1.4 Area"], TABLE1, [3, 4, 2, 6], 2,
             ["An elevation is named after the side of the building it shows: to see the north side, which way must you face?",
              "Capacity is the word used for containers such as bottles and tanks; area is measured in square units."],
             heads=["CONCEPT", "TABLE 1: EXPLANATIONS AND DEFINITIONS OF CONCEPTS"])]
q12 = [
    steps("1.2.1", "Convert 220 mm to metres.", 2,
          [("The width in metres (m)", 2, 0.22, 0.001, "220 mm ÷ 1 000 ✓MA = 0,22 m ✓A")],
          ["1 m = 1 000 mm.", "To a bigger unit: divide."]),
    mcq("1.2.2", "Choose, from the options (A, B or C) below, the correct one that could be used to calculate the volume of the hexagonal paving brick.",
        ["Volume = 6 × area of triangle × height", "Volume = side length + height + width", "Volume = 6 × perimeter × height"], 0,
        ["Volume = area of the top face × height.", "The top face is made up of 6 equal triangles: which option uses an AREA?"]),
    steps("1.2.3", "Calculate the number of bricks needed for a single row along a length of 2 860 mm.", 3,
          [("Number of bricks in the single row", 3, 13, 0.01, "Number of bricks = 2 860 mm ✓RT ÷ 220 mm ✓MA = 13 ✓A")],
          ["In THREE BRICKS IN A ROW, which dimension lies along the row?", "Divide the length of the row by that dimension."])]
q13 = [
    num("1.3.1", "Write down the total number of wooden items needed to assemble this chair.", 18, 0.01, "items",
        ["The # column gives how many of each item.", "Add the numbers of all the items in the material list."]),
    steps("1.3.2", "Determine the number of crosspieces found on the seats of THREE chairs.", 3, [
        ("Crosspieces on the seat of ONE chair", 1, 6, 0.01, "6 ✓RT"),
        ("Crosspieces on the seats of THREE chairs", 2, 18, 0.01, "Number of crosspieces = 6 × 3 ✓A = 18 ✓A")],
          ["Count the crosspieces across the SEAT only (not the back): the side view shows them as blocks.", "Then multiply by the number of chairs."]),
    term("1.3.3", "Name the item in the material list with the longest dimension.", ["Chair support", "Chair supports"],
         ["Each item's dimensions are given as thickness × width × length.", "Find the biggest of the lengths and read that item's name."]),
    num("1.3.4", "Identify which dimension of the chair support will represent the thickness of the wood.", 1.9, 0.01, "cm",
        ["Read the NOTE under the material list.", "Find the smallest of the chair support's three dimensions."]),
    steps("1.3.5", "Write down, in millimetres, the length of the spacing between the crosspieces of the back of the chair.", 2, [
        ("Spacing shown on the side view (cm)", 1, 1.27, 0.005, "1,27 cm ✓RT"),
        ("Spacing in millimetres (mm)", 1, 12.7, 0.01, "Space = 1,27 × 10 mm = 12,7 mm ✓MCA (NPU)")],
          ["The side view labels the spacing between the crosspieces of the chair back.", "1 cm = 10 mm."])]

# ---- QUESTION 2, the question paper page 5 and the memo pages 4-5 (2.1.2-2.1.5 and 2.2 read the ADDENDUM's ANNEXURES A and B) ----
q21 = [
    rub("2.1.1", "Explain what is meant by aerial view.", 2, [
        "View from the top (2).", "OR — View of the landscape from a certain height above ground like from a satellite or drone (2).",
        "OR — View from an elevated height (2).", "OR — Birds-eye view (2)."],
        ["The word 'aerial' comes from 'air'.", "Where would you have to be to see the whole camp like a map?"], each=2)]
q216 = [
    num("2.1.6(a)", "Write down the total number of showers.", 9, 0.01, "showers",
        ["Use the KEY: which symbol is a shower?", "Count those cubicles in the plan."]),
    steps("2.1.6(b)", "Determine, rounded to the nearest whole number, the scale of the plan.", 4, [
        ("Length of the plan measured on the printed page (mm)", 1, 90, 1.05, "90 mm ✓A (accept ± 1 mm deviation on the measurement)"),
        ("Actual length of the ablution facilities (mm)", 1, 8200, 0.01, "90 mm = 8,2 m; 8,2 m = 8 200 mm ✓C"),
        ("Scale before rounding, 1 : …", 1, 91.11, 1.03, "8 200 mm ÷ 90 ✓M = 91,11: 1 : 91,11 (OR 9 cm : 8,2 m = 9 cm : 820 cm = 1 : 91,11..)"),
        ("Scale rounded to the nearest whole number, 1 : …", 1, 91, 1.01, "1 : 91 ✓R (90 or 92 from a measurement of 91 mm or 89 mm)")],
          ["Measure the plan's length on the paper (the figure's caption gives it) and change 8,2 m to the same unit.",
           "Scale = 1 : actual length ÷ plan length; round to a whole number."]),
    rub("2.1.6(c)", "Give ONE suitable reason why benches are found in the ablution facilities.", 2, [
        "To allow people to sit while waiting for a toilet or shower to become available (2).",
        "OR — To place your clothes or belongings on while you are showering (2).",
        "OR — To sit while you change your outfit, or getting dressed or apply body lotion or for baby nappy change (2)."],
        ["Who uses the ablutions at a busy camp, and what might they have to wait for?", "What do you do with your clothes while you shower?"], each=2)]

# ---- QUESTION 3, the question paper pages 7-9 and the memo pages 7-11 ----
q31 = [
    term("3.1.1", "The school day ends at 12:55.\n\nTendani's father was late and only came to fetch him at 14:13.\n\nDetermine how long Tendani sat in "
         "the reading corner.", ["1 hour 18 minutes", "1 hour and 18 minutes", "1 hour 18 min", "1 hr 18 min", "1 hr 18 mins", "1 h 18 min",
                                 "1h18min", "1h18", "1 h 18", "1:18", "01:18", "78 minutes", "78 min", "78 mins", "1,3 hours", "1,3 h", "1,3 hrs"],
         ["From 12:55 to 13:00 is 5 minutes.", "Then count on from 13:00 to 14:13."]),
    steps("3.1.2", "The height of one pillow is 11 cm.\n\nDetermine the difference between the total height of the pillows in ONE bag and the height "
          "of the bag.", 4, [
        ("Total height of the pillows in ONE bag (cm)", 2, 44, 0.01, "Total height of 4 pillows = 11 cm × 4 ✓MA = 44 cm ✓CA"),
        ("Difference between the height of the bag and the pillows' total height (cm)", 2, 4, 0.01, "Difference = 48 cm ✓RT − 44 cm = 4 cm ✓CA "
         "(OR Difference = 48 cm − 11 cm − 11 cm − 11 cm − 11 cm = 4 cm). AO")],
          ["Count the pillows stacked in ONE bag in the picture.", "Add up their heights and compare with the bag's height."]),
    steps("3.1.3", "The piping around the bottom edge of some of the bags for the pillows needs to be replaced. The store sells the piping in half-metre "
          "lengths.\n\nCalculate the total length of piping she will have to purchase to replace the piping around the bottom edges of FOUR bags.\n\n"
          "You may use the following formula:\nPerimeter = 2 (length + width)", 5, [
        ("Perimeter of the bottom edge of ONE bag (cm)", 2, 152, 0.01, "Perimeter = 2 (46 cm + 30 cm) ✓SF = 2 (76 cm) = 152 cm ✓CA"),
        ("Piping for FOUR bags (cm)", 1, 608, 0.01, "Total length for 4 bags = 152 × 4 ✓MA = 608 cm"),
        ("Piping for FOUR bags in metres (m)", 1, 6.08, 0.005, "608 cm ÷ 100 = 6,08 m ✓C (OR in metres from the start: 2(0,3 m + 0,46 m) = "
         "1,52 m; 1,52 m × 4 = 6,08 m)"),
        ("Length of piping she must buy (m)", 1, 6.5, 0.01, "She must buy 6,5 m ✓R (OR ½ m = 50 cm; 608 cm ÷ 50 cm = 12,16 ≈ 13 half-metre lengths)")],
          ["The bottom edge of a bag is a rectangle 46 cm by 30 cm.", "Four bags, and the piping is sold only in half-metre lengths: round UP."])]
q32 = [
    steps("3.2.1", "Determine, in cm, the circumference of the circular wooden tag.\n\nYou may use the following formula:\n"
          "Circumference of a circle = 3,142 × diameter", 2,
          [("Circumference of the tag (cm)", 2, 25.136, 0.04, "Circumference = 3,142 × 8 cm ✓SF = 25,136 cm ✓A (NPR). AO")],
          ["The diameter of the tag is printed on the diagram.", "Use 3,142, as the formula says."]),
    steps("3.2.2", "Determine, in cm, the radius of ONE circular wooden tag.", 2,
          [("Radius of ONE tag (cm)", 2, 4, 0.01, "Radius = 8 cm ÷ 2 ✓MA = 4 cm ✓A (NPU). AO")],
          ["The radius runs from the centre of the circle to its edge.", "How does it compare with the diameter?"]),
    steps("3.2.3", "The hardware store sells paint in 50 mℓ, 1 litre, 5 litre and 20 litre containers.\n\nMrs Kgomo claims that a 50 mℓ can of paint "
          "will be sufficient to paint ONE side of 36 circular wooden tags.\n\nVerify her statement. Show ALL calculations.\n\nUse the following "
          "formula:\nArea of a circle = 3,142 × radius²", 9, [
        ("Area of the front of ONE tag, hole included (cm²)", 3, 50.272, 0.005, "Area of a circle = 3,142 × (4 cm)² ✓SF = 3,142 × 16 cm² ✓MCA "
         "= 50,272 cm² ✓CA (CA from 3.2.2)"),
        ("Area to be painted on ONE tag (cm²)", 1, 49.9578, 0.005, "Area = 50,272 − 0,3142 = 49,9578 cm² ✓CA"),
        ("Area to be painted on ONE side of the 36 tags (cm²)", 1, 1798.4808, 0.09, "Total area = 36 × 49,9578 cm² = 1 798,4808 cm² ✓MCA"),
        ("Area to be painted on the 36 tags in square metres (m²)", 1, 0.179848, 0.0005, "Total area in m² = 1 798,4808 ÷ 100² = 0,179848 m² ✓C"),
        ("Paint needed for the 36 tags (mℓ)", 3, 29.97468, 0.035, "Paint: 6 m² with 1 ℓ, so 0,17984808 m² with n ℓ: n = 0,17984808 ÷ 6 ℓ ✓MCA "
         "= 0,02997466 ℓ ≈ 30 mℓ ✓CA: VALID ✓O (OR 6 m² = 1 ℓ = 1 000 mℓ, so 50 mℓ paints 0,3 m² ✓MA; 0,3 m² > 0,179848 m² ✓CA: 50 mℓ will be "
         "more than sufficient ✓O; OR 6 m² : 1 ℓ = 60 000 cm² : 1 000 mℓ; paint for one tag = 49,9578 × 1 000 ÷ 60 000 = 0,83263 mℓ; × 36 = "
         "29,97 mℓ: VALID)")],
          ["Area to paint on one tag = the tag's area minus the hole's area.", "6 m² per litre: change cm² to m² (÷ 10 000) and find the mℓ for 36 tags."])]
q33 = [
    steps("3.3.1", "The volume of the cubic-shaped packet is 2 744 cm³.\n\nCalculate the side length of the cubic-shaped packet.\n\nYou may use the "
          "following formula:\nVolume of a cube = side × side × side", 4,
          [("Side length of the packet (cm)", 4, 14, 0.01, "2 744 cm³ = side × side × side ✓SF ✓SF; (side)³ = 2 744 cm³ ✓MA; 14 × 14 × 14 = 2 744; "
            "Side = 14 cm ✓CA")],
          ["Which number multiplied by itself three times gives 2 744?", "Use the cube root key, or try whole numbers between 10 and 20."])]
q332 = [
    steps("3.3.2", "Determine the probability, as a decimal, of randomly choosing a pink or a yellow sweet from the packet.", 3, [
        ("Number of sweets that are pink or yellow", 1, 15, 0.01, "8 + 7 = 15 ✓A"),
        ("Number of sweets in the packet", 1, 35, 0.01, "35 ✓A"),
        ("Probability, as a decimal", 1, 0.43, 0.03, "P = 15/35 = 0,42857… ≈ 0,43 ✓CA (OR P = 8/35 + 7/35 = 0,22857… + 0,2 = 0,42857… ≈ 0,43). NPR")],
          ["Add the pink and the yellow sweets.", "Divide by all the sweets in the packet, and write it as a decimal."])]

# ---- QUESTION 4, the question paper pages 10-11 and the memo pages 12-15 ----
q41 = [
    term("4.1.1", "Identify the crude oil product that will be third to boil.",
         ["Kerosene", "Lamp oil", "Kerosene (lamp oil)", "Kerosene or lamp oil"],
         ["The lower its boiling temperature, the sooner a product boils.", "Order the products from the lowest temperature: which is third?"]),
    term("4.1.2", "Write down the product extracted at 150 °C.", ["Gasoline", "Petrol", "Gasoline (petrol)", "Gasoline or petrol"],
         ["Find 150 °C on the tower.", "Follow the extractor pipe below that section to the product's name."]),
    steps("4.1.3", "Convert the boiling point of diesel to degrees Fahrenheit.\nUse the formula: °C = (°F − 32)/1,8", 4, [
        ("Boiling point of diesel (°C)", 1, 300, 0.01, "300 °C ✓RT"),
        ("Boiling point of diesel in degrees Fahrenheit (°F)", 3, 572, 0.01, "300 °C = (°F − 32)/1,8 ✓SF; °F = 1,8 × 300 + 32 ✓S = 572 ✓CA. AO")],
          ["Read the temperature at which diesel is extracted.", "Put it in place of °C and solve for °F: multiply by 1,8, then add 32."]),
    steps("4.1.4", "The pipes leading in and out of the vertical, cylindrical tower take up 2,5% of the surface area of part B of the cylindrical tower."
          "\n\nCalculate the total surface area of the vertical, cylindrical tower, excluding the area taken up by the pipes.\n\nUse the formula:\n"
          "Surface area of an open cylinder = 3,142 × diameter × height", 7, [
        ("Surface area of part B (m²)", 2, 1018.008, 0.005, "Surface area of an open cylinder = 3,142 × 6 m × 54 m ✓SF = 1 018,008 m² ✓CA"),
        ("Area taken up by the pipes (m²)", 2, 25.4502, 0.005, "Area of pipes = 2,5/100 × 1 018,008 ✓MCA = 25,4502 m² ✓CA"),
        ("Total surface area of the tower, excluding the pipes (m²)", 3, 1143.3738, 0.03, "Total surface area = 1 018,008 m² − 25,4502 m² ✓MCA "
         "+ 150,816 m² ✓MA = 1 143,3738 m² ✓CA (OR excluding the pipes: 97,5/100 × 1 018,008 = 992,5578 m²; 992,5578 m² + 150,816 m² = "
         "1 143,3738 m²). NPR")],
          ["Part B is an open cylinder 6 m wide and 54 m high: use the formula.", "Take away 2,5% of part B for the pipes, then add the area of "
           "A + C from the NOTE."])]
q42 = [
    steps("4.2.1", "Determine the total number of pallets of bricks needed to replace both garage doors.", 5, [
        ("Bricks in one row of the double-brick wall", 2, 19.5, 0.55, "19 ✓✓RT (OR one single row 10 bricks ✓RT, 20 rows high ✓RT)"),
        ("Bricks for ONE garage door", 1, 390, 10.5, "Number of bricks for 1 garage door = 19 × 20 ✓A = 380 (OR single line wall = 20 × 10 = 200 "
         "bricks; double line wall = 2 × 200 = 400 bricks ✓CA)"),
        ("Bricks for BOTH garage doors", 1, 780, 20.5, "Total number of bricks needed = 380 × 2 ✓MCA = 760 (OR 2 × 400 = 800 ✓MCA)"),
        ("Pallets of bricks needed", 1, 2, 0.01, "2 pallets of bricks ✓R")],
          ["Count the bricks in one row and the rows up the wall; the side view shows the wall is two bricks thick.",
           "There are two doors, and bricks are sold only in whole pallets of 525."]),
    steps("4.2.2", "The opening of a garage door has dimensions of 2,13 m × 3 m.\n\nOther costs to build the double-brick wall:\n• Material, other "
          "than bricks, cost R2 000,00\n• Labour is R500,00 per square metre\n\nThe owner states that the total cost to replace both garage doors "
          "with walls would be R15 200,00.\n\nVerify her statement by means of calculations.\n\nYou may use the following formula: Area = length × width", 7, [
        ("Area of the openings of BOTH garage doors (m²)", 3, 12.78, 0.005, "Area of 2 doors = 2 ✓MA × 2,13 × 3 ✓SF = 12,78 m² ✓A (OR one door: "
         "2,13 m × 3 m = 6,39 m²)"),
        ("Labour cost (R)", 1, 6445, 55.01, "Labour cost = 12,78 m² × R500 = R6 390 ✓CA (OR for one door R3 195, for two R6 390; OR 12,78 m² ≈ "
         "13 m² (cost per m²): 13 × R500 = R6 500 ✓CA)"),
        ("Cost of the bricks (R)", 1, 6772.50, 0.005, "Brick cost = 2 × 525 × R6,45 = R6 772,50 ✓CA (CA pallets from 4.2.1)"),
        ("Total cost to replace both garage doors (R)", 2, 15217.50, 55.01, "Total cost = R2 000 + R6 390 + R6 772,50 = R15 162,50 ✓CA: Not VALID ✓O "
         "(OR R6 500 + R6 772,50 + R2 000 = R15 272,50 ✓CA: Not VALID ✓O)")],
          ["Area of both openings = 2 × length × width; labour is R500 per square metre.",
           "Bricks: the pallets from 4.2.1 × 525 × R6,45; add the R2 000 material and compare with R15 200."]),
    rub("4.2.3", "Give ONE suitable reason why the bricks have to be placed on a wooden pallet.", 2, [
        "To be easily lifted by a fork lift (2).", "OR — Storage / loading / transportation are made easier (2).", "OR — It keeps them from breaking (2).",
        "OR — It makes counting easier (2).", "OR — To protect the bricks from damage (2).", "OR — To keep it tight and compact (2)."],
        ["How is a heavy stack of bricks moved from a truck to a building site?", "What could happen to loose bricks stacked on the ground?"], each=2)]

# ---- QUESTION 5, the question paper pages 12-13 and the memo pages 16-17 (5.1 reads the ADDENDUM's ANNEXURE C) ----
q52 = [
    steps("5.2.1", "Determine, rounded to THREE decimal places, the conversion factor from feet to metres used in this diagram, in the form "
          "1 foot = … m.", 3, [
        ("Height of Uluru in feet (feet)", 1, 1142, 0.01, "1 142 feet ✓RT"),
        ("Height of Uluru in metres, from the diagram (m)", 1, 348, 0.01, "= 348 m ✓RT"),
        ("Conversion factor rounded to THREE decimal places: 1 foot = … m", 1, 0.305, 0.0004, "1 foot = 348/1 142 = 0,304728546; 1 foot ≈ 0,305 m ✓A")],
          ["Uluru's height is given in feet in the text and in metres on the diagram.", "1 foot = metres ÷ feet; round to three decimal places."]),
    term("5.2.2", "Write, as a simplified ratio, the heights of Uluru : Eiffel Tower : Big Ben.", ["29 : 27 : 8", "29:27:8"],
         ["Read the three heights in metres, in the order the question asks.", "Divide all three by their highest common factor."], marks=4, strict=True)]
q53 = [
    term("5.3.1", "A meteorite (rock from the sky) fell somewhere in Australia.\n\nWrite down the probability that it randomly fell in Queensland.",
         ["22,5%", "22,5", "22,50%", "0,225", "0,2250", "0,224986", "0,22499", "22,4986%", "1 729 742/7 688 220", "1 729 742 ÷ 7 688 220"],
         ["The chance of landing in a state depends on its share of the total area.", "TABLE 3 gives each state's percentage of the total area."]),
    steps("5.3.2", "Show, with calculations, why it could be stated that the total area of the islands of Australia is approximately half of the area "
          "of the mainland area of Tasmania.", 3, [
        ("Total area of the islands of Australia (km²)", 1, 32159, 0.01, "32 159 ✓RT"),
        ("Mainland area of Tasmania (km²)", 1, 64519, 0.01, "64 519 ✓RT"),
        ("Islands' area as a fraction of Tasmania's mainland area (a decimal)", 1, 0.4984, 0.0017, "Area of island = 32 159/64 519 = 0,498 ≈ 0,5 ✓CA "
         "(OR half of Tasmania = 64 519 × ½ = 32 259,5 km², islands = 32 159 km²; OR 64 519 : 32 159 ≈ 2 : 1)")],
          ["Find the islands' TOTAL and Tasmania's MAINLAND area in TABLE 3.", "Divide the islands' area by Tasmania's mainland area: how close is it to ½?"]),
    steps("5.3.3(a)", "The Australian Capital Territory has a population of 454 499.\n\nDetermine, rounded to the nearest whole number, the population "
          "density of the Australian Capital Territory as people per square km.", 3, [
        ("Population density before rounding (people per km²)", 2, 192.7476, 0.05, "Population density = 454 499 ✓RT ÷ 2 358 ✓RT = 192,74…"),
        ("Population density rounded to the nearest whole number (people per km²)", 1, 193, 0.01, "≈ 193 ✓R")],
          ["Population density = number of people ÷ area.", "Use the Australian Capital Territory's total area in TABLE 3; round to a whole number."]),
    steps("5.3.3(b)", "The Australian Capital Territory has a population of 454 499.\n\nGive a suitable reason, with calculations, why this area is "
          "omitted from the percentage calculation in the table.", 4, [
        ("The Australian Capital Territory's area as a percentage of the total area (%)", 3, 0.03067, 0.0008, "Land % area = 2 358 ✓RT ÷ "
         "7 688 220 ✓RT × 100% = 0,0306..% ✓CA"),
        ("That percentage rounded to one decimal place, as in the table (%)", 1, 0, 0.01, "Rounds off to zero ✓O")],
          ["Work out its share of Australia's total area as a percentage.", "Compare the size of that percentage with the others in the table."])]

MATERIALS = {"title": "MATERIAL LIST", "head": ["#", "Wooden Item", "Dimensions (in cm)"],
             "rows": [["4", "Chair supports", "1,9 × 3,8 × 66"], ["13", "Crosspieces", "1,9 × 3,8 × 36"], ["1", "Seat back, bottom crosspiece", "1,9 × 3,8 × 32"]],
             "after": "NOTE:\n• The thickness of the wood is the smallest dimension.\n• # is the number of item(s)."}
SWEETS = {"title": "TABLE 2: NUMBER OF SWEETS PER COLOUR", "head": ["COLOUR OF SWEETS", "NUMBER OF SWEETS"],
          "rows": [["Blue", "4"], ["Purple", "5"], ["Pink", "8"], ["Orange", "11"], ["Yellow", "7"]]}
AREAS = {"title": "TABLE 3: AREA SIZES OF THE MAINLAND, ISLANDS AND TOTAL FOR EACH STATE OR TERRITORY",
         "head": ["STATE/TERRITORY", "MAINLAND AREA km²", "ISLAND AREA km²", "TOTAL AREA km²", "PERCENTAGE OF TOTAL AREA"],
         "rows": [["Western Australia", "2 526 924", "3 089", "2 527 013", "32,9"], ["Queensland", "1 723 030", "6 712", "1 729 742", "22,5"],
                  ["Northern Territory", "1 334 404", "13 387", "1 347 791", "17,5"], ["South Australia", "979 651", "4 670", "984 321", "12,8"],
                  ["New South Wales", "801 137", "13", "801 150", "10,4"], ["Victoria", "227 038", "406", "227 444", "3,0"],
                  ["Tasmania", "64 519", "3 882", "68 401", "0,9"], ["Australian Capital Territory", "2 358", "–", "2 358", "–"],
                  ["TOTAL (AUSTRALIA)", "7 656 061", "32 159", "7 688 220", "…"]],
         "after": "NOTE: Territory – a big area that compares to a district or province"}
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Measurement concepts", "marks": 8,
     "lead": "TABLE 1 below contains a list of explanations and definitions of concepts used in Mathematical Literacy.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Hexagonal paving bricks", "marks": 7,
     "lead": "Paving bricks are available in different shapes and sizes. Hexagonal paving bricks are made up of 6 equal triangles and will be used to "
             "cover a rectangular ground surface.",
     "figure": fig("1.2", "A table of three panels. SKETCH OF A HEXAGONAL PAVING BRICK: a six-sided brick drawn in 3D, its top divided into 6 equal "
                   "triangles by dashed lines from corner to corner; arrows mark L (one side), W (across the top, through the centre) and H (the "
                   "brick's thickness). DIMENSIONS OF THE PAVING BRICK: Equal side lengths (L) = 90 mm; Height (H) = 50 mm; Width (W) = 220 mm. "
                   "THREE BRICKS IN A ROW: three dark hexagons side by side, flat side against flat side, the first marked W from its left "
                   "edge to its right edge."), "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Fold-up chair", "marks": 11,
     "lead": "The fold-up chair is a beach chair that folds into itself. A 3D sketch, a side view, a material list, the assembled chair and a folded-up "
             "chair are shown below.", "table": MATERIALS,
     "figure": fig("1.3", "3D SKETCH OF FOLD-UP CHAIR: a slatted wooden beach chair: two chair supports crossing in an X, the back made of "
                   "crosspieces 36 cm long and the seat of crosspieces 32 cm across, labels Crosspiece and Chair support on each. SIDE VIEW OF "
                   "FOLD-UP CHAIR: the chair back, a light bar 66 cm long leaning up to the left, its crosspieces drawn as small blocks along "
                   "its top edge with the gap between two of them marked 1.27 cm spacing; the chair seat, a dark bar sloping up to the right, "
                   "with six raised blocks (its crosspieces) along its top. Below them the MATERIAL LIST (typed in the table) and a photo: "
                   "ASSEMBLED CHAIR AND FOLDED-UP CHAIR, the slatted chair standing open and, beside it, a second chair folded flat."),
     "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Aerial view", "marks": 2,
     "lead": "John and five other family members decided to participate in the Baviaanskloof Leopard Trail Run. They decided to camp at the "
             "Baviaanskloof Uitspan camping site.\n\nANNEXURE A shows an aerial view of Baviaanskloof Uitspan with campsites and the number of "
             "campers allowed. Some campsites have one hut and others have more than one hut, labelled A, B and C.", "items": q21},
    {"id": "2.1.6", "title": "Question 2.1.6", "kind": "Layout plan and scale", "marks": 8,
     "lead": "The layout plan below shows the ablution facilities (toilets and showers) in the middle of campsites 3, 4, 5 and 6.\n\nThe actual "
             "length of the ablution facilities is 8,2 metres.",
     "figure": fig("2.1.6", "LAYOUT PLAN OF THE ABLUTION FACILITIES: a long rectangle with an arrow along its top labelled 8,2 m, the arrow and "
                   "the plan printed about 90 mm long on the A4 question paper (on a screen they show at another size). Along the top wall, a "
                   "row of shower cubicles side by side, each with a shower head. Along the bottom wall, on the right, a row of toilet "
                   "cubicles. In the bottom left corner, an L-shaped bench: one part up the left wall, one part along the bottom wall. A door "
                   "in the right wall. KEY: Shower (a cubicle with a shower head), Toilet (a cubicle with a toilet), Bench (a striped strip)."),
     "items": q216},
    {"id": "3.1", "title": "Question 3.1", "kind": "Time and perimeter", "marks": 11,
     "lead": "Mrs Kgomo is a Grade 2 teacher at Happy Valley Primary School.\n\nShe has a reading corner at the back of her classroom. Learners who "
             "wait for their transport after school, usually sit there and read a book.\n\nMrs Kgomo stores pillows in bags (see pictures below). "
             "Learners sit on these pillows after school.\n\nNOTE: Piping: thin cord covered in fabric used to decorate the bag and reinforce the seams",
     "figure": fig("3.1", "PILLOWS IN THE BAG: a person holding a box-shaped storage bag with a zip around its lid and a handle on its side; a "
                   "clear strip down its front shows four pillows stacked one above the other; an arrow labelled Piping points to the cord "
                   "along its bottom edge. DIMENSIONS OF THE BAG: the same bag, 48 cm high, 46 cm long and 30 cm wide."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Circles and paint", "marks": 13,
     "lead": "Mrs Kgomo created a birthday calendar for her 2024 class to hang against the wall.\n\nShe will write each learner's name and birthday "
             "on a small circular wooden tag and attach the tag to the correct month.\n\nThe circular wooden tag has a circular hole to attach a "
             "ring that is used to hang the tag. The area of the circular hole is 0,3142 cm².\n\nEvery year she paints the front surface area of "
             "the circular wooden tags.\n\nThe spread rate of the paint is 6 m²/ℓ.",
     "figure": fig("3.2", "PICTURE AND DIAGRAM OF A CIRCULAR WOODEN TAG. Left: a round grey tag with 'Annette 6 April' written on it and a small "
                   "hole near its top edge (an arrow labelled Circular hole). Right: the tag drawn as a circle with the small hole near its "
                   "top; an arrow down its left side labelled 8 cm and an arrow under it labelled 8 cm (its height and its width)."),
     "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Volume of a cube", "marks": 4,
     "lead": "On each learner's birthday, the learner receives a cubic-shaped packet of homemade sweets, as shown in the diagram and picture below.",
     "figure": fig("3.3", "DIAGRAM AND PICTURE OF A CUBE AND A CUBIC-SHAPED PACKET. Left: a line drawing of a cube. Right: a photo of a "
                   "cube-shaped paper gift bag with two handles."), "items": q33},
    {"id": "3.3.2", "title": "Question 3.3.2", "kind": "Probability", "marks": 3,
     "lead": "There are 35 different coloured sweets in each packet.\n\nTABLE 2 below shows the number of sweets per colour.", "table": SWEETS,
     "items": q332},
    {"id": "4.1", "title": "Question 4.1", "kind": "Temperature and surface area", "marks": 15,
     "lead": "Crude oil is heated in a vertical, cylindrical tower to separate and extract products, such as petroleum gas, gasoline (petrol), "
             "kerosene (lamp oil), diesel, industrial oil, and paraffin wax, which boil at different temperatures.\n\nNOTE:\n• Extraction occurs "
             "because different liquids have different boiling points.\n• Extraction takes place in a large, vertical, cylindrical tower with a "
             "diameter of 6 m.\n• The total surface area of sections (A + C) = 150,816 m².",
     "figure": fig("4.1", "Left, CYLINDRICAL TOWER SHOWING DIFFERENT PRODUCTS AND THEIR BOILING TEMPERATURES: a tower heated from a furnace at its "
                   "bottom left, divided by rows of extractor pipes into sections marked, from the top down, 20 °C, 150 °C, 200 °C, 300 °C, "
                   "370 °C and 400 °C. Pipes lead out on the right; the products, from the top down: Petroleum gas, Gasoline (petrol), "
                   "Kerosene (lamp oil), Diesel, Industrial oil, and Paraffin wax out of the bottom of the tower. Right, DIAGRAM OF A "
                   "VERTICAL, CYLINDRICAL TOWER: a tall cylinder with rounded ends, split by two dashed lines into A (the rounded top), B (the "
                   "middle, 54 m high) and C (the rounded bottom); 6 m wide."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Bricks and costs", "marks": 14,
     "lead": "A worker at the oil refinery intends converting her double-door garage into a bigger living room by building double-bricked walls to "
             "replace both of the doors.\n\nNOTE:\n• 525 bricks per pallet at a price of R6,45 per brick. Bricks are sold per pallet.\n• Half bricks "
             "are thrown away (not re-used).",
     "figure": fig("4.2", "PICTURE OF TWO DOORS TO BE REPLACED: a double garage with two panelled doors side by side. BRICKS ON A WOODEN PALLET: "
                   "a cube-shaped stack of bricks on a wooden pallet. INCOMPLETE DIAGRAM SHOWING THE PATTERN OF HOW THE BRICKS SHOULD BE LAID, "
                   "WITH THE FIRST TWO ROWS COMPLETED: the face of the wall in a door opening: the bottom two rows run the full width, each "
                   "nine whole bricks and a half brick (the lower row starts with the half brick, the upper row ends with it); above them, a "
                   "staircase of rows up the right-hand edge shows the pattern to the top, 20 rows in all. SIDE VIEW OF THE DOUBLE-BRICK "
                   "WALL: the end of the wall, two bricks thick and 20 rows high."), "items": q42},
    {"id": "5.2", "title": "Question 5.2", "kind": "Conversion and ratio", "marks": 7,
     "lead": "Chris and Boipelo plan to visit Uluru. This oval-shaped big rock rises 1 142 feet above the surrounding desert plain.\n\nThe diagram "
             "below shows a comparison of the height of Uluru and some other tourist attractions around the world.",
     "figure": fig("5.2", "The outline of Uluru, a long rock with a rounded top, drawn across the whole diagram; a vertical line marked ULURU rises "
                   "to its highest point, labelled 348 m. In front of it, from left to right, each with its height: Sydney Harbour Bridge "
                   "134 m, the Eiffel Tower 324 m, the Great Pyramid of Giza 139 m and Big Ben 96 m."), "items": q52},
    {"id": "5.3", "title": "Question 5.3", "kind": "Area and population density", "marks": 12,
     "lead": "In addition to the mainland, Australia is surrounded by many thousands of small islands. Boipelo found TABLE 3 indicating the areas for "
             "the mainland, islands and total for each state or territory on a website. Some values have been omitted.", "table": AREAS, "items": q53},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P2", "sitting": "November 2024", "total_marks": 115, "time": "3 hours"},
    "sections": [{"title": "Mathematical Literacy", "total": 115, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "Every part playable from the question paper (Questions 1, 3 and 4 whole; 2.1.1, 2.1.6, 5.2 "
                                                           "and 5.3), hand-transcribed from scanned page images of the question paper (no text layer) "
                                                           "and from the memo's text and page images; no API call."},
        {"n": "2.1", "kind": "no_fit", "detail": "2.1.2 (3), 2.1.3 (2), 2.1.4 (2) and 2.1.5 (3), 10 marks, read ANNEXURE A (the aerial view of "
                                                 "Baviaanskloof Uitspan) in the ADDENDUM, which is not on disk: left out. 2.1.1 (what an aerial "
                                                 "view is) and 2.1.6 (the layout plan printed in the paper) are played."},
        {"n": "2.2", "kind": "no_fit", "detail": "2.2.1 (2), 2.2.2 (2), 2.2.3 (2), 2.2.4 (2) and 2.2.5 (3), 11 marks, all read ANNEXURE B (the map "
                                                 "and the elevation map of the Leopard Trail Run) in the ADDENDUM, which is not on disk: left out."},
        {"n": "5.1", "kind": "no_fit", "detail": "5.1.1 (2), 5.1.2 (3), 5.1.3 (3), 5.1.4 (2) and 5.1.5 (4), 14 marks, all read ANNEXURE C (the map "
                                                 "of Australia and the trip plan) in the ADDENDUM, which is not on disk: left out. With 2.1 and 2.2, "
                                                 "35 marks wait for the addendum; the paper totals the 115 marks that can be played (the printed "
                                                 "paper: 150; per question 26, 10 of 31, 31, 29, 19 of 33)."},
        {"n": "2.1.6(b)", "kind": "no_fit", "detail": "The memo's first mark is for MEASURING the printed plan (90 mm; accept ± 1 mm). A phone "
                                                      "shows the plan at another size, so the figure caption gives the printed length (measured on "
                                                      "the scan: 253,4 pt = 89,4 mm) and the mark becomes a read-off; the scale's steps take the "
                                                      "range a 89-91 mm measurement gives (1 : 90 to 1 : 92)."},
        {"n": "3.1.1", "kind": "no_fit", "detail": "Terms the memo marks in parts play all or nothing: 3.1.1 (MA + A; the duration in every common "
                                                   "written form) and 5.2.2 (RT + A order + 2 CA; the simplified ratio as a strict term)."},
        {"n": "1.2.1", "kind": "no_fit", "detail": "Calculations play as steps: each step is the number the memo's method produces, its SF/MA/RT/C "
                                                   "marks riding on that number. 'Verify' parts (3.2.3, 4.2.2) fold the memo's conclusion (VALID / "
                                                   "Not VALID, the O mark) into the last step's number; 5.3.3(b)'s reason ('rounds off to zero') is "
                                                   "played as the percentage rounded to the table's one decimal place (0). The memo's NPR rule "
                                                   "widens the tolerance where an answer must be rounded (3.2.1, 3.3.2, 4.1.4) and of 5.3.3(a)'s "
                                                   "unrounded density (192,7 to 192,75)."},
        {"n": "4.2.2", "kind": "no_fit", "detail": "The memo accepts the area rounded up to 13 m² (labour R6 500, total R15 272,50) as well as "
                                                   "12,78 m² (R6 390, R15 162,50): the labour and total steps take tolerances spanning both."},
        {"n": "5.2", "kind": "no_fit", "detail": "The picture of Uluru beside the lead is a photo only (no data) and is not cropped; its sentence "
                                                 "'A picture of Uluru is shown alongside.' is left out of the lead. The figure is the height "
                                                 "comparison diagram the parts read."},
        {"n": "2.1.6(b)", "kind": "memo_issue", "detail": "The memo's box reads 'Accept ± 1 mm deviation on measurement per province': the plan "
                                                          "has no provinces (a line carried over from another paper); read as ± 1 mm on the "
                                                          "measured length."},
        {"n": "4.2.1", "kind": "memo_issue", "detail": "The memo's two methods count different bricks: 19 a row of the double-brick wall × 20 rows "
                                                       "= 380 a door (760 for both), or 10 a row of a single wall × 20 rows = 200, 400 for the double "
                                                       "wall (800 for both); both give 2 pallets. The face diagram shows each row as nine whole "
                                                       "bricks and a half brick, so 19 counts the halves as halves and 20 as whole bricks. The steps' "
                                                       "tolerances span both (19-20, 380-400, 760-800)."},
        {"n": "3.2.3", "kind": "memo_issue", "detail": "The memo's fourth method writes the hole's area as 0,3142 ÷ 10 000 = 0,0000314 m², then "
                                                       "subtracts 0,00003142 m² (its result 0,00499578 m² and its answer 29,97 mℓ are right)."},
    ],
}
out = Path(__file__).parent / "out" / "ml-p2-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper and the memo PDF and their page "
                                                                       "images (no API call)",
                                                        "scope": "Questions 1, 3 and 4 whole; 2.1.1, 2.1.6, 5.2 and 5.3 (2.1.2-2.1.5, 2.2 and 5.1 "
                                                                 "read the addendum's annexures, not on disk)"}, "paper": paper},
                                              indent=1, ensure_ascii=False), encoding="utf-8")
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
