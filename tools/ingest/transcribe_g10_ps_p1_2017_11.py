"""Grade 10 Physical Sciences P1 (Physics) Nov 2017 (DBE common paper), the whole paper (Questions 1 to 11), hand-transcribed into the
catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options,
marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API
call: the transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets the 1.2 graphs, the
1.3 oil drops and the circuits as images, and the memo sets its fractions and its 8.2.2 working as images, so the text layers have gaps.

  python tools/ingest/transcribe_g10_ps_p1_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Physical Sciences P1 Nov 2017 Eng.pdf" "uploads/Grade 10 Physical Sciences P1 Nov 2017 MG Eng & Afr.pdf" --id g10-ps-p1-2017-11 --from-json

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; models: transcribe_ps_p1_2025_11.py and the Grade 10 pilot
transcribe_g10_ps_p1_2018_11.py):
  multiple choice printed in the paper -> mcq as printed (options printed as a table -> optTable; graph options -> the figure and
  "Graph A".."Graph D"); a choice printed in the stem with no explanation in the same part (6.5 "INCREASES, DECREASES or REMAINS THE
  SAME", 10.2 "GAIN or LOSE") -> mcq of the printed choices. One term the memo names -> term (3.1, 3.2.1, 3.2.2, 6.3, 8.1.1, 8.1.2);
  one read-off value with no working -> num (9.3.2, 9.3.3, 11.3.1).
  Every calculation ("Calculate", "Determine", 7.3's "How far apart ...?" whose memo shows a working) -> authored multiple choice,
  `work`: the memo's FIRST working line by line and three workings each built from a DIFFERENT realistic error (a sign slip, a value
  from the wrong body or part, a formula upside down or with a factor dropped, a power of ten slipped, a unit not converted, the wrong
  constant), every number recomputed; 0 or full marks. A value the memo also accepts (its positive marking from a rounded value) is
  never a wrong option; where the memo's own value is a slip the paper contradicts (8.2.2, 10.3) the right option uses the paper's
  value and the memo's value is never a wrong option (Murci's ruling 2026-10-10).
  A definition or law -> statements (pick 1 card for its marks; an OR form a second right card); an explanation the memo ticks point
  by point -> statements, 1 mark a point; a choice with its reasons (3.6, 11.4) -> the choice a card beside its reasons. No memo
  here weighs two sides, so no part plays as a sort.
  "Draw / Use a vector scale diagram" -> draw with the memo's criteria (self-checked, flagged no_fit).
  A part whose options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose stem or diagram changes part-way is two missions (4 and 4.3; 9 and 9.3; 10 and 10.4).
Figure boxes are measured in PDF points (page 595.32 x 841.92, read from the PDF) from the drawings and images themselves and checked
on a contact sheet (scratchpad lower/g10-ps-p1-2017-11/figs.py)."""
import json
import random
import re
from pathlib import Path

PID = "g10-ps-p1-2017-11"
W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.2": [3, 98.0, 354.0, 524.0, 477.0], "1.3": [3, 102.0, 536.0, 511.5, 571.0], "Q2": [6, 47.0, 183.0, 530.0, 390.0],
    "Q4": [8, 53.0, 318.0, 522.0, 429.0], "Q5": [9, 152.0, 159.0, 461.0, 346.0], "Q6": [10, 57.0, 163.0, 547.0, 324.0],
    "Q8": [11, 47.0, 141.0, 523.0, 284.0], "Q9a": [12, 148.0, 146.0, 410.0, 192.0], "Q9b": [12, 90.0, 325.0, 470.0, 576.0],
    "Q10": [13, 229.0, 285.0, 407.0, 337.0], "Q11": [14, 70.0, 149.0, 523.0, 410.0]}


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


# ---- QUESTION 1: multiple choice, the question paper pages 3-5 and the memo page 2 ----
q1 = [
    mcq("1.1", "Which ONE of the following pairs of physical quantities consists of one scalar and one vector quantity?",
        ["Distance and speed", "Speed and acceleration", "Displacement and velocity", "Velocity and acceleration"], 1,
        ["Which of the quantities in the options need a direction to be described fully?",
         "Which quantities describe only how far or how fast, with no direction?"]),
    mcq("1.2", "A car is travelling at a constant velocity along a straight road. It then slows down uniformly. Which ONE of the velocity-time "
        "graphs below best represents the motion of the car?", ["Graph A", "Graph B", "Graph C", "Graph D"], 2,
        ["What does a horizontal line on a velocity-time graph tell you about the velocity?",
         "If the velocity decreases at a constant rate, what shape and slope does that part of the graph have?"],
        figure=fig("1.2", "Four velocity-time graphs, A to D, each with v up and t across. A: a straight line rising from the origin. B: a horizontal "
                   "line, then a straight line rising. C: a horizontal line, then a straight line falling. D: a horizontal line.")),
    mcq("1.3", "Oil dripping from a truck at equal time intervals leaves the pattern below on the road. If the truck is moving eastwards, which ONE "
        "of the combinations below best describes the speed of the truck during the intervals M to Q, Q to V and V to Z?",
        ["Decreases; Remains constant; Increases", "Increases; Remains constant; Decreases", "Remains constant; Increases; Increases",
         "Increases; Decreases; Remains constant"], 0,
        ["The drops fall at equal time intervals: what does a bigger gap between two drops tell you about the speed?",
         "Look at the gaps from M to Q, from Q to V and from V to Z: how does each set of gaps change?"],
        optTable={"head": ["M TO Q", "Q TO V", "V TO Z"],
                  "rows": [["Decreases", "Remains constant", "Increases"], ["Increases", "Remains constant", "Decreases"],
                           ["Remains constant", "Increases", "Increases"], ["Increases", "Decreases", "Remains constant"]]},
        figure=fig("1.3", "A row of oil drops on a road, labelled M, N, O, P, Q, R, S, T, U, V, W, X, Y and Z from left to right, beside an arrow "
                   "pointing east.")),
    mcq("1.4", "A motorbike moving at a speed v, has a kinetic energy E. If the speed of the motorbike increases to 3v, the kinetic energy will be …",
        ["3E", "⅓E", "6E", "9E"], 3,
        ["Which formula gives the kinetic energy of an object?", "In that formula, to which power is the speed raised?"]),
    mcq("1.5", "The SI unit for gravitational potential energy is …", ["kg·m·s⁻¹", "kg·m·s⁻²", "kg·m²·s⁻²", "kg·m⁻¹·s⁻¹"], 2,
        ["Which formula gives the gravitational potential energy?", "What are the SI units of mass, of the gravitational acceleration and of height?"]),
    mcq("1.6", "The amplitude of a sound wave is increased without changing the frequency. How does this change affect the loudness and pitch of the sound?",
        ["Decreases; Decreases", "Decreases; Increases", "Increases; Unchanged", "Increases; Increases"], 2,
        ["Which property of a sound wave decides its loudness?", "Which property decides its pitch, and was that property changed?"],
        optTable={"head": ["LOUDNESS", "PITCH"],
                  "rows": [["Decreases", "Decreases"], ["Decreases", "Increases"], ["Increases", "Unchanged"], ["Increases", "Increases"]]}),
    mcq("1.7", "Which ONE of the combinations below is the CORRECT order of electromagnetic waves in INCREASING WAVELENGTHS?",
        ["Gamma ray → X-ray → ultraviolet → visible light → infrared → microwave",
         "Radio wave → microwave → infrared → visible light → ultraviolet → X-ray",
         "X-ray → ultraviolet → infrared → visible light → radio wave → microwave",
         "Gamma ray → X-ray → visible light → ultraviolet → infrared → microwave"], 0,
        ["Which electromagnetic waves have the shortest wavelengths, and which the longest?",
         "Check each order one step at a time: does every arrow lead to a longer wavelength?"]),
    mcq("1.8", "The force between two magnets decreases when …",
        ["two like poles come closer together.", "two unlike poles come closer together.", "the distance between them increases.",
         "the distance between them decreases."], 2,
        ["How does the force between two magnets change as they move apart?",
         "Does it matter for the size of the force whether the poles are alike or unlike?"]),
    mcq("1.9", "Two identical spheres, X and Y, on insulated stands, carry charges of 3 µC and −5 µC respectively. The spheres are brought into contact "
        "with each other and returned to their original positions. The charge on EACH sphere after contact is …",
        ["8 µC", "−4 µC", "−2 µC", "−1 µC"], 3,
        ["What is the total charge of the two spheres before they touch?", "How do two identical spheres share their total charge when they touch?"]),
    mcq("1.10", "The energy transferred per unit electric charge in a circuit is …", ["current.", "charge.", "power.", "potential difference."], 3,
        ["What is the unit of energy, and what is the unit of charge?", "Which of the quantities in the options is measured in joules per coulomb?"]),
]

