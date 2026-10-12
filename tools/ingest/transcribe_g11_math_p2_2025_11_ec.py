"""Grade 11 Mathematics P2 November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 10, 150 marks,
3 hours: statistics, analytical geometry, trigonometry, measurement, Euclidean geometry), hand-transcribed into the catalogue
format, then run through `ingest.py --from-json`. Stems, marks, answers and the memo's working are the paper's and the memo's own
(its English); clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2025_November_Gr_11_Exams, the
question paper zip (English PDF, 16 pages; most diagrams are images, the ogive and the box are vector drawings) and the memo PDF
(English and Afrikaans, 16 pages), read from their page images at 90 dpi.

  python tools/ingest/transcribe_g11_math_p2_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-math-p2-2025-11-ec/MATHS P2 QP GR 11 2025 ENG_watermark.pdf" "uploads/provincial/g11-math-p2-2025-11-ec/MATHS P2 MEMO GR 11  NOVEMBER 2025 (ENG & AFR)_watermark.pdf" --id g11-math-p2-2025-11-ec --from-json

The memo's shapes map by the Grade 12 rulings (provincial.py); a geometry statement carries its [reason] at the line's end. No part
of this paper asks for a drawing.
Figure boxes in PDF points (page 595 x 842): an image's box, or the union of a vector diagram's drawings (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-math-p2-2025-11-ec", 595.3, 841.9, {
    "Q2": [4, 60.4, 143.1, 531.3, 585.4], "Q3": [5, 57.3, 182.2, 539.2, 457.6], "Q4": [6, 56.4, 150.3, 415.0, 359.2],
    "Q5": [8, 55.8, 149.8, 539.5, 405.8], "Q6": [9, 92.4, 217.6, 479.0, 489.4], "Q7": [10, 71.1, 155.1, 474.0, 306.7],
    "Q8.1": [11, 142.0, 126.8, 453.1, 399.1], "Q8.2": [12, 90.4, 159.2, 401.6, 435.5], "Q9.1": [13, 124.8, 141.6, 465.1, 466.9],
    "Q9.2": [14, 93.3, 133.3, 479.9, 467.6], "Q10": [15, 139.2, 137.9, 440.2, 406.7]}, start=9)
work, answer, num = P.work, P.answer, P.num

# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
q1 = [
    work("1.1", "Calculate the value of x if the median (Q₂) of the data is 9 700.", 2, [
        "{x + 12 300}/{2} = 9 700\nx = 7 100",          # the memo
        "{x + 12 300}/{2} = 9 700\nx = 31 700",         # 12 300 added, not subtracted
        "{6 200 + x}/{2} = 9 700\nx = 13 200",          # the 4th and 5th values taken as the middle
        "x + 12 300 = 9 700\nx = −2 600"],              # not halved
        ["With 10 values, which two are in the middle?", "The median is halfway between them."]),
    work("1.2", "Calculate the value of y.", 3, [
        "{y + 186 200}/{10} = 21 770\ny + 186 200 = 217 700\ny = 31 500",      # the memo
        "{y + 179 100}/{10} = 21 770\ny + 179 100 = 217 700\ny = 38 600",      # x left out of the sum
        "{y + 186 200}/{9} = 21 770\ny + 186 200 = 195 930\ny = 9 730",        # ÷ 9 known values
        "{y + 186 200}/{10} = 21 770\ny + 186 200 = 2 177\ny = −184 023"],    # × 10 slipped as ÷ 10
        ["What is the sum of all ten prizes, x included?", "Mean = sum ÷ number of values."], after=["1.1"]),
    num("1.3", "Identify any outlier.", 87500, 0, "", ["Which prize is far above all the others?", "Write it without spaces or the R."]),
    num("1.4", "Determine the standard deviation of the prize money.", 25258.19, 0.5, "",
        ["Enter all ten prizes, x and y included, in your calculator's statistics mode.", "Use the population standard deviation, σ."],
        marks=2, after=["1.2"]),
    answer("1.5", "An amount of R200 is added to each of the top 10 participants. How will this adjustment affect the mean, the median and "
           "the standard deviation of the data?", 3,
           ["The mean and the median increase by R200; the standard deviation stays the same", "The mean, the median and the standard "
            "deviation all increase by R200", "The mean increases by R200; the median and the standard deviation stay the same",
            "The mean and the median increase by R200; the standard deviation increases by R20"],
           ["What happens to the middle value when every value moves up by the same amount?", "Does adding R200 to every prize change "
                                                                                              "how spread out they are?"])]

# ---- QUESTION 2, the question paper page 4 and the memo page 3 ----
q2 = [
    num("2.1", "How many employees participated in the survey?", 140, 0, "", ["Where does the ogive end?", "Read the last cumulative frequency."]),
    answer("2.2", "Write down the modal class of the data.", 1, ["30 < x ≤ 40", "40 < x ≤ 50", "50 < x ≤ 60", "0 < x ≤ 10"],
           ["In which class does the ogive climb most steeply?", "Which class has the biggest frequency?"]),
    num("2.3", "Determine how many employees earned R24 or less from the cumulative frequency graph.", 32, 1, "",
        ["Go up from R24 on the x-axis to the curve.", "Read the cumulative frequency across."], marks=2),
    work("2.4", "Determine the number of employees that earned R20 ≤ x ≤ R40.", 2, [
        "At R40 the ogive reads 118\nAt R20 it reads 24\n118 − 24 = 94",      # the memo
        "At R40 the ogive reads 118\nAt R20 it reads 24\n118 + 24 = 142",     # the readings added
        "At R40 the ogive reads 118\nAt R10 it reads 12\n118 − 12 = 106",     # read at R10, not R20
        "At R30 the ogive reads 52\nAt R20 it reads 24\n52 − 24 = 28"],       # read at R30, not R40
        ["What does the ogive give at R40 and at R20?", "How do two running totals give the number in between?"]),
    answer("2.5", "Determine the 25ᵗʰ percentile and the upper quartile of the data.", 2,
           ["Q₁ = R25 and Q₃ = R38", "Q₁ = R35 and Q₃ = R105", "Q₁ = R20 and Q₃ = R40", "Q₁ = R38 and Q₃ = R25"],
           ["25% and 75% of 140 employees are how many?", "Read across from those cumulative frequencies to the curve, then down."],
           after=["2.1"]),
    work("2.6", "Calculate the interquartile range of the data.", 2, [
        "IQR = Q₃ − Q₁\n= R38 − R25 = R13",       # the memo
        "IQR = Q₃ + Q₁\n= R38 + R25 = R63",       # the quartiles added
        "IQR = Q₃ − Q₁\n= 105 − 35 = 70",         # the positions, not the values
        "IQR = max − min\n= R60 − R0 = R60"],     # the range
        ["Which two values give the interquartile range?", "Subtract, do not add."], after=["2.5"])]

# ---- QUESTION 3, the question paper page 5 and the memo pages 4-5 ----
UV = "{3}/{2}x − {5}/{2} = {1}/{10}x + {59}/{10}\n{7}/{5}x = {42}/{5}, so x(U) = 6\n"
MID = "M(WS) = ({1 + 13}/{2} ; {6 + 3}/{2}) = (7 ; {9}/{2})\nM(QV) = ({3 + 11}/{2} ; {2 + 7}/{2}) = (7 ; {9}/{2})\n"
AR = "WU = {√101}/{2}\nUQ = √((6 − 3)² + ({13}/{2} − 2)²) = {3√13}/{2}\n"
q3 = [
    answer("3.1", "Write down the coordinates of Q.", 1, ["Q(3 ; 2)", "Q(2 ; 3)", "Q(3 ; 0)", "Q(0 ; 2)"],
           ["Q is level with P and straight above R.", "Which coordinate does each give?"]),
    work("3.2", "Calculate the gradient of QS.", 2, [
        "m(QS) = {3 − 2}/{13 − 3}\n= {1}/{10}",     # the memo
        "m(QS) = {13 − 3}/{3 − 2}\n= 10",           # x over y
        "m(QS) = {3 + 2}/{13 − 3}\n= {1}/{2}",      # 2 added, not subtracted
        "m(QS) = {3 − 0}/{13 − 0}\n= {3}/{13}"],    # S with the origin
        ["Which two points on QS do you know?", "Gradient = change in y ÷ change in x."], after=["3.1"]),
    work("3.3", "Determine the equation of WV.", 3, [
        "m(WV) = m(QS) = {1}/{10}\n6 = {1}/{10}(1) + c, so c = {59}/{10}\ny = {1}/{10}x + {59}/{10}",     # the memo
        "m(WV) = −10 (⊥ QS)\n6 = −10(1) + c, so c = 16\ny = −10x + 16",                                  # perpendicular
        "m(WV) = m(QS) = {1}/{10}\n6 = {1}/{10}(1) + c, so c = {61}/{10}\ny = {1}/{10}x + {61}/{10}",     # 1/10 added, not subtracted
        "m(WV) = m(QS) = {1}/{10}\n1 = {1}/{10}(6) + c, so c = {2}/{5}\ny = {1}/{10}x + {2}/{5}"],        # W's coordinates swapped
        ["How are the gradients of parallel lines related?", "Which point on WV do you know?"], after=["3.2"]),
    work("3.4", "If it is further given that the equation of QU is y = (3/2)x − 5/2, show that the coordinates of V are (11 ; 7).", 5, [
        UV + "y(U) = {3}/{2}(6) − {5}/{2} = {13}/{2}\n6 = {1 + x(V)}/{2} and {13}/{2} = {6 + y(V)}/{2}\nx(V) = 11 and y(V) = 7: V(11 ; 7)",  # the memo
        "V(11 ; 7): {1}/{10}(11) + {59}/{10} = 7\nV lies on WV\nU(6 ; {13}/{2}) is the midpoint of WV\n{3}/{2}(6) − {5}/{2} = {13}/{2}, so U is on QU\n"
        "So V(11 ; 7)",                                                                                           # starts from the answer
        "V is on WV: y = {1}/{10}x + {59}/{10}\nTake x(V) = 11\ny(V) = {11}/{10} + {59}/{10} = 7\nWV is a line through V\nSo V(11 ; 7)",  # x(V) assumed
        UV + "y(U) = {3}/{2}(6) + {5}/{2} = {23}/{2}\n6 = {1 + x(V)}/{2} and {23}/{2} = {6 + y(V)}/{2}\nx(V) = 11 and y(V) = 7: V(11 ; 7)"],  # 23 − 6 taken as 7
        ["U is on both WV and QU: what do you do with their equations?", "U is the midpoint of WV: how do you find V from W and U?"],
        after=["3.3"]),
    work("3.5", "Prove that WVSQ is a parallelogram.", 4, [
        MID + "The diagonals WS and QV have the same midpoint\nWVSQ is a parm [diagonals bisect each other]",                  # the memo
        "m(WV) = m(QS) = {1}/{10}\nWV ∥ QS\nOne pair of opposite sides is parallel\nWVSQ is a parm [one pair of opp sides ∥]",  # one pair is not enough
        "WS = √((13 − 1)² + (3 − 6)²) = √153\nQV = √((11 − 3)² + (7 − 2)²) = √89\nThe diagonals are not equal\n"
        "WVSQ is a parm [diagonals bisect each other]",                                                                         # unequal diagonals proved nothing
        MID + "The diagonals WS and QV have the same midpoint\nWVSQ is a parm [diagonals are equal]"],                         # the wrong reason
        ["Which two diagonals does WVSQ have?", "What does it tell you when the diagonals share their midpoint?"], after=["3.4"]),
    work("3.6", "Determine the length of WV. Leave your answer in surd form.", 2, [
        "WV = √((1 − 11)² + (6 − 7)²)\n= √101",     # the memo
        "WV = √((1 − 11)² − (6 − 7)²)\n= √99",      # the squares subtracted
        "WV = √((1 + 11)² + (6 + 7)²)\n= √313",     # the coordinates added
        "WV = (1 − 11)² + (6 − 7)²\n= 101"],        # the square root left out
        ["Which formula gives the distance between two points?", "What are the coordinates of W and V?"]),
    work("3.7", "Calculate the size of WÛQ.", 4, [
        "tan θ = m(WV) = {1}/{10}, θ = 5,71°\ntan α = m(QU) = {3}/{2}, α = 56,31°\nWÛQ = UQ̂S = α − θ [alt ∠s; WV ∥ QS]\nWÛQ = 50,60°",  # the memo
        "tan θ = m(WV) = {1}/{10}, θ = 5,71°\ntan α = m(QU) = {3}/{2}, α = 56,31°\nWÛQ = α + θ [alt ∠s; WV ∥ QS]\nWÛQ = 62,02°",           # added
        "tan θ = m(WV) = {1}/{10}, θ = 5,71°\ntan α = {2}/{3}, α = 33,69°\nWÛQ = UQ̂S = α − θ [alt ∠s; WV ∥ QS]\nWÛQ = 27,98°",           # QU's gradient upside down
        "tan θ = m(WV) = {1}/{10}, θ = 5,71°\ntan α = m(QU) = {3}/{2}, α = 56,31°\nWÛQ = 180° − (α − θ) [co-int ∠s; WV ∥ QS]\nWÛQ = 129,40°"],  # co-interior
        ["What are the angles of inclination of WV and QU?", "Which angle at Q equals WÛQ, and why?"], after=["3.4"]),
    work("3.8", "Determine the ratio: Area of PQRO / Area of ΔQUW", 6, [
        AR + "Area ΔQUW = {1}/{2} × {3√13}/{2} × {√101}/{2} × sin 50,60° = 10,50\nArea PQRO = 2 × 3 = 6\n"
             "{Area PQRO}/{Area ΔQUW} = {6}/{10,50} = {4}/{7}",                                                          # the memo
        "WU = √101\nUQ = √((6 − 3)² + ({13}/{2} − 2)²) = {3√13}/{2}\nArea ΔQUW = {1}/{2} × {3√13}/{2} × √101 × sin 50,60° = 21\n"
        "Area PQRO = 2 × 3 = 6\n{Area PQRO}/{Area ΔQUW} = {6}/{21} = {2}/{7}",                                           # WU not halved
        AR + "Area ΔQUW = {1}/{2} × {3√13}/{2} × {√101}/{2} × sin 50,60° = 10,50\nArea PQRO = 2 + 3 = 5\n"
             "{Area PQRO}/{Area ΔQUW} = {5}/{10,50} = {10}/{21}",                                                        # the sides added
        AR + "Area ΔQUW = {1}/{2} × {3√13}/{2} × {√101}/{2} × sin 50,60° = 10,50\nArea PQRO = 2 × 3 = 6\n"
             "{Area ΔQUW}/{Area PQRO} = {10,50}/{6} = {7}/{4}"],                                                         # the ratio upside down
        ["Which two sides of ΔQUW meet at U, and what is the angle between them?", "PQRO is a rectangle: how long are its sides?"],
        after=["3.6", "3.7"])]

# ---- QUESTION 4, the question paper pages 6-7 and the memo pages 6-8 ----
L431 = "cos x · tan x = sin x\n"
q41 = [
    work("4.1.1", "t", 2, [
        "tan 45° = {3}/{t}\nt = 3",                 # the memo
        "sin 45° = {3}/{t}\nt = 3√2",               # sine for the opposite over the adjacent
        "sin 45° = {t}/{3}\nt = {3√2}/{2}",         # the sides upside down
        "tan 45° = {3}/{t}\nt = {1}/{3}"],          # 3 ÷ t turned over
        ["Which sides of the right-angled triangle are t and 3?", "Which ratio uses the opposite and the adjacent side?"]),
    work("4.1.2", "k", 2, [
        "sin 45° = {3}/{k}\nk = 3√2",               # the memo
        "sin 45° = {k}/{3}\nk = {3√2}/{2}",         # the sides upside down
        "k = 3 + 3\nk = 6",                         # the sides added
        "tan 45° = {3}/{k}\nk = 3"],                # tan for the hypotenuse
        ["k is the hypotenuse: which ratio uses it with the side 3?", "What is sin 45°?"])]
q42 = [
    work("4.2.1", "Determine the value of cos α where cos α > 0 and 0° < α < 180°", 2, [
        "cos² α = {1}/{4}\ncos α = {1}/{2}",        # the memo
        "cos² α = {1}/{4}\ncos α = ±{1}/{2}",       # cos α > 0 ignored
        "cos² α = 4\ncos α = 2",                    # divided the wrong way
        "8 cos α = 2\ncos α = {1}/{4}"],            # the square ignored
        ["What is cos² α once 2 is moved and you divide by 8?", "Which sign does cos α > 0 allow?"]),
    work("4.2.2", "Hence, or otherwise, use a diagram to determine the value of 4[tan² α − cos² α]", 3, [
        "x = 1, r = 2, y = √(2² − 1²) = √3\n4[tan² α − cos² α] = 4[({√3}/{1})² − ({1}/{2})²]\n= 11",       # the memo
        "x = 1, r = 2, y = √(2² + 1²) = √5\n4[tan² α − cos² α] = 4[({√5}/{1})² − ({1}/{2})²]\n= 19",       # Pythagoras with a +
        "x = 1, r = 2, y = √(2² − 1²) = √3\n4[tan² α − cos² α] = 4[({√3}/{1})² − {1}/{2}]\n= 10",           # cos α not squared
        "x = 1, r = 2, y = √(2² − 1²) = √3\n4[tan² α − cos² α] = 4[({1}/{√3})² − ({1}/{2})²]\n= {1}/{3}"],  # tan α upside down
        ["Draw α with cos α = 1/2: what are x and r, and what is y?", "tan α = y ÷ x."], after=["4.2.1"])]
q43 = [
    work("4.3.1", "Simplify the above expression to a single trigonometric ratio of x.", 6, [
        L431 + "cos(x − 90°) = sin x and cos(−x) = cos x\n= {sin x}/{2[sin² x + cos² x]}\n= {sin x}/{2}",               # the memo
        L431 + "cos(x − 90°) = −sin x and cos(−x) = cos x\n= {sin x}/{2[−sin² x + cos² x]}\n= {sin x}/{2 cos 2x}",       # cos(x − 90°) as −sin x
        L431 + "cos(x − 90°) = sin x and cos(−x) = −cos x\n= {sin x}/{2[sin² x − cos² x]}\n= −{sin x}/{2 cos 2x}",       # cos(−x) as −cos x
        "cos x · tan x = 1\ncos(x − 90°) = sin x and cos(−x) = cos x\n= {1}/{2[sin² x + cos² x]}\n= {1}/{2}"],             # tan x taken as 1/cos x
        ["Write tan x as sin x/cos x.", "Which ratio is cos(x − 90°), and what is cos(−x)?"]),
    answer("4.3.2", "Hence, or otherwise, write down the period of the expression in QUESTION 4.3", 1, ["360°", "180°", "720°", "90°"],
           ["What is the period of sin x?", "Does dividing by 2 change the period?"], after=["4.3.1"])]
D44 = "= {cos 42° · cos 42° − (−tan 45°)²}/{(cos(90° + 42°))²}\n"
q44 = [
    work("4.4", "Simplify: (cos 42° sin 48° − tan²(−45°))/cos² 132° without using a calculator.", 5, [
        D44 + "= {cos² 42° − 1}/{(−sin 42°)²}\n= {1 − sin² 42° − 1}/{sin² 42°}\n= −1",                                   # the memo
        D44 + "= {cos² 42° + 1}/{(−sin 42°)²}\n= {2 − sin² 42°}/{sin² 42°}\n= {2}/{sin² 42°} − 1",                       # −(−1)² taken as +1
        "= {cos 42° · cos 42° − (−tan 45°)²}/{(cos(180° − 48°))²}\n= {cos² 42° − 1}/{(−cos 42°)²}\n= {cos² 42° − 1}/{cos² 42°}\n"
        "= −tan² 42°",                                                                                                    # cos 132° as −cos 42°
        D44 + "= {cos² 42° − 1}/{(−sin 42°)²}\n= {sin² 42°}/{sin² 42°}\n= 1"],                                          # cos² − 1 taken as sin²
        ["Write sin 48° and cos 132° as ratios of 42°.", "What is tan(−45°)?"])]
L451 = "LHS = {sin β}/{cos β} − sin β cos β\n"
q45 = [
    work("4.5.1", "Prove the above identity.", 3, [
        L451 + "= {sin β − sin β cos² β}/{cos β}\n= {sin β(1 − cos² β)}/{cos β}\n= tan β · sin² β = RHS",            # the memo
        "tan β · sin² β = tan β − sin β cos β\nsin² β = 1 − cos² β\n{sin β}/{cos β}(1 − cos² β) = tan β − sin β cos β\nLHS = RHS",  # both sides used at once
        L451 + "= {sin β − sin β cos β}/{cos β}\n= {sin β(1 − cos² β)}/{cos β}\n= tan β · sin² β = RHS",              # the lowest common denominator slipped
        L451 + "= {sin β − sin β cos² β}/{cos β}\n= {sin β(1 + cos² β)}/{cos β}\n= tan β · sin² β = RHS"],            # the sign in the bracket
        ["Write tan β as sin β/cos β and use one denominator.", "Which identity turns 1 − cos² β into one ratio?"]),
    answer("4.5.2", "For which value(s) of β will the identity in QUESTION 4.5 be undefined in the interval β ∈ [−180° ; 180°]?", 2,
           ["β = −90° and β = 90°", "β = 0° and β = 180°", "β = 90° only", "β = −180°, 0° and 180°"],
           ["Where is tan β undefined?", "For which β in the interval is cos β = 0?"])]
G46 = "3 sin θ = −2(1 − sin² θ)\n2 sin² θ − 3 sin θ − 2 = 0\n"
q46 = [
    work("4.6", "Determine the general solution of: 3 sin θ = −2 cos² θ", 6, [
        G46 + "(2 sin θ + 1)(sin θ − 2) = 0\nsin θ = −{1}/{2} or sin θ ≠ 2\nθ = 210° + k · 360° or θ = 330° + k · 360°, k ∈ ℤ",   # the memo
        G46 + "(2 sin θ − 1)(sin θ + 2) = 0\nsin θ = {1}/{2} or sin θ ≠ −2\nθ = 30° + k · 360° or θ = 150° + k · 360°, k ∈ ℤ",   # the factors' signs
        "3 sin θ = −2(1 + sin² θ)\n2 sin² θ + 3 sin θ + 2 = 0\nΔ = 9 − 16 < 0\nNo real sin θ\nNo solution",                       # cos² θ as 1 + sin² θ
        G46 + "(2 sin θ + 1)(sin θ − 2) = 0\nsin θ = −{1}/{2} or sin θ ≠ 2\nθ = 210° + k · 180°, k ∈ ℤ"],                         # the period of tan
        ["Which identity turns cos² θ into sin² θ?", "In which quadrants is sin θ negative?"])]

# ---- QUESTION 5, the question paper page 8 and the memo page 9 ----
q5 = [
    answer("5.1", "Determine the values of a and q", 2, ["a = 1 and q = 0", "a = −1 and q = 0", "a = 1 and q = 1", "a = 2 and q = −1"],
           ["f(180°) = 0: what is sin 90°?", "g has its maximum 1 at x = 0: what is cos 0°?"]),
    answer("5.2", "Write down the range of f", 2, ["y ∈ [−1,71 ; 0]", "y ∈ [−1 ; 1]", "y ∈ [−1,71 ; 1]", "y ∈ [−1 ; 0]"],
           ["Where in the interval is f highest, and where lowest?", "f(−90°) = sin(−45°) − 1: about how much is that?"], after=["5.1"]),
    answer("5.3", "Write down the amplitude of g", 1, ["1", "2", "0,5", "−1"], ["How far does g rise above its middle line?",
                                                                                 "g = cos x: what is its largest value?"]),
    answer("5.4", "Write down the value(s) of x where f(x) − g(x) = −2", 1, ["x = 0°", "x = 90°", "x = 180°", "x = −90°"],
           ["Where is f exactly 2 below g?", "Check: f(0°) = −1 and g(0°) = 1."]),
    answer("5.5", "For which values of x is f(x)g(x) ≤ 0?", 2,
           ["−90° ≤ x ≤ 90° or x = 180° or x = 270°", "90° ≤ x ≤ 270°", "−90° < x < 90°", "x = 90° or x = 180°"],
           ["f is never above the x-axis: when is the product negative or zero?", "Where is g on or above the x-axis, and where is f zero?"]),
    work("5.6", "The graph of h is obtained by shifting the graph of g by 90° to the left. Determine the equation of h in its simplest form.", 2, [
        "h(x) = cos(x + 90°)\n= −sin x",       # the memo
        "h(x) = cos(x − 90°)\n= sin x",        # shifted to the right
        "h(x) = cos(x + 90°)\n= sin x",        # the sign of the reduction
        "h(x) = cos(x + 90°)\n= −cos x"],      # the ratio unchanged
        ["Shifting left by 90° replaces x with what?", "Which ratio is cos(90° + x)?"], after=["5.1"])]

# ---- QUESTION 6, the question paper page 9 and the memo page 10 ----
q6 = [
    work("6.1", "Show that: OQ̂P = 180° − (β + α)", 2, [
        "QP̂O = α + θ [alt ∠s; SP ∥ OT]\nQÔP = β − θ\nOQ̂P = 180° − (α + θ) − (β − θ) [∠s in a Δ]\nOQ̂P = 180° − (β + α)",   # the memo
        "OQ̂P = 180° − (β + α) [given]\nQP̂O + QÔP = β + α\n(α + θ) + (β − θ) = β + α [∠s in a Δ]\nOQ̂P = 180° − (β + α)",   # starts from the answer
        "QP̂O = α + θ [corresp ∠s; SP ∥ OT]\nQÔP = β − θ\nOQ̂P = 180° − (α + θ) − (β − θ) [∠s in a Δ]\nOQ̂P = 180° − (β + α)",  # the wrong reason
        "QP̂O = α − θ [alt ∠s; SP ∥ OT]\nQÔP = β + θ\nOQ̂P = 180° − (α − θ) − (β + θ) [∠s in a Δ]\nOQ̂P = 180° − (β + α)"],   # the angles' parts swapped
        ["SP ∥ OT: which angle at P equals θ?", "What are the other two angles of ΔOQP?"]),
    work("6.2", "Show that OQ = x · sin(α + θ)/sin(β + α)", 3, [
        "{OQ}/{sin P̂} = {OP}/{sin OQ̂P}\n{OQ}/{sin(α + θ)} = {x}/{sin[180° − (β + α)]}\nOQ = {x sin(α + θ)}/{sin(β + α)}",     # the memo
        "{OQ}/{sin OQ̂P} = {OP}/{sin P̂}\n{OQ}/{sin[180° − (β + α)]} = {x}/{sin(α + θ)}\nOQ = {x sin(α + θ)}/{sin(β + α)}",     # sides with the wrong angles
        "{OQ}/{sin(α + θ)} = {x}/{sin[180° − (β + α)]}\nsin[180° − (β + α)] = −sin(β + α)\nOQ = {x sin(α + θ)}/{sin(β + α)}",  # the reduction's sign, then dropped
        "In ΔOQP, cos QÔP = {OP}/{OQ}\nOQ = {x}/{cos(β − θ)}\nOQ = {x sin(α + θ)}/{sin(β + α)}"],                            # a right angle assumed
        ["Which rule links two sides and their opposite angles?", "Which side is opposite P̂, and which opposite OQ̂P?"], after=["6.1"]),
    work("6.3", "Determine the value of x if θ = 15°, β = 60°, α = 30° and OQ = 5√2", 2, [
        "{5√2}/{sin 45°} = {x}/{sin 90°}\nx = 10",       # the memo
        "{5√2}/{sin 90°} = {x}/{sin 45°}\nx = 5",        # the formula turned over
        "{5√2}/{sin 45°} = {x}/{sin 75°}\nx = 9,66",     # β + θ for β + α
        "{5√2}/{cos 45°} = {x}/{cos 90°}\nx = 0"],       # cos for sin
        ["What are α + θ and β + α?", "Put the values into the formula from 6.2 and solve for x."], after=["6.2"])]

# ---- QUESTION 7, the question paper page 10 and the memo page 11 ----
q7 = [
    answer("7.1", "Write down length (L) and height (H) of the box in terms of x.", 2,
           ["L = 2x and H = x + 3", "L = x + 2 and H = 3x", "L = 2x and H = 3x", "L = x² and H = x + 3"],
           ["'Twice its width' means what?", "'3 cm more than its width' means what?"]),
    work("7.2", "Write an expression for the total surface area of the rectangular box in terms of x.", 3, [
        "SA = 2(2x · x) + 2(x(x + 3)) + 2(2x(x + 3))\n= 4x² + 2x² + 6x + 4x² + 12x\n= 10x² + 18x",      # the memo
        "SA = 2x · x + x(x + 3) + 2x(x + 3)\n= 2x² + x² + 3x + 2x² + 6x\n= 5x² + 9x",                   # each face counted once
        "V = 2x · x · (x + 3)\n= 2x²(x + 3)\n= 2x³ + 6x²",                                              # the volume
        "SA = 2(2x · x) + 2(x(x + 3)) + 2(2x(x + 3))\n= 4x² + 2x² + 6x + 4x² + 6\n= 10x² + 6x + 6"],    # 2(2x(x + 3)) as 4x² + 6
        ["A closed box has three pairs of faces: what are their sizes?", "SA = 2lb + 2lh + 2bh."], after=["7.1"]),
    work("7.3", "Hence or otherwise, determine the value of x.", 4, [
        "10x² + 18x = 784\n5x² + 9x − 392 = 0\n(5x + 49)(x − 8) = 0\nx = 8 (x ≠ −{49}/{5})",        # the memo
        "10x² + 18x = 784\n5x² + 9x − 392 = 0\n(5x − 49)(x + 8) = 0\nx = {49}/{5} (x ≠ −8)",        # the signs in the factors
        "10x² + 18x = 784\n10x² + 18x + 784 = 0\nΔ = 18² − 4(10)(784) < 0\nNo real x",               # 784 moved without its sign change
        "10x² + 18x = 784\n5x² + 9x − 784 = 0\nx = {−9 ± √15 761}/{10}\nx = 11,65 (x ≠ −13,45)"],    # 784 not halved
        ["Set your expression equal to 784.", "Divide by 2 and factorise: which root is a length?"], after=["7.2"]),
    work("7.4", "Calculate the volume of the box.", 2, [
        "V = (8)(2 × 8)(3 + 8)\n= 1 408 cm³",                        # the memo
        "V = (8)(2 × 8)(3 × 8)\n= 3 072 cm³",                        # H as 3x
        "V = (8)(8 + 2)(8 + 3)\n= 880 cm³",                          # L as x + 2
        "V = 2(8)(16) + 2(8)(11) + 2(16)(11)\n= 784 cm³"],           # the surface area
        ["What are L, x and H when x = 8?", "V = lbh."], after=["7.3"])]

# ---- QUESTION 8, the question paper pages 11-12 and the memo pages 12-13 ----
C81 = "Construction: join OA and OC\nIn ΔAOB and ΔCOB: AO = CO [radii]\n"
P822 = "TR = 2(UR) = 10 [diameter]\nŜ = 90° [∠ in semi-circle]\n10² = x² + (x + 2)² [Pyth]\n"
q81 = [
    work("8.1", "Use the diagram above to prove the theorem which states that the line drawn from the centre of a circle perpendicular to a "
         "chord bisects the chord, that is, prove that AB = BC.", 5, [
        C81 + "AB̂O = CB̂O = 90° [∠s on a str line]\nOB = OB [common]\nΔAOB ≡ ΔCOB [RHS], so AB = BC",              # the memo
        C81 + "AB̂O = CB̂O = 90° [∠s on a str line]\nOB = OB [common]\nΔAOB ≡ ΔCOB [SAS], so AB = BC",              # SAS: the angle is not between the sides
        "Construction: join OA and OC\nIn ΔAOB and ΔCOB: AB = BC [given]\nAB̂O = CB̂O = 90° [∠s on a str line]\nOB = OB [common]\n"
        "ΔAOB ≡ ΔCOB [SAS], so AB = BC",                                                                             # starts from the answer
        C81 + "AB̂O = CB̂O = 90° [∠ in semi-circle]\nOB = OB [common]\nΔAOB ≡ ΔCOB [RHS], so AB = BC"],              # the wrong reason for 90°
        ["Which construction gives you two triangles?", "Which three facts make the triangles congruent, and by which case?"])]
q82 = [
    work("8.2.1", "UR", 4, [
        "PQ = QR = 4 cm [line from centre ⊥ to chord]\nUR = √(4² + 3²) [Pyth]\nUR = 5 cm",      # the memo
        "PQ = QR = 8 cm [line from centre ⊥ to chord]\nUR = √(8² + 3²) [Pyth]\nUR = √73 cm",    # PR not halved
        "PQ = QR = 4 cm [line from centre ⊥ to chord]\nUR = 4 + 3 [Pyth]\nUR = 7 cm",          # the sides added
        "PQ = QR = 4 cm [tan ⊥ radius]\nUR = √(4² + 3²) [Pyth]\nUR = 5 cm"],                   # the wrong reason
        ["What does UQ ⊥ PR do to the chord PR?", "Which right-angled triangle has UR as its hypotenuse?"]),
    work("8.2.2", "TS", 6, [
        P822 + "2x² + 4x − 96 = 0\n(x − 6)(x + 8) = 0\nTS = 6 cm (x ≠ −8)",                                       # the memo
        "TR = UR = 5 [radii]\nŜ = 90° [∠ in semi-circle]\n5² = x² + (x + 2)² [Pyth]\n2x² + 4x − 21 = 0\nx = {−4 ± √184}/{4}\n"
        "TS = 2,39 cm (x ≠ −4,39)",                                                                                # the radius for the diameter
        P822 + "100 = x² + x² + 4\nx² = 48\nTS = 6,93 cm (x ≠ −6,93)",                                            # (x + 2)² as x² + 4
        P822 + "2x² + 4x − 96 = 0\n(x + 6)(x − 8) = 0\nTS = 8 cm (x ≠ −6)"],                                      # the signs in the factors
        ["TR is a diameter: what is the angle at S?", "Which equation does Pythagoras give in ΔTSR?"], after=["8.2.1"])]

# ---- QUESTION 9, the question paper pages 13-14 and the memo pages 14-15 ----
q91 = [
    work("9.1.1", "Ô₁", 2, [
        "Ô₁ = 2 × 15°\nÔ₁ = 30° [∠ at centre = 2 × ∠ at circumf]",     # the memo
        "Ô₁ = Ê₂\nÔ₁ = 15° [∠s in the same seg]",                       # equal, not double
        "Ô₁ = 180° − 2(15°)\nÔ₁ = 150° [∠s in a Δ]",                    # the angle at O in the isosceles triangle
        "Ô₁ = 2 × 15°\nÔ₁ = 30° [∠s opp equal radii]"],                 # the wrong reason
        ["Which angle at the circumference stands on the same arc BC as Ô₁?", "How is an angle at the centre related to it?"]),
    work("9.1.2", "Â", 2, [
        "Ô₂ = 150° [∠s on a str line]\nÂ = 75° [∠ at centre = 2 × ∠ at circumf]",      # the memo
        "Ô₂ = 150° [∠s on a str line]\nÂ = 150° [∠s in the same seg]",                  # equal, not half
        "Ô₂ = 30° [vert opp ∠s]\nÂ = 15° [∠ at centre = 2 × ∠ at circumf]",             # Ô₂ taken as vertically opposite Ô₁
        "Ô₂ = 150° [∠s on a str line]\nÂ = 300° [∠ at centre = 2 × ∠ at circumf]"],     # doubled, not halved
        ["BOE is a straight line: what is Ô₂?", "Which angle at the centre stands on the same arc CE as Â?"], after=["9.1.1"]),
    work("9.1.3", "D̂", 2, [
        "D̂ = 180° − 75°\nD̂ = 105° [opp ∠s of a cyclic quad]",       # the memo
        "D̂ = Â\nD̂ = 75° [∠s in the same seg]",                       # equal, not supplementary
        "D̂ = 180° − 75°\nD̂ = 105° [ext ∠ of a cyclic quad]",         # the wrong reason
        "D̂ = 180° − 15°\nD̂ = 165° [opp ∠s of a cyclic quad]"],       # Ê₂ for Â
        ["Which angle of cyclic quadrilateral ACDE is opposite D̂?", "What do opposite angles of a cyclic quadrilateral add up to?"],
        after=["9.1.2"]),
    work("9.1.4", "EĈF", 2, [
        "EĈF = Â\nEĈF = 75° [tan chord theorem]",      # the memo
        "EĈF = D̂\nEĈF = 105° [tan chord theorem]",     # the angle in the wrong segment
        "EĈF = Ê₂\nEĈF = 15° [alt ∠s]",                 # no parallel lines here
        "EĈF = Â\nEĈF = 75° [∠s in the same seg]"],     # the wrong reason
        ["EĈF is between the tangent CF and the chord CE.", "Which angle in the alternate segment equals it?"], after=["9.1.2"]),
    answer("9.1.5", "OĈG", 2, ["OĈG = 90° [radius ⊥ tangent]", "OĈG = 75° [tan chord theorem]", "OĈG = 90° [∠ in semi-circle]",
                               "OĈG = 105° [ext ∠ of a cyclic quad]"],
           ["OC is a radius and GCF the tangent at C.", "What angle does a radius make with the tangent at its end?"])]
q92 = [
    work("9.2.1", "Name TWO other angles each equal to P̂₁", 4, [
        "R̂₁ [tan chord theorem]\nMN̂Q [corresp ∠s; MN ∥ PR]",       # the memo
        "Q̂₁ [tan chord theorem]\nMN̂Q [corresp ∠s; MN ∥ PR]",       # the angle in the wrong segment
        "R̂₁ [tan chord theorem]\nP̂₃ [alt ∠s; MN ∥ PR]",             # an angle the parallel lines do not give
        "R̂₂ [tan chord theorem]\nN̂₃ [corresp ∠s; MN ∥ PR]"],        # the angles beside the right ones
        ["P̂₁ is between the tangent and the chord PQ: which angle in the alternate segment equals it?", "MN ∥ PR: which angle at N "
                                                                                                         "matches R̂₁?"]),
    work("9.2.2", "Prove that MNQP is a cyclic quadrilateral.", 4, [
        "P̂₁ = R̂₁ [tan chord theorem]\nR̂₁ = MN̂Q [corresp ∠s; MN ∥ PR]\nP̂₁ = MN̂Q\nMNQP is a cyclic quad [converse ext ∠ of cyclic quad]",  # the memo's proof
        "P̂₁ = R̂₁ [tan chord theorem]\nR̂₁ = MN̂Q [corresp ∠s; MN ∥ PR]\nP̂₁ = MN̂Q\nMNQP is a cyclic quad [opp ∠s of cyclic quad]",           # the theorem, not its converse
        "MNQP is a cyclic quad [given]\nR̂₁ = MN̂Q [corresp ∠s; MN ∥ PR]\nP̂₁ = MN̂Q\nMNQP is a cyclic quad [converse ext ∠ of cyclic quad]",  # starts from the answer
        "P̂₁ = R̂₁ [tan chord theorem]\nR̂₁ = MN̂Q [alt ∠s; MN ∥ PR]\nP̂₁ = MN̂Q\nMNQP is a cyclic quad [converse ext ∠ of cyclic quad]"],      # alternate for corresponding
        ["P̂₁ is an exterior angle of MNQP at P: which interior angle is opposite it?", "Which converse proves a quadrilateral cyclic from "
                                                                                         "an exterior angle?"], after=["9.2.1"]),
    work("9.2.3", "Prove that PN bisects SP̂R", 4, [
        "P̂₃ = N̂₂ [alt ∠s; MN ∥ PR]\nN̂₂ = Q̂₁ [∠s in the same seg]\nQ̂₁ = P̂₄ [tan chord theorem]\nP̂₃ = P̂₄, so PN bisects SP̂R",   # the memo
        "P̂₃ = N̂₂ [alt ∠s; MN ∥ PR]\nN̂₂ = Q̂₁ [tan chord theorem]\nQ̂₁ = P̂₄ [∠s in the same seg]\nP̂₃ = P̂₄, so PN bisects SP̂R",   # the reasons swapped
        "PN bisects SP̂R [given]\nN̂₂ = Q̂₁ [∠s in the same seg]\nQ̂₁ = P̂₄ [tan chord theorem]\nP̂₃ = P̂₄, so PN bisects SP̂R",     # starts from the answer
        "P̂₃ = N̂₂ [corresp ∠s; MN ∥ PR]\nN̂₂ = Q̂₁ [∠s in the same seg]\nQ̂₁ = P̂₄ [tan chord theorem]\nP̂₃ = P̂₄, so PN bisects SP̂R"],  # corresponding for alternate
        ["MN ∥ PR: which angle at N equals P̂₃?", "MNQP is cyclic: which angle at Q stands on the same chord MP as N̂₂?"], after=["9.2.2"])]

# ---- QUESTION 10, the question paper page 15 and the memo page 16 ----
q10 = [
    work("10", "Prove that AD ∥ FE", 5, [
        "Ĝ₃ = Â [corresp ∠s; GC ∥ AB]\nÂ = F̂ [∠s subt by = chords]\nĜ₃ = F̂\nAD ∥ FE [corresp ∠s =]",     # the memo
        "Ĝ₃ = Â [alt ∠s; GC ∥ AB]\nÂ = F̂ [∠s subt by = chords]\nĜ₃ = F̂\nAD ∥ FE [corresp ∠s =]",          # alternate for corresponding
        "Ĝ₃ = Â [corresp ∠s; GC ∥ AB]\nÂ = F̂ [∠s in the same seg]\nĜ₃ = F̂\nAD ∥ FE [corresp ∠s =]",       # BD and CE are different chords
        "AD ∥ FE [given]\nÂ = F̂ [∠s subt by = chords]\nĜ₃ = F̂\nAD ∥ FE [corresp ∠s =]"],                 # starts from the answer
        ["AB ∥ FC: which angle at G equals Â?", "BD = CE: which angles stand on these equal chords?"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Data handling", "marks": 11,
     "lead": "The following data represent the prize allocation (in R1 000) for the top ten male finishers in the 2025 20 km Marathon, "
             "listed in descending order from 10ᵗʰ place to the first place. Note that the prize money for 6ᵗʰ place and 3ʳᵈ place were not "
             "disclosed.\nThe mean prize across the available data is R21 770.\nPrizes: 3 600 ; 4 500 ; 5 400 ; 6 200 ; x ; 12 300 ; "
             "15 800 ; y ; 43 800 ; 87 500", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "The ogive", "marks": 10,
     "lead": "The cumulative frequency graph presents data from a survey conducted in a certain restaurant, detailing the distribution of "
             "tips earned by employees during their shift.",
     "figure": P.fig("Q2", "An ogive of tips in rands (0 to 70) against cumulative frequency (0 to 150), plotted at 0, 10, 20, 30, 40, 50 "
                           "and 60 and rising most steeply between 30 and 40."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Analytical geometry", "marks": 27,
     "lead": "In the diagram, W(1 ; 6), V, S and Q are the vertices of a quadrilateral WVSQ. P(0 ; 2) is the point where line PQ intersects "
             "the y-axis and R(3 ; 0) is the point where line QR intersects the x-axis. WV ∥ QS and WU = UV. PQRO is a rectangle.",
     "figure": P.fig("Q3", "Quadrilateral WVSQ: W(1 ; 6) top left, V top right, S(13 ; 3) on the right, Q at the bottom left. U is on WV, "
                           "joined to Q. PQRO is a rectangle with P(0 ; 2) on the y-axis and R(3 ; 0) on the x-axis."), "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Trigonometry", "marks": 4,
     "lead": "In the diagram below, O is the point of origin. OR = k, RÔS = 45°, R(t ; 3) is a point in the first quadrant and point S lies "
             "on the x-axis such that OS ⊥ RS.\nWithout using a calculator, calculate the value(s) of the following:",
     "figure": P.fig("Q4", "Right-angled triangle ORS: O at the origin, S on the x-axis with the right angle, R(t ; 3) above S; OR = k "
                           "and the angle at O is 45°."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Trigonometry", "marks": 5, "lead": "Given: 8cos² α − 2 = 0", "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Reduction formulae", "marks": 7,
     "lead": "Given: (cos x · tan x)/(2[sin x · cos(x − 90°) + cos x · cos(−x)])", "items": q43},
    {"id": "4.4", "title": "Question 4.4", "kind": "Reduction formulae", "marks": 5, "items": q44},
    {"id": "4.5", "title": "Question 4.5", "kind": "Identities", "marks": 5, "lead": "Given the identity: tan β − sin β · cos β = tan β · sin² β",
     "items": q45},
    {"id": "4.6", "title": "Question 4.6", "kind": "General solution", "marks": 6, "items": q46},
    {"id": "5", "title": "Question 5", "kind": "Trigonometric graphs", "marks": 10,
     "lead": "Given: f(x) = a sin(x/2) − 1 and g(x) = cos x + q, x ∈ [−90° ; 270°]\nUse the graphs to answer the following questions where "
             "x ∈ [−90° ; 270°]:",
     "figure": P.fig("Q5", "The graphs of f and g from −90° to 270°: g from (−90° ; 0) up to (0 ; 1), down to (180° ; −1) and up to "
                           "(270° ; 0); f rising from about (−90° ; −1,7) through (0 ; −1) to (180° ; 0) and down a little to 270°."),
     "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Trigonometry in two dimensions", "marks": 7,
     "lead": "A man standing on a horizontal plane at point O observes two helicopters positioned at points P and Q. The lines of sight from "
             "point O to each helicopter form angles of elevation θ and β with the horizontal plane. Additionally, a second man located in "
             "the helicopter at point P observes the helicopter at point Q, and his line of sight forms an angle of elevation α with the "
             "horizontal plane at P, measured along line PQ.\nON ⊥ NR and OP = x.",
     "figure": P.fig("Q6", "Triangle OQP: O at the bottom left on the horizontal OT, Q at the top on the line NR, P on the right. θ is the "
                           "angle of elevation of P from O and β of Q from O; α is the angle at P between the horizontal PS and PQ; OP = x."),
     "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Measurement", "marks": 11,
     "lead": "A closed rectangular box has a length (L) that is twice its width (W), and its height (H) is 3 cm more than its width. The "
             "surface area of the box is 784 cm². The length of the width is x cm.\nP = 2l + 2b ; A = l × b ; V = lbh ; SA = 2lb + 2lh + 2bh",
     "figure": P.fig("Q7", "A closed box with its length L along the front, its height H on the right edge and its width x along the "
                           "side, beside a box of formulae."), "items": q7},
    {"id": "8.1", "title": "Question 8.1", "kind": "Euclidean geometry", "marks": 5,
     "lead": "In the diagram below, O is the centre of the circle. AC is a chord. OB is drawn perpendicular to the chord.",
     "figure": P.fig("Q8.1", "A circle with centre O and the chord AC; OB is perpendicular to AC at B."), "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Euclidean geometry", "marks": 10,
     "lead": "In the diagram, TR is the diameter of the circle that passes through centre U. P, R, S and T are points on the circumference of "
             "the circle. UQ is a line from centre such that UQ ⊥ PR and PR is drawn.\nTS = x cm, SR = (x + 2) cm, PR = 8 cm and UQ = 3 cm\n"
             "Calculate, giving reasons, the length of:",
     "figure": P.fig("Q8.2", "A circle with centre U on the diameter TR. S is on the circle above, TS = x and SR = x + 2. PR is a chord "
                             "below, and UQ = 3 cm is perpendicular to PR at Q."), "items": q82},
    {"id": "9.1", "title": "Question 9.1", "kind": "Euclidean geometry", "marks": 10,
     "lead": "In the diagram below, O is the centre of the circle. ACDE and BCDE are cyclic quadrilaterals. GCF is a tangent to the circle at "
             "point C. Chord CE and line OC are drawn. Ê₂ = 15°.\nDetermine the size of the following angles below, giving reasons:",
     "figure": P.fig("Q9.1", "A circle with centre O on the diameter BE. A, B, C, D and E are on the circle; GCF is the tangent at C. "
                             "Chords AC, AE, BC, CD, DE and CE and the radius OC are drawn; Ê₂ = 15° is between EB and EC."), "items": q91},
    {"id": "9.2", "title": "Question 9.2", "kind": "Euclidean geometry", "marks": 12,
     "lead": "In the diagram below, P, Q, R and T are points on the circumference of the circle. PS is a tangent to the circle at P. Chord QR "
             "is produced to S. M and N are points on PS and RP respectively such that MN ∥ PR. PN is drawn. QT is produced to M.",
     "figure": P.fig("Q9.2", "A circle through P, Q, R and T. PS is the tangent at P; QR is produced to S. M is on PS and N on RS, with "
                             "MN ∥ PR; QT is produced to M and PN is drawn. The angles at P are numbered 1 to 4."), "items": q92},
    {"id": "10", "title": "Question 10", "kind": "Euclidean geometry", "marks": 5,
     "lead": "In the diagram below, A, B, C, D, E and F are points on the circumference of the circle. AD intersect CF at point G and CE at "
             "point H. AB ∥ FC and CE = BD.",
     "figure": P.fig("Q10", "A circle through A, B, C, D, E and F. AD crosses CF at G and CE at H; AB ∥ FC, and the chords BD and CE are "
                            "marked equal."), "items": q10},
]
P.finish(missions,
         {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
         [P.flag_workings("In a 'show that' or 'prove' (3.4, 3.5, 4.5.1, 6.1, 6.2, 8.1, 9.2.2, 9.2.3, 10) every option ends in the given "
                          "result; a wrong one reaches it through a wrong step or reason, or by starting from the answer."),
          P.flag_answers(),
          {"n": "1.3", "kind": "no_fit", "detail": "Read-off numbers stay typed on the keypad: 1.3 (87 500), 1.4 (σ = 25 258,19, within 0,5), "
                                                   "2.1 (140), 2.3 (32 read off the ogive, within 1)."},
          {"n": "3.4", "kind": "memo_issue", "detail": "The memo's last line (page 4) reads 11 = x(V) ; 5 = y(V): 13/2 = (6 + y(V))/2 gives "
                                                       "y(V) = 7, the stem's V(11 ; 7). The right option ends in V(11 ; 7)."},
          {"n": "5.2", "kind": "memo_issue", "detail": "The memo (page 9) gives y ∈ [−2 ; 0]; f(x) = sin(x/2) − 1 on [−90° ; 270°] has x/2 in "
                                                       "[−45° ; 135°], so its least value is sin(−45°) − 1 ≈ −1,71 (the graph's end point). "
                                                       "The right option is y ∈ [−1,71 ; 0]; [−2 ; 0] is in no option."},
          {"n": "5.5", "kind": "memo_issue", "detail": "The memo (page 9) gives −90° ≤ x ≤ 90°; the product is also 0 at x = 180° (f = 0) and "
                                                       "x = 270° (g = 0). The right option adds them; the memo's interval alone is in no "
                                                       "option."},
          {"n": "9.2.2", "kind": "memo_issue", "detail": "The memo's lines (page 15) read SP̂Q = Q̂ [tan chord], SP̂Q = M̂₁ [corresp ∠s], "
                                                         "Q̂₁ = M̂₁: as labelled they do not follow. The right option is the same proof with "
                                                         "9.2.1's angles: P̂₁ = R̂₁ = MN̂Q, so the exterior angle at P equals the interior "
                                                         "opposite angle [converse ext ∠ of cyclic quad]."},
          {"n": "9.2", "kind": "low_confidence", "detail": "The stem says N is on RP; the diagram puts N on RS (QR produced), where MN ∥ PR "
                                                           "can hold. The stem is kept as printed; the caption follows the diagram."},
          {"n": "7.3", "kind": "memo_issue", "detail": "The memo (page 11) writes x ≠ 40/5 for the rejected root; (5x + 49) = 0 gives −49/5. "
                                                       "The right option writes x ≠ −49/5."}],
         {"1": 11, "2": 10, "3": 27, "4": 32, "5": 10, "6": 7, "7": 11, "8": 15, "9": 22, "10": 5}, 150,
         {"1.2": ["1.1"], "1.4": ["1.2"], "2.5": ["2.1"], "2.6": ["2.5"], "3.2": ["3.1"], "3.3": ["3.2"], "3.4": ["3.3"], "3.5": ["3.4"],
          "3.7": ["3.4"], "3.8": ["3.6", "3.7"], "4.2.2": ["4.2.1"], "4.3.2": ["4.3.1"], "5.2": ["5.1"], "5.6": ["5.1"], "6.2": ["6.1"],
          "6.3": ["6.2"], "7.2": ["7.1"], "7.3": ["7.2"], "7.4": ["7.3"], "8.2.2": ["8.2.1"], "9.1.2": ["9.1.1"], "9.1.3": ["9.1.2"],
          "9.1.4": ["9.1.2"], "9.2.2": ["9.2.1"], "9.2.3": ["9.2.2"]},
         "Questions 1 to 10 (the whole paper)")
