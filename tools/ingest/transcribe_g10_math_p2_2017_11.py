"""Grade 10 Mathematics P2 Nov 2017 (DBE common paper), the whole paper (Questions 1 to 9, 100 marks: statistics, analytical geometry,
trigonometry, measurement, Euclidean geometry), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`
like any ingested paper. Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and
figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not). The question paper and the answer
book are SCANS (no text layer) and the memo's text layer garbles fractions, roots and angle names: everything was read from the page
images rendered at 150 dpi, with crops at 200-250 dpi where a number, an exponent or an angle label mattered (Question 1's data,
4.1 and 4.3, Question 5, the Question 6 diagram, the memo's Question 8, the answer book's number line and grid).

  python tools/ingest/transcribe_g10_math_p2_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Mathematics P2 Nov 2017 Eng.pdf" "uploads/Grade 10 Mathematics P2 Nov 2017 MG Afr & Eng.pdf" --id g10-math-p2-2017-11 --from-json --answer-book "uploads/Grade 10 Mathematics P2 Nov 2017 Answer Book Afr & Eng.pdf"

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p2_2025_11.py, and the Grade 10 papers
transcribe_g10_math_p2_2018_11.py and transcribe_g10_math_p1_2017_11.py):
  every part the memo WORKS OUT in two or more lines (a range, an interquartile range, a mean, a percentage, a distance, a midpoint,
  a gradient test, a trigonometric value or equation, a length, an angle, a radius, an area) and every geometry proof -> authored
  whole-working multiple choice, `work`: the memo's FIRST method line by line (a geometry statement with its [reason] at the line's
  end, "{a}/{b}" a stacked fraction) and three workings each built from a DIFFERENT real error (a wrong ratio, formula or theorem, a
  sign slip, a misread value, the wrong side, pair of segments or quadrant, a wrong reason, circular reasoning, the calculator in
  radians), every option of a part the same layout (`shape`), the right one's place spread over A-D across the paper; the part
  keeps its marks, all or nothing. The memo's OR methods are other right routes and never a wrong option.
  An answer the memo states with no working (the modal class, a range, Ô₁ with its reason) -> authored multiple choice of answers:
  the memo's and three common errors. One number with no working (1.1 the median, 2.1, 5.2.1, 5.3.1, 6.1) stays num; the box and
  whisker diagram 1.4 -> draw with build "boxplot" (2026-10-11: the five values placed on the answer book's number line, the box
  and whiskers drawn from them, marked online against the memo's three ticks); the sketch 5.1 -> draw with build "sketch" (2026-10-11:
  f and g placed on the answer book's grid, each curve drawn through its features, marked online against the memo's six
  criteria); 3.5 (the type of quadrilateral and its reason) -> statements, pick 2; 5.3.2, where the memo's answer leaves out a
  solution, -> a pick of one with both right
  (Murci's memo-slip ruling, 2026-10-10).
  Where a part's options, cards or criteria show an EARLIER part's answer it carries "after" (the GATES assert below).
Missions: Questions 1, 2, 3, 5, 6, 7 and 9 share one stem (and diagram or table) each, so each is one mission; Questions 4 and 8
change their stem part-way, so their numbered groups are missions (4.1, 4.2, 4.3, 8.1, 8.2, 8.3).
No figure comes from the answer book: its number line (1.4) and grid (5.1) are blank answer spaces (the draw memos describe them;
1.4's box and whisker diagram is built on the same line, 5.1's sketch on the same grid), and its other diagrams repeat the
question paper's.
Figure boxes are measured in PDF points (page 595 x 841, read from the PDF) from the ink on the scan (scratch tool
lower/g10-math-p2-2017-11/figs.py) and checked on a contact sheet with ingest's 1% pad applied."""
import json
import random
import re
from pathlib import Path

PID = "g10-math-p2-2017-11"
W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q3": [4, 129.9, 160.6, 462.0, 367.4],     # the axes and quadrilateral PQRS
    "Q6": [6, 182.5, 183.6, 406.2, 364.1],     # the pole RQ, the cables, the 47° and θ
    "Q7": [7, 89.1, 196.5, 274.9, 472.0],      # the hemisphere on the cone (the formula box is typed in the lead)
    "Q8.1": [8, 132.2, 185.3, 449.0, 400.3],   # rhombus KLMN
    "Q8.2": [8, 114.1, 543.6, 483.2, 709.7],   # parallelogram PQRS
    "Q8.3": [9, 106.2, 148.2, 450.8, 392.5],   # parallelograms ABCD, DECF and FGCH
    "Q9": [10, 232.6, 157.1, 394.3, 414.9]}    # △ABC with G, F, H and E


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
IQR = "IQR = Q₃ − Q₁\n"
q1 = [
    num("1.1", "Determine the median of the number of laptops sold.", 54, 0, "laptops",
        ["What must you do to the data before you can find its middle value?", "With 15 values, which position is the middle one?"], marks=2),
    work("1.2", "Calculate the range of the data.", 2, [
        "Range = 78 − 43\n= 35",      # the last and first values as listed, not the largest and smallest
        "Range = 90 − 37\n= 53",      # the smallest value, 34, overlooked
        "Range = 90 − 34\n= 56",      # the memo
        "Range = 84 − 34\n= 50"], 2,  # the largest value, 90, overlooked
        ["Which is the largest number of laptops sold, and which is the smallest?", "How does the range compare those two values?"]),
    work("1.3", "Calculate the interquartile range (IQR).", 3, [
        IQR + "= 73 − 46\n= 27",       # the memo
        IQR + "= 70,5 − 47\n= 23,5",   # the median 54 put into both halves
        IQR + "= 68 − 52\n= 16",       # the halves taken from the data as listed, not in order
        IQR + "= 46 − 73\n= −27"], 0,  # Q₁ and Q₃ swapped
        ["Once the data is in order, which value is the middle of the lower half, and which the middle of the upper half?",
         "With 15 values, does the median belong to either half?"]),
    draw("1.4", "Draw a box and whisker diagram for the data above.", 3, [
        ["The whiskers: out to the minimum 34 and the maximum 90", 1], ["The median 54 marked inside the box", 1],
        ["The box: from Q₁ = 46 to Q₃ = 73", 1]],
        ["Which five numbers does a box and whisker diagram need?", "Where on the number line do the ends of the box and the line inside it "
                                                                    "go?"],
        memo="The answer book gives a number line from about 30 to 92, labelled 35 ; 40 ; … ; 90 with a tick at every whole number. "
             "Five-number summary: 34 ; 46 ; 54 ; 73 ; 90.", after=["1.1", "1.2", "1.3"],
        # built on the answer book's line (2026-10-11): the five values placed, the box and whiskers drawn from them, marked as the memo
        # marks it (✓ min. & max., ✓ median (Q₂), ✓ Q₁ and Q₃: the two values of a tick earn it only together)
        build={"kind": "boxplot", "x": [30, 95, 1], "tick": 1, "label": 5, "tol": 0,
               "at": {"min": 34, "q1": 46, "med": 54, "q3": 73, "max": 90},
               "crit": {"min": 0, "max": 0, "med": 1, "q1": 2, "q3": 2}}),
]
for i in q1:   # the built box and whisker diagram: every memo criterion is earned by its values, and each value sits on the line's steps
    b = i.get("build") or {}
    if b.get("kind") == "boxplot":
        assert sorted(set(b["crit"].values())) == list(range(len(i["criteria"]))), (i["n"], b["crit"])
        assert all(b["x"][0] <= u <= b["x"][1] and abs(u / b["x"][2] - round(u / b["x"][2])) < 1e-9 for u in b["at"].values()), (i["n"], b["at"])

