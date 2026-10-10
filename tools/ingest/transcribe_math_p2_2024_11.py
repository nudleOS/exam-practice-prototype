"""Mathematics P2 Nov 2024, the whole paper (Questions 1 to 11: statistics, analytical geometry, trigonometry, Euclidean geometry),
hand-transcribed into the catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any
ingested paper. Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues, figure
captions and the wrong options of the authored multiple choice are ours. No API call: the transcription is the source, kept in git
(out/ is not). The question paper and the answer book are SCANS (no text layer) and the memo's text layer garbles fractions, roots
and diagrams: everything was read from the page IMAGES (1,5x).

  python tools/ingest/transcribe_math_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P2 Nov 2024 Eng.pdf" "<...>/Mathematics P2 Nov 2024 MG Afr & Eng.pdf" \
      --id math-p2-2024-11 --from-json --answer-book "<...>/Mathematics P2 Nov 2024 Answer Book Afr & Eng.pdf"

How the memo's shapes map (as Mathematics P2 Nov 2025: the phone has a number keypad, multiple choice, short text and self-checked
drawings, no algebra input):
  a number the memo calculates (a, b, a prediction, a quartile, a gradient, a length, a ratio, an angle, a coordinate) -> steps,
  each step ONE number the method produces, its formula and substitution marks riding on that number; tolerances cover the memo's
  rounding (its answers are two-decimal roundings: 0,006 for a value keyed at two decimals, 0,011 for one the memo prints to two
  decimals from a longer calculation, 0,005 for a fraction typed as a decimal, 1/3 -> 0,33); a coordinate is two steps (x, y);
  an equation of a line or an asymptote -> its numbers as steps (m and c; x = k), because the strict term compares letters and
  digits only and y = −⅓x + 10 / y = ⅓x + 10 would be one answer; a read-off -> num;
  "How does ... influence the standard deviation" -> term (its phrasings, 'increases' / 'decreases' rejected);
  "Calculate, with a reason" an angle -> steps (the reason mark rides on the number);
  "Draw a box and whisker diagram / the graph of g" -> draw with the memo's criteria (self-checked, flagged no_fit).
  Authored multiple choice (Murci, 2026-10-10) for every part a word or number marker cannot score: an interval (7.2), an expression
  in p (5.2), a general solution with working (7.4), "Show that" (3.3, 4.3, 4.4, 6.1.2), a derivation (6.1.1) and the proofs (4.6,
  9.2, 10.1, 10.2.1, 11.1-11.4). The stem gets "Choose the correct answer." (a short answer) or "Choose the correct working." (a
  working or a proof); four options: the memo's own answer or first method, and three built from real errors (a sign slip, a lost
  solution, the wrong theorem or reason, a converse, a circular reason, a flawed step that still claims the result). Options are
  laid out AS THE MEMO: one step per line ("\n"), a proof's [reason] at the END of its line, a fraction {numerator}/{denominator}
  (drawn stacked); every option of a part has the same number of lines and [reasons], so the layout never points at the answer;
  the right option sits at A, B, C and D four times each. Each keeps its marks (0 or full).
A mission is a question with its stem and diagram; a question whose stem changes part-way is two or three missions (5, 6, 10). A
single-line MCQ in a figure mission carries the figure itself (the MCQ stage shows an item's own figure only); a working MCQ plays
on the page, under the mission's figure.
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the 1,5x page images and ink-column profiles, and checked on
crops made as the ingest makes them (1% pad, 150 dpi; scratchpad math2_24: figs.py + figs.json); `inset` 40 on Q1 and Q2, whose
axis labels sit near the crop's top-left corner (the page's Hide button sits there). No figure comes from the answer book: its
diagrams repeat the question paper's (the push-up table, the ogive, Q3-Q5, the graph of tan x, Q8-Q11), and 2.4's scaled line is
described in the draw's memo; --answer-book is passed anyway, so an answer-book figure added later needs no change to the command."""
import json
import re
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad math2_24/figs.py + figs.json; [source, page, x0, y0, x1, y1] in points ("qp" the question paper, "ab" the answer book)
    "Q1": ["qp", 3, 122, 253, 517, 497], "Q2": ["qp", 4, 93, 141, 530, 397], "Q3": ["qp", 5, 113, 148, 493, 477],
    "Q4": ["qp", 6, 93, 172, 483, 453], "Q5": ["qp", 7, 213, 141, 343, 263], "Q7": ["qp", 9, 87, 150, 513, 427],
    "Q8": ["qp", 10, 137, 205, 488, 530], "Q9": ["qp", 11, 190, 190, 383, 410], "Q10.1": ["qp", 12, 190, 147, 410, 317],
    "Q10.2": ["qp", 12, 140, 453, 483, 697], "Q11": ["qp", 13, 130, 180, 443, 397]}
INSET = {"Q1": 40, "Q2": 40}


def fig(name, caption):
    src, p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"source": "answer_book"} if src == "ab" else {}), **({"inset": INSET[name]} if name in INSET else {})}


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


ANS, WORK = "\n\nChoose the correct answer.", "\n\nChoose the correct working."
EXACT, DP2, MEMO2, FRAC = 0.001, 0.006, 0.011, 0.005   # exact; keyed at two decimals; printed to two decimals; a fraction as a decimal

# ---- QUESTION 1, the question paper page 3 and the memo page 3 ----
q1 = [
    steps("1.1", "Determine the equation of the least squares regression line for the data.", 3, [
        ("a, the y-intercept of ŷ = a + bx", 1, 39.46, DP2, "a = 39,456001… ✓ a = 39,46"),
        ("b, the gradient of ŷ = a + bx", 2, -0.59, DP2, "b = −0,590018… ✓ b = −0,59; ŷ = 39,46 − 0,59x ✓ (equation). CORRECT ANSWER ONLY: FULL MARKS")],
        ["Put the weights in as x and the push-ups as y in your calculator's linear regression (STAT, A + BX) mode.",
         "The heavier players did fewer push-ups: which sign must b have?"]),
    num("1.2", "Write down the correlation coefficient.", -0.8, DP2, "",
        ["Find r on your calculator, with the same data as in 1.1.", "The points fall from left to right: which sign does r have?"]),
    steps("1.3", "The coach uses the least squares regression line to set the target for the minimum number of push-ups by each team member "
          "according to their weight. Predict the number of push-ups that a member of the team, who weighs 29 kg, should do to meet the target.", 2, [
        ("Predicted number of push-ups per minute", 2, 22.35, MEMO2, "y = 39,46 − 0,59(29) ✓ (substitution); y = 22,35 ✓ (OR y = 22,35 on the "
                                                                    "calculator ✓✓)")],
        ["Substitute the weight into your equation from 1.1.", "x is the weight in kg."]),
    num("1.4", "Write down the mean number of push-ups for the given data.", 18.33, DP2, "push-ups",
        ["Use the y-values only.", "Your calculator gives ȳ in the same statistics mode."]),
    term("1.5", "The players trained hard during the season. At the end of the season, the coach reported that each player was able to do 5 more "
         "push-ups per minute than they did at the beginning of the season. How does the increase in the number of push-ups influence the "
         "standard deviation of the data?",
         ["No influence", "It has no influence", "The increase has no influence", "The standard deviation stays the same",
          "The standard deviation remains the same", "It stays the same", "It remains the same", "Stays the same", "Remains the same",
          "No change", "It does not change", "Does not change", "It will not change", "Unchanged", "It is unchanged", "No effect",
          "It has no effect", "The same"],
        ["The standard deviation measures how spread out the data is around the mean.", "Adding the same number to every value moves the "
                                                                                          "data: does it spread it out?"],
        reject=["It increases", "Increases", "It increases by 5", "It decreases", "Decreases", "An influence", "It has an influence",
                "It changes", "Changes"]),
    steps("1.6", "At the beginning of the season, the coach used the least squares regression line as the minimum target for a player to aim "
          "for. Determine the maximum possible increase in the number of push-ups that a team member must obtain to reach the minimum target.", 2, [
        ("Push-ups per minute of the player furthest below the line", 1, 6, 0, "6 is the furthest y-value below the least squares regression "
                                                                               "line ✓"),
        ("Maximum possible increase (push-ups)", 1, 10, 0, "An increase of 10 push-ups will get the team member to (40 ; 16), the minimum number "
                                                           "of push-ups for a player weighing 40 kg ✓ (difference is 10)")],
        ["Find the point that lies furthest BELOW the regression line on the scatter plot.", "Read the line's value at that weight, in whole "
                                                                                             "push-ups."]),
]

