"""Mathematical Literacy P2 Nov 2024, the whole paper (Questions 1 to 5, 150 marks), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the transcription
is the source, kept in git (out/ is not). The question paper and its ADDENDUM are SCANS (no text layer): read from their page images;
the memo has a text layer, checked against its page images.

  python tools/ingest/transcribe_ml_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Mathematical Literacy P2 Nov 2024 Eng.pdf" "<...>/Mathematical Literacy P2 Nov 2024 MG Afr & Eng.pdf" \
      --id ml-p2-2024-11 --from-json --answer-book "<...>/Mathematical Literacy P2 Nov 2024 Addendum Eng.pdf"

The paper reads three ANNEXURES printed in the ADDENDUM (a 4-page scan; page 1 is its cover): A (page 2, an aerial view of the camp
with a table of campsites and campers) for 2.1.1-2.1.5, B (page 3, the trail-run route map and its elevation maps) for 2.2 and C
(page 4, a map of Australia beside the trip plan) for 5.1. Their figures are cropped from the addendum, passed to ingest.py as
--answer-book (figure source "answer_book", page = the addendum's page); A and C are landscape pages printed on their side (their
text reads bottom to top), so their figures carry rotate 90. A's table is typed as the mission's table. B is split in two: the route
map on 2.2 (2.2.1-2.2.2) and the elevation maps on 2.2.3 (2.2.3-2.2.5), each on the mission that reads it. C is one figure: 5.1's
parts read the map and the trip plan in turn (5.1.2 both). 5.3 says "refer to ANNEXURE C" but every part reads only TABLE 3.

The memo's shapes map as in Mathematical Literacy P2 Nov 2025 (transcribe_ml_p2_2025_11.py):
  matching concepts to TABLE 1's definitions (A-G) -> match (2 marks a pair); "Choose ... (A, B or C)" -> mcq; a name, a product, a
  duration, a direction, a probability read off a table, a simplified ratio -> term (every spelling the memo accepts; all or nothing
  where the memo splits the marks; `reject` for a wrong direction a spelling slip away); the names of several things the memo marks
  one by one (two cities, four months) -> list; an explanation or a reason (A/O marks) -> rubric, each memo alternative one 2-mark
  point.
  Every number the learner would TYPE (a count read off a figure, "Calculate / Determine / Convert", "Verify" / "Show ... whether
  or not he is correct") -> authored whole-working mcq (Murci, 2026-10-10; the layout of transcribe_math_p1_2025_11.py): the stem
  plus "Choose the correct working.", four workings with one step a line ("{a}/{b}" a fraction, numbers the memo's way): the memo's
  FIRST method as it works it, and three built from real errors (a wrong operation or base, a unit slip, a value read from the
  wrong row, radius for diameter, a wrong rounding; in a verify part an error that turns the conclusion), each ending in a
  confident result; every option of a part has the same number of lines; the part keeps its marks, all or nothing. A value the
  memo ALSO accepts (2.1.6(b)'s 89-91 mm measurement, 4.2.1's 20 bricks a row, 4.2.2's 13 m²) never appears in a wrong option.
Figure boxes are measured in PDF points (both scans are 595.2 x 841.68) with ink profiles of the page (scratchpad ml2_24_tools/ink.py),
set so that ingest's 1% pad keeps each drawing and its frame and leaves out the "[Adapted from ...]" / "[Source: ...]" lines, the
text around it and the question's outer box; `inset` where a printed heading touches the crop's top-left corner (the page's Hide
button sits there). An addendum box is in the page's OWN (unrotated) coordinates: ingest crops it, then turns it upright. B's two
boxes sit inside the annexure's frame (its title bars named in the captions), between each drawing and the source line printed
inside that frame. One exception: C's "[Adapted from www.wilmap.com.au]" sits inside the map's frame at the height of the map's Key
and below Tasmania, so no box can leave it out without clipping the Key or Tasmania; C's crop is the whole annexure frame, the line
included. Checked on the rendered crops."""
import json
import re
from pathlib import Path

W, H = 595.2, 841.68   # the question paper's page and the addendum's page alike
FIGS = {  # [page, x0, y0, x1, y1] in points (the question paper)
    "1.2": [3, 113.5, 458.6, 530.8, 580.0], "1.3": [4, 111.5, 125.2, 521.0, 510.5], "2.1.6": [5, 160.0, 503.0, 501.0, 653.5],
    "3.1": [7, 111.5, 228.6, 516.5, 402.8], "3.2": [8, 107.9, 264.2, 520.7, 412.0], "3.3": [9, 107.5, 127.0, 500.0, 306.0],
    "4.1": [10, 111.5, 162.5, 513.0, 418.5], "4.2": [11, 108.9, 113.6, 507.3, 474.0], "5.2": [12, 92.0, 528.0, 530.5, 681.5]}
ADDENDUM = {  # [page, x0, y0, x1, y1] in points of the ADDENDUM's page as scanned (A and C lie on their side)
    "2.1": [2, 120.0, 94.6, 493.3, 752.2], "2.2": [3, 66.0, 172.0, 546.0, 396.0], "2.2.3": [3, 66.0, 476.0, 524.0, 669.0],
    "5.1": [4, 118.5, 40.0, 515.0, 806.0]}
ROTATE = {"2.1": 90, "5.1": 90}   # clockwise degrees that turn the crop upright: A's and C's text reads bottom to top
INSET = {"1.2": 40, "1.3": 40, "2.1": 40, "2.1.6": 40, "2.2.3": 40, "3.1": 40, "3.2": 40, "3.3": 40, "4.1": 40, "4.2": 40, "5.1": 40}


def fig(name, caption):
    book = name in ADDENDUM   # an annexure: cropped from the addendum, given to ingest.py as --answer-book
    p, x0, y0, x1, y1 = (ADDENDUM if book else FIGS)[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"source": "answer_book"} if book else {}), **({"inset": INSET[name]} if name in INSET else {}),
            **({"rotate": ROTATE[name]} if name in ROTATE else {})}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


WORK = "\n\nChoose the correct working."


def work(n, q, marks, a, right, wrong, clues):
    """An authored whole-working MCQ (Murci, 2026-10-10): `right` is the memo's FIRST method, put at index a (0-3); `wrong` are the
    three workings built from common errors, filling the other places in order. One step a line ("\\n")."""
    assert len(wrong) == 3 and 0 <= a <= 3, n
    opts = list(wrong)
    opts.insert(a, right)
    return mcq(n, q + WORK, opts, a, clues, marks=marks)


# notes: the memo's marking instructions that are NOT points: never scored, never shown. worth: each point's own marks where they differ.
def rub(n, q, marks, bullets, clues, each=None, must=None, notes=None, worth=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {}), **({"notes": notes} if notes else {}), **({"worth": worth} if worth else {})}


