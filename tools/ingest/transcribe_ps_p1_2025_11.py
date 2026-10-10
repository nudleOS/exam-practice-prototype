"""Physical Sciences P1 (Physics) Nov 2025, the whole paper (Questions 1 to 10), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets formulas and symbols as
images, so its text layer has gaps.

  python tools/ingest/transcribe_ps_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P1 Nov 2025 Eng.pdf" "<...>/Physical Sciences P1 Nov 2025 MG Afr & Eng.pdf" --id ps-p1-2025-11 --from-json

How the memo's shapes map (Physical Sciences):
  multiple choice -> mcq (graph options: the figure, options "Graph A".."Graph D"; options printed as a table -> optTable);
  a definition/law/statement -> rubric (its key words); "Calculate" -> steps, each step ONE number the method produces (a unit in
  the label's brackets), the memo's formula and substitution marks riding on the number they lead to (the phone sees the number,
  not the working); a memo RANGE -> its centre with a tolerance covering it; one read-off number -> num; "Choose ... Explain"
  -> rubric (a choice cannot be marked as a number); "Show that" -> rubric when the memo marks words, steps on the numbers
  before the given answer when it marks a formula and its substitutions (7.3); a 3-way choice with no explanation -> mcq;
  "Draw / Sketch / Redraw" -> draw with the memo's criteria (self-checked, flagged no_fit). A mission is a question with its stem
  and diagram; a question whose diagram changes part-way is two missions (7, 9, 10).
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves and checked on a contact sheet."""
import json
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


def mcq(n, q, opts, a, clues, **kw):
    return {"t": "mcq", "n": n, "marks": 2, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points (key words, "... defined: 0/2", ACCEPT limits): never scored, never shown
rub = lambda n, q, marks, bullets, clues, each=None, notes=None: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets,
                                                                 **({"each": each} if each else {}), **({"notes": notes} if notes else {})}
term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


