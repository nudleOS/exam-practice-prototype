"""Grade 10 Physical Sciences P1 (Physics) Nov 2018 (DBE common paper), the whole paper (Questions 1 to 11), hand-transcribed into the
catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options,
marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API
call: the transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets formulas, the 1.7
signs and the wave patterns as images, so its text layer has gaps.

  python tools/ingest/transcribe_g10_ps_p1_2018_11.py
  python tools/ingest/ingest.py "uploads/Grade 10 Physical Sciences P1 Nov 2018 Eng.pdf" "uploads/Grade 10 Physical Sciences P1 Nov 2018 MG Eng & Afr.pdf" --id g10-ps-p1-2018-11 --from-json

The final form of the Grade 12 papers (Murci's rulings 2026-10-10; model: transcribe_ps_p1_2025_11.py):
  multiple choice printed in the paper -> mcq as printed (options printed as a table -> optTable); a choice printed in the stem with no
  explanation in the same part (3.2.1, 3.2.2 "uniform velocity or uniformly accelerated", 9.2 "A or B", 9.3 "NORTH or SOUTH", 9.6.1)
  -> mcq of the printed choices; 1.10, whose memo accepts two letters ("C/B"), is a pick of one with both right (Geography P2 Nov 2024
  1.1.8's form), in a mission of its own so the wave patterns stay its figure (a pickn carries no figure). One term the memo names ->
  term; one read-off value with no working -> num (6.2.2, 11.1.1(a) and (b), 11.2.2).
  Every calculation ("Calculate", "Determine", "Identify ... by performing a calculation", the YES/NO "support with a calculation" of
  4.3 and 5.5) -> authored multiple choice, `work`: the memo's FIRST working line by line and three workings each built from a
  DIFFERENT realistic error (a sign or direction slip, a value from the wrong body or part, a formula upside down or with a factor
  dropped, a power of ten slipped, a unit not converted), every number recomputed; 0 or full marks. A value the memo also accepts
  (its OR answers, its positive marking from a rounded value, its ranges) is never a wrong option.
  A definition, law or conclusion -> statements (pick 1 card for its marks; an OR form a second right card); an explanation the memo
  ticks point by point -> statements, 1 mark a point. 6.1 ("ONE difference and ONE similarity") plays as two cards, the memo's
  difference and its first similarity: its other similarities (period, frequency, transverse) are neither right nor wrong cards, so
  two similarities can never earn both marks. No memo here weighs two sides, so no part plays as a sort.
  A pick of letters the memo marks as a pair (6.2.1, "two points out of phase") -> a multiple choice of pairs.
  "Draw / Sketch / show on the graph" -> draw with the memo's criteria (self-checked, flagged no_fit).
  A part whose options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose diagram changes part-way is two missions (9 and 9.6; 11.1 and 11.2).
Figure boxes are measured in PDF points (page 595.32 x 841.92) from the drawings and images themselves and checked on a contact sheet
(scratchpad lower/g10-ps-p1-2018-11/figs.py)."""
import json
import random
import re
from pathlib import Path

PID = "g10-ps-p1-2018-11"
W, H = 595.32, 841.92
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.5": [4, 186.0, 136.0, 442.0, 247.0], "1.6": [4, 176.0, 448.0, 382.0, 637.0], "1.7": [5, 150.0, 131.0, 472.0, 237.0],
    "1.10": [6, 104.0, 119.0, 529.0, 412.0], "Q2": [7, 60.0, 176.0, 531.0, 339.0], "Q3": [8, 34.0, 166.0, 548.0, 311.0],
    "Q4": [9, 66.0, 164.0, 545.0, 338.0], "Q5": [10, 76.0, 175.0, 476.0, 388.0], "Q6": [11, 47.0, 141.0, 558.0, 393.0],
    "Q7": [12, 66.0, 184.0, 497.0, 294.0], "Q9a": [14, 128.0, 160.0, 482.0, 282.0], "Q9b": [14, 138.0, 538.0, 392.0, 645.0],
    "Q10": [15, 136.0, 154.0, 360.0, 306.0], "Q11a": [16, 94.0, 152.0, 516.0, 437.0], "Q11b": [17, 82.0, 125.0, 512.0, 462.0]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def pick1(n, q, opts, pool, clues, marks=2):
    """Choose ONE: every index in `pool` is right (a printed multiple choice whose memo accepts two letters)."""
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": 1}


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
q1 = [
    mcq("1.1", "An object is positively charged if it has more …",
        ["electrons than protons.", "electrons than neutrons.", "protons than electrons.", "protons than neutrons."], 2,
        ["Which particles carry a negative charge, and which a positive charge?", "Which particles can an object gain or lose when it is charged?"]),
    mcq("1.2", "A car is travelling at a speed of 30 m·s⁻¹ on a straight road. What would be the speed of the car in km·h⁻¹?",
        ["8,33 km·h⁻¹", "30 km·h⁻¹", "108 km·h⁻¹", "130 km·h⁻¹"], 2,
        ["How many metres are in a kilometre, and how many seconds in an hour?",
         "Should the number get bigger or smaller when you change metres per second into kilometres per hour?"]),
    mcq("1.3", "The UNIT in which the rate of flow of charge is measured, is called …", ["ampere.", "coulomb.", "volt.", "watt."], 0,
        ["What name is given to the rate of flow of charge?", "Which unit stands for one coulomb per second?"]),
    mcq("1.4", "The gradient of a velocity versus time graph is equivalent to the …",
        ["acceleration.", "displacement.", "position.", "total distance covered."], 0,
        ["A gradient is the change in the vertical quantity per change in what?", "On a velocity versus time graph, which quantity is on the vertical axis?"]),
    mcq("1.5", "An object is released from the top of a frictionless inclined plane, AB, as shown below. Which ONE of the following statements regarding "
        "the total mechanical energy of the object is CORRECT?",
        ["(Ep + Ek)A > (Ep + Ek)B", "(Ep + Ek)A < (Ep + Ek)B", "(Ep + Ek)A = (Ep + Ek)B", "(Ep + Ek)A = − (Ep + Ek)B"], 2,
        ["Is there any friction to take energy away as the object slides?", "Which principle applies to the total mechanical energy when no friction acts?"],
        figure=fig("1.5", "An object at the top, A, of an inclined plane, with an arrow pointing down the slope to B at the bottom.")),
    mcq("1.6", "Two identical light bulbs are connected in parallel, as shown in the circuit diagram below. Voltmeters V1 and V2 are connected across each "
        "light bulb. Which ONE of the following voltmeter readings is CORRECT?",
        ["V1 = V2", "V1 = 2V2", "V1 = ½V2", "V1 = ¼V2"], 0,
        ["How are the two bulbs connected to the battery?", "In a parallel circuit, is the potential difference shared between the branches, or the current?"],
        figure=fig("1.6", "A battery with two light bulbs in parallel below it; voltmeter V1 is connected across the upper bulb and voltmeter V2 across the "
                   "lower bulb.")),
    mcq("1.7", "Four identical balloons, each carrying a charge, are suspended from a ceiling, as shown in the diagram below. Balloon B is negatively "
        "charged. Which combination is CORRECT regarding the charges on the balloons?",
        ["−; +; −", "+; +; +", "−; −; −", "+; +; −"], 1,
        ["A and B touch: do they attract or repel each other?", "C and D hang apart: what does that say about their two charges?"],
        optTable={"head": ["SIGN OF CHARGE ON A", "SIGN OF CHARGE ON C", "SIGN OF CHARGE ON D"],
                  "rows": [["−", "+", "−"], ["+", "+", "+"], ["−", "−", "−"], ["+", "+", "−"]]},
        figure=fig("1.7", "Two ceiling bars: balloons A and B hang from the first bar, touching each other; balloons C and D hang from the second bar, "
                   "their strings spread so that the two balloons hang apart.")),
    mcq("1.8", "Two cyclists are cycling in opposite directions along the side line of a rectangular field. It is observed that they covered the same "
        "distance over a time interval of 3 s. Which ONE of the following physical quantities is the SAME regarding the cyclists over the interval of 3 s?",
        ["Acceleration", "Average speed", "Average velocity", "Displacement"], 1,
        ["Do the cyclists move in the same direction or in opposite directions?",
         "Which of these quantities have a direction, and which depend only on the distance covered?"]),
    mcq("1.9", "Red light of frequency f and wavelength λ shines on an object. The red light is then replaced by light of a higher energy. How do the "
        "frequency and the wavelength of light shining on the object now compare with that of red light?",
        ["Greater than f; Remains the same (λ)", "Less than f; Greater than λ", "Greater than f; Less than λ", "Remains the same (f); Less than λ"], 2,
        ["Which equation links the energy of a photon to its frequency?", "Light has a constant speed: which equation then links its frequency and wavelength?"],
        optTable={"head": ["FREQUENCY", "WAVELENGTH"],
                  "rows": [["Greater than f", "Remains the same (λ)"], ["Less than f", "Greater than λ"], ["Greater than f", "Less than λ"],
                           ["Remains the same (f)", "Less than λ"]]}),
]
q1b = [
    # the memo: "C/B". Patterns 1, 3 and 4 have the same frequency (pitch), 2 a higher one: 1 and 3 (B) and 1 and 4 (C) are both right
    pick1("1.10", "Which COMBINATION is the CORRECT representation of the wave patterns with the same pitch?",
          ["1 and 2", "1 and 3", "1 and 4", "2 and 4"], [1, 2],
          ["Which property of a sound wave decides its pitch?", "Count the complete waves each pattern shows across the same width: which patterns match?"])]