# ---- QUESTION 2, the question paper page 6 and the memo page 3 ----
q2 = [
    rub("2.1", "Define the term average speed.", 2, [
        "The total distance travelled per total time. (2)", "OR — The distance travelled divided by the total time. (2)"],
        ["Is average speed a scalar or a vector?", "Does it depend on the path an object takes, or only on where it starts and ends?"], each=2),
    work("2.2", "Calculate the average speed of the girl from the school to her home.", 4, [
        "Average speed = {distance travelled}/{time taken}\n= {500 + 800}/{30}\n= 43,33 m·s⁻¹",                  # the minutes not converted
        "Average speed = {distance travelled}/{time taken}\n= {500 + 800}/{30 × 60}\n= 0,72 m·s⁻¹",              # the memo
        "Average speed = {distance travelled}/{time taken}\n= {800}/{30 × 60}\n= 0,44 m·s⁻¹",                    # only the last 800 m (wrong part)
        "Average speed = {time taken}/{distance travelled}\n= {30 × 60}/{500 + 800}\n= 1,38 m·s⁻¹"], 1,          # the formula upside down
        ["How far does the girl walk in total from the school to her home?", "How many seconds are there in 30 minutes?"]),
    # (2026-10-11: NOT a force diagram, so not built with "forces": the memo marks three displacements head to tail, each "line, arrow AND
    # 500 m / 800 m / 1 300 m", drawn to the scale 1 cm = 100 m; the force builder's arrows start at one dot, carry force names, not
    # magnitudes, and their length is not marked. It stays self-checked until a vector scale-diagram builder exists)
    draw("2.3", "Use a vector scale diagram and represent the displacement of the boy from the time he realised he left his book at school until he "
         "reached home. Include ALL relevant information in the diagram. Use scale 1 cm = 100 m for the diagram.", 3, [
        ["A line with an arrow, labelled 500 m, pointing west: from where he turned back to the school (5 cm)", 1],
        ["A line with an arrow, labelled 800 m, pointing east: his displacement from where he turned back to home (8 cm)", 1],
        ["A line with an arrow, labelled 1 300 m, pointing east: from the school to home (13 cm)", 1]],
        ["Which way does the boy walk after he realises he left his book, and how far?", "With 1 cm = 100 m, how long must each arrow be?"],
        memo="The memo's diagram: a 500 m arrow pointing west back to the school, a 1 300 m arrow from the school east to home, and a dashed 800 m "
             "arrow east from where he turned back to home."),
    work("2.4", "If the average speed of the boy is the same as that of the girl, calculate how long it would take the boy to reach home from the time "
         "they both left the school together.", 4, [
        "Average speed = {distance travelled}/{time taken}\n0,72 = {1 300}/{time taken}\nt = 1 805,56 s",                    # the displacement, not the distance
        "Average speed = {distance travelled}/{time taken}\n0,72 = {500 + 1 300}/{time taken}\nt = 2 500 s",                 # the walk back left out
        "Average speed = {distance travelled}/{time taken}\n0,72 = {500 + 500 + 1 300}/{time taken}\nt = (0,72)(2 300) = 1 656 s",  # multiplied
        "Average speed = {distance travelled}/{time taken}\n0,72 = {500 + 500 + 1 300}/{time taken}\nt = 3 194,44 s"], 3,    # the memo
        # (the memo marks positively from 2.2 and uses the rounded 0,72; the unrounded 13/18 m·s⁻¹ gives 3 184,62 s, never an option)
        ["Which stretches does the boy walk from the moment they leave school until he gets home?",
         "His average speed equals the girl's: which formula then gives the time?"],
        after=["2.2", "2.3"]),   # the options show 2.2's 0,72 m·s⁻¹ and 2.3's 500 m and 1 300 m legs
]

# ---- QUESTION 3, the question paper page 7 and the memo pages 4-5 ----
q3 = [
    term("3.1", "Give the correct term for change of position per unit time.", ["Velocity", "Average velocity"],
         ["Is change of position a vector or a scalar?", "What is the SI unit of change of position per unit time?"]),
    term("3.2.1", "For this test, write down the independent variable.", ["Time"],
         ["Which quantity did the engineers set in equal steps?", "Is it the cause or the effect?"]),
    term("3.2.2", "For this test, write down the dependent variable.", ["Position", "Change in position"],
         ["Which quantity was measured at each of those moments?", "Is it the cause or the effect?"]),
    # BUILT on a grid (2026-10-11, build "plot"): the memo's mark allocation (memo page 4) as the learner's choices. Its axes' labels from
    # one list for both axes (1 + 1); the five points of the table placed and joined by a line (2: the memo gives no split, so all five
    # earn 2 and three or four 1, our reading); the shape (1): a straight line through the origin (a straight line, or the points joined
    # or a smooth curve through five points that lie on one line through (0 ; 0)). The memo does not mark a scale: the grid is the memo's
    # (1 s and 5 m a big square, five small squares in each), so the answer sheet's blank graph paper is given its numbers.
    {**draw("3.3", "Use the information in the table above and draw an accurate position-time graph on the graph paper on the attached ANSWER SHEET.", 5, [
        ["1 x correct y-axis label and unit: position / change in position (m)", 1], ["1 x correct x-axis label and unit: time (s)", 1],
        ["2 x points plotted and joined", 2], ["1 x shape of graph: a straight line through the origin", 1]],
        ["Which quantity goes on each axis of a position-time graph, and in which units?",
         "Plot the five (time; position) pairs: do they lie on a straight line or on a curve?"],
        memo="The memo's graph plots (0 s; 0 m), (1 s; 5 m), (2 s; 10 m), (3 s; 15 m) and (4 s; 20 m) and joins them.",
        after=["3.2.1", "3.2.2"]),   # its axis criteria show the independent (time) and dependent (position) variables
     "build": {"kind": "plot", "x": {"min": 0, "max": 8, "step": 1, "minor": 0.2, "snap": 0.2}, "y": {"min": 0, "max": 35, "step": 5, "minor": 1, "snap": 0.5},
               "labels": ["Position (m)", "Position (s)", "Time (s)", "Time (m)", "Velocity (m·s⁻¹)"], "xl": "Time (s)", "yl": "Position (m)",
               "points": [{"id": "t%d" % t, "name": "t = %d s" % t, "at": [t, 5 * t]} for t in range(5)], "tol": [0.1, 0.5],
               "tests": [{"k": "yl"}, {"k": "xl"}, {"k": "points", "joined": True, "part": [[3, 1]]},
                         {"k": "shape", "kinds": ["best", "join", "curve"], "straight": True, "through": [0, 0]}]}},
    work("3.4", "Calculate the gradient of the graph.", 4, [
        "Gradient = {Δy}/{Δx}\n= {20 − 5}/{4 − 1}\n= 5 m·s⁻¹",                      # the memo
        "Gradient = {Δx}/{Δy}\n= {4 − 1}/{20 − 5}\n= 0,20 m·s⁻¹",                   # the formula upside down
        "Gradient = {Δy}/{Δx}\n= {20 − 5}/{4 − 0}\n= 3,75 m·s⁻¹",                   # the 5 m point's time taken as 0 (a point misread)
        "Gradient = {Δy}/{Δx}\n= {20 − 5}/{4 − 1}\n= 5 m·s⁻²"], 0,                  # the unit of acceleration (the gradient taken as acceleration)
        ["Which two points on the line will you use, and what are their coordinates?",
         "Which quantity is on the vertical axis, and which on the horizontal axis?"],
        after=["3.3"]),   # the options show the line's points and one gradient for all of it (3.3's straight line)
    draw("3.5", "Draw (NOT to scale) a corresponding velocity-time graph for the motion of the car. Labels the axes.", 2, [
        ["Both axes labelled: velocity (m·s⁻¹) up and time (s) across", 1], ["A horizontal straight line at 5 m·s⁻¹", 1]],
        ["What does the gradient of a position-time graph give you?", "If that gradient is the same everywhere, what shape does the velocity-time graph have?"],
        memo="The memo's sketch: velocity (m·s⁻¹) up and time (s) across, a horizontal line at 5 m·s⁻¹.",
        after=["3.4"]),   # its criteria show 3.4's 5 m·s⁻¹
    rub("3.6", "Hence, deduce the magnitude of the acceleration of the car.", 2, [
        "The car has zero acceleration (1)", "as its velocity is constant (1)"],
        ["How does the velocity change during the motion?", "What does the gradient of a velocity-time graph give you?"],
        after=["3.5"]),   # its right cards (the velocity is constant) show 3.5's horizontal line
]

