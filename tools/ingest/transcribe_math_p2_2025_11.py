"""Mathematics P2 Nov 2025, the whole paper (Questions 1 to 11: statistics, analytical geometry, trigonometry, Euclidean geometry),
hand-transcribed into the catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any
ingested paper. Stems, options, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and
figure captions are ours. No API call: the transcription is the source, kept in git (out/ is not). The question paper and the
answer book are SCANS (no text layer) and the memo's text layer garbles fractions and diagrams: everything was read from the page
IMAGES (diagrams zoomed in).

  python tools/ingest/transcribe_math_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P2 Nov 2025 Eng.pdf" "<...>/Mathematics P2 Nov 2025 MG Afr & Eng.pdf" --id math-p2-2025-11 --from-json

How the memo's shapes map (Mathematics: there is no algebra input, a learner answers with the keypad, a choice, a short text or a
drawing self-checked on paper):
  a number the memo calculates (a, b, a prediction, σ, a gradient, θ, a length, a coordinate, an angle, a ratio) -> steps, each
  step ONE number the method produces, its formula and substitution marks riding on that number; tolerances cover the memo's
  rounding (two decimals, its answers are 2-decimal roundings of the exact value) plus a hair for floating point; a fraction is
  typed as a decimal (4/3 -> 1,33), a coordinate is two steps (x, y); one read-off number -> num;
  an equation of a line or circle -> its numbers as steps (m and c; a and r²): the strict term compares letters and digits only,
  so "y = ½x − 4" and "y = ½x + 4" would be the same answer;
  a simplified surd (8√5) -> QR² and the whole number a of a√b;
  an expression in k, a simplification and the general solution's working -> rubric (the memo's ticks, one bullet each) when the
  memo marks method; a one-step expression, an equation of a graph, a range and a solution INTERVAL (whose open/closed ends
  matter) -> mcq of the plausible forms;
  "Show that", "Prove" and the geometry proofs -> rubric: the memo's statements with their reasons exactly as ticked (S, R, S/R
  each a bullet), "OR — " starting an alternative proof; "Calculate, with reasons" an angle or a ratio -> steps (the reason marks
  ride on the number, as working marks do);
  "Draw a histogram / the graph of g" -> draw with the memo's criteria (self-checked, flagged no_fit).
A mission is a question with its stem and diagram; a question whose stem changes part-way is two missions (2, 5, 9, 11). An MCQ
in a figure mission carries the figure itself (the MCQ stage shows an item's own figure only).
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the 1.5x page images and checked on a contact sheet with the
ingest's 1% padding (Q3 and Q4 are trimmed so the question text above and below stays out)."""
import json
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad agent_math_p2/figs.py + figs.json; [page, x0, y0, x1, y1] in points
    "Q3": [5, 66.7, 155.0, 536.7, 458.0], "Q4": [6, 120.0, 178.5, 501.3, 478.0], "Q7": [8, 63.3, 148.0, 540.0, 466.7],
    "Q8": [9, 96.7, 266.7, 510.0, 462.0], "Q9.1": [10, 216.7, 170.0, 400.0, 354.7], "Q9.2": [11, 128.0, 128.0, 412.0, 345.3],
    "Q10": [12, 186.7, 174.7, 441.3, 408.0], "Q11.1": [13, 103.3, 197.3, 470.0, 372.0], "Q11.2": [14, 96.7, 145.3, 445.3, 382.0]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None, must=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {})}


num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


# ---- QUESTION 1, the question paper page 3 and the memo page 3 ----
q1 = [
    steps("1.1", "Determine the equation of the least squares regression line.", 3, [
        ("a, the y-intercept of ŷ = a + bx (rand)", 1, 331397.20, 0.011, "a = 331 397,20 ✓ (calculator: 331 397,196…)"),
        ("b, the gradient (rand per year)", 2, -22988.32, 0.011, "b = −22 988,32 ✓; ŷ = 331 397,20 − 22 988,32x ✓ (the equation)")],
        ["Put the ages in as x and the prices as y in your calculator's linear regression (STAT, A + BX) mode.", "The price falls as the car ages: which sign must b have?"]),
    steps("1.2", "Predict the selling price of a similar car at this car dealership that is 5 years old.", 2, [
        ("Predicted selling price (rand)", 2, 216455.605, 0.01, "ŷ = 331 397,20 − 22 988,32(5) ✓ = 216 455,60 ✓ (calculator: 216 455,61 ✓✓)")],
        ["Substitute the age into your equation from 1.1.", "x is the age in years."]),
    rub("1.3", "Use the correlation coefficient to show whether the prediction made in QUESTION 1.2 is valid or not.", 2, [
        "Strong correlation (r = −0,95): the data points lie close to the regression line", "The prediction is valid"],
        ["Find r on your calculator, with the same data as in 1.1.", "How close is r to −1 or 1, and what does that say about the points and the line?"]),
    num("1.4", "Use the answer to QUESTION 1.1 to write down the estimated average yearly decrease in the selling price of these 11 cars.",
        22988.32, 0.011, "R", ["Which number in ŷ = a + bx tells you the change in price for each extra year?", "A decrease: give its size."]),
]

# ---- QUESTION 2, the question paper page 4 and the memo pages 4-5 ----
q21 = [
    num("2.1.1", "How many people visited this website on that day?", 70, 0, "people",
        ["A cumulative frequency keeps adding up.", "Which row's count includes every visitor?"]),
    steps("2.1.2", "How many people spent more than 40 and up to 80 minutes on the website?", 2, [
        ("Number of people", 2, 27, 0, "67 − 40 ✓ = 27 ✓")],
        ["The cumulative frequency up to 80 minutes counts everyone with t ≤ 80.", "Take away everyone with t ≤ 40."]),
    draw("2.1.3", "Draw a histogram to represent the information provided in the cumulative frequency table.", 3, [
        ["Two frequencies correct (the bars: 0–20: 16; 20–40: 24; 40–60: 19; 60–80: 8; 80–100: 3)", 1],
        ["All frequencies correct", 1], ["No gaps between the bars", 1]],
        ["First turn the cumulative frequencies into the frequency of each class: subtract the one before.", "A histogram's bars touch."],
        memo="The answer book gives the grid: number of people (0 to 70, steps of 5) up, time t in minutes (0 to 100, classes of 20) across."),
    mcq("2.1.4", "Comment on the skewness of the data.", ["Symmetrical", "Skewed to the right (positively skewed)",
                                                         "Skewed to the left (negatively skewed)"], 1,
        ["Work out each class's frequency: where is the peak, and which way does the tail run?", "The tail points towards the skew."]),
]
q22 = [
    steps("2.2", "How many players' points score was outside ONE standard deviation of the mean points score?", 5, [
        ("Points scored by the ninth player", 2, 10, 0, "(11 + 14 + 19 + 20 + 8 + 10 + 2 + 14 + x)/9 = 12 ✓ (equating, using the mean); x + 98 = 108; x = 10 ✓"),
        ("Standard deviation σ of all nine scores", 1, 5.23, 0.01, "σ = 5,23 (5,22812…) ✓"),
        ("Lower end of the interval, x̄ − σ", 1, 6.77, 0.01, "(x̄ − σ ; x̄ + σ) = (12 − 5,23 ; 12 + 5,23) = (6,77 ; 17,23) ✓ (the interval)"),
        ("Number of players outside one standard deviation of the mean", 1, 3, 0, "3 players' points (2, 19 and 20) were outside one standard deviation of the mean ✓")],
        ["The mean of all nine scores is 12: find the missing ninth score first.", "Use the population standard deviation (σ, σx on the calculator), then count the scores outside (x̄ − σ ; x̄ + σ)."]),
]

