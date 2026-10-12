"""Physical Sciences P1 (Physics) Nov 2025, the whole paper (Questions 1 to 10), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets formulas and symbols as
images, so its text layer has gaps.

  python tools/ingest/transcribe_ps_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P1 Nov 2025 Eng.pdf" "<...>/Physical Sciences P1 Nov 2025 MG Afr & Eng.pdf" --id ps-p1-2025-11 --from-json

How the memo's shapes map (Physical Sciences, Murci's rulings 2026-10-10):
  multiple choice -> mcq (graph options: the figure, options "Graph A".."Graph D"; options printed as a table -> optTable); a 3-way
  choice with no explanation -> mcq; one word the memo names -> term; one read-off number with no working -> num (10.1.2).
  Every calculation ("Calculate", "Determine ... ENERGY PRINCIPLES", "Show that", "Choose ... by means of a calculation", and the
  one "Write down" whose memo shows a working, 8.3.2) -> authored multiple choice, `work`: the memo's FIRST working line by line
  (formula, substitution, the answer with its unit, and its direction or conclusion where the memo gives one) and three workings
  each built from a DIFFERENT realistic physics error (a sign or direction slip, g used wrongly or left out, a unit not converted,
  the wrong formula, a value from the wrong body or part), every number recomputed; 0 or full marks. A value the memo also accepts
  (its ranges) is never a wrong option. "Show that r = 0,05 m" (7.3): all four end at the given value, as learners write it; only
  the right one gets there. A definition or law ("Define / State / Describe") and the one-statement conclusion (6.3) -> statements
  (STATEMENTS at the bottom: pick 1 x 2, the memo's wording right, its OR form a second right card, the wrong cards a key condition
  dropped or swapped, the inverse relation, another law's wording); a choice with its reasons ("Choose ... Explain / Give a
  reason") -> statements, the choice and each memo point a card, 1 mark each as the memo ticks them. No memo here weighs two
  sides, so no part plays as a sort. "Draw a (labelled) free-body diagram" (2.2, 5.3) -> draw with build "forces" (2026-10-11: each
  force aimed from a dot from the same tray of seven, marked online as the memo marks it); another "Draw / Sketch / Redraw" -> draw
  with the memo's criteria (self-checked, flagged no_fit).
  A part whose options, cards or criteria show an earlier part's answer opens only after it ("after"). A mission is a question with
  its stem and diagram; a question whose diagram changes part-way is two missions (7, 9, 10).
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves and checked on a contact sheet."""
import json
import re
from pathlib import Path

W, H = 595.44, 841.68
FIGS = {  # tools: scratchpad figs_p1.py; [page, x0, y0, x1, y1] in points
    "1.2": [3, 103.1, 376.0, 551.5, 743.7], "1.3": [4, 233.7, 127.0, 449.5, 262.0], "1.4": [4, 134.9, 537.7, 485.7, 606.5],
    "1.5": [5, 185.1, 138.8, 474.0, 169.9], "1.7": [5, 180.5, 525.7, 436.0, 584.0], "1.8": [6, 193.0, 150.0, 441.0, 257.0],
    "1.10": [7, 97.2, 180.0, 549.3, 558.5], "Q2": [8, 197.0, 183.2, 397.2, 240.3], "Q3": [9, 189.3, 147.6, 290.9, 276.3],
    "Q4": [10, 136.0, 361.0, 455.0, 539.3], "Q5": [11, 114.7, 202.7, 506.1, 355.7], "Q6": [12, 91.0, 386.9, 494.0, 619.4],
    "Q7a": [13, 147.5, 166.5, 322.1, 245.4], "Q7b": [13, 129.4, 440.0, 463.7, 519.0], "Q8": [14, 44.0, 221.0, 549.0, 396.0],
    "Q9a": [15, 116.0, 152.2, 482.0, 334.0], "Q9b": [15, 102.8, 499.3, 464.0, 645.3], "Q10b": [16, 138.7, 494.3, 474.0, 612.0]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points (key words, "... defined: 0/2", ACCEPT limits): never scored, never shown
rub = lambda n, q, marks, bullets, clues, each=None, notes=None: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets,
                                                                 **({"each": each} if each else {}), **({"notes": notes} if notes else {})}
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


# ---- QUESTION 1: multiple choice, the question paper pages 3-7 and the memo page 2 ----
q1 = [
    mcq("1.1", "The net force acting on an object on a horizontal surface is always …",
        ["in the direction of motion of the object.", "in the direction of acceleration of the object.",
         "zero when the object moves at constant acceleration.", "increasing when the object moves at constant acceleration."], 1,
        ["Newton's second law links the net force to one quantity's direction.", "An object can move one way while slowing down."]),
    mcq("1.2", "A hot-air balloon is moving upwards at a constant velocity. A small stone is dropped from THE BALLOON. Which ONE of the following "
        "graphs represents the motions of the balloon and the stone? Ignore the effects of friction on the stone.",
        ["Graph A", "Graph B", "Graph C", "Graph D"], 1,
        # (the second clue no longer describes the right line's whole path: with the first it named graph B)
        ["At the moment it is dropped, the stone has the balloon's velocity.", "Once released, only gravity acts on the stone: which way does its velocity change?"],
        figure=fig("1.2", "Four velocity-time graphs, A and B on top and C and D below, each with v (m·s⁻¹) up and t (s) across and two lines, "
                   "'stone' and 'balloon'. A: the balloon a horizontal line above zero; the stone starts where the balloon line meets the axis and "
                   "rises. B: the balloon horizontal above zero; the stone starts at the balloon's velocity and falls in a straight line below zero. "
                   "C: the balloon horizontal above zero; the stone starts below zero and rises. D: the balloon horizontal above zero; the stone "
                   "starts at zero and rises.")),
    mcq("1.3", "A motor fixed to the ground is used to lift a box vertically upwards at a CONSTANT VELOCITY. Consider the statements below for the "
        "upward motion of the box.\n(i) The rate at which work is done by the motor on the box increases.\n(ii) The rate at which work is done by "
        "the motor on the box is constant.\n(iii) The mechanical energy of the box increases.\n(iv) The mechanical energy of the box is constant.\n"
        "Which of the statements above are CORRECT?",
        ["(i) and (iii) only", "(ii) and (iv) only", "(ii) and (iii) only", "(i) and (iv) only"], 2,
        ["Power = force x velocity: what happens to each at constant velocity?", "The box rises: what happens to its potential energy?"],
        figure=fig("1.3", "A motor on the ground with a string over a wheel above it; the string's other end holds a box; an arrow beside the box points up.")),
    mcq("1.4", "Objects P and Q, with masses m and 2m respectively, have the same momentum. The velocity of P is …",
        ["equal to the velocity of Q.", "half the velocity of Q.", "twice the velocity of Q.", "four times the velocity of Q."], 2,
        # (the old second clue, "Half the mass needs ... the velocity.", left one word to fill in: the answer)
        ["p = mv, and p is the same for both.", "Write p = mv for P and for Q, and set the two equal."],
        figure=fig("1.4", "Two boxes on a horizontal surface: a smaller box P on the left and a larger box Q on the right.")),
    mcq("1.5", "A block moves along a rough horizontal surface while a horizontal force F of magnitude 18 N and a constant kinetic frictional force of "
        "magnitude 6 N act on it. Which ONE of the following combinations of ACCELERATION and NET WORK DONE ON THE BLOCK is CORRECT?",
        ["Constant; increases", "Increases; constant", "Increases; increases", "Constant; constant"], 0,
        # (the old clues, "so the net force is ..." and "the distance keeps growing", read together named option A)
        ["Find the net force on the block: does it change as the block moves?", "Net work done = net force x distance moved."],
        optTable={"head": ["ACCELERATION", "NET WORK DONE ON THE BLOCK"],
                  "rows": [["Constant", "Increases"], ["Increases", "Constant"], ["Increases", "Increases"], ["Constant", "Constant"]]},
        figure=fig("1.5", "A block on a horizontal surface: F = 18 N pulls it to the right, fk = 6 N acts to the left.")),
    mcq("1.6", "A star's spectrum, observed from Earth, is red shifted. Which ONE of the following statements is CORRECT?",
        ["The speed of light is increasing.", "The star is moving towards Earth.", "The frequency of each spectral line has increased.",
         "The wavelength of each spectral line has increased."], 3,
        # (the old clues, "red has the longest wavelengths" and "the lines move towards red", read together named option D)
        ["A red shift is the Doppler effect for light.", "When a source moves away from you, are its waves stretched or squeezed?"]),
    mcq("1.7", "Three point charges, Q1, Q2 and Q3, are fixed in a straight line. Q1 is r metres from Q2, while Q3 is 2r metres from Q2. The magnitude "
        "of the charge on Q2 is q. The net electrostatic force on charge Q1 is zero. What is the magnitude of charge Q3 in terms of q?",
        ["⅑q", "⅓q", "3q", "9q"], 3,
        # (the old second clue wrote out the equation kQ3/(3r)² = kq/r², which solves to the answer)
        ["Q3 is 3r from Q1, Q2 is r from Q1.", "The net force on Q1 is zero: write Coulomb's law for each force on Q1 and set them equal."],
        figure=fig("1.7", "Charges Q1, Q2 and Q3 on a dashed line: r between Q1 and Q2, 2r between Q2 and Q3.")),
    mcq("1.8", "Three identical light bulbs, X, Y and Z, are connected in a circuit, as shown in the diagram below. Switch S is initially closed. "
        "Ignore the internal resistance of the battery. Switch S is now opened. How will the brightness of bulbs X and Y be affected?",
        ["Increases; decreases", "Decreases; increases", "Increases; increases", "Decreases; decreases"], 1,
        # (the second clue asked the question instead of answering both halves: it named option B)
        ["Opening S removes Z: the total resistance goes up.", "Then ask how the current through X changes, and how the battery's voltage is now shared between X and Y."],
        optTable={"head": ["BRIGHTNESS OF BULB X", "BRIGHTNESS OF BULB Y"],
                  "rows": [["Increases", "Decreases"], ["Decreases", "Increases"], ["Increases", "Increases"], ["Decreases", "Decreases"]]},
        figure=fig("1.8", "A battery in series with bulb X; after X the circuit splits into bulb Y and, through switch S, bulb Z, in parallel.")),
    mcq("1.9", "How does the commutator in a DC motor ensure that the coil rotates continuously in ONE direction?",
        ["By reducing friction", "By converting AC to DC", "By reversing the direction of the current in the coil",
         "By maintaining electrical contact between the external and the internal circuits"], 2,
        ["Every half turn, the force on each side of the coil would reverse.", "What must the current in the coil do to keep the turning one way?"]),
    mcq("1.10", "Light of different wavelengths is incident on a metal surface. Which ONE of the following graphs shows the CORRECT relationship between "
        "the maximum kinetic energy of the photoelectrons, Ek(max), and the inverse of the wavelength of the incident light, 1/λ?",
        ["Graph A", "Graph B", "Graph C", "Graph D"], 2,
        # (the old second clue, "the line starts on the axis", with the first's straight line described graph C)
        ["Ek(max) = hc/λ − W0: a straight line against 1/λ.", "Is there a lowest frequency (a threshold) below which no electrons are emitted?"],
        figure=fig("1.10", "Four graphs of Ek(max) (J) up against 1/λ (m⁻¹) across. A: a straight line rising from the origin. B: a line starting "
                   "on the 1/λ axis to the right of the origin and falling below it. C: a line starting on the 1/λ axis to the right of the origin "
                   "and rising. D: a line falling from the origin.")),
]