# ---- QUESTION 2, the question paper page 7 and the memo pages 2-3 ----
q2 = [
    rub("2.1", "Define the term displacement in words.", 2, [
        "The difference in position (in space). (2)", "OR — The change in position (of an object). (2)"],
        ["Is displacement about the path travelled, or about where the object ends up compared with where it started?",
         "Is displacement a vector or a scalar?"], each=2),
    # the memo: "12 m west (or −12 m)", no working; "−12 m West" earns 1 only; ACCEPT "12 m left". Played as a working: the distances added
    work("2.2", "Determine the position of the dog relative to the baby before they both moved.", 2, [
        "x = 7 m − 5 m = 2 m\nThe dog is 2 m west of the baby",               # the two distances subtracted
        "x = 7 m\nThe dog is 7 m west of the baby",                            # only the dog's distance to the toy (wrong part)
        "x = 5 m + 7 m = 12 m\nThe dog is 12 m east of the baby",              # the direction slip
        "x = 5 m + 7 m = 12 m\nThe dog is 12 m west of the baby"], 3,          # the memo
        ["How far is the dog from the toy, and how far is the toy from the baby?", "In which compass direction from the baby is the dog?"]),
    work("2.3", "Calculate the average velocity of the baby.", 4, [
        "v = {Δx}/{Δt}\nv = {5}/{30}\nv = 0,17 m·s⁻¹ west",                    # the memo
        "v = {Δx}/{Δt}\nv = {7}/{30}\nv = 0,23 m·s⁻¹ west",                    # the dog's 7 m (a value from the wrong body)
        "v = {Δt}/{Δx}\nv = {30}/{5}\nv = 6,00 m·s⁻¹ west",                    # the formula upside down
        "v = {Δx}/{Δt}\nv = {5}/{30}\nv = 0,17 m·s⁻¹ east"], 0,                # the direction slip
        ["Velocity uses displacement: how far did the baby crawl, and in which direction?", "How long did the baby take to reach the toy?"]),
    work("2.4", "If the average speed of the dog is TWICE that of the baby, calculate how long it would take the dog to reach the food bowl from the moment "
         "the dog started moving.", 4, [
        "speed = {distance}/{time}\nspeed(dog) = {0,17}/{2} = 0,085 m·s⁻¹\n0,085 = {12}/{Δt}\nΔt = 141,18 s",    # the speed halved, not doubled
        "speed = {distance}/{time}\nspeed(dog) = (0,17)(2) = 0,34 m·s⁻¹\n0,34 = {7}/{Δt}\nΔt = 20,59 s",        # only to the toy (wrong part)
        "speed = {distance}/{time}\nspeed(dog) = (0,17)(2) = 0,34 m·s⁻¹\n0,34 = {12}/{Δt}\nΔt = 35,29 s",       # the memo
        "speed = {distance}/{time}\nspeed(dog) = (0,17)(2) = 0,34 m·s⁻¹\nΔt = (0,34)(12)\nΔt = 4,08 s"], 2,    # rearranged as speed x distance
        # (the memo marks positively from 2.2 and 2.3 and rounds the baby's speed to 0,17 first; the unrounded 1/3 m·s⁻¹ gives 36 s, never an option)
        ["How fast does the dog walk if its speed is twice the baby's?", "How far must the dog walk from where it started to the food bowl?"],
        after=["2.2", "2.3"]),   # the options show 2.2's 12 m and 2.3's 0,17 m·s⁻¹
]

# ---- QUESTION 3, the question paper page 8 and the memo pages 3-5 ----
UV_Q = "What type of motion (motion with uniform velocity or uniformly accelerated motion) is represented by the following interval: "
q3 = [
    rub("3.1", "Distinguish between motion with uniform velocity and uniformly accelerated motion.", 4, [
        "Motion with uniform velocity: motion at constant velocity / motion with zero or no acceleration. (2)",
        "Uniformly accelerated motion: motion with constant acceleration / velocity changes with the same amount during each time interval / motion "
        "during which the velocity changes with a constant amount per unit time. (2)"],
        ["Does the athlete cover the same distance in every time interval when the velocity is uniform?",
         "What does 'accelerated' tell you about the velocity, and what does 'uniformly' add?"], each=2),
    mcq("3.2.1", UV_Q + "A to B?", ["Motion with uniform velocity", "Uniformly accelerated motion"], 0,
        ["How far does the athlete move in each 1,5 s interval from A to B?", "Are those distances equal, or does each one grow?"], marks=1),
    mcq("3.2.2", UV_Q + "B to C?", ["Motion with uniform velocity", "Uniformly accelerated motion"], 1,
        ["How far does the athlete move in each 1,5 s interval from B to C?", "Are those distances equal, or does each one grow?"], marks=1),
    draw("3.3", "Use the information in the diagram above to draw an accurate position versus time graph on the graph paper on the attached ANSWER SHEET.", 5, [
        ["x-axis (time) and its unit (s) correctly labelled", 1], ["y-axis (position) and its unit (m) correctly labelled", 1],
        ["2 points correctly plotted and joined", 1], ["Shape of the graph from 0 s to 3 s: a straight line", 1],
        ["Shape of the graph from 3 s to 7,5 s: curved", 1]],
        ["Which quantity goes on each axis of a position versus time graph?", "Plot the six (time; position) pairs: where is the graph straight, and where does it bend?"],
        memo="The memo's graph plots (0 s; 0 m), (1,5 s; 3 m), (3 s; 6 m), (4,5 s; 12 m), (6 s; 21 m) and (7,5 s; 33 m).",
        after=["3.2.1", "3.2.2"]),   # its shape criteria show the motion in each interval (3.2's answers)
    rub("3.4", "Define the term instantaneous velocity in words.", 2, [
        "Rate of change in position. (2)", "OR — Displacement divided by a very small time interval. (2)", "OR — Velocity at a particular time. (2)"],
        ["Is instantaneous velocity measured over a long time interval or at one moment?", "How does it differ from the average velocity over the whole race?"],
        each=2),
    draw("3.5", "On the graph drawn for QUESTION 3.3, show how you would determine the instantaneous velocity.", 2, [
        ["A tangent drawn to the curve at the chosen time", 2]],
        ["What does the gradient of a position versus time graph give?", "How can you find the gradient of a curve at one point, when the gradient keeps changing?"],
        memo="The memo draws the tangent to the curve near 6 s.",
        after=["3.3"]),   # its criterion shows the graph's curve (3.3's shape)
    work("3.6", "Calculate the velocity of the athlete at 3 s.", 4, [
        "v = {Δx}/{Δt}\nv = {12 − 6}/{4,5 − 3}\nv = 4 m·s⁻¹ right",                # the interval after 3 s (wrong part)
        "v = {Δt}/{Δx}\nv = {3 − 0}/{6 − 0}\nv = 0,5 m·s⁻¹ right",                 # the formula upside down
        "v = {Δx}/{Δt}\nv = {6 − 0}/{3 − 0}\nv = 2 m·s⁻¹ left",                    # the direction slip
        "v = {Δx}/{Δt}\nv = {6 − 0}/{3 − 0}\nv = 2 m·s⁻¹ right"], 3,               # the memo
        ["What kind of motion does the athlete have from 0 s to 3 s?", "Read the positions at 0 s and at 3 s: which way is the athlete moving?"]),
]