# ---- QUESTION 3, the question paper page 5 and the memo pages 6-8 ----
q3 = [
    steps("3.1", "Calculate the length of QR. Leave your answer in simplified surd form.", 2, [
        ("QR² (square units)", 1, 320, 0, "QR = √((−4 − 12)² + (−6 − 2)²) ✓ = √320"),
        ("QR in simplest surd form a√b: the whole number a", 1, 8, 0, "√320 = 8√5 units ✓")],
        ["Use the distance formula with Q and R.", "Take out the biggest perfect square that divides into the number under the root."]),
    steps("3.2", "Calculate the gradient of QR.", 2, [
        ("Gradient of QR", 2, 0.5, 0.001, "m(QR) = (−6 − 2)/(−4 − 12) ✓ = ½ ✓")],
        ["m = (y₂ − y₁)/(x₂ − x₁) with Q and R.", "Type a fraction as a decimal."]),
    steps("3.3", "Calculate the size of θ.", 2, [
        ("θ (degrees)", 2, 26.57, 0.011, "tan θ = m(QR) = ½ ✓; θ = 26,57° ✓")],
        ["The gradient of a line is the tangent of its angle of inclination.", "tan θ = m, then use tan⁻¹."]),
    steps("3.4", "Determine the equation of QR.", 2, [
        ("m, the gradient in y = mx + c", 1, 0.5, 0.001, "m(QR) = ½ (3.2)"),
        ("c, the y-intercept in y = mx + c", 1, -4, 0.001, "−6 = ½(−4) + c ✓ (OR y − 2 = ½(x − 12)); c = −4; y = ½x − 4 ✓")],
        ["You have the gradient from 3.2.", "Substitute Q or R into y = mx + c to find c."]),
    steps("3.5", "PQRS, in that order, is a parallelogram. Write down the coordinates of S.", 2, [
        ("x-coordinate of S", 1, 15, 0, "Q → R: (x ; y) → (x + 16 ; y + 8); S(15 ; 16): x(S) = 15 ✓"),
        ("y-coordinate of S", 1, 16, 0, "y(S) = 16 ✓")],
        ["In parallelogram PQRS, PS runs parallel and equal to QR.", "Move P by the same step that takes Q to R."]),
    steps("3.6", "T is a point on QR such that PT ⊥ QR. Calculate the coordinates of T.", 5, [
        ("Gradient of PT", 1, -2, 0.001, "m(QR) = ½, so m(PT) = −2 ✓"),
        ("c, the y-intercept of PT", 1, 6, 0.001, "8 = −2(−1) + c, c = 6: y = −2x + 6 ✓ (equation of PT)"),
        ("x-coordinate of T", 2, 4, 0.001, "−2x + 6 = ½x − 4 ✓ (equation QR = equation PT); −4x + 12 = x − 8 ✓ (simplification); 5x = 20; x = 4"),
        ("y-coordinate of T", 1, -2, 0.001, "y = ½(4) − 4 = −2: T(4 ; −2) ✓. OR: PQ = PR = √205, so △PQR is isosceles and the ⊥ height bisects the base: "
                                            "T is the midpoint of QR, T(4 ; −2)")],
        ["Perpendicular lines: the product of their gradients is −1.", "T lies on both PT and QR: solve the two equations together."]),
    steps("3.7", "Calculate the area of parallelogram PQRS.", 3, [
        ("Length of PT (units)", 1, 11.18, 0.011, "PT = √((4 − (−1))² + (−2 − 8)²) = √125 = 5√5 units = 11,18 units ✓"),
        ("Area of PQRS (square units)", 2, 200, 0.05, "Area of PQRS = QR.PT = (8√5)(5√5) ✓ = 200 units² ✓ (OR area of △PQR = ½(8√5)(5√5) = 100, doubled)")],
        ["Take QR as the base: PT is then the perpendicular height.", "Area of a parallelogram = base × perpendicular height."]),
]

