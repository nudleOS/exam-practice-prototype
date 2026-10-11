"""Grade 11 Mathematics P2 Nov 2018 (DBE common paper), the whole paper (Questions 1 to 11, 150 marks, 3 hours as the cover prints
them: statistics, analytical geometry, trigonometry, measurement, Euclidean geometry), hand-transcribed into the catalogue format,
then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working are the paper's and
the memo's own (its English); clues and figure captions are ours. No API call: the transcription is the source, kept in git (out/
is not). The question paper (16 pages, English only), the memo (28 pages, bilingual) and the answer book (24 pages) are SCANS (no
text layer): everything was read from their page images rendered at 150 dpi (the answer book at 100 dpi), with crops at 200-250 dpi
where a label or an angle number mattered (the Question 10.2 and 11 diagrams, the answer book's 7.1 triangle, its Question 3 axes
and its frequency-polygon grid).

  python tools/ingest/transcribe_g11_math_p2_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Mathematics P2 Nov 2018 Eng.pdf" "uploads/Grade 11 Mathematics P2 Nov 2018 MG Afr & Eng.pdf" --id g11-math-p2-2018-11 --from-json --answer-book "uploads/Grade 11 Mathematics P2 Nov 2018 Answer Book Afr & Eng.pdf"

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p2_2025_11.py, the Grade 10 P2 papers
transcribe_g10_math_p2_2018_11.py / transcribe_g10_math_p2_2017_11.py and the same sitting's transcribe_g11_math_p1_2018_11.py):
  every part the memo WORKS OUT in two or more lines (a mean, an interval, a combined mean, a read-off difference, a gradient, an
  equation, a length, coordinates, an angle, a trigonometric value, a reduction, an identity, a general solution, a cosine-rule
  length, an area, a volume, a value of x) and every geometry proof -> authored whole-working multiple choice, `work`: the memo's
  FIRST method line by line (a geometry statement with its [reason] at the line's end, "{a}/{b}" a stacked fraction, never nested)
  and three workings each built from a DIFFERENT real error (a wrong formula, ratio, identity or theorem, a sign slip, a misread
  value, the wrong side, pair of lines or quadrant, a wrong reason, circular reasoning, the calculator in radians), every option of
  a part the same layout (`shape`), the right one's place spread over A-D across the paper; the part keeps its marks, all or
  nothing. In a 'show that' or 'prove' (3.6, 5.3, 7.2.2, 8.1, 9.3, 10.1, 10.2.2, 11.1, 11.2) every option ends in the given result:
  a wrong one reaches it through a wrong step or reason, or by starting from the answer. The memo's OR methods and values are other
  right routes and never a wrong option.
  An answer the memo states with no working (the frequency column, tan θ, a range, a and b, coordinates, an equation of a graph,
  AĈD in θ and α, an angle with its one reason) -> authored multiple choice of answers: the memo's and three common errors.
  One number with no working (1.1, 1.3, 2.1.1, 6.2) stays num; the frequency polygon 2.1.4 -> draw (self-checked against the
  memo's criteria); 2.2 (agree or not, with two arguments) -> statements, 1 mark each.
  Where a part's stem, options, cards or criteria show an EARLIER part's answer it carries "after" (the GATES assert at the end).
Missions: Questions 1, 3, 4, 6, 8 and 11 share one stem (and diagram or data) each, so each is one mission; Questions 2, 5, 7, 9
and 10 change their stem part-way, so their numbered groups are missions (2.1, 2.2, 5.1, ... 10.2).
No figure comes from the answer book: its frequency table (2.1.3) is typed into the stem, its frequency-polygon grid (2.1.4) is a
blank answer space (the draw memo describes it), and its other diagrams repeat the question paper's (its 7.1 triangle with the 67°
moved to Q: memo_issue below).
Figure boxes are measured in PDF points (page 595 x 841, read from the PDF) from the ink on the scan (scratch tool
lower/g11-math-p2-2018-11/figs.py) and checked on a contact sheet with ingest's 1% pad applied."""
import json
import random
import re
from pathlib import Path

PID = "g11-math-p2-2018-11"
W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q2.1": [4, 78.6, 171.2, 514.0, 448.7],     # the ogive in its frame
    "Q3": [6, 61.7, 191.5, 541.2, 517.9],       # the axes, ABCD, E, N and M
    "Q4": [7, 95.8, 225.1, 500.9, 484.8],       # the axes and △FGC with N, β, θ and 104,04°
    "Q5.1": [8, 172.2, 188.6, 456.8, 347.5],    # T, P, θ and K
    "Q6": [9, 59.1, 175.7, 575.6, 467.0],       # f and g on their grid
    "Q7.1": [10, 209.8, 180.2, 422.0, 315.0],   # △PQR (the "(3)" mark column left out)
    "Q7.2": [10, 175.2, 380.2, 424.3, 605.3],   # △ABC with D, α, θ and h
    "Q8": [11, 212.2, 175.1, 317.3, 317.2],     # the cone (its formula box is typed in the lead)
    "Q9.1": [12, 180.8, 245.1, 447.6, 507.2],   # the circle with A-E and O
    "Q9.2": [13, 165.3, 134.6, 424.0, 399.6],   # the circle PQRT with centre S
    "Q9.3": [13, 235.2, 503.0, 431.5, 696.9],   # the circle with chord AC and radius OD
    "Q10.1": [14, 165.7, 183.0, 399.4, 423.0],  # cyclic quadrilateral PTSR
    "Q10.2": [15, 122.5, 204.6, 449.8, 448.4],  # the circle with diameters QS and PR, M, N and T
    "Q11": [16, 126.7, 196.5, 490.1, 550.3]}    # the two circles


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
DP2 = 0.006     # a value keyed at two decimal places: 5,79 accepted, 5,78 and 5,80 not


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


def stmt(n, q, marks, right, wrong, clues, each, **kw):
    """A written answer as statements: the memo's points (right) and clearly false cards (wrong), shuffled with a fixed seed."""
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random(PID + ":" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    pool = sorted(k for k, i in enumerate(order) if i < len(right))
    print("statements", n, "right cards at", pool, "of", len(opts))
    assert (count > 1 or pool[0] != 0) and pool != list(range(len(pool))), (n, "a single right card first, or all right cards on top", pool)
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count, **kw}


# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
INT2 = "(x̄ − 2σ ; x̄ + 2σ) = (16,9 − 2 × 5,79 ; 16,9 + 2 × 5,79)\n= (5,32 ; 28,48)\n"
OUT2 = " completed the race outside two standard deviations of the mean"
q1 = [
    num("1.1", "How long, in minutes, did it take for the fastest member of this team to complete the race?", 4, 0, "minutes",
        ["Does the fastest member take the most time or the least time?", "Is the table already in order from the shortest time to the "
                                                                          "longest?"]),
    work("1.2", "Determine the mean time taken by this team.", 2, [
        "Mean = {169}/{10}\n= 16,9 minutes",          # the memo
        "Mean = {169}/{9}\n= 18,78 minutes",          # divided by n − 1
        "Mean = {17 + 18}/{2}\n= 17,5 minutes",       # the median
        "Mean = {4 + 25}/{2}\n= 14,5 minutes"], 0,    # the middle of the smallest and the largest time
        ["What is the total of all ten times?", "How many members' times do you divide that total by?"], after=["1.1"]),
    num("1.3", "Calculate the standard deviation for the data.", 5.79, DP2, "minutes",
        ["Which calculator mode works out the standard deviation of a list of data?", "Is this the whole team (σ) or a sample of it?"]),
    work("1.4", "How many members of the team completed the obstacle race outside of two standard deviations of the mean?", 3, [
        "(x̄ − σ ; x̄ + σ) = (16,9 − 5,79 ; 16,9 + 5,79)\n= (11,11 ; 22,69)\n2 members" + OUT2,                          # one σ, not two
        INT2 + "1 member" + OUT2,                                                                                     # the memo
        INT2 + "9 members" + OUT2,                                                                                    # the times INSIDE counted
        "(x̄ − 2σ ; x̄ + 2σ) = (16,9 − 2 × 33,49 ; 16,9 + 2 × 33,49)\n= (−50,08 ; 83,88)\n0 members" + OUT2], 1,      # the variance as σ
        ["What are the values two standard deviations below and above the mean?", "Which times in the table lie outside that interval?"],
        after=["1.2", "1.3"]),
    work("1.5", "It took another team a total time of x + 5 minutes to complete the race. Calculate the value of x if the overall mean of the "
         "two teams combined was 18 minutes.", 3, [
        "{169 + x + 5}/{10} = 18\nx = 18 × 10 − 174\nx = 6",        # divided by one team's 10 members
        "{169 + x + 5}/{2} = 18\nx = 18 × 2 − 174\nx = −138",       # divided by the 2 teams
        "{169 + x + 5}/{20} = 18\nx = 18 × 20 − 174\nx = 186",      # the memo
        "{169 + x + 5}/{20} = 18\nx = 18 × 20 − 164\nx = 196"], 2,  # the 5 taken off 169 instead of added
        ["How many members do the two teams have together, and what is their total time?", "How is a mean worked out from a total?"],
        after=["1.2"]),
]

