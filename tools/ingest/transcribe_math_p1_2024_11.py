"""Mathematics P1 Nov 2024, the whole paper (Questions 1 to 12), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working are
the paper's and the memo's own (its English); clues, figure captions and the authored multiple-choice distractors are ours. No API
call: the transcription is the source, kept in git (out/ is not). The question paper is a SCAN (no text layer): read from its page
images (1,5x, formulas at 3x); the memo has a text layer whose fractions and exponents garble, so it was read from its page
images (1,6x).

  python tools/ingest/transcribe_math_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P1 Nov 2024 Eng.pdf" "<...>/Mathematics P1 Nov 2024 MG Afr & Eng.pdf" --id math-p1-2024-11 --from-json

How the memo's shapes map (Mathematics: the phone has a number keypad, multiple choice, short text and self-checked drawings,
no algebra input):
  a NUMBER (a solution, a sum, a term, n, an amount, a probability, a coordinate, a count) -> steps, each step ONE number the
  memo's method produces, its method marks riding on it; two solutions -> "Smaller solution, x" / "Larger solution, x"; a value
  that does not terminate is keyed at the paper's TWO decimals (instruction 7) with a tolerance of 0,006 (half a unit of the
  second decimal plus a hair); money to the cent: 0,011; an exact value: 0,001. One read-off number -> num.
  An EXPRESSION answer is decomposed into the numbers that fix it (a general term's a, b and c; a derivative's coefficients; a
  tangent's m and c; an asymptote's q), because the strict term ignores signs.
  Authored multiple choice (Murci's ruling, 2026-10-10) for what a word or number marker cannot score: an inequality or interval,
  a range, a domain restriction, a set of values, a sigma equation, an equation with a square root, a transformation of two moves,
  a "show that", first principles and an independence argument. Four options: the memo's answer or working and three built from
  real errors (a lost condition, the wrong region, ends included, a sign slip, the wrong formula, a flawed step that still claims
  the result). Workings are laid out as the memo's lines ("\\n"), fractions as {numerator}/{denominator} (drawn stacked), and every
  option of a part has the same shape; the stem ends "Choose the correct answer." (a short answer) or "Choose the correct
  working." (a working). The part keeps its marks.
  "Sketch the graph" and "Draw a Venn diagram" -> draw (self-checked against the memo's criteria).
Missions: Questions 3, 4, 5, 6, 9, 10, 11 and 12 share a stem, a diagram or a graph, so each is one mission; Questions 1, 2, 7 and 8
are their numbered groups (1.1, 1.2, 1.3, 2.1, 2.2 ...). A single-line MCQ in a figure mission carries the figure itself (the MCQ
stage shows an item's own figure only); a working MCQ plays on the page, under the mission's figure.
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the ink of the 3x page images and checked on a contact sheet with
the ingest's 1% padding; no label touches a crop's top-left corner, so none needs an inset."""
import json
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


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


EXACT, DP2, CENT = 0.001, 0.006, 0.011   # an exact value; a value keyed at two decimals; rands and cents
ANS, WORK = "\n\nChoose the correct answer.", "\n\nChoose the correct working."