# ---- QUESTION 2, the question paper page 8 and the memo pages 3-5 ----
q2 = [
    rub("2.1", "State Newton's Second Law of Motion in words.", 2, [
        "When the net/resultant force acts on an object, the object will accelerate in the direction of the force and the acceleration is directly "
        "proportional to the force and inversely proportional to the mass of the object. (2)",
        "OR — The net/resultant force acting on an object is equal to the rate of change of momentum of the object (in the direction of the net force). (2 or 0)"],
        ["It links net force, mass and acceleration.", "Directly proportional to one, inversely to the other."], each=2,
        notes=["Key words: net/resultant force; acceleration directly proportional to the force; inversely proportional to the mass. A key word omitted: deduct 1."]),
    draw("2.2", "Draw a labelled free-body diagram showing ALL the forces acting on the block.", 4, [
        ["w: Fg / Fw / weight / mg / 49 N / gravitational force, downwards", 1], ["F: FA / 18 N / applied force, at θ above the horizontal", 1],
        ["fs(max): Ff / fs / f / friction (force) / (static) friction, horizontal, to the left", 1], ["N: FN / normal (force), upwards", 1]],
        ["Four forces: weight, the applied force, friction and the normal force.", "Draw them from one dot, each with an arrow and a label."],
        memo="A mark for each label AND its arrow; fk not accepted as label. Any additional force(s), everything correct but no arrows, or forces "
             "not touching the dot: max 3/4.",
        # BUILT (2026-10-11, build "forces"): w 270°, N 90°, static friction against F's pull (180°), each within 10°; F at θ above the
        # horizontal, θ found only in 2.3.1 (33,56°) and drawn at about 26° in the figure, so F earns within 14° of 34° (20° to 48°). The
        # tray's friction is labelled f (the memo accepts f; it does not accept fk, which the tray never offers)
        build={"kind": "forces", "surface": 0, "forces": [{"id": "Fg", "at": 270, "crit": 0}, {"id": "FA", "at": 34, "tol": 14, "crit": 1},
                                                          {"id": "f", "at": 180, "crit": 2}, {"id": "FN", "at": 90, "crit": 3}]}),
    work("2.3.1", "The horizontal component of force F is 15 N. Calculate θ.", 2, [
        "Fx = F cos θ\n15 = 18 cos θ\nθ = 33,56°",                        # the memo
        "Fx = F sin θ\n15 = 18 sin θ\nθ = 56,44°",                        # the sine for the horizontal component
        "Fx = F tan θ\n15 = 18 tan θ\nθ = 39,81°",                        # the wrong ratio (tan)
        "Fx = F cos θ\n15 = 18 cos θ\nθ = 0,59°"], 0,                     # the calculator in radians
        ["You know F and its horizontal component.", "Which trig ratio links the side next to θ with the hypotenuse?"]),
    work("2.3.2", "The horizontal component of force F is 15 N. Calculate the coefficient of static friction.", 5, [
        "fs(max) = μsN\nfs(max) = μs(mg + F sin θ)\n15 = μs((5)(9,8) + 18 sin 33,56°)\nμs = 0,25",       # F's vertical part pushes down (sign)
        "fs(max) = μsN\nfs(max) = μs(mg − F cos θ)\n15 = μs((5)(9,8) − 18 cos 33,56°)\nμs = 0,44",       # the horizontal part taken off N
        "fs(max) = μsN\nfs(max) = μs(mg − F sin θ)\n18 = μs((5)(9,8) − 18 sin 33,56°)\nμs = 0,46",       # F itself as the friction (wrong value)
        "fs(max) = μsN\nfs(max) = μs(mg − F sin θ)\n15 = μs((5)(9,8) − 18 sin 33,56°)\nμs = 0,38"], 3,  # the memo (its OPTION 1)
        # (the old clues, "friction equals the horizontal pull" and "N is less than mg", read together picked out option D's lines)
        ["The block is on the point of moving: which force does the maximum static friction balance?",
         "Does F's vertical component press the block onto the surface or lift it?"],
        after=["2.3.1"]),   # the options show θ = 33,56°, 2.3.1's answer
    rub("2.4", "Angle θ is decreased while the magnitude of force F remains constant. How will the friction acting on the block be affected? Choose from "
        "INCREASES, DECREASES or REMAINS THE SAME. Explain the answer.", 4, [
        "Increases (1)", "The vertical component of F decreases (1)", "The normal force increases (1)",
        "μs remains constant, so fs(max) increases: it is directly proportional to the normal force (1)",
        "OR — Decreases (1)", "The horizontal component of F increases (1)", "The block will move / Fnet will increase (1)",
        "The kinetic friction is less than the maximum static friction (fk < fs(max)) (1)",
        "OR — Remains the same (1)", "A relevant calculation (1)", "choosing μk smaller than μs (1)", "and θ that together with μk gives fk = 15 N (1)"],
        ["Resolve F at the smaller angle: which component grows and which shrinks?", "How does the normal force depend on F's vertical component?"]),
]

