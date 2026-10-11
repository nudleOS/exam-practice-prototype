"""Mathematics P2 Nov 2025, the whole paper (Questions 1 to 11: statistics, analytical geometry, trigonometry, Euclidean geometry),
hand-transcribed into the catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any
ingested paper. Stems, options, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and
figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not). The question paper and the
answer book are SCANS (no text layer) and the memo's text layer garbles fractions and diagrams: everything was read from the page
IMAGES (diagrams zoomed in).

  python tools/ingest/transcribe_math_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P2 Nov 2025 Eng.pdf" "<...>/Mathematics P2 Nov 2025 MG Afr & Eng.pdf" --id math-p2-2025-11 --from-json

How the memo's shapes map (Mathematics: there is no algebra input, a learner answers with the keypad, a choice or a drawing
self-checked on paper):
  every calculation ("Calculate / Determine", "Calculate, with reasons", "Write down" with a working), "Show that", expression in
  k, reduction, identity and geometry proof -> authored multiple choice, `work` (Murci, 2026-10-10): the memo's FIRST working one
  step a line (a Euclidean geometry statement with its [reason] at the line's end, a fraction {numerator}/{denominator}), and
  three workings each built from a DIFFERENT real error (a wrong formula, identity or theorem, a sign slip, a misread value, the
  wrong side or angle, a wrong reason, circular reasoning, the calculator's other mode), each ending in a confident result; the
  same layout in all four (`shape`: line count and trailing reasons), 0 or full marks. The memo's OR methods are other right
  routes and never a wrong option; 4.7's working is ours (the memo gives the coordinates only);
  one 1-mark read-off with no working (2.1.1, 1.4, 4.1, 4.4, 7.1) -> num;
  a choice of plausible forms (the skewness, cos 40° in k, an interval whose open/closed ends matter, an equation of a graph, a
  range) -> mcq;
  "Draw a histogram" -> draw with the memo's criteria (self-checked, flagged no_fit); "draw the graph of g" (7.2) -> draw with
  build "sketch" (2026-10-11: its asymptotes and intercepts placed on a grid, the curve drawn through them, marked online against
  the memo's criteria).
A part whose working shows an EARLIER part's answer (3.3's tan θ = ½ is 3.2's gradient) opens only once that part is answered:
GATES, written to the part's "after".
A mission is a question with its stem and diagram; a question whose stem changes part-way is two missions (2, 5, 9, 11). An MCQ
of plausible forms in a figure mission carries the figure itself (the MCQ stage shows an item's own figure only); a working MCQ
plays on the page, under the mission's figure.
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the 1.5x page images and checked on a contact sheet with the
ingest's 1% padding (Q3 and Q4 are trimmed so the question text above and below stays out)."""
import json
import re
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad agent_math_p2/figs.py + figs.json; [page, x0, y0, x1, y1] in points
    "Q3": [5, 66.7, 155.0, 536.7, 458.0], "Q4": [6, 120.0, 178.5, 501.3, 478.0], "Q7": [8, 63.3, 148.0, 540.0, 466.7],
    "Q8": [9, 96.7, 266.7, 510.0, 462.0], "Q9.1": [10, 216.7, 170.0, 400.0, 354.7], "Q9.2": [11, 128.0, 128.0, 412.0, 345.3],
    "Q10": [12, 186.7, 174.7, 441.3, 408.0], "Q11.1": [13, 103.3, 197.3, 470.0, 372.0], "Q11.2": [14, 96.7, 145.3, 445.3, 382.0]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}