# ---- QUESTION 2, the question paper page 4 and the memo page 4 ----
q2 = [
    num("2.1", "Estimate the median travel time.", 65, 0.5, "minutes",
        ["The median is the middle value: half of the 60 employees.", "Go across from that cumulative frequency to the ogive, then down."]),
    num("2.2", "Estimate the lower quartile.", 44, 0.5, "minutes",
        ["The lower quartile is a quarter of the way through the data.", "A quarter of 60 employees: read the time at that cumulative "
                                                                          "frequency."]),
    steps("2.3", "Estimate the interquartile range.", 2, [
        ("Upper quartile, Q₃ (minutes)", 1, 84, 0.5, "Q₃ = 84 ✓"),
        ("Interquartile range (minutes)", 1, 40, 0.5, "IQR = 84 − 44 = 40 ✓")],
        ["Find the upper quartile the same way: three quarters of 60.", "IQR = Q₃ − Q₁."]),
    draw("2.4", "The minimum and maximum times taken for an employee to travel to work are 5 and 120 minutes respectively. On the scaled line "
         "in the ANSWER BOOK, draw a box and whisker diagram to indicate the distribution of the data as represented in the ogive above.", 2, [
        ["Box: from the lower quartile (44) to the upper quartile (84), with the median (65) inside", 1],
        ["Whiskers ending at 5 and 120", 1]],
        ["You need five numbers: the minimum, Q₁, the median, Q₃ and the maximum.", "The box runs between the quartiles; the whiskers reach the "
                                                                                     "smallest and largest times."],
        memo="The answer book gives a scaled line from 0 to 120 minutes (labels every 10, ticks every 5). Five-number summary: 5 ; 44 ; 65 ; "
             "84 ; 120."),
    steps("2.5", "The company manager decided that all employees who travel for an hour or more will be allowed to work from home for part of "
          "the day. What percentage of the employees will be allowed to work from home for part of the day?", 2, [
        ("Number of employees who travel for an hour or more", 1, 34.5, 0.51, "Number of employees who qualify = 34 ✓ (OR 35 ✓)"),
        ("Percentage of the employees (%)", 1, 57.5, 0.84, "% of employees who qualify = 34/60 × 100 = 56,67% of the employees ✓ (OR 35/60 × 100 "
                                                            "= 58,33% ✓)")],
        ["Read the cumulative frequency at 60 minutes: that many travel for less than an hour.", "Take them away from 60, then write the "
                                                                                                 "answer as a percentage of 60."]),
    steps("2.6", "Employees work 8 hours in a normal working day. The manager decided on the following rule for time to work from home:\n"
          "• An employee is allowed to work half an hour from home for each time interval of 20 minutes, or part thereof, above an hour taken "
          "to travel to work.\nOn a certain day, an employee takes 110 minutes to travel to work. Calculate the number of minutes that this "
          "employee will be allowed to work from home on this day.", 2, [
        ("Number of 20-minute intervals (or part thereof) above an hour", 1, 3, 0, "Number of intervals = 3 ✓"),
        ("Minutes allowed to work from home", 1, 90, 0, "Time allowed to work from home = 3(30 minutes) = 90 minutes OR 1,5 hours ✓")],
        ["How many minutes above an hour is 110 minutes?", "A part of an interval counts as a whole interval."]),
]

# ---- QUESTION 3, the question paper page 5 and the memo pages 5-7 ----
q3 = [
    steps("3.1", "Calculate the gradient of DC.", 2, [
        ("Gradient of DC", 2, -0.75, EXACT, "m(DC) = (−9 − 0)/(3 − (−9)) ✓ (correct substitution of D(3 ; −9) and C(−9 ; 0) into the gradient "
                                            "formula); m(DC) = −3/4 ✓")],
        ["m = (y₂ − y₁)/(x₂ − x₁) with D and C.", "Type a fraction as a decimal."]),
    steps("3.2", "Determine the equation of DC in the form y = mx + c.", 2, [
        ("m, the gradient in y = mx + c", 1, -0.75, EXACT, "0 = −3/4(−9) + c ✓ (correct substitution of C(−9 ; 0) or D(3 ; −9) into the equation "
                                                           "of the line; OR y − 0 = −3/4(x − (−9)))"),
        ("c, the y-intercept in y = mx + c", 1, -6.75, EXACT, "c = −27/4 or −6 3/4: y = −3/4 x − 27/4 ✓ (answer)")],
        ["You have the gradient from 3.1.", "Substitute C or D into y = mx + c to find c."]),
    mcq("3.3", "Show that k = −6." + WORK, [
        "k = −{3}/{4}(−1) − {27}/{4}\nk = −{3}/{4} − {27}/{4}\nk = −6",
        "−1 = −{3}/{4}k − {27}/{4}\n{3}/{4}k = −{23}/{4}\nk = −6",
        "k = −{3}/{4}(−1) − {27}/{4}\nk = {3}/{4} − {27}/{4}\nk = −6",
        "k = −6 gives B(−1 ; −6)\n−6 = −{3}/{4}(−1) − {27}/{4}\n−6 = −6, so k = −6"], 2,
        ["B lies on DC: its coordinates satisfy the equation from 3.2.", "Substitute x = −1 (not the answer) and watch the sign of −3/4 × −1."]),
    steps("3.4", "Calculate the length of DC.", 2, [
        ("Length of DC (units)", 2, 15, EXACT, "DC = √((3 + 9)² + (−9 − 0)²) ✓ (correct substitution of D(3 ; −9) and C(−9 ; 0) into the distance "
                                               "formula); DC = 15 units ✓")],
        ["Use the distance formula with D and C.", "d = √((x₂ − x₁)² + (y₂ − y₁)²)."]),
    steps("3.5", "Calculate the ratio of DB/DC.", 2, [
        ("Length of DB (units)", 1, 5, EXACT, "DB = √((3 − (−1))² + (−9 − (−6))²); DB = 5 ✓"),
        ("DB/DC", 1, 0.3333, FRAC, "∴ DB/DC = 5/15 = 1/3 ✓")],
        ["B is (−1 ; −6), from 3.3.", "Find DB with the distance formula, then divide by DC from 3.4."]),
    steps("3.6", "If M is a point on AD such that AC ∥ MB, calculate the ratio of Area △MBD / Area △ACD.", 4, [
        ("DM/DA", 1, 0.3333, FRAC, "DM/DA = DB/DC = 1/3 ✓ (DM/DA = DB/DC; MB ∥ AC)"),
        ("Area △MBD ÷ area △ACD", 3, 0.1111, FRAC, "Area △MBD / Area △ACD = [½(DM)(DB) sin D̂] / [½(DA)(DC) sin D̂] ✓ (correct use of the area rule) "
                                                   "= 1/3 × 1/3 ✓ (substitution for BD/DC and DM/DA into the correct formula) = 1/9 ✓")],
        ["MB is parallel to AC in △ACD: a line parallel to one side divides the other two sides in proportion.",
         "Both triangles share the angle D: area = ½ × side × side × sin D̂."]),
    steps("3.7", "If it is further given that the gradient of AD is −4 and the length of AD is √612 units, calculate the coordinates of A.", 6, [
        ("c, the y-intercept of AD", 1, 3, EXACT, "y = −4x + c; −9 = −4(3) + c ✓ (correct substitution of m(AD) = −4 and D(3 ; −9)); c = 3: "
                                                  "y = −4x + 3"),
        ("x-coordinate of A", 4, -3, EXACT, "(x − 3)² + (y + 9)² = 612 ✓; (x − 3)² + (−4x + 3 + 9)² = (√612)² ✓ (substitution of equation AD into "
                                            "the distance formula); x² − 6x + 9 + 16x² − 96x + 144 = 612; 17x² − 102x − 459 = 0; x² − 6x − 27 = 0 "
                                            "✓ (standard form); (x − 9)(x + 3) = 0; x = 9 (N/A) or x = −3 ✓ (x values with rejection)"),
        ("y-coordinate of A", 1, 15, EXACT, "y = −4(−3) + 3; y = 15: A(−3 ; 15) ✓. OR N(0 ; 3) ✓ (the y-intercept of AD); ND = √((3 − 0)² + "
                                            "(−9 − 3)²) = 3√17 ✓; AD = 6√17, ND = ½AD ✓: N is the midpoint of AD, A(−3 ; 15) ✓ x-value ✓ y-value")],
        ["Find the equation of AD from its gradient and D.", "A lies on AD at a distance √612 from D: solve the two together; A is in the "
                                                             "second quadrant."]),
]