term = lambda n, q, a, clues, marks=2, strict=False, reject=None: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                                   **({"strict": True} if strict else {}), **({"reject": reject} if reject else {})}
lst =lambda n, q, count, pool, clues, marks: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
match = lambda n, q, left, right, a, each, clues, **kw: {"t": "match", "n": n, "marks": len(left) * each, "q": q, "clues": clues, "left": left,
                                                         "right": right, "a": a, **({"each": each} if each > 1 else {}), **kw}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


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
    work("1.2.1", "Convert 220 mm to metres.", 2, 2,
         "220 mm ÷ 1 000\n= 0,22 m", [
             "220 mm ÷ 100\n= 2,2 m",
             "220 mm × 1 000\n= 220 000 m",
             "220 mm ÷ 10\n= 22 m"],
         ["1 m = 1 000 mm.", "To a bigger unit: divide."]),
    mcq("1.2.2", "Choose, from the options (A, B or C) below, the correct one that could be used to calculate the volume of the hexagonal paving brick.",
        ["Volume = 6 × area of triangle × height", "Volume = side length + height + width", "Volume = 6 × perimeter × height"], 0,
        ["Volume = area of the top face × height.", "The top face is made up of 6 equal triangles: which option uses an AREA?"]),
    work("1.2.3", "Calculate the number of bricks needed for a single row along a length of 2 860 mm.", 3, 0,
         "Number of bricks = 2 860 mm ÷ 220 mm\n= 13", [
             "Number of bricks = 2,86 m ÷ 220 mm\n= 0,013",
             "Number of bricks = 2 860 mm ÷ 90 mm\n= 31,78",
             "Number of bricks = 2 860 mm ÷ 22 cm\n= 130"],
         ["In THREE BRICKS IN A ROW, which dimension lies along the row?", "Divide the length of the row by that dimension."])]
q13 = [
    work("1.3.1", "Write down the total number of wooden items needed to assemble this chair.", 2, 3,
         "4 + 13 + 1\n= 18 items", [
             "4 + 13\n= 17 items",
             "4 × 13 × 1\n= 52 items",
             "1 + 1 + 1\n= 3 items"],
         ["The # column gives how many of each item.", "Add the numbers of all the items in the material list."]),
    work("1.3.2", "Determine the number of crosspieces found on the seats of THREE chairs.", 3, 1,
         "Number of crosspieces = 6 × 3\n= 18", [
             "Number of crosspieces = 13 × 3\n= 39",
             "Number of crosspieces = 6 + 3\n= 9",
             "Number of crosspieces = 5 × 3\n= 15"],
         ["Count the crosspieces across the SEAT only (not the back): the side view shows them as blocks.", "Then multiply by the number of chairs."]),
    term("1.3.3", "Name the item in the material list with the longest dimension.", ["Chair support", "Chair supports"],
         ["Each item's dimensions are given as thickness × width × length.", "Find the biggest of the lengths and read that item's name."]),
    work("1.3.4", "Identify which dimension of the chair support will represent the thickness of the wood.", 2, 0,
         "Smallest of 1,9 cm, 3,8 cm and 66 cm\n= 1,9 cm", [
             "Largest of 1,9 cm, 3,8 cm and 66 cm\n= 66 cm",
             "Middle of 1,9 cm, 3,8 cm and 66 cm\n= 3,8 cm",
             "1,9 cm + 3,8 cm + 66 cm\n= 71,7 cm"],
         ["Read the NOTE under the material list.", "Find the smallest of the chair support's three dimensions."]),
    work("1.3.5", "Write down, in millimetres, the length of the spacing between the crosspieces of the back of the chair.", 2, 2,
         "Space = 1,27 × 10 mm\n= 12,7 mm", [
             "Space = 1,27 ÷ 10 mm\n= 0,127 mm",
             "Space = 1,27 × 100 mm\n= 127 mm",
             "Space = 1,27 × 1 000 mm\n= 1 270 mm"],
         ["The side view labels the spacing between the crosspieces of the chair back.", "1 cm = 10 mm."])]

# ---- QUESTION 2, the question paper pages 5-6, the memo pages 4-6 and the ADDENDUM pages 2-3 (ANNEXURES A and B) ----
q21 = [
    rub("2.1.1", "Explain what is meant by aerial view.", 2, [
        "View from the top (2).", "OR — View of the landscape from a certain height above ground like from a satellite or drone (2).",
        "OR — View from an elevated height (2).", "OR — Birds-eye view (2)."],
        ["The word 'aerial' comes from 'air'.", "Where would you have to be to see the whole camp like a map?"], each=2),
    work("2.1.2", "Calculate the maximum number of campers that can be accommodated at Baviaanskloof Uitspan camping site.", 3, 1,
         "Number of campers = 6 + 15 + 4 + 15 + 4 + 4 + 5 + 15 + 8 + 10 + 6 + 6 + 20\n= 118", [
             "Number of campers = 6 + 15 + 4 + 15 + 4 + 4 + 5 + 15 + 8 + 10 + 4 + 4 + 20\n= 114",
             "Number of campers = 6 + 15 + 15 + 5 + 15 + 10 + 6 + 6 + 20\n= 98",
             "Number of campers = 6 + 15 + 4 + 15 + 4 + 4 + 5 + 15 + 8 + 10 + 5 + 5 + 20\n= 116"],
         ["Add the campers of EVERY hut in the table, the B and C huts included.", "Where the table gives a range (4 – 6), the maximum is "
          "its bigger number."]),
    term("2.1.3", "Determine the general direction of the dam from campsite 8.", ["South West", "SW", "Southwest"],
         ["Find campsite 8 and the dam on the aerial view; the arrow marked N points north.", "Stand at campsite 8: which way is the dam? "
          "Combine two compass directions."], reject=["South East", "Southeast", "North West", "Northwest"]),
    term("2.1.4", "The description below is found on their website:\n\n'This campsite is situated near the dam and can accommodate a maximum "
         "of 19 campers.'\n\nWrite down which campsite is being described. Write down only the number of the campsite.", ["2", "Campsite 2"],
         ["Which numbered campsites are close to the dam on the aerial view?", "Add the campers of all the huts at each of them: which "
          "totals 19?"]),
    work("2.1.5", "Calculate, as a percentage, the probability of John and his family randomly selecting a hut that can exactly accommodate "
         "the whole family.", 3, 3,
         "{3}/{13} × 100%\n= 23,076923%", [
             "{1}/{13} × 100%\n= 7,692308%",
             "{3}/{9} × 100%\n= 33,333333%",
             "{9}/{13} × 100%\n= 69,230769%"],
         ["How many people are in John's family group? Find the huts whose number of campers is exactly that (a range counts when the "
          "number is in it).", "Each row of the table is one hut: probability = huts that fit ÷ all the huts, × 100%."])]