# ---- QUESTION 1: multiple choice, the question paper pages 3-7 and the memo page 2 ----
q1 = [
    mcq("1.1", "The net force acting on an object on a horizontal surface is always …",
        ["in the direction of motion of the object.", "in the direction of acceleration of the object.",
         "zero when the object moves at constant acceleration.", "increasing when the object moves at constant acceleration."], 1,
        ["Newton's second law links the net force to one quantity's direction.", "An object can move one way while slowing down."]),
    mcq("1.2", "A hot-air balloon is moving upwards at a constant velocity. A small stone is dropped from THE BALLOON. Which ONE of the following "
        "graphs represents the motions of the balloon and the stone? Ignore the effects of friction on the stone.",
        ["Graph A", "Graph B", "Graph C", "Graph D"], 1,
        ["At the moment it is dropped, the stone has the balloon's velocity.", "Then only gravity acts on it: its velocity falls steadily, through zero."],
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
        ["p = mv, and p is the same for both.", "Half the mass needs ... the velocity."],
        figure=fig("1.4", "Two boxes on a horizontal surface: a smaller box P on the left and a larger box Q on the right.")),
    mcq("1.5", "A block moves along a rough horizontal surface while a horizontal force F of magnitude 18 N and a constant kinetic frictional force of "
        "magnitude 6 N act on it. Which ONE of the following combinations of ACCELERATION and NET WORK DONE ON THE BLOCK is CORRECT?",
        ["Constant; increases", "Increases; constant", "Increases; increases", "Constant; constant"], 0,
        ["Both forces are constant, so the net force is ...", "Net work = net force x distance, and the distance keeps growing."],
        optTable={"head": ["ACCELERATION", "NET WORK DONE ON THE BLOCK"],
                  "rows": [["Constant", "Increases"], ["Increases", "Constant"], ["Increases", "Increases"], ["Constant", "Constant"]]},
        figure=fig("1.5", "A block on a horizontal surface: F = 18 N pulls it to the right, fk = 6 N acts to the left.")),
    mcq("1.6", "A star's spectrum, observed from Earth, is red shifted. Which ONE of the following statements is CORRECT?",
        ["The speed of light is increasing.", "The star is moving towards Earth.", "The frequency of each spectral line has increased.",
         "The wavelength of each spectral line has increased."], 3,
        ["Red light has the longest wavelengths of visible light.", "Red shift: the source moves away, and the lines move towards red."]),
    mcq("1.7", "Three point charges, Q1, Q2 and Q3, are fixed in a straight line. Q1 is r metres from Q2, while Q3 is 2r metres from Q2. The magnitude "
        "of the charge on Q2 is q. The net electrostatic force on charge Q1 is zero. What is the magnitude of charge Q3 in terms of q?",
        ["⅑q", "⅓q", "3q", "9q"], 3,
        ["Q3 is 3r from Q1, Q2 is r from Q1.", "The two forces on Q1 are equal: kQ3/(3r)² = kq/r²."],
        figure=fig("1.7", "Charges Q1, Q2 and Q3 on a dashed line: r between Q1 and Q2, 2r between Q2 and Q3.")),
    mcq("1.8", "Three identical light bulbs, X, Y and Z, are connected in a circuit, as shown in the diagram below. Switch S is initially closed. "
        "Ignore the internal resistance of the battery. Switch S is now opened. How will the brightness of bulbs X and Y be affected?",
        ["Increases; decreases", "Decreases; increases", "Increases; increases", "Decreases; decreases"], 1,
        ["Opening S removes Z: the total resistance goes up.", "Less total current through X; more of the battery's voltage across Y."],
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
        ["Ek(max) = hc/λ − W0: a straight line against 1/λ.", "Below the threshold no electrons are emitted, so the line starts on the axis."],
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
        memo="A mark for each label AND its arrow; fk not accepted as a label. Any additional force(s), everything correct but no arrows, or forces "
             "not touching the dot: max 3/4."),
    steps("2.3.1", "The horizontal component of force F is 15 N. Calculate θ.", 2,
          [("Angle θ (degrees)", 2, 33.56, 0.1, "Fx = F cos θ; 15 = 18 cos θ ✓; θ = 33,56° ✓ (OR 9,95 = 15 tan θ, OR 9,95 = 18 sin θ). Answer only: 1/2.")],
          ["You know F and its horizontal component.", "cos θ = Fx / F."]),
    steps("2.3.2", "The horizontal component of force F is 15 N. Calculate the coefficient of static friction.", 5, [
        ("Vertical component of F (N)", 1, 9.95, 0.05, "Fy = 18 sin 33,56° = 9,95 N, OR Fy = √(18² − 15²) = 9,95 N ✓"),
        ("Normal force on the block (N)", 1, 39.05, 0.1, "FN + Fy − Fg = 0; FN = (5)(9,8) − 9,95 ✓ = 39,05 N"),
        ("Coefficient of static friction", 3, 0.38, 0.01, "fs(max) = μs N ✓; 15 ✓ = μs(39,05); μs = 0,38 ✓ (N not calculated: 3/5)")],
        ["The block is at rest with MAXIMUM static friction: friction equals the horizontal pull.", "F's vertical part lifts the block, so N is less than mg."]),
    rub("2.4", "Angle θ is decreased while the magnitude of force F remains constant. How will the friction acting on the block be affected? Choose from "
        "INCREASES, DECREASES or REMAINS THE SAME. Explain the answer.", 4, [
        # the memo's four ticks a point each (2026-10-10): one 4-mark point per answer gave "Increases because the normal force increases" 4 / 4
        "Increases (1)", "The vertical component of F decreases (1)", "The normal force increases (1)",
        "μs remains constant, so fs(max) increases: it is directly proportional to the normal force (1)",
        "OR — Decreases (1)", "The horizontal component of F increases (1)", "The block will move / Fnet will increase (1)",
        "The kinetic friction is less than the maximum static friction (fk < fs(max)) (1)",
        "OR — Remains the same (1)", "A relevant calculation (1)", "choosing μk smaller than μs (1)", "and θ that together with μk gives fk = 15 N (1)"],
        ["A smaller angle means a bigger horizontal part and a smaller vertical part of F.", "Friction depends on the normal force, and on whether the block starts to slide."]),
]

