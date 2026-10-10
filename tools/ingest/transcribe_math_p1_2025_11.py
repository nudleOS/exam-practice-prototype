"""Mathematics P1 Nov 2025, the whole paper (Questions 1 to 11), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's working are
the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the transcription is the source,
kept in git (out/ is not). The question paper is a SCAN (no text layer): read from its page images (1,5x, formulas at 2,5-3x);
the memo has a text layer whose fractions and exponents garble, so it was read from its page images too.

  python tools/ingest/transcribe_math_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P1 Nov 2025 Eng.pdf" "<...>/Mathematics P1 Nov 2025 MG Afr & Eng.pdf" --id math-p1-2025-11 --from-json

How the memo's shapes map (Mathematics: the phone has a number keypad, multiple choice, short text and self-checked drawings,
no algebra input):
  a NUMBER (a solution, a term, a sum, n, an amount, a probability, a coordinate, a gradient) -> steps, each step ONE number the
  memo's method produces, its method marks riding on it; two solutions -> "Smaller solution, x" / "Larger solution, x"; a value
  that does not terminate is keyed at the paper's TWO decimals (instruction 6) with a tolerance of 0,006 (half a unit of the
  second decimal plus a hair), so 0,23, 0,233 and 7/30 = 0,2333 all pass and 0,24 does not; money to the cent: 0,011 (a cent
  either side); an exact value: 0,001. One read-off number -> num.
  An EXPRESSION answer would be a strict term, but the strict term ignores '-', '+', '^', '=' and '/': every sign-only variant
  collides (−12x³ + 2 / 12x³ − 2, 2⁻²¹ / 2²¹, (−p ; 0) / (p ; 0), x ≠ 3 / x = 3), so an expression is decomposed into the
  numbers that fix it (coefficients, a base, an exponent, m and c, a, p and q); the one expression with no sign in it (y = 0)
  stays a strict term.
  An inequality, interval, domain or range -> rubric (the memo's ticks; its "✓✓ answer" is one bullet worth 2, or two bullets
  when the part has other ticks): a strict term cannot tell x < 0 from x > 0, and steps for the critical values would hand out
  the direction marks.
  "Show that / Determine from first principles" -> rubric (the memo's ticked statements in order); "Draw the graph" -> draw
  (self-checked against the memo's criteria); "Describe the transformation" -> term (its phrasings).
Missions: Questions 3, 4, 5, 6, 9 and 10 share a stem and a graph, diagram or table, so each is one mission; Questions 1, 2, 7,
8 and 11 are their numbered groups (1.1, 1.2, 2.1, 2.2 ...).
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the drawings themselves and checked on a contact sheet."""
import json
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad agent_math_p1/figs.py; [page, x0, y0, x1, y1] in points
    "Q4": [5, 77, 177, 500, 370], "Q5": [6, 50, 203, 523, 463], "Q6": [7, 50, 197, 560, 480], "Q9": [9, 110, 167, 517, 399],
    "Q10": [10, 57, 170, 520, 370]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def rub(n, q, marks, bullets, clues, each=None, must=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {})}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


term = lambda n, q, a, clues, marks=1, strict=False, reject=None: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                                  **({"strict": True} if strict else {}), **({"reject": reject} if reject else {})}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


EXACT, DP2, CENT = 0.001, 0.006, 0.011   # an exact value; a value keyed at two decimals; rands and cents

# ---- QUESTION 1, the question paper page 3 and the memo pages 2-4 ----
q11 = [
    steps("1.1.1", "(x + 5)(x − 2) = 0", 2, [
        ("Smaller solution, x", 1, -5, EXACT, "x = −5 ✓"),
        ("Larger solution, x", 1, 2, EXACT, "x = 2 ✓")],
        ["A product is zero only when one of its factors is zero.", "Set each bracket equal to zero."]),
    steps("1.1.2", "5x² + 2 = −9x (correct to TWO decimal places)", 4, [
        ("Smaller solution, x", 2, -1.54, DP2, "5x² + 9x + 2 = 0 ✓ (standard form); x = (−9 ± √41)/10; x = −1,54 ✓"),
        ("Larger solution, x", 2, -0.26, DP2, "x = [−9 ± √(9² − 4(5)(2))]/(2(5)) ✓ (substitution into the correct formula); x = −0,26 ✓")],
        ["Bring every term to one side first: ax² + bx + c = 0.", "It does not factorise neatly: use the quadratic formula."]),
    mcq("1.1.3", "8x² > 2x" + "\n\nChoose the correct answer.", ['0 < x < {1}/{4}', 'x < 0 or x > {1}/{4}', 'x > {1}/{4}', 'x < 0 or x > 4'], 0, ["Move everything to one side and factorise.", "Sketch the parabola: where is it ABOVE the x-axis?"], marks=4),
    steps("1.1.4", "2·2²ˣ − 9·2ˣ + 4 = 0", 4, [
        ("Smaller solution, x", 2, -1, EXACT, "(2·2ˣ − 1)(2ˣ − 4) = 0 ✓ (factors; OR let k = 2ˣ: 2k² − 9k + 4 = 0, (2k − 1)(k − 4) = 0); "
                                             "2ˣ = 1/2 = 2⁻¹; x = −1 ✓"),
        ("Larger solution, x", 2, 2, EXACT, "2ˣ = 1/2 or 2ˣ = 4 ✓ (both equations); 2ˣ = 2²; x = 2 ✓")],
        ["2²ˣ = (2ˣ)²: let k = 2ˣ.", "Solve the quadratic in k, then write each value as a power of 2."]),
    steps("1.1.5", "√(√(1/x) + 2) = 1/√x", 5, [
        ("x", 5, 0.25, EXACT, "Squaring both sides ✓: √(1/x) + 2 = 1/x; isolation of the surd ✓: 1/√x = 1/x − 2; squaring both sides only after "
                              "isolating the surd ✓: 1/x = 1/x² − 4/x + 4; 4x² − 5x + 1 = 0 ✓ (standard form); (4x − 1)(x − 1) = 0; x = 1/4, "
                              "x ≠ 1 ✓ (answer with selection). OR let 1/√x = k: √(k + 2) = k ✓ (equation); k + 2 = k² ✓ (squaring); "
                              "k² − k − 2 = 0 ✓ (standard form); k = 2 or k ≠ −1; 1/√x = 2 ✓ (substitution); x = 1/4 ✓")],
        ["Square both sides, isolate the root that is left, and square again (or let k = 1/√x).", "Check each solution in the ORIGINAL equation: one fails."])]