# ---- QUESTION 4, the question paper page 6 and the memo pages 8-11 ----
q4 = [
    steps("4.1", "Write down the coordinates of L.", 2, [
        ("x-coordinate of L", 1, -1, EXACT, "L(−1 ; −3): x = −1 ✓"),
        ("y-coordinate of L", 1, -3, EXACT, "y = −3 ✓")],
        ["PL passes through the centre M: it is a diameter.", "M is the midpoint of PL."]),
    steps("4.2", "Determine the equation of tangent ST to the circle at P.", 4, [
        ("Gradient of radius MP", 1, 3, EXACT, "m(MP) = (9 − 3)/(3 − 1); m(MP) = 3 ✓"),
        ("Gradient of tangent ST", 1, -0.3333, FRAC, "m(ST) = −1/3 ✓ (m(ST) = −1/m(MP))"),
        ("c, the y-intercept of ST", 2, 10, EXACT, "9 = −1/3(3) + c ✓ (substitution of m(ST) and P(3 ; 9) into the equation of a line; OR y − 9 = "
                                                   "−1/3(x − 3)); c = 10: y = −1/3 x + 10 ✓ (equation of tangent ST)")],
        ["A tangent is perpendicular to the radius at the point of contact.", "Then put P into y = mx + c."]),
    mcq("4.3", "Show that the equation of the circle with centre M is x² + y² − 2x − 6y − 30 = 0." + WORK, [
        "(x + 1)² + (y + 3)² = r²\n(3 + 1)² + (9 + 3)² = r²\nr² = 160\n(x + 1)² + (y + 3)² = 160\nx² + 2x + 1 + y² + 6y + 9 = 160\n"
        "x² + y² − 2x − 6y − 30 = 0",
        "(x − 1)² + (y − 3)² = r²\n(3 − 1)² + (9 − 3)² = r²\nr² = 40\n(x − 1)² + (y − 3)² = 40\nx² − 2x + 1 + y² − 6y + 9 = 40\n"
        "x² + y² − 2x − 6y − 30 = 0",
        "(x − 1)² + (y − 3)² = r²\n(3 − 1)² + (9 − 3)² = r²\nr² = 40\n(x − 1)² + (y − 3)² = 40\nx² − 1 + y² − 9 = 40\n"
        "x² + y² − 2x − 6y − 30 = 0",
        "(x − 1)² + (y − 3)² = r²\n(3 + 1)² + (9 + 3)² = r²\nr² = 160\n(x − 1)² + (y − 3)² = 160\nx² − 2x + 1 + y² − 6y + 9 = 160\n"
        "x² + y² − 2x − 6y − 30 = 0"], 1,
        ["The centre is M(1 ; 3) and P(3 ; 9) is on the circle: r = MP.", "Check each line: the signs in (x − a)², and each expansion."], marks=4),
    mcq("4.4", "Show that d = 7." + WORK, [
        "d = 7: (7)² + (1)² − 2(7) − 6(1) − 30\n= 49 + 1 − 14 − 6 − 30\n= 0\nR(7 ; 1) lies on the circle\n∴ d = 7",
        "d² + (1)² − 2d − 6(1) − 30 = 0\nd² − 2d − 35 = 0\n(d + 7)(d − 5) = 0\nd = −7 or d = 5\n∴ d = 7",
        "d² + (1)² − 2d − 6(1) − 30 = 0\nd² − 2d − 35 = 0\nd² − 2d = 35\nd(d − 2) = 35\n∴ d = 7",
        "d² + (1)² − 2d − 6(1) − 30 = 0\nd² − 2d − 35 = 0\n(d − 7)(d + 5) = 0\nd = 7 or d = −5\n∴ d = 7"], 3,
        ["R(d ; 1) is on the circle: substitute it into the equation from 4.3.", "A 'show that' may not start from the answer; d > 0."], marks=2),
    steps("4.5", "Calculate the size of L̂.", 5, [
        ("PÔV, the angle of inclination of PL (degrees)", 2, 71.57, MEMO2, "m(PO) = 3, ∴ tan PÔV = 3 ✓ (tan PÔV = m(PO)); PÔV = 71,565…° ✓"),
        ("Gradient of RL", 1, 0.5, EXACT, "m(RL) = (1 − (−3))/(7 − (−1)) = 1/2 ✓ (using R(7 ; 1) and L)"),
        ("RV̂N, the angle of inclination of RL (degrees)", 1, 26.57, MEMO2, "tan RV̂N = 1/2; RV̂N = 26,565…° ✓"),
        ("L̂ (degrees)", 1, 45, MEMO2, "L̂ = 71,565…° − 26,565…° [ext ∠ of △]; L̂ = 45° ✓. OR R̂ = 90° [∠ in semi-circle] ✓, PR = √80 = 4√5 ✓, "
                                       "PL = √160 = 4√10 OR RL = √80 = 4√5 ✓, sin L̂ = 4√5/4√10 OR cos L̂ = 4√5/4√10 OR tan L̂ = 4√5/4√5 ✓, "
                                       "L̂ = 45° ✓. OR PL, PR and LR ✓✓✓, cos L = (80 + 160 − 80)/(2√80 × √160) ✓ (cosine rule) = √2/2, "
                                       "L̂ = 45° ✓")],
        ["The gradients of PL and RL give their angles of inclination with the x-axis.",
         "In △OVL, the angle at O's side is an exterior angle: use the exterior angle of a triangle."]),
    mcq("4.6", "TR is a tangent to the circle at R. Prove that PT ⊥ RT." + WORK, [
        "m(RM) = {1 − 3}/{7 − 1} = −{1}/{3}\nm(RT) = 3 [tan ⊥ rad]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT",
        "m(RM) = {1 − 3}/{7 − 1} = −{1}/{3}\nm(RT) = 3 [tan-chord theorem]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT",
        "m(RM) = {1 − 3}/{7 − 1} = {1}/{3}\nm(RT) = −3 [tan ⊥ rad]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT",
        "m(RM) = {1 − 3}/{7 − 1} = −{1}/{3}\nm(RT) = 3 [PT ⊥ RT]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT"], 0,
        ["RT is a tangent at R: it is perpendicular to the radius MR.", "PT lies on tangent ST (4.2); perpendicular gradients multiply to −1."],
        marks=3),
]