# ---- QUESTION 4, the question paper page 9 and the memo pages 5-6 ----
q4 = [
    rub("4.1", "Define the term acceleration in words.", 2, ["The rate of change of velocity. (2)"],
        ["Think of a car speeding up: which of its quantities is changing?", "How is acceleration different from velocity?"],
        each=2),
    work("4.2.1", "Calculate the time it takes car A to come to rest.", 4, [
        "vf = vi + aΔt\n0 = 15 + (4,5)Δt\nΔt = −3,33 s",                           # the sign of the acceleration dropped
        "vf = vi + aΔt\n0 = 15 + (−4,5)Δt\nΔt = 3,33 s",                           # the memo (its first form)
        "vf = vi + aΔt\n0 = 30 + (−4,5)Δt\nΔt = 6,67 s",                           # car B's speed (the wrong body)
        "vf = vi + aΔt\n0 = 15 + (−4,5)Δt\nΔt = 0,30 s"], 1,                       # rearranged upside down (4,5 ÷ 15)
        ["What is car A's final velocity when it comes to rest?", "Which equation of motion links vi, vf, a and Δt?"]),
    work("4.2.2", "Calculate the stopping distance of car A.", 4, [
        "vf² = vi² + aΔx\n0² = 15² + (−4,5)Δx\nΔx = 50 m",                         # the 2 left out of the formula
        "vf² = vi² + 2aΔx\n0² = 15 + 2(−4,5)Δx\nΔx = 1,67 m",                      # vi not squared
        "vf² = vi² + 2aΔx\n0² = 15² + 2(4,5)Δx\nΔx = −25 m",                       # the sign of the acceleration dropped
        "vf² = vi² + 2aΔx\n0² = 15² + 2(−4,5)Δx\nΔx = 25 m"], 3,                   # the memo (OPTION 1; its OPTION 2 from 3,33 s: 24,98 m)
        ["Which equation of motion uses vi, vf and a, without the time?", "The acceleration is negative: what sign must the stopping distance have?"]),
    work("4.3", "Which car (A or B) has the longer stopping distance? Support the answer with a calculation.", 6, [
        "vf² = vi² + 2aΔx\n0² = 30² + 2(−4,5)Δx\nΔx = 100 m\nCar B has the longer stopping distance (100 m > 25 m)",            # the memo (OPTION 1)
        "vf² = vi² + 2aΔx\n0² = 30 + 2(−4,5)Δx\nΔx = 3,33 m\nCar A has the longer stopping distance (25 m > 3,33 m)",            # vi not squared
        "vf² = vi² + aΔx\n0² = 30² + (−4,5)Δx\nΔx = 200 m\nCar B has the longer stopping distance (200 m > 25 m)",               # the 2 left out
        "Δx = viΔt + ½aΔt²\nΔx = (30)(3,33) + ½(−4,5)(3,33)²\nΔx = 74,95 m\nCar B has the longer stopping distance (74,95 m > 25 m)"], 0,
        # ^ car A's stopping time used for car B (a value from the wrong body)
        ["What changes when you repeat 4.2.2's calculation for car B?", "How does car B's stopping distance compare with car A's?"],
        after=["4.2.1", "4.2.2"]),   # the options show 4.2.1's 3,33 s and 4.2.2's 25 m
    rub("4.4", "What conclusion can be made about the relationship between speed and stopping distance?", 2, [
        "The greater/larger the speed, the larger the stopping distance (1) if acceleration is constant (1)."],
        ["How do the two cars' speeds and their stopping distances compare?", "Which quantity was the same for both cars?"], each=2,
        after=["4.3"]),   # its right card (the faster car stops in the longer distance) names 4.3's car
]