# ---- QUESTION 2, the question paper page 3 and the memo page 3 ----
TEMPS = {"head": ["TEMPERATURE (IN °C)", "FREQUENCY"],
         "rows": [["20 ≤ T < 24", "2"], ["24 ≤ T < 28", "4"], ["28 ≤ T < 32", "9"], ["32 ≤ T < 36", "5"], ["36 ≤ T < 40", "7"],
                  ["40 ≤ T < 44", "3"]]}
PCT = "% of days = "
q2 = [
    num("2.1", "For how many days did the learner collect the data?", 30, 0, "days",
        ["What does each frequency count?", "How do the frequencies of all the classes together give the number of days?"]),
    mcq("2.2", "Write down the modal class for the data." + ANSWER, ["36 ≤ T < 40", "28 ≤ T < 32", "40 ≤ T < 44", "32 ≤ T < 36"], 1,
        ["Which class has the highest frequency?", "Is the modal class about the temperatures themselves or about how often they occur?"]),
    work("2.3", "Estimate the mean of the data.", 3, [
        "x̄ = {40 + 96 + 252 + 160 + 252 + 120}/{30}\n= {920}/{30}\n= 30,67 °C",     # each class's lower end for its midpoint
        "x̄ = {44 + 104 + 270 + 170 + 266 + 126}/{6}\n= {980}/{6}\n= 163,33 °C",      # divided by the number of classes
        "x̄ = {22 + 26 + 30 + 34 + 38 + 42}/{6}\n= {192}/{6}\n= 32 °C",               # the midpoints without their frequencies
        "x̄ = {44 + 104 + 270 + 170 + 266 + 126}/{30}\n= {980}/{30}\n= 32,67 °C"], 3,  # the memo
        ["What is the midpoint of each class, and on how many days does it count?", "What do you divide the total by?"], after=["2.1"]),
    work("2.4", "Calculate the percentage of days on which the temperature was at least 28 °C.", 2, [
        "5 + 7 + 3 = 15 days\n" + PCT + "{15}/{30} × 100\n= 50%",        # the class 28 ≤ T < 32 left out
        "9 + 5 + 7 + 3 = 24 days\n" + PCT + "{24}/{30} × 100\n= 80%",    # the memo
        "2 + 4 = 6 days\n" + PCT + "{6}/{30} × 100\n= 20%",              # 'at least' read as 'below'
        "9 + 5 + 7 = 21 days\n" + PCT + "{21}/{30} × 100\n= 70%"], 1,    # the class 40 ≤ T < 44 left out
        ["Which classes hold temperatures of 28 °C or more?", "How do you write a part of the total as a percentage?"], after=["2.1"]),
]

# ---- QUESTION 3, the question paper page 4 and the memo pages 3-4 ----
MQS = "M(QS) = "
MRS = "m(RS) = {3 − 1}/{0 − 1} = −2\n"
q3 = [
    work("3.1", "Calculate the length of PQ. Leave your answer in surd form.", 2, [
        "PQ = √((7 + 6)² + (4 + 6)²)\n= √((13)² + (10)²)\n= √269",   # a sign slip: adds the coordinates
        "PQ = (7 − 6)² + (4 − 6)²\n= (1)² + (−2)²\n= 5",             # the square root forgotten
        "PQ = √((7 − 4)² + (6 − 6)²)\n= √((3)² + (0)²)\n= 3",        # pairs each point's x with its own y
        "PQ = √((7 − 6)² + (4 − 6)²)\n= √((1)² + (−2)²)\n= √5"], 3,  # the memo
        ["Which formula gives the distance between two points?", "Do you subtract the x-values from each other and the y-values from each "
                                                                  "other?"]),
    work("3.2", "If T(7/2 ; 7/2) is the midpoint of QS, determine the coordinates of S.", 3, [
        MQS + "({6 + t}/{2} ; {6 + k}/{2}) = ({7}/{2} ; {7}/{2})\n{6 + t}/{2} = {7}/{2} and {6 + k}/{2} = {7}/{2}\nt = 1 and k = 1\n"
        "S(1 ; 1)",                                                                                          # the memo
        MQS + "({6 − t}/{2} ; {6 − k}/{2}) = ({7}/{2} ; {7}/{2})\n{6 − t}/{2} = {7}/{2} and {6 − k}/{2} = {7}/{2}\nt = −1 and k = −1\n"
        "S(−1 ; −1)",                                                                                        # subtracts in the midpoint
        MQS + "({6 + t}/{2} ; {6 + k}/{2}) = ({7}/{2} ; {7}/{2})\n6 + t = {7}/{2} and 6 + k = {7}/{2}\nt = −{5}/{2} and k = −{5}/{2}\n"
        "S(−{5}/{2} ; −{5}/{2})",                                                                            # never multiplied by 2
        MQS + "({7 + t}/{2} ; {4 + k}/{2}) = ({7}/{2} ; {7}/{2})\n{7 + t}/{2} = {7}/{2} and {4 + k}/{2} = {7}/{2}\nt = 0 and k = 3\n"
        "S(0 ; 3)"], 0,                                                                                      # P's coordinates for Q's
        ["Which formula gives the midpoint of QS from the coordinates of Q and S?", "What equation do you get when you set each coordinate "
                                                                                     "of that midpoint equal to the matching coordinate of T?"]),
    work("3.3", "If the coordinates of S are (1 ; 1), show that PR = QS.", 2, [
        "PQ = √((7 − 6)² + (4 − 6)²)\n= √5\nRS = √((0 − 1)² + (3 − 1)²)\n= √5\n∴ PR = QS",                    # two sides, not the diagonals
        "PR = √((7 + 0)² + (4 + 3)²)\n= √98 = 7√2\nQS = √((1 + 6)² + (1 + 6)²)\n= √98 = 7√2\n∴ PR = QS",      # a sign slip: adds the coordinates
        "PR = √((7 − 0)² + (4 − 3)²)\n= √50 = 5√2\nQS = √((1 − 6)² + (1 − 6)²)\n= √50 = 5√2\n∴ PR = QS",      # the memo
        "PR = (7 − 0)² + (4 − 3)²\n= 50\nQS = (1 − 6)² + (1 − 6)²\n= 50\n∴ PR = QS"], 2,                      # the square roots forgotten
        ["Which two segments are the diagonals of PQRS?", "Which formula gives each one's length?"], after=["3.1", "3.2"]),
    work("3.4", "Show that QR ⊥ RS.", 4, [
        "m(QR) = {6 − 0}/{6 − 3} = 2\nm(RS) = {0 − 1}/{3 − 1} = −{1}/{2}\nm(QR) × m(RS) = 2 × (−{1}/{2}) = −1\n∴ QR ⊥ RS",   # x over y
        "m(QR) = {6 − 3}/{6 − 0} = {1}/{2}\n" + MRS + "m(QR) × m(RS) = {1}/{2} × (−2) = −1\n∴ QR ⊥ RS",                    # the memo
        "m(QR) = {6 − 3}/{0 − 6} = −{1}/{2}\n" + MRS + "m(QR) × m(RS) = −{1}/{2} × (−2) = 1\n∴ QR ⊥ RS",                   # Q − R on top, R − Q below
        "m(QR) = {6 − 3}/{6 − 0} = {1}/{2}\n" + MRS + "m(QR) × m(RS) = {1}/{2} × (−2) = −1\n∴ QR ∥ RS"], 1,                # −1 read as parallel
        ["Which formula gives the gradient of a line through two points?", "What is the product of the gradients of two perpendicular "
                                                                            "lines?"], after=["3.2"]),
    # 1 + 1: the choice and its reason (the memo's own); the wrong cards are false for PQRS (PQ = √5, QR = √45; m(PR) = 1/7, m(QS) = 1).
    # With six (and seven) cards the seeded shuffle put "PQRS is a rectangle." first; the false "PQRS is a kite." (no two adjacent
    # sides are equal) and "Only one pair of its opposite sides is parallel." (m(PQ) = m(RS) = −2, m(QR) = m(PS) = 1/2) move it off the top
    stmt("3.5", "Hence, what type of special quadrilateral is PQRS? Motivate your answer.", 2,
         ["PQRS is a rectangle.", "Its diagonals are equal and one of its interior angles is 90°."],
         ["PQRS is a square.", "PQRS is a rhombus.", "Its diagonals bisect each other at right angles.", "All four of its sides are equal.",
          "PQRS is a kite.", "Only one pair of its opposite sides is parallel."],
         ["What did you show about the diagonals in 3.3, and about the angle at R in 3.4?", "Are all four sides of PQRS the same length?"], 1),
    work("3.6", "Calculate the size of RŜQ.", 3, [
        "sin RŜQ = {√5}/{5√2}\nRŜQ = 18,43°",   # sine for cosine
        "tan RŜQ = {√5}/{5√2}\nRŜQ = 17,55°",   # tangent for cosine
        "cos RŜQ = {√5}/{5√2}\nRŜQ = 1,25°",    # the calculator in radians
        "cos RŜQ = {√5}/{5√2}\nRŜQ = 71,57°"], 3,   # the memo
        ["In △QRS, where is the right angle, and which side is the hypotenuse?", "Which ratio links the side next to RŜQ with the hypotenuse?"],
        after=["3.1", "3.3"]),
]

