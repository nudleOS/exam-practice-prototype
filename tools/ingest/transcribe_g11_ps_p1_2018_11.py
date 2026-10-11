"""Grade 11 Physical Sciences P1 (Physics) Nov 2018 (DBE common paper), the whole paper (Questions 1 to 12), hand-transcribed into the
catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options,
marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API
call: the transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets its graphs, arrows,
field sketches and circuits as drawings, and the memo sets its fractions and formulas as images, so the text layers have gaps.

  python tools/ingest/transcribe_g11_ps_p1_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Physical Sciences P1 Nov 2018 Eng.pdf" "uploads/Grade 11 Physical Sciences P1 Nov 2018 MG Eng & Afr.pdf" --id g11-ps-p1-2018-11 --from-json

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; models: transcribe_ps_p1_2025_11.py and the Grade 10 pilots
transcribe_g10_ps_p1_2018_11.py / transcribe_g10_ps_p1_2017_11.py):
  multiple choice printed in the paper -> mcq as printed (graph and sketch options: the figure and "Graph A".."Graph D"; 1.8's four
  printed arrows: arrow signs with their directions, so its sketch of the charges stays its figure); a
  choice printed in the stem with no explanation in the same part (5.3 "UP THE SLOPE or DOWN THE SLOPE", 7.6 "YES or NO", 8.4 "RED or
  GREEN", 11.4 and 12.4 "INCREASE, DECREASE or STAY THE SAME", 11.6 "NORTH or SOUTH", 11.7 "FROM A TO B or FROM B TO A") -> mcq of the
  printed choices. One term the memo names -> term (2.1, 7.1). No part is a one-value read-off, so no part stays a typed number.
  Every calculation ("Calculate", "Hence, determine") whose memo shows a working -> authored multiple choice, `work`: the memo's FIRST
  working line by line and three workings each built from a DIFFERENT realistic error (a sign or direction slip, a value from the wrong
  body or part, a formula upside down or with a factor dropped, a power of ten slipped, a unit not converted, the wrong constant),
  every number recomputed; 0 or full marks. A value the memo also accepts (its OR answers and accepted directions, its "accept all
  possible options") is never a wrong option; where the memo's own value is a slip (12.3) the right option uses the right value and
  the memo's value is never a wrong option (Murci's ruling 2026-10-10). 10.2.1 ("Calculate the ratio", the memo's 16 : 1 with no
  working) is an answer multiple choice of realistic wrong ratios.
  A definition, law, conclusion or relationship -> statements (pick 1 card for its marks; an OR form a second right card); an
  explanation the memo ticks point by point -> statements, 1 mark a point; a choice with its reason in the same part (3.6) -> the
  choice a card beside its reason. No memo here weighs two sides, so no part plays as a sort.
  "Draw" (a free-body diagram, a ray diagram, a graph, a vector diagram, a field pattern) -> draw with the memo's criteria (self-checked,
  flagged no_fit).
  A part whose options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose stem or diagram changes part-way is two or three missions (7 and 7.4; 8, 8.3 and 8.5; 11 and
  11.6).
Figure boxes are measured in PDF points (page 595.44 x 841.68, read from the PDF) from the drawings, images and labels themselves and
checked on a contact sheet (scratchpad lower/g11-ps-p1-2018-11/figs.py)."""
import json
import random
import re
from pathlib import Path

PID = "g11-ps-p1-2018-11"
W, H = 595.44, 841.68
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.3": [3, 204.0, 500.0, 421.0, 603.0], "1.6": [4, 101.0, 433.0, 506.0, 649.0], "1.8": [5, 251.0, 296.0, 367.0, 382.0],
    "1.9": [5, 101.0, 606.0, 439.0, 753.0], "1.10": [6, 101.0, 129.0, 501.0, 361.0],
    "Q2": [7, 148.0, 169.0, 437.5, 346.0], "Q3": [8, 142.0, 166.0, 445.5, 248.0], "Q4": [9, 75.0, 176.0, 528.0, 540.0],
    "Q5": [10, 143.0, 176.0, 481.0, 302.0], "Q6": [10, 180.5, 566.0, 379.0, 693.5], "Q7a": [11, 235.0, 164.0, 336.0, 304.0],
    "Q7b": [11, 200.5, 506.0, 342.0, 635.5], "Q8a": [12, 130.0, 173.0, 511.0, 272.0], "Q8b": [12, 158.0, 385.0, 472.0, 495.0],
    "Q8c": [12, 125.0, 655.0, 427.5, 766.0], "Q9": [13, 149.0, 197.5, 380.0, 297.0], "Q10": [13, 203.5, 520.0, 361.0, 562.0],
    "Q11a": [14, 172.0, 177.0, 334.0, 254.0], "Q11b": [14, 118.0, 527.0, 311.0, 629.5], "Q12": [15, 156.5, 163.0, 398.5, 331.0]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points (key words, "... defined: 0/2", ACCEPT limits): never scored, never shown
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
    kw: catalogue extras, e.g. after=[...] when the options show an earlier part's answer."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


# ---- QUESTION 1: multiple choice, the question paper pages 3-6 and the memo page 2 ----
MC_LEAD = "Various options are provided as possible answers to the following questions."
q1 = [
    mcq("1.1", "Two forces, F1 and F2, act on a point. If F1 and F2 act in the same direction the maximum resultant has a magnitude of 13 N. If "
        "forces F1 and F2 act in opposite directions the magnitude of the minimum resultant is 3 N. The magnitude of the two forces, in newton, is …",
        ["8 and 5.", "16 and 10.", "3 and 10.", "10 and 7."], 0,
        ["When two forces act in the same direction, how do you combine their magnitudes?",
         "When they act in opposite directions, how do you combine them, and which pair of numbers fits both results?"]),
    mcq("1.2", "A free-moving block slides down an inclined plane at a CONSTANT VELOCITY. This means that the …",
        ["frictional force acting on the block is zero.", "net force acting on the block is in the direction down the slope of the plane.",
         "net force acting on the block is zero.", "component of weight parallel to the plane is greater than the frictional force."], 2,
        ["What is the acceleration of an object that moves at a constant velocity?", "Which of Newton's laws links an object's acceleration to the net force on it?"]),
    mcq("1.3", "A trolley is pushed along a horizontal surface with a force of 150 N at an angle of 45º to the horizontal. The trolley experiences a "
        "constant frictional force of 60 N.\n\nThe NET FORCE acting on the trolley:\n(i) Causes the trolley to accelerate horizontally\n(ii) Is equal "
        "to the applied force\n(iii) Is horizontally forward\n\nWhich of the statements above are CORRECT?",
        ["(i) and (ii)", "(ii) and (iii)", "(i) and (iii)", "(i), (ii) and (iii)"], 2,
        ["How big is the horizontal component of the 150 N push compared with the 60 N friction?",
         "Does the trolley move up or down, or is the vertical part of the push balanced by other forces?"],
        figure=fig("1.3", "A trolley on a horizontal surface. A 150 N force pushes on it from above and behind, at 45º to a dashed horizontal line; "
                   "a 60 N frictional force acts backwards along the surface.")),
    mcq("1.4", "A man in a lift is moving upwards at a CONSTANT SPEED. The weight of the man is W. According to Newton's Third Law, the reaction "
        "force of the weight W is the force of …", ["the floor on the man.", "Earth on the man.", "the man on the floor.", "the man on Earth."], 3,
        ["Between which two bodies does the weight W act, and which body exerts it?",
         "Does a reaction force act on the same body as its action force, or on the other body?"]),
    mcq("1.5", "The optical density of a medium …",
        ["will be high if the refraction of light is less.", "is a measure of the refracting power of the medium.",
         "is less when light bends towards the normal when entering the medium.", "will be high if light moves faster through the medium."], 1,
        ["Does light travel faster or slower in an optically denser medium?",
         "When light enters an optically denser medium, does it bend towards or away from the normal?"]),
    mcq("1.6", "In which ONE of the graphs below will the gradient represent the refractive index of a material when light passes from the air "
        "through the material?", ["Graph A", "Graph B", "Graph C", "Graph D"], 3,
        ["Write Snell's law for light that passes from air (n = 1) into the material: which quantity equals n multiplied by which?",
         "For the gradient to equal n, which quantity must go on the vertical axis, and which on the horizontal axis?"],
        figure=fig("1.6", "Four graphs, A to D, each a straight line from the origin. A: θi up against θr across. B: sin θr up against sin θi "
                   "across. C: θr up against θi across. D: sin θi up against sin θr across.")),
    mcq("1.7", "Every point on a wave front acts as a point source of spherical, secondary waves that move forward at the same speed as the wave. "
        "This statement represents …", ["Snell's law.", "Huygens' principle.", "refraction.", "the law of reflection."], 1,
        ["Is the statement about how a wave front moves forward, or about what happens where two media meet?",
         "Which principle explains why waves spread out after they pass through a narrow gap?"]),
    # the options are four printed arrows, typed as arrow signs with their directions, so the sketch of the charges stays the figure
    mcq("1.8", "Three charges of magnitudes +2q, +2q and -2q are shown in the sketch below. Which arrow CORRECTLY indicates the direction of the "
        "NET FORCE acting on the -2q charge?", ["↗ (up and to the right)", "↙ (down and to the left)", "→ (to the right)", "↓ (down)"], 0,
        ["Does each +2q charge attract or repel the -2q charge, and in which direction does each force act?",
         "How do you add two forces of equal size that act at right angles to each other?"],
        figure=fig("1.8", "Charge −2q, with a charge +2q a distance d directly above it and another +2q a distance d to its right, the two "
                   "distances at right angles.")),
    mcq("1.9", "Which ONE of the sketches below represents the CORRECT magnetic field pattern around a straight current-carrying conductor?",
        ["Sketch A", "Sketch B", "Sketch C", "Sketch D"], 1,
        ["Around a straight conductor, are the field lines circles or straight lines?",
         "What does a cross show about the direction of the current, and which way does the right-hand rule then turn the field?"],
        figure=fig("1.9", "Four sketches, A to D. A: concentric circles round a dot, with an arrow at the top pointing to the right. B: concentric "
                   "circles round a cross, with an arrow at the top pointing to the right. C: straight lines spreading out from a dot, with an "
                   "arrow on the right-hand line pointing towards the dot. D: straight lines spreading out from a dot, with an arrow on the "
                   "left-hand line pointing away from the dot.")),
    mcq("1.10", "Which ONE of the graphs below CORRECTLY represents the relationship between potential difference and current in a non-ohmic resistor?",
        ["Graph A", "Graph B", "Graph C", "Graph D"], 2,
        ["What shape does the potential difference against current graph have for an ohmic resistor?",
         "In a non-ohmic resistor, such as a bulb filament, what happens to the resistance as the current grows?"],
        figure=fig("1.10", "Four graphs, A to D, of V (V) up against I (A) across. A: a straight line from the origin. B: a curve that falls "
                   "steeply and then levels off. C: a curve from the origin that gets steeper as I increases. D: a straight line that falls from "
                   "the V-axis to the I-axis.")),
]