# ---- QUESTION 4, the question paper page 6 and the memo pages 9-12 ----
q4 = [
    num("4.1", "Write down the value of p.", -6, 0, "",
        ["MC is parallel to the y-axis and passes through E.", "Every point on a vertical line has the same x-coordinate."]),
    mcq("4.2", "Show that q = 4." + "\n\nChoose the correct working.", ['AM = ME = q [radii]\nAD = q − 1, MD = q + 1\nq² = (q − 1)² + (q + 1)² [Pythagoras]\nq = 4', 'AM = ME = q + 1 [radii]\nAD = q − 1, MD = q\n(q + 1)² = (q − 1)² − q² [Pythagoras]\nq² + 4q = 0, so q = 4', 'AM = ME = q + 1 [radii]\nAD = q − 1, MD = q\n(q + 1)² = (q − 1)² + q² [Pythagoras]\nq² − 4q = 0, so q = 4 (q ≠ 0)', 'AM = ME = q + 1 [radii]\nAD = q − 1, MD = q\nq + 1 = (q − 1) + q [Pythagoras]\nq = 4'], 2, ["Write the radius, AD and MD in terms of q.", "△AMD has a right angle at D: use Pythagoras."], marks=4),
    steps("4.3", "Determine the equation of the circle in the form (x − a)² + (y − b)² = r².", 2, [
        ("a, in (x − a)² + (y − b)² = r²", 1, -6, 0.001, "The centre is M(−6 ; 4) (b = q = 4, shown in 4.2): (x + 6)² + (y − 4)² ✓ (LHS)"),
        ("r², the right-hand side", 1, 25, 0.001, "AM = q + 1 = 5 units: = 25 ✓ (RHS). (x + 6)² + (y − 4)² = 25")],
        ["The centre is M(p ; q): you have p (4.1) and q (4.2).", "The radius is ME = q + 1."]),
    num("4.4", "If the circle is translated 2 units to the left, determine the minimum distance between the circle and the y-axis.", 3, 0, "units",
        ["After the translation, how far is the centre from the y-axis?", "Then take away the radius."]),
    steps("4.5", "Calculate the coordinates of A and B.", 3, [
        ("x-coordinate of A", 2, -9, 0.001, "(x + 6)² + (0 − 4)² = 25 ✓ (substituting y = 0); (x + 6)² = 9; x + 6 = −3: A(−9 ; 0) ✓ "
                                           "(OR q − 1 = 3: DB = AD = 3 [line from centre ⊥ to chord])"),
        ("x-coordinate of B", 1, -3, 0.001, "x + 6 = 3: B(−3 ; 0) ✓")],
        ["A and B lie on the x-axis: their y-coordinate is 0.", "Put y = 0 into the circle's equation and solve for x."]),
    steps("4.6", "Determine the equation of tangent BC.", 4, [
        ("Gradient of radius MB", 1, -1.3333, 0.005, "m(MB) = (4 − 0)/(−6 − (−3)) = −4/3 ✓"),
        ("Gradient of tangent BC", 1, 0.75, 0.001, "m(BC) = ¾ ✓ (tangent ⊥ radius)"),
        ("c, the y-intercept of BC", 2, 2.25, 0.005, "0 = ¾(−3) + c ✓ (substitution of the gradient and B); c = 9/4: y = ¾x + 9/4 ✓")],
        ["A tangent is perpendicular to the radius at the point of contact.", "Then put B into y = mx + c."]),
    steps("4.7", "Write down the coordinates of C.", 2, [
        ("x-coordinate of C", 1, -6, 0.001, "C lies on MC (x = −6): x(C) = −6 ✓"),
        ("y-coordinate of C", 1, -2.25, 0.005, "y = ¾(−6) + 9/4 = −9/4: C(−6 ; −9/4) ✓")],
        ["C is on the vertical line through M.", "C is also on tangent BC: use your equation from 4.6."]),
    steps("4.8", "Calculate the size of AĈB.", 4, [
        ("α, the angle of inclination of BC (degrees)", 1, 36.87, 0.011, "tan α = ¾; α = 36,87° ✓"),
        ("β, the angle of inclination of AC (degrees)", 2, 143.13, 0.011, "m(AC) = −¾; tan β = m(AC) ✓; β = 180° − 36,87° = 143,13° ✓"),
        ("AĈB (degrees)", 1, 106.26, 0.011, "AĈB = β − α = 106,26° ✓. OR: MÂB = 53,13°, AM̂D = 36,87°, MÂC = 90° [tangent ⊥ radius], AĈM = 53,13°, "
                                           "AĈB = 106,26° [property of kite]; OR tan AĈD = AD/DC = 3 ÷ 9/4 = 4/3, AĈD = 53,13°; OR AC = BC = 15/4 "
                                           "and the cosine rule in △ABC: cos AĈB = −0,28")],
        ["The gradients of BC and AC give their angles of inclination.", "An exterior angle of a triangle equals the two interior opposite angles."]),
]

# ---- QUESTION 5, the question paper page 7 and the memo pages 13-14 ----
K = "√(k² + 1)"
q51 = [
    mcq("5.1.1", "It is given that tan 50° = k. Express cos 40° in terms of k.",
        ["1/" + K, K + "/k", "k/" + K, "k/√(1 − k²)"], 2,
        ["Draw a right-angled triangle with a 50° angle: tan 50° = k/1.", "Find the hypotenuse with Pythagoras; cos 40° = sin 50°."], marks=2),
    rub("5.1.2", "(2 sin 25°.cos 25°)/(−2 + 4 sin² 25°)", 5, [
        "Numerator: 2 sin 25°.cos 25° = sin 50°",
        "Denominator: −2(1 − 2 sin² 25°)",
        "Double angle: 1 − 2 sin² 25° = cos 50°, giving sin 50°/(−2 cos 50°)",
        "Substitution: (k/" + K + ") ÷ (−2/" + K + "), OR the quotient identity: −½ tan 50°",
        "Answer: −½k"],
        ["Both the numerator and the bracket in the denominator are double angles.", "sin 50° over cos 50° is a single ratio you know in terms of k."]),
    rub("5.1.3", "sin 10°", 4, [
        "sin 10° = sin(50° − 40°)",
        "Correct expansion: sin 50° cos 40° − cos 50° sin 40°",
        "First term: (k/" + K + ")(k/" + K + ")",
        "Second term: (1/" + K + ")(1/" + K + "), so sin 10° = (k² − 1)/(k² + 1)",
        "OR — sin 10° = cos 80°",
        "Correct expansion: cos 2(40°) = 2 cos² 40° − 1",
        "Substitution: 2(k/" + K + ")² − 1",
        "Substitution simplified: 2k²/(k² + 1) − 1 = (k² − 1)/(k² + 1)",
        "OR — sin 10° = sin(60° − 50°)",
        "Correct expansion: sin 60° cos 50° − cos 60° sin 50°",
        "First term: (√3/2)(1/" + K + ")",
        "Second term: (1/2)(k/" + K + "), so sin 10° = (√3 − k)/(2" + K + ")"],
        ["Write 10° as a difference of two angles whose ratios you know in terms of k.", "Use your triangle from 5.1.1 for sin 50°, cos 50°, sin 40° and cos 40°."]),
]
q52 = [
    rub("5.2.1", "Simplify the expression above fully to a single trigonometric ratio.", 4, [
        "sin(540° + x) = −sin x", "cos(90° + x) = −sin x", "sin(−x) = −sin x", "Answer: (−sin x)(−sin x)/(−sin x) = −sin x"],
        ["540° = 360° + 180°: reduce each angle to x.", "Watch the sign of each ratio in its quadrant."]),
    mcq("5.2.2", "Hence, determine the values of x in the interval x ∈ [0° ; 360°] for which √(sin(540° + x).cos(90° + x)/sin(−x)) will be real.",
        ["0° < x < 180°", "180° ≤ x ≤ 360°", "0° ≤ x ≤ 180°", "180° < x < 360°"], 3,
        ["A square root is real when the expression under it is not negative: use your answer to 5.2.1.", "sin(−x) sits in a denominator: it may not be 0."], marks=2),
]