# ---- QUESTION 3, the question paper page 9 and the memo pages 5-9 ----
q3 = [
    rub("3.1", "Define the term free fall.", 2, [
        "Motion under the influence of weight/gravitational force only. (2 or 0)"],
        ["Which force is the ONLY one acting?", "Free fall: motion under the influence of ... only."], each=2, notes=["A projectile defined: 0/2."]),
    steps("3.2", "Using EQUATIONS OF MOTION ONLY, calculate the value of p.", 3,
          [("Time p (s)", 3, 1.53, 0.01, "vf = vi + aΔt ✓; 0 = 15 + (−9,8)Δt ✓ (upwards positive); Δt = 1,53 s ✓. Energy principles used: 1/3.")],
          ["At time p the velocity is 0: the top of the flight.", "vf = vi + aΔt with a = −9,8 m·s⁻² (upwards positive)."]),
    steps("3.3", "The ball strikes the ground 3,36 seconds after it was thrown upwards. Calculate q.", 3,
          [("Magnitude of velocity q (m·s⁻¹)", 3, 18.13, 0.2, "vf² = vi² + 2aΔy ✓; vf² = (15)² + 2(−9,8)(−5) ✓; vf = 17,97 m·s⁻¹ ✓ "
            "(OR vf = vi + aΔt = 15 + (−9,8)(3,36) = 17,93 m·s⁻¹). Range: 17,93 – 18,33.")],
          ["q is the speed when the ball hits the ground, 5 m below where it started.", "vf² = vi² + 2aΔy, or vf = vi + aΔt with Δt = 3,36 s."]),
    rub("3.4", "The ball bounces to a maximum height of 3 m after it struck the ground. Is the collision with the ground ELASTIC or INELASTIC? Explain "
        "the answer WITHOUT the use of calculations.", 3, [
        "Inelastic. (1)", "The height decreased/smaller. (1)",
        "The velocity with which the ball strikes the ground is not the same as the velocity with which it left the ground / kinetic energy is "
        "converted to heat and sound energy / kinetic energy is NOT conserved / the kinetic energy is not the same before and after the ball strikes "
        "the ground. ACCEPT: kinetic energy is lost. (1)"],
        ["Compare the heights: 5 m below the top before, 3 m after.", "Elastic means kinetic energy is conserved."],
        notes=["Do NOT accept any calculation as an explanation."]),
    draw("3.5", "Sketch a velocity versus time graph for the motion of the ball from the time it was projected until it reached the maximum height after "
         "it bounced. Show the following NUMERICAL VALUES on the graph: the initial velocity; time p; velocity q.", 4, [
        ["A straight line starting at v = 15 m·s⁻¹ with negative final velocity (or starting at −15 m·s⁻¹ with positive final velocity)", 1],
        ["The straight line cuts the time axis at the time calculated in 3.2 (1,53 s)", 1],
        ["The correct velocity calculated in 3.3 (17,97 m·s⁻¹) where the ball is on the ground", 1],
        ["The velocity of the second line is less than in 3.3; the lines are parallel and it ends at v = 0", 1]],
        ["One straight line until the bounce, then a second, parallel one.", "Mark 15, 1,53 and your q on the axes."],
        memo="Positive marking from 3.2 and 3.3. Accept if no contact time is shown on the graph.")]