# ---- QUESTION 4, the question paper page 8 and the memo pages 5-6 ----
q4a = [
    rub("4.1", "Define the term acceleration.", 2, ["Rate (1) of change of velocity (1)."],
        ["Think of a car speeding up: which of its quantities is changing?", "How is acceleration different from velocity?"], each=2),
    work("4.2.1", "Calculate the distance covered by the car.", 3, [
        "Δx = viΔt + ½aΔt²\nΔx = 0(2) + ½(15)(2)\nΔx = 15 m",                       # Δt not squared
        "Δx = viΔt + aΔt²\nΔx = 0(2) + (15)(2)²\nΔx = 60 m",                         # the ½ left out
        "Δx = viΔt + ½aΔt²\nΔx = 0(2) + ½(15)(2)²\nΔx = 30 m",                       # the memo
        "Δx = viΔt + ½aΔt²\nΔx = 0(2) + ½(15 × 2)²\nΔx = 450 m"], 2,                 # a and Δt squared together
        ["What is the car's initial velocity if it starts from rest?", "Which equation of motion links Δx, vi, a and Δt?"]),
    work("4.2.2", "Calculate the velocity of the car.", 3, [
        "vf² = vi² + aΔx\nvf² = 0² + (15)(30)\nvf = 21,21 m·s⁻¹ to the right",       # the 2 left out of the formula
        "vf² = vi² + 2aΔx\nvf² = 0² + 2(15)(30)\nvf = 30 m·s⁻¹ to the right",        # the memo (OPTION 1; its OPTION 2, vf = vi + aΔt, also 30)
        "vf² = vi² + 2aΔx\nvf² = 0² + 2(15)(30)\nvf = 900 m·s⁻¹ to the right",       # the square root not taken
        "vf² = vi² + 2aΔx\nvf² = 0² + 2(15)(2)\nvf = 7,75 m·s⁻¹ to the right"], 1,   # the 2 s put in for Δx (a value from the wrong part)
        ["Which equation of motion gives vf from vi, a and Δx, or from vi, a and Δt?", "Velocity is a vector: what must your answer include besides its size?"],
        after=["4.2.1"]),   # the options show 4.2.1's 30 m
]
q4b = [
    rub("4.3", "Explain the meaning of a safe 2-second following distance.", 2, [
        "When following a car, a motorist should keep a safe distance such that it takes more than 2 s (1) to reach the same position (1) as the car "
        "in front.", "OR — The car will need 2 s to stop in an emergency and not hit the car in front. (2)"],
        ["What could happen if the car in front stops suddenly?", "How can the gap behind a vehicle be measured in seconds instead of metres?"], each=2),
    work("4.4", "Calculate the safe 2-second following distance behind the truck.", 6, [
        "v = {90 × 10³}/{3600} = 25 m·s⁻¹\nΔx = viΔt + ½aΔt²\nΔx = (25)(2) + ½(0)(2)²\nΔx = 50 m",                    # the memo (OPTION 1)
        "v = 90 × 3,6 = 324 m·s⁻¹\nΔx = viΔt + ½aΔt²\nΔx = (324)(2) + ½(0)(2)²\nΔx = 648 m",                           # converted the wrong way (x 3,6)
        "v = {90}/{3600} = 0,025 m·s⁻¹\nΔx = viΔt + ½aΔt²\nΔx = (0,025)(2) + ½(0)(2)²\nΔx = 0,05 m",                   # km not changed to m (10³ dropped)
        "v = {(108 − 90) × 10³}/{3600} = 5 m·s⁻¹\nΔx = viΔt + ½aΔt²\nΔx = (5)(2) + ½(0)(2)²\nΔx = 10 m"], 0,         # the difference in speed used
        # (no option uses the car's own 30 m·s⁻¹: 60 m is the 2-second rule read from the follower's speed, which the memo does not use
        # but a learner could defend, so it is neither right nor wrong here)
        ["How do you change 90 km·h⁻¹ into m·s⁻¹?", "At a constant velocity, how far does the truck move in 2 s?"]),
    work("4.5", "Calculate how long it will take the motorist to get to a safe 2-second following distance behind the truck.", 5, [
        "v(car) = {108 × 10³}/{3600} = 30 m·s⁻¹\nDifference in speed: 30 + 25 = 55 m·s⁻¹\nDistance to close: 80 − 50 = 30 m\n"
        "distance = (v)(t): 30 = (55)(t)\nt = 0,55 s",                                  # the speeds added (vehicles taken as moving towards each other)
        "v(car) = {108 × 10³}/{3600} = 30 m·s⁻¹\nDifference in speed: 30 − 25 = 5 m·s⁻¹\nDistance to close: 80 m\n"
        "distance = (v)(t): 80 = (5)(t)\nt = 16 s",                                     # the whole gap, the safe distance not taken off (wrong part)
        "v(car) = {108 × 10³}/{3600} = 30 m·s⁻¹\nDifference in speed: 30 − 25 = 5 m·s⁻¹\nDistance to close: 80 − 50 = 30 m\n"
        "distance = (v)(t): t = {5}/{30}\nt = 0,17 s",                                  # rearranged upside down
        "v(car) = {108 × 10³}/{3600} = 30 m·s⁻¹\nDifference in speed: 30 − 25 = 5 m·s⁻¹\nDistance to close: 80 − 50 = 30 m\n"
        "distance = (v)(t): 30 = (5)(t)\nt = 6 s"], 3,                                  # the memo
        ["How much faster than the truck is the car moving, in m·s⁻¹?", "How much of the 80 m gap must the car close to be at the safe distance?"],
        after=["4.4"]),   # the options show 4.4's 25 m·s⁻¹ and 50 m
]