# ---- QUESTION 6, the question paper page 7 and the memo pages 15-16 ----
q6 = [
    rub("6.1", "Prove that: [tan(180° − x)](1 − cos² x) + cos² x = (sin x − cos x)(1 + sin x.cos x)/(−cos x)", 6, [
        "tan(180° − x) = −tan x",
        "1 − cos² x = sin² x",
        "Quotient identity: −tan x = −sin x/cos x",
        "Simplification to a single fraction: (sin³ x − cos³ x)/(−cos x)",
        "Factors for a difference of cubes: (sin x − cos x)(sin² x + sin x.cos x + cos² x)",
        "sin² x + cos² x = 1, giving (sin x − cos x)(1 + sin x.cos x)/(−cos x) = RHS",
        "OR — From the RHS: 1 = sin² x + cos² x",
        "Expansion: (sin x − cos x)(cos² x + sin² x + sin x.cos x)",
        "Simplification: (sin³ x − cos³ x)/(−cos x)",
        "Split fraction: sin³ x/(−cos x) + cos² x",
        "Quotient identity: (−sin x/cos x)(sin² x) = −tan x(sin² x)",
        "sin² x = 1 − cos² x, giving −tan x(1 − cos² x) + cos² x = LHS"],
        ["Reduce tan(180° − x), then write everything in sin x and cos x.", "The numerator becomes a difference of two cubes."]),
    steps("6.2", "It is given that sin² x ; cos² x and ½ sin 2x are the first three terms of an arithmetic sequence. The constant difference of the "
          "arithmetic sequence is NOT zero. Determine the general solution for x.", 7, [
        ("tan x, from the factor that does not make the difference zero", 5, -2, 0.001,
         "cos² x − sin² x = ½ sin 2x − cos² x ✓; sin 2x = 2 sin x cos x ✓; 2 cos² x − sin x cos x − sin² x = 0 ✓ (standard form); "
         "(2 cos x + sin x)(cos x − sin x) = 0 ✓ (factors); 2 cos x = −sin x or cos x = sin x: tan x = −2 or tan x = 1 ✓ (both equations); "
         "tan x = 1 makes the difference zero, so x ≠ 45° + k.180°"),
        ("x, the solution in the second quadrant (degrees)", 1, 116.57, 0.011, "reference angle 63,43°: x = 116,57° ✓"),
        ("The period added in the general solution, x + k.(…)° (degrees)", 1, 180, 0, "x = 116,57° + k.180° ; k ∈ Z ✓")],
        ["Equal differences: T₂ − T₁ = T₃ − T₂.", "Factorise into two brackets; one of them gives a difference of zero."]),
]

# ---- QUESTION 7, the question paper page 8 and the memo page 17 ----
F7 = ("The graph of f(x) = cos 2x for x from −135° to 135°, on a grid with vertical lines at −135°, −90°, −45°, 45°, 90° and 135° and "
      "horizontal lines at y = 1 and y = −1: f starts at (−135° ; 0), falls to a minimum at (−90° ; −1), rises through (−45° ; 0) to a "
      "maximum at (0° ; 1), falls through (45° ; 0) to a minimum at (90° ; −1) and rises to (135° ; 0).")
q7 = [
    num("7.1", "Write down the period of f.", 180, 0, "°",
        ["The period is the length of one full wave.", "cos 2x repeats twice as fast as cos x."]),
    draw("7.2", "On the set of axes provided in the ANSWER BOOK, draw the graph of g(x) = tan 2x − 1 for x ∈ [−135° ; 135°].", 3, [
        ["Asymptotes at x = −135°, −45°, 45° and 135°", 1],
        ["Shape: increasing tan branches, each between two asymptotes", 1],
        ["Intercepts with the axes: x-intercepts at −67,5°, 22,5° and 112,5°; y-intercept −1", 1]],
        ["tan 2x has period 90°: its asymptotes are where 2x = ±90°, ±270°.", "The − 1 shifts the whole graph one unit down."]),
    mcq("7.3", "Graph f is translated 45° to the left to form graph h. Determine the equation of h in its simplest form.",
        ["h(x) = sin 2x", "h(x) = −sin 2x", "h(x) = cos(2x + 45°)", "h(x) = −cos 2x"], 1,
        ["Translating left by 45° replaces x with (x + 45°).", "cos 2(x + 45°) = cos(2x + 90°): reduce it."], figure=fig("Q7", F7)),
    mcq("7.4", "Graph f is translated 45° to the left to form graph h. Write down the range of h.",
        ["y ∈ [−1 ; 1]", "y ∈ [0 ; 1]", "y ∈ [−2 ; 2]", "y ∈ (−1 ; 1)"], 0,
        ["A horizontal shift moves a graph sideways only.", "Read the lowest and highest y-values of f."], figure=fig("Q7", F7)),
    mcq("7.5", "Determine the values of x for which (1 − tan 2x)(cos 2x) ≥ 0 in the interval x ∈ [0° ; 135°].",
        ["0° ≤ x ≤ 22,5° or 112,5° ≤ x ≤ 135°", "22,5° ≤ x < 45° or 45° < x ≤ 112,5°", "0° ≤ x ≤ 22,5° or 112,5° ≤ x < 135°", "0° ≤ x ≤ 22,5° only"], 2,
        ["(1 − tan 2x)(cos 2x) ≥ 0 is (tan 2x − 1)(cos 2x) ≤ 0: where are g and f on opposite sides of the x-axis?", "g is undefined at its asymptotes."],
        marks=4, figure=fig("Q7", F7)),
]