q216 = [
    work("2.1.6(a)", "Write down the total number of showers.", 2, 2,
         "Shower cubicles along the top wall: 9\nTotal number of showers = 9", [
             "Toilet cubicles along the bottom wall: 6\nTotal number of showers = 6",
             "Cubicles along both walls: 9 + 6\nTotal number of showers = 15",
             "Shower symbols in the plan and the key: 9 + 1\nTotal number of showers = 10"],
         ["Use the KEY: which symbol is a shower?", "Count those cubicles in the plan."]),
    work("2.1.6(b)", "Determine, rounded to the nearest whole number, the scale of the plan.", 4, 0,
         "90 mm = 8,2 m\n90 mm = 8 200 mm (÷ 90)\n1 : 91,11\n1 : 91", [
             "90 mm = 8,2 m\n90 mm = 820 mm (÷ 90)\n1 : 9,11\n1 : 9",
             "9 cm = 8,2 m\n9 cm = 8 200 mm (÷ 9)\n1 : 911,11\n1 : 911",
             "90 mm = 8,2 m\n8 200 mm = 90 mm (÷ 90)\n91,11 : 1\n91 : 1"],
         ["Measure the plan's length on the paper (the figure's caption gives it) and change 8,2 m to the same unit.",
          "Scale = 1 : actual length ÷ plan length; round to a whole number."]),
    rub("2.1.6(c)", "Give ONE suitable reason why benches are found in the ablution facilities.", 2, [
        "To allow people to sit while waiting for a toilet or shower to become available (2).",
        "OR — To place your clothes or belongings on while you are showering (2).",
        "OR — To sit while you change your outfit, or getting dressed or apply body lotion or for baby nappy change (2)."],
        ["Who uses the ablutions at a busy camp, and what might they have to wait for?", "What do you do with your clothes while you shower?"], each=2)]
q22 = [
    term("2.2.1", "Write down the day during the run when you would pass Gabriel's Pools.", ["Day 2", "Day two", "2", "The second day"],
         ["Find Gabriel's Pools on the route map.", "Which loop, Day 1 or Day 2, does it lie on?"]),
    mcq("2.2.2", "The descriptions of a part of the route on the brochure are as follows:\n\n• Run for 5,5 km along Rhebok Valley.\n• Continue "
        "down the other side to the Reflection Pools for a swim and drinking water.\n• Then return to the home base.\n\nChoose the route "
        "described above and match it with A, B, C or D. Write only the letter next to the question number (2.2.2).",
        ["Leopard Trail Run – Day 1 (Part 1)", "Leopard Trail Run – Day 1 (Part 2)", "Leopard Trail Run – Day 2 (Part 1)",
         "Leopard Trail Run – Day 2 (Part 2)"], 3,
        ["Rhebok Valley and the Reflection Pools lie on the same loop: which day is it?", "The description ends back at the home base: is it "
         "the first or the second part of that day's run?"])]
q223 = [
    work("2.2.3", "Determine the number of kilometres John had run when he reached the highest point above sea level on Day 2.", 2, 1,
         "Highest point on the DAY 2 map: 1 173 m\nDistance run at that point = 12,5 km", [
             "Highest point on the DAY 2 map: 1 173 m\nDistance run = 21,9 km − 12,5 km = 9,4 km",
             "Highest point on the DAY 2 map: 1 173 m\nDistance run = 1 173 m ÷ 1 000 = 1,173 km",
             "Highest point on the DAY 1 map: 1 183 m\nDistance run at that point = 7 km"],
         ["Use the TRAIL RUN – DAY 2 elevation map.", "Find the curve's highest peak and read the distance straight below it."]),
    rub("2.2.4", "John's best average speed (in km/h) for the run was his average speed from the 8 km mark up to the 18 km mark on Day 1.\n\n"
        "Use the elevation map to explain why this was the case.", 2, [
        "The part shows a continuous downward slope, it is downhill (2).", "OR — That part does not have many uphills (2)."],
        ["Find 8 km and 18 km on the TRAIL RUN – DAY 1 elevation map.", "Between them, does the curve go up or down, and how does that "
         "change a runner's speed?"], each=2),
    work("2.2.5", "John stated that on Day 2, while he was running from the 17,5 km mark to the end of the trail, he had moved more than 100 "
         "metres closer to sea level.\n\nShow, by means of calculations, whether or not he is correct.", 3, 3,
         "Difference = 1 050 m − 900 m\n= 150 m\nHe is CORRECT.", [
             "Difference = 975 m − 900 m\n= 75 m\nHe is NOT correct.",
             "Difference = 1 050 m − 900 m\n= 150 m = 0,15 km\n0,15 is less than 100: he is NOT correct.",
             "Difference = 1 173 m − 900 m\n= 273 m\nHe is CORRECT."],
         ["On the DAY 2 elevation map, read the height at the 17,5 km line and at the end of the trail from the heights labelled on the "
          "left.", "Subtract the two heights and compare the difference with 100 m."])]

# ---- QUESTION 3, the question paper pages 7-9 and the memo pages 7-11 ----
q31 = [
    term("3.1.1", "The school day ends at 12:55.\n\nTendani's father was late and only came to fetch him at 14:13.\n\nDetermine how long Tendani sat in "
         "the reading corner.", ["1 hour 18 minutes", "1 hour and 18 minutes", "1 hour 18 min", "1 hr 18 min", "1 hr 18 mins", "1 h 18 min",
                                 "1h18min", "1h18", "1 h 18", "1:18", "01:18", "78 minutes", "78 min", "78 mins", "1,3 hours", "1,3 h", "1,3 hrs"],
         ["From 12:55 to 13:00 is 5 minutes.", "Then count on from 13:00 to 14:13."]),
    work("3.1.2", "The height of one pillow is 11 cm.\n\nDetermine the difference between the total height of the pillows in ONE bag and the height "
         "of the bag.", 4, 1,
         "Total height of 4 pillows = 11 cm × 4\n= 44 cm\nDifference = 48 cm − 44 cm\n= 4 cm", [
             "Total height of 4 pillows = 11 cm × 4\n= 44 cm\nDifference = 46 cm − 44 cm\n= 2 cm",
             "Total height of 3 pillows = 11 cm × 3\n= 33 cm\nDifference = 48 cm − 33 cm\n= 15 cm",
             "Total height of 4 pillows = 11 cm × 4\n= 44 cm\nDifference = 44 cm − 30 cm\n= 14 cm"],
         ["Count the pillows stacked in ONE bag in the picture.", "Add up their heights and compare with the bag's height."]),
    work("3.1.3", "The piping around the bottom edge of some of the bags for the pillows needs to be replaced. The store sells the piping in half-metre "
         "lengths.\n\nCalculate the total length of piping she will have to purchase to replace the piping around the bottom edges of FOUR bags.\n\n"
         "You may use the following formula:\nPerimeter = 2 (length + width)", 5, 2,
         "Perimeter = 2 (46 cm + 30 cm) = 2 (76 cm)\n= 152 cm\nTotal length for 4 bags = 152 × 4\n= 608 cm\n= {608}/{100} = 6,08 m\n"
         "She must buy 6,5 m", [
             "Perimeter = 46 cm + 30 cm\n= 76 cm\nTotal length for 4 bags = 76 × 4\n= 304 cm\n= {304}/{100} = 3,04 m\nShe must buy 3,5 m",
             "Perimeter = 2 (46 cm + 48 cm) = 2 (94 cm)\n= 188 cm\nTotal length for 4 bags = 188 × 4\n= 752 cm\n= {752}/{100} = 7,52 m\n"
             "She must buy 8 m",
             "Perimeter = 2 (46 cm + 30 cm) = 2 (76 cm)\n= 152 cm\nTotal length for 4 bags = 152 × 4\n= 608 cm\n= {608}/{100} = 6,08 m\n"
             "She must buy 6 m"],
         ["The bottom edge of a bag is a rectangle 46 cm by 30 cm.", "Four bags, and the piping is sold only in half-metre lengths: round UP."])]
