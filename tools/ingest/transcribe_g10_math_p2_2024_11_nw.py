"""Grade 10 Mathematics P2 November 2024 (North West Department of Education, provincial assessment), the whole paper (Questions 1
to 9, 100 marks, 2 hours: statistics, analytical geometry, trigonometry, measurement, Euclidean geometry), hand-transcribed into the
catalogue format, then run through `ingest.py --from-json`. Stems, marks, answers and the memo's working are the paper's and the
memo's own (its English); clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination >
Assessment, the question paper PDF (English, 10 pages; its diagrams are images), the marking guidelines PDF (English, 10 pages) and
the answer book PDF (English and Afrikaans, 15 pages; nothing is cropped from it), read from their page images at 100 dpi where
the text layer garbles fractions, roots and angles.

  python tools/ingest/transcribe_g10_math_p2_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-math-p2-2024-11-nw/19-NOVEMBER-2024-S2-GR10-MATHEMATICS-P2-QP-ENG.pdf" "uploads/provincial/g10-math-p2-2024-11-nw/19-NOVEMBER-2024-S2-GR10-MATHEMATICS-P2-MG-ENG.pdf" --id g10-math-p2-2024-11-nw --from-json

The memo's shapes map by the Grade 12 rulings (provincial.py); a geometry statement carries its [reason] at the line's end. The box
and whisker diagram 1.1 is built on a number line. The memo prints no answer for 9.1 (its page 9 ends with Question 9's diagram);
9.2's working, 18 = 4x + 8, is the midpoint theorem's PQ = 2SR, so 9.1 plays as that (flag below).
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-math-p2-2024-11-nw", 595.32, 841.92, {
    "Q2": [3, 45, 365, 500, 588],     # the histogram SCORES IN INTRODUCTORY STATISTICS
    "Q3": [4, 84, 140, 498, 418],     # ΔABC on the axes
    "Q4": [5, 163, 137, 426, 397],    # right-angled ΔABC with sides a, b, c
    "Q5": [6, 82, 153, 509, 417],     # f and g on [−180° ; 180°]
    "Q6": [7, 70, 168, 521, 489],     # the cliff CD and ships A and B
    "Q7": [8, 212, 135, 498, 266],    # the rectangular prism 8 m × 3 m × 5 m
    "Q8": [9, 120, 168, 405, 442],    # parallelogram ABCD with diagonal AC, BE ∥ FD
    "Q9": [10, 128, 152, 409, 348]}, start=6)   # ΔPQT with S and R the midpoints
work, answer, num, draw = P.work, P.answer, P.num, P.draw

# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
q1 = [
    draw("1.1", "Draw a box and whisker diagram to represent the data.", 3, [
        ["The whiskers: out to the minimum 12 and the maximum 68", 1], ["The box: Q₁ = 21, the median 32 and Q₃ = 50", 2]],
        ["Which five numbers does a box and whisker diagram need?", "With 13 values, which value is the median, and what are the middles "
                                                                    "of the lower and upper six?"],
        memo="The memo's diagram on a number line: whiskers from 12 to 21 and from 50 to 68, the box from 21 to 50 with the median at "
             "32. Five-number summary: 12 ; 21 ; 32 ; 50 ; 68.",
        # built on a number line: the five values placed, marked as the memo marks it (✓ min and max, ✓✓ the box in combination)
        build={"kind": "boxplot", "x": [10, 70, 1], "tick": 1, "label": 5, "tol": 0,
               "at": {"min": 12, "q1": 21, "med": 32, "q3": 50, "max": 68},
               "crit": {"min": 0, "max": 0, "q1": 1, "med": 1, "q3": 1}}),
    work("1.2", "Determine the interquartile range (IQR).", 2, [
        "IQR = Q₃ − Q₁\n= 50 − 21\n= 29",            # the memo
        "IQR = Q₃ + Q₁\n= 50 + 21\n= 71",            # the quartiles added
        "IQR = Q₃ − Q₁\n= 54 − 20\n= 34",            # the values next to the quartiles
        "IQR = max − min\n= 68 − 12\n= 56"],         # the range, not the interquartile range
        ["What are Q₁ and Q₃?", "The interquartile range is Q₃ minus Q₁."]),
    work("1.3", "Calculate the range of the data.", 2, [
        "Range = max − min\n= 68 − 12\n= 56",        # the memo
        "Range = max + min\n= 68 + 12\n= 80",        # added, not subtracted
        "Range = Q₃ − Q₁\n= 50 − 21\n= 29",          # the interquartile range
        "Range = max − min\n= 68 − 16\n= 52"],       # the second value taken as the minimum
        ["What are the smallest and the largest values?", "The range is the largest minus the smallest."]),
    answer("1.4", "Comment on the skewness of the data.", 1,
           ["The data is skewed to the right (positively skewed)", "The data is skewed to the left (negatively skewed)",
            "The data is symmetrical", "The data has no skewness because there are no outliers"],
           ["Is the median closer to Q₁ or to Q₃?", "Which whisker is longer?"], after=["1.1"])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 2-3 ----
q2 = [
    num("2.1", "How many learners wrote the examination?", 200, 0, "", ["Add up the heights of all the bars.", "12 + 18 + 55 + …"]),
    answer("2.2", "Identify the modal class of the data.", 1, ["60 < m ≤ 70", "50 < m ≤ 60", "57", "70 < m ≤ 80"],
           ["Which bar is the tallest?", "The modal class is an interval, not a frequency."]),
    work("2.3", "Estimate the mean of this data. Show all calculations.", 4, [
        "Σf·x = 12(35) + 18(45) + 55(55) + 57(65) + 43(75) + 11(85) + 4(95) = 12 500\nx̄ = {12 500}/{200}\nx̄ = 62,5",       # the memo
        "Σf·x = 12(30) + 18(40) + 55(50) + 57(60) + 43(70) + 11(80) + 4(90) = 11 500\nx̄ = {11 500}/{200}\nx̄ = 57,5",       # the lower limits
        "Σf·x = 12(40) + 18(50) + 55(60) + 57(70) + 43(80) + 11(90) + 4(100) = 13 500\nx̄ = {13 500}/{200}\nx̄ = 67,5",      # the upper limits
        "Σf·x = 12(35) + 18(45) + 55(55) + 57(65) + 43(75) + 11(85) + 4(95) = 12 500\nx̄ = {12 500}/{7}\nx̄ = 1 785,71"],    # ÷ the classes
        ["Which value stands for every learner in a class when the data is grouped?", "What do you divide the total by?"]),
    answer("2.4", "Estimate the median mark obtained by the group.", 2, ["60 < m ≤ 70", "50 < m ≤ 60", "70 < m ≤ 80", "100,5"],
           ["The median is the ½(200) + ½ = 100,5th mark: in which class does it fall?", "Add the frequencies from the left: 12, 30, "
                                                                                       "85, …"], after=["2.1"]),
    answer("2.5", "In which interval does the upper quartile lie?", 1, ["70 < m ≤ 80", "60 < m ≤ 70", "80 < m ≤ 90", "150,75"],
           ["The upper quartile is the ¾(200) + ¾ = 150,75th mark.", "Add the frequencies from the left until you pass 150,75."],
           after=["2.1"])]

# ---- QUESTION 3, the question paper page 4 and the memo pages 3-4 ----
MAB = "m_AB = {−5 − 2}/{3 − (−11)} = −{1}/{2}\n"
ABL = "AB = √((3 − (−11))² + (−5 − 2)²) = √245 = 7√5\n"
q3 = [
    work("3.1", "Calculate the length of BC. Leave the answer in surd form.", 2, [
        "BC = √((6 − 3)² + (1 − (−5))²)\n= √(9 + 36)\n= √45 = 3√5",          # the memo
        "BC = √((6 − 3)² + (1 − 5)²)\n= √(9 + 16)\n= √25 = 5",              # −(−5) taken as −5
        "BC = √((6 + 3)² + (1 + 5)²)\n= √(81 + 36)\n= √117 = 3√13",          # the coordinates added
        "BC = (6 − 3)² + (1 − (−5))²\n= 9 + 36\n= 45"],                     # no square root
        ["Which formula gives the distance between two points?", "What is 1 − (−5)?"]),
    work("3.2", "Write down the coordinates of the midpoint D, of AB.", 4, [
        "D = ({x₁ + x₂}/{2} ; {y₁ + y₂}/{2})\n= ({−11 + 3}/{2} ; {2 + (−5)}/{2})\nD = (−4 ; −{3}/{2})",         # the memo
        "D = ({x₁ − x₂}/{2} ; {y₁ − y₂}/{2})\n= ({−11 − 3}/{2} ; {2 − (−5)}/{2})\nD = (−7 ; {7}/{2})",          # subtracted
        "D = (x₁ + x₂ ; y₁ + y₂)\n= (−11 + 3 ; 2 + (−5))\nD = (−8 ; −3)",                                        # not halved
        "D = ({x₁ + x₂}/{2} ; {y₁ + y₂}/{2})\n= ({−11 + 6}/{2} ; {2 + 1}/{2})\nD = (−{5}/{2} ; {3}/{2})"],      # A and C, not A and B
        ["Which formula gives the midpoint of two points?", "Which two points are the ends of AB?"]),
    work("3.3", "Prove that AB̂C = 90°.", 5, [
        MAB + "m_BC = {1 − (−5)}/{6 − 3} = 2\nm_AB × m_BC = −{1}/{2} × 2 = −1\nAB ⊥ BC, so AB̂C = 90°",                          # the memo
        MAB + "m_BC = {6 − 3}/{1 − (−5)} = {1}/{2}\nm_AB × m_BC = −{1}/{2} × {1}/{2} = −{1}/{4}\nAB is not ⊥ BC, so AB̂C ≠ 90°",   # x over y
        "m_AB = {−5 − 2}/{3 − 11} = {7}/{8}\nm_BC = {1 − (−5)}/{6 − 3} = 2\nm_AB × m_BC = {7}/{8} × 2 = {7}/{4}\n"
        "AB is not ⊥ BC, so AB̂C ≠ 90°",                                                                                       # −(−11) as −11
        MAB + "m_AC = {1 − 2}/{6 − (−11)} = −{1}/{17}\nm_AB × m_AC = −{1}/{2} × −{1}/{17} = {1}/{34}\nAB is not ⊥ AC, so AB̂C ≠ 90°"],  # AC, not BC
        ["Which two lines meet at B?", "What is the product of the gradients of two perpendicular lines?"]),
    work("3.4", "Calculate the area of ΔABC.", 4, [
        ABL + "Area = ½ × BC × AB\n= ½ × 3√5 × 7√5\n= 52,5 units²",                                                        # the memo
        "AC = √((6 − (−11))² + (1 − 2)²) = √290\nArea = ½ × BC × AC\n= ½ × 3√5 × √290\n= 57,12 units²",                   # BC × AC
        ABL + "Area = BC × AB\n= 3√5 × 7√5\n= 105 units²",                                                                 # no ½
        "AB = √((3 − 11)² + (−5 − 2)²) = √113\nArea = ½ × BC × AB\n= ½ × 3√5 × √113\n= 35,66 units²"],                    # −(−11) as −11
        ["Which two sides meet at the right angle at B?", "What is the area of a right-angled triangle in terms of those two sides?"],
        after=["3.1", "3.3"])]

# ---- QUESTION 4, the question paper page 5 and the memo pages 5-6 ----
C40 = "Ĉ = 40° [sum of ∠s of a Δ]\n"
q41 = [
    answer("4.1.1", "sin A", 1, ["{a}/{b}", "{c}/{b}", "{a}/{c}", "{b}/{a}"],
           ["Which side is opposite A?", "Which side is the hypotenuse, opposite the right angle?"]),
    answer("4.1.2", "cot C", 1, ["{a}/{c}", "{c}/{a}", "{a}/{b}", "{b}/{c}"],
           ["cot C is the adjacent side over the opposite side.", "Which side is next to C, and which is opposite C?"]),
    work("4.1.3", "If it is given that a = 5 and Â = 50°, calculate the numerical value of c.", 3, [
        C40 + "cot 40° = {5}/{c}\nc = {5}/{cot 40°}\nc = 4,20",                                         # the memo
        C40 + "cot 40° = {c}/{5}\nc = 5 cot 40°\nc = 5,96",                                             # the ratio upside down
        "Ĉ = 130° [sum of ∠s of a Δ]\ncot 130° = {5}/{c}\nc = {5}/{cot 130°}\nc = −5,96",               # 180° − 50°, the right angle left out
        C40 + "sin 40° = {5}/{c}\nc = {5}/{sin 40°}\nc = 7,78"],                                        # the wrong ratio
        ["What is Ĉ when Â = 50° and B̂ = 90°?", "Which ratio of Ĉ uses a and c?"])]
COS = "13 cos θ = 12, so cos θ = {12}/{13}\nx = 12, r = 13\n"
q42 = [
    work("4.2.1", "sin θ", 4, [
        COS + "y² = 13² − 12², y = 5\nsin θ = {5}/{13}",             # the memo
        COS + "y² = 13² + 12², y = √313\nsin θ = {√313}/{13}",       # the squares added
        COS + "y² = 13² − 12², y = 5\nsin θ = {5}/{12}",             # y over x
        COS + "y² = 13² − 12², y = 5\nsin θ = {13}/{5}"],            # r over y (cosec)
        ["In your sketch, which sides are x and r?", "How does Pythagoras give y?"]),
    work("4.2.2", "tan θ − cosec²θ", 3, [
        "tan θ − cosec²θ = {5}/{12} − ({13}/{5})²\n= {5}/{12} − {169}/{25}\n= −{1 903}/{300} = −6,34",    # the memo
        "tan θ − cosec²θ = {12}/{5} − ({13}/{5})²\n= {12}/{5} − {169}/{25}\n= −{109}/{25} = −4,36",       # tan as x over y
        "tan θ − cosec²θ = {5}/{12} − ({13}/{12})²\n= {5}/{12} − {169}/{144}\n= −{109}/{144} = −0,76",    # cosec as r over x
        "tan θ − cosec²θ = {5}/{12} − 2({13}/{5})\n= {5}/{12} − {26}/{5}\n= −{287}/{60} = −4,78"],        # the square read as × 2
        ["What are tan θ and cosec θ in terms of x, y and r?", "Square cosec θ before you subtract."], after=["4.2.1"])]
q43 = [
    work("4.3", "cosec 60° · cot 30° + cos 45° · cosec 45°", 5, [
        "= {2}/{√3} · √3 + {1}/{√2} · √2\n= 2 + 1\n= 3",                    # the memo
        "= {√3}/{2} · √3 + {1}/{√2} · √2\n= {3}/{2} + 1\n= {5}/{2}",        # cosec 60° taken as sin 60°
        "= {2}/{√3} · {1}/{√3} + {1}/{√2} · √2\n= {2}/{3} + 1\n= {5}/{3}",  # cot 30° taken as tan 30°
        "= {2}/{√3} · √3 + √2 · √2\n= 2 + 2\n= 4"],                         # cos 45° taken as √2
        ["What are sin 60°, tan 30° and cos 45° as exact values?", "cosec, sec and cot are the reciprocals of sin, cos and tan."])]
q44 = [
    work("4.4", "3 + sec x = 5 and 0° ≤ x ≤ 90°", 3, [
        "sec x = 2\n{1}/{cos x} = 2\ncos x = {1}/{2}\nx = 60°",                     # the memo
        "sec x = 2\n{1}/{sin x} = 2\nsin x = {1}/{2}\nx = 30°",                     # sec taken as 1/sin
        "sec x = {5}/{3}\n{1}/{cos x} = {5}/{3}\ncos x = {3}/{5}\nx = 53,13°",       # divided by 3, not subtracted
        "sec x = 8\n{1}/{cos x} = 8\ncos x = {1}/{8}\nx = 82,82°"],                 # 3 moved without its sign change
        ["What is sec x on its own?", "sec x is the reciprocal of which ratio?"])]

# ---- QUESTION 5, the question paper page 6 and the memo page 6 ----
q5 = [
    answer("5.1", "Write down the values of a and b.", 2, ["a = 1 and b = −2", "a = 2 and b = 2", "a = 1 and b = 2", "a = −1 and b = −2"],
           ["What is f(0) = cos 0° + a on the graph?", "Is g = b sin x positive or negative just right of 0°?"]),
    answer("5.2", "Write down the period of g.", 1, ["360°", "180°", "90°", "720°"],
           ["After how many degrees does g repeat itself?", "Look from one maximum of g to the next."]),
    answer("5.3", "Determine the range of f.", 2, ["y ∈ [0 ; 2]", "y ∈ [−1 ; 1]", "y ∈ [−2 ; 2]", "y ∈ [1 ; 2]"],
           ["What is the lowest value of f?", "What is the highest value of f?"], after=["5.1"]),
    answer("5.4", "Write down the amplitude of g.", 1, ["2", "−2", "4", "1"],
           ["How far does g rise above its middle line?", "Can an amplitude be negative?"], after=["5.1"]),
    num("5.5", "Determine the number of solutions to f(x) = g(x) for −180° < x < 180°.", 1, 0, "",
        ["Where do the two graphs cross?", "Are x = −180° and x = 180° inside the interval?"]),
    answer("5.6", "For which values of x is g(x) < 0?", 2, ["0° < x < 180°", "−180° < x < 0°", "0° ≤ x ≤ 180°", "90° < x < 180°"],
           ["Where is g below the x-axis?", "Is g(x) < 0 at x = 0° or x = 180°?"]),
    answer("5.7.1", "The equation of h", 2, ["h(x) = −cos x − 3", "h(x) = −cos x − 1", "h(x) = cos x − 1", "h(x) = −cos x − 2"],
           ["What does a reflection about the x-axis do to f(x) = cos x + 1?", "Then what does moving 2 units down do?"], after=["5.1"]),
    answer("5.7.2", "The range of h", 2, ["y ∈ [−4 ; −2]", "y ∈ [−2 ; 0]", "y ∈ [−3 ; −1]", "y ∈ [2 ; 4]"],
           ["What are the lowest and highest values of −cos x?", "Then subtract 3 from each."], after=["5.7.1"])]

# ---- QUESTION 6, the question paper page 7 and the memo page 7 ----
SUM = "B̂ + Ĉ + BD̂C = 180° [sum of ∠s of a Δ]\n"
q6 = [
    work("6.1", "Determine the size of BD̂C.", 2, [
        SUM + "45° + 90° + BD̂C = 180°\nBD̂C = 45°",                                                           # the memo
        SUM + "30° + 90° + BD̂C = 180°\nBD̂C = 60°",                                                           # the angle at A
        SUM + "45° + 45° + BD̂C = 180°\nBD̂C = 90°",                                                           # Ĉ taken as 45°
        "B̂ + Ĉ + BD̂C = 360° [sum of ∠s of a Δ]\n45° + 90° + BD̂C = 360°\nBD̂C = 225°"],                       # 360° for a triangle
        ["What are the angles at B and at C in ΔBCD?", "What do the angles of a triangle add up to?"]),
    work("6.2", "Calculate the length of BC.", 2, [
        "tan B̂ = {DC}/{BC}\ntan 45° = {200}/{BC}\nBC = 200 m",                  # the memo
        "tan B̂ = {BC}/{DC}\ntan 30° = {BC}/{200}\nBC = 115,47 m",               # the angle at D, 30°
        "sin B̂ = {DC}/{BC}\nsin 45° = {200}/{BC}\nBC = 282,84 m",               # BC taken as the hypotenuse
        "tan B̂ = {DC}/{BC}\ntan 45° = {200}/{BC}\nBC = {200}/{45} = 4,44 m"],  # divided by the angle, not its tan
        ["Which ratio of B̂ uses DC and BC?", "What is tan 45°?"]),
    work("6.3", "Determine the distance between Ship A and Ship B.", 4, [
        "tan Â = {CD}/{AC}\ntan 30° = {200}/{AC}\nAC = 346,41 m\nAB = AC − BC = 346,41 − 200 = 146,41 m",       # the memo
        "tan Â = {AC}/{CD}\ntan 30° = {AC}/{200}\nAC = 115,47 m\nAB = BC − AC = 200 − 115,47 = 84,53 m",        # the ratio upside down
        "tan Â = {CD}/{AC}\ntan 30° = {200}/{AC}\nAC = 346,41 m\nAB = AC + BC = 346,41 + 200 = 546,41 m",       # added, not subtracted
        "sin Â = {CD}/{AC}\nsin 30° = {200}/{AC}\nAC = 400 m\nAB = AC − BC = 400 − 200 = 200 m"],              # AC taken as the hypotenuse
        ["Which ratio of Â uses CD and AC?", "How do AC and BC give AB?"], after=["6.2"])]

# ---- QUESTION 7, the question paper page 8 and the memo pages 7-8 ----
q7 = [
    work("7.1", "Calculate the surface area of the prism.", 2, [
        "SA = 2(8 × 3) + 2(8 × 5) + 2(5 × 3)\n= 158 m²",          # the memo
        "SA = 8 × 3 + 8 × 5 + 5 × 3\n= 79 m²",                    # each face once
        "SA = 2(8 × 3 × 5)\n= 240 m²",                            # twice the volume
        "SA = 2(8 + 3) + 2(8 + 5) + 2(5 + 3)\n= 64 m²"],          # the sides added, not multiplied
        ["Which three different rectangles make up the faces?", "How many of each face are there?"]),
    work("7.2", "Calculate the volume of the prism if the height is doubled and the breadth halved.", 2, [
        "V = L × B × H = 8 × 1,5 × 10\n= 120 m³",                 # the memo
        "V = L × B × H = 8 × 1,5 × 5\n= 60 m³",                   # the height not doubled
        "V = L × B × H = 8 × 3 × 10\n= 240 m³",                   # the breadth not halved
        "V = L + B + H = 8 + 1,5 + 10\n= 19,5 m³"],               # added, not multiplied
        ["What are the new height and breadth?", "Volume = L × B × H."]),
    work("7.3", "Calculate the volume if the length is doubled, the height is halved and the breadth is tripled.", 3, [
        "V = L × B × H = 16 × 9 × 2,5\n= 360 m³",                 # the memo
        "V = L × B × H = 16 × 1 × 2,5\n= 40 m³",                  # tripled read as divided by 3
        "V = L × B × H = 16 × 9 × 10\n= 1 440 m³",                # the height doubled
        "V = L × B × H = 4 × 9 × 2,5\n= 90 m³"],                  # the length halved
        ["What are the new length, breadth and height?", "Volume = L × B × H."])]

# ---- QUESTION 8, the question paper page 9 and the memo pages 8-9 ----
AB = "AB = CD [opp sides of parm are =]\n"
C1 = "Ĉ₁ = Â₂ [alt ∠s, BC ∥ AD]\n"
q8 = [
    work("8.1.1", "Prove that: ΔABE ≡ ΔCDF", 4, [
        AB + "Â₁ = Ĉ₂ [alt ∠s, AB ∥ CD]\nÊ₁ = F̂₁ [alt ∠s, BE ∥ FD]\nΔABE ≡ ΔCDF [AAS]",      # the memo
        AB + "Â₁ = Ĉ₂ [alt ∠s, AB ∥ CD]\nÊ₁ = F̂₁ [alt ∠s, BE ∥ FD]\nΔABE ≡ ΔCDF [SAS]",      # the wrong case
        AB + "Â₁ = Ĉ₂ [corr ∠s, AB ∥ CD]\nÊ₁ = F̂₁ [corr ∠s, BE ∥ FD]\nΔABE ≡ ΔCDF [AAS]",    # corresponding, not alternate
        AB + "Â₁ = Ĉ₁ [alt ∠s, AB ∥ CD]\nÊ₁ = F̂₁ [alt ∠s, BE ∥ FD]\nΔABE ≡ ΔCDF [AAS]"],     # the wrong angle at C
        ["Which sides of a parallelogram are equal?", "Which pairs of parallel lines make alternate angles with the diagonal AC?"]),
    work("8.1.2", "Prove that: CÊB = AF̂D", 3, [
        C1 + "B̂ = D̂ [opp ∠s of a parm]\nB̂₁ = D̂₁ [proven, ΔABE ≡ ΔCDF]\nB̂₂ = D̂₂\nÊ₂ = F̂₂ [sum of ∠s of a Δ]",       # the memo
        "Ĉ₁ = Â₂ [corr ∠s, BC ∥ AD]\nB̂ = D̂ [opp ∠s of a parm]\nB̂₁ = D̂₁ [proven, ΔABE ≡ ΔCDF]\nB̂₂ = D̂₂\n"
        "Ê₂ = F̂₂ [sum of ∠s of a Δ]",                                                                                # corresponding
        C1 + "B̂ = D̂ [opp sides of a parm]\nB̂₁ = D̂₁ [proven, ΔABE ≡ ΔCDF]\nB̂₂ = D̂₂\nÊ₂ = F̂₂ [sum of ∠s of a Δ]",    # sides, not angles
        C1 + "B̂ = D̂ [opp ∠s of a parm]\nB̂₁ = D̂₁ [proven, ΔABE ≡ ΔCDF]\nB̂₂ = D̂₂\nÊ₂ = F̂₂ [vert opp ∠s]"],          # the wrong last reason
        ["Which two angles of ΔCEB and ΔAFD are equal?", "Then what must their third angles be?"], after=["8.1.1"]),
    work("8.1.3", "Prove that: AF = CE", 3, [
        "Ĉ₁ = Â₂ [proven]\nB̂₂ = D̂₂ [proven]\nBC = AD [opp sides of parm are =]\nΔCBE ≡ ΔADF [AAS]\nAF = CE [congruent Δs]",      # the memo
        "Ĉ₁ = Â₂ [proven]\nB̂₂ = D̂₂ [proven]\nBC = AD [opp sides of parm are =]\nΔCBE ≡ ΔADF [SAS]\nAF = CE [congruent Δs]",      # the wrong case
        "Ĉ₁ = Â₂ [proven]\nB̂₂ = D̂₂ [proven]\nBC = AD [opp sides of parm are =]\nΔCBE ≡ ΔADF [AAS]\nAF = CE [opp sides of parm are =]",  # the wrong last reason
        "Ĉ₁ = Â₂ [proven]\nB̂₂ = D̂₂ [proven]\nBC = AD [alt ∠s, BC ∥ AD]\nΔCBE ≡ ΔADF [AAS]\nAF = CE [congruent Δs]"],             # a side from angles
        ["Which triangles contain AF and CE?", "Which sides and angles of those triangles are already known to be equal?"],
        after=["8.1.2"])]

# ---- QUESTION 9, the question paper page 10 and the memo pages 9-10 ----
q9 = [
    work("9.1", "Determine the length of PQ in terms of x.", 2, [
        "PQ = 2SR [midpt theorem]\nPQ = 4x + 8",                  # 9.2's working (the memo prints no 9.1)
        "PQ = SR [midpt theorem]\nPQ = 2x + 4",                   # equal, not double
        "PQ = ½SR [midpt theorem]\nPQ = x + 2",                   # half, not double
        "PQ = 2SR [midpt theorem]\nPQ = 4x + 4"],                 # 2 multiplied into 2x only
        ["S and R are the midpoints of two sides of ΔPQT: how is SR related to PQ?", "What is 2(2x + 4)?"]),
    work("9.2", "If the length of PQ is 18, determine the value of x.", 3, [
        "18 = 4x + 8\n18 − 8 = 4x\nx = {10}/{4} = {5}/{2}",       # the memo
        "18 = 2x + 4\n18 − 4 = 2x\nx = {14}/{2} = 7",             # SR set equal to 18
        "18 = 4x + 8\n18 + 8 = 4x\nx = {26}/{4} = {13}/{2}",      # 8 moved without its sign change
        "18 = 4x + 4\n18 − 4 = 4x\nx = {14}/{4} = {7}/{2}"],      # PQ = 4x + 4
        ["Set your expression for PQ equal to 18.", "Solve the linear equation for x."], after=["9.1"]),
    work("9.3", "Prove that ΔTRS ||| ΔTQP", 5, [
        "SR ∥ PQ [midpt theorem]\nQ̂ = TR̂S = 39° [corr ∠s, SR ∥ PQ]\nP̂ = TŜR = 55° [corr ∠s, SR ∥ PQ]\nT̂ = T̂ [common]\n"
        "ΔTRS ||| ΔTQP [∠, ∠, ∠]",                                                                                      # the memo
        "SR ∥ PQ [midpt theorem]\nQ̂ = TR̂S = 39° [alt ∠s, SR ∥ PQ]\nP̂ = TŜR = 55° [alt ∠s, SR ∥ PQ]\nT̂ = T̂ [common]\n"
        "ΔTRS ||| ΔTQP [∠, ∠, ∠]",                                                                                      # alternate, not corresponding
        "SR ∥ PQ [midpt theorem]\nQ̂ = TR̂S = 39° [corr ∠s, SR ∥ PQ]\nP̂ = TŜR = 55° [corr ∠s, SR ∥ PQ]\nT̂ = T̂ [common]\n"
        "ΔTRS ≡ ΔTQP [AAS]",                                                                                            # congruent, not similar
        "SR ∥ PQ [midpt theorem]\nQ̂ = TR̂S = 39° [co-int ∠s, SR ∥ PQ]\nP̂ = TŜR = 55° [co-int ∠s, SR ∥ PQ]\nT̂ = T̂ [common]\n"
        "ΔTRS ||| ΔTQP [∠, ∠, ∠]"],                                                                                     # co-interior
        ["Why is SR parallel to PQ?", "Which angles does the transversal QT make with SR and PQ?"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Statistics", "marks": 8,
     "lead": "Mr Baloyi conducted a survey on the amount of airtime (in rands) EACH learner had on his or her cellphone:\n"
             "12 ; 16 ; 20 ; 22 ; 26 ; 30 ; 32 ; 38 ; 40 ; 46 ; 54 ; 60 ; 68", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Statistics: grouped data", "marks": 9,
     "lead": "The histogram below shows the distribution of examination scores for learners in introductory statistics.",
     "figure": P.fig("Q2", "A histogram, SCORES IN INTRODUCTORY STATISTICS: examination scores in classes of 10 from 30 to 100 on the "
                           "horizontal axis, frequency up to 60 on the vertical axis. The bars: 30-40: 12, 40-50: 18, 50-60: 55, "
                           "60-70: 57, 70-80: 43, 80-90: 11, 90-100: 4."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Analytical geometry", "marks": 15,
     "lead": "In the figure, ΔABC has vertices A(−11 ; 2), B(3 ; −5) and C(6 ; 1).",
     "figure": P.fig("Q3", "ΔABC on the axes: A(−11 ; 2) top left, C(6 ; 1) just above the x-axis on the right, B(3 ; −5) below the "
                           "x-axis. AB crosses both axes."), "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Trigonometry", "marks": 5,
     "lead": "In the diagram is a right-angled triangle with sides a, b and c, and B̂ = 90°. Write down the following in terms of a, b "
             "and c:",
     "figure": P.fig("Q4", "Right-angled triangle ABC with the right angle at B: side a = CB, side c = AB and side b = AC, the "
                           "hypotenuse, opposite B."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Trigonometry", "marks": 7,
     "lead": "Given: 13 cos θ = 12, where 0° ≤ θ ≤ 90°. Without using a calculator, use a sketch to determine the following:",
     "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Special angles", "marks": 5, "lead": "Simplify, without the use of a calculator:",
     "items": q43},
    {"id": "4.4", "title": "Question 4.4", "kind": "Trigonometric equations", "marks": 3,
     "lead": "Solve for x, correct to two decimal places:", "items": q44},
    {"id": "5", "title": "Question 5", "kind": "Trigonometric graphs", "marks": 13,
     "lead": "In the diagram below, the graphs of f(x) = cos x + a and g(x) = b sin x are drawn for x ∈ [−180° ; 180°]. The graph of f "
             "is reflected about the x-axis and then moved 2 units downwards to form the graph of h (5.7).",
     "figure": P.fig("Q5", "f, a cosine curve, from 0 at −180° up to its maximum 2 at 0° and down to 0 at 180°. g, a sine curve, "
                           "from 0 at −180° up to 2 at −90°, through 0 at 0°, down to −2 at 90° and back to 0 at 180°. They cross "
                           "once between −90° and 0°."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Trigonometry: heights and distances", "marks": 8,
     "lead": "An observer on the top of a cliff, 200 m above sea level, observes the angles of depression of two ships to be 45° for "
             "ship B and 30° for ship A, as shown below.",
     "figure": P.fig("Q6", "A cliff CD, 200 m high, D at the top. The ships A and B lie on the sea level line through C, A further from "
                           "the cliff. From D the angles of depression are 30° to A and 45° to B; at A the angle of elevation is 30°, "
                           "at B 45°, and the angle at C is 90°."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Measurement", "marks": 7,
     "lead": "Given the rectangular prism below:\nV = L × B × H\nSA = 2(L × B) + 2(L × H) + 2(H × B)",
     "figure": P.fig("Q7", "A rectangular prism 8 m long, 3 m deep (the breadth) and 5 m high."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Euclidean geometry", "marks": 10,
     "lead": "Give reasons for ALL geometry statements. ABCD is a parallelogram and AC is a diagonal, with A, F, E and C collinear "
             "points.",
     "figure": P.fig("Q8", "Parallelogram ABCD with B above A on the left and C above D on the right, diagonal AC. BE runs parallel to "
                           "AD to E on AC, and FD runs parallel to BC from F on AC to D. Angles numbered: Â₁, Â₂ at A; B̂₁, B̂₂ at B; "
                           "Ĉ₁, Ĉ₂ at C; D̂₁, D̂₂ at D; Ê₁, Ê₂ at E; F̂₁, F̂₂ at F."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Euclidean geometry", "marks": 10,
     "lead": "Give reasons for ALL geometry statements. In the diagram below, R is the midpoint of QT and S is the midpoint of PT. The "
             "length of SR is 2x + 4. Q̂ = 39° and P̂ = 55°.",
     "figure": P.fig("Q9", "ΔPQT with P bottom left, T bottom right and Q above T. S is on PT and R on QT; SR = 2x + 4. The angle at Q "
                           "is 39° and at P 55°."), "items": q9}]

P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2024", "total_marks": 100, "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "1.1", "kind": "no_fit", "detail": "The box and whisker diagram is BUILT on a number line: the learner places the five "
                                                   "values, marked as the memo marks it (min and max 1; the box 2, in combination)."},
          {"n": "9.1", "kind": "memo_issue", "detail": "The memo prints no answer for 9.1 (its page 9 ends with Question 9's diagram, page "
                                                       "10 starts at 9.2). 9.2's working, 18 = 4x + 8, is PQ = 2SR = 2(2x + 4) by the "
                                                       "midpoint theorem; the right option is that."},
          {"n": "6", "kind": "low_confidence", "detail": "The stem gives 45° for ship A and 30° for ship B; the diagram and the memo put "
                                                         "30° at A and 45° at B (AC = 200/tan 30°). The lead here follows the diagram."}],
         {"1": 8, "2": 9, "3": 15, "4": 20, "5": 13, "6": 8, "7": 7, "8": 10, "9": 10}, 100,
         {"1.4": ["1.1"], "2.4": ["2.1"], "2.5": ["2.1"], "3.4": ["3.1", "3.3"], "4.2.2": ["4.2.1"], "5.3": ["5.1"], "5.4": ["5.1"],
          "5.7.1": ["5.1"], "5.7.2": ["5.7.1"], "6.3": ["6.2"], "8.1.2": ["8.1.1"], "8.1.3": ["8.1.2"], "9.2": ["9.1"]},
         "Questions 1 to 9 (the whole paper)")
