"""Grade 10 Mathematics P1 Nov 2017 (DBE common paper), the whole paper (Questions 1 to 7, 100 marks), hand-transcribed into the
catalogue format, then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working
are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the transcription is the
source, kept in git (out/ is not). The question paper is a SCAN (no text layer): read from its page images rendered at 150 dpi,
exponents and fractions checked on crops at 250 dpi (1.3.3, 2.3); the memo has a text layer whose fractions and exponents garble,
so it was read from its page images (150 dpi).

  python tools/ingest/transcribe_g10_math_p1_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Mathematics P1 Nov 2017 Eng.pdf" "uploads/Grade 10 Mathematics P1 Nov 2017 MG Afr & Eng.pdf" --id g10-math-p1-2017-11 --from-json

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p1_2025_11.py and the Grade 10 pilot
transcribe_g10_math_p1_2018_11.py):
  Every expression, value or set the memo WORKS OUT in two or more lines (substitute, factorise, simplify, solve, calculate,
  determine, a 'write down' whose memo shows a working: 5.6, 7.1.3) -> authored whole-working multiple choice, `work`: the memo's
  FIRST method line by line ("{a}/{b}" a stacked fraction) and three workings each built from a DIFFERENT real error, every option
  of a part the same layout (`shape`), the right one's place spread over A-D across the paper; the part keeps its marks, all or
  nothing. A form the memo ALSO accepts never appears in a wrong option (4.2's $1 ≈ £0,78: no option uses 0,78).
  An answer the memo states with no working (a pair of integers, a range, x-values read off a graph, an interval) -> authored
  multiple choice of answers: the memo's and three common errors.
  One number with no working (3.1.1, 5.2, 6.2.1, 7.1.1, 7.1.2) stays num; the one word 1.1.2 (Irrational) is a term with Rational
  rejected; the number line 2.1.2, the sketch 6.1.3 and the Venn diagram 7.2.1 -> draw (self-checked against the memo's criteria).
  Where a part's stem, options or criteria show an EARLIER part's answer it carries "after" (see the assert at the end).
Missions: Question 5 shares one stem and graph, so it is one mission; Questions 1, 2, 3, 4, 6 and 7 are their numbered groups
(1.1, 1.2, 1.3, 2.1 ...), 6.1 (the exponential p) and 6.2 (the hyperbola sketch) apart.
Figure boxes are measured in PDF points (page 595 x 841, read from the PDF) from the ink on the scan (scratch tool
lower/g10-math-p1-2017-11/figs.py) and checked on the padded crops (ingest's 1% pad applied)."""
import json
import re
from pathlib import Path

PID = "g10-math-p1-2017-11"
W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q3.2": [4, 215.2, 283.3, 409.6, 366.5],   # the triangle of numbers (rows 1-5)
    "Q5": [5, 111.2, 167.9, 481.6, 388.2],     # g, f and the points R, O, S(2 ; 0), T(0 ; 8)
    "Q6.2": [6, 104.7, 370.4, 489.2, 618.8]}   # f, g and the points P, Q, (−2 ; 7)


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


term = lambda n, q, a, clues, marks=1, strict=False, reject=None, **kw: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                                        **({"strict": True} if strict else {}),
                                                                        **({"reject": reject} if reject else {}), **kw}
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


# ---- QUESTION 1, the question paper page 3 and the memo pages 2-3 ----
q11 = [
    work("1.1.1", "Determine the value of q if a = 2, b = −1 and c = −4.\nLeave your answer in simplest surd form.", 2, [
        "q = √(b² − 4ac)\nq = √(−1² − 4(2 × −4))\nq = √31",                            # (−1)² taken as −1
        "q = √(b² − 4ac)\nq = √((−1)² − 4(2 × −4))\nq = √33",                          # the memo
        "q = √(b² − 4ac)\nq = √((−1)² − 4(2 × −4))\nq = √1 + √32 = 1 + 4√2",           # the root split over a sum
        "q = √(b² − 4ac)\nq = √((−1)² − 4(2 × −4))\nq = 5,74"], 1,                     # a decimal, not the surd form asked for
        ["Which value replaces each of a, b and c?", "What sign does (−1)² have, and what does subtracting a negative product do?"]),
    term("1.1.2", "State whether q is rational or irrational.", ["Irrational", "Irrational number", "q is irrational", "It is irrational"],
         ["Is the number under the square root a perfect square?", "Can the value of q be written as a fraction of two integers?"],
         reject=["Rational", "Rational number", "q is rational", "It is rational"]),
    mcq("1.1.3", "Between which TWO consecutive integers does q lie?" + ANSWER, ["4 and 5", "6 and 7", "5 and 6", "16 and 17"], 2,
        ["Which perfect squares lie on either side of the number under the root?",
         "How do the square roots of neighbouring perfect squares compare with q?"])]
q12 = [
    work("1.2.1", "t²(r − s) − r + s", 3, [
        "= t²(r − s) − (r − s)\n= (r − s)(t² − 1)\n= (r − s)(t − 1)²",            # a difference of squares taken as a perfect square
        "= t²r − t²s − r + s\n= r(t² − 1) − s(t² − 1)\n= (r − s)(t² − 1)",       # regrouped, and stops before the difference of squares
        "= t²(r − s) + (r − s)\n= (r − s)(t² + 1)\n= (r − s)(t + 1)²",            # −r + s written +(r − s)
        "= t²(r − s) − (r − s)\n= (r − s)(t² − 1)\n= (r − s)(t − 1)(t + 1)"], 3,  # the memo
        ["Can you write −r + s as a multiple of (r − s)?", "Once (r − s) is taken out, can the bracket that is left be factorised further?"]),
    work("1.2.2", "(x³ + 1)/(x² − x + 1)", 2, [
        "= {(x + 1)(x² − x + 1)}/{x² − x + 1}\n= x + 1",     # the memo
        "= {(x − 1)(x² + x + 1)}/{x² − x + 1}\n= x − 1",     # the sum of cubes factorised as a difference, then 'cancelled'
        "= {x · x² + 1}/{x² − x + 1}\n= {x + 1}/{−x + 1}",   # x² cancelled out of a sum
        "= {x³}/{x²} + {1}/{−x + 1}\n= x + {1}/{1 − x}"], 0, # the fraction split over the terms of its denominator
        ["Is the numerator a sum or a difference of two cubes?", "Which factor do the numerator and the denominator then share?"])]