WORK = "\n\nChoose the correct working."
AUTHORED = []   # the workings played as authored multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues):
    """A working as authored multiple choice (Murci, 2026-10-10): opts are the memo's FIRST working and three workings built from
    common errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks)


# ---- QUESTION 1, the question paper page 3 and the memo page 3 ----
q1 = [
    work("1.1", "Determine the equation of the least squares regression line.", 3, [
        "a = −22 988,32\nb = 331 397,20\nŷ = −22 988,32 + 331 397,20x",                         # the calculator's ax + b mode read as a + bx
        "a = 331 397,20\nb = −22 988,32\nŷ = 331 397,20 − 22 988,32x",                          # the memo
        "a = 13,46\nb = −0,00004\nŷ = 13,46 − 0,00004x",                                         # the prices entered as x, the ages as y
        "b = {148 000 − 293 000}/{8 − 2} = −24 166,67\na = 293 000 + 24 166,67(2) = 341 333,33\nŷ = 341 333,33 − 24 166,67x"], 1,
        # ^ the line through the first and last cars, not the least squares line
        ["Put the ages in as x and the prices as y in your calculator's linear regression (STAT, A + BX) mode.", "The price falls as the car ages: which sign must b have?"]),
    work("1.2", "Predict the selling price of a similar car at this car dealership that is 5 years old.", 2, [
        "ŷ = 331 397,20 + 22 988,32(5)\n= 446 338,80",                                           # b's sign dropped
        "ŷ = (331 397,20 − 22 988,32)(5)\n= 1 542 044,40",                                        # a multiplied by 5 too
        "ŷ = 331 397,20 − 22 988,32 ÷ 5\n= 326 799,54",                                          # divides by the age
        "ŷ = 331 397,20 − 22 988,32(5)\n= 216 455,60"], 3,                                       # the memo (calculator: 216 455,61)
        ["Substitute the age into your equation from 1.1.", "x is the age in years."]),
    work("1.3", "Use the correlation coefficient to show whether the prediction made in QUESTION 1.2 is valid or not.", 2, [
        "r = −0,95\nA strong correlation: the points lie close to the line\nThe prediction is valid",           # the memo
        "r = −0,95\nA weak correlation, because r is negative\nThe prediction is not valid",                  # the sign read as the strength
        "r = −0,95\nA strong correlation, but no car in the table is 5 years old\nThe prediction is not valid",  # 5 lies inside 2-8
        "r = −0,95\nA perfect correlation: every point lies on the line\nThe prediction is valid"], 0,        # strong, not perfect
        ["Find r on your calculator, with the same data as in 1.1.", "How close is r to −1 or 1, and what does that say about the points and the line?"]),
    num("1.4", "Use the answer to QUESTION 1.1 to write down the estimated average yearly decrease in the selling price of these 11 cars.",
        22988.32, 0.011, "R", ["Which number in ŷ = a + bx tells you the change in price for each extra year?", "A decrease: give its size."]),
]

# ---- QUESTION 2, the question paper page 4 and the memo pages 4-5 ----
q21 = [
    num("2.1.1", "How many people visited this website on that day?", 70, 0, "people",
        ["A cumulative frequency keeps adding up.", "Which row's count includes every visitor?"]),
    work("2.1.2", "How many people spent more than 40 and up to 80 minutes on the website?", 2, [
        "Number of people = 67 − 16\n= 51",                                                      # takes away t ≤ 20, not t ≤ 40
        "Number of people = 59 − 40\n= 19",                                                      # stops at 60 minutes
        "Number of people = 67 − 40\n= 27",                                                      # the memo
        "Number of people = 70 − 40\n= 30"], 2,                                                  # runs on to 100 minutes
        ["The cumulative frequency up to 80 minutes counts everyone with t ≤ 80.", "Take away everyone with t ≤ 40."]),
    draw("2.1.3", "Draw a histogram to represent the information provided in the cumulative frequency table.", 3, [
        ["Two frequencies correct (the bars: 0–20: 16; 20–40: 24; 40–60: 19; 60–80: 8; 80–100: 3)", 1],
        ["All frequencies correct", 1], ["No gaps between the bars", 1]],
        ["First turn the cumulative frequencies into the frequency of each class: subtract the one before.", "A histogram's bars touch."],
        memo="The answer book gives the grid: number of people (0 to 70, steps of 5) up, time t in minutes (0 to 100, classes of 20) across."),
    mcq("2.1.4", "Comment on the skewness of the data.", ["Symmetrical", "Skewed to the right (positively skewed)",
                                                         "Skewed to the left (negatively skewed)"], 1,
        ["Work out each class's frequency: where is the peak, and which way does the tail run?", "The tail points towards the skew."]),
]
MEAN9 = "{11 + 14 + 19 + 20 + 8 + 10 + 2 + 14 + x}/{9} = 12\nx + 98 = 108, so x = 10\n"
q22 = [
    work("2.2", "How many players' points score was outside ONE standard deviation of the mean points score?", 5, [
        MEAN9 + "σ = 5,23\n(x̄ − σ ; x̄ + σ) = (6,77 ; 17,23)\n6 players were outside one standard deviation",      # counts the ones INSIDE
        MEAN9 + "σ = 5,55\n(x̄ − σ ; x̄ + σ) = (6,45 ; 17,55)\n3 players were outside one standard deviation",      # the sample sd (sx), not σ
        MEAN9 + "σ = 27,33\n(x̄ − σ ; x̄ + σ) = (−15,33 ; 39,33)\n0 players were outside one standard deviation",   # the variance as σ
        MEAN9 + "σ = 5,23\n(x̄ − σ ; x̄ + σ) = (6,77 ; 17,23)\n3 players were outside one standard deviation"], 3,  # the memo
        ["The mean of all nine scores is 12: find the missing ninth score first.", "Use the population standard deviation (σ, σx on the calculator), then count the scores outside (x̄ − σ ; x̄ + σ)."]),
]

# ---- QUESTION 3, the question paper page 5 and the memo pages 6-8 ----
PT = "PT = √((4 − (−1))² + (−2 − 8)²)\n= √125 = 5√5 units\n"
q3 = [
    work("3.1", "Calculate the length of QR. Leave your answer in simplified surd form.", 2, [
        "QR = √((−4 − 12)² + (−6 − 2)²)\n= √320\n= 8√5 units",                                  # the memo
        "QR = √((−4 + 12)² + (−6 + 2)²)\n= √80\n= 4√5 units",                                   # a sign slip: adds R's coordinates
        "QR = √((−4 − (−6))² + (12 − 2)²)\n= √104\n= 2√26 units",                               # pairs each point's x with its own y
        "QR = √((−4 − 12)² + (−6 − 2)²)\n= √320\n= 64√5 units"], 0,                             # 64 taken out without its root
        ["Use the distance formula with Q and R.", "Take out the biggest perfect square that divides into the number under the root."]),
    work("3.2", "Calculate the gradient of QR.", 2, [
        "m(QR) = {−4 − 12}/{−6 − 2}\n= 2",                                                      # x over y
        "m(QR) = {−6 − 2}/{−4 − 12}\n= {1}/{2}",                                                # the memo
        "m(QR) = {−6 − 2}/{−4 + 12}\n= −1",                                                     # a sign slip in the bottom
        "m(QR) = {−6 − 2}/{12 − (−4)}\n= −{1}/{2}"], 1,                                         # Q − R on top, R − Q below
        ["m = (y₂ − y₁)/(x₂ − x₁) with Q and R.", "Take the two points in the same order on top and below."]),
    work("3.3", "Calculate the size of θ.", 2, [
        "sin θ = m(QR) = {1}/{2}\nθ = 30°",                                                     # sine for tangent
        "tan θ = {16}/{8} = 2\nθ = 63,43°",                                                     # run over rise
        "tan θ = m(QR) = {1}/{2}\nθ = 0,46°",                                                   # the calculator in radians
        "tan θ = m(QR) = {1}/{2}\nθ = 26,57°"], 3,                                              # the memo
        ["The gradient of a line is the tangent of its angle of inclination.", "tan θ = m, then use tan⁻¹."]),
    work("3.4", "Determine the equation of QR.", 2, [
        "−4 = {1}/{2}(−6) + c\nc = −1\ny = {1}/{2}x − 1",                                       # Q's x and y swapped
        "8 = {1}/{2}(−1) + c\nc = 8,5\ny = {1}/{2}x + 8,5",                                     # P, a point not on QR
        "−6 = {1}/{2}(−4) + c\nc = −4\ny = {1}/{2}x − 4",                                       # the memo (OR with R: y − 2 = ½(x − 12))
        "−6 = {1}/{2}(−4) + c\nc = −8\ny = {1}/{2}x − 8"], 2,                                   # −6 − (−2) taken as −8
        ["You have the gradient from 3.2.", "Substitute Q or R into y = mx + c to find c."]),
    work("3.5", "PQRS, in that order, is a parallelogram. Write down the coordinates of S.", 2, [
        "Q → R: (x ; y) → (x + 16 ; y + 8)\nP → S: (−1 + 16 ; 8 + 8)\nS(15 ; 16)",              # the memo
        "Q → R: (x ; y) → (x − 16 ; y − 8)\nP → S: (−1 − 16 ; 8 − 8)\nS(−17 ; 0)",              # the step taken backwards (R to Q)
        "P → R: (x ; y) → (x + 13 ; y − 6)\nQ → S: (−4 + 13 ; −6 − 6)\nS(9 ; −12)",             # the vertices in the order PQSR
        "Q → R: (x ; y) → (x + 8 ; y + 16)\nP → S: (−1 + 8 ; 8 + 16)\nS(7 ; 24)"], 0,           # across and up swapped
        ["In parallelogram PQRS, PS runs parallel and equal to QR.", "Move P by the same step that takes Q to R."]),
    work("3.6", "T is a point on QR such that PT ⊥ QR. Calculate the coordinates of T.", 5, [
        "m(PT) = 2\n8 = 2(−1) + c, so y = 2x + 10\n2x + 10 = {1}/{2}x − 4\n4x + 20 = x − 8, so x = −9,33\n"
        "y = {1}/{2}(−9,33) − 4 = −8,67: T(−9,33 ; −8,67)",                                    # the reciprocal without the sign change
        "m(PT) = −2\n8 = −2(−1) + c, so y = −2x + 6\n−2x + 6 = {1}/{2}x − 4\n−4x + 12 = x − 8, so x = 4\n"
        "y = {1}/{2}(4) − 4 = −2: T(4 ; −2)",                                                   # the memo (OR: △PQR isosceles, T the midpoint)
        "m(PT) = −2\n8 = −2(−1) + c, so y = −2x + 10\n−2x + 10 = {1}/{2}x − 4\n−4x + 20 = x − 8, so x = 5,6\n"
        "y = {1}/{2}(5,6) − 4 = −1,2: T(5,6 ; −1,2)",                                           # −2(−1) taken as −2: c = 10
        "m(PT) = −2\n8 = −2(−1) + c, so y = −2x + 6\n−2x + 6 = {1}/{2}x − 4\n−4x + 12 = x − 4, so x = 3,2\n"
        "y = {1}/{2}(3,2) − 4 = −2,4: T(3,2 ; −2,4)"], 1,                                       # the × 2 missed on the −4
        ["Perpendicular lines: the product of their gradients is −1.", "T lies on both PT and QR: solve the two equations together."]),
    work("3.7", "Calculate the area of parallelogram PQRS.", 3, [
        PT + "Area of PQRS = {1}/{2}QR.PT = {1}/{2}(8√5)(5√5)\n= 100 units²",                   # the triangle's formula
        "PQ = √((−4 − (−1))² + (−6 − 8)²)\n= √205 units\nArea of PQRS = QR.PQ = (8√5)(√205)\n= 256,12 units²",  # the slant side as height
        PT + "Area of PQRS = QR.PT = (8√5)(5√5)\n= 40√5 units²",                                # √5 × √5 left as √5
        PT + "Area of PQRS = QR.PT = (8√5)(5√5)\n= 200 units²"], 3,                             # the memo (OR 2 × area of △PQR)
        ["Take QR as the base: PT is then the perpendicular height.", "Area of a parallelogram = base × perpendicular height."]),
]

# ---- QUESTION 4, the question paper page 6 and the memo pages 9-12 ----
MB = "m(MB) = {4 − 0}/{−6 − (−3)} = −{4}/{3}\n"
BETA = "tan α = m(BC) = {3}/{4}, α = 36,87°\n"
q4 = [
    num("4.1", "Write down the value of p.", -6, 0, "",
        ["MC is parallel to the y-axis and passes through E.", "Every point on a vertical line has the same x-coordinate."]),
    work("4.2", "Show that q = 4.", 4, [
        "AM = ME = q [radii]\nAD = q − 1, MD = q + 1\nq² = (q − 1)² + (q + 1)² [Pythagoras]\nq = 4",
        "AM = ME = q + 1 [radii]\nAD = q − 1, MD = q\n(q + 1)² = (q − 1)² − q² [Pythagoras]\nq² + 4q = 0, so q = 4",
        "AM = ME = q + 1 [radii]\nAD = q − 1, MD = q\n(q + 1)² = (q − 1)² + q² [Pythagoras]\nq² − 4q = 0, so q = 4 (q ≠ 0)",   # the memo
        "AM = ME = q + 1 [radii]\nAD = q − 1, MD = q\nq + 1 = (q − 1) + q [Pythagoras]\nq = 4"], 2,
        ["Write the radius, AD and MD in terms of q.", "△AMD has a right angle at D: use Pythagoras."]),
    work("4.3", "Determine the equation of the circle in the form (x − a)² + (y − b)² = r².", 2, [
        "AM = q + 1 = 5 units\n(x + 6)² + (y − 4)² = 25",                                       # the memo
        "AM = q + 1 = 5 units\n(x − 6)² + (y + 4)² = 25",                                       # the centre's signs kept
        "AM = q + 1 = 5 units\n(x + 6)² + (y − 4)² = 5",                                        # r, not r²
        "AM = MD = q = 4 units\n(x + 6)² + (y − 4)² = 16"], 0,                                  # MD (to the x-axis) as the radius
        ["The centre is M(p ; q): you have p (4.1) and q (4.2).", "The radius is ME = q + 1."]),
    num("4.4", "If the circle is translated 2 units to the left, determine the minimum distance between the circle and the y-axis.", 3, 0, "units",
        ["After the translation, how far is the centre from the y-axis?", "Then take away the radius."]),
    work("4.5", "Calculate the coordinates of A and B.", 3, [
        "(x + 6)² + (0 − 4)² = 25\n(x + 6)² = 41\nx + 6 = −6,40 or x + 6 = 6,40\nA(−12,40 ; 0) and B(0,40 ; 0)",   # adds the 16
        "(x + 6)² + (0 − 4)² = 25\n(x + 6)² = 9\nx + 6 = 3 or x + 6 = −3\nA(−3 ; 0) and B(−9 ; 0)",              # A and B swapped
        "(x + 6)² + (0 − 4)² = 25\n(x + 6)² = 9\nx + 6 = −3 or x + 6 = 3\nA(−9 ; 0) and B(−3 ; 0)",              # the memo (OR factors; DB = AD = 3)
        "(x + 6)² + (0 − 4)² = 25\n(x + 6)² = 9\nx + 6 = −9 or x + 6 = 9\nA(−15 ; 0) and B(3 ; 0)"], 2,          # 9 never square-rooted
        ["A and B lie on the x-axis: their y-coordinate is 0.", "Put y = 0 into the circle's equation and solve for x."]),
    work("4.6", "Determine the equation of tangent BC.", 4, [
        MB + "m(BC) = −{4}/{3} [tangent ⊥ radius]\n0 = −{4}/{3}(−3) + c\ny = −{4}/{3}x − 4",     # the radius's gradient kept
        MB + "m(BC) = {3}/{4} [tangent ⊥ radius]\n0 = {3}/{4}(−3) + c\ny = {3}/{4}x + {9}/{4}",  # the memo
        MB + "m(BC) = −{3}/{4} [tangent ⊥ radius]\n0 = −{3}/{4}(−3) + c\ny = −{3}/{4}x − {9}/{4}",  # the reciprocal, sign unchanged
        "m(MB) = {4 − 0}/{−6 − 3} = −{4}/{9}\nm(BC) = {9}/{4} [tangent ⊥ radius]\n0 = {9}/{4}(−3) + c\ny = {9}/{4}x + {27}/{4}"], 1,
        # ^ −6 − (−3) taken as −6 − 3
        ["A tangent is perpendicular to the radius at the point of contact.", "Then put B into y = mx + c."]),
    work("4.7", "Write down the coordinates of C.", 2, [   # the memo gives C(−6 ; −9/4) only: the working is ours
        "C lies on the line MC: x = −6\ny = {3}/{4}(6) + {9}/{4} = {27}/{4}\nC(−6 ; {27}/{4})",   # 6 put in for −6
        "C lies on the line MC: x = −6\n(−6 + 6)² + (y − 4)² = 25, y = −1\nC(−6 ; −1)",          # the circle's equation: that is E
        "C lies on the line MC: x = −6\nDC = AD = 3, so y = −3\nC(−6 ; −3)",                    # DC taken equal to AD
        "C lies on the line MC: x = −6\ny = {3}/{4}(−6) + {9}/{4} = −{9}/{4}\nC(−6 ; −{9}/{4})"], 3,   # the memo's answer
        ["C is on the vertical line through M.", "C is also on tangent BC: use your equation from 4.6."]),
    work("4.8", "Calculate the size of AĈB.", 4, [
        BETA + "m(AC) = −{3}/{4}, tan β = −{3}/{4}\nβ = 180° − 36,87° = 143,13°\nAĈB = β − α = 106,26°",   # the memo
        BETA + "m(AC) = −{3}/{4}, tan β = −{3}/{4}\nβ = −36,87°\nAĈB = α − β = 73,74°",                    # the 180° never added
        BETA + "m(AC) = −{4}/{3}, tan β = −{4}/{3}\nβ = 180° − 53,13° = 126,87°\nAĈB = β − α = 90°",       # AC taken ⊥ BC
        "tan α = {9}/{4}, α = 66,04°\nm(AC) = −{9}/{4}, tan β = −{9}/{4}\nβ = 180° − 66,04° = 113,96°\nAĈB = β − α = 47,92°"], 0,
        # ^ the y-intercept 9/4 read as BC's gradient
        ["The gradients of BC and AC give their angles of inclination.", "An exterior angle of a triangle equals the two interior opposite angles."]),
]

# ---- QUESTION 5, the question paper page 7 and the memo pages 13-14 ----
K = "√(k² + 1)"
EXP = "{2sin 25°.cos 25°}/{−2 + 4sin² 25°} = "
SIN10 = "sin 10° = sin(50° − 40°)\n"
q51 = [
    mcq("5.1.1", "It is given that tan 50° = k. Express cos 40° in terms of k.",
        ["1/" + K, K + "/k", "k/" + K, "k/√(1 − k²)"], 2,
        ["Draw a right-angled triangle with a 50° angle: tan 50° = k/1.", "Find the hypotenuse with Pythagoras; cos 40° = sin 50°."], marks=2),
    work("5.1.2", "(2 sin 25°.cos 25°)/(−2 + 4 sin² 25°)", 5, [
        EXP + "{sin 50°}/{2(2sin² 25° − 1)}\n= {sin 50°}/{2cos 50°}\n= {k}/{" + K + "} ÷ {2}/{" + K + "}\n= {1}/{2}k",       # cos 2θ as 2sin²θ − 1
        EXP + "{sin 50°}/{−2(1 − 2sin² 25°)}\n= {sin 50°}/{−2cos 50°}\n= {k}/{" + K + "} ÷ {−2}/{" + K + "}\n= −{1}/{2}k",  # the memo
        EXP + "{sin 50°}/{−2(1 − 2sin² 25°)}\n= {sin 50°}/{−2sin 50°}\n= {k}/{" + K + "} ÷ {−2k}/{" + K + "}\n= −{1}/{2}",  # 1 − 2sin²θ as sin 2θ
        EXP + "{sin 50°}/{−2(1 − 2sin² 25°)}\n= {sin 50°}/{−2cos 50°}\n= {1}/{" + K + "} ÷ {−2k}/{" + K + "}\n= −{1}/{2k}"], 1,  # sin and cos 50° swapped
        ["Both the numerator and the bracket in the denominator are double angles.", "sin 50° over cos 50° is a single ratio you know in terms of k."]),
    work("5.1.3", "sin 10°", 4, [
        SIN10 + "= sin 50° cos 40° + cos 50° sin 40°\n= {k}/{" + K + "} · {k}/{" + K + "} + {1}/{" + K + "} · {1}/{" + K + "}\n= 1",  # cos's sign rule
        SIN10 + "= sin 50° cos 40° − cos 50° sin 40°\n= {k}/{" + K + "} · {1}/{" + K + "} − {1}/{" + K + "} · {k}/{" + K + "}\n= 0",  # 40°'s ratios swapped
        SIN10 + "= sin 50° − sin 40°\n= {k}/{" + K + "} − {1}/{" + K + "}\n= {k − 1}/{" + K + "}",                                 # sin shared out over the −
        SIN10 + "= sin 50° cos 40° − cos 50° sin 40°\n= {k}/{" + K + "} · {k}/{" + K + "} − {1}/{" + K + "} · {1}/{" + K + "}\n"
        "= {k² − 1}/{k² + 1}"], 3,                                                                                                   # the memo
        ["Write 10° as a difference of two angles whose ratios you know in terms of k.", "Use your triangle from 5.1.1 for sin 50°, cos 50°, sin 40° and cos 40°."]),
]
q52 = [
    work("5.2.1", "Simplify the expression above fully to a single trigonometric ratio.", 4, [
        "sin(540° + x) = sin(180° + x) = −sin x\ncos(90° + x) = −sin x\nsin(−x) = −sin x\n= {(−sin x)(−sin x)}/{−sin x} = −sin x",  # the memo
        "sin(540° + x) = sin(360° + x) = sin x\ncos(90° + x) = −sin x\nsin(−x) = −sin x\n= {(sin x)(−sin x)}/{−sin x} = sin x",     # 540° − 180°, not − 360°
        "sin(540° + x) = sin(180° + x) = −sin x\ncos(90° + x) = −cos x\nsin(−x) = −sin x\n= {(−sin x)(−cos x)}/{−sin x} = −cos x",  # no co-function at 90°
        "sin(540° + x) = sin 540° + sin x = sin x\ncos(90° + x) = −sin x\nsin(−x) = −sin x\n= {(sin x)(−sin x)}/{−sin x} = sin x"], 0,  # sin shared out
        ["540° = 360° + 180°: reduce each angle to x.", "Watch the sign of each ratio in its quadrant."]),
    mcq("5.2.2", "Hence, determine the values of x in the interval x ∈ [0° ; 360°] for which √(sin(540° + x).cos(90° + x)/sin(−x)) will be real.",
        ["0° < x < 180°", "180° ≤ x ≤ 360°", "0° ≤ x ≤ 180°", "180° < x < 360°"], 3,
        ["A square root is real when the expression under it is not negative: use your answer to 5.2.1.", "sin(−x) sits in a denominator: it may not be 0."], marks=2),
]

# ---- QUESTION 6, the question paper page 7 and the memo pages 15-16 ----
LHS = "LHS = (−tan x)(sin² x) + cos² x\n= (−{sin x}/{cos x})(sin² x) + cos² x\n= {sin³ x − cos³ x}/{−cos x}\n"
AS3 = "cos² x − sin² x = {1}/{2}sin 2x − cos² x\ncos² x − sin² x = sin x cos x − cos² x\n2cos² x − sin x cos x − sin² x = 0\n"
q6 = [
    work("6.1", "Prove that: [tan(180° − x)](1 − cos² x) + cos² x = (sin x − cos x)(1 + sin x.cos x)/(−cos x)", 6, [
        "LHS = (−tan x)(sin² x) + cos² x\n= (−{cos x}/{sin x})(sin² x) + cos² x\n= −sin x.cos x + cos² x\n= cos x(cos x − sin x)\n"
        "= {(sin x − cos x)(1 + sin x.cos x)}/{−cos x} = RHS",                                  # tan x as cos x/sin x, then a jump
        LHS + "= {(sin x − cos x)(sin² x + cos² x)}/{−cos x}\n= {sin x − cos x}/{−cos x} = RHS",  # the cubes' middle term lost
        LHS + "= {(sin x − cos x)(sin² x + sin x.cos x + cos² x)}/{−cos x}\n= {(sin x − cos x)(1 + sin x.cos x)}/{−cos x} = RHS",  # the memo
        "LHS = (tan 180° − tan x)(sin² x) + cos² x\n= (−{sin x}/{cos x})(sin² x) + cos² x\n= {sin³ x − cos³ x}/{−cos x}\n"
        "= {(sin x − cos x)(sin² x + sin x.cos x + cos² x)}/{−cos x}\n= {(sin x − cos x)(1 + sin x.cos x)}/{−cos x} = RHS"], 2,
        # ^ tan(180° − x) shared out as tan 180° − tan x
        ["Reduce tan(180° − x), then write everything in sin x and cos x.", "The numerator becomes a difference of two cubes."]),
    work("6.2", "It is given that sin² x ; cos² x and ½ sin 2x are the first three terms of an arithmetic sequence. The constant difference of the "
         "arithmetic sequence is NOT zero. Determine the general solution for x.", 7, [
        "cos² x − sin² x = {1}/{2}sin 2x − sin² x\ncos² x = sin x cos x\ncos² x − sin x cos x = 0\ncos x(cos x − sin x) = 0\n"
        "cos x = 0 or tan x = 1 (tan x = 1 gives d = 0)\nx = 90° + k.180° ; k ∈ Z",               # T₁ taken away on the right, not T₂
        AS3 + "(2cos x + sin x)(cos x − sin x) = 0\ntan x = −2 or tan x = 1 (tan x = 1 gives d = 0)\nx = 116,57° + k.180° ; k ∈ Z",   # the memo
        AS3 + "(2cos x − sin x)(cos x + sin x) = 0\ntan x = 2 or tan x = −1 (tan x = −1 gives d = 0)\nx = 63,43° + k.180° ; k ∈ Z",   # factor signs swapped
        AS3 + "(2cos x + sin x)(cos x − sin x) = 0\ntan x = −2 or tan x = 1 (tan x = 1 gives d = 0)\nx = 116,57° + k.360° ; k ∈ Z"], 1,  # tan's period as 360°
        ["Equal differences: T₂ − T₁ = T₃ − T₂.", "Factorise into two brackets; one of them gives a difference of zero."]),
]

# ---- QUESTION 7, the question paper page 8 and the memo page 17 ----
F7 = ("The graph of f(x) = cos 2x for x from −135° to 135°, on a grid with vertical lines at −135°, −90°, −45°, 45°, 90° and 135° and "
      "horizontal lines at y = 1 and y = −1: f starts at (−135° ; 0), falls to a minimum at (−90° ; −1), rises through (−45° ; 0) to a "
      "maximum at (0° ; 1), falls through (45° ; 0) to a minimum at (90° ; −1) and rises to (135° ; 0).")
q7 = [
    num("7.1", "Write down the period of f.", 180, 0, "°",
        ["The period is the length of one full wave.", "cos 2x repeats twice as fast as cos x."]),
    # built on the answer book's axes (2026-10-11, as transcribe_math_p1_2025_11.py 4.5): x from −135° to 135° on 22,5° steps (half the
    # answer book's 45° lines, so the x-intercepts are grid points), y from −2 to 2. Criterion 0 is the four asymptotes and criterion 2
    # the four intercepts, each matched as a set (three x-intercepts with one name), one feature of each carrying its mark; criterion 1
    # is the shape of the tan curve the learner's own features fix (increasing)
    {**draw("7.2", "On the set of axes provided in the ANSWER BOOK, draw the graph of g(x) = tan 2x − 1 for x ∈ [−135° ; 135°].", 3, [
        ["Asymptotes at x = −135°, −45°, 45° and 135°", 1],
        ["Shape: increasing tan branches, each between two asymptotes", 1],
        ["Intercepts with the axes: x-intercepts at −67,5°, 22,5° and 112,5°; y-intercept −1", 1]],
        ["tan 2x has period 90°: its asymptotes are where 2x = ±90°, ±270°.", "The − 1 shifts the whole graph one unit down."]),
     "build": {"kind": "sketch", "family": "tan", "b": 2, "x": [-135, 135, 22.5], "y": [-2, 2, 0.5], "domain": [-135, 135], "features": [
         {"id": "a1", "kind": "vline", "label": "asymptote", "at": -135, "tol": 0, "marks": 1, "crit": 0},
         {"id": "a2", "kind": "vline", "label": "asymptote", "at": -45, "tol": 0, "marks": 0, "crit": 0},
         {"id": "a3", "kind": "vline", "label": "asymptote", "at": 45, "tol": 0, "marks": 0, "crit": 0},
         {"id": "a4", "kind": "vline", "label": "asymptote", "at": 135, "tol": 0, "marks": 0, "crit": 0},
         {"id": "x1", "kind": "point", "label": "x-intercept", "at": [-67.5, 0], "tol": 0, "marks": 1, "crit": 2},
         {"id": "x2", "kind": "point", "label": "x-intercept", "at": [22.5, 0], "tol": 0, "marks": 0, "crit": 2},
         {"id": "x3", "kind": "point", "label": "x-intercept", "at": [112.5, 0], "tol": 0, "marks": 0, "crit": 2},
         {"id": "yint", "kind": "point", "label": "y-intercept", "at": [0, -1], "tol": 0, "marks": 0, "crit": 2}],
               "shape": {"label": "Shape", "answer": "increasing", "marks": 1, "crit": 1}}},
    mcq("7.3", "Graph f is translated 45° to the left to form graph h. Determine the equation of h in its simplest form.",
        ["h(x) = sin 2x", "h(x) = −sin 2x", "h(x) = cos(2x + 45°)", "h(x) = −cos 2x"], 1,
        ["Translating left by 45° replaces x with (x + 45°).", "cos 2(x + 45°) = cos(2x + 90°): reduce it."], figure=fig("Q7", F7)),
    mcq("7.4", "Graph f is translated 45° to the left to form graph h. Write down the range of h.",
        ["y ∈ [−1 ; 1]", "y ∈ [0 ; 1]", "y ∈ [−2 ; 2]", "y ∈ (−1 ; 1)"], 0,
        ["A horizontal shift moves a graph sideways only.", "Read the lowest and highest y-values of f."], figure=fig("Q7", F7)),
    mcq("7.5", "Determine the values of x for which (1 − tan 2x)(cos 2x) ≥ 0 in the interval x ∈ [0° ; 135°].",
        ["0° ≤ x ≤ 22,5° or 112,5° ≤ x ≤ 135°", "22,5° ≤ x < 45° or 45° < x ≤ 112,5°", "0° ≤ x ≤ 22,5° or 112,5° ≤ x < 135°", "0° ≤ x ≤ 22,5° only"], 2,
        ["(1 − tan 2x)(cos 2x) ≥ 0 is (tan 2x − 1)(cos 2x) ≤ 0: where are g and f on opposite sides of the x-axis?", "g is undefined at its asymptotes."],
        marks=4, figure=fig("Q7", F7)),
]
for i in q7:   # the built sketch: its features' and shape's marks are the memo criteria's, criterion by criterion
    if (i.get("build") or {}).get("kind") == "sketch":
        got = {}
        for x in i["build"]["features"] + [i["build"]["shape"]]:
            got[x["crit"]] = got.get(x["crit"], 0) + x["marks"]
        assert got == {k: c["marks"] for k, c in enumerate(i["criteria"])}, (i["n"], got)

# ---- QUESTION 8, the question paper page 9 and the memo page 18 ----
AK = "AK² = AB² + BK² = 18² + 18² [Pythagoras]\nAK = √648 = 18√2 = 25,46 cm\n"
q8 = [
    work("8.1", "Show that AB = 18 cm.", 2, [
        "BC = {1}/{2}AB\nArea of ABCD = BC × AB\n648 = {1}/{2}AB × AB\nAB² = 1 296, so AB = 18 cm",          # the ratio read upside down
        "BC = 2AB\nArea of ABCD = BC + AB\n648 = 2AB + AB\n3AB = 648, so AB = 18 cm",                          # adds the sides
        "BC = 2AB\nArea of ABCD = {1}/{2}BC × AB\n648 = {1}/{2}(2AB)(AB)\nAB² = 648, so AB = 18 cm",           # a triangle's area
        "BC = 2AB\nArea of ABCD = BC × AB\n648 = 2AB × AB\nAB² = 324, so AB = 18 cm"], 3,                      # the memo
        ["Write BC in terms of AB, from the ratio.", "Area of a rectangle = length × breadth."]),
    work("8.2", "Calculate the length of AC.", 2, [
        "AC² = AB² + BC² [Pythagoras]\n= 18² + 36²\nAC = √1 620 = 18√5 = 40,25 cm",            # the memo
        "AC² = AB² + BC² [Pythagoras]\n= 18² + 9²\nAC = √405 = 9√5 = 20,12 cm",                 # BC taken as half of AB
        "AC² = BC² − AB² [Pythagoras]\n= 36² − 18²\nAC = √972 = 18√3 = 31,18 cm",               # subtracts: AC is the hypotenuse
        "AC² = (AB + BC)² [Pythagoras]\n= (18 + 36)²\nAC = 54 cm"], 0,                          # squares the sum
        ["ABCD is a rectangle: △ABC has a right angle at B.", "BC is twice AB."]),
    work("8.3", "Calculate the length of diagonal KC.", 2, [
        "{KC}/{sin 52,6°} = {36}/{sin 104°}\nKC = {36 sin 52,6°}/{sin 104°}\nKC = 29,47 cm",     # the sides and angles mispaired
        "{KC}/{sin 104°} = {18}/{sin 52,6°}\nKC = {18 sin 104°}/{sin 52,6°}\nKC = 21,99 cm",     # AB (18) for BC
        "{KC}/{sin 104°} = {36}/{sin 52,6°}\nKC = {36 sin 104°}/{sin 52,6°}\nKC = 43,97 cm",     # the memo
        "{KC}/{sin 104°} = {36}/{sin 23,4°}\nKC = {36 sin 104°}/{sin 23,4°}\nKC = 87,95 cm"], 2,  # BC paired with the angle at C
        ["In △KBC you know two angles and the side BC.", "The sine rule: each side over the sine of its opposite angle."]),
    work("8.4", "If AB = BK, calculate the size of KÂC.", 4, [
        AK + "(43,97)² = (18√2)² + (18√5)² + 2(18√2)(18√5) cos KÂC\ncos KÂC = −0,16…\nKÂC = 99,40°",   # the rule's sign
        AK + "(43,97)² = (18√2)² + (18√5)² − 2(18√2)(18√5) cos KÂC\ncos KÂC = 0,16…\nKÂC = 80,60°",   # the memo
        AK + "(18√5)² = (18√2)² + (43,97)² − 2(18√2)(43,97) cos KÂC\ncos KÂC = 0,43…\nKÂC = 64,57°",  # AC opposite: that is AK̂C
        "AK² = AB² + BK² = 18² + 18² [Pythagoras]\nAK = 18 + 18 = 36 cm\n(43,97)² = 36² + (18√5)² − 2(36)(18√5) cos KÂC\n"
        "cos KÂC = 0,34…\nKÂC = 70,18°"], 1,                                                     # √(18² + 18²) taken as 18 + 18
        ["AB is vertical and BK horizontal: △ABK has a right angle at B.", "In △AKC you then know all three sides: use the cosine rule."]),
]

# ---- QUESTION 9, the question paper pages 10-11 and the memo pages 19-20 ----
KO = "Construction: draw KO produced\n"
q91 = [
    work("9.1", "Use the diagram above to prove the theorem which states that the angle subtended by a chord (or arc) at the centre of the circle is "
         "equal to twice the angle subtended by the same chord (or arc) at the circumference, that is prove that TÔP = 2 TK̂P.", 5, [
        KO + "K̂₁ = T̂ [∠s opp equal sides]\nÔ₁ = 2K̂₁ [∠ at centre = 2 × ∠ at circumference]\n"
        "likewise Ô₂ = 2K̂₂ [∠ at centre = 2 × ∠ at circumference]\n∴ TÔP = 2(K̂₁ + K̂₂) = 2 TK̂P",   # the theorem used to prove itself
        KO + "K̂₁ = T̂ [OK = OT]\nÔ₁ = 180° − 2K̂₁ [ext ∠ of △]\nlikewise Ô₂ = 180° − 2K̂₂ [ext ∠ of △]\n∴ TÔP = 2 TK̂P",   # KÔT's size for Ô₁
        KO + "K̂₁ = T̂ [∠s opp equal sides]\nÔ₁ = K̂₁ [vert opp ∠s]\nlikewise Ô₂ = K̂₂ [vert opp ∠s]\n∴ TÔP = K̂₁ + K̂₂ = 2 TK̂P",   # no vertical angles here
        KO + "K̂₁ = T̂ [∠s opp equal sides]\nÔ₁ = K̂₁ + T̂ = 2K̂₁ [ext ∠ of △]\nlikewise Ô₂ = 2K̂₂ [ext ∠ of △]\n"
        "∴ TÔP = 2(K̂₁ + K̂₂) = 2 TK̂P"], 3,                                                      # the memo
        ["Draw the line from K through O: it splits the figure into two isosceles triangles.", "OK, OT and OP are radii; use the exterior angle of each triangle."]),
]
q92 = [
    work("9.2.1", "Calculate, with reasons, the size of Ô₂.", 2, [
        "Ô₂ = 2P̂ [∠ at centre = 2 × ∠ at circumference]\nÔ₂ = 64°",                          # the memo (OR PL̂O = P̂ [∠s opp equal radii], ext ∠)
        "Ô₂ = 2P̂ [∠s in the same seg]\nÔ₂ = 64°",                                              # the wrong reason
        "Ô₂ = P̂ [∠s opp equal radii]\nÔ₂ = 32°",                                               # that is PL̂O, not Ô₂
        "Ô₂ = {1}/{2}P̂ [∠ at centre = 2 × ∠ at circumference]\nÔ₂ = 16°"], 0,                  # the theorem turned round
        ["Ô₂ and P̂ stand on the same arc LF.", "The angle at the centre and the angle at the circumference."]),
    work("9.2.2", "Calculate, with reasons, the size of M̂.", 3, [
        "PF̂M = 90° [tan ⊥ diameter]\nM̂ = 180° − 90° − 32° [sum of ∠s of △]\nM̂ = 58°",        # P̂ for Ô₂ in △MOF
        "PF̂M = 90° [∠ in semi-circle]\nM̂ = 180° − 90° − 64° [sum of ∠s of △]\nM̂ = 26°",       # the wrong reason: F is not on an arc
        "PF̂M = 90° [tan ⊥ diameter]\nM̂ = P̂ [tan chord theorem]\nM̂ = 32°",                    # M is not on the circle
        "PF̂M = 90° [tan ⊥ diameter]\nM̂ = 180° − 90° − 64° [sum of ∠s of △]\nM̂ = 26°"], 3,    # the memo
        ["MF is a tangent at the end of the diameter PF.", "Then use the angles of △MOF."]),
]

# ---- QUESTION 10, the question paper page 12 and the memo pages 21-22 ----
R55 = "R̂ = 180° − 90° − 35° = 55° [sum of ∠s in △]\n"
S55 = "Ŝ₁ = R̂ = 55° [given]\n"
q10 = [
    work("10.1", "Calculate, with reasons, the size of QT̂S.", 3, [
        R55 + "QT̂S = 180° − R̂ [opp ∠s of cyclic quad]\nQT̂S = 125°",                           # T and R are not opposite
        R55 + "QT̂S = R̂ [∠s in the same seg]\nQT̂S = 55°",                                      # the memo (OR Ŝ₂ = 35°, sum of ∠s in △)
        R55 + "QT̂S = Q̂₂ [∠s in the same seg]\nQT̂S = 35°",                                     # the wrong chord
        R55 + "QT̂S = 2R̂ [∠ at centre = 2 × ∠ at circumference]\nQT̂S = 110°"], 1,             # T is not the centre
        ["QT ⊥ SR, so △QVR has a right angle at V.", "QT̂S and R̂ stand on the same chord QS."]),
    work("10.2", "Prove that PQ ∥ SR.", 3, [
        "SP̂Q = 180° − Ŝ₁ = 125° [co-int ∠s; PQ ∥ SR]\n" + S55 + "SP̂Q + Ŝ₁ = 180°\n∴ PQ ∥ SR [co-int ∠s supp]",   # assumes what it proves
        "SP̂Q = R̂ = 55° [ext ∠ of cyclic quad]\n" + S55 + "SP̂Q = Ŝ₁\n∴ PQ ∥ SR [alt ∠s equal]",   # SP̂Q is not an exterior angle
        "SP̂Q = 180° − R̂ = 125° [opp ∠s of cyclic quad]\n" + S55 + "SP̂Q + Ŝ₁ = 180°\n∴ PQ ∥ SR [co-int ∠s supp]",   # the memo
        "SP̂Q = 180° − R̂ = 125° [opp ∠s of cyclic quad]\n" + S55 + "SP̂Q + Ŝ₁ = 180°\n∴ PS ∥ QR [co-int ∠s supp]"], 2,   # the wrong pair of lines
        ["PQRS is a cyclic quadrilateral: its opposite angles add up to 180°.", "Co-interior angles that add up to 180° make the lines parallel."]),
    work("10.3", "Prove that PT is a diameter of the circle.", 2, [
        "Q̂₁ = 90° [co-int ∠s; PQ ∥ SR]\n∴ PT is a diameter [converse ∠ in semi-circle]",        # the memo (OR PŜT = 90°)
        "Q̂₁ = 90° [co-int ∠s; PQ ∥ SR]\n∴ PT is a diameter [line from centre ⊥ to chord]",       # the wrong reason
        "Q̂₁ = 90° [∠ in semi-circle]\n∴ PT is a diameter [converse ∠ in semi-circle]",           # assumes what it proves
        "V̂₁ = 90° [given]\n∴ PT is a diameter [converse ∠ in semi-circle]"], 0,                 # V is not on the circle
        ["Find a 90° angle that stands on chord PT.", "A chord that subtends 90° at the circumference is a diameter."]),
]

# ---- QUESTION 11, the question paper pages 13-14 and the memo pages 23-26 ----
PROP = " [prop theorem; AD ∥ EF]\n"
AREA = "Area △ACD = {1}/{2}(5k)(5p) sin Ĉ\nArea GFDA = Area △ACD − Area △GCF\n"
q111 = [
    work("11.1.1", "Calculate, with reasons, the value of FD/CF.", 2, [
        "{FD}/{CF} = {CG}/{GA}" + PROP + "{FD}/{CF} = {3}/{2}",                                  # the ratio upside down
        "{FD}/{CF} = {GA}/{CG} [midpt theorem]\n{FD}/{CF} = {2}/{3}",                           # the wrong theorem: no midpoints
        "{FD}/{CF} = {CF}/{FB}" + PROP + "{FD}/{CF} = {2}/{5}",                                  # the given ratio of the other line
        "{FD}/{CF} = {GA}/{CG}" + PROP + "{FD}/{CF} = {2}/{3}"], 3,                              # the memo
        ["In △ADC, GF is parallel to AD.", "A line parallel to one side of a triangle divides the other two sides in the same proportion."]),
    work("11.1.2", "Calculate, with reasons, the value of BA/EA.", 4, [
        "CF = 2x, FB = 5x: FD = {2}/{3}(2x) = {4}/{3}x\n{BA}/{EA} = {BD}/{FD}" + PROP + "= {5x}/{4x/3}\n= {15}/{4}",                 # FB for BD
        "CF = 2x, FB = 5x: FD = {2}/{3}(2x) = {4}/{3}x\n{BA}/{EA} = {BD}/{FD}" + PROP + "= {5x − 4x/3}/{4x/3}\n= {11}/{4}",          # the memo
        "CF = 2x, FB = 5x: FD = {2}/{3}(2x) = {4}/{3}x\n{BA}/{EA} = {FD}/{BD}" + PROP + "= {4x/3}/{5x − 4x/3}\n= {4}/{11}",          # upside down
        "CF = 2x, FB = 5x: FD = {2}/{3}(5x) = {10}/{3}x\n{BA}/{EA} = {BD}/{FD}" + PROP + "= {5x − 10x/3}/{10x/3}\n= {1}/{2}"], 1,   # ⅔ of FB
        ["Give CF and FB lengths in one unit x from CF/FB = 2/5, then find FD with 11.1.1.", "In △BEF, AD is parallel to EF."]),
    work("11.1.3", "Calculate, with reasons, the value of Area of △GCF / Area of GFDA.", 4, [
        "Area △GCF = {1}/{2}(3k)(3p) sin Ĉ\nArea △ACD = {1}/{2}(5k)(5p) sin Ĉ\nArea GFDA = Area △ACD\n"
        "{Area △GCF}/{Area GFDA} = {9kp}/{25kp} = {9}/{25}",                                     # △GCF never taken away
        "Area △GCF = {1}/{2}(2k)(2p) sin Ĉ\n" + AREA + "{Area △GCF}/{Area GFDA} = {4kp}/{25kp − 4kp} = {4}/{21}",   # GA and FD for GC and FC
        "Area △GCF = {1}/{2}(3k)(3p) sin Ĉ\n" + AREA + "{Area △GCF}/{Area GFDA} = {9kp}/{25kp − 9kp} = {9}/{16}",   # the memo
        "Area △GCF : area △ACD = CG : CA = 3 : 5\nArea △ACD = 5 parts\nArea GFDA = Area △ACD − Area △GCF\n"
        "{Area △GCF}/{Area GFDA} = {3}/{5 − 3} = {3}/{2}"], 2,                                   # areas in the ratio of the sides
        ["Both triangles share the angle C: area = ½ × side × side × sin Ĉ.", "GFDA is △ACD with △GCF taken away."]),
]
QS = "{QS}/{QR} = {QZ}/{QS} [△QSZ ||| △QRS]\n"
q112 = [
    work("11.2.1", "PR = PW.QR/QE", 2, [
        "{QE}/{QR} = {PW}/{PR} [line ∥ one side of △]\nPR = {PW.QE}/{QR}",
        "{QE}/{QR} = {PW}/{PR} [prop theorem; PQ ∥ WE]\nPR = {PW.QR}/{QE}",                     # the memo
        "{QE}/{QR} = {PR}/{PW} [prop theorem; PQ ∥ WE]\nPR = {PW.QR}/{QE}",
        "{QE}/{QR} = {PW}/{PR} [corresp ∠s; PQ ∥ WE]\nPR = {PW.QR}/{QE}"], 1,
        ["In △PQR, WE is parallel to PQ.", "Write the proportion, then make PR the subject."]),
    work("11.2.2", "If △PQZ ||| △RQP, then PQ² = RQ.QZ", 1, [
        "{PQ}/{RQ} = {QZ}/{QP} [△PQZ ||| △RQP]\n∴ PQ² = RQ.QZ",                                  # the memo
        "{PQ}/{RQ} = {QP}/{QZ} [△PQZ ||| △RQP]\n∴ PQ² = RQ.QZ",                                  # QP and QZ do not match in that order
        "{PQ}/{RP} = {QZ}/{QP} [△PQZ ||| △RQP]\n∴ PQ² = RQ.QZ",                                  # PQ matched with RP, not RQ
        "{PQ}/{RQ} = {QZ}/{QP} [tan chord theorem]\n∴ PQ² = RQ.QZ"], 0,                          # PQ is not a tangent
        ["Similar triangles have sides in proportion: match the sides in the order of the letters.", "Then cross-multiply."]),
    work("11.2.3", "△QSZ ||| △QRS", 3, [
        "Q̂₂ = Q̂₂ [common ∠]\nŜ₁ = R̂₂ [∠s in the same seg]\nẐ₁ = QŜR [3rd ∠ of △]\n∴ △QSZ ||| △QRS [∠∠∠]",          # QS is a tangent, not a chord
        "Q̂₂ = Q̂₂ [common ∠]\nZŜR = R̂₂ [tan chord theorem]\nẐ₁ = QŜR [3rd ∠ of △]\n∴ △QSZ ||| △QRS [∠∠∠]",        # the angle inside, not at the tangent
        "Q̂₂ = Q̂₂ [common ∠]\nŜ₁ = R̂₂ [tan chord theorem]\nẐ₁ = QŜR [3rd ∠ of △]\n∴ △QSZ ||| △QRS [∠∠∠]",          # the memo
        "Q̂₂ = Q̂₂ [common ∠]\nŜ₁ = R̂₂ [tan chord theorem]\nQS = QS [common side]\n∴ △QSZ ||| △QRS [S∠S]"], 2,      # a congruence test
        ["The two triangles share an angle at Q.", "QS is a tangent: the angle between a tangent and a chord equals the angle in the alternate segment."]),
    work("11.2.4", "PQ = QS", 3, [
        QS + "QS² = QZ.QR\nbut PQ² = RQ.QZ [11.2.2]\n∴ PQ = QS",                                 # the memo
        "{QS}/{QR} = {QZ}/{QS} [tan chord theorem]\nQS² = QZ.QR\nbut PQ² = RQ.QZ [11.2.2]\n∴ PQ = QS",
        QS + "QS = QZ.QR\nbut PQ = RQ.QZ [11.2.2]\n∴ PQ = QS",
        "{QS}/{QR} = {SZ}/{QS} [△QSZ ||| △QRS]\nQS² = SZ.QR\nbut PQ² = RQ.QZ [11.2.2]\n∴ PQ = QS"], 0,
        ["Use the similar triangles of 11.2.3 to write QS² as a product.", "Compare it with PQ² from 11.2.2."]),
    work("11.2.5", "PW = QE.PZ/√(QR.QZ)", 4, [
        "PR = {PQ.PZ}/{QR} [△PQZ ||| △RQP]\nPR = {PW.QR}/{QE} [11.2.1]\nPW = {PQ.PZ.QE}/{QR²}\nPQ² = RQ.QZ [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}",
        "PR = {QR.PZ}/{PQ} [△PQZ ||| △RQP]\nPR = {PW.QR}/{QE} [11.2.1]\nPW = {QE.PZ}/{PQ}\nPQ = RQ.QZ [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}",
        "PR = {QR.PZ}/{PQ} [△PQZ ||| △RQP]\nPR = {PW.QR}/{QE} [11.2.1]\nPW = {QE.PZ}/{PQ}\nPQ = √(RQ.QZ) [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}",  # the memo
        "PR = {QR.PZ}/{PQ} [△PQZ ||| △RQP]\nPR = {PW.QE}/{QR} [11.2.1]\nPW = {QR².PZ}/{QE.PQ}\nPQ = √(RQ.QZ) [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}"], 2,
        ["Write PR in two ways: from 11.2.1 and from △PQZ ||| △RQP.", "Set them equal, then replace PQ using 11.2.2."]),
]

CARS = {"head": ["AGE OF CAR (IN YEARS)", "SELLING PRICE OF CAR (IN RAND)"],
        "rows": [["2", "293 000"], ["3", "265 000"], ["3", "256 000"], ["4", "219 000"], ["4", "241 000"], ["4", "246 000"], ["6", "226 000"],
                 ["6", "176 000"], ["7", "154 000"], ["7", "180 000"], ["8", "148 000"]]}
WEB = {"head": ["TIME, t (IN MINUTES)", "CUMULATIVE FREQUENCY"],
       "rows": [["0 < t ≤ 20", "16"], ["0 < t ≤ 40", "40"], ["0 < t ≤ 60", "59"], ["0 < t ≤ 80", "67"], ["0 < t ≤ 100", "70"]]}
POINTS = {"head": ["PLAYER", "POINTS SCORED"],
          "rows": [[str(i + 1), v] for i, v in enumerate(["11", "14", "19", "20", "8", "10", "2", "14"])]}
REASONS = "Provide reasons for your statements in QUESTIONS 9, 10 and 11."
missions = [
    {"id": "1", "title": "Question 1", "kind": "Regression and correlation", "marks": 8,
     "lead": "There were 11 cars of the same model for sale at a car dealership. The age (in years) of each car and its corresponding selling price "
             "(in rands) is provided in the table below.", "table": CARS, "items": q1},
    {"id": "2.1", "title": "Question 2.1", "kind": "Cumulative frequency", "marks": 7,
     "lead": "The cumulative frequency table below shows the amount of time that people spent on a particular website on a certain day.",
     "table": WEB, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Mean and standard deviation", "marks": 5,
     "lead": "There are 9 players in a basketball team. The coach calculated that on average, each player scored 12 points during a game. The points "
             "scored by 8 of the 9 players from the team is given below:", "table": POINTS, "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Lines and a triangle", "marks": 18,
     "lead": "In the diagram, P(−1 ; 8), Q(−4 ; −6) and R(12 ; 2) are the vertices of △PQR. The angle of inclination of QR is θ.",
     "figure": fig("Q3", "Axes with origin O. Triangle PQR: P(−1 ; 8) just left of the y-axis near the top, R(12 ; 2) to the right above the x-axis, "
                   "Q(−4 ; −6) at the bottom left. Side QR rises from Q, crosses the y-axis below O and the x-axis to the right of O; θ is marked "
                   "where QR crosses the x-axis, between the x-axis and QR."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "The circle and its tangents", "marks": 21,
     "lead": "In the diagram, M(p ; q) is the centre of the circle that intersects the x-axis at A and B. C is a point such that the line drawn from "
             "M to C is parallel to the y-axis and intersects the x-axis at D. MC intersects the circle at E(−6 ; −1). Tangents drawn from C touch "
             "the circle at A and B. AD = (q − 1) units.",
     "figure": fig("Q4", "Axes with origin O. A circle with centre M(p ; q) to the left of the y-axis and above the x-axis cuts the x-axis at A (left) "
                   "and B (right), both left of O. A vertical line from M goes down through D on the x-axis and E on the circle to C below the "
                   "circle. Radii MA and MB are drawn, and the tangents CA and CB."), "items": q4},
    {"id": "5.1", "title": "Question 5.1", "kind": "Ratios in terms of k", "marks": 11,
     "lead": "It is given that tan 50° = k. Express EACH of the following in terms of k:", "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Reduction formulae", "marks": 6,
     "lead": "Given: sin(540° + x).cos(90° + x)/sin(−x)", "items": q52},
    {"id": "6", "title": "Question 6", "kind": "Identities and general solutions", "marks": 13, "items": q6},   # no shared stem printed
    {"id": "7", "title": "Question 7", "kind": "Trigonometric graphs", "marks": 10,
     "lead": "In the diagram, the graph of f(x) = cos 2x is drawn for x ∈ [−135° ; 135°].", "figure": fig("Q7", F7), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Sine, cosine and area rules", "marks": 10,
     "lead": "As part of a school project, learners are required to design a portable stage for a puppet show, as shown in the diagram below. The "
             "design must fulfil the following requirements:\n• BKLC is a horizontal base having KB̂C = 104° and BK̂C = 52,6°.\n• The rectangular "
             "backdrop, ABCD, is vertical to the horizontal base and must have an area of 648 cm².\n• The sides of ABCD must be in the ratio AB : BC "
             "= 1 : 2.\n• The stage must be partly enclosed with triangular sides ABK and DCL.",
     "figure": fig("Q8", "A puppet stage. A shaded horizontal base BKLC: B at the back left, C at the back right, K at the front left and L at the "
                   "front right, with diagonal KC; KB̂C = 104° and BK̂C = 52,6°. A vertical rectangle ABCD (Area = 648 cm²) stands on BC, A above B "
                   "and D above C, with right angles at B and C. Triangular sides ABK on the left and DCL on the right."), "items": q8},
    {"id": "9.1", "title": "Question 9.1", "kind": "Circle geometry proof", "marks": 5,
     "lead": REASONS + " In the diagram, O is the centre of the circle. K, T and P lie on the circle.",
     "figure": fig("Q9.1", "A circle with centre O; K at the top, T at the bottom left and P at the bottom right. Chords KT and KP are drawn, and "
                   "radii OT and OP (TÔP opens downward)."), "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Angles, tangents and diameters", "marks": 5,
     "lead": REASONS + " In the diagram, O is the centre of the circle. POF is the diameter of the circle and MF is a tangent to the circle at F. "
             "OM cuts the circle at L. P̂ = 32°. Calculate, with reasons, the size of:",
     "figure": fig("Q9.2", "A circle with centre O and a vertical diameter POF, P at the top and F at the bottom. The tangent at F runs left to M; "
                   "the line OM cuts the circle at L, on the lower left. Chord PL is drawn; the angle at P between PL and PF is 32°. At O, angle 1 "
                   "lies between OP and OL, and angle 2 between OL and OF."), "items": q92},
    {"id": "10", "title": "Question 10", "kind": "Cyclic quadrilaterals", "marks": 8,
     "lead": REASONS + " In the diagram, PQRS is a cyclic quadrilateral. T is a point on the circle such that QT is perpendicular to SR at V. PT and "
             "ST are drawn. Q̂₂ = 35° and R̂ = Ŝ₁.",
     "figure": fig("Q10", "A circle through P (upper left), Q (top right), R (right), T (bottom right) and S (left). Quadrilateral PQRS; chord QT "
                   "crosses SR at V at right angles (angles V₁ to V₄, V₁ marked 90°); chords PT and ST are drawn. Q̂₁ lies between QP and QT, Q̂₂ "
                   "= 35° between QT and QR; P̂₁ between PS and PT, P̂₂ between PT and PQ; Ŝ₁ between SP and SR, Ŝ₂ between SR and ST; T̂₁ and "
                   "T̂₂ at T, either side of TP."), "items": q10},
    {"id": "11.1", "title": "Question 11.1", "kind": "Proportionality", "marks": 10,
     "lead": REASONS + " In the diagram, △ABC is drawn. BA is produced to E. F and D are points on BC such that AD ∥ EF. AC and EF intersect at G. "
             "CF/FB = 2/5 and CG/GA = 3/2. Calculate, with reasons, the value of:",
     "figure": fig("Q11.1", "Triangle ABC with B at the top right, C at the bottom and A on the upper left. BA is produced to E on the left. D and F "
                   "lie on BC, D nearer B. AD and EF are parallel (arrows); EF cuts AC at G."), "items": q111},
    {"id": "11.2", "title": "Question 11.2", "kind": "Similar triangles", "marks": 13,
     "lead": REASONS + " In the diagram, WVZR is a cyclic quadrilateral. RZ is produced to Q. A tangent is drawn from Q to touch the circle at S. WV "
             "is produced to E, a point on ZQ. RW produced meets ZV produced in P. PQ ∥ WE. RS and ZS are drawn. Prove, with reasons, that:",
     "figure": fig("Q11.2", "A circle through W (top), R (right), S (bottom), Z and V (left). P lies above and left of the circle: RW produced and ZV "
                   "produced meet at P. RZ produced meets Q at the bottom left; QS is a tangent at S. WV produced meets ZQ at E. PQ ∥ WE (arrows). "
                   "RS and ZS are drawn. Angles: P̂₁, P̂₂; Ŵ₁, Ŵ₂; V̂₁, V̂₂; R̂₁, R̂₂; Ẑ₁, Ẑ₂; Ŝ₁ (between SQ and SZ), Ŝ₂; Q̂₁ (between QP and QR), Q̂₂ "
                   "(between QR and QS)."), "items": q112},
]

# A part whose working (its options) shows an EARLIER part's answer opens only once that part is answered (the catalogue's "after")
GATES = {"1.2": ["1.1"],                     # a and b
         "3.3": ["3.2"], "3.4": ["3.2"],     # m(QR) = ½
         "3.6": ["3.2", "3.4"],              # m(QR) and the equation of QR
         "3.7": ["3.1", "3.6"],              # QR = 8√5 and T
         "4.3": ["4.1"],                     # the centre's x, p = −6
         "4.5": ["4.3"], "4.6": ["4.5"],     # the circle's equation; B(−3 ; 0)
         "4.7": ["4.6"], "4.8": ["4.6"],     # tangent BC
         "5.1.2": ["5.1.1"], "5.1.3": ["5.1.1"],   # sin 50° = cos 40° = k/√(k² + 1)
         "8.4": ["8.2", "8.3"],              # AC = 18√5 and KC = 43,97
         "9.2.2": ["9.2.1"],                 # Ô₂ = 64°
         "10.2": ["10.1"],                   # R̂ = 55° (= QT̂S)
         "11.1.2": ["11.1.1"], "11.1.3": ["11.1.1"]}   # FD = ⅔ CF
ITEMS = [i for m in missions for i in m["items"]]
for _m in missions:
    _order = [i["n"] for i in _m["items"]]
    for _i in _m["items"]:
        if _i["n"] in GATES:
            assert all(e in _order[:_order.index(_i["n"])] for e in GATES[_i["n"]]), (_i["n"], "a gate names an earlier part of its mission")
            _i["after"] = GATES[_i["n"]]
assert sorted(GATES) == sorted(i["n"] for i in ITEMS if i.get("after"))

# every part that played as typed steps or a rubric before 2026-10-10, and the five authored proofs, now workings to choose from
assert tuple(AUTHORED) == ("1.1", "1.2", "1.3", "2.1.2", "2.2", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "4.2", "4.3", "4.5", "4.6", "4.7",
                           "4.8", "5.1.2", "5.1.3", "5.2.1", "6.1", "6.2", "8.1", "8.2", "8.3", "8.4", "9.1", "9.2.1", "9.2.2", "10.1", "10.2",
                           "10.3", "11.1.1", "11.1.2", "11.1.3", "11.2.1", "11.2.2", "11.2.3", "11.2.4", "11.2.5"), AUTHORED
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or written answer is left"
assert sorted(i["n"] for i in ITEMS if i["t"] == "num") == ["1.4", "2.1.1", "4.1", "4.4", "7.1"]   # the 1-mark read-offs
assert all(i["marks"] == 1 for i in ITEMS if i["t"] == "num")
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation, 'Show that', expression in "
                                                       "k, reduction, identity and proof plays as four workings, 0 or full marks: "
                                                       + ", ".join(AUTHORED) + " (%d parts, %d marks). The right option is the memo's FIRST "
                                                         "working line by line (a geometry statement with its [reason]); each wrong one carries "
                                                         "a different real error (a wrong formula, identity or theorem, a sign slip, a misread "
                                                         "value, the wrong side or angle, a wrong reason, circular reasoning, the calculator's "
                                                         "other mode). The memo's OR methods and values (1.2 the calculator's 216 455,61, 3.4 "
                                                         "with R, 3.6 the isosceles triangle, 3.7 twice △PQR, 4.5 the factors and DB = AD, 4.6 "
                                                         "y − y₁ = m(x − x₁), 4.8 the kite, the tan ratio and the cosine rule, 5.1.2 the quotient "
                                                         "identity, 5.1.3 cos 80° and sin(60° − 50°), 6.1 from the RHS, 6.2 the other grouping, "
                                                         "9.1 the angles round O, 9.2.1 PL̂O = P̂, 10.1-10.3) are other right routes and never a "
                                                         "wrong option. 4.7's working is ours: the memo gives C(−6 ; −9/4) only."
                                                         % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from the page IMAGES: the question paper "
                                                           "and answer book are scans with no text layer, and the memo's text layer garbles fractions "
                                                           "and diagrams; no API call."},
        {"n": "1.2", "kind": "no_fit", "detail": "A working that shows an earlier part's answer opens only once that part is answered ('after'): "
                                                 + "; ".join(k + " after " + " and ".join(v) for k, v in GATES.items()) + "."},
        {"n": "2.2", "kind": "no_fit", "detail": "The table's player numbers 1-8 are ours: the paper prints the eight scores in one row."},
        {"n": "2.1.3", "kind": "no_fit", "detail": "The drawing 2.1.3 (histogram) is done on paper and self-checked against the memo's "
                                                   "criteria. The app's histogram builder marks T C L S P (6 marks), not this memo's 3-mark scheme "
                                                   "(two frequencies, all frequencies, no gaps), so 2.1.3 is a plain draw. The answer book's blank "
                                                   "grid is not used: the scan shows darker grid segments that read like pre-drawn bars."},
        {"n": "7.2", "kind": "no_fit", "detail": "The graph of g (7.2) is BUILT on the answer book's axes (2026-10-11; the graph of f that the "
                                                 "answer book prints is not drawn on it): the learner places the four asymptotes and the four "
                                                 "intercepts, the tan curve is drawn through them, and the memo's three criteria are marked from "
                                                 "them (the shape from the curve the learner's own features fix). The x steps are 22,5°, half "
                                                 "the answer book's 45° lines, so the x-intercepts −67,5°, 22,5° and 112,5° are grid points."},
        {"n": "5.1.1", "kind": "no_fit", "detail": "Expressions in k with one step of working (5.1.1) and choices whose open or closed ends matter "
                                                   "(5.2.2, 7.4, 7.5), an equation of a graph (7.3) and the skewness (2.1.4) play as MCQs of the "
                                                   "plausible forms, all or nothing: 5.1.1 loses the memo's 'third side' mark, 7.5 (4 marks) its "
                                                   "x = 22,5° and inequality-sign marks."},
        {"n": "1.4", "kind": "low_confidence", "detail": "The yearly DECREASE is keyed as a positive amount (22 988,32); a learner typing −22 988,32 "
                                                         "is marked wrong."},
    ],
}
QTOTAL = {"1": 8, "2": 12, "3": 18, "4": 21, "5": 17, "6": 13, "7": 10, "8": 10, "9": 10, "10": 8, "11": 23}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter, spread evenly over A-D across the paper (the plausible-form MCQs included)
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and i["a"] < 4]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
print("right options, the paper:", spread, "authored:", {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"})
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; gated:", len(GATES))
print("total:", total)
out = Path(__file__).parent / "out" / "math-p2-2025-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper, memo and answer book PDFs' page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