# ---- QUESTION 3, the question paper page 9 and the memo pages 5-9 ----
q3 = [
    rub("3.1", "Define the term free fall.", 2, [
        "Motion under the influence of weight/gravitational force only. (2 or 0)"],
        ["Which force is the ONLY one acting?", "Think of a ball thrown upwards with no air resistance: what acts on it the whole time?"], each=2,
        notes=["A projectile defined: 0/2."]),
    work("3.2", "Using EQUATIONS OF MOTION ONLY, calculate the value of p.", 3, [
        "vf = vi + aΔt\n0 = 15 + (9,8)Δt\nΔt = −1,53 s",                          # a = +9,8 with upwards positive (sign)
        "vf = vi + aΔt\n0 = 15 + (−9,8)Δt\nΔt = 1,53 s",                          # the memo (OPTION 1, upwards positive)
        "vf = vi + aΔt\n0 = 15 + (−10)Δt\nΔt = 1,50 s",                           # g taken as 10, not the data sheet's 9,8
        "Δy = viΔt + ½aΔt²\n0 = 15Δt + ½(−9,8)Δt²\nΔt = 3,06 s"], 1,              # Δy = 0: the time back to the roof, not to the top
        ["At time p the velocity is 0: the top of the flight.", "Choose upwards as positive and keep the signs of the velocity and the acceleration consistent."]),
    work("3.3", "The ball strikes the ground 3,36 seconds after it was thrown upwards. Calculate q.", 3, [
        "vf² = vi² + 2aΔy\nvf² = (15)² + 2(−9,8)(−5)\nq = 17,97 m·s⁻¹",           # the memo (OPTION 1, upwards positive)
        "vf² = vi² + 2aΔy\nvf² = (15)² + 2(−9,8)(5)\nq = 11,27 m·s⁻¹",            # the ground taken 5 m ABOVE the start (sign)
        "vf² = vi² + aΔy\nvf² = (15)² + (−9,8)(−5)\nq = 16,55 m·s⁻¹",             # the 2 left out of the formula
        "vf = vi + aΔt\nvf = 0 + (−9,8)(3,36)\nq = 32,93 m·s⁻¹"], 0,              # from rest, but over the whole 3,36 s (wrong part)
        # (the old second clue wrote the right working's formula, vf² = vi² + 2aΔy)
        ["q is the speed when the ball hits the ground, 5 m below where it started.",
         "Pick an equation of motion that uses what you know: vi, the acceleration and the displacement (mind its sign)."]),
    rub("3.4", "The ball bounces to a maximum height of 3 m after it struck the ground. Is the collision with the ground ELASTIC or INELASTIC? Explain "
        "the answer WITHOUT the use of calculations.", 3, [
        "Inelastic. (1)", "The height decreased/smaller. (1)",
        "The velocity with which the ball strikes the ground is not the same as the velocity with which it left the ground / kinetic energy is "
        "converted to heat and sound energy / kinetic energy is NOT conserved / the kinetic energy is not the same before and after the ball strikes "
        "the ground. ACCEPT: kinetic energy is lost. (1)"],
        # (the old first clue, "5 m below the top before", misplaced the heights)
        ["Compare how high the ball rose before the bounce with how high it rises after it.", "What does 'elastic' say about the kinetic energy?"],
        notes=["Do NOT accept any calculation as an explanation."]),
    draw("3.5", "Sketch a velocity versus time graph for the motion of the ball from the time it was projected until it reached the maximum height after "
         "it bounced. Show the following NUMERICAL VALUES on the graph: the initial velocity; time p; velocity q.", 4, [
        ["A straight line starting at v = 15 m·s⁻¹ with negative final velocity (or starting at −15 m·s⁻¹ with positive final velocity)", 1],
        ["The straight line cuts the time axis at the time calculated in 3.2 (1,53 s)", 1],
        ["The correct velocity calculated in 3.3 (17,97 m·s⁻¹) where the ball is on the ground", 1],
        ["The velocity of the second line is less than in 3.3; the lines are parallel and it ends at v = 0", 1]],
        ["One straight line until the bounce, then a second, parallel one.", "Mark 15, your p and your q on the axes."],
        memo="Positive marking from 3.2 and 3.3. Accept if no contact time is shown on the graph.",
        after=["3.2", "3.3"])]   # its criteria show p = 1,53 s and q = 17,97 m·s⁻¹

# ---- QUESTION 4, the question paper page 10 and the memo pages 9-10 ----
q4 = [
    rub("4.1", "Define the term impulse.", 2, [
        "The product of the resultant/net force acting on an object and the time the (net) force acts on the object. (2)",
        "OR — The product of the resultant/net force and the contact time. (2)"],
        ["Impulse = force x ...", "Which force, and which time?"], each=2, notes=["Key words: product; resultant/net force; time. A key word omitted: deduct 1."]),
    work("4.2.1", "Calculate the average net force acting on the ball.", 3, [
        "Fnet = gradient = {Δpf}/{Δ(Δt)}\nFnet = {4,5 − 0}/{0,03 − 0}\nFnet = 150 N to the right (opposite to the ball's original direction)",
        # ^ the line read from the origin, not from (0,01; 0) (wrong point)
        "Fnet = m × gradient = m{Δpf}/{Δ(Δt)}\nFnet = (0,15){4,5 − 0}/{0,03 − 0,01}\nFnet = 33,75 N to the right (opposite to the ball's original direction)",
        # ^ multiplies by the mass: the gradient is already Δp/Δt (wrong formula)
        "Fnet = gradient = {Δpf}/{Δ(Δt)}\nFnet = {4,5 − 0}/{0,03 − 0,01}\nFnet = 225 N to the right (opposite to the ball's original direction)",
        # ^ the memo (OPTION 1)
        "Fnet = gradient = {Δpf}/{Δ(Δt)}\nFnet = {4,5 − 0}/{0,03 − 0,01}\nFnet = 225 N to the left (in the ball's original direction)"], 2,
        # ^ the direction slip
        ["What quantity does the gradient of a momentum against time graph give?", "Read two points that lie ON the line."]),
    work("4.2.2", "Calculate the magnitude of the initial velocity of the ball.", 4, [
        "FnetΔt = Δp = mvf − mvi\n(−225)(0,03) = 4,5 − (0,15)vi\nvi = 75 m·s⁻¹\nMagnitude of vi = 75 m·s⁻¹",        # Fnet's sign against pf's (sign)
        "FnetΔt = Δp = mvf − mvi\n(225)(0,03) = 4,5 − (150)vi\nvi = −0,015 m·s⁻¹\nMagnitude of vi = 0,015 m·s⁻¹",   # 150 g not converted to kg
        "FnetΔt = mvi\n(225)(0,03) = (0,15)vi\nvi = 45 m·s⁻¹\nMagnitude of vi = 45 m·s⁻¹",                         # impulse taken as the momentum
        "FnetΔt = Δp = mvf − mvi\n(225)(0,03) = 4,5 − (0,15)vi\nvi = −15 m·s⁻¹\nMagnitude of vi = 15 m·s⁻¹"], 3,  # the memo (OPTION 1)
        # (the old first clue, "Impulse = change in momentum, with the mass in kg", with the second's signs picked out option D)
        ["Which principle links the impulse on the ball to its momentum before and after the hit?",
         "The ball comes in one way and leaves the other: watch the signs and the units."],
        after=["4.2.1"]),   # the options show Fnet = 225 N, 4.2.1's answer
    draw("4.3", "Redraw the graph in the ANSWER BOOK and label it as A. On the same set of axes, draw the graph that will be obtained when a ball with a "
         "bigger mass is used, without changing the initial velocity and average net force. Label this as B.", 2, [
        ["Line B parallel to A (same net force: same gradient), shifted to the right (bigger initial momentum to undo), both labelled", 2]],
        ["Same net force: same gradient.", "A bigger mass at the same speed has more initial momentum to reverse."],
        memo="2 or 0. Labels A and B not indicated: 0/2. Full marks for solid lines with labels.")]

# ---- QUESTION 5, the question paper page 11 and the memo pages 11-13 ----
q5 = [
    rub("5.1", "State the work-energy theorem in words.", 2, [
        "The net/total work done (on an object) is equal to the change in the object's kinetic energy. (2)",
        "OR — The work done (on an object) by a resultant/net force is equal to the change in the object's kinetic energy. (2)"],
        ["It links work and one kind of energy.", "Which work: by which force?"], each=2,
        notes=["Key words: net/total work done; equal; change in kinetic energy. A key word omitted: deduct 1."]),
    work("5.2", "Using ENERGY PRINCIPLES ONLY, calculate the kinetic energy of the crate at point B.", 3, [
        "Wnet = ΔEk\n(12)(7) cos 0° = Ekf − 0\nEkf = 84 J",                    # the memo
        "Wnet = ΔEk\n(12)(7) cos 20° = Ekf − 0\nEkf = 78,93 J",                # the slope's 20° used on the flat (wrong part)
        "Wnet = ΔEk\n(3)(9,8)(7) cos 0° = Ekf − 0\nEkf = 205,8 J",             # the weight mg used for F (g used wrongly)
        "Wnet = ΔEk\n½(12)(7) cos 0° = Ekf − 0\nEkf = 42 J"], 0,               # the ½ of Ek put on the work (wrong formula)
        # (the old clues, "F does all the work" and "Work = F Δx cos θ, from rest", read together picked out option A)
        ["From A to B the surface is frictionless: which force does net work on the crate?",
         "What is the angle between that force and the crate's displacement?"]),
    draw("5.3", "Force F is removed when the crate reaches point B. The crate then experiences a constant frictional force of 21 N as it moves down the "
         "incline. Draw a free-body diagram showing ALL the forces acting on the crate as it moves down the incline.", 3, [
        ["w: Fw / Fg / mg / gravitational force / 29,4 N / weight, vertically downwards", 1],
        ["f: Ff / fk / (kinetic) friction / 21 N, up the incline", 1], ["N: FN / normal (force), perpendicular to the incline", 1]],
        ["Three forces once F is gone.", "Friction opposes the motion down the slope; N is perpendicular to the slope."],
        memo="A mark for each label AND its arrow. Any additional force(s), no arrows, or forces not touching the dot: max 2/3.",
        # BUILT (2026-10-11, build "forces"; a force diagram, so converted): the incline falls to the right at 20° and the crate slides down
        # it, so friction acts up the incline (160°), the normal force perpendicular to it (70°), the weight straight down (270°), each
        # within 10°; F is gone, so an applied force is an extra (−1)
        build={"kind": "forces", "surface": -20, "forces": [{"id": "Fg", "at": 270, "crit": 0}, {"id": "f", "at": 160, "crit": 1}, {"id": "FN", "at": 70, "crit": 2}]}),
    work("5.4", "Force F is removed when the crate reaches point B. The crate then experiences a constant frictional force of 21 N as it moves down the "
         "incline. Using ENERGY PRINCIPLES ONLY, determine whether the crate will pass point C.", 5, [
        "Wnet = ΔEk\nWFg + Wfk = Ekf − Eki\n(3)(9,8) sin 20° Δx cos 180° + (21)Δx cos 180° = 0 − 84\nΔx = 2,70 m\n"
        "2,70 m < 6,8 m: the crate will not pass point C",                                  # gravity's work taken against the motion (sign)
        "Wnet = ΔEk\nWFg + Wfk = Ekf − Eki\n(3)(9,8) cos 20°(6,8) cos 0° + (21)(6,8) cos 180° = Ekf − 84\nEkf = 129,06 J\n"
        "129,06 J > 0 J: the crate will pass point C",                                      # cos 20° for gravity's component (wrong formula)
        "Wnet = ΔEk\nWFg + Wfk = Ekf − Eki\n(3) sin 20° Δx cos 0° + (21)Δx cos 180° = 0 − 84\nΔx = 4,21 m\n"
        "4,21 m < 6,8 m: the crate will not pass point C",                                  # g left out: the mass used as the weight
        "Wnet = ΔEk\nWFg + Wfk = Ekf − Eki\n(3)(9,8) sin 20° Δx cos 0° + (21)Δx cos 180° = 0 − 84\nΔx = 7,68 m\n"
        "7,68 m > 6,8 m: the crate will pass point C"], 3,                                  # the memo (OPTION 1)
        ["Down the slope, gravity's component along the slope does positive work and friction does negative work.",
         "Work out how far the crate slides before its kinetic energy from B is used up, then compare with BC = 6,8 m."],
        after=["5.2"])]   # the options show Ek at B = 84 J, 5.2's answer