q13 = [
    work("1.3.1", "(2y + 3)(7y² − 6y − 8)", 2, [
        "= 14y³ − 12y² − 16y + 21y² + 18y − 24\n= 14y³ + 9y² + 2y − 24",   # 3 × (−6y) taken as +18y
        "= 2y(7y² − 6y − 8) + 3\n= 14y³ − 12y² − 16y + 3",                 # the 3 not multiplied into the bracket
        "= 14y³ − 12y² − 16y + 21y² − 18y − 24\n= 14y³ + 9y² − 34y − 24",  # the memo
        "= 14y² − 12y² − 16y + 21y² − 18y − 24\n= 23y² − 34y − 24"], 2,    # 2y × 7y² taken as 14y²
        ["Have you multiplied each term of the first bracket by every term of the second?", "Which like terms can you collect afterwards?"]),
    work("1.3.2", "3/(x² − 9) + 2/(x − 3)²", 3, [
        "= {3}/{(x − 3)(x + 3)} + {2}/{(x − 3)²}\n= {3(x + 3) + 2(x − 3)}/{(x − 3)²(x + 3)}\n= {3x + 9 + 2x − 6}/{(x − 3)²(x + 3)}\n"
        "= {5x + 3}/{(x − 3)²(x + 3)}",                                                # each numerator multiplied by the wrong missing factor
        "= {3}/{(x − 3)(x + 3)} + {2}/{(x − 3)²}\n= {3(x − 3) + 2(x + 3)}/{(x − 3)²(x + 3)}\n= {3x − 9 + 2x + 6}/{(x − 3)²(x + 3)}\n"
        "= {5x − 3}/{(x − 3)²(x + 3)}",                                                # the memo
        "= {3}/{(x − 3)²} + {2}/{(x − 3)²}\n= {3 + 2}/{(x − 3)²}\n= {5}/{(x − 3)²}\n= {5}/{x² − 6x + 9}",   # x² − 9 factorised as (x − 3)²
        "= {3}/{(x − 3)(x + 3)} + {2}/{(x − 3)²}\n= {3(x − 3) + 2(x + 3)}/{(x − 3)²(x + 3)}\n= {3x − 9 + 2x + 3}/{(x − 3)²(x + 3)}\n"
        "= {5x − 6}/{(x − 3)²(x + 3)}"], 1,                                            # 2(x + 3) expanded as 2x + 3
        ["Can you factorise x² − 9?", "What is the lowest common denominator, and what must each numerator be multiplied by?"]),
    work("1.3.3", "(3ᵗ − 3ᵗ⁻²)/(2 · 3ᵗ − 3ᵗ)", 3, [
        "= {3ᵗ(1 − 3⁻²)}/{3ᵗ(2 − 1)}\n= (1 − {1}/{9}) ÷ 1\n= {8}/{9}",        # the memo
        "= {3ᵗ(1 − 3⁻²)}/{3ᵗ(2 − 1)}\n= (1 − (−9)) ÷ 1\n= 10",                # 3⁻² taken as −9
        "= {3ᵗ − (3ᵗ − 9)}/{2 · 3ᵗ − 3ᵗ}\n= {9}/{3ᵗ}\n= 3²⁻ᵗ",                # 3ᵗ⁻² read as 3ᵗ − 3²
        "= {3ᵗ(1 − 3⁻²)}/{2 · 3ᵗ}\n= (1 − {1}/{9}) ÷ 2\n= {4}/{9}"], 0,       # 2 · 3ᵗ − 3ᵗ taken as 2 · 3ᵗ
        ["Which common factor can you take out of the numerator and out of the denominator?", "How do you write 3⁻² as a fraction?"])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 4-5 ----
q21 = [
    work("2.1.1", "Solve the inequality.", 2, [
        "−2x < 12\nx < −6",       # the sign not reversed
        "−2x < 20\nx > −10",      # 4 moved across without its sign change
        "−2x < 12\nx > −24",      # multiplied by −2 instead of divided
        "−2x < 12\nx > −6"], 3,   # the memo
        ["What do you subtract from both sides first?", "What happens to the inequality sign when you divide by a negative number?"]),
    draw("2.1.2", "Hence, represent your answer to QUESTION 2.1.1 on a number line.", 1, [
        ["An open dot at −6 with an arrow from it to the right (x > −6)", 1]],
        ["Is the end point part of the solution: should its dot be open or closed?", "In which direction do the values that satisfy the "
                                                                                       "inequality lie?"],
        memo="The memo's number line: an open (unshaded) dot at −6, with 0 marked to its right, and an arrow from −6 pointing to the right.",
        after=["2.1.1"])]
EQS = "(1): 3x − 4y = −4 and (2): −2x − y = 10\n"
q22 = [
    work("2.2", "Solve simultaneously for x and y:\n−2x − y = 10 and 3x − 4y = −4", 4, [
        EQS + "(2) × (−4): 8x + 4y = −40 … (3)\n(1) + (3): 11x = −44\nx = −4\nSubstitute into (2): −2(−4) − y = 10\ny = 2",          # 8 − y = 10 solved as y = 2
        EQS + "(2) × (−4): 8x + 4y = 40 … (3)\n(1) + (3): 11x = 36\nx = {36}/{11}\nSubstitute into (2): −2({36}/{11}) − y = 10\n"
        "y = −{182}/{11}",                                                                                                         # 10 × (−4) taken as 40
        EQS + "(2) × (−4): 8x + 4y = −40 … (3)\n(1) + (3): 11x = −44\nx = −4\nSubstitute into (2): −2(−4) − y = 10\ny = −2",         # the memo
        EQS + "(2) × (−4): 8x + 4y = −40 … (3)\n(1) + (3): 11x = −44\nx = −{1}/{4}\nSubstitute into (2): −2(−{1}/{4}) − y = 10\n"
        "y = −{19}/{2}"], 2,                                                                                                       # the division upside down
        ["Which variable can you eliminate by multiplying one equation by a number?", "Once you know one variable, which equation is easiest "
                                                                                      "to substitute into?"])]
q23 = [
    work("2.3.1", "x(x − 5)/6 − 1 = 0", 3, [
        "x² − 5x − 6 = 0\n(x − 6)(x + 1) = 0\nx = 6 or x = −1",             # the memo
        "x² − 5x − 1 = 0\nx = {5 ± √29}/{2}\nx = 5,19 or x = −0,19",        # the 1 not multiplied by 6
        "x² − 5x − 6 = 0\n(x + 6)(x − 1) = 0\nx = −6 or x = 1",             # the signs in the factors swapped
        "x(x − 5) − 6 = 0\nx(x − 5) = 6\nx = 6 or x = 11"], 0,              # each factor set equal to 6
        ["What can you multiply every term by to remove the fraction?", "Can the quadratic you get be factorised?"]),
    work("2.3.2", "c = √(a + 2x)", 2, [
        "c² = a + 2x\n2x = c² + a\nx = {c² + a}/{2}",            # a moved across without its sign change
        "c² = a + 2x\n2x = c² − a\nx = {c² − a}/{2}",            # the memo
        "c² = a² + 4x²\n4x² = c² − a²\nx = {√(c² − a²)}/{2}",    # each term under the root squared on its own
        "c² = a + 2x\n2x = c² − a\nx = {c²}/{2} − a"], 1,        # only c² divided by 2
        ["How do you undo a square root?", "Which term must you move to leave 2x on its own?"])]
AGES = "Linda now: x; Tabelo now: 4x\n"
q24 = [
    work("2.4", "Tabelo is currently four times as old as his daughter, Linda. Six years from now, Tabelo will be three times as old as "
         "Linda.\n\nCalculate Linda's age currently.", 4, [
        AGES + "In 6 years: Linda x + 6; Tabelo 4x\n4x = 3(x + 6)\n4x − 3x = 18\nx = 18: Linda is 18 years old",                    # 6 years added to Linda only
        AGES + "In 6 years: Linda x + 6; Tabelo 4x + 6\n4x + 6 = 3(x + 6)\n4x − 3x = 18 − 6\nx = 12: Linda is 4(12) = 48 years old",  # Tabelo's age given
        AGES + "In 6 years: Linda x + 6; Tabelo 4x + 6\n4x + 6 = 3(x + 6)\n4x − 3x = 18 + 6\nx = 24: Linda is 24 years old",         # 6 moved without its sign change
        AGES + "In 6 years: Linda x + 6; Tabelo 4x + 6\n4x + 6 = 3(x + 6)\n4x − 3x = 18 − 6\nx = 12: Linda is 12 years old"], 3,     # the memo
        ["If Linda is x years old now, how old is Tabelo now?", "How old will each be in six years, and which of those ages is three times "
                                                                "the other?"])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 6-7 ----
q31 = [
    num("3.1.1", "Write down the value of b.", 14, 0, "",
        ["What is the constant difference between consecutive terms?", "Which terms stand on either side of b, and does your value fit "
                                                                        "both of them?"], marks=2),
    work("3.1.2", "Determine the nth term of the sequence.", 2, [
        "Tₙ = pn + q\nTₙ = 3n + q\nTₙ = 3n + 5",    # the first term taken as q
        "Tₙ = pn + q\nTₙ = 5n + q\nTₙ = 5n + 3",    # the first term taken as p and the difference as q
        "Tₙ = pn + q\nTₙ = 3n + q\nTₙ = 3n + 2",    # the memo
        "Tₙ = pn + q\nTₙ = 3n + q\nTₙ = 3n − 2"], 2,  # q found as 3 − 5
        ["What is the constant difference between the terms, and where does it go in Tₙ = pn + q?",
         "Which value of q makes T₁ equal to the first term?"]),
    work("3.1.3", "Calculate the value of the 15th term of the sequence.", 2, [
        "Tₙ = a + nd\nT₁₅ = 5 + 15(3)\nT₁₅ = 50",       # a + nd, not a + (n − 1)d
        "Tₙ = 3n + 2\nT₁₅ = 3(15) + 2\nT₁₅ = 47",       # the memo
        "Tₙ = 3n + 2\nT₁₅ = 3(14) + 2\nT₁₅ = 44",       # n − 1 put into a formula already in n
        "Tₙ = 3n + 2\nT₁₅ = 3(15 + 2)\nT₁₅ = 51"], 1,   # a bracket round n + 2
        ["Which value of n stands for the 15th term?", "What do you get when you substitute it into your general term?"], after=["3.1.2"]),
    work("3.1.4", "Which term in the sequence is equal to 83?", 2, [
        "Tₙ = 3n + 2\n83 = 3n + 2\n3n = 81\nn = 27",                 # the memo
        "Tₙ = 3n + 2\n83 = 3n + 2\n3n = 85\nn = 28,33",              # 2 moved across without its sign change
        "Tₙ = 3n + 2\nT₈₃ = 3(83) + 2\nT₈₃ = 249 + 2\nT₈₃ = 251",    # 83 taken as the position, not the value
        "Tₙ = 3n + 2\n83 = 3n + 2\n3n = 81\nn = 243"], 0,            # multiplied by 3 instead of divided
        ["Is 83 a position in the sequence or the value of a term?", "Can you set your general term equal to it and solve for n?"],
        after=["3.1.2"])]
ROWS = "Row sums: 2 ; 16 ; 54 ; 128 ; …\nRow 1: 2 × 1 = 2; row 2: 2 × 8 = 16; row 3: 2 × 27 = 54; row 4: 2 × 64 = 128\nRow n: 2n³\n"
q32 = [
    work("3.2.1", "Calculate the sum of the numbers in the 8th row.", 3, [
        ROWS + "Row 8: 2(8 × 3) = 48",          # the cube worked out as × 3
        ROWS + "Row 8: (2 × 8)³ = 4 096",       # 2n³ worked out as (2n)³
        ROWS + "Row 8: 2(8²) = 128",            # the cube worked out as a square
        ROWS + "Row 8: 2(8)³ = 1 024"], 3,      # the memo
        ["What is the sum of each of the first four rows?", "How do those sums compare with the cubes 1, 8, 27 and 64?"]),
    work("3.2.2", "Determine the mean of the numbers in the 20th row.", 2, [
        "Mean in row 20 = {(2 × 20)³}/{20}\n= 3 200",   # 2n³ worked out as (2n)³
        "Mean in row 20 = 2(20)³\n= 16 000",            # the row's sum, not divided by the count
        "Mean in row 20 = {2(20)³}/{20}\n= 800",        # the memo
        "Mean in row 20 = {2(20)²}/{20}\n= 40"], 2,     # a square for the cube
        ["How many numbers are there in the 20th row?", "How is a mean worked out from a sum and a count?"], after=["3.2.1"])]

# ---- QUESTION 4, the question paper page 4 and the memo page 8 ----
q41 = [
    work("4.1.1", "Calculate how much interest Mrs Grey has earned over the 7 years.", 2, [
        "SI = {Prt}/{100}\n= {18 000 × 4,5 × 7}/{100}\n= R5 670,00",           # the memo
        "SI = {Prt}/{100}\n= {18 000 × 0,045 × 7}/{100}\n= R56,70",            # the rate turned into a decimal AND divided by 100
        "A = P(1 + i·n)\n= 18 000(1 + 0,045 × 7)\n= R23 670,00",               # the amount at the end, not the interest
        "I = P(1 + i)ⁿ − P\n= 18 000(1 + 0,045)⁷ − 18 000\n= R6 495,51"], 0,   # compound interest for simple
        ["Which formula gives the simple interest earned on an amount?", "What are P, r and t here?"]),
    work("4.1.2", "Mrs Grey wants to buy a television set that costs R27 660,00 now. If the average rate of inflation over the last 5 years "
         "was 6,7% p.a., calculate the cost of the television set 5 years ago.", 3, [
        "A = P(1 + i·n)\n27 660 = P(1 + 0,067 × 5)\nP = {27 660}/{1 + 0,067 × 5}\nP = R20 719,10",       # simple growth for inflation
        "A = P(1 + i)ⁿ\nA = 27 660(1 + 0,067)⁵\nA = 27 660 × 1,067⁵\nA = R38 253,77",                   # grown forward instead of back
        "A = P(1 + i)ⁿ\n27 660 = P(1 + 0,067)⁷\nP = {27 660}/{(1 + 0,067)⁷}\nP = R17 567,15",           # 7 years (the investment's) for 5
        "A = P(1 + i)ⁿ\n27 660 = P(1 + 0,067)⁵\nP = {27 660}/{(1 + 0,067)⁵}\nP = R20 000,00"], 3,      # the memo
        ["Does a price grow with inflation like simple or compound interest?", "Is R27 660,00 the amount at the start or at the end of the "
                                                                                "5 years?"]),
    work("4.1.3", "At what rate of simple interest should Mrs Grey have invested her money 7 years ago if she intends buying the television "
         "set now using only her original investment of R18 000 and the interest earned over the last 7 years?", 3, [
        "A = P(1 + i·n)\n27 660 = 18 000(1 + i × 5)\n5i = {27 660}/{18 000} − 1\ni = 0,10733…\nSimple interest rate = 10,73%",   # 5 years (inflation's) for 7
        "A = P(1 + i·n)\n27 660 = 18 000(1 + i × 7)\n7i = {27 660}/{18 000} − 1\ni = 0,07666…\nSimple interest rate = 7,67%",    # the memo
        "A = P(1 + i)ⁿ\n27 660 = 18 000(1 + i)⁷\n(1 + i)⁷ = {27 660}/{18 000}\ni = 0,06329…\nSimple interest rate = 6,33%",      # the compound formula
        "A = P(1 + i·n)\n27 660 = 18 000(1 + i × 7)\n7i = {27 660}/{18 000}\ni = 0,21952…\nSimple interest rate = 21,95%"], 1,  # the 1 not subtracted
        ["What amount must the R18 000 grow to in 7 years?", "Which simple interest formula links A, P, i and n?"])]
q42 = [
    work("4.2", "On a certain day the exchange rate between the US dollar and South African rand is $1 = R12,91. At the same time the exchange "
         "rate between the British pound and the South African rand is £1 = R16,52.\n\nCalculate the exchange rate between the British pound "
         "and US dollar on that day.", 2, [
        "{Pound}/{Dollar} = {R16,52}/{R12,91}\n∴ $1 ≈ £1,28",       # the right ratio with the currencies swapped
        "Pound × Dollar = R16,52 × R12,91\n∴ £1 ≈ $213,27",         # the rand values multiplied
        "{Pound}/{Dollar} = {R16,52}/{R12,91}\n∴ £1 ≈ $1,28",       # the memo (its OR, $1 ≈ £0,78, is in no option)
        "Pound − Dollar = R16,52 − R12,91\n∴ £1 ≈ $3,61"], 2,       # the rand values subtracted
        ["How many rand is each currency worth?", "How many dollars have the same rand value as one pound?"])]

# ---- QUESTION 5, the question paper page 5 and the memo page 9 ----
q5 = [
    mcq("5.1", "Write down the range of g." + ANSWER, ["y ≤ 8", "y ≥ 8", "y < 8", "x ≤ 8"], 0,
        ["Which way does the parabola open?", "What is the largest y-value that g reaches?"]),
    num("5.2", "Write down the x-coordinate of R.", -2, 0, "",
        ["What is the axis of symmetry of g(x) = ax² + q?", "How far is S from that axis, and on which side of it is R?"]),
    work("5.3", "Calculate the values of a and q.", 3, [
        "g(x) = ax² + 8, so q = 8\ng(2) = a(2)² + 8 = 0\na = 2",           # 8 moved across without its sign change
        "g(x) = ax² + 8, so q = 8\ng(2) = 2a + 8 = 0\na = −4",             # (2)² taken as 2
        "g(x) = ax² + 8, so q = 8\ng(2) = a(2)² + 8 = 0\na = −{1}/{2}",    # the division upside down
        "g(x) = ax² + 8, so q = 8\ng(2) = a(2)² + 8 = 0\na = −2"], 3,      # the memo
        ["Which point on g gives you q straight away?", "Which other point can you substitute into g(x) = ax² + q to find a?"]),
    work("5.4", "Determine the equation of f.", 3, [
        "f(x) = mx + c, so c = 8\nf(−2) = −2m + 8 = 0\nm = 4\nf(x) = 4x + 8",                  # the memo
        "f(x) = mx + c, so c = 8\nf(2) = 2m + 8 = 0\nm = −4\nf(x) = −4x + 8",                  # S used instead of R
        "f(x) = mx + c, so c = 8\nf(−2) = −2m + 8 = 0\nm = {1}/{4}\nf(x) = {1}/{4}x + 8",      # the division upside down
        "f(x) = mx + c, so m = 8\nf(−2) = 8(−2) + c = 0\nc = 16\nf(x) = 8x + 16"], 0,         # the y-intercept taken as the gradient
        ["What is the y-intercept of f?", "Which point on the x-axis does f pass through, and what equation does substituting it give?"],
        after=["5.2"]),
    mcq("5.5.1", "Use the graphs to determine the value(s) of x for which: f(x) = g(x)" + ANSWER,
        ["x = −2 or x = 2", "x = −2 or x = 0", "x = 0 or x = 2", "x = −2 or x = 8"], 1,
        ["Where do the two graphs meet?", "What are the x-coordinates of those meeting points?"], marks=2, after=["5.2"]),
    mcq("5.5.2", "Use the graphs to determine the value(s) of x for which: x · g(x) ≤ 0" + ANSWER,
        ["x ≤ −2 or 0 ≤ x ≤ 2", "−2 ≤ x ≤ 2", "−2 < x < 0 or x > 2", "−2 ≤ x ≤ 0 or x ≥ 2"], 3,
        ["When is a product of two factors negative or zero?", "Where is g positive, where is it negative, and where is x negative?"],
        marks=3, after=["5.2"]),
    work("5.6", "The graph h is obtained when g is reflected along the line y = 0. Write down the equation of h in the form h(x) = px² + k.", 2, [
        "h(x) = −(−2x² + 8)\nh(x) = 2x² + 8",       # the minus not taken to the 8
        "h(x) = −(−2x² + 8)\nh(x) = 2x² − 8",       # the memo
        "h(x) = −2(−x)² + 8\nh(x) = −2x² + 8",      # reflected in the y-axis (x = 0) instead
        "h(x) = −(−2x² + 8)\nh(x) = −2x² − 8"], 1,  # only the constant's sign changed
        ["What happens to the y-values of a graph reflected in the x-axis?", "What do you get when you multiply every term of g(x) by −1?"],
        after=["5.3"])]

# ---- QUESTION 6, the question paper page 6 and the memo pages 10-11 ----
q61 = [
    mcq("6.1.1", "Write down the range of p." + ANSWER, ["y ≥ −9", "y < −9", "x > −9", "y > −9"], 3,
        ["Which horizontal line does p approach but never reach?", "Is the graph of kˣ + q above or below that line?"]),
    work("6.1.2", "Determine the equation of p.", 3, [
        "p(x) = kˣ − 9\n0 = k² − 9\nk² = 9\nk = ±9\nk = 9 since k > 0\np(x) = 9ˣ − 9",                                     # the square root not taken
        "p(x) = kˣ − 10\n0 = k² − 10\nk² = 10\nk = ±√10\nk = √10 since k > 0\np(x) = (√10)ˣ − 10",                        # the asymptote read as the y-intercept
        "p(x) = kˣ − 9\n0 = k² − 9\nk² = 9\nk = ±3\nk = 3 since k > 0\np(x) = 3ˣ − 9",                                     # the memo
        "p(x) = kˣ − 9\n0 = 2k − 9\n2k = 9\nk = {9}/{2}\nk = {9}/{2} since k > 0\np(x) = ({9}/{2})ˣ − 9"], 2,            # k² read as 2k
        ["What does the horizontal asymptote tell you about q?", "What equation do you get when you substitute the x-intercept into p(x)?"]),
    draw("6.1.3", "Sketch the graph of p. Show clearly the intercepts with the axes and the asymptote.", 3, [
        ["Asymptote y = −9 drawn as a dashed horizontal line", 1], ["Intercepts with the axes: (2 ; 0) and (0 ; −8)", 1],
        ["Shape: an increasing exponential curve above its asymptote", 1]],
        ["Where does p cut the y-axis: what is p(0)?", "Which horizontal line does p approach as x becomes very negative?"],
        memo="The memo's sketch: p(x) = 3ˣ − 9 rising from left to right, close above the dashed asymptote y = −9 on the left, cutting the "
             "y-axis at (0 ; −8) and the x-axis at (2 ; 0), then rising steeply.", after=["6.1.2"])]
q62 = [
    num("6.2.1", "Write down the value of w.", -1, 0, "",
        ["Through which point do both axes of symmetry of a hyperbola pass?", "What is the vertical asymptote of f(x) = k/x + w?"]),
    work("6.2.2", "The point (−2 ; 7) lies on f. Calculate the value of k.", 2, [
        "f(x) = {k}/{x} − 1\n7 = {k}/{−2} − 1\nk = −16",     # the memo
        "f(x) = {k}/{x} − 1\n7 = {k}/{−2} − 1\nk = −12",     # −1 moved across without its sign change
        "f(x) = {k}/{x} − 1\n−2 = {k}/{7} − 1\nk = −7",      # x and y swapped
        "f(x) = {k}/{x} − 1\n7 = {k}/{−2} − 1\nk = −4"], 0,  # divided by −2 instead of multiplied
        ["What is f(x) once you know w?", "What equation do you get when you substitute the point (−2 ; 7)?"], after=["6.2.1"]),
    work("6.2.3", "Calculate the x-coordinates of P and Q.", 4, [
        "f(x) = g(x)\n{−16}/{x} − 1 = −x − 1\nx² − 16 = 0\n(x − 4)(x + 4) = 0\nx = 4 at P or x = −4 at Q",                    # P and Q swapped
        "f(x) = g(x)\n{−16}/{x} − 1 = −x − 1\nx² − 16 = 0\n(x − 8)(x + 8) = 0\nx = −8 at P or x = 8 at Q",                    # 16 halved, not square-rooted
        "f(x) = g(x)\n{−16}/{x} − 1 = −x\nx² − x − 16 = 0\nx = {1 ± √65}/{2}\nx = −3,53 at P or x = 4,53 at Q",              # g's −1 dropped
        "f(x) = g(x)\n{−16}/{x} − 1 = −x − 1\nx² − 16 = 0\n(x − 4)(x + 4) = 0\nx = −4 at P or x = 4 at Q"], 3,               # the memo
        ["At the points where the graphs meet, how are f(x) and g(x) related?", "What can you multiply both sides by to clear the fraction?"],
        after=["6.2.1", "6.2.2"]),
    mcq("6.2.4", "Write down the values of x for which −16/x > −x." + ANSWER,
        ["x < −4 or 0 < x < 4", "−4 < x < 4, x ≠ 0", "−4 < x < 0 or x > 4", "x > 4"], 2,
        ["How does −16/x > −x compare f(x) with g(x)?", "For which x-values is the graph of f above the graph of g?"], marks=2,
        after=["6.2.3"])]

# ---- QUESTION 7, the question paper page 7 and the memo page 12 ----
q71 = [
    num("7.1.1", "Complete the statement: P(A) + P(B) = ...", 1, 0, "",
        ["What does it mean for two events to be complementary?", "If event A does not happen, which other event must happen?"]),
    num("7.1.2", "Write down the value of P(A and B).", 0, 0, "",
        ["Can complementary events happen at the same time?", "What does that tell you about the overlap of A and B in a Venn diagram?"]),
    work("7.1.3", "Write down the value of P(B).", 1, [
        "P(B) = 1 − P(A′)\n= 0,65",          # B taken as A
        "P(B) = P(A′)\n= 0,35",              # the memo
        "P(B) = 1 + P(A′)\n= 1,35",          # the complement rule with the wrong sign
        "P(B) = P(A) − P(A′)\n= 0,30"], 1,   # a made-up difference
        ["If A does not happen, which event happens?", "Which given probability belongs to 'not A'?"], after=["7.1.1"])]
q72 = [
    draw("7.2.1", "Represent the information above in a Venn diagram.", 4, [
        ["20 in the overlap of S and T", 1], ["28 in T only", 1], ["x − 20 in S only", 1], ["8 outside both circles", 1]],
        ["Which number goes in the overlap of the two circles?", "How many learners own a tablet only, once the overlap is taken out?"],
        memo="The memo's Venn diagram: a rectangle for the 150 learners holding two overlapping circles, S (smartphone) and T (tablet; the "
             "memo labels it B): x − 20 in S only, 20 in the overlap, 28 in T only and 8 outside both circles."),
    work("7.2.2", "How many learners owned only a smartphone?", 3, [
        "x − 20 + 20 + 48 + 8 = 150\nx = 94\nSmartphone only = 94 − 20\n= 74",             # all 48 tablet owners put in T only
        "x − 20 + 20 + 28 = 150\nx = 122\nSmartphone only = 122 − 20\n= 102",              # the 8 with neither device left out
        "x − 20 + 20 + 28 + 8 = 150\nx = 114\nSmartphone only = 114 − 20\n= 94",           # the memo
        "x − 20 + 20 + 28 + 8 = 150\nx = 114\nSmartphone only = 114 − 20 − 28\n= 66"], 2,  # the tablet-only learners subtracted too
        ["What must all the regions of the Venn diagram add up to?", "Does x count only the smartphone-only region, or the overlap too?"],
        after=["7.2.1"]),
    work("7.2.3(a)", "Calculate the probability that a learner selected at random from this group: owned only a smartphone", 1, [
        "P(S only) = {94}/{150}\n= 0,63",     # the memo
        "P(S only) = {114}/{150}\n= 0,76",    # every smartphone owner counted
        "P(S only) = {94}/{142}\n= 0,66",     # the 8 with no device left out of the total
        "P(S only) = {94}/{114}\n= 0,82"], 0, # out of the smartphone owners only
        ["How many learners owned only a smartphone?", "Out of how many learners is the one chosen?"], after=["7.2.2"]),
    work("7.2.3(b)", "Calculate the probability that a learner selected at random from this group: owned at most one type of device", 2, [
        "P(S only or T only) = {94}/{150} + {28}/{150}\n= {122}/{150}\n= {61}/{75}\n= 0,81",                                  # exactly one device
        "P(S only, T only or neither) = {94}/{150} + {28}/{150} + {8}/{150}\n= {130}/{150}\n= {13}/{15}\n= 0,87",              # the memo
        "P(S only, both or T only) = {94}/{150} + {20}/{150} + {28}/{150}\n= {142}/{150}\n= {71}/{75}\n= 0,95",                # at least one device
        "P(at most one) = 1 − {94}/{150}\n= {56}/{150}\n= {28}/{75}\n= 0,37"], 1,                                              # the wrong complement
        ["Which regions of the Venn diagram hold learners with no device or with exactly one device?",
         "How many learners are in those regions together?"], after=["7.2.1", "7.2.2"])]

# (no caption names a value or region a question asks for: the captions show in the enlarged view and to screen readers)
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Substitution and estimation", "marks": 4, "lead": "Given: q = √(b² − 4ac)", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Factorisation", "marks": 5, "lead": "Factorise the following expressions fully:", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Simplifying expressions", "marks": 8, "lead": "Simplify the following completely:",
     "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Linear inequalities", "marks": 3, "lead": "Given: 4 − 2x < 16 where x ∈ R", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Simultaneous equations", "marks": 4, "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Equations", "marks": 5, "lead": "Solve for x:", "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Word problems", "marks": 4, "items": q24},
    {"id": "3.1", "title": "Question 3.1", "kind": "Linear sequences", "marks": 8, "lead": "Consider the linear sequence: 5 ; 8 ; 11 ; b ; 17 ; …",
     "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Number patterns", "marks": 5,
     "lead": "Consider the number pattern below created by using the numbers of the sequence 2 ; 6 ; 10 ; 14 ; 18 ; …",
     "figure": fig("Q3.2", "A triangle of numbers in rows, one more number in each row: 2 in the first row; 6 and 10 in the second; 14, 18 "
                   "and 22 in the third; 26, 30, 34 and 38 in the fourth; and in the fifth, 42 followed by four places shown as dots."),
     "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Interest and inflation", "marks": 8,
     "lead": "Seven years ago, Mrs Grey decided to invest R18 000 in a bank account that paid simple interest at 4,5% p.a.", "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Exchange rates", "marks": 2, "items": q42},
    {"id": "5", "title": "Question 5", "kind": "Parabola and straight line", "marks": 15,
     "lead": "The diagram shows the graphs of g(x) = ax² + q and f(x) = mx + c.\nR and S(2 ; 0) are the x-intercepts of g and T(0 ; 8) is the "
             "y-intercept of g.\nGraph f passes through R and T.",
     "figure": fig("Q5", "The parabola g opens downwards; it crosses the y-axis at T(0 ; 8) and the x-axis at R, to the left of the origin O, "
                   "and at S(2 ; 0). The straight line f rises from bottom left to top right, crossing the x-axis at R and the y-axis at T."),
     "items": q5},
    {"id": "6.1", "title": "Question 6.1", "kind": "Exponential graphs", "marks": 7,
     "lead": "The function p(x) = kˣ + q is described by the following properties:\n• k > 0 ; k ≠ 1\n• x-intercept at (2 ; 0)\n• The "
             "horizontal asymptote is y = −9", "items": q61},
    {"id": "6.2", "title": "Question 6.2", "kind": "Hyperbola and straight line", "marks": 9,
     "lead": "The sketch below shows the graphs of f(x) = k/x + w and g(x) = −x − 1.\nThe graph g is an axis of symmetry of f. The graphs f and "
             "g intersect at P and Q.",
     "figure": fig("Q6.2", "The straight line g falls from top left to bottom right, crossing the x-axis to the left of the origin O and then "
                   "the y-axis. The hyperbola f has two branches: one at the top left, rising steeply beside the y-axis through the "
                   "marked point (−2 ; 7) and levelling off towards the left, and one at the bottom right, rising from far below beside the "
                   "y-axis and levelling off towards the right. g cuts the top-left branch at P and the bottom-right branch at Q."),
     "items": q62},
    {"id": "7.1", "title": "Question 7.1", "kind": "Complementary events", "marks": 3,
     "lead": "Two events, A and B, are complementary and make up the entire sample space. Also, P(A′) = 0,35.", "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Venn diagrams", "marks": 10,
     "lead": "A survey was conducted among 150 learners in Grade 10 at a certain school to establish how many of them owned the following "
             "devices: smartphone (S) or tablet (T).\n\nThe results were as follows:\n• 8 learners did not own either a smartphone or a "
             "tablet.\n• 20 learners owned both a smartphone and a tablet.\n• 48 learners owned a tablet.\n• x learners owned a smartphone.",
     "items": q72},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.1.1", "1.2.1", "1.2.2", "1.3.1", "1.3.2", "1.3.3", "2.1.1", "2.2", "2.3.1", "2.3.2", "2.4", "3.1.2", "3.1.3",
                           "3.1.4", "3.2.1", "3.2.2", "4.1.1", "4.1.2", "4.1.3", "4.2", "5.3", "5.4", "5.6", "6.1.2", "6.2.2", "6.2.3",
                           "7.1.3", "7.2.2", "7.2.3(a)", "7.2.3(b)"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["1.1.3", "5.1", "5.5.1", "5.5.2", "6.1.1", "6.2.4"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["3.1.1", "5.2", "6.2.1", "7.1.1", "7.1.2"]   # the one-number answers
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["1.1.2"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.1.2", "6.1.3", "7.2.1"]
assert not [i["n"] for i in ITEMS if i["t"] in ("pickn", "match")], "no statements or sorts in this paper"
for i in ITEMS:   # a line that ends in "[...]" draws as a proof's reason: no working here has one
    assert i["t"] != "mcq" or not any(shape(o)[1] for o in i["opts"]), i["n"]
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2017", "total_marks": 100, "time": "2 hours"},
    "sections": [{"title": "Mathematics", "total": 100, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines (a substitution, a factorisation, a simplification, a solution, a term, a sum, an "
                                                       "amount, a rate, a probability) plays as four workings, the memo's FIRST method line by "
                                                       "line and three built from real errors (a sign slip, a step not distributed, a wrong "
                                                       "formula or period, a misread value, a wrong count or region), one step a line, 0 or full "
                                                       "marks: " + ", ".join(AUTHORED) + " (%d parts, %d marks). A form the memo also accepts is "
                                                       "never a wrong option: no option of 4.2 uses its OR answer $1 ≈ £0,78."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.1.3", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                   "with no working (two consecutive integers, a range, x-values read off a graph, an interval) "
                                                   "that a word marker cannot read (y > −9 from y ≥ −9, x ≥ 2 from x > 2): four options, the "
                                                   "memo's answer and three common errors, 0 or full marks."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 7), hand-transcribed from a SCANNED question paper (no "
                                                           "text layer) and the memo's page images (its text layer garbles fractions and powers); "
                                                           "no API call."},
        {"n": "3.1.1", "kind": "no_fit", "detail": "One-number answers with no working stay typed on the keypad: 3.1.1 (b = 14, 2 marks), 5.2 "
                                                   "(x = −2), 6.2.1 (w = −1), 7.1.1 (1) and 7.1.2 (0)."},
        {"n": "1.1.2", "kind": "no_fit", "detail": "Rational or irrational is a term: the memo's 'Irrational' (and 'irrational number', 'q is "
                                                   "irrational'), with 'Rational' and its phrasings rejected, so the two-letter difference is "
                                                   "never forgiven as a spelling slip."},
        {"n": "2.1.2", "kind": "no_fit", "detail": "The number line (2.1.2), the sketch of p (6.1.3) and the Venn diagram (7.2.1) are drawn on "
                                                   "paper and self-checked against the memo's criteria."},
        {"n": "6.2.2", "kind": "memo_issue", "detail": "The memo's mark column reads 'subst. (2 ; −7)', but the paper's point and the memo's own "
                                                       "working are (−2 ; 7); played as (−2 ; 7) (k = −16, as the memo)."},
        {"n": "7.2.1", "kind": "memo_issue", "detail": "The memo's Venn diagram labels the tablet circle B, not T, and writes 'S = 150' for the "
                                                       "sample space, while S is also the smartphone event. The criteria name the circles S and T "
                                                       "as the paper does; the numbers (x − 20, 20, 28, 8) are the memo's."},
        {"n": "3.2.1", "kind": "memo_issue", "detail": "The memo's OR method lists row 8 as 114 + 118 + 122 + 136 + 130 + 134 + 138 + 142: the "
                                                       "fourth number is 126 (the sum 1 024 is right with 126, 1 034 with 136). Not played: the "
                                                       "options follow the memo's first method, 2n³."},
        {"n": "7.2.3(b)", "kind": "memo_issue", "detail": "The memo labels the working P(S or T or neither), but adds S only (94), T only (28) and "
                                                          "neither (8): 'S or T' would also take in the 20 with both devices. The right option "
                                                          "labels it P(S only, T only or neither) with the memo's numbers and answer (13/15 = 0,87)."},
    ],
}
QTOTAL = {"1": 17, "2": 16, "3": 13, "4": 10, "5": 15, "6": 16, "7": 13}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
assert per_q == QTOTAL, per_q
# the right letter (no printed multiple choice in this paper, so every letter is ours): the 30 authored workings as even as 30 allows
# (7 or 8 each: the brief's 3-7 band is for fewer workings), and all 36 four-option questions even (9 each)
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
worked = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(worked.values()) - min(worked.values()) <= 1 and min(worked.values()) >= 3, worked
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert len(four) == len(at) and max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, the paper:", spread, "authored workings:", worked, "four-option:", fspread)
total = sum(i["marks"] for i in ITEMS)
assert total == 100, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts")
print("total:", total)
# every gate, so a dropped "after" fails the run
assert {i["n"]: i["after"] for i in ITEMS if i.get("after")} == {
    "2.1.2": ["2.1.1"],                                        # x > −6
    "3.1.3": ["3.1.2"], "3.1.4": ["3.1.2"],                    # Tₙ = 3n + 2
    "3.2.2": ["3.2.1"],                                        # row n sums to 2n³
    "5.4": ["5.2"], "5.5.1": ["5.2"], "5.5.2": ["5.2"],        # R(−2 ; 0)
    "5.6": ["5.3"],                                            # g(x) = −2x² + 8
    "6.1.3": ["6.1.2"],                                        # p(x) = 3ˣ − 9 (its y-intercept −8)
    "6.2.2": ["6.2.1"], "6.2.3": ["6.2.1", "6.2.2"],           # f(x) = −16/x − 1
    "6.2.4": ["6.2.3"],                                        # x = ±4
    "7.1.3": ["7.1.1"],                                        # the complement rule
    "7.2.2": ["7.2.1"],                                        # the Venn regions x − 20, 20, 28, 8
    "7.2.3(a)": ["7.2.2"], "7.2.3(b)": ["7.2.1", "7.2.2"]}     # 94 own only a smartphone
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the memo's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 7 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
