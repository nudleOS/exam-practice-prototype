"""Grade 10 Mathematics P1 November 2024 (North West Department of Education, provincial assessment), the whole paper (Questions 1
to 9, 100 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json` like any ingested
paper. Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are
ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment, the question paper PDF (English, 9 pages,
text layer) and the marking guidelines PDF (English and Afrikaans, 7 pages, text layer). Both were read from their page images
too, where the text layer garbles fractions and powers.

  python tools/ingest/transcribe_g10_math_p1_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-math-p1-2024-11-nw/15-NOVEMBER-2024-S2-GR10-MATHEMATICS-P1-QP-ENG.pdf" "uploads/provincial/g10-math-p1-2024-11-nw/15-NOVEMBER-2024-S2-GR10-MATHEMATICS-P1-MG-ENG-AFR.pdf" --id g10-math-p1-2024-11-nw --from-json

The memo's shapes map by the Grade 12 rulings (provincial.py). The sketch 5.1 is built on a grid: f (a parabola: both x-intercepts,
the turning point and its shape) and g (an exponential graph: its y-intercept, its asymptote and its shape, picked, since one point
and the asymptote leave the curve open) on one set of axes. The Venn diagram 8.3 is pick the drawing (pictures_lower.py). 3.3.2
("describe the pattern in your own words") plays as statements. 8.1 prints "complimentary"; written "complementary" here.
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.5286)."""
from provincial import Paper

P = Paper("g10-math-p1-2024-11-nw", 595.32, 842.04, {
    "Q3": [4, 125, 140, 500, 208],    # diagrams 1, 2 and 3 of shaded and white squares
    "Q6": [5, 85, 342, 425, 628]}, start=4)   # f, g, A(4 ; 4), B, C, D(0 ; −4), E
work, answer, num, draw, stmt = P.work, P.answer, P.num, P.draw, P.stmt

# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
q11 = [
    answer("1.1.1", "x² − 16x + 15", 1, ["(x − 1)(x − 15)", "(x + 1)(x − 15)", "(x − 3)(x − 5)", "(x + 1)(x + 15)"],
           ["Which two numbers multiply to 15 and add to −16?", "Are both numbers negative or of opposite signs?"]),
    work("1.1.2", "a(6a + 2b) − 3(3a + b)", 2, [
        "= 2a(3a + b) − 3(3a + b)\n= (3a + b)(2a − 3)",          # the memo
        "= 2a(3a + b) − 3(3a + b)\n= (3a + b)(2a + 3)",          # the sign of 3 lost
        "= a(6a + 2b) − 3(3a + b)\n= (6a + 2b)(a − 3)",          # (6a + 2b) and (3a + b) taken as the same bracket
        "= 2a(3a + b) − 3(3a + b)\n= 2a − 3(3a + b)"],           # the common bracket taken out of one term only
        ["What common factor can you take out of 6a + 2b?", "Once both terms have the same bracket, what is left over?"])]
