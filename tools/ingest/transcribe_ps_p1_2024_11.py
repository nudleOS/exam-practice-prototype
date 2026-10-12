"""Physical Sciences P1 (Physics) Nov 2024, the whole paper (Questions 1 to 10), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets formulas and symbols as
images, so its text layer has gaps. Polished one subject at a time (Murci, 2026-10-10: "next subject: Physical Sciences").

  python tools/ingest/transcribe_ps_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P1 Nov 2024 Eng.pdf" "<...>/Physical Sciences P1 Nov 2024 MG Afr & Eng.pdf" --id ps-p1-2024-11 --from-json

How the memo's shapes map (Physical Sciences, Murci's rulings 2026-10-10; the patterns of Physical Sciences P1 Nov 2025):
  multiple choice -> mcq (options printed as a table -> optTable); a 2- or 3-way choice with no explanation -> mcq; one word the
  memo names -> term. 4.3.2 ("Write down the change in momentum of trolley A", 1 mark, no working) is a vector: its memo answer
  is "10,84 kg·m·s⁻¹ left/opposite direction", so it plays as a multiple choice of magnitude AND direction (a typed number could
  not take the direction, and a stem that printed the direction gave half the answer away).
  Every calculation ("Calculate", "Using ... ONLY, calculate", "Support your answer with a suitable calculation") -> authored
  multiple choice, `work`: the memo's FIRST working line by line (formula, substitution, the answer with its unit, and its
  direction or conclusion where the memo gives one) and three workings each built from a DIFFERENT realistic physics error (a
  sign or direction slip, g used wrongly or left out, a unit not converted, the wrong formula, a value from the wrong body or
  part), every number recomputed; 0 or full marks. A value the memo also accepts (its ranges) is never a wrong option.
  A definition or law ("Define / State / Write down the principle") and a one-statement answer (9.2, 9.3, 9.7) -> statements
  (STATEMENTS at the bottom: the memo's wording right, its OR / ACCEPT forms further right cards, the wrong cards a key condition
  dropped or swapped, the inverse relation, another law's or quantity's wording); a choice with its reason or an explanation
  (2.4, 6.2, 10.2.2, 10.3.2) -> statements, the choice and each memo point a card, 1 mark each as the memo ticks them. No memo
  here weighs two sides, so no part plays as a sort. "Draw a labelled free-body diagram" (2.2, 5.2) -> draw with build "forces"
  (2026-10-11: each force aimed from a dot from the same tray of seven, marked online as the memo marks it); another "Draw / Sketch"
  -> draw with the memo's criteria (self-checked, flagged no_fit). A part whose options, cards or criteria show an earlier part's answer opens only after it ("after"). A question whose
  diagram changes part-way is several missions (7, 9, 10).
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves (scratchpad figs24.py) and checked on a
contact sheet (sheet24.py)."""
import json
import re
from pathlib import Path

W, H = 595.44, 841.68
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.2": [3, 120, 425, 400, 575], "1.3": [4, 225, 170, 375, 280], "1.4": [4, 200, 490, 380, 585], "1.5": [5, 250, 135, 440, 232],
    "1.7": [6, 235, 145, 405, 282], "1.9": [7, 125, 135, 528, 320], "Q2": [8, 115, 222, 495, 563], "Q3": [9, 180, 220, 410, 388],
    "Q4": [10, 50, 238, 555, 393], "Q5": [11, 205, 198, 460, 306], "Q6": [12, 140, 225, 425, 375], "Q7a": [13, 190, 168, 418, 216],
    "Q7b": [13, 172, 312, 362, 372], "Q7c": [13, 185, 483, 432, 546], "Q8": [14, 100, 214, 478, 488], "Q9a": [15, 70, 142, 562, 292],
    "Q9b": [15, 100, 528, 570, 678], "Q10b": [16, 180, 252, 432, 378]}


