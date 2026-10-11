"""Grade 10 Mathematics P1 Nov 2018 (DBE common paper), the whole paper (Questions 1 to 8, 100 marks), hand-transcribed into the
catalogue format, then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working
are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the transcription is the
source, kept in git (out/ is not). The question paper is a SCAN (no text layer): read from its page images rendered at 150 dpi,
exponents, subscripts and the Venn shading checked on crops at 200-250 dpi; the memo has a text layer whose fractions and
exponents garble, so it was read from its page images too (150 dpi, zoomed crops at 250 dpi where a subscript mattered: 3.5).

  python tools/ingest/transcribe_g10_math_p1_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Mathematics P1 Nov 2018 Eng.pdf" "uploads/Grade 10 Mathematics P1 Nov 2018 MG Afr & Eng.pdf" --id g10-math-p1-2018-11 --from-json

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p1_2025_11.py):
  Every expression, value or set the memo WORKS OUT in two or more lines (factorise, simplify, solve, calculate, determine, show
  that) -> authored whole-working multiple choice, `work`: the memo's FIRST method line by line ("{a}/{b}" a stacked fraction)
  and three workings each built from a DIFFERENT real error, every option of a part the same layout (`shape`), the right one's
  place spread over A-D across the paper; the part keeps its marks, all or nothing. In the 'show that' (7.2) every option ends in
  the given R4 779,13: a wrong one reaches it through a wrong step. A form the memo ALSO accepts never appears in a wrong option
  (2.1.1 without its restriction, 1.2.2's OR form (1 − 8x)/((x + 3)(2 − x)), 5.4.1's (−2 ; 2)).
  An answer the memo states with no working (a factorised trinomial, a formula, a coordinate, a range, an interval, an axis of
  symmetry, probability notation, a choice of diagrams) -> authored multiple choice of answers: the memo's and three common errors.
  One read-off number with no working (2.2.2, 3.1, 4.1.1, 4.1.2) stays num; the sketch 6.2 -> draw (self-checked against the
  memo's criteria); 8.1.2 (a choice and its reason) -> statements, 1 mark each.
  Where a part's options show an EARLIER part's answer it carries "after" (see the assert below).
Missions: Questions 3, 4, 5, 6 and 7 share a stem (a pattern, a diagram, a graph, a function, an advertisement), so each is one
mission; Questions 1, 2 and 8 are their numbered groups (1.1, 1.2, 1.3 ...). 8.3 asks about the three Venn diagrams of 8.2, so
it is its own mission with the same figure.
Figure boxes are measured in PDF points (page 595 x 841) from the ink on the scan (scratch tool lower/g10-math-p1-2018-11/figs.py)
and checked on a contact sheet with ingest's 1% pad applied."""
import json
import random
import re
from pathlib import Path

W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q4": [4, 164, 354, 488, 450],      # the three dot patterns (their numbers and dot counts are the mission's table)
    "Q5": [5, 135, 195, 458, 457.5],    # y1 stops above "5.1 Write down the:" (its top is at 467.4 pt, the pad is 8.4 pt)
    "Q8": [7, 106, 344, 437, 683]}      # the three Venn diagrams with their labels 8.2.1 - 8.2.3


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