# ---- QUESTION 2, the question paper page 7 and the memo page 3 ----
q2 = [
    term("2.1", "Give the correct term for the following description: A single vector having the same effect as two or more vectors together",
         ["Resultant (net) vector", "Resultant vector", "Net vector", "Resultant"],
         ["Is this one vector that replaces several vectors, or one part of a single vector?",
          "What do you call the vector you get when you add two or more vectors?"]),
    work("2.2.1", "Calculate the magnitude of the vertical component of the 50 N.", 2, [
        "Fy = F cos θ\nFy = 50 cos 30°\nFy = 43,30 N",                                  # cos for sin (the side next to the angle)
        "Fy = F sin θ\nFy = 80 sin 30°\nFy = 40 N",                                     # the 80 N force (a value from the wrong force)
        "Fy = F sin θ\nFy = 50 sin 30°\nFy = 25 N",                                     # the memo (OR 50 cos 60°)
        "Fy = {F}/{sin θ}\nFy = {50}/{sin 30°}\nFy = 100 N"], 2,                        # the formula upside down
        ["Which angle does the 50 N force make with the horizontal?",
         "Is the vertical component the side opposite that angle or the side next to it?"]),
    work("2.2.2", "Calculate the magnitude of the resultant (net) force.", 5, [
        "Fx = 50 cos 30° = 43,3 N\nRx = 80 + 43,3 = 123,3 N\nFnet² = Rx² + Fy² = 123,3² + 25²\nFnet = 125,81 N",     # the components added (direction slip)
        "Fx = 50 sin 30° = 25 N\nRx = 80 − 25 = 55 N\nFnet² = Rx² + Fy² = 55² + 25²\nFnet = 60,42 N",               # sin for cos
        "Fx = 50 cos 30° = 43,3 N\nRx = 80 − 43,3 = 36,7 N\nFnet² = Rx² + Fy² = 36,7² + 25²\nFnet = 1 971,89 N",    # the square root not taken
        "Fx = 50 cos 30° = 43,3 N\nRx = 80 − 43,3 = 36,7 N\nFnet² = Rx² + Fy² = 36,7² + 25²\nFnet = 44,41 N"], 3,  # the memo
        # (the unrounded components give 44,40 N, a value the memo accepts: never an option)
        ["Which way does the horizontal component of the 50 N point, compared with the 80 N?",
         "Once you have the net horizontal and vertical components, which theorem combines them?"],
        after=["2.2.1"]),   # the options show 2.2.1's Fy = 25 N
    work("2.2.3", "Calculate the direction of the resultant (net) force.", 2, [
        "tan θ = {80}/{25}\nθ = 72,65° from the vertical (Ry)",                          # the 80 N for Rx (a value from the wrong force)
        "tan θ = {36,7}/{25}\nθ = 55,74° from the vertical (Ry)",                        # the memo (OPTION 1; its diagram measures θ from Ry)
        "tan θ = {44,41}/{25}\nθ = 60,62° from the vertical (Ry)",                       # the resultant used as a side (wrong ratio)
        "tan θ = {36,7}/{25}\nθ = 0,97° from the vertical (Ry)"], 1,                     # the calculator in radians
        # (the memo also accepts ϕ = 90° − θ = 34,26° from the horizontal: no option shows 34,26°)
        ["Sketch the net horizontal and vertical components head to tail: where is the angle measured from the vertical?",
         "Which trigonometric ratio uses only the two components?"],
        after=["2.2.1", "2.2.2"]),   # the options show 2.2.1's 25 N and 2.2.2's Rx = 36,7 N and 44,41 N
]

# ---- QUESTION 3, the question paper page 8 and the memo page 4 ----
q3 = [
    rub("3.1", "Define the term kinetic frictional force.", 2, ["The force that opposes the motion of a moving object relative to a surface. (2)"],
        ["How is kinetic friction different from static friction?", "What does the box rub against as it moves?"], each=2,
        notes=["[2 or 0]"]),
    rub("3.2", "State Newton's First Law of Motion in words.", 2, [
        "A body will remain in its state of rest or motion at constant velocity (1) unless a non-zero resultant/net force acts on it (1)."],
        ["Which property of an object, its inertia, does this law describe?",
         "How is the First Law different from the Second Law, which links the net force to the acceleration?"], each=2,
        notes=["Penalise −1 if key words/phrase is omitted."]),
    work("3.3", "Calculate the magnitude of the horizontal component of the applied force.", 2, [
        "Fx = 90 sin 50°\nFx = 68,94 N",                                                 # sin for cos
        "Fx = {90}/{cos 50°}\nFx = 140,02 N",                                            # the formula upside down
        "Fx = 45(9,8) cos 50°\nFx = 283,47 N",                                           # the weight resolved (a value from the wrong force)
        "Fx = 90 cos 50°\nFx = 57,85 N"], 3,                                             # the memo (OR 90 sin 40°)
        ["Is the horizontal component the side next to the 50º angle or the side opposite it?",
         "Should the horizontal component be larger or smaller than the 90 N pull?"]),
    work("3.4", "Calculate the magnitude of the normal force.", 4, [
        "N = Fg + Fy\nN = 45(9,8) + 90 sin 50°\nN = 509,94 N",                           # the vertical component added (direction slip)
        "N = Fg − Fy\nN = 45(9,8) − 90 cos 50°\nN = 383,15 N",                           # the horizontal component for the vertical
        "N = Fg − Fy\nN = 45(9,8) − 90 sin 50°\nN = 372,06 N",                           # the memo
        "N = Fg\nN = 45(9,8)\nN = 441 N"], 2,                                            # the pull's vertical component left out
        ["The box does not move up or down: which vertical forces must balance?",
         "In which direction does the vertical component of the 90 N pull act?"],
        after=["3.3"]),   # the options set 90 sin 50° (vertical) against 90 cos 50°, 3.3's horizontal component
    work("3.5", "Calculate the coefficient of kinetic friction.", 4, [
        "fk = μkN\n372,06 = μk(57,85)\nμk = 6,43",                                       # the forces swapped (upside down)
        "fk = μkN\n57,85 = μk(372,06)\nμk = 0,16",                                       # the memo
        "fk = μkN\n90 = μk(372,06)\nμk = 0,24",                                          # the whole pull taken as the friction
        "fk = μkN\n57,85 = μk(45)\nμk = 1,29"], 1,                                       # the mass taken as the normal force (g left out)
        ["The box moves at constant velocity: how big is the friction compared with the horizontal component of the pull?",
         "Which equation links the kinetic friction, the coefficient and the normal force?"],
        after=["3.3", "3.4"]),   # the options show 3.3's 57,85 N and 3.4's 372,06 N
    rub("3.6", "Will the coefficient of kinetic friction change if the angle of the applied force is decreased? Write only YES or NO and give a reason.", 2, [
        "No (1)", "The coefficient is dependent on the (nature of) the surfaces / type of material in contact. (1)"],
        ["Which quantities does the coefficient of kinetic friction depend on?", "Which quantities change when the angle of the pull is decreased?"]),
]