# ---- QUESTION 2, the question paper pages 4-5 and the memo pages 3-4 ----
CF = ("\n\nCLASS INTERVAL : CUMULATIVE FREQUENCY\n15 ≤ x < 20 : 4\n20 ≤ x < 25 : 13\n25 ≤ x < 30 : 37\n30 ≤ x < 35 : 47\n35 ≤ x < 40 : 50"
      "\n\nEach option gives the frequencies of the five classes, in this order.")
q21 = [
    num("2.1.1", "How many players took part in the soccer tournament?", 50, 0, "players",
        ["What does the last point of an ogive tell you?", "Which axis counts the players?"]),
    work("2.1.2", "Determine the number of players between the ages of 24 and 31 years old.", 2, [
        "Number of players = 37 − 13\n= 24 players",     # the class ends 30 and 25 read from the table
        "Number of players = 40 − 4\n= 36 players",      # 24 read as 20 on the age axis
        "Number of players = 31 − 24\n= 7 players",      # the ages subtracted
        "Number of players = 40 − 10\n= 30 players"], 3,  # the memo
        ["How many players are younger than 31 on the curve, and how many younger than 24?", "How do those two cumulative counts give the "
                                                                                              "players in between?"]),
    mcq("2.1.3", "Complete the frequency column of the table below in the ANSWER BOOK." + CF + ANSWER, [
        "4 ; 13 ; 37 ; 47 ; 50",      # the cumulative frequencies copied
        "4 ; 9 ; 24 ; 10 ; 3",        # the memo
        "0 ; 4 ; 9 ; 24 ; 10",        # each frequency one class late
        "46 ; 37 ; 13 ; 3 ; 0"], 1,   # 50 minus each cumulative frequency
        ["A cumulative frequency is a running total: how do you get one class's own count back from it?", "Which class's frequency equals "
                                                                                                          "its cumulative frequency?"],
        marks=3, after=["2.1.1"]),
    draw("2.1.4", "Use the grid provided in the ANSWER BOOK to draw a frequency polygon for the data.", 4, [
        ["Using the class midpoints: 17,5 ; 22,5 ; 27,5 ; 32,5 ; 37,5", 1],
        ["Plotting the points correctly: (17,5 ; 4), (22,5 ; 9), (27,5 ; 24), (32,5 ; 10), (37,5 ; 3)", 1],
        ["The points joined by straight lines", 1], ["Grounding at (12,5 ; 0) and (42,5 ; 0)", 1]],
        ["Where is the middle of each class?", "Where does a frequency polygon start and end on the horizontal axis?"],
        memo="The answer book gives a grid: Frequency from 0 to 25 up (labelled every 5, a line every 1) and Ages of soccer players from 0 "
             "to 40 along (labelled every 5, a line every year, running a little past 40). The memo's polygon: (12,5 ; 0), (17,5 ; 4), "
             "(22,5 ; 9), (27,5 ; 24), (32,5 ; 10), (37,5 ; 3) and (42,5 ; 0), joined by straight lines.", after=["2.1.3"]),
]
q22 = [
    # 1 + 1 + 1: the choice and the memo's two arguments; the wrong cards are false for these summaries (IQR A = 34 > B = 17, the
    # minimum of B (50) is above A's (30), Q₃ of B (75) is below A's (82)). With eight cards the seeded shuffle put the three right
    # cards on top ([0, 1, 2]); eight is the most cards a part takes, so a fifth wrong card ("the marks of class B are more spread out")
    # came out instead: seven cards put them at [0, 1, 6]
    stmt("2.2", "Do you agree with this claim? Use at least TWO different arguments to justify your answer.", 3,
         ["I do not agree: the claim is not valid.",
          "The range of class A (60) is bigger than the range of class B (40), so the marks of class A are more spread out.",
          "At least 25% of class A have lower marks than any learner in class B: class A did worse at the bottom end."],
         ["I agree: the claim is valid.", "The interquartile range of class A is smaller than that of class B.",
          "The lowest mark in class B is lower than the lowest mark in class A.", "The upper quartile of class B is higher than that of class A."],
         ["What do the minimum and the quartiles of each summary tell you that the median does not?", "Can two classes with the same middle "
                                                                                                       "mark still be spread out differently?"], 1),
]

# ---- QUESTION 3, the question paper page 6 and the memo pages 5-8 ----
AD = "m(AD) = m(BC) = {4}/{3} (AD ∥ BC)\n"
T0 = "0 = {4}/{3}t + {14}/{3}\n"
ANF = "AN = √((−2 − (−{7}/{2}))² + (2 − 0)²)\n"
D35 = "{3}/{8}x − 3 = {4}/{3}x + {14}/{3}\n"
MAB = "m(AB) = {5 − 2}/{6 − (−2)} = {3}/{8}\nm(AB) = m(DC), so AB ∥ DC\nbut AD ∥ BC\n∴ ABCD is a parallelogram "
MAC = "M is the midpoint of AC [diagonals bisect]\n"
q3 = [
    work("3.1", "Calculate the gradient of BC.", 2, [
        "m(BC) = {0 − 6}/{−3 − 5}\n= {−6}/{−8}\n= {3}/{4}",      # x over y
        "m(BC) = {−3 − 5}/{0 − 6}\n= {−8}/{−6}\n= {4}/{3}",      # the memo (OR B − C on top and below)
        "m(BC) = {−3 − 5}/{6 − 0}\n= {−8}/{6}\n= −{4}/{3}",      # C − B on top, B − C below
        "m(BC) = {5 − 3}/{6 − 0}\n= {2}/{6}\n= {1}/{3}"], 1,     # −(−3) taken as −3
        ["Which formula gives the gradient of a line through two points?", "Do you take the two points in the same order on top and below?"]),
    work("3.2", "Determine the equation of AD.", 3, [
        "m(AD) = −{3}/{4} (AD ∥ BC)\n2 = −{3}/{4}(−2) + c\nc = {1}/{2}\ny = −{3}/{4}x + {1}/{2}",   # the perpendicular gradient
        AD + "2 = {4}/{3}(−2) + c\nc = −{2}/{3}\ny = {4}/{3}x − {2}/{3}",                         # −8/3 moved across without its sign change
        AD + "2 = {4}/{3}(−2) + c\nc = {14}/{3}\ny = {4}/{3}x + {14}/{3}",                         # the memo (OR y − y₁ = m(x − x₁))
        AD + "−3 = {4}/{3}(0) + c\nc = −3\ny = {4}/{3}x − 3"], 2,                                 # C for A: that is the line BC
        ["AD ∥ BC: what does that tell you about the gradient of AD?", "Which point on AD do you know, to find c in y = mx + c?"],
        after=["3.1"]),
    work("3.3", "Determine the value of t.", 2, [
        T0 + "−{14}/{3} = {4}/{3}t\nt = −{14}/{4} = −{7}/{2}",           # the memo
        T0 + "{14}/{3} = {4}/{3}t\nt = {14}/{4} = {7}/{2}",              # 14/3 moved without its sign change
        T0 + "−{14}/{3} = {4}/{3}t\nt = −{14}/{3} × {4}/{3} = −{56}/{9}",  # multiplied by 4/3 instead of divided
        "t = {4}/{3}(0) + {14}/{3}\nt = 0 + {14}/{3}\nt = {14}/{3}"], 0,  # x = 0 put in: the y-intercept
        ["N lies on the x-axis: what is its y-coordinate?", "What equation do you get when you put that into the equation of AD?"],
        after=["3.2"]),
    work("3.4", "Calculate the length of AN.", 2, [
        "AN = √((−2 + (−{7}/{2}))² + (2 − 0)²)\n= √({137}/{4})\n= 5,85",   # a sign slip: adds N's x
        "AN = (−2 − (−{7}/{2}))² + (2 − 0)²\n= {9}/{4} + 4\n= {25}/{4}",   # the square root forgotten
        ANF + "= {3}/{2} + 2\n= {7}/{2}",                                 # the root shared out over the sum
        ANF + "= √({25}/{4})\n= {5}/{2}"], 3,                             # the memo
        ["Which formula gives the distance between two points?", "What are the coordinates of A and of N?"], after=["3.3"]),
    work("3.5", "If DC is defined by y = (3/8)x − 3, determine the coordinates of D.", 4, [
        D35 + "−{23}/{24}x = {14}/{3} − 3 = {5}/{3}\nx = −{40}/{23} = −1,74\ny = {4}/{3}(−1,74) + {14}/{3} = 2,35\nD(−1,74 ; 2,35)",   # −3 moved without its sign change
        "{3}/{8}x − 3 = {4}/{3}x − 3\n−{23}/{24}x = 0\nx = 0\ny = {4}/{3}(0) − 3 = −3\nD(0 ; −3)",                                        # BC's equation for AD's: that is C
        D35 + "{23}/{24}x = −{23}/{3}\nx = −8\ny = {4}/{3}(−8) + {14}/{3} = −6\nD(−8 ; −6)",                                               # the memo
        D35 + "{23}/{24}x = −{23}/{3}\nx = −8\ny = {4}/{3}(8) + {14}/{3} = 15,33\nD(−8 ; 15,33)"], 2,                                      # −8 put in as 8
        ["D lies on both AD and DC: what can you do with their two equations?", "Once you have x, which equation gives y most easily?"],
        after=["3.2"]),
    work("3.6", "Prove that ABCD is a parallelogram.", 3, [
        MAB + "[diagonals bisect each other]",                                                                           # the wrong reason
        MAB + "[opp sides are ∥]",                                                                                       # the memo (OR AD = BC and AD ∥ BC; OR the diagonals' midpoints)
        "AB ∥ DC [opp sides of ∥m]\nm(AB) = m(DC) = {3}/{8}\nbut AD ∥ BC\n∴ ABCD is a parallelogram",                    # assumes what it proves
        "m(AD) = m(BC) = {4}/{3}\nAD ∥ BC\nAD and BC are a pair of opposite sides\n∴ ABCD is a parallelogram [opp sides are ∥]"], 1,   # one pair only
        ["Which pair of opposite sides is already given parallel?", "What is the gradient of AB, and how does it compare with the gradient "
                                                                    "of DC?"], after=["3.1"]),
    work("3.7", "Calculate the coordinates of M.", 3, [
        "M is the midpoint of AB [diagonals bisect]\nM({−2 + 6}/{2} ; {2 + 5}/{2})\nM(2 ; {7}/{2})",   # AB is a side, not a diagonal
        MAC + "M({0 − (−2)}/{2} ; {−3 − 2}/{2})\nM(1 ; −{5}/{2})",                                   # subtracts in the midpoint
        MAC + "M(−2 + 0 ; 2 + (−3))\nM(−2 ; −1)",                                                    # never halved
        MAC + "M({−2 + 0}/{2} ; {2 + (−3)}/{2})\nM(−1 ; −{1}/{2})"], 3,                              # the memo
        ["What do the diagonals of a parallelogram do to each other?", "Which formula gives the midpoint of a line segment?"]),
]