q32 = [
    work("3.2.1", "Determine, in cm, the circumference of the circular wooden tag.\n\nYou may use the following formula:\n"
         "Circumference of a circle = 3,142 × diameter", 2, 0,
         "Circumference = 3,142 × 8 cm\n= 25,136 cm", [
             "Circumference = 3,142 × 4 cm\n= 12,568 cm",
             "Circumference = 2 × 3,142 × 8 cm\n= 50,272 cm",
             "Circumference = 3,142 × (8 cm)²\n= 201,088 cm"],
         ["The diameter of the tag is printed on the diagram.", "Use 3,142, as the formula says."]),
    work("3.2.2", "Determine, in cm, the radius of ONE circular wooden tag.", 2, 3,
         "Radius = {8 cm}/{2}\n= 4 cm", [
             "Radius = 8 cm × 2\n= 16 cm",
             "Radius = {25,136 cm}/{3,142}\n= 8 cm",
             "Radius = {8 cm}/{3,142}\n= 2,546 cm"],
         ["The radius runs from the centre of the circle to its edge.", "How does it compare with the diameter?"]),
    work("3.2.3", "The hardware store sells paint in 50 mℓ, 1 litre, 5 litre and 20 litre containers.\n\nMrs Kgomo claims that a 50 mℓ can of paint "
         "will be sufficient to paint ONE side of 36 circular wooden tags.\n\nVerify her statement. Show ALL calculations.\n\nUse the following "
         "formula:\nArea of a circle = 3,142 × radius²", 9, 2,
         "Area of a circle = 3,142 × (4 cm)² = 3,142 × 16 cm² = 50,272 cm²\nArea to be painted = 50,272 − 0,3142 = 49,9578 cm²\n"
         "Total area = 36 × 49,9578 cm² = 1 798,4808 cm²\nTotal area in m² = 1 798,4808 ÷ 100² = 0,179848 m²\n"
         "6 m² = 1 ℓ = 1 000 mℓ, so 0,3 m² = 50 mℓ\n0,3 m² > 0,179848 m²\nTherefore 50 mℓ will be more than sufficient.", [
             "Area of a circle = 3,142 × (8 cm)² = 3,142 × 64 cm² = 201,088 cm²\nArea to be painted = 201,088 − 0,3142 = 200,7738 cm²\n"
             "Total area = 36 × 200,7738 cm² = 7 227,8568 cm²\nTotal area in m² = 7 227,8568 ÷ 100² = 0,722786 m²\n"
             "6 m² = 1 ℓ = 1 000 mℓ, so 0,3 m² = 50 mℓ\n0,3 m² < 0,722786 m²\nTherefore 50 mℓ will not be sufficient.",
             "Area of a circle = 3,142 × (4 cm)² = 3,142 × 16 cm² = 50,272 cm²\nArea to be painted = 50,272 − 0,3142 = 49,9578 cm²\n"
             "Total area = 36 × 49,9578 cm² = 1 798,4808 cm²\nTotal area in m² = 1 798,4808 ÷ 100 = 17,984808 m²\n"
             "6 m² = 1 ℓ = 1 000 mℓ, so 0,3 m² = 50 mℓ\n0,3 m² < 17,984808 m²\nTherefore 50 mℓ will not be sufficient.",
             "Area of a circle = 3,142 × (4 cm)² = 3,142 × 16 cm² = 50,272 cm²\nArea to be painted = 50,272 + 0,3142 = 50,5862 cm²\n"
             "Total area = 36 × 50,5862 cm² = 1 821,1032 cm²\nTotal area in m² = 1 821,1032 ÷ 100² = 0,182110 m²\n"
             "6 m² = 1 ℓ = 1 000 mℓ, so 0,3 m² = 50 mℓ\n0,3 m² > 0,182110 m²\nTherefore 50 mℓ will be more than sufficient."],
         ["Area to paint on one tag = the tag's area minus the hole's area.", "6 m² per litre (1 000 mℓ): what area does 50 mℓ cover? Change "
          "the tags' cm² to m² (÷ 10 000) and compare."])]
q33 = [
    work("3.3.1", "The volume of the cubic-shaped packet is 2 744 cm³.\n\nCalculate the side length of the cubic-shaped packet.\n\nYou may use the "
         "following formula:\nVolume of a cube = side × side × side", 4, 1,
         "2 744 cm³ = side × side × side\n(side)³ = 2 744 cm³\n14 × 14 × 14 = 2 744\nSide = 14 cm", [
             "2 744 cm³ = side × side × side\n(side)³ = 2 744 cm³\nside = 2 744 ÷ 3 = 914,67\nSide = 914,67 cm",
             "2 744 cm³ = side × side\n(side)² = 2 744 cm³\nside = √2 744 = 52,38\nSide = 52,38 cm",
             "2 744 cm³ = side × side × side\n2 744 cm³ ÷ 1 000 = 2,744\n1,4 × 1,4 × 1,4 = 2,744\nSide = 1,4 cm"],
         ["Which number multiplied by itself three times gives 2 744?", "Use the cube root key, or try whole numbers between 10 and 20."])]
q332 = [
    work("3.3.2", "Determine the probability, as a decimal, of randomly choosing a pink or a yellow sweet from the packet.", 3, 0,
         "8 + 7 = 15\nP = {15}/{35} = 0,42857…\n≈ 0,43", [
             "8 + 11 = 19\nP = {19}/{35} = 0,54285…\n≈ 0,54",
             "8 + 7 = 15\nP = {15}/{35 − 15} = {15}/{20}\n= 0,75",
             "8 × 7 = 56\nP = {56}/{35 × 35} = 0,04571…\n≈ 0,05"],
         ["Add the pink and the yellow sweets.", "Divide by all the sweets in the packet, and write it as a decimal."])]