q12 = [
    steps("1.2", "Calculate the values of x and y if:\n• x is the sum of 2 and y\n• Five times the product of x and y, is 6 more than the square of x", 6, [
        ("Solution with the smaller x: x", 2, -0.5, EXACT, "x = y + 2 ✓ (1); 5xy = x² + 6 ✓ (2); … x = −1/2"),
        ("Solution with the smaller x: y", 1, -2.5, EXACT, "5(y + 2)y = (y + 2)² + 6 ✓ (substitution); … y = −5/2"),
        ("Solution with the larger x: x", 2, 3, EXACT, "5y² + 10y = y² + 4y + 4 + 6; 4y² + 6y − 10 = 0; 2y² + 3y − 5 = 0 ✓ (standard form); "
                                                      "(2y + 5)(y − 1) = 0; x = −1/2 or x = 3 ✓ (x-values)"),
        ("Solution with the larger x: y", 1, 1, EXACT, "y = −5/2 or y = 1 ✓ (y-values). OR y = x − 2 ✓; 5xy − 6 = x² ✓; 5x(x − 2) − 6 = x² ✓; "
                                                      "2x² − 5x − 3 = 0 ✓; (2x + 1)(x − 3) = 0, x = −1/2 or x = 3 ✓; y = −5/2 or y = 1 ✓")],
        ["Write the two sentences as two equations: the first is x = y + 2.", "Substitute one into the other to get a quadratic."])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 5-6 ----
q21 = [
    rub("2.1.1", "Show that t = −2", 3, [
        "Equating the ratios: (t − 2)/(t + 10) = (t + 4)/(t − 2)",
        "Cross multiplication: (t − 2)² = (t + 4)(t + 10)",
        "Expansion: t² − 4t + 4 = t² + 14t + 40, so −18t = 36 and t = −2"],
        ["In a geometric series the ratio of consecutive terms is constant.", "Set T₂/T₁ equal to T₃/T₂, then cross-multiply."]),
    steps("2.1.2", "Calculate the value of T₂₅. Write your answer in the form Tₙ = bˣ", 3, [
        ("First term, a", 1, 8, EXACT, "8 ; −4 ; … ✓ (8 and −4)"),
        ("Common ratio, r", 1, -0.5, EXACT, "r = −4/8 = −1/2 ✓"),
        ("T₂₅ as a power of 2: the exponent", 1, -21, EXACT, "T₂₅ = 8(−1/2)²⁴; T₂₅ = (1/2)²¹ or (2)⁻²¹ or (8)⁻⁷ or (128)⁻³ or (2 097 152)⁻¹ ✓ "
                                                             "(answer in exponential form)")],
        ["With t = −2 the series is 8 + (−4) + 2 + …", "T₂₅ = ar²⁴: write 8 and 1/2 as powers of 2."]),
    steps("2.1.3", "Calculate the sum of the infinite series.", 2, [
        ("Sum to infinity", 2, 5.33, DP2, "S∞ = a/(1 − r) = 8/(1 − (−1/2)) ✓ (substitution); S∞ = 16/3 = 5,33 ✓")],
        ["−1 < r < 1, so the series converges.", "S∞ = a/(1 − r)."])]
q22 = [
    num("2.2.1", "Write down the difference between T₆ and T₁₄", 32, EXACT, "",
        ["Each term of 4p − 1 is 4 more than the one before.", "From T₆ to T₁₄ is 8 steps of d."], marks=2),
    steps("2.2.2", "Calculate the value of k.", 5, [
        ("Last term of the sum", 1, 467, EXACT, "T₁₁₇ = 4(117) − 1 = 467 ✓ (last term)"),
        ("k", 4, 21, EXACT, "n = 118 − k ✓ (number of terms); S₁₁₈₋ₖ = (118 − k)/2 [4k − 1 + 467] ✓ (substitution); 26 675 = (118 − k)[2k + 233]; "
                            "2k² − 3k − 819 = 0 ✓ (standard form); (k − 21)(2k + 39) = 0; k = 21, k ≠ −39/2 ✓ (answer with selection). "
                            "OR S₁₁₇ − Sₖ₋₁ = 26 675: S₁₁₇ = 117/2 [2(3) + (116)4] = 27 495; Sₖ₋₁ = 820; 2n² + n − 820 = 0; n = 20 = k − 1; k = 21")],
        ["The sum runs from 4k − 1 up to 4(117) − 1: it has 118 − k terms.", "Sₙ = n/2 (first + last) gives a quadratic in k."])]

# ---- QUESTION 3, the question paper page 4 and the memo page 7 ----
q3 = [
    steps("3.1", "Calculate the depth of the torpedo at the end of the first 5 seconds.", 2, [
        ("Depth at the end of 4 seconds (m)", 1, 135, EXACT, "36 ; 71 ; 104 ; 135 ; 164: first differences 35 ; 33 ; 31 ; 29 ✓, second difference −2"),
        ("Depth at the end of 5 seconds (m)", 1, 164, EXACT, "T₅ = 164 ✓")],
        ["Find the first differences: 35, 33, …", "The second difference is constant: keep the pattern going."]),
    mcq("3.2", "Show that the depth of the torpedo at the end of n seconds was Tₙ = −n² + 38n − 1" + "\n\nChoose the correct working.", ['a = −2 (the second difference)\n3a + b = 35, so b = 41\na + b + c = 36, so c = −3', '2a = −2, so a = −1\na + b = 35, so b = 36\na + b + c = 36, so c = 1', '2a = −2, so a = −1\n3a + b = 35, so b = 38\na + b + c = 36, so c = −1', '2a = 2, so a = 1\n3a + b = 35, so b = 32\na + b + c = 36, so c = 3'], 2, ["Tₙ = an² + bn + c, where 2a is the second difference.", "3a + b is the first first difference; a + b + c is T₁."], marks=3),
    steps("3.3", "Calculate the maximum depth that the torpedo reached.", 3, [
        ("Time of the maximum depth, n (seconds)", 2, 19, EXACT, "n = −38/(2(−1)) ✓ (method; OR Tₙ′ = −2n + 38 = 0) = 19 ✓"),
        ("Maximum depth (m)", 1, 360, EXACT, "T₁₉ = −(19)² + 38(19) − 1 = 360 ✓")],
        ["The maximum of a quadratic is at its turning point.", "n = −b/(2a), then substitute that n into Tₙ."]),
    steps("3.4", "After how many seconds was the torpedo at 104 m below sea level for the second time?", 2, [
        ("Time (seconds)", 2, 35, EXACT, "(n + 3)/2 = 19 ✓ (method); n + 3 = 38; n = 35 ✓. OR −n² + 38n − 1 = 104 ✓; n² − 38n + 105 = 0; "
                                         "(n − 35)(n − 3) = 0; n = 35 ✓")],
        ["The first time was after 3 seconds, and the pattern is symmetric about its maximum.", "Or solve −n² + 38n − 1 = 104."])]

# ---- QUESTION 4, the question paper page 5 and the memo page 8 ----
q4 = [
    num("4.1", "Calculate the value of t", -1, EXACT, "",
        ["(3 ; t) is on f, so t = f(3).", "To what power must 1/3 be raised to give 3?"]),
    steps("4.2", "Write down the coordinates of A.", 1, [
        ("x-coordinate of A (its y-coordinate is 0)", 1, 1, EXACT, "A(1 ; 0) ✓")],
        ["A is on the x-axis, so f(x) = 0 there.", "The log of which number is always 0?"]),
    steps("4.3", "Determine the equation of f⁻¹, the inverse of f, in the form y = …", 2, [
        ("f⁻¹ in the form y = bˣ: the base b", 2, 0.33, DP2, "y = log₁⁄₃ x; x = log₁⁄₃ y ✓ (swopping); y = (1/3)ˣ = 3⁻ˣ ✓")],
        ["Swap x and y, then rewrite the log as a power.", "logₐ y = x means y = aˣ."]),
    term("4.4", "Write down the equation of the asymptote of f⁻¹", ["y = 0", "y=0"],
         ["f⁻¹ is an exponential graph.", "Which horizontal line does bˣ approach but never reach?"], strict=True),
    draw("4.5", "Draw the graph of f⁻¹ on the set of axes provided in the ANSWER BOOK. Clearly indicate the intercepts with the axes, the "
         "coordinates of ONE other point and the asymptotes.", 3, [
        ["Decreasing exponential shape with the asymptote y = 0", 1], ["y-intercept (0 ; 1)", 1], ["Any other point on the graph, e.g. (−1 ; 3)", 1]],
        ["f⁻¹ is the reflection of f in the line y = x.", "Every graph y = bˣ passes through (0 ; 1)."]),
    rub("4.6", "The graph of h is obtained when f⁻¹ is translated 5 units to the right. Determine the y-values of h where x > 4.", 2, [
        "(4 ; 3) is a point on h: 0 < y < 3, or y ∈ (0 ; 3)"],
        ["h(x) = f⁻¹(x − 5): work out h(4).", "h is decreasing and never reaches its asymptote."], each=2)]

# ---- QUESTION 5, the question paper page 6 and the memo pages 9-10 ----
q5 = [
    mcq("5.1", "Write down the domain of g." + "\n\nChoose the correct answer.", ['x ∈ ℝ', 'y ∈ ℝ, y ≠ 8', 'x ∈ ℝ, x ≠ 8', 'x ∈ ℝ, x ≠ 3'], 3, ["g is undefined where its denominator is zero.", "That x-value is its vertical asymptote."], marks=1),
    mcq("5.2", "Write down the range of f." + "\n\nChoose the correct answer.", ['y ≤ 8', 'y ≥ 8', 'x ≤ 3', 'y < 8'], 0, ["f opens downwards, so its turning point is its highest point.", "P is also where g's asymptotes cross."], marks=1),
    mcq("5.3.1", "Determine the values of x for which: g(x) ≤ f(x)" + "\n\nChoose the correct answer.", ['3 ≤ x ≤ 5', 'x < 3 or x ≥ 5', '3 < x ≤ 5', '3 < x < 5'], 2, ["Find where the graph of g is on or below the graph of f.", "Look between g's vertical asymptote and the intersection D."], marks=2),
    mcq("5.3.2", "Determine the values of x for which: f(x) < 6" + "\n\nChoose the correct answer.", ['x < 1 or x > 5', '1 < x < 5', 'x ≤ 1 or x ≥ 5', 'x > 5 only'], 0, ["f is symmetric about x = 3, and f(5) = 6.", "Where is the parabola BELOW the line y = 6?"], marks=2),
    rub("5.4", "Show that the equation of the parabola is f(x) = −½x² + 3x + 7/2", 3, [
        "p and q values: y = a(x − 3)² + 8",
        "Substitution of (5 ; 6): 6 = a(5 − 3)² + 8, so −2 = 4a and a = −½",
        "Simplification: y = −½(x − 3)² + 8 = −½(x² − 6x + 9) + 8 = −½x² + 3x + 7/2"],
        ["Use the turning-point form y = a(x − p)² + q with P.", "D(5 ; 6) is on f: substitute it to find a."]),
    steps("5.5", "Calculate the length of MT.", 6, [
        ("x-coordinate of M", 3, -1, EXACT, "−½x² + 3x + 7/2 = 0: x² − 6x − 7 = 0 ✓ (solve for x); (x − 7)(x + 1) = 0, x = 7 or x = −1 ✓ (x-values); "
                                            "M(−1 ; 0) ✓"),
        ("x-coordinate of T", 2, 3.5, EXACT, "0 = −4/(x − 3) + 8 ✓ (solve for x); −8x + 24 = −4; x = 7/2 ✓; T(7/2 ; 0)"),
        ("Length of MT (units)", 1, 4.5, EXACT, "MT = 7/2 + 1 = 9/2 = 4,5 ✓")],
        ["M: solve f(x) = 0. T: solve g(x) = 0.", "Both points are on the x-axis: subtract their x-coordinates."]),
    steps("5.6", "Determine the equation of the tangent to f at D.", 3, [
        ("Gradient of the tangent, m", 2, -2, EXACT, "f′(x) = −x + 3 ✓; m = f′(5) ✓ = −5 + 3 = −2"),
        ("y-intercept of the tangent, c", 1, 16, EXACT, "6 = −2(5) + c; c = 16; y = −2x + 16 ✓")],
        ["The gradient of the tangent at D is f′ at D's x-value.", "Then put the point D(5 ; 6) into y = mx + c."])]

# ---- QUESTION 6, the question paper page 7 and the memo pages 11-12 ----
q6 = [
    mcq("6.1", "Write down the coordinates of the x-intercept of g in terms of p." + "\n\nChoose the correct answer.", ['(p ; 0)', '(0 ; −p)', '(−p ; 0)', '(0 ; p)'], 2, ["The vertical asymptote of f is x = −p.", "g cuts the x-axis exactly there."], marks=1),
    steps("6.2", "Graph g intersects the horizontal asymptote of graph f at x = 1 and the graph f at x = 3. Graphs f and g also intersect on the "
          "y-axis. Determine the equation of f.", 5, [
        ("Value of p", 3, -2, EXACT, "g(x) = x + c, so c = p; q = 1 + c ✓; f(x) = a/(x + c) + 1 + c ✓; point (0 ; c): c = a/(0 + c) + 1 + c, a = −c; "
                                     "point (3 ; 3 + c): 3 + c = a/(3 + c) + 1 + c ✓; 3 + c = −c/(3 + c) + 1 + c; 9 + 6c + c² = −c + 3 + 4c + c²; "
                                     "3c = −6; c = −2. OR a = 6 + 2c from x = 3, then −1 = (6 + 2c)/c from x = 0: c = −2"),
        ("Value of a", 1, 2, EXACT, "a = 2 ✓"),
        ("Value of q", 1, -1, EXACT, "q = −1 ✓; f(x) = 2/(x − 2) − 1")],
        ["g's x-intercept is on f's vertical asymptote, and g meets y = q at x = 1.", "The intersections (0 ; g(0)) and (3 ; g(3)) both lie on f."]),
    term("6.3", "Describe the transformation that g must undergo to become an axis of symmetry of f that cuts f at two points.", [
        "Translation of 1 unit down", "1 unit down", "1 unit downwards", "One unit down", "Translate 1 unit down", "Translate g 1 unit down",
        "Shift 1 unit down", "Move 1 unit down", "Translation of 1 unit to the right", "1 unit to the right", "1 unit right", "One unit to the right",
        "Translate 1 unit to the right", "Translate g 1 unit to the right", "Shift 1 unit to the right", "Move 1 unit to the right"],
         ["f's axes of symmetry pass through the point where its asymptotes cross, with gradients 1 and −1.",
          "Which one cuts both branches? Compare it with g."], marks=2,
         reject=["1 unit up", "Translation of 1 unit up", "1 unit to the left", "Translation of 1 unit to the left", "1 unit left"])]

# ---- QUESTION 7, the question paper page 8 and the memo pages 13-14 ----
q71 = [
    steps("7.1", "A travel company informs Robert that a holiday to a certain destination costs R40 000 now. The company predicts that the cost of "
          "this holiday will increase by 7,8% per annum. What will this holiday cost in 5 years' time?", 2, [
        ("Cost of the holiday in 5 years' time (R)", 2, 58230.94, CENT, "A = P(1 + i)ⁿ; A = 40 000(1 + 7,8%)⁵ ✓ (substitution into the correct "
                                                                         "formula); A = R58 230,94 ✓")],
        ["The cost grows by 7,8% of each NEW cost: compound growth.", "A = P(1 + i)ⁿ."])]
q72 = [
    steps("7.2", "Sarah opened a savings account that paid interest at a rate of 5,8% p.a., compounded quarterly. She deposited R2 300 into the "
          "account on 1 January 2020 and continued to make deposits of R2 300 at the beginning of each quarter thereafter. She made her last "
          "deposit on 1 October 2025. Calculate the accumulated amount in the account on 1 January 2026.", 4, [
        ("Interest rate per quarter, i (as a decimal)", 1, 0.0145, 0.00005, "i = 0,058/4 ✓"),
        ("Accumulated amount on 1 January 2026 (R)", 3, 66411.60, CENT,
         "F = x[(1 + i)ⁿ − 1]/i: F = 2 300[(1 + 0,058/4)²⁴ − 1]/(0,058/4) ✓ (substitution into the correct formula) × (1 + 0,058/4) ✓ (future value "
         "× (1 + i)¹); F = R66 411,60 ✓. OR F = 2 300[(1 + 0,058/4)²⁵ − 1]/(0,058/4) ✓ − 2 300 ✓ = R66 411,60 ✓")],
        ["Count the deposits: one each quarter from 1 January 2020 to 1 October 2025.", "Deposits at the START of a quarter earn one more quarter "
                                                                                          "of interest by 1 January 2026."])]
q73 = [
    steps("7.3.1", "Rajesh was unable to make the first three payments. He made his first repayment of R10 000 on 30 June 2024. He continued to "
          "make monthly repayments of R10 000 at the end of each month thereafter. How long, in completed months, will it take Rajesh to repay the "
          "loan from the time the loan was granted?", 5, [
        ("Loan balance after the three missed payments (R)", 1, 915386.86, CENT, "A = P(1 + i)ⁿ = 900 000(1 + 0,068/12)³ = R915 386,86 ✓"),
        ("Number of repayments, n", 3, 129.42, DP2, "P = x[1 − (1 + i)⁻ⁿ]/i: 915 386,86 = 10 000[1 − (1 + 0,068/12)⁻ⁿ]/(0,068/12) ✓ (substitution into "
                                                    "the correct formula); (1 + 0,068/12)⁻ⁿ = 0,4812…; −n = log₁,₀₀₅… 0,4812… ✓ (correct use of logs); "
                                                    "n = 129,419… months ✓"),
        ("Months from the time the loan was granted", 1, 133, EXACT, "132,419 months since the loan was granted, so 133 months ✓")],
        ["First grow the loan through the three months with no payment.", "Then the present-value annuity formula with x = R10 000 gives n; "
                                                                           "remember the months before the first repayment."]),
    steps("7.3.2", "Calculate the value of the final payment.", 4, [
        ("Balance after the last full repayment (R)", 3, 4173.55, CENT,
         "P = 10 000[1 − (1 + 0,068/12)^(−0,419…)]/(0,068/12) ✓ (substitution) ✓ (n) = R4 173,55… ✓ (balance). OR A = 915 386,86(1 + 0,068/12)¹²⁹ "
         "= R1 897 482,712 ✓; F = 10 000[(1 + 0,068/12)¹²⁹ − 1]/(0,068/12) = R1 893 309,16 ✓; balance after 129 months = R4 173,552 ✓"),
        ("Final payment (R)", 1, 4197.21, CENT, "Final payment = 4 173,55…(1 + 0,068/12)¹ = R4 197,21 ✓")],
        ["The whole number in your n from 7.3.1 counts the full R10 000 payments; the decimal part is what is left over.",
         "Find the balance after the last full payment, then add one month's interest."])]

# ---- QUESTION 8, the question paper page 8 and the memo page 15 ----
q81 = [
    mcq("8.1", "Determine f′(x) from first principles if it is given that f(x) = −2x + 3." + "\n\nChoose the correct working.", ['f(x + h) = −2x + h + 3\nf′(x) = lim(h→0) {−2x + h + 3 − (−2x + 3)}/{h}\n= lim(h→0) {h}/{h}\n= 1', 'f(x + h) = −2(x + h) + 3\nf′(x) = lim(h→0) {−2(x + h) + 3 − (−2x − 3)}/{h}\n= lim(h→0) {6 − 2h}/{h}\n(no limit)', 'f(x + h) = −2(x + h) + 3\nf′(x) = lim(h→0) {−2(x + h) + 3}/{h}\n= lim(h→0) (−2)\n= −2', 'f(x + h) = −2(x + h) + 3\nf′(x) = lim(h→0) {−2(x + h) + 3 − (−2x + 3)}/{h}\n= lim(h→0) {−2h}/{h}\n= −2'], 3, ["f′(x) = lim (h→0) [f(x + h) − f(x)]/h.", "Write f(x + h) first and simplify before taking the limit."], marks=4)]
q82 = [
    steps("8.2.1", "g′(x) if g(x) = −3x⁴ + 2x", 2, [
        ("g′(x): the coefficient of x³", 1, -12, EXACT, "g′(x) = −12x³ + 2: −12x³ ✓"),
        ("g′(x): the constant term", 1, 2, EXACT, "+ 2 ✓")],
        ["Power rule: the derivative of axⁿ is naxⁿ⁻¹.", "Differentiate each term on its own."]),
    steps("8.2.2", "dy/dx if y = (2x⁴ + 1)/x²", 4, [
        ("dy/dx: the coefficient of x", 2, 4, EXACT, "y = 2x² + x⁻²: 2x² ✓; dy/dx = 4x − 2x⁻³: derivative of the first term ✓"),
        ("dy/dx: the coefficient of x⁻³", 2, -2, EXACT, "x⁻² ✓; derivative of the second term ✓")],
        ["Divide each term of the numerator by x² first.", "1/x² = x⁻²; then use the power rule."])]

# ---- QUESTION 9, the question paper page 9 and the memo pages 16-17 ----
q9 = [
    steps("9.1", "Calculate the coordinates of E.", 4, [
        ("x-coordinate of E", 3, 5, EXACT, "f′(x) = 3x² − 16x + 5 ✓; f′(x) = 0 ✓; (3x − 1)(x − 5) = 0; x = 1/3 or x = 5 ✓ (x-value)"),
        ("y-coordinate of E", 1, -36, EXACT, "E(5 ; −36) ✓ (y-value)")],
        ["At a turning point f′(x) = 0.", "E is the turning point on the right: put its x into f."]),
    mcq("9.2", "For which values of x is f concave down?" + "\n\nChoose the correct answer.", ['f″(x) = 6x − 16 > 0, so x > {8}/{3}', 'f″(x) = 6x − 16 < 0, so x < {8}/{3}', 'f′(x) = 3x² − 16x + 5 < 0, so {1}/{3} < x < 5', 'f″(x) = 6x − 8 < 0, so x < {4}/{3}'], 1, ["Concave down means f″(x) < 0.", "The point of inflection lies halfway between the turning points."], marks=3),
    rub("9.3", "The coordinates of B are (2 ; 0). Use the graph to determine the values of x for which f(x) · f″(x) < 0", 4, [
        "x-intercept of f: (−1 ; 0)",
        "x-intercept of f: (7 ; 0)",
        "First interval: −1 < x < 2",
        "Second interval: 8/3 < x < 7"],
        ["Divide f(x) by (x − 2) to find A and C.", "The product is negative where f and f″ have opposite signs; f″ changes sign at the point of "
                                                    "inflection."]),
    mcq("9.4", "For which values of t will y = −11x + t intersect f at 3 distinct points?" + "\n\nChoose the correct working.", ['f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nx = 4: t = 14; x = {4}/{3}: t = {634}/{27}\n14 ≤ t ≤ {634}/{27}', 'f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nt lies between the two x-values\n{4}/{3} < t < 4', 'f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nx = 4: t = 14; x = {4}/{3}: t = {634}/{27}\nt < 14 or t > {634}/{27}', 'f′(x) = 3x² − 16x + 5 = −11\n(x − 4)(3x − 4) = 0, so x = 4 or x = {4}/{3}\nx = 4: t = 14; x = {4}/{3}: t = {634}/{27}\n14 < t < {634}/{27}'], 3, ["Find where the tangent to f has gradient −11: f′(x) = −11.", "Those two tangents give the boundary values of t; the line lies between them."], marks=6)]

# ---- QUESTION 10, the question paper page 10 and the memo page 18 ----
q10 = [
    mcq("10.1", "Show that the volume of the cylinder is given by V = 25x²/(4π) − x³/(4π)" + "\n\nChoose the correct working.", ['2x + 2h = 50\nh = 25 − x\n2πr = x\nr = {x}/{2π}\nV = πr²h = π({x}/{2π})²(25 − x)\nV = {25x²}/{4π} − {x³}/{4π}', 'x + h = 50\nh = 50 − x\n2πr = x\nr = {x}/{2π}\nV = πr²h\nV = {25x²}/{4π} − {x³}/{4π}', '2x + 2h = 50\nh = 25 − x\n2πr = h\nr = {25 − x}/{2π}\nV = πr²x\nV = {25x²}/{4π} − {x³}/{4π}', '2x + 2h = 50\nh = 25 − x\n2πr = x\nr = {x}/{2π}\nV = 2πrh = x(25 − x)\nV = {25x²}/{4π} − {x³}/{4π}'], 0, ["The side x rolls into the circumference: 2πr = x.", "Use the perimeter to write h in terms of x, then V = πr²h."], marks=3),
    steps("10.2", "Calculate the value of x that will maximise the volume of the cylinder.", 3, [
        ("x (units)", 3, 16.67, DP2, "V′(x) = 50x/(4π) − 3x²/(4π) ✓; V′(x) = 0 ✓; 50x − 3x² = 0; x(50 − 3x) = 0; x ≠ 0 or x = 50/3; x = 50/3 = 16,67 ✓ "
                                     "(answer with selection)")],
        ["At a maximum V′(x) = 0.", "Factor out x: x = 0 gives no cylinder."])]

# ---- QUESTION 11, the question paper page 11 and the memo pages 19-21 ----
q111 = [
    mcq("11.1.1", "The events male and preferring juice are independent. Show that e = 84." + "\n\nChoose the correct working.", ['P(M or J) = P(M) × P(J)\n{36}/{210} = {90}/{210} × {e}/{210}\ne = 84', 'P(M and J) = P(M) × P(J)\n{36}/{210} = {90}/{210} × {e}/{210}\ne = 84', 'P(M and J) = P(M) × P(J)\n{36}/{90} = {90}/{210} × {e}/{210}\ne = 84', 'P(M and J) = P(M) + P(J) − 1\n{36}/{210} = {90}/{210} + {e}/{210} − 1\ne = 84'], 1, ["Independent events: P(A and B) = P(A) × P(B).", "Work out f, the number of males, first."], marks=3),
    steps("11.1.2", "Calculate the probability that a female learner, chosen at random from the group, will like energy drinks.", 3, [
        ("b, the number of females who like energy drinks", 2, 72, EXACT, "d = 210 − 84 = 126 ✓ (d-value); b = 126 − 54 = 72 ✓ (b-value). "
                                                                          "OR c = 120 ✓ (c-value); b = 72 ✓"),
        ("Probability", 1, 0.34, DP2, "P(Female and like energy drink) = b/210 = 72/210 = 12/35 = 0,34 ✓")],
        ["Use e = 84 to complete the table: d, then b.", "Read it as: the learner chosen from the WHOLE group is female AND likes energy drinks."])]
q112 = [
    steps("11.2", "At a kiosk, 120 people buy either a cup of coffee or a bottle of water. The chance of rain on any given day is 75%. The chance of a "
          "person buying a cup of coffee on a rainy day is three times the chance of the person buying coffee on a non-rainy day.\n\nThe probability "
          "of a person buying coffee on any given day is 7/12.\nCalculate the number of cups of coffee that will be sold on a non-rainy day.", 4, [
        ("Probability of a person buying coffee on a non-rainy day", 3, 0.23, DP2, "(3/4)(3x) ✓ + (1/4)x ✓ = 7/12 ✓; 27x + 3x = 7; 30x = 7; x = 7/30"),
        ("Cups of coffee sold on a non-rainy day", 1, 28, EXACT, "(7/30)(120) = 28 cups ✓. OR (75/100)(3x/120) ✓ + (25/100)(x/120) ✓ = 7/12 ✓; "
                                                                 "x = 28 cups of coffee ✓ (OR with x bottles of water: x = 92, so 28 cups)")],
        ["Let x be the chance of buying coffee on a non-rainy day; on a rainy day it is 3x.", "P(coffee) = P(rain)·3x + P(no rain)·x."])]
q113 = [
    num("11.3.1", "Calculate the total number of possible ways in which the 8 runners can finish the race if Bongi finishes in a position "
        "immediately after Andrew.", 5040, EXACT, "",
        ["Join Andrew and Bongi into one unit in a fixed order.", "Then arrange the units."], marks=2),
    steps("11.3.2", "Calculate the probability that TWO OR MORE runners finish the race after Andrew and before Bongi.", 4, [
        ("Finishing orders with Andrew ahead of Bongi and two or more runners between them", 2, 10800, EXACT,
         "A × 6 × 5 × B × 4 × 3 × 2 × 1 and the others: 5 × 6! + 4 × 6! + 3 × 6! + 2 × 6! + 1 × 6! = 6!(5 + 4 + 3 + 2 + 1) = 6!(15) ✓✓"),
        ("Probability", 2, 0.27, DP2, "P = 6!(15)/8! ✓ (8! in the denominator) = 15/56 ✓ = 0,27. OR [8! − (7!·2 + 2·6·6!)]/(8!·2): 8! in numerator "
                                      "and denominator ✓, (7!·2 + 2·6·6!) ✓✓, 15/56 ✓")],
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

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": "1.1.3", "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): 1.1.3, 3.2, 5.1, 5.2, 5.3.1, 5.3.2, 6.1, 8.1, 9.2, 9.4, 10.1, 11.1.1 ask for written working or an answer a word marker cannot read (an inequality, an interval, a coordinate, a proof); each is played as four options, the memo's answer or working and three built from common errors, and keeps its marks."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from a SCANNED question paper (no "
                                                           "text layer) and the memo's page images (its text layer garbles fractions and powers); "
                                                           "no API call."},
        {"n": "1.1.2", "kind": "no_fit", "detail": "Calculations play as steps, each the number the memo's method produces with its method marks "
                                                   "riding on it. Where the memo ticks the method once for two answers (1.1.2, 1.1.4, 1.2, 5.5, 9.1), "
                                                   "the method ticks are shared out over the numbers: 1.1.2 and 1.1.4 two marks a solution; 1.2's "
                                                   "six ticks over its four values as 2, 1, 2, 1."},
        {"n": "2.1.2", "kind": "no_fit", "detail": "Expression answers are decomposed into the numbers that fix them, because the strict term ignores "
                                                   "signs (2⁻²¹ and 2²¹ would collide): 2.1.2 T₂₅ as the exponent of 2 (−21; the memo also accepts "
                                                   "(1/2)²¹, 8⁻⁷, 128⁻³); 4.3 the base of y = bˣ (1/3 at 0,33 ± 0,006); 5.6 the tangent's m and c; 6.2 "
                                                   "f's p, a and q; 8.2.1 and 8.2.2 the coefficients (the labels name the powers x³ and x⁻³, a hint the "
                                                   "paper does not give); 4.2 the x-coordinate of A only (its y is 0 by definition)."},
        {"n": "1.1.3", "kind": "no_fit", "detail": "Inequalities, intervals, a domain, a range and a point in terms of p play as rubrics marked against "
                                                   "the memo's ticks (1.1.3, 4.6, 5.1, 5.2, 5.3.1, 5.3.2, 6.1, 9.2, 9.3, 9.4: 26 marks): a strict term "
                                                   "cannot tell x < 0 from x > 0 (or (−p ; 0) from (p ; 0)), and steps for the critical values would "
                                                   "hand out the direction marks. A memo '✓✓ answer' beside other ticks is two bullets (first half, "
                                                   "second half)."},
        {"n": "2.1.1", "kind": "no_fit", "detail": "Proofs play as rubrics of the memo's ticked statements: 2.1.1, 3.2, 5.4, 8.1 (first principles, "
                                                   "both memo methods as OR groups), 10.1, 11.1.1 (19 marks)."},
        {"n": "4.5", "kind": "no_fit", "detail": "The sketch of f⁻¹ is drawn on paper and self-checked against the memo's three criteria."},
        {"n": "4.4", "kind": "no_fit", "detail": "The asymptote's equation is a strict term (y = 0): it has no sign to lose, and x = 0 stays wrong."},
        {"n": "6.3", "kind": "no_fit", "detail": "The transformation is a term listing the memo's two answers (1 unit down OR 1 unit to the right) in "
                                                 "common phrasings, with 'up' and 'left' rejected; another wording is marked wrong."},
        {"n": "11.1.2", "kind": "memo_issue", "detail": "The question asks for 'the probability that a female learner, chosen at random from the "
                                                        "group, will like energy drinks', which reads as P(energy drinks | female) = 72/120 = 0,6; "
                                                        "the memo marks P(female and energy drinks) = 72/210 = 12/35 = 0,34. Played as the memo "
                                                        "(0,34); 0,6 is marked wrong. A teacher should confirm."},
        {"n": "2.2.1", "kind": "memo_issue", "detail": "'The difference between T₆ and T₁₄': the memo gives T₁₄ − T₆ = 32 only; −32 (T₆ − T₁₄) is "
                                                       "marked wrong."},
    ],
}
out = Path(__file__).parent / "out" / "math-p1-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the memo's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    print(m["id"], "parts:", len(m["items"]), "marks:", sum(i["marks"] for i in m["items"]), "/", m["marks"])
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