q12 = [
    work("1.2.1", "27^(2/3)", 2, [
        "= (3³)^(2/3)\n= 3²\n= 9",                                # the memo
        "= 27 × {2}/{3}\n= {54}/{3}\n= 18",                       # the power read as a product
        "= (3³)^(2/3)\n= 3²\n= 6",                                # 3² read as 3 × 2
        "= {1}/{(3³)^(2/3)}\n= {1}/{3²}\n= {1}/{9}"],             # a positive power read as a negative one
        ["How can you write 27 as a power of 3?", "What do you do with the powers when you raise a power to a power?"]),
    work("1.2.2", "(x + 3)/(x − 3) × (x³ − 27)/(x² − 9) ÷ (x² + 3x + 9)/(x − 3)", 4, [
        "= {x + 3}/{x − 3} × {x³ − 27}/{x² − 9} × {x − 3}/{x² + 3x + 9}\n"
        "= {x + 3}/{x − 3} × {(x − 3)(x² + 3x + 9)}/{(x − 3)(x + 3)} × {x − 3}/{x² + 3x + 9}\n= 1",                    # the memo
        "= {x + 3}/{x − 3} × {x³ − 27}/{x² − 9} × {x² + 3x + 9}/{x − 3}\n"
        "= {x + 3}/{x − 3} × {(x − 3)(x² + 3x + 9)}/{(x − 3)(x + 3)} × {x² + 3x + 9}/{x − 3}\n"
        "= {(x² + 3x + 9)²}/{(x − 3)²}",                                                                              # ÷ without the flip
        "= {x + 3}/{x − 3} × {x³ − 27}/{x² − 9} × {x − 3}/{x² + 3x + 9}\n"
        "= {x + 3}/{x − 3} × {(x − 3)(x² − 3x + 9)}/{(x − 3)(x + 3)} × {x − 3}/{x² + 3x + 9}\n"
        "= {x² − 3x + 9}/{x² + 3x + 9}",                                                                              # x³ − 27 with the sum's signs
        "= {x + 3}/{x − 3} × {x³ − 27}/{x² − 9} × {x − 3}/{x² + 3x + 9}\n"
        "= {x + 3}/{x − 3} × {(x − 3)(x² + 3x + 9)}/{(x − 3)(x − 3)} × {x − 3}/{x² + 3x + 9}\n= {x + 3}/{x − 3}"],  # x² − 9 as (x − 3)²
        ["What does dividing by a fraction become?", "How do the difference of two cubes and the difference of two squares factorise?"]),
    work("1.2.3", "(3ˣ⁺¹ − 3ˣ⁺²)/(3ˣ⁺² + 3ˣ)", 4, [
        "= {3ˣ⁺¹(1 − 3)}/{3ˣ(3² + 1)}\n= {3¹(−2)}/{10}\n= {−6}/{10}\n= −{3}/{5}",      # the memo
        "= {3ˣ⁺¹(1 − 3)}/{3ˣ(3² + 1)}\n= {3¹(−2)}/{9}\n= {−6}/{9}\n= −{2}/{3}",         # 3² + 1 taken as 9
        "= {3ˣ⁺¹(1 − 3)}/{3ˣ(3² + 1)}\n= {3¹(2)}/{10}\n= {6}/{10}\n= {3}/{5}",           # the sign of 1 − 3 lost
        "= {3ˣ⁺¹(1 − 3)}/{3ˣ(3² + 1)}\n= {3(−2)}/{3(10)}\n= {−6}/{30}\n= −{1}/{5}"],     # 3ˣ⁺¹ ÷ 3ˣ taken as 1, the 3 left below
        ["Which power of 3 is a common factor of the top, and of the bottom?", "What is 3ˣ⁺¹ ÷ 3ˣ?"])]

# ---- QUESTION 2, the question paper page 3 and the memo page 3 ----
q21 = [
    work("2.1.1", "2 · 3²ˣ = 18", 4, [
        "2 · 3²ˣ = 2 · 3²\n3²ˣ = 3²\n2x = 2\nx = 1",               # the memo
        "3²ˣ = 18 − 2\n3²ˣ = 16\n2x = 2,52\nx = 1,26",            # 2 subtracted, not divided
        "2 · 3²ˣ = 18\n3²ˣ = 9\n2x = 9\nx = {9}/{2}",             # 9 not written as a power of 3
        "2 · 3²ˣ = 2 · 3²\n3²ˣ = 3²\nx + 2 = 2\nx = 0"],          # 2x read as x + 2
        ["What must you do to both sides before you deal with the power?", "How can you write 9 as a power of 3?"]),
    work("2.1.2", "(2x − 1)/3 ≥ 2x + 1", 4, [
        "2x − 1 ≥ 3(2x + 1)\n2x − 1 ≥ 6x + 3\n−4x ≥ 4\nx ≤ −1",                 # the memo
        "2x − 1 ≥ 3(2x + 1)\n2x − 1 ≥ 6x + 3\n−4x ≥ 4\nx ≥ −1",                 # the sign kept when dividing by −4
        "2x − 1 ≥ 3(2x + 1)\n2x − 1 ≥ 6x + 1\n−4x ≥ 2\nx ≤ −{1}/{2}",           # 3 multiplied into 2x only
        "2x − 1 ≥ 3(2x + 1)\n2x − 1 ≥ 6x + 3\n−4x ≥ 2\nx ≤ −{1}/{2}"],          # −1 moved without its sign change
        ["What do you multiply both sides by to clear the fraction?", "What happens to the inequality sign when you divide by a "
                                                                      "negative number?"]),
    work("2.1.3", "2x² − x − 10 = 0", 4, [
        "(2x − 5)(x + 2) = 0\n2x − 5 = 0 or x + 2 = 0\nx = {5}/{2} or x = −2",   # the memo
        "(2x + 5)(x − 2) = 0\n2x + 5 = 0 or x − 2 = 0\nx = −{5}/{2} or x = 2",   # the signs in the factors swapped
        "(2x − 5)(x + 2) = 0\n2x − 5 = 0 or x + 2 = 0\nx = 5 or x = −2",         # 2x = 5 read as x = 5
        "(2x − 2)(x + 5) = 0\n2x − 2 = 0 or x + 5 = 0\nx = 1 or x = −5"],        # factors of −10 that do not give −x
        ["Which factors of 2 × (−10) = −20 add to −1?", "When is a product of two factors equal to zero?"])]