# ---- QUESTION 4, the question paper pages 10-11 and the memo pages 12-15 ----
q41 = [
    term("4.1.1", "Identify the crude oil product that will be third to boil.",
         ["Kerosene", "Lamp oil", "Kerosene (lamp oil)", "Kerosene or lamp oil"],
         ["The lower its boiling temperature, the sooner a product boils.", "Order the products from the lowest temperature: which is third?"]),
    term("4.1.2", "Write down the product extracted at 150 °C.", ["Gasoline", "Petrol", "Gasoline (petrol)", "Gasoline or petrol"],
         ["Find 150 °C on the tower.", "Follow the extractor pipe below that section to the product's name."]),
    work("4.1.3", "Convert the boiling point of diesel to degrees Fahrenheit.\nUse the formula: °C = (°F − 32)/1,8", 4, 3,
         "300 °C = {°F − 32}/{1,8}\n°F = 1,8 × 300 + 32\n= 572", [
             "370 °C = {°F − 32}/{1,8}\n°F = 1,8 × 370 + 32\n= 698",
             "300 °C = {°F − 32}/{1,8}\n°F = 300 ÷ 1,8 + 32\n= 198,67",
             "300 °C = {°F − 32}/{1,8}\n°F = 1,8 × 300 − 32\n= 508"],
         ["Read the temperature at which diesel is extracted.", "Put it in place of °C and solve for °F: multiply by 1,8, then add 32."]),
    work("4.1.4", "The pipes leading in and out of the vertical, cylindrical tower take up 2,5% of the surface area of part B of the cylindrical tower."
         "\n\nCalculate the total surface area of the vertical, cylindrical tower, excluding the area taken up by the pipes.\n\nUse the formula:\n"
         "Surface area of an open cylinder = 3,142 × diameter × height", 7, 1,
         "Surface area = 3,142 × 6 m × 54 m\n= 1 018,008 m²\nArea of pipes = {2,5}/{100} × 1 018,008\n= 25,4502 m²\n"
         "Total surface area = 1 018,008 m² − 25,4502 m² + 150,816 m²\n= 1 143,3738 m²", [
             "Surface area = 3,142 × 3 m × 54 m\n= 509,004 m²\nArea of pipes = {2,5}/{100} × 509,004\n= 12,7251 m²\n"
             "Total surface area = 509,004 m² − 12,7251 m² + 150,816 m²\n= 647,0949 m²",
             "Surface area = 3,142 × 6 m × 54 m\n= 1 018,008 m²\nArea of pipes = {2,5}/{100} × 1 018,008\n= 25,4502 m²\n"
             "Total surface area = 1 018,008 m² − 25,4502 m²\n= 992,5578 m²",
             "Surface area = 3,142 × 6 m × 54 m\n= 1 018,008 m²\nArea of pipes = {2,5}/{100} × 1 018,008\n= 25,4502 m²\n"
             "Total surface area = 1 018,008 m² + 25,4502 m² + 150,816 m²\n= 1 194,2742 m²"],
         ["Part B is an open cylinder 6 m wide and 54 m high: use the formula.", "Take away 2,5% of part B for the pipes, then add the area of "
          "A + C from the NOTE."])]
q42 = [
    work("4.2.1", "Determine the total number of pallets of bricks needed to replace both garage doors.", 5, 2,
         "Bricks in 1 row of a double-brick wall = 19\nBricks for 1 garage door = 19 × 20 = 380\nTotal number of bricks needed = 380 × 2 = 760\n"
         "∴ 760 ÷ 525 = 1,45: 2 pallets of bricks", [
             "Bricks in 1 row of a double-brick wall = 19\nBricks for 1 garage door = 19 × 20 = 380\nTotal number of bricks needed = 380 × 2 = 760\n"
             "∴ 760 ÷ 525 = 1,45: 1 pallet of bricks",
             "Bricks in 1 row of a double-brick wall = 19 × 2 = 38\nBricks for 1 garage door = 38 × 20 = 760\n"
             "Total number of bricks needed = 760 × 2 = 1 520\n∴ 1 520 ÷ 525 = 2,90: 3 pallets of bricks",
             "Bricks in 1 row of a double-brick wall = 19\nBricks for 1 garage door = 19 × 20 = 380\nTotal number of bricks needed = 380\n"
             "∴ 380 ÷ 525 = 0,72: 1 pallet of bricks"],
         ["Count the bricks in one row and the rows up the wall; the side view shows the wall is two bricks thick.",
          "There are two doors, and bricks are sold only in whole pallets of 525."]),
    work("4.2.2", "The opening of a garage door has dimensions of 2,13 m × 3 m.\n\nOther costs to build the double-brick wall:\n• Material, other "
         "than bricks, cost R2 000,00\n• Labour is R500,00 per square metre\n\nThe owner states that the total cost to replace both garage doors "
         "with walls would be R15 200,00.\n\nVerify her statement by means of calculations.\n\nYou may use the following formula: Area = length × width",
         7, 3,
         "Area of 2 doors = 2 × 2,13 × 3 = 12,78 m²\nLabour cost = 12,78 m² × R500 = R6 390\nBrick cost = 2 × 525 × R6,45 = R6 772,50\n"
         "Total cost = R2 000 + R6 390 + R6 772,50 = R15 162,50\nNot VALID", [
             "Area of 2 doors = 2 × 2,13 × 3 = 12,78 m²\nLabour cost = 12,78 m² × R500 = R6 390\nBrick cost = 2 × 525 × R6,45 = R6 772,50\n"
             "Total cost = R2 000 + R6 390 + R6 772,50 = R15 162,50\nVALID",
             "Area of 2 doors = 2 × 2,13 × 3 = 12,78 m²\nLabour cost = 12,78 m² × R500 = R6 390\nBrick cost = 760 × R6,45 = R4 902\n"
             "Total cost = R2 000 + R6 390 + R4 902 = R13 292\nNot VALID",
             "Area of 2 doors = 2 × (2,13 + 3) = 10,26 m²\nLabour cost = 10,26 m² × R500 = R5 130\nBrick cost = 2 × 525 × R6,45 = R6 772,50\n"
             "Total cost = R2 000 + R5 130 + R6 772,50 = R13 902,50\nNot VALID"],
         ["Area of both openings = 2 × length × width; labour is R500 per square metre.",
          "Bricks: the pallets from 4.2.1 × 525 × R6,45; add the R2 000 material and compare with R15 200."]),
    rub("4.2.3", "Give ONE suitable reason why the bricks have to be placed on a wooden pallet.", 2, [
        "To be easily lifted by a fork lift (2).", "OR — Storage / loading / transportation are made easier (2).", "OR — It keeps them from breaking (2).",
        "OR — It makes counting easier (2).", "OR — To protect the bricks from damage (2).", "OR — To keep it tight and compact (2)."],
        ["How is a heavy stack of bricks moved from a truck to a building site?", "What could happen to loose bricks stacked on the ground?"], each=2)]

