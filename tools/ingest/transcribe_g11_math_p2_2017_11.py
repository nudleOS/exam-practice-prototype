"""Grade 11 Mathematics P2 Nov 2017 (DBE common paper), the whole paper (Questions 1 to 12, 150 marks, 3 hours as the cover prints
them: statistics, analytical geometry, trigonometry, measurement, Euclidean geometry), hand-transcribed into the catalogue format,
then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working are the paper's and
the memo's own (its English); clues and figure captions are ours. No API call: the transcription is the source, kept in git (out/
is not). The question paper (13 pages, English only), the memo (19 pages, bilingual) and the answer book (24 pages) are SCANS: the
question paper and the answer book have no text layer, the memo's text layer turns fractions into columns of digits; everything was
read from their page images rendered at 150 dpi (the answer book at 100 dpi), with crops at 200-250 dpi where a label, an angle
number or a memo line mattered (the memo's 3.4.3 reason and its 6.2.3 graph, the Question 10 diagram, the answer book's 6.2.3 grid).

  python tools/ingest/transcribe_g11_math_p2_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Mathematics P2 Nov 2017 Eng.pdf" "uploads/Grade 11 Mathematics P2 Nov 2017 MG Afr & Eng.pdf" --id g11-math-p2-2017-11 --from-json --answer-book "uploads/Grade 11 Mathematics P2 Nov 2017 Answer Book Afr & Eng.pdf"

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p2_2025_11.py and the same grade's other year,
transcribe_g11_math_p2_2018_11.py):
  every part the memo WORKS OUT in two or more lines (an interquartile range, a value of y, a combined mean, a read-off percentage, a
  gradient, an equation, coordinates, a length, a radius, an angle, a simplification, a trigonometric value, a general solution, an
  area, an inequality, a surface area) and every proof or 'show that' -> authored whole-working multiple choice, `work`: the memo's
  FIRST method line by line (a geometry statement with its [reason] at the line's end, "{a}/{b}" a stacked fraction, never nested)
  and three workings each built from a DIFFERENT real error (a wrong formula, ratio, identity, theorem or congruency case, a sign
  slip, a misread value, the wrong side or quadrant, a wrong reason, circular reasoning, one value tried, the calculator in radians
  or used where the stem forbids it), every option of a part the same layout (`shape`), the right one's place spread over A-D across
  the paper; the part keeps its marks, all or nothing. In a 'show that' or 'prove' (5.2, 5.4, 7.1, 8.1, 9.1, 11.1, 11.2, 12.2) every
  option ends in the given result (or, starting from it, in a true statement): a wrong one reaches it through a wrong step or
  reason. The memo's OR methods and values are other right routes and never a wrong option.
  An answer the memo states with no working (the five-number summary, the completed table, the modal class, a range, the
  intersections, four angles with reasons) -> authored multiple choice of answers: the memo's and three common errors; the skewness
  (1.1.3) -> the Grade 12 model's three choices. One number with no working (1.2.2, 2.2, 6.2.1) stays num; the ogive 2.4 -> draw
  (self-checked against the memo's criteria); the graphs of f and g (6.2.3), which the memo marks by features -> draw with a
  `build` "sketch" (2026-10-11: two trigonometric graphs placed on a grid, marked online).
  Where a part's stem, options or criteria show an EARLIER part's answer it carries "after" (the GATES assert at the end).
Missions: Questions 2, 3, 4, 6, 7, 8, 10, 11 and 12 share one stem (and table or diagram) each, so each is one mission (Question
6's mission lead is its 6.2 sentence, so that 6.2.4, whose options show 6.1's solutions, can open after 6.1: a gate is looked up
inside its mission); Questions 1, 5 and 9 change their stem part-way, so their numbered groups are missions (1.1, 1.2, 5.1 ... 9.2).
No figure comes from the answer book: its Question 2 table repeats the paper's (typed as the mission's table), its ogive grid (2.4)
and its 6.2.3 grid are blank answer spaces (the draw memo and the sketch's grid describe them), and its other diagrams repeat the
question paper's.
Figure boxes are measured in PDF points (page 595 x 841, read from the PDF) from the ink on the scan (scratch tool
lower/g11-math-p2-2017-11/figs.py) and checked on a contact sheet with ingest's 1% pad applied."""
import json
import re
from pathlib import Path

PID = "g11-math-p2-2017-11"
W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q1.1": [3, 48.6, 210.6, 542.6, 269.6],    # the box-and-whisker diagram on its number line
    "Q3": [5, 118.9, 192.2, 477.0, 393.8],     # the axes and ABCD with T (a scan speck above the axes left out)
    "Q4": [6, 47.7, 207.7, 570.9, 462.6],      # the axes and △ABC with E, α and θ
    "Q5.3": [7, 105.8, 330.6, 459.5, 562.9],   # the axes, R, P, T, α and β
    "Q7": [8, 153.4, 433.4, 421.8, 590.4],     # △PQR
    "Q8": [9, 181.0, 195.2, 350.5, 463.5],     # the pyramid (its formula box, just right of T, is typed in the lead; x1 kept 2 pt inside T so the padded crop misses the box)
    "Q9.1": [10, 186.7, 219.7, 370.1, 401.6],  # the circle with chord RS and OT
    "Q9.2": [10, 202.2, 511.7, 376.0, 697.0],  # the circle with chord AB, F, O and D
    "Q10": [11, 171.7, 188.6, 496.7, 376.2],   # the circle SVQR with centre M and the tangents to P
    "Q11": [12, 130.2, 180.2, 433.6, 454.2],   # the circle with diameter BA, D, C and E
    "Q12": [13, 39.3, 216.7, 556.7, 524.4]}    # the two touching circles


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


num = lambda n, q, a, tol, unit, clues, marks=1, **kw: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol,
                                                        "unit": unit, **kw}
draw = lambda n, q, marks, criteria, clues, memo="", **kw: {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                           "criteria": [{"text": t, "marks": m} for t, m in criteria],
                                                           **({"memo": memo} if memo else {}), **kw}