# ---- QUESTION 5, the question paper page 7 and the memo pages 12-13 ----
q51 = [
    steps("5.1.1", "cos A", 2, [
        ("r, the length of OP", 1, 5, EXACT, "r = 5 ✓"),
        ("cos A", 1, -0.6, EXACT, "cos A = −3/5 ✓")],
        ["Use Pythagoras with x = −3 and y = −4.", "cos A = x/r."]),
    steps("5.1.2", "cos 2A", 2, [
        ("cos 2A", 2, -0.28, EXACT, "cos 2A = 2cos² A − 1 = 2(−3/5)² − 1 ✓ (substitution of cos A into the double angle formula) = −7/25 ✓. "
                                    "OR cos² A − sin² A = (−3/5)² − (−4/5)² = −7/25; OR 1 − 2sin² A = 1 − 2(−4/5)² = −7/25")],
        ["Choose a double angle formula for cos 2A.", "Use your cos A from 5.1.1 (sin A = −4/5)."]),
    steps("5.1.3", "sin(A − B), if it is further given that sin B = 4/5 and 90° < B < 360°", 4, [
        ("x, the x-coordinate of B's point (x ; 4) with r = 5", 1, -3, EXACT, "x = −3 ✓ (sin B > 0 with 90° < B < 360°: B is in the second "
                                                                             "quadrant)"),
        ("sin(A − B)", 3, 0.96, EXACT, "sin(A − B) = sin A cos B − cos A sin B = (−4/5)(−3/5) − (−3/5)(4/5) ✓✓ (substitution into the compound "
                                       "angle formula) = 12/25 + 12/25 = 24/25 ✓")],
        ["sin B is positive between 90° and 360° only in the second quadrant: draw B there.", "Expand sin(A − B) with the compound angle "
                                                                                            "formula."]),
]
q52 = [
    mcq("5.2", "If cos α = p, express the following expression in terms of p:\n(cos(α/2 − 45°).sin(α/2 − 45°))/2" + WORK, [
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {2 cos(α/2 − 45°).sin(α/2 − 45°)}/{2.2}\n= {sin(α − 90°)}/{4}\n= {cos α}/{4}\n= {p}/{4}",
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {sin 2(α/2 − 45°)}/{2}\n= {sin(α − 90°)}/{2}\n= {−cos α}/{2}\n= {−p}/{2}",
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {2 cos(α/2 − 45°).sin(α/2 − 45°)}/{2.2}\n= {sin(α − 90°)}/{4}\n= {−cos α}/{4}\n= {−p}/{4}",
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {2 cos(α/2 − 45°).sin(α/2 − 45°)}/{2.2}\n= {sin(α − 45°)}/{4}\n= {−cos α}/{4}\n= {−p}/{4}"], 2,
        ["2 sin θ cos θ = sin 2θ: multiply the numerator and the denominator by 2.", "sin(α − 90°) = −sin(90° − α): use the co-function."],
        marks=4),
]

# ---- QUESTION 6, the question paper page 8 and the memo pages 14-15 ----
N6, D6 = "cos(90° − x)cos y + sin(−y)cos(180° + x)", "cos x cos(360° + y) + sin(360° − x)sin y"
q61 = [
    mcq("6.1.1", "Use the compound angle identity given above to derive a formula for cos(x + y)." + WORK, [
        "cos(x + y) = cos(x − (−y))\n= cos x cos(−y) + sin x sin(−y)\n= cos x cos y + sin x sin y",
        "cos(x + y) = cos(x − (−y))\n= cos x cos(−y) + sin x sin(−y)\n= cos x cos y − sin x sin y",
        "cos(x + y) = cos(x − (−y))\n= cos x cos(−y) + sin x sin(−y)\n= −cos x cos y − sin x sin y",
        "cos(x + y) = −cos(x − y)\n= −(cos x cos y + sin x sin y)\n= cos x cos y − sin x sin y"], 1,
        ["Write x + y as x − (−y), then use the identity given.", "cos(−y) = cos y, but sin(−y) = −sin y."], marks=2),
    mcq("6.1.2", "Hence, or otherwise, show that:\n(" + N6 + ")/(" + D6 + ") = tan(x + y)" + WORK, [
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(sin x)cos y + (−sin y)(cos x)}/{cos x(cos y) + (−sin x)sin y}\n"
        "= {sin x cos y − cos x sin y}/{cos x cos y − sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS",
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(sin x)cos y + (−sin y)(−cos x)}/{cos x(cos y) + (sin x)sin y}\n"
        "= {sin x cos y + cos x sin y}/{cos x cos y + sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS",
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(cos x)cos y + (−sin y)(−cos x)}/{cos x(cos y) + (−sin x)sin y}\n"
        "= {cos x cos y + cos x sin y}/{cos x cos y − sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS",
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(sin x)cos y + (−sin y)(−cos x)}/{cos x(cos y) + (−sin x)sin y}\n"
        "= {sin x cos y + cos x sin y}/{cos x cos y − sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS"], 3,
        ["Reduce each angle first: cos(90° − x), sin(−y), cos(180° + x), cos(360° + y), sin(360° − x).",
         "The numerator and the denominator are then compound angle expansions."], marks=6),
]
q62 = [
    steps("6.2", "Given: f(x) = √(6 sin² x − 11 cos(90° + x) + 7)\nSolve for x in the interval x ∈ (0° ; 360°) if f(x) = 2.", 6, [
        ("sin x, from the factor that gives solutions", 4, -0.3333, FRAC,
         "6 sin² x − 11 cos(90° + x) + 7 = 4 ✓ (squaring both sides); 6 sin² x − 11(−sin x) + 7 = 4 ✓ (cos(90° + x) = −sin x); 6 sin² x + 11 sin x "
         "+ 3 = 0; (3 sin x + 1)(2 sin x + 3) = 0 ✓ (factors); sin x = −1/3 OR sin x = −3/2 ✓ (both equations), the second with no solution"),
        ("Smaller solution, x (degrees)", 1, 199.47, MEMO2, "ref ∠ = 19,47°; x = 199,47° ✓"),
        ("Larger solution, x (degrees)", 1, 340.53, MEMO2, "x = 340,53° ✓")],
        ["Square both sides, then reduce cos(90° + x).", "Factorise the quadratic in sin x; sin x is negative in the third and fourth quadrants."]),
]
q63 = [
    steps("6.3.1", "Calculate the maximum value of g.", 3, [
        ("Maximum value of g", 3, 1.3333, FRAC, "g(x) = 4(1 − 2sin² x)/3 ✓ (factors) = 4cos 2x/3 ✓; maximum value of cos 2x is 1: ∴ maximum value "
                                                "of g(x) = 4/3 ✓. OR 4 − 8sin² x is a maximum when sin² x is a minimum: min of sin² x = 0 ✓, "
                                                "g(x) = (4 − 8(0))/3 ✓ = 4/3 ✓. OR sin x = −(0)/(2(−8/3)) ✓, sin x = 0 ✓, g(x) = 4/3 ✓")],
        ["Take out the common factor 4: 1 − 2sin² x is a double angle.", "Or: g is largest when sin² x is smallest."]),
    num("6.3.2", "Write down the smallest possible value of x for which g will have a maximum value in the interval x ∈ (0° ; 360°].", 180, 0, "°",
        ["g is a maximum where sin x = 0 (cos 2x = 1).", "The interval leaves out 0°."]),
]