# ---- QUESTION 5, the question paper pages 12-13, the memo pages 16-17 and the ADDENDUM page 4 (ANNEXURE C) ----
q51 = [
    lst("5.1.1", "Write down the names of the cities where the distance between them is 738 km.", 2, [["Adelaide"], ["Melbourne"]],
        ["Find 738 km on the map of Australia.", "Its bracket joins two cities: name both."], 2),
    lst("5.1.2", "Name the FOUR months when Chris and Boipelo will be in Western Australia.", 4,
        [["Aug", "August"], ["Sep", "September"], ["Oct", "October"], ["Nov", "November"]],
        ["Find Western Australia on the map, then the same part of the country on the trip plan.", "Name the months whose labels lie in "
         "that part."], 3),
    work("5.1.3", "Determine the distance from Perth to Adelaide.", 3, 0,
         "14 655 − (738 + 1 062 + 922 + 1 705 + 2 850 + 1 871 + 2 811)\n= 14 655 − 11 959\n= 2 696 km", [
             "14 655 − (1 062 + 922 + 1 705 + 2 850 + 1 871 + 2 811)\n= 14 655 − 11 221\n= 3 434 km",
             "14 655 − (738 + 1 062 + 922 + 1 705 + 3 027 + 1 871 + 2 811)\n= 14 655 − 12 136\n= 2 519 km",
             "14 655 − (738 + 1 062 + 922 + 1 705 + 2 850 + 1 871)\n= 14 655 − 9 148\n= 5 507 km"],
         ["The A1 goes right round Australia (14 655 km); Perth to Adelaide is the one stretch the map gives no distance for.",
          "Add the distances printed along the A1, then take the total away from 14 655 km."]),
    term("5.1.4", "Name the state where they plan to be during February.", ["Tasmania"],
         ["Find FEB on the trip plan.", "Which state does the map show in the same place?"]),
    work("5.1.5", "Calculate the average speed, in km/h, from Brisbane to Cairns.\n\nYou may use the following formula: Distance = speed × time", 4, 2,
         "1 705 km = s × 20 h 40 min\n1 705 km = s × 20,67 h\nSpeed = {1 705 km}/{20,67 h}\n= 82,5 km/h", [
             "1 705 km = s × 20 h 40 min\n1 705 km = s × 20,4 h\nSpeed = {1 705 km}/{20,4 h}\n= 83,58 km/h",
             "1 705 km = s × 20 h 40 min\n1 705 km = s × 1 240 min\nSpeed = {1 705 km}/{1 240 min}\n= 1,38 km/h",
             "922 km = s × 10 h 30 min\n922 km = s × 10,5 h\nSpeed = {922 km}/{10,5 h}\n= 87,81 km/h"],
         ["Read the distance and the driving time between Brisbane and Cairns on the map.", "Change the minutes to hours (÷ 60), then "
          "speed = distance ÷ time."])]
q52 = [
    work("5.2.1", "Determine, rounded to THREE decimal places, the conversion factor from feet to metres used in this diagram, in the form "
         "1 foot = … m.", 3, 1,
         "1 142 feet = 348 m\n1 foot = {348}/{1 142}\n= 0,304728546\n1 foot ≈ 0,305 m", [
             "1 142 feet = 348 m\n1 foot = {1 142}/{348}\n= 3,281609195\n1 foot ≈ 3,282 m",
             "1 142 feet = 324 m\n1 foot = {324}/{1 142}\n= 0,283712785\n1 foot ≈ 0,284 m",
             "1 142 feet = 34 800 cm\n1 foot = {34 800}/{1 142}\n= 30,472854641\n1 foot ≈ 30,473 m"],
         ["Uluru's height is given in feet in the text and in metres on the diagram.", "1 foot = metres ÷ feet; round to three decimal places."]),
    term("5.2.2", "Write, as a simplified ratio, the heights of Uluru : Eiffel Tower : Big Ben.", ["29 : 27 : 8", "29:27:8"],
         ["Read the three heights in metres, in the order the question asks.", "Divide all three by their highest common factor."], marks=4, strict=True)]
q53 = [
    term("5.3.1", "A meteorite (rock from the sky) fell somewhere in Australia.\n\nWrite down the probability that it randomly fell in Queensland.",
         ["22,5%", "22,5", "22,50%", "0,225", "0,2250", "0,224986", "0,22499", "22,4986%", "1 729 742/7 688 220", "1 729 742 ÷ 7 688 220"],
         ["The chance of landing in a state depends on its share of the total area.", "TABLE 3 gives each state's percentage of the total area."]),
    work("5.3.2", "Show, with calculations, why it could be stated that the total area of the islands of Australia is approximately half of the area "
         "of the mainland area of Tasmania.", 3, 3,
         "Area of island = {32 159}/{64 519}\n= 0,498 ≈ 0,5", [
             "Area of island = {3 882}/{64 519}\n= 0,060 ≈ 0,1",
             "Area of island = {32 159}/{7 656 061}\n= 0,004 ≈ 0",
             "Area of island = {32 159}/{68 401}\n= 0,470 ≈ 0,47"],
         ["Find the islands' TOTAL and Tasmania's MAINLAND area in TABLE 3.", "Divide the islands' area by Tasmania's mainland area: how close is it to ½?"]),
    work("5.3.3(a)", "The Australian Capital Territory has a population of 454 499.\n\nDetermine, rounded to the nearest whole number, the population "
         "density of the Australian Capital Territory as people per square km.", 3, 0,
         "Population density = {454 499}/{2 358}\n= 192,74…\n≈ 193", [
             "Population density = {454 499}/{2 358}\n= 192,74…\n≈ 192",
             "Population density = {2 358}/{454 499}\n= 0,0051…\n≈ 0",
             "Population density = {454 499}/{68 401}\n= 6,64…\n≈ 7"],
         ["Population density = number of people ÷ area.", "Use the Australian Capital Territory's total area in TABLE 3; round to a whole number."]),
    work("5.3.3(b)", "The Australian Capital Territory has a population of 454 499.\n\nGive a suitable reason, with calculations, why this area is "
         "omitted from the percentage calculation in the table.", 4, 2,
         "Land % area = {2 358}/{7 688 220} × 100%\n= 0,0306…%\nRounds off to zero.", [
             "Land % area = {2 358}/{7 688 220}\n= 0,000306…%\nRounds off to zero.",
             "Land % area = {2 358}/{32 159} × 100%\n= 7,3323…%\nRounds off to 7,3%.",
             "Island % area = {0}/{32 159} × 100%\n= 0%\nIt has no islands, so it has no percentage."],
         ["Work out its share of Australia's total area as a percentage.", "Compare the size of that percentage with the others in the table."])]

MATERIALS = {"title": "MATERIAL LIST", "head": ["#", "Wooden Item", "Dimensions (in cm)"],
             "rows": [["4", "Chair supports", "1,9 × 3,8 × 66"], ["13", "Crosspieces", "1,9 × 3,8 × 36"], ["1", "Seat back, bottom crosspiece", "1,9 × 3,8 × 32"]],
             "after": "NOTE:\n• The thickness of the wood is the smallest dimension.\n• # is the number of item(s)."}
