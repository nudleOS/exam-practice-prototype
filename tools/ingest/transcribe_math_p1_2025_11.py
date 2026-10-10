"""Mathematics P1 Nov 2025, the whole paper (Questions 1 to 11), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working are
the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the transcription is the source,
kept in git (out/ is not). The question paper is a SCAN (no text layer): read from its page images (1,5x, formulas at 2,5-3x);
the memo has a text layer whose fractions and exponents garble, so it was read from its page images too.

  python tools/ingest/transcribe_math_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P1 Nov 2025 Eng.pdf" "<...>/Mathematics P1 Nov 2025 MG Afr & Eng.pdf" --id math-p1-2025-11 --from-json

How the memo's shapes map (Mathematics: the phone has multiple choice, short text, a number keypad and self-checked drawings, no
algebra input; Murci's rulings of 2026-10-10):
  Every number, expression or interval the memo WORKS OUT ("Solve", "Calculate", "Determine", "Show that", first principles, a
  set of x-values from a graph) -> authored whole-working multiple choice, `work`: the memo's FIRST method line by line (one step
  a line, "{a}/{b}" a stacked fraction, no square brackets at a line's end: a trailing "[...]" draws as a proof's reason), and
  three workings each built from a DIFFERENT real error (a sign or factor slip, a wrong formula or rate, a misread value, a
  dropped step, a wrong selection, a wrong count), every option of a part the same layout (`shape`), the right one's place
  spread over A-D across the paper; the part keeps its marks, all or nothing. In a "show that" every option ends in the given
  result: a wrong one reaches it through a wrong step (or by starting from the answer). A value the memo ALSO accepts never
  appears in a wrong option (11.1.2: no option uses 72/120, the conditional reading of its wording).
  An inequality, interval, domain, range or coordinate with no working in the memo -> authored multiple choice of answers (the
  memo's and three common errors: a reversed sign, the wrong end point, x for y).
  One read-off number with no working (4.1, 1 mark) stays num; "Draw the graph" -> draw (self-checked against the memo's
  criteria); "Write down the asymptote" -> strict term (y = 0); "Describe the transformation" -> term (its phrasings).
  Where a part's options show an EARLIER part's answer (3.4 shows 3.3's 19 and 360; 4.6 shows f⁻¹ and its asymptote; 5.4 shows
  P(3 ; 8); 6.2 shows p = c; 9.3 shows f″ < 0 for x < 8/3), it carries "after": it opens once that part is answered.
Missions: Questions 3, 4, 5, 6, 9 and 10 share a stem and a graph, diagram or table, so each is one mission; Questions 1, 2, 7,
8 and 11 are their numbered groups (1.1, 1.2, 2.1, 2.2 ...).
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the drawings themselves and checked on a contact sheet."""
import json
import re
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad agent_math_p1/figs.py; [page, x0, y0, x1, y1] in points
    "Q4": [5, 77, 177, 500, 370], "Q5": [6, 50, 203, 523, 463], "Q6": [7, 50, 197, 560, 480], "Q9": [9, 110, 167, 517, 399],
    "Q10": [10, 57, 170, 520, 370]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


term = lambda n, q, a, clues, marks=1, strict=False, reject=None: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                                  **({"strict": True} if strict else {}), **({"reject": reject} if reject else {})}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}

