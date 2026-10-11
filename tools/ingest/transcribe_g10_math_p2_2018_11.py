"""Grade 10 Mathematics P2 Nov 2018 (DBE common paper), the whole paper (Questions 1 to 8, 100 marks: statistics, analytical geometry,
trigonometry, measurement, Euclidean geometry), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`
like any ingested paper. Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and
figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not). The question paper, the memo
and the answer book are all SCANS (no text layer): everything was read from their page images rendered at 150 dpi, with crops at
200-250 dpi where a subscript, a label or a stem mattered (5.2's g(x) = a.cos bθ, the angle numbers of the Question 7 and 8
diagrams, the answer book's grid and number line).

  python tools/ingest/transcribe_g10_math_p2_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Mathematics P2 Nov 2018 Eng.pdf" "uploads/Grade 10 Mathematics P2 Nov 2018 MG Afr & Eng.pdf" --id g10-math-p2-2018-11 --from-json --answer-book "uploads/Grade 10 Mathematics P2 Nov 2018 Answer Book Afr & Eng.pdf"

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p2_2025_11.py, and the Grade 10 pilot
transcribe_g10_math_p1_2018_11.py):
  every part the memo WORKS OUT in two or more lines (a range, a mean, a median, a distance, a gradient, a midpoint, an area, an
  angle with its reason, a trigonometric value or equation, a volume) and every geometry proof -> authored whole-working multiple
  choice, `work`: the memo's FIRST method line by line (a geometry statement with its [reason] at the line's end, "{a}/{b}" a
  stacked fraction) and three workings each built from a DIFFERENT real error (a wrong ratio, formula or theorem, a sign slip, a
  misread value, the wrong side or pair of lines, a wrong reason, circular reasoning, the calculator in radians), every option of a
  part the same layout (`shape`), the right one's place spread over A-D across the paper; the part keeps its marks, all or nothing.
  The memo's OR methods and values are other right routes and never a wrong option.
  An answer the memo states with no working (the frequency column, a ratio, a trigonometric ratio, an equation of a graph, a and b,
  an interval, a range, a one-line reason) -> authored multiple choice of answers: the memo's and three common errors.
  One read-off number with no working (1.2, 4.2.1, 5.1.2(a)) stays num; the box and whisker diagram 1.5 and the sketch 5.1.1 ->
  draw (self-checked against the memo's criteria); 7.1 (complete a theorem) -> statements, pick 1.
  Where a part's options, cards or criteria show an EARLIER part's answer it carries "after" (the GATES assert below).
Missions: Questions 1, 2 and 6 share one stem and diagram each, so each is one mission; Questions 3, 4, 5 and 8 change their stem
part-way, so their numbered groups are missions (3.1, 3.2, 3.3 ...). Question 7 is ONE mission (7.1 and 7.2): 7.2.2's working names
the theorem 7.1 completes (AP = PS [line from midpoint ∥ to one side of △]), so it opens after 7.1, and a gate only works inside
its mission; 7.2's own stem rides in 7.2.1's and 7.2.2's question text.
No figure comes from the answer book: its table (1.1), number line (1.5) and grid (5.1.1) are blank answer spaces (the MCQ, the draw
memo and criteria carry them), and its other diagrams repeat the question paper's.
Figure boxes are measured in PDF points (page 595 x 841, read from the PDF) from the ink on the scan (scratch tool
lower/g10-math-p2-2018-11/figs.py) and checked on a contact sheet with ingest's 1% pad applied."""
import json
import random
import re
from pathlib import Path

PID = "g10-math-p2-2018-11"
W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q1": [3, 71.2, 154.8, 521.0, 503.3],      # the line graph in its frame
    "Q2": [4, 82.2, 202.7, 510.8, 458.5],      # the axes, △PQR, T, S, V
    "Q3.1": [5, 196.0, 162.0, 376.0, 328.6],   # △QPR
    "Q3.2": [5, 196.7, 452.0, 381.0, 630.3],   # OS and θ; y0 452 (ink from 450.8): the pad then stops below "x-axis." (ink to 443.4)
    "Q4.1": [6, 185.1, 175.1, 414.5, 328.7],   # ABC, ACD, ADE
    "Q5.2": [7, 106.0, 110.6, 486.2, 304.5],   # the graph of g
    "Q6": [7, 225.1, 539.1, 360.4, 703.3],     # the cup
    "Q7": [8, 137.5, 300.6, 462.0, 506.0],     # △ACS and parallelogram PSRQ
    "Q8.1": [9, 179.1, 155.8, 404.7, 379.4],   # parallelogram ABCD with J and K
    "Q8.2": [9, 201.7, 503.6, 424.0, 680.3]}   # the circle, P and T


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="", **kw: {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                           "criteria": [{"text": t, "marks": m} for t, m in criteria],
                                                           **({"memo": memo} if memo else {}), **kw}

ANSWER = "\n\nChoose the correct answer."
WORK = "\n\nChoose the correct working."
AUTHORED = []   # the whole-working multiple choice, in paper order
DP1 = 0.06      # a value keyed at one decimal place: 63,5 accepted, 63,4 and 63,6 not


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
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


def stmt(n, q, marks, right, wrong, clues, each, **kw):
    """A written answer as statements: the memo's points (right) and clearly false cards (wrong), shuffled with a fixed seed."""
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random(PID + ":" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    pool = sorted(k for k, i in enumerate(order) if i < len(right))
    assert pool != list(range(len(pool))), (n, "the right card(s) on top: an answer by position")
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count, **kw}


# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
FX = "{(1 × 3) + (2 × 4) + (3 × 5) + (4 × 3) + (5 × 6) + (7 × 7) + (8 × 9) + (9 × 5)}"
q1 = [
    mcq("1.1", "Complete the frequency column in the table provided in the ANSWER BOOK.\n\nEach option gives the frequencies of the marks 0 ; 1 ; "
        "2 ; … ; 10, in that order." + ANSWER, [
            "0 ; 3 ; 7 ; 12 ; 15 ; 21 ; 21 ; 28 ; 37 ; 42 ; 42",    # cumulative frequencies
            "3 ; 4 ; 5 ; 3 ; 6 ; 0 ; 7 ; 9 ; 5 ; 0 ; 0",            # each read one mark too early
            "0 ; 3 ; 4 ; 5 ; 3 ; 6 ; 0 ; 7 ; 9 ; 5 ; 0",            # the memo
            "0 ; 3 ; 8 ; 15 ; 12 ; 30 ; 0 ; 49 ; 72 ; 45 ; 0"], 2,  # mark × frequency
        ["Which mark does each point on the graph stand above?", "How do you read a point's frequency off the vertical axis?"], marks=2),
    num("1.2", "How many learners wrote the test?", 42, 0, "learners",
        ["What does each frequency count?", "How do the frequencies of all the marks together give the class?"]),
    work("1.3.1", "Calculate the range for the data.", 2, [
        "Range = 10 − 0\n= 10",     # the ends of the axis
        "Range = 9 − 1\n= 8",       # the memo
        "Range = 9 − 0\n= 9",       # the mark 0 counted, though no learner got it
        "Range = 9 − 3\n= 6"], 1,   # the highest and lowest non-zero frequencies
        ["Which is the highest mark a learner got, and which is the lowest?", "Does a mark with a frequency of 0 belong to the data?"]),
    work("1.3.2", "Calculate the mean for the test.", 3, [
        "x̄ = " + FX + "/{11}\n= {234}/{11}\n= 21,27",                                        # divided by the number of marks
        "x̄ = {0 + 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10}/{11}\n= {55}/{11}\n= 5",               # the marks without their frequencies
        "x̄ = {0 + 3 + 4 + 5 + 3 + 6 + 0 + 7 + 9 + 5 + 0}/{11}\n= {42}/{11}\n= 3,82",              # the mean of the frequencies
        "x̄ = " + FX + "/{42}\n= {234}/{42}\n= 5,57"], 3,                                     # the memo
        ["How many learners got each mark, and what is the total of all their marks?", "What do you divide that total by?"],
        after=["1.1", "1.2"]),
    work("1.4", "Determine the median for the data.", 3, [
        "Position of the median = {n + 1}/{2} = 21,5th\nQ₂ = {5 + 7}/{2}\n= 6",                  # the memo
        "Position of the median = {n + 1}/{2} = 21,5th\nQ₂ = {5 + 6}/{2}\n= 5,5",                # the mark 6 taken, though no learner got 6
        "Position of the median = {n}/{2} = 21st\nQ₂ = the 21st mark\n= 5",                      # n/2: the 22nd mark left out
        "Position of the median = {11 + 1}/{2} = 6th\nQ₂ = the 6th frequency from the smallest\n= 4"], 0,   # the frequencies' median
        ["How many marks are there altogether, and which position lies in the middle?", "Which mark sits at each middle position when you "
                                                                                        "count the learners mark by mark?"], after=["1.2"]),
    draw("1.5", "Draw a box and whisker diagram for the data.", 3, [
        ["Q₁ = 3: the left end of the box", 1], ["Q₃ = 8: the right end of the box", 1],
        ["The rest of the box: the median 6 inside it, and the whiskers out to the minimum 1 and the maximum 9", 1]],
        ["Which five numbers does a box and whisker diagram need?", "Where are the quartiles: the middle of the lower half and of the upper "
                                                                    "half of the data?"],
        memo="The answer book gives a number line from 0 to 10. Five-number summary: 1 ; 3 ; 6 ; 8 ; 9.", after=["1.3.1", "1.4"]),
]

# ---- QUESTION 2, the question paper page 4 and the memo pages 3-5 ----
QT = "QR = QP = √34\nQT = {1}/{2}PQ = {1}/{2}√34\nArea of △QTR = {1}/{2}(QR)(QT)\n"
MID = "m(T to the midpoint of PR) = "
q2 = [
    work("2.1.1", "Determine the length of PQ. Leave your answer in surd form.", 2, [
        "PQ = √((1 + 6)² + (0 + 3)²)\n= √(49 + 9)\n= √58",       # a sign slip: adds Q's coordinates
        "PQ = √((1 − 0)² + (6 − 3)²)\n= √(1 + 9)\n= √10",        # pairs each point's x with its own y
        "PQ = √((1 − 6)² + (0 − 3)²)\n= √(25 + 9)\n= √34",       # the memo
        "PQ = √((1 − 6)² + (0 − 3)²)\n= √25 + √9\n= 8"], 2,      # the root shared out over the sum
        ["Which formula gives the distance between two points?", "Do you subtract the x-values from each other and the y-values from each "
                                                                  "other?"]),
    work("2.1.2", "Determine the gradient of PQ.", 2, [
        "m(PQ) = {3 − 0}/{6 − 1}\n= {3}/{5}",      # the memo
        "m(PQ) = {6 − 1}/{3 − 0}\n= {5}/{3}",      # x over y
        "m(PQ) = {3 − 0}/{1 − 6}\n= −{3}/{5}",     # Q − P on top, P − Q below
        "m(PQ) = {3}/{6}\n= {1}/{2}"], 0,          # Q's y over its x, as if PQ passed through O
        ["Which formula gives the gradient between two points?", "Are the two points taken in the same order on top and below?"]),
    work("2.1.3", "Determine the coordinates of T.", 2, [
        "x-value: {6 − 1}/{2} = {5}/{2}\ny-value: {3 − 0}/{2} = {3}/{2}\nT({5}/{2} ; {3}/{2})",   # subtracts
        "x-value: 1 + 6 = 7\ny-value: 0 + 3 = 3\nT(7 ; 3)",                                       # never halved
        "x-value: {1 + 6}/{2} = {7}/{2}\ny-value: {0 + 3}/{2} = {3}/{2}\nT({3}/{2} ; {7}/{2})",   # the coordinates swapped
        "x-value: {1 + 6}/{2} = {7}/{2}\ny-value: {0 + 3}/{2} = {3}/{2}\nT({7}/{2} ; {3}/{2})"], 3,   # the memo
        ["T is the midpoint of PQ: which formula gives a midpoint?", "Do you add or subtract the two x-values, and what do you then divide by?"]),
    work("2.2.1", "Calculate the area of △QTR.", 3, [
        "QR = QP = √34\nQT = {1}/{2}PQ = {1}/{2}√34\nArea of △QTR = {1}/{2}(QR)(QP)\n= {1}/{2}(√34)(√34)\n= 17 square units",   # △PQR's area
        QT + "= {1}/{2}(√34)({1}/{2}√34)\n= {17}/{2} = 8,5 square units",                                                       # the memo
        "QR = QP = √34\nQT = {1}/{2}PQ = √17\nArea of △QTR = {1}/{2}(QR)(QT)\n= {1}/{2}(√34)(√17)\n= 12,02 square units",       # ½√34 as √17
        QT + "= {1}/{4}(√34)(√34) = {1}/{4}√68\n= 2,06 square units"], 1,                                                       # √34 × √34 as √68
        ["△QTR has a right angle at Q: which two of its sides are the base and the height?", "T is the midpoint of PQ: how long is QT "
                                                                                             "compared with PQ?"], after=["2.1.1"]),
    work("2.2.2", "Calculate the size of θ, with reasons.", 2, [
        "θ = 180° − 121° [∠s on a str line]\nθ = 59°",       # that is QŜP, not θ
        "θ = {1}/{2}(121°) [ext ∠ of △]\nθ = 60,5°",        # the exterior angle split equally between the two angles
        "θ = 121° − 90° [ext ∠ of △]\nθ = 31°",             # the memo (OR QŜP = 59° [∠s on a str line], θ = 31° [sum of ∠s in △])
        "θ = 121° − 90° [corresp ∠s]\nθ = 31°"], 2,         # the wrong reason
        ["QŜV lies outside △PQS: how is an exterior angle of a triangle related to the angles inside it?", "What size is the angle of △PQS "
                                                                                                             "at Q?"]),
    work("2.2.3", "Calculate the coordinates of S.", 3, [
        "cos θ = {PQ}/{PS}\ncos 31° = {√34}/{PS}\nPS = {√34}/{cos 31°} = 6,80\nS(6,8 + 1 ; 0)\nS(7,8 ; 0)",       # the memo (OR sin QŜP; OR QR's equation)
        "sin θ = {PQ}/{PS}\nsin 31° = {√34}/{PS}\nPS = {√34}/{sin 31°} = 11,32\nS(11,32 + 1 ; 0)\nS(12,32 ; 0)",  # sine for cosine
        "cos θ = {PQ}/{PS}\ncos 31° = {√34}/{PS}\nPS = {√34}/{cos 31°} = 6,80\nOS = PS = 6,8\nS(6,8 ; 0)",        # PS measured from O, not P
        "cos θ = {PS}/{PQ}\ncos 31° = {PS}/{√34}\nPS = √34 cos 31° = 5,00\nS(5 + 1 ; 0)\nS(6 ; 0)"], 0,           # the ratio upside down
        ["In right-angled △PQS, which side is the hypotenuse, and which side is next to θ?", "PS is a distance along the x-axis from P: where "
                                                                                             "does P lie?"], after=["2.1.1", "2.2.2"]),
    work("2.3", "Determine, with reasons, the gradient of the line through T and the midpoint of PR.", 3, [
        "m(QR) = {3 − 2}/{6 − 9}\n= −{1}/{3}\n" + MID + "m(QR) [midpoint theorem]\n= −{1}/{3}",                     # −(−2) taken as −2
        "m(QR) = {6 − 9}/{3 − (−2)}\n= −{3}/{5}\n" + MID + "m(QR) [midpoint theorem]\n= −{3}/{5}",                  # x over y
        "m(QR) = {3 − (−2)}/{6 − 9}\n= −{5}/{3}\n" + MID + "{1}/{2}m(QR) [midpoint theorem]\n= −{5}/{6}",           # the gradient halved
        "m(QR) = {3 − (−2)}/{6 − 9}\n= −{5}/{3}\n" + MID + "m(QR) [midpoint theorem]\n= −{5}/{3}"], 3,              # the memo (OR the midpoint (5 ; −1))
        ["The line joins the midpoints of two sides of △PQR: which side is it parallel to?", "How do the gradients of parallel lines compare?"]),
]