# ---- QUESTION 4, the question paper page 9 and the memo page 5 ----
q4 = [
    rub("4.1", "State Newton's Second Law of Motion in words.", 2, [
        "When a resultant/net force acts on an object, the object will accelerate in the direction of the force. The acceleration is directly "
        "proportional to the net force (1) and inversely proportional to the mass of the object (1)."],
        ["Which quantities does the Second Law link to an object's acceleration?", "In which direction does an object accelerate when a net force acts on it?"],
        each=2, notes=["Penalise −1 if key words/phrase is omitted."]),
    work("4.2", "Calculate the gradient of the graph.", 3, [
        "Gradient = {2,5 − 0}/{1,25 − 0}\nGradient = 2",                                 # the memo (it accepts any set of coordinates)
        "Gradient = {1,25 − 0}/{2,5 − 0}\nGradient = 0,5",                               # upside down (Δx over Δy)
        "Gradient = {2,5 − 1,7}/{0,85 − 1,25}\nGradient = −2",                           # the points subtracted in opposite orders (a sign slip)
        "Gradient = {2,5 − 0}/{1,5 − 0}\nGradient = 1,67"], 0,                           # the point at 1,25 kg misread as 1,5 kg
        ["Which two points on the line can you read exactly from the grid?", "Which quantity is on the vertical axis, and which on the horizontal axis?"]),
    work("4.3", "Hence, determine the net force applied on the object during the experiment.", 2, [
        "Gradient = ma = Fnet = 2\nFnet = 2 N",                                          # the gradient taken as Fnet (upside down)
        "Fnet = ma = (1,25)(2,5)\nFnet = 3,13 N",                                        # the 1/a reading used as a
        "Gradient = a = 2 m·s⁻²\nFnet = ma = (1,25)(2) = 2,5 N",                         # the gradient taken as the acceleration
        "Gradient = {1}/{ma} = {1}/{Fnet} = 2\nFnet = {1}/{2} = 0,5 N"], 3,              # the memo (OPTION 1; its OPTION 2 also gives 0,5 N)
        ["Rearrange Fnet = ma to make 1/a the subject: what multiplies m?", "How is the gradient of this graph related to the net force?"],
        after=["4.2"]),   # the options show 4.2's gradient of 2
    rub("4.4", "Write down a conclusion for this experiment.", 2, [
        "Acceleration is inversely proportional to the mass of an object (if the net force is kept constant). (2)",
        "ACCEPT — The inverse of acceleration is directly proportional to the mass of the object (if the net force is kept constant) / 1/a ∝ m. (2)"],
        ["What shape is the graph, and where does it start?", "Which quantity was kept the same in every run of the experiment?"], each=2),
]

# ---- QUESTION 5, the question paper page 10 and the memo page 6 ----
q5 = [
    draw("5.1", "Draw a free-body diagram of ALL the forces acting on the crate while it moves from B to C.", 3, [
        ["Weight (w / Fg), OR both of its components, drawn and labelled", 1], ["Normal force (N / FN) drawn and labelled", 1],
        ["Friction (f / Ff) drawn and labelled", 1]],
        ["Which bodies touch or pull on the crate as it slides from B to C?", "What does a rough surface add that a smooth surface does not?"],
        memo="Any additional force: deduct 1 mark (maximum 2/3). Arrowheads omitted: deduct 1 mark (maximum 2/3). Lines must touch the object "
             "(otherwise maximum 2/3). Vectors need not be drawn to scale."),
    work("5.2", "Calculate the magnitude of the acceleration of the crate while it moves from A to B.", 4, [
        "Fnet = ma\nmg cos θ = ma\n25(9,8) cos 15° = 25a\na = 9,47 m·s⁻²",              # cos for sin (the perpendicular component)
        "Fnet = ma\nmg = ma\n25(9,8) = 25a\na = 9,80 m·s⁻²",                             # the whole weight, not its component along the slope
        "Fnet = ma\nmg sin θ = ma\n25(9,8) sin 15° = 25a\na = 2,54 m·s⁻²",              # the memo (OR 25(9,8) cos 75°)
        "Fnet = ma\nmg sin θ = ma\n25(9,8) sin 15° = a\na = 63,41 m·s⁻²"], 2,            # the mass left out on one side
        ["Which component of the weight acts along the slope?", "Is there any friction between A and B?"]),
    mcq("5.3", "Write down the direction of the acceleration of the crate while it slows down from B to C. Write only UP THE SLOPE or DOWN THE SLOPE.",
        ["Up the slope", "Down the slope"], 0,
        ["Which force acts on the crate from B to C that did not act from A to B?",
         "From B to C, which is larger: the friction or the component of the weight along the slope?"], marks=1),
    work("5.4", "The magnitude of the net acceleration from B to C is 1,2 m·s⁻². Calculate the magnitude of the frictional force acting on the crate.", 4, [
        "Fnet = ma\nFg∥ + (−f) = ma\n25(9,8) sin 15° − f = 25(1,2)\nf = 33,41 N",        # the sign of the acceleration dropped
        "Fnet = ma\nFg∥ + (−f) = ma\n25(9,8) sin 15° − f = 25(−1,2)\nf = 93,41 N",       # the memo (it accepts up the slope as positive too)
        "Fnet = ma\nFg∥ + (−f) = ma\n25(9,8) cos 15° − f = 25(−1,2)\nf = 266,65 N",      # cos for sin
        "Fnet = ma\n−f = ma\n−f = 25(−1,2)\nf = 30 N"], 1,                               # the component of the weight left out
        ["Which two forces act along the slope from B to C, and in which directions?",
         "If you take down the slope as positive, which way does the acceleration point while the crate slows down?"],
        after=["5.2", "5.3"]),   # the options show 5.2's 25(9,8) sin 15° and a negative acceleration (5.3's direction)
]

# ---- QUESTION 6, the question paper page 10 and the memo page 7 ----
q6 = [
    rub("6.1", "State Newton's Law of Universal Gravitation in words.", 2, [
        "Each particle in the universe attracts every other particle with a gravitational force that is directly proportional to the product of "
        "their masses (1) and inversely proportional to the square of the distance between their centres (1)."],
        ["Does the law apply only to planets, or to every pair of particles?", "What happens to the force between two objects when they move further apart?"],
        each=2, notes=["Penalise −1 if key words/phrase is omitted."]),
    work("6.2", "Calculate the mass of the probe.", 4, [
        "F = {Gm1m2}/{r²}\n3 338 = {(6,67 × 10⁻¹¹)(6,39 × 10²³)m}/{(3 390)²}\nm = 9,00 × 10⁻⁴ kg",        # the radius left in km
        "F = {Gm1m2}/{r²}\n3 338 = {(6,67 × 10⁻¹¹)(6,39 × 10²³)m}/{3 390 × 10³}\nm = 2,65 × 10⁻⁴ kg",     # r not squared
        "F = {Gm1m2}/{r²}\n3 338 = {(6,67 × 10⁻¹¹)(5,98 × 10²⁴)m}/{(3 390 × 10³)²}\nm = 96,17 kg",        # the Earth's mass (the wrong body)
        "F = {Gm1m2}/{r²}\n3 338 = {(6,67 × 10⁻¹¹)(6,39 × 10²³)m}/{(3 390 × 10³)²}\nm = 900 kg"], 3,     # the memo (its OR: 899,73 kg)
        ["In Newton's law, which value is the force, and which of the two masses is unknown?", "What is the radius of Mars in metres?"]),
    work("6.3", "Calculate the weight of the probe on Earth.", 2, [
        "w = mg\nw = 900(3,71)\nw = 3 339 N",                                            # Mars's g (the wrong planet)
        "w = {m}/{g}\nw = {900}/{9,8}\nw = 91,84 N",                                     # the formula upside down
        "w = mg\nw = 900(9,8)\nw = 8 820 N",                                             # the memo
        "w = mg\nw = 900(10)\nw = 9 000 N"], 2,                                          # g taken as 10, not the data sheet's 9,8
        ["Which value of g applies on Earth?", "Does the mass of the probe change when it moves from Mars to Earth?"],
        after=["6.2"]),   # the options show 6.2's 900 kg
]