# ---- QUESTION 4, the question paper page 7 and the memo pages 9-10 ----
FC = "FC = √((6 − 2)² + (−5 − (−2))²)\n= √(16 + 9) = 5\n"
q4 = [
    work("4.1", "Calculate the gradient of FG.", 2, [
        "m(FG) = {2 − (−2)}/{5 − 2}\n= {4}/{3}",      # the memo
        "m(FG) = {5 − 2}/{2 − (−2)}\n= {3}/{4}",      # x over y
        "m(FG) = {2 − 2}/{5 − 2}\n= 0",               # −(−2) taken as −2
        "m(FG) = {2 − (−2)}/{2 − 5}\n= −{4}/{3}"], 0,  # G − F on top, F − G below
        ["Which formula gives the gradient between F and G?", "Do you subtract the coordinates in the same order on top and below?"]),
    work("4.2", "Calculate the value of y.", 3, [
        "m(FC) = {4}/{3} (FC ⊥ FG)\n{y + 2}/{6 − 2} = {4}/{3}\ny = {10}/{3}",     # FG's own gradient: parallel, not perpendicular
        "m(FC) = {3}/{4} (FC ⊥ FG)\n{y + 2}/{6 − 2} = {3}/{4}\ny = 1",            # the reciprocal without the sign change
        "m(FC) = −{3}/{4} (FC ⊥ FG)\n{y + 2}/{6 − 2} = −{3}/{4}\ny = −5",         # the memo (OR m(FC) × m(FG) = −1)
        "m(FC) = −{3}/{4} (FC ⊥ FG)\n{y − 2}/{6 − 2} = −{3}/{4}\ny = −1"], 2,     # y − (−2) taken as y − 2
        ["FG ⊥ FC: how are their gradients related?", "How can you write the gradient of FC using F and C(6 ; y)?"], after=["4.1"]),
    work("4.3", "Calculate the size of θ.", 3, [
        "tan β = {4}/{3}\nβ = 53,13°\nθ = 180° − 104,04° − 53,13° [sum of ∠s in △]\nθ = 22,83°",   # 104,04° taken as an angle inside the △
        "tan β = {3}/{4}\nβ = 36,87°\nθ = 104,04° − 36,87° [ext ∠ of △]\nθ = 67,17°",            # tan β as run over rise
        "tan β = {4}/{3}\nβ = 0,93°\nθ = 104,04° − 0,93° [ext ∠ of △]\nθ = 103,11°",             # the calculator in radians
        "tan β = {4}/{3}\nβ = 53,13°\nθ = 104,04° − 53,13° [ext ∠ of △]\nθ = 50,91°"], 3,        # the memo
        ["How is the angle of inclination β related to the gradient of FG?", "In the triangle that FG, NC and the x-axis make, how is the "
                                                                             "104,04° angle related to β and θ?"], after=["4.1"]),
    work("4.4", "Calculate the length of NC.", 4, [
        FC + "cos θ = {FC}/{NC}\ncos 50,91° = {5}/{NC}\nNC = {5}/{cos 50,91°} = 7,93 units",            # cosine for sine
        FC + "sin θ = {FC}/{NC}\nsin 50,91° = {5}/{NC}\nNC = {5}/{sin 50,91°} = 6,44 units",            # the memo
        FC + "sin θ = {NC}/{FC}\nsin 50,91° = {NC}/{5}\nNC = 5 sin 50,91° = 3,88 units",                # the ratio upside down
        "FC = √((6 − 2)² + (−5 − 2)²)\n= √(16 + 49) = √65\nsin θ = {FC}/{NC}\nsin 50,91° = {√65}/{NC}\n"
        "NC = {√65}/{sin 50,91°} = 10,39 units"], 1,                                                   # −(−2) taken as −2
        ["In right-angled △NFC, which side is opposite θ and which is the hypotenuse?", "How long is FC, from F and C?"],
        after=["4.2", "4.3"]),
]