# ---- QUESTION 1, the question paper page 3 and the memo pages 2-3 ----
q11 = [
    steps("1.1.1", "x(x − 3) = 0", 2, [
        ("Smaller solution, x", 1, 0, EXACT, "x = 0 ✓"),
        ("Larger solution, x", 1, 3, EXACT, "x = 3 ✓")],
        ["A product is zero only when one of its factors is zero.", "Set each factor equal to zero."]),
    steps("1.1.2", "2x² + 1 = 4x (correct to TWO decimal places)", 4, [
        ("Smaller solution, x", 2, 0.29, DP2, "2x² − 4x + 1 = 0 ✓ (standard form); x = 0,29 ✓"),
        ("Larger solution, x", 2, 1.71, DP2, "x = [−(−4) ± √((−4)² − 4(2)(1))]/(2(2)) ✓ (correct substitution in correct formula); x = 1,71 ✓")],
        ["Bring every term to one side first: ax² + bx + c = 0.", "It does not factorise: use the quadratic formula and round at the end."]),
    mcq("1.1.3", "x² − 2x − 3 > 0" + ANS, ['−1 < x < 3', 'x < −3 or x > 1', 'x < −1 or x > 3', 'x ≤ −1 or x ≥ 3'], 2,
        ["Factorise the left-hand side and find the critical values.", "Sketch the parabola: where is it ABOVE the x-axis?"], marks=4),
    steps("1.1.4", "2²ˣ − 2ˣ⁺² − 32 = 0", 5, [
        ("The value of 2ˣ that gives a solution", 4, 8, EXACT, "2²ˣ − 2².2ˣ − 32 = 0 ✓ (use of exponential law); (2ˣ − 8)(2ˣ + 4) = 0 ✓ (factors); "
                                                              "2ˣ = 8 ✓ or 2ˣ ≠ −4 ✓ (no solution)"),
        ("x", 1, 3, EXACT, "2ˣ = 2³; x = 3 ✓ (answer)")],
        ["2ˣ⁺² = 2²·2ˣ = 4·2ˣ: let k = 2ˣ.", "Solve the quadratic in k; 2ˣ can never be negative."]),
    steps("1.1.5", "√(−2x + 4) − x = 2", 4, [
        ("x", 4, 0, EXACT, "√(−2x + 4) = 2 + x ✓ (isolating the root); (√(−2x + 4))² = (2 + x)² ✓ (squaring both sides); −2x + 4 = 4 + 4x + x²; "
                           "x² + 6x = 0 ✓ (standard form); x(x + 6) = 0; x = 0 or x ≠ −6 ✓ (answers with selection)")],
        ["Isolate the root on one side, then square both sides.", "Check each solution in the ORIGINAL equation: one fails."])]