# ---- QUESTION 7, the question paper page 11 and the memo pages 8-9 ----
q7a = [
    term("7.1", "Name the phenomenon described by the underlined words above (\"The light ray changes direction every time it passes into a new medium\").",
         ["Refraction"],
         ["What happens to the speed of light when it passes into a medium of a different optical density?",
          "Is the light bouncing back, or passing through and changing direction?"]),
    work("7.2", "If the refractive index of water and air is 1,33 and 1 respectively, calculate the angle θ between the light ray and the SURFACE OF "
         "THE WATER if the angle of refraction in the water is 40º.", 4, [
        "ni sin θi = nr sin θr\n1 sin θi = 1,33 sin 40°\nθi = 58,75°\nθ = θi = 58,75°",                 # the angle with the normal given as θ
        "ni sin θi = nr sin θr\n1 sin θi = 1,33 sin 40°\nθi = 58,75°\nθ = 90° − 58,75° = 31,25°",       # the memo (OPTION 1)
        "ni sin θi = nr sin θr\n1,33 sin θi = 1 sin 40°\nθi = 28,90°\nθ = 90° − 28,90° = 61,10°",       # the two indices swapped
        "ni sin θi = nr sin θr\n1 θi = 1,33 × 40°\nθi = 53,20°\nθ = 90° − 53,20° = 36,80°"], 1,        # the sines cancelled
        ["Is θ measured from the surface or from the normal, and which angle does Snell's law use?",
         "Which refractive index belongs to the medium the light comes from?"]),
    work("7.3", "The angle of refraction in the glass is 35º. Calculate the refractive index of glass.", 3, [
        "ni sin θi = nr sin θr\n1,33 sin 40° = nr sin 35°\nnr = 1,49",                   # the memo
        "ni sin θi = nr sin θr\n1 sin 40° = nr sin 35°\nnr = 1,12",                      # air's index for water's (the wrong medium)
        "ni sin θi = nr sin θr\n1,33 sin 35° = nr sin 40°\nnr = 1,19",                   # the two angles swapped
        "ni sin θi = nr sin θr\n1,33 sin 40° = nr sin 35°\nnr = 0,67"], 0,               # rearranged upside down
        # (1 sin 58,75° = nr sin 35° also gives 1,49: never an option)
        ["At the boundary between the water and the glass, what is the angle of incidence in the water?",
         "Which refractive index belongs to the medium the light comes from at that boundary?"],
        after=["7.2"]),   # the options show 7.2's substitution, 1,33 sin 40°
]
q7b = [
    draw("7.4", "Draw the sketch below and complete the diagram of the path of the light ray from the air to the water to the glass. Show ALL the values "
         "of the angles of incidence, angles of refraction and normal in EACH medium.", 5, [
        ["The light ray bends towards the normal in the water", 1], ["The light ray bends further towards the normal in the glass", 1],
        ["The angle of incidence, 58,75º, shown (OR 31,25º to the surface)", 1], ["The angles in the water (40º) shown", 1],
        ["The angle in the glass (35º) shown", 1]],
        ["At each boundary, does the light pass into an optically denser or a less dense medium?",
         "Where do you draw each normal, and which angles are measured from it?"],
        memo="If the normal lines are not indicated: penalise 1 mark. If the arrows are omitted: penalise 1 mark (maximum 4/5).",
        after=["7.2"]),   # its criteria show 7.2's 58,75º and 31,25º
    work("7.5", "Calculate the speed of light through the glass prism if the refractive index of glass is 1,5.", 3, [
        "n = {v}/{c}\n1,5 = {v}/{3 × 10⁸}\nv = 4,5 × 10⁸ m·s⁻¹",                         # the formula upside down
        "n = {c}/{v}\n1,33 = {3 × 10⁸}/{v}\nv = 2,26 × 10⁸ m·s⁻¹",                       # water's index (the wrong medium)
        "n = {c}/{v}\n1,5 = {340}/{v}\nv = 226,67 m·s⁻¹",                                # the speed of sound for c (the wrong constant)
        "n = {c}/{v}\n1,5 = {3 × 10⁸}/{v}\nv = 2 × 10⁸ m·s⁻¹"], 3,                       # the memo
        ["Which equation links a refractive index to the speed of light in the medium?", "Which value does the data sheet give for the speed of light in a vacuum?"]),
    mcq("7.6", "Is it possible that total internal reflection of the light ray can occur in the above situation? Write only YES or NO.", ["Yes", "No"], 1,
        ["Which two conditions are needed for total internal reflection?",
         "Compare the refractive indices of air, water and glass: in which order does the light meet them?"], marks=1),
]

# ---- QUESTION 8, the question paper page 12 and the memo pages 9-10 ----
q8a = [
    rub("8.1", "Define the term diffraction.", 2, [
        "Diffraction is the ability of a wave to spread out in wave fronts (1) as the wave passes through a small aperture or around a sharp edge (1)."],
        ["Which property of waves does the pattern on the screen show?", "How is diffraction different from refraction?"], each=2),
    rub("8.2", "Write an investigative question for this experiment.", 2, [
        "What is the relationship between the wavelength of a light ray and the degree of diffraction? (2)",
        "OR — How does a change in wavelength affect the degree of diffraction? (2)"],
        ["Which variable did the experimenters change, and which did they measure?",
         "How do you ask about the link between them so that the answer cannot be YES or NO?"], each=2,
        notes=["Criteria: the dependent (degree of diffraction) and independent (wavelength) variables stated correctly (1); the relationship asked "
               "as a question, not a statement, that cannot be answered YES or NO (1)."]),
]
q8b = [
    rub("8.3", "Write the mathematical relationship between wavelength and the degree of diffraction.", 2, [
        "Degree of diffraction is directly proportional to the wavelength. (2)", "OR — Degree of diffraction ∝ λ. (2)"],
        ["What happens to the degree of diffraction as the wavelength increases?",
         "What does the point where the graph starts tell you about the kind of relationship?"], each=2),
    mcq("8.4", "Which colour of light, RED or GREEN, has the largest degree of diffraction?", ["Red", "Green"], 0,
        ["Where do red and green light sit in the visible spectrum?", "Which way does the graph go as the wavelength increases?"], marks=1),
]
q8c = [
    draw("8.5", "Copy the set of axes below into your ANSWER BOOK and draw a graph showing the relationship between slit width and degree of diffraction.", 2, [
        ["The line shows inverse proportionality: the degree of diffraction falls as the slit width increases", 2]],
        ["Does a narrower or a wider slit spread the light out more?", "Which shape of graph matches the trend you found?"],
        memo="The memo's sketch: a curve that falls steeply at small slit widths and then levels off."),
]

# ---- QUESTION 9, the question paper page 13 and the memo pages 10-11 ----
q9 = [
    rub("9.1", "State Coulomb's law in words.", 2, [
        "The magnitude of the electrostatic force exerted by two point charges on each other is directly proportional to the product of the "
        "(magnitudes of the) charges (1) and inversely proportional to the square of the distance between them (1)."],
        ["Which law, about masses, has the same form as Coulomb's law?", "Does the law give the size of the force between the charges, or only its direction?"],
        each=2, notes=["Penalise −1 if key words/phrase is omitted.", "If learners refer to masses, no marks awarded."]),
    draw("9.2", "Draw a VECTOR DIAGRAM of the forces acting on sphere A. Indicate at least ONE angle.", 4, [
        ["Weight (w / Fg) drawn and labelled", 1], ["Tension (T / FT) drawn and labelled", 1], ["Electrostatic force (FE) drawn and labelled", 1],
        ["At least one angle (20º) indicated", 1]],
        ["Which three forces act on sphere A?", "Sphere A hangs at rest: what must the three forces add up to?"],
        memo="The memo accepts the three forces as a closed triangle (Fg down, FE horizontal, T along the string) OR drawn from one point."),
    work("9.3", "Calculate the magnitude of the electrostatic force that sphere B exerts on sphere A.", 4, [
        "F = {kQ1Q2}/{r²}\nF = {(9 × 10⁹)(8 × 10⁻⁹)(7 × 10⁻⁹)}/{0,03}\nF = 1,68 × 10⁻⁵ N",            # r not squared
        "F = {kQ1Q2}/{r²}\nF = {(9 × 10⁹)(8 × 10⁻⁹)(7 × 10⁻⁹)}/{3²}\nF = 5,60 × 10⁻⁸ N",             # r left in cm
        "F = {kQ1Q2}/{r²}\nF = {(9 × 10⁹)(8 × 10⁻⁹)(7 × 10⁻⁹)}/{0,03²}\nF = 5,60 × 10⁻⁴ N",          # the memo (OPTION 1)
        "F = {kQ1Q2}/{r²}\nF = {(6,67 × 10⁻¹¹)(8 × 10⁻⁹)(7 × 10⁻⁹)}/{0,03²}\nF = 4,15 × 10⁻²⁴ N"], 2,  # G for k (the wrong constant)
        # (the memo accepts all options: its OPTIONS 2 and 3, from the weight and the 20º angle, give 7,13 x 10⁻⁴ N: never an option)
        ["Which equation links two point charges and the distance between them?", "What is 3 cm in metres?"]),
    work("9.4", "Calculate the magnitude of the tension force in the string.", 3, [
        "Fg = mg = (0,2 × 10⁻³)(9,8) = 1,96 × 10⁻³ N\nT² = (1,96 × 10⁻³)² + (5,6 × 10⁻⁴)²\nT = 4,16 × 10⁻⁶ N",   # the square root not taken
        "Fg = mg = (0,2 × 10⁻³)(9,8) = 1,96 × 10⁻³ N\nT² = (1,96 × 10⁻³)² + (5,6 × 10⁻⁴)²\nT = 2,04 × 10⁻³ N",   # the memo (OPTION 1)
        "Fg = mg = (0,2 × 10⁻³)(9,8) = 1,96 × 10⁻³ N\nT = (1,96 × 10⁻³) + (5,6 × 10⁻⁴)\nT = 2,52 × 10⁻³ N",      # the forces added as numbers
        "Fg = mg = (0,2)(9,8) = 1,96 N\nT² = (1,96)² + (5,6 × 10⁻⁴)²\nT = 1,96 N"], 1,                            # 0,2 g not converted to kg
        # (the memo accepts all options: 2,09 x 10⁻³ N (Fg / sin 70°), 1,64 x 10⁻³ N (FE / cos 70°), and from 7,13 x 10⁻⁴ N 2,09 or 2,08 x 10⁻³ N:
        # none is an option)
        ["Which three forces act on sphere A, and how do they fit together when A is at rest?", "What is 0,2 g in kilograms?"],
        after=["9.3"]),   # the options show 9.3's 5,6 x 10⁻⁴ N
]

