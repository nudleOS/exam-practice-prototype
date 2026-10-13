"""Grade 10 Mathematics P2 November 2025 (KwaZulu-Natal Department of Education; the pages are headed 'DBE/November 2025'), the whole
paper (Questions 1 to 9, 100 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`.
Stems, marks, answers and the memo's working are the paper's and the memo's own; clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): re-published by Stanmore Secondary (stanmorephysics.com) as one scanned PDF: the question paper (pages 1-11,
with the information sheet), the department's ADDENDUM of 4 November 2025 (page 12) and the FINAL marking guideline (pages 13-22), no
text layer: read from its page images (100 dpi). Split into '<id> QP.pdf' (pages 1-12) and '<id> MG.pdf' (scratch prov/split.py).

  python tools/ingest/transcribe_g10_math_p2_2025_11_kzn.py
  python tools/ingest/ingest.py "uploads/provincial/g10-math-p2-2025-11-kzn/g10-math-p2-2025-11-kzn QP.pdf" "uploads/provincial/g10-math-p2-2025-11-kzn/g10-math-p2-2025-11-kzn MG.pdf" --id g10-math-p2-2025-11-kzn --from-json

The addendum removes 7.2 as printed (the midpoint theorem, MN = ½BC) and replaces it with 'Given quadrilateral ABCD with AD = BC and
AD ∥ BC. Prove that ABCD is a parallelogram' (5): 7.2 plays the replacement, its figure cropped from the addendum page, and the memo's
7.2 answers it. The memo's shapes map by the Grade 12 rulings (provincial.py); a geometry statement carries its [reason] at the line's
end. The sketch 6.1 is built on a grid (f = 2 sin x and g = cos x + 1 on one set of axes, as transcribe_g10_math_p2_2017_11.py 5.1).
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-math-p2-2025-11-kzn", 595.32, 842.04, {
    "Q3": [4, 70, 120, 510, 462], "Q5.1": [6, 92, 120, 520, 448], "Q5.2": [7, 92, 113, 515, 298], "Q7.1": [8, 62, 165, 518, 366],
    "Q7.2": [12, 268, 511, 470, 574], "Q7.3": [9, 108, 116, 472, 288], "Q8": [10, 172, 125, 422, 358]}, start=3)
work, answer, num, draw = P.work, P.answer, P.num, P.draw

SCHOOLS = {"head": ["PROVINCE", "NUMBER OF PUBLIC SCHOOLS"],
           "rows": [["Eastern Cape", "5 468"], ["Free State", "1 214"], ["Gauteng", "x"], ["KwaZulu-Natal", "5 895"], ["Limpopo", "3 867"],
                    ["Mpumalanga", "1 725"], ["Northern Cape", "544"], ["North West", "1 472"], ["Western Cape", "1 450"],
                    ["Total", "23 718"]]}
MARKS = {"head": ["MARKS (in %)", "FREQUENCY"],
         "rows": [["20 ≤ x < 30", "6"], ["30 ≤ x < 40", "11"], ["40 ≤ x < 50", "9"], ["50 ≤ x < 60", "7"], ["60 ≤ x < 70", "8"],
                  ["70 ≤ x < 80", "13"], ["80 ≤ x < 90", "6"]]}

# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
SORTED = "544 ; 1 214 ; 1 450 ; 1 472 ; 1 725 ; 2 083 ; 3 867 ; 5 468 ; 5 895\n"
q1 = [
    num("1.1", "Determine the value of x.", 2083, 0, "", ["The nine provinces add up to the total.", "23 718 minus the other eight."]),
    work("1.2", "Calculate the mean number of schools in South Africa.", 2, [
        "Mean = {23 718}/{9}\n= 2 635,33",      # the memo
        "Mean = {23 718}/{10}\n= 2 371,8",      # ÷ the table's rows with the total
        "Mean = {23 718 − 2 083}/{8}\n= 2 704,38",   # Gauteng left out
        "Mean = {9}/{23 718}\n= 0,0004"],       # upside down
        ["How many provinces are there?", "Mean = total ÷ number of values."], after=["1.1"]),
    answer("1.3", "Write down the median province.", 1, ["Mpumalanga", "Limpopo", "Gauteng", "North West"],
           ["Arrange the nine numbers in order.", "The median is the 5th value."], after=["1.1"]),
    work("1.4", "Determine the interquartile range.", 3, [
        SORTED + "Q₁ = {1 214 + 1 450}/{2} = 1 332 and Q₃ = {3 867 + 5 468}/{2} = 4 667,5\nIQR = 4 667,5 − 1 332\n= 3 335,5",   # the memo
        SORTED + "Q₁ = 1 450 and Q₃ = 3 867\nIQR = 3 867 − 1 450\n= 2 417",                                                   # the 3rd and 7th values
        SORTED + "Q₁ = {1 214 + 1 450}/{2} = 1 332 and Q₃ = {3 867 + 5 468}/{2} = 4 667,5\nIQR = 4 667,5 + 1 332\n= 5 999,5", # added
        SORTED + "Q₁ = 544 and Q₃ = 5 895\nIQR = 5 895 − 544\n= 5 351"],                                                      # the range
        ["Split the ordered list into a lower and an upper half (leave out the median).", "IQR = Q₃ − Q₁."], after=["1.1"]),
    work("1.5", "Due to the population increase in South Africa, 0,68% more schools will be required in the next 15 years. Determine the "
         "number of schools needed in the next 15 years.", 2, [
        "Number of schools = 23 718 × 0,68%\n= 161,28 ≈ 162 schools",      # the memo
        "Number of schools = 23 718 × 0,68\n= 16 128,24 ≈ 16 128 schools", # 0,68% as 0,68
        "Number of schools = 23 718 ÷ 0,68%\n= 3 487 941 schools",         # divided
        "Number of schools = 23 718 × 0,68%\n= 161,28 ≈ 161 schools"],     # rounded down: a school cannot be part-built
        ["Find 0,68% of 23 718.", "Can you build part of a school?"])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 2-3 ----
MID = "x̄ = {25(6) + 35(11) + 45(9) + 55(7) + 65(8) + 75(13) + 85(6)}/{60}\n"
q2 = [
    num("2.1", "How many learners wrote the test?", 60, 0, "", ["Add up the frequencies.", "6 + 11 + 9 + …"]),
    work("2.2", "Calculate the estimated mean.", 4, [
        MID + "= {3 330}/{60}\nx̄ = 55,50",                                                              # the memo
        "x̄ = {20(6) + 30(11) + 40(9) + 50(7) + 60(8) + 70(13) + 80(6)}/{60}\n= {3 030}/{60}\nx̄ = 50,50",   # the lower limits
        MID + "= {3 330}/{7}\nx̄ = 475,71",                                                              # ÷ the classes
        "x̄ = {30(6) + 40(11) + 50(9) + 60(7) + 70(8) + 80(13) + 90(6)}/{60}\n= {3 630}/{60}\nx̄ = 60,50"],  # the upper limits
        ["Use each class's midpoint.", "Divide by the number of learners."], after=["2.1"]),
    work("2.3", "Calculate the percentage of learners who obtained less than SIXTY PERCENT.", 2, [
        "{6 + 11 + 9 + 7}/{60} × 100\n= {33}/{60} × 100 = 55%",          # the memo
        "{6 + 11 + 9 + 7 + 8}/{60} × 100\n= {41}/{60} × 100 = 68,33%",   # 60-70 included
        "{6 + 11 + 9}/{60} × 100\n= {26}/{60} × 100 = 43,33%",           # 50-60 left out
        "{6 + 11 + 9 + 7}/{60}\n= {33}/{60} = 0,55%"],                   # not × 100
        ["Which classes are below 60%?", "Then the percentage of 60."], after=["2.1"])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 3-4 ----
q3 = [
    work("3.1.1", "Determine the gradient of SF.", 2, [
        "m_SF = {0 − (−1)}/{3 − 0}\n= {1}/{3}",     # the memo
        "m_SF = {3 − 0}/{0 − (−1)}\n= 3",           # x over y
        "m_SF = {0 − 1}/{3 − 0}\n= −{1}/{3}",       # −(−1) as −1
        "m_SF = {0 − (−1)}/{0 − 3}\n= −{1}/{3}"],   # the x-values the wrong way round
        ["m = (y₂ − y₁)/(x₂ − x₁).", "S(0 ; −1) and F(3 ; 0)."]),
    work("3.1.2", "Determine the equation of QH.", 3, [
        "m_QH = m_SF = {1}/{3}\n4 = {1}/{3}(4) + c\nc = {8}/{3}\ny = {1}/{3}x + {8}/{3}",      # the memo
        "m_QH = −3\n4 = −3(4) + c\nc = 16\ny = −3x + 16",                                     # the perpendicular gradient
        "m_QH = m_SF = {1}/{3}\n4 = {1}/{3}(4) + c\nc = {16}/{3}\ny = {1}/{3}x + {16}/{3}",    # 4/3 added
        "m_QH = m_SF = {1}/{3}\n4 = {1}/{3} + c\nc = {11}/{3}\ny = {1}/{3}x + {11}/{3}"],      # x not substituted
        ["QH ∥ SF: what is its gradient?", "Substitute H(4 ; 4)."], after=["3.1.1"]),
    work("3.1.3", "Calculate the value of k.", 2, [
        "2 = {1}/{3}k + {8}/{3}\n{1}/{3}k = −{2}/{3}\nk = −2",       # the memo
        "2 = {1}/{3}k + {8}/{3}\n{1}/{3}k = {2}/{3}\nk = 2",         # the sign
        "2 = {1}/{3}k + {8}/{3}\n{1}/{3}k = −{2}/{3}\nk = −{2}/{9}", # multiplied by 1/3, not divided
        "k = {1}/{3}(2) + {8}/{3}\nk = {10}/{3}\nk = 3,33"],         # 2 put in for x
        ["Q(k ; 2) lies on QH.", "Put y = 2 into the equation of QH."], after=["3.1.2"]),
    work("3.1.4", "Determine the length of HF.", 2, [
        "HF = √((4 − 3)² + (4 − 0)²)\n= √17 = 4,12",      # the memo
        "HF = √((4 − 3)² + (4 − 0)²)\n= √5 = 2,24",       # 4² as 4
        "HF = (4 − 3)² + (4 − 0)²\n= 17",                 # no square root
        "HF = √((4 + 3)² + (4 + 0)²)\n= √65 = 8,06"],     # the coordinates added
        ["Use the distance formula.", "H(4 ; 4) and F(3 ; 0)."]),
    work("3.1.5", "Calculate the coordinates of M, the midpoint of HS.", 3, [
        "M({4 + 0}/{2} ; {4 − 1}/{2})\nM(2 ; {3}/{2})",     # the memo
        "M({4 − 0}/{2} ; {4 + 1}/{2})\nM(2 ; {5}/{2})",     # subtracted
        "M(4 + 0 ; 4 − 1)\nM(4 ; 3)",                       # not halved
        "M({4 + 3}/{2} ; {4 + 0}/{2})\nM({7}/{2} ; 2)"],    # H and F, not H and S
        ["Which two points are the ends of HS?", "Average the x-values and the y-values."]),
    work("3.2", "Line segment AB is perpendicular to the segment CD. A(−5 ; 2) and B(p ; −1) are points on AB. If the gradient of segment CD "
         "is 2, calculate the value of p.", 3, [
        "m_AB = −{1}/{2}\n{−1 − 2}/{p + 5} = −{1}/{2}\n−6 = −p − 5\np = 1",      # the memo
        "m_AB = 2\n{−1 − 2}/{p + 5} = 2\n−3 = 2p + 10\np = −{13}/{2}",            # parallel, not perpendicular
        "m_AB = −{1}/{2}\n{−1 − 2}/{p − 5} = −{1}/{2}\n−6 = −p + 5\np = 11",      # −(−5) as −5
        "m_AB = {1}/{2}\n{−1 − 2}/{p + 5} = {1}/{2}\n−6 = p + 5\np = −11"],     # the sign of the negative reciprocal
        ["Perpendicular gradients multiply to −1.", "Set the gradient of AB from A and B equal to −1/2."])]

# ---- QUESTION 4, the question paper page 5 and the memo pages 4-5 ----
q4 = [
    work("4.1.1", "sin x/2", 2, ["= {sin 67,7°}/{2}\n= 0,46", "= sin({67,7°}/{2})\n= 0,56", "= {sin 67,7°}/{2}\n= 0,93",
                                 "= {cos 67,7°}/{2}\n= 0,19"],
         ["Find sin 67,7° first.", "Then halve it."]),
    work("4.1.2", "cos(3y)", 2, ["= cos(3 × 52,3°)\n= −0,92", "= 3 cos 52,3°\n= 1,83", "= cos(3 + 52,3°)\n= 0,57",
                                "= cos(3 × 52,3°)\n= 0,92"],
         ["Multiply the angle first.", "cos 156,9° is negative."]),
    work("4.1.3", "cosec((x − y)/2)", 2, [
        "= cosec({67,7° − 52,3°}/{2})\n= {1}/{sin 7,7°}\n= 7,46",     # the memo
        "= cosec({67,7° − 52,3°}/{2})\n= {1}/{cos 7,7°}\n= 1,01",     # cosec as 1/cos
        "= cosec({67,7° + 52,3°}/{2})\n= {1}/{sin 60°}\n= 1,15",      # added
        "= cosec({67,7° − 52,3°}/{2})\n= sin 7,7°\n= 0,13"],           # no reciprocal
        ["cosec θ = 1/sin θ.", "Work out the angle first."]),
    work("4.2.1", "3 + cos 4θ = 3,706", 3, [
        "cos 4θ = 0,706\n4θ = 45,09°\nθ = 11,3°",       # the memo
        "cos 4θ = 0,706\n4θ = 45,09°\nθ = 180,4°",      # multiplied by 4
        "cos 4θ = 6,706\nNo solution\nθ has no value",  # 3 added
        "cos θ = {0,706}/{4}\nθ = 79,8°\nθ = 79,8°"],   # 4 divided into cos
        ["Get cos 4θ on its own.", "Then divide the angle by 4."]),
    work("4.2.2", "4 tan θ = 7 − 4 tan θ", 3, [
        "8 tan θ = 7\ntan θ = {7}/{8}\nθ = 41,2°",       # the memo
        "0 = 7\nNo solution\nθ has no value",           # 4 tan θ subtracted from both sides wrongly
        "8 tan θ = 7\ntan θ = {8}/{7}\nθ = 48,8°",      # upside down
        "4 tan θ = 3 tan θ\ntan θ = 0\nθ = 0°"],        # 7 − 4 tan θ as 3 tan θ
        ["Collect the tan θ terms on one side.", "Then divide by 8."]),
    answer("4.3.1", "In which quadrant does the terminal arm of the angle θ lie if sin θ < 0 and cos θ < 0?", 1,
           ["Third quadrant", "Second quadrant", "Fourth quadrant", "First quadrant"], ["Both negative.", "CAST: only tan is positive."]),
    answer("4.3.2", "In which quadrant does the terminal arm of the angle θ lie if tan θ < 0 and cos θ > 0?", 1,
           ["Fourth quadrant", "Second quadrant", "Third quadrant", "First quadrant"], ["cos positive, tan negative.", "CAST: only cos is positive."])]

# ---- QUESTION 5, the question paper pages 6-7 and the memo pages 5-6 ----
q51 = [
    work("5.1.1", "Calculate the length of OP.", 2, [
        "OP² = (−12)² + 5²\nOP = 13 units",       # the memo
        "OP² = (−12)² − 5²\nOP = √119 units",     # subtracted
        "OP = −12 + 5\nOP = −7 units",            # added, not by Pythagoras
        "OP² = (−12)² + 5²\nOP = 169 units"],     # no square root
        ["Use the theorem of Pythagoras.", "x² + y² = r²."]),
    answer("5.1.2(a)", "Hence, WITHOUT the use of a calculator, determine the value of tan θ.", 1,
           ["−{5}/{12}", "{5}/{12}", "−{12}/{5}", "{5}/{13}"], ["tan θ = y/x.", "x is negative here."], after=["5.1.1"]),
    work("5.1.2(b)", "Hence, WITHOUT the use of a calculator, determine the value of (sin θ + cos θ)².", 3, [
        "= ({5}/{13} + ({−12}/{13}))²\n= (−{7}/{13})²\n= {49}/{169}",       # the memo
        "= ({5}/{13} + {12}/{13})²\n= ({17}/{13})²\n= {289}/{169}",          # the sign of cos θ
        "= ({5}/{13})² + ({−12}/{13})²\n= {25}/{169} + {144}/{169}\n= 1",    # the square of a sum as a sum of squares
        "= ({12}/{13} + ({−5}/{13}))²\n= ({7}/{13})²\n= {49}/{169} (sin and cos swapped)"],   # sin and cos swapped
        ["sin θ = y/r and cos θ = x/r.", "Add first, then square."], after=["5.1.1"])]
q52 = [
    work("5.2.1", "Determine the length of WS.", 3, [
        "Ŝ₁ = 90° [∠s on a str line]\ncos 70° = {WS}/{40}\nWS = 13,68 units",        # the memo
        "Ŝ₁ = 90° [∠s on a str line]\nsin 70° = {WS}/{40}\nWS = 37,59 units",        # sin for cos
        "Ŝ₁ = 90° [∠s on a str line]\ncos 70° = {40}/{WS}\nWS = 116,95 units",       # the ratio upside down
        "Ŝ₁ = 90° [∠s on a str line]\ntan 70° = {WS}/{40}\nWS = 109,90 units"],      # tan for cos
        ["In ΔMSW, MW is the hypotenuse.", "Which ratio of 70° uses WS and MW?"]),
    work("5.2.2", "Hence, or otherwise, determine the length of ST.", 5, [
        "cos Ŵ = {WM}/{WT}\ncos 70° = {40}/{WT}\nWT = 116,95\nST = 116,95 − 13,68\nST = 103,27 units",     # the memo
        "cos Ŵ = {WT}/{WM}\ncos 70° = {WT}/{40}\nWT = 13,68\nST = 13,68 − 13,68\nST = 0 units",           # the ratio upside down
        "cos Ŵ = {WM}/{WT}\ncos 70° = {40}/{WT}\nWT = 116,95\nST = 116,95 + 13,68\nST = 130,63 units",    # added
        "tan Ŵ = {MT}/{WM}\ntan 70° = {MT}/{40}\nMT = 109,90\nST = 109,90 − 13,68\nST = 96,22 units"],     # MT for WT
        ["In ΔWMT, WT is the hypotenuse.", "ST = WT − WS."], after=["5.2.1"])]

# ---- QUESTION 6, the question paper page 7 and the memo page 7 ----
q6 = [
    draw("6.1", "Sketch the graphs of f(x) = 2 sin x and g(x) = cos x + 1 on the same set of axes for x ∈ [0° ; 360°].", 4, [
        ["g: the shape", 1], ["g: the turning points", 1], ["f: the shape", 1], ["f: the x-intercepts", 1]],
        ["What are f(0°), f(90°) and g(0°), g(180°)?", "What does the + 1 do to cos x, and the 2 to sin x?"],
        memo="The memo's graphs: g falls from (0° ; 2) to (180° ; 0) and rises to (360° ; 2); f rises from (0° ; 0) to (90° ; 2), falls through "
             "(180° ; 0) to (270° ; −2) and rises to (360° ; 0).",
        # built on a grid (2026-10-13), as transcribe_g10_math_p2_2017_11.py 5.1: each memo criterion its features (or a shape). g's turning
        # points are one criterion (one carries its mark) and fix cos x + 1; f's x-intercepts are one criterion, and f's 'shape' carries its
        # turning point (0 marks), which fixes 2 sin x (three zeros leave the amplitude open)
        build={"kind": "sketch", "family": "sin", "b": 1, "x": [0, 360, 45], "y": [-3, 3, 0.5], "domain": [0, 360], "features": [
            {"id": "gt1", "kind": "point", "label": "turning point of g", "at": [0, 2], "tol": 0, "marks": 1, "crit": 1, "graph": "g", "turn": True},
            {"id": "gt2", "kind": "point", "label": "turning point of g", "at": [180, 0], "tol": 0, "marks": 0, "crit": 1, "graph": "g",
             "turn": True},
            {"id": "gt3", "kind": "point", "label": "turning point of g", "at": [360, 2], "tol": 0, "marks": 0, "crit": 1, "graph": "g",
             "turn": True},
            {"id": "fx1", "kind": "point", "label": "x-intercept of f", "at": [0, 0], "tol": 0, "marks": 1, "crit": 3, "graph": "f"},
            {"id": "fx2", "kind": "point", "label": "x-intercept of f", "at": [180, 0], "tol": 0, "marks": 0, "crit": 3, "graph": "f"},
            {"id": "fx3", "kind": "point", "label": "x-intercept of f", "at": [360, 0], "tol": 0, "marks": 0, "crit": 3, "graph": "f"},
            {"id": "ft", "kind": "point", "label": "turning point of f", "at": [90, 2], "alt": [[270, -2]], "tol": 0, "marks": 0, "crit": 2,
             "graph": "f", "turn": True}],
               "graphs": [{"id": "f", "family": "sin", "label": "f", "b": 1, "domain": [0, 360],
                           "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 2}},
                          {"id": "g", "family": "cos", "label": "g", "b": 1, "domain": [0, 360],
                           "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 0}}]}),
    answer("6.2", "Write down the period of f.", 1, ["360°", "180°", "90°", "720°"], ["After how many degrees does 2 sin x repeat?",
                                                                                     "The 2 changes the height, not the period."]),
    answer("6.3", "Determine the range of g.", 2, ["y ∈ [0 ; 2]", "y ∈ [−1 ; 1]", "y ∈ [1 ; 2]", "y ∈ [−2 ; 2]"],
           ["cos x lies between −1 and 1.", "Add 1 to both."]),
    answer("6.4", "For which value of x will (g(x) − f(x))/3 = 1?", 2, ["x = 270°", "x = 90°", "x = 180°", "x = 0°"],
           ["g(x) − f(x) = 3.", "Where is g 3 more than f on your graph?"], after=["6.1"])]

# ---- QUESTION 7, the question paper pages 8-9, the addendum (page 12) and the memo pages 8-9 ----
CONG = "AC is common [common]\nĈ₁ = Â₂ [alt ∠s, AD ∥ BC]\nBC = AD [given]\n"
q71 = [
    work("7.1.1", "Determine the values of w and x.", 4, [
        "2w + 10° = 70° [corr ∠s, AB ∥ EG]\nw = 30°\n5x + 45° + 70° = 180° [sum of ∠s in Δ]\nx = 13°",      # the memo
        "2w + 10° = 70° [alt ∠s, AB ∥ EG]\nw = 30°\n5x + 45° + 70° = 180° [sum of ∠s in Δ]\nx = 13°",       # alternate, not corresponding
        "2w + 10° = 110° [co-int ∠s, AB ∥ EG]\nw = 50°\n5x + 45° + 110° = 180° [sum of ∠s in Δ]\nx = 5°",  # co-interior
        "2w + 10° = 70° [corr ∠s, AB ∥ EG]\nw = 40°\n5x + 45° + 70° = 180° [sum of ∠s in Δ]\nx = 13°"],    # 10 added, not subtracted
        ["Ê and Â lie on the same side of AE, with EG ∥ AB.", "Then use the angles of ΔEDF."]),
    work("7.1.2", "Calculate the values of y and z.", 4, [
        "y + 70° + 45° = 180° [sum of ∠s in Δ]\ny = 65°\nz = 70° [opp ∠s of parm]",       # the memo
        "y + 70° + 45° = 180° [sum of ∠s in Δ]\ny = 65°\nz = 110° [co-int ∠s, AD ∥ BC]",  # the co-interior angle
        "y + 70° = 180° [co-int ∠s, AD ∥ BC]\ny = 110°\nz = 70° [opp ∠s of parm]",        # the wrong angle at B
        "y + 70° + 45° = 180° [sum of ∠s in Δ]\ny = 65°\nz = 45° [alt ∠s, AB ∥ DC]"],     # the wrong angle at C
        ["Use ΔABD.", "Ĉ is opposite Â in the parallelogram."], after=["7.1.1"]),
    work("7.2", "Given quadrilateral ABCD as shown, with AD = BC and AD ∥ BC. Prove that ABCD is a parallelogram.", 5, [
        CONG + "ΔABC ≡ ΔCDA [SAS]\nÂ₁ = Ĉ₂ [congruent Δs]\nAB ∥ DC [alt ∠s =]\nABCD is a parm [both pairs of opp sides ∥]",       # the memo
        CONG + "ΔABC ≡ ΔCDA [SSS]\nÂ₁ = Ĉ₂ [congruent Δs]\nAB ∥ DC [alt ∠s =]\nABCD is a parm [both pairs of opp sides ∥]",       # the wrong case
        "AC is common [common]\nĈ₁ = Â₂ [corr ∠s, AD ∥ BC]\nBC = AD [given]\nΔABC ≡ ΔCDA [SAS]\nÂ₁ = Ĉ₂ [congruent Δs]\n"
        "AB ∥ DC [alt ∠s =]\nABCD is a parm [both pairs of opp sides ∥]",                                                          # corresponding
        CONG + "ΔABC ≡ ΔCDA [SAS]\nÂ₁ = Ĉ₂ [congruent Δs]\nAB ∥ DC [alt ∠s =]\nABCD is a parm [both pairs of opp ∠s =]"],        # the wrong last reason
        ["Which two triangles does the diagonal AC make?", "Once AB ∥ DC as well, what does ABCD have?"])]
q72 = [q71.pop()]   # the addendum's 7.2: its own mission, with its own figure
q73 = [
    work("7.3.1", "Prove that MX = 15/2 cm.", 3, [
        "MC = KC = 15 [line through midpt ∥ 2nd side]\nMX = CX [line through midpt ∥ 2nd side]\nMC = MX + CX = 2MX\n2MX = 15, so MX = {15}/{2}",    # the memo
        "MC = KC = 15 [midpt theorem]\nMX = CX [line through midpt ∥ 2nd side]\nMC = MX + CX = 2MX\n2MX = 15, so MX = {15}/{2}",                    # the wrong reason
        "MC = 2KC = 30 [line through midpt ∥ 2nd side]\nMX = CX [line through midpt ∥ 2nd side]\nMC = MX + CX = 2MX\n2MX = 30, so MX = 15",         # MC doubled
        "MC = KC = 15 [line through midpt ∥ 2nd side]\nMX = CX [opp sides of parm]\nMC = MX + CX = 2MX\n2MX = 15, so MX = {15}/{2}"],               # the wrong reason for MX
        ["P is the midpoint of MR and PC ∥ RK: what does that make C?", "Then X on MC, with PX ∥ RC."]),
    work("7.3.2", "Calculate KR if KR = (16/5)MX.", 2, [
        "KR = {16}/{5} × {15}/{2}\nKR = 24 cm",      # the memo
        "KR = {16}/{5} + {15}/{2}\nKR = 10,7 cm",    # added
        "KR = {16}/{5} × 15\nKR = 48 cm",            # MX as 15
        "KR = {16}/{5} ÷ {15}/{2}\nKR = 0,43 cm"],   # divided
        ["MX = 15/2 cm.", "Multiply by 16/5."], after=["7.3.1"]),
    work("7.3.3", "Hence, prove that MR̂K = 90°.", 2, [
        "MK² = 30² = 900\nMR² + KR² = 18² + 24² = 900\nMR̂K = 90° [converse Pythagoras]",      # the memo
        "MK² = 15² = 225\nMR² + KR² = 9² + 24² = 657\nMR̂K ≠ 90° [converse Pythagoras]",       # half-lengths
        "MK² = 30² = 900\nMR² + KR² = 18² + 24² = 900\nMR̂K = 90° [Pythagoras]",               # the theorem, not its converse
        "MK = 30\nMR + KR = 18 + 24 = 42\nMR̂K ≠ 90° [converse Pythagoras]"],                  # not squared
        ["MK = MC + CK and MR = MP + PR.", "Do the sides satisfy Pythagoras?"], after=["7.3.2"])]

# ---- QUESTION 8, the question paper page 10 and the memo pages 9-10 ----
q8 = [
    answer("8.1", "Determine the size of AB̂O.", 1, ["30°", "60°", "120°", "90°"], ["OB bisects AB̂C.", "Half of 60°."]),
    work("8.2", "Calculate the size of Ô₁.", 3, [
        "Â = AB̂O = 30° [∠s opp equal sides]\nÔ₁ = AB̂O + Â [ext ∠ of Δ]\nÔ₁ = 60°",           # the memo
        "Â = AB̂O = 30° [∠s opp equal sides]\nÔ₁ = 180° − 30° [∠s on a str line]\nÔ₁ = 150°",   # one angle only
        "Â = 60° [∠s opp equal sides]\nÔ₁ = AB̂O + Â [ext ∠ of Δ]\nÔ₁ = 90°",                  # Â as the whole 60°
        "Â = AB̂O = 30° [∠s opp equal sides]\nÔ₁ = 2 × 60° [∠ at centre = 2 × ∠ at circumf]\nÔ₁ = 120°"],   # the centre theorem misapplied
        ["OA = OB (radii): which angles are equal?", "Ô₁ is an exterior angle of ΔAOB."], after=["8.1"]),
    work("8.3", "Hence, prove that ΔOAB ≡ ΔOCB.", 3, [
        "BO is common [common]\nAB̂O = CB̂O = 30° [OB bisects AB̂C]\nÂ = Ĉ = 30° [∠s opp equal sides]\nΔABO ≡ ΔCBO [SAA]",     # the memo
        "BO is common [common]\nAB̂O = CB̂O = 30° [OB bisects AB̂C]\nÂ = Ĉ = 30° [∠s opp equal sides]\nΔABO ≡ ΔCBO [SAS]",     # the wrong case
        "BO is common [common]\nAB̂O = CB̂O = 30° [OB bisects AB̂C]\nÂ = Ĉ = 30° [∠s opp equal sides]\nΔABO ||| ΔCBO [∠, ∠, ∠]",  # similar, not congruent
        "BO is common [common]\nAB̂O = CB̂O = 30° [given]\nÂ = Ĉ = 60° [∠s opp equal sides]\nΔABO ≡ ΔCBO [SAA]"],               # the wrong angles
        ["Which side do the two triangles share?", "Which angles are equal and why?"], after=["8.2"])]

# ---- QUESTION 9, the question paper page 10 and the memo page 10 ----
q9 = [
    work("9.1", "Calculate the volume of the globe, correct to ONE decimal place.", 2, [
        "V = {4}/{3}π(21)³\nV = 38 792,4 cm³",     # the memo
        "V = {4}/{3}π(21)²\nV = 1 847,3 cm³",      # r squared
        "V = 4π(21)³\nV = 116 377,2 cm³",          # no 1/3
        "V = {4}/{3}π(42)³\nV = 310 339,1 cm³"],   # the diameter for the radius
        ["V = (4/3)πr³.", "r = 21 cm."]),
    work("9.2", "Determine the area of the globe, correct to ONE decimal place.", 2, [
        "A = 4π(21)²\nA = 5 541,8 cm²",      # the memo
        "A = π(21)²\nA = 1 385,4 cm²",       # one circle only
        "A = 4π(21)³\nA = 116 377,2 cm²",    # r cubed
        "A = 2π(21)²\nA = 2 770,9 cm²"],     # 2 for 4
        ["A = 4πr².", "r = 21 cm."]),
    answer("9.3", "If the radius is doubled, what would be the ratio of the volume of the original sphere to the volume of the new sphere?", 1,
           ["1 : 8", "1 : 2", "1 : 4", "8 : 1"], ["The volume depends on r³.", "2³ = ?"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Statistics", "marks": 9, "table": SCHOOLS,
     "lead": "The table below shows the number of public schools in the NINE provinces of South Africa.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Statistics: grouped data", "marks": 7, "table": MARKS,
     "lead": "The following table represents the Grade 10 mathematics test results at Excel Secondary School.", "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Analytical geometry", "marks": 15,
     "lead": "3.1: In the diagram below, trapezium QHFS is drawn, such that QH ∥ SF.",
     "figure": P.fig("Q3", "Trapezium QHFS on the axes: Q(k ; 2) on the left, H(4 ; 4) top right, F(3 ; 0) on the x-axis and S(0 ; −1) on "
                           "the y-axis."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Trigonometry", "marks": 14,
     "lead": "4.1: If x = 67,7° and y = 52,3°, calculate the following correct to TWO decimal places. 4.2: Solve for θ (correct to ONE decimal "
             "place).", "items": q4},
    {"id": "5.1", "title": "Question 5.1", "kind": "Trigonometry", "marks": 6,
     "lead": "In the diagram below, P(−12 ; 5) is a point in the Cartesian plane such that XÔP = θ.",
     "figure": P.fig("Q5.1", "The point P(−12 ; 5) in the second quadrant, joined to the origin O; θ is the angle from the positive x-axis to "
                             "OP."), "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Trigonometry: right triangles", "marks": 8,
     "lead": "In the diagram below, WM̂T = 90°, MS ⊥ WT, Ŵ = 70° and MW = 40 units.",
     "figure": P.fig("Q5.2", "Triangle WMT with the right angle at M and MS perpendicular to WT; MW = 40 units and the angle at W is 70°."),
     "items": q52},
    {"id": "6", "title": "Question 6", "kind": "Trigonometric graphs", "marks": 9,
     "lead": "Given: g(x) = cos x + 1 and f(x) = 2 sin x for x ∈ [0° ; 360°].", "items": q6},
    {"id": "7.1", "title": "Question 7.1", "kind": "Euclidean geometry", "marks": 8,
     "lead": "Give reasons for each statement. In the diagram below, ABCD is a parallelogram with AB ∥ EG ∥ DC.",
     "figure": P.fig("Q7.1", "Parallelogram ABCD with diagonal BD and EG parallel to AB and DC, meeting BD at F. Â = 70°, at E the angle "
                             "2w + 10°, at F the angle 5x, at D the angle 45°, at B the angle y and at C the angle z."), "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Euclidean geometry: proof", "marks": 5,
     "lead": "Give reasons for each statement. (The department's addendum of 4 November 2025 replaced the printed 7.2 with this question.)",
     "figure": P.fig("Q7.2", "Quadrilateral ABCD with AD ∥ BC and AD = BC, and diagonal AC; angles Â₁, Â₂ at A and Ĉ₁, Ĉ₂ at C."),
     "items": q72},
    {"id": "7.3", "title": "Question 7.3", "kind": "Euclidean geometry: midpoints", "marks": 7,
     "lead": "Give reasons for each statement. In the diagram below, KR ∥ CP, PX ∥ RC, MP = PR = 9 cm and CK = 15 cm.",
     "figure": P.fig("Q7.3", "Triangle MRK with P the midpoint of MR (MP = PR = 9 cm), C on MK with CK = 15 cm and PC ∥ RK, and X on MC "
                             "with PX ∥ RC."), "items": q73},
    {"id": "8", "title": "Question 8", "kind": "Euclidean geometry", "marks": 7,
     "lead": "Give reasons for each statement. In the diagram below, OB bisects AB̂C. O is the centre of the circle and AB̂C = 60°.",
     "figure": P.fig("Q8", "A circle with centre O; B at the top, A and C on the lower arc; BA, BC, BO, OA and OC drawn; AB̂C = 60°; Ô₁ and Ô₂ "
                           "below O."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Measurement", "marks": 5,
     "lead": "A globe of the world, spherical in shape, is placed in a geography classroom. The globe has a radius of 21 cm.", "items": q9}]

P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2025", "total_marks": 100, "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "7.2", "kind": "no_fit", "detail": "The department's addendum (4 November 2025, page 12 of the scan) removes the printed 7.2 "
                                                   "(prove MN = ½BC) and replaces it with 'ABCD has AD = BC and AD ∥ BC; prove that ABCD is a "
                                                   "parallelogram' (5). 7.2 plays the replacement; its figure is cropped from the addendum and "
                                                   "the memo answers it."},
          {"n": "6.1", "kind": "no_fit", "detail": "The sketch of f and g (6.1) is BUILT on a grid: g's turning points and f's x-intercepts are "
                                                   "placed, each graph's turning point fixing its curve."},
          {"n": "1.5", "kind": "low_confidence", "detail": "The memo gives 161,28 ≈ 162 more schools and also accepts 23 880 (the new total). "
                                                           "The right option is the memo's first, 162."}],
         {"1": 9, "2": 7, "3": 15, "4": 14, "5": 14, "6": 9, "7": 20, "8": 7, "9": 5}, 100,
         {"1.2": ["1.1"], "1.3": ["1.1"], "1.4": ["1.1"], "2.2": ["2.1"], "2.3": ["2.1"], "3.1.2": ["3.1.1"], "3.1.3": ["3.1.2"],
          "5.1.2(a)": ["5.1.1"], "5.1.2(b)": ["5.1.1"], "5.2.2": ["5.2.1"], "6.4": ["6.1"], "7.1.2": ["7.1.1"], "7.3.2": ["7.3.1"],
          "7.3.3": ["7.3.2"], "8.2": ["8.1"], "8.3": ["8.2"]},
         "Questions 1 to 9 (the whole paper, with the addendum's 7.2)")