# ---- QUESTION 3, the question paper page 5 and the memo pages 5-6 ----
SEC = "sec θ + sin² θ = "
q31 = [
    mcq("3.1.1", "Use the sketch to determine the ratio of tan(90° − R)." + ANSWER, ["PR/QP", "QP/PR", "PR/QR", "QP/QR"], 0,
        ["In △QPR, which angle is 90° − R?", "For that angle, which side is opposite and which is adjacent?"]),
    mcq("3.1.2", "Write down the trigonometric ratio that is equal to QR/QP." + ANSWER, ["cos Q", "cosec Q", "tan Q", "sec Q"], 3,
        ["Which side of △QPR is the hypotenuse?", "Is QR/QP one of sin, cos and tan, or the reciprocal of one of them?"]),
]
q32 = [
    work("3.2.1", "The length of OS", 2, [
        "OS = √((−3)² + (−4)²) [Pythagoras]\n= √9 + √16 = 7",     # the root shared out over the sum
        "OS = √((−3)² + (−4)²) [Pythagoras]\n= √(9 + 16) = 5",    # the memo
        "OS = √((−4)² − (−3)²) [Pythagoras]\n= √(16 − 9) = √7",   # subtracts, as if OS were a shorter side
        "OS = (−3)² + (−4)² [Pythagoras]\n= 9 + 16 = 25"], 1,     # the root forgotten
        ["OS is the hypotenuse of a right-angled triangle: what are its other two sides?", "What does Pythagoras' theorem say about the three "
                                                                                           "sides?"]),
    work("3.2.2", "The value of sec θ + sin² θ", 3, [
        SEC + "−{5}/{3} + (−{4}/{5})²\n= −{5}/{3} + {16}/{25}\n= −{77}/{75}",     # the memo
        SEC + "−{5}/{4} + (−{4}/{5})²\n= −{5}/{4} + {16}/{25}\n= −{61}/{100}",    # sec θ as r/y
        SEC + "−{5}/{3} + (−{3}/{5})²\n= −{5}/{3} + {9}/{25}\n= −{98}/{75}",      # sin θ as x/r
        SEC + "−{5}/{3} − ({4}/{5})²\n= −{5}/{3} − {16}/{25}\n= −{173}/{75}"], 0,  # the square of a negative kept negative
        ["Which of x, y and r do you need for sec θ, and which for sin θ?", "What sign does the square of a negative number have?"],
        after=["3.2.1"]),
]
q33 = [
    work("3.3", "Determine the value of the following WITHOUT using a calculator:\ncosec 45°/(sin 90°.tan 60°)", 4, [
        "= {sin 45°}/{(1)(√3)}\n= {√2}/{2} ÷ √3\n= {√2}/{2} × {1}/{√3}\n= {√2}/{2√3}",                     # cosec read as sin
        "= {1 ÷ sin 45°}/{(1)(1 ÷ √3)}\n= {2}/{√2} ÷ {1}/{√3}\n= {2}/{√2} × √3\n= {2√3}/{√2}",              # tan 60° as 1/√3
        "= {1 ÷ sin 45°}/{(1)(√3)}\n= {2}/{√2} ÷ √3\n= {2}/{√2} × {1}/{√3}\n= {2}/{√6}",                    # the memo (OR √2/√3; √6/3)
        "= {1 ÷ sin 45°}/{(1)(√3)}\n= 2 ÷ √3\n= 2 × {1}/{√3}\n= {2}/{√3}"], 2,                             # sin 45° as ½
        ["Which ratio is cosec the reciprocal of?", "What are the exact values of sin 45°, sin 90° and tan 60° in the special triangles?"]),
]