# ---- QUESTION 6, the question paper page 12 and the memo pages 13-14 ----
q6 = [
    rub("6.1", "STATE the Doppler effect.", 2, [
        "The change in frequency (or pitch) of the sound detected by a listener, because the sound source and the listener have different velocities "
        "relative to the medium of sound propagation. (2)",
        "OR — An (apparent) change in (observed/detected) frequency (pitch) as a result of the relative motion between a sound source and an observer. (2)"],
        ["Think of an ambulance passing you: what changes?", "Something must be different between the source and the listener."], each=2,
        notes=["Key words: change in frequency; source and listener; relative motion/different velocities. A key word omitted: deduct 1."]),
    term("6.2.1", "For this experiment, write down the independent variable.", ["Velocity of the ambulance", "Speed of the ambulance", "Velocity of the source",
                                                                                "Speed of the source", "vs"],
         # (the old second clue, "The graph's horizontal axis.", pointed to the answer by position)
         ["What did the experimenters change on purpose?", "The detected frequency depends on it."]),
    term("6.2.2", "For this experiment, write down a controlled variable.", [
        "Frequency of the sound produced by the ambulance siren", "Frequency of the siren", "Wavelength of the sound produced by the siren", "fs",
        "Speed of sound", "Density of air", "Temperature of air", "The detector is stationary", "The listener is stationary"],
         ["What was kept the same in every run?", "Think of the siren itself, the air, or the detector."]),
    rub("6.3", "What conclusion can be made for Part B of this experiment?", 2, [
        "As the velocity of the ambulance increases, the detected frequency decreases. (2)"],
        ["Part B: the ambulance moves AWAY from the detector.", "Which line is Part B's? Compare its frequency at 5 m·s⁻¹ and at 25 m·s⁻¹."], each=2,
        notes=["Inversely proportional indicated: 0/2."]),
    work("6.4", "Calculate the speed of sound in air.", 6, [
        "fL = {v}/{v − vs} fs (approaching)\nfs = 1115 Hz (the reading for Part B)\n1298 = {v}/{v − 25}(1115)\n1298(v − 25) = 1115v\n"
        "183v = 32 450\nv = 177,32 m·s⁻¹",                                                   # Part B's reading taken as the siren's own (wrong value)
        "fL = {v}/{v − vs} fs (approaching)\n1298 = {v}/{v − 25} fs, so vfs = 1298(v − 25) … (1)\nfL = {v}/{v + vs} fs (moving away)\n"
        "1115 = {v}/{v + 25} fs, so vfs = 1115(v + 25) … (2)\n(1) = (2): 1298(v − 25) = 1115(v + 25)\nv = 329,64 m·s⁻¹",   # the memo
        "fL = {v}/{v + vs} fs (approaching)\n1298 = {v}/{v + 25} fs, so vfs = 1298(v + 25) … (1)\nfL = {v}/{v − vs} fs (moving away)\n"
        "1115 = {v}/{v − 25} fs, so vfs = 1115(v − 25) … (2)\n(1) = (2): 1298(v + 25) = 1115(v − 25)\nv = −329,64 m·s⁻¹",  # the signs swapped
        "fL = {v}/{v − vs} fs (approaching)\nfs = {1298 + 1115}/{2} = 1206,5 Hz\n1298 = {v}/{v − 25}(1206,5)\n1298(v − 25) = 1206,5v\n"
        "91,5v = 32 450\nv = 354,64 m·s⁻¹"], 1,                                               # the siren's frequency taken halfway (misread)
        ["Read the two detected frequencies at 25 m·s⁻¹ and decide which line is the approaching ambulance.",
         "Two Doppler equations, two unknowns (v and fs): divide one by the other."],
        after=["6.3"])]   # the options say which reading is Part B's (moving away), the heart of 6.3's conclusion

# ---- QUESTION 7, the question paper page 13 and the memo pages 14-15 ----
q7a = [
    rub("7.1", "Describe an electric field.", 2, ["A region of space in which an electric charge experiences a force. (2 or 0)"],
        ["Where in space does it exist?", "What happens to a charge placed there?"], each=2),
    draw("7.2", "Draw the electric field pattern due to the charge on sphere X.", 2, [
        ["Direction: arrows pointing away from the positive charge", 1], ["Field lines radially outward", 1]],
        ["X is positive.", "Field lines point the way a positive test charge would be pushed."],
        memo="Two or more field lines inside the sphere / not touching the sphere / crossing each other: deduct 1. More than one charge drawn: 0/2."),
    # "Show that" (a given answer): every option ends at r = 0,05 m, as learners write it; only the memo's working gets there
    work("7.3", "Show, by means of a calculation, that r = 0,05 m.", 3, [
        "E = {kQ}/{r²}\n1,08 × 10⁶ = {(9 × 10⁹)(3 × 10⁻⁷)}/{r²}\nr = 0,05 m",           # the memo
        "E = {kQ}/{r²}\n1,08 × 10⁶ = {(9 × 10⁹)(3 × 10⁷)}/{r²}\nr = 0,05 m",            # 10⁻⁷ written 10⁷ (a power slip)
        "E = {kQ}/{r²}\n1,08 × 10⁶ = {(6,67 × 10⁻¹¹)(3 × 10⁻⁷)}/{r²}\nr = 0,05 m",      # G substituted for k (the wrong constant)
        "E = {kQ}/{r}\n1,08 × 10⁶ = {(9 × 10⁹)(3 × 10⁻⁷)}/{r}\nr = 0,05 m"], 0,         # r not squared (the wrong formula)
        # (the old clues wrote the right working's formula, E = kQ/r², and its rearrangement r² = kQ / E)
        ["The field at P is due to the charge on X alone, r metres away.", "Every option claims 0,05 m: work its numbers through to see which really gets there."])]
q7b = [
    work("7.4", "The NET FORCE acting on sphere X is 0,0427 N at point A. Is the surface frictionless? Choose from YES or NO. Explain the answer by "
         "means of a calculation.", 6, [
        "FXY = {kQXQY}/{r²} = {(9 × 10⁹)(3 × 10⁻⁷)(5 × 10⁻⁷)}/{(0,05)²}\nFXY = 0,54 N\nFXZ = {kQXQZ}/{r²} = {(9 × 10⁹)(3 × 10⁻⁷)(4 × 10⁻⁷)}/{(0,04)²}\n"
        "FXZ = 0,68 N\nFnet(E) = 0,68 + 0,54 = 1,22 N\nNo: Fnet(E) ≠ Fnet (1,22 N ≠ 0,0427 N), so friction acts",
        # ^ the two forces added: Y pulls X left, Z pulls it right (direction slip)
        "FXY = {kQY}/{r²} = {(9 × 10⁹)(5 × 10⁻⁷)}/{(0,05)²}\nFXY = 1,8 × 10⁶ N\nFXZ = {kQZ}/{r²} = {(9 × 10⁹)(4 × 10⁻⁷)}/{(0,04)²}\n"
        "FXZ = 2,25 × 10⁶ N\nFnet(E) = 2,25 × 10⁶ − 1,8 × 10⁶ = 4,5 × 10⁵ N\nNo: Fnet(E) ≠ Fnet (4,5 × 10⁵ N ≠ 0,0427 N), so friction acts",
        # ^ the field E = kQ/r² taken as the force, X's own charge left out (wrong formula)
        "FXY = {kQXQY}/{r²} = {(9 × 10⁹)(3 × 10⁻⁷)(5 × 10⁻⁷)}/{(0,05)²}\nFXY = 0,54 N\nFXZ = {kQXQZ}/{r²} = {(9 × 10⁹)(3 × 10⁻⁷)(4 × 10⁻⁷)}/{(0,04)²}\n"
        "FXZ = 0,68 N\nFnet(E) = 0,68 − 0,54 = 0,14 N\nNo: Fnet(E) ≠ Fnet (0,14 N ≠ 0,0427 N), so friction acts",
        # ^ the memo (OPTION 1)
        "FXY = {kQXQY}/{r²} = {(9 × 10⁹)(3 × 10⁻⁷)(5 × 10⁻⁷)}/{(0,05)²}\nFXY = 0,54 N\nFXZ = {kQXQZ}/{r²} = {(9 × 10⁹)(3 × 10⁻⁷)(4 × 10⁻⁷)}/{(0,05)²}\n"
        "FXZ = 0,43 N\nFnet(E) = 0,54 − 0,43 = 0,11 N\nNo: Fnet(E) ≠ Fnet (0,11 N ≠ 0,0427 N), so friction acts"], 2,
        # ^ Y's distance r used for Z too (a value from the wrong part)
        ["Work out the electrostatic force of Y and of Z on X, then the net electrostatic force.", "If that is more than 0,0427 N, something else (friction) acts."]),
    mcq("7.5", "Sphere Y is brought into contact with sphere X, and is placed back in its original position. How will the magnitude of the force that "
        "sphere X now exerts on sphere Y be affected? Choose from INCREASES, DECREASES or REMAINS THE SAME.",
        ["Increases", "Decreases", "Remains the same"], 1,
        # (the old first clue worked the shared charge out, (+3 + (−5))/2 each, leaving one multiplication to the answer)
        ["When the spheres touch, their total charge is shared between them: what is that total?", "Compare the product of the charges before and after."])]