# ---- QUESTION 5, the question paper page 10 and the memo pages 6-7 ----
q5 = [
    rub("5.1", "Define the term gravitational potential energy in words.", 2, [
        "The energy an object has because of its position in the gravitational field (1) relative to some reference point (1)."],
        ["Does this energy come from the object's motion or from its position?", "Why must you choose a zero level, such as the ground, before you can calculate it?"], each=2),
    work("5.2", "Calculate the gravitational potential energy of the skater just before he skates down the ramp.", 3, [
        "Ep = mgh\nEp = (65)(4,5)\nEp = 292,5 J",                                  # g left out
        "Ep = ½mgh\nEp = ½(65)(9,8)(4,5)\nEp = 1 433,25 J",                         # the ½ of Ek put in (wrong formula)
        "Ep = mgh\nEp = (65)(9,8)(4,5)\nEp = 2 866,5 J",                            # the memo
        "Ep = mgh\nEp = (65)(10)(4,5)\nEp = 2 925 J"], 2,                           # g taken as 10, not the data sheet's 9,8
        ["Which formula gives the gravitational potential energy?", "At what height does he start, and which value of g does the data sheet give?"]),
    rub("5.3", "State the principle of conservation of mechanical energy in words.", 2, [
        "The net/total mechanical energy (sum of kinetic and gravitational potential energy) in an isolated/closed system (1) remains constant / is "
        "conserved (1)."],
        ["Which two energies make up mechanical energy?", "What kind of system does the principle need: one with friction, or one on which no external forces act?"], each=2),
    work("5.4", "Use the principle stated in QUESTION 5.3 to calculate the magnitude of the velocity of the skateboarder when he reaches the ground at point X.", 4, [
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + mv²\n(65)(9,8)(4,5) = 0 + (65)v²\nv = 6,64 m·s⁻¹",          # the ½ left out of Ek
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n(65)(9,8)(4,5) = 0 + ½(65)v²\nv = 88,20 m·s⁻¹",       # the square root not taken
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n(65)(9,8)(6) = 0 + ½(65)v²\nv = 10,84 m·s⁻¹",         # Y's 6 m (the wrong point)
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n(65)(9,8)(4,5) = 0 + ½(65)v²\nv = 9,39 m·s⁻¹"], 3,   # the memo
        ["Which energies does he have at the top, starting from rest, and which at X on the ground?",
         "Set the mechanical energy at the top equal to that at X: which quantity do you solve for?"],
        after=["5.2"]),   # the options show 5.2's substitution (65)(9,8)(4,5)
    work("5.5", "Will the skateboarder be able to reach point Y if he were to remain on his skateboard? Write YES or NO and support the answer with a "
         "relevant calculation.", 5, [
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + mv²\n(65)(9,8)h + 0 = 0 + 65 × (9,39)²\n637h = 5 731,19\nh = 9,00 m\n"
        "Yes: h = 9,00 m > 6 m",                                                    # the ½ left out of Ek
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n(65)(9,8)h + 0 = 0 + ½ × 65 × (9,39)²\n637h = 2 865,6\nh = 4,50 m\n"
        "No: h = 4,50 m < 6 m",                                                     # the memo (OPTION 1; it prints h = 4,49 m: flagged)
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n(65)h + 0 = 0 + ½ × 65 × (9,39)²\n65h = 2 865,6\nh = 44,09 m\n"
        "Yes: h = 44,09 m > 6 m",                                                   # g left out: the mass used as the weight
        "(Ep + Ek)top = (Ep + Ek)bottom\nmgh + 0 = mgh + ½mv²\n(65)(9,8)h + 0 = 0 + ½ × 65 × 9,39\n637h = 305,18\nh = 0,48 m\n"
        "No: h = 0,48 m < 6 m"], 1,                                                 # v not squared (the working decides, not the "No")
        ["With no friction, how high can his kinetic energy at X lift him?", "How does that height compare with the height of Y?"],
        after=["5.4"]),   # the options show 5.4's 9,39 m·s⁻¹
]

# ---- QUESTION 6, the question paper page 11 and the memo pages 7-8 ----
q6 = [
    rub("6.1", "Write down ONE difference and ONE similarity between wave P and wave Q.", 2, [
        "Difference: amplitudes (1)", "Similarity: wavelength / period / frequency / transverse (any one) (1)"],
        ["Which features of a wave can you read from this graph?", "Which of those features do P and Q share, and which differ?"]),
    # the memo accepts four pairs (A and B, C and D, B and C, A and D): one of them beside the two in-phase pairs, the only wrong ones
    mcq("6.2.1", "For wave pattern P, write down two points that are out of phase.", ["A and C", "B and D", "A and B"], 2,
        ["Points in phase are at the same position in their cycles: where on wave P are A, B, C and D?", "Which pair is NOT at the same position in its cycle?"],
        marks=1),
    num("6.2.2", "For wave pattern P, write down the amplitude of the wave.", 15, 0, "mm",
        ["Is the amplitude measured from the rest position, or from a crest to a trough?", "Which scale gives the position, and where is the rest position on it?"]),
    rub("6.3", "Define the term frequency of the wave in words.", 2, ["The number of waves/wave pulses (1) passing a point per second (1)."],
        ["Frequency is measured in hertz: what is one hertz?", "How is frequency different from the period of a wave?"], each=2),
    work("6.4.1", "For wave pattern Q, calculate the frequency of the wave.", 3, [
        "f = {1}/{T}\nf = {1}/{3,0}\nf = 0,33 Hz",                                  # two waves' time taken as the period
        "f = {1}/{T}\nf = {1}/{0,75}\nf = 1,33 Hz",                                 # half a wave's time taken as the period
        "f = {1}/{λ}\nf = {1}/{0,1}\nf = 10 Hz",                                    # the wavelength used for the period (wrong formula)
        "f = {1}/{T}\nf = {1}/{1,5}\nf = 0,67 Hz"], 3,                              # the memo
        ["How long does wave Q take to complete one full wave?", "How are frequency and period related?"]),
    work("6.4.2", "For wave pattern Q, calculate the speed of the wave.", 3, [
        "v = fλ\nv = (0,67)(100)\nv = 67 m·s⁻¹",                                    # 100 mm not converted to metres
        "v = {f}/{λ}\nv = {0,67}/{0,1}\nv = 6,7 m·s⁻¹",                             # the formula upside down
        "v = fλ\nv = (0,67)(0,1)\nv = 0,067 m·s⁻¹",                                 # the memo (OPTION 1)
        "v = fλ\nv = (0,67)(0,01)\nv = 0,0067 m·s⁻¹"], 2,                           # Q's 10 mm amplitude taken as the wavelength
        ["Which wave equation links speed, frequency and wavelength?", "The graph gives the wavelength in millimetres: what is it in metres?"],
        after=["6.4.1"]),   # the options show 6.4.1's 0,67 Hz
]

# ---- QUESTION 7, the question paper page 12 and the memo page 8 ----
q7 = [
    rub("7.1.1", "For the investigation, write down the investigative question.", 2, [
        "What is the relationship between the speed of sound and temperature? (2)", "OR — How will the temperature affect the speed of sound? (2)",
        "OR — What is the relationship between the time taken for the sound to travel and temperature? (2)"],
        ["Which quantity did they change, and which did they measure?", "An investigative question asks about the relationship between those two: how would you word it?"],
        each=2, notes=["Criteria: dependent and independent variables correctly identified (1); a question about the relationship between them (1)."]),
    term("7.1.2", "For the investigation, write down the independent variable.", ["Temperature"],
         ["Which quantity did the experimenters choose to change from run to run?", "Is it the cause or the effect?"]),
    term("7.1.3", "For the investigation, write down the dependent variable.", [
        "Speed of sound", "Speed", "Time taken for the sound to travel", "Time taken"],   # the memo ticks "Speed"; its "/" form: the time taken
         ["Which quantity was measured each time the conditions were changed?", "Is it the cause or the effect?"]),
    work("7.2", "Calculate the speed of sound at 20 °C.", 3, [
        "v = {Δx}/{Δt}\nv = {50}/{0,146}\nv = 342,47 m·s⁻¹",                        # the memo
        "v = {Δx}/{Δt}\nv = {50}/{0,145}\nv = 344,83 m·s⁻¹",                        # the 25 °C time (the wrong row)
        "v = {Δt}/{Δx}\nv = {0,146}/{50}\nv = 2,92 × 10⁻³ m·s⁻¹",                   # the formula upside down
        "v = {Δx}/{Δt}\nv = {100}/{0,146}\nv = 684,93 m·s⁻¹"], 0,                   # the distance doubled, as if the sound went there and back
        ["How far did the sound travel, and how long did it take at 20 °C?", "Which formula links distance, time and speed?"]),
    rub("7.3", "Write down a conclusion for the investigation.", 2, [
        "The speed of sound increases / time taken for the sound to travel decreases / as the temperature increases. (2)"],
        ["Read down the table: how does the time change as the temperature rises?", "Over the same 50 m, what does that tell you about the speed?"], each=2),
    term("7.4", "The person who beat the drum, noticed that the sound reflected back after a while. Name the term used to describe the reflection of sound waves.",
         ["Echo"], ["What do you hear when you shout towards a distant cliff or wall?", "Is it the sound you made, coming back to you?"]),
]

# ---- QUESTION 8, the question paper page 13 and the memo pages 8-9 ----
EM_Q = "A certain type of electromagnetic radiation has a wavelength of 600 x 10⁻¹⁰ m. "
q8 = [
    term("8.1", "How are electromagnetic waves generated?", ["Accelerating charges", "By accelerating charges", "Accelerating charge"],
         ["Which particles are involved in producing electromagnetic waves?", "Do charges at rest, or at a constant velocity, produce them?"]),
    term("8.2", "What type of electromagnetic radiation has the highest energy?", ["Gamma rays", "Gamma radiation", "Gamma"],
         ["How is the energy of a photon related to its frequency?", "Which type in the table has the highest frequencies?"]),
    rub("8.3", "Explain the answer to QUESTION 8.2.", 2, [
        "It has the highest frequency (1)", "Energy is directly proportional to frequency / E α f (1)"],
        ["Where is the radiation you chose in 8.2 in the table?", "Which equation links a photon's energy to its frequency?"],
        after=["8.2"]),   # its cards name gamma rays, 8.2's answer
    work("8.4.1", EM_Q + "Identify the type of electromagnetic radiation by performing a calculation.", 4, [
        "c = fλ\n3 × 10⁸ = f(600 × 10⁻¹⁰)\nf = 5 × 10¹⁵ Hz\nVisible light",          # the table misread: 5 x 10¹⁵ Hz is above 10¹⁵ Hz
        "c = fλ\n3 × 10⁸ = f(6 × 10⁻¹⁰)\nf = 5 × 10¹⁷ Hz\nX-rays",                   # 600 x 10⁻¹⁰ written as 6 x 10⁻¹⁰ (a power slip)
        "c = fλ\n3 × 10⁸ = f(600)\nf = 5 × 10⁵ Hz\nRadio waves",                      # the 10⁻¹⁰ left out of the wavelength
        "c = fλ\n3 × 10⁸ = f(600 × 10⁻¹⁰)\nf = 5 × 10¹⁵ Hz\nUltraviolet"], 3,        # the memo (OPTION 1)
        ["Which equation links the speed of light, frequency and wavelength?", "Once you have the frequency, which range in the table contains it?"]),
    rub("8.4.2", EM_Q + "State ONE application of the type of radiation identified in QUESTION 8.4.1.", 1, [
        "Sterilisation of medical equipment / suntan beds / security in currency / astronomy (any one; any relevant use) (1)"],
        ["What did you identify in 8.4.1?", "Where in everyday life, medicine or industry is that radiation used?"],
        after=["8.4.1"]),   # its right cards are uses of ultraviolet, 8.4.1's answer
]

# ---- QUESTION 9, the question paper page 14 and the memo pages 9-10 ----
q9a = [
    term("9.1", "Write down the term describing a material that is easily magnetised.", ["Ferromagnetic", "Ferromagnetic material"],
         ["Iron, nickel and cobalt are examples of this kind of material: what is it called?", "How does this kind of material behave near a magnet?"]),
    mcq("9.2", "Which ONE of the bars (A or B) is made of iron?", ["A", "B"], 1,
        ["Which bar leans towards a magnet, and which hangs straight down?", "Is gold attracted by a magnet?"], marks=1),
    mcq("9.3", "Determine the polarity of bar B closest to bar magnet Y. Write only NORTH or SOUTH.", ["North", "South"], 1,
        ["X's left end is a north pole: what is its right end?", "X and Y push each other apart: what are Y's two ends, and what does Y induce in the iron next to it?"],
        marks=1),
    rub("9.4", "Explain the answer to QUESTION 9.3.", 2, [
        "Magnet X repels Y / south pole (1)", "Magnet Y attracts B / south pole at B (1)"],
        ["Do X and Y attract or repel each other, and what does that say about the poles facing each other?", "Does Y attract or repel bar B?"],
        after=["9.2", "9.3"]),   # its cards say B is attracted (iron, 9.2) and name B's south pole (9.3)
    draw("9.5", "Sketch the magnetic field pattern around bar magnet X.", 3, [
        ["Correct direction of the field lines: from the north pole to the south pole (X's north pole is at its left end)", 1],
        ["Shape of the magnetic field", 1], ["No field lines crossing each other", 1]],
        ["Which way do magnetic field lines point outside a magnet?", "Where are the field lines closest together, and can two lines ever cross?"]),
]
q9b = [
    mcq("9.6.1", "How will the change in the position of the attachment affect the final distance of separation between the bars? Write only GREATER "
        "THAN 5 cm, LESS THAN 5 cm or REMAINS at 5 cm.", ["Greater than 5 cm", "Less than 5 cm", "Remains at 5 cm"], 1,
        ["With bars A and B removed, which forces act on magnet Y now?", "How does moving the attachment points closer together change where the magnets hang?"],
        marks=1),
    rub("9.6.2", "Explain the answer to QUESTION 9.6.1.", 2, [
        "Magnitude of magnetic force is inversely proportional to the distance (1). B is no longer attracting Y to the right (1).",
        "OR — A decrease in distance increases the magnetic force (1). B is no longer attracting Y to the right (1)."],
        ["How does the magnetic force between two magnets change as the distance between them changes?",
         "What happened to the bars that hung next to X and Y?"],
        after=["9.6.1"]),   # its cards (B no longer pulls Y to the right) point to 9.6.1's answer
]

# ---- QUESTION 10, the question paper page 15 and the memo pages 10-11 ----
TOUCH = "The spheres are allowed to touch each other. After touching, they move away from each other. "
q10 = [
    work("10.1", "Calculate the magnitude of the charge on sphere Y.", 3, [
        "n = {e}/{Q}\n30 = {−1,6 × 10⁻¹⁹}/{Q}\nQ = −5,33 × 10⁻²¹ C",                 # the formula upside down
        "n = {Q}/{e}\n30 = {Q}/{9,11 × 10⁻³¹}\nQ = 2,73 × 10⁻²⁹ C",                  # the electron's mass for its charge (wrong constant)
        "n = {Q}/{e}\n30 = {Q}/{−1,6 × 10⁻¹⁹}\nQ = −4,8 × 10⁻¹⁸ C",                  # the memo (it also ACCEPTS 4,8 x 10⁻¹⁸ C)
        "n = {Q}/{e}\n30 = {Q}/{−1,6 × 10¹⁹}\nQ = −4,8 × 10²⁰ C"], 2,                # 10⁻¹⁹ written 10¹⁹ (a power slip)
        ["Which equation links a charge, the number of electrons and the charge on one electron?", "Which value of e does the data sheet give?"]),
    rub("10.2", "The spheres are now released and they move towards each other. Give a reason why spheres X and Y move towards each other.", 2, [
        "Unlike/opposite charges (1) attract (1)."],
        ["What are the signs of the charges on X and on Y?", "Which rule about electric charges explains the movement?"], each=2),
    rub("10.3", TOUCH + "State the principle of conservation of charge in words.", 2, [
        "The net/total charge in an isolated/closed system remains constant/is conserved. (2)"],
        ["What happens to the total charge when the spheres touch and share it?", "What kind of system must it be: can charge enter or leave it?"], each=2,
        notes=["If any of the underlined words/phrases (net/total charge, isolated/closed system, constant/conserved) are omitted in the correct context: minus 1 mark."]),
    work("10.4", TOUCH + "Calculate the charge on each sphere after they have separated.", 4, [
        "Qnet = Q1 + Q2\nQnet = 4 × 10⁻¹⁸ + (−4,8 × 10⁻¹⁸)\nQnet = −8 × 10⁻¹⁹ C",                    # the total not shared (not halved)
        "Qnet = {Q1 + Q2}/{2}\nQnet = {4 × 10⁻¹⁸ + (−4,8 × 10⁻¹⁸)}/{2}\nQnet = −4 × 10⁻¹⁹ C",       # the memo
        "Qnet = {Q1 + Q2}/{2}\nQnet = {4 × 10⁻¹⁸ + (−1,6 × 10⁻¹⁹)}/{2}\nQnet = 1,92 × 10⁻¹⁸ C",     # one electron's charge for Y's (wrong value)
        "Qnet = {Q1 + Q2}/{2}\nQnet = {4 × 10⁻¹⁸ + (−4,8 × 10⁻¹⁸)}/{2}\nQnet = −4 × 10⁻¹⁸ C"], 1,  # −0,8 x 10⁻¹⁸ taken as −8 x 10⁻¹⁸
        # (no option uses +4,8 x 10⁻¹⁸ C for Y: the memo accepts that magnitude in 10.1 and marks 10.4 positively from it)
        ["What is the total charge of the two spheres together?", "How do two identical spheres that touch share their total charge?"],
        after=["10.1"]),   # the options show 10.1's −4,8 x 10⁻¹⁸ C
]

# ---- QUESTION 11, the question paper pages 16-17 and the memo pages 11-12 ----
S_OPEN, S_SHUT = "Switch S is OPEN. Write down the reading on the following: ", "Switch S is now CLOSED. "
q11a = [
    num("11.1.1(a)", S_OPEN + "Voltmeter (V1)", 24, 0, "V",
        ["With S open, is there a complete path for charge to flow?", "What does a voltmeter across a battery measure when no current flows?"]),
    num("11.1.1(b)", S_OPEN + "Ammeter (A1)", 0, 0, "A",
        ["With S open, is there a complete path for charge to flow?", "What does an ammeter in series measure?"]),
    work("11.1.2", S_SHUT + "Calculate the equivalent resistance of the circuit.", 4, [
        "Rp = R1 + R2 = 8 + 8\nRp = 16 Ω\nRT = Rs + Rp = 8 + 16\nRT = 24 Ω",                        # the parallel pair added like series
        "{1}/{Rp} = {1}/{R1} + {1}/{R2} = {1}/{8} + {1}/{8}\nRp = 0,25 Ω\nRT = Rs + Rp = 8 + 0,25\nRT = 8,25 Ω",   # 1/Rp not turned over
        "{1}/{Rp} = {1}/{R1} + {1}/{R2} = {1}/{8} + {1}/{8}\nRp = 4 Ω\nRT = Rp\nRT = 4 Ω",          # the series bulb left out (wrong part)
        "{1}/{Rp} = {1}/{R1} + {1}/{R2} = {1}/{8} + {1}/{8}\nRp = 4 Ω\nRT = Rs + Rp = 8 + 4\nRT = 12 Ω"], 3,   # the memo (OPTION 1)
        ["Which two bulbs are in parallel, and which bulb is in series with them?", "Which do you work out first: the parallel pair, or the series bulb?"]),
    work("11.1.3", S_SHUT + "Calculate the reading on voltmeter V2.", 3, [
        "V divides in a ratio 8 : 4 (series)\nV2 = {8}/{12} × 24\nV2 = 16 V",                      # the memo (OPTION 1)
        "V divides in a ratio 4 : 8 (series)\nV2 = {4}/{12} × 24\nV2 = 8 V",                       # the shares swapped
        "V divides equally (series)\nV2 = {1}/{2} × 24\nV2 = 12 V",                                # an equal split
        "V divides in a ratio 8 : 4 (series)\nV2 = {8}/{4} × 24\nV2 = 48 V"], 0,                   # the two resistances divided, not the share
        ["How is the battery's 24 V shared between the series bulb and the parallel pair?", "How does a series circuit share its potential difference between resistances?"],
        after=["11.1.2"]),   # the options show 11.1.2's 12 Ω and 4 Ω
    rub("11.1.4", S_SHUT + "How do the readings on ammeters A2 and A3 compare with each other?", 1, ["A2 = A3 (1)"],
        ["How do the resistances of the two parallel branches compare?", "Is the potential difference across each branch the same?"]),
]
q11b = [
    rub("11.2.1", "Write down the relationship between the resistance and the length of the conducting wire.", 1, [
        "Resistance is directly proportional to the length of the conducting wire. (1)", "OR — As the length of the wire increases, the resistance increases. (1)"],
        ["What shape is the graph, and where does it start?", "What happens to the resistance when the length doubles?"]),
    num("11.2.2", "Determine the resistance of wire with a length of 30 mm.", 1.35, 0.05, "Ω",
        ["Find 30 mm on the length axis: where is the line straight above it?", "Read across to the resistance axis: between which marked values does it fall?"]),
]

T_TABLE = {"head": ["TEMPERATURE (°C)", "TIME (s)"],
           "rows": [["0", "0,151"], ["5", "0,150"], ["10", "0,148"], ["15", "0,147"], ["20", "0,146"], ["25", "0,145"]]}
EM_TABLE = {"head": ["TYPE OF RADIATION", "FREQUENCY (Hz)"],
            "rows": [["Radio waves", "10⁵–10¹⁰"], ["Microwaves", "10¹⁰–10¹¹"], ["Infrared", "10¹¹–10¹⁴"], ["Visible light", "10¹⁴–10¹⁵"],
                     ["Ultraviolet", "10¹⁵–10¹⁶"], ["X-rays", "10¹⁶–10¹⁸"], ["Gamma rays", "10¹⁸–10²¹"]]}
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 18,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "1.10", "title": "Question 1.10", "kind": "Multiple choice", "marks": 2, "lead": "Study the following wave patterns:",
     "figure": fig("1.10", "Four wave patterns, numbered 1 to 4, each drawn across a grid of the same size."), "items": q1b},
    {"id": "2", "title": "Question 2", "kind": "Displacement and velocity", "marks": 12,
     "lead": "A baby leaves a bowl of food on the floor and crawls westwards to fetch a toy placed 5 m away. At the same time a dog walks eastwards towards "
             "the baby. It takes the baby 30 s to reach the toy. The dog walks past the toy to eat the baby's food in the bowl.",
     "figure": fig("Q2", "A dog on the left, a toy 7 m to its right, and the baby with the food bowl 5 m to the right of the toy, all on one straight "
                   "line; a compass shows north up and east to the right."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Motion and graphs", "marks": 19,
     "lead": "The diagram below shows the positions of an athlete at different time intervals during a race.",
     "figure": fig("Q3", "An athlete running to the right along a number line, shown at t = 0 s, 1,5 s, 3,0 s, 4,5 s, 6,0 s and 7,5 s at positions "
                   "0, 3 m, 6 m, 12 m, 21 m and 33 m; point A is at 0, B at 6 m and C at 33 m."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Equations of motion", "marks": 18,
     "lead": "Two cars, A and B, are moving at speeds of 15 m·s⁻¹ and 30 m·s⁻¹ in the same direction. They are side by side when both drivers observe "
             "an obstruction ahead of them, as shown in the diagram below.\n\nBoth drivers apply their brakes and accelerate at −4,5 m·s⁻² until both "
             "cars come to rest. Ignore the reaction time of the drivers.",
     "figure": fig("Q4", "Car A at 15 m·s⁻¹ and car B at 30 m·s⁻¹, side by side in two lanes, both moving to the right towards an obstruction; a "
                   "double arrow shows the distance from car B to the obstruction."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Mechanical energy", "marks": 16,
     "lead": "A skateboarder, starting from the top of a ramp 4,5 m above the ground, skates down the ramp, as shown in the diagram below. The mass of "
             "the skateboarder and his board is 65 kg. Ignore the effects of friction.",
     "figure": fig("Q5", "A skateboarder at the top of a ramp 4,5 m above the ground; the ramp curves down to its lowest point X on the ground and up "
                   "again to point Y, 6 m above the ground."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Transverse waves", "marks": 12, "lead": "Study the two transverse waves, P and Q, as shown below.",
     "figure": fig("Q6", "Position (mm), from −15 to 15, up against time (s) across, the time axis marked at 1,5 and 3,0. Two waves start at the "
                   "origin: wave P, a solid line, and wave Q, a dashed line. P's crests are labelled A and C and its troughs B and D; a double arrow "
                   "labelled 100 mm runs from B to D."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Sound", "marks": 10,
     "lead": "Experiments were done to investigate the effect of temperature on the speed of sound. One person beat a drum while another person, who was "
             "standing 50 m away from the sound source, recorded the time travelled by the sound.\n\nThey performed the experiment at different "
             "temperatures at different times of the day. They recorded their findings in the table below.",
     "table": T_TABLE, "figure": fig("Q7", "A person holding a stopwatch on the left and a person beating a drum on the right, 50 m apart."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Electromagnetic radiation", "marks": 9,
     "lead": "The types of electromagnetic radiation are arranged according to frequency in the table below.", "table": EM_TABLE, "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Magnetism", "marks": 8,
     "lead": "Four metallic bars, suspended freely from a ceiling, interact, as shown in the diagram below. The points of attachment of X and Y on the "
             "ceiling are 4 cm apart.\n\nThe two bars in the middle are bar magnets (X and Y) and the distance between them is 5 cm. One of the bars "
             "(A or B) is made of iron and the other is made of gold.",
     "figure": fig("Q9a", "Four bars hang from one ceiling: bar A on the left hangs straight down; bar magnets X (its left end marked N) and Y hang "
                   "with their strings spread apart, their attachment points 4 cm apart and the bars 5 cm apart; bar B on the right hangs with its "
                   "string leaning towards Y."), "items": q9a},
    {"id": "9.6", "title": "Question 9.6", "kind": "Magnetic forces", "marks": 3,
     "lead": "Bars A and B are now removed and the points of attachment are now 2 cm, as shown in the diagram below.",
     "figure": fig("Q9b", "Bar magnets X and Y hang from the ceiling, their attachment points 2 cm apart, with a double arrow between the two bars."),
     "items": q9b},
    {"id": "10", "title": "Question 10", "kind": "Electrostatics", "marks": 11,
     "lead": "Two identical insulated spheres, X and Y, suspended by threads from a ceiling, are held at a small distance apart, as shown in the diagram "
             "below.\n\nSphere X carries a charge of + 4 x 10⁻¹⁸ C, while sphere Y has an excess of 30 electrons.",
     "figure": fig("Q10", "Sphere X, marked + and labelled +4 x 10⁻¹⁸ C, and sphere Y, marked −, hang side by side on threads from a ceiling."),
     "items": q10},
    {"id": "11.1", "title": "Question 11.1", "kind": "Electric circuits", "marks": 10, "lead": "Consider the circuit diagram below.",
     "figure": fig("Q11a", "A 24 V battery with voltmeter V1 across it, ammeter A1 and switch S in the main circuit; an 8 Ω bulb with voltmeter V2 "
                   "across it, in series with two 8 Ω bulbs in parallel, one branch with ammeter A2 and the other with ammeter A3."), "items": q11a},
    {"id": "11.2", "title": "Question 11.2", "kind": "Resistance of a wire", "marks": 2,
     "lead": "The graph below shows the relationship between the resistance and the length of the conducting wire.",
     "figure": fig("Q11b", "Resistance (Ω), 0 to 3,5, up against length of wire (mm), 0 to 70, across, on fine graph paper: a straight line drawn from "
                   "the origin."), "items": q11b},
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
    assert len(pool) == 1 or pool != list(range(len(pool))), (n, "every right card on top: an answer by position")
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "pool": pool, "count": count}


STATEMENTS = {
    # 2, either OR form: the wrong ones are distance, velocity, speed and position
    "2.1": (2, ["The difference in position (in space).", "The change in position of an object."],
               ["The total length of the path travelled by an object.", "The rate of change of position.", "The distance travelled per unit time.",
                "The position of an object relative to a reference point."]),
    # 2 + 2: one card for each kind of motion (its first reading), so two cards about one kind can never earn all four marks
    "3.1": (2, ["Motion with uniform velocity is motion at a constant velocity.", "Uniformly accelerated motion is motion with a constant acceleration."],
               ["Motion with uniform velocity is motion with a constant acceleration that is not zero.", "Uniformly accelerated motion is motion at a constant velocity.",
                "Uniformly accelerated motion is motion in which the position changes by the same amount in each time interval.",
                "Motion with uniform velocity is motion in which the speed stays the same while the direction keeps changing."]),
    # 2, any of the three OR forms: the wrong ones are the average velocity, the average speed, acceleration, displacement
    "3.4": (2, ["The rate of change in position.", "Displacement divided by a very small time interval.", "Velocity at a particular time."],
               ["The total displacement divided by the total time taken.", "The total distance travelled divided by the total time taken.",
                "The rate of change of velocity.", "The change in position of an object."]),
    # 2: the wrong ones are velocity, a change without "rate", speed, momentum
    "4.1": (2, ["The rate of change of velocity."],
               ["The rate of change of position.", "The change in velocity of an object.", "The distance travelled per unit time.",
                "The product of the mass of an object and its velocity."]),
    # 2 ticks in one statement (the relation, the condition): the wrong ones are the inverse, direct proportion (25 m -> 100 m when the
    # speed doubles), no relation, and the time to stop
    "4.4": (2, ["The greater the speed, the larger the stopping distance, if the acceleration is constant."],
               ["The greater the speed, the smaller the stopping distance, if the acceleration is constant.",
                "The stopping distance is directly proportional to the speed.", "The stopping distance does not depend on the speed.",
                "The greater the speed, the shorter the time taken to stop, if the acceleration is constant."]),
    # 2 ticks in one statement: the wrong ones are kinetic energy, mechanical energy, weight, power
    "5.1": (2, ["The energy an object has because of its position in the gravitational field relative to some reference point."],
               ["The energy an object has because of its motion.", "The sum of the kinetic energy and the gravitational potential energy of an object.",
                "The force with which the Earth attracts an object.", "The rate at which work is done against the gravitational force.",
                "The energy stored in a stretched or compressed spring."]),   # (a 5th wrong card: with five the right card came first)
    # 2: the wrong ones drop "isolated", keep only one energy constant, or make the total grow
    "5.3": (2, ["The total mechanical energy in an isolated system remains constant."],
               ["The total mechanical energy in a system remains constant even when friction acts on it.",
                "The kinetic energy of an object in an isolated system remains constant.",
                "The gravitational potential energy of an object in an isolated system remains constant.",
                "The total mechanical energy in an isolated system increases as an object falls.",
                "The total mechanical energy in an isolated system decreases as an object rises.",
                "The total mechanical energy in an isolated system is always zero."]),   # (6 wrong cards: with four or five the right one came first)
    # 1 + 1: the memo's difference (amplitudes) and its first similarity (wavelength); its other similarities (period, frequency, both
    # transverse) are true, so neither right cards (two similarities would earn both marks) nor wrong ones
    "6.1": (1, ["Difference: the amplitudes of wave P and wave Q are different.", "Similarity: wave P and wave Q have the same wavelength."],
               ["Difference: the wavelengths of wave P and wave Q are different.", "Similarity: wave P and wave Q have the same amplitude.",
                "Difference: wave P is transverse and wave Q is longitudinal.", "Difference: wave Q has a longer period than wave P."]),
    # 2 ticks in one statement: the wrong ones are period, wavelength, amplitude, speed
    "6.3": (2, ["The number of waves passing a point per second."],
               ["The time taken for one complete wave to pass a point.", "The distance between two consecutive crests.",
                "The maximum displacement of a particle from its rest position.", "The distance that a wave travels per second.",
                "The number of complete waves in a wave pattern.", "The time taken for a wave to travel one metre.",
                "The number of crests between two points one metre apart."]),   # (7 wrong cards: with four the right one came first, with five
                # or six third, as in 5.1 and 10.3)
    # 2, any of the memo's three questions: the wrong ones name another variable, reverse cause and effect, or ask about no variable
    "7.1.1": (2, ["What is the relationship between the speed of sound and temperature?", "How will the temperature affect the speed of sound?",
                  "What is the relationship between the time taken for the sound to travel and temperature?"],
                 ["What is the relationship between the speed of sound and the distance between the two people?",
                  "Does the loudness of the drum affect the speed of sound?", "How does the speed of sound affect the temperature?",
                  "What is the relationship between the temperature and the time of the day?"]),
    # 2, either "/" form: the wrong ones are the inverse trends, no trend, inverse proportion
    "7.3": (2, ["The speed of sound increases as the temperature increases.", "The time taken for the sound to travel decreases as the temperature increases."],
               ["The speed of sound decreases as the temperature increases.", "The time taken for the sound to travel increases as the temperature increases.",
                "The speed of sound does not depend on the temperature.", "The speed of sound is inversely proportional to the temperature."]),
    # 2 ticks: the highest frequency and E ∝ f. "Gamma rays have the shortest wavelength" is true and not the memo's: no card
    "8.3": (1, ["Gamma rays have the highest frequency.", "The energy of a photon is directly proportional to its frequency (E ∝ f)."],
               ["Gamma rays have the longest wavelength.", "The energy of a photon is inversely proportional to its frequency.",
                "Gamma rays travel faster in a vacuum than the other types of electromagnetic radiation.",
                "The energy of a photon is directly proportional to its wavelength."]),
    # 1, any of the memo's four uses of ultraviolet: the wrong ones are uses of microwaves, X-rays, infrared and radio waves
    "8.4.2": (1, ["Sterilisation of medical equipment.", "Suntan beds.", "Security in currency.", "Astronomy."],
                 ["Cooking food in a microwave oven.", "Taking images of broken bones.", "Night-vision cameras.", "Broadcasting radio signals."]),
    # 2 ticks: X repels Y (south pole), Y attracts B (south pole at B)
    "9.4": (1, ["Magnet X repels magnet Y, so the end of Y facing X is a south pole.", "Magnet Y attracts bar B, so the end of B facing Y is a south pole."],
               ["Magnet X attracts magnet Y, so the end of Y facing X is a north pole.", "Magnet Y repels bar B, so the end of B facing Y is a north pole.",
                "Like poles attract each other.", "Bar B hangs straight down because it is not magnetic."]),
    # 2 ticks: the force-distance relation (its first reading; the OR "a decrease in distance increases the force" says the same) and B gone
    "9.6.2": (1, ["The magnitude of the magnetic force is inversely proportional to the distance.", "Bar B no longer attracts magnet Y to the right."],
                 ["The magnitude of the magnetic force is directly proportional to the distance.", "Bar B now attracts magnet Y further to the right.",
                  "The magnetic force between X and Y does not depend on the distance between them.", "Magnets X and Y now attract each other."]),
    # 2 ticks in one statement: the wrong ones swap the rule, or blame any charge or the Earth's gravity
    "10.2": (2, ["Unlike (opposite) charges attract each other."],
                ["Like charges attract each other.", "Unlike charges repel each other.", "Charged objects always attract each other, whatever their charges.",
                 "The gravitational force of the Earth pulls the spheres towards each other."]),
    # 2: the wrong ones drop "isolated", create charge, make it zero, or keep each object's own charge
    "10.3": (2, ["The net charge in an isolated system remains constant."],
                ["The net charge in any system, isolated or not, remains constant.", "Charge can be created but cannot be destroyed.",
                 "The net charge of an isolated system is always zero.", "When two charged objects touch, each object keeps its own charge.",
                 "The net charge in an isolated system increases when two charged objects touch."]),   # (a 5th wrong card: with four the
                 # right card came first)
    # 1: the wrong ones make one branch's current larger, double, or the whole current
    "11.1.4": (1, ["The readings on A2 and A3 are equal (A2 = A3)."],
                  ["The reading on A2 is greater than the reading on A3.", "The reading on A3 is greater than the reading on A2.",
                   "The reading on A2 is twice the reading on A3.", "The reading on A2 is equal to the reading on A1."]),
    # 1, either OR form: the wrong ones are the inverse relations, no relation, the square
    "11.2.1": (1, ["Resistance is directly proportional to the length of the conducting wire.", "As the length of the wire increases, the resistance increases."],
                  ["Resistance is inversely proportional to the length of the conducting wire.", "As the length of the wire increases, the resistance decreases.",
                   "The resistance does not depend on the length of the wire.", "Resistance is directly proportional to the square of the length of the wire."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, laws, conclusions and explanations), so SORTS stays empty and sort_ is kept for parity.
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
            if _it.get("after"):   # its gate rides along
                _m["items"][_k]["after"] = _it["after"]
assert not [i["n"] for m in missions for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"

assert tuple(AUTHORED) == ("2.2", "2.3", "2.4", "3.6", "4.2.1", "4.2.2", "4.3", "5.2", "5.4", "5.5", "6.4.1", "6.4.2", "7.2", "8.4.1", "10.1", "10.4",
                           "11.1.2", "11.1.3"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["6.2.2", "11.1.1(a)", "11.1.1(b)", "11.2.2"], "only the read-offs stay typed numbers"
assert [i["n"] for i in ITEMS if i["t"] == "term"] == ["7.1.2", "7.1.3", "7.4", "8.1", "8.2", "9.1"]
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["3.3", "3.5", "9.5"]
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "2.4": ["2.2", "2.3"], "3.3": ["3.2.1", "3.2.2"], "3.5": ["3.3"], "4.3": ["4.2.1", "4.2.2"], "5.4": ["5.2"], "5.5": ["5.4"], "6.4.2": ["6.4.1"],
    "10.4": ["10.1"], "11.1.3": ["11.1.2"], "4.4": ["4.3"], "8.3": ["8.2"], "8.4.2": ["8.4.1"], "9.4": ["9.2", "9.3"], "9.6.2": ["9.6.1"]}
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn" and i["n"] in STATEMENTS]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2018", "total_marks": 150, "time": "2 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic physics errors (a sign or direction slip, a value "
                                                       "from the wrong body or part, a formula upside down or with a factor dropped, a power of "
                                                       "ten slipped, a unit not converted), 0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, "
                                                       "%d marks). 2.2 ('Determine the position', the memo's 12 m west with no working) plays as the "
                                                       "two distances added, then the position and its direction. 4.3 and 5.5 (decide by "
                                                       "calculation) end in the memo's conclusion; some wrong workings reach the same conclusion, so "
                                                       "the working decides. A value the memo also accepts is never a wrong option: 2.4's 36 s (the "
                                                       "unrounded speed), 4.2.2's 24,98 m (its OPTION 2), 10.1's +4,8 x 10⁻¹⁸ C (and 10.4 from it)."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.10", "kind": "memo_issue", "detail": "The memo accepts C/B: patterns 1, 3 and 4 have the same frequency (pitch), so '1 and 3' (B) "
                                                      "and '1 and 4' (C) are both right. Played as a pick of one with both right (Geography P2 Nov "
                                                      "2024 1.1.8's form), in a mission of its own so the wave patterns stay its figure (a pickn has "
                                                      "no figure of its own)."},
        {"n": "6.2.1", "kind": "no_fit", "detail": "'Two points that are out of phase': the memo accepts four pairs (A and B, C and D, B and C, A "
                                                   "and D). Played as a multiple choice of pairs: the memo's first (A and B) beside the only two "
                                                   "wrong pairs (A and C, B and D, both in phase); a fourth option would be a second right pair."},
        {"n": "5.5", "kind": "memo_issue", "detail": "The memo writes 637h = 2 865,6, h = 4,49 m; 2 865,6 / 637 = 4,4986, so h = 4,50 m (exactly "
                                                     "4,5 m, the start height, with the unrounded speed). The right option shows 4,50 m; the "
                                                     "conclusion (No: less than 6 m) is the memo's."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (formulas, the 1.7 signs and the 1.10 wave patterns are images); no API call."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions, laws, conclusions and the "
                                                    "investigative question (2.1, 3.4, 4.1, 4.4, 5.1, 5.3, 6.3, 7.1.1, 7.3, 10.2, 10.3, 11.1.4, "
                                                    "11.2.1) pick one card for their marks (an OR form is a second right card); 3.1 picks one "
                                                    "card for each kind of motion (2 + 2); the explanations ticked point by point (6.1, 8.3, 9.4, "
                                                    "9.6.2) pick the memo's points, 1 mark each; 8.4.2 picks one of the memo's four uses. 6.1's "
                                                    "other similarities (period, frequency, transverse) and 9.6.2's OR reading are neither right "
                                                    "nor wrong cards, so two cards for one point can never earn two marks." % len(PICKS)},
        {"n": "3.3", "kind": "no_fit", "detail": "Drawings (3.3 on the ANSWER SHEET's graph paper, 3.5 on that graph, 9.5) are done on paper and "
                                                 "self-checked against the memo's criteria."},
    ],
}
QTOTAL = {"1": 20, "2": 12, "3": 19, "4": 18, "5": 16, "6": 12, "7": 10, "8": 9, "9": 11, "10": 11, "11": 12}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter. Question 1's nine printed letters are the paper's (A3 B2 C4 D0) and five printed choices of two or three (3.2.1 A,
# 3.2.2 B, 9.2 B, 9.3 B, 9.6.1 B) can never be D, so an even paper needs D-heavy workings: the 18 workings sit at A4 B3 C4 D7, the paper
# within 2 of even, and the 27 four-option questions (Question 1's nine and the workings) at A7 B5 C8 D7
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