# ---- QUESTION 7, the question paper page 9 and the memo page 16 ----
F7 = ("The graph of f(x) = tan x for x from −180° to 180°, with y marked from −3 to 3: dashed asymptotes at x = −90° and x = 90°; f passes "
      "through (−180° ; 0), (0 ; 0) and (180° ; 0), each of its three branches rising from left to right.")
q7 = [
    steps("7.1", "Write down the equation of the asymptote of f in the interval x ∈ [0° ; 180°].", 1, [
        ("k, in the asymptote's equation x = k (degrees)", 1, 90, 0, "x = 90° ✓")],
        ["An asymptote of tan x is a vertical dashed line.", "Find the one between 0° and 180°."]),
    mcq("7.2", "Write down the values of x in the interval x ∈ [−180° ; 0°] for which f(x) ≤ 0." + ANS, [
        "x = −180° or −90° < x ≤ 0°", "−90° < x ≤ 0°", "x = −180° or −90° ≤ x ≤ 0°", "−180° ≤ x < −90°"], 0,
        ["Look for where the graph is on or below the x-axis between −180° and 0°.", "f is undefined at its asymptote, and f(x) = 0 counts too."],
        marks=2, figure=fig("Q7", F7)),
    num("7.3.1", "Given: g(x) = cos 2x + 1\nWrite down the period of g.", 180, 0, "°",
        ["The period is the length of one full wave.", "cos 2x repeats twice as fast as cos x."]),
    draw("7.3.2", "Given: g(x) = cos 2x + 1\nOn the grid given in the ANSWER BOOK, draw the graph of g(x) = cos 2x + 1 for the interval "
         "x ∈ [−180° ; 180°]. Clearly show the intercepts with the axes as well as the coordinates of the turning points.", 3, [
        ["Turning points on the x-axis: x = −90° ; 90°", 1], ["Shape", 1], ["Turning point on the y-axis at (0 ; 2)", 1]],
        ["cos 2x has period 180° and lies between −1 and 1.", "The + 1 lifts the whole graph one unit up."],
        memo="The answer book's grid repeats the paper's graph of f(x) = tan x. g runs from (−180° ; 2) down to (−90° ; 0), up to (0 ; 2), "
             "down to (90° ; 0) and up to (180° ; 2)."),
    mcq("7.4", "Use the graphs to determine the general solution of 2cos³ x − sin x = 0." + WORK, [
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {sin x}/{cos x}\n2cos² x = tan x\n2cos² x − 1 = tan x − 1\ncos 2x + 1 = tan x\n"
        "x = 45° + k.360° ; k ∈ Z",
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {sin x}/{cos x}\n2cos² x = tan x\n2cos² x − 1 = tan x − 1\ncos 2x + 1 = tan x\n"
        "x = 45° + k.180° ; k ∈ Z",
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {sin x}/{cos x}\n2cos² x = tan x\n2cos² x − 1 = tan x\ncos 2x = tan x\n"
        "x = 45° + k.180° ; k ∈ Z",
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {cos x}/{sin x}\n2cos² x = tan x\n2cos² x − 1 = tan x − 1\ncos 2x + 1 = tan x\n"
        "x = 45° + k.180° ; k ∈ Z"], 1,
        ["Divide by cos x to bring in tan x, then make the left side cos 2x + 1.", "g and f meet once in every 180°: where?"], marks=4),
]

# ---- QUESTION 8, the question paper page 10 and the memo pages 17-18 ----
q8 = [
    steps("8.1", "Calculate the length of AC, the distance between the observer at A and the foot of the building.", 2, [
        ("AC (m)", 2, 15, MEMO2, "tan DÂC = DC/AC; AC = 16/tan 46,85° ✓ (correct substitution into the trig ratio); AC = 15 m ✓")],
        ["△ACD has a right angle at C.", "You know the side opposite the 46,85° angle; AC is adjacent to it."]),
    steps("8.2", "Calculate how far the painter at E is from the top of the building.", 7, [
        ("BC (m)", 4, 8.30, MEMO2, "(AB)² = (BC)² + (AC)² − 2(BC)(AC) cos BĈA; (19)² = x² + (15)² − 2x(15) cos 105,61° ✓ (correct substitution into "
                                   "the cosine rule); x² + 8,07x − 136 = 0 ✓ (quadratic equation in standard form); x = [−8,07 ± √((8,07)² − "
                                   "4(1)(−136))]/(2(1)) ✓ (correct substitution into the quadratic formula); x = 8,30 m or x ≠ −16,38 m ✓ (length "
                                   "of BC). OR sin 105,61°/19 = sin CB̂A/15 ✓ (sine rule); CB̂A = 49,5°; BÂC = 24,89° ✓; BC/sin 24,89° = "
                                   "19/sin 105,61° ✓; BC = 8,3 m ✓"),
        ("BÊC (degrees)", 1, 58, 0, "BÊC = 58° ✓ (OR EB̂C = 32°)"),
        ("EC (m)", 1, 5.19, MEMO2, "tan BÊC = BC/EC; EC = 8,3/tan 58° (OR tan EB̂C = EC/BC, EC = 8,3 tan 32°); EC = 5,19 m ✓"),
        ("DE (m)", 1, 10.81, MEMO2, "DE = 10,81 m ✓")],
        ["In △ABC you know AB, AC and the angle C: the cosine rule gives a quadratic in BC.",
         "BÊC is on a straight line with DÊB; then use △BCE (right-angled at C) for EC, and DE = DC − EC."]),
]