# ---- QUESTION 4, the question paper page 10 and the memo pages 9-10 ----
q4 = [
    rub("4.1", "Define the term impulse.", 2, [
        "The product of the resultant/net force acting on an object and the time the (net) force acts on the object. (2)",
        "OR — The product of the resultant/net force and the contact time. (2)"],
        ["Impulse = force x ...", "Which force, and which time?"], each=2, notes=["Key words: product; resultant/net force; time. A key word omitted: deduct 1."]),
    steps("4.2.1", "Calculate the average net force acting on the ball.", 3,
          [("Average net force on the ball (N)", 3, 225, 1, "Gradient: Fnet = Δp/Δt = (4,5 − 0)/(0,03 − 0,01) ✓✓ = 225 N to the right/opposite to the original "
            "direction of the ball ✓ (OR Fnet(0,01) = 0 − pi and Fnet(0,03) = 4,5 − pi).")],
          ["The graph's gradient is the change in momentum over the change in time.", "Use the two points where the line is known: (0,01; 0) and (0,03; 4,5)."]),
    steps("4.2.2", "Calculate the magnitude of the initial velocity of the ball.", 4,
          [("Magnitude of the initial velocity (m·s⁻¹)", 4, 15, 0.1, "FnetΔt = Δp = mvf − mvi ✓ (any one); (225)(0,03) ✓ = 4,5 − (0,15)vi ✓; vi = −15 m·s⁻¹; "
            "vi = 15 m·s⁻¹ ✓ (positive marking from 4.2.1)")],
          ["Impulse = change in momentum, with the mass in kg (150 g).", "The ball comes in one way and leaves the other: watch the signs."]),
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
    steps("5.2", "Using ENERGY PRINCIPLES ONLY, calculate the kinetic energy of the crate at point B.", 3,
          [("Kinetic energy of the crate at B (J)", 3, 84, 0.5, "Wnet = ΔEk / FAΔx cos θ = ½mvf² − ½mvi² ✓ (any one); (12)(7) cos 0° = Ekf − 0 ✓; Ekf = 84 J ✓")],
          ["From A to B the surface is frictionless: F does all the work.", "Work = F Δx cos θ, and the crate starts at rest."]),
    draw("5.3", "Force F is removed when the crate reaches point B. The crate then experiences a constant frictional force of 21 N as it moves down the "
         "incline. Draw a free-body diagram showing ALL the forces acting on the crate as it moves down the incline.", 3, [
        ["w: Fw / Fg / mg / gravitational force / 29,4 N / weight, vertically downwards", 1],
        ["f: Ff / fk / (kinetic) friction / 21 N, up the incline", 1], ["N: FN / normal (force), perpendicular to the incline", 1]],
        ["Three forces once F is gone.", "Friction opposes the motion down the slope; N is perpendicular to the slope."],
        memo="A mark for each label AND its arrow. Any additional force(s), no arrows, or forces not touching the dot: max 2/3."),
    # "decide by calculation" (2026-10-10): as a rubric of the memo's options a strong learner's working scored 0 / 5 (numbers, no words to
    # match); played as the memo's Option 5, the marks riding on its two numbers, the conclusion on the distance (7,68 m > 6,8 m)
    steps("5.4", "Using ENERGY PRINCIPLES ONLY, determine whether the crate will pass point C.", 5, [
        ("Net force along the slope opposing the crate's motion (N)", 2, 10.94, 0.05,
         "W(Fg) = (3)(9,8) sin 20° Δx cos 0° ✓ (gravity's component, 10,06 N, along the motion); W(f) = (21) Δx cos 180° ✓ (friction against it): "
         "21 − 10,06 = 10,94 N"),
        ("Distance the crate slides down the slope from B before it stops (m)", 3, 7.68, 0.05,
         "Wnet = ΔEk: [(3)(9,8) sin 20° − 21] Δx cos 0° = 0 − 84 ✓; Δx = 7,68 m ✓; 7,68 m > 6,8 m: the crate WILL pass point C ✓. "
         "(Any of the memo's five options: W(Fg), W(f) and ΔEk substituted, the answer, the conclusion; e.g. Ekf at C = 9,58 J > 0 J.) "
         "Accept cos 70° or sin 20° throughout.")],
        ["Down the slope gravity's component (3 × 9,8 × sin 20°) helps; friction (21 N) opposes.", "Work out how far the crate slides before its 84 J is used up, then compare with BC = 6,8 m."])]