q12 = [
    steps("1.2", "Solve for x and y simultaneously:\n2x + y = 3\ny² + xy = 2", 5, [
        ("Solution with the smaller x: x", 2, 1, EXACT, "y = 3 − 2x ✓ (eq 1); (3 − 2x)² + (3 − 2x)x = 2 ✓ (substitution)"),
        ("Solution with the smaller x: y", 1, 1, EXACT, "4x² − 12x + 9 − 2x² + 3x − 2 = 0; 2x² − 9x + 7 = 0 ✓ (standard form)"),
        ("Solution with the larger x: x", 1, 3.5, EXACT, "(2x − 7)(x − 1) = 0; x = 7/2 or x = 1 ✓ (both x-values)"),
        ("Solution with the larger x: y", 1, -4, EXACT, "y = −4 or y = 1 ✓ (both y-values). OR x = (3 − y)/2 ✓ (eq 1); y² + ((3 − y)/2)y = 2 ✓ "
                                                       "(substitution); y² + 3y − 4 = 0 ✓ (standard form); (y + 4)(y − 1) = 0, y = −4 or y = 1 ✓; "
                                                       "x = 7/2 or x = 1 ✓")],
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
    steps("2.1.1", "Calculate the sum of this series.", 2, [
        ("Sum of the series", 2, 1090, EXACT, "Sₙ = n/2 [2a + (n − 1)d]; S₂₀ = 20/2 [2(7) + (20 − 1)(5)] ✓ (substitution); S₂₀ = 1 090 ✓")],
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
    steps("2.2.1", "If T₉₉ of this quadratic pattern is 9 632, calculate the value of T₉₈.", 3, [
        ("The first difference between T₉₈ and T₉₉", 1, 195, EXACT, "Tₙ = 2n − 1 (the first differences); 98th first difference = 2(98) − 1 = 195 ✓ (answer)"),
        ("T₉₈", 2, 9437, EXACT, "T₉₈ = 9 632 − 195 ✓ (method) = 9 437 ✓ (answer)")],
        ["The first differences 1 ; 3 ; 5 ; … follow the pattern 2n − 1.", "T₉₉ − T₉₈ is the 98th first difference."]),
    steps("2.2.2", "If it is further given that the third term of the quadratic pattern is 32, determine the general term, Tₙ, of the quadratic "
          "pattern.", 5, [
        ("a, in Tₙ = an² + bn + c", 2, 1, EXACT, "28 ; 29 ; 32: first differences 1 ; 3 ; 5 ; 7, second difference 2 ✓; 2a = 2, a = 1 ✓"),
        ("b, in Tₙ = an² + bn + c", 1, -2, EXACT, "3a + b = 1; 3(1) + b = 1; b = −2 ✓"),
        ("c, in Tₙ = an² + bn + c", 2, 29, EXACT, "9a + 3b + c = 32: T₃ = 1(3)² − 2(3) + c = 32 ✓ (method to calculate c; OR a + b + c = T₁: "
                                                  "1 − 2 + c = 28); c = 29 ✓. Tₙ = n² − 2n + 29")],
        ["Work back from T₃ = 32 with the first differences to find T₁ and T₂.", "In Tₙ = an² + bn + c: 2a is the second difference, 3a + b the "
                                                                              "first first difference."])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 5-6 ----
q3 = [
    num("3.1", "Write down the radius of the 3rd circle.", 1.5, EXACT, "cm",
        ["Each circle passes through the centre of the one before and touches it: its diameter is the radius before.",
         "So each radius is half the one before."], marks=2),
    steps("3.2", "Calculate the sum of the areas of the first 10 circles.", 4, [
        ("First term a = kπ (the area of the first circle): k", 1, 36, EXACT, "36π ; 9π ; 9/4 π ; …: a = 36π ✓"),
        ("Common ratio, r", 1, 0.25, EXACT, "r = 1/4 ✓"),
        ("Sum of the areas (cm²)", 2, 150.80, DP2, "S₁₀ = 36π((1/4)¹⁰ − 1)/(1/4 − 1) ✓ (substitution); S₁₀ = 150,80 ✓")],
        ["The areas πr² form a geometric sequence: find its first term and ratio.", "Use Sₙ = a(rⁿ − 1)/(r − 1) with n = 10."]),
    steps("3.3", "Which circle has a diameter of 3/128 cm?", 4, [
        ("Number of the circle, n", 4, 10, EXACT, "6 ; 3 ; 3/2 …: radius = ½(3/128) = 3/256 ✓; 3/256 = 6(1/2)ⁿ⁻¹ ✓ (equating to the radius general "
                                                  "term); 1/512 = (1/2)ⁿ⁻¹; (1/2)⁹ = (1/2)ⁿ⁻¹ ✓ (simplification) or n − 1 = log₁⁄₂(1/512); n − 1 = 9; "
                                                  "n = 10 ✓ (answer). OR diameters 12 ; 6 ; 3 ; …: 12(1/2)ⁿ⁻¹ ✓; 3/128 = 12(1/2)ⁿ⁻¹ ✓ (equating the "
                                                  "general term of the diameter to 3/128); 1/512 = (1/2)ⁿ⁻¹ ✓ (simplification); n = 10 ✓")],
        ["Work with radii (6 ; 3 ; 3/2 ; …) or diameters (12 ; 6 ; 3 ; …), but not both.",
         "Set the general term equal to the size you were given, and write both sides as powers of 1/2."])]

# ---- QUESTION 4, the question paper page 4 and the memo page 7 ----
q4 = [
    steps("4.1", "Calculate the value of a.", 2, [
        ("a", 2, 0.67, DP2, "−5/9 = a² − 1 ✓ (substitution); a² = 4/9; a = 2/3 ✓")],
        ["B is on f, so its coordinates satisfy f(x) = aˣ − 1.", "Substitute x = 2 and y = −5/9; remember a > 0."]),
    mcq("4.2", "Write down the range of f." + ANS, ['y < −1', 'y > −1', 'y ≥ −1', 'x > −1'], 1,
        ["aˣ is always positive.", "So which values can aˣ − 1 take?"]),
    draw("4.3", "Sketch the graph of f. Clearly show the intercepts with the axes and asymptotes, if any.", 3, [
        ["Intercept with the axes: (0 ; 0)", 1], ["Asymptote y = −1", 1], ["Decreasing shape", 1]],
        ["With 0 < a < 1, aˣ gets smaller as x gets bigger.", "Find f(0), and the horizontal asymptote from the − 1."],
        memo="The memo's sketch: a decreasing curve from the top left, through (0 ; 0) and B, levelling off above the dotted asymptote y = −1 "
             "on the right."),
    steps("4.4", "It is further given that C is a point on f at y = 19/8.\nDetermine the coordinates of C′, the image of C, when C is reflected "
          "about the line y = x.", 3, [
        ("x-coordinate of C", 2, -3, EXACT, "19/8 = (2/3)ˣ − 1 ✓ (substitution); 27/8 = (2/3)ˣ; (3/2)³ = (3/2)⁻ˣ; x = −3 ✓ (answer); C(−3 ; 19/8)"),
        ("x-coordinate of C′", 1, 2.375, DP2, "C′(19/8 ; −3) ✓ (answer)")],
        ["Put y = 19/8 into f and write both sides as powers of the same base.", "Reflecting about y = x swaps the coordinates."])]

# ---- QUESTION 5, the question paper page 5 and the memo page 8 ----
F5 = ("Axes with origin O. The hyperbola f has a dotted vertical asymptote that meets the x-axis at 1, and a dotted horizontal asymptote "
      "below the x-axis. Its left branch comes in from the left just above the horizontal asymptote, cuts the x-axis just left of O and "
      "the y-axis at 1, and climbs steeply beside the vertical asymptote. Its right branch rises from far below next to the vertical "
      "asymptote and levels off just below the horizontal asymptote. The straight line g rises from bottom left to top right through the "
      "point where the asymptotes cross.")
q5 = [
    num("5.1", "Write down the value of p.", -1, EXACT, "",
        ["The domain leaves out x = 1: that is the vertical asymptote.", "The vertical asymptote of a/(x + p) + q is x = −p."]),
    steps("5.2", "Determine the equation of the horizontal asymptote of f.", 2, [
        ("The horizontal asymptote y = q: q", 2, -2, EXACT, "y = x − 3; y = 1 − 3 ✓ (substitution); y = −2 ✓ (answer)")],
        ["A line of symmetry passes through the point where the asymptotes cross.", "Put the vertical asymptote's x-value into g."]),
    steps("5.3", "Calculate the value of a.", 2, [
        ("a", 2, -3, EXACT, "1 = a/(0 − 1) − 2 ✓ (substitute (0 ; 1)); 3 = a/(−1); a = −3 ✓ (answer)")],
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
    steps("6.1", "Calculate the coordinates of B, the turning point of f.", 3, [
        ("x-coordinate of B", 2, 2, EXACT, "x = −4/(2(−1)) ✓ (method for x; OR f′(x) = −2x + 4 = 0) = 2 ✓ (value of x)"),
        ("y-coordinate of B", 1, 9, EXACT, "y = −(2)² + 4(2) + 5 = 9 ✓ (value for y); B(2 ; 9)")],
        ["The turning point is at x = −b/(2a), or where f′(x) = 0.", "Substitute that x into f for the y-value."]),
    mcq("6.2", "Show that the equation of the line through A and C is given by g(x) = 2x + 2." + WORK, [
        'x² − 4x − 5 = 0\n(x + 5)(x − 1) = 0\nx = −5 or x = 1, so A(−1 ; 0)\nm = {8 − 0}/{3 + 1} = 2\ny − 0 = 2(x + 1)\ny = 2x + 2',
        'x² − 4x − 5 = 0\n(x − 5)(x + 1) = 0\nx = 5 or x = −1, so A(−1 ; 0)\nm = {8 − 0}/{3 + 1} = 2\ny − 0 = 2(x + 1)\ny = 2x + 2',
        'x² − 4x − 5 = 0\n(x − 5)(x + 1) = 0\nx = 5 or x = −1, so A(−1 ; 0)\nm = {3 + 1}/{8 − 0} = {1}/{2}\ny − 0 = 2(x + 1)\ny = 2x + 2',
        'x² − 4x − 5 = 0\n(x − 5)(x + 1) = 0\nx = 5 or x = −1, so A(−1 ; 0)\nm = {8 − 0}/{3 + 1} = 2\ny − 0 = 2(x − 1)\ny = 2x + 2'], 1,
        ["A is an x-intercept of f: solve f(x) = 0.", "Find the gradient through A and C, then substitute a point into y − y₁ = m(x − x₁)."], marks=3),
    steps("6.3", "Calculate the maximum length of EH for f > g.", 4, [
        ("x-value at which EH is longest", 3, 1, EXACT, "EH = −x² + 4x + 5 − (2x + 2) ✓ (difference); EH = −x² + 2x + 3 ✓; max EH at −2x + 2 = 0 "
                                                       "(OR x = −b/(2a) = −(2)/(2(−1))); x = 1 ✓ (x-value)"),
        ("Maximum length of EH", 1, 4, EXACT, "Max length of EH = −(1)² + 2(1) + 3 = 4 ✓ (length)")],
        ["EH = f(x) − g(x) at the same x.", "That difference is a parabola: find its maximum."]),
    steps("6.4", "Given: k(x) = f(x + m) = −x² − 2mx − m² + 4x + 4m + 5\nDetermine the value of m such that g is a tangent to k.", 5, [
        ("m", 5, -2, EXACT, "k′(x) = −2x − 2m + 4 ✓; k′(x) = 2 ✓; −2x − 2m + 4 = 2; x = 1 − m ✓; k(1 − m) = g(1 − m): −(1 − m)² − 2m(1 − m) − m² + "
                            "4(1 − m) + 4m + 5 = 2(1 − m) + 2 ✓ (substitution); −2m − 4 = 0; m = −2 ✓ (answer). OR −x² − 2mx − m² + 4x + 4m + 5 = "
                            "2x + 2 ✓ (equating); 0 = x² + (2m − 2)x + m² − 4m − 3 ✓ (simplification); Δ = (2m − 2)² − 4(1)(m² − 4m − 3) ✓ "
                            "(substitution into Δ); Δ = 8m + 16 = 0 ✓; m = −2 ✓. OR f′(x) = −2x + 4 = 2 ✓; x = 1 ✓; f(1) = 8 ✓ (y-value); "
                            "g passes through (3 ; 8), so translate 2 units to the right ✓; m = −2 ✓")],
        ["g is a tangent where k′(x) equals the gradient of g.", "The point of contact lies on both k and g (or: the equation k(x) = g(x) has "
                                                                "exactly one root)."])]

# ---- QUESTION 7, the question paper page 7 and the memo pages 11-13 ----
q71 = [
    steps("7.1", "Mary's grandparents deposited R5 000 into a savings account on the day that she was born. The account pays interest at a rate "
          "of 6,8% p.a., compounded quarterly. Calculate the accumulated amount in this account on Mary's 16th birthday.", 3, [
        ("Number of compounding periods, n", 1, 64, EXACT, "i = 6,8/400, n = 64 ✓ (i, n)"),
        ("Accumulated amount on Mary's 16th birthday (R)", 2, 14706.56, CENT, "A = P(1 + i)ⁿ; A = 5 000(1 + 6,8/400)⁶⁴ ✓ (substitution into the "
                                                                             "correct formula) = R14 706,56 ✓ (answer)")],
        ["Compounded quarterly: divide the yearly rate by 4 and count the quarters.", "A = P(1 + i)ⁿ."])]
q72 = [
    steps("7.2", "After 4 years, the value of a printer was half of its original value. Determine the rate at which the value of the printer "
          "depreciated over this period, if depreciation was calculated according to a straight-line method.", 2, [
        ("Rate of depreciation (% per annum)", 2, 12.5, EXACT, "A = P(1 − in); ½P = P(1 − 4i) ✓ (substitution into the correct formula); "
                                                               "½ = 1 − 4i; i = 1/8; r = 12,5% ✓ (answer). OR r = 50%/4 ✓ (method) = 12,5% ✓")],
        ["Straight-line depreciation: A = P(1 − in).", "After 4 years, A is half of P."])]
q73 = [
    steps("7.3.1", "Calculate the total interest that he will pay over the 5 years.", 2, [
        ("Total amount paid over the 5 years (R)", 1, 138058.80, CENT, "Already paid: 2 300,98 × 60 = R138 058,80 ✓ (amount already paid)"),
        ("Total interest (R)", 1, 38058.80, CENT, "138 058,80 − 100 000 = R38 058,80 ✓ (interest)")],
        ["Add up all the instalments he pays in 5 years.", "The interest is what he pays above the amount he borrowed."]),
    steps("7.3.2", "Tshepo paid R22 300,98 (his monthly instalment and an additional R20 000) on 1 March 2024 into the loan account. He continues "
          "to pay the original monthly instalment thereafter. How many months earlier will Tshepo repay the loan?", 7, [
        ("Balance after the payment on 1 March 2024, before the extra R20 000 (R)", 4, 67804.94, 0.3,
         "Balance after 2 years: P = x[1 − (1 + i)⁻ⁿ]/i; n = 36 ✓; i = 13,5/1200 ✓; P = 2 300,98[1 − (1 + 13,5/1200)⁻³⁶]/(13,5/1200) ✓ "
         "(substitution into the correct formula) = R67 804,94 ✓ (answer). OR A = 100 000(1 + 13,5/1200)²⁴ = R130 799,12; F = 2 300,98[(1 + "
         "13,5/1200)²⁴ − 1]/(13,5/1200) = R62 993,92 (n = 24 ✓, i ✓, substitution into both correct formulae ✓); balance outstanding = A − F = "
         "R67 805,20 ✓"),
        ("Balance after the extra R20 000 is paid (R)", 1, 47804.94, 0.3, "R67 804,94 − R20 000 = R47 804,94 ✓ (answer) (OR R67 805,20 − R20 000 "
                                                                         "= R47 805,20)"),
        ("Number of instalments still needed after 1 March 2024, n", 1, 23.80, 0.035,
         "47 804,94 = 2 300,98[1 − (1 + 13,5/1200)⁻ⁿ]/(13,5/1200) ✓ (substitution into the correct formula); 0,766 = (1,01125)⁻ⁿ; "
         "log₁,₀₁₁₂₅ 0,766 = −n; n = 23,83 (OR with R47 805,20: n = 23,80)"),
        ("How many months earlier the loan is repaid", 1, 12, EXACT,
         "∴ 12 months earlier ✓ (answer in months). OR 100 000 = 2 300,98[1 − (1 + 13,5/1200)⁻ⁿ]/(13,5/1200) + 20 000(1 + 13,5/1200)⁻²⁴ (i ✓, "
         "n = 24 ✓, = 100 000 ✓, substitution into the correct P formula ✓ and the correct A formula ✓); 84 709,38 = 2 300,98[1 − (809/800)⁻ⁿ]/"
         "(0,135/12) ✓ (simplification); (809/800)⁻ⁿ = 0,5858; n = 47,80 months after starting payments; ∴ 12 months earlier ✓")],
        ["Find the balance just after the payment on 1 March 2024: the present value of the instalments still to come.",
         "Take off the extra R20 000, then find how many instalments repay what is left."])]

# ---- QUESTION 8, the question paper page 7 and the memo pages 14-15 ----
q81 = [
    steps("8.1.1", "d/dx [3x − 5x²]", 2, [
        ("The derivative: its constant term", 1, 3, EXACT, "= 3 − 10x: 3 ✓"),
        ("The derivative: the coefficient of x", 1, -10, EXACT, "− 10x ✓")],
        ["Differentiate each term on its own.", "The derivative of axⁿ is naxⁿ⁻¹."]),
    steps("8.1.2", "g′(x) if g(x) = 2/x² − ∛(x⁷)", 4, [
        ("g′(x): the coefficient of x⁻³", 2, -4, EXACT, "g(x) = 2x⁻² − x⁷⁄³: 2x⁻² ✓; g′(x) = −4x⁻³ − (7/3)x⁴⁄³: −4x⁻³ ✓"),
        ("g′(x): the coefficient of x⁴⁄³", 2, -2.33, DP2, "−x⁷⁄³ ✓; −(7/3)x⁴⁄³ ✓")],
        ["Write each term as a power of x first: 1/x² = x⁻², and a cube root is the power 1/3.", "Then use the power rule on each term."])]
q82 = [
    steps("8.2", "Determine the equation of the tangent to f(x) = x³ − 4x² + 2x + 3 at x = 2.", 3, [
        ("Gradient of the tangent, m", 1, -2, EXACT, "f′(x) = 3x² − 8x + 2; m = f′(2) = 3(2)² − 8(2) + 2; m = −2 ✓"),
        ("y-coordinate of the point of contact", 1, -1, EXACT, "y = f(2) = (2)³ − 4(2)² + 2(2) + 3; y = −1 ✓"),
        ("y-intercept of the tangent, c", 1, 3, EXACT, "y + 1 = −2(x − 2); y = −2x + 3 ✓ (answer)")],
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
    steps("9.2", "Write down the x-intercepts of f′, the derivative of f.", 2, [
        ("Smaller x-intercept of f′", 1, 1, EXACT, "(1 ; 0): x = 1 ✓"),
        ("Larger x-intercept of f′", 1, 2.5, EXACT, "(5/2 ; 0): x = 5/2 ✓")],
        ["At a turning point the gradient is zero.", "Where on the graph is f′(x) = 0? Read those x-values."]),
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
    steps("10.1", "Calculate the maximum speed that the cyclist reached on this ride.", 3, [
        ("Time at the maximum speed, t", 2, 3, EXACT, "−6t + 18 = 0 ✓ (= 0); 18 = 6t; 3 = t ✓ (value of t)"),
        ("Maximum speed (km/h)", 1, 27, EXACT, "s′(3) = −3(3)² + 18(3) = 27 ✓ (answer)")],
        ["The speed is greatest where its own derivative is zero.", "Find t from s″(t) = 0, then substitute it into s′(t)."]),
    steps("10.2", "Calculate the distance between town P and town T.", 5, [
        ("Time when the cyclist stops, t", 2, 6, EXACT, "−3t² + 18t = 0; −3t(t − 6) = 0 ✓ (factors); t = 0 or t = 6 ✓ (values)"),
        ("Distance between town P and town T (km)", 3, 108, EXACT, "s(t) = at³ + bt²; s′(t) = 3at² + 2bt; 3a = −3 and 2b = 18: a = −1, b = 9 ✓ "
                                                                  "(a and b); s(t) = −1t³ + 9t²; s(6) = −(6)³ + 9(6)² ✓ (substitution); "
                                                                  "s(6) = 108 ✓ (answer)")],
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
    steps("11.2", "Calculate the probability that a learner, chosen at random, will sit for examinations in at least TWO of the subjects.", 2, [
        ("Learners who sit for at least two subjects", 1, 14, EXACT, "4 + 2 + 5 + 3 = 14 ✓ ((4 + 2 + 5 + 3) or 14 in the numerator)"),
        ("Probability", 1, 0.35, EXACT, "P(at least two subjects) = 14/40 ✓ (40 in the denominator) = 7/20 = 0,35")],
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
    num("12.1", "Determine how many different codes can be formed if letters and digits may be repeated.", 67600, EXACT, "",
        ["Count the choices for each of the four places.", "Letters and digits may repeat: multiply the choices."], marks=2),
    steps("12.2", "Determine how many different codes can be formed if:\n• The letters D, F, I, Q, U and V may NOT be used\n• The code may NOT "
          "start with a W or a Z\n• Letters or digits may NOT be repeated\n• The code ends with an odd digit", 4, [
        ("Choices for the first character (a letter)", 1, 18, EXACT, "18 ✓ (26 letters less D, F, I, Q, U, V, W and Z)"),
        ("Choices for the third character (a letter)", 1, 19, EXACT, "19 ✓ (W and Z may be used, the first letter may not be repeated)"),
        ("Choices for the last character (a digit)", 1, 5, EXACT, "5 ✓ (an odd digit)"),
        ("Number of different codes", 1, 15390, EXACT, "Given that it's multiplication: 18 × 9 × 19 × 5 = 15 390, the 9 ✓ (the second character: the "
                                                       "last digit may not be repeated)")],
        ["Fill the most restricted places first: the last digit and the first letter.", "A letter or digit used once cannot be used again."]),
    steps("12.3", "The company wishes to increase the number of 4-character codes formed in QUESTION 12.2 by allowing the letters D, F, I, Q, U "
          "and V to be used. Calculate the percentage increase in the number of different codes that can now be formed.", 2, [
        ("Number of codes with all the letters allowed", 1, 27000, EXACT, "24 × 9 × 25 × 5 = 27 000 ✓"),
        ("Percentage increase (%)", 1, 75.44, DP2, "(27 000 − 15 390)/15 390 × 100 = 75,44% ✓ (answer)")],
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

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": "1.1.3", "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): 1.1.3, 1.3, 2.1.2, 4.2, 5.4, 5.5, 6.2, 8.3.1, 8.3.2, "
                                                   "8.3.3, 9.1, 9.3, 9.4, 11.3 ask for written working or an answer a word marker cannot read (an "
                                                   "inequality, an interval, a range, a set of values, a sigma equation, a square-root equation, a "
                                                   "two-move transformation, a proof); each is played as four options, the memo's answer or working "
                                                   "and three built from common errors, and keeps its marks (40 marks in all)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 12), hand-transcribed from a SCANNED question paper (no "
                                                           "text layer) and the memo's page images (its text layer garbles fractions and powers); "
                                                           "no API call."},
        {"n": "1.1.2", "kind": "no_fit", "detail": "Calculations play as steps, each the number the memo's method produces with its method marks "
                                                   "riding on it. Where the memo ticks the method once for two answers, the ticks are shared out: "
                                                   "1.1.2 two marks a solution; 1.1.4 the law, factor and both 2ˣ ticks ride on 2ˣ = 8; 1.2's five "
                                                   "ticks over its four values as 2, 1, 1, 1; 10.2's 'a and b' tick rides on the distance; 12.2's "
                                                   "'9' tick (the second character) rides on the final count 15 390."},
        {"n": "2.2.2", "kind": "no_fit", "detail": "Expression answers are decomposed into the numbers that fix them, because the strict term ignores "
                                                   "signs: 2.2.2 Tₙ = n² − 2n + 29 as a, b and c; 5.2 the asymptote y = −2 as q; 8.1.1 and 8.1.2 the "
                                                   "coefficients (the labels name the powers x, x⁻³ and x⁴⁄³, a hint the paper does not give); 8.2 the "
                                                   "tangent as m, the point's y and c; 4.4 C′(19/8 ; −3) as C's x (−3, the substitution and answer "
                                                   "ticks) and C′'s x (19/8 = 2,375); C′'s y is C's x and is not asked twice; 9.2 the x-intercepts of "
                                                   "f′ as x-values (their y is 0)."},
        {"n": "3.2", "kind": "no_fit", "detail": "The first term a = 36π is asked as k in a = kπ (36), so the keypad needs no π; the sum is keyed at "
                                                 "150,80 ± 0,006 (exact 150,7963)."},
        {"n": "3.3", "kind": "no_fit", "detail": "One step (n = 10, 4 marks): the memo's two methods tick different first values (the radius 3/256 "
                                                 "or the diameter's general term 12(1/2)ⁿ⁻¹), so no intermediate number is keyed."},
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
        {"n": "7.3.2", "kind": "memo_issue", "detail": "The memo's first method rounds (1,01125)⁻ⁿ to 0,766 and prints n = 23,83; unrounded it is "
                                                       "23,797, and the memo's second method prints n = 23,80. The step accepts both (23,80 ± "
                                                       "0,035); the balances accept both methods' values (R67 804,94 / R67 805,20 and R47 804,94 / "
                                                       "R47 805,20, ± R0,30)."},
        {"n": "7.3.2", "kind": "low_confidence", "detail": "Steps follow the memo's first method (the balance after 1 March 2024, less R20 000, then "
                                                           "n); its third method (one equation from 1 March 2022, n = 47,80 months after the "
                                                           "payments start) reaches '12 months earlier' but not the step values, and is listed in "
                                                           "the last step's memo."},
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
assert sum(i["marks"] for m in missions for i in m["items"]) == 150
for m in missions:
    for i in m["items"]:
        assert len(i["clues"]) == 2, i["n"]
        if i["t"] == "mcq":
            o = i["opts"]
            assert len(o) == 4 and 0 <= i["a"] < 4, i["n"]
            assert len({x.count("\n") for x in o}) == 1, (i["n"], "options differ in line count")
            assert len({sum(ln.rstrip().endswith("]") for ln in x.split("\n")) for x in o}) == 1, (i["n"], "options differ in [reasons]")
            assert i["q"].endswith(ANS) or i["q"].endswith(WORK), i["n"]
at = [i["a"] for m in missions for i in m["items"] if i["t"] == "mcq"]
assert len(set(at)) == 4, at

out = Path(__file__).parent / "out" / "math-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the memo's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 12 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    print(m["id"], "parts:", len(m["items"]), "marks:", sum(i["marks"] for i in m["items"]))
print("total:", sum(i["marks"] for m in missions for i in m["items"]), "| MCQ answers (0-based):", at)