# ---- QUESTION 8, the question paper page 9 and the memo page 18 ----
q8 = [
    rub("8.1", "Show that AB = 18 cm.", 2, [
        "BC = 2AB", "Substitution into the area of the rectangle: 648 = 2AB × AB, so AB² = 324 and AB = 18 cm"],
        ["Write BC in terms of AB, from the ratio.", "Area of a rectangle = length × breadth."]),
    steps("8.2", "Calculate the length of AC.", 2, [
        ("AC (cm)", 2, 40.25, 0.011, "AC² = AB² + BC² [Pythagoras] = 18² + 36² ✓; AC = √1620 = 18√5 = 40,25 cm ✓")],
        ["ABCD is a rectangle: △ABC has a right angle at B.", "BC is twice AB."]),
    steps("8.3", "Calculate the length of diagonal KC.", 2, [
        ("KC (cm)", 2, 43.97, 0.011, "KC/sin KB̂C = BC/sin BK̂C; KC/sin 104° = 36/sin 52,6° ✓; KC = 36 sin 104°/sin 52,6° = 43,97 cm ✓")],
        ["In △KBC you know two angles and the side BC.", "The sine rule: each side over the sine of its opposite angle."]),
    steps("8.4", "If AB = BK, calculate the size of KÂC.", 4, [
        ("AK (cm)", 1, 25.46, 0.011, "AK² = AB² + BK² [Pythagoras] = 18² + 18²; AK = √648 = 18√2 = 25,46 cm ✓"),
        ("KÂC (degrees)", 3, 80.60, 0.011, "KC² = AK² + AC² − 2AK.AC cos KÂC; (43,97)² = (18√2)² + (18√5)² − 2(18√2)(18√5) cos KÂC ✓ (substitution into the "
                                          "cosine rule); cos KÂC = 0,16… ✓ (simplification); KÂC = 80,60° ✓")],
        ["AB is vertical and BK horizontal: △ABK has a right angle at B.", "In △AKC you then know all three sides: use the cosine rule."]),
]

# ---- QUESTION 9, the question paper pages 10-11 and the memo pages 19-20 ----
q91 = [
    mcq("9.1", "Use the diagram above to prove the theorem which states that the angle subtended by a chord (or arc) at the centre of the circle is "
        "equal to twice the angle subtended by the same chord (or arc) at the circumference, that is prove that TÔP = 2 TK̂P." + "\n\nChoose the correct working.", ['Construction: draw TP\nK̂ = T̂ = P̂ [∠s in the same segment]\nTÔP = 2 TK̂P [∠ at centre = 2 × ∠ at circumference]', 'Construction: draw KO produced\nK̂₁ = T̂ [OK = OT]\nÔ₁ = 180° − 2K̂₁ [ext ∠ of △]\nlikewise Ô₂ = 180° − 2K̂₂ [ext ∠ of △]\n∴ TÔP = 2 TK̂P', 'Construction: draw KO produced\nÔ₁ = K̂₁ and Ô₂ = K̂₂ [vert opp ∠s]\n∴ TÔP = K̂₁ + K̂₂ = 2 TK̂P', 'Construction: draw KO produced\nK̂₁ = T̂ [∠s opp equal sides]\nÔ₁ = K̂₁ + T̂ = 2K̂₁ [ext ∠ of △]\nlikewise Ô₂ = 2K̂₂ [ext ∠ of △]\n∴ TÔP = 2(K̂₁ + K̂₂) = 2 TK̂P'], 3, ["Draw the line from K through O: it splits the figure into two isosceles triangles.", "OK, OT and OP are radii; use the exterior angle of each triangle."], marks=5),
]
q92 = [
    steps("9.2.1", "Calculate, with reasons, the size of Ô₂.", 2, [
        ("Ô₂ (degrees)", 2, 64, 0, "Ô₂ = 64° ✓ S [∠ at centre = 2 × ∠ at circumference] ✓ R. OR PL̂O = P̂ = 32° [∠s opp equal radii] (S/R); Ô₂ = 64° "
                                   "[ext ∠ of △] (S)")],
        ["Ô₂ and P̂ stand on the same arc LF.", "The angle at the centre and the angle at the circumference."]),
    steps("9.2.2", "Calculate, with reasons, the size of M̂.", 3, [
        ("PF̂M (degrees)", 2, 90, 0, "PF̂M = 90° ✓ S [tan ⊥ diameter] ✓ R"),
        ("M̂ (degrees)", 1, 26, 0, "M̂ = 26° ✓ S [sum of ∠s of △]")],
        ["MF is a tangent at the end of the diameter PF.", "Then use the angles of △MOF."]),
]

# ---- QUESTION 10, the question paper page 12 and the memo pages 21-22 ----
q10 = [
    steps("10.1", "Calculate, with reasons, the size of QT̂S.", 3, [
        ("R̂ (degrees)", 1, 55, 0, "R̂ = 55° ✓ S [sum of ∠s in △] (in △QVR, V̂₂ = 90°)"),
        ("QT̂S (degrees)", 2, 55, 0, "QT̂S = 55° ✓ S [∠s in the same seg] ✓ R. OR Ŝ₂ = 35° [∠s in the same seg] (S, R); QT̂S = 55° [sum of ∠s in △] (S)")],
        ["QT ⊥ SR, so △QVR has a right angle at V.", "QT̂S and R̂ stand on the same chord QS."]),
    rub("10.2", "Prove that PQ ∥ SR.", 3, [
        "SP̂Q = 125°",
        "[opp ∠s of cyclic quad]",
        "Ŝ₁ = R̂ = 55° [given], so SP̂Q + Ŝ₁ = 180° and PQ ∥ SR [co-int ∠s supp]",
        "OR — PQ̂R = 125°",
        "[opp ∠s of cyclic quad]",
        "Q̂₁ = 125° − 35° = 90°, so Q̂₁ + V̂₁ = 180° and PQ ∥ SR [co-int ∠s supp]"],
        ["PQRS is a cyclic quadrilateral: its opposite angles add up to 180°.", "Co-interior angles that add up to 180° make the lines parallel."]),
    rub("10.3", "Prove that PT is a diameter of the circle.", 2, [
        "Q̂₁ = 90° [co-int ∠s; PQ ∥ SR]",
        "So PT is a diameter [converse ∠ in semi-circle / chord subtends 90°]",
        "OR — Ŝ₂ = 35° [ext ∠ of △SVT or sum of ∠s in △], so PŜT = 90°",
        "So PT is a diameter [converse ∠ in semi-circle / chord subtends 90°]"],
        ["Find a 90° angle that stands on chord PT.", "A chord that subtends 90° at the circumference is a diameter."]),
]

