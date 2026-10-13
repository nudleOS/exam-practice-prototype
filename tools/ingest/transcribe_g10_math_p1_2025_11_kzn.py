"""Grade 10 Mathematics P1 November 2025 (KwaZulu-Natal Department of Education; the pages are headed 'DBE/November 2025'), the whole
paper (Questions 1 to 7, 100 marks), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks,
answers and the memo's working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md):
re-published by Stanmore Secondary (stanmorephysics.com) as one scanned PDF, the question paper (pages 1-8, with the information sheet)
then the marking guideline (pages 9-18), no text layer: read from its page images (100 dpi). Split into '<id> QP.pdf' and
'<id> MG.pdf' (scratch prov/split.py) for ingest.

  python tools/ingest/transcribe_g10_math_p1_2025_11_kzn.py
  python tools/ingest/ingest.py "uploads/provincial/g10-math-p1-2025-11-kzn/g10-math-p1-2025-11-kzn QP.pdf" "uploads/provincial/g10-math-p1-2025-11-kzn/g10-math-p1-2025-11-kzn MG.pdf" --id g10-math-p1-2025-11-kzn --from-json

The memo's shapes map by the Grade 12 rulings (provincial.py). The sketch of m (6.2) is built on a grid (both x-intercepts, the turning
point, the shape); the Venn diagram 7.2.1 is built (x in the overlap, 42 − x and 35 − x, 38 outside); 5.2 ('sketch p from its
properties': a > 0, 0 < b < 1, q < 0) has no single right curve, so it plays as pick the drawing (pictures_lower.py: expo_graph).
The scan carries the re-publisher's watermark over the figures. Figure boxes in PDF points (page 612 x 792), measured on the page
images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-math-p1-2025-11-kzn", 612.0, 792.0, {
    "Q4": [5, 80, 150, 523, 340], "Q5": [6, 182, 181, 438, 420]}, start=2)
work, answer, num, draw = P.work, P.answer, P.num, P.draw

# ---- QUESTION 1, the question paper page 3 and the memo pages 10-11 ----
F13 = "= {2010 × (2013 + 3)(2013 − 3) × 2012}/{2016 × (2011 + 1)(2011 − 1)}\n"
q11 = [
    work("1.1.1", "(2x − 3)(2x + 3)", 2, [
        "= 4x² + 6x − 6x − 9\n= 4x² − 9",       # the memo
        "= 4x² − 6x + 6x + 9\n= 4x² + 9",       # the signs of the last product
        "= 4x² − 6x − 6x − 9\n= 4x² − 12x − 9", # both middle terms negative
        "= 2x² + 6x − 6x − 9\n= 2x² − 9"],      # 2x × 2x as 2x²
        ["Multiply each term in the first bracket by each term in the second.", "What happens to the two middle terms?"]),
    work("1.1.2", "−5x(2x − 1)² + 3", 3, [
        "= −5x(4x² − 4x + 1) + 3\n= −20x³ + 20x² − 5x + 3",     # the memo
        "= −5x(4x² + 1) + 3\n= −20x³ − 5x + 3",                 # (2x − 1)² as 4x² + 1
        "= −5x(4x² − 4x + 1 + 3)\n= −20x³ + 20x² − 20x",        # the 3 put inside the bracket
        "= −5x(4x² − 4x + 1) + 3\n= −20x³ − 20x² − 5x + 3"],    # −5x × −4x taken as negative
        ["Square the bracket first.", "Then multiply every term by −5x; the + 3 stays outside."]),
    work("1.1.3", "((2ˣ)³ · 27ˣ)/(8ˣ · (3²)ˣ · 3ˣ)", 3, [
        "= {2³ˣ · 3³ˣ}/{2³ˣ · 3²ˣ · 3ˣ}\n= 2⁰ × 3⁰\n= 1",                         # the memo
        "= {2³ˣ · 3³ˣ}/{2³ˣ · 3^(2 + x) · 3ˣ}\n= 2⁰ × 3^(x − 2)\n= 3^(x − 2)",     # (3²)ˣ as 3^(2 + x)
        "= {2³ˣ · 3³ˣ}/{2^(x + 3) · 3²ˣ · 3ˣ}\n= 2^(2x − 3) × 3⁰\n= 2^(2x − 3)",   # 8ˣ as 2^(x + 3)
        "= {2³ˣ · 3³ˣ}/{2³ˣ · 3²ˣ · 3ˣ}\n= 2⁰ × 3⁰\n= 0"],                        # a power of 0 taken as 0
        ["Write every base as a power of 2 or 3.", "What is any number to the power 0?"])]
q12 = [
    answer("1.2.1", "2p² − p − 15", 2, ["(2p + 5)(p − 3)", "(2p − 5)(p + 3)", "(2p + 3)(p − 5)", "(2p − 3)(p + 5)"],
           ["Which factors of 2 × (−15) = −30 add to −1?", "Check by expanding."]),
    work("1.2.2", "y − b + by − 1", 3, [
        "= y − 1 + by − b\n= (y − 1) + b(y − 1)\n= (y − 1)(1 + b)",      # the memo
        "= y − 1 + by − b\n= (y − 1) − b(y − 1)\n= (y − 1)(1 − b)",      # the sign of b
        "= y + by − b − 1\n= y(1 + b) − 1(b + 1)\n= (1 + b)(y + 1)",     # the sign in the second factor
        "= y − 1 + by − b\n= (y − 1) + b(y − 1)\n= b(y − 1)"],           # the 1 lost from (1 + b)
        ["Group the terms in pairs that share a factor.", "What common bracket appears?"]),
    work("1.2.3", "5m³ − 40", 3, [
        "= 5(m³ − 8)\n= 5(m − 2)(m² + 2m + 4)",      # the memo
        "= 5(m³ − 8)\n= 5(m − 2)(m² − 2m + 4)",      # the sum's middle sign
        "= 5(m³ − 8)\n= 5(m − 2)(m² + 4)",           # the middle term left out
        "= 5(m³ − 8)\n= 5(m − 2)³"],                 # a difference of cubes as a cube
        ["Take out the common factor first.", "m³ − 8 is a difference of two cubes."]),
    work("1.3", "Calculate the value of the following, WITHOUT the use of a calculator:\n(2010 × (2013² − 9) × 2012)/(2016 × (2011² − 1))", 4, [
        F13 + "= {2010 × 2016 × 2010 × 2012}/{2016 × 2012 × 2010}\n= 2010",                                                            # the memo
        F13 + "= {2010 × 2016 × 2010 × 2012}/{2016 × 2012 × 2010}\n= 1",                                                               # all cancelled
        F13 + "= {2010 × 2016 × 2010 × 2012}/{2016 × 2012 × 2010}\n= 2010²",                                                           # too few cancelled
        "= {2010 × (2013 + 3)(2013 − 3) × 2012}/{2016 × (2011 − 1)(2011 − 1)}\n= {2010 × 2016 × 2010 × 2012}/{2016 × 2010 × 2010}\n"
        "= 2012"],                                                                                                                    # 2011² − 1 as (2011 − 1)²
        ["2013² − 9 and 2011² − 1 are differences of two squares.", "What cancels?"])]

# ---- QUESTION 2, the question paper page 4 and the memo pages 11-12 ----
LCD = "LCD = x(x − 5); x ≠ 0, x ≠ 5\n"
q21 = [
    work("2.1.1", "2^(3x − 4) = 1/512", 3, [
        "2^(3x − 4) = 2⁻⁹\n3x − 4 = −9\nx = −{5}/{3}",      # the memo
        "2^(3x − 4) = 2⁹\n3x − 4 = 9\nx = {13}/{3}",        # the negative exponent lost
        "2^(3x − 4) = 2⁻⁹\n3x − 4 = −9\nx = −{13}/{3}",     # 4 moved without its sign change
        "2^(3x − 4) = 2⁻⁸\n3x − 4 = −8\nx = −{4}/{3}"],     # 512 as 2⁸
        ["Write 1/512 as a power of 2.", "512 = 2⁹."]),
    work("2.1.2", "4/(x − 5) − 10/x = 2/(x² − 5x)", 4, [
        LCD + "4x − 10(x − 5) = 2\n−6x = −48\nx = 8",       # the memo
        LCD + "4x − 10x − 5 = 2\n−6x = 7\nx = −{7}/{6}",    # 10 not multiplied into −5
        LCD + "4x − 10x − 50 = 2\n−6x = 52\nx = −{26}/{3}", # −10 × −5 taken as −50
        LCD + "4(x − 5) − 10x = 2\n−6x = 22\nx = −{11}/{3}"],   # the numerators crossed
        ["x² − 5x = x(x − 5) is the common denominator.", "Multiply every term by it."])]
EQ = "x + y = 20 and 20x + 12y = 320\n"
q22 = [
    work("2.2", "At a school event, tickets are sold at two different prices: R20 for adults and R12 for learners. A total of 20 tickets were "
         "sold, collecting R320 in total. How many adult tickets and learner tickets were sold? Let the number of adult tickets be x and the "
         "number of learner tickets be y.", 6, [
        EQ + "y = 20 − x\n20x + 12(20 − x) = 320\n8x = 80\nx = 10 adult and y = 10 learner tickets",           # the memo
        EQ + "y = 20 − x\n20x + 12(20 − x) = 320\n32x = 80\nx = 2,5 adult and y = 17,5 learner tickets",       # −12x taken as +12x
        EQ + "y = 20 − x\n20x + 12(20 − x) = 320\n8x = 560\nx = 70 adult and y = −50 learner tickets",         # 240 added, not subtracted
        EQ + "y = x − 20\n20x + 12(x − 20) = 320\n32x = 560\nx = 17,5 adult and y = −2,5 learner tickets"],    # y made the subject wrongly
        ["One equation counts tickets; the other counts rands.", "Make y the subject of the first and substitute."])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 12-13 ----
q3 = [
    num("3.1.1", "The nᵗʰ term of an arithmetic sequence is given as Tₙ = 7n − 3. Determine the first term of the sequence.", 4, 0, "",
        ["Put n = 1.", "7(1) − 3."]),
    work("3.1.2", "Which term is equal to 683?", 3, [
        "683 = 7n − 3\n686 = 7n\nn = 98",           # the memo
        "683 = 7n − 3\n680 = 7n\nn = 97,14",        # 3 subtracted, not added
        "Tₙ = 7(683) − 3\n= 4 778\nn = 4 778",      # 683 put in for n
        "683 = 7n − 3\n686 = 7n\nn = 4 802"],       # multiplied, not divided
        ["Is 683 a position or a value?", "Set 7n − 3 equal to 683."], after=["3.1.1"]),
    answer("3.2.1", "A Grade 10 learner wrote the word WHEAT over and over again: WHEATWHEATWHEAT… Write down the 30th letter.", 1,
           ["T", "W", "A", "E"], ["Each repeat has 5 letters.", "30 is a multiple of 5."]),
    work("3.2.2", "Determine the 508th letter.", 3, [
        "{508}/{5} = 101,6\n0,6 × 5 = 3, the 3rd letter\nE",       # the memo
        "{508}/{5} = 101,6\nThe remainder is 6, the 1st letter\nW", # the decimal read as the remainder
        "{508}/{4} = 127\nNo remainder, the last letter\nT",       # 4 letters in a repeat
        "{508}/{5} = 101,6\n0,6 × 5 = 3, the 4th letter\nA"],      # the letter after the remainder
        ["How many letters are left after 101 complete repeats?", "W, H, E, A, T."]),
    work("3.2.3", "The first H is in the second position, the second H is in the seventh position, the third H is in the twelfth position, and "
         "so forth. Determine in which position the 103rd H is.", 3, [
        "Tₙ = 5n − 3\nT₁₀₃ = 5(103) − 3\n= 512",     # the memo
        "Tₙ = 5n + 2\nT₁₀₃ = 5(103) + 2\n= 517",     # the constant from T₁ = 7
        "Tₙ = 2n\nT₁₀₃ = 2(103)\n= 206",             # the first position as the difference
        "Tₙ = 5n\nT₁₀₃ = 5(103)\n= 515"],            # no constant
        ["The positions are 2 ; 7 ; 12 ; …", "What is the common difference, and T₁?"]),
    work("3.3", "Consider the number pattern: −3 × 1 ; −7 × 4 ; −11 × 7 ; −15 × 10. Determine the 62nd term of the above pattern.", 4, [
        "Tₙ = (−4n + 1)(3n − 2)\nT₆₂ = [−4(62) + 1][3(62) − 2]\n= −247 × 184\n= −45 448",        # the memo
        "Tₙ = (−4n − 1)(3n + 1)\nT₆₂ = [−4(62) − 1][3(62) + 1]\n= −249 × 187\n= −46 563",        # the constants of each factor
        "Tₙ = (−3n)(3n − 2)\nT₆₂ = [−3(62)][3(62) − 2]\n= −186 × 184\n= −34 224",                 # the first factor's difference
        "Tₙ = (−4n + 1)(3n − 2)\nT₆₂ = [−4(62) + 1] + [3(62) − 2]\n= −247 + 184\n= −63"],        # the factors added
        ["Find a formula for each factor separately.", "Then multiply them."])]

# ---- QUESTION 4, the question paper page 5 and the memo pages 13-14 ----
q4 = [
    work("4.1", "Calculate the total amount Amanda will have after 2 years if she chooses the 2nd option.", 2, [
        "A = 8 000(1 + 0,055)²\n= R8 904,20",      # the memo
        "A = 8 000(1 + 2 × 0,055)\n= R8 880",      # simple interest
        "A = 8 000(1 + 0,55)²\n= R19 220",         # 5,5% as 0,55
        "A = 8 000(1 − 0,055)²\n= R7 144,20"],     # depreciation formula
        ["Option 2 is compound interest.", "A = P(1 + i)ⁿ."]),
    work("4.2", "Which option gives Amanda a better return after 2 years? Show calculations to support your answer.", 3, [
        "A = 8 000(1 + 2 × 0,06)\n= R8 960\nR8 960 > R8 904,20, so option 1",       # the memo
        "A = 8 000(1 + 0,06)²\n= R8 988,80\nR8 988,80 > R8 904,20, so option 1",    # option 1 compounded
        "A = 8 000(1 + 0,06)\n= R8 480\nR8 480 < R8 904,20, so option 2",           # one year only
        "A = 8 000 × 2 × 0,06\n= R960\nR960 < R8 904,20, so option 2"],             # the interest compared with an amount
        ["Option 1 is simple interest for 2 years.", "Compare the two final amounts."], after=["4.1"]),
    work("4.3", "If the exchange rate is £1 = R22,50, how many British pounds (£) will she have after 2 years if she chooses the better option?", 2, [
        "R8 960 ÷ 22,50\n= £398,22",          # the memo
        "R8 960 × 22,50\n= £201 600",         # multiplied
        "R8 904,20 ÷ 22,50\n= £395,74",       # the other option's amount
        "22,50 ÷ R8 960\n= £0,0025"],         # upside down
        ["Each pound costs R22,50.", "Divide the rands by 22,50."], after=["4.2"]),
    work("4.4", "Suppose instead she wants to use option 1, but save monthly. If the bank lets her save a fixed amount every month for 2 years "
         "and she wants a total of R9 000, calculate the fixed monthly payment. (Assume the interest is only calculated on the total of all "
         "deposits at the end of 2 years.)", 3, [
        "9 000 = P(1 + 2 × 0,06)\nP = R8 035,71\nMonthly payment = {8 035,71}/{24} = R334,82",     # the memo
        "9 000 = P (the interest ignored)\nP = R9 000\nMonthly payment = {9 000}/{24} = R375",     # no interest
        "9 000 = P(1 + 2 × 0,06)\nP = R8 035,71\nMonthly payment = {8 035,71}/{2} = R4 017,86",    # ÷ years, not months
        "9 000 = P(1 + 24 × 0,06)\nP = R3 688,52\nMonthly payment = {3 688,52}/{24} = R153,69"],   # n in months
        ["Find the total she must deposit, P, first.", "How many months are in 2 years?"])]

# ---- QUESTION 5, the question paper pages 6-7 and the memo pages 14-16 ----
A0 = "0 = −{2}/{x} − 1\n"
q5 = [
    answer("5.1.1(a)", "Write down the y-coordinate of E.", 1, ["−1", "1", "−2", "0"], ["E is the y-intercept of g.", "What is g(0)?"]),
    answer("5.1.1(b)", "Write down the equation of the vertical asymptote of f.", 1, ["x = 0", "y = 0", "y = −1", "x = −1"],
           ["f(x) = −2/x − 1 is undefined where?", "A vertical line: x = …"]),
    work("5.1.2", "Determine the coordinates of B.", 2, [
        "0 = −2x − 1\nB(−{1}/{2} ; 0)",       # the memo
        "0 = −2x − 1\nB({1}/{2} ; 0)",        # the sign lost
        "0 = −2x − 1\nB(0 ; −1)",             # the y-intercept
        "0 = −2x − 1\nB(−2 ; 0)"],            # f's x-intercept
        ["B is the x-intercept of g.", "Set g(x) = 0."]),
    work("5.1.3", "Calculate the length of AB.", 4, [
        A0 + "x = −2, A(−2 ; 0)\nAB = −{1}/{2} − (−2)\n= 1,5 units",               # the memo
        A0 + "x = 2, A(2 ; 0)\nAB = 2 − (−{1}/{2})\n= 2,5 units",                  # the sign of x
        A0 + "x = −2, A(−2 ; 0)\nAB = −{1}/{2} + (−2)\n= −2,5 units",              # added, not subtracted
        A0 + "x = −{1}/{2}, A(−{1}/{2} ; 0)\nAB = −{1}/{2} − (−{1}/{2})\n= 0 units"],  # g's intercept for f's
        ["A is the x-intercept of f.", "AB is the difference of the x-coordinates."], after=["5.1.2"]),
    work("5.1.4", "Determine the coordinates of C and D.", 5, [
        "−{2}/{x} − 1 = −2x − 1\n−2 = −2x²\nx² − 1 = 0\nx = −1 or x = 1\nC(−1 ; 1) and D(1 ; −3)",      # the memo
        "−{2}/{x} − 1 = −2x − 1\n−2 = −2x²\nx² − 1 = 0\nx = −1 or x = 1\nC(−1 ; −3) and D(1 ; 1)",      # the y-values swapped
        "−{2}/{x} − 1 = −2x − 1\n−2 = −2x\nx = 1\nx = 1 only\nD(1 ; −3) only",                          # not multiplied by x
        "−{2}/{x} − 1 = −2x − 1\n−2 = 2x²\nx² + 1 = 0\nNo real x\nThe graphs do not meet"],             # the sign of −2x²
        ["Set f(x) = g(x).", "Multiply both sides by x."]),
    answer("5.1.5(a)", "Determine the value(s) of x for which f is increasing.", 1, ["x ∈ ℝ, x ≠ 0", "x > 0 only", "x < 0 only", "x > −1"],
           ["Follow both branches of f from left to right.", "Do they both rise?"]),
    answer("5.1.5(b)", "Determine the value(s) of x for which g(x)/f(x) ≤ 0.", 3,
           ["x < −2 or −{1}/{2} ≤ x < 0", "−2 < x ≤ −{1}/{2}", "x ≤ −2 or −{1}/{2} ≤ x ≤ 0", "x < −2 or x > 0"],
           ["Where do g and f have opposite signs?", "f is undefined at 0 and zero at −2: can x be −2?"], after=["5.1.3"]),
    answer("5.1.6", "If h(x) = f(−x) + 3, describe in words the transformation from f to h.", 2,
           ["A reflection about the y-axis, then a shift 3 units up", "A reflection about the x-axis, then a shift 3 units up",
            "A reflection about the y-axis, then a shift 3 units down", "A shift 3 units to the left"],
           ["f(−x) changes the sign of x.", "+ 3 outside moves the graph vertically."]),
    draw("5.2", "Use the following properties to sketch the graph of p if p(x) = a × bˣ + q:\n• a > 0\n• 0 < b < 1\n• q < 0", 3, [
        ["Shape: a decreasing function", 1], ["The intercepts with the axes", 1], ["A horizontal asymptote below the x-axis", 1]],
        ["0 < b < 1: does the curve rise or fall?", "q < 0: where is the asymptote?"],
        memo="The memo's sketch: a decreasing exponential curve above a dashed horizontal asymptote below the x-axis; it accepts the curve "
             "cutting both axes, or passing through the origin.")]

# ---- QUESTION 6, the question paper page 7 and the memo page 17 ----
q6 = [
    work("6.1", "Determine the x-intercepts of m.", 2, [
        "0 = −2x² + 8\nx² = 4\nx = −2 or x = 2",       # the memo
        "0 = −2x² + 8\nx² = −4\nNo x-intercepts",       # 8 moved without its sign change
        "0 = −2x² + 8\nx² = 4\nx = 2 only",             # the negative root lost
        "0 = −2x² + 8\nx² = 16\nx = −4 or x = 4"],      # divided by 2 the wrong way
        ["Set m(x) = 0.", "Square roots have two signs."]),
    draw("6.2", "Sketch the graph of m.", 3, [
        ["The turning point (0 ; 8)", 1], ["Both x-intercepts (−2 ; 0) and (2 ; 0)", 1], ["Shape: concave down", 1]],
        ["Where does m cut the axes?", "a = −2: which way does it open?"],
        memo="The memo's sketch: a parabola opening downwards with its turning point (0 ; 8) and x-intercepts −2 and 2.", after=["6.1"],
        # built on a grid (2026-10-13): both x-intercepts are one criterion (one carries its mark); the turning point and the shape each one
        build={"kind": "sketch", "family": "parabola", "x": [-3, 3, 1], "y": [-10, 9, 1], "features": [
            {"id": "tp", "kind": "point", "label": "turning point", "at": [0, 8], "tol": 0, "marks": 1, "crit": 0, "turn": True},
            {"id": "x1", "kind": "point", "label": "x-intercept", "at": [-2, 0], "tol": 0, "marks": 1, "crit": 1},
            {"id": "x2", "kind": "point", "label": "x-intercept", "at": [2, 0], "tol": 0, "marks": 0, "crit": 1}],
               "shape": {"label": "Shape", "answer": "∩", "marks": 1, "crit": 2}}),
    answer("6.3", "Determine the value(s) of k for which m(x) = k will have no solution.", 1, ["k > 8", "k < 8", "k ≥ 8", "k > −8"],
           ["The highest point of m is 8.", "A horizontal line above it never meets m."], after=["6.2"]),
    work("6.4", "Determine the maximum value of 3^(m(x) − 5).", 2, [
        "Max m(x) = 8, so 8 − 5 = 3\n3³ = 27",          # the memo
        "Max m(x) = 8, so 8 − 5 = 3\n3 × 3 = 9",        # the power as a product
        "Max m(x) = 2, so 2 − 5 = −3\n3⁻³ = {1}/{27}",  # an x-intercept as the maximum
        "Max m(x) = 8\n3⁸ − 5 = 6 556"],                # 5 subtracted after the power
        ["The power is largest when m(x) is largest.", "What is the maximum of m?"])]

# ---- QUESTION 7, the question paper page 7 and the memo page 18 ----
q71 = [
    work("7.1.1", "If P(D) = 0,25 ; P(K) = 0,5 and P(D or K) = 0,625, calculate P(D and K).", 2, [
        "P(D and K) = 0,25 + 0,5 − 0,625\n= 0,125",     # the memo
        "P(D and K) = 0,25 + 0,5 + 0,625\n= 1,375",     # added
        "P(D and K) = 0,625 − 0,25\n= 0,375",           # P(K) left out
        "P(D and K) = 0,25 + 0,5\n= 0,75"],             # the overlap ignored
        ["P(D or K) = P(D) + P(K) − P(D and K).", "Make P(D and K) the subject."]),
    answer("7.1.2", "Are events D and K complementary? Give a reason.", 2,
           ["No, since P(D and K) ≠ 0 and P(D) + P(K) ≠ 1", "Yes, since P(D and K) ≠ 0", "Yes, since P(D) + P(K) < 1",
            "No, since P(D or K) > P(D)"],
           ["Complementary events cannot happen together and add up to 1.", "Check both."], after=["7.1.1"])]
q72 = [
    draw("7.2.1", "Draw a Venn diagram to represent the above information.", 3, [
        ["x in the intersection", 1], ["42 − x and 35 − x", 1], ["38 outside the circles", 1]],
        ["x learners do both: what is left of the 42 in Maths?", "Where do the 38 who do neither go?"],
        memo="The memo's Venn diagram: circles M and LO in a rectangle, 42 − x in M only, x in both, 35 − x in LO only and 38 outside.",
        # built (2026-10-13): the learner fills each region, the overlap with the unknown x, as the memo's diagram
        build={"kind": "venn", "sets": [{"id": "M", "name": "Maths"}, {"id": "L", "name": "Life Orientation"}], "outside": True, "unknown": "x",
               "regions": [{"in": "ML", "at": "x", "crit": 0}, {"in": "M", "at": "42 − x", "crit": 1}, {"in": "L", "at": "35 − x", "crit": 1},
                           {"in": "out", "at": 38, "crit": 2}]}),
    work("7.2.2", "Determine the number of learners who participated in both subjects.", 2, [
        "42 − x + x + 35 − x + 38 = 100\nx = 15",       # the memo
        "42 + x + 35 + 38 = 100\nx = −15",              # the totals put in the only-regions
        "42 − x + 35 − x + 38 = 100\nx = 7,5",          # the overlap left out
        "42 − x + x + 35 − x = 100\nx = −23"],          # the 38 left out
        ["All the regions add up to 100.", "Which regions contain x?"], after=["7.2.1"]),
    answer("7.2.3(a)", "Determine the probability that a learner selected at random participates in neither Maths nor LO.", 1,
           ["{38}/{100}", "{62}/{100}", "{15}/{100}", "{27}/{100}"], ["Neither is outside both circles.", "Out of 100."]),
    answer("7.2.3(b)", "Determine the probability that a learner selected at random participates in Maths or LO.", 1,
           ["{62}/{100}", "{77}/{100}", "{38}/{100}", "{47}/{100}"], ["Everyone except the 38.", "Do not count the overlap twice."],
           after=["7.2.2"]),
    answer("7.2.3(c)", "Determine the probability that a learner selected at random participates in Maths only.", 1,
           ["{27}/{100}", "{42}/{100}", "{15}/{100}", "{20}/{100}"], ["Maths only is 42 − x.", "x = 15."], after=["7.2.2"])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Algebraic expressions", "marks": 8, "lead": "Simplify the following completely:", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Factorisation", "marks": 12, "lead": "Factorise the following expressions fully:", "items": q12},
    {"id": "2.1", "title": "Question 2.1", "kind": "Equations", "marks": 7, "lead": "Solve for x without using a calculator:", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Simultaneous equations", "marks": 6, "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Number patterns", "marks": 15, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Finance", "marks": 10,
     "lead": "Amanda is planning a trip to England in 2 years. She considers two different ways to save her money.\nOption 1: She invests R8 000 "
             "at 6% per annum simple interest for 2 years.\nOption 2: She invests R8 000 at 5,5% per annum compound interest for 2 years.",
     "figure": P.fig("Q4", "Two shapes side by side: Option 1, R8 000 at 6% per annum simple interest for 2 years; Option 2, R8 000 at 5,5% "
                           "per annum compound interest for 2 years."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Functions", "marks": 22,
     "lead": "Sketched below are the graphs of f(x) = −2/x − 1 and g(x) = −2x − 1. Points A and B are x-intercepts of f and g respectively. E is "
             "the y-intercept of g. C and D are the points of intersection of f and g.",
     "figure": P.fig("Q5", "The hyperbola f with a dashed horizontal asymptote below the x-axis: one branch top left through C and A on the "
                           "x-axis, the other bottom right through D. The straight line g falls from the top left through C, B on the x-axis, "
                           "E on the y-axis and D."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Parabola", "marks": 8, "lead": "Given: m(x) = −2x² + 8", "items": q6},
    {"id": "7.1", "title": "Question 7.1", "kind": "Probability", "marks": 4, "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Venn diagrams", "marks": 8,
     "lead": "A survey was conducted among 100 learners to determine their participation in two subjects: Maths (M) and Life Orientation (LO).\n"
             "• 42 learners participate in Maths.\n• 35 learners participate in Life Orientation.\n• x learners participate in both subjects.\n"
             "• 38 learners did not participate at all.", "items": q72}]

P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2025", "total_marks": 100, "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "6.2", "kind": "no_fit", "detail": "The sketch of m (6.2) is BUILT on a grid and the Venn diagram (7.2.1) is built with x in the "
                                                   "overlap. 5.2 ('sketch p from its properties') has no single right curve, so it plays as pick "
                                                   "the drawing: the memo's kind of curve and three that break one property."},
          {"n": "5.1.1(a)", "kind": "figure_unclear", "detail": "The paper is a scan re-published by stanmorephysics.com; its watermark sits over "
                                                                "parts of the figures (Q4, Q5) but no label is hidden."}],
         {"1": 20, "2": 13, "3": 15, "4": 10, "5": 22, "6": 8, "7": 12}, 100,
         {"3.1.2": ["3.1.1"], "4.2": ["4.1"], "4.3": ["4.2"], "5.1.3": ["5.1.2"], "5.1.5(b)": ["5.1.3"], "6.2": ["6.1"], "6.3": ["6.2"],
          "7.1.2": ["7.1.1"], "7.2.2": ["7.2.1"], "7.2.3(b)": ["7.2.2"], "7.2.3(c)": ["7.2.2"]},
         "Questions 1 to 7 (the whole paper)")