def stmt(n, q, marks, right, wrong, clues, each):
    """A written answer as statements: the memo's points (right) and clearly false cards (wrong), shuffled with a fixed seed."""
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("g10-math-p1-2018-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


# ---- QUESTION 1, the question paper page 3 and the memo pages 2-3 ----
q11 = [
    work("1.1.1", "4x − x³", 2, [
        "= x(4 − x²)\n= x(2 − x)(2 + x)",          # the memo
        "= x(4 − x²)\n= x(2 − x)²",                # a difference of squares taken as a perfect square
        "= x(4 − x²)\n= x(4 − x)(4 + x)",          # 4 not square-rooted
        "= x(4 − x²)\n= x(x − 2)(x + 2)"], 0,      # the signs of 4 − x² reversed
        ["What factor do both terms share?", "Is the bracket that is left a difference of two squares?"]),
    mcq("1.1.2", "x² + 15x − 54" + ANSWER, ["(x − 18)(x + 3)", "(x + 18)(x − 3)", "(x + 6)(x − 9)", "(x − 6)(x + 9)"], 1,
        ["Which pairs of numbers multiply to −54?", "Which of those pairs adds up to +15?"], marks=2),
    work("1.1.3", "y − xy + x − 1", 3, [
        "= y(1 − x) + 1(x − 1)\n= (y + 1)(1 − x)",     # brackets not made the same before taking them out
        "= y(1 + x) − 1(1 + x)\n= (y − 1)(1 + x)",     # a sign slip taking y out of −xy
        "= y(1 − x) − 1(1 − x)\n= (y − 1)(1 − x)",     # the memo
        "= y(1 − x) − 1(x − 1)\n= (y − 1)(x − 1)"], 2, # −1 taken out without changing the signs in the bracket
        ["Can you group the four terms in pairs that each have a common factor?",
         "After grouping, are the two brackets the same? Which sign change would make them match?"])]
q12 = [
    work("1.2.1", "(x + 2)(x² − x + 3)", 2, [
        "= x³ − x² + 3x + 2x² − 2x + 6\n= x³ + x² + 5x + 6",   # 3x − 2x collected as 5x
        "= x³ − x² + 3x + 2x² − 2x + 6\n= x³ + x² + x + 6",    # the memo
        "= x³ + x² + 3x + 2x² − 2x + 6\n= x³ + 3x² + x + 6",   # x × (−x) taken as +x²
        "= x(x² − x + 3) + 2\n= x³ − x² + 3x + 2"], 1,         # the 2 not multiplied into the bracket
        ["Have you multiplied every term in the first bracket by every term in the second?", "Which like terms can you then collect?"]),
    work("1.2.2", "5/(x + 3) − 3/(2 − x)", 3, [
        "= {5}/{x + 3} − {3}/{x − 2}\n= {5(x − 2) − 3(x + 3)}/{(x + 3)(x − 2)}\n= {5x − 10 − 3x − 9}/{(x + 3)(x − 2)}\n"
        "= {2x − 19}/{(x + 3)(x − 2)}",                                                   # 2 − x turned round without changing the sign in front
        "= {5}/{x + 3} + {3}/{x − 2}\n= {5(x − 2) + 3(x + 3)}/{(x + 3)(x − 2)}\n= {5x − 10 + 3x + 3}/{(x + 3)(x − 2)}\n"
        "= {8x − 7}/{(x + 3)(x − 2)}",                                                    # 3(x + 3) expanded as 3x + 3
        "= {5}/{x + 3} + {3}/{x − 2}\n= {5 + 3}/{(x + 3)(x − 2)}\n= {8}/{(x + 3)(x − 2)}\n= {8}/{x² + x − 6}",   # numerators not multiplied
        "= {5}/{x + 3} + {3}/{x − 2}\n= {5(x − 2) + 3(x + 3)}/{(x + 3)(x − 2)}\n= {5x − 10 + 3x + 9}/{(x + 3)(x − 2)}\n"
        "= {8x − 1}/{(x + 3)(x − 2)}"], 3,                                                # the memo
        ["How can you rewrite 2 − x so that the two denominators share a factor?",
         "What is the lowest common denominator, and what does each numerator become over it?"]),
    work("1.2.3", "(25⁻ˣ · 15ˣ⁺¹)/(3ˣ · 5⁻ˣ)", 3, [
        "= {5⁻ˣ · 3ˣ⁺¹ · 5ˣ⁺¹}/{3ˣ · 5⁻ˣ}\n= 5⁻ˣ⁺ˣ⁺¹⁺ˣ · 3ˣ⁺¹⁻ˣ\n= 5ˣ⁺¹ · 3¹\n= 3 · 5ˣ⁺¹",          # 25⁻ˣ written 5⁻ˣ
        "= {5⁻²ˣ · 3ˣ⁺¹ · 5}/{3ˣ · 5⁻ˣ}\n= 5⁻²ˣ⁺¹⁺ˣ · 3ˣ⁺¹⁻ˣ\n= 5¹⁻ˣ · 3¹\n= 3 · 5¹⁻ˣ",              # 15ˣ⁺¹ split as 3ˣ⁺¹ · 5
        "= {5⁻²ˣ · 3ˣ⁺¹ · 5ˣ⁺¹}/{3ˣ · 5⁻ˣ}\n= 5⁻²ˣ⁺ˣ⁺¹⁺ˣ · 3ˣ⁺¹⁻ˣ\n= 5¹ · 3¹\n= 15",                # the memo
        "= {5⁻²ˣ · 3ˣ⁺¹ · 5ˣ⁺¹}/{3ˣ · 5⁻ˣ}\n= 5⁻²ˣ⁺ˣ⁺¹⁻ˣ · 3ˣ⁺¹⁻ˣ\n= 5¹⁻²ˣ · 3¹\n= 3 · 5¹⁻²ˣ"], 2,   # dividing by 5⁻ˣ taken as subtracting x
        ["Can you write 25 and 15 using only the prime bases 3 and 5?", "When you divide powers of the same base, what do you do with "
                                                                        "their exponents?"])]
q13 = [
    work("1.3", "Determine the value of (3p + q)² if 9p² + q² = 12 and pq = −3.", 3, [
        "(3p + q)² = 9p² + 6pq + q²\n= 9p² + q² + 6pq\n= 12 + 6(−3)\n= −6",    # the memo
        "(3p + q)² = 9p² + 3pq + q²\n= 9p² + q² + 3pq\n= 12 + 3(−3)\n= 3",     # the middle term not doubled
        "(3p + q)² = 9p² + 6pq + q²\n= 9p² + q² + 6pq\n= 12 + 6(3)\n= 30",     # the sign of pq lost
        "(3p + q)² = 9p² + 2pq + q²\n= 9p² + q² + 2pq\n= 12 + 2(−3)\n= 6"], 0, # the 3 left out of the middle term
        ["What do you get when you expand (3p + q)²?", "Which parts of that expansion can you replace with the given values?"])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 4-5 ----
q21 = [
    work("2.1.1", "px + qx = a", 2, [
        "x(p + q) = a\nx = a − p − q",               # subtracts instead of dividing
        "x(p + q) = a\nx = {p + q}/{a} ; a ≠ 0",     # divides the wrong way round
        "x(pq) = a\nx = {a}/{pq} ; p, q ≠ 0",        # px + qx taken out as x · pq
        "x(p + q) = a\nx = {a}/{p + q} ; p ≠ −q"], 3,  # the memo (it gives full marks without the restriction too)
        ["What factor do the two terms on the left share?", "What must you divide both sides by, and when is that not allowed?"]),
    work("2.1.2", "2x² − 5x + 2 = 0", 3, [
        "(2x + 1)(x + 2) = 0\nx = −{1}/{2} or x = −2",   # the signs in the factors
        "(2x − 1)(x − 2) = 0\nx = {1}/{2} or x = 2",     # the memo
        "(2x − 1)(x − 2) = 0\nx = 1 or x = 2",           # 2x − 1 = 0 solved without dividing by 2
        "x(2x − 5) = −2\nx = −2 or x = {3}/{2}"], 1,     # each factor set equal to −2
        ["Can the trinomial be factorised into two brackets?", "When is a product equal to zero?"]),
    work("2.1.3", "(1/2)³ˣ⁺¹ = 32", 3, [
        "2⁻³ˣ⁻¹ = 2⁵\n−3x − 1 = 5\n3x = −6\nx = −2",          # the memo
        "2³ˣ⁺¹ = 2⁵\n3x + 1 = 5\n3x = 4\nx = {4}/{3}",        # 1/2 taken as 2
        "2⁻³ˣ⁺¹ = 2⁵\n−3x + 1 = 5\n3x = −4\nx = −{4}/{3}",    # the minus on 3x only
        "2⁻³ˣ⁻¹ = 2⁴\n−3x − 1 = 4\n3x = −5\nx = −{5}/{3}"], 0, # 32 written 2⁴
        ["Can you write 1/2 and 32 as powers of the same base?", "Once the bases are the same, what can you say about the exponents?"])]
q22 = [
    work("2.2.1", "Solve for m.", 2, [
        "−19 ≤ 3m < −4\n−{19}/{3} ≤ m < −{4}/{3}",   # 8 subtracted instead of added
        "−3 ≤ 3m < 12\n−9 ≤ m < 36",                 # multiplied by 3 instead of divided
        "−3 ≤ 3m < 12\n−1 ≤ m < 4",                  # the memo
        "−3 ≤ 3m < 12\n−1 < m < 4"], 2,              # the ≤ lost: −1 left out
        ["What can you add to all three parts to leave 3m in the middle?", "What do you then divide all three parts by?"]),
    num("2.2.2", "Hence, write down the number of integers that satisfy the inequality.", 5, 0, "integers",
        ["Which whole numbers lie in the interval you found?", "Is each end point included or not?"])]
q23 = [
    work("2.3", "Solve simultaneously for x and y if:\n5x + 4y = 21 and 2x = 3 − y", 4, [
        "y = 3 − 2x\n5x + 4(3 − 2x) = 21\n5x − 8x = 21 + 12\n−3x = 33, so x = −11\ny = 3 − 2(−11) = 25",                 # 12 moved without its sign change
        "y = 3 − 2x\n5x + 4(3 − 2x) = 21\n5x − 2x = 21 − 12\n3x = 9, so x = 3\ny = 3 − 2(3) = −3",                      # 4 not multiplied into 2x
        "y = 2x − 3\n5x + 4(2x − 3) = 21\n5x + 8x = 21 + 12\n13x = 33, so x = {33}/{13}\ny = 2({33}/{13}) − 3 = {27}/{13}",  # y made the subject with the signs reversed
        "y = 3 − 2x\n5x + 4(3 − 2x) = 21\n5x − 8x = 21 − 12\n−3x = 9, so x = −3\ny = 3 − 2(−3) = 9"], 3,                # the memo
        ["Can you make y the subject of the second equation?", "What do you get when you substitute that into the first equation?"])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 5-6 ----
q3 = [
    num("3.1", "Write down the 4th term of the pattern.", 11, 0, "",
        ["What is the constant difference between consecutive terms?", "Is the pattern going up or down?"]),
    work("3.2", "Determine the expression for the nth term.", 2, [
        "Tₙ = pn + q = 3n + q\n14 = 3(3) + q\nq = 5\nTₙ = 3n + 5",           # the difference taken as +3
        "Tₙ = pn + q = −3n + q\n14 = −3(3) + q\nq = 23\nTₙ = −3n + 23",      # the memo
        "Tₙ = pn + q = −3n + q\n20 = −3(0) + q\nq = 20\nTₙ = −3n + 20",      # the first term counted as n = 0
        "Tₙ = pn + q = −3n + q\n14 = −3(3) + q\nq = 5\nTₙ = −3n + 5"], 1,    # −9 moved across without its sign change
        ["What is the constant difference, and what is its sign?", "In Tₙ = pn + q, how can one known term give you q?"]),
    work("3.3", "Calculate the number of terms in the sequence.", 2, [
        "−3n + 23 = −103\n−3n = −80\nn = 26,67, so 27 terms",   # 23 moved across without its sign change
        "20 − (−103) = 123\n{123}/{3} = 41\nn = 41",            # counts the steps, not the terms
        "−3n + 23 = −103\n3n = 126\nn = 42",                    # the memo
        "−3n + 23 = −103\n3n = 126\nn = 42 + 1 = 43"], 2,       # one added for the first term
        ["Which term of the pattern has the value −103?", "Can you set your expression for the nth term equal to that value and solve?"],
        after=["3.2"]),
    work("3.4", "Which term is the first to have a negative value?", 3, [
        "Tₙ < 0: −3n + 23 < 0\n−3n < −23\nn > {23}/{3} = 7,67\nn = 8: T₈ is the first negative term",      # the memo
        "Tₙ < 0: −3n + 23 < 0\n−3n < −23\nn < {23}/{3} = 7,67\nn = 7: T₇ is the first negative term",      # the sign not reversed
        "Tₙ < 0: −3n + 23 < 0\n−3n < −23\nn > 23 × 3 = 69\nn = 70: T₇₀ is the first negative term",        # multiplied instead of divided
        "Tₙ < 0: −3n + 23 < 0\n−3n < −23\nn > {3}/{23} = 0,13\nn = 1: T₁ is the first negative term"], 0,  # the division upside down
        ["When is a term negative: what inequality does that give?", "What happens to the inequality sign when you divide by a negative "
                                                                     "number?"], after=["3.2"]),
    work("3.5", "What is the value of the 19th even-valued term in the sequence?", 2, [
        "Even values at n = 2 ; 4 ; 6 ; …: the 19th is at n = 38\nT₃₈ = −3(38) + 23\nT₃₈ = −91",    # even positions, not even values
        "Even values at n = 1 ; 3 ; 5 ; …: the 19th is at n = 39\nT₃₉ = −3(39) + 23\nT₃₉ = −94",    # the 19th odd position taken as 2(19) + 1
        "The 19th term: n = 19\nT₁₉ = −3(19) + 23\nT₁₉ = −34",                                     # 'even-valued' ignored
        "Even values at n = 1 ; 3 ; 5 ; …: the 19th is at n = 37\nT₃₇ = −3(37) + 23\nT₃₇ = −88"], 3,  # the memo (its label T₃₉ is a slip)
        ["Which terms are even: 20, 17, 14, …? Is there a pattern in their positions?", "At which position does the 19th even-valued "
                                                                                       "term sit?"], after=["3.2"])]

# ---- QUESTION 4, the question paper page 4 and the memo page 6 ----
q4 = [
    num("4.1.1", "Write down the number of dots in the 4th pattern.", 16, 0, "dots",
        ["How is each number of dots related to its pattern number?", "Can you carry that on to pattern 4?"]),
    num("4.1.2", "Write down the number of dots in the 13th pattern.", 169, 0, "dots",
        ["What do you do to a pattern number to get its number of dots?", "Can you do the same to 13?"]),
    mcq("4.1.3", "Write down a formula for the number of dots in the nth pattern." + ANSWER,
        ["Tₙ = 2n − 1", "Tₙ = 3n − 2", "Tₙ = (n + 1)²", "Tₙ = n²"], 3,
        ["What do 1, 4 and 9 have in common?", "Does your formula give the right count for pattern 1, 2 AND 3?"]),
    work("4.2", "Hence, or otherwise, calculate the value of:\n1 + 3 + 5 + … + 43", 3, [
        "Tₙ = 2n − 1\n43 = 2n − 1\n44 = 2n, so n = 22\nTotal dots = 43² = 1 849",          # the last number squared
        "Tₙ = 2n − 1\n43 = 2n − 1\n44 = 2n, so n = 22\nTotal dots = n² = 22² = 484",      # the memo
        "Tₙ = 2n − 1\n43 = 2n − 1\n42 = 2n, so n = 21\nTotal dots = n² = 21² = 441",      # −1 moved across without its sign change
        "Tₙ = 2n − 1\n43 = 2n − 1\n44 = 2n, so n = 88\nTotal dots = n² = 88² = 7 744"], 1,  # multiplied by 2 instead of divided
        ["Which odd number, counting 1 ; 3 ; 5 ; …, is 43?", "How does the sum of the first n odd numbers relate to the dot patterns?"],
        after=["4.1.3"])]

# ---- QUESTION 5, the question paper page 5 and the memo page 7 ----
q5 = [
    mcq("5.1.1", "Write down the coordinates of D." + ANSWER, ["(0 ; −3)", "(0 ; −4)", "(−3 ; 0)", "(0 ; 1)"], 0,
        ["What is the value of x at a y-intercept?", "What does any non-zero number raised to the power 0 equal?"], marks=2),
    mcq("5.1.2", "Write down the range of g." + ANSWER, ["y ≥ −4", "y < −4", "y > −4", "x > −4"], 2,
        ["Which horizontal line does g approach but never reach?", "Is g above or below that line?"]),
    work("5.2.1", "Calculate the coordinates of A.", 2, [
        "({1}/{2})ˣ − 4 = 0\n2ˣ = 4 = 2²\nx = 2\nA(2 ; 0)",       # 1/2 taken as 2
        "({1}/{2})ˣ − 4 = 0\n2⁻ˣ = 4 = 2²\nx = −2\nA(0 ; −2)",    # the coordinates swapped
        "({1}/{2})ˣ − 4 = 0\n2⁻ˣ = 4 = 2²\nx = −2\nA(−2 ; 0)",    # the memo
        "({1}/{2})ˣ − 4 = 0\n{1}/{2}x = 4\nx = 8\nA(8 ; 0)"], 2,  # the exponent read as a product
        ["What is y at an x-intercept?", "Can you write both sides of the equation as powers of 2?"]),
    work("5.2.2", "Calculate the values of a and q.", 4, [
        "E(1 ; 3): 3 = a(1)² + q, so a + q = 3\nA(−2 ; 0): 0 = a(−2)² + q, so q = −4a\na − 4a = 3, so a = −1\nq = −4(−1) = 4",   # the memo
        "E(1 ; 3): 1 = a(3)² + q, so 9a + q = 1\nA(−2 ; 0): 0 = a(−2)² + q, so q = −4a\n9a − 4a = 1, so a = {1}/{5}\n"
        "q = −4({1}/{5}) = −{4}/{5}",                                                                                      # E's x and y swapped
        "E(1 ; 3): 3 = a(1)² + q, so a + q = 3\nA(−2 ; 0): 0 = a(−2)² + q, so q = −4a\na − 4a = 3, so a = 1\nq = −4(1) = −4",     # −3a = 3 solved as a = 1
        "E(1 ; 3): 3 = a(1)² + q, so a + q = 3\nA(−2 ; 0): 0 = −4a + q, so q = 4a\na + 4a = 3, so a = {3}/{5}\nq = 4({3}/{5}) = {12}/{5}"],
        0,                                                                                                                 # (−2)² taken as −4
        ["Which two points on f do you know the coordinates of?", "What two equations do you get when you substitute them into "
                                                                  "f(x) = ax² + q?"], after=["5.2.1"]),
    work("5.3.1", "Determine the length of CD.", 2, [
        "C(0 ; 4), D(0 ; 3)\nCD = 4 − 3\nCD = 1 unit",           # the sign of D's y-value lost
        "C(0 ; 4), D(0 ; −4)\nCD = 4 − (−4)\nCD = 8 units",      # D taken on the asymptote
        "C(0 ; 3), D(0 ; −3)\nCD = 3 − (−3)\nCD = 6 units",      # C read at E's height
        "C(0 ; 4), D(0 ; −3)\nCD = 4 − (−3)\nCD = 7 units"], 3,  # the memo
        ["On which axis do C and D both lie?", "How do you find the distance between two points on the same vertical line?"],
        after=["5.1.1", "5.2.2"]),
    work("5.3.2", "Determine the equation of a straight line through A and D.", 3, [
        "m = {0 − (−2)}/{−3 − 0} = −{2}/{3}\n0 = −{2}/{3}(−2) + c\nc = −{4}/{3}\ny = −{2}/{3}x − {4}/{3}",   # the gradient upside down
        "m = {−3 − 0}/{0 − (−2)} = −{3}/{2}\n0 = −{3}/{2}(−2) + c\nc = −3\ny = −{3}/{2}x − 3",            # the memo
        "m = {−3 − 0}/{0 − 2} = {3}/{2}\n0 = {3}/{2}(−2) + c\nc = 3\ny = {3}/{2}x + 3",                   # the sign of A's x lost
        "m = {−3 − 0}/{0 − (−2)} = −{3}/{2}\n0 = −{3}/{2}(−2) + c\nc = 3\ny = −{3}/{2}x + 3"], 1,        # a sign slip finding c
        ["What is the gradient between A and D?", "Which of the two points gives you the y-intercept straight away?"],
        after=["5.1.1", "5.2.1"]),
    mcq("5.4.1", "For which values of x is f(x) > 0?" + ANSWER, ["x < −2 or x > 2", "−2 ≤ x ≤ 2", "0 < x < 2", "−2 < x < 2"], 3,
        ["Where is the parabola above the x-axis?", "Are the x-intercepts themselves included?"], marks=2, after=["5.2.1"]),
    mcq("5.4.2", "For which values of x is f decreasing?" + ANSWER, ["x < 0", "x > 0", "x > 1", "y > 0"], 1,
        ["Where is the turning point of f?", "On which side of it does the graph go down as x increases?"])]

# ---- QUESTION 6, the question paper page 6 and the memo page 8 ----
q6 = [
    work("6.1.1", "Determine the equation of g.", 3, [
        "q = 1\n2 = {a}/{3} + 1\na = 3\ng(x) = {3}/{x} + 1",          # the memo
        "q = 1\n2 = {a}/{3} + 1\na = {1}/{3}\ng(x) = {1}/{3x} + 1",   # a/3 = 1 solved by dividing
        "q = −1\n2 = {a}/{3} − 1\na = 9\ng(x) = {9}/{x} − 1",         # the asymptote's sign
        "q = 1\n3 = {a}/{2} + 1\na = 4\ng(x) = {4}/{x} + 1"], 0,      # the point read as (2 ; 3)
        ["What does the range tell you about the horizontal asymptote, and so about q?", "How can the point (3 ; 2) give you a?"]),
    mcq("6.1.2", "Determine the equation of h, the axis of symmetry of g which has a positive gradient." + ANSWER,
        ["h(x) = x + 1", "h(x) = −x + 1", "h(x) = x − 1", "h(x) = x"], 0,
        ["Where do the asymptotes of g cross?", "What gradient does an axis of symmetry of a hyperbola have?"], marks=2),
    draw("6.2", "Sketch the graphs of g and h on the same system of axes. Clearly show ALL the asymptotes and intercepts with axes.", 4, [
        ["Shape of g: two branches, top right and bottom left of its asymptotes", 1], ["Asymptotes of g: x = 0 and y = 1", 1],
        ["h a straight line with a positive gradient", 1], ["x-intercepts of g (−3 ; 0) and h (−1 ; 0)", 1]],
        ["Where are the asymptotes of g, and in which quadrants of them do its branches lie?", "Where do g and h cut the x-axis?"],
        memo="The memo's sketch: g's two branches about the dashed asymptotes x = 0 and y = 1, one in the top right (falling towards "
             "y = 1) and one in the bottom left, cutting the x-axis at (−3 ; 0); h the straight line y = x + 1 through (−1 ; 0) and "
             "(0 ; 1), crossing both branches of g.", after=["6.1.1", "6.1.2"]),
    work("6.3", "Write the equations of the asymptotes of f if f(x) = −g(x) + 5.", 3, [
        "f(x) = −{3}/{x} + 1 + 5\nf(x) = −{3}/{x} + 6\nx = 0 and y = 6",           # the minus not taken into the bracket
        "f(x) = −({3}/{x} + 1 + 5)\nf(x) = −{3}/{x} − 6\nx = 0 and y = −6",        # the + 5 put inside the bracket
        "f(x) = −({3}/{x} + 1) + 5\nf(x) = −{3}/{x} + 4\nx = 0 and y = 4",         # the memo
        "f(x) = −({3}/{x} + 1) + 5\nf(x) = −{3}/{x} + 4\nx = 4 and y = 0"], 2,     # x and y swapped
        ["What is f(x) when you replace g(x) with its equation?", "How do the reflection and the shift move the asymptotes of g?"],
        after=["6.1.1"])]

# ---- QUESTION 7, the question paper page 6 and the memo page 9 ----
q7 = [
    work("7.1", "Calculate the total amount to be paid over a period of 24 months.", 1, [
        "Total amount paid = R229 × 12\n= R2 748",      # one year's payments
        "Total amount paid = R229 × 2\n= R458",         # 2 years for 24 months
        "Total amount paid = {R229}/{24}\n= R9,54",     # divided instead of multiplied
        "Total amount paid = R229 × 24\n= R5 496"], 3,  # the memo
        ["How many payments are there?", "How much is each payment?"]),
    work("7.2", "The monthly instalment, quoted in the advertisement, is calculated on a hire purchase agreement which charges interest of "
         "7,5% p.a. on the cash price of the cellphone. Show that the price of the cellphone is R4 779,13.", 2, [
        "A = P(1 + i·n)\n5 496 = P(1 + 0,75 × 2)\nP = {5 496}/{2,5} = R4 779,13",            # 7,5% written 0,75
        "A = P(1 + i·n)\n5 496 = P(1 + 0,075 × 2)\nP = {5 496}/{1,15} = R4 779,13",          # the memo
        "A = P(1 + i)ⁿ\n5 496 = P(1 + 0,075)²\nP = {5 496}/{1,155625} = R4 779,13",          # compound interest for hire purchase
        "A = P(1 + i·n)\n5 496 = P(1 + 0,075 × 24)\nP = {5 496}/{2,8} = R4 779,13"], 1,      # n in months with a yearly rate
        ["Is hire purchase interest simple or compound?", "What are A, i and n here?"], after=["7.1"]),
    work("7.3", "Calculate the total interest paid over a period of 24 months if the cellphone is bought with this hire purchase agreement.", 1, [
        "Interest = R4 779,13 × 0,075\n= R358,43",               # one year's interest only
        "Interest = R5 496 × 0,075\n= R412,20",                  # the rate on the total paid
        "Interest = R5 496 − R4 779,13\n= R716,87",              # the memo
        "Interest = R4 779,13 × 0,075 × 24\n= R8 602,43"], 2,    # n in months
        ["What is paid in total, and what is the cash price?", "The interest is the difference between which two amounts?"], after=["7.1"]),
    work("7.4", "The cellphone is insured at 11,5% p.a of the cash price. The total insurance is calculated and then split up over 24 months. "
         "It is then added to the monthly instalment. Calculate the new monthly instalment if the customer wants to insure the cellphone.", 3, [
        "Insurance per month = {R4 779,13 × 0,115}/{12}\n= R45,80\nNew instalment = R229 + R45,80 = R274,80",      # the memo
        "Insurance per month = {R4 779,13 × 0,115}/{24}\n= R22,90\nNew instalment = R229 + R22,90 = R251,90",      # one year's insurance over 24 months
        "Insurance per month = R229 × 0,115\n= R26,34\nNew instalment = R229 + R26,34 = R255,34",                 # 11,5% of the instalment
        "Insurance per month = R4 779,13 × 0,115\n= R549,60\nNew instalment = R229 + R549,60 = R778,60"], 0,      # a year's insurance added each month
        ["What is 11,5% of the cash price for one year?", "How much of that falls in each month?"]),
    work("7.5", "The cost of the cellphone is subject to inflation and increases to a cash price of R5 100,00 after 2 years. Calculate the "
         "annual inflation rate.", 4, [
        "A = P(1 + i·n)\n5 100 = 4 779,13(1 + 2i)\ni = {1,067139835… − 1}/{2} = 0,0336…\nInflation rate = 3,36%",   # simple growth
        "A = P(1 + i)ⁿ\n5 100 = 4 779,13(1 + i)²⁴\ni = ²⁴√1,067139835… − 1 = 0,0027…\nInflation rate = 0,27%",      # n in months
        "A = P(1 − i)ⁿ\n5 100 = 4 779,13(1 − i)²\ni = 1 − √1,067139835… = −0,0330…\nInflation rate = −3,30%",       # the depreciation formula
        "A = P(1 + i)ⁿ\n5 100 = 4 779,13(1 + i)²\ni = √1,067139835… − 1 = 0,0330…\nInflation rate = 3,30%"], 3,     # the memo
        ["Which formula fits a price that grows by a percentage of its new value each year?", "What are A, P and n here?"])]

# ---- QUESTION 8, the question paper page 7 and the memo page 10 ----
q81 = [
    work("8.1.1(a)", "Calculate P(B).", 2, [
        "P(B) = 1 + P(B′)\n= 1 + {3}/{8}\n= {11}/{8}",                  # the complement added
        "P(B) = 1 − P(B′)\n= 1 − {3}/{8}\n= {5}/{8}",                   # the memo
        "P(B) = 1 − P(A)\n= 1 − {2}/{5}\n= {3}/{5}",                    # the complement of A
        "P(B) = P(A or B) − P(B′)\n= {5}/{7} − {3}/{8}\n= {19}/{56}"], 1,  # a made-up identity
        ["How are the probabilities of an event and its complement related?", "Which given value belongs to the complement of B?"]),
    work("8.1.1(b)", "Calculate P(A and B).", 3, [
        "P(A and B) = P(A) × P(B)\n= {2}/{5} × {5}/{8}\nP(A and B) = {1}/{4} = 0,25",                                   # independence assumed
        "P(A or B) = P(A) + P(B) + P(A and B)\n{5}/{7} = {2}/{5} + {5}/{8} + P(A and B)\nP(A and B) = −{87}/{280} = −0,31",  # + P(A and B)
        "P(A or B) = P(A) + P(B) − P(A and B)\n{5}/{7} = {2}/{5} + {5}/{8} − P(A and B)\nP(A and B) = {87}/{280} = 0,31",   # the memo
        "P(A or B) = P(A) + P(B) − P(A and B)\n{5}/{7} = {2}/{5} + {3}/{8} − P(A and B)\nP(A and B) = {17}/{280} = 0,06"], 2,  # P(B′) for P(B)
        ["Which identity links P(A or B), P(A), P(B) and P(A and B)?", "Which value in it do you not know yet?"], after=["8.1.1(a)"]),
    # 1 + 1: the choice (NOT) and the reason; the wrong cards are false here (P(A) + P(B) = 41/40, P(A or B) = 5/7)
    stmt("8.1.2", "Hence, determine whether events A and B are mutually exclusive. Motivate your answer.", 2,
         ["A and B are not mutually exclusive events.", "P(A and B) ≠ 0"],
         ["A and B are mutually exclusive events.", "P(A and B) = 0", "P(A or B) = P(A) + P(B)", "P(A) + P(B) = 1"],
         ["What is P(A and B) for two mutually exclusive events?", "Is your answer to 8.1.1(b) zero?"], 1)]
q82 = [
    mcq("8.2.1", "The shaded region in diagram 8.2.1" + ANSWER, ["P(A or B)′", "P(A or B)", "P(A and B)′", "P(A and B)"], 3,
        ["Which outcomes does the shaded part contain?", "How do 'and' and 'or' differ in probability notation?"]),
    mcq("8.2.2", "The shaded region in diagram 8.2.2" + ANSWER, ["P(A and B)", "P(A or B)′", "P(A or B)", "P(A and B)′"], 1,
        ["Is any part of circle A or circle B shaded?", "What does a dash (′) after an event mean?"]),
    # a memo slip (flagged): the memo's P(A and B)′ also takes in the unshaded outside. Murci's ruling (2026-10-10, a memo value the
    # paper contradicts): the memo's answer AND the right one both earn the mark, so this is a pick of one with both right
    {"t": "pickn", "n": "8.2.3", "marks": 1, "q": "The shaded region in diagram 8.2.3\n\nPick ONE.",
     "clues": ["Which part of the circles is left unshaded?", "How is 'not' written in probability notation?"],
     "opts": ["P(A and B)′", "P(A or B) − P(A and B)", "P(A or B)′", "P(A)"], "pool": [0, 1], "count": 1}]
q83 = [
    # a memo slip (flagged): the memo answers 8.2.3, but the circles overlap in all three diagrams, so none shows mutually exclusive
    # events. Murci's ruling: the memo's answer AND the right one ("None of them") both earn the mark (a pick of one, both right)
    {"t": "pickn", "n": "8.3", "marks": 1,
     "q": "Which diagram(s) in QUESTIONS 8.2.1, 8.2.2 or 8.2.3 represent mutually exclusive events?\n\nPick ONE.",
     "clues": ["What does 'mutually exclusive' mean?", "Can two mutually exclusive events have outcomes in common?"],
     "opts": ["8.2.1", "8.2.2", "8.2.3", "None of them"], "pool": [2, 3], "count": 1}]

DOTS = {"head": ["Pattern number:", "1", "2", "3"], "rows": [["Number of dots:", "1² = 1", "1 + 3 = 2² = 4", "1 + 3 + 5 = 3² = 9"]]}
# (no region named: which region is shaded is what 8.2.1-8.2.3 ask; the caption shows in the enlarged view, 2026-10-11)
VENN = ("Three Venn diagrams, labelled 8.2.1, 8.2.2 and 8.2.3 from top to bottom, each a rectangle holding two overlapping circles, A on "
        "the left and B on the right, with a different region shaded in each.")
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Factorisation", "marks": 7, "lead": "Factorise the following expressions fully:", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Simplifying expressions", "marks": 8, "lead": "Simplify the following expressions fully:",
     "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Algebraic expressions", "marks": 3, "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Equations", "marks": 8, "lead": "Solve for x:", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Linear inequalities", "marks": 3, "lead": "Given: −11 ≤ 3m − 8 < 4", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Simultaneous equations", "marks": 4, "items": q23},
    {"id": "3", "title": "Question 3", "kind": "Linear patterns", "marks": 10, "lead": "Consider the finite linear pattern: 20 ; 17 ; 14 ; … ; −103",
     "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Number patterns", "marks": 6,
     "lead": "Samantha is investigating a pattern of dots represented in the diagram below.", "table": DOTS,
     "figure": fig("Q4", "Three dot patterns side by side, numbered 1, 2 and 3 from left to right. Pattern 1 is one dot in a small square. "
                   "Pattern 2 is a larger square: the square of pattern 1 in its top-left corner with an L-shaped band of dots round it. "
                   "Pattern 3 is a still larger square: pattern 2 in its top-left corner with a wider L-shaped band of dots round it."),
     "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Parabola and exponential graph", "marks": 17,
     "lead": "Sketched below are the graphs of f(x) = ax² + q and g(x) = (1/2)ˣ − 4.\nA and B are the x-intercepts of f. The graphs "
             "intersect at A and point E(1 ; 3) lies on f.\nC is the turning point of f and D is the y-intercept of g.",
     "figure": fig("Q5", "The parabola f opens downwards: its turning point C is where it cuts the y-axis, above the origin O. f cuts the "
                   "x-axis at A, left of O, and at B, right of O, and passes through E(1 ; 3) on its way down from C to B. The exponential "
                   "graph g comes down from the top left, crosses the x-axis at A where it meets f, cuts the y-axis at D below O, and levels "
                   "off towards a dashed horizontal asymptote that lies below D."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Hyperbolas", "marks": 12,
     "lead": "The equation of the function g(x) = a/x + q passes through the point (3 ; 2) and has a range of y ∈ (−∞ ; 1) ∪ (1 ; ∞).",
     "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Hire purchase and inflation", "marks": 11, "lead": "Read the advertisement below.",
     "extract": "Buy a Samsung J5 for only R229 per month.\n\nYou have 24 months to pay.\nNo deposit is required.", "items": q7},
    {"id": "8.1", "title": "Question 8.1", "kind": "Probability rules", "marks": 7,
     "lead": "In a random physical sciences experiment, A and B are two different events. It was found that:\nP(A) = 2/5, P(B′) = 3/8 and "
             "P(A or B) = 5/7", "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Venn diagrams", "marks": 3,
     "lead": "The Venn diagrams below represent different scenarios of events A and B.\n\nWrite down the probability of the shaded region for "
             "EACH of the diagrams below.", "figure": fig("Q8", VENN), "items": q82},
    {"id": "8.3", "title": "Question 8.3", "kind": "Mutually exclusive events", "marks": 1, "figure": fig("Q8", VENN), "items": q83},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.1.1", "1.1.3", "1.2.1", "1.2.2", "1.2.3", "1.3", "2.1.1", "2.1.2", "2.1.3", "2.2.1", "2.3", "3.2", "3.3", "3.4",
                           "3.5", "4.2", "5.2.1", "5.2.2", "5.3.1", "5.3.2", "6.1.1", "6.3", "7.1", "7.2", "7.3", "7.4", "7.5", "8.1.1(a)",
                           "8.1.1(b)"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["1.1.2", "4.1.3", "5.1.1", "5.1.2", "5.4.1", "5.4.2", "6.1.2", "8.2.1", "8.2.2"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["2.2.2", "3.1", "4.1.1", "4.1.2"]   # the read-off numbers
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["6.2"]
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn"]
assert PICKS == ["8.1.2", "8.2.3", "8.3"], PICKS
assert {i["n"]: i["after"] for i in ITEMS if i.get("after")} == {
    "3.3": ["3.2"], "3.4": ["3.2"], "3.5": ["3.2"],          # Tₙ = −3n + 23
    "4.2": ["4.1.3"],                                         # total dots = n²
    "5.2.2": ["5.2.1"], "5.3.2": ["5.1.1", "5.2.1"], "5.4.1": ["5.2.1"],   # A(−2 ; 0) (and D(0 ; −3))
    "5.3.1": ["5.1.1", "5.2.2"],                              # C(0 ; 4) and D(0 ; −3)
    "6.2": ["6.1.1", "6.1.2"], "6.3": ["6.1.1"],              # g(x) = 3/x + 1 (and h's x-intercept)
    "7.2": ["7.1"], "7.3": ["7.1"],                           # R5 496
    "8.1.1(b)": ["8.1.1(a)"]}                                 # P(B) = 5/8
for i in ITEMS:   # a line that ends in "[...]" draws as a proof's reason: no working here has one
    assert i["t"] != "mcq" or not any(shape(o)[1] for o in i["opts"]), i["n"]
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2018", "total_marks": 100, "time": "2 hours"},
    "sections": [{"title": "Mathematics", "total": 100, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines (a factorisation, a simplification, a solution, a value, a 'show that') plays as "
                                                       "four workings, the memo's FIRST method line by line and three built from real errors (a "
                                                       "sign slip, a step not distributed, a wrong formula or rate, a misread value, a wrong "
                                                       "count), one step a line, 0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, %d "
                                                       "marks). In the 'show that' (7.2) every option ends in the given R4 779,13; a wrong one "
                                                       "reaches it through a wrong step." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.1.2", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                   "with no working (a factorised trinomial, a formula, a coordinate, a range, an interval, an "
                                                   "axis of symmetry, probability notation, a choice of diagrams) that a word marker cannot read "
                                                   "(y > −4 from y ≥ −4, P(A or B)′ from P(A and B)′): four options, the memo's answer and three "
                                                   "common errors, 0 or full marks."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 8), hand-transcribed from a SCANNED question paper (no "
                                                           "text layer) and the memo's page images (its text layer garbles fractions and powers); "
                                                           "no API call."},
        {"n": "2.2.2", "kind": "no_fit", "detail": "Read-off numbers with no working stay typed on the keypad: 2.2.2 (5 integers), 3.1 (T₄ = 11), "
                                                   "4.1.1 (16 dots) and 4.1.2 (169 dots); the memo writes 4² = 16 and 13² = 169, the answer as a "
                                                   "square, not a working."},
        {"n": "6.2", "kind": "no_fit", "detail": "The sketch of g and h is drawn on paper and self-checked against the memo's four criteria (its "
                                                 "fourth, 'x intercepts of g and h', ends in a stray '6' in the memo, read as noise)."},
        {"n": "8.1.2", "kind": "no_fit", "detail": "The choice with its reason plays as statements: the memo's NOT (1) and its reason "
                                                   "P(A and B) ≠ 0 (1) are the two right cards; the wrong cards are false for these events "
                                                   "(P(A) + P(B) = 41/40, P(A or B) = 5/7)."},
        {"n": "1.3", "kind": "memo_issue", "detail": "The paper's data has no real solution: 9p² + q² = 12 with pq = −3 gives (3p + q)² = 12 + 6(−3) "
                                                     "= −6, a square below zero (9p² + q² ≥ 2|3pq| = 18 > 12 for real p and q). The memo's working "
                                                     "is the algebra the question asks for, so it plays as the memo (−6); a learner who knows a square "
                                                     "cannot be negative may doubt it. A teacher should confirm."},
        {"n": "3.5", "kind": "memo_issue", "detail": "The memo writes T₃₉ = −3(37) + 23 = −88 and ticks 'T₃₉': the 19th even-valued term is T₃₇ "
                                                     "(even values at n = 1 ; 3 ; 5 ; …), and −88 is T₃₇. The right option labels it T₃₇ with the "
                                                     "memo's value; T₃₉ = −94 (the 20th even-valued term) is a wrong option."},
        {"n": "6.3", "kind": "memo_issue", "detail": "The memo numbers this part 6.4 (the paper has no 6.4) and writes g(x) = −(3/x + 1) + 5 for "
                                                     "f(x); the working and the asymptotes x = 0 and y = 4 are f's, played as such."},
        {"n": "8.2.3", "kind": "memo_issue", "detail": "The memo's P(A ∩ B)′ (P(A and B)′) also takes in the part of the rectangle outside both "
                                                       "circles, which diagram 8.2.3 leaves UNSHADED (checked on the scan: white outside the "
                                                       "circles); the shaded region is A or B but not both, P(A or B) − P(A and B). Murci's memo-"
                                                       "slip ruling: a pick of one where the memo's answer AND P(A or B) − P(A and B) both earn "
                                                       "the mark. A teacher should confirm."},
        {"n": "8.3", "kind": "memo_issue", "detail": "The memo answers 8.2.3, but in all three diagrams the circles A and B overlap, so none of them "
                                                     "shows A and B as mutually exclusive events; the memo reads 8.2.3's two shaded pieces (A only, "
                                                     "B only), which cannot happen together. Murci's memo-slip ruling: a pick of one where the "
                                                     "memo's 8.2.3 AND 'None of them' both earn the mark. A teacher should confirm."},
    ],
}
QTOTAL = {"1": 18, "2": 15, "3": 10, "4": 6, "5": 17, "6": 12, "7": 11, "8": 11}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
assert per_q == QTOTAL, per_q
# the right option, spread evenly over A-D across the paper (and across the authored workings)
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
worked = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(worked.values()) - min(worked.values()) <= 1, worked
print("right options, the paper:", spread, "authored workings:", worked)
total = sum(i["marks"] for i in ITEMS)
assert total == 100, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts")
print("total:", total)
out = Path(__file__).parent / "out" / "g10-math-p1-2018-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the memo's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 8 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