# ---- QUESTION 11, the question paper pages 13-14 and the memo pages 23-26 ----
q111 = [
    steps("11.1.1", "Calculate, with reasons, the value of FD/CF.", 2, [
        ("FD/CF", 2, 0.6667, 0.005, "FD/CF = GA/CG ✓ S [prop theorem; AD ∥ EF / line ∥ one side of △] = 2/3 ✓")],
        ["In △ADC, GF is parallel to AD.", "A line parallel to one side of a triangle divides the other two sides in the same proportion."]),
    steps("11.1.2", "Calculate, with reasons, the value of BA/EA.", 4, [
        ("FD as a multiple of x, taking CF = 2x and FB = 5x", 1, 1.3333, 0.005, "FD = ⅔CF = ⅔(2x) = 4/3 x ✓"),
        ("BA/EA", 3, 2.75, 0.005, "BA/EA = BD/FD ✓ S [prop theorem; AD ∥ EF / line ∥ one side of △]; = (5x − 4/3 x)/(4/3 x) ✓ (substitution) = 11/3 × 3/4 "
                                  "= 11/4 ✓")],
        ["Give CF and FB lengths in one unit x from CF/FB = 2/5, then find FD with 11.1.1.", "In △BEF, AD is parallel to EF."]),
    steps("11.1.3", "Calculate, with reasons, the value of Area of △GCF / Area of GFDA.", 4, [
        ("Area △GCF ÷ area △ACD", 2, 0.36, 0.005, "Area △GCF = ½(GC)(FC) sin Ĉ ✓ = ½(3k)(3p) sin Ĉ; area △ACD = ½ AC.CD sin Ĉ = ½(5k)(5p) sin Ĉ ✓ "
                                                 "(CG : GA = 3 : 2, CF : FD = 3 : 2); ratio 9/25"),
        ("Area △GCF ÷ area GFDA", 2, 0.5625, 0.005, "GFDA = △CDA − △CGF ✓; ½(9kp) sin Ĉ / ½ sin Ĉ (25kp − 9kp) = 9/16 ✓")],
        ["Both triangles share the angle C: area = ½ × side × side × sin Ĉ.", "GFDA is △ACD with △GCF taken away."]),
]
q112 = [
    mcq("11.2.1", "PR = PW.QR/QE" + "\n\nChoose the correct working.", ['{QE}/{QR} = {PW}/{PR} [line ∥ one side of △]\nPR = {PW.QE}/{QR}', '{QE}/{QR} = {PW}/{PR} [prop theorem; PQ ∥ WE]\nPR = {PW.QR}/{QE}', '{QE}/{QR} = {PR}/{PW} [prop theorem; PQ ∥ WE]\nPR = {PW.QR}/{QE}', '{QE}/{QR} = {PW}/{PR} [corresp ∠s; PQ ∥ WE]\nPR = {PW.QR}/{QE}'], 1, ["In △PQR, WE is parallel to PQ.", "Write the proportion, then make PR the subject."], marks=2),
    rub("11.2.2", "If △PQZ ||| △RQP, then PQ² = RQ.QZ", 1, [
        "PQ/RQ = QZ/QP [△PQZ ||| △RQP], so PQ² = RQ.QZ"],
        ["Similar triangles have sides in proportion: match the sides in the order of the letters.", "Then cross-multiply."]),
    rub("11.2.3", "△QSZ ||| △QRS", 3, [
        "Q̂₂ = Q̂₂ [common ∠]",
        "Ŝ₁ = R̂₂ [tan chord theorem]",
        "Ẑ₁ = QŜR [3rd ∠ of △], OR △QSZ ||| △QRS [∠∠∠]"],
        ["The two triangles share an angle at Q.", "QS is a tangent: the angle between a tangent and a chord equals the angle in the alternate segment."]),
    mcq("11.2.4", "PQ = QS" + "\n\nChoose the correct working.", ['{QS}/{QR} = {QZ}/{QS} [△QSZ ||| △QRS]\nQS² = QZ.QR\nbut PQ² = RQ.QZ [11.2.2]\n∴ PQ = QS', '{QS}/{QR} = {QZ}/{QS} [tan chord theorem]\nQS² = QZ.QR\nbut PQ² = RQ.QZ [11.2.2]\n∴ PQ = QS', '{QS}/{QR} = {QZ}/{QS} [△QSZ ||| △QRS]\nQS = QZ.QR\nbut PQ = RQ.QZ [11.2.2]\n∴ PQ = QS', '{QS}/{QR} = {SZ}/{QS} [△QSZ ||| △QRS]\nQS² = SZ.QR\nbut PQ² = RQ.QZ [11.2.2]\n∴ PQ = QS'], 0, ["Use the similar triangles of 11.2.3 to write QS² as a product.", "Compare it with PQ² from 11.2.2."], marks=3),
    mcq("11.2.5", "PW = QE.PZ/√(QR.QZ)" + "\n\nChoose the correct working.", ['PR = {PQ.PZ}/{QR} [△PQZ ||| △RQP]\nPR = {PW.QR}/{QE} [11.2.1]\nPW = {PQ.PZ.QE}/{QR²}\nPQ² = RQ.QZ [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}', 'PR = {QR.PZ}/{PQ} [△PQZ ||| △RQP]\nPR = {PW.QR}/{QE} [11.2.1]\nPW = {QE.PZ}/{PQ}\nPQ = RQ.QZ [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}', 'PR = {QR.PZ}/{PQ} [△PQZ ||| △RQP]\nPR = {PW.QR}/{QE} [11.2.1]\nPW = {QE.PZ}/{PQ}\nPQ = √(RQ.QZ) [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}', 'PR = {QR.PZ}/{PQ} [△PQZ ||| △RQP]\nPR = {PW.QE}/{QR} [11.2.1]\nPW = {QR².PZ}/{QE.PQ}\nPQ = √(RQ.QZ) [11.2.2]\n∴ PW = {QE.PZ}/{√(QR.QZ)}'], 2, ["Write PR in two ways: from 11.2.1 and from △PQZ ||| △RQP.", "Set them equal, then replace PQ using 11.2.2."], marks=4),
]

CARS = {"head": ["AGE OF CAR (IN YEARS)", "SELLING PRICE OF CAR (IN RAND)"],
        "rows": [["2", "293 000"], ["3", "265 000"], ["3", "256 000"], ["4", "219 000"], ["4", "241 000"], ["4", "246 000"], ["6", "226 000"],
                 ["6", "176 000"], ["7", "154 000"], ["7", "180 000"], ["8", "148 000"]]}