# ---- QUESTION 5, the question paper page 8 and the memo pages 11-15 ----
PY = "x² + (15)² = 17² [Pythagoras]\nx² = 64\n"
TA = "tan θ = {a}/{−2} = {15}/{−8}\n{a}/{−2} = {15}/{−8}\n"
RED = "= {sin 60°.(−cos 30°)(−tan 45°).sin 63°}/{cos 180°.sin 63°}\n"
L1 = "LHS = {1}/{cos θ} − {cos θ}/{1 + sin θ}\n= {1 + sin θ − cos² θ}/{cos θ(1 + sin θ)}\n"
SC = "3 sin x = 2 × {sin x}/{cos x}\n3 sin x cos x = 2 sin x\n"
SIN0 = "sin x = 0: x = 360°.k or x = 180° + 360°.k ; k ∈ Z\n"
q51 = [
    work("5.1.1", "The value of x", 2, [
        PY + "x = −8 (T is in quadrant 2)",                                      # the memo
        PY + "x = 8",                                                            # the sign of the quadrant ignored
        "x² = (15)² + 17² [Pythagoras]\nx² = 514\nx = −22,67 (T is in quadrant 2)",   # adds: OT taken as a shorter side
        "x² = (17 − 15)² [Pythagoras]\nx² = 4\nx = −2 (T is in quadrant 2)"], 0,      # subtracts before squaring
        ["OT is the hypotenuse of a right-angled triangle: what are its other two sides?", "In which quadrant is T, and what sign does its "
                                                                                           "x-coordinate have?"]),
    mcq("5.1.2", "tan θ" + ANSWER, ["tan θ = −{15}/{8}", "tan θ = {15}/{8}", "tan θ = −{8}/{15}", "tan θ = {15}/{17}"], 0,
        ["Which two of x, y and r does tan θ use?", "What are the coordinates of T?"], after=["5.1.1"]),
    work("5.1.3", "cos(180° − θ)", 2, [
        "cos(180° − θ) = cos θ\n= (−{8}/{17})\n= −{8}/{17}",        # no sign change in the reduction
        "cos(180° − θ) = −sin θ\n= −({15}/{17})\n= −{15}/{17}",     # a co-function swap at 180°
        "cos(180° − θ) = −cos θ\n= −({8}/{17})\n= −{8}/{17}",       # x taken as 8, not −8
        "cos(180° − θ) = −cos θ\n= −(−{8}/{17})\n= {8}/{17}"], 3,   # the memo
        ["What does the reduction formula turn cos(180° − θ) into?", "What is cos θ in terms of x and r for T?"], after=["5.1.1"]),
    work("5.1.4", "sin² θ", 2, [
        "sin² θ = {15²}/{17}\n= {225}/{17}",           # only the numerator squared
        "sin² θ = (−{8}/{17})²\n= {64}/{289}",         # x/r for sin θ
        "sin² θ = ({15}/{17})²\n= {225}/{289}",        # the memo
        "sin² θ = 2({15}/{17})\n= {30}/{17}"], 2,      # squared as doubled
        ["Which two of x, y and r does sin θ use?", "What does squaring a fraction do to its numerator and to its denominator?"],
        after=["5.1.1"]),
    work("5.1.5", "The value of a", 3, [
        "tan θ = {−2}/{a} = {15}/{−8}\n{−2}/{a} = {15}/{−8}\na = {16}/{15}",    # tan θ as x/y
        TA + "a = {15}/{4}",                                                    # the memo (OR the line y = −15/8 x through P)
        "tan θ = {a}/{−2} = {15}/{8}\n{a}/{−2} = {15}/{8}\na = −{15}/{4}",      # the sign of −8 lost
        TA + "a = 60"], 1,                                                      # rearranged as 15 × (−8) ÷ (−2)
        ["P and T lie on the same line through O: what do they share?", "How can you write tan θ using the coordinates of P?"],
        after=["5.1.1", "5.1.2"]),
]
q52 = [
    work("5.2", "Simplify WITHOUT using a calculator:\n(sin 120°.cos 210°.tan 315°.cos 27°)/(sin 63°.cos 540°)", 7, [
        RED + "= ({√3}/{2})(−{√3}/{2})(−1) ÷ (−1)\n= −{3}/{4}",                                                   # the memo
        "= {sin 60°.(cos 30°)(−tan 45°).sin 63°}/{cos 180°.sin 63°}\n= ({√3}/{2})({√3}/{2})(−1) ÷ (−1)\n= {3}/{4}",   # cos 210° without its sign
        RED + "= ({√3}/{2})(−{1}/{2})(−1) ÷ (−1)\n= −{√3}/{4}",                                                   # cos 30° taken as ½
        RED + "= ({√3}/{2})(−{√3}/{2})(−√3) ÷ (−1)\n= −{3√3}/{4}"], 0,                                            # tan 45° taken as √3
        ["Which reduction formulae turn 120°, 210°, 315° and 540° into acute angles, and with which signs?", "How are cos 27° and sin 63° "
                                                                                                             "related?"]),
]
q53 = [
    work("5.3", "Prove the identity:\n1/cos θ − cos θ/(1 + sin θ) = tan θ", 5, [
        L1 + "= {1 + sin θ − 1 − sin² θ}/{cos θ(1 + sin θ)}\n= {sin θ(1 − sin θ)}/{cos θ(1 + sin θ)}\n= {sin θ}/{cos θ}\n= tan θ = RHS",   # a sign slip, then 1 − sin θ cancelled with 1 + sin θ
        "tan θ = {1}/{cos θ} − {cos θ}/{1 + sin θ}\n{sin θ}/{cos θ} = {1 + sin θ − cos² θ}/{cos θ(1 + sin θ)}\nsin θ(1 + sin θ) = 1 + sin θ − cos² θ\n"
        "sin θ + sin² θ = 1 + sin θ − cos² θ\nsin² θ + cos² θ = 1\nso LHS = RHS",                                                       # starts from the answer
        L1 + "= {1 + sin θ − (1 − sin² θ)}/{cos θ(1 + sin θ)}\n= {sin θ(1 + sin θ)}/{cos θ(1 + sin θ)}\n= {sin θ}/{cos θ}\n= tan θ = RHS",  # the memo (OR 1 − cos² θ = sin² θ)
        "Let θ = 30°\nLHS = {1}/{cos 30°} − {cos 30°}/{1 + sin 30°}\n= {2}/{√3} − {√3}/{2} ÷ {3}/{2}\n= {2}/{√3} − {√3}/{3}\n= {√3}/{3}\n"
        "= tan 30° = RHS"], 2,                                                                                                          # one value tried: no proof
        ["What common denominator do the two fractions on the left share?", "Which identity lets you write cos² θ in terms of sin θ?"]),
]
q54 = [
    work("5.4", "Determine the general solution of 3 sin x = 2 tan x", 6, [
        SC + "3 cos x = 2 (both sides ÷ sin x)\ncos x = {2}/{3}\nx = 48,19° + 360°.k\nor x = 311,81° + 360°.k ; k ∈ Z",          # sin x = 0 lost
        SC + "3 sin x cos x − 2 sin x = 0\nsin x(3 cos x − 2) = 0\n" + SIN0 + "cos x = {2}/{3}: x = 48,19° + 360°.k or x = 131,81° + 360°.k ; k ∈ Z",   # cos's second angle in quadrant II
        "3 sin x = 2 sin x cos x\n2 sin x cos x = 3 sin x\n2 sin x cos x − 3 sin x = 0\nsin x(2 cos x − 3) = 0\n" + SIN0 + "cos x = {3}/{2}: no solution",  # tan x taken as sin x.cos x
        SC + "3 sin x cos x − 2 sin x = 0\nsin x(3 cos x − 2) = 0\n" + SIN0 + "cos x = {2}/{3}: x = 48,19° + 360°.k or x = 311,81° + 360°.k ; k ∈ Z"], 3,   # the memo (OR 180°.k and ±48,19° + 360°.k)
        ["How can you write tan x in terms of sin x and cos x?", "What happens to the solutions of sin x = 0 if you divide both sides by "
                                                                 "sin x?"]),
]

# ---- QUESTION 6, the question paper page 9 and the memo page 16 ----
KM = " and M(−45° ; −1)\n"
q6 = [
    mcq("6.1", "Write down the range of f." + ANSWER, ["−3 < y < 3", "−1 ≤ y ≤ 1", "−3 ≤ y ≤ 3", "−180° ≤ x ≤ 180°"], 2,
        ["What are the lowest and highest y-values of f on the graph?", "Does f reach those values, so that the end points belong to the "
                                                                        "range?"], marks=2),
    num("6.2", "If M(−45° ; −1) lies on g, determine the value of c.", 1, 0, "",
        ["M lies on g: what must its coordinates do in the equation of g?", "What is tan 45°, and what sign does tan have for a negative "
                                                                            "angle like −45°?"]),
    mcq("6.3", "Write down the values of a and b." + ANSWER, ["a = 3 and b = 2", "a = −3 and b = 1", "a = 1 and b = 3", "a = 3 and b = 1"], 3,
        ["What is the largest y-value of f, and where does f reach it?", "After how many degrees does f complete one full wave?"], marks=2,
        after=["6.1"]),
    mcq("6.4", "Determine the coordinates of Q." + ANSWER, ["Q(−58° ; −1,6)", "Q(122° ; −1,6)", "Q(148° ; −1,6)", "Q(122° ; 1,6)"], 1,
        ["What happens to cos x and to tan x when x is replaced by 180° − x?", "How far is P to the left of x = 90°?"], marks=2),
    work("6.5", "K lies on f such that KM is parallel to the y-axis. Calculate the length of KM.", 2, [
        "K(−45° ; {3√2}/{2})" + KM + "KM = {3√2}/{2} − 1\n= {3√2 − 2}/{2} = 1,12",     # M's y taken off without its sign
        "K(−45° ; {3√2}/{2})" + KM + "KM = {3√2}/{2} + 1\n= {3√2 + 2}/{2} = 3,12",     # the memo
        "K(−45° ; {3}/{2})" + KM + "KM = {3}/{2} + 1\n= {5}/{2} = 2,5",                # cos 45° taken as ½
        "K(−45° ; 1,58)" + KM + "KM = 1,58 + 1\n= 2,58"], 1,                           # the calculator in radians
        ["KM is vertical: which x-value do K and M share?", "How do you find the distance between two points on the same vertical line?"],
        after=["6.3"]),
    mcq("6.6", "If the system of axes is shifted 45° to the left and the graphs remain fixed, write down the equation that is now represented "
        "by graph f." + ANSWER, ["f(x) = 3 cos(x − 45°)", "f(x) = 3 cos(x + 45°)", "f(x) = 3 cos x − 45°", "f(x) = −3 cos(x − 45°)"], 0,
        ["If the axes move to the left and the graph stays where it is, which way does the graph move compared with the new axes?",
         "How does moving a graph sideways change x in its equation?"], marks=2, after=["6.3"]),
]

# ---- QUESTION 7, the question paper page 10 and the memo pages 17-19 ----
COS = "QR² = PR² + PQ² − 2PR.PQ cos P̂\nQR² = (3)² + (9,2)² − 2(3)(9,2) cos 67°\n"
ROOT = "QR = √((3)² + (9,2)² − 2(3)(9,2) cos 67°)\n"
AREA = "Area of △ADC = {1}/{2} × AD × AC × sin "
q71 = [
    work("7.1", "Determine the length of QR.", 3, [
        COS + ROOT + "QR = 8,49 cm",                                                       # the memo
        "QR² = PR² + PQ² + 2PR.PQ cos P̂\nQR² = (3)² + (9,2)² + 2(3)(9,2) cos 67°\nQR = √((3)² + (9,2)² + 2(3)(9,2) cos 67°)\n"
        "QR = 10,73 cm",                                                                   # the rule's sign
        COS + ROOT + "QR = 11,06 cm",                                                      # the calculator in radians
        COS + "QR = (3)² + (9,2)² − 2(3)(9,2) cos 67°\nQR = 72,07 cm"], 0,                 # the square root forgotten
        ["You know two sides and the angle between them: which rule fits?", "Which side is opposite the 67° angle?"]),
]
q72 = [
    mcq("7.2.1", "Determine size of AĈD in terms of θ and α." + ANSWER, ["AĈD = θ + α", "AĈD = α − θ", "AĈD = θ − α", "AĈD = 90° − θ"], 2,
        ["Which angle at C is the bigger one, θ or α?", "AĈB is made up of which two angles at C?"]),
    work("7.2.2", "Prove that AD = h sin(θ − α)/cos α", 4, [
        "D̂₁ = 90° − α\n{sin(90° − α)}/{h} = {sin(θ − α)}/{AD}\n{cos α}/{h} = {sin(θ − α)}/{AD}\nAD = {h sin(θ − α)}/{cos α}",   # D̂₁ taken as 90° − α
        "D̂₁ = 90° + α\n{sin(90° + α)}/{AD} = {sin(θ − α)}/{h}\n{cos α}/{AD} = {sin(θ − α)}/{h}\nAD = {h sin(θ − α)}/{cos α}",   # each side over the wrong angle
        "D̂₁ = 90° + α\n{sin(90° + α)}/{h} = {sin(θ − α)}/{AD}\n{sin α}/{h} = {sin(θ − α)}/{AD}\nAD = {h sin(θ − α)}/{cos α}",   # sin(90° + α) as sin α
        "D̂₁ = 90° + α\n{sin(90° + α)}/{h} = {sin(θ − α)}/{AD}\n{cos α}/{h} = {sin(θ − α)}/{AD}\nAD = {h sin(θ − α)}/{cos α}"], 3,   # the memo
        ["In △ACD, which angle is opposite AD and which is opposite AC?", "D̂₁ lies outside △CDB: how is it related to the angles inside that "
                                                                          "triangle?"], after=["7.2.1"]),
    work("7.2.3", "Determine the length of AD if h = 17 units, θ = 58° and α = 23°.", 2, [
        "AD = {17(sin 58° − sin 23°)}/{cos 23°}\nAD = 8,45 units",    # sin shared out over the difference
        "AD = {17 sin(58° − 23°)}/{cos 23°}\nAD = 10,59 units",       # the memo
        "AD = {17 sin(58° + 23°)}/{cos 23°}\nAD = 18,24 units",       # θ + α for θ − α
        "AD = {17 sin(58° − 23°)}/{cos 23°}\nAD = 13,66 units"], 1,   # the calculator in radians
        ["Which values go in for h, θ and α in the formula you proved?", "Is your calculator in degree mode?"], after=["7.2.1"]),
    work("7.2.4", "Calculate the area of △ADC.", 3, [
        AREA + "AĈD\n= {1}/{2} × 10,59 × 17 × sin 35°\n= 51,63 unit²",           # AĈD is not between AD and AC
        "Area of △ADC = AD × AC × sin Â\n= 10,59 × 17 × sin 32°\n= 95,40 unit²",  # the ½ left out
        AREA + "Â\n= {1}/{2} × 10,59 × 17 × sin 32°\n= 47,70 unit²",             # the memo (OR through CD: 47,71)
        AREA + "Â\n= {1}/{2} × 10,59 × 17 × sin 58°\n= 76,34 unit²"], 2,         # θ taken as Â
        ["Which angle of △ADC lies between the sides AD and AC?", "What do the angles of right-angled △ABC add up to?"], after=["7.2.3"]),
]

