"""Grade 11 Physical Sciences P1 (Physics) November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 10,
150 marks, 3 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): ecexams.co.za, 2025_November_Gr_11_Exams, the question paper zip (English PDF, 17 pages, text layer; its
diagrams are vector drawings and images) and the memo PDF (English and Afrikaans, 12 pages), read from their text and page images.

  python tools/ingest/transcribe_g11_ps_p1_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ps-p1-2025-11-ec/PHYSICAL SC P1 QP GR11 NOV 2025 ENG_watermark.pdf" "uploads/provincial/g11-ps-p1-2025-11-ec/PHYSICAL SC P1 MEMO NOV 2025 E+A_watermark.pdf" --id g11-ps-p1-2025-11-ec --from-json

The rulings as in transcribe_g11_ps_p1_2024_11_ec.py. 1.3's vector diagram was checked on a 200 dpi crop: F₃'s arrowhead is at the
top, so F₂ + F₃ = F₁ and the memo's B stands.
Figure boxes in PDF points (page 595 x 842): an image's box or the union of a diagram's drawings and labels (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-ps-p1-2025-11-ec", 595.3, 842.0, {
    "1.3": [3, 165.1, 407.3, 383.1, 536.8], "1.5": [4, 139.4, 133.6, 455.3, 237.5], "1.8": [5, 117.9, 113.5, 364.1, 177.5],
    "1.9": [5, 165.9, 356.4, 422.1, 530.4], "1.10": [6, 90.5, 104.2, 446.9, 298.7], "Q2": [7, 151.0, 135.8, 391.0, 292.9],
    "Q3": [8, 165.7, 142.9, 414.7, 301.9], "Q4": [9, 90.5, 163.9, 459.5, 267.7], "Q5": [10, 150.5, 182.0, 448.2, 358.5],
    "Q6": [11, 255.0, 130.0, 460.0, 276.4], "Q7": [12, 96.4, 152.7, 472.1, 233.6], "Q7.3": [12, 221.1, 360.7, 365.6, 412.7],
    "Q8": [13, 167.0, 125.5, 409.2, 262.6], "Q9": [14, 76.5, 145.6, 497.4, 435.0], "Q10": [15, 107.9, 145.2, 487.4, 356.6]}, start=4)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term
CHANGE = ["INCREASE", "DECREASE", "REMAIN THE SAME"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
q1 = [
    mcq("1.1", "Vector B and vector −B are acting on the same point X. The angle between the two vectors is …", ["180°.", "90°.", "0°.", "270°."], 0,
        ["What does the minus sign do to a vector's direction?", "Opposite directions make which angle?"]),
    mcq("1.2", "Two forces, F1 and F2, act on a point. If F1 and F2 act in the same direction, the maximum resultant has a magnitude of 13 N. If "
        "forces F1 and F2 act in opposite directions the magnitude of the minimum resultant force is 7 N. The magnitude of the two forces, in "
        "newton, is …", ["10 and 5.", "16 and 10.", "3 and 10.", "8 and 5."], 2,
        ["Their sum is 13 N and their difference 7 N.", "Which pair adds to 13 and differs by 7?"]),
    mcq("1.3", "In the vector diagram below, the resultant (net) vector is …", ["Zero.", "F1.", "F3.", "F2."], 1,
        ["Follow the arrows head to tail.", "Which vector runs from the first tail to the last head?"],
        figure=P.fig("1.3", "A right-angled triangle of vectors: F₁ up the left side, F₂ along the bottom to the right, F₃ along the slant from "
                            "the bottom right to the top.")),
    mcq("1.4", "A boy, who is standing in a lift, observes a 20 N mass piece suspended from a spring balance fixed to the roof of the lift. He "
        "sees that the reading on the spring balance is less than 20 N for a short interval. The CORRECT description for the motion of the lift "
        "during this short interval is that the lift is …", ["accelerating upwards", "not moving", "accelerating downwards",
                                                             "moving at a constant velocity"], 2,
        ["The reading is less than the weight: which way is the net force on the mass piece?", "The acceleration is in the direction of the "
                                                                                               "net force."]),
    mcq("1.5", "A car of mass m moving up a rough incline at a constant acceleration, a, under the influence of an applied force F(A). The incline "
        "makes an angle θ with the horizontal. The coefficient of kinetic friction between the surface and the wheels of the car is μk.\nThe "
        "magnitude of the frictional force acting on the car, can be calculated as …",
        ["F(A) − μk mg cos θ.", "μk mg sin θ − F(A).", "μk mg sin θ.", "μk mg cos θ."], 3,
        ["Friction = μk × the normal force.", "On a slope, which component of the weight does the surface push against?"],
        figure=P.fig("1.5", "A car on a slope inclined at θ to the horizontal.")),
    mcq("1.6", "The gravitational force which the earth exerts on the moon is …",
        ["directly proportional to the distance between their centers.", "inversely proportional to the mass of the moon.",
         "inversely proportional to the product of the mass of the moon and the mass of the earth.",
         "inversely proportional to the square of the distance between their centers."], 3,
        ["How does the gravitational force depend on the distance?", "And on the masses?"]),
    mcq("1.7", "The centers of two identical metallic spheres, each carrying a charge Q, are a distance r apart. Which ONE of the following pairs "
        "of changes (made simultaneously) will double the electrostatic force that one charged sphere exerts on the other?",
        ["Decrease the distance to r/2; double the charges on both spheres", "Decrease the distance to r/2; reduce the charge on one sphere "
                                                                              "to Q/2",
         "Decrease the distance to r/√2; reduce the charges on both spheres to Q/2", "Decrease the distance to r/√2; double the charges on "
                                                                                     "both spheres"], 1,
        ["F is proportional to Q₁Q₂ and inversely proportional to r².", "Work out the factor for each change and multiply them."]),
    mcq("1.8", "Three small identical spheres, A, B and C is charged as shown in the diagram below. The distance between sphere B and C is r.\n"
        "For sphere B to experience no resultant electrostatic force, the distance between A and B must be …", ["¼ r.", "½ r.", "2 r.", "4 r."], 2,
        ["A (+16 μC) and C (+4 μC) both attract B (−4 μC): the two forces must be equal.", "16/d² = 4/r²: solve for d."],
        figure=P.fig("1.8", "Spheres A (+16 μC), B (−4 μC) and C (+4 μC) in a line, B and C a distance r apart.")),
    mcq("1.9", "The battery in the circuit diagram below has a potential difference of 12 V and negligible internal resistance. Two voltmeters, V1 "
        "and V2, are connected to the circuit, as shown in the diagram below.\nWhen the switch is open, the CORRECT readings on V1 and V2 will be "
        "as follows:", ["V1 12 V; V2 12 V", "V1 0 V; V2 12 V", "V1 12 V; V2 0 V", "V1 0 V; V2 0 V"], 2,
        ["With the switch open, does current flow?", "Which voltmeter is across the gap?"],
        figure=P.fig("1.9", "A battery, an ammeter, a bulb, a switch with voltmeter V₁ across it, and a second bulb with voltmeter V₂ across "
                            "it, all in series.")),
    mcq("1.10", "Which ONE of the following graphs best represents the relationship between the electrical power and the current in a given Ohmic "
        "conductor?", ["Graph A", "Graph B", "Graph C", "Graph D"], 3,
        ["P = I²R for a resistor of fixed R.", "What shape is a graph of y = x²?"],
        figure=P.fig("1.10", "Four graphs of P up against I across. A: a horizontal line. B: a straight line from the origin. C: a curve falling "
                             "towards the I-axis. D: a curve from the origin that gets steeper."))]

# ---- QUESTION 2, the question paper page 7 and the memo page 3 ----
RX = "Rx = 700 cos 60° + 800 cos 40° − 650 = 350 + 612,84 − 650 = 312,84 N\n"
q2 = [
    stmt("2.1", "Define the term vector.", 2, ["A physical quantity having both magnitude and direction."],
         ["A physical quantity having magnitude only.", "A force that acts at right angles to a surface.", "The sum of two or more forces.",
          "A quantity that is always positive."], ["How is a vector different from a scalar?", "What does a vector have that a scalar does not?"], 2),
    work("2.2.1", "Calculate the magnitude and direction of the resultant of the three forces.", 9, [
        RX + "Ry = 700 sin 60° − 800 sin 40° = 606,22 − 514,23 = 91,99 N\nR² = 312,84² + 91,99²\nR = 326,08 N\n"
             "tan θ = {91,99}/{312,84}: θ = 16,39° above the positive x-axis",                                                   # the memo
        "Rx = 700 cos 30° + 800 cos 40° − 650 = 606,22 + 612,84 − 650 = 569,06 N\nRy = 700 sin 30° − 800 sin 40° = 350 − 514,23 = −164,23 N\n"
        "R² = 569,06² + 164,23²\nR = 592,28 N\ntan θ = {164,23}/{569,06}: θ = 16,10° below the positive x-axis",                    # 30° from the x-axis
        "Rx = 700 cos 60° + 800 cos 40° + 650 = 350 + 612,84 + 650 = 1 612,84 N\nRy = 700 sin 60° − 800 sin 40° = 606,22 − 514,23 = 91,99 N\n"
        "R² = 1 612,84² + 91,99²\nR = 1 615,46 N\ntan θ = {91,99}/{1 612,84}: θ = 3,26° above the positive x-axis",                 # F₃ added
        RX + "Ry = 700 sin 60° + 800 sin 40° = 606,22 + 514,23 = 1 120,45 N\nR² = 312,84² + 1 120,45²\nR = 1 163,31 N\n"
             "tan θ = {1 120,45}/{312,84}: θ = 74,40° above the positive x-axis"],                                               # F₂'s y upwards
        ["Resolve each force into x- and y-components: which angle does F₁ make with the x-axis?", "Which components point left or down?"]),
    work("2.2.2", "Calculate the magnitude of the gravitational force acting on the crate.", 2, [
        "W = mg = 25 × 9,8\nW = 245 N",          # the memo
        "W = {m}/{g} = {25}/{9,8}\nW = 2,55 N",  # divided
        "W = m\nW = 25 N",                       # the mass as the weight
        "W = mg = 25 × 10\nW = 250 N"],          # g taken as 10
        ["Which formula gives the weight?", "g = 9,8 m·s⁻²."]),
    stmt("2.3", "Explain why the three forces will not form a closed vector diagram.", 2,
         ["The resultant force is not equal to zero.", "The three forces are not in equilibrium."],
         ["The resultant force is equal to zero.", "The forces are not drawn to scale.", "Three forces can never form a closed vector diagram.",
          "The forces act on a crate, not on a point."], ["When do forces form a closed vector diagram?", "What did you find for the resultant?"], 2,
         after=["2.2.1"])]

# ---- QUESTION 3, the question paper page 8 and the memo page 4 ----
q3 = [
    stmt("3.1", "Write down Newton's Second Law of motion in words.", 2,
         ["The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.",
          "When a net force acts on an object, the object accelerates in the direction of the net force, the acceleration directly proportional "
          "to the net force and inversely proportional to the mass."],
         ["The acceleration of an object is directly proportional to its mass and inversely proportional to the net force.",
          "A body remains at rest or moves at constant velocity unless a net force acts on it.", "For every action there is an equal and "
                                                                                                 "opposite reaction.",
          "The net force on an object is always equal to its weight."], ["Which law links net force, mass and acceleration?",
                                                                         "What happens to the acceleration when the mass doubles?"], 2),
    work("3.2.1", "Calculate the coefficient of kinetic friction for the road surface.", 3, [
        "N = mg = (4 500)(9,8) = 44 100 N\nf(k) = μ(k)N: 8 820 = μ(k)(44 100)\nμ(k) = 0,2",          # the memo
        "N = 4 500 N\nf(k) = μ(k)N: 8 820 = μ(k)(4 500)\nμ(k) = 1,96",                                # the mass as N
        "N = (5 750)(9,8) = 56 350 N\nf(k) = μ(k)N: 8 820 = μ(k)(56 350)\nμ(k) = 0,16",               # both masses
        "N = mg = (4 500)(9,8) = 44 100 N\nf(k) = μ(k)N: 11 270 = μ(k)(44 100)\nμ(k) = 0,26"],        # the engine force as friction
        ["On a level road, what is the normal force on truck A?", "f(k) = μ(k)N: which force is the friction?"]),
    work("3.2.2", "Calculate the frictional force exerted by the road on bakkie B.", 3, [
        "N = (1 250)(9,8) = 12 250 N\nf(k) = (0,2)(12 250)\nf(k) = 2 450 N",            # the memo
        "N = 1 250 N\nf(k) = (0,2)(1 250)\nf(k) = 250 N",                               # the mass as N
        "N = (4 500)(9,8) = 44 100 N\nf(k) = (0,2)(44 100)\nf(k) = 8 820 N",            # the truck's
        "N = (1 250)(9,8) = 12 250 N\nf(k) = {12 250}/{0,2}\nf(k) = 61 250 N"],         # divided by μ(k)
        ["The bakkie is on the same road: which μ(k)?", "What is the bakkie's normal force?"], after=["3.2.1"]),
    work("3.2.3", "Calculate the magnitude of the tension in the tow rope.", 3, [
        "F(net) = F − f(k) − T\n0 = 11 270 − 8 820 − T\nT = 2 450 N",       # the memo
        "F(net) = F + f(k) − T\n0 = 11 270 + 8 820 − T\nT = 20 090 N",      # friction forwards
        "F(net) = F − T\n0 = 11 270 − T\nT = 11 270 N",                     # friction left out
        "F(net) = F − f(k) − T\n0 = 11 270 − 2 450 − T\nT = 8 820 N"],      # the bakkie's friction on the truck
        ["At constant velocity, what is the net force on truck A?", "Which forces act on the truck along the road?"])]

# ---- QUESTION 4, the question paper page 9 and the memo pages 5-6 ----
Q43 = "5 kg: T − 9 = 5a\n"
q4 = [
    stmt("4.1", "Define kinetic frictional force in words.", 2, ["The force that opposes the motion of a moving object relative to a surface."],
         ["The force that keeps an object at rest on a surface.", "The force of a surface pushing up on an object.",
          "The force that moves an object along a surface.", "The force of gravity on a moving object."],
         ["Does kinetic friction act on a moving or a stationary object?", "Does it help or oppose the motion?"], 2),
    draw("4.2", "Draw a labelled free body diagram showing all the forces acting on the 10 kg block.", 5,
         [["F(N)", 1], ["F (applied)", 1], ["T", 1], ["f(k)", 1], ["F(g)", 1]],
         ["Which bodies touch or pull the 10 kg block?", "Do not forget the earth's pull."],
         memo="The memo's diagram: F(N) up, F at 30° above the horizontal, T and f(k) to the left, F(g) down."),
    work("4.3.1", "Calculate the magnitude of the normal force exerted on the 10 kg block.", 3, [
        "N = F(g) − F sin θ\nN = 10 × 9,8 − 50 sin 30°\nN = 73 N",       # the memo
        "N = F(g) + F sin θ\nN = 10 × 9,8 + 50 sin 30°\nN = 123 N",      # the lift added
        "N = F(g) − F cos θ\nN = 10 × 9,8 − 50 cos 30°\nN = 54,70 N",    # the horizontal component
        "N = F(g)\nN = 10 × 9,8\nN = 98 N"],                              # the lift ignored
        ["The 50 N pull lifts the block a little: which component?", "N + F sin θ = F(g)."]),
    work("4.3.2", "Calculate the magnitude of the acceleration of the blocks.", 7, [
        Q43 + "10 kg: 50 cos 30° − T − (0,18 × 73) = 10a\n43,30 − 9 − 13,14 = 15a\na = 1,41 m·s⁻²",      # the memo
        Q43 + "10 kg: 50 − T − (0,18 × 73) = 10a\n50 − 9 − 13,14 = 15a\na = 1,86 m·s⁻²",                  # F not resolved
        Q43 + "10 kg: 50 cos 30° − T − (0,18 × 98) = 10a\n43,30 − 9 − 17,64 = 15a\na = 1,11 m·s⁻²",       # N taken as mg
        Q43 + "10 kg: 50 cos 30° − T − (0,18 × 73) = 10a\n43,30 − 9 − 13,14 = 10a\na = 2,12 m·s⁻²"],     # only the 10 kg block's mass
        ["Write F(net) = ma for each block, then add the two equations.", "Friction on the 10 kg block is μ(k)N with the N from 4.3.1."],
        after=["4.3.1"]),
    stmt("4.4", "How will the magnitude of the normal force calculated in QUESTION 4.3.1 be affected if the angle between the applied force and "
         "the horizontal decreases?\nChoose from INCREASES, DECREASES or REMAINS THE SAME. Explain the answer.", 3,
         ["INCREASES", "The vertical component of the applied force decreases.", "The weight stays the same, so the normal force increases."],
         ["DECREASES", "REMAINS THE SAME", "The vertical component of the applied force increases.", "The weight of the block decreases."],
         ["What happens to F sin θ when θ decreases?", "N = F(g) − F sin θ."], 1, after=["4.3.1"]),
    stmt("4.5", "Use PHYSICS PRINCIPLES to explain why it is very dangerous when children are not secured in a child's car seat when travelling "
         "in a car.", 3,
         ["When the car brakes, the child continues in its state of constant velocity.", "A secured seat belt exerts a net force on the child "
                                                                                          "in the opposite direction.",
          "That force slows the child down with the car, keeping the child in the seat."],
         ["When the car brakes, the child stops at once with the car.", "The child's inertia pulls it backwards into the seat.",
          "A heavier child has less inertia.", "Seat belts only work at high speeds."],
         ["Which law says a body keeps moving unless a net force acts?", "What provides that force when the child is buckled in?"], 1)]

# ---- QUESTION 5, the question paper page 10 and the memo page 7 ----
S8 = "6 kg: 0 = T − 6 × 9,8, so T = 58,8 N\n8 kg: 0 = T − F − f(k) − F(g∥)\n"
q5 = [
    stmt("5.1", "State Newton's first law in words.", 2,
         ["A body will remain in its state of rest or motion at constant velocity unless a non-zero resultant force acts on it."],
         ["A body accelerates in the direction of the net force acting on it.", "For every action there is an equal and opposite reaction.",
          "A body moving at constant velocity will slow down and stop unless a force keeps pushing it.",
          "The acceleration of a body is inversely proportional to its mass."],
         ["Which law describes what happens with NO resultant force?", "It is also called the law of inertia."], 2),
    draw("5.2", "Draw a free-body diagram showing ALL the forces acting on the 6 kg block before motion.", 2, [["T", 1], ["w", 1]],
         ["Which two bodies pull on the hanging block?", "In which directions?"], memo="The memo's diagram: T up and w down from a dot."),
    work("5.3.1", "Calculate the magnitude of the frictional force acting on the 8 kg block.", 3, [
        "f(k) = μ(k)mg cos θ\nf(k) = (0,25)(8)(9,8) cos 20°\nf(k) = 18,42 N",      # the memo
        "f(k) = μ(k)mg sin θ\nf(k) = (0,25)(8)(9,8) sin 20°\nf(k) = 6,70 N",       # sin for cos
        "f(k) = μ(k)mg\nf(k) = (0,25)(8)(9,8)\nf(k) = 19,60 N",                    # the slope ignored
        "f(k) = μ(k)mg cos θ\nf(k) = (0,25)(6)(9,8) cos 20°\nf(k) = 13,81 N"],     # the hanging block's mass
        ["On a slope, which component of the weight does the surface push against?", "f(k) = μ(k)N."]),
    work("5.3.2", "Calculate the magnitude of force F, that will keep the blocks at rest.", 5, [
        S8 + "0 = 58,8 − F − 18,42 − 8 × 9,8 sin 20°\nF = 13,57 N",        # the memo
        S8 + "0 = 58,8 − F + 18,42 − 8 × 9,8 sin 20°\nF = 50,41 N",        # friction up the slope
        S8 + "0 = 58,8 − F − 18,42 − 8 × 9,8 cos 20°\nF = −33,29 N",       # cos for the parallel component
        S8 + "0 = 58,8 − F − 18,42\nF = 40,38 N"],                          # the parallel component left out
        ["What is the tension, from the hanging block at rest?", "Which forces act along the slope on the 8 kg block?"], after=["5.3.1"]),
    work("5.4", "The force F is now removed, and the blocks accelerate at 2,6 m·s⁻². Calculate the speed with which the 6 kg block will strike "
         "the ground.", 3, [
        "v(f)² = v(i)² + 2aΔy\nv(f)² = 0² + 2(2,6)(2)\nv(f) = 3,22 m·s⁻¹",      # the memo's working (its 3,6 a slip)
        "v(f)² = v(i)² + 2aΔy\nv(f)² = 0² + 2(2,6)(2)\nv(f) = 10,40 m·s⁻¹",     # the square root not taken
        "v(f)² = v(i)² + 2aΔy\nv(f)² = 0² + 2(9,8)(2)\nv(f) = 6,26 m·s⁻¹",      # g for the acceleration
        "v(f)² = v(i)² + aΔy\nv(f)² = 0² + (2,6)(2)\nv(f) = 2,28 m·s⁻¹"],       # the 2 dropped
        ["The block starts at rest and falls 2 m.", "Which equation of motion has no time in it?"])]

# ---- QUESTION 6, the question paper page 11 and the memo page 8 ----
GM = "250 = {(6,67 × 10⁻¹¹)(5,98 × 10²⁴)(500)}/{r²}\n"
q6 = [
    answer("6.1", "Name and state the law that you can use to clarify the learner's misconception.", 3, [
        "Newton's third law: when object A exerts a force on object B, object B simultaneously exerts an oppositely directed force of equal "
        "magnitude on object A.",
        "Newton's third law: the body with the larger mass exerts the larger force on the smaller body.",
        "Newton's second law: the acceleration of an object is directly proportional to the net force and inversely proportional to its mass.",
        "Newton's law of universal gravitation: the larger mass exerts the larger force."],
        ["Is the earth's pull on the satellite bigger than the satellite's pull on the earth?", "Which law is about pairs of forces?"]),
    work("6.2", "Calculate the distance of the satellite above the surface of the earth.", 5, [
        "F = {Gm₁m₂}/{r²}\n" + GM + "r = 2,82 × 10⁷ m\nh = 2,82 × 10⁷ − 6,38 × 10⁶ = 2,18 × 10⁷ m",       # the memo
        "F = {Gm₁m₂}/{r²}\n" + GM + "r = 2,82 × 10⁷ m\nh = r = 2,82 × 10⁷ m",                             # r taken as the height
        "F = {Gm₁m₂}/{r²}\n" + GM + "r = 2,82 × 10⁷ m\nh = 2,82 × 10⁷ + 6,38 × 10⁶ = 3,46 × 10⁷ m",       # the radius added
        "F = {Gm₁m₂}/{r²}\n" + GM + "r = 7,98 × 10¹⁴ m\nh = 7,98 × 10¹⁴ − 6,38 × 10⁶ = 7,98 × 10¹⁴ m"],   # the square root not taken
        ["Solve for r, the distance between the centres.", "How far above the SURFACE is that?"])]

# ---- QUESTION 7, the question paper page 12 and the memo page 9 ----
K2 = "(9 × 10⁹)(100 × 10⁻⁶)²"
q7 = [
    stmt("7.1", "Write down Coulomb's Law in words.", 2,
         ["The electrostatic force of attraction or repulsion between two charges is directly proportional to the product of the charges and "
          "inversely proportional to the square of the distance between them."],
         ["The electrostatic force between two charges is inversely proportional to the distance between them.",
          "The electrostatic force between two charges is directly proportional to the sum of the charges.",
          "The electrostatic force between two charges is directly proportional to the product of their masses.",
          "The force between two charges is the same at every distance."], ["How does the force depend on the charges?",
                                                                            "How does it depend on the distance?"], 2),
    work("7.2", "Calculate the net electrostatic force experienced by point charge C due to charge A and B.", 6, [
        "F = {kQ₁Q₂}/{d²}\nF(A) = {" + K2 + "}/{(0,06)²} = 25 000 N right\nF(B) = {" + K2 + "}/{(0,03)²} = 100 000 N right\n"
        "F(net) = 25 000 + 100 000 = 125 000 N right",                                                                  # the memo
        "F = {kQ₁Q₂}/{d²}\nF(A) = {" + K2 + "}/{(0,03)²} = 100 000 N right\nF(B) = {" + K2 + "}/{(0,03)²} = 100 000 N right\n"
        "F(net) = 100 000 + 100 000 = 200 000 N right",                                                                 # A taken 3 cm from C
        "F = {kQ₁Q₂}/{d²}\nF(A) = {" + K2 + "}/{(0,06)²} = 25 000 N left\nF(B) = {" + K2 + "}/{(0,03)²} = 100 000 N right\n"
        "F(net) = 100 000 − 25 000 = 75 000 N right",                                                                   # A taken to attract C
        "F = {kQ₁Q₂}/{d²}\nF(A) = {" + K2 + "}/{(6)²} = 2,5 N right\nF(B) = {" + K2 + "}/{(3)²} = 10 N right\n"
        "F(net) = 2,5 + 10 = 12,5 N right"],                                                                            # cm not converted
        ["How far is C from A and from B, in metres?", "Like charges repel: which way does each force push C?"])]
q73 = [
    stmt("7.3.1", "Define electric field at a point in words.", 2, ["The electrostatic force experienced per unit positive charge placed at that "
                                                                    "point."],
         ["The electrostatic force experienced per unit negative charge placed at that point.", "The total charge stored at that point.",
          "The force between two charges divided by the distance between them.", "The work done to move a charge to that point."],
         ["An electric field is described by the force on a test charge.", "Which sign of test charge?"], 2),
    draw("7.3.2", "Draw an electric field pattern around the −2 μC charge.", 2,
         [["Correct field direction", 1], ["Lines starting from the sphere and not crossing each other", 1]],
         ["Do field lines point towards or away from a negative charge?", "Where do the lines start?"],
         memo="The memo's pattern: straight lines radially inwards, arrows pointing towards the charge, never crossing."),
    work("7.3.3", "Calculate the electric field strength at point P.", 3, [
        "E = {kQ}/{r²}\nE = {(9 × 10⁹)(2 × 10⁻⁶)}/{(0,1)²}\nE = 1,8 × 10⁶ N·C⁻¹ to the left",       # the memo
        "E = {kQ}/{r}\nE = {(9 × 10⁹)(2 × 10⁻⁶)}/{0,1}\nE = 1,8 × 10⁵ N·C⁻¹ to the left",          # r not squared
        "E = {kQ}/{r²}\nE = {(9 × 10⁹)(2 × 10⁻⁶)}/{(0,1)²}\nE = 1,8 × 10⁶ N·C⁻¹ to the right",      # away from a negative charge
        "E = {kQ}/{r²}\nE = {(9 × 10⁹)(2 × 10⁻⁶)}/{(10)²}\nE = 180 N·C⁻¹ to the left"],             # cm not converted
        ["E = kQ/r² with r in metres.", "Does the field at P point towards or away from the negative charge?"])]

# ---- QUESTION 8, the question paper page 13 and the memo page 10 ----
q8 = [
    answer("8.1", "What is the polarity of the magnetic field of the solenoid at point A?", 2, ["North pole", "South pole", "No polarity",
                                                                                              "North and south"],
           ["Lenz's law: the induced current opposes the change.", "To oppose an approaching north pole, what must end A become?"]),
    mcq("8.2", "In which direction will the current in the galvanometer deflect? Write down TOWARDS P or TOWARDS Q.", ["TOWARDS P", "TOWARDS Q"], 1,
        ["Use the polarity at A and the right-hand rule for the solenoid.", "Which way does the current leave the coil into the wire?"],
        after=["8.1"])]
q83 = [
    stmt("8.3.1", "State Faraday's law of electromagnetic induction.", 2,
         ["The magnitude of the induced emf across the ends of a conductor is directly proportional to the rate of change in the magnetic flux "
          "linkage with the conductor."],
         ["The magnitude of the induced emf is directly proportional to the magnetic flux through the conductor.",
          "The induced current flows in a direction that opposes the change that caused it.",
          "The magnitude of the induced emf is inversely proportional to the rate of change in the magnetic flux.",
          "The emf of a battery is the energy it gives to each coulomb of charge."],
         ["Does the emf depend on the flux or on how fast it changes?", "Is it directly or inversely proportional?"], 2),
    stmt("8.3.2", "Mention TWO ways in which the magnitude of the induced emf can be increased.", 2,
         ["Pull the coil out of the field faster.", "Increase the number of turns on the coil.", "Increase the area of the coil.",
          "Use a stronger magnetic field."],
         ["Pull the coil out more slowly.", "Use a weaker magnetic field.", "Reduce the number of turns on the coil."],
         ["Which quantities appear in ε = −NΔΦ/Δt?", "How can each be made to give a bigger emf?"], 1),
    work("8.3.3", "Calculate the magnetic flux linkage.", 3, [
        "Φ = BA cos θ\nΦ = (0,6)(0,08) cos 0°\nΦ = 0,048 Wb",       # the memo
        "Φ = BA cos θ\nΦ = (0,6)(0,08) cos 90°\nΦ = 0 Wb",          # the angle from the plane
        "Φ = {B}/{A}\nΦ = {0,6}/{0,08}\nΦ = 7,5 Wb",                # divided
        "Φ = B + A\nΦ = 0,6 + 0,08\nΦ = 0,68 Wb"],                  # added
        ["Φ = BA cos θ: the axis is along the field, so what is θ?", "Multiply B by the area."]),
    work("8.3.4", "Calculate the magnitude of the induced emf.", 3, [
        "ε = −{NΔΦ}/{Δt}\nε = −{350(0 − 0,048)}/{0,25}\nε = 67,2 V",       # the memo
        "ε = −{ΔΦ}/{Δt}\nε = −{0 − 0,048}/{0,25}\nε = 0,19 V",              # N left out
        "ε = −NΔΦΔt\nε = −350(0 − 0,048)(0,25)\nε = 4,2 V",                 # multiplied by Δt
        "ε = −{NΔΦ}/{Δt}\nε = −{350(0,048 − 0)}/{0,25}\nε = −67,2 V"],      # ΔΦ the wrong way: not a magnitude
        ["The coil is pulled right out: what is the final flux?", "ε = −NΔΦ/Δt."], after=["8.3.3"])]

# ---- QUESTION 9, the question paper page 14 and the memo page 11 ----
q9 = [
    stmt("9.1", "Is the conductor ohmic or non-ohmic? Explain the answer.", 3,
         ["Ohmic", "The graph is a straight line through the origin.", "The current is directly proportional to the potential difference."],
         ["Non-ohmic", "The graph curves away from a straight line.", "The current is inversely proportional to the potential difference.",
          "The resistance increases as the current increases."], ["What shape is the graph?", "Does it pass through the origin?"], 1),
    answer("9.2.1", "Write down the dependent variable for this investigation.", 1, ["Current", "Potential difference", "Resistance", "Temperature"],
           ["Which quantity is measured as the other is changed?", "Which goes on the vertical axis?"]),
    stmt("9.2.2", "Write down the control variables for this investigation.", 2,
         ["Temperature", "Length of the conductor", "Thickness of the conductor", "Resistance"], ["Current", "Potential difference"],
         ["Which quantities must stay the same for a fair test?", "Which two are being measured and changed?"], 1)]
q93 = [
    work("9.3.1", "Calculate the gradient of the above graph.", 3, [
        "gradient = {ΔI}/{ΔV}\ngradient = {0,6 − 0,2}/{2,5 − 0,85}\ngradient = 0,24 A·V⁻¹",      # the memo
        "gradient = {ΔV}/{ΔI}\ngradient = {2,5 − 0,85}/{0,6 − 0,2}\ngradient = 4,13 V·A⁻¹",      # upside down
        "gradient = {ΔI}/{ΔV}\ngradient = {0,6}/{2,5 − 0,85}\ngradient = 0,36 A·V⁻¹",            # one current reading
        "gradient = {ΔI}/{ΔV}\ngradient = {0,6 − 0,2}/{2,5 + 0,85}\ngradient = 0,12 A·V⁻¹"],     # the potential differences added
        ["Read two points on the line.", "Gradient = change in I ÷ change in V."]),
    work("9.3.2", "Use a calculation to motivate whether this conductor is suitable to be used for this electric heater.", 6, [
        "R = {1}/{gradient} = {1}/{0,24} = 4,2 Ω\nP = I²R: 150 = 6²R\nR = 4,2 Ω\nSuitable: the conductor's resistance equals the resistance "
        "needed",                                                                                                                  # the memo
        "R = gradient = 0,24 Ω\nP = I²R: 150 = 6²R\nR = 4,2 Ω\nNot suitable: 0,24 Ω is not 4,2 Ω",                                 # R = gradient
        "R = {1}/{gradient} = {1}/{0,24} = 4,2 Ω\nP = IR: 150 = 6R\nR = 25 Ω\nNot suitable: 4,2 Ω is not 25 Ω",                   # P = IR
        "R = {1}/{gradient} = {1}/{0,24} = 4,2 Ω\nP = {V²}/{R} with V = 6: 150 = {36}/{R}\nR = 0,24 Ω\nNot suitable: 4,2 Ω is not 0,24 Ω"],  # 6 A as 6 V
        ["The graph is I against V: how is the gradient related to R?", "Which formula links P, I and R?"], after=["9.3.1"])]

# ---- QUESTION 10, the question paper page 15 and the memo page 12 ----
Q10 = "{1}/{R(p)} = {1}/{10} + {1}/{11 + 17}\nR(p) = 7,37 Ω\nR(ext) = 7,37 + 5 = 12,37 Ω\n"
q10 = [
    term("10.1", "Write down the term that is used to describe the underlined words (12 J of energy is given to each coulomb of charge that passes "
         "through the battery per second).", ["emf", "electromotive force"],
         ["It is measured in volts.", "It is the energy per coulomb the battery gives."]),
    work("10.2", "Calculate the current that flows through the 5 Ω resistor.", 6, [
        Q10 + "emf = I(R + r): 12 = I(12,37 + 0,6)\nI = 0,93 A",                                                            # the memo
        "{1}/{R(p)} = {1}/{10} + {1}/{11} + {1}/{17}\nR(p) = 4,00 Ω\nR(ext) = 4,00 + 5 = 9,00 Ω\nemf = I(R + r): 12 = I(9,00 + 0,6)\n"
        "I = 1,25 A",                                                                                                        # 11 Ω and 17 Ω in parallel
        Q10 + "emf = IR: 12 = I(12,37)\nI = 0,97 A",                                                                         # r ignored
        "R(p) = 10 + 11 + 17 = 38 Ω\nR(p) = 38 Ω\nR(ext) = 38 + 5 = 43 Ω\nemf = I(R + r): 12 = I(43 + 0,6)\nI = 0,28 A"],    # all in series
        ["Which resistors are in series, and which branch is in parallel with the 10 Ω?", "emf = I(R + r)."]),
    work("10.3", "Determine the reading on the voltmeter.", 3, [
        "V = IR(ext)\nV = (0,93)(12,37)\nV = 11,50 V",       # the memo
        "V = Ir\nV = (0,93)(0,6)\nV = 0,56 V",               # the lost volts
        "V = IR\nV = (0,93)(5)\nV = 4,65 V",                 # the 5 Ω only
        "V = I(R + r)\nV = (0,93)(12,97)\nV = 12,06 V"],     # the emf with rounding
        ["The voltmeter is across the battery's terminals.", "V = IR(ext)."], after=["10.2"]),
    mcq("10.4", "Switch S is now opened.\nWill the reading on the voltmeter, V, INCREASE, DECREASE or REMAIN THE SAME.", CHANGE, 0,
        ["What happens to the external resistance when S opens?", "How do the current and the lost volts change?"], marks=1),
    stmt("10.5", "Briefly explain the answer to QUESTION 10.4.", 3,
         ["The total resistance increases.", "The total current decreases.", "The lost volts decrease, so V(ext) = ε − V(int) increases."],
         ["The total resistance decreases.", "The total current increases.", "The emf of the battery increases.", "The internal resistance "
                                                                                                                    "decreases."],
         ["Opening S removes a branch: what happens to the total resistance?", "V(ext) = ε − Ir."], 1, after=["10.4"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as answers to the following questions.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Vectors", "marks": 15,
     "lead": "Three forces, F1, F2 and F3, NOT DRAWN TO SCALE, are applied to a crate of 25 kg as shown in the diagram below.",
     "figure": P.fig("Q2", "A crate at the origin of x- and y-axes: F₁ = 700 N up and to the right, 30° from the y-axis; F₂ = 800 N down and to "
                           "the right, 40° below the x-axis; F₃ = 650 N to the left along the x-axis."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Newton's laws", "marks": 11,
     "lead": "Truck A, of mass 4 500 kg travels at a CONSTANT VELOCITY while towing bakkie B, of mass 1 250 kg. The engine of truck A produces a "
             "force of 11 270 N. The road surface exerts a frictional force of 8 820 N on truck A.",
     "figure": P.fig("Q3", "Truck A (4 500 kg) towing bakkie B (1 250 kg) behind it, moving at 50 km·h⁻¹."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Newton's laws", "marks": 23,
     "lead": "A boy pulls a 10 kg block, that is attached to a 5 kg block by a light, inextensible string of negligible mass, with a force of "
             "50 N at an angle of 30° with the horizontal as shown in the diagram below. The coefficient of kinetic friction between the "
             "surface and the 10 kg block is 0,18. The 5 kg block experiences a kinetic frictional force of 9 N.",
     "figure": P.fig("Q4", "A 5 kg block on the left joined by a string (tension T) to a 10 kg block; a 50 N force pulls the 10 kg block at "
                           "30° above the horizontal."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Newton's laws", "marks": 15,
     "lead": "A block of mass 8 kg is held at rest on a rough inclined plane which makes an angle of 20° with the horizontal by a force F that "
             "acts down the inclined plane. The block is connected by a light inextensible string which passes over a light frictionless "
             "pulley to another block of mass 6 kg. The 6 kg block hangs vertically at 2 m above the ground as shown in the diagram below.\n"
             "The coefficient of kinetic friction between the 8 kg block and the surface of the inclined plane is 0,25. Ignore the effects of "
             "air friction.",
     "figure": P.fig("Q5", "An 8 kg block on a slope of 20°, with a force F down the slope; a string over a pulley at the top holds a 6 kg "
                           "block hanging 2 m above the ground."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Gravitation", "marks": 8,
     "lead": "A satellite of mass 500 kg orbits the earth as shown in the diagram below. The earth exerts a force of 250 N on the satellite.\n"
             "A learner argues that the earth exerts a bigger force on the satellite because it has a larger mass.",
     "figure": P.fig("Q6", "The earth (mass M) with a satellite of 500 kg in a circular orbit of radius r, its velocity v at a tangent."),
     "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Electrostatics", "marks": 8,
     "lead": "Three identical point charges A, B and C, all of magnitude +100 μC, are equally spaced on a straight line in a vacuum. The charges "
             "are a distance of 3 cm from each other as shown in the diagram below.",
     "figure": P.fig("Q7", "Charges A, B and C, each +100 μC, in a line, 3 cm apart."), "items": q7},
    {"id": "7.3", "title": "Question 7.3", "kind": "Electric fields", "marks": 7,
     "lead": "A negative charge of −2 μC is positioned 10 cm from point P, as shown in the diagram below.",
     "figure": P.fig("Q7.3", "A −2 μC charge on the left and the point P 10 cm to its right."), "items": q73},
    {"id": "8", "title": "Question 8", "kind": "Electromagnetism", "marks": 4,
     "lead": "The north pole of a magnet is pushed into a solenoid as shown in the diagram below.",
     "figure": P.fig("Q8", "A bar magnet, its N pole moving towards end A of a solenoid; end B is on the right. A galvanometer G joins the "
                           "solenoid's ends between P and Q."), "items": q8},
    {"id": "8.3", "title": "Question 8.3", "kind": "Electromagnetic induction", "marks": 10,
     "lead": "A coil with 350 turns has an area of 0,08 m². It is held with its axis coinciding with the direction of a magnetic field of strength "
             "0,6 T. In order to induce an emf in the coil, it is pulled out of the magnetic field in 0,25 seconds.", "items": q83},
    {"id": "9", "title": "Question 9", "kind": "Ohm's law", "marks": 6,
     "lead": "Learners investigate the relationship between current in a conductor and the potential differences across the ends of the "
             "conductor. The graph below is obtained from their investigation.",
     "figure": P.fig("Q9", "A graph of current I (A) against potential difference V (V): a straight line from the origin, reaching about "
                           "0,6 A at 2,5 V."), "items": q9},
    {"id": "9.3", "title": "Question 9.3", "kind": "Power", "marks": 9,
     "lead": "The learners intend to use the conductor to construct an electric heater that should be rated 150 W and draw a maximum current of "
             "6 A.", "items": q93},
    {"id": "10", "title": "Question 10", "kind": "Electric circuits", "marks": 14,
     "lead": "The battery used in the circuit diagram below has an internal resistance of 0,6 Ω. It is observed that 12 J of energy is given to "
             "each coulomb of charge that passes through the battery per second.\nThe resistance of the connecting wires can be ignored.",
     "figure": P.fig("Q10", "A battery (internal resistance 0,6 Ω) with a voltmeter V across it, in series with a 5 Ω resistor and a 10 Ω "
                            "resistor; across the 10 Ω, a branch of 17 Ω and 11 Ω in series with the switch S."), "items": q10},
]
P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
         [P.flag_workings(),
          P.flag_answers("'Name and state' (6.1) plays as named statements of a law."),
          {"n": "4.2", "kind": "no_fit", "detail": "Every drawing plays as pick the drawing: the free-body diagrams (4.2, 5.2) and the field of "
                                                   "the −2 μC charge (7.3.2), the memo's and three mistakes it marks down."},
          {"n": "5.4", "kind": "memo_issue", "detail": "The memo (page 7) writes 0² + 2(3,6)(2) = 3,79 m·s⁻¹; the stem's acceleration is 2,6 "
                                                       "m·s⁻², which gives v = √10,4 = 3,22 m·s⁻¹. The right option ends in 3,22; 3,79 is in no "
                                                       "option."},
          {"n": "3.1", "kind": "memo_issue", "detail": "The memo's first form (page 4) states Coulomb's law; its OR form, and its Afrikaans, "
                                                       "state Newton's Second Law, which the question asks for. The cards use the second law; "
                                                       "no card states Coulomb's law."},
          {"n": "2.2.1", "kind": "memo_issue", "detail": "The memo gives the direction as 73,7° beside θ = 16,39°: 90° − 16,39° = 73,61° from the "
                                                         "y-axis. The right option gives 16,39° above the positive x-axis."}],
         {"1": 20, "2": 15, "3": 11, "4": 23, "5": 15, "6": 8, "7": 15, "8": 14, "9": 15, "10": 14}, 150,
         {"2.3": ["2.2.1"], "3.2.2": ["3.2.1"], "4.3.2": ["4.3.1"], "4.4": ["4.3.1"], "5.3.2": ["5.3.1"], "8.2": ["8.1"], "8.3.4": ["8.3.3"],
          "9.3.2": ["9.3.1"], "10.3": ["10.2"], "10.5": ["10.4"]},
         "Questions 1 to 10 (the whole paper)")
