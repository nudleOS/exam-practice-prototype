"""Grade 11 Mathematics P1 November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 9, 150 marks,
3 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): ecexams.co.za, 2025_November_Gr_11_Exams, the question paper zip (English PDF, 11 pages; its graphs are
images) and the memo PDF (English and Afrikaans, 21 pages), read from their page images at 90 dpi.

  python tools/ingest/transcribe_g11_math_p1_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-math-p1-2025-11-ec/MATHS P1 QP GR11 NOV 2025 ENG_watermark.pdf" "uploads/provincial/g11-math-p1-2025-11-ec/MATHS P1 MEMO GR11 NOV 2025 E+A_watermark.pdf" --id g11-math-p1-2025-11-ec --from-json

The memo's shapes map by the Grade 12 rulings (provincial.py). The sketch 7.1.3 is built on a grid whose y-steps are thirds (the
y-intercept is −8/3); the Venn diagram 9.1.2 and the tree diagram 9.3.1 are pick the drawing (pictures_lower.py: the platform
has no Venn or tree builder yet).
Figure boxes in PDF points (page 595 x 842): each graph is one image, its box read from the PDF (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-math-p1-2025-11-ec", 595.3, 841.9, {
    "Q5": [6, 81.4, 161.3, 514.9, 483.8], "Q6": [7, 83.6, 145.1, 484.8, 463.1]}, start=6)
work, answer, num, draw = P.work, P.answer, P.num, P.draw

# ---- QUESTION 1, the question paper page 3 and the memo pages 2-4 ----
QF = "x = {−b ± √(b² − 4ac)}/{2a}\n"
X3 = "x(x − 4) − 2(x − 4) > 0\n(x − 4)(x − 2) > 0\nCritical values: x = 4 or x = 2\n"
SQ = "√(x + 14) = x + 2\nx + 14 = x² + 4x + 4\nx² + 3x − 10 = 0\n"
q11 = [
    answer("1.1.1", "x(2x + 6) = 0", 2, ["x = 0 or x = −3", "x = 0 or x = 3", "x = −3", "x = 0 or x = −6"],
           ["When is a product of two factors zero?", "What does 2x + 6 = 0 give?"]),
    work("1.1.2", "4x² = 9 − 3x (correct to TWO decimal places)", 4, [
        "4x² + 3x − 9 = 0\n" + QF + "x = {−3 ± √((3)² − 4(4)(−9))}/{2(4)}\nx = {−3 ± √153}/{8}\nx = 1,17 or x = −1,92",     # the memo
        "4x² − 3x − 9 = 0\n" + QF + "x = {3 ± √((−3)² − 4(4)(−9))}/{2(4)}\nx = {3 ± √153}/{8}\nx = 1,92 or x = −1,17",       # −3x moved without its sign change
        "4x² + 3x − 9 = 0\nx = {−b ± √(b² − 4ac)}/{a}\nx = {−3 ± √((3)² − 4(4)(−9))}/{4}\nx = {−3 ± √153}/{4}\nx = 2,34 or x = −3,84",  # ÷ a
        "4x² + 3x + 9 = 0\n" + QF + "x = {−3 ± √((3)² − 4(4)(9))}/{2(4)}\nx = {−3 ± √(−135)}/{8}\nNo real roots"],          # 9 moved without its sign change
        ["What does the equation look like in standard form?", "What are a, b and c?"]),
    work("1.1.3", "x(x − 4) + 2(4 − x) > 0", 4, [
        X3 + "x < 2 or x > 4",                                                                                       # the memo
        X3 + "2 < x < 4",                                                                                            # the region between
        "x(x − 4) + 2(x − 4) > 0\n(x − 4)(x + 2) > 0\nCritical values: x = 4 or x = −2\nx < −2 or x > 4",             # 2(4 − x) taken as 2(x − 4)
        X3 + "x ≤ 2 or x ≥ 4"],                                                                                      # the critical values included
        ["How can you write 2(4 − x) so that x − 4 is a common factor?", "Is the parabola above the x-axis between its roots or outside "
                                                                         "them?"]),
    answer("1.1.4(a)", "For which value(s) of x will f(x) be real?", 2, ["x ≥ −14, x ≠ −2", "x > −14, x ≠ −2", "x ≥ −14", "x ≥ 14, x ≠ 2"],
           ["What must be true of the number under a square root?", "Which x-value makes the denominator zero?"]),
    work("1.1.4(b)", "Solve for x, if f(x) = 1", 4, [
        SQ + "(x + 5)(x − 2) = 0\nx = 2 (x ≠ −5)",                                                                   # the memo
        SQ + "(x + 5)(x − 2) = 0\nx = 2 or x = −5",                                                                  # −5 not checked
        "√(x + 14) = x + 2\nx + 14 = x² + 4\nx² − x − 10 = 0\nx = {1 ± √41}/{2}\nx = 3,70 (x ≠ −2,70)",               # (x + 2)² as x² + 4
        SQ + "(x − 5)(x + 2) = 0\nx = 5 (x ≠ −2)"],                                                                  # the signs in the factors swapped
        ["Multiply both sides by x + 2: what do you square?", "Why must each answer be checked in the original equation?"])]
SUB = "x = 3y + 1\n(3y + 1)² − 2y(3y + 1) + 9y² = 17\n"
q12 = [
    work("1.2", "Solve simultaneously for x and y:\nx − 3y = 1\nx² − 2xy + 9y² = 17", 6, [
        SUB + "9y² + 6y + 1 − 6y² − 2y + 9y² − 17 = 0\n12y² + 4y − 16 = 0\n3y² + y − 4 = 0\n(y − 1)(3y + 4) = 0\n"
              "y = 1 or y = −{4}/{3}\nx = 4 or x = −3",                                                                # the memo
        SUB + "9y² + 1 − 6y² − 2y + 9y² − 17 = 0\n12y² − 2y − 16 = 0\n6y² − y − 8 = 0\ny = {1 ± √193}/{12}\n"
              "y = 1,24 or y = −1,07\nx = 4,72 or x = −2,22",                                                          # (3y + 1)² as 9y² + 1
        "x = 3y − 1\n(3y − 1)² − 2y(3y − 1) + 9y² = 17\n9y² − 6y + 1 − 6y² + 2y + 9y² − 17 = 0\n12y² − 4y − 16 = 0\n3y² − y − 4 = 0\n"
        "(3y − 4)(y + 1) = 0\ny = {4}/{3} or y = −1\nx = 3 or x = −4",                                                 # x = 3y − 1
        SUB + "9y² + 6y + 1 − 6y² + 2y + 9y² − 17 = 0\n12y² + 8y − 16 = 0\n3y² + 2y − 4 = 0\ny = {−2 ± √52}/{6}\n"
              "y = 0,87 or y = −1,54\nx = 3,61 or x = −3,61"],                                                         # −2y(3y + 1) as −6y² + 2y
        ["Which equation is easier to make x the subject of?", "After substituting and expanding, what equation in y do you get?"])]
q13 = [
    work("1.3", "Determine the value of x that will satisfy the equation (without the use of a calculator and show all your working)\n"
         "1 + 10/(1 + 1/(1 + 1/x)) = 7", 5, [
        "1 + {1}/{x} = {x + 1}/{x}\n1 ÷ {x + 1}/{x} = {x}/{x + 1}\n1 + {x}/{x + 1} = {2x + 1}/{x + 1}\n10 ÷ {2x + 1}/{x + 1} = {10(x + 1)}/{2x + 1}\n"
        "1 + {10(x + 1)}/{2x + 1} = 7, so {12x + 11}/{2x + 1} = 7\n12x + 11 = 14x + 7\nx = 2",                          # the memo
        "1 + {1}/{x} = {x + 1}/{x}\n1 ÷ {x + 1}/{x} = {x + 1}/{x}\n1 + {x + 1}/{x} = {2x + 1}/{x}\n10 ÷ {2x + 1}/{x} = {10x}/{2x + 1}\n"
        "1 + {10x}/{2x + 1} = 7, so {12x + 1}/{2x + 1} = 7\n12x + 1 = 14x + 7\nx = −3",                                  # the fraction not turned over
        "1 + {1}/{x} = {2}/{x}\n1 ÷ {2}/{x} = {x}/{2}\n1 + {x}/{2} = {x + 2}/{2}\n10 ÷ {x + 2}/{2} = {20}/{x + 2}\n"
        "1 + {20}/{x + 2} = 7, so {x + 22}/{x + 2} = 7\nx + 22 = 7x + 14\nx = {4}/{3}",                                  # 1 + 1/x taken as 2/x
        "1 + {1}/{x} = {x + 1}/{x}\n1 ÷ {x + 1}/{x} = {x}/{x + 1}\n1 + {x}/{x + 1} = {2x + 1}/{x + 1}\n10 ÷ {2x + 1}/{x + 1} = {10(x + 1)}/{2x + 1}\n"
        "1 + {10(x + 1)}/{2x + 1} = 7, so {12x + 11}/{2x + 1} = 7\n12x + 11 = 14x + 1\nx = 5"],                         # 7(2x + 1) as 14x + 1
        ["Start at the bottom: what is 1 + 1/x as one fraction?", "Dividing by a fraction: what do you multiply by instead?"])]

# ---- QUESTION 2, the question paper page 4 and the memo pages 5-6 ----
q21 = [
    work("2.1", "Simplify the following expression:\n(125ˣ · √(5^(4x − 2)))/(∛(5^(12x + 6)) · 5ˣ)", 4, [
        "= {5^(3x) · 5^(2x − 1)}/{5^(4x + 2) · 5ˣ}\n= 5^(3x + 2x − 1 − 4x − 2 − x)\n= 5⁻³\n= {1}/{125}",           # the memo
        "= {5^(2x) · 5^(2x − 1)}/{5^(4x + 2) · 5ˣ}\n= 5^(2x + 2x − 1 − 4x − 2 − x)\n= 5^(−x − 3)\n= {1}/{5^(x + 3)}",   # 125 taken as 5²
        "= {5^(3x) · 5^(2x − 2)}/{5^(4x + 2) · 5ˣ}\n= 5^(3x + 2x − 2 − 4x − 2 − x)\n= 5⁻⁴\n= {1}/{625}",            # only 4x halved
        "= {5^(3x) · 5^(2x − 1)}/{5^(4x + 6) · 5ˣ}\n= 5^(3x + 2x − 1 − 4x − 6 − x)\n= 5⁻⁷\n= {1}/{78 125}"],        # only 12x divided by 3
        ["Write every number as a power of 5: what is 125?", "A square root halves the exponent, a cube root divides it by 3."])]
q22 = [
    work("2.2.1", "6x^(3/2) = 48", 3, [
        "x^(3/2) = 8\nx = (2³)^(2/3)\nx = 2²\nx = 4",              # the memo
        "x^(3/2) = 8\nx = (2³)^(3/2)\nx = 2^(9/2)\nx = 22,63",     # raised to 3/2, not its reciprocal
        "x^(3/2) = 48 − 6\nx^(3/2) = 42\nx = (42)^(2/3)\nx = 12,08",  # 6 subtracted, not divided
        "x^(3/2) = 8\nx = 8 × {2}/{3}\nx = {16}/{3}\nx = 5,33"],    # multiplied by the exponent
        ["What do you do with the 6 first?", "What power undoes x^(3/2)?"]),
    work("2.2.2", "x^(1/2) − 3x^(1/4) + 2 = 0", 4, [
        "Let k = x^(1/4): k² − 3k + 2 = 0\n(k − 2)(k − 1) = 0\nx^(1/4) = 2 or x^(1/4) = 1\nx = 16 or x = 1",        # the memo
        "Let k = x^(1/4): k² − 3k + 2 = 0\n(k − 2)(k − 1) = 0\nx^(1/4) = 2 or x^(1/4) = 1\nx = 1,19 or x = 1",      # 2 raised to 1/4, not 4
        "Let k = x^(1/4): k² − 3k + 2 = 0\n(k + 2)(k + 1) = 0\nx^(1/4) = −2 or x^(1/4) = −1\nNo real solution",      # the signs in the factors
        "Let k = x^(1/4): 2k − 3k + 2 = 0\n−k + 2 = 0\nx^(1/4) = 2\nx = 16"],                                       # x^(1/2) taken as 2x^(1/4)
        ["How is x^(1/2) related to x^(1/4)?", "With k = x^(1/4), what kind of equation do you get?"])]
q23 = [
    work("2.3", "Given: The area of a rectangle is (16ˣ − 100) cm² and the breadth is (4ˣ + 10) cm.\nDetermine the length of the rectangle in "
         "terms of x.", 4, [
        "16ˣ − 100 = L(4ˣ + 10)\nL = {(4ˣ)² − 100}/{4ˣ + 10}\nL = {(4ˣ − 10)(4ˣ + 10)}/{4ˣ + 10}\nL = 4ˣ − 10",                 # the memo
        "16ˣ − 100 = L(4ˣ + 10)\nL = {4ˣ + 10}/{(4ˣ)² − 100}\nL = {4ˣ + 10}/{(4ˣ − 10)(4ˣ + 10)}\nL = {1}/{4ˣ − 10}",          # breadth ÷ area
        "16ˣ − 100 = L(4ˣ + 10)\nL = {(4ˣ)² − 100}/{4ˣ + 10}\nL = {(4ˣ + 10)(4ˣ + 10)}/{4ˣ + 10}\nL = 4ˣ + 10",                 # the factors' signs
        "16ˣ − 100 = {1}/{2}L(4ˣ + 10)\nL = {2((4ˣ)² − 100)}/{4ˣ + 10}\nL = {2(4ˣ − 10)(4ˣ + 10)}/{4ˣ + 10}\nL = 2(4ˣ − 10)"],  # a triangle's area
        ["Area = length × breadth: what is the length?", "How can 16ˣ be written with 4ˣ, and which factorising pattern fits?"])]
q24 = [
    work("2.4", "The difference between the squares of two consecutive integers is 45. Determine the value of the square of the sum of these "
         "two consecutive integers.\nHint: Let the smaller integer be x.", 4, [
        "Smaller x, next x + 1\n(x + 1)² − x² = 45\n2x + 1 = 45, so x = 22\n(22 + 23)² = 2 025",          # the memo
        "Smaller x, next x + 1\n(x + 1)² − x² = 45\n2x + 1 = 45, so x = 22\n22² + 23² = 1 013",            # the sum of the squares
        "Smaller x, next x + 2\n(x + 2)² − x² = 45\n4x + 4 = 45, so x = 10,25\n(10,25 + 12,25)² = 506,25",  # consecutive taken as 2 apart
        "Smaller x, next x + 1\n(x + 1)² − x² = 45\n2x = 45, so x = 22,5\n(22,5 + 23,5)² = 2 116"],        # (x + 1)² as x² + 2x
        ["Write the next integer and expand (x + 1)².", "The question wants the square of the SUM."])]

# ---- QUESTION 3, the question paper page 4 and the memo page 7 ----
q31 = [
    answer("3.1.1", "Write down the next TWO terms in the number pattern.", 2, ["4 ; 3,5", "4,5 ; 4", "3,5 ; 3", "4 ; 3"],
           ["What is the difference between consecutive terms?", "Is the pattern going up or down?"]),
    work("3.1.2", "Calculate the general term of the number pattern, in the form Tₙ = bn + c", 2, [
        "d = 5,0 − 5,5 = −0,5\nTₙ = −0,5n + c, with T₁ = −0,5 + c = 5,5\nTₙ = −0,5n + 6",     # the memo
        "d = 5,0 − 5,5 = −0,5\nTₙ = −0,5n + c, with c = T₁ = 5,5\nTₙ = −0,5n + 5,5",          # the first term taken as c
        "d = 5,5 − 5,0 = 0,5\nTₙ = 0,5n + c, with T₁ = 0,5 + c = 5,5\nTₙ = 0,5n + 5",          # the difference the wrong way round
        "d = 5,0 − 5,5 = −0,5\nTₙ = −0,5n + c, with T₁ = −0,5 + c = 5,5\nTₙ = −0,5n + 5"],     # −0,5 moved without its sign change
        ["What is b, the constant difference?", "Which c makes T₁ = 5,5?"]),
    work("3.1.3", "Which term in the number pattern is the first to be less than −113,5?", 2, [
        "−0,5n + 6 < −113,5\n−0,5n < −119,5\nn > 239, so n = 240",       # the memo
        "−0,5n + 6 < −113,5\n−0,5n < −119,5\nn < 239, so n = 238",       # the sign not turned when dividing by −0,5
        "−0,5n + 6 = −113,5\n−0,5n = −119,5\nn = 239",                    # equal to −113,5, not less
        "−0,5n + 6 < −113,5\n−0,5n < −107,5\nn > 215, so n = 216"],      # 6 added, not subtracted
        ["Which inequality says a term is less than −113,5?", "What happens to the sign when you divide by a negative number?"],
        after=["3.1.2"])]
q32 = [
    work("3.2", "The constant difference of a linear number pattern is 5 and the 38ᵗʰ term is 192.\nDetermine the value of the first term.", 3, [
        "Tₙ = 5n + c\n192 = 5(38) + c, so c = 2\nT₁ = 5(1) + 2 = 7",       # the memo
        "Tₙ = 5n + c\n192 = 5(38) + c, so c = 2\nT₁ = c = 2",               # c taken as the first term
        "Tₙ = 5n + c\n192 = 5(37) + c, so c = 7\nT₁ = 5(1) + 7 = 12",      # 37 for 38
        "Tₙ = 5n + c\n192 = 5(38) + c, so c = 382\nT₁ = 5(1) + 382 = 387"],  # 190 added, not subtracted
        ["What is the general term of a linear pattern with difference 5?", "Use the 38th term to find c, then put n = 1."])]

# ---- QUESTION 4, the question paper page 5 and the memo pages 8-9 ----
TERMS = "T₁ = 21, T₂ = 12, T₃ = 5, T₄ = 0\n"
D45 = "Tₙ − Tₙ₋₁ = 149\nn² − 12n + 32 − (n² − 14n + 45) = 149\n"
q41 = [
    work("4.1.1", "If T₆₂ = 3132, determine the value of k.", 2, [
        "3 132 = (62)² − 12(62) + k\nk = 32",       # the memo
        "3 132 = 2(62) − 12(62) + k\nk = 3 752",    # 62² as 2 × 62
        "3 132 = (62)² + 12(62) + k\nk = −1 456",   # the sign of −12n lost
        "3 132 = (62)² − 12(62) + k\nk = −32"],     # 3 100 moved the wrong way
        ["Put n = 62 into the general term.", "What is 62²?"]),
    work("4.1.2", "Determine the first THREE terms of the first difference number pattern.", 2, [
        TERMS + "First differences: −9 ; −7 ; −5",      # the memo
        TERMS + "First differences: 9 ; 7 ; 5",         # each difference the wrong way round
        TERMS + "First differences: 21 ; 12 ; 5",       # the terms, not their differences
        TERMS + "First differences: −9 ; −16 ; −21"],   # running totals of the differences
        ["Work out the first four terms with k = 32.", "A first difference is a term minus the one before it."], after=["4.1.1"]),
    work("4.1.3", "Calculate the value of n for which the quadratic number pattern will have a minimum.", 2, [
        "n = {−(−12)}/{2(1)}\n= 6",      # the memo
        "n = {−12}/{2(1)}\n= −6",        # the sign of b lost
        "n = {−(−12)}/{1}\n= 12",        # divided by a, not 2a
        "T₆ = 36 − 72 + 32\n= −4"],      # the minimum value, not n
        ["Which formula gives the turning point of an² + bn + c?", "What are a and b here?"]),
    work("4.1.4", "Determine Tₙ₋₁, in terms of n.", 2, [
        "Tₙ₋₁ = (n − 1)² − 12(n − 1) + 32\n= n² − 2n + 1 − 12n + 12 + 32\n= n² − 14n + 45",     # the memo
        "Tₙ₋₁ = (n − 1)² − 12(n − 1) + 32\n= n² − 1 − 12n + 12 + 32\n= n² − 12n + 43",          # (n − 1)² as n² − 1
        "Tₙ₋₁ = (n − 1)² − 12(n − 1) + 32\n= n² − 2n + 1 − 12n − 12 + 32\n= n² − 14n + 21",     # −12(n − 1) as −12n − 12
        "Tₙ₋₁ = (n − 1)² − 12n + 32\n= n² − 2n + 1 − 12n + 32\n= n² − 14n + 33"],              # only n² replaced
        ["Replace every n with n − 1.", "Expand (n − 1)² and −12(n − 1) carefully."], after=["4.1.1"]),
    work("4.1.5", "Between which two consecutive terms of the quadratic number pattern, will the difference be 149?", 3, [
        D45 + "2n − 13 = 149, so n = 81\nBetween T₈₀ and T₈₁",                            # the memo
        "Tₙ = 149\nn² − 12n + 32 = 149\nn² − 12n − 117 = 0, so n = 18,37\nBetween T₁₈ and T₁₉",   # a term set to 149
        D45 + "2n − 13 = 149, so n = 81\nBetween T₈₁ and T₈₂",                            # the wrong pair
        D45 + "2n + 77 = 149, so n = 36\nBetween T₃₅ and T₃₆"],                           # −45 taken as +45
        ["The difference between Tₙ and Tₙ₋₁ is 149: which equation is that?", "If n = 81, which two terms are they?"],
        after=["4.1.4"])]
DIFF = "First differences: 4 − x ; 3x − 4 ; 18 − 3x\n"
q42 = [
    work("4.2", "In a quadratic number pattern, the second term is 4, the third term is three times the first term and the fourth term is "
         "18.\nDetermine the value of T₃", 3, [
        DIFF + "Second differences: 4x − 8 ; −6x + 22\n4x − 8 = −6x + 22, so x = 3\nT₃ = 3x = 9",     # the memo
        DIFF + "Second differences: 4x − 8 ; −6x + 22\n4x − 8 = −6x + 22, so x = 3\nT₃ = 3",          # x given as T₃
        DIFF + "The first differences taken as equal\n4 − x = 3x − 4, so x = 2\nT₃ = 3x = 6",         # equal first differences
        DIFF + "Second differences: 4x − 8 ; −6x + 22\n4x − 8 = −6x + 22, so x = 1,4\nT₃ = 3x = 4,2"],  # 10x = 14
        ["Call the first term x: what are the four terms?", "What must be true of the second differences?"])]

# ---- QUESTION 5, the question paper page 6 and the memo pages 10-12 ----
F5 = "f(x) = {a}/{x − 3} − 1\n2 = {a}/{4 − 3} − 1\n"
q5 = [
    answer("5.1", "Write down the value of p.", 1, ["p = −3", "p = 3", "p = −1", "p = 1"],
           ["Where is f's vertical asymptote?", "x + p = 0 at the vertical asymptote."]),
    work("5.2", "Determine the equation of f.", 3, [
        F5 + "a = 3\nf(x) = {3}/{x − 3} − 1",                                                     # the memo
        "f(x) = {a}/{x − 3} + 1\n2 = {a}/{4 − 3} + 1\na = 1\nf(x) = {1}/{x − 3} + 1",            # the sign of q lost
        "f(x) = {a}/{x + 3} − 1\n2 = {a}/{4 + 3} − 1\na = 21\nf(x) = {21}/{x + 3} − 1",          # the sign of p lost
        F5 + "a = 1\nf(x) = {1}/{x − 3} − 1"],                                                    # −1 moved without its sign change
        ["Which values of p and q does C(3 ; −1) give?", "Which point on f lets you find a?"], after=["5.1"]),
    work("5.3", "Determine the coordinates of A and B.", 3, [
        "−1 = {3}/{3} + c, so c = −2: B(0 ; −2)\n0 = {x}/{3} − 2\nx = 6: A(6 ; 0)",            # the memo
        "−1 = {3}/{3} + c, so c = −2: B(0 ; −2)\n0 = {x}/{3} − 2\nx = {2}/{3}: A({2}/{3} ; 0)",  # divided by 3, not multiplied
        "−1 = {3}/{3} + c, so c = −2: B(−2 ; 0)\n0 = {x}/{3} − 2\nx = 6: A(0 ; 6)",            # the coordinates the wrong way round
        "−1 = 3(3) + c, so c = −10: B(0 ; −10)\n0 = 3x − 10\nx = {10}/{3}: A({10}/{3} ; 0)"],    # x/3 read as 3x
        ["g passes through C: what is c?", "A is on the x-axis and B on the y-axis."]),
    work("5.4", "Write down the domain of h, if h(x) = f[−(x − 4)]", 3, [
        "−(x − 4) − 3 = 0\n−x + 1 = 0, so x = 1\nDomain: x ∈ ℝ, x ≠ 1",       # the memo
        "(x − 4) − 3 = 0\nx − 7 = 0, so x = 7\nDomain: x ∈ ℝ, x ≠ 7",         # the minus sign dropped
        "−x − 4 − 3 = 0\n−x − 7 = 0, so x = −7\nDomain: x ∈ ℝ, x ≠ −7",       # −(x − 4) as −x − 4
        "−(x − 4) − 3 = 0\n−x + 1 = 0, so x = 1\nDomain: y ∈ ℝ, y ≠ −1"],     # the range given
        ["Where is h's denominator zero?", "Replace x in x − 3 with −(x − 4)."], after=["5.2"]),
    answer("5.5", "Determine the value of x, for which f(x) · g(x) < 0", 2, ["3 < x < 6 or x > 6", "x < 3 or x > 6", "3 < x < 6", "0 < x < 6"],
           ["When is a product of two numbers negative?", "Where is f above the x-axis, and where is g?"], after=["5.3"]),
    work("5.6", "Calculate the area of ΔABE if the length AB = 2√10 units.", 5, [
        "m(AB) = {1}/{3}, so θ = 18,43°\nm(EA) = {0 − 2}/{6 − 4} = −1, so EÂO = 45°\nEÂB = 18,43° + 45° = 63,43°\n"
        "EA = √((4 − 6)² + (2 − 0)²) = 2√2\nArea ΔABE = {1}/{2} × 2√2 × 2√10 × sin 63,43°\n= 8 units²",                 # the memo
        "m(AB) = {1}/{3}, so θ = 18,43°\nm(EA) = {0 − 2}/{6 − 4} = −1, so EÂO = 45°\nEÂB = 45° − 18,43° = 26,57°\n"
        "EA = √((4 − 6)² + (2 − 0)²) = 2√2\nArea ΔABE = {1}/{2} × 2√2 × 2√10 × sin 26,57°\n= 4 units²",                 # the angles subtracted
        "m(AB) = {1}/{3}, so θ = 18,43°\nm(EA) = {0 − 2}/{6 − 4} = −1, so EÂO = 45°\nEÂB = 18,43° + 45° = 63,43°\n"
        "EA = √((4 − 6)² + (2 − 0)²) = 2√2\nArea ΔABE = 2√2 × 2√10 × sin 63,43°\n= 16 units²",                          # the ½ left out
        "m(AB) = {1}/{3}, so θ = 18,43°\nm(EA) = {0 − 2}/{6 − 4} = −1, so EÂO = 45°\nEÂB = 18,43° + 45° = 63,43°\n"
        "EA = 2 (the rise only)\nArea ΔABE = {1}/{2} × 2 × 2√10 × sin 63,43°\n= 5,66 units²"],                          # EA taken as 2
        ["Which angle of ΔABE is between AB and AE, and how do the gradients give it?", "Which area rule uses two sides and the angle "
                                                                                        "between them?"], after=["5.3"])]

# ---- QUESTION 6, the question paper page 7 and the memo pages 13-14 ----
G6 = "g(x) = x² + 6x\nCD = g(x) − f(x) = x² + 6x − (−x² − 6x)\n14 = 2x² + 12x\nx² + 6x − 7 = 0\n"
R6 = "−x² − 6x = 0\nx(x + 6) = 0\nx = 0 or x = −6\n"
q6 = [
    work("6.1", "Write down the equation of f in the turning point form, i.e. y = a(x + p)² + q", 3, [
        "a = −1\nx = {−(−6)}/{2(−1)} = −3\nf(−3) = −(−3)² − 6(−3) = 9\nf(x) = −(x + 3)² + 9",     # the memo (its f(−3) line corrected)
        "a = −1\nx = {−(−6)}/{2(−1)} = 3\nf(3) = −(3)² − 6(3) = −27\nf(x) = −(x − 3)² − 27",      # the sign of the turning point's x
        "a = −1\nx = {−(−6)}/{2(−1)} = −3\nf(−3) = −(−3)² − 6(−3) = 9\nf(x) = −(x − 3)² + 9",     # p's sign in the form
        "a = −1\nx = {−(−6)}/{2(−1)} = −3\nf(−3) = (−3)² − 6(−3) = 27\nf(x) = −(x + 3)² + 27"],   # −(−3)² taken as +9
        ["Where is the axis of symmetry of f?", "In y = a(x + p)² + q, how are p and q related to the turning point?"]),
    work("6.2", "Determine the coordinates of A.", 3, [
        "x = −3 (the axis of symmetry)\n{−5 + x(A)}/{2} = −3, so x(A) = −1\nf(−1) = −(−1)² − 6(−1) = 5\nA(−1 ; 5)",     # the memo
        "x = −3 (the axis of symmetry)\n{−5 + x(A)}/{2} = −3, so x(A) = 2\nf(2) = −(2)² − 6(2) = −16\nA(2 ; −16)",     # not doubled
        "x = −3 (the axis of symmetry)\n{−5 + x(A)}/{2} = −3, so x(A) = −1\nf(−1) = (−1)² − 6(−1) = 7\nA(−1 ; 7)",     # −(−1)² as +1
        "x = 0 (the y-axis taken as the axis)\nx(A) = 5\nf(5) = −(5)² − 6(5) = −55\nA(5 ; −55)"],                         # the wrong axis
        ["A and B are the same distance from the axis of symmetry: where is it?", "Once you have A's x-value, use f."], after=["6.1"]),
    work("6.3", "Determine the length of OE if CD = 14 units.", 5, [
        G6 + "(x + 7)(x − 1) = 0\nx = −7 (x ≠ 1), so OE = 7 units",                                                         # the memo
        "g(x) = x² + 6x\nCD = f(x) − g(x) = −x² − 6x − (x² + 6x)\n14 = −2x² − 12x\nx² + 6x + 7 = 0\nx = −3 ± √2\n"
        "x = −4,41 (x ≠ −1,59), so OE = 4,41 units",                                                                       # f − g
        "g(x) = x² − 6x\nCD = g(x) − f(x) = x² − 6x − (−x² − 6x)\n14 = 2x²\nx² = 7\nx = ±√7\nx = −2,65, so OE = 2,65 units",  # g reflected wrongly
        G6 + "(x + 7)(x − 1) = 0\nx = 1, so OE = 1 unit"],                                                                 # the root on the wrong side
        ["What is g, the reflection of f in the x-axis?", "CD is the top graph minus the bottom graph at E."]),
    answer("6.4.1", "f(x) = −x² − 6x + k will have non-real roots.", 2, ["k < −9", "k > −9", "k < 9", "k ≤ −9"],
           ["Where is the turning point of f?", "How far down must f move so that it never meets the x-axis?"]),
    work("6.4.2", "f(x + k) will have two real roots that have different signs.", 3, [
        R6 + "−6 < k < 0",     # the memo
        R6 + "0 < k < 6",      # the shift taken the wrong way
        R6 + "k < −6 or k > 0",  # the outside region
        R6 + "−6 ≤ k ≤ 0"],    # the ends included: a root at 0 has no sign
        ["Where are the roots of f?", "f(x + k) moves the graph k units left: where must the two roots end up?"])]

# ---- QUESTION 7, the question paper page 8 and the memo pages 15-16 ----
Y0 = "y = ({1}/{3})^(0 + 1) − 3 = −{8}/{3}: (0 ; −{8}/{3})"
q71 = [
    answer("7.1.1", "Write down the equation of the asymptote of f", 1, ["y = −3", "y = 3", "x = −3", "y = −1"],
           ["Which number in f moves the graph up or down?", "Is the asymptote of an exponential graph horizontal or vertical?"]),
    work("7.1.2", "Calculate the coordinates of the intercepts of f", 3, [
        "({1}/{3})^(x + 1) − 3 = 0\n({1}/{3})^(x + 1) = ({1}/{3})⁻¹\nx + 1 = −1, so x = −2: (−2 ; 0)\n" + Y0,      # the memo
        "({1}/{3})^(x + 1) − 3 = 0\n({1}/{3})^(x + 1) = ({1}/{3})¹\nx + 1 = 1, so x = 0: (0 ; 0)\n" + Y0,         # 3 written as (1/3)¹
        "({1}/{3})^(x + 1) − 3 = 0\n({1}/{3})^(x + 1) = ({1}/{3})⁻¹\nx + 1 = −1, so x = −2: (−2 ; 0)\n"
        "y = ({1}/{3})⁰ − 3 = −2: (0 ; −2)",                                                                       # the + 1 dropped
        "({1}/{3})^(x + 1) − 3 = 0\n({1}/{3})^(x + 1) = −3\nNo x-intercept\n" + Y0],                               # −3 moved without its sign change
        ["What is y at an x-intercept, and how can 3 be written as a power of 1/3?", "What is x at the y-intercept?"]),
    draw("7.1.3", "Sketch the graph of f. Indicate the horizontal asymptote as well as the intercepts with the axes.", 3, [
        ["Shape: decreasing", 1], ["The x-intercept (−2 ; 0) and the y-intercept (0 ; −8/3)", 1], ["The asymptote y = −3", 1]],
        ["Is f increasing or decreasing?", "Where are its intercepts and its asymptote?"],
        memo="The memo's sketch: f falls from the top left through (−2 ; 0) and (0 ; −2,67) and flattens above the dashed asymptote y = −3.",
        after=["7.1.1", "7.1.2"],
        # built on a grid whose y-steps are thirds, so the y-intercept −8/3 is a grid point (tol 0.01 for its decimals)
        build={"kind": "sketch", "family": "exponential", "x": [-4, 3, 1], "y": [-4, 6, 1 / 3], "features": [
            {"id": "xint", "kind": "point", "label": "x-intercept", "at": [-2, 0], "tol": 0.01, "marks": 1, "crit": 1},
            {"id": "yint", "kind": "point", "label": "y-intercept", "at": [0, round(-8 / 3, 9)], "tol": 0.01, "marks": 0, "crit": 1},
            {"id": "asym", "kind": "hline", "label": "asymptote", "at": -3, "tol": 0.01, "marks": 1, "crit": 2}],
               "shape": {"label": "Shape", "answer": "decreasing", "marks": 1, "crit": 0, "pick": ["increasing", "decreasing"]}}),
    answer("7.1.4", "Determine the value of x for which f(x) ≥ 0", 2, ["x ≤ −2", "x ≥ −2", "x < −2", "x ≤ 0"],
           ["Where does f cut the x-axis?", "Is f above the x-axis to the left or to the right of that point?"], after=["7.1.2"])]
H7 = "y = a · kˣ − 2\n0 = a · k⁰ − 2, so a = 2\n"
q72 = [
    work("7.2", "An exponential function with equation h(x) = a · kˣ + r has the following properties:\n• The range is y ∈ (−2 ; ∞)\n"
         "• The points (0 ; 0) and (2 ; 6) lie on the graph\n\nDetermine the equation of h, in the form y = . . .", 4, [
        H7 + "6 = 2k² − 2, so k² = 4\nk = 2 (k > 0)\nh(x) = 2 · 2ˣ − 2",                       # the memo
        H7 + "6 = 2k² − 2, so k² = 4\nk = 4\nh(x) = 2 · 4ˣ − 2",                                # k² = 4 read as k = 4
        H7 + "6 = (2k)² − 2, so k² = 2\nk = √2 (k > 0)\nh(x) = 2 · (√2)ˣ − 2",                  # 2k² taken as (2k)²
        "y = a · kˣ + 2\n0 = a · k⁰ + 2, so a = −2\n6 = −2k² + 2, so k² = −2\nk² cannot be negative\nNo such h"],   # r = 2, not −2
        ["What does the range tell you about r?", "Which point gives a, and which then gives k?"])]

# ---- QUESTION 8, the question paper page 9 and the memo pages 17-18 ----
G = "(1 + {0,07}/{2})"
q8 = [
    work("8.1", "A motorbike costs R250 000 and depreciates by 13% p.a. annually, calculated on the reducing balance method.\n\nCalculate what "
         "the motorbike will be worth after 6 years.", 3, [
        "A = P(1 − i)ⁿ\nA = 250 000(1 − 0,13)⁶\nA = R108 406,55",       # the memo
        "A = P(1 − in)\nA = 250 000(1 − 0,13 × 6)\nA = R55 000,00",     # straight-line
        "A = P(1 + i)ⁿ\nA = 250 000(1 + 0,13)⁶\nA = R520 487,94",       # growth
        "A = P(1 − i)ⁿ\nA = 250 000(1 − 0,13)⁵\nA = R124 605,23"],      # 5 years
        ["Which formula gives a reducing-balance value?", "How many years, at what rate?"]),
    work("8.2", "Convert an annual effective rate of 7,5% per annum to a nominal rate per annum compounded quarterly.", 3, [
        "1 + 0,075 = (1 + {i(nom)}/{4})⁴\n⁴√1,075 − 1 = {i(nom)}/{4}\ni(nom) = 4(⁴√1,075 − 1) = 0,07297…\ni(nom) = 7,30% p.a.",    # the memo
        "1 + 0,075 = (1 + {i(nom)}/{4})⁴\n⁴√1,075 − 1 = {i(nom)}/{4}\ni(nom) = ⁴√1,075 − 1 = 0,01824…\ni(nom) = 1,82% p.a.",       # not × 4
        "1 + 0,075 = (1 + {i(nom)}/{12})¹²\n¹²√1,075 − 1 = {i(nom)}/{12}\ni(nom) = 12(¹²√1,075 − 1) = 0,07254…\ni(nom) = 7,25% p.a.",  # monthly
        "i(nom) = (1 + {0,075}/{4})⁴ − 1\n= 1,07714 − 1\n= 0,07714…\ni(nom) = 7,71% p.a."],                                         # the formula the wrong way
        ["Which formula links the effective rate to a nominal rate compounded 4 times a year?", "How do you undo the power 4?"]),
    work("8.3", "Rodney starts an investment with a deposit of R25 000. Two years later, he deposits another R10 000. Exactly four years after "
         "he started the investment, he withdraws R5 000. For the first two years, the interest is calculated at 4% per annum, compounded "
         "monthly and thereafter it is calculated at 7% per annum, compounded semi-annually.\n\nWhat is the accumulated amount of the "
         "investment exactly five years after the initial deposit?", 5, [
        "A = [25 000(1 + {0,04}/{12})²⁴ + 10 000]" + G + "⁶ − 5 000" + G + "²\nA = R40 222,91",       # the memo
        "A = [25 000(1 + {0,04}/{12})²⁴ + 10 000]" + G + "⁶ − 5 000\nA = R40 579,03",                 # the withdrawal not grown
        "A = [25 000(1 + {0,04}/{12})²⁴ + 10 000]" + G + "³ − 5 000" + G + "\nA = R35 934,68",         # years counted as periods
        "A = [25 000(1 + 0,04)² + 10 000]" + G + "⁶ − 5 000" + G + "²\nA = R40 175,49"],               # yearly, not monthly
        ["How many months at the first rate, and how many half-years at the second?", "For how long does the R5 000 withdrawal count?"]),
    work("8.4", "Brian borrows R x at an annual interest rate of 12% p.a. He has two options to repay the loan.\nOPTION 1: Pay R5 000, 2 years "
         "after the loan was granted and the remaining amount, 4 years after the loan was granted. The interest is compounded annually.\n"
         "OPTION 2: Pay R3 000, 1 year after the loan was granted and the remaining amount, 3 years after the loan was granted. The interest "
         "is compounded semi-annually.\n\nIf the total amount paid in both options is the same, calculate the value of x.", 6, [
        "Option 1: (x(1,12)² − 5 000)(1,12)²\nOption 2: (x(1,06)² − 3 000)(1,06)⁴\n(x(1,12)² − 5 000)(1,12)² = (x(1,06)² − 3 000)(1,06)⁴\n"
        "−5 000(1,12)² + 3 000(1,06)⁴ = x(1,06)⁶ − x(1,12)⁴\n−2 484,56912 = −0,1550002477x\nx = R16 029,45",                      # the memo
        "Option 1: (x(1,12)² − 5 000)(1,12)²\nOption 2: (x(1,06) − 3 000)(1,06)²\n(x(1,12)² − 5 000)(1,12)² = (x(1,06) − 3 000)(1,06)²\n"
        "−5 000(1,12)² + 3 000(1,06)² = x(1,06)³ − x(1,12)⁴\n−2 901,2 = −0,38250336x\nx = R7 584,77",                             # years as half-years
        "Option 1: (x(1,06)⁴ − 5 000)(1,06)⁴\nOption 2: (x(1,06)² − 3 000)(1,06)⁴\n(x(1,06)⁴ − 5 000)(1,06)⁴ = (x(1,06)² − 3 000)(1,06)⁴\n"
        "−5 000(1,06)⁴ + 3 000(1,06)⁴ = x(1,06)⁶ − x(1,06)⁸\n−2 524,95392 = −0,1753289623x\nx = R14 401,24",                      # option 1 semi-annual too
        "Option 1: (x(1,12)² − 5 000)(1,12)²\nOption 2: (x(1,06)² − 3 000)(1,06)²\n(x(1,12)² − 5 000)(1,12)² = (x(1,06)² − 3 000)(1,06)²\n"
        "−5 000(1,12)² + 3 000(1,06)² = x(1,06)⁴ − x(1,12)⁴\n−2 901,2 = −0,3110424x\nx = R9 327,35"],                            # 2 years as 2 half-years
        ["Draw a time line for each option: when is each payment made, and for how many periods does the rest grow?", "Set the final "
                                                                                                                     "payments equal."])]

# ---- QUESTION 9, the question paper page 10 and the memo pages 20-21 ----
PE = "P(enjoy) × P(male) = {56}/{106} × {42}/{106} = 0,2093…\n"
q91 = [
    work("9.1.1", "Are the events, A and B mutually exclusive? Motivate your answer.", 2, [
        "P(A and B) = P(A) × P(B) = 0,3 × 0,6 = 0,18\nP(A and B) ≠ 0\nNo: A and B are not mutually exclusive",     # the memo
        "P(A and B) = P(A) × P(B) = 0,3 × 0,6 = 0,18\nP(A and B) ≠ 0\nYes: A and B are mutually exclusive",        # the wrong conclusion
        "P(A or B) = 0,3 + 0,6 = 0,9\n0,9 < 1\nYes: A and B are mutually exclusive",                              # a sum under 1 taken as proof
        "Independent events are always mutually exclusive\nP(A and B) = 0\nYes: A and B are mutually exclusive"],   # the two ideas mixed up
        ["For independent events, what is P(A and B)?", "What must P(A and B) be for mutually exclusive events?"]),
    draw("9.1.2", "Represent the information on a Venn diagram.", 3, [["0,18 in A and B", 1], ["0,12 in A only and 0,42 in B only", 1],
                                                                       ["0,28 outside A and B", 1]],
         ["What is P(A and B) for independent events?", "What is left of P(A) once the overlap is taken out?"],
         memo="The memo's diagram: a rectangle S = 1 with circles A and B: 0,12 in A only, 0,18 in both, 0,42 in B only, 0,28 outside.",
         after=["9.1.1"]),
    answer("9.1.3", "Calculate P (not A and not B).", 2, ["0,28", "0,72", "0,82", "0,1"],
           ["'Not A and not B' is outside both circles.", "What is 1 − P(A or B)?"], after=["9.1.2"])]
q92 = [
    answer("9.2.1", "If an athlete from this group is chosen randomly, what is the probability that it is a male?", 1,
           ["{42}/{106} = {21}/{53}", "{26}/{106} = {13}/{53}", "{42}/{64} = {21}/{32}", "{26}/{56} = {13}/{28}"],
           ["How many athletes are male?", "Out of how many athletes is one chosen?"]),
    work("9.2.2", "Is the event \"enjoy jogging on sand\" independent of the gender?", 4, [
        PE + "P(enjoy and male) = {26}/{106} = 0,2453…\nP(enjoy and male) ≠ P(enjoy) × P(male)\nNot independent",          # the memo
        "P(enjoy) + P(male) = {56}/{106} + {42}/{106} = 0,9245…\nP(enjoy and male) = {26}/{106} = 0,2453…\n"
        "P(enjoy and male) ≠ P(enjoy) + P(male)\nNot independent",                                                         # the sum, not the product
        PE + "P(enjoy and male) = {26}/{56} = 0,4643…\nP(enjoy and male) ≠ P(enjoy) × P(male)\nNot independent",            # out of the wrong total
        PE + "P(enjoy and male) = {26}/{106} = 0,2453…\nP(enjoy and male) ≈ P(enjoy) × P(male)\nIndependent"],              # close taken as equal
        ["What must be true of P(enjoy and male) for independent events?", "Which totals do you divide by?"], after=["9.2.1"])]
q93 = [
    draw("9.3.1", "Draw a tree diagram, clearly labelling the branches and indicating the outcomes.", 3, [
        ["First branches: S 0,7 and S′ 0,3", 1], ["Second branches: after S, U x and U′ 1 − x; after S′, U 0,2x and U′ 1 − 0,2x", 1],
        ["Outcomes: SU, SU′, S′U, S′U′", 1]],
        ["What are the two weather outcomes and their chances?", "After each, what are the chances of using sunscreen or not?"],
        memo="The memo's tree: S 0,7 then U x (SU: 0,7x) and U′ 1 − x; S′ 0,3 then U 0,2x (S′U: 0,06x) and U′ 1 − 0,2x."),
    work("9.3.2", "If it is given that the overall probability of using sunscreen on a randomly selected day is 0,62, determine the value of x.", 3, [
        "P(U) = 0,7x + 0,3(0,2x)\n0,76x = 0,62\nx = 0,82",       # the memo
        "P(U) = 0,7x + 0,2x\n0,9x = 0,62\nx = 0,69",             # 0,2x not multiplied by 0,3
        "P(U) = 0,7x\n0,7x = 0,62\nx = 0,89",                    # only sunny days
        "P(U) = 0,7x × 0,3(0,2x)\n0,042x² = 0,62\nx = 3,84"],    # the branches multiplied, not added
        ["Which two branches end in U?", "Multiply along a branch, then add the branches."], after=["9.3.1"])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Equations and inequalities", "marks": 10, "lead": "Solve for x:", "items": q11[:3]},
    {"id": "1.1.4", "title": "Question 1.1.4", "kind": "Surd equations", "marks": 6, "lead": "Given: f(x) = √(x + 14)/(x + 2)", "items": q11[3:]},
    {"id": "1.2", "title": "Question 1.2", "kind": "Simultaneous equations", "marks": 6, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Equations", "marks": 5, "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Exponents", "marks": 4, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Exponential equations", "marks": 7, "lead": "Solve for x:", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Exponents", "marks": 4, "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Equations", "marks": 4, "items": q24},
    {"id": "3.1", "title": "Question 3.1", "kind": "Linear patterns", "marks": 6,
     "lead": "Consider the following linear number pattern: 5,5 ; 5,0 ; 4,5 ; . . .", "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Linear patterns", "marks": 3, "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Quadratic patterns", "marks": 11,
     "lead": "Given the nᵗʰ term of the quadratic number pattern: Tₙ = n² − 12n + k", "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Quadratic patterns", "marks": 3, "items": q42},
    {"id": "5", "title": "Question 5", "kind": "Hyperbola and straight line", "marks": 17,
     "lead": "The graphs of f(x) = a/(x + p) + q and g(x) = x/3 + c are drawn below. C(3 ; −1) is the point of intersection between the "
             "asymptotes of f. A and B are x- and y-intercepts of f and g respectively. E(4 ; 2) is a point on f in the first quadrant.",
     "figure": P.fig("Q5", "The hyperbola f with dashed asymptotes crossing at C(3 ; −1): one branch top right through E(4 ; 2) and A on the "
                           "x-axis, the other bottom left through B on the y-axis. The straight line g passes through B, C and A, making "
                           "the angle θ with the x-axis at A."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Parabolas", "marks": 11,
     "lead": "The graphs of f(x) = −x² − 6x and g(x) = ax² + bx are drawn below. g is the reflection of f along the x-axis. A and B(−5 ; n) "
             "are symmetrical on f along x = −p, i.e. the axes of symmetry.",
     "figure": P.fig("Q6", "The parabola f, opening downwards, and the dashed parabola g, opening upwards, both through O and F on the "
                           "x-axis. B(−5 ; n) and A are on f above the x-axis. A vertical line through E on the x-axis, left of F, meets g "
                           "at C above and f at D below."), "items": q6[:3]},
    {"id": "6.4", "title": "Question 6.4", "kind": "Parabolas", "marks": 5, "lead": "Determine the value(s) of k for which:", "items": q6[3:]},
    {"id": "7.1", "title": "Question 7.1", "kind": "Exponential graph", "marks": 9, "lead": "Given: f(x) = (1/3)^(x + 1) − 3", "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Exponential graph", "marks": 4, "items": q72},
    {"id": "8", "title": "Question 8", "kind": "Finance", "marks": 17, "items": q8},
    {"id": "9.1", "title": "Question 9.1", "kind": "Probability", "marks": 7,
     "lead": "A and B are independent events. It is further given that:\n• P(A) = 0,3\n• P(B) = 0,6", "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Contingency tables", "marks": 5,
     "lead": "The contingency table below represents 106 athletes' responses regarding jogging on the sand.\n"
             "Enjoy jogging on sand: male 26, female 30, total 56\nDo not enjoy jogging on sand: male 16, female 34, total 50\n"
             "Total: male 42, female 64, total 106", "items": q92},
    {"id": "9.3", "title": "Question 9.3", "kind": "Tree diagrams", "marks": 6,
     "lead": "During the summer season in South Africa, the probability of sunny weather on any given day is 0,7. If it is sunny, the "
             "probability that a person uses sunscreen is x. If it is not sunny, the probability of using sunscreen is 0,2x.", "items": q93},
]
P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "7.1.3", "kind": "no_fit", "detail": "The sketch of f is BUILT on a grid (its y-steps are thirds, so the y-intercept −8/3 is a "
                                                     "grid point): the learner places both intercepts and the asymptote and picks the "
                                                     "shape. The Venn diagram (9.1.2) and the tree diagram (9.3.1) play as pick the drawing: "
                                                     "the memo's and three mistakes."},
          {"n": "8.4", "kind": "low_confidence", "detail": "The stem says the TOTAL amount paid is the same; the memo equates the final payments "
                                                           "only, (x(1,12)² − 5 000)(1,12)² = (x(1,06)² − 3 000)(1,06)⁴, x = R16 029,45. Equating "
                                                           "the totals gives x ≈ R3 126, less than the R5 000 first payment, so the memo's "
                                                           "reading is the only sensible one; the right option is the memo's."},
          {"n": "6.1", "kind": "memo_issue", "detail": "The memo's substitution line (page 13) reads −(1)² − 6(−3) = 9; f(−3) = −(−3)² − 6(−3) "
                                                       "= 9. The right option writes −(−3)²."},
          {"n": "2.1", "kind": "memo_issue", "detail": "The memo's mark column (page 5) writes 125ˣ = 3³ˣ; its working uses 5³ˣ. The right "
                                                       "option uses 5³ˣ."}],
         {"1": 27, "2": 19, "3": 9, "4": 14, "5": 17, "6": 16, "7": 13, "8": 17, "9": 18}, 150,
         {"3.1.3": ["3.1.2"], "4.1.2": ["4.1.1"], "4.1.4": ["4.1.1"], "4.1.5": ["4.1.4"], "5.2": ["5.1"], "5.4": ["5.2"], "5.5": ["5.3"],
          "5.6": ["5.3"], "6.2": ["6.1"], "7.1.3": ["7.1.1", "7.1.2"], "7.1.4": ["7.1.2"], "9.1.2": ["9.1.1"], "9.1.3": ["9.1.2"],
          "9.2.2": ["9.2.1"], "9.3.2": ["9.3.1"]},
         "Questions 1 to 9 (the whole paper)")
