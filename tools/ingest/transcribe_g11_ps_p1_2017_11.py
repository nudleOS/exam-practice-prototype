"""Grade 11 Physical Sciences P1 (Physics) Nov 2017 (DBE common paper), the whole paper (Questions 1 to 10), hand-transcribed into the
catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options,
marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API
call: the transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets its vector diagrams,
ray paths, graphs and circuits as drawings, and the memo sets its fractions and formulas as images, so the text layers have gaps.

  python tools/ingest/transcribe_g11_ps_p1_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Physical Sciences P1 Nov 2017 Eng.pdf" "uploads/Grade 11 Physical Sciences P1 Nov 2017 MG Eng & Afr.pdf" --id g11-ps-p1-2017-11 --from-json

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; models: transcribe_ps_p1_2025_11.py and the same grade's other year,
transcribe_g11_ps_p1_2018_11.py):
  multiple choice printed in the paper -> mcq as printed (1.2's four vector diagrams: the figure and "Diagram A".."Diagram D"); a choice
  printed in the stem with no explanation in the same part (7.3, 7.5 and 10.1.5 "INCREASE, DECREASE or REMAIN THE SAME", 8.2 "NEGATIVE or
  POSITIVE") -> mcq of the printed choices. One term the memo names -> term (3.2.1, 3.2.2). A one-value answer with no working -> num
  (2.2's 0 N, 2.4's 200 N). 6.5.1 (a range of angles, no working) -> an answer multiple choice of realistic wrong ranges.
  Every calculation ("Calculate", "Determine" with a working) -> authored multiple choice, `work`: the memo's FIRST working line by line
  and three workings each built from a DIFFERENT realistic error (a sign or direction slip, a value from the wrong body, part or row, a
  formula upside down or with a factor dropped, a power of ten slipped, a unit not converted, the wrong constant, the calculator in
  radians), every number recomputed; 0 or full marks. 4.6's value with its direction mark plays its working, then the value with its
  direction. A value the memo also accepts (its OR answers, "accept any set of coordinates", rounding of its own intermediate values)
  is never a wrong option.
  A definition, law, hypothesis, investigative question or relationship -> statements (pick 1 card for its marks; an OR form a second
  right card); 4.2 (NAME AND STATE, 1 + 2) one card that names the law and states it, 3 marks; an explanation the memo ticks point by
  point -> statements, 1 mark a point; a choice with its reason in the same part (8.5) -> the choice a card beside its reason. No memo
  here weighs two sides, so no part plays as a sort.
  "Draw" (a free-body diagram, the graph on the ANSWER SHEET, a sketch graph, a field pattern) -> draw with the memo's criteria
  (self-checked, flagged no_fit).
  A part whose options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with its
  stem and diagram; a sentence the paper adds part-way (4.5 "Suddenly the tow bar ...", 6.4, 6.5, 10.1.5 "The switch ... is now OPENED")
  leads the parts it belongs to; 10.2 (a geyser, a new situation) is a mission of its own. Question 9's graph sits under its own
  sentence, below the coil diagram: the coil is the mission's figure and the graph is 9.2's.
Figure boxes are measured in PDF points (page 595.44 x 841.68, read from the PDF) from the ink of the drawings, images and labels
themselves, so that ingest.py's 1% padding reaches no body text, and checked on a contact sheet (scratchpad
lower/g11-ps-p1-2017-11/figs.py)."""
import json
import random
import re
from pathlib import Path

PID = "g11-ps-p1-2017-11"
W, H = 595.44, 841.68
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.2": [3, 101.5, 365.0, 483.5, 571.5], "1.3": [4, 176.0, 131.5, 399.5, 191.5], "1.6": [5, 243.0, 125.5, 349.5, 236.5],
    "1.8": [6, 196.5, 126.0, 383.0, 186.5], "1.10": [7, 140.5, 140.0, 405.5, 375.5], "Q2": [8, 168.0, 187.5, 448.0, 293.5],
    "Q3": [9, 153.0, 180.5, 533.5, 249.5], "Q4": [10, 117.0, 192.0, 477.0, 282.0], "Q6": [11, 170.5, 401.0, 441.0, 545.0],
    "Q7": [12, 168.0, 320.0, 382.0, 556.5], "Q8": [13, 168.5, 165.0, 469.0, 199.5], "Q9a": [14, 194.5, 161.0, 402.0, 271.0],
    "Q9b": [14, 178.0, 304.5, 404.5, 547.0], "Q10": [15, 162.0, 186.0, 397.5, 329.5]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points (key words, criteria, "... 2 or 0"): never scored, never shown
# kw: catalogue extras the played part keeps (after=[...] when its cards show an earlier part's answer)
rub = lambda n, q, marks, bullets, clues, each=None, notes=None, **kw: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues,
                                                                       "bullets": bullets, **({"each": each} if each else {}),
                                                                       **({"notes": notes} if notes else {}), **kw}