# ---- QUESTION 4, the question paper page 6 and the memo pages 7-8 ----
DAE = "DÂE = 90° − (30° + CÂD)\nDÂE = 90° − (30° + 48,19°) = 11,81°\n"
COS = "5 cos x = 2\ncos x = {2}/{5}\n"
q41 = [
    work("4.1.1", "Calculate the length of AC.", 2, [
        "cos 30° = {20}/{AC}\nAC = {20}/{cos 30°}\nAC = 23,09 units",     # cosine for sine
        "tan 30° = {20}/{AC}\nAC = {20}/{tan 30°}\nAC = 34,64 units",     # tangent: AC is the hypotenuse
        "sin 30° = {AC}/{20}\nAC = 20 sin 30°\nAC = 10 units",            # the ratio upside down
        "sin 30° = {20}/{AC}\nAC = {20}/{sin 30°}\nAC = 40 units"], 3,    # the memo (OR cosec 30°, cos 60°, sec 60°)
        ["In △ABC, which side is opposite the 30° angle, and which is the hypotenuse?", "Which ratio links those two sides?"]),
    work("4.1.2", "Calculate the size of CÂD.", 2, [
        "sin CÂD = {AC}/{60}\nsin CÂD = {40}/{60}\nCÂD = 41,81°",      # sine: AC lies next to the angle
        "cos CÂD = {AC}/{60}\ncos CÂD = {40}/{60}\nCÂD = 48,19°",      # the memo
        "tan CÂD = {AC}/{60}\ntan CÂD = {40}/{60}\nCÂD = 33,69°",      # tangent: 60 is the hypotenuse
        "cos CÂD = {BC}/{60}\ncos CÂD = {20}/{60}\nCÂD = 70,53°"], 1,  # BC for AC
        ["In △ACD, where is the right angle, and which side is the hypotenuse?", "Which ratio links the side next to CÂD with the hypotenuse?"],
        after=["4.1.1"]),
    work("4.1.3", "Calculate the length of DE.", 3, [
        DAE + "tan 11,81° = {DE}/{60}\nDE = 60 tan 11,81° = 12,55 units",                                         # the memo
        DAE + "sin 11,81° = {DE}/{60}\nDE = 60 sin 11,81° = 12,28 units",                                         # sine: AE is the hypotenuse
        "DÂE = 90° − CÂD\nDÂE = 90° − 48,19° = 41,81°\ntan 41,81° = {DE}/{60}\nDE = 60 tan 41,81° = 53,67 units",  # the 30° left out
        DAE + "tan 11,81° = {60}/{DE}\nDE = {60}/{tan 11,81°} = 286,95 units"], 0,                                # the ratio upside down
        ["The angles at A between AB and AE make 90°: which part of it is DÂE?", "In △ADE, which side is opposite DÂE and which is next to it?"],
        after=["4.1.2"]),
]
q42 = [
    num("4.2.1", "tan x = 2,01", 63.5, DP1, "°", ["Which calculator key undoes tan?", "Is your calculator in degree mode, and how do you round "
                                                                                     "to one decimal place?"], marks=2),
    work("4.2.2", "5 cos x + 2 = 4", 3, [
        "7 cos x = 4\ncos x = {4}/{7}\nx = cos⁻¹({4}/{7}) = 55,1500…°\nx = 55,2°",   # 5 cos x + 2 added up as 7 cos x
        COS + "x = sin⁻¹(0,4) = 23,5781…°\nx = 23,6°",                              # the wrong inverse key
        COS + "x = cos⁻¹(0,4) = 66,4218…°\nx = 66,4°",                              # the memo
        COS + "x = cos⁻¹(0,4) = 1,1592…°\nx = 1,2°"], 2,                            # the calculator in radians
        ["Can you get cos x on its own before you use the calculator?", "Which key undoes cos, and is the calculator in degree mode?"]),
    work("4.2.3", "(cosec x)/2 = 3", 3, [
        "cosec x = {3}/{2}\n{1}/{sin x} = {3}/{2}\nsin x = {2}/{3}\nx = 41,8°",   # divided by 2 instead of multiplying
        "cosec x = 6\n{1}/{sin x} = 6\nsin x = {1}/{6}\nx = 9,6°",                # the memo
        "cosec x = 5\n{1}/{sin x} = 5\nsin x = {1}/{5}\nx = 11,5°",               # the 2 moved across as if it were added
        "cosec x = 6\n{1}/{cos x} = 6\ncos x = {1}/{6}\nx = 80,4°"], 1,           # cosec taken as 1/cos
        ["How do you get cosec x on its own?", "cosec is the reciprocal of which ratio?"]),
]

