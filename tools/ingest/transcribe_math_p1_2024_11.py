"""Mathematics P1 Nov 2024, the whole paper (Questions 1 to 12), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working are
the paper's and the memo's own (its English); clues, figure captions and the authored multiple-choice distractors are ours. No API
call: the transcription is the source, kept in git (out/ is not). The question paper is a SCAN (no text layer): read from its page
images (1,5x, formulas at 3x); the memo has a text layer whose fractions and exponents garble, so it was read from its page
images (1,6x).

  python tools/ingest/transcribe_math_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P1 Nov 2024 Eng.pdf" "<...>/Mathematics P1 Nov 2024 MG Afr & Eng.pdf" --id math-p1-2024-11 --from-json

How the memo's shapes map (Mathematics: the phone has multiple choice, short text and self-checked drawings, no algebra input):
  Every typed calculation ("Calculate / Determine / Solve", a "Write down" whose memo shows a working) -> authored multiple choice,
  `work` (Murci, 2026-10-10): the memo's FIRST working line by line, its result last, and three workings each built from a
  DIFFERENT real error (a wrong formula, a sign slip, a misread value, a wrong factor, the wrong ratio, a rounding or counting
  slip), each ending in a confident result; 0 or full marks. One read-off number with no working (5.1, 1 mark) stays num.
  Authored multiple choice (Murci, 2026-10-10) also for what a word or number marker cannot score: an inequality or interval, a
  range, a domain restriction, a set of values, a sigma equation, a square-root equation, a transformation of two moves, a pair
  of read-off values, a "show that", first principles and an independence argument. Four options: the memo's answer or working
  and three built from real errors (a lost condition, the wrong region, ends included, a sign slip, the wrong formula, a flawed
  step that still claims the result). Workings are laid out as the memo's lines ("\\n"), fractions as {numerator}/{denominator}
  (drawn stacked; never nested, so a fraction inside one is written ¼ or 0,01125), no line ends in "]" (the player draws a
  trailing [..] as a proof's reason column, so the memo's S = n/2[...] is written with round brackets or with text after it),
  and every option of a part has the same shape; the stem ends "Choose the correct answer." (a short answer) or "Choose the
  correct working." (a working). The part keeps its marks. The right option's position is spread evenly over A-D.
  "Sketch the graph" and "Draw a Venn diagram" -> draw (self-checked against the memo's criteria).
  A part whose options show an EARLIER part's answer opens only after it (`after`, GATES below).
Missions: Questions 3, 4, 5, 6, 9, 10, 11 and 12 share a stem, a diagram or a graph, so each is one mission; Questions 1, 2, 7 and 8
are their numbered groups (1.1, 1.2, 1.3, 2.1, 2.2 ...). A single-line MCQ in a figure mission carries the figure itself (the MCQ
stage shows an item's own figure only); a working MCQ plays on the page, under the mission's figure.
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the ink of the 3x page images and checked on a contact sheet with
the ingest's 1% padding; no label touches a crop's top-left corner, so none needs an inset."""
import json
import re
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad math1_24/figs.py + final.json; [page, x0, y0, x1, y1] in points
    "Q3": [4, 345, 96, 500, 252], "Q5": [5, 60, 188, 510, 436], "Q6": [6, 54, 179, 516, 431], "Q9": [8, 89, 188, 486, 403]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}

