"""Grade 11 Mathematics P1 November 2024 (Eastern Cape Department of Education), the whole paper (Questions 1 to 10, 150 marks,
3 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json` like any ingested paper. Stems,
marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours.
Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the question paper zip (English PDF, 13 pages,
text layer) and the memo PDF (English and Afrikaans, 16 pages). The memo's text layer garbles fractions and powers, so it was
read from its page images at 100 dpi; the question paper from its page images too.

  python tools/ingest/transcribe_g11_math_p1_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-math-p1-2024-11-ec/MATHS P1 QP GR11 NOV2024 ENG D_watermark.pdf" "uploads/provincial/g11-math-p1-2024-11-ec/MATHS P1 MEMO GR11 NOV2024_ENG_AFR_watermark.pdf" --id g11-math-p1-2024-11-ec --from-json

The memo's shapes map by the Grade 12 rulings (provincial.py). The sketch 5.4 is built on a grid (hyperbola: shape, asymptotes,
intercepts). Question 10 (the spinners, 8 marks) plays as one working: the memo's alternative marking is a calculation
(1/3 × 5/8, 1/3 × 3/8, the sum), and its tree is a method, not something the question asks to draw.
The paper prints 2.2.2 as "3.5ˣ − 5ˣ⁻¹ = 14": the dot is a multiplication (the memo factors 5ˣ(3 − 1/5)), written here
3 · 5ˣ. Figure boxes in PDF points (page 595 x 842), measured from the vector drawing and image boxes (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-math-p1-2024-11-ec", 595.2, 842.0, {
    "Q6": [8, 134.6, 150.4, 436.3, 386.9],    # f with A, B, C, 0 and the point at x = 6
    "Q7": [9, 114.4, 184.7, 439.4, 456.2],    # f, g, the dashed asymptote, A(−2 ; 4), B
    "Q9": [11, 179.4, 345.7, 404.4, 545.0],   # the Venn diagram M, P, A
    "Q10": [12, 110.8, 119.1, 442.4, 292.1]}, start=0)
work, answer, num, draw = P.work, P.answer, P.num, P.draw

# ---- QUESTION 1, the question paper page 3 and the memo pages 3-5 ----
QF = "x = {−b ± √(b² − 4ac)}/{2a}\n"
q11 = [
    answer("1.1.1", "x² − 2x − 8 = 0", 2, ["x = 4 or x = −2", "x = −4 or x = 2", "x = 4 or x = 2", "x = 8 or x = −1"],
           ["Which two numbers multiply to −8 and add to −2?", "When is a product of two factors equal to zero?"]),
    work("1.1.2", "2x² − 3x = 7 (answers correct to TWO decimal places)", 4, [
        "2x² − 3x − 7 = 0\n" + QF + "x = {−(−3) ± √((−3)² − 4(2)(−7))}/{2(2)}\nx = 2,77 or x = −1,27",                     # the memo
        "2x² − 3x + 7 = 0\n" + QF + "x = {−(−3) ± √((−3)² − 4(2)(7))}/{2(2)}\nNo real roots",                              # 7 moved without its sign change
        "2x² − 3x − 7 = 0\n" + QF + "x = {−3 ± √((−3)² − 4(2)(−7))}/{2(2)}\nx = 1,27 or x = −2,77",                         # b for −b
        "2x² − 3x − 7 = 0\nx = {−b ± √(b² − 4ac)}/{a}\nx = {−(−3) ± √((−3)² − 4(2)(−7))}/{2}\nx = 5,53 or x = −2,53"],      # divided by a, not 2a
        ["What must the equation look like before you use the quadratic formula?", "What are a, b and c, and what is b² − 4ac?"]),
    work("1.1.3", "(x + 1)(4 − x) > 0 ; where x ∈ ℕ", 3, [
        "(x + 1)(x − 4) < 0\nCritical values: x = −1 or x = 4\n−1 < x < 4, but x ∈ ℕ\nx ∈ {1 ; 2 ; 3}",                      # the memo
        "(x + 1)(x − 4) > 0\nCritical values: x = −1 or x = 4\nx < −1 or x > 4, but x ∈ ℕ\nx ∈ {5 ; 6 ; 7 ; …}",              # sign kept when multiplying by −1
        "(x + 1)(x − 4) < 0\nCritical values: x = −1 or x = 4\n−1 < x < 4, but x ∈ ℕ\nx ∈ {0 ; 1 ; 2 ; 3}",                  # 0 taken as a natural number
        "(x + 1)(x − 4) < 0\nCritical values: x = −1 or x = 4\n−1 ≤ x ≤ 4, but x ∈ ℕ\nx ∈ {1 ; 2 ; 3 ; 4}"],                 # the end points included
        ["What happens to the inequality sign when you multiply both sides by −1?", "Which natural numbers lie strictly between the "
                                                                                   "critical values?"])]
q12 = [
    work("1.2.1", "Solve for p", 3, [
        "p(p + 5) = 14\np² + 5p − 14 = 0\n(p + 7)(p − 2) = 0\np = −7 or p = 2",                         # the memo
        "p(p + 5) = 14\np² + 5p − 14 = 0\n(p − 7)(p + 2) = 0\np = 7 or p = −2",                         # the signs in the factors swapped
        "14 = p² + 5\np² − 9 = 0\n(p − 3)(p + 3) = 0\np = 3 or p = −3",                                 # p multiplied into p only
        "p(p + 5) = 14\np² + 5p + 14 = 0\nΔ = 5² − 4(1)(14) = −31\nNo real solution"],                  # 14 moved without its sign change
        ["What do you multiply both sides by to clear the fraction?", "Which two numbers multiply to −14 and add to 5?"]),
    work("1.2.2", "Hence, or otherwise, solve for x if 14/√(x + 5) = √(x + 5) + 5", 4, [
        "Let √(x + 5) = p: p = 2 or p = −7\n√(x + 5) = 2 or √(x + 5) = −7\n√(x + 5) ≠ −7\nx + 5 = (2)²\nx = −1",            # the memo
        "Let √(x + 5) = p: p = 2 or p = −7\n√(x + 5) = 2 or √(x + 5) = −7\nx + 5 = (2)² or x + 5 = (−7)²\nx + 5 = 4 or x + 5 = 49\n"
        "x = −1 or x = 44",                                                                                                  # both roots kept
        "Let √(x + 5) = p: p = 2 or p = −7\n√(x + 5) = 2 or √(x + 5) = −7\n√(x + 5) ≠ −7\nx + 5 = 2\nx = −3",                 # not squared
        "Let √(x + 5) = p: p = 2 or p = −7\n√(x + 5) = 2 or √(x + 5) = −7\n√(x + 5) ≠ −7\nx + 5 = (2)²\nx = 9"],             # 5 added, not subtracted
        ["Which expression plays the part of p in this equation?", "Can a square root be negative?"], after=["1.2.1"])]
SUB = "x = 1 + 3y\n(1 + 3y)² − 2y(1 + 3y) − y² − 7 = 0\n"
q13 = [
    work("1.3", "Solve for x and y simultaneously:\n−3y = 1 − x and x² − 2xy − y² − 7 = 0", 6, [
        SUB + "1 + 6y + 9y² − 2y − 6y² − y² − 7 = 0\n2y² + 4y − 6 = 0\ny² + 2y − 3 = 0\n(y + 3)(y − 1) = 0\ny = −3 or y = 1\n"
              "x = −8 or x = 4",                                                                                        # the working, corrected
        SUB + "1 + 9y² − 2y − 6y² − y² − 7 = 0\n2y² − 2y − 6 = 0\ny² − y − 3 = 0\ny = {1 ± √13}/{2}\ny = 2,30 or y = −1,30\n"
              "x = 7,91 or x = −2,91",                                                                                  # (1 + 3y)² as 1 + 9y²
        SUB + "1 + 6y + 9y² − 2y + 6y² − y² − 7 = 0\n14y² + 4y − 6 = 0\n7y² + 2y − 3 = 0\ny = {−2 ± √88}/{14}\n"
              "y = 0,53 or y = −0,81\nx = 2,58 or x = −1,44",                                                           # −2y(1 + 3y) as −2y + 6y²
        SUB + "1 + 6y + 9y² − 2y − 6y² − y² − 7 = 0\n2y² + 4y − 6 = 0\ny² + 2y − 3 = 0\n(y + 3)(y − 1) = 0\ny = 1 (y ≠ −3)\n"
              "x = 4"],                                                                                                 # the negative root rejected
        ["Which equation is easier to make x the subject of?", "After substituting, expanding and collecting like terms, what equation in y "
                                                              "do you get?"])]
q14 = [
    work("1.4", "If 2x⁻¹ + x⁻² = 3 and x < 0, determine, without using a calculator, the value of 2(6x − 1)⁻¹.", 4, [
        "{2}/{x} + {1}/{x²} = 3\n2x + 1 − 3x² = 0\n3x² − 2x − 1 = 0\n(3x + 1)(x − 1) = 0\nx = −{1}/{3} (x < 0)\n"
        "2(6x − 1)⁻¹ = 2(6 × (−{1}/{3}) − 1)⁻¹\n= 2(−3)⁻¹\n= −{2}/{3}",                                                  # the memo
        "{2}/{x} + {1}/{x²} = 3\n2x + 1 − 3x² = 0\n3x² − 2x − 1 = 0\n(3x + 1)(x − 1) = 0\nx = 1 (x ≠ −{1}/{3})\n"
        "2(6x − 1)⁻¹ = 2(6 × 1 − 1)⁻¹\n= 2(5)⁻¹\n= {2}/{5}",                                                              # x < 0 ignored
        "{2}/{x} + {1}/{x²} = 3\n2x + 1 − 3x² = 0\n3x² − 2x − 1 = 0\n(3x + 1)(x − 1) = 0\nx = −{1}/{3} (x < 0)\n"
        "2(6x − 1)⁻¹ = −2(6 × (−{1}/{3}) − 1)\n= −2(−3)\n= 6",                                                            # the power −1 read as a minus
        "{2}/{x} + {1}/{x²} = 3\n2x + 1 − 3x² = 0\n3x² − 2x − 1 = 0\n(3x − 1)(x + 1) = 0\nx = −1 (x < 0)\n"
        "2(6x − 1)⁻¹ = 2(6 × (−1) − 1)⁻¹\n= 2(−7)⁻¹\n= −{2}/{7}"],                                                        # the signs in the factors swapped
        ["What is x⁻¹ written as a fraction, and what do you multiply by to clear the fractions?", "Which root does x < 0 allow?"])]

# ---- QUESTION 2, the question paper page 4 and the memo pages 6-7 ----
q21 = [
    work("2.1", "Simplify fully, without using a calculator:\n(√32 − √18 + 3√3)/(√108 + √8)", 4, [
        "= {√(16 × 2) − √(9 × 2) + 3√3}/{√(36 × 3) + √(4 × 2)}\n= {4√2 − 3√2 + 3√3}/{6√3 + 2√2}\n= {√2 + 3√3}/{2(3√3 + √2)}\n= {1}/{2}",  # the memo
        "= {√(16 × 2) − √(9 × 2) + 3√3}/{√(36 × 3) + √(4 × 2)}\n= {4√2 − 3√2 + 3√3}/{6√3 + 2√2}\n= {1 + 3√3}/{6√3 + 2√2}\n"
        "= {1 + 3√3}/{2(3√3 + √2)}",                                                                                  # 4√2 − 3√2 taken as 1
        "= {√(32 − 18) + 3√3}/{√(108 + 8)}\n= {√14 + 3√3}/{√116}\n= {√14 + 3√3}/{√(4 × 29)}\n= {√14 + 3√3}/{2√29}",  # roots subtracted and added inside
        "= {√(16 × 2) − √(9 × 2) + 3√3}/{√(36 × 3) + √(4 × 2)}\n= {4√2 − 3√2 + 3√3}/{6√3 + 2√2}\n= {√2 + 3√3}/{2(3√3 + √2)}\n= 2"],  # the 2 put on top
        ["Which perfect square is a factor of each number under a root?", "Once the surds are simplified, what do the top and the bottom "
                                                                          "have in common?"])]
q22 = [
    work("2.2.1", "2x^(−5/2) = 64", 3, [
        "x^(−5/2) = 32\nx = (2⁵)^(−2/5)\nx = 2⁻²\nx = {1}/{4}",          # the memo
        "x^(−5/2) = 64\nx = (2⁶)^(−2/5)\nx = 2^(−12/5)\nx = 0,19",       # not divided by 2 first
        "x^(−5/2) = 32\nx = (2⁵)^(2/5)\nx = 2²\nx = 4",                  # the sign of the exponent lost
        "x^(−5/2) = 32\nx = (2⁵)^(−2/5)\nx = 2⁻²\nx = −4"],              # 2⁻² taken as −4
        ["What must you do to both sides before you deal with the exponent?", "What power must x^(−5/2) be raised to, to leave x on its own?"]),
    work("2.2.2", "3 · 5ˣ − 5ˣ⁻¹ = 14", 5, [
        "3 · 5ˣ − 5ˣ · 5⁻¹ = 14\n5ˣ(3 − {1}/{5}) = 14\n5ˣ · {14}/{5} = 14\n5ˣ = 5\nx = 1",          # the memo
        "3 · 5ˣ − 5ˣ · 5⁻¹ = 14\n5ˣ(3 − 1) = 14\n5ˣ · 2 = 14\n5ˣ = 7\nx = 1,21",                    # the 5⁻¹ dropped from the factor
        "3 · 5ˣ − 5ˣ · 5 = 14\n5ˣ(3 − 5) = 14\n5ˣ · (−2) = 14\n5ˣ = −7\nNo solution",              # 5ˣ⁻¹ split as 5ˣ · 5
        "3 · 5ˣ − 5ˣ · 5⁻¹ = 14\n5ˣ(3 − {1}/{5}) = 14\n5ˣ · {14}/{5} = 14\n5ˣ = {196}/{5}\nx = 2,28"],  # multiplied by 14/5, not divided
        ["How can you write 5ˣ⁻¹ as 5ˣ times a number?", "What common factor can you take out of both terms?"])]
SQ = "(√a + √b)² = (√(9 + √56))²\na + b + 2√(ab) = 9 + 2√14\na + b = 9 and ab = 14\n"
q23 = [
    work("2.3", "Calculate a possible value for a² + b², if it is given that a and b are rational numbers such that √a + √b = √(9 + √56).", 5, [
        SQ + "a = 2 and b = 7\na² + b² = 4 + 49 = 53",          # the memo
        SQ + "a² + b² = (a + b)²\na² + b² = 81",                # a² + b² taken as (a + b)²
        SQ + "a = 2 and b = 7\na² + b² = 2(2) + 2(7) = 18",     # squaring taken as doubling
        SQ + "a = 3 and b = 6\na² + b² = 9 + 36 = 45"],         # only a + b = 9 checked
        ["What do you get when you square both sides?", "How can you write √56 so that it matches 2√(ab)?"])]

# ---- QUESTION 3, the question paper page 5 and the memo page 8 ----
q31 = [
    answer("3.1.1", "Write down the next TWO terms of the pattern.", 2, ["−17 ; −21", "−9 ; −5", "−17 ; −22", "−18 ; −23"],
           ["What is added to each term to get the next one?", "Is the constant difference positive or negative?"]),
    work("3.1.2", "Determine an expression for the nᵗʰ term of the pattern.", 2, [
        "d = −9 − (−5) = −4\nTₙ = −4n + c, with T₁ = −4 + c = −5\nTₙ = −4n − 1",     # the memo
        "d = −9 − (−5) = −4\nTₙ = −4n + c, with c = T₁ = −5\nTₙ = −4n − 5",          # the first term taken as c
        "d = −5 − (−9) = 4\nTₙ = 4n + c, with T₁ = 4 + c = −5\nTₙ = 4n − 9",          # the difference taken the wrong way round
        "d = −9 − (−5) = −4\nTₙ = −4n + c, with T₁ = −4 + c = −5\nTₙ = −4n − 9"],     # −4 moved without its sign change
        ["What is the constant difference d?", "Which value of c makes T₁ equal to −5?"]),
    work("3.1.3", "Calculate the value of n for which Tₙ = −141.", 2, [
        "−4n − 1 = −141\n−4n = −140\nn = 35",       # the memo
        "−4n − 1 = −141\n−4n = −142\nn = 35,5",     # −1 moved without its sign change
        "−4n − 1 = −141\n−4n = −140\nn = −35",      # the signs of −140 ÷ −4 lost
        "Tₙ = −4(−141) − 1\nTₙ = 563\nn = 563"],    # −141 put in for n
        ["Is −141 a position or the value of a term?", "Which n makes your nᵗʰ term equal to −141?"], after=["3.1.2"])]
T3 = "T₁ = x and d = x − 5\nx ; x + (x − 5) ; x + 2(x − 5)\n"
q32 = [
    work("3.2", "In a linear number pattern the first term is x and a common difference is 5 less than the first term.\n\nCalculate the value "
         "of the first term if it is given that the sum of the first three terms of the linear number pattern is 63.", 5, [
        T3 + "x + x + (x − 5) + x + 2(x − 5) = 63\n6x − 15 = 63\nx = 13",                                                 # the memo
        "T₁ = x and d = x − 5\nx ; x + (x − 5) ; x + 3(x − 5)\nx + x + (x − 5) + x + 3(x − 5) = 63\n7x − 20 = 63\nx = 11,86",  # T₃ = a + 3d
        T3 + "x + 2(x − 5) = 63\n3x − 10 = 63\nx = 24,33",                                                                # the third term set to 63
        T3 + "x + x + (x − 5) + x + 2(x − 5) = 63\n6x − 10 = 63\nx = 12,17"],                                             # 2(x − 5) as 2x − 5
        ["How do you write the second and third terms using x and the difference?", "Which equation does the sum of the three terms give?"])]

# ---- QUESTION 4, the question paper page 6 and the memo page 9 ----
q4 = [
    work("4.1", "Show that the above number pattern is quadratic.", 2, [
        "First differences: −14 ; −10 ; −6\nSecond differences: 4 ; 4\nThe second difference is constant, so the pattern is quadratic",  # the memo
        "First differences: 14 ; 10 ; 6\nSecond differences: −4 ; −4\nThe second difference is constant, so the pattern is quadratic",  # each difference the wrong way round
        "First differences: −14 ; −10 ; −6\nThe first differences change\nSo the pattern is quadratic",                                # changing differences are not enough
        "First differences: −14 ; −10 ; −6\nSecond differences: 4 ; 4\nThe second difference is positive, so the pattern is quadratic"],  # the wrong reason
        ["What are the first differences between consecutive terms?", "What must be true of the second differences of a quadratic pattern?"]),
    work("4.2", "Determine the nᵗʰ term of the quadratic number pattern in the form Tₙ = an² + bn + c.", 4, [
        "2a = 4, so a = 2\n3a + b = −14, so b = −20\na + b + c = 24, so c = 42\nTₙ = 2n² − 20n + 42",      # the memo's working
        "a = 4 (the second difference)\n3a + b = −14, so b = −26\na + b + c = 24, so c = 46\nTₙ = 4n² − 26n + 46",  # a taken as the second difference
        "2a = 4, so a = 2\n3a + b = −14, so b = −8\na + b + c = 24, so c = 30\nTₙ = 2n² − 8n + 30",         # 6 added instead of subtracted for b
        "2a = 4, so a = 2\n3a + b = −14, so b = −20\nc = T₁ = 24\nTₙ = 2n² − 20n + 24"],                    # the first term taken as c
        ["How is the second difference related to a?", "Which expressions in a, b and c give the first first difference and the first term?"]),
    work("4.3", "Calculate the value of T₅₂.", 2, [
        "T₅₂ = 2(52)² − 20(52) + 42\n= 4 410",          # the memo
        "T₅₂ = 2(104) − 20(52) + 42\n= −790",           # 52² taken as 2 × 52
        "T₅₂ = (2 × 52)² − 20(52) + 42\n= 9 818",       # the 2 squared with 52
        "T₅₂ = 2(52)² − 20(52) − 42\n= 4 326"],         # the sign of c lost
        ["Which value of n stands for the 52nd term?", "What do you get when you substitute it into your nᵗʰ term?"], after=["4.2"]),
    work("4.4", "Determine the smallest value of the quadratic number pattern.", 3, [
        "n = {−b}/{2a} = {−(−20)}/{2(2)} = 5\nT₅ = 2(5)² − 20(5) + 42\n= −8",          # the memo
        "n = {−b}/{2a} = {−20}/{2(2)} = −5\nT₋₅ = 2(−5)² − 20(−5) + 42\n= 192",        # the sign of b lost
        "n = {−b}/{a} = {−(−20)}/{2} = 10\nT₁₀ = 2(10)² − 20(10) + 42\n= 42",          # divided by a, not 2a
        "n = {−b}/{2a} = {−(−20)}/{2(2)} = 5\nT₅ = (2 × 5)² − 20(5) + 42\n= 42"],      # the 2 squared with 5
        ["At which n does the pattern turn?", "What is the value of the term at that n?"], after=["4.2"]),
    work("4.5", "Determine the value(s) of n for which the terms of the quadratic number pattern will be positive.", 4, [
        "2n² − 20n + 42 > 0\nn² − 10n + 21 > 0\n(n − 7)(n − 3) > 0\nn < 3 or n > 7\n1 ≤ n < 3 or n > 7, n ∈ ℕ",     # the memo
        "2n² − 20n + 42 > 0\nn² − 10n + 21 > 0\n(n − 7)(n − 3) > 0\n3 < n < 7\n3 < n < 7, n ∈ ℕ",                     # the region between the roots
        "2n² − 20n + 42 > 0\nn² − 10n + 21 > 0\n(n + 7)(n + 3) > 0\nn < −7 or n > −3\nn ≥ 1, n ∈ ℕ",                 # the signs in the factors lost
        "2n² − 20n + 42 > 0\nn² − 10n + 21 > 0\n(n − 7)(n − 3) > 0\nCritical values: 3 and 7\nn < 3 or n > 7, n ∈ ℝ"],  # n not a natural number
        ["When is a term positive, and which inequality does that give?", "Can n, a term's position, be zero, negative or a fraction?"],
        after=["4.2"])]

# ---- QUESTION 5, the question paper page 7 and the memo pages 10-11 ----
q5 = [
    work("5.1", "Show that p = −3 and q = 1.", 4, [
        "x − 2 = −x + 4\n2x = 6, so x = 3\nx − 3 = 0, so p = −3\ny = (3) − 2 = 1, so q = 1",                                   # the memo
        "f(x) = {−3}/{x − 3} + 1\nAsymptotes: x = 3 and y = 1\n3 − 2 = 1 and −3 + 4 = 1\nSo p = −3 and q = 1",                 # starts from the answer
        "The y-intercepts of the lines are 4 and −2\nq = {4 + (−2)}/{2} = 1\np = −(4 − 1) = −3\nSo p = −3 and q = 1",           # the y-intercepts used
        "x − 2 = −x + 4\n2x = 6, so x = 3\nx + 3 = 0, so p = −3\ny = (3) − 2 = 1, so q = 1"],                                   # x + 3 = 0 gives x = −3
        ["Where do the two axes of symmetry of a hyperbola meet?", "How are p and q related to the point where the asymptotes cross?"]),
    work("5.2", "Calculate the x-intercept of f.", 2, [
        "{−3}/{x − 3} + 1 = 0\n{−3}/{x − 3} = −1\n−x + 3 = −3\nx = 6",                   # the memo
        "{−3}/{0 − 3} + 1 = y\ny = 1 + 1\ny = 2\nx-intercept: (0 ; 2)",                  # the y-intercept worked out
        "{−3}/{x − 3} + 1 = 0\n{−3}/{x − 3} = −1\n−x + 3 = −3\nx = −6",                  # the last sign lost
        "{−3}/{x − 3} + 1 = 0\n{−3}/{x − 3} = 1\n−3 = x − 3\nx = 0"],                    # 1 moved without its sign change
        ["What is y at an x-intercept?", "How do you clear the fraction once the 1 is on the other side?"]),
    work("5.3", "Calculate the y-intercept of f.", 2, [
        "y = {−3}/{0 − 3} + 1\ny = 2",       # the memo
        "y = {−3}/{0 + 3} + 1\ny = 0",       # the sign of p lost
        "y = {−3}/{0 − 3}\ny = 1",           # the + 1 left off
        "y = {−3 + 1}/{0 − 3}\ny = {2}/{3}"],  # the + 1 put on top of the fraction
        ["What is x at a y-intercept?", "What is −3 divided by −3?"]),
    draw("5.4", "Sketch the graph of f. Clearly label all intercepts with the axes and asymptotes.", 3, [
        ["Shape: the two branches, top left and bottom right of the asymptotes", 1], ["The asymptotes x = 3 and y = 1", 1],
        ["The intercepts (0 ; 2) and (6 ; 0)", 1]],
        ["Where do the asymptotes cross, and where does the graph cut the axes?", "a = −3 is negative: in which quadrants of the asymptotes "
                                                                                  "are the branches?"],
        memo="The memo's sketch: dashed asymptotes x = 3 and y = 1; one branch top left, rising through (0 ; 2) towards x = 3; the other "
             "bottom right, rising from below through (6 ; 0) towards y = 1.", after=["5.2", "5.3"],
        build={"kind": "sketch", "family": "hyperbola", "x": [-4, 10, 1], "y": [-5, 6, 1], "features": [
            {"id": "va", "kind": "vline", "label": "vertical asymptote", "at": 3, "tol": 0, "marks": 1, "crit": 1},
            {"id": "ha", "kind": "hline", "label": "horizontal asymptote", "at": 1, "tol": 0, "marks": 0, "crit": 1},
            {"id": "xi", "kind": "point", "label": "x-intercept", "at": [6, 0], "tol": 0, "marks": 1, "crit": 2},
            {"id": "yi", "kind": "point", "label": "y-intercept", "at": [0, 2], "tol": 0, "marks": 0, "crit": 2}],
               "shape": {"label": "Shape", "answer": "top left and bottom right", "marks": 1, "crit": 0}}),
    answer("5.5", "Write down the domain of g if g is the reflection of f along the line x = 0.", 3,
           ["x ∈ ℝ, x ≠ −3", "x ∈ ℝ, x ≠ 3", "y ∈ ℝ, y ≠ 1", "x ∈ ℝ, x ≠ −1"],
           ["Where does the vertical asymptote of f go when the graph is reflected in the y-axis?", "Which x-value is left out of the domain?"]),
    answer("5.6", "For which values of x will x · f(x) ≤ 0?", 3, ["x ≤ 0 or 3 < x ≤ 6", "0 ≤ x < 3 or x ≥ 6", "x ≤ 0 or 3 ≤ x ≤ 6", "3 < x ≤ 6"],
           ["When is a product of two numbers negative or zero?", "Where is f above the x-axis, where below, and where is it not defined?"],
           after=["5.2"])]

# ---- QUESTION 6, the question paper page 8 and the memo pages 12-13 ----
X0 = "x² − 4x − 5 = 0\n"
H = "h(x) = −2x + c\nx² − 4x − 5 = −2x + c\n"
TP = "x = {−(−4)}/{2(1)} = 2\nf(2) = −9\n"
q6 = [
    work("6.1", "Determine the value of f(6).", 1, [
        "f(6) = (6)² − 4(6) − 5\n= 7",       # the memo
        "f(6) = (6)² − 4(6) + 5\n= 17",      # the sign of −5 lost
        "f(6) = 2(6) − 4(6) − 5\n= −17",     # 6² taken as 2 × 6
        "f(6) = (6)² − 4(−6) − 5\n= 55"],    # −4 × 6 taken as +24
        ["Where does 6 go in the formula?", "What is 6²?"]),
    work("6.2", "Determine the coordinates of A and B.", 3, [
        X0 + "(x − 5)(x + 1) = 0\nx = 5 or x = −1\nA(−1 ; 0) and B(5 ; 0)",      # the memo
        X0 + "(x + 5)(x − 1) = 0\nx = −5 or x = 1\nA(−5 ; 0) and B(1 ; 0)",      # the signs in the factors swapped
        X0 + "(x − 5)(x + 1) = 0\nx = 5 or x = −1\nA(5 ; 0) and B(−1 ; 0)",      # A and B swapped
        X0 + "(x − 5)(x + 1) = 0\nx = 5 or x = −1\nA(0 ; −1) and B(0 ; 5)"],     # the coordinates the wrong way round
        ["What is y at an x-intercept?", "Which of the two points is to the left of the y-axis?"]),
    num("6.3", "Hence, calculate the length of AB.", 6, 0, "", ["Which coordinates of A and B do you need?", "How far is it from −1 to 5?"],
        after=["6.2"]),
    work("6.4", "Write down the equation of g in the form g(x) = ax² + bx + c, if it is given that g(x) is obtained by shifting f(x) two units "
         "to the right and five units up.", 3, [
        "g(x) = (x − 2)² − 4(x − 2) − 5 + 5\n= x² − 4x + 4 − 4x + 8\n= x² − 8x + 12",      # the working, corrected
        "g(x) = (x + 2)² − 4(x + 2) − 5 + 5\n= x² + 4x + 4 − 4x − 8\n= x² − 4",           # shifted to the left
        "g(x) = (x − 2)² − 4(x − 2) − 5 + 5\n= x² − 4x + 4 − 4x − 8\n= x² − 8x − 4",      # −4(x − 2) as −4x − 8
        "g(x) = (x − 2)² − 4x − 5 + 5\n= x² − 4x + 4 − 4x\n= x² − 8x + 4"],                # only x² shifted
        ["What do you replace x with to shift a graph 2 units to the right?", "How does shifting 5 units up change the formula?"]),
    work("6.5", "Suppose h is a tangent to the curve f at a certain point, with a gradient of −2. Calculate the y-intercept of h.", 5, [
        H + "x² − 2x − 5 − c = 0\nΔ = (−2)² − 4(1)(−5 − c) = 24 + 4c\nTangent: Δ = 0, so 24 + 4c = 0\nc = −6",        # the memo
        H + "x² − 2x − 5 − c = 0\nΔ = (−2)² − 4(1)(−5 − c) = 24 − 4c\nTangent: Δ = 0, so 24 − 4c = 0\nc = 6",          # −4 × −c taken as −4c
        H + "x² − 6x − 5 − c = 0\nΔ = (−6)² − 4(1)(−5 − c) = 56 + 4c\nTangent: Δ = 0, so 56 + 4c = 0\nc = −14",        # −2x moved without its sign change
        H + "x² − 2x − 5 − c = 0\nΔ = (−2)² + 4(1)(−5 − c) = −16 − 4c\nTangent: Δ = 0, so −16 − 4c = 0\nc = −4"],      # + 4ac in the discriminant
        ["Where does a tangent meet the curve, and how many times?", "Which value of the discriminant gives exactly one point of contact?"]),
    work("6.6", "For which values of k will f(x) − k = 0 have just one real root?", 3, [
        TP + "k = −9 or k > 7",      # the memo
        TP + "k = −9",               # the end of the domain at x = 6 ignored
        TP + "k = −9 or k ≥ 7",      # k = 7 cuts f twice, at x = −2 and x = 6
        TP + "k > −9"],              # two roots taken as one
        ["How many times does a horizontal line y = k cut the graph of f, drawn only up to x = 6?", "What are the turning point of f and the "
                                                                                                    "value of f at x = 6?"], after=["6.1"])]

# ---- QUESTION 7, the question paper page 9 and the memo pages 13-14 ----
F1 = "g(−1) = {3}/{2}(−1) + 7 = {11}/{2}\n"
q7 = [
    answer("7.1", "Write down the coordinates of B.", 1, ["(0 ; 7)", "(7 ; 0)", "(0 ; 8)", "(0 ; 4)"],
           ["On which axis does B lie?", "What is g(0)?"]),
    work("7.2", "Show that b = 1/2.", 2, [
        "4 = −b⁻² + 8\nb⁻² = 4\nb² = {1}/{4}\nb = {1}/{2} (b > 0)",                                  # the memo
        "f(−2) = −({1}/{2})⁻² + 8\n= −4 + 8\n= 4\nSo b = {1}/{2}",                                    # starts from the answer
        "Using B(0 ; 7): 7 = −b⁰ + 8\n7 = −1 + 8\nb⁰ = 1\nSo b = {1}/{2}",                            # B fits f for every b
        "The gradient of g is {3}/{2}\nb = {3}/{2} − 1\nb = {1}/{2}\nSo b = {1}/{2}"],               # the gradient of g used
        ["Which point on f has known coordinates other than B?", "What is b⁻² written as a fraction?"]),
    answer("7.3", "Write down the average gradient of f between A and B.", 2, ["{3}/{2}", "{2}/{3}", "−{3}/{2}", "3"],
           ["A and B are on both graphs: what does that tell you about the straight line through them?", "Average gradient = change in y ÷ "
                                                                                                         "change in x."]),
    answer("7.4", "Write down the equation of the asymptote of f.", 1, ["y = 8", "y = −8", "x = 8", "y = 7"],
           ["Which number in f(x) = −(b)ˣ + 8 moves the graph up or down?", "Is the asymptote horizontal or vertical?"]),
    work("7.5", "Calculate the vertical distance between f and g at x = −1.", 3, [
        "f(−1) = −({1}/{2})⁻¹ + 8 = 6\n" + F1 + "f(−1) − g(−1) = 6 − {11}/{2}\n= {1}/{2}",                     # the memo
        "f(−1) = −({1}/{2})⁻¹ + 8 = 10\n" + F1 + "f(−1) − g(−1) = 10 − {11}/{2}\n= {9}/{2}",                   # (1/2)⁻¹ taken as −2
        "f(−1) = −({1}/{2})⁻¹ + 8 = 6\ng(−1) = {3}/{2}(1) + 7 = {17}/{2}\nf(−1) − g(−1) = 6 − {17}/{2}\n= −{5}/{2}",  # the sign of −1 lost in g
        "f(−1) = −({1}/{2}) + 8 = {15}/{2}\n" + F1 + "f(−1) − g(−1) = {15}/{2} − {11}/{2}\n= 2"],               # the power −1 dropped
        ["What are f(−1) and g(−1)?", "What is (1/2)⁻¹?"]),
    answer("7.6", "Describe the transformation of f to h if h(x) = (1/2)ˣ − 5.", 2,
           ["A reflection in the x-axis, then a translation 3 units up", "A reflection in the y-axis, then a translation 3 units down",
            "A reflection in the x-axis, then a translation 5 units down", "A translation 13 units down"],
           ["What happens to f(x) = −(1/2)ˣ + 8 when every y-value changes sign?", "How far is it from −8 to −5?"]),
    answer("7.7", "For which values of x is f(x) ≥ g(x)?", 2, ["−2 ≤ x ≤ 0", "x ≤ −2 or x ≥ 0", "−2 < x < 0", "x ≥ −2"],
           ["Where do the graphs of f and g meet?", "Between those points, which graph is on top?"])]

# ---- QUESTION 8, the question paper page 10 and the memo pages 14-15 ----
E = "i(eff) = (1 + {0,06}/{12})¹² − 1\n"
q81 = [
    work("8.1", "A Google Chromebook costs R14 500 and depreciates by 13% p.a. compounded annually calculated on the reducing-balance method."
         "\n\nCalculate what a Google Chromebook will be worth after exactly 5 years.", 3, [
        "A = P(1 − i)ⁿ\nA = 14 500(1 − 0,13)⁵\nA = R7 227,10",       # the memo
        "A = P(1 − in)\nA = 14 500(1 − 0,13 × 5)\nA = R5 075,00",    # straight-line depreciation
        "A = P(1 + i)ⁿ\nA = 14 500(1 + 0,13)⁵\nA = R26 715,31",      # growth, not depreciation
        "A = P(1 − i)ⁿ\nA = 14 500(1 − 0,013)⁵\nA = R13 581,69"],    # 13% taken as 0,013
        ["Which formula gives a reducing-balance value after n years?", "What is 13% as a decimal?"])]
G = "A = 15 000(1 + 0,061678)"
q82 = [
    work("8.2.1", "Convert the nominal rates to annual effective rates. (Answers correct to FOUR decimal places)", 4, [
        E + "= 6,1678%\ni(eff) = (1 + {0,1}/{2})² − 1\n= 10,2500%",                                         # the memo
        "i(eff) = (1 + {0,06}/{12})¹²\n= 106,1678%\ni(eff) = (1 + {0,1}/{2})²\n= 110,2500%",                  # the 1 not subtracted
        E + "= 6,1678%\ni(eff) = (1 + {0,1}/{12})¹² − 1\n= 10,4713%",                                        # the second rate compounded monthly
        "i(eff) = (1 + 0,06)¹² − 1\n= 101,2196%\ni(eff) = (1 + 0,1)² − 1\n= 21,0000%"],                      # the yearly rate each period
        ["How many times a year is each rate compounded?", "Which formula links a nominal rate to the effective rate?"]),
    work("8.2.2", "Hence, use the effective rates or otherwise, calculate the future value of the savings at the end of the ten-year period.", 4, [
        G + "⁴(1 + 0,1025)⁶\nA = R34 224,26",                 # the memo
        G + "⁴⁸(1 + 0,1025)¹²\nA = R855 637,29",              # months and half-years with yearly rates
        G + "⁶(1 + 0,1025)⁴\nA = R31 736,76",                 # the periods swapped
        G + "⁴ + 15 000(1 + 0,1025)⁶\nA = R45 995,20"],       # each stretch grown from R15 000
        ["For how many years does each effective rate apply?", "Does the second rate grow R15 000 or the amount after 4 years?"],
        after=["8.2.1"]),
    work("8.2.3", "The interest rate for the first 4 years remains at 6% p.a. compounded monthly. For the next 2 years the interest rate is x% "
         "p.a. compounded quarterly. For the last 4 years the interest rate is x% p.a. compounded semi-annually.\n\nIf Koza receives "
         "R48 897,03 at the end of the 10-year period, determine the interest rate for the last 6 years, i.e. the value of x.", 5, [
        "15 000(1 + {0,06}/{12})⁴⁸(1 + {x}/{4})⁸(1 + {x}/{2})⁸ = 48 897,03\n[(1 + {x}/{4})(1 + {x}/{2})]⁸ = 2,565784627\n"
        "1 + {x}/{2} + {x}/{4} + {x²}/{8} = 1,125\nx² + 6x − 1 = 0\nx = 0,1623 (x ≠ −6,1623)\nInterest rate = 16,23%",          # the memo
        "15 000(1 + {0,06}/{12})⁴⁸(1 + {x}/{4})⁸(1 + {x}/{2})⁸ = 48 897,03\n[(1 + {x}/{4})(1 + {x}/{2})]⁸ = 2,565784627\n"
        "1 + {x}/{2} + {x}/{4} + {x²}/{8} = 2,565784627\nx² + 6x − 12,5263 = 0\nx = 1,6396 (x ≠ −7,6396)\nInterest rate = 163,96%",  # the 8th root not taken
        "15 000(1 + {0,06}/{12})⁴⁸(1 + {x}/{2})¹² = 48 897,03\n(1 + {x}/{2})¹² = 2,565784627\n1 + {x}/{2} = 1,0817\n{x}/{2} = 0,0817\n"
        "x = 0,1634\nInterest rate = 16,34%",                                                                                       # all 6 years semi-annual
        "15 000(1 + {0,06}/{12})⁴(1 + {x}/{4})⁸(1 + {x}/{2})⁸ = 48 897,03\n[(1 + {x}/{4})(1 + {x}/{2})]⁸ = 3,195412832\n"
        "1 + {x}/{2} + {x}/{4} + {x²}/{8} = 1,1563\nx² + 6x − 1,2503 = 0\nx = 0,2016 (x ≠ −6,2016)\nInterest rate = 20,16%"],    # 4 months, not 48
        ["How many quarters are in 2 years, and how many half-years in 4?", "After dividing, how do you undo the power 8?"])]

# ---- QUESTION 9, the question paper page 11 and the memo page 15 ----
OR = "P(A and B) = 0,5 × 0,6 = 0,3\n"
q91 = [
    work("9.1.1", "If there is a trespasser, what is the probability that the trespasser will be detected by at least one camera?", 3, [
        OR + "P(A or B) = P(A) + P(B) − P(A and B)\n= 0,5 + 0,6 − 0,3\n= 0,8",          # the memo
        "P(A and B) = 0\nP(A or B) = P(A) + P(B) − P(A and B)\n= 0,5 + 0,6 − 0\n= 1,1",  # taken as mutually exclusive
        OR + "P(at least one) = P(A and B)\n= 0,5 × 0,6\n= 0,3",                         # both cameras, not at least one
        OR + "P(at least one) = 1 − P(A and B)\n= 1 − 0,3\n= 0,7"],                     # the wrong complement
        ["What does 'independent' tell you about P(A and B)?", "Which rule gives P(A or B)?"]),
    work("9.1.2", "Determine the probability that the trespasser will not be detected.", 2, [
        "P(not detected) = 1 − P(at least one)\n= 1 − 0,8\n= 0,2",       # the memo
        "P(not detected) = 1 − P(A and B)\n= 1 − 0,3\n= 0,7",           # the complement of both, not of at least one
        "P(not detected) = (1 − 0,5) + (1 − 0,6)\n= 0,5 + 0,4\n= 0,9",  # the two misses added
        "P(not detected) = P(A) × P(B)\n= 0,5 × 0,6\n= 0,3"],           # both detecting
        ["'Not detected' is the complement of which event?", "What is P(at least one camera) from 9.1.1?"], after=["9.1.1"])]
ALL = "26 + 9 + 12 + 4 + 24 + 15 + 12"
q92 = [
    work("9.2.1", "Show that x = 8.", 2, [
        "x = 110 − (" + ALL + ")\n= 110 − 102\nx = 8",                                              # the memo
        "26 + 9 + 12 + 8 + 4 + 24 + 15 + 12 = 110\n110 = 110\nx = 8",                               # starts from the answer
        "x = (" + ALL + ") − 110\n= −8\nx = 8 (a number of learners cannot be negative)",           # the subtraction the wrong way round
        "Accounting: 12 + x + 4 + 15 = 39 (an Accounting total assumed)\n31 + x = 39\nx = 8"],      # a total the diagram does not give
        ["What must all the numbers in the diagram, with x, add up to?", "Have you counted the 12 learners outside the circles?"]),
    work("9.2.2", "Calculate the probability that a learner chosen at random does only one of the three subjects.", 2, [
        "P(only one) = {26 + 24 + 15}/{110}\n= {65}/{110} ≈ 0,59",         # the memo
        "P(only one) = {9 + 12 + 4}/{110}\n= {25}/{110} ≈ 0,23",           # exactly two subjects
        "P(only one) = {26 + 24 + 15}/{98}\n= {65}/{98} ≈ 0,66",           # the 12 outside left out of the total
        "P(only one) = {26 + 24 + 15 + 12}/{110}\n= {77}/{110} = 0,7"],    # the 12 outside counted as one subject
        ["Which regions hold learners who do exactly one subject?", "Out of how many learners is the one chosen?"]),
    work("9.2.3", "Calculate the probability that a learner chosen at random does Mathematics and Accounting, but not Physical Sciences.", 2, [
        "P = {12}/{110}\n= {6}/{55} ≈ 0,11",            # the memo's fraction (its 0,12 a slip)
        "P = {12 + 8}/{110}\n= {2}/{11} ≈ 0,18",        # the centre x included
        "P = {26 + 12 + 15}/{110}\n= {53}/{110} ≈ 0,48",  # Mathematics only and Accounting only added
        "P = {12}/{55}\n= {12}/{55} ≈ 0,22"],            # out of the Mathematics learners
        ["Which single region is in M and A but outside P?", "Out of how many learners is the one chosen?"])]

# ---- QUESTION 10, the question paper page 12 and the memo page 16 ----
RR = "P(R ; R) = {1}/{3} × {3}/{8} = {1}/{8}\nP(B ; B) = {1}/{3} × {5}/{8} = {5}/{24}\n"
q10 = [
    work("10", "Bennie is going to spin both spinners. What is the probability that it lands on the same colour after spinning each spinner "
         "once?", 8, [
        RR + "P(same colour) = {1}/{8} + {5}/{24}\n= {1}/{3}",                                                              # the memo
        RR + "P(same colour) = {1}/{8} × {5}/{24}\n= {5}/{192}",                                                            # the two outcomes multiplied
        "P(R ; R) = {1}/{3} × {1}/{3} = {1}/{9}\nP(B ; B) = {1}/{3} × {1}/{3} = {1}/{9}\nP(same colour) = {1}/{9} + {1}/{9}\n= {2}/{9}",  # spinner 2 read as 3 equal colours
        RR + "P(same colour) = 1 − ({1}/{8} + {5}/{24})\n= {2}/{3}"],                                                      # the complement taken
        ["Which colours are on both spinners, and how many of spinner 2's eight parts are each colour?", "For each colour, multiply the "
                                                                                                        "chances on the two spinners; then "
                                                                                                        "combine the colours."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Equations and inequalities", "marks": 9, "lead": "Solve for x:", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Equations", "marks": 7, "lead": "Given: 14/p = p + 5", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Simultaneous equations", "marks": 6, "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Exponents and equations", "marks": 4, "items": q14},
    {"id": "2.1", "title": "Question 2.1", "kind": "Surds", "marks": 4, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Exponential equations", "marks": 8, "lead": "Solve for x:", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Surds", "marks": 5, "items": q23},
    {"id": "3.1", "title": "Question 3.1", "kind": "Linear patterns", "marks": 6, "lead": "Consider the linear number pattern: −5 ; −9 ; −13 ; …",
     "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Linear patterns", "marks": 5, "items": q32},
    {"id": "4", "title": "Question 4", "kind": "Quadratic patterns", "marks": 15, "lead": "Given the number pattern 24 ; 10 ; 0 ; −6 ; …",
     "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Hyperbola", "marks": 17,
     "lead": "The lines y = −x + 4 and y = x − 2 are the axes of symmetry of the function f(x) = −3/(x + p) + q.", "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Parabola", "marks": 16,
     "lead": "Sketched below is the graph of f(x) = x² − 4x − 5 for x ∈ (−∞ ; 6].\nA and B are the x-intercepts and C the y-intercept of f.",
     "figure": P.fig("Q6", "The parabola f, opening upwards, cuts the x-axis at A, left of the origin, and at B, right of it, and the y-axis "
                           "at C below the origin; it ends at a dot above x = 6, with a dotted line down to the x-axis."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Exponential graph and straight line", "marks": 13,
     "lead": "The graphs of f(x) = −(b)ˣ + 8 and g(x) = (3/2)x + 7 are drawn below.\nA(−2 ; 4) and B are points of intersection of f and g. "
             "B is the y-intercept of both graphs f and g.",
     "figure": P.fig("Q7", "The straight line g and the exponential graph f meet at A(−2 ; 4), left of the y-axis, and at B on the y-axis. "
                           "f rises from the bottom left and levels off below a dashed horizontal asymptote; g keeps rising to the top "
                           "right."), "items": q7},
    {"id": "8.1", "title": "Question 8.1", "kind": "Depreciation", "marks": 3, "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Compound and effective interest", "marks": 13,
     "lead": "Koza deposits R15 000 into a bank account for a period of 10 years. The interest rate for the first four years is 6% per annum "
             "compounded monthly. For the next six years, the interest rate changes to 10% per annum compounded semi-annually.", "items": q82},
    {"id": "9.1", "title": "Question 9.1", "kind": "Independent events", "marks": 5,
     "lead": "A certain company uses a camera detector system to detect trespassers. Two independent cameras, A and B are installed, one at "
             "the front main gate and the other one at the back of the building. If someone trespasses, the probability that the person "
             "will be detected by camera A is 0,5 and the probability that the person will be detected by camera B is 0,6.", "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Venn diagrams", "marks": 6,
     "lead": "At a certain high school, a survey was carried out on 110 learners, about their subject choices. The Venn diagram shows the "
             "results of the survey in terms of:\n• Mathematics (M)\n• Physical Sciences (P)\n• Accounting (A)",
     "figure": P.fig("Q9", "A Venn diagram of three circles, M, P and A, in a rectangle: 26 in M only, 24 in P only, 15 in A only, 9 in M "
                           "and P only, 12 in M and A only, 4 in P and A only, x in all three, and 12 outside the circles."), "items": q92},
    {"id": "10", "title": "Question 10", "kind": "Probability", "marks": 8,
     "lead": "Bennie has two fair spinners. (Circles are divided into 3 and 8 equal parts, respectively)",
     "figure": P.fig("Q10", "Spinner 1: a circle in three equal parts, red, blue and green. Spinner 2: a circle in eight equal parts, three "
                            "red and five blue."), "items": q10},
]
P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
         [P.flag_workings("In a 'show that' (4.1, 5.1, 7.2, 9.2.1) every option ends in the given result; a wrong one reaches it through a "
                          "wrong step or by starting from the answer."),
          P.flag_answers(),
          {"n": "6.3", "kind": "no_fit", "detail": "One read-off number stays typed on the keypad: 6.3 (the length of AB: 6, exact)."},
          {"n": "5.4", "kind": "no_fit", "detail": "The sketch of f is BUILT on a grid: the learner places both asymptotes and both "
                                                   "intercepts and draws the branches; the memo's three criteria (shape, asymptotes, "
                                                   "intercepts) are marked from them."},
          {"n": "10", "kind": "no_fit", "detail": "Question 10 (8 marks) plays as one working, 0 or full marks: the memo's alternative "
                                                  "marking is the calculation (1/3 × 5/8, 1/3 × 3/8, the sum); its tree is a method the "
                                                  "question does not ask for."},
          {"n": "1.3", "kind": "memo_issue", "detail": "The memo (page 4) collects 6y − 2y as −4y: 2y² − 4y − 6 = 0, y = 3 or −1, x = 10 or "
                                                       "−2, which do not satisfy x² − 2xy − y² − 7 = 0 (100 − 60 − 9 − 7 = 24). The right "
                                                       "option is the corrected working: 2y² + 4y − 6 = 0, y = −3 or 1, x = −8 or 4 (both "
                                                       "pairs check in both equations). The slip's reading is in no option."},
          {"n": "4.2", "kind": "memo_issue", "detail": "The memo's mark column (page 9) ticks a = 6, b = −9, c = 6; its working, and the "
                                                       "ticked Tₙ = 2n² − 20n + 42, give a = 2, b = −20, c = 42. The right option is the "
                                                       "working; no option uses the mark column's values."},
          {"n": "6.4", "kind": "memo_issue", "detail": "The memo (page 12) writes g(x) = x² − 8x − 12; its own line x² − 4x + 4 − 4x + 8 − 5 "
                                                       "+ 5 is x² − 8x + 12. The right option is x² − 8x + 12; the slip's reading is in no "
                                                       "option."},
          {"n": "9.2.3", "kind": "memo_issue", "detail": "The memo (page 15) rounds 6/55 to 0,12; 6/55 = 0,109…, so 0,11. The right option "
                                                         "is 6/55 ≈ 0,11; no option ends in 0,12."},
          {"n": "2.2.2", "kind": "low_confidence", "detail": "The paper prints 3.5ˣ: the dot is a multiplication (the memo factors 5ˣ(3 − "
                                                             "1/5)), written 3 · 5ˣ."}],
         {"1": 26, "2": 17, "3": 11, "4": 15, "5": 17, "6": 16, "7": 13, "8": 16, "9": 11, "10": 8}, 150,
         {"1.2.2": ["1.2.1"], "3.1.3": ["3.1.2"], "4.3": ["4.2"], "4.4": ["4.2"], "4.5": ["4.2"], "5.4": ["5.2", "5.3"], "5.6": ["5.2"],
          "6.3": ["6.2"], "6.6": ["6.1"], "8.2.2": ["8.2.1"], "9.1.2": ["9.1.1"]},
         "Questions 1 to 10 (the whole paper)")