# ---- QUESTION 5, the question paper pages 6-7 and the memo page 9 ----
q51 = [
    draw("5.1.1", "Sketch, on the grid provided in the ANSWER BOOK, the graph of f for 0° ≤ x ≤ 360°. Clearly show ALL the intercepts and "
         "asymptotes.", 3, [
             ["A tan graph passing through (45° ; −3) or (135° ; 3) or (225° ; −3) or (315° ; 3)", 1],
             ["x-intercepts at 0°, 180° and 360°", 1], ["Both asymptotes: x = 90° and x = 270°", 1]],
         ["Where is tan x undefined between 0° and 360°?", "What does the −3 do to the graph of y = tan x?"],
         memo="The answer book gives a grid: x from 0° to 360° across (labelled at 90, 180, 270 and 360, a line every 15°) and y from −4 to 4 "
              "up. The memo's graph: f falls from (0° ; 0) through (45° ; −3) towards the asymptote x = 90°, comes down from the top through "
              "(135° ; 3), (180° ; 0) and (225° ; −3) towards the asymptote x = 270°, then comes down from the top through (315° ; 3) to "
              "(360° ; 0)."),
    num("5.1.2(a)", "Hence, or otherwise, write down the period of f.", 180, 0, "°",
        ["After how many degrees does the graph of f start to repeat?", "Does multiplying tan x by −3 change how often it repeats?"]),
    mcq("5.1.2(b)", "Hence, or otherwise, write down the equation of h if h is the reflection of f about the x-axis." + ANSWER,
        ["h(x) = 3 tan(−x)", "h(x) = 3 tan x", "h(x) = (1/3) tan x", "h(x) = −3 tan x"], 1,
        ["When a graph is reflected about the x-axis, what happens to every y-value?", "Which part of f(x) = −3 tan x controls the sign of the "
                                                                                       "y-values?"]),
]
q52 = [
    mcq("5.2.1", "Write down the values of a and b." + ANSWER, ["a = 2 and b = 1", "a = −2 and b = 2", "a = −2 and b = 1", "a = 1 and b = −2"], 2,
        ["What is the y-value of g at x = 0°, and what is cos 0°?", "After how many degrees does g complete one full wave?"], marks=2),
    mcq("5.2.2", "Use the graph to determine the value(s) of x for which g(x) > 0." + ANSWER,
        ["90° ≤ x ≤ 270°", "0° ≤ x < 90° or 270° < x ≤ 360°", "0° < x < 180°", "90° < x < 270°"], 3,
        ["Where is the graph of g above the x-axis?", "Is g(x) > 0 at the x-intercepts themselves?"]),
    mcq("5.2.3", "Determine the range of h if h is the image of g if g is shifted down TWO units." + ANSWER,
        ["−4 ≤ y ≤ 0", "0 ≤ y ≤ 4", "−4 < y < 0", "−2 ≤ y ≤ 2"], 0,
        ["What is the range of g: its lowest and highest y-values?", "What happens to every y-value when a graph moves down two units?"], marks=2),
    work("5.2.4", "Determine, using the graph, the value of:\n−2(cos 0° + cos 1° + cos 2° + … + cos 358° + cos 359° + cos 360°)", 2, [
        "= −2(0)\n= 0",       # every value taken to cancel
        "= −2(2)\n= −4",      # cos 0° and cos 360° counted, all the rest cancelling
        "= −2(−1)\n= 2",      # cos 0° and cos 360° left out
        "= −2(1)\n= −2"], 3,  # the memo
        ["−2 cos x is g(x): on the graph, which values of g cancel each other out in pairs?", "Which value is left over once the pairs cancel?"]),
]

# ---- QUESTION 6, the question paper page 7 and the memo page 9 ----
q6 = [
    work("6.1", "Calculate the height of the cup.", 3, [
        "r = 3 cm\nV = πr²h\n117π = π(3)²h\nh = 13 cm",        # the memo
        "r = 6 cm\nV = πr²h\n117π = π(6)²h\nh = 3,25 cm",      # the diameter as the radius
        "r = 30 mm\nV = πr²h\n117π = π(30)²h\nh = 0,13 cm",    # millimetres mixed with cm³
        "r = 3 cm\nV = 2πrh\n117π = 2π(3)h\nh = 19,5 cm"], 0,  # the curved surface's formula
        ["The diameter is in mm and the volume in cm³: what is the radius in cm?", "Which formula gives the volume of a cylinder?"]),
    work("6.2", "Calculate the total surface area of the water that touches the cup if the cup is 80% full with water.", 4, [
        "TSA = 2πr² + 2πrh\n= 2π(3)² + 2π(3)(13) × 0,8\n= 252,58 cm²",      # a closed cylinder: the water's surface counted
        "TSA = πr² + 2πrh\n= (π(3)² + 2π(3)(13)) × 0,8\n= 218,65 cm²",      # 80% of the base as well
        "TSA = πr² + 2πrh\n= π(3)² + 2π(3)(13) × 0,8\n= 224,31 cm²",        # the memo (OR the height 10,4)
        "TSA = πr² + 2πrh\n= π(3)² + 2π(3)(13)\n= 273,32 cm²"], 2,          # the full height
        ["Which surfaces of the cup does the water touch?", "If the cup is 80% full, how high up the side does the water reach?"], after=["6.1"]),
]

# ---- QUESTION 7, the question paper page 8 and the memo page 10 ----
STEM72 = ("ACS is a triangle. P is a point on AS and R is a point on AC such that PSRQ is a parallelogram. PQ intersects AC at B such that B is "
          "the midpoint of AR. QC is joined. Also, CR = PS, Ĉ₁ = 50° and BP = 60 mm.\n\n")
ISO = "CR = PS [given]\nPS = QR [opp sides of ∥m equal]\nCR = QR\nQ̂₁ = Ĉ₁ = 50° [∠s opp equal sides]\n"
MIDP = "AP = PS [line from midpoint ∥ to one side of △]\n"
q7 = [
    # pick 1: the memo's completion; the wrong cards are false for every triangle (the line is HALF the second side and parallel to it)
    stmt("7.1", "Complete the statement so that it is TRUE:\n\nThe line drawn from the midpoint of the one side of a triangle, parallel to the "
         "second side, …", 1, ["Bisects the third side"],
         ["Is perpendicular to the third side", "Is equal in length to the second side", "Bisects the second side",
          "Is equal in length to the third side"],
         ["Draw a triangle, mark the midpoint of one side and draw a line from there parallel to a second side: where does it meet the third "
          "side?", "Measure the two pieces of the third side in your drawing: what do you notice?"], 1),
    work("7.2.1", STEM72 + "Calculate the size of Â.", 5, [
        ISO + "R̂₃ = 180° − 50° − 50° = 80° [sum of ∠s in △]\nÂ = 80° [alt ∠s; QR ∥ AS]",     # the angle inside △QRC at R taken as R̂₃
        ISO + "R̂₃ = 50° + 50° = 100° [ext ∠ of △]\nÂ = 100° [alt ∠s; QR ∥ AS]",             # the memo
        ISO + "R̂₃ = 50° + 50° = 100° [ext ∠ of △]\nÂ = 100° [corresp ∠s; QR ∥ AS]",         # the wrong reason: alternate, not corresponding
        ISO + "R̂₃ = 180° − 50° = 130° [ext ∠ of △]\nÂ = 130° [alt ∠s; QR ∥ AS]"], 1,        # the exterior angle as 180° minus Ĉ₁
        ["CR = PS and PSRQ is a parallelogram: what kind of triangle is △QRC?", "R̂₃ lies outside △QRC: how is it related to the angles inside, "
                                                                                "and how do the parallel lines QR and AS carry it to A?"]),
    work("7.2.2", STEM72 + "Determine the length of QP.", 3, [
        MIDP + "RS = {1}/{2}BP = 30 mm [midpoint theorem]\nQP = RS = 30 mm [opp sides of ∥m equal]",                          # halved, not doubled
        "AP = PS [midpoint theorem]\nRS = 2BP = 120 mm [line from midpoint ∥ to one side of △]\nQP = RS = 120 mm [opp sides of ∥m equal]",   # the reasons swapped
        MIDP + "RS = BP = 60 mm [opp sides of ∥m equal]\nQP = RS = 60 mm [opp sides of ∥m equal]",                             # BPSR taken as a ∥m
        MIDP + "RS = 2BP = 120 mm [midpoint theorem]\nQP = RS = 120 mm [opp sides of ∥m equal]"], 3,                          # the memo (OR △QBR ≡ △PBA)
        ["In △ARS, B is the midpoint of AR and BP ∥ RS: what do you know about P?", "How long is BP compared with RS, and which side of the "
                                                                                    "parallelogram equals RS?"], after=["7.1"]),
]

