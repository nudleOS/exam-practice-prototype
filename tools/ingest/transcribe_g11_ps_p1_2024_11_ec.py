"""Grade 11 Physical Sciences P1 (Physics) November 2024 (Eastern Cape Department of Education), Questions 1 to 10 (150 marks as printed;
144 played: 5.3 is left out, flag below), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`.
Stems, options, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions
are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the question paper zip (English PDF, 24 pages,
text layer; its diagrams are vector drawings and images) and the memo PDF (English and Afrikaans, 12 pages), read from their text
and page images.

  python tools/ingest/transcribe_g11_ps_p1_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ps-p1-2024-11-ec/PHYS SCIENCES  P1 QP GR11 NOV 2024 ENG D_watermark.pdf" "uploads/provincial/g11-ps-p1-2024-11-ec/PHYS SCIENCES P1 GR11 MEMO NOV 2024 ENG + AFR_watermark.pdf" --id g11-ps-p1-2024-11-ec --from-json

The Grade 12 rulings, as in transcribe_g11_ps_p1_2018_11.py: multiple choice printed in the paper as printed (where the memo's
letter is wrong physics, 1.4 and 1.5, the right letter is the physics and the memo's is flagged); a choice printed in the stem
(INCREASE / DECREASE / ...) an MCQ of the printed choices; every calculation an authored working (provincial.py); a definition, law
or explanation statements; "name and state" an MCQ of named statements; every drawing pick the drawing (pictures_lower.py).
Figure boxes in PDF points (page 595 x 842): the union of each diagram's drawings and labels, or its image (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-ps-p1-2024-11-ec", 595.2, 842.0, {
    "1.2": [3, 88.4, 334.9, 501.0, 377.5], "1.3": [3, 106.4, 471.3, 441.5, 543.9], "1.4": [4, 175.4, 128.5, 358.1, 163.2],
    "1.7": [5, 205.0, 125.0, 345.0, 235.0], "1.8": [6, 191.4, 107.9, 363.9, 260.1], "1.9": [7, 154.3, 93.3, 395.8, 204.1],
    "1.10": [7, 154.0, 454.2, 395.2, 536.3], "Q2": [8, 156.5, 168.1, 388.7, 343.8], "Q3": [9, 152.6, 171.1, 461.5, 246.9],
    "Q4": [10, 206.8, 154.3, 421.9, 281.0], "Q5": [11, 123.6, 152.5, 480.7, 350.3], "Q6": [12, 131.9, 166.4, 523.5, 231.2],
    "Q7": [13, 158.2, 146.8, 442.4, 238.3], "Q7.5": [13, 113.8, 469.3, 489.5, 550.3], "Q8": [14, 226.5, 131.0, 466.9, 254.0],
    "Q9": [15, 136.5, 127.5, 412.3, 254.4], "Q10a": [16, 167.7, 183.5, 427.9, 380.0], "Q10b": [16, 135.7, 423.6, 423.8, 591.0]}, start=1)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term
CHANGE = ["INCREASE", "DECREASE", "REMAIN THE SAME"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-7 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which of the following is a scalar quantity?", ["Force", "Velocity", "Acceleration", "Speed"], 3,
        ["A scalar has size only; a vector has size and direction.", "Which of the four has no direction?"]),
    mcq("1.2", "The objects below are all identical and resting on frictionless surfaces. Which object will experience the greatest "
        "acceleration?", ["A: 13 N to the left and 10 N to the right", "B: 12 N to the left and 12 N to the right",
                          "C: 7 N to the left and 2 N to the right", "D: 20 N to the left and 24 N to the right"], 2,
        ["The objects are identical: what decides the acceleration?", "Work out the net force on each object."],
        figure=P.fig("1.2", "Four identical blocks, A to D, each pulled by two opposite horizontal forces: A 13 N left and 10 N right; B 12 N "
                            "left and 12 N right; C 7 N left and 2 N right; D 20 N left and 24 N right.")),
    mcq("1.3", "The diagram below shows two trolleys held together by a compressed spring. The trolleys are initially at rest on a "
        "frictionless horizontal surface. Trolley A has a mass of 2 kg and trolley B has a mass of 1 kg.\nThe string breaks and the trollies "
        "move apart. The magnitude of the force that the spring exerts on trolley A is F. What is the magnitude of the force the spring "
        "exerts on trolley B?", ["½ F", "F", "2F", "4F"], 1,
        ["The spring pushes on both trolleys at the same time.", "What does Newton's Third Law say about the two forces?"],
        figure=P.fig("1.3", "Trolley A (2 kg) on the left and trolley B (1 kg) on the right, a compressed spring between them, on a "
                            "horizontal surface.")),
    mcq("1.4", "A block, slides to the left on a rough horizontal surface as shown in the diagram below. What are the directions of the "
        "resultant force and the acceleration of the block?",
        ["Resultant force to the right; acceleration to the left", "Resultant force to the right; acceleration to the right",
         "Resultant force to the left; acceleration to the left", "Resultant force to the left; acceleration to the right"], 1,
        ["Which force acts on a block sliding on a rough surface, and in which direction?", "Is the acceleration always in the direction "
                                                                                            "of the resultant force?"],
        figure=P.fig("1.4", "A block on a horizontal surface with an arrow labelled 'Direction of motion' pointing to the left.")),
    mcq("1.5", "A crate is being pushed across a rough horizontal floor at a constant velocity. If the force applied is suddenly removed, the "
        "crate will …", ["stop immediately.", "immediately start slowing down to a stop.",
                         "continue at constant velocity for a short time and then slow down to a stop.", "continue at constant velocity."], 1,
        ["Once the push is gone, which force is left on the crate?", "When does that force start to change the crate's velocity?"]),
    mcq("1.6", "A satellite experiences a gravitational force of magnitude F on the surface of the earth. The radius of the earth is R. The "
        "satellite now orbits the earth at an unknown height above the surface of the earth and experiences a gravitational force of "
        "magnitude ¼ F.\nThis unknown height above the earth's surface is …", ["R.", "2R.", "3R.", "4R."], 0,
        ["F is inversely proportional to r²: for ¼ F, what happens to r?", "r is measured from the earth's centre: how high above the "
                                                                          "surface is that?"]),
    mcq("1.7", "Two identical metal spheres X and Y, on isolated stands, have charges of +6 nC and −2 nC respectively. Y is brought into "
        "contact with X and then placed at its original position again.\nWhat is the direction in which electrons are transferred and the "
        "final charge on the spheres?",
        ["Electrons from Y to X; final charge −2 nC", "Electrons from Y to X; final charge 2 nC", "Electrons from X to Y; final charge 4 nC",
         "Electrons from X to Y; final charge −4 nC"], 1,
        ["After contact, identical spheres share the total charge equally.", "Electrons move towards the more positive sphere."],
        figure=P.fig("1.7", "Two metal spheres on stands: X with +6 nC and Y with −2 nC.")),
    mcq("1.8", "Two Ohmic conductors P and Q are connected in parallel to a battery as shown in the diagram below.\nThe resistance of "
        "conductor Q is much greater than that of conductor P. How does the potential difference across conductor Q and the current in Q "
        "compare to that of conductor P?",
        ["Potential difference: equal; current: less than", "Potential difference: equal; current: greater than",
         "Potential difference: greater than; current: greater than", "Potential difference: less than; current: less than"], 0,
        ["What is the same for resistors in parallel?", "With the same potential difference, which resistor carries less current?"],
        figure=P.fig("1.8", "A battery with conductors P and Q connected in parallel across it.")),
    mcq("1.9", "In the diagram below, the magnet is being pushed into the solenoid.\nWhat will the polarity of point A on the solenoid and the "
        "direction of the induced current in the solenoid be?",
        ["A: North; current P to Q", "A: South; current Q to P", "A: South; current P to Q", "A: North; current Q to P"], 0,
        ["Lenz's law: the induced current opposes the change that causes it.", "To oppose an approaching north pole, what must the near "
                                                                               "end of the solenoid become?"],
        figure=P.fig("1.9", "A bar magnet, S on the left and N on the right, moving to the right towards a solenoid whose near end is A; "
                            "the solenoid's ends are joined through a milliammeter between P and Q.")),
    mcq("1.10", "Three identical resistors X, Y and Z with equal resistance are connected as shown in the circuit diagram below.\nIf the "
        "power in X is P, then the power in Y is …", ["P.", "½ P.", "¼ P.", "2P."], 2,
        ["How does the current in X split between Y and Z?", "Power = I²R: what happens to the power when the current halves?"],
        figure=P.fig("1.10", "A battery in series with resistor X and with Y and Z connected in parallel."))]

# ---- QUESTION 2, the question paper page 8 and the memo page 3 ----
q2 = [
    stmt("2.1", "Explain the term forces in equilibrium in words.", 2,
         ["Forces are in equilibrium when the net force acting at the point is equal to zero.",
          "The forces are balanced, so the object remains stationary or moves at a constant velocity."],
         ["Forces are in equilibrium when they are all equal in size.", "Forces are in equilibrium when they all act in the same direction.",
          "Forces are in equilibrium when the net force is equal to the weight.", "Forces are in equilibrium when the object accelerates at "
                                                                                    "a constant rate."],
         ["What is the resultant of forces in equilibrium?", "What does an object do when the forces on it balance?"], 2),
    draw("2.2", "Draw a closed vector diagram showing ALL the forces acting at point O. Indicate the angle θ on the diagram.", 4,
         [["T", 1], ["Fg / W", 1], ["Fₐ = 60 N", 1], ["θ between W and T", 1]],
         ["Which three forces act at O?", "In a closed vector diagram, how do the arrows follow each other?"],
         memo="The memo's diagram: a right-angled triangle, W down the vertical side, Fₐ = 60 N along the bottom, T along the slant back to "
              "the top, head to tail, θ at the top between W and T."),
    work("2.3.1", "Magnitude of the tension T in the string OX", 3, [
        "T² = Fₐ² + W²\nT² = 60² + (8 × 9,8)²\nT = 98,72 N",       # the memo
        "T² = Fₐ² + W²\nT² = 60² + 8²\nT = 60,53 N",               # the mass for the weight
        "T = Fₐ + W\nT = 60 + (8 × 9,8)\nT = 138,40 N",            # the forces added as numbers
        "T² = W² − Fₐ²\nT² = (8 × 9,8)² − 60²\nT = 50,46 N"],      # Pythagoras the wrong way
        ["In the closed triangle, which side is T?", "What is the weight of 8 kg?"]),
    work("2.3.2", "Angle θ that the string OX makes with the vertical", 3, [
        "sin θ = {Fₐ}/{T}\nsin θ = {60}/{98,72}\nθ = 37,43°",      # the memo
        "cos θ = {Fₐ}/{T}\ncos θ = {60}/{98,72}\nθ = 52,57°",      # cos for sin
        "tan θ = {Fₐ}/{T}\ntan θ = {60}/{98,72}\nθ = 31,29°",      # tan with the hypotenuse
        "sin θ = {Fₐ}/{W}\nsin θ = {60}/{78,4}\nθ = 49,94°"],      # W as the hypotenuse
        ["Which side of the triangle is opposite θ, and which is the hypotenuse?", "Which ratio uses those two sides?"], after=["2.3.1"]),
    num("2.4", "Without doing a calculation, write down the magnitude of the resultant force at point O.", 0, 0, "N",
        ["The system is in equilibrium.", "What is the resultant of forces in equilibrium?"], marks=2)]

# ---- QUESTION 3, the question paper page 9 and the memo page 4 ----
Q3A = "Block A: F cos θ − T − f = 0 (constant velocity)\n8,26 cos 20° − T − 5,54 = 0\nT = 2,22 N\nBlock B: T = fk = μk N\n"
q3 = [
    stmt("3.1", "Define resultant force in words.", 2,
         ["It is a single force having the same effect as the sum of the forces acting together.", "The vector sum of two or more forces."],
         ["It is the largest of the forces acting on an object.", "It is the sum of the magnitudes of all the forces, ignoring direction.",
          "It is the force that keeps an object at rest.", "It is the force of friction on a moving object."],
         ["Is the resultant one force or many?", "How does it compare with the forces it replaces?"], 2),
    work("3.2.1", "Magnitude of the frictional force acting between block A and the rough surface", 4, [
        "fk = μk N\nN = 2 × 9,8 − 8,26 sin 20° = 16,77 N\nfk = 0,33 × 16,77\nfk = 5,54 N",       # the memo
        "fk = μk N\nN = 2 × 9,8 = 19,6 N\nfk = 0,33 × 19,6\nfk = 6,47 N",                         # the lift of F ignored
        "fk = μk N\nN = 2 × 9,8 + 8,26 sin 20° = 22,43 N\nfk = 0,33 × 22,43\nfk = 7,40 N",       # the lift added
        "fk = μk N\nN = 2 × 9,8 − 8,26 cos 20° = 11,84 N\nfk = 0,33 × 11,84\nfk = 3,91 N"],      # the horizontal component for the vertical
        ["F pulls A upwards a little: how does that change the normal force?", "fk = μk N."]),
    work("3.2.2", "Coefficient of kinetic friction between block B and the rough surface", 6, [
        Q3A + "2,22 = μk(1,5 × 9,8)\nμk = 0,15",                                                                         # the memo's working
        "Block A: F − T − f = 0 (constant velocity)\n8,26 − T − 5,54 = 0\nT = 2,72 N\nBlock B: T = fk = μk N\n2,72 = μk(1,5 × 9,8)\nμk = 0,19",  # F not resolved
        Q3A + "2,22 = μk(2 × 9,8)\nμk = 0,11",                                                                           # A's mass for B's
        Q3A + "2,22 = μk(3,5 × 9,8)\nμk = 0,06"],                                                                        # both masses
        ["At constant velocity, what is the net force on A, and so the tension T?", "On B, the tension balances the friction: fk = μk N."],
        after=["3.2.1"])]

# ---- QUESTION 4, the question paper page 10 and the memo page 5 ----
q4 = [
    stmt("4.1", "State Newton's First Law of Motion in words.", 2,
         ["A body will remain in its state of rest or motion at constant velocity unless a non-zero resultant force acts on it."],
         ["A body accelerates in the direction of the net force acting on it.", "For every action there is an equal and opposite reaction.",
          "A body moving at constant velocity will slow down and stop unless a force keeps pushing it.",
          "The acceleration of a body is inversely proportional to its mass."],
         ["Which law describes what a body does when there is NO resultant force?", "It is also called the law of inertia."], 2),
    stmt("4.2", "Why does the container remain stationary despite the tension being greater than the weight?", 2,
         ["There is air friction on the container, acting downwards.", "There is an extra downward force on the container."],
         ["The tension is not really greater than the weight.", "The container is too heavy to be moved.",
          "The helicopter pushes the container downwards.", "Air friction acts upwards on the container."],
         ["The container is stationary: what must the net force be?", "Which other force could balance the extra tension?"], 2),
    work("4.3", "Calculate the mass of the container.", 3, [
        "W = mg\n1 960 = m(9,8)\nm = 200 kg",         # the memo
        "W = mg\n1 960 = m(9,8)\nm = 19 208 kg",      # multiplied, not divided
        "W = mg\n2 100 = m(9,8)\nm = 214,29 kg",      # the tension for the weight
        "W = mg\n1 960 = m(10)\nm = 196 kg"],         # g taken as 10
        ["Which formula links weight and mass?", "Which number is the container's weight?"]),
    work("4.4", "Now the winch inside the helicopter starts to pull the container upwards with an acceleration of 0,13 m·s⁻² while the "
         "helicopter remains in its position.\n\nCalculate the magnitude of the tension in the cable as the container is being pulled "
         "upwards.", 4, [
        "Fnet = ma\nT − Fg − Fair = ma\nT − 1 960 − 140 = (200)(0,13)\nT = 2 126 N",     # the memo
        "Fnet = ma\nT − Fg = ma\nT − 1 960 = (200)(0,13)\nT = 1 986 N",                  # air friction left out
        "Fnet = ma\nT − Fg + Fair = ma\nT − 1 960 + 140 = (200)(0,13)\nT = 1 846 N",     # air friction upwards
        "Fnet = ma\nT − Fg − Fair = ma\nT − 1 960 − 140 = 0,13\nT = 2 100,13 N"],        # the mass left out of ma
        ["Which forces act on the container as it accelerates upwards?", "How big is the air friction, from the stationary container?"],
        after=["4.3"]),
    num("4.5", "After an acceleration of a few metres the container is pulled up at a constant velocity of 0,8 m·s⁻¹.\n\nWhat will the "
        "magnitude of the tension in the cable be while the container moves upwards at a constant velocity?", 2100, 0, "N",
        ["At constant velocity, what is the net force?", "Compare with the stationary container."])]

# ---- QUESTION 5, the question paper page 11 and the memo page 6 (5.3 left out: flag below) ----
q5 = [
    stmt("5.1", "State Newton's Second Law of Motion in words.", 2,
         ["When a net force is applied to an object, the object accelerates in the direction of the net force; the acceleration is directly "
          "proportional to the net force and inversely proportional to the mass of the object.",
          "The net force on an object is equal to the rate of change of its momentum, and is in the same direction."],
         ["The acceleration of an object is directly proportional to its mass and inversely proportional to the net force.",
          "A body remains at rest or moves at constant velocity unless a net force acts on it.",
          "For every action there is an equal and opposite reaction.", "The acceleration of an object is the same for every net force."],
         ["Which law links net force, mass and acceleration?", "How does the acceleration change when the mass doubles?"], 2),
    draw("5.2", "Draw a labelled free-body diagram showing ALL the forces acting on the 3 kg block.", 5,
         [["N", 1], ["F", 1], ["T", 1], ["f", 1], ["W", 1]],
         ["Which body pulls on the 3 kg block, and which surface touches it?", "Do not forget the force of the earth."],
         memo="The memo's diagram: N perpendicular to the slope, F up the slope, T and f down the slope, W straight down.")]

# ---- QUESTION 6, the question paper page 12 and the memo page 7 ----
GM = "(6,67 × 10⁻¹¹)(5,98 × 10²⁴)(4 600)"
q6 = [
    stmt("6.1", "State Newton's law of universal gravitation in words.", 2,
         ["Every particle in the universe attracts every other particle with a force that is directly proportional to the product of their "
          "masses and inversely proportional to the square of the distance between their centres."],
         ["Every particle attracts every other particle with a force that is inversely proportional to the distance between their centres.",
          "Every particle attracts every other particle with a force that is directly proportional to the sum of their masses.",
          "Every particle attracts every other particle with a force that does not depend on the distance between them.",
          "Every charged particle attracts every other particle with a force proportional to the product of their charges."],
         ["How does the force depend on the masses?", "How does it depend on the distance?"], 2),
    work("6.2", "Calculate the magnitude of the gravitational force between the earth and satellite A.", 4, [
        "F = {Gm₁m₂}/{r²}\nF = {" + GM + "}/{(6,38 × 10⁶ + 28 × 10⁶)²}\nF = 1 552,29 N",     # the memo
        "F = {Gm₁m₂}/{r²}\nF = {" + GM + "}/{(28 × 10⁶)²}\nF = 2 340,29 N",                 # the height for r
        "F = {Gm₁m₂}/{r}\nF = {" + GM + "}/{6,38 × 10⁶ + 28 × 10⁶}\nF = 5,34 × 10¹⁰ N",    # r not squared
        "F = {Gm₁m₂}/{r²}\nF = {" + GM + "}/{(6,38 × 10⁶ + 28 000)²}\nF = 44 682,74 N"],    # the height left in km
        ["r is measured from the earth's centre: what is it here?", "Convert 28 000 km to metres."]),
    stmt("6.3", "Explain the term weightlessness.", 2,
         ["Weightlessness is the sensation experienced when all contact forces are removed."],
         ["Weightlessness is when the gravitational force on an object is zero.", "Weightlessness is when an object has no mass.",
          "Weightlessness happens only far outside the earth's gravitational field.", "Weightlessness is when the normal force equals the weight."],
         ["Does gravity stop acting on an astronaut in orbit?", "What is missing that the body normally feels?"], 2),
    stmt("6.4", "What distance above the earth's surface should satellite B be to experience the same force towards the earth as satellite A?"
         "\nAnswer only GREATER THAN, LESS THAN or EQUAL TO. Explain the answer.", 4,
         ["GREATER THAN", "Satellite B's mass (5 300 kg) is greater than satellite A's (4 600 kg).",
          "The force on B must be the same as the force on A.", "So B must be farther from the earth: the force is inversely proportional to r²."],
         ["LESS THAN", "EQUAL TO", "Satellite B's mass is smaller than satellite A's.", "The force does not depend on the satellite's mass."],
         ["Which satellite has the greater mass?", "To keep the force the same with a bigger mass, what must happen to the distance?"], 1)]

# ---- QUESTION 7, the question paper page 13 and the memo pages 8-9 ----
E1 = "E₁ = {kQ}/{r²} = {9 × 10⁹(15 × 10⁻⁹)}/{(2 × 10⁻²)²} = 337 500 N·C⁻¹ to the left\n"
K2 = "(9 × 10⁹)(100 × 10⁻⁶)²"
q7 = [
    stmt("7.1", "Define the term electric field at a point.", 2,
         ["The electrostatic force experienced per unit positive charge placed at that point."],
         ["The electrostatic force experienced per unit negative charge placed at that point.", "The total charge stored at that point.",
          "The force between two charges divided by the distance between them.", "The work done to move a charge to that point."],
         ["An electric field is described by the force on a test charge.", "Which sign of test charge is used?"], 2),
    draw("7.2", "Draw the electric field pattern between charges A and B.", 3,
         [["Correct shape", 1], ["Correct field direction", 1], ["Lines starting from the spheres and not crossing each other", 1]],
         ["A is negative and B positive: where do field lines start and end?", "Can field lines cross?"],
         memo="The memo's pattern: lines leave B (positive) and curve into A (negative), between and around the spheres, never crossing."),
    work("7.3", "Calculate the magnitude of the unknown charge on sphere B.", 8, [
        E1 + "E₂ = {9 × 10⁹ Q}/{(8 × 10⁻²)²} = 1,40625 × 10¹² Q to the left\nE(net) = E₁ + E₂\n3,943 × 10⁵ = 337 500 + 1,40625 × 10¹² Q\n"
             "Q = 4,04 × 10⁻⁸ C",                                                                                         # the memo
        E1 + "E₂ = {9 × 10⁹ Q}/{(8 × 10⁻²)²} = 1,40625 × 10¹² Q to the right\nE(net) = E₁ − E₂\n3,943 × 10⁵ = 337 500 − 1,40625 × 10¹² Q\n"
             "Q = −4,04 × 10⁻⁸ C",                                                                                        # B's field taken to the right
        E1 + "E₂ = {9 × 10⁹ Q}/{(10 × 10⁻²)²} = 9 × 10¹¹ Q to the left\nE(net) = E₁ + E₂\n3,943 × 10⁵ = 337 500 + 9 × 10¹¹ Q\n"
             "Q = 6,31 × 10⁻⁸ C",                                                                                         # 10 cm for B's distance to P
        "E₁ = {kQ}/{r} = {9 × 10⁹(15 × 10⁻⁹)}/{2 × 10⁻²} = 6 750 N·C⁻¹ to the left\nE₂ = {9 × 10⁹ Q}/{8 × 10⁻²} = 1,125 × 10¹¹ Q to the left\n"
        "E(net) = E₁ + E₂\n3,943 × 10⁵ = 6 750 + 1,125 × 10¹¹ Q\nQ = 3,44 × 10⁻⁶ C"],                                   # r not squared
        ["In which direction does each sphere's field point at P?", "The two fields add to the net field: solve for Q."]),
    mcq("7.4", "Sphere B is removed. State whether the electric field at P, due to charge on sphere A, will INCREASE, DECREASE or REMAIN THE SAME.",
        CHANGE, 1, ["Before, the field at P came from A and B; after, only from A.", "Both fields pointed to the left at P."], marks=1)]
q75 = [
    stmt("7.5.1", "State Coulomb's law in words.", 2,
         ["The electrostatic force of attraction or repulsion between two charges is directly proportional to the product of the charges and "
          "inversely proportional to the square of the distance between them."],
         ["The electrostatic force between two charges is inversely proportional to the distance between them.",
          "The electrostatic force between two charges is directly proportional to the sum of the charges.",
          "The electrostatic force between two charges is directly proportional to the product of their masses.",
          "The force between two charges is the same at every distance."],
         ["How does the force depend on the charges?", "How does it depend on the distance?"], 2),
    work("7.5.2", "Calculate the net electrostatic force experienced by point charge C due to charge A and B.", 7, [
        "F = {kQ₁Q₂}/{r²}\nF(A) = {" + K2 + "}/{(0,06)²} = 25 000 N to the right\nF(B) = {" + K2 + "}/{(0,03)²} = 100 000 N to the right\n"
        "F(net) = 25 000 + 100 000 = 125 000 N to the right",                                                          # the memo
        "F = {kQ₁Q₂}/{r²}\nF(A) = {" + K2 + "}/{(0,03)²} = 100 000 N to the right\nF(B) = {" + K2 + "}/{(0,03)²} = 100 000 N to the right\n"
        "F(net) = 100 000 + 100 000 = 200 000 N to the right",                                                         # A taken 3 cm from C
        "F = {kQ₁Q₂}/{r²}\nF(A) = {" + K2 + "}/{(0,06)²} = 25 000 N to the left\nF(B) = {" + K2 + "}/{(0,03)²} = 100 000 N to the right\n"
        "F(net) = 100 000 − 25 000 = 75 000 N to the right",                                                           # A taken to attract C
        "F = {kQ₁Q₂}/{r²}\nF(A) = {" + K2 + "}/{(6)²} = 2,5 N to the right\nF(B) = {" + K2 + "}/{(3)²} = 10 N to the right\n"
        "F(net) = 2,5 + 10 = 12,5 N to the right"],                                                                    # cm not converted
        ["How far is C from A, and from B, in metres?", "Like charges repel: which way does each force push C?"])]

# ---- QUESTION 8, the question paper page 14 and the memo page 10 ----
q8 = [
    work("8.1", "Calculate the magnetic flux through the coil at the position indicated on the diagram, where the coil is perpendicular to the "
         "field.", 4, [
        "Φ = BA cos θ\nΦ = 3,2(π × 0,04²) cos 0°\nΦ = 0,016 Wb",        # the memo
        "Φ = BA cos θ\nΦ = 3,2(π × 0,04) cos 0°\nΦ = 0,40 Wb",          # the radius not squared
        "Φ = BA cos θ\nΦ = 3,2(π × 0,04²) cos 90°\nΦ = 0 Wb",           # the angle between the field and the plane
        "Φ = NBA cos θ\nΦ = 250 × 3,2(π × 0,04²) cos 0°\nΦ = 4,02 Wb"],  # the turns put into the flux
        ["What is the area of a circle of radius 0,04 m?", "θ is the angle between the field and the normal to the coil."]),
    work("8.2", "If the coil rotates clockwise through 25°, and the emf induced is 2,8 V. Calculate the time in which this rotation took place.", 4, [
        "ε = −{NΔΦ}/{Δt}\n2,8 = −{250(0,016 cos 25° − 0,016 cos 0°)}/{Δt}\nΔt = 0,13 s",       # the memo
        "ε = −{ΔΦ}/{Δt}\n2,8 = −{0,016 cos 25° − 0,016 cos 0°}/{Δt}\nΔt = 5,35 × 10⁻⁴ s",       # the turns left out
        "ε = −{NΔΦ}/{Δt}\n2,8 = {250(0,016 cos 25°)}/{Δt}\nΔt = 1,29 s",                         # the final flux for the change
        "ε = −{NΔΦ}/{Δt}\n2,8 = −{250(0,016 sin 25° − 0,016 sin 0°)}/{Δt}\nΔt = 0,60 s"],      # sin for cos
        ["What is the change in flux as the coil turns from 0° to 25°?", "Faraday's law: ε = −NΔΦ/Δt."], after=["8.1"]),
    answer("8.3", "Which law can be used to explain the phenomenon described in QUESTION 8.2? NAME and state this law.", 3, [
        "Faraday's law: the magnitude of the induced emf across the ends of a conductor is directly proportional to the rate of change in the "
        "magnetic flux linkage with the conductor.",
        "Lenz's law: the induced current flows in a direction that opposes the change that caused it.",
        "Faraday's law: the magnitude of the induced emf is directly proportional to the magnetic flux through the conductor.",
        "Ohm's law: the potential difference across a conductor is directly proportional to the current, at constant temperature."],
        ["Which law gives the SIZE of an induced emf?", "Does the emf depend on the flux or on how fast the flux changes?"]),
    mcq("8.4.1", "If the circular coil is replaced with a square coil with a side length of 0,04 m, and the same movement is made in the same "
        "amount of time, will the induced emf be the same as, larger than or smaller than the circular coil?\nWrite down only THE SAME AS, "
        "LARGER THAN or SMALLER THAN.", ["THE SAME AS", "LARGER THAN", "SMALLER THAN"], 2,
        ["Compare the area of a square of side 0,04 m with a circle of radius 0,04 m.", "How does the flux depend on the area?"], marks=1),
    stmt("8.4.2", "Explain the answer to QUESTION 8.4.1.", 2,
         ["The area of the square (0,04² m²) is smaller than the area of the circle (π × 0,04² m²).",
          "The induced emf is directly proportional to the area of the coil."],
         ["The square has corners, which cut more field lines.", "The area of the square is larger than the area of the circle.",
          "The induced emf does not depend on the shape or area of the coil.", "The square coil has fewer turns."],
         ["Work out both areas.", "Which quantity in Φ = BA cos θ changes?"], 2, after=["8.4.1"])]

# ---- QUESTION 9, the question paper page 15 and the memo page 11 ----
Q9 = "{1}/{R(p)} = {1}/{8} + {1}/{9 + 15}\nR(p) = 6 Ω\nR(ext) = 6 + 3 = 9 Ω\n"
q9 = [
    stmt("9.1", "Define the term emf of a battery in words.", 2,
         ["The maximum energy per coulomb of charge supplied by the battery."],
         ["The energy lost per coulomb of charge inside the battery.", "The total charge the battery can store.",
          "The current the battery supplies when it is short-circuited.", "The resistance inside the battery."],
         ["The emf is measured in volts: what is a volt per coulomb?", "Is it the energy when current flows or the most the battery can "
                                                                       "give?"], 2),
    work("9.2", "Calculate the current that flows through the 3 Ω resistor.", 7, [
        Q9 + "emf = I(R + r)\n12 = I(9 + 0,6)\nI = 1,25 A",                                                               # the memo
        "{1}/{R(p)} = {1}/{8} + {1}/{9} + {1}/{15}\nR(p) = 3,30 Ω\nR(ext) = 3,30 + 3 = 6,30 Ω\nemf = I(R + r)\n12 = I(6,30 + 0,6)\nI = 1,74 A",  # 9 and 15 in parallel
        Q9 + "emf = IR\n12 = I(9)\nI = 1,33 A",                                                                          # the internal resistance ignored
        "{1}/{R(p)} = {1}/{8} + {1}/{9 + 15}\nR(p) = 6 Ω\nR(ext) = 6 + 3 + 0,6 = 9,6 Ω\nemf = I(R + r)\n12 = I(9,6 + 0,6)\nI = 1,18 A"],  # r counted twice
        ["Which resistors are in series with each other, and which branch is in parallel with the 8 Ω?", "emf = I(R + r)."]),
    work("9.3", "Determine the reading on the voltmeter.", 3, [
        "V = IR(ext)\nV = (1,25)(9)\nV = 11,25 V",       # the memo
        "V = IR\nV = (1,25)(3)\nV = 3,75 V",            # the 3 Ω only
        "V = I(R + r)\nV = (1,25)(9,6)\nV = 12 V",      # the emf
        "V = Ir\nV = (1,25)(0,6)\nV = 0,75 V"],         # the lost volts
        ["The voltmeter is across the battery: does it read the emf or the terminal potential difference?", "V = IR(ext)."], after=["9.2"]),
    mcq("9.4", "The switch, S, is now opened.\nWill the reading on the voltmeter, V, INCREASE, DECREASE or REMAIN THE SAME?", CHANGE, 0,
        ["What happens to the external resistance when the branch with S is cut off?", "How do the current and the lost volts change?"],
        marks=1),
    stmt("9.5", "Fully explain your answer to QUESTION 9.4 above.", 3,
         ["The total external resistance increases.", "The total current decreases.", "The lost volts (Ir) decrease."],
         ["The total external resistance decreases.", "The total current increases.", "The emf of the battery increases.",
          "The internal resistance decreases."],
         ["Opening S removes one branch: what happens to the total resistance?", "V = emf − Ir."], 1, after=["9.4"]),
    work("9.6", "A learner uses an electrical heater of resistance 48 Ω that operates at a potential difference of 240 V to heat her room for "
         "half an hour.\nCalculate the cost of operating the heater if the cost of electricity is R2,56 per unit. (1 unit = 1 kW·h)", 5, [
        "W = {V²Δt}/{R}\nW = {240² × (30 × 60)}/{48} = 2 160 000 J\nkW·h = {2 160 000}/{3 600 000} = 0,6 kW·h\nCost = 0,6 × R2,56 = R1,54",  # the memo's working
        "W = {V²Δt}/{R}\nW = {240² × 30}/{48} = 36 000 J\nkW·h = {36 000}/{3 600 000} = 0,01 kW·h\nCost = 0,01 × R2,56 = R0,03",         # 30 s, not 30 min
        "P = {V²}/{R}\nP = {240²}/{48} = 1 200 W\nEnergy = 1 200 × 0,5 = 600 kW·h\nCost = 600 × R2,56 = R1 536,00",                     # W not changed to kW
        "W = {V²Δt}/{R}\nW = {240² × (30 × 60)}/{48} = 2 160 000 J\nkW·h = {2 160 000}/{1 000} = 2 160 kW·h\nCost = 2 160 × R2,56 = R5 529,60"],  # ÷ 1 000 only
        ["How much energy does the heater use in half an hour?", "1 kW·h = 3 600 000 J."])]

# ---- QUESTION 10, the question paper page 16 and the memo page 12 ----
q10 = [
    stmt("10.1", "State Ohm's Law in words.", 2,
         ["The potential difference across a conductor is directly proportional to the current in the conductor at constant temperature.",
          "The ratio of potential difference to current is constant, provided the temperature remains constant."],
         ["The current in a conductor is inversely proportional to the potential difference across it.",
          "The resistance of a conductor is directly proportional to the current in it.", "The potential difference across a battery is "
                                                                                          "equal to its emf.",
          "The power of a conductor is directly proportional to the current in it."],
         ["How are V and I related for an ohmic conductor?", "Under which condition?"], 2),
    answer("10.2", "What does the gradient of the graphs represent?", 1,
           ["The inverse of resistance (1/R)", "The resistance", "The power", "The emf of the battery"],
           ["The graph plots current against potential difference.", "Gradient = ΔI ÷ ΔV: what is that in terms of R?"]),
    stmt("10.3", "Without any calculation, state which resistor, X or Y, has the greater resistance.\nGive a reason for your answer.", 2,
         ["Y", "The gradient of graph Y is smaller, so 1/R is smaller and R is greater."],
         ["X", "The gradient of graph X is smaller, so X has the greater resistance.", "Y carries more current at every potential difference.",
          "The greater the gradient, the greater the resistance."],
         ["Which graph is steeper?", "The gradient is 1/R."], 1, after=["10.2"]),
    work("10.4", "Use the graph to determine the resistance of resistor X.", 4, [
        "gradient = {ΔI}/{ΔV} = {0,4 − 0,2}/{8 − 4} = 0,05\nR(X) = {1}/{0,05}\nR(X) = 20 Ω",     # the memo
        "gradient = {ΔI}/{ΔV} = {0,4 − 0,2}/{8 − 4} = 0,05\nR(X) = gradient\nR(X) = 0,05 Ω",    # the gradient taken as R
        "gradient = {ΔI}/{ΔV} = {0,2 − 0,1}/{8 − 4} = 0,025\nR = {1}/{0,025}\nR = 40 Ω",          # graph Y read
        "gradient = {ΔI}/{ΔV} = {0,4 − 0,2}/{8 − 4} = 0,5\nR(X) = {1}/{0,5}\nR(X) = 2 Ω"],        # 0,2 ÷ 4 slipped
        ["Read two points on graph X.", "R = 1 ÷ gradient, since the graph is I against V."], after=["10.2"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Forces in equilibrium", "marks": 14,
     "lead": "A light string is suspended from the ceiling X. An object of mass 8 kg is tied to the string at O. A horizontal force of 60 N is "
             "exerted at point O, causing the string OX to experience a tension T as shown in the diagram below. The system is in equilibrium.",
     "figure": P.fig("Q2", "String OX hangs from the ceiling at X at an angle θ to a dashed vertical; at O an 8 kg mass hangs straight down "
                           "and a 60 N force pulls horizontally to the right; the tension T acts along OX."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Friction", "marks": 12,
     "lead": "A light inelastic string connects two blocks A and B of mass 2 kg and 1,5 kg respectively.\nA 8,26 N force is applied at an angle "
             "of 20° on block A to keep the blocks moving at a CONSTANT VELOCITY across a rough surface to the right, as shown in the diagram "
             "below.\nThe coefficient of kinetic friction between block A and the rough surface is 0,33.\n\nCalculate the:",
     "figure": P.fig("Q3", "Block B (1,5 kg) on the left joined by a string to block A (2 kg) on the right; a force F = 8,26 N pulls A at "
                           "20° above the horizontal."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Newton's laws", "marks": 12,
     "lead": "A hovering rescuer helicopter has a container of supplies with a weight of 1 960 N, hanging from a cable. The tension in the cable "
             "is 2 100 N. The effect of air friction cannot be ignored.",
     "figure": P.fig("Q4", "A helicopter hovering with a container hanging below it on a cable."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Newton's second law", "marks": 7,
     "lead": "The diagram below shows a 3 kg block connected to a 1 kg block with a light inextensible string. A constant horizontal force of "
             "20 N pulls the system along a rough horizontal surface.\nThe frictional force between blocks P and Q and the surface is 2 N and "
             "1 N respectively.",
     "figure": P.fig("Q5", "Block P (3 kg) and block Q (1 kg) joined by a string on a surface drawn at 30°, a 20 N force pulling P up and "
                           "along it."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Gravitation", "marks": 12,
     "lead": "Two satellites orbiting the earth are situated on opposite sides of the earth. Satellite A has a mass of 4 600 kg and Satellite B "
             "has a mass of 5 300 kg. Satellite A is at a height of 28 000 km above the surface of the earth.",
     "figure": P.fig("Q6", "Satellite A on the left and satellite B on the right of the earth."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Electric fields", "marks": 14,
     "lead": "Two identical metal spheres, A and B, on insulated stands are placed with their centres 10 cm apart. Sphere A has a charge of "
             "−15 nC while sphere B carries an unknown positive charge. P is a point 2 cm away from the centre of A, as shown in the diagram "
             "below.\nThe NET electric field at point P is 3,943 × 10⁵ N·C⁻¹ to the left.",
     "figure": P.fig("Q7", "Sphere A on the left and sphere B on the right, on stands; P lies between them, 2 cm from A and 8 cm from B."),
     "items": q7},
    {"id": "7.5", "title": "Question 7.5", "kind": "Coulomb's law", "marks": 9,
     "lead": "Three +100 μC point charges, A, B and C, are equally spaced on a straight line in a vacuum. The charges are a distance of 3 cm "
             "from each other as shown in the diagram below.",
     "figure": P.fig("Q7.5", "Charges A, B and C, each +100 μC, in a line from left to right, 3 cm apart."), "items": q75},
    {"id": "8", "title": "Question 8", "kind": "Electromagnetism", "marks": 14,
     "lead": "A circular coil with 250 windings (turns) and a radius of 0,04 m, is rotated clockwise inside a magnetic field with a field "
             "strength of 3,2 T.",
     "figure": P.fig("Q8", "A circular coil between the N pole on the left and the S pole on the right, the field lines running from N to "
                           "S through the coil; an arrow marks its rotation."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Electric circuits", "marks": 21,
     "lead": "The battery used in the circuit below has emf of 12 V and internal resistance of 0,6 Ω.\nThe resistance of the connecting wires "
             "can be ignored.",
     "figure": P.fig("Q9", "A battery (internal resistance 0,6 Ω) with a voltmeter across it, in series with a 3 Ω resistor and an 8 Ω "
                           "resistor; across the 8 Ω, a branch of 15 Ω and 9 Ω in series with the switch S."), "items": q9},
    {"id": "10", "title": "Question 10", "kind": "Ohm's law", "marks": 9,
     "lead": "A learner sets up the circuit as shown below to investigate the relationship between potential difference and current for each "
             "of two unknown resistors X and Y. In experiment 1 she connected resistor X and recorded the ammeter and voltmeter readings. She "
             "then repeated the procedure in Experiment 2 with resistor Y. Ignore internal resistance of the battery.\nThe results of the two "
             "experiments are shown on graphs below.",
     "figure": P.fig("Q10b", "Current (A) against potential difference (V): two straight lines from the origin, X steeper (0,4 A at 8 V) and "
                             "Y less steep (0,3 A at 12 V)."), "items": q10},
]
P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2024", "total_marks": 144, "time": "3 hours"},
         [P.flag_workings(),
          P.flag_answers("8.3 ('NAME and state this law') plays as named statements of a law."),
          {"n": "paper", "kind": "no_fit", "detail": "Played out of 144: 5.3 (6 marks) is left out. The paper's words say the blocks move on a "
                                                     "horizontal surface; its diagram draws a 30° slope; the memo works on the slope but puts "
                                                     "2 kg for the 3 kg block, and its answer 2,15 m·s⁻² follows from neither (on the slope "
                                                     "a = −0,65 m·s⁻², on a horizontal surface 4,25 m·s⁻²). No reading gives one right "
                                                     "answer. The cover's 150 marks are printed."},
          {"n": "1.4", "kind": "memo_issue", "detail": "The memo gives C (resultant force and acceleration to the left). A block sliding left on a "
                                                       "rough surface with no other force has friction, and so the resultant force and the "
                                                       "acceleration, to the right: B. The right letter is B."},
          {"n": "1.5", "kind": "memo_issue", "detail": "The memo gives C (continue at constant velocity for a short time). With the push removed, "
                                                       "friction is the only horizontal force, so the crate slows down at once: B. The right "
                                                       "letter is B."},
          {"n": "3.2.2", "kind": "memo_issue", "detail": "The memo's working gives 2,22 = μk(1,5 × 9,8), which is μk = 0,15; it writes 0,25. "
                                                         "The right option ends in 0,15; 0,25 is in no option."},
          {"n": "9.6", "kind": "memo_issue", "detail": "The memo's working gives 2 160 000 J = 0,6 kW·h, which costs 0,6 × R2,56 = R1,54; it "
                                                       "writes R0,882. The right option ends in R1,54; R0,882 is in no option."},
          {"n": "8.2", "kind": "memo_issue", "detail": "The memo's line reads 28 = …; the stem's emf is 2,8 V, which its answer 0,13 s uses. The "
                                                       "memo also accepts 0,17 s (with Φ = 0,02 Wb): no wrong option is 0,17 s."},
          {"n": "7.4", "kind": "low_confidence", "detail": "The stem asks about 'the electric field at P, due to charge on sphere A' once B is "
                                                           "removed: A's own field does not change, but the field at P (now A's alone) is less "
                                                           "than the net field before. The memo gives DECREASE; the right choice is the memo's."},
          {"n": "2.2", "kind": "no_fit", "detail": "Every drawing plays as pick the drawing (2.2 the closed vector diagram, 5.2 the free-body "
                                                   "diagram, 7.2 the field pattern): the memo's and three mistakes it marks down."}],
         {"1": 20, "2": 14, "3": 12, "4": 12, "5": 7, "6": 12, "7": 23, "8": 14, "9": 21, "10": 9}, 144,
         {"2.3.2": ["2.3.1"], "3.2.2": ["3.2.1"], "4.4": ["4.3"], "8.2": ["8.1"], "8.4.2": ["8.4.1"], "9.3": ["9.2"], "9.5": ["9.4"],
          "10.3": ["10.2"], "10.4": ["10.2"]},
         "Questions 1 to 10, without 5.3")