# ---- QUESTION 8, the question paper page 11 and the memo page 20 ----
VOL = "V = {1}/{3}πr²h\n= {1}/{3}π(169 − h²)h\n= {169πh − πh³}/{3}"
R5 = "r = √(13² − 12²) = 5 (Pythagoras)\n"
q8 = [
    work("8.1", "Show that the volume of the cone is given by V = (169πh − πh³)/3", 4, [
        "r² = 13² − h² (Pythagoras)\nr² = 169 − h²\n" + VOL,                                                    # the memo
        "r² = 13² + h² (Pythagoras)\nr² = 169 + h²\n" + VOL,                                                    # adds, then the sign changed to reach the result
        "V = {169πh − πh³}/{3}\n= {1}/{3}πh(169 − h²)\n= {1}/{3}πr²h\nso r² = 169 − h²\n= 13² − h² (Pythagoras)",   # starts from the answer
        "r = 13 − h (Pythagoras)\nr² = 169 − h²\n" + VOL], 0,                                                   # (13 − h)² taken as 169 − h²
        ["The height, the radius and the slant height make a right-angled triangle: which of them is the hypotenuse?", "What do you get when "
                                                                                                                         "you put r² into the volume formula?"]),
    work("8.2", "If h = 12 cm, determine the total surface area of the cone.", 3, [
        R5 + "Total surface area = πr² + πrs\n= π(5²) + π(5)(12)\n= 85π = 267,04 cm²",                                      # the height for the slant height
        R5 + "Total surface area = πrs\n= π(5)(13)\n= 65π = 204,20 cm²",                                                     # the base left out
        "r = √(13² + 12²) = 17,69 (Pythagoras)\nTotal surface area = πr² + πrs\n= π(17,69²) + π(17,69)(13)\n= 1 705,86 cm²",   # adds the squares
        R5 + "Total surface area = πr² + πrs\n= π(5²) + π(5)(13)\n= 90π = 282,74 cm²"], 3,                                  # the memo
        ["Which side of the right-angled triangle inside the cone do you still need?", "Which lengths are r and s in the total surface "
                                                                                       "area formula?"]),
]

# ---- QUESTION 9, the question paper pages 12-13 and the memo pages 21-23 ----
CEN = "[∠ at centre = 2 × ∠ at circumference]"
B93 = "OA² = (4x)² + (2x)² [Pythagoras]\nOA = √(16x² + 4x²) = √(20x²) = 2√5 x\nOD = OA = 2√5 x [radii]\n"
q91 = [
    mcq("9.1.1", "Determine the size of Ô₁." + ANSWER, ["Ô₁ = 39° [∠s in the same seg]", "Ô₁ = 19,5° " + CEN, "Ô₁ = 78° [∠s in the same seg]",
                                                       "Ô₁ = 78° " + CEN], 3,
        ["Ô₁ and AÊB stand on the same chord: which one is at the centre and which at the circumference?", "How are those two angles "
                                                                                                             "related?"], marks=2),
    mcq("9.1.2", "Determine the size of Ô₂." + ANSWER, ["Ô₂ = 78° [equal chords; equal ∠s]", "Ô₂ = 39° [equal chords; equal ∠s]",
                                                       "Ô₂ = 78° [vert opp ∠s]", "Ô₂ = 102° [∠s on a str line]"], 0,
        ["Ô₂ stands on chord DC: what do you know about DC and AB?", "What can you say about the angles that two such chords subtend at "
                                                                     "the centre?"], marks=2, after=["9.1.1"]),
]
q92 = [
    work("9.2", "Determine the value of x.", 4, [
        "x − 8° = 2(2x − 40°) " + CEN + "\n4x − 80° = x − 8°\n3x = 72°\nx = 24°",                         # RŜT itself, not the reflex PŜR
        "180° − (x − 8°) = 2(2x − 40°) " + CEN + "\n4x − 80° = 188° − x\n5x = 268°\nx = 53,6°",            # the angle PŜR that is not reflex
        "x − 8° + 180° = 2(2x − 40°) " + CEN + "\n4x − 80° = 172° + x\n3x = 252°\nx = 84°",                # the memo (OR join TR)
        "x − 8° + 180° = 2(2x − 40°) [opp ∠s of cyclic quad]\n4x − 80° = 172° + x\n3x = 252°\nx = 84°"], 2,  # the wrong reason
        ["PQ̂R stands on an arc: which angle at the centre S stands on the same arc?", "PST is a straight line: how big is that angle at S in "
                                                                                       "terms of x?"]),
]
q93 = [
    work("9.3", "Show that the length of BD is 2x(√5 − 1) units.", 5, [
        "AB = BC = 4x [line from centre to midpt of chord]\n" + B93 + "BD = 2√5 x − 2x = 2x(√5 − 1)",       # the converse: assumes B is the midpoint
        "AB = BC = 4x [line from centre ⊥ to chord]\n" + B93 + "BD = 2√5 x − 2x = 2x(√5 − 1)",              # the memo
        "Let BD = 2x(√5 − 1) [given]\nOD = OB + BD = 2√5 x\nOA = OD = 2√5 x [radii]\nAB² = OA² − OB² = 20x² − 4x² = 16x² [Pythagoras]\n"
        "AB = 4x = {1}/{2}AC, so BD = 2x(√5 − 1)",                                                         # starts from the answer
        "AB = BC = 4x [line from centre ⊥ to chord]\n" + B93 + "BD = OB − OD = 2x − 2√5 x = 2x(√5 − 1)"], 1,  # OB − OD: the sign dropped
        ["What does a line from the centre perpendicular to a chord do to the chord?", "Which side of right-angled △OBA is a radius, and "
                                                                                       "how does that radius compare with OD?"]),
]