# ---- QUESTION 8, the question paper page 9 and the memo pages 11-13 ----
EBDF = "AB = DC, so AE + EB = DF + FC [opp sides of ∥m equal]\nAE = CF [given]\n∴ EB = DF\n"
KITE = "AP = BP [given]\nOA = OB [radii]\n"
q81 = [
    work("8.1.1", "DJ ∥ BK", 5, [
        EBDF + "AD ∥ BC [opp sides of ∥m parallel]\nEDFB is a parallelogram [one pair opp sides equal and ∥]\n∴ ED ∥ FB, so DJ ∥ BK",   # the parallel pair is not EB, DF
        EBDF + "DE = BF [opp sides of ∥m equal]\nEDFB is a parallelogram [both pairs opp sides equal]\n∴ ED ∥ FB, so DJ ∥ BK",          # assumes EDFB is a ∥m
        EBDF + "DF ∥ EB [opp sides of ∥m parallel]\nEDFB is a parallelogram [one pair opp sides equal and ∥]\n∴ ED ∥ FB, so DJ ∥ BK",   # the memo (OR △AED ≡ △CFB)
        EBDF + "DF ∥ EB [opp sides of ∥m parallel]\nEDFB is a parallelogram [diagonals bisect each other]\n∴ ED ∥ FB, so DJ ∥ BK"], 2,  # the wrong test
        ["AE = CF and AB = DC: what can you say about EB and DF?", "Which test for a parallelogram needs only ONE pair of opposite sides?"]),
    work("8.1.2", "Ê₁ = F̂₁", 4, [
        "Ê₁ = D̂₁ [corresp ∠s; AB ∥ DC]\nF̂₁ = D̂₁ [alt ∠s; DE ∥ FB]\n∴ Ê₁ = F̂₁",    # the memo (OR through Ê₃ or F̂₃; OR Ê₂ = F̂₂ in EDFB)
        "Ê₁ = D̂₁ [alt ∠s; AB ∥ DC]\nF̂₁ = D̂₁ [corresp ∠s; DE ∥ FB]\n∴ Ê₁ = F̂₁",    # the two reasons swapped
        "Ê₁ = D̂₁ [corresp ∠s; AD ∥ BC]\nF̂₁ = D̂₁ [alt ∠s; DE ∥ FB]\n∴ Ê₁ = F̂₁",    # the wrong pair of parallel lines
        "Ê₁ = D̂₁ [corresp ∠s; AB ∥ DC]\nF̂₁ = D̂₂ [alt ∠s; DE ∥ FB]\n∴ Ê₁ = F̂₁"], 0,  # D̂₂ is not alternate to F̂₁
        ["Which angle at D matches Ê₁ along the line DJ?", "Which angle at D matches F̂₁ across DC, now that DE ∥ FB?"]),
]
q82 = [
    work("8.2.1", "AT = BT", 5, [
        KITE + "OAPB is a rhombus [two pairs adj sides equal]\nAT = TB [diagonals of a rhombus bisect each other]",   # a rhombus needs four equal sides
        KITE + "OAPB is a kite [two pairs adj sides equal]\nAT = TB [one diagonal of a kite bisects the other]",      # the memo (OR △OAP ≡ △OBP, then △OAT ≡ △OBT)
        KITE + "OAPB is a kite [both pairs opp sides equal]\nAT = TB [one diagonal of a kite bisects the other]",     # the equal sides are adjacent, not opposite
        KITE + "OAPB is a kite [two pairs adj sides equal]\nAT = TB [diagonals of a kite are ⊥]"], 1,                # perpendicular is not bisected
        ["Which two pairs of sides of OAPB are equal, and why?", "What do you know about the diagonals of that quadrilateral?"]),
    # the memo's one line, a statement and its reason: a choice of reasons (its OR, △OTA ≡ △OTB with ∠s on a str line, takes two lines)
    mcq("8.2.2", "OT̂A = 90°" + ANSWER, ["OT̂A = 90° [sum of ∠s in △]", "OT̂A = 90° [properties of a kite: diagonals ⊥]", "OT̂A = 90° [vert opp ∠s equal]",
                                         "OT̂A = 90° [diagonals of a ∥m bisect each other]"], 1,
        ["What did you prove OAPB to be in 8.2.1?", "OT̂A is an angle between which two lines of that figure?"], after=["8.2.1"]),
]