CAMPERS = {"head": ["", "Number of campers"],   # the table printed on ANNEXURE A's aerial view (its first column has no heading)
           "rows": [["Campsite 1", "6"], ["Campsite 2A", "15"], ["2B", "4"], ["Campsite 3A", "15"], ["3B", "4"], ["3C", "4"],
                    ["Campsite 4", "5"], ["Campsite 5A", "15"], ["5B", "8"], ["Campsite 6", "10"], ["Campsite 7", "4 – 6"],
                    ["Campsite 8", "4 – 6"], ["Campsite 9", "20"]],
           "after": "NOTE: The bigger the hut, the more expensive it is."}
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
    {"id": "2.1", "title": "Question 2.1", "kind": "Aerial view", "marks": 12,
     "lead": "John and five other family members decided to participate in the Baviaanskloof Leopard Trail Run. They decided to camp at the "
             "Baviaanskloof Uitspan camping site.\n\nANNEXURE A shows an aerial view of Baviaanskloof Uitspan with campsites and the number of "
             "campers allowed. Some campsites have one hut and others have more than one hut, labelled A, B and C.", "table": CAMPERS,
     "figure": fig("2.1", "ANNEXURE A, AERIAL VIEW OF BAVIAANSKLOOF UITSPAN WITH CAMPSITES AND NUMBER OF CAMPERS: an aerial photo of the camp "
                   "in a valley. Top left, an arrow marked N points up the picture (north); beside it a label, Houtkloof mountains, lies "
                   "across rocky slopes that fill the upper left. Numbered circles mark the campsites. Lower left: campsite 1 at the left "
                   "edge of a dark pond labelled Dam, campsite 2 at its right edge and campsite 9 just below them. Upper middle: campsite 8 "
                   "where the rocky slopes end. To the lower right of 8, a cluster: 7, then 6 and 5 to its right, and below them 3 and 4, "
                   "with the label Ablution between them. Lower right: a building labelled Main house. In the top right corner, the table "
                   "of campsites and numbers of campers (typed in the table)."), "items": q21},
    {"id": "2.1.6", "title": "Question 2.1.6", "kind": "Layout plan and scale", "marks": 8,
     "lead": "The layout plan below shows the ablution facilities (toilets and showers) in the middle of campsites 3, 4, 5 and 6.\n\nThe actual "
             "length of the ablution facilities is 8,2 metres.",
     "figure": fig("2.1.6", "LAYOUT PLAN OF THE ABLUTION FACILITIES: a long rectangle with an arrow along its top labelled 8,2 m, the arrow and "
                   "the plan printed about 90 mm long on the A4 question paper (on a screen they show at another size). Along the top wall, a "
                   "row of shower cubicles side by side, each with a shower head. Along the bottom wall, on the right, a row of toilet "
                   "cubicles. In the bottom left corner, an L-shaped bench: one part up the left wall, one part along the bottom wall. A door "
                   "in the right wall. KEY: Shower (a cubicle with a shower head), Toilet (a cubicle with a toilet), Bench (a striped strip)."),
     "items": q216},
    {"id": "2.2", "title": "Question 2.2", "kind": "Trail run route map", "marks": 4,
     "lead": "The Leopard Trail Run is a two-day event, run on the outskirts of the camp, starting and ending at the Cedar Falls Home Base.\n\n"
             "ANNEXURE B shows the map as well as the elevation map of the Leopard Trail Run in the Baviaanskloof situated close to "
             "Willowmore.\n\nVisitors to the Baviaanskloof can also do a four-day hike, starting at the Cedar Falls Home Base.\n\nNOTE:\n"
             "• Day 1 of the trail run is Days 3 and 4 of the hike.\n• Day 2 of the trail run is Days 1 and 2 of the hike.\n• Trail (path "
             "through the natural landscape)",
     "figure": fig("2.2", "ANNEXURE B, MAP OF THE LEOPARD TRAIL RUN ROUTE: two loops of trail meet at the Cedar Falls Home Base, a pin under "
                   "a dark label box in the middle. The smaller loop on the left is labelled Day 2: Rhebok Valley along its far left end, "
                   "Gabriel's Pools marked on its upper side and Reflection Pools on its lower side. The larger loop on the right is "
                   "labelled Day 1: The Cauldron along its upper side near the home base, Fond Farewell and Birdsong Valley (with arrows) up "
                   "its long arm to the north, and Honeybush Hill and Inconvenient Truth along its lower side."), "items": q22},
    {"id": "2.2.3", "title": "Question 2.2.3", "kind": "Elevation map", "marks": 7,
     "lead": "The Leopard Trail Run is a two-day event, run on the outskirts of the camp, starting and ending at the Cedar Falls Home Base.\n\n"
             "ANNEXURE B shows the map as well as the elevation map of the Leopard Trail Run in the Baviaanskloof situated close to "
             "Willowmore.",
     "figure": fig("2.2.3", "ANNEXURE B, ELEVATION MAP OF THE LEOPARD TRAIL RUN ROUTE: two graphs of the height above sea level along the "
                   "route, distance run across the bottom. TRAIL RUN – DAY 1: distance marks at 5, 10, 15, 20, 25 and 30,5 km; heights "
                   "721 m, 1 000 m and 1 183 m marked up the side. The curve starts near 860 m, climbs to three sharp peaks near 1 183 m "
                   "between about 4 and 8 km, slopes steadily down to its lowest, about 721 m, near 18,5 km, climbs again to peaks above "
                   "1 000 m between about 23 and 27 km and ends at 861 m. TRAIL RUN – DAY 2: distance marks every 2,5 km up to 20 km, then "
                   "21,9 km; heights 864 m, 900 m, 975 m, 1 050 m and 1 173 m marked up the side, each with a dashed line across. The curve "
                   "starts at 864 m, climbs to about 1 050 m near 1 km, wanders down between about 900 m and 1 000 m to 10 km, climbs to "
                   "its highest point, 1 173 m, at the 12,5 km line, drops to about 1 050 m, rises to a second peak near 16,5 km, comes down "
                   "through the 1 050 m line at the 17,5 km line and finishes near the 900 m line at 21,9 km."), "items": q223},
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
    {"id": "5.1", "title": "Question 5.1", "kind": "Map and trip plan", "marks": 14,
     "lead": "Chris and Boipelo are planning a year-long trip, mostly along the A1 motorway, around Australia. It is the world's longest "
             "continuous road of 14 655 km that passes through every state and connects seven of its eight capitals.\n\nANNEXURE C is a map "
             "of Australia and the distances and driving times between the major cities and the states or territories. Next to it is the "
             "plan of their trip.",
     "figure": fig("5.1", "ANNEXURE C, two panels side by side. Left, MAP OF AUSTRALIA SHOWING THE A1 MOTORWAY, DISTANCES, DRIVING TIMES AND "
                   "STATES OR TERRITORIES: the A1 drawn as a thick line right round the mainland near the coast; KEY: STATE a triangle, City "
                   "a dot. Distances and driving times beside the road, clockwise from the north: Darwin to Cairns 2 850 km, 33 h 55 min; "
                   "Cairns to Brisbane 1 705 km, 20 h 40 min; Brisbane to Sydney 922 km, 10 h 30 min; Sydney to Melbourne 1 062 km, "
                   "13 h 40 min; Melbourne to Adelaide 738 km, 9 h 6 min; PERTH TO ADELAIDE 29 hours (no distance); Perth to Broome "
                   "2 811 km, 30 hours; Broome to Darwin 1 871 km, 21 h 13 min. Across the middle: DARWIN TO ADELAIDE 3 027 km 35 HOURS. "
                   "The states, with thin borders: Western Australia (the whole west), Northern Territory (the middle of the north), South "
                   "Australia (the middle of the south), Queensland (the north-east), New South Wales (the south-east), Victoria (the "
                   "south-east corner) and, across the sea to the south, Tasmania with Hobart. Right, PLANNED TRIP ALONG THE A1 MOTORWAY "
                   "AND OTHER ROADS: an outline of Australia with no borders, month labels joined by arrows: JAN in the south-east, FEB on "
                   "Tasmania, MAR on the south-east coast, APR up the east coast, MAY in the north-east, JUN in the middle of the north "
                   "(an arrow up to the north coast), JUL at the top, AUG in the north-west, SEP and OCT down the west coast, NOV in the "
                   "south-west and DEC in the middle of the south coast, an arrow from it pointing east."), "items": q51},
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