ANSWER = "\n\nChoose the correct answer."
WORK = "\n\nChoose the correct working."
AUTHORED = []   # the whole-working multiple choice, in paper order
DP2 = 0.006     # a value keyed at two decimal places: 30,94 accepted, 30,93 and 30,95 not


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues, **kw):
    """A worked part as authored multiple choice: opts are the memo's FIRST working and three workings built from common errors,
    one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing. kw: "after"."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    assert not any(re.search(r"\{[^{}]*\{", o) for o in opts), (n, "a nested brace: the app draws one level of {a}/{b}")
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


# ---- QUESTION 1, the question paper page 3 and the memo pages 2-3 ----
FIVE = ("\n\nEach option lists the minimum, the lower quartile, the median, the upper quartile and the maximum, in this order.")
q1a = [
    mcq("1.1.1", "Write down the five-number summary of the data." + FIVE + ANSWER, [
        "(10 ; 17 ; 30 ; 38 ; 66)",     # the number line's two ends for the minimum and the maximum
        "(12 ; 17 ; 27,5 ; 38 ; 65)",   # the median taken as the middle of the box
        "(12 ; 17 ; 30 ; 38 ; 65)",     # the memo
        "(12 ; 18 ; 30 ; 38 ; 64)"], 2,  # the odd values read at the nearest labelled mark
        ["Which parts of the diagram mark the smallest and the largest amounts?", "What do the two ends of the box and the line inside it "
                                                                                   "stand for?"], marks=2),
    work("1.1.2", "Determine the interquartile range.", 1, [
        "IQR = maximum − minimum\n= 65 − 12\n= 53",            # the range
        "IQR = Q₃ − Q₁\n= 38 − 17\n= 21",                      # the memo
        "IQR = Q₃ − median\n= 38 − 30\n= 8",                   # the upper half of the box only
        "IQR = {Q₃ − Q₁}/{2}\n= {38 − 17}/{2}\n= 10,5"], 1,    # halved: the semi-interquartile range
        ["Which two values of the five-number summary does the interquartile range use?", "Does the interquartile range measure the spread of "
                                                                                          "all the data or of its middle half?"],
        after=["1.1.1"]),
    mcq("1.1.3", "Comment on the skewness of the data." + ANSWER, ["Symmetrical", "Skewed to the right (positively skewed)",
                                                                  "Skewed to the left (negatively skewed)"], 1,
        ["Is the median closer to the lower quartile or to the upper quartile?", "Which whisker is the longer one, and which way does the "
                                                                                 "tail run?"]),
]
q1b = [
    work("1.2.1", "Calculate the value of y if the mean for this data set is 41.", 2, [
        "Mean = {439 + y}/{12}\n41 = {439 + y}/{12}\n439 + y = 492\ny = 53",      # divided by the 12 known values
        "Mean = {439 + y}/{13}\n41 = {439 + y}/{13}\n439 + y = 533\ny = 972",     # 439 added instead of subtracted
        "Mean = {439}/{13} + y\n41 = 33,77 + y\ny = 41 − 33,77\ny = 7,23",       # only the known total divided by 13
        "Mean = {439 + y}/{13}\n41 = {439 + y}/{13}\n439 + y = 533\ny = 94"], 3,  # the memo
        ["What is the total of all thirteen values, with y still unknown?", "How many values do you divide that total by?"]),
    num("1.2.2", "If y = 94, calculate the standard deviation of the data.", 30.94, DP2, "hours",
        ["Which calculator mode works out the standard deviation of a list of data?", "Is this the whole group (σ) or a sample of it?"],
        after=["1.2.1"]),
    work("1.2.3", "The mean time before another group of 6 students needed to recharge the batteries of their cellphones was 18 hours. "
         "Combine these groups and calculate the overall mean time needed for these two groups to recharge the batteries of their "
         "cellphones.", 3, [
        "41 × 13 = 533\n6 × 18 = 108\n{533 + 108}/{19} = {641}/{19} = 33,74 hours",    # the memo
        "41 × 13 = 533\n6 × 18 = 108\n{533 + 108}/{2} = {641}/{2} = 320,5 hours",      # divided by the 2 groups
        "Mean 1 = 41\nMean 2 = 18\n{41 + 18}/{2} = {59}/{2} = 29,5 hours",             # the mean of the two means
        "41 × 13 = 533\n6 × 18 = 108\n{533 + 108}/{13} = {641}/{13} = 49,31 hours"], 0,  # divided by the first group's 13 only
        ["What is each group's total time: its mean times its number of students?", "How many students are there in the two groups "
                                                                                    "together?"], after=["1.2.1"]),
]

# ---- QUESTION 2, the question paper page 4 and the memo pages 3-4 ----
CALLS = {"head": ["AGE OF PERSON IN SURVEY", "FREQUENCY", "CUMULATIVE FREQUENCY"],
         "rows": [["20 < x ≤ 30", "7", "7"], ["30 < x ≤ 40", "", "27"], ["40 < x ≤ 50", "25", ""], ["50 < x ≤ 60", "", "64"],
                  ["60 < x ≤ 70", "", "72"], ["70 < x ≤ 80", "4", ""], ["80 < x ≤ 90", "", "80"]]}
GAPS = ("\n\nEach option gives the missing frequencies (of 30 < x ≤ 40, 50 < x ≤ 60, 60 < x ≤ 70 and 80 < x ≤ 90), then the missing "
        "cumulative frequencies (of 40 < x ≤ 50 and 70 < x ≤ 80).")
READ = "At 54 years the ogive reads "
q2 = [
    mcq("2.1", "Complete the frequency and cumulative frequency columns in the table given in the ANSWER BOOK." + GAPS + ANSWER, [
        "Frequencies: 20 ; 12 ; 8 ; 4\nCumulative frequencies: 52 ; 76",      # the memo
        "Frequencies: 27 ; 64 ; 72 ; 80\nCumulative frequencies: 52 ; 76",    # the cumulative frequencies copied into the frequency column
        "Frequencies: 20 ; 39 ; 8 ; 4\nCumulative frequencies: 52 ; 76",      # 64 − 25: the frequency above taken off, not the running total
        "Frequencies: 20 ; 12 ; 8 ; 4\nCumulative frequencies: 47 ; 80"], 0,  # each running total adds the class above's frequency
        ["A cumulative frequency is a running total: how do you get one class's own frequency back from it?", "How do you get the next "
                                                                                                              "running total from the one "
                                                                                                              "before it?"], marks=4),
    num("2.2", "How many people participated in this survey?", 80, 0, "people",
        ["What does a cumulative frequency count?", "Which class's running total has counted every person in the survey?"]),
    mcq("2.3", "Write down the modal class." + ANSWER, ["80 < x ≤ 90", "30 < x ≤ 40", "50 < x ≤ 60", "40 < x ≤ 50"], 3,
        ["Which column shows how many people are in each class on its own?", "What does the mode of a data set describe?"]),
    draw("2.4", "Draw an ogive (cumulative frequency graph) to represent the data on the grid given in the ANSWER BOOK.", 3, [
        ["Grounding at (20 ; 0)", 1],
        ["Plotting at the upper limits: (30 ; 7), (40 ; 27), (50 ; 52), (60 ; 64), (70 ; 72), (80 ; 76), (90 ; 80)", 1],
        ["Shape: a smooth curve", 1]],
        ["At which age does the first class start, before anyone has been counted?", "Against which end of each class do you plot its "
                                                                                     "cumulative frequency?"],
        memo="The answer book gives a grid: Cumulative Frequency from 0 to 90 up (labelled every 10, a fine line every 2) and Age of person "
             "surveyed from 0 to 100 along (labelled every 10, a fine line every 2). The memo's ogive: (20 ; 0), (30 ; 7), (40 ; 27), "
             "(50 ; 52), (60 ; 64), (70 ; 72), (80 ; 76) and (90 ; 80), joined by a smooth curve.", after=["2.1"]),
    work("2.5", "Determine the percentage of marketing calls received by people older than 54 years.", 3, [
        READ + "58\n80 − 58 = 22\n{58}/{80} × 100 = 72,5%",      # the people up to 54 used
        READ + "58\n80 − 58 = 22\n{22}/{100} × 100 = 22%",       # divided by 100, not by the 80 people
        READ + "58\n80 − 58 = 22\n{22}/{80} × 100 = 27,5%",      # the memo (it accepts a reading of 56 to 59: 30% to 26,25%)
        READ + "52\n80 − 52 = 28\n{28}/{80} × 100 = 35%"], 2,    # the class end 50 read for 54
        ["How many people are 54 or younger, read from the ogive at 54?", "How many people are older than 54, and what fraction of everyone "
                                                                          "is that?"], after=["2.1"]),
]

# ---- QUESTION 3, the question paper page 5 and the memo pages 5-6 ----
BD = "BD: y = −{1}/{2}x + 9\nm(BD) = −{1}/{2}\n"
PS = "y − y₁ = m(x − x₁)\n"
T0 = "2x − 1 = −{1}/{2}x + 9\n"
AT = "AT = √((4 − (−2))² + (7 − (−5))²)\n= √180 = 6√5\n"
DIA = " is a diameter [converse ∠ in semi-circle]\nRadius = "
q3 = [
    work("3.1", "Determine the gradient of line AC.", 2, [
        BD + "m(AC) = 2",                                 # the memo
        "BD: y = −x + 18\nm(BD) = −1\nm(AC) = 1",         # 2y never divided by 2
        BD + "m(AC) = −{1}/{2}",                          # perpendicular taken as parallel
        BD + "m(AC) = −2"], 0,                            # the reciprocal without the sign change
        ["How do you rewrite 2y + x = 18 in the form y = mx + c?", "AC ⊥ BD: how are their gradients related?"]),
    work("3.2", "Determine the equation of AC in the form y = mx + c.", 2, [
        PS + "y − (−5) = 2(x − 2)\ny = 2x − 9",           # A's x without its sign
        PS + "y − (−2) = 2(x − (−5))\ny = 2x + 8",        # A's x and y swapped
        PS + "y − (−5) = 2(x − (−2))\ny = 2x − 1",        # the memo
        PS + "y − (−5) = 2(x − (−2))\ny = 2x + 9"], 2,    # the 5 moved across without its sign change
        ["Which point on AC do you know, and what is the gradient of AC?", "How do you substitute a point and a gradient into y − y₁ = "
                                                                           "m(x − x₁)?"], after=["3.1"]),
    work("3.3", "If the equation of AC is y = 2x − 1, calculate the coordinates of T.", 3, [
        T0 + "{3}/{2}x = 10\nx = {20}/{3}\ny = 2({20}/{3}) − 1 = {37}/{3}\nT({20}/{3} ; {37}/{3})",   # −½x moved without its sign change
        T0 + "{5}/{2}x = 8\nx = {16}/{5}\ny = 2({16}/{5}) − 1 = {27}/{5}\nT({16}/{5} ; {27}/{5})",      # −1 moved without its sign change
        T0 + "{5}/{2}x = 10\nx = 25\ny = 2(25) − 1 = 49\nT(25 ; 49)",                                   # multiplied by 5/2 instead of divided
        T0 + "{5}/{2}x = 10\nx = 4\ny = 2(4) − 1 = 7\nT(4 ; 7)"], 3,                                    # the memo
        ["T lies on both diagonals: what can you do with the equations of AC and BD?", "Once you have x, which equation gives y most easily?"],
        after=["3.2"]),
    work("3.4.1", "If ABCD is a kite with AB = BC: Determine the coordinates of C", 2, [
        "4 = {−2 + x}/{2}\nx = 6\n7 = {−5 + y}/{2}\ny = 12\nC(6 ; 12)",       # the 2 never multiplied across
        "4 = {−2 + x}/{2}\nx = 10\n7 = {−5 + y}/{2}\ny = 19\nC(10 ; 19)",     # the memo
        "x = {−2 + 4}/{2}\nx = 1\ny = {−5 + 7}/{2}\ny = 1\nC(1 ; 1)",         # the midpoint of A and T worked out instead
        "4 = {−2 + x}/{2}\nx = 10\n7 = {−5 + y}/{2}\ny = 9\nC(10 ; 9)"], 1,   # 14 − 5 for 14 + 5
        ["In a kite with AB = BC, what does the diagonal BD do to the diagonal AC?", "If T is the midpoint of AC, how do you work back from A "
                                                                                     "and T to C?"], after=["3.3"]),
    work("3.4.2", "If ABCD is a kite with AB = BC: Calculate the length of BT", 4, [
        AT + "BT² = AB² + AT² [Pythagoras]\nBT = √(15² + (√180)²)\n= √405 = 9√5",                     # adds: AB taken as a shorter side
        "AT = √((4 − (−2))² + (7 − 5)²)\n= √40 = 2√10\nBT² + AT² = AB² [Pythagoras]\nBT = √(15² − (√40)²)\n= √185 = 13,60",   # −(−5) taken as −5
        AT + "BT² + AT² = AB² [Pythagoras]\nBT = √(15² − (√180)²)\n= √45 = 3√5",                      # the memo
        AT + "BT² + AT² = AB² [Pythagoras]\nBT = 15 − √180\n= 15 − 6√5 = 1,58"], 2,                   # the root of a difference taken as a difference
        ["Which right-angled triangle has BT as a side and AB = 15 as its hypotenuse?", "How long is AT, from A and T?"], after=["3.3"]),
    work("3.4.3", "If ABCD is a kite with AB = BC: Write down the length of the radius of the circle passing through points B, C and T", 2, [
        "BC" + DIA + "{15}/{2} = 7,5 units",                          # the memo (its first form '[subt. right ∠]')
        "BC is a diameter [∠ in semi-circle]\nRadius = {15}/{2} = 7,5 units",   # the theorem, not its converse
        "BC" + DIA + "15 units",                                      # the diameter taken as the radius
        "BT" + DIA + "{3√5}/{2} = 3,35 units"], 0,                    # BT, an arm of the right angle, as the diameter
        ["What size is BT̂C, and what does that angle tell you about the chord BC?", "Which side of the kite is equal to BC?"],
        after=["3.4.2"]),
]

# ---- QUESTION 4, the question paper page 6 and the memo pages 7-8 ----
E0 = "y − 12 = {5}/{3}(x − 4)\n"
TA = "tan α = m(AB)\ntan α = "
INC = "Inclination of BC = 76° + 59° = 135° [ext ∠ of △]\ntan 135° = m(BC)\nm(BC) = −1\n"
q4 = [
    work("4.1", "Calculate the gradient of AB.", 2, [
        "m(AB) = {4 − (−5)}/{12 − (−3)}\n= {9}/{15} = {3}/{5}",      # x over y
        "m(AB) = {12 − 3}/{4 − (−5)}\n= {9}/{9} = 1",                # −(−3) taken as −3
        "m(AB) = {12 − (−3)}/{−5 − 4}\n= {15}/{−9} = −{5}/{3}",      # B − A on top, A − B below
        "m(AB) = {12 − (−3)}/{4 − (−5)}\n= {15}/{9} = {5}/{3}"], 3,  # the memo (OR A − B on top and below)
        ["Which formula gives the gradient of a line through two points?", "Do you subtract the coordinates in the same order on top and "
                                                                           "below?"]),
    work("4.2", "Determine the coordinates of point E.", 3, [
        E0 + "0 − 12 = {5}/{3}(x − 4)\nx = −{56}/{5}\nE(−{56}/{5} ; 0)",   # −20 moved across without its sign change
        E0 + "0 − 12 = {5}/{3}(x − 4)\nx = −{16}/{5}\nE(−{16}/{5} ; 0)",   # the memo (OR the gradient of EB or EA set equal to 5/3)
        E0 + "y − 12 = {5}/{3}(0 − 4)\ny = {16}/{3}\nE(0 ; {16}/{3})",     # x = 0 put in: the y-intercept
        E0 + "0 − 12 = {5}/{3}(x − 4)\nx = −16\nE(−16 ; 0)"], 1,           # multiplied by 5/3 instead of divided
        ["E lies on the x-axis: what is its y-coordinate?", "Which equation of AB can you write from its gradient and the point B?"],
        after=["4.1"]),
    work("4.3", "Determine the size of α. Round off to the nearest whole number.", 2, [
        TA + "{3}/{5}\nα = 31°",       # run over rise
        TA + "−{5}/{3}\nα = 121°",     # the gradient's sign changed
        TA + "{5}/{3}\nα = 59°",       # the memo
        TA + "{5}/{3}\nα = 1°"], 2,    # the calculator in radians (1,03)
        ["How is the angle of inclination of a line related to its gradient?", "Is your calculator in degree mode?"], after=["4.1"]),
    work("4.4", "If θ = 76°, determine the equation of the line through A parallel to BC.", 5, [
        INC + "y − (−3) = −1(x − (−5))\ny = −x − 8",                                                     # the memo
        "Inclination of BC = 180° − 76° − 59° = 45° [sum of ∠s in △]\ntan 45° = m(BC)\nm(BC) = 1\ny − (−3) = 1(x − (−5))\ny = x + 2",   # the angle inside △EBC at C as the inclination
        INC + "y − 12 = −1(x − 4)\ny = −x + 16",                                                         # through B: that is BC itself
        INC + "y − 3 = −1(x − 5)\ny = −x + 8"], 0,                                                       # A's signs dropped
        ["In △EBC, how is the angle that BC makes with the positive x-axis related to the angles at E and at B?", "What do parallel lines "
                                                                                                                 "have in common?"],
        after=["4.3"]),
]

# ---- QUESTION 5, the question paper page 7 and the memo pages 8-10 ----
RED = "= cos x.(−cos x) + {sin x}/{cos x}.cos x.(−sin x)\n= −cos² x − sin² x\n= −(cos² x + sin² x)\n"
SP = "= (−{1}/{√2})({1}/{√3}) ÷ {√3}/{2}\n= −{2}/{3√2}\n= −{√2}/{3} = RHS"
PY = "x² + y² = r² [Pythagoras]\n"
TC = "tan θ.cos² θ = {sin θ}/{cos θ} × cos² θ = sin θ.cos θ\nLHS = {sin θ − sin θ.cos θ}/{cos θ − "
q51 = [
    work("5.1", "Simplify fully:\nsin(90° − x).cos(180° + x) + tan x.cos x.sin(x − 180°)", 6, [
        "= cos x.(−cos x) + {sin x}/{cos x}.cos x.(sin x)\n= −cos² x + sin² x\n= −(cos² x − sin² x)\n= 1 − 2cos² x",   # sin(x − 180°) as sin x
        "= cos x.(cos x) + {sin x}/{cos x}.cos x.(−sin x)\n= cos² x − sin² x\n= (1 − sin² x) − sin² x\n= 1 − 2sin² x",  # cos(180° + x) as cos x
        RED + "= 1",                                                                                                  # the minus lost at the end
        RED + "= −1"], 3,                                                                                             # the memo
        ["What does each reduction formula turn sin(90° − x), cos(180° + x) and sin(x − 180°) into?", "Which identity links sin² x and "
                                                                                                      "cos² x?"]),
]
q52 = [
    work("5.2", "Prove, WITHOUT using a calculator, that\n(sin 315°.tan 210°.sin 190°)/(cos 100°.sin 120°) = −√2/3", 6, [
        "LHS = {(−sin 45°)(−tan 30°)(−sin 10°)}/{(sin 10°)(sin 60°)}\n" + SP,     # tan 210° and cos 100° both with the wrong sign: the slips cancel
        "LHS = {(−sin 45°)(tan 30°)(−sin 10°)}/{(−sin 10°)(sin 60°)}\n" + SP,     # the memo
        "LHS = {(−sin 45°)(tan 30°)(−sin 10°)}/{(−cos 10°)(sin 60°)}\n" + SP,     # cos 100° as −cos 10°, then cancelled with −sin 10°
        "LHS = {sin 315°.tan 210°.sin 190°}/{cos 100°.sin 120°}\n= {(−0,7071)(0,5774)(−0,1736)}/{(−0,1736)(0,8660)}\n= −0,4714\n"
        "= −{√2}/{3} = RHS"], 1,                                                   # the calculator used: no proof
        ["Which reduction formulae turn 315°, 210°, 190°, 100° and 120° into acute angles, and with which signs?", "Which factors are "
                                                                                                                   "special angles you can "
                                                                                                                   "write as surds, and "
                                                                                                                   "which two cancel?"]),
]
q53 = [
    work("5.3.1", "The value of tan α", 3, [
        PY + "x² + 3² = 5²\nx = 4\ntan α = {3}/{4}",        # the memo
        PY + "x² + 3² = 5²\nx = 4\ntan α = {4}/{3}",        # x over y
        PY + "x² + 3² = 5²\nx = −4\ntan α = −{3}/{4}",      # the negative root: R is in the first quadrant
        PY + "x² = 3² + 5²\nx = √34\ntan α = {3}/{√34}"], 0,  # adds the squares
        ["sin α = 3/5: which two of x, y and r does that give you for R?", "Which two of x, y and r does tan α use?"]),
    work("5.3.2", "The value of sin β", 3, [
        "sin β = sin(180° − α)\n= sin α\n= {3}/{5}",       # β taken as 180° − α
        "sin β = sin(180° + α)\n= sin α\n= {3}/{5}",       # no sign change in the reduction
        "sin β = sin(180° + α)\n= −sin α\n= −{3}/{5}",     # the memo
        "sin β = sin(180° + α)\n= −cos α\n= −{4}/{5}"], 2,  # a co-function swap at 180°
        ["P lies on RO extended: how is β related to α?", "In which quadrant is OP, and what sign does sine have there?"], after=["5.3.1"]),
    work("5.3.3", "The coordinates of P", 4, [
        "{y}/{5} = −{3}/{5}\ny = −3\nx = −4\nP(−4 ; −3)",      # OP taken as 5, not 2 × 5
        "{y}/{10} = {3}/{5}\ny = 6\nx = 8\nP(8 ; 6)",          # the sign of sin β lost: that point is on OR
        "{y}/{10} = −{3}/{5}\ny = −6\nx = −8\nP(−6 ; −8)",     # the coordinates written in the wrong order
        "{y}/{10} = −{3}/{5}\ny = −6\nx = −8\nP(−8 ; −6)"], 3,  # the memo
        ["OP = 2 RO: how long is OP?", "How does sin β = y/r give you the y-coordinate of P, and in which quadrant is P?"],
        after=["5.3.1", "5.3.2"]),
]
q54 = [
    work("5.4", "Prove the identity:\n(sin θ − tan θ.cos² θ)/(cos θ − 1 + sin² θ) = tan θ", 4, [
        "{sin θ − tan θ.cos² θ}/{cos θ − 1 + sin² θ} = tan θ\nsin θ − tan θ.cos² θ = tan θ(cos θ − 1 + sin² θ)\n"
        "sin θ − sin θ.cos θ = tan θ(cos θ − cos² θ)\nsin θ − sin θ.cos θ = sin θ − sin θ.cos θ\nso LHS = RHS",           # starts from the answer
        TC + "(1 − sin² θ)}\n= {sin θ − sin θ.cos θ}/{cos θ − cos² θ}\n= {sin θ(1 − cos θ)}/{cos θ(1 − cos θ)}\n= tan θ = RHS",   # the memo (OR −1 + sin² θ = −cos² θ)
        "Let θ = 30°\nLHS = {sin 30° − tan 30°.cos² 30°}/{cos 30° − 1 + sin² 30°}\n= {0,0670}/{0,1160}\n= 0,5774\n= tan 30° = RHS",   # one value tried: no proof
        TC + "1 + sin² θ}\n= {sin θ − sin θ.cos θ}/{cos θ + cos² θ}\n= {sin θ(1 − cos θ)}/{cos θ(1 + cos θ)}\n= tan θ = RHS"], 1,  # −1 + sin² θ as +cos² θ, then 1 − cos θ cancelled with 1 + cos θ
        ["How can you write tan θ in terms of sin θ and cos θ?", "Which identity turns −1 + sin² θ into a single term?"]),
]

# ---- QUESTION 6, the question paper page 8 and the memo pages 11-12 ----
S61 = "sin(x − 30°) = sin(90° − 2x)\n"
TWO = "x − 30° = 90° − 2x + 360°.k or x − 30° = 180° − (90° − 2x) + 360°.k\n3x = 120° + 360°.k or −x = 120° + 360°.k\n"
# 6.2.3, built on a grid (2026-10-11, as transcribe_math_p1_2025_11.py 4.5, here two trigonometric graphs on one set of axes): each memo
# criterion is features (or a shape) whose marks add up to its mark. The memo's 'shape of f' carries f's two turning points (0 marks),
# which fix the curve (one x-intercept leaves sin(x − 30°) open); 'shape of g' carries g's third x-intercept (−45°) and its other turning
# point (0 ; 1), 0 marks each, so that the chips of one name ("x-intercept", "turning point") are every such point of g in the interval
# and are matched as a set. The end points and f's y-intercept, which the memo does not mark, are not features (the domain draws the ends).
SK = {"kind": "sketch", "family": "sin", "b": 1, "x": [-90, 180, 15], "y": [-2, 2, 0.5], "domain": [-90, 180], "features": [
    {"id": "fx", "kind": "point", "label": "x-intercept", "at": [30, 0], "tol": 0, "marks": 1, "crit": 0, "graph": "f"},
    {"id": "ft1", "kind": "point", "label": "turning point", "at": [-60, -1], "tol": 0, "marks": 0, "crit": 1, "graph": "f", "turn": True},
    {"id": "ft2", "kind": "point", "label": "turning point", "at": [120, 1], "tol": 0, "marks": 0, "crit": 1, "graph": "f", "turn": True},
    {"id": "gx1", "kind": "point", "label": "x-intercept", "at": [45, 0], "tol": 0, "marks": 1, "crit": 2, "graph": "g"},
    {"id": "gx2", "kind": "point", "label": "x-intercept", "at": [135, 0], "tol": 0, "marks": 0, "crit": 2, "graph": "g"},
    {"id": "gx3", "kind": "point", "label": "x-intercept", "at": [-45, 0], "tol": 0, "marks": 0, "crit": 3, "graph": "g"},
    {"id": "gt2", "kind": "point", "label": "turning point", "at": [0, 1], "tol": 0, "marks": 0, "crit": 3, "graph": "g", "turn": True},
    {"id": "gt1", "kind": "point", "label": "turning point", "at": [90, -1], "tol": 0, "marks": 1, "crit": 4, "graph": "g", "turn": True}],
      "graphs": [{"id": "f", "family": "sin", "label": "f", "b": 1, "domain": [-90, 180],
                  "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 1}},
                 {"id": "g", "family": "cos", "label": "g", "b": 2, "domain": [-90, 180],
                  "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 3}}]}
q6 = [
    work("6.1", "Determine the general solution for sin(x − 30°) = cos 2x", 5, [
        S61 + "x − 30° = 90° − 2x + 360°.k\n3x = 120° + 360°.k\nx = 40° + 120°.k ; k ∈ Z",                    # the second case lost
        S61 + "x − 30° = 90° − 2x + 360°.k or x − 30° = 180° + (90° − 2x) + 360°.k\n3x = 120° + 360°.k or 3x = 300° + 360°.k\n"
        "x = 40° + 120°.k or x = 100° + 120°.k ; k ∈ Z",                                                      # sine's second angle as 180° + the angle
        S61 + TWO + "x = 40° + 120°.k or x = −120° + 360°.k ; k ∈ Z",                                          # the memo (OR cos(120° − x) = cos 2x)
        S61 + TWO + "x = 40° + 360°.k or x = −120° + 360°.k ; k ∈ Z"], 2,                                      # 360°.k not divided by 3
        ["Which co-function identity writes cos 2x as a sine?", "sin A = sin B in two quadrants: what are the two general forms that follow?"]),
    num("6.2.1", "Write down the period of g.", 180, 0, "°",
        ["After how many degrees does cos x complete one full wave?", "What does the 2 in cos 2x do to that?"]),
    mcq("6.2.2", "State the range of f." + ANSWER, ["−1 < y < 1", "−1 ≤ y ≤ 1", "y ≥ −1", "−1 ≤ x ≤ 1"], 1,
        ["What are the lowest and highest values of sin(x − 30°)?", "Does f reach those values, so that the end points belong to the range?"],
        marks=2),
    {**draw("6.2.3", "On the grid provided in the ANSWER BOOK, draw the graphs of f and g for x ∈ [−90° ; 180°].\nClearly show ALL "
            "intercepts with the axes, turning points and end points.", 5, [
        ["f: x-intercept at 30°", 1], ["Shape of f", 1], ["g: x-intercepts at 45° and 135°", 1], ["Shape of g", 1],
        ["g: turning point at (90° ; −1)", 1]],
        ["Where is sin(x − 30°) equal to 0, and where does it reach 1 and −1?", "Where does cos 2x start a wave at its highest point, and "
                                                                                "after how many degrees is it lowest?"],
        memo="The answer book gives a grid: x from −90° to 180° (a line every 30°) and y from −2 to 2 (a line every 0,5). The memo's graphs: "
             "f(x) = sin(x − 30°) falls from (−90° ; −0,87) to its minimum (−60° ; −1), rises through (0 ; −0,5) and (30° ; 0) to its "
             "maximum (120° ; 1) and falls to (180° ; 0,5); g(x) = cos 2x rises from (−90° ; −1) through (−45° ; 0) to (0 ; 1), falls "
             "through (45° ; 0) to (90° ; −1) and rises through (135° ; 0) to (180° ; 1)."), "build": SK},
    mcq("6.2.4", "Write down the x-coordinates of the points of intersection of f and g in the interval x ∈ [−90° ; 180°]." + ANSWER, [
        "x = 40° ; x = 160°",                           # only k = 0 and k = 1
        "x = 30° ; x = 45° ; x = 135°",                 # the x-intercepts of f and g, not where they meet
        "x = −80° ; x = 40° ; x = 160°",                # the memo
        "x = −120° ; x = −80° ; x = 40° ; x = 160°"], 2,  # −120° kept, outside the interval
        ["Which equation did you solve in 6.1, and how is it related to f(x) = g(x)?", "Which values of k put x inside the interval from −90° "
                                                                                       "to 180°?"], marks=3, after=["6.1", "6.2.3"]),
]
for i in q6:   # the built sketch: its features' and shapes' marks are the memo criteria's, criterion by criterion
    if (i.get("build") or {}).get("kind") == "sketch":
        got = {}
        for x in i["build"]["features"] + [g["shape"] for g in i["build"]["graphs"]]:
            got[x["crit"]] = got.get(x["crit"], 0) + x["marks"]
        assert got == {k: c["marks"] for k, c in enumerate(i["criteria"])}, (i["n"], got)
        assert {f["graph"] for f in i["build"]["features"]} == {g["id"] for g in i["build"]["graphs"]}, i["n"]

# ---- QUESTION 7, the question paper page 8 and the memo pages 12-13 ----
C7 = "\ncos θ = {3x² + 9}/{12x}\ncos θ = {3(x² + 3)}/{12x}\ncos θ = {x² + 3}/{4x}"
COS = "cos θ = {(2,4)² + 3}/{4(2,4)}\ncos θ = 0,9125\nθ = "
L73 = "For x > 0: cos θ > 0, so 0° < θ < 90°\n0 < {x² + 3}/{4x} < 1\nx² + 3 < 4x\nx² − 4x + 3 < 0\n"
q7 = [
    work("7.1", "Show that cos θ = (x² + 3)/(4x)", 3, [
        "x² = (2x)² + (3)² − 2(2x)(3)cos θ\n12x cos θ = 3x² + 9" + C7,                       # the memo
        "x² = (2x)² + (3)² + 2(2x)(3)cos θ\n12x cos θ = 3x² + 9" + C7,                       # the rule's sign, then dropped to reach the result
        "x² = (2x)² + (3)² − 2(2x)(3)cos θ\n6x cos θ = 3x² + 9\ncos θ = {3x² + 9}/{6x}\ncos θ = {3(x² + 3)}/{6x}\ncos θ = {x² + 3}/{4x}",   # 2(2x)(3) as 6x, then 3/6 as 1/4
        "cos θ = {x² + 3}/{4x}\n4x cos θ = x² + 3\n12x cos θ = 3x² + 9\nx² = 4x² + 9 − 12x cos θ\nx² = (2x)² + (3)² − 2(2x)(3)cos θ"], 0,  # starts from the answer
        ["Which side of △PQR is opposite θ?", "Which rule links three sides and one angle of a triangle?"]),
    work("7.2.1", "If x = 2,4 units: Calculate θ", 3, [
        "cos θ = {2(2,4) + 3}/{4(2,4)}\ncos θ = 0,8125\nθ = 35,66°",   # x² taken as 2x
        COS + "65,85°",                                                 # sin⁻¹ for cos⁻¹
        COS + "0,42°",                                                  # the calculator in radians
        COS + "24,15°"], 3,                                             # the memo
        ["What do you get when you put x = 2,4 into the formula from 7.1?", "Which calculator key undoes cos, and is it in degree mode?"]),
    work("7.2.2", "If x = 2,4 units: Calculate the area of △PQR", 2, [
        "Area of △PQR = {1}/{2} × PR × QR × sin Q̂\n= {1}/{2} × 2,4 × 3 × sin 24,15°\n= 1,47 units²",    # PR is not an arm of the angle at Q
        "Area of △PQR = {1}/{2} × PQ × QR × sin Q̂\n= {1}/{2} × 4,8 × 3 × sin 24,15°\n= 2,95 units²",    # the memo
        "Area of △PQR = PQ × QR × sin Q̂\n= 4,8 × 3 × sin 24,15°\n= 5,89 units²",                         # the ½ left out
        "Area of △PQR = {1}/{2} × PQ × QR × cos Q̂\n= {1}/{2} × 4,8 × 3 × cos 24,15°\n= 6,57 units²"], 1,  # cos for sin
        ["Which two sides of △PQR meet at the angle θ, and how long is each when x = 2,4?", "Which area rule uses two sides and the angle "
                                                                                            "between them?"], after=["7.2.1"]),
    work("7.3", "Calculate the values of x for which the triangle exists.", 4, [
        L73 + "(x − 1)(x − 3) < 0\nx < 1 or x > 3",    # outside the roots
        L73 + "(x + 1)(x + 3) < 0\n−3 < x < −1",       # the factors' signs swapped
        L73 + "(x − 1)(x − 3) < 0\n1 < x < 3",         # the memo
        L73 + "(x − 1)(x − 3) < 0\n1 ≤ x ≤ 3"], 2,     # the end points kept: no triangle there
        ["For θ to be an angle of this triangle, between which two values must (x² + 3)/(4x) lie?", "How do you solve a quadratic inequality "
                                                                                                    "once it is factorised?"]),
]

# ---- QUESTION 8, the question paper page 9 and the memo page 14 ----
SA = "Total surface area = (16 × 16) + 4({1}/{2} × 16 × "
q8 = [
    work("8.1", "Show that the perpendicular height of the pyramid, AP, is 7,5 cm.", 2, [
        "V = Ah\n640 = (16 × 16) × h\nh = 7,5 cm",                          # a prism's volume: no 1/3 (640 ÷ 256 is 2,5)
        "h = 7,5 cm\nV = {1}/{3} × (16 × 16) × 7,5\nV = 640 cm³",           # starts from the answer
        "V = {1}/{3}Ah\n640 = {1}/{3} × 16 × h\nh = 7,5 cm",                # the side 16 for the base's area (that gives 120)
        "V = {1}/{3}Ah\n640 = {1}/{3} × (16 × 16) × h\nh = 7,5 cm"], 3,     # the memo
        ["What is the area A of the square base?", "What equation do you get when you put V = 640 and A into the formula?"]),
    work("8.2", "Hence, determine the total surface area of the pyramid.", 4, [
        "AT = √(7,5² + 8²) = 10,9658… [Pythagoras]\n" + SA + "10,9658…)\n= 606,91 cm²",             # the memo
        "AT = √(7,5² + 16²) = 17,6706… [Pythagoras]\n" + SA + "17,6706…)\n= 821,46 cm²",            # the whole side 16 for PT
        "AT = √(7,5² + 8²) = 10,9658… [Pythagoras]\nTotal surface area = 4({1}/{2} × 16 × 10,9658…)\n= 350,91 cm²",   # the base left out
        "AT = √(8² − 7,5²) = 2,7839… [Pythagoras]\n" + SA + "2,7839…)\n= 345,08 cm²"], 0,           # subtracts the squares
        ["Which right-angled triangle gives the slant height AT of a triangular face?", "Which faces make up the total surface area?"]),
]

# ---- QUESTION 9, the question paper page 10 and the memo pages 14-15 ----
CON = "Construction: draw radii OR and OS\nIn △OTR and △OTS:\nOR = OS [radii]\n"
OT = "OT = OT [common side]\nT̂₁ = T̂₂ = 90° [∠s on str line]\n"
FIN = "∴ RT = TS [≡ △s]"
RAD = "OD = OB = 8 − x [radii]\nOB² = OF² + FB² [Pythagoras]\n(8 − x)² = x² + 4²\n"
PERP = "AF = FB = 4 cm [line from centre ⊥ to chord]\n" + RAD
q91 = [
    work("9.1", "Prove the theorem which states that if OT ⊥ RTS then RT = TS.", 5, [
        CON + OT + "△OTR ≡ △OTS [SAS]\n" + FIN,                                                       # the wrong case: the 90° is not between OR and OT
        CON + OT + "△OTR ≡ △OTS [90° HS]\n" + FIN,                                                    # the memo
        CON + "OT = OT [common side]\nRT = TS [line from centre ⊥ to chord]\n△OTR ≡ △OTS [SSS]\n" + FIN,  # uses the theorem it proves
        CON + "OT = OR [radii]\nT̂₁ = T̂₂ = 90° [∠s on str line]\n△OTR ≡ △OTS [90° HS]\n" + FIN], 1,     # OT taken as a radius
        ["Which construction gives you two triangles that share the side OT?", "What do you know about the angles at T, and about OR and OS?"]),
]
q92 = [
    work("9.2", "Determine the length of the radius of the circle.", 5, [
        PERP + "64 − 16x + x² = x² + 16\n−16x = 80, so x = −5\nRadius = 8 − (−5) = 13 cm",                     # 64 moved across without its sign change
        "AF = FB = 4 cm [line from centre to midpt of chord]\n" + RAD + "64 − 16x + x² = x² + 16\n48 = 16x, so x = 3\n"
        "Radius = 8 − 3 = 5 cm",                                                                               # the converse: F is not given as a midpoint
        PERP + "64 − x² = x² + 16\n2x² = 48, so x = 4,90\nRadius = 8 − 4,90 = 3,10 cm",                         # (8 − x)² taken as 64 − x²
        PERP + "64 − 16x + x² = x² + 16\n48 = 16x, so x = 3\nRadius = 8 − 3 = 5 cm"], 3,                         # the memo, with the right radius (memo_issue)
        ["What does the line from the centre perpendicular to AB do to AB?", "Which two lengths are radii, and how can you write each of them "
                                                                             "in terms of x?"]),
]

# ---- QUESTION 10, the question paper page 11 and the memo page 16 ----
TAN = "Q̂₂ = R̂₂ [tans from common pt]\n"
SUM = TAN + "Q̂₂ + R̂₂ + 70° = 180° [sum of ∠s in △]\n"
M1 = "M̂₁ + R̂₁ + Q̂₁ = 180° [sum of ∠s in △]\n"
q10 = [
    work("10.1", "Calculate the size of R̂₂.", 4, [
        SUM + "2R̂₂ = 110°\nR̂₂ = 220°",                                  # doubled instead of halved
        TAN + "Q̂₂ + R̂₂ = 70° [ext ∠ of △]\n2R̂₂ = 70°\nR̂₂ = 35°",        # 70° taken as an exterior angle
        SUM + "2R̂₂ = 110°\nR̂₂ = 55°",                                   # the memo
        SUM + "R̂₂ = 180° − 70°\nR̂₂ = 110°"], 2,                         # the two equal angles taken as one
        ["What do you know about the two tangents drawn from P?", "What do the three angles of △PQR add up to?"]),
    work("10.2", "Calculate the size of Q̂₁.", 2, [
        "Q̂₁ + Q̂₂ = 90° [tan ⊥ radius]\nQ̂₁ = 35°",           # the memo (OR R̂₁ = 35° with MR = MQ)
        "Q̂₁ + Q̂₂ = 180° [∠s on a str line]\nQ̂₁ = 125°",      # no straight line at Q
        "Q̂₁ = Q̂₂ [tans from common pt]\nQ̂₁ = 55°",          # the wrong pair of angles
        "Q̂₁ + Q̂₂ = 90° [∠ in semi-circle]\nQ̂₁ = 35°"], 0,    # the wrong reason
        ["MQ is a radius and QP a tangent: what angle do they make?", "Which part of that angle is Q̂₂?"], after=["10.1"]),
    work("10.3", "Determine the size of M̂₂.", 3, [
        M1 + "M̂₁ = 180° − 70° = 110°\nM̂₂ = 55° [∠ at centre = 2 × ∠ at circumference]",   # halved, with a theorem that does not apply
        M1 + "M̂₁ = 180° − 70° = 110°\nM̂₂ = 110° [equal chords; equal ∠s at centre]",      # the memo
        M1 + "M̂₁ = 180° − 35° = 145°\nM̂₂ = 145° [equal chords; equal ∠s at centre]",      # only one of the two base angles taken off
        M1 + "M̂₁ = 180° − 70° = 110°\nM̂₂ = 110° [vert opp ∠s]"], 1,                       # the wrong reason: M̂₁ and M̂₂ are not vertically opposite
        ["In △MQR, which two angles are equal because MQ = MR, and what is each?", "Which chord does M̂₂ stand on, and how is it related to "
                                                                                   "QR?"], after=["10.2"]),
]

# ---- QUESTION 11, the question paper page 12 and the memo pages 17-18 ----
BIS = "B̂₁ = B̂₂ = x [BD bisects AB̂C]\nAB̂C = 2x\n"
CEN = "[∠ at centre = 2 × ∠ at circumference]"
q11 = [
    work("11.1", "Prove that BC ∥ OD", 4, [
        BIS + "Ô₁ = 2x [∠s opp equal sides]\n∴ BC ∥ OD [corresp ∠s equal]",       # the wrong reason for Ô₁
        BIS + "Ô₁ = 2x " + CEN + "\n∴ BC ∥ OD [alt ∠s equal]",                    # Ô₁ and AB̂C are corresponding, not alternate
        BIS + "Ô₁ = AB̂C = 2x [corresp ∠s; BC ∥ OD]\n∴ BC ∥ OD [corresp ∠s equal]",  # assumes what it proves
        BIS + "Ô₁ = 2x " + CEN + "\n∴ BC ∥ OD [corresp ∠s equal]"], 3,            # the memo (OR alternate angles through D̂₁; OR co-interior angles)
        ["Ô₁ and AB̂D stand on the same arc AD: how are they related?", "Which pair of angles on BC and OD, cut by the line BA, can you show "
                                                                         "are equal?"]),
    work("11.2", "Show that Ĉ = 90°", 3, [
        "OD̂C = 90° [tan chord theorem]\nĈ = 90° [co-int ∠s; OD ∥ BC]",     # the wrong reason for the 90° at D
        "OD̂C = 90° [tan ⊥ radius]\nĈ = 90° [∠ in semi-circle]",            # C is not on the circle
        "OD̂C = 90° [tan ⊥ radius]\nĈ = 90° [co-int ∠s; OD ∥ BC]",          # the memo (OR through D̂₂ = 90° − x; OR corresponding angles at D)
        "OD̂C = 90° [tan ⊥ radius]\nĈ = 90° [alt ∠s; OD ∥ BC]"], 2,         # OD̂C and Ĉ are co-interior, not alternate
        ["What angle does the radius OD make with the tangent CDE?", "OD ∥ BC: how are OD̂C and BĈD related?"]),
]

# ---- QUESTION 12, the question paper page 13 and the memo page 19 ----
FOUR = "P̂₁ = x [tan chord theorem]\nĈ₂ = x [alt ∠s; AD ∥ BC]\nÊ = x [∠s in the same seg]\n"
DCB = "DĈB = Ĉ₁ + Ĉ₂ = y + x\n"
P2 = "P̂₂ = y [tans from common pt]\n"
DPT = "DP̂T = P̂₁ + P̂₂ + P̂₃ = x + y + (x + y) = 2x + 2y\nĈ = x + y\n"
q12 = [
    mcq("12.1", "Name, with reasons, FOUR other angles equal to x." + ANSWER, [
        "P̂₁ = x [tan chord theorem]\nĈ₂ = x [corresp ∠s; AD ∥ BC]\nÊ = x [∠s in the same seg]\nP̂₅ = x [vert opp ∠s]",   # alternate called corresponding
        "P̂₁ = x [∠s in the same seg]\nĈ₂ = x [alt ∠s; AD ∥ BC]\nÊ = x [∠s in the same seg]\nP̂₅ = x [vert opp ∠s]",       # P̂₁ is a tangent-chord angle
        FOUR + "P̂₄ = x [vert opp ∠s]",                                                                                 # P̂₄ is opposite P̂₈, not P̂₁
        FOUR + "P̂₅ = x [vert opp ∠s]"], 3,                                                                             # the memo
        ["Which angle between the tangent QPR and a chord stands on the same chord PD as DÂC?", "Which angle at C pairs with DÂC across the "
                                                                                                "parallel lines AD and BC?"],
        marks=7),
    work("12.2", "Show that EP̂A = x + y", 4, [
        DCB + "ED̂A = D̂₁ = x + y [corresp ∠s; AD ∥ BC]\n∴ EP̂A = x + y [∠s in the same seg]",   # the memo
        DCB + "ED̂A = D̂₁ = x + y [alt ∠s; AD ∥ BC]\n∴ EP̂A = x + y [∠s in the same seg]",       # D̂₁ and DĈB are corresponding, not alternate
        DCB + "ED̂A = D̂₁ = x + y [corresp ∠s; AD ∥ BC]\n∴ EP̂A = x + y [tan chord theorem]",     # EP̂A is not a tangent-chord angle
        DCB + "ED̂A = D̂₁ = x + y [corresp ∠s; AD ∥ BC]\n∴ EP̂A = x + y [vert opp ∠s]"], 0,      # EP̂A and ED̂A are not vertically opposite
        ["What is DĈB in terms of x and y?", "Which angle at D, and then which angle at P, can you show equal to DĈB?"], after=["12.1"]),
    work("12.3", "Determine the numerical value of x + y, if it is given that DCTP is a cyclic quadrilateral.", 4, [
        P2 + DPT + "DP̂T = Ĉ [opp ∠s of cyclic quad]\n2x + 2y = x + y\nx + y = 0°",                       # opposite angles taken as equal
        P2 + DPT + "DP̂T + Ĉ = 180° [opp ∠s of cyclic quad]\n3x + 3y = 180°\nx + y = 60°",                # the memo
        P2 + "DP̂T = P̂₁ + P̂₂ = x + y\nĈ = x + y\nDP̂T + Ĉ = 180° [opp ∠s of cyclic quad]\n2x + 2y = 180°\nx + y = 90°",   # P̂₃ left out
        P2 + DPT + "DP̂T + Ĉ = 180° [co-int ∠s; DP ∥ TC]\n3x + 3y = 180°\nx + y = 60°"], 1,                # a wrong reason: DP and TC are not parallel
        ["Which angles at P make up DP̂T, and what is each in terms of x and y?", "What do the opposite angles of a cyclic quadrilateral add "
                                                                                 "up to?"], after=["12.1", "12.2"]),
]

REASONS = "Give reasons for your statements and calculations in QUESTIONS 9, 10, 11 and 12."
# (no caption names a reading, a coordinate, a length, an angle size, a range or a type that a question asks for: captions show in the
# enlarged figure view and to screen readers)
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Box-and-whisker diagram", "marks": 4,
     "lead": "Mr Brown conducted a survey on the amount of airtime (in rands) EACH student had on his or her cellphone. He summarised the "
             "data in the box and whisker diagram below.",
     "figure": fig("Q1.1", "A box-and-whisker diagram drawn above a number line marked from 10 to 66 in steps of 2: a left whisker, the box "
                   "with a line inside it, and a long right whisker."), "items": q1a},
    {"id": "1.2", "title": "Question 1.2", "kind": "Mean and standard deviation", "marks": 6,
     "lead": "A group of 13 students indicated how long it took (in hours) before their cellphone batteries required recharging. The "
             "information is given in the table below.\n\n5   8   10   17   20   29   32   48   50   50   63   y   107", "items": q1b},
    {"id": "2", "title": "Question 2", "kind": "Cumulative frequency", "marks": 12,
     "lead": "A student conducted a survey among his friends and relatives to determine the relationship between the age of a person and the "
             "number of marketing phone calls he or she received within one month. The information is given in the table below.",
     "table": CALLS, "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Diagonals of a quadrilateral", "marks": 15,
     "lead": "A(−2 ; −5), B, C and D are the vertices of quadrilateral ABCD such that diagonal AC is perpendicular to diagonal BD at T.\n"
             "The equation of BTD is given by 2y + x = 18 and AB = 15 units.",
     "figure": fig("Q3", "Axes with origin O. Quadrilateral ABCD: B at the top left, C at the top right, D at the bottom right below the "
                   "x-axis, and A(−2 ; −5) at the bottom just left of the y-axis. The diagonals AC and BD cross at T, where a right angle is "
                   "marked. AB is marked 15."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Inclination and parallel lines", "marks": 12,
     "lead": "C, a point on the x-axis, A(−5 ; −3) and B(4 ; 12) are the vertices of a triangle.\nAB intersects the x-axis at E.\n"
             "AB̂C = θ and BÊC = α.",
     "figure": fig("Q4", "Axes with origin O. Triangle ABC: A(−5 ; −3) below the x-axis on the left, B(4 ; 12) at the top and C on the "
                   "x-axis far to the right. AB crosses the x-axis at E, where α is marked by an arc from the x-axis up to EB; θ is marked at "
                   "B, inside the triangle."), "items": q4},
    {"id": "5.1", "title": "Question 5.1", "kind": "Reduction formulae", "marks": 6, "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Special angles", "marks": 6, "items": q52},
    {"id": "5.3", "title": "Question 5.3", "kind": "Ratios on the Cartesian plane", "marks": 10,
     "lead": "In the diagram below, R is a point in the first quadrant such that TÔR = α.\nRO is extended to P such that OP = 2 RO and "
             "TÔP = β.\nIt is given that sin α = 3/5.\n\nWITHOUT using a calculator, determine:",
     "figure": fig("Q5.3", "Axes with origin O. R is a point in the first quadrant; the line from R through O is extended to P in the third "
                   "quadrant. T lies on the positive x-axis. α is marked at O, turning from OT up to OR; β is marked by a larger arc turning "
                   "anticlockwise from OT round to OP."), "items": q53},
    {"id": "5.4", "title": "Question 5.4", "kind": "Trigonometric identities", "marks": 4, "items": q54},
    {"id": "6", "title": "Question 6", "kind": "Equations and graphs", "marks": 16,
     "lead": "Consider the functions f(x) = sin(x − 30°) and g(x) = cos 2x", "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Cosine rule and area", "marks": 12,
     "lead": "In △PQR, QR = 3 units, PR = x units, PQ = 2x units and PQ̂R = θ.",
     "figure": fig("Q7", "Triangle PQR: P on the left, Q at the top right and R at the bottom. PQ is marked 2x, QR is marked 3 and PR is "
                   "marked x; θ is marked at Q."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Pyramid", "marks": 6,
     "lead": "A pyramid with a square base with a side length of 16 cm is sketched below. P lies on the square base directly below A.\nThe "
             "volume of the pyramid is 640 cm³.\n\nVolume of pyramid = (1/3)Ah",
     "figure": fig("Q8", "A pyramid on a square base; the front edge of the base is marked 16 cm. The perpendicular height h is drawn dashed "
                   "from the apex A down to P on the base, with a right angle at P. A dashed line runs from P to T on the right-hand edge of "
                   "the base, and another from A down to T."), "items": q8},
    {"id": "9.1", "title": "Question 9.1", "kind": "Proving a chord theorem", "marks": 5,
     "lead": REASONS + " In the diagram below, O is the centre of the circle and point T lies on chord RS.",
     "figure": fig("Q9.1", "A circle with centre O. The chord RS runs across the lower part of the circle, R on the left and S on the right. "
                   "A line from O runs straight down through T on RS to the circle. At T, angle 1 lies between TO and TR, and angle 2, marked "
                   "as a right angle, between TO and TS."), "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Chord and radius", "marks": 5,
     "lead": REASONS + " In the diagram, O is the centre of circle ABD. F is a point on chord AB such that DOF ⊥ AB. AB = FD = 8 cm and "
                       "OF = x cm.",
     "figure": fig("Q9.2", "A circle with centre O. The chord AB runs across the top, A on the left and B on the right, with F on it; a right "
                   "angle is marked at F. The line from F runs down through O to D at the bottom of the circle; FO is marked x. OB is "
                   "drawn."), "items": q92},
    {"id": "10", "title": "Question 10", "kind": "Tangents and a centre", "marks": 9,
     "lead": REASONS + " M is the centre of the circle SVQR having equal chords SV and QR.\nRP and QP are tangents to the circle at R and Q "
                       "respectively such that RP̂Q = 70°.",
     "figure": fig("Q10", "A circle with centre M. S (left), V (top), Q (upper right) and R (bottom) lie on the circle. The tangents at R and "
                   "Q meet at P to the right, where RP̂Q is marked 70°; the tangent at Q is drawn on past Q. Chords SV and QR carry the same "
                   "double tick mark. MS, MV, MQ and MR are drawn. Angles are numbered: M̂₁ between MQ and MR, M̂₂ between MS and MV; Q̂₁ "
                   "between QM and QR, Q̂₂ between QR and QP; R̂₁ between RM and RQ, R̂₂ between RQ and RP."), "items": q10},
    {"id": "11", "title": "Question 11", "kind": "Tangent and diameter", "marks": 7,
     "lead": REASONS + " In the diagram below, O is the centre of the circle. CDE is a tangent to the circle at D.\nDB bisects AB̂C. Let "
                       "B̂₁ = x",
     "figure": fig("Q11", "A circle with centre O. BA is a diameter, drawn straight down from B at the top to A at the bottom. D lies on the "
                   "circle at the lower right; OD and BD are drawn. C lies outside the circle to the right: BC is drawn, and CDE is the "
                   "tangent at D, running on down to E. Angles are numbered: B̂₁ between BA and BD, B̂₂ between BD and BC; Ô₁ between OA and "
                   "OD, Ô₂ between OD and OB; D̂₁ between DO and DB, D̂₂ between DB and DC."), "items": q11},
    {"id": "12", "title": "Question 12", "kind": "Touching circles", "marks": 15,
     "lead": REASONS + " In the diagram below, two circles touch each other externally at point P.\nQPR is a common tangent to both circles at "
                       "P. EDRC is a tangent to circle PBFC at C.\nRĈA = y and DÂC = x. AD ∥ BC.",
     "figure": fig("Q12", "Two circles touch at P: the larger on the left through A (top), E (bottom left), D (bottom) and P; the smaller on "
                   "the right through B, F, C and P. QPR is the common tangent at P, drawn straight up to Q and down to R. EDRC is a straight "
                   "line along the bottom, touching the smaller circle at C. AP runs on to C, EP to F (crossing BC at T) and DP to B. AB, AD "
                   "and BC are drawn; AD and BC carry arrows. x is marked at A between AD and AC, and y at C between CR and CA. Angles are "
                   "numbered: Â₁ and Â₂ at A; B̂₁ between BA and BP, B̂₂ between BP and BC; round P, P̂₁ between PD and PR, P̂₂ between PR "
                   "and PC, P̂₃ between PC and PT, P̂₄ between PT and PB, P̂₅ between PB and PQ, P̂₆ between PQ and PA, P̂₇ between PA and PE "
                   "and P̂₈ between PE and PD; D̂₁ between DE and DA, D̂₂ between DA and DP, D̂₃ between DP and DR; Ĉ₁ between CR and CA, "
                   "Ĉ₂ between CA and CB."), "items": q12},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.1.2", "1.2.1", "1.2.3", "2.5", "3.1", "3.2", "3.3", "3.4.1", "3.4.2", "3.4.3", "4.1", "4.2", "4.3", "4.4",
                           "5.1", "5.2", "5.3.1", "5.3.2", "5.3.3", "5.4", "6.1", "7.1", "7.2.1", "7.2.2", "7.3", "8.1", "8.2", "9.1", "9.2",
                           "10.1", "10.2", "10.3", "11.1", "11.2", "12.2", "12.3"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["1.1.1", "1.1.3", "2.1", "2.3", "6.2.2", "6.2.4", "12.1"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric", "term", "match", "pickn")], "a typed calculation, written answer, term, sort or pick left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["1.2.2", "2.2", "6.2.1"]   # the one-number answers
assert all(i["a"] >= 0 for i in ITEMS if i["t"] == "num"), "a signed answer belongs in a multiple choice (the keypad's sign)"
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.4", "6.2.3"]
assert [i["n"] for i in ITEMS if i["t"] == "draw" and i.get("build")] == ["6.2.3"]
for _m in missions:   # a gate names an EARLIER part of its own mission (the app looks a gate up inside the mission)
    _order = [i["n"] for i in _m["items"]]
    for _i in _m["items"]:
        assert all(e in _order[:_order.index(_i["n"])] for e in _i.get("after", [])), (_i["n"], "a gate outside its mission or later")
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
GATES = {i["n"]: i["after"] for i in ITEMS if i.get("after")}

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2017", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines and every proof plays as four workings, the memo's FIRST method line by line (a "
                                                       "geometry statement with its [reason]) and three built from real errors (a wrong formula, "
                                                       "ratio, identity, theorem or congruency case, a sign slip, a misread value, the wrong side "
                                                       "or quadrant, a wrong reason, circular reasoning, one value tried, the calculator in "
                                                       "radians or used where the stem forbids it), 0 or full marks: " + ", ".join(AUTHORED)
                                                       + " (%d parts, %d marks). In a proof or 'show that' every option ends in the given result "
                                                       "(a 'starts from the answer' option in a true statement). The memo's OR methods and values "
                                                       "(2.5 a reading of 56 to 59 calls, 4.1 A − B on top and below, 4.2 the gradients of EB and "
                                                       "EA set equal to 5/3, 5.4 −1 + sin² θ = −cos² θ, 6.1 cos(120° − x) = cos 2x with x = 240° + "
                                                       "360°.k, 10.2 R̂₁ = 35° with MR = MQ, 11.1 alternate angles through D̂₁ and co-interior "
                                                       "angles, 11.2 through D̂₂ = 90° − x and corresponding angles) are other right routes and "
                                                       "never a wrong option. The memo's 4.1 (one line) and 3.4.3 are set as two lines; its 5.2 "
                                                       "and 5.4 nested fractions are written with ÷ and with tan θ.cos² θ = sin θ.cos θ worked "
                                                       "first (one level of {a}/{b}); 3.4.3 keeps the memo's second reason form (converse ∠ in "
                                                       "semi-circle; its first is 'subt. right ∠')." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.1.1", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                   "with no working (the five-number summary, the skewness, the completed table, the modal class, "
                                                   "a range, the points of intersection, four angles with reasons): the memo's answer and common "
                                                   "errors, 0 or full marks (1.1.3: the Grade 12 model's three choices). 1.1.1 loses the memo's "
                                                   "split min + max / quartiles marks; 2.1 its four 1-mark pairs; 6.2.2 its values / notation (its "
                                                   "OR y ∈ [−1 ; 1] is the right option's interval and no wrong option); 6.2.4 its mark per value; "
                                                   "12.1 its statement and reason marks (7). The Question 2 table, with the answer book's blanks, "
                                                   "is the mission's table."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 12), hand-transcribed from the page images of a SCANNED "
                                                           "question paper, memo and answer book; no API call."},
        {"n": "1.2.2", "kind": "no_fit", "detail": "One-number answers with no working stay typed on the keypad: 1.2.2 (σ = 30,94: keyed at two "
                                                   "decimal places, tolerance 0,006, so the sample standard deviation 32,21 is marked wrong), 2.2 "
                                                   "(80 people) and 6.2.1 (180°)."},
        {"n": "2.4", "kind": "no_fit", "detail": "The ogive (2.4) is drawn on paper and self-checked against the memo's three criteria (its 'upper "
                                                 "limits' written out as the seven points); the answer book's blank grid is described in the "
                                                 "memo text, not cropped."},
        {"n": "6.2.3", "kind": "no_fit", "detail": "The graphs of f and g (6.2.3) are BUILT on a grid (2026-10-11): x from −90° to 180° in steps "
                                                   "of 15° (the 45° and 135° intercepts need them), y from −2 to 2 in steps of 0,5, as the answer "
                                                   "book's grid. The memo's five criteria are the features: f's x-intercept (30° ; 0); 'shape of "
                                                   "f' = f's curve drawn with its two turning points (−60° ; −1) and (120° ; 1), 0 marks each, "
                                                   "which fix the curve; g's x-intercepts (45° ; 0) and (135° ; 0) together; 'shape of g' = g's "
                                                   "curve drawn with its third x-intercept (−45° ; 0) and its turning point (0 ; 1), 0 marks "
                                                   "each, so the chips of one name are every such point of g in the interval; g's turning point "
                                                   "(90° ; −1). The end points and f's y-intercept, which the stem asks for but the memo does not "
                                                   "mark, are not features (each graph is drawn over the domain)."},
        {"n": "1.1.2", "kind": "no_fit", "detail": "A part whose stem, options or criteria show an earlier part's answer opens only once that part "
                                                   "is answered ('after'): " + "; ".join(k + " after " + " and ".join(v) for k, v in GATES.items())
                                                   + ". Question 6's mission lead is its 6.2 sentence (printed after 6.1 in the paper) so that "
                                                   "6.2.4, whose options show 6.1's solutions and 6.2.3's intercepts, can open after both (a gate "
                                                   "is looked up inside its mission)."},
        {"n": "9.2", "kind": "memo_issue", "detail": "The memo (page 15) finds x = 3 and then writes 'length of radius = 8 − x = 8 − 5 = 3 units'; "
                                                     "the radius is 8 − 3 = 5 cm. The right option ends in 5 cm, and no wrong option ends in the "
                                                     "memo's 3."},
        {"n": "7.3", "kind": "memo_issue", "detail": "The memo (page 13) writes x² + 3x < 4x where x² + 3 < 4x is meant (its next line x² − 4x + 3 "
                                                     "< 0 is right); the right option has x² + 3 < 4x."},
        {"n": "10.3", "kind": "memo_issue", "detail": "The memo (page 16) names the centre O (Ô₁, Ô₂, and 10.2's OR 'OR = OQ'); the paper's centre "
                                                      "is M, and the options use M̂₁, M̂₂."},
        {"n": "6.2.3", "kind": "memo_issue", "detail": "The memo's graph (page 12) labels f's left end point (−90° ; −0,7); f(−90°) = sin(−120°) = "
                                                       "−0,87. The end points are not features of the built sketch; the draw memo text gives "
                                                       "−0,87."},
        {"n": "4.4", "kind": "memo_issue", "detail": "The memo's mark column (page 8) reads 'subst (−3 ; −5)' for A(−5 ; −3); its working "
                                                     "substitutes A correctly."},
    ],
}
QTOTAL = {"1": 10, "2": 12, "3": 15, "4": 12, "5": 26, "6": 16, "7": 12, "8": 6, "9": 10, "10": 9, "11": 7, "12": 15}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
assert per_q == QTOTAL, per_q
# the right letter (no printed multiple choice in this paper, so every letter is ours): the 36 authored workings as even as 36 allows
# (9 each: the brief's 3-7 band is for fewer workings), the four-option MCQs within 1 of even (1.1.3 has the model's three choices)
worked = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(worked.values()) - min(worked.values()) <= 1 and min(worked.values()) >= 3, worked
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert [i["n"] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) != 4] == ["1.1.3"] and max(fspread.values()) - min(fspread.values()) <= 1, fspread
print("right options, authored workings:", worked, "four-option:", fspread)
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts; gated:", len(GATES))
print("total:", total)
# every gate, in full: a gate dropped by a helper or an edit fails the run before anything is written
assert GATES == {
    "1.1.2": ["1.1.1"],                     # Q₃ = 38 and Q₁ = 17
    "1.2.2": ["1.2.1"], "1.2.3": ["1.2.1"],   # y = 94 in the stem; 41 × 13 = 533 = 439 + y
    "2.4": ["2.1"],                         # its criteria: the cumulative frequencies
    "2.5": ["2.1"],                         # a wrong option reads 52 at 50
    "3.2": ["3.1"],                         # m(AC) = 2
    "3.3": ["3.2"],                         # the stem's y = 2x − 1
    "3.4.1": ["3.3"], "3.4.2": ["3.3"],     # T(4 ; 7)
    "3.4.3": ["3.4.2"],                     # a wrong option's BT = 3√5
    "4.2": ["4.1"], "4.3": ["4.1"],         # m(AB) = 5/3
    "4.4": ["4.3"],                         # α = 59°
    "5.3.2": ["5.3.1"],                     # a wrong option's cos α = 4/5
    "5.3.3": ["5.3.1", "5.3.2"],            # P(−8 ; −6) is 2 × R(4 ; 3) reversed; sin β = −3/5
    "6.2.4": ["6.1", "6.2.3"],              # 40° + 120°.k; a wrong option's intercepts 30°, 45°, 135°
    "7.2.2": ["7.2.1"],                     # θ = 24,15°
    "10.2": ["10.1"],                       # Q̂₂ = R̂₂ = 55°
    "10.3": ["10.2"],                       # R̂₁ + Q̂₁ = 70°
    "12.2": ["12.1"],                       # Ĉ₂ = x
    "12.3": ["12.1", "12.2"]}, GATES        # P̂₁ = x, Ĉ₂ = x and P̂₃ = EP̂A = x + y
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's, memo's and answer book's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 12 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