REASONS = "Give reasons for ALL geometry statements in QUESTIONS 7 and 8."
missions = [
    {"id": "1", "title": "Question 1", "kind": "Data from a line graph", "marks": 14,
     "lead": "The line graph below shows test marks out of 10 obtained by a Grade 10 class.",
     # (no readings: 1.1 asks for them)
     "figure": fig("Q1", "A line graph of test results: Frequency (0 to 10) up the side and Marks (0 to 10) along the bottom, on a square grid. A "
                   "point is plotted above each mark from 0 to 10, and the points are joined by straight lines."), "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Analytical geometry", "marks": 17,
     "lead": "In the diagram below, P(1 ; 0), Q(6 ; 3) and R(9 ; −2) are the vertices of a triangle such that PQ = QR and PQ ⊥ QR. T is a point on "
             "PQ such that T is the midpoint of PQ. S is the point of intersection of RQ and the x-axis. V is a point on the x-axis such that "
             "QŜV = 121°.\nQP̂S = θ",
     "figure": fig("Q2", "Axes with origin O. P(1 ; 0) lies on the x-axis to the right of O; Q(6 ; 3) is above the x-axis to the upper right, with "
                   "a right angle marked at Q; R(9 ; −2) is below the x-axis to the lower right. Triangle PQR is drawn, with T on PQ and the line "
                   "TR. QR crosses the x-axis at S; V is on the x-axis to the right of S, and the angle QŜV is marked 121°. The angle θ is marked "
                   "at P, between the x-axis and PQ."), "items": q2},
    {"id": "3.1", "title": "Question 3.1", "kind": "Trigonometric ratios", "marks": 2,
     "lead": "In the diagram below, △QPR is a right-angled triangle with QP̂R = 90°.",
     "figure": fig("Q3.1", "Right-angled triangle QPR: QP is horizontal at the top, Q on the left and P on the right; R is directly below P, so PR "
                   "is vertical; the right angle is marked at P, and QR is the sloping side."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Ratios on the Cartesian plane", "marks": 5,
     "lead": "S(−3 ; −4) is a point on the Cartesian plane such that OS makes an angle of θ with the positive x-axis.\n\nCalculate the following "
             "WITHOUT using a calculator:",
     "figure": fig("Q3.2", "Axes with origin O. A line runs from O down to the left to S(−3 ; −4). The angle θ is marked by an arc that turns "
                   "anticlockwise from the positive x-axis round to OS."), "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Special angles", "marks": 4, "items": q33},
    {"id": "4.1", "title": "Question 4.1", "kind": "Right-angled triangles", "marks": 7,
     "lead": "In the diagram below, ABC, ACD and ADE are right-angled triangles.\nBÂE = 90° and BÂC = 30°. BC = 20 units and AD = 60 units.\n\n"
             "Calculate the:",
     "figure": fig("Q4.1", "A figure with A at the top left and E at the top right, AE horizontal. B is directly below A, so AB is vertical, and C "
                   "is to the right of B on the horizontal side BC, marked 20. AC and AD are drawn, AD marked 60; D lies below and to the left of "
                   "E and is joined to C and to E. Right angles are marked at B, at A (between AB and AE), at C (between AC and CD) and at D "
                   "(between AD and DE). The angle between AB and AC is marked 30°."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Trigonometric equations", "marks": 8,
     "lead": "Solve for x, correct to ONE decimal place, where 0° ≤ x ≤ 90°:", "items": q42},
    {"id": "5.1", "title": "Question 5.1", "kind": "The tangent graph", "marks": 5, "lead": "Consider the function f(x) = −3 tan x.", "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "The cosine graph", "marks": 7, "lead": "Sketched below is the graph of g(x) = a.cos bθ",
     # (no turning points or intercepts: 5.2.1-5.2.3 read them)
     "figure": fig("Q5.2", "The graph of g, a smooth wave drawn from x = 0° to x = 360°, on axes marked 90°, 180°, 270° and 360° along the x-axis "
                   "and −2, −1, 0, 1 and 2 up the y-axis."), "items": q52},
    {"id": "6", "title": "Question 6", "kind": "Volume and surface area", "marks": 7,
     "lead": "The diagram below shows a cup with a volume of 117π cm³ and an inner diameter of 60 mm. Ignore the thickness of the cup.\n\n"
             "Calculate the:",
     "figure": fig("Q6", "A cylindrical cup: its inner diameter, 60 mm, is marked across the top, and its height h is marked down the right-hand "
                   "side. The cup is drawn partly filled with water (shaded)."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Triangles and parallelograms", "marks": 9, "lead": REASONS,
     "figure": fig("Q7", "The diagram of 7.2. Triangle ACS: A at the top, C at the bottom left and S at the bottom right. R and B lie on AC, R "
                   "nearer to C and B between R and A; P lies on AS. Q lies to the left of AC: QP crosses AC at B, and QR, RS and QC are drawn, "
                   "PSRQ being the parallelogram. CR and PS carry the same tick mark. Angles are numbered: Q̂₁ between QC and QR, Q̂₂ between QR "
                   "and QP; B̂₁, B̂₂ and B̂₃ at B; R̂₁ between RS and RC, R̂₂ between RA and RS, R̂₃ between RQ and RA; P̂₁ and P̂₂ at P; Ŝ₁ and Ŝ₂ at "
                   "S; Ĉ₁ between CQ and CR, Ĉ₂ between CR and CS."), "items": q7},
    {"id": "8.1", "title": "Question 8.1", "kind": "Parallelogram proofs", "marks": 9,
     "lead": REASONS + " ABCD is a parallelogram. E and F are points on AB and DC respectively such that AE = CF. DE is produced to J and CJ is "
                       "drawn. BF is produced to K and AK is drawn.\n\nProve that:",
     "figure": fig("Q8.1", "Parallelogram ABCD: A at the top left, B at the top right, C at the bottom right and D at the bottom left. E lies on AB "
                   "and F on DC; AE and FC carry the same tick mark. DE is produced up beyond AB to J, and BF is produced down beyond DC to K. CJ "
                   "cuts AB at G, and AK cuts DC at H. Angles are numbered at A (1, 2), E (1, 2, 3), G (1, 2, 3), B (1, 2), D (1, 2), H (1, 2, "
                   "3), F (1, 2, 3) and C (1, 2): Ê₁ lies between EJ and EB, and F̂₁ between FD and FK."), "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Circle diagram proofs", "marks": 6,
     "lead": REASONS + " In the diagram below O is the centre of the circle. A and B lie on the circumference of the circle. AP = BP.\n\nProve that:",
     "figure": fig("Q8.2", "A circle with centre O. A (upper left) and B (lower right) lie on the circle, and P lies outside it to the upper right. "
                   "PA and PB are drawn and carry the same double tick mark. OA, OB and the chord AB are drawn, and OP cuts AB at T. Angles are "
                   "numbered at A (1, 2), P (1, 2), B (1, 2), O (1, 2) and T (1, 2, 3, 4): T̂₁ lies between TA and TO."), "items": q82},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.3.1", "1.3.2", "1.4", "2.1.1", "2.1.2", "2.1.3", "2.2.1", "2.2.2", "2.2.3", "2.3", "3.2.1", "3.2.2", "3.3", "4.1.1",
                           "4.1.2", "4.1.3", "4.2.2", "4.2.3", "5.2.4", "6.1", "6.2", "7.2.1", "7.2.2", "8.1.1", "8.1.2", "8.2.1"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["1.1", "3.1.1", "3.1.2", "5.1.2(b)", "5.2.1", "5.2.2", "5.2.3", "8.2.2"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["1.2", "4.2.1", "5.1.2(a)"]   # the read-off numbers
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["1.5", "5.1.1"]
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn"]
assert PICKS == ["7.1"], PICKS
for _m in missions:   # a gate names an EARLIER part of its own mission (the app looks a gate up inside the mission)
    _order = [i["n"] for i in _m["items"]]
    for _i in _m["items"]:
        assert all(e in _order[:_order.index(_i["n"])] for e in _i.get("after", [])), (_i["n"], "a gate outside its mission or later")
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
GATES = {i["n"]: i["after"] for i in ITEMS if i.get("after")}

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2018", "total_marks": 100, "time": "2 hours"},
    "sections": [{"title": "Mathematics", "total": 100, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines and every geometry proof plays as four workings, the memo's FIRST method line by "
                                                       "line (a geometry statement with its [reason]) and three built from real errors (a wrong "
                                                       "ratio, formula or theorem, a sign slip, a misread value, the wrong side or pair of lines, "
                                                       "a wrong reason, circular reasoning, the calculator in radians), 0 or full marks: "
                                                       + ", ".join(AUTHORED) + " (%d parts, %d marks). The memo's OR methods and values (2.2.1 "
                                                       "QT from T, 2.2.2 QŜP = 59°, 2.2.3 sin QŜP and QR's equation, 2.3 the midpoint (5 ; −1), "
                                                       "3.3 √2/√3 and √6/3, 4.1.1 cosec 30°, cos 60° and sec 60°, 6.2 the height 10,4, 7.2.2 "
                                                       "△QBR ≡ △PBA, 8.1.1 △AED ≡ △CFB, 8.1.2 through Ê₃, F̂₃ or EDFB, 8.2.1 the congruent "
                                                       "triangles) are other right routes and never a wrong option. 4.1.3 joins the memo's six "
                                                       "lines into four." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.1", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                 "with no working (the frequency column, a ratio, a trigonometric ratio, an equation of a graph, "
                                                 "a and b, an interval, a range, a one-line reason): four options, the memo's answer and three "
                                                 "common errors, 0 or full marks. 1.1 loses the memo's 1 mark for 5-10 values correct, 5.2.1 its "
                                                 "split a / b, 5.2.3 its split critical values / notation. 3.1.2's memo accepts sec Q, cosec R, "
                                                 "cosec(90° − Q) and sec(90° − R): sec Q is the right option and no wrong one equals QR/QP. 8.2.2's "
                                                 "right reason words the memo's 'properties of a kite' as 'properties of a kite: diagonals ⊥'."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 8), hand-transcribed from the page images of a SCANNED "
                                                           "question paper, memo and answer book (no text layer); no API call."},
        {"n": "1.2", "kind": "no_fit", "detail": "Read-off numbers with no working stay typed on the keypad: 1.2 (42 learners), 4.2.1 (63,5°: keyed "
                                                 "at one decimal place, tolerance 0,06, so 63,4 and 63,6 are marked wrong where the memo gives "
                                                 "1/2 for incorrect rounding) and 5.1.2(a) (180°)."},
        {"n": "1.5", "kind": "no_fit", "detail": "Drawings (1.5 the box and whisker diagram on the answer book's number line, 5.1.1 the graph of f "
                                                 "on its grid) are done on paper and self-checked against the memo's criteria; the answer book's "
                                                 "blank number line and grid are described in the memo text, not cropped."},
        {"n": "7.1", "kind": "no_fit", "detail": "Completing the theorem plays as statements, pick 1: the memo's 'Bisects the third side' and four "
                                                 "cards that are false for every triangle (the line is half the second side and parallel to it, "
                                                 "so neither 'equal in length to the second side' nor 'bisects the second side' holds)."},
        {"n": "7.2.2", "kind": "no_fit", "detail": "A working that shows an earlier part's answer opens only once that part is answered ('after'): "
                                                   + "; ".join(k + " after " + " and ".join(v) for k, v in GATES.items()) + ". Question 7 is one "
                                                   "mission so that 7.2.2 (its AP = PS [line from midpoint ∥ to one side of △] completes 7.1's "
                                                   "theorem) can open after 7.1; 7.2's stem is repeated in 7.2.1 and 7.2.2."},
        {"n": "4.1", "kind": "memo_issue", "detail": "The paper prints 'right-angled tirangles'; transcribed 'triangles' (the paper's typo)."},
        {"n": "5.1.1", "kind": "memo_issue", "detail": "The paper prints 'intercepts and asympotes'; transcribed 'asymptotes' (the paper's typo)."},
        {"n": "5.2", "kind": "memo_issue", "detail": "The paper prints 'g(x) = a.cos bθ', θ where x is meant (the graph's axis is x and 5.2.2 asks for "
                                                     "x); kept as printed, read as g(x) = a cos bx (the memo: a = −2, b = 1)."},
        {"n": "7.2.2", "kind": "memo_issue", "detail": "The memo's OR method gives R̂₃ = Â '(proven) or (alt ∠s; QR || QS)': QS is a slip for AS "
                                                       "(QR ∥ AS, as in 7.2.1). The OR is not played; the right option is the memo's first method."},
    ],
}
QTOTAL = {"1": 14, "2": 17, "3": 11, "4": 15, "5": 12, "6": 7, "7": 9, "8": 15}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
assert per_q == QTOTAL, per_q
# the right letter: across the authored workings each of A-D 3 to 7 times; across the four-option multiple choice within 3 of even
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert min(wspread.values()) >= 3 and max(wspread.values()) <= 7, wspread
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, authored workings:", wspread, "four-option:", fspread)
print("statement right-card positions:", {i["n"]: i["pool"] for i in ITEMS if i["t"] == "pickn"})
total = sum(i["marks"] for i in ITEMS)
assert total == 100, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts; gated:", len(GATES))
print("total:", total)
# every gate, in full: a gate dropped by a helper or an edit fails the run before anything is written
assert GATES == {
    "1.3.2": ["1.1", "1.2"],            # the frequencies and n = 42
    "1.4": ["1.2"],                     # n = 42 (the 21,5th position)
    "1.5": ["1.3.1", "1.4"],            # its criteria: the minimum 1, the maximum 9 and the median 6
    "2.2.1": ["2.1.1"],                 # PQ = √34
    "2.2.3": ["2.1.1", "2.2.2"],        # √34 and θ = 31°
    "3.2.2": ["3.2.1"],                 # r = OS = 5
    "4.1.2": ["4.1.1"],                 # AC = 40
    "4.1.3": ["4.1.2"],                 # CÂD = 48,19°
    "6.2": ["6.1"],                     # h = 13 cm
    "7.2.2": ["7.1"],                   # AP = PS: the line from the midpoint bisects the third side
    "8.2.2": ["8.2.1"]}, GATES          # OAPB is a kite
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's, memo's and answer book's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 8 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