# ---- QUESTION 5, the question paper page 9 and the memo pages 6-7 ----
q5 = [
    rub("5.1", "Define the term kinetic energy.", 2, ["The energy an object has as a result of its motion. (2)"],
        ["Which formula gives kinetic energy, and which quantities are in it?", "What happens to an object's kinetic energy when it stops?"], each=2),
    work("5.2", "The man and his gear have a mass of 72 kg. Calculate the gravitational potential energy of the man just before he jumps from the sky bridge.", 3, [
        "Ep = mgh\nEp = 72 × 100\nEp = 7 200 J",                                     # g left out
        "Ep = mgh\nEp = 72 × 9,8 × 100\nEp = 70 560 J",                              # the memo
        "Ep = ½mgh\nEp = ½ × 72 × 9,8 × 100\nEp = 35 280 J",                         # the ½ of Ek put in (wrong formula)
        "Ep = mgh\nEp = 72 × 10 × 100\nEp = 72 000 J"], 1,                           # g taken as 10, not the data sheet's 9,8
        ["Which formula gives the gravitational potential energy?", "How high is the sky bridge, and which value of g does the data sheet give?"]),
    rub("5.3", "State the law of conservation of mechanical energy.", 2, [
        "The sum of the gravitational potential energy and kinetic energy (1) in an isolated system is constant (1).",
        "OR — The total mechanical energy of an isolated system remains constant. (2)"],
        ["Which two energies make up mechanical energy?",
         "What kind of system does the law need: one where air resistance acts, or one on which no external forces act?"], each=2),
    work("5.4", "Use the law in QUESTION 5.3 to calculate the velocity of the man at a height of 50 m above the ground.", 5, [
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n70 560 = (72)(9,8)(50) + ½ × 72 × v²\nv = 31,30 m·s⁻¹",   # the memo (31,3)
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + mv²\n70 560 = (72)(9,8)(50) + 72 × v²\nv = 22,14 m·s⁻¹",         # the ½ left out of Ek
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = 0 + ½mv²\n70 560 = 0 + ½ × 72 × v²\nv = 44,27 m·s⁻¹",                  # Ep at 50 m left out
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n70 560 = (72)(9,8)(50) + ½ × 72 × v²\nv = 980 m·s⁻¹"], 0,  # no square root
        ["Which energies does the man have on the sky bridge, and which at 50 m above the ground?",
         "Set the mechanical energy on the bridge equal to that at 50 m: which quantity do you solve for?"],
        after=["5.2"]),   # the options show 5.2's 70 560 J
    draw("5.5", "Draw a graph of Ep versus Ek for the motion of the man from the instant he jumps until he reaches the ground.", 3, [
        ["Axes with correct labels: Ep (J) and Ek (J)", 1], ["A straight line with a decreasing slope", 2]],
        ["Which quantity goes on the vertical axis of a graph of Ep versus Ek?", "As Ep decreases by some amount, by how much does Ek increase?"],
        memo="The memo's graph: Ep (J) up and Ek (J) across, a straight line from a point on the Ep axis down to a point on the Ek axis."),
]

# ---- QUESTION 6, the question paper page 10 and the memo pages 7-8 ----
q6 = [
    rub("6.1", "State the phenomenon observed when the two pulses meet at point C.", 3, [
        "Superposition of pulses. (1)", "Algebraic sum of the amplitudes of two pulses (1)", "that occupy the same space at the same time. (1)"],
        ["What happens to two pulses that meet in the same place at the same moment?", "How do you find the displacement of the rope where they overlap?"]),
    draw("6.2", "Draw a labelled diagram to show the resultant pulse when the two pulses meet at point C. Label the pulses clearly.", 2, [
        ["The resultant pulse drawn at C as a trough with an amplitude of −2 cm", 1], ["Both pulses, A and B, shown and labelled", 1]],
        ["Pulse A lies above the rope's rest position and pulse B below it: what happens to their displacements where they overlap?",
         "How will you show the two original pulses in your diagram?"],
        memo="The memo's diagram: pulse A (dashed, above) and pulse B (dashed, below) drawn over each other at C, and the resultant pulse, labelled "
             "−2 cm, below the rest position."),
    term("6.3", "Name the type of interference that takes place when the pulses meet.", ["Destructive interference", "Destructive"],
         ["Is each pulse above or below the rope's rest position?", "Is the resultant pulse bigger or smaller than the bigger of the two pulses?"]),
    work("6.4", "Determine the resultant amplitude of the pulses at point C.", 2, [
        "Amplitude = (+4) + (+6)\n= 10 cm",                                         # the sign of B left out
        "Amplitude = {(+4) + (−6)}/{2}\n= −1 cm",                                    # the two amplitudes averaged
        "Amplitude = (+4) + (−6)\n= −2 cm",                                          # the memo (2 or 0)
        "Amplitude = (−6) − (+4)\n= −10 cm"], 2,                                     # subtracted, not added
        ["What are the amplitudes of pulses A and B, with their signs?", "How do you combine two amplitudes where pulses overlap?"],
        after=["6.2", "6.3"]),   # the options show 6.2's −2 cm resultant, smaller than either pulse (6.3's destructive interference)
    mcq("6.5", "How will the amplitude of pulse A be affected after passing point C? Write down only INCREASES, DECREASES or REMAINS THE SAME.",
        ["Increases", "Decreases", "Remains the same"], 2,
        ["What happens to each pulse once the two have passed through each other?",
         "Does superposition change a pulse only while the pulses overlap, or afterwards too?"], marks=1),
]

# ---- QUESTION 7, the question paper page 10 and the memo page 8 ----
q7 = [
    rub("7.1", "Explain the term ultrasound.", 2, ["Sound with frequencies that are higher than what is audible to the human ear. (2)"],
        ["What is the range of frequencies the human ear can hear?", "Can a human hear the young dolphin's 130 kHz whistle?"], each=2),
    work("7.2", "Calculate the wavelength of the young dolphin's whistle.", 4, [
        "v = fλ\n1 480 = 130λ\nλ = 11,38 m",                                         # 130 kHz not changed to hertz
        "v = fλ\n1 480 = 130 000λ\nλ = 0,011 m",                                     # the memo
        "v = {f}/{λ}\n1 480 = {130 000}/{λ}\nλ = 87,84 m",                           # the wave equation upside down
        "v = fλ\n340 = 130 000λ\nλ = 2,62 × 10⁻³ m"], 1,                            # the speed of sound in air (a value from the wrong part)
        ["What is the frequency of the whistle in hertz?", "Which wave equation links speed, frequency and wavelength?"]),
    work("7.3", "Another dolphin hears the distress call of the young dolphin 2 s later. How far apart are the two dolphins from each other?", 4, [
        "Speed = {distance}/{time}\n1 480 = {distance}/{2}\ndistance = 2 960 m",          # the memo
        "Speed = {distance}/{time}\n1 480 = {distance}/{2}\ndistance = 740 m",            # divided instead of multiplied
        "Speed = {distance}/{time}\n340 = {distance}/{2}\ndistance = 680 m",              # the speed of sound in air
        "Speed = {distance}/{time}\n1 480 = {2 × distance}/{2}\ndistance = 1 480 m"], 0,  # treated as an echo (there and back)
        ["How fast does sound travel in seawater?", "Which formula links distance, speed and time?"]),
    rub("7.4", "The speed of sound in air is 340 m·s⁻¹. Briefly explain why the speed of sound in air is different from the speed of sound in seawater.", 2, [
        "The speed of sound in air is slower, as air is less dense (1) and the particles are further apart.",
        "The speed of sound in sea water is faster, as sea water is denser (1) and the particles are closer together."],
        ["How close together are the particles in air compared with those in seawater?", "How does sound pass from one particle to the next?"]),
    rub("7.5", "Describe how dolphins use echolocation to hunt their prey.", 3, [
        "Dolphins send out a sound (frequency). (1)", "The sound reflects off the prey and returns to the dolphin. (1)",
        "The dolphin estimates distance from prey by using time for echo to return. (1)"],
        ["What happens to a sound wave when it hits an object?", "What can the time between sending a sound and hearing it back tell you?"]),
]

# ---- QUESTION 8, the question paper page 11 and the memo page 9 ----
RED = "A laser pointer uses red light photons with a wavelength of 620 nm. "
q8 = [
    # the memo: "Infrared waves"; the paper's own 8.2 says the laser pointer uses red light of 620 nm (visible): both earn the mark
    term("8.1.1", "State the type of electromagnetic radiation that is emitted by the laser pointer.",
         ["Infrared waves", "Infrared", "Infrared radiation", "Visible light", "Red light", "Visible"],
         ["Which types of electromagnetic radiation have wavelengths close to those of red light?",
          "Look ahead to 8.2: what wavelength does the laser pointer's light have?"]),
    term("8.1.2", "State the type of electromagnetic radiation that is emitted by the cellphone.",
         ["Radio waves", "Microwaves", "Radio wave", "Microwave", "Radio waves or microwaves"],
         ["Which electromagnetic waves carry signals between a cellphone and a tower?", "Are these waves longer or shorter than visible light?"]),
    rub("8.2.1", RED + "Define the term photon.", 2, ["Packet of energy found in light. (2)"],
        ["Which formula gives the energy of one photon?", "Does a photon have a charge, or does it carry only energy?"], each=2),
    work("8.2.2", RED + "Calculate the energy of a red light photon.", 6, [
        "c = f × λ\n3 × 10⁸ = f × 620\nf = 4,839 × 10⁵ Hz\nE = hf\nE = 6,63 × 10⁻³⁴ × 4,839 × 10⁵\nE = 3,21 × 10⁻²⁸ J",            # nm not changed to m
        "c = f × λ\nf = {620 × 10⁻⁹}/{3 × 10⁸}\nf = 2,067 × 10⁻¹⁵ Hz\nE = hf\nE = 6,63 × 10⁻³⁴ × 2,067 × 10⁻¹⁵\nE = 1,37 × 10⁻⁴⁸ J",  # f = λ/c
        "c = f × λ\n3 × 10⁸ = f × 620 × 10⁻⁹\nf = 4,839 × 10¹⁴ Hz\nE = hf\nE = 1,6 × 10⁻¹⁹ × 4,839 × 10¹⁴\nE = 7,74 × 10⁻⁵ J",       # e for h (wrong constant)
        "c = f × λ\n3 × 10⁸ = f × 620 × 10⁻⁹\nf = 4,839 × 10¹⁴ Hz\nE = hf\nE = 6,63 × 10⁻³⁴ × 4,839 × 10¹⁴\nE = 3,21 × 10⁻¹⁹ J"], 3,
        # ^ the memo's OPTION 1 with the paper's 620 nm: the memo substitutes 650 x 10⁻⁹ m (f = 4,615 x 10¹⁴ Hz, E = 3,06 x 10⁻¹⁹ J), a slip
        # (flagged); 3,06 x 10⁻¹⁹ J earns the marks too, so it is never a wrong option
        ["What is 620 nm in metres?", "Which two equations take you from the wavelength to the energy of a photon?"]),
    rub("8.2.3", RED + "Refer to the answer to QUESTION 8.2.2. Explain why it is very dangerous to shine a laser pointer into a person's eyes.", 2, [
        "Laser light has high intensity and can penetrate soft tissues of humans. (1)", "This can lead to damage of eye tissue. (1)"],
        ["How concentrated is the light in a laser beam compared with ordinary light?", "Which part of the eye could the beam reach and harm?"]),
]

# ---- QUESTION 9, the question paper page 12 and the memo pages 9-10 ----
q9a = [
    rub("9.1", "Explain the term magnetic field.", 2, [
        "Magnetic field: an area or region in space where another magnet or ferromagnetic substance can experience a magnetic force. (2)"],
        ["What happens to a compass needle brought near a magnet?", "Which materials are attracted by a magnet?"], each=2),
    draw("9.2", "Draw the magnetic field pattern between the two north poles of the magnets.", 3, [
        ["Two north poles facing each other", 1], ["Curved magnetic field lines", 1], ["Field direction away from each north pole", 1]],
        ["Do magnetic field lines point away from or towards a north pole?",
         "Like poles repel: do the field lines between them join up, or turn away from each other?"],
        memo="The memo's sketch: field lines leave each north pole and curve away from each other, up and down, without joining."),
]
q9b = [
    rub("9.3.1", "What is the mathematical relationship between magnetic force and distance between the two magnets?", 1, [
        "Magnetic force is inversely proportional to the distance between two magnets. (1)",
        "OR — If the distance between the magnets increases, the force decreases. (1)"],
        ["What happens to the force as the distance doubles from 2 cm to 4 cm?", "Is the graph a straight line or a curve?"]),
    num("9.3.2", "What is the magnitude of the magnetic force between the two magnets when they are 4 cm apart?", 0.1, 0.01, "N",
        ["Find 4 cm on the distance axis: where is the curve above it?", "Read across to the force axis: on which marked value does it fall?"]),
    num("9.3.3", "How far apart must the magnets be to experience a force of 0,05 N?", 10, 0.5, "cm",
        ["Where is 0,05 N on the force axis?", "Follow it across to the curve: which distance is below that point?"]),
]

# ---- QUESTION 10, the question paper page 13 and the memo page 10 ----
q10a = [
    rub("10.1", "Distinguish between a neutral object and a charged object.", 2, [
        "Neutral object: has equal amount of both protons and electrons. (1)", "Charged object: has either gained or lost electrons. (1)"],
        ["Which particles in an atom carry a charge?", "Which of those particles can move from one object to another when they are rubbed?"]),
    mcq("10.2", "Does the ruler GAIN or LOSE electrons?", ["Gain", "Lose"], 0,
        ["Is the charge on the ruler positive or negative?", "Which particles carry a negative charge?"], marks=1),
    work("10.3", "Calculate the number of electrons transferred during the process of rubbing.", 3, [
        "n = {e}/{Q}\nn = {1,6 × 10⁻¹⁹}/{3,5 × 10⁻¹⁵}\nn = 4,57 × 10⁻⁵ electrons",      # the formula upside down
        "n = {Q}/{e}\nn = {3,5 × 10⁻¹⁵}/{9,11 × 10⁻³¹}\nn = 3,84 × 10¹⁵ electrons",     # the electron's mass for its charge (wrong constant)
        "n = {Q}/{e}\nn = {3,5 × 10⁻¹⁵}/{1,6 × 10⁻¹⁹}\nn = 2,19 × 10⁴ electrons",       # the memo's working with the paper's charge
        "n = {Q}/{e}\nn = {3,5 × 10⁻¹⁵}/{1,6 × 10¹⁹}\nn = 2,19 × 10⁻³⁴ electrons"], 2,  # 10⁻¹⁹ written 10¹⁹ (a power slip)
        # (the memo substitutes 3 x 10⁻⁶ C and gets 1,88 x 10¹³, a slip: flagged; that value earns the marks too, never a wrong option)
        ["Which equation links a charge, the number of electrons and the charge on one electron?", "What charge does the data sheet give for one electron?"]),
]
q10b = [
    rub("10.4.1", "Explain why the pieces of paper are attracted to the ruler.", 3, [
        "When the charged plastic ruler is brought closer to the uncharged pieces of paper, the paper is polarised. (1)",
        "The negative charges on the paper are repelled by the negative charges on the ruler. (1)",
        "This leaves the side of the paper closest to the ruler positive. (1)"],
        ["What happens to the charges inside a neutral piece of paper when a charged ruler comes near?", "Do like charges attract or repel each other?"]),
    rub("10.4.2", "Name ONE application of electrostatics in our daily lives.", 1, [
        "Photocopier / finger printing / spray painting (any one) (1)"],
        ["Which machines or processes use charged particles or charged droplets?", "Where does charge make powder or paint stick to a surface?"]),
]

# ---- QUESTION 11, the question paper page 14 and the memo page 11 ----
q11 = [
    rub("11.1", "Define the term emf.", 2, ["Work done per charge by the source (battery). (2)"],
        ["What does emf stand for?", "Is emf measured across the battery or across a resistor?"], each=2),
    work("11.2", "Calculate the total resistance of Circuit A.", 2, [
        "RT = R1 + R2\nRT = 1,5 + 1,5\nRT = 3 Ω",                                                      # added as if in series
        "{1}/{Rp} = {1}/{R1} + {1}/{R2}\n{1}/{Rp} = {1}/{1,5} + {1}/{1,5} = {4}/{3}\nRp = 1,33 Ω",       # 1/Rp not turned over
        "{1}/{Rp} = {1}/{R1} + {1}/{R2}\n{1}/{Rp} = {1 + 1}/{1,5 + 1,5} = {2}/{3}\nRp = 1,5 Ω",          # the fractions added top and bottom
        "{1}/{Rp} = {1}/{R1} + {1}/{R2}\n{1}/{Rp} = {1}/{1,5} + {1}/{1,5} = {4}/{3}\nRp = 0,75 Ω"], 3,   # the memo
        ["Are the two 1,5 Ω resistors in series or in parallel?", "Which formula gives the total resistance of resistors in that arrangement?"]),
    num("11.3.1", "Consider Circuit B. Write down the reading on A2.", 1.5, 0, "A",
        ["How are the 2 Ω and 4 Ω resistors connected to ammeter A1?", "How does the current compare at different points of a single loop?"]),
    work("11.3.2", "Consider Circuit B. Calculate the reading on V1.", 3, [
        "V = IR\nV = 1,5(4)\nV = 6 V",                                               # the 4 Ω resistor (the wrong part)
        "V = IR\nV = 1,5(2)\nV = 3 V",                                               # the memo
        "V = {I}/{R}\nV = {1,5}/{2}\nV = 0,75 V",                                    # the formula upside down
        "V = IR\nV = 1,5(2 + 4)\nV = 9 V"], 1,                                       # both resistors (the whole circuit)
        ["Across which resistor is V1 connected?", "Which formula links potential difference, current and resistance?"],
        after=["11.3.1"]),   # the options show the 1,5 A through the 2 Ω resistor (11.3.1's reading)
    rub("11.4", "If a third resistor (1,5 Ω) is placed in parallel with the existing resistors in Circuit A, would the total current in the circuit "
        "INCREASE, DECREASE or REMAIN THE SAME? Explain the answer.", 3, [
        "INCREASE (1)", "If the 1,5 Ω resistor is added, the resistance of the whole circuit decreases. (1)",
        "Since R ∝ 1/I, if R decreases, V is constant and I of the circuit increases. (1)"],
        ["What happens to the total resistance when you add another resistor in parallel?",
         "If the battery's potential difference stays the same, how does the current depend on the resistance?"]),
]

POS_TABLE = {"head": ["TIME (s)", "POSITION (m)"], "rows": [["0", "0"], ["1", "5"], ["2", "10"], ["3", "15"], ["4", "20"]]}
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Speed and displacement", "marks": 13,
     "lead": "A brother and sister walk home from school. After walking 500 m eastwards, the brother realises that he has left a book at school and "
             "he returns to school. His sister continues walking another 800 m to their home. She arrives home 30 minutes after leaving school.",
     "figure": fig("Q2", "A school on the left and a home on the right on one straight line: an arrow 500 m long runs from the school to the brother "
                   "and sister, and an arrow 800 m long from them to the home; a compass shows north up and east to the right."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Motion graphs", "marks": 16,
     "lead": "The engineers at a car company conduct various tests on their cars. During one of the tests they measure the change in position during "
             "equal time intervals. The results obtained are recorded in the table below.", "table": POS_TABLE, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Equations of motion", "marks": 8,
     "lead": "A car accelerates from rest at 15 m·s⁻² for 2 s on a horizontal road.", "items": q4a},
    {"id": "4.3", "title": "Question 4.3", "kind": "Safe following distance", "marks": 13,
     "lead": "While travelling at a constant velocity of 108 km·h⁻¹, the driver of a car notices a sign warning motorists to keep a safe 2-second "
             "following distance. At that instant the car is 80 m behind a truck that is travelling at a constant velocity of 90 km·h⁻¹.",
     "figure": fig("Q4", "A car moving to the right at 108 km·h⁻¹, 80 m behind a truck that is moving to the right at 90 km·h⁻¹."), "items": q4b},
    {"id": "5", "title": "Question 5", "kind": "Mechanical energy", "marks": 15,
     "lead": "A lift takes a man to a sky bridge, which is 100 m above the ground, as shown below. He makes a bungee jump from the sky bridge. Ignore "
             "the effects of air resistance.",
     "figure": fig("Q5", "A photograph of two painted cooling towers joined at the top by a sky bridge; a dashed line marks the bridge's height of "
                   "100 m above the ground."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Pulses on a rope", "marks": 9,
     "lead": "Two girls, standing at opposite ends of a rope, each makes a pulse of the same speed. Pulse A, with an amplitude of 4 cm, moves to the "
             "right and pulse B, with an amplitude of −6 cm, moves to the left. The pulses meet at point C.",
     "figure": fig("Q6", "Two girls hold the ends of a rope: pulse A, above the rope's rest position, is near the girl on the left, and pulse B, "
                   "below it, is near the girl on the right; point C is on the rope between them."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Sound", "marks": 15,
     "lead": "Dolphins communicate through the emission and reception of sounds. A young dolphin was separated from its mother and started whistling at "
             "a frequency of 130 kHz to call her. The speed of sound in seawater is 1 480 m·s⁻¹.", "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Electromagnetic radiation", "marks": 12,
     "lead": "Consider a laser pointer and cellphone, as shown below.",
     "figure": fig("Q8", "A laser pointer on the left and a cellphone with an aerial on the right."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Magnetism", "marks": 5, "lead": "Two magnets are placed so that their north poles face each other.",
     "figure": fig("Q9a", "Two bar magnets in a line with a gap between them; the end of each magnet marked N faces the other magnet."), "items": q9a},
    {"id": "9.3", "title": "Question 9.3", "kind": "Magnetic force and distance", "marks": 3,
     "lead": "The graph below shows how the magnetic force varies with distance between the magnets.",
     "figure": fig("Q9b", "Force (N), 0 to 0,5, up against distance (cm), 0 to 10, across, on a grid: a smooth curve drawn through five plotted "
                   "points between about 1 cm and 10 cm."), "items": q9b},
    {"id": "10", "title": "Question 10", "kind": "Electrostatics", "marks": 6,
     "lead": "A neutral plastic ruler becomes charged when it is rubbed with a woollen cloth. After rubbing, the ruler has a charge of −3,5 x 10⁻¹⁵ C.",
     "items": q10a},
    {"id": "10.4", "title": "Question 10.4", "kind": "Electrostatic attraction", "marks": 4,
     "lead": "The charged ruler is now brought closer to pieces of paper. The pieces of paper are attracted to the ruler, as shown below.",
     "figure": fig("Q10", "A ruler held horizontally just above small pieces of paper."), "items": q10b},
    {"id": "11", "title": "Question 11", "kind": "Electric circuits", "marks": 11,
     "lead": "Refer to Circuits A and B below and answer the questions that follow.",
     "figure": fig("Q11", "Circuit A: a 9 V battery and switch S1 with two 1,5 Ω resistors, each on its own branch between the two wires from the "
                   "battery; voltmeter V2 across the upper resistor and V1 across the lower one. Circuit B: a 9 V battery, switch S1, ammeter A1 "
                   "(1,5 A), a 2 Ω resistor, ammeter A2 and a 4 Ω resistor, one after the other in a single loop; voltmeter V1 across the 2 Ω "
                   "resistor and V2 across the 4 Ω resistor."), "items": q11},
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
    # 2, either OR form: the wrong ones are the average velocity, acceleration, velocity, displacement, a product and the inverse
    "2.1": (2, ["The total distance travelled per total time.", "The distance travelled divided by the total time."],
               ["The total displacement divided by the total time.", "The rate of change of velocity.", "The rate of change of position.",
                "The total distance travelled multiplied by the total time.", "The change in position of an object.",
                "The total time taken divided by the total distance travelled."]),   # (6 wrong cards: with three to five both right cards came first)
    # 2 ticks: the choice (zero acceleration) beside its reason (constant velocity); the wrong ones are a uniform or growing change
    "3.6": (1, ["The acceleration of the car is zero.", "The velocity of the car is constant."],
               ["The acceleration of the car is constant and greater than zero.", "The velocity of the car increases by the same amount every second.",
                "The acceleration of the car increases with time.", "The velocity of the car decreases uniformly."]),
    # 2: the wrong ones are velocity, a change without "rate", speed, momentum
    "4.1": (2, ["The rate of change of velocity."],
               ["The rate of change of position.", "The change in velocity of an object.", "The distance travelled per unit time.",
                "The product of the mass of an object and its velocity."]),
    # 2, either OR form: the wrong ones are less than 2 s, a distance in metres or a speed, and overtaking
    "4.3": (2, ["When following a car, a motorist should keep a safe distance such that it takes more than 2 s to reach the same position as the car "
                "in front.", "The car will need 2 s to stop in an emergency and not hit the car in front."],
               ["When following a car, a motorist should keep a distance such that it takes less than 2 s to reach the same position as the car in front.",
                "A motorist should always stay exactly 2 m behind the car in front.", "A motorist should drive 2 km·h⁻¹ slower than the car in front.",
                "A motorist should overtake the car in front within 2 s."]),
    # 2: the wrong ones are gravitational potential energy, mechanical energy, momentum, power, elastic energy
    "5.1": (2, ["The energy an object has as a result of its motion."],
               ["The energy an object has because of its position relative to a reference point.",
                "The sum of the kinetic energy and the gravitational potential energy of an object.",
                "The product of the mass of an object and its velocity.", "The rate at which work is done on an object.",
                "The energy stored in a stretched or compressed spring."]),
    # 2, either OR form: the wrong ones drop "isolated", keep only one energy constant, or make the total grow
    "5.3": (2, ["The sum of the gravitational potential energy and kinetic energy in an isolated system is constant.",
                "The total mechanical energy of an isolated system remains constant."],
               ["The total mechanical energy of a system remains constant even when air resistance acts on it.",
                "The kinetic energy of an object in an isolated system remains constant.",
                "The gravitational potential energy of an object in an isolated system remains constant.",
                "The total mechanical energy of an isolated system increases as an object falls."]),
    # 3 ticks: superposition (1) and its description (2), the description played as its two points (the algebraic sum; same space, same time)
    "6.1": (1, ["The phenomenon is the superposition of pulses.", "The resultant amplitude is the algebraic sum of the amplitudes of the two pulses.",
                "The two pulses occupy the same space at the same time."],
               ["The phenomenon is the reflection of pulses.", "The resultant amplitude is the product of the amplitudes of the two pulses.",
                "The two pulses bounce off each other at point C.", "The two pulses destroy each other permanently at point C."]),
    # 2: the wrong ones are infrasound, audible sound, loudness, speed, electromagnetic waves
    "7.1": (2, ["Sound with frequencies that are higher than what is audible to the human ear."],
               ["Sound with frequencies that are lower than what is audible to the human ear.",
                "Sound with frequencies within the range that the human ear can hear.", "Sound that is louder than the human ear can bear.",
                "Sound that travels faster than 340 m·s⁻¹.", "Electromagnetic waves with frequencies higher than those of visible light."]),
    # 2 ticks: air (less dense, slower) and seawater (denser, faster); the wrong ones swap the trend or the reason
    "7.4": (1, ["The speed of sound in air is slower, as air is less dense and its particles are further apart.",
                "The speed of sound in seawater is faster, as seawater is denser and its particles are closer together."],
               ["The speed of sound in air is faster, as the particles in air are further apart.", "The speed of sound in seawater is slower, as seawater is denser.",
                "Sound travels at the same speed in all media; only its frequency changes.",
                "The speed of sound in air is slower, as sound waves in air are transverse."]),
    # 3 ticks: send out, reflect, time the echo
    "7.5": (1, ["Dolphins send out a sound.", "The sound reflects off the prey and returns to the dolphin.",
                "The dolphin estimates the distance to the prey by using the time for the echo to return."],
               ["Dolphins send out pulses of light.", "The sound is absorbed by the prey and never returns.",
                "The dolphin estimates the distance to the prey from the loudness of the sound it sends out.",
                "The prey sends out a sound that the dolphin follows."]),
    # 2: the wrong ones are the electron, a massive particle, wavelength, frequency, the proton
    "8.2.1": (2, ["A packet of energy found in light."],
                 ["A negatively charged particle found in an atom.", "A particle of light with the same mass as an electron.",
                  "The distance between two consecutive crests of a light wave.", "The number of light waves passing a point per second.",
                  "A positively charged particle in the nucleus of an atom."]),
    # 2 ticks: high intensity that penetrates soft tissue; damage to the eye tissue
    "8.2.3": (1, ["Laser light has a high intensity and can penetrate the soft tissues of humans.", "This can lead to damage of the eye tissue."],
                 ["Laser light has a low intensity and cannot penetrate the soft tissues of humans.",
                  "Red light photons have more energy than gamma-ray photons.", "Laser light makes the eye magnetic.",
                  "Laser light carries an electric charge that shocks the eye."]),
    # 2: the wrong ones are the electric and gravitational fields, the force itself, the inside of a magnet, no force
    "9.1": (2, ["An area or region in space where another magnet or ferromagnetic substance can experience a magnetic force."],
               ["A region in space where an electric charge experiences an electric force.", "A region in space where a mass experiences a gravitational force.",
                "The force that a magnet exerts on a ferromagnetic substance.", "The region inside a magnet where its poles are found.",
                "The region around a magnet where no force is experienced.", "The force between two magnets divided by the distance between them.",
                "The number of magnetic poles that a magnet has."]),   # (7 wrong cards: with four to six the right card came first)
    # 1, either OR form: the wrong ones are direct proportion, the inverse trend, no relation, a straight line down
    "9.3.1": (1, ["Magnetic force is inversely proportional to the distance between the two magnets.",
                  "If the distance between the magnets increases, the force decreases."],
                 ["Magnetic force is directly proportional to the distance between the two magnets.",
                  "If the distance between the magnets increases, the force increases.",
                  "The magnetic force does not depend on the distance between the magnets.",
                  "The magnetic force decreases by the same amount for every centimetre the magnets move apart."]),
    # 1 + 1: one card for each kind of object, so two cards about one kind can never earn both marks
    "10.1": (1, ["A neutral object has equal amounts of protons and electrons.", "A charged object has either gained or lost electrons."],
                ["A neutral object has no electrons.", "A charged object has either gained or lost protons.", "A neutral object has more protons than electrons.",
                 "A charged object has equal amounts of protons and electrons."]),
    # 3 ticks: polarised, negative charges repelled, the near side positive
    "10.4.1": (1, ["The paper is polarised when the charged ruler is brought closer.",
                   "The negative charges on the paper are repelled by the negative charges on the ruler.",
                   "This leaves the side of the paper closest to the ruler positive."],
                  ["The positive charges on the paper are repelled by the ruler.", "This leaves the side of the paper closest to the ruler negative.",
                   "The ruler magnetises the pieces of paper.", "All objects attract each other, whatever their charges."]),
    # 1, any of the memo's three: the wrong ones are uses of magnetism, heating, microwaves and a magnet with a current
    "10.4.2": (1, ["Photocopier.", "Fingerprinting.", "Spray painting."],
                  ["A compass for navigation.", "An electric kettle.", "A microwave oven.", "A loudspeaker."]),
    # 2: the wrong ones are current, resistance, power, a store of charge, a count of electrons
    "11.1": (2, ["The work done per unit charge by the source (battery)."],
                ["The rate of flow of charge.", "The opposition to the flow of charge in a conductor.", "The work done per unit time.",
                 "The total charge that a battery can supply.", "The number of electrons in a battery."]),
    # 3 ticks: the choice (INCREASE) beside its two reasons (R decreases; V constant, I increases)
    "11.4": (1, ["The total current in the circuit INCREASES.", "Adding the 1,5 Ω resistor in parallel decreases the resistance of the whole circuit.",
                 "Since V is constant and I is inversely proportional to R, the current of the circuit increases as R decreases."],
                ["The total current in the circuit DECREASES.", "The total current in the circuit REMAINS THE SAME.",
                 "Adding a resistor in parallel increases the resistance of the whole circuit.",
                 "Since V is constant and I is directly proportional to R, the current of the circuit decreases as R decreases."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, laws, explanations and choices with reasons), so SORTS stays empty and sort_ is kept for parity.
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

assert tuple(AUTHORED) == ("2.2", "2.4", "3.4", "4.2.1", "4.2.2", "4.4", "4.5", "5.2", "5.4", "6.4", "7.2", "7.3", "8.2.2", "10.3", "11.2",
                           "11.3.2"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["9.3.2", "9.3.3", "11.3.1"], "only the read-offs stay typed numbers"
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["3.1", "3.2.1", "3.2.2", "6.3", "8.1.1", "8.1.2"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["2.3", "3.3", "3.5", "5.5", "6.2", "9.2"]
for i in ITEMS:   # a built plot (build-play.js "plot"): one test per memo criterion, its marks the part's, every point on the grid's snap
    b = i.get("build") or {}
    if b.get("kind") == "plot":
        ids = {p["id"] for p in b["points"]}
        assert len(b["tests"]) == len(i["criteria"]) and sum(c["marks"] for c in i["criteria"]) == i["marks"], i["n"]
        assert all(set(t.get("ids", [])) <= ids for t in b["tests"]), i["n"]
        for k, ax in enumerate((b["x"], b["y"])):
            for st in ([ax["snap"]] if "snap" in ax else [s / b["grid"].get("sub", 10) for s in ax["ok"]]):
                for p in b["points"]:
                    if "at" in p:
                        u = p["at"][k]
                        assert abs(u - round(u / st) * st) <= max(b["tol"][k], st / 2 if "scales" in ax else 0) + 1e-9, (i["n"], p["id"], k)
                        assert (ax.get("min", 0) <= u <= ax["max"]) if "max" in ax else u <= min(ax["ok"]) * (b["grid"]["nx"] if k == 0 else b["grid"]["ny"]), (i["n"], p["id"])
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "2.4": ["2.2", "2.3"], "3.3": ["3.2.1", "3.2.2"], "3.4": ["3.3"], "3.5": ["3.4"], "3.6": ["3.5"], "4.2.2": ["4.2.1"], "4.5": ["4.4"],
    "5.4": ["5.2"], "6.4": ["6.2", "6.3"], "11.3.2": ["11.3.1"]}
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2017", "total_marks": 150, "time": "2 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic physics errors (a sign slip, a value from the wrong "
                                                       "body or part, a formula upside down or with a factor dropped, a power of ten slipped, a unit "
                                                       "not converted, the wrong constant), 0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, "
                                                       "%d marks). 7.3 ('How far apart ...?') shows a working in the memo, so it is one of them. A "
                                                       "value the memo also accepts is never a wrong option: 2.4's 3 184,62 s (from the unrounded "
                                                       "13/18 m·s⁻¹), 4.2.2's OPTION 2 (vf = vi + aΔt, also 30 m·s⁻¹). 4.4 uses the truck's speed, as "
                                                       "the memo does (50 m); no option uses the car's own 30 m·s⁻¹ (60 m), a reading a learner could "
                                                       "defend. 4.2.2 and 4.4's directions: the memo's 'to the right'."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "4.2.1", "kind": "memo_issue", "detail": "The memo prints (4) for 4.2.1 and (4) for 4.2.2 (four ticks each); the paper prints (3) and (3), "
                                                       "and both give QUESTION 4 [21] (2 + 3 + 3 + 2 + 6 + 5): the paper's marks are kept."},
        {"n": "8.1.1", "kind": "memo_issue", "detail": "The memo answers 'Infrared waves' (memo page 9); the paper's own 8.2 says the laser pointer uses "
                                                       "red light photons of 620 nm, which is visible light. Both earn the mark (Murci's ruling "
                                                       "2026-10-10): the term accepts the memo's infrared and visible (red) light."},
        {"n": "8.2.2", "kind": "memo_issue", "detail": "The memo substitutes λ = 650 x 10⁻⁹ m (memo page 9, both options): f = 4,615 x 10¹⁴ Hz, "
                                                       "E = 3,06 x 10⁻¹⁹ J. The paper gives 620 nm: f = 4,839 x 10¹⁴ Hz, E = 3,21 x 10⁻¹⁹ J. The "
                                                       "right option uses the paper's 620 nm; the memo's 3,06 x 10⁻¹⁹ J earns the marks too, so it is "
                                                       "never a wrong option."},
        {"n": "10.3", "kind": "memo_issue", "detail": "The memo substitutes Q = 3 x 10⁻⁶ C (memo page 10): n = 1,88 x 10¹³. The paper gives the "
                                                      "ruler's charge as −3,5 x 10⁻¹⁵ C: n = 3,5 x 10⁻¹⁵ / 1,6 x 10⁻¹⁹ = 21 875 = 2,19 x 10⁴ "
                                                      "electrons. The right option uses the paper's charge; the memo's 1,88 x 10¹³ earns the marks "
                                                      "too, so it is never a wrong option."},
        {"n": "3.5", "kind": "memo_issue", "detail": "The memo's 3.5 sketch gives no mark allocation (2 marks): the criteria split them between the "
                                                     "labelled axes and the horizontal line at 5 m·s⁻¹. Its time axis ends at '20' while the table "
                                                     "runs from 0 to 4 s (the sketch is NOT to scale)."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11; its instructions say TEN questions, it prints eleven), "
                                                           "hand-transcribed from the paper and memo PDFs and their page images (the 1.2 graphs, 1.3 "
                                                           "oil drops, circuits and the memo's fractions and 8.2.2 working are images); no API call."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions and laws (2.1, 4.1, 4.3, 5.1, "
                                                    "5.3, 7.1, 8.2.1, 9.1, 11.1) pick one card for their 2 marks (an OR form is a second right "
                                                    "card) and the relationship 9.3.1 one card for 1; 10.1 picks one card for each kind of object "
                                                    "(1 + 1); the explanations ticked point by point (6.1, 7.4, 7.5, 8.2.3, 10.4.1) pick the memo's "
                                                    "points, 1 mark each (6.1's description, ticked twice, plays as its two points: the algebraic "
                                                    "sum, and the same space at the same time); the choices with reasons (3.6, 11.4) pick the "
                                                    "choice and its reasons, 1 mark each; 10.4.2 picks one of the memo's three applications."
                                                    % len(PICKS)},
        {"n": "2.3", "kind": "no_fit", "detail": "Drawings (2.3's vector scale diagram, 3.5, 5.5, 6.2, 9.2) are done on paper and self-checked "
                                                 "against the memo's criteria."},
        {"n": "3.3", "kind": "no_fit", "detail": "The position-time graph is BUILT on a grid (2026-10-11, build 'plot'): the axes' labels chosen "
                                                 "from one list (position, time, velocity in m or s), the five points placed (snapping to 0,2 s "
                                                 "and 0,5 m), and the line chosen (a straight line, a smooth curve or the points joined). The memo "
                                                 "marks no scale, so the grid carries the memo's (1 s and 5 m a big square). Its '2 x points "
                                                 "plotted and joined' gives no split: all five earn 2, three or four earn 1 (our reading)."},
    ],
}
QTOTAL = {"1": 20, "2": 13, "3": 16, "4": 21, "5": 15, "6": 9, "7": 15, "8": 12, "9": 8, "10": 10, "11": 11}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's ten printed letters are the paper's (A2 B1 C4 D3), 6.5 (C) and 10.2 (A) are printed choices of three and
# two, so the 16 workings sit at A4 B5 C3 D4: the paper within 2 of even, the 26 four-option questions within 1
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 2, spread
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
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