# ---- QUESTION 6, the question paper page 12 and the memo pages 13-14 ----
q6 = [
    rub("6.1", "STATE the Doppler effect.", 2, [
        "The change in frequency (or pitch) of the sound detected by a listener, because the sound source and the listener have different velocities "
        "relative to the medium of sound propagation. (2)",
        "OR — An (apparent) change in (observed/detected) frequency (pitch) as a result of the relative motion between a sound source and an observer. (2)"],
        ["Think of an ambulance passing you: what changes?", "It is about the detected frequency and the relative motion."], each=2,
        notes=["Key words: change in frequency; source and listener; relative motion/different velocities. A key word omitted: deduct 1."]),
    term("6.2.1", "For this experiment, write down the independent variable.", ["Velocity of the ambulance", "Speed of the ambulance", "Velocity of the source",
                                                                                "Speed of the source", "vs"],
         ["What did the experimenters change on purpose?", "The graph's horizontal axis."]),
    term("6.2.2", "For this experiment, write down a controlled variable.", [
        "Frequency of the sound produced by the ambulance siren", "Frequency of the siren", "Wavelength of the sound produced by the siren", "fs",
        "Speed of sound", "Density of air", "Temperature of air", "The detector is stationary", "The listener is stationary"],
         ["What was kept the same in every run?", "Think of the siren itself, the air, or the detector."]),
    rub("6.3", "What conclusion can be made for Part B of this experiment?", 2, [
        "As the velocity of the ambulance increases, the detected frequency decreases. (2)"],
        ["Part B: the ambulance moves AWAY from the detector.", "Read the falling line: what happens to the frequency as the velocity grows?"], each=2,
        notes=["Inversely proportional indicated: 0/2."]),
    steps("6.4", "Calculate the speed of sound in air.", 6,
          [("Speed of sound in air (m·s⁻¹)", 6, 329.64, 0.5,
            "Approaching: fL = v/(v − vs) fs ✓ (either formula); 1298 = v/(v − 25) fs ✓, so vfs = 1298(v − 25) (1). Moving away: fL = v/(v + vs) fs; "
            "1115 = v/(v + 25) fs ✓, so vfs = 1115(v + 25) (2). (1) = (2): 1298(v − 25) = 1115(v + 25) ✓ (OR (1) ÷ (2): 1,164(v − 25) = v + 25); "
            "v = 329,64 m·s⁻¹ ✓")],
          ["Read the two detected frequencies at 25 m·s⁻¹: 1 298 Hz approaching, 1 115 Hz moving away.", "Two Doppler equations, two unknowns (v and fs): divide one by the other."])]

# ---- QUESTION 7, the question paper page 13 and the memo pages 14-15 ----
q7a = [
    rub("7.1", "Describe an electric field.", 2, ["A region of space in which an electric charge experiences a force. (2 or 0)"],
        ["Where in space does it exist?", "What happens to a charge placed there?"], each=2),
    draw("7.2", "Draw the electric field pattern due to the charge on sphere X.", 2, [
        ["Direction: arrows pointing away from the positive charge", 1], ["Field lines radially outward", 1]],
        ["X is positive.", "Field lines point the way a positive test charge would be pushed."],
        memo="Two or more field lines inside the sphere / not touching the sphere / crossing each other: deduct 1. More than one charge drawn: 0/2."),
    # "Show that" with a formula and its substitutions (2026-10-10, memo self-test: as a rubric the memo's own working scored 0 / 3, a
    # formula has no words to match): steps on the numbers the working produces BEFORE the given answer, the marks riding on them
    steps("7.3", "Show, by means of a calculation, that r = 0,05 m.", 3, [
        ("Product kQ (N·m²·C⁻¹)", 1, 2700, 1, "(9 × 10⁹)(3 × 10⁻⁷) ✓ = 2 700"),
        ("r² (m²)", 2, 0.0025, 0.00005, "E = kQ/r² ✓; 1,08 × 10⁶ ✓ = (9 × 10⁹)(3 × 10⁻⁷)/r²; r² = 2,5 × 10⁻³ m², so r = 0,05 m")],
        ["E is the field of a point charge: E = kQ/r².", "Work out kQ first, then r² = kQ / E."])]