# ---- QUESTION 9, the question paper page 11 and the memo page 19 ----
q9 = [
    steps("9.1", "Calculate, with a reason, the value of Â₁.", 2, [
        ("Â₁ (degrees)", 2, 40, 0, "Â₁ = 40° ✓ S [ext ∠ of a cyclic quad] ✓ R")],
        ["Ĉ₁ is an exterior angle of the cyclic quadrilateral ABCD.", "It equals the interior opposite angle, DÂB = Â₁ + Â₂."]),
    mcq("9.2", "Hence, prove that AD = DC." + WORK, [
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [opp ∠s of cyclic quad]\n∴ Ĉ₂ = 40° [∠s opp equal sides]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [sides opp = ∠s]",
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [ext ∠ of cyclic quad]\n∴ Ĉ₂ = 40° [sum of ∠s in △]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [sides opp = ∠s]",
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [opp ∠s of cyclic quad]\n∴ Ĉ₂ = 40° [sum of ∠s in △]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [sides opp = ∠s]",
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [opp ∠s of cyclic quad]\n∴ Ĉ₂ = 40° [sum of ∠s in △]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [∠s opp equal sides]"], 2,
        ["Find B̂ from Â₁ = ½B̂, then D̂ in the cyclic quadrilateral.", "Show that the two angles of △ADC opposite AD and DC are equal."],
        marks=4),
]

# ---- QUESTION 10, the question paper page 12 and the memo pages 20-22 ----
CON = "Construction: join SB and TA; draw h₁ from B ⊥ AR and h₂ from A ⊥ RB"
R1, R2 = "{area △RAB}/{area △ASB} = {½RA × h₁}/{½AS × h₁} = {RA}/{AS}", "{area △RAB}/{area △ABT} = {½RB × h₂}/{½BT × h₂} = {RB}/{BT}"
R1x, R2x = "{area △RAB}/{area △ASB} = {½RA × h₂}/{½AS × h₂} = {RA}/{AS}", "{area △RAB}/{area △ABT} = {½RB × h₁}/{½BT × h₁} = {RB}/{BT}"
END = "∴ {area △RAB}/{area △ASB} = {area △RAB}/{area △ABT}\n∴ {RA}/{AS} = {RB}/{BT}"
COM = "area △RAB = area △RAB [common]"
q101 = [
    mcq("10.1", "Prove the theorem which states that a line drawn parallel to one side of a triangle divides the other two sides proportionally, "
        "i.e. RA/AS = RB/BT" + WORK, [
        "\n".join([CON, R1, R2, COM, "but area △ASB = area △ABT [prop theorem; AB ∥ ST]", END]),
        "\n".join([CON, R1x, R2x, COM, "but area △ASB = area △ABT [same base & height; AB ∥ ST]", END]),
        "\n".join([CON, R1, R2, COM, "but area △ASB = area △ABT [same base & height; AS ∥ BT]", END]),
        "\n".join([CON, R1, R2, COM, "but area △ASB = area △ABT [same base & height; AB ∥ ST]", END])], 3,
        ["Compare triangles that share a height: their areas are in the ratio of their bases.",
         "△ASB and △ABT stand on the same base AB between the parallel lines AB and ST."], marks=6),
]
q102 = [
    mcq("10.2.1", "Prove, with reasons, that OR : WS = 1 : 2" + WORK, [
        "PR = RS [line from centre ⊥ to chord]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [midpt theorem]\n∴ OR : WS = 1 : 2",
        "PR = RS [line from centre to midpt of chord]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [midpt theorem]\n∴ OR : WS = 1 : 2",
        "PR = RS [line from centre ⊥ to chord]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [prop theorem; OR ∥ WS]\n∴ OR : WS = 1 : 2",
        "PR = RS [midpt theorem]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [line from centre ⊥ to chord]\n∴ OR : WS = 1 : 2"], 0,
        ["OR is drawn from the centre perpendicular to the chord PS: what does it do to PS?", "R and O are then midpoints of two sides of △PSW."],
        marks=5),
    steps("10.2.2", "Calculate the length of PT if ST = 15 units.", 4, [
        ("RS (units)", 2, 5, EXACT, "OV/VT = RS/ST = 1/3 ✓ S/R [prop theorem; RO ∥ SW]; RS/15 = 1/3; RS = 5 units ✓ S"),
        ("PR (units)", 1, 5, EXACT, "PR = RS = 5 units ✓ S [line from centre ⊥ to chord]"),
        ("PT (units)", 1, 25, EXACT, "∴ PT = 25 units ✓")],
        ["OV : OT = 1 : 4, so OV : VT = 1 : 3; in △ORT, VS is parallel to OR.", "PT = PR + RS + ST."]),
]

# ---- QUESTION 11, the question paper page 13 and the memo pages 23-25 ----
GF0, GF1, GF2 = "{GF}/{BC} = {AF}/{AC} [△AGF ||| △ABC]", "{GF}/{BC} = {AC}/{AF} [△AGF ||| △ABC]", "∴ GF = {BC.AF}/{AC}"
SIM, SIMx = "△ACD ||| △FGC [∠∠∠]", "△ACD ||| △FGC [prop theorem; DC ∥ FG]"
MID = "∴ {AC}/{GF} = {AD}/{FC}\n∴ AC = {AD.FG}/{FC}\n∴ GF = BC.AF ÷ {AD.FG}/{FC}"
INV, INVx, LAST = "GF = BC.AF × {FC}/{AD.FG}", "GF = BC.AF × {AD.FG}/{FC}", "∴ GF² = {BC.FC.AF}/{AD}"
q11 = [
    mcq("11.1", "If EÂG = x, determine with reasons, FOUR other angles that are equal to x." + WORK, [
        "D̂₁ = EÂG = x [∠s in the same seg]\nĈ₁ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAF̂G = EÂG = x [tan-chord theorem]",
        "D̂₁ = EÂG = x [tan-chord theorem]\nĈ₁ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAF̂G = EÂG = x [tan-chord theorem]",
        "D̂₁ = EÂG = x [tan-chord theorem]\nĈ₃ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAF̂G = EÂG = x [tan-chord theorem]",
        "D̂₁ = EÂG = x [tan-chord theorem]\nĈ₁ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAĜF = EÂG = x [tan-chord theorem]"], 1,
        ["EA is a tangent to BOTH circles at A, and EF is a tangent to the smaller circle at C.",
         "The angle between a tangent and a chord equals the angle in the alternate segment."], marks=6),
    mcq("11.2", "Prove that AG.AD = AC.AF" + WORK, [
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [corresp ∠s; DC ∥ FG]\n{AG}/{AC} = {AF}/{AD} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF",
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [corresp ∠s =]\n{AG}/{AC} = {AD}/{AF} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF",
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [alt ∠s =]\n{AG}/{AC} = {AF}/{AD} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF",
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [corresp ∠s =]\n{AG}/{AC} = {AF}/{AD} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF"], 3,
        ["From 11.1, D̂₁ and AF̂G are equal: what does that make DC and FG?", "Then a line parallel to one side of △AGF divides the other sides "
                                                                              "in proportion."], marks=4),
    mcq("11.3", "Prove that △AGF ||| △ABC" + WORK, [
        "In △AGF and △ABC\nĜ = B̂₂ [∠s in the same seg]\nAF̂G = Ĉ₁ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [∠∠∠]",
        "In △AGF and △ABC\nĜ = B̂₂ [tan-chord theorem]\nAF̂G = Ĉ₁ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [∠∠∠]",
        "In △AGF and △ABC\nĜ = B̂₂ [∠s in the same seg]\nAF̂G = Ĉ₄ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [∠∠∠]",
        "In △AGF and △ABC\nĜ = B̂₂ [∠s in the same seg]\nAF̂G = Ĉ₁ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [sides in prop]"], 0,
        ["Ĝ and B̂₂ both stand on the chord AF of the larger circle.", "Use an angle equal to x from 11.1 that lies inside △ABC."], marks=4),
    mcq("11.4", "Prove that GF² = (BC.FC.AF)/AD" + WORK, [
        "\n".join([GF1, GF2, SIM, MID, INV, LAST]),
        "\n".join([GF0, GF2, SIMx, MID, INV, LAST]),
        "\n".join([GF0, GF2, SIM, MID, INV, LAST]),
        "\n".join([GF0, GF2, SIM, MID, INVx, LAST])], 2,
        ["From 11.3, write GF in terms of BC, AF and AC.", "Find a second pair of similar triangles that gives AC in terms of AD, FG and FC, "
                                                            "then substitute."], marks=6),
]

PUSH = {"head": ["Weight (in kg) (x)", "Number of push-ups per minute (y)"],
        "rows": [[a, b] for a, b in zip("34 32 40 27 33 28 27 55 39 44 30 57 28 32 31".split(), "26 21 6 20 16 26 23 7 18 14 17 8 28 25 20".split())]}
REASONS = "Provide reasons for your statements in QUESTIONS 9, 10 and 11."
missions = [
    {"id": "1", "title": "Question 1", "kind": "Regression and correlation", "marks": 10,
     "lead": "At the beginning of a season, the coach of a junior boys' rugby team recorded the weight (in kg) of the 15 players in his team "
             "and the number of push-ups that each player was able to do in one minute. The data is represented in the table and scatter "
             "plot below. The least squares regression line for the data is drawn.", "table": PUSH,
     "figure": fig("Q1", "A scatter plot: weight (in kg) from 0 to 60 across, push-ups per minute from 0 to 30 up. The 15 players' points from "
                   "the table, most of them between 27 and 34 kg, and the least squares regression line falling from left to right through "
                   "them, from about 27 kg to about 57 kg."), "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Ogive and box and whisker", "marks": 10,
     "lead": "The cumulative frequency graph (ogive) shows the time taken (in minutes) for 60 employees to travel to work each morning.",
     "figure": fig("Q2", "An ogive: time (in minutes) from 0 to 140 across, cumulative frequency from 0 to 65 up, on a fine grid. The curve has "
                   "plotted points at 0, 20, 40, 60, 80, 100 and 120 minutes: it starts at (0 ; 0), rises slowly at first, most steeply "
                   "between 60 and 100 minutes, and levels off at 60 employees at 120 minutes."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Lines and a triangle", "marks": 19,
     "lead": "In the diagram below, △ACD has vertices A, D(3 ; −9) and C(−9 ; 0), where A is a point in the second quadrant. B(−1 ; k) lies "
             "on side DC.",
     "figure": fig("Q3", "Axes with origin O. Triangle ACD: A high up in the second quadrant, C(−9 ; 0) on the negative x-axis and D(3 ; −9) "
                   "in the fourth quadrant. Side AD crosses the x-axis just right of O. B(−1 ; k) is marked on side DC, just left of the "
                   "y-axis."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "The circle and its tangents", "marks": 20,
     "lead": "In the diagram, M(1 ; 3) is the centre of the circle. The circle cuts the x-axis at N. ST is a tangent to the circle at P(3 ; 9). "
             "R(d ; 1), with d > 0, and L lie on the circle. O and V are the x-intercepts of PL and RL respectively.",
     "figure": fig("Q4", "Axes with origin O. A circle with centre M(1 ; 3) through P(3 ; 9) at the top, R(d ; 1) on the right just above the "
                   "x-axis, N where it cuts the positive x-axis, and L below the x-axis on the left. The tangent ST touches the circle at P, "
                   "S on the y-axis and T to the right. Chord PL passes through M and O; chord PR is drawn; chord RL cuts the x-axis at V, "
                   "between O and N."), "items": q4},
    {"id": "5.1", "title": "Question 5.1", "kind": "Ratios from a point", "marks": 8,
     "lead": "In the diagram, line OP is given with P(−3 ; −4). KÔP = A.\nDetermine, without using a calculator, the value of:",
     "figure": fig("Q5", "Axes with origin O and the point K on the positive x-axis. The line OP runs into the third quadrant to P(−3 ; −4). A "
                   "curved arrow marks the angle A, turning anticlockwise from OK round to OP."), "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Double angles and co-functions", "marks": 4, "items": q52},   # the whole stem is the part's
    {"id": "6.1", "title": "Question 6.1", "kind": "Compound angle identities", "marks": 8,
     "lead": "Given the identity: cos(x − y) = cos x cos y + sin x sin y", "items": q61},
    {"id": "6.2", "title": "Question 6.2", "kind": "Trigonometric equations", "marks": 6, "items": q62},
    {"id": "6.3", "title": "Question 6.3", "kind": "Maximum of a trig function", "marks": 4,
     "lead": "Consider the function: g(x) = (4 − 8 sin² x)/3", "items": q63},
    {"id": "7", "title": "Question 7", "kind": "Trigonometric graphs", "marks": 11,
     "lead": "In the diagram below, the graph of f(x) = tan x is drawn for the interval x ∈ [−180° ; 180°].", "figure": fig("Q7", F7),
     "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Heights and distances in 3D", "marks": 9,
     "lead": "In the diagram, C is the foot of a vertical building and D is the top of the same building. The height of the building, CD, is "
             "16 m. Two observers are standing 19 m apart at points A and B, where A, B and C lie in the same horizontal plane. A painter is "
             "working at point E on the building. The angle of elevation of D from A is 46,85°. DÊB = 122° and BĈA = 105,61°.",
     "figure": fig("Q8", "A drawing of a building with its vertical edge CD: C its foot, D its top, CD marked 16. E is a point on CD. On the "
                   "shaded ground, triangle ABC: B on the left, A on the right, AB = 19 and BĈA = 105,61°, with right angles at C between CD "
                   "and the ground. Lines DA and EB are drawn: the angle at A between AC and AD is 46,85°, and DÊB = 122° is marked at E."),
     "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Cyclic quadrilaterals", "marks": 6,
     "lead": REASONS + " In the diagram, ABCD is a cyclic quadrilateral. BC is produced to E. AC is drawn. Â₁ = ½B̂, Â₂ = 46° and Ĉ₁ = 86°.",
     "figure": fig("Q9", "A circle through A (top), B (right), C (bottom) and D (left): cyclic quadrilateral ABCD with the diagonal AC. BC is "
                   "produced beyond C to E. At A, angle 1 lies between AD and AC, angle 2 (46°) between AC and AB. At C, angle 1 (86°) lies "
                   "between CE and CD, angle 2 between CD and CA, angle 3 between CA and CB."), "items": q9},
    {"id": "10.1", "title": "Question 10.1", "kind": "Proportionality theorem", "marks": 6,
     "lead": REASONS + " In the diagram, △RST is drawn. Line AB intersects RS and RT at A and B respectively such that AB ∥ ST.",
     "figure": fig("Q10.1", "Triangle RST with R at the top, S at the bottom left and T at the bottom right. A lies on RS and B on RT; AB and "
                   "ST are marked parallel (arrows)."), "items": q101},
    {"id": "10.2", "title": "Question 10.2", "kind": "Proportion in a circle", "marks": 9,
     "lead": REASONS + " In the diagram, O is the centre of the circle. △PWS is drawn with P, W and S on the circle. OR ⊥ PS. PRS is produced "
             "to T. SW and OT intersect at V. OV : OT = 1 : 4",
     "figure": fig("Q10.2", "A circle with centre O; P at the top and W at the bottom, PW passing through O. S is on the circle to the right of "
                   "P; chord PS is produced beyond S to T, outside the circle on the right. R lies on PS with OR ⊥ PS (the right angle marked "
                   "at R). Chord SW is drawn, and OT cuts SW at V."), "items": q102},
    {"id": "11", "title": "Question 11", "kind": "Tangent circles and similar triangles", "marks": 20,
     "lead": REASONS + " In the diagram, A, B, G and F lie on the larger circle. A smaller circle is drawn to touch the larger circle internally "
             "at A. EA is a common tangent to both circles. EBCF is a tangent to the smaller circle at C. AC is produced to G. AF cuts the "
             "smaller circle at D. AB, CD and GF are drawn.",
     "figure": fig("Q11", "A larger circle through A (upper left), F (right), G (bottom) and B (left), and a smaller circle inside it touching "
                   "it at A. EA touches both circles at A, E outside on the left. The line EBCF touches the smaller circle at C and cuts the "
                   "larger circle at B and F. AC produced meets the larger circle at G; AF cuts the smaller circle at D. AB, CD and GF are "
                   "drawn. Angles: at A, 1 between AE and AB, 2 between AB and AC, 3 between AC and AF; at B, 1 and 2 either side of BA; at C, "
                   "1 between CB and CA, 2 between CA and CD, 3 between CD and CF, 4 between CF and CG; at D, 1 and 2 either side of DC; at "
                   "F, 1 between FA and FC, 2 between FC and FG."), "items": q11},
]

AUTHORED = ["3.3", "4.3", "4.4", "4.6", "5.2", "6.1.1", "6.1.2", "7.2", "7.4", "9.2", "10.1", "10.2.1", "11.1", "11.2", "11.3", "11.4"]
paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": "3.3", "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): " + ", ".join(AUTHORED) + " ask for written "
                                                 "working or an answer a word marker cannot read (an interval, an expression in p, a general "
                                                 "solution, a 'show that', a derivation, a proof); each is played as four options, the memo's "
                                                 "answer or first method and three built from common errors, and keeps its marks (63 marks, "
                                                 "all or nothing)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from the page IMAGES: the question "
                                                           "paper and answer book are scans with no text layer, and the memo's text layer garbles "
                                                           "fractions, roots and diagrams; no API call."},
        {"n": "1", "kind": "no_fit", "detail": "The paper prints the data table ACROSS (the 15 weights in one row, the push-ups in the next); it is "
                                               "typed as 15 rows of (x ; y) pairs, the same data in the same order."},
        {"n": "1.1", "kind": "no_fit", "detail": "Calculations play as steps: each step is the number the memo's method produces, its formula, "
                                                 "substitution and equation marks riding on that number (the phone sees numbers, not working)."},
        {"n": "1.5", "kind": "no_fit", "detail": "The influence on the standard deviation is a term listing the memo's two answers (no influence OR "
                                                 "the standard deviation stays the same) in common phrasings, with 'increases' and 'decreases' "
                                                 "rejected; another wording is marked wrong."},
        {"n": "1.6", "kind": "low_confidence", "detail": "The memo keys the increase as 10 (from (40 ; 6) up to the target (40 ; 16), the line's "
                                                         "15,86 taken as 16 whole push-ups); 9,86 is marked wrong."},
        {"n": "2.1", "kind": "low_confidence", "detail": "Ogive read-offs (2.1 median 65, 2.2 Q₁ 44, 2.3 Q₃ 84 and IQR 40) are keyed as the memo "
                                                         "prints them with a tolerance of half a minute: the memo gives one value and no range, "
                                                         "so a reading of 64 or 66 is marked wrong."},
        {"n": "2.4", "kind": "no_fit", "detail": "Drawings (2.4 box and whisker diagram, 7.3.2 graph of g) are done on paper and self-checked "
                                                 "against the memo's criteria; the answer book's scaled line and grid are described in each "
                                                 "draw's memo."},
        {"n": "2.5", "kind": "no_fit", "detail": "The memo accepts two readings (34 employees, 56,67%; OR 35 employees, 58,33%): each step's "
                                                 "tolerance spans both (34,5 ± 0,51; 57,5 ± 0,84), so a value between them also passes."},
        {"n": "3.2", "kind": "no_fit", "detail": "Line equations (3.2 y = −3/4 x − 27/4, 4.2 y = −1/3 x + 10) play as their numbers m and c, and 7.1's "
                                                 "asymptote x = 90° as k in x = k: the strict term compares letters and digits only, so a sign "
                                                 "would be lost. Coordinates (3.7 A, 4.1 L) play as x and y steps; fractions are typed as decimals "
                                                 "(−3/4 -> −0,75; 1/3 -> 0,33)."},
        {"n": "4.5", "kind": "low_confidence", "detail": "Steps follow the memo's first method (the angles of inclination PÔV and RV̂N); its other "
                                                         "methods (R̂ = 90° with a trig ratio, the cosine rule) reach the same 45° but not the step "
                                                         "values, and are listed in the last step's memo."},
        {"n": "6.2", "kind": "no_fit", "detail": "The equation plays as steps: sin x = −1/3 carries the memo's four method marks (squaring, the "
                                                 "reduction, the factors, both equations; sin x = −3/2 has no solution and is in the step's memo), "
                                                 "then the two solutions 199,47° and 340,53°."},
        {"n": "8.2", "kind": "low_confidence", "detail": "The memo accepts BÊC = 58° OR EB̂C = 32° for one mark; the step asks for BÊC, so a learner "
                                                         "who works with EB̂C must type 58 there. BC follows the memo's cosine-rule route (8,30); "
                                                         "its sine-rule route (8,3) passes the same tolerance."},
        {"n": "9.1", "kind": "no_fit", "detail": "'Calculate, with a reason' an angle (9.1) plays as steps: the R (reason) mark rides on the number; "
                                                 "the reason is in the step's memo."},
        {"n": "11.1", "kind": "low_confidence", "detail": "The memo accepts more than one set of four angles (its OR method reaches Ĉ₁ through "
                                                          "EA = EC [tans from common pt] and Ĉ₁ = EÂG [∠s opp equal sides]); the right option is "
                                                          "its first set, and each wrong option changes one line (a wrong reason or a wrong angle)."},
    ],
}
out = Path(__file__).parent / "out" / "math-p2-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper, memo and answer book PDFs' page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")


def shape(o):
    """(lines, trailing [reasons]): every option of one part must match, so the layout never points at the answer."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


QTOTAL = {"1": 10, "2": 10, "3": 19, "4": 20, "5": 12, "6": 18, "7": 11, "8": 9, "9": 6, "10": 15, "11": 20}   # the paper's [n] per question
per_q, at = {}, []
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    for i in m["items"]:
        if i["t"] == "mcq":
            assert len({shape(o) for o in i["opts"]}) == 1, (i["n"], [shape(o) for o in i["opts"]])
            assert len(set(i["opts"])) == len(i["opts"]), (i["n"], "two options are the same")
            at.append("ABCD"[i["a"]])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
assert sorted(i["n"] for m in missions for i in m["items"] if i["t"] == "mcq") == sorted(AUTHORED)
print("right options:", {k: at.count(k) for k in "ABCD"})
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