q22 = [
    work("2.2", "How much must be added to (x + 5)(x − 5) so that it will be equal to (x + 1)(x − 25)?", 4, [
        "(x + 5)(x − 5) = x² − 25\n(x + 1)(x − 25) = x² − 24x − 25\n−24x must be added",          # the memo
        "(x + 5)(x − 5) = x² + 25\n(x + 1)(x − 25) = x² − 24x − 25\n−24x − 50 must be added",     # the difference of squares as + 25
        "(x + 5)(x − 5) = x² − 25\n(x + 1)(x − 25) = x² − 26x − 25\n−26x must be added",          # the middle term −25x − x
        "(x + 5)(x − 5) = x² − 25\n(x + 1)(x − 25) = x² − 24x − 25\n24x must be added"],          # subtracted the wrong way round
        ["What do you get when you expand each product?", "What is the second expression minus the first?"])]
SUB = "y = 3x − 2\n7x − 2(3x − 2) = 8\n"
q23 = [
    work("2.3", "Solve for x and y simultaneously:\ny − 3x = −2 and 7x − 2y = 8", 4, [
        SUB + "7x − 6x + 4 = 8\nx = 4\ny = 3(4) − 2 = 10",                                          # the memo
        "y = 3x + 2\n7x − 2(3x + 2) = 8\n7x − 6x − 4 = 8\nx = 12\ny = 3(12) + 2 = 38",              # −3x moved without its sign change
        SUB + "7x − 6x − 4 = 8\nx = 12\ny = 3(12) − 2 = 34",                                        # −2 × −2 taken as −4
        SUB + "7x − 6x − 2 = 8\nx = 10\ny = 3(10) − 2 = 28"],                                       # −2 multiplied into 3x only
        ["Which equation is easier to make y the subject of?", "What is −2 × (−2)?"])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 3-4 ----
q31 = [
    answer("3.1.1", "Write down the formula or general term for the number of shaded squares.", 1,
           ["Tₙ = 3n", "Tₙ = 2n + 1", "Tₙ = n + 2", "Tₙ = 4n − 1"],
           ["How many shaded squares are in diagrams 1, 2 and 3?", "By how many does the number grow from one diagram to the next?"]),
    work("3.1.2", "Determine the number of shaded squares of diagram 300.", 2, [
        "T₃₀₀ = 3(300)\nT₃₀₀ = 900",           # the memo
        "T₃₀₀ = 3 + 300\nT₃₀₀ = 303",          # added, not multiplied
        "T₃₀₀ = 300 ÷ 3\nT₃₀₀ = 100",          # divided, not multiplied
        "T₃₀₀ = 300³\nT₃₀₀ = 27 000 000"],     # 3n read as n³
        ["Which value of n is diagram 300?", "What do you get when you put that n into your general term?"], after=["3.1.1"]),
    work("3.1.3", "Which diagram will consist of 1 500 shaded squares?", 2, [
        "1 500 = 3n\nn = 500",                 # the memo
        "1 500 = 3n\nn = 4 500",               # multiplied, not divided
        "1 500 = 3 + n\nn = 1 497",            # 3n read as 3 + n
        "Tₙ = 3(1 500)\nTₙ = 4 500"],          # 1 500 put in for n
        ["Is 1 500 a diagram number or a number of squares?", "Which n makes your general term equal to 1 500?"], after=["3.1.1"])]
TS = "TERMS repeats after the fifth letter\n"
q32 = [
    work("3.2", "If the pattern TERMSTERMS... continues in the same way, what will be the 383rd letter?", 3, [
        TS + "383 ÷ 5 = 76 remainder 3\nThe 383rd letter is R",          # the memo
        TS + "383 ÷ 5 = 76 remainder 3\nThe 383rd letter is M",          # the letter after the remainder
        TS + "383 ÷ 5 = 76,6 ≈ 77 words\nThe 383rd letter is S",         # rounded up to whole words
        TS + "383 ÷ 3 = 127 remainder 2\nThe 383rd letter is E"],        # divided by 3, the remainder's place
        ["How many letters are in one repeat of the pattern?", "After all the complete repeats, how many letters are left over?"])]
q33 = [
    answer("3.3.1", "Write down the next two terms of the pattern.", 2, ["36 ; 43", "35 ; 41", "36 ; 44", "43 ; 50"],
           ["What is added to each term to get the next one?", "Does that difference stay the same?"]),
    stmt("3.3.2", "Describe the pattern in your own words. Choose the description.", 2,
         ["Add 7 to the previous term to get the next term.", "Each term is 7 more than the term before it."],
         ["Multiply the previous term by 7 to get the next term.", "Add 8 to the previous term to get the next term.",
          "Each term is double the term before it.", "Subtract 7 from the previous term to get the next term."],
         ["What is the difference between consecutive terms?", "Is it the same each time?"], 2)]

# ---- QUESTION 4, the question paper page 4 and the memo page 4 ----
q41 = [
    work("4.1", "Mark has booked himself a hotel room for three nights during his visit to New York. The exchange rate during his visit "
         "was $1 = R9,10. The cost per night of the hotel was $450. How much did the three nights cost him in rands?", 3, [
        "3 × $450 = $1 350\n$1 350 × R9,10\n= R12 285",           # the memo
        "3 + $450 = $453\n$453 × R9,10\n= R4 122,30",             # added the nights, not multiplied
        "3 × $450 = $1 350\n$1 350 ÷ R9,10\n= R148,35",           # divided by the rate, not multiplied
        "$450 × R9,10 = R4 095\nR4 095 ÷ 3\n= R1 365"],           # divided by the nights
        ["What do the three nights cost in dollars?", "Does R9,10 for every $1 mean you multiply or divide?"])]
BAL = "Balance = R20 000 − R3 000 − R2 000 = R15 000\n"
q42 = [
    work("4.2.1", "Calculate the total interest paid.", 6, [
        BAL + "Total instalments = 24 × R900 = R21 600\nTotal interest = R21 600 − R15 000\n= R6 600",                    # the memo
        "Balance = R20 000 − R2 000 = R18 000\nTotal instalments = 24 × R900 = R21 600\nTotal interest = R21 600 − R18 000\n"
        "= R3 600",                                                                                                       # the trade-in ignored
        "Balance = R20 000\nTotal instalments = 24 × R900 = R21 600\nTotal interest = R21 600 − R20 000\n= R1 600",       # the full price as the loan
        BAL + "Total instalments = 12 × R900 = R10 800\nTotal interest = R15 000 − R10 800\n= R4 200"],                   # one year of instalments
        ["How much did Belinda still owe after the trade-in and the deposit?", "How many monthly instalments are there in 2 years?"]),
    work("4.2.2", "Calculate the simple interest rate.", 4, [
        "A = P(1 + ni)\n21 600 = 15 000(1 + 2i)\n{21 600}/{15 000} − 1 = 2i\ni = 0,22\nr = 22%",                         # the memo
        "A = P(1 + ni)\n21 600 = 15 000(1 + 24i)\n{21 600}/{15 000} − 1 = 24i\ni = 0,0183\nr = 1,83%",                  # n in months
        "A = P(1 + ni)\n6 600 = 15 000(1 + 2i)\n{6 600}/{15 000} − 1 = 2i\ni = −0,28\nr = −28%",                        # the interest as A
        "A = P(1 + ni)\n21 600 = 15 000(1 + 2i)\n{21 600}/{15 000} − 1 = 2i\ni = 0,44\nr = 44%"],                       # not divided by 2
        ["What are A, P and n here?", "Is n counted in years or in months?"], after=["4.2.1"])]

# ---- QUESTION 5, the question paper page 5 and the memo page 5 ----
q5 = [
    draw("5.1", "Sketch the graphs of f(x) = −x² + 4 and g(x) = 2ˣ + 3 on the same set of axes.", 5, [
        ["f: the intercepts", 1], ["f: the shape and the turning point", 1], ["g: the intercept", 1], ["g: the shape", 1],
        ["g: the asymptote", 1]],
        ["Where does f cut the axes, and where is its turning point?", "What is g(0), and which horizontal line does g approach?"],
        memo="The memo's sketch: f opening downwards with its turning point (0 ; 4) and x-intercepts (−2 ; 0) and (2 ; 0); g increasing "
             "from just above its dashed asymptote y = 3 on the left, through (0 ; 4).",
        # built on a grid (2026-10-12): f and g on one set of axes, each memo criterion its features (or a shape); f's two x-intercepts
        # are one criterion (one carries its mark) and its turning point goes with its shape; g's one point and its asymptote leave the
        # curve open, so its shape is picked. f's turning point and g's y-intercept are both (0 ; 4)
        build={"kind": "sketch", "family": "parabola", "x": [-3, 3, 1], "y": [-5, 11, 1], "features": [
            {"id": "fx1", "kind": "point", "label": "x-intercept of f", "at": [-2, 0], "tol": 0, "marks": 1, "crit": 0, "graph": "f"},
            {"id": "fx2", "kind": "point", "label": "x-intercept of f", "at": [2, 0], "tol": 0, "marks": 0, "crit": 0, "graph": "f"},
            {"id": "ftp", "kind": "point", "label": "turning point of f", "at": [0, 4], "tol": 0, "marks": 0, "crit": 1, "graph": "f",
             "turn": True},
            {"id": "gy", "kind": "point", "label": "y-intercept of g", "at": [0, 4], "tol": 0, "marks": 1, "crit": 2, "graph": "g"},
            {"id": "gha", "kind": "hline", "label": "asymptote of g", "at": 3, "tol": 0, "marks": 1, "crit": 4, "graph": "g"}],
               "graphs": [{"id": "f", "family": "parabola", "label": "f",
                           "shape": {"label": "Shape of f", "answer": "∩", "marks": 1, "crit": 1}},
                          {"id": "g", "family": "exponential", "label": "g",
                           "shape": {"label": "Shape of g", "answer": "increasing", "marks": 1, "crit": 3,
                                     "pick": ["increasing", "decreasing"]}}]}),
    answer("5.2", "Write down the coordinates of the turning point of f.", 1, ["(0 ; 4)", "(4 ; 0)", "(0 ; −4)", "(2 ; 0)"],
           ["Where is the axis of symmetry of f(x) = −x² + 4?", "What is f(0)?"]),
    answer("5.3", "The graph of h(x) = x² − 4 is obtained by transforming the graph of f. Describe the transformation that maps the "
                  "graph of f onto the graph of h.", 2,
           ["A reflection in the x-axis", "A reflection in the y-axis", "A shift of 8 units down", "A reflection in the line y = x"],
           ["How is h(x) related to −f(x)?", "Which axis flips a graph's y-values to their opposites?"])]

# ---- QUESTION 6, the question paper page 5 and the memo pages 5-6 ----
q6 = [
    answer("6.1", "Determine the values of m and c.", 2,
           ["m = 2 and c = −4", "m = −2 and c = −4", "m = 2 and c = 4", "m = {1}/{2} and c = −4"],
           ["Where does g cut the y-axis?", "What is the gradient between A(4 ; 4) and D(0 ; −4)?"]),
    answer("6.2", "Write down the range of f.", 2, ["y ∈ ℝ, y ≠ −2", "y ∈ ℝ, y ≠ 0", "y > −2", "y ∈ ℝ, y ≠ 2"],
           ["Which horizontal line does f approach but never reach?", "Does f take every other y-value?"]),
    work("6.3", "Determine the coordinates of the point(s) of intersection of the two graphs algebraically.", 4, [
        "{4}/{x} − 2 = 2x − 4\n4 − 2x = 2x² − 4x\n0 = 2x² − 2x − 4\n0 = 2(x − 2)(x + 1)\nB(2 ; 0) and E(−1 ; −6)",          # the memo
        "{4}/{x} − 2 = 2x − 4\n4 − 2x = 2x² − 4x\n0 = 2x² − 2x − 4\n0 = 2(x + 2)(x − 1)\nB(1 ; −2) and E(−2 ; −8)",         # the signs in the factors swapped
        "{4}/{x} − 2 = 2x − 4\n4 − 2 = 2x² − 4x\n0 = 2x² − 4x − 2\nx = 1 ± √2\nB(2,41 ; 0,83) and E(−0,41 ; −4,83)",       # x multiplied into 4 only
        "{4}/{x} − 2 = 2x − 4\n4 − 2x = 2x² − 4x\n0 = 2x² − 2x + 4\nΔ = (−2)² − 4(2)(4) = −28\nNo points of intersection"],  # 4 moved without its sign change
        ["What equation do you get when you set f(x) equal to g(x)?", "What do you multiply both sides by to clear the fraction?"],
        after=["6.1"]),
    answer("6.4", "Determine the value(s) of x for which g(x) ≥ f(x).", 2,
           ["−1 ≤ x < 0 or x ≥ 2", "−1 ≤ x ≤ 2", "x ≤ −1 or 0 < x ≤ 2", "−1 ≤ x ≤ 0 or x ≥ 2"],
           ["Where is the line on or above the hyperbola?", "Can x be 0, where f has its asymptote?"], after=["6.3"]),
    work("6.5", "Calculate the length of AC.", 3, [
        "f(4) = {4}/{4} − 2\n= −1\nAC = 4 + 1\n= 5 units",           # the memo
        "f(4) = {4}/{4} − 2\n= −1\nAC = 4 − 1\n= 3 units",           # the y-values subtracted the wrong way
        "f(4) = {4}/{4 − 2}\n= 2\nAC = 4 − 2\n= 2 units",            # 4/x − 2 read as 4/(x − 2)
        "g(4) = 2(4) − 4\n= 4\nAC = 4 − 0\n= 4 units"],              # C taken on the x-axis
        ["What is the y-value of C, on f at x = 4?", "How far is it from y = 4 down to that y-value?"])]

# ---- QUESTION 7, the question paper page 6 and the memo pages 6-7 ----
q7 = [
    answer("7.1", "Write down the equation of the asymptote of h.", 1, ["y = −2", "y = 2", "x = −2", "y = 0"],
           ["What does the range y > −2 tell you?", "Is the asymptote of an exponential graph horizontal or vertical?"]),
    work("7.2", "Determine the equation of h.", 4, [
        "a = 1 and q = −2\n0 = (1)b¹ − 2\nb = 2\nh(x) = 2ˣ − 2",              # the memo
        "a = 1 and q = 2\n0 = (1)b¹ + 2\nb = −2\nh(x) = (−2)ˣ + 2",           # q read off the range with the sign lost
        "a = 1 and q = −2\n0 = (1)b¹ − 2\nb = −2\nh(x) = (−2)ˣ − 2",          # −2 moved without its sign change
        "a = 2 and q = −2\n0 = 2b¹ − 2\nb = 1\nh(x) = 2 · 1ˣ − 2"],            # a = 2, though a < 2
        ["Which integer lies strictly between 0 and 2?", "What equation do you get when you substitute A(1 ; 0)?"], after=["7.1"]),
    answer("7.3", "Write down the y-intercept of h.", 1, ["(0 ; −1)", "(0 ; −2)", "(0 ; 1)", "(1 ; 0)"],
           ["What is x at the y-intercept?", "What is 2⁰?"], after=["7.2"])]

# ---- QUESTION 8, the question paper page 6 and the memo page 7 ----
q8 = [
    work("8.1", "Determine whether events A and B are complementary.", 2, [
        "P(A) + P(B) = 0,43 + 0,37\n= 0,80\nP(A) + P(B) ≠ 1, so not complementary",            # the memo
        "P(A) × P(B) = 0,43 × 0,37\n= 0,1591\nP(A) × P(B) = P(A and B), so complementary",       # independent taken as complementary
        "P(A) + P(B) = 0,43 + 0,37\n= 0,80\nP(A) + P(B) < 1, so complementary",                 # any sum below 1 taken as complementary
        "P(A and B) = 0,1591\nP(A and B) ≠ 0\nso complementary"],                                 # overlapping taken as complementary
        ["What must P(A) + P(B) be for complementary events?", "What is 0,43 + 0,37?"]),
    answer("8.2", "Are events A and B mutually exclusive? Explain your answer.", 2,
           ["No, since P(A and B) ≠ 0", "Yes, since P(A and B) ≠ 0", "Yes, since P(A) + P(B) ≠ 1", "No, since P(A) + P(B) ≠ 1"],
           ["What is P(A and B) for mutually exclusive events?", "Is P(A and B) zero here?"]),
    draw("8.3", "Draw a Venn diagram to represent the information above.", 4, [
        ["0,2709 in A only", 1], ["0,1591 in A and B", 1], ["0,2109 in B only", 1], ["0,3591 outside A and B", 1]],
        ["What is left of P(A) once the overlap is taken out?", "What is left of the whole sample space outside both circles?"],
        memo="The memo's diagram: circles A and B in a rectangle: 0,2709 in A only, 0,1591 in both, 0,2109 in B only, 0,3591 outside.")]

# ---- QUESTION 9, the question paper page 7 and the memo page 7 ----
q9 = [
    work("9.1", "P(not A)", 2, [
        "P(not A) = 1 − P(A)\n= 1 − {2}/{3}\n= {1}/{3}",       # the memo
        "P(not A) = 1 + P(A)\n= 1 + {2}/{3}\n= {5}/{3}",       # added, not subtracted
        "P(not A) = P(A) − 1\n= {2}/{3} − 1\n= −{1}/{3}",      # subtracted the wrong way round
        "P(not A) = {1}/{P(A)}\n= {3}/{2}\n= 1,5"],            # the complement read as the reciprocal
        ["What do P(A) and P(not A) add up to?", "Can a probability be more than 1 or negative?"]),
    work("9.2", "P(B)", 2, [
        "P(B) = 1 − P(B′)\n= 1 − {3}/{5}\n= {2}/{5}",          # the memo
        "P(B) = P(B′)\n= {3}/{5}\n= 0,6",                      # B′ read as B
        "P(B) = 1 + P(B′)\n= 1 + {3}/{5}\n= {8}/{5}",          # added, not subtracted
        "P(B) = 1 − P(B′)\n= {1 − 3}/{5}\n= −{2}/{5}"],        # 1 taken as 1/5
        ["What does B′ mean?", "What do P(B) and P(B′) add up to?"]),
    work("9.3", "P(A and B)", 3, [
        "P(A or B) = P(A) + P(B) − P(A and B)\n{4}/{7} = {2}/{3} + {2}/{5} − P(A and B)\nP(A and B) = {52}/{105}",     # the memo
        "P(A or B) = P(A) + P(B) − P(A and B)\n{4}/{7} = {2}/{3} + {3}/{5} − P(A and B)\nP(A and B) = {73}/{105}",     # P(B′) used for P(B)
        "P(A or B) = P(A) + P(B) + P(A and B)\n{4}/{7} = {2}/{3} + {2}/{5} + P(A and B)\nP(A and B) = −{52}/{105}",    # the sign in the rule
        "P(A and B) = P(A) × P(B)\n= {2}/{3} × {2}/{5}\nP(A and B) = {4}/{15}"],                                       # independence assumed
        ["Which rule links P(A or B), P(A), P(B) and P(A and B)?", "Which value do you use for P(B): 2/5 or 3/5?"], after=["9.2"])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Factorisation", "marks": 3,
     "lead": "Factorise the following expressions completely. Leave your answers in simplest form:", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Exponents and algebraic fractions", "marks": 10,
     "lead": "Simplify the following expressions completely:", "items": q12},
    {"id": "2.1", "title": "Question 2.1", "kind": "Equations and inequalities", "marks": 12, "lead": "Solve for x:", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Algebraic expressions", "marks": 4, "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Simultaneous equations", "marks": 4, "items": q23},
    {"id": "3.1", "title": "Question 3.1", "kind": "Linear patterns", "marks": 5,
     "lead": "In each diagram below, there are shaded squares and white squares.",
     "figure": P.fig("Q3", "Diagram 1: a 2 by 2 block, three shaded and one white. Diagram 2: a 2 by 4 block, six shaded and two white. "
                           "Diagram 3: a 2 by 6 block, nine shaded and three white. In each, the whole bottom row is shaded and the top "
                           "row alternates shaded and white."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Patterns", "marks": 3, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Linear patterns", "marks": 4,
     "lead": "Consider the following pattern: 8 ; 15 ; 22 ; 29 ; …", "items": q33},
    {"id": "4.1", "title": "Question 4.1", "kind": "Exchange rates", "marks": 3, "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Hire purchase", "marks": 10,
     "lead": "A television set costs R20 000. Belinda buys it on hire purchase. She traded in an old television for R3 000 and also "
             "paid a deposit of R2 000. She made monthly instalments of R900 for a period of 2 years.", "items": q42},
    {"id": "5", "title": "Question 5", "kind": "Parabola and exponential graph", "marks": 8, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Hyperbola and straight line", "marks": 13,
     "lead": "The graphs of f(x) = 4/x − 2 and g(x) = mx + c are drawn below. A(4 ; 4), B, D(0 ; −4) and E are points on g. B is the "
             "x-intercept of both f and g. B and E are the points of intersection of f and g. AC is parallel to the y-axis, with C a "
             "point on f.",
     "figure": P.fig("Q6", "The hyperbola f, one branch top right through B on the x-axis and C below it, the other bottom left through "
                           "E, with a dashed horizontal asymptote below the x-axis. The straight line g rises through E, D(0 ; −4) on "
                           "the y-axis, B and A(4 ; 4). A dotted vertical line joins A down to C."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Exponential graph", "marks": 6,
     "lead": "Given the equation of an exponential graph: h(x) = a · bˣ + q. The information of the function is known:\n"
             "• 0 < a < 2 ; a ∈ ℤ\n• The range of h is y > −2\n• A(1 ; 0) is a point on the graph.", "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Probability", "marks": 8,
     "lead": "Consider events A and B. P(A) = 0,43, P(B) = 0,37 and P(A and B) = 0,1591.", "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Probability", "marks": 7,
     "lead": "Two different events, A and B, form part of an investigation.\n• P(A) = 2/3\n• P(B′) = 3/5\n• P(A or B) = 4/7\n\n"
             "Determine the value of:", "items": q9}]

P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2024", "total_marks": 100, "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "5.1", "kind": "no_fit", "detail": "The sketch of f and g is BUILT on a grid: the learner places f's x-intercepts and "
                                                   "turning point, g's y-intercept and asymptote, and picks g's shape (one point and the "
                                                   "asymptote leave it open). The Venn diagram (8.3) plays as pick the drawing: the "
                                                   "memo's and three mistakes. 3.3.2 (describe the pattern) plays as statements."},
          {"n": "9.3", "kind": "low_confidence", "detail": "The paper's values cannot belong to real events: P(A or B) = 4/7 is less than "
                                                           "P(A) = 2/3, and the memo's P(A and B) = 52/105 is more than P(B) = 2/5. The "
                                                           "right option is the memo's formula and arithmetic, as printed."}],
         {"1": 13, "2": 20, "3": 12, "4": 13, "5": 8, "6": 13, "7": 6, "8": 8, "9": 7}, 100,
         {"3.1.2": ["3.1.1"], "3.1.3": ["3.1.1"], "4.2.2": ["4.2.1"], "6.3": ["6.1"], "6.4": ["6.3"], "7.2": ["7.1"], "7.3": ["7.2"],
          "9.3": ["9.2"]},
         "Questions 1 to 9 (the whole paper)")