q7b = [
    # "Choose ... by means of a calculation" (2026-10-10): as a rubric of the memo's options a strong learner's working scored 0 / 6; played as
    # Option 1, the marks riding on its three forces, "No" (1) and "Fnet(E) ≠ Fnet" (1) on the net force (0,14 N ≠ 0,0427 N: friction acts)
    steps("7.4", "The NET FORCE acting on sphere X is 0,0427 N at point A. Is the surface frictionless? Choose from YES or NO. Explain the answer by "
          "means of a calculation.", 6, [
        ("Electrostatic force of Y on X (N)", 2, 0.54, 0.005, "FXY = kQXQY/r² ✓ = (9 × 10⁹)(3 × 10⁻⁷)(5 × 10⁻⁷)/(0,05)² ✓ = 0,54 N"),
        ("Electrostatic force of Z on X (N)", 1, 0.675, 0.01, "FXZ = (9 × 10⁹)(3 × 10⁻⁷)(4 × 10⁻⁷)/(0,04)² ✓ = 0,68 N"),
        ("Net electrostatic force on X (N)", 3, 0.135, 0.01,
         "Fnet(E) = FXZ − FXY = 0,68 − 0,54 ✓ = 0,14 N; No ✓: Fnet(E) ≠ Fnet (0,14 N ≠ 0,0427 N), so friction acts ✓. "
         "(OR Enet = 450 000 N·C⁻¹, Fnet = qE = 0,14 N; OR 0,0427 = 0,14 − f, f = 0,0923 N.) Ignore negative charges substituted.")],
        ["Work out the electrostatic force from Y and from Z on X, then the net electrostatic force.", "If that is more than 0,0427 N, something else (friction) acts."]),
    mcq("7.5", "Sphere Y is brought into contact with sphere X, and is placed back in its original position. How will the magnitude of the force that "
        "sphere X now exerts on sphere Y be affected? Choose from INCREASES, DECREASES or REMAINS THE SAME.",
        ["Increases", "Decreases", "Remains the same"], 1,
        ["Touching shares the charge: (+3 + (−5))/2 each.", "Compare the product of the charges before and after."])]