# ---- QUESTION 10, the question paper pages 14-15 and the memo pages 24-25 ----
CON = "Construction: draw radii OR and OT (Ô₁ towards P, Ô₂ towards S)\nLet Ŝ = x and P̂ = y\n"
O12 = "Ô₁ = 2Ŝ = 2x " + CEN + "\nSimilarly Ô₂ = 2P̂ = 2y\n"
END = "x + y = 180°, so Ŝ + P̂ = 180°"
MS = "M̂₁ = Ŝ₁ = 48°\n∴ ST is a tangent to circle MNS "
q101 = [
    work("10.1", "Prove the theorem that states that P̂ + Ŝ = 180°.", 5, [
        CON + O12 + "2x + 2y = 360° [∠s round a point]\n" + END,                                            # the memo
        CON + O12 + "x + y = 180° [opp ∠s of cyclic quad]\n∴ Ŝ + P̂ = 180°",                                 # the theorem used to prove itself
        CON + O12 + "2x + 2y = 360° [∠s on a str line]\n" + END,                                            # the wrong reason
        CON + "Ô₁ = 2Ŝ = 2x [∠s round a point]\nSimilarly Ô₂ = 2P̂ = 2y\n2x + 2y = 360° " + CEN + "\n" + END], 0,   # the two reasons swapped
        ["Which construction lets you use angles at the centre O?", "What do the two angles at O, on either side of the radii you drew, add "
                                                                    "up to?"]),
]
q102 = [
    work("10.2.1(a)", "Determine, with reasons, the size of: Q̂₁", 3, [
        "PQ̂N = Ŝ₁ = 48° [∠s in the same seg]\nQ̂₁ = Q̂₂ = 24° [QS bisects PQ̂N]",              # the wrong reason
        "PQ̂N = 180° − 48° = 132° [opp ∠s of cyclic quad]\nQ̂₁ = Q̂₂ = 66° [QS bisects PQ̂N]",   # Ŝ₁ taken as an angle inside PQNS
        "Q̂₁ = Ŝ₁ = 48° [ext ∠ of cyclic quad]\nQ̂₂ = Q̂₁ = 48° [QS bisects PQ̂N]",             # the exterior angle set equal to Q̂₁ alone
        "PQ̂N = Ŝ₁ = 48° [ext ∠ of cyclic quad]\nQ̂₁ = Q̂₂ = 24° [QS bisects PQ̂N]"], 3,         # the memo
        ["Ŝ₁ lies outside cyclic quadrilateral PQNS: which angle inside it does Ŝ₁ equal?", "QS splits PQ̂N into Q̂₁ and Q̂₂: how do they "
                                                                                             "compare?"]),
    mcq("10.2.1(b)", "Determine, with reasons, the size of: R̂" + ANSWER, ["R̂ = 48° [∠s in the same seg]", "R̂ = 24° [∠s in the same seg]",
                                                                        "R̂ = 24° [vert opp ∠s]", "R̂ = 12° " + CEN], 1,
        ["Which chord do R̂ and Q̂₁ both stand on?", "Are R and Q on the same side of that chord?"], marks=2, after=["10.2.1(a)"]),
    mcq("10.2.1(c)", "Determine, with reasons, the size of: M̂₁" + ANSWER, ["M̂₁ = 48° [alt ∠s; PQ ∥ SR]", "M̂₁ = 24° [corresp ∠s; PQ ∥ SR]",
                                                                         "M̂₁ = 48° [corresp ∠s; PQ ∥ SR]", "M̂₁ = 132° [co-int ∠s; PQ ∥ SR]"], 2,
        ["Which pair of parallel lines does QN cross?", "Which angle at Q sits in the matching position to M̂₁?"], marks=2,
        after=["10.2.1(a)"]),
    work("10.2.2", "Prove that ST is a tangent to the circle passing through M, N and S.", 2, [
        MS + "[tan ⊥ radius]",                                                                 # the wrong reason
        MS + "[tan chord theorem]",                                                            # the theorem, not its converse
        MS + "[converse tan chord theorem]",                                                   # the memo
        "PQ̂N = Ŝ₁ = 48°\n∴ ST is a tangent to circle MNS [converse tan chord theorem]"], 2,    # an angle of the big circle, not of MNS
        ["Which angle between ST and a chord of circle MNS is given?", "Which angle in the alternate segment of that circle should it equal?"],
        after=["10.2.1(a)", "10.2.1(c)"]),
]

# ---- QUESTION 11, the question paper page 16 and the memo pages 26-28 ----
T1 = "T̂₁ = x [tan chord theorem]\n"
P2 = "P̂₂ = 90° − x [tan ⊥ diameter]\nR̂₂ = 90° − x [∠s opp equal sides]\n"
R1 = "R̂₁ = 90° − x [sum of ∠s in △]\n∴ R̂₁ = R̂₂: PR bisects OR̂N"
O2X = "Ô₁ = 2x " + CEN + "\n"
S2 = "Ŝ₂ = 90° [line from centre ⊥ to chord]\n"
q11 = [
    work("11.1", "Prove that PR bisects OR̂N.", 5, [
        # (not "∠ in semi-circle": RP̂T = 90° with P̂₃ = x is the memo's OR route to the same P̂₂, so that reason is not clearly false)
        T1 + O2X + "P̂₂ = 90° − x [tan chord theorem]\nR̂₂ = 90° − x [∠s opp equal sides]\n" + R1,    # the wrong reason for P̂₂
        T1 + O2X + P2 + R1,                                                                         # the memo, with its OR's R̂₁ line
        T1 + O2X + P2 + "R̂₁ = R̂₂ = 90° − x [PR bisects OR̂N]\n∴ PR bisects OR̂N",                     # assumes what it proves
        T1 + "Ô₁ = {1}/{2}x " + CEN + "\n" + P2 + R1], 1,                                           # the theorem turned round
        ["Which radius meets the tangent NP at P, and at what angle?", "Which two angles of △ORP are equal, and why?"]),
    work("11.2", "Prove that RÔS = PÂT.", 5, [
        "PÂT = 90° + x [opp ∠s of cyclic quad]\n" + S2 + "RÔS = 90° + x [ext ∠ of △]\n∴ RÔS = PÂT",                # the memo (OR through Ô₂ = 90° − x)
        "PÂT = 90° + x [ext ∠ of cyclic quad]\n" + S2 + "RÔS = 90° + x [ext ∠ of △]\n∴ RÔS = PÂT",                # the wrong reason
        "PÂT = 90° + x [opp ∠s of cyclic quad]\nŜ₂ = 90° [tan ⊥ radius]\nRÔS = 90° + x [ext ∠ of △]\n∴ RÔS = PÂT",  # PT is not a tangent
        "PÂT = 90° + x [opp ∠s of cyclic quad]\nRÔS = PÂT [ext ∠ of cyclic quad]\n" + S2 + "∴ RÔS = PÂT"], 0,     # no cyclic quad holds RÔS
        ["RTAP is a cyclic quadrilateral: which of its angles is opposite PÂT?", "RÔS lies outside △OST: how is it related to the angles "
                                                                                 "inside that triangle?"], after=["11.1"]),
]