WEB = {"head": ["TIME, t (IN MINUTES)", "CUMULATIVE FREQUENCY"],
       "rows": [["0 < t ≤ 20", "16"], ["0 < t ≤ 40", "40"], ["0 < t ≤ 60", "59"], ["0 < t ≤ 80", "67"], ["0 < t ≤ 100", "70"]]}
POINTS = {"head": ["PLAYER", "POINTS SCORED"],
          "rows": [[str(i + 1), v] for i, v in enumerate(["11", "14", "19", "20", "8", "10", "2", "14"])]}
REASONS = "Provide reasons for your statements in QUESTIONS 9, 10 and 11."
missions = [
    {"id": "1", "title": "Question 1", "kind": "Regression and correlation", "marks": 8,
     "lead": "There were 11 cars of the same model for sale at a car dealership. The age (in years) of each car and its corresponding selling price "
             "(in rands) is provided in the table below.", "table": CARS, "items": q1},
    {"id": "2.1", "title": "Question 2.1", "kind": "Cumulative frequency", "marks": 7,
     "lead": "The cumulative frequency table below shows the amount of time that people spent on a particular website on a certain day.",
     "table": WEB, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Mean and standard deviation", "marks": 5,
     "lead": "There are 9 players in a basketball team. The coach calculated that on average, each player scored 12 points during a game. The points "
             "scored by 8 of the 9 players from the team is given below:", "table": POINTS, "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Lines and a triangle", "marks": 18,
     "lead": "In the diagram, P(−1 ; 8), Q(−4 ; −6) and R(12 ; 2) are the vertices of △PQR. The angle of inclination of QR is θ.",
     "figure": fig("Q3", "Axes with origin O. Triangle PQR: P(−1 ; 8) just left of the y-axis near the top, R(12 ; 2) to the right above the x-axis, "
                   "Q(−4 ; −6) at the bottom left. Side QR rises from Q, crosses the y-axis below O and the x-axis to the right of O; θ is marked "
                   "where QR crosses the x-axis, between the x-axis and QR."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "The circle and its tangents", "marks": 21,
     "lead": "In the diagram, M(p ; q) is the centre of the circle that intersects the x-axis at A and B. C is a point such that the line drawn from "
             "M to C is parallel to the y-axis and intersects the x-axis at D. MC intersects the circle at E(−6 ; −1). Tangents drawn from C touch "
             "the circle at A and B. AD = (q − 1) units.",
     "figure": fig("Q4", "Axes with origin O. A circle with centre M(p ; q) to the left of the y-axis and above the x-axis cuts the x-axis at A (left) "
                   "and B (right), both left of O. A vertical line from M goes down through D on the x-axis and E on the circle to C below the "
                   "circle. Radii MA and MB are drawn, and the tangents CA and CB."), "items": q4},
    {"id": "5.1", "title": "Question 5.1", "kind": "Ratios in terms of k", "marks": 11,
     "lead": "It is given that tan 50° = k. Express EACH of the following in terms of k:", "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Reduction formulae", "marks": 6,
     "lead": "Given: sin(540° + x).cos(90° + x)/sin(−x)", "items": q52},
    {"id": "6", "title": "Question 6", "kind": "Identities and general solutions", "marks": 13, "items": q6},   # no shared stem printed
    {"id": "7", "title": "Question 7", "kind": "Trigonometric graphs", "marks": 10,
     "lead": "In the diagram, the graph of f(x) = cos 2x is drawn for x ∈ [−135° ; 135°].", "figure": fig("Q7", F7), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Sine, cosine and area rules", "marks": 10,
     "lead": "As part of a school project, learners are required to design a portable stage for a puppet show, as shown in the diagram below. The "
             "design must fulfil the following requirements:\n• BKLC is a horizontal base having KB̂C = 104° and BK̂C = 52,6°.\n• The rectangular "
             "backdrop, ABCD, is vertical to the horizontal base and must have an area of 648 cm².\n• The sides of ABCD must be in the ratio AB : BC "
             "= 1 : 2.\n• The stage must be partly enclosed with triangular sides ABK and DCL.",
     "figure": fig("Q8", "A puppet stage. A shaded horizontal base BKLC: B at the back left, C at the back right, K at the front left and L at the "
                   "front right, with diagonal KC; KB̂C = 104° and BK̂C = 52,6°. A vertical rectangle ABCD (Area = 648 cm²) stands on BC, A above B "
                   "and D above C, with right angles at B and C. Triangular sides ABK on the left and DCL on the right."), "items": q8},
    {"id": "9.1", "title": "Question 9.1", "kind": "Circle geometry proof", "marks": 5,
     "lead": REASONS + " In the diagram, O is the centre of the circle. K, T and P lie on the circle.",
     "figure": fig("Q9.1", "A circle with centre O; K at the top, T at the bottom left and P at the bottom right. Chords KT and KP are drawn, and "
                   "radii OT and OP (TÔP opens downward)."), "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Angles, tangents and diameters", "marks": 5,
     "lead": REASONS + " In the diagram, O is the centre of the circle. POF is the diameter of the circle and MF is a tangent to the circle at F. "
             "OM cuts the circle at L. P̂ = 32°. Calculate, with reasons, the size of:",
     "figure": fig("Q9.2", "A circle with centre O and a vertical diameter POF, P at the top and F at the bottom. The tangent at F runs left to M; "
                   "the line OM cuts the circle at L, on the lower left. Chord PL is drawn; the angle at P between PL and PF is 32°. At O, angle 1 "
                   "lies between OP and OL, and angle 2 between OL and OF."), "items": q92},
    {"id": "10", "title": "Question 10", "kind": "Cyclic quadrilaterals", "marks": 8,
     "lead": REASONS + " In the diagram, PQRS is a cyclic quadrilateral. T is a point on the circle such that QT is perpendicular to SR at V. PT and "
             "ST are drawn. Q̂₂ = 35° and R̂ = Ŝ₁.",
     "figure": fig("Q10", "A circle through P (upper left), Q (top right), R (right), T (bottom right) and S (left). Quadrilateral PQRS; chord QT "
                   "crosses SR at V at right angles (angles V₁ to V₄, V₁ marked 90°); chords PT and ST are drawn. Q̂₁ lies between QP and QT, Q̂₂ "
                   "= 35° between QT and QR; P̂₁ between PS and PT, P̂₂ between PT and PQ; Ŝ₁ between SP and SR, Ŝ₂ between SR and ST; T̂₁ and "
                   "T̂₂ at T, either side of TP."), "items": q10},
    {"id": "11.1", "title": "Question 11.1", "kind": "Proportionality", "marks": 10,
     "lead": REASONS + " In the diagram, △ABC is drawn. BA is produced to E. F and D are points on BC such that AD ∥ EF. AC and EF intersect at G. "
             "CF/FB = 2/5 and CG/GA = 3/2. Calculate, with reasons, the value of:",
     "figure": fig("Q11.1", "Triangle ABC with B at the top right, C at the bottom and A on the upper left. BA is produced to E on the left. D and F "
                   "lie on BC, D nearer B. AD and EF are parallel (arrows); EF cuts AC at G."), "items": q111},
    {"id": "11.2", "title": "Question 11.2", "kind": "Similar triangles", "marks": 13,
     "lead": REASONS + " In the diagram, WVZR is a cyclic quadrilateral. RZ is produced to Q. A tangent is drawn from Q to touch the circle at S. WV "
             "is produced to E, a point on ZQ. RW produced meets ZV produced in P. PQ ∥ WE. RS and ZS are drawn. Prove, with reasons, that:",
     "figure": fig("Q11.2", "A circle through W (top), R (right), S (bottom), Z and V (left). P lies above and left of the circle: RW produced and ZV "
                   "produced meet at P. RZ produced meets Q at the bottom left; QS is a tangent at S. WV produced meets ZQ at E. PQ ∥ WE (arrows). "
                   "RS and ZS are drawn. Angles: P̂₁, P̂₂; Ŵ₁, Ŵ₂; V̂₁, V̂₂; R̂₁, R̂₂; Ẑ₁, Ẑ₂; Ŝ₁ (between SQ and SZ), Ŝ₂; Q̂₁ (between QP and QR), Q̂₂ "
                   "(between QR and QS)."), "items": q112},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": "4.2", "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): 4.2, 9.1, 11.2.1, 11.2.4, 11.2.5 ask for written working or an answer a word marker cannot read (an inequality, an interval, a coordinate, a proof); each is played as four options, the memo's answer or working and three built from common errors, and keeps its marks."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from the page IMAGES: the question paper "
                                                           "and answer book are scans with no text layer, and the memo's text layer garbles fractions "
                                                           "and diagrams; no API call."},
        {"n": "1.1", "kind": "no_fit", "detail": "Calculations play as steps: each step is the number the memo's method produces, its formula, "
                                                 "substitution and equation marks riding on that number (the phone sees numbers, not working)."},
        {"n": "2.2", "kind": "no_fit", "detail": "The memo's interval mark rides on its lower end x̄ − σ = 6,77; the upper end 17,23 is in the memo "
                                                 "text, not asked (step marks are whole). The table's player numbers 1-8 are ours: the paper prints "
                                                 "the eight scores in one row."},
        {"n": "2.1.3", "kind": "no_fit", "detail": "Drawings (2.1.3 histogram, 7.2 graph of g) are done on paper and self-checked against the memo's "
                                                   "criteria. The app's histogram builder marks T C L S P (6 marks), not this memo's 3-mark scheme "
                                                   "(two frequencies, all frequencies, no gaps), so 2.1.3 is a plain draw. The answer book's blank "
                                                   "grid is not used: the scan shows darker grid segments that read like pre-drawn bars."},
        {"n": "3.1", "kind": "no_fit", "detail": "A simplified surd (8√5) plays as QR² = 320 (the substitution mark) and the whole number a = 8 of "
                                                 "a√b (the answer mark); 320 = 64 × 5 then fixes b."},
        {"n": "3.4", "kind": "no_fit", "detail": "Line equations (3.4 y = ½x − 4, 4.6 y = ¾x + 9/4) play as their numbers m and c: the strict term "
                                                 "compares letters and digits only, so y = ½x − 4 and y = ½x + 4 would be one answer. Fractions are "
                                                 "typed as decimals (−4/3 -> −1,33; 9/4 -> 2,25)."},
        {"n": "4.3", "kind": "no_fit", "detail": "The circle's equation plays as a = −6 (the LHS mark) and r² = 25 (the RHS mark); b = q = 4 is shown "
                                                 "in 4.2 and not asked, and the sign change into (x + 6)² is not tested."},
        {"n": "5.1.1", "kind": "no_fit", "detail": "Expressions in k with one step of working (5.1.1) and choices whose open or closed ends matter "
                                                   "(5.2.2, 7.4, 7.5), an equation of a graph (7.3) and the skewness (2.1.4) play as MCQs of the "
                                                   "plausible forms, all or nothing: 5.1.1 loses the memo's 'third side' mark, 7.5 (4 marks) its "
                                                   "x = 22,5° and inequality-sign marks."},
        {"n": "5.1.2", "kind": "no_fit", "detail": "Expressions in k (5.1.2, 5.1.3), the reductions (5.2.1), 'Show that' (1.3, 4.2, 8.1) and proofs "
                                                   "(6.1, 9.1, 10.2, 10.3, 11.2.1-11.2.5) are rubrics: the memo's ticks, one bullet each, 'OR — ' "
                                                   "starting an alternative. They need the AI marker: the keyword stand-in reads only words over "
                                                   "five letters, and most maths bullets have none."},
        {"n": "6.2", "kind": "no_fit", "detail": "The general solution plays as steps: tan x = −2 (the memo's five method marks ride on it), x = 116,57° "
                                                 "and the period 180°; 'k ∈ Z' is not checked and the equivalent −63,43° + k.180° is not accepted "
                                                 "by the second step (its label asks for the second-quadrant solution)."},
        {"n": "9.2.1", "kind": "no_fit", "detail": "'Calculate, with reasons' an angle or a ratio (9.2.1, 9.2.2, 10.1, 11.1.1-11.1.3) plays as steps: "
                                                   "the R (reason) marks ride on the number, as working marks do; the reasons are in each step's memo."},
        {"n": "1.4", "kind": "low_confidence", "detail": "The yearly DECREASE is keyed as a positive amount (22 988,32); a learner typing −22 988,32 "
                                                         "is marked wrong."},
        {"n": "4.8", "kind": "low_confidence", "detail": "Steps follow the memo's first method (angles of inclination α and β); its four other "
                                                         "methods (kite, tan AĈD, the cosine rule) reach the same 106,26° but not the step values, "
                                                         "and are listed in the last step's memo."},
    ],
}
out = Path(__file__).parent / "out" / "math-p2-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper, memo and answer book PDFs' page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