# ---- QUESTION 10, the question paper page 13 and the memo pages 12-13 ----
EF = "The magnitude of the electric field at point P is 4 x 10⁶ N·C⁻¹ and at point T the magnitude is 2,5 x 10⁵ N·C⁻¹. "
q10 = [
    draw("10.1", "Draw the electric field pattern around charge Q.", 2, [
        ["Shape of the field: at least 4 field lines, radial from the charge", 1], ["Direction of the field shown", 1]],
        ["Do electric field lines start or end on a positive charge?", "Can two field lines ever cross each other?"],
        memo="The memo's sketch: eight straight field lines pointing outwards, away from Q. Lines that do not touch the charge, or that cross: "
             "maximum 1/2."),
    mcq("10.2.1", EF + "Calculate the ratio of the electric field at point P to the electric field at point T. Write the answer as EP : ET.",
        ["16 : 1", "1 : 16", "4 : 1", "1,6 : 1"], 0,
        # the memo: 16 : 1, no working. The wrong ratios: turned round, its square root, a power of ten slipped (4 x 10⁶ / 2,5 x 10⁶)
        ["Which field is the stronger, and so which number in the ratio must be larger?", "How many powers of ten apart are the two field strengths?"],
        marks=1),
    work("10.2.2", EF + "Calculate the distance between charge Q and point P.", 4, [
        "EP : ET = 16 : 1\nE ∝ {1}/{r}, so rP : rT = 1 : 16\nr : (r + 3 mm) = 1 : 16\nr = 0,2 mm (0,0002 m)",     # the square left out
        "EP : ET = 16 : 1\nE ∝ {1}/{r²}, so rP : rT = 1 : 4\nr : 3 mm = 1 : 4\nr = 0,75 mm (0,00075 m)",         # 3 mm taken as Q to T
        "EP : ET = 16 : 1\nE ∝ {1}/{r²}, so rP : rT = 1 : 4\nr : (r + 3 mm) = 1 : 4\nr = 1 mm (0,001 m)",        # the memo (OPTION 1)
        "EP : ET = 16 : 1\nE ∝ r², so rP : rT = 4 : 1\nr : (r − 3 mm) = 4 : 1\nr = 4 mm (0,004 m)"], 2,         # direct, not inverse
        ["How does the field strength of a point charge depend on the distance from the charge?",
         "If P is r from Q, how far is T from Q, and how can you write the ratio of the two distances?"],
        after=["10.2.1"]),   # the options show 10.2.1's 16 : 1
    work("10.2.3", EF + "Calculate the magnitude of charge Q.", 2, [
        "E = {kQ}/{r²}\n4 × 10⁶ = {(9 × 10⁹)Q}/{(0,001)²}\nQ = 4,44 × 10⁻¹⁰ C",                                 # the memo (its OR, from T, agrees)
        "E = {kQ}/{r²}\n4 × 10⁶ = {(9 × 10⁹)Q}/{0,001}\nQ = 4,44 × 10⁻⁷ C",                                     # r not squared
        "E = {kQ}/{r²}\n4 × 10⁶ = {(9 × 10⁹)Q}/{(1)²}\nQ = 4,44 × 10⁻⁴ C",                                      # r left in mm
        "E = {kQ}/{r²}\n2,5 × 10⁵ = {(9 × 10⁹)Q}/{(0,001)²}\nQ = 2,78 × 10⁻¹¹ C"], 0,                           # T's field with P's distance
        ["Which equation gives the field strength at a distance r from a point charge?", "What is the distance from Q to P in metres?"],
        after=["10.2.2"]),   # the options show 10.2.2's 0,001 m
]

# ---- QUESTION 11, the question paper page 14 and the memo page 14 ----
FAST = "The coil is now rotated through an angle of 45º in 0,05 s. "
q11a = [
    rub("11.1", "State Faraday's law of electromagnetic induction in words.", 2, [
        "The magnitude of the induced emf across the ends of a conductor is directly proportional to the rate of change in the magnetic flux linkage "
        "with the conductor. (2)"],
        ["What must a conductor experience for an emf to be induced in it?", "Is this law about the size of the emf, or about the direction of the induced current?"],
        each=2, notes=["[2 or 0]"]),
    work("11.2", "Calculate the change in the magnetic flux.", 3, [
        "ε = {−ΔΦ}/{Δt}\n7 = {−ΔΦ}/{0,08}\nΔΦ = −0,56 Wb",                               # the number of windings left out
        "ε = {−NΔΦ}/{Δt}\n7 = {−400ΔΦ}/{0,08}\nΔΦ = −0,22 Wb",                           # rearranged wrongly (7 ÷ (400 x 0,08))
        "ε = {−NΔΦ}/{Δt}\n7 = {−400ΔΦ}/{0,05}\nΔΦ = −8,75 × 10⁻⁴ Wb",                    # the later time, 0,05 s (the wrong part)
        "ε = {−NΔΦ}/{Δt}\n7 = {−400ΔΦ}/{0,08}\nΔΦ = −1,4 × 10⁻³ Wb"], 3,                 # the memo
        ["Which equation links the emf, the number of windings and the change in flux?", "How long does the coil take to turn through 45º?"]),
    work("11.3", "Calculate the magnitude of the magnetic field.", 4, [
        "ΔΦ = AB(cos θf − cos θi)\n−0,0014 = (0,03)B(cos 45° − cos 0°)\nB = 0,16 T",                      # the side not squared for the area
        "ΔΦ = AB(cos θf − cos θi)\n−0,0014 = (3)²B(cos 45° − cos 0°)\nB = 5,31 × 10⁻⁴ T",                 # the side left in cm
        "ΔΦ = AB(cos θf − cos θi)\n−0,0014 = (0,03)²B(cos 45° − cos 0°)\nB = 5,31 T",                     # the memo
        "ΔΦ = NAB(cos θf − cos θi)\n−0,0014 = 400(0,03)²B(cos 45° − cos 0°)\nB = 1,33 × 10⁻² T"], 2,     # N counted a second time
        ["What is the area of the square coil in m²?", "What are the angles between the field and the normal to the coil before and after it turns?"],
        after=["11.2"]),   # the options show 11.2's −0,0014 Wb
    mcq("11.4", FAST + "How will the induced emf be affected? Write only INCREASE, DECREASE or STAY THE SAME.", ["Increase", "Decrease", "Stay the same"], 0,
        ["Is the change in flux the same as before?", "How does the time taken now compare with before?"], marks=1),
    rub("11.5", FAST + "Explain the answer to QUESTION 11.4.", 1, [
        "ε ∝ 1/Δt (1)", "OR — Emf is inversely proportional to time. If the time decreases, the emf will increase. (1)"],
        ["Which quantity in Faraday's law changed, and which stayed the same?", "Where does Δt appear in Faraday's law: on top or underneath?"],
        after=["11.4"]),   # its cards say the emf increases (11.4's answer; the memo marks 11.5 only after a right 11.4)
]
q11b = [
    mcq("11.6", "Which pole will be induced at point X? Write only NORTH or SOUTH.", ["North", "South"], 0,
        ["Which law gives the direction of an induced current?", "Does the solenoid help the approaching magnet in, or resist it?"], marks=1),
    mcq("11.7", "In which direction will the induced current flow? Write only FROM A TO B or FROM B TO A.", ["From A to B", "From B to A"], 0,
        ["Which pole must the current make at end X of the solenoid?",
         "Use the right-hand rule for a solenoid: which way must the current go round the coils to make that pole?"], marks=1),
]