# ---- QUESTION 4, the question paper page 5 and the memo pages 5-6 ----
SKETCH = "Use a sketch to determine the value of the following. DO NOT use a calculator.\n"
COT = "4 cot θ + 3 = 0\n"
SHOW = "∴ sin²θ − 1 = −cos²θ"
q41 = [
    work("4.1.1(a)", SKETCH + "cos θ", 4, [
        COT + "cot θ = −{3}/{4}\nθ in quadrant II: x = −4 and y = 3\nr = √((−4)² + 3²) = 5\ncos θ = −{4}/{5}",   # cot read as y/x
        COT + "cot θ = {3}/{4}\nθ in quadrant I: x = 3 and y = 4\nr = √(3² + 4²) = 5\ncos θ = {3}/{5}",          # the 3 moved across without its sign
        COT + "cot θ = −{3}/{4}\nθ in quadrant II: x = −3 and y = 4\nr = √((−3)² + 4²) = 5\ncos θ = −{3}/{5}",   # the memo
        COT + "cot θ = −{3}/{4}\nθ in quadrant II: x = −3 and y = 4\nr = 3 + 4 = 7\ncos θ = −{3}/{7}"], 2,       # r as x + y, not Pythagoras
        ["What is cot θ, and in which quadrant is θ if cot θ is negative and 0° < θ < 180°?", "Which values of x, y and r does that give?"]),
    work("4.1.1(b)", SKETCH + "(3 sin θ sec θ)/tan θ", 4, [
        "= 3({4}/{5})(−{5}/{3}) ÷ (−{4}/{3})\n= 3(−{4}/{3}) ÷ (−{4}/{3})\n= 3",       # the memo
        "= 3({4}/{5})({5}/{3}) ÷ (−{4}/{3})\n= 3({4}/{3}) ÷ (−{4}/{3})\n= −3",        # sec θ without its negative sign
        "= 3({4}/{5})({5}/{4}) ÷ (−{4}/{3})\n= 3(1) ÷ (−{4}/{3})\n= −{9}/{4}",        # sec θ taken as 1/sin θ
        "= 3({4}/{5})(−{5}/{3}) ÷ (−{3}/{4})\n= 3(−{4}/{3}) ÷ (−{3}/{4})\n= {16}/{3}"], 0,   # tan θ taken as x/y
        ["What are sin θ, sec θ and tan θ in terms of x, y and r?", "Can you simplify the expression before you substitute?"],
        after=["4.1.1(a)"]),
    work("4.1.2", "Hence, show that sin²θ − 1 = −cos²θ.", 3, [
        "LHS = ({3}/{5})² − 1\n= −{16}/{25}\nRHS = −({4}/{5})²\n= −{16}/{25}\n" + SHOW,      # sin and cos from cot read as y/x
        "LHS = ({4}/{5})² − 1\n= −{9}/{25}\nRHS = −({3}/{5})²\n= −{9}/{25}\n" + SHOW,        # the memo
        "LHS = ({4}/{5})² − 1\n= {9}/{25}\nRHS = −(−{3}/{5})²\n= {9}/{25}\n" + SHOW,         # 16/25 − 1 as 9/25 and −(−3/5)² as +9/25
        "LHS = ({4}/{7})² − 1\n= −{33}/{49}\nRHS = −({3}/{7})²\n= −{9}/{49}\n" + SHOW], 1,   # r = 7, and the result claimed anyway
        ["What are sin θ and cos θ from your sketch?", "What value does each side give when you substitute them?"], after=["4.1.1(a)"]),
]
q42 = [
    work("4.2", "Simplify the following expression WITHOUT using a calculator:\ncos 30° tan 60° + cosec² 45° sin² 60°", 3, [
        "= {√3}/{2} × √3 + ({√2}/{2})² × ({√3}/{2})²\n= {3}/{2} + {2}/{4} × {3}/{4}\n= {3}/{2} + {3}/{8}\n= {15}/{8}",    # cosec 45° as sin 45°
        "= {√3}/{2} × {1}/{√3} + ({2}/{√2})² × ({√3}/{2})²\n= {1}/{2} + {4}/{2} × {3}/{4}\n= {1}/{2} + {3}/{2}\n= 2",   # tan 60° as 1/√3
        "= {1}/{2} × √3 + ({2}/{√2})² × ({√3}/{2})²\n= {√3}/{2} + {4}/{2} × {3}/{4}\n= {√3}/{2} + {3}/{2}\n= {√3 + 3}/{2}",   # cos 30° as ½
        "= {√3}/{2} × √3 + ({2}/{√2})² × ({√3}/{2})²\n= {3}/{2} + {4}/{2} × {3}/{4}\n= {3}/{2} + {3}/{2}\n= 3"], 3,    # the memo
        ["Which special triangles give the exact values of cos 30°, tan 60°, sin 45° and sin 60°?",
         "Which ratio is cosec the reciprocal of?"]),
]
EQ = "{4}/{3} sin θ = cos 37°\n"
q43 = [
    work("4.3", "Solve for θ correct to TWO decimal places, if (4/3) sin θ = cos 37° and 0° ≤ θ ≤ 90°.", 2, [
        EQ + "sin θ = {3(0,76541405)}/{4}\nθ = 0,61°",    # the calculator in radians
        EQ + "sin θ = {3(0,79863551)}/{4}\nθ = 53,20°",   # the cos⁻¹ key for sin⁻¹
        EQ + "sin θ = {3(0,79863551)}/{4}\nθ = 36,80°",   # the memo
        EQ + "sin θ = cos 37° = sin 53°\nθ = 53,00°"], 2,  # the 4/3 dropped and the co-ratio used
        ["How do you get sin θ on its own?", "Which calculator key undoes sin, and is the calculator in degree mode?"]),
]