# ---- QUESTION 8, the question paper page 14 and the memo pages 16-18 ----
q8 = [
    rub("8.1", "Define the term emf.", 2, [
        "Maximum/total energy provided/work done by a battery/cell per unit/coulomb of charge passing through it. (2 or 0)"],
        ["Its unit, the volt, is a joule per coulomb.", "Is it measured with or without a current in the battery?"], each=2),
    work("8.2", "Switch S1 remains open while switch S2 is closed. The reading on ammeter A2 is 120 A. Calculate the reading on the voltmeter.", 3, [
        "R = {V}/{I}\n12 = {V}/{120}\nV = 1 440 V",                     # a headlight's 12 Ω (the wrong body)
        "R = {I}/{V}\n0,1 = {120}/{V}\nV = 1 200 V",                    # the formula upside down
        "R = {V}/{I}\n0,1 = {V}/{120}\nV = 8,33 × 10⁻⁴ V",              # rearranged as V = R/I
        "R = {V}/{I}\n0,1 = {V}/{120}\nV = 12 V"], 3,                   # the memo
        ["With only S2 closed, the voltmeter reads across the starter motor.", "Ohm's law, with the starter motor's resistance."]),
    work("8.3.1", "Switch S1 is now closed and switch S2 is opened. The power dissipated by each headlight is 15 W. Calculate the current passing through L1.", 3, [
        "P = I²R\n15 = I²(12)\nI = 1,12 A",                             # the memo (OPTION 1)
        "P = I²R\n15 = I²(6)\nI = 1,58 A",                              # the two headlights' 6 Ω for ONE headlight (wrong part)
        "P = I²R\n15 = I²(12)\nI = 1,25 A",                             # the square root left out
        "P = I²R\n15 = I²(0,1)\nI = 12,25 A"], 0,                       # the starter motor's 0,1 Ω (the wrong body)
        ["You know each headlight's power and resistance.", "P = I²R."]),
    work("8.3.2", "Switch S1 is now closed and switch S2 is opened. Write down the reading on ammeter A1.", 1, [
        "A1 = {1,12}/{2}\nA1 = 0,56 A",                                 # the current split in half, not added
        "A1 = {V}/{Rp} = {12}/{6}\nA1 = 2,00 A",                        # 8.2's 12 V used here (the wrong part)
        "A1 = (2)(1,12)\nA1 = 2,24 A",                                  # the memo
        "A1 = I(L1)\nA1 = 1,12 A"], 2,                                  # one headlight's current only
        # (the old second clue, "the branch currents add up", with the first gave A1 = 2 x 1,12 A)
        ["Where is A1: before or after the current splits between L1 and L2?", "Trace the current from the battery through A1 to the headlights."],
        after=["8.2", "8.3.1"]),   # the options show 8.3.1's 1,12 A and 8.2's 12 V
    work("8.4", "Calculate the emf of the battery.", 6, [
        "Rs = 12 + 12, so Rs = 24 Ω\nε = I(R + r) = 2,24(24 + r)\nε = I(R + r) = 120(0,1 + r)\n2,24(24 + r) = 120(0,1 + r)\nr = 0,35 Ω\n"
        "ε = 2,24(24 + 0,35) = 54,54 V",                                # the headlights taken in series (wrong formula)
        "{1}/{Rp} = {1}/{12} + {1}/{12}, so Rp = 6 Ω\nε = I(R + r) = 2,24(12 + r)\nε = I(R + r) = 120(0,1 + r)\n2,24(12 + r) = 120(0,1 + r)\n"
        "r = 0,13 Ω\nε = 2,24(12 + 0,13) = 27,17 V",                    # one headlight's 12 Ω with the total current (wrong part)
        "{1}/{Rp} = {1}/{12} + {1}/{12}, so Rp = 6 Ω\nε = V + Ir = 12 + 2,24r\nε = I(R + r) = 120(0,1 + r)\n12 + 2,24r = 120(0,1 + r)\n"
        "r = 0 Ω\nε = 12 + 2,24(0) = 12,00 V",                          # 8.2's 12 V taken as the headlights' voltage (wrong part)
        "{1}/{Rp} = {1}/{12} + {1}/{12}, so Rp = 6 Ω\nε = I(R + r) = 2,24(6 + r)\nε = I(R + r) = 120(0,1 + r)\n2,24(6 + r) = 120(0,1 + r)\n"
        "r = 0,012 Ω\nε = 2,24(6 + 0,012) = 13,47 V"], 3,               # the memo (OPTION 1; its range 13,42 V - 13,47 V)
        ["The emf is the same in both switch settings: ε = I(R + r).", "Write it twice (headlights, 2,24 A; starter motor, 120 A), set them equal and find r first."],
        after=["8.2", "8.3.2"]),   # the options show 8.3.2's 2,24 A and 8.2's 12 V
    rub("8.5", "Both switches are now closed. How will the reading on ammeter A1 be affected? Choose from INCREASES, DECREASES or REMAINS THE SAME. "
        "Explain the answer WITHOUT the use of a calculation.", 5, [
        "Decrease (1).", "The total/external resistance decreases (1).", "The total current increases (1).", "V(internal) increases (1).",
        "The voltage across the light bulbs decreases / V(external) decreases (1)."],
        ["Closing S2 adds the starter motor (0,1 Ω) in parallel.", "Follow the chain: the external resistance, the total current, the lost volts inside the battery, then the headlights."],
        notes=["A calculation given as the explanation: 1/5.",
               "ACCEPT (max 3/5): Increases (1) — the initial reading on A1 = 0 A when switch S1 is open (1); now both switches are closed and current "
               "flows through the circuit (1). The mark for 'increases' only if its explanation is correct."])]

# ---- QUESTION 9, the question paper page 15 and the memo pages 18-19 ----
q9a = [
    rub("9.1", "Define the term rms potential difference.", 2, [
        "The AC potential difference/voltage that produces/dissipates the same amount of energy as an equivalent DC potential difference/voltage. (2)"],
        ["It compares AC with DC.", "Think of the heating effect of each in the same resistor."], each=2,
        notes=["DC written first / energy or heating effect omitted / alternating current defined: 0/2."]),
    term("9.2", "What is the polarity of the magnet at Z?", ["North", "N"],
         # (the old second clue named the north pole)
         ["Use the right-hand rule for generators: the coil's motion and the induced current are shown.",
          "Find the direction the magnetic field must have for this current, then name the pole it leaves."], marks=2),
    work("9.3", "The resistance of the fan is 60 Ω and the maximum potential difference produced by the generator is 311,11 V. Calculate the cost of "
         "operating the fan for 1,5 hours if the cost of electricity is R3,33 per kWh.", 5, [
        "Vrms = Vmax = 311,11 V\nPave = {V²rms}/{R} = {(311,11)²}/{60} = 1 613,16 W = 1,61316 kW\ncost = PΔt × tariff = (1,61316)(1,5)(3,33)\n"
        "cost = R8,06",                                                 # the maximum voltage used as the rms (wrong value)
        "Vrms = {Vmax}/{√2} = {311,11}/{√2} = 219,99 V\nPave = {V²rms}/{R} = {(219,99)²}/{60} = 806,59 W = 0,80659 kW\n"
        "cost = PΔt × tariff = (0,80659)(1,5)(3,33)\ncost = R4,03",     # the memo (OPTION 1)
        "Vrms = {Vmax}/{2} = {311,11}/{2} = 155,56 V\nPave = {V²rms}/{R} = {(155,56)²}/{60} = 403,32 W = 0,40332 kW\n"
        "cost = PΔt × tariff = (0,40332)(1,5)(3,33)\ncost = R2,01",     # divides by 2, not √2 (wrong formula)
        "Vrms = {Vmax}/{√2} = {311,11}/{√2} = 219,99 V\nPave = {V²rms}/{R} = {(219,99)²}/{60} = 806,59 W\n"
        "cost = PΔt × tariff = (806,59)(1,5)(3,33)\ncost = R4 028,92"], 1,   # W not converted to kW
        ["The fan's average power uses the rms voltage.", "Electricity is sold per kWh: kilowatts times hours."])]
