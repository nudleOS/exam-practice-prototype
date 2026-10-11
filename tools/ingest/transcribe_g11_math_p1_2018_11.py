"""Grade 11 Mathematics P1 Nov 2018 (DBE common paper), the whole paper (Questions 1 to 9, 150 marks, 3 hours as the cover
prints them), hand-transcribed into the catalogue format, then run through `ingest.py --from-json` like any ingested paper.
Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are
ours. No API call: the transcription is the source, kept in git (out/ is not). The question paper is a SCAN (no text layer; its
pages 1-8 are English, 9-16 the Afrikaans copy): read from its page images rendered at 150 dpi, exponents (2.1, 2.2.1, 2.2.3,
2.3) checked on crops at 250 dpi. The memo is a scan too (no text layer): read from its page images at 150 dpi, zoomed to 250
dpi where a digit mattered (1.1.2's numerator, 1.1.4's mark column).

  python tools/ingest/transcribe_g11_math_p1_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Mathematics P1 Nov 2018 Eng.pdf" "uploads/Grade 11 Mathematics P1 Nov 2018 MG Afr & Eng.pdf" --id g11-math-p1-2018-11 --from-json

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p1_2025_11.py and the Grade 10 pilots
transcribe_g10_math_p1_2018_11.py / transcribe_g10_math_p1_2017_11.py):
  Every value, expression or set the memo WORKS OUT in two or more lines (solve, simplify, calculate, determine, show that, a
  'write down' whose memo shows a working: 5.7, 6.7) -> authored whole-working multiple choice, `work`: the memo's FIRST method
  line by line ("{a}/{b}" a stacked fraction, a fractional power written ^(a/b)) and three workings each built from a DIFFERENT
  real error, every option of a part the same layout (`shape`), the right one's place spread over A-D across the paper; the part
  keeps its marks, all or nothing. In a 'show that' (1.4, 4.1, 8.1) every option ends in the given result: a wrong one reaches it
  through a wrong step or by starting from the answer. A form the memo ALSO accepts never appears in a wrong option (6.5's x ≥ 3,
  9.1's OR with vegetarian and female, 7.3.2's OR value R30 871,48, which is also the right chain's value).
  An answer the memo states with no working (a pair of roots, asymptotes, an interval, a coordinate, a range) -> authored multiple
  choice of answers: the memo's and three common errors. 6.1 (y = −4) is one too, not a term: the term marker drops the minus sign,
  so y = 4 would pass.
  The tree diagram 8.2 -> draw (self-checked against the memo's criteria); the sketch 5.4 -> draw with build "sketch" (2026-10-11:
  f and g placed on one grid, each curve drawn through its features, marked online against the memo's five criteria); 9.2.1 (a
  choice and its reason) -> statements, 1 mark each.
  Where a part's stem, options or criteria show an EARLIER part's answer it carries "after" (the assert at the end).
Missions: Questions 4, 5, 6 and 8 share one stem (a pattern, two functions, a graph, a bag of balls), so each is one mission;
Questions 1, 2, 3, 7 and 9 are their numbered groups (1.1, 1.2, ...; 9.1 with its table).
The figure box is measured in PDF points (page 595 x 841, read from the PDF) from the ink on the scan (scratch tool
lower/g11-math-p1-2018-11/figs.py) and checked on the padded crop (ingest's 1% pad applied)."""
import json
import random
import re
from pathlib import Path

PID = "g11-math-p1-2018-11"
W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q6": [6, 149.8, 193.1, 442.8, 394.0]}   # f, g, the axes and the points A-E (the dotted asymptote of g included)


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


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
    print("statements", n, "right cards at", pool, "of", len(opts))
    assert pool[0] != 0 and pool != list(range(len(pool))), (n, "a right card first, or all right cards on top", pool)
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count, **kw}


# ---- QUESTION 1, the question paper page 3 and the memo pages 2-5 ----
K = "Let √(2x + 5) = k: k − {3}/{k} = −2\nk² − 3 = −2k\n"
q11 = [
    mcq("1.1.1", "x(2x + 1) = 0" + ANSWER, ["x = 0 or x = {1}/{2}", "x = 0 or x = −{1}/{2}", "x = −{1}/{2} only", "x = 0 or x = −2"], 1,
        ["When is a product of two factors equal to zero?", "How many factors does x(2x + 1) have, and what equation does each give?"], marks=2),
    work("1.1.2", "5x² + 2x − 6 = 0 (correct to TWO decimal places)", 3, [
        "x = {−b ± √(b² − 4ac)}/{2a}\nx = {−(2) ± √((2)² − 4(5)(−6))}/{2(5)}\nx = {−2 ± √124}/{10}\nx = 0,91 or x = −1,31",   # the memo (its 5 ± √124 a slip)
        "x = {−b ± √(b² − 4ac)}/{a}\nx = {−(2) ± √((2)² − 4(5)(−6))}/{5}\nx = {−2 ± √124}/{5}\nx = 1,83 or x = −2,63",         # divided by a, not 2a
        "x = {b ± √(b² − 4ac)}/{2a}\nx = {2 ± √((2)² − 4(5)(−6))}/{2(5)}\nx = {2 ± √124}/{10}\nx = 1,31 or x = −0,91",          # b for −b
        "x = {−b ± √(b² − 4ac)}/{2a}\nx = {−(2) ± √((2)² − (5)(−6))}/{2(5)}\nx = {−2 ± √34}/{10}\nx = 0,38 or x = −0,78"], 0,  # the 4 of 4ac dropped
        ["Does the trinomial factorise, or do you need the quadratic formula?", "What are a, b and c, and what does b² − 4ac come to?"]),
    work("1.1.3", "2x² − 2 ≥ 3x", 4, [
        "2x² − 3x − 2 ≥ 0\n(2x + 1)(x − 2) ≥ 0\n−{1}/{2} ≤ x ≤ 2",              # the region between the roots
        "2x² − 3x − 2 ≥ 0\n(2x − 1)(x + 2) ≥ 0\nx ≤ −2 or x ≥ {1}/{2}",        # the signs in the factors swapped
        "2x² − 3x − 2 ≥ 0\n(2x + 1)(x − 2) ≥ 0\nx ≤ −{1}/{2} or x ≥ 2",        # the memo
        "2x² − 3x − 2 ≥ 0\n(2x + 1)(x − 2) ≥ 0\nx < −{1}/{2} or x > 2"], 2,    # the end points left out
        ["What do you get when you move every term to one side?", "Where is the parabola y = 2x² − 3x − 2 on or above the x-axis?"]),
    work("1.1.4", "√(2x + 5) − 3/√(2x + 5) = −2", 6, [
        K + "k² + 2k − 3 = 0, so (k − 3)(k + 1) = 0\nk = 3 or k = −1\n√(2x + 5) = 3; or √(2x + 5) = −1: no solution\n2x + 5 = 9, so x = 2",  # factor signs
        K + "k² + 2k − 3 = 0, so (k + 3)(k − 1) = 0\nk = −3 or k = 1\n√(2x + 5) = −3: no solution; or √(2x + 5) = 1\n2x + 5 = 1, so x = −2",  # the memo
        K + "k² + 2k − 3 = 0, so (k + 3)(k − 1) = 0\nk = −3 or k = 1\n√(2x + 5) = −3 or √(2x + 5) = 1\n2x + 5 = 9 or 2x + 5 = 1, so x = 2 or "
            "x = −2",                                                                                                              # k = −3 kept
        K + "k² + 2k − 3 = 0, so (k + 3)(k − 1) = 0\nk = −3 or k = 1\n√(2x + 5) = −3: no solution; or √(2x + 5) = 1\n2x + 5 = 1, so x = 3"],  # 5 moved without its sign
        1, ["Which expression appears twice: what happens if you call it k?", "Can a square root ever equal a negative number?"])]