REASONS = "Give reasons for your statements and calculations in QUESTIONS 9, 10 and 11."
# (no caption names a reading, a coordinate, a length, an angle size, a range or a type that a question asks for: captions show in the
# enlarged figure view and to screen readers)
missions = [
    {"id": "1", "title": "Question 1", "kind": "Mean and standard deviation", "marks": 10,
     "lead": "A school held a sports day. One of the items on the programme was an obstacle race. Teams of 10 parents and learners "
             "participated in this race. The table below shows the time taken, in minutes, by each member of a particular team to complete "
             "the race.\n\n4   12   13   16   17   18   20   22   22   25", "items": q1},
    {"id": "2.1", "title": "Question 2.1", "kind": "Ogive and frequency polygon", "marks": 10,
     "lead": "A survey was conducted of the ages of players at a soccer tournament. The results are shown in the cumulative frequency graph "
             "(ogive) below.",
     "figure": fig("Q2.1", "Cumulative frequency graph of the ages of soccer players: Cumulative frequency (0 to 50, labelled every 10) up "
                   "the side and Ages of soccer players (0 to 40, labelled every 5) along the bottom, on a fine grid. Dots mark the plotted "
                   "points at the ends of the classes; the smooth curve through them starts on the age axis, rises slowly, then steeply, "
                   "then levels off at the top right."), "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Five-number summaries", "marks": 3,
     "lead": "Two Grade 11 Mathematics classes have the same number of learners. The five-number summaries of the marks obtained by these "
             "classes for a test are shown below.\n\nCLASS A   (30 ; 48 ; 65 ; 82 ; 90)\nCLASS B   (50 ; 58 ; 65 ; 75 ; 90)\n\nThe parents of "
             "learners in CLASS A and CLASS B observe that both classes have the same median and the same maximum mark and therefore claim "
             "that there is no difference in the performance between these classes.", "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Lines and a quadrilateral", "marks": 19,
     "lead": "In the diagram, A(−2 ; 2), B(6 ; 5), C(0 ; −3) and D(x ; y) are the vertices of a quadrilateral having AD ∥ BC. BA produced "
             "has an x-intercept at E. BD and AC intersect at M. N(t ; 0) is a point on AD.",
     "figure": fig("Q3", "Axes with origin O; as printed, the vertical axis carries the label x and the horizontal axis the label y. "
                   "Quadrilateral ABCD: A(−2 ; 2) above the horizontal axis to the left of O, B(6 ; 5) at the top right, C(0 ; −3) on the "
                   "vertical axis below O and D(x ; y) at the bottom left. AD and BC carry arrows. BA is produced down to the left and cuts "
                   "the horizontal axis at E; AD cuts it at N(t ; 0). The diagonals AC and BD cross at M."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Inclination and a triangle", "marks": 12,
     "lead": "In the diagram, F(2 ; −2), G(5 ; 2) and C(6 ; y) are the vertices of △FGC. FG ⊥ FC. N is a point on FG such that the "
             "inclination of NC is 104,04°.\nThe angle of inclination of FG is β and FN̂C = θ.",
     "figure": fig("Q4", "Axes with origin O. Triangle FGC: F(2 ; −2) just below the x-axis with a right angle marked at F, G(5 ; 2) above "
                   "the x-axis to the upper right and C(6 ; y) far below to the lower right. FG crosses the x-axis, where the angle β is "
                   "marked between the x-axis and FG. N lies on FG above the x-axis; NC crosses the x-axis, where an arc marks 104,04° from "
                   "the x-axis round to NC. θ is marked at N, between NF and NC."), "items": q4},
    {"id": "5.1", "title": "Question 5.1", "kind": "Ratios on the Cartesian plane", "marks": 10,
     "lead": "In the diagram below, T(x ; 15) is a point in the Cartesian plane such that OT = 17 units. P(−2 ; a) lies on OT. K is a point "
             "on the positive x-axis and TÔK = θ.\n\nDetermine, with the aid of the diagram, the following:",
     "figure": fig("Q5.1", "Axes with origin O. A line runs from O up to the left through P(−2 ; a) to T(x ; 15). K is a point on the "
                   "positive x-axis. The angle θ is marked by an arc that turns anticlockwise from OK round to OT."), "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Reduction formulae", "marks": 7, "items": q52},
    {"id": "5.3", "title": "Question 5.3", "kind": "Trigonometric identities", "marks": 5, "items": q53},
    {"id": "5.4", "title": "Question 5.4", "kind": "General solutions", "marks": 6, "items": q54},
    {"id": "6", "title": "Question 6", "kind": "Trigonometric graphs", "marks": 11,
     "lead": "The graphs of the functions f(x) = a cos bθ and g(x) = c tan θ for x ∈ [−180° ; 180°] are sketched below. The graphs intersect "
             "at P(58° ; 1,6) and Q.",
     "figure": fig("Q6", "The graphs of f and g from x = −180° to x = 180°, on a grid with vertical lines every 45° (labelled −180°, −90°, "
                   "0°, 90° and 180°) and horizontal lines at y = −3, −2, −1, 1, 2 and 3. f is a smooth wave. g has dashed vertical "
                   "asymptotes at x = −90° and x = 90° and a branch between each pair of them. The graphs cross at P, labelled (58° ; 1,6), "
                   "and at Q, lower down to the right. K on f and M on g are joined by a vertical segment to the left of the y-axis."),
     "items": q6},
    {"id": "7.1", "title": "Question 7.1", "kind": "Solving a triangle", "marks": 3,
     "lead": "In the diagram, P̂ = 67°, PQ = 3 cm and PR = 9,2 cm.",
     "figure": fig("Q7.1", "Triangle PQR with P at the top, Q at the bottom left and R at the bottom right. The angle at P is marked 67°, PQ "
                   "is marked 3 cm and PR 9,2 cm."), "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Lengths and areas in triangles", "marks": 10,
     "lead": "In the diagram below, DĈB = α, AC = h units and AĈB = θ.",
     "figure": fig("Q7.2", "Triangle ABC with C at the bottom left, B at the bottom right with a right angle, and A directly above B. D lies "
                   "on AB between A and B, and CD is drawn. AC is marked h. At C, α is marked between CB and CD, and θ between CB and CA. "
                   "At D, angle 1 lies between DA and DC, and angle 2 between DC and DB."), "items": q72},
    {"id": "8", "title": "Question 8", "kind": "Volume and surface area", "marks": 7,
     "lead": "The diagram below shows a cone with a perpendicular height of h cm, a radius of r cm and a slant height of 13 cm.\n\nVolume of "
             "cone = (1/3)πr²h\nTotal surface area of the cone = πr² + πrs",
     "figure": fig("Q8", "A cone. Its perpendicular height h is drawn dashed from the apex down to the centre of the base, with a right "
                   "angle where it meets the radius r, drawn dashed to the edge of the base. The slant height is marked 13 cm."),
     "items": q8},
    {"id": "9.1", "title": "Question 9.1", "kind": "Angles in a circle", "marks": 4,
     "lead": REASONS + " In the figure, O is the centre of the circle. A, B, C, D and E lie on the circle such that chord AB and chord DC are "
                       "equal in length and AÊB = 39°.",
     "figure": fig("Q9.1", "A circle with centre O. A (left), B (bottom), C (right), D (top right) and E (top left) lie on the circle. "
                   "Chords EA, EB, AB and DC are drawn; AB and DC carry the same double tick mark. Radii OA, OB, OC and OD are drawn. AÊB is "
                   "marked 39°. Ô₁ lies between OA and OB, and Ô₂ between OC and OD."), "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Angles and a diameter", "marks": 4,
     "lead": REASONS + " In the diagram, S is the centre of circle PQRT. PT is a diameter.\nRŜT = x − 8° and PQ̂R = 2x − 40°.",
     "figure": fig("Q9.2", "A circle with centre S. The diameter PT runs from P on the left to T on the right. Q (lower left) and R (bottom) "
                   "lie on the circle. Chords PQ and QR and the radius SR are drawn. PQ̂R is marked 2x − 40° and RŜT is marked x − 8°."),
     "items": q92},
    {"id": "9.3", "title": "Question 9.3", "kind": "Chords and radii", "marks": 5,
     "lead": REASONS + " In the diagram, O is the centre of the circle. Chord AC is perpendicular to radius OD at B. OB = 2x units and AC = 8x "
                       "units.",
     "figure": fig("Q9.3", "A circle with centre O. The chord AC runs from A (lower left) to C (right). The radius OD runs down to D on the "
                   "circle and crosses AC at B, where a right angle is marked. OA and OC are drawn."), "items": q93},
    {"id": "10.1", "title": "Question 10.1", "kind": "Cyclic quadrilateral proof", "marks": 5,
     "lead": REASONS + " In the diagram below, O is the centre of the circle and PTSR is a cyclic quadrilateral.",
     "figure": fig("Q10.1", "A circle with its centre O marked by a dot. The cyclic quadrilateral PTSR: P at the top, T on the right, S at the "
                   "bottom and R on the left, with the sides PT, TS, SR and RP drawn."), "items": q101},
    {"id": "10.2", "title": "Question 10.2", "kind": "Diameters and parallel chords", "marks": 9,
     "lead": REASONS + " In the figure, QS and PR are diameters of the circle with centre O such that PQ ∥ SR. PS is produced to T. N is a "
                       "point on the circle such that Q̂₁ = Q̂₂. SN is drawn.\nRS intersects QN at M. Ŝ₁ = 48°",
     "figure": fig("Q10.2", "A circle with centre O. The diameter QS runs across, Q on the left and S on the right; the diameter PR runs from P "
                   "at the top to R at the bottom left. PQ and SR carry arrows. N lies on the circle at the bottom, to the right of R. QN is "
                   "drawn and cuts RS at M. PS is produced beyond S to T, and SN is drawn; Ŝ₁ = 48° is marked between SN and ST. Angles are "
                   "numbered: Q̂₁ between QP and QS, Q̂₂ between QS and QN; at S, Ŝ₄ between SP and SQ, Ŝ₃ between SQ and SR, Ŝ₂ between SR "
                   "and SN, Ŝ₁ between SN and ST; at M, M̂₂ between MQ and MS, M̂₁ between MS and MN, M̂₃ between MR and MQ."),
     "items": q102},
    {"id": "11", "title": "Question 11", "kind": "Two touching circles", "marks": 10,
     "lead": REASONS + " O is the centre of the larger circle RTAP. OP is the diameter of the smaller circle PSO. NP is a tangent to both "
                       "circles at P. RN ⊥ NP.\nLet P̂₁ = x.",
     "figure": fig("Q11", "Two circles that touch at P, at the bottom: the larger circle RTAP with centre O, and a smaller circle through P, S "
                   "and O with OP as its diameter (its own centre marked on OP). R (left), T (upper right) and A (right) lie on the larger "
                   "circle; RT passes through O. S lies on the smaller circle, on PT. NP is the common tangent at P, and RN ⊥ NP with the "
                   "right angle at N. RP, OP, PT, PA, TA and OS are drawn. P̂₁ = x is marked between PN and PR. Angles are numbered: R̂₁ "
                   "between RN and RP, R̂₂ between RP and RO; Ô₁ between OR and OP, Ô₂ between OP and OS, Ô₃ between OS and OT; Ŝ₁ between "
                   "SP and SO, Ŝ₂ between SO and ST; T̂₁ between TO and TP, T̂₂ between TP and TA; at P, P̂₂ between PR and PO, P̂₃ between "
                   "PO and PS, P̂₄ between PS and PA."), "items": q11},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.2", "1.4", "1.5", "2.1.2", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "4.1", "4.2", "4.3", "4.4", "5.1.1",
                           "5.1.3", "5.1.4", "5.1.5", "5.2", "5.3", "5.4", "6.5", "7.1", "7.2.2", "7.2.3", "7.2.4", "8.1", "8.2", "9.2", "9.3",
                           "10.1", "10.2.1(a)", "10.2.2", "11.1", "11.2"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["2.1.3", "5.1.2", "6.1", "6.3", "6.4", "6.6", "7.2.1", "9.1.1", "9.1.2", "10.2.1(b)", "10.2.1(c)"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric", "term", "match")], "a typed calculation, written answer, term or sort left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["1.1", "1.3", "2.1.1", "6.2"]   # the one-number answers
assert all(i["a"] >= 0 for i in ITEMS if i["t"] == "num"), "a signed answer belongs in a multiple choice (the keypad's sign)"
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.1.4"]
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn"]
assert PICKS == ["2.2"], PICKS
for _m in missions:   # a gate names an EARLIER part of its own mission (the app looks a gate up inside the mission)
    _order = [i["n"] for i in _m["items"]]
    for _i in _m["items"]:
        assert all(e in _order[:_order.index(_i["n"])] for e in _i.get("after", [])), (_i["n"], "a gate outside its mission or later")
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
GATES = {i["n"]: i["after"] for i in ITEMS if i.get("after")}

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2018", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines and every proof plays as four workings, the memo's FIRST method line by line (a "
                                                       "geometry statement with its [reason]) and three built from real errors (a wrong formula, "
                                                       "ratio, identity or theorem, a sign slip, a misread value, the wrong side, pair of lines or "
                                                       "quadrant, a wrong reason, circular reasoning, one value tried, the calculator in "
                                                       "radians), 0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, %d marks). In a proof or "
                                                       "'show that' every option ends in the given result. The memo's OR methods and values (3.1 "
                                                       "B − C, 3.2 y − y₁ = m(x − x₁), 3.6 AD = BC with AD ∥ BC and the diagonals' common "
                                                       "midpoint, 4.2 m(FC) × m(FG) = −1, 5.1.5 the line y = −15/8 x, 5.3 two other routes, 5.4 "
                                                       "x = 180°.k and ±48,19° + 360°.k, 7.2.4 through CD: 47,71, 9.2 joining TR, 11.1 two other "
                                                       "routes, 11.2 through Ô₂ = 90° − x) are other right routes and never a wrong option; 3.6's "
                                                       "wrong option with the reason 'diagonals bisect each other' shows only the gradients, from "
                                                       "which that reason does not follow. The memo's one-line 1.2 (169/10 = 16,9) and 2.1.2 "
                                                       "(40 − 10 = 30) are set as two lines; 10.1's construction line adds which angle Ô₁ and Ô₂ "
                                                       "are (the memo's diagram shows it, the paper's does not)." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "2.1.3", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                   "with no working (the frequency column, tan θ, a range, a and b, coordinates, an equation of a "
                                                   "graph, AĈD in θ and α, an angle with its one reason): four options, the memo's answer and three "
                                                   "common errors, 0 or full marks. 2.1.3 loses the memo's 1 and 2 marks for two and three correct "
                                                   "values; 6.1 its split end points / notation (its OR y ∈ [−3 ; 3] is the right option's "
                                                   "interval and no wrong option); 6.3, 6.4 and 6.6 their split a / b, x / y and 3 / −45°; 9.1.1, "
                                                   "9.1.2, 10.2.1(b) and 10.2.1(c) their split statement / reason marks. 2.1.3's table (its "
                                                   "FREQUENCY column blank in the answer book) is typed into the stem, which shows the total 50, "
                                                   "so it opens after 2.1.1."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from the page images of a SCANNED "
                                                           "question paper, memo and answer book (no text layer in any of them); no API call."},
        {"n": "1.1", "kind": "no_fit", "detail": "One-number answers with no working stay typed on the keypad: 1.1 (4 minutes), 1.3 (σ = 5,79: keyed "
                                                 "at two decimal places, tolerance 0,006, so the sample standard deviation 6,10 is marked wrong), "
                                                 "2.1.1 (50 players) and 6.2 (c = 1)."},
        {"n": "2.1.4", "kind": "no_fit", "detail": "The frequency polygon (2.1.4) is drawn on paper and self-checked against the memo's four "
                                                   "criteria; the answer book's blank grid is described in the memo text, not cropped."},
        {"n": "2.2", "kind": "no_fit", "detail": "The choice with its two arguments plays as statements, 1 mark each: the memo's 'not valid' and its "
                                                 "two arguments (the bigger range of class A; at least 25% of class A below every mark of class B), "
                                                 "and four cards that are false for these summaries (the claim valid, IQR A = 34 > IQR B = 17, "
                                                 "the minimum of B is higher, Q₃ of B is lower)."},
        {"n": "1.4", "kind": "no_fit", "detail": "A part whose stem, options, cards or criteria show an earlier part's answer opens only once that "
                                                 "part is answered ('after'): " + "; ".join(k + " after " + " and ".join(v) for k, v in GATES.items())
                                                 + ". 1.2's wrong option (4 + 25)/2 shows 1.1's fastest time; 6.3's a = 3 shows 6.1's range."},
        {"n": "3", "kind": "memo_issue", "detail": "The question paper's diagram (page 6), as the answer book's (page 5), labels the vertical axis x "
                                                   "and the horizontal axis y; the memo's diagram (page 5) labels them y and x, as the stem's "
                                                   "coordinates and 'BA produced has an x-intercept at E' need. The figure is the paper's; its "
                                                   "caption names the swapped labels."},
        {"n": "6", "kind": "memo_issue", "detail": "The paper prints f(x) = a cos bθ and g(x) = c tan θ for x ∈ [−180° ; 180°], θ where x is meant "
                                                   "(the graph's axis is x); kept as printed in the lead. The memo's 6.6 answer f(x) = 3cos(θ − 45°) "
                                                   "is written f(x) = 3 cos(x − 45°) in the options."},
        {"n": "7.1", "kind": "memo_issue", "detail": "The answer book's triangle (page 13) marks the 67° at Q; the question paper (page 10), its stem "
                                                     "(P̂ = 67°) and the memo put it at P. The figure is the question paper's."},
        {"n": "7.2", "kind": "memo_issue", "detail": "The memo (page 19) prints [28] at the end of Question 7 (Question 5's total); its parts "
                                                     "(3 + 1 + 4 + 2 + 3) and the paper give 13, which is played."},
        {"n": "11.1", "kind": "memo_issue", "detail": "The memo's first method (page 26) goes from R̂₂ = 90° − x straight to ∴ R̂₁ = R̂₂; its OR "
                                                      "methods (page 27) give R̂₁ = 90° − x [sum of ∠s in △]. The right option adds that line."},
        {"n": "11.2", "kind": "memo_issue", "detail": "The memo (page 27) gives Ŝ₂ = 90° the reason 'line from centre ⊥ to chord'; the 90° itself "
                                                      "comes from the angle in a semi-circle (OP is the diameter of circle PSO, so Ŝ₁ = 90°). The "
                                                      "right option keeps the memo's reason, and no wrong option uses '∠ in semi-circle'."},
        {"n": "3.6", "kind": "memo_issue", "detail": "The memo's first OR (page 7) writes AD = √((−2 − (−8))² + (2 − 6)²) where (2 − (−6))² is meant "
                                                     "(its √100 = 10 is right). The OR is not played."},
        {"n": "9.2", "kind": "memo_issue", "detail": "The memo's diagram (page 22) labels P as A; its working uses the paper's letters."},
    ],
}
QTOTAL = {"1": 10, "2": 13, "3": 19, "4": 12, "5": 28, "6": 11, "7": 13, "8": 7, "9": 13, "10": 14, "11": 10}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
assert per_q == QTOTAL, per_q
# the right letter (no printed multiple choice in this paper, so every letter is ours): the 36 authored workings as even as 36 allows
# (9 each: the brief's 3-7 band is for fewer workings), the 11 answer MCQs within 1 of even, and the whole paper within 1
worked = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(worked.values()) - min(worked.values()) <= 1 and min(worked.values()) >= 3, worked
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert len(four) == len([i for i in ITEMS if i["t"] == "mcq"]) and max(fspread.values()) - min(fspread.values()) <= 1, fspread
print("right options, authored workings:", worked, "four-option:", fspread)
print("statement right-card positions:", {i["n"]: i["pool"] for i in ITEMS if i["t"] == "pickn"})
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts; gated:", len(GATES))
print("total:", total)
# every gate, in full: a gate dropped by a helper or an edit fails the run before anything is written
assert GATES == {
    "1.2": ["1.1"],                         # a wrong option's (4 + 25)/2: the fastest time
    "1.4": ["1.2", "1.3"],                  # x̄ = 16,9 and σ = 5,79
    "1.5": ["1.2"],                         # the total 169
    "2.1.3": ["2.1.1"],                     # the stem's table ends at 50
    "2.1.4": ["2.1.3"],                     # its criteria: the frequencies
    "3.2": ["3.1"],                         # m(BC) = 4/3
    "3.3": ["3.2"], "3.5": ["3.2"],         # y = 4/3 x + 14/3
    "3.4": ["3.3"],                         # t = −7/2
    "3.6": ["3.1"],                         # a wrong option's m(BC) = 4/3
    "4.2": ["4.1"], "4.3": ["4.1"],         # m(FG) = 4/3
    "4.4": ["4.2", "4.3"],                  # y = −5 and θ = 50,91°
    "5.1.2": ["5.1.1"], "5.1.3": ["5.1.1"], "5.1.4": ["5.1.1"],   # x = −8
    "5.1.5": ["5.1.1", "5.1.2"],            # tan θ = 15/−8
    "6.3": ["6.1"],                         # a = 3 shows the range
    "6.5": ["6.3"], "6.6": ["6.3"],         # a = 3 and b = 1
    "7.2.2": ["7.2.1"], "7.2.3": ["7.2.1"],   # θ − α
    "7.2.4": ["7.2.3"],                     # AD = 10,59
    "9.1.2": ["9.1.1"],                     # Ô₁ = 78°
    "10.2.1(b)": ["10.2.1(a)"],             # R̂ = Q̂₁ = 24°
    "10.2.1(c)": ["10.2.1(a)"],             # M̂₁ = PQ̂N = 48°
    "10.2.2": ["10.2.1(a)", "10.2.1(c)"],   # M̂₁ = 48° and a wrong option's PQ̂N = 48°
    "11.2": ["11.1"]}, GATES                # PÂT = 90° + x from R̂₂ = 90° − x; T̂₁ = x
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's, memo's and answer book's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