q9b = [
    draw("9.4", "Redraw this graph in the ANSWER BOOK and label it as A. On the same set of axes, draw the graph for ONE rotation of the coil when the speed "
         "of rotation is doubled. Label this as graph B.", 3, [
        ["The amplitude of graph B is bigger than that of graph A", 1], ["The period of B is half of A", 1],
        ["Correct shape and one cycle (a cosine graph)", 1]],
        ["Faster rotation: the flux changes faster.", "So a bigger peak voltage AND a shorter period."]),
    term("9.5", "State ONE way in which this generator can be changed to a DC generator.", [
        "By replacing slip rings with split ring commutator", "Replace the slip rings with a split ring commutator", "Replace slip rings with a commutator",
        "Use a split ring commutator", "Split ring", "Commutator"],
         ["What makes this generator AC?", "Swap the part that touches the brushes."])]

# ---- QUESTION 10, the question paper page 16 and the memo page 20 ----
q10a = [
    rub("10.1.1", "Define the term work function.", 2, [
        "Minimum energy needed for the electrons to be emitted from the metal surface. (2)"],
        ["It is an energy, not a frequency.", "It belongs to the metal, not to the light: each metal has its own value."], each=2,
        notes=["Threshold frequency defined: 0/2."]),
    num("10.1.2", "Write down the threshold frequency of zinc.", 1.045e15, 0.001e15, "Hz",
        # (the old second clue, "Read the frequency the learners used.", pointed to the answer by position)
        ["Zinc's electrons leave with zero kinetic energy at this frequency.", "At the threshold frequency a photon's energy just equals the work function."]),
    rub("10.1.3", "How does the work function of sodium compare to that of caesium? Choose from SMALLER THAN, GREATER THAN or EQUAL TO. Explain the answer.", 3, [
        "Greater than (1).", "The maximum kinetic energy of electrons from sodium is smaller (1).",
        "E is constant / the same frequency / the same light used (Ek(max) is smaller, W0 is larger) (1)."],
        ["Use E(photon) = W0 + Ek(max) for each metal.", "Read the table: which metal's electrons leave with less kinetic energy?"]),
    rub("10.1.4", "Light of the same frequency, but with a higher intensity, is now incident on metal M. Will electrons now be ejected? Choose from YES or NO. "
        "Give a reason for the answer.", 2, [
        "No (1).", "The intensity of light does not have any effect on the ejection of electrons for metal M (1), OR the frequency of light has not changed / "
        "the energy of a photon has not changed (1)."],
        ["Metal M emitted no electrons at this frequency.", "What does a higher intensity change: the number of photons or the energy of each photon?"])]
q10b = [
    work("10.2.1", "An electron of this atom moves from E3 to E1. Photon X is emitted. Calculate the frequency of photon X.", 4, [
        "E = hf\n5,7 × 10⁻¹⁹ − 1,3 × 10⁻¹⁹ = (6,63 × 10⁻³⁴)f\nf = 6,64 × 10¹⁴ Hz",              # the memo (OPTION 1)
        "E = hcf\n5,7 × 10⁻¹⁹ − 1,3 × 10⁻¹⁹ = (6,63 × 10⁻³⁴)(3 × 10⁸)f\nf = 2,21 × 10⁶ Hz",   # E = hf mixed with E = hc/λ (wrong formula)
        "E = hf\n5,7 × 10⁻¹⁹ − 5,1 × 10⁻¹⁹ = (6,63 × 10⁻³⁴)f\nf = 9,05 × 10¹³ Hz",              # E3 − E2, the wrong levels (wrong value)
        "E = hf\n5,7 × 10⁻¹⁹ + 1,3 × 10⁻¹⁹ = (6,63 × 10⁻³⁴)f\nf = 1,06 × 10¹⁵ Hz"], 0,         # the energies added (sign)
        # (the old second clue wrote the right working's formula, E = hf)
        ["The photon carries away the energy the electron loses.", "Which equation links a photon's energy to its frequency? Take h from the data sheet."]),
    rub("10.2.2", "Is it possible for a photon with an energy of 2,5 x 10⁻¹⁹ J to be emitted from this atom? Choose from YES or NO. Give a reason for the answer.", 2, [
        "No (1).", "The energy does not correspond to any transition in this atom (1)."],
        ["List the possible jumps: E3 − E2, E3 − E1, E2 − E1.", "Does any of them equal 2,5 × 10⁻¹⁹ J?"])]

V_TABLE = {"head": ["TIME (s)", "MAGNITUDE OF VELOCITY (m·s⁻¹)"], "rows": [["0", "15"], ["p", "0"], ["3,36", "q"]]}
M_TABLE = {"head": ["METALS", "ELECTRONS EMITTED", "MAXIMUM KINETIC ENERGY (J)"],
           "rows": [["Zinc", "Yes", "0"], ["Sodium", "Yes", "2,53 × 10⁻¹⁹"], ["Caesium", "Yes", "3,50 × 10⁻¹⁹"], ["Metal M", "No", "–"]]}
missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions. Each question has only ONE correct answer.", "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Newton's laws and friction", "marks": 17,
     "lead": "A block of mass 5 kg is at rest on a rough horizontal surface. When a constant force F of magnitude 18 N acts on the block at an angle θ to "
             "the horizontal, the block experiences maximum static friction. See the diagram below.",
     "figure": fig("Q2", "A 5 kg block on a horizontal surface; F = 18 N pulls up and to the right at angle θ above the horizontal."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Vertical projectile motion", "marks": 15,
     "lead": "A ball is projected vertically upwards from the top of a building that is 5 m high. Ignore the effects of friction. The table below shows the "
             "magnitude of the velocity of the ball at THREE different times during its motion.",
     "table": V_TABLE, "figure": fig("Q3", "A building 5 m high; a ball on its top edge with an arrow pointing straight up."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Momentum and impulse", "marks": 11,
     "lead": "Cricketers at an academy conduct an experiment to determine the relationship between the contact time and the final momentum of a ball for "
             "a constant average net force. A cricket ball of mass 150 g is thrown horizontally with a certain initial velocity and is struck by a bat "
             "so that the ball moves in the opposite direction. The average net force acting on the ball is horizontal.\n\nThe experiment is repeated "
             "using the same ball. The average net force and the initial velocity of the ball are kept constant. The contact time between the bat and "
             "the ball is changed EACH time. The results obtained are shown in the sketch graph below.",
     "figure": fig("Q4", "A sketch graph of final momentum pf (kg·m·s⁻¹) up against contact time Δt (s) across: a straight line through (0,01; 0) "
                   "and (0,03; 4,5), extended as a dashed line back to a negative value on the momentum axis. (The paper's diagram above it shows "
                   "the ball arriving at the bat with velocity vi to the left and leaving with vf to the right.)"), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Work, energy and power", "marks": 13,
     "lead": "A crate of mass 3 kg is at rest at point A on a frictionless horizontal surface. A constant horizontal force F of 12 N acts on the crate and "
             "moves it from point A to point B. The crate then moves down a rough plane, inclined at 20° to the horizontal. The distance from point A to "
             "point B is 7 m and from point B to point C is 6,8 m, as shown in the diagram below.",
     "figure": fig("Q5", "A 3 kg crate at A on a horizontal surface pulled by F = 12 N to the right; 7 m from A to B; from B a slope runs down at "
                   "20° to the ground, 6,8 m from B to C."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "The Doppler effect", "marks": 12,
     "lead": "An investigation is performed to determine the relationship between the velocity of a moving sound source and the frequency of the sound "
             "detected. The siren of an ambulance produces sound with a constant frequency. The ambulance, with its siren on, moves towards a stationary "
             "sound detector (Part A) and away from the stationary sound detector (Part B) at constant velocities. The experiment is repeated for "
             "different velocities of the ambulance. The detected frequency is measured for EACH velocity. The results obtained are shown in the graph below.",
     # (the caption no longer names the falling line as Part B's: the paper does not label the lines, and that was 6.3's conclusion)
     "figure": fig("Q6", "Detected frequency (Hz) up against velocity of the ambulance (m·s⁻¹) across, 0 to 30. Two straight lines, not labelled, "
                   "start at the same frequency on the axis: one rises to 1 298 Hz at 25 m·s⁻¹; the other falls to 1 115 Hz at 25 m·s⁻¹."), "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Electrostatics", "marks": 7,
     "lead": "A sphere X is placed at point A on a horizontal surface. X carries a charge of +3 x 10⁻⁷ C. Point P is r metres to the left of point A. The "
             "magnitude of the electric field at point P is 1,08 x 10⁶ N·C⁻¹.",
     "figure": fig("Q7a", "Sphere X at point A on a horizontal surface; point P is r metres to its left."), "items": q7a},
    {"id": "7.4", "title": "Question 7.4", "kind": "Electrostatic forces", "marks": 8,
     "lead": "Sphere Y, carrying a charge of −5 x 10⁻⁷ C, is now fixed at point P and sphere Z, carrying a charge of −4 x 10⁻⁷ C, is fixed 0,04 m to the "
             "right of sphere X.",
     "figure": fig("Q7b", "Spheres in a line: Y (−5 x 10⁻⁷ C) at P, then r to X (+3 x 10⁻⁷ C) at A, then 0,04 m to Z (−4 x 10⁻⁷ C)."), "items": q7b},
    {"id": "8", "title": "Question 8", "kind": "Electric circuits", "marks": 20,
     "lead": "Two identical headlights, L1 and L2, and a starter motor, M, of a car are connected to a battery, as shown in the circuit diagram below. The "
             "resistance of each headlight is 12 Ω, while the resistance of the starter motor is 0,1 Ω. The emf (ε) and internal resistance (r) of the "
             "battery are unknown. The ammeters and the connecting wires have negligible resistance, while the voltmeter has a high resistance. Switches "
             "S1 and S2 are initially open.",
     "figure": fig("Q8", "Headlights L1 and L2 (12 Ω each) in parallel on the left, joined through switch S1; in the middle the battery (emf ε with "
                   "internal resistance r) with ammeter A1 on its left branch and A2 on its right; a voltmeter V across the battery; the starter motor "
                   "M (0,1 Ω) on the right, joined through switch S2."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "AC generators", "marks": 9,
     "lead": "An AC generator operates a fan. The directions of the rotation of the coil and the induced current are shown in the simplified diagram below.",
     "figure": fig("Q9a", "A coil between two magnet poles (the right pole marked Z) turning as the curved arrow shows, with an arrow along the coil for "
                   "the induced current; slip rings and brushes connect it to a voltmeter V and a fan."), "items": q9a},
    {"id": "9.4", "title": "Question 9.4", "kind": "Generator output", "marks": 4, "lead": "The voltage versus time graph for this generator is given below.",
     "figure": fig("Q9b", "Voltage (V) against time (s): a cosine curve starting at its maximum, falling to its minimum and rising back to the maximum "
                   "at 4 s (one full rotation)."), "items": q9b},
    {"id": "10.1", "title": "Question 10.1", "kind": "The photoelectric effect", "marks": 8,
     "lead": "Learners conduct an experiment to determine whether electrons will be emitted from the surface of different metals when light with a single "
             "frequency is incident on the metal. The maximum kinetic energy of emitted electrons are measured when light of frequency 1,045 × 10¹⁵ Hz "
             "is used. The results obtained are shown in the table below.", "table": M_TABLE, "items": q10a},
    {"id": "10.2", "title": "Question 10.2", "kind": "Atomic spectra", "marks": 6,
     "lead": "The energy diagram below (NOT drawn to scale) shows the electron energies in different energy levels, E1, E2 and E3, of a certain atom.",
     "figure": fig("Q10b", "Three horizontal energy levels: E3 = 5,7 x 10⁻¹⁹ J at the top, E2 = 5,1 x 10⁻¹⁹ J, and E1 = 1,3 x 10⁻¹⁹ J at the bottom; "
                   "an arrow points down from E3 to E1."), "items": q10b},
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
    random.Random("ps-p1-2025-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    # 2 or 0, either OR form: the wrong ones drop "net", swap the proportions, or are the first and third laws
    "2.1": (2, ["When a net (resultant) force acts on an object, the object accelerates in the direction of the net force with an acceleration "
                "directly proportional to the net force and inversely proportional to the mass of the object.",
                "The net (resultant) force acting on an object is equal to the rate of change of momentum of the object."],
               ["When a force acts on an object, the object accelerates in the direction of that force, whatever other forces act on it.",
                "When a net force acts on an object, the object accelerates in the direction of the net force with an acceleration inversely "
                "proportional to the net force and directly proportional to the mass of the object.",
                "An object continues in its state of rest or of uniform motion unless a non-zero net force acts on it.",
                "When object A exerts a force on object B, object B simultaneously exerts a force of equal magnitude in the opposite direction on object A."]),
    # the memo's FIRST answer (Increases) and its three ticks, 1 each. The memo also accepts "Decreases" (the block moves: fk < fs(max))
    # and "Remains the same" (with a calculation): those cannot be cards beside "Increases" (a learner could pick both), so they are
    # left out, and no wrong card is true in them (the horizontal component DOES grow: not a wrong card)
    "2.4": (1, ["The friction acting on the block increases.", "The vertical component of F decreases.", "The normal force on the block increases.",
                "μs remains constant, and fs(max) is directly proportional to the normal force."],
               ["The vertical component of F increases.", "The normal force on the block decreases.",
                "The coefficient of static friction increases when θ decreases.",
                "The maximum static friction does not depend on the normal force."]),   # (a 4th wrong card: with seven the seeded
                # shuffle put the four right cards first, an answer by position)
    # 2 or 0 ("a projectile defined: 0/2"); the wrong ones add air resistance, a constant velocity, a net force of zero, downward motion only
    "3.1": (2, ["Motion under the influence of the gravitational force (weight) only."],
               ["Motion under the influence of the gravitational force and air resistance.", "Motion at a constant velocity under the influence of gravity.",
                "Motion in which the net force acting on the object is zero.", "Motion of an object downwards only, after it is dropped from rest."]),
    # 3 ticks: the choice, the height, kinetic energy (its "/" forms one reading: not conserved)
    "3.4": (1, ["The collision is inelastic.", "The ball bounces to a smaller height than it reached before the bounce.",
                "Kinetic energy is not conserved in the collision."],
               ["The collision is elastic.", "Kinetic energy is conserved in the collision.",
                "The ball leaves the ground with a greater speed than it strikes the ground.", "The ball gains mechanical energy when it strikes the ground."]),
    # 2, either OR form: the wrong ones are momentum, the net force (rate of change of momentum), work and acceleration
    "4.1": (2, ["The product of the resultant (net) force acting on an object and the time the resultant force acts on the object.",
                "The product of the resultant (net) force and the contact time."],
               ["The product of the mass of an object and its velocity.", "The rate of change of momentum of an object.",
                "The product of the resultant force acting on an object and the distance through which the object moves.",
                "The change in the velocity of an object divided by the time taken."]),
    # 2, either OR form: the wrong ones drop "net", swap kinetic for potential energy, or are another law's wording
    "5.1": (2, ["The net (total) work done on an object is equal to the change in the object's kinetic energy.",
                "The work done on an object by a resultant (net) force is equal to the change in the object's kinetic energy."],
               ["The work done on an object by a force is equal to the change in the object's kinetic energy, whatever other forces act on it.",
                "The net work done on an object is equal to the change in the object's potential energy.",
                "The total mechanical energy in an isolated system remains constant.",
                "The net work done on an object is equal to the rate of change of the object's momentum."]),
    # 2, either OR form: the wrong ones change the emitted frequency, the speed of sound or the loudness, or have no relative motion
    "6.1": (2, ["The change in frequency (or pitch) of the sound detected by a listener because the sound source and the listener have different "
                "velocities relative to the medium of sound propagation.",
                "An apparent change in the observed frequency (pitch) as a result of the relative motion between a sound source and an observer."],
               ["A change in the frequency of the sound that the source itself produces as the source moves.",
                "The change in the speed of sound detected by a listener because the source and the listener move relative to each other.",
                "The change in the loudness of a sound as its source moves closer to a listener.",
                "The change in the frequency detected by a listener when the source and the listener move with the same velocity."]),
    # 2, one statement ("inversely proportional indicated: 0/2"); the wrong ones are Part A's trend, no trend, the siren's own frequency
    "6.3": (2, ["As the velocity of the ambulance increases, the detected frequency decreases."],
               ["As the velocity of the ambulance increases, the detected frequency increases.",
                "The detected frequency is inversely proportional to the velocity of the ambulance.",
                "The detected frequency stays the same for every velocity of the ambulance.",
                "As the velocity of the ambulance increases, the frequency of the sound produced by the siren decreases."]),
    # 2 or 0: the wrong ones are a gravitational field, no force, current, potential difference
    "7.1": (2, ["A region of space in which an electric charge experiences a force."],
               ["A region of space in which a mass experiences a force.", "A region of space in which an electric charge experiences no force.",
                "The rate of flow of electric charge in a conductor.", "The energy transferred per unit charge between two points in a circuit."]),
    # 2 or 0: the wrong ones are current, power, stored charge, the terminal potential difference
    "8.1": (2, ["The maximum energy provided by a battery per coulomb of charge passing through it."],
               ["The rate of flow of charge through a battery.", "The energy provided by a battery per second.",
                "The total charge that a battery can store.", "The potential difference across the terminals of a battery while a current flows through it."]),
    # 5 ticks: the choice and the memo's chain. Its ACCEPT ("Increases", max 3/5, from 8.2's open S1) is not a card either way
    "8.5": (1, ["The reading on ammeter A1 decreases.", "The total (external) resistance of the circuit decreases.",
                "The total current from the battery increases.", "The potential difference across the internal resistance (V internal) increases.",
                "The potential difference across the headlights (V external) decreases."],
               ["The reading on ammeter A1 remains the same.", "The total (external) resistance of the circuit increases.",
                "The potential difference across the internal resistance (V internal) decreases."]),
    # 2 ("DC written first / energy omitted / AC defined: 0/2"): the wrong ones are DC first, the peak, the average, half the energy
    "9.1": (2, ["The AC potential difference that dissipates the same amount of energy as an equivalent DC potential difference."],
               ["The DC potential difference that dissipates the same amount of energy as an equivalent AC potential difference.",
                "The maximum (peak) value of an AC potential difference.", "The average value of an AC potential difference over one complete cycle.",
                "The AC potential difference that dissipates half the energy of an equivalent DC potential difference."]),
    # 2 ("threshold frequency defined: 0/2"): the wrong ones are the threshold frequency, the maximum kinetic energy, a photon's energy, intensity
    "10.1.1": (2, ["The minimum energy needed for electrons to be emitted from the surface of a metal."],
                  ["The minimum frequency of light needed for electrons to be emitted from the surface of a metal.",
                   "The maximum kinetic energy of the electrons emitted from the surface of a metal.",
                   "The energy of each photon of the light shining on the metal.",
                   "The minimum intensity of light needed for electrons to be emitted from the surface of a metal."]),
    # 3 ticks: the choice, the smaller Ek(max), the same light
    "10.1.3": (1, ["The work function of sodium is greater than that of caesium.", "The maximum kinetic energy of the electrons emitted from sodium is smaller.",
                   "The same frequency of light is used, so each photon has the same energy for both metals."],
                  ["The work function of sodium is smaller than that of caesium.", "The work function of sodium is equal to that of caesium.",
                   "The maximum kinetic energy of the electrons emitted from sodium is greater.", "Sodium is lit with light of a higher frequency than caesium."]),
    # 2 ticks: the choice and the memo's first reason (its OR form, "the frequency has not changed", is true: not a wrong card)
    "10.1.4": (1, ["No, electrons will not be ejected.", "The intensity of light does not have any effect on the ejection of electrons for metal M."],
                  ["Yes, electrons will now be ejected.", "A higher intensity gives each photon more energy.",
                   "A higher intensity increases the frequency of the light.", "Any metal emits electrons if the light is bright enough."]),
    # 2 ticks: the choice and the reason; the wrong ones misread the gaps (E3 − E2 = 0,6, E2 − E1 = 3,8 x 10⁻¹⁹ J)
    "10.2.2": (1, ["No, such a photon cannot be emitted.", "The energy 2,5 × 10⁻¹⁹ J does not correspond to any transition in this atom."],
                  ["Yes, such a photon can be emitted.", "2,5 × 10⁻¹⁹ J is the energy difference between E3 and E2.",
                   "2,5 × 10⁻¹⁹ J is the energy difference between E2 and E1.", "An atom can emit a photon of any energy smaller than E3 − E1."]),
}
# A memo that weighs two sides (advantages / disadvantages, for / against) would play as a SORT; none in this paper does (its written
# parts are definitions, laws, a conclusion and choices with reasons), so SORTS stays empty and sort_ is kept for parity.
SORTS = {}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("ps-p1-2025-11:sort:" + n).shuffle(order)
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
assert not [i["n"] for m in missions for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"

# every part that played as typed steps (and 8.3.2's num with a working) before 2026-10-10, now authored multiple choice
assert tuple(AUTHORED) == ("2.3.1", "2.3.2", "3.2", "3.3", "4.2.1", "4.2.2", "5.2", "5.4", "6.4", "7.3", "7.4", "8.2", "8.3.1", "8.3.2", "8.4",
                           "9.3", "10.2.1"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["10.1.2"], "only the read-off stays a typed number"
assert {i["n"]: i.get("after") for i in ITEMS if i.get("after")} == {
    "2.3.2": ["2.3.1"], "3.5": ["3.2", "3.3"], "4.2.2": ["4.2.1"], "5.4": ["5.2"], "6.4": ["6.3"], "8.3.2": ["8.2", "8.3.1"], "8.4": ["8.2", "8.3.2"]}
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
PICKS = [i["n"] for i in ITEMS if i["t"] == "pickn"]

FZ_IDS = ["Fg", "FN", "f", "FA", "T", "FE", "Fnet"]   # the force builder's tray (build-play.js FZ), the same for every question


def forces_ok(i):
    """A built force diagram: every force one of the tray's seven, every criterion earned by exactly one force (or the angle), one mark
    each, so the marks add up to the part's."""
    b = i["build"]
    assert all(f["id"] in FZ_IDS for f in b["forces"]) and all(x in FZ_IDS for x in b.get("free", [])), (i["n"], "a force outside the tray")
    crits = [f["crit"] for f in b["forces"]] + ([b["angle"]["crit"]] if "angle" in b else [])
    assert sorted(crits) == list(range(len(i["criteria"]))), (i["n"], "every criterion earned by one force or the angle")
    assert all(c["marks"] == 1 for c in i["criteria"]) and len(i["criteria"]) == i["marks"], (i["n"], "one mark a criterion")


FORCES = [i["n"] for i in ITEMS if (i.get("build") or {}).get("kind") == "forces"]
assert FORCES == ["2.2", "5.3"], FORCES
for _i in ITEMS:
    if _i["n"] in FORCES:
        forces_ok(_i)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every calculation plays as the memo's FIRST "
                                                       "working plus three built from realistic physics errors (a sign or direction slip, g used "
                                                       "wrongly or left out, a unit not converted, the wrong formula, a value from the wrong body or "
                                                       "part), 0 or full marks: " + ", ".join(AUTHORED) + " (%d parts, %d marks). 8.3.2 (a 'Write "
                                                       "down' whose memo shows A1 = (1,12)(2)) is one of them; 10.1.2 (a read-off) stays a typed "
                                                       "number. A value the memo's ranges accept is never a wrong option (3.3: 17,93 - 18,33 m·s⁻¹; "
                                                       "8.4: 13,42 - 13,47 V)." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "7.3", "kind": "no_fit", "detail": "'Show that r = 0,05 m': all four workings end at the given 0,05 m, as learners write it; only the "
                                                 "memo's substitution gets there (the others: 10⁻⁷ written 10⁷, G for k, r not squared). 5.4 and 7.4 "
                                                 "(decide by calculation) end in the memo's conclusion; 7.4's wrong workings also conclude 'No', so "
                                                 "the working decides, not the conclusion."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 10), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (formulas are images); no API call."},
        {"n": PICKS[0], "kind": "no_fit", "detail": "The written answers play as statements (%d parts): the definitions and laws (2.1, 3.1, 4.1, 5.1, "
                                                    "6.1, 7.1, 8.1, 9.1, 10.1.1) and the conclusion 6.3 pick one card for 2 marks (an OR form is a "
                                                    "second right card); the choices with reasons (2.4, 3.4, 8.5, 10.1.3, 10.1.4, 10.2.2) pick the "
                                                    "choice and the memo's points, 1 mark each. 2.4's memo also accepts 'Decreases' (fk < fs(max)) "
                                                    "and 'Remains the same' (with a calculation): only its first answer plays (two choices side by "
                                                    "side could both be picked), and no wrong card is true under the others. 8.5's ACCEPT "
                                                    "('Increases', max 3/5) and 10.1.4's OR reason are neither right nor wrong cards. The "
                                                    "choice stays a card beside its reasons rather than a multiple choice of its own: each "
                                                    "is ONE printed part (one number, the player's key), and a separate choice would mark "
                                                    "2.4's and 8.5's memo-accepted choices wrong."
                                                    % len(PICKS)},
        {"n": "2.2", "kind": "no_fit", "detail": "The free-body diagrams 2.2 and 5.3 are BUILT (2026-10-11, build 'forces'): the learner aims "
                                                 "each force from a dot, from the same tray of seven forces, one mark a force for its label AND "
                                                 "direction (within 10°; 2.2's F within 14° of 34°, as θ is found only in 2.3.1 and the figure "
                                                 "draws it at about 26°), −1 for each additional force, never below 0 (the memo's 'max 3/4' and "
                                                 "'max 2/3' for one extra). The tray's friction is f, which the memo accepts (fk, which 2.2's "
                                                 "memo does not accept, is never offered). 'No arrows' and 'not touching the dot' cannot happen "
                                                 "on screen. The other drawings (3.5, 4.3, 7.2, 9.4) are done on paper and self-checked against "
                                                 "the memo's criteria."},
        {"n": "8.4", "kind": "memo_issue", "detail": "The memo writes ε = 2,24(6 + 0,012) = 13,46 V; it is 13,47 V (2,24 × 6,012 = 13,467), inside its "
                                                     "own range (13,42 V - 13,47 V): the right option shows 13,47 V."},
        {"n": "6.4", "kind": "memo_issue", "detail": "The memo's OR route 1,164(v − 25) = v + 25 gives 329,88 m·s⁻¹, not its 329,64 m·s⁻¹ (the ratio "
                                                     "1298/1115 rounded to 1,164); the right option follows its first route, (1) = (2)."},
    ],
}
QTOTAL = {"1": 20, "2": 17, "3": 15, "4": 11, "5": 13, "6": 12, "7": 15, "8": 20, "9": 13, "10": 14}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
# the right letter, spread evenly over A-D across the paper (Question 1 and 7.5's three-way choice included)
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
# and across the calculations alone: Question 1's letters are the paper's (A1 B3 C4 D2, 7.5 B), so an even paper leaves the 17
# workings at A6 B3 C3 D5; every letter is right at least 3 times, never more than 6
wspread = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert min(wspread.values()) >= 3 and max(wspread.values()) <= 6, wspread
print("right options, the paper:", spread, "authored:", wspread)
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; statements:", len(PICKS), "parts")
print("total:", total)
out = Path(__file__).parent / "out" / "ps-p1-2025-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
