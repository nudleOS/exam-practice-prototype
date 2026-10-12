"""Grade 11 Mathematics P2 November 2024 (Eastern Cape Department of Education), the whole paper (Questions 1 to 10, 150 marks,
3 hours: statistics, analytical geometry, trigonometry, measurement, Euclidean geometry), hand-transcribed into the catalogue
format, then run through `ingest.py --from-json`. Stems, marks, answers and the memo's working are the paper's and the memo's own
(its English); clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the
question paper zip (English PDF, 16 pages; its diagrams are images) and the memo PDF (English and Afrikaans, 17 pages), read from
their page images at 90 dpi.

  python tools/ingest/transcribe_g11_math_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-math-p2-2024-11-ec/MATHS P2 QP GR11 2024 ENG D_watermark.pdf" "uploads/provincial/g11-math-p2-2024-11-ec/MATHS P2 GRADE 11 NOV 2024 ENG_AFR MARKING GUIDELINE_watermark.pdf" --id g11-math-p2-2024-11-ec --from-json

The memo's shapes map by the Grade 12 rulings (provincial.py); a geometry statement carries its [reason] at the line's end. The box
and whisker diagram 1.5 is built on a number line; the ogive 2.4 is pick the drawing (pictures_lower.py); the graph of h 6.4 is
built on a grid (a sine through its intercepts and turning point).
Question 3: the stem prints R(2 ; 3), the diagram R(3 ; 4); the memo marks both. The lead here follows the diagram (R(3 ; 4), whose
answers are whole numbers) so the words and the figure agree (flag below).
Figure boxes in PDF points (page 595 x 842): each diagram is one image, its box read from the PDF (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-math-p2-2024-11-ec", 595.2, 842.0, {
    "Q3": [5, 57.2, 189.8, 488.0, 442.0], "Q4": [6, 64.5, 157.1, 530.1, 443.3], "Q6": [8, 55.7, 131.8, 504.0, 377.2],
    "Q7": [9, 92.3, 153.1, 439.9, 344.6], "Q8": [10, 158.0, 197.3, 401.6, 514.4], "Q9.1": [11, 163.1, 117.6, 398.4, 340.9],
    "Q9.2": [12, 119.5, 123.9, 473.5, 371.1], "Q9.3": [13, 154.7, 106.1, 438.0, 365.4], "Q10.1": [14, 134.8, 160.0, 469.7, 445.1],
    "Q10.2": [15, 119.9, 184.3, 475.2, 492.1]}, start=3)
work, answer, num, draw, stmt = P.work, P.answer, P.num, P.draw, P.stmt

# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
q1 = [
    num("1.1", "Write down the mode of the data.", 41, 0, "", ["Which mark appears most often?", "Look along both rows of the table."]),
    num("1.2", "Identify any outlier.", 99, 0, "", ["Which mark lies far away from all the others?", "Is it at the low end or the high end?"]),
    num("1.3", "Determine the median of the data.", 54.5, 0, "", ["With 14 marks, which two are in the middle?", "The median is halfway "
                                                                                                                 "between them."], marks=2),
    work("1.4", "Determine the interquartile range of the data.", 3, [
        "Q₁ = 41\nQ₃ = 60\nIQR = Q₃ − Q₁ = 60 − 41\n= 19",         # the memo
        "Q₁ = 41\nQ₃ = 60\nIQR = Q₃ + Q₁ = 60 + 41\n= 101",        # the quartiles added
        "Q₁ = 28\nQ₃ = 62\nIQR = Q₃ − Q₁ = 62 − 28\n= 34",         # the second and the second-last values taken
        "Q₁ = 16\nQ₃ = 99\nIQR = Q₃ − Q₁ = 99 − 16\n= 83"],        # the range, not the interquartile range
        ["Split the 14 marks into a lower and an upper half of 7: what is the middle of each?", "The interquartile range is Q₃ minus Q₁."]),
    draw("1.5", "Draw a box and whisker diagram using the number line provided in the answer book.", 2, [
        ["The whiskers: out to the minimum 16 and the maximum 99", 1], ["The box: from Q₁ = 41 to Q₃ = 60, the median 54,5 inside it", 1]],
        ["Which five numbers does a box and whisker diagram need?", "Where do the ends of the box and the line inside it go?"],
        memo="The memo's diagram on the number line: whiskers from 16 to 41 and from 60 to 99, the box from 41 to 60 with the median at "
             "54,5. Five-number summary: 16 ; 41 ; 54,5 ; 60 ; 99.", after=["1.3", "1.4"],
        # built on a number line: the five values placed, marked as the memo marks it (✓ min and max, ✓ the box: Q₁, the median, Q₃)
        build={"kind": "boxplot", "x": [10, 100, 0.5], "tick": 1, "label": 10, "tol": 0,
               "at": {"min": 16, "q1": 41, "med": 54.5, "q3": 60, "max": 99},
               "crit": {"min": 0, "max": 0, "q1": 1, "med": 1, "q3": 1}}),
    answer("1.6", "Comment on the skewness of the data by using the box and whisker diagram.", 1,
           ["The data is skewed to the left (negatively skewed)", "The data is skewed to the right (positively skewed)",
            "The data is symmetrical", "The data has no skewness because of the outlier"],
           ["Is the median closer to Q₁ or to Q₃?", "Which side of the box is longer?"], after=["1.5"])]
for i in q1:   # the built box and whisker diagram: every memo criterion earned by its values, each value on the line's steps
    b = i.get("build") or {}
    if b.get("kind") == "boxplot":
        assert sorted(set(b["crit"].values())) == list(range(len(i["criteria"]))), i["n"]
        assert all(b["x"][0] <= u <= b["x"][1] and abs(u / b["x"][2] - round(u / b["x"][2])) < 1e-9 for u in b["at"].values()), i["n"]

# ---- QUESTION 2, the question paper page 4 and the memo page 3 ----
FX = "{1 × 45 + 3 × 65 + 9 × 85 + 6 × 105 + 3 × 125 + 1 × 145}/{23}"
q2 = [
    answer("2.1", "Complete the cumulative frequency column provided in the table in the ANSWER BOOK. (The cumulative frequencies, from the "
           "first class 35 ≤ x < 55 to the last 135 ≤ x < 155)", 2,
           ["1 ; 4 ; 13 ; 19 ; 22 ; 23", "1 ; 3 ; 9 ; 6 ; 3 ; 1", "0 ; 1 ; 4 ; 13 ; 19 ; 22", "23 ; 22 ; 19 ; 13 ; 4 ; 1"],
           ["Each cumulative frequency is the running total of the frequencies so far.", "What is the last cumulative frequency?"]),
    num("2.2", "Write down the total number of boxers.", 23, 0, "", ["Add up the frequencies.", "It is the last cumulative frequency."]),
    work("2.3", "Estimate the mean for the data.", 3, [
        "x̄ = " + FX + "\n= {2 155}/{23}\nx̄ = 93,70",                                                                   # the memo
        "x̄ = {1 × 35 + 3 × 55 + 9 × 75 + 6 × 95 + 3 × 115 + 1 × 135}/{23}\n= {1 925}/{23}\nx̄ = 83,70",                   # the lower limits
        "x̄ = {1 × 45 + 3 × 65 + 9 × 85 + 6 × 105 + 3 × 125 + 1 × 145}/{6}\n= {2 155}/{6}\nx̄ = 359,17",                    # ÷ the number of classes
        "x̄ = {1 × 55 + 3 × 75 + 9 × 95 + 6 × 115 + 3 × 135 + 1 × 155}/{23}\n= {2 385}/{23}\nx̄ = 103,70"],                # the upper limits
        ["Which value stands for every boxer in a class when the data is grouped?", "Multiply each midpoint by its frequency: what do you "
                                                                                    "divide the total by?"]),
    draw("2.4", "Use the grid provided in the ANSWER BOOK to draw a cumulative frequency graph (ogive) for the data.", 3, [
        ["Grounded at (35 ; 0)", 1], ["Each point plotted at the class's upper limit against its cumulative frequency", 1],
        ["The correct shape: a smooth S-shaped curve", 1]],
        ["At which x-values are the cumulative frequencies plotted?", "Where does the graph start, before the first class?"],
        memo="The memo's ogive: (35 ; 0), (55 ; 1), (75 ; 4), (95 ; 13), (115 ; 19), (135 ; 22) and (155 ; 23), joined by a smooth curve.",
        after=["2.1"]),
    work("2.5", "It is further given that, for a boxer to qualify for the next upcoming match, he must have a mass that is in the interval of "
         "75 < x ≤ 100.\n\nUsing the cumulative frequency graph (ogive), estimate the number of boxers that will qualify for the upcoming "
         "match.", 2, [
        "At 100 the ogive reads 15\nAt 75 it reads 4\nBoxers: 15 − 4 = 11",       # the memo
        "At 100 the ogive reads 15\nAt 75 it reads 4\nBoxers: 15 + 4 = 19",       # the readings added
        "At 100 the ogive reads 15\nAt 75 it reads 0\nBoxers: 15 − 0 = 15",       # every boxer up to 100 counted
        "At 95 the ogive reads 13\nAt 75 it reads 4\nBoxers: 13 − 4 = 9"],        # read at the class limit 95, not 100
        ["What does the ogive give you at x = 100, and at x = 75?", "How do two running totals give the number in between?"], after=["2.4"])]

# ---- QUESTION 3, the question paper page 5 and the memo page 4 (the guideline for R(3 ; 4)) ----
q3 = [
    work("3.1", "Calculate the gradient of PR.", 2, [
        "m(PR) = {4 − 0}/{3 − 0}\n= {4}/{3}",       # the memo
        "m(PR) = {3 − 0}/{4 − 0}\n= {3}/{4}",       # x over y
        "m(PR) = {4 − 2}/{3 − (−2)}\n= {2}/{5}",    # R and Q used
        "m(PR) = {4 + 0}/{3 − 0}\n= −{4}/{3}"],     # the sign lost
        ["Which two points on PR do you know?", "Gradient = change in y ÷ change in x."]),
    work("3.2", "Determine the equation of PR.", 3, [
        "m(PR) = {4}/{3} (P, O and R are collinear)\ny − 4 = {4}/{3}(x − 3)\ny = {4}/{3}x",         # the memo
        "m(PR) = {4}/{3} (P, O and R are collinear)\ny − 4 = {4}/{3}(x − 3)\ny = {4}/{3}x + 4",     # −4 + 4 left as + 4
        "m(PR) = {3}/{4} (P, O and R are collinear)\ny − 4 = {3}/{4}(x − 3)\ny = {3}/{4}x + {7}/{4}",  # the gradient upside down
        "m(PR) = −{3}/{4} (perpendicular to PR)\ny − 4 = −{3}/{4}(x − 3)\ny = −{3}/{4}x + {25}/{4}"],  # a perpendicular gradient
        ["Which point on PR makes the y-intercept easy to see?", "What is the y-intercept of a line through the origin?"], after=["3.1"]),
    work("3.3", "Determine the coordinates of P.", 4, [
        "6x + 14 = {4}/{3}x\n{14}/{3}x = −14\nx = −3\ny = 6(−3) + 14 = −4\nP(−3 ; −4)",           # the memo
        "6x + 14 = {4}/{3}x\n{22}/{3}x = −14\nx = −{21}/{11}\ny = 6(−{21}/{11}) + 14 = {28}/{11}\nP(−{21}/{11} ; {28}/{11})",  # + 4/3x
        "6x + 14 = {4}/{3}x\n{14}/{3}x = 14\nx = 3\ny = 6(3) + 14 = 32\nP(3 ; 32)",               # −14 moved without its sign change
        "6x + 14 = 0\n6x = −14\nx = −{7}/{3}\ny = 0\nP(−{7}/{3} ; 0)"],                           # the x-intercept S found instead
        ["P is on both PQ and PR: what do you do with their equations?", "Once you have x, which equation gives y most easily?"],
        after=["3.2"]),
    work("3.4", "Determine the coordinates of S.", 1, [
        "0 = 6x + 14\nx = −{7}/{3}\nS(−{7}/{3} ; 0)",     # the memo
        "0 = 6x + 14\nx = {7}/{3}\nS({7}/{3} ; 0)",       # 14 moved without its sign change
        "y = 6(0) + 14\ny = 14\nS(0 ; 14)",               # the y-intercept
        "0 = 6x + 14\nx = −{3}/{7}\nS(−{3}/{7} ; 0)"],    # the division upside down
        ["What is y at an x-intercept?", "Which equation is the line QP?"])]

# ---- QUESTION 4, the question paper page 6 and the memo pages 6-7 ----
q41 = [
    work("4.1.1", "Coordinates of P", 2, [
        "P = ({−7 + 3}/{2} ; {0 + 8}/{2})\nP(−2 ; 4)",     # the memo
        "P = ({−7 − 3}/{2} ; {0 − 8}/{2})\nP(−5 ; −4)",    # the coordinates subtracted
        "P = ({3 + 7}/{2} ; {8 + 0}/{2})\nP(5 ; 4)",       # −7 taken as 7
        "P = (−7 + 3 ; 0 + 8)\nP(−4 ; 8)"],                # not halved
        ["P is the midpoint of AB: which formula gives it?", "Add the x-values and halve; then the y-values."]),
    work("4.1.2", "Gradient of AB", 2, [
        "m(AB) = {8 − 0}/{3 + 7}\n= {4}/{5}",      # the memo
        "m(AB) = {8 − 0}/{3 − 7}\n= −2",           # −(−7) taken as −7
        "m(AB) = {3 + 7}/{8 − 0}\n= {5}/{4}",      # x over y
        "m(AB) = {8}/{3}\n= 2,67"],   # B's coordinates only
        ["Which two points on AB do you know?", "Gradient = change in y ÷ change in x."]),
    work("4.1.3", "Size of θ", 2, [
        "tan θ = {4}/{5}\nθ = 38,66°",      # the memo
        "tan θ = {5}/{4}\nθ = 51,34°",      # the gradient upside down
        "sin θ = {4}/{5}\nθ = 53,13°",      # sine for the gradient
        "cos θ = {4}/{5}\nθ = 36,87°"],     # cosine for the gradient
        ["How is the angle of inclination of a line related to its gradient?", "Which trigonometric ratio equals the gradient?"],
        after=["4.1.2"])]
q42 = [
    work("4.2", "Determine the equation of BC in the form y = mx + c.", 5, [
        "m(PQ) = {4 − 2}/{−2 − (−0,5)}\n= −{4}/{3}\nm(BC) = m(PQ) = −{4}/{3} [PQ ∥ BC]\n"
        "y − 8 = −{4}/{3}(x − 3)\ny = −{4}/{3}x + 12",                                                          # the memo
        "m(PQ) = {4 − 2}/{−2 − (−0,5)}\n= −{4}/{3}\nm(BC) = {3}/{4} [PQ ⊥ BC]\ny − 8 = {3}/{4}(x − 3)\ny = {3}/{4}x + {23}/{4}",  # perpendicular
        "m(PQ) = {4 − 2}/{−2 − (−0,5)}\n= −{4}/{3}\nm(BC) = m(PQ) = −{4}/{3} [PQ ∥ BC]\ny − 8 = −{4}/{3}(x − 3)\ny = −{4}/{3}x + 4",  # −8 + 4 slip
        "m(PQ) = {4 − 2}/{−2 + 0,5}\n= {4}/{3}\nm(BC) = m(PQ) = {4}/{3} [PQ ∥ BC]\ny − 8 = {4}/{3}(x − 3)\n"
        "y = {4}/{3}x + 4"],                                                                                      # the sign of −1,5 lost
        ["Which two points on PQ do you know, and how are the gradients of parallel lines related?", "Which point on BC can you use?"],
        after=["4.1.1"])]
q43 = [
    work("4.3.1", "Length of AC", 3, [
        "−{4}/{3}x + 12 = 0\nx = 9\nAC = 9 − (−7) = 16",        # the memo
        "−{4}/{3}x + 12 = 0\nx = −9\nAC = −9 − (−7) = −2",      # 12 moved without its sign change
        "−{4}/{3}x + 12 = 0\nx = 9\nAC = 9 − 7 = 2",            # −7 taken as 7
        "−{4}/{3}x + 12 = 0\nx = 16\nAC = 16 − (−7) = 23"],     # 12 × 4/3 for x
        ["Where does BC cut the x-axis?", "How far is it from A's x-value to C's?"], after=["4.2"]),
    work("4.3.2", "Area of trapezium PBCQ", 6, [
        "AB = √((3 + 7)² + (8 − 0)²) = √164\nArea ΔABC = {1}/{2} × √164 × 16 sin 38,65° = 63,99\n"
        "Area ΔAPQ = {1}/{2} × {√164}/{2} × 8 sin 38,65° = 16,00\nArea PBCQ = 47,99",                              # the memo
        "AB = √((3 + 7)² + (8 − 0)²) = √164\nArea ΔABC = √164 × 16 sin 38,65° = 127,99\n"
        "Area ΔAPQ = {√164}/{2} × 8 sin 38,65° = 32,00\nArea PBCQ = 95,99",                                       # the ½ left out
        "AB = √((3 + 7)² + (8 − 0)²) = √164\nArea ΔABC = {1}/{2} × √164 × 16 cos 38,65° = 80,00\n"
        "Area ΔAPQ = {1}/{2} × {√164}/{2} × 8 cos 38,65° = 20,00\nArea PBCQ = 60,00",                             # cos for sin
        "AB = √((3 + 7)² + (8 − 0)²) = √164\nArea ΔABC = {1}/{2} × √164 × 16 sin 38,65° = 63,99\n"
        "Area ΔAPQ = {1}/{2} × {√164}/{2} × 16 sin 38,65° = 32,00\nArea PBCQ = 31,99"],                           # AC for AQ
        ["The trapezium is ΔABC with ΔAPQ taken away: which two sides and the angle between them does each triangle have?", "How long "
                                                                                                                           "is AQ?"],
        after=["4.1.3", "4.3.1"])]

# ---- QUESTION 5, the question paper page 7 and the memo pages 8-10 ----
R14 = "x = 3, y = −√5, r = √(3² + (−√5)²) = √14 [diagram in quadrant 4]\n"
q5 = [
    work("5.1", "If −3 tan β − √5 = 0 and sin β < 0, determine the value of sin² β − cos² β with the aid of a diagram.", 5, [
        "tan β = −{√5}/{3}\n" + R14 + "sin² β − cos² β = ({−√5}/{√14})² − ({3}/{√14})²\n= −{2}/{7}",          # the memo
        "tan β = −{√5}/{3}\nx = −3, y = √5, r = √14 [diagram in quadrant 2]\nsin β − cos β = {√5}/{√14} − {−3}/{√14}\n= 1,40",  # quadrant 2; not squared
        "tan β = −{√5}/{3}\n" + R14 + "sin² β − cos² β = ({−√5}/{√14})² + ({3}/{√14})²\n= 1",                 # − taken as +
        "tan β = −{√5}/{3}\nx = 3, y = −√5, r = √(9 − 5) = 2 [diagram in quadrant 4]\nsin² β − cos² β = ({−√5}/{2})² − ({3}/{2})²\n= −1"],  # r² = x² − y²
        ["In which quadrant is tan β negative and sin β negative?", "Which side does Pythagoras give, and what are sin β and cos β?"])]
K = "√(1 − k²)"
q52 = [
    work("5.2.1", "sin 131°", 2, [
        "sin 131° = sin(180° − 49°)\n= sin 49°\n= " + K,          # the memo
        "sin 131° = sin(180° − 49°)\n= −sin 49°\n= −" + K,        # the sign of quadrant 2 wrong
        "sin 131° = sin(180° − 49°)\n= cos 49°\n= k",             # sin for cos
        "sin 131° = sin(90° + 41°)\n= −cos 41°\n= −" + K],        # the reduction 90° + θ wrong
        ["In which quadrant is 131°, and what is sin(180° − θ)?", "With cos 49° = k, which side is opposite 49° in a triangle with "
                                                                  "hypotenuse 1?"]),
    work("5.2.2", "1 − cos² 41°", 2, [
        "1 − cos² 41° = sin² 41°\n= k²",                 # the memo
        "1 − cos² 41° = sin² 41°\n= 1 − k²",             # sin 41° taken as √(1 − k²)
        "1 − cos² 41° = (1 − cos 41°)²\n= (1 − k)²",     # squared as a bracket
        "1 − cos² 41° = 1 − cos² 49°\n= 1 − k²"],        # 41° taken as 49°
        ["Which identity turns 1 − cos² θ into one ratio?", "41° and 49° add up to 90°: how are sin 41° and cos 49° related?"])]
T53 = "= {−tan x · cos x + sin² x · sin x}/{sin x}\n"
q53 = [
    work("5.3", "Simplify the expression to a single trigonometric ratio of x:\n(tan(180° − x) · cos(−x) + sin²(360° − x) cos(90° − x))/"
         "sin(180° − x)", 7, [
        T53 + "= {−sin x + sin³ x}/{sin x}\n= {−sin x(1 − sin² x)}/{sin x}\n= −cos² x",                     # the memo
        "= {tan x · cos x + sin² x · sin x}/{sin x}\n= {sin x + sin³ x}/{sin x}\n= {sin x(1 + sin² x)}/{sin x}\n= 1 + sin² x",  # tan(180° − x) as tan x
        T53 + "= {−sin x + sin³ x}/{sin x}\n= {−sin x(1 − sin² x)}/{sin x}\n= cos² x",                      # the minus lost
        "= {−tan x · cos x − sin² x · sin x}/{sin x}\n= {−sin x − sin³ x}/{sin x}\n= {−sin x(1 + sin² x)}/{sin x}\n= −1 − sin² x"],  # sin²(360° − x) as −sin² x
        ["Reduce each ratio: which quadrant is 180° − x, 360° − x, and what is cos(−x)?", "tan x = sin x/cos x: what is left to factorise?"])]
q54 = [
    work("5.4", "Simplify, without the use of a calculator:\nsin(−15°) · cos 75° + tan 75° · cos 75° · cos 165°", 5, [
        "= (−cos 75°)cos 75° + {sin 75°}/{cos 75°} · cos 75°(−sin 75°)\n= −cos² 75° − sin² 75°\n= −(cos² 75° + sin² 75°)\n= −1",   # the memo
        "= (cos 75°)cos 75° + {sin 75°}/{cos 75°} · cos 75°(sin 75°)\n= cos² 75° + sin² 75°\n= (cos² 75° + sin² 75°)\n= 1",         # the signs lost
        "= (−cos 75°)cos 75° + {sin 75°}/{cos 75°} · cos 75°(−sin 75°)\n= −cos² 75° − sin² 75°\n= −(cos² 75° − sin² 75°)\n= −cos 150°",  # the bracket's sign
        "= (−sin 75°)cos 75° + {sin 75°}/{cos 75°} · cos 75°(−cos 75°)\n= −sin 75° cos 75° − sin 75° cos 75°\n= −2 sin 75° cos 75°\n"
        "= −sin 150°"],                                                                                                             # co-functions swapped
        ["Write sin(−15°) and cos 165° as ratios of 75°.", "What is cos² θ + sin² θ?"])]
L55 = "LHS = {3 cos x}/{1 + sin x} + {3 sin x}/{cos x}\n"
q55 = [
    work("5.5", "Prove the identity: 3 cos x/(1 + sin x) + 3 tan x = 3/cos x", 4, [
        L55 + "= {3 cos² x + 3 sin x + 3 sin² x}/{cos x(1 + sin x)}\n= {3(cos² x + sin² x) + 3 sin x}/{cos x(1 + sin x)}\n"
        "= {3(1 + sin x)}/{cos x(1 + sin x)}\n= {3}/{cos x} = RHS",                                                      # the memo
        L55 + "= {3 cos x + 3 sin x}/{cos x + 1 + sin x}\n= {3(cos x + sin x)}/{cos x + 1 + sin x}\n= {3(1 + sin x)}/{cos x(1 + sin x)}\n"
        "= {3}/{cos x} = RHS",                                                                                             # tops and bottoms added
        "RHS = {3}/{cos x}\n= {3(1 + sin x)}/{cos x(1 + sin x)}\n= {3 cos² x + 3 sin² x + 3 sin x}/{cos x(1 + sin x)}\n"
        "= {3 cos x}/{1 + sin x} + 3 tan x\n= LHS",                                                                        # worked back from the answer
        L55 + "= {3 cos² x + 3 sin x + 3 sin² x}/{cos x(1 + sin x)}\n= {3(cos² x − sin² x) + 3 sin x}/{cos x(1 + sin x)}\n"
        "= {3(1 + sin x)}/{cos x(1 + sin x)}\n= {3}/{cos x} = RHS"],                                                     # the square identity wrong
        ["Write tan x as sin x/cos x: what is the lowest common denominator?", "Which identity turns cos² x + sin² x into 1?"])]
q56 = [
    work("5.6", "Determine the general solution of: sin² x − 3 cos² x = 0", 5, [
        "sin² x = 3 cos² x\ntan² x = 3\ntan x = ±√3\nx = 60° + k · 180° or x = −60° + k · 180°, k ∈ ℤ",          # the memo
        "sin² x = 3 cos² x\ntan² x = 3\ntan x = √3\nx = 60° + k · 180°, k ∈ ℤ",                                 # the negative root lost
        "sin² x = 3 cos² x\ntan² x = 3\ntan x = ±√3\nx = 60° + k · 360° or x = −60° + k · 360°, k ∈ ℤ",         # tan's period taken as 360°
        "sin² x = 3 cos² x\ntan² x = {1}/{3}\ntan x = ±{1}/{√3}\nx = 30° + k · 180° or x = −30° + k · 180°, k ∈ ℤ"],  # divided the wrong way
        ["Divide by cos² x: which ratio do you get?", "What is the period of tan, and how many signs does the square root give?"])]

# ---- QUESTION 6, the question paper page 8 and the memo page 11 ----
q6 = [
    answer("6.1", "Write down the period of f.", 1, ["360°", "180°", "270°", "30°"], ["How long does one full wave of a cosine take?",
                                                                                         "Does the + 30° change the period?"]),
    answer("6.2", "Write down the range of h(x) = f(x + 60°) + 1.", 2, ["y ∈ [0 ; 2]", "y ∈ [−1 ; 1]", "y ∈ [1 ; 3]", "y ∈ [−2 ; 0]"],
           ["What is the range of f?", "Which part of h moves the graph up or down?"]),
    work("6.3", "Write down the equation of h in its simplest form.", 2, [
        "h(x) = cos(60° + x + 30°) + 1\n= cos(90° + x) + 1\n= −sin x + 1",        # the memo
        "h(x) = cos(60° + x + 30°) + 1\n= cos(90° + x) + 1\n= sin x + 1",         # cos(90° + x) taken as sin x
        "h(x) = cos(x + 30° − 60°) + 1\n= cos(x − 30°) + 1\n= cos x − cos 30° + 1",   # shifted the wrong way; cos spread over the bracket
        "h(x) = cos(60° + x + 30°) + 1\n= cos(90° + x) + 1\n= −cos x + 1"],       # cos(90° + x) taken as −cos x
        ["What is f(x + 60°) when f(x) = cos(x + 30°)?", "Which ratio is cos(90° + x)?"]),
    draw("6.4", "Draw the graph of h(x) on the grid provided in your ANSWER BOOK.", 3, [
        ["The x-intercept (90° ; 0)", 1], ["The y-intercept (0 ; 1)", 1], ["The correct shape", 1]],
        ["Where does h cut the axes?", "h(x) = −sin x + 1: where is its highest point in the interval?"],
        memo="The memo's graph of h on the grid with f: from (−120° ; 1,87) up to its maximum (−90° ; 2), down through (0 ; 1) to its "
             "minimum (90° ; 0) on the x-axis, and up to (150° ; 0,5).", after=["6.3"],
        # built on a grid (as transcribe_math_p2_2024_11.py 7.3.2): the x-intercept and the y-intercept carry their marks; the
        # turning point (−90° ; 2), 0 marks, fixes the sine with them, and the shape is the curve through them
        build={"kind": "sketch", "family": "sin", "b": 1, "x": [-120, 150, 15], "y": [-2, 3, 0.5], "domain": [-120, 150], "features": [
            {"id": "hx", "kind": "point", "label": "x-intercept", "at": [90, 0], "tol": 0, "marks": 1, "crit": 0},
            {"id": "hy", "kind": "point", "label": "y-intercept", "at": [0, 1], "tol": 0, "marks": 1, "crit": 1},
            {"id": "ht", "kind": "point", "label": "turning point", "at": [-90, 2], "tol": 0, "marks": 0, "crit": 2, "turn": True}],
               "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 2}}),
    answer("6.5.1", "For which values of x is f having a minimum value?", 1, ["x = 150°", "x = −30°", "x = −120°", "x = 60°"],
           ["Where is f at its lowest in the interval?", "What is f(150°)?"]),
    answer("6.5.2", "For which values of x is h(x) × f(x) ≤ 0?", 2, ["60° ≤ x ≤ 150°", "−120° ≤ x ≤ 60°", "60° < x < 150°", "90° ≤ x ≤ 150°"],
           ["Can h ever be negative?", "Where is f on or below the x-axis?"], after=["6.4"]),
    answer("6.5.3", "For which values of x is f(x) = h(x)?", 1, ["x = 30°", "x = 0°", "x = 60°", "x = 90°"],
           ["Where do the two graphs cross?", "Check: is cos(x + 30°) = 1 − sin x there?"], after=["6.4"])]

# ---- QUESTION 7, the question paper page 9 and the memo page 12 ----
q7 = [
    answer("7.1", "Express PS in terms of α.", 1, ["PS = {5}/{cos α}", "PS = 5 cos α", "PS = {5}/{sin α}", "PS = 5 tan α"],
           ["In right-angled ΔSVP, which side is next to α and which is the hypotenuse?", "cos α = adjacent ÷ hypotenuse."]),
    work("7.2", "Determine RP in terms of α and β.", 3, [
        "PR̂Q = β [alt ∠s; RQ ∥ SP]\n{sin α}/{RP} = {sin β}/{5}\nRP = {5 sin α}/{sin β}",          # the memo
        "PR̂Q = β [alt ∠s; RQ ∥ SP]\n{sin α}/{5} = {sin β}/{RP}\nRP = {5 sin β}/{sin α}",          # the sides and angles mismatched
        "PR̂Q = β [corresp ∠s; RQ ∥ SP]\n{sin α}/{RP} = {sin β}/{5}\nRP = {5 sin α}/{sin β}",      # the wrong reason
        "PR̂Q = α [alt ∠s; RQ ∥ SP]\n{sin α}/{RP} = {sin α}/{5}\nRP = 5"],                          # the wrong pair of angles
        ["Which angle of ΔPQR equals β, and why?", "In the sine rule, which side is opposite α and which opposite β?"]),
    work("7.3", "Hence show that the area of ΔRPS = 25 tan α/2", 3, [
        "Area ΔRPS = {1}/{2}(RP)(PS) sin β\n= {1}/{2}({5 sin α}/{sin β})({5}/{cos α}) sin β\n= {25 sin α}/{2 cos α}\n= {25 tan α}/{2}",  # the memo
        "Area ΔRPS = {1}/{2}(RP)(PS) cos β\n= {1}/{2}({5 sin α}/{sin β})({5}/{cos α}) sin β\n= {25 sin α}/{2 cos α}\n= {25 tan α}/{2}",  # the area rule with cos
        "Area ΔRPS = {1}/{2}(PS)(SR) sin α\n= {1}/{2}({5}/{cos α})(5) sin α\n= {25 sin α}/{2 cos α}\n= {25 tan α}/{2}",                  # SR taken as 5
        "Area ΔRPS = {1}/{2}(RP)(PS)\n= {1}/{2}({5 sin α}/{sin β})({5}/{cos α})\n= {25 sin α}/{2 cos α}\n= {25 tan α}/{2}"],             # the sine dropped
        ["Which two sides of ΔRPS have you found, and which angle lies between them?", "What is sin α/cos α?"], after=["7.1", "7.2"])]

# ---- QUESTION 8, the question paper page 10 and the memo page 13 ----
q8 = [
    work("8.1", "Determine the height of the cone.", 3, [
        "13² = 5² + h²\nh² = 169 − 25 = 144\nh = 12 cm",        # the memo
        "13² = 10² + h²\nh² = 169 − 100 = 69\nh = 8,31 cm",    # the diameter for the radius
        "h² = 13² + 5²\nh² = 169 + 25 = 194\nh = 13,93 cm",    # the slant height taken as a leg
        "13 = 5 + h\nh = 13 − 5 = 8\nh = 8 cm"],               # the sides added, not squared
        ["Which right-angled triangle holds the slant height, the radius and h?", "Which side is the hypotenuse?"]),
    answer("8.2", "Write down the height of the container (height of the whole shape).", 1, ["17 cm", "12 cm", "22 cm", "25 cm"],
           ["The container is the cone on top of the hemisphere: what is the hemisphere's height?", "Add it to the cone's height."],
           after=["8.1"]),
    work("8.3", "Calculate the volume of this container.", 3, [
        "V = {2}/{3}πr³ + {1}/{3}πr²h\n= {2}/{3}π(5)³ + {1}/{3}π(5)²(12)\n= 575,96 cm³",           # the memo
        "V = {2}/{3}πr³ + {1}/{3}πr²h\n= {2}/{3}π(10)³ + {1}/{3}π(10)²(12)\n= 3 351,03 cm³",       # the diameter for r
        "V = {4}/{3}πr³ + {1}/{3}πr²h\n= {4}/{3}π(5)³ + {1}/{3}π(5)²(12)\n= 837,76 cm³",           # a whole sphere
        "V = {2}/{3}πr³ + {1}/{3}πr²h\n= {2}/{3}π(5)³ + {1}/{3}π(5)²(13)\n= 602,14 cm³"],          # the slant height for h
        ["Which two shapes make up the container?", "Which length is the cone's height, and which its radius?"], after=["8.1"]),
    work("8.4", "Determine the total surface area of the container.", 3, [
        "SA = 2πr² + πrs\n= 2π(5)² + π(5)(13)\n= 361,28 cm²",              # the memo
        "SA = 2πr² + πr² + πrs\n= 2π(5)² + π(5)² + π(5)(13)\n= 439,82 cm²",  # the shared circle counted
        "SA = 2πr² + πrs\n= 2π(5)² + π(5)(12)\n= 345,58 cm²",              # the height for the slant height
        "SA = 4πr² + πrs\n= 4π(5)² + π(5)(13)\n= 518,36 cm²"],             # a whole sphere's surface
        ["Which surfaces are on the outside of the container?", "Which length is s in πrs?"])]

# ---- QUESTION 9, the question paper pages 11-13 and the memo pages 14-15 ----
CON = "Construction: draw AO and OC\n"
q91 = [
    work("9.1", "Use the diagram above to prove the THEOREM which states that, the opposite angles of a cyclic quadrilateral add up to 180°, "
         "then prove that, B̂ + D̂ = 180°.", 5, [
        CON + "Ô₁ = 2B̂ [∠ at centre = 2 × ∠ at circumf]\nÔ₂ = 2D̂ [∠ at centre = 2 × ∠ at circumf]\nÔ₁ + Ô₂ = 360° [∠s around a point]\n"
              "2B̂ + 2D̂ = 360°, so B̂ + D̂ = 180°",                                                                    # the memo
        CON + "Ô₁ = 2B̂ [∠ at centre = 2 × ∠ at circumf]\nÔ₂ = 2D̂ [∠ at centre = 2 × ∠ at circumf]\nÔ₁ + Ô₂ = 180° [∠s on a str line]\n"
              "2B̂ + 2D̂ = 180°, so B̂ + D̂ = 180°",                                                                    # the wrong reason and sum
        CON + "Ô₁ = B̂ [∠s in the same seg]\nÔ₂ = D̂ [∠s in the same seg]\nÔ₁ + Ô₂ = 180° [∠s on a str line]\nB̂ + D̂ = 180°",  # the wrong theorems
        CON + "B̂ + D̂ = 180° [opp ∠s of cyclic quad]\nÔ₁ = 2B̂ and Ô₂ = 2D̂ [∠ at centre = 2 × ∠ at circumf]\n"
              "Ô₁ + Ô₂ = 360° [∠s around a point]\nSo B̂ + D̂ = 180°"],                                                 # the theorem used to prove itself
        ["Which construction lets you use angles at the centre O?", "What do the two angles at O, on either side of AO and OC, add up "
                                                                    "to?"])]
q92 = [
    work("9.2.1", "Ŝ", 2, [
        "Ŝ = {1}/{2} × 230°\nŜ = 115° [∠ at centre = 2 × ∠ at circumf]",     # the memo
        "Ŝ = {1}/{2} × 130°\nŜ = 65° [∠ at centre = 2 × ∠ at circumf]",      # the non-reflex angle used
        "Ŝ = 2 × 230°\nŜ = 460° [∠ at centre = 2 × ∠ at circumf]",          # doubled, not halved
        "Ŝ = {1}/{2} × 230°\nŜ = 115° [opp ∠s of cyclic quad]"],             # the wrong reason
        ["Which angle at the centre stands on the same arc as Ŝ?", "How is an angle at the centre related to one at the circumference?"]),
    work("9.2.2", "Q̂", 2, [
        "Q̂ = 180° − 115°\nQ̂ = 65° [opp ∠s of cyclic quad]",           # the memo
        "Q̂ = 180° − 85°\nQ̂ = 95° [opp ∠s of cyclic quad]",   # the exterior angle used
        "Q̂ = 115°\nQ̂ = Ŝ [∠s in the same seg]",                        # equal, not supplementary
        "Q̂ = 180° − 115°\nQ̂ = 65° [∠s on a str line]"],                # the wrong reason
        ["Which angle of the cyclic quadrilateral is opposite Q̂?", "What do opposite angles of a cyclic quadrilateral add up to?"],
        after=["9.2.1"]),
    work("9.2.3", "P̂₁", 2, [
        "P̂₁ + 20° = 85° [ext ∠ of cyclic quad]\nP̂₁ = 65°",           # the memo
        "P̂₁ + 20° = 95° [opp ∠s of cyclic quad]\nP̂₁ = 75°",          # 180° − 85° taken as the angle at P
        "P̂₁ = 85° [ext ∠ of cyclic quad]\nP̂₁ = 85°",                 # the 20° left out
        "P̂₁ + 20° = 85° [∠s in the same seg]\nP̂₁ = 65°"],            # the wrong reason
        ["Which interior angle equals the exterior angle QR̂T?", "The angle at P is made of P̂₁ and 20°."])]
q93 = [
    work("9.3", "Calculate, giving reasons, the size of P̂.", 4, [
        "Â₁ = 50° [∠s on a str line]\nR̂ = 110° [∠s in a Δ]\nP̂ = 70° [opp ∠s of a cyclic quad]",       # the memo
        "Â₁ = 50° [∠s on a str line]\nR̂ = 110° [∠s in a Δ]\nP̂ = 110° [∠s in the same seg]",         # equal, not supplementary
        "Â₁ = 130° [vert opp ∠s]\nR̂ = 30° [∠s in a Δ]\nP̂ = 150° [opp ∠s of a cyclic quad]",         # the angle at A misread
        "Â₁ = 50° [∠s on a str line]\nR̂ = 70° [∠s in a Δ]\nP̂ = 110° [opp ∠s of a cyclic quad]"],    # 180° − 50° − 20° slipped
        ["What is the angle at A inside ΔQAR?", "Which angle of the cyclic quadrilateral is opposite P̂?"])]

# ---- QUESTION 10, the question paper pages 14-15 and the memo pages 16-17 ----
q101 = [
    work("10.1.1", "Determine, giving reasons, the size of Ô₁.", 4, [
        "Â₁ = 37° [tan chord]\nÔ₁ = 2Â₁ = 74° [∠ at centre = 2 × ∠ at circumf]",       # the memo
        "Â₁ = 37° [tan chord]\nÔ₁ = Â₁ = 37° [∠s in the same seg]",                     # equal, not double
        "Â₁ = 53° [tan ⊥ radius]\nÔ₁ = 2Â₁ = 106° [∠ at centre = 2 × ∠ at circumf]",    # 90° − 37°
        "Â₁ = 37° [alt ∠s]\nÔ₁ = 2Â₁ = 74° [∠ at centre = 2 × ∠ at circumf]"],          # the wrong reason
        ["Which angle in the alternate segment equals the angle between the tangent PN and the chord PB?", "How is the angle at the centre "
                                                                                                           "on chord PB related to Â₁?"]),
    work("10.1.2(a)", "Prove that: OACB is a cyclic quadrilateral", 4, [
        "AB̂P = 90° [∠ in a semi-circle]\nB̂₁ = 90° [∠s on a str line]\nÔ₃ = 90° [given]\nÔ₃ = B̂₁, so OACB is a cyclic quad "
        "[converse ∠s in the same seg]",                                                                                  # the memo
        "AB̂P = 90° [∠ in a semi-circle]\nB̂₁ = 90° [∠s on a str line]\nÔ₃ = 90° [given]\nÔ₃ = B̂₁, so OACB is a cyclic quad "
        "[opp ∠s of a cyclic quad]",                                                                                      # the theorem, not its converse
        "AB̂P = 90° [tan ⊥ radius]\nB̂₁ = 90° [∠s on a str line]\nÔ₃ = 90° [given]\nÔ₃ = B̂₁, so OACB is a cyclic quad "
        "[converse ∠s in the same seg]",                                                                                  # the wrong reason for 90°
        "OACB is a cyclic quad [given]\nB̂₁ = 90° [∠s in the same seg]\nÔ₃ = 90° [given]\nÔ₃ = B̂₁, so OACB is a cyclic quad "
        "[converse ∠s in the same seg]"],                                                                                 # starts from the answer
        ["AP is a diameter: what is the angle at B in ΔABP?", "Which two equal angles stand on the same side AC of OACB?"]),
    work("10.1.2(b)", "Prove that: OC ∥ PN", 3, [
        "Ĉ₂ = Â₁ = 37° [∠s in the same seg]\nĈ₂ = P̂₂ = 37°\nOC ∥ PN [alt ∠s =]",           # the memo
        "Ĉ₂ = Â₁ = 37° [∠s in the same seg]\nĈ₂ = P̂₂ = 37°\nOC ∥ PN [co-int ∠s supp]",     # the wrong converse
        "Ĉ₂ = Ô₁ = 74° [∠s in the same seg]\nĈ₂ = 2P̂₂\nOC ∥ PN [alt ∠s =]",                # the wrong angle at C
        "OC ∥ PN [given]\nĈ₂ = P̂₂ = 37°\nOC ∥ PN [alt ∠s =]"],          # starts from the answer
        ["In cyclic quadrilateral OACB, which angle at A stands on the same chord as Ĉ₂?", "Which pair of angles do OC and PN make with the "
                                                                                          "line PC?"],
        after=["10.1.1", "10.1.2(a)"])]
q102 = [
    work("10.2.1", "Name, giving reasons, 3 angles equal to 90°.", 6, [
        "Â₃ = 90° [tan ⊥ rad]\nŜ₁ = 90° [tan-chord theorem]\nĈ = 90° [∠ in semi-circle]",           # the memo
        "Â₃ = 90° [tan ⊥ rad]\nŜ₁ = 90° [tan-chord theorem]\nB̂ = 90° [∠ in semi-circle]",           # the angle at B, not C
        "Â₃ = 90° [∠ in semi-circle]\nŜ₁ = 90° [tan ⊥ rad]\nĈ = 90° [tan-chord theorem]",           # the reasons swapped round
        "Â₁ = 90° [tan ⊥ rad]\nŜ₂ = 90° [∠s on a str line]\nM̂₁ = 90° [∠ in semi-circle]"],          # the wrong angles
        ["Which line through A is perpendicular to the tangent PAT?", "AB is a diameter of the larger circle: which angle stands on it?"]),
    answer("10.2.2", "Give a reason why MS ∥ BC.", 1, ["Corresp ∠s = (Ŝ₁ = Ĉ = 90°)", "Alt ∠s = (Ŝ₁ = Ĉ = 90°)",
                                                       "Co-int ∠s = (Ŝ₁ + Ĉ = 180°)", "Midpoint theorem"],
           ["Ŝ₁ and Ĉ are both 90°: where do they sit on the line AC?", "Which pair of angles is in matching positions?"],
           after=["10.2.1"]),
    answer("10.2.3", "Write down the ratio of AS : SC with a reason.", 2, ["AS : SC = 1 : 1 [line from centre ⊥ to chord]",
                                                                          "AS : SC = 1 : 2 [line from centre ⊥ to chord]",
                                                                          "AS : SC = 1 : 1 [tan-chord theorem]",
                                                                          "AS : SC = p : 6 [prop theorem; MS ∥ BC]"],
           ["M is the centre of the larger circle and MS ⊥ AC: what does the line from the centre do to the chord?", "Which reason names "
                                                                                                                     "that?"],
           after=["10.2.1"]),
    answer("10.2.4", "Write down the length of MS with a reason.", 2, ["MS = 3 [midpoint theorem]", "MS = 6 [midpoint theorem]",
                                                                       "MS = 3 [line from centre ⊥ to chord]", "MS = 12 [midpoint theorem]"],
           ["M and S are midpoints of AB and AC: how is MS related to BC?", "BC = 6 units."], after=["10.2.3"]),
    work("10.2.5", "Calculate the value of p.", 3, [
        "p² = (p − 1)² + 3² [Pyth]\np² = p² − 2p + 1 + 9\n2p = 10, so p = 5",       # the memo
        "p² = (p − 1)² + 3² [Pyth]\np² = p² + 1 + 9\n0 = 10: no value of p",         # (p − 1)² taken as p² + 1
        "(p − 1)² = p² + 3² [Pyth]\np² − 2p + 1 = p² + 9\n−2p = 8, so p = −4",      # the hypotenuse taken as AS
        "p² = (p − 1)² + 6² [Pyth]\np² = p² − 2p + 1 + 36\n2p = 37, so p = 18,5"],  # BC for MS
        ["Which right-angled triangle has sides p, p − 1 and MS?", "Which side is its hypotenuse?"], after=["10.2.4"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Data handling", "marks": 10,
     "lead": "After utilising GeoGebra to teach geometry, the 14 participants marks out of 100 are displayed in the table below.\n"
             "16 ; 28 ; 41 ; 41 ; 42 ; 52 ; 54 ; 55 ; 58 ; 59 ; 60 ; 62 ; 64 ; 99", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Grouped data and the ogive", "marks": 11,
     "lead": "The weight of the boxers who underwent fitness and health checks is shown in the frequency table below.\n"
             "Weight of boxers: frequency\n35 ≤ x < 55: 1\n55 ≤ x < 75: 3\n75 ≤ x < 95: 9\n95 ≤ x < 115: 6\n115 ≤ x < 135: 3\n135 ≤ x < 155: 1",
     "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Analytical geometry", "marks": 10,
     "lead": "In the diagram, P(x ; y), Q(−2 ; 2) and R(3 ; 4) are the vertices of triangle PQR. Line PR passes through the point of origin "
             "at O. The equation of line PQ is given as y = 6x + 14. S is the x-intercept of line QP.",
     "figure": P.fig("Q3", "Triangle PQR: Q(−2 ; 2) above the x-axis on the left, R(3 ; 4) top right, P(x ; y) bottom left below the "
                           "x-axis. PR passes through the origin O; QP cuts the x-axis at S."), "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Analytical geometry", "marks": 6,
     "lead": "In the diagram, ΔABC is drawn with vertices A(−7 ; 0), B(3 ; 8) and C. P is the midpoint of line AB. Q is a point on line AC. "
             "AQC is a line on the x-axis. E(−1/2 ; 2) is a point on line PQ. PQ ∥ BC\n\nCalculate the:",
     "figure": P.fig("Q4", "Triangle ABC with A(−7 ; 0) and C on the x-axis and B(3 ; 8) above. P is the midpoint of AB; PQ, through "
                           "E(−1/2 ; 2), runs down to Q on the x-axis, parallel to BC. θ is the angle at A between AB and the x-axis."),
     "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Analytical geometry", "marks": 5, "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Analytical geometry", "marks": 9, "lead": "Calculate the:", "items": q43},
    {"id": "5.1", "title": "Question 5.1", "kind": "Trigonometry", "marks": 5, "items": q5},
    {"id": "5.2", "title": "Question 5.2", "kind": "Reduction formulae", "marks": 4,
     "lead": "If cos 49° = k, determine the values of the following in terms of k.", "items": q52},
    {"id": "5.3", "title": "Question 5.3", "kind": "Reduction formulae", "marks": 7, "items": q53},
    {"id": "5.4", "title": "Question 5.4", "kind": "Reduction formulae", "marks": 5, "items": q54},
    {"id": "5.5", "title": "Question 5.5", "kind": "Identities", "marks": 4, "items": q55},
    {"id": "5.6", "title": "Question 5.6", "kind": "General solution", "marks": 5, "items": q56},
    {"id": "6", "title": "Question 6", "kind": "Trigonometric graphs", "marks": 12,
     "lead": "The graph of f(x) = cos(x + 30°) in the interval of x ∈ [−120° ; 150°] has been drawn in the diagram below.",
     "figure": P.fig("Q6", "The graph of f on a grid, x from −120° to 150° in steps of 30°, y from −1 to 2: f rises from the x-axis at "
                           "−120° to its maximum at −30°, crosses the x-axis at 60° and falls to its minimum at 150°."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Trigonometry in two dimensions", "marks": 7,
     "lead": "In the diagram, VP = PQ = 5 units, RQ̂P = SP̂V = α, SP̂R = β and PS ∥ QR. SV is perpendicular to VP.",
     "figure": P.fig("Q7", "Quadrilateral SRQP with SR across the top and triangle SVP below on the left, right-angled at V, VP = 5. "
                           "From P, lines go to S, to R and to Q; α marks the angle at P between VP and PS and the angle at Q; β the angle "
                           "at P between PS and PR; arrows mark PS ∥ QR."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Measurement", "marks": 10,
     "lead": "In the diagram, a lid with a hemispherical form seals an open cone. The slanted height of the cone is 13 cm, the diameter of the "
             "cone and hemisphere is 10 cm, the height of the cone h cm.\nFormulae: V = (2/3)πr³ ; V = (1/3)πr²h ; Surface Area = πr² + πrs ; "
             "Surface Area = 2πr²",
     "figure": P.fig("Q8", "A cone standing point up on a hemisphere of the same circle: the slant height marked 13 cm, the cone's height "
                           "h dashed from its tip to the centre of the circle, and the diameter 10 cm."), "items": q8},
    {"id": "9.1", "title": "Question 9.1", "kind": "Euclidean geometry", "marks": 5,
     "lead": "In the diagram, ABCD is a cyclic quadrilateral. O is the centre of the circle.",
     "figure": P.fig("Q9.1", "A circle with centre O and the cyclic quadrilateral ABCD: A on the left, B at the top right, C on the right, "
                             "D at the bottom left."), "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Euclidean geometry", "marks": 6,
     "lead": "In the diagram, O is the centre of the circle with a reflex angle of 230°. P, Q, R and S are points on the circumference of the "
             "circle with chord SR extended to point T. QR̂T = 85° and OP̂S = 20°.\n\nCalculate the magnitude of the following angles:",
     "figure": P.fig("Q9.2", "A circle with centre O: P on the left, Q at the top, R on the right, S at the bottom. The reflex angle POR at "
                             "O is 230°; SR is extended to T, with 85° between QR and RT; P̂₁ is between PQ and PO, and 20° between PO and "
                             "PS."), "items": q92},
    {"id": "9.3", "title": "Question 9.3", "kind": "Euclidean geometry", "marks": 4,
     "lead": "In the diagram, PQRS is a cyclic quadrilateral. QA intersects SR at point A. SÂQ = 130° and AQ̂R = 20°.",
     "figure": P.fig("Q9.3", "A circle through P (left), Q (top), R (right) and S (bottom). QA meets SR at A: 130° at A between AS and AQ, "
                             "20° at Q between QA and QR."), "items": q93},
    {"id": "10.1", "title": "Question 10.1", "kind": "Euclidean geometry", "marks": 11,
     "lead": "In the diagram, O is the centre of circle ABP. PB is extended to C. AC is drawn. PN is a tangent to the circle at P. OC intersects "
             "AP perpendicularly at point O. P̂₂ = 37°",
     "figure": P.fig("Q10.1", "A circle with centre O on the diameter AP. B is on the circle; PB is extended to C outside the circle. OC "
                              "is perpendicular to AP at O; AB, AC and OB are drawn. PN is the tangent at P, with 37° between PB and PN."),
     "items": q101},
    {"id": "10.2", "title": "Question 10.2", "kind": "Euclidean geometry", "marks": 14,
     "lead": "In the diagram, PAT is the common tangent of the smaller and larger circles at A. AMB is the diameter of the larger circle with M "
             "on the circumference of the smaller circle. ASC and BC are chords of the larger circle and MS chord of the smaller circle. M is "
             "the centre of the larger circle.\nIt is also given that, the length of AM = p units, AS = (p − 1) units and BC = 6 units.",
     "figure": P.fig("Q10.2", "Two circles touching inside at A, where the tangent PAT touches both. AMB crosses the larger circle, M on "
                              "the smaller one; ASC is a chord of the larger circle through S on the smaller one; MS and BC are drawn."),
     "items": q102},
]
P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
         [P.flag_workings("In a 'show that' or 'prove' (5.5, 7.3, 9.1, 10.1.2(a), 10.1.2(b)) every option ends in the given result; a "
                          "wrong one reaches it through a wrong step or reason, or by starting from the answer."),
          P.flag_answers(),
          {"n": "1.1", "kind": "no_fit", "detail": "Read-off numbers stay typed on the keypad: 1.1 (41), 1.2 (99), 1.3 (54,5: the memo gives "
                                                   "an answer only full marks), 2.2 (23)."},
          {"n": "1.5", "kind": "no_fit", "detail": "The box and whisker diagram is BUILT on a number line (the five values placed, the memo's "
                                                   "two criteria marked from them); the graph of h (6.4) is BUILT on a grid (its x- and "
                                                   "y-intercept and its maximum fix the curve). The ogive (2.4) plays as pick the drawing: "
                                                   "the memo's and three plotting mistakes (lower limits, not grounded, the frequencies)."},
          {"n": "paper", "kind": "low_confidence", "detail": "Question 3: the paper's stem prints R(2 ; 3), its diagram R(3 ; 4); the memo marks "
                                                             "both (page 4 for R(3 ; 4), page 5 for R(2 ; 3)). The lead here follows the "
                                                             "diagram, R(3 ; 4), so the words and the figure agree; the answers are the R(3 ; 4) "
                                                             "guideline's."},
          {"n": "5.1", "kind": "memo_issue", "detail": "The memo's first line (page 8) reads −3 tan β = 5; the stem's −3 tan β − √5 = 0 gives "
                                                       "−3 tan β = √5, which its next line uses (tan β = −√5/3). The right option starts at "
                                                       "tan β = −√5/3."},
          {"n": "4.3.2", "kind": "memo_issue", "detail": "The memo (page 7) uses θ = 38,65° in the areas after finding 38,66° in 4.1.3; its "
                                                         "63,99, 16,00 and 47,99 are kept (exactly, ΔABC = ½ × 16 × 8 = 64 and PBCQ = 48)."}],
         {"1": 10, "2": 11, "3": 10, "4": 20, "5": 30, "6": 12, "7": 7, "8": 10, "9": 15, "10": 25}, 150,
         {"1.5": ["1.3", "1.4"], "1.6": ["1.5"], "2.4": ["2.1"], "2.5": ["2.4"], "3.2": ["3.1"], "3.3": ["3.2"], "4.1.3": ["4.1.2"],
          "4.2": ["4.1.1"], "4.3.1": ["4.2"], "4.3.2": ["4.1.3", "4.3.1"], "6.4": ["6.3"], "6.5.2": ["6.4"], "6.5.3": ["6.4"],
          "7.3": ["7.1", "7.2"], "8.2": ["8.1"], "8.3": ["8.1"], "9.2.2": ["9.2.1"], "10.1.2(b)": ["10.1.1", "10.1.2(a)"],
          "10.2.2": ["10.2.1"], "10.2.3": ["10.2.1"], "10.2.4": ["10.2.3"], "10.2.5": ["10.2.4"]},
         "Questions 1 to 10 (the whole paper)")