# ---- QUESTION 8, the question paper page 14 and the memo pages 16-18 ----
q8 = [
    rub("8.1", "Define the term emf.", 2, [
        "Maximum/total energy provided/work done by a battery/cell per unit/coulomb of charge passing through it. (2 or 0)"],
        ["It is energy per charge.", "Energy provided by the battery for each coulomb."], each=2),
    steps("8.2", "Switch S1 remains open while switch S2 is closed. The reading on ammeter A2 is 120 A. Calculate the reading on the voltmeter.", 3,
          [("Reading on the voltmeter (V)", 3, 12, 0.05, "R = V/I ✓; 0,1 = V/120 ✓; V = 12 V ✓")],
          ["With only S2 closed, the voltmeter reads across the starter motor.", "V = IR with R = 0,1 Ω."]),
    steps("8.3.1", "Switch S1 is now closed and switch S2 is opened. The power dissipated by each headlight is 15 W. Calculate the current passing through L1.", 3,
          [("Current through L₁ (A)", 3, 1.12, 0.01, "P = I²R ✓; 15 = I²(12) ✓; I = 1,12 A ✓ (OR P = V²/R: V = 13,42 V, then P = VI or V = IR)")],
          ["You know each headlight's power and resistance.", "P = I²R."]),
    num("8.3.2", "Switch S1 is now closed and switch S2 is opened. Write down the reading on ammeter A1.", 2.24, 0.01, "A",
        ["A1 carries the current of both headlights.", "Two identical headlights, each with your current from 8.3.1."]),
    steps("8.4", "Calculate the emf of the battery.", 6, [
        ("Total resistance of the two headlights (Ω)", 1, 6, 0.01, "1/Rp = 1/12 + 1/12 ✓; Rp = 6 Ω"),
        ("Internal resistance of the battery (Ω)", 4, 0.012, 0.0006, "ε = I(R + r) ✓ = 2,24(6 + r) ✓; ε = 120(0,1 + r) ✓; equating: 2,24(6 + r) = 120(0,1 + r) ✓; r = 0,012 Ω"),
        ("emf of the battery (V)", 1, 13.445, 0.026, "ε = 2,24(6 + 0,012) = 13,46 V, OR ε = 120(0,1 + 0,012) = 13,47 V ✓. Range: 13,42 V – 13,47 V")],
        ["The emf is the same in both switch settings: ε = I(R + r).", "Write it twice (headlights, 2,24 A; starter motor, 120 A), set them equal and find r first."]),
    rub("8.5", "Both switches are now closed. How will the reading on ammeter A1 be affected? Choose from INCREASES, DECREASES or REMAINS THE SAME. "
        "Explain the answer WITHOUT the use of a calculation.", 5, [
        "Decrease (1).", "The total/external resistance decreases (1).", "The total current increases (1).", "V(internal) increases (1).",
        "The voltage across the light bulbs decreases / V(external) decreases (1)."],
        ["Closing S2 adds the starter motor (0,1 Ω) in parallel.", "More current from the battery means more 'lost volts' inside it."],
        notes=["A calculation given as the explanation: 1/5.",
               "ACCEPT (max 3/5): Increases (1) — the initial reading on A1 = 0 A when switch S1 is open (1); now both switches are closed and current "
               "flows through the circuit (1). The mark for 'increases' only if its explanation is correct."])]

# ---- QUESTION 9, the question paper page 15 and the memo pages 18-19 ----
q9a = [
    rub("9.1", "Define the term rms potential difference.", 2, [
        "The AC potential difference/voltage that produces/dissipates the same amount of energy as an equivalent DC potential difference/voltage. (2)"],
        ["It compares AC with DC.", "Which AC voltage gives the same energy (heating) as a DC voltage?"], each=2,
        notes=["DC written first / energy or heating effect omitted / alternating current defined: 0/2."]),
    term("9.2", "What is the polarity of the magnet at Z?", ["North", "N"],
         ["Use the right-hand rule for generators: the coil's motion and the induced current are shown.", "The field runs from the magnet's north to its south."], marks=2),
    steps("9.3", "The resistance of the fan is 60 Ω and the maximum potential difference produced by the generator is 311,11 V. Calculate the cost of "
          "operating the fan for 1,5 hours if the cost of electricity is R3,33 per kWh.", 5, [
        ("rms potential difference (V)", 1, 219.99, 0.05, "Vrms = Vmax/√2 = 311,11/√2 ✓ = 219,99 V"),
        ("Average power of the fan (W)", 2, 806.59, 0.5, "Pave = V²rms/R ✓ = (219,99)²/60 ✓ = 806,59 W = 0,80659 kW"),
        ("Cost of operating the fan (R)", 2, 4.03, 0.01, "cost = PΔt × tariff = 0,80659(1,5)(3,33) ✓ = R4,03 ✓ (OR E = PΔt = 1,21 kWh, cost = 1,21 × 3,33)")],
        ["Start from the rms voltage: Vrms = Vmax/√2.", "Power in kW x time in hours = kWh; then multiply by the tariff."])]
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
        ["It is an energy.", "The LEAST energy needed to free an electron from the surface."], each=2, notes=["Threshold frequency defined: 0/2."]),
    num("10.1.2", "Write down the threshold frequency of zinc.", 1.045e15, 0.001e15, "Hz",
        ["Zinc's electrons leave with zero kinetic energy at this frequency.", "Read the frequency the learners used."]),
    rub("10.1.3", "How does the work function of sodium compare to that of caesium? Choose from SMALLER THAN, GREATER THAN or EQUAL TO. Explain the answer.", 3, [
        "Greater than (1).", "The maximum kinetic energy of electrons from sodium is smaller (1).",
        "E is constant / the same frequency / the same light used (Ek(max) is smaller, W0 is larger) (1)."],
        ["E(photon) = W0 + Ek(max), and the light is the same for both.", "Which metal's electrons leave with less kinetic energy?"]),
    rub("10.1.4", "Light of the same frequency, but with a higher intensity, is now incident on metal M. Will electrons now be ejected? Choose from YES or NO. "
        "Give a reason for the answer.", 2, [
        "No (1).", "The intensity of light does not have any effect on the ejection of electrons for metal M (1), OR the frequency of light has not changed / "
        "the energy of a photon has not changed (1)."],
        ["Intensity is the number of photons, not the energy of each.", "Does each photon carry more energy now?"])]