# ---- QUESTION 5, the question paper page 5 and the memo page 7 ----
WRITE = "Write down the following:\n"
USE = "Use your graph to determine the following:\n"
q5 = [
    draw("5.1", "Sketch, on the grid provided in the ANSWER BOOK, the graph of f and g for 0° ≤ x ≤ 270°.", 6, [
        ["f: the shape of a sine graph, moved down 1 unit, drawn from x = 0° to x = 270°", 1], ["f: the x-intercept (90° ; 0)", 1],
        ["f: the y-intercept (0° ; −1)", 1], ["g: the shape of a cosine graph, stretched vertically by 2, drawn from x = 0° to x = 270°", 1],
        ["g: the x-intercepts (90° ; 0) and (270° ; 0)", 1], ["g: the y-intercept (0° ; 2)", 1]],
        ["What are the y-intercepts f(0°) and g(0°)?", "What does the −1 do to the graph of y = sin x, and what does the 2 do to the graph of "
                                                       "y = cos x?"],
        memo="The answer book gives a grid: x from −30° to 270° across (labelled every 30°, a line every 15°) and y from −3 to 3 up. The "
             "memo's graphs: f rises from (0° ; −1) to (90° ; 0), then falls to (270° ; −2); g falls from (0° ; 2) through (90° ; 0) to "
             "(180° ; −2), then rises to (270° ; 0).",
        # built on the answer book's grid (2026-10-11, as transcribe_g11_math_p2_2017_11.py 6.2.3: two trigonometric graphs on one set of
        # axes): each memo criterion is features (or a shape) whose marks add up to its mark. f's x- and y-intercept leave sin x − 1 open
        # (a sine through two points takes many phases), so the memo's 'shape' of f carries f's turning point (0 marks), which fixes the
        # curve: its minimum (270° ; −2) or its maximum (90° ; 0), both turning points of f in the interval. g's three marked intercepts
        # fix 2 cos x; criterion 4 is both x-intercepts of g, so one carries its mark. The domain draws the end points (unmarked)
        build={"kind": "sketch", "family": "sin", "b": 1, "x": [-30, 270, 15], "y": [-3, 3, 0.5], "domain": [0, 270], "features": [
            {"id": "fx", "kind": "point", "label": "x-intercept of f", "at": [90, 0], "tol": 0, "marks": 1, "crit": 1, "graph": "f"},
            {"id": "fy", "kind": "point", "label": "y-intercept of f", "at": [0, -1], "tol": 0, "marks": 1, "crit": 2, "graph": "f"},
            {"id": "ft", "kind": "point", "label": "turning point of f", "at": [270, -2], "alt": [[90, 0]], "tol": 0, "marks": 0, "crit": 0,
             "graph": "f", "turn": True},
            {"id": "gx1", "kind": "point", "label": "x-intercept of g", "at": [90, 0], "tol": 0, "marks": 1, "crit": 4, "graph": "g"},
            {"id": "gx2", "kind": "point", "label": "x-intercept of g", "at": [270, 0], "tol": 0, "marks": 0, "crit": 4, "graph": "g"},
            {"id": "gy", "kind": "point", "label": "y-intercept of g", "at": [0, 2], "tol": 0, "marks": 1, "crit": 5, "graph": "g"}],
               "graphs": [{"id": "f", "family": "sin", "label": "f", "b": 1, "domain": [0, 270],
                           "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 0}},
                          {"id": "g", "family": "cos", "label": "g", "b": 1, "domain": [0, 270],
                           "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 3}}]}),
    num("5.2.1", WRITE + "Amplitude of g", 2, 0, "", ["What is the amplitude of y = cos x?", "What does multiplying cos x by 2 do to the "
                                                                                            "height of the graph?"]),
    mcq("5.2.2", WRITE + "Range of f" + ANSWER, ["−2 ≤ y ≤ 0", "−1 ≤ y ≤ 1", "−2 < y < 0", "−1 ≤ y ≤ 0"], 0,
        ["What are the lowest and highest y-values of f between 0° and 270°?", "Does f reach those values, so that the ends belong to the "
                                                                               "range?"], marks=2),
    num("5.3.1", USE + "Number of solutions to f(x) = g(x) in the interval 0° ≤ x ≤ 270°", 2, 0, "",
        ["Where do the graphs of f and g cut each other?", "How many of those points lie between 0° and 270°?"]),
    # a memo slip (flagged): the memo gives x = 180° only, but sin x = 2 + 2 cos x also holds at x = 126,87° (sin x = 0,8 and
    # cos x = −0,6), inside 0° ≤ x ≤ 180°. Murci's ruling (2026-10-10, a memo value the paper contradicts): the memo's answer AND the
    # right one both earn the marks, so this is a pick of one with both right
    {"t": "pickn", "n": "5.3.2", "marks": 3,
     "q": USE + "Value(s) of x in the interval 0° ≤ x ≤ 180° for which sin x = 2 + 2 cos x\n\nPick ONE.",
     "clues": ["If you subtract 1 from both sides of sin x = 2 + 2 cos x, which function is on the left?",
               "Where between 0° and 180° is the graph of f exactly one unit above the graph of g?"],
     "opts": ["x = 90°", "x = 180°", "x = 90° or x = 180°", "x = 126,87° or x = 180°"], "pool": [1, 3], "count": 1},
]
for i in q5:   # the built sketch: its features' and shapes' marks are the memo criteria's, criterion by criterion; every feature names
    b = i.get("build") or {}   # one of the two graphs
    if b.get("kind") == "sketch":
        got = {}
        for x in b["features"] + [g["shape"] for g in b["graphs"]]:
            got[x["crit"]] = got.get(x["crit"], 0) + x["marks"]
        assert got == {k: c["marks"] for k, c in enumerate(i["criteria"])}, (i["n"], got)
        assert {f["graph"] for f in b["features"]} == {g["id"] for g in b["graphs"]}, i["n"]

# ---- QUESTION 6, the question paper page 6 and the memo page 8 ----
PQ = "cos 47° = {PQ}/{21}\nPQ = 21 × cos 47°\nPQ = 14,32 m\n"
q6 = [
    num("6.1", "Write down the size of θ.", 47, 0, "°",
        ["From which line is an angle of depression measured?", "That line through R is parallel to PS: how is the angle of depression "
                                                                "related to RP̂Q?"]),
    work("6.2", "Calculate the length of RQ.", 3, [
        "sin P = {RQ}/{RP}\nsin 47° = {RQ}/{21}\nRQ = 21 sin 47°\nRQ = 15,36 m",       # the memo
        "tan P = {RQ}/{RP}\ntan 47° = {RQ}/{21}\nRQ = 21 tan 47°\nRQ = 22,52 m",       # tangent: RP is the hypotenuse
        "sin P = {RP}/{RQ}\nsin 47° = {21}/{RQ}\nRQ = {21}/{sin 47°}\nRQ = 28,71 m",   # the ratio upside down
        "sin P = {RQ}/{RP}\nsin 47° = {RQ}/{21}\nRQ = 21 sin 47°\nRQ = 2,60 m"], 0,    # the calculator in radians
        ["In △PQR, which side is opposite θ, and which is the hypotenuse?", "Which ratio links those two sides?"], after=["6.1"]),
    work("6.3", "Hence, calculate the size of Ŝ.", 2, [
        "tan S = {QS}/{RQ}\ntan S = {17}/{15,36}\nŜ = tan⁻¹({17}/{15,36})\nŜ = 47,90°",   # the ratio upside down
        "tan S = {RQ}/{QS}\ntan S = {15,36}/{17}\nŜ = tan⁻¹({15,36}/{17})\nŜ = 42,10°",   # the memo
        "sin S = {RQ}/{QS}\nsin S = {15,36}/{17}\nŜ = sin⁻¹({15,36}/{17})\nŜ = 64,63°",   # sine: QS taken as the hypotenuse
        "tan S = {RQ}/{QS}\ntan S = {15,36}/{17}\nŜ = tan⁻¹({15,36}/{17})\nŜ = 0,73°"], 1,   # the calculator in radians
        ["In △RQS, which side is opposite Ŝ, and which is next to it?", "Which ratio links those two sides?"], after=["6.2"]),
    work("6.4", "If P, Q and S lie in a straight line, how far apart are the anchors of the wire cables?", 4, [
        "tan 47° = {PQ}/{21}\nPQ = 21 × tan 47°\nPQ = 22,52 m\nPS = 22,52 + 17\n= 39,52 m",          # tangent: 21 is the hypotenuse
        "cos 47° = {21}/{PQ}\nPQ = {21}/{cos 47°}\nPQ = 30,79 m\nPS = 30,79 + 17\n= 47,79 m",         # the ratio upside down
        PQ + "PS = 17 − 14,32\n= 2,68 m",                                                             # subtracted, as if P and S were on one side
        PQ + "PS = 14,32 + 17\n= 31,32 m"], 3,                                                        # the memo
        ["Which ratio in △PQR gives the distance from P to Q?", "P, Q and S lie in a straight line, with Q between P and S: how do PQ and QS make up PS?"],
        after=["6.1"]),
]

# ---- QUESTION 7, the question paper page 7 and the memo page 8 ----
VOL = "V = {1}/{3}πr²h\n"
q7 = [
    work("7.1", "The radius, r, of the cone", 2, [
        VOL + "83,38 = 6,5πr²\nr² = {83,38}/{6,5π}\nr = 2,02 cm",                         # the 1/3 dropped
        VOL + "83,38 = {1}/{3} × 6,5πr²\nr² = {3 × 83,38}/{6,5π}\nr = 12,25 cm",          # r² given as r: the root not taken
        VOL + "83,38 = {1}/{3} × 6,5πr²\nr² = {3 × 83,38}/{6,5π}\nr = 3,5 cm",            # the memo
        VOL + "83,38 = {1}/{3} × 6,5r²\nr² = {3 × 83,38}/{6,5}\nr = 6,20 cm"], 2,         # π left out
        ["Which formula gives the volume of a cone?", "What do you substitute for V and h, and how do you then get r on its own?"]),
    work("7.2", "The slant height, s, of the cone", 2, [
        "s² = h² − r²\ns² = 6,5² − 3,5²\ns = 5,48 cm",    # subtracted, as if h were the hypotenuse
        "s² = h² + r²\ns² = 6,5² + 3,5²\ns = 7,38 cm",    # the memo
        "s² = h² + r²\ns² = 6,5² + 3,5²\ns = 54,50 cm",   # s² given as s: the root not taken
        "s² = h² + r²\ns = 6,5 + 3,5\ns = 10 cm"], 1,     # the root shared out over the sum
        ["The height, the radius and the slant height form a right-angled triangle: which of them is the hypotenuse?",
         "What does Pythagoras' theorem say about the three sides?"], after=["7.1"]),
    work("7.3", "The surface area of the solid", 2, [
        "Surface area = 2πr² + πrs\n= 2π(3,5)² + π(3,5)(7,38)\n= 158,12 cm²",                       # the memo
        "Surface area = 4πr² + πrs\n= 4π(3,5)² + π(3,5)(7,38)\n= 235,09 cm²",                       # a whole sphere for the hemisphere
        "Surface area = 2πr² + πr² + πrs\n= 2π(3,5)² + π(3,5)² + π(3,5)(7,38)\n= 196,60 cm²",       # the hidden base of the cone counted
        "Surface area = πr² + πrs\n= π(3,5)² + π(3,5)(7,38)\n= 119,63 cm²"], 0,                     # the hemisphere taken as a flat circle
        ["Which surfaces of the solid are on the outside: the curved part of the hemisphere and what else?",
         "Is the flat circle where the hemisphere meets the cone on the outside of the solid?"], after=["7.1", "7.2"]),
]

# ---- QUESTION 8, the question paper pages 8-9 and the memo page 9 ----
L12 = "L̂₁ = L̂₂ = 56° "
TRI = "In △PMS and △RMQ:\nP̂₁ = R̂₁ [alt ∠s; PS ∥ QR]\n"
S1Q1 = "Ŝ₁ = Q̂₁ [alt ∠s; PS ∥ QR]\n"
CONG = "△PMS ≡ △RMQ [AAS]\n∴ PM = MR and MS = MQ"
q81 = [
    mcq("8.1.1", "Write down the size of Ô₁." + ANSWER, ["Ô₁ = 34° [alt ∠s; KL ∥ NM]", "Ô₁ = 90° [diagonals of rhombus bisect at 90°]",
                                                       "Ô₁ = 90° [diagonals of rhombus are equal]", "Ô₁ = 146° [co-int ∠s; KL ∥ NM]"], 1,
        ["Which properties of a rhombus are about its diagonals?", "Which of those properties fixes the angle between the diagonals?"]),
    work("8.1.2", "Calculate the size of L̂₁.", 2, [
        "L̂₁ = 180° − 34° [sum of ∠s of △]\n= 146°",               # Ô₁ = 90° left out
        "L̂₁ = 180° − (34° + 90°) [ext ∠ of △]\n= 56°",            # the wrong reason
        "L̂₁ = 180° − (17° + 90°) [sum of ∠s of △]\n= 73°",        # the 34° halved, as if it were the whole angle at K
        "L̂₁ = 180° − (34° + 90°) [sum of ∠s of △]\n= 56°"], 3,    # the memo
        ["In △KLO, which two angles do you know?", "What do the angles of a triangle add up to?"], after=["8.1.1"]),
    work("8.1.3", "Calculate the size of KN̂M.", 2, [
        L12 + "[diagonals bisect the ∠s]\nL̂₁ + L̂₂ = N̂₁ + N̂₂ [opp ∠s of rhombus =]\n∴ KN̂M = 112°",       # the memo
        L12 + "[diagonals bisect the ∠s]\nL̂₁ + L̂₂ + KN̂M = 180° [co-int ∠s; KL ∥ NM]\n∴ KN̂M = 68°",       # L and N taken as co-interior
        L12 + "[diagonals bisect the ∠s]\nKN̂M = L̂₁ [opp ∠s of rhombus =]\n∴ KN̂M = 56°",                    # half of the opposite angle
        L12 + "[diagonals bisect at 90°]\nL̂₁ + L̂₂ = N̂₁ + N̂₂ [opp ∠s of rhombus =]\n∴ KN̂M = 112°"], 0,    # the wrong reason
        ["What do the diagonals of a rhombus do to its angles?", "Which angle of the rhombus is opposite KN̂M?"], after=["8.1.2"]),
]
q82 = [
    work("8.2", "Prove that the diagonals bisect each other.", 4, [
        TRI + S1Q1 + "PS = QR [opp sides of ∥m equal]\n△PMS ≡ △RMQ [SAS]\n∴ PM = MR and MS = MQ",               # the wrong test
        TRI + "M̂₄ = M̂₂ [vert opp ∠s]\nPM = MR [diagonals of ∥m bisect each other]\n" + CONG,                    # circular: assumes PM = MR
        TRI + S1Q1 + "PS = QR [opp sides of ∥m equal]\n" + CONG,                                                # the memo (OR △PQM ≡ △RSM)
        TRI + S1Q1 + "PQ = SR [opp sides of ∥m equal]\n" + CONG], 2,                                            # PQ and SR are not sides of these triangles
        ["Which two triangles have PM and MR as sides, and MS and MQ?", "Which pairs of angles are equal because PS ∥ QR, and which sides are "
                                                                        "equal because PQRS is a parallelogram?"]),
]
DB = "DB = 2DE [diagonals of ∥m ABCD bisect: DE = EB]\n"
DEFC = "DE = FC [opp sides of ∥m DECF]\n"
FC = "FC = 2KC [diagonals of ∥m FGCH bisect: FK = KC]\n"
END = "DE = 2KC [DE = FC]\nDB = 2(2KC) [DB = 2DE]\nDB = 4KC"
q83 = [
    work("8.3", "Prove that DB = 4KC.", 4, [
        "DB = 2DE [midpoint theorem]\n" + DEFC + FC + END,                                     # the wrong theorem
        DB + DEFC + FC + END,                                                                  # the memo
        DB + "DE = FC [diagonals of ∥m DECF bisect each other]\n" + FC + END,                  # DE and FC are sides of DECF, not diagonals
        DB + DEFC + "FC = 2KC [diagonals of ∥m FGCH bisect: GK = KH]\n" + END], 1,             # the halves of the other diagonal
        ["What do the diagonals of a parallelogram do to each other: how is DB related to DE?", "Which side of DECF equals DE, and how is "
                                                                                                  "FC related to KC?"]),
]

# ---- QUESTION 9, the question paper page 10 and the memo page 10 ----
ACG = "In △ACG, F and H are the midpoints of AC and AG [given]\n"
FH = "FH ∥ CG [midpoint theorem]\n"
FE = "FE ∥ BC [same straight lines]\nIn △AGB, H is the midpoint of AG\n"
AREA = "Area of △AEH = {1}/{2} × EH × AE\n9,5 = {1}/{2} × 3,5 × AE\nAE = {38}/{7} = 5,43 cm\n"
BG = "BG = 7 cm [midpoint theorem]\n"
ABC = "Area of △ABC = {1}/{2} × BC × AB\n"
q9 = [
    work("9.1", "Prove that E is the midpoint of AB.", 3, [
        ACG + FH + FE + "HE ∥ BG [proved]\n∴ E is the midpoint of AB [midpoint theorem]",                                   # the theorem for its converse
        ACG + "FH = {1}/{2}CG [midpoint theorem]\n" + FE + "HE ∥ BG [proved]\n∴ E is the midpoint of AB [line from midpoint of side ∥ to 2nd "
        "side]",                                                                                                              # the half, so FE ∥ BC is never shown
        ACG + FH + FE + "HE = {1}/{2}BG [E is the midpoint of AB]\n∴ E is the midpoint of AB [midpoint theorem]",            # circular
        ACG + FH + FE + "HE ∥ BG [proved]\n∴ E is the midpoint of AB [line from midpoint of side ∥ to 2nd side]"], 3,       # the memo
        ["In △ACG, F and H are midpoints: what does that tell you about FH and CG?", "Which line through H is parallel to BG, and in which "
                                                                                     "triangle?"]),
    work("9.2", "If EH = 3,5 cm and the area of △AEH = 9,5 cm², calculate the length of AB.", 3, [
        "AÊH = AB̂C = 90° [alt ∠s; EF ∥ BC]\n" + AREA + "AB = 2AE = 2({38}/{7})\nAB = {76}/{7} = 10,86 cm",                 # the wrong reason
        "AÊH = AB̂C = 90° [corresp ∠s; EF ∥ BC]\nArea of △AEH = EH × AE\n9,5 = 3,5 × AE\nAE = {19}/{7} = 2,71 cm\nAB = 2AE = 2({19}/{7})\n"
        "AB = {38}/{7} = 5,43 cm",                                                                                            # the ½ of the area left out
        "AÊH = AB̂C = 90° [corresp ∠s; EF ∥ BC]\n" + AREA + "AB = 2AE = 2({38}/{7})\nAB = {76}/{7} = 10,86 cm",              # the memo
        "AÊH = AB̂C = 90° [corresp ∠s; EF ∥ BC]\n" + AREA + "AB = {1}/{2}AE = {1}/{2}({38}/{7})\nAB = {19}/{7} = 2,71 cm"], 2,   # AE halved, not doubled
        ["Which angle of △AEH is 90°, and why?", "What is the area of a right-angled triangle in terms of its two shorter sides?"]),
    work("9.3", "Hence, calculate the area of △ABC.", 3, [
        BG + "BC = 2BG = 14 cm\n" + ABC + "= {1}/{2} × 14 × {76}/{7}\n= 76 cm²",                         # the memo
        "BG = 3,5 cm [midpoint theorem]\nBC = 2BG = 7 cm\n" + ABC + "= {1}/{2} × 7 × {76}/{7}\n= 38 cm²",  # BG = EH: never doubled
        BG + "BC = {1}/{2}BG = 3,5 cm\n" + ABC + "= {1}/{2} × 3,5 × {76}/{7}\n= 19 cm²",                 # BG halved, not doubled
        BG + "BC = 2BG = 14 cm\nArea of △ABC = BC × AB\n= 14 × {76}/{7}\n= 152 cm²"], 0,                 # the ½ of the area left out
        ["How is BG related to EH, and BC to BG?", "Which two sides of △ABC are its base and its height?"], after=["9.2"]),
]

REASONS = "Give reasons for ALL statements in QUESTIONS 8 and 9."
missions = [
    {"id": "1", "title": "Question 1", "kind": "Ungrouped data", "marks": 10,
     "lead": "The data below shows the number of laptops sold by 15 sales agents during the last financial year.\n\n"
             "43   48   62   52   46   90   58   37   48   73   84   68   54   34   78", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Grouped data", "marks": 7,
     "lead": "A learner did a project on climate change. At 14:00 each day, she recorded the temperature (in °C) for a certain town. The "
             "information is given in the frequency table below.", "table": TEMPS, "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Analytical geometry", "marks": 16,
     "lead": "In the diagram below, P(7 ; 4), Q(6 ; 6), R(0 ; 3) and S(t ; k) are the vertices of quadrilateral PQRS.",
     # (no coordinates of S, no right angle, no type: 3.2, 3.4 and 3.5 ask for them)
     "figure": fig("Q3", "Axes with origin 0. Quadrilateral PQRS: R(0 ; 3) on the y-axis; Q(6 ; 6) to the upper right of R; P(7 ; 4) to the "
                   "right, a little below Q; S(t ; k) below R and a little to its right, above the x-axis. The sides RQ, QP, PS and SR are "
                   "drawn."), "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Trigonometric ratios", "marks": 11, "lead": "Given 4 cot θ + 3 = 0 and 0° < θ < 180°.",
     "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Special angles", "marks": 3, "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Trigonometric equations", "marks": 2, "items": q43},
    {"id": "5", "title": "Question 5", "kind": "Trigonometric graphs", "marks": 13,
     "lead": "Given f(x) = sin x − 1 and g(x) = 2 cos x for 0° ≤ x ≤ 270°.", "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Heights and distances", "marks": 10,
     "lead": "RQ is a vertical pole. The foot of the pole, Q, is on the same horizontal plane as P and S. The pole is anchored with wire cables "
             "RS and RP. The angle of depression from the top of the pole to point P is 47°. PR is 21 m and QS is 17 m. RP̂Q = θ.",
     # (θ's size is not named: 6.1 asks for it)
     "figure": fig("Q6", "A vertical pole RQ with its foot Q on the level line PS: P to the left of Q and S to the right, with a right angle "
                   "marked at Q. Wire cables run from the top R down to P and to S. PR is marked 21 m and QS 17 m. A dashed horizontal line "
                   "runs to the left from R, and the angle of depression between it and RP is marked 47°; the angle θ is marked at P, "
                   "between PQ and PR."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Surface area and volume", "marks": 6,
     "lead": "The diagram below shows the cross-section of a solid made up of a hemisphere placed on top of a right circular cone with radius r "
             "and slant height s. The perpendicular height of the cone, h, is 6,5 cm and the volume of the cone is 83,38 cm³.\n\nFormulae:\n"
             "Surface area of sphere = 4πr²\nVolume of sphere = (4/3)πr³\nSurface area of cone = πr² + πrs\nVolume of cone = (1/3)πr²h\n\n"
             "Calculate, correct to TWO decimal places:",
     "figure": fig("Q7", "The cross-section of the solid: a semicircle (the hemisphere) on top of an upside-down triangle (the cone) whose "
                   "point is at the bottom. The radius r is drawn dashed from the centre of the flat top to its right-hand end; the height h "
                   "is drawn dashed from the centre straight down to the point, with a right angle where r and h meet; the slant height s "
                   "is marked along the right-hand side of the cone."), "items": q7},
    {"id": "8.1", "title": "Question 8.1", "kind": "Properties of a rhombus", "marks": 5,
     "lead": REASONS + " KLMN is a rhombus with diagonals intersecting at O. LK̂M = 34°.",
     # (no size at O, L or N: 8.1.1-8.1.3 ask for them)
     "figure": fig("Q8.1", "Rhombus KLMN: K at the top left, L at the top right, M at the bottom right and N at the bottom left; the four sides "
                   "carry the same tick mark, and arrows show KL ∥ NM and KN ∥ LM. The diagonals KM and LN cross at O. LK̂M is marked 34°. "
                   "Angles are numbered: K̂₁ between KM and KN; L̂₁ between LK and LN, L̂₂ between LN and LM; Ô₁ at the top, Ô₂ on the "
                   "left, Ô₃ at the bottom and Ô₄ on the right; N̂₁ between NK and NL, N̂₂ between NL and NM; M̂₁ between ML and MK, M̂₂ "
                   "between MK and MN."), "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Parallelogram proofs", "marks": 4,
     "lead": REASONS + " Given parallelogram PQRS with diagonals PR and QS intersecting at M.",
     "figure": fig("Q8.2", "Parallelogram PQRS: P at the top left, S at the top right, R at the bottom right and Q at the bottom left; arrows "
                   "show PS ∥ QR and PQ ∥ SR. The diagonals PR and QS cross at M. Angles are numbered: P̂₁ between PS and PR, P̂₂ between "
                   "PQ and PR; Ŝ₁ between SP and SQ, Ŝ₂ between SQ and SR; R̂₁ between RQ and RP, R̂₂ between RP and RS; Q̂₁ between QR and "
                   "QS, Q̂₂ between QS and QP; at M, M̂₄ at the top, M̂₁ on the left, M̂₃ on the right and M̂₂ at the bottom."), "items": q82},
    {"id": "8.3", "title": "Question 8.3", "kind": "Nested parallelograms", "marks": 4,
     "lead": REASONS + " In the diagram, ABCD is a parallelogram with diagonals intersecting at E. The diagonals of parallelogram DECF "
                       "intersect at G. The diagonals of parallelogram FGCH intersect at K.",
     "figure": fig("Q8.3", "Parallelogram ABCD: A at the top left, B at the top right, C on the right and D on the left; its diagonals AC and "
                   "DB cross at E. Below DC lie F and H. DECF is a parallelogram whose diagonals DC and EF cross at G, and FGCH is a "
                   "parallelogram whose diagonals FC and GH cross at K. Arrows mark the pairs of parallel sides."), "items": q83},
    {"id": "9", "title": "Question 9", "kind": "Triangles and midpoints", "marks": 9,
     "lead": REASONS + " △ABC is right-angled at B. F and G are the midpoints of AC and BC respectively. H is the midpoint of AG. E lies on "
                       "AB such that FHE is a straight line.",
     "figure": fig("Q9", "Triangle ABC with a right angle marked at B: B at the top left, C at the top right and A at the bottom, directly "
                   "below B. G lies on BC, and BG and GC carry the same single tick mark; F lies on AC, and AF and FC carry the same triple "
                   "tick mark; AG is drawn, and AH and HG carry the same double tick mark. A line from E on AB runs through H to F."),
     "items": q9},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.2", "1.3", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4", "3.6", "4.1.1(a)", "4.1.1(b)", "4.1.2", "4.2", "4.3",
                           "6.2", "6.3", "6.4", "7.1", "7.2", "7.3", "8.1.2", "8.1.3", "8.2", "8.3", "9.1", "9.2", "9.3"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["2.2", "5.2.2", "8.1.1"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["1.1", "2.1", "5.2.1", "5.3.1", "6.1"]   # the one-number answers
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["1.4", "5.1"]
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn"]
assert PICKS == ["3.5", "5.3.2"], PICKS
for _m in missions:   # a gate names an EARLIER part of its own mission (the app looks a gate up inside the mission)
    _order = [i["n"] for i in _m["items"]]
    for _i in _m["items"]:
        assert all(e in _order[:_order.index(_i["n"])] for e in _i.get("after", [])), (_i["n"], "a gate outside its mission or later")
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
GATES = {i["n"]: i["after"] for i in ITEMS if i.get("after")}

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2017", "total_marks": 100, "time": "2 hours"},
    "sections": [{"title": "Mathematics", "total": 100, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines and every geometry proof plays as four workings, the memo's FIRST method line by "
                                                       "line (a geometry statement with its [reason]) and three built from real errors (a wrong "
                                                       "ratio, formula or theorem, a sign slip, a misread value, the wrong side, segments or "
                                                       "quadrant, a wrong reason, circular reasoning, the calculator in radians), 0 or full "
                                                       "marks: " + ", ".join(AUTHORED) + " (%d parts, %d marks). The memo's OR method (8.2 "
                                                       "△PQM ≡ △RSM) is another right route and never a wrong option. The memo's single line "
                                                       "'Range = 90 − 34 = 56' (1.2) is set as two lines; 3.3 keeps PR and QS as √50 = 5√2 "
                                                       "(the memo goes on to 7,07); 8.3's reasons add the theorem to the memo's own "
                                                       "'(DE = EB)' and '(FK = KC)'." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "2.2", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                 "with no working (the modal class, a range, Ô₁ with its reason): four options, the memo's "
                                                 "answer and three common errors, 0 or full marks. 5.2.2 loses the memo's split critical values / "
                                                 "notation; its OR notation y ∈ [−2 ; 0] is the right option's interval and no wrong option. "
                                                 "8.1.1's right option words the memo's 'Diagonal bisect at 90°' as 'diagonals of rhombus bisect "
                                                 "at 90°'."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from the page images of a SCANNED "
                                                           "question paper and answer book (no text layer) and the memo's page images (its text "
                                                           "layer garbles fractions, roots and angle names); no API call."},
        {"n": "1.1", "kind": "no_fit", "detail": "One-number answers with no working stay typed on the keypad: 1.1 (the median 54, 2 marks), 2.1 "
                                                 "(30 days), 5.2.1 (the amplitude 2), 5.3.1 (2 solutions) and 6.1 (θ = 47°)."},
        {"n": "1.4", "kind": "no_fit", "detail": "The box and whisker diagram 1.4 is BUILT on the answer book's number line (2026-10-11: 30 to 95, "
                                                 "a tick every 1, a number every 5): the learner places the five values, the box and whiskers "
                                                 "are drawn from them, and the memo's three ticks are marked from them (min. & max. together, "
                                                 "the median, Q₁ and Q₃ together). The answer book's blank number line and grid are described "
                                                 "in the memo text, not cropped."},
        {"n": "5.1", "kind": "no_fit", "detail": "The graphs of f and g (5.1) are BUILT on the answer book's grid (2026-10-11): the learner places "
                                                 "each graph's intercepts and f's turning point, each curve is drawn through its features, and "
                                                 "the memo's six criteria are marked from them. f's turning point (its minimum (270° ; −2) or its "
                                                 "maximum (90° ; 0)), which the memo does not mark on its own, is part of f's shape: two "
                                                 "intercepts do not fix a sine graph."},
        {"n": "3.5", "kind": "no_fit", "detail": "The type of quadrilateral with its motivation plays as statements, pick 2 (1 mark each, as the "
                                                 "memo's 'Rectangle' and 'reason'): the memo's choice and its reason, and four cards that are "
                                                 "false for PQRS (PQ = √5 but QR = √45, so it is neither a square nor a rhombus; m(PR) = 1/7 and "
                                                 "m(QS) = 1, so its diagonals are not perpendicular)."},
        {"n": "3.6", "kind": "no_fit", "detail": "A part whose stem, options or criteria show an earlier part's answer opens only once that part is "
                                                 "answered ('after'): " + "; ".join(k + " after " + " and ".join(v) for k, v in GATES.items())
                                                 + ". 3.3's stem gives S(1 ; 1), 3.2's answer."},
        {"n": "5.3.2", "kind": "memo_issue", "detail": "The memo (page 7) gives x = 180° only (3 marks), but sin x = 2 + 2 cos x has a second "
                                                       "solution in 0° ≤ x ≤ 180°: x = 126,87° (sin x = 0,8 and 2 + 2 cos x = 2 + 2(−0,6) = 0,8), "
                                                       "where the graph of f is one unit above g, as at 180°. Murci's memo-slip ruling "
                                                       "(2026-10-10): a pick of one where the memo's 'x = 180°' AND 'x = 126,87° or x = 180°' "
                                                       "both earn the 3 marks."},
        {"n": "3.3", "kind": "memo_issue", "detail": "The memo (page 4) prints 'OR' between the working for PR and the working for QS, but both "
                                                     "lengths are needed to show PR = QS (it gives a mark for each answer); played as one working "
                                                     "with both lengths."},
        {"n": "3.2", "kind": "memo_issue", "detail": "The memo (page 3) names S's coordinates x and y; the paper writes S(t ; k). The workings use t "
                                                     "and k, as the paper (S(1 ; 1), as the memo)."},
    ],
}
QTOTAL = {"1": 10, "2": 7, "3": 16, "4": 16, "5": 13, "6": 10, "7": 6, "8": 13, "9": 9}   # the paper's [n] per question
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
    "1.4": ["1.1", "1.2", "1.3"],       # its criteria: the median 54, the minimum 34 and maximum 90, Q₁ = 46 and Q₃ = 73
    "2.3": ["2.1"],                     # n = 30 days
    "2.4": ["2.1"],                     # n = 30 days
    "3.3": ["3.1", "3.2"],              # the stem's S(1 ; 1), and a wrong option's PQ = √5
    "3.4": ["3.2"],                     # m(RS) from S(1 ; 1)
    "3.6": ["3.1", "3.3"],              # RS = PQ = √5 and QS = 5√2
    "4.1.1(b)": ["4.1.1(a)"],           # x = −3, y = 4, r = 5
    "4.1.2": ["4.1.1(a)"],              # sin θ = 4/5 and cos θ = −3/5
    "6.2": ["6.1"],                     # θ = 47°
    "6.3": ["6.2"],                     # RQ = 15,36 m
    "6.4": ["6.1"],                     # θ = 47°
    "7.2": ["7.1"],                     # r = 3,5 cm
    "7.3": ["7.1", "7.2"],              # r = 3,5 cm and s = 7,38 cm
    "8.1.2": ["8.1.1"],                 # Ô₁ = 90°
    "8.1.3": ["8.1.2"],                 # L̂₁ = 56°
    "9.3": ["9.2"]}, GATES              # AB = 76/7 cm
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's and answer book's page images "
                                                                       "and the memo's page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