q12 = [
    work("1.2", "Solve for x and y simultaneously:\ny + x = 2 and x² + 3xy + 8 = 0", 6, [
        "y = 2 − x\nx² + 3x(2 − x) + 8 = 0\nx² + 6x − 3x² + 8 = 0\n−2x² + 6x + 8 = 0, so x² − 3x − 4 = 0\n(x + 4)(x − 1) = 0\nx = −4 or x = 1\n"
        "y = 6 or y = 1",                                                       # the signs in the factors swapped
        "y = 2 − x\nx² + 3x(2 − x) + 8 = 0\nx² + 6 − 3x² + 8 = 0\n−2x² + 14 = 0, so x² = 7\nx = ±√7\nx = 2,65 or x = −2,65\n"
        "y = −0,65 or y = 4,65",                                                # 3x × 2 taken as 6
        "y = 2 − x\nx² + 3x(2 − x) + 8 = 0\nx² + 6x − 3x² + 8 = 0\n−4x² + 6x + 8 = 0, so 2x² − 3x − 4 = 0\nx = {3 ± √41}/{4}\n"
        "x = 2,35 or x = −0,85\ny = −0,35 or y = 2,85",                        # x² − 3x² taken as −4x²
        "y = 2 − x\nx² + 3x(2 − x) + 8 = 0\nx² + 6x − 3x² + 8 = 0\n−2x² + 6x + 8 = 0, so x² − 3x − 4 = 0\n(x − 4)(x + 1) = 0\nx = 4 or x = −1\n"
        "y = −2 or y = 3"], 3,                                                  # the memo
        ["Which equation is easier to make x or y the subject of?", "After substituting, what quadratic do you get, and does it factorise?"])]
q13 = [
    work("1.3", "The roots of the equation f(x) = 0 are x = (4 ± √(16 − 4m(−m + 5)))/(2m)\n\nDetermine the values of m for which the roots will be "
         "non-real.", 4, [
        "Non-real roots: 16 − 4m(−m + 5) ≤ 0\n16 + 4m² − 20m ≤ 0\nm² − 5m + 4 ≤ 0\n(m − 4)(m − 1) ≤ 0\n1 ≤ m ≤ 4",          # equal roots taken in
        "Non-real roots: 16 − 4m(−m + 5) < 0\n16 + 4m² − 20m < 0\nm² − 5m + 4 < 0\n(m − 4)(m − 1) < 0\n1 < m < 4",          # the memo
        "Non-real roots: 16 − 4m(−m + 5) > 0\n16 + 4m² − 20m > 0\nm² − 5m + 4 > 0\n(m − 4)(m − 1) > 0\nm < 1 or m > 4",    # the condition for real roots
        "Non-real roots: 16 − 4m(−m + 5) < 0\n16 + 4m² + 20m < 0\nm² + 5m + 4 < 0\n(m + 4)(m + 1) < 0\n−4 < m < −1"], 1,    # −4m × 5 taken as +20m
        ["Which part of the formula decides the nature of the roots?", "Once you have an inequality in m, how do you solve a quadratic "
                                                                       "inequality?"])]