q10b = [
    steps("10.2.1", "An electron of this atom moves from E3 to E1. Photon X is emitted. Calculate the frequency of photon X.", 4,
          [("Frequency of photon X (Hz)", 4, 6.64e14, 0.01e14, "E = hf ✓; 5,7 × 10⁻¹⁹ − 1,3 × 10⁻¹⁹ ✓ = (6,63 × 10⁻³⁴) f ✓; f = 6,64 × 10¹⁴ Hz ✓ "
            "(accept E3 − E1 or E1 − E3; f must be positive)")],
          ["The photon carries away the energy difference E3 − E1.", "E = hf, with h = 6,63 × 10⁻³⁴ J·s."]),
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
     "figure": fig("Q6", "Detected frequency (Hz) up against velocity of the ambulance (m·s⁻¹) across, 0 to 30. Two straight lines start at the same "
                   "frequency on the axis: one rises (Part A, approaching) to 1 298 Hz at 25 m·s⁻¹; one falls (Part B, moving away) to 1 115 Hz at "
                   "25 m·s⁻¹."), "items": q6},
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

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 10), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (formulas are images); no API call."},
        {"n": "2.3.2", "kind": "no_fit", "detail": "Calculations play as steps: each step is the number the memo's method produces, its formula and "
                                                   "substitution marks riding on that number (the phone sees numbers, not working). 4.2.1 asks for a "
                                                   "vector: the direction mark ('to the right') rides on the magnitude."},
        {"n": "5.4", "kind": "no_fit", "detail": "Decide-by-calculation parts play as steps on the memo's numbers (5.4: its Option 5, the net force along the slope and the distance before stopping; 7.4: its Option 1, the two forces on X and the net force). The conclusion's mark rides on the decisive number (7,68 m > 6,8 m; 0,14 N ≠ 0,0427 N). As written answers, a strong learner's full working scored 0 (2026-10-10). 7.3 (Show that r = 0,05 m) likewise plays the numbers before the given answer."},
        {"n": "2.2", "kind": "no_fit", "detail": "Drawings (2.2, 3.5, 4.3, 5.3, 7.2, 9.4) are done on paper and self-checked against the memo's criteria."},
        {"n": "3.3", "kind": "memo_issue", "detail": "The memo gives a range (17,93 – 18,33 m·s⁻¹): played as its centre 18,13 ± 0,20, the memo's 17,97 shown."},
        {"n": "8.4", "kind": "memo_issue", "detail": "The memo gives a range for the emf (13,42 V – 13,47 V): played as 13,445 ± 0,026."},
    ],
}
out = Path(__file__).parent / "out" / "ps-p1-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    print(m["id"], "parts:", len(m["items"]), "marks:", sum(i["marks"] for i in m["items"]), "/", m["marks"])
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