EXACT = 0.001   # an exact value (4.1)
ANSWER = "\n\nChoose the correct answer."
WORK = "\n\nChoose the correct working."
AUTHORED = []   # the whole-working multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues, **kw):
    """A worked part as authored multiple choice (Murci, 2026-10-10): opts are the memo's FIRST working and three workings
    built from common errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing.
    kw: "after" (the earlier parts whose answers its options show)."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


# ---- QUESTION 1, the question paper page 3 and the memo pages 2-4 ----
q11 = [
    work("1.1.1", "(x + 5)(x − 2) = 0", 2, [
        "x² − 10 = 0\nx = −√10 or x = √10",                              # expands without the middle term
        "x² + 3x − 10 = 0\nx(x + 3) = 10, so x = 10 or x = 7",           # sets each factor equal to 10
        "x + 5 = 0 or x − 2 = 0\nx = −5 or x = 2",                       # the memo
        "x² − 3x − 10 = 0\n(x − 5)(x + 2) = 0, so x = 5 or x = −2"], 2,  # a sign slip in the expansion
        ["A product is zero only when one of its factors is zero.", "Set each bracket equal to zero."]),
    work("1.1.2", "5x² + 2 = −9x (correct to TWO decimal places)", 4, [
        "5x² + 9x + 2 = 0\nx = {−9 ± √(9² − 4(5)(2))}/{2(5)}\nx = {−9 ± √41}/{10}\nx = −0,26 or x = −1,54",          # the memo
        "5x² − 9x + 2 = 0\nx = {9 ± √((−9)² − 4(5)(2))}/{2(5)}\nx = {9 ± √41}/{10}\nx = 1,54 or x = 0,26",           # −9x moved without its sign change
        "5x² + 9x − 2 = 0\nx = {−9 ± √(9² − 4(5)(−2))}/{2(5)}\nx = {−9 ± √121}/{10}\nx = 0,2 or x = −2",            # +2 moved as −2
        "5x² + 9x + 2 = 0\nx = {−9 ± √(9² − 4(5)(2))}/{5}\nx = {−9 ± √41}/{5}\nx = −0,52 or x = −3,08"], 0,         # divides by a, not 2a
        ["Bring every term to one side first: ax² + bx + c = 0.", "It does not factorise neatly: use the quadratic formula."]),
    mcq("1.1.3", "8x² > 2x" + ANSWER, ['0 < x < {1}/{4}', 'x < 0 or x > {1}/{4}', 'x > {1}/{4}', 'x < 0 or x > 4'], 1,
        ["Move everything to one side and factorise.", "Sketch the parabola: where is it ABOVE the x-axis?"], marks=4),
    work("1.1.4", "2·2²ˣ − 9·2ˣ + 4 = 0", 4, [
        "(2·2ˣ − 4)(2ˣ − 1) = 0\n2ˣ = 2 or 2ˣ = 1\n2ˣ = 2¹ or 2ˣ = 2⁰\nx = 1 or x = 0",                            # wrong factors
        "(2·2ˣ − 1)(2ˣ − 4) = 0\n2ˣ = {1}/{2} or 2ˣ = 4\nx = log 0,5 or x = log 4\nx = −0,30 or x = 0,60",          # log base 10, not base 2
        "(2·2ˣ − 1)(2ˣ − 4) = 0\n2ˣ = −{1}/{2} or 2ˣ = 4\n2ˣ > 0: no solution, or 2ˣ = 2²\nx = 2 only",            # a sign slip loses a root
        "(2·2ˣ − 1)(2ˣ − 4) = 0\n2ˣ = {1}/{2} or 2ˣ = 4\n2ˣ = 2⁻¹ or 2ˣ = 2²\nx = −1 or x = 2"], 3,               # the memo
        ["2²ˣ = (2ˣ)²: let k = 2ˣ.", "Solve the quadratic in k, then write each value as a power of 2."]),
    work("1.1.5", "√(√(1/x) + 2) = 1/√x", 5, [
        "√({1}/{x}) + 2 = {1}/{x}\n{1}/{x} + 4 = {1}/{x²}\n4x² + x − 1 = 0\nx = {−1 ± √17}/{8}\nx = 0,39 or x = −0,64\n"
        "x = 0,39 (x ≠ −0,64)",                                                                     # squares term by term, surd not isolated
        "√({1}/{x}) + 2 = {1}/{x}\n{1}/{√x} = {1}/{x} − 2\n{1}/{x} = {1}/{x²} − {4}/{x} + 4\n4x² − 5x + 1 = 0\n(4x − 1)(x − 1) = 0\n"
        "x = {1}/{4} (x ≠ 1)",                                                                      # the memo
        "√({1}/{x}) + 2 = {1}/{x}\n{1}/{√x} = {1}/{x} − 2\n{1}/{x} = {1}/{x²} − {4}/{x} + 4\n4x² − 5x + 1 = 0\n(4x − 1)(x − 1) = 0\n"
        "x = {1}/{4} or x = 1",                                                                     # never checks: keeps x = 1
        "√({1}/{x}) + 2 = {1}/{x}\n{1}/{√x} = {1}/{x} − 2\n{1}/{x} = {1}/{x²} − {4}/{x} + 4\n4x² − x − 3 = 0\n(4x + 3)(x − 1) = 0\n"
        "x = 1 (x ≠ −{3}/{4})"], 1,                                                                 # × x² slip: 4/x × x² taken as 4
        ["Square both sides, isolate the root that is left, and square again (or let k = 1/√x).", "Check each solution in the ORIGINAL equation: one fails."])]
q12 = [
    work("1.2", "Calculate the values of x and y if:\n• x is the sum of 2 and y\n• Five times the product of x and y, is 6 more than the square of x", 6, [
        "x = y + 2\n5xy = x² + 6\n5(y + 2)y = (y + 2)² + 6\n5y² + 10y = y² + 4 + 6\n2y² + 5y − 5 = 0\ny = {−5 ± √65}/{4}\n"
        "y = 0,77 or y = −3,27\nx = 2,77 or x = −1,27",                                            # (y + 2)² taken as y² + 4
        "x = y + 2\n5xy + 6 = x²\n5(y + 2)y + 6 = (y + 2)²\n5y² + 10y + 6 = y² + 4y + 4\n2y² + 3y + 1 = 0\n(2y + 1)(y + 1) = 0\n"
        "y = −{1}/{2} or y = −1\nx = {3}/{2} or x = 1",                                            # the 6 added to the wrong side
        "x = y + 2\n5xy = x² + 6\n5(y + 2)y = (y + 2)² + 6\n5y² + 10y = y² + 4y + 4 + 6\n2y² + 3y − 5 = 0\n(2y + 5)(y − 1) = 0\n"
        "y = −{5}/{2} or y = 1\nx = −{1}/{2} or x = 3",                                            # the memo
        "y = x + 2\n5xy = x² + 6\n5x(x + 2) = x² + 6\n5x² + 10x = x² + 6\n2x² + 5x − 3 = 0\n(2x − 1)(x + 3) = 0\n"
        "x = {1}/{2} or x = −3\ny = {5}/{2} or y = −1"], 2,                                         # 'x is the sum of 2 and y' read as y = x + 2
        ["Write the two sentences as two equations: the first is x = y + 2.", "Substitute one into the other to get a quadratic."])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 5-6 ----
q21 = [
    work("2.1.1", "Show that t = −2", 3, [
        "t = −2 gives 8 + (−4) + 2 + …\n{−4}/{8} = −{1}/{2}\n{2}/{−4} = −{1}/{2}\nThe ratios are equal, so t = −2",           # starts from the answer
        "{t − 2}/{t + 10} = {t + 4}/{t − 2}\n(t − 2)² = (t + 4)(t + 10)\nt² + 4 = t² + 14t + 40\n−14t = 36, so t = −2",        # (t − 2)² as t² + 4
        "{t − 2}/{t + 10} = {t − 2}/{t + 4}\n(t − 2)(t + 4) = (t − 2)(t + 10)\nt² + 2t − 8 = t² + 8t − 20\n−6t = −12, so t = −2",  # T₂/T₁ = T₂/T₃
        "{t − 2}/{t + 10} = {t + 4}/{t − 2}\n(t − 2)² = (t + 4)(t + 10)\nt² − 4t + 4 = t² + 14t + 40\n−18t = 36, so t = −2"], 3,  # the memo
        ["In a geometric series the ratio of consecutive terms is constant.", "Set T₂/T₁ equal to T₃/T₂, then cross-multiply."]),
    work("2.1.2", "Calculate the value of T₂₅. Write your answer in the form Tₙ = bˣ", 3, [
        "a = 8: the series is 8 ; −4 ; 2 ; …\nr = {8}/{−4} = −2\nn − 1 = 24: T₂₅ = 8(−2)²⁴\nT₂₅ = 2²⁷",                       # r upside down
        "a = 8: the series is 8 ; −4 ; 2 ; …\nr = {−4}/{8} = −{1}/{2}\nn − 1 = 24: T₂₅ = 8(−{1}/{2})²⁴\nT₂₅ = ({1}/{2})²¹",      # the memo
        "a = 8: the series is 8 ; −4 ; 2 ; …\nr = {−4}/{8} = −{1}/{2}\nn = 25: T₂₅ = 8(−{1}/{2})²⁵\nT₂₅ = −({1}/{2})²²",         # rⁿ, not rⁿ⁻¹
        "a = 8: the series is 8 ; −4 ; 2 ; …\nr = {−4}/{8} = −{1}/{2}\nn − 1 = 24: T₂₅ = 8(−{1}/{2})²⁴\nT₂₅ = (−4)²⁴ = 2⁴⁸"], 1,  # 8 multiplied into the base
        ["With t = −2 the series is 8 + (−4) + 2 + …", "T₂₅ = ar²⁴: write 8 and 1/2 as powers of 2."]),
    work("2.1.3", "Calculate the sum of the infinite series.", 2, [
        "S∞ = {a}/{1 − r}\nS∞ = {8}/{1 − (−½)}\nS∞ = {16}/{3} = 5,33",          # the memo
        "S∞ = {a}/{1 − r}\nS∞ = {8}/{1 − ½}\nS∞ = 16",                           # loses the sign of r
        "S∞ = {a}/{r − 1}\nS∞ = {8}/{−½ − 1}\nS∞ = −{16}/{3} = −5,33",          # the formula upside down in its bracket
        "S∞ = {a}/{1 − r}\nS∞ = {8}/{1 − (−2)}\nS∞ = {8}/{3} = 2,67"], 0,       # r upside down
        ["−1 < r < 1, so the series converges.", "S∞ = a/(1 − r)."])]
q22 = [
    work("2.2.1", "Write down the difference between T₆ and T₁₄", 2, [
        "d = 4\nT₁₄ − T₆ = 9d\n= 4 × 9 = 36",              # counts the terms, not the steps between them
        "d = 3\nT₁₄ − T₆ = 8d\n= 3 × 8 = 24",              # the first term taken as d
        "d = 4\nT₁₄ − T₆ = 8d\n= 4 × 8 = 32",              # the memo
        "d = 4\nT₁₄ − T₆ = 4(14 − 6) − 1\n= 31"], 2,       # the −1s do not cancel
        ["Each term is d more than the one before: find d from 4p − 1.", "Count the steps from T₆ to T₁₄: each step adds d."]),
    work("2.2.2", "Calculate the value of k.", 5, [
        "n = 117 − k; T₁₁₇ = 4(117) − 1 = 467\n26 675 = {117 − k}/{2}(4k − 1 + 467)\n26 675 = (117 − k)(2k + 233)\n2k² − k − 586 = 0\n"
        "k = {1 ± √4 689}/{4}\nk = 17,37 (k ≠ −16,87)",                                             # one term too few
        "n = 118 − k; T₁₁₇ = 4(117) = 468\n26 675 = {118 − k}/{2}(4k − 1 + 468)\n53 350 = (118 − k)(4k + 467)\n4k² − 5k − 1 756 = 0\n"
        "k = {5 ± √28 121}/{8}\nk = 21,59 (k ≠ −20,34)",                                             # the last term without its −1
        "n = 118 − k; T₁₁₇ = 4(117) − 1 = 467\n26 675 = {118 − k}/{2}(4k − 1 + 467)\n26 675 = (118 − k)(2k + 233)\n2k² − 3k − 819 = 0\n"
        "(k + 21)(2k − 39) = 0\nk = {39}/{2} (k ≠ −21)",                                             # factor signs swapped
        "n = 118 − k; T₁₁₇ = 4(117) − 1 = 467\n26 675 = {118 − k}/{2}(4k − 1 + 467)\n26 675 = (118 − k)(2k + 233)\n2k² − 3k − 819 = 0\n"
        "(k − 21)(2k + 39) = 0\nk = 21 (k ≠ −{39}/{2})"], 3,                                         # the memo
        ["Count the terms from p = k to p = 117 carefully (try k = 116: how many terms is that?).",
         "Sₙ = n/2 (first + last) gives a quadratic in k."])]

# ---- QUESTION 3, the question paper page 4 and the memo page 7 ----
q3 = [
    work("3.1", "Calculate the depth of the torpedo at the end of the first 5 seconds.", 2, [
        "First differences: 35 ; 33 ; 31 ; 29\nSecond difference: −2\nT₅ = 135 + 29 = 164",     # the memo
        "First differences: 35 ; 33 ; 31\nSecond difference: −2\nT₅ = 104 + 31 = 135",          # stops one term short
        "First differences: 35 ; 33 ; 31 ; 29\nSecond difference: −2\nT₅ = 135 − 29 = 106",     # subtracts the first difference
        "First differences: 35 ; 33 ; 33 ; 33\nSecond difference: −2\nT₅ = 137 + 33 = 170"], 0,  # keeps the last first difference
        ["Find the first differences: 35, 33, …", "The second difference is constant: keep the pattern going."]),
    work("3.2", "Show that the depth of the torpedo at the end of n seconds was Tₙ = −n² + 38n − 1", 3, [
        'a = −2 (the second difference)\n3a + b = 35, so b = 41\na + b + c = 36, so c = −3', '2a = −2, so a = −1\na + b = 35, so b = 36\na + b + c = 36, so c = 1',
        '2a = −2, so a = −1\n3a + b = 35, so b = 38\na + b + c = 36, so c = −1', '2a = 2, so a = 1\n3a + b = 35, so b = 32\na + b + c = 36, so c = 3'], 2,
        ["Tₙ = an² + bn + c, where 2a is the second difference.", "3a + b is the first first difference; a + b + c is T₁."]),
    work("3.3", "Calculate the maximum depth that the torpedo reached.", 3, [
        "n = {38}/{2(−1)} = −19\nT₋₁₉ = −(−19)² + 38(−19) − 1\n= −1 084",     # loses the minus of −b
        "n = {−38}/{2(−1)} = 19\nT₁₉ = −(19)² + 38(19) − 1\n= 360",            # the memo
        "n = {−38}/{2(−1)} = 19\nT₁₉ = (19)² + 38(19) − 1\n= 1 082",           # −n² squared as (−n)²
        "n = {−38}/{−1} = 38\nT₃₈ = −(38)² + 38(38) − 1\n= −1"], 1,            # −b/a, without the 2
        ["The maximum of a quadratic is at its turning point.", "n = −b/(2a), then substitute that n into Tₙ."]),
    work("3.4", "After how many seconds was the torpedo at 104 m below sea level for the second time?", 2, [
        "{n + 3}/{2} = 360\nn + 3 = 720\nn = 717",     # the maximum depth for the time of the maximum
        "{n + 3}/{2} = 19\nn + 3 = 38\nn = 35",        # the memo
        "{n + 3}/{2} = 19\nn + 3 = 9,5\nn = 6,5",      # divides by 2 instead of multiplying
        "{n + 3}/{2} = 19\nn + 3 = 38\nn = 41"], 1,    # adds the 3 across
        ["The first time was after 3 seconds, and the pattern is symmetric about its maximum.", "Or solve −n² + 38n − 1 = 104."], after=["3.3"])]

# ---- QUESTION 4, the question paper page 5 and the memo page 8 ----
q4 = [
    num("4.1", "Calculate the value of t", -1, EXACT, "",
        ["(3 ; t) is on f, so t = f(3).", "To what power must 1/3 be raised to give 3?"]),
    mcq("4.2", "Write down the coordinates of A." + ANSWER, ['(0 ; 1)', '(3 ; 0)', '({1}/{3} ; 0)', '(1 ; 0)'], 3,
        ["A is on the x-axis, so f(x) = 0 there.", "The log of which number is always 0?"]),
    work("4.3", "Determine the equation of f⁻¹, the inverse of f, in the form y = …", 2, [
        "y = log₁⁄₃ x\nx = log₁⁄₃ y\ny = 3ˣ",                         # drops the reciprocal of the base
        "y = log₁⁄₃ x\nf⁻¹(x) = {1}/{f(x)}\ny = {1}/{log₁⁄₃ x}",       # the inverse taken as 1/f
        "y = log₁⁄₃ x\nx = log₁⁄₃ y\ny = ({1}/{3})ˣ = 3⁻ˣ",           # the memo
        "y = log₁⁄₃ x\nx = log₁⁄₃ y\ny = log₃ x"], 2,                  # flips the base, stays a log
        ["Swap x and y, then rewrite the log as a power.", "logₐ y = x means y = aˣ."]),
    term("4.4", "Write down the equation of the asymptote of f⁻¹", ["y = 0", "y=0"],
         ["f⁻¹ is an exponential graph.", "Which horizontal line does bˣ approach but never reach?"], strict=True),
    draw("4.5", "Draw the graph of f⁻¹ on the set of axes provided in the ANSWER BOOK. Clearly indicate the intercepts with the axes, the "
         "coordinates of ONE other point and the asymptotes.", 3, [
        ["Decreasing exponential shape with the asymptote y = 0", 1], ["y-intercept (0 ; 1)", 1], ["Any other point on the graph, e.g. (−1 ; 3)", 1]],
        ["f⁻¹ is the reflection of f in the line y = x.", "Where does a graph y = bˣ cut the y-axis? Work out b⁰."]),
    work("4.6", "The graph of h is obtained when f⁻¹ is translated 5 units to the right. Determine the y-values of h where x > 4.", 2, [
        "h(x) = ({1}/{3})ˣ⁻⁵\nh(4) = ({1}/{3})⁻¹ = 3\n0 < y < 3",                               # the memo
        "h(x) = ({1}/{3})ˣ⁺⁵\nh(4) = ({1}/{3})⁹ = {1}/{19 683}\n0 < y < {1}/{19 683}",          # 'to the right' as x + 5
        "h(x) = ({1}/{3})ˣ⁻⁵\nh(4) = ({1}/{3})⁻¹ = 3\ny > 3",                                   # h read as increasing
        "h(x) = ({1}/{3})ˣ⁻⁵\nh(4) = ({1}/{3})⁻¹ = {1}/{3}\n0 < y < {1}/{3}"], 0,               # drops the negative exponent
        ["h(x) = f⁻¹(x − 5): work out h(4).", "h is decreasing and never reaches its asymptote."], after=["4.3", "4.4"])]

# ---- QUESTION 5, the question paper page 6 and the memo pages 9-10 ----
q5 = [
    mcq("5.1", "Write down the domain of g." + ANSWER, ['x ∈ ℝ', 'y ∈ ℝ, y ≠ 8', 'x ∈ ℝ, x ≠ 8', 'x ∈ ℝ, x ≠ 3'], 3, ["g is undefined where its denominator is zero.", "That x-value is its vertical asymptote."], marks=1),
    mcq("5.2", "Write down the range of f." + ANSWER, ['y ≤ 8', 'y ≥ 8', 'x ≤ 3', 'y < 8'], 0, ["f opens downwards, so its turning point is its highest point.", "P is also where g's asymptotes cross."], marks=1),
    mcq("5.3.1", "Determine the values of x for which: g(x) ≤ f(x)" + ANSWER, ['3 ≤ x ≤ 5', 'x < 3 or x ≥ 5', '3 < x ≤ 5', '3 < x < 5'], 2, ["Find where the graph of g is on or below the graph of f.", "Look between g's vertical asymptote and the intersection D."], marks=2),
    mcq("5.3.2", "Determine the values of x for which: f(x) < 6" + ANSWER, ['x < 1 or x > 5', '1 < x < 5', 'x ≤ 1 or x ≥ 5', 'x > 5 only'], 0, ["f is symmetric about x = 3, and f(5) = 6.", "Where is the parabola BELOW the line y = 6?"], marks=2),
    work("5.4", "Show that the equation of the parabola is f(x) = −½x² + 3x + 7/2", 3, [
        "y = a(x + 3)² + 8\n6 = a(5 + 3)² + 8\n−2 = 64a, so a = −{1}/{32}\ny = −{1}/{32}(x² + 6x + 9) + 8\ny = −{1}/{2}x² + 3x + {7}/{2}",  # P's x with the wrong sign
        "y = a(x − 3)² + 8\n6 = a(5 − 3)² + 8\n−2 = 4a, so a = −{1}/{2}\ny = −{1}/{2}(x² − 6x + 9) + 8\ny = −{1}/{2}x² + 3x + {7}/{2}",  # the memo
        "y = a(x − 3)² + 8\n6 = a(5 − 3)² + 8\n−2 = 2a, so a = −1\ny = −1(x² − 6x + 9) + 8\ny = −{1}/{2}x² + 3x + {7}/{2}",                # (5 − 3)² taken as 2
        "y = a(x − 3)² + 8\n6 = a(5 − 3)² + 8\n−2 = 4a, so a = −{1}/{2}\ny = −{1}/{2}(x² + 9) + 8\ny = −{1}/{2}x² + 3x + {7}/{2}"], 1,       # (x − 3)² as x² + 9
        ["Use the turning-point form y = a(x − p)² + q with P.", "D(5 ; 6) is on f: substitute it to find a."], after=["5.1", "5.2"]),
    work("5.5", "Calculate the length of MT.", 6, [
        "x² − 6x − 7 = 0\n(x + 7)(x − 1) = 0\nx = −7 or x = 1, so M(−7 ; 0)\n0 = {−4}/{x − 3} + 8\n−8x + 24 = −4, so x = {7}/{2}\n"
        "MT = {7}/{2} + 7 = {21}/{2} = 10,5",                                                       # factor signs swapped
        "x² − 6x − 7 = 0\n(x − 7)(x + 1) = 0\nx = 7 or x = −1, so M(−1 ; 0)\n0 = {−4}/{x − 3} + 8\n−8x + 24 = 4, so x = {5}/{2}\n"
        "MT = {5}/{2} + 1 = {7}/{2} = 3,5",                                                         # a sign slip solving g(x) = 0
        "x² − 6x − 7 = 0\n(x − 7)(x + 1) = 0\nx = 7 or x = −1, so M(−1 ; 0)\n0 = {−4}/{x − 3} + 8\n−8x + 24 = −4, so x = {7}/{2}\n"
        "MT = {7}/{2} − 1 = {5}/{2} = 2,5",                                                         # subtracts M's x without its sign
        "x² − 6x − 7 = 0\n(x − 7)(x + 1) = 0\nx = 7 or x = −1, so M(−1 ; 0)\n0 = {−4}/{x − 3} + 8\n−8x + 24 = −4, so x = {7}/{2}\n"
        "MT = {7}/{2} + 1 = {9}/{2} = 4,5"], 3,                                                     # the memo
        ["M: solve f(x) = 0. T: solve g(x) = 0.", "Both points are on the x-axis: subtract their x-coordinates."]),
    work("5.6", "Determine the equation of the tangent to f at D.", 3, [
        "f′(x) = −{1}/{2}x + 3\nm = f′(5) = −{5}/{2} + 3 = {1}/{2}\n6 = {1}/{2}(5) + c, so c = {7}/{2}\ny = {1}/{2}x + {7}/{2}",  # the power 2 not brought down
        "f′(x) = −x + 3\nm = f(5) = 6\n6 = 6(5) + c, so c = −24\ny = 6x − 24",                                                 # f(5) for the gradient
        "f′(x) = −x + 3\nm = f′(5) = −5 + 3 = −2\n6 = −2(5) + c, so c = 16\ny = −2x + 16",                                      # the memo
        "f′(x) = −x + 3\nm = f′(5) = −5 + 3 = −2\n6 = −2(5) + c, so c = −4\ny = −2x − 4"], 2,                                  # a sign slip finding c
        ["The gradient of the tangent at D is f′ at D's x-value.", "Then put the point D(5 ; 6) into y = mx + c."])]

# ---- QUESTION 6, the question paper page 7 and the memo pages 11-12 ----
q6 = [
    mcq("6.1", "Write down the coordinates of the x-intercept of g in terms of p." + ANSWER, ['(p ; 0)', '(0 ; −p)', '(−p ; 0)', '(0 ; p)'], 2, ["The vertical asymptote of f is x = −p.", "g cuts the x-axis exactly there."], marks=1),
    work("6.2", "Graph g intersects the horizontal asymptote of graph f at x = 1 and the graph f at x = 3. Graphs f and g also intersect on the "
         "y-axis. Determine the equation of f.", 5, [
        "p = c and q = 1 + c, so f(x) = {a}/{x + c} + 1 + c\n(0 ; c): c = {a}/{0 + c} + 1 + c, so a = −c\n(3 ; 3 + c): 3 + c = {a}/{3 + c} + 1 + c\n"
        "3 + c = {−c}/{3 + c} + 1 + c\n9 + 6c + c² = −c + 3 + 4c + c²\n3c = −6, so c = −2\na = 2, q = −1: f(x) = {2}/{x − 2} − 1",      # the memo
        "p = −c and q = 1 + c, so f(x) = {a}/{x − c} + 1 + c\n(0 ; c): c = {a}/{0 − c} + 1 + c, so a = c\n(3 ; 3 + c): 3 + c = {a}/{3 − c} + 1 + c\n"
        "3 + c = {c}/{3 − c} + 1 + c\n9 − c² = c + 3 + 2c − c²\n3c = 6, so c = 2\na = 2, q = 3: f(x) = {2}/{x − 2} + 3",               # p's sign: x = −p read as p = −c
        "p = c and q = 1, so f(x) = {a}/{x + c} + 1\n(0 ; c): c = {a}/{0 + c} + 1, so a = c² − c\n(3 ; 3 + c): 3 + c = {a}/{3 + c} + 1\n"
        "3 + c = {c² − c}/{3 + c} + 1\n6 + 5c + c² = c² − c\n6c = −6, so c = −1\na = 2, q = 1: f(x) = {2}/{x − 1} + 1",                 # q taken as the x-value 1
        "p = c and q = 1 + c, so f(x) = {a}/{x + c} + 1 + c\n(0 ; c): c = {a}/{0 + c} + 1 + c, so a = −c\n(3 ; 3 + c): 3 + c = {a}/{3 + c} + 1 + c\n"
        "3 + c = {−c}/{3 + c} + 1 + c\n9 + c² = −c + 3 + 4c + c²\n3c = 6, so c = 2\na = −2, q = 3: f(x) = {−2}/{x + 2} + 3"], 0,       # (3 + c)² as 9 + c²
        ["g's x-intercept is on f's vertical asymptote, and g meets y = q at x = 1.", "The intersections (0 ; g(0)) and (3 ; g(3)) both lie on f."],
        after=["6.1"]),
    term("6.3", "Describe the transformation that g must undergo to become an axis of symmetry of f that cuts f at two points.", [
        "Translation of 1 unit down", "1 unit down", "1 unit downwards", "One unit down", "Translate 1 unit down", "Translate g 1 unit down",
        "Shift 1 unit down", "Move 1 unit down", "Translation of 1 unit to the right", "1 unit to the right", "1 unit right", "One unit to the right",
        "Translate 1 unit to the right", "Translate g 1 unit to the right", "Shift 1 unit to the right", "Move 1 unit to the right"],
         ["f's axes of symmetry pass through the point where its asymptotes cross, with gradients 1 and −1.",
          "Which one cuts both branches? Compare it with g."], marks=2,
         reject=["1 unit up", "Translation of 1 unit up", "1 unit to the left", "Translation of 1 unit to the left", "1 unit left"])]

# ---- QUESTION 7, the question paper page 8 and the memo pages 13-14 ----
q71 = [
    work("7.1", "A travel company informs Robert that a holiday to a certain destination costs R40 000 now. The company predicts that the cost of "
         "this holiday will increase by 7,8% per annum. What will this holiday cost in 5 years' time?", 2, [
        "A = P(1 + i)ⁿ\nA = 40 000(1 + 0,78)⁵\nA = R714 759,61",                  # 7,8% written as 0,78
        "A = P(1 + i)ⁿ\nA = 40 000(1 + 0,078)⁵\nA = R58 230,94",                  # the memo
        "A = P(1 + i)ⁿ\nA = 40 000(1 + {0,078}/{12})⁶⁰\nA = R59 004,72",          # compounds monthly
        "A = P(1 + i)ⁿ − P\nA = 40 000(1 + 0,078)⁵ − 40 000\nA = R18 230,94"], 1, # the increase only, not the cost
        ["The cost grows by 7,8% of each NEW cost: compound growth.", "A = P(1 + i)ⁿ."])]
q72 = [
    work("7.2", "Sarah opened a savings account that paid interest at a rate of 5,8% p.a., compounded quarterly. She deposited R2 300 into the "
         "account on 1 January 2020 and continued to make deposits of R2 300 at the beginning of each quarter thereafter. She made her last "
         "deposit on 1 October 2025. Calculate the accumulated amount in the account on 1 January 2026.", 4, [
        "i = {0,058}/{4} = 0,0145; n = 24\nF = {2 300[(1 + 0,0145)²⁴ − 1]}/{0,0145}\nF = R65 462,39",                            # no last quarter's growth
        "i = {0,058}/{4} = 0,0145; n = 23\nF = {2 300[(1 + 0,0145)²³ − 1]}/{0,0145} × (1 + 0,0145)\nF = R63 162,39",             # 23 deposits counted
        "i = 0,058; n = 24\nF = {2 300[(1 + 0,058)²⁴ − 1]}/{0,058} × (1 + 0,058)\nF = R120 390,81",                               # the yearly rate per quarter
        "i = {0,058}/{4} = 0,0145; n = 24\nF = {2 300[(1 + 0,0145)²⁴ − 1]}/{0,0145} × (1 + 0,0145)\nF = R66 411,60"], 3,         # the memo
        ["Count the deposits: one each quarter from 1 January 2020 to 1 October 2025.", "Deposits at the START of a quarter earn one more quarter "
                                                                                          "of interest by 1 January 2026."])]
q73 = [
    work("7.3.1", "Rajesh was unable to make the first three payments. He made his first repayment of R10 000 on 30 June 2024. He continued to "
         "make monthly repayments of R10 000 at the end of each month thereafter. How long, in completed months, will it take Rajesh to repay the "
         "loan from the time the loan was granted?", 5, [
        "i = {0,068}/{12}; the loan stays R900 000\n900 000 = {10 000[1 − (1 + i)⁻ⁿ]}/{i}\n(1 + i)⁻ⁿ = 0,49\n"
        "n = −{log 0,49}/{log(1 + i)} = 126,24…\n126,24…, so 127 months",                                                      # no growth over the missed months
        "i = {0,068}/{12}; A = 900 000(1 + i)³ = R915 386,86\n915 386,86 = {10 000[1 − (1 + i)⁻ⁿ]}/{i}\n(1 + i)⁻ⁿ = 0,4812…\n"
        "n = −{log 0,4812…}/{log(1 + i)} = 129,419…\n129,419…, so 130 months",                                                 # the three months not added
        "i = {0,068}/{12}; A = 900 000(1 + i)³ = R915 386,86\n915 386,86 = {10 000[1 − (1 + i)⁻ⁿ]}/{i}\n(1 + i)⁻ⁿ = 0,4812…\n"
        "n = −{log 0,4812…}/{log(1 + i)} = 129,419…\n3 + 129,419… = 132,419…, so 133 months",                                  # the memo
        "i = {0,068}/{12}; A = 900 000(1 + i)³ = R915 386,86\n915 386,86 = {10 000[1 − (1 + i)⁻ⁿ]}/{i}\n(1 + i)⁻ⁿ = 0,4812…\n"
        "n = −{log 0,4812…}/{log(1 + i)} = 129,419…\n3 + 129,419… = 132,419…, so 132 months"], 2,                             # rounds down
        ["First grow the loan through the three months with no payment.", "Then the present-value annuity formula with x = R10 000 gives n; "
                                                                           "remember the months before the first repayment."]),
    work("7.3.2", "Calculate the value of the final payment.", 4, [
        "i = {0,068}/{12}; part of a payment left: n = 0,419…\nBalance = {10 000[1 − (1 + i)^(−0,419…)]}/{i}\nBalance = R4 173,55…\n"
        "Final payment = 4 173,55…(1 + i) = R4 197,21",                                                                       # the memo
        "i = {0,068}/{12}; part of a payment left: n = 0,419…\nBalance = {10 000[1 − (1 + i)^(−0,419…)]}/{i}\nBalance = R4 173,55…\n"
        "Final payment = the balance = R4 173,56",                                                                            # no month of interest
        "i = {0,068}/{12}; part of a payment left: n = 0,419…\nBalance = 0,419… × 10 000\nBalance = R4 190,33\n"
        "Final payment = 4 190,33(1 + i) = R4 214,08",                                                                        # a share of R10 000
        "i = {0,068}/{12}; part of a payment left: n = 0,419…\nBalance = {10 000[(1 + i)^(0,419…) − 1]}/{i}\nBalance = R4 183,45\n"
        "Final payment = 4 183,45(1 + i) = R4 207,16"], 0,                                                                    # the future-value formula
        ["The whole number in your n from 7.3.1 counts the full R10 000 payments; the decimal part is what is left over.",
         "Find the balance after the last full payment, then add one month's interest."])]

# ---- QUESTION 8, the question paper page 8 and the memo page 15 ----
q81 = [
    work("8.1", "Determine f′(x) from first principles if it is given that f(x) = −2x + 3.", 4, ['f(x + h) = −2x + h + 3\nf′(x) = lim(h→0) {−2x + h + 3 − (−2x + 3)}/{h}\n= lim(h→0) {h}/{h}\n= 1', 'f(x + h) = −2(x + h) + 3\nf′(x) = lim(h→0) {−2(x + h) + 3 − (−2x − 3)}/{h}\n= lim(h→0) {6 − 2h}/{h}\n(no limit)', 'f(x + h) = −2(x + h) + 3\nf′(x) = lim(h→0) {−2(x + h) + 3}/{h}\n= lim(h→0) (−2)\n= −2', 'f(x + h) = −2(x + h) + 3\nf′(x) = lim(h→0) {−2(x + h) + 3 − (−2x + 3)}/{h}\n= lim(h→0) {−2h}/{h}\n= −2'], 3, ["f′(x) = lim (h→0) [f(x + h) − f(x)]/h.", "Write f(x + h) first and simplify before taking the limit."])]
q82 = [
    work("8.2.1", "g′(x) if g(x) = −3x⁴ + 2x", 2, [
        "g(x) = −3x⁴ + 2x\ng′(x) = −12x³ + 2x",     # keeps the x of 2x
        "g(x) = −3x⁴ + 2x\ng′(x) = −3x³ + 2",       # lowers the power without bringing it down
        "g(x) = −3x⁴ + 2x\ng′(x) = −12x³",          # 2x differentiated as a constant
        "g(x) = −3x⁴ + 2x\ng′(x) = −12x³ + 2"], 3,  # the memo
        ["Power rule: the derivative of axⁿ is naxⁿ⁻¹.", "Differentiate each term on its own."]),
    work("8.2.2", "dy/dx if y = (2x⁴ + 1)/x²", 4, [
        "y = {2x⁴}/{x²} + 1\ny = 2x² + 1\n{dy}/{dx} = 4x",                          # divides only the first term by x²
        "y = {2x⁴}/{x²} + {1}/{x²}\ny = 2x² + x⁻²\n{dy}/{dx} = 4x − 2x⁻³",          # the memo
        "y = {2x⁴ + 1}/{x²}\n{dy}/{dx} = {8x³}/{2x}\n{dy}/{dx} = 4x²",              # differentiates top and bottom separately
        "y = {2x⁴}/{x²} + {1}/{x²}\ny = 2x² + x⁻²\n{dy}/{dx} = 4x − x⁻³"], 1,       # the power −2 not brought down
        ["Divide each term of the numerator by x² first.", "1/x² = x⁻²; then use the power rule."])]

# ---- QUESTION 9, the question paper page 9 and the memo pages 16-17 ----
q9 = [
    work("9.1", "Calculate the coordinates of E.", 4, [
        "f′(x) = 3x² − 16x + 5 = 0\n(3x − 1)(x − 5) = 0\nx = {1}/{3} or x = 5\ny = ({1}/{3})³ − 8({1}/{3})² + 5({1}/{3}) + 14 = {400}/{27}\n"
        "E({1}/{3} ; {400}/{27})",                                                                  # the other turning point (D)
        "f′(x) = 3x² − 8x + 5 = 0\n(3x − 5)(x − 1) = 0\nx = 1 or x = {5}/{3}\ny = ({5}/{3})³ − 8({5}/{3})² + 5({5}/{3}) + 14 = {128}/{27}\n"
        "E({5}/{3} ; {128}/{27})",                                                                  # −8x² differentiated as −8x
        "f′(x) = 3x² − 16x + 5 = 0\n(3x − 1)(x − 5) = 0\nx = {1}/{3} or x = 5\ny = (5)³ − 8(5)² + 5(5) + 14 = −36\nE(5 ; −36)",  # the memo
        "f′(x) = 3x² − 16x + 5 = 0\n(3x − 1)(x − 5) = 0\nx = {1}/{3} or x = 5\ny = (5)³ − 8(5)² + 5(5) = −50\nE(5 ; −50)"], 2,  # drops the + 14
        ["At a turning point f′(x) = 0.", "E is the turning point on the right: put its x into f."]),
    mcq("9.2", "For which values of x is f concave down?" + ANSWER, ['f″(x) = 6x − 16 > 0, so x > {8}/{3}', 'f″(x) = 6x − 16 < 0, so x < {8}/{3}', 'f′(x) = 3x² − 16x + 5 < 0, so {1}/{3} < x < 5', 'f″(x) = 6x − 8 < 0, so x < {4}/{3}'], 1, ["Concave down means f″(x) < 0.", "The point of inflection lies halfway between the turning points."], marks=3),
    work("9.3", "The coordinates of B are (2 ; 0). Use the graph to determine the values of x for which f(x) · f″(x) < 0", 4, [
        "x-intercepts: A(−1 ; 0), B(2 ; 0), C(7 ; 0)\nf″(x) = 6x − 16 < 0 for x < {8}/{3}\n−1 < x < 2 or {8}/{3} < x < 7",          # the memo
        "x-intercepts: A(−1 ; 0), B(2 ; 0), C(7 ; 0)\nf″(x) = 6x − 16 < 0 for x < {8}/{3}\nx < −1 or 2 < x < {8}/{3} or x > 7",     # same signs (the product > 0)
        "x-intercepts: A(−1 ; 0), B(2 ; 0), C(7 ; 0)\nf′(x) = 3x² − 16x + 5 < 0 for {1}/{3} < x < 5\nx < −1 or {1}/{3} < x < 2 or 5 < x < 7",  # f′ for f″
        "x-intercepts: A(−1 ; 0), B(2 ; 0), C(7 ; 0)\nf″(x) = 6x − 8 < 0 for x < {4}/{3}\n−1 < x < {4}/{3} or 2 < x < 7"], 0,       # 8x² differentiated twice as 8x
        ["Divide f(x) by (x − 2) to find A and C.", "The product is negative where f and f″ have opposite signs; f″ changes sign at the point of "
                                                    "inflection."], after=["9.2"]),
    work("9.4", "For which values of t will y = −11x + t intersect f at 3 distinct points?", 6, ['f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nx = 4: t = 14; x = {4}/{3}: t = {634}/{27}\n14 ≤ t ≤ {634}/{27}', 'f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nt lies between the two x-values\n{4}/{3} < t < 4', 'f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nx = 4: t = 14; x = {4}/{3}: t = {634}/{27}\nt < 14 or t > {634}/{27}', 'f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nx = 4: t = 14; x = {4}/{3}: t = {634}/{27}\n14 < t < {634}/{27}'], 3, ["Find where the tangent to f has gradient −11: f′(x) = −11.", "Those two tangents give the boundary values of t; the line lies between them."])]

# ---- QUESTION 10, the question paper page 10 and the memo page 18 ----
q10 = [
    work("10.1", "Show that the volume of the cylinder is given by V = 25x²/(4π) − x³/(4π)", 3, ['2x + 2h = 50\nh = 25 − x\n2πr = x\nr = {x}/{2π}\nV = πr²h = π({x}/{2π})²(25 − x)\nV = {25x²}/{4π} − {x³}/{4π}', 'x + h = 50\nh = 50 − x\n2πr = x\nr = {x}/{2π}\nV = πr²h\nV = {25x²}/{4π} − {x³}/{4π}', '2x + 2h = 50\nh = 25 − x\n2πr = h\nr = {25 − x}/{2π}\nV = πr²x\nV = {25x²}/{4π} − {x³}/{4π}', '2x + 2h = 50\nh = 25 − x\n2πr = x\nr = {x}/{2π}\nV = 2πrh = x(25 − x)\nV = {25x²}/{4π} − {x³}/{4π}'], 0, ["The side x rolls into the circumference: 2πr = x.", "Use the perimeter to write h in terms of x, then V = πr²h."]),
    work("10.2", "Calculate the value of x that will maximise the volume of the cylinder.", 3, [
        "V′(x) = {25x}/{4π} − {3x²}/{4π} = 0\n25x − 3x² = 0\nx(25 − 3x) = 0\nx = {25}/{3} = 8,33 (x ≠ 0)",       # 25x² differentiated as 25x
        "V(x) = {25x²}/{4π} − {x³}/{4π} = 0\n25x² − x³ = 0\nx²(25 − x) = 0\nx = 25 (x ≠ 0)",                    # V = 0, not V′ = 0
        "V′(x) = {50x}/{4π} − {3x²}/{4π} = 0\n50x − 3x² = 0\nx(50 − 3x) = 0\nx = {3}/{50} = 0,06 (x ≠ 0)",      # 3x = 50 solved upside down
        "V′(x) = {50x}/{4π} − {3x²}/{4π} = 0\n50x − 3x² = 0\nx(50 − 3x) = 0\nx = {50}/{3} = 16,67 (x ≠ 0)"], 3,  # the memo
        ["At a maximum V′(x) = 0.", "Factor out x: x = 0 gives no cylinder."])]

# ---- QUESTION 11, the question paper page 11 and the memo pages 19-21 ----
q111 = [
    work("11.1.1", "The events male and preferring juice are independent. Show that e = 84.", 3, ['P(M or J) = P(M) × P(J)\n{36}/{210} = {90}/{210} × {e}/{210}\ne = 84', 'P(M and J) = P(M) × P(J)\n{36}/{210} = {90}/{210} × {e}/{210}\ne = 84', 'P(M and J) = P(M) × P(J)\n{36}/{90} = {90}/{210} × {e}/{210}\ne = 84', 'P(M and J) = P(M) + P(J) − 1\n{36}/{210} = {90}/{210} + {e}/{210} − 1\ne = 84'], 1, ["Independent events: P(A and B) = P(A) × P(B).", "Work out f, the number of males, first."]),
    work("11.1.2", "Calculate the probability that a female learner, chosen at random from the group, will like energy drinks.", 3, [
        "d = 210 − 84 = 126\nb = 126 − 36 = 90\nP(female and energy drink) = {90}/{210} = {3}/{7} = 0,43",    # subtracts the males' JUICE
        "d = 210 − 84 = 126\nb = 126 − 54 = 72\nP(female and energy drink) = {72}/{210} = {12}/{35} = 0,34",  # the memo
        "d = 210 − 90 = 120\nb = 120 − 54 = 66\nP(female and energy drink) = {66}/{210} = {11}/{35} = 0,31",  # the male total taken for e
        "d = 210 − 84 = 126\nb = 126 − 54 = 72\nP(female and energy drink) = {72}/{126} = {4}/{7} = 0,57"], 1,  # out of the energy-drink total
        ["Use e = 84 to complete the table: d, then b.", "Read it as: the learner chosen from the WHOLE group is female AND likes energy drinks."])]
q112 = [
    work("11.2", "At a kiosk, 120 people buy either a cup of coffee or a bottle of water. The chance of rain on any given day is 75%. The chance of a "
         "person buying a cup of coffee on a rainy day is three times the chance of the person buying coffee on a non-rainy day.\n\nThe probability "
         "of a person buying coffee on any given day is 7/12.\nCalculate the number of cups of coffee that will be sold on a non-rainy day.", 4, [
        "{3}/{4}(3x) + {1}/{4}x = {7}/{12}\n27x + 3x = 7\nx = {7}/{30}\n{7}/{30} × 120 = 28 cups",          # the memo
        "{1}/{4}(3x) + {3}/{4}x = {7}/{12}\n9x + 9x = 7\nx = {7}/{18}\n{7}/{18} × 120 ≈ 47 cups",           # the weather chances swapped
        "{3}/{4}(3x) + {1}/{4}x = {7}/{12}\n27x + 3x = 7\nx = {7}/{30}\n3 × {7}/{30} × 120 = 84 cups",      # answers for a rainy day
        "{3}/{4}(3x) + {1}/{4}x = {7}/{12}\n9x + 3x = 7\nx = {7}/{12}\n{7}/{12} × 120 = 70 cups"], 0,       # × 12 slip: 9x, not 27x
        ["Let x be the chance of buying coffee on a non-rainy day; on a rainy day it is 3x.", "P(coffee) = P(rain)·3x + P(no rain)·x."])]
q113 = [
    work("11.3.1", "Calculate the total number of possible ways in which the 8 runners can finish the race if Bongi finishes in a position "
         "immediately after Andrew.", 2, [
        "Places for the pair Andrew, Bongi: 7, in 2 orders\nOrders of the other 6 runners: 6!\nWays = 7 × 2 × 6! = 10 080",   # counts Bongi before Andrew too
        "Places for the pair Andrew, Bongi: 8\nOrders of the other 6 runners: 6!\nWays = 8 × 6! = 5 760",                   # one place too many
        "Places for the pair Andrew, Bongi: 7\nOrders of the other 6 runners: 6!\nWays = 7 × 6! = 5 040",                   # the memo
        "Places for the pair Andrew, Bongi: 7\nOrders of the other 6 runners: 6\nWays = 7 × 6 = 42"], 2,                     # 6 for 6!
        ["Join Andrew and Bongi into one unit in a fixed order.", "Then arrange the units."]),
    work("11.3.2", "Calculate the probability that TWO OR MORE runners finish the race after Andrew and before Bongi.", 4, [
        "Places for Andrew and Bongi: 2(5 + 4 + 3 + 2 + 1) = 30\nWays = 30 × 6!\nP = {30 × 6!}/{8!}\nP = {15}/{28} = 0,54",           # Bongi before Andrew too
        "Places for Andrew and Bongi: 5\nWays = 5 × 6!\nP = {5 × 6!}/{8!}\nP = {5}/{56} = 0,09",                                       # exactly two between only
        "Places for Andrew and Bongi: 6 + 5 + 4 + 3 + 2 + 1 = 21\nWays = 21 × 6!\nP = {21 × 6!}/{8!}\nP = {3}/{8} = 0,38",              # one or more between
        "Places for Andrew and Bongi: 5 + 4 + 3 + 2 + 1 = 15\nWays = 15 × 6!\nP = {15 × 6!}/{8!}\nP = {15}/{56} = 0,27"], 3,           # the memo
        ["Count the places Andrew and Bongi can take with Bongi at least three places behind Andrew; the other 6 runners fill the rest.",
         "Divide by the number of ALL finishing orders."])]

DEPTH = {"head": ["", "Depth (in metres)"], "rows": [["At the end of the first second", "36"], ["At the end of the first 2 seconds", "71"],
                                                    ["At the end of the first 3 seconds", "104"]]}
DRINKS = {"head": ["", "JUICE", "ENERGY DRINKS", "TOTAL"], "rows": [["Female", "a", "b", "c"], ["Male", "36", "54", "f"], ["Total", "e", "d", "210"]]}
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Equations and inequalities", "marks": 19, "lead": "Solve for x:", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Simultaneous equations", "marks": 6, "items": q12},
    {"id": "2.1", "title": "Question 2.1", "kind": "Geometric series", "marks": 8,
     "lead": "Given the infinite geometric series: (t + 10) + (t − 2) + (t + 4) + …", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Arithmetic series", "marks": 7,
     "lead": "Given Σ (4p − 1) = 26 675, the sum running from p = k to p = 117", "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Quadratic patterns", "marks": 10,
     "lead": "The depth of a torpedo below sea level forms a quadratic pattern, where 0 metres is at sea level. A submarine tracked a torpedo in "
             "one-second intervals.\n\nThe depth (in metres) that the torpedo reached is given in the table below.", "table": DEPTH, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Logs and inverses", "marks": 10,
     "lead": "The graph of f(x) = log₁⁄₃ x is drawn below. Point A is the x-intercept of f and (3 ; t) lies on f.",
     "figure": fig("Q4", "The graph of f, a decreasing curve: it comes down steeply beside the positive y-axis (its asymptote), cuts the x-axis "
                   "at A to the right of the origin O, and keeps falling slowly below the x-axis through the point (3 ; t)."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Parabola and hyperbola", "marks": 18,
     "lead": "The graphs of f(x) = ax² + bx + c and g(x) = −4/(x − 3) + 8 are drawn below.\nP is the turning point of f and the point of "
             "intersection of the asymptotes of g.\nThe graphs intersect at D(5 ; 6). M and T are x-intercepts of f and g respectively.",
     "figure": fig("Q5", "The parabola f opens downwards; its turning point P lies where g's dashed horizontal and vertical asymptotes cross. f "
                   "cuts the x-axis at M, left of the origin O, and again far to the right. The hyperbola g has one branch top left, above the "
                   "horizontal asymptote, rising towards the vertical asymptote; its other branch rises from below the x-axis next to the "
                   "vertical asymptote, cuts the x-axis at T, meets f at D(5 ; 6) and levels off below the horizontal asymptote."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Hyperbola and straight line", "marks": 8,
     "lead": "The graphs of g(x) = x + c and f(x) = a/(x + p) + q are drawn below. Graph g and the vertical asymptote of f intersect at the x-axis.",
     "figure": fig("Q6", "The straight line g rises from bottom left to top right. The hyperbola f has a dashed vertical asymptote right of the "
                   "y-axis and a dashed horizontal asymptote below the x-axis; g cuts the x-axis where the vertical asymptote meets it. One branch "
                   "of f, top right, comes down beside the vertical asymptote, crosses g, cuts the x-axis and levels off just above the horizontal "
                   "asymptote. The other branch, bottom left, runs just below the horizontal asymptote, crosses g on the y-axis and falls beside the "
                   "vertical asymptote."), "items": q6},
    {"id": "7.1", "title": "Question 7.1", "kind": "Compound growth", "marks": 2, "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Future value annuity", "marks": 4, "items": q72},
    {"id": "7.3", "title": "Question 7.3", "kind": "Loan repayments", "marks": 9,
     "lead": "The bank granted Rajesh a loan of R900 000 on 28 February 2024 at an interest rate of 6,8% p.a., compounded monthly.", "items": q73},
    {"id": "8.1", "title": "Question 8.1", "kind": "First principles", "marks": 4, "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Rules of differentiation", "marks": 6, "lead": "Determine:", "items": q82},
    {"id": "9", "title": "Question 9", "kind": "Cubic functions", "marks": 17,
     "lead": "Sketched below is the graph of f(x) = x³ − 8x² + 5x + 14. A, B and C are the x-intercepts of f. D and E are the turning points of f.",
     "figure": fig("Q9", "A cubic f: rising from bottom left, it cuts the x-axis at A, left of the origin O, reaches the turning point D just right "
                   "of the y-axis, falls through B on the x-axis to the turning point E well below the x-axis, then rises steeply through C on "
                   "the x-axis."), "items": q9},
    {"id": "10", "title": "Question 10", "kind": "Optimisation", "marks": 6,
     "lead": "A rectangular metal sheet has dimensions x and h units, with x > h, and a perimeter of 50 units. The metal sheet is rolled into a "
             "cylinder with two open ends (top and bottom) and height h units.",
     "figure": fig("Q10", "Left: a rectangle x units wide and h units high. Right: the cylinder of height h, open at the top and the bottom, made "
                   "by rolling the sheet so that the side x goes round the circular ends."), "items": q10},
    {"id": "11.1", "title": "Question 11.1", "kind": "Independent events", "marks": 6,
     "lead": "A survey was conducted among female and male learners at a school about which type of cold drink they preferred. The data from the "
             "survey is presented in the table below.", "table": DRINKS, "items": q111},
    {"id": "11.2", "title": "Question 11.2", "kind": "Dependent probability", "marks": 4, "items": q112},
    {"id": "11.3", "title": "Question 11.3", "kind": "Counting principle", "marks": 6,
     "lead": "Eight runners compete in a race where there are no tied finishes. Bongi and Andrew are two of the competitors.", "items": q113},
]

ITEMS = [i for m in missions for i in m["items"]]
# every worked part (typed steps, a rubric or an authored working until Murci's ruling of 2026-10-10), now whole-working multiple choice
assert tuple(AUTHORED) == ("1.1.1", "1.1.2", "1.1.4", "1.1.5", "1.2", "2.1.1", "2.1.2", "2.1.3", "2.2.1", "2.2.2", "3.1", "3.2", "3.3", "3.4",
                           "4.3", "4.6", "5.4", "5.5", "5.6", "6.2", "7.1", "7.2", "7.3.1", "7.3.2", "8.1", "8.2.1", "8.2.2", "9.1", "9.3",
                           "9.4", "10.1", "10.2", "11.1.1", "11.1.2", "11.2", "11.3.1", "11.3.2"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["1.1.3", "4.2", "5.1", "5.2", "5.3.1", "5.3.2", "6.1", "9.2"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["4.1"]   # the one read-off number
assert {i["n"]: i["after"] for i in ITEMS if i.get("after")} == {"3.4": ["3.3"], "4.6": ["4.3", "4.4"], "5.4": ["5.1", "5.2"], "6.2": ["6.1"],
                                                                  "9.3": ["9.2"]}
for i in ITEMS:   # a line that ends in "[...]" draws as a proof's reason: no working here has one
    assert i["t"] != "mcq" or not any(shape(o)[1] for o in i["opts"]), i["n"]
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings (Murci, 2026-10-10): every part the memo works out "
                                                       "(a solution, a sum, a value, a 'show that', a derivative from first principles, a set of "
                                                       "x-values) plays as four workings, the memo's FIRST method line by line and three built from "
                                                       "real errors (a sign or factor slip, a wrong formula or rate, a misread value, a dropped step, "
                                                       "a wrong selection or count), one step a line, 0 or full marks: " + ", ".join(AUTHORED)
                                                       + " (%d parts, %d marks). In a 'show that' (2.1.1, 3.2, 5.4, 10.1, 11.1.1) every option ends "
                                                         "in the given result; a wrong one reaches it through a wrong step (2.1.1's by starting from "
                                                         "the answer)." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.1.3", "kind": "no_fit", "detail": "Authored multiple choice, answers (Murci, 2026-10-10): " + ", ".join(ANSWERS) + " ask for an "
                                                   "inequality, an interval, a domain, a range or a coordinate a word marker cannot read (x < 0 "
                                                   "from x > 0, (−p ; 0) from (p ; 0)): four options, the memo's answer and three common errors (a "
                                                   "reversed sign, the wrong end point, x for y), 0 or full marks."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from a SCANNED question paper (no "
                                                           "text layer) and the memo's page images (its text layer garbles fractions and powers); "
                                                           "no API call."},
        {"n": "4.1", "kind": "no_fit", "detail": "One read-off number stays typed on the keypad: 4.1 (t = log₁⁄₃ 3 = −1, 1 mark, exact)."},
        {"n": "4.5", "kind": "no_fit", "detail": "The sketch of f⁻¹ is drawn on paper and self-checked against the memo's three criteria."},
        {"n": "4.4", "kind": "no_fit", "detail": "The asymptote's equation is a strict term (y = 0): it has no sign to lose, and x = 0 stays wrong."},
        {"n": "6.3", "kind": "no_fit", "detail": "The transformation is a term listing the memo's two answers (1 unit down OR 1 unit to the right) in "
                                                 "common phrasings, with 'up' and 'left' rejected; another wording is marked wrong."},
        {"n": "11.1.2", "kind": "memo_issue", "detail": "The question asks for 'the probability that a female learner, chosen at random from the "
                                                        "group, will like energy drinks', which reads as P(energy drinks | female) = 72/120 = 0,6; "
                                                        "the memo marks P(female and energy drinks) = 72/210 = 12/35 = 0,34. Played as the memo "
                                                        "(0,34); no option uses 72/120, so the conditional reading is never marked as an error. A "
                                                        "teacher should confirm."},
    ],
}
QTOTAL = {"1": 25, "2": 15, "3": 10, "4": 10, "5": 18, "6": 8, "7": 15, "8": 10, "9": 17, "10": 6, "11": 16}   # the paper's [n] per question
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
assert total == 150, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts")
print("total:", total)
out = Path(__file__).parent / "out" / "math-p1-2025-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the memo's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