# ---- QUESTION 12, the question paper page 15 and the memo pages 15-16 ----
SWAP = "The 4R resistor is replaced with an ammeter. "
q12 = [
    work("12.1", "Calculate the value of resistor R if the total resistance of the circuit is 4,8 Ω.", 3, [
        "Rs = R1 + R2\n4,8 = 4R + 6R\nR = 0,48 Ω",                                                       # the branches added in series
        "{1}/{Rp} = {1}/{R1} + {1}/{R2}\n{1}/{4,8} = {1}/{4R} + {1}/{6R}\nR = 2 Ω",                       # the memo (OPTION 1)
        "{1}/{Rp} = {1}/{R1} + {1}/{R2} + …\n{1}/{4,8} = {1}/{R} + {1}/{2R} + {1}/{3R} + {1}/{4R}\nR = 10 Ω",   # every resistor in parallel
        "{1}/{Rp} = {1}/{R1} + {1}/{R2}\n4,8 = {1}/{4R} + {1}/{6R}\nR = 0,09 Ω"], 1,                      # 4,8 not turned into 1/4,8
        ["Which resistors are in series with each other, and which branch is in parallel with the 4R resistor?",
         "How do you combine two resistances in parallel?"]),
    work("12.2", "Calculate the reading on the voltmeter if the current through the 4R resistor is 1,8 A.", 5, [
        "V4R = IR4R = 1,8(4)(2) = 14,4 V\nI6R = {V}/{R6R} = {14,4}/{12} = 1,2 A\nV2R = IR = 1,2(4) = 4,8 V",   # the memo (OPTION 1)
        "V4R = IR4R = 1,8(4)(1) = 7,2 V\nI6R = {V}/{R6R} = {7,2}/{6} = 1,2 A\nV2R = IR = 1,2(2) = 2,4 V",     # R's value (2 Ω) left out
        "V4R = IR4R = 1,8(4)(2) = 14,4 V\nI6R = I4R = 1,8 A\nV2R = IR = 1,8(4) = 7,2 V",                      # the same current in each branch
        "V4R = IR4R = 1,8(4)(2) = 14,4 V\nV2R = V4R (the 2R and 4R resistors taken as parallel)\nV2R = 14,4 V"], 0,   # 2R taken as parallel to 4R
        ["What is the potential difference across the 4R resistor, and which branch has the same potential difference?",
         "What current flows through the branch with R, 2R and 3R in it?"],
        after=["12.1"]),   # the options show 12.1's R = 2 Ω
    work("12.3", "Calculate the energy converted in resistor 4R in 2 minutes.", 3, [
        "W = I²RΔt\nW = (1,8)²(8)(2)\nW = 51,84 J",                                      # 2 minutes not converted to seconds
        "W = IRΔt\nW = (1,8)(8)(120)\nW = 1 728 J",                                      # I not squared
        "W = I²RΔt\nW = (1,8)²(4)(120)\nW = 1 555,2 J",                                  # the 4R resistor taken as 4 Ω
        "W = I²RΔt\nW = (1,8)²(8)(120)\nW = 3 110,4 J"], 3,                              # the memo's OPTION 1 (it prints 1 036,8 J: flagged)
        # (the memo's 1 036,8 J earns the marks too (Murci's ruling 2026-10-10): never an option)
        ["Which equation gives the energy converted from the current, the resistance and the time?", "What is 2 minutes in seconds?"],
        after=["12.1"]),   # the options show 12.1's 8 Ω (4R with R = 2 Ω)
    mcq("12.4", SWAP + "How will the reading on the voltmeter be influenced? Write only INCREASE, DECREASE or STAY THE SAME.",
        ["Increase", "Decrease", "Stay the same"], 1,
        ["What is the resistance of an ideal ammeter?", "Which path will the current take once the ammeter replaces the 4R resistor?"], marks=1),
    rub("12.5", SWAP + "Explain the answer to QUESTION 12.4.", 2, [
        "The ammeter has such a low resistance (1)", "It short circuits the parallel part and all current flows through the ammeter. (1)",
        "OR — The ammeter short circuits the resistors (1)", "OR — No current flows through resistor 2R (1)"],
        ["How does the resistance of an ammeter compare with that of the resistors?", "Which path does the current prefer when one path has almost no resistance?"],
        after=["12.4"]),   # its cards explain why the reading drops (12.4's answer; the memo marks 12.5 only after a right 12.4)
]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20, "lead": MC_LEAD, "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Vectors in two dimensions", "marks": 10,
     "lead": "Two forces, of magnitudes 50 N and 80 N, act at a point on a Cartesian plane in the directions shown in the sketch below.",
     "figure": fig("Q2", "A Cartesian grid. From the origin, an 80 N force points along the positive x-axis, and a 50 N force points up and to the "
                   "left, at 30º above the negative x-axis."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Forces and friction", "marks": 16,
     "lead": "A box, with a mass of 45 kg, is pulled with a force of 90 N at an angle of 50º to the horizontal. The box moves at a CONSTANT VELOCITY.",
     "figure": fig("Q3", "A 45 kg box on a horizontal surface, pulled by a 90 N force at 50º above the horizontal."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Mass and acceleration", "marks": 9,
     "lead": "Learners investigate the relationship between the mass of an object and the acceleration it experiences when a constant net force is "
             "applied on the object. They use their results to draw the graph below.",
     "figure": fig("Q4", "Graph of the inverse of acceleration versus mass: 1/a in (m·s⁻²)⁻¹, from 0 to 3, up against m in kg, from 0 to 1,5, "
                   "across, on graph paper, with four plotted points and a line drawn through them."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Motion on an incline", "marks": 12,
     "lead": "A crate, with a mass of 25 kg, slides down a plane which is inclined at 15º to the horizontal. During the first part of the motion, from "
             "A to B, there is no friction between the crate and the plane, but part BC has a rough surface.",
     "figure": fig("Q5", "A 25 kg crate at the top, A, of a plane inclined at 15º to the horizontal; B is part-way down the slope and C at the "
                   "bottom, and the part from B to C is marked as a rough surface."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Universal gravitation", "marks": 8,
     "lead": "The gravitational force on a probe, called Curiosity, on the surface of Mars is 3 338 N. The radius of Mars is 3 390 km and the mass of "
             "the planet is 6,39 x 10²³ kg.",
     "figure": fig("Q6", "A photograph of the Curiosity probe, a six-wheeled rover, on the surface of Mars."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Light in three media", "marks": 8,
     "lead": "A glass prism is placed at the bottom of a container filled with water. A light ray passes from the air through the water into the glass "
             "prism. The light ray changes direction every time it passes into a new medium.",
     "figure": fig("Q7a", "A container of water with a glass block at the bottom and air above the water; a light ray comes down through the air "
                   "and strikes the water surface, with the angle θ marked between the ray and the surface."), "items": q7a},
    {"id": "7.4", "title": "Question 7.4", "kind": "Ray path and speed", "marks": 9,
     "lead": "A glass prism is placed at the bottom of a container filled with water. A light ray passes from the air through the water into the glass "
             "prism.",   # (Question 7's own lead: the paper prints none before 7.4's sketch)
     "figure": fig("Q7b", "The sketch to complete: air, water and glass in layers separated by two horizontal lines, with a light ray in the air "
                   "that strikes the first line at the angle θ to the surface."), "items": q7b},
    {"id": "8", "title": "Question 8", "kind": "Diffraction of light", "marks": 4,
     "lead": "An experiment is performed to investigate the effect of wavelength on the degree of diffraction. Monochromatic light shines through a slit "
             "with a width of 0,002 mm and the pattern produced is shown on a screen.",
     "figure": fig("Q8a", "A monochromatic light ray passes through a slit to a screen, where a pattern of dark and bright bands forms."), "items": q8a},
    {"id": "8.3", "title": "Question 8.3", "kind": "Diffraction and wavelength", "marks": 3,
     "lead": "The degree of diffraction is recorded for different colours of monochromatic light and the results are shown on the graph below.",
     "figure": fig("Q8b", "A sketch graph of the degree of diffraction, up, against the wavelength in nm, across."), "items": q8b},
    {"id": "8.5", "title": "Question 8.5", "kind": "Diffraction and slit width", "marks": 2,
     "lead": "The experiment is repeated with only green light with a wavelength of 560 nm, but the slit width is changed and the degree of diffraction "
             "is recorded.",
     "figure": fig("Q8c", "A set of axes to copy: degree of diffraction up, against slit width in mm across."), "items": q8c},
    {"id": "9", "title": "Question 9", "kind": "Electrostatic forces", "marks": 13,
     "lead": "A small isolated sphere A, with a mass of 0,2 g, carrying a charge of +7 x 10⁻⁹ C, is suspended from a horizontal surface by a string of "
             "negligible mass. A second sphere B, carrying a charge of -8 x 10⁻⁹ C, on an isolated stand, attracts sphere A so that the string forms "
             "an angle of 20º to the vertical. The horizontal distance between the centres of the two spheres is 3 cm. Refer to the diagram below.",
     "figure": fig("Q9", "Sphere A, +7 x 10⁻⁹ C, hangs from a horizontal surface on a string at 20º to a dashed vertical line; sphere B, "
                   "−8 x 10⁻⁹ C, stands on an insulated stand 3 cm to the right of A."), "items": q9},
    {"id": "10", "title": "Question 10", "kind": "Electric fields", "marks": 9,
     "lead": "Two points, P and T, are situated 3 mm apart in the electric field of positive charge Q, as shown below.",
     "figure": fig("Q10", "Positive charge Q on the left, with points P and T to its right on one dotted line; a double arrow marks the 3 mm "
                   "between P and T."), "items": q10},
    {"id": "11", "title": "Question 11", "kind": "Electromagnetic induction", "marks": 11,
     "lead": "A SQUARE induction coil with a side length 3 cm and 400 windings, is placed perpendicularly in a uniform magnetic field and then rotated "
             "through an angle of 45º in 0,08 s.\n\nAn emf of 7 V is induced in the coil.",
     "figure": fig("Q11a", "A coil, seen edge-on as a thick line, between the N pole on the left and the S pole on the right of two magnets, with "
                   "dashed field lines from N to S passing through it."), "items": q11a},
    {"id": "11.6", "title": "Question 11.6", "kind": "Induction in a solenoid", "marks": 2,
     "lead": "The north pole of a bar magnet is pushed into a solenoid, as shown in the sketch below.",
     "figure": fig("Q11b", "A bar magnet, its N pole first, pushed from the left towards end X of a solenoid; the ends of the solenoid's wire are "
                   "labelled A, at the left, and B, at the right."), "items": q11b},
    {"id": "12", "title": "Question 12", "kind": "Electric circuits", "marks": 14,
     "lead": "Consider the circuit diagram below. The internal resistance of the battery and any resistance in the wires can be ignored.",
     "figure": fig("Q12", "A battery with a 4R resistor connected across it, in parallel with a branch of resistors R, 2R and 3R in series; a "
                   "voltmeter V is connected across the 2R resistor."), "items": q12},
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
    # 2 or 0: the wrong ones are static friction, the normal force, a force with the motion, ma, weight
    "3.1": (2, ["The force that opposes the motion of a moving object relative to a surface."],
               ["The force that opposes the tendency of motion of a stationary object relative to a surface.",
                "The force exerted by a surface on an object, perpendicular to the surface.", "The force that acts in the direction of motion of a moving object.",
                "The product of the mass of a moving object and its acceleration."]),
    # 2: the wrong ones are the second and third laws, acceleration for velocity, a moving body that always stops
    "3.2": (2, ["A body will remain in its state of rest or motion at constant velocity unless a non-zero resultant (net) force acts on it."],
               ["When a net force acts on an object, the object accelerates in the direction of the net force.",
                "When object A exerts a force on object B, object B simultaneously exerts an equal and opposite force on object A.",
                "A body will remain in its state of rest or motion at constant acceleration unless a non-zero resultant (net) force acts on it.",
                "A moving body always slows down and comes to rest unless a force keeps acting on it."]),
    # 2 ticks: the choice (No) beside its reason (the surfaces in contact; the memo's "/" form, the type of material, is the same reading)
    "3.6": (1, ["No, the coefficient of kinetic friction will not change.", "The coefficient of kinetic friction depends on the nature of the surfaces in contact."],
               ["Yes, the coefficient of kinetic friction will change.", "The coefficient of kinetic friction depends on the angle of the applied force.",
                "The coefficient of kinetic friction depends on the magnitude of the applied force.",
                "The coefficient of kinetic friction depends on the speed of the box."]),
    # 2: the wrong ones swap the proportions, reverse the direction, or are the first and third laws
    "4.1": (2, ["When a resultant (net) force acts on an object, the object will accelerate in the direction of the force. The acceleration is directly "
                "proportional to the net force and inversely proportional to the mass of the object."],
               ["When a resultant (net) force acts on an object, the object will accelerate in the direction of the force. The acceleration is inversely "
                "proportional to the net force and directly proportional to the mass of the object.",
                "When a resultant (net) force acts on an object, the object will accelerate in the direction opposite to the force. The acceleration is "
                "directly proportional to the net force and inversely proportional to the mass of the object.",
                "A body will remain in its state of rest or motion at constant velocity unless a non-zero resultant force acts on it.",
                "When object A exerts a force on object B, object B simultaneously exerts an equal and opposite force on object A."]),
    # 2, either form the memo accepts: the wrong ones are direct proportion, the net force for the mass, no relation, the inverse of 1/a ∝ m
    "4.4": (2, ["Acceleration is inversely proportional to the mass of an object, if the net force is kept constant.",
                "The inverse of acceleration is directly proportional to the mass of the object, if the net force is kept constant."],
               ["Acceleration is directly proportional to the mass of an object, if the net force is kept constant.",
                "Acceleration is inversely proportional to the net force, if the mass is kept constant.", "Acceleration does not depend on the mass of an object.",
                "The inverse of acceleration is inversely proportional to the mass of the object, if the net force is kept constant."]),
    # 2: the wrong ones drop the square, add the masses, swap the proportions, or are Coulomb's law
    "6.1": (2, ["Each particle in the universe attracts every other particle with a gravitational force that is directly proportional to the product of "
                "their masses and inversely proportional to the square of the distance between their centres."],
               ["Each particle in the universe attracts every other particle with a gravitational force that is directly proportional to the product of "
                "their masses and inversely proportional to the distance between their centres.",
                "Each particle in the universe attracts every other particle with a gravitational force that is directly proportional to the sum of their "
                "masses and inversely proportional to the square of the distance between their centres.",
                "Each particle in the universe attracts every other particle with a gravitational force that is inversely proportional to the product of "
                "their masses and directly proportional to the square of the distance between their centres.",
                "The force between two point charges is directly proportional to the product of the charges and inversely proportional to the square of "
                "the distance between them."]),
    # 2 ticks in one statement: the wrong ones are refraction, reflection, superposition, dispersion and travel through a vacuum
    "8.1": (2, ["Diffraction is the ability of a wave to spread out in wave fronts as the wave passes through a small aperture or around a sharp edge."],
               ["Diffraction is the change in direction of a wave as it passes from one medium into another.",
                "Diffraction is the bouncing back of a wave from a surface.", "Diffraction is the meeting of two waves at the same point, so that their amplitudes add.",
                "Diffraction is the splitting of white light into its colours by a prism."]),
    # 2, either of the memo's questions: the wrong ones name another variable, ask YES or NO, swap cause and effect, or make a statement
    "8.2": (2, ["What is the relationship between the wavelength of a light ray and the degree of diffraction?",
                "How does a change in wavelength affect the degree of diffraction?"],
               ["What is the relationship between the slit width and the degree of diffraction?", "Does the wavelength of light affect the degree of diffraction?",
                "How does the degree of diffraction affect the wavelength of light?", "The degree of diffraction increases as the wavelength increases."]),
    # 2, either form: the wrong ones are the inverse (in words and in symbols), no relation, the square
    "8.3": (2, ["The degree of diffraction is directly proportional to the wavelength.", "Degree of diffraction ∝ λ."],
               ["The degree of diffraction is inversely proportional to the wavelength.", "Degree of diffraction ∝ 1/λ.",
                "The degree of diffraction does not depend on the wavelength.", "The degree of diffraction is directly proportional to the square of the wavelength."]),
    # 2: the wrong ones use masses (the memo: no marks), drop the square, add the charges, swap the proportions
    "9.1": (2, ["The magnitude of the electrostatic force exerted by two point charges on each other is directly proportional to the product of the "
                "magnitudes of the charges and inversely proportional to the square of the distance between them."],
               ["The magnitude of the electrostatic force exerted by two point charges on each other is directly proportional to the product of their "
                "masses and inversely proportional to the square of the distance between them.",
                "The magnitude of the electrostatic force exerted by two point charges on each other is directly proportional to the product of the "
                "magnitudes of the charges and inversely proportional to the distance between them.",
                "The magnitude of the electrostatic force exerted by two point charges on each other is directly proportional to the sum of the "
                "magnitudes of the charges and inversely proportional to the square of the distance between them.",
                "The magnitude of the electrostatic force exerted by two point charges on each other is inversely proportional to the product of the "
                "magnitudes of the charges and directly proportional to the square of the distance between them.",
                "The magnitude of the electrostatic force between two point charges does not depend on the distance between them.",
                "Two point charges always attract each other, whatever the signs of their charges."]),   # (6 wrong cards: with four or five the
                # right card came first)
    # 2 or 0: the wrong ones drop "rate of change", make it inverse, are Lenz's law, or tie the emf to the time in the field
    "11.1": (2, ["The magnitude of the induced emf across the ends of a conductor is directly proportional to the rate of change in the magnetic flux "
                 "linkage with the conductor."],
                ["The magnitude of the induced emf across the ends of a conductor is directly proportional to the magnetic flux linkage with the conductor.",
                 "The magnitude of the induced emf across the ends of a conductor is inversely proportional to the rate of change in the magnetic flux "
                 "linkage with the conductor.",
                 "The induced current flows in a direction so that its magnetic field opposes the change that produced it.",
                 "The magnitude of the induced emf is directly proportional to the time for which the conductor stays in the magnetic field."]),
    # 1, either of the memo's forms: the wrong ones are direct proportion, the opposite trend, a bigger flux change, windings only
    "11.5": (1, ["The induced emf is inversely proportional to the time taken (ε ∝ 1/Δt).",
                 "Emf is inversely proportional to time: if the time decreases, the emf increases."],
                ["The induced emf is directly proportional to the time taken.", "If the time decreases, the induced emf decreases.",
                 "The change in magnetic flux is greater when the coil turns in a shorter time.",
                 "The induced emf depends only on the number of windings, not on the time taken."]),
    # 2 ticks: the memo's first reading (low resistance; it short-circuits the parallel part). Its OR reading (short-circuits the
    # resistors; no current through 2R) says the same: neither right nor wrong cards, so one point twice can never earn two marks
    "12.5": (1, ["The ammeter has a very low resistance.", "The ammeter short-circuits the parallel part, so all the current flows through the ammeter."],
                ["The ammeter has a very high resistance.", "More current now flows through resistor 2R.", "The total resistance of the circuit increases.",
                 "The ammeter adds resistance in series with the voltmeter."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, laws, a conclusion, a relationship and explanations), so SORTS stays empty and sort_ is kept for parity.
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

assert tuple(AUTHORED) == ("2.2.1", "2.2.2", "2.2.3", "3.3", "3.4", "3.5", "4.2", "4.3", "5.2", "5.4", "6.2", "6.3", "7.2", "7.3", "7.5", "9.3",
                           "9.4", "10.2.2", "10.2.3", "11.2", "11.3", "12.1", "12.2", "12.3"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == [], "no part is a one-value read-off"
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["2.1", "7.1"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["5.1", "7.4", "8.5", "9.2", "10.1"]
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]
assert PICKS == ["3.1", "3.2", "3.6", "4.1", "4.4", "6.1", "8.1", "8.2", "8.3", "9.1", "11.1", "11.5", "12.5"], PICKS

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2018", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic physics errors (a sign or direction slip, a value "
                                                       "from the wrong body or part, a formula upside down or with a factor dropped, a power of "
                                                       "ten slipped, a unit not converted, the wrong constant), 0 or full marks: " + ", ".join(AUTHORED) +
                                                       " (%d parts, %d marks). 10.2.1 ('Calculate the ratio', the memo's 16 : 1 with no working) "
                                                       "plays as an answer multiple choice: 16 : 1 beside the ratio turned round, its square root "
                                                       "and a power of ten slipped. 2.2.3's direction reads the memo's diagram (θ from the vertical, "
                                                       "Ry). A value the memo also accepts is never a wrong option: 2.2.2's 44,40 N (the unrounded "
                                                       "components), 2.2.3's ϕ = 34,26° (from the horizontal), 6.2's 899,73 kg (its OR), 7.3's route "
                                                       "1 sin 58,75° = nr sin 35°, 9.3's 7,13 x 10⁻⁴ N and 9.4's 2,09 / 2,08 / 1,64 x 10⁻³ N (its "
                                                       "'accept all possible options'), 12.3's 1 036,8 J (a memo slip)."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "12.3", "kind": "memo_issue", "detail": "The memo's OPTION 1 (memo page 16) writes W = 1,8²(8)(120) = 1036,8 J; 1,8² x 8 x 120 = 3 110,4 J, "
                                                      "which its own OPTIONS 2 and 3 give. The right option shows the memo's first working with "
                                                      "3 110,4 J; the memo's 1 036,8 J earns the marks too (Murci's ruling 2026-10-10), so it is never "
                                                      "a wrong option."},
        {"n": "9.3", "kind": "memo_issue", "detail": "The memo's OPTION 2 (memo page 11) writes FE = (1,96 x 10⁻³) tan 70° = 7,13 x 10⁻⁴ N; "
                                                     "(1,96 x 10⁻³) tan 70° = 5,39 x 10⁻³ N, and 7,13 x 10⁻⁴ N is (1,96 x 10⁻³) tan 20° (its OPTION 3 "
                                                     "agrees). The paper's own data disagree: Coulomb's law gives 5,60 x 10⁻⁴ N, the weight and the 20º "
                                                     "angle 7,13 x 10⁻⁴ N, and the memo accepts all options in 9.3 and 9.4. The right options follow "
                                                     "its OPTION 1 (Coulomb's law; 9.4 by Pythagoras, 2,04 x 10⁻³ N); no option shows another value it "
                                                     "accepts."},
        {"n": "1.8", "kind": "no_fit", "detail": "1.8's options are four printed arrows (A up and to the right, B down and to the left, C to the "
                                                 "right, D down), set apart from its sketch of the charges by the stem: they are typed as arrow "
                                                 "signs with their directions, in the paper's order, and the sketch is the question's figure."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 12), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (graphs, arrows, field sketches, circuits and the memo's fractions are images); "
                                                           "no API call."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions, laws, the conclusion, the "
                                                    "relationship and the investigative question (3.1, 3.2, 4.1, 4.4, 6.1, 8.1, 8.2, 8.3, 9.1, "
                                                    "11.1) pick one card for their 2 marks (an OR form the memo accepts is a second right card); 3.6 "
                                                    "picks the choice (No) and its reason, 1 mark each; 11.5 picks one of the memo's two forms for 1 "
                                                    "mark; 12.5 picks the memo's two points, 1 mark each, its OR reading (short-circuits the "
                                                    "resistors; no current through 2R) neither a right nor a wrong card, so one point twice can "
                                                    "never earn two marks." % len(PICKS)},
        {"n": "5.1", "kind": "no_fit", "detail": "Drawings (5.1's free-body diagram, 7.4's ray diagram, 8.5's graph, 9.2's vector diagram, 10.1's field "
                                                 "pattern) are done on paper and self-checked against the memo's criteria."},
    ],
}
QTOTAL = {"1": 20, "2": 10, "3": 16, "4": 9, "5": 12, "6": 8, "7": 17, "8": 9, "9": 13, "10": 9, "11": 13, "12": 14}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's ten printed letters are the paper's (A2 B3 C3 D2) and seven printed choices of two or three (5.3 A, 7.6 B,
# 8.4 A, 11.4 A, 11.6 A, 11.7 A, 12.4 B) can never be C or D, so an even paper needs C- and D-heavy workings: the 24 workings sit at A4 B6
# C7 D7 and 10.2.1 at A, the 35 four-option questions at A7 B9 C10 D9 and the whole paper at A12 B11 C10 D9 (within 3 of even)
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
    "2.2.2": ["2.2.1"], "2.2.3": ["2.2.1", "2.2.2"], "3.4": ["3.3"], "3.5": ["3.3", "3.4"], "4.3": ["4.2"], "5.4": ["5.2", "5.3"], "6.3": ["6.2"],
    "7.3": ["7.2"], "7.4": ["7.2"], "9.4": ["9.3"], "10.2.2": ["10.2.1"], "10.2.3": ["10.2.2"], "11.3": ["11.2"], "11.5": ["11.4"],
    "12.2": ["12.1"], "12.3": ["12.1"], "12.5": ["12.4"]}, {i["n"]: i.get("after") for i in ITEMS if i.get("after")}
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 12 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