# every part that played as typed steps or num until Murci's ruling of 2026-10-10, now an authored whole-working mcq
CALC = ["1.2.1", "1.2.3", "1.3.1", "1.3.2", "1.3.4", "1.3.5", "2.1.2", "2.1.5", "2.1.6(a)", "2.1.6(b)", "2.2.3", "2.2.5", "3.1.2", "3.1.3",
        "3.2.1", "3.2.2", "3.2.3", "3.3.1", "3.3.2", "4.1.3", "4.1.4", "4.2.1", "4.2.2", "5.1.3", "5.1.5", "5.2.1", "5.3.2", "5.3.3(a)",
        "5.3.3(b)"]
CALC_MARKS = sum(i["marks"] for m in missions for i in m["items"] if i["n"] in CALC)
paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P2", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematical Literacy", "total": 150, "missions": missions}],
    "flags": [
        {"n": CALC[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every typed calculation plays as the memo's "
                                                   "working plus three built from common errors, 0 or full marks: " + ", ".join(CALC) +
                                                   f" ({len(CALC)} parts, {CALC_MARKS} marks). The right option is the memo's FIRST method; a "
                                                   "value the memo also accepts never appears in a wrong option: 2.1.6(b) takes the memo's "
                                                   "90 mm measurement (1 : 90 and 1 : 92, from 91 or 89 mm inside its ± 1 mm, are not offered); "
                                                   "4.2.1 takes 19 bricks a row (20 a row, 400 and 800 bricks are not offered); 4.2.2 takes "
                                                   "12,78 m² (R6 500 and R15 272,50, from 13 m², are not offered)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 5, 150 marks; per question 26, 31, 31, 29, 33), "
                                                           "hand-transcribed from scanned page images of the question paper and its ADDENDUM (no text "
                                                           "layer; ANNEXURES A, B and C) and from the memo's text and page images; no API call."},
        {"n": "5.1.2", "kind": "no_fit", "detail": "The memo marks the four months 1 + 1 + 1 (the first right month, the second, then ALL four). "
                                                   "Played as a list of four months worth 3 marks, each right month scores ¾: four right = 3, as "
                                                   "the memo; one right = ¾ (memo 1), two = 1½ (memo 2), three = 2¼ (memo 2)."},
        {"n": "5.1", "kind": "no_fit", "detail": "ANNEXURE C's '[Adapted from www.wilmap.com.au]' line is printed inside the map's frame, level "
                                                 "with the map's Key and just below Tasmania: a box that left it out would clip the Key or cut "
                                                 "Tasmania off, so the crop keeps the whole annexure frame, that line included."},
        {"n": "2.2.5", "kind": "memo_issue", "detail": "The memo reads the end of Day 2 as 900 m (the labelled height line); on the scan the curve "
                                                       "ends a little below that line (about 890 m, measured between the 900 m and 864 m lines), "
                                                       "which gives about 160 m. The conclusion (more than 100 m: CORRECT) holds either way. "
                                                       "Transcribed as printed: the right option takes the memo's 1 050 m (the curve does cross "
                                                       "the 1 050 m line at the 17,5 km line), 900 m and 150 m, and no wrong option uses 890 m."},
        {"n": "3.1.1", "kind": "no_fit", "detail": "Terms the memo marks in parts play all or nothing: 3.1.1 (MA + A; the duration in every common "
                                                   "written form) and 5.2.2 (RT + A order + 2 CA; the simplified ratio as a strict term)."},
        {"n": "5.2", "kind": "no_fit", "detail": "The picture of Uluru beside the lead is a photo only (no data) and is not cropped; its sentence "
                                                 "'A picture of Uluru is shown alongside.' is left out of the lead. The figure is the height "
                                                 "comparison diagram the parts read."},
        {"n": "2.1.6(b)", "kind": "memo_issue", "detail": "The memo's box reads 'Accept ± 1 mm deviation on measurement per province': the plan "
                                                          "has no provinces (a line carried over from another paper); read as ± 1 mm on the "
                                                          "measured length."},
        {"n": "4.2.1", "kind": "memo_issue", "detail": "The memo's two methods count different bricks: 19 a row of the double-brick wall × 20 rows "
                                                       "= 380 a door (760 for both), or 10 a row of a single wall × 20 rows = 200, 400 for the double "
                                                       "wall (800 for both); both give 2 pallets. The face diagram shows each row as nine whole "
                                                       "bricks and a half brick, so 19 counts the halves as halves and 20 as whole bricks. The "
                                                       "multiple choice's right option is the memo's first method (19, 380, 760, 2 pallets); 20 a "
                                                       "row, 400 and 800 appear in no option."},
        {"n": "3.2.3", "kind": "memo_issue", "detail": "The memo's fourth method writes the hole's area as 0,3142 ÷ 10 000 = 0,0000314 m², then "
                                                       "subtracts 0,00003142 m² (its result 0,00499578 m² and its answer 29,97 mℓ are right)."},
    ],
}
out = Path(__file__).parent / "out" / "ml-p2-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper, its scanned addendum and the "
                                                                       "memo PDF and their page images (no API call)",
                                                        "scope": "the whole paper, Questions 1 to 5 (2.1, 2.2 and 5.1 read the addendum's "
                                                                 "ANNEXURES A, B and C)"}, "paper": paper},
                                              indent=1, ensure_ascii=False), encoding="utf-8")
def shape(o):
    """(lines, trailing [reasons]): every option of one part must match, so the layout never points at the answer."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


at = []
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    for i in m["items"]:
        assert i["t"] not in ("steps", "num"), (i["n"], "a typed number: Murci's 2026-10-10 ruling makes it an authored mcq")
        if i["n"] in CALC:   # an authored whole-working mcq: 4 distinct options, one shape, the right index in 0-3, a working of 2+ lines
            assert i["t"] == "mcq" and i["q"].endswith(WORK), i["n"]
            assert len(i["opts"]) == 4 and len(set(i["opts"])) == 4, (i["n"], "4 distinct options")
            assert len({shape(o) for o in i["opts"]}) == 1, (i["n"], [shape(o) for o in i["opts"]])
            assert shape(i["opts"][0])[0] >= 2 and 0 <= i["a"] <= 3, i["n"]
            at.append("ABCD"[i["a"]])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert sorted(i["n"] for m in missions for i in m["items"] if i["n"] in CALC) == sorted(CALC) and len(at) == len(CALC), "a CALC part is missing"
print("authored right options:", {k: at.count(k) for k in "ABCD"}, "over", len(at), "parts,", CALC_MARKS, "marks")
assert max(at.count(k) for k in "ABCD") - min(at.count(k) for k in "ABCD") <= 1, "spread the right letter evenly over A-D"
total = sum(i["marks"] for m in missions for i in m["items"])
print("total:", total)
# the totals the paper prints: [26] [31] [31] [29] [33] under its questions, 150 on its cover
per_q = {}
for m in missions:
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + sum(i["marks"] for i in m["items"])
assert per_q == {"1": 26, "2": 31, "3": 31, "4": 29, "5": 33}, per_q
assert total == paper["paper"]["total_marks"] == paper["sections"][0]["total"] == 150, total