q14 = [
    work("1.4", "Show that the maximum value of √(−x² + 4x + 12) is 4.", 4, [
        "−x² + 4x + 12 = −1(x² − 4x − 12)\n= −1(x² − 4x + 4 − 4 − 12)\n= −1(x − 2)² + 16\nThe maximum value of −x² + 4x + 12 is 16\n"
        "So the maximum value of √(−x² + 4x + 12) is √16 = 4",                                     # the memo
        "√(−x² + 4x + 12) = 4\n−x² + 4x + 12 = 16\nx² − 4x + 4 = 0, so (x − 2)² = 0\nx = 2 gives the value 4\n"
        "So the maximum value of √(−x² + 4x + 12) is 4",                                           # starts from the answer
        "x = 0: √12 = 3,46\nx = 1: √15 = 3,87\nx = 2: √16 = 4\nx = 3: √15 = 3,87\n"
        "So the maximum value of √(−x² + 4x + 12) is 4",                                           # a few values tried: no proof of a maximum
        "−x² + 4x + 12 = −1(x² + 4x − 12)\n= −1(x² + 4x + 4 − 4 − 12)\n= −1(x + 2)² + 16\nThe maximum value of −x² + 4x + 12 is 16, at x = −2\n"
        "So the maximum value of √(−x² + 4x + 12) is √16 = 4"], 0,                                 # −1 taken out without changing 4x's sign
        ["Where does the expression under the root reach its largest value?", "How can completing the square on −x² + 4x + 12 show that "
                                                                              "largest value?"])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 6-8 ----
SPLIT = "= {2ˣ · 2⁻³ − 3 · 2ˣ · 2¹}/{2ˣ · 2⁻²}\n= {2ˣ(2⁻³ − 3 · 2)}/{2ˣ · 2⁻²}\n"
q21 = [
    work("2.1", "Simplify fully, WITHOUT using a calculator: (2ˣ⁻³ − 3 · 2ˣ⁺¹)/2ˣ⁻²", 4, [
        SPLIT + "= (−8 − 6) ÷ (−4)\n= {7}/{2}",                                                                     # 2⁻³ and 2⁻² taken as −8 and −4
        "= {2ˣ · 2⁻³ − 3 · 2ˣ}/{2ˣ · 2⁻²}\n= {2ˣ(2⁻³ − 3)}/{2ˣ · 2⁻²}\n= ({1}/{8} − 3) ÷ {1}/{4}\n= −{23}/{2}",       # the 2¹ of 2ˣ⁺¹ lost
        SPLIT + "= ({1}/{8} − 6) × {1}/{4}\n= −{47}/{32}",                                                          # multiplied by 1/4 instead of divided
        SPLIT + "= ({1}/{8} − 6) ÷ {1}/{4}\n= −{47}/{2}"], 3,                                                       # the memo
        ["How can you split 2ˣ⁻³, 2ˣ⁺¹ and 2ˣ⁻² so that each has a factor 2ˣ?", "Once 2ˣ cancels, what are 2⁻³ and 2⁻² as fractions?"])]
SQ = "(2²)ˣ − 9 · 2ˣ + 8 = 0\n2²ˣ − 9 · 2ˣ + 8 = 0\n"
q22 = [
    work("2.2.1", "2 − 16x^(−3/2) = 0", 3, [
        "16x^(−3/2) = 2\nx^(−3/2) = {1}/{8}\n(x^(−3/2))^(−2/3) = (2³)^(−2/3)\nx = {1}/{4}",               # 1/8 written 2³
        "16x^(−3/2) = 2\nx^(−3/2) = 32\n(x^(−3/2))^(−2/3) = (2⁵)^(−2/3)\nx = 2^(−10/3) = 0,10",           # multiplied by 16 instead of divided
        "16x^(−3/2) = 2\nx^(−3/2) = {1}/{8}\n(x^(−3/2))^(−2/3) = (2⁻³)^(−2/3)\nx = 4",                    # the memo
        "16x^(−3/2) = 2\nx^(−3/2) = {1}/{8}\nx = ({1}/{8})^(−3/2) = (2⁻³)^(−3/2)\nx = 2^(9/2) = 22,63"], 2,  # raised to the same power, not its reciprocal
        ["What do you get when you isolate the power of x?", "What power must you raise x^(−3/2) to, to leave x on its own?"]),
    work("2.2.2", "4ˣ + 8 = 9 · 2ˣ", 4, [
        SQ + "(2ˣ − 8)(2ˣ − 1) = 0\n2ˣ = 8 or 2ˣ = 1\n2ˣ = 2³ or 2ˣ = 2⁰\nx = 3 or x = 0",           # the memo
        SQ + "(2ˣ − 8)(2ˣ − 1) = 0\n2ˣ = 8 or 2ˣ = 1\nx = {8}/{2} or x = {1}/{2}\nx = 4 or x = {1}/{2}",  # 2ˣ = 8 solved by dividing by 2
        SQ + "(2ˣ + 8)(2ˣ + 1) = 0\n2ˣ = −8 or 2ˣ = −1\n2ˣ > 0 for every x\nNo solution",             # the signs in the factors
        SQ + "(2ˣ − 8)(2ˣ − 1) = 0\n2ˣ = 8 or 2ˣ = 1\n2ˣ = 2³ or 2ˣ = 2¹\nx = 3 or x = 1"], 0,        # 1 written 2¹
        ["How can you write 4ˣ as a power of 2ˣ?", "If you let k = 2ˣ, what kind of equation do you get?"]),
    work("2.2.3", "ˣ√9 = 243", 3, [
        "3²ˣ = 3⁵\n2x = 5\nx = {5}/{2}",            # the root read as a power
        "3^(2/x) = 3⁵\n{2}/{x} = 5\nx = {2}/{5}",   # the memo
        "3^(2/x) = 3⁴\n{2}/{x} = 4\nx = {1}/{2}",   # 243 written 3⁴
        "3^(2/x) = 3⁵\n{2}/{x} = 5\nx = 10"], 1,    # multiplied instead of divided
        ["How can you write a root as a power with a fractional exponent?", "Can you write 9 and 243 as powers of the same prime?"])]
DS = "= {√((p − q)(p + q)) × (p + q)^(5/2)}/{(p − q)^(1/2)}\n= {(p − q)^(1/2)(p + q)^(1/2) × (p + q)^(5/2)}/{(p − q)^(1/2)}\n"
q23 = [
    work("2.3", "Simplify fully:\n(√(p² − q²) × (p + q)^(5/2))/(p − q)^(1/2) if p ≠ q", 3, [
        DS + "= (p + q)^(1/2 × 5/2)\n= (p + q)^(5/4)",                                                       # the exponents multiplied
        "= {(p − q) × (p + q)^(5/2)}/{(p − q)^(1/2)}\n= (p − q)^(1 − 1/2) × (p + q)^(5/2)\n= (p − q)^(1/2) × (p + q)^(5/2)\n"
        "= √(p − q) × (p + q)^(5/2)",                                                                        # √(p² − q²) taken as p − q
        DS + "= (p + q)^(1/2 + 5/2)\n= (p + q)³",                                                            # the memo
        DS + "= (p + q)^(1/2 + 5/2)\n= (p + q)^(3/2)"], 2,                                                   # 1/2 + 5/2 added as 6/4
        ["Can you factorise p² − q² as a difference of two squares?", "What happens to the exponents when you multiply powers of the same "
                                                                       "base?"])]

# ---- QUESTION 3, the question paper page 4 and the memo page 8 ----
q31 = [
    work("3.1.1", "Determine the general term, Tₙ, of the linear pattern.", 2, [
        "d = 2 − 7 = −5\nTₙ = an + b = −5n + b\nTₙ = −5n + 7",     # the first term taken as b
        "d = 7 − 2 = 5\nTₙ = an + b = 5n + b\nTₙ = 5n + 2",        # the difference taken the wrong way round
        "d = 2 − 7 = −5\nTₙ = an + b = −5n + b\nTₙ = −5n + 2",     # 7 = −5 + b solved as b = 2
        "d = 2 − 7 = −5\nTₙ = an + b = −5n + b\nTₙ = −5n + 12"], 3,  # the memo
        ["What is the constant difference between consecutive terms, and what is its sign?", "Which value of b makes T₁ equal to the first "
                                                                                             "term?"]),
    work("3.1.2", "Calculate the value of T₂₀.", 2, [
        "T₂₀ = 7 + 20(−5)\n= −93",      # a + nd, not a + (n − 1)d
        "T₂₀ = −5(20) + 12\n= −88",     # the memo
        "T₂₀ = −5(20 + 12)\n= −160",    # a bracket round n + 12
        "T₂₀ = −5(19) + 12\n= −83"], 1,  # n − 1 put into a formula already in n
        ["Which value of n stands for the 20th term?", "What do you get when you substitute it into your general term?"], after=["3.1.1"]),
    work("3.1.3", "Which term in the pattern has a value of −138?", 2, [
        "−5n + 12 = −138\n−5n = −150\nn = 30: the 30th term (T₃₀)",               # the memo
        "Tₙ = −5n + 12\nT₋₁₃₈ = −5(−138) + 12\n= 702",                            # −138 taken as the position
        "−5n + 12 = −138\n−5n = −126\nn = 25,2: no term has this value",           # 12 moved without its sign change
        "−5n + 12 = −138\n−5n = −150\nn = {−5}/{−150} = {1}/{30}: no term has this value"], 0,   # the division upside down
        ["Is −138 a position in the pattern or the value of a term?", "Can you set your general term equal to −138 and solve for n?"],
        after=["3.1.1"])]
DIFF = "T₂ − T₁ = (2x + 1) − 6 = 2x − 5\n"
q32 = [
    work("3.2", "6 ; 2x + 1 and 3x − 3 are the first three terms of a linear pattern.\n\nCalculate the value of x.", 3, [
        DIFF + "T₃ − T₂ = 3x − 3 − 2x + 1 = x − 2\n2x − 5 = x − 2\nx = 3",                      # −(2x + 1) taken as −2x + 1
        DIFF + "T₃ − T₂ = (3x − 3) − (2x + 1) = x − 4\n2x − x = −4 − 5\nx = −9",                 # −5 moved without its sign change
        DIFF + "T₃ − T₂ = (3x − 3) − (2x + 1) = x − 4\n2x − 5 = x − 4\nx = 1",                   # the memo
        DIFF + "T₃ − T₂ = (3x − 3) − (2x + 1) = x − 4\n2x + x = −4 + 5\nx = {1}/{3}"], 2,        # x moved without its sign change
        ["What is the same between consecutive terms of a linear pattern?", "What equation do you get when you set the two differences equal?"])]

# ---- QUESTION 4, the question paper page 4 and the memo pages 9-11 ----
FD = "First differences: p − 4 ; 11 − p ; q − 11 ; 22 − q\nSecond differences: −2p + 15 ; q + p − 22 ; 33 − 2q\n"
EQ = "{1}/{2}n² + {3}/{2}n + 2 = 232\n{1}/{2}n² + {3}/{2}n − 230 = 0\n"
SUM = ("Tₙ + Tₙ₊₁ = {1}/{2}n² + {3}/{2}n + 2 + {1}/{2}(n + 1)² + {3}/{2}(n + 1) + 2 = 1 227\nn² + 4n + 6 = 1 227\nn² + 4n − 1 221 = 0\n")
q4 = [
    work("4.1", "Show that p = 7 and q = 16.", 3, [
        "Let p = 7 and q = 16: 4 ; 7 ; 11 ; 16 ; 22\nFirst differences: 3 ; 4 ; 5 ; 6\nSecond differences: 1 ; 1 ; 1\nSo p = 7 and q = 16",  # assumes the answer
        "The second difference is 1, so the first differences are 3 ; 4 ; 5 ; 6\np = 4 + 3 = 7\nq = 11 + 5 = 16\nSo p = 7 and q = 16",      # first difference assumed
        FD + "−2p + 15 = 33 − 2q, so q − p = 9\np = 7 and q = 16 fit q − p = 9",                       # one equation in two unknowns
        FD + "−2p + 15 = 1, so p = 7\n33 − 2q = 1, so q = 16"], 3,                                     # the memo
        ["What are the first differences in terms of p and q?", "What must each second difference equal?"]),
    work("4.2", "Determine the general term, Tₙ, of the quadratic pattern.", 4, [
        "2a = 1, so a = {1}/{2}\n3a + b = 3, so b = {3}/{2}\na + b + c = 4, so c = 2\nTₙ = {1}/{2}n² + {3}/{2}n + 2",     # the memo
        "a = 1 (the second difference)\n3a + b = 3, so b = 0\na + b + c = 4, so c = 3\nTₙ = n² + 3",                       # a taken as the second difference
        "2a = 1, so a = {1}/{2}\n3a + b = 3, so b = {3}/{2}\na + b + c = 4, so c = 6\nTₙ = {1}/{2}n² + {3}/{2}n + 6",     # 2 added instead of subtracted for c
        "2a = 1, so a = {1}/{2}\n3a + b = 3, so b = {9}/{2}\na + b + c = 4, so c = −1\nTₙ = {1}/{2}n² + {9}/{2}n − 1"], 0,  # 3/2 added instead of subtracted for b
        ["How is the second difference related to a in Tₙ = an² + bn + c?", "Which expressions in a, b and c give the first first difference "
                                                                            "and the first term?"]),
    work("4.3", "Determine the value of n if Tₙ = 232.", 4, [
        EQ + "n² + 3n − 460 = 0\n(n − 23)(n + 20) = 0\nn = 23 (n ≠ −20)",            # the signs in the factors swapped
        EQ + "n² + 3n − 460 = 0\n(n + 23)(n − 20) = 0\nn = 20 or n = −23",           # the negative root kept
        EQ + "n² + 3n − 460 = 0\n(n + 23)(n − 20) = 0\nn = 20 (n ≠ −23)",            # the memo
        EQ + "n² + 3n − 230 = 0\nn = {−3 ± √929}/{2}\nn = 13,74 (n ≠ −16,74)"], 2,   # 230 not multiplied by 2
        ["What equation do you get when you set your general term equal to 232?", "Can n, a term's position, be negative or a fraction?"],
        after=["4.2"]),
    work("4.4", "If the sum of two consecutive terms in the pattern is 1 227, calculate the difference between these two terms.", 5, [
        SUM + "(n + 37)(n − 33) = 0, so n = 33 (n ≠ −37)\nT₃₃ − T₃₂ = 596 − 562 = 34",     # the term before T₃₃ taken
        SUM + "(n + 37)(n − 33) = 0, so n = 33 (n ≠ −37)\nT₃₄ − T₃₃ = 631 − 596 = 35",     # the memo
        SUM + "(n + 37)(n − 33) = 0, so n = 33 (n ≠ −37)\nT₃₄ − T₃₃: 34 − 33 = 1",          # the positions subtracted, not the terms
        SUM + "(n − 37)(n + 33) = 0, so n = 37 (n ≠ −33)\nT₃₈ − T₃₇ = 781 − 742 = 39"], 1,  # the signs in the factors swapped
        ["If the first term is Tₙ, how do you write the next one?", "Once you know n, which two terms do you subtract?"], after=["4.2"])]

# ---- QUESTION 5, the question paper page 5 and the memo pages 12-13 ----
X0 = "0 = {4}/{x − 3} + 2\n"
INT = "{4}/{x − 3} + 2 = x + 2\n"
AXIS = "y = x + c through (3 ; 2): 2 = 3 + c, so c = −1\ny = x − 1 is an axis of symmetry of f\n"
q5 = [
    mcq("5.1", "Write down the equations of the asymptotes of f." + ANSWER, ["x = 3 and y = 2", "x = −3 and y = 2", "x = 2 and y = 3",
                                                                             "x = 3 and y = −2"], 0,
        ["Which value of x makes the denominator zero?", "Which value does f(x) approach as x becomes very large?"], marks=2),
    work("5.2", "Determine the x-intercept of f.", 3, [
        X0 + "−2 = {4}/{x − 3}\n−2(x − 3) = 4\n−2x − 6 = 4\nx = −5",                 # −2 × (−3) taken as −6
        X0 + "2 = {4}/{x − 3}\n2(x − 3) = 4\n2x − 6 = 4\nx = 5",                     # 2 moved without its sign change
        X0 + "−2 = {4}/{x − 3}\nx − 3 = −{2}/{4}\nx − 3 = −{1}/{2}\nx = {5}/{2}",    # the fraction turned upside down
        X0 + "−2 = {4}/{x − 3}\n−2(x − 3) = 4\n−2x + 6 = 4\nx = 1"], 3,              # the memo
        ["What is the value of y at an x-intercept?", "How can you clear the fraction once the 2 is on the other side?"]),
    work("5.3", "Determine the y-intercept of f.", 2, [
        "y = {4}/{0 − 3} + 2\ny = {2}/{3}",      # the memo
        "y = {4}/{0 − 3 + 2}\ny = −4",           # the + 2 put into the denominator
        "y = {4}/{0 − 3} + 2\ny = −{2}/{3}",     # −4/3 + 2 worked out with the wrong sign
        "y = {4}/{0 − 3} + 2\ny = {10}/{3}"], 0,  # the minus of −3 lost
        ["What is the value of x at a y-intercept?", "Where does the + 2 go: inside or outside the fraction?"]),
    draw("5.4", "Sketch the graphs of f and g on the same system of axes. Show clearly ALL the intercepts with the axes and any asymptotes.", 5, [
        ["f: the asymptotes x = 3 and y = 2", 1], ["f: the shape, a hyperbola with branches top right and bottom left of its asymptotes", 1],
        ["f: the x-intercept (1 ; 0) and the y-intercept (0 ; 2/3)", 1], ["g: the x-intercept (−2 ; 0)", 1], ["g: the y-intercept (0 ; 2)", 1]],
        ["Where are the asymptotes of f, and is a in a/(x − p) + q positive or negative?", "Where does each graph cut the axes?"],
        memo="The memo's sketch: f's two branches about the dashed asymptotes x = 3 and y = 2, one top right and one bottom left, the "
             "bottom-left branch cutting the y-axis at 2/3 and the x-axis at 1; g the straight line y = x + 2 rising from bottom left to top "
             "right through (−2 ; 0) and (0 ; 2), crossing both branches of f.", after=["5.1", "5.2", "5.3"],
        # built on a grid (2026-10-11, as transcribe_g11_math_p1_2017_11.py 5.7): f and g on one set of axes, each memo criterion its
        # features (or f's shape); criterion 0 is both asymptotes of f and criterion 2 both intercepts of f, so one feature of each
        # carries its mark. The y step is 1/3 so that f's y-intercept 2/3 is a grid point (on a coarser step no tap reaches it, and a
        # nearby one fits no hyperbola with the other features). The memo marks no shape for g: its line is drawn through its intercepts
        build={"kind": "sketch", "family": "hyperbola", "x": [-4, 7, 1], "y": [-4, 6, 1 / 3], "features": [
            {"id": "fva", "kind": "vline", "label": "vertical asymptote of f", "at": 3, "tol": 0, "marks": 1, "crit": 0, "graph": "f"},
            {"id": "fha", "kind": "hline", "label": "horizontal asymptote of f", "at": 2, "tol": 0, "marks": 0, "crit": 0, "graph": "f"},
            {"id": "fx", "kind": "point", "label": "x-intercept of f", "at": [1, 0], "tol": 0, "marks": 1, "crit": 2, "graph": "f"},
            {"id": "fy", "kind": "point", "label": "y-intercept of f", "at": [0, 2 / 3], "tol": 0, "marks": 0, "crit": 2, "graph": "f"},
            {"id": "gx", "kind": "point", "label": "x-intercept of g", "at": [-2, 0], "tol": 0, "marks": 1, "crit": 3, "graph": "g"},
            {"id": "gy", "kind": "point", "label": "y-intercept of g", "at": [0, 2], "tol": 0, "marks": 1, "crit": 4, "graph": "g"}],
               "graphs": [{"id": "f", "family": "hyperbola", "label": "f",
                           "shape": {"label": "Shape", "answer": "top right and bottom left", "marks": 1, "crit": 1}},
                          {"id": "g", "family": "line", "label": "g"}]}),
    work("5.5", "Calculate the x-coordinates of the points of intersection of f and g.", 4, [
        INT + "{4}/{x − 3} = x\nx(x − 3) = 4\nx² − 3x − 4 = 0\n(x + 4)(x − 1) = 0\nx = −4 or x = 1",                 # the signs in the factors swapped
        INT + "{4}/{x − 3} = x + 4\n(x + 4)(x − 3) = 4\nx² + x − 16 = 0\nx = {−1 ± √65}/{2}\nx = 3,53 or x = −4,53",  # + 2 moved without its sign change
        INT + "{4}/{x − 3} = x\nx(x − 3) = 4\nx² − 3x − 4 = 0\n(x − 4)(x + 1) = 0\nx = 4 or x = −1",                 # the memo
        INT + "{4}/{x − 3} = x\nx(x − 3) = 4\nx² − 3 = 4\nx² = 7\nx = 2,65 or x = −2,65"], 2,                        # x(x − 3) expanded as x² − 3
        ["At an intersection, how are f(x) and g(x) related?", "What can you multiply both sides by to clear the fraction?"]),
    mcq("5.6", "If x < 3, determine the values of x for which 4/(x − 3) + 2 < x + 2." + ANSWER, ["x < −1", "−1 ≤ x < 3", "−1 < x < 3", "x > 4"], 2,
        ["Which graph does each side of the inequality stand for?", "Where is the graph of f below the graph of g, to the left of x = 3?"],
        marks=2, after=["5.5"]),
    work("5.7", "The line y = x − 1 cuts f at P(1 ; 0) and Q. Write down the coordinates of Q.", 3, [
        AXIS + "Q(4 + 3 ; 4 + 2) = Q(7 ; 6)",       # √4 taken as 4
        AXIS + "Q(√4 + 3 ; √4 + 2) = Q(5 ; 4)",     # the memo
        AXIS + "Q(3 − √4 ; 2 + √4) = Q(1 ; 4)",     # a sign slip in the x-coordinate
        AXIS + "Q(√4 + 2 ; √4 + 3) = Q(4 ; 5)"], 1,  # the coordinates swapped
        ["What is special about the line y = x − 1 for the graph of f?", "How far is P from the point where the asymptotes cross, and which "
                                                                         "point is the same distance on the other side?"],
        after=["5.1", "5.2"])]
for i in q5:   # the built sketch: its features' and shapes' marks are the memo criteria's, criterion by criterion; every feature names
    b = i.get("build") or {}   # one of the two graphs, and every placed value is a grid point
    if b.get("kind") == "sketch":
        got = {}
        for x in b["features"] + [g["shape"] for g in b["graphs"] if g.get("shape")]:
            got[x["crit"]] = got.get(x["crit"], 0) + x["marks"]
        assert got == {k: c["marks"] for k, c in enumerate(i["criteria"])}, (i["n"], got)
        assert {f["graph"] for f in b["features"]} == {g["id"] for g in b["graphs"]}, i["n"]
        on = lambda u, ax: abs((u - ax[0]) / ax[2] - round((u - ax[0]) / ax[2])) < 1e-6 and ax[0] <= u <= ax[1]
        for f in b["features"]:
            assert (on(f["at"][0], b["x"]) and on(f["at"][1], b["y"])) if f["kind"] == "point" else on(f["at"], b["y" if f["kind"] == "hline" else "x"]), (i["n"], f["id"])

# ---- QUESTION 6, the question paper page 6 and the memo pages 14-16 ----
AB = "0 = 2({1}/{2})ˣ⁺¹ − 4\n"
EXP = "f(x) = −(x − 3)² + 25 = −x² + 6x + 16\n−x² + 6x + 16 = 2x + k\n"
q6 = [
    mcq("6.1", "Write down the equation of the asymptote of g." + ANSWER, ["y = 4", "x = −4", "y = −3", "y = −4"], 3,
        ["What happens to 2(1/2)ˣ⁺¹ as x becomes very large?", "Which horizontal line does g then approach but never reach?"]),
    mcq("6.2", "Write down the coordinates of D." + ANSWER, ["(−3 ; 25)", "(25 ; 3)", "(3 ; −25)", "(3 ; 25)"], 3,
        ["In which form is f(x) = −(x − 3)² + 25 written?", "In y = a(x − p)² + q, where is the turning point?"], marks=2),
    mcq("6.3", "Write down the range of f." + ANSWER, ["y ≤ 25", "y ≥ 25", "y < 25", "x ≤ 3"], 0,
        ["Does f open upwards or downwards?", "What is the largest y-value f reaches, and is it included?"], after=["6.2"]),
    work("6.4", "Calculate the length of EB.", 4, [
        "f(0) = −(0 − 3)² + 25 = 34: E(0 ; 34)\ng(0) = 2({1}/{2})⁰⁺¹ − 4 = −3: B(0 ; −3)\nEB = 34 − (−3) = 37 units",   # −(−3)² taken as +9
        "f(0) = −(0 − 3)² + 25 = 16: E(0 ; 16)\ng(0) = 2({1}/{2})⁰⁺¹ − 4 = −3: B(0 ; −3)\nEB = 16 − 3 = 13 units",      # B's y subtracted without its sign
        "f(0) = −(0 − 3)² + 25 = 16: E(0 ; 16)\ng(0) = 2({1}/{2})⁰ − 4 = −2: B(0 ; −2)\nEB = 16 − (−2) = 18 units",     # the + 1 of the exponent lost
        "f(0) = −(0 − 3)² + 25 = 16: E(0 ; 16)\ng(0) = 2({1}/{2})⁰⁺¹ − 4 = −3: B(0 ; −3)\nEB = 16 − (−3) = 19 units"], 3,   # the memo
        ["On which axis do E and B both lie, and what is x there?", "How do you find the distance between two points on the same vertical "
                                                                    "line?"]),
    mcq("6.5", "Determine the values of x for which f is decreasing." + ANSWER, ["x < 3", "x > 3", "x > 25", "y > 3"], 1,
        ["On which side of the turning point does the graph go down as x increases?", "Which vertical line is the axis of symmetry of f?"],
        marks=2, after=["6.2"]),
    work("6.6", "Calculate the average gradient between points A and B.", 5, [
        AB + "2 = ({1}/{2})ˣ⁺¹ = 2⁻ˣ⁻¹\n1 = −x − 1, so x = −2\nA(−2 ; 0) and B(0 ; −3)\nAverage gradient = {x₂ − x₁}/{y₂ − y₁} = {0 − (−2)}/{−3 − 0}\n"
             "= −{2}/{3}",                                                                         # the gradient upside down
        AB + "4 = ({1}/{2})ˣ⁺¹ = 2⁻ˣ⁻¹\n2 = −x − 1, so x = −3\nA(−3 ; 0) and B(0 ; −3)\nAverage gradient = {y₂ − y₁}/{x₂ − x₁} = {−3 − 0}/{0 − (−3)}\n"
             "= −1",                                                                               # 4 not divided by 2
        AB + "2 = ({1}/{2})ˣ⁺¹ = 2⁻ˣ⁻¹\n1 = −x − 1, so x = −2\nA(−2 ; 0) and B(0 ; −3)\nAverage gradient = {y₂ − y₁}/{x₂ − x₁} = {−3 − 0}/{0 − (−2)}\n"
             "= −{3}/{2}",                                                                         # the memo
        "−(x − 3)² + 25 = 0\n(x − 3)² = 25\nx − 3 = 5, so x = 8\nA(8 ; 0) and B(0 ; −3)\nAverage gradient = {y₂ − y₁}/{x₂ − x₁} = {−3 − 0}/{0 − 8}\n"
        "= {3}/{8}"], 2,                                                                           # C's x-value taken for A
        ["Which graph gives you A most easily, and what is y there?", "How is the average gradient between two points worked out?"],
        after=["6.4"]),
    work("6.7", "Graph t is obtained by reflecting g about the x-axis. Write down the range of t.", 2, [
        "t(x) = −g(x) = −(2({1}/{2})ˣ⁺¹ − 4)\nt(x) = −2({1}/{2})ˣ⁺¹ + 4\nRange: y < 4",       # the memo
        "t(x) = g(−x) = 2({1}/{2})⁻ˣ⁺¹ − 4\nt(x) = 2 · 2ˣ⁻¹ − 4\nRange: y > −4",              # reflected about the y-axis instead
        "t(x) = −g(x) = −(2({1}/{2})ˣ⁺¹ − 4)\nt(x) = −2({1}/{2})ˣ⁺¹ + 4\nRange: y > 4",       # the inequality the wrong way round
        "t(x) = −g(x) = −(2({1}/{2})ˣ⁺¹) − 4\nt(x) = −2({1}/{2})ˣ⁺¹ − 4\nRange: y < −4"], 0,  # the minus not taken to the − 4
        ["What happens to every y-value of a graph reflected about the x-axis?", "Where does the asymptote of g move to, and is t above or "
                                                                                 "below it?"], after=["6.1"]),
    mcq("6.8", "If p(x) = f(x) + 2, write down the coordinates of the turning point of p." + ANSWER, ["(5 ; 25)", "(3 ; 23)", "(3 ; 27)", "(1 ; 25)"], 2,
        ["What does adding 2 to f(x) do to the graph?", "Which coordinate of the turning point changes, and which stays the same?"], marks=2,
        after=["6.2"]),
    work("6.9", "Determine the value of k for which the straight line y = 2x + k will be a tangent to f.", 4, [
        "f(x) = −(x − 3)² + 25 = −x² + 16\n−x² + 16 = 2x + k\n−x² − 2x + 16 − k = 0\nEqual roots: Δ = (−2)² − 4(−1)(16 − k) = 0\n4 + 64 − 4k = 0\n"
        "k = 17",                                                                                       # (x − 3)² taken as x² + 9
        EXP + "−x² + 4x + 16 − k = 0\nEqual roots: Δ = (4)² − 4(−1)(16 − k) = 0\n16 + 64 − 4k = 0\nk = 20",   # the memo
        EXP + "−x² + 8x + 16 − k = 0\nEqual roots: Δ = (8)² − 4(−1)(16 − k) = 0\n64 + 64 − 4k = 0\nk = 32",   # 2x moved without its sign change
        EXP + "−x² + 4x + 16 − k = 0\nEqual roots: Δ = (4)² − 4(−1)(16 − k) = 0\n16 − 64 + 4k = 0\nk = 12"], 1,   # −4(−1) taken as −4
        ["How many times does a tangent meet the parabola?", "What must the discriminant be for an equation to have equal roots?"])]

# ---- QUESTION 7, the question paper page 7 and the memo page 17 ----
EFF = "1 + i(eff) = (1 + {i(nom)}/{m})ᵐ\n"
G = "A = 23 068,12(1 + {0,078}/{12})²⁴ = R26 949,02\n"
q71 = [
    work("7.1", "Calculate the effective interest rate per annum if an investment earns interest at a rate of 11,5% p.a., compounded monthly.", 3, [
        EFF + "1 + i(eff) = (1 + {0,115}/{4})⁴\ni(eff) = (1 + {0,115}/{4})⁴ − 1\ni(eff) = 12,01%",       # compounded quarterly
        EFF + "1 + i(eff) = (1 + 0,115)¹²\ni(eff) = (1 + 0,115)¹² − 1\ni(eff) = 269,23%",                # the yearly rate each month
        EFF + "1 + i(eff) = (1 + {0,115}/{12})¹²\ni(eff) = (1 + {0,115}/{12})¹²\ni(eff) = 112,13%",      # the 1 not subtracted
        EFF + "1 + i(eff) = (1 + {0,115}/{12})¹²\ni(eff) = (1 + {0,115}/{12})¹² − 1\ni(eff) = 12,13%"], 3,  # the memo
        ["How many times a year is the interest added?", "Which formula links a nominal rate compounded m times a year to the effective rate?"])]
q72 = [
    work("7.2", "Karabo bought a computer for R4 700. The value of the computer depreciated at a rate of 18% p.a. Using the reducing-balance "
         "method, calculate the book value of the computer 4 years after it was bought.", 3, [
        "A = P(1 − i·n)\nA = 4 700(1 − 0,18 × 4)\nA = R1 316,00",   # straight-line depreciation
        "A = P(1 − i)ⁿ\nA = 4 700(1 − 0,18)⁴\nA = R2 124,97",       # the memo
        "A = P(1 − i)ⁿ\nA = 4 700(1 − 0,018)⁴\nA = R4 370,63",      # 18% written 0,018
        "A = P(1 + i)ⁿ\nA = 4 700(1 + 0,18)⁴\nA = R9 112,26"], 1,   # compound growth for depreciation
        ["Is reducing-balance depreciation worked out on the original price or on each year's new value?", "What are P, i and n here?"])]
q73 = [
    work("7.3.1", "Calculate how much Nhlanhla had in this investment account 2 years after the initial deposit was made.", 3, [
        "A = P(1 + i·n)\nA = 20 000(1 + 0,072 × 2)\nA = R22 880,00",        # simple interest
        "A = P(1 + i)ⁿ\nA = 20 000(1 + {0,072}/{4})²\nA = R20 726,48",      # n in years, with a quarterly rate
        "A = P(1 + i)ⁿ\nA = 20 000(1 + {0,072}/{4})⁸\nA = R23 068,12",      # the memo
        "A = P(1 + i)ⁿ\nA = 20 000(1 + 0,072)⁸\nA = R34 880,95"], 2,       # the yearly rate each quarter
        ["How many times is interest added in 2 years when it is compounded quarterly?", "What is the interest rate for each quarter?"]),
    work("7.3.2", "How much will the investment be worth 7 years after the initial deposit was made?", 4, [
        G + "R26 949,02 − R2 500 = R24 449,02\nA = 24 449,02(1 + {0,078}/{12})³⁶\nA = R30 871,48",          # the memo's method (its 26 949,12 a slip)
        G + "A = 26 949,02(1 + {0,078}/{12})³⁶ = R34 028,20\nR34 028,20 − R2 500\nA = R31 528,20",          # the R2 500 taken off at the end
        G + "R26 949,02 − R2 500 = R24 449,02\nA = 24 449,02(1 + {0,078}/{12})⁶⁰\nA = R36 065,19",          # 5 years after the withdrawal
        "R23 068,12 − R2 500 = R20 568,12\nA = 20 568,12(1 + {0,078}/{12})²⁴ = R24 028,42\nA = 24 028,42(1 + {0,078}/{12})³⁶\n"
        "A = R30 340,40"], 0,                                                                               # the R2 500 taken off at 2 years
        ["How long does the money grow at 7,8% before the withdrawal, and how long after it?", "What is the monthly rate, and how many months "
                                                                                                "is each stretch?"], after=["7.3.1"])]

# ---- QUESTION 8, the question paper page 7 and the memo page 18 ----
SAME = "P(G, G) + P(R, R) + P(Y, Y)\n"
q8 = [
    work("8.1", "Show that there are 32 balls in the bag.", 1, [
        "6 + 8 + 18 = 32\nSo there are 32 balls in the bag",                     # the 18 yellow balls assumed
        "x = 8 ÷ 25 = 0,32\nSo there are 32 balls in the bag",                    # 25% used as 25, and 0,32 read as 32
        "25% of 32 = 8 green balls\nSo there are 32 balls in the bag",            # starts from the answer
        "P(G) = {8}/{x} = {1}/{4}\nx = 32: there are 32 balls in the bag"], 3,   # the memo
        ["How is the probability of a green ball worked out from the numbers of balls?", "What fraction is 25%?"]),
    draw("8.2", "A ball is drawn from the bag, the colour is recorded and it is not returned to the bag. Thereafter another ball is drawn from "
         "the bag, the colour is recorded and it is also not returned to the bag.\n\nDraw a tree diagram to represent ALL the possible ways in "
         "which the two balls could have been drawn from the bag. Show the probabilities associated with EACH branch, as well as the outcomes.", 4, [
        ["18 yellow balls (32 − 6 − 8)", 1], ["Branches: red, green and yellow for the first ball, and the same three from each of them for the "
                                              "second", 1],
        ["Probabilities: 6/32, 8/32 and 18/32 for the first ball; out of 31 for the second, one fewer of the colour already drawn", 1],
        ["Outcomes: (R; R), (R; G), (R; Y), (G; R), (G; G), (G; Y), (Y; R), (Y; G), (Y; Y)", 1]],
        ["How many yellow balls are there?", "After one ball is taken out and not returned, how many balls are left, and how many of that "
                                             "colour?"],
        memo="The memo's tree: the first ball R 6/32, G 8/32, Y 18/32; after R: R 5/31, G 8/31, Y 18/31; after G: R 6/31, G 7/31, Y 18/31; "
             "after Y: R 6/31, G 8/31, Y 17/31; the nine outcomes (R; R) to (Y; Y) at the ends of the branches."),
    work("8.3", "Calculate the probability that the two balls drawn from the bag will have the same colour.", 4, [
        SAME + "= ({8}/{32} × {8}/{32}) + ({6}/{32} × {6}/{32}) + ({18}/{32} × {18}/{32})\n= {53}/{128}",            # as if each ball went back
        "P(G, G) + P(R, R)\n= ({8}/{32} × {7}/{31}) + ({6}/{32} × {5}/{31})\n= {43}/{496}",                            # the two yellow balls left out
        SAME + "= ({8}/{32} × {7}/{31}) + ({6}/{32} × {5}/{31}) + ({18}/{32} × {17}/{31})\n= {49}/{124}",            # the memo
        SAME + "= ({8}/{32} × {7}/{32}) + ({6}/{32} × {5}/{32}) + ({18}/{32} × {17}/{32})\n= {49}/{128}"], 2,        # the second ball still out of 32
        ["Which outcomes on your tree have two balls of the same colour?", "Along a branch, do you add or multiply the probabilities, and "
                                                                           "between outcomes?"], after=["8.2"])]

# ---- QUESTION 9, the question paper page 8 and the memo page 19 ----
VM = "P(V) × P(M) = {32}/{150} × {67}/{150} = 0,095\n"
q91 = [
    work("9.1", "Was the choice of snack on this flight independent of gender? Motivate your answer with the necessary calculations.", 5, [
        VM + "P(V and M) = {12}/{150} = 0,08\nP(V and M) ≠ P(V) × P(M)\nThe choice of snack was not independent of gender",          # the memo
        "P(V) + P(M) = {32}/{150} + {67}/{150} = 0,66\nP(V and M) = {12}/{150} = 0,08\nP(V and M) ≠ P(V) + P(M)\n"
        "The choice of snack was not independent of gender",                                                                       # the addition rule
        VM + "P(V and M) = {12}/{150} = 0,08\n0,095 ≈ 0,08 (both about 0,1)\nThe choice of snack was independent of gender",          # the two rounded together
        VM + "P(V and M) = {12}/{67} = 0,18\nP(V and M) ≠ P(V) × P(M)\nThe choice of snack was not independent of gender"], 0,        # out of the males only
        ["What must be true of P(A and B) when two events are independent?", "Which numbers in the table give P(vegetarian), P(male) and "
                                                                             "P(vegetarian and male)?"])]
q92 = [
    # 1 + 1: the choice (NOT) and its reason; the wrong cards are false here (P(A and B) = 0,12, so P(A or B) = P(A) + P(B) − 0,12 and
    # P(A) + P(B) = 0,95)
    stmt("9.2.1", "Are events A and B mutually exclusive? Justify your answer.", 2,
         ["A and B are not mutually exclusive.", "P(A and B) = 0,12 ≠ 0"],
         ["A and B are mutually exclusive.", "P(A and B) = 0", "P(A or B) = P(A) + P(B)", "P(A) + P(B) = 1", "P(A and B) = P(A or B)"],
         ["What is P(A and B) for two mutually exclusive events?", "Is the given P(A and B) equal to that?"], 1),
    work("9.2.2", "Calculate P(B).", 4, [
        "P(A or B) = P(A) + P(B) + P(A and B)\n0,83 = P(A) + 4P(A) + 0,12\n0,71 = 5P(A), so P(A) = 0,142\nP(B) = 4(0,142) = 0,57",   # + P(A and B)
        "P(A or B) = P(A) + P(B) − P(A and B)\n0,83 = 4P(B) + P(B) − 0,12\n0,95 = 5P(B)\nP(B) = 0,19",                               # P(B) = 4P(A) read backwards
        "P(A or B) = P(A) + P(B)\n0,83 = P(A) + 4P(A)\n0,83 = 5P(A), so P(A) = 0,166\nP(B) = 4(0,166) = 0,66",                       # treated as mutually exclusive
        "P(A or B) = P(A) + P(B) − P(A and B)\n0,83 = P(A) + 4P(A) − 0,12\n0,95 = 5P(A), so P(A) = 0,19\nP(B) = 4(0,19) = 0,76"], 3,  # the memo
        ["Which identity links P(A or B), P(A), P(B) and P(A and B)?", "How can you write P(B) in terms of P(A) to leave one unknown?"]),
    work("9.2.3", "Calculate P(not A).", 2, [
        "P(not A) = 1 − P(B)\n= 1 − 0,76\n= 0,24",           # B taken as 'not A'
        "P(not A) = 1 − P(A)\n= 1 − 0,19\n= 0,81",           # the memo
        "P(not A) = 1 − P(A and B)\n= 1 − 0,12\n= 0,88",     # the wrong probability subtracted
        "P(not A) = 1 + P(A)\n= 1 + 0,19\n= 1,19"], 1,       # the complement rule with the wrong sign
        ["How are the probabilities of an event and its complement related?", "Which value did you find for P(A) on the way to P(B)?"],
        after=["9.2.2"])]

SNACKS = {"head": ["SNACK", "MALE", "FEMALE", "TOTAL"], "rows": [["Vegetarian", "12", "20", "32"], ["Chicken", "55", "63", "118"],
                                                                ["TOTAL", "67", "83", "150"]]}
# (no caption names a value, a range, an asymptote or a direction a question asks for: captions show in the enlarged view and to
# screen readers)
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Equations and inequalities", "marks": 15, "lead": "Solve for x in each of the following:",
     "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Simultaneous equations", "marks": 6, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Nature of roots", "marks": 4, "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Maximum values", "marks": 4, "items": q14},
    {"id": "2.1", "title": "Question 2.1", "kind": "Exponents", "marks": 4, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Exponential equations", "marks": 10, "lead": "Solve for x:", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Surds and exponents", "marks": 3, "items": q23},
    {"id": "3.1", "title": "Question 3.1", "kind": "Linear patterns", "marks": 6, "lead": "Given the linear pattern: 7 ; 2 ; −3 ; …", "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Linear patterns", "marks": 3, "items": q32},
    {"id": "4", "title": "Question 4", "kind": "Quadratic patterns", "marks": 16,
     "lead": "The quadratic number pattern: 4 ; p ; 11 ; q ; 22 ; … has a constant second difference of 1.", "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Hyperbola and straight line", "marks": 21, "lead": "Given: f(x) = 4/(x − 3) + 2 and g(x) = x + 2",
     "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Parabola and exponential graph", "marks": 23,
     "lead": "The diagram below shows the graphs of f(x) = −(x − 3)² + 25 and g(x) = 2(1/2)ˣ⁺¹ − 4.\nGraph f cuts the x-axis at A and C, the "
             "y-axis at E and has a turning point at D.\nGraph g cuts the x-axis at A and the y-axis at B.",
     "figure": fig("Q6", "The parabola f opens downwards: it rises from below the x-axis through A, left of the y-axis, cuts the y-axis at E, "
                   "reaches its turning point D to the right of the y-axis, and comes down through C on the x-axis far to the right. The "
                   "exponential graph g comes down steeply from the top left, crosses the x-axis at A where it meets f, cuts the y-axis at B "
                   "below the origin, and levels off to the right just above a dotted horizontal asymptote below the x-axis."), "items": q6},
    {"id": "7.1", "title": "Question 7.1", "kind": "Effective interest", "marks": 3, "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Depreciation", "marks": 3, "items": q72},
    {"id": "7.3", "title": "Question 7.3", "kind": "Compound interest", "marks": 7,
     "lead": "Nhlanhla made an initial deposit of R20 000 into an investment account that paid interest at the rate of 7,2% p.a., compounded "
             "quarterly. After 2 years the interest rate changed to 7,8% p.a., compounded monthly. Four years after his initial deposit, "
             "Nhlanhla withdrew R2 500 from his investment.", "items": q73},
    {"id": "8", "title": "Question 8", "kind": "Tree diagrams", "marks": 9,
     "lead": "A bag contains 6 red balls, 8 green balls and an unknown number of yellow balls. The probability of randomly choosing a green "
             "ball from the bag is 25%.", "items": q8},
    {"id": "9.1", "title": "Question 9.1", "kind": "Contingency tables", "marks": 5,
     "lead": "On a flight, passengers could choose between a vegetarian snack and a chicken snack. The snacks selected by the passengers were "
             "recorded. The results are shown in the table below.", "table": SNACKS, "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Probability rules", "marks": 8,
     "lead": "For any two events, A and B, it is given that P(A and B) = 0,12, P(A or B) = 0,83 and P(B) = 4 P(A).", "items": q92},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.1.2", "1.1.3", "1.1.4", "1.2", "1.3", "1.4", "2.1", "2.2.1", "2.2.2", "2.2.3", "2.3", "3.1.1", "3.1.2", "3.1.3",
                           "3.2", "4.1", "4.2", "4.3", "4.4", "5.2", "5.3", "5.5", "5.7", "6.4", "6.6", "6.7", "6.9", "7.1", "7.2", "7.3.1",
                           "7.3.2", "8.1", "8.3", "9.1", "9.2.2", "9.2.3"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["1.1.1", "5.1", "5.6", "6.1", "6.2", "6.3", "6.5", "6.8"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert not [i["n"] for i in ITEMS if i["t"] in ("num", "term", "match")], "no read-off number, term or sort in this paper"
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["5.4", "8.2"]
assert [i["n"] for i in ITEMS if i["t"] == "pickn"] == ["9.2.1"]
for i in ITEMS:   # a line that ends in "[...]" draws as a proof's reason: no working here has one
    assert i["t"] != "mcq" or not any(shape(o)[1] for o in i["opts"]), i["n"]
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2018", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines (a solution, a simplification, a term, a value, an amount, a rate, a probability, a "
                                                       "'show that', a 'write down' with a working) plays as four workings, the memo's FIRST method "
                                                       "line by line and three built from real errors (a sign or factor slip, a wrong formula, "
                                                       "rate or period, a misread value, a dropped step, a wrong region or count), one step a line, "
                                                       "0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, %d marks). In a 'show that' (1.4, "
                                                       "4.1, 8.1) every option ends in the given result; a wrong one reaches it through a wrong "
                                                       "step or by starting from the answer. A form the memo also accepts is never a wrong option: "
                                                       "no option of 9.1 uses its OR (vegetarian and female)." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.1.1", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                   "with no working (a pair of roots, the asymptotes, an interval, a coordinate, a range) that a "
                                                   "word marker cannot read (y ≤ 25 from y ≥ 25, (3 ; 25) from (−3 ; 25)): four options, the "
                                                   "memo's answer and three common errors, 0 or full marks. 6.5's accepted x ≥ 3 is in no option."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from a SCANNED question paper and a "
                                                           "SCANNED memo (no text layer in either), read from their page images; no API call."},
        {"n": "6.1", "kind": "no_fit", "detail": "The asymptote's equation (y = −4) is an answer multiple choice, not a term: the term marker strips "
                                                 "the minus sign, so y = 4 would pass as y = −4."},
        {"n": "5.4", "kind": "no_fit", "detail": "The sketch of f and g (5.4) is BUILT on a grid (2026-10-11): the learner places f's two "
                                                 "asymptotes and intercepts and g's intercepts, each curve is drawn through its features, and "
                                                 "the memo's five criteria are marked from them (f's shape from the curve the learner's own "
                                                 "features make). The grid's y step is 1/3, so that f's y-intercept 2/3 can be placed exactly. "
                                                 "The tree diagram (8.2) is drawn on paper and self-checked against the memo's 4 criteria."},
        {"n": "9.2.1", "kind": "no_fit", "detail": "The choice with its reason plays as statements: the memo's NOT mutually exclusive (1) and its "
                                                   "reason P(A and B) = 0,12 ≠ 0 (1) are the two right cards; the wrong cards are false for these "
                                                   "events (P(A and B) = 0,12, P(A) + P(B) = 0,95)."},
        {"n": "1.1.2", "kind": "memo_issue", "detail": "The memo (page 2) writes the third line as (5 ± √124)/10; with b = 2 it is (−2 ± √124)/10, "
                                                       "and the memo's answers 0,91 and −1,31 are those of −2 ± √124 (5 ± √124 gives 1,61 and "
                                                       "−0,61). The right option writes −2 ± √124 with the memo's answers; no option uses 5 ± √124."},
        {"n": "1.1.4", "kind": "memo_issue", "detail": "The memo's mark column (page 3) ticks 'k = 3 or k = 1', while its working has k = −3 or k = 1 "
                                                       "(from (k + 3)(k − 1) = 0) and rejects √(2x + 5) = −3; played as the working."},
        {"n": "7.3.2", "kind": "memo_issue", "detail": "The memo (page 17) writes 23 068,12(1 + 0,078/12)²⁴ = R26 949,12: it is R26 949,02. The slip "
                                                       "carries into R24 449,12 and the answer R30 871,61; the memo's own OR method gives R30 871,48, "
                                                       "the value of the corrected chain. Murci's memo-slip ruling: the right option uses the right "
                                                       "values (R26 949,02, R24 449,02, R30 871,48), and the memo's R30 871,61 is never a wrong option."},
    ],
}
QTOTAL = {"1": 29, "2": 17, "3": 9, "4": 16, "5": 21, "6": 23, "7": 13, "8": 9, "9": 13}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
assert per_q == QTOTAL, per_q
# the right letter (no printed multiple choice in this paper, so every letter is ours): the 36 authored workings as even as 36 allows
# (9 each: the brief's 3-7 band is for fewer workings), and all 44 four-option questions even (11 each)
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
assert total == 150, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts")
print("total:", total)
# every gate, so a dropped "after" fails the run
assert {i["n"]: i["after"] for i in ITEMS if i.get("after")} == {
    "3.1.2": ["3.1.1"], "3.1.3": ["3.1.1"],                        # Tₙ = −5n + 12
    "4.3": ["4.2"], "4.4": ["4.2"],                                # Tₙ = ½n² + 3/2 n + 2
    "5.4": ["5.1", "5.2", "5.3"],                                  # the asymptotes and both intercepts of f
    "5.6": ["5.5"],                                                # x = −1 (and 4)
    "5.7": ["5.1", "5.2"],                                         # (3 ; 2), and the stem's P(1 ; 0) is 5.2's x-intercept
    "6.3": ["6.2"], "6.5": ["6.2"], "6.8": ["6.2"],                # D(3 ; 25)
    "6.6": ["6.4"],                                                # B(0 ; −3)
    "6.7": ["6.1"],                                                # g's asymptote y = −4
    "7.3.2": ["7.3.1"],                                            # R23 068,12
    "8.3": ["8.2"],                                                # the tree: 18 yellow, out of 31 on the second draw
    "9.2.3": ["9.2.2"]}                                            # P(A) = 0,19
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the scanned "
                                                                       "memo's page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