term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="", **kw: {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                           "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {}), **kw}

WORK = "\n\nChoose the correct working."
AUTHORED = []   # the calculations played as authored multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues, **kw):
    """A calculation as authored multiple choice (Murci, 2026-10-10): opts are the memo's FIRST working and three workings built
    from realistic physics errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing.
    kw: catalogue extras, e.g. after=[...] when the options show an earlier part's answer, figure=... for a part's own figure."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


# ---- QUESTION 1: multiple choice, the question paper pages 3-7 and the memo page 2 ----
MC_LEAD = "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer."
q1 = [
    mcq("1.1", "Which ONE of the following pairs of physical quantities is vector quantities?",
        ["Force and distance", "Velocity and speed", "Charge and electric field", "Electric field and force"], 3,
        ["What is the difference between a vector quantity and a scalar quantity?",
         "In each pair, do BOTH quantities need a direction to be described fully?"]),
    mcq("1.2", "Which ONE of the following vector diagrams represents three forces acting on an object simultaneously while the object moves at "
        "CONSTANT VELOCITY?", ["Diagram A", "Diagram B", "Diagram C", "Diagram D"], 0,
        ["What is the net force on an object that moves at a constant velocity?",
         "How do you add vectors with the head-to-tail method, and what does the sum look like when it is zero?"],
        figure=fig("1.2", "Four vector diagrams, A to D, each a right-angled triangle of three arrows. A: an arrow down the vertical side on the "
                   "left, an arrow to the right along the bottom, and an arrow along the slanted side pointing up to the top left. B: an arrow "
                   "along the slanted side pointing up to the top right, an arrow down the vertical side on the right, and an arrow to the "
                   "right along the bottom. C: an arrow up the vertical side on the left, an arrow along the slanted side pointing down to the "
                   "bottom right, and an arrow to the right along the bottom. D: an arrow to the right along the bottom, an arrow up the "
                   "vertical side on the right, and an arrow along the slanted side pointing up to the top right.")),
    mcq("1.3", "A block with a mass of 4 kg is pulled upwards along a frictionless slope, inclined at an angle θ, with a force F, as shown in the "
        "sketch below.\n\nWhich ONE of the following equations can be used to calculate the magnitude of the normal force (N)?",
        ["N = (4)(9,8)sin θ", "N = F − (4)(9,8)cos θ", "N = F + (4)(9,8)cos θ", "N = (4)(9,8)cos θ"], 3,
        ["Which forces, or components of forces, act perpendicular to the slope?",
         "In which direction does F act compared with the surface of the slope?"],
        figure=fig("1.3", "A 4 kg block on a slope inclined at θ to the horizontal, pulled up the slope by a force F drawn along the slope.")),
    mcq("1.4", "A satellite orbits Earth at a height where the gravitational force is a quarter (¼) of the force it experiences on the surface of "
        "the Earth. If the radius of Earth is R, the height of the satellite ABOVE THE SURFACE of Earth is …", ["4R", "2R", "R", "½R"], 2,
        ["How does the gravitational force depend on the distance from the centre of the Earth?",
         "Is the height above the surface the same as the distance from the centre of the Earth?"]),
    mcq("1.5", "A light ray passes from glass to air. The angle of incidence is 35°. The critical angle of glass is 38°.\n\nThe light ray will "
        "undergo …", ["diffraction.", "refraction and bend away from the normal.", "total internal reflection.",
                       "refraction and bend towards the normal."], 1,
        ["Is the angle of incidence larger or smaller than the critical angle?",
         "What happens to the speed of light when it passes into an optically less dense medium?"]),
    mcq("1.6", "The path of a light ray passing from air through a rectangular Perspex block is shown below.\n\nThe magnitude of angle θ will be …",
        ["less than 39°.", "equal to 39°.", "equal to 51°.", "equal to 90°."], 2,
        ["Is the 39° measured from the normal or from the surface of the block, and what is the angle of incidence?",
         "How does the direction of the ray that leaves a rectangular block compare with the direction of the ray that enters it?"],
        figure=fig("1.6", "A light ray in the air strikes the top face of a rectangular Perspex block, with 39° marked between the ray and the "
                   "top surface; dashed normals are drawn where the ray enters and where it leaves through the bottom face, and θ is marked "
                   "between the ray that leaves and the lower normal.")),
    mcq("1.7", "A monochromatic red light ray passes through a single slit of width d. The diffraction pattern is projected on a screen. The red "
        "light is then replaced with monochromatic blue light and passed through the same single slit.\n\nThe degree of diffraction will …",
        ["increase because the degree of diffraction is directly proportional to wavelength.",
         "decrease because blue light has a shorter wavelength than red light.",
         "increase because blue light has a longer wavelength than red light.",
         "decrease because the degree of diffraction is inversely proportional to wavelength."], 1,
        ["Which has the longer wavelength: red light or blue light?", "How does the degree of diffraction depend on the wavelength?"]),
    mcq("1.8", "A negative charge of 1 µC, which is free to move, is placed at a distance 2r from a positive charge of 4 µC.\n\nWhich ONE of the "
        "following statements regarding the −1 µC charge, when it is at distance r, is CORRECT?\n\nThe electrostatic force experienced by the "
        "−1 µC charge will …", ["remain the same.", "be halved.", "be doubled.", "increase four times."], 3,
        ["How does the electrostatic force between two charges depend on the distance between them?",
         "By what factor does the distance change when the charge moves from 2r to r?"],
        figure=fig("1.8", "Charge +4 µC on the left and charge −1 µC on the right on a dashed line; a tick halfway along is labelled r, and the "
                   "position of the −1 µC charge is labelled 2r.")),
    mcq("1.9", "A circular coil is placed inside a magnetic field and rotated clockwise to induce an emf. Which ONE of the following changes will "
        "increase the induced emf?", ["Rotating the coil slower", "Decreasing the number of turns/windings of the coil",
                                       "Increasing the speed of rotation of the coil", "Changing the polarity of the magnets"], 2,
        ["Which quantities in Faraday's law make the induced emf larger?",
         "How does the time the flux takes to change depend on how the coil is turned?"]),
    mcq("1.10", "In the circuit diagram below, the battery has negligible internal resistance. The resistance of the ammeter and wires may also be "
        "ignored.\n\nThe reading on voltmeter V₃ will be equal to …", ["V₁", "½ V₁", "V₁ + V₂", "V₂ − V₁"], 1,
        ["Which branch is in parallel with the 4 Ω resistor, and what potential difference does that branch share with it?",
         "How does the potential difference split between two equal resistors in series?"],
        figure=fig("1.10", "A battery in series with an ammeter A. The current then splits into two branches: one is a 4 Ω resistor with "
                   "voltmeter V₁ across it; the other is an 8 Ω resistor with voltmeter V₂ across it, in series with a second 8 Ω resistor "
                   "with voltmeter V₃ across it.")),
]

# ---- QUESTION 2, the question paper page 8 and the memo page 3 ----
q2 = [
    rub("2.1", "Define the term resultant vector.", 2, [
        "The vector sum of two or more vectors. (2)", "OR — The single vector which has the same effect as two or more vectors together. (2)"],
        ["Does a resultant replace the vectors it comes from, or add to them?", "How is a resultant different from a component?"], each=2),
    num("2.2", "What is the magnitude of the resultant force acting on block B?", 0, 0, "N",
        ["Block B is stationary: what does that tell you about the forces acting on it?",
         "Which of Newton's laws describes an object that stays at rest?"]),
    draw("2.3", "Draw a labelled free-body diagram indicating all the forces acting on block B.", 3, [
        ["Weight (w / Fg) drawn and labelled", 1], ["Tension in cable C (FC / TC) drawn and labelled", 1],
        ["Tension in rope R (FR / TR) drawn and labelled", 1]],
        ["Which ropes or cables are attached to block B?", "Which force acts on block B even though nothing touches it?"],
        memo="The memo's diagram: w straight down, FC up and to the left along the cable, FR up and to the right along the rope, all from one "
             "point. Any additional force: deduct 1 mark (maximum 2/3). Lines must touch the object (otherwise maximum 2/3)."),
    num("2.4", "Determine the horizontal component of the force in rope R.", 200, 0, "N",
        ["Which horizontal forces act on block A?", "Block A does not move: what is the net horizontal force on it?"]),
    work("2.5", "Calculate the vertical component of the force in cable C.", 4, [
        "FRY = 200 tan 35° = 140,04 N\nFg = mg = 56(9,8) = 548,8 N\nFRY + FCY = Fg: 140,04 + FCY = 548,8\nFCY = 408,76 N",       # tan upside down
        "FRY = {200}/{tan 35°} = 285,63 N\nFg = mg = 56(9,8) = 548,8 N\nFCY = Fg + FRY: FCY = 548,8 + 285,63\nFCY = 834,43 N",  # the rope taken as
        # pulling down (a direction slip)
        "FRY = {200}/{tan 35°} = 285,63 N\nFg = mg = 56(9,8) = 548,8 N\nFRY + FCY = Fg: 285,63 + FCY = 548,8\nFCY = 263,17 N",  # the memo
        "FRY = {200}/{tan 35°} = 285,63 N\nFg = mg = 56(10) = 560 N\nFRY + FCY = Fg: 285,63 + FCY = 560\nFCY = 274,37 N"], 2,  # g taken as 10
        ["The rope makes 35° with the vertical: which trigonometric ratio links its horizontal and vertical components?",
         "Block B is at rest: which upward forces must balance its weight?"],
        after=["2.3", "2.4"]),   # the options show the forces on B (2.3's free-body diagram) and 2.4's 200 N
    work("2.6", "Calculate the angle θ between the cable and the ceiling.", 2, [
        "tan θ = {263,17}/{200}\nθ = 52,77°",                                            # the memo
        "tan θ = {200}/{263,17}\nθ = 37,23°",                                            # the ratio upside down
        "tan θ = {285,63}/{200}\nθ = 55,00°",                                            # the rope's vertical component (the wrong rope)
        "tan θ = {263,17}/{200}\nθ = 0,92°"], 0,                                         # the calculator in radians
        ["What is the horizontal component of the force in cable C, given that block B is at rest?",
         "Which trigonometric ratio links the vertical and horizontal components to the angle with the ceiling?"],
        after=["2.4", "2.5"]),   # the options show 2.4's 200 N and 2.5's 263,17 N
]

# ---- QUESTION 3, the question paper page 9 (ANSWER SHEET page 18) and the memo pages 4-5 and 14 ----
q3 = [
    rub("3.1", "Write down a hypothesis for this experiment.", 2, [
        "The (net) force is directly proportional to acceleration if the mass of the trolley is kept constant. (2)"],
        ["Which variable did the learners change, and which did they measure?",
         "A hypothesis is a prediction: what relationship do you expect between the two variables?"], each=2,
        notes=["Criteria: the dependent (acceleration) and independent ((net) force) variables stated correctly (1); the relationship between "
               "them stated (1)."]),
    term("3.2.1", "Identify the independent variable.", ["(Net) force", "Net force", "Force", "Resultant force"],
         ["Which quantity did the learners set by hanging different masses on the string?",
          "Is the independent variable the cause or the effect?"]),
    term("3.2.2", "Identify the controlled variable.", ["Mass of trolley", "Mass of the trolley", "The mass of the trolley", "Trolley mass",
                                                         "Trolley's mass"],
         ["Which quantity, other than the two in the table, could change the acceleration?",
          "Is a controlled variable changed, measured, or kept the same?"]),
    draw("3.3", "Use the graph paper on the ANSWER SHEET and draw a graph of the acceleration versus net force.", 4, [
        ["Axes with a correct, appropriate scale", 1], ["3 or more coordinates correctly plotted", 2], ["A line of best fit drawn", 1]],
        ["Which quantity goes on the vertical axis of a graph of acceleration versus net force?",
         "What scale lets the largest values in the table fit on the grid?"],
        memo="The memo's graph drawn to scale (memo page 14): a (m·s⁻²), 0 to 1,5, up, against F (N), 0 to 1,2, across; the four points of the "
             "table plotted and a straight line of best fit drawn from the origin."),
    work("3.4", "Calculate the gradient of the graph.", 3, [
        "gradient = {1,2 − 0,3}/{1,45 − 0,36}\ngradient = 0,83",                         # upside down (Δx over Δy)
        "gradient = {1,45 − 0,36}/{0,3 − 1,2}\ngradient = −1,21",                        # the points subtracted in opposite orders (a sign slip)
        "gradient = {1,45 − 0,73}/{1,2 − 0,3}\ngradient = 0,80",                         # an acceleration from the wrong row
        "gradient = {1,45 − 0,36}/{1,2 − 0,3}\ngradient = 1,21"], 3,                     # the memo (it accepts any set of coordinates)
        ["Which two points on your line are far apart and easy to read?", "Which quantity is on the vertical axis, and which on the horizontal axis?"],
        after=["3.3"]),   # the options show the line's points and one gradient for all of it (3.3's straight line)
    work("3.5", "Use the gradient of the graph calculated in QUESTION 3.4 to determine the mass of the trolley.", 2, [
        "Gradient = {a}/{F} = m\nm = 1,21 kg",                                           # the gradient taken as the mass
        "Gradient = {a}/{F} = {1}/{m}\nm = {1}/{1,21} = 0,83 kg",                        # the memo
        "Gradient = {a}/{F} = {1}/{mg}\nm = {1}/{(1,21)(9,8)} = 0,08 kg",                # the weight for the mass (g brought in)
        "Gradient = {a}/{F} = {1}/{m}\nm = {1}/{1,45} = 0,69 kg"], 1,                    # an acceleration from the table for the gradient
        ["Rearrange Fnet = ma to make a the subject: what multiplies F?",
         "How is the gradient of an acceleration versus force graph related to the mass?"],
        after=["3.4"]),   # the options show 3.4's 1,21
]

# ---- QUESTION 4, the question paper page 10 and the memo pages 6-7 ----
MU = "If the coefficient of kinetic friction between the tow-truck tyres and the road surface is 0,45, calculate the "
LOOSE = "Suddenly the tow bar between the car and the tow truck disconnects and the car comes loose.\n\n"
q4 = [
    rub("4.1", "Define the term frictional force.", 2, [
        "Frictional force is the force that opposes the motion of an object and which acts parallel to the surface. (2)"],
        ["What happens to a moving object if friction is the only horizontal force on it?",
         "How is the frictional force different from the normal force that the same surface exerts?"], each=2),
    rub("4.2", "NAME AND STATE the law that explains why the force exerted by the tow truck on the car is the same as the force exerted by the "
        "car on the tow truck.", 3, [
        "Newton's Third law (1): When object A exerts a force on object B, object B simultaneously exerts an oppositely directed force of "
        "equal magnitude on object A. (2)"],
        ["Which two objects exert these forces, and on which object does each force act?",
         "How do the sizes and the directions of the two forces compare?"], each=3),
    draw("4.3", "Draw a labelled free-body diagram indicating all the forces acting on the tow truck.", 5, [
        ["Weight (w / Fg / 12 740 N) drawn and labelled", 1], ["Tension (T / FT) drawn and labelled", 1], ["Friction (f / Ff) drawn and labelled", 1],
        ["Normal force (N / FN / 12 740 N) drawn and labelled", 1], ["Applied force (FA / Fapplied / Fengine / F) drawn and labelled", 1]],
        ["Which bodies touch or pull on the tow truck?", "Which forces act vertically, and which horizontally?"],
        memo="The memo's diagram: N up, w down, FA to the left, f and T to the right, all from one point. Any additional force: deduct 1 mark "
             "(maximum 4/5). Lines must touch the object (otherwise maximum 4/5)."),
    work("4.4.1", MU + "magnitude of the tension in the tow bar.", 5, [
        "Fnet = ma\nFengine − f − T = 0\n9 000 − 0,45(1 300)(9,8) − T = 0\nT = 3 267 N",       # the memo
        "Fnet = ma\nFengine − f − T = 0\n9 000 − 0,45(950)(9,8) − T = 0\nT = 4 810,5 N",       # the car's mass for the truck's (the wrong body)
        "Fnet = ma\nFengine − f − T = 0\n9 000 − 0,45(1 300) − T = 0\nT = 8 415 N",            # the mass taken as the normal force (g left out)
        "Fnet = ma\nFengine + f − T = 0\n9 000 + 0,45(1 300)(9,8) − T = 0\nT = 14 733 N"], 0,  # friction taken as forward (a direction slip)
        ["The vehicles move at constant velocity: what is the net force on the tow truck?",
         "Which forces act on the tow truck horizontally, and in which directions?"],
        after=["4.3"]),   # the options show the horizontal forces on the tow truck (4.3's free-body diagram)
    work("4.4.2", MU + "coefficient of kinetic friction between the CAR tyres and the road surface.", 5, [
        "Fnet = ma: T − f = 0\n3 267 − f = 0, so f = 3 267 N\nfk = µkN = µkmg\n3 267 = µk(1 300)(9,8)\nµk = 0,26",       # the truck's mass
        "Fnet = ma: Fengine − f = 0\n9 000 − f = 0, so f = 9 000 N\nfk = µkN = µkmg\n9 000 = µk(950)(9,8)\nµk = 0,97",    # the engine force
        # for the pull on the car (a force on the wrong body)
        "Fnet = ma: T − f = 0\n3 267 − f = 0, so f = 3 267 N\nfk = µkN = µkmg\n3 267 = µk(950)(9,8)\nµk = 0,35",         # the memo
        "Fnet = ma: T − f = 0\n3 267 − f = 0, so f = 3 267 N\nfk = {N}/{µk} = {mg}/{µk}\n3 267 = {(950)(9,8)}/{µk}\nµk = 2,85"], 2,  # upside down
        ["Which horizontal forces act on the car, and how do they compare when it moves at constant velocity?",
         "Which equation links the kinetic friction, the coefficient and the normal force?"],
        after=["4.4.1"]),   # the options show 4.4.1's 3 267 N
    rub("4.5", LOOSE + "Using a relevant law of motion, explain why the car continues moving forward for a short distance.", 3, [
        "According to Newton's first law, (1)", "an object will continue moving at a constant velocity unless a non-zero net force acts on it. (1)",
        "The net force acting on the car now is the frictional force and it causes the car to slow down. (1)"],
        ["What force still acts on the car once the tow bar no longer pulls it?",
         "What happens to the velocity of an object when no net force acts on it?"]),
    work("4.6", LOOSE + "Calculate the acceleration of the car as it comes to a stop after a short distance.", 3, [
        "Fnet = ma\n−3 267 = 950a\na = −3,44 m·s⁻²\na = 3,44 m·s⁻², forwards (to the left)",                  # the direction slipped
        "Fnet = ma\n−3 267 = 1 300a\na = −2,51 m·s⁻²\na = 2,51 m·s⁻², backwards (to the right)",               # the truck's mass (the wrong body)
        "Fnet = ma\n−3 267 = (1 300 + 950)a\na = −1,45 m·s⁻²\na = 1,45 m·s⁻², backwards (to the right)",       # both masses
        "Fnet = ma\n−3 267 = 950a\na = −3,44 m·s⁻²\na = 3,44 m·s⁻², backwards (to the right)"], 3,             # the memo
        ["Which force acts on the car once it comes loose, and in which direction?",
         "Which equation links the net force, the mass and the acceleration?"],
        after=["4.4.1", "4.4.2"]),   # the options show the friction on the car, 3 267 N (4.4.1's tension, 4.4.2's f)
]

# ---- QUESTION 5, the question paper page 11 and the memo page 7 ----
q5 = [
    rub("5.1", "Explain the difference between weight and mass.", 2, [
        "Weight is the gravitational force exerted on an object by the earth. (1)", "Mass is the amount of matter in a body. (1)"],
        ["Which of the two is measured in kilograms, and which in newtons?", "Which of the two changes when an object is taken to another planet?"]),
    work("5.2", "Calculate the mass of planet X.", 4, [
        "g = {GM}/{r²}\n2,7 = {(6,67 × 10⁻¹¹)M}/{(6,38 × 10⁶)²}\nM = 1,65 × 10²⁴ kg",          # the Earth's radius (not divided by 3)
        "g = {GM}/{r²}\n2,7 = {(6,67 × 10⁻¹¹)M}/{(⅓ × 6,38 × 10⁶)²}\nM = 1,83 × 10²³ kg",     # the memo
        "g = {GM}/{r²}\n2,7 = {(6,67 × 10⁻¹¹)M}/{⅓ × 6,38 × 10⁶}\nM = 8,61 × 10¹⁶ kg",         # r not squared
        "g = {GM}/{r²}\n9,8 = {(6,67 × 10⁻¹¹)M}/{(⅓ × 6,38 × 10⁶)²}\nM = 6,65 × 10²³ kg"], 1,  # the Earth's g (the wrong planet)
        ["Which equation links g at a planet's surface to its mass and radius?", "What is the radius of planet X in metres?"]),
    work("5.3", "Determine the factor by which the weight of an object on planet X will differ from the weight of the same object on Earth.", 2, [
        "{9,8}/{2,7}\n= 3,63 times greater on planet X than on Earth",                    # the direction turned round
        "({R}/{⅓R})² = 3²\n= 9 times greater on planet X than on Earth",                  # the radius alone (the mass left out)
        "{9,8}/{2,7}\n= 3,63 times smaller on planet X than on Earth",                    # the memo
        "{10}/{2,7}\n= 3,70 times smaller on planet X than on Earth"], 2,                 # g taken as 10, not the data sheet's 9,8
        ["Does the mass of the object change when it moves from Earth to planet X?", "How does the weight of an object depend on g?"]),
]

# ---- QUESTION 6, the question paper pages 11-12 and the memo page 8 ----
NEWB = "If material A is replaced by material B, the angle of refraction is 31° when the angle of incidence is 40°. "
TIR = "Total internal reflection occurs when a light ray passes from material A to material B. The critical angle of material A is 49°. "
q6 = [
    rub("6.1", "Define the term angle of incidence.", 2, ["Angle of incidence is the angle between the normal to a reflecting surface and incident ray. (2)"],
        ["Is the angle of incidence measured from the surface, or from another line?",
         "How is the angle of incidence different from the angle of refraction?"], each=2),
    work("6.2", "Calculate the refractive index of material A using the data in the graph.", 3, [
        "gradient = {0,37 − 0}/{0,56 − 0} = 0,66\ngradient = {sin θr}/{sin θi} = {ni}/{nr} = {1}/{nr}\nnr = {1}/{0,66} = 1,51",   # the memo (OPTION 1)
        "gradient = {0,37 − 0}/{0,56 − 0} = 0,66\ngradient = {sin θr}/{sin θi} = {nr}/{ni} = nr\nnr = 0,66",                    # Snell's law upside down
        "gradient = {0,37 − 0}/{0,56 − 0} = 0,7\ngradient = {sin θr}/{sin θi} = {ni}/{nr} = {1}/{nr}\nnr = {1}/{0,7} = 1,43",     # rounded too early
        "θi = sin⁻¹ 0,56 = 34,06° and θr = sin⁻¹ 0,37 = 21,72°\nni θi = nr θr\nnr = {34,06}/{21,72} = 1,57"], 0,               # the sines cancelled
        # (1/0,66 = 1,52 (flagged); the memo's OPTION 2, 1(0,56) = nr(0,37), gives 1,51: no option shows 1,52)
        ["Write Snell's law for light passing from air into material A: which sine goes with which refractive index?",
         "How is the gradient of a graph of sin θr against sin θi related to the refractive index of material A?"]),
    work("6.3", "Calculate the speed of the light through material A.", 3, [
        "n = {v}/{c}\n1,51 = {v}/{3 × 10⁸}\nv = 4,53 × 10⁸ m·s⁻¹",                         # the formula upside down
        "n = {c}/{v}\n1,51 = {340}/{v}\nv = 225,17 m·s⁻¹",                                # the speed of sound for c (the wrong constant)
        "n = {c}/{v}\n1 = {3 × 10⁸}/{v}\nv = 3 × 10⁸ m·s⁻¹",                              # air's index (the wrong medium)
        "n = {c}/{v}\n1,51 = {3 × 10⁸}/{v}\nv = 1,99 × 10⁸ m·s⁻¹"], 3,                     # the memo (from 1,52: 1,97 x 10⁸, never an option)
        ["Which equation links a refractive index to the speed of light in the medium?", "Which value does the data sheet give for the speed of light in a vacuum?"],
        after=["6.2"]),   # the options show 6.2's 1,51
    work("6.4.1", NEWB + "Calculate the refractive index of material B.", 4, [
        "ni sin θi = nr sin θr\n1 sin 31° = nr sin 40°\nnr = 0,80",                       # the two angles swapped
        "ni sin θi = nr sin θr\n1 sin 40° = nr sin 31°\nnr = 1,25",                       # the memo
        "ni sin θi = nr sin θr\n1 × 40° = nr × 31°\nnr = 1,29",                           # the sines cancelled
        "ni sin θi = nr sin θr\n1 sin 40° = nr sin 31°\nnr = −1,84"], 1,                  # the calculator in radians
        ["Which medium does the light come from, and what is its refractive index?", "Which angle goes with which refractive index in Snell's law?"]),
    draw("6.4.2", NEWB + "Redraw the graph of material A, and on the same set of axis, draw the graph you expect for material B. Label the graphs of "
         "material A and material B clearly.", 2, [["The gradient of B is bigger than the gradient of A", 2]],
         ["How is the gradient of a graph of sin θr against sin θi related to the refractive index?",
          "Which material has the larger refractive index, A or B?"],
         memo="The memo's sketch: sin θr up against sin θi across, two straight lines from the origin labelled A and B, B the steeper.",
         after=["6.4.1"]),   # its criterion (B steeper) shows which index 6.4.1 makes the smaller
    mcq("6.5.1", TIR + "Which range of angles will make it possible for total internal reflection to occur?",
        ["Angles of incidence between 49° and 90°", "Angles of incidence between 0° and 49°", "Angles of incidence between 41° and 90°",
         "An angle of incidence of exactly 49° only"], 0,
        # the memo: between 49° and 90° (OR 49° < θ < 90°), no working. The wrong ranges: below the critical angle, the critical angle's
        # complement (90° − 49°), the critical angle itself
        ["What happens to the refracted ray when the angle of incidence equals the critical angle?",
         "What is the largest angle of incidence a ray can have at a boundary?"]),
    rub("6.5.2", TIR + "What OTHER condition is necessary for total internal reflection to take place?", 2, [
        "Light must travel from optically denser medium (higher refractive index) to an optically less dense medium (lower refractive index). (2)"],
        ["Can total internal reflection happen when light passes from air into glass?",
         "How do the refractive indices of materials A and B compare?"], each=2),
]

# ---- QUESTION 7, the question paper page 12 and the memo page 9 ----
CHOOSE = " Choose from INCREASE, DECREASE or REMAIN THE SAME."
q7 = [
    rub("7.1", "Write down an investigative question for this experiment.", 2, [
        "What is the relationship between slit width and degree of diffraction? (2)",
        "OR — How does the width of the central bright band change as the slit width changes? (2)"],
        ["Which variable is changed in this experiment, and which is measured?",
         "How do you ask about the link between them so that the answer cannot be YES or NO?"], each=2,
        notes=["Criteria: the dependent (degree of diffraction) and independent (slit width) variables stated correctly (1); the relationship "
               "between them asked (1)."]),
    rub("7.2", "State Huygens' principle in words.", 2, [
        "Every point of a wave front serves as a point source of spherical, secondary waves that move forward with the same speed as the wave. (2)"],
        ["Which wave behaviour seen at a narrow slit does the principle explain?", "How does the principle describe a wave front moving forward?"],
        each=2),
    mcq("7.3", "How will distance x be affected if the slit width is increased?" + CHOOSE, ["Increase", "Decrease", "Remain the same"], 1,
        ["Does a narrow gap or a wide gap make waves spread out more?",
         "How is the width of the central bright band linked to how much the light spreads out?"], marks=1),
    rub("7.4", "Explain the answer to QUESTION 7.3.", 2, ["The degree/amount of diffraction is inversely proportional to the slit width. (2)"],
        ["Which quantity did you change in QUESTION 7.3, and how did the spreading of the light change?",
         "What kind of relationship links those two quantities?"], each=2,
        after=["7.3"]),   # its cards (inverse proportion) give 7.3's answer
    mcq("7.5", "How will distance x be affected if distance y is increased?" + CHOOSE, ["Increase", "Decrease", "Remain the same"], 0,
        ["Does moving the screen change how much the light spreads out at the slit?",
         "Think of a torch beam: how does the patch of light on a wall change as you move the torch further away?"], marks=1),
]

# ---- QUESTION 8, the question paper page 13 and the memo page 10 ----
q8 = [
    rub("8.1", "Define the term electric field at a point.", 2, [
        "Electric field at a point is the electrostatic force experienced per unit positive charge placed at that point. (2)"],
        ["What is the SI unit of electric field strength?", "Is the electric field a scalar or a vector quantity?"], each=2),
    mcq("8.2", "Are the charges NEGATIVE or POSITIVE?", ["Negative", "Positive"], 0,
        ["Does the electric field point towards or away from a negative charge?",
         "Both charges are to the left of P: in which direction do their fields at P point?"], marks=1),
    draw("8.3", "Draw the resultant electric field pattern for charges X and Y.", 3, [
        ["Shape of the field", 1], ["Direction of the field", 1], ["Lines touch the charges and do not cross", 1]],
        ["Do field lines start or end on the kind of charge you found in QUESTION 8.2?",
         "Between two like charges, do the field lines join up or turn away from each other?"],
        memo="The memo's sketch: two negative charges, field lines coming in from all sides and ending on each charge; between the charges the "
             "lines bend away from each other without crossing.",
        after=["8.2"]),   # its memo sketch (lines ending on negative charges) shows 8.2's answer
    work("8.4", "Calculate the magnitude of the charge X.", 5, [
        "Enet = {kQ}/{r²} + {kQ}/{r²}\n5,44 × 10⁶ = {(9 × 10⁹)Q}/{(2 × 10⁻³)²} + {(9 × 10⁹)Q}/{(3 × 10⁻³)²}\nQ = 1,67 × 10⁻⁹ C",   # 2 mm for X to P
        "Enet = {kQ}/{r²} − {kQ}/{r²}\n5,44 × 10⁶ = {(9 × 10⁹)Q}/{(3 × 10⁻³)²} − {(9 × 10⁹)Q}/{(5 × 10⁻³)²}\nQ = 8,5 × 10⁻⁹ C",    # the fields
        # taken as opposite (a direction slip)
        "Enet = {kQ}/{r²} + {kQ}/{r²}\n5,44 × 10⁶ = {(9 × 10⁹)Q}/{5 × 10⁻³} + {(9 × 10⁹)Q}/{3 × 10⁻³}\nQ = 1,13 × 10⁻⁶ C",        # r not squared
        "Enet = {kQ}/{r²} + {kQ}/{r²}\n5,44 × 10⁶ = {(9 × 10⁹)Q}/{(5 × 10⁻³)²} + {(9 × 10⁹)Q}/{(3 × 10⁻³)²}\nQ = 4 × 10⁻⁹ C"], 3,  # the memo
        ["Do the fields of X and Y at P point the same way or opposite ways?", "How far is charge X from point P, in metres?"]),
    rub("8.5", "Charge Y is now replaced by an identical oppositely charged point charge.\n\nHow will the magnitude of the net electric field at point "
        "P be affected? Choose from INCREASE, DECREASE or REMAIN THE SAME.\n\nGive a reason for the answer.", 2, [
        "Net electric field DECREASES (1)",
        "The positive charge on X will have a field in the opposite direction. The electric field (strength) being a vector will decrease because "
        "of opposite directions. (1)"],
        ["Does the field of a positive charge point towards it or away from it?", "At P, in which direction does the field of each charge now point?"],
        after=["8.2"]),   # its cards name the original charges as negative (8.2's answer)
]

# ---- QUESTION 9, the question paper page 14 and the memo page 11 ----
q9 = [
    rub("9.1", "State Faraday's law in words.", 2, [
        "The magnitude of the induced emf across the ends of a conductor is directly proportional to the rate of change in the magnetic flux linkage "
        "with the conductor. (2)"],
        ["What must a conductor experience for an emf to be induced in it?", "Is this law about the size of the emf, or about the direction of the induced current?"],
        each=2),
    work("9.2", "The graph below shows how the induced emf varies with the inverse of time.\n\nUse the information in the graph to calculate the "
         "change in magnetic flux.", 5, [
        "ε = {−NΔΦ}/{Δt}\n3 = (−200)ΔΦ(1,8)\nΔΦ = −0,0083 Wb",                           # the memo (OPTION 1; any point of the line gives it)
        "ε = {−NΔΦ}/{Δt}\n3 = {(−200)ΔΦ}/{1,8}\nΔΦ = −0,027 Wb",                         # 1/Δt read as Δt
        "ε = {−ΔΦ}/{Δt}\n3 = (−1)ΔΦ(1,8)\nΔΦ = −1,67 Wb",                                # the number of windings left out
        "ε = {−NΔΦ}/{Δt}\n3 = (−200)ΔΦ(2)\nΔΦ = −0,0075 Wb"], 0,                         # the line misread at 3 V (2 for 1,8)
        ["Which equation links the emf, the number of windings and the change in flux?",
         "Which pair of values can you read exactly where the line crosses a grid line?"],
        figure=fig("Q9b", "Graph of the induced emf ε in V, 0 to 3, up, against 1/Δt, 0 to 3, across, on a grid, with a straight line drawn from "
                   "the origin.")),
    work("9.3", "The coil rotates through an angle θ to a position where the magnetic flux becomes zero. Calculate angle θ.", 4, [
        "ΔΦ = Φf − Φi\n−0,0083 = (4,86 × 10⁻³)(2,4) sin 0° − (4,86 × 10⁻³)(2,4) sin θ\nθ = 45,36°",                 # sin for cos (flux from the plane)
        "ΔΦ = Φi − Φf\n−0,0083 = (4,86 × 10⁻³)(2,4) cos θ − (4,86 × 10⁻³)(2,4) cos 90°\nθ = 135,36°",               # the change turned round
        "ΔΦ = Φf − Φi\n−0,0083 = (4,86 × 10⁻³)(2,4) cos 90° − (4,86 × 10⁻³)(2,4) cos θ\nθ = 44,64°",                # the memo
        "ΔΦ = Φf − Φi\n−0,0083 = 200(4,86 × 10⁻³)(2,4) cos 90° − 200(4,86 × 10⁻³)(2,4) cos θ\nθ = 89,80°"], 2,      # N counted in the flux
        # (the unrounded −0,00833 Wb gives 44,40°: never an option)
        ["What is the area of the coil in m²?", "At which angle between the field and the normal to the coil is the flux zero?"],
        after=["9.2"]),   # the options show 9.2's −0,0083 Wb
]

# ---- QUESTION 10, the question paper page 15 and the memo pages 12-13 ----
OPEN = "The switch in the circuit is now OPENED. "
q10a = [
    rub("10.1.1", "Define the term power.", 2, ["Power is the rate at which work is done or energy is transfered. (2)"],
        ["What is the SI unit of power?", "How is power different from the work done?"], each=2),
    work("10.1.2", "Calculate the effective resistance of the parallel combination.", 2, [
        "R = R1 + R2\nR = 6 + 15\nR = 21 Ω",                                                       # added as if in series
        "{1}/{R∥} = {1}/{R1} + {1}/{R2}\n{1}/{R∥} = {1}/{6} + {1}/{15}\nR∥ = 4,29 Ω",               # the memo (OPTION 1)
        "{1}/{R∥} = {1}/{R1} + {1}/{R2}\n{1}/{R∥} = {1}/{6} + {1}/{15}\nR∥ = 0,23 Ω",               # 1/R∥ not turned over
        "{1}/{R∥} = {1}/{R1} + {1}/{R2}\n{1}/{R∥} = {1 + 1}/{6 + 15}\nR∥ = 10,5 Ω"], 1,             # the fractions added top and bottom
        ["Are the 6 Ω and 15 Ω resistors in series or in parallel?", "Which formula gives the effective resistance of resistors in that arrangement?"]),
    work("10.1.3", "Calculate the potential difference across the resistors in parallel.", 3, [
        "P = {V²}/{R}\n50 = {V²}/{4,29}\nV = 214,5 V",                                   # the square root not taken
        "P = {V²}/{R}\n50 = {V²}/{6}\nV = 17,32 V",                                      # one resistor only (the wrong part)
        "P = {V²}/{R}\n50 = {V²}/{6 + 15}\nV = 32,40 V",                                 # the resistors combined as in series
        "P = {V²}/{R}\n50 = {V²}/{4,29}\nV = 14,65 V"], 3,                               # the memo (from the unrounded 4,286 Ω: 14,64 V, never
        # an option)
        ["Which equation links power, potential difference and resistance?", "Which resistance must you use for the parallel part as a whole?"],
        after=["10.1.2"]),   # the options show 10.1.2's 4,29 Ω
    work("10.1.4", "Calculate the current through resistor R.", 3, [
        "R = {V}/{I}\n4,29 = {14,65}/{I}\nI = 3,41 A",                                   # the memo (OPTION 1)
        "R = {V}/{I}\n4,29 = {14,65}/{I}\nI = 62,85 A",                                  # rearranged wrongly (multiplied)
        "R = {V}/{I}\n6 = {14,65}/{I}\nI = 2,44 A",                                      # one branch only (the 6 Ω resistor)
        "R = {V}/{I}\n6 + 15 = {14,65}/{I}\nI = 0,70 A"], 0,                             # the parallel resistors added as in series
        # (the memo's OPTION 4 adds the branch currents to 3,42 A: never an option)
        ["Which equation links potential difference, current and resistance?",
         "How does the current through R compare with the total current through the parallel part?"],
        after=["10.1.2", "10.1.3"]),   # the options show 10.1.2's 4,29 Ω and 10.1.3's 14,65 V
    mcq("10.1.5", OPEN + "How will the reading on the voltmeter (V) be influenced? Choose from INCREASE, DECREASE or REMAIN THE SAME.",
        ["Increase", "Decrease", "Remain the same"], 1,
        ["What happens to the resistance of the parallel part when one of its branches is cut off?",
         "How does the current in the circuit change when the total resistance changes?"], marks=1),
    rub("10.1.6", OPEN + "Explain the answer to QUESTION 10.1.5.", 3, [
        "The total resistance increases (1)", "The current in the circuit decreases (1)",
        "The resistance of R is constant, (1) then the potential difference across R decreases."],
        ["What happens to the effective resistance of the parallel part when the 15 Ω branch is cut off?",
         "Across which resistor is the voltmeter connected?"],
        after=["10.1.5"]),   # its cards say the reading decreases (10.1.5's answer)
]
q10b = [
    work("10.2.1", "Calculate the energy used by the geyser for 5 hours per day.", 4, [
        "P = {W}/{Δt}\n2 000 = {W}/{5}\nW = 1 × 10⁴ J",                                  # the time left in hours
        "P = {W}/{Δt}\n2 000 = {W}/{300}\nW = 6 × 10⁵ J",                                # the time in minutes
        "P = {W}/{Δt}\n2 000 = {W}/{18 000}\nW = 3,6 × 10⁷ J",                           # the memo
        "P = WΔt\n2 000 = W(18 000)\nW = 0,11 J"], 2,                                    # the formula upside down
        ["Which equation links power, energy and time?", "What is 5 hours in seconds?"]),
    work("10.2.2", "Calculate the cost of electricity to operate the geyser for a month with 30 days.", 2, [
        "Cost = price × unit kWh\nCost = 80(2)(5)\nCost = 800 cents = R8",                           # one day only
        "Cost = price × unit kWh\nCost = 80(2)(5)(30)\nCost = 24 000 cents = R240",                  # the memo (rand or cents)
        "Cost = price × unit kWh\nCost = 80(2 000)(5)(30)\nCost = 24 000 000 cents = R240 000",      # the watts not turned into kilowatts
        "Cost = price × unit kWh\nCost = 80(2)(5)(30)\nCost = R24 000"], 1,                          # the cents taken as rand
        ["What is the geyser's power in kilowatts?", "In which unit of energy is the price of electricity given?"]),
]

POS_TABLE = {"head": ["NET FORCE (N)", "a (m·s⁻²)"], "rows": [["0,3", "0,36"], ["0,6", "0,73"], ["0,9", "1,09"], ["1,2", "1,45"]]}
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20, "lead": MC_LEAD, "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Forces in equilibrium", "marks": 13,
     "lead": "Block A, which is at rest on a horizontal rough surface, is used as an anchor to hold block B, with a mass of 56 kg, in the air at a "
             "certain height above the ground. The two blocks are connected with rope R, which makes an angle of 35° with the vertical. Block B "
             "is suspended from the ceiling with cable C. Refer to the diagram below.\n\nBlock A experiences a frictional force of magnitude 200 N. "
             "The system is stationary.",
     "figure": fig("Q2", "Block B, 56 kg, hangs from the ceiling by cable C, which makes the angle θ with the ceiling; rope R runs from B up and to "
                   "the right to block A, which rests on a horizontal surface, and makes 35° with a dashed vertical line through B."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Force and acceleration", "marks": 13,
     "lead": "Learners investigate the relationship between net force and acceleration by pulling a trolley across a surface which is slightly "
             "inclined to compensate for friction. The trolley is connected to different masses by a string of negligible mass. The string passes "
             "over a frictionless pulley. Refer to the diagram below.\n\nTicker-tape attached to the trolley passes through the ticker-timer. The "
             "acceleration of the trolley is determined by analysing the ticker-tape. The results of the net force produced by the different "
             "masses and the acceleration of the trolley were recorded in the table below.",
     "table": POS_TABLE,
     "figure": fig("Q3", "A trolley on a slightly inclined runway, joined by a string over a pulley at the left end to a hanging mass; ticker tape "
                   "from the trolley runs through a ticker-timer at the right end."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Towing at constant velocity", "marks": 26,
     "lead": "A tow truck pulls a car along a gravel road.\n\nThe force applied by the engine of the tow truck is 9 000 N. The mass of the tow truck "
             "is 1 300 kg and the mass of the car is 950 kg. The vehicles are connected to each other by an inelastic tow bar of negligible mass. "
             "See the diagram below.\n\nThe tow truck and car move at a CONSTANT VELOCITY.",
     "figure": fig("Q4", "A tow truck, 1 300 kg, on the left pulls a car, 950 kg, behind it along a road, joined by a tow bar marked T; an arrow "
                   "labelled 9 000 N points to the left from the front of the truck."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Gravity on another planet", "marks": 8,
     "lead": "The acceleration due to gravity on planet X is 2,7 m·s⁻². The radius of this planet is a third (⅓) of the radius of Earth.", "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Refractive index", "marks": 18,
     "lead": "Experiments are performed to compare the refractive indices of different materials.\n\nIn one experiment a light ray passes from air to "
             "material A and the angles of incidence and refraction are measured. The refractive index for air is 1.\n\nThe graph below was drawn "
             "using the results of material A.",
     "figure": fig("Q6", "Graph of sin θr up against sin θi across: a straight line from the origin labelled A; dashed lines from 0,56 on the "
                   "sin θi axis and from 0,37 on the sin θr axis meet on the line."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Diffraction at a single slit", "marks": 8,
     "lead": "An experiment is set up, as shown below, to investigate the effect of slit width on the degree of diffraction. Distance y on the diagram "
             "represents the distance between the screen and the single slit. Distance x on the diagram represents the width of the central bright "
             "band.",
     "figure": fig("Q7", "A light source below a single slit; the light passes up through the slit to a screen a distance y above it, where the "
                   "central bright band of width x lies between two dark bands."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Electric field of two charges", "marks": 13,
     "lead": "Two IDENTICAL point charges, X and Y, are placed 2 mm apart. Point P is 3 mm to the right of charge Y. The net electric field at point P "
             "is 5,44 × 10⁶ N·C⁻¹ to the left.",
     "figure": fig("Q8", "Charges X and Y, 2 mm apart, with point P 3 mm to the right of Y, all on one line."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Electromagnetic induction", "marks": 11,
     "lead": "An induction coil of area 48,6 cm² and 200 windings is rotated clockwise in a constant magnetic field of magnitude 2,4 T. Refer to the "
             "diagram below.",
     "figure": fig("Q9a", "A circular coil between the S pole on the left and the N pole on the right, with the magnetic field lines pointing from "
                   "N to S; a dashed line through the coil is tilted to the field, and a curved arrow marks the angle θ from it down to a dashed "
                   "field line."), "items": q9},
    {"id": "10", "title": "Question 10", "kind": "Electric circuits", "marks": 14,
     "lead": "The circuit below consists of a 6 Ω and 15 Ω resistor connected in parallel and an unknown resistor R, in series. An ammeter, a "
             "high-resistance voltmeter, a closed switch and battery are connected, as shown. The resistance of the battery and wires can be "
             "ignored.\n\nThe total power dissipated in the parallel part of the circuit is 50 W.",
     "figure": fig("Q10", "A battery in series with an ammeter A, a resistor R with voltmeter V across it, and a parallel pair: a 6 Ω resistor in "
                   "one branch and a 15 Ω resistor with a closed switch in the other."), "items": q10a},
    {"id": "10.2", "title": "Question 10.2", "kind": "Electrical energy and cost", "marks": 6,
     "lead": "A geyser, labelled 2 000 W, is used for an average of 5 hours per day. The cost of electricity is 80 cents per kWh.", "items": q10b},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Grade 12 Physical Sciences P1 2025 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, the inverse relation, another quantity's definition, the opposite choice):
# never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns `each`;
# the cards are shuffled the same way every run. The rubric bullets above stay as the source.


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random(PID + ":" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    pool = sorted(k for k, i in enumerate(order) if i < len(right))
    # a single right card first, or every right card on top, would be an answer by position
    assert pool != list(range(len(pool))), (n, "the right cards on top: an answer by position", pool)
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count}


STATEMENTS = {
    # 2, either form the memo gives: the wrong ones are a component, a scalar, a difference, a perpendicular vector
    "2.1": (2, ["The vector sum of two or more vectors.", "The single vector which has the same effect as two or more vectors together."],
               ["One of two perpendicular vectors that together have the same effect as a single vector.", "A physical quantity that has magnitude only.",
                "The difference between the largest and the smallest of two vectors.", "A vector that acts at right angles to another vector."]),
    # 2 (the memo's example): the wrong ones are the inverse, the wrong variables, a question, no relation
    "3.1": (2, ["The net force is directly proportional to the acceleration, if the mass of the trolley is kept constant."],
               ["The net force is inversely proportional to the acceleration, if the mass of the trolley is kept constant.",
                "The mass of the trolley is directly proportional to its acceleration, if the net force is kept constant.",
                "What is the relationship between the net force and the acceleration of the trolley?",
                "The acceleration of the trolley does not depend on the net force acting on it."]),
    # 2: the wrong ones are friction with the motion, the normal force, weight, friction perpendicular to the surface
    "4.1": (2, ["Frictional force is the force that opposes the motion of an object and which acts parallel to the surface."],
               ["Frictional force is the force that acts in the direction of motion of an object and parallel to the surface.",
                "Frictional force is the force exerted by a surface on an object, perpendicular to the surface.",
                "Frictional force is the force with which the Earth attracts an object.",
                "Frictional force is the force that opposes the motion of an object and which acts perpendicular to the surface."]),
    # 3 (NAME 1 + STATE 2) in one card: the wrong ones name another law, reverse the direction, change the size, drop "simultaneously",
    # or pair the third law's name with the first or second law's words (7 wrong cards: with four to six the right card came first)
    "4.2": (3, ["Newton's Third Law: when object A exerts a force on object B, object B simultaneously exerts an oppositely directed force of equal "
                "magnitude on object A."],
               ["Newton's First Law: when object A exerts a force on object B, object B simultaneously exerts an oppositely directed force of equal "
                "magnitude on object A.",
                "Newton's Third Law: when object A exerts a force on object B, object B simultaneously exerts a force of equal magnitude in the same "
                "direction on object A.",
                "Newton's Third Law: when object A exerts a force on object B, object B exerts a smaller force on object A some time later.",
                "Newton's Third Law: a body remains in its state of rest or of motion at constant velocity unless a non-zero net force acts on it.",
                "Newton's Second Law: when object A exerts a force on object B, object B simultaneously exerts an oppositely directed force of equal "
                "magnitude on object A.",
                "Newton's Third Law: when object A exerts a force on object B, object B simultaneously exerts an oppositely directed force of twice "
                "the magnitude on object A.",
                "Newton's Third Law: the acceleration of an object is directly proportional to the net force acting on it and inversely proportional "
                "to its mass."]),
    # 3 ticks: the law, its words, the friction that slows the car; the wrong ones are the third law, the opposite of inertia, a pull that
    # stays, a zero net force
    "4.5": (1, ["The car's motion is explained by Newton's first law.",
                "An object continues moving at a constant velocity unless a non-zero net force acts on it.",
                "The net force acting on the car is now the frictional force, which causes the car to slow down."],
               ["The car's motion is explained by Newton's third law.", "An object needs a net force acting on it to keep moving at a constant velocity.",
                "The tow bar keeps pulling the car forward after it disconnects.", "The net force acting on the car is now zero, so it slows down."]),
    # 2 ticks, one each: the wrong ones swap the two definitions, make mass change, give weight the unit of mass
    "5.1": (1, ["Weight is the gravitational force exerted on an object by the Earth.", "Mass is the amount of matter in a body."],
               ["Weight is the amount of matter in a body.", "Mass is the gravitational force exerted on an object by the Earth.",
                "The mass of an object changes when it is taken to another planet.", "Weight is measured in kilograms."]),
    # 2: the wrong ones measure from the surface, are the angles of refraction and reflection, or the angle between the two rays
    "6.1": (2, ["Angle of incidence is the angle between the normal to a reflecting surface and the incident ray."],
               ["Angle of incidence is the angle between the incident ray and the surface.", "Angle of incidence is the angle between the normal and the "
                "refracted ray.", "Angle of incidence is the angle between the incident ray and the reflected ray.",
                "Angle of incidence is the angle between the normal and the reflected ray."]),
    # 2: the wrong ones reverse the direction, make the media equal, send the ray along the normal, ask for white light
    "6.5.2": (2, ["Light must travel from an optically denser medium (higher refractive index) to an optically less dense medium (lower refractive "
                  "index)."],
                 ["Light must travel from an optically less dense medium (lower refractive index) to an optically denser medium (higher refractive "
                  "index).", "The two media must have the same refractive index.", "The light must strike the boundary along the normal.",
                  "The light must be white light, not monochromatic light."]),
    # 2, either of the memo's questions: the wrong ones name another variable, ask YES or NO, swap cause and effect, ask about brightness
    "7.1": (2, ["What is the relationship between slit width and degree of diffraction?",
                "How does the width of the central bright band change as the slit width changes?"],
               ["What is the relationship between the wavelength of the light and the degree of diffraction?",
                "Does the slit width affect the degree of diffraction?", "How does the degree of diffraction affect the slit width?",
                "Which light source gives the brightest central band?"]),
    # 2: the wrong ones halve the speed, send the waves backwards, deny bending, are the law of reflection
    "7.2": (2, ["Every point of a wave front serves as a point source of spherical, secondary waves that move forward with the same speed as the wave."],
               ["Every point of a wave front serves as a point source of spherical, secondary waves that move forward with half the speed of the wave.",
                "Every point of a wave front serves as a point source of secondary waves that move backwards, towards the source.",
                "Light travels in straight lines and cannot bend around the edges of a slit.",
                "The angle of incidence is equal to the angle of reflection."]),
    # 2 (the memo's "/" read once: degree): the wrong ones are direct, no relation, the wavelength inverse, a wider slit spreading more
    "7.4": (2, ["The degree of diffraction is inversely proportional to the slit width."],
               ["The degree of diffraction is directly proportional to the slit width.", "The degree of diffraction does not depend on the slit width.",
                "The degree of diffraction is inversely proportional to the wavelength of the light.", "A wider slit makes the light spread out more."]),
    # 2: the wrong ones use a negative test charge, drop "per unit charge", are potential, or a charge
    "8.1": (2, ["Electric field at a point is the electrostatic force experienced per unit positive charge placed at that point."],
               ["Electric field at a point is the electrostatic force experienced per unit negative charge placed at that point.",
                "Electric field at a point is the electrostatic force experienced by any charge placed at that point.",
                "Electric field at a point is the work done per unit positive charge to bring it to that point.",
                "Electric field at a point is the amount of charge placed at that point."]),
    # 2 ticks: the choice (decreases) beside its reason. The memo's reason names X as the new positive charge; the stem replaces Y
    # (flagged): the right card names neither letter
    "8.5": (1, ["The net electric field at P decreases.",
                "The field of the positive charge at P points in the opposite direction to the field of the negative charge; the electric field is a "
                "vector, so the net field decreases."],
               ["The net electric field at P increases.", "The net electric field at P remains the same.",
                "The fields of the two charges now point in the same direction at P, so they add.",
                "The electric field is a scalar, so the fields of the two charges add as numbers."]),
    # 2: the wrong ones drop "rate of change", make it inverse, are Lenz's law, or tie the emf to the time in the field
    "9.1": (2, ["The magnitude of the induced emf across the ends of a conductor is directly proportional to the rate of change in the magnetic flux "
                "linkage with the conductor."],
               ["The magnitude of the induced emf across the ends of a conductor is directly proportional to the magnetic flux linkage with the conductor.",
                "The magnitude of the induced emf across the ends of a conductor is inversely proportional to the rate of change in the magnetic flux "
                "linkage with the conductor.",
                "The induced current flows in a direction so that its magnetic field opposes the change that produced it.",
                "The magnitude of the induced emf is directly proportional to the time for which the conductor stays in the magnetic field."]),
    # 2: the wrong ones are a total, potential difference, current and work
    "10.1.1": (2, ["Power is the rate at which work is done or energy is transferred."],
                  ["Power is the total work done by a device.", "Power is the energy transferred per unit charge.", "Power is the rate of flow of charge.",
                   "Power is the product of a force and the distance through which it moves an object."]),
    # 3 ticks: the wrong ones reverse the resistance and the current, change R, or send more current through the 15 Ω branch
    "10.1.6": (1, ["The total resistance increases.", "The current in the circuit decreases.",
                   "The resistance of R is constant, so the potential difference across R decreases."],
                  ["The total resistance decreases.", "The current in the circuit increases.", "The resistance of R increases when the switch is opened.",
                   "More current now flows through the 15 Ω resistor."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, laws, a hypothesis, an investigative question, a relationship and explanations), so SORTS stays empty and sort_
# is kept for parity.
SORTS = {}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random(PID + ":sort:" + n).shuffle(order)
    rows = [rows[i] for i in order]
    assert marks == len(rows) and len(set(b for _, b in rows)) == len(bins), n
    return {"t": "match", "n": n, "marks": marks, "q": q + " Sort each statement.", "clues": clues, "left": [r for r, _ in rows],
            "right": bins, "a": [b for _, b in rows], "heads": ["STATEMENTS", "SORT INTO"], "groups": True}


for _m in missions:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric" and _it["n"] in SORTS:
            _bins, _rows = SORTS[_it["n"]]
            _m["items"][_k] = sort_(_it["n"], _it["q"], _it["marks"], _bins, _rows, _it["clues"])
        elif _it["t"] == "rubric" and _it["n"] in STATEMENTS:
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            _m["items"][_k] = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
        if _it.get("after"):   # its gate rides along onto the played part
            _m["items"][_k]["after"] = _it["after"]
assert not [i["n"] for m in missions for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"

assert tuple(AUTHORED) == ("2.5", "2.6", "3.4", "3.5", "4.4.1", "4.4.2", "4.6", "5.2", "5.3", "6.2", "6.3", "6.4.1", "8.4", "9.2", "9.3",
                           "10.1.2", "10.1.3", "10.1.4", "10.2.1", "10.2.2"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["2.2", "2.4"]
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["3.2.1", "3.2.2"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.3", "3.3", "4.3", "6.4.2", "8.3"]
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]
assert PICKS == ["2.1", "3.1", "4.1", "4.2", "4.5", "5.1", "6.1", "6.5.2", "7.1", "7.2", "7.4", "8.1", "8.5", "9.1", "10.1.1", "10.1.6"], PICKS

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2017", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic physics errors (a sign or direction slip, a value "
                                                       "from the wrong body, part or row, a formula upside down or with a factor dropped, a power "
                                                       "of ten slipped, a unit not converted, the wrong constant, the calculator in radians), 0 or "
                                                       "full marks: " + ", ".join(AUTHORED) +
                                                       " (%d parts, %d marks). 4.6 shows its working, then the value with its direction (the memo's "
                                                       "backwards / to the right). 6.5.1 (a range of angles, no working) plays as an answer multiple "
                                                       "choice: 49° to 90° beside the range below the critical angle, the critical angle's "
                                                       "complement and the critical angle alone. A value the memo also accepts is never a wrong "
                                                       "option: 3.4's 1,21 / 1,22 / 1,2 (any set of coordinates), 6.2's 1,52 (1/0,66) and so 6.3's "
                                                       "1,97 x 10⁸ m·s⁻¹, 9.3's 44,40° (from the unrounded −0,00833 Wb), 10.1.3's 14,64 V (from the "
                                                       "unrounded 4,286 Ω), 10.1.4's 3,42 A (its OPTION 4); 10.2.2's right option gives both cents "
                                                       "and rand." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "3.3", "kind": "memo_issue", "detail": "The memo's graph on memo page 4 plots the points with the axes' values swapped (the accelerations "
                                                     "0,36 to 1,45 along the axis labelled Force, the forces 0,3 to 1,2 up the axis labelled "
                                                     "Acceleration). Its graph drawn to scale on memo page 14 is right (a up, F across), and 3.4 and 3.5 "
                                                     "use a / F; 3.3's memo note follows page 14."},
        {"n": "6.2", "kind": "memo_issue", "detail": "The memo's OPTION 1 (memo page 8) writes nr = 1/0,66 = 1,51; 1/0,66 = 1,52 (1,51 comes from "
                                                     "the unrounded gradient 0,6607, as its OPTION 2's 1(0,56) = nr(0,37) does). The right option keeps "
                                                     "the memo's lines and 1,51; 1,52, and 6.3's 1,97 x 10⁸ m·s⁻¹ from it, are never a wrong option."},
        {"n": "8.5", "kind": "memo_issue", "detail": "The memo's reason (memo page 10) says 'The positive charge on X will have a field in the opposite "
                                                     "direction'; the stem replaces charge Y with the oppositely charged charge, so the positive charge "
                                                     "is the new one at Y. The right reason card names neither letter: the positive charge's field at P "
                                                     "opposes the negative charge's, the field is a vector, so the net field decreases (5,44 x 10⁶ to "
                                                     "2,56 x 10⁶ N·C⁻¹)."},
        {"n": "6.5.1", "kind": "low_confidence", "detail": "The paper gives material A's critical angle as 49°; 6.2's and 6.4.1's indices (1,51 and "
                                                           "1,25) would put it at 55,9° from A to B (41,5° from A to air). 6.5.1 plays as printed, "
                                                           "with the memo's 49° to 90°."},
        {"n": "1.2", "kind": "no_fit", "detail": "1.2's options are four printed vector diagrams: they are the question's figure (each triangle's "
                                                 "arrows described in its caption), and the options read 'Diagram A' to 'Diagram D'."},
        {"n": "9.2", "kind": "no_fit", "detail": "Question 9 prints the coil diagram, then a sentence, then the graph: the coil is the mission's "
                                                 "figure, and the graph, with its sentence, is 9.2's own (the only part that reads it)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 10), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (vector diagrams, ray paths, graphs, circuits and the memo's fractions are "
                                                           "images); no API call."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions, laws, the hypothesis, the "
                                                    "investigative question and the relationship (2.1, 3.1, 4.1, 6.1, 6.5.2, 7.1, 7.2, 7.4, 8.1, "
                                                    "9.1, 10.1.1) pick one card for their 2 marks (an OR form the memo accepts is a second right "
                                                    "card); 4.2 (NAME AND STATE, 1 + 2) picks one card that names and states the law, 3 marks; 4.5 "
                                                    "and 10.1.6 pick the memo's three points, 1 mark each; 5.1 picks its two points, 1 mark each; "
                                                    "8.5 picks the choice (decreases) and its reason, 1 mark each." % len(PICKS)},
        {"n": "2.3", "kind": "no_fit", "detail": "Drawings (2.3's and 4.3's free-body diagrams, 3.3's graph on the ANSWER SHEET's graph paper, 6.4.2's "
                                                 "sketch graphs, 8.3's field pattern) are done on paper and self-checked against the memo's criteria."},
    ],
}
QTOTAL = {"1": 20, "2": 13, "3": 13, "4": 26, "5": 8, "6": 18, "7": 8, "8": 13, "9": 11, "10": 20}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's ten printed letters are the paper's (A1 B3 C3 D3) and four printed choices of two or three (7.3 B, 7.5 A,
# 8.2 A, 10.1.5 B) can never be C or D: the 20 workings sit at A5 B5 C5 D5 and 6.5.1 at A, so the 31 four-option questions sit at A7 B8 C8
# D8 and the whole paper at A9 B10 C8 D8 (within 3 of even)
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 3, spread
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert min(wspread.values()) >= 3 and max(wspread.values()) <= 7, wspread
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, the paper:", spread, "authored:", wspread, "four-option:", fspread)
print("statement right-card positions:", {i["n"]: i["pool"] for i in ITEMS if i["t"] == "pickn"})
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; statements:", len(PICKS), "parts")
print("total:", total)
# every gate, so a dropped "after" fails the run
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "2.5": ["2.3", "2.4"], "2.6": ["2.4", "2.5"], "3.4": ["3.3"], "3.5": ["3.4"], "4.4.1": ["4.3"], "4.4.2": ["4.4.1"], "4.6": ["4.4.1", "4.4.2"],
    "6.3": ["6.2"], "6.4.2": ["6.4.1"], "7.4": ["7.3"], "8.3": ["8.2"], "8.5": ["8.2"], "9.3": ["9.2"], "10.1.3": ["10.1.2"],
    "10.1.4": ["10.1.2", "10.1.3"], "10.1.6": ["10.1.5"]}, {i["n"]: i.get("after") for i in ITEMS if i.get("after")}
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