# the paper's words inside a crop, painted white (measured from the PDF's text, 2026-10-12): Q2's stem's last line between the two
# drawings (the lead carries it) and 2.1's question under the graph
BLANK = {"Q2": [[107, 368.5, 404, 385], [105, 556, 268, 572]]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    f = {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}
    if name in BLANK:
        f["blank"] = [[round(a / W, 4), round(b / H, 4), round(c / W, 4), round(d / H, 4)] for a, b, c, d in BLANK[name]]
    return f


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points (key words, "... 0/2", ACCEPT limits): never scored, never shown.
# The rubric bullets stay as the source; every rubric plays as statements (STATEMENTS at the bottom).
rub = lambda n, q, marks, bullets, clues, each=None, notes=None, after=None: {
    "t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
    **({"notes": notes} if notes else {}), **({"after": after} if after else {})}
term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
draw = lambda n, q, marks, criteria, clues, memo="", **kw: {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                           "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {}), **kw}
KEYWORDS = "If any of the underlined key words/phrases in the correct context is omitted, deduct 1 mark."

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


# ---- QUESTION 1: multiple choice, the question paper pages 3-7 and the memo page 2 ----
# (the clues are questions now: several old pairs, e.g. 1.3 "halve v and K changes by the square of that factor" or 1.7 "Set
# kQ²/r² = mg and solve for r", left one step to the answer)
q1 = [
    mcq("1.1", "Several forces are acting on a moving object. Which ONE of the following statements is CORRECT when these forces are in equilibrium?",
        ["The velocity of the object is increasing.", "The object is moving at a constant velocity.", "The kinetic energy of the object is decreasing.",
         "The object has a non-zero acceleration."], 1,
        ["When forces are in equilibrium, what is the net force on the object?", "The object is already moving: what can a zero net force change about its motion?"]),
    mcq("1.2", "A stone thrown vertically downwards from the top of a building takes t seconds to strike the ground. Consider the acceleration-time graph "
        "below for the motion of the stone. The effects of air friction are ignored. What does the shaded area between 0 and t seconds, shown in the "
        "graph, represent?",
        ["The final velocity of the stone", "The change in position of the stone", "The constant velocity of the stone", "The change in velocity of the stone"], 3,
        ["The area under a graph is the product of the quantities on its two axes: which quantities are they here?",
         "Which equation of motion contains the product aΔt?"],
        figure=fig("1.2", "An acceleration-time graph: acceleration (m·s⁻²) up, time (s) across. A horizontal line at 9,8 runs from 0 to t, and the "
                          "rectangle under it, from 0 to t, is shaded.")),
    mcq("1.3", "A ball moving horizontally has constant momentum p and kinetic energy K. The ball collides with a wall and bounces back horizontally. "
        "Immediately after the collision, the ball has momentum ½p. The mass of the ball remains constant. Which ONE of the following is the kinetic "
        "energy of the ball immediately after the collision?", ["¼K", "½K", "2K", "4K"], 0,
        ["p = mv and the mass stays the same: how does the speed after the collision compare with the speed before?",
         "Does the kinetic energy depend on v or on v²?"],
        figure=fig("1.3", "A ball moving right towards a vertical wall with momentum p; below it, the ball moving left away from the wall with momentum ½p.")),
    mcq("1.4", "A force F acts on a box as the box moves from rest down a rough incline at a constant acceleration. The force is parallel to the incline, as "
        "shown in the diagram below. Choose the option that CORRECTLY completes the following statement. The work done by the gravitational force is … "
        "the work done by the frictional force and the work done by F.",
        ["equal to the sum of", "less than the sum of", "greater than the sum of", "equal to the difference between"], 2,
        ["The box speeds up from rest: is the net work done on it positive, negative or zero?", "Which forces on the box act against its motion down the incline?"],
        figure=fig("1.4", "A box on a slope that goes down to the right, an arrow beside it pointing down the slope (its motion); force F acts on the "
                          "box up the slope, parallel to it.")),
    mcq("1.5", "A ball falling vertically downwards from point A strikes the ground with velocity v and bounces, reaching a maximum height at point B, as "
        "shown in the diagram below. Which ONE of the combinations below is CORRECT for the direction of the impulse on the ball upon striking the "
        "ground and the magnitude of the velocity with which the ball leaves the ground?",
        ["Impulse upward · leaves greater than v", "Impulse downward · leaves greater than v", "Impulse upward · leaves less than v",
         "Impulse downward · leaves less than v"], 2,
        ["The impulse equals the change in momentum: which way does the ball's momentum change when it bounces?",
         "Does the ball reach the same height after the bounce? What does that say about its kinetic energy as it leaves the ground?"],
        figure=fig("1.5", "A ball at A falls straight down to the ground (arrow down), and a ball bounces back up to B, which is lower than A (arrow up)."),
        optTable={"head": ["DIRECTION OF THE IMPULSE ON THE BALL", "MAGNITUDE OF THE VELOCITY WITH WHICH THE BALL LEAVES THE GROUND"],
                  "rows": [["Upward", "Greater than v"], ["Downward", "Greater than v"], ["Upward", "Less than v"], ["Downward", "Less than v"]]}),
    mcq("1.6", "The absorption spectrum of an element surrounding a moving star is observed on Earth and found to be red shifted. Which ONE of the "
        "following combinations is CORRECT for the movement of the star and the frequency of the observed light on Earth?",
        ["Away from Earth · decreased", "Towards Earth · decreased", "Away from Earth · increased", "Towards Earth · increased"], 0,
        ["A red shift is the Doppler effect for light: are the observed wavelengths longer or shorter than the emitted ones?",
         "For light, c = fλ: how is the frequency linked to the wavelength, and which motion of a source stretches its waves?"],
        optTable={"head": ["MOVEMENT OF STAR", "FREQUENCY OF OBSERVED LIGHT ON EARTH"],
                  "rows": [["Away from Earth", "Decreased"], ["Towards Earth", "Decreased"], ["Away from Earth", "Increased"], ["Towards Earth", "Increased"]]}),
    mcq("1.7", "Two small identical spheres, each with mass m and charge +Q, are placed in a vertical cylinder. The spheres remain stationary when their "
        "centres are r metres apart, as shown in the diagram below. Ignore ALL frictional effects. Which ONE of the following expressions can be used "
        "to CORRECTLY calculate the distance r?", ["√(kQ²/mg)", "√(kmg/Q²)", "√(Q²/kmg)", "√(mg/kQ²)"], 0,
        ["Which two forces act on the top sphere, and in which directions?", "The top sphere is at rest: how do the sizes of those two forces compare?"],
        figure=fig("1.7", "A vertical cylinder; one sphere of mass m and charge +Q rests at the bottom and an identical one floats above it, their "
                          "centres r apart.")),
    mcq("1.8", "The kilowatt-hour (kWh) is a unit of …", ["power.", "electric current.", "electrical energy.", "potential difference."], 2,
        ["A kilowatt is a unit of power and an hour is a unit of time.", "Rearrange P = W/Δt from the data sheet: which quantity equals power x time?"]),
    mcq("1.9", "The diagram below shows a simplified electric motor. The rotation of the coil is observed from the battery. Which ONE of the following "
        "statements is CORRECT while the motor is in operation? The coil and the …",
        ["slip rings rotate anti-clockwise.", "slip rings rotate clockwise.", "commutator rotate clockwise.", "commutator rotate anti-clockwise."], 3,
        # (the old first clue said a DC motor uses a split-ring commutator: with the battery, half the answer)
        ["Slip rings or a split-ring commutator: which does a motor need when it runs on a battery?",
         "Find the current's direction in each side of the coil, then use the left-hand (motor) rule for the force on each side."],
        # (the caption no longer names the ring a split ring: the options ask which kind it is)
        figure=fig("1.9", "A rectangular coil between the N pole (left) and the S pole (right) of a magnet; its two ends join a ring at the front, "
                          "touched by two brushes that are wired to a battery below.")),
    mcq("1.10", "Which of the following statements is/are TRUE for the photoelectric effect? The photoelectric effect demonstrates that:\n(i) Light has a "
        "wave nature\n(ii) Light has a particle nature\n(iii) Light energy is quantised",
        ["(i) only", "(ii) only", "(i) and (iii) only", "(ii) and (iii) only"], 3,
        ["How did Einstein explain the photoelectric effect: with light as waves or as photons?", "What is a photon?"]),
]

# ---- QUESTION 2, the question paper page 8 and the memo pages 3-4 ----
q2 = [
    rub("2.1", "Define the term static friction.", 2,
        ["The force that opposes the tendency of motion of a stationary object relative/parallel to a surface. (2)"],
        ["The object is not moving yet.", "Which force acts against the TENDENCY to move?"], each=2, notes=[KEYWORDS]),
    draw("2.2", "Draw a labelled free-body diagram showing ALL the HORIZONTAL forces acting on the crate JUST BEFORE it starts moving.", 2,
         [["T: tension / FT / Fstring, to the right (towards the pulley)", 1], ["fs: static friction / f / Ff, to the left", 1]],
         ["Which horizontal forces act on the crate just before it moves?", "Which way does each of them point?"],
         memo="Mark for label and arrow. Vertical forces (w, N) shown: no penalty. Arrows not touching the dot, any other force, or no arrows: max 1/2.",
         # BUILT (2026-10-11, build "forces"): T towards the pulley (0°), static friction against it (180°), each within 10°; the memo's
         # "do not penalise if vertical forces (w, N) are shown": Fg and FN are free (neither earn nor cost), any other force costs 1
         build={"kind": "forces", "surface": 0, "forces": [{"id": "T", "at": 0, "crit": 0}, {"id": "f", "at": 180, "crit": 1}], "free": ["Fg", "FN"]}),
    work("2.3.1", "Calculate the coefficient of static friction (µs).", 4, [
        "T = mg = 7,4(9,8) = 72,52 N\nfs(max) = μsN\nμs(8,5)(9,8) = 72,52\nμs = 0,87",          # Y's 7,4 kg read for the start (wrong part)
        "T = mg = 4,2(9,8) = 41,16 N\nfs(max) = μsN\nμs(8,5)(9,8) = 41,16\nμs = 0,49",          # the memo (OPTION 1)
        "T = mg = 4,2(9,8) = 41,16 N\nfs(max) = μsN\nμs(8,5) = 41,16\nμs = 4,84",               # N taken as the mass: g left out
        "T = mg = 4,2(9,8) = 41,16 N\nfs(max) = μsN\nμs(8,5 + 4,2)(9,8) = 41,16\nμs = 0,33"], 1, # N from the crate AND the hanging mass (wrong body)
        # (the old second clue, "T = weight of the hanging mass = fs(max) = µs N", was the working itself)
        ["At which hanging mass does the crate just start to move?", "Just before it moves, which forces balance on the crate, and on the hanging mass?"]),
    work("2.3.2", "Calculate the magnitude of the acceleration represented by Y on the graph if the coefficient of kinetic friction between the crate "
         "and the table is 0,40.", 5, [
        "Fnet = ma\nCrate: T − 0,4(8,5)(9,8) = 8,5a\nHanging mass: T − 7,4(9,8) = 7,4a\nY = a = 35,64 m·s⁻²",    # the hanging mass's forces signed upward (sign)
        "Fnet = ma\nCrate: T − 0,4(8,5)(9,8) = 8,5a\nHanging mass: 4,2(9,8) − T = 4,2a\nY = a = 0,62 m·s⁻²",     # the 4,2 kg start mass, not 7,4 kg (wrong value)
        "Fnet = ma\nCrate: T − 0,4(8,5) = 8,5a\nHanging mass: 7,4(9,8) − T = 7,4a\nY = a = 4,35 m·s⁻²",         # g left out of the normal force
        "Fnet = ma\nCrate: T − 0,4(8,5)(9,8) = 8,5a\nHanging mass: 7,4(9,8) − T = 7,4a\nY = a = 2,47 m·s⁻²"], 3, # the memo
        ["Which hanging mass gives the acceleration Y?",
         "Which forces act along the motion on the crate, and on the hanging mass? Apply Newton's second law to each."]),
    rub("2.4", "A 5 kg block is now placed inside the crate and the experiment is repeated. How will this affect the maximum static frictional force now "
        "experienced by the crate? Choose from INCREASES, DECREASES or REMAINS THE SAME. Give a reason for the answer.", 2,
        ["Increases (1)", "fs(max) α N / fs(max) = µsN: the normal force acting on the crate increases / the mass (weight) of the crate increases. (1)"],
        ["What does the extra 5 kg do to the normal force on the crate?", "How does the maximum static friction depend on the normal force?"]),
]

# ---- QUESTION 3, the question paper page 9 and the memo pages 5-10 ----
q3 = [
    work("3.1.1", "Using EQUATIONS OF MOTION ONLY, calculate the value of t, as shown in the graphs.", 5, [
        "Δy = viΔt + ½aΔt²\nBall A: Δy = 12t + ½(−9,8)t²\nBall B: Δy = −5,4(t − 2) + ½(−9,8)(t − 2)²\n"
        "12t + ½(−9,8)t² = −5,4(t − 2) + ½(−9,8)(t − 2)²\nt = 4 s",                                    # the memo (OPTION 1, upwards positive)
        "Δy = viΔt + ½aΔt²\nBall A: Δy = 12t + ½(−9,8)t²\nBall B: Δy = 5,4(t − 2) + ½(−9,8)(t − 2)²\n"
        "12t + ½(−9,8)t² = 5,4(t − 2) + ½(−9,8)(t − 2)²\nt = 2,34 s",                                  # ball B's downward velocity signed upward
        "Δy = viΔt + ½aΔt²\nBall A: Δy = 12t + ½(−10)t²\nBall B: Δy = −5,4(t − 2) + ½(−10)(t − 2)²\n"
        "12t + ½(−10)t² = −5,4(t − 2) + ½(−10)(t − 2)²\nt = 3,54 s",                                   # g taken as 10, not the data sheet's 9,8
        "Δy = viΔt + aΔt²\nBall A: Δy = 12t + (−9,8)t²\nBall B: Δy = −5,4(t − 2) + (−9,8)(t − 2)²\n"
        "12t + (−9,8)t² = −5,4(t − 2) + (−9,8)(t − 2)²\nt = 1,30 s"], 0,                               # the ½ left out of the formula
        # (the old second clue, "its time in the air is t − 2", was a line of the working)
        ["Both balls start at the top and end on the ground: how do their displacements compare?",
         "Ball B is thrown 2 s after ball A: for how long is ball B in the air?"]),
    work("3.1.2", "Using EQUATIONS OF MOTION ONLY, calculate the value of Z, as shown in the graphs.", 3, [
        "Δy = viΔt + ½aΔt²\nΔy = (−5,4)(4) + ½(−9,8)(4)²\nΔy = −100 m\nZ = 100 m",               # ball B given ball A's 4 s in the air (wrong body)
        "Δy = viΔt + ½aΔt²\nΔy = (12)(4) + ½(−9,8)(4)²\nΔy = −30,4 m\nZ = 30,4 m",               # the memo (OPTION 1, upwards positive)
        "Δy = viΔt + ½aΔt²\nΔy = (12)(4) + ½(9,8)(4)²\nΔy = 126,4 m\nZ = 126,4 m",               # a = +9,8 with upwards positive (sign)
        "Δy = viΔt + ½aΔt²\nΔy = (12)(4) + ½(−9,8)(4)\nΔy = 28,4 m\nZ = 28,4 m"], 1,             # Δt not squared
        ["What does Z stand for on the graph, and which ball's motion can give it?", "How long is ball A in the air, and what is its initial velocity?"],
        after=["3.1.1"]),   # the options show t = 4 s, 3.1.1's answer
    work("3.1.3", "Using EQUATIONS OF MOTION ONLY, calculate the value of Y, as shown in the graphs.", 4, [
        "vf² = vi² + 2aΔy\n0 = (12)² + 2(−9,8)Δy\nΔy = 7,35 m\nY = 30,4 − 7,35 = 23,05 m",            # the rise taken off Z, not added (sign)
        "vf² = vi² + aΔy\n0 = (12)² + (−9,8)Δy\nΔy = 14,69 m\nY = 14,69 + 30,4 = 45,09 m",              # the 2 left out of the formula
        "vf² = vi² + 2aΔy\n0 = (5,4)² + 2(−9,8)Δy\nΔy = 1,49 m\nY = 1,49 + 30,4 = 31,89 m",             # ball B's speed for ball A (wrong body)
        "vf² = vi² + 2aΔy\n0 = (12)² + 2(−9,8)Δy\nΔy = 7,35 m\nY = 7,35 + 30,4 = 37,75 m"], 3,          # the memo (OPTION 1; range 37,72 - 37,75 m)
        ["What is ball A's velocity at its highest point?", "Y is measured from the ground: how high is the roof above the ground?"],
        after=["3.1.2"]),   # the options show Z = 30,4 m, 3.1.2's answer
    draw("3.2", "On the same set of axes, sketch the velocity-time graphs for ball A and ball B while they are in free fall. Label the graphs A and B for "
         "ball A and ball B respectively. Clearly indicate the following on the graphs: the initial velocity of each ball; the time at which each ball "
         "is thrown; the time at which the balls strike the ground.", 4,
         [["Correct initial velocities of balls A and B (12 and −5,4 m·s⁻¹, upwards positive) with straight lines of the same sign of slope", 1],
          ["Correct initial times: A at 0 s, B at 2 s (B starts after A crosses the time axis)", 1], ["Both graphs end at 4 s (accept t)", 1],
          ["The graphs are parallel, B to the right of A", 1]],
         ["In free fall, what is the gradient of each velocity-time line?", "With upwards positive, what sign does each ball's initial velocity have?"],
         memo="No labels A and B: deduct 1 mark.", after=["3.1.1"]),   # its criteria show t = 4 s, 3.1.1's answer
]

# ---- QUESTION 4, the question paper page 10 and the memo pages 11-12 ----
q4 = [
    rub("4.1", "Write down the principle of conservation of mechanical energy in words.", 2,
        ["The total mechanical energy / sum of gravitational potential energy and kinetic energy in an isolated system remains constant / is conserved. (2)"],
        ["Mechanical energy = potential + kinetic.", "In which kind of system does it stay the same?"], each=2, notes=[KEYWORDS]),
    work("4.2", "Calculate the speed of trolley B at the bottom of the inclined plane.", 4, [
        "Emech(top) = Emech(bottom)\n(mgh + ½mv²)top = (mgh + ½mv²)bottom\n(2)(9,8)(1,5) + 0 = 0 + ½(1,5)v²\nv = 6,26 m·s⁻¹",  # A's mass in Ek (wrong body)
        "Emech(top) = Emech(bottom)\n(mgh + ½mv²)top = (mgh + ½mv²)bottom\n(2)(1,5) + 0 = 0 + ½(2)v²\nv = 1,73 m·s⁻¹",          # g left out of Ep
        "Emech(top) = Emech(bottom)\n(mgh + ½mv²)top = (mgh + ½mv²)bottom\n(2)(9,8)(1,5) + 0 = 0 + ½(2)v²\nv = 5,42 m·s⁻¹",    # the memo (OPTION 1)
        "Emech(top) = Emech(bottom)\n(mgh + ½mv)top = (mgh + ½mv)bottom\n(2)(9,8)(1,5) + 0 = 0 + ½(2)v\nv = 29,40 m·s⁻¹"], 2, # v not squared in Ek
        # (the old second clue, "All its kinetic energy at the bottom becomes potential energy at 1,5 m", was the working's middle line)
        ["Which energy principle applies on a frictionless incline?", "Where on the incline is trolley B's kinetic energy zero, and where its potential energy?"]),
    work("4.3.1", "For the t seconds that the spring takes to return to its natural length, calculate the change in momentum of trolley B.", 3, [
        "Δp = mvf − mvi\nΔp = 2(5,42 − 0)\nΔp = 10,84 kg·m·s⁻¹ to the right",          # the memo
        "Δp = mvf − mvi\nΔp = 2(5,42 − 0)\nΔp = 10,84 kg·m·s⁻¹ to the left",           # the direction slip
        "Δp = mvf − mvi\nΔp = 1,5(5,42 − 0)\nΔp = 8,13 kg·m·s⁻¹ to the right",         # trolley A's mass (wrong body)
        "Δp = ½mvf² − ½mvi²\nΔp = ½(2)(5,42² − 0)\nΔp = 29,38 kg·m·s⁻¹ to the right"], 0,   # the change in Ek for the change in momentum
        ["What are trolley B's velocities before and after the spring pushes it?", "Which formula gives a change in momentum, and which way does B move?"],
        after=["4.2"]),   # the options show v = 5,42 m·s⁻¹, 4.2's answer
    # a vector, 1 mark, no working: magnitude AND direction as the memo marks it (a typed number lost the direction, and the old stem
    # printed "opposite in direction to B's", half the answer)
    mcq("4.3.2", "For the t seconds that the spring takes to return to its natural length, write down the change in momentum of trolley A.",
        ["10,84 kg·m·s⁻¹ to the right", "10,84 kg·m·s⁻¹ to the left", "8,13 kg·m·s⁻¹ to the left", "0 kg·m·s⁻¹"], 1,
        # (the old clues, "equal and opposite impulses: equal and opposite changes in momentum", stated the answer)
        ["How do the forces the spring exerts on A and on B compare, and for how long does each act?", "What does the impulse on a trolley equal?"],
        marks=1, after=["4.3.1"]),   # the options show 10,84 kg·m·s⁻¹, 4.3.1's answer
    work("4.4", "Calculate the speed of trolley A after t seconds.", 2, [
        "ΔpA = mvf − mvi\n−10,84 = 2(vf − 0)\nvf = −5,42 m·s⁻¹\nspeed = 5,42 m·s⁻¹",                # trolley B's mass (wrong body)
        "ΔpA = mvf − mvi\n−10,84 = 1,5(vf − 5,42)\nvf = −1,81 m·s⁻¹\nspeed = 1,81 m·s⁻¹",           # B's speed as A's initial velocity (wrong part)
        "ΔpA = mvf − mvi\n−10,84 = 1,5(vf − 0)\nvf = (−10,84)(1,5) = −16,26 m·s⁻¹\nspeed = 16,26 m·s⁻¹",   # multiplied by the mass, not divided
        "ΔpA = mvf − mvi\n−10,84 = 1,5(vf − 0)\nvf = −7,23 m·s⁻¹\nspeed = 7,23 m·s⁻¹"], 3,         # the memo
        ["What is trolley A's change in momentum, and its mass?", "What was trolley A's velocity before the spring was released?"],
        after=["4.2", "4.3.2"]),   # the options show 4.3.2's −10,84 kg·m·s⁻¹ (left) and 4.2's 5,42 m·s⁻¹
]

# ---- QUESTION 5, the question paper page 11 and the memo pages 13-14 ----
q5 = [
    rub("5.1", "Define the term work done by a force.", 2,
        ["The work done on an object by a constant force F is FΔx cos θ, where F is the magnitude of the force, Δx the magnitude of the displacement and "
         "θ the angle between the force and the displacement. (2)",
         "OR — The work done on an object is the product of the force and the displacement of the object in the direction of the displacement. (2)"],
        ["Which two quantities does work combine?", "Does all of a force do work, or only the part of it along the displacement?"], each=2, notes=[KEYWORDS]),
    draw("5.2", "Draw a labelled free-body diagram showing ALL the forces acting on the crate as it moves.", 4,
         [["w: weight / Fg / mg / 58,8 N / gravitational force, downwards", 1], ["N: normal force / FN, upwards", 1],
          ["f: friction / Ff / fk, to the left (against the motion)", 1], ["F: applied force / FA, at 30° above the horizontal", 1]],
         ["Which forces act on a crate pulled along a rough horizontal surface?", "Draw F at its angle: do not split it into components."],
         memo="Mark for label and arrow. Any other force, no arrows, forces not touching the dot, or F drawn as components: max 3/4.",
         # BUILT (2026-10-11, build "forces"): w 270°, N 90°, friction against the motion to the right (180°), F at 30° above the
         # horizontal as the figure gives it (30°), each within 10°. F cannot be drawn as components (the tray holds F, not its parts)
         build={"kind": "forces", "surface": 0, "forces": [{"id": "Fg", "at": 270, "crit": 0}, {"id": "FN", "at": 90, "crit": 1}, {"id": "f", "at": 180, "crit": 2},
                                                           {"id": "FA", "at": 30, "crit": 3}]}),
    work("5.3", "Using ENERGY PRINCIPLES ONLY, calculate the magnitude of force F.", 4, [
        "Wnc = ΔEk + ΔEp\nWF + Wf = ½m(vf² − vi²) + mg(hf − hi)\nF(1,5)sin 30° + 10(1,5)cos 180° = ½(6)(2² − 0²) + 0\nF = 36,00 N",   # sin for cos
        "Wnc = ΔEk + ΔEp\nWF + Wf = ½m(vf² − vi²) + mg(hf − hi)\nF(1,5)cos 30° + 10(1,5)cos 180° = ½(6)(2² − 0²) + 0\nF = 20,78 N",   # the memo (OPTION 1)
        "Wnc = ΔEk + ΔEp\nWF + Wf = ½m(vf − vi) + mg(hf − hi)\nF(1,5)cos 30° + 10(1,5)cos 180° = ½(6)(2 − 0) + 0\nF = 16,17 N",         # v not squared
        "Wnc = ΔEk + ΔEp\nWF = ½m(vf² − vi²) + mg(hf − hi)\nF(1,5)cos 30° = ½(6)(2² − 0²) + 0\nF = 9,24 N"], 1,                        # friction's work left out
        # (the old second clue wrote both works with their values, F(1,5)cos 30° and 10(1,5)cos 180°)
        ["Which forces do work on the crate as it moves from A to B?", "What is the angle between each of those forces and the displacement?"]),
    mcq("5.4", "A 2 kg object is placed in the crate. What effect will this have on the work done by the same force F when the crate is again moved from "
        "point A to point B? Write only INCREASES, DECREASES or REMAINS THE SAME.", ["Increases", "Decreases", "Remains the same"], 2,
        ["Which quantities does the work done by F depend on?", "Does adding mass change any of them?"]),
]

# ---- QUESTION 6, the question paper page 12 and the memo page 15 ----
q6 = [
    term("6.1", "Name the phenomenon that explains why the wavelengths shown in the graph differ.", ["Doppler effect", "Doppler"],
         ["A moving source changes the wavelength a listener detects.", "It is named after an Austrian physicist."]),
    rub("6.2", "Is the car moving TOWARDS or AWAY FROM the listener? Give a reason for the answer.", 2,
        ["Away (from the listener) (1)",
         "The wavelength detected by the listener is longer than the wavelength emitted by the source / λL > λS OR the frequency detected is lower than "
         "the frequency of the source / fL < fs. (1)"],
        # (the old second clue, "A source moving away stretches the waves", with the graph's λL > λS gave the choice)
        ["Which is longer on the graph: λL or λS?", "Does a source that moves towards a listener squeeze or stretch the waves the listener receives?"]),
    work("6.3.1", "Calculate the frequency of the sound emitted by the siren.", 3, [
        "v = fλ\n343 = f(0,38)\nf = 902,63 Hz",                           # the memo
        "v = fλ\n343 = f(0,40)\nf = 857,50 Hz",                           # the listener's λL, not the siren's λS (wrong value)
        "c = fλ\n3 × 10⁸ = f(0,38)\nf = 7,89 × 10⁸ Hz",                   # the speed of light for sound (the memo's "c = fλ" slip)
        "v = {f}/{λ}\n343 = {f}/{0,38}\nf = 130,34 Hz"], 0,               # the wave equation upside down
        # (the old second clue wrote the formula with its value, v = fλ with v = 343 m·s⁻¹)
        ["Which wavelength on the graph belongs to the siren itself?", "Which wave equation links speed, frequency and wavelength?"]),
    work("6.3.2", "Calculate the magnitude of the velocity of the car.", 6, [
        "v = fλ\n343 = fL(0,40)\nfL = 857,5 Hz\nfL = {v − vs}/{v} fs\n857,5 = {343 − vs}/{343}(902,63)\nvs = 17,15 m·s⁻¹",    # vs in the numerator (wrong formula)
        "v = fλ\n340 = fL(0,40)\nfL = 850 Hz\nfL = {v}/{v + vs} fs\n850 = {340}/{340 + vs}(902,63)\nvs = 21,05 m·s⁻¹",           # 340 m·s⁻¹ for the given 343
        "v = fλ\n343 = fL(0,38)\nfL = 902,63 Hz\nfL = {v}/{v + vs} fs\n902,63 = {343}/{343 + vs}(857,5)\nvs = −17,15 m·s⁻¹",    # the wavelengths swapped
        "v = fλ\n343 = fL(0,40)\nfL = 857,5 Hz\nfL = {v}/{v + vs} fs\n857,5 = {343}/{343 + vs}(902,63)\nvs = 18,05 m·s⁻¹"], 3,  # the memo (range 18,05 - 18,45)
        # (the old second clue wrote the right working's formula, fL = v/(v + vs) fs)
        ["What frequency does the listener detect? Use λL.",
         "The car moves away: is the detected frequency lower or higher than the siren's, and which form of the Doppler equation gives that?"],
        after=["6.2", "6.3.1"]),   # the options show fs = 902,63 Hz (6.3.1's answer); the working's v + vs and the clue, a car moving AWAY (6.2's)
]

# ---- QUESTION 7, the question paper page 13 and the memo pages 16-17 ----
q7a = [
    work("7.1", "Calculate the magnitude of the electric field at X.", 3, [
        "E = {kQ}/{r²}\nE = {(9 × 10⁹)(2 × 10⁻⁹)}/{(6)²}\nE = 0,5 N·C⁻¹",             # 6 cm not converted to m
        "E = {kQ}/{r²}\nE = {(9 × 10⁹)(2 × 10⁻⁹)}/{(0,06)²}\nE = 5 × 10³ N·C⁻¹",      # the memo
        "E = {kQ}/{r}\nE = {(9 × 10⁹)(2 × 10⁻⁹)}/{0,06}\nE = 300 N·C⁻¹",              # r not squared (wrong formula)
        "E = {kQ}/{r²}\nE = {(9 × 10⁹)(2)}/{(0,06)²}\nE = 5 × 10¹² N·C⁻¹"], 1,       # 2 nC not converted to C
        # (the old clues wrote the formula, E = kQ/r², and both conversions, 2 x 10⁻⁹ C and 0,06 m)
        ["Which equation in the data sheet gives the field of a point charge?", "What are 2 nC and 6 cm in SI units?"]),
]
q7b = [
    draw("7.2", "Draw the resultant electric field pattern due to charges P and S.", 3,
         [["Correct direction of the field lines (from P to S)", 1], ["Correct shape between the charges and outside them", 1],
          ["No field lines crossing; lines touch the charges but do not go inside", 1]],
         ["Are P and S like or unlike charges?", "Do field lines point away from a positive charge or towards it?"],
         memo="The field of two like charges: 0/3. Only one charge drawn: 0/3."),
]
q7c = [
    rub("7.3.1", "State Coulomb's law in words.", 2,
        ["The magnitude of the electrostatic force exerted by one point charge on another point charge is directly proportional to the product of the "
         "magnitudes of their charges and inversely proportional to the square of the distance between them. (2)"],
        ["It is about the force between two point charges.", "What happens to that force when the distance between the charges doubles?"], each=2,
        notes=[KEYWORDS, "If reference to masses / if the word FORCE in context is omitted: 0/2."]),
    mcq("7.3.2", "What is the polarity of charge T? Choose from POSITIVE or NEGATIVE.", ["Positive", "Negative"], 0,
        ["P and S carry charges of the same size: which of them is closer to T, so exerts the bigger force on it?",
         "The net force on T points to the left: is T pulled towards S or pushed away from it?"], marks=1),
    work("7.3.3", "Calculate the magnitude of charge T.", 5, [
        "F = {kQ1Q2}/{r²}\nFST = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,02)²}\nFPT = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,06)²}\nFnet = FST + FPT\n"
        "2,5 × 10⁻⁴ = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,02)²} + {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,06)²}\nQT = 5 × 10⁻⁹ C",       # the forces added (direction)
        "F = {kQ1Q2}/{r²}\nFST = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,02)²}\nFPT = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,04)²}\nFnet = FST − FPT\n"
        "2,5 × 10⁻⁴ = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,02)²} − {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,04)²}\nQT = 7,41 × 10⁻⁹ C",    # P to S (4 cm) for P to T (wrong part)
        "F = {kQ1Q2}/{r²}\nFST = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,02)²}\nFPT = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,06)²}\nFnet = FST − FPT\n"
        "2,5 × 10⁻⁴ = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,02)²} − {(9 × 10⁹)(2 × 10⁻⁹)QT}/{(0,06)²}\nQT = 6,25 × 10⁻⁹ C",    # the memo (OPTION 1)
        "F = {kQ1Q2}/{r}\nFST = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{0,02}\nFPT = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{0,06}\nFnet = FST − FPT\n"
        "2,5 × 10⁻⁴ = {(9 × 10⁹)(2 × 10⁻⁹)QT}/{0,02} − {(9 × 10⁹)(2 × 10⁻⁹)QT}/{0,06}\nQT = 4,17 × 10⁻⁷ C"], 2,   # r not squared
        # (the old second clue wrote the deciding equation, Fnet = FST − FPT = 2,5 x 10⁻⁴ N)
        ["How far is T from S, and how far from P?", "Do the forces of P and of S on T act in the same direction or in opposite directions?"]),
]

# ---- QUESTION 8, the question paper page 14 and the memo pages 18-19 ----
q8 = [
    rub("8.1", "Define the term power.", 2,
        ["The rate at which work is done OR the rate at which energy is transferred/dissipated OR work done per unit time. (2 or 0)"],
        # (the old second clue, "How fast work is done.", was the answer)
        ["Which quantities does P = W/Δt (data sheet) link?", "Two machines do the same work, one in half the time: which has more power, and why?"], each=2),
    work("8.2.1", "If both light bulbs operate as RATED, calculate the reading on ammeter A2.", 3, [
        "P = {V}/{I}\n48 = {32}/{I}\nI = 0,67 A",             # the formula upside down
        "P = I²R\n48 = I²(32)\nI = 1,22 A",                   # the rated voltage used as a resistance
        "P = VI\n48 = 20I\nI = 2,4 A",                        # L1's voltage with L2's power (wrong body)
        "P = VI\n48 = 32I\nI = 1,5 A"], 3,                    # the memo (OPTION 1)
        ["Which bulb is in the same branch as A2, and what is its rating?", "Which formula links power, potential difference and current?"]),
    work("8.2.2", "If both light bulbs operate as RATED, calculate the reading on ammeter A1.", 3, [
        "P = VI\n36 = 20I\nI = 1,8 A\nITOT = 1,5 + 1,8 = 3,3 A",                 # the memo (OPTION 1)
        "P = VI\n36 = 32I\nI = 1,13 A\nITOT = 1,5 + 1,13 = 2,63 A",              # the parallel 32 V used for L1 (wrong value)
        "P = VI\n36 = 20I\nI = 1,8 A\nITOT = 1,8 − 1,5 = 0,3 A",                 # the branch currents subtracted
        "P = I²R\n36 = I²(20)\nI = 1,34 A\nITOT = 1,5 + 1,34 = 2,84 A"], 0,      # the rated voltage used as a resistance
        ["Where does A1 sit: in one branch or in the main circuit?", "What current does L1 draw when it works as rated (36 W ; 20 V)?"],
        after=["8.2.1"]),   # the options show I(A2) = 1,5 A, 8.2.1's answer
    work("8.2.3", "If both light bulbs operate as RATED, calculate the resistance of resistor R1.", 4, [
        "VR1 + VL1 = V∥\nVR1 + 20 = 32\nVR1 = 12 V\nV = IR\n12 = 3,3R1\nR1 = 3,64 Ω",               # the total current for R1's branch (wrong part)
        "VR1 + VL1 = V∥\nVR1 + 20 = 32\nVR1 = 12 V\nV = IR\n12 = 1,8R1\nR1 = 6,67 Ω",               # the memo (OPTION 1)
        "VR1 − VL1 = V∥\nVR1 − 20 = 32\nVR1 = 52 V\nV = IR\n52 = 1,8R1\nR1 = 28,89 Ω",              # L1's voltage added to the branch (sign)
        "VR1 + VL1 = V∥\nVR1 + 20 = 32\nVR1 = 12 V\nV = {I}/{R}\n12 = {1,8}/{R1}\nR1 = 0,15 Ω"], 1, # Ohm's law upside down
        # (the old second clue gave the branch current, L1's 1,8 A: 8.2.2's working)
        ["R1 and L1 share one branch, in parallel with L2: what is the potential difference across that branch?", "Which current flows through R1?"],
        after=["8.2.2"]),   # the options show 8.2.2's 1,8 A (L1) and 3,3 A (A1)
    work("8.2.4", "If both light bulbs operate as RATED, calculate the emf of the battery.", 4, [
        "V2 = ITOT R2 = 3,3(4) = 13,2 V\nε = Vext\nε = 13,2 + 32\nε = 45,20 V",                     # the lost volts Ir left out
        "V2 = IR2 = 1,5(4) = 6 V\nε = Vext + Ir\nε = (6 + 32) + 1,5(0,6)\nε = 38,90 V",              # A2's current for the battery's (wrong part)
        "V2 = ITOT R2 = 3,3(4) = 13,2 V\nε = Vext − Ir\nε = (13,2 + 32) − 3,3(0,6)\nε = 43,22 V",   # the lost volts subtracted (sign)
        "V2 = ITOT R2 = 3,3(4) = 13,2 V\nε = Vext + Ir\nε = (13,2 + 32) + 3,3(0,6)\nε = 47,18 V"], 3,   # the memo (OPTION 1; range 47,16 - 47,19 V)
        # (the old second clue wrote the formula with its value, ε = V(external) + Ir with r = 0,6 Ω)
        ["What is the potential difference across R2, which carries the total current?",
         "Which equation links the emf, the external potential difference and the internal resistance?"],
        after=["8.2.1", "8.2.2"]),   # the options show 8.2.2's 3,3 A and 8.2.1's 1,5 A
    # decide by calculation: each working ends in its own conclusion (L2's rated current is 1,5 A); the memo's is "No" (accept: not glow)
    work("8.3", "Bulb L1 burns out after a while. Assume that the resistance of bulb L2 remains constant. Will bulb L2 continue to glow after bulb L1 "
         "burns out? Choose from YES or NO. Support your answer with a suitable calculation.", 5, [
        "P = {V²}/{R}\n48 = {32²}/{RL2}\nRL2 = 21,33 Ω\nε = IR\n47,18 = I(21,33 + 4)\nI = 1,86 A\n"
        "1,86 A is more than L2's rated 1,5 A: No",                                   # the internal resistance left out
        "P = {V²}/{R}\n48 = {32²}/{RL2}\nRL2 = 21,33 Ω\nε = I(R + r)\n47,18 = I(21,33 + 4 + 0,6)\nI = 1,82 A\n"
        "1,82 A is more than L2's rated 1,5 A: No",                                   # the memo
        "P = {V²}/{R}\n36 = {20²}/{RL2}\nRL2 = 11,11 Ω\nε = I(R + r)\n47,18 = I(11,11 + 4 + 0,6)\nI = 3,00 A\n"
        "3,00 A is more than L2's rated 1,5 A: No",                                   # L1's rating for L2's resistance (wrong body)
        "P = {V²}/{R}\n48 = {32²}/{RL2}\nRL2 = 21,33 Ω\nε = I(R + r)\n32 = I(21,33 + 4 + 0,6)\nI = 1,23 A\n"
        "1,23 A is less than L2's rated 1,5 A: Yes"], 1,                              # the old 32 V across the bulbs taken as the emf
        # (the old first clue listed the resistances left in the circuit: it picked out the right working)
        ["Once L1 burns out, which resistances are left in series with the battery?", "How does the new current through L2 compare with the current it is rated for?"],
        after=["8.2.1", "8.2.4"]),   # the options show 8.2.4's ε = 47,18 V and 8.2.1's 1,5 A
]

# ---- QUESTION 9, the question paper page 15 and the memo page 20 ----
q9a = [
    mcq("9.1", "Name the type of generator. Choose from AC or DC.", ["AC", "DC"], 1,
        # (the old second clue, "It stays on one side of the time axis.", gave the answer away)
        ["Does the current in the graph ever change direction?", "Which type of generator gives a current that reverses every half turn?"], marks=1),
    rub("9.2", "State the energy conversion that takes place in this generator while it is in operation.", 2,
        ["Mechanical / kinetic (energy) to electrical (energy). (2 or 0)"],
        ["A generator is turned by something.", "What goes in, and what comes out?"], each=2),
    rub("9.3", "Give a reason why this generator is NOT suitable for the transmission of electricity over long distances.", 1,
        ["Power / energy / voltage loss cannot be reduced / will be too large OR the current cannot be made smaller. ACCEPT: transformers do not work "
         "with DC / it cannot be stepped up or down. (1)"],
        # (the old second clue, "Can DC be stepped up?", named 9.1's answer and this one's)
        ["Why is electricity sent over long distances at a high voltage?", "Which device changes the voltage, and what kind of current does it need?"],
        after=["9.1"]),   # a card names DC (transformers do not work with DC), 9.1's answer
    work("9.4", "Calculate the frequency at which the coil rotates in the generator.", 2, [
        "f = {1}/{T} = {1}/{0,01}\nf = 100 Hz",               # one hump taken as one rotation
        "f = {1}/{T} = {1}/{0,04}\nf = 25 Hz",                # all four humps taken as one rotation
        "f = {1}/{T} = {1}/{0,02}\nf = 50 Hz",                # the memo
        "f = {1}/{T} = {1}/{0,005}\nf = 200 Hz"], 2,          # the time to the first peak taken as the period
        # (the old first clue, "One full rotation of the coil gives two humps here.", picked out the right reading)
        ["How many humps on the graph does one full rotation of the coil make?", "How is the frequency linked to the period?"]),
    rub("9.5", "Define the term root mean square (rms) current.", 2,
        ["The (root-mean-square) current is the alternating current that dissipates the same amount of energy as an equivalent DC current. (2)"],
        ["It compares AC with DC.", "Think of the heating effect of each in the same resistor."], each=2, notes=[KEYWORDS]),
    work("9.6", "Calculate the root-mean-square current delivered by the generator.", 3, [
        "Irms = {Imax}/{2}\nIrms = {1,2}/{2}\nIrms = 0,60 A",       # divided by 2, not √2
        "Irms = {Imax}/{√2}\nIrms = {1,2}/{√2}\nIrms = 0,85 A",     # the memo
        "Irms = Imax√2\nIrms = 1,2√2\nIrms = 1,70 A",                # multiplied by √2
        "Irms = {Imax}/{√2}\nIrms = {0,6}/{√2}\nIrms = 0,42 A"], 1, # the second graph's peak (9.7), not this one's (wrong part)
        # (the old second clue wrote the right working's formula, Irms = Imax/√2)
        ["What is the peak current on the graph?", "Which data-sheet equation links the rms current and the maximum current?"]),
]
q9b = [
    rub("9.7", "The graph below shows how the induced current varies with time after a change was made to the operation of the generator. Fully describe "
        "the change that was made.", 2,
        ["The speed of rotation was halved/half. ACCEPT: the frequency was halved/half OR the period was doubled. (2)"],
        # (the old second clue, "Both changed by the same factor.", was half the answer)
        ["How do the peak current and the time for one hump compare with the first graph?",
         "What change to the coil's rotation makes the induced current both smaller and slower?"], each=2,
        notes=["If the speed of rotation is slower / the frequency decreases / the period increases (not halved / doubled): 1/2."]),
]

# ---- QUESTION 10, the question paper page 16 and the memo pages 21-22 ----
q10a = [
    rub("10.1", "Define the term photoelectric effect.", 2,
        ["The process whereby electrons are ejected from a metal surface when light (of suitable frequency) is incident / shining on that surface. (2)"],
        ["Light falls on a metal.", "What leaves the metal surface?"], each=2, notes=[KEYWORDS]),
]
q10b = [
    mcq("10.2.1", "Which colour of light is responsible for ejecting electrons that have a maximum kinetic energy equal to 2,65 x 10⁻²⁰ J?",
        ["Red", "Blue", "Green"], 2,
        # (the old clues, "Only two of the colours eject electrons" and "The lower-frequency one of those two", left one step)
        ["Which of the colours have photons with enough energy to eject electrons from potassium?",
         "Does a photon with less energy give the electron it ejects a smaller or a larger Ek(max)?"], marks=1),
    # the memo's two ticks: "Only green and blue light eject electrons / red light does not ✓" and "Green has a lower frequency than
    # blue / ... ✓ and therefore ejects electrons with the lower kinetic energy" (the old bullets dropped the first point)
    rub("10.2.2", "Explain the answer to QUESTION 10.2.1.", 2,
        ["Only green and blue light eject electrons / red light does not eject electrons. (1)",
         "Green light has a lower frequency / a longer wavelength than blue light / photons of blue light have more energy than photons of green light, "
         "and therefore green light ejects the electrons with the lower kinetic energy. (1)"],
        ["Which colours have photons energetic enough to eject electrons from potassium?",
         "How does a photon's energy affect the Ek(max) of the electron it ejects?"],
        after=["10.2.1"]),   # the cards name green, 10.2.1's answer
    work("10.2.3", "The electrons with a maximum kinetic energy of 2,65 x 10⁻²⁰ J are ejected by light that has a frequency of 5,85 x 10¹⁴ Hz. "
         "Calculate the frequency of the light that ejected electrons with a maximum kinetic energy of 6,96 x 10⁻²⁰ J.", 5, [
        "E = W0 + Ek(max)\n(6,63 × 10⁻³⁴)(5,85 × 10¹⁴) = W0 + 2,65 × 10⁻²⁰\nW0 = 3,61 × 10⁻¹⁹ J\n"
        "(6,63 × 10⁻³⁴)f = 3,61 × 10⁻¹⁹ + 6,96 × 10⁻²⁰\nf = 6,5 × 10¹⁴ Hz",                      # the memo (OPTION 1)
        "E = W0 + Ek(max)\n(6,63 × 10⁻³⁴)(5,85 × 10¹⁴) + 2,65 × 10⁻²⁰ = W0\nW0 = 4,14 × 10⁻¹⁹ J\n"
        "(6,63 × 10⁻³⁴)f = 4,14 × 10⁻¹⁹ + 6,96 × 10⁻²⁰\nf = 7,29 × 10¹⁴ Hz",                     # Ek(max) added to hf for W0 (sign)
        "E = W0 + Ek(max)\n(6,63 × 10⁻³⁴)(5,85 × 10¹⁴) = W0 + 6,96 × 10⁻²⁰\nW0 = 3,18 × 10⁻¹⁹ J\n"
        "(6,63 × 10⁻³⁴)f = 3,18 × 10⁻¹⁹ + 2,65 × 10⁻²⁰\nf = 5,20 × 10¹⁴ Hz",                     # the two Ek(max) values swapped (wrong value)
        "E = W0 + Ek(max)\n(6,63 × 10⁻³⁴)(5,85 × 10¹⁴) = W0 + 2,65 × 10⁻²⁰\nW0 = 3,61 × 10⁻¹⁹ J\n"
        "(6,63 × 10⁻³⁴)f = 6,96 × 10⁻²⁰\nf = 1,05 × 10¹⁴ Hz"], 0,                                 # W0 left out of the second light's equation
        # (the old second clue, "Find W0 from the first light, then use it for the second.", was the working's plan)
        ["What stays the same for both colours on the same potassium sheet?", "Which equation links a photon's energy, the work function and Ek(max)?"]),
    mcq("10.2.4", "The intensity of the red light is increased, while the intensities of the blue light and green light remain the same. What effect will "
        "this change have on the rate at which electrons are ejected? Choose from INCREASES, DECREASES or REMAINS THE SAME.",
        ["Increases", "Decreases", "Remains the same"], 2,
        # (the old second clue, "More photons that cannot eject electrons change nothing.", was the answer)
        ["Does red light eject any electrons from potassium?", "What does a higher intensity change: the energy of each photon, or the number of photons?"]),
]
q10c = [
    term("10.3.1", "Name the type of spectrum formed.", ["emission spectrum", "line emission spectrum", "emission"],
         # (the old second clue, "The gas gives out light.", named the type in other words)
         ["Spectra are named by what the atoms do with light: which do the atoms of a hot, excited gas do?",
          "Are the lines bright on a dark background, or dark on a bright one?"]),
    rub("10.3.2", "Explain the presence of the coloured lines in the spectrum.", 2,
        ["The coloured lines represent the (associated) frequencies / wavelengths / energies of the emitted photons (1)",
         "when atoms / electrons move (drop) to a lower energy level. (1)"],
        ["Each line is one frequency of light.", "What happens to an excited electron when its atom gives out light?"],
        after=["10.3.1"]),   # the cards speak of EMITTED photons: 10.3.1's answer is an emission spectrum
]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Friction and Newton's laws", "marks": 15,
     "lead": "In an experiment, a crate of mass 8,5 kg, lying stationary on a rough horizontal table, is connected to a mass hanger by means of a light "
             "inextensible string passing over a frictionless pulley, as shown in the diagram below. Mass pieces are added to the mass hanger and the "
             "acceleration of the crate is measured. The experiment is repeated several times by adding different masses to increase the hanging mass "
             "each time. Ignore the effects of air friction. The results obtained were used to draw the sketch graph below.",
     "figure": fig("Q2", "Top: an 8,5 kg crate on a table, joined by a string over a pulley at the table's right edge to a mass hanger with mass pieces. "
                         "Below: a sketch graph of acceleration of crate (m·s⁻²) against hanging mass (kg); the curve starts on the mass axis at 4,2 and "
                         "rises; a dashed line from 7,4 on the mass axis meets the curve at height Y."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Vertical projectile motion", "marks": 16,
     "lead": "Ball A is thrown vertically upwards at 12 m·s⁻¹ from the top of a building. Two seconds after ball A was thrown upwards, ball B is thrown "
             "vertically downwards at 5,4 m·s⁻¹ from the top of the same building. Both balls, A and B, strike the ground at time t seconds. Ignore the "
             "effects of air friction. The position-time sketch graphs for both balls are shown below.",
     "figure": fig("Q3", "Position (m) against time (s): curve A starts at height Z, rises to a maximum at Y and falls to 0 at time t; curve B starts "
                         "at Z later and falls to 0 at the same time t."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Momentum and energy", "marks": 12,
     "lead": "Two trolleys, A and B, of masses of 1,5 kg and 2 kg respectively, are held in a stationary position on a straight, horizontal, frictionless "
             "track, with a compressed spring between them. The trolleys are released and the spring takes t seconds to return to its natural length. The "
             "spring then falls to the ground. Trolley A moves to the left, while trolley B moves to the right and then up a frictionless inclined plane, "
             "rising to a maximum vertical height of 1,5 m, as shown in the diagram below. Ignore the rotational effects of the wheels.",
     "figure": fig("Q4", "Left, before the spring is released: trolleys A (1,5 kg) and B (2 kg) touching, with a compressed spring between them. Right, "
                         "after: A moving left, the spring at natural length on the track, and B moving right and up an incline to a height of 1,5 m."),
     "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Work and energy", "marks": 12,
     "lead": "A constant force F is applied at an angle of 30° to the horizontal on a crate of mass 6 kg that is initially at rest, as shown in the diagram "
             "below. A constant frictional force of 10 N acts on the crate as it moves from rest at point A along a horizontal surface to point B. The "
             "distance between point A and point B is 1,5 m. The speed of the crate at point B is 2 m·s⁻¹.",
     "figure": fig("Q5", "A 6 kg crate at point A on a horizontal surface; force F pulls it at 30° above the horizontal; point B is 1,5 m to the right."),
     "items": q5},
    # (the kind was "Doppler effect": 6.1 asks the learner to NAME the phenomenon)
    {"id": "6", "title": "Question 6", "kind": "Waves and sound", "marks": 12,
     "lead": "A stationary listener, standing on the roadside, records the wavelength of the sound emitted by the siren of a police car travelling at a "
             "constant velocity. In the wavelength-time graph below, NOT drawn to scale, λL is the wavelength of the sound recorded by the listener and "
             "λS is the wavelength of the sound emitted by the siren. Take the speed of sound in air to be 343 m·s⁻¹.",
     "figure": fig("Q6", "Wavelength (m) against time (s): two horizontal lines, λL at 0,40 m and λS at 0,38 m."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Electrostatics", "marks": 3,
     "lead": "P is a +2 nC point charge. X is a point 6 cm away from charge P, as shown in the diagram below.",
     "figure": fig("Q7a", "Point charge P (+2 nC) on the left and point X 6 cm to its right."), "items": q7a},
    {"id": "7.2", "title": "Question 7", "kind": "Electrostatics", "marks": 3,
     "lead": "Point charge S, with a charge of −2 nC, is placed 4 cm to the right of charge P, as shown in the diagram below.",
     "figure": fig("Q7b", "Point charge P (+2 nC) on the left and point charge S (−2 nC) 4 cm to its right."), "items": q7b},
    {"id": "7.3", "title": "Question 7", "kind": "Electrostatics", "marks": 8,
     "lead": "A third point charge T is placed 2 cm to the right of S, as shown in the diagram below. Point charge T experiences a net electrostatic force "
             "of 2,5 x 10⁻⁴ N to the left.",
     "figure": fig("Q7c", "P (+2 nC), then S (−2 nC) 4 cm to its right, then T 2 cm to the right of S."), "items": q7c},
    {"id": "8", "title": "Question 8", "kind": "Electric circuits", "marks": 21,
     "lead": "L1 and L2 are two light bulbs that have the following ratings: L1: 36 W ; 20 V and L2: 48 W ; 32 V. The two bulbs are connected as shown in "
             "the circuit diagram below. The battery has an internal resistance of 0,6 Ω while the conducting wires and the ammeters have negligible "
             "resistance. R1 and R2 are resistors.",
     "figure": fig("Q8", "A battery of emf ε with internal resistance r = 0,6 Ω at the top. Ammeter A1 in the main circuit on the left; resistor R2 (4 Ω) "
                         "on the right. Between them two parallel branches: ammeter A2 in series with bulb L2, and resistor R1 in series with bulb L1."),
     "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Generators", "marks": 11,
     "lead": "The graph below shows how the induced current in a generator varies with time.",
     # (the caption no longer says "the current never goes below zero": 9.1 asks for the type that tells)
     "figure": fig("Q9a", "Induced current (A) against time (s), 0 to 0,04 s: four equal humps, each rising from 0 to a peak of 1,2 A and falling back "
                          "to 0, the first ending at 0,01 s and the last at 0,04 s."), "items": q9a},
    {"id": "9.7", "title": "Question 9", "kind": "Generators", "marks": 2,
     "lead": "The graph below shows how the induced current varies with time after a change was made to the operation of the generator.",
     "figure": fig("Q9b", "Induced current (A) against time (s): two equal humps, each rising from 0 to a peak of 0,6 A and back to 0, one every 0,02 s "
                          "from 0 to 0,04 s."), "items": q9b},
    {"id": "10", "title": "Question 10", "kind": "Photoelectric effect", "marks": 2, "lead": "", "items": q10a},
    {"id": "10.2", "title": "Question 10", "kind": "Photoelectric effect", "marks": 10,
     "lead": "Red light, blue light and green light are shone simultaneously on a sheet of potassium, as shown in the diagram below. Each colour of light "
             "consists of a single frequency. Two maximum kinetic energies of the ejected electrons are possible, namely 6,96 x 10⁻²⁰ J and "
             "2,65 x 10⁻²⁰ J. Each ejected electron has only one of these maximum kinetic energies.",
     "figure": fig("Q10b", "Arrows labelled 'Red light, blue light and green light' point down onto a flat sheet labelled 'Potassium sheet'."), "items": q10b},
    {"id": "10.3", "title": "Question 10", "kind": "Atomic spectra", "marks": 3,
     "lead": "Some of the atoms of a hot gas, made up of a single element, are in an excited state. The spectrum formed by the hot gas is observed on a "
             "screen in a darkened room. The spectrum consists of specific coloured lines on a black background.", "items": q10c},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10; the helpers are the Business Studies P2 2025 reference's) ----
# A written part plays as picking statements: the memo's own points (right, tidied to ONE reading of its "/" alternatives) and
# CLEARLY wrong ones (a key condition dropped or swapped, the inverse relation, another law's or quantity's wording, the opposite
# choice): never a true point the memo leaves out. The learner picks marks/each of them, any right one counts, each right pick earns
# `each`; the cards are shuffled the same way every run. The rubric bullets above stay as the source.
import random


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("ps-p1-2024-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    # 2 ("key words"): the wrong ones are kinetic friction, the normal force, the direction swapped, the opposite effect
    "2.1": (2, ["The force that opposes the tendency of motion of a stationary object relative to a surface."],
               ["The force that opposes the motion of a moving object relative to a surface.",
                "The force that a surface exerts on an object resting on it, perpendicular to the surface.",
                "The force that opposes the tendency of motion of a stationary object, acting perpendicular to the surface.",
                "The force that makes a stationary object start to move along a surface."]),
    # 2 ticks: the choice and the reason (its "/" forms, fs(max) α N, the normal force increases, the weight increases, are one
    # point: one card, so two reasons cannot earn the choice's mark)
    "2.4": (1, ["The maximum static frictional force increases.", "The normal force acting on the crate increases."],
               ["The maximum static frictional force decreases.", "The maximum static frictional force remains the same.",
                "The coefficient of static friction increases when the mass of the crate increases.",
                "The maximum static frictional force does not depend on the normal force.",
                "Adding mass to the crate decreases the normal force on it."]),   # (a 5th wrong card: with six the seeded shuffle
                # put both right cards first, an answer by position)
    # 2 ("key words"): the wrong ones drop "isolated" (friction acting), swap mechanical for kinetic energy, or are other laws
    "4.1": (2, ["The total mechanical energy in an isolated system remains constant."],
               ["The total mechanical energy of an object always remains constant, even when friction acts on it.",
                "The kinetic energy in an isolated system remains constant.", "The total momentum in an isolated system remains constant.",
                "The net work done on an object is equal to the change in the object's kinetic energy."]),
    # 2, either OR form: the wrong ones are impulse, power, the sine for the cosine, mass for force
    "5.1": (2, ["The work done on an object by a constant force F is FΔx cos θ, where F is the magnitude of the force, Δx the magnitude of the "
                "displacement and θ the angle between the force and the displacement.",
                "The work done on an object is the product of the force and the displacement of the object in the direction of the displacement."],
               ["The work done on an object is the product of the force and the time for which the force acts.",
                "The work done on an object is the rate at which energy is transferred to it.",
                "The work done on an object by a constant force F is FΔx sin θ, where θ is the angle between the force and the displacement.",
                "The work done on an object is the product of its mass and its displacement."]),
    # 2 ticks: the choice and the reason (its OR forms, fL < fs and λL > λS, are one point: one card; the frequency form is true,
    # so it is not a wrong card either)
    "6.2": (1, ["The car is moving away from the listener.",
                "The wavelength detected by the listener is longer than the wavelength emitted by the source."],
               ["The car is moving towards the listener.", "The wavelength detected by the listener is shorter than the wavelength emitted by the source.",
                "The frequency detected by the listener is higher than the frequency of the source.",
                "The speed of sound in air increases when the source moves away from the listener."]),
    # 2 ("masses / force omitted: 0/2"): the wrong ones swap the proportions, drop the square, are Newton's law of gravitation, or
    # take the sum of the charges
    "7.3.1": (2, ["The magnitude of the electrostatic force exerted by one point charge on another point charge is directly proportional to the "
                  "product of the magnitudes of their charges and inversely proportional to the square of the distance between them."],
                 ["The magnitude of the electrostatic force exerted by one point charge on another point charge is inversely proportional to the "
                  "product of the magnitudes of their charges and directly proportional to the square of the distance between them.",
                  "The magnitude of the electrostatic force exerted by one point charge on another point charge is directly proportional to the "
                  "product of the magnitudes of their charges and inversely proportional to the distance between them.",
                  "Every particle with mass attracts every other particle with a force directly proportional to the product of their masses and "
                  "inversely proportional to the square of the distance between their centres.",
                  "The magnitude of the electrostatic force exerted by one point charge on another point charge is directly proportional to the "
                  "sum of the magnitudes of their charges and inversely proportional to the square of the distance between them."]),
    # 2 or 0, the memo's OR forms (work done per unit time reads the same as the first); the wrong ones are work, current,
    # potential difference, energy
    "8.1": (2, ["The rate at which work is done.", "The rate at which energy is transferred."],
               ["The product of a force and the displacement in the direction of the force.", "The rate of flow of charge.",
                "The energy transferred per unit charge.", "The total energy used by a device.",
                "The force applied per unit area."]),   # (a 5th wrong card: with six both right cards came first)
    # 2 or 0: the wrong ones are a motor, a cell, a solar cell, charging a battery
    "9.2": (2, ["Mechanical (kinetic) energy is converted to electrical energy."],
               ["Electrical energy is converted to mechanical energy.", "Chemical energy is converted to electrical energy.",
                "Light energy is converted to electrical energy.", "Electrical energy is converted to chemical energy."]),
    # 1, any one of the memo's forms (its ACCEPT, transformers, is one of them); the wrong ones are false claims about DC
    "9.3": (1, ["The power loss in the transmission lines cannot be reduced.", "The current in the transmission lines cannot be made smaller.",
                "Transformers do not work with DC, so the voltage cannot be stepped up or down."],
               ["DC loses no energy in transmission lines.", "Transformers can step DC up to a high voltage.",
                "DC flows in both directions, so it cancels itself out over long distances."]),
    # 2 ("key words"): the wrong ones put DC first, are the peak or the average value, or halve the energy
    "9.5": (2, ["The alternating current that dissipates the same amount of energy as an equivalent DC current."],
               ["The direct current that dissipates the same amount of energy as an equivalent AC current.", "The maximum (peak) value of an alternating current.",
                "The average value of an alternating current over one complete cycle.",
                "The alternating current that dissipates half the energy of an equivalent DC current."]),
    # 2, the memo's answer and its two ACCEPT forms; "slower / frequency decreases / period increases" earns 1/2, so it is neither a
    # right nor a wrong card; the wrong ones (doubled speed; the field or the turns halved at the same speed) do not change the period
    "9.7": (2, ["The speed of rotation of the coil was halved.", "The frequency of rotation was halved.", "The period was doubled."],
               ["The speed of rotation of the coil was doubled.", "The strength of the magnetic field was halved, at the same speed of rotation.",
                "The number of turns on the coil was halved, at the same speed of rotation."]),
    # 2 ("key words"): the wrong ones reverse the process, heat the metal, eject protons, or are the work function
    "10.1": (2, ["The process whereby electrons are ejected from a metal surface when light of suitable frequency is incident on that surface."],
                ["The process whereby light is emitted from a metal surface when electrons strike that surface.",
                 "The process whereby electrons are ejected from a metal surface when the metal is heated.",
                 "The process whereby protons are ejected from a metal surface when light of suitable frequency is incident on that surface.",
                 "The minimum energy needed to eject an electron from a metal surface."]),
    # 2 ticks: the colours that eject electrons, and green's lower frequency with its consequence (the wavelength and photon-energy
    # forms of the second point are the same point: one card)
    "10.2.2": (1, ["Only green light and blue light eject electrons from potassium; red light does not.",
                   "Green light has a lower frequency than blue light, so it ejects the electrons with the lower kinetic energy."],
                  ["Only red light and green light eject electrons from potassium.", "Green light has a higher frequency than blue light.",
                   "Red light ejects the electrons with the lowest maximum kinetic energy.",
                   "A brighter light ejects electrons with a greater maximum kinetic energy."]),
    # 2 ticks: what the lines represent, and when the photons are emitted
    "10.3.2": (1, ["The coloured lines represent the frequencies (energies) of the emitted photons.",
                   "The photons are emitted when electrons move to a lower energy level."],
                  ["The photons are emitted when electrons move to a higher energy level.",
                   "The coloured lines represent the frequencies of the light absorbed by the gas.",
                   "The coloured lines show that the hot gas emits light of every frequency.",
                   "The coloured lines appear because electrons are ejected from the atoms by light."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, a law, a principle, one-statement answers and choices with reasons), so SORTS stays empty and sort_ is kept
# for parity.
SORTS = {}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("ps-p1-2024-11:sort:" + n).shuffle(order)
    rows = [rows[i] for i in order]
    assert marks == len(rows) and len(set(b for _, b in rows)) == len(bins), n
    return {"t": "match", "n": n, "marks": marks, "q": q + " Sort each statement.", "clues": clues, "left": [r for r, _ in rows],
            "right": bins, "a": [b for _, b in rows], "heads": ["STATEMENTS", "SORT INTO"], "groups": True}


for _m in missions:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric" and _it["n"] in SORTS:
            _bins, _rows = SORTS[_it["n"]]
            _new = sort_(_it["n"], _it["q"], _it["marks"], _bins, _rows, _it["clues"])
        elif _it["t"] == "rubric" and _it["n"] in STATEMENTS:
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            _new = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
        else:
            continue
        if _it.get("after"):
            _new["after"] = _it["after"]
        _m["items"][_k] = _new
assert not [i["n"] for m in missions for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"

# every part that played as typed steps before 2026-10-10, now authored multiple choice
assert tuple(AUTHORED) == ("2.3.1", "2.3.2", "3.1.1", "3.1.2", "3.1.3", "4.2", "4.3.1", "4.4", "5.3", "6.3.1", "6.3.2", "7.1", "7.3.3",
                           "8.2.1", "8.2.2", "8.2.3", "8.2.4", "8.3", "9.4", "9.6", "10.2.3"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric", "num")], "a typed calculation, typed number or written answer is left"
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "3.1.2": ["3.1.1"], "3.1.3": ["3.1.2"], "3.2": ["3.1.1"], "4.3.1": ["4.2"], "4.3.2": ["4.3.1"], "4.4": ["4.2", "4.3.2"], "6.3.2": ["6.2", "6.3.1"],
    "8.2.2": ["8.2.1"], "8.2.3": ["8.2.2"], "8.2.4": ["8.2.1", "8.2.2"], "8.3": ["8.2.1", "8.2.4"], "9.3": ["9.1"], "10.2.2": ["10.2.1"],
    "10.3.2": ["10.3.1"]}
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn"]
# no pick part may put all its right cards first (an answer by position)
for _i in ITEMS:
    if _i["t"] == "pickn" and len(_i["pool"]) > 1:
        assert _i["pool"] != list(range(len(_i["pool"]))), (_i["n"], _i["pool"])

FZ_IDS = ["Fg", "FN", "f", "FA", "T", "FE", "Fnet"]   # the force builder's tray (build-play.js FZ), the same for every question


def forces_ok(i):
    """A built force diagram: every force one of the tray's seven, every criterion earned by exactly one force (or the angle), one mark
    each, so the marks add up to the part's; a free force is never one the memo marks."""
    b = i["build"]
    assert all(f["id"] in FZ_IDS for f in b["forces"]) and all(x in FZ_IDS for x in b.get("free", [])), (i["n"], "a force outside the tray")
    assert not {f["id"] for f in b["forces"]} & set(b.get("free", [])), (i["n"], "a marked force is free")
    crits = [f["crit"] for f in b["forces"]] + ([b["angle"]["crit"]] if "angle" in b else [])
    assert sorted(crits) == list(range(len(i["criteria"]))), (i["n"], "every criterion earned by one force or the angle")
    assert all(c["marks"] == 1 for c in i["criteria"]) and len(i["criteria"]) == i["marks"], (i["n"], "one mark a criterion")


FORCES = [i["n"] for i in ITEMS if (i.get("build") or {}).get("kind") == "forces"]
assert FORCES == ["2.2", "5.2"], FORCES
for _i in ITEMS:
    if _i["n"] in FORCES:
        forces_ok(_i)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic physics errors (a sign or direction slip, g used "
                                                       "wrongly or left out, a unit not converted, the wrong formula, a value from the wrong body or "
                                                       "part), 0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, %d marks). A value the memo's "
                                                       "ranges accept is never a wrong option (3.1.3: 37,72 - 37,75 m; 5.3: 20,769 - 20,79 N; 6.3.2: "
                                                       "18,05 - 18,45 m·s⁻¹; 8.2.4: 47,16 - 47,19 V). 8.3 (decide by calculation) ends each working "
                                                       "in its own conclusion: three say 'No', so the working decides, not the conclusion."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "4.3.2", "kind": "no_fit", "detail": "'Write down the change in momentum of trolley A' (1 mark) is a vector, and the memo marks "
                                                   "'10,84 kg·m·s⁻¹ left/opposite direction': it plays as a multiple choice of magnitude and "
                                                   "direction. As a typed number its stem had to print the direction ('opposite in direction to "
                                                   "B's'), half the answer."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 10), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (formulas are images); no API call."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions, the law and the principle "
                                                    "(2.1, 4.1, 5.1, 7.3.1, 8.1, 9.5, 10.1) and the one-statement answers 9.2, 9.3 and 9.7 pick one "
                                                    "card (an OR / ACCEPT form is a further right card); the choices with reasons and the "
                                                    "explanations (2.4, 6.2, 10.2.2, 10.3.2) pick the choice and the memo's points, 1 mark each. A "
                                                    "memo point's '/' forms are ONE card (two cards of one point could earn the choice's mark), "
                                                    "and a true form left out (6.2's fL < fs) is never a wrong card. 9.7's 'slower / frequency "
                                                    "decreases' (1/2) is neither right nor wrong. The choice stays a card beside its reasons: "
                                                    "each is ONE printed part (one number, the player's key)." % len(PICKS)},
        {"n": "2.2", "kind": "no_fit", "detail": "The free-body diagrams 2.2 and 5.2 are BUILT (2026-10-11, build 'forces'): the learner aims "
                                                 "each force from a dot, from the same tray of seven forces, one mark a force for its label AND "
                                                 "direction (within 10°), −1 for each additional force, never below 0 (the memo's 'max 1/2' and "
                                                 "'max 3/4' for one extra). 2.2 asks for the HORIZONTAL forces: the weight and the normal force "
                                                 "are free, as the memo's 'do not penalise if vertical forces are shown'. 'No arrows', 'not "
                                                 "touching the dot' and 'F as components' cannot happen on screen. The other drawings (3.2, 7.2) "
                                                 "are done on paper and self-checked against the memo's criteria."},
        {"n": "10.2.2", "kind": "memo_issue", "detail": "The memo ticks 'Only green and blue light eject electrons / red light does not' (1) and "
                                                        "'green has a lower frequency than blue ... and therefore ejects electrons with the lower "
                                                        "kinetic energy' (1); the old rubric had dropped the first point. Both are now cards."},
        {"n": "10.2.3", "kind": "memo_issue", "detail": "The memo prints W0 = 3,61 x 10⁻¹⁹ J and f = 6,5 x 10¹⁴ Hz: from the rounded W0, f = "
                                                        "6,49 x 10¹⁴ Hz; the memo's 6,5 comes from the unrounded W0 (3,6136 x 10⁻¹⁹ J). The right "
                                                        "option shows the memo's 6,5 x 10¹⁴ Hz; no wrong option is near it."},
        {"n": "8.2.3", "kind": "memo_issue", "detail": "Small slips outside the played working: 8.2.3's OPTION 2 writes R = 17,77 Ω (32/1,8 = 17,78 Ω); "
                                                       "2.3.2's note T = 54,32 N comes from the rounded a = 2,47 (54,28 N unrounded); 8.2.4's OPTION 3 "
                                                       "writes Rp = 9,7 Ω then uses 9,69 Ω. None changes an answer."},
    ],
}
QTOTAL = {"1": 20, "2": 15, "3": 16, "4": 12, "5": 12, "6": 12, "7": 14, "8": 21, "9": 13, "10": 15}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter, spread evenly over A-D across the paper (Question 1's letters are the paper's, A3 B1 C3 D3, and the 2- and 3-way
# choices 5.4, 7.3.2, 9.1, 10.2.1, 10.2.4 keep the paper's order: A4 B2 C6 D3 fixed), so the 22 authored ones carry A5 B8 C3 D6
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
# and across the calculations alone: every letter right at least 3 times, never more than 7
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert min(wspread.values()) >= 3 and max(wspread.values()) <= 7, wspread
print("right options, the paper:", spread, "authored:", wspread)
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; statements:", len(PICKS), "parts")
print("total:", total)
out = Path(__file__).parent / "out" / "ps-p1-2024-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