EXACT = 0.001   # an exact value (5.1, the one typed number left)
ANS, WORK = "\n\nChoose the correct answer.", "\n\nChoose the correct working."
AUTHORED = []   # the typed calculations played as authored multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues):
    """A typed calculation as authored multiple choice (Murci, 2026-10-10): opts are the memo's FIRST working and three workings
    built from common errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks)


# ---- QUESTION 1, the question paper page 3 and the memo pages 2-3 ----
q11 = [
    work("1.1.1", "x(x − 3) = 0", 2, [
        'x(x − 3) = 0\nx = 0 or x = −3',                                       # sign slip in the second factor
        'x(x − 3) = 0\nx = 0 or x = 3',                                        # the memo
        'x(x − 3) = 0\nx = 3 (both sides divided by x)',                       # divides by x: the root x = 0 is lost
        'x² − 3 = 0\nx = −√3 or x = √3'], 1,                                   # expands x(x − 3) as x² − 3
        ["A product is zero only when one of its factors is zero.", "Set each factor equal to zero."]),
    work("1.1.2", "2x² + 1 = 4x (correct to TWO decimal places)", 4, [
        '2x² + 4x + 1 = 0\nx = {−(4) ± √((4)² − 4(2)(1))}/{2(2)}\nx = −0,29 or x = −1,71',      # 4x moved across without its sign change
        '2x² − 4x + 1 = 0\nx = {−(−4) ± √((−4)² − 4(2)(1))}/{2}\nx = 3,41 or x = 0,59',         # divides by 2, not 2a
        '2x² − 4x + 1 = 0\nx = {−(−4) ± √((−4)² + 4(2)(1))}/{2(2)}\nx = 2,22 or x = −0,22',     # b² + 4ac under the root
        '2x² − 4x + 1 = 0\nx = {−(−4) ± √((−4)² − 4(2)(1))}/{2(2)}\nx = 1,71 or x = 0,29'], 3,  # the memo
        ["Bring every term to one side first: ax² + bx + c = 0.", "It does not factorise: use the quadratic formula and round at the end."]),
    mcq("1.1.3", "x² − 2x − 3 > 0" + ANS, ['−1 < x < 3', 'x < −3 or x > 1', 'x < −1 or x > 3', 'x ≤ −1 or x ≥ 3'], 2,
        ["Factorise the left-hand side and find the critical values.", "Sketch the parabola: where is it ABOVE the x-axis?"], marks=4),
    work("1.1.4", "2²ˣ − 2ˣ⁺² − 32 = 0", 5, [
        '2²ˣ − 2² · 2ˣ − 32 = 0\n(2ˣ − 8)(2ˣ + 4) = 0\n2ˣ = 8 or 2ˣ ≠ −4 (no solution)\n2ˣ = 2³\nx = 3',     # the memo
        '2²ˣ − 2² · 2ˣ − 32 = 0\n(2ˣ + 8)(2ˣ − 4) = 0\n2ˣ ≠ −8 (no solution) or 2ˣ = 4\n2ˣ = 2²\nx = 2',     # the factors' signs swapped
        '2²ˣ − 2² · 2ˣ − 32 = 0\n(2ˣ − 8)(2ˣ + 4) = 0\n2ˣ = 8 or 2ˣ = −4\n2ˣ = 2³ or 2ˣ = 2⁻²\nx = 3 or x = −2',  # −4 read as 2⁻²
        '2²ˣ − 2² · 2ˣ = 32\n2ˣ(2ˣ − 4) = 32\n2ˣ = 32 or 2ˣ − 4 = 32\n2ˣ = 2⁵\nx = 5'], 0,              # a product equal to 32, not 0
        ["2ˣ⁺² = 2²·2ˣ = 4·2ˣ: let k = 2ˣ.", "Solve the quadratic in k; 2ˣ can never be negative."]),
    work("1.1.5", "√(−2x + 4) − x = 2", 4, [
        '√(−2x + 4) = 2 + x\n(√(−2x + 4))² = (2 + x)²\n−2x + 4 = 4 + x²\nx² + 2x = 0\nx(x + 2) = 0\nx = 0 or x = −2',   # (2 + x)² as 4 + x²
        '√(−2x + 4) = 2 + x\n(√(−2x + 4))² = (2 + x)²\n−2x + 4 = 4 + 4x + x²\nx² + 6x = 0\nx(x + 6) = 0\n'
        'x = 0 or x = −6',                                                                                      # no check: keeps x = −6
        '√(−2x + 4) = 2 + x\n(√(−2x + 4))² = (2 + x)²\n−2x + 4 = 4 + 4x + x²\nx² + 6x = 0\nx(x + 6) = 0\n'
        'x = 0 or x ≠ −6',                                                                                      # the memo
        '√(−2x + 4) = 2 − x\n(√(−2x + 4))² = (2 − x)²\n−2x + 4 = 4 − 4x + x²\nx² − 2x = 0\nx(x − 2) = 0\nx = 0 or x = 2'], 2,  # −x moved as −x
        ["Isolate the root on one side, then square both sides.", "Check each solution in the ORIGINAL equation: one fails."])]
q12 = [
    work("1.2", "Solve for x and y simultaneously:\n2x + y = 3\ny² + xy = 2", 5, [
        'y = 3 − 2x\n(3 − 2x)² + (3 − 2x)x = 2\n4x² − 12x + 9 − 2x² + 3x − 2 = 0\n2x² − 9x + 7 = 0\n(2x − 7)(x − 1) = 0\n'
        'x = {7}/{2} or x = 1\ny = −4 or y = 1',                                    # the memo
        'y = 3 − 2x\n(3 − 2x)² + (3 − 2x)x = 2\n4x² − 12x + 9 − 2x² + 3x − 2 = 0\n2x² − 9x + 7 = 0\n(2x + 7)(x + 1) = 0\n'
        'x = −{7}/{2} or x = −1\ny = 10 or y = 5',                                  # the factors' signs swapped
        'y = 3 − 2x\n(3 − 2x)² + (3 − 2x)x = 2\n4x² − 12x + 9 − 2x² + 3x − 2 = 0\n2x² − 15x + 7 = 0\n(2x − 1)(x − 7) = 0\n'
        'x = {1}/{2} or x = 7\ny = 2 or y = −11',                                   # −12x + 3x collected as −15x
        'y = 3 − 2x\n(3 − 2x)² + (3 − 2x)x = 2\n4x² − 12x + 9 − 2x² + 3x = 0\n2x² − 9x + 9 = 0\n(2x − 3)(x − 3) = 0\n'
        'x = {3}/{2} or x = 3\ny = 0 or y = −3'], 0,                                # the 2 on the right never moved across
        ["Make y the subject of the linear equation.", "Substitute it into the second equation to get a quadratic in x."])]
q13 = [
    mcq("1.3", "Consider the product (1 + 1/2)(1 + 1/3)(1 + 1/4)…\nEach factor in the product is of the form (1 + 1/n) for n ≥ 2.\n"
        "Determine ALL the values of n for which the product will be an integer value." + WORK, [
        'Product = {3}/{2} × {4}/{3} × {5}/{4} × … × {n + 1}/{n} = {n + 1}/{2}\nAn integer when n + 1 is divisible by 2\n'
        'n is an odd number greater than 2: n ∈ {3 ; 5 ; 7 ; …}',
        'Product = {3}/{2} × {4}/{3} × {5}/{4} × … × {n + 1}/{n} = {n}/{2}\nAn integer when n is divisible by 2\n'
        'n is an even number: n ∈ {2 ; 4 ; 6 ; …}',
        'Product = {3}/{2} × {4}/{3} × {5}/{4} × … × {n + 1}/{n} = {n + 1}/{2}\nAn integer when n + 1 is divisible by 2\n'
        'n is an odd number: n ∈ {1 ; 3 ; 5 ; …}',
        'Product = {3}/{2} × {4}/{3} × {5}/{4} × … × {n + 1}/{n} = n + 1\nAn integer for every n\n'
        'n is any natural number: n ∈ {2 ; 3 ; 4 ; …}'], 0,
        ["Write each factor as one fraction: 1 + 1/2 = 3/2, 1 + 1/3 = 4/3 …", "Most numerators and denominators cancel: what is left?"], marks=3)]

# ---- QUESTION 2, the question paper page 3 and the memo page 4 ----
q21 = [
    work("2.1.1", "Calculate the sum of this series.", 2, [
        'Sₙ = {n}/{2}[2a + (n − 1)d] with a = 7, d = 5, n = 20\nS₂₀ = {20}/{2}[2(7) + (20)(5)] = 1 140',        # n for (n − 1)
        'Sₙ = {n}/{2}[2a + (n − 1)d] with a = 7, d = 5, n = 20\nS₂₀ = {20}/{2}[7 + (20 − 1)(5)] = 1 020',       # a for 2a
        'Tₙ = a + (n − 1)d with a = 7, d = 5, n = 20\nT₂₀ = 7 + (20 − 1)(5) = 102',                            # the last term, not the sum
        'Sₙ = {n}/{2}[2a + (n − 1)d] with a = 7, d = 5, n = 20\nS₂₀ = {20}/{2}[2(7) + (20 − 1)(5)] = 1 090'], 3,  # the memo
        ["Sₙ = n/2 [2a + (n − 1)d].", "Read a, d and n from the description of the series."]),
    mcq("2.1.2", "The original arithmetic series is extended to 75 terms. The sum of these 75 terms is 14 400. Using sigma notation, write down an "
        "equation for the sum of the terms added to the original series." + WORK, [
        'Tₙ = 7 + (n − 1)(5) = 5n + 2\nS₇₅ − S₂₀ = 14 400 − 1 090 = 13 310\nΣ (5n + 2) = 13 310, summed from n = 20 to n = 75',
        'Tₙ = 7 + (n + 1)(5) = 5n + 12\nS₇₅ − S₂₀ = 14 400 − 1 090 = 13 310\nΣ (5n + 12) = 13 310, summed from n = 21 to n = 75',
        'Tₙ = 7 + (n − 1)(5) = 5n + 2\nS₇₅ = 14 400\nΣ (5n + 2) = 14 400, summed from n = 1 to n = 75',
        'Tₙ = 7 + (n − 1)(5) = 5n + 2\nS₇₅ − S₂₀ = 14 400 − 1 090 = 13 310\nΣ (5n + 2) = 13 310, summed from n = 21 to n = 75'], 3,
        ["Which terms were added to the original 20? The sum starts at the first new term.",
         "Find the general term Tₙ = a + (n − 1)d, and the sum of the new terms from S₇₅ and S₂₀."], marks=4)]
q22 = [
    work("2.2.1", "If T₉₉ of this quadratic pattern is 9 632, calculate the value of T₉₈.", 3, [
        'First differences: Tₙ = 2n − 1\n99th first difference = 2(99) − 1 = 197\nT₉₈ = 9 632 − 197 = 9 435',     # the 99th difference
        'First differences: Tₙ = 2n − 1\n98th first difference = 2(98) − 1 = 195\nT₉₈ = 9 632 − 195 = 9 437',     # the memo
        'First differences: Tₙ = 2n − 1\n98th first difference = 2(98) − 1 = 195\nT₉₈ = 9 632 + 195 = 9 827',     # adds going back
        'First differences: Tₙ = 2n − 1\n98th first difference = 2(98 − 1) = 194\nT₉₈ = 9 632 − 194 = 9 438'], 1,  # a bracket slip
        ["The first differences 1 ; 3 ; 5 ; … follow the pattern 2n − 1.", "T₉₉ − T₉₈ is one of those first differences: which one?"]),
    work("2.2.2", "If it is further given that the third term of the quadratic pattern is 32, determine the general term, Tₙ, of the quadratic "
         "pattern.", 5, [
        '28 ; 29 ; 32: second difference 2\n2a = 2, so a = 1\n3a + b = 1: 3(1) + b = 1, so b = −2\n'
        'T₃ = 1(3)² − 2(3) + c = 32, so c = 29\nTₙ = n² − 2n + 29',                  # the memo
        '28 ; 29 ; 32: second difference 2\na = 2 (the second difference)\n3a + b = 1: 3(2) + b = 1, so b = −5\n'
        'T₃ = 2(3)² − 5(3) + c = 32, so c = 29\nTₙ = 2n² − 5n + 29',                 # a = the second difference, not half of it
        '28 ; 29 ; 32: second difference 2\n2a = 2, so a = 1\n3a + b = 1: 3(1) + b = 1, so b = −2\n'
        'T₁ = a + b + c = 32: 1 − 2 + c = 32, so c = 33\nTₙ = n² − 2n + 33',         # the third term put into T₁'s equation
        '28 ; 29 ; 32: second difference 2\n2a = 2, so a = 1\n3a + b = 1: 3(1) + b = 1, so b = 4\n'
        'T₃ = 1(3)² + 4(3) + c = 32, so c = 11\nTₙ = n² + 4n + 11'], 0,              # 3 moved across without its sign change
        ["Work back from T₃ = 32 with the first differences to find T₁ and T₂.", "In Tₙ = an² + bn + c: 2a is the second difference, 3a + b the "
                                                                              "first first difference."])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 5-6 ----
q3 = [
    work("3.1", "Write down the radius of the 3rd circle.", 2, [
        '2nd circle: {6}/{2} = 3 cm\n3rd circle: {6}/{3} = 2 cm',                   # divides by the circle's number
        '2nd circle: {3}/{2} = 1,5 cm\n3rd circle: {1,5}/{2} = 0,75 cm',            # 6 cm taken as the first DIAMETER
        '2nd circle: {6}/{2} = 3 cm\n3rd circle: {3}/{2} = 1,5 cm',                 # the memo
        '2nd circle: {6}/{4} = 1,5 cm\n3rd circle: {1,5}/{4} = 0,375 cm'], 2,       # the areas' ratio ¼ used for the radii
        ["Each circle passes through the centre of the one before and touches it: its diameter is the radius before.",
         "Find the second circle's radius first, then the third's."]),
    work("3.2", "Calculate the sum of the areas of the first 10 circles.", 4, [
        '36π ; 18π ; 9π ; …\nr = {1}/{2} ; a = 36π\nS₁₀ = {36π[(½)¹⁰ − 1]}/{½ − 1}\nS₁₀ = 225,97',                # the radii's ratio for the areas
        '12π ; 6π ; 3π ; …\nr = {1}/{2} ; a = 12π\nS₁₀ = {12π[(½)¹⁰ − 1]}/{½ − 1}\nS₁₀ = 75,32',                  # 2πr, the circumference
        '36π ; 9π ; {9}/{4}π ; …\nr = {1}/{4} ; a = 36π\nS₁₀ = {36π[(¼)¹⁰ − 1]}/{1 − ¼}\nS₁₀ = −150,80',          # the two forms of Sₙ mixed
        '36π ; 9π ; {9}/{4}π ; …\nr = {1}/{4} ; a = 36π\nS₁₀ = {36π[(¼)¹⁰ − 1]}/{¼ − 1}\nS₁₀ = 150,80'], 3,       # the memo
        ["The areas πr² form a geometric sequence: find its first term and ratio.", "Use Sₙ = a(rⁿ − 1)/(r − 1) with n = 10."]),
    work("3.3", "Which circle has a diameter of 3/128 cm?", 4, [
        '6 ; 3 ; {3}/{2} ; …\nradius = {1}/{2} × {3}/{128} = {3}/{256}\n{3}/{256} = 6(½)ⁿ⁻¹\n{1}/{512} = (½)ⁿ⁻¹ = (½)⁹\nn − 1 = 9\nn = 10',
        '6 ; 3 ; {3}/{2} ; …\nradius = {3}/{128}\n{3}/{128} = 6(½)ⁿ⁻¹\n{1}/{256} = (½)ⁿ⁻¹ = (½)⁸\nn − 1 = 8\nn = 9',      # the diameter as the radius
        '6 ; 3 ; {3}/{2} ; …\nradius = 2 × {3}/{128} = {3}/{64}\n{3}/{64} = 6(½)ⁿ⁻¹\n{1}/{128} = (½)ⁿ⁻¹ = (½)⁷\nn − 1 = 7\n'
        'n = 8',                                                                                                             # doubles, not halves
        '12 ; 6 ; 3 ; …\nradius = {1}/{2} × {3}/{128} = {3}/{256}\n{3}/{256} = 12(½)ⁿ⁻¹\n{1}/{1 024} = (½)ⁿ⁻¹ = (½)¹⁰\n'
        'n − 1 = 10\nn = 11'], 0,                                                                                            # radius vs the diameters' term
        ["Work with radii (6 ; 3 ; 3/2 ; …) or diameters (12 ; 6 ; 3 ; …), but not both.",
         "Set the general term equal to the size you were given, and write both sides as powers of 1/2."])]

# ---- QUESTION 4, the question paper page 4 and the memo page 7 ----
q4 = [
    work("4.1", "Calculate the value of a.", 2, [
        'f(x) = aˣ − 1\n−{5}/{9} = a² − 1\na² = {14}/{9}\na = {√14}/{3}',        # the minus of −5/9 dropped
        'f(x) = aˣ − 1\n−{5}/{9} = a² − 1\na² = {4}/{9}\na = ±{2}/{3}',           # keeps the negative root (a > 0)
        'f(x) = aˣ − 1\n−{5}/{9} = a² − 1\na² = {4}/{9}\na = {2}/{9}',            # the square root of the numerator only
        'f(x) = aˣ − 1\n−{5}/{9} = a² − 1\na² = {4}/{9}\na = {2}/{3}'], 3,        # the memo
        ["B is on f, so its coordinates satisfy f(x) = aˣ − 1.", "Substitute x = 2 and y = −5/9; remember a > 0."]),
    mcq("4.2", "Write down the range of f." + ANS, ['y < −1', 'y > −1', 'y ≥ −1', 'x > −1'], 1,
        ["aˣ is always positive.", "So which values can aˣ − 1 take?"]),
    draw("4.3", "Sketch the graph of f. Clearly show the intercepts with the axes and asymptotes, if any.", 3, [
        ["Intercept with the axes: (0 ; 0)", 1], ["Asymptote y = −1", 1], ["Decreasing shape", 1]],
        ["With 0 < a < 1, aˣ gets smaller as x gets bigger.", "Find f(0), and the horizontal asymptote from the − 1."],
        memo="The memo's sketch: a decreasing curve from the top left, through (0 ; 0) and B, levelling off above the dotted asymptote y = −1 "
             "on the right."),
    work("4.4", "It is further given that C is a point on f at y = 19/8.\nDetermine the coordinates of C′, the image of C, when C is reflected "
         "about the line y = x.", 3, [
        '{19}/{8} = ({2}/{3})ˣ − 1\n{27}/{8} = ({2}/{3})ˣ\n({2}/{3})³ = ({2}/{3})ˣ\nx = 3, so C(3 ; {19}/{8})\nC′({19}/{8} ; 3)',     # flips 27/8 as (2/3)³
        '{19}/{8} = ({2}/{3})ˣ − 1\n{27}/{8} = ({2}/{3})ˣ\n({3}/{2})³ = ({3}/{2})⁻ˣ\nx = −3, so C(−3 ; {19}/{8})\nC′({19}/{8} ; −3)',  # the memo
        '{19}/{8} = ({2}/{3})ˣ − 1\n{27}/{8} = ({2}/{3})ˣ\n({3}/{2})³ = ({3}/{2})⁻ˣ\nx = −3, so C(−3 ; {19}/{8})\nC′(−3 ; −{19}/{8})',  # reflected in the x-axis
        '{19}/{8} = ({2}/{3})ˣ − 1\n{27}/{8} = ({2}/{3})ˣ\n({3}/{2})³ = ({3}/{2})⁻ˣ\nx = −3, so C(−3 ; {19}/{8})\nC′(−{19}/{8} ; 3)'],  # reflected in y = −x
        1, ["Put y = 19/8 into f and write both sides as powers of the same base.", "Reflecting about y = x swaps the coordinates."])]

# ---- QUESTION 5, the question paper page 5 and the memo page 8 ----
F5 = ("Axes with origin O. The hyperbola f has a dotted vertical asymptote that meets the x-axis at 1, and a dotted horizontal asymptote "
      "below the x-axis. Its left branch comes in from the left just above the horizontal asymptote, cuts the x-axis just left of O and "
      "the y-axis at 1, and climbs steeply beside the vertical asymptote. Its right branch rises from far below next to the vertical "
      "asymptote and levels off just below the horizontal asymptote. The straight line g rises from bottom left to top right through the "
      "point where the asymptotes cross.")
q5 = [
    num("5.1", "Write down the value of p.", -1, EXACT, "",
        ["The domain leaves out one x-value: that is where the vertical asymptote is.", "The vertical asymptote of a/(x + p) + q is x = −p."]),
    work("5.2", "Determine the equation of the horizontal asymptote of f.", 2, [
        'y = x − 3\ny = −1 − 3\ny = −4',          # p put in for the asymptote's x-value
        'y = x − 3\ny = 0 − 3\ny = −3',           # the y-intercept's x-value
        'y = x − 3\ny = 1 − 3\ny = −2',           # the memo
        'y = x − 3\ny = 1 + 3\ny = 4'], 2,        # a sign slip
        ["A line of symmetry passes through the point where the asymptotes cross.", "Put the vertical asymptote's x-value into g."]),
    work("5.3", "Calculate the value of a.", 2, [
        '1 = {a}/{0 − 1} − 2\n3 = {a}/{−1}\na = −3',              # the memo
        '1 = {a}/{0 + 1} − 2\n3 = {a}/{1}\na = 3',                # p taken as +1
        '1 = {a}/{0 − 1} − 2\n−1 = {a}/{−1}\na = 1',              # the 2 moved across without its sign change
        '1 = {a}/{0 − 1} − 2\n3 = {a}/{−1}\na = −{1}/{3}'], 0,    # divides by 3 instead of multiplying by −1
        ["Use the values of p and q you found.", "Substitute the y-intercept (0 ; 1) and solve for a."]),
    mcq("5.4", "For which values of x is f(x) ≥ 0?" + ANS, ['−{1}/{2} < x < 1', 'x ≤ −{1}/{2} or x > 1', '−{1}/{2} ≤ x < 1', '−{1}/{2} ≤ x ≤ 1'], 2,
        ["Find the x-intercept of f: solve f(x) = 0.", "Where is the graph on or above the x-axis? A vertical asymptote is never included."],
        marks=3, figure=fig("Q5", F5)),
    mcq("5.5", "Graph f undergoes a transformation to h where:\n• The domain and range of h are the same as that of f\n• h′(x), the derivative of "
        "h, is negative on its domain\nDescribe a possible transformation that f could have undergone to result in h." + ANS, [
        'f is reflected in the y-axis, then translated 2 units to the left',
        'f is reflected in the x-axis, then translated 2 units down',
        'f is reflected in the line y = x, then translated 2 units to the right',
        'f is reflected in the y-axis, then translated 2 units to the right'], 3,
        ["h keeps both asymptotes of f, but must decrease on both branches.", "Which reflection turns an increasing hyperbola into a decreasing "
                                                                              "one, and how must it then move to put the asymptotes back?"],
        marks=2, figure=fig("Q5", F5))]

# ---- QUESTION 6, the question paper page 6 and the memo pages 9-10 ----
q6 = [
    work("6.1", "Calculate the coordinates of B, the turning point of f.", 3, [
        'x = {4}/{2(−1)} = −2\ny = −(−2)² + 4(−2) + 5 = −7\nB(−2 ; −7)',      # x = b/(2a): the minus lost
        'x = {−4}/{2(−1)} = 2\ny = (−2)² + 4(2) + 5 = 17\nB(2 ; 17)',          # −(2)² squared as (−2)²
        'x = {−4}/{−1} = 4\ny = −(4)² + 4(4) + 5 = 5\nB(4 ; 5)',               # x = −b/a: the 2 left out
        'x = {−4}/{2(−1)} = 2\ny = −(2)² + 4(2) + 5 = 9\nB(2 ; 9)'], 3,        # the memo
        ["The turning point is at x = −b/(2a), or where f′(x) = 0.", "Substitute that x into f for the y-value."]),
    mcq("6.2", "Show that the equation of the line through A and C is given by g(x) = 2x + 2." + WORK, [
        'x² − 4x − 5 = 0\n(x + 5)(x − 1) = 0\nx = −5 or x = 1, so A(−1 ; 0)\nm = {8 − 0}/{3 + 1} = 2\ny − 0 = 2(x + 1)\ny = 2x + 2',
        'x² − 4x − 5 = 0\n(x − 5)(x + 1) = 0\nx = 5 or x = −1, so A(−1 ; 0)\nm = {8 − 0}/{3 + 1} = 2\ny − 0 = 2(x + 1)\ny = 2x + 2',
        'x² − 4x − 5 = 0\n(x − 5)(x + 1) = 0\nx = 5 or x = −1, so A(−1 ; 0)\nm = {3 + 1}/{8 − 0} = {1}/{2}\ny − 0 = 2(x + 1)\ny = 2x + 2',
        'x² − 4x − 5 = 0\n(x − 5)(x + 1) = 0\nx = 5 or x = −1, so A(−1 ; 0)\nm = {8 − 0}/{3 + 1} = 2\ny − 0 = 2(x − 1)\ny = 2x + 2'], 1,
        ["A is an x-intercept of f: solve f(x) = 0.", "Find the gradient through A and C, then substitute a point into y − y₁ = m(x − x₁)."], marks=3),
    work("6.3", "Calculate the maximum length of EH for f > g.", 4, [
        'EH = −x² + 4x + 5 − 2x + 2\nEH = −x² + 2x + 7\nMax EH at −2x + 2 = 0: x = 1\nMax length of EH = −(1)² + 2(1) + 7\n= 8',  # the bracket's sign
        'EH = −x² + 4x + 5 − (2x + 2)\nEH = −x² + 2x + 3\nMax EH at −2x + 2 = 0: x = 1\nMax length of EH = −(1)² + 2(1) + 3\n= 4',  # the memo
        'EH = 2x + 2 − (−x² + 4x + 5)\nEH = x² − 2x − 3\nMax EH at 2x − 2 = 0: x = 1\nMax length of EH = (1)² − 2(1) − 3\n= −4',  # g − f
        'EH = −x² + 4x + 5 − (2x + 2)\nEH = −x² + 2x + 3\nMax EH at the turning point of f: x = 2\nMax length of EH = −(2)² + 2(2) + 3\n'
        '= 3'], 1,                                                                                                             # at B, not where EH peaks
        ["EH = f(x) − g(x) at the same x.", "That difference is a parabola: find its maximum."]),
    work("6.4", "Given: k(x) = f(x + m) = −x² − 2mx − m² + 4x + 4m + 5\nDetermine the value of m such that g is a tangent to k.", 5, [
        "k′(x) = −2x − 2m + 4 = 0\nx = 2 − m\nk(2 − m) = g(2 − m)\n−(2 − m)² − 2m(2 − m) − m² + 4(2 − m) + 4m + 5 = 2(2 − m) + 2\n"
        "−2m − 3 = 0\nm = −{3}/{2}",                                                                  # k′ set to 0, not to g's gradient
        "k′(x) = −2x − 2m + 4 = 2\nx = m − 1\nk(m − 1) = g(m − 1)\n−(m − 1)² − 2m(m − 1) − m² + 4(m − 1) + 4m + 5 = 2(m − 1) + 2\n"
        "−4m² + 10m = 0\nm = 0 or m = {5}/{2}",                                                       # x = 1 − m solved as m − 1
        "k′(x) = −2x − 2m + 4 = 2\nx = 1 − m\nk(1 − m) = g(1 − m)\n−(1 − m)² − 2m(1 − m) − m² + 4(1 − m) + 4m + 5 = 2(1 − m) + 2\n"
        "−2m − 4 = 0\nm = −2",                                                                        # the memo
        "k′(x) = −2x − 2m + 4 = 2\nx = 1 − m\nk(1 − m) = g(1 − m)\n−(1 − m)² − 2m(1 − m) − m² + 4(1 − m) + 4m + 5 = 2(1 − m) + 2\n"
        "−2m − 4 = 0\nm = 2"], 2,                                                                     # the last step's sign
        ["g is a tangent where k′(x) equals the gradient of g.", "The point of contact lies on both k and g (or: the equation k(x) = g(x) has "
                                                                "exactly one root)."])]

# ---- QUESTION 7, the question paper page 7 and the memo pages 11-13 ----
q71 = [
    work("7.1", "Mary's grandparents deposited R5 000 into a savings account on the day that she was born. The account pays interest at a rate "
         "of 6,8% p.a., compounded quarterly. Calculate the accumulated amount in this account on Mary's 16th birthday.", 3, [
        'A = P(1 + i)ⁿ\nA = 5 000(1 + {6,8}/{400})⁶⁴\n= R14 706,56',          # the memo
        'A = P(1 + i)ⁿ\nA = 5 000(1 + {6,8}/{100})¹⁶\n= R14 325,51',          # compounded yearly, not quarterly
        'A = P(1 + in)\nA = 5 000(1 + {6,8}/{400} × 64)\n= R10 440,00',      # simple interest
        'A = P(1 + i)ⁿ\nA = 5 000(1 + {6,8}/{400})¹⁶\n= R6 547,95'], 0,       # the years, not the quarters, as n
        ["Compounded quarterly: divide the yearly rate by 4 and count the quarters.", "A = P(1 + i)ⁿ."])]
q72 = [
    work("7.2", "After 4 years, the value of a printer was half of its original value. Determine the rate at which the value of the printer "
         "depreciated over this period, if depreciation was calculated according to a straight-line method.", 2, [
        'A = P(1 − i)ⁿ\n{1}/{2}P = P(1 − i)⁴\n{1}/{2} = (1 − i)⁴\ni = 1 − ∜0,5 = 0,1591\nr = 15,91%',     # reducing balance, not straight line
        'A = P(1 + in)\n{1}/{2}P = P(1 + 4i)\n{1}/{2} = 1 + 4i\ni = −{1}/{8}\nr = −12,5%',                 # the growth formula
        'A = P(1 − in)\n{1}/{2}P = P(1 − 4i)\n{1}/{2} = 1 − 4i\ni = {3}/{8}\nr = 37,5%',                   # 4i = 1 + ½: a sign slip
        'A = P(1 − in)\n{1}/{2}P = P(1 − 4i)\n{1}/{2} = 1 − 4i\ni = {1}/{8}\nr = 12,5%'], 3,               # the memo
        ["Straight-line depreciation: A = P(1 − in).", "After 4 years, A is half of P."])]
q73 = [
    work("7.3.1", "Calculate the total interest that he will pay over the 5 years.", 2, [
        'A = 100 000(1 + {13,5}/{1 200})⁶⁰ = R195 664,52\nInterest: 195 664,52 − 100 000 = R95 664,52',   # the loan left to grow, no payments
        'Already paid: 2 300,98 × 60 = R138 058,80\nInterest: 138 058,80 − 100 000 = R38 058,80',         # the memo
        'Simple interest: I = Prn\nI = 100 000 × 0,135 × 5 = R67 500,00',                                 # simple interest
        'Already paid: 2 300,98 × 59 = R135 757,82\nInterest: 135 757,82 − 100 000 = R35 757,82'], 1,     # 59 instalments counted
        ["Add up all the instalments he pays in 5 years.", "The interest is what he pays above the amount he borrowed."]),
    work("7.3.2", "Tshepo paid R22 300,98 (his monthly instalment and an additional R20 000) on 1 March 2024 into the loan account. He continues "
         "to pay the original monthly instalment thereafter. How many months earlier will Tshepo repay the loan?", 7, [
        'i = {13,5}/{1 200} ; n = 24\nP = {2 300,98[1 − (1,01125)⁻²⁴]}/{0,01125} = R48 160,82\nR48 160,82 − R20 000 = R28 160,82\n'
        '28 160,82 = {2 300,98[1 − (1,01125)⁻ⁿ]}/{0,01125}\n0,862 = (1,01125)⁻ⁿ\nn = 13,27\n∴ 10 months earlier',   # n = the 24 PAID, not the 36 left
        'i = {13,5}/{1 200} ; n = 36\nP = {2 300,98[1 − (1,01125)⁻³⁶]}/{0,01125} = R67 804,94\nR67 804,94 − R22 300,98 = R45 503,96\n'
        '45 503,96 = {2 300,98[1 − (1,01125)⁻ⁿ]}/{0,01125}\n0,778 = (1,01125)⁻ⁿ\nn = 22,44\n∴ 13 months earlier',   # the instalment taken off twice
        'i = {13,5}/{1 200} ; n = 36\nP = {2 300,98[1 − (1,01125)⁻³⁶]}/{0,01125} = R67 804,94\nR67 804,94 − R20 000 = R47 804,94\n'
        '47 804,94 = {2 300,98[1 − (1,01125)⁻ⁿ]}/{0,01125}\n0,766 = (1,01125)⁻ⁿ\nn = 23,83\n∴ 12 months earlier',   # the memo
        'i = {13,5}/{1 200} ; n = 60\nP = R100 000, the loan\nR100 000 − R20 000 = R80 000\n'
        '80 000 = {2 300,98[1 − (1,01125)⁻ⁿ]}/{0,01125}\n0,609 = (1,01125)⁻ⁿ\nn = 44,33\n∴ 15 months earlier'], 2,  # the 24 instalments paid ignored
        ["Find the balance just after the payment on 1 March 2024: the present value of the instalments still to come.",
         "Take off the extra R20 000, then find how many instalments repay what is left."])]

# ---- QUESTION 8, the question paper page 7 and the memo pages 14-15 ----
q81 = [
    work("8.1.1", "d/dx [3x − 5x²]", 2, [
        '{d}/{dx}(3x − 5x²)\n= 3 − 10x²',      # the power not lowered
        '{d}/{dx}(3x − 5x²)\n= −10x',          # 3x treated as a constant
        '{d}/{dx}(3x − 5x²)\n= 3 + 10x',       # a sign slip
        '{d}/{dx}(3x − 5x²)\n= 3 − 10x'], 3,   # the memo
        ["Differentiate each term on its own.", "The derivative of axⁿ is naxⁿ⁻¹."]),
    work("8.1.2", "g′(x) if g(x) = 2/x² − ∛(x⁷)", 4, [
        'g(x) = {2}/{x²} − ∛(x⁷)\ng(x) = 2x⁻² − x⁷⁄³\ng′(x) = −4x⁻³ − {7}/{3}x⁴⁄³',       # the memo
        'g(x) = {2}/{x²} − ∛(x⁷)\ng(x) = 2x⁻² − x³⁄⁷\ng′(x) = −4x⁻³ − {3}/{7}x⁻⁴⁄⁷',      # the root's power upside down
        'g(x) = {2}/{x²} − ∛(x⁷)\ng(x) = 2x⁻² − x⁷⁄³\ng′(x) = −4x⁻¹ − {7}/{3}x⁴⁄³',       # −2 − 1 taken as −1
        'g(x) = {2}/{x²} − ∛(x⁷)\ng(x) = {2}/{x²} − x⁷⁄³\ng′(x) = {2}/{2x} − {7}/{3}x⁴⁄³'], 0,   # differentiates the denominator
        ["Write each term as a power of x first: 1/x² = x⁻², and a cube root is the power 1/3.", "Then use the power rule on each term."])]
q82 = [
    work("8.2", "Determine the equation of the tangent to f(x) = x³ − 4x² + 2x + 3 at x = 2.", 3, [
        'f′(x) = 3x² − 8x + 2\nm = f(2) = (2)³ − 4(2)² + 2(2) + 3 = −1\ny = f′(2) = 3(2)² − 8(2) + 2 = −2\ny + 2 = −1(x − 2)\ny = −x',  # f and f′
        'f′(x) = 3x² − 8x + 2\nm = f′(2) = 3(2)² − 8(2) + 2 = −2\ny = f(2) = (2)³ − 4(2)² + 2(2) + 3 = −1\ny − 1 = −2(x − 2)\n'
        'y = −2x + 5',                                                                                                               # y₁ = −1 with its sign lost
        'f′(x) = 3x² − 8x + 2\nm = f′(2) = 3(2)² − 8(2) + 2 = −2\ny = f(2) = (2)³ − 4(2)² + 2(2) + 3 = −1\ny + 1 = −2(x − 2)\n'
        'y = −2x + 3',                                                                                                               # the memo
        'f′(x) = 3x² − 8x + 2\nm = f′(2) = (3 × 2)² − 8(2) + 2 = 22\ny = f(2) = (2)³ − 4(2)² + 2(2) + 3 = −1\ny + 1 = 22(x − 2)\n'
        'y = 22x − 45'], 2,                                                                                                          # 3(2)² as (3 × 2)²
        ["The gradient of the tangent is f′(2).", "Find the point of contact from f(2), then use y − y₁ = m(x − x₁)."])]
q83 = [
    mcq("8.3.1", "Determine f′(x) from first principles." + WORK, [
        'f′(x) = lim(h→0) {f(x + h) − f(x)}/{h}\n= lim(h→0) {−6(x + h)² + 6x²}/{h}\n= lim(h→0) {−6x² − 12xh − 6h² + 6x²}/{h}\n'
        '= lim(h→0) {−12xh − 6h²}/{h}\n= lim(h→0) {h(−12x − 6h)}/{h}\n= lim(h→0) (−12x − 6h)\n= −12x',
        'f′(x) = lim(h→0) {f(x + h) − f(x)}/{h}\n= lim(h→0) {−6(x + h)² + 6x²}/{h}\n= lim(h→0) {−6x² − 6h² + 6x²}/{h}\n'
        '= lim(h→0) {−6h²}/{h}\n= lim(h→0) {h(−6h)}/{h}\n= lim(h→0) (−6h)\n= 0',
        'f′(x) = lim(h→0) {f(x + h) − f(x)}/{h}\n= lim(h→0) {−6(x + h)² − 6x²}/{h}\n= lim(h→0) {−6x² − 12xh − 6h² − 6x²}/{h}\n'
        '= lim(h→0) {−12xh − 6h²}/{h}\n= lim(h→0) {h(−12x − 6h)}/{h}\n= lim(h→0) (−12x − 6h)\n= −12x',
        'f′(x) = lim(h→0) {f(x + h) − f(x)}/{h}\n= lim(h→0) {−6(x + h)² + 6x²}/{h}\n= lim(h→0) {−6x² − 12xh − 6h² + 6x²}/{h}\n'
        '= lim(h→0) {−12xh − 6h²}/{h}\n= lim(h→0) {h(−12x − 6)}/{h}\n= lim(h→0) (−12x − 6)\n= −12x − 6'], 0,
        ["f′(x) = lim (h→0) [f(x + h) − f(x)]/h.", "Expand −6(x + h)² carefully, simplify, take out the common factor h, then let h → 0."], marks=5),
    mcq("8.3.2", "Write down how you will restrict the domain of f such that f⁻¹, the inverse of f, is a function." + ANS,
        ['x ∈ ℝ', 'y ≤ 0', 'x ≥ 0', '−1 ≤ x ≤ 1'], 2,
        ["The inverse is a function only when each y-value comes from ONE x-value.", "Keep only one side of the parabola's axis of symmetry."]),
    mcq("8.3.3", "Determine the equation of f⁻¹ for f⁻¹(x) ≤ 0. Write your answer in the form y = …" + WORK, [
        'y = −6x²\nx = −6y²\ny² = −{1}/{6}x\ny = ±√(−{1}/{6}x)\ny = √(−{1}/{6}x) ; x ≤ 0',
        'y = −6x²\nx = −6y²\ny² = {1}/{6}x\ny = ±√({1}/{6}x)\ny = −√({1}/{6}x) ; x ≥ 0',
        'y = −6x²\nx = −6y²\ny² = −6x\ny = ±√(−6x)\ny = −√(−6x) ; x ≤ 0',
        'y = −6x²\nx = −6y²\ny² = −{1}/{6}x\ny = ±√(−{1}/{6}x)\ny = −√(−{1}/{6}x) ; x ≤ 0'], 3,
        ["Swap x and y, then make y the subject.", "f⁻¹(x) ≤ 0 tells you which square root to keep."], marks=3)]

# ---- QUESTION 9, the question paper page 8 and the memo page 16 ----
F9 = ("Axes with origin O. The cubic f rises from bottom left, cuts the x-axis just left of O and the y-axis at C (at 7), climbs to its "
      "turning point A(1 ; 9), falls gently to its turning point B(5/2 ; 8), then rises again to the top right.")
q9 = [
    mcq("9.1", "For which values of x is f decreasing?" + ANS, ['x < 1 or x > {5}/{2}', '1 < x < {5}/{2}', '8 < x < 9', '0 < x < {5}/{2}'], 1,
        ["f decreases from one turning point to the next.", "Read the x-values of A and B."], marks=2, figure=fig("Q9", F9)),
    mcq("9.2", "Write down the x-intercepts of f′, the derivative of f." + ANS,
        ['x = 9 and x = 8', 'x = {7}/{4}', 'x = −1 and x = −{5}/{2}', 'x = 1 and x = {5}/{2}'], 3,   # the turning points' y-values; f″ = 0; signs
        ["At a turning point the gradient is zero.", "So where on the graph of f is f′(x) = 0?"], marks=2, figure=fig("Q9", F9)),
    mcq("9.3", "For which values of x will f be concave up?" + ANS, [
        'x = ({5}/{2} + 1) ÷ 2 = {7}/{4}, so x > {7}/{4}', 'x = ({5}/{2} + 1) ÷ 2 = {7}/{4}, so x < {7}/{4}',
        'x = ({5}/{2} − 1) ÷ 2 = {3}/{4}, so x > {3}/{4}', 'x = {5}/{2} + 1 = {7}/{2}, so x > {7}/{2}'], 0,
        ["The point of inflection of a cubic lies halfway between its turning points.", "f ends rising to the right: on which side of the point "
                                                                                       "of inflection does it curve upwards?"],
        marks=2, figure=fig("Q9", F9)),
    mcq("9.4", "Determine the value of k for which y = f(x) + k will have THREE positive x-intercepts." + ANS,
        ['8 < k < 9', '−9 < k < −7', '−9 < k < −8', '−9 ≤ k ≤ −8'], 2,
        ["Adding k slides the graph up or down.", "For three x-intercepts A must stay above the x-axis and B go below it; check where the "
                                                  "y-intercept ends up too."], marks=2, figure=fig("Q9", F9))]

# ---- QUESTION 10, the question paper page 8 and the memo page 16 ----
q10 = [
    work("10.1", "Calculate the maximum speed that the cyclist reached on this ride.", 3, [
        '−6t + 18 = 0\n18 = 6t\nt = 3\ns′(3) = −3(3)² + 18(3) = 27',              # the memo
        '−3t² + 18t = 0\n−3t(t − 6) = 0\nt = 6\ns′(6) = −3(6)² + 18(6) = 0',      # s′(t) = 0: where the speed is zero
        '−6t + 18 = 0\n18 = 6t\nt = 3\ns′(3) = (−3 × 3)² + 18(3) = 135',          # −3(3)² as (−3 × 3)²
        '−6t + 18 = 0\n18 = −6t\nt = −3\ns′(−3) = −3(−3)² + 18(−3) = −81'], 0,    # 18 moved across without its sign change
        ["The speed is greatest where its own derivative is zero.", "Find t from s″(t) = 0, then substitute it into s′(t)."]),
    work("10.2", "Calculate the distance between town P and town T.", 5, [
        '−3t² + 18t = 0: −3t(t − 6) = 0\nt = 0 or t = 6\ns(t) = at³ + bt², s′(t) = 3at² + 2bt\n3a = −3 and 2b = 18: a = −1, b = 36\n'
        's(6) = −(6)³ + 36(6)²\ns(6) = 1 080',                                       # multiplies by 2, not divides
        '−3t² + 18t = 0: −3t(t − 6) = 0\nt = 0 or t = 6\ns(t) = at³ + bt², s′(t) = 3at² + 2bt\n3a = −3 and 2b = 18: a = −1, b = 9\n'
        's(6) = −(6)³ + 9(6)²\ns(6) = 108',                                          # the memo
        '−3t² + 18t = 0: −3t(t − 6) = 0\nt = 0 or t = 6\ns(t) = at³ + bt², s′(t) = 3at² + 2bt\na = −3 and b = 18, the coefficients of s′\n'
        's(6) = −3(6)³ + 18(6)²\ns(6) = 0',                                          # raises the powers, keeps s′'s coefficients
        '−3t² + 18t = 0: −3t(t − 6) = 0\nt = 0 or t = 6\ns(t) = at³ + bt², s′(t) = 3at² + 2bt\n3a = −3 and 2b = 18: a = 1, b = 9\n'
        's(6) = (6)³ + 9(6)²\ns(6) = 540'], 1,                                       # a's sign lost
        ["The cyclist stops when the speed is zero: find that t.", "s′(t) is the derivative of the distance s(t): work back to s(t) = at³ + bt², "
                                                                  "then substitute."])]

# ---- QUESTION 11, the question paper page 9 and the memo page 17 ----
q11b = [
    draw("11.1", "Draw a Venn diagram to represent ALL the learners sitting for these examinations.", 3, [
        ["2 in the region for all three subjects", 1],
        ["3, 4 and 5 in the regions for exactly two subjects (T and G only, M and G only, M and T only)", 1],
        ["6, 9 and 11 in the regions for one subject only (T only, G only, M only)", 1]],
        ["Start with the centre: Tourism's total minus its other three regions.", "Then work out the 'only' regions for Mathematics and "
                                                                                  "Geography from their totals."],
        memo="The memo's Venn diagram: M only 11, T only 6, G only 9; M and T only 5, M and G only 4, T and G only 3; all three 2; 40 learners "
             "in all, none outside the circles."),
    work("11.2", "Calculate the probability that a learner, chosen at random, will sit for examinations in at least TWO of the subjects.", 2, [
        'P(at least two subjects) = {4 + 5 + 3}/{40}\n= {12}/{40} = {3}/{10} = 0,3',                   # the centre (all three) left out
        'P(at least two subjects) = {4 + 2 + 5 + 3}/{22 + 16 + 18}\n= {14}/{56} = {1}/{4} = 0,25',     # the subject totals as the total
        'P(at least two subjects) = {11 + 6 + 9}/{40}\n= {26}/{40} = {13}/{20} = 0,65',                # one subject only: the complement
        'P(at least two subjects) = {4 + 2 + 5 + 3}/{40}\n= {14}/{40} = {7}/{20} = 0,35'], 3,          # the memo
        ["Add the regions with two or three subjects.", "Divide by the number of learners in all."]),
    mcq("11.3", "Determine if the events: sitting for examinations in Mathematics and sitting for examinations in Tourism are independent. "
        "Support your answer with the necessary calculations." + WORK, [
        'P(M) + P(T) = {22}/{40} + {16}/{40} = {19}/{20} = 0,95\nP(M and T) = {7}/{40} = 0,175\nP(M) + P(T) ≠ P(M and T)\n'
        'Events M and T are not independent',
        'P(M) × P(T) = {22}/{40} × {16}/{40} = {11}/{50} = 0,22\nP(M and T) = {7}/{40} = 0,175\nP(M) × P(T) ≠ P(M and T)\n'
        'Events M and T are not independent',
        'P(M) × P(T) = {22}/{40} × {16}/{40} = {11}/{50} = 0,22\nP(M and T) = {5}/{40} = 0,125\nP(M) × P(T) ≠ P(M and T)\n'
        'Events M and T are not independent',
        'P(M) × P(T) = {22}/{40} × {16}/{40} = {11}/{50} = 0,22\nP(M and T) = {7}/{40} = 0,175\nP(M and T) ≠ 0, so M and T are not mutually '
        'exclusive\nEvents M and T are independent'], 1,
        ["Independent events: P(M and T) = P(M) × P(T).", "P(M and T) counts every learner in both circles, the centre too."], marks=4)]

# ---- QUESTION 12, the question paper page 9 and the memo page 17 ----
q12b = [
    work("12.1", "Determine how many different codes can be formed if letters and digits may be repeated.", 2, [
        '26 × 10 × 26 × 10\n= 67 600',         # the memo
        '26 + 10 + 26 + 10\n= 72',             # adds the choices
        '26 × 10 × 25 × 9\n= 58 500',          # no repeats, though repeats are allowed
        '36 × 36 × 36 × 36\n= 1 679 616'], 0,  # any letter or digit in every place
        ["Count the choices for each of the four places.", "Letters and digits may repeat: multiply the choices."]),
    work("12.2", "Determine how many different codes can be formed if:\n• The letters D, F, I, Q, U and V may NOT be used\n• The code may NOT "
         "start with a W or a Z\n• Letters or digits may NOT be repeated\n• The code ends with an odd digit", 4, [
        '1st: 18 ; 2nd: 10 ; 3rd: 19 ; 4th: 5\n18 × 10 × 19 × 5 = 17 100',     # the second digit may repeat the last
        '1st: 18 ; 2nd: 9 ; 3rd: 17 ; 4th: 5\n18 × 9 × 17 × 5 = 13 770',       # W and Z kept out of the third place too
        '1st: 18 ; 2nd: 9 ; 3rd: 19 ; 4th: 5\n18 × 9 × 19 × 5 = 15 390',       # the memo
        '1st: 18 ; 2nd: 9 ; 3rd: 20 ; 4th: 5\n18 × 9 × 20 × 5 = 16 200'], 2,   # the third letter may repeat the first
        ["Fill the most restricted places first: the last digit and the first letter.", "A letter or digit used once cannot be used again."]),
    work("12.3", "The company wishes to increase the number of 4-character codes formed in QUESTION 12.2 by allowing the letters D, F, I, Q, U "
         "and V to be used. Calculate the percentage increase in the number of different codes that can now be formed.", 2, [
        '24 × 9 × 25 × 5 = 27 000\n{27 000 − 15 390}/{27 000} × 100 = 43,00%',     # divides by the new count
        '24 × 9 × 25 × 5 = 27 000\n{27 000 − 15 390}/{15 390} × 100 = 75,44%',     # the memo
        '24 × 9 × 25 × 5 = 27 000\n{27 000}/{15 390} × 100 = 175,44%',             # the new count as a percentage of the old
        '26 × 9 × 25 × 5 = 29 250\n{29 250 − 15 390}/{15 390} × 100 = 90,06%'], 1,  # W and Z allowed first as well
        ["Count the codes again with all 26 letters, the other rules unchanged.", "Percentage increase = (new − old)/old × 100."])]

CODE = {"head": ["1st character", "2nd character", "3rd character", "4th character"], "rows": [["letter", "digit", "letter", "digit"]]}
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Equations and inequalities", "marks": 19, "lead": "Solve for x:", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Simultaneous equations", "marks": 5, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Patterns in a product", "marks": 3, "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Arithmetic series", "marks": 6,
     "lead": "The first term of an arithmetic series is 7. The common difference of this series is 5 and the series contains 20 terms.",
     "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Quadratic patterns", "marks": 8,
     "lead": "The sequence of the first differences of a quadratic pattern is: 1 ; 3 ; 5 ; …", "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Geometric patterns", "marks": 10,
     "lead": "A circle with radius 6 cm is drawn.\nA second, smaller circle is drawn through the centre of the first circle and also touches the "
             "first circle internally, as shown in the diagram.\nA third, smaller circle is drawn through the centre of the second circle and "
             "touches the second circle internally. The process of drawing circles continues and forms a geometric pattern.",
     "figure": fig("Q3", "Three circles, each touching the one before it internally at the top: the largest circle; a second circle whose "
                   "lowest point, marked with a dot, is the centre of the largest circle; and a third, smallest circle whose lowest point, "
                   "marked with a dot, is the centre of the second circle."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Exponential functions", "marks": 9,
     "lead": "Given: f(x) = aˣ − 1 for a > 0. B(2 ; −5/9) is a point on f.", "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Hyperbolas", "marks": 10,
     "lead": "Sketched below is the graph of f(x) = a/(x + p) + q having the domain (−∞ ; 1) ∪ (1 ; ∞).\nThe graph of f cuts the y-axis at "
             "(0 ; 1). A line of symmetry of f is given by g(x) = x − 3.", "figure": fig("Q5", F5), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Parabola and straight line", "marks": 15,
     "lead": "In the diagram below, the graphs of f(x) = −x² + 4x + 5 and g, a straight line, are drawn.\nC(3 ; 8) is a point of intersection "
             "of f and g. EH is drawn parallel to the y-axis, with E a point on f and H a point on g.",
     "figure": fig("Q6", "Axes with origin O. The parabola f opens downwards: it cuts the x-axis at A, left of O, and at D, far to the right, "
                   "cuts the y-axis at 5, and has its turning point B at the top. The straight line g rises from bottom left to top right: it "
                   "cuts the x-axis at A too and meets f again at C(3 ; 8), right of B. E on f and H on g, between the y-axis and B, are joined "
                   "by a dashed vertical line EH."), "items": q6},
    {"id": "7.1", "title": "Question 7.1", "kind": "Compound interest", "marks": 3, "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Straight-line depreciation", "marks": 2, "items": q72},
    {"id": "7.3", "title": "Question 7.3", "kind": "Loan repayments", "marks": 9,
     "lead": "Tshepo was granted a loan of R100 000 on 1 March 2022 at an interest rate of 13,5% p.a., compounded monthly. Tshepo agreed to "
             "repay the loan over 5 years in monthly instalments of R2 300,98, starting on 1 April 2022.", "items": q73},
    {"id": "8.1", "title": "Question 8.1", "kind": "Rules of differentiation", "marks": 6, "lead": "Determine:", "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Equation of a tangent", "marks": 3, "items": q82},
    {"id": "8.3", "title": "Question 8.3", "kind": "First principles and inverses", "marks": 9, "lead": "Given: f(x) = −6x²", "items": q83},
    {"id": "9", "title": "Question 9", "kind": "Cubic functions", "marks": 8,
     "lead": "A(1 ; 9) and B(5/2 ; 8) are the turning points of graph f below.\nC(0 ; 7) is the y-intercept of f.", "figure": fig("Q9", F9),
     "items": q9},
    {"id": "10", "title": "Question 10", "kind": "Rates of change", "marks": 8,
     "lead": "A cyclist rode from town P and stopped at town T. The speed (in km/h) at which this cyclist rode, is represented by the equation "
             "s′(t) = −3t² + 18t.\n\nNOTE: Speed is the rate of change in distance with respect to time.", "items": q10},
    {"id": "11", "title": "Question 11", "kind": "Venn diagrams and independence", "marks": 9,
     "lead": "A certain number of learners are sitting for examinations in Mathematics, Tourism and Geography.\n• All these learners sit for at "
             "least one of these examinations.\n• The total number of learners who sit for Mathematics (M), is 22.\n• The total number of "
             "learners sitting for Tourism (T), is 16.\n• The total number of learners sitting for Geography (G), is 18.\n• 5 learners sit for "
             "Mathematics and Tourism, but not Geography.\n• 4 learners sit for Mathematics and Geography, but not Tourism.\n• 3 learners sit "
             "for Tourism and Geography, but not Mathematics.\n• 6 learners sit for only Tourism.", "items": q11b},
    {"id": "12", "title": "Question 12", "kind": "Counting principle", "marks": 8,
     "lead": "A company generates a 4-character code using the 26 letters of the alphabet and the 10 digits, from 0 to 9.\n\nThe code is in the "
             "form:", "table": CODE, "items": q12b},
]

# A part whose options show an earlier part's answer opens only once that part is answered (`after`, 2026-10-10)
GATES = {"2.1.2": ["2.1.1"],          # S₇₅ − S₂₀ = 14 400 − 1 090: the sum 2.1.1 asks for
         "3.2": ["3.1"],              # the areas 36π ; 9π ; 9/4 π: the third radius 3/2
         "3.3": ["3.1"],              # the radii 6 ; 3 ; 3/2
         "4.4": ["4.1"],              # (2/3)ˣ: the value of a
         "5.3": ["5.1", "5.2"],       # a/(0 − 1) − 2: p = −1 and q = −2
         "11.2": ["11.1"],            # 4 + 2 + 5 + 3: the Venn diagram's regions
         "11.3": ["11.1"],            # P(M and T) = 7/40: the Venn diagram's regions
         "12.3": ["12.2"]}            # (27 000 − 15 390)/15 390: the count 12.2 asks for
for _m in missions:
    for _it in _m["items"]:
        if _it["n"] in GATES:
            _it["after"] = GATES[_it["n"]]

ITEMS = [i for m in missions for i in m["items"]]
_nums = [i["n"] for i in ITEMS]
assert all(a in _nums and _nums.index(a) < _nums.index(n) and any(a in [i["n"] for i in m["items"]] and n in [i["n"] for i in m["items"]]
                                                                  for m in missions) for n, aa in GATES.items() for a in aa), "a gate out of place"
# every part that played as typed steps (or a num with a working) before 2026-10-10, now authored multiple choice
assert tuple(AUTHORED) == ("1.1.1", "1.1.2", "1.1.4", "1.1.5", "1.2", "2.1.1", "2.2.1", "2.2.2", "3.1", "3.2", "3.3", "4.1", "4.4", "5.2",
                           "5.3", "6.1", "6.3", "6.4", "7.1", "7.2", "7.3.1", "7.3.2", "8.1.1", "8.1.2", "8.2", "10.1", "10.2", "11.2",
                           "12.1", "12.2", "12.3"), AUTHORED
assert not [i["n"] for i in ITEMS if i["t"] == "steps"], "typed steps left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["5.1"], "a typed number left besides the 1-mark read-off 5.1"
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # the authored answers and the formula/proof workings

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every typed calculation plays as the memo's "
                                                       "FIRST working plus three built from common errors, 0 or full marks: " + ", ".join(AUTHORED)
                                                       + " (%d parts, %d marks). A value the memo also accepts (another method's balance, "
                                                         "x ≤ 0 in 8.3.2, the other transformations in 5.5) is never a wrong option; only "
                                                         "5.1 (p = −1, a 1-mark read-off with no working) stays a typed number." % (
                                                             len(AUTHORED), AUTHORED_MARKS)},
        {"n": ANSWERS[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): " + ", ".join(ANSWERS) + " ask for written "
                                                      "working or an answer a word marker cannot read (an inequality, an interval, a range, a "
                                                      "set of values, a sigma equation, a square-root equation, a two-move transformation, a "
                                                      "pair of read-off values, a proof); each is played as four options, the memo's answer or "
                                                      "working and three built from common errors, and keeps its marks (%d marks in all)."
                                                      % sum(i["marks"] for i in ITEMS if i["n"] in ANSWERS)},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 12), hand-transcribed from a SCANNED question paper (no "
                                                           "text layer) and the memo's page images (its text layer garbles fractions and powers); "
                                                           "no API call."},
        {"n": "2.1.1", "kind": "no_fit", "detail": "A working line never ends in a bracket (the player draws a trailing [..] as a proof's reason): "
                                                   "2.1.1 writes the memo's Sₙ = n/2[2a + (n − 1)d] with 'with a = 7, d = 5, n = 20' after it; "
                                                   "8.1.1 writes d/dx(3x − 5x²) with round brackets. A fraction inside a fraction is written "
                                                   "inline: ¼ and ½ in 3.2, i = 0,01125 in 7.3.2 (the memo's 13,5/1200)."},
        {"n": "2.1.2", "kind": "no_fit", "detail": "Parts whose options show an earlier part's answer open only after it (after): " + "; ".join(
            "%s after %s" % (n, ", ".join(a)) for n, a in GATES.items()) + "."},
        {"n": "4.3", "kind": "no_fit", "detail": "Drawings (4.3 the sketch of f, 11.1 the Venn diagram) are done on paper and self-checked against "
                                                 "the memo's three criteria each."},
        {"n": "5.5", "kind": "no_fit", "detail": "The memo accepts four transformations (reflect in the y-axis then 2 units right; reflect in the "
                                                 "x-axis then 4 units down; reflect about x = 1; reflect about y = −2). The MCQ offers the first; "
                                                 "each distractor was checked to change the domain or range of f (2 units left: x ≠ −3; x-axis then "
                                                 "2 down: y ≠ 0; y = x then 2 right: x ≠ 0)."},
        {"n": "8.3.2", "kind": "no_fit", "detail": "The memo accepts x ≥ 0 OR x ≤ 0; only x ≥ 0 (the memo's first) is an option, so the MCQ has one "
                                                   "right answer; the distractors (x ∈ ℝ, y ≤ 0, −1 ≤ x ≤ 1) leave f⁻¹ not a function."},
        {"n": "9.1", "kind": "low_confidence", "detail": "The memo prints only 1 < x < 5/2; the closed interval 1 ≤ x ≤ 5/2, which some teachers "
                                                         "accept for 'decreasing', is deliberately NOT a distractor."},
        {"n": "9.2", "kind": "no_fit", "detail": "The x-intercepts of f′ are read off the turning points (the memo: (1 ; 0) and (5/2 ; 0), no "
                                                 "working), so the part is an answer MCQ: x = 1 and x = 5/2 against the turning points' y-values, "
                                                 "the point of inflection 7/4 and the signs flipped."},
        {"n": "7.3.2", "kind": "memo_issue", "detail": "The memo's first method rounds (1,01125)⁻ⁿ to 0,766 and prints n = 23,83; unrounded it is "
                                                       "23,797, and the memo's second method prints n = 23,80 (balance R67 805,20 / R47 805,20). "
                                                       "The right option is the first method as printed (n = 23,83, 12 months earlier); the "
                                                       "distractors round their (1,01125)⁻ⁿ to three decimals the same way (0,862 / 0,778 / 0,609)."},
        {"n": "12", "kind": "no_fit", "detail": "The code's form is printed as one row of four boxes (letter, digit, letter, digit); the table's "
                                                "heads (1st to 4th character) are ours."},
    ],
}

# ---- self-checks: totals, and the authored options' shape (rule: the layout must never point at the answer) ----
QTOT = {"1": 27, "2": 14, "3": 10, "4": 9, "5": 10, "6": 15, "7": 14, "8": 18, "9": 8, "10": 8, "11": 9, "12": 8}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
for qn, want in QTOT.items():
    got = sum(i["marks"] for m in missions if m["id"].split(".")[0] == qn for i in m["items"])
    assert got == want, ("Question " + qn, got, want)
assert sum(i["marks"] for i in ITEMS) == 150
for i in ITEMS:
    assert len(i["clues"]) == 2, i["n"]
    if i["t"] == "mcq":
        o = i["opts"]
        assert len(o) == 4 and len(set(o)) == 4 and 0 <= i["a"] < 4, i["n"]
        assert len({shape(x) for x in o}) == 1, (i["n"], "options differ in line count or [reasons]", [shape(x) for x in o])
        assert not any(shape(x)[1] for x in o), (i["n"], "a line ends in [..]: the player would draw it as a reason column")
        assert i["q"].endswith(ANS) or i["q"].endswith(WORK), i["n"]
# the right letter, spread evenly over A-D across the paper
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread

out = Path(__file__).parent / "out" / "math-p1-2024-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the memo's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 12 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    print(m["id"], "parts:", len(m["items"]), "marks:", sum(i["marks"] for i in m["items"]))
print("right options:", spread, "| authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks")
print("total:", sum(i["marks"] for i in ITEMS))
